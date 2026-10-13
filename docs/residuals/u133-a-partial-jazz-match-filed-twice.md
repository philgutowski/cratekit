---
title: A partial "jazz" genre already in NonElectronic's default sub is filed in a Jazz band and left in Rock
found: at the review of #308, U133, 2026-10-12.
issue: no
---

**The mechanism.** U133 moved the keyword rule `keyword = "jazz"` from the
non electronic bucket to the new Jazz bucket, as the author's brief named,
unlike R&B's and Hip-Hop's (R-804, R-941). Before it, a genre that only
contains the word, such as `Acid Jazz`, `Jazz Funk`, `Jazz House` or
lowercase `jazz`, routed to NonElectronic by the keyword, had no row in its
source map, and landed in the default sub, Rock. It routes to Jazz now. Rock
is not a place Jazz competes on, so adoption files such a track into a Jazz
band, applicable and not withheld, and `crate adopt move` plans nothing for
it: the track sits in Jazz and in NonElectronic / Rock, and no verb settles
it. The rule also sits before `house` and `hip hop` in first match order, so
`Jazz House`, `Jazzstep` and `Jazz Rap` file as Jazz rather than in a dance
or Hip-Hop folder; before U133 they landed in Rock, also not their folder.
Pinned by `test_a_partial_jazz_match_already_in_rock_is_filed_in_jazz_and_stays_in_rock`.

**Measured cost.** Driven on the shipped template through the adoption plan
and the move plan with a placement reader holding the track in Rock. How
many live tracks carry such a genre is unmeasured, since the unit does not
read the live library. The brief counted 15 rows with the genre Jazz and 15
tracks in NonElectronic / Jazz, which are exact matches, not this
population. The live copy is not affected until its own keyword rule is
repointed by hand: `crate taxonomy upgrade` adds the bucket and leaves the
copy's rule, and says so.

**Options.** (a) Leave it, and count the population with `crate report
genres` at the attended tail before repointing the live copy's rule. (b)
Declare NonElectronic's default sub a split place of Jazz for tracks whose
genre names Jazz, so the move takes them out of Rock. (c) Put the keyword
rule back on NonElectronic and add only the wanted spellings as exact Jazz
aliases. (d) Move the rule below `house` so `Jazz House` files as house.

**Closes when:** the author chooses, with the live count in hand. Not on the
board bar: nothing is lost, nothing false is said, and the live copy keeps
its old rule until a person repoints it.
