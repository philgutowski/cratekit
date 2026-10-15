---
title: An account step that reads the rekordbox tree lags the database area's writes of the same organize run
date: 2026-10-15
category: integration-issues
module: src/cratekit/organize/cli.py, src/cratekit/organize/account_mirror.py
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: documentation_update
tags: [organize, account-mirror, gate, digest, ordering]
applies_when:
  - "A step of crate organize's account area reads anything the database area writes"
  - "A test asserts that a second organize run after a full apply plans nothing"
  - "A brief says a refresh keeps the account equal to rekordbox on every sitting"
---

# An account step that reads the rekordbox tree lags the database area's writes of the same organize run

## Problem

U147 added the account mirror, a step of the account area that copies every
genre folder of the routing tree onto the account. The suite's
`test_a_second_run_after_a_full_apply_plans_nothing` failed on the first
battery: after a full approved run, the second run planned mirror steps again,
creating playlists such as `Deep House Unsorted` that the first run's adoption
had just made in rekordbox.

## Cause

`crate organize` runs plan, ask, write (`organize/cli.py`). Both areas are
planned before either gate is asked, and each gate binds its answer to the
digest of the plan it showed. So the mirror is planned from the tree as it was
BEFORE the database area's adoption and filing wrote to it, and those writes
reach the account one organize run later. Re-planning the mirror after the
database apply would write something no gate showed, which is the one thing
the digest exists to refuse.

## What was done

Nothing in the ordering, deliberately. The test now says the second run plans
only mirror steps and the third plans nothing, and the lag is a residual with
its options (a second account gate after the database apply, or a mirror only
rerun at the end of a sitting). A live sitting that wants the account current
runs `crate organize --only mirror` once more after the full run.

## The rule

Before adding an account step, ask whether it reads anything the database
area writes. If it does, it lags one run, and the brief's "a second run plans
nothing" holds only for a run whose database area wrote nothing.
