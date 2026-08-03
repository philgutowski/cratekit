# Cratekit

Acquisition and curation for rekordbox DJs. A slim core, toggleable feature
modules, and guarded library writes.

This file is the session contract. `docs/HANDOFF.md` is the narrative state and is
what to read next.

## The board is the queue

Work is not picked from a plan document, a backlog, or a conversation. It is
picked from the board:

    https://github.com/users/philgutowski/projects/2

Every implementation unit, residual finding, and attended item is an issue on this
repository, and the issue number matches the unit number: U11 is issue #11.

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
- **Exit 2, contradiction.** A unit's issue is closed while a register still owes
  it a module, so the board says work landed that the repository says did not.
  Two registers are read: `tests/_pending.py`, and the `planned_in` markers on
  the verb registry. `sync` deliberately will not touch these, because repairing
  them automatically means picking one source of truth to overwrite, which is how
  the wrong one wins silently. Either reopen the issue or clear the register
  entry.

Run the audit even when you changed nothing, because the cheapest time to catch
drift is before it is load-bearing.

**Before writing a merge commit that closes a unit:**

    .venv/bin/python scripts/board.py closing --since main

Exit 2 means the trailer you are about to write closes a unit that a register
still owes a module. That is the same comparison `audit` makes, asked before the
close instead of after it, and it is the last moment it is cheap: once the close
has cascaded, `sync` will not repair it. It is network-free, so it works with no
token. It runs in CI on every push and in a `commit-msg` hook if you installed
that hook type, and it is here as well because the hook is absent from a fresh
clone (R1) and CI answers after the push rather than before it.

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
