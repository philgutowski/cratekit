"""Seams between packages, enforced as tests: the import rules (U296).

Point 4 of U290 asks that each feature module reach the core only through a
small named interface, and that toggling any module off leave nothing
dangling. ``tests/test_layering.py`` already holds the direction of imports;
this file holds how wide a package's reach may be. Four rules, each with an
allowance per importing package under ``tests/ratchets/imports/`` that only
ever shrinks:

1. **No private name crosses a package.** A name with a leading underscore
   belongs to the package that defines it.
2. **A feature package imports from core only the modules on the named
   interface**, the list below, at most 25 of them.
3. **An always on package never imports a toggleable package at module top
   level.** Under a function it may, since that import runs only when asked.
4. **With each toggle off in turn and its homes unimportable, every verb that
   remains still builds.** Read from source: a verb builds by importing its
   module and running its builder, so it dangles when what those load names a
   module in a home of the toggle that was switched off. Driving it for real
   costs more than the whole budget of these checks, so the suite reads it
   statically and ``scripts/refactor_measure.py imports --drive`` drives it
   for the audit; on the day this was written the two readings agreed on
   every toggle, 159 dangling verbs summed over them. An import made by a
   function the builder calls is not followed, and an import guarded by
   ``try`` is read as one that runs.

And one ceiling: the count of distinct core names feature packages use may
not grow.

AN ALLOWANCE LINE IS A CROSSING, NOT A COUNT OF ITS USES. One line per package
and name, however many files hold it, so a module that is split in two adds
no line, and a line whose crossing is gone fails nothing: one card's cleanup
cannot redden another card's package.

The lists live here, where the layer ladder's own lists live, and the script
reads them from this file as literals so there is one copy. The checkers are
pure functions over source text in ``scripts/refactor_measure.py``, the same
code the refactor's audit reads through. Fixture tests prove each rule bites
on synthetic sources before the one test that reads the tree.
"""

from __future__ import annotations

import collections
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core import profiles
from tests._refactor_measure import measure

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# The lists. Literals, because the script reads them without importing this.
# ---------------------------------------------------------------------------

#: The core modules a feature package may import: the named interface. These
#: are the 25 that three or more feature packages reached when U290's survey
#: measured them. The list is capped below and is not a place to park a reach:
#: a module joins only when it replaces one that leaves.
CORE_INTERFACE = (
    "active_taxonomy",
    "analysis_store",
    "backup_facts",
    "binaries",
    "cause",
    "config",
    "convergence",
    "exit_codes",
    "foreign_tree",
    "jobs",
    "locations",
    "naming",
    "preflight",
    "profiles",
    "provider_gate",
    "rb_writer",
    "review",
    "routing",
    "secrets",
    "session",
    "snapshot",
    "tags",
    "taxonomy",
    "tombstone",
    "tree_registry",
)
CORE_INTERFACE_LIMIT = 25

#: The modules and packages each toggle of ``core.profiles.MODULES`` owns: what
#: cannot be imported once it is off. A package holding any of them is
#: toggleable, and every other package is always on. Four toggles own nothing:
#: ``web`` and ``desktop`` are deferred, and the verbs ``identify`` and
#: ``repair`` gate live in always on packages.
TOGGLE_HOMES = {
    "analysis": ("cratekit.analysis",),
    "vocals": ("cratekit.vocals",),
    "favorites": ("cratekit.favorites",),
    "labels": ("cratekit.label",),
    "deletion": ("cratekit.deletion",),
    "web": (),
    "desktop": (),
    "identify": (),
    "repair": (),
    "duplicates": ("cratekit.modules.reports.duplicates",),
    "reports": ("cratekit.modules.reports",),
    "export": ("cratekit.export", "cratekit.modules.outbound"),
    "setbuilder": ("cratekit.setbuilder", "cratekit.modules.tools.setbuilder"),
    "mastering": ("cratekit.master", "cratekit.modules.tools.mastering"),
    "backup": ("cratekit.backup", "cratekit.modules.tools.backup"),
    "skills": ("cratekit.skills",),
}

#: The most distinct core names feature packages may use between them, 437 on
#: the commit U290's survey measured. It moves down only, and by the card that
#: lowers the count; ``refactor_measure.py imports --names`` lists the names,
#: so two runs of it say which one a failing branch added.
CORE_NAMES_CEILING = 437


