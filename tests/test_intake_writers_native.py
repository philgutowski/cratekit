"""R-770: every intake writer chooses its medium by the intake tree's mode.

``intake land`` has chosen that way since R-746. The ledger said every other
writer still spliced, and named five. Driven, the list is shorter than it was
read to be: two callers reach the intake emitter in ``src``, both through
``place_files``, and one verb besides the landing drives them, ``intake file``.
The favourites sweep, the composed pass and the label batch write nothing to
the intake tree on either medium, and section 4 holds them to that on both.

What this file pins, each against a native fixture and a bridge fixture:

1. ``intake file`` on a native intake tree adds one content row and one batch
   playlist under the adopted root, and writes nothing to an export.
2. ``intake file`` on the bridge is unchanged.
3. The splice itself refuses a native tree in its own words, naming the
   landing, and never as a defect. That is the checking path, and it holds for
   a caller that did not read the switch.
4. The verbs the ledger named and that never splice run the same on both.
5. One switch. Nothing beside it reads the intake tree's mode.

The fixtures are the native landing's own, so the two suites cannot come to
mean two libraries by "a native intake tree". D1 applies: nothing here names a
real volume, a real person or a real track.
"""

from __future__ import annotations

import ast
import shutil
import sqlite3
from pathlib import Path

import pytest

from cratekit.cli import gates
from cratekit.core import config, jobs, preflight, rb_writer, session, tags, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import file_cli, ingest, land_cli, landing, native
from cratekit.modules.outbound import source as outbound_source
from tests import adopt_fixtures, outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data
from tests.test_intake_land_native import (
    DECLARED,
    INTAKE,
    MY_DEVICE,
    TODAY,
    _cut_over_intake,
    _query,
    _seed_binding_rows,
)
from tests.test_label_workers import LABELS, SLUGS, readable, register
from tests.test_label_workers import bind as bind_catalogue
from tests.test_outbound_workers import _resume as resume_outbound
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import catalog
from tests.test_rb_writer_db import RECORDED_APP_VERSION
from tests.xml_fixtures import _fresh_xml

GATE = file_cli.NATIVE_GATE
SRC = Path(ingest.__file__).resolve().parents[1]

BRIDGE = "bridge"
NATIVE = "native"

#: The two rows ``_build_disposable_database`` seeds, which name no file.
BASELINE = ("1", "2")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _forget_libraries():
    outbound_source.forget_libraries()
    yield
    outbound_source.forget_libraries()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the native landing patches it."""
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


def _machine(tmp_path, monkeypatch, *, profile: str | None = None) -> config.Config:
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    (tmp_path / "staging").mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(
        root,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    if profile is not None:
        data["profile"] = {"name": profile}
    resolved = config.from_dict(data)
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
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set-up machine with a disposable database and no acknowledgment yet."""
    return _machine(tmp_path, monkeypatch)


@pytest.fixture
def bridge_library(machine) -> config.Config:
    """The acknowledged machine, its intake tree where every library's is today."""
    session.record_acknowledgment(machine, terminal=lambda: True)
    return machine


@pytest.fixture
def native_library(bridge_library):
    """The same machine with its intake tree cut over. Answers (cfg, root id)."""
    return bridge_library, _cut_over_intake(bridge_library)


@pytest.fixture(params=(BRIDGE, NATIVE))
def either(request, tmp_path, monkeypatch) -> config.Config:
    """Every module switched on, on each medium in turn, for the verbs of section 4."""
    resolved = _machine(tmp_path, monkeypatch, profile="full")
    if request.param == NATIVE:
        _cut_over_intake(resolved)
    assert ingest.intake_medium(resolved).native is (request.param == NATIVE)
    return resolved


