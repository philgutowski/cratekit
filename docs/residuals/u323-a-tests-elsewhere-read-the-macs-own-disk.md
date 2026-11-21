---
title: Ten tests in eight files outside the backup's own read the machine's real disk identity and mount table, so on a Mac they run against a foreign identity
found: at the review of #914, U323, 2026-11-21.
issue: no
---

**The mechanism.** `tests/test_backup_unproven_root.py` now fails any test
that reaches `preflight.default_identity_provider` or
`preflight.local_mount_points`. No other file has that guard, and the
review, running the whole suite with the platform provider answering a real
looking foreign UUID as a Mac does, logged ten tests reaching the fallback
with no seam: four in `tests/test_backup_comparison.py` (doctor and age
reports), and one each in `tests/test_config.py`
(`test_doctor_reports_a_database_that_sits_outside_the_library_root`),
`tests/test_doctor.py`
(`test_the_wizard_does_not_call_an_intact_configuration_corrupt`),
`tests/test_intake_imported.py`
(`test_a_refused_close_is_reported_and_tried_again_next_time`),
`tests/test_provider_budget.py`
(`test_calls_past_the_budget_is_refused_before_a_verb_that_makes_no_call_runs`),
`tests/test_restore.py`
(`test_a_reconciliation_store_on_an_unmounted_volume_is_not_an_empty_one`)
and `tests/test_write_session.py`
(`test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`).

**Measured cost.** None red: all ten passed under the foreign answer, and
A183's macOS battery failed only the three U323 fixed. What they prove can
differ by platform, which the next finding shows for one of them.

**Closes when:** the suite answers the platform identity and the mount table
through a seam in `tests/conftest.py`, or each of the ten passes its own, so
no test reads the machine it runs on. Ledger only: nothing fails.
