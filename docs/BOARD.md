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

## Keeping it honest

The board drifts the moment a merge lands and nothing moves, and a stale board is
worse than none because it is read as current. So, in the same pass as the merge:

1. Close the unit's issue.
2. Flip every unit it unblocks from Blocked to Ready, and remove the `blocked`
   label. The issue body lists them under **Unblocks**.
3. If the unit closed a residual finding, close that issue too.
4. Update `docs/HANDOFF.md`, which stays the narrative state and is what a
   memoryless session reads first.

The dependency graph on the board was derived from the plan's unit index table. If
a unit's dependencies change during the build, change them in the plan and on the
board, or the Ready column starts lying.

## Rebuilding it

The board was generated from two files: the plan's unit index and unit sections,
and `docs/residual-findings.md`. Nothing about it is hand maintained except status.
If it needs regenerating, those two files are the source.
