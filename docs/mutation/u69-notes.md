# U69 mutation notes

The tables are `docs/mutation/u69.md` (rows M1 to M9) and `docs/mutation/u69-b.md`
(rows M10 to M20). Both were measured by `scripts/mutate.py` in the foreground on
`relay/114`, and the row files sit beside them as `u69-rows.toml` and
`u69-b-rows.toml`. There are 20 rows in total, under the cap of 25, and none was
dropped. Nineteen are over `src/cratekit/intake/missing_cli.py` and one, M20, is
over the verb's registry entry. The derived subset is `tests/test_intake_missing.py`,
21 tests. M20 names its own subset, that file plus `tests/test_cli_contract.py`.

The batch was split in two because a Relay session runs every command in the
foreground, and one batch of 20 rows with a promoted zero could pass the 600
second tool ceiling mid row. Each batch ran its own full suite baseline, green
with 7778 collected, and its own null control, which killed 0 of 7778. There was
no collect drift on any row. `git diff --quiet HEAD -- src` was clean between
the two batches, and `git status` after each batch showed only that batch's
output files.

This is the author's table. Nobody ran an independent pass.

19 of 20 rows kill.

## The zero

- **M14_frozen_config is inert at this entry point, not untested.** The row
  reads the reports with the live configuration instead of the job's frozen
  one. `artifacts.committed` resolves its folder through
  `jobs.store_dir(cfg)`, which is `config.state_path("job_queue", cfg)`, and
  the `job_queue` state entry is `StateRoot.INSTALLATION` (see
  `core/config.py`, the entry keyed `job_queue`). An installation scoped entry
  ignores the config it is handed, so no configuration can make the two
  readings differ, and no test can kill the row. The frozen config is still
  what is passed, because it is the brief's instruction and it stays correct
  if the queue ever becomes library scoped. That move would make this row
  killable. The promoted full suite run collected 7778, the baseline.

## What the killing rows hold

- M1 to M6 are the refusals that keep a partial list from reading as
  complete. They cover a job of another verb, a job that is not succeeded,
  a job with no items, reports that do not cover the items, a count
  comparison standing in for an identifier comparison, and a state word the
  verb cannot read. Each kills at least one test, and M5 kills the test built
  for it, a stray report and a skipped one cancelling out.
- M7 and M8 are the selection. Listing offered rows kills 4 tests, and
  listing suppressed rows kills 1: the tombstone test, where a heart deleted
  on purpose would otherwise have been downloaded.
- M9 and M13 are the review's second finding and the no-op outcome.
- M12 and M16 are what a person reads, driven in the default human mode, not
  in json.
- M20 declares the verb `plan/1`. That kills 10, because the human renderer
  shows nothing of a plan payload, which is the reason the verb is
  `diagnostic/1`.
