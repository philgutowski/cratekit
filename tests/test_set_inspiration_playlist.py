"""U121: a set intake leaves a permanent playlist of the set under INSPIRATION.

A set job is queued as ``intake set`` queues one and run, then landed with
``--set`` on the disposable database, or backfilled after a landing. D1 applies.
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
from cratekit.core import active_taxonomy, config, jobs, rb_writer, review, session, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.export import set_cli
from cratekit.intake import batch_name, inspiration_cli, land_cli, native, set_playlist
from cratekit.intake import cli as intake_cli
from cratekit.modules.outbound import ledger
from cratekit.sync import mark_record
from tests import cutover_fixtures
from tests import test_intake_land_account_playlists_native as account_native
from tests import test_intake_land_native as land_native
from tests._sync_builders import exited
from tests.cli_drive import drive
from tests.test_intake_land_account_playlists_native import _cut_over, _machine, _templated
from tests.test_intake_land_native import (
    DECLARED,
    GATE,
    INTAKE,
    LIBRARY_LINK,
    _cut_over_intake,
    _members,
    _music,
    _query,
    _two_acts,
)

# The native landing suite's fixtures, bound so pytest finds them here.
_platform_seams = land_native._platform_seams
_release_process_locks = land_native._release_process_locks
acknowledged, library = land_native.acknowledged, land_native.library
silence = account_native.silence

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
    """The native landing suite's machine on the FULL profile, which carries ``intake set``."""
    return _machine(library, monkeypatch, profile={"name": "full"})


@pytest.fixture
def native_library(acknowledged):
    """The acknowledged machine with its intake tree cut over. Answers (cfg, root id)."""
    return _cut_over(acknowledged)


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


# Fixtures: files, rows and a finished set job


def _tagged(path: Path, silence: Path, title: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    return path


def _stage(cfg: config.Config, silence: Path, title: str) -> Path:
    return _tagged(Path(cfg.paths.download_staging) / f"{title}.flac", silence, title)


def _staged(cfg: config.Config, silence: Path, *titles: str) -> None:
    for title in titles:
        _stage(cfg, silence, title)


def _owned(cfg: config.Config, silence: Path, title: str, *, content_id: str) -> Path:
    """A file the library holds under its own folder, with the collection row rekordbox gave it."""
    path = _tagged(Path(cfg.library.root) / cfg.library.music_dir / "Owned" / f"{title}.flac", silence, title)
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES (?, ?, ?, 0, '2026-01-01', '2026-01-01')",
        content_id,
        title,
        str(path),
    )
    return path


def _queued(cfg: config.Config, tracks: dict, **payload) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload={intake_cli.TRACKS: tracks, **payload},
            cfg=cfg,
            item_ids=tuple(tracks),
        )


def _run(job: jobs.Job) -> str:
    resumed = exited(drive(cli_jobs.argv_for(job)))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    return job.job_id


def _track(title: str, **more) -> dict:
    return {"artist": "Probe", "title": title, **more, "origin": match.TEXT, "spelled": f"Probe - {title}"}


def set_job(cfg: config.Config, titles: tuple[str, ...], *, page: dict | None = None) -> str:
    """One set job over ``titles`` in that order, queued as ``intake set`` queues one and run."""
    return _run(
        _queued(
            cfg,
            {f"rc_{title}": _track(title) for title in titles},
            **{
                intake_cli.SOURCE: "https://example.invalid/a-set",
                intake_cli.CALLS: len(titles),
                intake_cli.UNREACHED: 0,
                intake_cli.PARTS: 1,
                intake_cli.PAGE: dict(page or {}),
            },
        )
    )


def _land(*extra: str) -> list[str]:
    return ["intake", "land", "--name", BATCH, *extra]


def _inspiration(job_id: str, *extra: str) -> list[str]:
    return ["intake", "inspiration", "--job", job_id, *extra]


def _decided(verb: list[str], gate: str = APPROVE, answer: str = "apply") -> dict:
    """The first act refused at the gate and the person's answer recorded: its refusal."""
    refused = exited(drive(verb), ExitCode.DECISION_REQUIRED)
    exited(drive(["run", "decide", refused["run_id"], gate, answer, "--actor", "a-person"]))
    return refused


