---
title: The no token count includes a file its label tagged that was searched for its picture, and the blocked sentence counts searches never sent
found: at the review of #673, U244, round two, 2026-11-12.
issue: no
---

**The mechanism.** `discogs_without_token` leaves out files with the
`has-genre` skip reason, and a file its registered label tagged in the same
run, then searched only for its picture, carries no skip reason and is
counted. And after Discogs is remembered as blocked, the later files answer
BLOCKED from memory with no request, and the summary's "refused every one of
the N searches it was sent" counts them as sent.

**Measured cost.** Driven at round two through `tag_one` and the summary: the
count one file high; three files and one 429 read "the 3 searches it was
sent" where one was sent.

**Closes when:** the count reads whether a genre was owed, and a remembered
refusal is counted apart from a sent one. Ledger only: a count in a warning.
