---
title: A restore that brings analysis files back is refused by the watch over its own session
date: 2026-09-20
category: integration-issues
module: "src/cratekit/modules/tools/backup.py, src/cratekit/session/restore_cli.py, src/cratekit/core/analysis_store.py, src/cratekit/core/session.py"
problem_type: integration_issue
component: restore
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A restore transfers everything, every return code is zero, and the verb still ends refused as moved analysis files"
  - "The refusal arrives after the database has already been replaced, and its remedy is to restore from a snapshot"
  - "Every test of the new transfer is green, because every fake runner answers a return code and writes no file"
  - "In the outside layout the transfer lands under the library root, where the database also lands, and rekordbox reads neither"
applies_when:
  - "A unit adds a transfer to backup.plan_restore, or anything else that puts files under the library root or the analysis share"
  - "A restore engine is tested with a runner that records commands and returns zero"
  - "A plan is built in modules/tools/backup.py and spent inside restore_cli's recovery session"
related_components:
  - "beat_grid_protection"
  - "analysis_watch"
  - "testing_framework"
tags:
  - "analysis-watch"
  - "beat-grid"
  - "restore"
  - "analysis-share"
  - "fake-runner"
  - "green-suite"
  - "r338"
---

# A restore that brings analysis files back is refused by the watch over its own session

## Context

R-338 added the analysis share to the backup. In rekordbox's default layout the
database sits outside the library root, the `share` folder beside it holds every
beat grid, and no backup carried it. The capture half was simple. The restore
half planned one more transfer in `backup.plan_restore`, a copy of the share to
`share` beside wherever the database lands, and every test of it passed.

The built in review read one file further than the tests did. The engine lives
in `modules/tools/backup.py` and knows nothing about sessions. Its one caller,
`restore_cli.restore_under_one_session`, spends the plan INSIDE
`restore.recovery_session(analysis_roots=analysis_store.watch_roots(cfg))`. That
watch fingerprints every analysis file under the library root and the live
share when the session opens, compares when it closes, and counts a file that
APPEARED as drift. A restore of the share makes thousands of them appear.

Driven, it did exactly that: the database transfer ran, the share transfer ran,
every return code was zero, and the session closed refused as moved analysis
files, after the database had been replaced.

## Why the suite could not see it

Every restore test in this repository injects a runner that records the command
and returns a `CommandResult`. None of them writes a file. The analysis watch
compares files, so under those runners it has nothing to compare and closes
clean whatever was planned. The transfer was tested. Its effect never existed.

The test that catches it uses the REAL session and a runner that writes one
`ANLZ0000.DAT` where the transfer is aimed.
`tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
is that test.

## What was done, and what was not

The engine asks `analysis_store.is_watched(cfg, landing)` before it plans the
transfer. A landing place the watch covers is WITHHELD, the plan and the totals
say so in one word, and the remote is not asked about a share it will not pull.
The share comes back through `--target`, which lands outside both watched roots.

That steps around the conflict and does not resolve it. The same refusal is on
`main` for the contained layout: `restore run --from-backup --include-mirror`
ends refused whenever the mirror brings back a grid the volume lacks, which is
the partial recovery the flag exists for. That is R-606, and the fix it needs is
in the watch, an exemption for what the session's own planned transfers wrote.

The same drive surfaced R-605, which is older and worse: in the outside layout
a live restore lands the database at `<library root>/master.db`, a file
rekordbox never reads, and reports it restored.

## The general rule

A plan built in one module and spent inside another module's guard has to be
tested inside that guard, with a fake that produces the EFFECT the guard
measures and not only the return code the engine reads. For anything that
touches a path, ask what is watching that path before asking whether the
command is spelled correctly.

## See also

- `docs/solutions/integration-issues/a-guard-that-refuses-an-empty-list-cannot-see-a-barren-one.md`,
  the same watch, met from the other side: armed over a root that holds no grid.
- R-338, R-605 and R-606 in `docs/residual-findings.md`.
