# U38 round 8: the mutation table, every row measured against the shipped tree

**What this file is.** Every guard, constant and whitelist this unit ships,
reverted ALONE, full suite, deaths counted from a pytest plugin's report objects.
It is the primary evidence the round produces. The round before this one carried
its table inside `docs/residual-findings.md` and the round before THAT carried it
only in a chat message, where a verifier could not compare it row by row.

**Where the exact reverts are.** `docs/mutation/u38-round-8-reverts.json`, beside
this file. Every row in the table below has an entry there carrying the file, the
exact text to find, the exact text to put in its place, and the node ids that
died. A row NAME does not identify a mutation, and a count with no row definition
beside it is not evidence.

**How it was measured.**

* Baseline on this branch: **3399 passed, 15 skipped, 3414 collected**.
* Each row was applied to a COPY of the worktree refreshed from it with
  `rsync --checksum --delete` immediately beforehand, so no row could inherit the
  row before it and the worktree itself was never written by the driver.
* The driver never invokes `git`. It never passes `-q`, because `pyproject.toml`
  already sets it and a second one becomes `-qq`, which suppressed the summary
  line and turned an entire result set into zeros on 2026-08-09.
* `PYTHONDONTWRITEBYTECODE=1`, because two mutations of identical byte length
  written inside one second make CPython reuse a cached bytecode file.
* Dying node ids come off `report.nodeid`, never off a parsed `FAILED` line: the
  ids in this suite are parametrized with whole fixture sources and contain the
  `" - "` separator, so splitting on it collapses ids and undercounts a row.
* The COLLECTED count is recorded on every row. Three rows move it, and all three
  are import-time refusals in `cli/exit_codes.py` that take whole test files with
  them. That is the guard biting rather than a broken row, and the count is what
  says so.
* A substitution whose occurrence count is not exactly what the row declares is a
  hard error, so no row can silently apply nothing.

**What a zero means here.** A guard that kills nothing is a finding. Sixteen rows
measured zero in this round's first sweep and eleven were CLOSED by fixtures
rather than explained; the closures are the two commits before this file. Every
zero row that remains is paired with a composite that shows what it does hold,
because a prose argument is not evidence.

## The table

`G` is `tests/_source_guards.py`, `T` is `tests/test_reserved_causes.py`, `S` is
`src/cratekit/cli/exit_codes.py` and `D` is `docs/residual-findings.md`. The
`collected` column is blank when the row collected the baseline 3414 and carries
the number when it did not.

