# U61 mutation table: NOT MEASURED

**Verdict.** The driver could not finish inside a ten minute foreground call, so
no row carries a death count, not even the author's. Twenty one rows are
committed in `docs/mutation/u61-rows.toml`. The gap is R-329, and this unit adds
the measurement R-329 was missing: where the time goes.

## Why, measured on 2026-09-10

- The full suite on the committed tree: 7251 passed and 1 skipped, in 349
  seconds, before the review fix's test and the digest layer test joined.
- **Attempt 1.** A `perl` wrapper sent SIGINT at 570 seconds. The traceback put
  the interruption inside the null control, `measure_batch` at
  `scripts/mutate.py:1002`. No sidecar, and `git status --porcelain` was empty.
- **Attempt 2** sampled `pgrep -lf pytest` every three seconds. Every pytest run
  the driver starts carries the same flags, so the stage is read off what the
  run's own children were doing:

  | seconds | what ran |
  |---|---|
  | 3 to 363 | the full baseline: ffmpeg fixtures, fake rclone backups, the disk image probe |
  | 363 to 366 | no pytest child: the subset baseline for `tests/test_sync_all.py`, under three seconds |
  | 366 to 570 | a second FULL run, the same ffmpeg, rclone and `job_worker.py` children |
  | 570 | SIGINT, with the second run still going |

- **Why the second run is full.** The control is measured with subset `None` and
  the label `"full suite"` at `scripts/mutate.py:1002`. It does not derive a
  subset from the first row's file, whatever R-329 and U60's notes said, so no
  row file can move it. The preflight is two full suite runs, about 720 seconds,
  before the first row.
- Both restores were checked: `git status --porcelain` and `git diff HEAD -- src`
  were empty after each call.

## What stands in, and it is not a table

The rows were written against named assertions in `tests/test_sync_all.py`, and
this is the author's expectation of which assertion each mutation reaches. None
of it is a measurement.

| rows | the test expected to kill |
|---|---|
| P1 | the slim pass, `playlists` reported as not built |
| P2, P3 | a source that refuses does not stop the other; the slim pass |
| P4 | the full pass, one intake run across both jobs |
| P5, P6 | the full pass, each job under its own key; no job under `sync.all` |
| G1, G2 | aborting queues no favourites job and names it declined |
| G3, H1 | the digest comparison between the two verbs; the full pass, whose hand off refuses a digestless decision |
| G4, F1 | the jobs run to done through `argv_for`, whose favourites resume is refused on a run another verb owns |
| G5 | the gate refusal has queued nothing and says what would be |
| N1, N2, N3, N4 | every source refused is a refusal; the slim no-op; the queue time refusal; the warning code |
| H4, H5 | the favourites job carries a gate run its own verb owns, actor and digest compared |
| H2 | the hand off case whose gate compares a digest and does not offer the option |
| H3 | the digest layer case, added after the rows were written, because no real gate offers the option without a digest |

The rows run unchanged with
`./.venv/bin/python scripts/mutate.py docs/mutation/u61-rows.toml` in any
session that can hold one command for about fifteen minutes.
