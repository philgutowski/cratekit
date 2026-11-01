"""U113 on the native medium: each account playlist is its own INBOX playlist row.

The same scenarios ``tests/test_intake_land_account_playlists.py`` drives on the
bridge, driven here against the disposable database the native landing suite
builds, so both media are held to one behaviour. The rotation is then planned
over what the landing wrote, which is how it is shown to age an account
playlist by its landing record rather than by its name, whose date at the
end (U175) is for a person to read.

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
    _music,
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
    """Every live playlist directly under the intake root and the titles it holds.

    All but INBOX / Analyze (U166), which every landing fills with the rows it
    made and whose own suite is ``tests/test_inbox_analyzed.py``.
    """
    rows = _query(
        cfg,
        "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND rb_local_deleted = 0 "
        "AND Name != ? ORDER BY Seq",
        root_id,
        native.ANALYZE,
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

    folder = _music(cfg, BATCH)
    assert sorted(p.name for p in folder.iterdir()) == ["One.flac", "Three.flac", "Two.flac"]
    assert _inbox(cfg, root_id) == {
        "Sunset Warmup 2026-10-03": ["One", "Two"],
        "Deep Cuts 2026-10-03": ["Three"],
    }
    written = [item for item in acted["data"]["items"] if item["action"] == "playlist"]
    assert [(item["playlist"], item["account"], item["count"]) for item in written] == [
        ("Sunset Warmup 2026-10-03", "pl-a", 2),
        ("Deep Cuts 2026-10-03", "pl-b", 1),
    ]
    assert acted["data"]["totals"]["memberships"] == 3


def test_a_track_both_playlists_brought_in_is_a_member_of_both(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Shared")), "pl-b": ("Deep Cuts", ("Shared",))})
    for title in ("One", "Shared"):
        _stage(cfg, silence, title)

    _landed(cfg)

    assert _inbox(cfg, root_id) == {
        "Sunset Warmup 2026-10-03": ["One", "Shared"],
        "Deep Cuts 2026-10-03": ["Shared"],
    }
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE Title = 'Shared'")) == 1


def test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date(
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
    # Its own landing's date tells the two passes apart, so no `` 2`` is needed (U175).
    assert _inbox(cfg, root_id) == {
        "Sunset Warmup 2026-10-03": ["One"],
        "Sunset Warmup 2026-10-10": ["Two"],
    }


def test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    swept(cfg, {"favorites": (None, ("Hearted",))}, source_id=intake_cli.FAVORITES_SOURCE_ID)
    for title in ("One", "Hearted"):
        _stage(cfg, silence, title)

    acted = _landed(cfg)

    batch = "2026-10-03 Tidal playlists and Favorites"
    assert _inbox(cfg, root_id) == {batch: ["Hearted"], "Sunset Warmup 2026-10-03": ["One"]}
    (warning,) = [w for w in acted["warnings"] if w["code"] == "rows-await-analysis"]
    # U166: the warning names the one playlist the visit selects, every row
    # either playlist holds being in it, and neither of the two.
    assert f"the {DECLARED.intake.display} / {native.ANALYZE} playlist" in warning["message"]
    assert batch not in warning["message"] and "Sunset Warmup" not in warning["message"]


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
        handle.create_playlist("Sunset Warmup 2026-10-03", parent=handle.get_playlist(ID=root_id))
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
    assert list(_inbox(cfg, root_id)) == ["Sunset Warmup 2026-10-03"]


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
        {"id": written["id"], "name": "Sunset Warmup 2026-10-03", "account": "pl-a", "pass": PASS}
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

    (batch,) = [b for b in planned.moves if b.name == "Sunset Warmup 2026-10-03"]
    assert batch.recognised_by == rotate.BY_RECORD
    assert batch.aged_from == rotate.AGED_FROM_RECORD
    assert batch.landed == landed
    assert batch.action == rotate.MOVE



def _rotation(cfg: config.Config, today: date) -> dict[str, str]:
    """What the rotation would do on ``today``, by playlist name."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        planned = rotate.plan_rotation(
            cfg, handle, declared=DECLARED, registry=tree_registry.read(cfg), today=today
        )
    finally:
        rb_writer.close_db(handle)
    return {b.name: b.action for b in (*planned.moves, *planned.removals, *planned.kept)}


