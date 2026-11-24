"""Seams between packages, enforced as tests: the import rules (U296).

U290 point 4: each feature module reaches the core only through a small named
interface, and toggling a module off leaves nothing dangling.
``tests/test_layering.py`` holds import direction; this holds reach. Four
rules, each with a per package allowance under ``tests/ratchets/imports/``
that only shrinks:

1. **No private name crosses a package.**
2. **A feature package imports from core only the named interface** below.
   A listed module answers for the names it defines and the names it
   re-exports from a core module off the list, each one a counted core name.
   A module it imports at its top level is not one of them: reached as an
   attribute of the listed module, or imported from it, it is read as a reach
   of that module itself as well (U331). A module bound some other way is
   not followed.
3. **An always on package never imports a toggleable one at module top
   level**; under a function it may.
4. **With each toggle off, every remaining verb still builds**, read
   statically from what each verb's module and builder import (the drive in
   ``scripts/refactor_measure.py imports --drive`` agreed on every toggle).
   An import in a function the builder calls is not followed; one guarded by
   ``try`` counts as run.

And one ceiling: the count of distinct core names feature packages use may
not grow. An allowance line is one crossing per package and name, so a split
module adds no line, and since U331 every allowance is empty and a line put
back fails. The script reads the lists below as literals.
"""

from __future__ import annotations

import collections
import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core import profiles
from tests._refactor_measure import measure

REPO_ROOT = Path(__file__).resolve().parent.parent

# ── The lists. Literals, because the script reads them without importing this. ───

#: The core modules a feature package may import: the named interface. Twenty one are among
#: the 25 that three or more feature packages reached in U290's survey. The list is capped
#: below and is no place to park a reach: a module joins only when one leaves.
#:
#: U331 MADE FOUR SWAPS, each for a module a feature package must import itself: ``art``
#: needs ``tags`` at import and borrows the two private container helpers the beat grid rule
#: depends on; ``pool`` is the module the sizing guards of ``tests/test_pool_sizing.py`` are
#: keyed on, and loads the process pool's machinery; ``restore`` imports ``session``, the
#: module that would have to answer for it, and ``taxonomy_word`` imports the upgrade and
#: ``routing``, which ``active_taxonomy`` answering for it would load with every importer (a
#: cycle, until the upgrade read the loader where it calls it). The four that left are each
#: re-exported by a listed module that loads what it needs already: ``profiles`` by
#: ``config``, ``preflight`` and ``snapshot`` by ``session``, and ``foreign_tree`` by
#: ``active_taxonomy``, which has the taxonomy loaded where ``tree_registry`` would load it
#: for the restore; so every module importing ``active_taxonomy`` at its top loads the foreign
#: tree too, which is why the doctor's two readers import it where they call it (U331's merge
#: of U343 put the doctor's help at its ceiling). ``session`` answers for ``processes`` the
#: same way, ``jobs`` for ``discovery``, and ``pool`` for the cores' ceiling, so a spawned
#: worker loads nothing more for it.
#:
#: A RE-EXPORT IS NEVER FREE, which is why the list is not emptied into it: the listed module
#: imports the other with every command that imports it, a guard that follows imports follows
#: it there, and a test that patches the name patches it where the caller reads it. Loading
#: it on demand instead hides it from those guards (``tests/modules/test_reports.py`` refuses
#: a computed import), so it is not done.
CORE_INTERFACE = (
    "active_taxonomy", "analysis_store", "art", "backup_facts", "binaries", "cause", "config",
    "convergence", "exit_codes", "jobs", "locations", "naming", "pool", "provider_gate",
    "rb_writer", "restore", "review", "routing", "secrets", "session", "tags", "taxonomy",
    "taxonomy_word", "tombstone", "tree_registry",
)
CORE_INTERFACE_LIMIT = 25

