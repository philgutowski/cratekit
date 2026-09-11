---
title: "U27's backup.remote trash-policy table was tested against hand-written rclone config stubs, so a Dropbox option rclone does not have and a OneDrive option rclone ignores both read green"
date: 2026-09-11
category: workflow-issues
module: "src/cratekit/cli/doctor.py, tests/test_doctor.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A doctor or config check validates a per-remote or per-provider option name against a real external tool's own option table (rclone, an API client, a CLI's own flag set)"
  - "The check's tests build the provider's config as a hand-written dict rather than reading it from the real tool"
  - "A new row is about to be added to a table like _REMOTE_TRASH_POLICY by inference from documentation rather than by reading the tool's own backend help"
symptoms:
  - "A Dropbox remote failed doctor's backup.remote check on every run, with a fix (set permanent_delete) that rclone's Dropbox backend has no such option to apply"
  - "A Dropbox remote with permanent_delete written into its config by hand passed the check clean while its prune behavior was unchanged, because the check only reads the key, not whether rclone's backend honors it"
  - "A OneDrive remote with hard_delete correctly set to true still read green on a personal drive, where rclone's OneDrive backend ignores that option entirely"
tags:
  - "rclone"
  - "doctor"
  - "fixture-fidelity"
  - "test-stubs"
  - "provider-table"
---

# U27's backup.remote trash-policy table was tested against hand-written rclone config stubs, so a Dropbox option rclone does not have and a OneDrive option rclone ignores both read green

## What happened

U27 shipped `_REMOTE_TRASH_POLICY` in `src/cratekit/cli/doctor.py`, a table
mapping each rclone remote type to the per-remote option that stops a prune
from going to that provider's recycle bin. Its tests in `tests/test_doctor.py`
drove the check through `probes(rclone_remotes=lambda _r: {...})`, a plain
Python dict built by hand to stand in for what `rclone config dump` returns
for a real remote. Nothing in that fixture, or in the check itself, ever
called rclone.

Two of the table's rows were wrong from the start, and the hand-written
stubs could not catch either, because a stub is only as correct as the
person who typed it and the check has no way to disagree with its own
fixture:

- Dropbox's row named `permanent_delete`. Read against rclone 1.74.3's own
  `rclone help backend dropbox`, the Dropbox backend has no such option. Every
  real Dropbox remote failed the check with a fix nothing could apply, and a
  test fixture with `permanent_delete: "true"` written into it by hand passed
  clean, because the check only asked whether the key was present and set,
  never whether rclone's Dropbox backend does anything with it.
- OneDrive's row named `hard_delete` with no qualification. rclone honors
  `hard_delete` on business drives and document libraries only; on a personal
  drive it is silently ignored. A fixture setting `hard_delete: "true"` with
  no `drive_type` read green regardless, because nothing in the check or its
  fixtures modeled that the option's effect depends on a second field.

Fixed in `837daa4`: Dropbox's row became option-less (`TrashPolicy(option=None)`,
same shape as Box and pCloud), and `TrashPolicy` gained `applies_when`, a
`(setting, allowed-values)` pair that turns an out-of-scope OneDrive remote
into an informational note instead of a false green or a false red.

## Why this passed a green suite

The check and its tests share one author's model of what rclone's config
looks like. `_REMOTE_TRASH_POLICY`'s rows describe what the author believed
each backend's option to be, and the test fixtures describe the same belief
in dict form. Comparing the check against its own fixtures only asks whether
the check does what the author intended; it cannot ask whether the author's
intent matched rclone, because rclone was never in the loop. This is the same
mechanism as
[a checker that reimplements what it checks drifts and stays green](a-checker-that-reimplements-what-it-checks-drifts-and-stays-green.md),
one layer down: there the checker reimplemented argparse's grammar, here the
fixtures reimplement rclone's option table, and in both cases the fixture and
the code under test are two expressions of the same private model rather than
independent evidence.

## The rule

**Before adding or trusting a row in a table that names an external tool's
option, read that tool's own help for the option's name, its default, and any
account-kind or plan-kind caveat.** `rclone help backend <type>` for every row
in `_REMOTE_TRASH_POLICY`, not just the ones being changed. A stub built from
memory or from documentation skimmed once cannot be told apart, by the suite,
from a stub built from the tool's own answer, and only one of them is still
correct a version later.

**Hand-written config stubs test the check's logic, not the check's content.**
They are fine for proving that a given key and value combination produces the
right `Status`, the same way `_FIXTURE_VERBS` was fine for proving the old
skills-lint walker resolved verb paths correctly. They cannot prove the key
name or the value's meaning is real, because nothing compares the stub to the
provider. Where a table like this exists, the fact that needs periodic
re-verification against the real backend is the row itself, not just the
check that reads it.

## Related

- [A checker that reimplements what it checks drifts and stays green](a-checker-that-reimplements-what-it-checks-drifts-and-stays-green.md),
  the general form: a fixture shaped like the checker's own model cannot
  disagree with that model.
- `docs/residual-findings.md`, R-7 (closed in place by this branch), R-336
  (the quota sentence the option-less rows share, unmeasured against any
  provider), and R-337 (mega, b2, jottacloud, yandex, pikpak: rclone gives
  each a delete option and the table has no row for any of them).
- Issue [#44](https://github.com/philgutowski/cratekit/issues/44), R-7,
  closed by merge `140a8de`.