# ---------------------------------------------------------------------------
# Fixtures: a package of synthetic modules
# ---------------------------------------------------------------------------


def _tree(**modules: str):
    """A tree from ``package__module=source`` pairs, an ``__init__`` for each package."""
    sources: dict[str, str] = {}
    for name, text in modules.items():
        path = "src/cratekit/" + name.replace("__", "/") + ".py"
        sources[path] = text
        parts = path.split("/")[2:-1]
        for depth in range(1, len(parts) + 1):
            sources.setdefault("src/cratekit/" + "/".join(parts[:depth]) + "/__init__.py", "")
    sources.setdefault("src/cratekit/__init__.py", "")
    return measure.Tree(sources)


def _lines(found: dict[str, collections.Counter[str]]) -> dict[str, list[str]]:
    return {package: sorted(lines.elements()) for package, lines in sorted(found.items())}


HOMES = {"labels": ("cratekit.label",), "export": ("cratekit.export",), "repair": ()}


# ═══════════════════════════════════════════════════════════════════════════
# Rule one: no private name crosses a package
# ═══════════════════════════════════════════════════════════════════════════


def test_a_private_name_imported_across_packages_fails():
    tree = _tree(
        core__config="def _exclusive_lock(): ...\n",
        sync__run="from cratekit.core.config import _exclusive_lock\n",
    )
    assert _lines(measure.private_crossings(tree)) == {
        "sync": ["private cratekit.core.config._exclusive_lock"]
    }


def test_the_same_private_import_inside_its_own_package_passes():
    tree = _tree(
        core__config="def _exclusive_lock(): ...\n",
        core__session="from cratekit.core.config import _exclusive_lock\n",
    )
    assert measure.private_crossings(tree) == {}


def test_a_lazy_private_import_across_packages_still_fails():
    tree = _tree(
        core__config="def _exclusive_lock(): ...\n",
        sync__run=(
            "def lock():\n"
            "    from cratekit.core.config import _exclusive_lock\n"
            "    return _exclusive_lock()\n"
        ),
    )
    assert _lines(measure.private_crossings(tree)) == {
        "sync": ["private cratekit.core.config._exclusive_lock"]
    }


def test_a_private_name_reached_through_an_imported_module_fails():
    """The import statement names a public module; the crossing is the attribute."""
    tree = _tree(
        write__trees="def _rollback_quietly(): ...\n",
        tagging__rows="from cratekit.write import trees\n\ntrees._rollback_quietly()\n",
    )
    assert _lines(measure.private_crossings(tree)) == {
        "tagging": ["private cratekit.write.trees._rollback_quietly"]
    }


def test_a_private_module_of_another_package_fails_and_a_dunder_does_not():
    tree = _tree(
        core___locks="def take(): ...\n",
        sync__run="from cratekit.core._locks import take\nfrom cratekit import __version__\n",
    )
    assert _lines(measure.private_crossings(tree)) == {
        "sync": ["private cratekit.core._locks.take"]
    }


def test_the_vendored_tree_is_not_a_private_crossing():
    tree = _tree(acquire__vendored="from cratekit._vendor.streamrip import client\n")
    assert measure.private_crossings(tree) == {}


def test_a_private_crossing_is_one_line_however_many_files_hold_it():
    """So splitting the module that holds it adds no line to the allowance."""
    source = "from cratekit.core.config import _mkdir_private\n"
    tree = _tree(core__config="def _mkdir_private(): ...\n", adopt__move=source, adopt__scan=source)
    assert _lines(measure.private_crossings(tree)) == {
        "adopt": ["private cratekit.core.config._mkdir_private"]
    }


def test_a_relative_import_is_resolved_and_cannot_hide_a_crossing():
    tree = _tree(
        core__config="def _exclusive_lock(): ...\n",
        sync__run="from ..core.config import _exclusive_lock\n",
    )
    assert _lines(measure.private_crossings(tree)) == {
        "sync": ["private cratekit.core.config._exclusive_lock"]
    }


