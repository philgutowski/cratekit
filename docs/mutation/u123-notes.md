# U123 mutation table: TWO OF TWENTY FIVE ROWS MEASURED

**Verdict.** The driver could not finish inside this relay task's ten minute
foreground call, so twenty three rows carry no death count. The gap is R-329.
All twenty five rows are committed in `docs/mutation/u123-rows.toml`, and the
partial sidecar `docs/mutation/u123.json` holds what was measured, so an
attended `--resume` reuses those rows.

## What was measured, 2026-10-10, at `b63984d`

| row | deaths | collected | note |
|---|---|---|---|
| full baseline | green | 13308 | |
| NULL_CONTROL | 0 | 13308 | the apparatus is sound |
| H1_outside_refusal | 2 | 38 of 38 | restore verified against HEAD |
| H2_no_releases_refusal | 1 | 38 of 38 | restore verified against HEAD |

One driver call, eight pytest runs, stopped by SIGINT at 540 seconds while the
third row's run was being guarded. `git diff HEAD -- src` was empty afterwards.
How the 540 seconds split between the two full runs and the rows was not
sampled, so no figure is offered for it.

## Not measured

H3 to H15, C1, T1 to T5, L1 to L3 and D1. Each guard has a test in
`tests/test_label_heard.py` written to drive it, and that is the author's
expectation, not a measurement. Two rows were considered and dropped, with the
reason, in the rows file.

## To finish it

From an attended session, on a tree whose sources match this branch:

    ./.venv/bin/python scripts/mutate.py docs/mutation/u123-rows.toml --resume

`--resume` reuses H1 and H2, and every row after them runs. A zero on a user
facing row then owes the composite METHOD describes.
