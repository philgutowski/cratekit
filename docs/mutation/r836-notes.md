# R-836 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's). This is the first
path that removes anything from the streaming account, so it gets the full 25
rows of a light pass, every one of them user facing.

Seven batches, 25 rows, the unit's light cap. Split so each run fits one
foreground wait: a five row batch measured 7 to 9 minutes, most of it the full
suite baseline every batch runs. Each batch names an explicit subset, the
prune, label playlists, outbound, adapter and outbound worker suites; batch a
also carried the export collection suite, dropped after for time. A zero is
promoted to the full suite either way. Every batch's null control was zero
and every row's restore was verified against `git show HEAD:`, 32 of 32.

- `r836-a`: the adapter's removal. A1 the ledger asked first, A3 the declared
  total, A4 the video count, A5 never retried, A6 the read back. 5 of 5 killed.
- `r836-b`: the ledger. L1 adopted anywhere wins, L2 export records vouch, L3
  an adopted year written not created, L4 a taken track leaves `added`, L5 an
  unreadable export date is older. 5 of 5 killed.
- `r836-c`: L6 the export date on the confirmed record, L7 no row for a track
  this product never wrote, F1 the build skips a pruned track. 3 of 3 killed.
- `r836-d`: P1 only created years, P2 the mismatch judged only with nothing
  gone, P3 a kept release keeps its track. 2 of 3 killed. **P2 zero**,
  promoted to the full suite and confirmed: the guard had a second copy, since
  the releases credited elsewhere are read only while `judged`, so the check
  in the leaving rule could never change an answer. The copy was removed as
  redundant in `628ee57`, with no behaviour change, and the guard that remains
  was measured as P2b.
- `r836-e`: P4 a track on the playlist twice, P5 the apply asks the ledger
  again, P2b the mismatch read only with nothing gone. 3 of 3 killed.
- `r836-f`: the export planner. P7 an unrowed playlist with an unmatched row,
  P8 a drifted match, P9 a row still in the playlist keeps its track. 3 of 3
  killed.
- `r836-g`: P11 absence is not evidence, C1 holds judged again, C3 a dangling
  row is a row. 3 of 3 killed.

Two guards had no test when the rows were written, L7 and C3, and each was
given one before its batch ran, in `6f39423`, so they measure tests rather
than read as zeros.

Dropped below the cap, logged in `r836-g-rows.toml`: A2, an adapter with no
configuration, which `open_account` never builds and a test drives directly;
A7, a removal answered False, a layer under A6's read back; P10, an older
export left alone in the planner, the family of L5; and P6, an account answer
that leaves out an asked track, dropped to make room for P2b, since the
adapter returns every asked identifier or raises.
