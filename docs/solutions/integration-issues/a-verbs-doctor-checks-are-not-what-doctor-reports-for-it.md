---
title: "A verb's doctor checks are not what doctor reports for it, and a read still needs the pins"
date: 2026-09-19
category: integration-issues
module: src/cratekit/cli/doctor.py
problem_type: integration_issue
component: development_workflow
severity: medium
root_cause: unverified_assumption
resolution_type: code_fix
applies_when:
  - "A brief drops or adds a key in a registry entry's doctor_checks and expects doctor to say something different"
  - "A verb opens the rekordbox database without write intent and a brief says it needs no rekordbox precondition"
tags: [doctor, registry, doctor-checks, pins, rekordbox, read-only, r-313, r-444]
---

# A verb's doctor checks are not what doctor reports for it, and a read still needs the pins

## What looked true

The R-313 brief said: drop `rekordbox.closed` and `rekordbox.pins` from
`route.unplaced`, and "doctor no longer requires rekordbox closed for this
verb". Both halves read as if a verb's `doctor_checks` set what `crate doctor`
tells a person before running that verb, and as if a read-only verb needs
nothing from rekordbox.

## What is true

Doctor has no per verb report. `doctor.requires_check(key, membership)` is an
`any()` over every entry the profile switches on. While a core write verb
(`route.inbox`, `route.resort`, `route.pending`) declares `rekordbox.closed`,
it is required in `slim`, `full` and `custom`, whatever one report declares.
Changing one entry changes the declaration, conformance 3, 6 and 8, and the
cloud-sync pairing test. It does not change a line of doctor's output. To test
the per verb claim at all, narrow `registry.entries` to the one entry and call
`requires_check`, as
`test_doctor_does_not_ask_for_rekordbox_closed_for_the_unplaced_report` does.

A read still needs the pins. `rb_writer.open_db` checks the binding pin
(`assert_binding_version`) on EVERY open and the schema pin after it. Only the
two-process refusal, the application pin and the unreadable cloud-sync refusal
wait for `require_closed`. So a read-only report refuses `pyrekordbox-pin-drift`,
exit 23, on a drifted binding, and declaring no `rekordbox.pins` would have
doctor call it ready first. The cloud-sync decision really is unreachable for a
read and can go.

## What to do

Before removing a doctor check from a read, sort each check by what the open
actually enforces with no write intent: the binding and schema pins, yes;
rekordbox closed and the application pin, no. `rekordbox.pins` covers two pins
in one check, which is why no declaration is exactly right for a read, and
R-444 records that along with `converge`, which reads and declares no pins.
Do not write a test scenario that expects doctor's output to change unless the
same key leaves every entry in the profile.
