---
title: "A vocal loader an earlier test left bound adds analyze vocals to the tail, so an exact list of the tail's verbs fails on some runs of the suite"
date: 2026-11-01
category: workflow-issues
module: "tests/test_label_sync_go.py, src/cratekit/analysis/vocals.py, src/cratekit/cli/tail.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: test_isolation
resolution_type: test_fix
applies_when:
  - "scripts/mutate.py reports INVALID BATCH: the null control killed a tail test the branch never changed"
  - "A test asserts the exact list of verbs the acquisition tail ran, and passes alone and in its own file"
symptoms:
  - "At index 4 diff: ('analyze', 'vocals') != ('analyze', 'restamp')"
  - "test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate dies under the mutation driver's full runs and passes in cloud_battery.py, alone, and in its file"
tags:
  - "cloud-lane"
  - "mutation-driver"
  - "null-control"
  - "vocals"
  - "tail"
  - "xdist"
---

## The trap

`vocals.unavailable()` answers None, able to score, whenever a loader is bound
in the process, and an analysis worker driven in process binds the shipped one
and leaves it there. The tail (`cratekit.cli.tail.rescore`) asks it before it
runs, so in an xdist worker where an earlier test drove an analysis, the tail
queues `analyze vocals --unscored` after `analyze run`. A test that pins the
tail's verbs as an exact list then fails, and only on the distributions of the
suite that put such a test first on the same worker.

Measured at R-1115 on 2026-11-01: the mutation driver's null control killed the
go's tail test in two of its four full runs, while `cloud_battery.py baseline`,
`compare`, three more full runs, 25 runs alone and ten runs of its file passed.
A scratch test that only binds `vocals._VOCAL_LOADER`, run first in the same
process, reproduces it every time.

## What to do

- A suite that asserts what the tail ran pins the vocal model's state in its
  own fixture, never inherits it: `tests/test_sync_land.py` binds a stand in
  loader (`vocal_model`), and `tests/test_label_sync_go.py` pins the model
  unable (`no_vocal_model`), each with `monkeypatch` so the pin is undone.
- To prove a suspected leak, bind the global in a scratch test file named to
  sort first and run it with the suspect in one `-n 0` process.
- A test the null control kills that passes alone is not the machine's until it
  is measured on the base; here it was the suite's, and the fix was the fixture.