@pytest.fixture
def silence(tmp_path: Path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return synth_container(scratch, ".flac")


@pytest.fixture
def export(tmp_path: Path) -> Path:
    path = tmp_path / "fresh.xml"
    path.write_bytes(_fresh_xml())
    return path


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir


def _single(cfg: config.Config, silence: Path, name: str = "Single.flac") -> Path:
    """One tagged file already in the library, where this verb finds its files."""
    path = _music(cfg) / name
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path,
        {"title": f"01A - 124 - {Path(name).stem}", "artist": "Probe", "genre": "Deep House"},
    )
    return path


def _file(path: Path, *extra: str) -> list[str]:
    return ["intake", "file", str(path), *extra]


def _rows(cfg: config.Config) -> list[tuple]:
    """Every content row beyond the two the disposable database is built with."""
    return _query(
        cfg,
        "SELECT ID, Title, FolderPath FROM djmdContent WHERE ID NOT IN (?, ?) ORDER BY FolderPath",
        *BASELINE,
    )


def _playlists(cfg: config.Config, name: str) -> list[tuple]:
    return _query(cfg, "SELECT ID, ParentID, Attribute FROM djmdPlaylist WHERE Name = ?", name)


def _members(cfg: config.Config, playlist_id: str) -> list[str]:
    rows = _query(
        cfg,
        "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY TrackNo",
        playlist_id,
    )
    return [str(row[0]) for row in rows]


def _xml_anywhere(cfg: config.Config, tmp_path: Path) -> list[str]:
    """Every xml document under the test's own tree except the ones it made."""
    return sorted(
        str(path.relative_to(tmp_path))
        for path in tmp_path.rglob("*.xml")
        if path.name not in ("fresh.xml", "collection.xml")
    )


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


def _assert_nothing_written(cfg: config.Config, tmp_path: Path) -> None:
    assert _rows(cfg) == []
    assert _query(cfg, "SELECT COUNT(*) FROM djmdSongPlaylist") == [(0,)]
    assert _xml_anywhere(cfg, tmp_path) == []
    assert session.records(cfg) == ()


def _assert_refused_before_the_gate(envelope: dict, code: int, reason: str) -> None:
    assert envelope["cause"]["reason"] == reason, envelope
    assert code != int(ExitCode.OK)
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert not gates.run_path(envelope["run_id"]).exists()


# ═══════════════════════════════════════════════════════════════════════════
# 1. intake file on a native intake tree
# ═══════════════════════════════════════════════════════════════════════════


def test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root(
    native_library, silence, tmp_path
):
    cfg, root_id = native_library
    path = _single(cfg, silence)
    before = path.read_bytes()

    code, acted, refused = _two_acts(_file(path))

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "ok"
    # The plan the person approved is the plan that was applied.
    assert refused["cause"]["detail"]["shown"]["digest"] == acted["data"]["digest"]
    # The file is where it was and as it was: this verb has never moved one.
    assert path.read_bytes() == before

    ((content_id, title, folder_path),) = _rows(cfg)
    assert folder_path == str(path.resolve())
    assert title == ingest.read_meta(path, cfg=cfg)["name"]
    assert title.startswith("01A - 124 - ")

    ((playlist_id, parent, attribute),) = _playlists(cfg, file_cli.batch_name(path))
    assert str(parent) == root_id, "the batch playlist was not parented to the adopted root"
    assert int(attribute or 0) == 0, "the batch node is a folder, not a playlist"
    assert _members(cfg, str(playlist_id)) == [str(content_id)]

    # NOTHING WAS WRITTEN TO AN EXPORT, and no intake file exists to import.
    assert _xml_anywhere(cfg, tmp_path) == []
    assert tree_registry.pending_intake_xml(cfg) == ()
    assert "pending_human_action" not in acted or acted["pending_human_action"] is None

    item, playlist = acted["data"]["items"]
    assert item["action"] == file_cli.ADDED and item["content_id"] == str(content_id)
    assert item["left_empty"] == sorted(native.LEFT_EMPTY)
    assert playlist == {
        "action": land_cli.PLAYLIST,
        "playlist": file_cli.batch_name(path),
        "id": str(playlist_id),
        "tree": INTAKE,
        "session": playlist["session"],
    }
    assert acted["data"]["totals"] == {
        "count": 1,
        "added": 1,
        "already present": 0,
        "memberships": 1,
    }
    (warning,) = acted["warnings"]
    assert warning["code"] == land_cli.AWAITING_ANALYSIS
    assert file_cli.batch_name(path) in warning["message"] and "Analyze" in warning["message"]

    # What a restore reads and what a revert of the intake cutover refuses over.
    (record,) = session.records(cfg)
    assert record.session_id == playlist["session"]
    assert record.state is session.SessionState.CLOSED
    assert record.sources == {INTAKE: "committed"}
    assert {change.tree: change.created for change in record.change.trees} == {
        INTAKE: 1,
        rb_writer.CONTENT_TABLE: 1,
    }


