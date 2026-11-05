---
title: The native landing lookups read an unlisted session log as no landing, so sync mark sends a person to land a pass that landed
found: at the review of #526, R-1255, 2026-11-05.
issue: yes
---

**The mechanism.** `native.landed_passes` and `native.landings_of_pass` read
`session.scan_log` and drop its unread half by their own policy. Since R-1255
an unlisted log is that half, so both answer no landing over a log holding a
closed committed one. `crate sync mark --pass` then refuses with "no landing
of the pass into the database native intake tree committed" and names
`crate intake land` as the way on (`sync/mark_cli.py`, the native branch).

**Measured cost.** Driven at the function level in round one: a closed native
record naming the pass answered `()`, its readable twin the session id and
the pass. The verb's message was not driven. `crate intake land` then refuses
at its gate, so nothing is written, but the product says something false and
names the wrong remedy, the board bar's (b).

**Closes when:** both lookups refuse on `session.log_unlisted`, or their
callers say the log could not be listed, with a dispatcher test of
`crate sync mark --pass` over a refused listing beside its readable twin.
