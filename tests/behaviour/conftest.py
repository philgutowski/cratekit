"""The fixtures around every behaviour scenario (U297).

Three things are added on top of ``tests/conftest.py``, whose isolation is
already in force for every file under ``tests/`` and is not repeated here.

1. THE ROOTS MOVE INTO THE SCENARIO'S OWN DIRECTORY. The suite's isolation
   gives each test numbered directories of its own, numbered in the order the
   run made them, so a scenario's paths would change with the scenarios that
   ran before it. Every variable that isolation pointed into one of those is
   re-pointed to the same place under the scenario's ``tmp_path``, which
   pytest names for the test and nothing else. The list of variables is read
   off the environment and not kept here, so a root the suite's isolation
   gains later moves with the rest.

2. THE CLOCK AND THE IDS ARE PINNED, and the terminal width and time zone
   fixed, so two runs of one scenario print and write the same bytes.

3. A SCENARIO THAT COULD REACH PAST ITS OWN DIRECTORY IS REFUSED. Before every
   command the configuration and state directories the product itself
   resolves must be inside the scenario's ``tmp_path`` and inside the
   system's temporary directory.

All three are autouse here, so they are set up after the suite's isolation
and before any fixture a scenario asks for, and they hold an instance of
``pytest.MonkeyPatch`` of their own for the reason the suite's conftest gives.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import time
from pathlib import Path

import pytest

from tests import behaviour

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load_script():
    """``scripts/behaviour_compare.py``, which owns the record's form and the refusal."""
    name = "cratekit_behaviour_compare"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(
        name, REPO_ROOT / "scripts" / "behaviour_compare.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


compare = _load_script()

_PASSED = pytest.StashKey[bool]()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Remember whether a scenario's own body passed, for the stage's teardown."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.stash[_PASSED] = report.passed


def refuse_a_root_outside(scenario_root: Path) -> None:
    """Raise unless the product's own configuration and state roots are the scenario's.

    Asked of the product, not of the environment this file set: what matters
    is where a write would land, and a resolver that stopped reading the
    variables would otherwise send it somewhere this check never looked.
    """
    from cratekit.core import config

    for what, path in (
        ("the configuration directory", Path(config.config_dir())),
        ("the state directory", Path(config.installation_state_dir())),
    ):
        compare.refuse_outside_temporary(path, what)
        if not compare.is_inside(path, scenario_root):
            raise compare.Refusal(
                f"{what} is {path}, which is not inside the scenario's own directory "
                f"{scenario_root}; a scenario writes only there"
            )


def refuse_a_scenario_without_a_stage(fixturenames) -> None:
    """Raise for a scenario that does not take the stage.

    Its commands would run past the record, it would pass, and the capture
    would close without it and say nothing.
    """
    if "stage" not in fixturenames:
        raise compare.Refusal(
            "a scenario takes the stage fixture and runs its commands through it; one "
            "that does not would pass and leave no record"
        )


def refuse_another_source() -> None:
    """Raise unless the product was imported from the source the capture placed."""
    import cratekit

    expected = os.environ.get(compare.ENV_SOURCE)
    imported = Path(cratekit.__file__).resolve()
    if expected and not compare.is_inside(imported, Path(expected)):
        raise compare.Refusal(
            f"the scenarios imported cratekit from {imported}, not from the source the "
            f"capture placed at {expected}, so this run would record another tree"
        )


@pytest.fixture(autouse=True)
def _scenario_world(request, tmp_path):
    """The roots, the pins and the fixed terminal, for the life of one scenario."""
    from cratekit.core import config

    refuse_a_scenario_without_a_stage(request.fixturenames)
    refuse_another_source()
    moved = {
        request.getfixturevalue("_isolate_state_roots"): tmp_path,
        request.getfixturevalue("_block_real_library_paths"): tmp_path / "library",
    }
    with pytest.MonkeyPatch.context() as patch:
        for old, new in moved.items():
            for name, value in behaviour.environment_under(old).items():
                patch.setenv(name, str(new / Path(value).relative_to(old)))
            for name in ("CONFIG_DIR", "STATE_DIR", "LIBRARY_ROOT"):
                value = getattr(config, name, None)
                if isinstance(value, Path) and compare.is_inside(value / "x", old):
                    patch.setattr(config, name, new / value.relative_to(old))
        for name in ("HOME", "XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"):
            Path(os.environ[name]).mkdir(parents=True, exist_ok=True)
        (tmp_path / "library").mkdir(exist_ok=True)
        patch.setenv("COLUMNS", "80")
        patch.setenv("LINES", "24")
        patch.setenv("TZ", "UTC")
        time.tzset()
        config.reset_cache()
        unpin = behaviour.pin(patch)
        try:
            yield
        finally:
            unpin()
    time.tzset()
    config.reset_cache()


@pytest.fixture
def stage(request, tmp_path, _scenario_world):
    """The scenario's stage. Its record is written when the scenario passed and a capture asked."""
    name = behaviour.scenario_name(request.node.path, request.node.originalname)
    made = behaviour.Stage(
        name=name, root=tmp_path, refuse_outside=lambda: refuse_a_root_outside(tmp_path)
    )
    made.refuse_outside()
    yield made
    out = os.environ.get(compare.ENV_OUT)
    if out and request.node.stash.get(_PASSED, False):
        compare.record_scenario(
            Path(out), name, made.commands, tmp_path, behaviour.process_identity()
        )
