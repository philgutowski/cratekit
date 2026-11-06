---
title: An adoption ledger the account mirror cannot read reads as no landing, and the landed track's account edit is undone with no word of the ledger
found: at the review of #579, U227, 2026-11-06.
issue: no
---

**The mechanism.** `organize.mirror_downloads.filed` answers `{}` when the
job queue or the adoption applied ledger cannot be read, or when an entry
names a sub the taxonomy no longer declares. The edit rule then reads a
landed track's filing by its tags as a change made in rekordbox, as before
U227. The plan says "so rekordbox's place stands" and the mirror takes the
track off the playlist the person put it in on the account. Neither step names
the ledger it could not read.

**Measured cost.** Driven on U204's world by Fable's round one (P1, P3).
After the queue, the landing and its filing, the ledger's `applied` field was
made a string, or the entry's sub was made one the taxonomy lacks. The plan
then kept rekordbox's place, and the apply emptied the account's Tech House
Med. The producer was not driven: the ledger is written atomically under a
lock by `adopt.apply.write`, and one candidate, the tool's own writer, was
driven and wrote a readable ledger. So whether a real library reaches an
unreadable ledger is unmeasured.

**Closes when:** `filed` returns why it read nothing, and the edit rule holds
each queued track whose landing it could not read, with that reason, rather
than reading it as rekordbox's. Ledger only until a producer is driven.
