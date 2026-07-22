"""Audit candidate publishers for discoverable feeds and official social links.

This tool reads public home pages and feed endpoints only. It does not bypass
logins, consent walls, robots controls, or paywalls, and it never crawls article
bodies. Results are leads for manual source review, not automatic permission.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "source-candidates.json"
DEFAULT_OUTPUT = ROOT / "data" / "source-audit.json"
USER_AGENT = "MISE-Source-Audit/0.1 (+local development; feed discovery only)"
SOCIAL_HOSTS = {
    "instagram.com": "instagram",
    "www.instagram.com": "instagram",
    "facebook.com": "facebook",
    "www.facebook.com": "facebook",
    "linkedin.com": "linkedin",
    "www.linkedin.com": "linkedin",
    "at.linkedin.com": "linkedin",
    "youtube.com": "youtube",
    "www.youtube.com": "youtube",
    "x.com": "x",
    "www.x.com": "x",
    "twitter.com": "x",
    "www.twitter.com": "x",
    "tiktok.com": "tiktok",
    "www.tiktok.com": "tiktok",
}


class DiscoveryParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.feeds: set[str] = set()
        self.social: dict[str, set[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.casefold(): value or "" for key, value in attrs}
        href = values.get("href", "").strip()
        if not href:
            return
        absolute = urllib.parse.urljoin(self.base_url, href)
        if tag.casefold() == "link":
            rel = values.get("rel", "").casefold()
            media_type = values.get("type", "").casefold()
            if "alternate" in rel and any(marker in media_type for marker in ("rss", "atom", "xml")):
                self.feeds.add(absolute)
        if tag.casefold() == "a":
            host = urllib.parse.urlsplit(absolute).netloc.casefold()
            platform = SOCIAL_HOSTS.get(host)
            if platform:
                self.social.setdefault(platform, set()).add(absolute)


def request_bytes(url: str, timeout: int) -> tuple[bytes, str, int]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, text/html;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(4_000_000), response.headers.get("Content-Type", ""), response.status


def looks_like_feed(payload: bytes) -> tuple[bool, int]:
    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        return False, 0
    root_name = root.tag.rsplit("}", 1)[-1].casefold()
    entries = sum(1 for element in root.iter() if element.tag.rsplit("}", 1)[-1].casefold() in {"item", "entry"})
    return root_name in {"rss", "feed", "rdf"} and entries > 0, entries


def common_feed_candidates(homepage_url: str) -> list[str]:
    parsed = urllib.parse.urlsplit(homepage_url)
    root = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    candidates = [
        urllib.parse.urljoin(root + "/", "feed/"),
        urllib.parse.urljoin(root + "/", "rss/"),
        urllib.parse.urljoin(root + "/", "rss.xml"),
        urllib.parse.urljoin(root + "/", "feed.xml"),
    ]
    return list(dict.fromkeys(candidates))


def audit_candidate(candidate: dict, timeout: int) -> dict:
    started = time.monotonic()
    result = {**candidate, "homepage_status": "error", "feeds": [], "social_urls": {}, "errors": []}
    discovered_feeds: list[str] = []
    try:
        payload, content_type, status = request_bytes(candidate["homepage_url"], timeout)
        result["homepage_status"] = "ok"
        result["homepage_http_status"] = status
        result["homepage_content_type"] = content_type
        parser = DiscoveryParser(candidate["homepage_url"])
        parser.feed(payload.decode("utf-8", errors="replace"))
        discovered_feeds.extend(sorted(parser.feeds))
        result["social_urls"] = {platform: sorted(urls)[:4] for platform, urls in parser.social.items()}
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        result["errors"].append(f"homepage: {error}")

    feed_candidates = list(dict.fromkeys(discovered_feeds + common_feed_candidates(candidate["homepage_url"])))
    for feed_url in feed_candidates[:8]:
        try:
            payload, content_type, status = request_bytes(feed_url, timeout)
            valid, entries = looks_like_feed(payload)
            if valid:
                result["feeds"].append(
                    {"url": feed_url, "entries": entries, "http_status": status, "content_type": content_type}
                )
        except (urllib.error.URLError, TimeoutError, OSError):
            continue

    result["duration_ms"] = round((time.monotonic() - started) * 1000)
    result["recommendation"] = "rss_review" if result["feeds"] else "manual_or_publisher_review"
    if candidate.get("access") in {"paid", "paid_or_mixed"}:
        result["recommendation"] = "licensed_access_review"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    candidates = json.loads(args.input.read_text(encoding="utf-8"))["candidates"]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(audit_candidate, candidate, args.timeout): candidate for candidate in candidates}
        for future in concurrent.futures.as_completed(futures):
            candidate = futures[future]
            try:
                result = future.result()
            except Exception as error:  # Keep the audit moving when one publisher behaves unexpectedly.
                result = {**candidate, "homepage_status": "error", "feeds": [], "social_urls": {}, "errors": [str(error)]}
            results.append(result)
            print(f"{result['id']}: {len(result.get('feeds', []))} feed(s), {result.get('recommendation', 'error')}")

    order = {candidate["id"]: index for index, candidate in enumerate(candidates)}
    results.sort(key=lambda item: order[item["id"]])
    payload = {
        "schema_version": 1,
        "candidate_count": len(results),
        "homepage_success_count": sum(1 for item in results if item.get("homepage_status") == "ok"),
        "feed_candidate_count": sum(1 for item in results if item.get("feeds")),
        "social_candidate_count": sum(1 for item in results if item.get("social_urls")),
        "results": results,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in payload if key != "results"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
