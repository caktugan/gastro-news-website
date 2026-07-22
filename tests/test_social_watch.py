import unittest

from scripts.build_social_watch import build_payload, channel_links


class SocialWatchTests(unittest.TestCase):
    def test_only_public_https_links_enter_browser_payload(self):
        channel = {"url": "http://insecure.example", "urls": ["https://public.example", "javascript:alert(1)"]}
        self.assertEqual(channel_links(channel), ["https://public.example"])

    def test_payload_contains_no_post_or_username_content(self):
        source = {
            "updated_at": "2026-07-22",
            "policy": {"publication_rule": "Label posts.", "automation": "Use approved access."},
            "channels": [{
                "id": "reddit-wien", "name": "r/wien", "platform": "reddit",
                "url": "https://www.reddit.com/r/wien/", "status": "api_review",
                "posts": [{"username": "private-user", "body": "not for publication"}],
            }],
        }
        payload = build_payload(source)
        rendered = str(payload)
        self.assertEqual(payload["channel_count"], 1)
        self.assertNotIn("private-user", rendered)
        self.assertNotIn("not for publication", rendered)
        self.assertEqual(payload["ai_requests"], 0)
        self.assertEqual(payload["status"], "catalogued_unverified")


if __name__ == "__main__":
    unittest.main()
