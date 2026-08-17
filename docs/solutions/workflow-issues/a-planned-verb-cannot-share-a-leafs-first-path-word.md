---
title: A planned verb cannot share a landed leaf's first path word
date: 2026-08-17
category: workflow-issues
module: src/cratekit/cli/registry.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - A planned verb is about to land with a dotted name whose first path word is already a one-word landed Entry
  - A new CLI name is being chosen next to an existing leaf such as doctor, status, or adopt
  - The registry is about to add a grouped verb under a word that already called add_parser as a leaf
  - planned_in is being discharged by landing a verb whose path prefix collides with a landed leaf
symptoms:
  - argparse raises ArgumentError conflicting subparser when the whole CLI parser is built
  - crate refuses to start at all, not just the new verb
  - doctor.repair-paths cannot be registered beside the landed doctor leaf
  - The suite that builds the parser goes red on construction, before any handler runs
related_components:
  - testing_framework
  - documentation
tags:
  - cli
  - argparse
  - registry
  - verb-path
  - name-collision
  - planned-in
  - landing
  - silent-failure
---

# A planned verb cannot share a landed leaf's first path word

## Context

Cratekit's CLI verb tree is not hand-written. It is assembled from
`registry.Entry` rows. Each entry's `name` is a dotted string, and `path` is
that string split on the dots:

```217:219:src/cratekit/cli/registry.py
    @property
    def path(self) -> tuple[str, ...]:
        """The subcommand path a user types, as words."""
        return tuple(self.name.split("."))
```

`build_parser` walks `landed_entries()` and hangs each path off the root
(`src/cratekit/cli/__init__.py:221-239`). A one-word path calls
`root.add_parser(path[-1])` and becomes a leaf. A multi-word path calls
`_group_parser` with every word except the last. `_group_parser` does
`parent.add_parser(path[-1])`, then `add_subparsers`, and caches the group
(`src/cratekit/cli/__init__.py:168-177`). The last word is then added as a
leaf under that group. Two groups that share a prefix are fine: the cache
returns the same subparsers object. A group and a leaf that share a word on
the same parent are not fine. argparse will not register the same subparser
name twice.

`doctor` is a landed one-word leaf. Its module is `cratekit.cli.doctor`
(`src/cratekit/cli/registry.py:523-531`). Issue #37 needed a path-repair
verb. The planned name was `doctor.repair-paths`. That name's first path
word is `doctor`. `_group_parser` therefore tries `root.add_parser("doctor")`
a second time. argparse raises:

    argparse.ArgumentError: argument <command>: conflicting subparser: doctor

The metavar is `<command>` because that is what `build_parser` sets on the
root subparsers (`src/cratekit/cli/__init__.py:216`). The error is not a
handler failure and not a usage failure on the new verb. Construction of
the whole parser refuses. `crate` cannot start.

`planned_in` is what kept the collision invisible. An entry whose
`planned_in` names a unit is declared but not landed
(`src/cratekit/cli/registry.py:23-28`, `src/cratekit/cli/registry.py:163-164`).
`landed` is exactly `planned_in is None` (`src/cratekit/cli/registry.py:211-214`).
`landed_entries()` returns only those (`src/cratekit/cli/registry.py:1511-1513`).
`build_parser` walks that list, so a planned verb with a colliding first
word can sit in the registry for months and never touch argparse.

The marker expires when the module exists.
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
(`tests/test_cli_contract.py:1138-1155`) probes with
`importlib.util.find_spec(entry.module)` and fails the moment the module is
importable. Creating `cratekit.intake.repair_cli` forced the then-named
`doctor.repair-paths` entry to land. Clearing `planned_in` put the verb in
`landed_entries()`. The next `build_parser` call refused the tree.

The first red test was
`test_status_two_belongs_to_the_argument_parser_and_to_nothing_else`
(`tests/test_cli_contract.py:190`). That test calls `drive` with an unknown
flag (`tests/test_cli_contract.py:204`). `drive` is `cli.run`
(`tests/test_cli_contract.py:134-137`). `run` builds the parser before it
parses anything (`src/cratekit/cli/__init__.py:338-342`). The unknown flag
is not what failed. Construction is. The new verb never ran.