def test_the_row_carries_the_librarys_own_device(native_library, silence):
    cfg, _root = native_library
    code, acted, _ = _two_acts(_file(_single(cfg, silence)))
    assert code == int(ExitCode.OK), acted
    ((device_id, master),) = _query(
        cfg, "SELECT DeviceID, MasterDBID FROM djmdContent WHERE FolderPath IS NOT NULL"
    )
    assert (str(device_id), str(master)) == MY_DEVICE


def test_after_the_write_no_analysis_value_is_on_the_new_row_column_by_column(
    native_library, silence
):
    """The standing constraint on the new path, read from SQL on the row as
    rekordbox will find it: every column an analysis pass fills, and no cue,
    mixer or file row naming the new row."""
    cfg, _root = native_library
    code, acted, _ = _two_acts(_file(_single(cfg, silence)))
    assert code == int(ExitCode.OK), acted

    selected = ", ".join(native.LEFT_EMPTY)
    ((content_id, *values),) = _query(
        cfg, f"SELECT ID, {selected} FROM djmdContent WHERE FolderPath IS NOT NULL"
    )
    assert len(values) == len(native.LEFT_EMPTY) > 0
    for name, value in zip(native.LEFT_EMPTY, values):
        assert value in (None, 0, 0.0, "", "0"), f"row {content_id} carries {name}={value!r}"
    for table in rb_writer.CONTENT_ANALYSIS_TABLES:
        ((count,),) = _query(cfg, f"SELECT COUNT(*) FROM {table} WHERE ContentID = ?", content_id)
        assert count == 0, f"{table} holds a row for the new content row {content_id}"


def test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database(
    native_library, silence, tmp_path
):
    cfg, root_id = native_library
    path = _single(cfg, silence)

    code, refused = drive(_file(path))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["file"] == str(path.resolve())
    assert shown["reads and writes"] == str(cfg.library.db_path)
    assert shown["playlist"] == (
        f"{file_cli.batch_name(path)} under {DECLARED.intake.display} (row {root_id})"
    )
    assert shown["left empty for rekordbox"] == list(native.LEFT_EMPTY)
    assert shown["adds"] == 1 and shown["already present"] == 0
    (item,) = shown["items"]
    assert item["action"] == native.ADD
    assert item["to"] == str(path.resolve())
    assert set(item["row"]) == {"Title", "FolderPath", "FileNameL", "FileSize", "FileType"}
    # Nothing was written for a plan nobody answered.
    _assert_nothing_written(cfg, tmp_path)
    assert _playlists(cfg, file_cli.batch_name(path)) == []


def test_the_native_gate_takes_no_inline_answer(native_library, silence, tmp_path):
    cfg, _root = native_library
    path = _single(cfg, silence)
    code, envelope = drive(["-d", f"{GATE}=apply", *_file(path)])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["gate"] == GATE
    _assert_nothing_written(cfg, tmp_path)


def test_an_abort_writes_nothing(native_library, silence, tmp_path):
    cfg, _root = native_library
    path = _single(cfg, silence)
    code, refused = drive(_file(path))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *_file(path)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    _assert_nothing_written(cfg, tmp_path)


