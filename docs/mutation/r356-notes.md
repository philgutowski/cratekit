# Mutation notes: R-356, several releases under one ISRC

Two batches, `r356-a` and `r356-b`, **25 rows, at the cap of 25**, the author's
own and not an independent table. **25 killed, no zeros.** Null control zero in
each batch, of 9114 collected, and every row's restore verified against
`git show HEAD:`. Both measured on `relay/158` at `fedfef3`, after the code
review's fixes, so every published row is measured on one tree.

Both batches ran in the FOREGROUND, which is how a Relay session runs this
driver: `docs/METHOD.md` prefers a tracked background job, and a session that
cannot wait on one across turns takes the batch split instead. Batch a took 2
minutes 51 and batch b 5 minutes 42, each under the harness tool ceiling. The
split is for that ceiling alone. Batch b is the slower one because three of its
rows mutate a verb's shell, whose derived subset is the whole suite.

## What the rows cover

Batch a, 14 rows, all on `modules/outbound/tidal_account.py`: each of the two
choosing rules loosened from "exactly one" to "any", the hearts asked of every
track rather than the agreeing ones, a withdrawn track let back in, an
unreadable track no longer stopping rule one, the version and the artist each
dropped from agreement, each of the artist rule's two conditions removed alone,
each side's second title reading dropped alone, the joiner words emptied, and
the reason neither stored nor cleared.

Batch b, 11 rows: the naming head left on the release title, the template's
marker rule dropped and its empty marker guard dropped, the artist left off a
heart candidate, each engine handing on the wrong title and dropping the reason,
the export item report dropping the reason, the export envelope listing plain
unmatched rows, and the sweep's envelope dropping its reasons.

## No zero is not a claim of coverage

METHOD measures the author's table against independent ones at 10 of 17, 39 of
49 and 49 of 83, so "the author could not find a guard that kills nothing" is
what this says and all it says.

## Dropped at the cap, with why each ranked below it

- `bool(first) and` in `_artist_agrees`. Unreachable: `match.read_row` refuses a
  provider row with no artist before this is asked, so the row would have
  predicted its own zero on a maintainer surface.
- `_row_of` returning a row for half a name. The mutation raises rather than
  misbehaves, so it measures the reader's refusal and not this unit's guard.
- The favourites worker leaving the names off a reason. The envelope assertion
  that kills B11 reads the same sentence, so the row would be B11 again.
- `tracks.pop("", None)`, a track with no identifier. U63's guard, unchanged by
  this unit and outside the round's own diff.
