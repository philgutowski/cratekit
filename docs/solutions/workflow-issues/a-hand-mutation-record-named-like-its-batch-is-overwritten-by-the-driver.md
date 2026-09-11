---
title: "A hand mutation record named like its rows batch is overwritten by the first attended driver run"
date: 2026-09-11
category: workflow-issues
module: "scripts/mutate.py, docs/mutation/"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
tags:
  - mutation-table
  - r-329
  - hand-check
  - record-loss
applies_when:
  - "A relay session cannot run scripts/mutate.py inside its ten minute call and checks rows red by hand instead"
  - "A hand written record is about to be saved beside a rows file under docs/mutation/"
---

# A hand mutation record named like its rows batch is overwritten by the driver

## What happens

`scripts/mutate.py` writes its results to `docs/mutation/<batch name>.md` and
`.json`, where the batch name is the rows file's `name` field
(`write_outputs`). It does not check whether that file already exists.

Since R-329, a relay session cannot finish the driver inside its foreground
call, so it checks rows red by hand and writes the result down itself. The
natural name for that record is the unit's, `r-15.md`, and the natural batch name
in the rows file is the same, `name = "r-15"`. The rows file's header then tells a
person to run the driver attended. The first time somebody does, the driver
overwrites the hand record, and if that record holds a measurement the driver
does not reproduce, such as a full suite run taken BEFORE the guard existed, the
measurement is gone.

Found by the built in review on R-15, before any run. Nothing was lost.

## What to do

Give the rows file a batch name that no hand record uses, `r-15-driver`, and say
so in both files, so the driver's table lands beside the hand record rather than
over it. Or keep hand results inside the rows file's header comment, which the
driver reads and never writes, as R-14 and R-11 did.

A before measurement is the one to protect most. A pin can be checked red at
any time, but a measurement of what the suite let through before the pin existed
can only be taken once, before the pin is committed.
