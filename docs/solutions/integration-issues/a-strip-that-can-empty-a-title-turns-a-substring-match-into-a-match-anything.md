---
title: "A strip that can empty a title turns a substring match into a match of anything"
date: 2026-11-12
category: integration-issues
module: src/cratekit/tagging/searchers.py
problem_type: integration_issue
component: tagging
severity: high
resolution_type: code_fix
applies_when:
  - "A unit compares titles, artists or any names by containment after stripping part of them"
  - "A unit adds a new catalogue source, or a new caller of the shared title matcher"
tags: [title-match, substring, bracket-strip, beatport, discogs, traxsource, bandcamp, r-1534, r-1631, r-1636, camelot-head, dash-parts]
---

# A strip that can empty a title turns a substring match into a match of anything

## Problem

The record shop matcher strips a trailing bracketed suffix ("(Extended Mix)")
and then compares the two titles by containment, because a catalogue and a
file disagree about the suffix and about features. The strip runs from the
first "(" to the last ")", so a title that starts and ends with a bracket,
"(Intro)" or "(Not Just) Knee Deep (Part 1)", strips to the empty string. The
empty string is contained in every string, so the comparison answered yes for
every row by the artist, and that row's genre was written onto the file for
good (R-1534, driven at U244's review). The same shape turned up three times:
the sync twins reader on a title wholly in square brackets, Discogs at U244,
and Beatport's own scoring, which strips separately from the shared matcher.

## What to do

- **Ask what the strip leaves before comparing.** A side with no letter or
  digit left identifies nothing and matches nothing, on either side, searched
  or found. `_identifies` in `tagging/searchers.py` is the check.
- **Read a title the strip empties by its core, not by the remainder.**
  `_title_core` takes off only the bracket groups a title ends with, read as
  balanced groups from the end, and for a title of brackets alone takes the
  groups' words and marks them for exact comparison only.
- **Containment is the wrong comparison, not a loose one (R-1631).** After
  R-1534 three shapes of the same substring test still wrote another
  recording's genre: a strip from the first bracket cut "Knee (Not Just) Deep
  (Part 1)" to "knee", in "Knee Slapper"; a containment between whole titles
  read a word inside one title's brackets as the other title ("Intro" in
  "Sunrise Mood (Intro)"), refused only for a hand list of version words that
  missed "vocal" and "reprise"; and raw characters put "Club" in "Nightclub".
  What landed compares readings, tuples of whole words once a title has shed
  what is not its title (`_readings` in `tagging/searchers.py`), and two titles
  match on a shared reading.
- **Ask of any list in a matcher which way it fails.** A list that refuses a
  match for its words fails open on every word it lacks. The version words now
  come from the domain's `core.tombstone.VERSION_WORDS` and mostly shed a
  trailing version from a title, where a word the list lacks costs a miss. A
  file's dash tail of version words alone was refused on it (`_names_a_title`),
  so "Other Song - Vocal Mix" read "vocal mix" as a title until R-1636 replaced
  the list's verdict with the tail's position (below).
- **A number is part of the title (round one of R-1631).** Shedding numbers
  with a version read "Kitchen Session 2" as "Kitchen Session 1"; shedding a
  leading number after the bracket words joined read "909 (Jack Mix)" as
  "Jack"; and refusing every all number part refused "1998" its own row behind
  a head. Round two found the class one rule over: a year riding with any
  version read "Summer 1999 (Original Mix)" as "Summer 2000 (Original Mix)".
  Only a year beside "remaster" rides with a version, only a zero padded
  number is a track number, and only the head's own parts are refused for
  being numbers.
- **The file's title is not shaped like a catalogue's.** The live library
  writes `KEY - BPM - ` into the title tag (the solution on the head in the
  title tag), and a file with no title tag is asked by its "Artist - Album -
  01 Title" name, so a catalogue row is read only by its head before a
  version tail and the file's side differently. Read the two the same way and
  either the head is the title ("Aurora Bloom" matching every "Aurora Bloom -
  X" heading) or the headed library matches nothing.
- **Which of a file's dash parts is its title is a matter of position and the
  artist, not of a list (R-1636).** R-1631 read the file's side from any run
  of its dash parts, so a version tail the list lacked ("Other Song - Vocal
  Mix" as "vocal mix"), an untagged name's album ("KEY - BPM - Tide - Artist -
  Sun Path" as "sun path") and its artist ("KEY - BPM - Artist - Sun Path" as
  the artist) each wrote another recording's genre. The searcher already
  holds the file's artist, so `_title_starts` places the title at the first
  part after the head that is not the artist's name, word for word, and never
  reads a later part alone, save a track numbered "02 Title". Bound the head
  to the shapes the naming verb writes (a key, a tempo, or one of each,
  `_head_end`): an unbounded run of numbers ate "909" of "08A - 124 - 909 -
  Artist - Album" and moved the title onto the album. And the artist is the
  title only when nothing else can be, judged by version words alone, never
  by a part that merely ends in one: "Artist - Sunrise Mood Extended Mix" is
  "sunrise mood", found only by wrapping every suite title in each name shape
  and comparing it with the plain title's own matches.
- **What the new rule cannot tell apart, it refuses.** "How Does It Feel"
  against "Untitled (How Does It Feel)" has the same evidence as "Intro"
  against "Sunrise Mood (Intro)", so both are refused; that loss is pinned as
  a known cost. Keep "Original" finding "Original feat. Someone" (round one
  of R-1534 drove that loss through `tag_one`). A differential that filters
  out the pairs the new rule is about measures nothing: run it unfiltered,
  over title positions in the suite rather than every string, and read every
  gain as closely as every loss: R-1631's own draft gained "Aurora Bloom - Sun
  Path" matching a heading "Aurora Bloom - Tide", found only by reading gains.
- **Every scorer that strips on its own needs the same care.** Beatport's
  `_beatport_best` never called the shared matcher; fixing the matcher alone
  would have left it open. And a scorer ranks, so a change that only widens
  one row's tier can lose the file's own row on page order: round two of
  R-1534 drove a row "Love (feat. X)", read by its core "love", tying with and
  beating "Love Is The Message". Drive two rows on one page, not one. Grep for `in name`, `in right` and the strip's
  callers, not only the matcher's.
- **The same empty substring hides on the artist side.** A credit with no
  name was contained in every searched artist in `_beatport_best`.

## How to test it

Drive both ways round, on every source that reads the matcher, with a table
of pairs that must match (so no correct match is lost) and a table that must
not, plus a file through `tag.tag_one` with the genre read back. A headed
title tag, "04A - 126 - Burning (Extended Mix)", is in the table, since a
plain title proves nothing about the library's own. A test of
the matcher alone would have missed Beatport, which scores rows itself.
