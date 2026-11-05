# Cratekit

Acquisition and curation for rekordbox DJs. A slim core, toggleable feature
modules, and guarded library writes.

This file is the session contract, kept short because every session and every
agent loads it on every call (U196). **`docs/METHOD.md` is the operating
instruction and is what to read next**: the pipeline, the card sizes, the merge
bar, the mutation method, the driver rules, the merge constraints and the
do-not-touch list. `docs/METHOD-local.md` is the part only a session on
Phillip's Mac needs: the local board commands, attended cards and releases.
`RESTART-cratekit.md` is the verified current state, read by a local session;
each unit's own record is a file in `docs/restart/`. `docs/history/` is the
narrative of how the rules were arrived at, read for reasoning, never for
instruction.

`docs/solutions/` is the record of problems already solved, filed with YAML
frontmatter (`module`, `problem_type`, `tags`) so it is searched rather than
read: grep it by module before touching an area. `CONCEPTS.md` is the shared
vocabulary; grep it for a term that is unclear, never read it whole.

## How a session runs

**The cloud is where Cratekit is built**, decided by Phillip on 2026-10-27.
Of Phillip's two Claude projects, one turns his ideas and bugs into cards
with the `file-card` skill and keeps the decisions page, and the coordinator
of the other, the building project, keeps build threads going, each running
the `cloud-unit` skill on its card: plan, build, Fable's review to the merge
bar, the mutation table, the record, a pull request merged to `main` with the
closing trailer once CI is green. A session does the whole of a unit itself;
the compound engineering plugin is not used. **Only a card that cannot be
built without the machine is built locally**, set aside by the cloud with a
comment carrying the steps; `docs/METHOD-local.md` is how.

Every question for Phillip reaches the decisions page,
https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS, where he answers with a
tap; a build thread asks on its card only, and the other project copies the
question to the page and his answer back. Nobody is watching a session while it runs, so a question is a stop:
make the conservative call, record it as a residual, and keep going.

## The board is the queue

Work is picked from the board, https://github.com/users/philgutowski/projects/2,
never from a plan document or a conversation. Every implementation unit `U-N`
and every attended chore `A-N` is an issue, and **the issue is the brief**:
goal, requirements, dependencies, key files, approach, test scenarios,
verification. If the brief is insufficient, fix the issue rather than working
around it. An issue number does not always match its unit number (U38 is
issue #51), so look it up before writing a trailer.

**U29, #29, is attended and never a session's to take**, whatever a queue
says; METHOD's do-not-touch section says why.

`docs/residual-findings.md` is the LEDGER. A residual `R-N` is a real problem
recorded rather than fixed; a unit files it unnumbered in `docs/residuals/`,
it takes its number when it lands on `main`, and it earns an issue only when
it meets METHOD's board bar. **Do not backfill the rest.** The ledger is over
forty thousand lines: search it with `board.py residuals --search WORDS`.

The merge commit ends with the closing trailer, `Closes #N`, and pushing
`main` closes the issue; the board workflow then flips every unit waiting on it
from blocked to ready. Never hand-edit `ready` and `blocked` labels or drag
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

On a Linux cloud container the suite is read against the base's own failures
with `scripts/cloud_battery.py`. The suite is the merge gate, not the edit
loop: while building, run the test files for what you touched. An author's own
battery is not a review; every defect the adversarial reviews found here
passed a green suite written by its author, so after a green suite, hunt what
a green suite cannot see, as METHOD lists.

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
  to let it analyse, and to read what it shows. A cloud session, a job, a verb
  and a test never launch rekordbox or its background agent. Before opening it: no
  Cratekit job is running, and `crate doctor` reads both backup ages under five
  days. After quitting it: `rekordbox` and `rekordboxAgent` are both confirmed
  gone before any verb runs. The analysis visit after a landing follows the
  project's `rekordbox-visit` skill step by step (U173), and a whole sync pass,
  from the account's new music to filed and analysed, follows the project's
  `crate-sync` skill (U174).
- **A backup is needed only when the library is more than five days out of
  date, or when Phillip asks for one**, decided by Phillip on 2026-10-10,
  relaxing the one day rule of 2026-09-29. Below five days a session opens
  rekordbox and mints the acknowledgment without running `crate backup run`
  first; at or over five days, or with either age unknown, it runs the backup
  before anything else.
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
  so the session reads the ages, refuses unless both are under five days, and
  answers with the actor `session`. Since U138 the verb accepts that answer
  with no controlling terminal and itself refuses unless both ages are under
  five days; until the installed copy carries U138, run it under
  `script -q /dev/null` as before. Answer as `session` either way: any other
  actor takes the terminal rule, which checks no age. Since U184 it is one
  command, `crate session ack --as session`, with no gate and no run left
  waiting; until the installed copy carries U184, use the gate as before.
- **DJ_tools is read-only for code.** It is the live system until each workflow's
  replacement is proven. Its `docs/` are the exception.
- **Do not symlink `.venv` into a worktree.** The editable install names the
  checkout it was installed from, so a worktree would verify code it cannot see.
- **A pull request per unit, merged by the session that opened it once CI is
  green**, decided by U158, replacing the old no pull requests rule. Feature
  branch per unit, open a pull request against `main`, merge it through the
  API as `merge(uN): ...` ending with the closing trailer once every check on
  its head is green, delete the branch. Never a pull request that waits on a
  person, and never a closing keyword in its body. CI reads the card a merge
  will close off a `cloud/N-slug` head only; a local unit's pull request is
  judged on its range, and its close on the push to `main`. **A cloud session merges
  itself**, attended or not, authorized by Phillip on 2026-10-27 ("I
  authorize you to merge to main here in the cloud now and going forward").
  A cloud session cannot delete a remote branch, so "Automatically delete
  head branches" stays on and a merged pull request takes its branch with it;
  any other stale `cloud/` branch is listed for Phillip's next local session.
- **Other builders share the board**, decided by Phillip on 2026-11-04. Never
  take a card or touch a branch held on `grok/`. One Claude project builds
  and the other files cards and keeps the decisions page. METHOD's Sharing the
  board section has the rules, the limits and the definition of done.
- **No em dashes, en dashes, or double hyphens** in any prose, code comment,
  commit message, or issue body. Do not swap a dash for a colon; favor commas,
  and keep colons for a genuine list or definition.
- **Explanations are batched per phase.** A unit lands with its commit messages
  and its record. Phillip runs the explainer over a merged phase when he wants
  it. A session does not run it.
