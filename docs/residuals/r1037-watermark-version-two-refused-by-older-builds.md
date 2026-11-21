---
title: A deletion watermark written at version 2 is refused by every build before R-1037, sync removed's first position included
found: at the review of #913, R-1037, round one, 2026-11-21.
issue: no
---

**The mechanism.** R-1037 keeps the number each absent landed row is given in
the deletion watermark's document, so it writes version 2. A build before it
reads only version 1 and refuses anything else (`deletion-watermark-unusable`,
"it says version 2 and this build writes 1"). `crate sync removed` gives the
pass its first position through the same store, so its document is version 2
too.

**Measured cost.** The review loaded the base's `watermark.py` against a
document the branch wrote and drove the refusal. A refusal, nothing lost: an
older install asked to run `delete review` or `sync removed` against a library
a newer one already read stops and says why. No mixed install was driven.

**Closes when:** every install that reads the library carries R-1037, or a
reader of version 2 is backported. Ledger only: a refusal over an unusual
install is the intended answer of a versioned document.
