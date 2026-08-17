---
title: The brief Files line is not the landing path
date: 2026-08-17
category: workflow-issues
module: src/cratekit/cli/registry.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - A unit is about to place files and the issue Files list names a path under src/cratekit/modules/
  - registry.Entry.module already names a dotted path that is not that Files tree
  - test_layering already ranks the first path word as a top-level module package
  - planned_in is still set on verbs whose countdown keys on that Entry.module string
  - The brief Files line and the registry module string disagree, the same hole U10, U11, and U34 already paid for
symptoms:
  - Code lands under src/cratekit/modules/labels/ while four verbs still name cratekit.label.cli
  - importlib.util.find_spec of Entry.module stays None or raises ModuleNotFoundError on the missing parent
  - test_a_planned_verb_whose_module_has_landed_must_lose_its_marker stays green
  - All four label verbs keep planned_in and never enter the conformance suite
  - The battery is green because the countdown only asks whether the registry string is importable
related_components:
  - testing_framework
  - documentation
tags:
  - planned-in
  - landing
  - brief
  - registry
  - layering
  - cli
  - verb-path
  - silent-failure
---

# The brief Files line is not the landing path

## Context

A Cratekit verb does not become real when a directory appears on disk. It
becomes real when the static registry can import the module string already
written on its `Entry`. That string is `Entry.module`
(`src/cratekit/cli/registry.py:126`). The unit that is supposed to create
that module is `Entry.planned_in` (`src/cratekit/cli/registry.py:163-164`).
`landed` is exactly `planned_in is None` (`src/cratekit/cli/registry.py:211-214`).
`landed_entries()` returns only those rows (`src/cratekit/cli/registry.py:1481-1483`).
The dispatcher walks that list and calls `import_module(entry.module)`
(`src/cratekit/cli/__init__.py:221-227`). A package that exists under a
different dotted path is invisible to every one of those steps.

The marker is supposed to expire on its own. The registry docstring says
so (`src/cratekit/cli/registry.py:23-28`): `tests/test_cli_contract.py`
asserts every planned module is genuinely still absent, so the marker
expires the moment its unit lands rather than surviving as a comment
nobody re-reads. The test that implements that promise is
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
(`tests/test_cli_contract.py:1171-1188`). It does not walk the issue
brief. It does not walk `src/`. It calls `importlib.util.find_spec(entry.module)`
and treats a missing parent as absent (`tests/test_cli_contract.py:1180-1183`).
If that spec is missing, the test stays green and `planned_in` stays.
If that spec appears, the test goes red and the marker must be cleared
so the conformance suite starts driving the verb.

U26 on 2026-08-17 is the unit that made this expensive to miss. The
issue brief's Files line named `src/cratekit/modules/labels/`. The
registry already named `cratekit.label.cli` on all four label verbs
(`src/cratekit/cli/registry.py:1141`, `1179`, `1191`, `1209`). Those
four rows have no `planned_in` in the current tree. They are landed.
The package that exists is `src/cratekit/label/`, with `cli.py` beside
the registry, sweep, import, and harvest engines. The brief named
`src/cratekit/modules/labels/` and that path was never created.
`src/cratekit/modules/` holds
the reports engines and the tools package, which is a different shape
and a different unit.

Layering had already ranked `label` as a top-level feature-module
package. `MODULE_PACKAGES` lists `"label"` next to `"acquire"`,
`"intake"`, `"favorites"`, and the rest (`tests/test_layering.py:123-134`).
The first-match layer rule `^cratekit\.[a-z_]+\.` ranks
`cratekit.label.cli` as `modules` (`tests/test_layering.py:109`). That
is a legal place for a feature CLI shell, and U26's shell stays legal
by not importing the registry: builders take an untyped `entry` so
`src/cratekit/label/cli.py` does not reach upward (KTD23)
(`src/cratekit/label/cli.py:3-4`). The brief Files path would have
created `cratekit.modules.labels`, which is a different import string
from `cratekit.label.cli`. `find_spec("cratekit.label.cli")` would
still have failed. The countdown would have stayed green. All four
verbs would have stayed planned forever.

This is the same hole U10, U11, and U34 paid for. A brief or planned
path that is not the registry module string will not land the verb.
U10 originally named `cratekit.core.jobs_cli`. A verb module imports
this registry, KTD23 ranks `core` below the CLI, and that path could
not have been written without an upward import. U10 landed at
`cratekit.cli.jobs` (`src/cratekit/cli/registry.py:684-689`). U11 made
the same correction from `cratekit.core.review_cli` to
`cratekit.cli.review` (`src/cratekit/cli/registry.py:736-743`). U34's
four report verbs named `cratekit.reports.cli`. Layering ranks
`cratekit.reports.*` as `modules` while the registry they must dispatch
through ranks `cli`, so the module could not have imported the table
without an upward import. The path moved to `cratekit.cli.reports`,
and the owner moved to U27, because U34's declared file list was the
reports engine package and it landed exactly that
(`src/cratekit/cli/registry.py:349-362`; `tests/_pending.py:191-197`).

