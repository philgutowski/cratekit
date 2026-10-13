"""U121: a set intake leaves a permanent playlist of the set under INSPIRATION.

Driven against the disposable database the native landing suite builds. A set
job is queued the way ``intake set`` queues one, run to the end so its reports
say which tracks the library owns and which are missing, and the landing is
given the job with ``--set``. The backfill verb is driven over a set that
landed without it.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.core import active_taxonomy, config, jobs, preflight, rb_writer, review, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import batch_name, inspiration_cli, land_cli, set_playlist
from cratekit.intake import cli as intake_cli
from tests import adopt_fixtures, cutover_fixtures
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_intake_land_native import (
    DECLARED,
    INTAKE,
    LIBRARY_LINK,
    _cut_over_intake,
    _members,
    _query,
    _seed_binding_rows,
    _two_acts,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_rb_writer_db import RECORDED_APP_VERSION

DAY = date(2026, 10, 9)
BATCH = "2026-10-09 Set"
FOLDER = DECLARED.inspiration.display
WORDS = ["--dj", "Probe DJ", "--set-name", "Live at Probe", "--set-date", "2026-05"]
NAME = "10_09_26 Probe DJ Live at Probe 5-26"
POSTED_NAME = "5_03_26 Probe DJ Live at Probe 5-26"
PAGE = {"title": "Probe DJ - Live at Probe 05.03.26", "uploader": "Probe DJ", "upload_date": "20260503"}
APPROVE = inspiration_cli.APPROVE_GATE


@pytest.fixture
def machine(library, monkeypatch):
    """The native landing suite's machine on the FULL profile, which carries ``intake set``.

    The landing suite's own machine is on the default profile, where the set
    verb is not enabled and a set job cannot be resumed through the driver.
    Everything else is that fixture's: the disposable database, the binding
    rows, the identity seams.
    """
    resolved = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, ())
    _seed_binding_rows(resolved)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return resolved


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


# ---------------------------------------------------------------------------
# Fixtures: files, rows and a finished set job
# ---------------------------------------------------------------------------


def _tagged(path: Path, silence: Path, title: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    return path


def _stage(cfg: config.Config, silence: Path, title: str) -> Path:
    return _tagged(Path(cfg.paths.download_staging) / f"{title}.flac", silence, title)


def _owned(cfg: config.Config, silence: Path, title: str, *, content_id: str) -> Path:
    """A file the library holds under its own folder, with the collection row rekordbox gave it."""
    path = _tagged(Path(cfg.library.root) / cfg.library.music_dir / "Owned" / f"{title}.flac", silence, title)
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES (?, ?, ?, 0, '2026-01-01', '2026-01-01')",
        (content_id, title, str(path)),
    )
    conn.commit()
    conn.close()
    return path


def set_job(cfg: config.Config, titles: tuple[str, ...], *, page: dict | None = None) -> str:
    """One set job over ``titles`` in that order, queued as ``intake set`` queues one and run."""
    tracks = {
        f"rc_{title}": {
            "artist": "Probe",
            "title": title,
            "origin": match.TEXT,
            "spelled": f"Probe - {title}",
        }
        for title in titles
    }
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload={
                intake_cli.SOURCE: "https://example.invalid/a-set",
                intake_cli.TRACKS: tracks,
                intake_cli.CALLS: len(titles),
                intake_cli.UNREACHED: 0,
                intake_cli.PARTS: 1,
                intake_cli.PAGE: dict(page or {}),
            },
            cfg=cfg,
            item_ids=tuple(tracks),
        )
    code, resumed = drive(cli_jobs.argv_for(job))
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    return job.job_id


def _land(*extra: str) -> list[str]:
    return ["intake", "land", "--name", BATCH, *extra]


def _inspiration(job_id: str, *extra: str) -> list[str]:
    return ["intake", "inspiration", "--job", job_id, *extra]


def _two_acts_approve(verb: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against the backfill's explicit gate, then the acting drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == APPROVE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, APPROVE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _row_ids_by_name(cfg: config.Config) -> dict[str, str]:
    rows = _query(cfg, "SELECT ID, FolderPath FROM djmdContent WHERE rb_local_deleted = 0")
    return {Path(str(folder)).stem: str(content_id) for content_id, folder in rows}


def _playlists_named(cfg: config.Config, name: str) -> list[tuple]:
    return _query(
        cfg,
        "SELECT ID, ParentID, Attribute, rb_local_deleted FROM djmdPlaylist WHERE Name = ?",
        name,
    )


def _root_folders(cfg: config.Config, name: str) -> list[tuple]:
    return _query(
        cfg,
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 AND "
        "(ParentID IS NULL OR ParentID IN ('', '0', 'root', 'None'))",
        name,
    )


def _children(cfg: config.Config, parent_id: str) -> list[str]:
    return [
        str(row[0])
        for row in _query(
            cfg,
            "SELECT ID FROM djmdPlaylist WHERE ParentID = ? AND rb_local_deleted = 0",
            parent_id,
        )
    ]


def _content_table(cfg: config.Config) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdContent ORDER BY ID")


def _refused_before_the_gate(cfg: config.Config, code: int, envelope: dict, reason: str) -> None:
    assert code != int(ExitCode.OK) and code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == reason, envelope
    assert not [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]


# ---------------------------------------------------------------------------
# The name
# ---------------------------------------------------------------------------


def test_the_name_is_the_source_systems_form_to_the_character():
    words = set_playlist.SetWords("Public Service NYC", "Live at Vonking", date(2026, 5, 1))
    assert (
        set_playlist.playlist_name(words, on=date(2026, 10, 9))
        == "10_09_26 Public Service NYC Live at Vonking 5-26"
    )
    # The folder's own examples: month without a leading zero, day with one.
    assert set_playlist.playlist_name(
        set_playlist.SetWords("oshe", "GOATCHELLA Radio Mix", date(2026, 4, 1)), on=date(2026, 5, 28)
    ) == "5_28_26 oshe GOATCHELLA Radio Mix 4-26"
    assert set_playlist.playlist_name(
        set_playlist.SetWords("Pepofit", "PEPOFIT LIB JUNKYARD", date(2026, 5, 1)),
        on=date(2026, 6, 16),
    ) == "6_16_26 Pepofit PEPOFIT LIB JUNKYARD 5-26"
    # December and a two digit month in the set's half.
    assert set_playlist.playlist_name(
        set_playlist.SetWords("A", "B", date(2025, 12, 1)), on=date(2026, 1, 3)
    ) == "1_03_26 A B 12-25"


def _job_with(page: dict) -> jobs.Job:
    return jobs.Job(
        job_id="j-1",
        handler_key=set_playlist.SET_KEY,
        payload={intake_cli.PAGE: page},
        config_fingerprint="",
        config_toml="",
        library_id="",
        state=jobs.JobState.SUCCEEDED,
        created="",
        updated="",
    )


def test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title():
    words = set_playlist.words_for(_job_with(PAGE))
    assert words == set_playlist.SetWords("Probe DJ", "Live at Probe 05.03.26", date(2026, 5, 1))
    # A title not led by the uploader is kept whole, and so is one that is only the uploader.
    assert set_playlist.words_for(_job_with({**PAGE, "title": "Live at Probe"})).name == "Live at Probe"
    assert set_playlist.words_for(_job_with({**PAGE, "title": "Probe DJ"})).name == "Probe DJ"
    assert set_playlist.words_for(_job_with({**PAGE, "title": "probe dj | Set"})).name == "Set"


def test_a_flag_wins_over_the_page_and_a_day_is_read_as_its_month():
    words = set_playlist.words_for(
        _job_with(PAGE), dj="PSNYC", set_name="Vonking", set_date="2026-04-17"
    )
    assert words == set_playlist.SetWords("PSNYC", "Vonking", date(2026, 4, 1))


@pytest.mark.parametrize(
    ("page", "flags", "missing"),
    [
        ({}, {}, ["--dj", "--set-name", "--set-date"]),
        ({"title": "A Set"}, {}, ["--dj", "--set-date"]),
        ({"uploader": "Probe"}, {"set_name": "A Set"}, ["--set-date"]),
        ({"uploader": "Probe", "title": "Probe", "upload_date": "2026-05-03"}, {}, ["--set-date"]),
    ],
)
def test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag(page, flags, missing):
    with pytest.raises(CratekitError) as caught:
        set_playlist.words_for(_job_with(page), **flags)
    cause = caught.value.cause
    assert cause.reason == set_playlist.UNNAMED
    assert cause.detail["missing"] == missing
    assert list(cause.remediation.steps) == [f"pass {flag}" for flag in missing]


@pytest.mark.parametrize("given", ["May 2026", "2026-13", "2026-00", "2026-02-30"])
def test_a_set_date_that_is_not_a_month_is_refused_by_name(given):
    with pytest.raises(CratekitError) as caught:
        set_playlist.words_for(_job_with(PAGE), set_date=given)
    assert caught.value.cause.reason == set_playlist.UNNAMED
    assert caught.value.cause.remediation.remedy is Remedy.FIX_COMMAND_LINE


def test_a_page_date_that_is_not_a_date_names_no_month_and_the_flag_is_asked_for():
    with pytest.raises(CratekitError) as caught:
        set_playlist.words_for(_job_with({**PAGE, "upload_date": "20261300"}))
    assert caught.value.cause.detail["missing"] == ["--set-date"]


def test_a_job_with_upload_date_names_playlists_for_the_posted_day():
    """U136: upload_date 20260325 opens as 3_25_26, not the landing day."""
    words = set_playlist.SetWords("Public Service NYC", "Live at Signal", date(2026, 2, 1))
    day, warn = set_playlist.naming_day(page_upload_date="20260325", landing=date(2026, 10, 10))
    assert warn is None
    assert day == date(2026, 3, 25)
    assert set_playlist.playlist_name(words, on=day) == (
        "3_25_26 Public Service NYC Live at Signal 2-26"
    )
    assert batch_name.set_playlist_form(
        day, dj=words.dj, name=words.name, month=words.month
    ) == "3_25_26 Public Service NYC Live at Signal 2-26"


def test_a_job_without_upload_date_names_for_the_landing_day_and_warns():
    day, warn = set_playlist.naming_day(page_upload_date="", landing=date(2026, 10, 10))
    assert day == date(2026, 10, 10)
    assert warn is not None
    assert warn["code"] == set_playlist.POSTED_FALLBACK
    assert "10_10_26" in warn["message"]


def test_posted_flag_wins_over_the_page_upload_date():
    day, warn = set_playlist.naming_day(
        posted="2026-04-17", page_upload_date="20260325", landing=date(2026, 10, 10)
    )
    assert warn is None
    assert day == date(2026, 4, 17)
    words = set_playlist.SetWords("Probe", "Friday", date(2026, 4, 1))
    assert set_playlist.playlist_name(words, on=day) == "4_17_26 Probe Friday 4-26"


def test_a_backfill_a_week_later_recomputes_the_same_posted_name():
    """R-949 closes: the form takes the day as an argument, so today cannot twin it."""
    words = set_playlist.SetWords("Public Service NYC", "Live at Signal", date(2026, 2, 1))
    first, _ = set_playlist.naming_day(page_upload_date="20260325", landing=date(2026, 10, 10))
    later, _ = set_playlist.naming_day(page_upload_date="20260325", landing=date(2026, 10, 17))
    assert first == later == date(2026, 3, 25)
    assert set_playlist.playlist_name(words, on=first) == set_playlist.playlist_name(words, on=later)
    # The landing day alone would have twinned.
    assert set_playlist.playlist_name(words, on=date(2026, 10, 10)) != set_playlist.playlist_name(
        words, on=date(2026, 10, 17)
    )


def test_the_inbox_batch_name_is_unchanged_by_the_posted_day():
    """INBOX still ages by the landing day; U136 does not retarget batch_name.readable."""
    assert batch_name.is_default_shape("2026-10-10 Set")
    # The set playlist form is a different shape and lives beside readable.
    assert batch_name.set_day_word(date(2026, 3, 25)) == "3_25_26"
    assert not batch_name.is_default_shape("3_25_26 Public Service NYC Live at Signal 2-26")


def test_a_pinned_naming_day_keeps_a_posted_override_over_the_page():
    """apply_alone re-plans with on=made_on; a --posted override must survive."""
    words = set_playlist.SetWords("Probe", "Friday", date(2026, 4, 1))
    posted, _ = set_playlist.naming_day(
        posted="2026-04-17", page_upload_date="20260325", landing=date(2026, 10, 10)
    )
    assert posted == date(2026, 4, 17)
    # The page alone would prefer March 25; the pinned day wins.
    assert set_playlist.playlist_name(words, on=posted) == "4_17_26 Probe Friday 4-26"
    page_day, _ = set_playlist.naming_day(page_upload_date="20260325")
    assert page_day == date(2026, 3, 25)
    assert set_playlist.playlist_name(words, on=page_day) != set_playlist.playlist_name(
        words, on=posted
    )


@pytest.mark.parametrize("given", ["April 17", "2026-4-17", "2026-04", "2026-04-17T12:00:00"])
def test_a_posted_flag_that_is_not_a_day_is_refused_by_name(given):
    with pytest.raises(CratekitError) as caught:
        set_playlist.naming_day(posted=given, landing=date(2026, 10, 10))
    assert caught.value.cause.reason == set_playlist.UNNAMED
    assert caught.value.cause.remediation.remedy is Remedy.FIX_COMMAND_LINE


# ---------------------------------------------------------------------------
# The landing given --set
# ---------------------------------------------------------------------------


def test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order(
    native_library, silence
):
    cfg, root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("One", "Three", "Two"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["set playlist"] == NAME
    assert shown["set tracks"] == 3 and shown["set left out"] == 0
    assert shown["under"] == f"{FOLDER} (row {folder_id})"
    # The plan the person approved is the plan that was applied, set included.
    assert shown["digest"] == acted["data"]["digest"]

    ((playlist_id, parent, attribute, removed),) = _playlists_named(cfg, NAME)
    assert str(parent) == folder_id and int(attribute or 0) == 0 and not removed
    rows = _row_ids_by_name(cfg)
    # Owned and landed alike, in the order the set played them.
    assert _members(cfg, str(playlist_id)) == [rows["One"], "held-3", rows["Two"]]

    # The batch is as every landing makes it: the landed files only, under INBOX.
    ((batch_id, batch_parent, _a, _r),) = _playlists_named(cfg, BATCH)
    assert str(batch_parent) == root_id
    assert _members(cfg, str(batch_id)) == [rows["One"], rows["Two"]]
    assert _children(cfg, root_id) == [str(batch_id)]

    totals = acted["data"]["totals"]
    assert totals["memberships"] == 2, "the set's memberships are not the batch's"
    assert totals["set playlist tracks"] == 3 and totals["set playlist left out"] == 0
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert item["id"] == str(playlist_id) and item["count"] == 3 and item["added"] == 3
    assert item["folder"] == folder_id and item["folder_created"] is False
    codes = [w["code"] for w in acted["warnings"]]
    assert codes == [land_cli.AWAITING_ANALYSIS, land_cli.VOX_NOT_WRITTEN, set_playlist.WRITTEN]

    # The one record names both, and counts the set's memberships under the
    # folder's own id, apart from the intake tree's.
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.CLOSED
    assert record.detail[set_playlist.RECORD_KEY] == {
        "id": str(playlist_id),
        "name": NAME,
        "job": job_id,
        "folder": folder_id,
    }
    assert {change.tree: change.created for change in record.change.trees} == {
        INTAKE: 2,
        rb_writer.CONTENT_TABLE: 2,
        DECLARED.inspiration.id: 3,
    }
    assert record.sources[DECLARED.inspiration.id] == "committed"


def test_the_words_come_off_the_jobs_page_when_no_flag_is_given(native_library, silence):
    cfg, _root_id = native_library
    job_id = set_job(cfg, ("One",), page=PAGE)
    _stage(cfg, silence, "One")
    code, acted, _ = _two_acts(_land("--set", job_id))
    assert code == int(ExitCode.OK), acted
    assert _playlists_named(cfg, "5_03_26 Probe DJ Live at Probe 05.03.26 5-26")


def test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day(
    native_library, silence
):
    """U136: page upload_date wins over the landing day for the INSPIRATION name."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",), page=PAGE)
    _stage(cfg, silence, "One")
    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set playlist"] == POSTED_NAME
    assert _playlists_named(cfg, POSTED_NAME)
    assert _playlists_named(cfg, NAME) == []


