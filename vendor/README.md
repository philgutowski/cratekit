# Vendored components

Third-party code copied into this repository because no package index still
serves it. One component today.

The policy behind this directory, and why vendoring was chosen over a
`file://` reference or a git submodule, is in [`docs/vendoring.md`](../docs/vendoring.md).
This file is the inventory and the replacement procedure.

---

## Inventory

| | |
|---|---|
| Component | the acquisition downloader |
| Vendored version | **0.33.0** |
| Vendored on | 2026-08-01 |
| Smoke-tested end to end | **2026-08-28** (A1): authorize, download, no tempo tag on the MP4 or the FLAC surface. R-195, R-196 and R-197 were found there and are closed by U47 (2026-09-01). The attended re-run those fixes now need is R-210, and it is not done |
| Location | the one package under `src/cratekit/_vendor/`, which `src/cratekit/_vendor/__init__.py` records as data |
| Licence | **AGPL-3.0-only** |
| Licence text | the package's own `LICENSE` and the copy in this directory (byte-identical, asserted) |
| Upstream author | Robert Honz |
| Upstream repository | deleted; its address is kept for attribution in `src/cratekit/_vendor/__init__.py` |
| Supported Python | `>=3.12,<3.14`, which is where Cratekit's own bound comes from (KTD19) |

Cratekit's authored code is MIT. The vendored component keeps its own AGPL
licence, which ships with it in both locations above.

### Why it is vendored

The project was removed from GitHub and from PyPI in late December 2025, along
with its author's account. Its
documented install command fails outright, so no new machine can be provisioned
from any public source. A known-good copy exists only as a local backup. R6 and
R8 require a fresh clone to work without reaching a public index for it, and a
committed source tree is the only shape that satisfies that while surviving
`git clone`, editable installs, and Windows.

### Source artifacts

Two known-good copies exist, both outside version control in the source
repository's gitignored local-state directory. Both are **irreplaceable**: no
public index serves either one. Treat them as strictly read-only, extract into a
scratch directory, and never in place.

| Artifact | Shape | Status |
|---|---|---|
| the 0.33.0 source distribution | proper source distribution | **the vendored copy** |
| a 0.26.2 virtualenv backup | tarball of an installed virtualenv | fallback, not shipped |

The 0.33.0 source distribution was chosen over the older backup on evidence, not
preference:

* It is a real sdist with `LICENSE`, `PKG-INFO`, `README.md`, `pyproject.toml`,
  and the package. The 0.26.2 artifact is a virtualenv image whose `bin/` embeds
  an absolute interpreter path and whose `lib/` is bound to one Python minor
  version; it cannot be installed anywhere else.
* It installs cleanly from cold on Python 3.12, resolving every transitive
  dependency from PyPI, and every module on the download path imports.
* Its `requires-python` is exactly the bound Cratekit declares.
* 0.26.2 pins `tidalapi >=0.8.3,<0.9`; 0.33.0 pins `>=0.8.10,<0.9`. Neither
  collides with Cratekit, but 0.33.0 carries the later authentication code, which
  matters because a provider authentication change in March 2026 is what broke
  the older copy in practice.
* 0.33.0 drops the `mpegdash` direct dependency and adds `helper/camelot.py` and
  `helper/cli.py`, neither of which exists in 0.26.2.

### Transitive dependencies

These remain on PyPI and stay ordinary dependencies, declared in
`pyproject.toml` with the upper bounds upstream declared. **Vendoring moved
responsibility for those bounds onto Cratekit**: no resolver reads the vendored
package's metadata any more, so a bound not written into `pyproject.toml` is a
bound that no longer exists.

| Package | Note |
|---|---|
| `dataclasses-json` | settings and token serialization |
| `m3u8` | HLS manifest parsing |
| `mutagen` | already a Cratekit dependency |
| `pathvalidate` | filename sanitization |
| `pycryptodome` | **compiled C extension.** Wheels are published for CPython 3.12 and 3.13 on macOS, Linux, and Windows, so no user needs a compiler. It is the only non-pure-Python entry here. |
| `python-ffmpeg` | thin wrapper, but it **requires the `ffmpeg` binary on PATH**. That is a system dependency `pip` cannot install. Doctor has to check for it, or a download fails at the remux step with a message about a missing executable. |
| `requests` | already a Cratekit dependency; floor raised to 2.32.5 |
| `rich`, `typer` | the vendored CLI's output and argument parsing |
| `tidalapi` | already a Cratekit dependency; **floor raised from 0.7 to 0.8.10 and capped below 0.9.** The old specifier would have let a resolver pick 0.7.x, which the vendored tree cannot run against. |

