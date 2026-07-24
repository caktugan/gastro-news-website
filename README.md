# MISE — gastronomy news prototype

An English-first, dark editorial prototype for an AI-curated gastronomy news product, with Austria and Global editions. Vienna reporting is included and prioritised inside Austria rather than separated into a quieter edition.

For the durable product decisions, deferred features, known limitations, and new-task handoff, read [`docs/PROJECT_HANDOFF.md`](docs/PROJECT_HANDOFF.md).

## Run locally

From this folder:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Then open [http://127.0.0.1:4173](http://127.0.0.1:4173).

## Refresh the source data and English Austria edition

The source registry lives in `data/sources.json`. To retrieve the active RSS/Atom feeds, normalize their metadata, filter broad official feeds, and rebuild the browser dataset:

```powershell
python .\scripts\update.py
```

This retrieves the active feeds, refreshes the official operator-cost benchmarks, rebuilds the clusters and source-driven trend radar, verifies the official event calendar, and prepares up to 100 recent Austria stories for the English edition. It also writes `data/update-status.json` and `data/update-status.js`, which power the reader-facing Data health control. The pipeline is failure-tolerant: independent stages continue after a failure and verified cached values remain available, while the command still exits non-zero when a worker actually fails.

The Austria enrichment worker uses 45 curated English translations first, then a cache of unchanged model results. New German-language items are translated and screened with Gemini by default. Set `GEMINI_API_KEY` locally:

```powershell
$env:GEMINI_API_KEY = "your-new-key"
python .\scripts\update.py
```

Do not put an API key in this repository or paste it into a chat. The default model is `gemini-3.1-flash-lite`, selected for low-cost, high-volume work and structured-output support. Mistral remains an automatic fallback when `GEMINI_API_KEY` is absent and `MISTRAL_API_KEY` is available. Select a provider explicitly with `--provider gemini` or `--provider mistral`; override its model with `--model`, `MISE_GEMINI_MODEL`, or `MISE_MISTRAL_MODEL`. Only publisher feed titles, short excerpts, dates, attribution, and source-role metadata are sent; article bodies and publisher images are not retrieved or submitted.

### Free-tier AI budget

The updater is deliberately safe for a free Gemini account. It batches eight stories per request, permanently reuses unchanged summaries, and allows at most **15 API attempts per provider per UTC day** by default. Every attempt, including a retry after a transient error, is reserved in the private local ledger `data/.ai-usage.json` before network access. Once the limit is reached, the updater stops AI enrichment without deleting cached or manually curated content; remaining stories stay pending for a later run.

The final `data/austria-enrichment-report.json` records requests used and remaining, attempted items, processed items, and pending items. Preview the current workload and remaining budget without making a request:

```powershell
python .\scripts\enrich_austria.py --dry-run
```

Override the ceiling for one run, or set it persistently for the current shell:

```powershell
python .\scripts\update.py --max-api-requests 10
$env:MISE_DAILY_AI_REQUEST_LIMIT = "10"
```

Use `--max-api-requests 0` or `--no-api` for a guaranteed zero-request run. The ledger controls only this local application; requests made by other projects using the same API key still count against Google's project quota and will not appear in this file.

Use `--skip-events` when you want to rebuild news data without contacting official organizer pages. Use `--skip-markets` to retain the current operator-cost cache without contacting official benchmark endpoints.

To test the complete local path without any API request:

```powershell
python .\scripts\update.py --skip-fetch --no-api
```

To inspect which stories would be selected without changing output files:

```powershell
python .\scripts\enrich_austria.py --dry-run
```

If no provider key is present, the updater completes in safe fallback mode: the 45 curated Austria stories stay available, cached automated translations remain usable, and the report records the missing provider key. Model output is constrained to structured JSON and supplied feed evidence, but automated drafts should still pass editorial review before a production publication workflow.

To rebuild clusters without fetching the feeds again:

```powershell
python .\scripts\cluster.py
```

## Refresh operator-cost benchmarks

The News page includes a vertical hospitality-market tape and individual detail pages for nine official series: Austria bread wheat, raw milk, barn eggs, whole broiler chicken and class E pigmeat; an EU butter reference; Milan crude sunflower oil; Italian bulk extra-virgin olive oil; and EUR/USD. Refresh it with:

```powershell
python .\scripts\update_markets.py
```

This worker uses only public, keyless structured endpoints from the European Commission Agri-food Data Portal and the European Central Bank. It makes **zero AI requests**. It writes the full audit cache to `data/markets.json` and the small browser payload to `data/markets.js`. Each value retains its unit, reporting frequency, observation date, source link, recent history, and comparison basis. Reference values are directional wholesale or macro benchmarks, not prices a restaurant is guaranteed to receive from a supplier.

If one endpoint is temporarily unavailable, the worker preserves that benchmark's previous cached value, marks it stale, and records the error instead of inventing a replacement.

## Automated refresh and deployment

The deployment-ready workflow at `.github/workflows/refresh-and-deploy.yml` refreshes the complete product four times daily, runs the test suite, builds a public-only `dist` artifact, and deploys it to GitHub Pages. It restores the enrichment ledger and model-result cache between runs so scheduled refreshes do not repeatedly spend the free-tier AI budget on unchanged stories. The public artifact excludes source-audit files, raw article data, enrichment caches, scripts, tests, and credentials.

After this folder is published to a GitHub repository:

1. In **Settings → Pages**, choose **GitHub Actions** as the publishing source.
2. In **Settings → Secrets and variables → Actions**, create a repository secret named `GEMINI_API_KEY`. Do not put the value in a workflow file.
3. Run **Refresh and deploy MISE** manually once from the Actions tab. Scheduled runs then use Europe/Vienna time.

To inspect the exact public bundle locally without refreshing any data:

```powershell
python .\scripts\build_site.py
```

## Rebuild the industry trend radar

The trend radar and catalogued social-source directory are rebuilt automatically by `scripts/update.py`. To rebuild the radar from the current clustered article evidence without fetching feeds or making an AI request:

```powershell
python .\scripts\build_trends.py
```

The detector uses curated English and German theme patterns, a 14-day evidence window, distinct-publisher breadth, and Austria relevance. Coverage direction compares a theme's share of all available stories with the prior window, rather than comparing raw counts, because RSS feeds retain recent history unevenly. These labels describe changing **publisher attention**, not measured consumer demand or market growth. Every signal expands to the source stories that caused it to appear. The detector records zero AI requests.

## Refresh and verify the events calendar

Official event sources and their publication rules live in `data/event-sources.json`. Refresh the calendar independently with:

```powershell
python .\scripts\update_events.py
```

The updater checks each configured event's identity and configured date markers on the organizer's official page, publishes only verified upcoming events, removes expired dates automatically, and deduplicates matching listings. It does not rewrite dates from page text automatically: when an organizer moves an event and its expected markers disappear, the cached record becomes stale until the registry is reviewed. Event-like stories found in the news clusters are written to `data/event-review.json`; they do not enter the public calendar until an organizer source confirms the date. The current source set covers Vienna Coffee Festival, Vienna Wine Hiking Day, a WKO Vienna gastronomy seminar, FAFGA, Alles für den Gast, and BIOFACH. This workflow uses zero AI requests.

After a summary-prompt change, regenerate the selected Austria stories from the current feed evidence without fetching every source again:

```powershell
python .\scripts\update.py --skip-fetch --refresh-enrichment
```

Clustering is deliberately conservative: articles must use the same language and edition, fall within a four-day window, and either share several distinctive title terms or an exact multi-word venue/company name found in the feed evidence. Multi-source briefs are extractive and retain evidence URLs per bullet. This stage does not call a generative model.

`data/clusters.json` retains the complete local evidence payload for auditing. The generated browser bundle deliberately omits raw articles and unused source metadata so readers do not download backend-only data.

## Source discovery and social signals

The production registry is `data/sources.json`. The broader discovery inventory and its latest technical audit are stored in `data/source-candidates.json` and `data/source-audit.json`. The July 2026 inventory contains 206 source candidates; the latest audit found 91 with technically discoverable feeds. A discoverable feed is reviewed for scope, access, and rights before activation. Re-run the public feed/social-link audit with:

```powershell
python .\scripts\audit_sources.py
```

The audit checks public homepages for advertised RSS/Atom feeds and site-linked official social accounts. It does not crawl article bodies, bypass paywalls, or imply republication permission.

The registry is Austria-first. Vienna has a dedicated discovery layer covering city and district reporting, official market and hospitality bodies, local food/lifestyle publishers, guides, and first-party social signals. Austria-wide coverage includes national trade media and all nine ORF regional newsrooms. Broad feeds are subject to gastronomy filters, and sources presented as Vienna-specific may also require geographic scope terms. Stale or noisy feeds remain in the review queue rather than the live collector.

Reddit communities and official publisher, supplier, creator, and executive social accounts are catalogued separately in `data/signals.json`. A public post may appear in the product as a clearly labelled Social Post with its platform, source class, original link, and uncertainty intact. Material claims must be corroborated before the post becomes a MISE news briefing or a confirmed opening/closure record; supplier and executive accounts remain labelled first-party.

The public Monthly tracker includes a social-source directory generated by `scripts/build_social_watch.py`. It publishes channel names and outbound links only—never usernames, user posts, or scraped profile data. Its current status describes the inventory, not verified API access or retrieved posts. Reddit content requires approved Data API access, while Instagram and other closed platforms remain manual or permissioned-API sources. Until that access exists, the interface does not manufacture a social feed; future approved items already have dedicated Social post and first-party labels in the tracker.

Falstaff, Falstaff PROFI, Transgourmet, KRÖSWANG, WKO, VOL.AT, Michelin and Statistics Austria are in the permission/licensing queue because a suitable public feed or structured-data agreement was not confirmed. Die Presse, profil, Sifted and Just Food expose feeds but remain inactive pending mixed/paid-access review. Gault&Millau Austria and AHGZ Austria expose public feeds, so only their feed metadata and excerpts are indexed; restricted article content is never retrieved. The former Hotel & Touristik portal is represented by its current successor, AHGZ Austria, rather than duplicated as a separate source.

The 2026-07-24 review added the B2B trade, Bundesland, wholesale-supply and regulatory layers. Rolling Pin consolidated its `.at`, `.de` and `.ch` sites onto `rollingpin.com`, so the registry now uses the canonical domain and adds its distinct People, Konzepte & Openings, Industry News, Top Supplier News and Careers section feeds. VOL.AT stays out of the collector: its Gastronomie tag page exposes no feed, and the general `/rss` feed starts returning a binary bot-protection payload under a `text/xml` content type after repeated automated requests, so it is recorded as rate-limited review alongside FoodBev. NÖN and BVZ publish 100-entry feeds, so their `max_items` is set high enough for the collector to scan the whole feed rather than only the newest entries. Lebensmittel Zeitung, Kleine Zeitung, OÖNachrichten, Salzburger Nachrichten and Tiroler Tageszeitung expose public feeds but stay inactive pending paid-access review. APA-OTS, Vienna.at, Vorarlberger Nachrichten and Handelszeitung advertise no working public feed. produktwarnung.at fails TLS certificate verification, so it is not ingested and certificate validation is never disabled to reach it; AGES and RASFF cover the same recall beat. artichox is recorded at low priority with an explicit warning that it resurfaces older articles under refreshed dates and is not a primary source for a fact. The Rolling Pin issue archive is reference-only: its gated magazine content is never ingested, and it exists in the registry for the editorial calendar and low-frequency issue detection.

Statistical and regulatory reference sources — WIFO, IHS, E-Control, the EU Agri-Food Data Portal, the Milk Market Observatory, AMI, Produktenbörse Wien, EUR-Lex, RASFF, DG SANTE, BMF FinDok, the Fairnessbüro, the Bundeswettbewerbsbehörde and GS1 — are catalogued in `data/source-candidates.json` rather than wired into the RSS news collector. They are inputs for the operator-cost and regulatory-deadline workstreams, which use structured endpoints instead of feeds.

## Included in this prototype

- Austria and Global editions, with Vienna prioritised inside Austria
- Top-level News, Calendar, and Monthly Tracker navigation
- Dark editorial interface
- Responsive desktop and mobile layouts
- Source-ranked Top News section with one lead development and topic-diverse supporting stories
- Discover-inspired, image-led story grid with automatic loading as the reader scrolls
- Relevance-ranked and latest-story views
- Topic filters
- Dedicated monthly Austria opening tracker with evidence-linked reports grouped by publication month and explicit date semantics
- Verified gastronomy calendar for trade fairs, festivals, tastings, and industry gatherings
- Keyless operator-cost watch with official sources, dated observations, units, trend history, and honest stale states
- Subtle, expandable industry trend bar with publisher breadth, Austria/global mix, normalized coverage direction, and source evidence
- Editorial review metadata for a future private control surface; it is not exposed in the public reader
- Story-title, summary, topic, and location search
- Saved-story interactions
- Current Austria and Global feed metadata with links to original reporting
- Cached, structured English translation and relevance screening for the Austria edition
- Conservative story clustering with source-count and confidence metadata
- Shared-press-release detection so repeated announcements are not mistaken for independent confirmation
- Extractive, evidence-linked briefs for corroborated clusters
- Prototype AI briefing drawer for sample stories
- Source and editorial-transparency patterns
- Original generated editorial imagery

Indexed items contain only publisher-provided feed metadata and excerpts. For Austria, the enrichment worker turns that evidence into a compact 70–130 word English summary when the source material supports it; thin feed evidence produces a shorter summary rather than invented detail. New enrichment requests explicitly ask for varied, factual journalistic headline structures without clickbait or unsupported colour. The ingestion worker does not crawl article bodies or bypass paywalls. The local prototype displays image candidates supplied directly in publisher feeds and falls back to optimised category artwork when they fail; production launch still requires a documented thumbnail-rights policy. Automated Austria translations preserve the original source title and link in the story drawer. Review metadata remains in the data model for a future private editorial surface with persistent approvals, user roles, audit history, and claim-level evidence decisions.

Saved stories persist as compact snapshots in the current browser with `localStorage`, so an item remains available after it leaves the newest generated feed; no account is required. The current interface is English-only. Future German and Turkish localization should translate interface copy and story fields while keeping original-source titles and source-language metadata available.
