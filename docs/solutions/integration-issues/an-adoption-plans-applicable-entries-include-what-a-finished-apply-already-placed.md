---
title: "An adoption plan's applicable entries include what a finished apply already placed"
date: 2026-10-03
category: integration-issues
module: src/cratekit/adopt/apply.py
problem_type: integration_issue
component: adoption
severity: medium
resolution_type: code_fix
applies_when:
  - "A caller other than the adopt apply worker asks whether an adoption has anything left to do"
  - "A composer reads adopt apply's current_plan to decide planned or nothing"
  - "A second run after a full apply still plans the adoption"
tags: [adoption, applied-ledger, outstanding, composer, organize, u112]
---

# An adoption plan's applicable entries include what a finished apply already placed

## The contract

`apply_cli.current_plan(cfg, declared).applicable()` answers every entry the
plan COULD place, and it stays the same after an apply has placed them. The
plan is rebuilt from the census on every run (R26), and filing a track into
its sub does not change its disposition, so a fully adopted library still
plans every one of its tracks as applicable.

What is left to do is a second record: the applied ledger. The engine's own
rule is `adopt.apply.outstanding(plan, adopt.apply.read(cfg))`, the applicable
entries the ledger does not hold. `apply_plan` uses it to skip, and reports the
rest as `already_applied`.

## Why it was not visible

`adopt apply` asks its gate over the applicable entries and queues a pass
whenever there are any, so on a fully adopted library it queues a pass that
applies nothing and reports `already_applied` for every entry. Nothing fails,
so nothing showed it. U112's `crate organize` read `applicable()` to decide
whether its adoption step had work, and its test that a second run after a
full apply plans nothing failed with both tracks planned again, measured on
2026-10-03.

## What to do

Decide "anything to do" with `outstanding`, never with `applicable()` alone.
Keep the gate's screen and digest on the applicable entries if the caller
hands the job to `adopt apply`'s worker, since the worker rebuilds that same
plan and compares that digest. A ledger that cannot be read raises
`AppliedLedgerUnreadable`, and that is the step's refusal, not "nothing to do".
