# U102 mutation pass, notes

Issue #147, branch `relay/147`, 2026-09-20. Two tables, `u102-a.md` and
`u102-b.md`, rows files beside each. **Twenty five rows, all twenty five
killed, no zero.** The author's own table and no independent one, which METHOD
requires to be said here rather than implied: every number below is what the
author could kill, not what is killable.

Two tables rather than one to stay inside the harness tool ceiling, each run in
the foreground and waited on, with nothing else touching the tree. Both
baselines were green at 9542 collected. Every row reports `head_verified` true
and `git status` showed no source file changed after either run.

**Every row names its subset.** No test file imports `intake/repair_cli.py`,
because the tests drive the verb through the real dispatcher, so the derived
subset would have been empty and every row would have promoted to a full suite
run. The subset is `tests/intake/test_repair_apply.py`, with
`tests/intake/test_repair.py` added for the two rows in `intake/repair.py`.
Since every row died on the subset, none was promoted.

**The cap was reached and six rows were dropped for it**, logged at the foot of
each rows file with the reason each ranked below the cap: a stored path that is
not text, the reader taking one page, an `OSError` from the claim escaping, an
unusable item not counted as owed, the confirm gate dropped from the entry, and
the apply digest built without its marker.

## The shape of the pass

Batch A, thirteen rows. Two in the reader: `keep` read as accepted, and an
undecided item read as accepted. Five on a proposed name, which comes out of a
store that can be imported from an edited document: no stored path, a name with
a separator in it, an empty name, a changed extension, and a linked file whose
stored path is the link's target. Three on `--root`: the separator dropped from
the prefix test, the casefold dropped, and the filter ignored. Three on the
plan's classes: an unchanged proposal planned as a rename, a missing file
planned again, and a missing file always worded as a rename already carried
out.

Batch B, twelve rows. The collection guard removed from the plan, removed after
the gate, and the second read removed, each alone, since a guard covered by
another guard is a guard nothing covers. The plan's collision detection
removed, the atomic claim removed, the abort answer ignored. Then the R-172
hazard from three sides: a referenced file not counted as owed, a collision not
counted as owed, which is R-172 itself, and the post gate missing file check
removed. Then `retryable` from both sides, and the claim left behind.

## What four rows needed first

Four guards had no test when the rows were drafted, and a row over an untested
guard measures the absence of a test and nothing about the guard: the item with
no stored path, the claim, the post gate missing file check and the claim's
`OSError`. Four tests were written first and committed separately. The two race
tests stand on the verb's second collection read, which is the one moment
between the plan and the rename a test can occupy the way another process
would, so G5 and G9 each die on a file that really appears or really vanishes
rather than on a stubbed answer.
