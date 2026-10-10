# U131 mutation notes

The rows are `docs/mutation/u131-rows.toml`, ten rows over the round's own diff.
`scripts/mutate.py` refused on this Linux box because its full baseline is not
green (123 failing, the macOS proofs: hdiutil volumes, FAT hardware, backup
rehearsals), so the table is owed to the watcher's macOS run with:

    .venv/bin/python scripts/mutate.py docs/mutation/u131-rows.toml --out-dir docs/mutation

As a read only, not a table, each row was applied and its listed subset run
here: every row killed at least one test (K1 1, K2 2, K3 1, K4 2, K5 2, K6 1,
K7 5, K8 1, K9 1, K10 1). K10 guards the failure message's count and is
maintainer facing. Nothing was dropped for the cap.
