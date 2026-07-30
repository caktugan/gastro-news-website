from __future__ import annotations

import contextlib
import copy
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import enrich_austria  # noqa: E402


def cluster(identifier: str, title: str) -> dict:
    return {
        "id": identifier,
        "edition": "austria",
        "language": "de",
        "title": title,
        "summary": "Hospitality industry update.",
        "published_at": "2026-07-21T12:00:00Z",
        "independent_source_count": 1,
        "sources": [{"source_id": "source", "title": title, "summary": "", "url": "https://example.com"}],
    }


def translated(identifier: str) -> dict:
    return {
        "id": identifier,
        "publish": True,
        "title": "English title",
        "deck": "Supported deck.",
        "summary": "A longer evidence-based summary containing only supported information.",
        "location": "Austria",
        "relevance_score": 80,
        "exclusion_reason": None,
    }


@contextlib.contextmanager
def enrichment_run(directory: str, provider: str, gemini_key: str, mistral_key: str):
    """Run main() against throwaway files with both provider keys configurable."""
    base = Path(directory)
    recent = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    clusters = []
    for index in range(2):
        item = cluster(f"{index:016x}", f"Wien restaurant story {index}")
        item["published_at"] = recent
        clusters.append(item)
    (base / "clusters.json").write_text(json.dumps({"clusters": clusters}), encoding="utf-8")
    (base / "sources.json").write_text(json.dumps({"sources": [{"id": "source", "priority": 50}]}), encoding="utf-8")

    argv = [
        "enrich_austria.py",
        "--clusters", str(base / "clusters.json"),
        "--sources", str(base / "sources.json"),
        "--manual", str(base / "missing-manual.js"),
        "--cache", str(base / "cache.json"),
        "--output", str(base / "auto.js"),
        "--report", str(base / "report.json"),
        "--usage-ledger", str(base / "usage.json"),
        "--batch-size", "1",
        "--max-api-requests", "10",
        "--provider", provider,
    ]
    previous_argv = sys.argv
    previous_env = {name: os.environ.get(name) for name in ("GEMINI_API_KEY", "MISTRAL_API_KEY")}
    sys.argv = argv
    os.environ["GEMINI_API_KEY"] = gemini_key
    os.environ["MISTRAL_API_KEY"] = mistral_key
    try:
        yield base
    finally:
        sys.argv = previous_argv
        for name, value in previous_env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


class ProviderFailoverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.real_gemini = enrich_austria.call_gemini
        self.real_mistral = enrich_austria.call_mistral
        self.calls: list[str] = []

    def tearDown(self) -> None:
        enrich_austria.call_gemini = self.real_gemini
        enrich_austria.call_mistral = self.real_mistral

    def _stub(self, name: str, fail_after: int | None = None, error: Exception | None = None):
        def call(api_key, model, batch, timeout, retries, reserve):
            self.calls.append(name)
            attempts = sum(1 for entry in self.calls if entry == name)
            if fail_after is not None and attempts > fail_after:
                raise error or RuntimeError(f"{name} unavailable")
            return [translated(item["id"]) for item in batch]
        return call

    def test_auto_hands_the_remaining_batches_to_the_fallback(self) -> None:
        budget = enrich_austria.DailyBudgetExceeded("gemini daily budget reached (10/10 UTC)")
        enrich_austria.call_gemini = self._stub("gemini", fail_after=1, error=budget)
        enrich_austria.call_mistral = self._stub("mistral")

        with tempfile.TemporaryDirectory() as directory:
            with enrichment_run(directory, "auto", "gemini-key", "mistral-key") as base:
                exit_code = enrich_austria.main()
            report = json.loads((base / "report.json").read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["processed_count"], 2)
        self.assertEqual(report["remaining_pending_count"], 0)
        self.assertEqual(report["providers_used"], ["gemini", "mistral"])
        self.assertEqual(report["provider"], "gemini → mistral")
        self.assertEqual(report["primary_provider"], "gemini")
        self.assertEqual(len(report["failover_notes"]), 1)
        self.assertIn("gemini handed over to mistral", report["failover_notes"][0])

    def test_fallback_covers_a_transport_failure_not_just_the_budget(self) -> None:
        enrich_austria.call_gemini = self._stub("gemini", fail_after=0, error=RuntimeError("HTTP 503"))
        enrich_austria.call_mistral = self._stub("mistral")

        with tempfile.TemporaryDirectory() as directory:
            with enrichment_run(directory, "auto", "gemini-key", "mistral-key") as base:
                enrich_austria.main()
            report = json.loads((base / "report.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["providers_used"], ["mistral"])
        self.assertEqual(report["processed_count"], 2)

    def test_explicit_provider_is_taken_literally_and_never_fails_over(self) -> None:
        enrich_austria.call_gemini = self._stub("gemini", fail_after=0, error=RuntimeError("HTTP 503"))
        enrich_austria.call_mistral = self._stub("mistral")

        with tempfile.TemporaryDirectory() as directory:
            with enrichment_run(directory, "gemini", "gemini-key", "mistral-key") as base:
                exit_code = enrich_austria.main()
            report = json.loads((base / "report.json").read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["status"], "partial_failure")
        self.assertEqual(report["providers_used"], [])
        self.assertNotIn("mistral", self.calls)

    def test_missing_fallback_key_leaves_single_provider_behaviour(self) -> None:
        budget = enrich_austria.DailyBudgetExceeded("gemini daily budget reached (10/10 UTC)")
        enrich_austria.call_gemini = self._stub("gemini", fail_after=0, error=budget)
        enrich_austria.call_mistral = self._stub("mistral")

        with tempfile.TemporaryDirectory() as directory:
            with enrichment_run(directory, "auto", "gemini-key", "") as base:
                enrich_austria.main()
            report = json.loads((base / "report.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "daily_budget_reached")
        self.assertNotIn("mistral", self.calls)
        self.assertEqual(list(report["daily_request_budget"]["by_provider"]), ["gemini"])


class EnrichmentTests(unittest.TestCase):
    def test_vienna_ranks_above_austria_and_foreign(self) -> None:
        now = datetime(2026, 7, 21, 13, tzinfo=timezone.utc)
        priorities = {"source": 50}
        vienna = enrich_austria.rank_score(cluster("1", "Restaurant opening in Wien"), priorities, now)
        austria = enrich_austria.rank_score(cluster("2", "Restaurant opening in Österreich"), priorities, now)
        foreign = enrich_austria.rank_score(cluster("3", "Restaurant opening in Berlin"), priorities, now)
        self.assertGreater(vienna, austria)
        self.assertGreater(austria, foreign)

    def test_signature_changes_with_source_evidence(self) -> None:
        original = cluster("1", "A title")
        changed = copy.deepcopy(original)
        changed["sources"][0]["summary"] = "New evidence"
        self.assertEqual(enrich_austria.source_signature(original), enrich_austria.source_signature(copy.deepcopy(original)))
        self.assertNotEqual(enrich_austria.source_signature(original), enrich_austria.source_signature(changed))

    def test_browser_output_only_publishes_current_non_manual_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "translations.js"
            current = cluster("current", "Current evidence")
            current["source_signature"] = enrich_austria.source_signature(current)
            stale = cluster("stale", "Changed evidence")
            stale["source_signature"] = enrich_austria.source_signature(stale)
            manual = cluster("manual", "Manual translation")
            manual["source_signature"] = enrich_austria.source_signature(manual)
            base = {
                "publish": True,
                "title": "English title",
                "deck": "Supported deck.",
                "summary": "Supported summary.",
                "location": "Austria",
                "relevance_score": 80,
                "generated_at": "2026-07-22T12:00:00Z",
                "model": "test-model",
                "provider": "gemini",
                "prompt_version": enrich_austria.PROMPT_VERSION,
            }
            cache = {"items": {
                "current": {**base, "source_signature": current["source_signature"]},
                "stale": {**base, "source_signature": "old-signature"},
                "manual": {**base, "source_signature": manual["source_signature"]},
            }}

            count = enrich_austria.write_browser_data(output, cache, [current, stale, manual], {"manual"})
            rendered = output.read_text(encoding="utf-8")

            self.assertEqual(count, 1)
            self.assertIn('"current"', rendered)
            self.assertNotIn('"stale"', rendered)
            self.assertNotIn('"manual"', rendered)

    def test_batch_validation_requires_every_id_once(self) -> None:
        stories = [cluster("1", "One"), cluster("2", "Two")]
        result = lambda identifier: {
            "id": identifier,
            "publish": True,
            "title": "English title",
            "deck": "Supported deck.",
            "summary": "A longer evidence-based summary containing only supported information.",
            "location": "Austria",
            "relevance_score": 80,
            "exclusion_reason": None,
        }
        validated = enrich_austria.validate_batch([result("1"), result("2")], stories)
        self.assertEqual(set(validated), {"1", "2"})
        with self.assertRaises(ValueError):
            enrich_austria.validate_batch([result("1")], stories)

    def test_manual_translation_ids(self) -> None:
        # Fixture data, not the live file: asserting against data/ made this
        # test fail on ordinary content edits rather than code bugs.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "austria-english.js"
            path.write_text(
                'window.MISE_AUSTRIA_ENGLISH = {"translations": {\n'
                '  "0123456789abcdef": {"title": "One"},\n'
                '  "fedcba9876543210": {"title": "Two"}\n'
                "}};\n",
                encoding="utf-8",
            )
            self.assertEqual(
                enrich_austria.manual_translation_ids(path),
                {"0123456789abcdef", "fedcba9876543210"},
            )
            self.assertEqual(enrich_austria.manual_translation_ids(Path(directory) / "missing.js"), set())

    def test_age_ceiling_excludes_old_and_undated_clusters(self) -> None:
        now = datetime.now(timezone.utc)
        fresh = cluster("f" * 16, "Wien aktuell")
        fresh["published_at"] = (now - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
        old = cluster("0" * 16, "Wien damals")
        old["published_at"] = (now - timedelta(days=120)).strftime("%Y-%m-%dT%H:%M:%SZ")
        undated = cluster("1" * 16, "Wien undatiert")
        undated["published_at"] = None

        selected = enrich_austria.select_clusters(
            [fresh, old, undated], [{"id": "source", "priority": 50}], limit=10
        )

        self.assertEqual([item["id"] for item in selected], ["f" * 16])

    def test_sharp_s_district_terms_receive_the_vienna_locality_boost(self) -> None:
        # Regression: the haystack is casefolded (ß→ss); un-folded terms like
        # "landstraße" could never match, silently dropping the Vienna boost.
        now = datetime.now(timezone.utc)
        district = cluster("a" * 16, "Neues Lokal auf der Landstraße")
        neutral = cluster("b" * 16, "Neues Lokal in der Innenstadt")
        priorities = {"source": 50}

        district_score = enrich_austria.rank_score(district, priorities, now)
        neutral_score = enrich_austria.rank_score(neutral, priorities, now)

        self.assertEqual(district_score - neutral_score, 260 - 30)

    def test_mistral_request_uses_strict_schema(self) -> None:
        request = enrich_austria.build_mistral_request("mistral-small-2603", [cluster("1", "Wien opening")])
        self.assertEqual(request["model"], "mistral-small-2603")
        self.assertEqual(request["response_format"]["type"], "json_schema")
        self.assertTrue(request["response_format"]["json_schema"]["strict"])
        self.assertEqual(request["messages"][0]["role"], "system")

    def test_mistral_completion_extraction(self) -> None:
        response = {"choices": [{"message": {"content": '{"items": []}'}}]}
        self.assertEqual(enrich_austria.extract_mistral_output_text(response), '{"items": []}')

    def test_gemini_request_uses_json_schema(self) -> None:
        request = enrich_austria.build_gemini_request([cluster("1", "Wien opening")])
        config = request["generationConfig"]
        self.assertEqual(config["responseMimeType"], "application/json")
        self.assertEqual(config["responseJsonSchema"]["type"], "object")
        self.assertEqual(request["contents"][0]["role"], "user")
        item_schema = config["responseJsonSchema"]["properties"]["items"]["items"]
        self.assertIn("summary", item_schema["required"])

    def test_gemini_completion_extraction(self) -> None:
        response = {"candidates": [{"content": {"parts": [{"text": '{"items": []}'}]}}]}
        self.assertEqual(enrich_austria.extract_gemini_output_text(response), '{"items": []}')

    def test_current_gemini_default_is_available_model(self) -> None:
        self.assertEqual(enrich_austria.DEFAULT_GEMINI_MODEL, "gemini-3.1-flash-lite")

    def test_headline_prompt_requires_variety_without_clickbait(self) -> None:
        instructions = enrich_austria.enrichment_instructions()
        self.assertIn("journalistic headline", instructions)
        self.assertIn("Vary headline rhythm", instructions)
        self.assertIn("Do not use clickbait", instructions)

    def test_daily_request_budget_is_persisted_and_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger_path = Path(directory) / "usage.json"
            first = enrich_austria.reserve_api_request(ledger_path, "gemini", 8, 2)
            second = enrich_austria.reserve_api_request(ledger_path, "gemini", 3, 2)
            self.assertEqual(first["request_count"], 1)
            self.assertEqual(second["request_count"], 2)
            self.assertEqual(second["item_count"], 11)
            with self.assertRaises(enrich_austria.DailyBudgetExceeded):
                enrich_austria.reserve_api_request(ledger_path, "gemini", 1, 2)
            saved = json.loads(ledger_path.read_text(encoding="utf-8"))
            totals = enrich_austria.usage_totals(saved, enrich_austria.usage_day(), "gemini")
            self.assertEqual(totals["request_count"], 2)

    def test_daily_limit_can_come_from_environment(self) -> None:
        previous = os.environ.get("MISE_DAILY_AI_REQUEST_LIMIT")
        os.environ["MISE_DAILY_AI_REQUEST_LIMIT"] = "9"
        try:
            self.assertEqual(enrich_austria.daily_request_limit(None), 9)
            self.assertEqual(enrich_austria.daily_request_limit(4), 4)
        finally:
            if previous is None:
                os.environ.pop("MISE_DAILY_AI_REQUEST_LIMIT", None)
            else:
                os.environ["MISE_DAILY_AI_REQUEST_LIMIT"] = previous


if __name__ == "__main__":
    unittest.main()
