---
title: "A numba kernel keeps the code it was first compiled to, so the same measure in two processes can differ in its last bits"
date: 2026-11-23
category: integration-issues
module: "src/cratekit/analysis/energy.py, src/cratekit/analysis/warm.py, src/cratekit/analysis/detect.py"
problem_type: integration_issue
component: analysis
severity: medium
root_cause: compile_order
resolution_type: guard
applies_when:
  - "Two verbs compute the same feature from the same audio in different processes and are expected to agree to the bit"
  - "A head runs in a worker process and a restamp or calibrate runs in the driver"
  - "A new path calls librosa or a numba kernel before the warm up has run in its process"
symptoms:
  - "The energy features of one file differ in the last float32 bits between a worker's head and the driver's restamp"
  - "A level one step apart on a track sitting on a decile cut, only across processes, never within one"
  - "The difference comes and goes with which verb a process ran first"
tags:
  - "numba"
  - "librosa"
  - "warm-up"
  - "determinism"
  - "energy"
  - "u344"
---

# A numba kernel keeps the code it was first compiled to

## What happened

U344 made `analyze run` measure energy through the restamp's own measure, so
the tail could leave out the files the run had scored. Within one process
the two agreed on every file. Across processes, a head in a worker against
the restamp's measure in the driver, 21 of 23 FLACs and 19 of 32 MP3 and M4A transcodes
agreed: the others differed in the last bits of `beat_concentration`, enough
to move a file on a level's edge.

## Why

librosa's numba kernels are compiled lazily, and each keeps the
specialisation it was first compiled to for the life of the process. A
process that ran a whole head first compiled the shared kernels for the
head's inputs; one that measured energy first compiled them for the slice.
Same code, same audio, different machine code, different last bits. The
cause was not in the measure, which was identical; it was in what the
process had run before it.

## What to do

Every path that measures energy goes through `energy.features_from_path`,
which calls `warm.kernels()` before it decodes, so every process compiles
its kernels in the same order, the warm up's, before its first real
measure (and under the warm up's lock, which also closed R-1491's cache
damage). With that, 23 of 23 and 32 of 32 agreed across processes. A new
path that calls a numba kernel, or librosa, before the warm up has run in
its process reopens this: ask `warm.kernels()` first.

To see it: measure a set of files in one fresh process that runs a head
first and in another that measures energy first, over the same kernel
cache, and compare the features with `==`, not a tolerance.
