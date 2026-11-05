---
title: The check before a sync pair write does not read again that an unpaired twin's account playlist is still gone
found: at the build of #499, U209, 2026-11-05.
issue: no
---

**The mechanism.** U209's `check` reads, before the write, every list the
held plan's writes are merged from, and that a made pair let go for its
rekordbox side is still let go. A twin or made pair the plan unpaired because
its account playlist was gone is forgotten at the write without reading the
account's playlists again, which would cost the catalogue's listing of every
playlist of the author's.

**Measured cost.** Not driven. A playlist deleted on the account does not
come back under its identifier, so no producer is known; the write touches
only the pairs document, no list.

**Closes when:** a producer is found, then the check lists the author's
playlists once when the plan unpairs any for a gone account side. Ledger only.