#: The modules and packages each toggle of ``core.profiles.MODULES`` owns. A package holding
#: any is toggleable, every other always on. ``web`` and ``desktop`` are deferred, and
#: ``identify`` and ``repair`` gate verbs in always on packages, so those four own nothing.
#:
#: A HOME NEVER HOLDS WHAT BUILDS A VERB ITS TOGGLE DOES NOT GATE (U331), which rule four
#: fails; a verb a toggle gates may still be built outside any home, as ``label.sync`` is in
#: the shell. ``favorites`` gates one verb, ``sync.favorites`` in ``favorites/cli.py``; the
#: rest of that package builds four verbs no toggle gates and the landing, so the toggle owns
#: the module, as ``duplicates`` owns one module of ``reports``. ``export`` gates the verbs of
#: ``cratekit.export``; the outbound package under ``modules`` is what the favourites sweep is
#: built on too, and what organize, sync, label and intake call, so no toggle owns it, and
#: rules three and four no longer read it.
TOGGLE_HOMES = {
    "analysis": ("cratekit.analysis",),
    "vocals": ("cratekit.vocals",),
    "favorites": ("cratekit.favorites.cli",),
    "labels": ("cratekit.label",),
    "deletion": ("cratekit.deletion",),
    "web": (),
    "desktop": (),
    "identify": (),
    "repair": (),
    "duplicates": ("cratekit.modules.reports.duplicates",),
    "reports": ("cratekit.modules.reports",),
    "export": ("cratekit.export",),
    "setbuilder": ("cratekit.setbuilder", "cratekit.modules.tools.setbuilder"),
    "mastering": ("cratekit.master", "cratekit.modules.tools.mastering"),
    "backup": ("cratekit.backup", "cratekit.modules.tools.backup"),
    "skills": ("cratekit.skills",),
}

#: The most distinct core names feature packages may use between them: 437 on the commit
#: U290's survey measured, and 446 on the day this check landed, U292 having added nine for
#: the taxonomy word edits its backlog plans while this was built. It moves down only, and by
#: the card that lowers the count; ``refactor_measure.py imports --names`` lists the names, so
#: two runs of it say which one a failing branch added.
#:
#: ONE CARD RAISED IT, U298, by the coordinator's call on R-1746, and that call is no rule for
#: any other card. U298 gave every helper the packages had each written one home, and a home
#: in core that a feature package calls is a name. It added thirteen and freed seven, so the
#: ceiling rose by six:
#:
#:   added   backup_facts.took, config.RemediedError, config.held, config.lock_within,
#:           config.read_bytes_if_present, config.read_json, config.read_json_as_text,
#:           config.read_json_map, jobs.Artifacts, jobs.advance, jobs.reported,
#:           jobs.resumed, preflight.device_of
#:   freed   artifacts.Location, artifacts.committed, artifacts.produced, naming.MarkerRule,
#:           session.attach_capture, snapshot.assert_verified, snapshot.capture
#:
#: The three private names it made public (config.exclusive_lock, config.mkdir_private,
#: preflight.names_one_path) each replaced the private spelling of itself and moved nothing.
#:
#: 2026-11-23, U342, by the coordinator's call for #994, raised by one for naming.stamp_head,
#: which analyze adopt calls to give a title with no head one: the naming engine is the one
#: place a head is rendered, and building it in a feature package would undo what the
#: refactor is for. U331 (#980) counts it as an interface name.
#:
#: U331 lowered it from 453 to 432, the count measured once every reach went through the
#: list: a name re-exported by a listed module replaced the one it stood for,
#: ``Config.membership()`` replaced ``profiles.resolve``, and the names of the modules that
#: moved to the feature that used them (``held_plan`` to sync, ``rehearsal`` and ``drift`` to
#: intake) are core names no longer.
CORE_NAMES_CEILING = 432


# ── Fixtures: a package of synthetic modules ─────────────────────────────────


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


def _private(tree) -> dict[str, list[str]]:
    return _lines(measure.private_crossings(tree))


def _off(tree, *listed: str) -> dict[str, list[str]]:
    return _lines(measure.off_interface(tree, list(listed) or ["config"]))


def _top(tree, **reading) -> dict[str, list[str]]:
    return _lines(measure.top_level_toggleable(tree, HOMES, **reading))


LOCK = "def _exclusive_lock(): ...\n"
IMPORT_LOCK = "from cratekit.core.config import _exclusive_lock\n"
LOCK_CROSSING = {"sync": ["private cratekit.core.config._exclusive_lock"]}
ROLLBACK = "def _rollback_quietly(): ...\n"
ROLLED = "_rollback_quietly()\n"
REGISTRY = "class Registry: ...\n"