def _two_acts_approve(verb: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against the backfill's explicit gate, then the acting drive."""
    refused = _decided(verb)
    detail = refused["cause"]["detail"]
    assert detail["gate"] == APPROVE and detail["explicit"] is True
    code, acted = drive(["--run", refused["run_id"], *verb])
    return code, acted, refused


def _ok(verb: list[str], acts=_two_acts) -> tuple[dict, dict]:
    """The verb's two acts, applied without a refusal: its envelope and what its gate showed."""
    code, acted, refused = acts(verb)
    assert code == int(ExitCode.OK), acted
    return acted, refused["cause"]["detail"]["shown"]


def _backfilled(job_id: str, *extra: str) -> tuple[dict, dict]:
    return _ok(_inspiration(job_id, *WORDS, *extra), _two_acts_approve)


def _row_ids_by_name(cfg: config.Config) -> dict[str, str]:
    rows = _query(cfg, "SELECT ID, FolderPath FROM djmdContent WHERE rb_local_deleted = 0")
    return {Path(str(folder)).stem: str(content_id) for content_id, folder in rows}


def _playlists_named(cfg: config.Config, name: str) -> list[tuple]:
    return _query(
        cfg,
        "SELECT ID, ParentID, Attribute, rb_local_deleted FROM djmdPlaylist WHERE Name = ?",
        name,
    )


def _under_parent(cfg: config.Config, name: str, parent_id: str) -> list[tuple]:
    """Playlists of ``name`` parented to ``parent_id`` (INBOX or INSPIRATION)."""
    return [row for row in _playlists_named(cfg, name) if str(row[1]) == str(parent_id)]


def _under_folder(cfg: config.Config, name: str = NAME) -> list[tuple]:
    return _under_parent(cfg, name, _inspiration_folder_id(cfg))


def _inspiration_folder_id(cfg: config.Config) -> str:
    ((folder_id,),) = _root_folders(cfg, FOLDER)
    return str(folder_id)


def _root_folders(cfg: config.Config, name: str) -> list[tuple]:
    return _query(
        cfg,
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 AND "
        "(ParentID IS NULL OR ParentID IN ('', '0', 'root', 'None'))",
        name,
    )


def _children(cfg: config.Config, parent_id: str) -> list[str]:
    rows = _query(
        cfg, "SELECT ID FROM djmdPlaylist WHERE ParentID = ? AND rb_local_deleted = 0", parent_id
    )
    return [str(row[0]) for row in rows]


def _content_table(cfg: config.Config) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdContent ORDER BY ID")


def _sql(cfg: config.Config, statement: str, *args: object) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(statement, args)
    conn.commit()
    conn.close()


def _with_folder(native_library) -> config.Config:
    """The fresh native library with the INSPIRATION folder made at its root."""
    cfg, _root_id = native_library
    _templated("inspiration", cfg, lambda: cutover_fixtures.add_folder(cfg, FOLDER))
    return cfg


def _set_item(acted: dict, name: str = NAME) -> dict:
    """The landing's or the backfill's item for the set playlist written."""
    (item,) = [
        i for i in acted["data"]["items"] if i.get("playlist") == name and "playlist_created" in i
    ]
    return item


def _set_playlist_id(cfg: config.Config) -> str:
    ((playlist_id, *_rest),) = _under_folder(cfg)
    return playlist_id


def _warned(acted: dict, code: str) -> list[dict]:
    return [w for w in acted["warnings"] if w["code"] == code]


def _set_records(cfg: config.Config) -> list:
    return [r for r in session.records(cfg) if r.workflow == set_playlist.WORKFLOW]


def _still_staged(cfg: config.Config, title: str = "One") -> bool:
    return (Path(cfg.paths.download_staging) / f"{title}.flac").is_file()


def _refused_before_the_gate(cfg: config.Config, code: int, envelope: dict, reason: str) -> None:
    assert code != int(ExitCode.OK) and code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == reason, envelope
    assert not _set_records(cfg)


# The name


def test_the_name_is_the_source_systems_form_to_the_character():
    named = [
        # The folder's own examples: month without a leading zero, day with one.
        (("Public Service NYC", "Live at Vonking", date(2026, 5, 1)), date(2026, 10, 9)),
        (("oshe", "GOATCHELLA Radio Mix", date(2026, 4, 1)), date(2026, 5, 28)),
        (("Pepofit", "PEPOFIT LIB JUNKYARD", date(2026, 5, 1)), date(2026, 6, 16)),
        # December and a two digit month in the set's half.
        (("A", "B", date(2025, 12, 1)), date(2026, 1, 3)),
    ]
    assert [set_playlist.playlist_name(set_playlist.SetWords(*w), on=on) for w, on in named] == [
        "10_09_26 Public Service NYC Live at Vonking 5-26",
        "5_28_26 oshe GOATCHELLA Radio Mix 4-26",
        "6_16_26 Pepofit PEPOFIT LIB JUNKYARD 5-26",
        "1_03_26 A B 12-25",
    ]


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
        # A page date that is not a date names no month, and the flag is asked for.
        ({**PAGE, "upload_date": "20261300"}, {}, ["--set-date"]),
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


def test_the_naming_day_is_the_posted_flag_then_the_page_then_the_landing_day():
    """U136: the page's upload day names the set whatever day it lands (R-949), the flag wins.

    INBOX still ages by the landing day, so the batch name keeps its own shape.
    """
    words = set_playlist.SetWords("Public Service NYC", "Live at Signal", date(2026, 2, 1))
    named = "3_25_26 Public Service NYC Live at Signal 2-26"
    for landing in (date(2026, 10, 10), date(2026, 10, 17), None):
        assert set_playlist.naming_day(page_upload_date="20260325", landing=landing) == (
            date(2026, 3, 25),
            None,
        )
    assert set_playlist.playlist_name(words, on=date(2026, 3, 25)) == named
    assert (
        batch_name.set_playlist_form(
            date(2026, 3, 25), dj=words.dj, name=words.name, month=words.month
        )
        == named
    )
    # The landing day alone would have twinned.
    assert set_playlist.playlist_name(words, on=date(2026, 10, 10)) != set_playlist.playlist_name(
        words, on=date(2026, 10, 17)
    )
    day, warn = set_playlist.naming_day(
        posted="2026-04-17", page_upload_date="20260325", landing=date(2026, 10, 10)
    )
    assert (day, warn) == (date(2026, 4, 17), None)
    friday = set_playlist.SetWords("Probe", "Friday", date(2026, 4, 1))
    assert set_playlist.playlist_name(friday, on=day) == "4_17_26 Probe Friday 4-26"
    day, warn = set_playlist.naming_day(page_upload_date="", landing=date(2026, 10, 10))
    assert day == date(2026, 10, 10)
    assert warn["code"] == set_playlist.POSTED_FALLBACK and "10_10_26" in warn["message"]
    assert batch_name.is_default_shape("2026-10-10 Set")
    assert batch_name.set_day_word(date(2026, 3, 25)) == "3_25_26"
    assert not batch_name.is_default_shape(named)


@pytest.mark.parametrize("given", ["April 17", "2026-4-17", "2026-04", "2026-04-17T12:00:00"])
def test_a_posted_flag_that_is_not_a_day_is_refused_by_name(given):
    with pytest.raises(CratekitError) as caught:
        set_playlist.naming_day(posted=given, landing=date(2026, 10, 10))
    assert caught.value.cause.reason == set_playlist.UNNAMED
    assert caught.value.cause.remediation.remedy is Remedy.FIX_COMMAND_LINE


# The landing given --set


def test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order(
    native_library, silence
):
    """In the set's order, not the titles'; the owned row is untouched to the byte (no grid)."""
    cfg, root_id = native_library
    folder_id = _inspiration_folder_id(_with_folder(native_library))
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Two", "One", "Three"))
    _staged(cfg, silence, "One", "Two")
    before = {row[0]: row for row in _content_table(cfg)}
    acted, shown = _ok(_land("--set", job_id, *WORDS))
    assert shown["set playlist"] == NAME
    assert shown["set tracks"] == 3 and shown["set left out"] == 0
    assert shown["under"] == f"{FOLDER} (row {folder_id})"
    # The plan the person approved is the plan that was applied, set included.
    assert shown["digest"] == acted["data"]["digest"]
    ((playlist_id, parent, attribute, removed),) = _under_parent(cfg, NAME, folder_id)
    assert str(parent) == folder_id and int(attribute or 0) == 0 and not removed
    rows = _row_ids_by_name(cfg)
    # Owned and landed alike, in the order the set played them.
    assert _members(cfg, str(playlist_id)) == [rows["Two"], rows["One"], "held-3"]
    # The INBOX playlist is named for the set (U135), holding the landed files only.
    ((batch_id, batch_parent, _a, _r),) = _under_parent(cfg, NAME, root_id)
    assert str(batch_parent) == root_id
    assert _members(cfg, str(batch_id)) == [rows["Two"], rows["One"]]
    # And INBOX / Analyze (U166), which holds every row the landing made.
    ((analyze_id, _p, _a, _r),) = _under_parent(cfg, native.ANALYZE, root_id)
    assert sorted(_children(cfg, root_id)) == sorted([str(batch_id), str(analyze_id)])
    assert _members(cfg, str(analyze_id)) == [rows["One"], rows["Two"]]
    totals = acted["data"]["totals"]
    assert totals["memberships"] == 2, "the set's memberships are not the batch's"
    assert totals["set playlist tracks"] == 3 and totals["set playlist left out"] == 0
    item = _set_item(acted)
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
    # U166: the batch's two memberships and INBOX / Analyze's two.
    assert {change.tree: change.created for change in record.change.trees} == {
        INTAKE: 4,
        rb_writer.CONTENT_TABLE: 2,
        DECLARED.inspiration.id: 3,
    }
    assert record.sources[DECLARED.inspiration.id] == "committed"
    after = {row[0]: row for row in _content_table(cfg)}
    assert after["held-3"] == before["held-3"]
    assert set(after) - set(before) == {rows["One"], rows["Two"]}
    for table in ("djmdBeatGrid", "djmdCue", "djmdHotCueBanklist"):
        found = _query(cfg, "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", table)
        if found:
            assert _query(cfg, f"SELECT COUNT(*) FROM {table}") == [(0,)]


@pytest.mark.parametrize(
    ("page", "posted"), [(PAGE, ()), (None, ("--posted", "2026-05-03"))], ids=["page", "flag"]
)
def test_a_landing_names_the_playlist_for_the_posted_day(native_library, silence, page, posted):
    """U136: the page's upload_date, or ``--posted`` on a pre freeze job, wins over the landing day."""
    cfg, root_id = native_library
    _with_folder(native_library)
    job_id = set_job(cfg, ("One",), page=page)
    _stage(cfg, silence, "One")
    _acted, shown = _ok(_land("--set", job_id, *WORDS, *posted))
    assert shown["set playlist"] == POSTED_NAME
    assert _under_folder(cfg, POSTED_NAME)
    assert _under_folder(cfg) == []
    # The INBOX batch keeps the landing day, named for the set since U135.
    assert _under_parent(cfg, NAME, root_id)


def test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning(
    native_library, silence
):
    """U136: a job queued since U129 keeps its frozen name over ``--posted``, said once."""
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("One",), page=PAGE)
    _freeze_name(job_id, NAME)
    _stage(cfg, silence, "One")
    acted, shown = _ok(_land("--set", job_id, *WORDS, "--posted", "2026-05-03"))
    assert shown["set playlist"] == NAME
    assert _under_folder(cfg)
    assert _playlists_named(cfg, POSTED_NAME) == []
    ignored = _warned(acted, set_playlist.POSTED_IGNORED)
    assert len(ignored) == 1, acted["warnings"]
    (warning,) = ignored
    assert "--posted 2026-05-03" in warning["message"]
    assert POSTED_NAME.split()[0] in warning["message"]
    assert NAME.split()[0] in warning["message"]
    assert "the frozen name wins" in warning["message"]
    assert shown["posted day"] == warning["message"]
    assert not _warned(acted, set_playlist.POSTED_FALLBACK)


