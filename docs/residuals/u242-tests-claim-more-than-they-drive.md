---
title: Some U242 tests build the strip's record by hand or call a private reader, and two fix guards kill no test
found: at the review of #671, U242, round two, 2026-11-12.
issue: no
---

**The mechanism.** `test_a_legacy_archive_mark_a_strip_superseded_no_longer_holds_the_rename`
seeds the strip's record by hand and calls `set_cli._standing_mark`;
`test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before` hand
lists two kinds of playlist. Round two's mutation of the fix found the stamp's
"not already stamped" test and the supersede test's time half killing
nothing; the second has a test since, the first is harmless by reading (a
second stamp writes a later time over a stamp already there).

**Measured cost.** None direct; the wiring a later change could drop is
named here and in `docs/mutation/u242.md`.

**Closes when:** each is driven through `sync strip` and `export set
--rename` end to end. Ledger only.
