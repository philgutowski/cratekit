---
title: METHOD's opening still calls Native Relay live, though its own Relay section says it retired on 2026-10-27
found: at the review of #395, U187, 2026-11-01.
issue: no
---

**The mechanism.** `docs/METHOD.md` says in its opening paragraph that Native
Relay "is in the loop" and points at "Relay below", and the board bar section
still says "The Relay feeder picks up" cards and "Relay reads every card it is
about to launch". The section those point at is headed "Relay, retired
2026-10-27". U187 added a flagged ambiguity to `CONCEPTS.md` separating Native
Relay from the decisions relay thread, and left these lines alone because the
brief names only the decisions page paragraph of METHOD.

**Measured cost.** None to a DJ. A session reading METHOD from the top meets
Relay as live on its first page and retired further down; the later section
and the cloud lane section are both right. Found by a grep for "Relay" over
METHOD, not driven further.

**Closes when:** the opening paragraph and the board bar lines say Relay is
retired, or speak of the cloud lane instead. Ledger only: a wording fix in a
maintainer document.
