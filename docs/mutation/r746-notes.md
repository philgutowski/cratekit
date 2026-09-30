# R-746 mutation tables, read

Four tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/224`. Subsets were named per row: the native
landing suite, the two guard suites, the bridge landing suites, the write
session suite and the cutover verb suite. Null control 0 on every table, no
collect drift except the one named below, every restore verified against
`git show HEAD`. Each batch ran in the foreground under the ten minute
ceiling: 7 minutes 9 seconds, 6 minutes 22, 4 minutes 18 and 3 minutes 46.

**`r746-a.md`**, 9 rows over `core/rb_writer.py` at `9071884`, the admission
and its column policy. 8 killed, 1 zero, 1 collect drift with a kill.

**`r746-b.md`**, 9 rows at `9071884`: seven over `intake/native.py` and two
over `intake/landing.py`. 8 killed, 1 zero.

**`r746-c.md`**, 7 rows over `intake/land_cli.py` at `9071884`. 7 killed.

**`r746-d.md`**, the two zeros measured again at `80089c3`, after the test
each bought. 2 killed.

25 distinct mutations, 25 killed once the two zeros were bought, plus two
re-measures. Nothing was dropped at the cap.

## The zeros, and what each bought

- **G5, the content row read back against the playlist tables' five columns
  rather than the ten.** User facing. Zero on the subset and zero on the full
  suite: the one SQL taint test put a tempo on the row, and the tempo is in
  both lists, so the narrower policy still refused it. Bought
  `test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`, which
  taints `KeyID`, a column in the content policy and not the playlist one.
  `r746-d` measures the same mutation at 1 kill.
- **N1, every device matches so the first by identifier is stamped.** User
  facing. Zero on the full suite, and the reason was the fixture: the wrong
  device was `d-other` and the right one `d-mine`, so a choice that dropped
  the `MasterDBID` rule and kept the sort still picked `d-mine`. The wrong
  device is now `d-aaa-other`, which sorts first and is also the binding's
  own first. `r746-d` measures the same mutation at 1 kill. The lesson is
  METHOD's fourth pattern one row over: a fixture that happens to agree with
  the mutation proves nothing about the rule.

## The collect drift

- **G8, `KeyID` dropped from `CONTENT_ROW_EMPTY_COLUMNS`.** The guard suite
  parametrizes one test over the constant, so removing a member removes a
  test and the driver reports the population moving by one. The kill is
  `test_the_wider_content_policy_contains_the_playlist_policy`, which names
  the five columns the content policy adds. Read as a kill with a known
  cause, not as a drift to investigate.

## Considered and not run

- The re-check for a row that appeared between the plan and the apply,
  `_taken_since_the_plan`. No test opens a second writer in that window, so
  the row would measure zero on a path nothing in the suite produces, and a
  composite would prove only that the plan's own present detection holds,
  which N5 measures. Maintainer facing until a second writer is driven.
- The malformed buffer entry branch of `_buffer_entries`. Maintainer facing,
  refuses on a shape the binding does not produce, one line.
- The rephrasing of the shared bridge refusal in `anchored_intake_root`.
  The engine test asserts the step that names `tree cutover`; a reword row
  would measure that assertion and nothing else.
