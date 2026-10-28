"""R-746: ``crate intake land`` on a library whose intake tree has cut over.

The same verb, the other medium. Every test here drives the real dispatcher
over real FLAC containers tagged through the product's own writer, against a
disposable database built the way the adoption suites build one, with the
intake tree recorded database native and anchored to a root folder the fixture
made. The bridge medium keeps ``tests/test_intake_land.py``; this file pins
what the native medium adds and what it must never write.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import gates
from cratekit.core import config, preflight, rb_writer, session, tags, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import ingest, land_cli, landing, native
from cratekit.write import row_link
from tests import adopt_fixtures, cutover_fixtures
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _row

DECLARED = taxonomy.default_taxonomy()
INTAKE = DECLARED.intake.id
BATCH = "2026-09-29_favourites"
GATE = land_cli.NATIVE_GATE
TODAY = date(2026, 9, 29)

#: Two devices, the first one NOT the library's, so a row stamped by the
#: binding's own default is stamped wrong and the writer has to choose. The
#: wrong one also sorts FIRST by identifier, so a choice that dropped the
#: MasterDBID rule and kept the sort would still pick wrong: the first table
#: measured a device row that sorted the right way by accident.
OTHER_DEVICE = ("d-aaa-other", "999")
MY_DEVICE = ("d-mine", "1")

#: The counter the binding's ``add_content`` copies into ``ContentLink``, the
#: TRACK menu item's ``rb_local_usn`` as seeded below, and the value rekordbox
#: wrote on the rows it made in this library (U126). Two numbers that differ,
#: so a landed row says which one it was given. Neither is the live library's:
#: the landing reads the value, it does not know it.
BINDING_LINK = 7
LIBRARY_LINK = 4242

#: The rows rekordbox made in the fixture library: the two the disposable
#: database is built with, ``1`` and ``2``, given its value here.
REKORDBOX_ROWS = ("1", "2")


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
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    (tmp_path / "staging").mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def _seed_binding_rows(cfg: config.Config) -> None:
    """The rows the binding's ``add_content`` reads, and the rows rekordbox made.

    The TRACK menu item and the devices are what the binding reads. The
    content rows the database is built with stand for rekordbox's own, and
    are given the ContentLink the landing reads off the library and gives its
    rows (U126).
    """
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(tables.DjmdMenuItems, ID="m-track", Name="TRACK", rb_local_usn=BINDING_LINK)
        )
        for content_id in REKORDBOX_ROWS:
            db_session.get(tables.DjmdContent, content_id).ContentLink = LIBRARY_LINK
        for device_id, master in (OTHER_DEVICE, MY_DEVICE):
            db_session.add(
                _row(tables.DjmdDevice, ID=device_id, MasterDBID=master, Name=device_id)
            )
        db_session.commit()
    engine.dispose()


@pytest.fixture
def machine(library, monkeypatch):
    """A set-up machine: a disposable database, the binding rows, an acknowledgment."""
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
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


@pytest.fixture
def acknowledged(machine):
    session.record_acknowledgment(machine, terminal=lambda: True)
    return machine


def _cut_over_intake(cfg: config.Config) -> str:
    """Record the intake tree native, anchored to a root folder made here."""
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


@pytest.fixture
def silence(tmp_path: Path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return synth_container(scratch, ".flac")


def _staging(cfg: config.Config) -> Path:
    return Path(cfg.paths.download_staging)


def _stage(cfg: config.Config, silence: Path, name: str, *, head: str = "01A - 124") -> Path:
    path = _staging(cfg) / name
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path,
        {"title": f"{head} - {Path(name).stem}", "artist": "Probe", "genre": "Deep House"},
    )
    return path


def _music(cfg: config.Config, batch: str = BATCH) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir / batch


def _staged_names(cfg: config.Config) -> list[str]:
    return sorted(p.name for p in _staging(cfg).glob("*.flac"))


def _staged_names_all(cfg: config.Config) -> list[str]:
    return sorted(p.name for p in _staging(cfg).iterdir() if p.is_file())


def _land(*extra: str) -> list[str]:
    return ["intake", "land", "--name", BATCH, *extra]


def _query(cfg: config.Config, sql: str, *params) -> list[tuple]:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _landed_rows(cfg: config.Config) -> list[tuple]:
    """(ID, Title, FolderPath) of every row under the batch folder, by name."""
    return _query(
        cfg,
        "SELECT ID, Title, FolderPath FROM djmdContent WHERE FolderPath LIKE ? "
        "ORDER BY FileNameL",
        f"%{BATCH}%",
    )


def _batch_playlist(cfg: config.Config) -> list[tuple]:
    return _query(cfg, "SELECT ID, ParentID, Attribute FROM djmdPlaylist WHERE Name = ?", BATCH)


def _members(cfg: config.Config, playlist_id: str) -> list[str]:
    rows = _query(
        cfg,
        "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY TrackNo",
        playlist_id,
    )
    return [str(row[0]) for row in rows]


def _two_acts(verb: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


# ---------------------------------------------------------------------------
# Three files land as three rows and one playlist under the adopted root
# ---------------------------------------------------------------------------


def test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root(
    native_library, silence
):
    cfg, root_id = native_library
    staged = [_stage(cfg, silence, name) for name in ("One.flac", "Three.flac", "Two.flac")]

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "ok"
    # The plan the person approved is the plan that was applied.
    assert refused["cause"]["detail"]["shown"]["digest"] == acted["data"]["digest"]
    assert _staged_names(cfg) == []
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["One.flac", "Three.flac", "Two.flac"]

    rows = _landed_rows(cfg)
    assert [Path(row[2]).name for row in rows] == ["One.flac", "Three.flac", "Two.flac"]
    for (_content_id, title, folder_path), source in zip(rows, sorted(staged)):
        landed = _music(cfg) / source.name
        assert folder_path == str(landed)
        # The R-740 name: the title tag's head kept, read off the landed file.
        assert title == ingest.read_meta(landed, cfg=cfg)["name"]
        assert title.startswith("01A - 124 - ")

    (playlist,) = _batch_playlist(cfg)
    playlist_id, parent, attribute = playlist
    assert str(parent) == root_id, "the batch playlist was not parented to the adopted root"
    assert int(attribute or 0) == 0, "the batch node is a folder, not a playlist"
    assert _members(cfg, str(playlist_id)) == [str(row[0]) for row in rows]

    totals = acted["data"]["totals"]
    assert totals == {
        "count": 3,
        "landed": 3,
        "refused": 0,
        "added": 3,
        "already present": 0,
        "memberships": 3,
    }
    # U127: no vocal calibration on this machine, so no row is tagged vox and
    # the landing says why rather than leaving the tag silently absent.
    assert [w["code"] for w in acted["warnings"]] == [
        land_cli.AWAITING_ANALYSIS,
        land_cli.VOX_NOT_WRITTEN,
    ]
    assert "Analyze" in acted["warnings"][0]["message"]
    assert "pending_human_action" not in acted or acted["pending_human_action"] is None

    # The session record is what a restore reads and what a revert of the
    # intake tree's cutover refuses over: the commit is recorded under the
    # tree for the memberships and under the content table for the rows.
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.CLOSED
    assert record.sources == {INTAKE: "committed"}
    assert {change.tree: change.created for change in record.change.trees} == {
        INTAKE: 3,
        rb_writer.CONTENT_TABLE: 3,
    }
    assert record.snapshot_path, "the capture the commit happened behind is not attached"
    # U111. The record names the batch playlist, which is where the rotation
    # reads a batch's landing date from.
    assert record.detail[native.BATCH_PLAYLIST_KEY] == {"id": str(playlist_id), "name": BATCH}


def test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads(
    native_library, silence
):
    """R-777. The pass is written with the commit, and ``landings_of_pass`` is
    what ``sync mark --pass`` reads as the proof the pass landed."""
    cfg, _root_id = native_library
    _stage(cfg, silence, "One.flac")

    code, acted, _refused = _two_acts(_land("--pass", "RUN_synced"))

    assert code == int(ExitCode.OK), acted
    (record,) = session.records(cfg)
    assert record.detail[native.PASS_KEY] == "RUN_synced"
    assert native.landings_of_pass(cfg, "RUN_synced") == (record.session_id,)
    assert native.landings_of_pass(cfg, "ANOTHER_synced") == ()


def test_a_landing_given_no_pass_names_none(native_library, silence):
    cfg, _root_id = native_library
    _stage(cfg, silence, "One.flac")
    code, acted, _refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    (record,) = session.records(cfg)
    assert native.PASS_KEY not in record.detail


def test_two_unnamed_landings_on_one_day_are_two_playlists_and_never_one(
    native_library, silence, monkeypatch
):
    """U110. The writer finds a playlist by its name under the root and adds to
    it, so the second landing's default name has to differ or the two batches
    merge silently. Each is named for the date, the second with `` 2``."""
    from cratekit.intake import batch_name

    cfg, root_id = native_library
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 3))
    _stage(cfg, silence, "One.flac")
    code, first, _ = _two_acts(["intake", "land"])
    assert code == int(ExitCode.OK), first
    _stage(cfg, silence, "Two.flac")

    code, second, _ = _two_acts(["intake", "land"])

    assert code == int(ExitCode.OK), second
    named = _query(
        cfg,
        "SELECT Name, ParentID FROM djmdPlaylist WHERE Name LIKE ? ORDER BY Name",
        "2026-10-03 Downloads%",
    )
    assert named == [("2026-10-03 Downloads", root_id), ("2026-10-03 Downloads 2", root_id)]
    assert [first["data"]["items"][-1]["playlist"], second["data"]["items"][-1]["playlist"]] == [
        "2026-10-03 Downloads",
        "2026-10-03 Downloads 2",
    ]


def test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing(
    native_library, silence, monkeypatch
):
    """U110. The name is chosen before the gate and the write comes after it,
    so another landing can take the name in between. Under the batch lock the
    native landing asks again and refuses stale, with no move and no row."""
    from cratekit.intake import batch_name

    cfg, _root_id = native_library
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 3))
    _stage(cfg, silence, "One.flac")
    real_lock = landing.batch_lock

    def take_then_lock(batch):
        (Path(cfg.library.root) / cfg.library.music_dir / batch).mkdir(parents=True)
        return real_lock(batch)

    monkeypatch.setattr(landing, "batch_lock", take_then_lock)

    code, acted, _ = _two_acts(["intake", "land"])

    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _staged_names(cfg) == ["One.flac"]
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name LIKE ?", "2026-10-03%") == []


def test_the_rows_carry_the_library_device_and_not_the_bindings_first(native_library, silence):
    """Sitting 17: the database holds two devices and ``get_device().first()``
    is order dependent. The row is stamped with the device whose MasterDBID is
    the property table's DBID, asserted rather than trusted."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    ((device_id, master),) = _query(
        cfg, "SELECT DeviceID, MasterDBID FROM djmdContent WHERE FolderPath LIKE ?", f"%{BATCH}%"
    )
    assert (str(device_id), str(master)) == MY_DEVICE


