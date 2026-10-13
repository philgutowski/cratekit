# U140 mutation notes

Author's table, measured on macOS on `relay/317` after the review fixes,
in two runs of `scripts/mutate.py docs/mutation/u140-rows.toml`, the second
with `--resume` so the first six rows were reused. 16 rows, 16 killed, no
zero row, so no composite was owed. Every row's head verified against HEAD
and the tree was clean after each run.

Every count is the author's own measurement. No independent verifier ran
(METHOD), and independent tables have found more than authors' before.

Dropped, one row: `C1_ledger_already_moved_return`, the early return in
`ledger.rename_set_playlist` when the record is already under the new name.
It is reached only by a race between the plan and the apply, because the
plan takes a record under the new name and then plans no rename, so it is
maintainer facing and ranked below the cap.
