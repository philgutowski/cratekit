---
title: A downloaded file's date tag can carry the day the release became available, not the day it was released
found: at the review of #337, U156, 2026-10-28.
issue: no
---

**The mechanism.** `intake land --label` files each file under the year its
date tag names. The vendored downloader writes that tag from the album's
`available_release_date` when the provider gives one, and its `release_date`
only otherwise (`_vendor/tidal_dl_ng/download.py`, the metadata step). A
catalogue reissued or added to a service years after its release would then
be filed under the year it arrived, not the year it came out. A Bandcamp
purchase, the case the unit was cut for, is tagged by its own download and
was not read.

**Measured cost.** Not measured on a real file. The gate screen names every
file's playlist, so a wrong year is shown before anything is written.

**Closes when:** the year a `--label` landing files under is read from a
source that is the release's own date, or a sitting measures that the tag
agrees with the release year on the files the cloud lane lands. Ledger only.
