# U34 round 10, the INDEPENDENT mutation table

Derived by the verifier, who did not write the code. This is not a re-run of the
author's table in `docs/mutation-u34.md`. It was composed from the round's own
diff plus a fixed sample of the unit's existing guards, and the author's table
was read only after this one had been composed, so the overlap is convergence
rather than copying.

Light pass per `docs/METHOD.md`: scoped to the round's diff plus a sample, not an
eighty row sweep of the whole unit.

## How every number here was taken

- Branch `unit/u34-read-only-library-reports` at `1a7cdf7`, worktree
  `.worktrees/u34`, that worktree's own `.venv`.
- `PYTHONDONTWRITEBYTECODE=1` on every run.
- Rows run synchronously in the foreground, one at a time, never backgrounded.
- The driver never invokes git. It snapshots file text, rewrites it, and restores
  it by rewriting the snapshot. Every restore was verified afterwards against
  `git show HEAD:<path>` piped to `shasum`, not against a scratch copy.
- Node ids read from pytest report objects through a `pytest_runtest_logreport`
  hook, never by splitting a `FAILED` line.
- The collected count was checked on EVERY row with
  `pytest --collect-only -o addopts=`. No row moved it. Subset counts were 751,
  531 and 347; the full suite counted 3537 on every row it was run on.
- Deaths confirmed on a subset; every zero on a subset was promoted to a full
  suite run before it is reported as a zero here.
- Message mutations are reworded, never appended, because the suite asserts with
  `in`.

## Baselines

| scope | files | result |
|-|-|-|
| full suite | all | 3522 passed, 15 skipped, 3537 collected |
| rbxml subset | `test_reports.py`, `test_layering.py`, `test_no_beatgrid_ever.py`, `test_rbxml.py`, `test_tree_registry.py`, `test_tree_writer.py`, `test_xml_splice_golden.py`, `test_review_queue.py` | 745 passed, 6 skipped, 751 collected |
| reports subset | `test_reports.py`, `test_review_queue.py`, `test_layering.py` | 527 passed, 4 skipped, 531 collected |
| tests subset | `tests/modules/test_reports.py` | 347 passed, 347 collected |

## The classification, which is the round's subject

`src/cratekit/write/rbxml.py`, rbxml subset.

| id | what was reverted | deaths |
|-|-|-|
| V01 | `node_kind` answers FOLDER for a kind it could not read, the classification that shipped before this round | 7 |
| V02 | `node_kind` answers PLAYLIST for a kind it could not read, the same two valued rule pointed the other way | 7 |
| V03 | `node_kind` stops recognising the FOLDER value positively, so a declared folder reads as unreadable | 39 |
| V04 | `node_kind` stops recognising the PLAYLIST value positively | 38 |
| V05 | `node_kind` swaps the two declared values, so every folder reads as a playlist and back | 26 |
| V06 | `node_kind` reads an ABSENT `Type` as a folder and still refuses every other unknown value, the shipped defect narrowed to the one spelling a real document produces | 3 |
| V07 | `node_kind` reads an ABSENT `Type` as a playlist, the other half of the same narrowing | 3 |
| V08 | the `KIND_UNREADABLE` constant is respelled | **0** |
| V09 | the `KIND_FOLDER` constant is respelled to `directory` | **0** |
| V10 | the `KIND_PLAYLIST` constant is respelled to `list` | 1 |

V01 and V02 costing the same seven is independently reproduced. V03 and V04 both
include collection time errors in fixtures that build a tree, which is why they
run an order of magnitude higher than the rows either side of them.

**Composite for V08.** The constant's VALUE is unobservable by construction:
`_type_name` compares `kind == KIND_UNREADABLE` by symbol and `export._read_nodes`
compares against `rbxml.KIND_FOLDER` and `rbxml.KIND_PLAYLIST` by symbol, so no
call site can see the string change. V13 below shows the branch that constant
selects IS held, at 1. V08 is an inert mutation rather than an unheld guard, and
it is recorded so that the distinction is on the record.

**Composite for V09.** `KIND_FOLDER`'s value IS observable: `_type_name` returns
the kind string straight into a write refusal a person acts on. V39 rewords that
whole sentence and kills 2, so the SENTENCE is pinned and the type word inside it
is not. See finding 4 in the verification report.

## `_type_name`

| id | what was reverted | deaths |
|-|-|-|
| V11 | `_type_name` calls an unreadable kind a playlist again, which is what shipped before this round | 1 |
| V12 | `_type_name` calls an unreadable kind a folder, the other default | 1 |
| V13 | `_type_name` returns the kind name bare, so the refusal reads "a unreadable named X is already there" | 1 |
| V39 | COMPOSITE: the whole "is already there" refusal sentence is reworded | 2 |

## The three way split and the refusal

`src/cratekit/modules/reports/export.py`, reports subset.

| id | what was reverted | deaths |
|-|-|-|
| V14 | `_read_nodes` classifies with an `else` again, so the third state stops existing at the site | 3 |
| V15 | `_read_nodes` files an unreadable node as a PLAYLIST rather than carrying it out | 3 |
| V16 | `read_export` walks past the unreadable nodes without refusing | 3 |
| V17 | the refusal loses the PATHS it found, so nobody is told which node to look at | 3 |
| V18 | the refusal loses the `Type` VALUES it saw | **0** (full suite) |
| V19 | the refusal is reworded to describe a truncated file instead of an unreadable kind | 3 |
| V20 | the refusal fires only when EVERY node is unreadable | 3 |
| V50 | the refusal fires only when MORE THAN ONE node is unreadable, an off by one narrowing | **0** (full suite) |
| V51 | COMPOSITE for V50: the refusal never fires at all | 3 |

