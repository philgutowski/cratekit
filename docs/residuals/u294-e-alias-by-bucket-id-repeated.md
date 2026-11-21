---
title: An alias answer given by bucket id and repeated while its word is settled is refused
found: at round two of the review of #851, U294, 2026-11-21.
issue: no
---

**The mechanism.** `_same_as_settled` in `cli/verbs/tag_campaign.py` compares a repeated alias answer with the settled word's genre folder by its display name only. `Indie Tech=melodic_house`, the bucket id, is taken on the first run. Repeated while the word is still settled, because some of its files did not take the genre, it is refused with "already has its one answer".

**Measured cost.** The repeated command is refused with nothing written, and runs once the answer is dropped or given by name.

**Closes when:** the settled comparison reads the bucket id too. Ledger only.
