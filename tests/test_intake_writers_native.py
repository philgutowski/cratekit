"""R-770: every intake writer chooses its medium by the intake tree's mode, read by one
switch. A native ``intake file`` adds one row and one batch playlist and writes no export,
the bridge is unchanged, and the splice refuses a native tree in its own words. D1.
"""

from __future__ import annotations

import ast
import shutil
import sqlite3
import unicodedata
from pathlib import Path

import pytest

from cratekit.cli import gates
from cratekit.core import config, jobs, rb_writer, session, tags, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import file_cli, ingest, land_cli, landing, native
from cratekit.modules.outbound import source as outbound_source
from tests import outbound_fakes
from tests import test_intake_land_native as land
from tests.cli_drive import approve_and_queue, drive
from tests.test_intake_land_native import (
    DECLARED,
    INTAKE,
    LIBRARY_LINK,
    MY_DEVICE,
    TODAY,
    _cut_over_intake,
    _members,
    _query,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_label_workers import LABELS, SLUGS, queued_sweep, readable, register
from tests.test_label_workers import bind as bind_catalogue
from tests.test_outbound_workers import _resume as resume_outbound
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import catalog
from tests.xml_fixtures import _fresh_xml

GATE = file_cli.FILE_GATE
SRC = Path(ingest.__file__).resolve().parents[1]

BRIDGE = "bridge"
NATIVE = "native"

#: The two rows ``_build_disposable_database`` seeds, which name no file.
BASELINE = ("1", "2")


@pytest.fixture(autouse=True)
def _forget_libraries():
    outbound_source.forget_libraries()
    yield
    outbound_source.forget_libraries()


def _machine(tmp_path, monkeypatch, *, profile: str | None = None) -> config.Config:
    return land._configured(land._library_root(tmp_path, monkeypatch), monkeypatch, profile=profile)


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


@pytest.fixture(params=(BRIDGE, NATIVE))
def both(request, bridge_library) -> config.Config:
    if request.param == NATIVE:
        _cut_over_intake(bridge_library)
    return bridge_library


@pytest.fixture
def export(tmp_path: Path) -> Path:
    path = tmp_path / "fresh.xml"
    path.write_bytes(_fresh_xml())
    return path


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir


def _tagged(silence: Path, path: Path, title: str) -> Path:
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    return path


def _single(cfg: config.Config, silence: Path, name: str = "Single.flac") -> Path:
    """One tagged file already in the library, where this verb finds its files."""
    return _tagged(silence, _music(cfg) / name, f"01A - 124 - {Path(name).stem}")


def _outside(tmp_path: Path, silence: Path) -> Path:
    (tmp_path / "elsewhere").mkdir()
    return _tagged(silence, tmp_path / "elsewhere" / "Out.flac", "Out")


def _staged_one(cfg: config.Config, silence: Path) -> Path:
    return _tagged(silence, Path(cfg.paths.download_staging) / "One.flac", "One")


def _file(path: Path, *extra: str) -> list[str]:
    return ["intake", "file", str(path), *extra]


def _rows(cfg: config.Config) -> list[tuple]:
    """Every content row beyond the two the disposable database is built with."""
    sql = "SELECT ID, Title, FolderPath FROM djmdContent WHERE ID NOT IN (?, ?) ORDER BY FolderPath"
    return _query(cfg, sql, *BASELINE)


def _playlists(cfg: config.Config, name: str) -> list[tuple]:
    return _query(cfg, "SELECT ID, ParentID, Attribute FROM djmdPlaylist WHERE Name = ?", name)


def _xml_anywhere(cfg: config.Config, tmp_path: Path) -> list[str]:
    """Every xml document under the test's own tree except the ones it made."""
    made = ("fresh.xml", "collection.xml")
    found = tmp_path.rglob("*.xml")
    return sorted(str(path.relative_to(tmp_path)) for path in found if path.name not in made)


def _two_acts(verb: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against this verb's explicit gate, then the acting drive."""
    return land._two_acts(verb, GATE)


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


# 1. intake file on a native intake tree
def test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root(
        native_library, silence, tmp_path):
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
    # The library's own device, and no analysis value, cue, mixer or file row for it.
    selected = ", ".join(native.LEFT_EMPTY)
    sql = f"SELECT DeviceID, MasterDBID, {selected} FROM djmdContent WHERE ID = ?"
    ((device_id, master, *values),) = _query(cfg, sql, content_id)
    assert (str(device_id), str(master)) == MY_DEVICE
    assert len(values) == len(native.LEFT_EMPTY) > 0
    for name, value in zip(native.LEFT_EMPTY, values):
        assert value in (None, 0, 0.0, "", "0"), f"row {content_id} carries {name}={value!r}"
    for table in rb_writer.CONTENT_ANALYSIS_TABLES:
        ((count,),) = _query(cfg, f"SELECT COUNT(*) FROM {table} WHERE ContentID = ?", content_id)
        assert count == 0, f"{table} holds a row for the new content row {content_id}"
    ((playlist_id, parent, attribute),) = _playlists(cfg, path.stem)
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
        "action": land_cli.PLAYLIST, "playlist": path.stem, "id": str(playlist_id), "tree": INTAKE,
        "session": playlist["session"],
    }
    assert acted["data"]["totals"] == {"count": 1, "added": 1, "already present": 0, "memberships": 1}
    # U127: uncalibrated, the row joins with no vox My Tag and the second warning says why.
    warning, vox = acted["warnings"]
    assert warning["code"] == land_cli.AWAITING_ANALYSIS
    # U166: the one playlist the visit selects, not the batch the row joined.
    assert f"{DECLARED.intake.display} / {native.ANALYZE}" in warning["message"]
    assert vox["code"] == land_cli.VOX_NOT_WRITTEN
    assert native.VOX_UNCALIBRATED in vox["message"]
    # What a restore reads and what a revert of the intake cutover refuses over.
    (record,) = session.records(cfg)
    assert record.session_id == playlist["session"]
    assert record.state is session.SessionState.CLOSED
    assert record.sources == {INTAKE: "committed"}
    # U166: the batch's one membership and INBOX / Analyze's one.
    created = {change.tree: change.created for change in record.change.trees}
    assert created == {INTAKE: 2, rb_writer.CONTENT_TABLE: 1}


def test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database(
        native_library, silence, tmp_path):
    """And the gate takes no inline answer, and an abort writes nothing."""
    cfg, root_id = native_library
    path = _single(cfg, silence)
    code, inline = drive(["-d", f"{GATE}=apply", *_file(path)])
    assert code == int(ExitCode.DECISION_REQUIRED), inline
    assert inline["cause"]["detail"]["gate"] == GATE
    code, refused = drive(_file(path))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["file"] == str(path.resolve())
    assert shown["reads and writes"] == str(cfg.library.db_path)
    assert shown["playlist"] == f"{path.stem} under {DECLARED.intake.display} (row {root_id})"
    assert shown["left empty for rekordbox"] == list(native.LEFT_EMPTY)
    assert shown["adds"] == 1 and shown["already present"] == 0
    (item,) = shown["items"]
    assert item["action"] == native.ADD
    assert item["to"] == str(path.resolve())
    assert set(item["row"]) == {
        "Title", "FolderPath", "FileNameL", "FileSize", "FileType", rb_writer.FILE_ID_COLUMN,
        rb_writer.CONTENT_LINK_COLUMN,
        # U163: the file's artist and genre, each with the row it takes.
        native.ARTIST_COLUMN, native.GENRE_COLUMN,
    }
    # THE LIBRARY'S VALUE, shown with its count, never the binding's (U126).
    assert item["row"][rb_writer.CONTENT_LINK_COLUMN] == LIBRARY_LINK
    assert shown["content link"] == f"{LIBRARY_LINK}, carried by 2 of the library's 2 live rows"
    # U115: the file id is named as a sentence, since no plan can know the number.
    assert item["row"][rb_writer.FILE_ID_COLUMN] == native.FILE_ID_AT_LANDING
    # Nothing was written for a plan nobody answered.
    _assert_nothing_written(cfg, tmp_path)
    assert _playlists(cfg, path.stem) == []
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *_file(path)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    _assert_nothing_written(cfg, tmp_path)


def _retitled(cfg: config.Config, path: Path) -> None:
    """The digest covers the row's columns."""
    tags.write_tags(path, {"title": "02A - 126 - Renamed"})


def _grown(cfg: config.Config, path: Path) -> None:
    """The plan's half of the digest alone: the row's size moved and nothing the verb lists did."""
    with path.open("ab") as handle:
        handle.write(b"\0" * 64)
    assert ingest.read_meta(path, cfg=cfg)["name"].startswith("01A - 124 - ")


def _reartisted(cfg: config.Config, path: Path) -> None:
    """The verb's own half alone: the artist is on the plan read and on no column the row sets."""
    size = path.stat().st_size
    tags.write_tags(path, {"artist": "Other"})
    assert path.stat().st_size == size, "the retag moved the size, so this proves nothing"


@pytest.mark.parametrize("change", [_retitled, _grown, _reartisted])
def test_an_answer_is_stale_once_the_file_changed_after_it(
        native_library, silence, tmp_path, change):
    cfg, _root = native_library
    path = _single(cfg, silence)
    _code, refused = drive(_file(path))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    change(cfg, path)
    code, envelope = drive(["--run", run_id, *_file(path)])
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    _assert_nothing_written(cfg, tmp_path)


def test_intake_file_tags_its_row_vox_from_the_files_score(native_library, silence):
    """U127 through ``intake file``: a file scoring at the cut joins with the vox My Tag."""
    from cratekit.adopt import placements as adopt_placements
    from tests.test_intake_land_vox_native import _calibrate, _seed_vocals
    cfg, _root = native_library
    _calibrate(cfg)
    _seed_vocals(cfg)
    path = _single(cfg, silence)
    assert tags.write_tags(path, {"voxlevel": "5"})
    code, acted, refused = _two_acts(_file(path))
    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["vox My Tag"].startswith("1 of 1 added row(s)")
    ((content_id, _title, _folder),) = _rows(cfg)
    db = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        assert adopt_placements.vox_tagged(db) == {str(content_id)}
    finally:
        rb_writer.close_db(db)
    assert [w["code"] for w in acted["warnings"]] == [land_cli.AWAITING_ANALYSIS]


def test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row(
        native_library, silence):
    cfg, _root = native_library
    path = _single(cfg, silence)
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('held-1', 'held', ?, 0, '2026-01-01', '2026-01-01')",
        (str(path.resolve()),))
    conn.commit()
    conn.close()
    code, acted, refused = _two_acts(_file(path))
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 0 and shown["already present"] == 1
    assert code == int(ExitCode.OK), acted
    assert [row[0] for row in _rows(cfg)] == ["held-1"], "the held file gained a second row"
    ((playlist_id, _parent, _attribute),) = _playlists(cfg, path.stem)
    assert _members(cfg, str(playlist_id)) == ["held-1"]
    item = acted["data"]["items"][0]
    assert item["action"] == native.PRESENT and item["content_id"] == "held-1"
    assert "left_empty" not in item
    assert acted["data"]["totals"] == {"count": 1, "added": 0, "already present": 1, "memberships": 1}
    assert acted["warnings"] == [], "nothing joined the collection, so nothing awaits analysis"


