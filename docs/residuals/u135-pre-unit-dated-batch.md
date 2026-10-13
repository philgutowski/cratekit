---
title: A pre-unit --set landing with no set playlist record cannot name its dated INBOX batch as a leftover
found: at the review of #309, U135, 2026-10-12.
issue: no
---

**The mechanism.** `leftover_set_inbox` finds dated batch playlists from before
U135 by walking closed sessions whose set playlist record names this job and
whose batch playlist detail carries no `job` key. A pre-unit `--set` landing
whose set playlist wrote nothing (every member left out) never wrote a set
playlist record, so that walk cannot name the dated INBOX batch it did make.
The later landing then makes a set-named INBOX playlist beside the dated one
without listing the dated name under inbox leftovers.

**Measured cost.** Edge: only landings that wrote the INBOX batch and wrote
nothing under INSPIRATION. Not driven.

**Closes when:** `leftover_set_inbox` also walks batch playlist details that
name the set without a set playlist record, or the operator renames the dated
batch by hand. Ledger only.
