# U129 mutation notes

Author's table in `docs/mutation/u129-rows.toml` (20 rows, light cap 25). Soft
skip paths, the gate before the queue, the landing archive warning fold, and
the backfill listing are the user facing surfaces; the export set and archive
bodies were already covered by R-837's table.

## Rows driven

| # | Id | Guard | How mutated | Covering test |
|---|----|-------|-------------|---------------|
| 1 | A1 | account gate before enqueue | move ask after enqueue | test_a_set_intake_plans_and_makes_the_account_playlist |
| 2 | A2 | gate ask dropped | return apply without require | test_a_set_intake_plans_and_makes_the_account_playlist |
| 3 | A3 | abort still writes | apply even on abort | test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist |
| 4 | A4 | archive raise fails landing | let raise escape | driven land archive failure test |
| 5 | A5 | archive return discarded | discard apply_archive warnings | driven land archive not-renamed test |
| 6 | A6 | archive notes not on envelope | drop warnings.extend(archive_notes) | driven land archive tests |
| 7 | A7 | with_archive omits digest | omit archive from identity | test_with_archive_folds_into_the_landing_digest |
| 8 | A8 | land writes without remote | drop remote from writes | test_intake_land_declares_remote_and_provider_for_the_archive |
| 9 | A9 | land without provider check | drop credential.provider | test_intake_land_declares_remote_and_provider_for_the_archive |
| 10 | A10 | export set without library.mounted | drop library.mounted | test_export_set_and_archive_declare_library_mounted_for_backfill |
| 11 | A11 | export archive without library.mounted | drop library.mounted | test_export_set_and_archive_declare_library_mounted_for_backfill |
| 12 | A12 | archive backfill swallows all | catch Exception | soft skip and CredentialError refuse tests |
| 13 | A13 | job lookup uses today | drop naming day | other-day and 23:30 local tests |
| 14 | A14 | export set backfill hides made | drop mid-loop naming | mid-fail and CredentialError mid-loop tests |
| 15 | A15 | archive backfill hides filed | drop mid-loop naming | archive mid-fail test |
| 16 | A16 | soft skip re-raises | re-raise CratekitError | soft skip path on intake set |
| 17 | A17 | empty add still writes | force writes True | test_a_set_with_no_matches_makes_nothing_and_says_so |
| 18 | A18 | frozen name ignored | return empty frozen name | frozen name / backfill |
| 19 | A19 | plan archive always none | return None | test_plan_archive_named_skips_the_intake_file_check |
| 20 | A20 | apply archive skips rename | skip rename_playlist | export archive and land rename tests |

## Skipped (ranked below the cap)

- Inspiration sort order, waiting-set shown context, tracklist-vs-apply order,
  abort outcome word, session-scan fallback, unnamed warning drop: ranked
  below the cap.

## Low note

The playlist name uses today's date while the gate sits before the queue, so a
resume on a later day rebuilds the name and refuses with DecisionStale. The
"resume" remedy in the export set backfill meets the same stale digest once
finished playlists drop out of missing.

## Archive order inside write

The account archive runs inside ``write()`` after ``apply_native`` commits but
before ``assert_rows_gridless`` and ``assert_rows_identified``, with the
database handle still open. A later check failing leaves the account saying
DOWNLOADED. Moving the archive after those checks is the better order when it
is a small change; left as a note for now.

## Verdict

Author's table only; watcher measures on macOS.

## Gate before recognition (fifth round)

The account gate digests the playlist name alone (``intake-set-account``), so it
can fire from the name flags before recognition and before any mix download, or
from the mix page after a fetch and still before ACRCloud. Tracks are matched
after recognition when the write is applied. A resume reuses the recognition
cache for chunks already answered; a mix download is not cached across runs.

## Mix URL with no page

A mix URL whose fetch left no info document is warned as ``set-account-unnamed``
the same way a page that left a word out is: the person gave an address, so the
account step was expected. A bare local recording with no name flags stays silent.

