# MISE project handoff and decision record

Last updated: 22 July 2026

This file is the durable context for continuing MISE in a new Codex task. Read it together with `README.md` and `AGENTS.md` before changing product direction, ingestion, enrichment, or the public interface.

## Canonical project location

The working project is:

`C:\Users\caktu\Desktop\ChatGPT Workspace\projects\active\gastro-news-website`

An older copy still exists at `C:\Users\caktu\Documents\Gastro news website`. Do not make new product changes in that older copy. The canonical repository contains the completed redesign commit `cb6b0fc` (`feat: refocus news desk and market intelligence`).

## Product purpose

MISE is a daily intelligence product for people working in gastronomy, especially operators and industry professionals in Vienna and Austria. It should help a reader quickly understand:

- the most important Austrian gastronomy developments;
- business, economic, labour, cost, supplier, and company news affecting the industry;
- emerging restaurant and hospitality trends;
- meaningful new openings and closures;
- upcoming gastronomy events, fairs, tastings, and trade gatherings;
- relevant global developments after Austrian coverage.

The product is not intended to be a consumer restaurant directory or a generic food-lifestyle feed.

## Core editorial decisions

- The public product is English-first. German and Turkish are future localization options.
- Austria and Global are the only news editions. Vienna is prioritised inside Austria instead of being a separate, quieter edition.
- AI is an editorial finishing layer, never the factual source. Feed evidence, official data, and attributable sources remain the basis of every item.
- Reporting, first-party announcements, and social posts must remain visibly distinct.
- Summaries must not imply access to full article bodies. The ingestion pipeline uses feed titles, excerpts, dates, images, attribution, and source metadata; it does not bypass paywalls.
- Source attribution and original links are mandatory.
- Routine openings and closures belong mainly in the Tracker. They appear in News only when editorially significant, such as a major chain entering Austria or a notable institution closing.
- News ranking should favour operator usefulness: company performance, prices, inflation, labour, wages, regulation, taxation, insolvencies, investment, suppliers, and market changes.
- Headlines should remain factual and neutral but use varied journalistic structures. Avoid repetitive templates, clickbait, unsupported colour, and invented conclusions.
- Trend detection should be source-driven and deterministic. AI is not required to decide that a trend exists.

## Public information architecture

### News

- Top navigation contains News, Calendar, and Monthly Tracker, with Search on the right.
- The former sidebar was removed.
- News has Austria and Global edition controls.
- The top briefing is simply a Top News segment: one lead story and supporting stories selected for relevance and topic diversity.
- The main feed is a Discover-inspired image-led grid with automatic loading as the reader scrolls.
- Routine opening/closure stories are filtered out of the News feed.
- Publisher-feed image candidates are shown when available, with optimized local category artwork as a fallback.

### Hospitality Tape

- The former Gastro Pulse module was removed.
- A vertical market module called **The Hospitality Tape** appears beside the News feed on desktop and becomes a horizontally scrollable strip on mobile.
- Clicking a benchmark opens its own detail view with current value, change, observation date, chart history, methodology, and official source.
- Current series: Austria bread wheat, raw milk, barn eggs, whole broiler chicken, class E pigmeat; EU butter; Milan crude sunflower oil; Italian bulk extra-virgin olive oil; and EUR/USD.
- These are directional wholesale or macro references, not guaranteed supplier prices.

### Trend Radar

- Trend Radar is deliberately subtle: a compact expandable bar rather than a dominant dashboard.
- It uses curated German and English theme rules, distinct-publisher breadth, Austria relevance, and comparison windows.
- Its direction describes changing publisher attention, not proven consumer demand or market growth.
- The feature is being retained for now, but its information design may be reconsidered after further product review.

### Monthly Tracker

- The Tracker is monthly, not weekly.
- It groups opening and closure reports by publication month and explains that the date is a reporting date unless the source confirms an event date.
- It includes opening, opening-soon, closed, and unconfirmed evidence states where supported.
- It also contains the Vienna-focused source directory for opening discovery and social monitoring.

### Calendar