def test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name(
    native_library, silence, monkeypatch
):
    """Driven R-949: playlist pre-made under the posted name; a week on, one playlist."""
    cfg = _with_folder(native_library)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",), page=PAGE)
    _make_playlist(cfg, POSTED_NAME, under=_inspiration_folder_id(cfg))
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 16))
    acted, shown = _backfilled(job_id)
    assert shown["set playlist"] == POSTED_NAME
    assert len(_playlists_named(cfg, POSTED_NAME)) == 1
    assert _playlists_named(cfg, "10_16_26 Probe DJ Live at Probe 5-26") == []
    assert acted["data"]["totals"]["added"] == 1
    assert _set_item(acted, POSTED_NAME)["playlist_created"] is False


def test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it(
    native_library, silence
):
    """With no flag given, the words come off the job's page."""
    cfg, _root_id = native_library
    assert _root_folders(cfg, FOLDER) == []
    job_id = set_job(cfg, ("One",), page=PAGE)
    _stage(cfg, silence, "One")
    acted, shown = _ok(_land("--set", job_id))
    named = "5_03_26 Probe DJ Live at Probe 05.03.26 5-26"
    assert shown["under"] == f"{FOLDER}, created at the playlist root"
    ((folder_id,),) = _root_folders(cfg, FOLDER)
    ((_pid, parent, _a, _r),) = _under_folder(cfg, named)
    assert str(parent) == str(folder_id)
    assert _set_item(acted, named)["folder_created"] is True


