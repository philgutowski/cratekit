---
title: The content floor passes a root holding exactly a tenth of the census, so one stray file at the mount point of a ten file library is mirrored as the library
found: at the round one review of #893, R-1761, 2026-11-21.
issue: no
---

**The mechanism.** `_unproven` refuses `held * LIBRARY_FLOOR < had`, a root
holding under a tenth of the files the census counted. A library of ten
files or fewer and one stray file at its mount point is held to the floor
and passes, and the full sync archives the mirror.

**Measured cost.** Driven at the engine with a ten file census and one stray
file written by hand: 10 mirror files archived. Bounded to libraries of ten
files or fewer, and no producer of the stray file was found.

**Closes when:** the floor also asks for a minimum number of files, or the
census's own paths, at a library this small. Ledger only.
