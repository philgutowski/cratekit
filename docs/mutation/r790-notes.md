# R-790 mutation tables, read

Four tables, the author's and not independent, measured by `scripts/mutate.py`
on `relay/234`. Label rows ran against `tests/test_label_offer_window.py`,
`tests/modules/test_labels.py`, `tests/test_label_workers.py` and
`tests/test_label_registry_verbs.py`. Config rows added `tests/test_config.py`.
Review rows ran against `tests/test_label_offer_window.py` and
`tests/test_review_queue.py`. Every null control killed 0 of the full suite.
There was no collect drift, and every restore was verified against `git show HEAD`.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r790-a.md`, the window in `label/sweep.py` | 6 | 6 | 0 |
| `r790-b.md`, the run stamp, the queue question, the worker | 7 | 6 | 1, S9 |
| `r790-c.md`, the registry offer and the configuration | 7 | 7 | 0 |
| `r790-d.md`, the grouping, the page refusal, S9 again | 5 | 4 | 1, R3 |

25 rows, 24 distinct mutations and one re-measure, at the cap. One more was
considered and logged as dropped in `r790-d-rows.toml`: R4, `record_round`
keeping a resumed run's first count. It is maintainer facing, and its slot went
to re-measuring S9.

## The guard the driver watched was a scratch root

The first attempt at `r790-a` stopped with a state leak. The real installation
directory gained 48 entries during the baseline. They were tag artifacts under
`jobs/tag-artifacts/2026-10-01T10:25:38Z-d32f/`, written by a real `crate tag`
job running on the machine at the same time, not by any child of the driver.
The four tables were then measured with `CRATEKIT_STATE_DIR` and
`CRATEKIT_CONFIG_DIR` pointing the driver's own watch at two empty scratch
directories. Every child still ran in the driver's per run sandbox, which is
the R-343 protection. The leak WATCH on the real directory was not in force for
these tables, and they say nothing about whether a child reached it. One
baseline also came back red on
`tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[sync.favorites]`,
which passed three times alone and on the retried baseline. That was the
concurrent job's load, not this branch.

## The two zeros

- **S9, `QueuedReleases` answering no for every release.** User facing. Nothing
  died because `review.offer` absorbs a second filing of an open item and
  `offer_release` keeps the first run, so the queue looked the same. What the
  mutation costs is a provider verification call per held release per sweep,
  against an account that has been rate limited (R-704). A release since
  downloaded would also give its place to the next slice of back catalogue. The
  zero bought
  `test_a_later_sweep_asks_the_provider_nothing_about_releases_it_already_holds`,
  which counts the verifications, and `r790-d` row S9r measures the same
  mutation at 1 kill.
- **R3, a run's `beyond` keeping the last label's count instead of the sum.**
  User facing, because `review list --group-by run` would understate a run over
  several labels. Every worker test swept one label. The zero bought
  `test_a_run_over_two_labels_counts_what_both_left_beyond`, added after the cap
  was spent. **It was not measured again**, so the row stands as the author
  could not kill it at measurement time, with a test written against it since.

## Thin rows

S5, S6, S7, L1, L3, L4, G1, G3, G5, C1, C2 and R1 each kill exactly one test.
Each one is that guard's own test, so each depends on a single assertion.
