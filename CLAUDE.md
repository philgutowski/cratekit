# Cratekit

Acquisition and curation for rekordbox DJs. A slim core, toggleable feature
modules, and guarded library writes.

This file is the session contract. **`docs/METHOD.md` is the operating
instruction and is what to read next**: the pipeline, the merge bar, the
mutation method, the driver rules, the merge constraints and the do-not-touch
list. `RESTART-cratekit.md` is the verified current state, and each unit's own
record of it is a file in `docs/restart/`. `docs/history/` is
the narrative record of how the rules were arrived at, read for reasoning, never
for instruction.

Two more are worth knowing about rather than reading front to back.
`docs/solutions/` is the durable record of problems already solved here, filed by
category with YAML frontmatter (`module`, `problem_type`, `tags`) so it can be
searched rather than read; most entries are traps that cost real time once and are
written so they do not cost it twice. `CONCEPTS.md` is the shared vocabulary, the
words that carry a specific meaning in this project rather than their ordinary
one. Both are relevant when starting work in an area either one covers, and
`CONCEPTS.md` is the faster of the two when a term is the thing that is unclear.

## How a session runs, decided 2026-09-07

**The compound engineering plugin is not used here.** No `ce-plan`, `ce-work`,
`ce-code-review`, `ce-compound`. Native Relay, which runs METHOD's pipeline and
none of those skills, drives unattended runs, and METHOD's Relay section says
how. A session does the whole of one unit itself: plan mode against the issue brief,
build, the built in `/code-review`, an author's mutation table capped at 25
rows, the record, the merge. METHOD's pipeline section is the exact sequence.

A restart prompt names a board item and nothing else, because the issue is the
brief. "Take #56" is a complete instruction once this file and METHOD are read.
Nobody is watching a session while it runs, so a question is a stop: make the
conservative call, record it as a residual, and keep going.

**The unattended build system starts with one word: `/board-up`** (the
`board-up` skill, decided 2026-10-10). It checks that nothing is running, that
cards are Ready, that rekordbox is closed and the checkout free, then starts
the Relay feeder, the watcher, the fable builder and the operator seat from
`~/.relay/manifests/cratekit-board.lanes.toml`, one step at a time. Nothing
else needs remembering to launch it; `board-lanes` is the skill underneath.

## The board is the queue

Work is not picked from a plan document, a backlog, or a conversation. It is
picked from the board:

    https://github.com/users/philgutowski/projects/2

**The board is the BUILD. `docs/residual-findings.md` is the LEDGER.** Two
registers answering two questions, and they are not mirrors of each other.

- Every implementation unit `U-N` is an issue, and so is every attended chore
  `A-N`. Those are the work, and the board is where work is picked.
- A residual `R-N` is a real problem that was recorded rather than fixed, because
  it did not meet the bar to hold a merge. It lives in the file and usually has
  no issue. A unit files it unnumbered in `docs/residuals/`, and it takes its
  number when it lands on `main`. **Do not backfill the rest.** A residual earns an issue only if
  somebody decides to act on it, and the thirteen that have one are now in the
  queue behind the units, each to be done or closed back to the ledger.

An issue number usually matches its unit number, U11 is issue #11, and it is not
guaranteed: U38 is issue #51. Look it up before writing a trailer.

**Start every session here:**

    .venv/bin/python scripts/board.py next

That prints what is ready, ranked by how much of the remaining build each unit
releases, and names the one to take. **It will name #29 and you must not take
it.** U29 is attended. METHOD's do-not-touch section says why.

**Take a unit:**

    .venv/bin/python scripts/board.py start 11

That refuses if the unit is blocked, if the working tree is dirty, or if you are
not on `main`. Otherwise it branches, marks the issue In Progress, and prints the
closing trailer to use.

**The issue is the brief.** Each unit issue carries its full specification: goal,
requirements, dependencies, key files, approach, test scenarios, verification.
Read it with `board.py show 11`. If the brief is insufficient, fix the issue
rather than working around it.

`DJ_tools/docs/migration/00-SEAM-DECISIONS.md` remains authoritative over any
brief. Part 5 is seven failure shapes learned the expensive way and applies to
every unit.

