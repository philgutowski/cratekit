---
title: "pyrekordbox binds its own process probe, so a test that fakes the utils name still reads the host's process table"
date: 2026-11-07
category: workflow-issues
module: "tests/conftest.py, tests/_host_processes.py, src/cratekit/core/rb_writer.py, src/cratekit/core/processes.py"
problem_type: workflow_issue
component: test_isolation
severity: high
root_cause: bound_import
resolution_type: guard
applies_when:
  - "The Mac battery is red only while rekordbox is open, and green on Linux and on a Mac with rekordbox quit"
  - "A test fakes a running or absent rekordbox by patching pyrekordbox.utils.get_rekordbox_pid"
  - "A new test or a new code path asks whether rekordbox is running"
symptoms:
  - "A release cut refused on a red battery while rekordbox was open on the machine"
  - "A gated write exits 1 at commit with RuntimeError: Rekordbox is running"
  - "A verb exits 21 (rekordbox running) in a test that never faked rekordbox"
tags:
  - "test-isolation"
  - "process-table"
  - "pyrekordbox"
  - "rekordbox-running"
  - "u232"
  - "conftest"
---

# pyrekordbox binds its own process probe, so a test that fakes the utils name still reads the host

## What happened

The v0.13.0 cut was refused on a red Mac battery because rekordbox was open
on the machine. Two tests read the host's real process table. One exited 21
for a rekordbox it should never have seen. The other faked
`pyrekordbox.utils.get_rekordbox_pid` and still exited 1, at a commit
pyrekordbox refused with "Rekordbox is running".

## Why

`pyrekordbox.db6.database` does `from ..utils import get_rekordbox_pid` and
asks that bound name at construction (a warning) and inside `commit` (a
`RuntimeError`). Patching the name on `pyrekordbox.utils` leaves the
binding's own reference walking the real host. Both of pyrekordbox's names
call `utils.get_process_id` by its global, which is the one place all three
routes meet. The careful scan, `core.processes`, reaches the host through
`_platform()`, which is psutil.

Measured on the base with the whole suite run as if rekordbox were open
(below): 96 tests red beyond the Linux machine failures, every one a
rekordbox refusal, not two.

## What to do

Nothing, for an ordinary test: since U232 `tests/conftest.py` answers both
routes as a machine with no rekordbox (`processes._platform` an empty table,
`pyrekordbox.utils.get_process_id` no process), and psutil's `process_iter`
and `pids` beneath them fail any test that reaches them. To fake rekordbox
running, patch either seam, or `rb_writer.rekordbox_running`, on the test's
own `monkeypatch`, which wins. A test that needs pyrekordbox's real walk over
its own fake `psutil.process_iter` puts the real `get_process_id` back, as
`tests/test_process_scan.py`'s `real_probes` does. A test that needs the
real host carries `@pytest.mark.real_process_table`.

To see the suite as a Mac with rekordbox open would, on any machine:

    .venv/bin/python -m pytest -p tests._host_processes

which puts a `rekordbox` and a `rekordboxAgent` on psutil's own table for the
session. Compared against the machine's own failures it should change
nothing. Real processes of those names work too: copy `/bin/sleep` to a
scratch directory as `rekordbox` and `rekordboxAgent` and run them. That is
how the review found the one assertion that held only when rekordbox was
not really open, a pid pyrekordbox answered first.
