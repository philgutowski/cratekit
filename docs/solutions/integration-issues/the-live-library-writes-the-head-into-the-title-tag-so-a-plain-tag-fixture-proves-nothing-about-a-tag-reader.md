---
title: The live library writes the head into the title tag, so a fixture with a plain tag proves nothing about a tag reader
date: 2026-09-23
category: integration-issues
module: src/cratekit/acquire/match.py, src/cratekit/core/tags.py
problem_type: integration_issue
component: library_index
severity: high
root_cause: convention_not_visible_in_code
resolution_type: guard
applies_when:
  - A reader takes a title tag and compares it with a provider spelling, a
    listing row, a search query or the index.
  - A fixture writes a plain title into a real container and the reader passes.
  - A live count says owned files are missing, offered, or unmatched, and the
    filename side already strips heads.
tags:
  - library-index
  - title-tag
  - camelot-head
  - fixtures
  - r-664
  - r-665
  - r-168
---

# The live library writes the head into the title tag, so a fixture with a plain tag proves nothing about a tag reader

## The symptom

The first live `crate intake playlist favorites` resolved 206 hearts as 0
owned, 61 offered and 145 missing over a library that an earlier sitting had
proved holds at least 59 of them by ISRC. Every fixture test of the index was
green. `intake missing --job` over that job would have listed at least 96
owned tracks for download, and the landing after it would have put 96
duplicates into the library.

## Where the cause actually was

Not in the matcher and not in the filename stripper. `match._read_from_disk`
strips the `KEY - BPM - ` head from the filename stem and takes the title tag
verbatim, on the reasoning that a tag is the file speaking. On this library
the tag is not plain: the live system writes the same head into the title tag
as into the filename, 9767 of 9868 files under the music folder, a convention
R-168 records for the naming verb and nothing in the code states for the
reader. So every processed file indexed under a recording token carrying its
head, an exact match was impossible, and the approximate pass either offered
the file or scored a short title under the floor.

Every fixture that reached the tag reader wrote a plain title into its
container. A plain tag and a plain provider row match whichever way the reader
is written, so the suite could not see the defect and did not.

## The rule

A fixture for a reader of the title tag carries the head inside the tag, the
way the volume does, or it proves nothing about that reader. The shared
helper is `tests/_containers.py:tagged_container`, and the index tests in
`tests/test_match_states.py` under the headed title tag section are the
pattern: a real container, the head in both surfaces, a provider row spelling
the plain title.

The index strips the tag under the same template the stem strips under, both
ends, before the pair rule, and reads the key off the tag's head below the
stem's. Four other readers still take the tag verbatim; R-665 names them and
says which carry a cost today.

## How to tell you are in this trap again

A live count over the volume disagrees with a green suite about ownership,
identity or a search hit, and the reader under suspicion reads `title` off
`tags.read_tag` without a `strip_heads` beside it. Check the tag on one real
file before trusting any fixture.
