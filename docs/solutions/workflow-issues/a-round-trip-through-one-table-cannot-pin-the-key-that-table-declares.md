---
title: "A round trip through one table cannot pin the key that table declares"
date: 2026-09-17
category: workflow-issues
module: src/cratekit/core/tags.py
problem_type: testing_gap
component: testing_framework
severity: medium
root_cause: self_referential_test
resolution_type: test_added
applies_when:
  - "A field is being added to core/tags.py FIELDS"
  - "A reader and a writer are driven by one shared table of keys"
  - "A round-trip test is the only coverage a mapping has"
  - "A mutation row over a key or a format constant measures zero"
symptoms:
  - "A mutation that renames a key survives the whole suite"
  - "Every container's round trip passes while the on-disk format is wrong"
  - "A field written by this product reads back fine and is invisible to every other tool"
tags:
  - mutation-testing
  - round-trip
  - tags
  - id3
  - pattern-four
---

# A round trip through one table cannot pin the key that table declares

## Context

R-355's fix added an `isrc` field to `core/tags.py`, whose `FIELDS` table is the
single place a logical field name maps to a Vorbis comment, an ID3 frame and an
MP4 atom. The module's whole design argument is that ONE table driving both the
reader and the writer makes reader and writer disagreement unrepresentable, and
`tests/test_tags.py` round trips every field in `FIELDS` through all six
containers.

The sitting's mutation table changed the ID3 side of the new row from `TSRC`,
which is the frame the ID3 standard names for a recording's ISRC, to
`TXXX:ISRC`, a user defined frame. **Zero tests died.**

## Why zero, and why that is not a flaw in the assertion

The round trip is genuinely valuable and it cannot possibly catch this. It writes
through the table and reads back through the same table, so both halves move
together. Rename the key to anything at all and the test still passes, because
the test never asserts what is ON DISK, only that a value survives a write
followed by a read.

The design property, reader and writer cannot disagree, is exactly what makes the
test blind here. The two things that CAN disagree are this product and every
other tool that touches the file, and no test represented that until now.

This is METHOD's pattern four seen from an unusual angle: the justifying fixture
was not written alongside the guard, it was written alongside the guard's own
mirror image.

## The fix

`test_an_isrc_another_tagger_wrote_is_read_from_the_standard_frame` writes a bare
`TSRC` frame with mutagen directly into a real AIFF and a real MP3, then asserts
the shipped reader returns it. One tagger writes, a different one reads, so the
key itself is pinned rather than the symmetry.

## The rule to carry forward

**Any field in `FIELDS` whose key matters outside this product needs one test that
does not use the writer.** The round trip proves the product is self consistent.
A file produced elsewhere proves the product is correct. For `isrc` the stakes
are concrete: the outbound verbs hand this value to the streaming account to match
a recording, and every file in the library was tagged by something else.

A mutation row over a key or a format constant that measures zero is usually this
shape. Before calling it equivalent, ask what would have to read the file for the
difference to show, and whether anything in the suite is that reader.

## One more thing this sitting proved about the row

The remeasure of the row after the fix was never run: the driver was killed by
the operating system for memory pressure with unrelated work holding the machine,
and it left its null control comment appended to `core/tags.py`, restored from
`git show HEAD:` and verified. **So the kill is asserted by construction and not
measured**, which `docs/mutation/sitting4-notes.md` states and which the next
session touching this module should settle with
`scripts/mutate.py docs/mutation/sitting4-rows.toml --resume`.
