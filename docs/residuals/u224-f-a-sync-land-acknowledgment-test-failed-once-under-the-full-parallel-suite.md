---
title: test_the_acknowledgment_stop_names_the_gate_the_replanned_landing_will_ask failed once under the full parallel suite on the cloud container and passes alone
found: at the battery of #576, U224, 2026-11-06.
issue: no
---

**The mechanism.** Unmeasured. `tests/test_sync_land.py::test_the_acknowledgment_stop_names_the_gate_the_replanned_landing_will_ask` failed in one `cloud_battery.py compare` run of the whole suite at cb92bbfd, U224's branch with `main` merged in, and passed in the run before it at cf7cd4fd. Alone it passed three times, and its file passed whole under `-n auto`. U224 changes only `crate doctor`'s DEADCA7 check, which that file never names; the merge brought only `docs/cutover.md`.

**Measured cost.** Maintainer facing: one run in two of the full suite on this container. Its failure output was not kept, so the cause is not known.

**Closes when:** a run that keeps the failure's output names what it shares under the parallel run, and the test is made independent of it. Ledger only.
