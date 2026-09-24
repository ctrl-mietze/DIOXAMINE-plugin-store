#!/usr/bin/env python3
"""Assemble only public discovery-site assets and package downloads for Pages."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"

if OUTPUT == ROOT or OUTPUT.parent != ROOT:
    raise SystemExit("Refusing to build outside the repository root")
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir()

for name in ("index.html",):
    shutil.copy2(ROOT / name, OUTPUT / name)
for name in ("assets", "plugins", "catalogue"):
    shutil.copytree(ROOT / name, OUTPUT / name)
(OUTPUT / "store-plugin").mkdir()
shutil.copy2(ROOT / "store-plugin/plugin.zip", OUTPUT / "store-plugin/plugin.zip")
(OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built GitHub Pages site in {OUTPUT}")
