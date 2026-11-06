---
title: A library change to a mirrored playlist between the account gate and its apply is applied as decided, a choice built while Phillip's answer waits
found: at the build of #552, U222, 2026-11-05.
issue: no
---

**The mechanism.** Since R-1031 the run that answers the account gate rebuilds
the mirror from the library as the gate read it, and since U222 from the
snapshot as the gate read it too, so any library change made between the two
acts, to a mirrored playlist or not, is left for the next organize. The card
asked Phillip whether a change he makes in rekordbox to a mirrored playlist
between the acts should instead refuse the answer as stale (the card's
"Question for Phillip", answer 1 recommended). U222 built answer 1, the
behaviour already shipped and proven at sitting 58, as the conservative call.

**Measured cost.** None lost under answer 1: a track the library added or took
off between the acts reaches the account at the next organize, one run late.
Not driven live; driven on U204's disposable library for the edits the
rekordbox area takes from the account.

**Closes when:** Phillip answers on the decisions page. Answer 1 closes it as
is; answer 2 or 3 is a follow up card that reads the live library on the apply
and compares it with the frozen one. Ledger only.