def test_a_landing_honours_posted_on_a_pre_freeze_job(native_library, silence):
    """U136: intake land --set JOB --posted must reach plan_for_landing."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, acted, refused = _two_acts(
        _land("--set", job_id, *WORDS, "--posted", "2026-05-03")
    )
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set playlist"] == POSTED_NAME
    assert _playlists_named(cfg, POSTED_NAME)
    assert _playlists_named(cfg, NAME) == []


def test_posted_equal_to_landing_day_on_a_pageless_job_is_not_decision_stale(
    native_library, silence
):
    """U136: --posted equal to today must not flip posted_fallback on re-plan."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    code, acted, refused = _two_acts_approve(
        _inspiration(job_id, *WORDS, "--posted", "2026-10-09")
    )
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] != "error"
    assert refused["cause"]["detail"]["shown"]["set playlist"] == NAME
    assert _playlists_named(cfg, NAME)
    assert not any(w["code"] == set_playlist.POSTED_FALLBACK for w in acted["warnings"])


def test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name(
    native_library, silence, monkeypatch
):
    """Driven R-949: playlist pre-made under the posted name; a week on, one playlist."""
    cfg, _root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",), page=PAGE)
    _make_playlist(cfg, POSTED_NAME, under=folder_id)
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 16))
    code, acted, refused = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set playlist"] == POSTED_NAME
    assert len(_playlists_named(cfg, POSTED_NAME)) == 1
    assert _playlists_named(cfg, "10_16_26 Probe DJ Live at Probe 5-26") == []
    assert acted["data"]["totals"]["added"] == 1
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == POSTED_NAME]
    assert item.get("playlist_created") is False


