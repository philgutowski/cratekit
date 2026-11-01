---
title: The install.extras row prints the install command twice on a copy that is not a release install
found: at the review of #378, U181, 2026-11-01.
issue: no
---

**The mechanism.** `crate doctor`'s `install.extras` row quotes the vocals module's sentence, which already ends with the install command, and then adds "Reinstall with:" and the command again. On a release install the second is the release form and the two differ; on any other copy they are the same text.

**Measured cost.** Seen on the real doctor output of an editable copy. Noise on one row; nothing false.

**Closes when:** the row quotes the reason without the command, or the probe's sentence and its command are carried apart. Ledger only.
