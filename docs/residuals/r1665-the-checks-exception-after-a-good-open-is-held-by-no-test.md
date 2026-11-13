---
title: The integrity check's answer for a consistency check that raises after a good open is held by no test that runs on Linux
found: at the review of #804, R-1665, 2026-11-13.
issue: no
---

**The mechanism.** `rb_writer.integrity_ok` answers False when `PRAGMA
quick_check` raises after the open succeeded (`except Exception: return
False`). Mutated to answer True, the only tests that fail are the two sealed
database tests in `tests/test_rb_writer_db.py`, which fail on the Linux
container anyway because it runs as root, so on Linux the branch is held by
nothing. The guard predates R-1665; the round two review found it while
checking that R-1665's new damage test reaches the consistency check's own
verdict, which it does.

**Measured cost.** None driven. Four damaged copies were tried (a truncated
tail, an index cell count of 0xffff, a garbage index body, a garbage root of
an empty table) and none made `quick_check` raise after a good open, so the
input that would reach this branch is unmeasured.

**Closes when:** a damaged copy that opens and then makes `quick_check`
raise is found and pinned, or the macOS battery is confirmed to kill the
mutant through the sealed database tests. Ledger only: no producer is known.
