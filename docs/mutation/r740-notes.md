# R-740 mutation tables, read

Three tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/222`. Subsets were named per row: the naming,
landing, landing head and intake pipeline test files, plus the collection XML
and no beatgrid suites for E2. Null control 0 on every table, no collect
drift, every restore verified against `git show HEAD`.

**`r740-a.md`**, 7 rows over `core/naming.py` at `dcd6e07`, the head fill in
`normalize_spec`. 6 killed.

**`r740-b.md`**, 7 rows at `dcd6e07`: five over `intake/ingest.py` and two
existing guards sampled, the library name's coupling to the title tag and the
intake row's gridless `AverageBpm`. 6 killed.

**`r740-c.md`**, row I2 measured again at `c2360ac`, after the test its zero
bought. 1 kill.

15 rows, 14 distinct mutations and one re-measure, under the cap of 25.
Nothing was dropped.

Two baselines went red and one batch stopped on a state leak before any row
ran, all while a real `crate backup run` and a `crate doctor` from the installed
copy were running on the same machine. The red tests were a timing test and an
intake listing test, each green when run alone three times. The leaked entries
were `doctor` run records whose times fall outside every suite this session
ran. Each batch was rerun and the tables above are the valid runs.

## The zeros

- **N7, the head's tempo converted to an integer.** Maintainer facing. Left as
  text, a filled tempo renders the same bytes, and the only difference is that
  a spec supplying an integer tempo no longer agrees with the head. No producer
  supplies a tempo without a key: analysis supplies both, the naming verb
  derives its tempo from the same head, and `read_meta` supplies none.
- **I2, `read_meta`'s filename fallback, zero on the first table.** User
  facing. `normalize_spec` already fills from the stem head when the key tag
  agrees or is absent, so the fallback matters only when the key tag disagrees
  with the filename's head. The zero bought
  `test_a_filename_head_wins_over_a_disagreeing_key_tag`, and `r740-c` measures
  the same mutation at 1 kill.
