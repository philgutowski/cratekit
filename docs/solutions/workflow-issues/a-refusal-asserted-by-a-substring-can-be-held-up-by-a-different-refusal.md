---
title: "A refusal asserted by a substring can be held up by a different refusal, and only a mutation row shows it"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/core/restore.py, src/cratekit/session/restore_cli.py, tests/test_restore.py, tests/test_restore_cli.py"
problem_type: workflow_issue
component: restore
root_cause: unverified_assumption
resolution_type: test_fix
applies_when:
  - "A function runs several refusals in order and they share one reason slug"
  - "A test asserts a refusal with `in cause.message` on an ordinary word"
  - "A fixture puts its scratch directories side by side under one temporary directory"
  - "A unit is the first caller of an engine whose guards were tested only at the seam"
  - "An engine runs a list of commands and reads their return codes afterwards"
symptoms:
  - "A mutation row that deletes a guard kills zero tests while three tests are named after that guard"
  - "A refusal test passes for a reason other than the one in its name"
  - "A failed first transfer still lands the second one, and the rerun is refused"
related_components:
  - restore
  - backup
  - mutation-table
tags:
  - bare-metal-recovery
  - refusal-tests
  - substring-assertion
  - guard-covered-by-guard
  - first-caller
  - mutation-table
  - u96
  - r-412
  - r-592
---

# A refusal asserted by a substring can be held up by a different refusal, and only a mutation row shows it

## What happened

`restore.bare_metal_session` runs four refusals in order, all under one reason,
`recovery-target-refused`. The first, that the recorded library must be
genuinely gone, is the one that keeps a bare metal recovery apart from a live
restore. Three tests asserted it, one in the engine's suite since the engine
landed. U96's mutation table deleted it and killed nothing, on the subset and
then on the full suite.

The tests built the replacement directory beside the configured library, both
under `tmp_path`. The second refusal, the stub check, refuses a target that sits
in the directory the library mounts into and is not a mount point, and a
temporary directory never is one. Its sentence says the target is "the empty
folder an unmounted volume leaves behind". The tests asserted
`"mounted" in cause.message`. So with the first guard deleted, the second one
refused, under the same reason, with a message containing the asserted word.

## The rule

When several refusals share a reason, a test for one of them has to make every
OTHER one pass, and assert a phrase only its own sentence holds. Here that meant
passing `mount_probe=lambda _path: True` so the stub check could not fire, and
asserting "nothing to recover from bare metal". After that the same mutation
kills three.

A fixture that lays scratch directories side by side is what made this
reachable. "Beside the configured root" is a real hazard the engine checks for,
and `tmp_path / "library"` next to `tmp_path / "replacement"` reproduces it in
every test whether the test is about it or not.

## Two more things the first caller found

`backup.run_restore` runs EVERY command and reads the return codes afterwards.
For a live restore that is harmless. For a recovery onto an empty drive it means
a failed mirror still lands the database, and the engine then refuses the rerun,
because a target holding a database is refused. The verb splits the one plan by
label and spends it a half at a time with `dataclasses.replace`, rather than
changing the engine under its other caller.

The mirror carries the state directory beside the library, so it carries
database files of this product's own, the review queue and every capture. "The
target must hold no database" therefore stops being true the moment the mirror
half starts, on any library and not only one prepared for a player. The brief
had fixed `replacing_existing` at False, so the unit kept the rule, gave every
failure one true step for the rerun, tested that step by following it, and
filed the redesign as R-592.
