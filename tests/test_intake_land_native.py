"""R-746: ``crate intake land`` on a cut over intake tree, D1 applying.

What the native medium adds and must never write; the bridge keeps ``test_intake_land.py``."""

from __future__ import annotations

import shutil
import sqlite3
from contextlib import closing, contextmanager
from dataclasses import replace
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.cli import gates
from cratekit.cli.output import digest_of
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
#: The folder a native landing files BATCH in (U164), spelled here, not by the engine.
FILED_AS = "09_29_26 favourites"
GATE = land_cli.NATIVE_GATE
TODAY = date(2026, 9, 29)

#: The first device is NOT the library's and sorts first, so a writer that kept
#: the binding's default or dropped the MasterDBID rule for the sort stamps wrong.
OTHER_DEVICE = ("d-aaa-other", "999")
MY_DEVICE = ("d-mine", "1")

#: The TRACK menu counter ``add_content`` copies into ``ContentLink``, and the
#: value rekordbox wrote on its own rows here (U126): two, so a row says which.
BINDING_LINK = 7
LIBRARY_LINK = 4242

#: The rows rekordbox made: the two the disposable database is built with.
REKORDBOX_ROWS = ("1", "2")

#: The silent container, synthesised once per process, since ffmpeg writes the same bytes.
_SILENCE: list[bytes] = []


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
        rb_writer, "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0})
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False))


@pytest.fixture
def library(tmp_path, monkeypatch):
    return _library_root(tmp_path, monkeypatch)


