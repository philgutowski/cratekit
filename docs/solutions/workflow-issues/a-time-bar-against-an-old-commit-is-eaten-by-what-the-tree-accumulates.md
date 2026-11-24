---
title: A time bar against an old commit is eaten by what the tree accumulates, and half a parser build was argparse asking gettext
date: 2026-11-24
category: workflow-issues
module: tests/conftest.py, tests/behaviour/__init__.py, docs/mutation
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: unmeasured_shared_setup
resolution_type: tuning
applies_when:
  - A card sets out to make the suite faster than an older commit, or reads a time bar.
  - A worker's run time grows with no test to blame.
  - A test drives the crate command line in process many times.
tags:
  - suite-speed
  - argparse
  - gettext
  - mutation-tables
  - time-bar
  - u336
---

# A time bar against an old commit is eaten by what the tree accumulates, and half a parser build was argparse asking gettext

## What happened

U336 set out to make the suite 30 percent faster than at `ff8e5ec`, both timed
on one container. On its four core container `ff8e5ec` read 444 to 499
seconds over the afternoon and `main` 413 to 471, so `main` was about 10
percent faster there, against the 16.4 the audit read on another container,
and the branch landed at a ratio of 0.898. Profiling the base found where the
time goes, and most of it is not the tests' own code:

- **The mutation tables.** `docs/mutation` held 30 MB of tracked text at
  `ff8e5ec` and 223 MB at `50022274`, mostly the refactor's replay tables
  (`u325-replay-before.json` alone is 5.6 MB). Every test that reads every
  tracked file pays for them: the secret scan's equality proof, whose
  reference runs every pattern over every character, went from about 15 to
  89 seconds, and the repository scan in `tests/test_portability.py` reads
  them twice more. They are records, never rewritten, so the cost only grows.
- **The command line rebuilt per call.** A full run builds the whole crate
  parser 12,624 times, once per verb a test drives, 162 seconds summed over
  the workers, and argparse asks `gettext` for every message it formats,
  4.9 million lookups. With no catalogue `gettext` answers each with the
  message itself, but only after reading four environment variables and
  expanding the language list: 12.0 ms a build with it, 6.8 ms without.
- **The collector** still takes 22 to 50 seconds a worker after U326's
  thresholds, most of it young passes, whose cost follows the allocations,
  not the threshold.
- **Waiting.** The workers used 1,525 of the 1,796 core seconds a run gave
  them; the rest is `fsync` (66,000 calls, 53 seconds), sqlite's own syncs and
  subprocesses. Six workers instead of four read 433 seconds against about
  445, with one more failure, so oversubscribing buys nothing worth its risk.

## What to do

- **Read a time bar as a ratio**, the base and the branch each timed three
  times, interleaved, on one container (METHOD). One container drifts five to
  ten percent in an hour (the same branch read 471 and 413 seconds).
- **Measure where the time goes before cutting**: a `--durations=0` run for
  the tests, then a small plugin timing `gc.callbacks`, `cli.build_parser`,
  `ast.parse`, `os.fsync`, `time.sleep` and `Popen.communicate`, and
  `resource.getrusage` per worker for the CPU actually used.
- **argparse's lookups are answered directly in the suite.** Where
  `gettext.find` finds no catalogue, `tests/conftest.py` hands argparse
  `NullTranslations`' `gettext` and `ngettext`, one entry per configure so a
  run configured inside the run keeps the outer run's, and
  `tests/test_argparse_lookups.py` holds it to `gettext`'s answers.
- **A pytest run of your own outside `cloud_battery.py` leaves its basetemp
  under `/tmp/pytest-of-<user>`**, and the next run deletes the oldest past
  three: a whole suite's directory takes about 70 seconds to delete, inside
  that next run's time. Read timings only from runs given a fresh `TMPDIR`, as
  `cloud_battery.py` gives each run.
- **What is left is not the tests'.** The mutation tables, the parser built
  per call (a product change: make a verb's subparser only when chosen) and
  the disk waits (#702's question about memory) are each a decision, not a
  tuning; U336's residual names them.
