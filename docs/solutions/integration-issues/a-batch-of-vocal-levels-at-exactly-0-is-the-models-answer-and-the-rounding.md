---
title: A batch of vocal levels at exactly 0 is the model's answer and the rounding, not a decode or chunking defect
date: 2026-11-03
category: integration-issues
module: "src/cratekit/analysis/vocal.py, src/cratekit/analysis/vocals.py"
problem_type: integration_issue
component: vocal_scoring
root_cause: incorrect_assumption
resolution_type: documentation_update
severity: low
symptoms:
  - "Most of a landed batch of house and techno stamps voxlevel 0, and almost none stamps 1"
  - "A track with an audible vocal carries voxlevel 0 and no vox tag"
applies_when:
  - "Someone asks why a batch scored mostly zero vocal levels"
  - "A change to the vocal floor, rounding or classes is proposed to make more tracks vocal"
tags:
  - "vocals"
  - "panns"
  - "voxlevel"
  - "u171"
  - "a64"
---

# A batch of vocal levels at exactly 0 is the model's answer and the rounding, not a decode or chunking defect

## Context

Sitting 47 scored 116 landed tracks and 80 stamped a vocal level of exactly
0; sitting 51 scored 19 and 17 stamped 0. It looked like a defect: a short
decode, a chunk dropped, a silent stem, the wrong column. U171 had A64
measure, on the Mac, what the frame model heard on every frame of the 116
and of ten known sung leads.

## What it was

The stamp is `round(100 * share of frames with Singing >= 0.05)`, and that
reproduces the voxlevel on all 126 rows. The decode covered every whole file
(100.1 frames a second on every row), the chunk count matched every length,
and the singing columns were the ones read. Of the 80 zeros, 68 never reach
0.05 on a single frame (median loudest frame 0.013), and 12 reach it on under
half a percent of frames, which rounds to 0. Those 12 are the whole of the
"none at 1" look.

One known sung lead, Donna Summer "I Feel Love", stamps 0 because the model
hears no vocal class on it at all (Singing at most 0.034). That is the model's
limit, recorded as a residual, and the choice of what `vox` should count went
to Phillip.

## Guidance

- **Ask for the frame summary before reading the code again.** A64's script
  prints, per track, the max, 95th percentile and share at the floor for
  each vocal class. A zero with a loudest Singing frame under the floor is
  the model's answer; nothing in the decode or the reduction can be its
  cause.
- **Do not lower the floor or widen the classes to rescue one track.** At a
  0.01 floor I Feel Love stamps 1 and an instrumental stamps 16; Speech
  reaches the floor on 43 of the 116. Every change also moves the scale the
  library's existing `vox` tags were stamped on, so it is a restamp decision.
- **`tests/test_vocal_zeros.py` pins the shapes** through `vocals.analyse`,
  so a proposed change shows what it does to each.
