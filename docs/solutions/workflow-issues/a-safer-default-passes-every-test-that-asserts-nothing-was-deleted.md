---
title: A safer default passes every test that asserts nothing was deleted
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/modules/tools/backup.py"
problem_type: workflow_issue
component: archive_rotation
root_cause: vacuous_negative_assertion
resolution_type: test_fix
severity: medium
symptoms:
  - "A change makes a deleting path delete nothing under some starting state, and that state is the one every fixture starts in"
  - "Tests that assert a deletion HAPPENED fail and get fixed, which looks like the whole of the fallout"
  - "Tests that assert a deletion did NOT happen keep passing, and now pass whether or not their guard exists"
applies_when:
  - "A fix adds a conservative default to code that deletes, purges, prunes or overwrites"
  - "Existing tests prove a rehearsal, a failed step or a refusal suppresses that deletion by asserting its absence"
  - "The fixtures those tests use do not set up the state the new default needs before it will delete anything"
tags:
  - "backup"
  - "rotation"
  - "mutation"
  - "vacuous-test"
  - "dry-run"
  - "r222"
---

# A safer default passes every test that asserts nothing was deleted

## What happened

The archive rotation used to purge all but the newest dated folder. To stop a
retried mirror purging its failed attempt's archive, it now purges only folders
older than the last COMPLETED mirror on record, and with no record it purges
nothing.

Four tests failed at once, the ones asserting that a purge happened. They were
the visible fallout and were fixed by starting them from a recorded mirror.

The fallout that did not show was the other direction. Two tests prove a
rehearsal never purges, by asserting that no purge command was issued. Their
fixtures record no completed mirror. After the change the engine purges nothing
in that state for anyone, so both tests passed with `purge=not dry_run` in place
and would have passed with it removed. A green suite said the rehearsal guard
was covered on the day it stopped being covered.

A first cut made this worse by design. It passed the floor in from the caller as
`None` for a rehearsal, which made two layers stand between a rehearsal and a
purge. METHOD's driver rule says a guard covered by another guard is a guard
nothing covers, and that is what the second layer did to the first.

## The rule

After making a deleting path more conservative, grep the tests for assertions of
ABSENCE on that path, `not in recorder.labels()`, `purged == []`, and ask of
each one whether the deletion it rules out could still have happened in its
fixture. If not, give the fixture the state the deletion needs, so the test
fails when its guard is removed.

Then measure it rather than argue it. The mutation row `A9_rehearsal_purges` in
`docs/mutation/r222-a.md` reverts the existing rehearsal guard and kills five.
The same row against the fixtures as they were was NOT run, so that it would
have killed none is the reasoning above and not a measurement.

## Where the floor is read

The floor is read inside `_prune_archive`, below the rehearsal's return, and not
passed in. That keeps `purge` the one thing between a rehearsal and a deletion,
and it means a preview never opens the record at all.
