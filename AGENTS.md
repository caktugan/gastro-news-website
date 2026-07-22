# Project guidance

This is the active MISE gastronomy news website project.

## Product direction

- Keep the public interface English-first; German and Turkish are future options.
- Prioritize Vienna and Austria reporting, then global gastronomy industry news.
- Treat AI as an editorial finishing layer, not as the source of facts.
- Preserve source attribution and distinguish reporting, first-party announcements, and social posts.
- Do not add user accounts, newsletters, or a venue-address database unless the user explicitly reintroduces them.

## Implementation

- Read `README.md` before changing ingestion, enrichment, or local-run workflows.
- Never commit API keys or credentials. Keep `.env` files ignored.
- Preserve cached enrichment and the daily AI request ceiling unless a change is explicitly requested.
- Run `python -m unittest discover -s tests -v` after changing Python workers.
- Verify interface changes through the local preview at `http://127.0.0.1:4173/`.