| id | file | deaths | collected |
| --- | --- | --- | --- |
| `review-walk-suffix-match` | G | 5 |  |
| `review-leaf-hardcoded` | G | 1 |  |
| `exit-code-leaf-hardcoded` | G | 1 |  |
| `exit-code-class-spelled-again` | G | 1 |  |
| `import-targets-fallback-sibling-dropped` | G | 3 |  |
| `import-targets-fallback-package-none-dropped` | G | 2 |  |
| `import-targets-absolute-package-clause-dropped` | G | 7 |  |
| `import-targets-package-resolution-ignored` | G | 6 |  |
| `walk-off-the-top-clause-dropped` | G | 1 |  |
| `relative-module-level-off-by-one` | G | 4 |  |
| `exit-code-imports-package-arm-dropped` | G | 5 |  |
| `exit-code-imports-plain-import-arm-dropped` | G | 1 |  |
| `no-module-qualified-exitcode` | G | 2 |  |
| `names-the-class-direct-clause-dropped` | G | 4 |  |
| `names-a-code-class-qualified-clause-dropped` | G | 14 |  |
| `names-a-code-module-qualified-clause-dropped` | G | 4 |  |
| `no-module-level-literals` | G | 24 |  |
| `module-level-literals-annassign-dropped` | G | 1 |  |
| `no-class-level-literals` | G | 10 |  |
| `class-level-literals-annassign-dropped` | G | 1 |  |
| `max-hops-at-2` | G | 2 |  |
| `max-hops-at-4` | G | 3 |  |
| `max-hops-at-6` | G | 3 |  |
| `hop-bound-check-dropped` | G | 3 |  |
| `bool-exclusion-dropped` | G | 1 |  |
| `resolve-int-name-branch-dropped` | G | 18 |  |
| `resolve-int-attribute-branch-dropped` | G | 5 |  |
| `unary-minus-branch-dropped` | G | 1 |  |
| `no-arithmetic` | G | 7 |  |
| `arithmetic-add-dropped` | G | 3 |  |
| `arithmetic-sub-dropped` | G | 1 |  |
| `arithmetic-mult-dropped` | G | 1 |  |
| `no-floor-division-or-remainder` | G | 2 |  |
| `division-by-zero-guard-dropped` | G | 1 |  |
| `int-conversion-in-resolve-int-dropped` | G | 1 |  |
| `enum-declarations-off` | G | 27 |  |
| `enum-classified-by-class-name` | G | 27 |  |
| `enum-base-narrowed-to-the-three-spellings` | G | 2 |  |
| `enum-import-clause-dropped` | G | 2 |  |
| `enum-spelling-clause-dropped` | G | 1 |  |
| `enum-bases-walk-disabled` | G | 2 |  |
| `enum-bases-narrowed-to-strenum-alone` | G | 0 |  |
| `enum-bases-emptied` | G | 2 |  |
| `enum-values-annassign-dropped` | G | 1 |  |
| `enum-cause-shape-filter-dropped` | G | 1 |  |
| `cause-slug-shape-widened-to-one-word` | G | 1 |  |
| `key-not-resolved-through-names` | G | 9 |  |
| `key-not-resolved-through-a-class-attribute` | G | 5 |  |
| `own-declarations-dropped-from-the-key-set` | G | 26 |  |
| `no-resolution-through-names` | G | 8 |  |
| `no-resolution-through-module-constants` | G | 7 |  |
| `no-resolution-through-branch-locals` | G | 1 |  |
| `through-names-hop-bound-dropped` | G | 1 |  |
| `status-does-not-read-through-names-first` | G | 3 |  |
| `no-constructor-conversion` | G | 5 |  |
| `constructor-conversion-regated-to-the-range` | G | 2 |  |
| `one-argument-narrowing-dropped` | G | 1 |  |
| `int-conversion-in-status-dropped` | G | 2 |  |
| `no-getattr-conversion` | G | 1 |  |
| `getattr-conversion-not-narrowed-to-the-class` | G | 1 |  |
| `bare-integer-range-gate-dropped` | G | 9 |  |
| `narrowed-to-the-eighteen-live-integers` | G | 11 |  |
| `sequence-not-read-through-a-name` | G | 2 |  |
| `crossed-values-not-filtered-by-status` | G | 0 |  |
| `no-record-dict-crossing` | G | 1 |  |
| `dict-literal-arm-dropped` | G | 59 |  |
| `tuple-and-list-arm-dropped` | G | 7 |  |
| `comprehension-arm-dropped` | G | 7 |  |
| `comprehension-iterable-refiltered-to-constants` | G | 2 |  |
| `subscript-assignment-arm-dropped` | G | 4 |  |
| `setdefault-arm-neutered` | G | 3 |  |
| `dict-and-ordereddict-arm-dropped` | G | 2 |  |
| `catch-all-call-crossing-dropped` | G | 5 |  |
| `call-keyword-arguments-not-crossed` | G | 3 |  |
| `branches-not-collected` | G | 15 |  |
| `branch-match-arm-dropped` | G | 3 |  |
| `branch-if-arm-dropped` | G | 12 |  |
| `branch-if-arm-refiltered-to-constants` | G | 3 |  |
| `branch-body-read-at-top-level-only` | G | 2 |  |
| `branch-enters-a-nested-scope` | G | 1 |  |
| `branch-locals-not-read` | G | 4 |  |
| `zipped-two-argument-check-dropped` | G | 1 |  |
| `seen-dedupe-dropped` | G | 1 |  |
| `branch-label-ignored-and-restatused` | G | 4 |  |
| `os-underscore-exit-dropped` | G | 1 |  |
| `tracked-modules-narrowed-to-sys` | G | 5 |  |
| `walk-scope-enters-nested-scopes` | G | 4 |  |
| `parameter-shadowing-dropped` | G | 1 |  |
| `nested-scope-does-not-inherit` | G | 21 |  |
| `binding-fixed-point-runs-once` | G | 1 |  |
| `status-subclass-binding-dropped` | G | 1 |  |
| `exit-held-in-a-name-binding-dropped` | G | 3 |  |
| `module-rebinding-dropped` | G | 1 |  |
| `import-module-held-in-a-name-dropped` | G | 1 |  |
| `symbol-import-of-exit-dropped` | G | 3 |  |
| `symbol-import-of-systemexit-dropped` | G | 1 |  |
| `symbol-import-of-a-tracked-module-dropped` | G | 1 |  |
| `os-sys-attribute-chain-dropped` | G | 1 |  |
| `import-by-name-resolution-dropped` | G | 2 |  |
| `imported-module-narrowed-to-tracked-dropped` | G | 0 |  |
| `getattr-fetched-exit-dropped` | G | 2 |  |
| `fetched-attribute-must-be-a-constant-dropped` | G | 1 |  |
| `attribute-exit-arm-dropped` | G | 12 |  |
| `systemexit-through-builtins-dropped` | G | 1 |  |
| `ends-the-process-status-half-dropped` | G | 6 |  |
| `ends-the-process-exit-half-dropped` | G | 17 |  |
| `scan-single-argument-narrowing-dropped` | G | 1 |  |
| `scan-zero-exclusion-dropped` | G | 2 |  |
| `scan-treats-negatives-as-success` | G | 1 |  |
| `scan-negatives-as-success-and-no-unary-minus` | G | 1 |  |
| `scan-does-not-recurse-into-nested-scopes` | G | 22 |  |
| `scope-literals-shadowing-dropped` | G | 1 |  |
| `scope-literals-do-not-inherit` | G | 3 |  |
| `index-duplicate-check-dropped` | S | 1 |  |
| `index-vocabulary-check-dropped` | S | 8 |  |
| `index-range-check-dropped` | S | 3 |  |
| `index-band-check-dropped` | S | 0 |  |
| `index-verb-producible-check-dropped` | S | 0 |  |
| `reservation-remediation-check-dropped` | S | 1 |  |
| `reserved-names-no-missing-cause` | S | 1 |  |
| `reserved-range-widened-to-the-growth-band` | S | 5 |  |
| `reserved-range-narrowed-by-one` | S | 2 |  |
| `reserved-bands-widened` | S | 1 |  |
| `a-duplicate-reservation-injected` | S | 1 | 3186 |
| `a-duplicate-reservation-injected-with-the-index-check-dropped` | S | 2 |  |
| `key-set-drops-the-registry` | T | 44 |  |
| `key-set-drops-the-derivation` | T | 44 |  |
| `key-set-drops-only-the-derivation` | T | 1 |  |
| `package-of-collapsed` | T | 1 |  |
| `package-sources-narrowed` | T | 6 |  |
| `package-sources-vendor-filter-dropped` | T | 2 |  |
| `table-owners-widened` | T | 3 |  |
| `owned-sources-hand-listed` | T | 2 |  |
| `population-includes-the-table-owners` | T | 1 |  |
| `at-risk-own-declarations-ignored` | T | 1 |  |
| `a-fresh-per-line-hatch-on-a-marker-the-fixtures-use` | G | 2 |  |
| `a-fresh-per-line-hatch-on-a-marker-nobody-guessed` | G | 1 |  |
| `a-fresh-hatch-nobody-guessed-with-the-structural-rule-relaxed` | G + T | 0 |  |
| `the-structural-rule-relaxed-alone` | T | 0 |  |
| `tokenize-imported-into-the-guard-module` | G | 1 |  |
| `tokenize-imported-with-the-whitelist-relaxed` | G + T | 0 |  |
| `the-import-whitelist-relaxed-alone` | T | 0 |  |
| `an-invented-title-in-a-covered-file` | G | 1 |  |
| `citation-reverse-direction-dropped` | T | 0 |  |
| `an-invented-title-with-the-reverse-direction-dropped` | G + T | 0 |  |
| `residual-headings-read-into-a-set-of-titles` | T | 0 |  |
| `a-byte-identical-duplicate-heading` | D | 2 |  |
| `a-duplicate-heading-with-the-headings-read-into-a-set` | D + T | 0 |  |
| `cited-residuals-loses-an-entry` | T | 1 |  |
| `authored-globs-narrowed-to-source` | T | 2 |  |
| `citation-form-widened-to-any-quote` | T | 2 |  |
| `not-a-cause-loses-an-entry` | T | 0 |  |
| `converted-elsewhere-loses-the-preflight-entry` | T | 5 |  |
| `reserved-range-widened-to-the-whole-byte` | S | 16 |  |
| `a-process-band-code-reserved-with-the-range-widened` | S | 1 | 3186 |
| `a-process-band-code-reserved-with-the-band-check-dropped` | S | 18 |  |
| `a-non-producible-code-reserved-past-the-range-and-the-band` | S | 1 | 3186 |
| `a-non-producible-code-reserved-with-the-producible-check-dropped` | S | 18 |  |
| `setdefault-arm-deleted-so-the-catch-all-handles-it` | G | 0 |  |
| `crossed-values-unfiltered-with-the-dedupe-dropped` | G | 1 |  |
| `not-a-cause-loses-the-scope-entry` | T | 6 |  |
| `not-a-cause-emptied` | T | 10 |  |

