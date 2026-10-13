---
title: An unattended live sitting decides each job gate twice, rehearses on a copy the doctor accepts, and keeps the machine quiet while a table measures
date: 2026-10-13
category: workflow-issues
module: "cratekit gates, scripts/mutate.py state guard, copy rehearsal"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "A session drives gated database or account writes live with nobody present, after a rehearsal on a copy"
  - "A verb queues a job and the continuation stops at its gate again"
  - "A copy rehearsal config is refused by crate doctor"
  - "scripts/mutate.py stops with STATE LEAK during a night that also runs live verbs"
tags:
  - "unattended"
  - "live-gate"
  - "copy-rehearsal"
  - "job-continuation"
  - "mutation-driver"
  - "state-guard"
  - "digest"
related_components:
  - "tooling"
  - "database"
---

# An unattended live sitting decides each job gate twice, rehearses on a copy the doctor accepts, and keeps the machine quiet while a table measures

## Context

Sitting 39 (2026-10-13, merge 62ead9c, `docs/cutover.md` "Sitting 39") was run by the overnight watcher with nobody present. Every gated write was rehearsed on a disposable copy, then driven live by the installed `crate` through a small driver script, `live_gate.sh`, kept in the watcher's state directory outside the repository. For each verb the script plans live, compares the live digest with the rehearsed one, decides the gate as the actor `session`, runs the verb under its run, and continues a queued job. The same night, mutation tables for the landing cards kept measuring in the gaps. Three mechanisms cost time and are not visible in the final code.

## Guidance

**1. A job backed verb asks its gate a second time on the continuation.** `adopt scan`, `adopt apply` and `adopt move` queue a job when the first gate is decided. Continuing that job with the job flag raises a fresh run and a fresh gate, with its own digest. A driver that decides once and then continues reports a gate left open. Decide, run, read the job id from the envelope, continue, and if the continuation shows a gate, compare its digest with the expected one and decide again. The same equal digest check applies to the second gate, because a state change between the two asks is exactly what the check is for.

**2. A copy rehearsal needs three things before the doctor accepts its config.**
- `db_path` names a database copy that sits under `library.root`, as a scratch copy on the volume (removed when the sitting ends, or the next backup mirrors it).
- The volume's `.cratekit` is cloned to a scratch name (`.cratekit-copyrun`) and `library.state_dirname` is pointed at it, so no ledger the live run reads is marked done by the copy.
- The installation state is copied under the redirected `CRATEKIT_STATE_DIR`, including the backup acknowledgment, which is state too.

Leave one of these out and `crate doctor` refuses the copy's config, or worse, accepts a config whose state paths are the live ones. Read the doctor's `tree.registry` line and each gate's reads and writes lines for the scratch name before answering any gate on the copy. This extends the rule in `docs/solutions/workflow-issues/a-disposable-database-copy-does-not-make-library-state-disposable.md`, which says why library state must be redirected; this adds the one setting the doctor insists on when the database copy is not at its live path (`db_outside_root_acknowledged_on`, `src/cratekit/core/config.py:2449`).

**3. The mutation driver's state guard trips on three sources a live night produces.** `check_state_guard` (`scripts/mutate.py:896`) fingerprints the real installation state at the start of a batch and stops the batch when it moves, and by its own docstring it cannot tell a child's write from a concurrent one. During sitting 39 the movers were:
- the watcher's own `crate doctor`, which writes a run record;
- any account read, which writes `provider_gate.json` (`src/cratekit/core/config.py:791`), including a read only check of the Tidal account;
- a job journal under the state root, written by another lane's verb.

The driver exits 6 and prints `STATE LEAK`. A table measures only while no live verb, doctor, or account read runs from the same machine. Run the live steps in the gaps between tables, take the rows that stopped as unmeasured with their rerun command, and `pgrep` for a live crate before suspecting the child. See `docs/solutions/workflow-issues/a-state-leak-halt-during-the-null-control-can-be-another-process-polling-the-installed-copy-so-read-the-newest-run-record-before-blaming-a-child.md` for reading the newest run record.

## Why This Matters

A session that waits for a person at each gate cannot finish a night's work, and the rehearsed digest is the check the person was making. That only holds if the second gate is also compared, the copy really is isolated, and the measurements it ran beside were not disturbed. A skipped second gate leaves a half applied adoption; a leaky copy marks the live ledger done; a tripped guard throws away a table's elapsed time.

## When to Apply

Any live sitting driven by a session rather than a person, and any night where mutation tables and live verbs share one machine.

## Examples

The digest rule that held: every live digest equalled its rehearsal except `favorites refresh`, whose only difference was the row ids of folders created separately on the copy and on the live library. That is the id only shape the 2026-10-09 rule approves after the difference is read and recorded in the sitting record. A difference in what is written, as opposed to an id, still stops the run.

Timing on the account: `organize --only file` reported in 22 minutes and applied in 45. Run such steps under nohup with a pid waiter, since a background command dies at thirty minutes.
