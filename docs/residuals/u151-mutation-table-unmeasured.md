---
title: The U151 mutation table is unmeasured, because the driver needs a green full suite and Linux cannot give one
found: at the build of #332, U151, 2026-10-21.
issue: no
---

**The mechanism.** `scripts/mutate.py` refuses a batch whose full baseline is
red, and drops an inherited `PYTEST_ADDOPTS`, so a session on Linux cannot run
any table: 93 tests in 13 files fail there for want of `hdiutil`, `rclone` and
macOS filesystem and FFmpeg behaviour. U151 was built on Linux, so its sixteen
rows in `docs/mutation/u151-rows.toml` were authored and not run.

**Measured cost.** Not driven. Which of the sixteen guards a test would let
through is unknown; `docs/mutation/u151-notes.md` names the test meant to kill
each.

**Closes when:** a session on a Mac runs the table and records the result in
`docs/mutation/u151-notes.md`. Ledger only.