- The Calendar covers verified gastronomy events, fairs, festivals, tastings, and useful industry gatherings.
- Organizer pages are the authority for dates.
- News mentions may enter a review queue but do not become public calendar events without official confirmation.

## AI and cost policy

- Gemini is the default enrichment provider; Mistral remains an optional fallback.
- Preserve the free-tier safeguards: batches of eight, cached results, and a default ceiling of 15 API attempts per provider per UTC day.
- The private usage ledger reserves attempts before network access so failures and retries still count.
- `--no-api` or `--max-api-requests 0` must continue to guarantee a zero-request run.
- Never commit API keys, `.env` files, usage ledgers, or private caches.
- Prompt changes do not automatically justify spending calls to rewrite unchanged cached stories. Existing cache should be preserved unless regeneration is explicitly requested.
- Market data, trend detection, event verification, clustering, and source audits use zero AI requests.

## Sources and social media

- Coverage is Austria-first and should especially serve Vienna operators.
- Trade media, business/economy reporting, official bodies, regional newsrooms, suppliers, and company announcements all have distinct editorial value.
- Paid or restricted publications may contribute public feed metadata and excerpts where allowed; restricted article bodies are never copied.
- Reddit and Instagram are valid source types for opening discovery and first-party announcements, not merely invisible leads.
- When shown publicly, a social item must be labelled as a Social Post with platform, source class, original link, and uncertainty preserved.
- A social claim does not become confirmed news merely because it was posted. Material claims require corroboration.
- Reddit requires approved API access; Instagram and other closed platforms require manual or permissioned access. Do not fabricate a live social feed when access is absent.

## Deferred or explicitly excluded features

Do not add these without the user explicitly reintroducing them:

- user accounts;
- newsletters;
- a venue-address database.

Also deferred:

- German and Turkish localization;
- a production editorial approval system with roles and audit history;
- automated Instagram ingestion without permissioned access;
- a final redesign of the News grid, pending the user's visual review.

## Current technical shape

The data path is:

1. source registry and public feed ingestion;
2. normalized article metadata;
3. deterministic clustering and shared-release detection;
4. cached Austria translation/relevance enrichment where needed;
5. source-driven trend, market, event, tracker, and social-directory builders;
6. small public JavaScript data bundles;
7. static English reader interface.

Important commands and worker behavior are documented in `README.md`. The full updater is failure-tolerant and preserves verified cached values if an independent endpoint fails.

## Current validation baseline

- 40 Python tests passed after the July 2026 redesign.
- JavaScript syntax validation passed.
- The static public bundle built successfully.
- Nine market benchmarks refreshed with zero source errors.
- Desktop and 390 px mobile browser checks showed no page-level horizontal overflow.
- Commodity detail navigation, the collapsed Trend Radar, and monthly Tracker navigation were verified in the local preview.

After Python worker changes, run:

```powershell
python -m unittest discover -s tests -v
```

After interface changes, verify the local preview at `http://127.0.0.1:4173/` on desktop and mobile widths.

## Known limitations and risks

- Publisher-feed image availability does not establish republication rights. A production thumbnail-rights and licensing policy is still required.
- Many publishers expose only thin excerpts, so summaries must remain proportionate to available evidence.
- Existing cached headlines retain older structures; the improved headline prompt affects new or explicitly regenerated enrichment.
- Social monitoring currently publishes a source directory rather than pretending that closed-platform posts have been ingested.
- Conservative clustering produces fewer multi-source clusters but avoids presenting syndicated releases as independent corroboration.
- Market benchmarks are official references with mixed reporting frequencies and should not be presented as live procurement quotes.
- Saved stories use local browser storage and do not sync between devices.

## Recommended next product review

The next task should begin with the user reviewing the current build and listing visual or editorial changes. Likely high-value follow-ups are:

1. decide the final News-page visual hierarchy;
2. expand Austrian business, economy, supplier, and company source coverage;
3. review publisher thumbnail rights and permitted-image policy;
4. improve event-source breadth and confirmed event-date coverage;
5. assess Trend Radar usefulness before investing further in its presentation;
6. prepare production hosting and scheduled refresh only after the reader experience is approved.