def test_a_landing_from_a_playlist_job_or_no_job_writes_no_set_playlist(native_library, silence):
    cfg = _with_folder(native_library)
    _stage(cfg, silence, "One")
    acted, _shown = _ok(_land())
    assert _children(cfg, _inspiration_folder_id(cfg)) == []
    assert "set playlist tracks" not in acted["data"]["totals"]
    (record,) = session.records(cfg)
    assert set_playlist.RECORD_KEY not in record.detail


def test_a_playlist_job_named_with_set_is_refused_before_anything_moves(native_library, silence):
    """So is a set the page and the flags cannot name, and a word flag without --set."""
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
    assert _still_staged(cfg)
    code, envelope = drive(_land("--set", set_job(cfg, ("One",)), "--dj", "Probe DJ"))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == set_playlist.UNNAMED
    assert envelope["cause"]["detail"]["missing"] == ["--set-name", "--set-date"]
    code, envelope = drive(_land("--dj", "Probe DJ", "--set-date", "2026-05"))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert envelope["cause"]["detail"]["given"] == ["--dj", "--set-date"]
    assert "--set JOB" in envelope["cause"]["message"]
    assert _still_staged(cfg)
    assert session.records(cfg) == ()


def test_a_taxonomy_with_no_inspiration_folder_is_refused_by_name_before_the_gate(
    native_library, silence, monkeypatch
):
    """The landing and the backfill alike."""
    cfg, _root_id = native_library
    monkeypatch.setattr(active_taxonomy, "load", lambda _cfg: replace(DECLARED, inspiration=None))
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--set", job_id, *WORDS))
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == set_playlist.FOLDER_UNDECLARED
    assert any("[inspiration]" in step for step in envelope["cause"]["remediation"]["steps"])
    assert _still_staged(cfg)
    assert session.records(cfg) == ()
    code, envelope = drive(_inspiration(job_id, *WORDS))
    _refused_before_the_gate(cfg, code, envelope, set_playlist.FOLDER_UNDECLARED)


def test_two_root_folders_of_the_name_are_refused_rather_than_one_chosen(native_library, silence):
    cfg = _with_folder(native_library)
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, envelope = drive(_land("--set", job_id, *WORDS))
    assert envelope["cause"]["reason"] == set_playlist.FOLDER_UNDECLARED, envelope
    assert envelope["cause"]["detail"]["count"] == 2


def test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added(native_library, silence):
    """A row resolving only to a different version is not guessed (U113): the set leaves it out."""
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("One", "Four", "Two", "Six"))
    _staged(cfg, silence, "One", "Two", "Six (Extended Mix)")
    acted, shown = _ok(_land("--set", job_id, *WORDS))
    assert shown["set tracks"] == 2 and shown["set left out"] == 2
    assert acted["data"]["totals"]["added"] == 3, "the batch did not land every file"
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(_set_playlist_id(cfg))) == [rows["One"], rows["Two"]]
    (left,) = _warned(acted, set_playlist.LEFT_OUT)
    assert "2. Probe - Four" in left["message"] and set_playlist.NOT_RESOLVED in left["message"]
    assert "4. Probe - Six" in left["message"]
    missing = {"artist": "Probe", "state": "missing", "why": set_playlist.NOT_RESOLVED}
    assert _set_item(acted)["left"] == [
        {"position": 2, **missing, "title": "Four"},
        {"position": 4, **missing, "title": "Six"},
    ]


def test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so(native_library, silence):
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("Four",))
    _stage(cfg, silence, "One")
    acted, _shown = _ok(_land("--set", job_id, *WORDS))
    assert _under_folder(cfg) == []
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
    assert _still_staged(cfg)


# The backfill: crate intake inspiration


def test_the_backfill_over_a_landed_set_adds_the_playlist_and_nothing_to_inbox(
    native_library, silence
):
    cfg, root_id = native_library
    folder_id = _inspiration_folder_id(_with_folder(native_library))
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("One", "Three", "Two"))
    _staged(cfg, silence, "One", "Two")
    _ok(_land())
    inbox_before = _children(cfg, root_id)
    content_before = _content_table(cfg)
    acted, shown = _backfilled(job_id)
    assert shown["set playlist"] == NAME and shown["set tracks"] == 3 and shown["set left out"] == 0
    assert shown["digest"] == acted["data"]["digest"]
    ((playlist_id, parent, _a, _r),) = _under_folder(cfg)
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
    (record,) = _set_records(cfg)
    assert record.state is session.SessionState.CLOSED
    assert record.detail[set_playlist.RECORD_KEY]["id"] == str(playlist_id)
    assert {c.tree: c.created for c in record.change.trees} == {DECLARED.inspiration.id: 3}