# ── Rule one: no private name crosses a package ──────────────────────────────


@pytest.mark.parametrize(
    "modules, expected",
    [
        pytest.param({"core__config": LOCK, "sync__run": IMPORT_LOCK}, LOCK_CROSSING, id="direct"),
        pytest.param(
            {
                "core__config": LOCK,
                "sync__run": (
                    "def lock():\n"
                    "    from cratekit.core.config import _exclusive_lock\n"
                    "    return _exclusive_lock()\n"
                ),
            },
            LOCK_CROSSING, id="a-lazy-import-still-fails"),
        pytest.param(
            {"core__config": LOCK, "sync__run": "from ..core.config import _exclusive_lock\n"},
            LOCK_CROSSING, id="a-relative-import-is-resolved-and-cannot-hide-it"),
        # The import statement names a public module; the crossing is the attribute.
        pytest.param(
            {
                "write__trees": ROLLBACK,
                "tagging__rows": "from cratekit.write import trees\n\ntrees._rollback_quietly()\n",
            },
            {"tagging": ["private cratekit.write.trees._rollback_quietly"]},
            id="reached-through-an-imported-module"),
        pytest.param(
            {
                "core___locks": "def take(): ...\n",
                "sync__run": (
                    "from cratekit.core._locks import take\nfrom cratekit import __version__\n"
                ),
            },
            {"sync": ["private cratekit.core._locks.take"]},
            id="a-private-module-of-another-package-and-a-dunder-does-not"),
        pytest.param(
            {
                "write__trees": ROLLBACK,
                "tagging__rows": "import cratekit.write.trees as writer\n\nwriter." + ROLLED,
                "intake__land": "import cratekit.write.trees\n\ncratekit.write.trees." + ROLLED,
            },
            {
                "intake": ["private cratekit.write.trees._rollback_quietly"],
                "tagging": ["private cratekit.write.trees._rollback_quietly"],
            },
            id="a-dotted-import-under-another-name-is-followed-to-its-module"),
        pytest.param(
            {
                "core__art": "def _open(): ...\n",
                "core__tags": "from cratekit.core import art\n",
                "tagging__tag": "from cratekit.core import tags\n\ntags.art._open()\n",
            },
            {"tagging": ["private cratekit.core.art._open"]},
            id="a-name-of-a-module-handed-over"),
    ])
def test_a_private_name_crossing_a_package_fails_by_each_listed_reach(modules, expected):
    assert _private(_tree(**modules)) == expected


@pytest.mark.parametrize(
    "modules",
    [
        pytest.param({"core__config": LOCK, "core__session": IMPORT_LOCK}, id="its-own-package"),
        pytest.param(
            {"acquire__vendored": "from cratekit._vendor.streamrip import client\n"},
            id="the-vendored-tree"),
    ])
def test_a_private_import_that_crosses_no_package_passes(modules):
    assert measure.private_crossings(_tree(**modules)) == {}


def test_a_private_crossing_is_one_line_however_many_files_hold_it():
    """So splitting the module that holds it adds no line to the allowance."""
    source = "from cratekit.core.config import _mkdir_private\n"
    tree = _tree(core__config="def _mkdir_private(): ...\n", adopt__move=source, adopt__scan=source)
    assert _private(tree) == {"adopt": ["private cratekit.core.config._mkdir_private"]}


def test_a_relative_import_in_a_package_initializer_starts_from_that_package():
    """One dot in ``sync/__init__.py`` is ``cratekit.sync``, not ``cratekit``."""
    sources = {
        "src/cratekit/__init__.py": "",
        "src/cratekit/core/__init__.py": "",
        "src/cratekit/core/config.py": LOCK,
        "src/cratekit/sync/__init__.py": "from ..core.config import _exclusive_lock\n"
        "from .run import _go\n",
        "src/cratekit/sync/run.py": "def _go(): ...\n",
    }
    assert _private(measure.Tree(sources)) == LOCK_CROSSING


# ── Rule two: a feature package imports only the named interface of core ─────


