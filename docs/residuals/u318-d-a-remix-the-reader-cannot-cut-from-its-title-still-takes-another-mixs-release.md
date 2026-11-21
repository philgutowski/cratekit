---
title: A remix written with no bracket, or with a feature credit after it, still takes another mix's Discogs release
found: at the build and review of #882, U318, 2026-11-21.
issue: no
---

**The mechanism.** `titles.named_versions` reads a version only from a
bracket group the title part ends with or the dash part after the title.
"Sunrise Mood Tim Green Remix", where only a list could cut the title from
the mix, "Sunrise Mood - Tide Remix feat. Sun" and "Two Months Off (Tim
Green Remix) feat. Tide - Artist", whose feature credit follows the mix, and
a remixer whose whole name is folded words, "(Mono Remix)", name nothing, so
they are matched as main matched them, another mix's release included.

**Measured cost.** Round one's shape drive: 9 of 1,056 names, all the
feature credit after the mix, still take the four other mixes release, as on
main. Not new; a wrong genre where main wrote the same one.

**Closes when:** the reader reads a version before a trailing feature
credit and the unbracketed shapes have a rule that is not a list. Ledger
only: no cost beyond main's.
