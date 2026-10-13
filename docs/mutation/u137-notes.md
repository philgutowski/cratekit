# U137 mutation tables, read

The author's tables, not independent, driven by `scripts/mutate.py` on
`relay/314`. Two batches, 22 rows in all under the cap of 25, nothing dropped.

**u137, at `4885d9d9`: 21 rows, 19 killed, 2 zeros.** A green full baseline of
13,747 collected, the null control at 0 on the full suite, no collect drift on
any row, every restore verified against `git show HEAD`. The four `steps.py`
rows ran on the full suite, since no test file imports that module and the
derived subset was empty; each killed on it.

| Row | Guard reverted | Deaths |
|---|---|---|
| S1 | the selection named in the area's digest document | 1 |
| S2 | the selection named in the area's facts | 2 |
| S3 | `Area.wants` letting every kind through | 6 |
| S4 | `selection` taking every kind when any is named | 7 |
| C1 | an area none of whose kinds is named still planned | 4 |
| C2 | `--only` read and then dropped | 9 |
| C3 | the parser's `choices` | 1 |
| C4 | the registry read only for a step that uses it | **0**, maintainer |
| A1 | the label steps' gate | 3 |
| A2 | the set archives' gate | 4 |
| A3 | the marks' gate | **0**, user, rerun as u137-b |
| A4 | the account's yours gate | 2 |
| A5 | the filing planned for yours | 1 |
| A6 | the filing planned for yours into an area nobody is shown | 1 |
| A7 | the filing refused over an unread registry | 1 |
| A8 | that refusal only with the labels module on | 1 |
| R1 | the adoption's gate | 3 |
| R2 | the rotation planned for yours | 2 |
| R3 | a refused rotation shown when planned only for yours | 1 |
| R4 | a planned rotation hidden when planned only for yours | 1 |
| R5 | the record labels listing's gate | 4 |

**C4, one line.** Reading the label registry under `--only adopt` costs a
local file read and changes no plan, so no test can see it; it is a
maintainer facing economy and the author could not kill it.

**A3, and what it holds.** No test world holds a landed sync pass, so with the
marks gate open `--only file` still planned no mark step, and the row read
zero over a user facing surface: a person asking for the filing alone would
be asked to approve renames. `test_each_account_kind_runs_its_own_builder_and_no_other`
records each account builder at its seam, one `--only` kind at a time.

**u137-b, at `9d77f071`: A3 rerun, killed 4** of 66 on `tests/test_organize.py`,
the four parametrized cases that name a kind other than marks. That test is
A3's composite, and the pairing is recorded here rather than by `pairs_with`,
which pairs within one batch only.
