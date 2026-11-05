---
title: The account's added date of a track a playlist lists twice is its first mention's
found: at the review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `intake.cli.list_playlist_dated` keeps the first mention's
date for a track a playlist lists twice, as the frozen rows keep the first
mention. The provider dates each item, so a second copy added later never
moves the track's date and never reads as the track put back on the account.

**Measured cost.** Not measurable in the harness, whose fake account dates
per track; a mutation to the last mention killed nothing. A duplicate added
later reads as unchanged, so a rekordbox removal of the track is applied as
before U202 rather than weighed against the addition.

**Closes when:** a pair reads the latest date among a track's items, with a
test whose fake dates each item. Ledger only.
