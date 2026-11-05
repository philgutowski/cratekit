---
title: A downloaded row the ledger already links to another account track is never tied to the track it was queued for
found: at the review of #494, U204, 2026-11-05.
issue: no
---

**The mechanism.** `account_mirror._read_edits` ties a queued track to the row
of its frozen ISRC (`mirror_downloads.landed`) and answers the row as that
track, unless the ledger links the row to another track, which round one's
fix made the rule so an owned row's release is never swapped. A landed row that
some other engine linked before organize read it is therefore never adopted.

**Measured cost.** Driven by review round two with a direct ledger write: the
account track stays named as awaiting its landing on every run. The real
producer, another engine linking a freshly landed row first, was not driven.

**Closes when:** the tie tells a row the download made from one the library
held before it, by the landing record that names the row. Ledger only.
