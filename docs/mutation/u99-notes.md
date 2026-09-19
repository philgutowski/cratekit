# U99 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/144`. Every row's subset was the three label
test files, `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`
and `tests/test_label_workers.py`.

**`u99-a.md`**, 13 rows over `label/registry.py` at `f2de30c`, null control 0
of 8211, no collect drift, every restore verified against `git show HEAD`. 12
killed.

**`u99-b.md`**, 10 rows at `3af06d6`, nine over `label/cli.py` and one that
measures A6 again, null control 0 of 8214, no collect drift, every restore
verified. All 10 killed.

23 rows in all, 22 distinct mutations and one re-measure, under the cap of 25.
Two more were considered and logged as dropped in `u99-b-rows.toml`: the track
limit and the match needle leaving the check detail, the same family as B9,
which is measured.

## The one zero

- **A6, the store's own track limit floor.** Maintainer facing when measured,
  because every test reached the store through `crate label registry`, and the
  parser's `positive_limit` refuses a limit below one before the store is asked.
  The store is not only reached through the parser: the fourth attended sitting
  carried its 47 labels through `RegistryStore.add` directly. So rather than a
  line, the zero bought a test,
  `test_the_store_refuses_a_limit_below_one_from_a_python_caller`, on `add` and
  on `edit`, and `u99-b` row A6r measures the same mutation at 1 kill.

## What the kills say

The id seed guard is held from four directions, each by its own case in the
parametrized malformed seed test: the whole refusal (A2, 7 kills), the case of
the prefix (A3, `ID:12`), the digit count (A4, a bare `id:`) and whole match
against prefix match (A5, `id:12a`). Removing the check from `add` alone (A7)
or `edit` alone (A8) each kills, so neither verb leans on the other's guard.

`edit` keeping the fields it was not handed is held per field (A10 to A12), and
the refusal of an unknown label is held against the realistic failure, a set
that quietly creates the entry (A9), not only against a crash.
