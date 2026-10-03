# R-850 mutation notes

**Verdict: measured at sitting 30, 2026-10-02, 15 of 15 killed, none at
zero**, `r850-a.md`, run from the attended worktree at `main` with no
installed `crate` process running. What follows is why the author's own run
could not measure it.

**The author's verdict was: not measured.** Fifteen rows are written in `r850-a-rows.toml`,
one per guard this unit added: the summary's three counts and its unmatched
listing, the reason gate and the no match sentence, the warning's zero, total
and whole count checks, the shell's call to the verb's `concluded`, and the
renderer's queued gate, count gate, row fallback, line break quoting and row
lines. Every row's `old` text was checked to occur exactly once in its file
at the commit that added the rows.

**Why nothing was measured.** `scripts/mutate.py` stopped in its full
baseline with the STATE LEAK message, the real installation state's entry
count unchanged and its contents changed. Read before any rerun, as
`docs/solutions/workflow-issues/a-state-leak-halt-during-the-null-control-can-be-another-process-polling-the-installed-copy-so-read-the-newest-run-record-before-blaming-a-child.md`
says. The writer was not a child of the driver. `lsof` on the real
`provider_gate.lock` and `jobs/queue.db` named, in turn, a Python script on
standard input started from a separate attended session at 20:12 local, a
live `crate sync mark` from the installed copy at 20:23, and a live
`crate --run ...` resume after it, each against the installed copy and
each paced through the real provider gate, whose call count rose from 52,661
to 52,758 in seventy five seconds with nothing of this session's running.
The first writer ended after about four hundred seconds; the next started
within the minute's quiet check. Two more bounded waits, nine and five
minutes, did not see the real state go quiet. R-793 records redirecting the
watch as the wrong move unattended, and METHOD forbids a hand rolled driver,
so the table is left unmeasured rather than measured some other way.

**What does stand.** The battery on the branch, ruff clean, 12,262 passed
and 1 skipped, the scan clean. The guards are each exercised by a named test
written alongside them, which is the author's claim and not a measurement.

**To measure it.** With no installed `crate` process holding the real queue
or provider gate, from the branch's checkout:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/r850-a-rows.toml --out-dir docs/mutation

Promote any subset zero to a full run before reporting it, and pair a zero
on a user facing guard with a composite, as METHOD requires.
