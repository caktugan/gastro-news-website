import unittest
from datetime import datetime, timedelta, timezone

from scripts.build_trends import THEMES, build_payload, build_signals, coverage_label, theme_matches


def make_cluster(index, published_at, title, source=None):
    source_name = source or f"Publisher {index}"
    return {
        "id": f"cluster-{index}",
        "edition": "austria" if index % 2 else "global",
        "title": title,
        "summary": "Evidence summary.",
        "published_at": published_at.isoformat().replace("+00:00", "Z"),
        "source_count": 1,
        "sources": [{"source_name": source_name, "url": f"https://example.com/{index}"}],
    }


class TrendDetectionTests(unittest.TestCase):
    def test_coverage_label_is_about_share_not_raw_count(self):
        self.assertEqual(coverage_label(0.10, 0.10, 20), "Steady coverage")
        self.assertEqual(coverage_label(0.15, 0.10, 20), "Rising coverage")
        self.assertEqual(coverage_label(0.05, 0.10, 20), "Cooling coverage")
        self.assertEqual(coverage_label(0.20, 0.0, 8), "Current signal")

    def test_equal_coverage_share_stays_steady_when_window_sizes_differ(self):
        generated = datetime(2026, 7, 22, tzinfo=timezone.utc)
        clusters = []
        # Current window: 40 clusters, four technology matches (10%).
        for index in range(40):
            title = "Restaurant payment software launches" if index < 4 else "Chef publishes a new menu"
            clusters.append(make_cluster(index, generated - timedelta(days=2), title))
        # Previous window: 20 clusters, two technology matches (also 10%).
        for offset in range(20):
            index = 100 + offset
            title = "Digital ordering technology update" if offset < 2 else "Restaurant profile"
            clusters.append(make_cluster(index, generated - timedelta(days=18), title))
        payload = {
            "generated_at": generated.isoformat().replace("+00:00", "Z"),
            "clusters": clusters,
        }
        technology = next(signal for signal in build_signals(payload) if signal["id"] == "restaurant-technology")
        self.assertEqual(technology["status"], "Steady coverage")
        self.assertEqual(technology["coverage_delta_pp"], 0.0)

    def test_payload_records_zero_ai_requests(self):
        generated = datetime(2026, 7, 22, tzinfo=timezone.utc)
        source = {"generated_at": generated.isoformat().replace("+00:00", "Z"), "clusters": []}
        self.assertEqual(build_payload(source)["ai_requests"], 0)

    def test_closure_is_not_misclassified_as_expansion(self):
        expansion = next(theme for theme in THEMES if theme["id"] == "expansion-and-formats")
        self.assertTrue(theme_matches(expansion, "A group opens its first restaurant location"))
        self.assertFalse(theme_matches(expansion, "Restaurant closes after its opening 38 years ago due to insolvency"))
        self.assertFalse(theme_matches(expansion, "Comeback vor der Eröffnung geplatzt"))


if __name__ == "__main__":
    unittest.main()
