---
title: A title of brackets alone misses its own row when the row adds a feature, a dash suffix or punctuation
found: at the review of #713, R-1534, round one, 2026-11-12.
issue: no
---

**The mechanism.** Since R-1534 a title made only of bracket groups,
"(Intro)", is compared exactly by its words, never by containment, since a
word out of a bracket is contained in too many titles. So it matches "(Intro)",
"Intro" and "Intro (Original Mix)", and misses its own recording listed as
"Intro feat. X", "Intro - Original Mix", "Intro." or "[Intro]". A title that
opens with punctuation and a bracket, "- (Intro)", misses "Intro", and square
brackets are not read as brackets at all ("[Not Just] Knee Deep (Part 1)").
A title that opens with bracket groups keeps them in its core, so "(Not Just)
Knee Deep (Part 1)" misses "Not Just Knee Deep feat. X" while it finds "(Not
Just) Knee Deep feat. X" (round two).
Before R-1534 these matched, but only because such a title matched every row
by the artist, so the right row was taken by its order in the page.

**Measured cost.** Driven at round one through `tag_one`: "(Intro)" against a
Beatport row "Intro feat. X" writes nothing where the base wrote that row's
genre. A miss, so the file is offered to the next source and the general
catalogue; no wrong data. Not measured: how often a catalogue lists a bracket
title with an added feature.

**Closes when:** a bracket only title also matches a row whose own core,
with a feature or dash suffix taken off, equals its words, driven against the
R-1534 tables so no different recording matches. Ledger only: the cost is a
miss.
