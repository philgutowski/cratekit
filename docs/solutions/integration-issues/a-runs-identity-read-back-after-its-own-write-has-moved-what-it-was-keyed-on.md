---
title: "A run's identity read back after its own write has moved what it was keyed on"
date: 2026-11-05
category: integration-issues
module: "src/cratekit/sync/pair_cli.py"
problem_type: integration_issue
component: tooling
severity: high
root_cause: identity_moved_by_own_write
resolution_type: code_fix
applies_when:
  - "A verb holds a plan under its run and reads it back in a later command (U209)"
  - "The write marks, makes or records something the plan's own identity is computed from"
  - "A continue of a run that stopped part way through its write refuses stale, or plans again"
tags: [sync-pair, held-plan, resume, stale, U209, U210]
---

# A run's identity read back after its own write has moved what it was keyed on

## Problem

U210's first drive of a ceiling stop after three of five made pairs, then a
continue of the same run, answered `decision-stale` at the gate: the held plan
had been refused and the pairs planned again. U209 reads a held plan back only
when it was made for the pairs the command asks for, and a sync of every pair
asks for every MARKED pair. The three pairs the stopped write had made were
marked now, so the command asked for more pairs than the plan was made for,
though nothing but the run's own write had moved.

## Cause

The held plan's identity (`extra.asked`, the targets and their marks) is read
off state the write changes: the pairs document. Any write step that marks a
pair (a made account side, a made rekordbox side, a first sync's mark of a
pair named by hand) moves it. The same shape waits in U209's check before the
write: discovery excludes paired rekordbox playlists, a queued job reads as
another sync's, a folder the plan was to make reads as one someone made, and a
title the run gave a playlist reads as taken.

## What to do

- Before a held plan or a check is compared with the live state, take out
  what the run's own recorded steps account for (`_asked_before`, and
  `ours`, `our_folders` and the `STEP_QUEUED` exclusion in `check`), and read
  a list the run part wrote for only what its own write could have done
  (`_beyond`). Never relax the comparison for anything the steps do not name.
- A test for a resume drives the stop with a real provider gate in front of
  the fake account (`tests/test_sync_pair_resume.py`, `gate_the_account`), at
  every stop point the write has, and asserts the continue made nothing twice
  and planned nothing again.
- Any new check added to U209's `check` needs the same question asked of it:
  can this run's own write, part done, produce the state it refuses?
