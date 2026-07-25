import tempfile
import unittest
from pathlib import Path

from scripts.cluster import build_clusters, build_payload, shared_entities, write_payload


class ClusterMetadataTests(unittest.TestCase):
    def test_cluster_preserves_image_candidate_and_review_status(self):
        articles = [{
            "id": "story-1",
            "edition": "austria",
            "language": "de",
            "topic": "Restaurants",
            "title": "Neues Restaurant eröffnet in Wien",
            "summary": "Ein neues Restaurant hat im siebten Bezirk eröffnet.",
            "published_at": "2026-07-22T08:00:00Z",
            "source_id": "publisher",
            "source_name": "Publisher",
            "source_type": "local_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "AT",
            "url": "https://example.com/story",
            "image_url": "https://example.com/story.jpg",
        }]

        cluster = build_clusters(articles, {"publisher": 100})[0]

        self.assertEqual(cluster["image_url"], "https://example.com/story.jpg")
        # No image_usage on the article means it predates the provenance field.
        self.assertEqual(cluster["image_usage"], "review_required")
        self.assertEqual(cluster["review_status"], "source_metadata_only")
        self.assertEqual(cluster["sources"][0]["image_url"], "https://example.com/story.jpg")

    def test_paraphrased_titles_cluster_on_shared_venue_name(self):
        base = {
            "edition": "austria",
            "language": "de",
            "topic": "Openings",
            "published_at": "2026-07-22T08:00:00Z",
            "source_type": "trade_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "AT",
            "image_url": None,
        }
        articles = [
            {
                **base,
                "id": "one",
                "source_id": "publisher-one",
                "source_name": "Publisher One",
                "title": "Neues Bistro setzt auf leichte Kueche",
                "summary": 'Barbara Aichinger eroeffnet ihr Bistro "Mini Mayr" in der Josefstadt.',
                "url": "https://example.com/one",
            },
            {
                **base,
                "id": "two",
                "source_id": "publisher-two",
                "source_name": "Publisher Two",
                "title": "Neueroeffnung: Mini Mayr",
                "summary": "Mini Mayr verbindet Genuss und bewusstes Essen in Wien.",
                "url": "https://example.com/two",
            },
        ]

        clusters = build_clusters(articles, {"publisher-one": 10, "publisher-two": 20})

        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["source_count"], 2)
        self.assertEqual(clusters[0]["coverage_pattern"], "independently_reported")

    def test_feed_provided_image_provenance_survives_clustering(self):
        base = {
            "edition": "austria",
            "language": "de",
            "topic": "Restaurants",
            "published_at": "2026-07-22T08:00:00Z",
            "source_id": "publisher",
            "source_name": "Publisher",
            "source_type": "local_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "AT",
            "url": "https://example.com/story",
        }
        with_image = build_clusters(
            [{**base, "id": "a", "title": "Lokal eroeffnet", "summary": "",
              "image_url": "https://cdn.example/a.jpg", "image_usage": "feed_provided"}],
            {"publisher": 100},
        )[0]
        without_image = build_clusters(
            [{**base, "id": "b", "title": "Kein Bild dabei", "summary": "",
              "image_url": None, "image_usage": "none"}],
            {"publisher": 100},
        )[0]

        self.assertEqual(with_image["image_usage"], "feed_provided")
        self.assertEqual(without_image["image_usage"], "none")

    def test_brand_named_only_in_the_excerpt_still_clusters(self):
        """German binds a brand to the noun before it, so the same company is
        extracted as differently-bracketed phrases across publishers."""
        base = {
            "edition": "austria",
            "language": "de",
            "topic": "Restaurants",
            "source_type": "trade_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "AT",
            "image_url": None,
        }
        articles = [
            {
                **base,
                "id": "one",
                "source_id": "rolling-pin",
                "source_name": "Rolling Pin",
                "published_at": "2026-07-23T12:31:02Z",
                "title": "Figlmueller macht das Wiener Schnitzel zum Schmuckstueck",
                "summary": "Das Wiener Traditionshaus Figlmueller und die Schmuckmarke ARION Jewelry "
                           "bringen eine limitierte Schnitzelkette auf den Markt.",
                "url": "https://example.com/one",
            },
            {
                **base,
                "id": "two",
                "source_id": "gastro-at",
                "source_name": "GASTRO.at",
                "published_at": "2026-07-23T12:26:20Z",
                "title": "ARION Jewelry und Figlmueller praesentieren exklusive Schnitzelkette",
                "summary": "Die Wiener Schmuckmarke ARION Jewelry und Figlmueller haben sich "
                           "zusammengetan.",
                "url": "https://example.com/two",
            },
        ]

        clusters = build_clusters(articles, {"rolling-pin": 80, "gastro-at": 70})

        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["source_count"], 2)

    def test_incidental_excerpt_mention_does_not_cluster(self):
        """One shared two-word name, days apart, is context rather than one story."""
        base = {
            "edition": "austria",
            "language": "de",
            "topic": "Restaurants",
            "source_type": "trade_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "AT",
            "image_url": None,
        }
        articles = [
            {
                **base,
                "id": "one",
                "source_id": "ahgz",
                "source_name": "AHGZ",
                "published_at": "2026-07-20T08:00:00Z",
                "title": "Salzburger Festspiele: Jedermann-Premiere in perfektem Rahmen",
                "summary": "Die Premiere verlief in feierlichem Rahmen.",
                "url": "https://example.com/one",
            },
            {
                **base,
                "id": "two",
                "source_id": "kurier",
                "source_name": "KURIER",
                "published_at": "2026-07-22T17:24:00Z",
                "title": "Schinkenfleckerl und Gin Tonic an der Salzach",
                "summary": "Am Vorabend der Eroeffnung der Salzburger Festspiele bittet der "
                           "Gastgeber ins Cafe Bazar.",
                "url": "https://example.com/two",
            },
        ]

        clusters = build_clusters(articles, {"ahgz": 80, "kurier": 70})

        self.assertEqual(len(clusters), 2)

    def test_shared_entities_matches_by_containment(self):
        self.assertEqual(
            shared_entities({"schmuckmarke arion jewelry"}, {"arion jewelry"}),
            {"arion jewelry"},
        )
        self.assertEqual(shared_entities({"wiener schnitzel"}, {"arion jewelry"}), set())
        # a shorter phrase must be a whole-word run, not a substring
        self.assertEqual(shared_entities({"grand hotel sauerhof"}, {"hotel sauer"}), set())

    def test_publisher_boilerplate_does_not_chain_unrelated_articles(self):
        base = {
            "edition": "austria",
            "language": "de",
            "topic": "People",
            "published_at": "2026-07-22T08:00:00Z",
            "source_id": "rolling-pin",
            "source_name": "Rolling Pin",
            "source_type": "trade_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "AT",
            "image_url": None,
        }
        articles = [
            {
                **base,
                "id": "chef-change",
                "title": "Sternekoch verlaesst Hotelrestaurant",
                "summary": "Ein Kuechenchef wechselt den Betrieb. The post appeared first on Rolling Pin.",
                "url": "https://example.com/chef-change",
            },
            {
                **base,
                "id": "supplier-award",
                "title": "Auszeichnung fuer neuen Kuechengeraetehersteller",
                "summary": "Ein Lieferant gewinnt einen Preis. The post appeared first on Rolling Pin.",
                "url": "https://example.com/supplier-award",
            },
        ]

        self.assertEqual(len(build_clusters(articles, {"rolling-pin": 100})), 2)

    def test_one_similar_pair_does_not_mark_three_source_cluster_as_syndicated(self):
        base = {
            "edition": "global",
            "language": "en",
            "topic": "Business",
            "title": "Acme Dining Group announces expansion",
            "published_at": "2026-07-22T08:00:00Z",
            "source_type": "trade_press",
            "access": "open",
            "corroboration_role": "independent_editorial",
            "country": "US",
            "image_url": None,
        }
        articles = [
            {**base, "id": "one", "source_id": "one", "source_name": "One", "summary": "Acme Dining Group will open ten restaurants across Austria next year.", "url": "https://one.example/story"},
            {**base, "id": "two", "source_id": "two", "source_name": "Two", "summary": "Acme Dining Group will open ten restaurants across Austria next year.", "url": "https://two.example/story"},
            {**base, "id": "three", "source_id": "three", "source_name": "Three", "summary": "Executives linked the expansion to franchise demand and outlined staffing risks.", "url": "https://three.example/story"},
        ]

        result = build_clusters(articles, {"one": 10, "two": 20, "three": 30})

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["coverage_pattern"], "independently_reported")

    def test_independent_metric_and_browser_payload_contract(self):
        articles = []
        for suffix, source in (("one", "publisher-one"), ("two", "publisher-two")):
            articles.append({
                "id": suffix,
                "edition": "global",
                "language": "en",
                "topic": "Business",
                "title": "Acme Dining Group files annual results",
                "summary": (
                    "Profit rose as catering contracts expanded across regional markets."
                    if suffix == "one"
                    else "Executives outlined a new hospitality expansion strategy for the coming year."
                ),
                "published_at": "2026-07-22T08:00:00Z",
                "source_id": source,
                "source_name": source,
                "source_type": "trade_press",
                "access": "open",
                "corroboration_role": "independent_editorial",
                "country": "US",
                "url": f"https://example.com/{suffix}",
                "image_url": None,
            })
        registry = {"sources": [
            {"id": "publisher-one", "priority": 10},
            {"id": "publisher-two", "priority": 20},
        ]}

        payload = build_payload({"generated_at": "2026-07-22T09:00:00Z", "articles": articles}, registry)

        self.assertEqual(payload["independently_corroborated_cluster_count"], 1)
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = Path(temp_dir) / "clusters.json"
            js_path = Path(temp_dir) / "live-news.js"
            write_payload(payload, json_path, js_path)
            self.assertIn('"articles"', json_path.read_text(encoding="utf-8"))
            browser_bundle = js_path.read_text(encoding="utf-8")
            self.assertNotIn('"articles"', browser_bundle)
            self.assertNotIn('"article_id"', browser_bundle)
            self.assertIn('"coverage_pattern":"independently_reported"', browser_bundle)
            self.assertIn('"source_type":"trade_press"', browser_bundle)


if __name__ == "__main__":
    unittest.main()
