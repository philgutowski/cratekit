# U38 round 8: the INDEPENDENT mutation table

**Who wrote this.** An agent that did not write the code, running the light pass
`docs/METHOD.md` assigns U38. The author's own table is
`docs/mutation/u38-round-8.md`; this one was derived from the round's diff
without reading his row list first, and the two are compared at the end.

**Where the exact reverts are.** `docs/mutation/u38-round-8-independent-rows.json`,
beside this file. Every row below has an entry there carrying the file, the exact
text to find, the exact text to put in its place, the declared occurrence count,
and the node ids that died. A row NAME does not identify a mutation.

**How it was measured.**

* Baseline in the worktree: **3399 passed, 15 skipped, 3414 collected**.
* Rows were applied to a COPY of the worktree in the unit's own scratch
  directory. The worktree itself was never written by the driver and is byte
  identical to `HEAD` throughout. Restores are rewrites from a pristine snapshot
  taken with `git show HEAD:` by hand, never by a checkout.
* The driver never invokes git, never passes a second quiet flag, and reads
  dying node ids off `report.nodeid` from a pytest plugin rather than off a
  parsed failure line.
* `PYTHONDONTWRITEBYTECODE=1` on every row.
* A substitution whose occurrence count is not exactly what the row declares is
  a hard error, so no row can silently apply nothing. Two rows were caught by
  that rule while the table was being built and were repaired against the tree.
* The COLLECTED count was taken on every row from a separate collect only run
  over the whole suite. **All 89 rows collected 3414.** No row in this table
  moves the collected count.
* Deaths were confirmed on the subset of files importing the mutated module
  (`test_reserved_causes.py`, `test_review_queue.py`, `test_cli_contract.py`,
  793 passed and 6 skipped at baseline). **Every zero on the subset was promoted
  to a full suite run**: 40 rows, 40 full runs, and the subset and the full
  suite disagreed on zero of them.

**One trap this table paid for, recorded so the next agent does not.** The first
full suite batch reported one death on every row, including rows that could not
possibly reach the dying test. The dying test was
`tests/test_portability.py::test_the_repository_itself_is_clean`, and it was
failing on the COPY at baseline because the copy carries `.venv`,
`.pytest_cache`, `.ruff_cache` and `.scan-identity` while carrying no `.git`, so
the repository scan walked files a real checkout ignores. A null row was run to
establish the copy's own baseline, the four local only paths were removed, the
pytest cache was disabled, and the batch was rerun. Without the null control the
whole batch would have read as five escape hatches being caught. This is defect
pattern four, a number taken on a fixture rather than on the tree, arriving with
a green suite and a confident reading.

## Part one: twenty one escape hatches, each proven live before it was scored

Every hatch below was PROVEN to work before its detection was scored. A helper
script imported the mutated guard module and ran a real second table, or a real
pair of bare exits, with and without the marker on one line. Every one of the
twenty one prints `HATCH IS LIVE`: the marker silences a reservation the guard
would otherwise report. A hatch that did not silence anything would make the
detection question meaningless.

`reported` is what the structural rule itself answers for that source, measured
by calling `text_the_guard_module_reads` on the hatched text directly. `deaths`
is the suite. The two columns differ, and the difference is the finding.

