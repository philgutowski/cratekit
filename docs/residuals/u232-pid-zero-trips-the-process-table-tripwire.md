---
title: A lock record with no pid trips the suite's process table tripwire, since psutil answers pid zero from its whole listing
found: at the review of #606, U232, 2026-11-07.
issue: no
---

**The mechanism.** U232's autouse fixture in `tests/conftest.py` leaves
`psutil.pid_exists` real, which is right for the lock liveness path, and trips
on `psutil.pids` and `psutil.process_iter`. On POSIX psutil answers
`pid_exists(0)` as `0 in pids()`, so `core.session.process_exists(0)` and
`holder_alive` over a holder record with no pid field (`from_json` defaults
the pid to 0) reach the tripwire. The product turns the refusal into an
unknown answer, `None`, read towards alive, where this Linux host answers
`False`, and the test fails at teardown with a message naming the two seams
U232 stubs, neither of which is the route. Read from psutil's source and not
measured: a Mac lists `kernel_task` at pid 0, so `process_exists(0)` is
already `True` on a Mac and `False` on Linux on `main`, before this unit.

**Measured cost.** Maintainer facing only. Driven by the review with a scratch
test under the real conftest: both calls error at teardown with a stack naming
`core/session.py` line 740. No test in the suite reaches it, measured over the
whole branch suite. No product writer of a pid less holder record was found;
the candidates are a hand edited or truncated lock file, not driven.

**Closes when:** the session's liveness check answers pid zero without asking
psutil, as no process a lock names, or the tripwire on `pids` lets a call
made from inside `pid_exists` through. Ledger only: it costs a future test's author a misleading message,
not a DJ anything.