def test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it(
    native_library, silence
):
    cfg, _root_id = native_library
    assert _root_folders(cfg, FOLDER) == []
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["under"] == f"{FOLDER}, created at the playlist root"
    ((folder_id,),) = _root_folders(cfg, FOLDER)
    ((_pid, parent, _a, _r),) = _playlists_named(cfg, NAME)
    assert str(parent) == str(folder_id)
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert item["folder_created"] is True


def test_a_landing_from_a_playlist_job_or_no_job_writes_no_set_playlist(native_library, silence):
    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _stage(cfg, silence, "One")
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    ((folder_id,),) = _root_folders(cfg, FOLDER)
    assert _children(cfg, str(folder_id)) == []
    assert "set playlist tracks" not in acted["data"]["totals"]
    (record,) = session.records(cfg)
    assert set_playlist.RECORD_KEY not in record.detail


def test_a_playlist_job_named_with_set_is_refused_before_anything_moves(native_library, silence):
    cfg, _root_id = native_library
    _stage(cfg, silence, "One")
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="intake.playlist",
            payload={intake_cli.SOURCE: "pl-1", intake_cli.TRACKS: {}},
            cfg=cfg,
            item_ids=(),
        )
    code, envelope = drive(_land("--set", job.job_id, *WORDS))
    assert envelope["cause"]["reason"] == "job-unknown", envelope
    assert code != int(ExitCode.DECISION_REQUIRED)
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


