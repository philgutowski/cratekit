# U131 mutation notes

The rows are `docs/mutation/u131-rows.toml`, thirteen rows over the unit's own diff, K11 to K13 added at review round one.
`scripts/mutate.py` refused on this Linux box because its full baseline is not
green (123 failing, the macOS proofs: hdiutil volumes, FAT hardware, backup
rehearsals), so the table is owed to the watcher's macOS run with:

    .venv/bin/python scripts/mutate.py docs/mutation/u131-rows.toml --out-dir docs/mutation

As a read only, not a table, each row was applied and its listed subset run
here: every row killed at least one test (K1 1, K2 2, K3 1, K4 2, K5 2, K6 1,
K7 5, K8 5, K9 1, K10 1, K11 1, K12 1, K13 2). K10 guards the failure message's count and is
maintainer facing. Nothing was dropped for the cap.

**Review round one.** The UNDATED leave of U116 is reversed on purpose: a
playlist whose mark carries no year is filed in `Mine` with the reason
`UNDATED`, pinned by `test_a_playlist_whose_mark_has_no_year_is_filed_in_mine`.
K8 and K9 now read against the gated filing in `export.py`; K9's mutation
narrows the warning's catch, which the filing failure test kills.
