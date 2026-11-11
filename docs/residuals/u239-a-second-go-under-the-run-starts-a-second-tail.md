---
title: A second --go under a label go's run while the first is still in its tail starts a second tail over the same folder
found: at the review of #647, U239, 2026-11-10.
issue: no
---

**The mechanism.** Since U239 a `--go` under the run of a go that started a
download takes that download on and runs its tail, asking nothing. A second
such `--go` started while the first is still in its tail queues `tag folder`
again, and its later steps meet the first's jobs. Before U239 the second
refused `decision-stale` before touching anything.

**Measured cost.** Driven re entrantly in one process at the review
(`test_T`): the second tail stopped at `analyze run` on `job-driver-held`.
Two processes were not driven, so what a real second tail does is unmeasured.

The same window from the other side, driven at round two in one process
(nested, not two processes): a fresh go landed the download while the
origin run's walk sat at a prompt, and the origin run's go, reading the
record it loaded at its start, ran the tail again, so two landing plans were
made over one folder, manifest and pass, and its save at exit overwrote the
fresh go's record of the landing.

**Closes when:** the continuation holds a lock per run, or reads a tail job
over the folder still open and refuses naming it. Ledger only, unmeasured.