The verb that shipped is `repair.paths` (`src/cratekit/cli/registry.py:533-548`),
module `cratekit.intake.repair_cli`, builder `build_repair_paths`. The user
types `crate repair paths`. That is the issue #37 landing, reachable on
`main`. `repair` is not a landed leaf, so `_group_parser` creates a new
group and then adds `paths` under it.

Keeping the name `doctor.repair-paths` under the existing `doctor` parser
does not work. That would require making `doctor` a group and moving the
check verb under it (`crate doctor check`, or some other second word). That
is a breaking rename of a landed verb. argparse has no way to let
`crate doctor` stay a leaf and also accept `crate doctor repair-paths`.

## Guidance

Before landing a `planned_in` verb, check whether `name.split(".")[0]` is
already a landed one-word `Entry.name`. If it is, pick a first word that is
not a leaf. Do this at declaration, not at the first CLI drive.

A test that walks landed entries and planned entries for this prefix
collision would have failed when the name was written, months before the
module existed. The current countdown only asks whether the module is
present (`tests/test_cli_contract.py:1138-1155`). It does not ask whether
argparse can build the path. Discharging `planned_in` is what the countdown
demands. Discharging it is also what makes the tree unstartable. The
countdown is doing its job. The job is incomplete.

Do not try to nest under an existing leaf. A landed one-word verb has
already called `add_parser` on that word as a command, not as a group.
There is no hook to hang a child on. The only ways out are a first word
that is not a leaf, or a breaking rename of the landed verb into a group.
Issue #37 took the first. The second is not a landing, it is a product
change.

A group prefix is not this collision. `adopt.scan` and `adopt.apply` share
`adopt` because both go through `_group_parser` and the groups cache
returns the same subparsers object. Two groups on one word are one group.
A leaf and a group on one word are a refusal.

The landed one-word verbs that already occupy a root word include `setup`,
`doctor`, `status`, `login`, `converge`, and `rebuild`. A new grouped verb
must not start with any of those. `setbuild` and `master` are still planned
one-word names (`src/cratekit/cli/registry.py:1368-1396`). They become the
same kind of leaf the moment their `planned_in` clears. Treat a planned
one-word name as a reserved leaf too, or the next unit that groups under
that word will hit this the day the leaf lands.

When the countdown goes red because a new module exists, look at the
entry's `name` before clearing the marker. If the first word is already a
leaf, rename first, then clear. Clearing first, then driving the suite, is
how this presented: a usage test that does not mention the new verb, an
`ArgumentError` that names a different verb, and a parser that will not
build at all.

## Why This Matters

The failure is not a red assertion on the new verb. It is a construction
refusal of the entire CLI. Every test that builds the parser goes red,
including tests that never name the new verb and never intend to exercise
it. The first hit on issue #37 was a status-code ownership test whose
argv is a flag that does not exist. A reader who starts from that failure
looks at exit code 2, not at the registry.

The collision is silent at declaration and loud at the wrong moment.
Planned verbs are excluded from `landed_entries()`, so `build_parser` never
sees them. The name can be wrong for the whole life of the countdown. The
moment the module exists, the countdown forces the marker off, the verb
enters the landed set, and the next `drive` refuses the product. The
authoring act and the failing act are different units, different files,
and often different sessions.

This is not the same problem as a countdown discharge that drops a test
file from collection. That neighbour is about `@requires` and `PENDING`
keys: delete the register entry without removing the decorator, and pytest
cannot collect the file. This is about a verb path whose first word is
already a leaf. They share a landing moment (a module appears, a marker
must expire). They do not share a mechanism. Treating them as one lesson
would send the next session to the wrong file.

U23 sits in the same landing area and is also not this defect.
`adopt.scan` and `adopt.apply` shared one `module=` string, so `planned_in`
could not expire for the ready half. The countdown keys on the module
path, not on the verb name. They split into `scan_cli` and `apply_cli`.
The comment that records that decision is in
`src/cratekit/adopt/scan_cli.py:3-9`. Same table, same expiry test,
different cause.

## When to Apply

Every time a `planned_in` verb is about to land, and its `name` contains a
dot. Concretely:

