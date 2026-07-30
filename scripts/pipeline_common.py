"""Helpers shared across the MISE pipeline scripts.

Each of these existed as several diverging copies (five ISO parsers, four
user agents, six JSON+JS-twin writers) before being pulled here.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# One identity for every outbound request the pipeline makes.
USER_AGENT = "MISE/1.0 (+https://caktugan.github.io/gastro-news-website/; metadata-only reader)"


def parse_iso_datetime(value: str | None) -> datetime | None:
    """Parse an ISO-8601 timestamp ("Z" accepted); None when unparseable.

    Naive timestamps are assumed UTC. Returning None instead of raising is
    deliberate: a single malformed date must degrade one record, not a stage.
    """
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def write_text_atomic(path: Path, text: str) -> None:
    """Write via a sibling temp file and replace.

    Several stages read these files back as their stale-data fallback; an
    in-place write interrupted mid-run left truncated JSON that the fallback
    loaders silently treated as an empty cache.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def write_json_atomic(path: Path, payload: Any) -> None:
    write_text_atomic(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def write_browser_payload(path: Path, global_name: str, payload: Any) -> None:
    """The site is fetch-free static: browser data ships as a global-assigning
    script twin of the pipeline's JSON state."""
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    write_text_atomic(path, f"window.{global_name} = {rendered};\n")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
