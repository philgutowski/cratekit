---
title: Guards U317's fix rounds added that the review's mutations reverted with a green suite
found: at the round two review of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** Round two reverted each of these alone on a scratch copy
with every test in the five backup files green: an unreadable fact file read
as no reason in `_record_unpublished`; the root's device read again after the
walk; `still_removed` comparing the device and treating an unreadable path as
absent; an unconfirmed scan before the second database read; the archived
count over every quick command; the under a second bound; and the doubt count
inside `changed`. Each was then driven by hand and holds on the branch.

**Measured cost.** None today; each can be reverted with a green suite. The
unit's own table, `docs/mutation/u317.md`, measures its 25 rows against the
whole suite and names its own zeros.

**Closes when:** a test pins each. Ledger only.
