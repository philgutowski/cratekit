"""Every mutation row for round 9, as an exact text substitution.

Each tuple is ``(id, target, description, OLD text, NEW text)``. ``target`` names
the file the substitution applies to, because two rows below inject a defect into
a document or into the suite's own citation guard rather than reverting a
function.

The old text is a verbatim slice of the file as this branch ships it and every one
applies exactly once. A driver replaces one of them alone, runs
`tests/modules/test_reports.py` reading node ids off ``report.nodeid``, restores
the file and verifies a checksum.

NO LINE IN THIS FILE IS A COLLISION MARKER AND NO LINE CITES A RESIDUAL BY NUMBER.
The one row that needs both builds them by concatenation, so this file needs no
exemption passage of its own and the citation guard reads every line of it. That
is deliberate: round eight's reverts file needed a delimited passage, and a file
that needs no exemption is a file the guard cannot be walked past in.

FOUR ROUND EIGHT ROWS ARE RE-SPELLED HERE, `V02`, `V03`, `V19` and `S18`, because
round nine edited the lines they anchored on. Their round eight text no longer
occurs anywhere in the suite, which is the failure mode this file exists to
prevent: a row whose spelling stops matching becomes a number nobody can re-run.
"""

SUITE = "tests/modules/test_reports.py"
MUTATION = "docs/mutation-u34.md"

