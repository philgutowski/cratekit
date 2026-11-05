---
title: The account order's pauses and reread count are a bound, not a measurement of the provider
found: at the build of #543, U220, 2026-11-05.
issue: no
---

**The mechanism.** `tidal_account.ORDER_PAUSES` (1, 2 and 4 seconds) and
`ORDER_REREADS` (3) decide how long `order_tracks` waits for a reading that
lags a write before it refuses. They were chosen in the cloud with no live
provider. Three facts the card asked to be measured first are still not:
how long the provider's reads lag its writes, whether its tracks endpoint and
its playlist endpoint issue the same version tag, and where it lands a move
to the playlist's length. The adapter is built to be right under every
answer (moves go to the front, a 412 is read again, a lagging read back is
read again), so the cost of a wrong guess is a refusal that a continue
finishes, never a wrong move.

**Measured cost.** Not driven live. A provider lagging longer than seven
seconds a step leaves the pair unordered and named in the stop.

**Closes when:** the attended card U220 filed records the measurement on the
card and the constants are set from it, or confirmed. Ledger only: it closes
at an attended sitting.
