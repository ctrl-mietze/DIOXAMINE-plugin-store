# DIOXAMINE Plugin Store

**Community-Plugins für DIOXAMINE.**

| [Plugins entdecken](https://ctrl-mietze.github.io/DIOXAMINE-plugin-store/plugins/) | [Plugin einreichen](CONTRIBUTING.md) | [English](README.md) |
| --- | --- | --- |

[![Katalogprüfung](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml/badge.svg)](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml) [![GitHub Pages](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/pages.yml/badge.svg)](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/pages.yml) ![MIT-Lizenz](https://img.shields.io/badge/license-MIT-527db7) ![Community-Projekt](https://img.shields.io/badge/community-built-74a891)

Der DIOXAMINE Plugin Store ist ein Community-Katalog mit einer öffentlichen Entdeckungsseite. Plugin-Pakete liegen direkt in diesem Repository und werden über GitHub bereitgestellt. Das unabhängige Projekt wird von der DIOXAMINE-Community gepflegt.

## Projektstatus

Katalog und Website werden gerade aufgebaut. **Aktuell sind noch keine Community-Plugins gelistet.** Dieses Repository enthält bereits das Katalogformat, automatische Prüfungen, eine zweisprachige Website sowie den Quellcode für ein Store-Plugin in DIOXAMINE.

## Für Nutzer

Durchsuche den [Plugin-Katalog](https://ctrl-mietze.github.io/DIOXAMINE-plugin-store/plugins/). Website und Store-Plugin lesen `catalogue/plugins.json` aus diesem öffentlichen Repository. Plugin-Archive liegen unter `plugins/<plugin-id>/` und werden direkt von GitHub geladen; GitHub Releases werden nicht verwendet.

Das Store-Plugin nutzt DIOXAMINEs aktuelles ZIP-Pluginformat (`plugin.json` im Archiv-Stammverzeichnis). DIOXAMINE bleibt für Validierung und Installation über den vorhandenen Plugin-Installer zuständig. Die mitgelieferte Integration **Mit DIOXAMINE öffnen** leitet ZIP-Importe an `pluginRepo.install(uri)` weiter. Falls sie in deiner App-Version noch fehlt, wähle **Plugins → Install Plugin** und dann die heruntergeladene ZIP-Datei.

Installiere den In-App-Katalog über das [Store-Plugin-ZIP](store-plugin/plugin.zip): Lade es auf Android herunter und öffne die ZIP-Datei mit DIOXAMINE.

## Website veröffentlichen

Der Pages-Workflow baut und veröffentlicht die Website bei Pushes auf `main`. Falls Pages für dieses Repository noch nicht aktiviert ist, stelle einmalig **Settings → Pages → Build and deployment → Source → GitHub Actions** ein. Danach laufen Veröffentlichungen automatisch.

## Für Entwickler

Jeder darf ein kompatibles DIOXAMINE-Plugin entwickeln und zur Aufnahme in diesen Community Plugin Store einreichen. Lies zuerst die [Einreichungsanleitung](docs/plugin-submission.md) und danach das [Paketformat](docs/plugin-format.md). Einreichungen werden geprüft. Die Aufnahme garantiert weder Sicherheit noch eine Empfehlung. Prüfe Quellcode und angeforderte Berechtigungen, bevor du ein Plugin installierst.

## Repository-Aufbau

```text
catalogue/                 Öffentlicher maschinenlesbarer Katalog
plugins/<plugin-id>/       Metadaten, ZIP-Paket, Hinweise und Assets
store-plugin/              DIOXAMINE-Store-Plugin und Paketierung
site/                      GitHub-Pages-Website (Deutsch + Englisch)
docs/                      Dokumentation für Entwickler und Paketformat
scripts/                   Lokale Prüf- und Paketierungswerkzeuge
.github/workflows/         Katalogprüfung und Pages-Veröffentlichung
```

## Lokal arbeiten

```bash
python3 scripts/validate_catalogue.py
python3 store-plugin/package.py
```

Die Prüfung kontrolliert Metadaten, Paketpfade, Manifest-Abgleich, ZIP-Sicherheit, SHA-256-Prüfsummen und doppelte Kennungen. GitHub Actions führt sie für Pull Requests und Pushes aus.

## Links

- [Plugins entdecken](https://ctrl-mietze.github.io/DIOXAMINE-plugin-store/plugins/)
- [Plugin einreichen](docs/plugin-submission.md)
- [Paketformat](docs/plugin-format.md)
- [Mitwirken](CONTRIBUTING.md)
- [Repository](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store)

## Lizenz

Repository-Werkzeuge und Website: [MIT](LICENSE). Für Plugin-Pakete gilt die Lizenz, die der jeweilige Autor angibt.
