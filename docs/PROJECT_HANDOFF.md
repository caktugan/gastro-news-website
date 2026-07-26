# MISE project handoff and decision record

Last updated: 26 July 2026

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

- **The public product is native-language as of 2026-07-25.** Every story is published in the language it was filed in: Austrian reporting stays German, and Global carries English and German side by side. Tiles show a language tag. An English edition is a future option, not the current base — see the decision record at the end of this file.
- **German and English are the only languages carried.** The single French source was dropped on 2026-07-25; see that day's second decision record.
- Austria and Global are the only news editions. Vienna is prioritised inside Austria instead of being a separate, quieter edition.
- AI is an editorial finishing layer, never the factual source. Feed evidence, official data, and attributable sources remain the basis of every item. **Nothing on the public site is currently AI-generated**: the enrichment stage runs with `--no-api`.
- Reporting, first-party announcements, and social posts must remain visibly distinct.
- Summaries must not imply access to full article bodies. The ingestion pipeline uses feed titles, excerpts, dates, images, attribution, and source metadata; it does not bypass paywalls.
- Source attribution and original links are mandatory.
- Routine openings and closures were once filtered out of News and left to the Tracker. **That filter was removed on 2026-07-25**: its significance keywords were English-only and, against a German feed, it suppressed Austrian openings almost categorically. Ranking now decides prominence instead of a gate.
- News ranking should favour operator usefulness: company performance, prices, inflation, labour, wages, regulation, taxation, insolvencies, investment, suppliers, and market changes.
- Headlines should remain factual and neutral but use varied journalistic structures. Avoid repetitive templates, clickbait, unsupported colour, and invented conclusions.
- Trend detection should be source-driven and deterministic. AI is not required to decide that a trend exists.

## Public information architecture

### News

- Top navigation contains News, Calendar, and Monthly Tracker, with Search on the right.
- The former sidebar was removed.
- News has Austria and Global edition controls.
- The top briefing is a Top News segment: one lead card and two stacked secondaries, selected for relevance and topic diversity.
- The main feed is a six-track grid composed from three tile weights — `feature` (full width, image beside text), `standard` (half width, image above text) and `brief` (third width, no image, roughly a third the height). Two rhythms alternate so the feature does not land on a fixed beat, and the illustrated and imageless streams are composed separately.
- **Stock category artwork was removed on 2026-07-25.** A story either carries the publisher's own image or carries none; imageless stories become briefs, and imageless hero cards use the topic gradient with the story's initial. A publisher image that fails to load degrades to that same treatment rather than to stock.
- The Trend Radar was removed from the News page on 2026-07-25. `data/trends.js` is still built and read by the Tracker.

### Commodity Board

- The former Gastro Pulse module was removed.
- A vertical market module called **The Commodity Board** (renamed from "The Hospitality Tape" during the Night Desk redesign) appears beside the News feed on desktop, with benchmarks grouped by region (Austria, European Union, Global) as compact rows with sparklines.
- Clicking a benchmark opens its own detail view with current value, change, observation date, chart history, methodology, and official source.
- Current series: Austria bread wheat, raw milk, barn eggs, whole broiler chicken, class E pigmeat; EU butter; Milan crude sunflower oil; Italian bulk extra-virgin olive oil; and EUR/USD.
- These are directional wholesale or macro references, not guaranteed supplier prices.

### Trend Radar

- Removed from the News page on 2026-07-25. The signals still power the Tracker's Theme momentum bars, and `scripts/build_trends.py` still runs on every refresh.
- It uses curated German and English theme rules, distinct-publisher breadth, Austria relevance, and comparison windows.
- Its direction describes changing publisher attention, not proven consumer demand or market growth.

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

