# Cratekit

Acquisition and curation for rekordbox DJs. A slim core, toggleable feature
modules, and guarded library writes.

This file is the session contract. **`docs/METHOD.md` is the operating instruction
and is what to read next**: the merge bar, the mutation method, the driver rules,
the merge constraints and the do-not-touch list. `RESTART-cratekit.md` is the
current wave state and `docs/HANDOFF.md` is the longer narrative.

A restart prompt names board items and nothing else, because the issue is the
brief. `/ce-work #56` is a complete instruction once this file and METHOD are
read.

## The board is the queue

Work is not picked from a plan document, a backlog, or a conversation. It is
picked from the board:

    https://github.com/users/philgutowski/projects/2

**The board is the BUILD. `docs/residual-findings.md` is the LEDGER.** Two
registers answering two questions, and they are not mirrors of each other.

- Every implementation unit `U-N` is an issue, and so is every attended chore
  `A-N`. Those are the work, and the board is where work is picked.
- A residual `R-N` is a real problem that was recorded rather than fixed, because
  it did not meet the bar to hold a merge. It is not a queued task, it is the
  honest register of what is known and accepted, so it lives in the file and
  usually has no issue at all. Fifteen of one hundred and fourteen do, which is
  an artifact of a single batch created on 2026-08-02 rather than a rule.
  **Do not backfill the rest.** Putting the ledger on the board would claim you
  intend to do a hundred things you have decided not to do, and would flood the
  project board's Ready column, because a non unit issue with nothing waiting on it
  derives as Ready. `board.py next` filters to units and would be unaffected, so
  the damage is to the view a person reads rather than to the tool. A residual
  issue is also unstable before its unit merges, since a merge renumbers the
  incoming branch's residuals and the issue title keeps the old number.
- A residual earns an issue only if somebody decides to act on it. `board.py
  audit` then checks that the issue still names the finding its number points at,
  because a residual's number lives in its issue title, which is a surface the
  repository cannot otherwise see.

An issue number usually matches its unit number, U11 is issue #11, and it is not
guaranteed: U38 is issue #51. Look it up before writing a trailer.

**Start every session here:**

    .venv/bin/python scripts/board.py next

That prints what is ready, ranked by how much of the remaining build each unit
releases, and names the one to take. Ranking is by transitive reach rather than
direct dependents, because a unit whose one dependent is the gateway to a whole
phase outranks a unit with three dead-end dependents.

**Take a unit:**

    .venv/bin/python scripts/board.py start 11

That refuses if the unit is blocked, if the working tree is dirty, or if you are
not on `main`. Otherwise it branches, marks the issue In Progress, and prints the
closing trailer to use.

**The issue is the brief.** Each unit issue carries its full specification copied
from the plan: goal, requirements, dependencies, key files, approach, test
scenarios, verification. Read it with `board.py show 11`. Do not go hunting for
the plan document unless the brief is genuinely insufficient, and if it is, fix
the issue rather than working around it.

`DJ_tools/docs/migration/00-SEAM-DECISIONS.md` remains authoritative over any
brief. Part 5 is seven failure shapes learned the expensive way and applies to
every unit.

## The board stays true on its own

End the merge commit with the trailer `board.py start` printed:

    Closes #11

Pushing `main` closes the issue, and `.github/workflows/board.yml` fires and flips
every unit that was waiting on it from blocked to ready. That chain has exactly
one human act in it, writing the trailer, and it is the act that was going to
happen anyway.

Do not hand-edit `ready` and `blocked` labels or drag cards. Those are derived
values. Change the dependency line in an issue body and let the sync recompute
them, or the board becomes a thing that has to be remembered rather than a thing
that is true.

**Before ending a session:**

    .venv/bin/python scripts/board.py audit

Two failure modes, and they are not the same thing:

- **Exit 1, drift.** A derived value fell out of date. `board.py sync` repairs it.
- **Exit 2, contradiction.** A unit's issue is closed while `tests/_pending.py`
  still owes it a module, so the board says work landed that the repository says
  did not. `sync` deliberately will not touch these, because repairing them
  automatically means picking one source of truth to overwrite, which is how the
  wrong one wins silently. Either reopen the issue or clear the register entry.

Run the audit even when you changed nothing, because the cheapest time to catch
drift is before it is load-bearing.

## The battery

Nothing merges until all three are clean:

    .venv/bin/ruff check src tests scripts
    .venv/bin/python -m pytest
    .venv/bin/python scripts/scan_repo.py

An author's own battery is not a review. Every defect the adversarial reviews have
found in this repository passed a green suite written by the person who wrote the
defect. After a unit's suite is green, hunt what a green suite cannot see:
duplicate keys in a mapping several branches appended to, and one symbol meaning
two things in two modules.

## Standing constraints

- **Never write a beat grid.** Not a tempo element, not a BPM tag, not an
  average-BPM field, not an ANLZ grid, in any container. Two suites enforce this
  across five surfaces. Absolute.
- **The live rekordbox database is off limits.** Never open, copy, or name it. A
  unit needing a real database makes a disposable copy in a temporary directory.
  Never launch rekordbox or its background agent.
- **DJ_tools is read-only for code.** It is the live system until each workflow's
  replacement is proven. Its `docs/` are the exception.
- **Do not symlink `.venv` into a worktree.** The editable install names the main
  checkout's `src`, so a worktree would verify code it cannot see.
- **No pull requests.** Feature branch per unit, merge to `main` locally, push
  `main`, delete the branch.
- **No em dashes, en dashes, or double hyphens** in any prose, code comment,
  commit message, or issue body.
- **Ship the explanation.** Every unit lands with the code and architecture
  explanation Phillip's standing rule asks for. He is learning this codebase as it
  is built and should be able to explain any of it in an interview.
