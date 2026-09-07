# Wave state, snapshot taken 2026-08-03

**This is a snapshot and it goes stale.** `RESTART-cratekit.md` explains why a
second copy of a fact is how the two come to disagree. Trust `git log`, the
branch tips, and `board.py next` over anything written here. This file exists
only because the per-branch review state is not recorded anywhere else.

## What is on main

`3269ab1`, pushed. One merge: the conformance 3 correction, alone.

Two files, `tests/test_cli_contract.py` and `docs/residual-findings.md`. **Zero
production source.** `gates.py`, `registry.py` and `cli/__init__.py` are
byte-identical to where they were.

It fixes an assertion that demanded a violation of the rule it enforced.
`test_conformance_3` drove an inline `-d` answer at an explicitly gated verb and
asserted exit OK, but R34 requires an explicit gate to refuse an inline answer.
Fifteen registry entries declare an explicit gate; all were unlanded. Four units
independently concluded their verb "cannot land" and paid register bookkeeping
to work around it. The wall was this test.

Verified: battery green on main, plus a mutation test (mutate the landed gated
verb to never ask its declared gate; the assertion fails as it should).

## What is NOT on main, deliberately

`fix/conformance-3-and-soft-delete-reader` is parked. It carries the live
`write/metadata.py:195` permissive-reader fix and the `board.py` closing rules.
Its guards took defects in **three consecutive rounds** of verification, so only
the conformance third was lifted out. The metadata defect is still live on main.

## The nine unit branches

None merged. All have had implementation, two adversarial reviews, at least one
fix round, and most have had verification.

| Branch | State |
|---|---|
| `unit/u36-...` | **SAFE TO MERGE.** Round 2 verified clean. |
| `unit/u32-...` | Round 3 landed (`c7a1a7d`), needs verification |
| `unit/u38-...` | Round 2 landed (`a08c695`), needs verification |
| `unit/u24-...` | Round 2 landed (`400f87a`), needs verification |
| `unit/u16-...` | Round 2 landed (`13be438`), needs verification |
| `unit/u23-...` | Round 3 verified: blocking, needs round 4 |
| `unit/u27-...` | Round 3 verified: blocking, needs round 4 |
| `unit/u12-...` | Round 1 verified: blocking, needs round 2 |
| `unit/u34-...` | Round 1 verified: fix required, needs round 2 |

Each worktree has its own venv. Run its battery from inside it:

    cd .worktrees/u36 && ./.venv/bin/python -m pytest

## Phillip's decisions, standing

**U27 merges WITHOUT a `Closes #27` trailer** (decided 2026-08-03). Three
branches parked register obligations on U27 for modules that exist nowhere:
`cratekit.adopt.apply_cli` (u23), `cratekit.cli.reports` (u34),
`cratekit.session.restore_cli` (u32). U27 is built with nothing left to write,
so closing it makes `board.py audit` return exit 2 permanently, and `sync`
refuses to repair a contradiction by design. Leaving #27 open costs nothing and
needs no edit on any branch. Add a comment on the issue recording the three.

**Do not touch:** U30's board state, U20, U29, R-9, A1, A2.

## Merge order and the traps

1. **U24 before U16.** After both, `match.TOMBSTONE_KIND` and
   `match.version_identity` collapse into imports from `core.tombstone`, and
   U24 must delete the `cratekit.core.tombstone` entry U16 added, which is what
   arms U16's cross-copy drift guard.
2. **U36 and U32 together, with SIX items, not four** (U32's R-21). Two are
   silent: dropping `@requires("cratekit.write.rebuild")` in
   `tests/test_restore.py`, or that file fails to COLLECT and roughly 200 tests
   vanish with a green-looking run; and re-pointing the handoff test to patch
   `convergence.mark_unconverged`. U32's own trial merge with all six: 3394
   passed.
3. **U27 without the trailer.**

**Silent trap:** `tests/_pending.py` between u23 and u34 is a false conflict in
**two** hunks. Both deletions must survive AND both additions must survive.
Taking either side wholesale is wrong in both.

**Convergent duplicate:** u23 and u34 independently made the same fix to
`test_every_new_adjudication_surface_is_owed_by_a_registered_unit`. u34 adds
`_target_offers_into`; u23 widens `_package_offers_into` to do the same job.
Delete one at merge.

**Three copies of one walk:** U12's `ImportsOf`, U38's `ExitCodeImports`, and
the parked branch's `SoftDeleteNames`. All merge clean, no behavioural
divergence today. Book the collapse as follow-up.

Use git's merge algorithm only. `diff3 -m` silently produces a broken merge of
`tests/_pending.py`.

Residual-finding numbers collide across branches. Renumber sequentially from
R-16 in merge order and verify with:

    grep "^## R-" docs/residual-findings.md | sort | uniq -d   # must be empty

## The technique that found the most

Ask every fix round for a **mutation table**: revert each new guard one at a
time, run the suite, count the deaths. A guard that kills zero tests is a
finding.

It caught, among others: a guard covered by nothing whose docstring called it
the answer to the original defect; an exactness test that defined its expected
value by calling the function it verified (a deliberately lossy reader passed
3324 tests); and every tuning constant in U12 surviving being moved, including a
swap threshold changed from 1 GiB to **one byte** with the suite green.

## The through-line

Written up in `docs/wave-explainer-DRAFT.md`. Six patterns, of which the two
worth carrying into any project:

**Absence read as evidence of absence.** "I could not observe" folded into
"there is nothing there." Independently in five units.

**Identity that is not unique to the thing it identifies.** Two units wrote
incompatible `version_identity` functions; one treated a library-wide bucket
name as proof of authorship; one keyed a latch on an id new on every attempt;
one keyed a plan on display names. Ask of every identifier: *what two different
things could produce this same value?*

And the thing I got wrong: **fix rounds are about as defect-prone as
implementation rounds**, and they fail in the opposite direction, by being too
restrictive or by relocating a hole rather than closing it.
