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
    LIBRARY_LINK,
    MY_DEVICE,
    TODAY,
    _cut_over_intake,
    _query,
    _seed_binding_rows,
)
from tests.test_label_workers import LABELS, SLUGS, queued_sweep, readable, register
from tests.test_label_workers import bind as bind_catalogue
from tests.test_outbound_workers import _resume as resume_outbound
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import catalog
from tests.test_rb_writer_db import RECORDED_APP_VERSION
from tests.xml_fixtures import _fresh_xml

GATE = file_cli.FILE_GATE
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
        "action": land_cli.PLAYLIST,
        "playlist": path.stem,
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
    assert path.stem in warning["message"] and "Analyze" in warning["message"]

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
        f"{path.stem} under {DECLARED.intake.display} (row {root_id})"
    )
    assert shown["left empty for rekordbox"] == list(native.LEFT_EMPTY)
    assert shown["adds"] == 1 and shown["already present"] == 0
    (item,) = shown["items"]
    assert item["action"] == native.ADD
    assert item["to"] == str(path.resolve())
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
    # Nothing was written for a plan nobody answered.
    _assert_nothing_written(cfg, tmp_path)
    assert _playlists(cfg, path.stem) == []


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


def test_an_answer_is_stale_once_the_file_itself_changed_under_the_same_tags(
    native_library, silence, tmp_path
):
    """The collection plan's half of the digest, alone: the size the row would
    carry moved and nothing the verb's own plan lists did."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    code, refused = drive(_file(path))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    with path.open("ab") as handle:
        handle.write(b"\0" * 64)
    assert ingest.read_meta(path, cfg=cfg)["name"].startswith("01A - 124 - ")

    code, envelope = drive(["--run", run_id, *_file(path)])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    _assert_nothing_written(cfg, tmp_path)


def test_an_answer_is_stale_once_the_artist_the_plan_showed_changed(
    native_library, silence, tmp_path
):
    """The verb's own half of the digest, alone: the artist is on the plan the
    person read and on no column the row sets."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    size = path.stat().st_size
    code, refused = drive(_file(path))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert tags.write_tags(path, {"artist": "Other"})
    assert path.stat().st_size == size, "the retag moved the size, so this proves nothing"

    code, envelope = drive(["--run", run_id, *_file(path)])

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
    ((playlist_id, _parent, _attribute),) = _playlists(cfg, path.stem)
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


def test_a_file_outside_the_library_is_refused_on_the_native_medium(
    native_library, silence, tmp_path
):
    """The review drove this: a file outside the root was planned as an add,
    written, and could never be found again, since the matcher resolves under
    the root. A second run then planned a second row for it."""
    cfg, _root = native_library
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    outside = elsewhere / "Out.flac"
    shutil.copyfile(silence, outside)
    assert tags.write_tags(outside, {"title": "Out", "artist": "Probe", "genre": "Deep House"})

    code, envelope = drive(_file(outside))

    _assert_refused_before_the_gate(envelope, code, "intake-list-unusable")
    message = envelope["cause"]["message"]
    assert "Out.flac" in message and "outside the library" in message
    assert str(cfg.library.root) in message
    _assert_nothing_written(cfg, tmp_path)


def test_a_file_outside_the_library_is_still_spliced_on_the_bridge(
    bridge_library, silence, export, tmp_path
):
    """The bridge never asked, and still does not: a Location is text."""
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    outside = elsewhere / "Out.flac"
    shutil.copyfile(silence, outside)
    assert tags.write_tags(outside, {"title": "Out", "artist": "Probe", "genre": "Deep House"})
    code, envelope = drive(_file(outside, "--export", str(export)))
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert b"Out.flac" in (elsewhere / "Out_inboxed.xml").read_bytes()


def test_a_file_named_through_a_link_is_stored_under_the_configured_root(
    native_library, silence, tmp_path
):
    """The row is spelled as the native landing spells its targets, under the
    root as configured, so it matches the rows the collection holds whichever
    way the person reached the file."""
    cfg, _root = native_library
    path = _single(cfg, silence)
    alias = tmp_path / "alias"
    alias.symlink_to(cfg.library.root, target_is_directory=True)
    through = alias / path.relative_to(cfg.library.root)
    assert through.is_file() and str(through) != str(path)

    code, acted, _ = _two_acts(_file(through))

    assert code == int(ExitCode.OK), acted
    ((_content_id, _title, folder_path),) = _rows(cfg)
    assert folder_path == str(Path(cfg.library.root) / cfg.library.music_dir / "Single.flac")
    # And a second run finds the row it made, where the unresolved spelling
    # planned a second one.
    code, refused = drive(_file(through))
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 0 and shown["already present"] == 1


