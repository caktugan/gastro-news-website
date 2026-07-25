import unittest
import xml.etree.ElementTree as ET

from scripts.ingest import deduplicate, extract_image_url


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


if __name__ == "__main__":
    unittest.main()
