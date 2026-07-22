"""Run the complete MISE data refresh and publish a browser-readable health report."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATUS_JSON = ROOT / "data" / "update-status.json"
STATUS_JS = ROOT / "data" / "update-status.js"

STAGE_META = {
    "news": ("News feeds", ROOT / "data" / "ingestion-report.json"),
    "markets": ("Cost benchmarks", ROOT / "data" / "markets.json"),
    "trends": ("Trend radar", ROOT / "data" / "trends.json"),
    "social": ("Social source directory", ROOT / "data" / "social-watch.json"),
    "events": ("Events calendar", ROOT / "data" / "event-update-report.json"),
    "enrichment": ("English edition", ROOT / "data" / "austria-enrichment-report.json"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def run_stage(identifier: str, command: list[str]) -> dict[str, Any]:
    """Run one stage without preventing independent stages from refreshing."""
    print(f"\n> {' '.join(command)}", flush=True)
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)
    output_lines = [line.strip() for line in (completed.stdout or "").splitlines() if line.strip()]
    error_lines = [line.strip() for line in (completed.stderr or "").splitlines() if line.strip()]
    return {
        "id": identifier,
        "exit_code": completed.returncode,
        "duration_ms": round((time.perf_counter() - started) * 1000),
        "completed_at": utc_now(),
        "message": (error_lines or output_lines or [""])[-1][:300],
    }


def skipped_stage(identifier: str) -> dict[str, Any]:
    return {
        "id": identifier,
        "exit_code": None,
        "duration_ms": 0,
        "completed_at": None,
        "message": "Skipped by operator",
    }


def stage_health(outcome: dict[str, Any]) -> dict[str, Any]:
    """Combine process state with the source-specific audit report."""
    identifier = outcome["id"]
    label, report_path = STAGE_META[identifier]
    stage = {
        "id": identifier,
        "label": label,
        "status": "skipped" if outcome["exit_code"] is None else "failed" if outcome["exit_code"] else "current",
        "completed_at": outcome["completed_at"],
        "duration_ms": outcome["duration_ms"],
        "summary": outcome["message"] or "Refresh completed",
        "issues": 0,
    }
    if outcome["exit_code"] is None or outcome["exit_code"]:
        return stage

    report = load_json(report_path)
    if identifier == "news":
        active = int(report.get("active_source_count", 0))
        successful = int(report.get("successful_source_count", 0))
        failed = int(report.get("failed_source_count", 0))
        articles = int(report.get("items_after_deduplication", 0))
        stage["summary"] = f"{successful} of {active} feeds responded · {articles} items"
        stage["issues"] = failed
        if failed:
            stage["status"] = "partial"
    elif identifier == "markets":
        benchmarks = report.get("benchmarks", [])
        errors = report.get("errors", [])
        stage["summary"] = f"{len(benchmarks)} official benchmarks · 0 AI requests"
        stage["issues"] = len(errors)
        if report.get("status") != "current" or errors:
            stage["status"] = "partial"
    elif identifier == "trends":
        signals = report.get("signals", [])
        stage["summary"] = f"{len(signals)} evidence-backed signals · 0 AI requests"
    elif identifier == "social":
        channels = int(report.get("channel_count", 0))
        stage["summary"] = f"{channels} catalogued channels · access unverified · 0 posts retrieved"
    elif identifier == "events":
        verified = int(report.get("verifiedSourceCount", 0))
        active = int(report.get("activeSourceCount", 0))
        errors = int(report.get("errorSourceCount", 0))
        stage["summary"] = f"{verified} of {active} official pages verified"
        stage["issues"] = errors
        if errors:
            stage["status"] = "partial"
    elif identifier == "enrichment":
        published = int(report.get("published_auto_count", 0)) + int(report.get("manual_translation_count", 0))
        pending = int(report.get("remaining_pending_count", 0))
        provider = report.get("provider") or "cached"
        stage["summary"] = f"{published} English briefs · {provider} · {pending} pending"
        stage["issues"] = pending + len(report.get("errors", []))
        if report.get("status") not in {"complete", "current"} or stage["issues"]:
            stage["status"] = "partial"
    return stage


def build_status(outcomes: list[dict[str, Any]], generated_at: str | None = None) -> dict[str, Any]:
    stages = [stage_health(outcome) for outcome in outcomes]
    active = [stage for stage in stages if stage["status"] != "skipped"]
    issue_count = sum(int(stage["issues"]) for stage in active)
    failed_count = sum(stage["status"] == "failed" for stage in active)
    if failed_count:
        overall = "failed" if failed_count == len(active) else "partial"
    elif any(stage["status"] == "partial" for stage in active):
        overall = "partial"
    else:
        overall = "current"
    return {
        "schema_version": 1,
        "generated_at": generated_at or utc_now(),
        "overall_status": overall,
        "issue_count": issue_count + failed_count,
        "stages": stages,
    }


def write_status(payload: dict[str, Any]) -> None:
    STATUS_JSON.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    STATUS_JSON.write_text(rendered + "\n", encoding="utf-8")
    STATUS_JS.write_text(f"window.MISE_UPDATE_STATUS = {rendered};\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-fetch", action="store_true", help="Reuse current articles and rebuild clusters.")
    parser.add_argument("--skip-markets", action="store_true", help="Do not refresh official market benchmarks.")
    parser.add_argument("--skip-events", action="store_true", help="Do not refresh official event pages or the calendar cache.")
    parser.add_argument("--no-api", action="store_true", help="Do not call Gemini or Mistral; use manual and cached translations.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum recent Austria clusters to consider.")
    parser.add_argument(
        "--max-api-requests",
        type=int,
        help="Maximum Gemini/Mistral request attempts per UTC day (default 15).",
    )
    parser.add_argument("--provider", choices=("auto", "gemini", "mistral"), default="auto")
    parser.add_argument("--model", help="Override the selected provider's default model for this run.")
    parser.add_argument(
        "--refresh-enrichment",
        action="store_true",
        help="Regenerate selected English summaries even when a manual or cached result exists.",
    )
    args = parser.parse_args()

    python = sys.executable
    outcomes = []
    news_command = [python, str(ROOT / "scripts" / ("cluster.py" if args.skip_fetch else "ingest.py"))]
    outcomes.append(run_stage("news", news_command))

    if args.skip_markets:
        outcomes.append(skipped_stage("markets"))
    else:
        outcomes.append(run_stage("markets", [python, str(ROOT / "scripts" / "update_markets.py")]))

    outcomes.append(run_stage("trends", [python, str(ROOT / "scripts" / "build_trends.py")]))
    outcomes.append(run_stage("social", [python, str(ROOT / "scripts" / "build_social_watch.py")]))
    if args.skip_events:
        outcomes.append(skipped_stage("events"))
    else:
        outcomes.append(run_stage("events", [python, str(ROOT / "scripts" / "update_events.py")]))

    enrichment = [
        python,
        str(ROOT / "scripts" / "enrich_austria.py"),
        "--limit",
        str(max(1, args.limit)),
        "--provider",
        args.provider,
    ]
    if args.no_api:
        enrichment.append("--no-api")
    if args.max_api_requests is not None:
        enrichment.extend(["--max-api-requests", str(max(0, args.max_api_requests))])
    if args.model:
        enrichment.extend(["--model", args.model])
    if args.refresh_enrichment:
        enrichment.append("--force")
    outcomes.append(run_stage("enrichment", enrichment))

    status = build_status(outcomes)
    write_status(status)
    print(f"\nMISE refresh {status['overall_status']}: {status['issue_count']} issue(s).")
    return 1 if any(outcome["exit_code"] not in {None, 0} for outcome in outcomes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
