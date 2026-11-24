"""``crate export collection`` and every verb that reads what it writes (R-745).

Read back by a real parser, the strict reader and each verb taking an export, never its writer (D1).
"""

from __future__ import annotations

import argparse
import importlib
import re
import shutil
import sqlite3
import xml.etree.ElementTree as ET
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from pyrekordbox.db6 import tables
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from cratekit import __version__
from cratekit.cli import export_collection, registry
from cratekit.core import (
    config,
    jobs,
    locations,
    preflight,
    rb_writer,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import collection_xml
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound import source as outbound_source
from cratekit.modules.reports import export as library_export
from cratekit.sync import cli as sync_cli
from cratekit.write import collection_export, metadata_cli, rbxml
from tests import cutover_fixtures, outbound_fakes
from tests._containers import synth_container
from tests._readings import serve_readings
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data
from tests.test_no_beatgrid_ever import FORBIDDEN_TOKENS, GRIDLESS_AVERAGE_BPM
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row
from tests.xml_fixtures import _fresh_xml

DECLARED = taxonomy.default_taxonomy()
INTAKE = DECLARED.intake.display
TREE = DECLARED.tree.display
WRITTEN = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)

#: The tempo every seeded row stores, in hundredths, that no spelling of can appear by accident.
STORED_TEMPO = 98765
TEMPO_SPELLINGS = ("98765", "987.65", "987")

#: The rows the fixture builder seeds, with no path and no tempo, in every count below.
BASELINE = ("1", "2")

#: A title and a file name carrying the three characters the brief names.
AWKWARD_TITLE = 'Salt & "Pepper" Café'
AWKWARD_FILE = 'Salt & "Pepper" Café.flac'

#: identifier, file name, title, stars, tombstone
TRACKS = (
    ("11", "Low Track.flac", "Low Track", 0, False),
    ("12", "Mid Track.flac", "Mid Track", 3, False),
    ("13", "Top Track.flac", "Top Track", 5, False),
    ("31", AWKWARD_FILE, AWKWARD_TITLE, 4, False),
    ("41", "Gone Track.flac", "Gone Track", 2, True),
)
LIVE = ("1", "2", "11", "12", "13", "31")
#: The batch playlist's keys in stored order, the tombstone left out.
BATCH_KEYS = ("11", "12", "13")

#: What the routing rules read off each intake file, served by file name.
READINGS = {
    "Low Track.flac": ("Deep House", 2),
    "Mid Track.flac": ("Deep House", 5),
    "Top Track.flac": ("Tech House", 8),
}

BATCH = "2026-09-18 batch"
CRATE = "Night Crate"

#: Every playlist the export must carry, by path under the root, with its keys in stored order.
EXPECTED_PLAYLISTS = {
    (INTAKE, BATCH): BATCH_KEYS,
    (TREE, "Deep House", "Low"): (),
    (TREE, "Deep House", "Med"): (),
    (TREE, "Deep House", "High"): (),
    (TREE, "Tech House", "Low"): (),
    (TREE, "Tech House", "Med"): (),
    (TREE, "Tech House", "High"): (),
    ("Crates", "Late", CRATE): ("13", "31", "11"),
    ("Crates", "Late", "Empty Crate"): (),
    (outbound_fakes.FAVORITES,): ("12", "13"),
}
EXPECTED_FOLDERS = {
    (INTAKE,): 1,
    (TREE,): 2,
    (TREE, "Deep House"): 3,
    (TREE, "Tech House"): 3,
    ("Crates",): 2,
    ("Crates", "Late"): 2,
    ("Crates", "Hollow"): 0,
}
ROOT_CHILDREN = (INTAKE, TREE, "Crates", outbound_fakes.FAVORITES)

#: The drive a moved library was made on, which rekordbox keeps recording and nothing mounts (R-773).
BASE_DRIVE = "former-drive"

#: The two ways a library's rows are recorded: where mounted, or under the base drive.
UNDER_THE_ROOT = "recorded-under-the-root"
UNDER_A_BASE_DRIVE = "recorded-under-a-base-drive"


def _exited(result: tuple[int, dict], expected: ExitCode = ExitCode.OK) -> dict:
    """The envelope of a drive that exited ``expected``, OK unless told otherwise."""
    code, envelope = result
    assert code == int(expected), envelope
    return envelope


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the cutover suite patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer, "read_rekordbox_settings", lambda *_a, **_k: {rb_writer.LIBRARY_SYNC_SETTING: 0}
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real = rb_writer.integrity_ok
    monkeypatch.setattr(rb_writer, "integrity_ok", lambda target, **_: real(target, unlock=False))
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(export_collection, "_now", lambda: WRITTEN)


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _forget_libraries():
    outbound_source.forget_libraries()
    yield
    outbound_source.forget_libraries()


def _machine(tmp_path, monkeypatch, *, moved: bool = False, rule: bool = True) -> config.Config:
    """A set-up machine on every module with the seeded library; ``moved`` and ``rule`` as setup."""
    root, staging = tmp_path / "library", tmp_path / "staging"
    for folder in (root / "db", root / "Music", staging):
        folder.mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    pin = {"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"}
    data = valid_data(root, profile={"name": "full"}, rekordbox=pin)
    data["paths"] = {"download_staging": str(staging)}
    if moved and rule:
        rule = {"from": str(tmp_path / BASE_DRIVE), "to": "{library.root}"}
        data["library"]["location_prefix_map"] = [rule]
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    _seed(resolved, moved=moved)
    session.record_acknowledgment(resolved, terminal=lambda: True)
    return resolved


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A library whose rows record the paths it is mounted under."""
    return _machine(tmp_path, monkeypatch)


@pytest.fixture
def moved(tmp_path, monkeypatch) -> config.Config:
    """A library recorded under a base drive, with the one rule recorded."""
    return _machine(tmp_path, monkeypatch, moved=True)


@pytest.fixture
def unruled(tmp_path, monkeypatch) -> config.Config:
    """The same library with no rule recorded, which is sitting 19's export."""
    return _machine(tmp_path, monkeypatch, moved=True, rule=False)


@pytest.fixture(params=(UNDER_THE_ROOT, UNDER_A_BASE_DRIVE))
def either(request, tmp_path, monkeypatch) -> config.Config:
    """Both layouts in turn, for a claim that has to hold on each."""
    return _machine(tmp_path, monkeypatch, moved=request.param == UNDER_A_BASE_DRIVE)


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / "Music"


def _base(cfg: config.Config) -> Path:
    return Path(cfg.library.root).parent / BASE_DRIVE


def _under_base(cfg: config.Config, path: Path) -> Path:
    """``path`` as a moved library's database records it, under the base drive."""
    return _base(cfg) / Path(path).relative_to(cfg.library.root)


def _sql(cfg: config.Config, statement: str, params=()) -> list[tuple]:
    """One statement straight to the library file, committed, with no binding."""
    with closing(sqlite3.connect(cfg.library.db_path)) as conn:
        rows = conn.execute(statement, params).fetchall()
        conn.commit()
    return rows


def _is_moved(cfg: config.Config) -> bool:
    """Whether the drive row names a base drive; a moved library with no rule is still moved."""
    return bool(_sql(cfg, "SELECT BaseDBDrive FROM djmdProperty")[0][0])


def _as_recorded(cfg: config.Config, path: Path) -> Path:
    """``path`` as this library's database records it, whichever layout it is."""
    return _under_base(cfg, path) if _is_moved(cfg) else Path(path)


