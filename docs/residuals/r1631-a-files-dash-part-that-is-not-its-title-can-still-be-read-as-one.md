---
title: A file's dash part that is not its title can still be read as its title, so another row by the artist writes its genre
found: at the review of #770, R-1631, rounds one and two, 2026-11-12.
issue: yes
---

**The mechanism.** Since R-1631 the file's side of the record shop matcher in
`tagging/searchers.py` (`_readings`, `searched=True`) is read by any run of
its dash parts, because the live library writes `KEY - BPM - ` into the title
tag and a file with no title tag is asked by its name. Which part is the
title cannot be told without the artist, so three shapes still read a part
that is not the title. A dash version tail with a word `VERSION_WORDS` lacks
is read as a title: "08A - 124 - Other Song - Vocal Mix" meets a Discogs track
"Vocal Mix", and "Other Song - Vocal Mix" a Beatport row "Vocal"
(`_names_a_title` refuses a tail of version words only by the list). A name
"KEY - BPM - Title - Artist - Album" reads its album, so an untagged "08A -
124 - Tide - Aurora Bloom - Sun Path" meets the title track "Sun Path"; and a
name "KEY - BPM - Artist - Title" reads its artist, meeting a self titled row.
Every one matched on `main` too, by containment.

**Measured cost.** Driven through `tag.tag_one` at round one: the Discogs
style of "Vocal Mix" was written onto "08A - 124 - Other Song - Vocal Mix",
and Beatport's "Vocal" row onto "Other Song - Vocal Mix", on `main` and on
the branch alike. The producer of a dash version in a title tag was read,
not driven: the fallback landing writes `Wanted.listed`, and `split_title`
says the playlist API ships "Title - Version". `naming_cli` measures 53% of
live names as "Title - Artist - Album". Not measured: how many files carry
such a title or no title tag.

**Closes when:** the matcher is given the searched artist and album, so a
dash part that names either is shed rather than read, and a dash version
tail is told from a title by its position after the title rather than by a
list. A wrong genre written onto a file is the board bar's damaged data.
