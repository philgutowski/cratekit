---
title: "A slow job blamed on the pool's gates never reached the pool, its declared worker cost was thirty times low, and half its time was one filter"
date: 2026-11-10
category: workflow-issues
module: "src/cratekit/analysis/cli.py, src/cratekit/analysis/light.py, src/cratekit/analysis/separation.py, src/cratekit/analysis/warm.py, src/cratekit/core/pool.py"
problem_type: workflow_issue
component: analysis
severity: high
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A brief explains a slow run by a pool's gate, ceiling or worker count before anyone has checked the run uses the pool"
  - "A module declares what its worker costs and no run has ever been planned at that figure"
  - "A stage built on librosa.effects.harmonic, hpss or scipy.ndimage.median_filter is the hot one"
  - "A queued verb is about to be made parallel"
  - "A process pool's workers are about to outlive a foreground command for the first time"
symptoms:
  - "A job runs in one process on a machine with eleven cores, and the swap gate is named as the reason"
  - "A worker cost constant reads 64 megabytes over a function that holds two gigabytes"
  - "RuntimeWarning: WRITEBACKIFCOPY detected in clearing of array, out of scipy's rank filter"
  - "librosa.effects.harmonic returns numbers on one call and not a number on the next, for a clip under a third of a second"
  - "Ctrl-C on a pooled run fails the item in hand as an internal error"
  - "Worker processes stay alive after their parent is killed"
  - "Segmentation fault in a numba kernel on a fresh install, and on every run after it until the cache is deleted"
related_components:
  - job_engine
  - pool
tags:
  - u241
  - analysis
  - pool
  - process-pool
  - spawn
  - median-filter
  - numba
  - cold-cache
  - librosa
  - scipy
  - memory
  - cause-not-where-it-looked
---

# A slow job blamed on the pool's gates never reached the pool

## What looked true

`analyze run` took forty seconds a track, in one process, on an eleven core
machine sitting on 11.8 GB of swap. `core/pool.py` refuses a pool at 1 GB of
swap, and its default ceiling is two. So the card read: the swap gate dropped
the pool to one worker, the ceiling would have held it to two anyway, raise
the ceiling from the cores at the light pass's "measured 64 MB" a worker.

## What is true

Four things, each found by driving rather than reading the brief.

**The job never called the pool.** A queued verb's worker is
`handle(job, item, cfg)`, one item at a time, and `handle_run` called
`light.analyse` and `vocals.analyse` directly, in the driver. `light.run` and
`run_batch`, the functions that plan a pool, had no caller outside the tests.
`git grep -n 'light.run\|run_batch' -- src` showed it in a minute. The run was
serial on every machine, whatever its swap. METHOD already says the first
caller of an engine owns its unreviewed failure paths; the corollary is that a
planner with no production caller has no measured behaviour at all.

**The declared cost had never been exercised, so nothing had ever disagreed
with it.** `LIGHT_WORKER_BYTES` was 64 MB, "librosa-scale, tens of megabytes".
Measured in a fresh process per track, one head held 374 MB for 45 seconds of
audio and 2.0 GB for eleven minutes: the transform, its magnitude, its phase,
two medians, two masks and two products all alive at once. A ceiling of nine
from the cores at 64 MB a worker would have planned nine two gigabyte workers
on an 18 GB machine, the exact kill the pool was written to prevent, through
the pool's own arithmetic. A cost is a measurement or it is a guess, and the
only way to know which is to measure it: `scripts/analyze_stages.py memory`.

**Half the time was two median filters, and the same medians are ten times
cheaper.** `librosa.effects.harmonic` asks scipy for a two dimensional rank
filter over the whole spectrogram, twice. Scipy's one dimensional filter keeps
a running order over the window; the two dimensional one sorts each window
afresh. A median of an odd window is one of its own elements, so both return
the same bits. Filtering one contiguous line at a time measured 0.25 s against
2.63 s along time, arrays equal. Three traps on the way:

