---
title: "A strip that can empty a title turns a substring match into a match of anything"
date: 2026-11-12
category: integration-issues
module: src/cratekit/tagging/titles.py
problem_type: integration_issue
component: tagging
severity: high
resolution_type: code_fix
applies_when:
  - "A unit compares titles, artists or any names by containment after stripping part of them"
  - "A unit adds a new catalogue source, or a new caller of the shared title matcher"
tags: [title-match, substring, bracket-strip, beatport, discogs, traxsource, bandcamp, r-1534, r-1631, r-1636, r-1646, u280, camelot-head, dash-parts, typed-parse, differential]
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
  or found. `identifies` in `tagging/titles.py` is the check.
- **Read a title the strip empties by its core, not by the remainder.**
  `title_core` takes off only the bracket groups a title ends with, read as
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
  what is not its title (`_readings`, since replaced by U280's parse, below), and two titles
  matched on a shared reading.
- **Ask of any list in a matcher which way it fails.** A list that refuses a
  match for its words fails open on every word it lacks. The version words now
  come from the domain's `core.tombstone.VERSION_WORDS` and mostly shed a
  trailing version from a title, where a word the list lacks costs a miss. A
  file's dash tail of version words alone was refused on it (`_names_a_title`, gone),
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
  holds the file's artist, so the parse (`_layout` in `tagging/titles.py`) places the title at the first
  part after the head that does not credit the artist, and never reads a
  later part alone, save a track numbered "02 Title". Read the artist's part
  as a name writes it, not as the tag does: round one of the review drove a
  collaboration ("Artist & Tide"), "The", an accent, the naming verb's
  "[MP3]" marker and a track number before the artist, each losing the
  file's own row once the artist test was word for word. But a part merely
  holding the artist's name is a title, "Riding The Tide" by Tide or
  "Bernard Badie Theme": round two drove that looser test to wrong genres.
  The test is a credit, the part's names split on the joins a credit is
  written with ("&", ",", "x", "feat"), one of them the artist's name, accents
  folded; "and" and "with" join nothing, since titles hold them. A
  differential that wraps titles only in the exact artist string is a
  measurement on a fixture: wrap them in the artist as names write it, and
  put the artist's name inside titles too. Bound the head
  to the shapes the naming verb writes (a key, a tempo, or one of each,
  `_head_end`): an unbounded run of numbers ate "909" of "08A - 124 - 909 -
  Artist - Album" and moved the title onto the album. And the artist is the
  title only when nothing else can be, judged by version words alone, never
  by a part that merely ends in one: "Artist - Sunrise Mood Extended Mix" is
  never the artist alone, found only by wrapping every suite title in each
  name shape and comparing it with the plain title's own matches.
- **A shape only a list could tell apart is read by the row's own structure
  (R-1646).** "Artist - Vocal Mix" is a title "Vocal Mix" or the artist's
  self titled track in its vocal mix, and "Artist - Sunrise Mood Extended
  Mix" is the same shape the other way; R-1636 read both ways, so a "Vocal"
  row or a self titled row wrote its genre. Reading either way alone loses a
  row on page order, and a list deciding which words are versions fails open
  on every word it lacks. So the name is read only as its two splits into a
  title and a version (`_name_splits`), and a row matches it only by writing
  one of them itself, its title and version apart in brackets, after a dash,
  or in Beatport's name and mix (`_row_splits`, `read_beatport_row`). A
  plain row "Vocal Mix" confirms nothing, since Discogs lists a single's
  versions as its track titles. The cost is a miss on the file's own row
  written under another mix, with no version, or with one more bracket
  group, asked of Phillip on #788. When the brief's scenarios want both
  readings to win in turn, check whether anything but a list tells them
  apart before building either. And drop a reading in one place only after
  checking every other reading of the same name: round one of the review
  found the whole title reading, shed of a feature credit, still collapsing
  "Artist feat. Tide - Sunrise Mood Extended Mix" to the artist's name, so
  the self titled row won where `main` had at least ranked the title's own
  row. A whole name whose first part credits the artist was then read
  unshed; since U280 no whole name is shed across its dashes (below).
- **After four fixes in a day, stop patching the reading model (U280).** A
  matcher that reads a title as every way it could be read and matches on
  any shared reading widens every source with each reading a fix adds, and a
  fix that removes one must chase every other path to the same words; four
  fixes in a row each made the next review's defect. What replaced it,
  `tagging/titles.py`, reads a file's name once into typed parts (the head,
  a track number, the artist's credits, the title, an album before a track
  numbered title), each with how it was told, and an outcome: titled,
  ambiguous where only a list of version words could tell, or unreadable.
  Ambiguity is a miss unless the row writes the same split. Two lessons of
  how it was built. Build the new beside the old and drive it to parity
  first: `scripts/title_differential.py` loads `main`'s `searchers.py` from
  git and decides every name and row pair of the suite's corpus, wrapped in
  the naming verb's shapes, by an index, so the first run proved the parse
  re-expressed `main` exactly (no difference over 394,160 names) before any
  rule moved. Then make each deliberate change alone and classify every
  difference it makes against the commit before it, by which change
  explains it; a difference no change explains is a defect. And keep
  shedding inside the title: a feature credit, a version or a bracket group
  shed from a whole name cuts through parts that are not the title, which is
  how "Artist feat. Tide - X" and "Artist - (Intro)" collapsed to the
  artist, and how "08A - 124 - Interlude" met "08A - 124 - (Intro)" on the
  head's words alone. The whole name is compared as written, never shed of
  a feature credit or a version, and a bracket group is shed only from the
  part that carries it; the
  review's first round found the bracket case and a track number read past
  the marker across a dash, both shapes of the same rule. What that shedding found rightly, a
  first part naming the artist only as featured (with no head before it, as
  `main` read it) and a tempo alone before a version alone, is now a title
  candidate the parse names. A property over
  names the naming verb renders found two misses `main` shared, a marker
  before a lone track number and before a title of its own brackets.
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
