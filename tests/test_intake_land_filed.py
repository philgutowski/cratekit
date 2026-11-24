"""U164: a native landing puts its files straight into Processed_Tracks/<year>/<MM_DD_YY subject>.

The rows carry their final ``FolderPath`` from the first commit, so no shelve follows. Nothing
here is real (D1)."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, shelve_cli
from tests.cli_drive import drive
from tests.test_intake_land_hearts_native import cfg as cfg  # noqa: PLC0414 - the fixture
from tests.test_intake_land_native import _answered, _hold, _query, _shown, _stage, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged
from tests.test_intake_land_native import library as library
from tests.test_intake_land_native import machine as machine
from tests.test_intake_land_native import native_library as native_library
from tests.test_intake_land_native import silence as silence

DAY = date(2026, 10, 27)
SUBJECT = "Tidal playlists and Favorites"
NAMED = f"2026-10-27 {SUBJECT}"


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


def _processed(cfg: config.Config) -> Path:
    # Spelled here, not through the engine, so the code does not agree with itself.
    return Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks"


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir


def _paths(cfg: config.Config) -> list[str]:
    """Every row's stored FolderPath, in order."""
    return [str(row[0]) for row in _query(cfg, "SELECT FolderPath FROM djmdContent ORDER BY 1")]


def _playlists(cfg: config.Config, like: str) -> list[str]:
    rows = _query(cfg, "SELECT Name FROM djmdPlaylist WHERE Name LIKE ? ORDER BY Name", like)
    return [str(row[0]) for row in rows]


def _landed(*args: str) -> dict:
    code, acted, _refused = _two_acts(["intake", "land", *args])
    assert code == int(ExitCode.OK), acted
    return acted


def test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject(cfg, silence):
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    filed = _processed(cfg) / "2026" / f"10_27_26 {SUBJECT}"
    # THE SCREEN AND THE DIGEST NAME THE FINAL FOLDER, before anything moves.
    assert _shown(["intake", "land", "--name", NAMED])["lands in"] == str(filed)
    acted = _landed("--name", NAMED)
    assert sorted(p.name for p in filed.iterdir()) == ["One.flac", "Two.flac"]
    assert _paths(cfg)[-2:] == [str(filed / "One.flac"), str(filed / "Two.flac")]
    assert not (_music(cfg) / NAMED).exists(), "no batch folder is made under the music folder"
    # The INBOX playlist keeps the batch's readable name; only the folder changed.
    assert _playlists(cfg, "2026-10-27%") == [NAMED]
    assert acted["data"]["items"][-1]["playlist"] == NAMED
    # A shelve over the batch landed filed has nothing to do.
    before = _paths(cfg)
    code, envelope = drive(["intake", "shelve", NAMED])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op", envelope
    (item,) = envelope["data"]["items"]
    assert item["action"] == shelve_cli.ALREADY_FILED
    assert item["folder"] == str(filed)
    assert [one["code"] for one in envelope["warnings"]] == [shelve_cli.BATCH_ALREADY_FILED]
    assert _paths(cfg) == before
    assert "gate" not in envelope["data"]


def test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over(cfg, silence):
    """A folder moved away by hand leaves rows stored under its name, with nothing on disk."""
    taken = _processed(cfg) / "2026" / f"10_27_26 {SUBJECT}"
    taken.mkdir(parents=True)
    (taken / "Kept.flac").write_bytes(b"filed by hand")
    gone = _processed(cfg) / "2026" / f"10_27_26 {SUBJECT} 2"
    _hold(cfg, "moved-1", str(gone / "Elsewhere.flac"))
    _stage(cfg, silence, "One.flac")
    _landed("--name", NAMED)
    assert sorted(p.name for p in taken.iterdir()) == ["Kept.flac"]
    assert not gone.exists()
    assert (_processed(cfg) / "2026" / f"10_27_26 {SUBJECT} 3" / "One.flac").is_file()


def test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder(cfg, silence):
    """No folder under the music folder keeps the name taken, so the record does."""
    _stage(cfg, silence, "One.flac")
    _landed()
    _stage(cfg, silence, "Two.flac")
    _landed()
    assert _playlists(cfg, "2026-10-27%") == ["2026-10-27 Downloads", "2026-10-27 Downloads 2"]
    assert (_processed(cfg) / "2026" / "10_27_26 Downloads" / "One.flac").is_file()
    assert (_processed(cfg) / "2026" / "10_27_26 Downloads 2" / "Two.flac").is_file()


def test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone(cfg, silence):
    filed = _processed(cfg) / "2026" / "10_27_26 Friday warmup"
    _stage(cfg, silence, "One.flac")
    _landed("--name", "Friday warmup")
    # ``--name`` with no date is the subject, filed under the landing day.
    assert _playlists(cfg, "Friday warmup") == ["Friday warmup"]
    _stage(cfg, silence, "Two.flac")
    _landed("--name", "Friday warmup")
    assert sorted(p.name for p in filed.iterdir()) == ["One.flac", "Two.flac"]
    # A recorded folder moved away is not reused; its stored rows pass it over.
    os.rename(filed, filed.parent / "elsewhere")
    _stage(cfg, silence, "Three.flac")
    _landed("--name", "Friday warmup")
    assert not filed.exists()
    assert (filed.parent / "10_27_26 Friday warmup 2" / "Three.flac").is_file()


def test_a_name_that_is_a_date_alone_files_as_downloads(cfg, silence):
    """The shelve's word for a batch that says nothing about its source."""
    _stage(cfg, silence, "One.flac")
    _landed("--name", "2026-10-27")
    assert (_processed(cfg) / "2026" / "10_27_26 Downloads" / "One.flac").is_file()


def test_a_filed_folder_on_another_device_is_refused_at_the_move(cfg, silence, monkeypatch):
    """The device is checked against the folder the plan chose; nothing leaves staging."""
    from cratekit.intake import landing
    _stage(cfg, silence, "One.flac")
    run_id = _answered(["intake", "land", "--name", NAMED])[1]
    real = landing._device_of
    processed = str(_processed(cfg))

    def elsewhere(path):
        return -1 if str(path).startswith(processed) else real(path)
    monkeypatch.setattr(landing, "_device_of", elsewhere)
    code, acted = drive(["--run", run_id, "intake", "land", "--name", NAMED])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "intake-staging-refused", acted
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    assert not (_processed(cfg) / "2026").exists()
