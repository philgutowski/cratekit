---
title: A word the template declares as a tag with no folder is refused as one that already has a place
found: at the second review of #465, U194, 2026-11-02.
issue: no
---

**The mechanism.** The shipped template declares `Melodic Techno` as a suggest rule with a literal tag and no bucket, and its comment says to declare a bucket for it. `suggest_tag` does not flag it off taxonomy, so `crate taxonomy folder "Melodic Techno"` and `crate taxonomy alias "Melodic Techno" Techno` refuse it as `already-filed`, "already has a place in the taxonomy: tagging writes it as 'Melodic Techno', a word the copy declares on purpose", while a file carrying it routes by keyword to Melodic House.

**Measured cost.** Driven by the review. The pass never names the word, since it is not off taxonomy, so nobody is sent there; the cost is a sentence that says "a place" for a word with no folder.

**Closes when:** the sentence says the word is one tagging writes as itself with no folder of its own, declared so by the copy, or the folder verb accepts such a word. Ledger only: wording, and the plan's decision that only an off taxonomy word is answered stands.