def test_a_set_the_page_and_the_flags_cannot_name_is_refused_before_the_gate(
    native_library, silence
):
    cfg, _root_id = native_library
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--set", job_id, "--dj", "Probe DJ"))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == set_playlist.UNNAMED
    assert envelope["cause"]["detail"]["missing"] == ["--set-name", "--set-date"]
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    assert session.records(cfg) == ()


def test_a_taxonomy_with_no_inspiration_folder_is_refused_by_name_before_the_gate(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    monkeypatch.setattr(active_taxonomy, "load", lambda _cfg: replace(DECLARED, inspiration=None))
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--set", job_id, *WORDS))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == set_playlist.FOLDER_UNDECLARED
    assert any("[inspiration]" in step for step in envelope["cause"]["remediation"]["steps"])
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    assert session.records(cfg) == ()


def test_two_root_folders_of_the_name_are_refused_rather_than_one_chosen(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--set", job_id, *WORDS))
    assert envelope["cause"]["reason"] == set_playlist.FOLDER_UNDECLARED, envelope
    assert envelope["cause"]["detail"]["count"] == 2


def test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One", "Four", "Two"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["set tracks"] == 2 and shown["set left out"] == 1
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["One"], rows["Two"]]
    (left,) = [w for w in acted["warnings"] if w["code"] == set_playlist.LEFT_OUT]
    assert "2. Probe - Four" in left["message"] and set_playlist.NOT_RESOLVED in left["message"]
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert item["left"] == [
        {"position": 2, "artist": "Probe", "title": "Four", "state": "missing", "why": set_playlist.NOT_RESOLVED}
    ]


def test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("Four",))
    _stage(cfg, silence, "One")
    code, acted, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert _playlists_named(cfg, NAME) == []
    codes = [w["code"] for w in acted["warnings"]]
    assert set_playlist.NOTHING in codes and set_playlist.LEFT_OUT in codes
    (record,) = session.records(cfg)
    assert set_playlist.RECORD_KEY not in record.detail


def test_a_landing_on_the_bridge_given_set_is_refused_by_name_before_anything_moves(
    acknowledged, silence
):
    """The one refusal both verbs make for a bridge tree, the landing told it
    can land without --set and backfill after the cutover."""
    cfg = acknowledged
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--set", "any-job", *WORDS))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == "tree-unconverged"
    steps = envelope["cause"]["remediation"]["steps"]
    assert any("without --set" in step for step in steps)
    assert any("tree cutover" in step for step in steps)
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


def test_a_word_flag_without_set_is_refused_rather_than_ignored(native_library, silence):
    cfg, _root_id = native_library
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--dj", "Probe DJ", "--set-date", "2026-05"))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert envelope["cause"]["detail"]["given"] == ["--dj", "--set-date"]
    assert "--set JOB" in envelope["cause"]["message"]
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


