import http.client
import unittest
import xml.etree.ElementTree as ET

from scripts.ingest import deduplicate, extract_image_url, ingest_sources, matches_filter, matches_term, parse_date


def article(source_id: str, url: str, title: str) -> dict:
    return {"source_id": source_id, "url": url, "title": title}


class FeedImageTests(unittest.TestCase):
    def test_image_is_read_from_media_content_and_from_inline_markup(self):
        entry = ET.fromstring(
            '<item xmlns:media="http://search.yahoo.com/mrss/">'
            '<media:content url="https://cdn.example/story.jpg" type="image/jpeg" />'
            "</item>"
        )
        self.assertEqual(extract_image_url(entry, ""), "https://cdn.example/story.jpg")

        bare = ET.fromstring("<item />")
        self.assertEqual(
            extract_image_url(bare, '<p><img src="https://cdn.example/inline.jpg"></p>'),
            "https://cdn.example/inline.jpg",
        )

    def test_entry_without_any_image_returns_none(self):
        self.assertIsNone(extract_image_url(ET.fromstring("<item />"), "<p>Kein Bild.</p>"))


class IngestionDeduplicationTests(unittest.TestCase):
    def test_matching_titles_from_different_publishers_survive_for_clustering(self):
        items = [
            article("publisher-one", "https://one.example/story", "Vienna restaurant opens"),
            article("publisher-two", "https://two.example/story", "Vienna restaurant opens"),
        ]

        self.assertEqual(len(deduplicate(items)), 2)

    def test_duplicate_title_within_one_publisher_is_removed(self):
        items = [
            article("publisher", "https://example.com/one", "Vienna restaurant opens"),
            article("publisher", "https://example.com/two", "Vienna restaurant opens"),
        ]

        self.assertEqual(len(deduplicate(items)), 1)

    def test_duplicate_url_is_removed_across_publishers(self):
        items = [
            article("publisher-one", "https://example.com/story", "First title"),
            article("publisher-two", "https://example.com/story", "Second title"),
        ]

        self.assertEqual(len(deduplicate(items)), 1)


class ParseDateTests(unittest.TestCase):
    def test_rfc2822_and_iso_dates_normalize_to_utc_z(self):
        self.assertEqual(parse_date("Tue, 22 Jul 2026 08:30:00 +0200"), "2026-07-22T06:30:00Z")
        self.assertEqual(parse_date("2026-07-22T06:30:00Z"), "2026-07-22T06:30:00Z")
        self.assertEqual(parse_date("2026-07-22T08:30:00+02:00"), "2026-07-22T06:30:00Z")

    def test_naive_timestamp_is_assumed_utc(self):
        self.assertEqual(parse_date("2026-07-22T06:30:00"), "2026-07-22T06:30:00Z")

    def test_unparseable_dates_return_none_instead_of_raising(self):
        self.assertIsNone(parse_date(""))
        self.assertIsNone(parse_date("22. Juli 2026"))
        self.assertIsNone(parse_date("gestern"))


class TermMatchingTests(unittest.TestCase):
    def test_short_terms_require_word_boundaries(self):
        # "wein" must not fire inside "weinen" (crying) or "Schweinefleisch".
        self.assertTrue(matches_term("neuer wein aus der wachau", "wein"))
        self.assertFalse(matches_term("sie musste weinen", "wein"))
        self.assertFalse(matches_term("schweinefleisch im angebot", "wein"))

    def test_longer_compound_terms_match_as_substrings(self):
        self.assertTrue(matches_term("das wirtshaussterben in tirol", "wirtshaus"))
        self.assertTrue(matches_term("weinbaugebiet wachau", "weinbau"))

    def test_sharp_s_terms_match_casefolded_text(self):
        # casefold() folds ß to "ss"; the haystack passed to matches_term is
        # casefolded, so a ß-carrying term must still land.
        haystack = "lokal auf der landstraße eröffnet".casefold()
        self.assertTrue(matches_term(haystack, "landstraße"))

    def test_exclude_and_scope_terms_gate_the_match(self):
        self.assertTrue(matches_filter("Wirtshaus eröffnet", "", ["wirtshaus"], []))
        self.assertFalse(matches_filter("Wirtshaus eröffnet", "", ["wirtshaus"], ["eröffnet"]))
        self.assertFalse(matches_filter("Wirtshaus eröffnet", "", ["wirtshaus"], [], ["salzburg"]))
        self.assertTrue(matches_filter("Wirtshaus in Salzburg", "", ["wirtshaus"], [], ["salzburg"]))


class SourceIsolationTests(unittest.TestCase):
    def test_one_failing_feed_only_costs_that_source(self):
        sources = [{"id": "broken"}, {"id": "healthy"}]

        def fetcher(source, timeout):
            if source["id"] == "broken":
                raise http.client.IncompleteRead(b"partial")
            return [article("healthy", "https://ok.example/story", "Story")], {
                "source_id": "healthy",
                "status": "ok",
                "items_kept": 1,
            }

        fetched, reports = ingest_sources(sources, timeout=1, fetcher=fetcher)
        self.assertEqual(len(fetched), 1)
        self.assertEqual([report["status"] for report in reports], ["error", "ok"])


if __name__ == "__main__":
    unittest.main()
