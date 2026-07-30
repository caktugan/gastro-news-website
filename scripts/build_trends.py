#!/usr/bin/env python3
"""Detect evidence-backed gastronomy themes without generative AI."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from pipeline_common import parse_iso_datetime, write_text_atomic


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "clusters.json"
JSON_OUTPUT = ROOT / "data" / "trends.json"
JS_OUTPUT = ROOT / "data" / "trends.js"
WINDOW_DAYS = 14


THEMES = [
    {
        "id": "value-led-dining",
        "label": "Value-led dining",
        "description": "Lunch offers, accessible pricing and formats designed for cost-conscious guests.",
        "terms": [
            r"\bvalue menu\b", r"\baffordable\b", r"\bbudget\b", r"\bdiscount", r"\blunch\b",
            r"\bmeal deal\b", r"\bpreis(?:wert|e|en)?\b", r"\bmittag(?:essen|smenü|sangebot)?\b",
            r"\bgünstig", r"\bsparen\b", r"\btraffic\b",
        ],
    },
    {
        "id": "wellness-led-menus",
        "label": "Wellness-led menus",
        "description": "Plant-forward, gut-conscious and lower-alcohol choices moving into mainstream menus.",
        "terms": [
            r"\bplant[- ]based\b", r"\bvegan", r"\bvegetarian", r"\bgut[- ]friendly\b", r"\bwellness\b",
            r"\bferment", r"\bzero[- ]proof\b", r"\bnon[- ]alcoholic\b", r"\balcohol[- ]free\b",
            r"\bgesund", r"\balkoholfrei", r"\bdarmfreund",
        ],
    },
    {
        "id": "workforce-and-training",
        "label": "Workforce & training",
        "description": "Recruitment, retention, pay and skills development across hospitality teams.",
        "terms": [
            r"\bstaff(?:ing)?\b", r"\bworkforce\b", r"\blabou?r\b", r"\brecruit", r"\bwage", r"\btalent\b",
            r"\bapprentice", r"\btraining\b", r"\bscholarship\b", r"\bpersonal(?:mangel)?\b",
            r"\bfachkräft", r"\blehrling", r"\bausbildung\b", r"\bkollektivvertrag\b",
        ],
    },
    {
        "id": "restaurant-technology",
        "label": "Restaurant technology",
        "description": "Payments, ordering, loyalty and automation changing restaurant operations.",
        "terms": [
            r"\bpayment", r"\bpoint of sale\b", r"\bPOS\b", r"\bdigital order", r"\bonline order",
            r"\bloyalty\b", r"\bautomation\b", r"\brobot", r"\bartificial intelligence\b", r"\bAI[- ]powered\b",
            r"\brestaurant tech", r"\bsoftware\b", r"\btechnolog", r"\bdigitalisier",
        ],
    },
    {
        "id": "experience-led-hospitality",
        "label": "Experience-led hospitality",
        "description": "Pop-ups, collaborations and programmed events turning visits into occasions.",
        "terms": [
            r"\bpop[- ]up\b", r"\bguest chef\b", r"\bcollaboration\b", r"\bimmersive\b", r"\btasting\b",
            r"\bfestival\b", r"\blive music\b", r"\bevent series\b", r"\bexperience\b", r"\bcollab",
            r"\bgastkoch", r"\bverkostung\b", r"\bkulinarik[- ]event\b",
        ],
    },
    {
        "id": "expansion-and-formats",
        "label": "Expansion & new formats",
        "description": "New locations, franchising and hybrid concepts reshaping the competitive map.",
        "terms": [
            r"\bnew location\b", r"\bfirst location\b", r"\bexpan(?:d|sion)", r"\bfranchis", r"\brolls? out\b",
            r"\bopening\b", r"\bopens\b", r"\bopened\b", r"\bnew venue\b", r"\bnew restaurant\b",
            r"\beröffn", r"\bneues lokal\b", r"\bneuer standort\b", r"\bexpandier",
        ],
        "exclude": [
            r"\bclos(?:ed|es|ure)\b", r"\binsolven", r"\bschließ", r"\bgeschlossen\b",
            r"\bcancel", r"\babgesagt\b", r"\bgeplatzt\b",
        ],
    },
    {
        "id": "sourcing-and-sustainability",
        "label": "Sourcing & sustainability",
        "description": "Local supply, waste reduction and environmental claims affecting purchasing decisions.",
        "terms": [
            r"\bsustainab", r"\blocal sourcing\b", r"\bregenerative\b", r"\bfood waste\b", r"\bzero waste\b",
            r"\bseasonal\b", r"\borganic\b", r"\btraceab", r"\bnachhalt", r"\bregional", r"\bsaisonal",
            r"\blebensmittelverschwendung\b",
        ],
    },
    {
        "id": "beverage-shifts",
        "label": "Beverage shifts",
        "description": "Coffee, wine and alcohol alternatives creating new menu and margin opportunities.",
        "terms": [
            r"\bspecialty coffee\b", r"\bcoffee\b", r"\bcafé\b", r"\bcafe\b", r"\bmatcha\b", r"\bhojicha\b",
            r"\bnatural wine\b", r"\bwine bar\b", r"\bnon[- ]alcoholic\b", r"\bzero[- ]proof\b",
            r"\bkaffee\b", r"\bweinbar\b", r"\bnaturwein\b", r"\balkoholfrei",
        ],
    },
]


def parse_timestamp(value: str | None) -> datetime | None:
    # Tolerant: build_signals filters unparseable timestamps out up front, so a
    # single malformed date degrades one cluster instead of crashing the stage.
    return parse_iso_datetime(value)


def compile_theme(theme: dict[str, Any]) -> re.Pattern[str]:
    return re.compile("|".join(f"(?:{term})" for term in theme["terms"]), re.IGNORECASE)


def theme_matches(theme: dict[str, Any], text: str) -> bool:
    if not compile_theme(theme).search(text):
        return False
    exclusions = theme.get("exclude", [])
    return not exclusions or not re.search("|".join(f"(?:{term})" for term in exclusions), text, re.IGNORECASE)


def cluster_text(cluster: dict[str, Any]) -> str:
    return f"{cluster.get('title', '')} {cluster.get('summary', '')}"


def coverage_label(current_share: float, previous_share: float, previous_total: int) -> str:
    """Describe change in editorial coverage share, never market growth."""
    if previous_total < 20:
        return "Current signal"
    delta_points = (current_share - previous_share) * 100
    if delta_points >= 3:
        return "Rising coverage"
    if delta_points <= -3:
        return "Cooling coverage"
    return "Steady coverage"


def evidence_item(cluster: dict[str, Any]) -> dict[str, Any] | None:
    source = next((item for item in cluster.get("sources", []) if item.get("url")), None)
    if not source:
        return None
    return {
        "cluster_id": cluster.get("id"),
        "title": cluster.get("title"),
        "summary": cluster.get("summary"),
        "url": source.get("url"),
        "source": source.get("source_name"),
        "published_at": cluster.get("published_at"),
        "edition": cluster.get("edition"),
        "source_count": cluster.get("source_count", 1),
    }


def build_signals(payload: dict[str, Any]) -> list[dict[str, Any]]:
    generated = parse_timestamp(payload.get("generated_at")) or datetime.now(timezone.utc)
    current_start = generated - timedelta(days=WINDOW_DAYS)
    previous_start = current_start - timedelta(days=WINDOW_DAYS)
    clusters = []
    for cluster in payload.get("clusters", []):
        published = parse_timestamp(cluster.get("published_at"))
        if published is not None and published >= previous_start:
            clusters.append(cluster)
    current_total = sum(parse_timestamp(cluster["published_at"]) >= current_start for cluster in clusters)
    previous_total = len(clusters) - current_total
    signals = []
    for theme in THEMES:
        matched = [cluster for cluster in clusters if theme_matches(theme, cluster_text(cluster))]
        current = [cluster for cluster in matched if parse_timestamp(cluster["published_at"]) >= current_start]
        previous = [cluster for cluster in matched if parse_timestamp(cluster["published_at"]) < current_start]
        source_names = {
            source.get("source_name")
            for cluster in current
            for source in cluster.get("sources", [])
            if source.get("source_name")
        }
        if len(current) < 3 or len(source_names) < 2:
            continue
        austria_count = sum(cluster.get("edition") == "austria" for cluster in current)
        current_share = len(current) / current_total if current_total else 0
        previous_share = len(previous) / previous_total if previous_total else 0
        coverage_delta = round((current_share - previous_share) * 100, 1)
        evidence = [item for item in (evidence_item(cluster) for cluster in current) if item]
        evidence.sort(
            key=lambda item: (
                item["edition"] == "austria",
                item.get("source_count", 1),
                item.get("published_at", ""),
            ),
            reverse=True,
        )
        score = len(current) * 2 + len(source_names) * 1.5 + austria_count * 2 + max(0, len(current) - len(previous))
        signals.append({
            "id": theme["id"],
            "label": theme["label"],
            "description": theme["description"],
            "status": coverage_label(current_share, previous_share, previous_total),
            "current_count": len(current),
            "previous_count": len(previous),
            "current_share_pct": round(current_share * 100, 1),
            "previous_share_pct": round(previous_share * 100, 1),
            "coverage_delta_pp": coverage_delta,
            "current_window_total": current_total,
            "previous_window_total": previous_total,
            "source_count": len(source_names),
            "austria_count": austria_count,
            "global_count": len(current) - austria_count,
            "window_days": WINDOW_DAYS,
            "score": round(score, 1),
            "evidence": evidence[:5],
        })
    signals.sort(key=lambda signal: (signal["score"], signal["source_count"]), reverse=True)
    return signals[:5]


def build_payload(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": source["generated_at"],
        "ai_requests": 0,
        "window_days": WINDOW_DAYS,
        "methodology": "Curated multilingual keyword themes ranked by recent cluster count, distinct publishers and Austria relevance. Coverage direction compares each theme's share of all available stories, reducing RSS retention bias. It describes publisher attention, not market growth. Every signal links to its evidence.",
        "signals": build_signals(source),
    }


def write_payload(payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    write_text_atomic(JSON_OUTPUT, rendered + "\n")
    write_text_atomic(JS_OUTPUT, f"window.MISE_TRENDS = {rendered};\n")


def main() -> int:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    payload = build_payload(source)
    write_payload(payload)
    print(f"Wrote {len(payload['signals'])} source-driven trend signals (0 AI requests).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
