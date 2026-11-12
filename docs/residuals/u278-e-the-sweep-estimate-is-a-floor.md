---
title: The label sweep's estimate counts kept answers rather than pages and only label sync says one
found: at the build of #741, U278, 2026-11-12.
issue: no
---

**The mechanism.** `label sync`'s estimate before a walk over every followed
label counts one call per aged kept answer, but a listed answer of many pages
costs a call a page, and a label with no kept listing is estimated at the
mean of the kept ones (or 100). Only `label sync --next` without `--label`
and its interactive walk say an estimate; the retired `sync labels` resume,
`label import` and any other verb that lists a label's whole catalogue say
none. The hour's line still stops each of them call by call.

**Measured cost.** Not measured on a real catalogue. A low estimate lets a
sweep start that the hour then stops part way, which keeps what it read; it
cannot spend the reserve.

**Closes when:** a kept listing records the calls its pages cost and the
estimate reads that, and every verb that walks every label shares the one
estimate. Ledger only.
