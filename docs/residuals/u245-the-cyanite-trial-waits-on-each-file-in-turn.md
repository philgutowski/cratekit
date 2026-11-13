---
title: The Cyanite trial waits on each file's analysis before uploading the next, so a run of forty files can take hours
found: at the build of #674, U245, 2026-11-13.
issue: no
---

**The mechanism.** `tagging/cyanite.py` uploads a file, makes its library
track, and polls its analysis every ten seconds for up to five minutes before
it uploads the next. A file still unfinished after the window is kept,
pending, for a resumed run.

**Measured cost.** Not measured against the service. At Cyanite's stated
analysis time of about a minute a track, forty files take about forty
minutes; at the window's worst, over three hours. Nothing is lost or paid
twice either way, since every made track is written down before its wait.

**Closes when:** the attended trial measures the time a track takes, and, if
it matters, a later card uploads every file first and then polls them
together. Ledger only.
