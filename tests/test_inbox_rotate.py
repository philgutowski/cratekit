"""U111: ``crate inbox rotate`` moves stale batches into Old and removes expired ones.

Every drive goes through the real dispatcher against a disposable database
built the way the adoption suites build one, with the intake tree recorded
database native and anchored to a root folder the fixture made. Each scenario
reads the content and membership tables from SQL before and after, because the
one promise this verb makes beyond its plan is that no track goes anywhere.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from cratekit.core import config, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import native, rotate, rotate_cli
from tests import adopt_fixtures, cutover_fixtures
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION

DECLARED = taxonomy.default_taxonomy()
INTAKE = DECLARED.intake.id
OLD = DECLARED.intake_old.display
GATE = rotate_cli.APPROVE_GATE
TODAY = date(2026, 10, 3)
VERB = ["inbox", "rotate", "--as-of", TODAY.isoformat()]

#: Eight tracks, two to a batch, every one also filed in a genre playlist.
TRACKS = tuple(
    adopt_fixtures.Track(content_id=f"t{n}", filename=f"track-{n}.flac", genre="House")
    for n in range(1, 9)
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the cutover suite patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )


@pytest.fixture
def machine(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    (tmp_path / "staging").mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    resolved = config.from_dict(
        valid_data(
            root,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, TRACKS)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return resolved


@pytest.fixture
def acknowledged(machine):
    session.record_acknowledgment(machine, terminal=lambda: True)
    return machine


def _cut_over_intake(cfg: config.Config) -> str:
    root_id = cutover_fixtures.add_folder(cfg, DECLARED.intake.display)
    tree_registry.write(
        cfg,
        tree_registry.Registry().with_record(
            tree_registry.TreeRecord(
                tree_id=INTAKE,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=TODAY,
                root_id=root_id,
                source=tree_registry.DerivationSource.TAXONOMY,
            )
        ),
    )
    return root_id


@pytest.fixture
def native_library(acknowledged):
    """The acknowledged machine with its intake tree cut over. Answers (cfg, root id)."""
    return acknowledged, _cut_over_intake(acknowledged)


# ---------------------------------------------------------------------------
# Building INBOX
# ---------------------------------------------------------------------------


def _open(cfg: config.Config):
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)


def _node(
    cfg: config.Config,
    name: str,
    *,
    under: str,
    age: int | None = None,
    tracks: tuple[str, ...] = (),
    folder: bool = False,
    batch_folder: bool = False,
) -> str:
    """One playlist or folder under ``under``, created ``age`` days before TODAY."""
    handle = _open(cfg)
    try:
        parent = handle.get_playlist(ID=under)
        row = (
            handle.create_playlist_folder(name, parent=parent)
            if folder
            else handle.create_playlist(name, parent=parent)
        )
        if age is not None:
            row.created_at = datetime.combine(TODAY - timedelta(days=age), datetime.min.time())
        for content_id in tracks:
            handle.add_to_playlist(row, content_id)
        handle.session.commit()
        playlist_id = str(row.ID)
    finally:
        rb_writer.close_db(handle)
    if batch_folder:
        (Path(cfg.library.root) / cfg.library.music_dir / name).mkdir(parents=True)
    return playlist_id


def _genre_playlist(cfg: config.Config) -> str:
    """A playlist outside INBOX holding every track, as BY GENRE + ENERGY would."""
    folder = cutover_fixtures.add_folder(cfg, "genre tree")
    return _node(cfg, "House Low", under=folder, tracks=tuple(t.content_id for t in TRACKS))


def _record_landing(
    cfg: config.Config,
    playlist_id: str,
    name: str,
    landed: date,
    *,
    source: session.SourceState = session.SourceState.COMMITTED,
) -> None:
    """A native landing's session record naming its batch playlist, closed."""
    started = datetime.combine(landed, datetime.min.time().replace(hour=12)).astimezone()
    record = session.SessionRecord(
        session_id=f"{started.strftime('%Y%m%dT%H%M%S')}-landing",
        workflow=native.WORKFLOW,
        started=started.isoformat(),
        state=session.SessionState.CLOSED,
        sources={INTAKE: str(source)},
        ended=started.isoformat(),
        detail={native.BATCH_PLAYLIST_KEY: {"id": playlist_id, "name": name}},
    )
    session.write_record(record, cfg)


