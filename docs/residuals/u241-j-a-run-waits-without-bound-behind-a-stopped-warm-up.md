---
title: A run waits without bound on the warm up lock behind a holder that is stopped rather than dead, and neither Ctrl-C nor a terminate ends the wait
found: at the review of #649, U241, 2026-11-11.
issue: no
---

**The mechanism.** `analysis/warm.py` takes an exclusive `flock` with no
deadline. A holder that dies releases it. A holder that is STOPPED keeps it:
round two sent a stop signal to a real `analyze run` while it was inside its
warm up, started a second run, and the second run's driver blocked in the
lock for 208 seconds, through a terminate at 45 seconds and an interrupt at
190, because the job engine records both signals for the item boundary
rather than raising and the lock call is restarted. It ended only when the
first run was continued, and then answered cancelled. Before the warm up two
runs never waited on each other.

**Measured cost.** A person who suspends an analysis in its first seconds
and starts another is blocked with no message, and Ctrl-C does not end it;
continuing or killing the first run does, and nothing is lost. The producer
driven was a stop signal sent by a script at a chosen moment. A person's
producer is Ctrl-Z inside a window measured at about half a second to two
seconds a process on a filled cache and about eight on an empty one; its
likelihood is unmeasured, and the terminal's own stop signal was not driven.

**Closes when:** the wait is a loop of non blocking attempts that reads the
job's recorded signal and says who holds the lock. A deadline that then
proceeds unlocked on an empty cache is the original crash again, so the
bound has to refuse or keep waiting with a message, and the change wants a
review of its own. Ledger only until a person meets it.
