# Mutation notes: r694

Author's table, no independent verifier (METHOD, 2026-09-07). Seventeen rows
in `r694-rows.toml`, under the cap, all in `write/routing_cli.py`: four on the
inbox sweep's new branch between a review and a pending import, three on the
inbox review warning, two on the unplaced sweep's ending, four on the shared
warning helper, four on the pending import's new text. Light pass, because
the unit changes which answer a run gives and what it says, and writes
nothing a run did not already write.

**NOT MEASURED.** There is no `r694.md` or JSON sidecar, because the driver
never got past its full baseline. Every row is unmeasured, so the table says
nothing about kills. The full suite was green at the branch head, the touched
suites were run after every edit, and each row below names the test written
to kill it.

Why: the same `crate analyze vocals --recursive` job over the whole DJ
library that halted R-693's and R-689's tables, `2026-09-24T21:04:27Z-fbe8`,
started from another session against the installed copy, was still running,
one hour and forty one minutes in when the halt was read. It writes one
analysis artifact per track under the application support directory, so the
watched root grew from 6,713 to 6,743 entries while the baseline ran and the
driver's state leak guard stopped the batch. The job's own process was alive
when the halt was read, the second shape in the solutions entry on null
control halts.

The run is repeatable as written, with no cratekit job running:

    ./.venv/bin/python scripts/mutate.py docs/mutation/r694-rows.toml

Every row's subset is `tests/test_routing_workers.py`.

| Row | What it reverts | Written to kill it |
|---|---|---|
| B1 | the inbox sweep ends pending on every written file, the defect | `test_the_check_run_after_the_playlist_import_owes_no_import`, and every inbox test now asserting exit 0 on a written file |
| B2 | the inbox sweep never owes an import | `test_an_export_run_owes_the_import_of_the_root_playlist_it_added_to_alone`, `test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not` |
| B3 | the declaration half of the branch is gone | expected to survive: `lengthened` is nonzero only when `apply_export` had a declared playlist to add to, so the half is unreachable. Maintainer facing, kept for the type narrowing it gives the next line |
| B4 | a nested only inbox file ends no_op | `test_an_export_inbox_lands_each_track_in_its_declared_sub` asserts `Outcome.OK` |
| W1 | the inbox review warning is dropped | the same test pins the warning text; `test_an_owed_star_rating_is_not_written_into_the_export` unpacks exactly one |
| W2 | the inbox remedy names no step | `test_an_export_inbox_lands_each_track_in_its_declared_sub`, the full text |
| W3 | the inbox warning ignores the created vocal subs | `test_vocal_subs_alone_are_a_change_and_write_a_file`, `test_a_calibrated_export_files_over_the_cut_and_not_under_it` |
| W4 | the unplaced review warning is dropped | `test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created`, the full text |
| W5 | the unplaced review ends no_op | the same test and `test_the_unplaced_check_run_owes_no_import_before_the_tracks_are_filed` assert `Outcome.OK` |
| H1 | the helper warns only on a routed membership | `test_vocal_subs_alone_are_a_change_and_write_a_file`, zero routed and two subs |
| H2 | the helper warns over a file with nothing nested | `test_a_long_track_alone_is_a_change_and_writes_a_file`, zero routed and zero subs, asserts no review warning |
| H3 | the warning stops naming created subs | `test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created`, the full text |
| H4 | the warning stops giving the reason | both full text tests |
| P1 | the first step goes back to any root playlist | `test_an_export_run_owes_the_import_of_the_root_playlist_it_added_to_alone`, the full steps |
| P2 | the tree step is dropped | the same |
| P3 | the check step promises a run that plans nothing | the same |
| P4 | the summary claims the routing | the same, the full summary |

**B3 is the one row the author expects to survive**, for the reason in its
line. H2 was expected to survive when the table was authored, since no test
read the warnings of a file of long tracks alone, and that test now asserts
there is no review warning, so it is written to die.
