---
title: The two beat grid suites took 341 added lines from three feature cards during the refactor, so U315's literal log over them is not empty
found: at the build of #872, U315, 2026-11-23.
issue: no
---

**The mechanism.** U315's brief measures point 7 as `git log ff8e5ec..main` over `tests/test_no_beatgrid_ever.py` and `tests/test_rb_writer_guard.py` being empty. It prints six commits: `eac3d93c` (U288), `75146b96`, `c8c25cea`, `dc262e14` (R-1830), `6940bf84` and `c8e604f9` (U327), all feature cards outside the epic. `git diff --stat ff8e5ec main` over the two files is 341 insertions and 0 deletions: every line at `ff8e5ec` is still there, and no epic card's commit touches either file. The definition of done says the suites are untouched by the refactor; the instrument the audit brief chose also counts feature cards that added guards.

**Measured cost.** None to a user: the guards only grew. The audit took the conservative reading that point 7 holds for the refactor, named the six commits, and asked Phillip on #872 which reading holds.

**Closes when:** Phillip answers on #872, and #987 (U338) measures point 7 by the epic's commits, or by every commit, as he answers. Ledger only.