def test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes(native_library, silence):
    """R-923: a row the binding leaves NULL in these columns will not load to a
    deck. Read from SQL, every one carries rekordbox's own value, exactly."""
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted

    columns = list(rb_writer.CONTENT_ROW_DEFAULTS)
    rows = _query(
        cfg,
        f"SELECT ID, {', '.join(columns)} FROM djmdContent WHERE FolderPath LIKE ?",
        f"%{BATCH}%",
    )
    assert len(rows) == 2
    # COMPARED AS TEXT. The binding declares ``DJPlayCount`` a string and the
    # disposable schema is the binding's, where the live table declares an
    # integer and stores the binding's ``'0'`` as rekordbox's 0 by affinity.
    wanted = {column: str(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()}
    for content_id, *values in rows:
        found = {column: str(value) for column, value in zip(columns, values)}
        assert found == wanted, content_id
        assert None not in values, content_id
    assert not set(rb_writer.CONTENT_ROW_DEFAULTS) & rb_writer.CONTENT_ROW_EMPTY_COLUMNS


def test_the_rows_carry_the_landed_files_inode_as_their_file_id(native_library, silence):
    """U115, R-928: a row the binding makes carries a random ``rb_file_id`` and
    rekordbox will not load it to a deck. rekordbox's own value is the file's
    inode at import, so every landed row carries ``st_ino`` of its landed
    file, read from SQL and compared as text, and the envelope says so."""
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted

    rows = _query(
        cfg,
        f"SELECT ID, FolderPath, {rb_writer.FILE_ID_COLUMN} FROM djmdContent WHERE FolderPath LIKE ?",
        f"%{BATCH}%",
    )
    assert len(rows) == 2
    by_id: dict[str, str] = {}
    for content_id, folder_path, file_id in rows:
        landed = Path(folder_path)
        assert landed.is_file(), folder_path
        assert file_id is not None and str(file_id) == str(landed.stat().st_ino), content_id
        # Not the binding's random id: that is under 2 to the 28th by construction,
        # and the inode of a file on this machine is what the row holds instead.
        assert int(file_id) == landed.stat().st_ino
        by_id[str(content_id)] = str(file_id)
    landed_items = [item for item in acted["data"]["items"] if item["action"] == "landed"]
    assert len(landed_items) == 2
    for item in landed_items:
        assert item["row"][rb_writer.FILE_ID_COLUMN] == by_id[item["content_id"]]


def test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session(
    native_library, silence, monkeypatch
):
    """The restamp reads the inode once per row and the assertion reads it again
    after the commit. A first reading that lies, standing in for a binding or
    guard that drops the column, leaves a row rekordbox will not load, and the
    landing says so with the session to restore rather than exiting OK."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    real = native.file_id_of
    calls: list[Path] = []

    def lying_once(path: Path) -> int:
        calls.append(path)
        return real(path) + (1 if len(calls) == 1 else 0)

    monkeypatch.setattr(native, "file_id_of", lying_once)
    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "internal-error"
    assert rb_writer.FILE_ID_COLUMN in acted["cause"]["message"]
    (record,) = session.records(cfg)
    assert record.session_id in " ".join(acted["cause"]["remediation"]["steps"])
    ((file_id, folder_path),) = _query(
        cfg, f"SELECT {rb_writer.FILE_ID_COLUMN}, FolderPath FROM djmdContent WHERE FolderPath LIKE ?", f"%{BATCH}%"
    )
    assert int(file_id) == Path(folder_path).stat().st_ino + 1, "the write is durable"


def test_assert_rows_identified_is_pure_over_what_was_read_back(tmp_path):
    path = tmp_path / "a.flac"
    path.write_bytes(b"fLaC")
    right = native.AddedRow(
        target=path, content_id="1", title="t", folder_path=str(path), empty={},
        file_id=str(path.stat().st_ino), content_link=LIBRARY_LINK,
    )
    wrong = native.AddedRow(
        target=path, content_id="2", title="t", folder_path=str(path), empty={},
        file_id="73894078", content_link=LIBRARY_LINK,
    )
    native.assert_rows_identified(_landed(right, content_link=LIBRARY_LINK))
    with pytest.raises(CratekitError) as caught:
        native.assert_rows_identified(_landed(right, wrong, content_link=LIBRARY_LINK))
    assert caught.value.cause.reason == "internal-error"
    assert "2: " in caught.value.cause.message and "73894078" in caught.value.cause.message
    assert "restore session s-1" in " ".join(caught.value.cause.remediation.steps)


def _landed(*rows: native.AddedRow, content_link: int | None = None) -> native.NativeLanded:
    return native.NativeLanded(
        tree_id=INTAKE, playlist="p", playlist_id="9", added=tuple(rows), present=(),
        memberships_added=len(rows), session_id="s-1", content_link=content_link,
    )


# ---------------------------------------------------------------------------
# U126: the row is given the library's ContentLink, never the binding's
# ---------------------------------------------------------------------------


def _set_links(cfg: config.Config, links: dict[str, int | str | None]) -> None:
    """Put the named ContentLink on each named row of the disposable library."""
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        for content_id, link in links.items():
            conn.execute("UPDATE djmdContent SET ContentLink = ? WHERE ID = ?", (link, content_id))
        conn.commit()
    finally:
        conn.close()


def test_the_rows_carry_the_librarys_content_link_and_not_the_bindings(native_library, silence):
    """R-928, sitting 37: the binding gives a row the TRACK menu item's counter
    and rekordbox will not load it; given the value rekordbox's own rows
    carry, it loads. Every landed row carries the library's value, read from
    SQL, and the answer says so."""
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted

    rows = _query(
        cfg,
        f"SELECT ID, {rb_writer.CONTENT_LINK_COLUMN} FROM djmdContent WHERE FolderPath LIKE ?",
        f"%{BATCH}%",
    )
    assert len(rows) == 2
    assert {link for _id, link in rows} == {LIBRARY_LINK}
    assert BINDING_LINK != LIBRARY_LINK
    landed_items = [item for item in acted["data"]["items"] if item["action"] == "landed"]
    # A number in the answer as on the screen, never the text of one.
    assert [item["row"][rb_writer.CONTENT_LINK_COLUMN] for item in landed_items] == [
        LIBRARY_LINK
    ] * 2


def test_a_library_with_no_majority_content_link_refuses_before_the_gate(native_library, silence):
    """One value on one row and another on the other: neither is carried by
    more than half the live rows, so there is no value of rekordbox's to give,
    and the landing refuses by name with nothing moved and nothing written."""
    cfg, _root = native_library
    _set_links(cfg, {"2": 30})
    _stage(cfg, silence, "One.flac")
    rows_before = _query(cfg, "SELECT COUNT(*) FROM djmdContent")

    code, refused = drive(_land())

    assert code == int(ExitCode.LIBRARY_PREREQUISITE), refused
    assert refused["cause"]["reason"] == row_link.MAJORITY_UNCLEAR
    assert refused["cause"]["detail"]["rows"] == 2
    assert refused["cause"]["detail"]["carriers"] == 1
    assert _staged_names(cfg) == ["One.flac"]
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent") == rows_before
    assert session.records(cfg) == ()


def test_the_content_link_moves_the_digest(native_library, silence):
    """The value is part of what is approved: the same files planned against a
    library whose rows carry another value digest differently, so an approval
    taken at one value is never applied at another."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    _set_links(cfg, {"1": LIBRARY_LINK + 1, "2": LIBRARY_LINK + 1})
    code, second = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), second

    (one,) = first["cause"]["detail"]["shown"]["items"]
    (two,) = second["cause"]["detail"]["shown"]["items"]
    assert one["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
    assert two["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK + 1
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]


def test_an_approval_taken_at_one_content_link_is_not_applied_at_another(native_library, silence):
    """The library's rows move between the approval and the apply. The apply
    re-plans, the digest differs, and nothing lands with the value approved
    or the new one."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    _set_links(cfg, {"1": LIBRARY_LINK + 1, "2": LIBRARY_LINK + 1})

    code, acted = drive(["--run", run_id, *_land()])

    assert code != int(ExitCode.OK), acted
    assert _landed_rows(cfg) == []
    assert _staged_names(cfg) == ["One.flac"]


def test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit(
    native_library, silence, monkeypatch
):
    """A restamp that leaves the binding's value, standing in for a binding or
    guard that drops the column, is refused by the read back with the session
    to restore, rather than reporting a row rekordbox will not load as landed."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    real = native._restamp

    def keeping_the_bindings(content, row, plan):
        real(content, row, plan)
        setattr(content, rb_writer.CONTENT_LINK_COLUMN, BINDING_LINK)

    monkeypatch.setattr(native, "_restamp", keeping_the_bindings)
    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "internal-error"
    assert rb_writer.CONTENT_LINK_COLUMN in acted["cause"]["message"]
    (record,) = session.records(cfg)
    assert record.session_id in " ".join(acted["cause"]["remediation"]["steps"])
    ((link,),) = _query(
        cfg, f"SELECT {rb_writer.CONTENT_LINK_COLUMN} FROM djmdContent WHERE FolderPath LIKE ?",
        f"%{BATCH}%",
    )
    assert link == BINDING_LINK, "the write is durable"


def test_assert_rows_identified_holds_the_link_to_the_one_planned(tmp_path):
    path = tmp_path / "a.flac"
    path.write_bytes(b"fLaC")
    inode = str(path.stat().st_ino)
    right = native.AddedRow(
        target=path, content_id="1", title="t", folder_path=str(path), empty={},
        file_id=inode, content_link=LIBRARY_LINK,
    )
    wrong = native.AddedRow(
        target=path, content_id="2", title="t", folder_path=str(path), empty={},
        file_id=inode, content_link=BINDING_LINK,
    )
    native.assert_rows_identified(_landed(right, content_link=LIBRARY_LINK))
    with pytest.raises(CratekitError) as caught:
        native.assert_rows_identified(_landed(right, wrong, content_link=LIBRARY_LINK))
    assert caught.value.cause.reason == "internal-error"
    message = caught.value.cause.message
    assert f"2: {rb_writer.CONTENT_LINK_COLUMN} = {BINDING_LINK}" in message
    assert "1: " not in message
    # NO PLANNED VALUE IS NO PASS: a row added with nothing to hold it to is
    # refused, rather than the check going quiet.
    with pytest.raises(CratekitError) as caught:
        native.assert_rows_identified(_landed(right))
    assert f"1: {rb_writer.CONTENT_LINK_COLUMN}" in caught.value.cause.message


def test_a_landing_that_adds_no_row_needs_no_majority(native_library, silence):
    """Every file already in the collection: the landing writes memberships
    alone, so a library with no majority ContentLink does not refuse it, and
    no row on the screen claims a link it would not be given."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    held = str(_music(cfg) / "One.flac")
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, ContentLink, rb_local_deleted, "
        "created_at, updated_at) VALUES ('held-1', 'held', ?, 30, 0, '2026-01-01', '2026-01-01')",
        (held,),
    )
    conn.commit()
    conn.close()
    _set_links(cfg, {"2": 31})

    code, refused = drive(_land())

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 0 and shown["already present"] == 1
    assert shown["content link"] == "none, since no row is added"
    (item,) = shown["items"]
    assert rb_writer.CONTENT_LINK_COLUMN not in item["row"]


def test_the_content_link_counts_move_the_digest(native_library, silence):
    """The screen shows how many rows carry the value, so the digest covers
    the count as well: the same value carried by one more row is another plan."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, ContentLink, rb_local_deleted, created_at, updated_at) "
        "VALUES ('rb-made', ?, 0, '2026-01-01', '2026-01-01')",
        (LIBRARY_LINK,),
    )
    conn.commit()
    conn.close()
    code, second = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert second["cause"]["detail"]["shown"]["content link"].endswith("3 of the library's 3 live rows")
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]


