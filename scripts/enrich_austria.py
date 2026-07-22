"""Translate and rank Austrian gastronomy clusters for the English edition.

The worker sends only publisher feed titles, short excerpts, and attribution
metadata to Gemini or the Mistral Chat Completions API. It never sends or retrieves article
bodies. Results are cached by a hash of the supplied evidence so unchanged
stories do not incur repeat model calls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLUSTERS = ROOT / "data" / "clusters.json"
DEFAULT_SOURCES = ROOT / "data" / "sources.json"
DEFAULT_MANUAL = ROOT / "data" / "austria-english.js"
DEFAULT_CACHE = ROOT / "data" / "austria-enrichment.json"
DEFAULT_OUTPUT = ROOT / "data" / "austria-auto.js"
DEFAULT_REPORT = ROOT / "data" / "austria-enrichment-report.json"
DEFAULT_USAGE_LEDGER = ROOT / "data" / ".ai-usage.json"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"
DEFAULT_MISTRAL_MODEL = "mistral-small-2603"
DEFAULT_DAILY_REQUEST_LIMIT = 15
PROMPT_VERSION = 2

VIENNA_TERMS = {
    "wien", "wiener", "vienna", "döbling", "neubau", "alsergrund", "leopoldstadt",
    "landstraße", "liesing", "favoriten", "ottakring", "mariahilf", "donaustadt",
    "währing", "meidling", "hietzing", "penzing", "floridsdorf", "brigittenau",
    "rudolfsheim", "josefstadt", "simmering", "hernals", "prater", "ringstraße",
}
AUSTRIA_TERMS = {
    "österreich", "austria", "steiermark", "styria", "salzburg", "tirol", "tyrol",
    "vorarlberg", "kärnten", "carinthia", "burgenland", "niederösterreich",
    "oberösterreich", "wachau", "graz", "linz", "innsbruck", "klagenfurt",
    "st. pölten", "mühlviertel", "zillertal",
}
FOREIGN_TERMS = {"deutschland", "germany", "frankfurt", "berlin", "münchen", "munich", "hamburg"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def evidence_text(cluster: dict) -> str:
    source_text = " ".join(
        f"{source.get('title', '')} {source.get('summary', '')}" for source in cluster.get("sources", [])
    )
    return f"{cluster.get('title', '')} {cluster.get('summary', '')} {source_text}".casefold()


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def rank_score(cluster: dict, source_priorities: dict[str, int], now: datetime) -> int:
    text = evidence_text(cluster)
    published = parse_datetime(cluster.get("published_at"))
    age_hours = max(0.0, (now - published).total_seconds() / 3600)
    freshness = max(0, 180 - int(age_hours * 2))
    source_score = max(
        (source_priorities.get(source.get("source_id", ""), 50) for source in cluster.get("sources", [])),
        default=50,
    )
    locality = 260 if contains_any(text, VIENNA_TERMS) else 110 if contains_any(text, AUSTRIA_TERMS) else 30
    if contains_any(text, FOREIGN_TERMS) and not contains_any(text, VIENNA_TERMS | AUSTRIA_TERMS):
        locality -= 180
    corroboration = min(80, max(0, cluster.get("independent_source_count", 1) - 1) * 40)
    source_roles = {source.get("corroboration_role") for source in cluster.get("sources", [])}
    role_adjustment = -35 if source_roles and source_roles <= {"press_release", "official_first_party"} else 0
    return freshness + source_score + locality + corroboration + role_adjustment


def source_signature(cluster: dict) -> str:
    evidence = {
        "title": cluster.get("title"),
        "summary": cluster.get("summary"),
        "sources": [
            {
                "id": source.get("source_id"),
                "title": source.get("title"),
                "summary": source.get("summary"),
                "url": source.get("url"),
            }
            for source in cluster.get("sources", [])
        ],
    }
    encoded = json.dumps(evidence, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:20]


def select_clusters(clusters: list[dict], sources: list[dict], limit: int) -> list[dict]:
    priorities = {source["id"]: int(source.get("priority", 50)) for source in sources}
    now = datetime.now(timezone.utc)
    candidates = []
    for cluster in clusters:
        if cluster.get("edition") != "austria":
            continue
        age_days = (now - parse_datetime(cluster.get("published_at"))).total_seconds() / 86400
        if age_days > 30:
            continue
        enriched = dict(cluster)
        enriched["ranking_score"] = rank_score(cluster, priorities, now)
        enriched["source_signature"] = source_signature(cluster)
        candidates.append(enriched)
    candidates.sort(key=lambda item: (item["ranking_score"], item.get("published_at") or ""), reverse=True)
    return candidates[:limit]


def manual_translation_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(re.findall(r'^\s*"([0-9a-f]{16})"\s*:', path.read_text(encoding="utf-8"), re.MULTILINE))


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "updated_at": None, "model": None, "items": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.setdefault("items", {})
    return payload


class DailyBudgetExceeded(RuntimeError):
    """Raised before a request that would exceed the local daily AI budget."""


def daily_request_limit(cli_value: int | None) -> int:
    if cli_value is not None:
        return max(0, cli_value)
    configured = os.environ.get("MISE_DAILY_AI_REQUEST_LIMIT", "").strip()
    if not configured:
        return DEFAULT_DAILY_REQUEST_LIMIT
    try:
        return max(0, int(configured))
    except ValueError as error:
        raise ValueError("MISE_DAILY_AI_REQUEST_LIMIT must be a whole number") from error


def load_usage_ledger(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "days": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.setdefault("schema_version", 1)
    payload.setdefault("days", {})
    return payload


def usage_day() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def usage_totals(ledger: dict, day: str, provider: str) -> dict:
    return ledger.get("days", {}).get(day, {}).get(provider, {"request_count": 0, "item_count": 0})


def reserve_api_request(path: Path, provider: str, item_count: int, limit: int) -> dict:
    """Persist a request reservation before network I/O so failures and retries count."""
    ledger = load_usage_ledger(path)
    day = usage_day()
    days = ledger.setdefault("days", {})
    for old_day in sorted(days)[:-7]:
        days.pop(old_day, None)
    provider_usage = days.setdefault(day, {}).setdefault(
        provider,
        {"request_count": 0, "item_count": 0},
    )
    used = int(provider_usage.get("request_count", 0))
    if used >= limit:
        raise DailyBudgetExceeded(
            f"Local {provider} daily request budget reached ({used}/{limit} UTC); pending stories will use cached/original evidence."
        )
    provider_usage["request_count"] = used + 1
    provider_usage["item_count"] = int(provider_usage.get("item_count", 0)) + max(0, item_count)
    provider_usage["last_request_at"] = utc_now()
    write_json(path, ledger)
    return provider_usage


def request_items(clusters: list[dict]) -> list[dict]:
    items = []
    for cluster in clusters:
        sources = cluster.get("sources", [])
        items.append(
            {
                "id": cluster["id"],
                "original_language": cluster.get("language", "de"),
                "topic": cluster.get("topic", "Restaurants"),
                "published_at": cluster.get("published_at"),
                "source_count": cluster.get("source_count", len(sources)),
                "source_roles": sorted({source.get("corroboration_role", "unknown") for source in sources}),
                "source_names": [source.get("source_name") for source in sources],
                "title": cluster.get("title", "")[:300],
                "feed_excerpt": cluster.get("summary", "")[:1200],
            }
        )
    return items


def response_schema() -> dict:
    item_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string"},
            "publish": {"type": "boolean"},
            "title": {"type": "string", "maxLength": 150},
            "deck": {"type": "string", "maxLength": 360},
            "summary": {"type": "string", "maxLength": 1000},
            "location": {"type": "string", "maxLength": 60},
            "relevance_score": {"type": "integer", "minimum": 0, "maximum": 100},
            "exclusion_reason": {"type": ["string", "null"], "maxLength": 160},
        },
        "required": ["id", "publish", "title", "deck", "summary", "location", "relevance_score", "exclusion_reason"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {"items": {"type": "array", "items": item_schema}},
        "required": ["items"],
    }


def gemini_response_schema() -> dict:
    """Return the schema subset accepted by Gemini structured output."""
    schema = response_schema()

    def remove_unsupported(value: object) -> None:
        if isinstance(value, dict):
            value.pop("maxLength", None)
            for child in value.values():
                remove_unsupported(child)
        elif isinstance(value, list):
            for child in value:
                remove_unsupported(child)

    remove_unsupported(schema)
    return schema


def enrichment_instructions() -> str:
    return (
        "You are the English translation desk for an Austria-first gastronomy news product. "
        "Use only the supplied publisher feed title, short excerpt, date, attribution, and source-role metadata. "
        "Do not add background facts, infer missing details, or make a press release sound independently verified. "
        "Translate faithfully into natural, concise British English. Write a factual but journalistic headline rather than a repetitive subject-verb template. "
        "Vary headline rhythm naturally across the batch: use consequence-led, subject-led, place-led or concise declarative structures when the evidence supports them. "
        "Do not use clickbait, invented colour, unsupported adjectives, rhetorical questions, or novelty for its own sake. "
        "The deck must be one sentence and contain only claims supported by the supplied text. "
        "The summary should be 70 to 130 words in two or three compact paragraphs when the evidence supports that length. "
        "Include the concrete who, what, where and why-it-matters details present in the feed excerpt, without padding. "
        "If the source evidence is thin, write a shorter summary rather than repeating claims or adding context. "
        "Choose a precise Austrian location when explicit; otherwise use Austria. "
        "Set publish=false for recipes, adverts, non-Austrian stories without a material Austrian connection, event listings "
        "without industry relevance, or text too thin to translate safely. Return every supplied id exactly once."
    )


def build_mistral_request(model: str, clusters: list[dict]) -> dict:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": enrichment_instructions()},
            {
                "role": "user",
                "content": json.dumps({"stories": request_items(clusters)}, ensure_ascii=False),
            },
        ],
        "temperature": 0,
        "max_tokens": 5000,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "austria_translation_batch",
                "strict": True,
                "schema": response_schema(),
            },
        },
    }


def build_gemini_request(clusters: list[dict]) -> dict:
    return {
        "systemInstruction": {"parts": [{"text": enrichment_instructions()}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": json.dumps({"stories": request_items(clusters)}, ensure_ascii=False)}
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 5000,
            "responseMimeType": "application/json",
            "responseJsonSchema": gemini_response_schema(),
        },
    }


def extract_mistral_output_text(response: dict) -> str:
    choices = response.get("choices", [])
    if not choices:
        raise ValueError("Mistral API result did not contain a completion choice")
    content = choices[0].get("message", {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [item.get("text", "") for item in content if isinstance(item, dict)]
        if any(parts):
            return "".join(parts)
    raise ValueError("Mistral API completion did not contain text content")


def extract_gemini_output_text(response: dict) -> str:
    candidates = response.get("candidates", [])
    if not candidates:
        feedback = response.get("promptFeedback", {})
        raise ValueError(f"Gemini API result did not contain a candidate: {feedback}")
    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    if any(text_parts):
        return "".join(text_parts)
    raise ValueError("Gemini API candidate did not contain text content")


def call_mistral(
    api_key: str,
    model: str,
    clusters: list[dict],
    timeout: int,
    retries: int,
    before_request=None,
) -> list[dict]:
    body = json.dumps(build_mistral_request(model, clusters), ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        MISTRAL_API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "MISE-Austria-Enrichment/0.2",
        },
    )
    for attempt in range(retries + 1):
        if before_request:
            before_request()
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return json.loads(extract_mistral_output_text(payload))["items"]
        except urllib.error.HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt >= retries:
                detail = error.read(2000).decode("utf-8", errors="replace")
                raise RuntimeError(f"Mistral API HTTP {error.code}: {detail}") from error
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt >= retries:
                raise RuntimeError(f"Mistral API request failed: {error}") from error
        time.sleep(min(8, 2 ** attempt))
    raise RuntimeError("Mistral API retry loop ended unexpectedly")


def call_gemini(
    api_key: str,
    model: str,
    clusters: list[dict],
    timeout: int,
    retries: int,
    before_request=None,
) -> list[dict]:
    body = json.dumps(build_gemini_request(clusters), ensure_ascii=False).encode("utf-8")
    url = f"{GEMINI_API_BASE}/{model}:generateContent"
    for attempt in range(retries + 1):
        if before_request:
            before_request()
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "MISE-Austria-Enrichment/0.3",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return json.loads(extract_gemini_output_text(payload))["items"]
        except urllib.error.HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt >= retries:
                detail = error.read(2000).decode("utf-8", errors="replace")
                raise RuntimeError(f"Gemini API HTTP {error.code}: {detail}") from error
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt >= retries:
                raise RuntimeError(f"Gemini API request failed: {error}") from error
        time.sleep(min(8, 2 ** attempt))
    raise RuntimeError("Gemini API retry loop ended unexpectedly")


def validate_batch(results: list[dict], clusters: list[dict]) -> dict[str, dict]:
    expected = {cluster["id"] for cluster in clusters}
    received: dict[str, dict] = {}
    for item in results:
        identifier = item.get("id")
        if identifier not in expected or identifier in received:
            raise ValueError(f"Unexpected or duplicate enrichment id: {identifier}")
        if item.get("publish") and (
            not item.get("title", "").strip()
            or not item.get("deck", "").strip()
            or not item.get("summary", "").strip()
        ):
            raise ValueError(f"Published enrichment lacks title/deck/summary: {identifier}")
        received[identifier] = item
    if set(received) != expected:
        raise ValueError(f"Enrichment batch omitted ids: {sorted(expected - set(received))}")
    return received


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_browser_data(path: Path, cache: dict, selected: list[dict], excluded_ids: set[str] | None = None) -> int:
    excluded_ids = excluded_ids or set()
    selected_by_id = {cluster["id"]: cluster for cluster in selected}
    translations = {
        identifier: {
            "title": item["title"],
            "deck": item["deck"],
            "summary": item.get("summary", item["deck"]),
            "location": item["location"],
            "relevanceScore": item["relevance_score"],
            "generatedAt": item["generated_at"],
            "model": item["model"],
            "provider": item.get("provider", "mistral"),
        }
        for identifier, item in cache.get("items", {}).items()
        if (
            identifier in selected_by_id
            and identifier not in excluded_ids
            and item.get("publish")
            and item.get("source_signature") == selected_by_id[identifier].get("source_signature")
            and item.get("prompt_version") == PROMPT_VERSION
        )
    }
    payload = {
        "schemaVersion": 1,
        "generatedAt": utc_now(),
        "translations": translations,
    }
    path.write_text(
        "window.MISE_AUSTRIA_AUTO = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    return len(translations)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clusters", type=Path, default=DEFAULT_CLUSTERS)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--manual", type=Path, default=DEFAULT_MANUAL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--usage-ledger", type=Path, default=DEFAULT_USAGE_LEDGER)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument(
        "--max-api-requests",
        type=int,
        help=f"Maximum API attempts per provider per UTC day (default: {DEFAULT_DAILY_REQUEST_LIMIT}; env: MISE_DAILY_AI_REQUEST_LIMIT).",
    )
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--provider", choices=("auto", "gemini", "mistral"), default="auto")
    parser.add_argument("--model", help="Override the selected provider's default model.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Never call the API; rebuild browser output from manual and cached translations only.",
    )
    args = parser.parse_args()
    request_limit = daily_request_limit(args.max_api_requests)

    cluster_payload = json.loads(args.clusters.read_text(encoding="utf-8"))
    source_payload = json.loads(args.sources.read_text(encoding="utf-8"))
    selected = select_clusters(cluster_payload["clusters"], source_payload["sources"], max(1, args.limit))
    selected_ids = {cluster["id"] for cluster in selected}
    manual_ids = manual_translation_ids(args.manual)
    cache = load_cache(args.cache)
    cache_items = cache["items"]

    pending = []
    for cluster in selected:
        cached = cache_items.get(cluster["id"])
        if not args.force and cluster["id"] in manual_ids:
            continue
        if (
            not args.force
            and cached
            and cached.get("source_signature") == cluster["source_signature"]
            and cached.get("prompt_version") == PROMPT_VERSION
        ):
            continue
        pending.append(cluster)

    if args.dry_run:
        preview_provider = args.provider if args.provider != "auto" else "gemini"
        current_usage = usage_totals(load_usage_ledger(args.usage_ledger), usage_day(), preview_provider)
        print(json.dumps({
            "selected": len(selected),
            "manual_reused": len(selected_ids & manual_ids),
            "cached_reused": sum(
                1
                for cluster in selected
                if (cached := cache_items.get(cluster["id"]))
                and cached.get("source_signature") == cluster["source_signature"]
                and cached.get("prompt_version") == PROMPT_VERSION
            ),
            "pending": len(pending),
            "daily_request_budget": {
                "provider": preview_provider,
                "utc_day": usage_day(),
                "limit": request_limit,
                "used": int(current_usage.get("request_count", 0)),
                "remaining": max(0, request_limit - int(current_usage.get("request_count", 0))),
            },
            "top": [{"id": item["id"], "score": item["ranking_score"], "title": item["title"]} for item in selected[:15]],
        }, ensure_ascii=False, indent=2))
        return 0

    gemini_key = "" if args.no_api else os.environ.get("GEMINI_API_KEY", "").strip()
    mistral_key = "" if args.no_api else os.environ.get("MISTRAL_API_KEY", "").strip()
    provider = args.provider
    if provider == "auto":
        provider = "gemini" if gemini_key or not mistral_key else "mistral"
    api_key = gemini_key if provider == "gemini" else mistral_key
    default_model = (
        os.environ.get("MISE_GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        if provider == "gemini"
        else os.environ.get("MISE_MISTRAL_MODEL", DEFAULT_MISTRAL_MODEL)
    )
    model = args.model or default_model
    status = "complete"
    errors: list[str] = []
    processed = 0
    budget_message = None
    if pending and not api_key:
        status = f"skipped_no_{provider}_key"
    elif pending:
        for offset in range(0, len(pending), max(1, args.batch_size)):
            batch = pending[offset : offset + max(1, args.batch_size)]
            try:
                reserve = lambda: reserve_api_request(
                    args.usage_ledger,
                    provider,
                    len(batch),
                    request_limit,
                )
                results = (
                    call_gemini(api_key, model, batch, args.timeout, args.retries, reserve)
                    if provider == "gemini"
                    else call_mistral(api_key, model, batch, args.timeout, args.retries, reserve)
                )
                validated = validate_batch(results, batch)
                generated_at = utc_now()
                for cluster in batch:
                    result = validated[cluster["id"]]
                    cache_items[cluster["id"]] = {
                        **result,
                        "source_signature": cluster["source_signature"],
                        "generated_at": generated_at,
                        "model": model,
                        "provider": provider,
                        "prompt_version": PROMPT_VERSION,
                    }
                processed += len(batch)
                cache.update({"schema_version": 1, "updated_at": generated_at, "model": model, "provider": provider})
                write_json(args.cache, cache)
            except DailyBudgetExceeded as error:
                status = "daily_budget_reached"
                budget_message = str(error)
                break
            except (RuntimeError, ValueError, json.JSONDecodeError) as error:
                status = "partial_failure"
                errors.append(str(error))
                break

    published_auto = write_browser_data(args.output, cache, selected, manual_ids)
    final_usage = usage_totals(load_usage_ledger(args.usage_ledger), usage_day(), provider)
    report = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "status": status,
        "provider": provider,
        "model": model,
        "prompt_version": PROMPT_VERSION,
        "selected_cluster_count": len(selected),
        "manual_translation_count": len(selected_ids & manual_ids),
        "pending_before_run": len(pending),
        "processed_count": processed,
        "remaining_pending_count": max(0, len(pending) - processed),
        "published_auto_count": published_auto,
        "daily_request_budget": {
            "utc_day": usage_day(),
            "limit": request_limit,
            "used": int(final_usage.get("request_count", 0)),
            "remaining": max(0, request_limit - int(final_usage.get("request_count", 0))),
            "attempted_item_count": int(final_usage.get("item_count", 0)),
        },
        "budget_message": budget_message,
        "errors": errors,
    }
    write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if status == "partial_failure" else 0


if __name__ == "__main__":
    raise SystemExit(main())
