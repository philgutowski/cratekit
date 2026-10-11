---
title: The nested Sets and Labels folder scheme was considered and deferred
found: at the build of #299, U131, 2026-10-10.
issue: no
---

**The mechanism.** U131's brief proposed `Sets / <year>` and `Labels / <Label>`,
one level down. The label step, the set archive and U116's filing all find
their folder by name at the account root, the seam creates a folder only at
the root, and `move_to_folder` moves a playlist and never a folder, so the
existing year and label folders could not be put under a parent. U131 kept the
root shapes and added root `Mine` and `Exports` folders.

**Measured cost.** Not driven. The account's root holds one folder per label
and per year beside `Mine` and `Exports`, rather than four parents.

**Closes when:** Phillip chooses the nested scheme, a seam member creates a
folder under a parent and moves a folder, and the three steps read under it.
