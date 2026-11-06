# Vendoring

Cratekit ships one component it did not write: the acquisition downloader,
upstream `tidal-dl-ng` 0.33.0, as a source tree under
`src/cratekit/_vendor/downloader/`. Its upstream was removed from GitHub and
PyPI in December 2025, so no index can install it.

- **Provenance** is data: the `DOWNLOADER` record in
  `src/cratekit/_vendor/__init__.py` (project, version, licence, date).
- **Inventory, reductions, the numbered patch table and the attended smoke
  test** are in [`vendor/README.md`](../vendor/README.md).
- **The adapter boundary** around it is [`adapters.md`](adapters.md).

## Rules

| Rule | Enforced by |
|---|---|
| The vendored project is never a dependency specifier or an install command | `tests/test_vendor_import.py` |
| Its dependencies that still exist are ordinary dependencies in `pyproject.toml`, carrying upstream's upper bounds (except `requests<2.33`) | review; no resolver reads the vendored metadata |
| `requires-python` is `>=3.12,<3.14`, the vendored tree's range | `pyproject.toml` |
| Its licence, AGPL-3.0-only, ships inside the package and as `vendor/LICENSE.downloader`, byte-identical | `tests/test_vendor_import.py` |
| `scripts/scan_repo.py` scans it like any other tracked file | the scan |
| ruff skips it; every vendored module is byte-compiled instead | `tests/test_vendor_import.py` |
| Patches are applied by `scripts/revendor_downloader.py`, never by hand; the patched state is asserted in tests | `tests/test_vendor_import.py` |

## Patches

Each patch declares the exact text it expects. `Patch` and `SpanPatch` anchors
must occur exactly once and a `LinePatch` prefix must start exactly one line,
or the script aborts; a refused patch is re-derived, never skipped.

| Group | Why |
|---|---|
| Credential removal | upstream ships client credentials, encoded and commented out |
| Version metadata pinned | upstream read whatever `pyproject.toml` sat nearby |
| State directory name and adoption | the directory is `cratekit-downloader`, and one left under the old name is moved into place |
| No tempo tags | Cratekit never writes a beat grid or BPM tag |
| PKCE login | the provider serves the device-linking client lossy audio |

A new patch must point at upstream code that already exists and works.
Anything that has to be written here belongs in an adapter.

## Refreshing

The upstream sdist is not committed; `vendor/README.md` records where the
known-good copies are.

```bash
.venv/bin/python scripts/revendor_downloader.py path/to/tidal_dl_ng-<version>.tar.gz
```

The script:

1. unpacks the sdist with the `data` filter, reads the version from its
   `PKG-INFO`, and refuses one without a non-empty `LICENSE`;
2. replaces `src/cratekit/_vendor/downloader/` with the sdist's package;
3. drops the GUI modules and `api.py`, aborting if any is missing upstream;
4. deletes compiled files;
5. applies every patch;
6. removes the CLI's `gui` subcommand;
7. rewrites `from tidal_dl_ng` imports to `from cratekit._vendor.downloader`;
8. copies `LICENSE` into the package and to `vendor/LICENSE.downloader`.

Then:

1. Update `DOWNLOADER` in `src/cratekit/_vendor/__init__.py` (version,
   `vendored_on`).
2. Reconcile `pyproject.toml` with the new sdist's requirements.
3. Record any new patch in `vendor/README.md`'s patch table.
4. Run `scripts/scan_repo.py` and `tests/test_vendor_import.py`.
5. Run the attended smoke test in `vendor/README.md`.