class _Handle:
    """What ``library_link`` reads through: a handle with a session on the file."""

    def __init__(self, path: Path):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session

        self.engine = create_engine(f"sqlite:///{path}")
        self.session = Session(self.engine)

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()


def _majority(cfg: config.Config, rows: dict[str, tuple[int | str | None, int]]):
    """Replace the library's content rows with ``rows`` (link, deleted) and read the majority."""
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("DELETE FROM djmdContent")
        for content_id, (link, deleted) in rows.items():
            conn.execute(
                "INSERT INTO djmdContent (ID, ContentLink, rb_local_deleted, created_at, "
                "updated_at) VALUES (?, ?, ?, '2026-01-01', '2026-01-01')",
                (content_id, link, deleted),
            )
        conn.commit()
    finally:
        conn.close()
    handle = _Handle(Path(cfg.library.db_path))
    try:
        return row_link.library_link(handle)
    finally:
        handle.close()


@pytest.mark.parametrize(
    ("rows", "carriers"),
    [
        # Three of four: a majority.
        ({"a": (9, 0), "b": (9, 0), "c": (9, 0), "d": (5, 0)}, 3),
        # Removed rows are not the library's: two live of two, whatever the dead carry.
        ({"a": (9, 0), "b": (9, 0), "c": (5, 1), "d": (5, 1), "e": (5, 1)}, 2),
        # Stored as text, as the binding's affinity can leave it, still a whole number.
        ({"a": ("9", 0), "b": (9, 0), "c": (None, 0)}, 2),
    ],
)
def test_the_library_link_is_the_value_more_than_half_the_live_rows_carry(machine, rows, carriers):
    found = _majority(machine, rows)
    assert found.value == 9
    assert found.carriers == carriers
    assert found.rows == sum(1 for _link, deleted in rows.values() if not deleted)


