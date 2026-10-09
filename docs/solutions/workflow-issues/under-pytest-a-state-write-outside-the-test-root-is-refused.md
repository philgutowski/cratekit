---
title: Under pytest, a state write outside the test root is refused, whatever the environment says
date: 2026-10-09
category: workflow-issues
module: src/cratekit/core/config.py, tests/conftest.py
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: environment_only_isolation
resolution_type: guard
applies_when:
  - A test, probe or helper raises WriteOutsideTestRoot naming a path.
  - A test deliberately aims a write at a real location, such as the read only
    system volume, to prove what the kernel answers.
  - A child process started by a test imports a helper from tests and writes.
  - Shipped code is given a new scratch location outside the system temporary
    directory.
tags:
  - test-isolation
  - conftest
  - config
  - r-926
  - write-outside-test-root
  - probe
---

# Under pytest, a state write outside the test root is refused, whatever the environment says

## What happened

On 2026-10-08 a review subagent wrote a probe test in its own scratch
folder, imported two fixtures from `tests/test_repair_rows.py`, and ran the
worktree's pytest on it from there. `tests/conftest.py` loads only for files
under `tests/`, so HOME, the XDG variables and `CRATEKIT_CONFIG_DIR` were the
real machine's, and the fixture's `config.save` replaced the live
`config.toml` with a pytest library (R-926). The isolation was the
environment, and the environment is exactly what a missing conftest leaves
alone.

## The rule now in code

`_refuse_write_outside_test_root` in `cratekit.core.config` asks two things
and reads no environment variable: is pytest in `sys.modules`, and does the
resolved target sit under `config._TEST_WRITE_ROOT`, which the conftest's
`_isolate_state_roots` sets to pytest's base temporary directory for each
test. It runs in three places:

- `_write_lock`, taken first by every configuration writer (`save`,
  `update`, the migration write back). Test root only.
- `atomic_write_bytes` and `_exclusive_lock`, which every other state writer
  uses. Test root, or the system temporary directory, registered root or not.

## What a future session would get wrong

- **The temporary allowance is load bearing.** Shipped code writes a provider
  session token and a scratch config into `tempfile.mkdtemp` folders through
  `atomic_write_bytes`. Holding the primitives to the test root alone refused
  101 tests. A test's child process that imports anything from `tests` has
  pytest loaded and no conftest, so no root, and it writes its locks under the
  test's own folder; that is why the allowance does not wait on a root.
- **The configuration never gets the allowance.** A configuration save into a
  mkdtemp folder under pytest is refused on purpose, so a probe in the system
  temporary directory cannot pass a real config path through it.
- **A test that means to write somewhere real widens the root for itself.**
  `test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`
  aims at `/` to get the kernel's EROFS, and sets `config._TEST_WRITE_ROOT`
  to `/` on its own monkeypatch. Do that in the test, never in the guard.
- **What it cannot see.** A child process with no pytest loaded is never
  checked and still trusts the environment it inherited (R-931). A probe still
  goes under `tests/`.
