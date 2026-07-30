"""Assemble the public-only MISE static site in ``dist`` for deployment."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"
PUBLIC_FILES = ("index.html", "app.js", "styles.css")
PUBLIC_DATA = (
    "live-news.js",
    "events.js",
    "markets.js",
    "trends.js",
    "social-watch.js",
    "update-status.js",
)


def build(output: Path = OUTPUT) -> Path:
    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    (output / "data").mkdir(parents=True)
    for name in PUBLIC_FILES:
        shutil.copy2(ROOT / name, output / name)
    for source in (ROOT / "assets").glob("*.webp"):
        shutil.copy2(source, output / "assets" / source.name)
    for name in PUBLIC_DATA:
        shutil.copy2(ROOT / "data" / name, output / "data" / name)
    (output / ".nojekyll").write_text("", encoding="utf-8")
    return output


if __name__ == "__main__":
    destination = build()
    print(f"Built public site at {destination}")
