---
title: A maker named by the mix descriptions' words alone is read as no one, so their remix takes another mix's Discogs release as on main
found: at the review of #882, U318, round two, 2026-11-21.
issue: no
---

**The mechanism.** `titles._naming_words` folds `titles.MIX_DESCRIPTIONS`
off both ends of a version, so a maker whose name is only those words, "DJ
Deep", "DJ Promo", "Digital", "Final Cut", "Classic", is read as no one and
the file is matched as main matched it. And `writes_version` reads a titled
row's unbracketed whole by its last words, across a dash, so "Dixon Remix"
takes "Sunrise Mood - Alan Dixon Remix", and a fold can make one maker end
another's ("New Order" folds to "order" and meets "Out Of Order Remix").
With a refusal ahead of it on one result page, such a release can be the
one taken where main took an earlier one (round two's row 4).

**Measured cost.** Round two: 29 of 377 maker names it wrote are folded
away whole, 25 of them by the round one widening, "dj" alone 7; on 60,000
generated releases that never write the file's maker the fix took 4,579
where round one's head took 4,153. Against main nothing is newly taken at
the release level (0 of 330,000); round two's row 4, two crafted releases
on one page, writes House from the second where main wrote Techno from the
first. No such maker or pair was driven from a real library. The fold and
the misses of `u318-f` pull against each other: a word taken out of the list
buys back makers and loses the plain recording's mixes main matched.

**Closes when:** a description can be told from a maker by something other
than a list (Discogs' own credits, `u318-b`), or Phillip decides which way
the list should fail. Ledger only: no cost beyond main's for one release.