@pytest.mark.parametrize(
    "modules, expected",
    [
        pytest.param(
            {
                "core__config": "",
                "core__drift": "def check(): ...\n",
                "intake__landing": (
                    "from cratekit.core import config\nfrom cratekit.core.drift import check\n"
                ),
            },
            {"intake": ["off-interface cratekit.core.drift"]},
            id="imported"),
        pytest.param(
            {
                "core__pool": "def size(): ...\n",
                "analysis__run": (
                    "def go():\n    from cratekit.core import pool\n    return pool.size()\n"
                ),
            },
            {"analysis": ["off-interface cratekit.core.pool"]},
            id="a-lazy-reach-still-fails"),
        pytest.param(
            {
                "core__restore": "class Plan: ...\n",
                "session__cli": (
                    "from typing import TYPE_CHECKING\n"
                    "if TYPE_CHECKING:\n"
                    "    from cratekit.core.restore import Plan\n"
                ),
            },
            {"session": ["off-interface cratekit.core.restore"]},
            id="a-reach-under-type-checking-is-still-a-reach"),
    ])
def test_a_core_module_off_the_list_fails_from_a_feature_package(modules, expected):
    assert _off(_tree(**modules)) == expected


def test_the_same_import_passes_from_core_write_and_the_shell():
    source = "from cratekit.core.drift import check\n"
    tree = _tree(
        core__drift="def check(): ...\n", core__session=source, write__trees=source,
        cli__doctor=source)
    assert measure.off_interface(tree, ["config"]) == {}


def test_a_module_on_the_list_passes_from_a_feature_package():
    tree = _tree(core__config="def load(): ...\n", intake__landing="from cratekit.core.config import load\n")
    assert measure.off_interface(tree, ["config"]) == {}


def test_a_name_a_listed_module_re_exports_is_reached_through_the_list():
    """How a part is reached: the listed module answers for the name, and it is counted."""
    tree = _tree(
        core__pool="def plan_pool(): ...\n",
        core__jobs="from cratekit.core.pool import plan_pool as plan_pool\n",
        analysis__light=(
            "from cratekit.core import jobs\nfrom cratekit.core.jobs import plan_pool\n\n"
            "jobs.plan_pool()\n"
        ))
    assert measure.off_interface(tree, ["jobs"]) == {}
    assert measure.core_names(tree) == {"analysis": {"cratekit.core.jobs.plan_pool"}}


def test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module():
    """Or eleven modules could hide behind eleven counted names of the list."""
    tree = _tree(
        core__art="def read(): ...\ndef write(): ...\n",
        core__tags="from cratekit.core import art\n",
        tagging__tag="from cratekit.core import tags\n\ntags.art.read()\n",
        tagging__summary="from cratekit.core.tags import art as pictures\n\npictures.write()\n",
        sync__run="from cratekit.core import tags\n\nkept = tags.art\n")
    assert _off(tree, "tags") == {
        "sync": ["off-interface cratekit.core.art"], "tagging": ["off-interface cratekit.core.art"]
    }
    # The name of ``tags`` that was written is counted too, beside what was read through it.
    assert measure.core_names(tree) == {
        "sync": {"cratekit.core.tags.art"},
        "tagging": {"cratekit.core.art.read", "cratekit.core.art.write", "cratekit.core.tags.art"},
    }
    assert measure.off_interface(tree, ["art", "tags"]) == {}


def test_a_module_handed_over_twice_is_followed_to_the_module_it_is():
    """A chain of any length ends at a module and a name in it, never at a name of the first."""
    tree = _tree(
        core__codec="def decode(): ...\n",
        core__art="from cratekit.core import codec\n",
        core__tags="import cratekit.core.art\nfrom cratekit.core import art\n",
        tagging__tag=(
            "from cratekit.core import tags\n\ntags.art.codec.decode()\n"
            "tags.cratekit.core.codec.decode()\n"
        ),
        tagging__rows="from cratekit.core.tags import art\n\nart.codec.decode()\n")
    assert _off(tree, "tags") == {
        "tagging": ["off-interface cratekit.core.art", "off-interface cratekit.core.codec"]
    }
    assert measure.core_names(tree) == {
        "tagging": {
            "cratekit.core.codec.decode", "cratekit.core.tags.art", "cratekit.core.tags.cratekit",
        }
    }