def test_an_answer_given_for_one_title_is_stale_once_the_file_is_retagged(
    native_library, silence, tmp_path
):
    """The digest covers the row's columns, so a plan approved over one title
    does not write another."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    code, refused = drive(_file(path))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert tags.write_tags(path, {"title": "02A - 126 - Renamed"})

    code, envelope = drive(["--run", run_id, *_file(path)])

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    _assert_nothing_written(cfg, tmp_path)


def test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row(
    native_library, silence
):
    cfg, _root = native_library
    path = _single(cfg, silence)
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('held-1', 'held', ?, 0, '2026-01-01', '2026-01-01')",
        (str(path.resolve()),),
    )
    conn.commit()
    conn.close()

    code, acted, refused = _two_acts(_file(path))

    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 0 and shown["already present"] == 1
    assert code == int(ExitCode.OK), acted
    assert [row[0] for row in _rows(cfg)] == ["held-1"], "the held file gained a second row"
    ((playlist_id, _parent, _attribute),) = _playlists(cfg, file_cli.batch_name(path))
    assert _members(cfg, str(playlist_id)) == ["held-1"]
    item = acted["data"]["items"][0]
    assert item["action"] == native.PRESENT and item["content_id"] == "held-1"
    assert "left_empty" not in item
    assert acted["data"]["totals"] == {
        "count": 1,
        "added": 0,
        "already present": 1,
        "memberships": 1,
    }
    assert acted["warnings"] == [], "nothing joined the collection, so nothing awaits analysis"


def test_an_export_on_a_native_tree_is_refused_by_name_and_not_as_a_defect(
    native_library, silence, export, tmp_path
):
    """The residual's own sentence. Before this unit this drive reached the
    emitter guard: ``tree-unconverged``, ``report-defect``, over a cutover the
    person chose."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    before = export.read_bytes()

    code, envelope = drive(_file(path, "--export", str(export)))

    _assert_refused_before_the_gate(envelope, code, "intake-list-unusable")
    cause = envelope["cause"]
    assert cause["remediation"]["remedy"] == "fix-command-line"
    assert "drop --export" in cause["message"] and INTAKE in cause["message"]
    assert export.read_bytes() == before
    _assert_nothing_written(cfg, tmp_path)


def test_a_file_under_staging_is_refused_on_the_native_medium_too(
    native_library, silence, tmp_path
):
    """A row stamped from staging dies when staging is cleaned, as a Location does."""
    cfg, _root = native_library
    staged = Path(cfg.paths.download_staging) / "Staged.flac"
    shutil.copyfile(silence, staged)
    code, envelope = drive(_file(staged))
    _assert_refused_before_the_gate(envelope, code, "intake-staging-refused")
    _assert_nothing_written(cfg, tmp_path)


def test_a_suffix_the_database_has_no_type_for_is_refused_before_the_gate(
    native_library, silence, tmp_path
):
    cfg, _root = native_library
    odd = _single(cfg, silence).rename(_music(cfg) / "Single.opus")
    code, envelope = drive(_file(odd))
    _assert_refused_before_the_gate(envelope, code, "intake-list-unusable")
    assert "Single.opus" in envelope["cause"]["message"]
    assert "no file type" in envelope["cause"]["message"]
    _assert_nothing_written(cfg, tmp_path)


