---
title: A label go stopped at its tag step carries the tag job's bare cause, so the per file report tag folder now gives is read only by running the step again
found: at the review of #648, U240, 2026-11-11.
issue: no
---

**The mechanism.** `tail.settle` and `tail.job_error` in `src/cratekit/cli/tail.py` drop the tag job's envelope and raise the job's own cause. U240 put the per file report (each file by label, by catalogue or not at all, the failed files named, the two label sentence) on `tag folder`'s refusal, which the tail never relays.

**Measured cost.** Driven at round two of the review through `label sync` with a go, four files, catalogues blocked: the go exits with "finished 2 items and failed 2" and no counts, no failed file named beyond the inner cause, no two label sentence. Nothing false is said; the stop's first step, `crate tag folder STAGING`, prints the report.

**Closes when:** the tail relays a step's refusal message and detail when a job ends failed, or names the command that prints the report. Ledger only.