def test_an_export_on_a_native_tree_is_refused_by_name_and_not_as_a_defect(
        native_library, silence, export, tmp_path):
    """The residual's sentence: this once reached the emitter guard as ``report-defect``."""
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


def _from_staging(cfg, silence, tmp_path, monkeypatch):
    """A row stamped from staging dies when staging is cleaned, as a Location does."""
    staged = Path(cfg.paths.download_staging) / "Staged.flac"
    shutil.copyfile(silence, staged)
    return staged, ()


def _untyped(cfg, silence, tmp_path, monkeypatch):
    return _single(cfg, silence).rename(_music(cfg) / "Single.opus"), ("Single.opus", "no file type")


def _unplaceable(cfg, silence, tmp_path, monkeypatch):
    """Every file has a declared sub, so the check is driven at its seam to prove it is asked."""
    path = _single(cfg, silence)
    monkeypatch.setattr(ingest, "decide_placement", lambda meta, declared: None)
    return path, ("no declared sub",)


def _outside_the_library(cfg, silence, tmp_path, monkeypatch):
    """Once added, then never found under the root, so a second run planned a second row."""
    return _outside(tmp_path, silence), ("Out.flac", "outside the library", str(cfg.library.root))


def _rekordbox_running(cfg, silence, tmp_path, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    return _single(cfg, silence), ()


@pytest.mark.parametrize(
    ("made", "reason"),
    [
        (_from_staging, "intake-staging-refused"), (_untyped, "intake-list-unusable"),
        (_unplaceable, "intake-list-unusable"), (_outside_the_library, "intake-list-unusable"),
        (_rekordbox_running, "rekordbox-running"),
    ])
def test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate(
        native_library, silence, tmp_path, monkeypatch, made, reason):
    cfg, _root = native_library
    path, said = made(cfg, silence, tmp_path, monkeypatch)
    code, envelope = drive(_file(path))
    _assert_refused_before_the_gate(envelope, code, reason)
    message = envelope["cause"]["message"]
    assert [one for one in said if one not in message] == [], message
    _assert_nothing_written(cfg, tmp_path)


def test_no_acknowledgment_refuses_before_the_gate(machine, silence, tmp_path):
    cfg = machine
    _cut_over_intake(cfg)
    code, envelope = drive(_file(_single(cfg, silence)))
    _assert_refused_before_the_gate(envelope, code, "backup-acknowledgment-missing")
    assert envelope["cause"]["remediation"]["remedy"] == "acknowledge-backup"
    _assert_nothing_written(cfg, tmp_path)


def test_a_file_outside_the_library_is_still_spliced_on_the_bridge(
        bridge_library, silence, export, tmp_path):
    """The bridge never asked, and still does not: a Location is text."""
    outside = _outside(tmp_path, silence)
    code, envelope = drive(_file(outside, "--export", str(export)))
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert b"Out.flac" in (outside.parent / "Out_inboxed.xml").read_bytes()


def test_a_file_named_through_a_link_is_stored_under_the_configured_root(
        native_library, silence, tmp_path):
    """Spelled under the configured root, as landing spells it, however the file was reached."""
    from dataclasses import replace
    cfg, _root = native_library
    path = _single(cfg, silence)
    alias = tmp_path / "alias"
    alias.symlink_to(cfg.library.root, target_is_directory=True)
    linked = replace(cfg, library=replace(cfg.library, root=alias))
    assert file_cli._in_the_library(path, linked) == alias / cfg.library.music_dir / "Single.flac"
    through = alias / path.relative_to(cfg.library.root)
    assert through.is_file() and str(through) != str(path)
    code, acted, _ = _two_acts(_file(through))
    assert code == int(ExitCode.OK), acted
    ((_content_id, _title, folder_path),) = _rows(cfg)
    assert folder_path == str(Path(cfg.library.root) / cfg.library.music_dir / "Single.flac")
    # A second run finds the row it made, where the unresolved spelling planned another.
    code, refused = drive(_file(through))
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 0 and shown["already present"] == 1
def test_the_engine_refuses_a_target_it_cannot_resolve_instead_of_planning_an_add(
        native_library, silence, tmp_path):
    """Unasked is not absent: a path off the root once read as having no row."""
    cfg, _root = native_library
    outside = tmp_path / "elsewhere.flac"
    shutil.copyfile(silence, outside)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        with pytest.raises(CratekitError) as raised:
            native.plan_rows(cfg, db, tree_id=INTAKE, registry=tree_registry.read(cfg),
                             batch="probe", files=[(outside, outside)])
    finally:
        rb_writer.close_db(db)
    cause = raised.value.cause
    assert cause.reason == "intake-list-unusable"
    assert str(outside) in cause.message and "no row was planned" in cause.message


def test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy(
        native_library, silence, tmp_path, monkeypatch):
    """A binding failure says what it leaves, and the skew refusal keeps its own remedy."""
    cfg, root_id = native_library
    path = _single(cfg, silence)

    def broken(*args, **kwargs):
        raise ValueError("the binding said no")
    monkeypatch.setattr(native, "apply_rows", broken)
    code, acted, _ = _two_acts(_file(path))
    assert code != int(ExitCode.OK), acted
    cause = acted["cause"]
    assert cause["reason"] == "internal-error"
    assert "the binding said no" in cause["message"]
    assert "no row was added and Single.flac is where it was" in cause["message"]
    assert path.is_file()
    assert _rows(cfg) == []

    def skewed(*args, **kwargs):
        said = "the adopted intake root could not be read back"
        raise tree_registry.RegistrySkew(said, tree_id=INTAKE, root_id=root_id)
    monkeypatch.setattr(native, "apply_rows", skewed)
    code, acted, _ = _two_acts(_file(path))
    cause = acted["cause"]
    assert cause["reason"] == "tree-unconverged"
    assert cause["remediation"]["remedy"] == "restore-from-snapshot"
    assert "the adopted intake root could not be read back" in cause["message"]
    assert "no row was added" in cause["message"]
    assert cause["detail"]["tree_id"] == INTAKE and cause["detail"]["source"] == str(path)
# 2. intake file on the bridge, unchanged
def test_on_the_bridge_the_export_is_spliced_as_before(bridge_library, silence, export, tmp_path):
    cfg = bridge_library
    path = _single(cfg, silence)
    before = export.read_bytes()
    code, envelope = drive(_file(path, "--export", str(export)))
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    intake_file = path.with_name("Single_inboxed.xml")
    assert envelope["pending_human_action"]["artifact"] == str(intake_file)
    written = intake_file.read_bytes()
    # The bridge names the batch playlist after its intake file, as it did.
    assert b'<NODE Name="Single_inboxed" Type="1"' in written
    assert b"Single.flac" in written
    # The export itself is read and never written, and the database is not touched.
    assert export.read_bytes() == before
    assert _rows(cfg) == []
    assert _playlists(cfg, path.stem) == []
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT
    # And the splice called directly still takes a bridge tree.
    destination = tmp_path / "direct_inboxed.xml"
    (placed,) = ingest.place_files([path], cfg=cfg, export=export, destination=destination)
    assert placed.path == path and destination.is_file()


def test_on_the_bridge_no_export_is_a_plan_and_asks_no_gate(bridge_library, silence, tmp_path):
    """The bridge reads the medium before its plan too: an unreadable registry says why."""
    cfg = bridge_library
    path = _single(cfg, silence)
    code, envelope = drive(_file(path))
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["pending_human_action"] is None
    assert envelope.get("cause") is None, "the bridge plan asked a gate"
    assert gates.load(envelope["run_id"]).offers == {}
    _assert_nothing_written(cfg, tmp_path)
    registry_file = tree_registry.path_for(cfg)
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    registry_file.write_text("{ not json", encoding="utf-8")
    code, envelope = drive(_file(path))
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "tree-registry-unusable"
    assert _rows(cfg) == [] and _xml_anywhere(cfg, tmp_path) == []


def test_a_file_that_is_not_there_or_not_audio_refuses_from_the_vocabulary_on_either_medium(
        both, tmp_path):
    """Held here on both media since the conformance sample needed a file that exists."""
    cfg = both
    notes = _music(cfg) / "notes.txt"
    notes.write_text("not audio\n", encoding="utf-8")
    for path, said in (
        (_music(cfg) / "no-such-track.flac", "is not a file on this machine"),
        (notes, "not an audio file"),
    ):
        code, envelope = drive(_file(path))
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "intake-list-unusable"
        assert said in envelope["cause"]["message"]
    _assert_nothing_written(cfg, tmp_path)
# 3. The splice refuses a native tree in its own words
def _assert_names_the_landing_and_no_defect(cause) -> None:
    assert cause.reason == "tree-unconverged"
    assert str(cause.remediation.remedy) == "fix-command-line"
    assert str(cause.remediation.remedy) != "report-defect"
    assert INTAKE in cause.message and "database native" in cause.message
    assert any("crate intake land" in step for step in cause.remediation.steps)
    assert cause.origin == ("intake.ingest",)
    assert cause.detail == {"tree_id": INTAKE, "mode": str(tree_registry.Mode.DATABASE)}


def test_the_splice_refuses_a_native_intake_tree_naming_the_landing(
        native_library, silence, export, tmp_path):
    """The refusal sits in ``place_files`` before the export is looked for: no re-export helps."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    destination = tmp_path / "direct_inboxed.xml"
    before = export.read_bytes()
    for given in (export, tmp_path / "no-such.xml"):
        with pytest.raises(CratekitError) as raised:
            ingest.place_files([path], cfg=cfg, export=given, destination=destination)
        _assert_names_the_landing_and_no_defect(raised.value.cause)
    assert export.read_bytes() == before
    assert not destination.exists()
    _assert_nothing_written(cfg, tmp_path)


def test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way_and_moves_nothing(
        native_library, silence, export, tmp_path):
    """The pre-move check and the apply's registry read (R-677) say what the splice says."""
    cfg, _root = native_library
    staged = _staged_one(cfg, silence)
    planned = landing.plan(Path(cfg.paths.download_staging), cfg, "2026-09-30_batch")
    destination = land_cli.intake_file(cfg, "2026-09-30_batch")
    with pytest.raises(CratekitError) as raised:
        landing.preflight(planned, cfg=cfg, export=tmp_path / "no-such.xml", destination=destination)
    _assert_names_the_landing_and_no_defect(raised.value.cause)
    assert staged.exists()
    with pytest.raises(CratekitError) as raised:
        landing.apply(planned, cfg=cfg, export=export, destination=destination)
    _assert_names_the_landing_and_no_defect(raised.value.cause)
    assert staged.exists() and not destination.exists()
    assert not (Path(cfg.library.root) / cfg.library.music_dir / "2026-09-30_batch").exists()
def test_every_intake_emitter_caller_builds_its_tree_through_the_one_refusing_builder():
    callers: dict[str, tuple[int, list[int]]] = {}
    builders: list[str] = []
    for module in sorted(SRC.rglob("*.py")):
        text = module.read_text(encoding="utf-8")
        # Neither name in the text, no node of either: only such modules are parsed.
        folded = unicodedata.normalize("NFKC", text)
        if "intake_tree" not in folded and "insert_intake_playlist" not in folded:
            continue
        tree = ast.parse(text)
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            key = f"{module.relative_to(SRC).as_posix()}::{function.name}"
            calls = [node for node in ast.walk(function) if isinstance(node, ast.Call)]
            attrs = [(n.lineno, n.func.attr) for n in calls if isinstance(n.func, ast.Attribute)]
            builders += [key for _line, attr in attrs if attr == "intake_tree"]
            emits = [line for line, attr in attrs if attr == "insert_intake_playlist"]
            if not emits or module.name == "rbxml.py":
                continue
            named = attrs + [(n.lineno, n.func.id) for n in calls if isinstance(n.func, ast.Name)]
            asked = [line for line, name in named if name == "bridge_intake_tree"]
            callers[key] = (min(emits), asked)
    assert set(callers) == {"intake/ingest.py::place_files", "intake/landing.py::_check_export"}
    for key, (first_emit, asked) in callers.items():
        assert asked and min(asked) < first_emit, (
            f"{key} reaches the intake emitter without building its tree through "
            f"the function that refuses a native one first"
        )
    assert builders == ["intake/ingest.py::bridge_intake_tree"]
    parsed = ast.parse(Path(ingest.__file__).read_text(encoding="utf-8"))
    (function,) = [
        node for node in ast.walk(parsed)
        if isinstance(node, ast.FunctionDef) and node.name == "bridge_intake_tree"
    ]
    first, second = [
        node for node in function.body
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant))
    ]
    assert isinstance(first, ast.Expr) and first.value.func.id == "assert_intake_on_the_bridge"
    assert isinstance(second, ast.Return)


