# U41 independent adversarial review

Commits `fe47197` ("feat(naming): the head is derived, the body is carried
through"), `b91e69a` ("test(mutation): U41 author table, eight rows, every row
killed") and `79b172f` ("fix(naming): close what the review found, and correct
two records I wrote"), branch
`unit/u41-what-the-filename-body-is-composed-from-`, GitHub issue #59.
`origin/main` is at `398c77c`.

Reviewed by an agent that did not write the code, in its own worktree
(`git worktree add --detach <repo> 79b172f`, detached because the branch was
checked out elsewhere), with its own virtual environment built from
`/opt/homebrew/bin/python3.12` and verified to resolve `cratekit` to that
worktree's own `src` before any measurement was trusted.

Paths are written as `<repo>` and `<scratch>` because the repository's own
portability scan refuses an absolute home directory in a shipped artifact.

## Verdict

**CLEAN.** No finding meets all three conditions of the merge bar in
`docs/METHOD.md`. The decision the unit implements is correctly implemented and
correctly pinned: the filename renders from the filename's body and the title
tag from the tag's, and the row that restores the R-168 truncation now kills 8
tests at this tip rather than 0. Every scenario the brief names was driven end
to end through the real dispatcher against real audio files. `R-171` and `R-172`
were re driven independently and both entries are accurate as written.

On the specific question this unit turns on: **the docstring resolution in
`79b172f` is honest.** Its claim that the three fixtures trigger neither
shortener was driven and is true, so the equality assertion no longer forbids
behaviour the docstring calls correct. The test still has a gap, but it is a
different one and nobody had named it: the whole guard lives inside a loop over
the planned moves and executes zero assertions when the plan is empty. That is
finding 1.

| # | Finding | Class | Measured cost |
|---|---------|-------|---------------|
| 1 | The unit's central guard, `test_a_rename_never_replaces_the_body_with_the_title_tag`, asserts only inside a loop over the planned moves, so an implementation proposing no rename satisfies it vacuously | RESIDUAL, proposed R-173 | driven: the shipped test PASSES with the plan pass replaced by one that returns no items; its sibling `test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt` asserts `len(moves) == 1` and the sibling does not |
| 2 | `naming.claim_target`'s removal kills 0 of 6266, and the mutated tree destroys audio | RESIDUAL, proposed R-174 | driven: two 8430 byte files become one 8430 byte file and both originals are gone; composite `C1` kills 7 and `C7` kills 4 on the same loop |
| 3 | The verb can no longer restore a filename body from the title tag, so a name that is a head and nothing else is a fixed point | RESIDUAL, proposed R-175 | driven both halves: the pre U41 `_spec_for` PRODUCES `01A - 124 - .flac`, and the reviewed verb given that file with the title tag still holding `01A - 124 - Song Title` proposes nothing; population in the library unmeasured, the volume is disconnected |
| 4 | Three shell level normalizations and fallbacks in `_spec_for` are fully masked by the engine, which is R-170's class reproduced twice more | RESIDUAL, proposed R-176 | driven: `A3`, `A4` and `A7` each kill 0 of 6266 and each is byte identical to the shipped tree on every input driven; R-170's "redundant" holds at one and two stacked heads and FAILS at three |
| 5 | `dedupe_stem`'s two structural guards mask each other, so no single layer mutation can reach them | RESIDUAL, proposed R-177 | driven: `D2` and `D5` each kill 0 and each alone changes no output; applied TOGETHER, `"Song - Song"` becomes `"Song"` |
| 6 | Four more guards on the write path kill 0 and each was driven to a real behavioural difference: `C5`, `E2`, `E6`, `D4` | RESIDUAL, proposed R-178 | driven: a failed rename leaves a 0 byte phantom track; two stems that dedupe alike hash alike; a cut lands on a trailing space; a stem starting and ending in the separator loses its tail |
| 7 | The author's shipped mutation table was measured at `fe47197` and the tip is `79b172f`, which changed an assertion in a test the table credits with a kill and added four tests | RESIDUAL, proposed R-179 | measured: the table states baseline 6262 collected; the tip collects 6266, and `R8` kills 8 here rather than the 5 the table and the solutions doc record |
| 8 | The measurements that decided this unit's design have no reproducible artifact in the repository | RESIDUAL, proposed R-180 | the 53/25/1 percent grammar split, the 149 of 150 sample and the sixty file drive appear only as prose; the volume is disconnected and none can be re derived this session |

## Battery, from inside the worktree with its own venv

    ./.venv/bin/ruff check src tests scripts        All checks passed!
    ./.venv/bin/python -m pytest --tb=no             6265 passed, 1 skipped in 260.62s
    ./.venv/bin/python scripts/scan_repo.py          exit 0, no output

    pytest --collect-only -o addopts=                6266 collected

The author measured 6265 passed and 1 skipped. **Confirmed, exactly.** Ruff and
the portability scan were re run after the mutation batch and after the scratch
probes were removed, and both were clean again with the tree byte identical to
`git show HEAD` for every tracked file.

## Mutation headline

Full pass, driven by `scripts/mutate.py` from inside the review worktree. Table
and JSON sidecar at `docs/mutation/u41-naming-independent.md` and `.json`, spec
at `docs/mutation/u41-naming-independent.toml`.

    rows run              43 against the 45 row full pass cap (author ran 8)
    rows dropped          6, each logged in the spec with the reason it ranked below the cap
    null control          0 deaths, so the apparatus is believable
    baseline              green, 6266 collected, re established in each driver session
    total deaths          207 (author measured 30)
    zero rows             15: 14 user facing, 1 maintainer facing, every one promoted to a full suite run
    collect drift         none; every row's collected count matched its own subset baseline, and no row reported a collect error
    restores              all 43 verified against `git show HEAD:<path>`
    pytest invocations    66 across two driver sessions (37 then 29; see the driver incident below)

The fifteen zero rows are `A3_stem_not_stripped`, `A4_title_not_stripped`,
`A7_title_fallback_dropped`, `C3_apply_isfile_recheck_dropped`,
`C4_claim_target_dropped`, `C5_failed_rename_leaves_the_claim`,
`C6_target_identity_guard_dropped`, `D2_structural_min_parts_lowered`,
`D4_empty_lead_guard_dropped`, `D5_candidate_separator_guard_dropped`,
`D7_dedupe_title_argument_from_the_stem`, `E2_hash_source_dropped`,
`E6_dangling_trim_dropped`, `E7_filename_ceiling_dropped` and
`F5_body_tag_truthiness_becomes_identity`.

**Every one of them was classified by driving the MUTATED tree**, which is what
`docs/solutions/workflow-issues/dismissing-a-zero-row-is-a-claim-about-the-mutated-tree.md`
demands and what this unit exists because of. The classification came out three
ways.

- **Six are genuinely inert**, meaning the two trees produce identical output on
  every input driven: `A7`, `C3`, `D2`, `D5`, `D7`, `E7`. Per that doc's mirror
  an inert row is not filed as a residual, so none of them is, and the
  redundancy each one points at is recorded instead, in findings 4 and 5 and in
  the reading by area.
- **Eight are real test gaps on reachable inputs**: `A3` and `A4` at three
  stacked heads (finding 4), `C4` (finding 2), `C5`, `D4`, `E2` and `E6`
  (finding 6), and `F5`, which is `R-171` measured from the fix side.
- **One, `C6`, produces a real difference under the mutation and its input is
  not producible by the shipped plan pass.** Driven both ways: with a hand built
  no op plan item the shipped tree writes the corrected title tag and the
  mutated tree leaves it unwritten. One candidate producer was driven, the real
  `_plan_for`, and it does not emit such an item, because it appends only when
  `rendered.filename != path.name`.

The author versus independent gap on this unit is 8 rows against 43 and 30
deaths against 207, with 0 zeros against 15. That is the largest gap recorded on
this project and it is METHOD:95 operating exactly as written: the author's
eight rows all sit on `_spec_for` and `dedupe_stem`, which is what the author
believed the round changed, and every guard the decision now LEANS on rather
than TOUCHES went unmutated.

## What was driven

Everything below ran through `cratekit.cli.run`, against real audio files built
by `tests/_containers.synth_container`, in the repository's own redirected state
roots. The live rekordbox database was never opened and the library volume is
disconnected and was never touched.

- The brief's five test scenarios, each independently: an artist the tag lacks
  survives a plan and an apply; both library grammars round trip; a rename never
  produces a body that is a strict truncation of the one it replaces; the pass
  stays idempotent over its own output; and `R8` is a killing row again, killed
  by tests asserting the decided rule.
- `R-171` reproduced from its own text.
- `R-172` reproduced from its own text.
- The brief's step 4, the tag driven purpose, driven from the direction nobody
  tested: a title tag corrected to carry MORE text than the filename body.
- Budget truncation applied and then re planned, which the shipped test does not
  do.
- The three fixtures of the body preservation test, put through `dedupe_stem`
  and `fit_stem_to_budget` directly, to check the docstring's claim about them.
- The pre U41 `_spec_for`, restored in memory, as the producer for finding 3.
- The mutated tree for all fifteen zero rows.

## Finding 1 (proposed R-173), residual. The central guard asserts nothing when the plan is empty

`tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
is the test the brief asked for by name and the one the mutation row `R8` is
supposed to be killed by. Its whole body is a loop:

    for frm, to in _moves(_plan(folder)):
        before = naming.strip_head(Path(frm).stem, template=template)
        after = naming.strip_head(Path(to).stem, template=template)
        assert after != "Song", ...
        assert after == before, ...

There is no assertion outside the loop and no assertion about the loop's length,
so an implementation whose plan pass proposes nothing passes it.

**Driven.** A pytest plugin at `<scratch>/emptyplan_plugin.py` replaces
`cratekit.write.naming_cli._plan_for` with one that returns an empty item list.
Nothing on disk is edited; the checkout stays byte identical to `HEAD`.

    PYTHONPATH=<scratch> ./.venv/bin/python -m pytest \
      "tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag" \
      -p emptyplan_plugin -o addopts= --tb=line

    tests/test_naming_apply_cli.py .                                         [100%]
    1 passed in 0.48s

Driven a second way, without any patching, by giving the same three fixture
bodies names that are already in convention so the real plan pass returns
nothing. The loop then executes and the assertion counter reads zero:

    P9 planned moves: []
    P9 assertions executed: 0

**Why this is not the same defect two reviewers already caught, and why it is
not fixed by what they got.** Their finding was that `assert after == before`
forbade `dedupe_stem` and `fit_to_budget`, which the docstring had just called
legitimate. `79b172f` resolved that by scoping the docstring to these three
inputs, and **that resolution is honest**: driven directly, all three bodies are
identity under both shorteners.

    P6 (body, dedupe_is_identity, budget_is_identity):
        ('Artist Name - Song Title', True, True)
        ('Song - Artist - Album', True, True)
        ('Just A Body', True, True)

So the docstring no longer promises something weaker than the assertion
enforces. What it still does not say is that the assertion runs only if there is
something to assert about.

**One smaller observation on the same test.** The commit message says the first
assertion "was also a tautology given the second, catching nothing on its own",
and the fix changed `assert after != "Song" or before == "Song"` to
`assert after != "Song"`. Given the second assertion and `before != "Song"`,
which holds for all three fixtures, the new first assertion is still implied by
the second. The redundancy was narrowed rather than removed. It is harmless, it
produces a better failure message, and it is recorded here only because the
commit claims otherwise.

**Measured cost.** None to any person today. The three fixtures do produce three
moves on this tree, so the guard is not vacuous as shipped. The cost is that the
one test carrying this unit's decision cannot distinguish "the body was
preserved" from "nothing was renamed", and the neighbouring test written in the
same fix round DOES make that distinction with `assert len(moves) == 1`.

**Closes when:** the test asserts how many moves it expects before it iterates
them.

## Finding 2 (proposed R-174), residual. The claim that stops a rename destroying audio kills zero tests

`C4_claim_target_dropped` removes the two lines

    if not naming.claim_target(target):
        continue

from `write/naming_cli.py`'s apply loop and kills 0 of 6266, promoted to a full
suite run before being reported.

**The mutated tree, driven, because a zero is unclassified until it has been.**
Two files whose rendered names collide, each 8430 bytes, with
`naming.claim_target` replaced in memory by `lambda path: True`:

    C4 mutated: sizes before: {'5A - 120 - Song - Artist.flac': 8430,
                               '5A - 120 - Song - Artist - Song.flac': 8430}
    C4 mutated: planned: [('5A - 120 - Song - Artist - Song.flac', '05A - 120 - Song - Artist.flac'),
                          ('5A - 120 - Song - Artist.flac', '05A - 120 - Song - Artist.flac')]
    C4 mutated: files after: {'05A - 120 - Song - Artist.flac': 8430}
    C4 mutated: originals still present: False False

Two tracks in, one track out. POSIX `rename` overwrites, so the loser of the
collision loses its audio. The shipped tree on the identical input keeps both
files and renames one:

    P2 files after apply: ['05A - 120 - Song - Artist.flac', '5A - 120 - Song - Artist.flac']

**Composite**, per METHOD's requirement for a user facing zero.
`C1_plan_no_op_filter_dropped` kills 7 and `C7_title_tag_write_dropped` kills 4
on the same function, so the loop is exercised; it is this guard inside it that
nothing reaches.

**Measured cost.** None today: the shipped guard is correct and was driven. The
cost is that the single line standing between a collision and destroyed audio,
in a verb whose registry entry writes files, has no test, so a regression
removing it would be invisible. The zero row learning ranks exactly this shape
above the other zeros.

**Closes when:** a test drives two colliding renames and asserts both files
still exist.

## Finding 3 (proposed R-175), residual. A name that is a head and nothing else is now a fixed point

The decision is that the body is carried, and an absent body is carried as
absent. The pre U41 verb composed the filename body from the title tag, which is
what made it destructive and is also what made it able to REPAIR a filename that
had lost its body while the tag kept the text. That repair is gone.

**Both halves driven.** The producer first, which is the merge bar's third
condition. `origin/main`'s `_spec_for` differs from the reviewed one in exactly
two assignments; those two lines were restored in memory and the pre U41 verb
was run on this tree:

    Producer, pre U41 verb, planned: [('1A - 124 - Artist Name - Song Title.flac', '01A - 124 - .flac')]
    Producer, pre U41 verb, files after apply: ['01A - 124 - .flac']
    Producer, pre U41 verb, title tag: '01A - 124 -'

That is the same output `R-171` records for `origin/main`, reproduced
independently. Then the reviewed verb, handed the producer's own output with a
title tag that still holds the text:

    Repair attempt, reviewed verb, planned: []
    Repair attempt, files after apply: ['01A - 124 - .flac']
    Repair attempt, title tag: '01A - 124 - Song Title'

The plan is empty. The file keeps a name with no body while the tag holds
`Song Title`, and the run reports `ok`.

**Why this is a residual and not a blocking finding.** The report is accurate,
nothing is lost by the run, and no verb is refused. The producer is the code
this merge deletes, so after the merge nothing on the tree produces the state.
Whether any such file already exists in the library is UNMEASURED and cannot be
measured this session, because the library volume is disconnected; R-168
records the pre U41 cost as imminent rather than incurred, which suggests the
population is zero, and that is an inference rather than a count.

**Closes when:** either a decision is recorded that a body less filename is left
alone deliberately, or the verb composes a body from the tag in the one case
where there is no competing body to destroy.

## Finding 4 (proposed R-176), residual. Three shell layers are masked by the engine, which is R-170's class twice more

R-170 says the shell's `strip_head` is redundant because `build` normalizes
twice inside itself. This pass measured that and found two more instances of the
same shape in the same eight line function.

**`A3_stem_not_stripped` and `A4_title_not_stripped` kill 0**, and driven with
the shell's strip removed on its own, one layer only, the two trees agree at one
and at two stacked heads and DIVERGE at three:

    A3 heads=1 shell_strip=True : '1A - 121 - Artist - Song.flac'                     -> '01A - 121 - Artist - Song.flac'
    A3 heads=1 shell_strip=False: '1A - 121 - Artist - Song.flac'                     -> '01A - 121 - Artist - Song.flac'
    A3 heads=2 shell_strip=True : '1A - 121 - 2A - 122 - Artist - Song.flac'          -> '01A - 121 - Artist - Song.flac'
    A3 heads=2 shell_strip=False: '1A - 121 - 2A - 122 - Artist - Song.flac'          -> '01A - 121 - Artist - Song.flac'
    A3 heads=3 shell_strip=True : '1A - 121 - 2A - 122 - 3A - 123 - Artist - Song.flac' -> '01A - 121 - Artist - Song.flac'
    A3 heads=3 shell_strip=False: '1A - 121 - 2A - 122 - 3A - 123 - Artist - Song.flac' -> '01A - 121 - 3A - 123 - Artist - Song.flac'

R-170 says "A body carrying TWO stacked heads loses both either way, because two
normalizations already saturate it." Correct, and this extends it with a
number: there are THREE normalizations on the path, one in the shell and two in
`build`, so the saturation point is three heads and the shell's strip is the one
that supplies the third. R-170's "For every shape driven, none" should read
"for every shape driven up to two stacked heads".

**`A7_title_fallback_dropped` kills 0 and is the new instance.** The shell reads

    title = tags.read_tag(path, "title") or path.stem

and `core/naming.py:745` reads

    body_tag = spec.title if spec.title else spec.stem

Two fallbacks spelling one rule. Driven with only the shell's fallback replaced
by the empty string, on a file with no title tag at all, both surfaces are
identical:

    A7 shipped: files=['01A - 124 - Artist Name - Song Title.flac'] title tag='01A - 124 - Artist Name - Song Title'
    A7 mutated: files=['01A - 124 - Artist Name - Song Title.flac'] title tag='01A - 124 - Artist Name - Song Title'

So `test_a_file_with_no_title_tag_takes_its_body_from_the_filename`, added in
`79b172f` precisely for this case, is held by the ENGINE's fallback and not by
the shell's, and the shell's line could be deleted with the suite green. That is
the mirror learning's "two symbols meaning one thing in two modules", and it is
METHOD's fifth pattern operating on the fix round itself: the round fixed the
instance it was handed, in R-170, and the class was sitting one line below.

**Composite.** `A1` kills 8, `A2` kills 1, `A5` kills 1, `A6` kills 19 and `A8`
kills 1, all on the same three lines, so the function is exercised.

**Measured cost.** None to any person. Three lines of the reviewed function can
be deleted without the suite noticing, which makes any later cleanup of them
look safe when at least one of them, the shell's strip, is not.

**Closes when:** `build` normalizes exactly once and the shell owns the other,
or the duplication is recorded as deliberate with a test at each layer.

## Finding 5 (proposed R-177), residual. dedupe's two structural guards mask each other

METHOD says to remove each guard layer alone, because a guard covered by another
guard is a guard nothing covers. Here the covering is mutual, so no single layer
row can reach it. `D2_structural_min_parts_lowered` lowers `len(parts) >= 3` to
`>= 2` and kills 0. `D5_candidate_separator_guard_dropped` removes
`if sep in candidate:` and kills 0.

**Driven directly on the rule, all four trees on one input:**

    D2/D5 'Song - Song'         : shipped='Song - Song'   min2='Song - Song'   nosep='Song - Song'   both='Song'
    D2/D5 'Song - Artist - Song': shipped='Song - Artist' min2='Song - Artist' nosep='Song - Artist' both='Song - Artist'
    D2/D5 'A - B'               : shipped='A - B'         min2='A - B'         nosep='A - B'         both='A - B'

Either guard alone holds `"Song - Song"`. Both gone and the name becomes
`"Song"`, which for a filename body means half of it is deleted. This is the
same "AMBIGUITY MEANS IDENTITY" rule the fix round wrote a negative test for,
approached from the one direction that test cannot see.

**Composite.** `D1` kills 3, `D3` kills 4 and `D6` kills 2 on the same function.

**Measured cost.** None today, both guards are present and correct. The cost is
that the mutation apparatus reports two clean zeros over a pair that is not
covered at all, so a future round relaxing both, which is a plausible single
intention, ships green.

**Closes when:** a test drives `dedupe_stem` over a two segment stem whose
second segment repeats the first and pins that it survives.

## Finding 6 (proposed R-178), residual. Four more write path guards kill zero, each driven to a real difference

Grouped because they share a disposition, not because they share a mechanism.
None is inert, each was driven, and none is reachable through the shipped verb
today.

**`C5_failed_rename_leaves_the_claim`.** Removing `target.unlink(missing_ok=True)`
from the `except OSError` arm. Driven with `Path.rename` made to raise and
`Path.unlink` made a no op:

    C5 shipped tree after a failing rename: [('1A - 124 - Cola.flac', 8430)]
    C5 mutated tree after a failing rename: [('01A - 124 - Cola.flac', 0), ('1A - 124 - Cola.flac', 8430)]

The mutated tree leaves a zero byte file with a plausible track name, which is
the phantom track `claim_target`'s own docstring warns about.

**`E2_hash_source_dropped`.** `hash_source=spec.stem` becomes `None`. The two
differ only when dedupe changed the stem AND the name is over the ceiling, and
no fixture is both. Driven directly on `fit_stem_to_budget` with an input that
is both:

    E2 shipped (hash_source=original): ... Filler Fille~ae55c5
    E2 mutated (hash_source=None)    : ... Filler Fille~905327

which is exactly the collapse the function's docstring describes, "two sources
that dedupe to the same visible stem also hash to the same value".

**`E6_dangling_trim_dropped`.** `trim_dangling` removed from the truncation
path. The cut has to land on a space, a dash or an open bracket, and no fixture
makes it. Swept across parent directory lengths until it does:

    parent len 40 | untrimmed cut ends ' Word A '
      shipped name ends ' Word A~9ff7ef'
      mutated name ends 'Word A ~9ff7ef'

**`D4_empty_lead_guard_dropped`.** `if lead and ...` becomes `if ...`. Reachable
only for a body that both starts and ends with the segment separator:

    D4 ' - Artist - ': shipped=' - Artist - ' no_lead_guard=' - Artist'

**Measured cost.** None today. All four guards are shipped and correct. Three of
the four sit on the path this unit made reachable for the first time: while the
body came off the title tag it was short by construction and the ceiling was
never approached.

**Closes when:** each has a test, or a decision is recorded that the degenerate
inputs are out of scope.

## Finding 7 (proposed R-179), residual. The shipped author table describes the wrong commit

`docs/mutation/u41-author-full.md` says in its own header that it was measured
"branch `unit/u41-what-the-filename-body-is-composed-from-` at `fe47197`", with
"Baseline: green, 6262 collected". The branch tip is `79b172f`, two commits
later, and that commit added four tests and changed an assertion inside
`test_a_rename_never_replaces_the_body_with_the_title_tag`, which the table
credits with killing `R8_stem_from_title_again`.

**Measured.** The tip collects 6266, not 6262. The same mutation re measured
here as `A1_stem_from_title_again` kills 8, not 5, and the four extra kills are
the four tests `79b172f` added:

    test_a_deduping_rename_converges_on_one_pass
    test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt
    test_a_trailing_segment_that_only_starts_with_the_lead_survives
    test_a_file_with_no_title_tag_takes_its_body_from_the_filename   (killed by A5, not A1)

`docs/solutions/workflow-issues/dismissing-a-zero-row-is-a-claim-about-the-mutated-tree.md`
also states "`R8` now dies five times" in the paragraph `79b172f` added to it.
That number is a `fe47197` measurement written into a document by the commit
that made it stale.

**Measured cost.** Maintainer facing and small. Nothing is wrong, the numbers
understate the coverage rather than overstating it, and this independent table
supersedes the author's for the tip. The cost is that a later session reading
the author's table or the learning gets a count that no state of the repository
produces.

**Closes when:** the numbers are restated against the tip, or the table's header
is enough for a reader to know it is not the tip.

## Finding 8 (proposed R-180), residual. The design measurements have no reproducible artifact

The decision this unit implements rests on four numbers: 53 percent of names are
`Title - Artist - Album`, 25 percent are `Artist - Title`, 1 percent have a body
equal to the title tag, and 149 of 150 randomly sampled files out of 9867 lose
text under the old rename. A fifth set justifies the two shorteners: over sixty
copies of real library files, dedupe fires nine times and the ceiling four.

Those numbers appear in the `_spec_for` docstring, in the `fe47197` commit
message, in R-168, in the test docstrings and in the solutions doc. **They
appear in no committed script and no committed output.** The branch adds
`src/cratekit/write/naming_cli.py`, `tests/test_naming_apply_cli.py`,
`docs/mutation/u41-author-full.{md,json}`, `docs/residual-findings.md` and one
solutions file, and nothing else.

The library volume is disconnected, so none of them can be re derived this
session. **This report does not claim they are wrong.** They are internally
consistent, they are the right kind of measurement, and the decision they
support is sound on every input driven here. What is recorded is that METHOD's
"A table that lives only in a chat message is a claim" applies to a sampling run
exactly as it applies to a mutation table, and this one lives only in prose.

**Measured cost.** None today. The cost lands when somebody revisits the
decision, because reopening it means re running a sample nobody can reproduce
from the repository.

**Closes when:** the sampling script ships, read only, with its output, or the
decision is recorded as taken and closed.

## What was checked and found correct

- **The decision is implemented on both surfaces and pinned in both
  directions.** `A1_stem_from_title_again`, which is R-168 restored, kills 8.
  `A2_title_fed_the_filename_body`, the opposite collapse, kills 1.
  `F3_body_tag_preference_flipped`, the same collapse reproduced inside the
  engine, kills 27, and `F6_filename_prefers_the_title_body`, R-168 reproduced
  inside the engine, kills 34. The class was hunted one file over, per METHOD's
  fifth pattern, and the engine is pinned as well as the shell.
- **`R8` is killed by tests asserting the decided rule.** The eight tests it
  kills are the ones this unit wrote about grammar, artist survival and both
  shorteners, not tests matching current behaviour. The brief asked for this by
  name and it holds.
- **Both library grammars round trip, driven.** `Artist - Title` and
  `Title - Artist - Album` both pad their head and keep every byte of their body.
- **The pass is idempotent over its own output, including over TRUNCATED
  output**, which the shipped suite plans but never applies. Driven: apply, re
  plan, apply again.

      P7 first plan:  [('1A - 124 - Artist Name - Extremely Long ... Part.flac',
                        '01A - 124 - Artist Name - Extremely Long Song Title Part Extremely Long Song Title Part Extremely~f8e7dc.flac')]
      P7 second plan: []

  Convergence is not pinned by any test. It is correct because a stem that has
  been fitted is at most `max_stem` bytes so the second pass returns early, and
  it is recorded here as driven rather than as assumed.
- **The brief's step 4, the tag driven purpose, is resolved coherently.** A title
  tag corrected to carry MORE text than the filename body does not move the
  file: `P3 moves: []`. The key still moves it, which
  `test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges` pins. So the
  scoping is real: the tag owns the key, the filename owns the body, and the
  head is derived from both. The docstring records it, obliquely, as "the verb
  pads the head it understands and leaves the text it does not".
- **`R-171` is accurate as filed**, reproduced from its own text: a present
  title tag reading `1A - 124 -` leaves the filename correct and hands the TAG
  the filename's body, `'01A - 124 - Artist Name - Song Title'`.
  `F5_body_tag_truthiness_becomes_identity` applies R-171's own proposed fix as
  a mutation and kills 0, which confirms independently that neither the current
  behaviour nor its alternative is pinned.
- **`R-172` is accurate as filed**, reproduced end to end: a two item plan, one
  rename performed, one file untouched, exit 0 and outcome `ok`.
- **The head half U39 settled is untouched.** `B1` through `B8` re measure the
  head recovery, the key precedence, the Camelot check and both operands of the
  lossy `or`, and all eight kill. In particular `B7` and `B8`, which are U39's
  `K1` and `K2`, went from 0 to 1 there and are still killing here, so the tests
  written to close them are still doing their job.
- **The head is all or nothing, so no legitimate body segment can be eaten.**
  `NameTemplate.head_optional` is an empty frozenset, so `head_shapes` emits the
  single shape `("key", "bpm")`. A body starting with a bare tempo like
  `303 - Artist` therefore does NOT parse as a head, which was the hazard this
  review went looking for when the body started coming off the filename. The
  only prefix the engine can amputate is a complete `KEY - BPM - ` head, which
  is R-170's stacked case.
- **No duplicate keys in any mapping.** AST sweep over every dict and set
  literal in all 252 Python files at `HEAD`, in `src`, `tests` and `scripts`:
  zero duplicate constant keys.
- **The X equals X sweep found exactly two asserts in this unit's test file**,
  both of the form `strip_head(...) == strip_head(...)`. Both genuinely exercise
  the code and neither is a tautology on the shipped tree; the weakness in the
  first of them is finding 1 and is about the loop rather than the comparison.
- **One symbol meaning two things**, checked and judged benign: `build` is
  defined in 17 modules, sixteen of them the CLI registration hook and one of
  them `core/naming.build`, the render entry point, and both appear inside
  `write/naming_cli.py`. `_template` means a report template in
  `cli/reports.py` and a `NameTemplate` here. Neither is new and neither can
  collide, since both are reached through their module.
- **The countdown register is untouched.** The branch adds nothing to
  `tests/_pending.py` and removes nothing from it.
- **No tempo reaches any tag, database field or ANLZ container.** The tempo in
  the head is text in a filename and a title convention, which
  `core.tags.FIELDS` having no tempo key makes structural. This unit changes
  what the BODY is composed from and touches no head field.

## The mutation table, read by area

**A, the round's own diff, 8 rows, 30 deaths, 3 zeros.** The two changed
assignments are the strongest pinned lines in the file: restoring either
collapse kills immediately, and taking the stem from `path.name` rather than
`path.stem` kills 19. The three zeros are all redundancy with the engine and are
finding 4. This area is where the author's table and mine agree most closely,
which is expected, since it is the area the author knew they had changed.

**B, the head, key, tempo and lossy sample, 8 rows, 22 deaths, 0 zeros.** U39's
territory, re measured because this unit sits on top of it. Every row kills.
`B4_bpm_dropped` kills 14, which is the widest blast radius in the file and
confirms the head is load bearing across the suite rather than in one test.

**C, the plan and apply loop, 6 rows, 11 deaths, 4 zeros.** The weakest area,
and the one that writes to disk. `C1` and `C7` kill, so the loop runs and the
tag write is asserted. Everything the loop does to protect a file, the existence
recheck, the claim, the stub cleanup and the identity guard, kills nothing.
`C4` is finding 2 and `C5` is part of finding 6. `C3` is inert: `_spec_for` on a
missing path raises nothing, so the mutated tree claims a target, fails the
rename with a `FileNotFoundError` that the existing `except OSError` already
catches, unlinks the stub and continues to the same end state as the shipped
tree. `C6` is the one row whose mutated tree differs on an input the plan pass
cannot produce: handed a hand built no op item, the shipped tree wrote
`'01A - 124 - stale'` into the title tag and the mutated tree left it at
`'stale'`, because `claim_target` on the file itself returns False and the
`continue` skips the tag write.

**D, dedupe, 7 rows, 9 deaths, 4 zeros.** The fix round's two new dedupe tests
are real: `D3` and `D6`, the two plausible widenings of the repeat rule, both
kill, and `D6` is killed by the negative test the round added. The zeros are the
mutually masking pair, finding 5, plus `D7`, which is inert because
`_spec_for` never sets `album` and the tag confirmed branch therefore cannot be
entered from this verb. Driven: `D7 spec.album: None`.

**E, the byte budget, 7 rows, 22 deaths, 3 zeros.** Better covered than expected
for a path that was unreachable until this unit. The arithmetic is pinned:
`min` becoming `max` kills 8, the separator byte kills 3, the reserved tail kills
5. The zeros are the hash source and the dangling trim, finding 6, and
`E7_filename_ceiling_dropped`, which is inert for a structural reason worth
recording: with `path_budget_bytes` 250 and `filename_max_bytes` 255, the path
allowance is `232 minus the parent length` and the filename allowance is a flat
238, so the path ceiling binds for every parent directory longer than nothing.
Driven at a 136 byte parent: path allowance 96, filename allowance 238.

**F, the engine's render seam, 7 rows, 116 deaths, 1 zero.** The most strongly
pinned area in the pass, and the reason is that `render_all` is shared by every
naming caller in the repository. `F4_body_tag_fallback_dropped` kills 52 and
`F6_filename_prefers_the_title_body` kills 34. The single zero is `F5`, which is
R-171 approached from the fix side.

## Rows dropped

Six, all logged in `docs/mutation/u41-naming-independent.toml`'s `[[dropped]]`
table and reproduced in the generated table. 43 rows were run against the 45 row
cap, so the cap was not the binding constraint; each of the six was ranked below
the cap on merit.

- `C2_audio_extension_case_fold_dropped`: the extension filter pre dates U41 and
  has no bearing on what a body is composed from.
- `C8_apply_parent_dir_blanked`: the budget arithmetic is already covered by
  `E3` through `E7`, and the plan pass carries the identical call.
- `C9_plan_iteration_order_unsorted`: deliberately not run. The result would
  depend on filesystem order, so neither a death nor a zero would be
  reproducible, which is what METHOD's timing rule forbids in spirit.
- `G1_pad_head_key_span_widened`: U39 owns `pad_head` and its independent table
  measured it; this unit does not touch the head.
- `G2_camelot_end_anchor_dropped`: already measured at zero by the U39
  independent pass and filed as R-167. Re running it buys a second copy of a
  known number.
- `H1_sanitize_segment_slash_rule_dropped`: `_spec_for` never calls it and
  dedupe reaches it only on the tag confirmed branch, which this verb cannot
  enter with `album` unset.

## Driver incidents during this pass

Four, all logged here per METHOD's instruction that a driver failure be visible
rather than silently absorbed.

1. **The driver process was killed mid row and left a target mutated.** The
   first run completed 25 of 43 rows and was then stopped by the agent harness,
   not by `mutate.py` and not by this reviewer, while row
   `D4_empty_lead_guard_dropped` was applied. `git status` showed
   `M src/cratekit/core/naming.py` and `git diff --stat` showed one changed
   line, which is the one the row writes. The restore was done by writing
   `git show HEAD:src/cratekit/core/naming.py` back over the file and then
   confirming an exactly empty `git diff`, per METHOD's rule that a restore is
   verified against `HEAD` and never against a scratch copy. The batch was then
   resumed with `--resume`, which re used the 25 stored results, re established
   the full suite baseline at 6266 and ran the remaining 18. This is the same
   incident shape U39's independent pass logged, and the sidecar being rewritten
   after every row rather than at the end is what made the resume free.
2. **The two driver sessions report separate invocation counts.** The header of
   the generated table says 29 pytest invocations, which is the resumed session
   only. The first session ran 37. The total for this pass is 66, and the
   generated number is not wrong so much as scoped to one session; it is
   restated here so a later reader does not read 29 as the cost of 43 rows.
3. **No row used the `pairs_with` field, so the generated table prints "USER
   FACING ZERO WITH NO COMPOSITE" against all fourteen user facing zeros.** The
   composites exist and are reported in this document, area by area, with both
   counts, and every zero additionally had its MUTATED tree driven, which is a
   stronger result than a composite. The gap is in how the rows were authored
   rather than in what was measured, and it is recorded so the generated table's
   warning is not read as an unmet requirement.

4. **The first draft of this file reddened the battery.** It named the library
   volume by its absolute path four times, and `scripts/scan_repo.py` refused
   with "hardcoded volume path; the library root is configuration, not a
   literal", exit 1. That is the same way a previous reviewer reddened it, so it
   is recorded rather than quietly fixed: the scan reads a review document with
   the same rule it reads shipped source, and a report ABOUT the volume is
   exactly the document most likely to name it. It now says "the library
   volume", and the scan is back to exit 0. Absolute paths elsewhere in this
   file are written as `<repo>` and `<scratch>` for the same reason.

Nothing else refused, no row was rejected for an ambiguous or absent anchor, no
row drifted in its collected count, and all 43 restores verified against
`git show HEAD:<path>`.

## What this review could not measure

- The library volume is DISCONNECTED. Every number this unit derived from
  the real library, the grammar percentages, the 149 of 150 sample and the sixty
  file drive, is unverifiable this session. None of them is contradicted by
  anything driven here, and finding 8 is about their reproducibility rather than
  their truth.
- Whether any file in the library is already in the state finding 3 describes.
  The producer was driven and the state is reachable; the population is not
  countable without the volume.
- The board was not audited and no GitHub state was read or written, since this
  is a verification and the brief scoped it to the tree.
