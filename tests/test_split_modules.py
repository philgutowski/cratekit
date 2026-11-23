"""``tests/_split_modules.py`` reads every part of each split module (R-1890).

The scans that read a split module through the helper trust its glob, so the
glob is held here against two independent lists of the parts: the module
table in ``docs/DEVELOPING.md``, which is what a person is told, and the call
time accessor each part holds back to its module, which is what the code does.
A part named off the convention, or a module whose table row drifts, fails
here rather than falling silently out of every scan at once.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from tests._split_modules import CORE, PACKAGE, SPLIT_MODULES, files_of, names_of, source_of

DEVELOPING = Path(__file__).resolve().parent.parent / "docs" / "DEVELOPING.md"


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


def test_the_glob_reads_every_part_that_reaches_back_to_its_module():
    accessors = _accessor_parts()
    assert all(accessors.values()), f"no accessor found for some module: {accessors}"
    for module, parts in accessors.items():
        read = {path.stem for path in files_of(module)}
        assert parts <= read, f"{module}'s scan misses {sorted(parts - read)}"


def test_the_module_comes_first_and_every_name_is_its_file():
    for module in SPLIT_MODULES:
        files = files_of(module)
        assert files[0].name == module.rsplit(".", 1)[-1] + ".py"
        assert len(set(files)) == len(files) > 1
        assert names_of(module) == tuple(f"{PACKAGE}.{path.stem}" for path in files)
        assert all(path.read_text(encoding="utf-8") in source_of(module) for path in files)
