---
title: A pair sync that fails part way through the account's reorder replays the half order as the account's
found: at the review of #298, U130, 2026-10-10.
issue: no
---

**The mechanism.** The pair snapshot moves only when the whole pair was
written, so a sync that fails part way through `order_tracks` leaves the old
snapshot. When rekordbox led the order, the account now stands half reordered,
and the next sync reads both sides as changed in order and follows the
account's, which is the half order.

**Measured cost.** Not driven: it needs a provider failure between two moves.
No track is added or removed by it, only the order, and a later reorder on
either side puts it right.

**Closes when:** a failed account reorder records the moves that landed, or the
next sync reads an account order that is a prefix of the planned one as
unchanged. Ledger only.
