# U24 round 10, the INDEPENDENT mutation table

Derived by an agent that did not write the code, against the author's table in
`u24-round-10.md`. METHOD.md: an author's own table is a draft, not a result.

**72 rows, 14 zero rows.** The author's table is 39 rows and 1 zero row. Every
row of his that overlaps one of mine reproduces its count exactly, with one
instructive exception recorded below. His table is honest and incomplete, which
is the measured pattern on this project: 10 against 17, 39 against 49, 49 against
83, and now 39 against 72.

## How it was measured

* Driver in the agent's own scratch directory, run one row at a time. It
  snapshots each file's text in memory, rewrites it, and rewrites the snapshot
  back. **It never invokes git.**
* Restores verified after the run against `git show HEAD:<path>` piped to
  `shasum -a 256`, in a separate shell step, never against a scratch copy. All
  five mutated source files matched their `HEAD` blob digest and
  `git status --porcelain` named no source file.
* `PYTHONDONTWRITEBYTECODE=1` in every child. Every `__pycache__` under `src`
  removed before the first row.
* **No `-q` anywhere.** Counts from `pytest --tb=no`. The collected count and
  every failed node id are read from pytest REPORT OBJECTS in a plugin, never
  from stdout text.
* **The collected count is reported on every row.** It was 1206 on the baseline
  and on all 72 rows, no exceptions.
* Subset: the nine test files importing `tombstone`, `deletion.stores`,
  `deletion.library`, `deletion.run` or `deletion.candidates`. Baseline 1206
  collected, 1195 passed, 0 failed.
* Every zero on the subset was promoted to a full run before being reported as a
  zero. Full baseline 3504 collected, 3489 passed, 15 skipped.
* Each substitution was checked for a UNIQUE anchor before the run, so no row
  could silently edit the wrong occurrence, and no row could be a no operation
  because its anchor was absent.

**One artefact, named rather than hidden.** Three promoted full runs reported one
failure, `tests/test_portability.py::test_the_repository_itself_is_clean`, and in
every case the cause was a literal absolute path, either one this table's own
mutation text introduced into `src` or one in the verification report being
drafted alongside. It is the repository hygiene scan doing its job on the
measurement apparatus, not a guard dying. Those rows are recorded as zeros.

## The round 10 diff: the identity scheme stamp

| id | deaths | what was reverted, and what it means if it kills nothing |
| --- | --- | --- |
| V1 | **0** | `json.dumps` loses `sort_keys=True`, so a dict whose insertion order changes digests differently and one set of rules produces two stamps. |
| V2 | 1 | `ensure_ascii` flips to True, so a non-ASCII composed title is escaped before it is digested. |
| V3 | 1 | The digest becomes md5 rather than sha256. |
| V4 | 2 | The digest is truncated to 8 hex characters. A coefficient mutation, half the width. |
| V5 | 2 | The digest is truncated to 32 hex characters. The other direction of the same coefficient. |
| V6 | 1 | The probes are digested in reverse order, so reordering the tuple restamps identical rules. |
| V7 | **0** | The probe's `content_id` literal changes. |
| V8 | **0** | The probe's `recorded` value becomes a path. |
| V9 | 1 | The unbelieved value is dropped from the digest, which is the limb the docstring's second paragraph claims makes the vocabulary observable. |
| V10 | 8 | Only the unbelieved value is digested, dropping the composed identity, the believed version and the kind. |
| V11 | 2 | The probe filling BOTH version columns is removed, which is the only one pinning their order. |
| V12 | 3 | The featured-credit probe is removed, the only one exercising `_is_a_credit`. |
| V13 | 1 | The word-boundary probe is removed, the only one pinning `_already_carries`'s delimiting. |
| V14 | 1 | The unbelieved-Subtitle probe is removed, the only probe through which the vocabulary is observable at all. |
| V15 | 1 | The empty-artist probe is removed, so `version_identity`'s single-empty branch is unmeasured. |
| V16 | 1 | A duplicate of the first probe is added, which measures nothing new and restamps. |
| V17 | 6 | `_SchemeProbe` stops carrying `RemixerName` under that name, so the reader reads nothing there and every remixer probe degrades to the empty branch. The class docstring says the suite is where that is caught, and it is. |
| V18 | 3 | The same for `Subtitle`. |
| V19 | 10 | `identity_scheme` becomes a hand set constant, which is round 9's instrument. Author M5, same count. |
| V20 | 9 | The stamp is computed once at import and cached, so it is a snapshot of one process rather than a measurement of the rules in front of it. |
| V21 | 2 | `_SCHEME_PREFIX` changes, so a stored stamp never equals a computed one. Author M20, same count. |
| V22 | 1 | `IDENTITY_SCHEME_FIELD` is renamed, orphaning the stamp in every store the previous build wrote. Author M21, same count. |
| V23 | 2 | `record_tombstone` stops stamping the era. Author M11, same count. |
| V24 | 2 | `record_tombstone` stamps a CONSTANT, so every record claims one era for ever. |
| V25 | 2 | `summarize` stops emitting the era. Author M12, same count. |
| V26 | 1 | `summarize` defaults an absent era to this build's stamp rather than to empty, so a pre-stamp record reads as one of this build's. |

