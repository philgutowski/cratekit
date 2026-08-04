"""Every mutation row for round 7, as an exact text substitution.

Each tuple is (id, description, OLD text, NEW text). The old text is a verbatim
slice of ``tests/modules/test_reports.py`` as this branch ships it, and every one
of the sixty eight applies exactly once. A driver replaces one of them alone,
runs the suite reading node ids off ``report.nodeid``, restores the file and
verifies a checksum.

THIS FILE EXISTS BECAUSE TWO EARLIER ROWS CANNOT BE REPRODUCED. ``N05`` and
``N22`` carry recorded counts that no later spelling has matched, and the reason
in both cases is that the revert's exact text was never written down. A number
without its spelling is not a measurement anyone can re-run.
"""

# (id, description, old, new)
ROWS = [
    # ---------------- F1: the family ----------------
    (
        "P01",
        "`_inherited_attributes` answers nothing, so no class reaches what its family declared",
        '    found: dict[str, _Bound] = {}\n    for one in families:\n        upward = _related(one, families, upward=True)',
        '    found: dict[str, _Bound] = {}\n    for one in []:\n        upward = _related(one, families, upward=True)',
    ),
    (
        "P02",
        "`_inherited_attributes` stops resolving a CLASS attribute through the bases, so `Row.mod` never finds `Base.mod`",
        '        for other in upward:\n            _carry(found, declared, other, one, f"{other}.")',
        '        for other in upward[:1]:\n            _carry(found, declared, other, one, f"{other}.")',
    ),
    (
        "P03",
        "`_inherited_attributes` resolves an INSTANCE attribute upward only, so a mixin's method cannot see what its subclass binds",
        '        for other in upward + [key for key in downward if key not in upward]:\n            _carry(found, declared, other, one, f"{other}{_INSTANCE}.")',
        '        for other in upward:\n            _carry(found, declared, other, one, f"{other}{_INSTANCE}.")',
    ),
    (
        "P04",
        "`_inherited_attributes` resolves an INSTANCE attribute downward only, so a subclass cannot see what its base's constructor bound",
        '        for other in upward + [key for key in downward if key not in upward]:\n            _carry(found, declared, other, one, f"{other}{_INSTANCE}.")',
        '        for other in downward:\n            _carry(found, declared, other, one, f"{other}{_INSTANCE}.")',
    ),
    (
        "P05",
        "`_related` walks ONE HOP instead of transitively, so a grandparent is not a relative",
        "    seen, order, queue = {start}, [start], [start]\n    while queue:\n        one = queue.pop(0)",
        "    seen, order, queue = {start}, [start], [start]\n    while queue:\n        one = queue.pop(0)\n        if one != start:\n            continue",
    ),
    (
        "P06",
        "`_related` reads a family as one CONNECTED COMPONENT, walking both directions at once",
        "        if upward:\n            step: tuple[str, ...] = families.get(one, ())\n        else:\n            step = tuple(key for key, bases in families.items() if one in bases)",
        "        step: tuple[str, ...] = families.get(one, ()) + tuple(\n            key for key, bases in families.items() if one in bases\n        )",
    ),
    (
        "P07",
        "`_class_of` stops resolving a class's BASES, so every class is its own family",
        "    return _Class(\n        _class_key(node),\n        tuple(\n            found.key\n            for found in (_bound_value(one, table, instance) for one in node.bases)\n            if isinstance(found, _Class)\n        ),\n    )",
        "    return _Class(_class_key(node), ())",
    ),
    (
        "P08",
        "`_writer_bindings` folds REACHED back into DECLARED, so a derived key is re-derived from",
        "        names, direct = _walk_bindings(tree, reached, frozenset(), declared, families)\n        reached = _inherited_attributes(declared, families)",
        "        names, direct = _walk_bindings(tree, reached, frozenset(), declared, families)\n        reached = _inherited_attributes(declared, families)\n        declared.update(reached)",
    ),
    (
        "P09",
        "`_walk_bindings` carries out the scope's whole VIEW rather than its OWN bindings, which is what round six shipped",
        "    objects.update(\n        {key: value for key, value in own.items() if not key.isidentifier()}\n    )",
        "    objects.update(\n        {key: value for key, value in visible.items() if not key.isidentifier()}\n    )",
    ),
    (
        "P10",
        "`_member_scope` stops reading `_attachments`, so a method attached by `Row.go = _go` is nobody's method",
        '    attached = _attachments(scope).get(getattr(nested, "name", ""), "")\n    if attached:\n        return attached, _method_instance(nested, attached)\n',
        "",
    ),
    (
        "P11",
        "the audit stops reading `_attachments`, so an attached writer is read as a plain module level function",
        '            owner = (\n                _class_key(node)\n                if isinstance(node, ast.ClassDef)\n                else attached.get(node.name, "")\n            )',
        '            owner = _class_key(node) if isinstance(node, ast.ClassDef) else ""',
    ),
    (
        "P12",
        "the audit stops handing `mutations_in` an INSTANCE, so an attached function's first parameter is nobody's",
        "                instance=(\n                    _Instance()\n                    if isinstance(node, ast.ClassDef)\n                    else _method_instance(node, owner)\n                ),\n",
        "",
    ),
    # ---------------- F3 and F4: class identity ----------------
    (
        "P13",
        "`_class_key` answers the class's NAME, which is round six's identity, so two `class Keeper` are one class",
        '    return f"{node.name}{_DEFINED}{node.lineno}"',
        "    return node.name",
    ),
    (
        "P14",
        "`_scope_own_bindings` stops recording a nested CLASS as a binding of its own name",
        "            if isinstance(nested, ast.ClassDef)\n        }",
        "            if False\n        }",
    ),
    (
        "P15",
        "`_bound_value` stops resolving an attribute THROUGH a class, so `Keeper.mod` is only ever a flat spelling",
        '    if isinstance(node, ast.Attribute):\n        reached = _bound_value(node.value, table, instance)\n        if isinstance(reached, _Class):\n            found = table.get(f"{reached.key}.{node.attr}", "")\n            if found:\n                return found\n',
        "",
    ),
    (
        "P17",
        "`_walk_bindings` stops recording who inherits from whom, so the closure has no family to take",
        "        if isinstance(nested, ast.ClassDef):\n            families[member] = _class_of(nested, visible, instance).bases",
        "        if isinstance(nested, ast.ClassDef) and False:\n            families[member] = _class_of(nested, visible, instance).bases",
    ),
    # ---------------- F2: the namespace propagation ----------------
    (
        "R03",
        "`_mapping_operands` stops yielding a CALL's ARGUMENTS, so `dict(vars(Path))` and `ChainMap(vars(Path))` carry nothing",
        "        yield from node.args\n        yield from (word.value for word in node.keywords)",
        "        yield from (word.value for word in node.keywords)",
    ),
    (
        "R04",
        "`_mapping_operands` stops yielding a `**` SPREAD value in a dict literal",
        "    elif isinstance(node, ast.Dict):\n        yield from (\n            value for key, value in zip(node.keys, node.values) if key is None\n        )",
        "    elif isinstance(node, ast.Dict):\n        return",
    ),
    (
        "R13",
        "`_mapping_operands` stops yielding a BINARY OPERATOR's operands, so `Path.__dict__ | {}` carries nothing",
        "    elif isinstance(node, ast.BinOp):\n        yield node.left\n        yield node.right",
        "    elif isinstance(node, ast.BinOp):\n        return",
    ),
    (
        "R14",
        "`_mapping_operands` stops yielding a method call's RECEIVER, so `vars(Path).copy()` carries nothing",
        "        if isinstance(node.func, ast.Attribute):\n            yield node.func.value\n",
        "",
    ),
    (
        "R15",
        "`_mapping_operands` stops yielding a call's KEYWORD values, so `dict(**vars(Path))` carries nothing",
        "        yield from node.args\n        yield from (word.value for word in node.keywords)",
        "        yield from node.args",
    ),
    (
        "R16",
        "`_call_mutations`'s namespace ASKED branch requires ARGUMENTS again, so a mapping method that takes none is invisible",
        "        space = _bound_value(func.value, resolved, instance)\n        if isinstance(space, _Namespace):\n            said = _namespace_reads(\n                space,\n                node.args[0] if node.args else None,",
        "        space = _bound_value(func.value, resolved, instance)\n        if isinstance(space, _Namespace) and node.args:\n            said = _namespace_reads(\n                space,\n                node.args[0] if node.args else None,",
    ),
    # ---------------- round 6's rows, re-run ----------------
    (
        "R01",
        "`_namespace_of` stops recognising `__dict__`",
        '    if isinstance(node, ast.Attribute) and node.attr == "__dict__":\n        return _Namespace(_receiver_key(node.value, instance))\n',
        "",
    ),
    (
        "R02",
        "`_namespace_of` stops recognising `vars()`",
        '    if (\n        isinstance(node, ast.Call)\n        and getattr(node.func, "id", "") == "vars"\n        and len(node.args) == 1\n        and not node.keywords\n    ):\n        return _Namespace(_receiver_key(node.args[0], instance))\n',
        "",
    ),
    (
        "R05",
        "RULE 5 READS ITS RECEIVER INLINE AGAIN, which is what round five shipped: `_namespace_of` off the subscript's own `value`, table never asked",
        "            space = _bound_value(node.value, resolved, instance)\n            if isinstance(space, _Namespace):",
        "            space = _namespace_of(node.value, resolved, instance)\n            if isinstance(space, _Namespace):",
    ),
    (
        "R06",
        "rule 5 drops the namespace requirement, comparing every constant subscript key against the mutation set",
        "            space = _bound_value(node.value, resolved, instance)\n            if isinstance(space, _Namespace):\n                said = _namespace_reads(\n                    space, node.slice, resolved, instance, reflection=reflection\n                )",
        "            space = _bound_value(node.value, resolved, instance)\n            if True:\n                said = _namespace_reads(\n                    _Namespace(), node.slice, resolved, instance, reflection=reflection\n                )",
    ),
    (
        "R06b",
        "ROUND FOUR'S LITERAL RULE 5, the constant key compared against FILESYSTEM_MUTATIONS with no receiver and no owner read",
        """            space = _bound_value(node.value, resolved, instance)
            if isinstance(space, _Namespace):
                said = _namespace_reads(
                    space, node.slice, resolved, instance, reflection=reflection
                )
                if said is not None:
                    found.append(f"line {node.lineno}: [{said}]")""",
        """            index = node.slice
            if isinstance(index, ast.Constant) and index.value in FILESYSTEM_MUTATIONS:
                found.append(f"line {node.lineno}: [{index.value!r}]")""",
    ),
    (
        "R07",
        "`_namespace_reads` stops reporting a key it CANNOT READ",
        '    if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):\n        return "<a key this cannot read>" if reflection else None',
        "    if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):\n        return None",
    ),
    (
        "R08",
        "`_namespace_reads` reports an unreadable key with the reflection switch OFF too",
        '    if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):\n        return "<a key this cannot read>" if reflection else None',
        '    if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):\n        return "<a key this cannot read>"',
    ),
    (
        "R09",
        "`_call_mutations` drops the namespace ASKED branch entirely",
        "        space = _bound_value(func.value, resolved, instance)\n        if isinstance(space, _Namespace):\n            said = _namespace_reads(\n                space,\n                node.args[0] if node.args else None,\n                resolved,\n                instance,\n                reflection=reflection,\n            )\n            if said is not None:\n                return [f\"line {node.lineno}: {name}({said})\"]",
        "        pass",
    ),
    (
        "R10",
        "`_returned_value` hands back modules only, so a helper returning an attribute mapping binds nothing",
        "            owner = _bound_value(child.value, modules, instance)\n            if owner:\n                return owner",
        "            owner = _bound_value(child.value, modules, instance)\n            if isinstance(owner, str) and owner:\n                return owner",
    ),
    (
        "R11",
        "`_namespace_reads` drops the OWNER read, so `vars(config)[\"save\"]` is missed",
        '    named = wanted.value in FILESYSTEM_MUTATIONS or (\n        owner and f"{owner}.{wanted.value}" in QUALIFIED_MUTATIONS\n    )',
        "    named = wanted.value in FILESYSTEM_MUTATIONS",
    ),
    (
        "R12",
        "`_global_aliases` answers nothing",
        "    return {\n        f\"globals()[{name!r}]\": value\n        for name, value in modules.items()\n        if name.isidentifier()\n    }",
        "    return {}",
    ),
    (
        "Q01",
        "`_receiver_key` ignores the owning class, so two `self` in one file share one key",
        "    if isinstance(node, ast.Name):\n        return instance.root if instance.name == node.id else node.id",
        "    if isinstance(node, ast.Name):\n        return node.id",
    ),
    (
        "Q02",
        "`_method_instance` keys on the literal name `self` instead of the FIRST POSITIONAL parameter",
        '    return _Instance(positional[0].arg, f"{owner}{_INSTANCE}")',
        '    return _Instance("self", f"{owner}{_INSTANCE}")',
    ),
    (
        "Q03",
        "`_method_instance` stops exempting a `staticmethod`",
        '    if not positional or "staticmethod" in kinds:\n        return _Instance()',
        "    if not positional:\n        return _Instance()",
    ),
    (
        "Q04",
        "`_method_instance` reads a `classmethod`'s first parameter as an instance",
        '    if "classmethod" in kinds:\n        return _Instance(positional[0].arg, owner)\n',
        "",
    ),
    (
        "Q06",
        "`ast.ClassDef` dropped from `_SCOPES`, which is the reading round five shipped",
        "    ast.FunctionDef,\n    ast.AsyncFunctionDef,\n    ast.ClassDef,\n    ast.Lambda,",
        "    ast.FunctionDef,\n    ast.AsyncFunctionDef,\n    ast.Lambda,",
    ),
    (
        "Q07",
        "`_walk_bindings` stops writing the `<Class>.<name>` attribute key",
        '                objects[f"{owner}.{key}"] = value\n                objects[f"{owner}{_INSTANCE}.{key}"] = value',
        '                objects[f"{owner}{_INSTANCE}.{key}"] = value',
    ),
    (
        "Q08",
        "`_walk_bindings` stops writing the `<Class>::self.<name>` key",
        '                objects[f"{owner}.{key}"] = value\n                objects[f"{owner}{_INSTANCE}.{key}"] = value',
        '                objects[f"{owner}.{key}"] = value',
    ),
    (
        "Q09",
        "`_handed_to_members` hands a class's methods the table the CLASS built rather than the one it inherited",
        "    return outside if isinstance(scope, ast.ClassDef) else inside",
        "    return inside",
    ),
    (
        "Q11",
        "`_defined_here` stops reading a `ClassDef`, so a class no longer takes its own name",
        "        if isinstance(nested, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))",
        "        if isinstance(nested, (ast.FunctionDef, ast.AsyncFunctionDef))",
    ),
    (
        "Q13",
        "`_member_scope` stops dropping the instance when a nested scope takes that name back",
        "    if instance.name and instance.name in _names_taken(nested):\n        return owner, _Instance()\n",
        "",
    ),
    (
        "Q14",
        "`_member_scope` stops carrying the instance into a nested scope, so a closure over `self` loses it",
        "    return owner, instance\n\n\ndef _handed_to_members",
        "    return owner, _Instance()\n\n\ndef _handed_to_members",
    ),
    (
        "Q15",
        "a method's RETURNED value is keyed without its class",
        '                root = f"{owner}{_INSTANCE}." if isinstance(scope, ast.ClassDef) else ""',
        '                root = ""',
    ),
    (
        "Q16",
        "the audit stops naming a `ClassDef` as its own owner, so every method's `self` renders unqualified",
        '            owner = (\n                _class_key(node)\n                if isinstance(node, ast.ClassDef)\n                else attached.get(node.name, "")\n            )',
        '            owner = "" if isinstance(node, ast.ClassDef) else attached.get(node.name, "")',
    ),
    (
        "T01",
        "`_flag_names` stops reading a BARE NAME, so an imported `os` flag is unreadable",
        "    if isinstance(node, ast.Name):\n        return [node.id]",
        "    if isinstance(node, ast.Name):\n        return None",
    ),
    (
        "T02",
        "`_flag_names` answers a READING flag for an expression it cannot read at all, so `os.open(p, chosen())` reads",
        "    if isinstance(node, ast.Name):\n        return [node.id]\n    return None",
        '    if isinstance(node, ast.Name):\n        return [node.id]\n    return ["O_RDONLY"]',
    ),
    (
        "U01",
        "`_invoked_reads` answers with EVERY reflective read rather than only the ones whose result is called",
        "def _invoked_reads(tree: ast.AST) -> frozenset[int]:",
        "def _invoked_reads(tree: ast.AST) -> frozenset[int]:\n    return frozenset(\n        id(node) for node in ast.walk(tree) if _reflective_call(node)\n    )",
    ),
    (
        "B09",
        "a computed `__getattribute__` is gated on the reflection switch again instead of on its result being called",
        '        if id(node) in invoked or (reflection and name == "getattr"):',
        '        if (id(node) in invoked and name == "getattr") or reflection:',
    ),
    (
        "S16",
        "`_visible_bindings` adds the scope's own bindings BEFORE shadowing instead of after",
        "    taken = _names_taken(node)\n    kept = {key: owner for key, owner in modules.items() if key not in taken}\n    reachable = frozenset(name for name in direct if name not in taken)\n    own, own_direct = _scope_own_bindings(node, kept, instance)\n    kept.update(own)",
        "    taken = _names_taken(node)\n    reachable = frozenset(name for name in direct if name not in taken)\n    own, own_direct = _scope_own_bindings(node, dict(modules), instance)\n    merged = {**modules, **own}\n    kept = {key: owner for key, owner in merged.items() if key not in taken}",
    ),
    (
        "N21",
        "`mutations_in` stops descending into NESTED SCOPES",
        "    for nested in _nested_scopes(tree):\n        member, member_instance = _member_scope(tree, owner, instance, nested)\n        found += mutations_in(",
        "    for nested in []:\n        member, member_instance = _member_scope(tree, owner, instance, nested)\n        found += mutations_in(",
    ),
    (
        "N22",
        "`_receiver_module` answers an UNRESOLVED name with itself",
        "    found = _bound_value(node, modules, instance)\n    return found if isinstance(found, str) else \"\"",
        '    found = _bound_value(node, modules, instance)\n    if isinstance(found, str) and found:\n        return found\n    return _receiver_key(node, instance).rsplit(".", 1)[-1]',
    ),
    (
        "N05",
        "the rebinding sweep removed, imports only",
        "        for child in _scope_nodes(scope):\n            found, names = _binds(child, table, instance)\n            direct |= names",
        "        for child in _scope_nodes(scope):\n            if not isinstance(child, (ast.Import, ast.ImportFrom)):\n                continue\n            found, names = _binds(child, table, instance)\n            direct |= names",
    ),
    (
        "M35",
        "`write_text` dropped from `FILESYSTEM_MUTATIONS`",
        '        "write_text",\n',
        "",
    ),
    (
        "N12",
        "the ASSIGNMENT rebinding branch removed",
        "    if isinstance(node, (ast.Assign, ast.AnnAssign)):\n        targets = node.targets if isinstance(node, ast.Assign) else [node.target]",
        "    if isinstance(node, (ast.Assign, ast.AnnAssign)) and False:\n        targets = node.targets if isinstance(node, ast.Assign) else [node.target]",
    ),
    (
        "S01",
        "`_names_taken` reverted to PARAMETERS ONLY, the flat table round four shipped",
        "    taken = set(_defined_here(node))\n    for child in _scope_nodes(node):\n        taken |= _bound_here(child)\n    return frozenset(taken)",
        "    taken = set()\n    for child in _scope_nodes(node):\n        if isinstance(child, ast.arguments):\n            taken |= _bound_here(child)\n    return frozenset(taken)",
    ),
    (
        "C01",
        "`_called_keys` answers nothing",
        "def _called_keys(tree: ast.AST) -> frozenset[str]:",
        "def _called_keys(tree: ast.AST) -> frozenset[str]:\n    return frozenset()",
    ),
    (
        "S09",
        "`_bound_here` stops reading a PARAMETER LIST",
        "    if isinstance(node, ast.arguments):\n        named = [*node.posonlyargs, *node.args, *node.kwonlyargs]",
        "    if isinstance(node, ast.arguments) and False:\n        named = [*node.posonlyargs, *node.args, *node.kwonlyargs]",
    ),
    (
        "C05",
        "`_invoked_reads` stops reading a read BOUND TO A NAME the file calls",
        "        for key, value in _stored(node):\n            if key in keys:\n                for read in _handed_over(value):\n                    found.add(id(read))",
        "        for key, value in _stored(node):\n            if False:\n                for read in _handed_over(value):\n                    found.add(id(read))",
    ),
    (
        "C09",
        "`_invoked_reads` stops reading the INLINE spelling",
        "        if isinstance(node, ast.Call):\n            for read in _handed_over(node.func):\n                found.add(id(read))",
        "        if isinstance(node, ast.Call):\n            for read in []:\n                found.add(id(read))",
    ),
    (
        "S18",
        "`_walk_bindings` stops carrying OBJECT bindings out of the scope that made them",
        "    objects.update(\n        {key: value for key, value in own.items() if not key.isidentifier()}\n    )",
        "",
    ),
    (
        "S21",
        "`_scope_own_bindings` stops recording a FAILED attempt for a binding `_binds` cannot read",
        '            for name in _bound_here(child) - set(found):\n                attempts.setdefault(name, []).append("")',
        "            pass",
    ),
    (
        "S22",
        "`_scope_own_bindings` stops recording a failed attempt for a nested DEFINITION, keeping only the classes",
        '        for name in _defined_here(scope):\n            attempts.setdefault(name, []).append(made.get(name, ""))',
        "        for name in _defined_here(scope):\n            if name in made:\n                attempts.setdefault(name, []).append(made[name])",
    ),
    (
        "S14",
        "`_scope_own_bindings` accepts a name when ANY binding of it resolves rather than when EVERY binding agrees",
        "            if all(owners) and len(set(owners)) == 1",
        "            if any(owners)",
    ),
    (
        "S15",
        "`_scope_own_bindings` inner fixed point cut to ONE pass",
        "        if (objects, settled) == before:\n            return {**objects, **settled}, frozenset(direct)",
        "        return {**objects, **settled}, frozenset(direct)",
    ),
    (
        "S19",
        "`_walk_bindings` stops recording a function's RETURNED module",
        "            returned = _returned_value(nested, nested_visible, member_instance)\n            if returned:",
        "            returned = _returned_value(nested, nested_visible, member_instance)\n            if False:",
    ),
    (
        "S20",
        "`_writer_bindings` outer fixed point cut to ONE pass",
        "        if (declared, families) == before:\n            return {",
        "        if True:\n            return {",
    ),
]