def _content(cfg: config.Config, rows) -> None:
    """Add collection rows the way rekordbox records them: a plain path, stars."""
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        if db_session.get(tables.DjmdArtist, "900") is None:
            db_session.add(_row(tables.DjmdArtist, ID="900", Name="Probe & Co"))
        for identifier, _filename, title, stars, deleted, path in rows:
            db_session.add(_row(
                tables.DjmdContent, ID=identifier, Title=title, ArtistID="900",
                FolderPath=str(path), BPM=STORED_TEMPO, Rating=stars, Length=300, FileType=5,
                StockDate="2026-09-18", rb_local_deleted=1 if deleted else 0,
            ))
        db_session.commit()
    engine.dispose()


#: Each worker's seeded database per layout and pin, with its seed folder (U256).
_SEEDED: dict[tuple[bool, str], tuple[str, bytes]] = {}


def _seed(cfg: config.Config, *, moved: bool = False) -> None:
    """Five rows, four trees, one of everything odd; the files are always under the mounted root."""
    music = _music(cfg)
    for _identifier, filename, *_rest in TRACKS:
        (music / filename).write_bytes(b"")
    database = Path(cfg.library.db_path)
    here = str(Path(cfg.library.root).parent)
    key = (moved, rb_writer.pinned_db_version(cfg))
    if key in _SEEDED:
        seeded_under, image = _SEEDED[key]
        database.write_bytes(image)
        moved_to = (seeded_under, here)
        _sql(cfg, "UPDATE djmdContent SET FolderPath = replace(FolderPath, ?, ?)", moved_to)
        _sql(cfg, "UPDATE djmdProperty SET BaseDBDrive = replace(BaseDBDrive, ?, ?), "
             "CurrentDBDrive = replace(CurrentDBDrive, ?, ?)", moved_to * 2)
        return
    _seed_from_nothing(cfg, moved=moved)
    if not any(Path(f"{database}{suffix}").exists() for suffix in ("-wal", "-shm", "-journal")):
        _SEEDED[key] = (here, database.read_bytes())


def _seed_from_nothing(cfg: config.Config, *, moved: bool) -> None:
    _build_disposable_database(Path(cfg.library.db_path), with_tag_category=False)
    music = _music(cfg)
    recorded = _under_base(cfg, music) if moved else music
    _content(cfg, [(*track, recorded / track[1]) for track in TRACKS])
    if moved:  # rekordbox's record of the rename, which setup offers the rule from.
        _sql(cfg, "UPDATE djmdProperty SET BaseDBDrive = ?, CurrentDBDrive = ?",
             (f"{_base(cfg)}/", f"{cfg.library.root}/"))
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        def folder(name, parent=None):
            return handle.create_playlist_folder(name, parent=parent)

        def playlist(name, parent=None, keys=()):
            made = handle.create_playlist(name, parent=parent)
            for key in keys:
                handle.add_to_playlist(made, handle.get_content(ID=key))
            return made

        inbox = folder(INTAKE)
        # THE TOMBSTONE IS A MEMBER, and the export must leave its key out.
        playlist(BATCH, inbox, ("11", "12", "41", "13"))
        tree = folder(TREE)
        for genre in ("Deep House", "Tech House"):
            bucket = folder(genre, tree)
            for sub in ("Low", "Med", "High"):
                playlist(sub, bucket)
        crates = folder("Crates")
        late = folder("Late", crates)
        playlist(CRATE, late, ("13", "31", "11"))
        playlist("Empty Crate", late)
        folder("Hollow", crates)
        playlist(outbound_fakes.FAVORITES, None, ("12", "13"))

        removed = playlist("Removed Crate", None, ("11",))
        removed.rb_local_deleted = 1
        smart = playlist("Smart Crate", None)
        smart.Attribute = tables.PlaylistType.SMART_PLAYLIST.value
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)


def _drive_collection(cfg: config.Config, name: str) -> tuple[Path, dict]:
    destination = Path(cfg.library.root) / "exports" / name
    envelope = _exited(drive(["export", "collection", str(destination)]))
    return destination, envelope


def _export(cfg: config.Config, name: str = "collection.xml") -> Path:
    """Write one export under the library's own folder and answer its path."""
    destination, envelope = _drive_collection(cfg, name)
    assert envelope["data"]["summary"]["export"] == str(destination)
    return destination


def _parsed(path: Path) -> ET.Element:
    """The document through a real parser, which is what rekordbox is."""
    return ET.fromstring(path.read_bytes())


def _walk(node: ET.Element, path: tuple[str, ...] = ()):
    """Every node under ``node`` with the path that reaches it, by a real parser."""
    for child in node.findall("NODE"):
        here = (*path, child.get("Name"))
        yield here, child
        yield from _walk(child, here)


def _tree(path: Path) -> dict[tuple[str, ...], ET.Element]:
    root = _parsed(path).find("PLAYLISTS").find("NODE")
    return dict(_walk(root))


def _tracks(document: bytes) -> dict[str, ET.Element]:
    """Each collection row by its identifier, by a real parser."""
    return {
        track.get("TrackID"): track
        for track in ET.fromstring(document).find("COLLECTION").findall("TRACK")
    }


def _summarised(envelope: dict, **expected) -> None:
    """Each named count of the envelope's summary, as expected."""
    summary = envelope["data"]["summary"]
    assert {key: summary[key] for key in expected} == expected