def test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together(
    native_library, silence
):
    """U175, Phillip's answer 2 read flat: a pass's playlists age as one."""
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",)), "pl-b": ("Deep Cuts", ("Two",))})
    for title in ("One", "Two", "Loose"):
        _stage(cfg, silence, title)
    acted = _landed(cfg)
    written = [item for item in acted["data"]["items"] if item["action"] == "playlist"][0]
    landed = rotate.landings(cfg).by_id[written["id"]]
    pass_playlists = {BATCH, "Sunset Warmup 2026-10-03", "Deep Cuts 2026-10-03"}
    stale, expired = cfg.reports.intake_stale_days, cfg.reports.intake_expired_days

    # Every day from the landing to past expiry, the three are planned alike.
    for age in range(0, expired + 2):
        planned = _rotation(cfg, landed + timedelta(days=age))
        assert set(planned) == pass_playlists, age
        assert len({planned[name] for name in pass_playlists}) == 1, (age, planned)
    assert set(_rotation(cfg, landed + timedelta(days=stale + 1)).values()) == {rotate.MOVE}

    # Moved into Old together, they are removed together.
    moving = landed + timedelta(days=stale + 1)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        plan = rotate.plan_rotation(
            cfg, handle, declared=DECLARED, registry=tree_registry.read(cfg), today=moving
        )
    finally:
        rb_writer.close_db(handle)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rotate.apply_rotation(
            cfg, handle, plan, declared=DECLARED, analysis_roots=[Path(cfg.library.root)]
        )
    finally:
        rb_writer.close_db(handle)
    assert not pass_playlists & set(_inbox(cfg, root_id))
    gone = _rotation(cfg, landed + timedelta(days=expired + 1))
    assert {gone[name] for name in pass_playlists} == {rotate.REMOVE}

def test_the_gate_screen_names_each_playlist_as_the_bridge_does(native_library, silence):
    cfg, root_id = native_library
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist("Sunset Warmup 2026-10-03", parent=handle.get_playlist(ID=root_id))
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
        "Sunset Warmup 2026-10-03 2 (1 file(s)), the account's Sunset Warmup"
    ]
    assert shown["batch playlist holds"] == "1 file(s) no account playlist claimed"



def test_an_undated_playlist_from_before_u175_is_left_as_it_is(native_library, silence):
    """Phillip's answer 4: nothing INBOX already holds is renamed, and the landing still lands."""
    cfg, root_id = native_library
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        before = handle.create_playlist("Sunset Warmup", parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
        before_id = str(before.ID)
    finally:
        rb_writer.close_db(handle)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")

    _landed(cfg)

    assert _inbox(cfg, root_id) == {"Sunset Warmup": [], "Sunset Warmup 2026-10-03": ["One"]}
    assert _query(cfg, "SELECT Name FROM djmdPlaylist WHERE ID = ?", before_id) == [
        ("Sunset Warmup",)
    ]

def test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks(
    native_library, silence
):
    cfg, root_id = native_library
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        gone = handle.create_playlist(
            "Sunset Warmup 2026-10-03", parent=handle.get_playlist(ID=root_id)
        )
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
    assert _inbox(cfg, root_id) == {"Sunset Warmup 2026-10-03": ["One"]}
    assert _members(cfg, gone_id) == []


# ---------------------------------------------------------------------------
# U128: the INBOX playlist mirrors the whole account playlist, owned rows too
# ---------------------------------------------------------------------------


def _owned(cfg: config.Config, silence: Path, titles: tuple[str, ...]) -> None:
    """Land ``titles`` first under a name of their own and no pass, so each is a row."""
    for title in titles:
        _stage(cfg, silence, title)
    code, acted, _ = _two_acts(["intake", "land", "--name", "older batch"])
    assert code == int(ExitCode.OK), acted


def test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order(
    native_library, silence
):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1", "Held2", "Held3"))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1", "Held2", "New2", "Held3"))})
    for title in ("New1", "New2"):
        _stage(cfg, silence, title)

    acted = _landed(cfg)

    inbox = _inbox(cfg, root_id)
    assert inbox["Sunset Warmup 2026-10-03"] == ["Held1", "New1", "Held2", "New2", "Held3"]
    # The owned rows are the library's own, never a second row for one file.
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE Title = 'Held1'")) == 1
    (written,) = [
        item for item in acted["data"]["items"] if item.get("account") == "pl-a"
    ]
    assert written["count"] == 5
    assert not [w for w in acted["warnings"] if w["code"] == account_playlists.LEFT_OUT]


def test_an_owned_track_in_two_account_playlists_is_in_both(native_library, silence):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(
        cfg,
        {"pl-a": ("Sunset Warmup", ("Held1", "New1")), "pl-b": ("Deep Cuts", ("New1", "Held1"))},
    )
    _stage(cfg, silence, "New1")

    _landed(cfg)

    inbox = _inbox(cfg, root_id)
    assert inbox["Sunset Warmup 2026-10-03"] == ["Held1", "New1"]
    assert inbox["Deep Cuts 2026-10-03"] == ["New1", "Held1"]


