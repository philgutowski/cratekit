---
title: "A second producer of a record meets every reader that assumed what the first producer never did"
date: 2026-10-02
category: workflow-issues
module: "core/review.py withhold and held_offers, label/judge_cli.py, label/sweep.py list_for_label, label/held_cli.py"
problem_type: workflow_issue
component: core_logic
severity: high
root_cause: incorrect_assumption
applies_when:
  - "A record that had one producer gains a second, whose subjects have a history the first producer's never had"
  - "A table that only ever grew gains its first delete"
  - "A producer that only describes a candidate reuses a write built for a producer that files one"
tags: [label, review-queue, held-offers, withhold, ordinal, offer, refresh, sweep, r-815, r-798]
---

# A second producer of a record meets every reader that assumed what the first never did

## Problem

R-798 gave the label sweep a hold: a release the genre gate keeps out of
review, recorded in `held_offers`. The sweep was the only producer, and
every hold it made was of a release NEVER FILED.

R-815 added a second producer. `crate label judge` judges the releases
already in review and takes the misfits back into a hold. The row is the
same row. Its subject is not: it was filed once, and a person may have been
looking at it.

The first build was green. Two passes of the built in review then found
five places where code written for the first producer was wrong for the
second, and none of them was in the new verb's own logic.

## What assumed "never filed"

- **The sweep drops a hold its window does not reach once the gate would
  pass it.** Right for a release never filed: it goes back to being
  unexamined. A withheld release was in review, and dropped it was in
  neither place, with nothing said.
- **The sweep refreshes a standing hold by rewriting its payload** as the
  candidate it would file now, which names no filing run. The run the
  release was first filed under went with it.
- **`label held return` files a held release under the hold's own run.**
  Right when the hold's run is the sweep that would have filed it. The
  second producer's run is a judging job, which files nothing.
- **`label held` reads what a sweep's gate did off the stamps on the items
  it filed.** The second producer writes stamps too.

## What assumed "nothing is ever deleted"

`withhold` is the first code to delete a row from `review_items`. The next
ordinal was `MAX(ordinal) + 1` over the table, which is monotonic only
while the table never shrinks. Withhold the newest item, file another, and
the new one takes the old one's ordinal. Paging keys on the ordinal, so a
reader holding a cursor at the old highest, `review list --after`, is never
shown it. Nothing fails. The review drove it.

## What assumed "this producer files"

The first build wrote a stamp onto a release that stays through the sweep's
`offer_release`. That is `review.offer`, which rewrites an open item AND
INSERTS when the row is gone. For a producer that files, that is the point.
For one that only describes, it meant a release another judging job had
just withheld was filed again beside its own hold, and the next sweep
dropped the hold.

## The rule

When a record gains a second producer, do not start from the new producer's
code. List every reader and every other writer of the record, and for each
ask what it believes about where a row came from. Then ask the same of the
table the new producer takes rows OUT of: what did it believe while nothing
left it.

Three checks that would each have found one of these before the review did:

- Grep the table name for every `UPDATE` and `DELETE`, and read each as if
  the row had the new history.
- If the new producer is the first to delete from a table, find how that
  table allocates anything from its own contents: an ordinal, a sequence,
  a count.
- If the new producer reuses a write helper, read what that helper does
  when the row it expects is absent.

## What it looks like now

- A hold says it was taken back, `withheld_from_review` on its payload, and
  `review._put_hold` carries that word and the filing run across a refresh.
  It is the one writer of a hold row.
- The sweep leaves a withheld hold past its window standing. R-823 records
  the cost and the other option.
- `ordinal_floor`, an additive one row table, keeps the highest ordinal a
  deleted item held, and both writers that insert an item allocate past it.
- `review.redescribe` rewrites an item only while it is open and there.

## Where to look

- `src/cratekit/core/review.py`: `withhold`, `_put_hold`, `redescribe`,
  `_NEXT_ORDINAL`.
- `src/cratekit/label/sweep.py`, `list_for_label`, the loop after the walk.
- `tests/test_label_judge.py`, sections 1 and 5.
- `a-record-that-withholds-a-candidate-needs-an-exit-on-every-branch-of-the-walk-that-skips-it.md`,
  the first producer's own traps.
