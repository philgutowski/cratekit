---
title: "A mutation driver can exit 0 with its last mutant still on disk, so a green battery afterwards is green on a tree nobody checked"
date: 2026-09-07
category: workflow-issues
module: "scripts/mutate.py, src/cratekit/cli/handlers.py, docs/METHOD.md"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: unverified_assumption
resolution_type: workflow_improvement
applies_when:
  - "scripts/mutate.py has just returned, whatever its exit code, and the next step is the battery or a merge"
  - "A mutation pass was resumed with --resume, or was interrupted at any point in its life"
  - "A mutation row deletes or empties a line rather than rewriting it, so its mutant is invisible at a glance"
  - "A session is about to trust a green suite it ran after a mutation pass"
  - "A driver run reported every row and printed a complete table, which reads as a clean finish"
symptoms:
  - "git status --porcelain is not empty after a driver exited with code 0"
  - "A source file's mtime sits before the driver's own table and sidecar writes, naming the driver as the last writer"
  - "A handler, registry or mapping entry is missing from src and no commit removed it"
  - "The mutation table asserts that N tests kill exactly the change now sitting in the working tree"
  - "A row's sidecar entry says head_verified true and the file still does not match HEAD"
related_components:
  - "development_workflow"
  - "testing_framework"
tags:
  - "mutation-testing"
  - "mutation-driver"
  - "silent-failure"
  - "restore-verification"
  - "method-compliance"
  - "contaminated-tree"
---
# A mutation driver can exit 0 with its last mutant still on disk, so a green battery afterwards is green on a tree nobody checked

## Context

U56 (issue #74) landed the catalogue searcher and bound the two tagging verbs to
workers, which is what takes `tag.folder` and `tag.retag` out of the R-203
population of queued verbs that declare an engine and run nothing. The binding
itself is two lines in `src/cratekit/cli/handlers.py`:

    "tag.folder": "cratekit.tagging.cli:handle",
    "tag.retag": "cratekit.tagging.retag_cli:handle",

The unit's mutation spec ends with the two rows that mutate exactly those lines,
`R39_tag_folder_unbound` and `R40_tag_retag_unbound`, each deleting its line so
the key declares no worker again. `R39` killed 10 tests and `R40` killed 13, so
the suite holds the binding well.

The pass was resumed with `--resume` from a sidecar left by a run interrupted
four days earlier, ran rows 20 through 40, printed its full forty row table and
exited with code 0.

## What happened

`git status --porcelain` after that clean exit was not empty:

    M src/cratekit/cli/handlers.py

`R40`'s mutant was still applied. The `tag.retag` binding was gone, replaced by
the blank line its deletion leaves behind. The working tree had been clean before
the run, so nothing but the driver could have written it, and the file's mtime
sat seven seconds BEFORE the driver wrote its own table and sidecar, which places
the write inside the driver's run rather than after it.

The thing to sit with is what comes next in the normal order of work. A session
finishes a pass, sees exit 0 and a complete table, runs the battery, and merges.
That battery would have been green on a tree with `tag.retag` unbound. The merge
would have shipped a verb that queues a job and never runs it, which is the exact
state the unit existed to leave, and it would have shipped it in the same commit
as a mutation table asserting that thirteen tests kill that change. Both
artifacts would be internally consistent and the repository would be wrong.

Nothing in a green suite says which tree it was green on.

## Why the source does not explain it

`scripts/mutate.py` is careful here, which is why this is worth writing down
rather than filing as a sloppy driver. It has exactly two writes to a mutation
target, and both are in one context manager:

    path.write_bytes(mutant.encode("utf-8"))
    try:
        yield path
    finally:
        path.write_bytes(snapshot)
        if head_verify:
            verify_restore(repo_root, rel)

The `finally` runs on a normal exit, on an exception and on KeyboardInterrupt.
`verify_restore` compares the file byte for byte against `git show HEAD:<path>`
and RAISES on a mismatch, and the caller re-raises `RestoreVerificationError`
rather than recording it, so a failed restore is supposed to stop the batch
loudly. The snapshot is read before the mutant is applied. Every rule
`docs/METHOD.md` asks a driver to hold, this driver holds as a property.

A two row reproduction, the same two mutations against the same file on a clean
tree, restored correctly and left the tree clean.

So: the source says this cannot happen, and it happened, and it did not
reproduce. **No mechanism is offered here.** METHOD's fourth recurring defect
pattern is a fix justified by a measurement that was never taken, and its driver
rules end with "every number was measured or the report says it was not". A
guessed cause with a confident patch is how this gets worse rather than better.

## What was not damaged, because that matters too

`R40` is the last row in the spec. The contamination therefore began after every
measurement in the table had been taken, and the table stands:

- the null control killed zero on the full 6781 test suite, so the apparatus was
  measuring correctly
- no row reported collect drift or a collect error, so no row silently lost a
  test file
- `R39` and `R40` killed 10 and 13, against an independent two row rerun's 10 and
  14 on a larger suite

A pass whose contaminated row is in the MIDDLE would be a different and much
worse finding, and the way you would know is the collected count per row, which
is why that check is not optional.

## One field that reads as more than it is

The sidecar's per row `head_verified` is set from the driver's input flag, not
from the verification's result:

    head_verified=head_verify,

It records that HEAD verification was REQUESTED. It was `true` on all forty rows
of this pass, and the tree was still contaminated. Do not read it as evidence
that the restores held.

## The rule

**After `scripts/mutate.py` returns, run `git status --porcelain` before you run
the battery, before you trust a row, and before you merge. Exit code 0 and a
complete table are not evidence the tree is clean.**

Restore with `git show HEAD:<path> > <path>`, never `git checkout`, which
discards uncommitted edits that may be the only copy of something. Verify the
restore by diffing against HEAD rather than against a copy you made, because a
contaminated copy certifies itself.

This costs one command. The failure it catches is a merge of code the repository
believes it tested.

## The check that would close it

The driver could verify every distinct target against HEAD once more after its
last row, and refuse to exit 0 otherwise. That check does not need the mechanism
to be understood, which is what makes it the right shape: it catches this
instance and every other cause of the same shape. It is the closing condition on
R-256 in `docs/residual-findings.md`.

## See also

- R-256 in `docs/residual-findings.md`, the ledger entry with the measured cost.
- `docs/mutation/u56-catalogue-searcher-and-tag-workers.md`, whose appended
  section records the observation beside the run it came from.
- `docs/solutions/workflow-issues/dismissing-a-zero-row-is-a-claim-about-the-mutated-tree.md`,
  the neighbouring lesson that a claim about a mutation must be settled on the
  mutated tree and not the unmutated one. This entry is the same principle
  applied to the tree the BATTERY runs on rather than the one a row reasons
  about.
