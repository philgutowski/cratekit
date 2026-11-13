---
title: crate doctor does not report a catalogue that has been refusing this client, or since when
found: at the build of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** U284 keeps when each record shop began refusing this
client in `catalogue_refusals.json` (`src/cratekit/tagging/refused.py`), and a
sweep's report and a pass's stop read it. `crate doctor` does not: a person
asking the health check learns nothing of a Beatport that has refused every
lookup for days until a sweep or a pass says so. The card's first requirements,
written for its option 1, asked doctor to report a catalogue refusing on its
last N lookups with the date it began; Phillip chose option 3, whose answer
names no doctor check, so the build left it out.

**Measured cost.** Not driven: no verb is blocked and nothing false is said,
the date reaches a person at the sweep and at the pass.

**Closes when:** doctor reads the record and reports each refusing catalogue
with its `since` and `last`, never failing on it. Ledger only.
