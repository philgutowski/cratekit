---
title: Seven guards of the kept label listing kill no test, each costing provider calls or a line's wording at most
found: at the review of #533, U217, rounds one and two, 2026-11-05.
issue: no
---

**The mechanism.** The review reverted each guard of the branch alone and
these left the label suites green: the two counts of an answer about an artist
with no identifier (`_member_named` and `_listed`), which cover each other;
`_Member` reading its provider object once; a kept name answer holding at most
one artist; `KeptListing.has_listing`'s age check; discovery's kept "no such
artist" answer skipping the read; `release_row`'s fallback from `copyright` to
`label`; and `_year` keeping an integer year.

**Measured cost.** Driven by the reviewer on the fake client for each: an
extra provider call or two per run, or the same line with a stale count; no
false report, lost row or wrong release reached a person. The id less pair is
reachable only on a client whose artists carry no identifier, which the live
provider's do.

**Closes when:** a test pins each, one per guard. Ledger only, a maintainer
facing gap.