def test_a_module_passed_on_by_name_through_a_third_module_is_followed_to_it():
    """``tags`` took ``art`` from ``pictures``, which imported it: still ``core.art``."""
    tree = _tree(
        core__art="def read(): ...\n", core__pictures="from cratekit.core import art\n",
        core__tags="from cratekit.core.pictures import art as covers\n",
        tagging__tag="from cratekit.core import tags\n\ntags.covers.read()\n",
        tagging__rows="from cratekit.core.tags import covers\n\ncovers.read()\n")
    assert _off(tree, "tags") == {"tagging": ["off-interface cratekit.core.art"]}
    assert "cratekit.core.art.read" in measure.core_names(tree)["tagging"]


def test_the_module_an_import_names_is_still_reached_when_the_name_is_a_module():
    """Following the name adds a reach and takes none away: each rule still reads the
    module the statement names, as it did before the follow."""
    tree = _tree(
        core__cause="", core__preflight="from cratekit.core import cause\n",
        core___hidden="from cratekit.core import cause\n",
        label__registry="from cratekit.core import cause\n",
        intake__landing="from cratekit.core.preflight import cause\n",
        sync__run="from cratekit.label.registry import cause\n",
        adopt__move="from cratekit.core._hidden import cause\n")
    assert _off(tree, "cause") == {
        "adopt": ["off-interface cratekit.core._hidden"],
        "intake": ["off-interface cratekit.core.preflight"],
    }
    assert _top(tree) == {"sync": ["top-level cratekit.label.registry.cause"]}
    assert _private(tree) == {"adopt": ["private cratekit.core._hidden.cause"]}


def test_a_function_that_imports_its_module_when_called_is_not_that_module():
    """``session_call_time.session`` is the tree's own case: the import is inside the
    function, so the name on the module is the function and nothing is handed over."""
    tree = _tree(
        core__session="def lock(): ...\n",
        core__session_call_time=(
            "def session():\n    from cratekit.core import session\n    return session\n"
        ),
        core__session_ack="from cratekit.core.session_call_time import session as _session\n",
        core__tags="def cover():\n    from cratekit.core import art\n    return art\n",
        core__art="def read(): ...\n",
        tagging__tag="from cratekit.core import tags\n\ntags.art.read()\n")
    assert tree.loads["cratekit.core.session_ack"] == frozenset({"cratekit.core.session_call_time"})
    assert measure.off_interface(tree, ["tags"]) == {}


def test_a_toggleable_module_handed_over_at_top_level_is_a_top_level_import():
    """Rule three reads the module a name is, not the always on module that passed it on."""
    tree = _tree(
        label__registry=REGISTRY, intake__landing="from cratekit.label import registry\n",
        sync__run="from cratekit.intake.landing import registry\n")
    assert _top(tree)["sync"] == ["top-level cratekit.label.registry"]


# ── Rule three: an always on package never imports a toggleable one at top level ───


@pytest.mark.parametrize(
    "modules, expected",
    [
        pytest.param(
            {"sync__run": "from cratekit.label.registry import Registry\n"},
            {"sync": ["top-level cratekit.label.registry.Registry"]},
            id="at-top-level-from-an-always-on-package-fails"),
        pytest.param(
            {"sync__run": "class Pass:\n    from cratekit.label import registry\n"},
            {"sync": ["top-level cratekit.label.registry"]},
            id="in-a-class-body-runs-at-import-time-and-fails"),
        pytest.param(
            {
                "sync__run": (
                    "from typing import TYPE_CHECKING\n"
                    "if TYPE_CHECKING:\n"
                    "    from cratekit.label.registry import Registry\n"
                    "else:\n"
                    "    from cratekit.label import registry\n"
                ),
            },
            {"sync": ["top-level cratekit.label.registry"]},
            id="under-type-checking-never-runs-and-passes"),
        pytest.param(
            {
                "sync__run": (
                    "import typing\n"
                    "if typing.TYPE_CHECKING:\n"
                    "    from cratekit.label.registry import Registry\n"
                ),
            },
            {},
            id="type-checking-spelled-through-its-module-is-read-the-same"),
        # Rule three is about the always on packages. Rule four reads the rest.
        pytest.param(
            {"export__cli": "from cratekit.label.registry import Registry\n"}, {},
            id="a-toggleable-package-may-import-another"),
    ])
