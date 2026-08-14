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

<!-- ------------------------------------------------------------------ -->

# Second session, 2026-08-14: the guard was asked what it saw, and said something else

The session above ended by sending U27 back for a decision between three
resolutions. This one went to take that decision and found the finding's recorded
mechanism was wrong, which changes what the decision is between. Nothing was
merged. `main` moved by two docs commits and is otherwise untouched.

## The compound artifact from the previous session was sitting uncommitted

`CONCEPTS.md` and
`docs/solutions/workflow-issues/merge-falsifies-a-guard-invariant-and-every-remedy-breaks-something.md`
were finished and unstaged. Every line reference in the document was resolved
against the tree before committing, and all of them held. Committed as `1ac0cac`
and pushed.

## R-80's mechanism, corrected by driving it

R-80 said `_os_open_reads` declines the probe's flags because one branch of
`os.O_RDWR if writing else os.O_RDONLY` is not a read. The learning document
written alongside it corrected that to unreadability, which is the right
category, and then named the wrong unreadable shape, the conditional.

**Both are wrong. The guard never sees the assignment.** It reads the call
argument, and the call is `os.open(path, flags)` whose argument is a bare local
name. Five rewrites of the assignment were driven and all five stayed red,
including `flags = os.O_RDONLY` with no conditional and no `getattr`:

| assignment, call left as `os.open(path, flags)` | guard |
|---|---|
| `os.O_RDONLY` | RED |
| `os.O_RDONLY \| os.O_NONBLOCK` | RED |
| `os.O_RDONLY \| getattr(os, "O_NONBLOCK", 0)` | RED |
| `os.O_RDWR \| os.O_NONBLOCK` | RED |
| `os.O_RDWR` | RED |
| **inlined** `os.open(path, os.O_RDONLY \| os.O_NONBLOCK)` | **GREEN** |
| **inlined** `os.open(path, os.O_RDWR \| os.O_NONBLOCK)` | RED |

The guard is saying "I cannot tell what this opens", not "this writes", and on a
readable shape it is exactly right in both directions. **Three accounts of a
thirty line helper were written from reading it, by three readers including an
independent verifier, and the first two were wrong in different ways.** It
answers in under two seconds when asked. METHOD's driven-end-to-end rule applies
to a finding's MECHANISM and not only to its existence, and that is the lesson
worth more than the correction.

The correction opens a fourth resolution nobody could see while the conditional
was believed to be the problem: split the probe's two intents so the read only
one spells its flags at the call site, leaving only `_from_database_error` to
answer for.

## The first closing condition is achievable and fixes nothing

R-80's first resolution, and the one both it and the previous session called the
honest structural answer, was driven. Moving the raw open into
`cratekit.core.access_probe`, which the allowlist does not admit, and leaving
`cause.py` calling it, turns the guard **green** with the chain from the reports
package to a write capable handle untouched.

`test_the_package_imports_downward_only` catches that relocation, because `cause`
is FOUNDATION by explicit name and a new `cratekit.core.*` module defaults to
INFRASTRUCTURE. **It is then satisfied by adding one name to one regex**, after
which the suite is green apart from two unrelated pre-existing failures.

Both structural guards, satisfied by a change that fixes nothing. Filed as
**R-102**, because the hole is in the guard rather than in the merge: the audit
walks only the modules the allowlist NAMES, so any admitted module can delegate
its writing one hop out and be read as ordinary code. Sideways delegation, to a
module at the same layer, evades the layering guard too.

## The write capable handle is pinned by nothing

Forcing the probe to `os.O_RDONLY` always killed **zero** tests: 3 failed, 5030
passed, 11 skipped, 5044 collected, which is the baseline exactly. Three of
R-80's four resolutions change this behaviour and the suite would not notice any
of them. Whichever is taken brings its own evidence.

## The preserved merge branch is red on THREE guards, and every record said one

Measured on `merge/u27-attempt-2026-08-14` at `01eb6da`: 3 failed, 5030 passed,
11 skipped, 5044 collected. R-80 is one. The other two are that branch's own
unfinished re-pinning, and neither is a second collision:

- the kebab literal pin holds `(256, 156)` against a tree measuring `(268, 163)`.
  The branch re-pinned the cause population and not this one.
- the refusal walk sees `grant-path-access`, the reservation that same branch
  added, against a fixture expecting `{repair-backup-facts, upgrade-cratekit}`.

Re-measure and re-pin work, never widen. Recorded so the next session does not
resolve R-80, meet two unexplained reds, and start hunting a collision that is
not there.

## A driver bug, caught by its own output

One batch of four rows was run through a shell function that never passed its
argument to `python3 -c`, so no mutation was applied and all four reported the
previous row's result. It was visible only because the traceback printed above
each identical result line. The rows were discarded and re-run through a script
file taking real arguments. **Four rows that would have read as a clean
measurement.** METHOD's rule against hand rolled drivers earns itself again;
these were single line edits that felt too small to need `scripts/mutate.py`.

## What the next session does

1. **U27 still needs the decision, now between four resolutions rather than
   three**, with the fourth the smallest and none of them validated by the suite.
   Read R-80 first; it carries every measurement above.
2. **U12**, still the last unverified unit, untouched by any of this.
3. R-102 is open on `main` and is nobody's merge blocker.

## The fourth resolution was taken, and R-80 is now one function

Phillip chose the split. It landed on `unit/u27-setup-wizard-and-doctor` in two
commits, `10b9fdc` and `46e04ae`, pushed.

