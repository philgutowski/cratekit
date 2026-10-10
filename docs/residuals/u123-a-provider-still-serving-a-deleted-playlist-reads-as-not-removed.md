---
title: A provider that still serves a playlist just after accepting its delete makes remove_playlist report it not removed
found: at the review of #282, U123, 2026-10-10.
issue: no
---

**The mechanism.** `TidalAccount.remove_playlist` reads the playlist back after
the provider accepts its delete and refuses `outbound-remove-refused`,
`read-back-differs`, when it is still served. A provider whose lookup lags its
delete for a moment would be reported as having refused, the ledger entry would
not be dropped and no release would be marked heard.

**Measured cost.** Not measured: no live delete was made from this task. The
failure is the safe direction, a removal reported as not done, and a second run
then finds no playlist by the name in the folder, plans ABSENT, names the
ledger's identifier as possibly outside the folder, and marks the releases
heard.

**Closes when:** a live delete at an attended sitting shows whether the lookup
lags, and if it does, the read back waits and asks again before refusing.
Ledger only.
