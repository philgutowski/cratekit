# U124 mutation notes

The author's table, as METHOD says: every zero reads "the author could not
kill it" until a test does.

`docs/mutation/u124.md` is the batch of 23 rows over the new guards in
`scripts/board.py` and `scripts/scan_repo.py`, all maintainer facing. 22
killed. The one zero:

- **B19_audit_reads_folder**, zero across the full suite (13,024 collected).
  Nothing drove `cmd_audit` with a residual file present.
  `test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`
  landed for it, and `docs/mutation/u124-b19.md` reran the row alone: killed 1.

The first attempt at the batch was cut off by the 20 minute background cap
after five rows, with B4 (the missing opening fence) a zero. Its case passed
because the closing fence's message also contained the expected words. The
case now pins the opening check's own message, and the batch was rerun from
the start. That attempt's partial sidecar was discarded, not committed.

The first B19 rerun was INVALID. Its null control killed
`tests/test_sync_unmark.py::test_an_unreadable_record_refuses_the_mark_before_its_gate`
with a load average near 28 from two other lanes' drivers, and nothing in
`scripts/board.py` reaches that test. The second rerun's control was clean.

Nothing was dropped below the cap; 23 rows were authored and every one ran.
