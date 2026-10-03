"""U113 on the native medium: each account playlist is its own INBOX playlist row.

The same scenarios ``tests/test_intake_land_account_playlists.py`` drives on the
bridge, driven here against the disposable database the native landing suite
builds, so both media are held to one behaviour. The rotation is then planned
over what the landing wrote, which is how it is shown to age an account
playlist by its landing record rather than by a name that carries no date.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs, rb_writer, session, tags, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import account_playlists, batch_name, missing_cli, native, rotate
from cratekit.intake import cli as intake_cli
from cratekit.sync import playlists
from tests.cli_drive import drive
from tests.test_intake_land_native import (
    DECLARED,
    _members,
    _query,
    _two_acts,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

DAY = date(2026, 10, 3)
RUN = "2026-10-03T101500Z-cd34"
PASS = missing_cli.synced_name(RUN)
BATCH = "2026-10-03 Tidal playlists"


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


def _stage(cfg: config.Config, silence: Path, title: str) -> Path:
    path = Path(cfg.paths.download_staging) / f"{title}.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    return path


def swept(
    cfg: config.Config,
    listed: dict[str, tuple[str | None, tuple[str, ...]]],
    *,
    run_id: str = RUN,
    source_id: str = playlists.SOURCE_ID,
) -> None:
    """One job per playlist, ``id -> (account name, titles)``, queued as a sweep does and run."""
    queued = []
    with jobs.open_store() as store:
        for playlist_id, (name, titles) in listed.items():
            queued.append(
                intake_cli.queue_playlist(
                    store,
                    cfg,
                    handler_key="intake.playlist",
                    reference=playlist_id,
                    tracks={
                        f"tid-{title}": {
                            "artist": "Probe",
                            "title": title,
                            "origin": match.TIDAL,
                            "ref": f"tid-{title}",
                        }
                        for title in titles
                    },
                    run_id=run_id,
                    source_id=source_id,
                    name=name,
                )
            )
    for job in queued:
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed


def _land(pass_name: str = PASS) -> list[str]:
    return ["intake", "land", "--pass", pass_name]


def _inbox(cfg: config.Config, root_id: str) -> dict[str, list[str]]:
    """Every live playlist directly under the intake root and the titles it holds."""
    rows = _query(
        cfg,
        "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND rb_local_deleted = 0 "
        "ORDER BY Seq",
        root_id,
    )
    held = _query(cfg, "SELECT ID, Title FROM djmdContent")
    titles = {str(content_id): str(title) for content_id, title in held}
    return {
        str(name): [titles[member] for member in _members(cfg, str(playlist_id))]
        for playlist_id, name in rows
    }


def _landed(cfg: config.Config) -> dict:
    code, acted, _refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    return acted


# ---------------------------------------------------------------------------
# The scenarios the brief names, on this medium
# ---------------------------------------------------------------------------


def test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names(
    native_library, silence
):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two")), "pl-b": ("Deep Cuts", ("Three",))})
    for title in ("One", "Two", "Three"):
        _stage(cfg, silence, title)

    acted = _landed(cfg)

    folder = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    assert sorted(p.name for p in folder.iterdir()) == ["One.flac", "Three.flac", "Two.flac"]
    assert _inbox(cfg, root_id) == {"Sunset Warmup": ["One", "Two"], "Deep Cuts": ["Three"]}
    written = [item for item in acted["data"]["items"] if item["action"] == "playlist"]
    assert [(item["playlist"], item["account"], item["count"]) for item in written] == [
        ("Sunset Warmup", "pl-a", 2),
        ("Deep Cuts", "pl-b", 1),
    ]
    assert acted["data"]["totals"]["memberships"] == 3


def test_a_track_both_playlists_brought_in_is_a_member_of_both(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Shared")), "pl-b": ("Deep Cuts", ("Shared",))})
    for title in ("One", "Shared"):
        _stage(cfg, silence, title)

    _landed(cfg)

    assert _inbox(cfg, root_id) == {"Sunset Warmup": ["One", "Shared"], "Deep Cuts": ["Shared"]}
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE Title = 'Shared'")) == 1


def test_a_second_landing_of_one_playlist_the_next_week_is_named_two(
    native_library, silence, monkeypatch
):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    _landed(cfg)

    run = "2026-10-10T101500Z-ef56"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Two",))}, run_id=run)
    _stage(cfg, silence, "Two")
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    code, acted, _ = _two_acts(_land(missing_cli.synced_name(run)))

    assert code == int(ExitCode.OK), acted
    assert _inbox(cfg, root_id) == {"Sunset Warmup": ["One"], "Sunset Warmup 2": ["Two"]}


def test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    swept(cfg, {"favorites": (None, ("Hearted",))}, source_id=intake_cli.FAVORITES_SOURCE_ID)
    for title in ("One", "Hearted"):
        _stage(cfg, silence, title)

    acted = _landed(cfg)

    batch = "2026-10-03 Tidal playlists and Favorites"
    assert _inbox(cfg, root_id) == {batch: ["Hearted"], "Sunset Warmup": ["One"]}
    (warning,) = [w for w in acted["warnings"] if w["code"] == "rows-await-analysis"]
    assert f"the {batch} and Sunset Warmup playlists" in warning["message"]


def test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": (None, ("One",))})
    _stage(cfg, silence, "One")

    acted = _landed(cfg)

    assert _inbox(cfg, root_id) == {BATCH: ["One"]}
    written = [item["playlist"] for item in acted["data"]["items"] if item["action"] == "playlist"]
    assert written == [BATCH]


def test_a_name_inbox_came_to_hold_after_the_plan_is_refused_and_nothing_is_written(
    native_library, silence, monkeypatch
):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    # A playlist of that name sits under INBOX, and the verb is handed the
    # names it would have chosen before it did, so only the engine's own
    # check stands between the plan and a second playlist of one name.
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist("Sunset Warmup", parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    chosen = account_playlists.named
    monkeypatch.setattr(
        account_playlists, "named", lambda claimed, held, batch: chosen(claimed, (), batch=batch)
    )

    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert "nothing was written" in acted["cause"]["message"]
    # Refused before the first move, so the landing can simply be run again.
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    assert _query(cfg, "SELECT ID FROM djmdContent WHERE Title = 'One'") == []
    assert list(_inbox(cfg, root_id)) == ["Sunset Warmup"]


# ---------------------------------------------------------------------------
# The record, and the rotation ageing what the landing wrote
# ---------------------------------------------------------------------------


def test_the_record_names_each_account_playlist_by_identifier(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")

    acted = _landed(cfg)

    (written,) = [item for item in acted["data"]["items"] if item["action"] == "playlist"]
    landings = [r for r in session.records(cfg) if native.INBOX_PLAYLISTS_KEY in r.detail]
    (record,) = landings
    assert record.detail[native.INBOX_PLAYLISTS_KEY] == [
        {"id": written["id"], "name": "Sunset Warmup"}
    ]
    # Every row went into the account playlist, so no batch playlist was written.
    assert native.BATCH_PLAYLIST_KEY not in record.detail


def test_the_rotation_ages_an_account_playlist_by_its_landing_date(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    acted = _landed(cfg)
    (written,) = [item for item in acted["data"]["items"] if item["action"] == "playlist"]

    landed = rotate.landings(cfg).by_id[written["id"]]
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        planned = rotate.plan_rotation(
            cfg,
            handle,
            declared=DECLARED,
            registry=tree_registry.read(cfg),
            today=landed + timedelta(days=cfg.reports.intake_stale_days + 1),
        )
    finally:
        rb_writer.close_db(handle)

    (batch,) = [b for b in planned.moves if b.name == "Sunset Warmup"]
    assert batch.recognised_by == rotate.BY_RECORD
    assert batch.aged_from == rotate.AGED_FROM_RECORD
    assert batch.landed == landed
    assert batch.action == rotate.MOVE


def test_the_gate_screen_names_each_playlist_as_the_bridge_does(native_library, silence):
    cfg, root_id = native_library
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist("Sunset Warmup", parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    for title in ("One", "Loose"):
        _stage(cfg, silence, title)

    code, refused = drive(_land())

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlists"] == [
        "Sunset Warmup 2 (1 file(s)), the account's Sunset Warmup"
    ]
    assert shown["batch playlist holds"] == "1 file(s) no account playlist claimed"


def test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks(
    native_library, silence
):
    cfg, root_id = native_library
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        gone = handle.create_playlist("Sunset Warmup", parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
        gone_id = str(gone.ID)
    finally:
        rb_writer.close_db(handle)
    # Soft removed, the way the rotation removes an expired batch.
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            f"UPDATE djmdPlaylist SET {rb_writer.SOFT_DELETE_COLUMN} = 1 WHERE ID = ?", (gone_id,)
        )
    conn.close()
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")

    _landed(cfg)

    # A removed node holds no name, so the exact name is free, and the new
    # playlist is a new live row: the removed one gains nothing.
    assert _inbox(cfg, root_id) == {"Sunset Warmup": ["One"]}
    assert _members(cfg, gone_id) == []
