---
title: A Bandcamp fetch holds a track by its number only when the file name begins with the release's own artist and title
found: at the second review of #357, U176, 2026-10-28.
issue: no
---

**The mechanism.** `bandcamp_cli.number_in` reads the track number only after
the prefix `band_name - item_title - `, which round one made strict so an album
titled with a leading number no longer held every file. A release whose file
names spell the album differently from `item_title` (a slash written as a
hyphen, say) gives no number, so the plan's hold by track number does not
apply and only the file's own tags can hold it back.

**Measured cost.** Driven with a fixture: an untagged file of an owned track,
under a title Bandcamp would have to rewrite, is staged again. A duplicate in
staging, never a loss; the landing finds it owned. Whether Bandcamp rewrites
characters in file names, and whether a release arrives untagged, is
unmeasured: sitting 46's 96 files carried their tags.

**Closes when:** the attended run reads a release whose title holds a
character a file name cannot carry, and either the prefix is read with the
same rewrite or the hold falls back to the track's title. Ledger only.