@pytest.mark.parametrize(
    "rows",
    [
        # Exactly half is not more than half.
        {"a": (9, 0), "b": (9, 0), "c": (5, 0), "d": (6, 0)},
        # A plurality is a guess.
        {"a": (9, 0), "b": (9, 0), "c": (5, 0), "d": (6, 0), "e": (7, 0)},
        # A majority of NULL is no value.
        {"a": (None, 0), "b": (None, 0), "c": (9, 0)},
        # Not a whole number, in three shapes a looser test let through to int().
        {"a": ("x9", 0), "b": ("x9", 0), "c": (9, 0)},
        {"a": ("--5", 0), "b": ("--5", 0), "c": (9, 0)},
        {"a": ("\u00b2", 0), "b": ("\u00b2", 0), "c": (9, 0)},
        # Every row removed, so no live row carries anything.
        {"a": (9, 1), "b": (9, 1)},
        # No rows at all.
        {},
    ],
)
def test_no_majority_link_refuses_by_name(machine, rows):
    with pytest.raises(CratekitError) as caught:
        _majority(machine, rows)
    assert caught.value.cause.reason == row_link.MAJORITY_UNCLEAR
    assert caught.value.cause.detail["column"] == rb_writer.CONTENT_LINK_COLUMN


def test_the_link_is_not_an_analysis_column_and_not_bookkeeping():
    """Given on a created row, so the creation policy must admit it, and never
    blinded for every writer by being called bookkeeping."""
    assert rb_writer.CONTENT_LINK_COLUMN not in rb_writer.CONTENT_ROW_EMPTY_COLUMNS
    assert rb_writer.CONTENT_LINK_COLUMN not in rb_writer.BOOKKEEPING_COLUMNS
    assert rb_writer.CONTENT_LINK_COLUMN not in native.LEFT_EMPTY


