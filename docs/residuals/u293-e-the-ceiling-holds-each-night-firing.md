---
title: One night firing spends at most one command's ceiling, so a large pass takes two nights
found: at the review of #850, U293, 2026-11-21, round one finding 4.
issue: no
---

**The mechanism.** Built at first so the night's line stood in for the per command ceiling, one firing sent 1,200 calls where any other command stops at 500. The fix round made the firing's line the lower of the night's remainder and the ceiling, the conservative reading of "every line only lowers". A pass needing more than 500 calls, about a hundred tracks at sitting 100's 42 calls per ten, stops at the night's line and is continued by the next firing.

**Measured cost.** A pass over about 110 tracks lands over two nights rather than one unless the schedule fires twice a night. Not driven on a real account.

**Closes when:** Phillip decides whether a night firing may spend past `[provider] calls_per_command`, or U295 schedules a second firing a night.
