# U211 mutation notes

**The table.** `u211.md` and `u211.json`, 25 rows over the scan, the writer's
probes, the binding's probe, the dispatcher's kept run, doctor, the backup's
database portion and the restore session's database half. The null control
killed zero and every row killed at least one test; D3 was promoted to the
full suite and killed there. Measured by the author, so a row that killed is
a guard the author could kill, and the table says nothing of what an
independent table would find.

**One known failure added for this table only.** The driver was passed a
scratch copy of `.cloud-battery/baseline.txt` with one id added,
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
never written into the measured file. It failed 7 of 8 alone on the base
`9bc03db0` (4 of 4 under `/tmp`, 3 of 4 under `/var/tmp`), it killed the null
control of one batch and reddened the baseline of another, and nothing in
this unit touches it. It is the inode bound trap the solutions entry
`an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies`
records; `/var/tmp` did not clear it this time.

**One batch refused before any row.** A subset baseline was red on
`tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.unmark]`,
which passed alone and did not redden the next batch: intermittent under the
parallel run.

**Zero guards the reviewer found and this table does not carry.** Round one's
review reverted guards on a scratch copy of `src` and found six that kill
nothing, each harmless when removed: the re-entry guard in
`rb_writer._binding_probe`, the `is careful` check before the binding's name
is restored, `and not parked` on `kept`, the dry run branch of
`restore_cli._absence_unconfirmed`, `if name:` in `running_processes`, and the
no command line wording of `run_continue_command`. Round two found the names
in `read` in the writer's `rekordbox_processes_running` unreachable through
the scan, since a probe that refused never had its own name read; its comment
now says so, and row W7 measures the guard that closes round one's finding
(the refusal when nothing was read) instead.

**Dropped below the cap.** W2 (an `ImportError` read as a failed scan,
maintainer facing), W6 (the binding's name put back, pinned by its own test),
S1 (setup's note, the same catch shape as C2, killed by round one's scratch
row m13), S2 (setup's early check, the same shape again).
