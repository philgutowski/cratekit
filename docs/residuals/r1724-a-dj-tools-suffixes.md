---
title: The naming suffixes DJ_tools once wrote beside _PN were not read, since DJ_tools is not in a cloud container
found: at the build of #883, R-1724, 2026-11-21.
issue: no
---

**The mechanism.** The brief asks that any other suffix the naming verb or
DJ_tools once wrote be checked against DJ_tools' naming docs, read only,
and handled as `_PN` is only if it is the same kind of marker. DJ_tools is
not cloned into a cloud container, so its docs could not be read. Cratekit's
own code, docs and ledger name only `_PN` (R-168's and R-1192's samples,
sitting 101's count), and Cratekit's naming verb writes no suffix of its
own (`_mastered.flac` and `_set` are the mastering tool's output names, not
a library name's tail). So `titles.name_title` reads `_PN` only, exactly
and case sensitively.

**Measured cost.** Not driven. A library name ending in another such marker
is asked and matched with it, as on main.

**Closes when:** a local session greps DJ_tools' naming docs and code, read
only, for every suffix it wrote after a title, and either finds none other
or a card adds each to `titles.NAME_TAIL`'s reading. Ledger only.