def _approved(verb: list[str], gate: str, answer: str) -> tuple[int, dict]:
    """Drive a gated verb to its gate, answer it as a person, and drive it again."""
    refused = _exited(drive(verb), ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["gate"] == gate
    decided, envelope = drive(["run", "decide", refused["run_id"], gate, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    return drive(["--run", refused["run_id"], *verb])


def _land(export: Path, batch: str) -> dict:
    """Land the staged files as ``batch`` against ``export``, left waiting on the import."""
    code, landed = drive(
        ["-d", "intake.land.confirm=apply", "intake", "land", "--export", str(export),
         "--name", batch]
    )  # fmt: skip
    assert code == int(ExitCode.PENDING_HUMAN), landed
    return landed


def test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted(machine):
    exported = _export(machine)
    nodes = _tree(exported)
    playlists = {
        path: tuple(track.get("Key") for track in node.findall("TRACK"))
        for path, node in nodes.items()
        if node.get("Type") == "1"
    }
    folders = {path: node for path, node in nodes.items() if node.get("Type") == "0"}
    assert playlists == EXPECTED_PLAYLISTS
    assert set(folders) == set(EXPECTED_FOLDERS)
    assert playlists[("Crates", "Late", "Empty Crate")] == ()
    assert "41" not in playlists[(INTAKE, BATCH)], "a tombstone's key was written"
    assert not [path for path in nodes if path[-1] in ("Removed Crate", "Smart Crate")]
    root = _parsed(exported).find("PLAYLISTS").find("NODE")
    assert tuple(child.get("Name") for child in root.findall("NODE")) == ROOT_CHILDREN
    collection = _parsed(exported).find("COLLECTION")
    assert tuple(track.get("TrackID") for track in collection.findall("TRACK")) == LIVE


def test_every_declared_count_equals_what_was_written(machine):
    exported = _export(machine)
    document = _parsed(exported)
    collection = document.find("COLLECTION")
    assert int(collection.get("Entries")) == len(collection.findall("TRACK")) == len(LIVE)

    root = document.find("PLAYLISTS").find("NODE")
    assert int(root.get("Count")) == len(root.findall("NODE")) == len(ROOT_CHILDREN)
    for path, node in _tree(exported).items():
        if node.get("Type") == "1":
            assert int(node.get("Entries")) == len(node.findall("TRACK")), path
            assert int(node.get("Entries")) == len(EXPECTED_PLAYLISTS[path]), path
        else:
            assert int(node.get("Count")) == len(node.findall("NODE")), path
            assert int(node.get("Count")) == EXPECTED_FOLDERS[path], path


def test_the_strict_reader_takes_the_file_and_sees_the_same_library(machine):
    exported = _export(machine)
    view = library_export.read_export_file(exported)
    assert tuple(entry.track_id for entry in view.entries) == LIVE
    assert {item.path: item.track_ids for item in view.playlists} == EXPECTED_PLAYLISTS
    by_id = {entry.track_id: entry for entry in view.entries}
    assert by_id["31"].playlists == (("Crates", "Late", CRATE),)


def test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out(machine):
    """And says that no tempo data was written."""
    destination, envelope = _drive_collection(machine, "counted.xml")
    # The two rows the fixture builder seeds record no path at all.
    _summarised(
        envelope, tracks=len(LIVE), folders=len(EXPECTED_FOLDERS),
        playlists=len(EXPECTED_PLAYLISTS), bytes=destination.stat().st_size,
        memberships=sum(len(keys) for keys in EXPECTED_PLAYLISTS.values()),
        smart_playlists_omitted=1, memberships_omitted=1, tracks_without_a_file=len(BASELINE),
        rows_normalised=0,
    )
    warned = {warning["code"]: warning["message"] for warning in envelope["warnings"]}
    assert set(warned) == {
        "export-smart-playlist-omitted",
        "export-member-not-in-collection",
        "export-location-not-a-file",
    }
    assert "'Smart Crate'" in warned["export-smart-playlist-omitted"]
    assert "'1', '2'" in warned["export-location-not-a-file"]
    (tempo,) = [c for c in envelope["data"]["checks"] if c["key"] == "export.tempo"]
    assert "no tempo data was written" in tempo["detail"]


def test_every_line_ends_in_a_carriage_return_and_a_line_feed(machine):
    content = _export(machine).read_bytes()
    assert b"\n" in content
    assert content.replace(b"\r\n", b"").find(b"\n") == -1
    assert content.replace(b"\r\n", b"").find(b"\r") == -1


def test_a_folder_with_nothing_in_it_has_a_body_a_landing_could_insert_into(machine):
    """rekordbox self closes one. The readers insert ahead of a closing line."""
    content = _export(machine).read_bytes()
    root = rbxml.root_node(content)
    crates = rbxml.direct_child(content, root, "Crates", rbxml.FOLDER_TYPE)
    hollow = rbxml.direct_child(content, crates, "Hollow", rbxml.FOLDER_TYPE)
    assert not hollow.self_closing
    assert content[hollow.close_start :].startswith(b"</NODE>\r\n")


#: Every attribute a collection row of an export carries, in the fixtures' order.
REKORDBOX_TRACK_ATTRIBUTES = (
    "TrackID", "Name", "Artist", "Composer", "Album", "Grouping", "Genre", "Kind",
    "Size", "TotalTime", "DiscNumber", "TrackNumber", "Year", "AverageBpm",
    "DateAdded", "BitRate", "SampleRate", "Comments", "PlayCount", "Rating",
    "Location", "Remixer", "Tonality", "Label", "Mix",
)  # fmt: skip


def test_a_row_carries_the_attributes_the_intake_emitter_writes_in_its_order(machine):
    """The intake emitter's rows import. A row here is held to the same names."""
    content = _export(machine).read_bytes()
    ours = rbxml.find_collection_track(content, "12")
    spelled = tuple(
        key.decode() for key, _value in rbxml._ATTR_PAIR.findall(content[ours.tag_start : ours.tag_end])
    )
    assert spelled == REKORDBOX_TRACK_ATTRIBUTES

    row = {"name": "n", "artist": "a", "location": "/library/n.flac"}
    theirs = collection_xml.build_track_xml(1, row, "2026-09-18", declared=DECLARED).encode()
    assert spelled == tuple(key.decode() for key, _value in rbxml._ATTR_PAIR.findall(theirs))


def test_a_row_says_what_the_database_row_says(machine):
    track = _tracks(_export(machine).read_bytes())["12"]
    assert track.get("Name") == "Mid Track"
    assert track.get("Artist") == "Probe & Co"
    assert track.get("Kind") == "FLAC File"
    assert track.get("TotalTime") == "300"
    assert track.get("DateAdded") == "2026-09-18"
    assert track.get("Rating") == "153"
    assert track.get("Location") == locations.location_url(_music(machine) / "Mid Track.flac")


def test_each_star_count_is_spelled_as_the_export_byte(machine):
    rows = {key: track.get("Rating") for key, track in _tracks(_export(machine).read_bytes()).items()}
    assert rows == {"1": "0", "2": "0", "11": "0", "12": "153", "13": "255", "31": "204"}


def test_a_rating_on_neither_scale_is_written_unrated_and_said_so(machine):
    _content(machine, [("51", "Odd.flac", "Odd", 7, False, _music(machine) / "Odd.flac")])
    destination, envelope = _drive_collection(machine, "odd.xml")
    assert _tracks(destination.read_bytes())["51"].get("Rating") == "0"
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "export-rating-unreadable"]
    assert "'51'" in warning["message"]


def test_an_ampersand_a_quote_and_an_accent_survive_the_readers(machine):
    exported = _export(machine)
    content = exported.read_bytes()
    assert _tracks(content)["31"].get("Name") == AWKWARD_TITLE
    span = rbxml.find_collection_track(content, "31")
    read = rbxml.attributes(content, span)
    assert rbxml.xml_unescape_attr(read["Name"]) == AWKWARD_TITLE
    decoded = locations.location_to_path(rbxml.xml_unescape_attr(read["Location"]))
    assert Path(decoded) == _music(machine) / AWKWARD_FILE
    view = library_export.read_export_file(exported)
    entry = {item.track_id: item for item in view.entries}["31"]
    assert entry.name == AWKWARD_TITLE
    assert entry.artist == "Probe & Co"


def test_no_tempo_the_database_holds_reaches_the_file(either):
    """Every seeded row stores a tempo; the file carries the gridless constant on both layouts."""
    machine = either
    stored = {row: bpm for row, bpm in _sql(machine, "SELECT ID, BPM FROM djmdContent") if bpm}
    assert set(stored) >= {"11", "12", "13", "31"}, "no row stores a tempo to leak"
    assert set(stored.values()) == {STORED_TEMPO}
    exported = _export(machine)
    content = exported.read_bytes().decode("utf-8")
    tracks = _parsed(exported).find("COLLECTION").findall("TRACK")
    assert len(tracks) == len(LIVE)
    for track in tracks:
        assert track.get("AverageBpm") == GRIDLESS_AVERAGE_BPM, track.get("TrackID")
        assert list(track) == [], "a collection row has a child element"
        for name, value in track.attrib.items():
            if name == "Location":
                continue
            for spelling in TEMPO_SPELLINGS:
                assert spelling not in value, (track.get("TrackID"), name, value)
    for token in FORBIDDEN_TOKENS:
        assert token not in content, token
    assert content.count("AverageBpm=") == len(LIVE)
    assert content.count(f'AverageBpm="{GRIDLESS_AVERAGE_BPM}"') == len(LIVE)


def test_the_file_says_cratekit_wrote_it_and_what_it_knows_of_the_database(machine):
    content = _export(machine).read_bytes()
    assert collection_export.provenance_of(content) == {
        "writer": f"cratekit {__version__}",
        "written": "2026-09-29T12:00:00Z",
        "database-schema": rb_writer.pinned_db_version(machine),
        "application-installed": RECORDED_APP_VERSION,
        "application-pinned": RECORDED_APP_VERSION,
    }
    # A parser takes the comment, and the document element is still the root.
    assert _parsed(Path(machine.library.root) / "exports" / "collection.xml").tag == "DJ_PLAYLISTS"


def test_an_export_rekordbox_wrote_says_nothing_of_the_kind():
    assert collection_export.provenance_of(_fresh_xml()) is None


def test_a_version_nobody_could_read_is_written_as_unknown(machine, monkeypatch):
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: None)
    found = collection_export.provenance_of(_export(machine).read_bytes())
    assert found["application-installed"] == "unknown"
    assert found["application-pinned"] == RECORDED_APP_VERSION


def test_a_provenance_value_cannot_close_the_comment_it_sits_in():
    line = collection_export.provenance_line(
        collection_export.Provenance(writer='x --> <NODE Name="y">', written="now")
    )
    assert line.count("-->") == 1
    assert "<NODE" not in line
    assert '"y"' not in line


@pytest.mark.parametrize("probe", ["rekordbox_running", "rekordbox_agent_running"])
def test_rekordbox_or_its_agent_running_is_refused_and_nothing_is_written(
    machine, monkeypatch, probe
):
    """Under one slug, and with no folder of the destination's made."""
    monkeypatch.setattr(rb_writer, probe, lambda: True)
    destination = Path(machine.library.root) / "new" / "deeper" / "out.xml"
    code, envelope = drive(["export", "collection", str(destination)])
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "rekordbox-running"
    assert not destination.exists()
    assert not (Path(machine.library.root) / "new").exists()


def test_a_file_that_appears_after_the_check_is_refused_by_the_write(machine, tmp_path):
    """The exclusive create is the guard. The check ahead of it is a courtesy."""
    destination = tmp_path / "raced.xml"
    destination.write_bytes(b"arrived first")
    with pytest.raises(CratekitError) as caught:
        export_collection._write_new(destination, b"the export")
    assert caught.value.cause.reason == "output-exists"
    assert destination.read_bytes() == b"arrived first"


def test_a_file_that_came_and_went_is_still_refused_as_taken(tmp_path, monkeypatch):
    """A sync client does this. The refusal is decided by the create, not a second look."""
    destination = tmp_path / "flicker.xml"
    real_open = open

    def taken_then_gone(path, mode="r", *args, **kwargs):
        if Path(path) == destination and "x" in mode:
            raise FileExistsError(17, "File exists", str(path))
        return real_open(path, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", taken_then_gone)
    with pytest.raises(CratekitError) as caught:
        export_collection._write_new(destination, b"the export")
    assert caught.value.cause.reason == "output-exists"
    assert not destination.exists()


def test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made(tmp_path, monkeypatch):
    kept = tmp_path / "kept"
    kept.mkdir()
    destination = kept / "made" / "deeper" / "torn.xml"

    def fail(_descriptor):
        raise OSError("the volume went away")

    monkeypatch.setattr(export_collection.os, "fsync", fail)
    with pytest.raises(OSError):
        export_collection._write_new(destination, b"the export")
    assert not destination.exists()
    assert not (kept / "made").exists()
    assert kept.is_dir()


def _copies(monkeypatch) -> list[Path]:
    """Every database the verb copies from here on, so a test can see there were none."""
    taken: list[Path] = []
    real_copy = rb_writer.disposable_copy

    def watched(source):
        taken.append(Path(source))
        return real_copy(source)

    monkeypatch.setattr(rb_writer, "disposable_copy", watched)
    return taken


def test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied(machine, monkeypatch):
    blocked = Path(machine.library.root) / "not-a-folder"
    blocked.write_bytes(b"a file")
    taken = _copies(monkeypatch)
    envelope = _exited(drive(["export", "collection", str(blocked / "deep" / "out.xml")]), ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert envelope["cause"]["detail"]["blocked"] == str(blocked.resolve())
    # The true reason; "cannot be written into" would send a person to its permissions.
    assert "is not a folder" in envelope["cause"]["message"]
    assert taken == []
    assert blocked.read_bytes() == b"a file"


def test_an_existing_file_is_refused_before_the_database_is_copied(machine, monkeypatch):
    """And left as it was. The exclusive create would refuse it too, after the read."""
    destination = Path(machine.library.root) / "kept.xml"
    destination.write_bytes(b"somebody kept this")
    taken = _copies(monkeypatch)
    envelope = _exited(drive(["export", "collection", str(destination)]), ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "output-exists"
    assert destination.read_bytes() == b"somebody kept this"
    assert taken == []


def test_a_folder_nobody_may_write_to_is_refused_before_the_database_is_copied(
    machine, monkeypatch
):
    locked = Path(machine.library.root) / "locked"
    locked.mkdir()
    locked.chmod(0o500)
    taken = _copies(monkeypatch)
    try:
        code, envelope = drive(["export", "collection", str(locked / "out.xml")])
    finally:
        locked.chmod(0o700)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert taken == []
    assert list(locked.iterdir()) == []


@pytest.mark.parametrize("suffix", tree_registry.PENDING_XML_SUFFIXES)
def test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused(machine, suffix):
    destination = Path(machine.library.root) / f"2026-09-29{suffix}"
    envelope = _exited(drive(["export", "collection", str(destination)]), ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "library-export-unusable"
    assert not destination.exists()
    assert tree_registry.pending_intake_xml(machine) == ()


def test_an_identifier_that_is_not_digits_is_refused_and_nothing_is_written(machine):
    _content(machine, [("r-one", "R.flac", "R", 0, False, _music(machine) / "R.flac")])
    destination = Path(machine.library.root) / "exports" / "refused.xml"
    envelope = _exited(drive(["export", "collection", str(destination)]), ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "library-export-unusable"
    assert envelope["cause"]["detail"]["identifier"] == "r-one"
    assert not destination.exists()


def test_the_configured_database_is_never_opened_and_is_left_byte_for_byte(machine, monkeypatch):
    """The copy is what is opened. The configured path is only ever copied from."""
    database = Path(machine.library.db_path)
    before = database.read_bytes()
    opened: list[Path] = []
    real_open = rb_writer.open_db

    def watched(target, **kwargs):
        opened.append(Path(target).resolve())
        return real_open(target, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", watched)
    _export(machine)
    assert opened, "nothing was opened, so nothing was read"
    assert database.resolve() not in opened
    assert database.read_bytes() == before


def test_the_verb_declares_one_xml_no_database_surface_and_asks_nothing():
    entry = registry.entry("export.collection")
    assert entry.writes == frozenset({"xml"})
    assert not entry.destructive
    assert entry.gates == ()
    assert entry.module_id is None, "a core workflow cannot wait on a module"
    assert "rekordbox.closed" in entry.doctor_checks
    # The check that says how many rows no rule places (R-773).
    assert "library.paths_resolved" in entry.doctor_checks


def test_the_population_of_verbs_that_take_an_export_is_the_one_driven_here():
    """Derived off the shipped parsers, so a new verb taking one fails here."""
    taking: set[str] = set()
    for entry in registry.ENTRIES:
        if not entry.landed:
            continue
        parser = argparse.ArgumentParser()
        getattr(importlib.import_module(entry.module), entry.builder)(parser, entry)
        if any("--export" in action.option_strings for action in parser._actions):
            taking.add(entry.name)
    assert taking == DRIVEN


#: The verbs the tests below drive, each named by the test that drives it.
DRIVEN = {
    "intake.land", "intake.imported", "intake.file", "tree.cutover", "route.inbox",
    "route.unplaced", "export.playlist", "export.prune", "sync.favorites", "sync.all",
}


@pytest.fixture
def silence(tmp_path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return synth_container(scratch, ".flac")


def _stage(cfg: config.Config, silence: Path, name: str, folder: Path | None = None) -> Path:
    path = (folder or Path(cfg.paths.download_staging)) / name
    shutil.copyfile(silence, path)
    fields = {"title": Path(name).stem, "artist": "Probe", "genre": "Deep House", "energylevel": 7}
    assert tags.write_tags(path, fields)
    return path


def _imported(cfg: config.Config, paths) -> None:
    """Rows for ``paths`` as rekordbox's import records them, from identifier 9000 up."""
    _content(cfg, [
        (str(9000 + i), p.name, p.stem, 0, False, _as_recorded(cfg, p.resolve())) for i, p in paths
    ])


def _spliced(artifact: str, added: int) -> ET.Element:
    """The intake file a landing wrote, its collection the export's rows and ``added`` more."""
    spliced = ET.fromstring(Path(artifact).read_bytes())
    collection = spliced.find("COLLECTION")
    assert int(collection.get("Entries")) == len(collection.findall("TRACK")) == len(LIVE) + added
    return spliced


def test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second(either, silence):
    """The import is proved off a second export, moved library too, with no edit between (R-773)."""
    machine = either
    cutover_fixtures.verified_snapshot(machine)
    first = _export(machine, "before-landing.xml")
    for name in ("One.flac", "Two.flac"):
        _stage(machine, silence, name)
    batch = "2026-09-29_landed"
    landed = _land(first, batch)
    intake_file = Path(landed["pending_human_action"]["artifact"])
    spliced = _spliced(landed["pending_human_action"]["artifact"], 2)
    nodes = dict(_walk(spliced.find("PLAYLISTS").find("NODE")))
    # The batch playlist carries the batch's name, not the file's (U110).
    assert len(nodes[(INTAKE, batch)].findall("TRACK")) == 2
    # What the export already held is still there, in the same order.
    assert tuple(t.get("Key") for t in nodes[(INTAKE, BATCH)].findall("TRACK")) == BATCH_KEYS
    assert collection_export.provenance_of(intake_file.read_bytes()) is not None
    landed_in = Path(machine.library.root) / machine.library.music_dir / batch
    _imported(machine, enumerate(sorted(landed_in.glob("*.flac"))))
    second = _export(machine, "after-import.xml")
    before = second.read_bytes()
    proved = _exited(drive(["intake", "imported", "--export", str(second)]))
    (item,) = proved["data"]["items"]
    assert item["action"] == "imported"
    assert item["count"] == 2
    assert not intake_file.exists()
    assert second.read_bytes() == before, "the export was edited between the two verbs"
    tree_registry.assert_cutover_ready(machine, export=second)


def test_the_import_proof_is_withheld_against_an_export_taken_before_the_import(machine, silence):
    """The other direction. A file this verb wrote is not proof by being one."""
    first = _export(machine, "before-landing.xml")
    _stage(machine, silence, "One.flac")
    landed = _land(first, "2026-09-29_unproved")
    stale = _export(machine, "still-before-import.xml")
    _exited(drive(["intake", "imported", "--export", str(stale)]), ExitCode.PENDING_HUMAN)
    assert Path(landed["pending_human_action"]["artifact"]).exists()


def test_a_single_file_intake_splices_into_the_file(either, silence):
    machine = either
    exported = _export(machine)
    path = _stage(machine, silence, "Single.flac", _music(machine))
    envelope = _exited(drive(["intake", "file", str(path), "--export", str(exported)]), ExitCode.PENDING_HUMAN)
    _spliced(envelope["pending_human_action"]["artifact"], 1)


def test_a_cutover_takes_the_file_as_its_fresh_export(either):
    """The precheck asks only that the export is a file holding something, which this one is."""
    machine = either
    cutover_fixtures.verified_snapshot(machine)
    exported = _export(machine)
    results = tree_registry.cutover_precheck(machine, export=exported)
    assert {result.check: result.passed for result in results}["fresh-export"] is True
    assert all(result.passed for result in results), [r.cause for r in results if r.cause]

    verb = ["tree", "cutover", DECLARED.tree.id, "--export", str(exported)]
    code, recorded = _approved(verb, "tree.cutover.approve", "approve")
    assert code == int(ExitCode.OK), recorded
    assert recorded["data"]["totals"]["recorded"] is True
    record = tree_registry.read(machine).record(DECLARED.tree.id)
    assert record is not None and record.mode == tree_registry.Mode.DATABASE


@pytest.fixture
def tagged(monkeypatch):
    """The routing rules' tag readings, served by file name at the tag reader (U250)."""
    def read(index: int):
        return lambda path: READINGS.get(path.name, (None, None))[index]
    serve_readings(monkeypatch, genre=read(0), energy=read(1), vox=lambda path: None)


def _sub_keys(document: bytes, folder: str, sub: str) -> tuple[str, ...]:
    nodes = dict(_walk(ET.fromstring(document).find("PLAYLISTS").find("NODE")))
    return tuple(track.get("Key") for track in nodes[(TREE, folder, sub)].findall("TRACK"))


def test_the_inbox_routing_reads_the_file_and_routes_its_intake(either, tagged):
    exported = _export(either)
    envelope = _exited(drive(["-d", "route.inbox.apply=apply", "route", "inbox", "--export", str(exported)]))
    assert envelope["data"]["totals"]["inserted"] == 3
    written = Path(envelope["data"]["totals"]["output"]).read_bytes()
    assert _sub_keys(written, "Deep House", "Low") == ("11",)
    assert _sub_keys(written, "Deep House", "Med") == ("12",)
    assert _sub_keys(written, "Tech House", "High") == ("13",)
    assert written != exported.read_bytes()


def test_the_unplaced_sweep_reads_the_file_and_places_what_no_sub_holds(either, tagged):
    exported = _export(either)
    envelope = _exited(drive(["route", "unplaced", "--export", str(exported)]))
    placed = {item["track_id"]: item["destination"] for item in envelope["data"]["items"]}
    assert placed["11"] == "Deep House/Low"
    assert placed["12"] == "Deep House/Med"
    assert placed["13"] == "Tech House/High"
    written = Path(envelope["data"]["totals"]["output"]).read_bytes()
    assert _sub_keys(written, "Tech House", "High") == ("13",)


def _bind(monkeypatch, account) -> None:
    monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(account))


@pytest.mark.parametrize(
    ("verb", "gate", "queued"),
    [
        (["export", "playlist", CRATE], "export.playlist.confirm", ["13", "31", "11"]),
        (["sync", "favorites"], "sync.favorites.confirm", ["12", "13"]),
    ],
    ids=["playlist-export", "favourites-sweep"],
)
def test_a_queueing_verb_reads_the_file_and_queues_its_tracks(
    either, monkeypatch, verb, gate, queued
):
    exported = _export(either)
    _bind(monkeypatch, outbound_fakes.FakeAccount(catalog={}))
    _run, job_id = approve_and_queue([*verb, "--export", str(exported)], gate)

    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == queued


def test_a_playlist_prune_reads_the_file_and_takes_off_only_what_left_it(either, monkeypatch):
    """R-836: the recorded track no row in the file matches any more is the one taken off."""
    machine = either
    exported = _export(machine)
    account = outbound_fakes.FakeAccount(catalog={"13": "tid-13", "31": "tid-31", "11": "tid-11"})
    _bind(monkeypatch, account)
    key = outbound_source.resolve(outbound_source.read_library(exported), CRATE).key
    remote = ledger.reserve_playlist(machine, key, lambda: account.create_playlist(CRATE)).remote_id
    for one in ("tid-13", "tid-31", "tid-11", "tid-gone"):
        account.add_to_playlist(remote, one)
        ledger.record_playlist_track(machine, key, one)
    verb = ["export", "prune", CRATE, "--export", str(exported)]
    code, done = _approved(verb, "export.prune.confirm", "apply")
    assert code == int(ExitCode.OK), done
    assert account.playlist_tracks(remote) == ("tid-13", "tid-31", "tid-11")
    assert account.taken == [(remote, ("tid-gone",))]


def test_the_composed_sync_reads_the_file_and_queues_the_favourites(either, monkeypatch):
    exported = _export(either)
    _bind(monkeypatch, outbound_fakes.FakeAccount(catalog={}))
    _exited(_approved(["sync", "all", "--export", str(exported)], sync_cli.CONFIRM, "sync"))
    with jobs.open_store() as store:
        favourites = [job for job in jobs.list_jobs(store) if job.handler_key == "sync.favorites"]
        (job,) = favourites
        assert [item.item_id for item in jobs.items(store, job.job_id)] == ["12", "13"]


NOBODY = collection_export.Provenance(writer="cratekit test", written="2026-09-29T12:00:00Z")
_Track = collection_export.TrackRow
_Node = collection_export.NodeRow


def _rendered(tracks, nodes=(), *, root="/library", prefix_map=()) -> collection_export.Document:
    return collection_export.render(tuple(tracks), tuple(nodes), NOBODY, root=root, prefix_map=tuple(prefix_map))


def _rows(document: collection_export.Document) -> dict[str, str]:
    return {key: track.get("Location") for key, track in _tracks(document.content).items()}


def _at(*rows: tuple[str, str]) -> list:
    """A track row per ``(identifier, location)``."""
    return [_Track(track_id=key, location=location) for key, location in rows]


def test_an_identifier_is_spelled_one_way_in_the_collection_and_in_a_playlist():
    """A leading zero. The row and the key naming it have to be the same string."""
    held = [_Node("1", "root", "Held", 0, 1, ("007",))]
    document = _rendered(_at(("007", "/library/a.flac")), held)
    view = library_export.read_export(document.content)
    assert tuple(entry.track_id for entry in view.entries) == ("007",)
    assert {item.path: item.track_ids for item in view.playlists} == {("Held",): ("007",)}
    assert document.omitted.dangling_members == 0


def test_two_identifiers_that_are_one_number_are_two_rows_the_reader_takes():
    document = _rendered(
        _at(("7", "/library/a.flac"), ("007", "/library/b.flac")),
        [_Node("1", "root", "Held", 0, 1, ("007", "7"))],
    )
    view = library_export.read_export(document.content)
    assert sorted(entry.track_id for entry in view.entries) == ["007", "7"]
    assert view.playlists[0].track_ids == ("007", "7")


@pytest.mark.parametrize(
    "rows",
    [_at(("7", "/library/a.flac"), ("7", "/library/b.flac")), _at(('7" Evil="1', "/a.flac"))],
    ids=["held-twice", "handed-straight-to-the-emitter-not-digits"],
)
def test_an_identifier_the_readers_would_lose_is_refused_by_the_emitter(rows):
    with pytest.raises(CratekitError) as caught:
        _rendered(rows)
    assert caught.value.cause.reason == "library-export-unusable"


@pytest.mark.parametrize("bad", ["\x01", "\x00", "\x1f", "\t", "\n", "\r", "\ufffe"])
def test_a_character_no_document_may_carry_is_written_as_a_space_and_counted(bad):
    document = _rendered(
        [_Track(track_id="7", name=f"Left{bad}Right", comments="plain", location="/library/a.flac")],
        [_Node("1", "root", f"Crate{bad}Name", 0, 1, ("7",))],
    )
    parsed = ET.fromstring(document.content)
    (track,) = parsed.find("COLLECTION").findall("TRACK")
    assert track.get("Name") == "Left Right"
    assert track.get("Comments") == "plain"
    (node,) = parsed.find("PLAYLISTS").find("NODE").findall("NODE")
    assert node.get("Name") == "Crate Name"
    assert document.omitted.normalised_text == ("7", "Crate Name")
    assert document.content.replace(b"\r\n", b"").find(b"\n") == -1


def test_a_row_with_nothing_to_clean_is_not_counted_as_cleaned():
    document = _rendered([_Track(track_id="7", name=AWKWARD_TITLE, location="/library/a.flac")])
    assert document.omitted.normalised_text == ()


def test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine():
    spellings = (
        ("7", "tidal:tracks:123", "tidal:tracks:123"),
        ("8", "", ""),
        ("9", "/library/Music/a b.flac", "file://localhost/library/Music/a%20b.flac"),
        ("10", "file://localhost/library/Music/c%20d.flac",
         "file://localhost/library/Music/c%20d.flac"),
    )
    document = _rendered(_at(*((key, held) for key, held, _written in spellings)))
    assert _rows(document) == {key: written for key, _held, written in spellings}
    assert document.omitted.not_file_paths == ("7", "8")


def _node(identifier: str, attribute) -> SimpleNamespace:
    """A playlist row as the binding hands one over, with whatever kind it holds."""
    return SimpleNamespace(ID=identifier, ParentID="root", Name=f"Node {identifier}",
                           Attribute=attribute, Seq=int(identifier), rb_local_deleted=0)


def _handle(rows, songs=()) -> SimpleNamespace:
    """A handle serving ``rows`` as its playlists and ``songs`` as their memberships."""
    return SimpleNamespace(get_playlist=lambda: list(rows), get_playlist_songs=lambda: list(songs))


@pytest.mark.parametrize("unreadable", [None, "folder", "", True, 2.5j])
def test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist(unreadable):
    nodes = collection_export.read_nodes(_handle([_node("1", unreadable), _node("2", 0)]))
    document = _rendered([], nodes)
    root = ET.fromstring(document.content).find("PLAYLISTS").find("NODE")
    written = [node.get("Name") for node in root.findall("NODE")]
    assert written == ["Node 2"]
    assert document.omitted.unreadable_kinds == ("Node 1",)
    assert document.playlists == 1


def test_the_lookup_tables_are_read_once_each_and_not_once_per_row(machine):
    """Forty rows, forty artists. The statements must not grow with the rows."""
    engine = create_engine(f"sqlite:///{machine.library.db_path}")
    with Session(engine) as db_session:
        for index in range(40):
            db_session.add(_row(tables.DjmdArtist, ID=str(5000 + index), Name=f"Artist {index}"))
            db_session.add(_row(
                tables.DjmdContent, ID=str(6000 + index), Title=f"Title {index}",
                ArtistID=str(5000 + index), FolderPath=str(_music(machine) / f"{index}.flac"),
                rb_local_deleted=0,
            ))
        db_session.commit()
    engine.dispose()
    handle = rb_writer.open_db(
        rb_writer.live_db_path(machine), require_closed=False, check_app_version=False, cfg=machine
    )
    statements: list[str] = []
    try:
        bound = handle.session.get_bind()
        event.listen(bound, "before_cursor_execute", lambda *args: statements.append(args[2]))
        tracks, _unrated = collection_export.read_tracks(handle)
    finally:
        rb_writer.close_db(handle)
    named = {track.track_id: track.artist for track in tracks}
    assert named["6000"] == "Artist 0" and named["6039"] == "Artist 39"
    assert named["12"] == "Probe & Co"
    assert len(statements) <= 1 + len(collection_export.LOOKUPS), statements


def test_the_day_added_falls_back_to_the_day_on_this_machines_clock():
    class Row:
        StockDate = ""
        created_at = datetime(2026, 9, 29, 1, 0, tzinfo=timezone.utc)

    here = Row.created_at.astimezone().date().isoformat()
    assert collection_export._date_added(Row) == here

    class Evening(Row):
        created_at = datetime(2026, 9, 29, 1, 0, tzinfo=timezone(timedelta(hours=-4)))

    assert collection_export._date_added(Evening) == Evening.created_at.astimezone().date().isoformat()

    class Stocked(Row):
        StockDate = "2026-09-18"

    assert collection_export._date_added(Stocked) == "2026-09-18"


def test_a_comment_inside_the_document_does_not_answer_for_the_file():
    """Only the line ahead of the document element says who wrote the file."""
    line = collection_export.provenance_line(NOBODY).encode("utf-8")
    theirs = _fresh_xml()
    at = theirs.index(b"  <PRODUCT")
    assert collection_export.provenance_of(theirs[:at] + line + theirs[at:]) is None
    ahead = theirs.index(b"<DJ_PLAYLISTS")
    assert collection_export.provenance_of(theirs[:ahead] + line + theirs[ahead:]) == {
        "writer": "cratekit test",
        "written": "2026-09-29T12:00:00Z",
        "database-schema": "unknown",
        "application-installed": "unknown",
        "application-pinned": "unknown",
    }


def _song(identifier: str, playlist: str, content: str, order: int) -> SimpleNamespace:
    return SimpleNamespace(ID=identifier, PlaylistID=playlist, ContentID=content, TrackNo=order,
                           rb_local_deleted=0)


def test_members_come_out_in_their_stored_order_whatever_order_the_rows_arrive_in():
    songs = [_song("c", "1", "30", 3), _song("a", "1", "10", 1), _song("b", "1", "20", 2)]
    (node,) = collection_export.read_nodes(_handle([_node("1", 0)], songs))
    assert node.members == ("10", "20", "30")


def test_siblings_come_out_in_their_sequence_and_not_in_identifier_order():
    nodes = [_Node("1", "root", "Third", 0, 3), _Node("2", "root", "First", 0, 1),
             _Node("3", "root", "Second", 1, 2)]
    root = ET.fromstring(_rendered([], nodes).content).find("PLAYLISTS").find("NODE")
    assert [node.get("Name") for node in root.findall("NODE")] == ["First", "Second", "Third"]

def test_a_membership_somebody_removed_is_not_written_back_into_the_playlist():
    """The zero row E2 bought this. The track is live. Its place in the list is not."""
    removed = _song("b", "1", "20", 2)
    removed.rb_local_deleted = 1
    songs = [_song("a", "1", "10", 1), removed, _song("c", "1", "30", 3)]
    (node,) = collection_export.read_nodes(_handle([_node("1", 0)], songs))
    assert node.members == ("10", "30")
    tracks = _at(*((key, f"/library/{key}.flac") for key in ("10", "20", "30")))
    document = _rendered(tracks, [node])
    view = library_export.read_export(document.content)
    assert view.playlists[0].track_ids == ("10", "30")
    assert document.omitted.dangling_members == 0


def test_a_membership_that_cannot_say_whether_it_was_removed_refuses():
    unreadable = _song("a", "1", "10", 1)
    unreadable.rb_local_deleted = None
    with pytest.raises(CratekitError) as caught:
        collection_export.read_nodes(_handle([_node("1", 0)], [unreadable]))
    assert caught.value.cause.reason == "soft-delete-marker-unreadable"


#: The seeded file names as the one encoder spells them, written out by hand.
ENCODED = {
    "11": "Low%20Track.flac",
    "12": "Mid%20Track.flac",
    "13": "Top%20Track.flac",
    "31": "Salt%20%26%20%22Pepper%22%20Caf%c3%a9.flac",
}

_PLAIN = re.compile(r"[A-Za-z0-9/_.-]+")


def _locations(path: Path) -> dict[str, str]:
    """Each collection row's location, by a real parser."""
    return {key: track.get("Location") for key, track in _tracks(path.read_bytes()).items()}


def _encoded_under(prefix: str) -> dict[str, str]:
    """Every row's written location, the seeded files' under ``prefix``, the baseline's empty."""
    under = {key: f"file://localhost{prefix}/Music/{name}" for key, name in ENCODED.items()}
    return {"1": "", "2": "", **under}


def _location_check(envelope: dict) -> dict:
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == "export.locations"]
    return check


def test_the_moved_fixture_is_a_library_whose_base_drive_is_not_its_mounted_root(moved):
    """The fixture, held to the shape the finding was measured on."""
    base, root = str(_base(moved)), str(moved.library.root)
    assert _PLAIN.fullmatch(root), "the literals below assume a root the encoder leaves alone"
    assert not Path(base).exists(), "the base drive is a name nothing mounts"
    held = "SELECT ID, FolderPath FROM djmdContent WHERE ID IN ('11', '12', '13', '31')"
    recorded = dict(_sql(moved, held))
    assert set(recorded) == {"11", "12", "13", "31"}
    assert all(path.startswith(base + "/Music/") for path in recorded.values()), recorded
    (drives,) = _sql(moved, "SELECT BaseDBDrive, CurrentDBDrive FROM djmdProperty")
    assert drives == (base + "/", root + "/")
    assert moved.resolved_prefix_map() == ((base, root),)


def test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it(moved):
    exported, envelope = _drive_collection(moved, "mounted.xml")
    assert _locations(exported) == _encoded_under(str(moved.library.root))
    assert BASE_DRIVE.encode() not in exported.read_bytes()
    _summarised(envelope, locations_remapped=4, tracks_under_no_rule=0)
    assert "export-location-unmapped" not in {w["code"] for w in envelope["warnings"]}
    check = _location_check(envelope)
    assert check["status"] == "ok"
    assert check["detail"].startswith("4 location(s) written where")


def test_a_library_recorded_where_it_is_mounted_has_nothing_to_place(machine):
    exported, envelope = _drive_collection(machine, "in-place.xml")
    root = str(machine.library.root)
    assert _locations(exported)["12"] == f"file://localhost{root}/Music/Mid%20Track.flac"
    _summarised(envelope, locations_remapped=0, tracks_under_no_rule=0)


def test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted(unruled):
    """Never dropped and never guessed. The root is not swapped in on a hunch."""
    base = str(_base(unruled))
    exported, envelope = _drive_collection(unruled, "as-held.xml")
    assert _locations(exported) == _encoded_under(base)
    # The two baseline rows hold no path, and are not the prefix map's to place.
    _summarised(envelope, tracks=len(LIVE), tracks_under_no_rule=4, locations_remapped=0,
                tracks_without_a_file=len(BASELINE))
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "export-location-unmapped"]
    assert warning["message"].startswith("4 track(s) record a path under neither")
    assert "'11', '12', '13', '31'" in warning["message"]
    assert "library.paths_resolved" in warning["message"]
    # The prefix the rows record, two components deep, spelled from the path.
    leading = "/" + "/".join(Path(base).parts[1:3])
    assert f"rule (4 under {leading})" in warning["message"]
    check = _location_check(envelope)
    assert check["status"] == "info"
    assert "4 under no rule" in check["detail"]


def test_the_export_and_doctor_count_the_same_rows_as_under_no_rule(unruled):
    """Two surfaces, one survey; a row under the mounted root stops both counting every row."""
    _content(unruled, [("61", "Here.flac", "Here", 0, False, _music(unruled) / "Here.flac")])
    (_music(unruled) / "Here.flac").write_bytes(b"")
    with rb_writer.read_only_copy(rb_writer.live_db_path(unruled), cfg=unruled) as db:
        totals = metadata_cli.resolution_totals(unruled, db)
    _exported, envelope = _drive_collection(unruled, "surveyed.xml")
    assert totals.unmapped == 4
    assert envelope["data"]["summary"]["tracks_under_no_rule"] == 4


def test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule(unruled, silence):
    """Sitting 19: no rule joins the landed file and the imported row, so the run stays waiting."""
    machine = unruled
    first = _export(machine, "before-landing.xml")
    _stage(machine, silence, "One.flac")
    batch = "2026-09-30_unjoined"
    landed = _land(first, batch)
    _imported(machine, enumerate(sorted((_music(machine) / batch).glob("*.flac"))))
    second, envelope = _drive_collection(machine, "after-import.xml")
    assert envelope["data"]["summary"]["tracks_under_no_rule"] == 5
    _exited(drive(["intake", "imported", "--export", str(second)]), ExitCode.PENDING_HUMAN)
    assert Path(landed["pending_human_action"]["artifact"]).exists()


RULE = (locations.PrefixRule("/former", "/library"),)


def test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver():
    """One row per way a row can resolve, with the written value spelled out."""
    spellings = (
        ("1", "/former/Music/a b.flac", "file://localhost/library/Music/a%20b.flac"),
        ("2", "file://localhost/former/Music/c%20d.flac",
         "file://localhost/library/Music/c%20d.flac"),
        # Decomposed on the way in, composed and lowercase on the way out.
        ("3", "/former/Music/Café.flac", "file://localhost/library/Music/Caf%c3%a9.flac"),
        # A different folder that shares the rule's spelling, so no rule places it.
        ("4", "/formerly/Music/e.flac", "file://localhost/formerly/Music/e.flac"),
        ("5", "/library/Music/f.flac", "file://localhost/library/Music/f.flac"),
        ("6", "tidal:tracks:123", "tidal:tracks:123"),
        ("7", "file://elsewhere/former/Music/g.flac", "file://elsewhere/former/Music/g.flac"),
        ("8", "", ""),
        # Two more under no rule and one prefix, so the most rows are not met first.
        ("9", "/elsewhere/Music/h.flac", "file://localhost/elsewhere/Music/h.flac"),
        ("10", "/elsewhere/Music/i.flac", "file://localhost/elsewhere/Music/i.flac"),
    )
    document = _rendered(_at(*((key, held) for key, held, _written in spellings)), prefix_map=RULE)
    assert _rows(document) == {key: written for key, _held, written in spellings}
    assert document.remapped == 3
    assert document.omitted.unmapped_paths == ("4", "9", "10")
    assert document.omitted.unmapped_prefixes == (("/elsewhere/Music", 2), ("/formerly/Music", 1))
    assert document.omitted.left_to_rule == ()
    assert document.omitted.not_file_paths == ("6", "8")


def test_the_rules_are_walked_in_the_order_they_were_recorded():
    """First match wins, so a rule that is another's prefix has to come first."""
    rules = (locations.PrefixRule("/former/Music", "/library/Deep"),
             locations.PrefixRule("/former", "/library"))
    tracks = _at(("1", "/former/Music/a.flac"), ("2", "/former/Sets/b.flac"))
    document = _rendered(tracks, prefix_map=rules)
    assert _rows(document) == {
        "1": "file://localhost/library/Deep/a.flac", "2": "file://localhost/library/Sets/b.flac",
    }
    assert document.remapped == 2


def _read_back(location: str, *, root: str, prefix_map) -> str | None:
    """Where a verb taking the file resolves one written location, by the resolver."""
    return locations.resolve_recorded_path(
        locations.location_to_path(location), root=root, prefix_map=prefix_map
    ).path


def test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it():
    """Rewritten, the row would resolve under no rule; as recorded, the readers resolve it."""
    onto_second = (locations.PrefixRule("/former", "/second"),)
    document = _rendered(_at(("1", "/former/Music/a.flac")), prefix_map=onto_second)
    written = _rows(document)["1"]
    assert written == "file://localhost/former/Music/a.flac"
    assert _read_back(written, root="/library", prefix_map=onto_second) == "/second/Music/a.flac"
    # What the rewritten spelling would have read back as, which is the reason.
    assert _read_back("file://localhost/second/Music/a.flac", root="/library", prefix_map=onto_second) is None
    assert document.remapped == 0
    assert document.omitted.left_to_rule == ("1",)
    assert document.omitted.unmapped_paths == ()


@pytest.mark.parametrize(
    ("rules", "written", "read_back", "remapped", "left"),
    [
        # The identity rule is how a folder outside the root is declared readable.
        (
            (("/former", "/second"), ("/second", "/second")),
            "/second/Music/a.flac", "/second/Music/a.flac", 1, (),
        ),
        # Written at the first target, the row would read back at the second.
        (
            (("/former", "/middle"), ("/middle", "/library")),
            "/former/Music/a.flac", "/middle/Music/a.flac", 0, ("1",),
        ),
        # A target that is not a path is left to its rule, not under no rule, as doctor counts it.
        ((("/former", "Music"),), "/former/Music/a.flac", "Music/Music/a.flac", 0, ("1",)),
    ],
    ids=["onto-itself", "moved-again", "target-not-a-path"],
)  # fmt: skip
def test_a_rule_places_a_row_only_where_it_reads_back_as_itself(
    rules, written, read_back, remapped, left
):
    prefix_map = tuple(locations.PrefixRule(source, target) for source, target in rules)
    document = _rendered(_at(("1", "/former/Music/a.flac")), prefix_map=prefix_map)
    assert _rows(document) == {"1": f"file://localhost{written}"}
    assert _read_back(f"file://localhost{written}", root="/library", prefix_map=prefix_map) == read_back
    assert document.remapped == remapped
    assert document.omitted.left_to_rule == left
    assert document.omitted.unmapped_paths == ()


def test_the_envelope_counts_a_row_left_to_its_rule(tmp_path, monkeypatch):
    """The three counts through the shipped verb, on a rule onto a second volume."""
    cfg = _machine(tmp_path, monkeypatch, moved=True, rule=False)
    document = dict(cfg.to_toml_dict())
    rule = {"from": str(_base(cfg)), "to": str(tmp_path / "second-volume")}
    document["library"]["location_prefix_map"] = [rule]
    config.save(config.from_dict(document))
    config.reset_cache()
    exported, envelope = _drive_collection(cfg, "second-volume.xml")
    assert _locations(exported)["12"] == f"file://localhost{_base(cfg)}/Music/Mid%20Track.flac"
    _summarised(envelope, locations_left_to_a_rule=4, locations_remapped=0, tracks_under_no_rule=0)
    assert "export-location-unmapped" not in {w["code"] for w in envelope["warnings"]}
    check = _location_check(envelope)
    assert check["status"] == "ok"
    assert "4 left to a rule" in check["detail"]


@pytest.mark.parametrize(
    ("prefixes", "listed"),
    [
        ((("/a/b", 3),), "rule (3 under /a/b), and"),
        ((("/a/b", 3), ("/c/d", 2), ("/e/f", 1)),
         "rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and"),
        ((("/a/b", 3), ("/c/d", 2), ("/e/f", 1), ("/g/h", 1)),
         "rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and"),
        ((("/a/b", 3), ("/c/d", 2), ("/e/f", 1), ("/g/h", 1), ("/i/j", 1)),
         "rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and"),
    ],
)
def test_the_warning_names_three_prefixes_and_counts_the_rest(prefixes, listed):
    """A drive that has gone dark is a line here, where a count would hide it."""
    rows = tuple(str(index) for index in range(sum(count for _prefix, count in prefixes)))
    omitted = collection_export.Omitted(unmapped_paths=rows, unmapped_prefixes=prefixes)
    (warning,) = export_collection._warnings(omitted)
    assert warning["code"] == "export-location-unmapped"
    assert warning["message"].startswith(f"{len(rows)} track(s) record a path")
    assert listed in warning["message"]


def test_the_emitter_cannot_be_asked_for_a_document_without_saying_where_it_is_mounted():
    """No default for either argument, since a default is sitting 19's export."""
    for given in ({}, {"root": "/library"}, {"prefix_map": ()}):
        with pytest.raises(TypeError):
            collection_export.render((), (), NOBODY, **given)
