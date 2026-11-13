---
title: Setup says it is checking a Discogs token it then refuses to send for its shape, and a relink's last note drops an earlier refusal
found: at the review of #799, U283, 2026-11-13.
issue: no
---

**The mechanism.** `_link_discogs` writes "Checking the token with Discogs..."
before `searchers.check_discogs_token`, which refuses a token that is not one
printable word without a request, so the line precedes a refusal that says
it was not sent. Separately, when one try is refused with a 401 and a later
try meets an outage on a relink, the final note names the outage only.

**Measured cost.** Driven by round two's reviewer with "two words", "x y"
and "a b": each printed the line and then "it was not sent to Discogs".
Nothing stored, nothing leaked; a wording cost only.

**Closes when:** the line is written only for a token that will be sent, and
a relink's final note names any earlier refusal. Ledger only.
