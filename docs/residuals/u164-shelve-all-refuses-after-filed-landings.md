---
title: shelve --all refuses where only filed landings exist, rather than saying there is nothing to do
found: at the review of #345, U164, 2026-10-31.
issue: no
---

**The mechanism.** `intake shelve` given a batch a native landing filed answers
`already-filed` with nothing to do (U164). `intake shelve --all` walks only the
folders under the music folder, and since native landings make none, a library
whose every recent batch was filed has nothing for it to find, so
`shelve_cli._assert_nothing_to_ask` refuses `intake-list-unusable`, "no batch
under the music folder can be shelved". The sentence is true and the refusal
predates this unit.

**Measured cost.** Driven at the review: exit 30 with that sentence, nothing
moved or written. A person reads a refusal where the honest answer is that
nothing is waiting.

**Closes when:** `--all` over a music folder with no batch folder ends with
nothing to do, naming the filed batches it knows of, rather than refusing.
Ledger only.
