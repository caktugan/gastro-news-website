#!/usr/bin/env python3
"""Verify official gastronomy events and build the MISE calendar payload."""

from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "event-sources.json"
CLUSTERS_PATH = ROOT / "data" / "clusters.json"
JSON_OUTPUT = ROOT / "data" / "events.json"
JS_OUTPUT = ROOT / "data" / "events.js"
REVIEW_OUTPUT = ROOT / "data" / "event-review.json"
REPORT_OUTPUT = ROOT / "data" / "event-update-report.json"
USER_AGENT = "MISE/1.0 (+local gastronomy industry calendar)"

EVENT_TERMS = re.compile(
    r"\b(festival|fair|trade show|tasting|seminar|workshop|conference|summit|expo|messe|"
    r"verkostung|kongress|weinwander|food week|masterclass|symposium)\b",
    re.IGNORECASE,
)
FUTURE_TERMS = re.compile(
    r"\b(upcoming|save the date|will take place|takes place|scheduled|findet statt|"
    r"termin|veranstaltung|lädt ein|ankuendigung|ankündigung)\b",
    re.IGNORECASE,
)


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def fetch_text(url: str, timeout: int = 25) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8-sig", errors="replace")


def page_text(markup: str) -> str:
    parser = VisibleTextParser()
    parser.feed(markup)
    return " ".join(html.unescape(" ".join(parser.parts)).split())


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKC", html.unescape(value or ""))
    value = value.replace("–", "-").replace("—", "-").replace("‑", "-")
    return " ".join(value.casefold().split())


def validate_markers(markup: str, markers: list[str]) -> tuple[bool, list[str]]:
    haystack = normalized(page_text(markup))
    missing = [marker for marker in markers if normalized(marker) not in haystack]
    return not missing, missing


def event_key(event: dict[str, Any]) -> tuple[str, str, str]:
    title = re.sub(r"[^a-z0-9]+", " ", normalized(event.get("title", ""))).strip()
    return title, event.get("startDate", ""), normalized(event.get("city", ""))


def deduplicate(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str]] = set()
    result = []
    for event in sorted(events, key=lambda item: (item.get("startDate", ""), item.get("title", ""))):
        key = event_key(event)
        if key in seen:
            continue
        seen.add(key)
        result.append(event)
    return result


def is_upcoming(event: dict[str, Any], today: date | None = None) -> bool:
    today = today or date.today()
    try:
        end = date.fromisoformat(event.get("endDate") or event["startDate"])
    except (KeyError, TypeError, ValueError):
        return False
    return end >= today


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def discover_candidates(cluster_payload: dict[str, Any], known_urls: set[str], today: date | None = None) -> list[dict[str, Any]]:
    today = today or date.today()
    cutoff = datetime.combine(today - timedelta(days=45), datetime.min.time(), tzinfo=timezone.utc)
    candidates = []
    for cluster in cluster_payload.get("clusters", []):
        published_raw = cluster.get("published_at")
        if not published_raw:
            continue
        try:
            published = datetime.fromisoformat(published_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            continue
        if published < cutoff:
            continue
        text = f"{cluster.get('title', '')} {cluster.get('summary', '')}"
        years = [int(value) for value in re.findall(r"\b20\d{2}\b", text)]
        if not EVENT_TERMS.search(text) or not (FUTURE_TERMS.search(text) or any(year >= today.year for year in years)):
            continue
        source = next((item for item in cluster.get("sources", []) if item.get("url")), None)
        if not source or source["url"] in known_urls:
            continue
        candidates.append({
            "id": cluster.get("id"),
            "title": cluster.get("title"),
            "summary": cluster.get("summary"),
            "publishedAt": published_raw,
            "source": source.get("source_name"),
            "url": source.get("url"),
            "edition": cluster.get("edition"),
            "status": "needs_official_date_verification",
        })
    candidates.sort(key=lambda item: (item["edition"] == "austria", item["publishedAt"]), reverse=True)
    return candidates[:30]


def build_calendar(
    registry: dict[str, Any],
    fetcher=fetch_text,
    *,
    today: date | None = None,
    cached_payload: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    today = today or date.today()
    checked_at = today.isoformat()
    cached_by_source = {
        event.get("sourceId"): event
        for event in (cached_payload or {}).get("events", [])
        if event.get("sourceId")
    }
    events = []
    source_reports = []
    for source in registry.get("sources", []):
        if not source.get("active", True):
            continue
        try:
            markup = fetcher(source["url"])
            valid, missing = validate_markers(markup, source.get("required_markers", []))
            if not valid:
                raise ValueError(f"Official page is missing expected markers: {', '.join(missing)}")
            event = dict(source["event"])
            event.update({
                "url": source["url"],
                "sourceId": source["id"],
                "verificationStatus": "verified",
                "lastVerified": checked_at,
            })
            if is_upcoming(event, today):
                events.append(event)
            source_reports.append({"sourceId": source["id"], "status": "verified", "eventId": event["id"]})
        except Exception as exc:
            cached = cached_by_source.get(source.get("id"))
            if cached and is_upcoming(cached, today):
                fallback = dict(cached)
                fallback["verificationStatus"] = "stale"
                events.append(fallback)
            source_reports.append({"sourceId": source.get("id"), "status": "error", "error": str(exc)})

    payload = {
        "schemaVersion": 2,
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "checkedAt": checked_at,
        "aiRequests": 0,
        "methodology": "Events publish only after their configured date and identity markers are found on an official organizer page. Expired events are removed automatically; feed-discovered leads remain in review.",
        "events": deduplicate(events),
    }
    report = {
        "generatedAt": payload["generatedAt"],
        "activeSourceCount": sum(source.get("active", True) for source in registry.get("sources", [])),
        "verifiedSourceCount": sum(item["status"] == "verified" for item in source_reports),
        "errorSourceCount": sum(item["status"] == "error" for item in source_reports),
        "publishedEventCount": len(payload["events"]),
        "sources": source_reports,
    }
    return payload, report


def write_outputs(payload: dict[str, Any], report: dict[str, Any], candidates: list[dict[str, Any]]) -> None:
    payload["reviewCandidateCount"] = len(candidates)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    JSON_OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    JS_OUTPUT.write_text(f"window.MISE_EVENTS = {rendered};\n", encoding="utf-8")
    REVIEW_OUTPUT.write_text(json.dumps({"generatedAt": payload["generatedAt"], "candidates": candidates}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    registry = load_json(REGISTRY_PATH, {"sources": []})
    cached = load_json(JSON_OUTPUT, {})
    payload, report = build_calendar(registry, cached_payload=cached)
    known_urls = {event.get("url", "") for event in payload["events"]}
    clusters = load_json(CLUSTERS_PATH, {"clusters": []})
    candidates = discover_candidates(clusters, known_urls)
    report["reviewCandidateCount"] = len(candidates)
    write_outputs(payload, report, candidates)
    print(
        f"Wrote {len(payload['events'])} verified/stale events and {len(candidates)} review candidates "
        f"({report['errorSourceCount']} source errors, 0 AI requests)."
    )
    return 0 if payload["events"] else 1


if __name__ == "__main__":
    sys.exit(main())