def test_no_beat_grid_tempo_or_rating_is_written_for_the_set_playlist(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three", "One"))
    _stage(cfg, silence, "One")
    before = {row[0]: row for row in _content_table(cfg)}
    code, acted, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    after = {row[0]: row for row in _content_table(cfg)}
    # The owned row is untouched to the byte; the landed row is the landing's
    # own, whose analysis columns the engine reads back empty and asserts.
    assert after["held-3"] == before["held-3"]
    assert set(after) - set(before) == {_row_ids_by_name(cfg)["One"]}
    for table in ("djmdBeatGrid", "djmdCue", "djmdHotCueBanklist"):
        found = _query(cfg, "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", table)
        if found:
            assert _query(cfg, f"SELECT COUNT(*) FROM {table}") == [(0,)]


# ---------------------------------------------------------------------------
# The backfill: crate intake inspiration
# ---------------------------------------------------------------------------


def test_the_backfill_over_a_landed_set_adds_the_playlist_and_nothing_to_inbox(
    native_library, silence
):
    cfg, root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("One", "Three", "Two"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")
    code, landed, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), landed
    inbox_before = _children(cfg, root_id)
    content_before = _content_table(cfg)

    code, acted, refused = _two_acts_approve(_inspiration(job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["set playlist"] == NAME and shown["set tracks"] == 3 and shown["set left out"] == 0
    assert shown["digest"] == acted["data"]["digest"]
    ((playlist_id, parent, _a, _r),) = _playlists_named(cfg, NAME)
    assert str(parent) == folder_id
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["One"], "held-3", rows["Two"]]
    assert acted["data"]["totals"] == {
        "count": 3,
        "members": 3,
        "left": 0,
        "added": 3,
        "read back": 3,
    }
    assert [i["action"] for i in acted["data"]["items"]] == ["add", "add", "add", "playlist"]
    assert [w["code"] for w in acted["warnings"]] == [
        set_playlist.POSTED_FALLBACK,
        set_playlist.WRITTEN,
    ]
    # Nothing under INBOX moved and no content row changed.
    assert _children(cfg, root_id) == inbox_before
    assert _content_table(cfg) == content_before
    records = [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]
    (record,) = records
    assert record.state is session.SessionState.CLOSED
    assert record.detail[set_playlist.RECORD_KEY]["id"] == str(playlist_id)
    assert {c.tree: c.created for c in record.change.trees} == {DECLARED.inspiration.id: 3}


def test_the_backfill_run_twice_on_one_day_adds_nothing_the_second_time(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, _landed, _ = _two_acts(_land())
    assert code == int(ExitCode.OK)
    code, first, _ = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    code, again, _ = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["added"] == 0 and again["data"]["totals"]["read back"] == 1
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)
    assert len(_members(cfg, str(playlist_id))) == 1


def test_the_backfill_over_a_set_with_nothing_owned_asks_and_then_writes_nothing(
    native_library, silence
):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("Four",))
    code, acted, _ = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _playlists_named(cfg, NAME) == []
    assert [w["code"] for w in acted["warnings"]] == [
        set_playlist.POSTED_FALLBACK,
        set_playlist.NOTHING,
        set_playlist.LEFT_OUT,
    ]
    assert not [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    _cut_over_intake(machine)
    job_id = set_job(machine, ("One",))
    code, envelope = drive(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.ACK_REQUIRED), envelope
    assert "gate" not in (envelope.get("cause") or {}).get("detail", {})


def test_the_backfill_on_the_bridge_is_refused_naming_the_cutover(acknowledged):
    code, envelope = drive(_inspiration("any-job", *WORDS))
    _refused_before_the_gate(acknowledged, code, envelope, "tree-unconverged")
    assert any("tree cutover" in step for step in envelope["cause"]["remediation"]["steps"])


def test_the_backfill_refuses_a_job_that_is_not_a_set_and_an_unfinished_one(native_library):
    cfg, _root_id = native_library
    code, envelope = drive(_inspiration("no-such-job", *WORDS))
    _refused_before_the_gate(cfg, code, envelope, "job-unknown")
    with jobs.open_store() as store:
        queued = jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload={intake_cli.SOURCE: "x", intake_cli.TRACKS: {"rc_a": {"artist": "P", "title": "A"}}},
            cfg=cfg,
            item_ids=("rc_a",),
        )
    code, envelope = drive(_inspiration(queued.job_id, *WORDS))
    _refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert envelope["cause"]["detail"]["state"] == "queued"


def test_a_taxonomy_with_no_inspiration_folder_refuses_the_backfill_by_name(
    native_library, monkeypatch
):
    cfg, _root_id = native_library
    monkeypatch.setattr(active_taxonomy, "load", lambda _cfg: replace(DECLARED, inspiration=None))
    job_id = set_job(cfg, ("One",))
    code, envelope = drive(_inspiration(job_id, *WORDS))
    _refused_before_the_gate(cfg, code, envelope, set_playlist.FOLDER_UNDECLARED)


def test_a_folder_that_went_between_the_plan_and_the_write_is_refused_as_stale(
    native_library, silence
):
    cfg, _root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, _landed, _ = _two_acts(_land())
    assert code == int(ExitCode.OK)
    verb = _inspiration(job_id, *WORDS)
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, APPROVE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (folder_id,))
    conn.commit()
    conn.close()
    code, acted = drive(["--run", run_id, *verb])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _playlists_named(cfg, NAME) == []


# ---------------------------------------------------------------------------
# What the hunt after the suite added: a guess, a moved collection, a gone folder
# ---------------------------------------------------------------------------


def test_a_row_that_resolves_only_to_a_different_version_is_not_guessed(native_library, silence):
    """The account playlists' rule (U113): a file that is only close, a different
    version, claims nothing. The set wants the original and staging holds the
    extended mix, so the batch lands the file and the set playlist leaves the
    row out, written for nobody rather than for a guess."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One (Extended Mix)")
    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set tracks"] == 0
    assert acted["data"]["totals"]["added"] == 1, "the batch did not land the file"
    assert _playlists_named(cfg, NAME) == []
    (left,) = [w for w in acted["warnings"] if w["code"] == set_playlist.LEFT_OUT]
    assert "1. Probe - One" in left["message"]


def test_a_collection_that_moved_between_the_plan_and_the_write_is_refused_as_stale(
    native_library, silence
):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    verb = _inspiration(job_id, *WORDS)
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, APPROVE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = 'held-3'")
    conn.commit()
    conn.close()
    code, acted = drive(["--run", run_id, *verb])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _playlists_named(cfg, NAME) == []
    assert not [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]


def test_a_landing_whose_folder_went_between_the_two_acts_moves_nothing(native_library, silence):
    """The acting drive plans again on the write handle and the gate compares
    the digest, so a folder rekordbox removed after the approval is a changed
    plan: refused before the first move, the files still in staging."""
    cfg, _root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    verb = _land("--set", job_id, *WORDS)
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    gate = refused["cause"]["detail"]["gate"]
    decided, _ = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (folder_id,))
    conn.commit()
    conn.close()
    code, acted = drive(["--run", run_id, *verb])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert "has since changed" in acted["cause"]["message"]
    assert _playlists_named(cfg, NAME) == []
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent WHERE FolderPath LIKE ?", f"%{BATCH}%") == [(0,)]


# ---------------------------------------------------------------------------
# What the review added: answers read back, nothing offered, a pair of rows, a gap filled
# ---------------------------------------------------------------------------


def _offered_item(cfg: config.Config, job_id: str, title: str) -> tuple[str, str]:
    """The review item the worker offered for ``title`` and its first option."""
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        reports = set_playlist.reports_of(store, job)
    (report,) = [r for r in reports if r["track"]["title"] == title]
    assert report["state"] == "offered", report
    with review.open_store(cfg) as items:
        held = review.find(items, report["review_item"])
    assert held is not None
    return held.item_id, held.options[0].option_id


def _unresolved(cfg: config.Config) -> int:
    with review.open_store(cfg) as items:
        return review.count_unresolved(items)


def test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing(
    native_library, silence
):
    """A row the report called offered was never downloaded: the person
    answered that the library's other version is the one, so it is owned and
    the landing reads that answer back rather than leaving it out."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "One (Extended Mix)", content_id="held-1x")
    job_id = set_job(cfg, ("One", "Two"))
    item_id, option = _offered_item(cfg, job_id, "One")
    code, answered = drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option])
    assert code == int(ExitCode.OK), answered
    _stage(cfg, silence, "Two")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set tracks"] == 2
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == ["held-1x", rows["Two"]]