def test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column(
    native_library, silence
):
    """The standing constraint, asserted from SQL on the rows as rekordbox will
    find them: the ten columns an analysis pass fills, and no cue, mixer or
    file row naming the new rows."""
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted

    selected = ", ".join(native.LEFT_EMPTY)
    rows = _query(cfg, f"SELECT ID, {selected} FROM djmdContent WHERE FolderPath LIKE ?", f"%{BATCH}%")
    assert len(rows) == 2
    for row in rows:
        content_id, *values = row
        for name, value in zip(native.LEFT_EMPTY, values):
            assert value in (None, 0, 0.0, "", "0"), f"row {content_id} carries {name}={value!r}"
        for table in rb_writer.CONTENT_ANALYSIS_TABLES:
            (count,) = _query(cfg, f"SELECT COUNT(*) FROM {table} WHERE ContentID = ?", content_id)[0]
            assert count == 0, f"{table} holds a row for the new content row {content_id}"
    # And the envelope names the columns left for rekordbox, on every landed item.
    landed = [item for item in acted["data"]["items"] if item["action"] == "landed"]
    assert all(item["left_empty"] == sorted(native.LEFT_EMPTY) for item in landed)


def test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database(
    native_library, silence
):
    cfg, root_id = native_library
    _stage(cfg, silence, "One.flac")
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["reads and writes"] == str(cfg.library.db_path)
    assert shown["playlist"] == f"{BATCH} under {DECLARED.intake.display} (row {root_id})"
    assert shown["left empty for rekordbox"] == list(native.LEFT_EMPTY)
    assert shown["adds"] == 1 and shown["already present"] == 0
    (item,) = shown["items"]
    assert item["action"] == native.ADD
    assert item["to"] == str(_music(cfg) / "One.flac")
    assert set(item["row"]) == {
        "Title",
        "FolderPath",
        "FileNameL",
        "FileSize",
        "FileType",
        rb_writer.FILE_ID_COLUMN,
        rb_writer.CONTENT_LINK_COLUMN,
    }
    # THE LIBRARY'S VALUE, shown with its count, never the binding's (U126).
    assert item["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
    assert shown["content link"] == (
        f"{LIBRARY_LINK}, carried by 2 of the library's 2 live rows"
    )
    # U115: the file id is named as the sentence it is, since the number is
    # read on the landed file when the row is made and no plan can know it.
    assert item["row"][rb_writer.FILE_ID_COLUMN] == native.FILE_ID_AT_LANDING
    assert item["row"]["FileType"] == 5, "FLAC is file type 5 in the binding"
    # Nothing moved and nothing was written for a plan nobody answered.
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg).exists()
    assert _landed_rows(cfg) == [] and _batch_playlist(cfg) == []


def test_the_native_gate_takes_no_inline_answer(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(["-d", f"{GATE}=apply", *_land()])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["gate"] == GATE
    assert _staged_names(cfg) == ["One.flac"]
    assert _landed_rows(cfg) == []


def test_an_abort_moves_nothing_and_writes_nothing(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, refused = drive(_land())
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *_land()])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _staged_names(cfg) == ["One.flac"]
    assert _landed_rows(cfg) == [] and _batch_playlist(cfg) == []


# ---------------------------------------------------------------------------
# A file already in the collection, and a second run
# ---------------------------------------------------------------------------


