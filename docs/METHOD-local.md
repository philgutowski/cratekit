# Method, local and attended

The part of the method only a session on Phillip's Mac needs, moved out of
`CLAUDE.md` and `docs/METHOD.md` by U196 so a cloud session does not read it on
every call. Nothing here was dropped on the way; it is the same text. A cloud
session reads `docs/METHOD.md` and the `cloud-unit` skill, and comes here only
when a card is set aside for the machine or Phillip asks for a release.

## The local board commands

A restart prompt names a board item and nothing else, because the issue is the
brief. "Take #56" is a complete instruction once `CLAUDE.md` and METHOD are
read. A local session also reads `RESTART-cratekit.md` at orientation.

**Start every session here:**

    .venv/bin/python scripts/board.py next

That prints what is ready, ranked by how much of the remaining build each unit
releases, and names the one to take. **It will name #29 and you must not take
it.** U29 is attended. METHOD's do-not-touch section says why. A cloud session
reads `board.py cloud` instead, which never offers an attended card.

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

## The order

`board.py next` orders the queue. The list serialized here on 2026-09-07 is
spent, every line of it landed or was closed back to the ledger by 2026-09-18,
and its text is in git history. On 2026-09-18 a parity audit against DJ_tools
found the product could not finish an acquisition workflow, and the board
gained Phase G, units U67 onward, plus the residuals that meet the board bar.
`docs/ideation/2026-09-18-parity-to-feature-complete.md` is the design those
units were cut from, read for reasoning, never for instruction. The issue is
the brief.

**#29, U29, stays attended and is never a session's to take.** METHOD's do-not-touch section says why.

## Relay, retired 2026-10-27

Native Relay, the feeder, the watcher, the fable builder and `/board-up` ran
this file's pipeline on Phillip's machine from 2026-09-07 to 2026-10-27. They
are abandoned, decided by Phillip on 2026-10-27, and the cloud lane below
replaces them. Their manifests and run state live outside this repository and
are not read. What they taught stays in `docs/solutions/` and in the driver
rules above, and `docs/history/` has how they ran.

## Releases, decided by U159 on 2026-10-28

**People install tagged releases, never raw `main`.** A release is cut when
Phillip asks, in any session, by the `release` skill in the repository's
Claude Code skills directory: `scripts/release.py plan` lists the pull
requests (and, before U158, the merges) since the last `vX.Y.Z` tag and
proposes a semantic version bump with a reason for each; the session judges
it; `scripts/release.py cut --bump <kind>` refuses off a clean `main` equal
to `origin/main` and without a clean battery on that commit, then writes the
version into `pyproject.toml` and `src/cratekit/__init__.py` together, commits
`release: vX.Y.Z`, tags it, pushes `main` and the tag, and publishes the
GitHub release with its notes. The release commit is the one commit that
reaches `main` without a pull request, because it carries nothing but the
version. `crate doctor`'s `install.release` check tells an installed copy
when a newer release exists and prints the pipx command that upgrades it,
keeping its extras. No package index, no automatic upgrade, no cadence.
**The cut is the Mac's**: a cloud session's proxy refuses tag pushes and the
releases API, so a cloud session plans and judges the bump and hands the cut
to an attended card, which runs it with `--mac-battery`.

## Local attended work, decided 2026-10-28

**Work only Phillip's Mac can do is an attended card**, titled `A<N>:` and
labelled `attended`, so the cloud never offers it. `board.py local` lists
them, ready first, and a local Claude Code session shows that list when it
starts. A cloud worker files one card per live check its landing owes, rather
than leaving it in a comment.

**How a local session takes one without colliding with the cloud**, which
writes `main` at any hour:

1. Start from a fresh `main`: `git checkout main && git pull --ff-only`.
2. **A run and its record** (most attended cards): do the run, write the
   record (`docs/cutover.md` or the card's own file), commit on `main`, then
   `git pull` (a merge, never a rebase or a force) and push. Records are
   append only and per sitting, so a merge of them is clean.
3. **A run that shows code must change:** do not fix it locally. File a card
   with the `file-card` skill, carrying what the run showed, and let the cloud
   build it. Only a card that cannot be built without the machine is built
   locally, on a branch from `board.py start N` and merged after the battery,
   between cloud landings: check `board.py cloud` shows no held card touching
   the same files, merge `origin/main` in again just before the merge, and
   run the battery once more if it moved.
4. Close the card with a comment naming the record's commit.