## The fifteen zero rows, each with the composite that says what it holds

A zero row is acceptable only when a COMPOSITE shows what it does hold: a
mutation of the thing it guards, with both counts reported. A prose argument is
not evidence. Every zero row below is one of three shapes: a check that cannot
die alone because the defect it catches is not present, a whitelist entry that
covers something nothing reaches, or a term that is genuinely redundant with
another and is now recorded as redundant rather than described as a guard.

### The two import-time checks this file has always called unreachable

`cli/exit_codes.py` carries a comment saying its band check and its
verb-producible check are unreachable today, because the range check above them
already excludes every code outside a reserved band. Reverting either alone kills
zero, which is what that comment predicts and is not evidence for it. The
composite makes both reachable and measures what each catches:

| row | deaths | collected |
| --- | --- | --- |
| `reserved-range-widened-to-the-whole-byte`, the control | 16 | 3414 |
| `a-process-band-code-reserved-with-the-range-widened` | 1 | **3186** |
| `a-process-band-code-reserved-with-the-band-check-dropped` | 18 | 3414 |
| `a-non-producible-code-reserved-past-the-range-and-the-band` | 1 | **3186** |
| `a-non-producible-code-reserved-with-the-producible-check-dropped` | 18 | 3414 |

The collected count is the reading here. A reservation in the process band, with
the range no longer excluding it, makes `cli/exit_codes.py` refuse AT IMPORT, so
228 tests never collect and the one death is the collection error. Drop the band
check and the module imports, the count returns to 3414, and 18 ordinary
assertions fail instead. The same pair reproduces for the producible check once
the band check is out of the way. So both checks bite exactly what they claim,
and both are unreachable only because the range is where it is.