def test_a_file_no_declared_sub_would_take_is_refused_before_the_gate(
    native_library, silence, tmp_path, monkeypatch
):
    """The shipped taxonomy declares a sub for every file, so the placement
    check is driven at its seam, and what this proves is that the native
    medium asks it at all."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    monkeypatch.setattr(ingest, "decide_placement", lambda meta, declared: None)
    code, envelope = drive(_file(path))
    _assert_refused_before_the_gate(envelope, code, "intake-list-unusable")
    assert "no declared sub" in envelope["cause"]["message"]
    _assert_nothing_written(cfg, tmp_path)


def test_no_acknowledgment_refuses_before_the_gate(machine, silence, tmp_path):
    cfg = machine
    _cut_over_intake(cfg)
    code, envelope = drive(_file(_single(cfg, silence)))
    _assert_refused_before_the_gate(envelope, code, "backup-acknowledgment-missing")
    assert envelope["cause"]["remediation"]["remedy"] == "acknowledge-backup"
    _assert_nothing_written(cfg, tmp_path)


def test_rekordbox_running_refuses_before_the_gate(native_library, silence, tmp_path, monkeypatch):
    cfg, _root = native_library
    path = _single(cfg, silence)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    code, envelope = drive(_file(path))
    _assert_refused_before_the_gate(envelope, code, "rekordbox-running")
    _assert_nothing_written(cfg, tmp_path)


# ═══════════════════════════════════════════════════════════════════════════
# 2. intake file on the bridge, unchanged
# ═══════════════════════════════════════════════════════════════════════════


def test_on_the_bridge_the_export_is_spliced_as_before(bridge_library, silence, export):
    cfg = bridge_library
    path = _single(cfg, silence)
    before = export.read_bytes()

    code, envelope = drive(_file(path, "--export", str(export)))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    intake_file = path.with_name("Single_inboxed.xml")
    assert envelope["pending_human_action"]["artifact"] == str(intake_file)
    written = intake_file.read_bytes()
    assert b'<NODE Name="Single_inboxed" Type="1"' in written
    assert b"Single.flac" in written
    # The playlist has one name on both media: the intake file's stem.
    assert intake_file.stem == file_cli.batch_name(path)
    # The export itself is read and never written, and the database is not touched.
    assert export.read_bytes() == before
    assert _rows(cfg) == []
    assert _playlists(cfg, file_cli.batch_name(path)) == []
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT


def test_on_the_bridge_no_export_is_a_plan_and_asks_no_gate(bridge_library, silence, tmp_path):
    cfg = bridge_library
    path = _single(cfg, silence)
    code, envelope = drive(_file(path))
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["pending_human_action"] is None
    assert envelope.get("cause") is None, "the bridge plan asked a gate"
    assert gates.load(envelope["run_id"]).offers == {}
    _assert_nothing_written(cfg, tmp_path)


# ═══════════════════════════════════════════════════════════════════════════
# 3. The splice refuses a native tree in its own words
# ═══════════════════════════════════════════════════════════════════════════


def _assert_names_the_landing_and_no_defect(cause) -> None:
    assert cause.reason == "tree-unconverged"
    assert str(cause.remediation.remedy) == "fix-command-line"
    assert str(cause.remediation.remedy) != "report-defect"
    assert INTAKE in cause.message and "database native" in cause.message
    assert any("crate intake land" in step for step in cause.remediation.steps)
    assert cause.origin == ("intake.ingest",)
    assert cause.detail == {"tree_id": INTAKE, "mode": str(tree_registry.Mode.DATABASE)}


def test_the_splice_refuses_a_native_intake_tree_naming_the_landing(
    native_library, silence, export, tmp_path
):
    """A caller that did not read the switch. ``place_files`` is the one path
    every xml intake write takes, so this is where the refusal has to be."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    destination = tmp_path / "direct_inboxed.xml"
    before = export.read_bytes()

    with pytest.raises(CratekitError) as raised:
        ingest.place_files([path], cfg=cfg, export=export, destination=destination)

    _assert_names_the_landing_and_no_defect(raised.value.cause)
    assert export.read_bytes() == before
    assert not destination.exists()
    _assert_nothing_written(cfg, tmp_path)


