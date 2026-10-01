# R-791 mutation tables, read

Three tables, the author's and not independent, measured by `scripts/mutate.py`
on `relay/235`. Every row ran against `tests/test_catalogue_searcher.py`,
`tests/test_tag_workers.py` and `tests/test_tagging_engine.py`. Every null
control killed 0 of the full suite, every sidecar reads valid and state
guarded, there was no collect drift, and every restore was verified against
`git show HEAD`.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r791-a.md`, the blocked answer and the decline in `searchers.py` | 14 | 14 | 0 |
| `r791-b.md`, the disposition, the artifact, the summary, the warnings | 11 | 10 | 1, C5 |
| `r791-c.md`, C5 again after the test it bought | 1 | 1 | 0 |

25 distinct rows and one re-measure, at the light cap. Nothing was dropped.

## C5, the one zero

`_unread_warnings` names a source as blocked on every search only when it was
asked at least once. Removing `asked and` killed nothing on the full suite in
`r791-b`, 11,122 collected. The surface is user facing and common: a sweep
where Beatport matched every file holds both fallbacks at zero asked, and the
mutant then warns that each one refused every one of 0 searches. The test
`test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked` was written
for it, and `r791-c` measured the same row again: killed, 1, collected 11,123.

## Measured with the leak watch on

The first attempt at `r791-a` stopped with a state leak in the full baseline:
126,372 entries became 126,382. They were analysis artifacts under
`jobs/analysis-artifacts/2026-10-01T10:34:47Z-c87e/`, a real `crate analyze
run` job over the download folder started outside this session against the
installed copy, its lock naming a live process. The solution entry on state
leak halts names this shape. The session did not redirect the watch, which
R-793 records as the wrong move unattended. It waited on the queue database,
read only, for that job to finish, then for the `crate analyze restamp` job
that followed it, `2026-10-01T11:40:50Z-229f`, and measured all three tables
once no installed `crate` process had run for ninety seconds. No table halted.