U26 is the other face of the same class. The registry string was
already buildable. The brief Files line was not that string. Following
Files would have created a package the countdown cannot see.

The U26 merge on main is recorded in this checkout's `HEAD` log as the
ort merge of `unit/u26-label-registry-sweeps-import-harvest` on
2026-08-17.

## Guidance

Look up the registry `module=` field before creating a package.

Open `src/cratekit/cli/registry.py` and read `Entry.module` on every
verb the unit is supposed to land. That string is the landing path.
The issue brief's Files line is a hint about what the unit contains,
not a second source of truth for where the importable module lives.

If Files and `module` agree, land there.

If they disagree, do not follow Files. Land where the registry
already points, or change the registry in the same commit that lands,
after checking layering. Those are the only two legal moves. Landing
at Files and leaving `module=` alone is the silent miss: the package
exists, `find_spec(entry.module)` is still `None`, the countdown stays
green, and `planned_in` never expires.

Before you change `module=`, walk the layering rules in
`tests/test_layering.py`. Two questions, in order:

1. What layer does the current `module=` string rank as? First match
   in `_LAYER_RULES` wins (`tests/test_layering.py:69-112`).
   `cratekit.label.cli` matches `^cratekit\.[a-z_]+\.` and ranks
   `modules`. `cratekit.reports.cli` ranks the same way.
   `cratekit.cli.jobs` matches `^cratekit\.cli\.` and ranks `cli`.
2. Can a file at that path import what it has to import? A verb
   module that imports the registry must live in the CLI layer or
   above it. A feature CLI shell that takes an untyped `entry` and
   does not import the registry can live in the modules layer, which
   is what `src/cratekit/label/cli.py` does. U10, U11, and the U34
   reports rewrite each found a registry string that could not import
   the table, and they moved the string. U26 found a registry string
   that could, and they moved the files.

If you change `module=`, change every entry that shares it, in the
same commit that creates the file. The countdown keys on the module
string, not on the verb name. Four label verbs share
`cratekit.label.cli`. Four report verbs share `cratekit.cli.reports`.
One file appearing expires every marker that names that string. One
file appearing under a different string expires none of them.

Then clear `planned_in` on those entries. That is what
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
demands once `find_spec` succeeds. Clearing the marker without the
named module existing is the other miss: `landed` becomes true,
`build_parser` calls `import_module(entry.module)`, and a missing
module that is not a missing extra raises
(`src/cratekit/cli/__init__.py:227-230`). The product then fails at
parser construction, not on the new verb.

Do not copy `src/cratekit/modules/` from a unit that only owed
engines. U34 landed engines at `src/cratekit/modules/reports/` because
that unit never owed a CLI. Its four verb markers were re-pointed so
they would not name a closed unit (`tests/_pending.py:191-197`). A
later unit that does owe verbs does not inherit that directory.

## Why This Matters

`planned_in` is how Feature Inventory parity stays checkable before
the implementing unit exists (`src/cratekit/cli/registry.py:23-28`).
The alternative the docstring names is discovering at the last unit
that two Feature rows never acquired a verb. That only works if the
marker dies when the unit actually lands. The countdown that kills
it looks at one string. A Files tree that does not match that string
is not a landing. It is a second package the product cannot dispatch.

The failure is silent in the direction that costs the most. The
author creates `src/cratekit/modules/labels/`, the unit's own tests
pass against that tree, the battery is green, and
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
never sees `cratekit.label.cli`. The four verbs stay declared and
not landed. `landed_entries()` keeps omitting them.
`build_parser` never imports them. Conformance never drives them.
Feature rows 21 and 22 keep a verb on paper and no command a user
can type. `scripts/board.py` reads `tests/_pending.py` and never
reads `planned_in`, so the board will not save you either. That is
the same shape U34's comment calls R-13: the test only fires once
the named module appears, and an obligation that never becomes
importable under the string the registry holds is owned by nobody.

The other direction is loud and still wrong. Clear `planned_in`
because "the unit landed" while `entry.module` still does not
exist, and the next `drive()` cannot build the parser. That is a
red suite, which is better than a forever-planned verb, and it is
still a landing you have to undo.

U10, U11, and U34 already spent the afternoon this rule exists to
avoid. U26 is the reminder that the hole is not only "the registry
string is unbuildable." It is also "the brief named a different
tree." Both are a brief or planned path that is not the registry
module string.

## When to Apply

Every time a unit is about to create a package that a `planned_in`
verb names, before the first file is written.

Concretely:

- A unit issue Files line names `src/cratekit/modules/<name>/` and
  the registry already says `cratekit.<other>.cli`.
