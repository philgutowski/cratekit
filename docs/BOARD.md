# The board

Cratekit's work is tracked on GitHub, not in this repository.

**https://github.com/users/philgutowski/projects/2**

Issues live on `philgutowski/cratekit`. Milestones are the seven plan phases, A to G.

## What is on it

**The board is the BUILD. `docs/residual-findings.md` is the LEDGER.** Two
registers answering two questions, and they are not mirrors of each other.

| Kind | On the board | Why |
|---|---|---|
| Implementation units `U-N` | always | they are the work, and work is picked here |
| Attended items `A-N` | always | a chore needing a person at the machine is also work |
| Residual findings `R-N` | only past the board bar | a residual is a problem recorded rather than fixed, so it lives in the ledger and earns an issue only when it meets METHOD's board bar: a person using the shipped verbs pays for it |

**Do not backfill residuals.** Most have no issue and should not. Putting the
ledger on the board would claim you intend to do a hundred things you have decided
not to do, and would flood the project board's Ready column, because a non unit
issue with nothing waiting on it derives as Ready. A residual takes its number
only when `board.py residuals --land` runs on `main`, so its issue is filed
after that, never from a branch. `board.py audit` reports a title that no
longer matches its finding as a CONTRADICTION.

**No count is written here on purpose.** An earlier version of this section gave
one, as a table, and it was true for 97 minutes: it said eleven residual findings
on 2026-08-02 and the file passed a hundred while the table sat still, and every
session read the stale number for twelve days. A census in a document nothing
checks is a claim with no expiry. Ask the repository instead:

    gh issue list --repo philgutowski/cratekit --state all --limit 5000 \
      --json number,title --jq '.[].title' | cut -c1-3 | sort | uniq -c
    grep -c '^## R-' docs/residual-findings.md

**An issue number usually matches its unit number and is not guaranteed to.** U8
is issue #8 and U37 is issue #37, but U38 is issue #51, because #38 onward were
taken by residual and attended issues. Look it up before writing a closing
trailer rather than computing it.

Each unit issue carries that unit's full brief: goal, requirements,
dependencies, key files, approach, test scenarios, verification. The issue is
the brief, so a session picks up a unit without reading any plan document, and
an insufficient brief is fixed on the issue. New cards are filed in that form
by the `file-card` skill. `DJ_tools/docs/migration/00-SEAM-DECISIONS.md` is
authoritative over any brief.

## Status

- **Ready**, every dependency has landed, this can start now.
- **Blocked**, waiting on another unit. The issue body names which, by number.
- **In Progress**, on a branch.
- **In review**, held by the relay runner; like In Progress, a holder's status
  that is never derived, so a recomputation keeps it.
- **Attended**, needs Phillip at the machine and an agent must not drive it.
- **Done**, landed on `main`.

The **Unblocks** field is how many other units this one releases. Sorting the Ready
column by it is how you pick the highest-leverage next unit rather than the lowest
numbered one.

## The tool

`scripts/board.py` is how a session reads the queue and how the board is kept true.

| Command | What it does |
|---|---|
| `board.py next` | the ready queue, ranked by how much of the build each unit releases |
| `board.py show 11` | one issue's brief |
| `board.py start 11` | branch, mark In Progress, print the closing trailer |
| `board.py sync` | make the board match the repository, idempotent |
| `board.py audit` | report drift and contradictions, exit 1 or 2 |
| `board.py closing` | refuse a `Closes` trailer while a register still owes that unit |
| `board.py residuals` | list the residual files waiting for a number; `--land` numbers them on `main`, `--search` finds ledger headings |
| `board.py cloud` | the cloud lane's queue, read from the cards' comments over REST |
| `board.py local` | the attended cards only Phillip's Mac can do |

`next` ranks by **transitive** reach rather than direct dependents. A unit whose
one dependent is the gateway to a whole phase outranks a unit with three dead-end
dependents, and the direct count cannot tell those apart.

`start` refuses a blocked unit, a dirty tree, or a branch that is not `main`. A
guard that lets you start blocked work is a board nobody trusts.

## Keeping it honest

The board drifts the moment a merge lands and nothing moves, and a stale board is
worse than none because it is read as current. So the update is not a step anybody
performs.

**The chain.** End the merge commit with `Closes #11`. Pushing `main` closes the
issue. `.github/workflows/board.yml` fires on the close, rebuilds the graph, and
flips every unit that was waiting on 11 from blocked to ready. The only human act
in that chain is writing the trailer, which `board.py start` prints for you.

The workflow fires on every issue event, an edited body included, and also
runs weekly and on demand, because a scheduled run is what notices the
workflow itself has been failing.

**On the token.** `GITHUB_TOKEN` is repository-scoped and cannot reach a
user-owned project, so with it alone the workflow runs `--labels-only`: the
`ready` and `blocked` labels stay true and the cards do not move. That is the
right half to keep if only one can be kept, because the labels are what the
queue is derived from and the card is the view of it. With a `BOARD_TOKEN`
repository secret of `project` scope it moves the cards too, and its run
summary says which of the two it ran. Running `board.py sync` locally always does
both, because Phillip's own token carries that scope.

**The one input nothing else checks.** Every value the board derives comes from
issue closure state, so a close is the board's single unverified claim, and it
cascades: one wrong close moved four units from blocked to ready in under a
minute, correctly, off a false premise. Two registers already hold the
answer: `tests/_pending.py`, and a `planned_in` marker on a verb registry
entry. Each is the repository asserting, in an enforced file, that a named unit
has not finished. `audit` reads both and flags any unit whose issue is closed
while either still owes it a module.

Those are reported as **contradictions**, separately from drift, and `sync` will
not touch them. Drift is a derived value that fell out of date. A contradiction is
two sources of truth disagreeing, and repairing that automatically means picking
one to overwrite, which is how the wrong one wins silently. Exit 1 is drift, exit
2 is a contradiction.

**Derived values are not edited by hand.** `ready`, `blocked`, Status, and
Unblocks are all computed from issue closure state and the dependency graph. Do
not drag cards or toggle labels. Change the `**Depends on:**` line in an issue
body and let the sync recompute, or the board goes back to being a thing that has
to be remembered.

## Where the graph lives

In the issue bodies, and nowhere else. Each unit issue carries a
`**Depends on:** #18 (U18), #31 (U31)` line, and `board.py` parses it.

There is deliberately no committed copy. A second representation of one fact is
how the two come to disagree, which is the same argument this codebase makes about
duplicated resolvers and duplicated idempotency rules. The cost is that an issue
body which loses its line becomes invisible to the graph, so `audit` fails loudly
on a unit that does not parse rather than treating it as dependency-free. That
distinction is real: U1 genuinely has no dependencies and says so explicitly.

The board was first generated from the plan's unit index and `docs/residual-findings.md`.
If a unit's dependencies change during the build, change them in the issue body.
The plan stays the record of intent; the issues are what the tooling reads.
