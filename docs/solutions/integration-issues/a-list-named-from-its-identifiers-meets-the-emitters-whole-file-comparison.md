---
title: "A list named from its track identifiers alone meets the emitter's whole file comparison"
date: 2026-09-19
category: integration-issues
module: "src/cratekit/acquire/listdoc.py, src/cratekit/label/approved_cli.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "A new verb calls listdoc.write and chooses the list's name itself"
  - "The list's content can change between two runs over the same source"
symptoms:
  - "A second run refuses with 'already exists and holds something else'"
  - "The refusal repeats on every run until somebody moves a file by hand"
tags:
  - listdoc
  - idempotence
  - naming
  - labels
---

# A list named from its track identifiers alone meets the emitter's whole file comparison

## Problem

`crate label approved` has no job to name its list after, and its content moves
with the library, so U75 first named the list with a digest of the track
identifiers it listed. The unit's `/code-review` found the hole and a test drove
it red: run once with a release whose year read as none, run again after the
year is known, and the second run refuses `label-list-unusable` for ever.

## Cause

`listdoc.write` compares BOTH files byte for byte against what is already under
the name, and refuses when either differs. That is what makes an identical
repeat a no-op and what keeps it from replacing somebody's list. The manifest's
bytes carry the year, the label and the release, and the list's bytes carry the
title, the version and the ISRC. So the same identifiers do not mean the same
bytes, and a name derived from less than the emitter compares is a name that
can be asked to hold two different files.

`intake missing` does not meet this, because it names a list for a finished job
whose committed reports never change.

## What to do next time

- A caller whose content is not fixed by the thing it is named after digests
  EVERYTHING the emitter writes: `listdoc.document(rows)` for the tracks, and
  each listed id's `Provenance`. `approved_cli.list_name` is the worked example.
- The manifest records its own list's file name, so digest the provenance, not
  the encoded manifest, or the name depends on itself.
- Do not pin the digest in a test by re-deriving it. Find the one list on disk
  and pin the SHAPE of its name, then pin that the name moves when a year or a
  label moves. A re-derived digest is the module's recipe copied into its test.
