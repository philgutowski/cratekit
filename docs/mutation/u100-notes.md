# U100 mutation tables, read

Three tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/145`. Every zero row in this record means the
author could not kill it, not that nobody could.

**`u100-a.md`**, 11 rows over `label/harvest.py` and `label/registry.py` at
`7f6bf64`, subsets derived from imports, null control 0 of 8229, no collect
drift, every restore verified against `git show HEAD`. 9 killed, 2 zero.

**`u100-b.md`**, 10 rows over `label/cli.py` at `b16a1d5`, subset
`tests/test_label_registry_adopt.py` and `tests/test_label_registry_verbs.py`
named explicitly, because no test imports `cratekit.label.cli` to reach adopt
and a derived subset would have missed the adopt tests. Null control 0 of 8230,
no collect drift, every restore verified. 9 killed, 1 zero.

**`u100-c.md`**, the three zero rows measured again at `68fa9bb` after the fix
round, null control 0 of 8230, every restore verified. All 3 killed.

24 rows in all, 21 distinct mutations and 3 re-measures, under the cap of 25.
Two more were considered and logged as dropped in `u100-b-rows.toml`: reading
the name from the payload before the identity, which the only producer writes
equal so no reachable input tells them apart, and the strict pairing of results
to items, which cannot mismatch by construction.

## The three zeros, and what each bought

- **R5 and R6, the write skip.** `RegistryStore.adopt` returning False when it
  added nothing, and `update` honouring that. The idempotence test compared the
  file after the second run with the file after the first, and those bytes are
  equal whether or not the second run wrote. The cost of a needless write is
  real and was not tested: `recognize` drops a record it cannot read, so saving
  what it loaded discards that record. The zero bought
  `test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`, over a
  registry holding one unreadable record, and `u100-c` measures each at 1 kill.
- **C8, a refused name reported as present.** Nothing asserted `present` on the
  no identifier path. One assertion in
  `test_a_name_with_no_identifier_fails_alone_and_the_rest_land`, and `u100-c`
  measures it at 1 kill.

## What the kills say

The R-381 hazard is held on its own row. R1 replaces the presence resolution
with a slug lookup and is killed by the carried over `Sueño` test, which is the
only test that reaches a name whose slug differs from its held identifier. R3,
resolving against the file as loaded rather than the entries this run added, is
killed only by the two spellings in one run test, so that test is the whole
guard for in batch duplicates.

The verdict filter is held from both sides, a rejected item adopted (H1a) and an
open one adopted (H1b), by separate assertions in one test. The kind filter
(H2) is held by a sweep release on the same queue, which is the population the
filter exists for. C9, the dispatch, kills 12 because every adopt test goes
through it.
