"""Regression tests for catalogue metadata and plugin archive validation."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZIP_DEFLATED, ZipFile


SOURCE_VALIDATOR = Path(__file__).resolve().parents[1] / "scripts/validate_catalogue.py"


class CatalogueValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "fixture"
        (self.root / "catalogue").mkdir(parents=True)
        (self.root / "scripts").mkdir()
        (self.root / "plugins/dev.example.sample").mkdir(parents=True)
        shutil.copy2(SOURCE_VALIDATOR, self.root / "scripts/validate_catalogue.py")
        self.manifest = {
            "schemaVersion": 1,
            "id": "dev.example.sample",
            "name": "Sample",
            "description": "Fixture plugin",
            "version": "1.0.0",
            "versionCode": 1,
            "author": "Fixture",
            "entry": "index.html",
            "icon": "icon.svg",
            "minAppVersionCode": 1,
            "permissions": {"common": []},
        }
        self.plugin_dir = self.root / "plugins/dev.example.sample"
        (self.plugin_dir / "plugin.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        (self.plugin_dir / "README.md").write_text("Test fixture only.\n", encoding="utf-8")
        self.write_zip()
        self.entry = {
            "id": self.manifest["id"],
            "name": {"en": "Sample", "de": "Beispiel"},
            "description": {"en": "Test fixture", "de": "Testbeispiel"},
            "author": "Fixture",
            "version": "1.0.0",
            "versionCode": 1,
            "category": "Tools",
            "package": "plugins/dev.example.sample/plugin.zip",
            "sha256": self.digest(),
            "source": "https://github.com/example/sample",
            "license": "MIT",
            "permissions": self.manifest["permissions"],
            "compatibility": {"minVersionCode": 1},
            "updatedAt": "2026-09-24T00:00:00Z",
        }
        self.write_catalogue()

    def tearDown(self):
        self.temp.cleanup()

    def write_zip(self, extra=()):
        with ZipFile(self.plugin_dir / "plugin.zip", "w", ZIP_DEFLATED) as archive:
            archive.writestr("plugin.json", json.dumps(self.manifest))
            archive.writestr("index.html", "<h1>Fixture</h1>")
            archive.writestr("icon.svg", "<svg xmlns='http://www.w3.org/2000/svg'/>")
            for name, content in extra:
                archive.writestr(name, content)

    def digest(self):
        return hashlib.sha256((self.plugin_dir / "plugin.zip").read_bytes()).hexdigest()

    def write_catalogue(self):
        data = {
            "schemaVersion": 1,
            "catalogueVersion": 1,
            "updatedAt": "2026-09-24T00:00:00Z",
            "plugins": [self.entry],
        }
        (self.root / "catalogue/plugins.json").write_text(json.dumps(data), encoding="utf-8")

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/validate_catalogue.py")],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_current_format_plugin_passes(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 plugin(s)", result.stdout)

    def test_zip_path_traversal_fails_even_when_hash_matches(self):
        self.write_zip(extra=[("../escape.txt", "no")])
        self.entry["sha256"] = self.digest()
        self.write_catalogue()
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe ZIP path", result.stderr)

    def test_package_hash_mismatch_fails(self):
        with ZipFile(self.plugin_dir / "plugin.zip", "a", ZIP_DEFLATED) as archive:
            archive.writestr("extra.txt", "changed after catalogue hash")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("digest mismatch", result.stderr)

    def test_legacy_flat_permissions_fail(self):
        self.manifest["permissions"] = ["network"]
        (self.plugin_dir / "plugin.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        self.write_zip()
        self.entry["permissions"] = self.manifest["permissions"]
        self.entry["sha256"] = self.digest()
        self.write_catalogue()
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("current object format", result.stderr)


if __name__ == "__main__":
    unittest.main()
