---
title: A test that hands a verb a failing provider sleeps the listing's real retry ladder, 31 seconds a reading, unless it binds the sleep
date: 2026-11-12
category: workflow-issues
module: src/cratekit/acquire/listing.py
problem_type: workflow_issue
component: provider_listing
root_cause: wrong_assumption
resolution_type: test_fix
severity: low
symptoms:
  - "A test over a provider failure takes 31 seconds, or a whole multiple of 31, and passes"
  - "One worker of the parallel suite carries minutes more than the others and the run sits at 99 percent"
applies_when:
  - "A test hands a verb a fake playlist, listing or provider call that raises something other than a refusal declaring retryable False"
tags:
  - "listing"
  - "retry-ladder"
  - "sleep"
  - "slow-test"
  - "u252"
---

# A test that hands a verb a failing provider sleeps the real retry ladder

## What happened

The speed survey of 2026-11-12 found the three slowest tests of 18,085 in
`tests/test_sync_twins.py`, 187 seconds between them, each a whole number of
31 second ladders: a fake playlist raising `RuntimeError("the provider timed
out")` climbed `listing.fetch_with_retry`'s ladder, 1, 2, 4, 8 and 16 real
seconds, once per reading. U252 bound the sleep and they take a third of a
second each.

## Why patching time.sleep does not help

`fetch_with_retry` takes `sleep` as a keyword whose default is `time.sleep`,
bound when the module is imported, so a monkeypatch of `time.sleep` never
reaches it. The ladder retries any exception except `ListingNotPaginated` and
a Cratekit refusal whose cause says `retryable=False`, deliberately, so a fake
failure of any other type is taken for transient.

## What to do

- Bind the sleep through the caller that hands its keywords down to the
  ladder, and keep the real function: wrap it with
  `kwargs.setdefault("sleep", waits.append)`. `harvest.playlist_tracks` is
  that caller for a playlist read (`ladder_waits` in
  `tests/test_sync_twins.py`), `crawl.releases` for the label crawl
  (`_ladder_without_waiting` in `tests/test_label_workers.py`).
- Assert the recorded waits, `[1, 2, 4, 8, 16]` per reading, so the test
  proves the ladder was climbed and notices if it stops being.
- Run the new test with `--durations=5`: a time near a multiple of 31
  seconds is this trap.
