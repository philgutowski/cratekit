---
title: "A disposable database copy does not make library state disposable, so a copy run that approves a write can mark the live library done"
date: 2026-09-25
category: workflow-issues
module: "cratekit.adopt.apply, cratekit.core.config state inventory"
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - "A verb is being driven against a disposable copy of master.db to preview what it would do live"
  - "The run on the copy is about to go past a gate, rather than stopping at it"
  - "The temporary setup redirects CRATEKIT_CONFIG_DIR and CRATEKIT_STATE_DIR and nothing else"
symptoms:
  - "A copy run's config points db_path at the copy, yet state files appear under .cratekit on the volume"
  - "A later live run reports entries already applied that were never written to the live database"
related_components:
  - "database"
  - "tooling"
tags:
  - "disposable-copy"
  - "library-state"
  - "adoption-ledger"
  - "cutover"
---

## The trap

The attended sittings preview a live write by copying `master.db` into a
temporary directory and pointing a temporary config at it, with
`CRATEKIT_CONFIG_DIR` and `CRATEKIT_STATE_DIR` redirected. That isolates the
database and the installation state, all but the provider gate, which is
never redirected: every provider call the copy makes is spent from the live
hour's budget, and a sweep on the copy can stop a live go (U278). It does not isolate LIBRARY state, which
`config.library_state_dir` puts at `<library.root>/.cratekit` on the volume,
and the copy's config still names the real root.

`adoption_ledger.json` is one of those files (`StateRoot.LIBRARY`, snapshot role
`COUPLED`). Approving `adopt apply` on the copy would write memberships into the
copy and then mark every entry applied in the volume's ledger. The live run
reads that ledger through `outstanding()` and skips every entry it finds, so it
would write nothing live and report the adoption done. Found at sitting 13
before it was driven, by reading where the ledger lives.

## The rule

Stopping at the gate is safe on a copy: the plan and the census write nothing a
live run reads as done. Going PAST a gate on a copy needs the library root
redirected as well (`CRATEKIT_LIBRARY_ROOT`, or `library.root` in the temporary
config) to a scratch directory, and the state inventory checked for every
`StateRoot.LIBRARY` entry the verb touches. Grep the inventory in
`src/cratekit/core/config.py` for `root=StateRoot.LIBRARY` before trusting any
copy run that approves.

## How it was done, sittings 14 and 15

Redirecting the library ROOT does not work on a real library: every file the
census reads sits under the real root, so a moved root puts all of them
outside it. What the rule protects is the state directory, and that has its
own setting. The copy's temporary config keeps `library.root` on the volume
and sets `library.state_dirname` to a scratch name, after the volume's state
directory is copied to that name with `cp -Rp`. `db_path` names the database
copy and `db_outside_root_acknowledged_on` carries the day.

Three checks before any gate is answered on the copy. `crate doctor` in that
environment prints the `tree.registry` path, which must carry the scratch
name. Each gate prints what it reads and what it writes, and both must be
scratch paths. The live database's sha256 is taken before and compared after.

The backup acknowledgment is library state too, so the copy has none until
the author's live one is copied into the scratch `local` directory. Remove
the scratch directory from the volume when the run ends, or the next backup
mirrors it.

Both sittings' rehearsals matched their live runs to the digit, plan digest
and every membership, which is what the copy is for.

## Related

`docs/cutover.md` sitting 13, which also leaves open whether an approved
adoption lands memberships at all on a tree no verb has cut over.
