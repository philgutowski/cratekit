---
title: A remix's Discogs search reads three releases ranked for its plain title, so a refusal can spend the cap before its own release
found: at the review of #882, U318, round one, 2026-11-21.
issue: no
---

**The mechanism.** `DiscogsAsker._search` asks Discogs for the title with
its last bracketed group set aside (`_last_group_stripped`), so a remix is
asked as its plain title, and reads the first `DISCOGS_RELEASES_READ`, three,
of the releases the search names. Before U318 the first plain pressing was
taken; since U318 a pressing without the file's mix is refused, so three
plain pressings ranked first spend the cap and a fourth release carrying the
remix is never read.

**Measured cost.** Driven on hand built answers: four search results, three
plain pressings and a fourth "Sunrise Mood (Remixes)" holding "Sunrise Mood
(Tide Remix)", through `tag_one`: a miss naming releases 1 to 3, release 4
never fetched. How often Discogs ranks the remix release past three is a live
service's order and unmeasured; a sitting recorded 43 releases for one title.
The cost is a miss, never a wrong genre.

**Closes when:** a remix's search asks with its mix (or reads further when a
named mix was refused), measured at the next attended tag sweep. Ledger
only: a miss is no board bar cost.
