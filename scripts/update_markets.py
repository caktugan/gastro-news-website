#!/usr/bin/env python3
"""Build the keyless MISE operator-cost benchmark payload.

The worker retrieves official structured data only. It does not use AI, scrape
article pages, or require API credentials. Existing cached benchmarks survive
individual source failures so the reader can see an honest stale state instead
of an empty or invented value.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


from pipeline_common import USER_AGENT, write_text_atomic


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "data" / "markets.json"
JS_OUTPUT = ROOT / "data" / "markets.js"

EU_API = "https://api.tech.ec.europa.eu/agrifood/api"
ECB_API = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"


def fetch_text(url: str, timeout: int = 30) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/csv,*/*"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8-sig")


def fetch_json(url: str) -> list[dict[str, Any]]:
    payload = json.loads(fetch_text(url))
    if not isinstance(payload, list):
        raise ValueError(f"Expected a list from {url}")
    return payload


def api_url(path: str, **params: Any) -> str:
    return f"{EU_API}/{path}?{urlencode(params, doseq=True)}"


def parse_eu_price(value: Any) -> float:
    """Parse EU price strings containing either decimal commas or dots."""
    text = re.sub(r"[^0-9,.-]", "", str(value or ""))
    if not text:
        raise ValueError(f"No numeric price in {value!r}")
    if "," in text and "." in text:
        # Whichever separator appears last is the decimal marker.
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        tail = text.rsplit(",", 1)[1]
        text = text.replace(",", ".") if len(tail) <= 2 else text.replace(",", "")
    return float(text)


def eu_date(value: str) -> date:
    return datetime.strptime(value, "%d/%m/%Y").date()


def iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def percentage_change(current: float, previous: float) -> float | None:
    if previous == 0:
        return None
    return round((current - previous) / previous * 100, 1)


def select_series(
    records: Iterable[dict[str, Any]],
    predicate: Callable[[dict[str, Any]], bool],
    *,
    date_field: str,
    date_parser: Callable[[str], date],
    value_field: str = "price",
    divisor: float = 1,
) -> list[dict[str, Any]]:
    """Return a chronological, date-deduplicated numeric series."""
    observations: dict[str, dict[str, Any]] = {}
    for record in records:
        if not predicate(record):
            continue
        try:
            observed = date_parser(str(record[date_field]))
            value = parse_eu_price(record[value_field]) / divisor
        except (KeyError, TypeError, ValueError):
            continue
        observations[observed.isoformat()] = {"date": observed.isoformat(), "value": round(value, 4)}
    return [observations[key] for key in sorted(observations)]


def benchmark(
    *,
    identifier: str,
    label: str,
    scope: str,
    unit: str,
    frequency: str,
    change_basis: str,
    source: str,
    source_url: str,
    description: str,
    history: list[dict[str, Any]],
    decimals: int,
    stale_after_days: int,
) -> dict[str, Any]:
    if len(history) < 2:
        raise ValueError(f"{label} needs at least two observations")
    latest, previous = history[-1], history[-2]
    age_days = (date.today() - iso_date(latest["date"])).days
    return {
        "id": identifier,
        "label": label,
        "scope": scope,
        "value": round(float(latest["value"]), decimals),
        "display_decimals": decimals,
        "unit": unit,
        "period": latest["date"],
        "frequency": frequency,
        "change_pct": percentage_change(float(latest["value"]), float(previous["value"])),
        "change_basis": change_basis,
        "source": source,
        "source_url": source_url,
        "description": description,
        "stale": age_days > stale_after_days,
        "history": history[-12:],
    }


def build_wheat(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "AT"
        and row.get("productName") == "Breadmaking common wheat"
        and row.get("marketName") == "National Average",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="at-bread-wheat",
        label="Bread wheat",
        scope="Austria",
        unit="€/t",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url("cereal/prices", memberStateCodes="AT", productCodes="BLTPAN"),
        description="Austria national-average breadmaking common wheat reference price.",
        history=history,
        decimals=0,
        stale_after_days=21,
    )


def build_milk(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "AT" and row.get("product") == "Raw milk",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="at-raw-milk",
        label="Raw milk",
        scope="Austria",
        unit="€/100 kg",
        frequency="Monthly",
        change_basis="vs previous month",
        source="European Commission",
        source_url=api_url("rawMilk/prices", memberStateCodes="AT", products="Raw milk"),
        description="Austria monthly raw-milk price reported by the Member State.",
        history=history,
        decimals=2,
        stale_after_days=75,
    )


def build_eggs(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "AT" and row.get("farmingMethod") == "Barn",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="at-barn-eggs",
        label="Eggs",
        scope="Austria barn eggs",
        unit="€/100 kg",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url("poultry/egg/prices", memberStateCodes="AT", farmingMethods="Barn"),
        description="Austria wholesale reference for Class A barn eggs; a directional purchasing-cost benchmark.",
        history=history,
        decimals=2,
        stale_after_days=21,
    )


def build_poultry(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "AT"
        and row.get("productName") == "Whole broiler (65%)"
        and row.get("priceType") == "Selling price",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="at-whole-broiler",
        label="Chicken",
        scope="Austria whole broiler",
        unit="€/100 kg",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url("poultry/prices", memberStateCodes="AT", products="Whole broiler (65%)"),
        description="Austria selling-price reference for whole broiler chicken, reported per 100 kg.",
        history=history,
        decimals=2,
        stale_after_days=21,
    )


def build_pigmeat(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "AT" and row.get("pigClass") == "E",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="at-pigmeat-e",
        label="Pigmeat",
        scope="Austria class E",
        unit="€/100 kg",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url("pigmeat/prices", memberStateCodes="AT"),
        description="Austria weekly class E pig-carcass price; a directional meat-cost benchmark.",
        history=history,
        decimals=2,
        stale_after_days=21,
    )


def build_butter(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "EU" and row.get("product") == "BUTTER",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="eu-butter",
        label="Butter",
        scope="European Union",
        unit="€/100 kg",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url("dairy/prices", memberStateCodes="EU", products="BUTTER"),
        description="European Union weekly butter reference price; Austria does not publish this series consistently.",
        history=history,
        decimals=2,
        stale_after_days=21,
    )


def build_sunflower(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "IT"
        and row.get("product") == "Crude sunflower oil"
        and row.get("market") == "Milano",
        date_field="endDate",
        date_parser=eu_date,
    )
    return benchmark(
        identifier="eu-sunflower-oil",
        label="Sunflower oil",
        scope="Milan benchmark",
        unit="€/t",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url("oilseeds/prices", products="Crude sunflower oil", markets="Milano"),
        description="Crude sunflower-oil wholesale reference from Milan; a directional EU input-cost proxy, not an Austrian supplier quote.",
        history=history,
        decimals=0,
        stale_after_days=21,
    )


def build_olive(records: list[dict[str, Any]]) -> dict[str, Any]:
    history = select_series(
        records,
        lambda row: row.get("memberStateCode") == "IT"
        and row.get("product") == "Extra virgin olive oil (up to 0.8%)"
        and row.get("market") == "Average national price",
        date_field="endDate",
        date_parser=eu_date,
        divisor=100,
    )
    return benchmark(
        identifier="it-extra-virgin-olive-oil",
        label="Extra virgin olive oil",
        scope="Italy bulk benchmark",
        unit="€/kg",
        frequency="Weekly",
        change_basis="vs previous week",
        source="European Commission",
        source_url=api_url(
            "oliveOil/prices",
            memberStateCodes="IT",
            products="Extra virgin olive oil (up to 0.8%)",
        ),
        description="Italian national-average bulk extra-virgin olive-oil reference, converted from €/100 kg to €/kg.",
        history=history,
        decimals=2,
        stale_after_days=21,
    )


def build_fx(csv_text: str) -> dict[str, Any]:
    history = []
    for row in csv.DictReader(io.StringIO(csv_text)):
        try:
            history.append({"date": iso_date(row["TIME_PERIOD"]).isoformat(), "value": float(row["OBS_VALUE"])})
        except (KeyError, TypeError, ValueError):
            continue
    history.sort(key=lambda item: item["date"])
    return benchmark(
        identifier="eur-usd",
        label="EUR / USD",
        scope="ECB reference rate",
        unit="USD per EUR",
        frequency="Daily",
        change_basis="vs previous trading day",
        source="European Central Bank",
        source_url="https://data.ecb.europa.eu/data/datasets/EXR/EXR.D.USD.EUR.SP00.A",
        description="ECB euro reference rate; useful context for globally priced imported inputs.",
        history=history,
        decimals=4,
        stale_after_days=7,
    )


def load_cached() -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {item["id"]: item for item in payload.get("benchmarks", []) if item.get("id")}


def write_payload(payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    write_text_atomic(JSON_OUTPUT, rendered + "\n")
    write_text_atomic(JS_OUTPUT, f"window.MISE_MARKETS = {rendered};\n")


def main() -> int:
    today = date.today()
    begin = f"01/01/{today.year - 1}"
    jobs: list[tuple[str, Callable[[], dict[str, Any]]]] = [
        (
            "at-bread-wheat",
            lambda: build_wheat(fetch_json(api_url("cereal/prices", memberStateCodes="AT", productCodes="BLTPAN", beginDate=begin))),
        ),
        (
            "at-raw-milk",
            lambda: build_milk(fetch_json(api_url("rawMilk/prices", memberStateCodes="AT", products="Raw milk", years=[today.year - 1, today.year]))),
        ),
        (
            "at-barn-eggs",
            lambda: build_eggs(fetch_json(api_url("poultry/egg/prices", memberStateCodes="AT", beginDate=begin))),
        ),
        (
            "at-whole-broiler",
            lambda: build_poultry(fetch_json(api_url("poultry/prices", memberStateCodes="AT", beginDate=begin))),
        ),
        (
            "at-pigmeat-e",
            lambda: build_pigmeat(fetch_json(api_url("pigmeat/prices", memberStateCodes="AT", beginDate=begin))),
        ),
        (
            "eu-butter",
            lambda: build_butter(fetch_json(api_url("dairy/prices", memberStateCodes="EU", products="BUTTER", years=[today.year - 1, today.year]))),
        ),
        (
            "eu-sunflower-oil",
            lambda: build_sunflower(fetch_json(api_url("oilseeds/prices", products="Crude sunflower oil", beginDate=begin))),
        ),
        (
            "it-extra-virgin-olive-oil",
            lambda: build_olive(fetch_json(api_url("oliveOil/prices", beginDate=begin))),
        ),
        (
            "eur-usd",
            lambda: build_fx(fetch_text(f"{ECB_API}?lastNObservations=14&format=csvdata")),
        ),
    ]

    cached = load_cached()
    benchmarks: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for identifier, job in jobs:
        try:
            benchmarks.append(job())
        except Exception as exc:  # One unavailable source must not erase the rest.
            if identifier in cached:
                fallback = dict(cached[identifier])
                fallback["stale"] = True
                fallback["cache_fallback"] = True
                benchmarks.append(fallback)
            errors.append({"benchmark": identifier, "message": str(exc)})

    order = [identifier for identifier, _ in jobs]
    benchmarks.sort(key=lambda item: order.index(item["id"]))
    payload = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "current" if not errors else "partial",
        "ai_requests": 0,
        "methodology": "Official reference series only. Values are directional wholesale or macro benchmarks, not supplier quotes.",
        "benchmarks": benchmarks,
        "errors": errors,
    }
    write_payload(payload)
    print(f"Wrote {len(benchmarks)} market benchmarks ({len(errors)} source errors).")
    return 0 if benchmarks else 1


if __name__ == "__main__":
    sys.exit(main())
