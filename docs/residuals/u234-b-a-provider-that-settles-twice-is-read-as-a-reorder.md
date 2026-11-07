---
title: A provider that serves one order steadily for five minutes after a stop and then another steadily for five more is read as the DJ's reorder
found: at round one of the review of #623, U234, 2026-11-07.
issue: no
---

**The mechanism.** The person's reorder after a stop is read from two
settled readings in different orders (`_moved_since_stop`). Each is settled
by agreement over `AGREE_AFTER`, U231's window. A provider that served one
partial state for more than the window and then another for more than the
window again would pass both, and the account would lead into rekordbox.

**Measured cost.** Round one's review drove the shape on the suite's fake
provider through U231's pending path (D3), with the window set to nothing:
before the fix round it wrote the second order into rekordbox; since the fix
round each order must settle on its own, and the drive finishes from
rekordbox. With the real window the producer is a provider whose served order
holds still for minutes twice and changes between, which no sitting has
measured: Sitting 86 measured reads seconds apart that differ, not reads
minutes apart that agree and then move. Unmeasured, so a residual.

**Closes when:** a sitting measures whether a provider's served order after
a stop ever moves after holding still for the window. Ledger only.
