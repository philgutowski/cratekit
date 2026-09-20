---
title: A refusal that hands over a value to record must read it through the guard that will judge it
date: 2026-09-19
category: integration-issues
module: "src/cratekit/core/session.py"
problem_type: integration_issue
component: volume_identity_gate
root_cause: missing_validation
resolution_type: code_fix
severity: high
symptoms:
  - "A volume identity gate refuses because nothing is recorded, and its remedy step says: the volume there identifies as X, record it"
  - "With the drive ejected, X is the identity of the disk holding the mount directory, usually the boot disk"
  - "Once X is recorded the gate passes for good against the ejected drive's leftover mount point, which is the hole the gate was built to close"
  - "A second look placed immediately before a destructive write never runs for a missing disk, because a missing disk takes the branch that records a deletion instead of the branch that moves a file"
applies_when:
  - "A gate compares an observed value against a recorded one and, on nothing recorded, offers the observed value for recording"
  - "A path is identified by walking up to its containing mount, and the path may cross a mount point with nothing mounted in it"
  - "A loop re-asserts a precondition before its write and also has a branch that records a permanent fact when the thing to write is absent"
tags:
  - "volume-identity"
  - "prefix-rule"
  - "deletion"
  - "trust-on-first-use"
  - "absence-as-evidence"
  - "r44"
  - "r51"
---

# A refusal that hands over a value to record must read it through the guard that will judge it

## Context

The deletion pass asserted the volume identity of the library root only, and a
prefix rule could send it onto any other disk. The fix gave each rule an
optional `volume_id` and asserted every rule target with
`preflight.assert_library_volume`. A rule outside the library root with nothing
recorded refuses, and to make that refusal one edit from a working run it named
the identity the disk shows now.

The built in review found that this helpful sentence reopened the defect the
change existed to close, and that the second look before the write guarded the
wrong branch. Both passed a green suite written by the author of both.

## What went wrong, twice

**The advice was read by a weaker reader than the gate.** The refusal read the
identity with `containing_mount`, which walks up to the deepest existing
ancestor and then to a mount. For an ejected drive whose mount point was left
behind, that walk ends at the disk holding the mount directory. So the step said
"it identifies as the boot disk's identity, record it". A person who did exactly
what the product told them then had a rule whose recorded identity matches an
EMPTY directory, permanently. `preflight.identity_source` already existed to
refuse reading an identity through an empty mount slot, and setup already used
it for the library's identity for this exact reason. The new gate did not.

The fix is two things, not one. The handed over identity is read from the mount
`identity_source` accepted. And the gate itself asks `identity_source` first and
refuses an empty slot whatever is recorded, because a configuration that already
carries the wrong identity, by that advice or because the library shares the
boot disk, must not pass either. Fixing only the sentence would have been a fix
on the performing path with the checking path still open.

**The second look sat in front of the branch a missing disk never takes.** The
re-assertion was placed immediately before `trash.move_to_trash`. With the drive
gone, the re-check cannot stat the file, the anchor directory still exists, the
answer is `GONE`, and `GONE` is SETTLED: a tombstone, handled, the watermark
past it. The move is never reached, so neither was the assertion. The
destructive act for a missing disk is the RECORD, not the move. The look now
runs at the top of the loop, which covers a retirement and a settlement of the
plan's answer, and again after the re-check and before both of its branches.

## How to apply it

- When a refusal offers a value to record, read it through the strictest reader
  the gate has, and ask what the person's configuration looks like after they
  follow the step. If following it disarms the gate, the step is the defect.
- When you add a "check again before the write", list every permanent act in
  the loop first. A tombstone, a watermark advance and a suppression are writes.
  Then ask which branch the failure you are guarding against actually takes.
- Assert after the evidence was gathered and before it is acted on. A check in
  front of the stat validates a disk the stat may no longer be talking to.
- Probe the thing that will be written, here the file's own directory, not the
  configured thing that led to it. A volume mounted inside a rule's target is a
  third disk the target's identity says nothing about.

## Where it lives

`session._assert_rule_volume`, `session.assert_mapped_volume_identities`,
`session.assert_mapped_file_volume`, and
`deletion/run.py::_assert_the_volume_this_file_is_on`. Tests:
`test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record`,
`test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it`
and `test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`.
`tests/_mounts.py` stands directories in as mount points and as mount slots,
since a suite cannot mount a real volume.