**Composite for V18** is V17, its sibling key in the same `detail` dict, at 3.
The refusal's `nodes` key is asserted by the parametrized test; its `found` key is
asserted nowhere. See finding 3.

**Composite for V50** is V51 at 3. The guard is held for a document with several
unreadable nodes and unpinned at its boundary, because every parametrized case
uses `content.replace(old, new)` without a count and therefore retypes all seven
playlists at once. No fixture in the suite carries exactly one unreadable node.
See finding 5.

## A fixed sample of the unit's existing guards

| id | file | what was reverted | deaths |
|-|-|-|-|
| V21 | `aging.py` | aging stops refusing when the intake folder is absent from the tree | 1 |
| V22 | `export.py` | `has_folder` matches a folder at ANY position in its path rather than at its last | **0** (full suite) |
| V23 | `export.py` | `read_export` stops comparing the COLLECTION's declared count with what it holds | 2 |
| V24 | `export.py` | `read_export` stops refusing a COLLECTION carrying one TrackID twice | 1 |
| V25 | `export.py` | `read_export` returns an empty view instead of refusing when the PLAYLISTS section has no root node | 1 |
| V26 | `export.py` | `read_export` stops checking that the COLLECTION sits inside the document element | 1 |
| V27 | `duplicates.py` | the audit stops skipping an entry missing HALF its identity, keeping only the both missing case | 2 |
| V28 | `aging.py` | the grouping filter reads the WHOLE path rather than the ancestors, so a playlist named for the intake folder becomes a grouping | **0** (full suite) |
| V40 | `export.py` | COMPOSITE for V22: `has_folder` answers False for everything | 23 |
| V41 | `export.py` | COMPOSITE for V22: `has_folder` answers True for everything | 2 |
| V42 | `aging.py` | COMPOSITE for V28: the grouping filter is dropped entirely | 5 |

V22 and V28 are both WIDENINGS of a membership test, and each is answered by a
composite that shows the test is load bearing in both directions. What neither
composite covers is the widening itself, which is finding 6.

## The guards this round added to its own test surface

`tests/modules/test_reports.py`, run against that file.

| id | what was reverted | deaths |
|-|-|-|
| V29 | `CITED_FLOOR` drops one named file, the reverts file this very commit created | **0** (full suite) |
| V30 | `CITED_FLOOR` drops `src/cratekit/write/rbxml.py`, the module the round changed | **0** (full suite) |
| V31 | `CITED_FLOOR` is emptied entirely | **0** (full suite) |
| V32 | the named floor check is removed from `_covered_files`, leaving the property alone | 1 |
| V33 | the property check is removed from `_covered_files`, leaving the named floor alone | 1 |
| V34 | the ban list is narrowed at its TOP edge | 2 |
| V35 | the ban list is narrowed at its BOTTOM edge | 2 |
| V36 | the residual headings are read from the residual DOCUMENT rather than from the diff | 2 |
| V37 | `_files_this_branch_writes` stops reading the untracked files | **0** (full suite) |
| V38 | the second derivation stops reading the working tree's status | **0** (full suite) |
| V43 | the shared merge base resolves to `HEAD`, which empties both derivations at once | 4 |
| V45 | COMPOSITE: V43 with `CITED_FLOOR` emptied at the same time | 3 |
| V46 | COMPOSITE: V43 with `CITED_FLOOR` short one file | 4 |
| V47 | `_record` stops clearing the faint mark | 2 |
| V48 | `_record` stops letting a resolved write overwrite an unresolved one | 4 |
| V49 | `_record` clears the faint mark on the WEAK path too | 2 |

V44 was composed and turned out to be textually identical to V43. It is recorded
as a duplicate rather than dropped, because a row that measured a second time and
agreed is worth more on the record than a gap in the numbering.

**The composite for V29 to V31**, and it is the finding. V43 with the floor intact
kills 4. V45, the same merge base failure with the floor EMPTIED, kills 3. Exactly
one of the four deaths belongs to the floor, and the floor's own contents can be
deleted with 3537 tests green. Read by node id, the test whose entire subject is
that constant, `test_the_named_floor_still_bites_when_both_derivations_narrow_together`,
appears in NO failure list in this table except V32's: it survives the constant
being emptied, because its body is a `for` loop over the constant and an empty
constant makes it a test that asserts nothing. See finding 2.

**The composite for V37 and V38**, run with one untracked file created under
`docs/` and removed in a `finally`, tree verified clean afterwards:

    C0  no revert,        untracked file present    0
    C1  V37 alone,        untracked file present    3
    C2  V38 alone,        untracked file present    0
    C3  V37 and V38,      untracked file present    0

This reproduces the author's composite exactly. V37's zero is a fact about a
committed tree having no untracked files, not about the guard.

## Row count, and how it compares

| | rows | zero rows |
|-|-|-|
| the author's table | 30 | 4 |
| this table | 50 distinct, plus 4 untracked composites | 11 |

The eleven zero rows are V08, V09, V18, V22, V28, V29, V30, V31, V37, V38 and
V50. Two of them, V37 and V38, are the author's K15 and K18 and reproduce his
counts. One, V08, is inert by construction. The other eight are guards the
author's table did not mutate.