def test_an_import_of_a_toggleable_package_is_read_by_when_it_runs(modules, expected):
    assert _top(_tree(label__registry=REGISTRY, **modules)) == expected


def test_the_same_import_under_a_function_passes():
    tree = _tree(
        label__registry=REGISTRY,
        sync__run=(
            "def favourites():\n"
            "    from cratekit.label.registry import Registry\n"
            "    return Registry()\n"
        ))
    assert measure.top_level_toggleable(tree, HOMES) == {}
    assert _top(tree, lazy=True) == {"sync": ["top-level cratekit.label.registry.Registry"]}


def test_each_imported_name_is_one_place():
    """The survey counted its 54 this way, so the reading does too."""
    tree = _tree(
        label__registry="A = B = 1\n", sync__run="from cratekit.label.registry import A, B\n",
        sync__pair="from cratekit.label.registry import A\n")
    found = measure.top_level_toggleable(tree, HOMES)
    assert found["sync"] == collections.Counter(
        {"top-level cratekit.label.registry.A": 2, "top-level cratekit.label.registry.B": 1})


# ── Rule four: with a toggle off, every verb that remains still builds ───────


def _verb(name: str, module: str, toggle: str | None = None, builder: str = "build"):
    return measure.Verb(name=name, module=module, builder=builder, toggle=toggle)


def _dangling(tree, *verbs: measure.Verb) -> list:
    """The toggles of HOMES read over ``verbs``, the one ``sync`` verb when none is named."""
    return measure.dangling(tree, list(verbs) or [_verb("sync", "cratekit.sync.cli")], HOMES)


def test_a_core_verb_whose_module_imports_a_toggled_off_package_dangles():
    tree = _tree(
        label__registry="",
        organize__cli="from cratekit.label import registry\n\ndef build(parser, entry): ...\n")
    (labels, export, repair) = _dangling(tree, _verb("organize", "cratekit.organize.cli"))
    assert (labels.toggle, labels.verbs) == ("labels", ("organize",))
    assert labels.edges == (("cratekit.organize.cli", "cratekit.label.registry"),)
    assert export.verbs == () and repair.verbs == ()
    assert _lines(measure.dangling_lines(tree, [labels, export, repair])) == {
        "organize": ["dangling labels cratekit.label.registry"]
    }


def test_the_toggles_own_verbs_are_off_and_so_never_dangle():
    tree = _tree(label__cli="from cratekit.label import registry\n", label__registry="")
    found = _dangling(tree, _verb("label.sweep", "cratekit.label.cli", toggle="labels"))
    assert [item.verbs for item in found] == [(), (), ()]


def test_a_verb_dangles_through_a_module_it_only_reaches_indirectly():
    """The import is filed under the package that holds it, not the verb's."""
    tree = _tree(
        label__registry="", intake__landing="from cratekit.label import registry\n",
        sync__cli="from cratekit.intake import landing\n\ndef build(parser, entry): ...\n")
    found = _dangling(tree)
    assert found[0].verbs == ("sync",)
    assert _lines(measure.dangling_lines(tree, found)) == {
        "intake": ["dangling labels cratekit.label.registry"]
    }


def test_an_import_under_a_function_does_not_dangle_a_verb():
    run = "def run(args):\n    from cratekit.label import registry\n"
    tree = _tree(label__registry="", sync__cli="def build(parser, entry): ...\n" + run)
    assert [item.verbs for item in _dangling(tree)] == [(), (), ()]


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
        ))
    found = _dangling(
        tree, _verb("intake.set", "cratekit.intake.cli", builder="build_set"),
        _verb("intake.other", "cratekit.intake.cli", builder="build_other"))
    assert found[0].verbs == ("intake.set",)


