---
title: A row passed over for a token Discogs refused loses what the searcher knew of Beatport, so its line leaves Beatport out and Deezer is never asked
found: at the review of #891, U322, round two, 2026-11-21.
issue: no
---

**The mechanism.** When Discogs refuses the recorded token and no record shop
matches, `catalogue_searcher` raises the credential refusal and drops every
other catalogue's answer. Since U322 `suggest.catalogue_lookup` reads that
refusal by its declared reason as Discogs passed over, so the walk goes on,
but its words are only Discogs `not-asked`: `tag backlog`'s catalogue line has
no Beatport entry whether Beatport refused or answered, and the general
catalogue's seam never runs, so Deezer is asked about no row. The review drove
six rows each way and eight with Beatport missing: Deezer asked 0 times where
the same library with no token is asked 8.

**Measured cost.** The warning names the refused token and says how to record
a new one, so a person is told the cause; what they are not told is Beatport's
part, and the rows take no Deezer genre until the token is fixed.

**Closes when:** the searcher carries the shops' answers on the credential
refusal as a declared field, or returns a decline that names Discogs passed
over for a refused token, so the lookup reads the words and offers the row to
the general catalogue. Ledger only.