def test_an_unanswered_question_is_left_out_and_the_plan_offers_nothing(native_library, silence):
    """The plan reads the worker's item and writes none of its own: a question
    nobody answered leaves the row out, and the review queue is as it was
    before the plan, before the gate and after an abort alike."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "One (Extended Mix)", content_id="held-1x")
    job_id = set_job(cfg, ("One",))
    _offered_item(cfg, job_id, "One")
    before = _unresolved(cfg)
    assert before == 1

    code, refused = drive(_inspiration(job_id, *WORDS))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["set tracks"] == 0 and shown["set left out"] == 1
    assert _unresolved(cfg) == before
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, APPROVE, "abort", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    code, acted = drive(["--run", run_id, *_inspiration(job_id, *WORDS)])
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    assert _unresolved(cfg) == before
    assert _playlists_named(cfg, NAME) == []


def test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked(
    native_library, silence
):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    path = _owned(cfg, silence, "Three", content_id="held-3a")
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, ContentLink, rb_local_deleted, "
        "created_at, updated_at) VALUES ('held-3b', 'Three', ?, ?, 0, '2026-01-01', "
        "'2026-01-01')",
        # rekordbox's value, so the library's rows still hold a majority (U126).
        (str(path), LIBRARY_LINK),
    )
    conn.commit()
    conn.close()
    job_id = set_job(cfg, ("Three", "One"))
    _stage(cfg, silence, "One")

    code, acted, _ = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)
    assert _members(cfg, str(playlist_id)) == [_row_ids_by_name(cfg)["One"]]
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert [one["why"] for one in item["left"]] == [set_playlist.AMBIGUOUS_ROWS]


def test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write(native_library, silence):
    """The playlist is found by its name and rekordbox appends what it lacked,
    so the track that became owned since sits last; every asked id is read
    back live and the write is reported as what it was, one track added."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "One", content_id="held-1")
    _owned(cfg, silence, "Two", content_id="held-2")
    job_id = set_job(cfg, ("One", "Three", "Two"))
    code, first, _ = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)
    assert _members(cfg, str(playlist_id)) == ["held-1", "held-2"]

    _owned(cfg, silence, "Three", content_id="held-3")
    code, again, _ = _two_acts_approve(_inspiration(job_id, *WORDS))

    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["added"] == 1 and again["data"]["totals"]["read back"] == 3
    assert _members(cfg, str(playlist_id)) == ["held-1", "held-2", "held-3"]
    # The second write finds the recorded playlist, so the posted fallback is not re-warned.
    assert [w["code"] for w in again["warnings"]] == [set_playlist.WRITTEN]


# ---------------------------------------------------------------------------
# What the table added: an order that is not alphabetical, and the engine's own stale checks
# ---------------------------------------------------------------------------


def test_members_keep_the_sets_order_when_it_is_not_alphabetical(native_library, silence):
    """The first table's order row was inert: every set until now played its
    tracks in title order, so a sort by title changed nothing. This set does not."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Two", "One", "Three"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")
    code, acted, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["Two"], rows["One"], "held-3"]


def _backfill_inputs(cfg: config.Config, job_id: str):
    declared = active_taxonomy.load(cfg)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        reports = set_playlist.reports_of(store, job)
    words = set_playlist.words_for(job, dj="Probe DJ", set_name="Live at Probe", set_date="2026-05")
    return declared, job, words, reports


def test_the_engine_refuses_a_plan_whose_collection_moved_even_with_no_gate_in_front(
    native_library, silence
):
    """The gate re-plans on every drive and catches this first, so the engine's
    own re-plan on the write handle is reached only by a caller with no gate.
    Driven here as that caller, since a guard held by another guard is a
    guard nothing covers."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    declared, job, words, reports = _backfill_inputs(cfg, job_id)
    plan = inspiration_cli.planned(cfg, declared, job, words, reports)
    assert [one.content_id for one in plan.members] == ["held-3"]
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = 'held-3'")
    conn.commit()
    conn.close()
    with pytest.raises(CratekitError) as caught:
        inspiration_cli.written(cfg, declared, plan, job, words, reports)
    assert caught.value.cause.reason == "decision-stale"
    assert _playlists_named(cfg, NAME) == []


def test_the_engine_refuses_a_folder_removed_after_the_plan_even_with_no_gate_in_front(
    native_library, silence
):
    cfg, _root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    declared, job, words, reports = _backfill_inputs(cfg, job_id)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        plan = set_playlist.plan_for_backfill(cfg, db, declared, job, words, reports)
        assert plan.folder_id == folder_id
        row = db.get_playlist(ID=folder_id)
        setattr(row, rb_writer.SOFT_DELETE_COLUMN, 1)
        db.session.flush()
        with pytest.raises(CratekitError) as caught:
            set_playlist.write_members(db, plan)
        assert caught.value.cause.reason == "decision-stale"
        db.session.rollback()
    finally:
        rb_writer.close_db(db)
    assert _playlists_named(cfg, NAME) == []


# ---------------------------------------------------------------------------
# What the watcher's review added
# ---------------------------------------------------------------------------


def _soft_delete_playlist(cfg: config.Config, playlist_id: str) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (playlist_id,))
    conn.commit()
    conn.close()


def _make_playlist(cfg: config.Config, name: str, *, under: str) -> str:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        row = handle.create_playlist(name, parent=handle.get_playlist(ID=under))
        handle.session.commit()
        return str(row.ID)
    finally:
        rb_writer.close_db(handle)


