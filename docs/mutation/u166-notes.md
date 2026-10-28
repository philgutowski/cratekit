# U166 mutation table, read

One table, the author's and not independent, `u166.md`, measured by
`scripts/mutate.py` on the cloud container at `4384801`, so a Linux measure of
a macOS suite, green net of the machine's failures. 25 rows over
`intake/native.py` (9), `intake/batch_name.py` (1), `intake/land_cli.py` (1),
`intake/analyzed.py` (11), `intake/analyzed_cli.py` (2), `intake/refill.py`
(1) and `intake/rotate.py` (1). Null control 0 of 14479, every restore
verified against `git show HEAD`. All 25 killed, 65 deaths.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base, 168 ids, plus one:
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`.
It killed the null control in two driver runs, so neither table was valid.
Run alone on the base commit `3d94634` in this container it failed three times
of four, the first fresh run passing in 75 seconds, because it expects a file
inode above 2,000,000 and ext4 here hands out about 400,000 to 700,000. The
baseline battery caught its passing run. The id was added in a scratch copy
passed to the driver, with that measurement as its comment, and the measured
baseline file was not edited. See
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`.

## The two zeros, and the tests they bought

A first valid run at `4fd4b4f` left two user facing zeros, and each bought a
test rather than a composite:

- **C5, a membership whose collection row is missing is cleared.** No test
  held a membership naming no row.
  `test_a_membership_whose_collection_row_is_missing_stays_and_is_named`.
- **C13, the verb skips the read back.** Only the engine's unit test held
  `assert_read_back`; nothing drove the verb over a removal that did not take.
  `test_a_removal_that_did_not_take_is_refused_after_the_commit`.

The table here is the full run after both tests, not a resume: `--resume`
reuses a row whose text is unchanged, so it would have carried the two zeros
over.

## Ranked below the cap

Two rows were drafted and dropped to admit the refill and rotation
reservations the second review bought: the gate screen's found or made
wording (`collection_facts`), pinned by
`test_the_gate_screen_names_analyze_and_whether_it_is_found_or_made` and the
second landing test, and the clear's session record (`_record_clear_commit`),
pinned by the record assertions in
`test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
and the duplicate test. Each is a line a person reads or a restore lists,
ranked below a guard whose failure moves or clears a row.