def _library_root(tmp_path: Path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    (tmp_path / "staging").mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def _config_data(root: Path, profile: str | None = None) -> dict:
    data = valid_data(
        root, rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"})
    if profile is not None:
        data["profile"] = {"name": profile}
    return data


def _seed_binding_rows(cfg: config.Config) -> None:
    """What ``add_content`` reads, and rekordbox's rows given the library's ContentLink (U126)."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(tables.DjmdMenuItems, ID="m-track", Name="TRACK", rb_local_usn=BINDING_LINK))
        for content_id in REKORDBOX_ROWS:
            db_session.get(tables.DjmdContent, content_id).ContentLink = LIBRARY_LINK
        for device_id, master in (OTHER_DEVICE, MY_DEVICE):
            db_session.add(_row(tables.DjmdDevice, ID=device_id, MasterDBID=master, Name=device_id))
        db_session.commit()
    engine.dispose()


@pytest.fixture
def machine(library, monkeypatch):
    """A set-up machine: a disposable database, the binding rows, an acknowledgment."""
    return _configured(library, monkeypatch)


def _configured(root: Path, monkeypatch, *, profile: str | None = None) -> config.Config:
    resolved = config.from_dict(_config_data(root, profile))
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, ())
    _seed_binding_rows(resolved)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id))
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
                tree_id=INTAKE, mode=tree_registry.Mode.DATABASE, cutover_on=TODAY, root_id=root_id,
                source=tree_registry.DerivationSource.TAXONOMY)))
    return root_id


@pytest.fixture
def native_library(acknowledged):
    """The acknowledged machine with its intake tree cut over. Answers (cfg, root id)."""
    return acknowledged, _cut_over_intake(acknowledged)


@pytest.fixture
def one_staged(native_library, silence) -> config.Config:
    """The native library with One.flac staged, answering its config."""
    _stage(native_library[0], silence, "One.flac")
    return native_library[0]


@pytest.fixture
def silence(tmp_path: Path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    if not _SILENCE:
        _SILENCE.append(synth_container(scratch, ".flac").read_bytes())
    path = scratch / "probe.flac"
    path.write_bytes(_SILENCE[0])
    return path


def _staging(cfg: config.Config) -> Path:
    return Path(cfg.paths.download_staging)


def _stage(cfg: config.Config, silence: Path, name: str, *, head: str = "01A - 124") -> Path:
    path = _staging(cfg) / name
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path, {"title": f"{head} - {Path(name).stem}", "artist": "Probe", "genre": "Deep House"})
    return path


def _music(cfg: config.Config, batch: str = BATCH) -> Path:
    """Where a native landing files ``batch`` (U164): its year folder under the processed tree."""
    from cratekit.intake import batch_name, shelve
    when, said = shelve.filed_parts(batch, on=batch_name.today())
    return shelve.processed_root(cfg) / f"{when.year}" / shelve.filed_name(when, said)


def _staged_names(cfg: config.Config) -> list[str]:
    return sorted(p.name for p in _staging(cfg).glob("*.flac"))


def _staged_names_all(cfg: config.Config) -> list[str]:
    return sorted(p.name for p in _staging(cfg).iterdir() if p.is_file())


def _land(*extra: str) -> list[str]:
    return ["intake", "land", "--name", BATCH, *extra]


def _query(cfg: config.Config, sql: str, *params) -> list[tuple]:
    with closing(sqlite3.connect(cfg.library.db_path)) as conn:
        return conn.execute(sql, params).fetchall()


def _execute(cfg: config.Config, sql: str, *params) -> None:
    with closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute(sql, params)


def _landed_rows(cfg: config.Config) -> list[tuple]:
    """(ID, Title, FolderPath) of every row under the batch's filed folder, by name."""
    return _query(
        cfg, "SELECT ID, Title, FolderPath FROM djmdContent WHERE FolderPath LIKE ? "
        "ORDER BY FileNameL", f"%/{FILED_AS}/%",
    )


def _batch_playlist(cfg: config.Config) -> list[tuple]:
    return _query(cfg, "SELECT ID, ParentID, Attribute FROM djmdPlaylist WHERE Name = ?", BATCH)


def _members(cfg: config.Config, playlist_id: str) -> list[str]:
    rows = _query(
        cfg, "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY TrackNo",
        playlist_id)
    return [str(row[0]) for row in rows]


def _advance_usn(conn: sqlite3.Connection) -> None:
    """Advance the library's local update count by one, as rekordbox does when it adds a row."""
    conn.execute(
        "UPDATE agentRegistry SET int_1 = int_1 + 1 WHERE registry_id = 'localUpdateCount'")


def _hold(cfg: config.Config, content_id: str, path: str, link: int | None = None) -> None:
    """A row rekordbox holds for ``path``, the update count advanced, or it reads as another db."""
    with closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute(
            "INSERT INTO djmdContent (ID, Title, FolderPath, ContentLink, rb_local_deleted, "
            "created_at, updated_at) VALUES (?, 'held', ?, ?, 0, '2026-01-01', '2026-01-01')",
            (content_id, path, link),
        )
        _advance_usn(conn)


def _asked(verb: list[str]) -> dict:
    """The first act alone: the gate's screen, nothing answered."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused


def _shown(verb: list[str]) -> dict:
    """What the gate's screen shows for ``verb``, nothing answered."""
    return _asked(verb)["cause"]["detail"]["shown"]


def _answered(verb: list[str], gate: str = GATE) -> tuple[dict, str]:
    """The first act and an answer of apply recorded on its run, the continuation left to the test."""
    refused = _asked(verb)
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    return refused, run_id


def _land_first(cfg: config.Config, silence: Path, name: str = "Zero.flac") -> None:
    """Land one file under BATCH, so its filed folder exists and is recorded (U164)."""
    _stage(cfg, silence, name)
    _landed_ok()


def _two_acts(verb: list[str], gate: str = GATE) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    refused, run_id = _answered(verb, gate)
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate and detail["explicit"] is True
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _landed_ok(verb: list[str] | None = None) -> dict:
    """Both acts of ``verb`` (the batch's landing by default), which must succeed."""
    return _lands(verb=verb)[0]


def _lands(*extra: str, verb: list[str] | None = None) -> tuple[dict, dict]:
    """Both acts of the batch's landing with ``extra``, or of ``verb``, which must succeed:
    (acted, refused)."""
    code, acted, refused = _two_acts(_land(*extra) if verb is None else verb)
    assert code == int(ExitCode.OK), acted
    return acted, refused


def _land_fails() -> dict:
    """Both acts of the batch's landing, which must not succeed."""
    code, acted, _ = _two_acts(_land())
    assert code != int(ExitCode.OK), acted
    return acted


def test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root(
        native_library, silence):
    cfg, root_id = native_library
    staged = [_stage(cfg, silence, name) for name in ("One.flac", "Three.flac", "Two.flac")]
    code, acted, refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "ok"
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
    assert acted["data"]["totals"] == {
        "count": 3, "landed": 3, "refused": 0, "added": 3, "already present": 0, "memberships": 3,
    }
    # U127: no vocal calibration here, so no row is tagged vox and the landing says why.
    assert [w["code"] for w in acted["warnings"]] == [
        land_cli.AWAITING_ANALYSIS, land_cli.VOX_NOT_WRITTEN,
    ]
    assert "Analyze" in acted["warnings"][0]["message"]
    assert "pending_human_action" not in acted or acted["pending_human_action"] is None
    # What a restore reads and a revert of the intake cutover refuses over.
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.CLOSED
    assert record.sources == {INTAKE: "committed"}
    # U166: the batch's three memberships and INBOX / Analyze's three.
    assert {change.tree: change.created for change in record.change.trees} == {
        INTAKE: 6, rb_writer.CONTENT_TABLE: 3,
    }
    assert record.snapshot_path, "the capture the commit happened behind is not attached"
    # U111: the rotation reads a batch's landing date from its playlist.
    assert record.detail[native.BATCH_PLAYLIST_KEY] == {"id": str(playlist_id), "name": BATCH}


@pytest.mark.parametrize("passed", ["RUN_synced", None])
def test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads(one_staged, passed):
    """R-777: ``sync mark --pass`` reads ``landings_of_pass`` as its proof the pass landed.
    And an answer continued over its database lands (U161)."""
    cfg = one_staged
    _landed_ok(_land(*(("--pass", passed) if passed else ())))
    assert len(_landed_rows(cfg)) == 1
    (record,) = session.records(cfg)
    if passed is None:
        assert native.PASS_KEY not in record.detail
        return
    assert record.detail[native.PASS_KEY] == "RUN_synced"
    assert native.landings_of_pass(cfg, "RUN_synced") == (record.session_id,)
    assert native.landings_of_pass(cfg, "ANOTHER_synced") == ()


def test_two_unnamed_landings_on_one_day_are_two_playlists_and_never_one(
        native_library, silence, monkeypatch):
    """U110: the writer adds to a playlist found by name, or two batches merge silently."""
    from cratekit.intake import batch_name
    cfg, root_id = native_library
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 3))
    _stage(cfg, silence, "One.flac")
    first = _landed_ok(["intake", "land"])
    _stage(cfg, silence, "Two.flac")
    second = _landed_ok(["intake", "land"])
    named = _query(
        cfg, "SELECT Name, ParentID FROM djmdPlaylist WHERE Name LIKE ? ORDER BY Name",
        "2026-10-03 Downloads%")
    assert named == [("2026-10-03 Downloads", root_id), ("2026-10-03 Downloads 2", root_id)]
    assert [first["data"]["items"][-1]["playlist"], second["data"]["items"][-1]["playlist"]] == [
        "2026-10-03 Downloads", "2026-10-03 Downloads 2",
    ]


