---
title: tag second judges a row by its file's genre while adoption files it by the row's
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/second.py` reads the file's genre to decide
`genre-names-that-folder` and `genre-names-no-folder`; adoption's census
routes by the row's genre. Where the two disagree the verb's outcome and the
filing disagree (seam rule P2).

**Measured cost.** Driven at round one on seeded rows: a blank row genre with
file genre Deep House was written and told `crate adopt apply` files it, and
adoption read it as needs-genre and filed it nowhere; a row genre Deep House
with a blank file genre was left as `genre-names-no-folder` while adopt apply
files it by the row. The producer of a disagreeing row (an unfile on the
account) was driven for its file half only.

**Closes when:** the verb judges by the census's row genre, the one adoption
files by. Ledger only.