def _query(cfg: config.Config, sql: str, *params) -> list[tuple]:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _content(cfg: config.Config) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdContent ORDER BY ID")


def _memberships(cfg: config.Config, *, outside: tuple[str, ...] = ()) -> list[tuple]:
    marks = ",".join("?" for _ in outside) or "''"
    return _query(
        cfg,
        f"SELECT * FROM djmdSongPlaylist WHERE PlaylistID NOT IN ({marks}) ORDER BY ID",
        *outside,
    )


def _node_row(cfg: config.Config, playlist_id: str) -> tuple:
    (row,) = _query(
        cfg,
        "SELECT Name, ParentID, rb_local_deleted, Attribute FROM djmdPlaylist WHERE ID = ?",
        playlist_id,
    )
    return row


def _live_members(cfg: config.Config, playlist_id: str) -> list[str]:
    rows = _query(
        cfg,
        "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
        "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY ContentID",
        playlist_id,
    )
    return [str(row[0]) for row in rows]


def _olds(cfg: config.Config, root_id: str) -> list[str]:
    rows = _query(
        cfg,
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND ParentID = ? AND Attribute = 1 "
        "AND COALESCE(rb_local_deleted, 0) = 0",
        OLD,
        root_id,
    )
    return [str(row[0]) for row in rows]


