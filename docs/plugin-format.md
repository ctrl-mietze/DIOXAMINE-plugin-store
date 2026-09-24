# Plugin package format

The Store targets DIOXAMINE's current plugin installer format. The archive is a ZIP with the current `plugin.json` manifest at the archive root; the installer validates and extracts it. The Store does not install packages itself and does not introduce a parallel plugin manager.

## Package layout

```text
plugin.zip
├── plugin.json
├── index.html
├── styles.css
├── app.js
└── icon.png
```

The manifest must match the current DIOXAMINE schema. A typical manifest includes `schemaVersion: 1`, a reverse-DNS `id`, `name`, `version`, positive `versionCode`, `entry`, and a `permissions` object. For example:

```json
{
  "schemaVersion": 1,
  "id": "dev.example.deviceinfo",
  "name": "Device Info",
  "description": "Displays device information",
  "version": "1.0.0",
  "versionCode": 1,
  "author": "Example Developer",
  "entry": "index.html",
  "icon": "icon.png",
  "minAppVersionCode": 1,
  "permissions": { "common": [] },
  "fullscreen": false,
  "homepage": "https://github.com/example/device-info"
}
```

Use the current DIOXAMINE [manifest specification](https://github.com/ctrl-mietze/Dioxamine/blob/main/docs/src/plugins/manifest.md) and [plugin API reference](https://github.com/ctrl-mietze/Dioxamine/tree/main/docs/src/plugins/api) as authoritative references. The installer validates the manifest, supported permissions, paths, archive bounds, and entry file. The Store's validator performs additional catalogue checks; it is not a replacement for DIOXAMINE validation.

## Catalogue metadata

`catalogue/plugins.json` is a versioned JSON document. Each entry carries a stable `id`, localized name and description, author, semantic version and integer version code, category, repository-relative `package`, SHA-256 digest, compatibility requirements, permissions, source URL, update timestamp, and optional artwork/changelog. Unknown future fields are allowed by clients. Paths must stay within this repository.

## Installation boundary

The current public plugin bridge exposes `dioxamine.http.fetch()` for text HTTP responses and `dioxamine.openUrl()` for user-confirmed external links. It does not expose a native binary download-to-URI or plugin-install bridge to embedded plugins. Therefore the Store plugin does not pretend to call the app-internal `pluginRepo.install(uri)` API. Its compatible fallback opens the package URL; Android/DIOXAMINE's ZIP import then hands the selected archive to the existing installer. A future host API can remove this handoff step while still delegating installation to the same `pluginRepo.install(uri)` workflow.

The supplied Android import change is an app-side integration reference, not part of a plugin ZIP: it registers ZIP MIME types and routes incoming `ACTION_VIEW` URIs through the existing installer. It must be included in the DIOXAMINE app build for Android's **Open with DIOXAMINE** action; without it, users can still install the downloaded ZIP through DIOXAMINE's existing plugin file picker.
