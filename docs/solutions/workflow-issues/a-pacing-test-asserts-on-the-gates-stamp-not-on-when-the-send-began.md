---
title: "A pacing test asserts on the gate's stamp, not on when the send began"
date: 2026-09-29
category: workflow-issues
module: "tests/test_provider_gate.py"
problem_type: workflow_issue
component: testing_framework
root_cause: incorrect_assumption
resolution_type: test_fix
applies_when:
  - "A test spawns real processes against a pacing gate, a rate limiter or a lock and asserts on times it measured itself"
  - "A test fails at a gate on a loaded machine and passes alone"
  - "A timing assertion carries a tolerance, a fraction of the interval or a ceiling in seconds"
symptoms:
  - "A list of gaps printed by an assertion, most at the interval and one or two well under it"
  - "Green alone three times of three, red in a full run the minute another application launched"
related_components:
  - provider_gate
  - relay
tags:
  - timing
  - load
  - flaky-test
  - provider-gate
  - r-759
  - r-711
---

# A pacing test asserts on the gate's stamp, not on when the send began

## What happened

`test_two_processes_never_call_at_once_and_keep_the_interval` failed twice
in a day at a Relay gate and once in a mutation baseline (R-711), each time
on a busy machine, and passed every time alone. It was a LOWER bound, not an
upper one: each gap between two send starts had to be at least nine tenths
of the interval. A lower bound on spacing sounds load proof, since a slow
machine can only spread calls out. It was not, because the test measured a
different quantity from the one the gate spaces.

The gate stamps `last_call`, writes the state file with an fsync, and then
sends. The next caller's due time is that stamp plus the interval. The test
timed each send's start, which is the stamp plus the write. When one write
takes longer than the next, two send starts land closer than the interval
even though every stamp is correctly spaced. Measured at load 13: the write
delay varied by 13.6 milliseconds, send starts came 40.7 milliseconds apart,
and the stamps stayed at least 50.1 apart against an interval of 50.

## The trap in the diagnosis

Running the old test twenty times beside a full suite, at load up to 15,
passed twenty of twenty. The failure needs a slow fsync on one call and a
fast one on the next, which a CPU bound suite does not reliably produce; a
desktop application launching did. So "I could not reproduce it" is not
"it is fine". Measure the mechanism directly, stamp and send start side by
side, rather than waiting for the assertion to fail.

## What to do

- Assert on what the code under test RECORDED, here the stamps in the shared
  state file, and compare them with the same arithmetic the code uses. The
  gate stamps the later of the clock and the last stamp plus the interval,
  so the bound holds exactly with no tolerance.
- Tie the real event to the recorded one with a bound load can only widen:
  a send never begins before its own stamp. That catches a gate that stamps
  correctly and skips the wait, which a stamp chain alone passes.
- Prove mutual exclusion with a marker created `O_EXCL`, not with spans. And
  hold each call LONGER than the interval, or the interval alone keeps calls
  apart and a gate with no lock passes.
- Each claim that needs a different hold gets its own test. One test with a
  short hold cannot kill a removed lock, and one with a long hold cannot kill
  a removed interval.

## Related

- `docs/solutions/workflow-issues/a-red-mutation-baseline-on-a-loaded-machine-is-starvation-before-it-is-a-failure.md`,
  the other way load reads as a failure.
- R-759 and R-711 in `docs/residual-findings.md`; the measurements are in
  `docs/mutation/r759-notes.md`.