## The round 10 diff: the row coordinate

| id | deaths | what was reverted |
| --- | --- | --- |
| V27 | 1 | `_row_coordinates` accepts a `None` content identifier. Author M1, same count. |
| V28 | 2 | It accepts a boolean, and JSON carries booleans. Author M2, same count. |
| V29 | **0** | Only the `.strip()` limb of the blank guard is removed, so `""` is still refused and `"   "` is accepted. **The author's M3 reports 1 for this guard; it reports 1 for the guard REMOVED WHOLE, which is V30. The `.strip()` layer alone kills nothing.** METHOD: remove each guard layer alone. |
| V30 | 1 | The blank guard is removed whole. Author M3, same count. |
| V31 | 1 | The recorded path stops being composed to NFC. Author M4, same count. |
| V32 | **0** | The recorded path is composed NFD rather than NFC. |
| V33 | **0** | A null recorded value folds to the text `None` rather than to empty. This is the `str(None)` shape the module says it has closed "at four doors", on the OTHER half of the same pair. |
| V34 | **0** | The recorded path is also case-folded. |
| V35 | **0** | The recorded path is dropped from the key entirely, so the coordinate is the content identifier alone. |
| C1 | **0** | The content identifier is dropped from the key entirely, so the coordinate is the path alone. The composite pair to V35. |

## The round 10 diff: the recogniser

| id | deaths | what was reverted |
| --- | --- | --- |
| V36 | 1 | A record of any KIND contributes a row key, so a decline in the tombstone store answers the tombstone question. Author M16, same count. |
| V37 | 11 | The kind test is inverted, so a version record is skipped. Author C16, same count. |
| V38 | 10 | No record is ever matched on its row, which is the round 9 behaviour. Author M13, same count. |
| V39 | 1 | Every record is matched on its row, so the stamp decides nothing. Author M14, same count. |
| V40 | 11 | The era test is INVERTED, so this build's records fall to the row lookup and every other era is trusted on its identity. |
| V41 | **0** | The `or ""` coalesce is removed, so a payload carrying null compares `None` against a string. |
| V42 | 10 | The row key is built from the payload's `resolved` rather than its `recorded`. |
| V43 | 10 | The row key is built from the payload's `title` rather than its `content_id`. |
| V44 | 1 | The `is not None` filter on the coordinate is removed. Author M15, same count. |
| V45 | 10 | The row lookup is skipped. Author M17, same count. |
| V46 | 10 | The row lookup is asked with the row's artist rather than its recorded path, so the two sides stop being the same function. |
| V47 | 1 | `except Exception: return False` becomes `return True`. B4, author M18, same count. |
| V48 | 1 | Revoked records stop counting. Author M19, same count. |
| V49 | **0** | An extra per-row store read is added. **This row is DEFECTIVE and is recorded rather than dropped: it adds a read and changes no behaviour, so it could never kill anything.** It is here because the author recorded two defective rows of his own and the honest thing is to do the same. |

## The composites

Every zero row is paired with a mutation of the thing it guards.

