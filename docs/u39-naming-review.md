# U39 independent adversarial review

Commits `311ab67` ("feat(naming): write the padded Camelot form and carry the
head through name.apply") and `3147600` ("test(mutation): U39 author table,
fourteen rows, every row killed"), branch
`unit/u39-camelot-padding-at-write-time-and-name-a`, GitHub issue #57.

Reviewed by an agent that did not write the code, in its own worktree
(`git worktree add --detach <repo> 3147600`), with its own virtual
environment built from the system Python 3.12 and verified to resolve
`cratekit` to that worktree's own `src`.

Paths in this file are written as `<repo>` and `<scratch>` because the
repository's own portability scan refuses an absolute home directory in a
shipped artifact.

## Verdict

**CLEAN.** No finding met all three conditions of the merge bar in
`docs/METHOD.md`. Every scenario the issue brief names was driven end to end
against real audio files through the real dispatcher (`cratekit.cli.run`) and
matched the brief exactly, including the specific hazard this unit exists to
fix (`01A - 124 - Cola.flac` no longer collapses to `Cola.flac`). The registry
correction is accurate: `name.apply`'s handler opens no database.

The independent mutation table below runs 22 rows, eight more than the
author's 14, and finds five zero-death rows on user-facing lines the author's
table did not touch, plus one on a maintainer-facing line. All five user-facing
zeros meet METHOD's composite requirement: each is paired with a neighboring
mutation on the same code that DOES kill, and each is additionally paired with
a hand-built scratch driver scenario (`drive_u39.py`, not part of the shipped
suite) that confirms the shipped code's actual behaviour on the exact branch
the zero row touches is correct. That combination is why none of the five
rises to BLOCKING: the shipped code is right when driven, the shipped test
suite just does not pin it. Those six rows collapse into FIVE findings,
because `K1` and `K2` are the two halves of one finding, and they are filed
as residuals R-166 through R-170.

| # | Finding | Class | Measured cost |
|---|---------|-------|---------------|
| 1 | The lossy marker's `or` has two live branches; the shipped suite exercises only the case where both are true at once | residual (R-166) | zero kills on `K1`/`K2`; composite: `K3` (same line region) kills 1; scratch scenario G shows the shipped code correctly recovers a title-only marker, and a title-only-branch mutation would silently stop doing so |
| 2 | Filename-first / title-second head-recovery precedence is stated in the commit message but pinned by no test where the two heads disagree in VALUE | residual (R-167) | zero kills on `R3`; composite: `R1`/`R2` (same code region) each kill 1; scratch scenario E shows the shipped code does prefer the filename when a stale title disagrees |
| 3 | `_spec_for`'s `stem` must come from the title tag's BODY text, not the raw filename stem, and no shipped test makes the two disagree outside the head | residual (R-168) | zero kills on `R8`; composite: `R4`/`R6`/`K3` (same function) kill 6/1/1; scratch scenario H shows the shipped code correctly prefers a corrected title's body over a stale filename body |
| 4 | CUT.md's reconciliation of `dj-pad-camelot` is prose only; no test guards the reverse direction of `test_every_source_entry_point_is_either_mapped_or_written_down_as_cut`, so the exact contradiction this unit fixed (claimed by a verb's `source_scripts` while CUT.md called it not ported) is not guarded against recurring | residual (R-169), maintainer-facing, no composite required | zero kills on `CUT1`, promoted to a full-suite run before being reported |
| 5 | The Camelot regex's end anchor (`$`) has zero test coverage; a regression dropping it would let `"1Axyz"` wrongly validate | residual (R-170), existing-guard sample, not part of this round's diff | zero kills on `E3`, promoted to a full-suite run; confirmed by direct interpreter check that the shipped anchor correctly rejects `is_camelot("1Axyz")` and `parse_camelot("1Axyz")` today |

