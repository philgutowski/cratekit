# U119 mutation tables, read

Three tables, both the author's and not independent, measured by
`scripts/mutate.py` on `fable/276-every-genre-folder-has`. Every row's subset
was `tests/test_genre_favorites.py`, with `tests/test_taxonomy.py` beside it for
the loader rows, `tests/test_rebuild.py` for the rebuild row, and
`tests/test_genre_favorites_adoption.py` with `tests/test_adopt_apply_cli.py`
for the adoption row.

**`u119.md`**, 25 rows at `638a53c`, null control 0 of 13,045, no collect
drift, every restore verified against `git show HEAD`. 21 killed, 1 collect
error, 3 zero, each promoted to the full suite and still zero. The driver's
first two launches refused before any row ran, because the baseline was red
on the conformance sample for the new verb: the review's fix round had made an
emptied source playlist a refusal and the lazy sample made an emptied one. The
sample now hearts the fixture's first row into the source, after one more
launch found the binding's query object truthy with no rows in it.

**`u119-b.md`**, 3 rows at `b086709`: the three zeros measured again against
the tests they bought. Null control 0 of 13,049. All 3 killed.

**`u119-c.md`**, 7 rows at `7ea30f8`, the guards the watcher's review round
added: a torn record listed (C2), the uncompared playlist dimension's
differences dropped (C3), a first Favorites under the recorded folder (C4),
the interruption carrying what landed (C5, 3 kills), the skip said (C6), the
partial carried by the additive half (C7). Null control 0 of 13,056. 6
killed, 1 zero.

32 distinct mutations in all, 25 in the author's first pass under the cap of
25 and 7 for the watcher's round: **30 killed outright, 1 killed at
collection, 1 zero**. Three more were considered and logged as dropped in
`u119-rows.toml`: the verb's nothing to refresh note and its left alone note,
both wordings, and the CONCEPTS text.

## The third table's zero

- **C1, the record's Favorites entry binds the bucket before its band
  entries.** The first fix sorted the record's entries so the band entries
  bound the folder first; the same fix also marks a bucket torn when two of
  its live entries name different folders, and a torn bucket is listed and
  skipped whichever entry came first. So the order decided nothing, the
  reversal killed nothing, and the sort was dead logic beside the guard that
  holds (C2, 1 kill). The sort is removed and the comment says why; nothing
  is left to measure.

## The collection error

- **T4, a class with no `signal` key reads as a playlist class.** Measured as
  39 failures over 99 collected in the subset, flagged by the driver as a
  collection error rather than a death count: with the default flipped the
  shipped template's two older classes become playlist classes with no
  `signal_playlist`, the loader refuses the template, and every test that
  builds the default taxonomy dies at import. The mutation is dead, by the
  template's own load rather than by a test of the rule. The rule itself,
  that an absent key means the vocal reading, is pinned by
  `test_the_shipped_default_declares_the_genre_favorites_as_a_playlist_signal`,
  which asserts the vocal class's signal is `vox` with no playlist, so a
  mutation that flipped the default for a class with no `signal_playlist`
  alone would also die there.

## What the first table's zeros bought

- **G5, the folder's own Favorites counted among the folder's members.** Inert
  on the first suite: a Favorites member is a member of the folder's band in
  every test, so counting it twice changed nothing. The case it holds is a
  favourite moved out of its band by hand, which must then leave Favorites
  too, since it is no longer the folder's.
  `test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`.
  1 kill.
- **G12, a removed Favorites of the name written into.** No test held a
  removed namesake under a folder. `test_a_removed_favorites_under_the_folder_is_not_written_into`.
  1 kill.
- **A1, the adoption's end skips the refresh.** No test drove the adoption
  worker with a source playlist present; the suite that drives the real
  dispatcher on a cut over tree is the cutover suite's, so the new file
  `tests/test_genre_favorites_adoption.py` sits on its fixtures. 2 kills.

## What the kills say

The declaration is held from four sides: one additive class per signal (T1), a
playlist signal names its playlist (T2) and needs version 4 (T3), and the
default signal is the vocal reading (T4, at collection). The source is held
to a plain, live, non-empty playlist (G1 the class, G2 an emptied source, G3
two sources, G4 a removed membership). The plan is held on what a folder
holds (G5, G6 with 11 kills), which folder is whose (G7, G8), what the digest
covers (G9) and what a missing source names (G10). The write is held on the
stale digest (G11), the removed namesake (G12), the removals asked for (G13)
and counted (G14), the second commit's admission (G15, 4 kills), the read
back (G16) and the node record (G17, 3 kills). The rebuild asks the vocal
derivation only of vocal classes (R1, 35 kills) and adds the favourites to
the routing tree alone (R2). The adoption's end runs the refresh (A1) and the
verb reads the acknowledgment before its gate (V1).
