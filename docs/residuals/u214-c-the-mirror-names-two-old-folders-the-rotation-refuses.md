---
title: Two live folders named Old under INBOX are both named the Old folder by the mirror, while the rotation refuses the tree
found: at the review of #512, U214, 2026-11-05.
issue: no
---

**The mechanism.** `plan_rotation` refuses `intake-old-undeclared` when INBOX
holds two live folders of the declared Old's name, since a rotation that
targets the folder by name cannot tell them apart. `live_batches` refuses
nothing there and the mirror's INBOX step names both as "the Old folder".

**Measured cost.** Nothing false: neither folder is mirrored and both are
named. The mirror and the rotation disagree on whether INBOX is readable, and
only the rotation's refusal says why. Driven on a disposable database.

**Closes when:** the mirror's line for a second Old says the rotation refuses
the pair. Ledger only.