def test_a_relative_import_in_a_package_initializer_starts_from_that_package():
    """One dot in ``sync/__init__.py`` is ``cratekit.sync``, not ``cratekit``."""
    sources = {
        "src/cratekit/__init__.py": "",
        "src/cratekit/core/__init__.py": "",
        "src/cratekit/core/config.py": "def _exclusive_lock(): ...\n",
        "src/cratekit/sync/__init__.py": (
            "from ..core.config import _exclusive_lock\nfrom .run import _go\n"
        ),
        "src/cratekit/sync/run.py": "def _go(): ...\n",
    }
    assert _lines(measure.private_crossings(measure.Tree(sources))) == {
        "sync": ["private cratekit.core.config._exclusive_lock"]
    }


def test_a_dotted_import_under_another_name_is_followed_to_its_module():
    tree = _tree(
        write__trees="def _rollback_quietly(): ...\n",
        tagging__rows="import cratekit.write.trees as writer\n\nwriter._rollback_quietly()\n",
        intake__land="import cratekit.write.trees\n\ncratekit.write.trees._rollback_quietly()\n",
    )
    assert _lines(measure.private_crossings(tree)) == {
        "intake": ["private cratekit.write.trees._rollback_quietly"],
        "tagging": ["private cratekit.write.trees._rollback_quietly"],
    }


# ═══════════════════════════════════════════════════════════════════════════
# Rule two: a feature package imports only the named interface of core
# ═══════════════════════════════════════════════════════════════════════════


def test_a_core_module_off_the_list_fails_from_a_feature_package():
    tree = _tree(
        core__config="",
        core__drift="def check(): ...\n",
        intake__landing="from cratekit.core import config\nfrom cratekit.core.drift import check\n",
    )
    assert _lines(measure.off_interface(tree, ["config"])) == {
        "intake": ["off-interface cratekit.core.drift"]
    }


def test_the_same_import_passes_from_core_write_and_the_shell():
    source = "from cratekit.core.drift import check\n"
    tree = _tree(
        core__drift="def check(): ...\n",
        core__session=source,
        write__trees=source,
        cli__doctor=source,
    )
    assert measure.off_interface(tree, ["config"]) == {}


def test_a_lazy_reach_off_the_list_still_fails():
    tree = _tree(
        core__pool="def size(): ...\n",
        analysis__run="def go():\n    from cratekit.core import pool\n    return pool.size()\n",
    )
    assert _lines(measure.off_interface(tree, ["config"])) == {
        "analysis": ["off-interface cratekit.core.pool"]
    }


def test_a_reach_under_type_checking_is_still_a_reach():
    tree = _tree(
        core__restore="class Plan: ...\n",
        session__cli=(
            "from typing import TYPE_CHECKING\n"
            "if TYPE_CHECKING:\n"
            "    from cratekit.core.restore import Plan\n"
        ),
    )
    assert _lines(measure.off_interface(tree, ["config"])) == {
        "session": ["off-interface cratekit.core.restore"]
    }


def test_a_module_on_the_list_passes_from_a_feature_package():
    tree = _tree(core__config="def load(): ...\n", intake__landing="from cratekit.core.config import load\n")
    assert measure.off_interface(tree, ["config"]) == {}


# ═══════════════════════════════════════════════════════════════════════════
# Rule three: an always on package never imports a toggleable one at top level
# ═══════════════════════════════════════════════════════════════════════════


def test_a_top_level_import_of_a_toggleable_package_fails_from_an_always_on_package():
    tree = _tree(
        label__registry="class Registry: ...\n",
        sync__run="from cratekit.label.registry import Registry\n",
    )
    assert _lines(measure.top_level_toggleable(tree, HOMES)) == {
        "sync": ["top-level cratekit.label.registry.Registry"]
    }


def test_the_same_import_under_a_function_passes():
    tree = _tree(
        label__registry="class Registry: ...\n",
        sync__run=(
            "def favourites():\n"
            "    from cratekit.label.registry import Registry\n"
            "    return Registry()\n"
        ),
    )
    assert measure.top_level_toggleable(tree, HOMES) == {}
    assert _lines(measure.top_level_toggleable(tree, HOMES, lazy=True)) == {
        "sync": ["top-level cratekit.label.registry.Registry"]
    }


def test_an_import_in_a_class_body_runs_at_import_time_and_fails():
    tree = _tree(
        label__registry="class Registry: ...\n",
        sync__run="class Pass:\n    from cratekit.label import registry\n",
    )
    assert _lines(measure.top_level_toggleable(tree, HOMES)) == {
        "sync": ["top-level cratekit.label.registry"]
    }