| id | deaths | what it shows |
| --- | --- | --- |
| C3 | 10 | The digest is fed one constant per probe instead of the probe's own values. The digest INPUT is load bearing; `sort_keys` (V1) is framing on top of it. |
| C4 | 1 | A probe's ARTIST changes, which the composed identity does read. The probe TUPLE is load bearing; the probe's row-coordinate fields (V7, V8) are not read by anything the digest sees. |
| C5 | **0** | `tombstone.removed_file_identity` composes NFD rather than NFC. Paired with E5 below, and it is a zero of its own rather than a composite that closes one. |
| V30 | 1 | closes V29. |
| V31 | 1 | closes V32, V34 and E5: the NORMALISATION is load bearing, the CHOICE of form is not. |
| V27 | 1 | closes V33: the `str(None)` shape is pinned on the content identifier and not on the path. |
| V43 | 10 | closes V35 and C1 on the RECORD side: reading the wrong payload field kills 10, while reading BOTH fields correctly and then discarding one kills nothing. |
| V45 | 10 | closes C2: the row lookup itself is heavily pinned; only the STRUCTURAL name test around it is not. |
| V38 | 10 | closes V41. |
| V48 | 1 | closes V49. |

## The zero rows, all 14

The 14 split three ways: five are equivalent or defective, eight are real
coverage holes sharing one cause, and one is a finding of its own.

### The five that are equivalent or defective

* **V1**, `sort_keys`. `composed` is built by `version_identity`, which always
  inserts `artist` then `title`, so sorting is a no operation for every value the
  probes can produce. Equivalent. C3 kills 10.
* **V7 and V8**, the probe's `content_id` and `recorded`. `version_of` reads
  neither, and the digest is over the composed identity, the version, the kind
  and the unbelieved value. Equivalent. C4 kills 1.
* **V41**, the `or ""` coalesce. `None != scheme` is already True for a string
  `scheme`, so the coalesce changes no branch. Equivalent. V38 kills 10.
* **V49**, defective by construction, declared above.

### The eight that are real coverage holes, and they share one cause

**`_row_coordinates` is applied to BOTH sides of the comparison, so no test can
see any change to it that is symmetric.** The docstring names this property as
the safety argument: "Both sides of every comparison here run through this one
function in one build, which is the whole difference from the composition case."
That is true, and it is exactly what makes the function unmeasurable. Six
mutations of it kill zero on the full suite:

* **V29**, the `.strip()` layer alone.
* **V32**, NFD instead of NFC.
* **V33**, a null path folded to the text `None`.
* **V34**, the path case-folded.
* **V35**, the path dropped from the key.
* **C1**, the identifier dropped from the key.

Only ASYMMETRIC mutations kill: V27 and V28 kill because a record can carry a
null or a boolean that a row cannot; V30 kills because a record can name a blank
that a row cannot; V31 kills because the test plants a record whose path is
spelled the other way; V44 kills because a record can name nothing.

So every property of the row coordinate that the two sides share is pinned by
nothing, and V35 and C1 say that neither half of the documented pair carries its
own weight in any test. Recorded as a residual: the code is correct today, and a
future edit to this function is invisible.

**E5**, `tombstone.removed_file_identity` dropping NFC, and **C5**, the same
function composing NFD, are the same shape one module over: the decline store's
identity is composed by one function on both sides, so a symmetric change to it
is invisible too. V31 kills 1 because `_row_coordinates`, the SECOND
implementation of that same rule, is asymmetrically testable. The authority's
copy is unpinned and the copy is pinned.

### C2, and it is a finding rather than a hole

**C2, 0 deaths on the full suite.** A new function is added to `tombstone` that
reconstructs what a former build composed, under the name
`legacy_version_title`. `test_nothing_reconstructs_a_former_builds_composition_any_more`
refuses only the substrings `before_the`, `earlier_builds` and `historical`, so
it passes. The test's docstring says it refuses the shape "whatever it is
called". It refuses round 9's three names.

## The fixed sample of U24's existing guards