# 4. The verbs the ledger named that never splice, on both media
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
        ["sync", "favorites", "--export", str(exported)], "sync.favorites.confirm")
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
    decision = ["run", "decide", refused["run_id"], sync_cli.CONFIRM, "sync", "--actor", "a-person"]
    decided, envelope = drive(decision)
    assert decided == int(ExitCode.OK), envelope
    code, passed = drive(["--run", refused["run_id"], *verb])
    assert code == int(ExitCode.OK), passed
    with jobs.open_store() as store:
        queued = {job.handler_key for job in jobs.list_jobs(store)}
    # LABELS REGISTERED AND NOT SWEPT (U109): ``crate label sync`` takes them.
    assert queued == {"sync.favorites"}
    _assert_the_intake_tree_was_left_alone(cfg, exported, before)


def test_the_label_batch_sweeps_on_either_medium(either, monkeypatch):
    cfg = either
    exported = outbound_fakes.write_export(cfg.library.root / "outbound")
    before = exported.read_bytes()
    register(*LABELS[:2])
    bind_catalogue(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    with jobs.open_store() as store:
        states = {item.item_id: str(item.state) for item in jobs.items(store, job_id)}
    assert states == {slug: str(jobs.ItemState.DONE) for slug in SLUGS[:2]}
    _assert_the_intake_tree_was_left_alone(cfg, exported, before)


# 5. One switch
def test_the_switch_reads_the_recorded_mode_and_nothing_else(machine):
    cfg = machine
    assert ingest.intake_medium(cfg).native is False
    root_id = _cut_over_intake(cfg)
    medium = ingest.intake_medium(cfg)
    assert medium.native is True
    assert medium.declared.intake.id == INTAKE
    assert medium.registry.record(INTAKE).root_id == root_id
    # ANOTHER TREE'S CUTOVER IS NOT THE INTAKE TREE'S.
    genre = tree_registry.TreeRecord(
        tree_id=DECLARED.tree.id, mode=tree_registry.Mode.DATABASE, cutover_on=TODAY,
        root_id="root-genre", source=tree_registry.DerivationSource.TAXONOMY)
    tree_registry.write(cfg, tree_registry.Registry().with_record(genre))
    assert ingest.intake_medium(cfg).native is False
    # The registry lives under the root: with none there is no record, so the bridge is taken.
    _cut_over_intake(cfg)
    shutil.move(str(cfg.library.root), str(Path(cfg.library.root).with_name("unmounted")))
    medium = ingest.intake_medium(cfg)
    assert (medium.declared, medium.registry, medium.native) == (None, None, False)
def test_both_intake_verbs_read_the_one_switch_and_nothing_beside_it_reads_the_mode():
    """No second switch: one module reads the mode, for both verbs and the backfill (U121)."""
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
    assert switched == {"land_cli.py", "file_cli.py", "inspiration_cli.py"}
