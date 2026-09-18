# U68 mutation notes

The table is `docs/mutation/u68.md`, measured by `scripts/mutate.py` in the
foreground on `relay/113`, 23 rows over `src/cratekit/acquire/listdoc.py`, the
subset `tests/test_listdoc.py`. It is the author's table, with no independent
pass. Null control 0 of 7733, no collect drift, every restore verified against
`git show HEAD`, and `git status` after the run showed only the driver's two
output files. This is the first real table the driver has run since the suite
went parallel. The null control and the promoted zeros each collected 7733,
which is the baseline, so the parallel run lost no file to collection.

20 of 23 killing. Three zeros, each promoted to the full suite.

## The zeros

- **W3_listed_compared and W5_title_compared, equivalent mutations. The
  comparisons they removed are gone from the code.** `_reads_back` compared
  the re-read's matching title, version token and addressed title. The two
  spellings `_spellings` offers re-read to the same matching title and the same
  addressed title by construction. The source's own spelling read with no
  declared version is its own address. The raw title read with the declared
  version recomposes to exactly `spelled`. Only the version token can differ,
  and W4, which removed that comparison, kills 2. Rather than keep two guards
  that cannot fire, the commit after this table removed both comparisons and
  says why in the docstring. They were labelled user facing in the row file.
  Once removed they have no surface, so there is no composite to pair.
- **W6_unreadable_spelling, maintainer facing.** A spelling the reader refuses
  counted as reading back. That changes the output only for a hand built
  `Wanted` carrying a spelling the reader refuses. Every `Wanted` the readers
  produce was read from that spelling. Either way `document` refuses the row, or
  writes the plain title and version. The author could not kill it.

## Also seen

`test_writing_the_same_list_again_is_a_no_op` asserts `second == first`, two
outputs of `write`. That comparison is X equals X on its own. The test's real
check is the unchanged modification times, which F2 kills.
