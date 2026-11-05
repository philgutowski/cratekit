---
title: Reporting a finished resort through route resort --job meets its gate again
found: at the review of #537, U219, round one, 2026-11-05.
issue: no
---

**The mechanism.** Since U219 the resort's resume answers its explicit gate
from the job's frozen plan before anything else, so `crate route resort --job
J` on a job that already succeeded, with no `--run`, mints a new run and
exits `decision-required`. With `--run` naming the gate run it reports as
before.

**Measured cost.** Driven after a succeeded job: exit 10 with empty checks.
`crate job show J` reports the job, and the resume the job engine spawns
carries `--run`, so no queued work stalls. The cost is a person reaching for
the verb to read a result and being asked a question already answered.

**Closes when:** the resume answers the gate only while the job is open, and
a closed job is reported without it.