| row | reported by the rule | deaths | scope |
| --- | --- | --- | --- |
| `H0-authors-hatch-unguessed-marker` | 1 | 1 | subset |
| `H1-starred-parameter-on-the-callee` | 0 | **0** | full |
| `H2-double-starred-parameter-on-the-callee` | 1 | 1 | subset |
| `H3-entry-parameter-renamed-off-the-seed` | **0** | 1 | subset |
| `H4-entry-annotation-widened-to-object` | **0** | 1 | subset |
| `H5-entry-parameter-unannotated` | **0** | 1 | subset |
| `H6-control-inline-hatch-on-a-live-seed` | 1 | 1 | subset |
| `H7-hatch-behind-a-class` | 1 | 1 | subset |
| `H8-hatch-in-a-nested-function` | 1 | 1 | subset |
| `H9-hatch-in-a-decorator` | 0 | **0** | full |
| `H10-text-laundered-through-a-returning-helper` | **0** | 1 | subset |
| `P0-control-inline-hatch-in-the-bare-status-guard` | 1 | 1 | subset |
| `P1-starred-callee-in-the-bare-status-guard` | **0** | 1 | subset |
| `P2-parameter-renamed-off-the-seed-anchor-intact` | 0 | **0** | full |
| `P3-parameter-unannotated-anchor-intact` | 0 | **0** | full |
| `P4-annotation-widened-to-object-anchor-intact` | 0 | **0** | full |
| `P5-decorator-on-the-bare-status-guard` | 0 | **0** | full |
| `P6-hatch-behind-a-lambda` | 1 | 1 | subset |
| `P7-laundered-through-a-returning-starred-helper` | **0** | 1 | subset |
| `P1b-starred-callee-under-a-name-the-fixture-does-not-use` | 0 | **0** | full |
| `P7b-laundered-through-a-returning-starred-helper-renamed` | 0 | **0** | full |

Row by row.

* **H0**, the author's own hatch rebuilt from his reverts file, with a marker
  nobody guessed. Reported, one death. His figure reproduces exactly.
* **H1**, the same hatch whose helper takes `*text` instead of `text: str`. The
  call site is permitted because the callee is a module level function; the
  propagation then finds an empty positional landing list and stops. Nothing is
  reported and the full suite is green.
* **H2**, the helper takes `**named` and the call passes the text as a keyword.
  Caught, and not by the keyword propagation branch: the parent of the tainted
  name is an `ast.keyword` node rather than the `ast.Call`, so it falls to the
  catch all and is reported as reaching a keyword. The keyword propagation
  branch cannot be the thing that caught it, which the next section measures.
* **H3, H4, H5**, the entry point's parameter renamed, unannotated, and
  annotated `object`. **The rule reports nothing for all three.** The suite still
  goes red, but for a different reason: all three destroy the text anchor inside
  `_with_a_fresh_hatch_wired_in`, so the probe's own hatch is defined and never
  called, and the second assertion fires saying the rule is measuring nothing.
  P2, P3 and P4 repeat the same three shapes without moving the anchor and are
  green.
* **H6**, the control. An inline hatch on a live seed. Reported.
* **H7**, the text handed to a class constructor. Reported, because the callee is
  not in the module level function table.
* **H8**, the hatch as a nested function inside the seeded entry point.
  Reported, for the same reason.
* **H9**, a decorator on `reserved_code_tables`. The wrapper reads
  `passed[0].splitlines()` and filters the returned hits. The rule never looks at
  a decorator and the wrapper's parameters are not seeds. Green on the full
  suite.
* **H10, P1, P7**, laundered through a helper. The rule reports nothing. They go
  red only because the injected helper is named `_hushed`, the same name the
  probe fixture uses, so the probe's own helper is shadowed. **P1b and P7b are
  the same hatches under the name `_muted`, and both are green on the full
  suite.**
* **P0**, the control for the bare status guard. Reported.
* **P2, P3, P4, P5**, parameter renamed, unannotated, annotated `object`, and a
  decorator, all in `process_status_literals`, all leaving the probe's anchor
  intact. **All four green on the full suite.**
* **P6**, a lambda between the seed and the hatch. Reported.

**Eight of twenty one live escape hatches ship with 3399 passed, 15 skipped and
3414 collected.** Six more go red only because they perturbed the probe fixture
rather than because the rule saw them.

## Part two: the structural rule clause by clause

The author's table has no row for any internal clause of
`text_the_guard_module_reads`. It is the round's largest new function and the one
his own account calls load bearing. These are its clauses.