def test_the_backfill_over_a_set_with_nothing_owned_asks_and_then_writes_nothing(
    native_library, silence
):
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("Four",))
    acted, _shown = _backfilled(job_id)
    assert acted["outcome"] == "no_op"
    assert _under_folder(cfg) == []
    assert [w["code"] for w in acted["warnings"]] == [
        set_playlist.POSTED_FALLBACK,
        set_playlist.NOTHING,
        set_playlist.LEFT_OUT,
    ]
    assert not _set_records(cfg)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    _cut_over_intake(machine)
    job_id = set_job(machine, ("One",))
    envelope = exited(drive(_inspiration(job_id, *WORDS)), ExitCode.ACK_REQUIRED)
    assert "gate" not in (envelope.get("cause") or {}).get("detail", {})


def test_the_backfill_on_the_bridge_is_refused_naming_the_cutover(acknowledged):
    code, envelope = drive(_inspiration("any-job", *WORDS))
    _refused_before_the_gate(acknowledged, code, envelope, "tree-unconverged")
    assert any("tree cutover" in step for step in envelope["cause"]["remediation"]["steps"])


def test_the_backfill_refuses_a_job_that_is_not_a_set_and_an_unfinished_one(native_library):
    cfg, _root_id = native_library
    code, envelope = drive(_inspiration("no-such-job", *WORDS))
    _refused_before_the_gate(cfg, code, envelope, "job-unknown")
    queued = _queued(cfg, {"rc_a": {"artist": "P", "title": "A"}}, **{intake_cli.SOURCE: "x"})
    code, envelope = drive(_inspiration(queued.job_id, *WORDS))
    _refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert envelope["cause"]["detail"]["state"] == "queued"


@pytest.mark.parametrize("verb", ["backfill", "landing"])
def test_a_folder_that_went_between_the_plan_and_the_write_is_refused_as_stale(
    native_library, silence, verb
):
    """A folder removed after the approval changes the digest; nothing moves out of staging."""
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    if verb == "backfill":
        _ok(_land())
        argv, gate = _inspiration(job_id, *WORDS), APPROVE
    else:
        argv, gate = _land("--set", job_id, *WORDS), GATE
    run_id = _decided(argv, gate=gate)["run_id"]
    _soft_delete_playlist(cfg, _inspiration_folder_id(cfg))
    code, acted = drive(["--run", run_id, *argv])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _under_folder(cfg) == []
    if verb == "landing":
        assert "has since changed" in acted["cause"]["message"]
        assert _still_staged(cfg)
        landed = _query(cfg, "SELECT COUNT(*) FROM djmdContent WHERE FolderPath LIKE ?", f"%{BATCH}%")
        assert landed == [(0,)]


# What the review added: answers read back, nothing offered, a pair of rows, a gap filled


def _offered_item(cfg: config.Config, job_id: str, title: str) -> tuple[str, str]:
    """The review item the worker offered for ``title`` and its first option."""
    with jobs.open_store() as store:
        reports = set_playlist.reports_of(store, jobs.get(store, job_id))
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
    """An offered row answered as the library's other version is owned, not left out."""
    cfg = _with_folder(native_library)
    _owned(cfg, silence, "One (Extended Mix)", content_id="held-1x")
    job_id = set_job(cfg, ("One", "Two"))
    item_id, option = _offered_item(cfg, job_id, "One")
    exited(drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option]))
    _stage(cfg, silence, "Two")
    _acted, shown = _ok(_land("--set", job_id, *WORDS))
    assert shown["set tracks"] == 2
    assert _members(cfg, str(_set_playlist_id(cfg))) == ["held-1x", _row_ids_by_name(cfg)["Two"]]


def test_an_unanswered_question_is_left_out_and_the_plan_offers_nothing(native_library, silence):
    """An unanswered question leaves the row out, and the plan writes no review item of its own."""
    cfg = _with_folder(native_library)
    _owned(cfg, silence, "One (Extended Mix)", content_id="held-1x")
    job_id = set_job(cfg, ("One",))
    _offered_item(cfg, job_id, "One")
    before = _unresolved(cfg)
    assert before == 1
    refused = exited(drive(_inspiration(job_id, *WORDS)), ExitCode.DECISION_REQUIRED)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["set tracks"] == 0 and shown["set left out"] == 1
    assert _unresolved(cfg) == before
    run_id = refused["run_id"]
    exited(drive(["run", "decide", run_id, APPROVE, "abort", "--actor", "a-person"]))
    code, acted = drive(["--run", run_id, *_inspiration(job_id, *WORDS)])
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    assert _unresolved(cfg) == before
    assert _under_folder(cfg) == []


def test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked(
    native_library, silence
):
    cfg = _with_folder(native_library)
    path = _owned(cfg, silence, "Three", content_id="held-3a")
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, Title, FolderPath, ContentLink, rb_local_deleted, "
        "created_at, updated_at) VALUES ('held-3b', 'Three', ?, ?, 0, '2026-01-01', "
        "'2026-01-01')",
        # rekordbox's value, so the library's rows still hold a majority (U126).
        str(path),
        LIBRARY_LINK,
    )
    job_id = set_job(cfg, ("Three", "One"))
    _stage(cfg, silence, "One")
    acted, _shown = _ok(_land("--set", job_id, *WORDS))
    assert _members(cfg, str(_set_playlist_id(cfg))) == [_row_ids_by_name(cfg)["One"]]
    assert [one["why"] for one in _set_item(acted)["left"]] == [set_playlist.AMBIGUOUS_ROWS]


