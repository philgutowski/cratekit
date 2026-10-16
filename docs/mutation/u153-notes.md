# U153 mutation table, read

The author's table, not independent, measured by `scripts/mutate.py` on
`unit/u153-...` at `5b399b2a`, twenty three distinct guards in one pass.
Baseline green at 14,102 collected, null control 0 of 14,102, no collect
drift, every restore verified against `git show HEAD`. Subsets were the unit's
own suites: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`
and `tests/test_favorites_backfill.py` for the engine, and
`tests/test_intake_land_hearts_native.py` with
`tests/test_intake_land_owned_hearts_native.py` for the landing.

**23 guards, 18 killed in the run, 5 zeros. One zero (L2) is armed by a test
added after the run and now kills; the other four are composite-held or a
subsumed maintainer branch.** So the standing position is 19 killed, 4 zeros
each accounted for below.

| id | guard | status | deaths |
|---|---|---|---|
| C1 | `is_uncoloured` reads the core writer's empties | killed | 3 |
| C2 | `sort_rows` dedup on seen | killed | 1 |
| C3 | `sort_rows` skips a row the handle cannot find | killed | 1 |
| C4 | `sort_rows` uncoloured vs held branch | killed | 10 |
| C5 | `find_row` returns a pending-insert row first | zero | 0 |
| C6 | `write_pink` re-checks fill only | killed | 2 |
| C7 | `write_pink` reports only a real write | killed | 5 |
| P1 | `plan_placements` marks a placement for colour | killed | 11 |
| P2 | `to_colour` returns nothing with no Pink row | zero | 0 |
| P3 | `PlacementPlan.writes` counts a colour-only plan | killed | 4 |
| P4 | identity digests the Pink row | killed | 1 |
| P5 | recolour dedup against the hearts | killed | 3 |
| P6 | `place` colours only with a Pink id | killed | 2 |
| B1 | backfill `_read_back` checks each coloured row reads Pink | killed | 21 |
| B2 | backfill records a colour-only commit | killed | 1 |
| B3 | `_member_order` tolerates a non-numeric id | killed | 1 |
| N1 | `_restamp` coerces the minted ID to text | killed | 10 |
| N2 | landing reads colour only with a Pink row | zero | 0 |
| N3 | landing colours the owned hearts | killed | 1 |
| N4 | landing records a colour count | zero | 0 |
| L1 | landing gate counts owned hearts in the Pink total | killed | 1 |
| L2 | landing emits the held note | zero → killed | 0 → 1 |
| L3 | landing emits the missing-Pink note | killed | 1 |

**The four standing zeros, each accounted for:**

- **C5, a guard covered by another guard.** `find_row` returns a row the
  session holds pending-insert before querying, so a heart made this commit is
  coloured on the one instance. Disabling it kills nothing because `_restamp`
  (N1, 10 deaths) coerces the minted ID to text, so the autoflush that
  `get_content` triggers finds the same new row and colours it. The explicit
  scan is the intended path and the autoflush is the fallback; N1 is the
  composite that shows the capability is held. Kept as the clearer path.

- **P2 and N2, the no-Pink short-circuits, held by P6.** Each avoids handing a
  caller rows to colour when the colour table has no live Pink row, but the
  real protection is `place`'s `if pink and to_colour` (P6, 2 deaths): with no
  Pink id nothing is coloured however the plan reads. Removing P2 or N2 only
  makes a pointless `sort_rows(db, "", ...)` call whose result `place`
  discards. Kept as cheap defence, the behaviour pinned by P6.

- **N4, a maintainer branch subsumed by `hearts`.** The landing records the
  favourites commit on `hearts > 0 or coloured > 0`. A landing only colours a
  row it also adds a membership for, a new file into All Favorites or an owned
  heart joining it, so `coloured > 0` implies `added > 0` and the `coloured`
  disjunct never changes the record. It is unreachable today and kept as
  defence against a future colour-only landing path; the backfill's own
  colour-only record branch (B2) is reachable and killed.

- **L2 was a test gap, now killed.** The held note in `favorites_notes` fires
  only on the native-apply path, which needs a file in the batch beside the
  held owned heart; the existing held test took the owned-only path and its
  own warning block. `test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  stages a file beside a pre-coloured owned heart and asserts the note. It was
  confirmed to fail with the branch disabled and pass with it restored.
