"""R-1917: a broken test root guard leaves nothing behind it.

``tests/test_config_test_root.py`` once aimed its refused writes at a fixed name
at the filesystem root, so a mutation row that broke ``core/config.py``'s guard
left a folder there and eight of its tests failed on that machine in every later
run. Here the file runs in a child pytest twice: once with the guard broken by a
plugin, which must fail and leave its own system temporary folder empty and the
filesystem root as it found it, then once with the guard intact on the same
machine, which must pass.
"""

from __future__ import annotations

import os
import subprocess
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

#: The file under test, run by path from the checkout this suite sits in.
TARGET = Path(__file__).with_name("test_config_test_root.py")

#: Loaded with ``-p``: every state writer is let through, as a mutant of the guard does.
BREAK_THE_GUARD = '''from cratekit.core import config as guarded


def _let_through(path, *, system_temporary=False):
    return None


def pytest_configure(config):
    guarded._refuse_write_outside_test_root = _let_through
'''


#: The tests whose refused write aims at the ``outside`` fixture: with the guard
#: broken each write lands there, so each must fail, and the fixture must remove it.
AIMED_OUTSIDE = (
    "test_a_path_outside_the_root_is_refused_with_the_isolation_in_place",
    "test_a_link_inside_the_root_aimed_outside_it_is_refused",
    "test_a_path_resolution_that_leaves_the_root_is_refused",
    "test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]",
    "test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]",
    "test_a_lock_outside_every_temporary_folder_is_refused",
)


def _run_the_file(
    tmp_path: Path, name: str, *, broken: bool
) -> tuple[subprocess.CompletedProcess, Path]:
    system_temporary = tmp_path / f"{name}-system-temporary"
    system_temporary.mkdir()
    env = os.environ.copy()
    env["TMPDIR"] = str(system_temporary)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-o", "addopts="]
    if broken:
        (tmp_path / "break_the_guard.py").write_text(BREAK_THE_GUARD, encoding="utf-8")
        env["PYTHONPATH"] = os.pathsep.join(
            each for each in (str(tmp_path), env.get("PYTHONPATH", "")) if each
        )
        command += ["-p", "break_the_guard"]
    report = tmp_path / f"{name}-report.xml"
    command += ["--tb=line", f"--junitxml={report}", f"--basetemp={tmp_path / f'{name}-base'}"]
    command.append(str(TARGET))
    done = subprocess.run(
        command, cwd=TARGET.parent.parent, env=env, capture_output=True, text=True,
        check=False, timeout=600,
    )
    left = sorted(each.name for each in system_temporary.iterdir())
    assert left == [], f"the {name} run left {left} in its system temporary folder"
    return done, report


def _failed(report: Path) -> set[str]:
    """The failed or erred test names, read off pytest's own report, never off its output."""
    cases = ElementTree.parse(report).getroot().iter("testcase")
    return {
        case.get("name") for case in cases
        if case.find("failure") is not None or case.find("error") is not None
    }


#: The probes ``tests/test_doctor.py`` makes and removes at the real filesystem root
#: on Linux, which a parallel worker may hold for an instant while this test lists it.
DOCTOR_PROBES = "cratekit-u27-"


def _root_names() -> set[str]:
    return {name for name in os.listdir(os.sep) if not name.startswith(DOCTOR_PROBES)}


def test_a_broken_guard_fails_the_file_leaves_nothing_and_a_later_run_passes(tmp_path):
    root_before = _root_names()

    broken, report = _run_the_file(tmp_path, "broken", broken=True)
    assert broken.returncode == 1, broken.stdout[-3000:] + broken.stderr[-3000:]
    assert set(AIMED_OUTSIDE) <= _failed(report), broken.stdout[-3000:]
    assert _root_names() - root_before == set()

    intact, report = _run_the_file(tmp_path, "intact", broken=False)
    assert _failed(report) == set()
    assert intact.returncode == 0, intact.stdout[-3000:] + intact.stderr[-3000:]
    assert _root_names() - root_before == set()
