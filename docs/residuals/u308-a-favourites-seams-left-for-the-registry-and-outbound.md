---
title: Seven favourites seam lines stay, four held by the registry declaring the favourites verbs with no toggle and three by outbound names favorites.cli keeps at module level
found: at the build of #865, U308, 2026-11-22.
issue: no
---

**The mechanism.** `tests/ratchets/imports/favorites.txt` keeps seven lines U308
could not clear from its own files. Four read `dangling favorites
cratekit.favorites.<verb>_cli`: `cli/registry.py` declares `favorites split`,
`backfill`, `order` and `refresh` with no toggle, so with the `favorites` module
off the registry still loads them, from a package the toggle owns. Three read
`dangling export cratekit.modules.outbound.<hearts|shell|source>`:
`favorites/cli.py`, which builds `sync favorites`, imports outbound's `hearts`,
`shell` and `source` at module level, because `tests/test_outbound_workers.py`
patches `favorites_cli.hearts` there, other files read the outbound constants
it holds (`NO_MATCH`), and `build_sync` takes its default from `source`.

**Measured cost.** None driven: every toggle is on in the shipped profiles. With
`favorites` off the four verbs still show and run; with `export` off and
`favorites` on, `sync favorites` cannot build.

**Closes when:** the registry gates the four verbs on `favorites` (the cli card,
#860, U303, whose file the registry is), and the outbound card (#866, U309)
moves the patch in `tests/test_outbound_workers.py` to the outbound module so
`favorites/cli.py` can import outbound under its functions; then
`refactor_measure.py prune favorites` empties the file. Ledger only.
