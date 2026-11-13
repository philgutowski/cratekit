---
title: The adapter's add_to_playlist and its held playlist have no caller in src after U270
found: at the build of #699, U270, 2026-11-13.
issue: no
---

**The mechanism.** `export.apply` was the one caller of
`RemoteAccount.add_to_playlist`, and U270 moves it to `add_tracks`. The held
playlist U255 built for it (`TidalAccount._held`, `_opened`) is now reached
only by `add_to_playlist`, which nothing in `src` calls, and by
`_membership`, which still holds what it opened. The attended card U255 owed,
A131 (#716), reads the 412s of adds through that held object from a live
`export playlist`, which no longer makes one.

**Measured cost.** None to a library: the code path is unreached. The cost is
a maintainer reading U255's held object as the export's path, and an attended
check that can no longer read what it asks for.

**Closes when:** `add_to_playlist` is given a caller again or is taken out of
the protocol, the adapter and the fakes, and A131's add checks are rewritten
to the batched add. Ledger only.
