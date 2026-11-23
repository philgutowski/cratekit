---
title: rekordbox's Auto Analysis dialog shows the Analysis Mode the last Analyze Tracks OK wrote, so a visit that ends on its Dynamic run sets up the next one to cancel
date: 2026-11-23
category: workflow-issues
module: "attended sittings, the rekordbox visit"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "A rekordbox visit runs a Dynamic Analyze Tracks run for rows carrying the dyn My Tag"
  - "The launch's Auto Analysis dialog reads Analysis Mode Dynamic with every other field the standard"
tags:
  - "rekordbox"
  - "auto-analysis"
  - "analyze-tracks"
  - "dynamic"
  - "attended-sitting"
related_components:
  - "tooling"
---

# rekordbox's Auto Analysis dialog shows the Analysis Mode the last Analyze Tracks OK wrote

## Context

At attended sitting 104 (A190) the launch's Auto Analysis dialog read
Analysis Mode **Dynamic**, every other field Phillip's standard, so the
`rekordbox-visit` skill cancelled it. The Analyze Tracks dialog then opened
on the same fields. Sitting 103 had ended its visit with the skill's Dynamic
run on its `dyn` rows. The two dialogs are not two settings: they read one
Analysis Mode, and the last Analyze Tracks OK writes it. So every visit with
a `dyn` row, run Normal first and Dynamic second as the skill then said, set
up the next visit to cancel the short path. Cancel held (no analysis file in
32 seconds), and an Auto Analysis run set no cue (no `djmdCue` row on sitting
103's 100 rows), so the Auto Analysis path was otherwise sound.

## Guidance

**Make the visit's last OK a Normal one** (U954). On the Analyze Tracks path
run the Dynamic run on the `dyn` rows first and the Normal run on the rows
whose `dyn` is false last: the selections never overlap, so no Dynamic grid
is overwritten and no row is analysed twice. On the Auto Analysis path, whose
OK analyses every waiting row on Normal before anything is selected, follow
the Dynamic run with a closing Normal Analyze Tracks run on one row without
`dyn`, which analyses it again on the same fields and leaves Normal set.

**A batch whose every row carries `dyn` has no row to end on Normal.** That
visit ends on Dynamic, says so in its record, and the next launch's dialog is
cancelled for this known cause. Sitting 104 itself put the mode back by
analysing a throwaway AIFF alone on Normal, under CLAUDE.md's clause for a
probe; whether a visit may do that routinely is open (the residual U954
filed).

**The track list's filter offers no My Tag** (sitting 104), so the `dyn`
rows are selected by Command clicks, and the Normal run's selection is every
row with the `dyn` rows Command clicked out.

**Unmeasured until the next attended visit**: that a visit ending on Normal
leaves the next launch's dialog reading Normal, and that the closing run's
second analysis of an analysed row raises no dialog of its own.
