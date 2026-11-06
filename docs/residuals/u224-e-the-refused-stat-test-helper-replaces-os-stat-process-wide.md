---
title: The U224 test helper that refuses os.stat replaces it process wide and assumes every caller passes a path
found: at the review of #576, U224, 2026-11-06.
issue: no
---

**The mechanism.** `_refuse_stat_under` in `tests/test_doctor.py` patches `os.stat` for the whole process during `doctor.run` and builds `Path(path)` from every argument before deciding, so a caller inside the run that passes a file descriptor or bytes would raise TypeError rather than see a refusal or a real stat.

**Measured cost.** Maintainer facing. The 28 U185 and U224 cases pass on this container, so no such caller is reached today; a later check that stats a descriptor would fail those tests for a reason they do not name.

**Closes when:** the helper refuses only a `str` or `PathLike` argument under the path and passes everything else to the real call. Ledger only.
