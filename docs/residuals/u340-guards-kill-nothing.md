---
title: Guards of U340's second genre paths that no test kills, among them read backs and digests on paths that write
found: at the review of #989, U340, 2026-11-23.
issue: yes
---

**The mechanism.** Round one removed 53 guards of the diff one at a time and
24 killed no test; round two removed 14 of the fix rounds' guards and 4
survived. The fix rounds pinned three of them (`kept_beside`'s holder
condition, the fallback half of `_filed_by`, the per track counts), and the
25 row table kills every row it holds. These remain unkilled, the starred
ones confirmed over 117 suites at round one:

- `tagging/second.py`: the read back compare*, `items` in `SecondPlan.digest`*,
  live memberships only*, live nodes only, two nodes at one path, the parent
  cycle guard.
- `organize/mirror_edits.py`: an unfile clearing the second genre*, the second
  genre in `Change.identity()`* (the step's digest) and in its read back*,
  in `item()`, the non move refusal, the band word check.
- `adopt/plan.py`: the second sub's ROUTE guard and its `sub is None` guard*,
  the second genre word on the second entry*, `review_row`'s `second_genre`
  key, the `if sub` guard on the second entry's `beside` (no shipped bucket
  lacks a place for a reading).
- `adopt/move.py`: `_own`'s claim condition*.
- The `firsts()` call sites in `adopt/apply_cli.py`*, `intake/filing.py`* and
  `organize/rekordbox.py`*; `rebuild.filed_genres`' second word*; both
  `routing_export._shown` call sites.
- The genre check in both `second.plan` and `second_cli.read_plan`, either
  alone removable.

**Measured cost.** Each was removed alone and the suite stayed green; the
behaviour at the head was driven right by both rounds. A read back, a digest
or a clear on a path that writes files can break with nothing red.

**Closes when:** a test kills each, or the guard is shown equivalent and
removed. An issue: guards on paths that write that kill nothing (the bar's d).
