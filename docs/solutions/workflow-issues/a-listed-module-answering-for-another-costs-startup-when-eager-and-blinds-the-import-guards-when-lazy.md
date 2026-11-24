---
title: A listed module answering for another costs startup when eager and blinds the import guards when lazy
date: 2026-11-23
category: workflow-issues
module: tests/test_import_rules.py, cratekit.core.jobs, cratekit.core.session, cratekit.core.pool
problem_type: workflow_issue
component: import_rules
severity: medium
root_cause: hidden_cost_of_a_re_export
resolution_type: design_rule
applies_when:
  - A core module off CORE_INTERFACE is reached by a feature package and the
    plan is to re-export its names from a listed module.
  - A listed module is about to import another module only to hand its names on.
  - A module level __getattr__ or importlib.import_module is proposed to keep an
    import off the startup path.
  - A source guard resolves uses of a module by its dotted name.
symptoms:
  - tests/test_cli_lazy.py fails at its ceiling on the doctor's closure after a
    change that touched no verb.
  - tests/modules/test_reports.py says the audit could not follow a computed
    import out of the allowlist.
  - tests/test_pool_sizing.py says no module in the analysis package calls the
    planner, while the package still plans every pool through it.
tags:
  - import-rules
  - named-interface
  - re-export
  - lazy-import
  - startup-cost
  - reports-audit
  - u331
---

# A listed module answering for another costs startup when eager and blinds the import guards when lazy

## The trap

`tests/test_import_rules.py` lets a feature package import 25 core modules and
no other. The obvious way to reach a twenty sixth is to re-export its names
from one of the 25. U331 tried that twice and each way failed a guard it had
not been thinking about.

**Eager, the plain `from part import name as name`.** `core.jobs` re-exported
the pool's names and `core.active_taxonomy` the word edits. Every command that
imports the job queue then imported `concurrent.futures` and
`multiprocessing` with it, and every one that loads the taxonomy imported the
routing and the upgrade. Measured over 15 fresh interpreters importing
`jobs`, `session`, `active_taxonomy` and `tags`: 207.4 ms at best with the
re-exports against 193.0 ms on the base. `tests/test_cli_lazy.py` caught it as
the doctor's help reaching its ceiling of 90 of Cratekit's modules, from 88.

**Lazy, a module `__getattr__` that imports the part when a name is first
read.** No startup cost, one binding, no import cycle. But the reports audit
(`tests/modules/test_reports.py`) follows every import out of its allowlist to
name the writers a report can reach, and refuses a module whose import it
cannot read: `core.session`, which a report reaches, had a computed import
behind it. A guard that walks imports cannot see through `__getattr__`, and
the ones that fail loudly are the lucky ones.

**Either way, a guard keyed on the module's name stops seeing its callers.**
`tests/test_pool_sizing.py` resolves every use of the planner through
`ImportsOf(tree, "cratekit.core.pool")`. Once the analysis package reached it
as `jobs.plan_pool` the countdown reported that nothing sized a pool, and
would have been silent on a plan built by hand through the same door.

## The rule U331 settled on

A feature package reaches a core module in one of three ways, and the choice
is made by what the module costs, not by what is least typing:

1. **The module is on the list and is imported itself.** For a module that is
   heavy to import (`pool`), that a guard is keyed on (`pool`), or that imports
   the module that would have to answer for it (`art` imports `tags`,
   `restore` imports `session`), or whose own imports would load with every
   importer of the module answering for it (`taxonomy_word` imports the
   upgrade and `routing`; before the upgrade read `active_taxonomy` where it
   calls it, answering for it there was also a cycle). A module joins only as another leaves.
2. **A listed module re-exports the names, eagerly.** Only where the listed
   module imported the other already, or the reports audit already admits it
   beside it and the cost was measured: `session` for `preflight`, `processes`
   and `snapshot`, `config` for `profiles`, `active_taxonomy` for
   `foreign_tree`, `jobs` for `discovery`, `pool` for the cores' ceiling.
3. **The module is no part of core and lives in the feature package that owns
   it**, when nothing in core or write imports it: `sync/held_plan.py`,
   `intake/rehearsal.py`, `intake/drift.py` (which analysis and the shell's
   tail import from intake).

Never the lazy `__getattr__`.

**Measured does not mean measured at the listed module.** The first review
found two re-exports that passed every check above and still cost something.
`core.jobs` answered for the cores' ceiling, so `analysis/light.py`, which a
spawned worker unpickles, imported the queue and the shell with it: 52.8 ms
to import on the base, 110.6 ms on the branch, and 5 MB a worker. And
`core.tree_registry` answered for `foreign_tree`, which loads the taxonomy
that module had kept under `TYPE_CHECKING`. Ask who imports the listed module
for the new name alone, and what else that module loads: the ceiling went to
`pool`, which the worker imports already, and the foreign tree's names to
`active_taxonomy`, which loads the taxonomy anyway. That home has a price of
its own: every module importing `active_taxonomy` at its top now loads
`foreign_tree` too, and once U343 merged, `crate doctor --help` reached its
module ceiling for it, so the doctor's two readers (`cli/doctor_state.py` and
`core/taxonomy_upgrade.py`) import the loader in the function that calls it.

## What to check before re-exporting

- `python -X importtime -c "import cratekit.core.<listed>"` before and after,
  and the doctor's closure (`tests/test_cli_lazy.py`).
- `_admitted_closure()` in `tests/modules/test_reports.py`: is the listed
  module in it, and is the other module in it already?
- `grep -rn '"cratekit.core.<part>"' tests`: a guard that names the module
  resolves its callers by that name.
- Every importer of the caller, a spawned worker's module above all: `python
  -X importtime -c "import cratekit.<package>.<caller>"` before and after.
- The tests that patch the name: with an eager re-export there are two
  bindings, and a patch on one is not seen through the other. Assert the two
  are one object (`tests/test_import_rules.py` does, for every name a listed
  module takes from another core module) and patch below both where a test
  must reach both (`tests/test_intake_land_rehearse.py` takes the room away
  in `snapshot._free_bytes`).