| row | deaths | scope |
| --- | --- | --- |
| `taint-seed-name-clause-dropped` | 1 | subset |
| `taint-seed-annotation-clause-dropped` | **0** | full |
| `taint-seed-widened-to-any-text-parameter` | **0** | full |
| `taint-seed-keyword-only-arguments-dropped` | **0** | full |
| `taint-anti-vacuity-check-dropped` | **0** | full |
| `taint-positional-propagation-dropped` | 1 | subset |
| `taint-keyword-propagation-dropped` | **0** | full |
| `taint-assignment-propagation-dropped` | **0** | full |
| `taint-fixed-point-runs-once` | 1 | subset |
| `the-only-sink-respelled-to-ast-walk` | 1 | subset |
| `sink-single-argument-narrowing-dropped` | **0** | full |
| `call-to-a-module-level-function-no-longer-permitted` | 1 | subset |
| `assignment-of-the-source-text-no-longer-permitted` | **0** | full |
| `the-source-text-is-called-arm-dropped` | **0** | full |
| `taint-load-context-filter-dropped` | **0** | full |
| `async-functions-not-collected-as-functions` | **0** | full |
| `positional-landing-drops-positional-only-parameters` | **0** | full |

* `taint-seed-name-clause-dropped` widens the seed to any parameter annotated
  `str`, which taints `wanted` and `queue` in the review walks and reports them.
  One death, so the narrowing to the NAME `source` is load bearing in the
  direction of false positives.
* `taint-seed-annotation-clause-dropped` and
  `taint-seed-widened-to-any-text-parameter` both kill nothing, because the
  guard module happens to annotate every `source` parameter and happens to have
  no parameter called `text` or `raw`. So neither half of the seed test is
  pinned from the other side, and P2 through P4 are the escapes that follow.
* `taint-anti-vacuity-check-dropped` kills nothing. Paired below: it is
  genuinely redundant with the probe rather than unexercised.
* `taint-keyword-propagation-dropped` kills nothing, and H2 says why: a tainted
  name in keyword position is reported by the catch all before the propagation
  could matter. The branch cannot change an answer on any source that reaches
  it.
* `taint-assignment-propagation-dropped` and
  `assignment-of-the-source-text-no-longer-permitted` both kill nothing, because
  no function in the shipped guard module assigns its source text to another
  name. Paired below.
* `sink-single-argument-narrowing-dropped` kills nothing, because nothing in the
  module calls `ast.parse` with two arguments. Paired below.
* `the-source-text-is-called-arm-dropped`, `taint-load-context-filter-dropped`,
  `async-functions-not-collected-as-functions` and
  `positional-landing-drops-positional-only-parameters` all kill nothing: the
  module calls no source text, stores to no tainted name, defines no async
  function and declares no positional only parameter, so each arm is written
  against a shape the tree does not contain.

### The composites for those zeros

| row | deaths | what it says |
| --- | --- | --- |
| `C8-a-two-argument-parse-of-the-source-text` | 1 | the sink narrowing bites the moment a two argument parse exists |
| `C9-the-source-text-assigned-then-read-as-an-attribute` | 1 | the assignment propagation and the assignment permit together catch a laundered assignment |
| `C10-the-same-assignment-with-the-assignment-propagation-dropped` | **0** | and dropping the propagation is what lets it through, so the pair is real and only unexercised |
| `V2-no-parameter-matches-the-seed-name` | 1 | with no seed at all the vacuity message makes the first assertion fail |
| `V3-no-seed-with-the-anti-vacuity-check-dropped` | 1 | and it still fails, because the both directions probe already covers a rule seeded on nothing |

`V2` and `V3` together are the honest reading of `taint-anti-vacuity-check-dropped`:
the check is REDUNDANT with the probe below it rather than uncovered, and that is
worth recording as redundancy instead of describing it as a guard.

## Part three: the comment round trip property

| row | deaths | scope |
| --- | --- | --- |
| `without-comments-neutered-to-the-identity` | **0** | full |
| `the-anti-vacuity-floor-of-twenty-two-raised-by-one` | 1 | subset |
| `the-anti-vacuity-floor-of-twenty-two-dropped-to-zero` | **0** | full |
| `fresh-escape-markers-narrowed-to-one` | **0** | full |
| `fresh-escape-markers-emptied` | **0** | full |
| `slugs-and-statuses-neutered-to-an-empty-list` | **0** | full |
| `V1-the-marker-half-run-against-a-source-with-no-reservations` | **0** | full |

