---
title: Modules import sqlalchemy, construct and soundfile directly while Cratekit declares none of them, relying on another package's requirements
found: at the review of #698, U269, 2026-11-12.
issue: no
---

**The mechanism.** A sweep of `src/cratekit` for imports no line of
`pyproject.toml` declares, made while proving lxml unused, found three that a
default install still resolves only through someone else's metadata.
`sqlalchemy` (imported in `write/row_link.py`, `write/playlist_pair.py`,
`sync/twins.py`, `tagging/rows.py`, `organize/` and others) and `construct`
(`analysis/rekordbox_check.py`) arrive because `pyrekordbox==0.4.4` requires
them. `soundfile` (`analysis/decode.py`) arrives because `librosa` requires
it. The others the sweep names are handled: `yaml` in `cli/doctor.py` is
caught as `ImportError` and named as the dev extra's, `streamrip` is the
optional adapter's lazy import, and `PySide6` is the vendored tree's GUI,
which Cratekit never runs.

**Measured cost.** None today. `pyrekordbox` is pinned exactly, so its
requirements cannot move under the core; `librosa` has a floor and no
ceiling, so a release that drops `soundfile` would break `analysis/decode.py`
with a `ModuleNotFoundError` naming none of this. `tests/test_packaging.py`
already argues the same for numpy in the analysis extra.

**Closes when:** `sqlalchemy` and `construct` are declared in the core with
the floors `pyrekordbox` states, and `soundfile` in the analysis extra, or a
recorded decision says the pin makes the first two unnecessary. Ledger only:
out of U269's scope, which names no other dependency.
