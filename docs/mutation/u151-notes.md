# U151 mutation table, measured

Sixteen rows in `docs/mutation/u151-rows.toml`, a light pass on
`scripts/board.py`, all maintainer surface. None dropped.

**Measured 2026-10-26 on a Mac, closing R-1036.** All sixteen killed. The
baseline was green at 14121 collected, the null control killed 0, every row
collected 59 on its three file subset, and every row's restore was verified
against HEAD. Each row was killed by the test named below; M2, U1 and X4 were
killed by more than one. The table is `docs/mutation/u151.md`, its sidecar
`docs/mutation/u151.json`.

It was authored and unmeasured at the build. The unit was built on Linux,
where 93 tests in 13 files fail for want of macOS tooling or behaviour
(`hdiutil`, `rclone`, an NFD filename fixture, an FFmpeg channel layout), and
`scripts/mutate.py` refuses a red full baseline and drops an inherited
`PYTEST_ADDOPTS`, so no row could run there.

To measure it again, on a Mac with a green suite:

    .venv/bin/python scripts/mutate.py docs/mutation/u151-rows.toml

The rows, and the test meant to kill each:

| Row | Mutation | Expected killer |
|---|---|---|
| O1 | owner filter dropped | `test_a_card_on_another_project_or_owner_is_not_this_boards` |
| O2 | owner match case sensitive | same, the owner case row |
| N1 | project number filter dropped | same, the number row |
| M1 | per issue membership count dropped | `test_an_issue_whose_memberships_come_back_short_is_refused` |
| M2 | repository issue count dropped | the U148 short read tests in `test_board_reads.py` |
| C1 | no cursor guard dropped | `test_a_page_that_says_more_and_gives_no_cursor_is_refused` |
| C2 | page bound loses its last page | `test_one_row_under_the_limit_is_taken_as_whole` |
| F1 | cursor passed as `-F` | the pagination test in `test_board_cost.py` |
| A1 | archived cards read | the query shape test in `test_board_cost.py` |
| U1 | Unblocks written on every card | `test_an_unchanged_unblocks_number_is_not_written` |
| U2 | an added card reads as holding 0 | `test_an_issue_off_the_board_is_added_then_given_its_status_and_number` |
| X1 | `next` skips the project read | the token visibility test in `test_board_status.py` |
| X2 | no organization fallback | `test_the_context_asks_the_organization_when_the_owner_is_not_a_user` |
| X3 | Status refusal dropped | the missing Status test in `test_board_cost.py` |
| X4 | unseen project trusted | `test_a_project_the_token_cannot_see_is_refused_and_says_why` |
| X5 | field count dropped | `test_a_project_whose_fields_come_back_short_is_refused` |
