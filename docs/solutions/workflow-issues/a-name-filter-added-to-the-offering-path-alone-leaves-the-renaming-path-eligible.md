---
title: "A name filter added to the offering path alone leaves the renaming path eligible"
date: 2026-09-22
category: workflow-issues
module: "sync/playlists.py exclusion, sync/pending_marks, mark_cli plan"
problem_type: workflow_issue
component: core_logic
severity: medium
root_cause: incomplete_seam_coverage
applies_when:
  - "A naming convention gates whether a playlist is offered by a sync pass"
  - "A second entry point reads the same account state to decide a rename or write"
  - "The two entry points look like one rule because they share one predicate name"
tags: [sync, playlists, r-361, mark, pending_marks, two-entry-points, name-filter]
---

# A name filter added to the offering path alone leaves the renaming path eligible

## Problem

R-361 added `is_library_debris`, a suffix check on ` LIBRARY` (leading space,
case sensitive) so the source system's own label-run playlists stop being
offered by `sync.playlists.exclusion` as ordinary intake. The first build
added the check in exactly one place: `exclusion`, which decides what a pass
OFFERS. The built-in review caught that this was not enough.

## Cause

`exclusion` deciding what gets offered is not the only place that reads a
playlist's name against this convention. `pending_marks`, and `mark_cli`'s
plan for `crate sync mark`, decide what gets RENAMED on the account, and they
read the same account state independently. A debris playlist can still reach
the cursor without ever being offered: an older job queued before the rule
existed, or a hand run through `crate intake playlist`. If that happens, the
rule living only in `exclusion` leaves `pending_marks` and the mark verb happy
to rename the source system's own throwaway to `DOWNLOADED Sol Selectas
LIBRARY`, a write the source system never makes itself.

The swept prefix already lived correctly in all three places. The new debris
suffix was added to only the first, because the offering path is the one the
issue brief names and the one a test naturally exercises first. The seam that
was missed is not "did the check", it is "which callers ask a name predicate
before doing something to the account".

Since U242 the mark renames nothing: it records the playlist as taken in the
mark record, and `pending_marks` asks `playlists.is_taken` where it asked the
prefix. The lesson is unchanged, with TAKING in place of RENAMING: a rule on
the offering path alone leaves the taking path open.

## Next time

- When a naming convention gates a sync pass, ask at the seam how many entry
  points touch account state by name: what gets offered, and separately what
  gets renamed or written. A rule added to one and not the other passes its
  own tests clean, because each test drives one path.
- Read the shared reason word through the enum (`Excluded.LABEL_DEBRIS`) at
  every site rather than respelling a literal, so the kebab string used for
  assertions and reason columns is pinned once, not once per call site.
- The built-in review is what caught this, not the author's own battery. A
  green suite over a rule added at one of three sites still reports green.
