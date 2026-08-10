# U38 round 8: independent verification

**Verdict: MERGE.** No blocking finding. Eleven residuals, all measured, all
recorded here by content so none of them depends on a transcript surviving.

**Who wrote this.** An agent that did not write the round. The light pass
`docs/METHOD.md` assigns U38, scoped to the round's own diff plus a fixed sample
of what came before, with its own worktree, its own venv and its own scratch
directory. The independent mutation table is
`docs/mutation/u38-round-8-independent.md` and its exact reverts are
`docs/mutation/u38-round-8-independent-rows.json`.

## The battery

Run from inside the worktree with its own venv, at commit `c2fda57`, on a clean
tree:

* `ruff check src tests scripts`: **All checks passed.**
* the suite: **3399 passed, 15 skipped**, in 79 seconds.
* the collect only run: **3414 collected.**
* `scripts/scan_repo.py`: silent, exit 0.

All three clean.

## The severity floor, applied

A finding is BLOCKING only if it was driven end to end AND it has a named user
facing cost: somebody loses data, is told something false, is blocked from a
verb, or is shown a clean report over state the tool could not read.

Every finding below was driven end to end. **None of them has a user facing
cost, and the reason is structural rather than lenient.** Everything this round
touched is a META guard: assertions in `tests/` about the shape of this
repository's own source, plus one shipping module, `cli/exit_codes.py`, whose
reservation table came through the round unchanged and whose every mutation in
this table behaves exactly as its author reported. A hole in a meta guard costs a
MAINTAINER: a reviewer believes a rule cannot be switched off and it can. It
costs a user only after somebody writes the evasion and a later module uses it,
and neither has happened. Twenty two reservations, twenty two distinct causes, no
duplicate key, no widened range, no unreachable remediation.

So the verdict is MERGE, and the leading residual below is the largest one this
unit has produced. It should not be lost.

## Finding 1. The structural taint rule misses eight of twenty one live escape hatches, all of them green

**RESIDUAL.** Driven: yes, twenty one hatches built, every one proven to silence
a real reservation or a real bare exit before it was scored, eight of them
measured green on the FULL suite at 3399 passed, 15 skipped, 3414 collected.
User facing cost: none today. Maintainer facing cost: the round's headline claim,
that the structural rule is the only thing that catches an escape hatch nobody
predicted the spelling of, holds only for hatches that keep the parameter named
`source`, keep an annotation that spells `str`, sit at module level, and reach
the text through a shape the propagation models. It is not a rule about the
shape of the module. It is a rule about four specific spellings.

The eight that ship green:

1. `H1` and `P1b`: the helper takes `*text`. The call site is permitted because
   the callee is a module level function, and the propagation then finds an
   empty positional landing list and stops. Nothing is tainted inside the
   helper, which reads `text[0].splitlines()` freely.
2. `P7b`: the same, laundered through a second starred helper that returns the
   text.
3. `H9` and `P5`: a decorator. The rule never looks at a decorator. The wrapper's
   `*passed` is not a seed, so the wrapper reads `passed[0].splitlines()` and
   filters the hits the guard returns. One line of syntax, complete evasion.
4. `P2`: the parameter is renamed. `process_status_literals(raw: str)` is not a
   seed, and the anti vacuity check still passes because six other functions
   still take `source: str`. The rename is invisible to every caller because
   every caller passes positionally.
5. `P3`: the parameter loses its annotation.
6. `P4`: the annotation is widened to `object`, which needs no import.

Six more hatches, `H3`, `H4`, `H5`, `H10`, `P1` and `P7`, are NOT reported by the
rule either. They go red for a different reason, and the reason matters because
it looks like a catch and is not: they either move the text anchor inside
`_with_a_fresh_hatch_wired_in`, so the probe's own hatch is defined and never
called, or they name their helper `_hushed`, the same name the probe uses, so the
probe's helper is shadowed. `P1b` and `P7b` are those same hatches under the name
`_muted` and both are green. So the count of hatches the RULE sees is seven of
twenty one, and the count the SUITE catches is thirteen of twenty one, six of
which are caught by an accident of the probe fixture's own text.

The cheapest fix, if it is taken: seed on the parameter's POSITION rather than
its name, treat any function reachable from a seeded call as tainted regardless
of its parameter list shape, and refuse a decorator on any function this rule
seeds. The largest single win is the decorator, because it needs no cooperation
from the function it hides in.

## Finding 2. The behavioural property's tree wide half catches nothing today

