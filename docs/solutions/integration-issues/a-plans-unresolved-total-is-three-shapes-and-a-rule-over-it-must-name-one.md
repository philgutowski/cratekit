---
title: A plan's unresolved total folds three shapes, and a majority rule written over it must name which one it reads
date: 2026-09-22
category: integration-issues
module: "src/cratekit/write/metadata_cli.py, src/cratekit/cli/doctor.py, src/cratekit/cli/setup.py, src/cratekit/core/rb_writer.py"
problem_type: integration_issue
component: recorded_path_resolution
root_cause: wrong_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A brief defines a refusal as a ratio over a plan's unresolved total, and the sitting's numbers make the ratio look exact"
  - "The refusal, written literally, turns every existing drive over the shared two row fixture into a failure, because the fixture's rows carry no path"
  - "A refusal that tells a person to add a prefix rule fires over a library of streaming rows or of deleted files, where a rule fixes nothing"
applies_when:
  - "A guard is being written over a count that a plan reports as unresolved, skipped, or missing"
  - "The count was measured on one library where every member happened to be the same shape"
  - "A diagnostic wants to read the database and the live path is off limits"
tags:
  - "locations"
  - "prefix-map"
  - "unmapped"
  - "mytags"
  - "doctor"
  - "disposable-copy"
  - "r372"
---

# A plan's unresolved total folds three shapes

## Context

R-372: the first real My Tags plan reported `count 0, active 9937, unresolved
9937`, outcome ok, over a library whose rows record a renamed drive and whose
prefix map was empty. The brief asked for a refusal when `unresolved * 2 >
active`, and for a doctor check reading "the same ratio".

## What the number hides

`plan_mytags` counted a row as unresolved whenever it could not read a file for
it, and that is three different rows:

- **no recorded path**, a streaming row, and the two rows of the shared
  disposable fixture that every conformance drive runs over;
- **a path under no rule**, the renamed drive, the shape R-372 is about;
- **a mapped path whose file is gone**, which is the deletion pass's question.

On the sitting's library all 9937 were the second shape, so the ratio over the
total and the ratio over the second shape were the same number, and the brief
was written from that number. Written literally, the rule refused the
conformance drives of the My Tags verb over a fixture with two pathless rows,
which is the fixture saying what the rule would ask of every library with a
handful of streaming rows and a lot of deleted files: a refusal whose step,
"add a prefix rule", cannot help.

## The rule that landed

The survey counts `unmapped`, rows whose recorded path resolved
`Resolution.UNMAPPED`, beside the unchanged `unresolved` total, and the majority
rule reads `unmapped`. The plan's totals show both, so a person sees the
breakdown. The refusal groups unmapped rows by `locations.leading_prefix`, which
is what that function was written for, and names the drive rather than the
rows.

**When a brief's ratio is defined over a total, ask what shapes the total
folds, and whether the remedy the refusal carries fixes every one of them.** A
rule whose remedy fixes one shape reads that shape.

## Also true at this seam

- **A diagnostic reads the database off a copy, and the copy is taken only
  under a closed application.** `rb_writer.read_only_copy` is the one site of
  copy, open the copy, close, remove, and it asserts rekordbox closed first,
  because a copy taken under the live application is torn the way a backup is:
  it opens, and is missing whatever was mid write. Doctor asks the same
  question first through its process seam so a torn copy's open failure is
  never forwarded as a refusal naming a snapshot restore.
- **A check that copies the database asks the volume checks before it reads.**
  A leftover mount point holding a stale database is the first state
  `core/preflight` tells apart, and a survey over it is a report on a disk
  nobody is using. `_library_state_unreadable` comes before the survey, the
  order the taxonomy check already uses.
- **The wizard's offer is read against the configured root, not only against
  the other column.** `BaseDBDrive` equal to `CurrentDBDrive` is not "no rule
  needed": a drive renamed before rekordbox was next opened records the old
  name twice while the person has configured the new root. A root already
  under the base drive is the case that needs nothing, and a target that is
  the root is written as `{library.root}` so the rule survives a remount.
- **A guard layer beneath another guard measures zero unless the test names the
  upper layer's own sentence.** The wizard's process question sits over the
  copy's own assertion; a test that looked for "running" passed through
  either. The test asks for the wizard's wording, and the composite row removes
  both.

## Still open

R-654, each diagnostic copies the whole file set and setup does it twice.
R-655, an offered rule with a literal target carries no volume identity.
