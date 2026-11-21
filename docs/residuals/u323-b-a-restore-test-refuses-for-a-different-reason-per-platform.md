---
title: The restore test of a reconciliation store on an unmounted volume refuses for a different reason on each platform, and its assertion names none
found: at the review of #914, U323, 2026-11-21.
issue: no
---

**The mechanism.** In `tests/test_restore.py`,
`test_a_reconciliation_store_on_an_unmounted_volume_is_not_an_empty_one`
ends on `pytest.raises(CratekitError)` around `close_session`, with no seam
for the volume identity. Driven at the review of U323 with the platform
provider patched: answering none, as Linux does, it refuses
`library-volume-mismatch`; answering a foreign UUID, as a Mac does, or the
recorded volume, it refuses `library-volume-unmounted`. The assertion takes
either.

**Measured cost.** None to a person: it refuses on both. The test cannot tell
which refusal it proved, so a change that broke the unmounted reading on one
platform would pass there through the other.

**Closes when:** the test passes the identity it means and asserts the
reason it expects. Ledger only.
