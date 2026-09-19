# u81 notes: the two zero rows, and the row that was refused

`docs/mutation/u81.md` and `docs/mutation/u81-round-2.md` are what the driver
measured and are left exactly as it wrote them. This is the author's reading of
the three rows in that table that did not simply kill.

## The verdict R-322 asked for

Ten rows over three batches, eight deaths and two explained zeros. The two rows
the residual is built out of are among the deaths.

| row | U59 | here |
| --- | --- | --- |
| `B5_contradictions_by_number` | 0, promoted to the full suite | 1 |
| `B5_composite` | 0, promoted to the full suite | 1 |

Both rows are copied verbatim from `docs/mutation/u59-rows.toml`, subsets
included, so the comparison is between two measurements of the same experiment
and not between two experiments. `B5_composite` becoming a killing row is the
condition the brief sets, and it is proved by re-running the row rather than by
asserting anything about it.

Baselines green: 7233 collected in rounds 1 and 2, and 7235 in round 3 after the
fix round added two more tests, against U59's measured 7228. The seven are
reconciled BY IDENTIFIER rather than by total. `tests/test_pending_units.py` is
the only file this task changes, so the reconciliation is scoped to it: `main`'s
copy declares 28 test functions, the branch collects those 28 plus exactly the
seven this task's commits name, and nothing is lost. A total only check would
have shown the same healthy rise over a file that had dropped a test and gained
eight. The null control killed zero in all three batches.

## `B5_unit_label_dropped`, zero, maintainer facing

Dropping `node["unit"]` and keeping only the closure test kills nothing on the
full suite. The term is redundant, and that is a property of the function that
feeds it rather than an opinion: `units_by_issue_number` skips any node whose
`unit` flag is false, so the number it returns can never address an unlabelled
issue, and the term it would be protecting against has no reachable input.

METHOD gives a maintainer facing zero one line and no composite. It is given one
line and an assertion as well, because a zero explained only in prose is the
shape this project has been wrong about before:
`test_the_unit_to_issue_map_is_read_off_the_titles_and_drops_a_duplicate` now
carries an issue titled `U40:` with no unit label, and asserts it is excluded. So
the redundancy is now pinned rather than argued, and a change that makes the term
load bearing again turns that test red.

## `B5_heading_anchor_dropped`, zero, maintainer facing

Replacing `re.match(r"^## R-(\d+)\.\s*...")` with an unanchored `re.search` kills
nothing. The reason is that the difference is unreachable on the tree, and that
was measured rather than assumed. Over all 14,499 lines of
`docs/residual-findings.md`, both forms find the same 325 headings, produce no
extra keys and no differing title. There is no line in the document today that
carries a residual heading anywhere other than at its start.

That is a statement about the document rather than about the code, so it can stop
being true, and the honest report of this row is that the anchor is correct and
currently costs nothing to remove. It is not a residual: no reachable input
produces a wrong answer, which is the third condition METHOD sets for a blocking
finding, and the entry it would open would say only that a guard is guarding
against something no input supplies.

## `B5_owed_argument_ignored`, refused in round 1, killed in round 2

The driver refused the row because its `old` text matched twice.
`owed = owed_by_unit() if owed is None else owed` is written once in
`unresolved_closes` and once in `contradictions`, since both functions take the
register the same way on purpose, and an ambiguous match does not fail loudly in
a hand rolled driver, it mutates the wrong site and returns a confident number
about an experiment nobody ran. Re-run as its own batch with the following line
for context, in `docs/mutation/u81-round-2-rows.toml`, and it kills.

## Round 3, the fix round, and a correction to round 1's own record

`/code-review` raised three findings and all three are driven rather than
argued. `docs/mutation/u81-round-3.md` holds the measurement, three rows, three
deaths.

| row | kills |
| --- | --- |
| `B5_owed_default_dropped` | 2 |
| `B5_audit_exit_code` | 1 |
| `B5_audit_drops_the_detector` | 1 |

**The first row is the hole the fix opened, one frame up.** Making the register
injectable is what lets the drivers survive somebody discharging a marker, and it
means every driver supplies a register while `cmd_audit`, the only production
caller, supplies none. `owed = owed or {}` in place of the `is None` test keeps
the whole battery green and stops `board.py audit` reporting register
contradictions at all, returning 0 where it owes 2. That is R-322's own shape
reproduced by the fix for R-322, which is METHOD's fifth pattern exactly: a fix
round fixes the instance it was handed and reproduces the class one file over.

**ROUND 1 DROPPED `B5_audit_exit_code` ON A FALSE PREMISE, and the correction
belongs here rather than in the row file.** The reason logged was that
`cmd_audit` shells out to `gh` for the issue list, so a row over it could not run
without a token. Every name that function calls is module level and replaceable,
`tests/test_pending_units.py` already replaces two of them the same way, and
`_board()` returns a fresh module per call so nothing leaks. The claim was wrong
and, worse than wrong, it certified the hole: the next reader would have found
the gap considered and settled. `docs/mutation/u81-rows.toml` and the table
generated from it are left as they were written, because a row file edited after
the fact no longer describes the table it produced, and a record that quietly
becomes correct is a record nobody can audit.

The lesson is one this repository has already paid for once, in this same test
file: an earlier version of the closing-spelling table asserted that `Fixes #36`
does not close an issue and justified it with the repository's own contract. A
test, or a dropped row, may not assert a limitation into a fact.

## What is still undriven after this task

`reconcile` and the two board-writing paths under it. Those genuinely need a
project-scoped token, and `audit --labels-only` exists because a
repository-scoped one cannot read a user-owned project at all. Everything
`cmd_audit` does with what `reconcile` returns is now driven, which is the half
that decides the exit code.
