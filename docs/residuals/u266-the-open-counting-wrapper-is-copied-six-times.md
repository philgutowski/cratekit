---
title: The test wrapper that counts container opens is copied in six test files
found: at the review of #695, U266, 2026-11-12.
issue: no
---

**The mechanism.** U266 added two more copies of a wrapper over `mutagen.File`
that counts container opens, in `tests/test_setbuilder_one_open.py` and
`tests/test_setbuilder_cli.py`, beside the ones in
`tests/test_rebuild_one_open.py`, `tests/test_library_reads_remembered.py`,
`tests/test_match_states.py` and `tests/test_analysis_ahead.py`. Its
`_tagged` helper also repeats most of `tests/_containers.tagged_container`.
Six copies of one counter can drift apart in what they count.

**Measured cost.** Maintenance only; no test is wrong today.

**Closes when:** one shared open counting fixture lives beside the container
helpers and the six suites use it. Ledger only.
