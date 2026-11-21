---
title: tag folder still holds Deezer behind a refusing Beatport while the suggest verbs ask past it
found: at the plan of #891, U322, 2026-11-21.
issue: no
---

**The mechanism.** U322 gave `tag suggest --catalogue` and `tag backlog
--catalogue` their own binder, `published.for_suggestions`, which asks the
general catalogue on a row Beatport refused once Discogs answered. `tag folder`
keeps `published.for_taxonomy`, whose gate asks it only once Beatport answered
a match or a miss, the conservative option U281 built while #796's question
waits. So while Beatport refuses, a sweep records Deezer not asked on every
file Discogs missed, and `tag suggest --catalogue` asks it about the same
rows.

**Measured cost.** Not driven on the live library. The two verbs disagree only
on files Discogs missed while Beatport refused; the suggest verbs show what
they would write at a gate, and a sweep writes without one.

**Closes when:** #796's question is answered and `tag folder` follows it, or
U282 ends Beatport's refusal. Ledger only.