- A new CLI name is being chosen next to an existing leaf such as
  `doctor`, `status`, or `setup`.
- The registry is about to add a grouped verb under a word that already
  called `add_parser` as a leaf.
- `planned_in` is being discharged because the module now exists.
  `test_a_planned_verb_whose_module_has_landed_must_lose_its_marker` is
  red. That is the moment this collision becomes a running parser.
- A unit is about to create the module a planned verb already names. The
  name has to be safe before the file exists, because creating the file
  is what forces the landing.

Apply it at declaration if the name is new, and again at discharge if the
name is old. The declaration check is the one that would have failed
before issue #37 spent a landing on a rename. The discharge check is the
one that still has to catch names that were written before the rule
existed.

## Examples

Issue #37, the path-repair verb, on `main`.

The planned name was `doctor.repair-paths`. `doctor` had already landed as
a one-word leaf in module `cratekit.cli.doctor`
(`src/cratekit/cli/registry.py:523-531`). The repair module was created as
`cratekit.intake.repair_cli`. The countdown at
`tests/test_cli_contract.py:1138` went red: the module exists, so
`planned_in` must go. Clearing the marker put the verb in
`landed_entries()`. `build_parser` then did this, in order:

1. `doctor` is one word, so `root.add_parser("doctor")`.
2. `doctor.repair-paths` is two words, so
   `_group_parser(root, groups, ("doctor",))`.
3. `_group_parser` does `root.add_parser("doctor")` a second time.

argparse raised `ArgumentError: argument <command>: conflicting subparser:
doctor`. The suite failed in
`test_status_two_belongs_to_the_argument_parser_and_to_nothing_else`
because that test is an early `drive` of an unknown flag, and `drive`
builds the whole parser.

The name that landed is `repair.paths`
(`src/cratekit/cli/registry.py:533-548`). `repair` is not a landed leaf.
`_group_parser` creates a `repair` group, then `add_parser("paths")`. The
user types `crate repair paths`. The check verb stays `crate doctor`.

U23 is the neighbour in the same landing area, not the same defect. The
two adoption verbs shared one `module=` string. The marker test that
expires a `planned_in` keys on that string, so the half that was ready
was held back by the half that was not. They split. `src/cratekit/adopt/scan_cli.py:3-9`
says so in the module that exists because of that split:

```3:9:src/cratekit/adopt/scan_cli.py
WHY THIS IS A MODULE OF ITS OWN, AND WHY ITS SIBLING IS NOT BESIDE IT. The two
adoption verbs are not in the same position and never were. ``adopt.apply``
writes the database, is destructive, and declares two gates; ``adopt.scan``
declares none, writes nothing, and reads. They shared one ``module=`` string in
the registry, and the marker test that expires a ``planned_in`` keys on that
string, so the half that is ready was held back by the half that is not, for no
reason of its own. Splitting them costs one file.
```

That is a countdown keyed on a module path. This is argparse refusing a
path word. Both fire when a planned verb is forced to land. They are
fixed in different places.

## Related

- [Discharging a countdown entry by half takes a whole test file out of collection](countdown-entry-discharge-drops-a-whole-test-file.md):
  countdown discharge that drops a file from collection. Same landing
  moment, a module appears and a marker must expire. Different mechanism,
  `@requires` and `PENDING` keys, not verb paths.
- `src/cratekit/adopt/scan_cli.py:3-9`: U23 split of `adopt.scan` from
  `adopt.apply`. Countdown keyed on the module path, not on the verb
  name. Same landing area, different cause.
- `tests/test_cli_contract.py:1138-1155`: the `planned_in` expiry test.
  It asks whether the module exists. It does not ask whether the path
  can be built.
- `src/cratekit/cli/__init__.py:168-239`: `_group_parser` and
  `build_parser`. The leaf versus group collision lives here.
- `src/cratekit/cli/registry.py:217-219`: `Entry.path`. The first path
  word is `name.split(".")[0]`. That is the check.
- `src/cratekit/cli/registry.py:523-548`: the landed `doctor` leaf and
  the `repair.paths` verb issue #37 shipped instead of
  `doctor.repair-paths`.
