---
name: library-reports
description: The four read-only reports over a collection export, coverage, duplicates, library statistics, and intake aging. Use when someone asks how big the library is, which tracks the governed trees do not file, whether a recording is held twice, what is still sitting in intake and how stale it is, or when a report's numbers look wrong and the real question is which export produced them.
---

# Library reports

Four verbs that read one document and write nothing to it, the argument all four
need, and the three places a person misreads what they say.

## The export is an argument, and there is no default

```bash
crate audit coverage /path/to/export.xml
crate audit duplicates /path/to/export.xml
crate report library /path/to/export.xml
crate report intake-aging /path/to/export.xml
```

The product records no location for a collection export, so there is nothing to
fall back on, and inventing a default would mean reading whatever happens to sit
at a guessed filename. A stale export answers every question here confidently and
wrongly, and all four answers would agree with each other while all of them were
about last month's library. Typing the path is what makes it visible which
document you are looking at, so it is the path you last wrote rather than one the
tool chose.

None of these opens the database. The reports package is held to an import
allowlist that admits no database module at all, so a report cannot acquire a
handle that could commit, even by mistake.

## A wrong file is refused, never read as an empty library

The document is recognized positively, one structure at a time: the export root
element, a collection section, a declared entry count on it, a playlist section
and its root node, that declared count agreeing with the number of track elements
actually found, no identifier appearing twice, and every node in the tree saying
which kind it is. Anything that fails is refused with the structure named.

That is worth more than it looks. A half-copied file holds no readable tracks, so
a duplicate audit over it reports nothing, and nothing is also the correct answer
for a clean library. Two very different facts with one rendering is how a person
never finds out.

## Coverage counts placements, not presence

```bash
crate audit coverage /path/to/export.xml
crate audit coverage /path/to/export.xml --limit 2000
crate audit coverage /path/to/export.xml --limit 0
```

An entry is covered when one of its placements sits under the declared routing
tree at any depth, so a tree somebody filed inside another folder is still read
as the tree. A track in three folders beneath it is covered once and reported as
filed three times, because a track genuinely in three places is a different thing
to look at from a track in one, and a per-playlist walk cannot see the difference
at all.

The list is capped at two hundred by default, since a library nobody has swept
puts its entire collection in the answer. The cap never touches the arithmetic.
The summary carries the true total beside the number listed, and a run that
dropped rows says so in a row of its own, because a capped list that reads as a
complete one is worse than no list. `--limit 0` lists none and still counts
everything.

This verb moves nothing, which is what makes it safe to read before deciding
whether to act. Acting is a different verb.

```bash
crate route unplaced
```

## The duplicate audit asks once and remembers the answer

```bash
crate audit duplicates /path/to/export.xml
crate review list --queue duplicates
crate review show ITEM-ID
crate review resolve ITEM-ID --verdict rejected
```

It compares the whole collection rather than one playlist at a time, so what it
finds is the expensive pair: one recording acquired twice, months apart, filed
under two different folders, with two files on disk. Scoped to a playlist that
pair is invisible by construction, because the two entries are never in the same
list.

Nothing is deleted and nothing here can delete. A pair becomes an item in the
duplicates queue, and a rejected verdict on it is the persistent ignore, so an
intentional alternate, a clean cut kept beside the explicit, is asked about once
rather than on every run forever. Re-run the audit as often as you like. It
re-offers the same items, finds them already there, and leaves every verdict
alone.

An item is addressed by the normalized artist and title, which is the recording
rather than the pair or the file. Renaming a file, re-importing it, or moving it
between folders does not orphan the decision, and a third copy arriving later
does not re-ask, because the question answered was about the recording.

```bash
crate review clear ITEM-ID
```

Clearing revokes a verdict, so a suppression is reversible rather than permanent.

## The library report answers four questions and judges none

Genres, one row per folder directly under the governed tree, counted by distinct
track. Summing the sub-playlists would double count every track filed under two
energy bands, which is how a folder comes to look twice its real size. Tempo
spread, read through the declared naming template rather than a pattern of the
report's own, with unreadable heads counted and reported instead of dropped, so
"the spread of what I could read" is never passed off as "the spread of the
library". Tree shape, the deepest path in the export against the depth the
template declares. And three gaps, kept apart because three different acts answer
them.

Every row is INFO on purpose. An unused bucket is a taxonomy somebody has not
grown into and a shallow tree is a library somebody is still building, so
painting either red would be the tool deciding what a library ought to look like.
When the governed tree is missing from the export entirely you get one row saying
that, not one row per declared bucket, because a page of true rows that are not
the problem is how the actual problem gets buried.

The tempo spread is read and only read. Nothing in this product writes a tempo
value, a grid, or an average into any container.

## Intake aging bands every grouping, on thresholds you declared

```bash
crate report intake-aging /path/to/export.xml
crate report intake-aging /path/to/export.xml --as-of 2026-08-01
```

Four bands, expired, stale, current, and undated, and every grouping lands in
exactly one. The two day counts come from configuration and from nowhere else,
so there is no hardcoded policy to fall back on and the report cannot quietly run
against a threshold nobody chose.

A grouping is aged on the date in its own name. One carrying no date is undated
rather than aged at zero, because guessing an age eventually tells somebody to
throw away a list that is a week old. Nothing is recorded between runs either.
The answer is a pure function of the names, the thresholds, and the day, which is
why there is no ledger on disk to go stale or get corrupted.

`--as-of` names that day, which is what makes an answer reproducible and what
lets you ask how the queue looked before a sweep. Pass it as an ISO date. An
empty value is refused rather than treated as absent, since an empty string is
something a person typed and answering it for a day nobody named is the outcome
the refusal exists to prevent.

## Reading the answers with something other than your eyes

```bash
crate --output json report library /path/to/export.xml
crate --output json audit coverage /path/to/export.xml --limit 0
```

Three of the four emit the same shape the health check emits, built from its own
check row type rather than a second shape that happens to serialize the same keys
today, so anything already reading the health check reads these. The duplicate
audit emits a review set instead, because its answers are queue items rather than
check rows. Reach for the JSON whenever something other than a person is going to
read the result, since the human rendering is free to change and the payload is
not.

## When one of them is not there at all

Coverage is core and is available under every profile. The duplicate audit rides
on its own module, and both reports ride on the reports module, so a profile with
those switched off does not merely refuse them, it does not register them: the
verb is absent from the parser and you get an argument error rather than a
message about modules. The error will not mention the profile, which is why this
is worth knowing here.

```bash
crate profile show
crate profile set full
crate doctor
```

The health check is also where a refusal about configuration goes, because all
four verbs read the library root and the naming template out of the configuration
before they read a single byte of the export.
