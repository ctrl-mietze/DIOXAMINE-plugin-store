import json, zipfile, hashlib, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
cat = json.loads((root/"catalogue/plugins.json").read_text(encoding="utf-8"))
allowed = {
    "adb": {"shell","push","pull","install","forward","reverse"},
    "common": {"network","internet"},
    "fastboot": {"fastboot","access"},
}
errors = []
for p in cat["plugins"]:
    z = root / p["package"]
    if not z.exists():
        errors.append(p["id"] + ": package missing")
        continue
    if hashlib.sha256(z.read_bytes()).hexdigest() != p["sha256"]:
        errors.append(p["id"] + ": sha mismatch")
    with zipfile.ZipFile(z) as f:
        if "plugin.json" not in f.namelist():
            errors.append(p["id"] + ": plugin.json not at ZIP root")
            continue
        m = json.loads(f.read("plugin.json"))
        if m.get("id") != p["id"]:
            errors.append(p["id"] + ": manifest id mismatch")
        for group, values in m.get("permissions", {}).items():
            if group not in allowed or any(v not in allowed.get(group, set()) for v in values):
                errors.append(p["id"] + ": invalid permission")
print(f"plugins={len(cat['plugins'])} errors={len(errors)}")
for e in errors:
    print(e)
sys.exit(1 if errors else 0)
