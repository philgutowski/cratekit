---
title: The title matcher still reads a word cut out of a bracket, or a title cut short by the strip, as contained in another recording by the artist
found: at the review of #713, R-1534, round one, 2026-11-12.
issue: yes
---

**The mechanism.** R-1534 closed the empty title: a title the shared strip
empties, or one with no letter or digit, now matches nothing in
`tagging/searchers.py`. Three looser shapes of the same substring comparison
remain, all on the base before R-1534. A bracket in mid title still cuts the
title at its first bracket, so "Knee (Not Just) Deep (Part 1)" strips to
"knee", contained in "Knee Slapper". The containment between whole titles,
suffix and all, reads a bracketed word as the title: "Sunrise Mood (Intro)"
matches a row named "Intro", and Beatport's lowest tier scores that row. And
`_VERSION_WORDS` is a hand list: "vocal", "acapella", "mixed", "remixes",
"intro" and "reprise" are not on it, so a file titled "Vocal Mix" matches the
Bandcamp heading "Other Song (Vocal Mix)" where "Original Mix" is refused. A
title cut to one or two letters is R-1540's, on Discogs, and the same holds for
the other sources.

**Measured cost.** Driven at round one through the shipped parsers: Beatport
wrote the genre of the artist's "Knee Slapper" onto "Knee (Not Just) Deep
(Part 1)", the genre of the artist's "Intro" row onto "Sunrise Mood (Intro)",
and Bandcamp's onto "Vocal Mix". A genre is fill if empty, so each is written
for good. Not measured: how many files in a real library carry such a title.

**Closes when:** the strip keeps a title's text before a mid title bracket
when what follows it is not a suffix, the containment between whole titles is
dropped or limited to a suffix the other side carries, and the version word
list is replaced by a rule (a word read only inside brackets is never the
title), each driven with the unfiltered differential of R-1534 so no title
loses its own row. A wrong genre written onto a file is the board bar's
damaged data.
