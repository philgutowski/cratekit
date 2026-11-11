---
title: crate sync land lands whatever the staging folder holds, a label go's download included, under the sync pass
found: at the review of #655, R-1467, 2026-11-11.
issue: yes
---

**The mechanism.** R-1467 made `label sync --go` refuse while the staging
folder holds anything that is not its own download. `crate sync land` has no
such read: its tail runs `name apply` over the whole folder and its landing
takes every file there, so a label go's download waiting at its landing's
gate (renamed, unlanded) is landed under the sync pass's manifest and pass,
and the label go's own landing is left with nothing.

**Measured cost.** Driven at the review's round one
(`test_rv9.py::test_s8c`): go A to its landing's gate, then `crate sync
land`, its landing decided and applied: "4 file(s) are named in
..._synced_inboxed.xml", A's two tracks filed in the account playlists'
batch folder. The label's tracks are filed under the sync pass and no label.

**Closes when:** `sync land` reads the folder the way `label.go.beside`
does and refuses beside another download's tracks or files no download
names, naming how each lands. Earns an issue: the product files a DJ's
tracks under the wrong pass, the mirror of R-1467.
