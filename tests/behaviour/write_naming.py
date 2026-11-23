"""The write layer's naming scenarios: a folder put in the naming convention (U302).

`crate name apply --root FOLDER` renames each file out of convention behind its
gate and writes its title tag; a row under an unmapped volume refuses the pass,
and a rename onto a held name is never made. Its own file because both suites
name ``configured`` and ``library``.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_naming_apply_cli import _folder, _pair, _record, _track
from tests.test_naming_apply_cli import collected as collected  # noqa: PLC0414
from tests.test_naming_apply_cli import configured as configured  # noqa: PLC0414
from tests.test_naming_apply_cli import library as library  # noqa: PLC0414
from tests.test_naming_apply_cli import prefix_map as prefix_map  # noqa: PLC0414

OK = int(ExitCode.OK)
APPLY = "name.apply.confirm=apply"


def test_a_rename_planned_and_applied_beside_a_referenced_file(stage, collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")

    asked = stage.crate("name", "apply", "--root", str(folder))
    assert asked.code == int(ExitCode.DECISION_REQUIRED), asked.stdout
    applied = stage.json("-d", APPLY, "name", "apply", "--root", str(folder))
    assert applied.code == OK, applied.stdout
    assert held.is_file() and not free.exists()
    # Ask again: the referenced file is still held, and nothing else is planned.
    stage.crate("name", "apply", "--root", str(folder))


def test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing(stage, collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")

    refused = stage.json("-d", APPLY, "name", "apply", "--root", str(folder))
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert refused.envelope["cause"]["reason"] == "collection-row-unmapped"
    assert held.is_file() and free.is_file()


def test_a_rename_onto_a_name_another_file_holds_overwrites_nothing(stage, configured):
    folder = _folder(configured)
    _track(folder, "01A - 124 - Cola.flac", title="01A - 124 - Cola", key="01A")
    other = _track(folder, "1A - 124 - Cola.flac", title="1A - 124 - Cola", key="1A")

    refused = stage.json("-d", APPLY, "name", "apply", "--root", str(folder))
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert refused.envelope["cause"]["reason"] == "rename-incomplete"
    assert other.is_file()
