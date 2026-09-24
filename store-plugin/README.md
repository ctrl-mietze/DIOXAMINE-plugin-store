# DIOXAMINE Plugin Store plugin

This plugin is built on DIOXAMINE's current plugin base and ZIP manifest contract. Its `plugin.json`, entry point, icon, and permission declaration follow the current DIOXAMINE plugin structure and [plugin quickstart](https://github.com/ctrl-mietze/Dioxamine/blob/main/docs/src/plugins/quickstart.md). It uses the current network bridge and relies on DIOXAMINE's existing installer to validate and import its ZIP package; it does not add a second plugin manager.

## Build

From the repository root:

```bash
python3 store-plugin/package.py
```

The script creates `store-plugin/plugin.zip`. Select/open the ZIP with a DIOXAMINE build that supports the current native ZIP import flow. The imported plugin then reads the catalogue from the public GitHub repository.

## Installation boundary

The current in-app plugin bridge exposes text HTTP requests and user-confirmed URL opening, but no binary-to-content-URI download or embedded `pluginRepo.install(uri)` call. The Store provides a direct GitHub package link and explains the Android open-with handoff. If the app build does not include the supplied ZIP `ACTION_VIEW` integration, use DIOXAMINE's existing plugin file picker. DIOXAMINE remains the sole installer and validator. See [`../docs/plugin-format.md`](../docs/plugin-format.md).
