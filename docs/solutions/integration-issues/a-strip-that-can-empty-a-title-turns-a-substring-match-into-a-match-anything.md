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
tags: [title-match, substring, bracket-strip, beatport, discogs, traxsource, bandcamp, r-1534]
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
  `_title_core` keeps the leading bracket groups and the text after them, and
  for a title of brackets alone takes the groups' words and marks them for
  exact comparison only.
- **A containment that reaches into a bracketed suffix needs a contained
  side that names more than a version.** Version words alone ("Original Mix",
  "Dub") are in the suffix of half a catalogue; `_contains` refuses them there.
  Between two cores, where the suffix is gone, they compare as any title does,
  or a track called "Original" loses "Original feat. Someone" (round one of
  R-1534 drove that loss through `tag_one`). A differential that filters out
  the pairs the new rule is about measures nothing: run it unfiltered.
- **Every scorer that strips on its own needs the same care.** Beatport's
  `_beatport_best` never called the shared matcher; fixing the matcher alone
  would have left it open. Grep for `in name`, `in right` and the strip's
  callers, not only the matcher's.
- **The same empty substring hides on the artist side.** A credit with no
  name was contained in every searched artist in `_beatport_best`.

## How to test it

Drive both ways round, on every source that reads the matcher, with a table
of pairs that must match (so no correct match is lost) and a table that must
not, plus a file through `tag.tag_one` with the genre read back. A test of
the matcher alone would have missed Beatport, which scores rows itself.
