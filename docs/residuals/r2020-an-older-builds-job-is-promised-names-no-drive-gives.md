---
title: a resort job an older build queued is told at its gate that the drive names the playlists not compared, and a drive over an older build's item reports names none
found: at the review of #1036, R-2020, round two, 2026-11-24.
issue: no
---

**The mechanism.** `routing_cli.UNRECORDED_UNREAD`, the gate's line over
facts frozen before R-2020, says "the drive names any it finds". A job the
older build already finished, or that this build finished, has no drive left,
and `--job` answers `ok succeeded` with no warning. And `rebuild.after_messages`
reads an item report with no `unidentified` key, which an older build's resort
worker wrote, as nothing unread, so a job left open with one tree done by the
older build names no unread playlist for that tree on either exit.

**Measured cost.** Driven: the base queued a job, this branch drove it (named
the playlist), and a second `--job` showed the gate's promise over a job no
drive was left for. A job the base itself finished was not produced (its
worker refused on volume identity in the harness). The second shape was
driven only with a stand in report; its producer needs two routed trees or a
crash window, and the shipped taxonomy derives one tree. The gate's line
already says the count may leave some out, so neither is a clean report.

**Closes when:** the line says a drive still to run names them, and a report
without the key is named as one that did not record them. Ledger only; it
closes by itself once no job queued before R-2020 is open.
