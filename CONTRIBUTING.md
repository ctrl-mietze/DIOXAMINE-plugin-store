# Contributing

This is a community project for discovering plugins that use DIOXAMINE's current plugin format. Contributions are welcome through GitHub pull requests.

## Submit a plugin

1. Build and test the plugin with DIOXAMINE's current ZIP installer. The archive must contain `plugin.json` at its root.
2. Read [`docs/plugin-format.md`](docs/plugin-format.md) and [`docs/plugin-submission.md`](docs/plugin-submission.md).
3. Fork this repository and add the package directory under `plugins/<plugin-id>/`.
4. Add its metadata to `catalogue/plugins.json`, including the archive SHA-256.
5. Run `python3 scripts/validate_catalogue.py` and open a pull request using the template.

Each submission is reviewed for format, metadata, source availability, and obvious risks. Review is not a security audit or a guarantee of safety. Do not include secrets, private signing keys, or personal data.

## Change the site or tooling

Keep the site dependency-free where practical, preserve English and German strings, and test at mobile and desktop widths. Run the catalogue validator after changing the schema or sample data. Changes to the native Store plugin must retain compatibility with the current manifest and archive format.

## Review and acceptance

Only maintainers can add entries to the shared catalogue by merging a pull request. Submitting a plugin does not automatically publish it. Maintainers may request changes or decline submissions that are incomplete, misleading, incompatible, or unsafe to distribute.
