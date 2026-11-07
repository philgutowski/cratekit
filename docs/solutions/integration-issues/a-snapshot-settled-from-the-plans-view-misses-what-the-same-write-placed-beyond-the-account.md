---
title: A snapshot settled from the plan's view misses what the same write placed beyond what the account holds
date: 2026-11-07
category: integration-issues
module: src/cratekit/modules/outbound/mirror_edits.py, src/cratekit/organize/mirror_edits.py, src/cratekit/modules/outbound/ledger.py
problem_type: integration_issue
component: tooling
severity: high
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "A mirror-edits write places a track somewhere the account edit did not name"
  - "An edit rule compares rekordbox's side with a snapshot the library step settled"
  - "A second account edit to the same track lands before the next organize"
tags:
  - mirror-edits
  - favourites
  - snapshot
  - account-mirror
  - organize
---

# A snapshot settled from the plan's view misses what the same write placed beyond what the account holds

## Problem

Sitting 88 (A90, U236): a track put in `All Favorites` on the account was
carried by organize into All Favorites and its month in rekordbox. The account
then took it off All Favorites, and the next organize kept the favourite,
"placed in the favourites in rekordbox since: an addition beats a removal".

## Cause

A carried edit settles each playlist where both sides will agree after the
write (`Decision.settle`, from the plan's reading). The FAVOURITE's month is
the library's choice, made at the write (`placeholders.month_label` of the
account's added time), so at the plan neither side holds it there and the month
is settled WITHOUT the track. The account area was planned before the write
(R-1029), so the account's month never gets it that run. Every later reading
then sees rekordbox holding the track in a month the snapshot lacks, which is
exactly what a person's addition in rekordbox looks like.

## What was done

The write records the month it placed as the library's own placement, by the
month's account title on the mirrored folder's ledger record (`placed`), so a
month the write made and no mirror record holds yet is covered too. The
Favorites rule never counts a placed month as an addition in rekordbox. A
placement is dropped when a settle gives the track its word on that title, or
when the mirror finishes the playlist with no hold on the track
(`mirror_edits.placed_after`), so a person's later addition is read as theirs.
The frozen mirror plan carries placements beside the snapshot (U222).

## The rule

When a library step writes anything an account edit did not name, ask what
the next reading of that playlist will make of it. A snapshot can only record
what both sides hold; what the library alone wrote needs its own record, or it
reads as a person's change in rekordbox on every run until the mirror catches
up, and a second account edit in that window is decided against it.