### The four rows that pin an ABSENCE, and the injections that pair with them

An assertion that something is NOT there cannot die on a tree where it is not
there. Each is paired with the defect it watches for.

| row | deaths |
| --- | --- |
| `a-fresh-per-line-hatch-on-a-marker-the-fixtures-use` | 2 |
| `a-fresh-per-line-hatch-on-a-marker-nobody-guessed` | 1 |
| `a-fresh-hatch-nobody-guessed-with-the-structural-rule-relaxed` | **0** |
| `the-structural-rule-relaxed-alone` | **0** |
| `tokenize-imported-into-the-guard-module` | 1 |
| `tokenize-imported-with-the-whitelist-relaxed` | **0** |
| `the-import-whitelist-relaxed-alone` | **0** |

Read the first three together, because they are the round's leading finding
measured rather than argued. A fresh per-line escape hatch whose marker is one of
the five the fixtures append is caught twice, by the behavioural property and by
the structural rule. A fresh hatch whose marker NOBODY guessed is caught once,
and relaxing the structural rule takes that to zero. So the structural rule is
the only thing in the suite that catches an escape hatch nobody predicted the
spelling of, which is precisely what the fingerprint assertions it replaced could
not do.

The import whitelist reads the same way: adding `tokenize` to the guard module
kills exactly one test, and relaxing the whitelist from exact membership to a
superset takes it to zero.

### The two citation rows and the two heading rows

Both pairs are carried forward from the round before and both reproduce.

| row | deaths |
| --- | --- |
| `an-invented-title-in-a-covered-file` | 1 |
| `citation-reverse-direction-dropped` | **0** |
| `an-invented-title-with-the-reverse-direction-dropped` | **0** |
| `a-byte-identical-duplicate-heading` | 2 |
| `residual-headings-read-into-a-set-of-titles` | **0** |
| `a-duplicate-heading-with-the-headings-read-into-a-set` | **0** |

### Three terms that are genuinely redundant, and are now recorded as redundant

These are the rows where the honest answer is that the term cannot change an
answer, and each one is measured beside the thing that DOES catch the shape.