def test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write(native_library, silence):
    """The playlist found by name gains only what it lacked, last, reported as one track added.

    ``--posted`` equal to the landing day must not flip the fallback on the re-plan,
    and a rerun on one day adds nothing and records no commit.
    """
    cfg = _with_folder(native_library)
    _owned(cfg, silence, "One", content_id="held-1")
    _owned(cfg, silence, "Two", content_id="held-2")
    job_id = set_job(cfg, ("One", "Three", "Two"))
    first, shown = _backfilled(job_id, "--posted", "2026-10-09")
    assert first["outcome"] != "error"
    assert shown["set playlist"] == NAME
    assert not _warned(first, set_playlist.POSTED_FALLBACK)
    playlist_id = _set_playlist_id(cfg)
    assert _members(cfg, str(playlist_id)) == ["held-1", "held-2"]
    _owned(cfg, silence, "Three", content_id="held-3")
    again, _shown = _backfilled(job_id)
    assert again["data"]["totals"]["added"] == 1 and again["data"]["totals"]["read back"] == 3
    assert _members(cfg, str(playlist_id)) == ["held-1", "held-2", "held-3"]
    # The second write finds the recorded playlist, so the posted fallback is not re-warned.
    assert [w["code"] for w in again["warnings"]] == [set_playlist.WRITTEN]
    rerun, _shown = _backfilled(job_id)
    assert rerun["data"]["totals"]["added"] == 0 and rerun["data"]["totals"]["read back"] == 3
    assert len(_members(cfg, str(playlist_id))) == 3
    # Records inside one second sort either way, so each is found by what it holds.
    records = _set_records(cfg)
    assert len(records) == 3
    committed = [r for r in records if r.sources]
    assert [r.sources for r in committed] == [{DECLARED.inspiration.id: "committed"}] * 2
    (nothing,) = [r for r in records if not r.sources]
    assert nothing.change.trees == ()
    assert set_playlist.RECORD_KEY not in nothing.detail


# What the table added: the engine's own stale checks


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
    """The engine's own re-plan is driven as a caller with no gate, then through the stale gate."""
    cfg = _with_folder(native_library)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    verb = _inspiration(job_id, *WORDS)
    run_id = _decided(verb)["run_id"]
    declared, job, words, reports = _backfill_inputs(cfg, job_id)
    plan = inspiration_cli.planned(cfg, declared, job, words, reports)
    assert [one.content_id for one in plan.members] == ["held-3"]
    _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = 'held-3'")
    with pytest.raises(CratekitError) as caught:
        inspiration_cli.written(cfg, declared, plan, job, words, reports)
    assert caught.value.cause.reason == "decision-stale"
    code, acted = drive(["--run", run_id, *verb])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _under_folder(cfg) == []
    assert not _set_records(cfg)


def test_the_engine_refuses_a_folder_removed_after_the_plan_even_with_no_gate_in_front(
    native_library, silence
):
    cfg = _with_folder(native_library)
    folder_id = _inspiration_folder_id(cfg)
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
    assert _under_folder(cfg) == []


# What the watcher's review added


def _soft_delete_playlist(cfg: config.Config, playlist_id: str) -> None:
    _sql(cfg, "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", playlist_id)


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
    cfg, root_id = native_library
    folder_id = _inspiration_folder_id(_with_folder(native_library))
    job_id = set_job(cfg, ("One", "Two"))
    _stage(cfg, silence, "One")
    _ok(_land("--set", job_id, *WORDS))
    ((playlist_id, *_rest),) = _under_parent(cfg, NAME, folder_id)
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    _stage(cfg, silence, "Two")
    second, shown = _ok(["intake", "land", "--name", "2026-10-10 Set", "--set", job_id, *WORDS])
    assert shown["playlist"].startswith("adds to the playlist")
    assert _under_parent(cfg, "10_10_26 Probe DJ Live at Probe 5-26", folder_id) == []
    assert len(_under_parent(cfg, NAME, folder_id)) == 1
    assert len(_under_parent(cfg, NAME, root_id)) == 1
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["One"], rows["Two"]]
    item = _set_item(second)
    assert (
        item["id"] == str(playlist_id) and item["added"] == 1 and item["playlist_created"] is False
    )


def test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made(
    native_library, silence
):
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    _ok(_land("--set", job_id, *WORDS))
    ((removed_id, *_rest),) = _under_folder(cfg)
    _soft_delete_playlist(cfg, str(removed_id))
    _acted, shown = _backfilled(job_id)
    assert shown["playlist"].startswith("found live")
    ((live_id, *_r),) = [row for row in _under_folder(cfg) if not row[3]]
    assert str(live_id) != str(removed_id)
    one = _row_ids_by_name(cfg)["One"]
    assert _members(cfg, str(live_id)) == [one]
    assert _members(cfg, str(removed_id)) == [one], "the removed one kept its own"


def test_a_removed_namesake_under_the_folder_is_not_written_into(native_library, silence):
    cfg = _with_folder(native_library)
    folder_id = _inspiration_folder_id(cfg)
    removed_id = _make_playlist(cfg, NAME, under=folder_id)
    _soft_delete_playlist(cfg, removed_id)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    acted, _shown = _backfilled(job_id)
    assert _members(cfg, removed_id) == []
    ((live_id, parent, _a, _r),) = [row for row in _under_parent(cfg, NAME, folder_id) if not row[3]]
    assert str(parent) == folder_id and str(live_id) != removed_id
    assert _members(cfg, str(live_id)) == ["held-3"]
    assert _set_item(acted)["playlist_created"] is True


