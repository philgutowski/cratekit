"""``tests/_split_modules.py`` reads every part of each split module (R-1890).

The scans that read a split module through the helper trust its glob, so the
glob is held here against three independent lists of the parts: the module
table in ``docs/DEVELOPING.md``, which is what a person is told; the import
graph, since ``DEVELOPING.md`` says a part is imported only by its module and
that module's other parts; and the call time accessor most parts hold back
to their module. A part named off the convention fails here when it is in the
table, when only its module and its parts import it by an absolute import, or
when it holds an accessor in the spelling the parts use. One that escapes all
three is described in the helper's docstring.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from tests._split_modules import CORE, PACKAGE, SPLIT_MODULES, files_of, names_of, source_of

DEVELOPING = Path(__file__).resolve().parent.parent / "docs" / "DEVELOPING.md"
SRC = CORE.parent


def _glob_matched() -> dict[str, set[str]]:
    return {module: {path.stem for path in files_of(module)} for module in SPLIT_MODULES}


def _imports_by_module() -> dict[str, set[str]]:
    """Every authored module's dotted name, and the cratekit modules it imports anywhere in it."""
    found: dict[str, set[str]] = {}
    for path in sorted(SRC.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        name = ".".join(path.relative_to(SRC.parent).with_suffix("").parts)
        imported: set[str] = set()
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imported.add(node.module)
                imported.update(f"{node.module}.{alias.name}" for alias in node.names)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
        found[name] = imported
    return found


def _exclusive_parts() -> dict[str, set[str]]:
    """Each split module's core imports that nothing outside it and those imports imports.

    Grown to a fixed point from the module itself, so a part imported only by
    its module and by its sibling parts (``rb_tables``) joins once they have.
    """
    imports = _imports_by_module()
    found: dict[str, set[str]] = {}
    for module in SPLIT_MODULES:
        held = {module}
        grew = True
        while grew:
            grew = False
            for candidate in sorted(imports):
                if candidate in held or not candidate.startswith(f"{PACKAGE}."):
                    continue
                importers = {name for name, wanted in imports.items() if candidate in wanted}
                if importers and importers <= held:
                    held.add(candidate)
                    grew = True
        found[module] = {name.rsplit(".", 1)[-1] for name in held - {module}}
    return found


def _documented_parts() -> dict[str, set[str]]:
    """Each split module's parts as ``docs/DEVELOPING.md``'s table names them."""
    text = DEVELOPING.read_text(encoding="utf-8")
    section = text.split("## The guarded writer, the session and the restore, in parts", 1)[1]
    table: dict[str, set[str]] = {}
    for line in section.split("\n## ", 1)[0].splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or not cells[0].startswith("`core."):
            continue
        module = f"cratekit.{cells[0].strip('`')}"
        table[module] = set(re.findall(r"`([a-z_]+)`", cells[1]))
    return table


def _accessor_parts() -> dict[str, set[str]]:
    """Each core module holding a function that imports a split module and returns it."""
    found: dict[str, set[str]] = {module: set() for module in SPLIT_MODULES}
    short = {module.rsplit(".", 1)[-1]: module for module in SPLIT_MODULES}
    for path in sorted(CORE.glob("*.py")):
        if path.stem in short:
            continue
        for node in ast.parse(path.read_text(encoding="utf-8")).body:
            if not isinstance(node, ast.FunctionDef):
                continue
            bound: dict[str, str] = {}
            for inner in ast.walk(node):
                if isinstance(inner, ast.ImportFrom) and inner.module == PACKAGE:
                    for alias in inner.names:
                        if alias.name in short:
                            bound[alias.asname or alias.name] = short[alias.name]
            for inner in ast.walk(node):
                if isinstance(inner, ast.Return) and isinstance(inner.value, ast.Name):
                    if inner.value.id in bound:
                        found[bound[inner.value.id]].add(path.stem)
    return found


def test_every_split_module_has_a_row_in_the_developing_table():
    assert set(_documented_parts()) == set(SPLIT_MODULES)


def test_the_glob_reads_every_part_the_developing_table_names():
    for module, parts in _documented_parts().items():
        read = {path.stem for path in files_of(module)}
        assert parts, f"the table names no part for {module}, so it is not being read"
        assert parts <= read, f"{module}'s scan misses {sorted(parts - read)}"


def test_the_glob_reads_every_part_only_its_module_imports():
    exclusive = _exclusive_parts()
    assert all(exclusive.values()), f"the import graph found no part for some module: {exclusive}"
    for module, parts in exclusive.items():
        read = _glob_matched()[module]
        assert parts <= read, f"{module}'s scan misses {sorted(parts - read)}"


def test_a_module_holding_an_accessor_is_read_with_the_module_it_reaches():
    """Read with the module it reaches back to, or proved another module's part.

    A session part may break an import cycle with the writer's accessor, and is
    then the session's part, not the writer's: it passes only when the import
    graph proves it the session's (only the session and its parts import it).
    A writer part merely named ``session_*`` is not proved so, and fails.
    The accessor is read in the spelling the parts use, a module level
    function returning a name ``from cratekit.core import X`` bound.
    """
    accessors = _accessor_parts()
    assert all(accessors.values()), f"no accessor found for some module: {accessors}"
    globbed, exclusive = _glob_matched(), _exclusive_parts()
    proved = {part for module in SPLIT_MODULES for part in globbed[module] & exclusive[module]}
    for module, holders in accessors.items():
        unread = sorted(holders - globbed[module] - proved)
        assert not unread, f"{module}'s scan misses {unread}, which reach back to it"


def test_the_module_comes_first_and_every_name_is_its_file():
    for module in SPLIT_MODULES:
        files = files_of(module)
        assert files[0].name == module.rsplit(".", 1)[-1] + ".py"
        assert len(set(files)) == len(files) > 1
        assert names_of(module) == tuple(f"{PACKAGE}.{path.stem}" for path in files)
        assert all(path.read_text(encoding="utf-8") in source_of(module) for path in files)
