# U116 mutation notes

Rows in `docs/mutation/u116-rows.toml`, 11 rows, the author's own.

`scripts/mutate.py` refused on this machine before any row ran: its baseline is
the full suite, and the full suite is a macOS proof (123 failures on Linux,
hdiutil, rclone and APFS normalisation among them). So each row was measured by
hand the way the script measures it, the mutation applied, `tests/test_organize.py`
run with `-x`, the file restored, on grok-2's Linux box, 2026-10-09.

| Row | Result |
| --- | --- |
| M1 label rule dropped | killed |
| M2 set rule dropped | killed |
| M3 unmark ignored | killed |
| M4 folders not read | killed |
| M5 ambiguous year moves anyway | killed |
| M6 no adopt | killed, after a test with no set archive was added; the first run survived because the archive adopted the same folder first |
| M7 folder reserved per playlist | survived, equivalent: `ledger.reserve_set_folder` answers the recorded folder on a second call, so a second reservation writes nothing and changes no outcome |
| M8 failure names nothing | killed |
| M9 yours lists a moved playlist | killed |
| M10 any four characters a year | killed |
| M11 earliest mark wins | killed, after a test of a playlist marked in two years was added |

10 of 11 killed, the eleventh equivalent. The watcher's run of `scripts/mutate.py`
on macOS is the measurement of record.
