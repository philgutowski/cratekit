# u81 notes: the two zero rows, and the row that was refused

`docs/mutation/u81.md` and `docs/mutation/u81-round-2.md` are what the driver
measured and are left exactly as it wrote them. This is the author's reading of
the three rows in that table that did not simply kill.

## The verdict R-322 asked for

Four of six rows kill, and the two the residual is built out of are among them.

| row | U59 | here |
| --- | --- | --- |
| `B5_contradictions_by_number` | 0, promoted to the full suite | 1 |
| `B5_composite` | 0, promoted to the full suite | 1 |

Both rows are copied verbatim from `docs/mutation/u59-rows.toml`, subsets
included, so the comparison is between two measurements of the same experiment
and not between two experiments. `B5_composite` becoming a killing row is the
condition the brief sets, and it is proved by re-running the row rather than by
asserting anything about it.

Baseline green at 7233 collected, against U59's measured 7228, and the five are
reconciled BY IDENTIFIER rather than by total. `tests/test_pending_units.py` is
the only file this task changes, so the reconciliation is scoped to it: `main`'s
copy declares 28 test functions, the branch collects those 28 plus exactly the
five named in this task's commits, and nothing is lost. A total only check would
have shown the same healthy rise over a file that had dropped a test and gained
six. The null control killed zero in both batches.

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

## What is still undriven after this task

`cmd_audit` itself. It calls `load_issues`, which shells out to `gh`, so its exit
code cannot be measured without a token and no test asserts it. The distance
between what is now driven and what `audit` reports is one function call and one
`return 2`, and that is the whole of the remaining gap. Logged as a dropped row
in `docs/mutation/u81-rows.toml` rather than left implied.
