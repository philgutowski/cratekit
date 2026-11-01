"""U169: a ``--root`` is read against the library root, and a missing one refuses.

Sitting 47 ran ``crate name apply --root Downloads`` meaning the library's
Downloads folder. It was read against the shell's working directory, found no
files, and planned 0 renames as an ordinary empty plan, which is the answer a
tidy folder gives too. Every ``--root`` now goes through one reading: ``~``
expanded, a relative path joined to the library root, the library root when
omitted, and a folder that is not there refused naming the path it tried.
``repair paths --apply`` takes the reading and not the refusal, because its
root filters accepted proposals rather than naming a folder to walk.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import naming_cli
from tests.intake.test_repair_apply import LONG, SHORT, _accept, _answer, _names
from tests.intake.test_repair_apply import configured as repair_configured  # noqa: F401
from tests.intake.test_repair_apply import drive as repair_drive
from tests.test_config import valid_data
from tests.test_naming_apply_cli import _track, drive, library  # noqa: F401
from tests.test_naming_apply_cli import configured as name_configured  # noqa: F401

ELSEWHERE = "elsewhere"


@pytest.fixture
def standing_elsewhere(tmp_path, monkeypatch) -> Path:
    """The shell's directory, holding a folder of the same name as the library's.

    The old reading would have walked THIS folder, so its presence is what lets
    a test tell the two readings apart rather than only the missing case.
    """
    here = tmp_path / ELSEWHERE
    (here / "Music" / "wave").mkdir(parents=True)
    monkeypatch.chdir(here)
    return here


def _cfg(tmp_path: Path) -> config.Config:
    root = tmp_path / "lib"
    root.mkdir()
    return config.from_dict(valid_data(root))


# ═══════════════════════════════════════════════════════════════════════════
# The reading itself
# ═══════════════════════════════════════════════════════════════════════════


def test_a_relative_root_is_read_against_the_library_root(tmp_path, standing_elsewhere):
    cfg = _cfg(tmp_path)
    root = Path(cfg.library.root)

    assert naming_cli.root_path("Downloads", cfg, verb="v") == root / "Downloads"
    assert naming_cli.root_path("Music/wave", cfg, verb="v") == root / "Music" / "wave"


def test_an_absolute_root_is_taken_as_it_is(tmp_path):
    cfg = _cfg(tmp_path)
    elsewhere = tmp_path / "other"

    assert naming_cli.root_path(str(elsewhere), cfg, verb="v") == elsewhere


def test_a_home_relative_root_is_expanded_not_joined_to_the_library(tmp_path, monkeypatch):
    cfg = _cfg(tmp_path)
    home = tmp_path / "home"
    (home / "Downloads").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))

    assert naming_cli.root_folder("~/Downloads", cfg, verb="v") == home / "Downloads"


def test_an_omitted_root_is_the_library_root(tmp_path):
    cfg = _cfg(tmp_path)

    assert naming_cli.root_folder(None, cfg, verb="v") == Path(cfg.library.root)


@pytest.mark.parametrize("given", ["", "   "])
def test_an_empty_root_is_refused_rather_than_read_as_the_working_directory(tmp_path, given):
    cfg = _cfg(tmp_path)

    with pytest.raises(CratekitError) as caught:
        naming_cli.root_path(given, cfg, verb="name apply")
    assert caught.value.cause.reason == naming_cli.ROOT_MISSING
    assert "empty path" in caught.value.cause.message


def test_a_missing_relative_root_refuses_naming_the_path_it_tried(tmp_path, standing_elsewhere):
    cfg = _cfg(tmp_path)
    tried = Path(cfg.library.root) / "Downloads"

    with pytest.raises(CratekitError) as caught:
        naming_cli.root_folder("Downloads", cfg, verb="name apply")

    cause = caught.value.cause
    assert cause.reason == "root-folder-missing"
    assert cause.code is ExitCode.PRECONDITION
    assert f"--root Downloads was read against the library root as {tried}" in cause.message
    assert "name apply has nothing to work on" in cause.message
    assert cause.detail == {"tried": str(tried), "given": "Downloads"}


def test_a_missing_absolute_root_refuses_naming_it(tmp_path):
    cfg = _cfg(tmp_path)
    gone = tmp_path / "gone"

    with pytest.raises(CratekitError) as caught:
        naming_cli.root_folder(str(gone), cfg, verb="repair paths")
    assert caught.value.cause.message.startswith(f"--root {gone} is not a folder on this machine")


def test_a_file_where_the_folder_should_be_is_refused(tmp_path):
    cfg = _cfg(tmp_path)
    (Path(cfg.library.root) / "notes.txt").write_text("x")

    with pytest.raises(CratekitError) as caught:
        naming_cli.root_folder("notes.txt", cfg, verb="name apply")
    assert caught.value.cause.reason == "root-folder-missing"


def test_a_missing_library_root_is_refused_when_no_root_was_given(tmp_path, monkeypatch):
    unmounted = tmp_path / "unmounted"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(unmounted))
    cfg = config.from_dict(valid_data(unmounted))
    assert Path(cfg.library.root) == unmounted and not unmounted.exists()

    with pytest.raises(CratekitError) as caught:
        naming_cli.root_folder(None, cfg, verb="name apply")
    assert caught.value.cause.message.startswith("the library root ")


# ═══════════════════════════════════════════════════════════════════════════
# name apply, driven
# ═══════════════════════════════════════════════════════════════════════════


def _plan(*extra: str) -> tuple[int, dict]:
    code, out, err = drive(
        ["--output", "json", "-d", "name.apply.confirm=abort", "name", "apply", *extra]
    )
    return code, json.loads(out or err)


def test_name_apply_reads_a_relative_root_inside_the_library(
    name_configured, standing_elsewhere  # noqa: F811
):
    folder = Path(name_configured.library.root) / "Music" / "wave"
    folder.mkdir(parents=True)
    _track(folder, "Song - Artist - Song.flac", title="Song", key="4A")

    code, envelope = _plan("--root", "Music/wave")

    assert code == int(ExitCode.OK), envelope
    paths = [item["path"] for item in envelope["data"]["items"]]
    assert paths and all(path.startswith(str(folder)) for path in paths), paths


def test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library(
    name_configured, standing_elsewhere  # noqa: F811
):
    code, envelope = _plan("--root", "Downloads")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "root-folder-missing"
    tried = str(Path(name_configured.library.root) / "Downloads")
    assert tried in envelope["cause"]["message"]


# ═══════════════════════════════════════════════════════════════════════════
# repair paths, driven in both modes
# ═══════════════════════════════════════════════════════════════════════════


def test_repair_paths_scans_a_relative_root_inside_the_library(
    repair_configured, standing_elsewhere  # noqa: F811
):
    folder = Path(repair_configured.library.root) / "Music" / "wave"
    folder.mkdir(parents=True)
    (folder / LONG).write_bytes(b"fLaC")

    code, out, _ = repair_drive(["--output", "json", "repair", "paths", "--root", "Music/wave"])

    assert code == int(ExitCode.OK), out
    paths = [item["path"] for item in json.loads(out)["data"]["items"]]
    assert paths == [str(folder / LONG)], paths


def test_repair_paths_refuses_a_root_with_no_folder(repair_configured, standing_elsewhere):  # noqa: F811
    code, out, err = repair_drive(["--output", "json", "repair", "paths", "--root", "Downloads"])

    assert code == int(ExitCode.PRECONDITION), out or err
    assert json.loads(out or err)["cause"]["reason"] == "root-folder-missing"


def test_repair_apply_reads_a_relative_root_against_the_library_root(
    repair_configured, standing_elsewhere  # noqa: F811
):
    folder = Path(repair_configured.library.root) / "Music" / "wave"
    folder.mkdir(parents=True)
    path = folder / LONG
    path.write_bytes(b"fLaC")
    repair_drive(["--output", "json", "repair", "paths", "--root", str(folder)])
    _accept(repair_configured, path)

    code, envelope = _answer("apply", "--root", "Music/wave")

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["outside_root"] == 0
    assert _names(folder) == {SHORT}
