---
title: "A value planted in SQL at the restamp reaches the whitelist, because the membership step reloads the row"
date: 2026-11-25
category: database-writes
module: src/cratekit/core/rb_writer.py
problem_type: testing_gap
component: testing_framework
severity: high
root_cause: incorrect_assumption
resolution_type: test_fix
applies_when:
  - "A test plants a value in SQL to prove a guard that reads the stored row refuses it"
  - "A mutation row on assert_created_rows_are_gridless reads zero"
symptoms:
  - "The taint test passes with the SQL read back disarmed, refused by the whitelist's in memory judge instead"
  - "The refusal names a created row declaring an analysis column, not a row carrying analysis data"
related_components:
  - pyrekordbox
  - sqlalchemy
tags:
  - gridless
  - read-back
  - identity-map
  - mutation-zero
  - r2072
---

# A value planted in SQL at the restamp reaches the whitelist, because the membership step reloads the row

## Context

The guarded commit judges a new content row twice before it commits: the
whitelist's in memory judge (`guard_violations`, fed by `_declared_columns`,
which reads the instance dictionary) and the SQL read back
(`assert_created_rows_are_gridless`). A test that means to prove the read
back plants its value by SQL, so the object never carries it. R-2072 found
that test passing with the read back disarmed (r746-a G7, r746-d G5 read
zero on the full suite).

## The cause

The binding's `add_content` flushes the new row and leaves every column it
did not set unloaded. A value written by SQL at `native._restamp` is not in
the object then. But the membership step, `rb_writer.add_memberships`, calls
the binding's `add_to_playlist`, which asks for the row with `get_content`;
the query refreshes every unloaded column of the instance already in the
identity map, the planted one with it. By the guarded commit the object
carries the value, and the whitelist refuses it first. Traced with a
`refresh` listener on the content class.

## What works

Plant where nothing reads the row again: wrap `rb_writer.commit_guarded` in
the test, write the value by SQL on the disposable copy, then call the real
commit. Assert the read back's own wording and the absence of the
whitelist's, not merely the reason, which both layers share: a later read
added between the plant and the judge then fails the test instead of quietly
handing the kill to another layer. An assertion on the object's dictionary
right after the plant proves nothing, since an SQL write never sets it:
`test_an_analysis_value_only_the_stored_row_holds_is_refused_by_the_read_back`
in `tests/test_intake_land_native.py`.

## The general rule

Two layers that refuse with the same reason cannot be told apart by the
reason. A test written for one layer asserts that layer's own words and the
precondition that keeps the other layer blind, or it is covered by nothing
the day the order of reads changes.
