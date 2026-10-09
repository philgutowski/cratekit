"""R-228: pink rows outside All Favorites join the favourites sweep.

THE COLOUR READ IS FAKED HERE. A real read only open needs a disposable
library, which other suites already drive for rb_writer. This file pins the
union, the refusals and the plan facts against stand in rows and a patched
``read_pink_track_ids``, so the product decisions stay testable without a
database.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import cli as favorites_cli
from cratekit.modules.outbound import shell, source
from tests import outbound_fakes
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data
from tests.test_outbound_workers import _resume, bind, catalog, favorites_verb


@dataclass
class _Colour:
    ID: str
    Commnt: str
    rb_local_deleted: int = 0


@dataclass
class _Content:
    ID: str
    ColorID: str | None
    rb_local_deleted: int = 0


class _FakeDB:
    def __init__(self, colours: list[_Colour], contents: list[_Content]) -> None:
        self._colours = colours
        self._contents = contents

    def get_color(self, **kwargs):
        rows = self._colours
        for key, value in kwargs.items():
            rows = [row for row in rows if getattr(row, key) == value]
        return rows

    def get_content(self):
        return self._contents


@pytest.fixture
def installed(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    source.forget_libraries()
    yield resolved
    source.forget_libraries()


def test_pink_colour_id_looks_up_by_name_and_skips_soft_deleted():
    db = _FakeDB(
        colours=[
            _Colour("9", "Pink", rb_local_deleted=1),
            _Colour("7", "Pink"),
            _Colour("3", "Red"),
        ],
        contents=[],
    )
    assert favorites_cli.pink_colour_id(db) == "7"


def test_pink_colour_id_refuses_when_no_live_pink_row():
    db = _FakeDB(
        colours=[_Colour("1", "Pink", rb_local_deleted=1), _Colour("2", "Red")],
        contents=[],
    )
    with pytest.raises(CratekitError) as caught:
        favorites_cli.pink_colour_id(db)
    assert caught.value.cause.reason == favorites_cli.PINK_COLOUR_MISSING


def test_pink_content_ids_skips_soft_deleted_and_non_pink():
    db = _FakeDB(
        colours=[_Colour("1", "Pink")],
        contents=[
            _Content("10", "1"),
            _Content("11", "1", rb_local_deleted=1),
            _Content("12", "2"),
            _Content("13", None),
            _Content("14", "1"),
        ],
    )
    assert favorites_cli.pink_content_ids(db) == ("10", "14")


def test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink(installed):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1,), tracks=4
    )
    library = source.read_library(path)
    playlist = source.resolve(library, outbound_fakes.FAVORITES)
    resolved = favorites_cli.union_with_pink(library, playlist, ("1", "3", "4"))
    assert resolved.track_ids == ("1", "3", "4")
    assert resolved.from_playlist == 1
    assert resolved.from_colour == 3
    assert resolved.pink_missing == ()


def test_union_leaves_non_pink_outside_playlist_out(installed):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1, 2), tracks=4
    )
    library = source.read_library(path)
    playlist = source.resolve(library, outbound_fakes.FAVORITES)
    resolved = favorites_cli.union_with_pink(library, playlist, ("1",))
    assert resolved.track_ids == ("1", "2")
    assert "3" not in resolved.track_ids
    assert "4" not in resolved.track_ids
    assert resolved.from_playlist == 2
    assert resolved.from_colour == 1


def test_union_names_pink_rows_the_export_lacks(installed):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1,), tracks=2
    )
    library = source.read_library(path)
    playlist = source.resolve(library, outbound_fakes.FAVORITES)
    resolved = favorites_cli.union_with_pink(library, playlist, ("1", "99", "98"))
    assert resolved.track_ids == ("1",)
    assert resolved.pink_missing == ("99", "98")
    assert resolved.from_colour == 1


def test_resolve_sweep_refuses_empty_favorites_before_colour(installed, monkeypatch):
    """Noticed, not changed: an empty All Favorites still refuses (watcher answer 4)."""
    called: list[str] = []

    def boom(cfg):
        del cfg
        called.append("pink")
        raise AssertionError("colour must not be read after an empty playlist refusal")

    monkeypatch.setattr(favorites_cli, "read_pink_track_ids", boom)
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=()
    )
    with pytest.raises(CratekitError) as caught:
        favorites_cli.resolve_sweep(str(path), None, cfg=installed)
    assert caught.value.cause.reason == "export-playlist-empty"
    assert called == []


def test_resolve_sweep_propagates_the_colour_reads_own_cause(installed, monkeypatch):
    path = outbound_fakes.write_export(installed.library.root / "outbound")

    def unread(cfg):
        del cfg
        raise refuse(
            "rekordbox-running",
            "rekordbox is open, so the colour cannot be read",
            origin=("test", "favorites_pink"),
        )

    monkeypatch.setattr(favorites_cli, "read_pink_track_ids", unread)
    with pytest.raises(CratekitError) as caught:
        favorites_cli.resolve_sweep(str(path), None, cfg=installed)
    assert caught.value.cause.reason == "rekordbox-running"


def test_the_gate_names_colour_and_playlist_counts(installed, monkeypatch):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1,), tracks=3
    )
    monkeypatch.setattr(favorites_cli, "read_pink_track_ids", lambda cfg: ("1", "3"))
    code, refused = drive(favorites_verb(path))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["from_playlist"] == 1
    assert shown["from_colour"] == 2
    assert shown["items"] == ["1", "3"]
    assert shown["count"] == 2


def test_pink_missing_is_warned_beside_dangling(installed, monkeypatch):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound",
        favorites=(1, 99),
        tracks=2,
    )
    monkeypatch.setattr(favorites_cli, "read_pink_track_ids", lambda cfg: ("2", "88"))
    code, refused = drive(favorites_verb(path))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["items"] == ["1", "2"]
    assert shown["pink_missing"] == ["88"]
    assert shown["from_playlist"] == 1
    assert shown["from_colour"] == 1

    exported, resolved = favorites_cli.resolve_sweep(
        str(path), None, cfg=installed, pink_ids=("2", "88")
    )
    del exported
    age = source.export_age(path, limit_days=installed.outbound.export_stale_days)
    warned = shell.queue_warnings(resolved, noun="favourite", age=age)
    codes = [one["code"] for one in warned]
    assert "playlist-track-missing" in codes
    assert "favorites-pink-export-missing" in codes
    pink = next(one for one in warned if one["code"] == "favorites-pink-export-missing")
    assert "88" in pink["message"]
    dangling = next(one for one in warned if one["code"] == "playlist-track-missing")
    assert "99" in dangling["message"]


def test_pink_outside_playlist_is_offered_and_hearted(installed, monkeypatch):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1,), tracks=3
    )
    monkeypatch.setattr(favorites_cli, "read_pink_track_ids", lambda cfg: ("3",))
    account = outbound_fakes.StrictAccount(catalog=catalog(1, 3))
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(favorites_verb(path), "sync.favorites.confirm")
    del _run
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert sorted(account.hearted) == ["tid-1", "tid-3"]


def test_pink_already_hearted_is_counted_as_already(installed, monkeypatch):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1,), tracks=3
    )
    monkeypatch.setattr(favorites_cli, "read_pink_track_ids", lambda cfg: ("3",))
    account = outbound_fakes.StrictAccount(catalog=catalog(1, 3), hearts={"tid-3"})
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(favorites_verb(path), "sync.favorites.confirm")
    del _run
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["outbound"]["hearted"] == ["tid-1"]
    assert resumed["data"]["progress"]["outbound"]["already"] == ["tid-3"]


def test_pink_readers_call_trees_soft_delete_marker():
    """The watcher named trees.soft_delete_marker; a private read would widen the pin."""
    source_text = Path("src/cratekit/favorites/cli.py").read_text()
    assert "trees.soft_delete_marker" in source_text
    assert "getattr(row, \"rb_local_deleted\"" not in source_text
    assert "row.rb_local_deleted" not in source_text