## The board stays true on its own

End the merge commit with the trailer `board.py start` printed:

    Closes #11

Pushing `main` closes the issue, and `.github/workflows/board.yml` fires and flips
every unit that was waiting on it from blocked to ready.

Do not hand-edit `ready` and `blocked` labels or drag cards. Those are derived
values. Change the dependency line in an issue body and let the sync recompute
them.

**Before ending a session:**

    .venv/bin/python scripts/board.py audit

- **Exit 1, drift.** A derived value fell out of date. `board.py sync` repairs it.
- **Exit 2, contradiction.** A unit's issue is closed while a register still owes
  it a module, so the board says work landed that the repository says did not.
  Two registers are read: `tests/_pending.py`, and the `planned_in` markers on
  the verb registry. `sync` deliberately will not touch these, because repairing
  them automatically means picking one source of truth to overwrite, which is how
  the wrong one wins silently. Either reopen the issue or clear the register
  entry.

Run the audit even when you changed nothing.

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

The suite runs across every core and takes about a minute. It is the merge
gate, not the edit loop: while building, run the test files for what you
touched. METHOD's battery section has the numbers.

An author's own battery is not a review. Every defect the adversarial reviews
found in this repository passed a green suite written by the person who wrote the
defect. After a unit's suite is green, hunt what a green suite cannot see. METHOD
lists what.

## Standing constraints

- **Never write a beat grid.** Not a tempo element, not a BPM tag, not an
  average-BPM field, not an ANLZ grid, in any container. Two suites enforce this
  across five surfaces. Absolute.
- **The live rekordbox database is protected, not untouchable.** The default is
  hands off, and a unit needing a real database makes a disposable copy in a
  temporary directory rather than reaching for the live one. The exception is the
  backup feature, whose whole job is to capture that file: it may read and copy
  the live database, but only with both `rekordbox` and `rekordboxAgent`
  confirmed gone, only into a new dated destination, and never in place. Writing
  to the live database outside a gated destructive session stays forbidden.
- **rekordbox is opened by an attended session and by nothing else**, decided
  2026-09-29. A session Phillip is present for may open, drive and quit
  rekordbox on the live library through the desktop control tool, to import,
  to let it analyse, and to read what it shows. A Relay run, a job, a verb and
  a test never launch rekordbox or its background agent. Before opening it: no
  Cratekit job is running, and `crate doctor` reads both backup ages under one
  day. After quitting it: `rekordbox` and `rekordboxAgent` are both confirmed
  gone before any verb runs.
- **A database write gate is approved by the session only when a rehearsal
  matches**, decided 2026-09-29. The session drives the same verb on a
  disposable copy with library state redirected, reads the result, and then
  brings the live plan to its gate. If the live digest equals the rehearsed
  one, the session approves and reports. **If it differs, the session still
  approves**, decided by Phillip on 2026-10-09 ("don't ask for my approval on
  anything going forward"), after reading the difference and recording it in
  the sitting record; a rehearsal that fails, or a difference in what is
  written rather than in a path, is the one case that still stops. The actor
  on every gate is `session`. **The backup acknowledgment may be minted by
  the session**, decided by Phillip on 2026-10-09, reversing the 2026-09-29
  rule: the gate shows both backup ages and the person only pasted a command,
  so the session reads the ages, refuses unless both are under one day, and
  answers with the actor `session`. The verb still wants a controlling
  terminal, so until a card lets it accept the session, it is run under
  `script -q /dev/null`.
- **DJ_tools is read-only for code.** It is the live system until each workflow's
  replacement is proven. Its `docs/` are the exception.
- **Do not symlink `.venv` into a worktree.** The editable install names the
  checkout it was installed from, so a worktree would verify code it cannot see.
- **No pull requests.** Feature branch per unit, merge to `main` locally, push
  `main`, delete the branch.
- **No em dashes, en dashes, or double hyphens** in any prose, code comment,
  commit message, or issue body. Do not swap a dash for a colon; favor commas,
  and keep colons for a genuine list or definition.
- **Explanations are batched per phase.** A unit lands with its commit messages
  and its record. Phillip runs the explainer over a merged phase when he wants
  it. A session does not run it.
