---
title: The per job key a label go's landing is recorded under kills no test alone
found: at the review of #647, U239, 2026-11-10.
issue: no
---

**The mechanism.** U239 records the landing a go's tail reached under
`landing_role(job)` on the run whose go queued the job. Writing it on the
queuing run is what closes the review's blocking finding; keying it by the job
as well guards a run holding a second job after its first landed, which no
shipped verb was found to produce.

**Measured cost.** At round two, `landing_role` returning the bare prefix
killed 0 of 71 tests and the record written on whichever run ran the tail
killed 1; both together killed 2. Two candidate producers of a second job
under one run were driven (`job cancel` on a landed job, `job resume` on it)
and neither produces it. No user facing cost measured.

**Closes when:** a test drives a run that holds a second go job after its
first landed, or the key is removed as unreachable. Ledger only.
