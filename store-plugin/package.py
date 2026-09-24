#!/usr/bin/env python3
"""Package the in-app Store plugin in DIOXAMINE's current ZIP format."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "plugin.zip"
FILES = (
    ("plugin.json", "plugin.json"),
    ("index.html", "index.html"),
    ("store.css", "store.css"),
    ("store.js", "store.js"),
    ("icon.svg", "icon.svg"),
    ("README.md", "README.md"),
    ("../LICENSE", "LICENSE"),
)

with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for source, archive_name in FILES:
        path = ROOT / source
        if not path.is_file():
            raise SystemExit(f"Missing plugin asset: {path}")
        info = ZipInfo(archive_name, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)

print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
