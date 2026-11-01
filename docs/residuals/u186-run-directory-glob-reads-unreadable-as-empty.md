---
title: The sibling run warning and doctor's runs.open-gates note read a run directory Path.glob cannot list as holding no run
found: at the review of #394, U186, 2026-11-01.
issue: no
---

**The mechanism.** `gates.siblings` and doctor's `_check_open_gates` list the
run records with `run_dir().glob("*.json")` and rescue an `OSError` as no
records. Measured on this interpreter by the status reader's own comment
(`cli/doctor.py`, `_run_report`), `Path.glob` swallows a `PermissionError`
inside its scandir walk and answers an empty list, so the rescue never fires
and a run directory this account cannot read reads as one with no run in it:
the gate says nothing of a sibling and the note says no run has sat at a gate.

**Measured cost.** Both silences were produced at the second review round of
U186, by replacing the run directory with a regular file and by forcing
`Path.glob` to raise: the gate answered no sibling and the note said no run
has sat at a gate for more than a day, over a directory never read. The
producer was not driven: the review container runs as root, where a chmod
changes nothing, and the tool makes the directory itself, so the
reachability on a person's machine is unmeasured. The status reader has
carried the same limit since before U186.

**Closes when:** the three readers of the run directory (`crate status`,
`run retire`'s `old_gates`, and these two) list it through one helper that
tells an unreadable directory from an empty one, for example by an
`os.scandir` that raises, and each says so. Ledger only: it closes on no
reachable producer yet, and it is maintainer facing until one is driven.
