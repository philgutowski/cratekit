---
title: An answer recorded before the spelled out lookup reads differently once it adds a candidate
found: at review round one of #833, R-1705, 2026-11-15.
issue: no
---

**The mechanism.** A review answer is read against the candidates the
matcher offers now. Where card 833's lookup adds a candidate to an item
answered before it landed, the answer meets an offer it was not given. A
yes recorded without naming a candidate, over `Prince - Luv U` offered only
`Luv Us`, matched on main and now reads `needs_review` with
`verdict-unspecific` once the library's `Love You` joins the offer. A
rejection still reads `missing`, `verdict-rejected`, and downloads, and its
report lists `Love You` among the rejected candidates though the person was
never shown it.

**Measured cost.** A settled row reopens and needs `review clear` or a new
answer; a row rejected before the change still downloads the copy this card
was meant to catch. Driven through `apply_verdict` in the review; how many
such answers sit in a real queue is unmeasured. It is the existing
behaviour of any change that adds a candidate.

**Closes when:** a sitting reads the review queue for answered
`title-approximate` items whose offer the lookup widened, or the answer
reader tells an offer widened since it was answered from one it was given.
Ledger only.
