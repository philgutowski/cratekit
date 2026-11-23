"""U113 on the native medium: each account playlist is its own INBOX playlist row.

The bridge suite's scenarios on the disposable database, so both media are
held to one behaviour, and the rotation planned over what the landing wrote,
which ages an account playlist by its landing record, not its name. D1 applies.
"""

from __future__ import annotations

import shutil
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs, preflight, rb_writer, session, tags, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import account_playlists, batch_name, missing_cli, native, rotate
from cratekit.intake import cli as intake_cli
from cratekit.sync import playlists
from tests import adopt_fixtures, cutover_fixtures
from tests import test_intake_land_native as land_native
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_intake_land_native import (
    DECLARED,
    INTAKE,
    TODAY,
    _members,
    _music,
    _query,
    _seed_binding_rows,
    _two_acts,
)
from tests.test_rb_writer_db import RECORDED_APP_VERSION

# The native landing suite's fixtures, bound so pytest finds them here.
_platform_seams = land_native._platform_seams
_release_process_locks = land_native._release_process_locks
acknowledged, library = land_native.acknowledged, land_native.library

DAY = date(2026, 10, 3)
RUN = "2026-10-03T101500Z-cd34"
PASS = missing_cli.synced_name(RUN)
BATCH = "2026-10-03 Tidal playlists"


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


# The native landing suite's machine, its database built once and copied after

#: What a key's first build left in the database file, and what it answered.
_BUILT: dict[str, tuple[bytes, str | None]] = {}


def _templated(key: str, cfg: config.Config, build) -> str | None:
    """Build ``cfg``'s database the first time, and copy those bytes in every time after.

    Every test then starts from a byte identical database, for a copy rather
    than a build; the suites over these fixtures build some ninety. A build that
    left a sidecar beside the file is not copied, since the file alone would not
    be the whole database.
    """
    db = Path(cfg.library.db_path)
    if key in _BUILT:
        data, answer = _BUILT[key]
        db.write_bytes(data)
        return answer
    answer = build()
    if not list(db.parent.glob(f"{db.name}-*")):
        _BUILT[key] = (db.read_bytes(), answer)
    return answer


def _machine(library: Path, monkeypatch, **data) -> config.Config:
    """A set-up machine: a disposable database, the binding rows, the identity seams."""
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
            **data,
        )
    )
    config.save(resolved)
    config.reset_cache()

    def build() -> None:
        adopt_fixtures.build(resolved, ())
        _seed_binding_rows(resolved)
    _templated(f"machine {resolved.profile.name}", resolved, build)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return resolved