def test_a_file_already_in_the_collection_is_present_and_not_added_twice(native_library, silence):
    cfg, root_id = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    # A row rekordbox already holds for the path Two.flac will land at.
    held = str(_music(cfg) / "Two.flac")
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('held-2', 'held', ?, 0, '2026-01-01', '2026-01-01')",
        (held,),
    )
    conn.commit()
    conn.close()

    code, refused = drive(_land())
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 1 and shown["already present"] == 1
    present = [item for item in shown["items"] if item["action"] == native.PRESENT]
    assert [item["content_id"] for item in present] == ["held-2"]
    # THE LINK ONLY WHERE A ROW IS ADDED (U126): the held row is not written,
    # so it claims no value, and the added one carries the library's.
    assert rb_writer.CONTENT_LINK_COLUMN not in present[0]["row"]
    (added,) = [item for item in shown["items"] if item["action"] == native.ADD]
    assert added["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK

    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["added"] == 1
    assert acted["data"]["totals"]["already present"] == 1
    rows = _query(cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", held)
    assert rows == [("held-2",)], "the held file gained a second row"
    (playlist,) = _batch_playlist(cfg)
    members = _members(cfg, str(playlist[0]))
    assert len(members) == 2 and members[1] == "held-2", "the batch playlist is the batch, in order"


def test_a_second_approved_run_over_the_landed_files_adds_nothing(native_library, silence):
    """Driven at the engine, where the same files can be planned twice: the
    second plan reads every row present and the apply inserts no row and no
    membership."""
    cfg, _root = native_library
    folder = _music(cfg)
    folder.mkdir(parents=True)
    files = []
    for name in ("One.flac", "Two.flac", "Three.flac"):
        path = _stage(cfg, silence, name)
        landed = folder / name
        shutil.move(path, landed)
        files.append((landed, landed))
    registry = tree_registry.read(cfg)

    def run() -> native.NativeLanded:
        db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
        try:
            plan = native.plan_rows(cfg, db, tree_id=INTAKE, registry=registry, batch=BATCH, files=files)
            return native.apply_rows(cfg, db, plan, analysis_roots=[Path(cfg.library.root)])
        finally:
            rb_writer.close_db(db)

    first = run()
    assert len(first.added) == 3 and first.memberships_added == 3
    second = run()
    assert second.added == () and second.memberships_added == 0
    assert len(second.present) == 3
    assert len(_landed_rows(cfg)) == 3
    (playlist,) = _batch_playlist(cfg)
    assert len(_members(cfg, str(playlist[0]))) == 3


def test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged(
    native_library, silence
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    before = _landed_rows(cfg)
    _stage(cfg, silence, "One.flac")

    code, again = drive(_land())
    # The plan reads the file as present, because the row holds its target.
    assert again["cause"]["detail"]["shown"]["already present"] == 1
    code, acted, _ = _two_acts(_land())
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "intake-list-unusable"
    assert "One.flac" in acted["cause"]["message"]
    assert _landed_rows(cfg) == before
    assert _staged_names(cfg) == ["One.flac"]


# ---------------------------------------------------------------------------
# Refused before the gate
# ---------------------------------------------------------------------------


def _assert_refused_before_the_gate(cfg: config.Config, code: int, envelope: dict, reason: str):
    assert envelope["cause"]["reason"] == reason, envelope
    assert code != int(ExitCode.OK)
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert not gates.run_path(envelope["run_id"]).exists()
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg).exists()
    assert _landed_rows(cfg) == [] and _batch_playlist(cfg) == []


def test_an_intake_tree_on_the_bridge_is_refused_before_the_gate_naming_the_cutover(
    acknowledged, silence
):
    """No --export and no cutover: the xml landing wants its export, and the
    refusal names the verb that would move the intake tree off the bridge."""
    cfg = acknowledged
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land())
    _assert_refused_before_the_gate(cfg, code, envelope, "library-export-unusable")
    steps = " ".join(envelope["cause"]["remediation"]["steps"])
    assert f"crate tree cutover {INTAKE}" in steps and "--export" in steps


def test_the_engine_refuses_a_bridge_tree_naming_the_cutover(acknowledged):
    cfg = acknowledged
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        with pytest.raises(CratekitError) as raised:
            native.anchored_intake_root(db, INTAKE, tree_registry.read(cfg))
    finally:
        rb_writer.close_db(db)
    cause = raised.value.cause
    assert cause.reason == "tree-unconverged"
    assert any(f"crate tree cutover {INTAKE}" in step for step in cause.remediation.steps)


def test_no_acknowledgment_refuses_before_the_gate(machine, silence):
    """R-733's lesson: the acknowledgment is read before the gate is asked,
    and a missing one refuses with the mint as its remedy."""
    cfg = machine
    _cut_over_intake(cfg)
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land())
    _assert_refused_before_the_gate(cfg, code, envelope, "backup-acknowledgment-missing")
    assert envelope["cause"]["remediation"]["remedy"] == "acknowledge-backup"


def test_rekordbox_running_refuses_before_the_gate(native_library, silence, monkeypatch):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    code, envelope = drive(_land())
    _assert_refused_before_the_gate(cfg, code, envelope, "rekordbox-running")


def test_an_export_on_a_native_tree_is_refused_before_the_gate(native_library, silence, tmp_path):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    export = tmp_path / "fresh.xml"
    export.write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")
    code, envelope = drive(_land("--export", str(export)))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "--export" in envelope["cause"]["message"]


def test_an_empty_staging_folder_is_a_plan_of_nothing_and_asks_no_explicit_gate(
    native_library,
):
    """Staging is empty after every landing. An explicit gate is the price of a
    new kind of write, not of learning there is nothing to move, so a plan of
    nothing answers no_op in one invocation and opens nothing."""
    cfg, _root = native_library
    code, envelope = drive(_land())
    assert code == int(ExitCode.OK) and envelope["outcome"] == "no_op", envelope
    assert envelope["data"]["items"] == [] and envelope["data"]["totals"] == {"count": 0}
    assert "gate" not in (envelope.get("cause") or {})
    assert _landed_rows(cfg) == [] and _batch_playlist(cfg) == []


# ---------------------------------------------------------------------------
# A failure on the second of three files
# ---------------------------------------------------------------------------


def test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac", "Three.flac"):
        _stage(cfg, silence, name)
    from pyrekordbox.db6.database import Rekordbox6Database

    real = Rekordbox6Database.add_content
    calls: list[str] = []

    def failing(self, path, **kwargs):
        calls.append(Path(path).name)
        if len(calls) == 2:
            raise RuntimeError("the second file broke the binding")
        return real(self, path, **kwargs)

    monkeypatch.setattr(Rekordbox6Database, "add_content", failing)

    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert len(calls) == 2
    message = acted["cause"]["message"]
    assert "no row was added" in message
    assert "3 file(s) were already moved into the library and stay there" in message
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["One.flac", "Three.flac", "Two.flac"]
    assert _staged_names(cfg) == []
    assert _landed_rows(cfg) == [], "a row landed although the commit never happened"
    assert _batch_playlist(cfg) == []
    records = session.records(cfg)
    assert [record.state for record in records] == [session.SessionState.ABANDONED]


def test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit(
    native_library, silence, monkeypatch
):
    """The guard's read back sees a flushed creation (R-760). The value is put
    on the row by SQL after the binding flushed it, where the in memory judge
    cannot see it, and the commit is refused on the row as stored."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    from sqlalchemy import text

    real = native._restamp

    def restamp_and_taint(content, row, plan):
        real(content, row, plan)
        # The binding flushed the row, so its id is assigned and an UPDATE by
        # SQL reaches the stored row without touching the mapped object.
        content._sa_instance_state.session.execute(
            text("UPDATE djmdContent SET BPM = 12400 WHERE ID = :id"), {"id": str(content.ID)}
        )

    monkeypatch.setattr(native, "_restamp", restamp_and_taint)

    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "whitelist-violation"
    assert "BPM" in acted["cause"]["message"]
    assert _landed_rows(cfg) == [], "a row carrying a tempo was committed"
    assert _batch_playlist(cfg) == []


def test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit(
    native_library, silence, monkeypatch
):
    """The key is one of the five columns a content row is held to beyond the
    playlist tables' five (R-746): an analysis output here and nowhere else.
    Tainted by SQL after the flush, as the tempo is above, so the read back is
    what refuses it, and it refuses because the content policy is the wider
    list and not the playlist one."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    from sqlalchemy import text

    real = native._restamp

    def restamp_and_key(content, row, plan):
        real(content, row, plan)
        content._sa_instance_state.session.execute(
            text("UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id"),
            {"id": str(content.ID)},
        )

    monkeypatch.setattr(native, "_restamp", restamp_and_key)

    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "whitelist-violation"
    assert "KeyID" in acted["cause"]["message"]
    assert _landed_rows(cfg) == []


