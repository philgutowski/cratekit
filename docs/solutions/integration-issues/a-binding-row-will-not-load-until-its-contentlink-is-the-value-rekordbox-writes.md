---
title: "A content row the binding makes will not load to a deck until its ContentLink is the value rekordbox writes on its own rows"
date: 2026-10-10
category: integration-issues
module: src/cratekit/intake/native.py, src/cratekit/write/row_link.py
problem_type: integration_issue
component: native_landing
severity: high
root_cause: wrong_assumption
resolution_type: workflow_improvement
applies_when:
  - "A row Cratekit created in master.db shows every column in rekordbox but Load is greyed and a drag to a deck lands nothing"
  - "A column comparison between a loadable row and an unloadable one is being read by eye"
  - "A candidate cause is being tested one column per rekordbox open"
symptoms:
  - "Load, Add To Tag List and Export Track greyed on a landed row's context menu, live on a row rekordbox imported"
  - "The row analyses on request and shows title, art and length, and still never loads"
related_components:
  - "database"
  - "rekordbox"
tags:
  - rekordbox
  - contentlink
  - native-landing
  - r-928
  - probe
  - play-history
---

# A binding row will not load until its ContentLink is rekordbox's value

## The trap

pyrekordbox's `add_content` sets `djmdContent.ContentLink` from the TRACK menu
item's `rb_local_usn`. Every row the native landing made carried `2973454`.
rekordbox writes one value on nearly every row it imports, `2950670` on 10,292
of this library's rows, and that value keys no table. A row carrying the
binding's value is read whole by rekordbox, analysed on request, and refused a
deck, with no dialog and nothing in any log.

Three sittings were spent on columns that were real differences and not the
block: the twenty one NULL defaults (R-923, sitting 33) and the random
`rb_file_id` (U115, sitting 36). Both repairs stay correct. Neither made a row
load.

## The proof, sitting 37 in docs/cutover.md

One gated write put ContentLink alone on two rows and ISRC alone on another,
with an untouched row as the control. The two ContentLink rows loaded at once,
the ISRC row and the control did not. After ContentLink was written on the
remaining rows, the control itself loaded: the same row, before and after one
column. `ISRC` stored NULL and `AnalysisUpdated` at 1 were still on every row
that loaded, so neither is needed.

## How the cause was found fast, and how to find the next one

The slow part was testing one guessed column per rekordbox open. What found it:

1. **Enumerate by exclusion, not by eye.** For every column, ask whether the
   unloadable row's value, or its storage shape (NULL against empty text),
   occurs on ANY row rekordbox made. A value that some loadable row carries
   cannot be the block. Over 78 columns this left three candidates where a
   side by side diff of two rows showed a dozen differences.
2. **Play history is evidence of loadability.** `djmdSongHistory` names rows
   that were loaded to a deck. A candidate value carried by a row played under
   the current rekordbox version is eliminated without opening rekordbox. Date
   the play: a play from rekordbox 6 does not speak for 7.
3. **One rekordbox open, many rows.** `crate repair link` takes many
   `--set ROW:COLUMN=VALUE` triples, so each subset of candidates sits on its
   own row and one reading answers all of them. Keep an untouched row as the
   control, and prove a positive on a second row.
4. **Never write an analysis column to test it.** `AnalysisUpdated` is refused
   by the guard under R17. Let rekordbox move it by analysing the row again.

A drag onto a deck is the reliable read from the desktop control tool. The
context menu sometimes does not appear in a screenshot at all.

## What still has to change

The landing still lets the binding choose ContentLink, so every new native row
is unplayable until the landing sets the library's own value. Until that lands,
`crate repair link` with `--set ROW:ContentLink=2950670` per landed row is the
repair, rehearsed on a copy like any gated write.

## Related

`docs/residual-findings.md` R-928. `src/cratekit/core/rb_writer.py`
`ROW_PROBE_COLUMNS`. [[a-read-back-that-walks-session-new-cannot-see-a-creation-the-binding-flushed]]
is the neighbouring trap in the same landing.
