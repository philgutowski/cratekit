---
title: Closing the integrity check's handle removes the log files a capture of an open database records, and the restore then refuses the capture
found: at the review of #701, U272, 2026-11-13, driven on main at b09e0da.
issue: yes
---

**The mechanism.** `snapshot.capture` records which of the database's
companion files landed in the capture by looking for them before the check
runs. The check, `rb_writer.integrity_ok`, opens the copy through `open_db`
and closes it through `close_db`; for a database in write ahead log mode,
the last connection's close folds the log into the main file and deletes the
log and its shared memory index from the capture directory. The manifest
still lists both as captured, so `snapshot.assert_sources_present`, which
`restore.plan` asks, refuses: "records 2 files it no longer holds".

**Measured cost.** Driven by the U272 review on `main` at `b09e0da`: a write
ahead log database with its handle open, captured with the real check and
attached to a closed session; `restore.plan` refused the capture. No test
combines the real check with a restore, since the suite's captures use a stand
in verifier. Whether rekordbox's own database is in this mode, and so whether
every capture of the real library is one the restore refuses, was not
measured. If it is, a DJ's undo of any guarded write cannot run.

**Closes when:** the real database's journal mode is read at an attended
sitting, and the capture records what is in the directory after the check (or
the check runs on a copy of the copy), with a test that captures with the real
check and restores. Earns an issue: if reachable, a workflow a DJ needs, the
restore, cannot finish.
