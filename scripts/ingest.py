"""Fetch, normalize, filter, and deduplicate RSS/Atom feeds for MISE.

This intentionally stores only feed-provided metadata and excerpts. It does not
download publisher images or crawl article bodies.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data" / "sources.json"
DEFAULT_OUTPUT = ROOT / "data" / "articles.json"
DEFAULT_REPORT = ROOT / "data" / "ingestion-report.json"
USER_AGENT = "MISE-News-Prototype/0.1 (+local development; metadata-only RSS reader)"
TRACKING_PARAMS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "source"}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def strip_markup(value: str | None, limit: int = 480) -> str:
    if not value:
        return ""
    parser = TextExtractor()
    try:
        parser.feed(html.unescape(value))
        text = " ".join(parser.parts)
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html.unescape(value))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rsplit(" ", 1)[0] + "…"
    return text


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def child_text(element: ET.Element, names: set[str]) -> str:
    for child in list(element):
        if local_name(child.tag) in names and child.text:
            return child.text.strip()
    return ""


def first_descendant_text(element: ET.Element, names: set[str]) -> str:
    for child in element.iter():
        if local_name(child.tag) in names and child.text:
            return child.text.strip()
    return ""


def extract_link(element: ET.Element) -> str:
    for child in list(element):
        if local_name(child.tag) != "link":
            continue
        href = child.attrib.get("href", "").strip()
        rel = child.attrib.get("rel", "alternate")
        if href and rel in {"alternate", ""}:
            return href
        if child.text and child.text.strip().startswith(("http://", "https://")):
            return child.text.strip()
    guid = child_text(element, {"guid", "id"})
    return guid if guid.startswith(("http://", "https://")) else ""


def extract_image_url(element: ET.Element, description: str) -> str | None:
    for child in element.iter():
        name = local_name(child.tag)
        url = child.attrib.get("url") or child.attrib.get("href")
        media_type = child.attrib.get("type", "")
        if url and (name in {"thumbnail", "content"} or media_type.startswith("image/")):
            return url.strip()
        if name == "enclosure" and url and media_type.startswith("image/"):
            return url.strip()
    match = re.search(r"<img[^>]+src=[\"']([^\"']+)", description or "", re.IGNORECASE)
    return html.unescape(match.group(1)) if match else None


def canonical_url(value: str) -> str:
    if not value:
        return ""
    parsed = urllib.parse.urlsplit(value.strip())
    kept_query = []
    for key, val in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in TRACKING_PARAMS:
            continue
        kept_query.append((key, val))
    return urllib.parse.urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), urllib.parse.urlencode(kept_query), "")
    )


def parse_date(value: str) -> str | None:
    if not value:
        return None
    parsed: datetime | None = None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def matches_term(haystack: str, term: str) -> bool:
    normalized = term.casefold().strip()
    if not normalized:
        return False
    if len(normalized) <= 5 and normalized.replace("&", "").isalnum():
        return re.search(rf"(?<!\w){re.escape(normalized)}(?!\w)", haystack) is not None
    return normalized in haystack


def matches_filter(
    title: str,
    summary: str,
    terms: list[str],
    excluded_terms: list[str],
    scope_terms: list[str] | None = None,
) -> bool:
    haystack = f"{title} {summary}".casefold()
    if any(matches_term(haystack, term) for term in excluded_terms):
        return False
    if scope_terms and not any(matches_term(haystack, term) for term in scope_terms):
        return False
    if not terms:
        return True
    return any(matches_term(haystack, term) for term in terms)


def infer_topic(title: str, summary: str, fallback: str) -> str:
    text = f"{title} {summary}".casefold()
    rules = [
        ("Sustainability", ["sustainab", "climate", "waste", "organic", "bio ", "klima", "nachhalt", "recycling"]),
        ("People", ["chef", "koch", "award", "guide", "michelin", "winner", "sommelier", "auszeichnung"]),
        ("Food & Wine", ["wine", "wein", "beer", "bier", "coffee", "kaffee", "ingredient", "lebensmittel", "recipe"]),
        ("Business", ["market", "sales", "revenue", "cost", "labour", "labor", "staff", "business", "industry", "steuer", "umsatz"]),
        ("Restaurants", ["restaurant", "gastronom", "dining", "menu", "café", "cafe", "opening", "eröffnet"]),
    ]
    for topic, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return topic
    return fallback


def parse_entries(xml_bytes: bytes) -> list[ET.Element]:
    root = ET.fromstring(xml_bytes)
    entries = [element for element in root.iter() if local_name(element.tag) in {"item", "entry"}]
    return entries


def fetch_feed(source: dict, timeout: int) -> tuple[list[dict], dict]:
    started = time.monotonic()
    request = urllib.request.Request(
        source["feed_url"],
        headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read(5_000_000)
        content_type = response.headers.get("Content-Type", "")

    articles: list[dict] = []
    entries = parse_entries(payload)
    for entry in entries[: int(source.get("max_items", 25)) * 3]:
        title = strip_markup(child_text(entry, {"title"}), limit=240)
        raw_description = child_text(entry, {"description", "summary", "content", "encoded"})
        if not raw_description:
            raw_description = first_descendant_text(entry, {"description", "summary", "content", "encoded"})
        summary = strip_markup(raw_description)
        url = canonical_url(extract_link(entry))
        if not title or not url or not matches_filter(
            title,
            "" if source.get("filter_title_only") else summary,
            source.get("filter_terms", []),
            source.get("exclude_terms", []),
            source.get("scope_terms", []),
        ):
            continue
        published_raw = child_text(entry, {"pubdate", "published", "updated", "date"})
        published_at = parse_date(published_raw)
        identifier = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
        articles.append(
            {
                "id": identifier,
                "edition": source["edition"],
                "country": source["country"],
                "language": source["language"],
                "source_id": source["id"],
                "source_name": source["name"],
                "source_type": source["source_type"],
                "access": source.get("access", "open"),
                "corroboration_role": source.get(
                    "corroboration_role",
                    "official_primary" if source["source_type"] == "official" else "independent_editorial",
                ),
                "title": title,
                "summary": summary,
                "url": url,
                "published_at": published_at,
                "image_url": extract_image_url(entry, raw_description),
                "topic": infer_topic(title, summary, source["default_topic"]),
            }
        )
        if len(articles) >= int(source.get("max_items", 25)):
            break

    return articles, {
        "source_id": source["id"],
        "status": "ok",
        "items_seen": len(entries),
        "items_kept": len(articles),
        "content_type": content_type,
        "duration_ms": round((time.monotonic() - started) * 1000),
    }


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.casefold())[:180]


def deduplicate(articles: list[dict]) -> list[dict]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    result: list[dict] = []
    for article in articles:
        normalized_title = title_key(article["title"])
        if article["url"] in seen_urls or normalized_title in seen_titles:
            continue
        seen_urls.add(article["url"])
        seen_titles.add(normalized_title)
        result.append(article)
    return result


def sort_key(article: dict) -> str:
    return article.get("published_at") or "1970-01-01T00:00:00Z"


def write_outputs(articles: list[dict], report: dict, output: Path, report_path: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "generated_at": report["generated_at"],
        "source_count": report["successful_source_count"],
        "article_count": len(articles),
        "articles": articles,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--timeout", type=int, default=18)
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    active_sources = [
        source
        for source in registry["sources"]
        if source.get("status") == "active" and source.get("ingestion_mode") == "rss" and source.get("feed_url")
    ]

    fetched: list[dict] = []
    source_reports: list[dict] = []
    for source in active_sources:
        try:
            articles, source_report = fetch_feed(source, args.timeout)
            fetched.extend(articles)
            source_reports.append(source_report)
            print(f"{source['id']}: kept {len(articles)}", file=sys.stderr)
        except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as error:
            source_reports.append(
                {
                    "source_id": source["id"],
                    "status": "error",
                    "error": str(error),
                    "items_kept": 0,
                }
            )
            print(f"{source['id']}: ERROR {error}", file=sys.stderr)

    fetched.sort(key=sort_key, reverse=True)
    articles = deduplicate(fetched)
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    report = {
        "schema_version": 1,
        "generated_at": generated_at,
        "active_source_count": len(active_sources),
        "successful_source_count": sum(1 for item in source_reports if item["status"] == "ok"),
        "failed_source_count": sum(1 for item in source_reports if item["status"] == "error"),
        "items_before_deduplication": len(fetched),
        "items_after_deduplication": len(articles),
        "sources": source_reports,
    }
    article_payload = write_outputs(articles, report, args.output, args.report)
    from cluster import DEFAULT_CLUSTERS, DEFAULT_JS, build_payload, write_payload

    cluster_payload = build_payload(article_payload, registry)
    write_payload(cluster_payload, DEFAULT_CLUSTERS, DEFAULT_JS)
    report["cluster_count"] = cluster_payload["cluster_count"]
    report["multi_source_cluster_count"] = cluster_payload["multi_source_cluster_count"]
    report["independently_corroborated_cluster_count"] = cluster_payload[
        "independently_corroborated_cluster_count"
    ]
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["successful_source_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