def test_a_home_imported_directly_in_the_builder_dangles_the_verb():
    tree = _tree(
        label__registry="",
        sync__cli="def build(parser, entry):\n    from cratekit.label import registry\n")
    found = _dangling(tree)
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
        ))
    verbs = (_verb("sync", "cratekit.sync.cli"), _verb("intake", "cratekit.intake.cli"))
    assert [item.verbs for item in _dangling(tree, *verbs)] == [(), (), ()]


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
        ))
    assert _dangling(tree)[0].verbs == ("sync",)


def test_a_verb_the_registry_loads_from_inside_a_home_it_is_not_gated_by_dangles():
    tree = _tree(label__cli="def build(parser, entry): ...\n")
    found = _dangling(tree, _verb("label.heard", "cratekit.label.cli"))
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
    found = _dangling(measure.Tree(sources))
    assert found[0].verbs == ("sync",)
    assert found[0].edges == (("cratekit.sync", "cratekit.label.registry"),)


def test_nothing_is_followed_through_a_module_that_cannot_be_imported():
    """An import past the switched off package never runs, so it is no cause."""
    tree = _tree(
        export__cli="", label__registry="from cratekit.export import cli\n",
        sync__cli="from cratekit.label import registry\n\ndef build(parser, entry): ...\n")
    labels, export, _ = _dangling(tree)
    assert labels.edges == (("cratekit.sync.cli", "cratekit.label.registry"),)
    assert export.edges == (("cratekit.label.registry", "cratekit.export.cli"),)


# ── The count of core names ──────────────────────────────────────────────────


def test_core_names_are_counted_across_feature_packages_and_only_there():
    tree = _tree(
        core__config="def load(): ...\ndef save(): ...\nlocate = load\n",
        core__jobs="from cratekit.core.config import save\n",
        cli__doctor="from cratekit.core.config import save\n",
        intake__landing="from cratekit.core.config import load\n",
        sync__run="from cratekit.core import config\n\nconfig.load()\nconfig.locate()\n")
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
        core__config="try:\n    import tomllib\nexcept ImportError:\n    def fallback(): ...\n",
        sync__run="from cratekit.core import config\n\nconfig.fallback()\nconfig.tomllib\n")
    assert measure.core_names(tree) == {
        "sync": {"cratekit.core.config.fallback", "cratekit.core.config.tomllib"}
    }


def test_a_local_variable_named_as_an_imported_module_is_not_a_use_of_it():
    """A local ``source.name`` beside an imported module ``source`` is not a use of it."""
    tree = _tree(
        core__config="def load(): ...\n",
        sync__run=(
            "from cratekit.core import config\n\n"
            "def run(config):\n"
            "    return config.library, config._cache, config.load\n"
        ))
    assert measure.core_names(tree) == {"sync": {"cratekit.core.config.load"}}
    assert measure.private_crossings(tree) == {}


def test_a_module_that_answers_for_any_name_has_every_attribute_counted():
    """A ``__getattr__`` or a star import means the listed names are not all of them."""
    tree = _tree(
        core__config="def __getattr__(name): ...\n", core__naming="from os.path import *\n",
        sync__run="from cratekit.core import config, naming\n\nconfig.anything()\nnaming.join()\n")
    assert measure.core_names(tree) == {
        "sync": {"cratekit.core.config.anything", "cratekit.core.naming.join"}
    }


# ── The lists and the readings they depend on ────────────────────────────────


def test_the_interface_is_at_most_25_core_modules_sorted_and_real():
    assert len(CORE_INTERFACE) <= CORE_INTERFACE_LIMIT == 25
    assert list(CORE_INTERFACE) == sorted(set(CORE_INTERFACE))
    core = REPO_ROOT / measure.SOURCE / "core"
    missing = [name for name in CORE_INTERFACE if not (core / f"{name}.py").is_file()]
    assert not missing, f"the interface names core modules that do not exist: {missing}"


def test_every_toggle_has_its_homes_declared_and_every_home_exists():
    """Every toggle declares its homes here, or rule four reads its package as always on."""
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
    read = measure._load(REPO_ROOT)[3]
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


