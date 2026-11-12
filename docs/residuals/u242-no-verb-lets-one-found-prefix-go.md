---
title: No verb lets a playlist the migration found prefixed go, so a hand marked playlist cannot be made new again short of editing the mark record
found: at the review of #671, U242, round two, 2026-11-12.
issue: no
---

**The mechanism.** `crate sync unmark` releases only what a pass took, and
since round one a playlist `sync taken` recorded as `found-prefixed` under
`migration` is no pass's, so no unmark lets it go. That was the fix for round
one's third blocker, which released every hand mark at once and offered them
all as new. The review drove three routes after the strip, `--pass migration
--playlist ID`, an unmark of `prefix-strip` with the prefix then taken off by
hand, and a plain retitle: none releases it. Before U242 a person could make
such a playlist new by taking the prefix off by hand.

**Measured cost.** A person who wants one hand marked playlist offered by a
sync again has no verb for it. Nobody is told anything false: the guide says
no unmark lets one go.

**Closes when:** Phillip decides whether naming one playlist should let it go
(`sync unmark --pass migration --playlist ID`, with its own gate), and it is
built. Ledger only.
