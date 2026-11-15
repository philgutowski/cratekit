---
title: The spelled out lookup and title test cost more CPU on a library heavy in slang titles
found: at review round one of #833, R-1705, 2026-11-15.
issue: no
---

**The mechanism.** Every approximate pass now spells out the wanted title,
looks it up in a map built once per index, and spells out both titles in
each title test it runs. The author measured 0.569 s on main against
0.668 s on the branch for 1,000 rows over 10,000 recordings, CPU median of
five, on a corpus of their own; the review, on titles heavy in listed
words, measured 0.851 s against 1.403 s, about 0.55 ms more a row, with no
state changing in that corpus. The author's number came from a fixture
written alongside the change.

**Measured cost.** Not user facing at the library's size: a list of a few
hundred rows pays a fraction of a second. Unmeasured on the live volume.

**Closes when:** the approximate pass is timed on the live library at a
sitting, or the spelled out forms are cached per recording as the sorted
words are. Ledger only.