def _cut_over(cfg: config.Config) -> tuple[config.Config, str]:
    """The intake tree recorded native, anchored to a root folder: ``_cut_over_intake``'s."""
    root_id = str(
        _templated(
            f"native {cfg.profile.name}",
            cfg,
            lambda: cutover_fixtures.add_folder(cfg, DECLARED.intake.display),
        )
    )
    record = tree_registry.TreeRecord(
        tree_id=INTAKE,
        mode=tree_registry.Mode.DATABASE,
        cutover_on=TODAY,
        root_id=root_id,
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    tree_registry.write(cfg, tree_registry.Registry().with_record(record))
    return cfg, root_id


@pytest.fixture
def machine(library, monkeypatch):
    return _machine(library, monkeypatch)


@pytest.fixture
def native_library(acknowledged):
    """The acknowledged machine with its intake tree cut over. Answers (cfg, root id)."""
    return _cut_over(acknowledged)


@pytest.fixture(scope="session")
def silence(tmp_path_factory) -> Path:
    """One second of silence, made once: every test copies it and none writes it."""
    return synth_container(tmp_path_factory.mktemp("scratch"), ".flac")


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
    with jobs.open_store() as store:
        queued = [
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
            for playlist_id, (name, titles) in listed.items()
        ]
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


def _staged(cfg: config.Config, silence: Path, *titles: str) -> None:
    for title in titles:
        _stage(cfg, silence, title)


def _written(acted: dict) -> list[dict]:
    return [item for item in acted["data"]["items"] if item["action"] == "playlist"]


def _left(acted: dict) -> list[dict]:
    return [w for w in acted["warnings"] if w["code"] == account_playlists.LEFT_OUT]


def _made(cfg: config.Config, root_id: str, name: str) -> str:
    """A playlist of ``name`` made under INBOX before the landing, as a person makes one."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        made = handle.create_playlist(name, parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
        return str(made.ID)
    finally:
        rb_writer.close_db(handle)


def _plans(cfg: config.Config, *days: date) -> list[rotate.RotationPlan]:
    """What the rotation would do on each of ``days``, planned on one handle."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        registry = tree_registry.read(cfg)
        return [
            rotate.plan_rotation(cfg, handle, declared=DECLARED, registry=registry, today=day)
            for day in days
        ]
    finally:
        rb_writer.close_db(handle)


def _actions(plan: rotate.RotationPlan) -> dict[str, str]:
    return {b.name: b.action for b in (*plan.moves, *plan.removals, *plan.kept)}


# The scenarios the brief names, on this medium


def test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names(
    native_library, silence
):
    """A track both playlists brought in is a member of both, and one row."""
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two")), "pl-b": ("Deep Cuts", ("Three", "Two"))})
    _staged(cfg, silence, "One", "Two", "Three")
    acted = _landed(cfg)
    folder = _music(cfg, BATCH)
    assert sorted(p.name for p in folder.iterdir()) == ["One.flac", "Three.flac", "Two.flac"]
    assert _inbox(cfg, root_id) == {
        "Sunset Warmup 2026-10-03": ["One", "Two"],
        "Deep Cuts 2026-10-03": ["Three", "Two"],
    }
    assert [(item["playlist"], item["account"], item["count"]) for item in _written(acted)] == [
        ("Sunset Warmup 2026-10-03", "pl-a", 2),
        ("Deep Cuts 2026-10-03", "pl-b", 2),
    ]
    assert acted["data"]["totals"]["memberships"] == 4
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE Title = 'Two'")) == 1


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
    _staged(cfg, silence, "One", "Hearted")
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
    assert [item["playlist"] for item in _written(acted)] == [BATCH]


def test_a_name_inbox_came_to_hold_after_the_plan_is_refused_and_nothing_is_written(
    native_library, silence, monkeypatch
):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    # A playlist of that name sits under INBOX, and the verb is handed the
    # names it would have chosen before it did, so only the engine's own
    # check stands between the plan and a second playlist of one name.
    _made(cfg, root_id, "Sunset Warmup 2026-10-03")
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


# The record, and the rotation ageing what the landing wrote


def test_the_record_names_each_account_playlist_by_identifier(native_library, silence):
    """And the rotation ages that playlist by its landing date, read off the record."""
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    (written,) = _written(_landed(cfg))
    landings = [r for r in session.records(cfg) if native.INBOX_PLAYLISTS_KEY in r.detail]
    (record,) = landings
    assert record.detail[native.INBOX_PLAYLISTS_KEY] == [
        {"id": written["id"], "name": "Sunset Warmup 2026-10-03", "account": "pl-a", "pass": PASS}
    ]
    # Every row went into the account playlist, so no batch playlist was written.
    assert native.BATCH_PLAYLIST_KEY not in record.detail
    landed = rotate.landings(cfg).by_id[written["id"]]
    (planned,) = _plans(cfg, landed + timedelta(days=cfg.reports.intake_stale_days + 1))
    (batch,) = [b for b in planned.moves if b.name == "Sunset Warmup 2026-10-03"]
    assert batch.recognised_by == rotate.BY_RECORD
    assert batch.aged_from == rotate.AGED_FROM_RECORD
    assert batch.landed == landed
    assert batch.action == rotate.MOVE


def test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together(
    native_library, silence
):
    """U175, Phillip's answer 2 read flat: a pass's playlists age as one."""
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",)), "pl-b": ("Deep Cuts", ("Two",))})
    _staged(cfg, silence, "One", "Two", "Loose")
    written = _written(_landed(cfg))[0]
    landed = rotate.landings(cfg).by_id[written["id"]]
    pass_playlists = {BATCH, "Sunset Warmup 2026-10-03", "Deep Cuts 2026-10-03"}
    stale, expired = cfg.reports.intake_stale_days, cfg.reports.intake_expired_days
    # Every day from the landing to past expiry, the three are planned alike.
    days = [landed + timedelta(days=age) for age in range(0, expired + 2)]
    for age, plan in enumerate(_plans(cfg, *days)):
        planned = _actions(plan)
        assert set(planned) == pass_playlists, age
        assert len({planned[name] for name in pass_playlists}) == 1, (age, planned)
    (moving,) = _plans(cfg, landed + timedelta(days=stale + 1))
    assert set(_actions(moving).values()) == {rotate.MOVE}
    # Moved into Old together, they are removed together.
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rotate.apply_rotation(
            cfg, handle, moving, declared=DECLARED, analysis_roots=[Path(cfg.library.root)]
        )
    finally:
        rb_writer.close_db(handle)
    assert not pass_playlists & set(_inbox(cfg, root_id))
    gone = _actions(_plans(cfg, landed + timedelta(days=expired + 1))[0])
    assert {gone[name] for name in pass_playlists} == {rotate.REMOVE}


def test_the_gate_screen_names_each_playlist_as_the_bridge_does(native_library, silence):
    cfg, root_id = native_library
    _made(cfg, root_id, "Sunset Warmup 2026-10-03")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One", "Loose")
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
    before_id = _made(cfg, root_id, "Sunset Warmup")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    _landed(cfg)
    assert _inbox(cfg, root_id) == {"Sunset Warmup": [], "Sunset Warmup 2026-10-03": ["One"]}
    assert _query(cfg, "SELECT Name FROM djmdPlaylist WHERE ID = ?", before_id) == [
        ("Sunset Warmup",)
    ]


def test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks(native_library, silence):
    cfg, root_id = native_library
    gone_id = _made(cfg, root_id, "Sunset Warmup 2026-10-03")
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


# U128: the INBOX playlist mirrors the whole account playlist, owned rows too


def _owned(cfg: config.Config, silence: Path, titles: tuple[str, ...]) -> None:
    """Land ``titles`` first under a name of their own and no pass, so each is a row."""
    for title in titles:
        _stage(cfg, silence, title)
    code, acted, _ = _two_acts(["intake", "land", "--name", "older batch"])
    assert code == int(ExitCode.OK), acted


def test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order(
    native_library, silence
):
    """And an owned track in two account playlists is in both."""
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1", "Held2", "Held3"))
    swept(
        cfg,
        {
            "pl-a": ("Sunset Warmup", ("Held1", "New1", "Held2", "New2", "Held3")),
            "pl-b": ("Deep Cuts", ("New1", "Held1")),
        },
    )
    _staged(cfg, silence, "New1", "New2")
    acted = _landed(cfg)
    inbox = _inbox(cfg, root_id)
    assert inbox["Sunset Warmup 2026-10-03"] == ["Held1", "New1", "Held2", "New2", "Held3"]
    assert inbox["Deep Cuts 2026-10-03"] == ["New1", "Held1"]
    # The owned rows are the library's own, never a second row for one file.
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE Title = 'Held1'")) == 1
    (written,) = [item for item in acted["data"]["items"] if item.get("account") == "pl-a"]
    assert written["count"] == 5
    assert not _left(acted)


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
    (warning,) = _left(acted)
    assert "Sunset Warmup 2026-10-03 1. Probe - Held1" in warning["message"]
    assert account_playlists.NO_ROW in warning["message"]


def test_a_rerun_of_the_same_pass_adds_nothing_twice(native_library, silence, monkeypatch):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1", "Late"))})
    _stage(cfg, silence, "New1")
    first = _landed(cfg)
    # Late never arrived the first time, so the first landing named it.
    (warning,) = _left(first)
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
    assert not _left(later)


def test_a_rerun_is_read_from_the_record_of_this_pass_alone(native_library, silence):
    """Another pass of the same account playlist mirrors it whole again, as its own landing.

    The first landing's gate screen counts the owned rows beside the new.
    """
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _stage(cfg, silence, "New1")
    code, acted, refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["account playlists"] == [
        "Sunset Warmup 2026-10-03 (2 file(s), 1 already in the library), the account's Sunset Warmup"
    ]
    run = "2026-10-03T201500Z-ab78"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New2"))}, run_id=run)
    _stage(cfg, silence, "New2")
    code, acted, _ = _two_acts(_land(missing_cli.synced_name(run)))
    assert code == int(ExitCode.OK), acted
    assert _inbox(cfg, root_id)["Sunset Warmup 2026-10-03 2"] == ["Held1", "New2"]


def test_another_owned_row_is_another_plan():
    """The digest names each owned row, so an answer for one row is stale for another."""
    target = Path("/library/music/b/New1.flac")
    new = native.PlaylistMember(target=target)

    def planned(*members: native.PlaylistMember) -> dict:
        one = native.PlaylistPlan(name="Sunset Warmup", account="pl-a", members=members)
        return native._playlist_identity(one)
    first = planned(native.PlaylistMember(content_id="101"), new)
    assert first != planned(native.PlaylistMember(content_id="102"), new)
    assert first["members"] == ["row 101", str(target)]
    # A playlist of new files alone keeps the keys it had before U128.
    assert planned(new) == {"name": "Sunset Warmup", "account": "pl-a", "targets": [str(target)]}


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
