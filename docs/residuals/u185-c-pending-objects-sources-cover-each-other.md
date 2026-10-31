---
title: Four layers of the DEADCA7 guard kill no test, each covered by another layer
found: at the reviews of #392, U185, 2026-10-31.
issue: no
---

**The mechanism.** The guard asks two ways, and some of its layers answer only what another already answers. In `rb_writer.pending_objects`, dropping the buffer's `move` branch, or the `session.dirty` loop, leaves every U185 test green, because the other source reports the same object. In `foreign_tree`, the `delete` branch of `pending_touches` is reached only after the additive whitelist has refused the hard delete, and the changed columns branch of `differences` is reached only by a raw column change on a row below the folder, which no test makes; a raw rename of the folder itself is refused, but as every row of the folder being gone, since a renamed root is no longer a foreign root on the second reading.

**Measured cost.** None to a person: every touch the two review rounds drove is refused with nothing written. Measured as zero death rows in the review rounds' own mutation passes; the refusal's wording for a raw rename names a disappearance rather than a rename.

**Closes when:** a test drives a touch only one layer sees for each: a write the binding makes with its tracking off, a raw session change, and a raw column change on a pushed playlist. Ledger only.
