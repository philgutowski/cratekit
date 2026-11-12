---
title: The shared title matcher reads a title that strips to nothing as a match, so Beatport can write another track's genre
found: at the review of #673, U244, 2026-11-12.
issue: yes
---

**The mechanism.** `_title_matches` in `src/cratekit/tagging/searchers.py`
strips a trailing bracket with `_without_trailing_bracket`, whose group runs
from the first "(" to the last ")". A title that starts and ends with a
bracket, "(Not Just) Knee Deep (Part 1)" or an "(Intro)", strips to the empty
string, and the empty string is a substring of every title, so any row by the
artist matches. U244 closed this for Discogs alone with
`_discogs_title_matches`; Beatport and the two scraped parsers still read the
shared matcher.

**Measured cost.** Driven at U244's review through `tag.tag_one` on the
shipped Beatport parser: a file titled "(Intro)" took Deep House off a
different track by the same artist, written for good, since a genre is fill if
empty. Not measured: how many files in a real library carry such a title.

**Closes when:** the shared matcher refuses an empty side and compares a
title its strip empties whole or by its last group, as Discogs' does, with the
Beatport and scraped suites driven over it. A wrong genre written onto a file
is the board bar's damaged data.
