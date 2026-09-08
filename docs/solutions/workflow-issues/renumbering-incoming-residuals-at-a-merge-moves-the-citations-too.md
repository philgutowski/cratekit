---
title: "Renumbering an incoming branch's residuals at a merge moves every citation of them, and the citations live in entries the branch only amended"
date: 2026-09-07
category: workflow-issues
module: "docs/residual-findings.md, docs/METHOD.md, RESTART-cratekit.md"
problem_type: workflow_issue
component: documentation
severity: medium
root_cause: incomplete_procedure
resolution_type: workflow_improvement
applies_when:
  - "a branch that filed residuals is being merged after main's highest number moved past the numbers it used"
  - "a residual entry on the branch cites another residual filed on the same branch"
  - "the branch amended an existing entry on main and the amendment cites a branch number"
tags:
  - residuals
  - merge
  - renumbering
  - append-only
---

# Renumbering incoming residuals moves the citations too

## The rule as METHOD states it

Residual numbers are append only. At a merge, the numbers on `main` never
move, and the incoming branch's residuals take fresh numbers above `main`'s
current highest. METHOD gives two greps to verify a merge: no duplicate
headings, and no heading deleted against `origin/main`.

## What the two greps do not see

Both greps look at headings. A residual number also appears in three other
places, and none of them is a heading:

1. **Inside another incoming entry.** U52's branch filed R-235 through R-242.
   Its R-240 said "R-236 is the only thing standing between these
   declarations and being true", and its R-241 said "R-238 records the
   `IncrementResult` half of the same split". After renumbering the headings
   to R-257 through R-264, both sentences pointed at main's R-236 and R-238,
   which are U55's entries about adoption. Wrong entry, right looking number.
2. **Inside an entry on main that the branch amended.** The branch added dated
   paragraphs to R-137 and R-139, and each paragraph cited a branch number:
   "That is R-237, filed separately" and "R-236 records that gap". Those
   lines auto merged without conflict, because they were additions to text
   main had not touched, so the merge resolution never showed them.
3. **In the branch's plan and RESTART**, which say what the numbering was at
   branch time. The plan is a closed record and can carry a parenthesis; the
   RESTART is rewritten anyway.

The first two are the trap. A heading grep is clean, the battery is green, and
two amendments on main now cite entries about a different unit.

## The procedure that closes it

After renumbering the incoming headings, run one grep over the WHOLE file for
every number in the incoming range, excluding the headings, and read each hit:

    grep -n "R-23[5-9]\b\|R-24[0-2]\b" docs/residual-findings.md | grep -v "^[0-9]*:## R-"

Every hit is one of three things: a citation of the incoming entry (repoint
it), a citation of main's entry with the same number (leave it, and there will
be some, because main's numbers are real entries), or a citation in a
`docs/history/` file (leave it, history is not instruction). Telling the first
two apart is a read of the sentence, not a pattern, because "R-236" in a
paragraph dated 2026-09-02 about labels is the branch's and "R-236" in a
paragraph about a cutover is main's.

Do the renumbering with a mapping applied ONLY to the incoming block's lines
and to the hits the grep identified as the branch's, never to the whole file.
A whole file substitution renumbers main's own citations of its own entries.

## Why this is worth an entry

It cost nothing this time because the grep was run before the commit. It
would have cost a later session a wrong pointer that reads as a right one: an
entry saying "R-258 records that gap" is only checkable by opening R-258, and
nothing in the suite opens it. `tests/modules/test_reports.py` bans a unit's
own residual numbers from files it did not write, which is a different check
and does not see this.

## Related

- `docs/METHOD.md`, "Committing and merging", the append only rule and its
  two greps. This entry is the third check.
- The U52 merge commit on `relay/70`, which carried out the repointing and
  names both amended entries.
