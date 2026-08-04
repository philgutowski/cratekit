"""Every mutation row for round 8, as an exact text substitution.

Each tuple is ``(id, target, description, OLD text, NEW text)``. ``target`` names
the file the substitution applies to, because this round changes a document as
well as the suite: the citation rule was claimed over source, docstrings and tests
and broken in `docs/`, so the guard now reads `docs/` and two of the rows below
revert a document rather than a function.

The old text is a verbatim slice of the file as this branch ships it and every one
applies exactly once. A driver replaces one of them alone, runs
`tests/modules/test_reports.py` reading node ids off ``report.nodeid``, restores
the file from the git object database and verifies a checksum.

TWO ROUND SEVEN ROWS ARE RE-SPELLED HERE, `S01` and `S18`, because round eight
edited the lines they anchored on. Their round seven text no longer occurs, which
is the failure mode this file exists to prevent: a row whose spelling stops
matching becomes a number nobody can re-run.
"""

SUITE = "tests/modules/test_reports.py"
MUTATION = "docs/mutation-u34.md"
HANDOFF = "docs/HANDOFF.md"

# (id, target, description, old, new)
ROWS = [
    # ==== F1: an assignment that could not be read still takes the key back ====
    (
        "V01",
        SUITE,
        "`_scope_own_bindings` object half stops recording a FAILED attempt, which is the round's whole defect",
        '                elif owner:\n                    objects[key] = owner\n                else:\n                    objects.setdefault(key, "")',
        "                elif owner:\n                    objects[key] = owner",
    ),
    (
        "V02",
        SUITE,
        "`_walk_bindings` writes a class body attribute only when it RESOLVED, so `mod = None` shadows nothing",
        '            if key.isidentifier():\n                _record(objects, f"{owner}.{key}", value)\n                _record(objects, f"{owner}{_INSTANCE}.{key}", value)',
        '            if key.isidentifier() and value:\n                _record(objects, f"{owner}.{key}", value)\n                _record(objects, f"{owner}{_INSTANCE}.{key}", value)',
    ),
    (
        "V03",
        SUITE,
        "`_record` lets an unresolved key OVERWRITE a resolved one, so the answer depends on which scope the walk reached first",
        "    if value or key not in objects:\n        objects[key] = value",
        "    objects[key] = value",
    ),
    (
        "V04",
        SUITE,
        "`_carry` carries an unresolved key DOWNWARD too, so one subclass's override hides a sibling's real binding from a mixin",
        '            if other not in upward:\n                _carry(found, declared, other, one, f"{other}{_INSTANCE}.", overriding=False)',
        '            if other not in upward:\n                _carry(found, declared, other, one, f"{other}{_INSTANCE}.", overriding=True)',
    ),
    (
        "V05",
        SUITE,
        "`_carry` never carries an unresolved key, upward included, so a nearer ancestor's override stops blocking",
        "        if not key.startswith(prefix) or (not value and not overriding):",
        "        if not key.startswith(prefix) or not value:",
    ),
    (
        "V06",
        SUITE,
        "`_scope_own_bindings` drops a name that did not settle instead of answering it empty",
        '        settled = {\n            key: owners[0] if all(owners) and len(set(owners)) == 1 else ""\n            for key, owners in attempts.items()\n        }',
        "        settled = {\n            key: owners[0]\n            for key, owners in attempts.items()\n            if all(owners) and len(set(owners)) == 1\n        }",
    ),
    # ==== F2: two losses that are not undecidable ====
    (
        "V07",
        SUITE,
        "`_rebound_to_itself` answers nothing, so `Keeper = Keeper` is a second binding that vetoes the class",
        "    if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):\n        return frozenset()",
        "    if True:\n        return frozenset()",
    ),
    (
        "V08",
        SUITE,
        "`_names_taken` stops exempting a self rebinding, so `config = config` takes the name from the import",
        "        taken |= _bound_here(child) - _rebound_to_itself(child)",
        "        taken |= _bound_here(child)",
    ),
    (
        "V19",
        SUITE,
        "`_scope_own_bindings` stops recording what an IDLE rebinding already held, so `class Keeper: config = config` binds no attribute",
        '            for key in idle:\n                held = table.get(key, "")\n                if not held:\n                    continue\n                if key.isidentifier():\n                    attempts.setdefault(key, []).append(held)\n                else:\n                    objects[key] = held',
        "            pass",
    ),
    (
        "V20",
        SUITE,
        "an idle rebinding records a FAILED attempt when what it held cannot be read, which deadlocks `Keeper = Keeper` again",
        "                if not held:\n                    continue",
        "                if not held:\n                    attempts.setdefault(key, []).append(held)\n                    continue",
    ),
    (
        "V09",
        SUITE,
        "`_alternate_classes` records nothing, so two `class Keeper` in two arms leave only the last one reachable",
        "        if others:\n            found[_class_key(settled)] = others",
        "        if False:\n            found[_class_key(settled)] = others",
    ),
    (
        "V10",
        SUITE,
        "`_alternate_classes` calls two definitions in ONE statement list alternates too, which is the shape that is correctly quiet",
        "            if blocks.get(id(one)) != blocks.get(id(settled))",
        "            if True",
    ),
    (
        "V11",
        SUITE,
        "`_sequences` reads the scope's own body only, so two definitions inside an `if` are in no block at all",
        "    for holder in (scope, *_scope_nodes(scope)):",
        "    for holder in (scope,):",
    ),
    (
        "V12",
        SUITE,
        "`_inherited_attributes` stops carrying an ALTERNATE definition's attributes onto the name's settled class",
        '    for one, others in alternates.items():\n        for other in others:\n            _carry(found, declared, other, one, f"{other}.", overriding=False)',
        "    for one, others in []:\n        for other in others:\n            pass",
    ),
    (
        "V13",
        SUITE,
        "`_branched` answers nothing, so a veto written inside an arm a run can skip counts as if every run cast it",
        "    found: set[int] = set()\n    for holder in _scope_nodes(scope):\n        if not isinstance(holder, _BRANCHING):",
        "    found: set[int] = set()\n    for holder in []:\n        if not isinstance(holder, _BRANCHING):",
    ),
    (
        "V14",
        SUITE,
        "`_branched` counts a `finally` block as skippable, which is the one block every path runs",
        '_BRANCHED_FIELDS = ("body", "orelse", "handlers", "cases")',
        '_BRANCHED_FIELDS = ("body", "orelse", "handlers", "cases", "finalbody")',
    ),
    # ==== F4: the citation rule, checked over `docs/` ====
    (
        "V15",
        SUITE,
        "the citation guard stops exempting the delimited collision passage, so the one passage whose subject IS the numbers fails it",
        "        if _is_delimiter(line, _COLLISION_OPEN):\n            exempt = True",
        "        if False:\n            exempt = True",
    ),
    (
        "V16",
        SUITE,
        "the citation guard stops reading `docs/`, which is the exact width the earlier claim was checked at",
        '    "docs/mutation-u34.md",\n    "docs/mutation/u34-round-7-reverts.py",\n    "docs/mutation/u34-round-8-reverts.py",\n    "docs/HANDOFF.md",',
        "",
    ),
    # V17 records the spelling it reverts TO, which is a residual number, so this
    # one row is inside the delimited exemption for the same reason the collision
    # statement is: its subject IS the number rather than a use of it.
    # [[collision-set]]
    (
        "V17",
        HANDOFF,
        "the handoff's report-verbs citation restored to the NUMBER spelling this branch shipped it in",
        '| U27 | `cratekit.cli.reports` | the four report verbs, and the two report engines two of them still have none of. See the residual titled "Four report verbs were owed by a unit that was about to close, and named a module nobody could build": U27 is a judgement, not a decision |',
        "| U27 | `cratekit.cli.reports` | the four report verbs, and the two report engines two of them still have none of. See R-16: U27 is a judgement, not a decision |",
    ),
    # [[/collision-set]]
    (
        "V18",
        MUTATION,
        "the collision passage's CLOSING marker removed, which would exempt every line after it to the end of the file",
        "[[/collision-set]]",
        "",
    ),
    # ==== round seven rows this round had to RE-SPELL ====
    (
        "S01",
        SUITE,
        "`_names_taken` reverted to PARAMETERS ONLY, the flat table round four shipped. Re-spelled: round eight edited this line",
        "    taken = set(_defined_here(node))\n    for child in _scope_nodes(node):\n        taken |= _bound_here(child) - _rebound_to_itself(child)\n    return frozenset(taken)",
        "    taken: set[str] = set()\n    for child in _scope_nodes(node):\n        if isinstance(child, ast.arguments):\n            taken |= _bound_here(child)\n    return frozenset(taken)",
    ),
    (
        "S18",
        SUITE,
        "`_walk_bindings` stops carrying OBJECT bindings out of the scope that made them. Re-spelled: round eight replaced the update with `_record`",
        "    for key, value in own.items():\n        if not key.isidentifier():\n            _record(objects, key, value)",
        "    pass",
    ),
]
