---
title: A test that pins a total is a merge hotspot, because every card that adds a reason code edits the same assert lines
date: 2026-10-10
category: workflow-issues
module: tests/test_reserved_causes.py
problem_type: workflow_issue
component: testing_framework
severity: medium
applies_when:
  - "Two or more cards that each add a reason code or a kebab shaped literal to src are built in parallel from the same base"
  - "A lane branch is queued to land and the feeder lands another card first"
  - "A test pins a total count (distinct causes, non key literals, holders) rather than a count per module"
  - "A new shared register is being designed and the question is whether it is one file everyone edits or one file per unit"
tags: [test-pins, merge-conflict, reserved-causes, parallel-lanes, shared-hotspot, board-lanes, u124]
---

# A test that pins a total is a merge hotspot, because every card that adds a reason code edits the same assert lines

## Context

`tests/test_reserved_causes.py` guards the reserved-cause namespace by pinning counts. Four of its asserts pin whole-repository totals, written as tuples compared with `==`: the distinct causes beside those that are not reserved and the reserved set (`len(causes), len(causes - CAUSES), len(CAUSES)`, about line 5218 at the time of writing), the distinct kebab literals beside those that are not causes (about 6288), the named at-risk modules counted without own declarations, with them, and holding an integer (about 6441), and the literal holders beside those also holding an integer (about 7148). The last three carry a failure message that names the counts measured; the first is a bare tuple, so a failure there shows only what pytest prints for the comparison.

Any card that adds a reason code, or a kebab shaped literal that is not a cause, moves those totals. So every such card rewrites the same four tuples. Two cards built from the same base each rewrite them from the same starting numbers, and the second to land conflicts with the first in a file neither author was otherwise editing.

On 2026-10-10 this cost five separate merge rounds on the Cratekit board across four cards: #274 behind #276, #263 behind #264, #278 twice (once behind #276 and once more after the cards that landed since), and #277 behind #282. Each round was a builder merging main, then re-measuring the pins on the merged tree by hand, then reporting Ready again. U124 (#287) had landed in the small hours of that night, moving the RESTART paragraphs and the residual numbers into per unit files, which ended those two conflicts for good. The pins were what was left, and nothing in U124 touched them.

The trail it leaves is visible in the file itself: the comment above each pinned assert is a dated list of every re-pin (`Re-measured on the merge of main at ...`). As of this writing the file carries 285 re-pin or re-measure comment lines, and 30 commits touched it between 2026-10-09 and 2026-10-10 alone. That is the cost of a shared edit point, paid in the open.

## Guidance

**Lasting fix (built by U125): do not pin totals.** `tests/_pinned_reserved_populations.py` pins per module (kebab literals, named holders, literal holders) and one slug per line for the non-reserved cause set. Totals are derived from those pins. A new cause then adds a line to its own module's pin, or one slug line, and two cards that add causes in different modules touch different lines and merge cleanly. This is the same shape as U124: the shared register was one file every unit edited, and the fix was one file per unit (here, one pin entry per module).

**Interim fix (what to do if a total pin is reintroduced, or for an older branch still carrying one):**

1. Merge main into the branch with a merge commit, never a rebase. Expect the conflict in this file and only in this file when the cards are otherwise independent.
2. Keep both sides' pin comments. Resolve the conflict by keeping the comment blocks of both and one copy of the assert.
3. Do not take either side's numbers. Run the file alone, serially (`-n0`), read the counts the failing assert's message reports, write them in, and run again. Only the first failing assert is reported per run, so a merge that moved several pins takes several runs.
4. Add a dated comment line naming the merge and the counts, as the file already does, and say the counts were measured on the merged tree and not either side alone.

**Who resolves it.** The builder does, not the watcher. A watcher that resolves a conflict itself and then lands its own resolution is approving its own code, and the auto mode check refused exactly that on 2026-10-10 when the watcher tried it for #278. One landing made that way earlier the same night (for #263) stands, because its only watcher authored lines were the re-measured pin and its comment and it passed the full gate, but it was not repeated. So every pin conflict goes back to the builder, and a builder that moves only when nudged (the remote Grok agents) makes each round cost a wait as well as a merge.

## Why This Matters

The conflict is mechanical and the resolution is mechanical, which is why it looks harmless, but a round trip through a builder is neither. On a board with one lane landing per feeder cycle it turned a hands-off tail into several hours of nudged rounds, and at 285 comment lines the file's own history shows the cost accumulating on every card, not only on the unlucky ones.

It is also a place where the merge can be wrong silently. Taking one side's numbers, or adding the two sides' deltas, gives a count that was never measured on the merged tree. The neighbouring learning on pins that move by the right amount explains why that is not a measurement; the hotspot makes the temptation recur on every parallel pair.

## When to Apply

- Before adding a second card that adds reason codes to a lane already holding one: expect the pin conflict and plan the merge round, or sequence the two cards so one lands first.
- When designing any new guard that counts something repository wide: prefer a per module count or a derived total over a literal tuple of totals.
- When a landing hook refuses a branch with a conflict in this file and nothing else: send it back to the builder with the interim fix above, not to the watcher.

## Examples

Before, the shape every card edits (illustrative, the numbers change on every landing):

```python
assert (len(literals), len(literals - set(causes))) == (702, 493), (
    f"the kebab-literal population moved to {len(literals)} distinct with "
    f"{len(literals - set(causes))} that are not keys"
)
```

Two cards each add literals. Card A rewrites the tuple to its own total, card B rewrites it to its own, and whichever lands second conflicts on the tuple and on the comment block above it.

After (the shape the lasting fix would take): each module pins its own count, and the repository total is derived and asserted to equal the sum, so adding a cause in one module edits one module's line and no other card's.

## Related

- `docs/solutions/workflow-issues/a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md` is the closest neighbour: how to re-pin correctly (measure the merged tree). This learning is the cause of the repeated re-pinning.
- `docs/solutions/workflow-issues/a-new-kebab-literal-in-src-moves-the-reserved-cause-suite-and-a-file-write-belongs-inside-the-row-session.md` is the single card view of the same file.
- `docs/solutions/workflow-issues/renumbering-incoming-residuals-at-a-merge-moves-the-citations-too.md` is the earlier shared hotspot (the residual ledger and the restart file) that U124 (#287) ended with per unit files, the precedent for the fix here.
