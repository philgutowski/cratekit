---
title: A live label needle that relied on a part word match now confirms nothing, and none of the live needles was measured
found: at the review of #645, U237, 2026-11-10.
issue: no
---

**The mechanism.** `labels_match` (`src/cratekit/label/verify.py`) now needs one side to appear in the other as whole words of the folded strings. Credit shapes the substring rule confirmed and the word rule refuses: a clipped needle (`Some Label Rec` against `Some Label Records`), a run together credit (`RawaxRecords`), a year joined to the name (`©2021Rawax`), a catalogue number suffix (`RAWAX007`), an abbreviation against a full name (`Cadenza Records` against `Cadenza Rec.`), an accent at the needle's edge (`Cliché` against `Cliche Music`).

**Measured cost.** Each shape driven by the reviewer, main confirming and the branch refusing. Loud when every release of a label fails (`label-sweep-incomplete`), silent when only some do. The live registry is not on a cloud container, so how many of its needles are affected is unknown.

**Closes when:** the attended card for U237 has run a label sync over every registered label on a disposable state copy and repaired each needle that confirms fewer releases than before with `crate label registry set NAME --match`. Ledger only.