def test_two_landings_of_one_set_on_two_days_make_one_playlist(native_library, silence, monkeypatch):
    """The second landing reads the first's session record, adds to the playlist
    it made and keeps its name, so a set landed in two parts is one playlist."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One", "Two"))
    _stage(cfg, silence, "One")
    code, first, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    ((playlist_id, *_rest),) = _playlists_named(cfg, NAME)

    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    _stage(cfg, silence, "Two")
    verb = ["intake", "land", "--name", "2026-10-10 Set", "--set", job_id, *WORDS]
    code, second, refused = _two_acts(verb)

    assert code == int(ExitCode.OK), second
    assert refused["cause"]["detail"]["shown"]["playlist"].startswith("adds to the playlist")
    assert _playlists_named(cfg, "10_10_26 Probe DJ Live at Probe 5-26") == []
    assert len(_playlists_named(cfg, NAME)) == 1
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["One"], rows["Two"]]
    (item,) = [i for i in second["data"]["items"] if i.get("playlist") == NAME]
    assert item["id"] == str(playlist_id) and item["added"] == 1 and item["playlist_created"] is False


def test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made(
    native_library, silence
):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, first, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    ((removed_id, *_rest),) = _playlists_named(cfg, NAME)
    _soft_delete_playlist(cfg, str(removed_id))

    code, acted, refused = _two_acts_approve(_inspiration(job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["playlist"].startswith("found live")
    live = [row for row in _playlists_named(cfg, NAME) if not row[3]]
    ((live_id, *_r),) = live
    assert str(live_id) != str(removed_id)
    assert _members(cfg, str(live_id)) == [_row_ids_by_name(cfg)["One"]]
    assert _members(cfg, str(removed_id)) == [_row_ids_by_name(cfg)["One"]], "the removed one kept its own"


def test_a_removed_namesake_under_the_folder_is_not_written_into(native_library, silence):
    cfg, _root_id = native_library
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    removed_id = _make_playlist(cfg, NAME, under=folder_id)
    _soft_delete_playlist(cfg, removed_id)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))

    code, acted, _ = _two_acts_approve(_inspiration(job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert _members(cfg, removed_id) == []
    live = [row for row in _playlists_named(cfg, NAME) if not row[3]]
    ((live_id, parent, _a, _r),) = live
    assert str(parent) == folder_id and str(live_id) != removed_id
    assert _members(cfg, str(live_id)) == ["held-3"]
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert item["playlist_created"] is True


def test_when_every_landed_members_file_is_refused_the_left_list_names_them(
    native_library, silence
):
    """The write's own answer carries the members whose files did not land,
    not only the plan's left rows, so the count is not zero over the set. A
    landing where every file is refused refuses as a whole before the write,
    so the file outside the set is what lets the batch land here."""
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One", "Two"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")
    _stage(cfg, silence, "Extra")
    occupied = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    occupied.mkdir(parents=True)
    (occupied / "One.flac").write_bytes(b"taken")
    (occupied / "Two.flac").write_bytes(b"taken")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set tracks"] == 2
    assert acted["data"]["totals"]["landed"] == 1 and acted["data"]["totals"]["refused"] == 2
    assert acted["data"]["totals"]["set playlist left out"] == 2
    assert acted["data"]["totals"]["set playlist tracks"] == 0
    assert _playlists_named(cfg, NAME) == []
    (nothing,) = [w for w in acted["warnings"] if w["code"] == set_playlist.NOTHING]
    assert "2 track(s) are listed as left out" in nothing["message"]
    (left,) = [w for w in acted["warnings"] if w["code"] == set_playlist.LEFT_OUT]
    assert "1. Probe - One (its file did not land)" in left["message"]
    assert "2. Probe - Two (its file did not land)" in left["message"]
    (record,) = session.records(cfg)
    assert set_playlist.RECORD_KEY not in record.detail


def test_two_rows_of_the_set_resolving_to_one_track_are_one_member(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    tracks = {
        "rc_a": {"artist": "Probe", "title": "Three", "origin": match.TEXT, "spelled": "Probe - Three"},
        "rc_b": {
            "artist": "Probe",
            "title": "Three",
            "isrc": "X1",
            "origin": match.TEXT,
            "spelled": "Probe - Three",
        },
    }
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload={intake_cli.SOURCE: "x", intake_cli.TRACKS: tracks, intake_cli.PAGE: {}},
            cfg=cfg,
            item_ids=tuple(tracks),
        )
    code, resumed = drive(cli_jobs.argv_for(job))
    assert code == int(ExitCode.OK), resumed

    code, acted, refused = _two_acts_approve(_inspiration(job.job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["set tracks"] == 2, "both positions are shown"
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert item["count"] == 1 and item["added"] == 1
    assert acted["data"]["totals"]["read back"] == 1
    assert _members(cfg, item["id"]) == ["held-3"]


def test_a_rerun_that_adds_nothing_records_no_commit(native_library, silence):
    cfg, _root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    code, first, _ = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    code, again, _ = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["added"] == 0
    # Two records written inside one second sort either way by identifier,
    # so each is found by what it holds rather than by its place.
    records = [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]
    assert len(records) == 2
    (first_record,) = [r for r in records if r.sources]
    (second_record,) = [r for r in records if not r.sources]
    assert first_record.sources == {DECLARED.inspiration.id: "committed"}
    assert second_record.change.trees == ()
    assert set_playlist.RECORD_KEY not in second_record.detail


def test_the_backfill_creates_the_declared_folder_at_the_root_when_the_library_lacks_it(
    native_library, silence
):
    cfg, _root_id = native_library
    assert _root_folders(cfg, FOLDER) == []
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    code, acted, refused = _two_acts_approve(_inspiration(job_id, *WORDS))
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["under"] == f"{FOLDER}, created at the playlist root"
    ((folder_id,),) = _root_folders(cfg, FOLDER)
    ((_pid, parent, _a, _r),) = _playlists_named(cfg, NAME)
    assert str(parent) == str(folder_id)
    (item,) = [i for i in acted["data"]["items"] if i.get("playlist") == NAME]
    assert item["folder_created"] is True and item["playlist_created"] is True
    (record,) = [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]
    assert record.detail[set_playlist.RECORD_KEY]["folder"] == str(folder_id)


# ---------------------------------------------------------------------------
# U129: the landing archives the account playlist (driven)
# ---------------------------------------------------------------------------


@pytest.fixture
def account_on_native(native_library, monkeypatch):
    """Native landing library with the outbound account bound for archive writes."""
    from cratekit.core import secrets
    from cratekit.label import catalogue
    from tests import outbound_fakes
    from tests.label_fakes import FakeCatalogue, catalogue_factory
    from tests.test_outbound_workers import bind as bind_account

    cfg, root_id = native_library
    # Doctor's credential.provider check reads the keychain before the verb;
    # the account and catalogue seams are substituted for the writes themselves.
    secrets.set_json(
        secrets.Credential.PROVIDER_SESSION,
        {"access_token": "test-token", "refresh_token": "test-refresh"},
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(FakeCatalogue(searches={})))
    held = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, held)
    return cfg, root_id, held


def _record_account_set(cfg, held, name: str, *, year: str = "2026") -> str:
    """Record a set playlist on the ledger and create it on the fake account."""
    from cratekit.modules.outbound import ledger

    remote_id, _created = ledger.reserve_set_playlist(
        cfg, name, year, lambda: held.create_playlist(name)
    )
    return remote_id


def _freeze_name(job_id: str, name: str) -> None:
    """Put the INSPIRATION name on a succeeded set job the way intake set freezes it."""
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        payload = dict(job.payload)
        payload[intake_cli.PLAYLIST_NAME] = name
        with store.immediate() as conn:
            import json as _json

            conn.execute(
                "UPDATE jobs SET payload = ? WHERE job_id = ?",
                (_json.dumps(payload), job_id),
            )


def test_a_landing_archives_the_account_playlist_with_prefix_and_year_folder(
    account_on_native, silence
):
    cfg, _root_id, held = account_on_native
    cutover_fixtures.add_folder(cfg, FOLDER)
    remote_id = _record_account_set(cfg, held, NAME)
    job_id = set_job(cfg, ("One",), page=PAGE)
    _freeze_name(job_id, NAME)
    _stage(cfg, silence, "One")

    code, acted, _refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert any(
        pid == remote_id and title.startswith("DOWNLOADED ") for pid, title in held.renamed
    ), held.renamed
    assert "2026" in held.folders_created or any(
        name == "2026" for name in held.folder_names.values()
    ), held.folders_created
    assert not any(w["code"] == land_cli.LAND_ARCHIVE_FAILED for w in acted["warnings"])


def test_a_landing_archive_failure_is_a_warning_on_the_envelope(
    account_on_native, silence, monkeypatch
):
    cfg, _root_id, held = account_on_native
    cutover_fixtures.add_folder(cfg, FOLDER)
    _record_account_set(cfg, held, NAME)
    job_id = set_job(cfg, ("One",), page=PAGE)
    _freeze_name(job_id, NAME)
    _stage(cfg, silence, "One")

    from cratekit.core.cause import refuse
    from cratekit.core.exit_codes import Remedy
    from cratekit.export import set_cli

    def boom(_cfg, _archived):
        raise refuse(
            "unavailable-transient",
            "the account could not be reached",
            remedy=Remedy.RETRY_LATER,
            origin=("test",),
        )

    monkeypatch.setattr(set_cli, "apply_archive", boom)

    code, acted, _refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert any(w["code"] == land_cli.LAND_ARCHIVE_FAILED for w in acted["warnings"])
    assert any("could not finish after the landing wrote" in w["message"] for w in acted["warnings"])
    assert held.renamed == []


def test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope(
    account_on_native, silence, monkeypatch
):
    cfg, _root_id, held = account_on_native
    cutover_fixtures.add_folder(cfg, FOLDER)
    _record_account_set(cfg, held, NAME)
    job_id = set_job(cfg, ("One",), page=PAGE)
    _freeze_name(job_id, NAME)
    _stage(cfg, silence, "One")

    from cratekit.export import set_cli

    archived_holder = {}

    real_plan = land_cli._plan_set_archive

    def capture(cfg_arg, **kwargs):
        planned = real_plan(cfg_arg, **kwargs)
        archived_holder["planned"] = planned
        return planned

    monkeypatch.setattr(land_cli, "_plan_set_archive", capture)

    def soft(_cfg, archived):
        return (
            archived.payload,
            [
                {
                    "code": "export-archive-changed-since-plan",
                    "message": f"{NAME} was retitled by somebody, so it was not renamed",
                }
            ],
            False,
        )

    monkeypatch.setattr(set_cli, "apply_archive", soft)

    code, acted, _refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert archived_holder.get("planned") is not None
    assert any(w["code"] == "export-archive-changed-since-plan" for w in acted["warnings"])
    assert any("not renamed" in w["message"] for w in acted["warnings"])
    assert held.renamed == []


def test_export_set_backfill_lists_inspiration_playlists_from_the_disposable_database(
    account_on_native, monkeypatch
):
    """Drive ``_inspiration_playlists`` against the disposable DB, never a stub."""
    from cratekit.acquire import match
    from cratekit.core import rb_writer
    from cratekit.export import set_cli
    from cratekit.modules.outbound import ledger

    cfg, _root_id, held = account_on_native
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    names = [
        "10_09_26 Public Service NYC Live at Vonking 5-26",
        "10_10_26 Public Service NYC Live at Signal 5-26",
    ]
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        parent = handle.get_playlist(ID=folder_id)
        for name in names:
            handle.create_playlist(name, parent=parent)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    # Succeeded set jobs whose frozen names match the playlists above.
    from tests.test_u129_set_account_playlist import _succeeded_set_job

    _succeeded_set_job(cfg, names[0], created="2026-10-09T15:00:00+00:00")
    _succeeded_set_job(cfg, names[1], created="2026-10-10T15:00:00+00:00")

    wanted = (match.Wanted(artist="Probe", title="One", origin=match.TEXT),)
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)

    listed = set_cli._inspiration_playlists(cfg)
    assert [name for name, _pid in listed] == names

    code, refused = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    message = json.dumps(refused)
    assert names[0] in message and names[1] in message
    assert held.created == []
    assert "export-set-backfill-no-job" not in message
    assert ledger.set_playlist_names(cfg) == ()
