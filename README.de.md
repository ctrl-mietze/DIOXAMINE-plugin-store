# DIOXAMINE Plugin Store

**Ein Community-Katalog für DIOXAMINE-Plugins.**

[English](README.md) · [Plugin einreichen](docs/plugin-submission.md) · [Plugin-Format](docs/plugin-format.md)

[![Katalogprüfung](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml/badge.svg)](https://github.com/ctrl-mietze/DIOXAMINE-plugin-store/actions/workflows/validate-catalogue.yml) [![MIT-Lizenz](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Beiträge willkommen](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

Dieses Repository ist der öffentliche Katalog und Paket-Speicher der DIOXAMINE-Community. Plugins, Metadaten und Dokumentation liegen direkt hier. Das In-App-Plugin **DIOXAMINE Plugin Store** liest den Katalog direkt von GitHub. Es gibt keine separate gehostete Website und kein separates Backend.

## Plugins entdecken

Die maschinenlesbare Übersicht steht in [`catalogue/plugins.json`](catalogue/plugins.json). Die [`plugins/`](plugins/) enthält die Paketdateien. **Aktuell sind noch keine Community-Plugins gelistet.** Der Katalog bleibt leer, bis echte Plugins geprüft und aufgenommen wurden.

Plugin-Pakete liegen in diesem Repository und werden direkt von GitHub geladen. GitHub Releases werden dafür nicht verwendet.

## Store in DIOXAMINE verwenden

Quellcode und aktuelles Paket des Store-Plugins befinden sich in [`store-plugin/`](store-plugin/). Lade auf Android [`store-plugin/plugin.zip`](store-plugin/plugin.zip) herunter und öffne es mit einer kompatiblen DIOXAMINE-Version. Das Store-Plugin liest anschließend die Katalogdaten aus diesem Repository.

DIOXAMINEs vorhandenes Plugin-Repository und der ZIP-Installer bleiben für Prüfung und Installation zuständig. Das Store-Plugin baut keinen parallelen Installer.

## Plugin einreichen

Jeder darf ein kompatibles DIOXAMINE-Plugin entwickeln und zur Aufnahme in diesen Community Plugin Store einreichen. Forke dieses Repository, folge der [Einreichungsanleitung](docs/plugin-submission.md) und dem [Plugin-Format](docs/plugin-format.md) und erstelle einen Pull Request. Automatische Prüfungen kontrollieren Katalog und Paket; Verantwortliche prüfen Einreichungen vor dem Merge.

Eine Community-Prüfung ist weder ein Sicherheitsaudit noch eine Sicherheitsgarantie. Prüfe Quelle, Lizenz, Kompatibilität und angeforderte Berechtigungen eines Plugins vor der Installation.

## Repository-Aufbau

```text
catalogue/                 Öffentlicher Katalog und Schema
plugins/<plugin-id>/       Geprüfte Plugin-Metadaten, ZIP-Pakete und Dateien
store-plugin/              In-App-Store-Plugin und ZIP-Paketierung
docs/                      Anleitung zur Einreichung und Plugin-Format
scripts/                   Katalogprüfung und Paketwerkzeuge
.github/workflows/         Automatische Katalog- und Paketprüfungen
```

## Lokal prüfen

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_catalogue.py
python3 store-plugin/package.py
```

Der Validator prüft Pflichtangaben, eindeutige Plugin-IDs, Paketpfade, Manifest-Abgleich, ZIP-Sicherheit und SHA-256-Prüfsummen. GitHub Actions führt diese Prüfungen bei Pull Requests und Pushes auf `main` aus.

## Lizenz

Repository-Werkzeuge und Store-Plugin-Quellcode: [MIT](LICENSE). Für eingereichte Plugins gilt die Lizenz, die der jeweilige Autor angibt.