**RESIDUAL.** Driven: `without-comments-neutered-to-the-identity` kills 0 on the
full suite, and `C3`, the same neutering with a guessed marker hatch wired in,
kills 2, exactly what the hatch kills without it. So the comparison of each table
owner against its own comment free twin removes nothing from the catch. It is not
wrong and it is not vacuous, since its anti vacuity floor is pinned: raising the
floor from 22 to 23 kills 1. It simply does not catch anything the marker loop
does not already catch, because no comment in either table owner sits on a line
the guard reports.

## Finding 3. The behavioural property's teeth are five hand guessed markers

**RESIDUAL.** Driven: `C0`, a guessed marker hatch as it ships, kills 2.
`C1`, the same hatch with `FRESH_ESCAPE_MARKERS` emptied, kills 1. `C2`, the same
with the structural rule also relaxed, kills 0 on the full suite. And
`fresh-escape-markers-emptied` alone kills 0.

So the tuple of five markers is the whole of the behavioural half's teeth, and it
can be emptied for free. This is the fingerprint shape the round set out to
replace, one level up: instead of naming the last implementation's symbols it
names five spellings somebody guessed. It is a better fingerprint, and the
round's own docstring is right that no marker appears in the RULE, but the
measurement says the rule's catch comes from the marker list.

## Finding 4. The marker half has no anti vacuity floor

**RESIDUAL.** Driven: `V1` runs the marker loop against a source containing no
reservations at all. Both sides of the comparison become empty lists, the
assertion passes, and the full suite is green at 3399 passed. The tree wide half
has a floor and it is pinned; the marker half has none. If the fixture ever stops
producing hits, and it is a hand written fixture that a later round could edit,
the loop silently compares nothing to nothing. This is the same class as the
R-20 claim this round withdrew, caught before it shipped rather than after.

## Finding 5. The import whitelist is not exact membership over imports

**RESIDUAL.** Driven, all on the full suite: `whitelist-relative-import-clause-dropped`
kills 0, `a-relative-import-into-the-guard-module` kills 0,
`whitelist-top-level-split-dropped` kills 0,
`an-import-fetched-through-the-import-builtin` kills 0. The whitelist bites a
plain import, a symbol import, an import inside a function, and a missing entry,
each at 1 death. It cannot see two routes:

* a RELATIVE import. The collector skips any `ast.ImportFrom` whose level is non
  zero, so `from . import _hush` adds nothing to the set. `tests` is a package,
  so a sibling module that can read comments is one line and no review away.
* `__import__`. `tokenize = __import__("tokenize")` is a call, not an import
  node.

The docstring says what is pinned is what the module MAY import, and adding one
costs the review that line brings. Two spellings cost no line and no review.

## Finding 6. Three clauses inside the enum base walk are unpinned

**RESIDUAL.** Driven on the full suite: the relative import level check, the
membership test against `ENUM_BASES`, and the exact module name `enum` each kill
0. Paired: disabling the walk kills 2, emptying the set kills 2, ignoring the
`as` name kills 2, dropping either half of the disjunction kills 2 and 1. So the
clause as a whole is real and three widenings inside it are free. Any of them
makes `from .vocabularies import Anything as Whatever` read as an enum base out
of the standard library, which widens the guard toward reporting correct code.

## Finding 7. Neither deleted arm's conjuncts are pinned in the widening direction

**RESIDUAL.** Driven on the full suite: `is-exit-attribute-name-check-dropped`
kills 0, `is-status-builtins-identity-check-dropped` kills 0,
`is-status-attribute-name-check-dropped` kills 0. Paired: removing the whole
attribute exit arm kills 12 and removing the whole status arm kills 1, which
reproduce the author's figures exactly. So both arms are real and each conjunct
can be dropped for free, which turns `sys.anything(30)` into an exit and
`anything.SystemExit` into a status. That is the P7 failure this file runs
fixtures against everywhere else: a guard that fires on correct code gets routed
around.

## Finding 8. The author's table is correct where sampled and incomplete against his own diff

**RESIDUAL**, and it is the one METHOD names explicitly as a residual rather than
a blocker.

Correct: ten of ten rows where his mutation and mine are the same text produce
the same count, including 12 for the attribute exit arm and 5 for the widened
range. His reverts file and his markdown agree row for row, 162 rows, 15 zeros,
no duplicate row id, and his three collected count movements at 3186 are real.
The eleventh sampled row differs only because the two mutations differ.

