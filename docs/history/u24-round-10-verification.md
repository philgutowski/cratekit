# U24 round 10, independent verification

Written by an agent that did not write the code, under METHOD.md's full
adversarial pass, which is what this unit gets because it deletes.

Worktree `.worktrees/u24`, branch `unit/u24-track-deletion-and-tombstones`,
verified at tip `2815e4a`, with its own venv and its own scratch directory.

The independent table is `docs/mutation/u24-round-10-independent.md`: 72 rows,
14 zero rows, against the author's 39 and 1.

## Verdict

**BLOCKING, one finding.**

Round 10 says it ends the class by removing reconstruction: nothing recomputes
history, the identity scheme version is stamped into the record at write time,
and reading history is a lookup. **The removal of reconstruction is real and it
is correct.** The stamp is where the drift went.

**Finding 1 is the fifth consecutive instance of this branch's signature
failure.** Round 9 froze the composers and did not freeze what the composers
call. Round 10 digests the composer's OUTPUT over a fixed set of 23 probe rows
and does not cover the INPUTS that a composition rule change actually fires on.
One level down, again.

Everything else measured is a residual or a verified claim.

## Finding 1, BLOCKING. A composition rule change that does not move the stamp

### What the stamp promises

`stores.identity_scheme()` runs 23 frozen probe rows through
`library._version_of` and `stores.version_of` and digests the four values that
come out. `tombstone_predicate` reads a record's stamp: equal to this build's,
the record is matched on its identity; anything else, the record is matched on
the row it names.

So the stamp has to move whenever a change to any composition rule moves any
real row's identity. Its own docstring on `_SCHEME_PROBES` states the required
direction: "the bias is toward moving the stamp too often rather than too
rarely." The measured bias is the opposite for the commonest class of change.

### The probe, 19 candidates

Each candidate was applied by rebinding the module global that the live code
reads at call time, which is what a source edit does, and the stamp was compared
against the composed identity of a real rekordbox row shape.

**16 of the 19 moved a real row's composed identity without moving the stamp.**

| candidate | stamp moved | a real row's identity moved |
| --- | --- | --- |
| `VERSION_WORDS` gains `refix` | no | `strobe` becomes `strobe (refix)` |
| `VERSION_WORDS` gains `redux` | no | `strobe` becomes `strobe (redux)` |
| `VERSION_WORDS` gains `vocal` | no | `strobe` becomes `strobe (vocal)` |
| `VERSION_WORDS` gains `acappella` | no | `strobe` becomes `strobe (acappella)` |
| `VERSION_WORDS` gains `nightcore` | no | `strobe` becomes `strobe (nightcore)` |
| `VERSION_WORDS` gains `slowed` | no | `strobe` becomes `strobe (slowed)` |
| `VERSION_WORDS` gains `rmx` | no | `strobe` becomes `strobe (rmx)` |
| `VERSION_WORDS` gains `dubplate` | no | `strobe` becomes `strobe (dubplate)` |
| `VERSION_WORDS` gains `versión` | no | `strobe` becomes `strobe (versión)` |
| `VERSION_WORDS` gains `bootie` | no | `strobe` becomes `strobe (bootie)` |
| `_CREDIT_MARKERS` gains `vs` | no | `losing it (vs anna)` gains a remix bracket |
| `_CREDIT_MARKERS` gains `x` | no | `losing it (x anna)` gains a remix bracket |
| `fold` normalises NFKC rather than NFC | no | a fullwidth artist folds to ASCII |
| `fold` drops normalisation entirely | no | a decomposed title stops equalling its composed spelling |
| `_BRACKET_CHARACTERS` also covers braces | no | `strobe ({extended mix})` becomes `strobe (extended mix)` |
| `_BRACKETED` also matches braces | no | a title carrying its version in braces stops composing a second one |
| `REMIX_DESIGNATION` becomes `Remix Edit` | **yes** | yes |
| `_WORD_SPLIT` keeps apostrophes | no | no |
| `_VERSION_COLUMNS` gains a third column below the two | no | no |

`VERSION_WORDS` is the sharpest of these because the constant's own docstring
names the missing spellings: "``Acappella``, ``Vocal``, ``Refix``, ``Redux``,
``Rmx``, ``Dubplate``, ``Nightcore``, ``Slowed``, ``12 Inch``, ``Ao Vivo``,
``Versión`` and the rest of a long tail". Adding one of those is not a
hypothetical future change. It is the change the code asks for in writing.

