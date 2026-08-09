# Restart: Cratekit parallel wave

**Last session 2026-08-09.** It resumed the wave the weekly budget cut short on
2026-08-04, finished the one unfinished fix round, and ran three independent
adversarial verifications. All three returned BLOCKING. Nothing merged.

## Do this first

1. Read `docs/wave-state-2026-08-09.md` in full. It is this session's durable
   record: three verdicts, the findings that generalise, and two process
   failures worth not repeating.
2. `docs/wave-state-2026-08-04.md` stays authoritative for everything earlier,
   including the wave's method, the four recurring defect patterns and the
   standing mutation driver rules. Read it second, not instead.
3. `CLAUDE.md` is the session contract and is current.
4. `DJ_tools/docs/migration/00-SEAM-DECISIONS.md` is authoritative over any
   brief. Part 5 applies to every unit.

## Main, verify before trusting it

Confirmed clean at the end of the 2026-08-09 session.

    git log --oneline -1
    git status --porcelain            # must be empty
    .venv/bin/pytest --tb=no          # 3422 passed, 17 skipped
    .venv/bin/python scripts/board.py audit   # must be exit 0

**No unit has merged since U32.** U32 is still the only unit ever to clear the
merge criterion.

## Phillip's two standing decisions, both taken 2026-08-09

1. **Narrow fan-out.** Verify two or three units per session, highest value
   first. Do not relaunch the seven agent wave.
2. **The merge exit criterion STANDS.** Nothing merges until a branch verifies
   CLEAN. Merging on zero BLOCKING with residuals was considered and declined.

The 2026-08-04 decisions all still hold: U27 and U24 merge WITHOUT closing
trailers, do not touch U30's board state, U20, U29, R-9, A1 or A2.

## The eight branches, all clean, none merged

| unit | tip | state |
|---|---|---|
| u12 | `fc73b82` | round 6, never verified. Untouched 2026-08-09. |
| u16 | `3262bc8` | round 7, never verified. Untouched. Merges AFTER U24. |
| u23 | `6f8db39` | round 8, never verified. Untouched. |
| u24 | `b5a4e86` | **round 9, never verified.** The only round in flight. |
| u27 | `44ced7e` | round 8, never verified. Untouched. |
| u34 | `85eb996` | round 9 **verified BLOCKING, 4 findings.** Needs round 10. |
| u38 | `171e058` | round 7 **verified BLOCKING, 4 findings and 7 residuals.** Needs round 8. |
| conformance | `897ef12` | parked. Its `write/metadata.py:195` defect is still live on main. |

## What to do next, in order

1. **Verify U24 round 9.** It is committed and has never been attacked. Round 9
   fixed round 8's own defect, which was itself the third consecutive instance
   of "a fix that lands on the wrong object" on that one branch, so it deserves
   a hostile read.
2. **U34 fix round 10.** Lead with B2: the aging report renders CLEAN over an
   intake tree whose node types it could not read, and the misread nodes satisfy
   the very guard written to catch their loss. It is the only finding this
   session with a direct user facing cost.
3. **U38 fix round 8.** Lead with B3: the test forbidding a per-line escape
   hatch pins the deleted hatch's symbol names rather than the property, so a
   fresh hatch with a different marker ships green.
4. U12, U23 and U27 are still at their 2026-08-04 tips with their 2026-08-04
   attacks queued. They were skipped deliberately, because their queued work
   needs a 25 run timing measurement, a mounted FAT image and a real read only
   volume image.

## Two things that will bite you again

**Give every parallel agent its own scratch directory, named for its unit.** A
shared scratchpad collided across three concurrent verifiers on 2026-08-09, the
second occurrence of this failure. Two careful agents caught it; no measurement
was corrupted, and that was luck.

**Never pass `-q` to pytest, including to a collection run.** `pyproject.toml`
sets it, a second one becomes `-qq`, and it suppresses both the summary line and
the collect listing. This broke a mutation driver's collected-count column on
2026-08-09 so that it read a constant zero on every row.

## Still open, still blocking merges

The residual numbering decision from `docs/wave-state-2026-08-04.md` is
unchanged: six numbers collide with different content across branches. A branch
can merge only if its residual section is append only or its numbers happen not
to collide. The recommendation on record is to renumber sequentially at each
merge, now that citations are moving from numbers to titles.

## One thing the board cannot tell you

Two agents committing in one working directory on one branch makes "hold this
until review" unenforceable, because a push carries whatever else is sitting on
the branch. It happened on 2026-08-02. If a second session might be running,
either work in a worktree or say so before you start.
