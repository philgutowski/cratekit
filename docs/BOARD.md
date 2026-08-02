# The board

Cratekit's work is tracked on GitHub, not in this repository.

**https://github.com/users/philgutowski/projects/2**

Issues live on `philgutowski/cratekit`. Milestones are the six plan phases.

## What is on it

| Kind | Range | Count | Source |
|---|---|---|---|
| Implementation units | U1 to U37 | 37 | the reengineering plan's unit index |
| Residual findings | R-1 to R-11 | 11 | `docs/residual-findings.md` |
| Attended items | A1, A2 | 2 | things that need a person at the machine |

**Issue numbers match unit numbers.** U8 is issue #8, U37 is issue #37. R-1 through
R-11 are #38 to #48, and A1 and A2 are #49 and #50.

Each unit issue carries that unit's full brief, copied from the plan: goal,
requirements, dependencies, key files, approach, test scenarios, verification. The
issue is the working spec, so a session can pick up a unit without reading the plan
document. The plan stays authoritative if the two ever disagree, and
`DJ_tools/docs/migration/00-SEAM-DECISIONS.md` is authoritative over the plan.

## Status

- **Ready**, every dependency has landed, this can start now.
- **Blocked**, waiting on another unit. The issue body names which, by number.
- **In Progress**, on a branch.
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
| `board.py audit` | report drift, exit 1 if the board is lying |

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

The workflow also runs weekly and on demand, because the event triggers cover
every ordinary change but not an issue body edited to change a dependency, and
because a scheduled run is what notices the workflow itself has been failing.

**On the token.** `GITHUB_TOKEN` is repository-scoped and cannot reach a
user-owned project, so in CI the workflow runs `--labels-only`: the `ready` and
`blocked` labels stay true and the cards do not move. That is the right half to
keep if only one can be kept, because the labels are what the queue is derived
from and the card is the view of it. Adding a `BOARD_TOKEN` repository secret with
`project` scope moves the cards too. Running `board.py sync` locally always does
both, because Phillip's own token carries that scope.

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
