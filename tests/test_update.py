import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_site import PUBLIC_DATA, build
from scripts.update import build_status, stage_health


class UpdatePipelineTests(unittest.TestCase):
    def outcome(self, identifier, exit_code=0):
        return {
            "id": identifier,
            "exit_code": exit_code,
            "duration_ms": 10,
            "completed_at": "2026-07-22T18:00:00+00:00",
            "message": "completed",
        }

    def test_news_source_failures_create_partial_health(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            report.write_text(json.dumps({
                "active_source_count": 10,
                "successful_source_count": 8,
                "failed_source_count": 2,
                "items_after_deduplication": 120,
            }), encoding="utf-8")
            with patch.dict("scripts.update.STAGE_META", {"news": ("News feeds", report)}):
                health = stage_health(self.outcome("news"))
        self.assertEqual(health["status"], "partial")
        self.assertEqual(health["issues"], 2)
        self.assertIn("8 of 10", health["summary"])

    def test_one_failed_stage_does_not_hide_other_current_stages(self):
        outcomes = [self.outcome("news", 1), self.outcome("trends"), self.outcome("markets", None)]
        payload = build_status(outcomes, generated_at="2026-07-22T18:00:00+00:00")
        self.assertEqual(payload["overall_status"], "partial")
        self.assertEqual(payload["stages"][0]["status"], "failed")
        self.assertEqual(payload["stages"][1]["status"], "current")
        self.assertEqual(payload["stages"][2]["status"], "skipped")

    def test_pending_translations_are_not_counted_as_issues(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            report.write_text(json.dumps({
                "published_auto_count": 63,
                "manual_translation_count": 0,
                "remaining_pending_count": 86,
                "provider": "gemini",
                "status": "partial",
                "errors": [],
            }), encoding="utf-8")
            with patch.dict("scripts.update.STAGE_META", {"enrichment": ("English edition", report)}):
                health = stage_health(self.outcome("enrichment"))
        # Untranslated stories are a budget decision, not a data problem: the
        # header badge must not read "86 data issues" forever.
        self.assertEqual(health["issues"], 0)
        self.assertEqual(health["status"], "current")
        self.assertIn("86 pending", health["summary"])

    def test_enrichment_errors_still_mark_the_stage_partial(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            report.write_text(json.dumps({
                "published_auto_count": 10,
                "remaining_pending_count": 0,
                "provider": "gemini",
                "errors": ["quota exceeded"],
            }), encoding="utf-8")
            with patch.dict("scripts.update.STAGE_META", {"enrichment": ("English edition", report)}):
                health = stage_health(self.outcome("enrichment"))
        self.assertEqual(health["issues"], 1)
        self.assertEqual(health["status"], "partial")

    def test_skip_fetch_does_not_stamp_the_stale_ingestion_report_as_fresh(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            report.write_text(json.dumps({
                "active_source_count": 10,
                "successful_source_count": 8,
                "failed_source_count": 2,
                "items_after_deduplication": 120,
            }), encoding="utf-8")
            outcome = self.outcome("news")
            outcome["reused_articles"] = True
            with patch.dict("scripts.update.STAGE_META", {"news": ("News feeds", report)}):
                health = stage_health(outcome)
        self.assertIn("cached articles", health["summary"])
        self.assertEqual(health["issues"], 0)

    def test_public_build_excludes_private_audit_json(self):
        with tempfile.TemporaryDirectory() as directory:
            output = build(Path(directory) / "dist")
            self.assertTrue((output / "index.html").exists())
            self.assertTrue(all((output / "data" / name).exists() for name in PUBLIC_DATA))
            self.assertFalse((output / "data" / "articles.json").exists())
            self.assertFalse((output / "scripts").exists())


if __name__ == "__main__":
    unittest.main()