def test_a_starred_name_is_followed_into_the_part_that_holds_its_tuple():
    """The table is split over parts (U328): a part's rows and a constant of another source."""
    registry = (
        'UNIT = "U99"\n'
        'ENTRIES = (Entry(name="a", module="cratekit.a.cli", builder="build"), *MORE)\n'
    )
    part = (
        "MORE: tuple[Entry, ...] = (\n"
        '    Entry(name="b", module="cratekit.b.cli", builder="build", module_id="labels"),\n'
        '    Entry(name="c", module="cratekit.c.cli", builder="build", planned_in=UNIT),\n'
        ")\n"
    )
    assert measure.verbs_from(registry, part) == [
        measure.Verb("a", "cratekit.a.cli", "build", None),
        measure.Verb("b", "cratekit.b.cli", "build", "labels"),
    ]
    with pytest.raises(ValueError, match="holds no MORE tuple"):
        measure.verbs_from(registry)
    for unread in ((), (part,)):  # a tree with no registry is refused, never read as no verbs
        with pytest.raises(ValueError, match="holds no ENTRIES tuple"):
            measure.verbs_from(*unread)
    with pytest.raises(ValueError, match="not an Entry"):
        measure.verbs_from("ENTRIES = (*more.ROWS,)\n", part)


# ── The real package ─────────────────────────────────────────────────────────


def test_a_name_a_listed_module_takes_from_another_core_module_is_that_modules_own():
    """A re-export is a second binding, so each is held to the object it was taken from:
    every name a listed module imports by name from a core module off the list, read off
    the source, so a re-export added later is held without being listed here."""
    tree = measure.Tree(measure.read_sources(REPO_ROOT, [measure.SOURCE]))
    checked = 0
    for listed in CORE_INTERFACE:
        module = importlib.import_module(f"cratekit.core.{listed}")
        taken = tree._read[tree.modules[module.__name__]].handed
        for local, (origin, name) in taken.items():
            parts = origin.split(".")
            if name is None or parts[:2] != ["cratekit", "core"] or parts[2] in CORE_INTERFACE:
                continue
            held = getattr(importlib.import_module(origin), name)
            assert getattr(module, local) is held, (
                f"core.{listed}.{local} is no longer {origin}.{name}: a feature package "
                f"reading it through the list reads something else"
            )
            checked += 1
    assert checked > 100, f"only {checked} re-exported names were read off the listed modules"


#: The toggles whose homes U331 changed or whose verbs it moved out of.
DRIVEN_TOGGLES = ("analysis", "vocals", "favorites", "export")


def test_with_a_toggle_off_every_remaining_verb_builds_and_formats_its_help():
    """Rule four driven for real, for the toggles U331 touched: each toggle's homes made
    unimportable in a fresh interpreter, then every verb the toggle does not gate imported,
    built and its help formatted. Every toggle is ``refactor_measure.py imports --drive``."""
    homes = {toggle: TOGGLE_HOMES[toggle] for toggle in DRIVEN_TOGGLES}
    finished = subprocess.run(
        [sys.executable, "-c", measure._DRIVE, json.dumps(homes)],
        capture_output=True, text=True, check=False, cwd=REPO_ROOT)
    assert finished.returncode == 0, finished.stderr[-2000:]
    failed = json.loads(finished.stdout.strip().splitlines()[-1])
    assert failed == {toggle: [] for toggle in DRIVEN_TOGGLES}


def test_every_import_allowance_is_empty():
    """U331 emptied every allowance; a line put back is a crossing excused, so none may stand."""
    directory = REPO_ROOT / measure.IMPORT_ALLOWANCES
    files = sorted(directory.glob("*.txt"))
    assert len(files) > 10, f"read {len(files)} allowance files, too few to be the packages"
    held = {
        path.name: sorted(lines)
        for path in files
        if (lines := measure.parse_allowance(path.read_text(encoding="utf-8")))
    }
    assert not held, f"an allowance holds a line again, close the crossing instead: {held}"


def test_no_package_crosses_a_seam_beyond_its_allowance():
    """All four rules and the ceiling over one reading, so the package is parsed once."""
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
    # U328: a part of the verb table is imported by the registry alone, so a verb is read
    # through cli.registry, where the suite patches the table.
    part = f"{registry.__name__}_"
    reach = {use.path for uses in tree.uses.values() for use in uses if use.target.startswith(part)}
    assert reach == {measure.REGISTRY}, f"a part of the verb table is imported past it: {reach}"
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
