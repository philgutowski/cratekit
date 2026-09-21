---
title: "Evidence kept to recognise a thing later is a snapshot replaced whole, not a log, and a queued job's stable identity is what it was confirmed against"
date: 2026-09-21
category: workflow-issues
module: "src/cratekit/modules/outbound/ledger.py, src/cratekit/modules/outbound/export.py, src/cratekit/export/cli.py"
problem_type: workflow_issue
component: outbound_ledger
root_cause: wrong_identity
resolution_type: code_fix
applies_when:
  - "A brief asks for state to be keyed on a stable identifier from a rekordbox collection export"
  - "A store has to recognise something whose only key is a name or a path a person can change"
  - "A per item worker records evidence about the whole it is one item of"
  - "A record is moved or re-keyed while jobs confirmed against the old key may still be queued"
symptoms:
  - "A threshold against recorded evidence passes every test and stops matching after a few real runs"
  - "One recorded row out of a hundred makes anything carrying that row a full match"
  - "A job resumed after a re-key reads its own key as never written and creates a duplicate"
  - "A gate said update and the worker created"
related_components:
  - job_engine
  - confirm_gate
tags:
  - outbound
  - ledger
  - identity
  - r-229
  - per-item-shape
  - rekordbox-export
---

# Evidence kept to recognise a thing later is a snapshot replaced whole, not a log

## Context

R-229: the outbound ledger keys a remote playlist on the crate's display path,
so a rename or a drag into a folder made the next export create a second remote
playlist. The issue's approach said to key on "the playlist's stable identifier
from the export". There is none. A playlist node in a rekordbox collection
export is a name, a place in a tree and its track ids, which
`modules/reports/export.py` shows and which the ledger entry had already said in
its own second sentence. The brief and the entry it pointed at disagreed, and
the entry was right.

So the fix had to RECOGNISE a crate under a new path from evidence, and the
first version of that evidence was wrong in three ways a green suite did not
see. The built in review found all three.

## The trap

**One, the evidence was a log.** The first version appended each written row's
library identity to the record, per item, and judged "this crate still carries
at least half of what was recorded". A crate whose music rotates, a current set,
grows the log on every export and the crate never grows with it. Three full
rotations and the share is a third, the record stops matching, nothing is
offered and nothing is warned, and the rename forks again. Every test passed,
because every test exported once or twice.

**Two, per item recording makes partial evidence.** One item is one track here.
A legacy record being backfilled row by row, interrupted after the first item,
holds one row, and then ANY crate carrying that row scores one of one.

**Three, a moved record strands the jobs confirmed against it.** Re-keying the
record from the old path to the new one is right, and a half driven job still
queued under the old path then reads "no record under my key" as "never
exported" and creates, which is the defect again by a second route. The same
hole in the other direction: two crates can both be offered one orphaned record
before either is driven, both gates say update, and the second to run found the
record gone and fell through to create.

## What to do instead

- **Record what the thing HELD at its last write, whole, and replace it.** The
  crate's full track set is frozen in the job payload, so the worker hands it to
  `reserve_playlist` as `contents` and the first item writes all of it under the
  ledger lock. Replaced, so the threshold is always against the last export.
  Whole, so there is no partial state. Unmatched rows included, since a row the
  provider lacks is still a row of the crate.
- **Bound both sides of an overlap.** Half of the record alone lets a three
  thousand track crate that merely contains an eight track orphan score eight
  of eight. The shared tracks must also be a quarter of the crate, and the
  sentence a person reads names both sizes.
- **Freeze the remote id the gate showed, and find the record by it.** It is the
  one stable identifier an outbound job has. A job whose key no longer holds
  that id looks for the record that does and writes there. A job that confirmed
  an adoption or an update and finds neither REFUSES `outbound-record-moved`. It
  never creates, because a create is not what the person confirmed.
- **Absence of the field, not emptiness, marks a legacy record.** A record this
  build wrote with an empty list has no evidence and gets no name rule.
- **Do not bump a state file's version for an additive field** while the pipx
  copy of the product reads the same file. `_load` refuses any version it does
  not know, so a bump locks the other copy out of its own ledger.

## How to notice it next time

- When a brief and the ledger entry it cites disagree about what exists, read
  the reader. `grep -n 'class Playlist' src/cratekit/modules/reports/export.py`
  answered this one in ten lines. Then fix the card, as METHOD says.
- For any threshold against recorded evidence, ask what the denominator does
  over ten runs, not two. Write the test that exports three times with disjoint
  contents, `test_the_recorded_contents_are_replaced_and_not_grown`.
- For any per item worker that records something about the whole, ask what the
  record says if the job dies after item one.
- For any re-key, grep for who else holds the old key: queued payloads first.
  `formerly` was written by the first version and read by nothing, which is what
  a forwarding address nobody follows looks like.

Open after this: R-630, a path reused for a different crate still updates the
old playlist when it is exported first, warned and not prevented; R-631, no way
to choose among several candidates; R-633, the two bounds are judgment and no
adoption has met a real account.
