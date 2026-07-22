import unittest
from datetime import date

from scripts.update_events import (
    build_calendar,
    deduplicate,
    discover_candidates,
    is_upcoming,
    validate_markers,
)


class EventUpdaterTests(unittest.TestCase):
    def test_marker_validation_normalizes_dash_styles_and_case(self):
        markup = "<html><body><h1>Vienna Coffee Festival</h1><p>11.–13. SEPTEMBER 2026</p></body></html>"
        valid, missing = validate_markers(markup, ["vienna coffee festival", "11.-13. September 2026"])
        self.assertTrue(valid)
        self.assertEqual(missing, [])

    def test_expired_events_are_removed(self):
        self.assertFalse(is_upcoming({"startDate": "2025-01-01", "endDate": "2025-01-02"}, date(2026, 7, 22)))
        self.assertTrue(is_upcoming({"startDate": "2026-07-22", "endDate": "2026-07-22"}, date(2026, 7, 22)))

    def test_duplicate_events_collapse_on_title_date_and_city(self):
        event = {"title": "Food Fair 2026", "startDate": "2026-09-01", "city": "Vienna"}
        duplicate = {"title": "Food Fair 2026!", "startDate": "2026-09-01", "city": "VIENNA"}
        self.assertEqual(len(deduplicate([event, duplicate])), 1)

    def test_failed_source_keeps_cached_event_but_marks_it_stale(self):
        registry = {
            "sources": [{
                "id": "official-event",
                "active": True,
                "url": "https://organizer.example/event",
                "required_markers": ["Official Event", "September 2026"],
                "event": {
                    "id": "official-event-2026", "title": "Official Event",
                    "startDate": "2026-09-01", "endDate": "2026-09-02",
                    "city": "Vienna", "region": "vienna", "source": "Organizer",
                },
            }]
        }
        cached = {"events": [{
            "id": "official-event-2026", "sourceId": "official-event", "title": "Official Event",
            "startDate": "2026-09-01", "endDate": "2026-09-02", "city": "Vienna",
            "region": "vienna", "source": "Organizer", "lastVerified": "2026-07-20",
        }]}

        def failing_fetcher(_url):
            raise OSError("offline")

        payload, report = build_calendar(
            registry, failing_fetcher, today=date(2026, 7, 22), cached_payload=cached
        )
        self.assertEqual(payload["events"][0]["verificationStatus"], "stale")
        self.assertEqual(report["errorSourceCount"], 1)

    def test_feed_event_lead_needs_official_verification(self):
        clusters = {"clusters": [{
            "id": "candidate-1", "edition": "austria",
            "title": "Food festival will take place in September 2026",
            "summary": "Save the date for the upcoming tasting.",
            "published_at": "2026-07-21T10:00:00Z",
            "sources": [{"source_name": "Trade Press", "url": "https://publisher.example/story"}],
        }]}
        candidates = discover_candidates(clusters, set(), today=date(2026, 7, 22))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["status"], "needs_official_date_verification")


if __name__ == "__main__":
    unittest.main()
