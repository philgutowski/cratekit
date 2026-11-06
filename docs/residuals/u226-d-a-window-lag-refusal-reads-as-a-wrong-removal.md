---
title: A removal stopped by a window that never caught up carries a wrong removal's cause and stops every later pair's write
found: at round one of U226's review (#578), 2026-11-06.
issue: no
---

**The mechanism.** When a removal's positions read or read back still finds
the window disagreeing with a partial unpaged read after the last pause,
`TidalAccount` refuses `outbound-remove-refused`, problem `window-lags` or
`read-back-differs` with `lagged: yes`. That cause is the one a removal
that may have taken the wrong track carries, exit 30 and not retryable,
though this one is a wait. `crate sync pair`'s `_write_account` stops one
pair alone only for an order's refusal, so the removal's refusal stops the
write of every pair after it.

**Measured cost.** Driven at round one through the verb with the fake
account raising the adapter's refusal: exit 30, the second pair's add
unwritten, the steps saying to wait and run it again. Since the fix round a
lag at the positions read is read again three times first. The live
producer, a partial unpaged read whose window lags for longer than the
pauses at a removal, was not driven.

**Closes when:** a lag refusal carries a cause of its own that a run reads
as a wait, and a pair's lagging removal stops that pair alone, as an
order's does. Ledger only: the run says to wait and run it again, and R-1343
records what the callers do not record of such a removal.
