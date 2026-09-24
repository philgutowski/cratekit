# Mutation notes: r695

Author's table, no independent verifier (METHOD, 2026-09-07). Eight rows in
`r695-rows.toml`, under the cap, all in `write/routing_cli.py`: three on the
two remedy texts, three on the new `export_remedy` builder, two on its two
callers. Light pass, because the unit changes what a warning says and writes
nothing.

**NOT MEASURED.** There is no `r695.md` or JSON sidecar, because the driver
never got past its full baseline. Every row is unmeasured, so the table says
nothing about kills. The touched suite was run after every edit, and each row
below names the test written to kill it.

Why: the same `crate analyze vocals --recursive` job over the whole DJ library
that halted R-689's, R-693's and R-694's tables, `2026-09-24T21:04:27Z-fbe8`,
was still running against the installed copy, one hour and fifty four minutes
in when the halt was read. The driver's state leak guard stopped the batch
when the application support directory grew from 7,165 to 7,205 entries
during the baseline.

The run is repeatable as written, with no cratekit job running:

    ./.venv/bin/python scripts/mutate.py docs/mutation/r695-rows.toml

Every row's subset is `tests/test_routing_workers.py`.

| Row | What it reverts | Written to kill it |
|---|---|---|
| T1 | the inbox remedy says the library is still filed through an export, the defect | `test_without_export_a_library_with_no_native_tree_names_the_export_remedy` and the four gate and empty inbox tests, all comparing the literal `INBOX_REMEDY` |
| T2 | the inbox remedy drops the review and the hand filing | the same five, and `test_a_taxonomy_with_no_long_track_playlist_gets_the_review_alone_as_its_remedy` |
| T3 | the unplaced remedy says it places what the tree does not hold | `test_without_the_flag_nothing_is_written_and_the_answer_names_the_flag`, the full text |
| B1 | the long track playlist is never named | the five `INBOX_REMEDY` tests, on the shipped declaration |
| B2 | a long track playlist is named whatever the declaration holds | `test_a_taxonomy_with_no_long_track_playlist_gets_the_review_alone_as_its_remedy` |
| B3 | the shipped playlist name instead of the declared one | `test_the_remedy_names_the_long_track_playlist_the_active_copy_declares`, added for this row |
| C1 | the plan carries the bare review, so the gate and the declined answer lose the playlist | `test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer`, and the declined half of the no long track test does not, since the bare review is its expected text |
| C2 | the applied answer carries the bare review | `test_without_export_a_library_with_no_native_tree_names_the_export_remedy`, and the empty inbox test's applied half |
