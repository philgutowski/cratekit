---
title: The page title is used whole as the set's name when no flag abbreviates it
found: by the author of U121, 2026-10-09, naming the Vonking set.
issue: no
---

**The mechanism.** The form asks for an abbreviated set name, and the page
title is what the uploader typed: `Public Service NYC - Live at Vonking
05.03.26` gives, less the uploader's name in front, `Live at Vonking
05.03.26`, so the playlist would read `10_09_26 Public Service NYC Live at
Vonking 05.03.26 5-26`, the date twice. The strip rule takes the uploader's
name off the front with its separator and nothing else; a title that names
the uploader elsewhere, or a date, keeps it. `--set-name` is the abbreviation
and wins.

**Measured cost.** A longer playlist name than the author would type, for a
set landed from an address with no `--set-name`. Driven by
`test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`.
No playlist is misnamed in a way that loses it.

**Closes when:** the author decides a rule for abbreviating, which the brief
left to the flag. Ledger only.
