---
title: A stop between a landed export batch and its ledger write leaves up to a hundred tracks the ledger never records
found: at the review of #699, U270, 2026-11-13.
issue: no
---

**The mechanism.** R-1543 a batch at a time. `export.apply` records a batch's
tracks once `add_tracks` answers. A kill, or a provider gate park at the
client's read after the POST, between the request and that write leaves every
track of the batch on the playlist and none recorded; the resumed batch finds
them on the playlist and reports them as already there. Recording the rows
sent before the request and settling them on the next read was built and
taken out at round one of the review, because that read cannot tell a landed
add from a person's own add of the same track. A question for Phillip on #699
asks whether he wants that settle back.

**Measured cost.** Driven by round two of the review with a park after the
POST through the driver, 100 tracks: 100 on the playlist, none twice, 0
recorded, counts `written 0, already 100`. A prune after one of those rows
leaves the crate takes nothing off. Before U270 the same stop cost one track.
A refused read after the POST no longer reaches it: `add_tracks` reopens and
reads back on its retry.

**Closes when:** a track a stopped batch sent is recorded on evidence that
tells it from a person's add, or Phillip answers that the later read is
evidence enough. Ledger only: the cost is a prune that leaves a track.
