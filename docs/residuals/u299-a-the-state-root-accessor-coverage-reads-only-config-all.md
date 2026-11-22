---
title: The composed path lint's accessor coverage reads only config.__all__, so an accessor left out of it escapes both checks
found: at the review of #856, U299, 2026-11-22, round two.
issue: no
---

**The mechanism.** `tests/test_config.py` holds the composed path lint to
`_STATE_ROOT_ACCESSORS` and checks that set against the `*_dir` names in
`config.__all__`. A new directory accessor that is not listed in `__all__`
escapes the coverage test, and a module composing a path under it then
escapes the lint as well. The review drove it with a planted
`library_scratch_dir` and a consumer composing under it: both checks stayed
green on the branch (accessor in `core/state_files.py`) and equally on `main`
at `c919209` (accessor in `core/config.py`, left out of `__all__`). The miss
predates U299.

**Measured cost.** None to a user today: no such accessor exists. It is a
guard that checks a declared list rather than the definitions.

**Closes when:** the coverage test reads every public function returning a
directory from config and its parts (U299's `config_parts()` in the same file),
not `__all__`. Ledger only.