`_probe` became `_probe_readable` and `_probe_writable`, each spelling its flags
INLINE at its own call site, because that is the only shape the guard can read.
One call site can spell one expression, so the duplication is forced rather than
sloppy, and the reason is recorded in the source next to it: folding them back
into a shared helper taking `flags` is the obvious tidy up and silently restores
the unreadable shape. The `getattr(os, "O_NONBLOCK", 0)` fallback was measured
unreadable by the same guard and is now spelled directly.

**Verified on a REAL merge rather than on the branch**, because `main` had
touched `cause.py` since the branch point and only a merge answers what the guard
will see. Scratch clone, `git merge`, six conflicts matching the preserved
attempt, and `cause.py` among the files that auto merged clean:

| tree | the guard reports |
|---|---|
| before | `['_probe']`, three call sites, two of which only ever read |
| after | `['_probe_writable']`, one function, one call site |

## What the write capable handle buys, and the honest shape of the answer

Six scenarios driven against the alternative that never opens write capable and
infers from `statvfs` `ST_RDONLY`, the existing `_immutable` helper and
`os.access`. Ordinary file, `chmod 444`, `chflags uchg`, an ACL denying write
with the mode still 644, an absent file, and a real read only mounted volume.
**All six agree.**

That is written as "six were driven and all six agree", never as "the handle buys
nothing", because the class where they are known to diverge was not driven: a
network mounted volume, where the client can answer while the server is what
refuses.

The reframing that weakens the objection, and the thing to attack first next
time: the write probe is only ever reached for a driver error that is not
`SQLITE_CANTOPEN`, so the driver has ALREADY established that a write was
refused. The probe disambiguates why rather than predicting whether, and network
staleness is a much smaller hazard for explaining a refusal than for predicting
one.

## The behaviour is pinned now, and it was pinned by nothing before

`test_the_write_probe_classifies_every_way_a_write_is_refused`. Three live rows,
each verified to bite rather than silently skip, plus a negative row so they are
not passing on a probe that refuses everything. With the write handle mutated to
read only the test fails and the other 251 tests in its file pass.

**The same mutation killed zero of 5044 before it existed.** Every candidate
resolution changes this behaviour, so the decision was about to be taken over a
suite that could not see the difference. Pinning first was worth more than
deciding fast, and it is the step that was available regardless of which way the
decision goes.

## U12 merged, and the coordination note that had aged

Verified MERGE by an independent pass that did not write the code: 45 rows
against the cap, 44 killed, one zero, that zero promoted to the full suite and
shown effectively equivalent for any importable source. Five residuals, none
blocking. **Eight units have now cleared the merge bar.**

The merge's real work was `tests/_source_guards.py`, where both sides had
independently generalized one import walk. `main` carried a coordination note
naming U12 by name and saying the collapse must take `_import_targets` with it,
because the other copies "still carry the suffix match this file has now
replaced in both of its own".

**That note had aged and checking it was worth the trip.** The branch had since
grown its own resolution in `_absolute_module`, and the two resolvers were
compared directly on the climb cases rather than read: they agree, including the
off the top case that returns None. So the collapse onto the branch's module
parameterized `ImportsOf` reinstates nothing. The note was right that the
collapse is not textual, and wrong about which copy was defective by the time
the two met. A merge instruction is a measurement with a date on it.

**What the merge did have to add**, and it is the shape worth carrying: the
generalization arrived on one branch and the `package` argument that makes the
relative half exact arrived on the other. The subclass took only a tree, and
every review caller on the other side passes a package positionally. That
mismatch raises NOTHING, because the resolution falls back to matching by dotted
tail, so the failure is a guard answering about the wrong file. Driven rather
than assumed: three tests fail without the forward, the first reporting offenders
in a source that has none.

`tests/_pending.py` auto merged and was verified by hand rather than trusted:
main's ten keys plus `cratekit.analysis`, the one key the branch adds, with the
`EXPECTED_PENDING` mirror resolved as a union. No countdown discharge here.

### The renumber, and one judgement inside it

Twelve residuals arrived. Seven collided and became R-108 through R-114; R-103
through R-107 kept their numbers because `main`'s highest was R-102. **R-18 did
not collide**, `main` having a gap there, and it was moved with its siblings
anyway rather than dropped into the gap, because a lone finding seated between
`main`'s unrelated R-17 and R-19 reads as belonging to a sequence it has nothing
to do with. Nothing inside the twelve cited a moved number, checked rather than
assumed. The `R23` token that looks like a citation is a plan REQUIREMENT, as are
R29, R31 and R34 elsewhere in the file, and a regex that treated those as
residuals would have repointed four requirements at findings.

### The reconciliation

5689 in the union, 5665 collected, **24 present on a side and absent, all 24
accounted for.** Fourteen are `main`'s rename of conformance 3, which carries 22
identifiers on both sides. Five are register keys `main` has discharged. Four are
planned verbs that have landed and correctly lost their markers. One is
`deletion_verb` to `deletion_pass`. None is lost coverage.

## R-115: ten red CI runs that nobody had looked at

Found by reading the run LIST rather than a run, immediately after the push.
**Every CI run on `main` in the visible history is a failure**, back through ten
commits and several merges, while the local battery was clean for every one.

It is not a regression and nothing is broken. The workflow runs Linux and this
product targets macOS: the hardware proofs require `hdiutil` and **fail rather
than skip** by deliberate design, the calibration correctly refuses a baseline
from a different machine, and one test receives `OS linux not supported!`.

The cost is that a signal exists which cannot change state. Red when the tree is
perfect is red when the tree is broken. It is the same defect as the flaky
battery and the silent countdown, in the shape this project is least equipped to
notice, because the thing carrying no information sits OUTSIDE the battery.
METHOD rests the whole merge discipline on three local commands and never
mentions CI, which is exactly why ten red runs went unremarked.
