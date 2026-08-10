# U24 round 11, the author's mutation table

Scoped to this round's own diff plus a fixed sample of the unit's existing
guards, which is what METHOD asks for. 35 rows.

**Baselines.** Subset, the three test files importing the mutated modules
(`tests/test_deletion.py`, `tests/test_tombstones.py`, `tests/_pending.py`):
343 collected, 343 passed, 0 failed. Full suite: 3527 collected, 3512 passed,
0 failed.

**The collected count was checked on every row.** Every subset row collected 343
and every full row collected 3527.

**One driver defect, found and corrected, and it invalidated seven rows.** The
first pass ran children with `PATH=/usr/bin:/bin`, which drops ffmpeg, and 28
audio tests failed on every FULL run including the baseline. Every full row
therefore reported 28 and every one of those 28s was the driver rather than the
mutation. The seven rows that had gone to a full run were re-run against an
inherited environment, on a baseline of 3527 collected, 3512 passed, 0 failed.
The numbers below are the corrected ones. Subset rows were never affected: the
subset does not touch ffmpeg and its baseline was clean at 343 of 343.

**The whole table was measured twice, independently, and the two passes agree on
all 33 original rows.** That was an accident of a bad import rather than a
design, and it is reported because a reproducibility check is worth having
however it arrives.

## This round's diff

| row | the mutation | deaths | scope |
| --- | --- | --- | --- |
| R1 | the walk stops skipping what is only RAISED | 3 | subset |
| R2 | the walk stops collecting attribute chains | 8 | subset |
| R3 | the walk stops collecting bare names | 21 | subset |
| R4 | a frozenset is encoded in iteration order rather than sorted | 2 | subset |
| R5 | a compiled pattern is digested without its flags | 1 | subset |
| R6 | a compiled pattern is digested as its type rather than its pattern | 4 | subset |
| R7 | a literal is digested without its type | 1 | subset |
| R8 | a mapping is encoded in insertion order rather than sorted | **0** | full |
| R9 | the docstring is left in the digested source | 2 | subset |
| R10 | the raw source text is digested rather than the parsed form | 3 | subset |
| R11 | the parse cache is keyed by qualified name rather than by the object | **0** | full |
| R12 | the walk follows functions but not classes | 1 | subset |
| R13 | the walk does not recurse, so only the roots are read | 21 | subset |
| R14 | the walk digests code but not the vocabularies it reads | 19 | subset |
| R15 | the walk digests vocabularies but not code | 2 | subset |
| R16 | the walk stops at `cratekit.core`, so the reader one package over is foreign | 2 | subset |
| R17 | the rules are dropped from the stamp, which is the round 10 stamp | 19 | subset |
| R18 | the output probes are dropped, leaving the rules alone | 1 | subset |
| R19 | the rules are digested in walk order rather than sorted | 1 | subset |
| R20 | the stamp goes back to the `is1_` prefix | 2 | subset |
| R21 | a record with no recorded path is read as the literal word `None` | **0** | full |
| R22 | the row coordinate drops the path | **0** | full |
| R23 | the row coordinate drops the identifier | **0** | full |
| R24 | the row coordinate case-folds the path | **0** | full |
| R25 | a record naming no row raises rather than answering None | 4 | subset |
| R26 | the stamp is written but never read, so every record matches on its row | 1 | subset |
| R27 | the stamp comparison is inverted | 11 | subset |

R17 is the row that matters most: reverting to the round 10 stamp, which digests
the 23 output probes and nothing else, kills 19. Before this round it killed
nothing, because it WAS the code.

## The fixed sample of existing guards

| row | the mutation | deaths | scope |
| --- | --- | --- | --- |
| S1 | `removed_file_identity` stops stripping before testing emptiness | 4 | subset |
| S2 | `removed_file_identity` stops refusing a boolean identifier | 4 | subset |
| S3 | `removed_file_identity` composes NFD rather than NFC | **0**, then **1** | full, then subset |
| S4 | the recogniser stops checking the record's kind | 1 | subset |
| S5 | the probe set loses its last row | 1 | subset |
| S6 | a row with no identity is read as already recorded | 1 | subset |

**S3 was a zero and is not one now.** The normal form is hashed into the
identifier a decline and a review item are stored under, so it is a wire format
on other people's disks, and nothing pinned it: every existing assertion builds
both sides in one run and both sides move together. That is the same shape that
made four rounds of this branch's defect silent.
`test_the_row_identity_composes_NFC_and_the_normal_form_is_pinned` pins the
literal composed form, and re-running S3 against it kills 1. That test was added
AFTER the table, so the final collected count is 3528 rather than the 3527 every
row above was measured at, and the difference is that one test by name.

## The zero rows, each accounted for

**R8, maintainer facing, one line.** No `Mapping` constant is reachable from the
composition roots today, so the branch is unexercised rather than unguarded. It
is kept for the reason the frozenset branch exists, and the frozenset branch is
measured at R4.

**R11, maintainer facing, one line.** Keying the parse cache by qualified name
rather than by the object kills zero over five full runs, because every
replacement a test binds carries its own qualified name. The docstring on
`_PARSED` used to call the object key a guard and now says what was measured. One
earlier run of this row reported a single death in
`test_nothing_reconstructs_a_former_builds_composition_any_more`; it did not
reproduce in five subsequent full runs or in 30 runs of that test alone, so it is
recorded as unreproduced rather than as a count.

**R21, R22, R23, R24, user facing, with composites.** These are the round 10
verification's finding 2 and they are unchanged by this round.
`_row_coordinates` runs on BOTH sides of its own comparison, so any mutation that
moves both sides together is invisible. Two composites were run against the thing
it guards, which is the claim that a record is matched to the row it names:

| row | the composite | deaths | scope |
| --- | --- | --- | --- |
| C1 | the tombstone payload names a different row than the one deleted | **0** | full |
| C2 | the tombstone payload records no path for the row it names | **0** | full |

**Both composites are zero too, and that is the finding rather than an excuse
for it.** The row lookup is reachable only through a record whose stamp is not
this build's, and no test in the suite writes one except by planting it, so the
whole path is exercised by planted records whose coordinates the test also
controls. It stays a residual under the floor because nothing has shipped and no
store exists that a previous build wrote. It is recorded in
`docs/residual-findings.md` with the wider reachability this round gives it.

## How this was measured

* Driver in the scratch directory, one row at a time, file text snapshotted in
  memory and rewritten back. **The driver never invokes git.**
* Restores verified against `git show HEAD:<path>` piped to `shasum -a 256` for
  `core/tombstone.py`, which is unmodified by this round, and against the
  in-memory snapshot for `deletion/stores.py`, which is not at its `HEAD` blob
  because this round changed it. `git status --porcelain` named only the two
  files this round edits.
* `PYTHONDONTWRITEBYTECODE=1` in every child, and every `__pycache__` under `src`
  removed before the first row.
* No `-q` anywhere. The collected count and every failing node id are read from
  pytest report objects in a plugin, never from a `FAILED` line split on `" - "`.
* Every zero on the subset was promoted to a full run before being reported.
* Each anchor was checked for uniqueness before the row ran, so no row could edit
  the wrong occurrence or be a no operation.
* Rows ran synchronously, one child at a time, with nothing else touching the
  tree while they ran.

## What was ranked below the cap and dropped

The cap is 45 rows and this table is 35, so nothing was dropped for the cap.
Deliberately NOT mutated: `review.DecisionStore`, which is U11's and was reviewed
there; the gates and the Trash, which this round did not touch; and the 23 probe
rows individually, since S5 measures the set's contribution and 23 rows of one
shape would be volume rather than coverage.