def test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit(
    native_library, silence, monkeypatch
):
    """The other half of the column policy: no cue, mixer or file row may name
    a row this product creates. Planted by SQL after the flush, the way an
    analysis pass would write one, and the commit is refused on it."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    from sqlalchemy import text

    real = native._restamp

    def restamp_and_plant(content, row, plan):
        real(content, row, plan)
        content._sa_instance_state.session.execute(
            text(
                "INSERT INTO djmdMixerParam (ID, ContentID, rb_local_deleted, created_at, "
                "updated_at) VALUES ('mp-1', :id, 0, '2026-01-01', '2026-01-01')"
            ),
            {"id": str(content.ID)},
        )

    monkeypatch.setattr(native, "_restamp", restamp_and_plant)

    code, acted, _ = _two_acts(_land())

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "whitelist-violation"
    assert "djmdMixerParam" in acted["cause"]["message"]
    assert _landed_rows(cfg) == []
    assert _query(cfg, "SELECT COUNT(*) FROM djmdMixerParam")[0] == (0,)


# ---------------------------------------------------------------------------
# What is stored: the base drive form
# ---------------------------------------------------------------------------


def test_folder_path_is_stored_under_the_base_drive_rekordbox_records(
    native_library, silence, tmp_path
):
    """Sitting 17: rekordbox's own rows store the base drive prefix, which on
    a renamed volume is not the mounted path. The mounted path is what the
    binding stats; the base drive form is what the row carries."""
    cfg, _root = native_library
    # The drive rekordbox made the database on is a name this machine no longer
    # mounts, and the current drive is the temporary root the library sits under.
    base = str(tmp_path.parent / "old-drive")
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "UPDATE djmdProperty SET BaseDBDrive = ?, CurrentDBDrive = ?",
        (base + "/", str(tmp_path) + "/"),
    )
    conn.commit()
    conn.close()
    _stage(cfg, silence, "One.flac")

    code, refused = drive(_land())
    shown = refused["cause"]["detail"]["shown"]
    expected = base + "/library/Music/" + BATCH + "/One.flac"
    assert shown["items"][0]["row"]["FolderPath"] == expected
    assert shown["paths stored"].startswith(f"under the base drive {base}")

    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    ((folder_path,),) = _query(cfg, "SELECT FolderPath FROM djmdContent WHERE Title LIKE '%One%'")
    assert folder_path == expected
    assert (_music(cfg) / "One.flac").is_file()


def test_the_stored_path_is_nfc_and_the_swap_is_anchored_on_a_whole_component(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    assert native.stored_folder_path(
        new / "Music" / "a.flac", base_drive=str(old), current_drive=str(new)
    ) == str(old / "Music" / "a.flac")
    # A sibling drive whose name merely begins with the current one is not under it.
    newer = tmp_path / "newer"
    assert native.stored_folder_path(
        newer / "Music" / "a.flac", base_drive=str(old), current_drive=str(new)
    ) == str(newer / "Music" / "a.flac")
    # No drives recorded: the mounted path, composed.
    decomposed = tmp_path / "No\u0308pi.flac"
    assert native.stored_folder_path(decomposed, base_drive=None, current_drive=None) == str(
        tmp_path / "N\u00f6pi.flac"
    )


def test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands(
    native_library, silence
):
    """One file's problem is one file's refusal, as an occupied target is on the
    bridge. The xml landing takes every suffix AUDIO_EXTS names, because a
    Location is text; the binding's file type is an enum of five."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    odd = _stage(cfg, silence, "Two.flac")
    odd.rename(odd.with_suffix(".opus"))

    code, refused = drive(_land())
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 1 and shown["left in staging"] == 1
    (planned_odd,) = [item for item in shown["items"] if item["action"] == native.UNSUPPORTED]
    assert "Two.opus" in planned_odd["why"] and "left in staging" in planned_odd["why"]

    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    assert _staged_names_all(cfg) == ["Two.opus"]
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["One.flac"]
    assert [Path(row[2]).name for row in _landed_rows(cfg)] == ["One.flac"]
    assert acted["data"]["totals"]["refused"] == 1 and acted["data"]["totals"]["added"] == 1
    assert any("Two.opus" in w["message"] for w in acted["warnings"])


def test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too(
    native_library, silence, monkeypatch
):
    """The bridge leaves such a file to be tagged and landed again, and so does
    this medium: a row added for it would sit in the intake with no route. The
    shipped taxonomy declares a sub for every file, so the placement check is
    driven at its seam, and what this proves is that the native landing asks
    it at all, which the first cut of the medium did not."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    real = landing._unplaceable

    def unplaceable(path, declared):
        if path.name == "Two.flac":
            return landing.Refused(
                path=path,
                reason="intake-list-unusable",
                sentence=f"{path.name} resolves to a bucket with no declared sub, so it "
                f"was left in staging; run crate tag folder over it and land it again",
            )
        return real(path, declared)

    monkeypatch.setattr(landing, "_unplaceable", unplaceable)

    code, acted, _ = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    assert _staged_names(cfg) == ["Two.flac"]
    assert [Path(row[2]).name for row in _landed_rows(cfg)] == ["One.flac"]
    (warning,) = [w for w in acted["warnings"] if w["code"] == "intake-list-unusable"]
    assert "Two.flac" in warning["message"] and "tag folder" in warning["message"]


def test_the_landing_engine_module_is_the_only_caller_that_admits_a_content_row():
    """The counterpart of the guard's own source test, read from the verb's side."""
    source = Path(landing.__file__).read_text(encoding="utf-8")
    assert "creations=" not in source, "the landing module asks the writer itself"


# ---------------------------------------------------------------------------
# The digest names the library, not the database file (U161, R-922)
# ---------------------------------------------------------------------------


def _point_at_a_copy(cfg: config.Config) -> Path:
    """Copy the disposable database to another path under the library and point the config at it.

    What a rehearsal does by design: the same library, read through a copy
    whose file is elsewhere. The device, the master id and every row are the
    database's own, so only the path differs.
    """
    # ANOTHER FILE NAME AS WELL AS ANOTHER FOLDER, so a digest of the bare
    # name would differ too.
    copy = Path(cfg.library.root) / "rehearsal" / "master-copy.db"
    copy.parent.mkdir(parents=True)
    shutil.copyfile(cfg.library.db_path, copy)
    data = valid_data(
        Path(cfg.library.root),
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    data["library"]["db_path"] = str(copy)
    moved = config.from_dict(data)
    config.save(moved)
    config.reset_cache()
    return copy


def _spy_identity(monkeypatch) -> list[dict]:
    """Every identity the engine digests, in the order it was taken."""
    taken: list[dict] = []
    real = native.identity

    def spying(plan):
        found = real(plan)
        taken.append(found)
        return found

    monkeypatch.setattr(native, "identity", spying)
    return taken


def _strings(value) -> list[str]:
    """Every string anywhere in a nested identity, keys and values both."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for key, one in value.items() for s in (*_strings(key), *_strings(one))]
    if isinstance(value, (list, tuple)):
        return [s for one in value for s in _strings(one)]
    return []


