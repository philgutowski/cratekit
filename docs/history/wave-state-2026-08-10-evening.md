# Wave state, 2026-08-10 evening: three units merged, and one defect class named

Continues `docs/wave-state-2026-08-10.md`. The method lives in `docs/METHOD.md`.
This file is history: what was measured and what was decided.

## What is on main

`63e11da`, pushed, clean. **4410 passed, 14 skipped.** `board.py audit` exit 0.

**U34, U24 and U38 all merged.** The wave went from one merged unit to four.
`scripts/mutate.py` merged with them.

## The defect class this session named, and it produced four blockers

**A rule verified on one surface while another surface carries the same
coupling.** Four instances, all measured:

1. **A guard reading a diff against `origin/main`.** On a pushed main those are
   the same commit, so the diff is empty. Four of U34's tests failed and a fifth
   passed over an empty loop. It would have left main red on the push. Found by
   attempting the merge, not by any verifier.
2. **The renumber certified against `src`, `tests` and `scripts`.** GitHub issue
   titles carry the number in their text, and nothing in the repository can see
   them. Phillip reversed the rule: **residual numbers are APPEND ONLY.**
3. **A citation sweep that covered code and never `docs/`.** Two numeric
   citations in U24's own verification report addressed a residual that had
   become U34's.
4. **The closing trailer scan reading the merge commit only.** GitHub scans every
   commit in a pushed range. U24's merge commit carried no trailer and its issue
   closed anyway, on two commits from far earlier in the branch that spell the
   keyword next to the number inside prose explaining why it must not be used.
   The scan is now over the range. **Never write a closing keyword next to an
   issue number, even to quote one. Backticks do not defuse it.**

## Merges

**U34.** Verified MERGE. Its blocking finding was downgraded on a producer hunt
done on the tree: four candidates driven, including two real 56 MB rekordbox
exports measured at 28189 paired tags with zero declared counts disagreeing
across 28250 nodes. None produces the input. Filed as a residual stating that
four candidates were driven and none produces it, which is not the claim that
nothing does. Round 11 fixed instance 1 above. Issue closed, board synced.

**U24, eleven rounds.** Its signature failure was a fix correct in isolation with
the hole open one level down, five times. Round 10 stamped the identity scheme at
write time; an independent pass measured that the drift had MOVED rather than
gone, with 16 of 19 candidate rule changes escaping the stamp. Round 11 closed
the class: the stamp digests the rules themselves and its membership is COMPUTED
by a walk from two roots rather than enumerated, so a helper factored out one
level down is reached because it is called. All 19 candidates now move it.

**U24 merged WITHOUT a closing trailer and its issue is deliberately OPEN.**
`tests/_pending.py` still owes it `cratekit.deletion.cli`, whose wall is R-13's
database fixture. Clearing that entry is a decision about who owns the fixture,
not a repair. The issue closed twice by accident on pushes and was reopened both
times.

**U38.** Verified MERGE. Its verifier built 21 live escape hatches against the
structural taint rule and **8 escaped** with a green suite. All are maintainer
facing, so none blocks under the floor. Four pinned tree populations were
re-pinned at merge because U24 and U34 landed modules; the two halves those pins
protect did not move.

## The cost work

Measured across five agents: a flat **2,400 tokens per tool call**. Context is
re-sent on every call, so the bill is tool calls times context size. Most calls
were an agent hand rolling a mutation driver.

`scripts/mutate.py` now takes rows as data and returns the table. Measured on
five real rows: **2 agent tool calls against 26**, and it runs a null control the
hand rolled version never did. Four METHOD rules also became four cost rules:
reachability before a blocking verdict, composites only for user facing zero
rows, hard row caps with dropped rows logged, and reading discipline.

Session cost was roughly 2.3M tokens across nine agent runs.

## What the next session does

1. **The hardware fixture harness**, approved and not built. One reusable set:
   a repeat count timing runner with a pass rate, a FAT image, and a real read
   only volume. It unblocks U12, U23 and U27, which have been deferred four
   sessions. Calibrate the timing fixture on a quiet machine.
2. **U16 is ready and merges after U24, which has now merged.**
3. `docs/mutation-rows.md` documents the hand rolled procedure and disagrees
   with METHOD. Retire it or point it at the driver.
4. `docs/METHOD.md` is 260 lines against the 80 it was written to be. It wants a
   trim pass.
