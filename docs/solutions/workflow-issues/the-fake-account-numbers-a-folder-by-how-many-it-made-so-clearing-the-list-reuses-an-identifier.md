---
title: "The fake account numbers a folder by how many it made, so clearing the list reuses an identifier"
date: 2026-10-13
category: workflow-issues
module: "tests/outbound_fakes.py, tests/test_organize.py, tests/test_playlist_kinds.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: incorrect_assumption
resolution_type: test_fix
applies_when:
  - "A test makes a folder on the fake account by hand and then empties folders_created to measure what the verb makes"
  - "The verb under test then creates a folder of its own, a label's, Mine or Exports"
tags: [outbound, fake-account, folders, fixtures, organize, U142]
---

# Clearing `folders_created` on the fake account lets the next folder take a hand made one's identifier

## Problem

U142's test of a set a person had already put in `Downloaded Sets 2026` made
that folder with `held.create_folder(...)`, then called
`held.folders_created.clear()` so a later assertion could say the verb made no
folder. The plan read correctly. After the apply, a second report planned the
set as a move into its folder again, as though it were somewhere else.

## Cause

`StrictAccount.create_folder` names a new folder `folder-<n>` with
`n = len(self.folders_created) + 1`. Emptying the list resets the counter, so
the next folder the verb creates, the label's folder in the organize world,
gets the identifier the hand made folder already has and overwrites its name
in `folder_names`. The playlist placed in the hand made folder is now in a
folder called `Kompakt`, and every read after the apply sees a different
account from the one the test built. A test that only asserts on the plan, or
on `placed[...] == folder` by identifier, stays green over it.

## Next time

Do not clear `folders_created`. Take its length after the folders made by
hand and compare only the tail, `held.folders_created[made_by_hand:]`, and
assert the hand made folder still carries its name after the apply. Several
older tests in `tests/test_organize.py` and `tests/test_playlist_kinds.py`
still clear the list; they pass because they assert by identifier, and any
of them extended to read the account after an apply meets this.
