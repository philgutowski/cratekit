"""The reserved cause pins are read from one file per package (U296).

U125 keyed the pins by module so that two cards touching different modules
edit different lines. U296 holds them one file per package, under
``tests/ratchets/reserved_causes/``, so that a card splitting a module edits
no register another package's card edits. ``tests/_pinned_reserved_populations.py``
merges those files into the tables ``tests/test_reserved_causes.py`` reads.

That suite still compares every table with the tree, which is what holds the
merged pins equal to what was pinned before the split: the tree did not
change, so a pin lost or misfiled in the move fails there by its module's
name. What is proven here is the reader: that it merges, and that it refuses
a file it would otherwise read wrongly, at import, where nobody can miss it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests import _pinned_reserved_populations as pins
from tests._refactor_measure import measure


def _write(directory: Path, name: str, text: str) -> None:
    (directory / f"{name}.py").write_text(text, encoding="utf-8")


def test_each_packages_tables_are_merged_into_one_mapping_per_table(tmp_path):
    _write(
        tmp_path,
        "core",
        "KEBAB_LITERALS = {'core/config.py': ['config-unusable'], 'core/jobs.py': ['job-unknown']}\n"
        "NAMED_WITH_INTEGER = frozenset({'core/config.py'})\n",
    )
    _write(
        tmp_path,
        "modules.outbound",
        "KEBAB_LITERALS = {'modules/outbound/mirror.py': ['internal-error']}\n",
    )
    merged = pins.read_package_pins(tmp_path)
    assert merged["KEBAB_LITERALS"] == {
        "core/config.py": ["config-unusable"],
        "core/jobs.py": ["job-unknown"],
        "modules/outbound/mirror.py": ["internal-error"],
    }
    assert set(merged["NAMED_WITH_INTEGER"]) == {"core/config.py"}
    assert merged["LITERAL_HOLDERS"] == {}
    assert set(merged) == set(pins.PER_MODULE_TABLES)


def test_a_module_pinned_in_another_packages_file_is_refused(tmp_path):
    _write(tmp_path, "core", "KEBAB_LITERALS = {'write/trees.py': ['internal-error']}\n")
    with pytest.raises(ValueError, match=r"core\.py pins 'write/trees\.py'.*belongs in write\.py"):
        pins.read_package_pins(tmp_path)


def test_a_table_the_reader_does_not_know_is_refused_rather_than_ignored(tmp_path):
    """A misspelt table would otherwise be a pin that silently stopped pinning."""
    _write(tmp_path, "core", "KEBAB_LITERAL = {'core/config.py': ['config-unusable']}\n")
    with pytest.raises(ValueError, match=r"core\.py defines \['KEBAB_LITERAL'\]"):
        pins.read_package_pins(tmp_path)


def test_every_pin_file_is_named_for_the_package_of_the_modules_it_holds():
    """Over the real files, by the script's own definition of a package."""
    files = sorted(pins.PINS_DIRECTORY.glob("*.py"))
    assert len(files) > 10
    packages = {
        measure.package_of_path(path)
        for path in measure.python_files(pins.REPO_ROOT, measure.SOURCE)
    }
    assert {path.stem for path in files} <= packages


def test_the_merged_tables_are_the_ones_the_suite_imports():
    merged = pins.read_package_pins(pins.PINS_DIRECTORY)
    assert pins.PINNED_KEBAB_LITERALS_BY_MODULE == merged["KEBAB_LITERALS"]
    assert pins.PINNED_NAMED_WITHOUT_OWN == merged["NAMED_WITHOUT_OWN"]
    assert pins.PINNED_NAMED_WITH_OWN == merged["NAMED_WITH_OWN"]
    assert pins.PINNED_NAMED_WITH_INTEGER == frozenset(merged["NAMED_WITH_INTEGER"])
    assert pins.PINNED_LITERAL_HOLDERS == merged["LITERAL_HOLDERS"]
    assert pins.PINNED_LITERAL_HOLDERS_WITH_INTEGER == frozenset(
        merged["LITERAL_HOLDERS_WITH_INTEGER"]
    )
    assert len(pins.PINNED_KEBAB_LITERALS_BY_MODULE) > 200
