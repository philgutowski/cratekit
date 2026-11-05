---
title: A DOWNLOADED copy's reason can say the sync brings in a playlist the same plan leaves out
found: at the review of #530, U216, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_cli._discovered_back` checks each fresh
account playlist for a `DOWNLOADED ` copy against the paired titles and the
other fresh playlists in the folder, before the later checks (the scope check,
`home_of`, two taking one rekordbox name) run on the fresh one it copies. So
when the plain playlist is left out by a later check, the copy's reason still
says "which this sync brings in from the same folder".

**Measured cost.** Driven by the review's second round on the fake account:
rekordbox already holding a `Disco` no pair made, and the account holding
`Genre Trivia! Disco` and `DOWNLOADED Disco`, planned no create, a TAKEN row
for the plain one and a COPY row saying the sync brings it in. Nothing is made
and nothing is lost; the gate carries two rows that disagree.

**Closes when:** the copy check runs after the place checks and reads only the
fresh playlists still wanted, or its words say "a playlist beside it in the
same folder". Ledger only.
