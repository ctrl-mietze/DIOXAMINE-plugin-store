# Plugin submission

Anyone may develop a compatible DIOXAMINE plugin and submit it for inclusion in the Community Plugin Store.

## Prepare the package

- Use DIOXAMINE's current ZIP plugin format. Do not use legacy manifests or a legacy plugin base.
- Put `plugin.json` at the ZIP root and ensure its `id` matches the catalogue ID.
- Include all runtime assets referenced by the manifest's `entry` and `icon` fields.
- Declare only permissions that the plugin needs. Explain network access and other sensitive behavior in the README.
- Provide source code, a license, and a clear description of what the plugin does.
- Test installation and use on a current DIOXAMINE build.

## Add it to this repository

```text
plugins/<reverse-dns-id>/
├── plugin.zip
├── plugin.json
├── README.md
├── icon.png                 (optional)
└── screenshots/             (optional)
```

Add a matching entry to `catalogue/plugins.json`. Use repository-relative paths and calculate the ZIP digest with:

```bash
sha256sum plugins/<id>/plugin.zip
```

Then validate and submit a pull request:

```bash
python3 scripts/validate_catalogue.py
```

The pull request should identify the author, source repository, plugin license, compatibility, declared permissions, and any material limitations. Do not upload a plugin through GitHub Releases; package files belong in the repository tree.

## Review and trust

Maintainers check the manifest, catalogue fields, archive structure, hash, and submitted source information. Review reduces catalogue errors but is not a full security audit. A catalogue listing is not an endorsement or safety certification. Users should inspect source, developer identity, requested permissions, and updates before installation. Maintainers may remove or decline a listing.
