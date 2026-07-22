from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
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
        ids = enrich_austria.manual_translation_ids(ROOT / "data" / "austria-english.js")
        self.assertGreaterEqual(len(ids), 40)

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
