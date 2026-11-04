---
title: sync pair's discovery leaves out a registered tree root by its identifier, and no test pins it apart from the name
found: at the mutation table of #483, U198, 2026-11-04.
issue: no
---

**The mechanism.** `pair_discover.discover` leaves out a node the tree registry records as a root, and separately a top level node carrying a name the taxonomy declares. Every test tree names its roots by the taxonomy, so the identifier check is masked by the name check: row D1 of `docs/mutation/u198.md`, reverted alone, kills nothing over the full suite.

**Measured cost.** Not driven. The input is a Cratekit tree root renamed in rekordbox away from its declared name, which the registry still records; with the identifier check gone its playlists would be paired with the account. The check is in place, so nothing is paid today.

**Closes when:** a test registers a root under a name the taxonomy does not declare and shows its playlists are never discovered. Ledger only.
