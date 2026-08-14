# Wave state, 2026-08-14: two merges, and a unit that verified clean and still could not land

Continues `docs/wave-state-2026-08-13.md`. The method lives in `docs/METHOD.md`.
This file is history: what was measured and what was decided.

## What is on main

`6bff237`, pushed, clean. **5385 passed, 12 skipped**, 5397 collected. Ruff
clean, `scan_repo` clean. `board.py audit` exit 0, 27 done, 6 ready, 5 blocked.

**Seven units have now cleared the merge bar: U32, U34, U24, U38, U30, U16 and
U23.** Main's highest residual is **R-101**.

## The countdown instruction text, corrected before the merges rather than after

The proximate cause of both of this repository's countdown incidents was that
the text a person reads AT the moment of discharge told them the wrong thing.
Five strings, not the four the brief named:

1. `tests/_pending.py` module docstring.
2. `tests/test_pending_units.py` module docstring, point 2.
3. The countdown test's docstring.
4. The assertion message a failing run prints, which is the one read at the exact
   moment of acting.
5. **The `KeyError` message in `requires()` itself**, which was not in the brief
   and is corrected for the same reason. It offered exactly one remedy, add the
   key to the register. That is right for a key somebody is adding by hand and
   exactly backwards at a merge, where the key is leaving. It now names both
   cases and says which one a collection failure means you are in.

All five now say discharge is three edits in one commit, name the grep, and say
what doing the first two without the third actually does.

The countdown table in `docs/HANDOFF.md` was regenerated from `PENDING` rather
than repaired by hand: it had carried eleven targets across ten rows against ten
keys, with three dead targets and two live keys missing.

**Both merges in this session then met a discharge, and both went cleanly.**

## R-79: a gate on a deliberate act was sitting in an ordinary test's path

Found by running the battery on `main`'s own tree while reviewing three
docstrings. `test_calibration_round_trips_and_threshold_is_a_multiple` called
`calibrate(repeats=2)` and passed the live payload through `write_calibration`,
whose quiet machine refusal exists to gate a deliberate calibration act.

| context | repeats | pass | fail |
|---|---|---|---|
| full suite, before | 3 | 1 | 2 |
| that test alone, before | 10 | 10 | 0 |
| its file alone, after | 15 | 15 | 0 |
| full suite, after | 3 | 3 | 0 |

The isolation row is why nobody caught it: the natural check after touching the
harness is to run the harness's own file, and the harness's own file passes.
A second site carrying the identical shape had never fired and was found by
looking one function over, which is METHOD's fifth pattern used as a practice.

**This one mattered out of proportion to its size.** A battery that goes red two
runs in three, for a reason unrelated to the change under review, teaches a
reader to discount a red battery, and the battery is the one signal the merge
discipline rests on.

## U27: verified MERGE, and blocked at the merge. R-80

The independent pass was clean and thorough: 42 rows against the author's 19,
25 deaths, 17 zeros, no blocking finding, full battery green on the branch.
Main was green. **The merged tree was not, and neither side could have seen it.**

U27 lands `_probe` in `core/cause.py`, calling
`os.open(path, os.O_RDWR | os.O_NONBLOCK)` to ask the operating system whether a
write would be permitted rather than guess from a driver error. It changes
nothing and it does open a write capable handle. That module is on the read only
reports allowlist because both report modules import `Scope` and `refuse` from
it. `_os_open_reads` correctly declines to read a flag expression with an
`O_RDWR` branch as a read.

**Both remedies the guard offers were driven to their end and both fail.**
Naming the writer propagates to callers; the transitive closure over the module,
computed with an AST walk rather than chased a layer per run, is eleven names and
contains `refuse`; naming `refuse` fires the reports' own guard at
`aging.py:248` and `export.py:195`. Dropping the module fails both report
modules' imports. The third path, widening `_os_open_reads`, was not taken,
because that guard is behaving exactly as designed.

No user facing cost was found or claimed, so under the merge bar this is a
residual. It still stops the merge, because the battery rule is absolute.

**The work is preserved, not discarded.** `merge/u27-attempt-2026-08-14` is
pushed and marked DO NOT MERGE. It carries the six resolved conflicts, the
verified register discharge, the ten incoming residuals renumbered to R-80
through R-89 in that branch's own file, the `grant-path-access` reservation and
the re-pinned cause population. None of it should be paid for twice.

