---
title: Two recorded kills of sync land's staged download read zero since R1499
found: at the kill set replay of #860, U303, 2026-11-23.
issue: no
---

**The mechanism.** U212's table recorded two kills in
`src/cratekit/cli/sync_land.py`: `S2_download_refused_all`, which drops the
`if not listed.staged` return so a download that lands nothing always stops
the pass, and `S3_no_list_download`, which drops the info check and return
when every missing track is staged already. Each was killed by one test in
`tests/test_sync_land_staged.py`. R1499 (`f02eff82`) changed what a pass does
beside an unlanded pass's staged files, from landing them to refusing, and
renamed both tests to the refusing behaviour
(`test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`,
`test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`).
Neither renamed test, nor any other, fails on either mutation now: U303's
replay before, on `main`'s code at `fd8173d3`, read both as zero on the
subset and again on the full suite (`docs/mutation/u303-replay-before-c.md`).
So the two lines are either no longer reached on the paths the tests drive, or
reached with nothing checking what they do.

**Measured cost.** None to a person shown: the refusal R1499 added comes
first on the paths the renamed tests drive. The cost is to the kill set: two
guards the ledger counts as killed are not, and `killset.py check` passes
U303 on them only because they read zero before as well as after. U303 does
not change either line, so the zeros are not this card's.

**Closes when:** the next unit that edits sync land's staged download either
shows the two branches unreachable and removes them, or writes the test that
kills each. Ledger only.