Composites, on the guessed marker hatch that the property is supposed to be the
thing that catches:

| row | deaths | what it says |
| --- | --- | --- |
| `C0-a-guessed-marker-hatch-as-it-ships` | 2 | the behavioural property and the structural rule, exactly as the author reports |
| `C1-a-guessed-marker-hatch-with-the-markers-emptied` | 1 | emptying the five hand written markers removes the behavioural catch entirely |
| `C2-the-same-with-the-structural-rule-also-relaxed` | **0** | and then the hatch ships green |
| `C3-a-guessed-marker-hatch-with-the-comment-stripper-neutered` | 2 | neutering the comment stripper removes nothing, so the tree wide half catches nothing today |

Read `C0`, `C1` and `C3` together. The behavioural property has two halves. The
tree wide half, which compares each table owner against its own comment free
twin, contributes **zero** on today's tree: making `_without_comments` the
identity function leaves the catch at 2. The marker half, which appends five hand
written markers to a fixture, is the whole of the property's teeth, and emptying
that tuple takes the catch from 2 to 1. So the behavioural property is a
fingerprint over five guessed spellings wearing a property's clothes, which is
the shape the round said it was replacing.

`V1` is the second half of that. The marker half has NO anti vacuity floor: run
it against a source with no reservations in it and both sides are empty lists,
the assertion passes, and nothing anywhere notices. The tree wide half does have
a floor and the floor is pinned at its boundary, which is what
`the-anti-vacuity-floor-of-twenty-two-raised-by-one` at 1 death measures.

## Part four: the import whitelist

| row | deaths | scope |
| --- | --- | --- |
| `control-import-tokenize-plainly` | 1 | subset |
| `a-symbol-import-out-of-tokenize` | 1 | subset |
| `tokenize-imported-inside-a-function` | 1 | subset |
| `whitelist-loses-the-future-entry` | 1 | subset |
| `whitelist-relative-import-clause-dropped` | **0** | full |
| `whitelist-top-level-split-dropped` | **0** | full |
| `a-relative-import-into-the-guard-module` | **0** | full |
| `an-import-fetched-through-the-import-builtin` | **0** | full |

The whitelist bites a plain import, a symbol import, an import inside a function
body, and a missing entry. It does not see two routes that need no review at all:

* **a relative import.** The collector skips any `ast.ImportFrom` with a non zero
  level, so `from . import _pending` in the guard module adds nothing to the set
  and the assertion still reads `{"__future__", "ast", "re"}`. `tests` is a
  package, so a sibling module that can read comments is one line away.
* **`__import__`.** `tokenize = __import__("tokenize")` is a call, not an import
  node, so the collector never sees it.

Both were driven end to end on the full suite and both are green.

## Part five: the enum base clause, the round's other new code

| row | deaths | scope |
| --- | --- | --- |
| `enum-base-alias-ignored` | 2 | subset |
| `enum-bound-clause-dropped` | 2 | subset |
| `enum-spelling-clause-dropped` | 1 | subset |
| `enum-bases-emptied` | 2 | subset |
| `C5-enum-bases-walk-disabled` | 2 | subset |
| `enum-import-level-check-dropped` | **0** | full |
| `enum-base-membership-check-dropped` | **0** | full |
| `enum-module-name-widened-to-a-suffix` | **0** | full |
| `enum-bases-narrowed-to-strenum-alone` | **0** | full |
| `enum-spelling-clause-loses-the-dotted-split` | **0** | full |

