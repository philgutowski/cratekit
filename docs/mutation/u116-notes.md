# U116 mutation notes

Rows in `docs/mutation/u116-rows.toml`, 13 rows, the author's own.

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
| M7 folder reserved per playlist | zero on the watcher's macOS run, equivalent: `ledger.reserve_set_folder` answers the recorded folder on a second call, so dropping the once-per-year guard costs one ledger read and can never make a second folder; reclassified maintainer facing, no composite owed |
| M8 failure names nothing | killed |
| M9 yours lists a moved playlist | killed |
| M10 year check | killed |
| M11 earliest mark wins | killed, after a test of a playlist marked in two years was added |
| M12 nested folders ignored | killed |
| M13 utc year | killed |

12 of 13 killed on the watcher's macOS measurement (`docs/mutation/u116.md`).
M7 is equivalent and reclassified maintainer facing, no composite owed. M12 and
M13 are the review's guards for nested leave and local year.
