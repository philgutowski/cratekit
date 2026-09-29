"""R-745: ``crate export collection``, and every verb that reads what it writes.

WHAT THIS FILE IS FOR. The verb's claim is that the file it writes is one the
other verbs take, so the file is never judged by the module that wrote it. It is
read back three ways: by a real XML parser, which is what rekordbox is; by the
strict reader the reports and the outbound verbs share; and by each verb that
takes an export, driven through the shipped command line.

THE DATABASE IS SEEDED BY HAND AND THE EXPECTATIONS ARE SPELLED OUT. Every
expected path, count and order below is written as a literal beside the rows
that produce it, so no assertion is the emitter asked twice.

THE REPOSITORY HOLDS NO REKORDBOX EXPORT OF A REAL LIBRARY, so the comparison
the brief asks for is against the byte fixtures the splice suites already use,
which were cut from one, and against what each reader requires. The comparison
with an export taken the same minute is the attended verification.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit import __version__
from cratekit.cli import export_collection, registry
from cratekit.core import (
    config,
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
from cratekit.modules.outbound import source as outbound_source
from cratekit.modules.reports import export as library_export
from cratekit.write import collection_export, rbxml
from tests import cutover_fixtures, outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data
from tests.test_no_beatgrid_ever import FORBIDDEN_TOKENS, GRIDLESS_AVERAGE_BPM
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row
from tests.xml_fixtures import _fresh_xml

DECLARED = taxonomy.default_taxonomy()
INTAKE = DECLARED.intake.display
TREE = DECLARED.tree.display
WRITTEN = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)

#: The tempo every seeded row stores, in the database's hundredths. Chosen so
#: that neither spelling of it can appear in the file by accident.
STORED_TEMPO = 98765
TEMPO_SPELLINGS = ("98765", "987.65", "987")

#: The rows the fixture builder seeds before anything here is added. They carry
#: no path and no tempo. Named, since every count below includes them.
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

#: What the routing rules read off each intake file, served by file name.
READINGS = {
    "Low Track.flac": ("Deep House", 2),
    "Mid Track.flac": ("Deep House", 5),
    "Top Track.flac": ("Tech House", 8),
}

BATCH = "2026-09-18 batch"
CRATE = "Night Crate"

#: Every playlist the export must carry, as its path under the root and the
#: keys it holds in stored order. Spelled out, never derived.
EXPECTED_PLAYLISTS = {
    (INTAKE, BATCH): ("11", "12", "13"),
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


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


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


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set-up machine, every module on, whose database holds the seeded library."""
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    staging = tmp_path / "staging"
    staging.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(
        root,
        profile={"name": "full"},
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    data["paths"] = {"download_staging": str(staging)}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    _seed(resolved)
    session.record_acknowledgment(resolved, terminal=lambda: True)
    return resolved


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / "Music"


def _content(cfg: config.Config, rows) -> None:
    """Add collection rows the way rekordbox records them: a plain path, stars."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        if db_session.get(tables.DjmdArtist, "900") is None:
            db_session.add(_row(tables.DjmdArtist, ID="900", Name="Probe & Co"))
        for identifier, filename, title, stars, deleted, path in rows:
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=identifier,
                    Title=title,
                    ArtistID="900",
                    FolderPath=str(path),
                    BPM=STORED_TEMPO,
                    Rating=stars,
                    Length=300,
                    FileType=5,
                    StockDate="2026-09-18",
                    rb_local_deleted=1 if deleted else 0,
                )
            )
        db_session.commit()
    engine.dispose()


def _seed(cfg: config.Config) -> None:
    """The library every test reads: five rows, four trees, one of everything odd."""
    from pyrekordbox.db6 import tables

    _build_disposable_database(Path(cfg.library.db_path), with_tag_category=False)
    music = _music(cfg)
    for _identifier, filename, *_rest in TRACKS:
        (music / filename).write_bytes(b"")
    _content(
        cfg,
        [
            (identifier, filename, title, stars, deleted, music / filename)
            for identifier, filename, title, stars, deleted in TRACKS
        ],
    )

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


def _export(cfg: config.Config, name: str = "collection.xml") -> Path:
    """Write one export under the library's own folder and answer its path."""
    destination = Path(cfg.library.root) / "exports" / name
    code, envelope = drive(["export", "collection", str(destination)])
    assert code == int(ExitCode.OK), envelope
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


# ═══════════════════════════════════════════════════════════════════════════
# 1. The shape, read by a parser and by the strict reader
# ═══════════════════════════════════════════════════════════════════════════


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
    nodes = _tree(exported)
    for path, node in nodes.items():
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
    destination = Path(machine.library.root) / "exports" / "counted.xml"
    code, envelope = drive(["export", "collection", str(destination)])

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["tracks"] == len(LIVE)
    assert summary["folders"] == len(EXPECTED_FOLDERS)
    assert summary["playlists"] == len(EXPECTED_PLAYLISTS)
    assert summary["memberships"] == sum(len(keys) for keys in EXPECTED_PLAYLISTS.values())
    assert summary["bytes"] == destination.stat().st_size
    assert summary["smart_playlists_omitted"] == 1
    assert summary["memberships_omitted"] == 1
    warned = {warning["code"]: warning["message"] for warning in envelope["warnings"]}
    assert set(warned) == {
        "export-smart-playlist-omitted",
        "export-member-not-in-collection",
        "export-location-not-a-file",
    }
    assert "'Smart Crate'" in warned["export-smart-playlist-omitted"]
    # The two rows the fixture builder seeds record no path at all.
    assert summary["tracks_without_a_file"] == len(BASELINE)
    assert "'1', '2'" in warned["export-location-not-a-file"]
    assert summary["rows_normalised"] == 0


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


# ═══════════════════════════════════════════════════════════════════════════
# 2. Field by field, against what the readers require
# ═══════════════════════════════════════════════════════════════════════════

#: Every attribute a collection row of a rekordbox export carries, as the byte
#: fixtures cut from one spell them, in order.
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

    theirs = collection_xml.build_track_xml(
        1,
        {"name": "n", "artist": "a", "location": "/library/n.flac"},
        "2026-09-18",
        declared=DECLARED,
    ).encode()
    assert spelled == tuple(key.decode() for key, _value in rbxml._ATTR_PAIR.findall(theirs))


def test_a_row_says_what_the_database_row_says(machine):
    track = {
        element.get("TrackID"): element
        for element in _parsed(_export(machine)).find("COLLECTION").findall("TRACK")
    }["12"]

    assert track.get("Name") == "Mid Track"
    assert track.get("Artist") == "Probe & Co"
    assert track.get("Kind") == "FLAC File"
    assert track.get("TotalTime") == "300"
    assert track.get("DateAdded") == "2026-09-18"
    assert track.get("Rating") == "153"
    assert track.get("Location") == locations.location_url(_music(machine) / "Mid Track.flac")


def test_each_star_count_is_spelled_as_the_export_byte(machine):
    rows = {
        element.get("TrackID"): element.get("Rating")
        for element in _parsed(_export(machine)).find("COLLECTION").findall("TRACK")
    }
    assert rows == {"1": "0", "2": "0", "11": "0", "12": "153", "13": "255", "31": "204"}


def test_a_rating_on_neither_scale_is_written_unrated_and_said_so(machine):
    _content(machine, [("51", "Odd.flac", "Odd", 7, False, _music(machine) / "Odd.flac")])
    destination = Path(machine.library.root) / "exports" / "odd.xml"
    code, envelope = drive(["export", "collection", str(destination)])

    assert code == int(ExitCode.OK), envelope
    rows = {
        element.get("TrackID"): element.get("Rating")
        for element in _parsed(destination).find("COLLECTION").findall("TRACK")
    }
    assert rows["51"] == "0"
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "export-rating-unreadable"]
    assert "'51'" in warning["message"]


