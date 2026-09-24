# DIOXAMINE Plugin Store plugin

This is a purpose-built plugin for DIOXAMINE's current ZIP plugin system. It is not copied from a legacy plugin base. The plugin uses the current manifest shape and network permission, and relies on DIOXAMINE's existing installer to import its ZIP package.

## Build

From the repository root:

```bash
python3 store-plugin/package.py
```

The script creates `store-plugin/plugin.zip`. Select/open the ZIP with a DIOXAMINE build that supports the current native ZIP import flow. The imported plugin then reads the catalogue from the public GitHub repository.

## Installation boundary

The current in-app plugin bridge exposes text HTTP requests and user-confirmed URL opening, but no binary-to-content-URI download or embedded `pluginRepo.install(uri)` call. The Store provides a direct GitHub package link and explains the Android open-with handoff. If the app build does not include the supplied ZIP `ACTION_VIEW` integration, use DIOXAMINE's existing plugin file picker. DIOXAMINE remains the sole installer and validator. See [`../docs/plugin-format.md`](../docs/plugin-format.md).
