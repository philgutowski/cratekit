---
title: A full label build parked by the breaker while its kept reads cannot be written does not say the reads were lost
found: at the review of #410, R-1091, 2026-11-01.
issue: no
---

**The mechanism.** When the provider's breaker parks a full `crate label
playlists LABEL` build, `_grouped` in `src/cratekit/label/playlists_cli.py`
writes the kept reads once more and, if that write fails, adds a note to the
park's exception. A note reaches neither the JSON envelope nor the human
output, so the person is told the park and not that the reads made before it
were not kept. The clean paths say it, on the build gate's screen and as the
warning `label-playlists-reads-unkept`; the park path is the one that does
not, because the park's cause is built by the provider gate and this module
does not rewrite it.

**Measured cost.** Driven by both review rounds: `FLUSH_EVERY` two, the
writer refusing with a full disk, the park after three reads; the envelope's
reason is `provider-cooldown` and the words "could not be kept" are nowhere
in it, and removing the note kills no test. The cost is calls only: the next
run reads those releases again, and nothing on the screen claims they were
kept.

**Closes when:** a park whose reads could not be written carries that on
what the person is shown, for example as a warning the dispatcher keeps on a
refusal, or the record says why a park's cause is not this module's to add to.
