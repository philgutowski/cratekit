---
title: "Two behaviour captures of one commit differ until everything Python reads is pinned and everything the operating system gives is named"
date: 2026-11-21
category: workflow-issues
module: "scripts/behaviour_compare.py, tests/behaviour"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: incorrect_assumption
resolution_type: workflow_improvement
applies_when:
  - "tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal fails after a scenario was added under tests/behaviour"
  - "behaviour_compare.py compare prints a difference between two captures of the same commit"
  - "A scenario's verb writes an id, a time, a duration, an inode or a process id"
tags:
  - behaviour-comparison
  - determinism
  - clock
  - capture
  - refactor
---

## What it looks like

A new scenario passes, and the equality test fails, or `compare` shows a
difference between two captures of one tree. The diff it prints is the
answer: it names the command, the file or the row, and the value that moved.

## What made the six shipped scenarios differ, in the order it was found

Each of these looked like the last one.

1. **Run and job ids.** `secrets.token_hex`, pinned to a counted sequence, so
   the nth id of a scenario is always the same. Counted, not constant: ids
   must stay distinct. A change that mints one more id therefore shifts
   every id after it, which is a difference to explain and not noise.
2. **The clock.** `datetime` and `date` are replaced by classes whose `now`
   answers one instant and whose constructor returns the real type, in the
   standard library's module and in every loaded module that already held
   the name. `time.time` likewise.
3. **A new rekordbox row's id.** The binding draws it from
   `secrets.token_bytes`, not `uuid4`.
4. **The binding's row stamps.** Its tables declare `default=datetime.now`,
   the real class's method bound at import, which no patch of a name
   reaches. The column defaults are re-pointed where the schema holds them.
5. **Durations.** `time.monotonic` and `time.perf_counter` stand still, so a
   measured duration is zero. A wait that would have timed out never does;
   the capture's own timeout ends it.
6. **A file's times.** A gate says how long a run has stood open by its
   record's last write. The clock is pinned and the disk's is not, so every
   file under the scenario's directory is set to the pinned instant between
   commands.
7. **The process id and start, and a landed file's inode.** These cannot be
   pinned without changing the code under test. Each capture records its
   own, and `compare` reads past them only where each side holds its own
   word, whole, at the same place.
8. **The fixture database's schema.** The suite's own builder writes each
   table's foreign keys in an order that changes per process, which the
   schema comparison found on its first run. The dump reads a table's
   constraints in one order.

## What to do

Read the diff, find which of the eight it is, and if it is a ninth, pin it
where Python reads it or record it as a capture's own word, in the stage
(`tests/behaviour/__init__.py`) and never in the scenario. A pinned name asks
whether the pins are on each time it is called, so a reference that outlives
the scenario is the real thing again. Do not scrub a capture: what it holds
is what the commands printed and wrote. A file's own times read back inside
the command that wrote it, and its change time, are not held still, and no
shipped scenario records one.
