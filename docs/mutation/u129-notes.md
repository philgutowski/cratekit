# U129 mutation notes

Author's table in `docs/mutation/u129-rows.toml` (20 rows, light cap 25). Soft
skip paths, the gate before the queue, the landing archive warning fold, and
the backfill listing are the user facing surfaces; the export set and archive
bodies were already covered by R-837's table.

## Rows driven

| # | Guard | How mutated | Deaths (subset) | Notes |
|---|-------|-------------|-----------------|-------|
| 1 | account gate before enqueue | ask after enqueue / drop ask | test_u129 job count | BLOCK 1 |
| 2 | abort skips the write | apply on abort | abort test | should fix |
| 3 | archive raise is a warning | let raise escape | land archive failure test | BLOCK 2 |
| 4 | archive return is a warning | discard warnings | changed-since test | BLOCK 2 |
| 5 | archive notes on envelope | drop extend | land archive tests | BLOCK 2 |
| 6 | archive folded into digest | omit archive digest | _with_archive test | |
| 7 | intake.land declares remote | drop remote | declaration test | should fix 3 |
| 8 | landing.provider on land | drop check | declaration test | should fix 3 |
| 9 | library.mounted on export set/archive | drop check | declaration test | should fix 5 |
| 10 | archive backfill catches CratekitError | catch Exception | soft skip test | should fix 4 |
| 11 | job lookup uses queue day | use today() | other-day test | should fix 5 |
| 12 | backfill names made playlists | drop naming | mid-fail test | should fix 6 |
| 13 | unnamed warning | drop warning | unnamed local test | |
| 14 | soft skip keeps the set | re-raise | soft skip path | |
| 15 | empty add writes false | force True | no matches test | |
| 16 | frozen name preferred | return empty | frozen name / backfill | |
| 17 | landing plans archive | return None | plan_archive_named | |
| 18 | archive rename | skip rename | export archive prefix | |

## Skipped (ranked below the cap)

- Inspiration sort order, waiting-set shown context, tracklist-vs-apply order,
  abort outcome word, session-scan fallback: ranked below the cap.

## Verdict

No zero death row on a user facing guard without a covering test. Author's
table only; watcher measures on macOS.
