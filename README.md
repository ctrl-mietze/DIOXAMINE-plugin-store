# DIOXAMINE Plugin Store

**A community-built plugin catalogue for DIOXAMINE.**

[Deutsch](README.de.md) · [Submit a plugin](docs/plugin-submission.md) · [Plugin format](docs/plugin-format.md)

[![Catalogue validation](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml/badge.svg)](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml) [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

This repository is the public catalogue and package source for the DIOXAMINE community. Plugins live here, alongside their metadata and documentation. The in-app **DIOXAMINE Plugin Store** plugin reads the catalogue directly from GitHub. There is no separate hosted website or backend.

## Browse plugins

Open [`catalogue/plugins.json`](catalogue/plugins.json) to see the machine-readable catalogue, or browse the [`plugins/`](plugins/) directory for package contents. **There are currently no community plugins listed.** The catalogue is intentionally empty until a real plugin has been reviewed and accepted.

Plugin packages are stored in this repository and downloaded directly from GitHub. They are not distributed through GitHub Releases.

## Use the in-app Store

The Store plugin source and current package are in [`store-plugin/`](store-plugin/). On Android, download [`store-plugin/plugin.zip`](store-plugin/plugin.zip) and open it with a compatible DIOXAMINE build. The Store plugin fetches catalogue metadata from this repository.

DIOXAMINE's existing plugin repository and ZIP installer remain responsible for validating and installing plugin archives. The Store plugin does not create a parallel installer.

## Submit a plugin

Anyone may develop a compatible DIOXAMINE plugin and submit it for inclusion in this Community Plugin Store. Fork this repository, follow the [submission guide](docs/plugin-submission.md) and [plugin format](docs/plugin-format.md), then open a pull request. Automated checks validate the catalogue and package; maintainers review submissions before merging.

Community review is not a security audit or a safety guarantee. Check each plugin's source, license, compatibility, and requested permissions before installing it.

## Repository layout

```text
catalogue/                 Public machine-readable catalogue and schema
plugins/<plugin-id>/       Reviewed plugin metadata, ZIP packages, and assets
store-plugin/              In-app Store plugin source and ZIP packager
docs/                      Plugin format and submission guides
scripts/                   Catalogue validation and package tooling
.github/workflows/         Automated catalogue and package checks
```

## Validate locally

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_catalogue.py
python3 store-plugin/package.py
```

The validator checks required metadata, unique plugin IDs, package paths, manifest agreement, ZIP safety, and SHA-256 hashes. GitHub Actions runs these checks for pull requests and pushes to `main`.

## License

Repository tooling and Store plugin source: [MIT](LICENSE). Each submitted plugin keeps the license declared by its author.