Incomplete: his table has **no row for any internal clause of
`text_the_guard_module_reads`**, the round's largest new function and the one he
names as load bearing. It also has no row for `_without_comments`, none for
`FRESH_ESCAPE_MARKERS`, none for `_slugs_and_statuses`, none for the floor of 22,
none for either of the whitelist's two collection clauses, and none for any
sub clause of `_enum_bases`. He mutated the three new guards only from the
outside, by relaxing the assertion that uses them. Twenty two of my forty zero
rows are on code his table has no row for at all.

My table is 89 rows with 40 zeros against his 162 with 15. The two are not
comparable by total, because his sweeps the whole unit and mine is scoped to the
diff, but they are comparable on the diff, and on the diff his coverage of the
round's own new function is zero rows.

## Finding 9. The keyword propagation branch cannot change an answer

**RESIDUAL.** Driven: `taint-keyword-propagation-dropped` kills 0 on the full
suite, and `H2` says why. A tainted name in keyword position has an `ast.keyword`
node as its parent, not the `ast.Call`, so it is reported by the catch all before
the propagation could ever matter. The branch is unreachable in effect. It should
be recorded as redundant or deleted, the way this round correctly deleted the two
dotted lookups in `_is_exit` and `_is_status`.

## Finding 10. Four arms of the reporting pass are written against shapes the tree does not contain

**RESIDUAL.** Driven on the full suite, each at 0: the source text is CALLED arm,
the store context filter, the async function collection, and the positional only
landing list. Each is defensible as defence in depth, and none is measured. The
round's own good practice, which is to say what is undriven rather than leave it
to be found, was applied to `ENUM_BASES` and not to these.

## Finding 11. The anti vacuity check on the taint rule is redundant, not uncovered

**RESIDUAL**, and it is the mildest one here. `taint-anti-vacuity-check-dropped`
kills 0. Paired: with no parameter matching the seed name at all, the first
assertion fails whether or not the anti vacuity block is present, because the
both directions probe below it already fails when the rule is seeded on nothing.
So the block is a second statement of something the probe already says. That is
worth writing down as redundancy rather than leaving as a zero row.

## What was checked and found clean

* **An instrument that cannot fail.** The one deliberate fingerprint this round
  keeps, the test that nobody in the package writes the deleted marker, CAN go
  red: writing `# not-a-reservation` into `cli/exit_codes.py` kills it, measured.
  The structural rule's both directions probe can go red, measured twice. The
  behavioural property can go red, measured. The only vacuity found is Finding 4.
* **A test whose expected value comes from the code under test.** Swept with an
  AST walk over every assertion in `tests/`, not a grep. Two hits, both in the
  comment round trip property, and both are the intended shape of a property
  test: the same function over two inputs that differ only by comments. The
  hazard they carry is Finding 4 and it is recorded there.
* **A test that forbids a feature by naming the last implementation's symbols.**
  The round DELETED the one that did this, which is the right move, and replaced
  it with one deliberate fingerprint that is documented as a fingerprint and
  measured to bite. No new one was introduced in this unit.
* **Duplicate keys in a mapping several branches appended to.** Swept over every
  dict, set, tuple and list literal in the tree. Zero in this unit's files. The
  reservation table holds 22 reservations and 22 distinct causes.
* **One symbol meaning two things in two modules.** `REPO_ROOT` is defined in
  both `test_reserved_causes.py` and `test_review_queue.py` and is the identical
  expression in both, so it is one thing spelled twice rather than two things
  spelled once. One test NAME is shared across those two files, which pytest
  keeps distinct by node id.
* **The collected count on every row.** All 89 rows collected 3414. Reconciled by
  identifier and not only by total.
* **The shipping module.** Every mutation of `cli/exit_codes.py` in the sample
  behaves as the author reports. Nothing user facing is broken.

## What was NOT measured, named as unmeasured

* **The author's other 146 rows.** Sixteen were sampled and reproduced. The
  remaining rows were not rerun, so this report does not certify their counts.
  Nothing in the sample suggests a problem with them.
* **The three collected count movements to 3186 in his table.** Read from his
  reverts file rather than reproduced. His mechanism is checked and coherent, and
  the same shape was observed in this table's own trap, but the number is his.
* **Timing.** No timing row exists in this unit, so no repeat count or pass rate
  was needed.
* **Whether a hatch could be built that survives BOTH the structural rule and a
  fixed version of it.** Out of scope. The eight that ship green were enough to
  characterise the class.
* **`docs/residual-findings.md` beyond its headings.** Its 23 headings are
  unique, R-21 through R-23 are the round's additions, and no numeric citation
  check was rerun.
