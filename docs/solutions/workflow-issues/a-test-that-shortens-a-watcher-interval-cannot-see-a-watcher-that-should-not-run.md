---
title: "A test that shortens a watcher interval cannot see a watcher that should not run"
date: 2026-10-09
category: workflow-issues
module: "src/cratekit/intake/fetch.py, tests/intake/test_set_progress.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: missing_workflow_step
resolution_type: test_fix
applies_when:
  - "A test asserts a background thread is absent, and the same test shortens that thread's interval to make another assertion fast"
tags:
  - mutation
  - threads
  - progress
  - r924
---

# A test that shortens a watcher interval cannot see a watcher that should not run

## What happened

R-924 added a thread to `fetch.fetched` that reports download progress every
fifteen seconds. It starts only when the verb was handed a progress writer,
and JSON output hands None. The test for JSON output shortened the interval
to 0.01 s, then had a fake fetcher check whether a watcher thread was
running. The mutation table removed the guard that keeps the thread from
starting, and that test still passed. Row F6 killed nothing.

## Why

With the guard gone, the watcher started with `progress` set to None. On
its first tick it called None, raised `TypeError`, and the thread died.
Python reports an exception in a thread through `threading.excepthook` and
nowhere the test reads. At 0.01 s the thread was dead before the fake
looked, so "no watcher running" was true, and it was true of a watcher that
had started, failed, and gone.

The same shape appears whenever a background loop calls something it was
handed. A loop that should never have started fails fast when the thing it
was handed is missing, and a test that waits past that failure reads its
absence as the loop never having started.

## The rule

Assert a thread's absence at the shipped interval, or at any interval
longer than the test takes. Shorten the interval only in a test that
asserts what the thread SAYS, where a dead thread fails the assertion
rather than passing it.

## Where it was fixed

`tests/intake/test_set_progress.py`, `WatchedFetcher`, which now runs at
the shipped interval. `docs/mutation/r924-notes.md` records that the fix
landed after the table's one pass and the row was not re-measured.
