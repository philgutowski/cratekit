---
title: "unmapped-genre only means a deliberate decline on a catch-all string, so a tag alias verb cannot answer it"
date: 2026-09-21
category: workflow-issues
module: "src/cratekit/.../searchers.py, core routing.suggest_tag, taxonomy loader, tests/test_tag_workers.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: inadequate_documentation
resolution_type: documentation_update
applies_when:
  - "A brief or ledger entry (R-247) says an unmapped source genre needs somewhere to become an alias"
  - "A test reports a genre as unresolved by handing a worker a fake SearchHit with genre None"
tags: [tagging, taxonomy, unmapped-genre, r-247, r-145, fixture-vs-tree, blocked-task]
---

# unmapped-genre only means a deliberate decline on a catch-all string

## Problem

Relay task 170 (R-247) was briefed to add a verb that writes an alias for an unmapped source genre. It blocked, with nothing committed, because the premise does not hold on the tree.

## Cause

The premise was read and never driven. Driving `searchers._resolved` against `taxonomy.default_taxonomy()`:

- A word the taxonomy has never heard of (`gqom`, `footwork`) is written to the file raw. `suggest_tag`'s last tier passes an unknown string through, so it is never reported `unmapped-genre`.
- `unmapped-genre` comes from exactly fourteen catch-all strings. Five are exact `decline = "ask"` rules (`Techno`, `Electronica`, `Electronic`, `Electronica / Other`, `Other`). Nine are routing aliases of the fallback bucket (`Acapella`, `DJ Tools / Acapellas`, `DJ Tools / Samples`, `Electro`, `Electro (Classic / Detroit / Modern)`, `Experimental`, `Live Electronic`, `Loop Samples`, `Mainstage`).
- A tag alias cannot answer either class. Exact refusals run before `tagging_alias`, so the alias would be written and never read. `_build_alias_indexes` also indexes a bucket's routing aliases for tagging, so a tag alias on another bucket fails the load with "claimed by both". Changing either rule in core recreates the blanket genre bug the `[fallback]` block exists to prevent.
- Every verb loads the packaged template. The library's own taxonomy copy is read only by doctor (R-145, open), so an alias written there changes nothing yet.
- The R24 test in `tests/test_tag_workers.py` hides all this by using a fake `SearchHit` with `genre=None` for `gqom`, which the shipped searcher cannot produce. `_bandcamp_tag`'s docstring carries the same wrong belief.

## Next time

- Before building on a brief marked read and not driven, run the string through the real resolver. A one minute script settled what an hour of reading assumed.
- The consistent fix is R-247's first closing arm, `tag folder` offering each decline into `review.Queue.GENRE`, answered per file. That is a product decision reserved for Phillip. Options A, B and C are in the comment on card 170.
- Owed regardless: correct R-247's text to name the fourteen strings, and rebuild the R24 test on a string the shipped resolver really declines.

## What happened next

Both owed items are discharged. R-247's text was corrected on `groom/board-2026-09-21` and superseded by R-650, and the R24 test in `tests/test_tag_workers.py` now spends `Techno` and `Electronic`, two strings the shipped resolver really declines, rather than `gqom` and `footwork`, which it writes.

R-650 itself was built on 2026-09-21, issue #189: the last tier now sets `off_taxonomy`, the sweep counts the distinct strings and warns. Its build found that "no bucket" identifies nothing, because the shipped template declares `Melodic Techno` as a rule with a literal tag and no bucket, and that the suppression must ask routing's question rather than the vocabulary's. That is filed beside this one as `a-suppression-rule-must-ask-the-question-that-decides-the-outcome.md`.

## Since U118 and U194

The second half of the claim above is stale. U118 let a bucket's tagging only alias win over another bucket's routing alias, so a tag alias of `Electro` on Afro House now loads and tags `Electro` as Afro House; the "claimed by both" refusal still holds for two routing aliases. U194's review drove it on 2026-11-02. The exact `decline` rules still run ahead of every alias, so for those five words the claim stands. `crate taxonomy alias` refuses both classes all the same, as its brief asked: a word the copy declares a catch-all stays one unless a person edits the copy by hand, and the refusal now says that rather than that no alias could answer it.