### What the suite sees, which is the round 9 measurement shape verbatim

Five candidates were then applied as SOURCE EDITS and run against the suite.
Baseline subset 1206 collected, 1195 passed, 0 failed. Every row collected 1206.

| row | the edit | deaths | promoted to the full suite |
| --- | --- | --- | --- |
| A1 | `VERSION_WORDS` gains `refix` | 4 | |
| A2 | `VERSION_WORDS` loses `club`, which its own docstring calls a false positive | 2 | |
| A3 | `_CREDIT_MARKERS` gains `vs` | **0** | 3504 collected, 3489 passed, 0 failed |
| A4 | `fold` normalises NFKC rather than NFC | **0** | 3504 collected, 3489 passed, 0 failed |
| A5 | `_BRACKET_CHARACTERS` also tidies braces | **0** | 3504 collected, 3489 passed, 0 failed |

A1's four deaths, by node id:

* `test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
* `test_the_collision_is_looked_for_across_the_whole_walk_not_the_offered_rows`
* `test_the_version_vocabulary_is_exactly_this_set_and_no_other`
* `test_two_recordings_that_land_on_one_identity_are_refused_rather_than_suppressed`

**None of them is a history test and none of them is a stamp test.** The only one
that speaks to the change at all is the exact-membership pin, and what it says is
"you edited the list", which is precisely what the person editing the list
intended. It is a number somebody remembers to bump, which is the instrument this
round exists to replace. They bump it, the suite goes green, and the stamp has
not moved.

Round 9's B1 was reported in exactly this shape: "the literal pinning that was
supposed to make drift go red kills 5 tests, none of them a history test."

### Why the author's 10 of 10 does not contradict this

`test_the_stamp_moves_when_any_rule_below_it_moves` parametrises nine drifts and
every one of them is a WHOLESALE REPLACEMENT that destroys behaviour the probes
already cover:

* `_CREDIT_MARKERS` to `frozenset()`, which removes `feat`, and probe 11 carries
  a featured credit.
* `VERSION_WORDS` to `frozenset({"remix"})`, which removes `extended`, `mix` and
  `live`, all three of which probes carry.
* `fold` to a function that drops NFC AND casefold, and probe 20 is an
  upper-case artist.
* `_as_a_bracketed_value` to the identity function, and probe 6 carries a
  whitespace run.
* `_already_carries` to a substring test, and probe 13 is the `Lively Up`
  against `Live` shape.
* `_VERSION_COLUMNS` reversed, and probe 10 fills both columns.

Every parameter SUBTRACTS covered behaviour. Not one ADDS a rule that fires on an
input no probe carries, which is the direction a real forward change takes. The
set of drifts tried is the set the probes cover, and the 10 of 10 measures that
rather than the property it is named for.

### The drive, end to end, on a real store

Build A, the tree exactly as `2815e4a` has it. A rekordbox row: artist
`deadmau5`, title `Strobe`, `Subtitle` `Refix`, `RemixerName` empty.

* `library._version_of` answers `version=''`, `unbelieved='Refix'`, because
  `refix` is not in `VERSION_WORDS`.
* `stores.version_of` composes `{'artist': 'deadmau5', 'title': 'strobe'}`.
* `stores.record_tombstone` writes it with `trashed_to` naming the Trash and
  `identity_scheme` `is1_898ad13cd09eeffd`.
* Build A's own predicate answers True. Correct.

Build B, which differs from build A by the one word.

* stamp: `is1_898ad13cd09eeffd`. **Unmoved.**
* `library._version_of` now answers `version='Refix'`.
* `stores.version_of` now composes
  `{'artist': 'deadmau5', 'title': 'strobe (refix)'}`.
* The record on disk carries build B's own stamp, so it is NOT put into
  `rows_recorded_under_other_rules`, so the row lookup never runs for it.
* `stores.tombstone_predicate(cfg)(row)` answers **False**, with the record
  sitting in the store.

### The user facing cost, measured on the shipped run paths

Three costs, all produced by handing that False to the two functions in `run`
that consume it.

**Cost A, the person is told something false.**
`run._warn_that_an_unanswered_removal_is_being_retired` emits, verbatim apart
from the path:

> removal 4242 was retired without being offered: the file is not at [the path
> the row recorded] and no tombstone records this library ever deleting it, so
> there is nothing to move and nothing to record. If you deleted it yourself
> that is the end of it; if you MOVED it, the file is still on this disk outside
> the collection and nothing will offer it again

A tombstone does record this library deleting it, and it names the Trash path the
file was moved to. This log line is the only notice the person gets.

**Cost B, a duplicate record.** `run._settle_a_confirmed_absence` writes a SECOND
tombstone. The store goes from one record to two, one under `strobe` and one
under `strobe (refix)`, both carrying the same stamp, and the person is told the
deletion "has been RECORDED anyway" and named the new suppression to revoke.

**Cost C, and this is the one that blocks a verb.** Under a suspect anchor,
`_settle_a_confirmed_absence` returns False rather than True, so the row is NOT
retired, the watermark holds at it, and the person is told:

> confirmed removal 4242 is not at [the path] and NOTHING WAS RECORDED ... Mount
> the volume and run this again; the removal is still open and every removal
> after it is waiting behind it

The same call with a predicate that answers True, which is the truth, returns
True and retires the row. The watermark is contiguous, so one row answered wrong
holds every removal behind it.

Both floor conditions are met. It was driven end to end through the shipped
predicate and the shipped `run` helpers on a real store on disk, not argued from
reading the source, and the cost is named: the person is told something false,
and a removal that was completed and recorded blocks the queue.

### What would close it

The stamp measures OUTPUTS over a fixed input set, so it can only see a rule
change that moves one of those 23 outputs. Digest the RULE INPUTS as well: the
sorted membership of `VERSION_WORDS` and `_CREDIT_MARKERS`, the value of
`REMIX_DESIGNATION`, the pattern strings of `_SPACING`, `_BRACKETED`,
`_BRACKET_CHARACTERS` and `_WORD_SPLIT`, the contents of
`library._VERSION_COLUMNS`, and a hash of the code objects of `fold`,
`_already_carries`, `_is_a_credit`, `already_spelled_as_a_remix`,
`remixer_title`, `version_title`, `version_identity` and `library._version_of`.
A digest over the call tree's own code plus its vocabulary moves on every change
by construction, which is the direction `_SCHEME_PROBES` already declares safe.
The output probes then stay, as the check that the code hash is not vacuous.

## Finding 2, RESIDUAL. The row coordinate is unmeasurable by construction

`_row_coordinates` is applied to BOTH sides of the comparison. The docstring
names that as the safety argument: "Both sides of every comparison here run
through this one function in one build, which is the whole difference from the
composition case." That is true for correctness, and it is exactly what makes
the function invisible to the suite.

**Six mutations of it kill zero on the full suite**, each promoted from the
subset and each run at 3504 collected, 3489 passed, 0 failed:

* the `.strip()` layer of the blank guard alone;
* NFD instead of NFC;
* a null path folded to the text `None` rather than to empty, which is the
  `str(None)` shape this module says it has closed at four doors, arriving on the
  other half of the same pair;
* the path case-folded;
* the path dropped from the key entirely;
* the identifier dropped from the key entirely.

Only ASYMMETRIC mutations kill, and they kill because a RECORD can carry a value
a ROW cannot: a null, a boolean, a blank, a differently normalised path. Every
property the two sides share is pinned by nothing.

**Cost, and why it is a residual.** Dropping either half means a record about one
row retires a different row that shares the other half, which is a deletion
surface. It is reachable only through a record whose stamp is not this build's,
so today only through a store written by an unmerged branch tip, which the floor
puts out of scope. The code is correct as written. What is not measured is that
it stays correct.

The same shape appears one module over: `tombstone.removed_file_identity`
dropping NFC, and composing NFD instead, both kill zero.

## Finding 3, RESIDUAL. One rule, two implementations, in two modules

`stores._row_coordinates` guards with `content_id is None`, `isinstance(content_id,
bool)` and `not str(content_id).strip()`, which is a verbatim re-implementation
of `tombstone.removed_file_identity`'s guard, in a different module, with nothing
asserting that the two agree. The `_row_coordinates` docstring names
`removed_file_identity` as the authority for the NFC rule, on the grounds that
"two rules for one field is how the two come to disagree", and then writes the
second rule.

They agree today. Measured: weakening `removed_file_identity` alone kills 2 for
the boolean layer and 4 for the blank layer, and 0 for the normalisation layer,
while the copy in `stores` kills 1 for the same normalisation layer. The
authority's copy is the less pinned of the two.

## Finding 4, RESIDUAL. The no-reconstruction test forbids three substrings

`test_nothing_reconstructs_a_former_builds_composition_any_more` refuses any name
in `tombstone` or `stores` containing `before_the`, `earlier_builds` or
`historical`. Its docstring says it refuses the shape "whatever it is called".

**Driven.** A function that reconstructs what a former build composed was added
to `tombstone` under the name `legacy_version_title`. Subset deaths 0; full run
3504 collected, 3489 passed, and the single reported failure was the repository
hygiene scan reacting to a literal path in this report's own draft, not a test of
the feature.

This is METHOD's "a test that forbids a feature by naming the last
implementation's symbols" precisely: it forbids round 9's three names, not the
class. No user facing cost today, so residual.

## Finding 5, RESIDUAL. The removal identity is not byte identical, and the
## measurement that says so was taken on a probe

The residual titled "Three more stored decisions are addressed by a key a later build recomputes" rests on this sentence: "the ROW identity `removed_file_identity(content_id,
recorded)` was rebuilt at all eleven commits on this branch and evaluated on one
probe row, and it produced a byte identical answer at every one of them."

Measured over all 19 commits on the branch by parsing each commit's blob:
`tombstone.removed_file_identity` takes **four distinct forms**, changing at
`c02a7b4`, `c087439` and `df945fb`.

What is identical at every commit is the RETURN expression. Every change widened
the REFUSAL GUARD:

* through `5cb1ed3`: `if not str(content_id)`
* `c02a7b4`: `if content_id is None or not str(content_id)`
* `c087439`: adds `.strip()`
* `df945fb`: adds `isinstance(content_id, bool)`

So the conclusion holds for every input that produces an identity at all, and the
set of inputs that produce one shrank three times. A probe row that produces an
identity cannot see that, which is METHOD's fourth pattern: a number taken on a
fixture rather than over the input space.

A decline recorded by a pre-`c087439` build for a whitespace content identifier
is now refused rather than composed, and `decline_predicate` has no handler, so
it would raise. Driven: unreachable, because `candidates.categorize` asks
`identifiable` first and unconditionally and answers UNIDENTIFIABLE, so
`decline_predicate` is never asked about such a row through the pass. The only
store that could carry such a record is one written by an unmerged branch tip.
Not blocking.

## Verified claims, no finding

**Attack 3, the stamp comparison. Nothing.** Eleven stamp shapes were planted in
real records whose identity this build would never compose, so only the row
lookup could match them, and the branch each took was read off the answer:

| stamp in the payload | branch taken |
| --- | --- |
| absent | row lookup, read as history |
| `null` | row lookup |
| empty string | row lookup |
| whitespace | row lookup |
| truncated to 8 characters | row lookup |
| prefix only, `is1_` | row lookup |
| an integer | row lookup |
| a boolean | row lookup |
| a list | row lookup |
| a foreign era `is1_0000000000000000` | row lookup |
| THIS build's stamp | identity only, read as current |

There is no corner that reads as the current era when it should read as history.
The `str(... or "")` coalesce lands every malformed shape on the safe side.

**Attack 4, the migration path. The claim holds, and holds wider than claimed.**
Every one of the 19 commits on this branch writes `content_id` AND `recorded`
into the tombstone payload, measured by parsing the `record_tombstone` payload
dict out of each commit's blob. "Nothing to migrate" is true. The author's count
of eleven is an undercount of the commits; the conclusion is unaffected. Thirteen
of the 19 touch `src`.

The same sweep confirms that residual's premise: the DECLINE payload carries `recorded` at
all 19 commits and `content_id` at none of them.

**Attack 5, B4's reachability. The author's statement is exact.** Driven through
the shipped `categorize` with `stores.identifiable` wired as `run.plan` wires it:

| row shape, file genuinely absent, anchor present | category | `version_of` raises |
| --- | --- | --- |
| ordinary | gone | no |
| artist and title both empty | unidentifiable | yes |
| artist and title both whitespace | unidentifiable | yes |
| content identifier blank | unidentifiable | no |
| content identifier empty | unidentifiable | no |

Only a row where `version_of` raises can reach `except Exception: return False`,
and every such row is UNIDENTIFIABLE rather than GONE. The predicate's only
caller in `src` is `run.py:796`, and both consumers return early unless the
category is GONE. So the branch is unreachable through the pass and reachable
through the exported predicate, which is where the test asks it. B4 stays a
residual, as round 9 classified it.

One thing worth carrying: `categorize`'s `identifiable` parameter DEFAULTS to
`lambda _row: True`, a permissive default on the guard that makes this
unreachable, and `candidates.recheck` calls `categorize` without it. That is safe
today only because `recheck` sees nothing the plan did not already call
deletable.

**Attack 6, M8's equivalence. It holds.** `library._version_of` returns either
`("", "", unbelieved)` or `(found, holds, unbelieved)` with `holds` non-empty, so
an empty kind implies an empty version by construction. With an empty version,
`version_of` returns `title` through either branch, so `version_kind=kind` and
`version_kind=kind or VERSION_IS_A_DESIGNATION` cannot differ for any input the
reader can produce. The raw `kind` is separately digested, so the mutation
touches only the composed value. Genuinely equivalent.

The equivalence rests on an invariant of `_version_of` that nothing asserts
directly. If a future reader returns a kind-less believed version, M8 stops being
equivalent silently.

**Attack 7, the stamp pin.** An AST walk over every `assert` in `tests/` finds 7
that name the identity scheme. Exactly one pins a literal, at
`tests/test_deletion.py:5513`. It is a literal, not a recomputation, and it is
the value this tree actually produces. The author's claim is correct.

Two of the seven take their expected value from the code under test, which the
test's own comment acknowledges and pairs with a shape assertion.

The same walk finds 30 asserts whose two sides call the same production function.
All 30 are property assertions over two different inputs rather than X equals X,
and they are legitimate; they do carry the weakness the author names, that an
inequality survives any change moving both sides together. That weakness is what
finding 2 measures.

**Test identifiers reconciled by name, not by total.** Round 9 tip carried 181
test functions in `test_deletion.py`, round 10 carries 193: 16 added, 4 removed.
All four removals name the deleted feature
(`test_a_tombstone_the_previous_build_wrote_is_still_recognised`,
`test_an_ordinary_row_offers_no_earlier_spelling`,
`test_both_preceding_spellings_are_offered_where_they_differ`,
`test_the_frozen_history_does_not_move_when_the_live_composer_does`) and are
replaced by the 16. No accidental removal.

**Duplicate mapping keys.** An AST sweep of every dict and set literal in `src`
finds none. `_SCHEME_PROBES` holds 23 rows, 23 distinct.

**No test names the deleted symbols.** `version_title_before_the_value_was_tidied`,
`remixer_title_before_the_value_was_tidied` and `spellings_earlier_builds_wrote`
appear nowhere in `src`, `tests` or `scripts`, only in `docs/mutation-rows.md` as
history.

## How everything here was measured

* Driver in the scratch directory, one row at a time, files snapshotted in memory
  and rewritten back. **The driver never invokes git.**
* Restores verified against `git show HEAD:<path>` piped to `shasum -a 256`,
  taken in a separate shell step, never against a scratch copy. All five mutated
  source files matched their `HEAD` blob digest afterwards and
  `git status --porcelain` named no source file.
* `PYTHONDONTWRITEBYTECODE=1` in every child, and every `__pycache__` under `src`
  removed before the first row.
* No `-q` anywhere. Counts from `pytest --tb=no`; the collected count and every
  failed node id are read from pytest report objects in a plugin, never from a
  `FAILED` line split on `" - "`.
* Collected count checked on every row: 1206 on the baseline and on all 72.
* Every zero on the subset promoted to a full run before being reported.
* Each substitution's anchor was checked for uniqueness before the run, so no row
  could edit the wrong occurrence or be a no operation.

## The battery, at `2815e4a`

    ./.venv/bin/ruff check src tests scripts       All checks passed
    ./.venv/bin/python -m pytest --tb=no           3489 passed, 15 skipped
    ./.venv/bin/python scripts/scan_repo.py        exit 0

    pytest --collect-only -o addopts=              3504 collected

## Unmeasured, and named as unmeasured

* **Whether rekordbox reuses a content identifier after a hard delete, and
  whether it rewrites `FolderPath` on a soft-deleted row during a relocate.**
  Either would make the row coordinate name a different thing than it named when
  the record was written. The live database is off limits, so this was not
  driven. It is the reachability question behind finding 2's cost.
* **Whether the tombstone store should be bound to `database_identity`.** It is
  not today, so a rebuilt library shares one store with the library it replaced,
  and content identifiers restart. Not driven, for the same reason.
* **A second, independently written composition rule change applied by a person
  rather than by this table.** Finding 1's five source edits are the ones an
  adversary chose; the population of plausible future changes was not sampled.
