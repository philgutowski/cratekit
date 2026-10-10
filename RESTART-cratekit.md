# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Each unit's own record is a file in `docs/restart/`**, named for what it
records, `u114.md` for U114, `r572.md` for R-572, `sitting35.md` for an
attended sitting. A unit writes its paragraph there and never here, so two
units built in parallel land in either order. This lists the ones added since
U124, newest first:

    git log --diff-filter=A --name-only --format= -- docs/restart

U124 moved every earlier record in one commit, so those list together after
them; the newest of those are `u118.md`, `u114.md` and `r925.md`.

This file keeps only the sections no unit owns, and `scripts/scan_repo.py`
refuses a unit's paragraph anywhere in it.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # read what it prints; an In review card is no longer drift

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | DONE on `relay/77` |
| | #78 | U60, the deletion pass | DONE on `relay/78`, no mutation table (R-329) |
| | #79 | U61, `crate sync all` composes the source increments | DONE on `relay/79`, no mutation table (R-329) |
| 9 | #38 | R-1, doctor checks every configured hook type | DONE on `relay/38`, 25 of 25 rows killing. Halted `partial_landing`, repaired by hand 2026-09-11 |
| | #40 | R-3, the scan refuses a tracked archive | DONE on `relay/40`, 15 rows committed and unrun (R-329) |
| | #41 | R-4, extras tied to their module and every toggle driven | DONE on `relay/41`, 6 rows committed and unrun (R-329) |
| | #42 | R-5, conformance 4 and 8 already drive behaviour, closed in place | DONE on `relay/42`, no guard changed, R-335 filed |
| | #43 | R-6, the conformance drives cover sixty two landed verbs, closed in place | DONE on `relay/43`, no guard changed, nothing filed |
| | #44 | R-7, doctor reports a trashing remote, closed in place with two rows fixed | DONE on `relay/44`, 6 rows committed and unrun (R-329), R-336 and R-337 filed |
| | #47 | R-10, one membership call per playlist and one folder lookup per folder | DONE on `relay/47`, 8 rows committed and unrun (R-329) |
| | #48 | R-11, the lead break helper and the watch driven through the database half | DONE on `relay/48`, 6 rows committed and unrun (R-329), two findings still open in the ledger |
| 10 | #25 | U25, vocal restamp and My Tags shells | DONE on `unit/u25-vocal-restamp-and-my-tags-shells` |
| 11 | | Phase F explanation, Phillip's and not a session's | |
| 12 | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**#38 is the one task in that run that did not verify itself.** It landed at
`d3fe927` with its whole pipeline complete, seven commits through the review
round, the mutation table, the record and the restart, and only the tracker
writes failed, so the record halted `partial_landing`. Repaired by hand on
2026-09-11: the issue was closed with a comment naming `d3fe927`, `relay/38` was
deleted, and `verify` then returned every check green. **Its record still reads
`halted` and always will**, because that manifest is finished and nothing will
start against it again. See the `verify` confirms section below before treating
that as a second repair.

**The board after this merge**: 61 units, 60 done, 1 ready, 0 blocked, once
main is pushed. The one ready is #29, attended and not a session's. METHOD
line 10 is done. Line 11 is Phillip's. Do not take #29.

**Phase E is complete with the U53 merge.** Line 7 is Phillip's, the explainer
over the range from `46d5a4c` to the U53 merge commit. A session does not run
it. Phase F's explainer is line 11, over the U59 merge and the residual
commits plus this one.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Each was taken as a relay task, which is Phillip placing it.

**#42, R-5 was a close**, read against the tree rather than assumed. Its
successor is R-335, which has no issue.

Residual issues carry the `residual` label. They are the queue after the units,
each done or closed back to the ledger. A2 is attended. **#81, R-322, is the
first of them to be worked and it is done**, which leaves the rest of that label
as the live list; run
`gh issue list --repo philgutowski/cratekit --label residual --state open` rather
than trusting a count written here. R-324 is closed on #80. R-327 has no
issue, which is the normal state for a residual: the ledger holds it until
somebody decides to act on it.

**Every unit in METHOD's serialized list is built except #29, and so
are #78 and #79.** What is left is Phillip's: the two explanations, #46 and
#39, and #29.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds. Line 10 is done. Line 12 is #29, attended.
2. `board.py next`. It names #29 first by reach. Do not take it. There is no
   unit left that a session may take.
3. Grep `docs/solutions/` for the module you are about to touch. A unit that
   opens a destructive write reads the barren list entry before it names an
   `analysis_roots`; a worker that moves files reads the rename intent entry
   before it binds. Read R-277 before touching `analyze.vocals`.

