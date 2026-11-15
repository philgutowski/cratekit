---
title: A file with a title tag and no artist tag is not asked by its name's artist
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** The brief asks that "a file with no artist tag is asked
with the artist and title its name reads to". The session read "its name"
as the file's name, asked by `tag_one` only when the file has no title tag
either, since a title tag is not the name and the name's artist beside a
tag's title is two sources for one question. So a file whose title tag is
`8A - 122 - Kerri Chandler - On My Way` and whose artist tag is empty is
asked artist empty and track `Kerri Chandler - On My Way`, which no
catalogue on the walk can match, and the test
`test_a_title_tag_with_no_artist_tag_is_never_split_by_its_name` pins it.

**Measured cost.** Driven at round two: no genre for that file, where the
same file with no tags writes House. Not a regression: main asked it with
no artist and the head too. Sitting 100 cleared both tags on every file it
stripped, so how many library files carry a title tag and no artist tag is
unmeasured.

**Closes when:** a live count says such files exist, and the split is read
off the title tag or the name for them, Phillip's call if the two disagree.
Ledger only.