- **The enrichment stage is currently switched off.** The workflow runs `scripts/update.py --no-api`, so the public site makes zero AI requests. The stage still rebuilds its browser output from cache, and dropping the flag resumes it.
- Gemini is the default enrichment provider; Mistral is a real fallback since 2026-07-25 — when Gemini exhausts its budget or errors mid-run, the remaining batches continue on Mistral, which carries its own separate daily allowance. That failover has never fired in production.
- Preserve the free-tier safeguards: batches of eight, cached results, and a default ceiling of 25 API attempts per provider per UTC day.
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
7. static reader interface, serving each story in its original language.

Step 4 currently runs with `--no-api`, so it consumes its cache and calls no model. The site is deployed by GitHub Actions (`.github/workflows/refresh-and-deploy.yml`), which refreshes and redeploys four times daily and on every push to `master`, at <https://caktugan.github.io/gastro-news-website/>.

Important commands and worker behavior are documented in `README.md`. The full updater is failure-tolerant and preserves verified cached values if an independent endpoint fails.

## Current validation baseline

- 50 Python tests pass as of 2026-07-25.
- 40 Python tests passed after the July 2026 redesign.
- Run the suite as `PYTHONIOENCODING=utf-8 python -m unittest discover -s tests`. Without it, `test_enrich_austria` fails on a bare Windows console with a `UnicodeEncodeError` on `→`; that is the cp1252 console, not a code fault.
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

- **No editorial relevance gate remains.** The AI enrichment prompt used to set `publish=false` for recipes, adverts, non-Austrian items and text too thin to use, and it was withholding roughly a third of collected clusters. Switching the stage off removed that screen, and `isNewsworthyOpening` was removed separately. Only the per-source `filter_terms` at ingest still apply. If the feed drifts toward noise, the fix is a deterministic German-and-English relevance rule, ideally validated against what the AI screen used to reject.
- **`relevanceScore()`'s remaining German shortfall is editorial mix, not vocabulary.** German operator vocabulary was added on 2026-07-25, taking the German hit rate on the +22 `operatorImpact` bonus from 25% to 33% against 42% for English. Backtesting showed the rest of that gap is real: of the 157 German clusters the English-only list missed, most were wine tastings, chef moves and festivals, which should not score an operator bonus. Do not close the remaining gap by loosening the pattern.
- **German bare stems are traps in this feed, and the pattern deliberately uses compounds instead.** A `Preis` is as often a prize as a price and matched wine-guide items; `Gehalt` is a wine's body before it is a salary and matched `Riesling 2025 gehaltvoll`; `Gewinner` are competition winners; `gesetzt` is not a law. Any future addition to `OPERATOR_IMPACT_PATTERN` should be backtested the same way before shipping.
- Publisher-feed image availability does not establish republication rights. A production thumbnail-rights and licensing policy is still required. `image_usage` now records provenance (`feed_provided` / `none`) rather than an unfulfilled review, and the UI treats a publisher's own feed thumbnail as cleared.
- Many publishers expose only thin excerpts, so summaries must remain proportionate to available evidence.
- Existing cached headlines retain older structures; the improved headline prompt affects new or explicitly regenerated enrichment.
- Social monitoring currently publishes a source directory rather than pretending that closed-platform posts have been ingested.
- Conservative clustering produces fewer multi-source clusters but avoids presenting syndicated releases as independent corroboration.
- Market benchmarks are official references with mixed reporting frequencies and should not be presented as live procurement quotes.
- Saved stories use local browser storage and do not sync between devices.

## Recommended next product review

1. Watch the Austria feed for noise now that both relevance gates are gone, and build a deterministic screen if it drifts.
2. Expand Austrian business, economy, supplier, and company source coverage.
3. Improve event-source breadth beyond the current eleven verified events.
4. Reduce the deployed payload: `data/live-news.js` is roughly 520 KB of a 1.1 MB bundle.
5. Consider accessibility of the calendar month grid, which is currently 42 divs with no grid semantics.

Item 2 of the previous list — German and French ranking vocabulary — was settled on 2026-07-25. German was added; French was removed from the product instead.

## Decision record — 2026-07-25

