---
title: The matcher and the tombstone module still read a credit spelled with leading punctuation, an accent or fullwidth letters differently
found: at the build of #691, U262, 2026-11-12.
issue: no
---

**The mechanism.** U262 gave `acquire/match.py` `_is_a_credit` the first
whole word rule `core/tombstone.py` `_is_a_credit` asks, over an equal
marker set, and a test holds the two equal over one list of groups. The two
still fold differently: the matcher folds punctuation to spaces and strips
accents and compatibility forms (NFKD), the tombstone module keeps
punctuation and composes (NFC). So `- feat. Anna`, `"with" Anna`,
`ｆｅａｔ Anna`, `Feät Anna` and `Ⓕeat X` are credits to the matcher and
versions to the tombstone module. Every one of them answered the same way
under the letters rule U262 replaced, so this unit moved none of them.

**Measured cost.** Driven on the two predicates only. A title carrying such
a group is split by the matcher with the group taken off as a credit, while
a deletion of that row records no companion, so a provider spelling without
the guest misses the tombstone and is reported as a missed suppression. No
list or library title in this shape was found or driven, so the reachability
is unmeasured.

**Closes when:** one fold is chosen for both predicates. The tombstone
module's set and rule are inside the identity stamp, so the change is the
matcher's, and it moves the matcher's answer for these spellings, which needs
its own card. Ledger only.
