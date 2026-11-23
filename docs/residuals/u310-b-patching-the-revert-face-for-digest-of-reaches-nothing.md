---
title: Patching digest_of on the revert module reaches nothing since the ledger was split
found: at the review of #867, U310, 2026-11-22.
issue: no
---

**The mechanism.** `adopt/revert.py` was split into `revert.py`,
`revert_record.py` and `revert_changed.py`. `revert.py` re-exports
`digest_of`, but its only callers are in `revert_changed.py`, which resolves
its own module global. A test that patches `cratekit.adopt.revert.digest_of`,
the site every such test used before the split, now changes nothing and
passes or fails for another reason. The thirteen tests that patch it were
moved to `revert_changed` and each was shown to bite.

**Measured cost.** None to a person: no production path is affected. Base
`tests/test_adoption.py` with its patches unchanged, run over the branch's
source, fails 11 tests beyond the machine set, which is how the review
measured it.

**Closes when:** a guard refuses a patch of a name a module only re-exports,
or the re-export is dropped once nothing outside imports it from `revert`.
Ledger only.
