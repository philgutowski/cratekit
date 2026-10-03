# R-835 mutation notes

The author's table, as METHOD sets it, over the guards the label folder build
and the label mark added and their first review round added. Twenty five
rows, the cap for a unit that writes to the account, run in two batches so
each fits the tool ceiling, `r835-a.md` and `r835-b.md`, and the zeros of
both measured again in `r835-c.md` after a test was written for each.

## Summary

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| a | 12 | 7 | F1, F7, F8, F13, L2 |
| b | 13 | 7 | S2, P3, M2, M4, M6, T3 |
| c, the zeros again | 10 | 10 | 0 |

24 of 25 killed after one round of tests for the zeros. F13 stays at zero
and is maintainer facing, below.

## The zeros, and what each needed

- **F1** and **L2**, a recorded folder the account no longer lists is not
  reused, in the plan and in the ledger's reserve. User facing: year
  playlists would be moved into a folder that is gone. No test deleted the
  folder; one now does, and both rows die on it.
- **F7**, only a provider failure reading a recorded year outside the folder
  is passed over as unreadable. User facing: a rejected session would be read
  as a deleted playlist. A test now raises a rejected session there.
- **F8**, an unrecorded year already carrying the mark prefix is matched by
  that name. User facing: it would be made a second time. A test now plants
  one.
- **S2**, the sync pass hands the sweep the ledger's year playlists. User
  facing: every year playlist would be swept as intake. The exclusion itself
  was tested and the hand off was not; a test now drives the hand off.
- **P3**, a track the provider will not play is never planned. User facing:
  it would be refused on every run. No fixture had one; one now does.
- **M2**, a year already marked is skipped as already marked. Covered by the
  retitled guard below it, which skips the same playlist under another
  reason, so the row was a wrong reason rather than a wrong rename. The
  second mark's test now asserts the reason.
- **M4**, the recheck before each rename. User facing. No test changed a
  title between the plan and the write; one now does.
- **M6**, the importable file is required. The batch read refuses a missing
  file on its own, so only an EMPTY file reached the gap. A test now passes
  an empty one.
- **T3**, an add answer that leaves a track out is read again. User facing:
  a track the playlist holds would be recorded refused. The fake answered
  truthfully; a test now has the client answer with nothing.

## The one left at zero

- **F13**, the label's name in the digest beside the folder action. Maintainer
  facing. The year playlists' titles are in the digest and carry the label's
  name, so the only plan it decides is a folder created while every year is
  reused under a recorded title, which no verb was driven to produce.

## Dropped below the cap

Five rows were written and ranked below the twenty five: the apply's skip of
an ambiguous or unreadable year and the move on a fresh create, both covered
by the plan's own decisions; the skip of a read for a year whose tracks are
all recorded, a saving and not a guard; the adapter's chunk size, pinned by
the chunked add test's exact counts; and the mark's retitled skip, which M2's
test now reaches.

Every zero row reads as "the author could not kill it" until batch c, and
batch c measured each at one death or more. The author ran the table, not an
independent verifier, which is the gap METHOD records.
