---
title: "A lone ID3v1 trailer survives any save, so a preservation test needs both tags disagreeing"
date: 2026-09-19
category: workflow-issues
module: "tests/test_art.py, src/cratekit/core/art.py, src/cratekit/core/tags.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: incorrect_assumption
resolution_type: test_fix
applies_when:
  - "A new writer saves an MP3 and must go through tags._save to keep the ID3v1 trailer"
  - "A test appends a 128 byte TAG block to a synthesized MP3 and asserts it is unchanged after a write"
  - "A mutation row swaps tags._save for a bare handle.save() and kills nothing"
symptoms:
  - "The trailer test passes with the guarded save and with the bare one"
  - "scripts/mutate.py reports the save seam row as zero, promoted to the full suite"
  - "A hand appended trailer reads back byte for byte after a plain mutagen save"
related_components:
  - development_workflow
  - testing_framework
tags:
  - mutation-testing
  - id3v1
  - mutagen
  - fixture
  - tags-save-seam
---

# A lone ID3v1 trailer survives any save, so a preservation test needs both tags disagreeing

## What happened

U83's art writer saves through `tags._save`, the one seam that keeps a real
`.mp3`'s ID3v1 trailer. Its test appended a hand built 128 byte `TAG` block to a
synthesized MP3, wrote a cover, and asserted the last 128 bytes were unchanged.
It passed. The mutation row that replaced `tags._save(path, handle)` with
`handle.save()` killed nothing, in the subset and in the full suite.

## Why

The guess was that mutagen's default save rewrites a present ID3v1 tag from the
v2 frames, so a bare save would blank a trailer whose file has no matching v2
frames. Driving it showed otherwise. When an MP3 has an ID3v1 tag, mutagen LOADS
it into v2 frames on open: the probe file came back with `TIT2` and `TCON` it
never had. The rewrite on save is then built from those frames and reproduces
the trailer byte for byte. A lone trailer is round tripped faithfully by any
save, guarded or not, so a fixture made of one cannot tell the two apart.

What a bare save does destroy is narrower. An ID3v1 genre is one byte indexing a
fixed list. When the file ALSO carries a v2 genre outside that list, mutagen
rewrites the byte to 255. That needs both tags present and disagreeing, which is
the state a legacy library is actually in.

## The fixture that works

`tests/test_adoption.py::_give_it_an_id3v1_genre` had it already. Set a v2
`TCON` to a genre the v1 list never held, `save(v1=2)` so mutagen writes the
trailer, then overwrite the last byte with a real v1 index such as 31. A bare
save now turns that byte into 255 and the guarded save keeps it.
`tests/test_art.py::test_an_mp3_id3v1_trailer_survives_the_write` builds the
same state, and the re-measured row kills it (`docs/mutation/u83-c.md`).

## The rule

Any test that claims an MP3 write preserves the ID3v1 trailer builds BOTH tags
with a v2 genre outside the v1 list. Then revert the save seam once by hand, or
give it a mutation row, because this test passes for the wrong reason silently.
