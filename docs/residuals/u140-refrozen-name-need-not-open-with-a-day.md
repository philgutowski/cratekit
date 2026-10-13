---
title: A refrozen set name need not open with a day, and the posted warning still reads its first word as one
found: at the review of #317, U140, 2026-10-13.
issue: no
---

**The mechanism.** `export set --rename` refreezes the name a person gave
the INSPIRATION playlist, which need not be the source system's dated
form. `set_playlist.ignored_posted` splits the frozen name and reads its
first word as the day it opens with, so after a rename to `Warehouse Night`
a later `intake land --set JOB --posted DAY` warns that the frozen name
"opens with Warehouse". The flag is ignored either way, since the frozen
name wins, so only the wording is wrong. Separately, `land_cli` looks an
INBOX batch up by the frozen name only when no landing recorded one, so a
second landing of a renamed set that recorded none would make a new INBOX
playlist under the new name.

**Measured cost.** Not driven. The warning names a word that is not a day;
the INBOX path needs a landing whose record carries no INBOX playlist,
which no candidate driven here produced.

**Closes when:** `ignored_posted` checks the first word is a day word before
naming it, and the author decides whether an INBOX lookup should try the
name before a refreeze. Ledger only.
