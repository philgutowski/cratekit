---
title: A pair whose rekordbox side was released after a stopped order and paired again has its first sync write the stopped write's scramble into rekordbox
found: at the review of #591, R-1372, round one, 2026-11-06.
issue: yes
---

**The mechanism.** A stopped order on a pair is read by `_Reader.stopped_write`, which `plan_pair` consults only for a pair the pairs document holds. When the pair's rekordbox playlist is deleted after the stop, a sync releases the pair (`sync-pair-released`), and when the account playlist is then paired by hand with a new rekordbox playlist, that pair's first sync runs with no pair record (`held` is None), so the stopped write is never read: the first sync takes the account's order, which is the stopped write's scramble. The carried record R-1372 keeps is on disk and read by nothing, and the second sync has a snapshot that passes it.

**Measured cost.** Driven by the round one reviewer on the fake account: the U225 stop, the rekordbox playlist deleted, a sync (released), a new rekordbox playlist in rekordbox's order, `crate sync pair ACC --rekordbox NEW`. The new rekordbox playlist became 2, 7, 1, 3, 4, 5, 6, with nothing said of the stop. The same before R-1372 within thirty days, and with or without its mark guard. The producer, a deletion and a hand pairing after a stop, was driven step by step, not observed live.

**Closes when:** the first sync of a pair marked on an account playlist with a stopped write carried for it finishes that order from the side that led it, or names the stop on the gate and leaves the account's order out of what it writes to rekordbox.
