---
title: A file an earlier pass staged lands under the later pass's name, so that pass's heart months and gate are not its own
found: at the build of #506, U212, 2026-11-05.
issue: no
---

**The mechanism.** `crate sync land` lands everything a landing would take
from the download staging folder, with `--pass` naming the pass that ran it.
Since U212 a later pass skips the tracks an unlanded earlier pass staged and
lands them over that folder under its own pass name. The heart month filing
(`account_playlists.hearted`) reads only the landing pass's hearts, so a
staged file the earlier pass's hearts asked for, and the later pass's did not,
is given no heart month there. The earlier pass's landing gate, never
answered, is now stale: its folder changed.

**Measured cost.** Not driven. The landing of every file staged was already
the behaviour before this unit for any landing over that folder; U212 makes
the path the normal one when an earlier gate is left open. Landing or
abandoning old open gates is out of the card's scope.

**Closes when:** a landing over a staging folder holding another pass's files
names that pass's hearts too, or the old gate is answered or abandoned first.
Ledger only.
