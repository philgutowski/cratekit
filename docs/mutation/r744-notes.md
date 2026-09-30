# R-744 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/232`, in the foreground, one at a time, with
`CRATEKIT_CONFIG_DIR` and `CRATEKIT_STATE_DIR` pointed at an empty scratch
directory for the reason R-783 gives: a job of the author's was running
beside the session. Null control 0 on each, 11,059 collected against 11,059,
no collect drift, every restore verified against `git show HEAD`.

**The first attempt at `r744.md` was refused by the driver:** the null
control killed one test,
`tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`,
unrelated to the mutated module. The machine's load average was 8.8 at the
time and the test passed alone three times in a row. The batch was rerun
and the control read zero. A timing test under load is the shape the
2026-09-24 sitting recorded, and the driver did what it is for.

**`r744.md`**, 18 rows: the estimator's window, interpolation and prior in
`analysis/detect.py`, the binding in `analysis/cli.py`, the window's
validation in `core/config.py`, and the comparison in
`analysis/agreement.py`. 17 killed, one zero. The largest kills are `E3`, the
interpolation removed, 11, which is the whole of the off by one to three
bucket, and `A3`, the classic key names unmapped, 18.

**The zero, `E7_no_prior`, was the test's and not the prior's.** The test
put two equal peaks inside the window, and with the prior removed the
argmax tie fell on the higher tempo, which was the value the test expected.
The test was rewritten with both peaks on whole bins and the slower one a
twentieth stronger, so a flat window names the slower level and the prior
names the faster, and the row was measured again.

**`r744-b.md`**, 1 row: `E7` again. Killed, 1.

**19 rows measured, 19 killed, no zero standing.** Four rows were considered
and not run, each named in `r744-rows.toml` with the reason it ranked below
the cap: one is an equivalent mutant, three re-measure a single line each
that another row's consequence already covers.

Read as METHOD says to read an author's table: every count is what the
author could kill, and an independent table on this unit would find more.