The whole day's work sits in `git log`; these are the decisions behind it.

- **Night Desk restyle applied from `Austrian gastronomy news site/design_handoff_night_desk/`.** That bundle is design reference, not production code, and is gitignored. Where its README and its `.dc.html` prototypes disagreed, the prototypes generally won on layout and the README on tokens.
- **The market module is "The Commodity Board"** — the user's choice over the README's "Hospitality Tape" and the prototype's "Cost Board".
- **Native language over an English base.** The user's reasoning: the articles are already German and the audience reads German, so translating was both a cost and a ceiling. Austria went 113 → 188 stories and Global 210 → 269 the moment the gates came off. An English edition remains possible; the enrichment cache is kept warm for exactly that.
- **Show everything the collector holds.** `--limit` 100 → 250, the translation age window 30 → 90 days, and `isNewsworthyOpening` deleted. All 457 clusters now reach the feed.
- **Clustering was tightened, not loosened.** Names now match by whole-word containment, because German binds a brand to the noun before it ("ARION Jewelry" vs "Schmuckmarke ARION Jewelry"). Two earlier attempts were rejected by backtesting: rare-token matching produced 22 merges that were nearly all wrong, and exact phrase equality produced three false merges from incidental excerpt mentions. The shipped rule merges five clusters across the corpus, all correct.
- **Stock artwork removed**, because with a third of stories imageless the same four photographs repeated down the page and implied photography MISE does not have.
- **Three feeds are blocked to cloud runners** — foodservice, NÖN and BVZ return HTTP 403 to GitHub's IPs while working from a residential connection. They are `rate_limited_review`, not deleted.

## Decision record — 2026-07-25, ranking and language (commits `24eabbb`, `13da98c`)

Recorded 26 July. These two commits closed item 2 of the previous review list.

- **German operator vocabulary was added to `relevanceScore()`** (`24eabbb`). The keyword list had been English-only since before the product went native-language, so German stories reached the +22 `operatorImpact` bonus at 25% against 42% for English.
- **Backtesting changed the shape of that fix, and should change the next one too.** The premise — that the gap was purely vocabulary — turned out to be half wrong. Of the 157 German clusters the old list missed, only about 17 were genuine operator stories; the rest were wine tastings, chef moves and festivals that correctly earn no bonus. So a precise compound list shipped rather than a broad stem list. German went to 33%, English was unchanged with zero regressions, and all 17 newly matched stories were inspected individually.
- **Bare German stems were rejected as false-positive traps.** `Preis` matched wine guides because it means prize as often as price; `Gehalt` matched `Riesling 2025 gehaltvoll` because it is a wine's body before it is a salary; `Gewinner` are competition winners; `gesetzt` is not a law. `OPERATOR_IMPACT_PATTERN` therefore uses `preiserhöhung`, `lohnkosten`, `gesetzlich` and similar compounds. This is the same discipline that rejected two clustering rules the day before.
- **Measured product effect, not just hit rate.** In the Austria feed the `Teuerung` monitor moved sixth to third, `Neun von zehn Betrieben finden kaum Personal` and the Taflo expansion entered the top 20, and two soft sustainability items left it. The Top News trio was unchanged, because topic diversity in `selectDailyBriefing()` dominates the lead selection.
- **French was removed from the product rather than ranked** (`13da98c`). The user's call. Gault&Millau International was the only French source and the only reason the feed carried a third language; its nine items were gala evenings, a Guide Jaune launch and a magazine issue — guide business, not industry reporting, and nothing a Vienna operator needs. Adding French ranking vocabulary would have promoted content the audience does not read. `Gault&Millau Austria` is German, Austria edition, and stays.
- The registry went 101 sources to 100, 73 active feeds to 72. Because `ingest.py` rebuilds `articles.json` from the active registry each run rather than accumulating history, the nine French clusters cleared on the next refresh with no data edit. Verified on the deployed bundle: 240 German, 210 English, no French.

