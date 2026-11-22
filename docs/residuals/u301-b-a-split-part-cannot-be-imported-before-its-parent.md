---
title: A part split from core.jobs or core.review cannot be imported before its parent
found: at the review of #858, U301, 2026-11-22.
issue: no
---

**The mechanism.** U301 split `core/jobs.py` (the drive loop into
`core/jobs_drive.py`) and `core/review.py` (into `review_holds`,
`review_exchange`, `review_groups` and `review_surfaces`). Each part imports
names from its parent and the parent imports the part back at its foot, so
`import cratekit.core.jobs_drive` in a fresh interpreter, before
`cratekit.core.jobs`, raises ImportError on a partially initialized module.
Every moved class and function carries its parent's `__module__`, so a pickle
names the parent and a fresh process imports the parent first; the side
effect is that `inspect.getsource` cannot find a pinned class's source.

**Measured cost.** None driven: three candidates were driven and none imports
a part first (the module walk in `tests/test_cli_contract.py` imports parents
first and swallows errors; a pickle round trip of `Hold`, `DriveResult` and
`Interrupt` into a fresh interpreter works; no base caller of a part exists).
Nothing in `src` or `tests` calls `inspect.getsource` on a moved class.

**Closes when:** a caller needs a part on its own; then the part reads its
parent lazily inside the functions that need it. Ledger only.
