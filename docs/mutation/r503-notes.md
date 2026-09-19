# R-503 mutation table, summary

The author's own table, run with `scripts/mutate.py` on `relay/184`,
2026-09-19, after the code review's fix round. Every zero below reads "the
author could not kill it" and nothing stronger. Full rows are in `r503-a.md`
and `r503-b.md`, with the row data beside them.

Twenty one rows in two batches, split so each driver run finished inside one
foreground call: nineteen over this unit's new guards and two over existing
guards of the same verb. Under the cap of 25, so nothing was dropped.

| Row | Guard | Surface | Deaths |
| --- | --- | --- | --- |
| G1 | the review lookup of offered rows | user | 7 |
| G2 | only an item with a verdict is answered | user | 1 |
| G3 | a blank `review_item` is no item | maintainer | 0 |
| G4 | an answered row leaves the offered count | user | 5 |
| G5 | an answered row is counted under its word now | user | 3 |
| G6 | an answered row is counted under `answered_*` | user | 5 |
| G7 | an answered row is not counted under `since` | user | 5 |
| G8 | a rejected row missing now is kept and listed | user | 4 |
| G9 | answered rows keep their playlist order | user | 2 |
| G10 | an answered row now owned is `answered_owned` | user | 75 |
| G11 | the `answered_*` counts in the summary | user | 5 |
| G12 | the answered check's breakdown | user | 2 |
| G13 | the offered check routes back to this listing | user | 1 |
| G14 | the refusal names what the earlier list holds and this does not | user | 2 |
| G15 | the refusal names what this list holds and the earlier does not | user | 1 |
| G16 | an earlier file that is not JSON gives no reason | user | 2 |
| G17 | the refusal hint read from the earlier file | user | 3 |
| G18 | the two lists compared by provider identifier | maintainer | 0 |
| G19 | the review store opened only for an offered row | maintainer | 0 |
| E1 | existing: the consult reads a person's answer back | user | 7 |
| E2 | existing: an unanswered row is not asked again | user | 1 |

**G10, 75.** Filing two states under one key leaves `answered_owned` out of the
counts, and the answered check reads it on every listing, so every listing
raises. Loud, and a real death.

**E2's description in the rows file overstates the mutation.** Asking every
offered row again does not list it: an unanswered row comes back from the
consult as a question and stays offered. What E2 measures is that an
unanswered row is not asked again, and the one death is the test that takes
the library away under a job whose only question nobody answered.

**G3, zero, maintainer facing.** Every report the worker has committed since
U57 names its review item, so a blank key comes from no producer this
session drove, and `review.find` over a blank identifier answers no item
anyway.

**G18, zero, maintainer facing.** Every fixture track has a distinct name and a
distinct identifier, so comparing by either tells the same story. It diverges
only for two tracks sharing an artist and a title, and there it changes a hint
on a refusal, not what is written.

**G19, zero, maintainer facing.** Opening the store for a job with no offered
row costs one open and changes nothing a person reads.
