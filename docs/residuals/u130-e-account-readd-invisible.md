---
title: An account track removed and added again between two pair syncs reads as never removed
found: at the build of #298, U130, 2026-10-10.
issue: no
---

**The mechanism.** The merge sees a removal and a re-add on the same side
between two syncs only where the side gives a membership an identity, which
rekordbox does with its row and the account does not. So a track removed in
rekordbox and, in the same interval, removed and added again on the account,
reads on the account as held all along, and the rekordbox removal is applied
to the account.

**Measured cost.** Not driven: the account offers nothing a sync could read it
from. The re-add made on the account is lost, and the track is still in the
collection.

**Closes when:** the provider exposes when a track was added to a playlist and
the snapshot records it. Ledger only.