def _two_acts(verb: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _by_action(envelope: dict) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for item in envelope["data"]["items"]:
        found.setdefault(item["action"], []).append(item["playlist"])
    return found


# ---------------------------------------------------------------------------
# The brief's scenario: 10, 40 and 100 in INBOX, 120 in Old
# ---------------------------------------------------------------------------


@pytest.fixture
def four_batches(native_library):
    """Three batches in INBOX, one in Old, a person's playlist and folder beside them."""
    cfg, root_id = native_library
    genre = _genre_playlist(cfg)
    old_id = _node(cfg, OLD, under=root_id, folder=True)
    ids = {
        "10": _node(
            cfg, "2026-09-23 Tidal playlists", under=root_id, age=10,
            tracks=("t1", "t2"), batch_folder=True,
        ),
        "40": _node(
            cfg, "2026-08-24 Favorites", under=root_id, age=40,
            tracks=("t3", "t4"), batch_folder=True,
        ),
        "100": _node(
            cfg, "2026-06-25T101010Z-1_inboxed", under=root_id, age=100, tracks=("t5", "t6")
        ),
        # Recognised and aged by its run record: the row itself says today.
        "120": _node(cfg, "a batch named by hand", under=old_id, age=0, tracks=("t7", "t8")),
        "mine": _node(cfg, "listen later", under=root_id, age=200, tracks=("t1", "t8")),
        "dated but mine": _node(cfg, "2026-01-01 my list", under=root_id, age=275),
        "folder": _node(cfg, "Lisa picks", under=root_id, folder=True),
    }
    _record_landing(cfg, ids["120"], "a batch named by hand", TODAY - timedelta(days=120))
    return cfg, root_id, old_id, genre, ids


def test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves(
    four_batches,
):
    cfg, root_id, old_id, genre, ids = four_batches
    content_before = _content(cfg)
    others_before = _memberships(cfg, outside=(ids["120"],))
    genre_before = _live_members(cfg, genre)

    code, acted, refused = _two_acts(VERB)

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["digest"] == acted["data"]["digest"]
    actions = _by_action(acted)
    assert actions["move"] == ["2026-06-25T101010Z-1_inboxed", "2026-08-24 Favorites"]
    assert actions["remove"] == ["a batch named by hand"]
    assert actions["keep"] == ["2026-09-23 Tidal playlists"]
    assert sorted(actions[rotate_cli.LEAVE]) == ["2026-01-01 my list", "Lisa picks", "listen later"]

    # The moves: parent is Old, still live, every track still in it.
    for key, members in (("40", ["t3", "t4"]), ("100", ["t5", "t6"])):
        name, parent, deleted, _attribute = _node_row(cfg, ids[key])
        assert (str(parent), int(deleted or 0)) == (old_id, 0), name
        assert _live_members(cfg, ids[key]) == members
    # The removal: the node and its own memberships carry the marker, the rows stay.
    assert int(_node_row(cfg, ids["120"])[2]) == 1
    assert _live_members(cfg, ids["120"]) == []
    assert len(_query(cfg, "SELECT ID FROM djmdSongPlaylist WHERE PlaylistID = ?", ids["120"])) == 2
    # Kept and left alone exactly as they were.
    assert str(_node_row(cfg, ids["10"])[1]) == root_id
    for key in ("mine", "dated but mine", "folder"):
        assert str(_node_row(cfg, ids[key])[1]) == root_id and not _node_row(cfg, ids[key])[2]

    # NO TRACK WENT ANYWHERE: every content row and every other membership,
    # every column, as before.
    assert _content(cfg) == content_before
    assert _memberships(cfg, outside=(ids["120"],)) == others_before
    assert _live_members(cfg, genre) == genre_before

    totals = acted["data"]["totals"]
    assert (totals["moved"], totals["removed"], totals["memberships removed"]) == (2, 1, 2)
    assert totals["old created"] is False
    (record,) = [r for r in session.records(cfg) if r.workflow == rotate.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert record.sources == {INTAKE: "committed"}
    assert record.snapshot_path


def test_each_batch_says_how_it_was_recognised_and_what_it_was_aged_from(four_batches):
    cfg, *_ = four_batches
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    shown = {item["playlist"]: item for item in envelope["data"]["items"]}
    assert shown["a batch named by hand"]["recognised by"] == rotate.BY_RECORD
    assert shown["a batch named by hand"]["aged from"] == rotate.AGED_FROM_RECORD
    assert shown["a batch named by hand"]["age_days"] == 120
    assert shown["2026-06-25T101010Z-1_inboxed"]["recognised by"] == rotate.BY_SUFFIX
    assert shown["2026-08-24 Favorites"]["recognised by"] == rotate.BY_NAME
    assert shown["2026-08-24 Favorites"]["aged from"] == rotate.AGED_FROM_CREATED
    assert shown["2026-08-24 Favorites"]["tracks"] == 2
    assert shown["listen later"]["kind"] == "playlist"
    assert shown["Lisa picks"]["kind"] == "folder"
    # A dated name with no batch folder is somebody's playlist.
    assert shown["2026-01-01 my list"]["action"] == rotate_cli.LEAVE


def test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing(four_batches):
    """The two stages: a batch past expiry still in INBOX moves first."""
    cfg, root_id, old_id, _genre, ids = four_batches
    assert _two_acts(VERB)[0] == int(ExitCode.OK)

    code, acted, _ = _two_acts(VERB)
    assert code == int(ExitCode.OK), acted
    assert _by_action(acted)["remove"] == ["2026-06-25T101010Z-1_inboxed"]
    assert int(_node_row(cfg, ids["100"])[2]) == 1

    code, acted, _ = _two_acts(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert "move" not in _by_action(acted) and "remove" not in _by_action(acted)
    assert rotate_cli.NOTHING_TO_ROTATE in [w["code"] for w in acted["warnings"]]


# ---------------------------------------------------------------------------
# Old, idempotence, the empty plan
# ---------------------------------------------------------------------------


def test_old_is_created_once_and_the_second_run_reuses_it(native_library):
    cfg, root_id = native_library
    first = _node(cfg, "2026-08-20 Set", under=root_id, age=44, tracks=("t1",), batch_folder=True)
    assert _olds(cfg, root_id) == []

    code, acted, _ = _two_acts(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["old created"] is True
    (old_id,) = _olds(cfg, root_id)
    assert str(_node_row(cfg, first)[1]) == old_id
    assert int(_node_row(cfg, old_id)[3]) == 1

    second = _node(cfg, "2026-08-21 Set", under=root_id, age=43, tracks=("t2",), batch_folder=True)
    code, acted, _ = _two_acts(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["old created"] is False
    assert _olds(cfg, root_id) == [old_id]
    assert str(_node_row(cfg, second)[1]) == old_id


def test_a_second_run_plans_nothing_and_still_asks(native_library):
    cfg, root_id = native_library
    _node(cfg, "2026-08-20 Set", under=root_id, age=44, tracks=("t1",), batch_folder=True)
    assert _two_acts(VERB)[0] == int(ExitCode.OK)
    content, members = _content(cfg), _memberships(cfg)
    nodes = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")

    code, acted, refused = _two_acts(VERB)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert refused["cause"]["detail"]["gate"] == GATE
    assert [item["action"] for item in acted["data"]["items"]] == ["keep"]
    assert (acted["data"]["totals"]["move"], acted["data"]["totals"]["remove"]) == (0, 0)
    assert (_content(cfg), _memberships(cfg)) == (content, members)
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == nodes


def test_an_empty_inbox_still_asks_and_creates_no_old(native_library):
    cfg, root_id = native_library
    code, acted, refused = _two_acts(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert refused["cause"]["detail"]["shown"]["items"] == []
    assert _olds(cfg, root_id) == []


# ---------------------------------------------------------------------------
# Refusals before the gate
# ---------------------------------------------------------------------------


def _refused_before_the_gate(cfg: config.Config, code: int, envelope: dict, reason: str) -> None:
    assert code != int(ExitCode.OK) and code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == reason, envelope
    assert not [r for r in session.records(cfg) if r.workflow == rotate.WORKFLOW]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    _cut_over_intake(machine)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), envelope
    assert "gate" not in (envelope.get("cause") or {}).get("detail", {})


def test_an_intake_tree_on_the_bridge_is_refused_naming_the_cutover(acknowledged):
    code, envelope = drive(VERB)
    _refused_before_the_gate(acknowledged, code, envelope, "tree-unconverged")
    assert any("tree cutover" in step for step in envelope["cause"]["remediation"]["steps"])


def test_a_taxonomy_with_no_old_folder_is_refused_by_name(native_library, monkeypatch):
    cfg, _ = native_library
    from dataclasses import replace

    from cratekit.core import active_taxonomy

    monkeypatch.setattr(active_taxonomy, "load", lambda _cfg: replace(DECLARED, intake_old=None))
    code, envelope = drive(VERB)
    _refused_before_the_gate(cfg, code, envelope, "intake-old-undeclared")


def test_two_old_folders_are_refused_rather_than_one_chosen(native_library):
    cfg, root_id = native_library
    _node(cfg, OLD, under=root_id, folder=True)
    _node(cfg, OLD, under=root_id, folder=True)
    code, envelope = drive(VERB)
    _refused_before_the_gate(cfg, code, envelope, "intake-old-undeclared")


def test_an_inbox_changed_after_the_approval_is_refused_and_nothing_is_written(native_library):
    cfg, root_id = native_library
    _node(cfg, "2026-08-20 Set", under=root_id, age=44, tracks=("t1",), batch_folder=True)
    code, refused = drive(VERB)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    _node(cfg, "2026-08-19 Set", under=root_id, age=45, tracks=("t2",), batch_folder=True)
    nodes = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")

    code, envelope = drive(["--run", run_id, *VERB])

    assert code == int(ExitCode.DECISION_STALE), envelope
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == nodes


# ---------------------------------------------------------------------------
# The engine and the writer, below the verb
# ---------------------------------------------------------------------------


def _plan(cfg: config.Config) -> rotate.RotationPlan:
    handle = _open(cfg)
    try:
        return rotate.plan_rotation(
            cfg, handle, declared=DECLARED, registry=tree_registry.read(cfg), today=TODAY
        )
    finally:
        rb_writer.close_db(handle)


def _apply(cfg: config.Config, plan: rotate.RotationPlan) -> rotate.Rotated:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return rotate.apply_rotation(
            cfg, handle, plan, declared=DECLARED, analysis_roots=[Path(cfg.library.root)]
        )
    finally:
        rb_writer.close_db(handle)


def test_the_engine_refuses_a_plan_inbox_no_longer_matches(native_library):
    cfg, root_id = native_library
    batch = _node(cfg, "2026-08-20 Set", under=root_id, age=44, tracks=("t1",), batch_folder=True)
    plan = _plan(cfg)
    handle = _open(cfg)
    try:
        handle.get_playlist(ID=batch).Name = "2026-08-20 Set renamed"
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    nodes = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")
    with pytest.raises(CratekitError) as raised:
        _apply(cfg, plan)
    assert raised.value.cause.reason == "decision-stale"
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == nodes


def test_a_removal_that_reaches_another_playlists_membership_is_refused_and_rolled_back(
    four_batches, monkeypatch
):
    """The confinement check's composite: the whitelist admits a membership marker
    in this commit, so only the SQL comparison can tell whose membership it was."""
    cfg, _root, _old, genre, _ids = four_batches
    real = rb_writer.remove_playlist_node

    def reaches_further(db, playlist):
        marked = real(db, playlist)
        rb_writer.remove_memberships(db, db.get_playlist(ID=genre), ["t1"])
        return marked

    monkeypatch.setattr(rb_writer, "remove_playlist_node", reaches_further)
    plan = _plan(cfg)
    content, members = _content(cfg), _memberships(cfg)
    nodes = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")
    with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
        _apply(cfg, plan)
    assert raised.value.cause.reason == "whitelist-violation"
    assert genre in raised.value.cause.message
    assert (_content(cfg), _memberships(cfg)) == (content, members)
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == nodes


def test_a_move_that_lands_somewhere_else_is_refused_and_rolled_back(four_batches, monkeypatch):
    cfg, root_id, _old, _genre, _ids = four_batches
    real = rb_writer.move_playlist_node

    def misplaces(db, playlist, parent):
        real(db, playlist, parent)
        playlist.ParentID = root_id

    monkeypatch.setattr(rb_writer, "move_playlist_node", misplaces)
    plan = _plan(cfg)
    nodes = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")
    with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
        _apply(cfg, plan)
    assert "not live under the planned" in raised.value.cause.message
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == nodes


def test_the_writer_refuses_to_move_or_remove_a_folder(native_library):
    cfg, root_id = native_library
    folder = _node(cfg, "Lisa picks", under=root_id, folder=True)
    target = _node(cfg, "elsewhere", under=root_id, folder=True)
    handle = _open(cfg)
    try:
        row = handle.get_playlist(ID=folder)
        with pytest.raises(CratekitError) as moved:
            rb_writer.move_playlist_node(handle, row, handle.get_playlist(ID=target))
        with pytest.raises(CratekitError) as removed:
            rb_writer.remove_playlist_node(handle, row)
    finally:
        rb_writer.close_db(handle)
    assert "folder" in moved.value.cause.message and "folder" in removed.value.cause.message


def test_the_writer_refuses_a_parent_that_is_not_a_folder(native_library):
    cfg, root_id = native_library
    batch = _node(cfg, "2026-08-20 Set", under=root_id, age=44)
    plain = _node(cfg, "a playlist", under=root_id)
    handle = _open(cfg)
    try:
        with pytest.raises(CratekitError) as raised:
            rb_writer.move_playlist_node(
                handle, handle.get_playlist(ID=batch), handle.get_playlist(ID=plain)
            )
    finally:
        rb_writer.close_db(handle)
    assert "not a live folder" in raised.value.cause.message


def test_the_membership_move_commit_still_refuses_a_removed_playlist(native_library):
    """The membership move names its own table only, so a node marker is refused there."""
    cfg, root_id = native_library
    batch = _node(cfg, "2026-08-20 Set", under=root_id, age=44)
    handle = _open(cfg)
    try:
        setattr(handle.get_playlist(ID=batch), rb_writer.SOFT_DELETE_COLUMN, 1)
        with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
            rb_writer.commit_guarded(handle, removals=(rb_writer.MEMBERSHIP_TABLE,))
    finally:
        rb_writer.close_db(handle)
    assert "djmdPlaylist" in raised.value.cause.message
    assert not _node_row(cfg, batch)[2]


# ---------------------------------------------------------------------------
# The pure judge
# ---------------------------------------------------------------------------


def _tables(**changes) -> rb_writer.NodeTables:
    base = {
        "content": {"c1": "a digest"},
        "playlists": {
            "root": ("root", "INBOX", "", 1, 0),
            "old": ("old", "Old", "root", 2, 0),
            "b1": ("b1", "batch", "root", 3, 0),
            "b2": ("b2", "batch two", "old", 1, 0),
            "sib": ("sib", "sibling", "root", 4, 0),
        },
        "memberships": {
            "m1": ("m1", "b2", "c1", 0),
            "m2": ("m2", "g", "c1", 0),
        },
    }
    for key, value in changes.items():
        base[key] = {**base[key], **value}
    return rb_writer.NodeTables(
        content=base["content"],
        playlists=base["playlists"],
        memberships=base["memberships"],
        playlist_columns=("ID", "Name", "ParentID", "Seq", rb_writer.SOFT_DELETE_COLUMN),
        membership_columns=("ID", "PlaylistID", "ContentID", rb_writer.SOFT_DELETE_COLUMN),
    )


def _judge(after: rb_writer.NodeTables, **kwargs) -> list[str]:
    plan = {"moved": {"b1": "old"}, "removed": ["b2"], "created": ()}
    plan.update(kwargs)
    return rb_writer.node_change_violations(_tables(), after, **plan)


#: The reading after exactly the planned change: b1 moved to the end of Old,
#: its INBOX sibling closed up, b2 and its membership marked removed.
ADMITTED = {
    "playlists": {
        "b1": ("b1", "batch", "old", 2, 0),
        "b2": ("b2", "batch two", "old", 1, 1),
        "sib": ("sib", "sibling", "root", 3, 0),
    },
    "memberships": {"m1": ("m1", "b2", "c1", 1)},
}


def _after(**changes) -> rb_writer.NodeTables:
    merged = {key: dict(value) for key, value in ADMITTED.items()}
    for key, value in changes.items():
        merged[key] = {**merged.get(key, {}), **value}
    return _tables(**merged)


def test_the_judge_admits_exactly_the_planned_change():
    assert _judge(_after()) == []


@pytest.mark.parametrize(
    "after, expected",
    [
        (_after(content={"c1": "another digest"}), "djmdContent"),
        (_after(memberships={"m2": ("m2", "g", "c1", 1)}), "only a removed playlist"),
        (_after(memberships={"m1": ("m1", "b2", "c9", 1)}), "only its marker may go on"),
        (_after(memberships={"m1": ("m1", "b2", "c1", 0)}), "is still live"),
        (_after(memberships={"m3": ("m3", "g", "c1", 0)}), "added or disappeared"),
        (_after(playlists={"b1": ("b1", "batch", "sib", 2, 0)}), "not live under the planned"),
        (_after(playlists={"b1": ("b1", "batch", "root", 3, 0)}), "not live under the planned"),
        (_after(playlists={"b1": ("b1", "renamed", "old", 2, 0)}), "['Name']"),
        (_after(playlists={"b2": ("b2", "batch two", "old", 1, 0)}), "does not carry the marker"),
        (_after(playlists={"sib": ("sib", "sibling", "old", 3, 0)}), "['ParentID']"),
        (_after(playlists={"sib": ("sib", "sibling", "root", 3, 1)}), "rb_local_deleted"),
        (_after(playlists={"x": ("x", "x", "root", 9, 0)}), "unplanned"),
    ],
)
def test_the_judge_refuses_every_change_the_plan_does_not_explain(after, expected):
    violations = _judge(after)
    assert len(violations) == 1 and expected in violations[0], violations


def test_the_judge_refuses_a_renumbering_outside_the_parents_a_node_left_or_joined():
    """The binding renumbers INBOX and Old. A position moved anywhere else is not that."""
    base = _tables(playlists={"g1": ("g1", "genre", "genre-root", 1, 0)})
    after = _after(playlists={"g1": ("g1", "genre", "genre-root", 2, 0)})
    violations = rb_writer.node_change_violations(base, after, moved={"b1": "old"}, removed=["b2"])
    assert len(violations) == 1 and "['Seq']" in violations[0], violations


def test_the_judge_refuses_a_planned_change_that_was_never_made():
    """Asked whether it changed or not: a move or a removal that did nothing is a refusal."""
    violations = _judge(_tables())
    assert sorted(violations) == [
        "the djmdSongPlaylist row 'm1' of the removed playlist 'b2' is still live",
        "the moved playlist 'b1' is not live under the planned 'old'",
        "the removed playlist 'b2' does not carry the marker",
    ]


def test_a_commit_naming_the_rotation_tables_admits_a_node_marker_and_no_content_marker():
    removal = {rb_writer.SOFT_DELETE_COLUMN, "updated_at"}
    assert (
        rb_writer.guard_violations(
            [], [(rb_writer.PLAYLIST_TABLE, removal)], [], removals=rotate.REMOVALS
        )
        == []
    )
    refused = rb_writer.guard_violations(
        [], [(rb_writer.CONTENT_TABLE, removal)], [], removals=rotate.REMOVALS
    )
    assert len(refused) == 1 and "djmdContent" in refused[0]


# ---------------------------------------------------------------------------
# What the review of U111 asked for
# ---------------------------------------------------------------------------


def _removal_callers() -> dict[str, list[str]]:
    """Every ``removals=`` handed to the guarded commit or the whitelist in ``src``."""
    import ast

    src = Path(rb_writer.__file__).resolve().parents[1]
    found: dict[str, list[str]] = {}
    for path in sorted(src.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(
                node.func, "id", ""
            )
            if name not in {"commit_guarded", "assert_session_whitelisted", "guard_violations"}:
                continue
            for keyword in node.keywords:
                if keyword.arg == "removals":
                    found.setdefault(path.relative_to(src).as_posix(), []).append(
                        ast.unparse(keyword.value)
                    )
    return found


def test_only_the_rotation_asks_its_commit_to_admit_a_removed_playlist():
    """The playlist table is in the removable set, so who names it is held here.

    The membership move names its own table and nothing else, the rotation
    names its own tuple, and the writer's two judges pass the argument through.
    A new caller, or ``REMOVABLE_TABLES`` handed over whole, fails this.
    """
    assert _removal_callers() == {
        "core/rb_writer.py": ["removals", "removals"],
        "intake/rotate.py": ["REMOVALS"],
        "write/trees.py": ["(rb_writer.MEMBERSHIP_TABLE,)"],
        # U119. The genre Favorites refresh takes a favourite out of a folder's
        # Favorites in its second commit, the membership table alone, as the
        # move does, behind its own explicit gate.
        "write/genre_favorites.py": ["(rb_writer.MEMBERSHIP_TABLE,)"],
    }
    assert set(rotate.REMOVALS) == {rb_writer.PLAYLIST_TABLE, rb_writer.MEMBERSHIP_TABLE}


def _template_with(section: str) -> str:
    text = Path(taxonomy.__file__).resolve().parents[1].joinpath(
        "templates", "taxonomy.default.toml"
    ).read_text(encoding="utf-8")
    start = text.index("[intake_old]")
    end = text.index("\n\n", start)
    return text[:start] + section + text[end:]


@pytest.mark.parametrize(
    "declared, expected",
    [
        ("Old", "must be a table"),
        ({"id": "inbox", "display": "Old"}, "must differ from [intake]"),
        ({"id": "inbox_old", "display": "INBOX"}, "must differ from [intake]"),
    ],
)
def test_an_old_folder_declared_wrongly_is_a_taxonomy_problem_and_not_a_traceback(
    declared, expected
):
    import tomllib

    data = tomllib.loads(_template_with(""))
    data["intake_old"] = declared
    with pytest.raises(taxonomy.TaxonomyError) as raised:
        taxonomy.build_taxonomy(data)
    assert any(expected in problem for problem in raised.value.problems), raised.value.problems


def test_a_template_without_the_section_declares_no_old_folder():
    import tomllib

    assert taxonomy.build_taxonomy(tomllib.loads(_template_with(""))).intake_old is None
    assert DECLARED.intake_old == taxonomy.Node("inbox_old", "Old")


def test_the_name_a_landing_gives_is_the_shape_the_rotation_recognises(machine, monkeypatch):
    """One owner of the shape: what ``readable`` names, ``is_default_shape`` knows."""
    from cratekit.intake import batch_name

    monkeypatch.setattr(batch_name, "today", lambda: TODAY)
    for words in (batch_name.PLAYLISTS, batch_name.DOWNLOADS, "Sudbeat"):
        name = batch_name.free(machine, f"{batch_name.today().isoformat()} {words}")
        assert batch_name.is_default_shape(name), name
    assert batch_name.is_default_shape("2026-10-03 Tidal playlists 2")
    for name in ("listen later", "2026-10-03", "2026-10-03T101010Z-1_inboxed", "3_9_26 phil"):
        assert not batch_name.is_default_shape(name), name


def test_a_batch_created_late_in_the_evening_is_aged_from_its_local_day(
    native_library, monkeypatch
):
    """The row stores UTC. A batch made at 23:30 local is that day's, not tomorrow's.

    End to end through the binding, which converts to naive local time on read,
    so this pins the outcome and not the aware branch in ``_created_date``,
    which the pinned binding never reaches (mutation row C1).
    """
    cfg, root_id = native_library
    monkeypatch.setenv("TZ", "America/New_York")
    import time

    time.tzset()
    try:
        batch = _node(cfg, "2026-10-02 Set", under=root_id, batch_folder=True)
        handle = _open(cfg)
        try:
            row = handle.get_playlist(ID=batch)
            local = datetime(2026, 10, 2, 23, 30).astimezone()
            row.created_at = local
            handle.session.commit()
        finally:
            rb_writer.close_db(handle)
        stored = _query(cfg, "SELECT created_at FROM djmdPlaylist WHERE ID = ?", batch)[0][0]
        assert stored.startswith("2026-10-03"), stored
        (kept,) = _plan(cfg).kept
        assert (kept.landed, kept.age_days) == (date(2026, 10, 2), 1)
    finally:
        monkeypatch.delenv("TZ")
        time.tzset()


def test_a_landing_record_that_committed_nothing_dates_nothing(native_library):
    """A record naming a playlist whose commit never landed is not the batch's landing."""
    cfg, root_id = native_library
    batch = _node(cfg, "2026-09-30 Set", under=root_id, age=3, tracks=("t1",), batch_folder=True)
    refused = [state for state in session.SourceState if state is not session.SourceState.COMMITTED]
    _record_landing(cfg, batch, "2026-09-30 Set", TODAY - timedelta(days=60), source=refused[0])
    (kept,) = _plan(cfg).kept
    assert (kept.aged_from, kept.age_days) == (rotate.AGED_FROM_CREATED, 3)