def test_the_target_is_spelled_under_the_root_as_configured_not_as_resolved(
    native_library, silence, tmp_path
):
    """A library configured through a link. The file is named by its real path
    and the row is planned under the link, which is how the landing spells a
    target and how the collection's rows are matched."""
    from dataclasses import replace

    cfg, _root = native_library
    path = _single(cfg, silence)
    alias = tmp_path / "alias"
    alias.symlink_to(cfg.library.root, target_is_directory=True)
    linked = replace(cfg, library=replace(cfg.library, root=alias))
    assert file_cli._in_the_library(path, linked) == alias / cfg.library.music_dir / "Single.flac"


def test_the_engine_refuses_a_target_it_cannot_resolve_instead_of_planning_an_add(
    native_library, silence, tmp_path
):
    """Unasked is not absent. The matcher never looked for a row for a path it
    could not put under the root, and the plan used to read that as no row."""
    cfg, _root = native_library
    outside = tmp_path / "elsewhere.flac"
    shutil.copyfile(silence, outside)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        with pytest.raises(CratekitError) as raised:
            native.plan_rows(
                cfg,
                db,
                tree_id=INTAKE,
                registry=tree_registry.read(cfg),
                batch="probe",
                files=[(outside, outside)],
            )
    finally:
        rb_writer.close_db(db)
    cause = raised.value.cause
    assert cause.reason == "intake-list-unusable"
    assert str(outside) in cause.message and "no row was planned" in cause.message


def test_a_binding_failure_past_the_gate_says_what_it_leaves(
    native_library, silence, tmp_path, monkeypatch
):
    cfg, _root = native_library
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


def test_a_refusal_past_the_gate_keeps_its_reason_and_remedy(
    native_library, silence, monkeypatch
):
    """The engine's own skew refusal, whose remedy is not its reason's default,
    so a wrapper that dropped the remedy would answer with another one."""
    cfg, root_id = native_library
    path = _single(cfg, silence)

    def skewed(*args, **kwargs):
        raise tree_registry.RegistrySkew(
            "the adopted intake root could not be read back", tree_id=INTAKE, root_id=root_id
        )

    monkeypatch.setattr(native, "apply_rows", skewed)
    code, acted, _ = _two_acts(_file(path))

    cause = acted["cause"]
    assert cause["reason"] == "tree-unconverged"
    assert cause["remediation"]["remedy"] == "restore-from-snapshot"
    assert "the adopted intake root could not be read back" in cause["message"]
    assert "no row was added" in cause["message"]
    assert cause["detail"]["tree_id"] == INTAKE and cause["detail"]["source"] == str(path)


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
    # The bridge names the batch playlist after its intake file, as it did.
    assert b'<NODE Name="Single_inboxed" Type="1"' in written
    assert b"Single.flac" in written
    # The export itself is read and never written, and the database is not touched.
    assert export.read_bytes() == before
    assert _rows(cfg) == []
    assert _playlists(cfg, path.stem) == []
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


@pytest.fixture(params=(BRIDGE, NATIVE))
def both(request, bridge_library) -> config.Config:
    """The acknowledged machine on each medium in turn."""
    if request.param == NATIVE:
        _cut_over_intake(bridge_library)
    return bridge_library


def test_a_file_that_is_not_there_refuses_from_the_vocabulary_on_either_medium(both, tmp_path):
    """The conformance sample held the verb to this until it needed a file that
    exists, so it is held here, on both media."""
    cfg = both
    code, envelope = drive(_file(_music(cfg) / "no-such-track.flac"))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "is not a file on this machine" in envelope["cause"]["message"]
    _assert_nothing_written(cfg, tmp_path)


