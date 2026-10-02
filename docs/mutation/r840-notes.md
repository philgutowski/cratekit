# R-840 mutation tables, read

Three tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/244` after the review's fix round, one at a
time, each run in the foreground and waited on with nothing else touching the
tree. Every null control killed 0 of the full suite, 12,196 collected against
12,196, every row's collected count equalled its subset's baseline, every
row's `head_verified` is true, no row was promoted, and after each table
`git status` showed the table's own two files and nothing else.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r840-a.md`, the walk and its scope | 9 | 9 | 0 |
| `r840-b.md`, the read and the write | 11 | 11 | 0 |
| `r840-c.md`, the store, the adapter, the seam and the sweep | 5 | 5 | 0 |

25 rows, the cap, one pass. No zero, so no composite was owed.

Three tables and not one, so each finishes under the 600 second foreground
ceiling a Relay session has to stay inside. The full baseline took about two
minutes on this run and each table finished in under five.

Subsets, named on every row and not derived. Tables a and b ran
`tests/test_label_artists.py`, 56 collected. Table c ran that file with
`tests/test_label_judge.py` for the store's rows, 131, and
`tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py` and
`tests/test_label_workers.py` for the adapter, the seam and the sweep, 156
to 280.

## The rows that die on one test

Ten rows are held by a single test each. Each is a real death, and each is
one deleted test away from a zero: `A3`, `A4`, `A5`, `A8`, `B1`, `B2`, `B5`,
`B6`, `B10` and `C2`.

## Two rows dropped at the cap, both logged in their row files

- `B12_a_refused_read_is_not_asked`, a maintainer facing count whose one
  assertion sits beside `B2`'s.
- `C6_a_release_the_client_returns_nothing_for`, a guard of U75 that this
  unit moved into the read two methods now share and did not change.

## What the tables do not measure

- **The pacing.** No row removes the provider gate, because the verb does not
  attach it. `catalogue.resolve` does, for every caller, and R-705's own suite
  holds that. What this unit's suite holds is that the verb reads through
  `catalogue.resolve` and through nothing else.
- **The real client.** The adapter's rows run against a stand in. That the
  client fills an album's artist from the album's own payload, with no second
  request, was read in the installed client at 0.8.11 and not driven against
  the provider. The live run is where it is driven.