**`crossed-values-not-filtered-by-status`, 0.** `_crossed` filters the value side
by `status` before pairing. `reserved_code_tables` computes the status again for
every pair and drops the ones that answer None, so the filter cannot change what
is reported. Paired: `crossed-values-unfiltered-with-the-dedupe-dropped` kills 1,
and it is the SAME node id that `seen-dedupe-dropped` kills on its own, so
removing both together adds nothing to removing the dedupe alone. The filter is a
narrowing that saves work, not a guard, and it is written down as one.

**`imported-module-narrowed-to-tracked-dropped`, 0.**
`importlib.import_module("x").exit(30)` resolves to an identity, and the narrowing
keeps identities to the four tracked modules. Dropping it lets any imported name
become an identity, and nothing downstream can act on one: `_is_exit` requires the
identity to be a key of `EXIT_ATTRIBUTES`, which is `sys` and `os`. Paired:
`import-by-name-resolution-dropped` kills 2, so the path itself is covered twice
and only the redundant narrowing inside it is not.

**`setdefault-arm-deleted-so-the-catch-all-handles-it`, 0.** Deleting the
`setdefault` arm so those calls fall through to the catch-all that crosses every
call's arguments kills nothing, which reproduces exactly what the round before
claimed for it. Paired: `setdefault-arm-neutered`, which leaves the arm in place
and empties it so no arm handles the shape at all, kills 3. So the SHAPE is
covered three times and the specific arm is redundant. Its stated justification,
that it binds the key to its value by position rather than crossing them, cannot
be driven: `dict.setdefault` takes at most two arguments, so the crossing and the
positional binding produce the same pair on every input a real source can write.

### One entry in a whitelist that covers something nothing reaches

**`not-a-cause-loses-an-entry`, 0.** `NOT_A_CAUSE` classifies eleven package enums
as carrying context rather than a refusal cause, and the walk consults it only
where a declared enum appears in an exception's constructor annotations. Removing
the `cratekit.core.routing.Decline` entry kills nothing, because no exception in
the package annotates a `Decline`. Paired, on the same mapping:

| row | deaths |
| --- | --- |
| `not-a-cause-loses-an-entry`, the `Decline` entry | **0** |
| `not-a-cause-loses-the-scope-entry` | 6 |
| `not-a-cause-emptied` | 10 |

So the mapping as a whole is load bearing and that one entry is an exemption for
nothing. It is a finding rather than a curiosity, because an exemption nothing
reaches is exactly how a whitelist grows an entry that later switches a guard off
for free, which is what `TABLE_OWNERS` did on this branch two rounds ago. It is
carried by the residual
"One entry in the not-a-cause whitelist covers an enum the walk never reaches"
rather than closed, because closing it means deciding between deleting a
classification somebody made deliberately and adding a test that fails the moment
an unrelated unit stops annotating an enum.

### One set member the suite does not turn

**`enum-bases-narrowed-to-strenum-alone`, 0.** `ENUM_BASES` names the three
spellings the `enum` module offers for a vocabulary and is read only where a base
was imported under another name. The suite aliases `StrEnum` and does not alias
`Enum` or `IntEnum`, so narrowing the set to `{"StrEnum"}` changes nothing.
Paired: `enum-bases-emptied` kills 2. The two entries stay, with the reason
written above the set: a fixture for each would be a fixture for a spelling this
repository does not write.

## What moved, and against what

Nine rows carried forward from the round before reproduce exactly:
`review-walk-suffix-match` 5, `import-targets-fallback-sibling-dropped` 3,
`walk-off-the-top-clause-dropped` 1, `no-module-qualified-exitcode` 2,
`review-leaf-hardcoded` 1, `exit-code-leaf-hardcoded` 1,
`exit-code-class-spelled-again` 1, `no-resolution-through-branch-locals` 1 and
`seen-dedupe-dropped` 1.

Rows that moved upward moved because this round added 26 node ids across eleven
functions, and every one of them is a fixture for a guard that previously killed
nothing. The largest movers are the rows whose reverts break the key set, which
now takes the new enum and annotated-assignment fixtures with it:
`key-set-drops-the-registry` 40 to 44, `enum-declarations-off` 22 to 27,
`own-declarations-dropped-from-the-key-set` 25 to 26.

**The one row that moved for a reason worth naming is `attribute-exit-arm-dropped`
at 12.** It is not the row the round before would have run. The clause that stood
there, a dotted lookup against `self.exits`, was deleted this round as unreachable
by construction, so the row now reverts what is LEFT of that branch rather than
the dead tail, and 12 is the cost of the branch that is real.