def test_a_file_that_is_not_audio_refuses_on_either_medium(both, tmp_path):
    cfg = both
    notes = _music(cfg) / "notes.txt"
    notes.write_text("not audio\n", encoding="utf-8")
    code, envelope = drive(_file(notes))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "not an audio file" in envelope["cause"]["message"]
    _assert_nothing_written(cfg, tmp_path)


def test_a_registry_nobody_can_read_refuses_the_plan_with_its_own_cause(
    bridge_library, silence, tmp_path
):
    """The medium is read before the plan is shown, on the bridge too. A
    registry that cannot be read is not read as "on the bridge": the verb
    cannot say whether there is a gate to ask, so it says why."""
    cfg = bridge_library
    path = _single(cfg, silence)
    registry_file = tree_registry.path_for(cfg)
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    registry_file.write_text("{ not json", encoding="utf-8")

    code, envelope = drive(_file(path))

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "tree-registry-unusable"
    assert _rows(cfg) == [] and _xml_anywhere(cfg, tmp_path) == []


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


def test_a_bridge_apply_on_a_native_tree_moves_nothing_and_keeps_the_splices_cause(
    native_library, silence, export
):
    """A cutover recorded between the verb's read and the engine's. The engine
    reads the registry again before its first move (R-677), and what it finds
    is refused there, unwrapped, with the file still in staging."""
    cfg, _root = native_library
    staged = Path(cfg.paths.download_staging) / "One.flac"
    shutil.copyfile(silence, staged)
    assert tags.write_tags(staged, {"title": "One", "artist": "Probe", "genre": "Deep House"})
    planned = landing.plan(Path(cfg.paths.download_staging), cfg, "2026-09-30_batch")
    destination = land_cli.intake_file(cfg, "2026-09-30_batch")

    with pytest.raises(CratekitError) as raised:
        landing.apply(planned, cfg=cfg, export=export, destination=destination)

    _assert_names_the_landing_and_no_defect(raised.value.cause)
    assert staged.exists() and not destination.exists()
    assert not (Path(cfg.library.root) / cfg.library.music_dir / "2026-09-30_batch").exists()


def test_the_splice_still_takes_a_bridge_tree(bridge_library, silence, export, tmp_path):
    cfg = bridge_library
    path = _single(cfg, silence)
    destination = tmp_path / "direct_inboxed.xml"
    (placed,) = ingest.place_files([path], cfg=cfg, export=export, destination=destination)
    assert placed.path == path and destination.is_file()


def test_every_caller_of_the_intake_emitter_builds_its_tree_through_the_refusal():
    """The emitter guard says ``report-defect``. A writer that reaches it with
    a tree the refusal never saw tells a person who chose a cutover to file a
    bug, which is the finding. The callers are named, so a third one is a line
    somebody reads in a diff."""
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
                == "bridge_intake_tree"
            ]
            key = f"{module.relative_to(SRC).as_posix()}::{function.name}"
            callers[key] = (min(emits), asked)

    assert set(callers) == {"intake/ingest.py::place_files", "intake/landing.py::_check_export"}
    for key, (first_emit, asked) in callers.items():
        assert asked and min(asked) < first_emit, (
            f"{key} reaches the intake emitter without building its tree through "
            f"the function that refuses a native one first"
        )


def test_the_intake_tree_is_built_in_one_place_and_that_place_refuses_first():
    """The write layer names no verb, so the refusal that names the landing
    lives one layer up, in the one function that builds the tree a splice is
    handed. A second builder is a second way past it."""
    builders: list[str] = []
    for module in sorted(SRC.rglob("*.py")):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(function):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "intake_tree"
                ):
                    builders.append(f"{module.relative_to(SRC).as_posix()}::{function.name}")
    assert builders == ["intake/ingest.py::bridge_intake_tree"]

    (function,) = [
        node
        for node in ast.walk(ast.parse(Path(ingest.__file__).read_text(encoding="utf-8")))
        if isinstance(node, ast.FunctionDef) and node.name == "bridge_intake_tree"
    ]
    first, second = [
        node
        for node in function.body
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant))
    ]
    assert isinstance(first, ast.Expr) and first.value.func.id == "assert_intake_on_the_bridge"
    assert isinstance(second, ast.Return)


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
    module, and both verbs that write the intake tree call the function there.
    So does the set playlist's backfill (U121), which writes no intake node
    and asks the same switch only to refuse a bridge tree by name."""
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
