# Wave state, 2026-08-10: the bar changed, and three units moved

Continues `docs/wave-state-2026-08-09.md`. **The method now lives in
`docs/METHOD.md`, not here.** This file is history: what was measured and what
was decided. Read METHOD.md to find out how to work.

This file is deliberately short. The previous two snapshots run to 1320 lines
between them and every agent was reading both before doing any work. That is
the cost this session removed.

## What is on main

`24b58d1`, pushed, clean. 3422 passed, 17 skipped. `board.py audit` exit 0.
**Still no unit merged since U32.** One docs commit this session, the method
file.

## Three decisions, all Phillip's, all taken this session

**1. The merge bar has a severity floor, and a round cap behind it.**

A finding is BLOCKING only if it was driven end to end AND has a named user
facing cost. Everything else is a residual. Behind that, a hard cap of two more
fix rounds per unit counted from now, after which the unit merges and open
findings become residuals.

The reason is measured rather than felt. The previous bar, that the verifier
found nothing, is not a reachable state: a mutation table over a suite this size
always finds a zero death row, because that is a property of large test suites
and not of any branch. Twenty consecutive blocking verdicts is the measurement.
The severity curve supports it too: of U34's four round 9 findings only B2 had a
user facing cost, and of U38's four only B2 did. The other six were docstrings
that overclaim and assertions naming the wrong number.

This reverses the 2026-08-09 decision, and it reverses it on evidence gathered
since.

**2. Residuals renumber sequentially at each merge.** Open since 2026-08-04 and
blocked on the fear that a renumber silently repoints a source citation, which
happened once on the U36 merge. Measured this session across all eight branches
and main: **zero numeric `R-NN` citations remain in `src`, `tests` or
`scripts`**. Every citation is by title. The renumber is mechanical, and
`grep "^## R-" ... | sort | uniq -d` verifies it.

The collision figure on record was understated. It read six numbers. Measured
today the union is nine, R-14 through R-17 and R-19 through R-23, and the worst
single branch is U34 with seven.

**3. U24 reconstructs history from a recorded scheme version, not by
recomputation.** See the U24 section. And stores written by unmerged branch tips
do NOT count as history the shipped code must reconstruct, since nothing has
shipped.

## State

| unit | tip | round | state |
|---|---|---|---|
| u12 | `fc73b82` | 6 | never verified. Untouched. Needs a 25 run timing measurement. |
| u16 | `3262bc8` | 7 | never verified. Untouched. Merges AFTER U24. |
| u23 | `6f8db39` | 8 | never verified. Untouched. Needs a mounted FAT image. |
| u24 | `b5a4e86` | 9 | **verified BLOCKING, 4 findings.** Needs round 10. |
| u27 | `44ced7e` | 8 | never verified. Untouched. Needs a read only volume image. |
| u34 | `1a7cdf7` | 10 | **fixed, UNVERIFIED.** 3522 passed, 15 skipped, 3537 collected. |
| u38 | `c2fda57` | 8 | **fixed, UNVERIFIED.** 3399 passed, 15 skipped, 3414 collected. |
| conformance | `897ef12` | parked | its `write/metadata.py:195` defect is still live on main. |

Every branch is clean and pushed. U34 and U38 are behind main by 46 and 45
commits respectively, which is why U38's suite is smaller than main's.

## U24 round 9, BLOCKING with 4

**Round 9 froze the composer and did not freeze what the composer calls.** The
fourth consecutive instance of this branch's signature failure, a fix correct in
isolation with the hole still open one level down.

**B1, and it is the generalizable one.** The two frozen historical composers at
`tombstone.py:678` and `:695` call the LIVE `_already_carries`, which changed at
`1bd0399`. So the frozen functions reconstruct the pre `1bd0399` era using the
post `1bd0399` rule. Driven: monkeypatching `_is_a_credit` moves the
reconstruction, and the literal pinning that was supposed to make drift go red
kills 5 tests, **none of them a history test**.

**Generalise it: freezing one node of a call tree does not freeze the
reconstruction. Any helper below it can drift.** That is why the fix is to stop
recomputing history at all.