def test_when_every_landed_members_file_is_refused_the_left_list_names_them(
    native_library, silence
):
    """The write's answer counts members whose files did not land, not only the plan's left rows.

    The file outside the set is what lets the batch land at all.
    """
    cfg = _with_folder(native_library)
    job_id = set_job(cfg, ("One", "Two"))
    # The batch landed into again by its own name goes back to its filed
    # folder (U164), so an earlier landing makes it and its names are held.
    _stage(cfg, silence, "Zero")
    _ok(_land())
    _staged(cfg, silence, "One", "Two", "Extra")
    occupied = _music(cfg, BATCH)
    (occupied / "One.flac").write_bytes(b"taken")
    (occupied / "Two.flac").write_bytes(b"taken")
    acted, shown = _ok(_land("--set", job_id, *WORDS))
    assert shown["set tracks"] == 2
    totals = acted["data"]["totals"]
    assert totals["landed"] == 1 and totals["refused"] == 2
    assert totals["set playlist left out"] == 2
    assert totals["set playlist tracks"] == 0
    assert _under_folder(cfg) == []
    (nothing,) = _warned(acted, set_playlist.NOTHING)
    assert "2 track(s) are listed as left out" in nothing["message"]
    (left,) = _warned(acted, set_playlist.LEFT_OUT)
    assert "1. Probe - One (its file did not land)" in left["message"]
    assert "2. Probe - Two (its file did not land)" in left["message"]
    # The first landing's record, then this one's.
    _first_record, record = session.records(cfg)
    assert set_playlist.RECORD_KEY not in record.detail


def test_two_rows_of_the_set_resolving_to_one_track_are_one_member(native_library, silence):
    cfg = _with_folder(native_library)
    _owned(cfg, silence, "Three", content_id="held-3")
    tracks = {"rc_a": _track("Three"), "rc_b": _track("Three", isrc="X1")}
    job_id = _run(_queued(cfg, tracks, **{intake_cli.SOURCE: "x", intake_cli.PAGE: {}}))
    acted, shown = _backfilled(job_id)
    assert shown["set tracks"] == 2, "both positions are shown"
    item = _set_item(acted)
    assert item["count"] == 1 and item["added"] == 1
    assert acted["data"]["totals"]["read back"] == 1
    assert _members(cfg, item["id"]) == ["held-3"]


def test_the_backfill_creates_the_declared_folder_at_the_root_when_the_library_lacks_it(
    native_library, silence
):
    cfg, _root_id = native_library
    assert _root_folders(cfg, FOLDER) == []
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Three",))
    acted, shown = _backfilled(job_id)
    assert shown["under"] == f"{FOLDER}, created at the playlist root"
    ((folder_id,),) = _root_folders(cfg, FOLDER)
    ((_pid, parent, _a, _r),) = _under_folder(cfg)
    assert str(parent) == str(folder_id)
    item = _set_item(acted)
    assert item["folder_created"] is True and item["playlist_created"] is True
    (record,) = _set_records(cfg)
    assert record.detail[set_playlist.RECORD_KEY]["folder"] == str(folder_id)


# U129: the landing archives the account playlist (driven)


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
    remote_id, _created = ledger.reserve_set_playlist(
        cfg, name, year, lambda: held.create_playlist(name)
    )
    return remote_id


def _freeze_name(job_id: str, name: str) -> None:
    """Put the INSPIRATION name on a succeeded set job the way intake set freezes it."""
    with jobs.open_store() as store:
        payload = {**jobs.get(store, job_id).payload, intake_cli.PLAYLIST_NAME: name}
        with store.immediate() as conn:
            conn.execute(
                "UPDATE jobs SET payload = ? WHERE job_id = ?", (json.dumps(payload), job_id)
            )


def _frozen_set(cfg, held, silence, *, record: bool = True) -> tuple[str, str]:
    """A set job frozen under NAME with its file staged, its account playlist recorded first."""
    cutover_fixtures.add_folder(cfg, FOLDER)
    remote_id = _record_account_set(cfg, held, NAME) if record else ""
    job_id = set_job(cfg, ("One",), page=PAGE)
    _freeze_name(job_id, NAME)
    _stage(cfg, silence, "One")
    return job_id, remote_id


def _transient(_cfg, _archived):
    raise refuse(
        "unavailable-transient",
        "the account could not be reached",
        remedy=Remedy.RETRY_LATER,
        origin=("test",),
    )


@pytest.mark.parametrize("failure", ["raised", "not-renamed"])
def test_a_landing_archive_failure_is_a_warning_on_the_envelope(
    account_on_native, silence, monkeypatch, failure
):
    """A raise after the landing wrote is a warning, and so is a not-renamed return."""
    cfg, _root_id, held = account_on_native
    job_id, _remote_id = _frozen_set(cfg, held, silence)
    planned = []
    real_plan = land_cli._plan_set_archive

    def capture(cfg_arg, **kwargs):
        planned.append(real_plan(cfg_arg, **kwargs))
        return planned[-1]

    def soft(_cfg, archived):
        said = f"{NAME} was retitled by somebody, so it was not renamed"
        return archived.payload, [{"code": "export-archive-changed-since-plan", "message": said}], False
    monkeypatch.setattr(land_cli, "_plan_set_archive", capture)
    monkeypatch.setattr(set_cli, "apply_archive", _transient if failure == "raised" else soft)
    acted, _shown = _ok(_land("--set", job_id, *WORDS))
    assert planned and planned[-1] is not None
    if failure == "raised":
        assert _warned(acted, land_cli.LAND_ARCHIVE_FAILED)
        said = "could not finish after the landing wrote"
    else:
        assert _warned(acted, "export-archive-changed-since-plan")
        said = "not renamed"
    assert any(said in w["message"] for w in acted["warnings"])
    assert held.renamed == []


