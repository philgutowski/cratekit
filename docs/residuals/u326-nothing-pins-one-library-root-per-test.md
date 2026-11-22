---
title: Nothing pins that each test gets a library root of its own
found: at the review of #932, U326, 2026-11-22.
issue: no
---

**The mechanism.** `_block_real_library_paths` in `tests/conftest.py` gives
every test a fresh library root, by `tmp_path_factory.mktemp` before U326 and
by `tempfile.mkdtemp` under one session directory since. The review drove a
mutant that hands every test in a worker one shared library root: it killed
nothing across 45 files and 4,582 tests. A root made outside the base temp is
killed (four tests, R-926's write root), so where the root sits is pinned and
whether it is shared is not. True before U326 as well.

**Measured cost.** Not driven past the mutant. A shared root lets one test's
library files answer a later test's walk, which is the leak the fixture's own
docstring says it prevents for `tmp_path`.

**Closes when:** a test asserts two tests' `CRATEKIT_LIBRARY_ROOT` differ and
each starts empty, in a file #869 (U312) owns. Ledger only.
