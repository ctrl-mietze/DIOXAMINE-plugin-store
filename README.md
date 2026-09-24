# DIOXAMINE Plugin Store

**Community-built plugins for DIOXAMINE.**

| [Get Plugins](https://ctrl-mietze.github.io/DIOXAMINE-plugin-store/plugins/) | [Submit a plugin](CONTRIBUTING.md) | [Deutsch](README.de.md) |
| --- | --- | --- |

[![Catalogue validation](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml/badge.svg)](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml) [![GitHub Pages](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/pages.yml/badge.svg)](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/pages.yml) ![MIT License](https://img.shields.io/badge/license-MIT-527db7) ![Community project](https://img.shields.io/badge/community-built-74a891)

The DIOXAMINE Plugin Store is a community-built catalogue and discovery site. Plugin packages live in this repository and are served directly from GitHub. It is an independent project maintained by the DIOXAMINE community.

## Project status

The catalogue and website are being established. **There are currently no community plugins listed.** The repository includes the catalogue format, automated checks, a bilingual discovery site, and the source for an in-app Store plugin.

## For users

Browse the [Get Plugins catalogue](https://ctrl-mietze.github.io/DIOXAMINE-plugin-store/plugins/). The site and the in-app Store read `catalogue/plugins.json` from this public repository. Plugin archives are stored under `plugins/<plugin-id>/` and downloaded directly from GitHub; distribution does not use GitHub Releases.

The Store plugin is built for DIOXAMINE's current ZIP plugin format (`plugin.json` at the archive root). DIOXAMINE remains responsible for validating and installing a package through its existing plugin installer. The supplied app-side **Open with DIOXAMINE** integration routes ZIP imports to `pluginRepo.install(uri)`; if it is not present in your app build, use **Plugins → Install Plugin** and select the downloaded ZIP.

Install the in-app catalogue from [the Store plugin ZIP](store-plugin/plugin.zip): download it on Android and open the ZIP with DIOXAMINE.

## Publish the website

The Pages workflow builds and deploys the site on pushes to `main`. If Pages has not been enabled for this repository yet, set **Settings → Pages → Build and deployment → Source → GitHub Actions** once; subsequent deployments run automatically.

## For developers

Anyone may develop a compatible DIOXAMINE plugin and submit it for inclusion in this Community Plugin Store. Start with [plugin submission](docs/plugin-submission.md), then review the [package format](docs/plugin-format.md). Submissions are reviewed; inclusion does not guarantee that a plugin is safe or endorsed. Review source code and requested permissions before installing.

## Repository map

```text
catalogue/                 Public, versioned machine-readable index
plugins/<plugin-id>/       Plugin metadata, ZIP package, source notes, assets
store-plugin/              DIOXAMINE Store plugin source and packager
site/                      GitHub Pages discovery website (English + German)
docs/                      Contributor and format documentation
scripts/                   Local validation and package tooling
.github/workflows/         Catalogue validation and Pages deployment
```

## Work locally

```bash
python3 scripts/validate_catalogue.py
python3 store-plugin/package.py
```

The validator checks metadata, package paths, manifest agreement, ZIP safety, archive hashes, and duplicate identifiers. GitHub Actions runs it for pull requests and pushes.

## Links

- [Get Plugins](https://ctrl-mietze.github.io/DIOXAMINE-plugin-store/plugins/)
- [Plugin submission guide](docs/plugin-submission.md)
- [Plugin package format](docs/plugin-format.md)
- [Contributing](CONTRIBUTING.md)
- [Repository](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store)

## License

Repository tooling and website: [MIT](LICENSE). Plugin packages retain the license declared by each plugin author.
