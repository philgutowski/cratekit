"""A listed core module answering for its parts, each loaded when first read (U331).

``cratekit.core.parts.answering`` is how ``core.jobs``, ``core.session``,
``core.tags`` and ``core.active_taxonomy`` answer for the core modules off the
named interface that a feature package reaches through them. Three things are held here: the
part is not imported with its module, a name is read off the part each time
so there is one binding, and every name in every table is one its part holds,
since a table is not checked when its module is imported.
"""

from __future__ import annotations

import importlib
import subprocess
import sys

import pytest

from cratekit.core import active_taxonomy, drift, jobs, parts, pool, session, snapshot, tags
from tests.test_import_rules import CORE_INTERFACE

#: The listed modules that answer for parts, read off the interface so a new one is held too.
ANSWERING = {
    name: module
    for name in CORE_INTERFACE
    if hasattr(
        vars(module := importlib.import_module(f"cratekit.core.{name}")).get("__getattr__"), "parts"
    )
}


@pytest.fixture
def package(tmp_path, monkeypatch):
    """A package of a home module answering for one part, importable and then forgotten."""
    root = tmp_path / "u331_parts"
    root.mkdir()
    (root / "__init__.py").write_text("")
    (root / "part.py").write_text("value = 1\nother = 2\n")
    (root / "home.py").write_text(
        "from cratekit.core import parts\n\nown = 0\n"
        '__getattr__ = parts.answering(__name__, {"part": ("value",)})\n'
    )
    (root / "renaming.py").write_text(
        "from cratekit.core import parts\n\n"
        '__getattr__ = parts.answering(__name__, {"part": {"PART_OTHER": "other"}})\n'
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    yield "u331_parts"
    for name in [name for name in sys.modules if name.split(".")[0] == "u331_parts"]:
        del sys.modules[name]


def test_a_part_is_imported_when_one_of_its_names_is_first_read_and_not_before(package):
    home = importlib.import_module(f"{package}.home")
    assert f"{package}.part" not in sys.modules
    assert home.own == 0
    assert f"{package}.part" not in sys.modules, "a name of the module's own loaded its part"
    assert home.value == 1
    assert f"{package}.part" in sys.modules


def test_a_name_is_read_off_the_part_each_time_so_there_is_one_binding(package):
    home = importlib.import_module(f"{package}.home")
    part = importlib.import_module(f"{package}.part")
    assert home.value == 1
    part.value = 7
    assert home.value == 7, "the module kept a copy of the name, which a patch on the part misses"
    assert "value" not in vars(home)


def test_a_name_the_table_does_not_hold_is_not_an_attribute_of_the_module(package):
    home = importlib.import_module(f"{package}.home")
    with pytest.raises(AttributeError, match=rf"module '{package}\.home' has no attribute 'other'"):
        home.other
    assert f"{package}.part" not in sys.modules, "an unknown name loaded the part to look"
    assert not hasattr(home, "missing")


def test_a_name_offered_under_another_is_read_off_the_part_by_the_name_it_holds(package):
    renaming = importlib.import_module(f"{package}.renaming")
    assert renaming.PART_OTHER == 2
    importlib.import_module(f"{package}.part").other = 9
    assert renaming.PART_OTHER == 9
    assert not hasattr(renaming, "other"), "the held name is offered beside the one it was given"


def test_the_table_is_kept_on_the_function_one_mapping_a_part():
    read = parts.answering(
        "cratekit.core.jobs", {"pool": ["plan_pool"], "cores": {"ceiling": "worker_ceiling"}}
    )
    assert read.parts == {
        "pool": {"plan_pool": "plan_pool"}, "cores": {"ceiling": "worker_ceiling"},
    }
    assert read("plan_pool") is pool.plan_pool


# ── The real modules ─────────────────────────────────────────────────────────


def test_the_listed_modules_that_answer_for_parts_are_the_four():
    """A reading that found none would pass every test below."""
    assert sorted(ANSWERING) == ["active_taxonomy", "jobs", "session", "tags"]


@pytest.mark.parametrize("listed", sorted(ANSWERING))
def test_every_name_a_listed_module_answers_for_is_held_by_its_part(listed):
    """A table is not read when its module is imported, so a misspelt name is found here."""
    module = ANSWERING[listed]
    table = vars(module)["__getattr__"].parts
    assert table, f"core.{listed} answers for no part"
    for part, names in table.items():
        assert part not in CORE_INTERFACE, f"core.{part} is listed, so nothing answers for it"
        held = importlib.import_module(f"cratekit.core.{part}")
        assert names, f"core.{listed} names core.{part} and none of its names"
        for offered, name in names.items():
            assert hasattr(held, name), f"core.{part} holds no {name}, which core.{listed} offers"
            assert getattr(module, offered) is getattr(held, name)


@pytest.mark.parametrize("listed", sorted(ANSWERING))
def test_no_listed_module_binds_a_name_its_table_answers_for(listed):
    """A name bound in the module too is found first, a second binding the part's patch misses."""
    module = ANSWERING[listed]
    answered = {name for names in vars(module)["__getattr__"].parts.values() for name in names}
    assert not answered & set(vars(module)), sorted(answered & set(vars(module)))
    assert len(answered) == sum(map(len, vars(module)["__getattr__"].parts.values()))


def test_a_patch_on_a_part_is_seen_through_the_module_that_answers_for_it(monkeypatch):
    """What the suites that patch ``pool`` and ``snapshot`` rely on, through the listed module."""
    monkeypatch.setattr(pool, "plan_pool", "a plan")
    monkeypatch.setattr(snapshot, "assert_room_for_check", "a measure")
    assert jobs.plan_pool == "a plan"
    assert session.assert_room_for_check == "a measure"
    monkeypatch.undo()
    assert jobs.plan_pool is pool.plan_pool
    assert tags.DRIFT_VARIABLE is drift.VARIABLE and tags.drift_reading is drift.reading
    assert active_taxonomy.alias is importlib.import_module("cratekit.core.taxonomy_word").alias


def test_importing_the_listed_modules_loads_none_of_their_parts_that_cost_a_command():
    """The reason the parts are read lazily: the pool's machinery is not every command's."""
    costly = ("pool", "discovery", "cores", "snapshot", "taxonomy_word", "drift")
    probe = (
        "import sys\n"
        "import cratekit.core.jobs, cratekit.core.session, cratekit.core.active_taxonomy\n"
        "import cratekit.core.tags\n"
        f"print(sorted(name for name in {costly!r} if 'cratekit.core.' + name in sys.modules))\n"
        "import cratekit.core.jobs as jobs\n"
        "jobs.plan_pool\n"
        "print('cratekit.core.pool' in sys.modules, 'concurrent.futures.process' in sys.modules)\n"
    )
    finished = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, check=True
    )
    assert finished.stdout.splitlines() == ["[]", "True True"], finished.stdout + finished.stderr
