---
title: "A containment check admits the authorised directory itself, and the operation it guards then reaches that directory's parent"
date: 2026-09-20
category: integration-issues
module: "src/cratekit/core/restore.py, tests/test_restore.py, docs/mutation/u95-c-rows.toml"
problem_type: integration_issue
component: restore
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A guard answers whether a path is inside an authorised directory, and a new write location is being put behind it"
  - "The guarded operation stages, prunes, renames or creates beside its target rather than only at it"
  - "A value type, a plan or a job, carries a path that was derived at build time and is trusted at run time"
  - "A path is derived from a session or a token so that, by construction, it cannot be wrong"
symptoms:
  - "A check of the form equal to the root or under the root passes for the root itself"
  - "A cleanup step takes the PARENT of a checked path, so authorising the path authorised nothing about what is deleted"
  - "A plan side guard kills zero tests, because no honest derivation can produce the input it refuses"
tags: [restore, authorisation, path-containment, staging, prune, mutation-table, plan-as-value]
---

# A containment check admits the directory itself, and the operation reaches its parent

## What happened

U95 made a bare metal recovery session spendable by deriving every path in
`restore.plan` and `restore.run` from `Held.authorises`. The unit added one
guard, that every location a plan writes at is authorised by the session, and
extended it to the companion staging directory, which is a write location the
per step check had never covered because it is not a step target.

The built in review found that the extension was not enough. `Held.authorises_path`
answers "equal to the authorised directory, or under it", which is the right
question for a file about to be replaced. It is the wrong question for the
staging directory, for a reason that is not in the check at all: the restore's
closing step calls `_prune_staged_companions(pre_restore_root.parent)`, and that
function deletes directories. A plan value whose staging directory was the
library root passed authorisation, and the prune was then handed the directory
ABOVE the library, whose other entries are the machine's other volumes. The same
shape applies to a step whose target is the root: replacing a directory stages
beside it, one level above anything the session was asked about.

## The rule

**Authorising a path says nothing about what the operation does to the path's
parent. For each write location behind a containment check, write down every
path the operation touches, and if any of them is a parent, the check has to be
an exact derivation rather than a containment.**

Here that meant two re-derivations from the rooted configuration, both asked at
plan time and again at run time because a plan is a value:

- the staging directory must sit DIRECTLY under the one staging store the
  configuration derives, `pre_restore_root.parent == _pre_restore_root(cfg).parent`;
- every step target must be a member of `restorable_targets(cfg)`, derived again
  rather than trusted from plan time, which excludes the root itself.

## The second trap, found by the mutation table

Once every path derives from the session, no argument a caller can pass makes
`plan` produce an outside path. That is the design working, and it means the
plan side copy of the guard has nothing to kill it: removing it left the suite
green. The fix is not to delete the plan side check, because a preview must
refuse as loudly as a write. It is to force the derivation wrong through its
seam, `monkeypatch.setattr(restore, "_pre_restore_root", ...)`, which is what a
later edit to that derivation would amount to. A guard against an input that is
impossible today is a guard against tomorrow's edit, and it needs a test that
plays the edit.

## How to check for it

`git grep -n '\.parent' src/cratekit/core/restore.py` and, for each hit on a
path that came out of a plan or a job, ask which check covered the parent. In
this file the hits that mattered were the prune and the two staged replacements.
