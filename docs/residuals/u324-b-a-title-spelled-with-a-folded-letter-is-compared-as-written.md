---
title: A title spelled with a letter the name fold reads plain is still compared as written, so a credit now read past can cost the one match main made by misreading it
found: at the review of #919, U324, round one, 2026-11-21.
issue: no
---

**The mechanism.** U324 folds a maker's and a credit's name
(`titles._folded`), never a title, which `Title.same` compares by its
words as written: "Straße" and "Strasse", "Trentemøller Remix" and
"Trentemoller Remix" as titles are two titles, on `main` and on the branch.
Folding titles was left out on purpose, because a title's letters are
words of a language, and "Bøg" and "Bog", or "Sø" and "So", are different
words that a fold would join. Round two's reviewer counted, at `ba1231a2`,
6 lost pairs of this shape where `main` matched the file's own title
(round one's count, 12, was taken over a corpus one string shorter and
before the fix rounds): artist "Trentemøller", file
"Trentemoller - Sun Path - 02 Trentemøller Remix", row "Trentemoller
Remix". `main` matched only because it read the plain credit
"Trentemoller" as the title, which the row's core then met; the branch
reads it as the credit, as `main` reads the same name spelled one way
throughout, and the title "trentemøller remix" never meets the row's
"trentemoller remix".

**Measured cost.** 6 pairs over the differential's corpus, each a name
that spells the credit one way and the title the other; 45 more lost pairs
whose row is the file's title once folded are self titled shapes,
"Trentemoller - Trentemoller Remix", which `main` already misses spelled
one way ("Ame - Ame Remix"), so no regression. No real file of that shape was
found. A title spelled with ø against a catalogue row spelled plain misses
on `main` and on the branch alike.

**Closes when:** a title comparison reads these letters plain where both
sides are a name rather than a word (round two's smallest fix: fold a
title's word only where its folded form is a word of the searched
artist's folded names, so "Bøg" meets "Bog" only for an artist named
Bøg), or a measured decision that it never does. Ledger only: a miss, never a wrong genre.
