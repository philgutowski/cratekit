---
title: A native landing writes its label filing record only when the commit added or made something, so label mark by pass could say a batch filed nothing
found: at the review of #362, R-1056, 2026-11-01.
issue: no
---

**The mechanism.** `label_filing.record_commit` returns before writing the
`labels` key when `written.changed()` is false, that is when every year
playlist the commit filed into already held every track it was asked to
hold and no node was made. `label mark --pass` reads that key as what the
landing filed, so a landing whose filing changed nothing would be read as
one that filed no year, and the mark would end NO_OP with
`label-mark-nothing-filed`. The bridge writes its tree into the intake file
whatever it added, so the two proofs could disagree here.

**Measured cost.** Not driven to a cost. The one candidate driven, a second
native landing of the same file under another pass, is refused before it
moves anything because the file already exists in the library, so no record
commits. No producer was found.

**Closes when:** a landing that filed into year playlists names them on its
record whether or not it added a membership, or a producer is shown not to
exist. Ledger only, since nothing reaches it.