## The branches

| branch | state |
|---|---|
| `relay/48` | R-11, the branch this record is on; delete after the merge |
| `relay/47` | R-10, merged to `main`; delete if it still exists |
| `relay/44` | R-7, merged to `main`; delete if it still exists |
| `relay/43` | R-6, merged to `main`; delete if it still exists |
| `relay/42` | R-5, merged to `main`; delete if it still exists |
| `relay/41` | R-4, merged to `main`; delete if it still exists |
| `relay/40` | R-3, merged to `main`; delete if it still exists |
| `relay/38` | R-1, merged to `main`; delete if it still exists |
| `relay/79` | U61, merged to `main`; delete if it still exists |
| `relay/78` | U60, merged to `main`; delete if it still exists |
| `relay/81` | R-322, merged to `main`; delete if it still exists |
| `relay/77` | U59, merged to `main`; delete if it still exists |
| `fix/conformance-3-and-soft-delete-reader` | LANDED into `relay/77` by merge. Still in `.worktrees/conformance`, untouched, and now redundant. Deleting it and the worktree is Phillip's call, not a session's, because the merge is not pushed yet |

## When a relay run is cut off mid unit

It has happened three times, all three on a usage limit, and the shape is worth
recognising. The endings differ:

- **The runner had already merged.** Its own verify then refuses to call the
  task landed, `halt_class: partial_landing`, and the tracker issue stays open.
  So `main` carries a unit whose review, table and record never happened. That
  was #72.
- **The runner had not merged.** The task branch holds the work and the tree is
  left dirty, `halt_class: unclean_exit`, and the run stops there whatever
  `on_halt.continue_past_task_halt` says. That was #75.

The state lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`, `halt_class`,
`halt_message`, `findings`, and `transcript_path`. Read the task's last assistant
messages to learn which pipeline step it reached. Finish it on the task's own
branch, merge, and close the issue from there. **Do not re-run the unit from the
board as though nothing had landed.**

**`verify` needs the issue named as `#N`.** After a hand landing, `relay_cli.py
verify <manifest> <task>` reaches a landed verdict only when it can find the
link. It derives one from a default branch commit naming `#N` when the record
carries no `landing_ref`; when the record already carries one, as a
`partial_landing` record does, it instead wants a tracker COMMENT naming that
sha, and one comment is the whole repair. native-relay's own `docs/solutions/`
carries both halves.

**`verify` confirms, it does not promote.** `cmd_verify` computes the verdict,
prints the checks, and returns an exit code; it writes nothing to the record
(`cli.py:395`). A halted record stays halted, reading `partial_landing`, however
green the verdict is. Promotion happens at the NEXT run's startup, where
`startup_reverify` re-runs the full verdict on every halted record and promotes
the ones that now pass. So a repaired task whose manifest is finished keeps a
halted record forever, and that is cosmetic rather than a second repair to chase.
Measured on #38, 2026-09-11: every check green, `38: landed` printed, record
still `halted`.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** A residual is filed unnumbered in
  `docs/residuals/` and `board.py residuals --land` numbers it on main at
  landing (U124), so no branch is renumbered and main's never are.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why. **Never
  run `git checkout` on a file while a fix is uncommitted**: this session reverted
  one of its own review fixes that way and had to re-apply it, which is METHOD's
  driver rule arriving by hand instead of through a driver.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved, and U59 hit the sharper version: the soft delete
  reader pin went from two members to a DIFFERENT two, so the count did not move
  at all while both members did.
- **A guard that goes red at a merge is usually right and out of date.** Ask
  whether the RULE moved or the TREE did, and drive the answer. Weakening a stale
  guard to get green takes the rule with it. Four of them in U59, all four right.
- **The audit's exit code is a measurement, not a constant.** It exited 2 for
  R-324 until issue #25 was reopened and it exits 1 now for R-265, the `In
  review` card. Read what it printed rather than what a record predicted, and do
  not soften `contradictions()` either way. Softening it now fails tests, which
  is new: R-322 put seven of them behind that function.
- **A double belongs at the PRODUCER's boundary, not at the shape it produces.**
  Hand-build the payload the network returns and let the real derivation run over
  it. Hand-building the derived structure asserts what its author believes the
  producer makes. And making an input injectable moves the undriven path one
  frame UP, to the caller that supplies nothing, so write the row for the default
  branch too.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
  The worktree stays on that list even though its branch has landed, because
  removing it is a cleanup Phillip takes once the merge is pushed.
