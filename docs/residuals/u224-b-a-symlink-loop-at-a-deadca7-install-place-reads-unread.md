---
title: A symlink loop at a DEADCA7 install place reads as whether DEADCA7 is installed cannot be said, where Path.is_dir answers absent
found: at the review of #576, U224, 2026-11-06.
issue: no
---

**The mechanism.** `_folder_presence` in `src/cratekit/cli/doctor.py` reads absent only for `FileNotFoundError` and `NotADirectoryError`; a stat that fails with ELOOP is unread. So `~/Applications/DEADCA7.app` linked to itself makes `crate doctor` say whether DEADCA7 is installed cannot be said, on a Mac with no DEADCA7. A dangling link reads absent.

**Measured cost.** Driven by the round one review through `crate doctor` with a self linked bundle path, the reviewer's own construction: one INFO line that hedges where "not installed" is true. The conservative side of the unread rule. No natural producer of such a link was driven.

**Closes when:** ELOOP is read as absent, or left as unread on purpose with the reason in the docstring. Ledger only.