def test_an_import_under_type_checking_never_runs_and_passes():
    tree = _tree(
        label__registry="class Registry: ...\n",
        sync__run=(
            "from typing import TYPE_CHECKING\n"
            "if TYPE_CHECKING:\n"
            "    from cratekit.label.registry import Registry\n"
            "else:\n"
            "    from cratekit.label import registry\n"
        ),
    )
    assert _lines(measure.top_level_toggleable(tree, HOMES)) == {
        "sync": ["top-level cratekit.label.registry"]
    }


def test_type_checking_spelled_through_its_module_is_read_the_same():
    tree = _tree(
        label__registry="class Registry: ...\n",
        sync__run=(
            "import typing\n"
            "if typing.TYPE_CHECKING:\n"
            "    from cratekit.label.registry import Registry\n"
        ),
    )
    assert measure.top_level_toggleable(tree, HOMES) == {}


def test_a_toggleable_package_may_import_another_at_top_level_under_this_rule():
    """Rule three is about the always on packages. Rule four reads the rest."""
    tree = _tree(
        label__registry="class Registry: ...\n",
        export__cli="from cratekit.label.registry import Registry\n",
    )
    assert measure.top_level_toggleable(tree, HOMES) == {}


def test_each_imported_name_is_one_place():
    """The survey counted its 54 this way, so the reading does too."""
    tree = _tree(
        label__registry="A = B = 1\n",
        sync__run="from cratekit.label.registry import A, B\n",
        sync__pair="from cratekit.label.registry import A\n",
    )
    found = measure.top_level_toggleable(tree, HOMES)
    assert found["sync"] == collections.Counter(
        {"top-level cratekit.label.registry.A": 2, "top-level cratekit.label.registry.B": 1}
    )


# ═══════════════════════════════════════════════════════════════════════════
# Rule four: with a toggle off, every verb that remains still builds
# ═══════════════════════════════════════════════════════════════════════════


def _verb(name: str, module: str, toggle: str | None = None, builder: str = "build"):
    return measure.Verb(name=name, module=module, builder=builder, toggle=toggle)


def test_a_core_verb_whose_module_imports_a_toggled_off_package_dangles():
    tree = _tree(
        label__registry="",
        organize__cli="from cratekit.label import registry\n\ndef build(parser, entry): ...\n",
    )
    verbs = [_verb("organize", "cratekit.organize.cli")]
    (labels, export, repair) = measure.dangling(tree, verbs, HOMES)
    assert (labels.toggle, labels.verbs) == ("labels", ("organize",))
    assert labels.edges == (("cratekit.organize.cli", "cratekit.label.registry"),)
    assert export.verbs == () and repair.verbs == ()
    assert _lines(measure.dangling_lines(tree, [labels, export, repair])) == {
        "organize": ["dangling labels cratekit.label.registry"]
    }


def test_the_toggles_own_verbs_are_off_and_so_never_dangle():
    tree = _tree(label__cli="from cratekit.label import registry\n", label__registry="")
    verbs = [_verb("label.sweep", "cratekit.label.cli", toggle="labels")]
    assert [item.verbs for item in measure.dangling(tree, verbs, HOMES)] == [(), (), ()]


def test_a_verb_dangles_through_a_module_it_only_reaches_indirectly():
    """The import is filed under the package that holds it, not the verb's."""
    tree = _tree(
        label__registry="",
        intake__landing="from cratekit.label import registry\n",
        sync__cli="from cratekit.intake import landing\n\ndef build(parser, entry): ...\n",
    )
    found = measure.dangling(tree, [_verb("sync", "cratekit.sync.cli")], HOMES)
    assert found[0].verbs == ("sync",)
    assert _lines(measure.dangling_lines(tree, found)) == {
        "intake": ["dangling labels cratekit.label.registry"]
    }


def test_an_import_under_a_function_does_not_dangle_a_verb():
    tree = _tree(
        label__registry="",
        sync__cli=(
            "def build(parser, entry): ...\n"
            "def run(args):\n"
            "    from cratekit.label import registry\n"
        ),
    )
    found = measure.dangling(tree, [_verb("sync", "cratekit.sync.cli")], HOMES)
    assert [item.verbs for item in found] == [(), (), ()]