`ansi2html` and `coloredlogs` are upstream dependencies that Cratekit does **not**
declare: the only modules importing them are in the GUI half, which is not
vendored. `toml` is likewise not declared; see patch 6.

---

## What was removed, and why

The vendored tree is not a verbatim copy. Every reduction and patch below exists
for a failure observed in the artifact, and each is applied by
`scripts/revendor_downloader.py`, which **aborts** if any of them no longer
applies. That matters more than it sounds: the classic way vendoring fails is a
version bump that re-copies the tree and silently drops the patches.

### Reductions

**1. The GUI half.** `gui.py`, `logger.py`, `dialog.py`, `worker.py`,
`helper/gui.py`, and the whole `ui/` directory. Every one imports PySide6 at
module scope, and PySide6 is an optional upstream extra Cratekit does not
install, so in a Cratekit environment none of them can import at all. Verified by
importing each in a clean environment: five for five raise
`ModuleNotFoundError: No module named 'PySide6'`. Shipping a module that provably
cannot import is a trap for the next reader. It also removes 356 KB of icon
binaries and two dependencies. The vendored tree is 256 KB against 932 KB for the
full package.

The CLI's `gui` subcommand is removed with it, rather than left pointing at a
file that is not there.

**2. `api.py`.** Three independent reasons, any one sufficient:

* it carries **five plaintext third-party streaming OAuth client id and client
  secret pairs**, with comments recording which other projects they were taken
  from;
* it **raises `JSONDecodeError` at import** in 0.33.0, because the JSON blob it
  parses at module scope uses `//` comments, which JSON does not have. It is
  upstream-broken, not merely unused;
* nothing in the package imports it.

### Patches

| # | File | Change | Failure it prevents |
|---|---|---|---|
| 1 | `constants.py` | `ATMOS_ID_B64` and `ATMOS_SECRET_B64` emptied | Upstream ships a third-party client id and secret here, base64-encoded and split across concatenated literals. Decoded, one is the same key published in `api.py`. R1: no shipped artifact carries credential material, encoded or not. |
| 2 | `config.py` | two commented-out plaintext credential lines removed | A scanner cannot tell a commented credential from a live one, and neither can a reader skimming a diff. Leaving them would force an exemption in the secret scan, and an exemption there is the hole the widened scan exists to close. |
| 3 | `__init__.py` | `metadata_project()` replaced by a pinned constant | **The sharpest hazard, and vendoring caused it.** Upstream walks up to three parent directories from its own `__file__` looking for a `pyproject.toml` and reads `["project"]["version"]` and `["project"]["urls"]["repository"]` out of whichever it finds, with no check on whose file that is. Vendored, the nearest such file is the HOST application's. Reading it raises `KeyError` at import time when the host declares no `[project.urls]`, and that lookup sits outside upstream's `try`, so `import` itself fails for a reason naming none of this. Today the walk misses Cratekit's `pyproject.toml` by exactly one directory level. That is a coincidence of depth, not a design. |
| 4 | `__init__.py` | `__name_display__` pinned to the upstream display name | It is not a label. It names the directory holding the settings file, the log, and the persisted token (`helper/path.py::path_config_base`). Derived from `__package__`, vendored it becomes the package's internal import path, plus a `-dev` suffix because the distribution is not installed under that name, so the tool would write its state to a directory named after an internal import path. |
| 5 | `metadata.py`, `download.py` | **all three tempo tag writes removed**, and the provider tempo zeroed at its entry point | **R17, the one rule with no configuration flag.** Upstream writes the provider's BPM into every file it saves: a Vorbis `BPM` comment for FLAC, an ID3 `TBPM` frame for MP3 and AIFF, and an MP4 `tmpo` atom. rekordbox reads file tags on import, so each seeds a grid Cratekit never authored. A wrong grid is worse than none: detection octave-folds, so a half-time or double-time grid drags every cue point and every loop the user ever set against that track. |
| 6 | `__init__.py` | `import toml` and `from pathlib import Path` removed | Only the replaced `metadata_project()` used them. `toml` is an unmaintained 2020 package the standard library replaced with `tomllib` in 3.11; declaring it as a Cratekit dependency to support dead code is a cost with no buyer. |
| 7 | `model/cfg.py` | `is_pkce` added to the `Token` dataclass | Upstream persists four token keys and has no field for the one that says which client minted the session. A PKCE token therefore reloads as a device-flow token and refreshes against the wrong client, and that client is the one the provider serves lossy audio to. A field the write never stores is a field the read cannot see (R-196). |
| 8 | `config.py` | `token_persist()` writes `is_pkce` | The other half of row 7: the field exists and nothing fills it. Written through `self.data` rather than `set_option`, because `set_option` calls `.lower()` on the incoming value whenever the existing one is a bool and `is_pkce` is this model's only bool field, so the obvious edit raises `AttributeError`. The source is the SESSION's flag, not the vendored login wrapper's: `login()` calls `login_token()` first, which assigns `self.is_pkce` from its own defaulted argument before any PKCE handshake runs, so reading it there would record every fresh PKCE session as a device-flow one. |
| 9 | `config.py` | the vendored `login()` mints through `login_pkce`, and reuses a stored session only when it is already PKCE (two patch objects, one per edit) | **The provider changed under this tool.** Lossless audio is gated behind the PKCE client; the device-linking client upstream calls is served lossy, silently, for every requested quality (R-196, driven by A1 on 2026-08-28 against the same account, track and minute). Upstream already carried the PKCE call here as a comment beside the one it used, so this flips which of two existing lines is live. No handshake is authored: the provider's client library ships it. There is deliberately no flag preserving the device flow, because a flag that preserves it preserves the defect. The reuse half is not cosmetic: upstream reuses ANY loadable token, so on a machine holding a device-flow token this method reports "you are logged in", never reaches the mint, and hands back the token the adapter refuses. That is every machine that ran the tool before the switch, which would have made the documented re-authorisation an unbreakable loop. |
| 10 | every module | absolute self-imports re-rooted under `cratekit._vendor` | The package imports itself absolutely throughout (33 statements across 8 files). Moved, none of them resolve. Absolute re-rooting is used rather than relative imports because a relative rewrite depends on each module's depth in the package, which is three rules instead of one and gets a file wrong quietly. |