def test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned(native_library, silence):
    cfg, root_id = native_library
    # On disk under the music folder, so the sweep calls it owned, and never
    # landed, so the collection holds no row for its file.
    loose = Path(cfg.library.root) / cfg.library.music_dir / "by hand"
    loose.mkdir(parents=True)
    _stage(cfg, silence, "Held1").rename(loose / "Held1.flac")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _stage(cfg, silence, "New1")

    acted = _landed(cfg)

    assert _inbox(cfg, root_id) == {"Sunset Warmup 2026-10-03": ["New1"]}
    (warning,) = [w for w in acted["warnings"] if w["code"] == account_playlists.LEFT_OUT]
    assert "Sunset Warmup 2026-10-03 1. Probe - Held1" in warning["message"]
    assert account_playlists.NO_ROW in warning["message"]


def test_a_rerun_of_the_same_pass_adds_nothing_twice(native_library, silence, monkeypatch):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1", "Late"))})
    _stage(cfg, silence, "New1")
    first = _landed(cfg)
    # Late never arrived the first time, so the first landing named it.
    (warning,) = [w for w in first["warnings"] if w["code"] == account_playlists.LEFT_OUT]
    assert "Probe - Late" in warning["message"]

    # Nothing staged: the same pass again is a plan of nothing and writes nothing.
    code, again = drive(_land())
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op", again

    # Late arrives and the same pass is landed again: the account playlist
    # this pass already mirrored is not mirrored a second time, and the new
    # landing's playlist holds only what it brought.
    _stage(cfg, silence, "Late")
    later = _landed(cfg)

    inbox = _inbox(cfg, root_id)
    assert inbox["Sunset Warmup 2026-10-03"] == ["Held1", "New1"]
    assert inbox["Sunset Warmup 2026-10-03 2"] == ["Late"]
    assert not [w for w in later["warnings"] if w["code"] == account_playlists.LEFT_OUT]


def test_a_rerun_is_read_from_the_record_of_this_pass_alone(native_library, silence):
    """Another pass of the same account playlist mirrors it whole again, as its own landing."""
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _stage(cfg, silence, "New1")
    _landed(cfg)

    run = "2026-10-03T201500Z-ab78"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New2"))}, run_id=run)
    _stage(cfg, silence, "New2")
    code, acted, _ = _two_acts(_land(missing_cli.synced_name(run)))

    assert code == int(ExitCode.OK), acted
    assert _inbox(cfg, root_id)["Sunset Warmup 2026-10-03 2"] == ["Held1", "New2"]


def test_the_gate_screen_counts_the_owned_rows_beside_the_new(native_library, silence):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _stage(cfg, silence, "New1")

    code, refused = drive(_land())

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlists"] == [
        "Sunset Warmup 2026-10-03 (2 file(s), 1 already in the library), the account's Sunset Warmup"
    ]


def test_another_owned_row_is_another_plan():
    """The digest names each owned row, so an answer for one row is stale for another."""
    target = Path("/library/music/b/New1.flac")

    def planned(owned: str) -> dict:
        one = native.PlaylistPlan(
            name="Sunset Warmup",
            account="pl-a",
            members=(
                native.PlaylistMember(content_id=owned),
                native.PlaylistMember(target=target),
            ),
        )
        return native._playlist_identity(one)

    assert planned("101") != planned("102")
    assert planned("101")["members"] == ["row 101", str(target)]
    # A playlist of new files alone keeps the keys it had before U128.
    alone = native.PlaylistPlan(
        name="Sunset Warmup", account="pl-a", members=(native.PlaylistMember(target=target),)
    )
    assert native._playlist_identity(alone) == {
        "name": "Sunset Warmup",
        "account": "pl-a",
        "targets": [str(target)],
    }


def test_a_playlist_whose_only_file_is_unsupported_still_names_it_as_left():
    """A playlist dropped for holding nothing writable keeps its left rows, by its name."""
    target = Path("/library/music/b/Odd.xyz")
    member = account_playlists.Member(position=3, file=Path("Odd.xyz"), artist="Probe", title="Odd")
    row = native.RowPlan(
        source=Path("/staging/Odd.xyz"),
        target=target,
        action=native.UNSUPPORTED,
        title="Odd",
        folder_path=str(target),
        file_name=target.name,
        file_size=1,
        file_type=0,
        content_link=None,
    )
    one = native.PlaylistPlan(
        name="Deep Cuts",
        account="pl-b",
        members=(native.PlaylistMember(target=target, member=member),),
    )

    kept, dropped = native._supported_only([one], [row])

    assert kept == ()
    assert dropped == (("Deep Cuts", member.left(account_playlists.NOT_LANDED)),)