def test_an_ampersand_a_quote_and_an_accent_survive_the_readers(machine):
    exported = _export(machine)
    content = exported.read_bytes()

    parsed = {
        element.get("TrackID"): element
        for element in _parsed(exported).find("COLLECTION").findall("TRACK")
    }["31"]
    assert parsed.get("Name") == AWKWARD_TITLE

    span = rbxml.find_collection_track(content, "31")
    read = rbxml.attributes(content, span)
    assert rbxml.xml_unescape_attr(read["Name"]) == AWKWARD_TITLE
    decoded = locations.location_to_path(rbxml.xml_unescape_attr(read["Location"]))
    assert Path(decoded) == _music(machine) / AWKWARD_FILE

    view = library_export.read_export_file(exported)
    entry = {item.track_id: item for item in view.entries}["31"]
    assert entry.name == AWKWARD_TITLE
    assert entry.artist == "Probe & Co"


# ═══════════════════════════════════════════════════════════════════════════
# 3. No beat grid, and no tempo the database held
# ═══════════════════════════════════════════════════════════════════════════


def test_no_tempo_the_database_holds_reaches_the_file(machine):
    """Every seeded row stores a tempo. The file carries the gridless constant."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{machine.library.db_path}")
    with Session(engine) as db_session:
        stored = {
            row.ID: row.BPM for row in db_session.query(tables.DjmdContent).all() if row.BPM
        }
    engine.dispose()
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


def test_the_envelope_says_no_tempo_was_written(machine):
    code, envelope = drive(
        ["export", "collection", str(Path(machine.library.root) / "exports" / "said.xml")]
    )
    assert code == int(ExitCode.OK), envelope
    (tempo,) = [c for c in envelope["data"]["checks"] if c["key"] == "export.tempo"]
    assert "no tempo data was written" in tempo["detail"]


# ═══════════════════════════════════════════════════════════════════════════
# 4. Who wrote it
# ═══════════════════════════════════════════════════════════════════════════


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


# ═══════════════════════════════════════════════════════════════════════════
# 5. The refusals
# ═══════════════════════════════════════════════════════════════════════════


def test_rekordbox_running_is_refused_and_nothing_is_written(machine, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    destination = Path(machine.library.root) / "exports" / "refused.xml"

    code, envelope = drive(["export", "collection", str(destination)])

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "rekordbox-running"
    assert not destination.exists()
    assert not destination.parent.exists()


def test_the_agent_running_is_refused_under_the_same_slug(machine, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    destination = Path(machine.library.root) / "exports" / "refused.xml"

    code, envelope = drive(["export", "collection", str(destination)])

    assert envelope["cause"]["reason"] == "rekordbox-running"
    assert code != int(ExitCode.OK)
    assert not destination.exists()


def test_an_existing_file_is_refused_and_left_as_it_was(machine):
    destination = Path(machine.library.root) / "kept.xml"
    destination.write_bytes(b"somebody kept this")

    code, envelope = drive(["export", "collection", str(destination)])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "output-exists"
    assert destination.read_bytes() == b"somebody kept this"


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


def test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made(
    tmp_path, monkeypatch
):
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


def test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied(
    machine, monkeypatch
):
    blocked = Path(machine.library.root) / "not-a-folder"
    blocked.write_bytes(b"a file")
    taken = _copies(monkeypatch)

    code, envelope = drive(["export", "collection", str(blocked / "deep" / "out.xml")])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert envelope["cause"]["detail"]["blocked"] == str(blocked.resolve())
    # The reason it gives is the true one. A file also fails the next question,
    # whether it can be written into, and that answer would send a person to
    # its permissions.
    assert "is not a folder" in envelope["cause"]["message"]
    assert taken == []
    assert blocked.read_bytes() == b"a file"


def test_an_existing_file_is_refused_before_the_database_is_copied(machine, monkeypatch):
    """The exclusive create would refuse it too, after the whole database was read."""
    destination = Path(machine.library.root) / "kept.xml"
    destination.write_bytes(b"somebody kept this")
    taken = _copies(monkeypatch)

    code, envelope = drive(["export", "collection", str(destination)])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "output-exists"
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


def test_a_refused_read_leaves_no_folder_behind(machine, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    destination = Path(machine.library.root) / "new" / "deeper" / "out.xml"

    code, envelope = drive(["export", "collection", str(destination)])

    assert envelope["cause"]["reason"] == "rekordbox-running", (code, envelope)
    assert not (Path(machine.library.root) / "new").exists()


@pytest.mark.parametrize("suffix", tree_registry.PENDING_XML_SUFFIXES)
def test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused(machine, suffix):
    destination = Path(machine.library.root) / f"2026-09-29{suffix}"

    code, envelope = drive(["export", "collection", str(destination)])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "library-export-unusable"
    assert not destination.exists()
    assert tree_registry.pending_intake_xml(machine) == ()


def test_an_identifier_that_is_not_digits_is_refused_and_nothing_is_written(machine):
    _content(machine, [("r-one", "R.flac", "R", 0, False, _music(machine) / "R.flac")])
    destination = Path(machine.library.root) / "exports" / "refused.xml"

    code, envelope = drive(["export", "collection", str(destination)])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "library-export-unusable"
    assert envelope["cause"]["detail"]["identifier"] == "r-one"
    assert not destination.exists()


def test_the_configured_database_is_never_opened_and_is_left_byte_for_byte(
    machine, monkeypatch
):
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


# ═══════════════════════════════════════════════════════════════════════════
# 6. Every verb that takes an export, driven against one this verb wrote
# ═══════════════════════════════════════════════════════════════════════════


def test_the_population_of_verbs_that_take_an_export_is_the_one_driven_here():
    """Derived off the shipped parsers, so a new verb taking one fails here."""
    import argparse
    import importlib

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
    "intake.land",
    "intake.imported",
    "intake.file",
    "tree.cutover",
    "route.inbox",
    "route.unplaced",
    "export.playlist",
    "sync.favorites",
    "sync.all",
}


@pytest.fixture
def silence(tmp_path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return synth_container(scratch, ".flac")


def _stage(cfg: config.Config, silence: Path, name: str) -> Path:
    path = Path(cfg.paths.download_staging) / name
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path,
        {"title": Path(name).stem, "artist": "Probe", "genre": "Deep House", "energylevel": 7},
    )
    return path


def test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second(
    machine, silence
):
    """``intake.land`` and ``intake.imported``, with the import done by hand.

    THE IMPORT IS SIMULATED BY WHAT IT CHANGES: rekordbox importing an intake
    file adds one collection row per file, recording the path. So the rows are
    added to the database, and the proof is read off a SECOND export written by
    this verb, which is the workflow the finding asks for.
    """
    cutover_fixtures.verified_snapshot(machine)
    first = _export(machine, "before-landing.xml")
    for name in ("One.flac", "Two.flac"):
        _stage(machine, silence, name)

    batch = "2026-09-29_landed"
    code, landed = drive(
        ["-d", "intake.land.confirm=apply", "intake", "land", "--export", str(first),
         "--name", batch]
    )  # fmt: skip
    assert code == int(ExitCode.PENDING_HUMAN), landed

    intake_file = Path(landed["pending_human_action"]["artifact"])
    spliced = ET.fromstring(intake_file.read_bytes())
    collection = spliced.find("COLLECTION")
    assert int(collection.get("Entries")) == len(collection.findall("TRACK")) == len(LIVE) + 2
    nodes = dict(_walk(spliced.find("PLAYLISTS").find("NODE")))
    assert len(nodes[(INTAKE, intake_file.stem)].findall("TRACK")) == 2
    # What the export already held is still there, in the same order.
    assert tuple(t.get("Key") for t in nodes[(INTAKE, BATCH)].findall("TRACK")) == (
        "11", "12", "13",
    )  # fmt: skip
    assert collection_export.provenance_of(intake_file.read_bytes()) is not None

    landed_in = Path(machine.library.root) / machine.library.music_dir / batch
    _content(
        machine,
        [
            (str(9000 + index), path.name, path.stem, 0, False, path.resolve())
            for index, path in enumerate(sorted(landed_in.glob("*.flac")))
        ],
    )
    second = _export(machine, "after-import.xml")

    code, proved = drive(["intake", "imported", "--export", str(second)])

    assert code == int(ExitCode.OK), proved
    (item,) = proved["data"]["items"]
    assert item["count"] == 2
    assert not intake_file.exists()
    tree_registry.assert_cutover_ready(machine, export=second)


def test_the_import_proof_is_withheld_against_an_export_taken_before_the_import(
    machine, silence
):
    """The other direction. A file this verb wrote is not proof by being one."""
    first = _export(machine, "before-landing.xml")
    _stage(machine, silence, "One.flac")
    code, landed = drive(
        ["-d", "intake.land.confirm=apply", "intake", "land", "--export", str(first),
         "--name", "2026-09-29_unproved"]
    )  # fmt: skip
    assert code == int(ExitCode.PENDING_HUMAN), landed
    stale = _export(machine, "still-before-import.xml")

    code, withheld = drive(["intake", "imported", "--export", str(stale)])

    assert code == int(ExitCode.PENDING_HUMAN), withheld
    assert Path(landed["pending_human_action"]["artifact"]).exists()


def test_a_single_file_intake_splices_into_the_file(machine, silence):
    exported = _export(machine)
    path = _music(machine) / "Single.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path, {"title": "Single", "artist": "Probe", "genre": "Deep House", "energylevel": 7}
    )

    code, envelope = drive(["intake", "file", str(path), "--export", str(exported)])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    spliced = ET.fromstring(Path(envelope["pending_human_action"]["artifact"]).read_bytes())
    collection = spliced.find("COLLECTION")
    assert int(collection.get("Entries")) == len(collection.findall("TRACK")) == len(LIVE) + 1


def test_a_cutover_takes_the_file_as_its_fresh_export(machine):
    """The precheck asks that the export is a file holding something, and no more.

    So it holds for this file with no rule of its own, and the file is a better
    answer to what the check is for than the one it was written against: it is
    the tree as the database held it the minute the cutover was planned.
    """
    cutover_fixtures.verified_snapshot(machine)
    exported = _export(machine)

    results = tree_registry.cutover_precheck(machine, export=exported)
    assert {result.check: result.passed for result in results}["fresh-export"] is True
    assert all(result.passed for result in results), [r.cause for r in results if r.cause]

    verb = ["tree", "cutover", DECLARED.tree.id, "--export", str(exported)]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == "tree.cutover.approve"
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, "tree.cutover.approve", "approve", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, recorded = drive(["--run", run_id, *verb])

    assert code == int(ExitCode.OK), recorded
    assert recorded["data"]["totals"]["recorded"] is True
    record = tree_registry.read(machine).record(DECLARED.tree.id)
    assert record is not None and record.mode == tree_registry.Mode.DATABASE


@pytest.fixture
def tagged(monkeypatch):
    """The tag readings the routing rules ask for, served from the file name."""
    monkeypatch.setattr(
        tags, "read_genre_from_file", lambda path: READINGS.get(Path(path).name, (None, None))[0]
    )
    monkeypatch.setattr(
        tags, "read_energy_from_file", lambda path: READINGS.get(Path(path).name, (None, None))[1]
    )
    monkeypatch.setattr(tags, "read_vox_from_file", lambda path: None)


def _sub_keys(document: bytes, folder: str, sub: str) -> tuple[str, ...]:
    nodes = dict(_walk(ET.fromstring(document).find("PLAYLISTS").find("NODE")))
    return tuple(track.get("Key") for track in nodes[(TREE, folder, sub)].findall("TRACK"))


def test_the_inbox_routing_reads_the_file_and_routes_its_intake(machine, tagged):
    exported = _export(machine)

    code, envelope = drive(
        ["-d", "route.inbox.apply=apply", "route", "inbox", "--export", str(exported)]
    )

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 3
    written = Path(envelope["data"]["totals"]["output"]).read_bytes()
    assert _sub_keys(written, "Deep House", "Low") == ("11",)
    assert _sub_keys(written, "Deep House", "Med") == ("12",)
    assert _sub_keys(written, "Tech House", "High") == ("13",)
    assert written != exported.read_bytes()


def test_the_unplaced_sweep_reads_the_file_and_places_what_no_sub_holds(machine, tagged):
    exported = _export(machine)

    code, envelope = drive(["route", "unplaced", "--export", str(exported)])

    assert code == int(ExitCode.OK), envelope
    placed = {item["track_id"]: item["destination"] for item in envelope["data"]["items"]}
    assert placed["11"] == "Deep House/Low"
    assert placed["12"] == "Deep House/Med"
    assert placed["13"] == "Tech House/High"
    written = Path(envelope["data"]["totals"]["output"]).read_bytes()
    assert _sub_keys(written, "Tech House", "High") == ("13",)


def _bind(monkeypatch, account) -> None:
    monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(account))


def test_a_playlist_export_reads_the_file_and_queues_the_playlists_tracks(
    machine, monkeypatch
):
    from cratekit.core import jobs

    exported = _export(machine)
    _bind(monkeypatch, outbound_fakes.FakeAccount(catalog={}))

    _run, job_id = approve_and_queue(
        ["export", "playlist", CRATE, "--export", str(exported)], "export.playlist.confirm"
    )

    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == ["13", "31", "11"]


def test_the_favourites_sweep_reads_the_file_and_queues_the_favourites(machine, monkeypatch):
    from cratekit.core import jobs

    exported = _export(machine)
    _bind(monkeypatch, outbound_fakes.FakeAccount(catalog={}))

    _run, job_id = approve_and_queue(
        ["sync", "favorites", "--export", str(exported)], "sync.favorites.confirm"
    )

    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == ["12", "13"]


def test_the_composed_sync_reads_the_file_and_queues_the_favourites(machine, monkeypatch):
    from cratekit.core import jobs
    from cratekit.sync import cli as sync_cli

    exported = _export(machine)
    _bind(monkeypatch, outbound_fakes.FakeAccount(catalog={}))
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
        favourites = [job for job in jobs.list_jobs(store) if job.handler_key == "sync.favorites"]
        (job,) = favourites
        assert [item.item_id for item in jobs.items(store, job.job_id)] == ["12", "13"]


# ═══════════════════════════════════════════════════════════════════════════
# 7. What the review found, each driven
# ═══════════════════════════════════════════════════════════════════════════

NOBODY = collection_export.Provenance(writer="cratekit test", written="2026-09-29T12:00:00Z")


def _rendered(tracks, nodes=()) -> collection_export.Document:
    return collection_export.render(tuple(tracks), tuple(nodes), NOBODY)


def test_an_identifier_is_spelled_one_way_in_the_collection_and_in_a_playlist():
    """A leading zero. The row and the key naming it have to be the same string."""
    document = _rendered(
        [collection_export.TrackRow(track_id="007", location="/library/a.flac")],
        [collection_export.NodeRow("1", "root", "Held", 0, 1, ("007",))],
    )
    view = library_export.read_export(document.content)

    assert tuple(entry.track_id for entry in view.entries) == ("007",)
    assert {item.path: item.track_ids for item in view.playlists} == {("Held",): ("007",)}
    assert document.omitted.dangling_members == 0


def test_two_identifiers_that_are_one_number_are_two_rows_the_reader_takes():
    document = _rendered(
        [
            collection_export.TrackRow(track_id="7", location="/library/a.flac"),
            collection_export.TrackRow(track_id="007", location="/library/b.flac"),
        ],
        [collection_export.NodeRow("1", "root", "Held", 0, 1, ("007", "7"))],
    )
    view = library_export.read_export(document.content)

    assert sorted(entry.track_id for entry in view.entries) == ["007", "7"]
    assert view.playlists[0].track_ids == ("007", "7")


def test_one_identifier_held_twice_is_refused():
    with pytest.raises(CratekitError) as caught:
        _rendered(
            [
                collection_export.TrackRow(track_id="7", location="/library/a.flac"),
                collection_export.TrackRow(track_id="7", location="/library/b.flac"),
            ]
        )
    assert caught.value.cause.reason == "library-export-unusable"


def test_a_row_handed_straight_to_the_emitter_is_held_to_digits_as_well():
    with pytest.raises(CratekitError) as caught:
        _rendered([collection_export.TrackRow(track_id='7" Evil="1', location="/a.flac")])
    assert caught.value.cause.reason == "library-export-unusable"


@pytest.mark.parametrize("bad", ["\x01", "\x00", "\x1f", "\t", "\n", "\r", "\ufffe"])
def test_a_character_no_document_may_carry_is_written_as_a_space_and_counted(bad):
    document = _rendered(
        [
            collection_export.TrackRow(
                track_id="7", name=f"Left{bad}Right", comments="plain", location="/library/a.flac"
            )
        ],
        [collection_export.NodeRow("1", "root", f"Crate{bad}Name", 0, 1, ("7",))],
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
    document = _rendered(
        [collection_export.TrackRow(track_id="7", name=AWKWARD_TITLE, location="/library/a.flac")]
    )
    assert document.omitted.normalised_text == ()


def test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine():
    document = _rendered(
        [
            collection_export.TrackRow(track_id="7", location="tidal:tracks:123"),
            collection_export.TrackRow(track_id="8", location=""),
            collection_export.TrackRow(track_id="9", location="/library/Music/a b.flac"),
            collection_export.TrackRow(
                track_id="10", location="file://localhost/library/Music/c%20d.flac"
            ),
        ]
    )
    rows = {
        track.get("TrackID"): track.get("Location")
        for track in ET.fromstring(document.content).find("COLLECTION").findall("TRACK")
    }

    assert rows == {
        "7": "tidal:tracks:123",
        "8": "",
        "9": "file://localhost/library/Music/a%20b.flac",
        "10": "file://localhost/library/Music/c%20d.flac",
    }
    assert document.omitted.not_file_paths == ("7", "8")


class _Row:
    """A playlist row as the binding hands one over, with whatever kind it holds."""

    def __init__(self, identifier: str, attribute) -> None:
        self.ID = identifier
        self.ParentID = "root"
        self.Name = f"Node {identifier}"
        self.Attribute = attribute
        self.Seq = int(identifier)
        self.rb_local_deleted = 0


class _Handle:
    def __init__(self, rows) -> None:
        self._rows = rows

    def get_playlist(self):
        return list(self._rows)

    def get_playlist_songs(self):
        return []


@pytest.mark.parametrize("unreadable", [None, "folder", "", True, 2.5j])
def test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist(unreadable):
    nodes = collection_export.read_nodes(_Handle([_Row("1", unreadable), _Row("2", 0)]))
    document = _rendered([], nodes)

    written = [
        node.get("Name")
        for node in ET.fromstring(document.content).find("PLAYLISTS").find("NODE").findall("NODE")
    ]
    assert written == ["Node 2"]
    assert document.omitted.unreadable_kinds == ("Node 1",)
    assert document.playlists == 1


def test_the_lookup_tables_are_read_once_each_and_not_once_per_row(machine):
    """Forty rows, forty artists. The statements must not grow with the rows."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{machine.library.db_path}")
    with Session(engine) as db_session:
        for index in range(40):
            db_session.add(_row(tables.DjmdArtist, ID=str(5000 + index), Name=f"Artist {index}"))
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=str(6000 + index),
                    Title=f"Title {index}",
                    ArtistID=str(5000 + index),
                    FolderPath=str(_music(machine) / f"{index}.flac"),
                    rb_local_deleted=0,
                )
            )
        db_session.commit()
    engine.dispose()

    handle = rb_writer.open_db(
        rb_writer.live_db_path(machine), require_closed=False, check_app_version=False, cfg=machine
    )
    statements: list[str] = []
    try:
        bound = handle.session.get_bind()
        event.listen(
            bound, "before_cursor_execute", lambda *args: statements.append(args[2])
        )
        tracks, _unrated = collection_export.read_tracks(handle)
    finally:
        rb_writer.close_db(handle)

    named = {track.track_id: track.artist for track in tracks}
    assert named["6000"] == "Artist 0" and named["6039"] == "Artist 39"
    assert named["12"] == "Probe & Co"
    assert len(statements) <= 1 + len(collection_export.LOOKUPS), statements