def test_the_splice_refuses_a_native_tree_before_it_looks_for_the_export(
    native_library, silence, tmp_path
):
    """On this medium there is no export to find, so "export the collection
    again" would be the wrong thing to tell anybody."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    with pytest.raises(CratekitError) as raised:
        ingest.place_files(
            [path],
            cfg=cfg,
            export=tmp_path / "no-such.xml",
            destination=tmp_path / "direct_inboxed.xml",
        )
    _assert_names_the_landing_and_no_defect(raised.value.cause)


def test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way(
    native_library, silence, tmp_path
):
    """The landing's pre-move check reaches the emitter on a copy. A caller that
    came to the bridge engine on a native tree is told what the splice tells it,
    with nothing moved."""
    cfg, _root = native_library
    staged = Path(cfg.paths.download_staging) / "One.flac"
    shutil.copyfile(silence, staged)
    assert tags.write_tags(staged, {"title": "One", "artist": "Probe", "genre": "Deep House"})
    planned = landing.plan(Path(cfg.paths.download_staging), cfg, "2026-09-30_batch")

    with pytest.raises(CratekitError) as raised:
        landing.preflight(
            planned,
            cfg=cfg,
            export=tmp_path / "no-such.xml",
            destination=land_cli.intake_file(cfg, "2026-09-30_batch"),
        )

    _assert_names_the_landing_and_no_defect(raised.value.cause)
    assert staged.exists()


def test_the_splice_still_takes_a_bridge_tree(bridge_library, silence, export, tmp_path):
    cfg = bridge_library
    path = _single(cfg, silence)
    destination = tmp_path / "direct_inboxed.xml"
    (placed,) = ingest.place_files([path], cfg=cfg, export=export, destination=destination)
    assert placed.path == path and destination.is_file()


def test_every_caller_of_the_intake_emitter_asks_the_bridge_assertion_first():
    """The emitter guard says ``report-defect``. A writer that reaches it
    without asking the assertion first tells a person who chose a cutover to
    file a bug, which is the finding. The callers are named, so a third one is
    a line somebody reads in a diff."""
    callers: dict[str, tuple[int, list[int]]] = {}
    for module in sorted(SRC.rglob("*.py")):
        if module.name == "rbxml.py":
            continue
        tree = ast.parse(module.read_text(encoding="utf-8"))
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            emits = [
                node.lineno
                for node in ast.walk(function)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "insert_intake_playlist"
            ]
            if not emits:
                continue
            asked = [
                node.lineno
                for node in ast.walk(function)
                if isinstance(node, ast.Call)
                and isinstance(node.func, (ast.Attribute, ast.Name))
                and getattr(node.func, "attr", getattr(node.func, "id", ""))
                == "assert_intake_on_the_bridge"
            ]
            key = f"{module.relative_to(SRC).as_posix()}::{function.name}"
            callers[key] = (min(emits), asked)

    assert set(callers) == {"intake/ingest.py::place_files", "intake/landing.py::_check_export"}
    for key, (first_emit, asked) in callers.items():
        assert asked and min(asked) < first_emit, (
            f"{key} reaches the intake emitter without asking the bridge assertion first"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 4. The verbs the ledger named that never splice, on both media
# ═══════════════════════════════════════════════════════════════════════════


def _assert_the_intake_tree_was_left_alone(cfg: config.Config, exported: Path, before: bytes):
    assert exported.read_bytes() == before, "the export was written"
    assert tree_registry.pending_intake_xml(cfg) == (), "an intake file was written"
    assert _rows(cfg) == [], "a content row was written"
    assert _query(cfg, "SELECT COUNT(*) FROM djmdSongPlaylist") == [(0,)]
    assert session.records(cfg) == (), "a write session was opened"


def test_the_favourites_sweep_queues_and_hearts_on_either_medium(either, monkeypatch):
    cfg = either
    exported = outbound_fakes.write_export(cfg.library.root / "outbound")
    before = exported.read_bytes()
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind_account(monkeypatch, account)

    _run, job_id = approve_and_queue(
        ["sync", "favorites", "--export", str(exported)], "sync.favorites.confirm"
    )
    code, resumed = resume_outbound(job_id)

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert account.hearted, "the sweep hearted nothing, so this drive proved nothing"
    _assert_the_intake_tree_was_left_alone(cfg, exported, before)


def test_the_composed_pass_queues_each_source_on_either_medium(either, monkeypatch):
    from cratekit.sync import cli as sync_cli

    cfg = either
    exported = outbound_fakes.write_export(cfg.library.root / "outbound")
    before = exported.read_bytes()
    bind_account(monkeypatch, outbound_fakes.FakeAccount(catalog={}))
    register(*LABELS[:2])
    verb = ["sync", "all", "--export", str(exported)]

    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == sync_cli.CONFIRM
    decided, envelope = drive(
        ["run", "decide", refused["run_id"], sync_cli.CONFIRM, "sync", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, passed = drive(["--run", refused["run_id"], *verb])

    assert code == int(ExitCode.OK), passed
    with jobs.open_store() as store:
        queued = {job.handler_key for job in jobs.list_jobs(store)}
    assert queued == {"sync.favorites", "sync.labels"}
    _assert_the_intake_tree_was_left_alone(cfg, exported, before)


def test_the_label_batch_sweeps_on_either_medium(either, monkeypatch):
    cfg = either
    exported = outbound_fakes.write_export(cfg.library.root / "outbound")
    before = exported.read_bytes()
    register(*LABELS[:2])
    bind_catalogue(monkeypatch, readable(*SLUGS[:2]))

    code, queued = drive(["sync", "labels"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    with jobs.open_store() as store:
        states = {item.item_id: str(item.state) for item in jobs.items(store, job_id)}
    assert states == {slug: str(jobs.ItemState.DONE) for slug in SLUGS[:2]}
    _assert_the_intake_tree_was_left_alone(cfg, exported, before)


# ═══════════════════════════════════════════════════════════════════════════
# 5. One switch
# ═══════════════════════════════════════════════════════════════════════════


def test_the_switch_reads_the_recorded_mode_and_nothing_else(machine):
    cfg = machine
    assert ingest.intake_medium(cfg).native is False
    root_id = _cut_over_intake(cfg)
    medium = ingest.intake_medium(cfg)
    assert medium.native is True
    assert medium.declared.intake.id == INTAKE
    assert medium.registry.record(INTAKE).root_id == root_id
    # ANOTHER TREE'S CUTOVER IS NOT THE INTAKE TREE'S.
    tree_registry.write(
        cfg,
        tree_registry.Registry().with_record(
            tree_registry.TreeRecord(
                tree_id=DECLARED.tree.id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=TODAY,
                root_id="root-genre",
                source=tree_registry.DerivationSource.TAXONOMY,
            )
        ),
    )
    assert ingest.intake_medium(cfg).native is False


def test_an_unreachable_library_root_decides_nothing(machine):
    """The registry lives under the root. With no root there is no record to
    read, and the bridge path is taken as it was before the second medium."""
    cfg = machine
    _cut_over_intake(cfg)
    shutil.move(str(cfg.library.root), str(Path(cfg.library.root).with_name("unmounted")))
    medium = ingest.intake_medium(cfg)
    assert (medium.declared, medium.registry, medium.native) == (None, None, False)


def test_both_intake_verbs_read_the_one_switch_and_nothing_beside_it_reads_the_mode():
    """No second switch. Under ``intake`` the recorded mode is read in one
    module, and both verbs that write the intake tree call the function there."""
    readers: set[str] = set()
    switched: set[str] = set()
    for module in sorted((SRC / "intake").glob("*.py")):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            if node.func.attr in ("is_database_native", "is_on_the_bridge", "mode"):
                readers.add(module.name)
            if node.func.attr == "intake_medium":
                switched.add(module.name)
    assert readers == {"ingest.py"}
    assert switched == {"land_cli.py", "file_cli.py"}
