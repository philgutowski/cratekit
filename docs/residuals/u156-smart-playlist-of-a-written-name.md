---
title: The set playlist and the INBOX batch playlist find a smart playlist of their name and fail at the write, after the moves
found: at the review of #337, U156, 2026-10-28.
issue: no
---

**The mechanism.** `set_playlist._named_playlist_row`, `native._batch_playlist_row`
and `native.live_inbox_named` skip a folder and a removed node and take any
other node of the name under the parent, a smart playlist included. The
binding refuses a membership in a smart playlist, so a set's INSPIRATION
playlist, or an INBOX batch playlist, whose name a smart playlist already
carries under the same folder fails at the write, when the files are already
in the library. U156's label filing refuses the same shape before the gate
(`label_filing._of_kind`); these three were left as they were, since they are
outside the unit.

**Measured cost.** Driven for the label filing only, at the review of #337:
the landing refused with `internal-error` after the moves, its files in the
library, no row added. For these three, read and not driven; a smart playlist
named exactly as a set or a dated INBOX batch is unlikely and was not
measured on a real library.

**Closes when:** the three take a plain playlist only and refuse a smart one
by name before the gate, the way the label filing does. Ledger only.
