---
title: "A tempo off by one to three is the tempogram's bin width, not a setting, and a parabola through three bins recovers it"
date: 2026-09-30
category: workflow-issues
module: src/cratekit/analysis/detect.py
problem_type: workflow_issue
component: analysis
severity: high
root_cause: quantisation
resolution_type: code_fix
applies_when:
  - "A measured tempo disagrees with a reference by a small integer on many tracks and by a ratio on a few"
  - "A brief attributes a disagreement to an analyser's settings, a range or a notation, before the mechanism is driven"
  - "librosa.feature.tempo or a tempogram argmax is the estimator"
  - "A precision problem is about to be fixed by a finer hop, at several times the cost"
symptoms:
  - "129 against 127.00, 112 against 110.11, 144 against 140.00: the head is high by one to three near 128 and the reference is a fraction"
  - "Exact agreement with rekordbox is 39 of 299 and agreement within one beat 106 of 299"
  - "The same tracks read equal on 193 of 299 after interpolation with nothing else changed"
related_components:
  - analysis
  - naming
tags:
  - r744
  - tempo
  - tempogram
  - librosa
  - interpolation
  - quantisation
  - cause-not-where-it-looked
---

# A tempo off by one to three is the bin width, not a setting

## Context

R-744 recorded heads that disagreed with rekordbox's grid, most by one to
three and a few by a ratio, and its brief looked to the analyser's settings:
a tempo range that halves or doubles, a key notation. The range was real and
worth adding, and it explained the ratio cases in part. It explained none
of the one to three cases, which were the bulk.

## The mechanism

`librosa.feature.tempo` names the strongest bin of an aggregated tempogram,
and a tempogram bin is one frame of lag. At the 22,050 Hz measure rate with
a hop of 512 samples a frame is 23.2 ms, and tempo is `60 * rate / (hop *
lag)`, so the bins are not evenly spaced in tempo: lag 20 reads 129.2, lag
21 reads 123.0, lag 23 reads 112.4, lag 24 reads 107.7. Near 128 the grid is
six beats wide, and a track at 127.00 lands on lag 20 and is named 129. Every
one to three case in the ledger is that arithmetic. The number came out
confident because a wrong bin is still a peak.

## The fix, and what it measured

Fit a parabola through the strongest bin and its two neighbours and take
the vertex as the lag. On 299 files rekordbox had analysed itself, exact
agreement went from 39 to 171 with nothing else changed, and to 194 with the
window and prior on top. The vertex is held to half a bin either side and the
answer is held inside the window, because the bin is chosen on the
prior-weighted score and the parabola is fitted on the raw strength, so a
stronger raw neighbour outside the window can lean the vertex past the
edge. The built in review found that; a test with an edge bin pins it.

A finer hop would have bought the same precision at four times the onset
cost and was not needed. What no interpolation fixes is the other level
bucket, 51 of 299, a pulse read at three to two or four to three of the
reference; that is the method's rate and is recorded as such.

## The rule

When a measurement is off by a small amount on most inputs and by a ratio on
a few, compute the estimator's own resolution at the input's scale before
reading its settings. A quantised estimator disagrees by its bin width,
and the bin width is arithmetic that can be checked against the ledger's own
examples in a minute.

## Related

- `docs/cutover.md`, sitting 22, the estimator table.
- `docs/mutation/r744.md`, row `E3`, the interpolation removed, 11 kills.
- R-744, closed on `relay/232`.
