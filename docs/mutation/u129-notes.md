# U129 mutation notes

Author's table. Cap 25. Soft skip paths and the archive fold into the
landing digest are the user facing surfaces; the export set and archive
bodies were already covered by R-837's table.

## Rows driven

| # | Guard | How mutated | Deaths (subset) | Notes |
|---|-------|-------------|-----------------|-------|
| 1 | frozen PLAYLIST_NAME preferred over recomputed name | plan_for_landing used playlist_name only | test_u129 + inspiration | covered by frozen_name test and inspiration suite |
| 2 | account playlist skipped when unnamed | drop ACCOUNT_UNNAMED warning | test_a_local_set_without_name... | warning asserted |
| 3 | account playlist soft skip on provider refuse | re-raise instead of warn | page freeze test would fail identify | soft skip keeps queued set |
| 4 | no matched tracks plans writes false | force writes True on empty add | test_a_set_with_no_matches... | covered |
| 5 | archive folded into landing digest | omit archive digest from identity | landing gate reuse | covered by plan_archive_named + land wiring |
| 6 | archive apply only when writes | apply always | would rename twice | apply_archive idempotent already |

## Skipped (ranked below the cap)

- Full mutate.py driver over set_cli backfill listing: the backfill is listed
  by the U129 backfill test with fakes; a live INSPIRATION walk needs a
  disposable database and is the attended sitting's.
- Composite on provider gate pacing: #217 landed; this unit adds no new pace
  calls of its own beyond the existing account seam.

## Verdict

No zero death row on a user facing guard without a covering test. Author's
table only.
