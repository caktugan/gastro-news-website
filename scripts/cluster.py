"""Group related feed items into evidence-preserving story clusters for MISE.

The clustering is deliberately conservative. It only joins articles in the same
edition and language when their titles share enough distinctive terms within a
four-day window. Briefs are extractive: every bullet comes from a feed excerpt
and records the source that supports it. No LLM is called in this stage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTICLES = ROOT / "data" / "articles.json"
DEFAULT_REGISTRY = ROOT / "data" / "sources.json"
DEFAULT_CLUSTERS = ROOT / "data" / "clusters.json"
DEFAULT_JS = ROOT / "data" / "live-news.js"

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "in", "is", "it", "its",
    "new", "of", "on", "or", "that", "the", "their", "this", "to", "with", "after", "into", "over",
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einer", "eines", "im", "in", "ist",
    "mit", "nach", "und", "von", "vor", "zu", "zur", "zum", "für", "auf", "aus", "bei", "wird",
    "food", "restaurant", "restaurants", "world", "cup", "global", "latest", "news", "2026",
}

# Company and venue names also appear in the feed excerpt when a publisher keeps
# them out of the headline, so capitalized phrases are read from the summary as
# well as the title. German capitalizes every noun, so an unfiltered sweep would
# offer up phrases like "Wiener Traditionshaus" as if they were brands; a summary
# phrase therefore only counts when it carries a token rare across the corpus,
# which is what separates "ARION Jewelry" from "Der goldfarbene Anhänger".
RARE_TOKEN_DOCUMENT_LIMIT = 4
RARE_TOKEN_MIN_LENGTH = 5
ANNOUNCEMENT_WINDOW_HOURS = 3

CAPITALIZED_PHRASE = re.compile(
    r"\b[A-Z\u00c0-\u00d6\u00d8-\u00de][\w\u00c0-\u00ff'’-]+(?:\s+[A-Z\u00c0-\u00d6\u00d8-\u00de][\w\u00c0-\u00ff'’-]+)+"
)
QUOTED_PHRASE = re.compile(r"[\"“„](.{3,80}?)[\"”]")


def normalized_words(value: str) -> list[str]:
    folded = unicodedata.normalize("NFKD", value.casefold())
    ascii_text = "".join(char for char in folded if not unicodedata.combining(char))
    words = re.findall(r"[a-z0-9]+", ascii_text)
    return [word for word in words if len(word) > 2 and word not in STOPWORDS]


def normalized_phrase(value: str) -> str:
    return " ".join(normalized_words(value))


def _usable_phrases(article: dict, candidates: set[str]) -> set[str]:
    source_name = normalized_phrase(article.get("source_name", ""))
    return {
        phrase
        for phrase in (normalized_phrase(candidate) for candidate in candidates)
        if 2 <= len(phrase.split()) <= 6 and len(phrase) >= 7
        and phrase != source_name
        and phrase not in {"the post", "der beitrag", "read more", "mehr lesen"}
    }


def named_phrases(article: dict) -> set[str]:
    """Return conservative venue/company-name candidates from feed evidence."""
    title = article.get("title", "")
    summary = article.get("summary", "")
    candidates = set(QUOTED_PHRASE.findall(f"{title} {summary}"))
    candidates.update(CAPITALIZED_PHRASE.findall(title))
    if ":" in title:
        candidates.add(title.split(":", 1)[1])
    return _usable_phrases(article, candidates)


def summary_named_phrases(article: dict, rare_tokens: set[str]) -> set[str]:
    """Capitalized phrases from the excerpt, kept only when they carry a rare token."""
    candidates = set(CAPITALIZED_PHRASE.findall(article.get("summary", "")))
    return {
        phrase
        for phrase in _usable_phrases(article, candidates)
        if set(phrase.split()) & rare_tokens
    }


def article_timestamp(article: dict) -> datetime | None:
    value = article.get("published_at")
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def within_time_window(left: dict, right: dict, days: int = 4) -> bool:
    left_time = article_timestamp(left)
    right_time = article_timestamp(right)
    if not left_time or not right_time:
        return True
    return abs((left_time - right_time).total_seconds()) <= days * 86400


def filed_within_hours(left: dict, right: dict, hours: int = ANNOUNCEMENT_WINDOW_HOURS) -> bool:
    """Unlike within_time_window, a missing timestamp is not treated as proximity."""
    left_time = article_timestamp(left)
    right_time = article_timestamp(right)
    if not left_time or not right_time:
        return False
    return abs((left_time - right_time).total_seconds()) <= hours * 3600


def shared_entities(left_phrases: set[str], right_phrases: set[str]) -> set[str]:
    """Match names by containment, not equality.

    German binds a brand to the noun in front of it, so one excerpt yields
    "Schmuckmarke ARION Jewelry" where another yields "ARION Jewelry". Those are
    the same company, and exact set intersection never sees it. The shorter
    phrase must still be a whole-word run inside the longer one.
    """
    matches = set()
    for left in left_phrases:
        for right in right_phrases:
            short, long = sorted((left, right), key=lambda phrase: len(phrase.split()))
            if short == long or f" {long} ".find(f" {short} ") >= 0:
                matches.add(short)
    return matches


def rare_title_tokens(articles: list[dict], limit: int = RARE_TOKEN_DOCUMENT_LIMIT) -> set[str]:
    """Title tokens carried by at most `limit` articles in the current corpus."""
    counts: dict[str, int] = {}
    for article in articles:
        for word in set(normalized_words(article.get("title", ""))):
            counts[word] = counts.get(word, 0) + 1
    return {
        word
        for word, count in counts.items()
        if count <= limit and len(word) >= RARE_TOKEN_MIN_LENGTH
    }


def cluster_score(left: dict, right: dict, rare_tokens: set[str] | None = None) -> float:
    if left.get("edition") != right.get("edition") or left.get("language") != right.get("language"):
        return 0.0
    if not within_time_window(left, right):
        return 0.0

    left_words = set(normalized_words(left.get("title", "")))
    right_words = set(normalized_words(right.get("title", "")))
    if not left_words or not right_words:
        return 0.0

    shared = left_words & right_words
    union = left_words | right_words
    jaccard = len(shared) / len(union)
    sequence = SequenceMatcher(None, " ".join(sorted(left_words)), " ".join(sorted(right_words))).ratio()

    # Exact multi-word venue/company names are a strong match even when one
    # publisher omits the name from its headline and only includes it in the
    # feed excerpt. This catches paraphrased coverage without broadening the
    # generic title-similarity thresholds below.
    different_publishers = left.get("source_id") != right.get("source_id")
    if different_publishers and named_phrases(left) & named_phrases(right):
        return 0.72

    # The same name also identifies a story when one publisher keeps it out of
    # the headline and only the excerpt carries it. That evidence is weaker,
    # because an excerpt often names a venue in passing, so one shared name is
    # only accepted with corroborating structure: a second independent name, a
    # longer name, or a filing gap short enough that both outlets are clearly
    # working from the same announcement.
    if different_publishers and rare_tokens:
        matches = shared_entities(
            named_phrases(left) | summary_named_phrases(left, rare_tokens),
            named_phrases(right) | summary_named_phrases(right, rare_tokens),
        )
        if matches and (
            len(matches) >= 2
            or any(len(phrase.split()) >= 3 for phrase in matches)
            or filed_within_hours(left, right)
        ):
            return 0.70

    # Three shared distinctive words is the minimum. This avoids grouping
    # articles that merely share a company, city, award, or broad event theme.
    if len(shared) >= 4 and jaccard >= 0.42:
        return round((jaccard * 0.7) + (sequence * 0.3), 3)
    if len(shared) >= 3 and jaccard >= 0.58 and sequence >= 0.68:
        return round((jaccard * 0.7) + (sequence * 0.3), 3)
    return 0.0


def text_similarity(left: str, right: str) -> float:
    left_words = set(normalized_words(left))
    right_words = set(normalized_words(right))
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / len(left_words | right_words)


def first_sentences(value: str, limit: int = 2) -> list[str]:
    text = re.sub(r"\s+", " ", value or "").strip()
    if not text:
        return []
    chunks = re.split(r"(?<=[.!?])\s+", text)
    results: list[str] = []
    for chunk in chunks:
        cleaned = chunk.strip()
        if len(cleaned) < 25:
            continue
        if len(cleaned) > 280:
            cleaned = cleaned[:279].rsplit(" ", 1)[0] + "…"
        results.append(cleaned)
        if len(results) >= limit:
            break
    return results or [text[:279].rsplit(" ", 1)[0] + ("…" if len(text) > 280 else "")]


def source_view(article: dict) -> dict:
    return {
        "article_id": article["id"],
        "source_id": article["source_id"],
        "source_name": article["source_name"],
        "source_type": article["source_type"],
        "access": article.get("access", "open"),
        "corroboration_role": article.get("corroboration_role", "independent_editorial"),
        "country": article["country"],
        "language": article["language"],
        "title": article["title"],
        "summary": article.get("summary", ""),
        "url": article["url"],
        "published_at": article.get("published_at"),
        "image_url": article.get("image_url"),
    }


def build_brief(group: list[dict]) -> dict:
    distinct_sources = []
    seen = set()
    for article in group:
        if article["source_id"] in seen:
            continue
        seen.add(article["source_id"])
        distinct_sources.append(article)

    if len(distinct_sources) == 1:
        return {
            "type": "feed_excerpt",
            "review_status": "source_metadata_only",
            "bullets": [],
        }

    bullets = []
    seen_text = set()
    for article in distinct_sources:
        for sentence in first_sentences(article.get("summary", ""), limit=1):
            key = " ".join(normalized_words(sentence))[:180]
            if not key or key in seen_text:
                continue
            seen_text.add(key)
            bullets.append(
                {
                    "text": sentence,
                    "source_ids": [article["source_id"]],
                    "evidence_urls": [article["url"]],
                }
            )
        if len(bullets) >= 3:
            break

    return {
        "type": "extractive_evidence_brief",
        "review_status": "automated_unreviewed",
        "bullets": bullets,
    }


def build_clusters(
    articles: list[dict],
    priorities: dict[str, int],
    entity_matching: bool = True,
) -> list[dict]:
    parents = list(range(len(articles)))
    edge_scores: dict[tuple[int, int], float] = {}
    rare_tokens = rare_title_tokens(articles) if entity_matching else None

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[right_root] = left_root

    for left_index, left in enumerate(articles):
        for right_index in range(left_index + 1, len(articles)):
            score = cluster_score(left, articles[right_index], rare_tokens)
            if score:
                edge_scores[(left_index, right_index)] = score
                union(left_index, right_index)

    grouped: dict[int, list[tuple[int, dict]]] = {}
    for index, article in enumerate(articles):
        grouped.setdefault(find(index), []).append((index, article))

    clusters = []
    for members in grouped.values():
        member_indexes = {index for index, _ in members}
        group_articles = [article for _, article in members]
        group_articles.sort(
            key=lambda article: (priorities.get(article["source_id"], 0), article.get("published_at") or ""),
            reverse=True,
        )
        lead = group_articles[0]
        sources = [source_view(article) for article in group_articles]
        distinct_source_count = len({source["source_id"] for source in sources})
        independent_source_count = len(
            {
                source["source_id"]
                for source in sources
                if source.get("corroboration_role") in {"independent_editorial", "editorial_guide"}
            }
        )
        summary_similarities = [
            text_similarity(group_articles[left].get("summary", ""), group_articles[right].get("summary", ""))
            for left in range(len(group_articles))
            for right in range(left + 1, len(group_articles))
        ]
        likely_syndicated = bool(summary_similarities and min(summary_similarities) >= 0.72)
        coverage_pattern = (
            "single_source"
            if distinct_source_count == 1
            else "likely_syndicated"
            if likely_syndicated
            else "independently_reported"
            if independent_source_count > 1
            else "mixed_primary_and_editorial"
        )
        scores = [
            score
            for (left, right), score in edge_scores.items()
            if left in member_indexes and right in member_indexes
        ]
        fingerprint = "|".join(sorted(article["id"] for article in group_articles))
        cluster_id = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:16]
        brief = build_brief(group_articles)
        clusters.append(
            {
                "id": cluster_id,
                "edition": lead["edition"],
                "language": lead["language"],
                "topic": lead["topic"],
                "title": lead["title"],
                "summary": lead.get("summary", ""),
                "image_url": lead.get("image_url"),
                "image_usage": lead.get("image_usage", "review_required"),
                "published_at": max((article.get("published_at") or "" for article in group_articles), default=None),
                "source_count": distinct_source_count,
                "independent_source_count": independent_source_count,
                "coverage_pattern": coverage_pattern,
                "max_summary_similarity": round(max(summary_similarities), 3) if summary_similarities else 0.0,
                "article_count": len(group_articles),
                "cluster_confidence": "single_source" if len(group_articles) == 1 else "high" if min(scores or [0]) >= 0.68 else "medium",
                "similarity_scores": scores,
                "brief": brief,
                "review_status": brief["review_status"],
                "sources": sources,
            }
        )

    clusters.sort(key=lambda cluster: cluster.get("published_at") or "", reverse=True)
    return clusters


def build_payload(article_payload: dict, registry: dict) -> dict:
    priorities = {source["id"]: int(source.get("priority", 0)) for source in registry["sources"]}
    clusters = build_clusters(article_payload["articles"], priorities)
    multi_source = sum(1 for cluster in clusters if cluster["source_count"] > 1)
    independently_corroborated = sum(
        1 for cluster in clusters if cluster["coverage_pattern"] == "independently_reported"
    )
    return {
        "schema_version": 2,
        "generated_at": article_payload["generated_at"],
        "source_count": article_payload.get("source_count", len({article["source_id"] for article in article_payload["articles"]})),
        "article_count": len(article_payload["articles"]),
        "cluster_count": len(clusters),
        "multi_source_cluster_count": multi_source,
        "independently_corroborated_cluster_count": independently_corroborated,
        "clustering": {
            "method": "conservative_title_similarity_v1",
            "briefing": "extractive_feed_evidence_only",
            "llm_used": False,
        },
        # Retained in clusters.json for local auditability. write_payload strips
        # this raw evidence array from the browser bundle because the UI reads
        # clusters only.
        "articles": article_payload["articles"],
        "clusters": clusters,
    }


def write_payload(payload: dict, cluster_path: Path, js_path: Path) -> None:
    cluster_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cluster_fields = {
        "id", "edition", "language", "topic", "title", "summary", "image_url", "image_usage",
        "published_at", "source_count", "independent_source_count", "coverage_pattern",
        "cluster_confidence", "brief", "review_status",
    }
    source_fields = {"source_name", "source_type", "title", "url", "corroboration_role", "country", "image_url"}
    browser_clusters = []
    for cluster in payload["clusters"]:
        browser_cluster = {key: value for key, value in cluster.items() if key in cluster_fields}
        browser_cluster["sources"] = [
            {key: value for key, value in source.items() if key in source_fields}
            for source in cluster["sources"]
        ]
        browser_clusters.append(browser_cluster)
    browser_payload = {
        key: value
        for key, value in payload.items()
        if key not in {"articles", "clusters"}
    }
    browser_payload["clusters"] = browser_clusters
    js_path.write_text(
        "window.MISE_LIVE_NEWS = " + json.dumps(browser_payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articles", type=Path, default=DEFAULT_ARTICLES)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_CLUSTERS)
    parser.add_argument("--js-output", type=Path, default=DEFAULT_JS)
    args = parser.parse_args()

    article_payload = json.loads(args.articles.read_text(encoding="utf-8"))
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    payload = build_payload(article_payload, registry)
    write_payload(payload, args.output, args.js_output)
    print(
        json.dumps(
            {
                "articles": payload["article_count"],
                "clusters": payload["cluster_count"],
                "multi_source_clusters": payload["multi_source_cluster_count"],
                "independently_corroborated_clusters": payload["independently_corroborated_cluster_count"],
                "method": payload["clustering"]["method"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
