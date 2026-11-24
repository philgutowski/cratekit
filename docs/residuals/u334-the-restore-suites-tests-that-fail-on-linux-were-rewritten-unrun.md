---
title: The restore suites' tests that fail on Linux were moved onto shared fixtures and checked only by reading
found: at the review of #983, U334, 2026-11-24.
issue: no
---

**The mechanism.** 26 tests in `tests/test_restore_cli.py` (no `rclone` on the container) and 8 in `tests/test_restore.py` (root ignores a directory's mode, and one backup restore) fail on every Linux container and are on the base's known failures. #983 moved them onto the fixtures and helpers it added in those files (`acked`, `record`, `remote_log`, `scratch`, `target`, `seams`, `decided`, `_refusal`, `_one_session`, `_recover`, `_two_acts`, `_refused_as`). The review compared each against `main` and found the same calls in the same order with the same arguments, but none of them could be run to a pass here, and a kill whose only killer is one of them cannot be seen by the Linux replay either.

**Measured cost.** Not driven: on Linux they fail before and after for the machine's reasons, the same 34 ids. If a rewrite were wrong, a macOS battery would show it as newly failing there.

**Closes when:** the macOS battery runs these two files on the merged tree and reports the 34 tests passing as they did on `main` at `55e958b`. Ledger only: the check is owed at a local sitting, already in the record's OWED paragraph.
