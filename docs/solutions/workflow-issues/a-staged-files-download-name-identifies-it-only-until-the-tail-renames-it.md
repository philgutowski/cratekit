---
title: "A staged file's download name identifies it only until the tail renames it, and missing is not renamed"
date: 2026-11-11
category: workflow-issues
module: "src/cratekit/label/go.py, src/cratekit/cli/label_sync.py, src/cratekit/intake/land_cli.py"
problem_type: workflow_issue
component: label_sync
root_cause: wrong_identity
resolution_type: code_fix
applies_when:
  - "A verb decides which files in download staging are its own before a landing, which takes the whole folder"
  - "A job's recorded artifact path is used to find its file after the acquisition tail has run"
  - "A landing proof by pass is used to decide whether files in staging are waiting"
symptoms:
  - "A download whose tracks the tail renamed reads as landed, and a later landing takes them under another pass"
  - "A go is blamed for files that are another go's own renamed tracks, and the step named runs nothing"
  - "A count of renamed tracks lets as many foreign files through once the go's own left the folder"
related_components:
  - job_engine
  - intake_landing
tags:
  - staging
  - landing
  - name-apply
  - identity
  - r-1467
---

# A staged file's download name identifies it only until the tail renames it, and missing is not renamed

## Context

R-1467: every download stages into one folder and `intake land` lands the
whole folder, so a label go must not land files that are not its own. Each
download job records its artifact, the path a track was downloaded to, so the
first build found "its own" by those paths and judged other downloads the
same way, with a landing proof by pass for the rest.

## The trap

**The acquisition tail's `name apply` renames every track before the
landing's gate.** That is the usual state after any go or sync pass: the tail
stopped at the landing's gate, waiting for a person. From then on no job's
recorded artifact names any file in the folder, so:

- a plain download or a sync pass that reached its gate reads as gone, and
  the next go lands it under the go's pass (review round one, driven with a
  real `sync land`);
- a proof by pass cannot decide either: a go whose pass never gained a proof
  is blamed for any file no download names, including another go's own
  renamed tracks, and the step its refusal names runs nothing.

The second build let a go's own rerun read files no download names as its
own, bounded by how many of its tracks were no longer at their download
names. **Missing is not renamed**: once its tracks left the folder (a sync
pass landed them), that count let the same number of foreign files through
(review round two, driven end to end to a landing under the wrong pass).

## What holds

- Decide by what the landing would take, `intake.landing.listing`, not by
  which downloads are recorded: anything there that is not the verb's own
  track at its download name is beside it, whoever put it there. Attribution
  (which job, which pass) is for the message, never for the decision.
- Identity across the rename is recorded, not inferred: whichever way the tail
  ends, `label.go.keep_tail` keeps each file the folder holds by name, size
  and modification time, the identity the landing's own digest reads. Only
  those files are the go's own on its next run, and none once its pass has a
  landing proof.
- A test stand in that renames nothing hides all of this: the suite's `Tail`
  answers `name apply` with nothing renamed, so a test must rename the files
  itself, and at the moment the real step would, before the stop.