def test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path(
    native_library, silence
):
    """R-922. A rehearsal reads a copy at another path, so a digest that named
    the file could never equal the live one. The same staged files planned
    against the database and against its copy digest the same, and each gate
    screen still says which file it reads and writes."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    live_path = str(cfg.library.db_path)
    code, live = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), live

    copy = _point_at_a_copy(cfg)
    code, rehearsed = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), rehearsed

    shown_live = live["cause"]["detail"]["shown"]
    shown_copy = rehearsed["cause"]["detail"]["shown"]
    assert shown_live["reads and writes"] == live_path
    assert shown_copy["reads and writes"] == str(copy)
    assert shown_live["items"] == shown_copy["items"]
    assert shown_live["digest"] == shown_copy["digest"]
    # Nothing moved and nothing was written by either plan.
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    assert _landed_rows(cfg) == []


def test_the_engine_identity_names_the_device_and_master_id_and_no_database_path(
    native_library, silence, monkeypatch
):
    """The device and the master id are what identify the library, so they stay
    in what is digested; the file path is nowhere in it, as a key or a value."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    taken = _spy_identity(monkeypatch)
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused

    assert taken, "the engine took no identity"
    for one in taken:
        assert one["device"] == MY_DEVICE[0]
        assert one["master_db_id"] == MY_DEVICE[1]
        assert "database" not in one
        database = Path(cfg.library.db_path)
        named = _strings(one)
        assert not [s for s in named if str(database) in s or str(database.parent) == s], named


def test_a_changed_playlist_or_an_added_file_still_moves_the_digest(native_library, silence):
    """Taking the path out takes nothing else out: the batch playlist's name and
    one more row each move the digest."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    code, renamed = drive(["intake", "land", "--name", f"{BATCH}_other"])
    assert code == int(ExitCode.DECISION_REQUIRED), renamed
    _stage(cfg, silence, "Two.flac")
    code, grown = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), grown

    digests = {
        envelope["cause"]["detail"]["shown"]["digest"] for envelope in (first, renamed, grown)
    }
    assert len(digests) == 3, digests


def test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path(
    native_library, silence, monkeypatch
):
    """The engine's own digest, read off the plan it returns: the copy's path
    leaves it alone, and one row's column or the playlist's name moves it."""
    from dataclasses import replace

    from cratekit.cli.output import digest_of

    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    plans: list[native.NativePlan] = []
    real = native.identity

    def keeping(plan):
        plans.append(plan)
        return real(plan)

    monkeypatch.setattr(native, "identity", keeping)
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    plan = plans[-1]
    base = digest_of(real(plan))

    elsewhere = replace(plan, database=Path(cfg.library.root) / "rehearsal" / "master.db")
    assert digest_of(real(elsewhere)) == base
    (row,) = plan.rows
    renamed_row = replace(row, title=f"{row.title} (edit)")
    assert digest_of(real(replace(plan, rows=(renamed_row,)))) != base
    assert digest_of(real(replace(plan, playlist=f"{plan.playlist}_other"))) != base
    assert digest_of(real(replace(plan, device_id=OTHER_DEVICE[0]))) != base
    assert digest_of(real(replace(plan, master_db_id=OTHER_DEVICE[1]))) != base


def test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing(
    native_library, silence, monkeypatch
):
    """An answer recorded by a build whose digest still named the file is bound
    to that digest. The continuation plans the new one, refuses stale, and
    moves and writes nothing, rather than accepting the old answer."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    real = native.identity
    monkeypatch.setattr(
        native, "identity", lambda plan: {**real(plan), "database": str(plan.database)}
    )
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    monkeypatch.setattr(native, "identity", real)

    code, acted = drive(["--run", run_id, *_land()])

    assert acted["cause"]["reason"] == "decision-stale", acted
    assert acted["cause"]["detail"]["expected"] == refused["cause"]["detail"]["shown"]["digest"]
    assert _staged_names(cfg) == ["One.flac"]
    assert _landed_rows(cfg) == []
    assert _batch_playlist(cfg) == []


def test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another(
    native_library, silence
):
    """The review of U161, driven. With the path out of the digest, the config
    pointed at a copy of the same library between the answer and the
    continuation digests equal, and the write used to land in the copy the
    screen never named. The file is pinned on the run, so the continuation is
    refused stale naming both files, and neither database gains a row."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    live_path = str(cfg.library.db_path)
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["reads and writes"] == live_path
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope

    copy = _point_at_a_copy(cfg)
    code, acted = drive(["--run", run_id, *_land()])

    assert code == int(ExitCode.DECISION_STALE), acted
    detail = acted["cause"]["detail"]
    assert detail["pinned"] == land_cli.DATABASE_PIN
    assert detail["expected"] == live_path and detail["actual"] == str(copy)
    assert _staged_names(cfg) == ["One.flac"]
    for database in (live_path, str(copy)):
        conn = sqlite3.connect(database)
        try:
            landed = conn.execute(
                "SELECT ID FROM djmdContent WHERE FolderPath LIKE ?", (f"%{BATCH}%",)
            ).fetchall()
        finally:
            conn.close()
        assert landed == [], database


def test_an_answer_continued_over_the_file_it_was_given_over_lands(native_library, silence):
    """The pin's other side: the same file at both acts takes the answer."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, acted, _refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    assert len(_landed_rows(cfg)) == 1
