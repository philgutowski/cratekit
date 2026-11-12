---
title: Four other verbs still open a file once per tag field they read
found: at the review of #695, U266, 2026-11-12.
issue: no
---

**The mechanism.** U266 made the set builder's index read its seven fields
through one `tags.read_tags` open. Four other places still ask
`tags.read_tag` for each field and so open the file again per field: the
naming plan in `write/naming_cli.py` (title, then the initial key), the
catalogue genre pass in `tagging/tag.py` (artist, then title), the retag
candidate search in `tagging/retag.py` (artist, then title) and the staging
read in `tagging/guess.py` (artist, then title). Each is two opens where one
would do.

**Measured cost.** Not driven; read from the code at the review. Twice the
container opens of one read in each of those batch verbs, which matters on a
library on an external drive.

**Closes when:** each reads its fields through one `tags.read_tags` call with
the answer proven equal and the open count as the assertion, the way U250 and
U266 did. Ledger only, until a speed survey measures one of them on the real
library.
