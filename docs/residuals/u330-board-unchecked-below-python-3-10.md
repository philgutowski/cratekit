---
title: Nothing runs board.py under a Python below 3.10, though the commit-msg hook calls it with the bare python3
found: at review round two of #979, U330, 2026-11-23.
issue: no
---

**The mechanism.** `.pre-commit-config.yaml` runs `python3 scripts/board.py closing` with `language: system`, so the hook uses whatever `python3` the committing shell finds, while `pyproject.toml` requires 3.12 and the suite and CI run 3.12 and 3.13. U330's first head used `isinstance(node, ast.AnnAssign | ast.Assign)`, which raises `TypeError` below 3.10; review round one drove it under CPython 3.9 (24 of 166 captured commands changed exit code) and the fix round put the tuple back. Reverting that fix kills no test.

**Measured cost.** Every commit refused by a traceback on a machine whose `python3` is older than 3.10. Reachability unmeasured: this container's `python3` is 3.13, and no machine whose own `python3` is below 3.10 was driven.

**Closes when:** a check runs `board.py`'s offline commands under the oldest interpreter the hook may meet, or the hook names the venv's interpreter. Ledger only.
