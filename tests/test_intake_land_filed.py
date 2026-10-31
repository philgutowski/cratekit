"""U164: a native landing puts its files straight into Processed_Tracks/<year>/<MM_DD_YY subject>.

The batch lands where a shelve would have filed it, so its rows carry their
final ``FolderPath`` from the first commit and no shelve follows. These tests
drive the real dispatcher against the disposable database
``tests/test_intake_land_native.py`` builds, and pin what the brief asks: the
filed folder for a dated name and for a name of no date, the shelve rule's
suffix on a taken name, a second landing that day taking `` 2`` for its
playlist and its folder, the INBOX playlist keeping its readable name, the
rows read back with the final path, and ``intake shelve`` reporting nothing to
do for such a batch. The xml bridge keeps ``Music/<batch>``, which
``tests/test_intake_land_names.py`` and ``tests/test_intake_land.py`` hold.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, shelve_cli
from tests.cli_drive import drive
from tests.test_intake_land_native import _advance_usn, _query, _stage, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

DAY = date(2026, 10, 27)
SUBJECT = "Tidal playlists and Favorites"
NAMED = f"2026-10-27 {SUBJECT}"


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


def _processed(cfg: config.Config) -> Path:
    # Spelled here and not through the engine, so the expectation is not the
    # code under test agreeing with itself.
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


# ---------------------------------------------------------------------------
# The filed folder
# ---------------------------------------------------------------------------


def test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")

    code, refused = drive(["intake", "land", "--name", NAMED])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    filed = _processed(cfg) / "2026" / f"10_27_26 {SUBJECT}"
    # THE SCREEN AND THE DIGEST NAME THE FINAL FOLDER, before anything moves.
    assert refused["cause"]["detail"]["shown"]["lands in"] == str(filed)

    acted = _landed("--name", NAMED)

    assert sorted(p.name for p in filed.iterdir()) == ["One.flac", "Two.flac"]
    assert _paths(cfg)[-2:] == [str(filed / "One.flac"), str(filed / "Two.flac")]
    assert not (_music(cfg) / NAMED).exists(), "no batch folder is made under the music folder"
    # The INBOX playlist keeps the batch's readable name; only the folder changed.
    assert _playlists(cfg, "2026-10-27%") == [NAMED]
    assert acted["data"]["items"][-1]["playlist"] == NAMED


def test_an_unnamed_landing_files_under_the_day_and_its_source_words(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    _landed()

    filed = _processed(cfg) / "2026" / "10_27_26 Downloads"
    assert (filed / "One.flac").is_file()
    assert _playlists(cfg, "2026-10-27%") == ["2026-10-27 Downloads"]


def test_a_name_with_no_date_is_the_subject_under_the_landing_day(native_library, silence):
    """``--name`` still sets the subject; a name that carries no date is filed
    under the day it landed."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    _landed("--name", "Friday warmup")

    assert (_processed(cfg) / "2026" / "10_27_26 Friday warmup" / "One.flac").is_file()
    assert _playlists(cfg, "Friday warmup") == ["Friday warmup"]


# ---------------------------------------------------------------------------
# A taken name, the shelve rule's suffix
# ---------------------------------------------------------------------------


def test_a_folder_already_on_disk_is_passed_over_for_the_next_suffix(native_library, silence):
    cfg, _root = native_library
    taken = _processed(cfg) / "2026" / f"10_27_26 {SUBJECT}"
    taken.mkdir(parents=True)
    (taken / "Kept.flac").write_bytes(b"filed by hand")
    _stage(cfg, silence, "One.flac")

    _landed("--name", NAMED)

    assert (_processed(cfg) / "2026" / f"10_27_26 {SUBJECT} 2" / "One.flac").is_file()
    assert sorted(p.name for p in taken.iterdir()) == ["Kept.flac"]


def test_a_folder_the_collection_stores_rows_under_is_passed_over_with_nothing_on_disk(
    native_library, silence
):
    """A folder filed by hand and later moved leaves rows stored under its name,
    and a batch landed there would sit beside rows it did not make."""
    cfg, _root = native_library
    gone = _processed(cfg) / "2026" / f"10_27_26 {SUBJECT}"
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('moved-1', 'moved', ?, 0, '2026-01-01', '2026-01-01')",
        (str(gone / "Elsewhere.flac"),),
    )
    _advance_usn(conn)
    conn.commit()
    conn.close()
    _stage(cfg, silence, "One.flac")

    _landed("--name", NAMED)

    assert not gone.exists()
    assert (_processed(cfg) / "2026" / f"10_27_26 {SUBJECT} 2" / "One.flac").is_file()


def test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder(
    native_library, silence
):
    """No folder is left under the music folder to keep the name taken, so the
    landing's record keeps it, and the two batches never share a playlist."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _landed()
    _stage(cfg, silence, "Two.flac")

    _landed()

    assert _playlists(cfg, "2026-10-27%") == ["2026-10-27 Downloads", "2026-10-27 Downloads 2"]
    assert (_processed(cfg) / "2026" / "10_27_26 Downloads" / "One.flac").is_file()
    assert (_processed(cfg) / "2026" / "10_27_26 Downloads 2" / "Two.flac").is_file()


def test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone(
    native_library, silence
):
    cfg, _root = native_library
    filed = _processed(cfg) / "2026" / "10_27_26 Friday warmup"
    _stage(cfg, silence, "One.flac")
    _landed("--name", "Friday warmup")
    _stage(cfg, silence, "Two.flac")

    _landed("--name", "Friday warmup")

    assert sorted(p.name for p in filed.iterdir()) == ["One.flac", "Two.flac"]
    # A recorded folder moved away by hand is not reused; the free rule
    # chooses, and the rows still stored under the old name pass it over.
    os.rename(filed, filed.parent / "elsewhere")
    _stage(cfg, silence, "Three.flac")
    _landed("--name", "Friday warmup")
    assert not filed.exists()
    assert (filed.parent / "10_27_26 Friday warmup 2" / "Three.flac").is_file()


# ---------------------------------------------------------------------------
# Shelve has nothing to do
# ---------------------------------------------------------------------------


def test_shelve_over_a_batch_landed_filed_reports_nothing_to_do(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _landed("--name", NAMED)
    before = _paths(cfg)

    code, envelope = drive(["intake", "shelve", NAMED])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op", envelope
    (item,) = envelope["data"]["items"]
    assert item["action"] == shelve_cli.ALREADY_FILED
    assert item["folder"] == str(_processed(cfg) / "2026" / f"10_27_26 {SUBJECT}")
    assert [one["code"] for one in envelope["warnings"]] == [shelve_cli.BATCH_ALREADY_FILED]
    assert _paths(cfg) == before
    assert "gate" not in envelope["data"]
