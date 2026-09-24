#!/usr/bin/env python3
"""Validate the public catalogue and every referenced current-format DIOXAMINE ZIP."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "catalogue/plugins.json"
ID_RE = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9_]+)+$")
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
MAX_ARCHIVE = 500 * 1024 * 1024
MAX_ENTRIES = 5000
MAX_EXPANDED = 500 * 1024 * 1024
ALLOWED_PERMISSIONS = {
    "adb": {"shell", "push", "pull", "install", "forward", "reverse"},
    "common": {"network", "internet"},
    "fastboot": {"fastboot", "access"},
}
errors: list[str] = []


def fail(where: str, message: str) -> None:
    errors.append(f"{where}: {message}")


def require(condition: bool, where: str, message: str) -> None:
    if not condition:
        fail(where, message)


def safe_repo_path(value: object, where: str) -> Path | None:
    if not isinstance(value, str) or not value:
        fail(where, "path must be a non-empty string")
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        fail(where, f"unsafe repository path: {value!r}")
        return None
    resolved = (ROOT / Path(*path.parts)).resolve()
    if ROOT.resolve() not in resolved.parents:
        fail(where, f"path escapes repository: {value!r}")
        return None
    return resolved


def valid_localized(value: object, where: str) -> None:
    require(isinstance(value, dict), where, "must be a localized object with en and de strings")
    if isinstance(value, dict):
        for locale in ("en", "de"):
            require(isinstance(value.get(locale), str) and bool(value[locale].strip()), where, f"missing non-empty {locale!r} text")


def valid_timestamp(value: object, where: str) -> None:
    require(isinstance(value, str), where, "must be an ISO-8601 timestamp")
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            require(parsed.utcoffset() is not None, where, "timestamp must include a timezone")
        except ValueError:
            fail(where, "must be an ISO-8601 timestamp with a timezone")


def validate_archive(entry: dict, where: str) -> None:
    plugin_id = entry.get("id")
    if not isinstance(plugin_id, str) or not ID_RE.fullmatch(plugin_id):
        return
    archive_path = safe_repo_path(entry.get("package"), f"{where}.package")
    if archive_path is None:
        return
    require(archive_path.is_file() and not archive_path.is_symlink(), f"{where}.package", "archive is missing or is a symlink")
    if not archive_path.is_file() or archive_path.is_symlink():
        return
    size = archive_path.stat().st_size
    require(0 < size <= MAX_ARCHIVE, f"{where}.package", f"archive size must be between 1 byte and {MAX_ARCHIVE} bytes")
    hasher = hashlib.sha256()
    with archive_path.open("rb") as package_stream:
        for chunk in iter(lambda: package_stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    digest = hasher.hexdigest()
    require(entry.get("sha256") == digest, f"{where}.sha256", f"digest mismatch; expected {digest}")
    plugin_dir = ROOT / "plugins" / plugin_id
    manifest_sidecar = plugin_dir / "plugin.json"
    require(manifest_sidecar.is_file() and not manifest_sidecar.is_symlink(), f"plugins/{entry.get('id')}/plugin.json", "sidecar manifest is required and cannot be a symlink")
    if manifest_sidecar.is_symlink():
        return
    try:
        sidecar = json.loads(manifest_sidecar.read_text(encoding="utf-8")) if manifest_sidecar.is_file() else None
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"plugins/{entry.get('id')}/plugin.json", f"cannot parse manifest: {exc}")
        sidecar = None
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            require(0 < len(infos) <= MAX_ENTRIES, f"{where}.package", f"entry count must be 1–{MAX_ENTRIES}")
            names: set[str] = set()
            expanded = 0
            for info in infos:
                name = info.filename
                posix = PurePosixPath(name)
                require(not posix.is_absolute() and ".." not in posix.parts and "\\" not in name, f"{where}.package", f"unsafe ZIP path {name!r}")
                require(name not in names, f"{where}.package", f"duplicate ZIP entry {name!r}")
                names.add(name)
                expanded += info.file_size
                require(info.file_size >= 0, f"{where}.package", f"invalid expanded size for {name!r}")
                require(info.file_size <= MAX_EXPANDED, f"{where}.package", f"entry is oversized: {name!r}")
                unix_mode = (info.external_attr >> 16) & 0xFFFF
                require((unix_mode & 0o170000) != 0o120000, f"{where}.package", f"symbolic link is not allowed: {name!r}")
            require(expanded <= MAX_EXPANDED, f"{where}.package", "expanded archive exceeds size limit")
            require("plugin.json" in names, f"{where}.package", "plugin.json must be at the ZIP root")
            if "plugin.json" in names:
                try:
                    manifest = json.loads(archive.read("plugin.json"))
                except (KeyError, json.JSONDecodeError, UnicodeDecodeError, RuntimeError) as exc:
                    fail(f"{where}.package", f"invalid root plugin.json: {exc}")
                    manifest = None
            else:
                manifest = None
            if isinstance(manifest, dict):
                validate_manifest(manifest, where)
                require(sidecar == manifest, f"{where}.package", "ZIP plugin.json differs from sidecar plugin.json")
                entry_file = manifest.get("entry")
                require(isinstance(entry_file, str) and entry_file in names, f"{where}.package", "manifest entry file is absent from ZIP root")
                require(manifest.get("id") == entry.get("id"), f"{where}.id", "catalogue ID does not match plugin manifest ID")
                require(manifest.get("version") == entry.get("version"), f"{where}.version", "catalogue version does not match plugin manifest")
                require(manifest.get("versionCode") == entry.get("versionCode"), f"{where}.versionCode", "catalogue versionCode does not match plugin manifest")
                require(manifest.get("permissions", {}) == entry.get("permissions"), f"{where}.permissions", "catalogue permissions do not match plugin manifest")
                compatibility = entry.get("compatibility")
                if isinstance(compatibility, dict) and compatibility.get("minVersionCode") is not None:
                    require(compatibility["minVersionCode"] == manifest.get("minAppVersionCode", 1), f"{where}.compatibility.minVersionCode", "does not match current plugin manifest")
                icon = manifest.get("icon")
                if icon:
                    require(icon in names, f"{where}.manifest.icon", "manifest icon file is absent from ZIP")
            try:
                bad = archive.testzip()
                require(bad is None, f"{where}.package", f"CRC check failed for {bad}")
            except RuntimeError as exc:
                fail(f"{where}.package", f"encrypted/unsupported ZIP entry: {exc}")
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        fail(f"{where}.package", f"not a readable ZIP archive: {exc}")
        return
    readme = plugin_dir / "README.md"
    require(readme.is_file() and not readme.is_symlink(), f"plugins/{entry.get('id')}/README.md", "plugin README is required and cannot be a symlink")


def validate_manifest(manifest: dict, where: str) -> None:
    required = ("schemaVersion", "id", "name", "version", "versionCode", "entry")
    for field in required:
        require(field in manifest, f"{where}.manifest", f"missing required field {field!r}")
    require(manifest.get("schemaVersion") == 1, f"{where}.manifest.schemaVersion", "only current schemaVersion 1 is supported")
    require(isinstance(manifest.get("id"), str) and bool(ID_RE.fullmatch(manifest["id"])), f"{where}.manifest.id", "must use the current lowercase reverse-DNS ID format")
    require(isinstance(manifest.get("name"), str) and 0 < len(manifest["name"]) <= 100, f"{where}.manifest.name", "must be 1–100 characters")
    require(isinstance(manifest.get("version"), str) and bool(VERSION_RE.fullmatch(manifest["version"])), f"{where}.manifest.version", "must use semantic major.minor.patch format")
    require(isinstance(manifest.get("versionCode"), int) and manifest["versionCode"] > 0, f"{where}.manifest.versionCode", "must be a positive integer")
    permissions = manifest.get("permissions", {})
    require(isinstance(permissions, dict), f"{where}.manifest.permissions", "must be the current object format, not a legacy flat list")
    if isinstance(permissions, dict):
        for group, values in permissions.items():
            require(group in ALLOWED_PERMISSIONS, f"{where}.manifest.permissions", f"unknown permission group {group!r}")
            require(isinstance(values, list), f"{where}.manifest.permissions.{group}", "must be an array")
            if isinstance(values, list) and group in ALLOWED_PERMISSIONS:
                for permission in values:
                    require(isinstance(permission, str) and permission in ALLOWED_PERMISSIONS[group], f"{where}.manifest.permissions.{group}", f"unsupported permission {permission!r}")
    entry = manifest.get("entry")
    require(isinstance(entry, str) and bool(entry) and ".." not in entry and not entry.startswith(("/", "\\")), f"{where}.manifest.entry", "must be a safe relative path")
    icon = manifest.get("icon")
    if icon is not None:
        require(isinstance(icon, str) and bool(icon) and ".." not in icon and not icon.startswith(("/", "\\")), f"{where}.manifest.icon", "must be a safe relative path")


def main() -> int:
    try:
        data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR catalogue/plugins.json: {exc}", file=sys.stderr)
        return 1
    require(isinstance(data, dict), "catalogue", "root must be an object")
    if not isinstance(data, dict):
        return 1
    require(data.get("schemaVersion") == 1, "catalogue.schemaVersion", "must be 1")
    require(isinstance(data.get("catalogueVersion"), int) and data["catalogueVersion"] >= 1, "catalogue.catalogueVersion", "must be a positive integer")
    valid_timestamp(data.get("updatedAt"), "catalogue.updatedAt")
    plugins = data.get("plugins")
    require(isinstance(plugins, list), "catalogue.plugins", "must be an array")
    if not isinstance(plugins, list):
        plugins = []
    ids: set[str] = set()
    for index, entry in enumerate(plugins):
        where = f"plugins[{index}]"
        if not isinstance(entry, dict):
            fail(where, "must be an object")
            continue
        plugin_id = entry.get("id")
        require(isinstance(plugin_id, str) and bool(ID_RE.fullmatch(plugin_id)), f"{where}.id", "must use lowercase reverse-DNS format")
        if isinstance(plugin_id, str):
            require(plugin_id not in ids, f"{where}.id", f"duplicate plugin ID {plugin_id!r}")
            ids.add(plugin_id)
        valid_localized(entry.get("name"), f"{where}.name")
        valid_localized(entry.get("description"), f"{where}.description")
        require(isinstance(entry.get("author"), str) and bool(entry["author"].strip()), f"{where}.author", "must be a non-empty string")
        require(isinstance(entry.get("version"), str) and bool(VERSION_RE.fullmatch(entry["version"])), f"{where}.version", "must use semantic major.minor.patch format")
        require(isinstance(entry.get("versionCode"), int) and entry["versionCode"] > 0, f"{where}.versionCode", "must be a positive integer")
        require(isinstance(entry.get("category"), str) and bool(entry["category"].strip()), f"{where}.category", "must be a non-empty string")
        require(isinstance(entry.get("source"), str) and entry["source"].startswith("https://"), f"{where}.source", "must be an HTTPS source URL")
        require(isinstance(entry.get("license"), str) and bool(entry["license"].strip()), f"{where}.license", "must name the plugin license")
        require(isinstance(entry.get("permissions"), dict), f"{where}.permissions", "must be an object")
        require(isinstance(entry.get("compatibility"), dict), f"{where}.compatibility", "must be an object")
        valid_timestamp(entry.get("updatedAt"), f"{where}.updatedAt")
        package = entry.get("package")
        require(package == f"plugins/{plugin_id}/plugin.zip", f"{where}.package", "must be plugins/<plugin-id>/plugin.zip")
        expected_icon = entry.get("icon")
        if expected_icon:
            icon_path = safe_repo_path(expected_icon, f"{where}.icon")
            if icon_path:
                require(icon_path.is_file(), f"{where}.icon", "file does not exist")
        shots = entry.get("screenshots", [])
        require(isinstance(shots, list), f"{where}.screenshots", "must be an array")
        if isinstance(shots, list):
            for shot_index, shot in enumerate(shots):
                shot_path = safe_repo_path(shot, f"{where}.screenshots[{shot_index}]")
                if shot_path:
                    require(shot_path.is_file(), f"{where}.screenshots[{shot_index}]", "file does not exist")
        validate_archive(entry, where)
    expected_dirs = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir() and not p.is_symlink() and (p / "plugin.json").exists()}
    require(expected_dirs == ids, "plugins", f"plugin directories and catalogue IDs differ (unlisted={sorted(expected_dirs-ids)}, missing_dirs={sorted(ids-expected_dirs)})")
    if errors:
        for message in errors:
            print(f"ERROR {message}", file=sys.stderr)
        print(f"Catalogue validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Catalogue valid: {len(plugins)} plugin(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
