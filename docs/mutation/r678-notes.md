# R-678 mutation tables, read

Three tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/196` in the foreground under the Relay session's
rule. Each row names its subset: the human mode tests beside the four verbs'
own fixtures, in `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`,
`tests/test_tag_workers.py` and `tests/test_intake_imported.py`, plus
`tests/test_render_payloads.py`. Null control 0 of 10118 on all three, no
collect drift, every restore verified against `git show HEAD`.

**`r678-a.md`**, 12 rows over `cli/render.py` at `8f83e49`: the two new cases
dropped from `render`, the job case's schema and identifier gates, the queued
state on the drive line, the intake verbs on the resolution, the succeeded
state and the nonzero count on the next command, the absent word, the proof's
verb gate, the run count from the verb's total, and the retired file's name.
11 killed, 1 zero.

**`r678-b.md`**, 4 rows over `cli/__init__.py` at `8f83e49`: the dispatcher
handing in no drive, the verb check that keeps `job show` and `job resume`
from naming a second driver, the broad catch that keeps a builder's raise from
becoming a traceback over a queued job, and the queued state gate on the
lookup. 3 killed, 1 zero.

**`r678-c.md`**, 1 row at `85f33cd`: A3 measured again after its test was
fixed. Killed, 1.

16 distinct mutations, 17 rows, under the cap of 25. Nothing was dropped.

## The two zeros

- **A3, the job case's schema gate, in `r678-a`.** User facing, so it was
  not left as a zero. The test written for it nested `job_id` under
  `summary`, where the empty identifier gate stopped it before the schema
  gate was asked, so the test pinned the wrong guard. The test now puts the
  identifier at the top of a `review_set` payload, where the job case reads
  it, and `r678-c` kills 1. No shipped verb puts a top level `job_id` on
  another surface today; the gate is what keeps one from growing a job line.
- **B4, the queued state gate on the drive lookup, in `r678-b`.** Maintainer
  facing, one line: it saves a store read for a job that is not queued, and
  the renderer's own queued check, A5, is what keeps the line off the screen.