def test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing(
        one_staged, monkeypatch):
    """U110: a name taken between the gate and the write is asked again under the lock."""
    from cratekit.intake import batch_name
    cfg = one_staged
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 3))
    real_lock = landing.batch_lock

    def take_then_lock(batch):
        (Path(cfg.library.root) / cfg.library.music_dir / batch).mkdir(parents=True)
        return real_lock(batch)
    monkeypatch.setattr(landing, "batch_lock", take_then_lock)
    code, acted, _ = _two_acts(["intake", "land"])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _staged_names(cfg) == ["One.flac"]
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name LIKE ?", "2026-10-03%") == []


def test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value(native_library, silence):
    """The library's device (A8), defaults (R-923), inode (U115) and ContentLink (U126), read
    from SQL; no analysis column holds a value, and no cue, mixer or file row names a new row."""
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    acted = _landed_ok()
    defaults = list(rb_writer.CONTENT_ROW_DEFAULTS)
    rows = _query(
        cfg,
        f"SELECT ID, FolderPath, DeviceID, MasterDBID, {rb_writer.FILE_ID_COLUMN}, "
        f"{rb_writer.CONTENT_LINK_COLUMN}, {', '.join(defaults)}, {', '.join(native.LEFT_EMPTY)} "
        "FROM djmdContent WHERE FolderPath LIKE ?", f"%/{FILED_AS}/%")
    assert len(rows) == 2
    # Defaults COMPARED AS TEXT: the binding declares ``DJPlayCount`` a string.
    wanted = {column: str(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()}
    by_id: dict[str, str] = {}
    for content_id, folder_path, device_id, master, file_id, link, *values in rows:
        assert (str(device_id), str(master)) == MY_DEVICE
        landed = Path(folder_path)
        assert landed.is_file(), folder_path
        assert file_id is not None and str(file_id) == str(landed.stat().st_ino), content_id
        assert int(file_id) == landed.stat().st_ino
        by_id[str(content_id)] = str(file_id)
        assert link == LIBRARY_LINK
        found = values[: len(defaults)]
        assert {c: str(v) for c, v in zip(defaults, found)} == wanted, content_id
        assert None not in found, content_id
        for name, value in zip(native.LEFT_EMPTY, values[len(defaults) :]):
            assert value in (None, 0, 0.0, "", "0"), f"row {content_id} carries {name}={value!r}"
        for table in rb_writer.CONTENT_ANALYSIS_TABLES:
            (count,) = _query(cfg, f"SELECT COUNT(*) FROM {table} WHERE ContentID = ?", content_id)[0]
            assert count == 0, f"{table} holds a row for the new content row {content_id}"
    assert not set(rb_writer.CONTENT_ROW_DEFAULTS) & rb_writer.CONTENT_ROW_EMPTY_COLUMNS
    assert BINDING_LINK != LIBRARY_LINK
    # The envelope names each value as written, a number, and the columns left.
    landed_items = [item for item in acted["data"]["items"] if item["action"] == "landed"]
    assert len(landed_items) == 2
    for item in landed_items:
        assert item["row"][rb_writer.FILE_ID_COLUMN] == by_id[item["content_id"]]
        assert item["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
        assert item["left_empty"] == sorted(native.LEFT_EMPTY)


def _file_id_lies_once(monkeypatch):
    """The restamp's one inode read lies, so the read back after the commit differs."""
    real = native.file_id_of
    calls: list[Path] = []

    def lying_once(path: Path) -> int:
        calls.append(path)
        return real(path) + (1 if len(calls) == 1 else 0)
    monkeypatch.setattr(native, "file_id_of", lying_once)
    return rb_writer.FILE_ID_COLUMN, lambda value, path: int(value) == Path(path).stat().st_ino + 1


def _link_keeps_the_bindings(monkeypatch):
    """The restamp leaves the binding's ContentLink on the row."""
    real = native._restamp

    def keeping_the_bindings(content, row, plan):
        real(content, row, plan)
        setattr(content, rb_writer.CONTENT_LINK_COLUMN, BINDING_LINK)
    monkeypatch.setattr(native, "_restamp", keeping_the_bindings)
    return rb_writer.CONTENT_LINK_COLUMN, lambda value, _path: value == BINDING_LINK


@pytest.mark.parametrize("dropped", [_file_id_lies_once, _link_keeps_the_bindings])
def test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit(
        one_staged, monkeypatch, dropped):
    """A dropped column makes a row rekordbox will not load; the read back names the restore."""
    cfg = one_staged
    column, durable = dropped(monkeypatch)
    acted = _land_fails()
    assert acted["cause"]["reason"] == "internal-error"
    assert column in acted["cause"]["message"]
    (record,) = session.records(cfg)
    assert record.session_id in " ".join(acted["cause"]["remediation"]["steps"])
    ((value, folder_path),) = _query(
        cfg, f"SELECT {column}, FolderPath FROM djmdContent WHERE FolderPath LIKE ?", f"%/{FILED_AS}/%"
    )
    assert durable(value, folder_path), "the write is durable"


def test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses(one_staged, monkeypatch):
    """A step failing after the commit: the record names its rows and the verb refuses."""
    cfg = one_staged
    real = rb_writer.commit_guarded

    def committed_then_failed(*args, **kwargs):
        real(*args, **kwargs)
        raise RuntimeError("a step after the commit failed")
    monkeypatch.setattr(rb_writer, "commit_guarded", committed_then_failed)
    _land_fails()
    (record,) = session.records(cfg)
    assert record.detail["collection_landed"], record.detail


def _landed(*rows: native.AddedRow, content_link: int | None = None) -> native.NativeLanded:
    return native.NativeLanded(
        tree_id=INTAKE, playlist="p", playlist_id="9", added=tuple(rows), present=(),
        memberships_added=len(rows), session_id="s-1", content_link=content_link)


def _added_row(path: Path, content_id: str, file_id: str, link: int) -> native.AddedRow:
    return native.AddedRow(
        target=path, content_id=content_id, title="t", folder_path=str(path), empty={},
        file_id=file_id, content_link=link)


def test_assert_rows_identified_holds_the_file_id_and_the_link_to_the_ones_planned(tmp_path):
    path = tmp_path / "a.flac"
    path.write_bytes(b"fLaC")
    inode = str(path.stat().st_ino)
    right = _added_row(path, "1", inode, LIBRARY_LINK)
    native.assert_rows_identified(_landed(right, content_link=LIBRARY_LINK))
    for wrong, said in (
        (_added_row(path, "2", "73894078", LIBRARY_LINK), "73894078"),
        (_added_row(path, "2", inode, BINDING_LINK), f"{rb_writer.CONTENT_LINK_COLUMN} = {BINDING_LINK}"),
    ):
        with pytest.raises(CratekitError) as caught:
            native.assert_rows_identified(_landed(right, wrong, content_link=LIBRARY_LINK))
        cause = caught.value.cause
        assert cause.reason == "internal-error"
        assert "2: " in cause.message and said in cause.message and "1: " not in cause.message
        assert "restore session s-1" in " ".join(cause.remediation.steps)
    # NO PLANNED VALUE IS NO PASS: a row with nothing to hold it to is refused.
    with pytest.raises(CratekitError) as caught:
        native.assert_rows_identified(_landed(right))
    assert f"1: {rb_writer.CONTENT_LINK_COLUMN}" in caught.value.cause.message


# U126: the row is given the library's ContentLink, never the binding's
def _set_links(cfg: config.Config, links: dict[str, int | str | None]) -> None:
    """Put the named ContentLink on each named row of the disposable library."""
    for content_id, link in links.items():
        _execute(cfg, "UPDATE djmdContent SET ContentLink = ? WHERE ID = ?", link, content_id)


def test_an_approval_at_one_link_is_not_applied_at_another_and_no_majority_refuses(one_staged):
    """Rows moved after the approval change the digest; then with no value on more than half
    the live rows there is none of rekordbox's to give, so it refuses before the gate."""
    cfg = one_staged
    _refused, run_id = _answered(_land())
    _set_links(cfg, {"1": LIBRARY_LINK + 1, "2": LIBRARY_LINK + 1})
    code, acted = drive(["--run", run_id, *_land()])
    assert code != int(ExitCode.OK), acted
    assert _landed_rows(cfg) == []
    assert _staged_names(cfg) == ["One.flac"]
    _set_links(cfg, {"2": 30})
    rows_before = _query(cfg, "SELECT COUNT(*) FROM djmdContent")
    code, refused = drive(_land())
    assert code == int(ExitCode.LIBRARY_PREREQUISITE), refused
    assert refused["cause"]["reason"] == row_link.MAJORITY_UNCLEAR
    assert refused["cause"]["detail"]["rows"] == 2
    assert refused["cause"]["detail"]["carriers"] == 1
    assert _staged_names(cfg) == ["One.flac"]
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent") == rows_before
    assert session.records(cfg) == ()


def test_the_link_its_count_the_playlist_and_each_file_move_the_digest(one_staged, silence):
    """What the screen shows is what is approved, so the count, the value, the playlist name
    and one more file each move the digest, the path taken out of it taking nothing else."""
    cfg = one_staged
    first = _asked(_land())
    renamed = _asked(["intake", "land", "--name", f"{BATCH}_other"])
    _execute(
        cfg,
        "INSERT INTO djmdContent (ID, ContentLink, rb_local_deleted, created_at, updated_at) "
        "VALUES ('rb-made', ?, 0, '2026-01-01', '2026-01-01')",
        LIBRARY_LINK,
    )
    counted = _asked(_land())
    assert counted["cause"]["detail"]["shown"]["content link"].endswith("3 of the library's 3 live rows")
    _set_links(cfg, {"1": LIBRARY_LINK + 1, "2": LIBRARY_LINK + 1})
    second = _asked(_land())
    _stage(cfg, silence, "Two.flac")
    grown = _asked(_land())
    (one,) = first["cause"]["detail"]["shown"]["items"]
    (two,) = second["cause"]["detail"]["shown"]["items"]
    assert one["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
    assert two["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK + 1
    every = (first, renamed, counted, second, grown)
    assert len({each["cause"]["detail"]["shown"]["digest"] for each in every}) == 5


def test_a_landing_that_adds_no_row_needs_no_majority(native_library, silence):
    """Every file already held: memberships alone, so no majority is asked and no link shown."""
    cfg, _root = native_library
    _land_first(cfg, silence)
    _stage(cfg, silence, "One.flac")
    _hold(cfg, "held-1", str(_music(cfg) / "One.flac"), 30)
    _set_links(cfg, {"2": 31})
    shown = _shown(_land())
    assert shown["adds"] == 0 and shown["already present"] == 1
    assert shown["content link"] == "none, since no row is added"
    (item,) = shown["items"]
    assert rb_writer.CONTENT_LINK_COLUMN not in item["row"]


def _majority(cfg: config.Config, rows: dict[str, tuple[int | str | None, int]]):
    """Replace the library's content rows with ``rows`` (link, deleted) and read the majority."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    _execute(cfg, "DELETE FROM djmdContent")
    for content_id, (link, deleted) in rows.items():
        _execute(
            cfg, "INSERT INTO djmdContent (ID, ContentLink, rb_local_deleted, created_at, "
            "updated_at) VALUES (?, ?, ?, '2026-01-01', '2026-01-01')", content_id, link, deleted,
        )
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    try:
        with Session(engine) as db_session:
            return row_link.library_link(SimpleNamespace(session=db_session))
    finally:
        engine.dispose()


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
        {"a": ("²", 0), "b": ("²", 0), "c": (9, 0)},
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
    """Given on a created row, so the creation policy must admit it, asked of it by landing."""
    assert rb_writer.CONTENT_LINK_COLUMN not in rb_writer.CONTENT_ROW_EMPTY_COLUMNS
    assert rb_writer.CONTENT_LINK_COLUMN not in rb_writer.BOOKKEEPING_COLUMNS
    assert rb_writer.CONTENT_LINK_COLUMN not in native.LEFT_EMPTY
    assert "creations=" not in Path(landing.__file__).read_text(encoding="utf-8")


def test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database(
        native_library, one_staged):
    """And the gate takes no inline answer, and an abort moves and writes nothing."""
    cfg, root_id = native_library
    inline = _asked(["-d", f"{GATE}=apply", *_land()])
    assert inline["cause"]["detail"]["gate"] == GATE
    refused = _asked(_land())
    shown = refused["cause"]["detail"]["shown"]
    assert shown["reads and writes"] == str(cfg.library.db_path)
    assert shown["playlist"] == f"{BATCH} under {DECLARED.intake.display} (row {root_id})"
    assert shown["left empty for rekordbox"] == list(native.LEFT_EMPTY)
    assert shown["adds"] == 1 and shown["already present"] == 0
    (item,) = shown["items"]
    assert item["action"] == native.ADD
    assert item["to"] == str(_music(cfg) / "One.flac")
    # U163: the artist and genre each with its row; the fixture writes no album and no date.
    assert set(item["row"]) == {
        "Title", "FolderPath", "FileNameL", "FileSize", "FileType", rb_writer.FILE_ID_COLUMN,
        rb_writer.CONTENT_LINK_COLUMN, native.ARTIST_COLUMN, native.GENRE_COLUMN,
    }
    assert item["row"][native.ARTIST_COLUMN]["name"] == "Probe"
    assert item["row"][native.GENRE_COLUMN]["name"] == "Deep House"
    # THE LIBRARY'S VALUE, shown with its count, never the binding's (U126).
    assert item["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
    assert shown["content link"] == (f"{LIBRARY_LINK}, carried by 2 of the library's 2 live rows")
    # U115: the file id is named as a sentence, since no plan can know the number.
    assert item["row"][rb_writer.FILE_ID_COLUMN] == native.FILE_ID_AT_LANDING
    assert item["row"]["FileType"] == 5, "FLAC is file type 5 in the binding"
    _nothing_landed(cfg)
    assert not _music(cfg).exists()
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *_land()])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    _nothing_landed(cfg)


# A file already in the collection, and a second run
def test_a_file_already_in_the_collection_is_present_and_not_added_twice(native_library, silence):
    """Landed into again by its name (U164), where the collection holds a row for one file."""
    cfg, root_id = native_library
    _land_first(cfg, silence)
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    held = str(_music(cfg) / "Two.flac")
    _hold(cfg, "held-2", held)
    shown = _shown(_land())
    assert shown["adds"] == 1 and shown["already present"] == 1
    present = [item for item in shown["items"] if item["action"] == native.PRESENT]
    assert [item["content_id"] for item in present] == ["held-2"]
    # THE LINK ONLY WHERE A ROW IS ADDED (U126): the held row is not written.
    assert rb_writer.CONTENT_LINK_COLUMN not in present[0]["row"]
    (added,) = [item for item in shown["items"] if item["action"] == native.ADD]
    assert added["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
    acted = _landed_ok()
    assert acted["data"]["totals"]["added"] == 1
    assert acted["data"]["totals"]["already present"] == 1
    rows = _query(cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", held)
    assert rows == [("held-2",)], "the held file gained a second row"
    (playlist,) = _batch_playlist(cfg)
    members = _members(cfg, str(playlist[0]))
    # The first landing's file, then this one's two, in order.
    assert len(members) == 3 and members[2] == "held-2", "the batch playlist is the batch, in order"


def test_a_second_approved_run_over_the_landed_files_adds_nothing(native_library, silence):
    """At the engine, where files can be planned twice, the second plan reads every row present."""
    cfg, _root = native_library
    folder = _music(cfg)
    folder.mkdir(parents=True)
    files = []
    for name in ("One.flac", "Two.flac", "Three.flac"):
        landed = folder / name
        shutil.move(_stage(cfg, silence, name), landed)
        files.append((landed, landed))
    registry = tree_registry.read(cfg)

    def run() -> native.NativeLanded:
        with _opened(cfg) as db:
            plan = native.plan_rows(cfg, db, tree_id=INTAKE, registry=registry, batch=BATCH, files=files)
            return native.apply_rows(cfg, db, plan, analysis_roots=[Path(cfg.library.root)])
    first = run()
    assert len(first.added) == 3 and first.memberships_added == 3
    second = run()
    assert second.added == () and second.memberships_added == 0
    assert len(second.present) == 3
    assert len(_landed_rows(cfg)) == 3
    (playlist,) = _batch_playlist(cfg)
    assert len(_members(cfg, str(playlist[0]))) == 3


def test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged(
        one_staged, silence):
    cfg = one_staged
    _landed_ok()
    before = _landed_rows(cfg)
    _stage(cfg, silence, "One.flac")
    # The plan reads the file as present, because the row holds its target.
    assert _shown(_land())["already present"] == 1
    acted = _land_fails()
    assert acted["cause"]["reason"] == "intake-list-unusable"
    assert "One.flac" in acted["cause"]["message"]
    assert _landed_rows(cfg) == before
    assert _staged_names(cfg) == ["One.flac"]


@contextmanager
def _opened(cfg: config.Config):
    """The disposable library opened as the engine opens it, closed after."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        yield db
    finally:
        rb_writer.close_db(db)


def _nothing_landed(cfg: config.Config, staged: tuple[str, ...] = ("One.flac",)) -> None:
    """Every staged file still staged, and no row and no batch playlist written."""
    assert _staged_names(cfg) == list(staged)
    assert _landed_rows(cfg) == [] and _batch_playlist(cfg) == []


# Refused before the gate
def _assert_refused_before_the_gate(cfg: config.Config, code: int, envelope: dict, reason: str):
    assert envelope["cause"]["reason"] == reason, envelope
    assert code != int(ExitCode.OK)
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert not gates.run_path(envelope["run_id"]).exists()
    _nothing_landed(cfg)
    assert not _music(cfg).exists()


def test_an_intake_tree_on_the_bridge_is_refused_before_the_gate_naming_the_cutover(
        acknowledged, silence):
    """No --export and no cutover: the refusal names the cutover, and the engine's does too."""
    cfg = acknowledged
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land())
    _assert_refused_before_the_gate(cfg, code, envelope, "library-export-unusable")
    steps = " ".join(envelope["cause"]["remediation"]["steps"])
    assert f"crate tree cutover {INTAKE}" in steps and "--export" in steps
    with _opened(cfg) as db, pytest.raises(CratekitError) as raised:
        native.anchored_intake_root(db, INTAKE, tree_registry.read(cfg))
    cause = raised.value.cause
    assert cause.reason == "tree-unconverged"
    assert any(f"crate tree cutover {INTAKE}" in step for step in cause.remediation.steps)


def test_no_acknowledgment_refuses_before_the_gate(machine, silence):
    """R-733's lesson: the acknowledgment is read before the gate, its mint the remedy."""
    cfg = machine
    _cut_over_intake(cfg)
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land())
    _assert_refused_before_the_gate(cfg, code, envelope, "backup-acknowledgment-missing")
    assert envelope["cause"]["remediation"]["remedy"] == "acknowledge-backup"


def test_rekordbox_running_or_an_export_on_a_native_tree_is_refused_before_the_gate(
        one_staged, tmp_path, monkeypatch):
    cfg = one_staged
    export = tmp_path / "fresh.xml"
    export.write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")
    code, envelope = drive(_land("--export", str(export)))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "--export" in envelope["cause"]["message"]
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    code, envelope = drive(_land())
    _assert_refused_before_the_gate(cfg, code, envelope, "rekordbox-running")


def test_an_empty_staging_folder_is_a_plan_of_nothing_and_asks_no_explicit_gate(native_library):
    """An explicit gate is the price of a new write, not of learning there is nothing to move."""
    cfg, _root = native_library
    code, envelope = drive(_land())
    assert code == int(ExitCode.OK) and envelope["outcome"] == "no_op", envelope
    assert envelope["data"]["items"] == [] and envelope["data"]["totals"] == {"count": 0}
    assert "gate" not in (envelope.get("cause") or {})
    assert _landed_rows(cfg) == [] and _batch_playlist(cfg) == []


def test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves(
        native_library, silence, monkeypatch):
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
    acted = _land_fails()
    assert len(calls) == 2
    message = acted["cause"]["message"]
    assert "no row was added" in message
    assert "3 file(s) were already moved into the library and stay there" in message
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["One.flac", "Three.flac", "Two.flac"]
    assert _staged_names(cfg) == []
    assert _landed_rows(cfg) == [], "a row landed although the commit never happened"
    assert _batch_playlist(cfg) == []
    assert [record.state for record in session.records(cfg)] == [session.SessionState.ABANDONED]


@pytest.mark.parametrize(
    ("sql", "named"),
    [
        # A tempo: the guard's read back sees a flushed creation (R-760).
        ("UPDATE djmdContent SET BPM = 12400 WHERE ID = :id", "BPM"),
        # The key, held on a content row beyond the playlist tables' columns (R-746).
        ("UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id", "KeyID"),
        # An analysis product row naming the new row, as an analysis pass would write.
        (
            "INSERT INTO djmdMixerParam (ID, ContentID, rb_local_deleted, created_at, "
            "updated_at) VALUES ('mp-1', :id, 0, '2026-01-01', '2026-01-01')",
            "djmdMixerParam",
        ),
    ],
)
def test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit(
        one_staged, monkeypatch, sql, named):
    """Written by SQL after the flush, past the in memory judge, so refused on the row stored."""
    from sqlalchemy import text
    cfg = one_staged
    real = native._restamp

    def restamp_and_taint(content, row, plan):
        real(content, row, plan)
        content._sa_instance_state.session.execute(text(sql), {"id": str(content.ID)})
    monkeypatch.setattr(native, "_restamp", restamp_and_taint)
    acted = _land_fails()
    assert acted["cause"]["reason"] == "whitelist-violation"
    assert named in acted["cause"]["message"]
    assert _landed_rows(cfg) == [], "a row carrying an analysis value was committed"
    assert _batch_playlist(cfg) == []
    assert _query(cfg, "SELECT COUNT(*) FROM djmdMixerParam")[0] == (0,)


# What is stored: the base drive form
def test_folder_path_is_stored_under_the_base_drive_rekordbox_records(one_staged, tmp_path):
    """Sitting 17: rows store the base drive, on a renamed volume not the mounted path."""
    cfg = one_staged
    # The drive the database was made on is one this machine no longer mounts.
    base = str(tmp_path.parent / "old-drive")
    _execute(
        cfg, "UPDATE djmdProperty SET BaseDBDrive = ?, CurrentDBDrive = ?", base + "/", str(tmp_path) + "/"
    )
    shown = _shown(_land())
    expected = base + "/library/Music/Processed_Tracks/2026/" + FILED_AS + "/One.flac"
    assert shown["items"][0]["row"]["FolderPath"] == expected
    assert shown["paths stored"].startswith(f"under the base drive {base}")
    _landed_ok()
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
    decomposed = tmp_path / "Nöpi.flac"
    assert native.stored_folder_path(decomposed, base_drive=None, current_drive=None) == str(
        tmp_path / "Nöpi.flac")


def test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands(
        one_staged, silence):
    """One file's problem is one file's refusal: the binding's file type is an enum of five."""
    cfg = one_staged
    odd = _stage(cfg, silence, "Two.flac")
    odd.rename(odd.with_suffix(".opus"))
    shown = _shown(_land())
    assert shown["adds"] == 1 and shown["left in staging"] == 1
    (planned_odd,) = [item for item in shown["items"] if item["action"] == native.UNSUPPORTED]
    assert "Two.opus" in planned_odd["why"] and "left in staging" in planned_odd["why"]
    acted = _landed_ok()
    assert _staged_names_all(cfg) == ["Two.opus"]
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["One.flac"]
    assert [Path(row[2]).name for row in _landed_rows(cfg)] == ["One.flac"]
    assert acted["data"]["totals"]["refused"] == 1 and acted["data"]["totals"]["added"] == 1
    assert any("Two.opus" in w["message"] for w in acted["warnings"])


def test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too(
        one_staged, silence, monkeypatch):
    """A row with no route is refused, driven at the check's seam."""
    cfg = one_staged
    _stage(cfg, silence, "Two.flac")
    real = landing._unplaceable

    def unplaceable(path, declared):
        if path.name == "Two.flac":
            return landing.Refused(
                path=path, reason="intake-list-unusable",
                sentence=f"{path.name} resolves to a bucket with no declared sub, so it "
                f"was left in staging; run crate tag folder over it and land it again")
        return real(path, declared)
    monkeypatch.setattr(landing, "_unplaceable", unplaceable)
    acted = _landed_ok()
    assert _staged_names(cfg) == ["Two.flac"]
    assert [Path(row[2]).name for row in _landed_rows(cfg)] == ["One.flac"]
    (warning,) = [w for w in acted["warnings"] if w["code"] == "intake-list-unusable"]
    assert "Two.flac" in warning["message"] and "tag folder" in warning["message"]


# The digest names the library, not the database file (U161, R-922)
def _point_at_a_copy(cfg: config.Config) -> Path:
    """Point the config at a copy of the database elsewhere, as a rehearsal does."""
    copy = Path(cfg.library.root) / "rehearsal" / "master-copy.db"
    copy.parent.mkdir(parents=True)
    shutil.copyfile(cfg.library.db_path, copy)
    data = _config_data(Path(cfg.library.root))
    data["library"]["db_path"] = str(copy)
    config.save(config.from_dict(data))
    config.reset_cache()
    return copy


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
        one_staged, silence):
    """R-922: a copy at another path digests equal, each screen naming its file; an answer
    over the live file is pinned to it, so the copy's continuation is stale (U161)."""
    cfg = one_staged
    _stage(cfg, silence, "Two.flac")
    live_path = str(cfg.library.db_path)
    live, run_id = _answered(_land())
    copy = _point_at_a_copy(cfg)
    shown_live = live["cause"]["detail"]["shown"]
    shown_copy = _shown(_land())
    assert shown_live["reads and writes"] == live_path
    assert shown_copy["reads and writes"] == str(copy)
    assert shown_live["items"] == shown_copy["items"]
    assert shown_live["digest"] == shown_copy["digest"]
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    assert _landed_rows(cfg) == []
    code, acted = drive(["--run", run_id, *_land()])
    assert code == int(ExitCode.DECISION_STALE), acted
    detail = acted["cause"]["detail"]
    assert detail["pinned"] == land_cli.DATABASE_PIN
    assert detail["expected"] == live_path and detail["actual"] == str(copy)
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    for database in (live_path, str(copy)):
        with closing(sqlite3.connect(database)) as conn:
            landed = conn.execute(
                "SELECT ID FROM djmdContent WHERE FolderPath LIKE ?", (f"%/{FILED_AS}/%",)
            ).fetchall()
        assert landed == [], database


def test_the_engine_identity_names_the_device_and_master_id_and_no_database_path(
        one_staged, monkeypatch):
    """The device and master id identify the library and are digested; the path is not."""
    cfg = one_staged
    real = native.identity
    plans: list[native.NativePlan] = []
    taken: list[dict] = []
    monkeypatch.setattr(
        native, "identity", lambda plan: plans.append(plan) or taken.append(real(plan)) or taken[-1]
    )
    _asked(_land())
    assert taken, "the engine took no identity"
    database = Path(cfg.library.db_path)
    for one in taken:
        assert one["device"] == MY_DEVICE[0]
        assert one["master_db_id"] == MY_DEVICE[1]
        assert "database" not in one
        named = _strings(one)
        assert not [s for s in named if str(database) in s or str(database.parent) == s], named
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
        one_staged, monkeypatch):
    """An answer recorded against a digest that named the file is stale, and writes nothing."""
    real = native.identity
    monkeypatch.setattr(
        native, "identity", lambda plan: {**real(plan), "database": str(plan.database)})
    refused, run_id = _answered(_land())
    monkeypatch.setattr(native, "identity", real)
    code, acted = drive(["--run", run_id, *_land()])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert acted["cause"]["detail"]["expected"] == refused["cause"]["detail"]["shown"]["digest"]
    _nothing_landed(one_staged)