## Battery, from inside the worktree with its own venv

    ./.venv/bin/ruff check src tests scripts        All checks passed
    ./.venv/bin/python -m pytest --tb=no             6253 passed, 1 skipped in 277.52s
    ./.venv/bin/python scripts/scan_repo.py          exit 0, no output

    pytest --collect-only -o addopts=                6254 collected

Matches the author's own mutation table baseline (`docs/mutation/u39-author-full.md`:
"Baseline: green, 6254 collected") exactly, and the worktree's `src` was
confirmed to be the one under test (`python -c "import cratekit,os;
print(os.path.abspath(cratekit.__file__))"` resolved inside `<repo>/src`, not
the main checkout's).

`RESTART-cratekit.md`'s "last measured suite" of 6239 passed predates this
branch by other units landing in between; it is not the comparison point.

## Mutation headline

Full pass, driven by `scripts/mutate.py` from inside the review worktree.
Table and JSON sidecar at `docs/mutation/u39-naming-independent.md` and
`.json` (spec at `docs/mutation/u39-naming-independent.toml`).

    rows run              22 (author ran 14; 8 of these are new)
    rows dropped          3, each logged in the spec with the reason it ranked below the cap
    null control          0 deaths, so the apparatus is believable
    baseline              green, 6254 collected, re-established across two driver sessions
    total deaths          77
    zero rows             6: 5 user-facing (composite provided for each), 1 maintainer-facing
    collect drift         none; every row's collected count matched its own subset baseline
    pytest invocations    34 across two driver sessions (25 then 9; see driver incident below)

The six zero rows: `R3_head_precedence_swapped`, `R8_stem_source_swapped`,
`K1_lossy_title_side_dropped`, `K2_lossy_filename_side_dropped`,
`CUT1_prose_contradicted`, `E3_camelot_anchor_dropped`. `CUT1` and `E3` were
each promoted to a full-suite run before being reported as zero, per METHOD;
the other four were already measured against the full suite because no test
file imports `cratekit.write.naming_cli` by name, so their "subset" already
was the full 6254.

## What was driven

Beyond the shipped `tests/test_naming_apply_cli.py` (which the full pytest
run above already exercises), a standalone scratch driver,
`<scratch>/drive_u39.py`, builds real FLAC files with `ffmpeg`, writes real
tags with `cratekit.core.tags`, and drives the real dispatcher
(`cratekit.cli.run`) exactly as the shipped tests do, but constructs eight
scenarios the shipped suite does not:

- **A.** `render_all` with key `1A` pads to `01A - 124 - Cola.flac`; `12A`
  renders unchanged. A third case confirms that a syntactically non-Camelot
  key passed directly to the render engine's `key` field is REFUSED, not
  "rendered as it arrives": `HEAD_FIELDS["key"]` is fixed to the Camelot
  shape regardless of `key_pad`, so the brief's third render scenario
  ("a key that is not Camelot renders as it arrives") is not this path.
- **B.** `name.apply` over an already-padded folder proposes no rename.
- **C. The hazard.** `1A - 124 - Cola.flac` plans to `01A - 124 - Cola.flac`,
  applies cleanly, the orphaned `Cola.flac` head-collapse the pre-U39 code
  produced does not occur, the title tag matches the new stem, and a second
  plan over the result is empty (idempotent).
- **D.** A file with no parseable head (`Some Random Bootleg.flac`) proposes
  no rename.
- **E.** Filename and title carry DIFFERENT head values (`1A - 124` in the
  filename, stale `5B - 95` in the title). The plan uses the filename's
  values, confirming the commit message's "filename first" claim as actual
  driven behaviour, not just a docstring.
- **F.** The brief's actual "renders as it arrives" scenario: a non-Camelot
  `initialkey` tag (`Amaj`) on a file whose own head is `1A - 124` is ignored;
  the file's own head renders and still pads.
- **G.** The lossy marker present in only one of filename/title. Marker in
  the title alone (`Cola.flac` / title `[MP3] Cola`) is correctly recovered
  and repairs the filename to `[MP3] Cola.flac`. (Marker in the filename
  alone happens to already equal its own rendered target, so that half is a
  poor discriminator; case G's title-only half is the one that matters and it
  passes.)
- **H.** Filename body text (`Old Stale Body`) and title body text
  (`Corrected Body`) disagree; the plan uses the title's body, confirming the
  shared spec builder is title-sourced for the stem, not filename-sourced.

Also verified directly (not via a scenario, by reading and by running a
one-line interpreter check): no seventh site writes an unpadded template.
`acquire/match.py:1650`'s `template or naming.NameTemplate()` is a READER
(`index_library` parses existing filenames through it), never a renderer, so
it correctly falls outside the six constructors the brief names and needed no
flip.

## Finding 1 (R-166), residual. The lossy marker's OR is exercised only on its always-true diagonal

`write/naming_cli.py`'s shared spec builder computes
`lossy=marker in path.stem or marker in title`. The only shipped test that
touches this line,
`tests/test_naming_apply_cli.py::test_the_plan_and_the_apply_agree_on_a_marked_file`,
puts the marker in both operands at once (`f"{marker} Cola.flac"`, title
`f"{marker} Cola"`), so it cannot distinguish which operand is doing the work.

**Driven.** `K1_lossy_title_side_dropped` (`lossy=marker in path.stem`) and
`K2_lossy_filename_side_dropped` (`lossy=marker in title`) both killed 0 of
6254 on the full suite (`docs/mutation/u39-naming-independent.md` rows
`K1`/`K2`).

**Composite.** `K3_lossy_flag_dropped`, which drops the flag entirely
(`lossy=False`), kills 1 on the same function
(`test_the_plan_and_the_apply_agree_on_a_marked_file`), so the apparatus is
sensitive to breakage in this exact area; it just cannot see which half of
the OR carries the marked-title-only case. `drive_u39.py` scenario G drives
that case directly against the UNMUTATED shipped code: a file named
`Cola.flac` with title tag `[MP3] Cola` plans to rename to `[MP3] Cola.flac`,
correctly recovering the marker from the title alone. This is the marker's
own crash-window case, symmetric to the head-recovery healing this unit's
commit message describes for R2 ("the tag then rename crash window, where the
head survives in the title and not in the filename"): a run that wrote the
marked title tag but crashed before the rename would leave exactly this
state, and `K1` shows that dropping the title operand would silently stop
repairing it.

**Not BLOCKING** because the shipped code is correct on this branch, driven.
What is missing is a pinning test, not a working guard.

## Finding 2 (R-167), residual. Filename-first precedence is asserted, not pinned

The commit message states: "The head is recovered as text from the filename
first and the title tag second... never from any analysis surface." The code
is `head = parse_head(path.name) or parse_head(title) or {}`. Every shipped
test that gives both filename and title a parseable head gives them the SAME
values (`test_a_folder_already_in_convention_proposes_no_rename`,
`test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`, etc.), so
none of them can tell "filename wins" from "either wins, it did not matter
here".

**Driven.** `R3_head_precedence_swapped` (title tried before filename, not
dropped, just reordered) killed 0 of 6254 on the full suite.

**Composite.** `R1_filename_source_dropped` and `R2_title_fallback_dropped`,
which each drop one operand from the exact same three-line expression, kill 1
each (`test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it` and
`test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`
respectively), so the apparatus is sensitive to this code, just not to
precedence when both sides parse. `drive_u39.py` scenario E constructs the
missing case directly: filename `1A - 124 - Cola.flac` (current, correct) and
title tag `5B - 95 - Cola` (stale, disagreeing in both key and tempo). The
shipped code's plan uses the filename's values (`01A - 124 - Cola.flac`),
confirming the commit's claim as driven fact rather than an unverified
docstring.

**Not BLOCKING.** The behaviour is real, intentional (the docstring gives a
coherent reason: the filename is the convention's ground truth, the title is
a recovery fallback for the crash window, not a correction channel), and
correct when driven. The gap is that no shipped test would catch a regression
that silently swapped this precedence.

## Finding 3 (R-168), residual. Stem source must be the title, not the raw filename stem

`_spec_for` computes `stem = naming.strip_head(title, template=template)`.
Every shipped scenario that supplies both a title tag and a filename gives
them body text that agrees once the head is stripped, so a version reading
`path.stem` instead of `title` for this one line passes every shipped test.

**Driven.** `R8_stem_source_swapped` killed 0 of 6254 on the full suite.

**Composite.** Neighboring mutations of the same `_spec_for` function --
`R4_bpm_dropped` (6 kills), `R6_head_key_overrules_tag` (1 kill),
`K3_lossy_flag_dropped` (1 kill) -- all die, so the apparatus is not blind to
this function in general. `drive_u39.py` scenario H constructs the missing
case: filename `1A - 124 - Old Stale Body.flac`, title tag
`1A - 124 - Corrected Body`. The shipped code's plan proposes
`01A - 124 - Corrected Body.flac`, using the title's corrected body text, not
the filename's stale one. This is the exact scenario the whole point of
tag-driven naming exists to serve (a user corrects a title, expects the file
to follow it), and the code does it correctly; there is simply no shipped
test that ever makes a title's body text differ from its filename's.

**Not BLOCKING.** Driven, correct, undocumented by a test.

## Finding 4 (R-169), residual, maintainer-facing. CUT.md's reconciliation has no reverse-direction guard

This unit's own stated purpose (issue #57, approach step 3) was partly to fix
a live contradiction: `name.apply`'s registry entry claimed `dj-pad-camelot`
as a ported source script while `CUT.md` simultaneously listed it as
not-ported. The fix moved the row out of the "not ported" table into a new
paragraph. `tests/test_cli_contract.py::test_every_source_entry_point_is_either_mapped_or_written_down_as_cut`
is the test nearest this area, and it only checks that a script is `mapped`
(claimed via some entry's `source_scripts`) OR named anywhere in `CUT.md`'s
text -- an OR, not an exclusive one. Since the new paragraph still contains
the literal string `dj-pad-camelot`, and the entry's `source_scripts` still
claims it, THAT test cannot distinguish "reconciled" from "contradictory but
both true", because both states satisfy its OR.

**Driven.** `CUT1_prose_contradicted` reverts the reconciliation paragraph's
opening to say the script is NOT ported (restoring the pre-U39
contradiction, word for word matching the ledger's old wording, `"the
zero-padding pass is absorbed into the naming engine, which applies the same
rule at write time"`) while leaving `registry.py`'s `source_scripts` claiming
it. Killed 0 of 6254, confirmed by promotion to the full suite.

**Not BLOCKING**, and no composite is required (maintainer-facing, per
METHOD's severity floor). It is filed because it is the identical defect
CLASS this unit was built to fix, now unguarded against a future edit
reintroducing it on either side.

## Finding 5 (R-170), residual, existing-guard sample. The Camelot regex's end anchor has zero test coverage

Not part of this round's diagonal; sampled as one of the fixed existing-guard
rows METHOD asks for. `_CAMELOT_RE = re.compile(rf"^0?({_CAMELOT_NUMBER})({_CAMELOT_LETTER})$",
re.IGNORECASE)` is matched with `.match()` (start-anchored only) inside
`is_camelot` and `parse_camelot`, so the trailing `$` is the only thing
stopping a value like `"1Axyz"` from validating as `"1A"` with junk ignored.

**Driven.** `E3_camelot_anchor_dropped` removes the `$` and kills 0 of 6254,
confirmed by promotion to the full suite.

**Confirmed as a real, currently-closed gap** (not a live bug): a direct
interpreter check against the UNMUTATED shipped code,
`naming.is_camelot("1Axyz")` and `naming.parse_camelot("1Axyz")`, returns
`False` / `None` today, exactly as the anchor promises.

**Not BLOCKING.** Pre-existing, untouched by this diff, and currently
correct; filed because the sample surfaced it and METHOD says to record what
it finds.

## What was checked and found correct

- The hazard this unit exists to fix (`01A - 124 - Cola.flac` -> `Cola.flac`)
  does not reproduce; driven in scenario C above, both the plan and the
  applied result are correct, and a second plan is empty.
- The registry correction is accurate: `write/naming_cli.py`'s handler opens
  no database (confirmed by reading the whole file; the only I/O is
  `Path.rename`, `naming.claim_target`, and `tags.write_tags`), so
  `writes=frozenset({"files"})` is true, and dropping
  `CLOUD_SYNC_UNREADABLE_GATE` is consistent with
  `test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`'s
  reverse-direction check (`W1`/`W2` in the mutation table each kill exactly
  that test when reverted).
- All six of the brief's named template constructors (`write/naming_cli.py:36`,
  `intake/ingest.py:53`, `acquire/match_cli.py:840-841`, `cli/reports.py:105`,
  `intake/repair.py:23`, `analysis/run.py:22`) construct `NameTemplate()` with
  no `key_pad` override, so all six correctly inherit the new padded default.
  No seventh writer site exists: `acquire/match.py:1650`'s
  `template or NameTemplate()` is a reader used only by `index_library` to
  parse existing filenames, never to render one, and is correctly out of
  scope.
- `key_pad` normalizes a code arriving as DATA (a tag or detector value) and
  leaves an off-wheel value to fall through to the one refusal path, rather
  than raising from inside `pad_camelot` itself; `D2`/`D3` in the mutation
  table both die, and `test_an_off_wheel_key_is_still_refused_not_padded`
  pins the refusal-not-padding distinction.
- R17 (no tempo into any tag or database field) holds structurally: `bpm`
  in `_spec_for` is sourced only from `head` (filename or title text via the
  head parser), never from a tag; `core.tags.FIELDS` has no tempo key, and
  the two beat-grid suites plus the tags round-trip suite are part of the
  6253 passing.
- `test_the_key_is_written_and_measured_in_the_same_padded_form` and the
  budget-interaction tests confirm the byte the budget always reserved
  (`budget_key_pad = "camelot2"` predates this unit) is now simply spent
  rather than held in reserve; `E1` (budget-ordering guard) still dies when
  inverted.
- The plan/apply disagreement on the `lossy` flag that predated this unit
  (the plan pass never set it at all) is closed: `K3` kills
  `test_the_plan_and_the_apply_agree_on_a_marked_file` when the shared
  builder's flag is dropped.
- No swept-in AST-walk-detectable pattern from METHOD's "what a green suite
  cannot see" section was found in the new test file: `tests/test_naming_apply_cli.py`'s
  assertions compare against literal expected strings
  (`"01A - 124 - Cola.flac"`, etc.), not against a value derived from the code
  under test, so none of the new tests are an X-equals-X tautology. No test
  in this diff forbids a feature by naming a retired implementation's
  symbols. No duplicate registry key was introduced (`writes=frozenset({"files"})`
  is a single assignment, not a merge of branches). `key_pad` as a name does
  not collide with any other module-level meaning searched for across `src`.

## The mutation table, read by area

**Write-time padding (`core/naming.py`, D-series + M1 + E-series).** Twelve of
twelve rows died. The default flip (`D1`), the padding condition in both
directions (`D2` inverted, `D3` disabled), and a fake pad that uppercases
without zero-filling (`D4`) all die across the same nine-file subset (11 to
15 kills each), which is wide because `TestWriteTimePadding` and several
`TestRender`/`TestBudgetInteraction` tests all depend on the padded default
now being on. The refusal-message reword (`M1`) dies twice, confirming the
suite asserts with `in` against unappended text, matching METHOD's driver
rule. The two existing-guard samples split: `E1` (budget ordering) and `E2`
(letter class widened to admit C) both die; `E3` (anchor dropped) does not,
filed as R-170.

**The shared spec builder (`write/naming_cli.py`, R-series + K-series).**
Eleven rows, six die, five do not. The three genuinely destructive mutations
this unit's own commit message calls out by name -- dropping the recovered
tempo (`R4`, 6 kills, the exact shape of the pre-U39 hazard), reversing key
precedence (`R6`), and admitting a junk tag (`R7`) -- all die immediately.
The five zeros (`R3`, `R8`, `K1`, `K2`, plus `CUT1` in a different file) are
Findings 1 through 3 above: every one of them is a reordering or an
operand-drop on a line whose ONLY shipped test happens to construct both
sides identically. None is a defect in the shipped code; all five are gaps
where the shipped suite's own fixtures never disagree with themselves.

**The registry correction (`cli/registry.py`, W-series).** Both rows die
against the same single test,
`test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`,
which is the exact "both directions" check the commit message describes:
`W1` restores the false `writes` claim, `W2` restores the unreachable gate,
and either one alone trips that one test. This is a single point of failure
for the registry correctness of this unit -- both halves of the fix are
protected by one assertion, not two -- which is worth naming even though it
is not a gap: the test genuinely does fire on both mutations.

**Documentation (`CUT.md`, CUT1).** Zero, Finding 4/R-169.

## Rows dropped

Three, all logged in `docs/mutation/u39-naming-independent.toml`'s
`[[dropped]]` table and reproduced here:

- `S1_constructor_sites`: mutating each of the six template constructor call
  sites individually was ranked out because the round changed no
  constructor; every site inherits the default `D1` already measures, so six
  rows would re-measure one guard six times.
- `S2_strip_and_claim_guards`: mutating `strip_head`, `dedupe_stem`, and
  `claim_target` internals was ranked out as untouched by this round and
  already measured by prior tables; it ranked below the E-series
  existing-guard sample actually taken.
- `S3_config_key_pad_threading`: mutating `config.py`'s naming defaults was
  ranked out because no site in this round reads a config value for
  `key_pad` -- verified by reading (all six constructors use the
  `NameTemplate` default directly, see "what was checked and found correct"
  above) rather than measured, so a config-layer row would test nothing this
  round touches.

22 rows were run against a 45-row full-pass cap; the eight new rows beyond
the author's fourteen (`D2` restated as an inversion rather than a bound
change, `D4`, `R3`, `R5`, `R8`, `K1`, `K2`, `CUT1`, `E3` -- nine, not eight,
counting generously) were chosen to probe the exact shape METHOD warns an
author's table misses: branches of an `or`/ordering that the author's own
fixtures never exercise because the author, like every fix agent, tested what
they believed they changed.

## Driver incidents during this pass

Two, both logged here per METHOD's instruction that a truncation or a driver
failure be visible rather than silently absorbed.

1. **A hand-copied `old` string did not match the file byte-for-byte.** The
   first version of the `CUT1_prose_contradicted` row's `old` text was
   reconstructed from a `git show` diff hunk read earlier in this review
   rather than copied from the file itself, and the diff hunk's line-wrapping
   did not match CUT.md's actual physical line breaks (a sentence that
   appeared to end a line in the earlier diff read in fact continues onto
   the same physical line as the next sentence in the file). `mutate.py`
   correctly refused rather than mis-measuring: status `refused`, note "old
   text is not present in the target; the row cannot be applied." Fixed by
   reading the exact bytes from the file with a small script
   (`text[text.index(...):...]`) rather than retyping from a remembered diff,
   per METHOD's own instruction ("Copy the text out of the file rather than
   retyping it," which is literally the tool's own refusal message).

2. **The first full run of all 22 rows did not finish cleanly on `E3`.** The
   driver process exited (not killed by this reviewer) after successfully
   completing 21 of 22 rows, leaving `src/cratekit/core/naming.py` mutated
   on disk (the `E3` anchor-drop) and uncommitted -- caught immediately on
   the next action, `--resume`, which correctly refused rather than
   proceeding: "refused: uncommitted changes to mutation targets... Restores
   are verified against `git show HEAD`, which cannot see an uncommitted
   edit." Per METHOD's driver rule ("verify restores against `git show
   HEAD:<path>`, never a scratch copy"), the fix was `git checkout --
   src/cratekit/core/naming.py` followed by a diff against
   `git show HEAD:src/cratekit/core/naming.py` confirming an exactly empty
   diff before re-running. The re-run used `--timeout 600` (up from 300) as
   a precaution and completed cleanly; whether the first run's stall was
   actually a timeout was not established with a measurement (no captured
   stderr survived the background-process transition), so no mechanism is
   claimed here beyond what was observed: the file was left dirty, the
   restore-verification refusal caught it before it could contaminate a
   later row, and a clean re-run with a longer timeout did not reproduce it.
   All four registry/writer files were reconfirmed byte-identical to `git
   show HEAD:<path>` after the full run completed, and the battery was
   re-run clean afterward.

## Postscript: what was done about these findings, 2026-08-25

Added after the review was written, by the session that received it. The
measurements above are the reviewer's and are untouched. This section records
the disposition, because a review that names the residuals it expects to be
filed becomes false the moment somebody fixes them instead.

**Four of the five findings were closed with tests rather than filed.** The
verdict was CLEAN, so none of them held the merge, and all four sat on code
this unit had just written. The reviewer had already built the driving
scenarios that proved the behaviour correct, so the remaining work was to turn
each into a shipped assertion.

| finding | proposed | what happened |
|---|---|---|
| 1, lossy marker's two operands | R-166, R-167 | **closed.** Two tests, one per operand |
| 2, filename first precedence | R-167 | **closed.** One test where the heads disagree in value |
| 3, title sourced stem | R-168 | **closed.** One test where the bodies disagree |
| 4, CUT.md reconciliation | R-169 | **filed as R-166** |
| 5, Camelot end anchor | R-170 | **filed as R-167** |

The four rows were re-measured with `scripts/mutate.py` after the tests landed,
against the same expressions the review mutated. Every one now dies, and each
is killed by exactly the one test written for it, which is a stronger result
than a death somewhere in the suite:

    baseline               6258 collected, up from 6254 by exactly the four new tests
    null control           0 deaths
    R3_head_precedence_swapped        0 -> 1   test_the_filename_head_wins_when_both_heads_parse_and_disagree
    R8_stem_source_swapped            0 -> 1   test_the_body_text_comes_from_the_title_and_not_the_filename
    K1_lossy_title_side_dropped       0 -> 1   test_a_marker_in_the_title_alone_is_still_recovered
    K2_lossy_filename_side_dropped    0 -> 1   test_a_marker_in_the_filename_alone_is_not_stripped_off

**One correction to the review, and it is the interesting one.** Finding 1
records the marker's filename-only half as "a poor discriminator", on the
grounds that such a file already equals its own rendered target. That is true
of the unmutated tree and it is not true under the mutation, which is the only
state that matters for whether a row is killable. Driven: `[MP3] Cola.flac`
with a clean title proposes no rename today, and with the filename operand
dropped the render loses the marker, so the pass proposes renaming the marked
file to its unmarked form. `core/naming.py`'s own stripper docstring says what
that costs, a marked lossy copy and its lossless twin normalize to the same
key and stop being distinguishable. So the row was not only killable, it was
the direction of the two that loses data.

The general shape is worth naming, because METHOD already carries its sibling.
METHOD says an author's own mutation table is a draft rather than a result. The
same applies one level up: **a reviewer's reason for leaving a zero row at zero
is itself an unverified claim, and it is verified the same way everything else
here is, by driving it.**

**Also corrected:** the verdict paragraph above originally said the six zero
rows were "filed as residuals R-166 through R-171". Six rows collapse to five
findings, because `K1` and `K2` are two halves of one, so that numbering
claimed a residual that never existed. Fixed in place.
