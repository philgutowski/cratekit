---
title: "A whole number tempo in the collection is the source system's import, and only a stored fraction is rekordbox's own analysis"
date: 2026-09-30
category: integration-issues
module: src/cratekit/analysis/agreement.py
problem_type: integration_issue
component: rekordbox_database
severity: high
root_cause: sample_selection
resolution_type: workflow_improvement
applies_when:
  - "A measurement is about to compare anything this product computes with what rekordbox computed for the same file"
  - "A sample is being drawn from djmdContent rows and the brief says 'rows rekordbox has analysed'"
  - "A stored BPM, KeyID or grid is about to be read as ground truth"
  - "A rate over the back catalogue reads as suspiciously good"
symptoms:
  - "The back catalogue's heads agree with the stored tempo on three rows in four and disagree only by one to three"
  - "Every stored tempo on an old row is a whole number in hundredths"
  - "The stored key names are Camelot codes in two paddings rather than classic names"
  - "A comparison over thousands of rows measures the source tool against itself"
related_components:
  - analysis
  - rekordbox_database
  - cutover
tags:
  - r744
  - rekordbox
  - tempo
  - key
  - sample
  - ground-truth
  - source-system
---

# A whole number tempo in the collection is the import, not rekordbox

## Context

R-744's brief asked for a comparison of the head's tempo and key with
`djmdContent.BPM` and `KeyID` over 200 or more files rekordbox has analysed.
The first read of a disposable copy answered in seconds and looked
excellent: 9,776 rows with a head, 73.8 percent equal to the stored tempo,
25.3 percent off by one to three, 89 percent of keys equal. None of it
measured rekordbox.

## What was actually there

The source system, DJ_tools, wrote a `TEMPO` grid into the collection xml
at import, with the same integer its head named, and Mixed In Key wrote the
key into the file tag in Camelot notation. rekordbox keeps an imported grid
and an imported key and does not recompute either. So on every row the
source system imported, the stored tempo IS the head, in hundredths, and the
stored key IS the head's key in a `djmdKey` row named `8A` or `08A`. The
comparison the brief asked for was, on those rows, a tool compared with its
own earlier output.

rekordbox's own analysis leaves a different mark: a tempo with a fraction,
90.96, 110.11, 127.00 stored as 12700 is ambiguous, 155.62. No tool that fed
this library writes a fraction: Mixed In Key writes an integer, the source
system rounds half up, tag readers carry integers. So `BPM % 100 != 0` is
sufficient for "rekordbox computed this", and 1,361 of 10,020 rows are so.
It is not necessary: rekordbox answers a whole number on roughly two
programmed tracks in five, and those rows cannot be told from imports after
the fact. The sample therefore leans toward unquantised material, classical
and live recordings among them, and understates agreement on programmed
music. The 22 rows this product headed and rekordbox then analysed were the
only clean intake sample and were reported beside it.

## The rule

Before comparing anything with "what rekordbox computed", ask where the
stored value came from. In this library the answer is in the value's own
shape, and `HeadRow.analysed_by_rekordbox` holds it. State the bias the
selection carries wherever the numbers are quoted, and keep a second, clean
sample beside the biased one even when it is small.

## Related

- `docs/cutover.md`, sitting 22, both tables.
- R-744, closed on `relay/232`; R-784, the key rate.
- `docs/solutions/workflow-issues/a-mapping-that-carries-bpm-is-a-grid-write.md`,
  why the detector's dictionary says `rate`.