### Two guard gaps this work exposed

Both are in guards owned by U6, both are real, and neither is fixed here because
that file is being edited concurrently. Reported rather than patched.

1. **`scripts/scan_repo.py` misses camelCase credential keys.** Its
   credential-assignment pattern expects `client_secret`; `api.py` uses
   `"clientSecret":`. The scan correctly caught the snake_case pair in
   `config.py` and missed all five in `api.py`.
2. **`tests/test_no_beatgrid_ever.py` misses two of the three tempo writes.** Its
   checker matches an assignment whose subscript key is in `FORBIDDEN_TAG_KEYS`.
   The ID3 write is a call, `tags.add(TBPM(...))`, not an assignment; the MP4 key
   is the atom name `tmpo`, which is not in the set. It caught one of three.

`tests/test_vendor_import.py` asserts all of these shapes over the vendored tree,
so this component is covered either way.

---

## Replacing it

Run the procedure, do not perform it by hand:

```
python scripts/revendor_downloader.py path/to/<the downloader's sdist>-<version>.tar.gz
```

The script extracts the sdist into a temporary directory, copies the package,
drops the reductions, applies every patch, re-roots the imports, and copies the
licence into both locations. **It refuses to finish if any patch anchor is
missing or ambiguous**, which is what stops a version bump from silently
reverting a credential removal or an R17 fix. A refusal is a signal to re-derive
that patch by hand, never to skip it.

Then:

1. Update `VENDORED` in `src/cratekit/_vendor/__init__.py` with the new version
   and date.
2. Reconcile `pyproject.toml` against the new sdist's `PKG-INFO` requirements.
   Bounds that changed upstream have to change here; nothing else reads them.
3. `python scripts/scan_repo.py`
4. `python -m pytest tests/test_vendor_import.py`
5. Run the attended smoke test below. Nothing automated can replace it.

### Attended smoke test

The verification that matters cannot be a unit test, because it needs an account,
an interactive authorisation, and the network:

1. Build a throwaway virtualenv on Python 3.12.
2. Install Cratekit from the checkout.
3. Authorise against the provider.
4. Download one track.
5. Confirm the file carries **no** tempo tag, in whichever container it arrived.

Step 5 is not optional. It is the only end-to-end check of patch 5, and R17 is
the rule with no fallback.

### If a provider change breaks it

Do not start by patching the vendored tree. The downloader sits behind the
adapter interface in `cratekit.acquire` (U14), and an alternative implementation
against the same contract is the designed response (KTD5). Replacing the adapter
is configuration; patching vendored code is a maintenance burden that compounds
at every version bump.