- librosa's transform is column ordered, so a frequency bin's run over time is
  a STRIDED line. Hand a strided line to the one dimensional filter as its
  output and numpy lends it a temporary and writes back as the temporary is
  cleared, with a `WRITEBACKIFCOPY` warning it says it will stop honouring.
  Copy a block of rows out, filter contiguous lines, copy back.
- scipy's rank filter is not reliable on a line shorter than half the window.
  For a two element line under a window of 31 its answer changed with the
  array's memory layout and from call to call, so `librosa.effects.harmonic`
  itself is not deterministic on a clip of two or three frames. Equality with
  librosa is undefined there. Take those lines by the definition, in numpy.
- "equal" has to be `array_equal`, with `equal_nan=True`, on signals holding
  silence and repeated values. Random noise has no ties and proves less.

**A pool behind a foreground command needs two rules `map_workers` never
needed.** Ctrl-C reaches every process in the foreground group, so a spawned
worker with the default handler dies mid item, the executor breaks, and the
item in hand fails as an internal error where the person asked for a stop. And
a spawned worker holds its own call queue's write end, so a parent killed
outright never closes it and the worker waits for ever with everything it
loaded. Workers ignore the interrupt, since the driver owns where a stop
lands, and watch the parent's sentinel and leave with it. Both were driven
with the rule removed first: the orphan lingered and the interrupt escaped.

**And the first code to start two librosa processes together owns numba's
cache.** The author's suite was green and every pooled run on the author's
machine was clean, because numba's on disk cache had been filled by the first
serial measurement. The review emptied it and ran the real verb: five runs
in seven ended in a segmentation fault inside a compiled kernel
(`librosa/core/pitch.py`, `_parabolic_interpolation`), first in a worker and
then in the driver, which had fallen back to the same call; and the cache
was left damaged, so every later analysis on that world crashed until its
cache files were deleted by hand. One process at a time on the same cold
cache: six clean in six. Two processes compiling into one numba cache is not
safe, whatever its index file suggests, and a fresh install, a new virtual
environment and any upgrade of librosa or numba all start cold. The fix is
`analysis/warm.py`: every process runs one whole head over audio it makes
itself, alone under a lock, before its first real one, so the cache is only
ever filled by one. It is held by two tests that need the extra: the warm up
on an empty cache followed by real heads must leave the cache unchanged, so
no kernel is left for two workers to compile later, and two workers on an
empty cache must finish, three attempts, because a race is not proven by one.
The lesson past numba: a test with real workers on a warm machine says
nothing about a cold one. Ask what state every dependency keeps on disk, and
run the first use twice at once.

## What to do

1. Before explaining a slow run by a planner's inputs, prove the run reaches
   the planner. Grep for the planner's callers in `src`, not in `tests`.
2. Measure before choosing what to change. One process, per stage, on a set
   of mixed lengths: 51 percent harmonic separation, 20 percent the vocal
   model, 16 percent energy, 2 percent each for the decode and the drift. The
   card's own list offered to cut the decode and the drift.
3. Look for the result identical speedup before the approximate one. Windows
   and a cheaper key trade agreement for time and need a reference to judge
   them; the same medians sooner needed nothing but `array_equal`.
4. To make a queued verb parallel, move the MEASURING and leave the writing:
   the engine's one item at a time order is what makes a kill resumable. Read
   results by position through `pool.stream_workers`, and hold a result
   measured ahead to the file and the settings it was measured under.
5. Before two processes share a library for the first time, empty every
   cache that library keeps and start them together, several times.
6. Say what the pool was on both of the verb's exits. A run that failed or was
   stopped leaves through its cause, not its envelope.

## What it bought

On the 23 track synthetic set, one process, same results: 787 s to 355 s. The
light pass's peak for an eleven minute track fell from 2.0 GB to 1.18 GB,
which is what lets a pool be afforded at all. What the pool adds on top is
bounded by the vocal pass, which stays one model in the driver.