def test_the_day_added_falls_back_to_the_day_on_this_machines_clock():
    from datetime import timedelta

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


class _Song:
    def __init__(self, identifier: str, playlist: str, content: str, order: int) -> None:
        self.ID = identifier
        self.PlaylistID = playlist
        self.ContentID = content
        self.TrackNo = order
        self.rb_local_deleted = 0


class _Songs(_Handle):
    def __init__(self, rows, songs) -> None:
        super().__init__(rows)
        self._songs = songs

    def get_playlist_songs(self):
        return list(self._songs)


def test_members_come_out_in_their_stored_order_whatever_order_the_rows_arrive_in():
    songs = [
        _Song("c", "1", "30", 3),
        _Song("a", "1", "10", 1),
        _Song("b", "1", "20", 2),
    ]
    (node,) = collection_export.read_nodes(_Songs([_Row("1", 0)], songs))
    assert node.members == ("10", "20", "30")


def test_siblings_come_out_in_their_sequence_and_not_in_identifier_order():
    document = _rendered(
        [],
        [
            collection_export.NodeRow("1", "root", "Third", 0, 3),
            collection_export.NodeRow("2", "root", "First", 0, 1),
            collection_export.NodeRow("3", "root", "Second", 1, 2),
        ],
    )
    root = ET.fromstring(document.content).find("PLAYLISTS").find("NODE")
    assert [node.get("Name") for node in root.findall("NODE")] == ["First", "Second", "Third"]


def test_a_membership_somebody_removed_is_not_written_back_into_the_playlist():
    """The zero row E2 bought this. The track is live. Its place in the list is not."""
    removed = _Song("b", "1", "20", 2)
    removed.rb_local_deleted = 1
    songs = [_Song("a", "1", "10", 1), removed, _Song("c", "1", "30", 3)]
    (node,) = collection_export.read_nodes(_Songs([_Row("1", 0)], songs))
    assert node.members == ("10", "30")

    document = _rendered(
        [
            collection_export.TrackRow(track_id=key, location=f"/library/{key}.flac")
            for key in ("10", "20", "30")
        ],
        [node],
    )
    view = library_export.read_export(document.content)
    assert view.playlists[0].track_ids == ("10", "30")
    assert document.omitted.dangling_members == 0


def test_a_membership_that_cannot_say_whether_it_was_removed_refuses():
    unreadable = _Song("a", "1", "10", 1)
    unreadable.rb_local_deleted = None
    with pytest.raises(CratekitError) as caught:
        collection_export.read_nodes(_Songs([_Row("1", 0)], [unreadable]))
    assert caught.value.cause.reason == "soft-delete-marker-unreadable"