## U23: merged, and three things only the merged tree could see

Verified MERGE independently: 45 rows against the cap, 32 killed, 13 zeros of
which **only 6 are gaps**, the other seven proved equivalent from the
`_digest_state` invariant rather than asserted to be. One zero death row was
closed on the branch rather than filed.

The FAT proofs this unit waited five sessions for are real: a mounted FAT32
image, filesystem asked through `filesystem_kind` rather than probed, failing
rather than skipping without hdiutil.

**1. The adoption ledger is COUPLED and declared no `rollback_effects`.** U23 was
cut before U32 landed the rule that every coupled entry names what its records
caused outside the set a restore replaces. `NONE` would have been false, and
false in exactly the way that enum's docstring warns about: applying a plan entry
writes a tag INTO a file on the music volume, and rolling the ledger back does
not un-write it. It needed a new member, `WRITTEN_FILE_TAG`, because adoption is
the first feature whose coupled record describes an edit to somebody else's bytes
rather than a database row. The originals survive in the tag revert log, which is
`NEVER_RESTORED` precisely so it outlives the rollback that would erase them.

**2. The branch cited its own residual numbers outside the residual file**, in
`docs/HANDOFF.md` and its mutation notes, and after the renumber those numbers
belonged to U34, which has a guard against exactly that. Repointed, and only on
the lines the branch added: main's own citations sit in historical paragraphs and
did not move. **A renumber is not finished inside `docs/residual-findings.md`.**

**3. Four pinned populations moved and every one was re-measured.** Causes 101 to
103, non reserved 79 to 81, reserved UNCHANGED at 22. Kebab literals 256 to 270,
non keys 156 to 168. Named at risk 18 to 20 and 10 to 11, literal at risk 38 to
42 and 12 to 13. **The half worth watching, modules holding a name resolving to a
cause declared elsewhere, is STILL 8**, now across four measurements and three
merges, and the comparison those numbers are bought for widened again.

### The reconciliation, by identifier and against the union

5421 in the union, 5397 collected, **25 present on a side and absent from the
merge, all 25 accounted for.** Sixteen are renames `main` made: conformance 3's
test name, and `deletion_verb` to `deletion_pass`. Nine are correct retirements,
one countdown key and one verb marker discharged by this merge and the rest
already discharged on main. None is lost coverage. A total only check would have
seen a healthy rise.

### R-101, which this merge created

Both branches independently grew the same guard from "the target is in the
register" to "the register counts down to it OR it has landed and offers into the
queue", and named it differently. `tests/test_review_queue.py` now holds both
`_target_offers_into` and `_package_offers_into`. Git had no reason to see it:
the two definitions do not touch. Filed rather than unified, because unifying
means re-pointing nine call sites inside a merge with no table over the result.

## Two process facts worth carrying

**A closing trailer was omitted on the U23 merge.** The no-trailer standing
decision covers U27 and not U23, and this was noticed after main was pushed.
Issue #23 was closed by hand with the reason recorded on it, rather than
rewriting a pushed main. Nothing was stranded: no open unit declares a dependency
on U23. **Check whether a unit is trailer exempt before writing the merge commit,
not after pushing it.**

**Two agents on one machine share a process namespace, and METHOD's isolation
rules do not cover that.** The U23 agent killed its own backgrounded driver with
`pkill -f "scripts/mutate.py"`, and that pattern also matched the U27 agent's
driver on a different branch in a different worktree with a different venv. It
verified afterwards that U27's tree was clean and it was, so no measurement was
corrupted, and that was luck rather than design. Own worktree, own venv and own
scratch directory are three kinds of isolation that all stop at the process
table. Kill by PID, or by a pattern naming the unit.

## What the next session does

1. **U27 needs a decision, not a fix round in the usual sense.** R-80 names three
   closing conditions. The structural one, moving the probe out of the refusal
   vocabulary, is the honest answer and is not a merge's work. Read R-80 and
   `merge/u27-attempt-2026-08-14` before touching anything.
2. **U12** is the last unmerged unit that has never been verified. The harness
   provides what it was waiting for: `time_repeated(fn, repeats=25,
   threshold_seconds=threshold_seconds(multiplier))`.
3. `docs/METHOD.md` still wants its trim pass. The countdown lesson in it is now
   one line plus a pointer to the solutions document, not a section.
