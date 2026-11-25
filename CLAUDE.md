# Cratekit

Acquisition and curation for rekordbox DJs. A slim core, toggleable feature
modules, and guarded library writes.

This file is the session contract, kept short because every session and every
agent loads it on every call (U196). **`docs/METHOD.md` is the operating
instruction and is what to read next.** `docs/METHOD-local.md` is the part only
a session on Phillip's Mac needs. `RESTART-cratekit.md` is the verified current
state, read by a local session; each unit's own record is a file in
`docs/restart/`. `docs/history/` is narrative, read for reasoning, never for
instruction. `docs/solutions/` is the record of problems already solved, filed
with YAML frontmatter (`module`, `problem_type`, `tags`) so it is searched
rather than read: grep it by module before touching an area. `CONCEPTS.md` is
the shared vocabulary; grep it for a term that is unclear, never read it whole.

## How a session runs

**The cloud is where Cratekit is built**, decided by Phillip on 2026-10-27:
the building project's threads each run the `cloud-unit` skill on a card,
and his other project files cards with the `file-card` skill and keeps the
decisions page (METHOD's Sharing the board). A session does the whole of a
unit itself. **Only a card that cannot be built without the machine is built
locally**, by `docs/METHOD-local.md`.

Every question for Phillip reaches the decisions page,
https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS, where he answers with a
tap; a build thread asks on its card only, and the other project copies the
question to the page and his answer back. Nobody is watching a session while
it runs, so a question is a stop: make the conservative call, record it as a
residual, and keep going.

## The board is the queue

Work is picked from the board, https://github.com/users/philgutowski/projects/2,
never from a plan document or a conversation. Every implementation unit `U-N`
and every attended chore `A-N` is an issue, and **the issue is the brief**
(goal, requirements, dependencies, key files, approach, test scenarios,
verification): if it is insufficient, fix the issue rather than working around
it. An issue
number does not always match its unit number (U38 is issue #51), so look it
up before writing a trailer. **U29, #29, is attended and never a session's to
take**, whatever a queue says; METHOD's Do not touch says why.

The LEDGER is `docs/residual-findings.md` and its archive `docs/ledger/`. A
residual `R-N` is a real problem recorded rather than fixed; a unit files it
unnumbered in `docs/residuals/`, it takes its number when it lands on `main`,
and it earns an issue only when it meets METHOD's board bar. **Do not
backfill the rest.** Search it with `board.py residuals --search WORDS`.

The merge commit ends with the closing trailer, `Closes #N`, and pushing
`main` closes the issue; the board workflow then flips every unit waiting on
it from blocked to ready. Never hand-edit `ready` and `blocked` labels or drag
cards: change the dependency line in an issue body and let the sync recompute
them. `board.py closing --since origin/main` before writing a trailer refuses
one that closes a unit a register still owes a module.

`DJ_tools/docs/migration/00-SEAM-DECISIONS.md` remains authoritative over any
brief. Part 5 is seven failure shapes learned the expensive way and applies to
every unit.

## The battery

Nothing merges until all three are clean:

    .venv/bin/ruff check src tests scripts
    .venv/bin/python -m pytest
    .venv/bin/python scripts/scan_repo.py

On Linux the suite is read against the base's own failures (METHOD). An
author's own battery is not a review: every defect the adversarial reviews
found here passed a green suite its author wrote, so after a green suite,
hunt what a green suite cannot see, as METHOD lists.

## Standing constraints

- **Never write a beat grid.** Not a tempo element, not a BPM tag, not an
  average-BPM field, not an ANLZ grid, in any container. Two suites enforce
  this across five surfaces. Absolute.
- **The live rekordbox database is protected, not untouchable.** The default
  is hands off: a unit needing a real database makes a disposable copy in a
  temporary directory. The exception is the backup feature, which may read and
  copy the live database, but only with both `rekordbox` and `rekordboxAgent`
  confirmed gone, only into a new dated destination, and never in place.
  Writing to the live database outside a gated destructive session stays
  forbidden.
- **rekordbox is opened by an attended session and by nothing else**, decided
  2026-09-29. A session Phillip is present for may open, drive and quit
  rekordbox on the live library through the desktop control tool, to import,
  to let it analyse, and to read what it shows. Where an attended card asks
  what rekordbox itself writes, it may also make, on a throwaway track and a
  playlist made by hand for the check, the change that card names (removing it
  from the collection, setting cues, playing it on a deck, deleting that
  playlist), and may change an analysis setting a probe names and put it back
  to Phillip's standard, read back by a screenshot; never on a real track, and
  never a change the card does not name (U321). A cloud session, a job, a verb
  and a test never launch rekordbox or its background agent; the checks before
  opening it and after quitting it are `docs/METHOD-local.md`'s. The analysis
  visit after a landing follows the project's `rekordbox-visit` skill step by
  step (U173), and a whole sync pass, from the account's new music to filed
  and analysed, follows the project's `crate-sync` skill (U174). A whole
  attended sitting, every open attended card driven with worker sessions,
  follows the project's `attended-orchestrator` skill (U316).
- **A backup is needed only when the library is more than five days out of
  date, or when Phillip asks for one**, decided by Phillip on 2026-10-10,
  relaxing the one day rule of 2026-09-29; `docs/METHOD-local.md` says how a
  sitting reads the ages.
- **A database write gate is approved by the session only when a rehearsal
  matches**, decided 2026-09-29: the same verb driven on a disposable copy
  with library state redirected, then the live plan brought to its gate and
  approved, and reported, if its digest equals the rehearsed one. **If it
  differs, the session still approves**, decided by Phillip on 2026-10-09
  ("don't ask for my approval on anything going forward"), after reading the
  difference and recording it in the sitting record; a rehearsal that fails,
  or a difference in what is written rather than in a path, is the one case
  that still stops. The actor on every gate is `session`. **The backup
  acknowledgment may be minted by the session**, decided by Phillip on
  2026-10-09, reversing the 2026-09-29 rule: it reads both backup ages,
  refuses unless both are under five days, and answers as `session`, since any
  actor but `session` and the menu bar app's `app` (U962) takes the terminal
  rule, which checks no age. `docs/METHOD-local.md` has the command.
- **DJ_tools is read-only for code.** It is the live system until each
  workflow's replacement is proven. Its `docs/` are the exception.
- **Do not symlink `.venv` into a worktree.** The editable install names its
  checkout, so a worktree would verify code it cannot see.
- **A pull request per unit, merged by the session that opened it once CI is
  green**, decided by U158, replacing the old no pull requests rule; never one
  that waits on a person. **A cloud session merges itself**, attended or not,
  authorized by Phillip on 2026-10-27 ("I authorize you to merge to main here
  in the cloud now and going forward"). METHOD's Committing and merging has
  the rest.
- **Other builders share the board**, decided by Phillip on 2026-11-04. Never
  take a card or touch a branch held on `grok/`. METHOD's Sharing the board
  section has the rules, the limits and the definition of done.
- **No em dashes, en dashes, or double hyphens** in any prose, code comment,
  commit message, or issue body. Do not swap a dash for a colon; favor commas,
  and keep colons for a genuine list or definition.
- **Every doc is kept up to date**, decided by Phillip on 2026-11-07: a change
  lands with every doc it makes untrue corrected in the same pull request, a
  user's doc and a session's alike, its record naming each (METHOD's Docs
  always current).
