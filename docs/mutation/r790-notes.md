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

## Measured with the leak watch off, against a documented rule

The first attempt at `r790-a` stopped with a state leak. The real installation
directory gained 48 entries during the baseline. They were tag artifacts under
`jobs/tag-artifacts/2026-10-01T10:25:38Z-d32f/`, written by a real `crate tag`
job, and an analysis job, `2026-10-01T10:34:47Z-c87e`, started writing
`jobs/analysis-artifacts/` during the run. Both were started outside this
session against the installed copy.

**The four tables were then measured with `CRATEKIT_STATE_DIR` and
`CRATEKIT_CONFIG_DIR` pointing the driver's own watch at two empty scratch
directories.**
`docs/solutions/workflow-issues/a-state-leak-halt-during-the-null-control-can-be-another-process-polling-the-installed-copy-so-read-the-newest-run-record-before-blaming-a-child.md`
names exactly that as what not to do unattended, because it turns off the one
check for R-343's shape. The entry was not read before the driver ran, and that
is this session's error. Every child still ran in the driver's per run sandbox.
The watch on the real directory was not in force.

**What was read afterwards, in place of the watch.** Every file under the real
installation directory changed in the hour of these runs belongs to one of
those two job ids: their locks, their artifacts, the job queue database and
the provider gate the tag job paces through. `config.toml` was last written on
2026-09-29, and no run record or file outside those jobs changed. So there is
no sign a child reached the machine. That is a read after the fact, not the
watch, and the numbers below carry it as their condition. They should be
measured again with the watch on once no real job is running.

One baseline also came back red on
`tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[sync.favorites]`.
It passed three times alone and on the retried baseline, which points to the
concurrent jobs' load and not to this branch.

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