- A unit is about to "put the CLI next to the engines" by copying
  the U34 reports directory shape onto a unit that already has
  verb rows.
- `module=` on the verbs you are landing does not match the
  directory you were about to mkdir.
- Layering ranks the current `module=` string as `modules` while
  the file you are about to write must import
  `cratekit.cli.registry`, or ranks it as `cli` while the brief
  put it under a feature package.
- Several verbs share one `module=` string. Creating one file
  expires all of them, or none of them, together.
- `test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  is still green after you believe you landed. That is the signal
  that `entry.module` is still absent. Do not treat a green
  countdown as proof of landing.

Apply it at the start of the unit, not at discharge. Discharge is
too late: the files are already in the wrong tree, the suite
against that tree is green, and the countdown cannot see them.

## Examples

U26, favourite-label registry, sweeps, import, and harvest, merged
to main on 2026-08-17.

The brief Files line was `src/cratekit/modules/labels/`. The
registry already pointed all four verbs at `cratekit.label.cli`
(`src/cratekit/cli/registry.py:1141`, `1179`, `1191`, `1209`).
`MODULE_PACKAGES` already listed `"label"` as a top-level feature
package (`tests/test_layering.py:125`). The landing that matches
those facts is `src/cratekit/label/cli.py`, with the engines in the
same package so the shell can import them downward. That is what
merged. `planned_in` is gone on all four rows. `find_spec` can
resolve `cratekit.label.cli`. Conformance can drive the verbs.

The landing that would have matched the brief is
`src/cratekit/modules/labels/`. That package would have been
`cratekit.modules.labels`. `find_spec("cratekit.label.cli")` would
still have returned `None`. The countdown at
`tests/test_cli_contract.py:1171` would have stayed green. The four
markers would have stayed. `landed_entries()` would have kept
omitting `sync.labels`, `label.registry`, `label.import`, and
`label.harvest`. The product would have shipped the engines and no
commands.

U10 and U11 are the same class with the other legal move. The
registry originally named `cratekit.core.jobs_cli` and
`cratekit.core.review_cli`. Those strings ranked below the CLI
layer, and a verb module has to import the registry, so the path
could not be built. They did not create the historical path
`src/cratekit/core/jobs_cli.py` and leave the countdown staring at a
string that could never appear.
They changed `module=` to `cratekit.cli.jobs` and
`cratekit.cli.review` in the landing itself
(`src/cratekit/cli/registry.py:684-743`). The plan file lists for
those units already named `src/cratekit/cli/jobs.py` and
`src/cratekit/cli/review.py`. Files and `module=` were brought into
agreement, then the files were written at the agreed string.

U34 is the neighbour that records the reports half of the same
rewrite. The four report verbs named `cratekit.reports.cli`.
Layering ranks that path `modules`. The registry they must dispatch
through ranks `cli`. The module could not have been built as
spelled (`src/cratekit/cli/registry.py:355-362`).
`tests/_pending.py` records the correction: the module path moved
from `cratekit.reports.cli` to `cratekit.cli.reports`, "which
test_layering ranks modules while the registry it must dispatch
through ranks cli, so it could not have been built as spelled;
that is the same correction U10 and U11 each made on landing"
(`tests/_pending.py:194-197`). U34's own Files line was
`src/cratekit/modules/reports/` and it landed the engines there.
That was correct for a unit that did not owe a CLI. It is not a
template for a unit whose verbs already name a different module
string.

The mechanism in every case is the same. Look up `module=`. If
Files disagrees, land at `module=`, or change `module=` after
checking layering, in the same commit that lands. Never create the
Files tree and hope the countdown will notice.

## Related

- [A planned verb cannot share a landed leaf's first path word](a-planned-verb-cannot-share-a-leafs-first-path-word.md):
  same `planned_in` expiry, same
  `test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`,
  same `find_spec(entry.module)`. That learning is argparse
  refusing a group under a word that is already a landed leaf.
  This one is landing at the brief Files path so the named module
  never becomes importable. U23 in that document is closer still:
  expiry keys on the module string, so a shared or wrong `module=`
  holds the ready half or never fires.
- [Discharging a countdown entry by half takes a whole test file out of collection](countdown-entry-discharge-drops-a-whole-test-file.md):
  same landing moment, a module appears and a marker must expire.
  Different register. `PENDING` plus `@requires` is collection.
  `planned_in` plus `Entry.module` is verb landing. Do not treat
  them as one lesson.
- `tests/_pending.py` on `cratekit.cli.reports` (`tests/_pending.py:181-208`):
  the prior instance of this class, not itself a solutions
  document. U34's verbs could not be built as `cratekit.reports.cli`.
  The path moved. The owner moved so four markers would not name a
  closed unit. Same correction U10 and U11 made on landing.
