---
title: A match count is not a held count, so check a download list against the library by ISRC before driving it
date: 2026-09-23
category: integration-issues
module: src/cratekit/acquire/match.py, src/cratekit/intake/missing_cli.py, src/cratekit/modules/outbound/source.py
problem_type: integration_issue
component: library_index
severity: high
root_cause: identity_field_ignored
resolution_type: measurement_rule
applies_when:
  - A live intake, sync or match run reports owned, offered and missing counts and a download is the next step.
  - A residual sizes a matching gap from a sample, and the fix for one cause is about to be read as the whole answer.
  - Both sides of a comparison carry an ISRC and the comparison is made on text.
tags:
  - library-index
  - isrc
  - favourites
  - cutover
  - R-664
  - R-667
---

# A match count is not a held count, so check a download list against the library by ISRC before driving it

## Problem

Sitting 6 found the index taking the title tag with its head on, and the unit
for R-664 fixed it. The measurement that justified the fix, 96 owned, 27
offered and 83 missing, was taken with the head stripped and nothing else
changed, and the entry named a "second and narrower" artist gap of 14 rows.
Sitting 7 ran the fixed reader and got 96, 29 and 81, the numbers the unit
predicted. The next step, `intake missing --job`, then wrote 81 rows to the
download list, and 26 of them were files the library holds.

## Cause

Two things sit together here.

- The match engine compares text and never the ISRC. `recording_token` is the
  folded artist joined to the folded title, and `Owned` has no ISRC field, so
  a file whose artist tag lists every credited artist, which is every processed
  file in this library, cannot match a provider row naming the primary artist,
  whatever the title says. `BY_ISRC` in the same module searches the provider,
  not the library.
- The gap was sized from the rows one earlier sitting happened to have matched
  by ISRC, 59 of 206, and the count carried was the count inside that sample.
  Over all 206 it is 49, a quarter of the account's hearts, and the head fix
  moved rows from missing to offered as much as to owned.

The trap is the second one. A fix for the cause that was found, verified by a
number taken on the tree, still leaves the list the next verb writes untested
against the one identity both sides carry.

## What to do next time

- Before `acquire download` over any list the product wrote, walk the music
  folder by ISRC tag, about ten seconds for ten thousand files through
  `tags.read_tag(path, "isrc")`, and drop every row held under its own ISRC.
  The sitting's script is `docs/cutover.md`'s sitting 7, and the list it built
  sits beside the product's own in the lists folder.
- Report held by ISRC beside owned by match whenever a live count is written
  down. They are different measurements and the gap between them is the size
  of the matching defect.
- Size a gap over the whole population before calling it narrow. A sample one
  sitting matched for another purpose is not the population.
- Neighbours: R-664 and R-667 in `docs/residual-findings.md`; the head in the
  tag entry beside this one.
