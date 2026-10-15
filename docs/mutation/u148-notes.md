# U148 mutation notes

**UNMEASURED.** The seventeen rows in `u148-rows.toml` were authored and the
driver run twice on 2026-10-15, and both runs stopped at the full baseline on
`STATE LEAK`: the real installation state directory grew by two and then three
entries while the baseline ran. Both times a live attended sitting was running
`crate` verbs against it (`live_gate.sh mirror-s42`, `crate organize --only
mirror`, then `crate favorites backfill`), read with `pgrep` before and after
each run, so the writer was the sitting and not a child of the driver, and no
row was measured. `scripts/board.py` was checked equal to `HEAD` after each stop.

So no row has a death count, and none is reported as zero. The guards the rows
target are each asserted by name in `tests/test_board_reads.py`:

| Row | Guard | Test written to kill it |
|---|---|---|
| L1, L2, L3 | the limit asked of `gh` | `test_every_issue_and_project_item_is_read_past_three_hundred`, `test_both_reads_ask_gh_for_the_limit` |
| W1 to W4 | a read that fills the limit | `test_a_read_that_fills_the_limit_is_refused_by_name` |
| C1, C2, C6 | the item count | `test_items_short_of_the_projects_own_count_are_refused` |
| C3, C4 | a read with no count | `test_an_item_read_with_no_count_is_refused`, `test_an_issue_count_that_is_not_a_number_is_refused` |
| C5 | the issue count | `test_issues_short_of_the_repositorys_own_count_are_refused` |
| C7 | count before read | `test_issues_filed_after_the_count_are_read_and_not_refused` |
| N1 | `next` and a truncation | `test_next_refuses_a_truncated_item_read_rather_than_blame_the_token` |
| S1, S2 | `start` | `test_start_reads_the_board_before_it_branches`, `test_start_says_so_when_the_card_is_not_on_the_board` |

That table is the author's claim of intent, not a measurement. Rerun with no
`crate` verb live (`pgrep -lf "crate --output"` empty), from the checkout:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/u148-rows.toml