The clause as a whole is load bearing: ignoring the `as` name kills 2, dropping
either half of the disjunction kills 2 and 1, emptying the set kills 2, disabling
the walk kills 2. Three clauses INSIDE the walk are not pinned by anything: the
relative import level check, the membership test against `ENUM_BASES`, and the
exact module name `enum`. Any of the three can be widened for free, which means
`from .vocabularies import Anything as Whatever` would be read as an enum base
out of the standard library. `enum-spelling-clause-loses-the-dotted-split` is a
fourth: nothing in the tree writes a module qualified base, so the dotted split
the docstring calls out is unexercised.

## Part six: the two dead tails this round deleted

| row | deaths | scope |
| --- | --- | --- |
| `C6-attribute-exit-arm-removed-entirely` | 12 | subset |
| `is-exit-identity-check-dropped` | 1 | subset |
| `is-exit-attribute-name-check-dropped` | **0** | full |
| `C7-is-status-attribute-arm-removed-entirely` | 1 | subset |
| `is-status-builtins-identity-check-dropped` | **0** | full |
| `is-status-attribute-name-check-dropped` | **0** | full |
| `unary-minus-branch-dropped` | 1 | subset |
| `negatives-treated-as-success` | 1 | subset |

Both arms are real, at 12 and 1. Neither arm's individual CONJUNCTS are pinned in
the widening direction: keeping only the module identity, or only the attribute
name, kills nothing in three of the four cases. Each of those widenings makes the
guard report correct code, which is the failure shape this file names P7 and
runs fixtures against everywhere else.

## Part seven: a fixed sample of the unit's existing guards

Run to check whether the author's table reproduces at all. Where the mutation is
the same, the count is the same, ten times out of ten.

| row | mine | the author's | his row |
| --- | --- | --- | --- |
| `sample-max-hops-at-4` | 3 | 3 | `max-hops-at-4` |
| `sample-bool-exclusion-dropped` | 1 | 1 | `bool-exclusion-dropped` |
| `unary-minus-branch-dropped` | 1 | 1 | same id |
| `negatives-treated-as-success` | 1 | 1 | `scan-treats-negatives-as-success` |
| `enum-bases-emptied` | 2 | 2 | same id |
| `enum-bound-clause-dropped` | 2 | 2 | `enum-import-clause-dropped` |
| `enum-spelling-clause-dropped` | 1 | 1 | same id |
| `C5-enum-bases-walk-disabled` | 2 | 2 | `enum-bases-walk-disabled` |
| `C6-attribute-exit-arm-removed-entirely` | 12 | 12 | `attribute-exit-arm-dropped` |
| `C7-is-status-attribute-arm-removed-entirely` | 1 | 1 | `systemexit-through-builtins-dropped` |
| `sample-seen-dedupe-dropped` | 1 | 1 | `seen-dedupe-dropped` |
| `sample-index-duplicate-check-dropped` | 1 | 1 | `index-duplicate-check-dropped` |
| `sample-index-range-check-dropped` | 3 | 3 | `index-range-check-dropped` |
| `sample-reserved-range-narrowed-by-one` | 2 | 2 | same id |
| `sample-reserved-range-widened-to-the-growth-band` | 5 | 5 | same id, his to 64 and mine to 70 |
| `sample-review-walk-suffix-match` | 6 | 5 | different mutations, not a discrepancy |

`sample-review-walk-suffix-match` replaces the module constant with a two part
spelling; his replaces the resolution call with a suffix comparison. Two
different mutations of one guard, so 6 against 5 says nothing about either.

`C4-the-deleted-marker-written-into-a-package-source` kills 1. The one deliberate
fingerprint the round keeps, the test that nobody writes the deleted marker, CAN
go red. It is not an instrument that cannot fail.

## What this table counts

* **89 rows**, against the author's 162. Mine is scoped harder: his sweeps the
  whole unit, mine is the round's diff plus a sixteen row sample of what came
  before.
* **40 zero rows**, against his 15. Every one was promoted from the subset to a
  full suite run and every one held.
* **All 89 rows collected 3414.** No row in this table moves the collected count,
  which is the opposite of his three import time refusals and is expected: this
  table barely touches `cli/exit_codes.py`.
* Twenty two of my forty zeros are on code the author's table has no row for at
  all.
