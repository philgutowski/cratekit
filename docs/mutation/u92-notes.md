# U92 mutation notes

The measured table is `u92-author.md` and its numbers as data are
`u92-author.json`. This file is what the table cannot carry: what it took to
get a valid batch, and which of its numbers came from a second measurement.

## Three batches were started and one is the table

| attempt | at | outcome |
| --- | --- | --- |
| 1 | `d802062` | REFUSED before any row ran. Baseline not green, 25 failing, 9255 collected. |
| 2 | `d802062` | INVALID. Baseline green, then the null control killed the same 25. |
| 3 | `d802062` | Valid. 9 rows, 8 killed, 1 zero. |
| 4 | `e847f70` | Valid. 9 rows, 9 killed, after the zero was closed. |
| 5 | `a6b107c` | Valid. 9 rows, 9 killed. **This is the table.** |

The 25 were the same 25 every time, all in `tests/test_rebuild.py`, and that
file was green run alone and green in five full suite runs by hand. It is the
starvation shape recorded under `docs/solutions/workflow-issues/`, which this
unit extended with a second incident, because that entry's tell is "hundreds of
failing tests" and 25 in one file does not look like it. Load average was 10 to
13 throughout, with memory fine, and the batch that succeeded ran at the highest
load of the three. Nothing in the driver, the environment or this unit's diff
was ever shown to be the cause, and nothing in this table rests on any number
measured during attempts 1 or 2.

## Attempts 4 and 5 exist because the tree moved under the table

Attempt 3 found the unit's one zero row, `G7_reason_reworded`. Rather than pair
it with a composite, the gap it names was closed: every assertion this unit
wrote read `vocals.REASON_AUDIO_TOO_LARGE` rather than the string it holds, so
renaming the slug was invisible to all of them. The slug is a surface, it is the
`vocal_reason` on the item artifact and the key of `by_vocal_reason` on the
envelope, and its two siblings were already pinned as literals. Attempt 4
re-measured with that pin in place and G7 killed 1.

Attempt 5 re-measured again because a test changed after attempt 4:
`--durations` named a new 11.9 second test, `missing_requirement` importing
`panns_inference` was timed as the whole of it, and it was stubbed out of the
half that did not need it. G9's count was unchanged at 5. The table is
attempt 5, so every row in it was measured against the tree that merges.

## What the table does not cover

- **The light pass.** `analysis/detect.py` decodes the same file first, under no
  cap, and that is R-583 rather than this unit's guard. There is nothing here to
  revert, so it is logged as a dropped row rather than measured.
- **A real oversize decode.** No file over the cap was ever handed to a real
  decoder, here or anywhere in the suite. The guard is measured; the hang it
  prevents is still the unmeasured claim R-408 made.
- **The author measured this.** METHOD's own figures say an independent table
  finds more than the author's, 17 against 10, 49 against 39, 83 against 49. Nine
  rows with nine deaths is what the author could kill, not a statement that
  nothing else is killable.
