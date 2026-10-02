# R-840 mutation tables, read

Three tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/244` after both of the review's fix rounds, one
at a time, each run in the foreground and waited on with nothing else
touching the tree. Every null control killed 0 of the full suite, 12,202
collected against 12,202, every row's collected count equalled its subset's
baseline, every row's `head_verified` is true, no row was promoted, and after
each table `git status` showed the table's own two files and nothing else.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r840-a.md`, the walk and its scope | 9 | 9 | 0 |
| `r840-b.md`, the read, the write and the counts | 11 | 11 | 0 |
| `r840-c.md`, the store, the adapter, the seam and the judging stamp | 5 | 5 | 0 |

25 rows, the cap. No zero, so no composite was owed.

**Measured twice, and the second measurement is the one on file.** The
tables were first run after the first fix round, 25 of 25 killed. The second
fix round then replaced the write's compare and set with the store's locked
change and moved the walk into its own function, so four rows named text
that no longer existed and the rest named text that had moved. Those four
were rewritten for what replaced them, one row gave its place to the judging
stamp, and all three tables were run again on the final code. The count
stayed at 25. The first run's tables are in the branch's history.

Three tables and not one, so each finishes under the 600 second foreground
ceiling a Relay session has to stay inside. The full baseline took about two
minutes and each table finished in under five.

Subsets, named on every row and not derived. Tables a and b ran
`tests/test_label_artists.py`, 61 collected. Table c ran that file with
`tests/test_label_judge.py` for the store's rows, 137,
`tests/test_label_tidal_catalogue.py` and `tests/modules/test_labels.py` for
the adapter and the seam, 156 and 195, and `tests/test_label_judge.py` with
`tests/test_label_genre_gate.py` for the judging stamp, 214.

## The rows that die on one test

Eight rows are held by a single test each. Each is a real death, and each is
one deleted test away from a zero: `A3`, `A4`, `A5`, `A8`, `B1`, `B2`, `B10`
and `C5`.

## Four rows dropped at the cap, each logged in its row file

- `B12_a_refused_read_is_not_asked`, a maintainer facing count whose one
  assertion sits beside `B2`'s.
- `C6_a_release_the_client_returns_nothing_for`, a guard of U75 that this
  unit moved into the read two methods now share and did not change.
- `C7_the_sweep_files_a_name`, measured in the first run, 2 killed of 280,
  on code the second fix round did not touch. It gave its place to `C5`.
- `C8_a_payload_that_is_not_an_object_is_the_empty_one`, maintainer facing,
  driven by five parametrized cases in the suite.

## What the tables do not measure

- **The pacing.** No row removes the provider gate, because the verb does not
  attach it. `catalogue.resolve` does, for every caller, and R-705's own suite
  holds that. What this unit's suite holds is that the verb reads through
  `catalogue.resolve` and through nothing else.
- **The real client.** The adapter's rows run against a stand in. That the
  client fills an album's artist from the album's own payload, with no second
  request, was read in the installed client at 0.8.11 and not driven against
  the provider. The live run is where it is driven.
- **The write lock.** That the store hands the payload over inside its
  immediate transaction is read from the source. One connection in one
  process cannot interleave with itself, so no test here drives two writers
  through that window. What is driven is a writer acting during the provider
  read, on both verbs.