def test_an_import_written_in_the_builder_runs_when_the_verb_builds_and_dangles():
    """``intake.set`` is this shape on the tree: its builder imports the module
    whose own imports reach a toggleable package."""
    tree = _tree(
        label__registry="",
        intake__set_playlist="from cratekit.label import registry\n",
        intake__cli=(
            "def build_set(parser, entry):\n"
            "    from cratekit.intake import set_playlist\n"
            "def build_other(parser, entry): ...\n"
        ),
    )
    verbs = [
        _verb("intake.set", "cratekit.intake.cli", builder="build_set"),
        _verb("intake.other", "cratekit.intake.cli", builder="build_other"),
    ]
    found = measure.dangling(tree, verbs, HOMES)
    assert found[0].verbs == ("intake.set",)


def test_a_home_imported_directly_in_the_builder_dangles_the_verb():
    tree = _tree(
        label__registry="",
        sync__cli="def build(parser, entry):\n    from cratekit.label import registry\n",
    )
    found = measure.dangling(tree, [_verb("sync", "cratekit.sync.cli")], HOMES)
    assert found[0].verbs == ("sync",)
    assert found[0].edges == (("cratekit.sync.cli", "cratekit.label.registry"),)


def test_an_import_under_type_checking_is_never_loaded_for_a_verb():
    """Neither at the top of a module nor in its builder."""
    guarded = "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from cratekit.label import registry\n"
    tree = _tree(
        label__registry="",
        sync__cli=guarded + "def build(parser, entry): ...\n",
        intake__cli=(
            "from typing import TYPE_CHECKING\n"
            "def build(parser, entry):\n"
            "    if TYPE_CHECKING:\n"
            "        from cratekit.label import registry\n"
        ),
    )
    verbs = [_verb("sync", "cratekit.sync.cli"), _verb("intake", "cratekit.intake.cli")]
    assert [item.verbs for item in measure.dangling(tree, verbs, HOMES)] == [(), (), ()]


def test_an_import_guarded_by_try_is_read_as_one_that_runs():
    """A known limit, pinned so it is changed on purpose: the driven reading
    builds this verb, and the static one calls it dangling."""
    tree = _tree(
        label__registry="",
        sync__cli=(
            "try:\n"
            "    from cratekit.label import registry\n"
            "except ImportError:\n"
            "    registry = None\n"
            "def build(parser, entry): ...\n"
        ),
    )
    found = measure.dangling(tree, [_verb("sync", "cratekit.sync.cli")], HOMES)
    assert found[0].verbs == ("sync",)


def test_a_verb_the_registry_loads_from_inside_a_home_it_is_not_gated_by_dangles():
    tree = _tree(label__cli="def build(parser, entry): ...\n")
    found = measure.dangling(tree, [_verb("label.heard", "cratekit.label.cli")], HOMES)
    assert found[0].verbs == ("label.heard",)
    assert found[0].edges == ((measure.REGISTRY_LOADS, "cratekit.label.cli"),)
    assert _lines(measure.dangling_lines(tree, found)) == {
        "label": ["dangling labels cratekit.label.cli"]
    }


def test_a_package_initializer_is_loaded_with_any_module_inside_it():
    """Importing ``cratekit.sync.cli`` runs ``cratekit/sync/__init__.py`` first."""
    sources = {
        "src/cratekit/__init__.py": "",
        "src/cratekit/label/__init__.py": "",
        "src/cratekit/label/registry.py": "",
        "src/cratekit/sync/__init__.py": "from cratekit.label import registry\n",
        "src/cratekit/sync/cli.py": "def build(parser, entry): ...\n",
    }
    found = measure.dangling(measure.Tree(sources), [_verb("sync", "cratekit.sync.cli")], HOMES)
    assert found[0].verbs == ("sync",)
    assert found[0].edges == (("cratekit.sync", "cratekit.label.registry"),)


def test_nothing_is_followed_through_a_module_that_cannot_be_imported():
    """An import past the switched off package never runs, so it is no cause.

    ``sync`` loads ``label`` and ``label`` loads ``export``. With ``export``
    off, ``label`` is still there and its import of ``export`` dangles the
    verb. With ``labels`` off the import of ``label`` is where it stops, and
    ``label``'s own import of ``export`` is never reached.
    """
    tree = _tree(
        export__cli="",
        label__registry="from cratekit.export import cli\n",
        sync__cli="from cratekit.label import registry\n\ndef build(parser, entry): ...\n",
    )
    labels, export, _ = measure.dangling(tree, [_verb("sync", "cratekit.sync.cli")], HOMES)
    assert labels.edges == (("cratekit.sync.cli", "cratekit.label.registry"),)
    assert export.edges == (("cratekit.label.registry", "cratekit.export.cli"),)