**B2.** The empty tuple, round 8's F1 verbatim, is still reachable on an
ordinary rekordbox row (`Strobe Extended Mix` with Subtitle `Extended Mix`),
through a live helper instead of the live composer.

**B3.** Seven distinct composition rules have written a store on this branch,
not the four assumed. Three of the seven are offered by nothing. Under decision
3 the pre merge eras fall away, but `1bd0399` and `3e56753` sit inside the
window round 9 explicitly claims, so that part stands.

**B4, residual under the floor except one item.** 11 of 38 rows kill zero over 9
guards; the author reported none. The exception worth carrying:
`stores.py:335` `except Exception: return False` also kills zero when flipped to
`return True`, and `True` means an unidentifiable row reads as "already
recorded", retiring a confirmed removal for a file someone merely renamed. Pre
existing since `b4540ee`. Field reachability UNMEASURED.

**What round 9 got right, measured.** All 11 pinned literals are correct against
composers rebuilt at their own commits. F2 and F3 are genuinely closed. All 8 of
the author's rows reproduce. The table was incomplete, not wrong.

## U34 round 10

B2 fixed at the classification rather than the site: `rbxml.node_kind()` is now
a total three valued function and `read_export` refuses before a `LibraryView`
exists, so the view type cannot describe a tree whose kinds were a question.
Both declared values are recognised positively.

**A second user facing cost the round 9 verifier did not name, measured here:**
with every node unreadable the duplicate audit still reports its one group with
every placement on both members empty.

30 rows, 4 zero rows, every one paired with a composite. Collected 3537 on all
30 rows and both baselines. 14 tests added, all 14 killed by at least one revert.

**Found, measured and deliberately NOT fixed:** `rbxml._tree_node` and
`trees._tree_folders` filter positively for `FOLDER_TYPE`, so an unreadable root
folder turns a refusal to infer an ambiguous tree into a successful inference.
Write path, other units' surfaces, filed as a residual with reproduction.

## U38 round 8

B3 replaced the fingerprint assertions with three things, none of which knows a
marker: a property that a comment cannot survive a round trip through the syntax
tree, a structural taint rule that permits raw source text to reach nothing but
`ast.parse`, and an exact membership import whitelist.

**The measurement that matters:** a fresh hatch with a guessed marker kills 2,
with an unguessed marker kills 1, and with the structural rule relaxed kills
**0**. Only the structural rule catches a hatch nobody predicted the spelling of.

162 rows, 15 zero rows, all paired. Sixteen zero rows were found on the first
sweep and **eleven were closed by fixtures**, which is the right response to a
zero row and the first time this wave has done it at scale.

R-20's completeness claim is withdrawn as an instrument that cannot fail rather
than restated more carefully.

## Three process notes

**The git in a driver hazard reached a third instance, by hand this time.**
U34's agent ran `git checkout-index -f` to restore a file mid probe and it
discarded uncommitted test edits. Recovered whole from a scratch snapshot taken
seconds earlier. The rule is in METHOD.md and it needs to cover hands, not only
drivers.

**Five of U38's seven round 7 residuals are unrecoverable.** Only R2 and R3 were
recorded by content in the 2026-08-09 file; the verification report itself is
gone with its session. This is the second time this wave has lost findings to a
transcript. A verdict summary is not a substitute for the report.

**Per unit scratch directories worked.** Three concurrent agents, zero
collisions, first clean run since the failure was named.

## What the next session does

1. **U24 round 10.** Record the identity scheme version in the store at write
   time so history reconstruction is a lookup and not a recomputation. This ends
   the drift class rather than closing its fourth spelling. Pre merge eras are
   out of scope. Needs a migration path for rows already written without a stamp.
2. **Verify U34 round 10 and U38 round 8, light pass**, scoped per METHOD.md.
   Both are author written and unverified, and an author's table is a draft.
3. Apply the severity floor when reading those verdicts. On the evidence so far
   both units are close to merging.
4. U12, U23 and U27 still need hardware fixtures. Buying them once, as a reusable
   harness, is now cheaper than deferring them a fourth session.
