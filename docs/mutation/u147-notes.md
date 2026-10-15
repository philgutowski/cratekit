# U147 mutation tables, read

The author's table, not independent, measured by `scripts/mutate.py` on
`relay/326`, twenty five rows over twenty three distinct guards in four
batches, two of them measured twice. Four batches because one batch passes the
ten minute ceiling on a foreground command once a zero is promoted to the full
suite. Row subsets were the unit's own suites, `tests/test_organize_mirror.py`
and `tests/test_organize_mirror_library.py`; every zero was promoted to the
full suite. Every batch: baseline green (14,068 collected for a, 14,070 after
the two tests batch a asked for), null control 0, no collect drift, every
restore verified against `git show HEAD`.

| Batch | Head | Rows | Killed | Zero | Refused |
|---|---|---|---|---|---|
| `u147-a` | `8da449ad` | 6 | 4 | 2 (M2, M4) | 0 |
| `u147-b` | `6c00a29d` | 7 | 7 | 0 | 0 |
| `u147-c` | `2805f778` | 7 | 7 | 0 | 0 |
| `u147-d` | `8cf496ea` | 5 | 5 | 0 | 0 |

25 measured mutations over 23 distinct guards: **all killed**, two of them
only after a test was added.

- **M2, a recorded folder reused though the root no longer lists it.** Zero on
  the full suite in batch a, user facing: nothing drove a mirror folder deleted
  on the account. `test_a_recorded_folder_deleted_on_the_account_is_made_again_rather_than_reused`
  added; killed in batch b, 1 death.
- **M4, a refused track offered again on every refresh.** Zero on the full
  suite in batch a, user facing: nothing drove the provider refusing a track.
  `test_a_track_the_provider_refused_is_not_offered_again_so_a_refresh_plans_nothing`
  added; killed in batch b, 1 death.

Dropped below the cap, logged in the row files: M7, the chunk coefficient
(the 250 track test asserts 100, 100, 50 directly); M12, an unreadable
playlist taken for one still in its folder (the labels engine's rule copied
whole, measured under R-835); A4, a nested folder mirrored as a playlist (the
library test builds one and asserts it absent).