| id | deaths | what was reverted |
| --- | --- | --- |
| E1 | 1 | `identifiable` stops asking for the ROW identity and asks only for the version's. |
| E2 | 23 | `version_of` composes a remixer as though it were a designation. Author E2, same count. |
| E3 | 2 | `removed_file_identity` accepts a boolean, so its guard and `_row_coordinates`'s stop agreeing. |
| E4 | 4 | `removed_file_identity` accepts a blank identifier, the other half of the same duplicated rule. |
| E5 | **0** | `removed_file_identity` stops composing the recorded path to NFC. |
| E6 | 4 | `version_identity` accepts an identity with neither field. |
| E7 | 8 | `_already_carries` reads a featured credit group as a version group. |
| E8 | 2 | `_is_a_credit` tests the whole group rather than its head word. |
| E9 | 9 | `already_spelled_as_a_remix` tests the first word rather than the last. |
| E10 | 13 | `version_title` composes an empty bracket for every ordinary row. |
| E11 | 1 | `version_title` folds the untidied value while composing the tidied one. |
| E12 | 13 | `library._version_of` believes any `Subtitle` at all. |
| E13 | 3 | `library._version_of` drops what it did not believe rather than carrying it out. |
| E14 | 2 | `library._identifier` folds an absent identifier to the text `None`. |
| E15 | 2 | `ambiguous_versions` folds the ISRC as free text rather than as a structured code. |
| E16 | 1 | `run._settle_a_confirmed_absence` settles even where the anchor proved nothing. |
| E17 | 2 | `run._settle_a_confirmed_absence` settles a row a run already recorded. |
| E18 | 3 | `candidates.categorize` stops asking identifiability first, so an unidentifiable row whose file is absent is reported GONE. |

## The drift rows, which are finding 1

These are not guard reverts. They are PLAUSIBLE FORWARD CHANGES to a composition
rule, applied as source edits, and what they measure is whether anything at all
notices.

| id | deaths | the change |
| --- | --- | --- |
| A1 | 4 | `VERSION_WORDS` gains `refix`, a designation the constant's own docstring names as missing. |
| A2 | 2 | `VERSION_WORDS` loses `club`, which the same docstring names as a false positive. |
| A3 | **0** | `_CREDIT_MARKERS` gains `vs`. Full run: 3504 collected, 3489 passed, 0 failed. |
| A4 | **0** | `fold` normalises NFKC rather than NFC, the form `fold_code` already uses. Full run: 3504 collected, 3489 passed, 0 failed. |
| A5 | **0** | `_BRACKET_CHARACTERS` also tidies braces. Full run: 3504 collected, 3489 passed, 0 failed. |

A1's four deaths by node id, none of which is a history test or a stamp test:

* `test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
* `test_the_collision_is_looked_for_across_the_whole_walk_not_the_offered_rows`
* `test_the_version_vocabulary_is_exactly_this_set_and_no_other`
* `test_two_recordings_that_land_on_one_identity_are_refused_rather_than_suppressed`

Each of the five moves a real row's composed identity. **None of the five moves
the stamp.** See `docs/u24-round-10-verification.md` for the end to end drive and
the user facing cost.

## Reconciliation with the author's 39

Every row of his that maps onto one of mine reproduces its count: M1, M2, M3,
M4, M5, M10 as a coefficient, M11, M12, M13, M14, M15, M16, M17, M18, M19, M20,
M21, C16, and six of his existing-guard rows. **His table is accurate.**

The one instructive difference is M3. He reports 1 death for the blank guard,
and 1 is what the guard kills when it is removed WHOLE. Removing only its
`.strip()` layer kills nothing, so the finer layer of a two-layer guard is
unmeasured and his row cannot see that.

What his 39 rows do not reach, measured here: the digest's serialisation
(V1 to V3, V9, V10), the digest width in both directions (V4, V5), the probe
ORDER (V6), seven individual probe rows (V11 to V16), the probe class's own
column names (V17, V18), the on-demand computation (V20), a constant stamp
(V24), `summarize`'s default (V26), five properties of the row coordinate
(V29, V32 to V35, C1), the inverted era test (V40), two wrong payload fields
(V42, V43), the asymmetric row key (V46), five existing guards (E3, E4, E5, E13,
E14, E16, E18), and the five drift rows that are the blocking finding.