def test_export_set_backfill_lists_inspiration_playlists_from_the_disposable_database(
    account_on_native, monkeypatch
):
    """Drive ``_inspiration_playlists`` against the disposable DB, never a stub."""
    from tests.test_u129_set_account_playlist import _succeeded_set_job
    cfg, _root_id, held = account_on_native
    folder_id = cutover_fixtures.add_folder(cfg, FOLDER)
    names = [
        "10_09_26 Public Service NYC Live at Vonking 5-26",
        "10_10_26 Public Service NYC Live at Signal 5-26",
    ]
    for name in names:
        _make_playlist(cfg, name, under=folder_id)
    # Succeeded set jobs whose frozen names match the playlists above.
    _succeeded_set_job(cfg, names[0], created="2026-10-09T15:00:00+00:00")
    _succeeded_set_job(cfg, names[1], created="2026-10-10T15:00:00+00:00")
    wanted = (match.Wanted(artist="Probe", title="One", origin=match.TEXT),)
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)
    assert [name for name, _pid in set_cli._inspiration_playlists(cfg)] == names
    refused = exited(drive(["export", "set"]), ExitCode.DECISION_REQUIRED)
    message = json.dumps(refused)
    assert names[0] in message and names[1] in message
    assert held.created == []
    assert "export-set-backfill-no-job" not in message
    assert ledger.set_playlist_names(cfg) == ()


# U140: the account playlist follows a renamed INSPIRATION playlist


def _landed_and_renamed(cfg, held, silence, *, record_first: bool) -> tuple[str, str, dict]:
    """A set landed under NAME, its account playlist recorded, its INSPIRATION renamed by hand."""
    job_id, remote_id = _frozen_set(cfg, held, silence, record=record_first)
    landed, _shown = _ok(_land("--set", job_id, *WORDS))
    if not record_first:
        remote_id = _record_account_set(cfg, held, NAME)
    _sql(cfg, "UPDATE djmdPlaylist SET Name = ? WHERE ID = ?", POSTED_NAME, str(_set_playlist_id(cfg)))
    return job_id, remote_id, landed


def _renamed(job_id: str) -> dict:
    argv = ["export", "set", "--rename", job_id]
    acted = exited(drive(["--run", _decided(argv, gate=set_cli.RENAME_GATE)["run_id"], *argv]))
    return acted


def test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database(
    account_on_native, silence
):
    """U140's read of the INSPIRATION playlist driven against the database, never a stub."""
    cfg, _root_id, held = account_on_native
    job_id, remote_id, _landed = _landed_and_renamed(cfg, held, silence, record_first=False)
    _renamed(job_id)
    assert held.renamed == [(remote_id, POSTED_NAME)]
    assert ledger.set_playlist_names(cfg) == (POSTED_NAME,)
    with jobs.open_store() as store:
        assert set_playlist.frozen_name(jobs.get(store, job_id)) == POSTED_NAME
    # The backfill over INSPIRATION now finds the renamed playlist recorded.
    after = exited(drive(["export", "set"]), ExitCode.DECISION_REQUIRED)
    assert after["cause"]["detail"]["shown"]["inspiration without account playlist"] == ["none"]
    assert held.created == [NAME]


def test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder(
    account_on_native, silence
):
    """U242: held as taken by id under the pass, no title written, whatever it is called now."""
    cfg, _root_id, held = account_on_native
    job_id, remote_id, landed = _landed_and_renamed(cfg, held, silence, record_first=True)
    assert held.renamed == [], held.renamed
    assert remote_id in mark_record.MarkRecord(cfg).taken_ids()
    # U142: the set's folder is Downloaded Sets <year>, never the plain year.
    assert "Downloaded Sets 2026" in held.folders_created or any(
        name == "Downloaded Sets 2026" for name in held.folder_names.values()
    ), held.folders_created
    assert "2026" not in held.folders_created
    assert not _warned(landed, land_cli.LAND_ARCHIVE_FAILED)
    _renamed(job_id)
    assert held.renamed == [(remote_id, POSTED_NAME)]
    assert remote_id in mark_record.MarkRecord(cfg).taken_ids()


def test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed(account_on_native, silence):
    """An archive before U242 marked the set's title; the rename leaves that mark alone."""
    cfg, _root_id, held = account_on_native
    job_id, remote_id, _landed = _landed_and_renamed(cfg, held, silence, record_first=True)
    mark_record.MarkRecord(cfg).record_marked(
        "2026-10-09 Set", {remote_id: (NAME, f"DOWNLOADED {NAME}")}
    )
    held.titles[remote_id] = f"DOWNLOADED {NAME}"
    before = list(held.renamed)
    refused = exited(drive(["export", "set", "--rename", job_id]), ExitCode.PRECONDITION)
    assert refused["cause"]["reason"] == set_cli.RENAME_UNRESOLVED
    assert "the pass 2026-10-09 Set" in refused["cause"]["message"]
    assert any(
        "crate sync unmark --pass '2026-10-09 Set'" in step
        for step in refused["cause"]["remediation"]["steps"]
    ), refused["cause"]["remediation"]
    assert held.renamed == before
    assert ledger.set_playlist_names(cfg) == (NAME,)


def test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order():
    """U246: a playlist found by name keeps what it held ahead of the set's rows, in order."""
    written = set_playlist.Written(
        name="a set",
        playlist_id="p",
        folder_id="f",
        folder_created=False,
        playlist_created=False,
        members=2,
        added=2,
        left=(),
        ids=("a", "b"),
        read_back=("x", "a", "b"),
    )
    set_playlist.assert_read_back(written)
    with pytest.raises(CratekitError) as caught:
        set_playlist.assert_read_back(replace(written, read_back=("x", "b", "a")))
    assert caught.value.cause.reason == "session-committed-unverified"