# ═══════════════════════════════════════════════════════════════════════════
# The count of core names
# ═══════════════════════════════════════════════════════════════════════════


def test_core_names_are_counted_across_feature_packages_and_only_there():
    tree = _tree(
        core__config="def load(): ...\ndef save(): ...\nlocate = load\n",
        core__jobs="from cratekit.core.config import save\n",
        cli__doctor="from cratekit.core.config import save\n",
        intake__landing="from cratekit.core.config import load\n",
        sync__run="from cratekit.core import config\n\nconfig.load()\nconfig.locate()\n",
    )
    assert measure.core_names(tree) == {
        "intake": {"cratekit.core.config.load"},
        "sync": {"cratekit.core.config.load", "cratekit.core.config.locate"},
    }


def test_a_name_imported_from_the_core_package_itself_is_a_core_name():
    sources = {
        "src/cratekit/__init__.py": "",
        "src/cratekit/core/__init__.py": "VERSION = 1\n",
        "src/cratekit/sync/__init__.py": "",
        "src/cratekit/sync/run.py": "from cratekit.core import VERSION\n",
    }
    assert measure.core_names(measure.Tree(sources)) == {"sync": {"cratekit.core.VERSION"}}


def test_a_name_bound_in_an_except_branch_is_a_name_the_module_defines():
    tree = _tree(
        core__config=(
            "try:\n    import tomllib\nexcept ImportError:\n    def fallback(): ...\n"
        ),
        sync__run="from cratekit.core import config\n\nconfig.fallback()\nconfig.tomllib\n",
    )
    assert measure.core_names(tree) == {
        "sync": {"cratekit.core.config.fallback", "cratekit.core.config.tomllib"}
    }


def test_a_local_variable_named_as_an_imported_module_is_not_a_use_of_it():
    """The tree's own case: ``source.name`` beside an imported module ``source``.

    A module's alias is followed anywhere in the file, so what keeps a local
    variable's attributes out of the count, and out of the private rule, is
    that the module does not define them.
    """
    tree = _tree(
        core__config="def load(): ...\n",
        sync__run=(
            "from cratekit.core import config\n\n"
            "def run(config):\n"
            "    return config.library, config._cache, config.load\n"
        ),
    )
    assert measure.core_names(tree) == {"sync": {"cratekit.core.config.load"}}
    assert measure.private_crossings(tree) == {}


def test_a_module_that_answers_for_any_name_has_every_attribute_counted():
    """A ``__getattr__`` or a star import means the listed names are not all of them."""
    tree = _tree(
        core__config="def __getattr__(name): ...\n",
        core__naming="from os.path import *\n",
        sync__run=(
            "from cratekit.core import config, naming\n\n"
            "config.anything()\nnaming.join()\n"
        ),
    )
    assert measure.core_names(tree) == {
        "sync": {"cratekit.core.config.anything", "cratekit.core.naming.join"}
    }


# ═══════════════════════════════════════════════════════════════════════════
# The lists and the readings they depend on
# ═══════════════════════════════════════════════════════════════════════════


def test_the_interface_is_at_most_25_core_modules_sorted_and_real():
    assert len(CORE_INTERFACE) <= CORE_INTERFACE_LIMIT == 25
    assert list(CORE_INTERFACE) == sorted(set(CORE_INTERFACE))
    core = REPO_ROOT / measure.SOURCE / "core"
    missing = [name for name in CORE_INTERFACE if not (core / f"{name}.py").is_file()]
    assert not missing, f"the interface names core modules that do not exist: {missing}"


def test_every_toggle_has_its_homes_declared_and_every_home_exists():
    """A toggle added to ``core.profiles.MODULES`` must say here what it owns.

    Otherwise rule four reads it as owning nothing and its verbs' package as
    always on, which is the quiet way for a new module to be born unguarded.
    """
    assert tuple(TOGGLE_HOMES) == profiles.MODULES
    source = REPO_ROOT / "src"
    for toggle, owned in TOGGLE_HOMES.items():
        for home in owned:
            path = source / home.replace(".", "/")
            assert path.is_dir() or path.with_suffix(".py").is_file(), (
                f"{toggle} owns {home}, which is neither a package nor a module"
            )


