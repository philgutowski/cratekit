---
title: A pairs document that fails to write after a playlist is made from the account leaves that playlist unpaired
found: at the second review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `PairStore.reserve_made_rekordbox` takes the lock, runs the
create, which commits the rekordbox playlist, and then writes the document.
The lock proves the document's directory is writable before anything is made;
it does not prove the write after will succeed. A write that fails there, a
full disk for one, leaves the playlist in rekordbox with no pair, and the next
sync names the account playlist taken because its rekordbox folder holds the
name. U198's `reserve_made` has the same shape on the account side.

**Measured cost.** The second review made `PairStore._write` raise a disk full
error: the verb exited 1, the playlist was live and unpaired. The producer was
simulated, not driven. One account playlist then needs a hand pair, which the
warning says how to do.

**Closes when:** the pair is written before the create under a reserved
marker, or a playlist the product made is recognised by a record written
before its commit. Ledger only.
