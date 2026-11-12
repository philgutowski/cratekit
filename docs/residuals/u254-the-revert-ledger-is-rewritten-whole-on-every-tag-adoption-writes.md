---
title: The adoption revert ledger is rewritten whole on every tag adoption writes, so its bytes grow with the square of the files tagged
found: while building #683, U254, 2026-11-12.
issue: no
---

**The mechanism.** `revert.write_tag_with_record` takes the adoption lock,
reads the whole revert ledger, adds or stamps one record, and writes the whole
ledger back through `config.atomic_write_bytes`, once per entry whose tag an
apply writes. U254 made the applied ledger a journal and left this one as it
was, because its records are changed in place after they are written (the
digest stamp, the list of entries that wrote through a record), so an append
needs update records and a fold of its own, not the applied ledger's.

**Measured cost.** Driven on this container with `write_tag_with_record` over
synthesized FLAC files in a scratch library: 50 records wrote 1,479,470 bytes,
100 wrote 5,873,770, 200 wrote 23,417,570, about 582 bytes a record and four
times the bytes for twice the records. By the fit, and not run, about 17.6 GB
for the 7,773 entries of the cutover's live apply, if every entry wrote a tag.
Only an apply that writes tags pays it; a membership only apply writes nothing
here.

**Closes when:** the revert ledger records each tag write without rewriting
itself whole, on a card of its own, with the same byte count test U254 uses.
Ledger only: a speed cost, none of the board bar's four.
