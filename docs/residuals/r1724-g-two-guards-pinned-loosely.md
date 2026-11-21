---
title: The tail alone guard's choice of the stem over the stripped text, and the ISRC test's hold on the reading, are pinned loosely
found: at the review of #883, R-1724, round two, 2026-11-21.
issue: no
---

**The mechanism.** Two of round two's mutations on a scratch copy. The tail
alone guard in `titles.name_title` returning the stripped text rather than
the stem survives, 0 kills of 1,285 collected: a file named `_PN  .flac`
would be asked `_PN` rather than `_PN  `, and no test lists a tail alone
name with trailing whitespace. Round one's reading restored alone, a tail
alone name reading to the empty string with `tag_one` still asking, is
killed by 9 tests but not by
`test_a_name_with_no_title_past_its_tail_still_takes_its_genre_by_isrc`,
since an empty title is still asked and the ISRC lookup still runs; that
test fails 3 of 3 against round one's whole source, the defect it was
written for.

**Measured cost.** None driven: both inputs ask a question that misses and
reach the ISRC lookup either way.

**Closes when:** a test names a tail alone stem with trailing whitespace,
and the ISRC test asserts what Discogs was asked. Ledger only.