# (id, target, description, old, new)
ROWS = [
    # ==== F1: a branch exempts a NAME's veto and never an attribute's ====
    (
        "W01",
        SUITE,
        "the branch rule applied to the OBJECT half again, which is the round's whole defect: six ordinary subclass overrides written one indent in are reported as writes",
        "                supplied = key.isidentifier() or chained or bool(table.get(key))\n                if key in idle or (optional and not owner and supplied):",
        "                if key in idle or (optional and not owner):",
    ),
    (
        "W02",
        SUITE,
        "the restriction the flag alone would have been: an object key's veto always stands inside a branch, so a constructor that chains to its base is quiet",
        "                supplied = key.isidentifier() or chained or bool(table.get(key))",
        "                supplied = key.isidentifier()",
    ),
    (
        "W03",
        SUITE,
        "`_scope_own_bindings` stops asking whether the scope CHAINS, so `super().__init__()` above a conditional override reaches nothing",
        "                supplied = key.isidentifier() or chained or bool(table.get(key))",
        "                supplied = key.isidentifier() or bool(table.get(key))",
    ),
    (
        "W04",
        SUITE,
        "`_scope_own_bindings` stops asking whether the key is ALREADY SUPPLIED, so a class body binding under a conditional override reaches nothing",
        "                supplied = key.isidentifier() or chained or bool(table.get(key))",
        "                supplied = key.isidentifier() or chained",
    ),
    (
        "W05",
        SUITE,
        "`_chains_to_base` answers yes for every scope, so an override in a branch is optional whatever the scope does",
        "def _chains_to_base(scope: ast.AST) -> bool:",
        "def _chains_to_base(scope: ast.AST) -> bool:\n    return True",
    ),
    (
        "W06",
        SUITE,
        "`_chains_to_base` counts a chaining call written INSIDE a branch, so the arm that skips both the call and the override is read as reaching the base",
        "        if id(child) in skippable or not isinstance(child, ast.Call):",
        "        if not isinstance(child, ast.Call):",
    ),
    (
        "W07",
        SUITE,
        "`_chains_to_base` accepts any call at all rather than one that reaches an initializer, so `self.setup()` is read as chaining",
        '        if isinstance(child.func, ast.Attribute) and child.func.attr == "__init__":\n            return True',
        "        if isinstance(child.func, ast.Attribute):\n            return True",
    ),
    # ==== F2: a class body's INSTANCE spelling is fainter than an override ====
    (
        "W08",
        SUITE,
        "`_walk_bindings` writes a class body's instance spelling at full strength again, so an ordinary constructor under `mod = config` is reported as a write",
        '                _record(objects, f"{owner}{_INSTANCE}.{key}", value, faint, weak=True)',
        '                _record(objects, f"{owner}{_INSTANCE}.{key}", value, faint)',
    ),
    (
        "W09",
        SUITE,
        "`_record` stops MARKING a weak write, so nothing can tell a class body's instance spelling from an instance scope's own and the override never clears it",
        "        objects[key] = value\n        faint.add(key)\n        return",
        "        objects[key] = value\n        return",
    ),
    (
        "W10",
        SUITE,
        "`_record` stops letting an instance scope's unresolved write clear a weak one, so the class body answer survives an override",
        "    if value or key not in objects or key in faint:",
        "    if value or key not in objects:",
    ),
    # There is no `W14`. It reverted a `key.isidentifier()` filter inside what was
    # then `_deleted_attributes`, and it killed nothing, because the call site
    # tested the same thing again through `root.endswith(_INSTANCE)`. Two half
    # guards for one fact is what lets them drift, so the pair became one function,
    # `_restored_attributes`, which computes the key AND the class spelling under
    # it together. `W12` and `W13` row the two halves of that one function.
    #
    # There is no `W11`. Making the CLASS spelling a weak write as well was
    # measured and killed nothing, because a class body is the only thing in the
    # walk that ever writes `<class key>.<name>`: the flat `Keeper.mod = None`
    # spelling an outside scope writes is a DIFFERENT key, since the class key
    # carries the definition site. The asymmetry between the two spellings is
    # therefore carried entirely by `W08`, and a row that distinguishes nothing is
    # a number nobody can read. Recorded here rather than left out silently.
    # ==== F7: a delete reaches the class attribute under it ====
    (
        "W12",
        SUITE,
        "`_walk_bindings` stops reading a `del` of an object key, so an instance attribute deleted over a module valued class attribute reaches nothing",
        "    for key, through in _restored_attributes(scope, instance).items():",
        "    for key, through in {}.items():",
    ),
    (
        "W13",
        SUITE,
        "the restore lands on the CLASS spelling instead of the instance one, which is this repository's third recurring defect aimed at the round's own fix",
        '        _record(objects, key, objects.get(through, ""), faint)',
        '        _record(objects, through, objects.get(through, ""), faint)',
    ),
    # ==== F5: two spellings that were quiet and are not undecidable ====
    (
        "W15",
        SUITE,
        "`_rebound_to_itself` reads ONE receiver key again instead of the values the expression can evaluate to, so `Keeper = Keeper or None` throws the class away",
        "    sources = {\n        key\n        for key in (_receiver_key(one, instance) for one in _alternatives(node.value))\n        if key\n    }",
        '    sources = {_receiver_key(node.value, instance) if node.value is not None else ""} - {""}',
    ),
    (
        "W16",
        SUITE,
        "`_alternatives` reads a CALL through as well, so `Keeper = dataclass(Keeper)` is treated as decidable when it is not",
        "    elif node is not None:\n        yield node",
        "    elif isinstance(node, ast.Call):\n        yield from node.args\n    elif node is not None:\n        yield node",
    ),
    (
        "W17",
        SUITE,
        "the idle branch stops falling back to what the statement could still evaluate to, so `alias = alias or config` binds nothing at all",
        '                held = table.get(key, "") or found.get(key, "")',
        '                held = table.get(key, "")',
    ),
    # ==== F3 and F4: the citation guard's own two holes ====
    (
        "W18",
        SUITE,
        "an unclosed collision marker and a bare number citation inserted into the guard's OWN file, which is exactly the shape the pair exists to catch and which it was told not to look at",
        "_CITATION = re.compile",
        "# [[" + "collision-set]]\n# see R-" + "20 for the rest of it\n_CITATION = re.compile",
    ),
    (
        "W19",
        SUITE,
        "`_files_this_branch_writes` quietly stops covering a report module, which under the typed list left the whole suite green",
        "    return tuple(sorted(one for one in named if (REPO_ROOT / one).is_file()))",
        '    return tuple(\n        sorted(\n            one\n            for one in named\n            if (REPO_ROOT / one).is_file() and not one.endswith("reports/aging.py")\n        )\n    )',
    ),
    (
        "W20",
        SUITE,
        "`_citing_files` stops taking the residual file out of its own coverage, so the file whose SUBJECT is the numbers is policed for spelling them",
        "    return tuple(one for one in written if one != RESIDUAL_FINDINGS_NAME)",
        "    return tuple(written)",
    ),
    (
        "W21",
        SUITE,
        "a lone CLOSING marker injected into a covered file, which the guard that counted opens only could not see",
        "def _citing_lines(text: str):",
        "# [[/" + "collision-set]]\ndef _citing_lines(text: str):",
    ),
    (
        "W22",
        MUTATION,
        "the collision passage's OPENING marker removed from the mutation table, so the passage that spells the numbers is no longer exempt and no longer delimited",
        "[[" + "collision-set]]\n",
        "",
    ),
    # ==== round eight rows this round had to RE-SPELL ====
    (
        "V02",
        SUITE,
        "`_walk_bindings` writes a class body attribute only when it RESOLVED, so `mod = None` shadows nothing. Re-spelled: round nine added the faint tier",
        '            if key.isidentifier():\n                _record(objects, f"{owner}.{key}", value, faint)',
        '            if key.isidentifier() and value:\n                _record(objects, f"{owner}.{key}", value, faint)',
    ),
    (
        "V03",
        SUITE,
        "`_record` lets an unresolved key OVERWRITE a resolved one, so the answer depends on which scope the walk reached first. Re-spelled: round nine added the faint tier",
        "    if value or key not in objects or key in faint:\n        objects[key] = value",
        "    objects[key] = value",
    ),
    (
        "V19",
        SUITE,
        "`_scope_own_bindings` stops recording what an IDLE rebinding already held, so `class Keeper: config = config` binds no attribute. Re-spelled: round nine added the fallback",
        '            for key in idle:\n                # WHAT THE KEY HELD, and what the statement could still evaluate\n                # to when it held nothing this pass could read. ``alias = alias or\n                # config`` keeps its own value on one path and the module on the\n                # other, and reading only the first would lose the module.\n                held = table.get(key, "") or found.get(key, "")\n                if not held:\n                    continue\n                if key.isidentifier():\n                    attempts.setdefault(key, []).append(held)\n                else:\n                    objects[key] = held',
        "            pass",
    ),
    (
        "S18",
        SUITE,
        "`_walk_bindings` stops carrying OBJECT bindings out of the scope that made them. Re-spelled: round nine gave `_record` its faint argument",
        "    for key, value in own.items():\n        if not key.isidentifier():\n            _record(objects, key, value, faint)",
        "    pass",
    ),
]
