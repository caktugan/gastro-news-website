"""Build the public social-source watchlist without retrieving user posts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline_common import write_text_atomic


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "signals.json"
JSON_OUTPUT = ROOT / "data" / "social-watch.json"
JS_OUTPUT = ROOT / "data" / "social-watch.js"

FEATURED_CHANNELS = (
    "reddit-wien",
    "reddit-austria",
    "falstaff-instagram",
    "gaultmillau-austria-instagram",
    "gastro-news-social",
    "vienna-local-food-social",
    "vienna-opening-creators",
    "vienna-official-social",
)


def channel_links(channel: dict[str, Any]) -> list[str]:
    values = [channel.get("url"), *(channel.get("urls") or [])]
    return [value for value in values if isinstance(value, str) and value.startswith("https://")][:6]


def build_payload(source: dict[str, Any]) -> dict[str, Any]:
    by_id = {channel.get("id"): channel for channel in source.get("channels", [])}
    channels = []
    for identifier in FEATURED_CHANNELS:
        channel = by_id.get(identifier)
        if not channel:
            continue
        links = channel_links(channel)
        if not links:
            continue
        channels.append({
            "id": identifier,
            "name": channel.get("name", identifier),
            "platform": channel.get("platform", "social"),
            "region": channel.get("region") or "Austria",
            "signal_type": channel.get("signal_type", "social_signal"),
            "access_status": channel.get("status", "manual_review"),
            "links": links,
        })
    return {
        "schema_version": 1,
        "generated_at": source.get("updated_at"),
        "status": "catalogued_unverified",
        "ai_requests": 0,
        "channel_count": len(channels),
        "publication_rule": source.get("policy", {}).get("publication_rule", ""),
        "automation_rule": source.get("policy", {}).get("automation", ""),
        "channels": channels,
    }


def write_payload(payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    write_text_atomic(JSON_OUTPUT, rendered + "\n")
    write_text_atomic(JS_OUTPUT, f"window.MISE_SOCIAL_WATCH = {rendered};\n")


def main() -> int:
    payload = build_payload(json.loads(INPUT.read_text(encoding="utf-8")))
    write_payload(payload)
    print(f"Wrote {payload['channel_count']} catalogued social-source channels (0 posts retrieved, 0 AI requests).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
