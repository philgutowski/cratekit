# U298's kill set replay, as far as #855 measured it

U298 (#855) began the kill set replay its rules ask for and stopped it on
2026-11-22, when Phillip split the replay into #930 (U325) so U298 could land.
This folder is what #930 resumes. It sits one level below `docs/mutation/` on
purpose: `killset.py` reads every `*.json` directly under `docs/mutation/` as
a recorded table, and an unfinished sidecar there would read as an unreadable
one.

## What is here

| batch | rows | measured | killed | zero | error | collect error | unmeasured |
|---|---|---|---|---|---|---|---|
| a | 932 | 226 | 225 | 1 | 0 | 0 | 706 |
| b | 932 | 281 | 277 | 1 | 1 | 2 | 651 |
| c | 931 | 307 | 304 | 3 | 0 | 0 | 624 |
| d | 930 | 388 | 385 | 3 | 0 | 0 | 542 |
| all | 3,725 | 1,202 | 1,191 | 8 | 1 | 2 | 2,523 |

- `u298-replay-before-X.json` is each batch's sidecar as the driver last wrote
  it, after its last finished row, measured on `main` at `539638eb`. Its header
  says `in progress`, because no batch finished.
- `u298-replay-before-X-unmeasured.txt` lists the row ids that batch had not
  reached.
- The row files are `docs/mutation/u298-replay-before-X-rows.toml`. Batch d's
  leaves out `u241-dsp.D4_settings_not_handed_to_the_head`, whose one test file
  is skipped whole where the audio libraries are absent; it is owed to the
  macOS battery.

Rows that did not read killed, for #930 to look at first:

- zero: `r1761.P24_flag_lost_in_the_worker`, `u62.S7_naive_expiry_as_local`,
  `r668-a.M11_no_frozen_list_skip`, `u42-author.W1_onerror_hook`,
  `u42-author.W3_onerror_silent`, `u90-d.D1_fit_refuses_over_its_energy_write`,
  `u94-b.W2_unreadable_not_counted`, `u263.D19_energy_duration`.
- error: `r390-a.A1_retry_re_arms_unconditionally`, at pytest's own cleanup
  (`Directory not empty: 'popen-gw0'`), the shape U298's own row H9 met; drive
  it by hand as `docs/mutation/u298-h9-driven.md` did.
- collect error: `r746-a.G8_key_dropped_from_the_content_policy` and
  `u111-a.A6_playlist_not_removable`, each a mutation that also changes how
  many tests collect; read their kills and the count by hand.

## How #930 resumes

Each batch ran in its own clone checked out at `539638eb`, one xdist worker
each (`PYTEST_XDIST_AUTO_NUM_WORKERS=1`), four side by side on a four core
container. A replay resumes rows only from a sidecar measured at the same
commit with no tracked file changed, so in each clone at `539638eb`:

    cp <this folder>/u298-replay-before-X.json docs/mutation/
    cp <branch>/docs/mutation/u298-replay-before-X-rows.toml docs/mutation/
    .venv/bin/python scripts/mutate.py docs/mutation/u298-replay-before-X-rows.toml \
        --known-failures <scratch copy> --resume

Batch d's row file differs from `539638eb` by the one row left out, which the
resume reads as a changed tracked file; #855 ran
`git update-index --assume-unchanged` on it in that clone. A resume measures
every subset baseline and the null control again before its first row, about
three to four hours a batch at one worker; the rows ran at about 210 an hour
across the four.

## The machine's failures

Measure the container's own baseline on `539638eb`
(`cloud_battery.py baseline`), copy it to the scratchpad, and append these two
lines with their measurement, as the solutions entry on the inode bound test
says. Never edit the measured baseline.

- `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`:
  failed alone 4 of 4 on `539638eb` on the container's disk (#702), and
  refused batches a and d's subset baselines.
- `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`:
  passed alone 4 of 4 and refused batch b's subset baseline once while the four
  batches ran side by side. It asks a later file for a higher inode, which ext4
  does not promise while other runs free inodes.

Batches b and d were last resumed against that copy, a and c against the
measured baseline alone. A row whose only kill is one of these two tests is not
believed until it is measured again against the copy.
