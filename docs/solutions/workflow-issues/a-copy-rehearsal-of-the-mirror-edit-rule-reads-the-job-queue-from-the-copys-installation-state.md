---
title: A copy rehearsal of the mirror edit rule reads the job queue from the copy's installation state, so a copy set up before the download was queued reads no landing
date: 2026-11-06
category: workflow-issues
module: src/cratekit/organize/mirror_downloads.py, src/cratekit/organize/account_mirror.py, src/cratekit/core/config.py
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - An organize run with mirror-edits is rehearsed on a disposable copy before the live run
  - A track a mirror download queued has landed and the plan should read it as landed for the account's edit
  - A rehearsal says "rekordbox's place stands" for a track U227 should carry
tags:
  - copy-rehearsal
  - mirror-edits
  - mirror-downloads
  - job-queue
  - installation-state
  - library-state
  - u227
  - u230
---

# A copy rehearsal of the mirror edit rule reads the job queue from the copy's installation state

## The trap

U227's landing rule needs two inputs beside the account and the database:
the mirror jobs that queued each download (`mirror_downloads._queued_at`,
`queued_from`) and the adoption ledger's entries for the landed row
(`mirror_downloads.filed`). They live in two different state roots:

- the job queue is `StateRoot.INSTALLATION` (`job_queue`, `jobs/`), under
  `CRATEKIT_STATE_DIR`;
- the adoption ledger and the mirror's snapshots (`outbound_writes.json`) are
  `StateRoot.LIBRARY`, under the library's state directory.

A copy rehearsal redirects both (the sitting 39 rule in
`an-unattended-live-sitting-decides-each-job-gate-twice-and-rehearses-on-a-copy-the-doctor-accepts.md`).
A copy whose installation state was copied before the download was queued,
or whose library state was cloned before the landing filed the row, reads no
mirror job or no landing entry. `filed` then gives nothing, the edit is read
by the later change rule, and the rehearsal says "rekordbox's place stands"
where the live run would carry the edit. Refreshing only the database copy
does not refresh either.

## What U230 found

Sitting 86 rehearsed A90's filing on a refreshed copy and read the later
change rule's why. Its record names the live queue and ledger as holding
both inputs. The why is reached only when the account side reads as an
addition, so the edited playlist's base did not hold the track at that read,
and driven on U204's disposable world with U227's real producers no snapshot
takes the queued track after the queue or the landing. Which input the copy
lacked was not measured, since the copy's state was not read; a copy whose
state predates the queue or the landing fits every observed line. U230 built
the brief's rule anyway (the edited playlist's base read as it stood at the
queue), so a base that does hold the track no longer stops it.

## The rule

Before rehearsing an organize that should read a landing, copy the
installation state (the `jobs` directory) and clone the library state after
the last queue and the last landing, then read both on the copy: the
mirror job holding the track (`crate job list` in the copy's environment, which reads the queue under its
`CRATEKIT_STATE_DIR`) and the adoption ledger's entry for the row. A
rehearsal missing either is not a rehearsal of the live plan.
