---
title: tag suggest asks Beatport again every day about rows Discogs was not asked about, and keeps a general catalogue decline from Discogs for a week
found: at the review of #673, U244, round two, 2026-11-12.
issue: no
---

**The mechanism.** A row unread only because Discogs had no token is kept for
the day and is no longer a reason to stop the walk, so with no token every
unresolved row is asked of Beatport on every day `tag suggest` runs, where
before U244 the walk stopped after three. And a row the general catalogue
declined with no token recorded is kept `declined` for seven days, so a token
recorded the next day is not asked about it until the eighth. Since round two
a row kept as passed over is asked again once a token is recorded.

**Measured cost.** Driven at round two: 40 rows with no token sent 40 paced
Beatport searches on each of four days; the declined row was asked of Discogs
on day seven. No false statement either way.

**Closes when:** a kept answer records whether Discogs could be asked, and the
walk keeps a per day budget for rows only passed over. Ledger only.
