---
title: a resort or rebuild resume refused because another driver holds the job carries the holder's findings so far as its own steps
found: at the review of #1036, R-2020, 2026-11-24.
issue: no
---

**The mechanism.** Each resume drives inside `ReportedDrive.owing()`, which
adds the after check's sentences, read from the committed item reports, to any
refusal raised there. `job-driver-held` is raised inside it, before this run
claims anything, so the refusal names what the other driver's finished trees
left and did not compare, counted so far while it keeps going. That is
against the rule `test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
states for the resort's calibration refusal (a run that drove nothing answers
for no tree). The resort did this on the base; the rebuild does it from
R-2020. `rebuilt` also turns `DriverHeld` into a plain `CratekitError`, keeping
its reason and exit code; no reader in the process tells them apart for these
verbs.

**Measured cost.** Driven with the driver lock held in process: exit 20,
`job-driver-held`, with the leftover and the not compared sentences of the one
committed tree as steps. True of that tree, and partial. Not driven with two
processes.

**Closes when:** `owing()` adds the steps only when this run claimed an item,
or the driver held refusal is raised before it. Ledger only.
