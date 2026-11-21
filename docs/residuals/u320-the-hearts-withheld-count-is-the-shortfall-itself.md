---
title: The provider publishes no withheld count, so a heart lost to a fault within a tenth of the hearts' count reads as withheld and sync removed can offer past it
found: at the build of #889, U320, and its review round one, 2026-11-21.
issue: no
---

**The mechanism.** The card asked for the hearts to be read whole when short
"only by the count the provider declares it withholds". The provider declares
one count, the total; `HeartsShortfall.withheld` is that total less the rows
served by a walk that reached it. So nothing tells a heart the provider will
not serve from one a fault dropped inside a window, or one skipped at a page
boundary by a heart removed while the walk ran. `sync.removed.read_hearts`
reads the hearts whole (`withheld`) when at least one heart was served and the
shortfall is at most a tenth of the declared count (`WITHHELD_AT_MOST`); a
larger shortfall, or none served, stays short and stops every offer.

**Measured cost.** Driven on fixtures by review round one with no bound: 349
declared and 100 listed read whole, and a hearted track on the lost page was
offered. With the bound that shape stays short (tested). Inside the bound, a
lost heart that is also a removed downloaded track would be offered at the
gate; unmeasured live, and the provider has not been seen serving an empty
window with a success status. The bound is the build's call on a question
posted on the card under its question heading.

**Closes when:** Phillip answers the question on #889 and the bound matches
his answer, or the provider is found to publish which hearts it withholds.
Ledger only.
