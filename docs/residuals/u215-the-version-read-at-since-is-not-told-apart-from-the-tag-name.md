---
title: No test tells the version written at a release plan's --since from the version its tag name spells
found: at the review of #529, U215, 2026-11-05.
issue: no
---

**The mechanism.** `cmd_plan --since` reads the base version with `version_at`,
the `pyproject.toml` version at that commit. Reading it from the tag's name
instead, `dotted(parse_tag(since))`, passes all of `tests/test_release.py`,
because every fixture tag, like every real one, names the version written at
its commit.

**Measured cost.** None: the two readings agree on all six real tags, so no
range produces a difference. Sharper mutations of `version_at` die. The test
that names this behaviour cannot tell the two apart.

**Closes when:** a test tags a commit whose `pyproject.toml` version differs
from the tag name, if that shape is ever wanted. Ledger only.
