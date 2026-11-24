---
title: "A driver started under nohup and an ampersand ignores SIGINT, so a kill that needs the interrupt reads zero"
date: 2026-11-24
category: workflow-issues
module: "scripts/mutate.py, src/cratekit/core/pool.py, tests/test_pool_stream.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: environment_constraint
resolution_type: workflow_improvement
applies_when:
  - "a mutation batch or a kill set replay is started by hand in a helper container rather than as the harness's own tracked background job"
  - "a row's killing test sends the process the terminal's interrupt and expects the default handler"
tags: [cloud, mutation, replay, killset, sigint, nohup, background, helpers]
---

## The trap

U334 (#983) replayed 2,592 rows in twenty helper containers. Pair 4's
`killset.py check` lost one row, `u241.M01_worker_takes_the_interrupt`:
the stream worker's `signal.signal(signal.SIGINT, signal.SIG_IGN)` in
`src/cratekit/core/pool.py` removed. Its one killer,
`tests/test_pool_stream.py::test_the_terminals_interrupt_does_not_kill_a_stream_worker`,
has each worker send itself SIGINT and fails when the interrupt kills it.
Neither file had changed. The after helper had started the driver as
`(nohup .venv/bin/python scripts/mutate.py ... &)` from a foreground call. A
command a non interactive shell backgrounds with `&` starts with SIGINT
ignored, nohup keeps it so, Python then installs no `KeyboardInterrupt`
handler, and every worker the pool forks inherits the ignore. With the line
removed the worker still ignores the interrupt, so the mutant survives and
the row reads zero, promoted to the full suite and zero there too.

Measured on one container: the mutant failed the test 5 of 5 runs with SIGINT
at its default, and passed under `trap '' INT`, as the unmutated code does.
`python -c "import signal; print(signal.getsignal(signal.SIGINT))"` prints
`default_int_handler` in the foreground and as the harness's own background
job, and `1` (`SIG_IGN`) under `( ... &)`, with or without nohup.

## What to do

- **Start the driver, the baseline and the battery as the harness's tracked
  background job**, as METHOD's driver rules say, never under `&`, `nohup` or
  `setsid` inside a shell. A shell cannot undo an ignore it inherited: POSIX
  forbids a non interactive shell to trap or reset a signal ignored on entry.
- **A row a replay reads zero that its own table killed** is measured again,
  on both sides, in a process whose SIGINT is the default, before the loss is
  believed. U334 ran it as a one row batch each side, recorded beside the
  pair.
- **Ask the helper how it started the driver** when a lost row's killer sends
  a signal; the table does not record the disposition it ran under.

## Related

- `a-kill-set-replay-of-thousands-of-rows-is-paid-in-starts-null-controls-and-zero-promotions.md`,
  the helper practice this extends.
- The residual U334 filed, that the driver neither records nor refuses an
  inherited SIGINT ignore.
