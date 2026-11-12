---
title: A full build of a label every track of which was removed creates an empty folder under its name
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** ``label playlists`` leaves out a year every playable track
of which was removed, and a full build of a label with no year left still
plans the folder: driven, the gate showed ``folder: Kompakt: create it`` and no
year, and the apply made an empty folder. A releases build already guards
against this and makes nothing.

**Measured cost.** An empty folder under the label's name on the account. The
input, a label whose every track was removed, was not produced by anything
driven beyond the fixture.

**Closes when:** a full build with no year to make makes no folder, as a
releases build does. Ledger only.
