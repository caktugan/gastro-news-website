import unittest

from scripts.ingest import deduplicate


def article(source_id: str, url: str, title: str) -> dict:
    return {"source_id": source_id, "url": url, "title": title}


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