def test_the_script_reads_these_lists_from_this_file():
    rules = measure.rules_from((REPO_ROOT / measure.IMPORT_RULES_TEST).read_text(encoding="utf-8"))
    assert Path(__file__).resolve() == REPO_ROOT / measure.IMPORT_RULES_TEST
    assert rules.interface == CORE_INTERFACE
    assert rules.homes == TOGGLE_HOMES
    assert rules.names_ceiling == CORE_NAMES_CEILING


def test_the_script_reads_the_registry_as_the_package_declares_it():
    """The script cannot import the registry, so its reading of the text is held to it."""
    read = measure.verbs_from((REPO_ROOT / measure.REGISTRY).read_text(encoding="utf-8"))
    live = [
        measure.Verb(entry.name, entry.module, entry.builder, entry.module_id)
        for entry in registry.landed_entries()
    ]
    assert len(live) > 50
    assert read == live


def test_a_registry_entry_the_script_cannot_read_is_refused_not_skipped():
    source = 'ENTRIES = (Entry(name="a.b", module=make_module(), builder="build"),)\n'
    with pytest.raises(ValueError, match="'a.b' gives module"):
        measure.verbs_from(source)
    with pytest.raises(ValueError, match="'a.c' does not give builder"):
        measure.verbs_from('ENTRIES = (Entry(name="a.c", module="cratekit.a.cli"),)\n')


def test_a_planned_entry_is_not_a_landed_verb():
    source = (
        'UNIT = "U99"\n'
        "ENTRIES = (\n"
        '    Entry(name="a", module="cratekit.a.cli", builder="build", module_id="labels"),\n'
        '    Entry(name="b", module="cratekit.b.cli", builder="build", planned_in=UNIT),\n'
        ")\n"
    )
    assert measure.verbs_from(source) == [
        measure.Verb("a", "cratekit.a.cli", "build", "labels")
    ]


# ═══════════════════════════════════════════════════════════════════════════
# The real package
# ═══════════════════════════════════════════════════════════════════════════


def test_no_package_crosses_a_seam_beyond_its_allowance():
    """All four rules and the ceiling over one reading of the tree.

    One test, because the reading parses every module and four tests would
    parse the package four times.
    """
    sources = measure.read_sources(REPO_ROOT, [measure.SOURCE])
    tree = measure.Tree(sources)
    rules = measure.Rules(CORE_INTERFACE, TOGGLE_HOMES, CORE_NAMES_CEILING)
    verbs = [
        measure.Verb(entry.name, entry.module, entry.builder, entry.module_id)
        for entry in registry.landed_entries()
    ]
    # A reading that read nothing would pass, so the reading is checked first.
    assert len(sources) > 100 and sum(map(len, tree.uses.values())) > 1_000
    assert all(verb.module in tree.modules for verb in verbs), "a verb names no module"

    allowed = measure.read_allowances(REPO_ROOT, measure.IMPORT_ALLOWANCES)
    excess = measure.over_allowance(measure.import_findings(tree, rules, verbs), allowed)
    problems = [
        f"{package}: {line}"
        for package, lines in sorted(excess.items())
        for line in sorted(lines)
    ]
    assert not problems, (
        "a package crossed a seam it had not crossed before. `private`: use a public "
        "name, or give the name one public home. `off-interface`: reach core through "
        "a module on CORE_INTERFACE. `top-level`: import it inside the function that "
        "needs it. `dangling`: that import stops a verb building with the toggle "
        f"off. The allowance under {measure.IMPORT_ALLOWANCES}/ is never added to:\n"
        + "\n".join(problems)
    )

    used = measure.core_names(tree)
    names = {name for group in used.values() for name in group}
    assert len(names) <= CORE_NAMES_CEILING, (
        f"feature packages now use {len(names)} distinct core names, over the ceiling "
        f"of {CORE_NAMES_CEILING}. `scripts/refactor_measure.py imports --names` on "
        "main and on this branch lists both sets; use a name already there."
    )
