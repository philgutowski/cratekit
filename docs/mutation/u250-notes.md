# U250 mutation table, read

One table, the author's and not independent, `u250.md`, measured by
`scripts/mutate.py` on the cloud container at `41848089`, so a Linux measure of
a macOS suite, green net of the machine's failures. Eight rows, the size a
read only change calls for: four over `rebuild.read_truth`, three over
`tags.whole_number` and one over the raise in `tags.read_energy_checked`. Null
control 0 of 18567. All eight killed.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base `87e933be`, 161 ids, plus
one: `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`.
It killed the first driver run's null control, so that table was invalid. Run
alone on the base commit in its own worktree it failed (a file inode near
418,000 under the test's 2,000,000 bound); a second baseline measurement on the
base caught it passing and recorded the same 161. A file under `/var/tmp` drew
an inode near 575,000, also under the bound, so the scratch copy was the
remedy: the id was added there with that measurement as its comment and passed
to the driver, and the measured baseline file was not edited. See
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`.

## The thin rows

- **M5, a word read as 0, and M8, a decimal read as its whole part, die in one
  test each**, `test_a_numeric_reading_converts_the_way_the_single_readers_convert`.
  The container matrix cannot kill them: its oracle is the three single field
  readers, which since the fix round go through the same `whole_number`, so a
  change to the conversion moves both sides together. The literal
  expectations in that one test (energy 7, a padded 6, a word and a decimal
  read as None) are what pin main's conversion. Round two of the review
  measured the same for M8.
- **M7, the energy reader answering None for a word instead of raising**, dies
  in the two `tests/test_adopt_energy.py` tests that tell absent from
  unreadable, which is the distinction the raise exists for.
