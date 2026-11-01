---
title: crate status and crate run retire stop with an internal error on a run record the gate warning and doctor's note name as unreadable
found: at the second review round of #394, U186, 2026-11-01.
issue: no
---

**The mechanism.** U186's two readers of the run directory, `gates.siblings`
and doctor's `_check_open_gates`, count a record whose load raises anything
as unreadable and go on. The two readers before them, `crate status`
(`_run_report` in `cli/doctor.py`) and `crate run retire` (`old_gates` in
`cli/verbs/runs.py`), catch only the structured refusal, so a record that
parses as schema 1 and lacks a field raises `KeyError` through them.

**Measured cost.** Driven at the review with a hand written
`{"version": 1, "run_id": "half"}` in the run directory: both verbs exit 1
with `internal-error` naming `KeyError: 'verb'`, while the gate and doctor
name the record and carry on. The producer was not driven: `gates.save`
writes every key atomically, and no writer of such a record was found in
the tree (zero candidates), so a hand edit is the only input measured.

**Closes when:** the four readers share one listing helper that names an
unreadable record the same way, so they cannot disagree about one file.
Ledger only, since it is reached only by a hand edited record so far; it
was left out of U186 because both verbs belong to U170 and the brief names
neither.
