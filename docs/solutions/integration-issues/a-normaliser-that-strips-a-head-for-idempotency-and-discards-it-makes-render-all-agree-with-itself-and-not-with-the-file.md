---
title: A normaliser that strips a head for idempotency and discards it makes render_all agree with itself and not with the file
date: 2026-09-29
category: integration-issues
module: src/cratekit/core/naming.py
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "A caller supplies a key without a tempo to naming.render_all"
  - "A landed track's rekordbox Name is bare while its filename and title tag carry a head"
---

# A normaliser that strips a head for idempotency and discards it makes render_all agree with itself and not with the file

## Problem

R-740. A track landed by `intake land` had filename and title tag `01A - 112 - Ain't Gonna Hurt Nobody` and a rekordbox Name of `Ain't Gonna Hurt Nobody`. Measured on 18 of 18 landed files. Every landing needed Reload Tags by hand. The symptom pointed at `intake.ingest.read_meta`, which is where the bare name was built.

## Cause

The loss was not in intake. `naming.normalize_spec` strips a head from the title so that rendering twice never doubles it, and it threw the stripped head away. The three surfaces (filename, title tag, library name) agree with each other only because `render_all` renders all three from one spec, so they agreed with the spec and not with the file. No tempo tag is ever written, so the tempo lived only in the head that was stripped. Any caller that supplied a key and no tempo lost the head. The naming verb and analysis had each been silently rebuilding the head before calling it, which hid the defect from every path except intake.

## What to do next time

- Fix it in `normalize_spec`, where it broke: it keeps the head it strips and fills empty spec fields from it only when every supplied value agrees. `read_meta` takes its key from the title head, then the filename head, over the key tag.
- Read the tempo out of the head as text with `naming.split_head`. Never from a tempo tag, a BPM tag or an average BPM field, since that is a grid write (see `a-mapping-that-carries-bpm-is-a-grid-write.md`).
- When a function strips something for idempotency, ask what it does with the stripped part. A caller that compensates by rebuilding the value before the call is the sign the function is dropping it.
- Ledger rows R-748 to R-750 hold what was left over. The 18 and 61 rows already landed with bare Names are not repaired by this fix.
- `scripts/mutate.py` refuses a batch on a state leak or red baseline when an installed crate backup or doctor runs on the same machine. Rerun the batch; see `a-state-leak-halt-during-the-null-control-can-be-another-process-polling-the-installed-copy-so-read-the-newest-run-record-before-blaming-a-child.md`.
