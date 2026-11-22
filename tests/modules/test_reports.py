"""The read-only library reports, and the promise that they are read-only.

A question a person must ANSWER is a review item and a result a person READS is
output (R12), so the duplicate audit offers into ``Queue.DUPLICATES`` and the
aging report returns a value; neither writes a file of its own. The read-only
promise is proved twice: behaviourally, by comparing every byte and database row
before and after a run, and structurally, by holding the package's syntax tree to
an import allowlist and a filesystem mutation rule.
"""

from __future__ import annotations

import ast
import hashlib
import os
import re
import sqlite3
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import NamedTuple

import pytest

from cratekit.core import config, review, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.core.taxonomy import default_taxonomy
from cratekit.modules.reports import aging, duplicates, export
from cratekit.write import rbxml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_ROOT = REPO_ROOT / "src"
REPORTS_ROOT = SRC_ROOT / "cratekit" / "modules" / "reports"

#: The naming template this library declares: a key and tempo head, and a lossy
#: marker inside it. Built here rather than defaulted, so the head stripping is
#: exercised against the shape a real name has.
TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))

TODAY = date(2026, 8, 2)


# Fixtures: a whole synthetic library, in bytes


def _collection(
    tracks: list[tuple[int, str, str, str]], *, declared: int | None = None
) -> list[str]:
    """The COLLECTION section for ``(track_id, name, artist, location)`` rows."""
    lines = [f'  <COLLECTION Entries="{len(tracks) if declared is None else declared}">']
    for track_id, name, artist, location in tracks:
        lines.append(
            f'    <TRACK TrackID="{track_id}" '
            f'Name="{rbxml.xml_escape_attr(name)}" '
            f'Artist="{rbxml.xml_escape_attr(artist)}" '
            f'Location="{rbxml.xml_escape_attr(location)}"/>'
        )
    lines.append("  </COLLECTION>")
    return lines


def _document(*, collection: list[str], root_children: list[str], root_count: int) -> bytes:
    """A byte-exact export: CRLF everywhere, and the indents the locates expect."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<DJ_PLAYLISTS Version="1.0.0">',
        '  <PRODUCT Name="rekordbox" Version="6.0.0" Company="AlphaTheta"/>',
        *collection,
        "  <PLAYLISTS>",
        f'    <NODE Type="0" Name="ROOT" Count="{root_count}">',
        *root_children,
        "    </NODE>",
        "  </PLAYLISTS>",
        "</DJ_PLAYLISTS>",
    ]
    return ("\r\n".join(lines) + "\r\n").encode("utf-8")


def _folder(name: str, count: int, depth: int) -> str:
    return rbxml.folder_open(name, count, rbxml.indent_at(depth)).rstrip("\r\n")


def _playlist(name: str, track_ids: list[int], depth: int) -> list[str]:
    indent = rbxml.indent_at(depth)
    out = [rbxml.playlist_open(name, len(track_ids), indent).rstrip("\r\n")]
    out += [
        line
        for line in rbxml.track_key_lines(track_ids, rbxml.indent_at(depth + 1)).split("\r\n")
        if line
    ]
    out.append(rbxml.node_close(indent).rstrip("\r\n"))
    return out


def _close(depth: int) -> str:
    return rbxml.node_close(rbxml.indent_at(depth)).rstrip("\r\n")


INTAKE = default_taxonomy().intake
TREE = default_taxonomy().tree


def library_export() -> bytes:
    """One export carrying every shape the two reports have to handle."""
    tracks = [
        (1, "08A - 124 - Cold Light", "Recondite", "file://localhost/library/a.flac"),
        (2, "05B - 120 - Other Thing", "Somebody", "file://localhost/library/b.flac"),
        (4, "11A - 126 - [MP3] Cold  Light", "recondite", "file://localhost/library/d.flac"),
        (5, "", "", "file://localhost/library/e.flac"),
    ]
    root_children = [
        _folder(TREE.display, 2, 1),
        _folder("Deep House", 1, 2),
        *_playlist("High", [1], 3),
        _close(2),
        _folder("Melodic House", 1, 2),
        *_playlist("Med", [4, 2], 3),
        _close(2),
        _close(1),
        _folder(INTAKE.display, 5, 1),
        *_playlist("phil_07_01_2026", [1], 2),
        *_playlist("lisa_07_30_26", [2], 2),
        *_playlist("2026-06-15 bandcamp", [4], 2),
        *_playlist("white labels", [5], 2),
        _folder("Old", 1, 2),
        *_playlist("phil_5_01_25", [1], 3),
        _close(2),
        _close(1),
    ]
    return _document(collection=_collection(tracks), root_children=root_children, root_count=2)


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library, saved, so a second process resolves the same one."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def store(cfg):
    with review.open_store(cfg) as opened:
        yield opened


@pytest.fixture
def view():
    return export.read_export(library_export())


# The export reader: a wrong document is never an empty library


def test_a_document_that_is_not_an_export_refuses_rather_than_reading_as_empty():
    """The U11 shape, one package along."""
    with pytest.raises(CratekitError) as raised:
        export.read_export(b'{"tracks": []}')
    assert raised.value.cause.reason == "library-export-unusable"
    assert "not a rekordbox collection export" in raised.value.cause.message


@pytest.mark.parametrize(
    "content, expected",
    [
        (
            _document(collection=[], root_children=[], root_count=0),
            "no COLLECTION section",
        ),
        (
            _document(
                collection=["  <COLLECTION>", "  </COLLECTION>"],
                root_children=[],
                root_count=0,
            ),
            "declares no entry count",
        ),
        (
            _document(
                collection=['  <COLLECTION Entries="many">', "  </COLLECTION>"],
                root_children=[],
                root_count=0,
            ),
            "not a number",
        ),
        (
            _document(collection=_collection([]), root_children=[], root_count=0).replace(
                b"  <PLAYLISTS>\r\n", b""
            ),
            "no PLAYLISTS section",
        ),
    ],
)
def test_each_missing_structure_is_refused_by_name(content, expected):
    """Recognized positively, one structure at a time, so the failure is legible."""
    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert expected in raised.value.cause.message


def test_a_playlist_section_with_no_root_node_refuses():
    content = _document(collection=_collection([]), root_children=[], root_count=0)
    stripped = content.replace(b'    <NODE Type="0" Name="ROOT" Count="0">\r\n', b"")
    with pytest.raises(CratekitError) as raised:
        export.read_export(stripped)
    assert "no root node" in raised.value.cause.message


def test_a_document_carrying_both_names_in_the_wrong_order_refuses():
    """Something else that happens to contain both names is not a damaged export."""
    body = _document(collection=_collection([]), root_children=[], root_count=0)
    opening = b'<DJ_PLAYLISTS Version="1.0.0">\r\n'
    section = b'  <COLLECTION Entries="0">\r\n  </COLLECTION>\r\n'
    assert section in body and opening in body
    moved = body.replace(section, b"").replace(opening, section + opening)

    with pytest.raises(CratekitError) as raised:
        export.read_export(moved)
    assert "outside the document element" in raised.value.cause.message


def test_the_entry_count_is_read_from_the_section_and_never_from_a_track():
    """The window that bounds the attribute search, which nothing used to reach."""
    content = _document(
        collection=[
            "  <COLLECTION>",
            '    <TRACK TrackID="1" Name="live Entries="99" set" '
            'Artist="a" Location="file://localhost/library/a.flac"/>',
            "  </COLLECTION>",
        ],
        root_children=[],
        root_count=0,
    )
    assert b'Entries="99"' in content

    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert "declares no entry count" in raised.value.cause.message


def test_a_truncated_export_refuses_because_the_declared_count_disagrees():
    """The half-copied file, which is the case the count check exists for."""
    content = _document(
        collection=_collection([(1, "a", "b", "file://localhost/library/a.flac")], declared=4),
        root_children=[],
        root_count=0,
    )
    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert raised.value.cause.detail["declared"] == 4
    assert raised.value.cause.detail["located"] == 1


def test_a_track_element_with_no_identifier_makes_the_count_disagree():
    """The other way a document can be wrong while looking well formed."""
    content = _document(
        collection=[
            '  <COLLECTION Entries="2">',
            '    <TRACK TrackID="1" Name="a" Artist="b" Location="file://localhost/library/a.flac"/>',
            '    <TRACK Name="c" Artist="d" Location="file://localhost/library/c.flac"/>',
            "  </COLLECTION>",
        ],
        root_children=[],
        root_count=0,
    )
    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert raised.value.cause.detail["located"] == 1


def test_a_track_element_spanning_several_lines_is_read_whole():
    """The shape a REAL export has, which a minimal fixture does not."""
    content = _document(
        collection=[
            '  <COLLECTION Entries="1">',
            '    <TRACK TrackID="1" Name="08A - 124 - Cold Light"',
            '      Artist="Recondite" Composer=""',
            '      Location="file://localhost/library/a.flac" Rating="0">',
            "    </TRACK>",
            "  </COLLECTION>",
        ],
        root_children=[],
        root_count=0,
    )
    entries = export.read_export(content).entries
    assert len(entries) == 1
    assert entries[0].artist == "Recondite"
    assert entries[0].location == "file://localhost/library/a.flac"


def test_one_track_identifier_used_twice_refuses():
    """An identifier is what every later answer is addressed BY."""
    content = _document(
        collection=[
            '  <COLLECTION Entries="2">',
            '    <TRACK TrackID="7" Name="a" Artist="b" Location="file://localhost/a.flac"/>',
            '    <TRACK TrackID="7" Name="a" Artist="b" Location="file://localhost/b.flac"/>',
            "  </COLLECTION>",
        ],
        root_children=[],
        root_count=0,
    )
    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert "the same TrackID more than once" in raised.value.cause.message
    assert raised.value.cause.detail["repeated"] == ["7"]


def test_the_reader_reports_the_folders_it_walked_through(view):
    """Carried because an absent structure and an empty one are not one fact."""
    assert view.has_folder(INTAKE.display)
    assert view.has_folder("Old")
    assert not view.has_folder("Bandcamp Queue")


def test_a_genuinely_empty_library_reads_as_empty_rather_than_refusing():
    """P7's other half: the guard must not fire on the correct document."""
    view = export.read_export(_document(collection=_collection([]), root_children=[], root_count=0))
    assert view.entries == ()
    assert view.playlists == ()


def test_a_file_that_cannot_be_opened_refuses_rather_than_returning_nothing(tmp_path):
    with pytest.raises(CratekitError) as raised:
        export.read_export_file(tmp_path / "never-written.xml")
    assert raised.value.cause.reason == "library-export-unusable"


def test_the_reader_returns_every_entry_with_the_playlists_that_hold_it(view):
    assert [entry.track_id for entry in view.entries] == ["1", "2", "4", "5"]
    first = view.entry("1")
    assert first is not None
    assert first.artist == "Recondite"
    assert (TREE.display, "Deep House", "High") in first.playlists
    assert (INTAKE.display, "phil_07_01_2026") in first.playlists


def test_the_reader_returns_playlists_and_never_folders(view):
    displays = {playlist.display for playlist in view.playlists}
    assert "High" in displays and "Med" in displays
    assert TREE.display not in displays and "Deep House" not in displays


#: THE THREE SPELLINGS OF A KIND THIS BUILD CANNOT READ, applied to the export
#: every other test in this file drives rather than to a document written for the
#: occasion. ``Type="2"`` is a value the format does not define, the attribute
#: removed is the one a truncated or hand-edited export produces, and ``Type=""``
#: is the attribute present and saying nothing. All three reach the classifier as
#: something that is neither declared type, and no fixture in this repository
#: built one of them before, which is why nothing could see the defect.
UNREADABLE_KINDS = [
    ("a Type value the format does not define", b'Type="1"', b'Type="2"'),
    ("no Type attribute at all", b' Type="1"', b""),
    ("a Type attribute whose value is empty", b'Type="1"', b'Type=""'),
]


@pytest.mark.parametrize(
    "old, new",
    [(spelling, replacement) for _, spelling, replacement in UNREADABLE_KINDS],
    ids=[shape for shape, _, _ in UNREADABLE_KINDS],
)
def test_a_node_whose_kind_cannot_be_read_refuses_rather_than_reading_as_a_folder(old, new, cfg):
    """The two answers side by side, which is the whole finding."""
    healthy = export.read_export(library_export())
    report = aging.intake_aging(
        healthy, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    assert (len(report.expired), len(report.stale)) == (1, 2)

    content = library_export().replace(old, new)
    assert content != library_export(), "the substitution changed nothing"
    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert raised.value.cause.reason == "library-export-unusable"
    assert "kind it does not declare" in raised.value.cause.message
    assert f"{INTAKE.display} / phil_07_01_2026" in raised.value.cause.detail["nodes"]


def _paths_the_shipped_classification_called_folders(content: bytes) -> tuple:
    """Every node a "playlist, or else a folder" rule would have filed as a folder."""
    root = rbxml.root_node(content)
    assert root is not None
    return tuple(
        path
        for path, node in rbxml.walk_nodes(content, root)
        if rbxml.node_kind(node.node_type) != rbxml.KIND_PLAYLIST
    )


@pytest.mark.parametrize(
    "substitutions, intake_kind",
    [
        ([(b'Type="1"', b'Type="2"')], rbxml.KIND_FOLDER),
        (
            [(b'Type="1"', b'Type="2"'), (b'Type="0"', b'Type="2"')],
            rbxml.KIND_UNREADABLE,
        ),
    ],
    ids=["only the playlists are unreadable", "every node is unreadable"],
)
def test_the_misread_nodes_satisfy_the_very_guard_written_to_catch_their_loss(
    substitutions, intake_kind
):
    """Why one more check inside the aging report could not have closed this."""
    content = library_export()
    for old, new in substitutions:
        assert old in content, "the substitution matched nothing"
        content = content.replace(old, new)

    root = rbxml.root_node(content)
    assert root is not None
    kinds = {
        path[-1]: rbxml.node_kind(node.node_type) for path, node in rbxml.walk_nodes(content, root)
    }
    assert kinds[INTAKE.display] == intake_kind
    assert kinds["phil_07_01_2026"] == rbxml.KIND_UNREADABLE

    as_folders = export.LibraryView(
        entries=(),
        playlists=(),
        folders=_paths_the_shipped_classification_called_folders(content),
    )
    assert len(as_folders.folders) == 12, "every node was filed as a folder"
    assert as_folders.has_folder(INTAKE.display)
    assert aging.intake_groupings(as_folders, intake=INTAKE, today=TODAY) == ()


def test_every_node_in_a_healthy_export_declares_a_kind_the_reader_knows():
    """The other side of the same classification, so it cannot be vacuous."""
    content = library_export()
    root = rbxml.root_node(content)
    assert root is not None
    kinds = {rbxml.node_kind(node.node_type) for _, node in rbxml.walk_nodes(content, root)}
    assert kinds == {rbxml.KIND_FOLDER, rbxml.KIND_PLAYLIST}


# Scenario 3: duplicates across two folders, not only within one playlist


def test_duplicates_across_two_folders_are_detected(view):
    """The case the source system cannot see at all."""
    groups = duplicates.audit(view, template=TEMPLATE)
    assert len(groups) == 1
    group = groups[0]
    assert {member.track_id for member in group.members} == {"1", "4"}
    assert group.spans_playlists
    placements = {path for member in group.members for path in member.playlists}
    assert (TREE.display, "Deep House", "High") in placements
    assert (TREE.display, "Melodic House", "Med") in placements


def test_two_copies_are_one_recording_across_head_marker_case_and_spacing(view):
    """Every difference between the two copies is one the head or case explains."""
    entries = {entry.track_id: entry for entry in view.entries}
    left = duplicates.recording_of(entries["1"], template=TEMPLATE)
    right = duplicates.recording_of(entries["4"], template=TEMPLATE)
    assert left == right == duplicates.Recording(artist="recondite", title="cold light")


def test_entries_with_nothing_to_compare_are_never_grouped(view):
    """An untagged file has no recording identity, and pretending it does is worse."""
    groups = duplicates.audit(view, template=TEMPLATE)
    grouped = {member.track_id for group in groups for member in group.members}
    assert "5" not in grouped


def test_entries_carrying_only_an_artist_are_never_grouped():
    """The half-tagged case, which fails the same way the untagged one does."""
    tracks = [
        (index, "", "Recondite", f"file://localhost/library/{index}.flac") for index in (1, 2, 3)
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=[], root_count=0)
    )
    assert duplicates.audit(view, template=TEMPLATE) == ()


def test_entries_carrying_only_a_title_are_never_grouped():
    """The mirror of the case above, refused by the same rule for the same reason."""
    tracks = [
        (index, "08A - 124 - Untitled", "", f"file://localhost/library/{index}.flac")
        for index in (1, 2, 3)
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=[], root_count=0)
    )
    assert duplicates.audit(view, template=TEMPLATE) == ()


#: One recording, two composition forms. Written as ESCAPES rather than as
#: literal characters, because the two spellings are indistinguishable on
#: screen and in a diff, and a fixture whose whole point is that they differ
#: must not depend on anybody's editor or terminal preserving the difference.
_NFC_NAME = "Bj\u00f6rk"
_NFD_NAME = "Bjo\u0308rk"


def test_two_composition_forms_of_one_name_are_one_recording():
    """The NFC split, which the timid normalization is not allowed to be timid about."""
    assert _NFC_NAME != _NFD_NAME
    tracks = [
        (1, "08A - 124 - Cold Light", _NFC_NAME, "file://localhost/library/a.flac"),
        (2, "11A - 126 - Cold Light", _NFD_NAME, "file://localhost/library/b.flac"),
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=[], root_count=0)
    )
    groups = duplicates.audit(view, template=TEMPLATE)
    assert len(groups) == 1
    assert {member.track_id for member in groups[0].members} == {"1", "2"}


def test_re_tagging_into_the_other_composition_form_keeps_the_decision(store):
    """The consequence that is worse than the missed duplicate."""

    def viewed(artist: str):
        tracks = [
            (index, "08A - 124 - Cold Light", artist, f"file://localhost/library/{index}.flac")
            for index in (1, 2)
        ]
        return export.read_export(
            _document(collection=_collection(tracks), root_children=[], root_count=0)
        )

    before = duplicates.audit_and_offer(viewed(_NFC_NAME), store, template=TEMPLATE)
    after = duplicates.audit_and_offer(viewed(_NFD_NAME), store, template=TEMPLATE)
    assert before.items[0].item_id == after.items[0].item_id
    assert len(review.list_items(store, queue=review.Queue.DUPLICATES).items) == 1


def test_a_recording_present_once_is_not_a_duplicate(view):
    groups = duplicates.audit(view, template=TEMPLATE)
    grouped = {member.track_id for group in groups for member in group.members}
    assert "2" not in grouped


def test_three_copies_are_one_question_rather_than_three_pairs():
    """Pairwise questions about one recording are the same question, repeated."""
    tracks = [
        (index, "08A - 124 - Cold Light", "Recondite", f"file://localhost/library/{index}.flac")
        for index in (1, 2, 3)
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=[], root_count=0)
    )
    groups = duplicates.audit(view, template=TEMPLATE)
    assert len(groups) == 1
    assert len(groups[0].members) == 3


# Scenario 1: the audit's output is a review item, never a file


def test_the_audit_puts_its_pairs_in_the_review_queue(view, store):
    report = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert len(report.items) == 1
    item = report.items[0]
    assert item.queue == review.Queue.DUPLICATES
    assert item.kind == duplicates.KIND
    assert review.count_unresolved(store, queue=review.Queue.DUPLICATES) == 1
    assert {option.option_id for option in item.options} == {"1", "4"}


def test_every_item_carries_the_handler_key_the_registry_declares(view, store):
    """Addressability, which the default of "" silently opted every item out of."""
    report = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert duplicates.HANDLER_KEY == "audit.duplicates"
    assert {item.handler_key for item in report.items} == {duplicates.HANDLER_KEY}
    addressed = review.list_items(store, handler_key=duplicates.HANDLER_KEY).items
    assert [item.item_id for item in addressed] == [report.items[0].item_id]
    assert review.list_items(store, handler_key="").items == ()


def test_the_declared_handler_key_is_the_one_the_registry_carries():
    """Read from the registry rather than restated, so a rename fails here."""
    from cratekit.cli import registry

    declared = {
        entry.handler_key for entry in registry.entries() if entry.name == "audit.duplicates"
    }
    assert declared == {duplicates.HANDLER_KEY}


def test_the_item_is_addressed_by_the_recording_and_shows_the_copies(view, store):
    report = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    item = report.items[0]
    assert review.identity_of(store, item.item_id) == {
        "artist": "recondite",
        "title": "cold light",
    }
    assert item.payload["copies"] == 2
    assert {member["track_id"] for member in item.payload["members"]} == {"1", "4"}


def test_running_the_audit_twice_produces_one_item(view, store):
    """IDEMPOTENT, which is the requirement rather than an optimization."""
    first = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    second = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert [item.item_id for item in first.items] == [item.item_id for item in second.items]
    assert len(review.list_items(store, queue=review.Queue.DUPLICATES).items) == 1


def test_a_renamed_or_re_imported_copy_keeps_the_decision(store):
    """The identity is the RECORDING, so nothing about the file is in it."""
    before = export.read_export(
        _document(
            collection=_collection(
                [
                    (1, "08A - 124 - Cold Light", "Recondite", "file://localhost/library/a.flac"),
                    (2, "08A - 124 - Cold Light", "Recondite", "file://localhost/library/b.flac"),
                ]
            ),
            root_children=[],
            root_count=0,
        )
    )
    after = export.read_export(
        _document(
            collection=_collection(
                [
                    (77, "08A - 124 - Cold Light", "Recondite", "file://localhost/library/x.flac"),
                    (78, "08A - 124 - Cold Light", "Recondite", "file://localhost/library/y.flac"),
                ]
            ),
            root_children=[],
            root_count=0,
        )
    )
    first = duplicates.audit_and_offer(before, store, template=TEMPLATE)
    second = duplicates.audit_and_offer(after, store, template=TEMPLATE)
    assert first.items[0].item_id == second.items[0].item_id


# Scenario 2: never deletes, and the ignore persists across runs and processes


_REJECT_IN_ANOTHER_PROCESS = """
import sys

from cratekit.core import config, review

cfg = config.load()
with review.open_store(cfg) as store:
    review.resolve(store, sys.argv[1], review.Verdict.REJECTED, actor="another-process")
"""


def _in_another_process(script: str, *arguments: str) -> None:
    """Run a short script in a genuinely separate interpreter, and check it."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    finished = subprocess.run(
        [sys.executable, "-c", script, *arguments],
        env=env,
        capture_output=True,
        text=True,
    )
    assert finished.returncode == 0, finished.stderr or finished.stdout


def test_an_intentional_alternate_stays_ignored_across_runs_and_processes(view, cfg, store):
    """The scenario, end to end, with the verdict recorded by a real process."""
    first = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert len(first.outstanding) == 1

    _in_another_process(_REJECT_IN_ANOTHER_PROCESS, first.items[0].item_id)

    with review.open_store(cfg) as reopened:
        second = duplicates.audit_and_offer(view, reopened, template=TEMPLATE)
    assert second.groups, "the pair is still a duplicate; it is just no longer a question"
    assert second.outstanding == ()
    assert [item.item_id for item in second.suppressed] == [first.items[0].item_id]


def test_a_revoked_ignore_puts_the_pair_back_in_front_of_a_person(view, store):
    """R12 and R36 both need the door to open both ways."""
    first = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    review.resolve(store, first.items[0].item_id, review.Verdict.REJECTED, actor="me")
    review.clear(store, first.items[0].item_id, actor="me")
    assert len(duplicates.audit_and_offer(view, store, template=TEMPLATE).outstanding) == 1


def test_the_audit_deletes_nothing_from_the_library(cfg, store):
    """The behavioural half of "never deletes", over real files on disk."""
    music = cfg.library.root / "Music"
    for name in ("a.flac", "b.flac", "d.flac", "e.flac"):
        (music / name).write_bytes(b"not really audio, but really bytes")
    exported = music / "collection.xml"
    exported.write_bytes(library_export())

    duplicates.audit_and_offer(export.read_export_file(exported), store, template=TEMPLATE)

    assert sorted(path.name for path in music.iterdir()) == [
        "a.flac",
        "b.flac",
        "collection.xml",
        "d.flac",
        "e.flac",
    ]


# Scenario 4: aging thresholds come from config, never from a module constant


def test_the_thresholds_have_no_defaults_so_a_hardcoded_policy_cannot_exist():
    """Structural, and it is what makes the scenario true rather than observed."""
    import dataclasses

    for field in dataclasses.fields(aging.AgingThresholds):
        assert field.default is dataclasses.MISSING, (
            f"{field.name} carries a default, so a caller can build a policy "
            f"without reading configuration"
        )
    with pytest.raises(TypeError):
        aging.AgingThresholds()  # type: ignore[call-arg]


def test_the_thresholds_come_from_the_configured_values(cfg):
    assert aging.thresholds_from(cfg) == aging.AgingThresholds(stale_days=30, expired_days=90)


def test_changing_the_configured_thresholds_changes_the_report(view, cfg):
    """The same library, two policies, two answers. Nothing is pinned in code."""
    lenient = aging.intake_aging(
        view,
        intake=INTAKE,
        thresholds=aging.thresholds_from(cfg),
        today=TODAY,
    )
    strict_cfg = config.from_dict(
        {
            **config.load().to_toml_dict(),
            "reports": {"intake_stale_days": 1, "intake_expired_days": 2},
        }
    )
    strict = aging.intake_aging(
        view,
        intake=INTAKE,
        thresholds=aging.thresholds_from(strict_cfg),
        today=TODAY,
    )
    assert {group.display for group in lenient.expired} == {"phil_5_01_25"}
    assert {group.display for group in strict.expired} == {
        "phil_5_01_25",
        "phil_07_01_2026",
        "2026-06-15 bandcamp",
        "lisa_07_30_26",
    }
    assert strict.current == ()


def test_the_report_carries_the_thresholds_it_was_run_against(view, cfg):
    report = aging.intake_aging(
        view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    assert report.thresholds == aging.thresholds_from(cfg)
    assert report.as_of == TODAY


@pytest.mark.parametrize(
    "raw, expected",
    [
        ({"intake_stale_days": 0}, "positive whole number"),
        ({"intake_expired_days": -1}, "positive whole number"),
        ({"intake_stale_days": "thirty"}, "positive whole number"),
        ({"intake_stale_days": 120}, "earlier than"),
    ],
)
def test_a_configured_threshold_that_cannot_describe_a_policy_is_refused(
    tmp_path, monkeypatch, raw, expected
):
    """Reported with the key that is wrong, which is what a file needs."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    problems = config.validate(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
            "reports": raw,
        }
    )
    assert any(expected in problem for problem in problems), problems


def test_a_rejected_threshold_is_never_reported_against_the_default_it_did_not_set(
    tmp_path, monkeypatch
):
    """The message has to name the line the person can go and fix."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    problems = config.validate(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
            "reports": {"intake_stale_days": "thirty", "intake_expired_days": 5},
        }
    )
    assert any("intake_stale_days must be a positive" in problem for problem in problems)
    assert not any("earlier than" in problem for problem in problems), problems


@pytest.mark.parametrize(
    "stale, expired",
    [(0, 90), (30, 29), (-1, 5)],
)
def test_a_threshold_pair_built_in_code_refuses_the_same_rule(stale, expired):
    with pytest.raises(aging.AgingPolicyInvalid):
        aging.AgingThresholds(stale_days=stale, expired_days=expired)


# The aging report itself


def test_every_grouping_lands_in_exactly_one_band(view, cfg):
    """A grouping in two bands is acted on twice; one in none was never surfaced."""
    report = aging.intake_aging(
        view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    every = aging.intake_groupings(view, intake=INTAKE, today=TODAY)
    banded = [group.path for group in report.groupings]
    assert sorted(banded) == sorted(group.path for group in every)
    assert len(banded) == len(set(banded))


def test_the_bands_are_the_ages_the_thresholds_declare(view, cfg):
    report = aging.intake_aging(
        view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    assert {group.display for group in report.expired} == {"phil_5_01_25"}
    assert {group.display for group in report.stale} == {
        "phil_07_01_2026",
        "2026-06-15 bandcamp",
    }
    assert {group.display for group in report.current} == {"lisa_07_30_26"}
    assert {group.display for group in report.undated} == {"white labels"}


def test_a_grouping_nested_below_the_intake_flow_is_aged_too(view, cfg):
    """Somebody who filed their intake into a folder has organized it, not hidden it."""
    report = aging.intake_aging(
        view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    nested = [group for group in report.expired if group.display == "phil_5_01_25"]
    assert nested and nested[0].path == (INTAKE.display, "Old", "phil_5_01_25")


def test_nothing_outside_the_intake_flow_is_reported(view):
    """The routing tree is not an intake queue, and aging it would be nonsense."""
    groupings = aging.intake_groupings(view, intake=INTAKE, today=TODAY)
    assert all(group.path[0] == INTAKE.display for group in groupings)
    assert not any(group.display in {"High", "Med"} for group in groupings)


def test_an_undated_grouping_is_reported_and_never_aged(view, cfg):
    report = aging.intake_aging(
        view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    assert [group.display for group in report.undated] == ["white labels"]
    assert all(group.age_days is None for group in report.undated)


def test_a_grouping_carries_the_number_of_tracks_in_it(view):
    groupings = {
        group.display: group for group in aging.intake_groupings(view, intake=INTAKE, today=TODAY)
    }
    assert groupings["phil_07_01_2026"].track_count == 1
    assert groupings["white labels"].track_count == 1


@pytest.mark.parametrize(
    "name, expected",
    [
        ("lisa_06_19_2026", date(2026, 6, 19)),
        ("3_9_26_phil", date(2026, 3, 9)),
        ("02_19_26 lisa", date(2026, 2, 19)),
        ("2026-06-15 bandcamp", date(2026, 6, 15)),
        ("white labels", None),
        ("13_45_26 nonsense", None),
        ("2_30_26 february thirtieth", None),
        ("2026-02-30 also not a day", None),
        ("phil_5_01_1999", None),
        ("phil_5_01_2500", None),
        ("phil_5_01_99", date(2099, 5, 1)),
    ],
)
def test_the_intake_naming_conventions_all_parse(name, expected):
    """Every shape the live library actually uses, plus the ones that must not."""
    assert aging.parse_intake_date(name) == expected


def test_a_name_with_two_dates_is_dated_by_the_first():
    """The intake date is at the front; the second is usually a source list."""
    assert aging.parse_intake_date("6_01_26 lisa_5_26_26") == date(2026, 6, 1)


def test_the_oldest_grouping_is_reported_first():
    """Ties break on the path, so two runs of an unchanged library agree."""
    tracks = [(1, "n", "a", "file://localhost/library/a.flac")]
    root_children = [
        _folder(INTAKE.display, 3, 1),
        *_playlist("phil_01_01_2026", [1], 2),
        *_playlist("phil_03_01_2026", [1], 2),
        *_playlist("phil_02_01_2026", [1], 2),
        _close(1),
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=root_children, root_count=1)
    )
    report = aging.intake_aging(
        view,
        intake=INTAKE,
        thresholds=aging.AgingThresholds(stale_days=1, expired_days=2),
        today=TODAY,
    )
    assert [group.display for group in report.expired] == [
        "phil_01_01_2026",
        "phil_02_01_2026",
        "phil_03_01_2026",
    ]


def test_two_groupings_of_one_age_are_ordered_by_path_not_by_the_walk():
    """The TIE-BREAK, which the fixture above never reached."""
    tracks = [(1, "n", "a", "file://localhost/library/a.flac")]
    root_children = [
        _folder(INTAKE.display, 2, 1),
        *_playlist("phil_01_01_2026 zulu", [1], 2),
        *_playlist("phil_01_01_2026 alpha", [1], 2),
        _close(1),
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=root_children, root_count=1)
    )
    report = aging.intake_aging(
        view,
        intake=INTAKE,
        thresholds=aging.AgingThresholds(stale_days=1, expired_days=2),
        today=TODAY,
    )
    ages = {group.age_days for group in report.expired}
    assert len(ages) == 1, f"the two groupings must be the same age to tie: {ages}"
    assert [group.display for group in report.expired] == [
        "phil_01_01_2026 alpha",
        "phil_01_01_2026 zulu",
    ]


# The verification: both run against a copy and write nothing


def _tree_digest(root: Path) -> dict[str, tuple[str, int]]:
    """Every file under ``root``, by relative path, content hash AND modified time."""
    return {
        str(path.relative_to(root)): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            path.stat().st_mtime_ns,
        )
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_the_digest_sees_a_write_that_changed_no_byte(tmp_path):
    """The INSTRUMENT, checked before anything is concluded from it."""
    probe_root = tmp_path / "probe"
    probe_root.mkdir()
    stamped = probe_root / "unchanged.bin"
    stamped.write_bytes(b"identical either way")

    before = _tree_digest(probe_root)
    moved = stamped.stat().st_mtime_ns + 1_000_000_000
    os.utime(stamped, ns=(moved, moved))
    after = _tree_digest(probe_root)

    assert after != before, (
        "the digest cannot see a write that leaves the bytes alone, so the two "
        "read-only comparisons built on it are weaker than they read"
    )
    assert after["unchanged.bin"][0] == before["unchanged.bin"][0], (
        "and the difference has to be the stamp rather than the content, or this "
        "is measuring the wrong thing"
    )


def _database_rows(path: Path) -> list[tuple]:
    """Every row of the synthetic database, so a write to it would be visible."""
    with sqlite3.connect(str(path)) as conn:
        return list(conn.execute("SELECT id, title FROM content ORDER BY id"))


@pytest.fixture
def library_on_disk(cfg):
    """A library with audio, a database, and an export, all in a temp directory."""
    music = cfg.library.root / "Music"
    for name in ("a.flac", "b.flac", "d.flac", "e.flac"):
        (music / name).write_bytes(b"audio bytes for " + name.encode("utf-8"))
    exported = music / "collection.xml"
    exported.write_bytes(library_export())

    cfg.library.db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(cfg.library.db_path)) as conn:
        conn.execute("CREATE TABLE content (id INTEGER PRIMARY KEY, title TEXT)")
        conn.executemany(
            "INSERT INTO content (id, title) VALUES (?, ?)",
            [(1, "Cold Light"), (2, "Other Thing")],
        )
    return exported


def test_the_aging_report_changes_no_byte_anywhere(cfg, library_on_disk, tmp_path):
    """The strongest form of the claim: nothing on disk moves, at all."""
    rows_before = _database_rows(cfg.library.db_path)
    before = _tree_digest(tmp_path)

    aging.intake_aging(
        export.read_export_file(library_on_disk),
        intake=INTAKE,
        thresholds=aging.thresholds_from(cfg),
        today=TODAY,
    )

    assert _tree_digest(tmp_path) == before
    assert _database_rows(cfg.library.db_path) == rows_before


def test_the_duplicate_audit_changes_nothing_except_the_review_queue(
    cfg, library_on_disk, tmp_path
):
    """The one write, named, and everything else asserted byte-identical."""
    rows_before = _database_rows(cfg.library.db_path)
    before = _tree_digest(tmp_path)

    with review.open_store(cfg) as store:
        duplicates.audit_and_offer(
            export.read_export_file(library_on_disk), store, template=TEMPLATE
        )

    after = _tree_digest(tmp_path)
    queue_dir = review.store_dir(cfg).resolve()
    changed = {name for name in set(before) | set(after) if before.get(name) != after.get(name)}
    outside = sorted(
        name for name in changed if queue_dir not in (tmp_path / name).resolve().parents
    )
    assert not outside, f"the duplicate audit wrote outside the review queue: {outside}"
    assert changed, "nothing changed at all, so this test is not exercising the write"
    assert _database_rows(cfg.library.db_path) == rows_before


#: The name the lock probe writes. Named once so the proof below and the tidy-up
#: after it cannot drift apart into a file left in a library on a failing run.
_LOCK_PROBE = "scratch.tmp"


def _directories_refusing_a_write(directories: list[Path]) -> list[Path]:
    """Which of these directories REFUSE a new file, measured rather than assumed."""
    refused: list[Path] = []
    for directory in directories:
        probe = directory / _LOCK_PROBE
        try:
            probe.write_bytes(b"the lock has to be real")
        except OSError:
            refused.append(directory)
        else:
            probe.unlink(missing_ok=True)
    return refused


def test_the_lock_probe_sees_a_directory_that_was_not_locked(tmp_path):
    """The INSTRUMENT, checked before the read-only proof concludes from it."""
    shut, open_ = tmp_path / "shut", tmp_path / "open"
    shut.mkdir()
    open_.mkdir()
    mode = shut.stat().st_mode
    shut.chmod(0o555)
    try:
        assert _directories_refusing_a_write([shut, open_]) == [shut]
        assert _directories_refusing_a_write([open_]) == []
        assert not list(open_.iterdir())
    finally:
        shut.chmod(mode)


def test_every_report_runs_with_the_library_directory_read_only(cfg, library_on_disk, tmp_path):
    """READ ONLY, proved by taking the permission away rather than by watching."""
    music = cfg.library.root / "Music"
    database = cfg.library.db_path
    # The decision store lives under the library root, so the directory it writes
    # into has to exist before the root is locked. Creating it here is what lets
    # the lock cover the library ROOT rather than only the audio folder, which is
    # where a report writing ``library/.cratekit-sightings`` would have landed.
    with review.open_store(cfg):
        pass
    locked = [library_on_disk, database, *sorted(music.glob("*.flac"))]
    directories = [cfg.library.root, music, database.parent]
    modes = {path: path.stat().st_mode for path in [*directories, *locked]}
    scratches = [directory / _LOCK_PROBE for directory in directories]
    for path in locked:
        path.chmod(0o444)
    for path in directories:
        path.chmod(0o555)
    try:
        refused = _directories_refusing_a_write(directories)
        assert refused == directories, (
            f"only {refused} refused a write after chmod 0o555, so this proof "
            f"would pass without proving anything for the rest. It needs an "
            f"ordinary user and a filesystem that honours permission bits; "
            f"running as root defeats it. There is deliberately no skip here, "
            f"because a read-only claim that quietly stops being checked is the "
            f"defect this unit is."
        )

        stamped = sorted(music.glob("*.flac"))[0]
        moved = stamped.stat().st_mtime_ns + 1_000_000_000
        try:
            os.utime(stamped, ns=(moved, moved))
            utimed = stamped.stat().st_mtime_ns == moved
            stamped.touch()
            touched = stamped.stat().st_mtime_ns != moved
        except OSError:
            utimed = touched = False
        assert utimed and touched, (
            "a bare stamp on a locked file was refused after all, so this lock "
            "does cover the shape a sighting ledger reaches for and the docstring "
            "above now says something false about its own limit. The digest is "
            "what covers that act; this says so out loud so the two proofs are "
            "not read as one."
        )

        view = export.read_export_file(library_on_disk)
        report = aging.intake_aging(
            view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
        )
        assert [group.display for group in report.expired] == ["phil_5_01_25"]
        assert [group.display for group in report.undated] == ["white labels"]

        with review.open_store(cfg) as store:
            audited = duplicates.audit_and_offer(view, store, template=TEMPLATE)
        assert len(audited.items) == 1
        assert audited.items[0].payload["copies"] == 2
    finally:
        # This restore is also the chmod half of what the docstring above claims:
        # every one of these succeeds through the lock, on files and directories
        # the lock has already refused a write to, because a mode change needs
        # ownership rather than the write bit.
        for path, mode in modes.items():
            path.chmod(mode)
        # Only reachable when a lock did not hold, and the tree digest tests run
        # against their own temporary directories, so this is tidiness rather
        # than isolation. It is here because a file left behind by a failing
        # read-only proof is the one piece of evidence somebody debugging it
        # would most want to be sure came from the test.
        for scratch in scratches:
            scratch.unlink(missing_ok=True)


# The structural half: the package cannot write, whatever a test drives

#: Every top-level module the reports package may import, and every dotted target
#: inside this one. DERIVED FROM WHAT READING NEEDS.
ALLOWED_IMPORTS = frozenset(
    {
        "__future__",
        "collections",
        "collections.abc",
        "dataclasses",
        "datetime",
        "pathlib",
        "re",
        "typing",
        "cratekit.core.cause",
        "cratekit.core.config",
        "cratekit.core.exit_codes",
        "cratekit.core.locations",
        "cratekit.core.naming",
        "cratekit.core.review",
        "cratekit.core.taxonomy",
        "cratekit.write.rbxml",
    }
)

#: The package this allowlist governs. Named once and matched WITH A DOT
#: BOUNDARY, because the bare-prefix version of this test accepted every module
#: whose dotted name merely started with these characters. A sibling file
#: ``cratekit/modules/reports_ledger.py`` was importable from inside the package
#: on that reading AND sat outside the directory ``_report_modules`` walks, so
#: the private ignore ledger the countdown against this unit forbids by name
#: could have been written, imported, and called with both structural guards
#: green. The dot boundary is what the allowlist entries below already get right
#: through ``startswith(f"{allowed}.")``; only the self reference was loose.
REPORTS_PACKAGE = "cratekit.modules.reports"

#: Method names that mutate the filesystem and are not also ordinary methods on a
#: string, a mapping, or a sequence.
FILESYSTEM_MUTATIONS = frozenset(
    {
        # U254: the synced append beside the atomic writer, for a ledger that
        # grows a record at a time. Flat like its sibling, a name nothing else
        # carries.
        "append_durable_bytes",
        "atomic_write_bytes",
        "chmod",
        "hardlink_to",
        "lchmod",
        "mkdir",
        "rename",
        "rmdir",
        "rmtree",
        "symlink_to",
        "touch",
        "truncate",
        "unlink",
        "write_bytes",
        "write_text",
    }
)

#: The write surface the ALLOWLIST itself admits, spelled with the module a
#: caller has to reach it THROUGH.
QUALIFIED_MUTATIONS = frozenset(
    {
        "config._back_up_version",
        "config.exclusive_lock",
        # U298: the lock every state store shared, in its four forms. Each
        # creates the lock file, and the directory above it, when it is absent.
        "config.flock_exclusive",
        "config.held",
        "config.lock_now",
        "config.lock_within",
        "config.mkdir_private",
        "config._write_lock",
        "config.load",
        "config.load_from_path",
        "config.save",
        "config.update",
        "naming.claim_target",
        "backup_facts.record",
        "backup_facts.clear_outcome",
        "backup_facts.write_outcome",
        "rb_writer._candidate_app_paths",
        "rb_writer._loaded_config",
        "rb_writer._pins",
        "rb_writer.assert_app_version",
        "rb_writer.assert_binding_version",
        "rb_writer.assert_schema_version",
        "rb_writer.default_protected_snapshot_paths",
        # The disposable copy of the database from the residual finding "Setup
        # wrote no location prefix rule for rekordbox's renamed drive, and the
        # My Tags plan read clean over 9770 rows it could not resolve": it
        # creates a private temporary directory, copies the file set into it,
        # and removes the directory afterwards, and the read only handle over
        # it opens that copy. A report has no business making one, and a
        # report that read through the copy would be reading through a
        # writer, so both are named here rather than admitted.
        "rb_writer.disposable_copy",
        "rb_writer.read_only_copy",
        # U267: the organize report's one read handle opens the database at
        # its first read, so a report holding one opens through a writer, and
        # the reader's end of a read closes or releases that handle.
        "rb_writer.SharedRead",
        "rb_writer.done_reading",
        "rb_writer.integrity_ok",
        "rb_writer.live_db_path",
        "rb_writer.open_db",
        "rb_writer.pin_validated_on",
        "rb_writer.pinned_app_version",
        "rb_writer.pinned_db_version",
        "rb_writer.pinned_pyrekordbox",
        "rb_writer.prune_snapshots",
        "rb_writer.read_installed_app_version",
        "rb_writer.restore_from_snapshot",
        "rb_writer.snapshot_db",
        "rb_writer.snapshot_root",
        "rb_writer.write_lock_path",
        "rb_writer.write_session_lock",
        "reconcile._locked",
        # U298: the mode the convergence lock is held to, handed to
        # ``config.flock_exclusive`` as its hardening.
        "reconcile._own_only",
        "reconcile._write",
        "reconcile.close_marker",
        "reconcile.record_markers",
        "reconcile.retract_in_flight",
        "session._open_lock_file",
        "session._recorded",
        "session._write_holder",
        "session.abandon_orphaned_sessions",
        "session.assert_gates",
        "session.attach_capture",
        "session.close_session",
        "session.commit_sources",
        "session.mark_awaiting_import",
        "session.mark_import_verified",
        "session.open_session",
        "session.record_acknowledgment",
        "session.record_commit",
        "session.release_stale_lock",
        "session.resolve_unverified_session",
        "session.session_lock",
        "session.verify_commit",
        "session.write_record",
        "snapshot._chmod",
        "snapshot._harden",
        "snapshot._not_flushed",
        # The capture's manifest rewritten unverified before a room refusal.
        "snapshot._record_unverified",
        "snapshot._verify",
        "snapshot._write_manifest",
        "snapshot.capture",
        "tree_registry.flip",
        "tree_registry.record_cutover",
        "tree_registry.revert_cutover",
        "tree_registry.write",
        # U298: the one config load every verb's shell shares. It calls
        # ``config.load``, which writes the file back, so it is a writer by the
        # rule above, and a report is HANDED its configuration and loads none.
        "output.load_config",
    }
)

#: The modules ``QUALIFIED_MUTATIONS`` qualifies against, derived rather than
#: listed so a name added above brings its module with it.
_QUALIFYING_MODULES = frozenset(name.split(".", 1)[0] for name in QUALIFIED_MUTATIONS)

#: Characters in an ``open`` mode that mean the handle can write.
_WRITING_MODES = frozenset({"w", "a", "x", "+"})

#: How many dotted parts make a PACKAGE rather than a module, for reading a
#: ``from X import y``. ``cratekit`` and ``cratekit.<subpackage>``, plus the
#: stdlib's own one and two level packages.
_PACKAGE_DEPTH = 2


#: What a dynamic import spells when its argument is not a literal this can read.
#: It is deliberately not a module path, so ``_permitted`` can never match it: a
#: computed import is exactly how a name check is walked past, and the guard's
#: answer to something it cannot read is the same as its answer to ``open`` with
#: a computed mode.
_COMPUTED_IMPORT = "<computed import>"


def _is_package(dotted: str, root: Path = SRC_ROOT) -> bool:
    """Whether a dotted path names a DIRECTORY in this repository's source tree."""
    return root.joinpath(*dotted.split(".")).is_dir()


def _package_of(module: str, root: Path = SRC_ROOT) -> str:
    """The package a module's relative imports resolve against."""
    if root.joinpath(*module.split(".")).is_dir():
        return module
    return module.rsplit(".", 1)[0]


def _resolved_imports(source: str, module: str, root: Path = SRC_ROOT) -> list[str]:
    """Every module ``source`` depends on, as absolute dotted paths."""
    package = _package_of(module, root)
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = package.split(".")
                base = ".".join([*parts[: len(parts) - node.level + 1], *([base] if base else [])])
            if len(base.split(".")) <= _PACKAGE_DEPTH or _is_package(base, root):
                found += [f"{base}.{alias.name}" for alias in node.names]
            else:
                found.append(base)
        elif isinstance(node, ast.Call) and getattr(node.func, "id", "") == "__import__":
            first = node.args[0] if node.args else None
            found.append(
                first.value
                if isinstance(first, ast.Constant) and isinstance(first.value, str)
                else _COMPUTED_IMPORT
            )
    return found


def _permitted(target: str) -> bool:
    """Whether one resolved import is inside the allowlist or inside this package."""
    if target == REPORTS_PACKAGE or target.startswith(f"{REPORTS_PACKAGE}."):
        return True
    return any(target == allowed or target.startswith(f"{allowed}.") for allowed in ALLOWED_IMPORTS)


def forbidden_imports(source: str, module: str) -> list[str]:
    """Every dependency the reports package is not allowed to have."""
    return [target for target in _resolved_imports(source, module) if not _permitted(target)]


def filesystem_mutations(source: str) -> list[str]:
    """Every call in ``source`` that could change a file, with its line."""
    tree = ast.parse(source)
    modules, direct = _writer_bindings(tree)
    return mutations_in(tree, modules=modules, direct=direct)


class _Instance(NamedTuple):
    """Which local name, in one scope, is an instance of which class."""

    name: str = ""
    root: str = ""


#: What an instance of a class renders as inside the binding table. Written as a
#: suffix on the class path rather than as the parameter's own spelling, because
#: the parameter's spelling is the thing that is not stable.
_INSTANCE = "::self"


def _receiver_key(node: ast.AST | None, instance: _Instance = _Instance()) -> str:
    """A canonical spelling of one receiver EXPRESSION, or "" when it has none."""
    if isinstance(node, ast.Name):
        return instance.root if instance.name == node.id else node.id
    if isinstance(node, ast.Attribute):
        base = _receiver_key(node.value, instance)
        return f"{base}.{node.attr}" if base else ""
    if isinstance(node, ast.Subscript):
        base = _receiver_key(node.value, instance)
        if base and isinstance(node.slice, ast.Constant):
            return f"{base}[{node.slice.value!r}]"
        return ""
    if isinstance(node, ast.Call):
        base = _receiver_key(node.func, instance)
        return f"{base}()" if base and not node.args and not node.keywords else ""
    return ""


#: The node types that OPEN A SCOPE, which is what makes the binding table below
#: lexical rather than a flat sweep of the file.
_SCOPES = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Lambda,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
)


def _memoized_on_node(walk):
    """Keep a walk's answer on the node it was asked of: no tree is mutated after
    it is parsed, and the audit asks the same scope the same question many times.
    """
    key = f"_cached_{walk.__name__}"

    def cached(node: ast.AST) -> tuple[ast.AST, ...]:
        found = node.__dict__.get(key)
        if found is None:
            found = tuple(walk(node))
            setattr(node, key, found)
        return found

    return cached


def _walk_scope(node: ast.AST):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPES):
            continue
        yield child
        yield from _walk_scope(child)


def _walk_nested(node: ast.AST):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPES):
            yield child
        else:
            yield from _walk_nested(child)


#: Every node inside one scope, stopping where a nested scope begins.
_scope_nodes = _memoized_on_node(_walk_scope)
#: Every function, lambda and comprehension directly inside one scope.
_nested_scopes = _memoized_on_node(_walk_nested)


#: The statement fields a single run can SKIP ENTIRELY, by the node that holds
#: them. ``finalbody`` is deliberately absent: a ``finally`` block runs on every
#: path there is, so a binding written in one is not optional at all.
_BRANCHED_FIELDS = ("body", "orelse", "handlers", "cases")

_BRANCHING = (
    ast.If,
    ast.Try,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.Match,
    ast.match_case,
)


def _branched(scope: ast.AST) -> frozenset[int]:
    """Every statement in one scope a single run can skip, by node identity."""
    found: set[int] = set()
    for holder in _scope_nodes(scope):
        if not isinstance(holder, _BRANCHING):
            continue
        for field in _BRANCHED_FIELDS:
            for one in getattr(holder, field, None) or []:
                found.update(id(inner) for inner in ast.walk(one))
    return frozenset(found)


def _chains_to_base(scope: ast.AST) -> bool:
    """Whether one scope UNCONDITIONALLY runs a base class's initializer."""
    skippable = _branched(scope)
    for child in _scope_nodes(scope):
        if id(child) in skippable or not isinstance(child, ast.Call):
            continue
        if isinstance(child.func, ast.Attribute) and child.func.attr == "__init__":
            return True
    return False


def _alternatives(node: ast.AST | None):
    """The values ONE expression can evaluate to, when it is a choice between some."""
    if isinstance(node, ast.BoolOp):
        for one in node.values:
            yield from _alternatives(one)
    elif isinstance(node, ast.IfExp):
        yield from _alternatives(node.body)
        yield from _alternatives(node.orelse)
    elif node is not None:
        yield node


def _restored_attributes(scope: ast.AST, instance: _Instance) -> dict[str, str]:
    """Each instance attribute one scope DELETES, with the class spelling under it."""
    found: dict[str, str] = {}
    for child in _scope_nodes(scope):
        if not isinstance(child, ast.Delete):
            continue
        for target in child.targets:
            key = _receiver_key(target, instance)
            root, _, attribute = key.rpartition(".")
            if root.endswith(_INSTANCE):
                found[key] = f"{root[: -len(_INSTANCE)]}.{attribute}"
    return found


def _target_names(targets) -> set[str]:
    """Every BARE NAME an assignment target list binds, unpacking as it goes."""
    found: set[str] = set()
    for target in targets:
        if isinstance(target, ast.Name):
            found.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            found |= _target_names(target.elts)
        elif isinstance(target, ast.Starred):
            found |= _target_names([target.value])
    return found


def _bound_here(node: ast.AST) -> set[str]:
    """The bare names ONE statement or expression binds in the scope it sits in."""
    if isinstance(node, ast.arguments):
        named = [*node.posonlyargs, *node.args, *node.kwonlyargs]
        named += [one for one in (node.vararg, node.kwarg) if one is not None]
        return {one.arg for one in named}
    if isinstance(node, ast.Assign):
        return _target_names(node.targets)
    if isinstance(node, (ast.AugAssign, ast.AnnAssign, ast.NamedExpr)):
        return _target_names([node.target])
    if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
        return _target_names([node.target])
    if isinstance(node, ast.withitem):
        return _target_names([node.optional_vars]) if node.optional_vars else set()
    if isinstance(node, ast.ExceptHandler):
        return {node.name} if node.name else set()
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return {(one.asname or one.name).split(".", 1)[0] for one in node.names}
    return set()


def _defined_here(node: ast.AST) -> frozenset[str]:
    """The names nested DEFINITIONS bind in the scope that holds them."""
    return frozenset(
        nested.name
        for nested in _nested_scopes(node)
        if isinstance(nested, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )


def _rebound_to_itself(node: ast.AST, instance: _Instance = _Instance()) -> frozenset[str]:
    """The receiver keys one assignment binds to the value they already hold.

    ``Keeper = Keeper`` cannot change what the name is bound to, unlike
    ``Keeper = dataclass(Keeper)``, which the residual
    "A class rebound after its own definition is no longer reachable by name"
    files as undecidable.
    """
    if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
        return frozenset()
    sources = {
        key for key in (_receiver_key(one, instance) for one in _alternatives(node.value)) if key
    }
    if not sources:
        return frozenset()
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return frozenset(
        key for key in (_receiver_key(one, instance) for one in targets) if key in sources
    )


def _names_taken(node: ast.AST) -> frozenset[str]:
    """Every bare name one scope binds to something of its OWN."""
    taken = set(_defined_here(node))
    for child in _scope_nodes(node):
        taken |= _bound_here(child) - _rebound_to_itself(child)
    return frozenset(taken)


class _Namespace(NamedTuple):
    """A TYPE'S ATTRIBUTE MAPPING, as a thing a name can be BOUND to."""

    owner: str = ""


class _Class(NamedTuple):
    """ONE CLASS DEFINITION, as a thing a name can be BOUND to."""

    key: str = ""
    bases: tuple[str, ...] = ()


#: What any receiver key in the binding table can be bound to.
_Bound = str | _Namespace | _Class


#: What separates a class's NAME from its definition site in a class key.
_DEFINED = "#"


def _class_key(node: ast.ClassDef) -> str:
    """The identity of ONE class definition, which is where it is written."""
    return f"{node.name}{_DEFINED}{node.lineno}"


def _sequences(scope: ast.AST):
    """Every STATEMENT LIST one scope holds, stopping where a nested scope begins."""
    for holder in (scope, *_scope_nodes(scope)):
        for _, value in ast.iter_fields(holder):
            if isinstance(value, list) and any(isinstance(one, ast.stmt) for one in value):
                yield value


def _alternate_classes(scope: ast.AST) -> dict[str, tuple[str, ...]]:
    """Same-named class definitions in one scope that NO SINGLE RUN reaches twice."""
    blocks: dict[int, int] = {}
    for block in _sequences(scope):
        for one in block:
            blocks[id(one)] = id(block)
    order: dict[str, list[ast.ClassDef]] = {}
    for nested in _nested_scopes(scope):
        if isinstance(nested, ast.ClassDef):
            order.setdefault(nested.name, []).append(nested)
    found: dict[str, tuple[str, ...]] = {}
    for entries in order.values():
        settled = entries[-1]
        others = tuple(
            _class_key(one)
            for one in entries[:-1]
            if blocks.get(id(one)) != blocks.get(id(settled))
        )
        if others:
            found[_class_key(settled)] = others
    return found


def _mapping_operands(node: ast.AST | None):
    """Every sub-expression an expression could carry a MAPPING out of."""
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            yield node.func.value
        yield from node.args
        yield from (word.value for word in node.keywords)
    elif isinstance(node, ast.BinOp):
        yield node.left
        yield node.right
    elif isinstance(node, ast.Dict):
        yield from (value for key, value in zip(node.keys, node.values) if key is None)


def _namespace_of(
    node: ast.AST | None, table: dict[str, _Bound], instance: _Instance
) -> _Namespace | None:
    """The attribute mapping one expression IS, or None."""
    if isinstance(node, ast.Attribute) and node.attr == "__dict__":
        return _Namespace(_receiver_key(node.value, instance))
    if (
        isinstance(node, ast.Call)
        and getattr(node.func, "id", "") == "vars"
        and len(node.args) == 1
        and not node.keywords
    ):
        return _Namespace(_receiver_key(node.args[0], instance))
    for part in _mapping_operands(node):
        carried = _bound_value(part, table, instance)
        if isinstance(carried, _Namespace):
            return carried
    return None


def _bound_value(
    node: ast.AST | None,
    table: dict[str, _Bound],
    instance: _Instance = _Instance(),
) -> _Bound:
    """What one expression evaluates to in the table, or the empty string."""
    if isinstance(node, ast.IfExp):
        return _bound_value(node.body, table, instance) or _bound_value(
            node.orelse, table, instance
        )
    if isinstance(node, ast.BoolOp):
        for one in node.values:
            found = _bound_value(one, table, instance)
            if found:
                return found
        return ""
    space = _namespace_of(node, table, instance)
    if space is not None:
        return space
    if isinstance(node, ast.Attribute):
        reached = _bound_value(node.value, table, instance)
        if isinstance(reached, _Class):
            found = table.get(f"{reached.key}.{node.attr}", "")
            if found:
                return found
    key = _receiver_key(node, instance)
    return table.get(key, "") if key else ""


def _class_of(node: ast.ClassDef, table: dict[str, _Bound], instance: _Instance) -> _Class:
    """One class definition's identity, with its BASES resolved through the table."""
    return _Class(
        _class_key(node),
        tuple(
            found.key
            for found in (_bound_value(one, table, instance) for one in node.bases)
            if isinstance(found, _Class)
        ),
    )


def _elements(value: ast.AST | None):
    """Every constant-addressed element of a container literal, index and node."""
    if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
        return list(enumerate(value.elts))
    if isinstance(value, ast.Dict):
        return [
            (key.value, element)
            for key, element in zip(value.keys, value.values)
            if isinstance(key, ast.Constant)
        ]
    return []


def _element_bindings(
    target: str,
    value: ast.AST | None,
    modules: dict[str, _Bound],
    instance: _Instance,
) -> dict[str, _Bound]:
    """What a container literal binds, element by element and NESTED."""
    found: dict[str, _Bound] = {}
    for index, element in _elements(value):
        key = f"{target}[{index!r}]"
        owner = _bound_value(element, modules, instance)
        if owner:
            found[key] = owner
        found.update(_element_bindings(key, element, modules, instance))
    return found


def _iterated_values(
    node: ast.AST, modules: dict[str, _Bound], instance: _Instance
) -> list[_Bound]:
    """Every admitted module or namespace a loop could hand its target."""
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        found = [_bound_value(element, modules, instance) for element in node.elts]
        return [owner for owner in found if owner]
    key = _receiver_key(node, instance)
    if not key:
        return []
    return [owner for bound, owner in modules.items() if bound.startswith(f"{key}[")]


def _default_bindings(
    args: ast.arguments, modules: dict[str, _Bound], instance: _Instance
) -> dict[str, _Bound]:
    """Parameters whose DEFAULT is an admitted module or a namespace."""
    found: dict[str, _Bound] = {}
    positional = [*args.posonlyargs, *args.args]
    supplied = positional[len(positional) - len(args.defaults) :]
    pairs = [*zip(supplied, args.defaults), *zip(args.kwonlyargs, args.kw_defaults)]
    for parameter, default in pairs:
        owner = _bound_value(default, modules, instance) if default is not None else ""
        if owner:
            found[parameter.arg] = owner
    return found


def _returned_value(node: ast.AST, modules: dict[str, _Bound], instance: _Instance) -> _Bound:
    """What a function hands back, so ``_mod().save(cfg)`` resolves."""
    for child in _scope_nodes(node):
        if isinstance(child, ast.Return) and child.value is not None:
            owner = _bound_value(child.value, modules, instance)
            if owner:
                return owner
    return ""


def _assigned(
    target: ast.AST,
    value: ast.AST | None,
    modules: dict[str, _Bound],
    instance: _Instance,
) -> dict[str, _Bound]:
    """The admitted modules one assignment target takes, keyed by receiver."""
    if isinstance(target, (ast.Tuple, ast.List)):
        if isinstance(value, (ast.Tuple, ast.List)) and len(target.elts) == len(value.elts):
            found: dict[str, _Bound] = {}
            for one, element in zip(target.elts, value.elts):
                found.update(_assigned(one, element, modules, instance))
            return found
        return {}
    key = _receiver_key(target, instance)
    if not key:
        return {}
    found = {key: _bound_value(value, modules, instance)}
    found.update(_element_bindings(key, value, modules, instance))
    return found


def _binds(
    node: ast.AST, modules: dict[str, _Bound], instance: _Instance
) -> tuple[dict[str, _Bound], frozenset[str]]:
    """Every binding ONE statement makes, and the bare WRITER names it imports."""
    if isinstance(node, ast.Import):
        found: dict[str, _Bound] = {}
        for alias in node.names:
            short = alias.name.rsplit(".", 1)[-1]
            if short in _QUALIFYING_MODULES:
                found[alias.asname or alias.name] = short
        return found, frozenset()
    if isinstance(node, ast.ImportFrom):
        found, direct = {}, set()
        base = (node.module or "").rsplit(".", 1)[-1]
        for alias in node.names:
            if alias.name == "*":
                direct |= _writer_names_of(node.module or "")
            elif alias.name in _QUALIFYING_MODULES:
                found[alias.asname or alias.name] = alias.name
            elif f"{base}.{alias.name}" in QUALIFIED_MUTATIONS:
                direct.add(alias.asname or alias.name)
        return found, frozenset(direct)
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        found = {}
        for target in targets:
            found.update(_assigned(target, node.value, modules, instance))
        return found, frozenset()
    if isinstance(node, ast.NamedExpr):
        return _assigned(node.target, node.value, modules, instance), frozenset()
    if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
        key = _receiver_key(node.target, instance)
        if not key:
            return {}, frozenset()
        iterated = _iterated_values(node.iter, modules, instance)
        return ({key: iterated[0]} if iterated else {}), frozenset()
    return {}, frozenset()


def _scope_own_bindings(
    scope: ast.AST, modules: dict[str, _Bound], instance: _Instance
) -> tuple[dict[str, _Bound], frozenset[str]]:
    """What one scope binds for itself, resolved against what it can already see."""
    objects: dict[str, _Bound] = {}
    settled: dict[str, _Bound] = {}
    direct: set[str] = set()
    chained = _chains_to_base(scope)
    while True:
        before = dict(objects), dict(settled)
        table = {**modules, **objects, **settled}
        attempts: dict[str, list[_Bound]] = {}
        skippable = _branched(scope)
        for child in _scope_nodes(scope):
            found, names = _binds(child, table, instance)
            direct |= names
            idle = _rebound_to_itself(child, instance)
            optional = id(child) in skippable
            for key, owner in found.items():
                # A SKIPPED VETO ONLY COUNTS WHEN SOMETHING ELSE STILL SUPPLIES
                # THE KEY on the path that skipped it. For a NAME that is always
                # so, because the statement that bound it ran. For an OBJECT key
                # it is so in exactly two cases: the attribute is already in this
                # scope's table, which is what a class body binding it does, or
                # this scope chains to a base initializer that binds it. Anything
                # else and the arm that skipped the override reaches an attribute
                # that was never created, so the veto stands.
                supplied = key.isidentifier() or chained or bool(table.get(key))
                if key in idle or (optional and not owner and supplied):
                    continue
                if key.isidentifier():
                    attempts.setdefault(key, []).append(owner)
                elif owner:
                    objects[key] = owner
                else:
                    objects.setdefault(key, "")
            for key in idle:
                # WHAT THE KEY HELD, and what the statement could still evaluate
                # to when it held nothing this pass could read. ``alias = alias or
                # config`` keeps its own value on one path and the module on the
                # other, and reading only the first would lose the module.
                held = table.get(key, "") or found.get(key, "")
                if not held:
                    continue
                if key.isidentifier():
                    attempts.setdefault(key, []).append(held)
                else:
                    objects[key] = held
            if optional:
                continue
            for name in _bound_here(child) - set(found) - idle:
                attempts.setdefault(name, []).append("")
        made = {
            nested.name: _class_of(nested, table, instance)
            for nested in _nested_scopes(scope)
            if isinstance(nested, ast.ClassDef)
        }
        for name in _defined_here(scope):
            attempts.setdefault(name, []).append(made.get(name, ""))
        settled = {
            key: owners[0] if all(owners) and len(set(owners)) == 1 else ""
            for key, owners in attempts.items()
        }
        if (objects, settled) == before:
            return {**objects, **settled}, frozenset(direct)


def _visible_bindings(
    node: ast.AST,
    modules: dict[str, _Bound],
    direct: frozenset[str],
    instance: _Instance = _Instance(),
) -> tuple[dict[str, _Bound], frozenset[str], dict[str, _Bound]]:
    """The bindings one scope really sees: inherited, shadowed, then its own."""
    taken = _names_taken(node)
    kept = {key: owner for key, owner in modules.items() if key not in taken}
    reachable = frozenset(name for name in direct if name not in taken)
    own, own_direct = _scope_own_bindings(node, kept, instance)
    kept.update(own)
    args = getattr(node, "args", None)
    if isinstance(args, ast.arguments):
        defaults = _default_bindings(args, modules, instance)
        kept.update(defaults)
        own = {**own, **defaults}
    return kept, reachable | own_direct, own


def _method_instance(node: ast.AST, owner: str) -> _Instance:
    """Which parameter of one method is the instance, and what it renders as."""
    if not owner or not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return _Instance()
    kinds = {one.id for one in node.decorator_list if isinstance(one, ast.Name)}
    positional = [*node.args.posonlyargs, *node.args.args]
    if not positional or "staticmethod" in kinds:
        return _Instance()
    if "classmethod" in kinds:
        return _Instance(positional[0].arg, owner)
    return _Instance(positional[0].arg, f"{owner}{_INSTANCE}")


def _attachments(scope: ast.AST) -> dict[str, str]:
    """Every function one scope ATTACHES to a class it defines, by ``Row.go = _go``."""
    classes = {
        nested.name: _class_key(nested)
        for nested in _nested_scopes(scope)
        if isinstance(nested, ast.ClassDef)
    }
    found: dict[str, str] = {}
    for node in _scope_nodes(scope):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Name):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id in classes
            ):
                found[node.value.id] = classes[target.value.id]
    return found


def _member_scope(
    scope: ast.AST, owner: str, instance: _Instance, nested: ast.AST
) -> tuple[str, _Instance]:
    """The class identity and instance one NESTED scope is read under."""
    if isinstance(nested, ast.ClassDef):
        return _class_key(nested), instance
    if isinstance(scope, ast.ClassDef):
        return owner, _method_instance(nested, owner)
    attached = _attachments(scope).get(getattr(nested, "name", ""), "")
    if attached:
        return attached, _method_instance(nested, attached)
    if instance.name and instance.name in _names_taken(nested):
        return owner, _Instance()
    return owner, instance


def _handed_to_members(scope: ast.AST, inside, outside):
    """What a nested scope is handed: the parent's view, or the parent's OWN INPUT."""
    return outside if isinstance(scope, ast.ClassDef) else inside


def _walk_bindings(
    scope: ast.AST,
    inherited: dict[str, _Bound],
    reachable: frozenset[str],
    objects: dict[str, _Bound],
    families: dict[str, tuple[str, ...]],
    alternates: dict[str, tuple[str, ...]],
    faint: set[str],
    owner: str = "",
    instance: _Instance = _Instance(),
) -> tuple[dict[str, _Bound], frozenset[str]]:
    """One scoped pass over a tree, collecting every OBJECT binding it DECLARES."""
    visible, visible_direct, own = _visible_bindings(
        scope, {**inherited, **objects}, reachable, instance
    )
    for key, value in own.items():
        if not key.isidentifier():
            _record(objects, key, value, faint)
    for key, through in _restored_attributes(scope, instance).items():
        _record(objects, key, objects.get(through, ""), faint)
    if isinstance(scope, ast.ClassDef) and owner:
        for key, value in own.items():
            if key.isidentifier():
                _record(objects, f"{owner}.{key}", value, faint)
                _record(objects, f"{owner}{_INSTANCE}.{key}", value, faint, weak=True)
    handed, handed_direct = _handed_to_members(
        scope, (visible, visible_direct), (dict(inherited), reachable)
    )
    alternates.update(_alternate_classes(scope))
    for nested in _nested_scopes(scope):
        member, member_instance = _member_scope(scope, owner, instance, nested)
        if isinstance(nested, ast.ClassDef):
            families[member] = _class_of(nested, visible, instance).bases
        nested_visible, _ = _walk_bindings(
            nested,
            handed,
            handed_direct,
            objects,
            families,
            alternates,
            faint,
            member,
            member_instance,
        )
        if isinstance(nested, (ast.FunctionDef, ast.AsyncFunctionDef)):
            returned = _returned_value(nested, nested_visible, member_instance)
            if returned:
                root = f"{owner}{_INSTANCE}." if isinstance(scope, ast.ClassDef) else ""
                objects[f"{root}{nested.name}()"] = returned
    return visible, visible_direct


def _record(
    objects: dict[str, _Bound],
    key: str,
    value: _Bound,
    faint: set[str],
    *,
    weak: bool = False,
) -> None:
    """Write one declared attribute key: resolved wins, unresolved only fills."""
    if weak:
        objects[key] = value
        faint.add(key)
        return
    if value or key not in objects or key in faint:
        objects[key] = value
    faint.discard(key)


def _related(start: str, families: dict[str, tuple[str, ...]], *, upward: bool) -> list[str]:
    """One class and the classes an attribute lookup on it can reach, NEAREST FIRST."""
    seen, order, queue = {start}, [start], [start]
    while queue:
        one = queue.pop(0)
        if upward:
            step: tuple[str, ...] = families.get(one, ())
        else:
            step = tuple(key for key, bases in families.items() if one in bases)
        for other in step:
            if other not in seen:
                seen.add(other)
                order.append(other)
                queue.append(other)
    return order


def _inherited_attributes(
    declared: dict[str, _Bound],
    families: dict[str, tuple[str, ...]],
    alternates: dict[str, tuple[str, ...]],
) -> dict[str, _Bound]:
    """Every attribute key a class REACHES, from the keys its family DECLARED."""
    found: dict[str, _Bound] = {}
    for one in families:
        upward = _related(one, families, upward=True)
        for other in upward:
            _carry(found, declared, other, one, f"{other}.", overriding=True)
        for other in upward:
            _carry(found, declared, other, one, f"{other}{_INSTANCE}.", overriding=True)
        for other in _related(one, families, upward=False):
            if other not in upward:
                _carry(found, declared, other, one, f"{other}{_INSTANCE}.", overriding=False)
    for one, others in alternates.items():
        for other in others:
            _carry(found, declared, other, one, f"{other}.", overriding=False)
    return found


def _carry(
    found: dict[str, _Bound],
    declared: dict[str, _Bound],
    source: str,
    target: str,
    prefix: str,
    *,
    overriding: bool,
) -> None:
    """Copy one class's declared keys onto another class's root, nearest wins."""
    for key, value in declared.items():
        if not key.startswith(prefix) or (not value and not overriding):
            continue
        found.setdefault(f"{target}{key[len(source) :]}", value)


def _global_aliases(
    modules: dict[str, _Bound],
) -> dict[str, _Bound]:
    """``globals()["config"]``, which is the module reached without its name."""
    return {f"globals()[{name!r}]": value for name, value in modules.items() if name.isidentifier()}


def _writer_bindings(
    tree: ast.AST,
) -> tuple[dict[str, _Bound], frozenset[str]]:
    """Receivers bound to an admitted module, and names bound to a writer itself."""
    declared: dict[str, _Bound] = {}
    families: dict[str, tuple[str, ...]] = {}
    alternates: dict[str, tuple[str, ...]] = {}
    faint: set[str] = set()
    reached: dict[str, _Bound] = {}
    while True:
        before = dict(declared), dict(families)
        names, direct = _walk_bindings(
            tree, reached, frozenset(), declared, families, alternates, faint
        )
        reached = _inherited_attributes(declared, families, alternates)
        if (declared, families) == before:
            return {
                **reached,
                **declared,
                **names,
                **_global_aliases(names),
            }, direct


def _imported_modules(tree: ast.AST) -> frozenset[str]:
    """Every name an ``import X`` statement binds to a MODULE."""
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.asname or alias.name.split(".", 1)[0])
    return frozenset(found)


def _receiver_module(node: ast.AST, modules: dict[str, _Bound], instance: _Instance) -> str:
    """Which admitted module a receiver was BOUND to, or the empty string."""
    found = _bound_value(node, modules, instance)
    return found if isinstance(found, str) else ""


def _writer_names_of(dotted: str) -> frozenset[str]:
    """The qualified writers one module's OWN bare names spell."""
    short = dotted.rsplit(".", 1)[-1]
    return frozenset(
        name.split(".", 1)[1] for name in QUALIFIED_MUTATIONS if name.split(".", 1)[0] == short
    )


def _namespace_reads(
    space: _Namespace,
    wanted: ast.AST | None,
    modules: dict[str, _Bound],
    instance: _Instance,
    *,
    reflection: bool,
) -> str | None:
    """What one lookup INTO a type's attribute mapping reports, or None."""
    if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):
        return "<a key this cannot read>" if reflection else None
    owner = modules.get(space.owner, "") if space.owner else ""
    owner = owner if isinstance(owner, str) else ""
    named = wanted.value in FILESYSTEM_MUTATIONS or (
        owner and f"{owner}.{wanted.value}" in QUALIFIED_MUTATIONS
    )
    return repr(wanted.value) if named else None


def _reflective_call(node: ast.AST) -> bool:
    """Whether one call is a reflective attribute read, however it is spelled."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    return name in _REFLECTIVE_READERS


def _handed_over(node: ast.AST | None):
    """Every reflective read one expression hands straight to whatever takes it."""
    if _reflective_call(node):
        yield node
    elif isinstance(node, ast.IfExp):
        yield from _handed_over(node.body)
        yield from _handed_over(node.orelse)


def _stored(node: ast.AST):
    """Every (receiver key, value) pair one statement stores."""
    if isinstance(node, ast.Assign):
        return [
            (_receiver_key(target), node.value) for target in node.targets if _receiver_key(target)
        ]
    if isinstance(node, (ast.AnnAssign, ast.NamedExpr)) and node.value is not None:
        key = _receiver_key(node.target)
        return [(key, node.value)] if key else []
    return []


def _called_keys(tree: ast.AST) -> frozenset[str]:
    """Every receiver spelling this file CALLS, wherever in the file it calls it."""
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            key = _receiver_key(node.func)
            if key:
                found.add(key)
        for decorator in getattr(node, "decorator_list", []):
            key = _receiver_key(decorator)
            if key:
                found.add(key)
    return frozenset(found)


def _invoked_results(tree: ast.AST) -> frozenset[str]:
    """Every callee whose RETURNED VALUE this file then calls, as in ``w(p)(d)``."""
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Call):
            key = _receiver_key(node.func.func)
            if key:
                found.add(key)
    return frozenset(found)


def _invoked_reads(tree: ast.AST) -> frozenset[int]:
    """Every reflective read in ``tree`` whose RESULT is called somewhere."""
    keys = _called_keys(tree)
    returned = _invoked_results(tree)
    found: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for read in _handed_over(node.func):
                found.add(id(read))
            if isinstance(node.func, ast.Call):
                supplied = [
                    *node.func.args,
                    *(keyword.value for keyword in node.func.keywords),
                ]
                for argument in supplied:
                    for read in _handed_over(argument):
                        found.add(id(read))
            if isinstance(node.func, ast.Subscript) and isinstance(node.func.slice, ast.Constant):
                for index, element in _elements(node.func.value):
                    if index == node.func.slice.value:
                        for read in _handed_over(element):
                            found.add(id(read))
        for decorator in getattr(node, "decorator_list", []):
            for read in _handed_over(decorator):
                found.add(id(read))
        for key, value in _stored(node):
            if key in keys:
                for read in _handed_over(value):
                    found.add(id(read))
            for index, element in _elements(value):
                if f"{key}[{index!r}]" in keys:
                    for read in _handed_over(element):
                        found.add(id(read))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in returned or f"{node.name}()" in keys:
                for child in _scope_nodes(node):
                    if isinstance(child, ast.Return):
                        for read in _handed_over(child.value):
                            found.add(id(read))
    return frozenset(found)


def mutations_in(
    tree: ast.AST,
    *,
    reflection: bool = True,
    modules: dict[str, _Bound] | None = None,
    direct: frozenset[str] = frozenset(),
    invoked: frozenset[int] | None = None,
    libraries: frozenset[str] | None = None,
    owner: str = "",
    instance: _Instance = _Instance(),
) -> list[str]:
    """The five rules above, applied to any node rather than to a whole module."""
    if invoked is None:
        invoked = _invoked_reads(tree)
    if libraries is None:
        libraries = _imported_modules(tree)
    resolved, reachable, _ = _visible_bindings(tree, dict(modules or {}), direct, instance)
    found: list[str] = []
    for node in _scope_nodes(tree):
        if isinstance(node, ast.Attribute):
            # The ATTRIBUTE rather than the call around it, so a bound method
            # captured now and called later is caught at the point it is
            # reached. A called one lands here too and only here, because the
            # call branch below deliberately checks a bare name only.
            if node.attr in FILESYSTEM_MUTATIONS:
                found.append(f"line {node.lineno}: {node.attr}")
            else:
                holder = _receiver_module(node.value, resolved, instance)
                if holder and f"{holder}.{node.attr}" in QUALIFIED_MUTATIONS:
                    found.append(f"line {node.lineno}: {holder}.{node.attr}")
        elif isinstance(node, ast.Subscript):
            # Rule 5, with the receiver read THROUGH THE TABLE. ``table =
            # vars(Path)`` followed by ``table["write_text"](p, d)`` is the same
            # two-line refactor ``alias = config`` is, and reading the receiver
            # inline saw neither line. Reported on the subscript rather than on a
            # call around it, on the same terms rule 1 reads an attribute: bound
            # now and called later still writes.
            space = _bound_value(node.value, resolved, instance)
            if isinstance(space, _Namespace):
                said = _namespace_reads(
                    space, node.slice, resolved, instance, reflection=reflection
                )
                if said is not None:
                    found.append(f"line {node.lineno}: [{said}]")
        elif isinstance(node, ast.Name) and node.id in reachable:
            # A writer imported off an admitted module, or one of that module's
            # own, reached with no receiver to read. Bound rather than called is
            # the same answer rule 1 gives for the same reason.
            found.append(f"line {node.lineno}: {node.id}")
        elif isinstance(node, ast.Call):
            found += _call_mutations(
                node,
                resolved,
                reflection=reflection,
                invoked=invoked,
                libraries=libraries,
                instance=instance,
            )
    handed, handed_direct = _handed_to_members(
        tree, (resolved, reachable), (dict(modules or {}), direct)
    )
    for nested in _nested_scopes(tree):
        member, member_instance = _member_scope(tree, owner, instance, nested)
        found += mutations_in(
            nested,
            reflection=reflection,
            modules=handed,
            direct=handed_direct,
            invoked=invoked,
            libraries=libraries,
            owner=member,
            instance=member_instance,
        )
    return found


def _call_mutations(
    node: ast.Call,
    resolved: dict[str, _Bound],
    *,
    reflection: bool,
    invoked: frozenset[int],
    libraries: frozenset[str],
    instance: _Instance = _Instance(),
) -> list[str]:
    """Rules 2, 3 and 4, which are the ones that read a CALL rather than a name."""
    func = node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    if isinstance(func, ast.Name) and name in FILESYSTEM_MUTATIONS:
        return [f"line {node.lineno}: {name}"]
    if isinstance(func, ast.Attribute):
        # RULE 5 ASKED RATHER THAN INDEXED. ``Path.__dict__.get("write_text")``
        # hands back the same function object the subscript does, and so does
        # ``vars(obj).pop(...)``. Any method of a namespace is read on the same
        # terms, because the narrowing that keeps this off ordinary code is the
        # RECEIVER being a type's attribute mapping, not the list of method names
        # somebody might use to reach into one.
        space = _bound_value(func.value, resolved, instance)
        if isinstance(space, _Namespace):
            said = _namespace_reads(
                space,
                node.args[0] if node.args else None,
                resolved,
                instance,
                reflection=reflection,
            )
            if said is not None:
                return [f"line {node.lineno}: {name}({said})"]
    if name == "open":
        library = _library_receiver(func, libraries)
        if library == "os":
            return (
                []
                if _os_open_reads(node)
                else [f"line {node.lineno}: os.open(flags this cannot read as a read)"]
            )
        mode = _open_mode(node, bound=not library and isinstance(func, ast.Attribute))
        if mode is None or _WRITING_MODES & set(mode):
            return [f"line {node.lineno}: open(mode={mode!r})"]
        return []
    if name == "replace" and len(node.args) == 1 and not node.keywords:
        return [f"line {node.lineno}: replace(one argument)"]
    if name not in _REFLECTIVE_READERS:
        return []
    receiver, wanted = _reflective_arguments(node, name)
    if wanted is None:
        return []
    if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):
        # The COMPUTED half. ``getattr`` is what an author reaches for, so inside
        # the governed package a computed one is reported whether or not its
        # result is called: there, an attribute this cannot read is the
        # violation. ``__getattribute__`` is not that. Written out by hand its
        # ordinary spelling is ``return super().__getattribute__(name)``, a
        # delegation that forwards the name the interpreter already asked for and
        # calls nothing, and reporting it was collateral the rule's own comment
        # said it did not have. So the dunder is read on the RESULT BEING CALLED
        # in both directions, which still catches
        # ``object.__getattribute__(p, n)(d)``.
        if id(node) in invoked or (reflection and name == "getattr"):
            return [f"line {node.lineno}: {name}(<computed attribute>)"]
        return []
    owner = _receiver_module(receiver, resolved, instance) if receiver is not None else ""
    if wanted.value in FILESYSTEM_MUTATIONS or (
        owner and f"{owner}.{wanted.value}" in QUALIFIED_MUTATIONS
    ):
        return [f"line {node.lineno}: {name}({wanted.value!r})"]
    return []


#: The builtin and the dunder that read an attribute by NAME. ``getattr`` is the
#: one anybody writes; ``__getattribute__`` is what it calls, it is reachable in
#: both a bound and an unbound spelling, and both of them write when they are
#: handed ``"write_text"``.
_REFLECTIVE_READERS = frozenset({"getattr", "__getattribute__"})


def _reflective_arguments(node: ast.Call, name: str) -> tuple[ast.AST | None, ast.AST | None]:
    """The receiver and the attribute NAME one reflective read was handed."""
    if len(node.args) >= 2:
        return node.args[0], node.args[1]
    if name == "__getattribute__" and node.args and isinstance(node.func, ast.Attribute):
        return node.func.value, node.args[0]
    return None, None


def _library_receiver(func: ast.AST, libraries: frozenset[str]) -> str:
    """The imported MODULE an attribute call was reached through, or ""."""
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id if func.value.id in libraries else ""
    return ""


#: The ``os.open`` flags that cannot change a file. ``os.open`` is the one module
#: level ``open`` whose second argument is a FLAG SET rather than a mode string,
#: so reading it as a mode gives an unreadable answer and an unreadable answer is
#: a finding. ``cratekit/core/jobs.py`` line 788 opens a DIRECTORY read only to
#: fsync it, and that is what was being reported as a write.
_READING_FLAGS = frozenset(
    {
        "O_RDONLY",
        "O_CLOEXEC",
        "O_DIRECTORY",
        "O_NOCTTY",
        "O_NOFOLLOW",
        "O_NONBLOCK",
    }
)


def _flag_names(node: ast.AST | None) -> list[str] | None:
    """Every flag name one ``os.open`` flag expression ORs, or None if unreadable."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        left = _flag_names(node.left)
        right = _flag_names(node.right)
        return None if left is None or right is None else left + right
    if isinstance(node, ast.Attribute):
        return [node.attr]
    if isinstance(node, ast.Name):
        return [node.id]
    return None


def _os_open_reads(node: ast.Call) -> bool:
    """Whether an ``os.open`` call's flags say read only, and say it readably."""
    flags: ast.AST | None = node.args[1] if len(node.args) > 1 else None
    for keyword in node.keywords:
        if keyword.arg == "flags":
            flags = keyword.value
    names = _flag_names(flags)
    return bool(names) and all(one in _READING_FLAGS for one in names)


def _open_mode(node: ast.Call, *, bound: bool) -> str | None:
    """The literal mode an ``open`` call was given, or None when it is not literal."""
    position = 0 if bound else 1
    supplied: ast.AST | None = node.args[position] if len(node.args) > position else None
    for keyword in node.keywords:
        if keyword.arg == "mode":
            supplied = keyword.value
    if supplied is None:
        return "r"
    if isinstance(supplied, ast.Constant) and isinstance(supplied.value, str):
        return supplied.value
    return None


def _report_modules() -> list[tuple[str, str]]:
    """Every module in the package, walked rather than named (P3)."""
    out: list[tuple[str, str]] = []
    for path in sorted(REPORTS_ROOT.rglob("*.py")):
        parts = list(path.relative_to(SRC_ROOT).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        out.append((".".join(parts), path.read_text()))
    return out


def _elements_written_twice(source: str, name: str) -> list[str]:
    """Values a module-level set literal in ``source`` spells more than once."""
    literal = None
    for node in ast.walk(ast.parse(source)):
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        if target == name:
            literal = node.value

    assert literal is not None, f"{name} is no longer a module-level assignment"
    elements = literal.args[0].elts if isinstance(literal, ast.Call) else literal.elts
    written = [element.value for element in elements]
    return sorted({value for value in written if written.count(value) > 1})


def test_the_duplicate_element_check_sees_a_name_written_twice():
    """The INSTRUMENT, checked before anything is concluded from it."""
    assert _elements_written_twice('X = frozenset({"a", "b", "a"})\n', "X") == ["a"]
    assert _elements_written_twice('X = frozenset({"a", "b"})\n', "X") == []
    assert _elements_written_twice('X = {"a", "b", "a", "b"}\n', "X") == ["a", "b"]
    with pytest.raises(AssertionError):
        _elements_written_twice('X = {"a"}\n', "MISSING")


@pytest.mark.parametrize(
    "name",
    [
        "ALLOWED_IMPORTS",
        "FILESYSTEM_MUTATIONS",
        "QUALIFIED_MUTATIONS",
        "_EVERY_MUTATING_NAME",
        "_EVERY_WRITING_MODE",
    ],
)
def test_the_guard_literals_have_no_element_written_twice(name):
    """A duplicate in a set literal is silent: the runtime object deduplicates it."""
    import inspect

    repeated = _elements_written_twice(inspect.getsource(sys.modules[__name__]), name)
    assert not repeated, f"written twice and collapsed at parse time: {repeated}"


#: Where a residual finding is DEFINED, as git spells it, so it is one string for
#: the derivation that must not police it and for the diff that names what this
#: branch added to it.
RESIDUAL_FINDINGS_NAME = "docs/residual-findings.md"

#: The files this unit is KNOWN to write. A FLOOR rather than the list, because a
#: hand kept list is the defect this guard exists to answer, one level in: the
#: previous version named nine files while the branch changed seventeen, and eight
#: of the eight it missed were invisible to every check here. Two of those eight
#: carry residual citations already.
CITED_FLOOR = (
    "tests/modules/test_reports.py",
    "tests/test_rbxml.py",
    "src/cratekit/modules/reports/__init__.py",
    "src/cratekit/modules/reports/aging.py",
    "src/cratekit/modules/reports/duplicates.py",
    "src/cratekit/modules/reports/export.py",
    "src/cratekit/write/rbxml.py",
    "docs/mutation-u34.md",
    "docs/mutation/u34-round-7-reverts.py",
    "docs/mutation/u34-round-8-reverts.py",
    "docs/mutation/u34-round-9-reverts.py",
    "docs/mutation/u34-round-10-reverts.py",
    "docs/mutation/u34-round-10-verification-table.md",
    "docs/mutation/u34-round-11-reverts.py",
    "docs/mutation/u34-round-11-table.md",
    "docs/u34-round-10-verification.md",
    "docs/HANDOFF.md",
)


#: How a commit says which unit made it. Every commit this unit has ever written
#: carries it in the subject line, and it is the one identifier of this unit's
#: work that a MERGE does not move.
UNIT_COMMIT_TAG = "(U34)"


def _git(*argv: str) -> str:
    """One git read, from the repository root, for the derivations below."""
    return subprocess.run(
        ["git", *argv], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout


def _unit_log(*argv: str) -> str:
    """One `git log` restricted to the commits this unit made."""
    return _git("log", "--format=", "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD", *argv)


def _unit_commits() -> tuple[str, ...]:
    return tuple(_git("log", "--format=%H", "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD").split())


def _existing(named: set[str]) -> tuple[str, ...]:
    return tuple(sorted(one for one in named if (REPO_ROOT / one).is_file()))


def _files_this_unit_writes() -> tuple[str, ...]:
    """Every file this unit changes, read from git rather than kept by hand."""
    named: set[str] = set(_unit_log("--name-only").split())
    for argv in (
        ["diff", "--name-only", "HEAD"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        named |= set(_git(*argv).split())
    return _existing(named)


def _files_this_unit_writes_by_a_second_route() -> tuple[str, ...]:
    """The same question, asked with different plumbing, so a narrowing has to
    happen twice to stay silent.
    """
    named: set[str] = set()
    for commit in _unit_commits():
        fields = [
            one
            for one in _git(
                "diff-tree", "--no-commit-id", "-r", "-z", "--name-status", commit
            ).split("\0")
            if one
        ]
        index = 0
        while index + 1 < len(fields):
            status = fields[index]
            named.add(fields[index + 1])
            index += 2
            if status[0] in "RC" and index < len(fields):
                # In -z mode the path a rename or copy went TO is its own field.
                named.add(fields[index])
                index += 1
    entries = [one for one in _git("status", "--porcelain", "-uall", "-z").split("\0") if one]
    index = 0
    while index < len(entries):
        status, path = entries[index][:2], entries[index][3:]
        named.add(path)
        index += 1
        if status[0] in "RC" and index < len(entries):
            # In -z mode the path a rename or copy CAME FROM is its own field.
            named.add(entries[index])
            index += 1
    return _existing(named)


def _covered_files(written: tuple[str, ...], *, expected: tuple[str, ...]) -> tuple[str, ...]:
    """The derived list, checked against what it must cover, minus one file."""
    missing = sorted(set(expected) - set(written))
    assert missing == [], f"the derivation stopped covering files this unit writes: {missing}"
    unnamed = sorted(set(CITED_FLOOR) - set(written))
    assert unnamed == [], f"both derivations stopped covering named files: {unnamed}"
    return tuple(one for one in written if one != RESIDUAL_FINDINGS_NAME)


def _citing_files() -> tuple[str, ...]:
    """The derived list, minus the one file whose subject IS the numbers."""
    return _covered_files(
        _files_this_unit_writes(),
        expected=_files_this_unit_writes_by_a_second_route(),
    )


#: Modules that live in the reports package and are NOT this unit's, so the bound
#: below must not claim them.
_PACKAGE_MODULES_ANOTHER_UNIT_OWNS: frozenset[str] = frozenset(
    {
        "src/cratekit/modules/reports/coverage.py",
        "src/cratekit/modules/reports/library.py",
    }
)


def _files_this_unit_puts_on_disk() -> tuple[str, ...]:
    """What `CITED_FLOOR` cannot fall below, read off the filesystem."""
    named = {str(one.relative_to(REPO_ROOT)) for one in REPORTS_ROOT.rglob("*.py")}
    named.add(str(Path(__file__).resolve().relative_to(REPO_ROOT)))
    for pattern in ("docs/mutation-u34.*", "docs/u34-*", "docs/mutation/u34-*"):
        named |= {str(one.relative_to(REPO_ROOT)) for one in REPO_ROOT.glob(pattern)}
    absent = sorted(one for one in _PACKAGE_MODULES_ANOTHER_UNIT_OWNS if one not in named)
    assert absent == [], (
        f"the exclusion names files the package does not hold: {absent}. A stale "
        f"entry here silently shrinks the bound, which is the failure the bound "
        f"exists to catch one level up"
    )
    claimed = sorted(set(_PACKAGE_MODULES_ANOTHER_UNIT_OWNS) & set(CITED_FLOOR))
    assert claimed == [], (
        f"the exclusion names files this unit's own floor claims: {claimed}. The "
        f"two registers would then disagree about who owns them, and the widening "
        f"that adds a genuinely owned file to the exclusion is exactly the drift "
        f"this bound exists to refuse"
    )
    remaining = tuple(sorted(named - set(_PACKAGE_MODULES_ANOTHER_UNIT_OWNS)))
    assert remaining, "the exclusion emptied the bound, so it bounds nothing"
    return remaining


#: The residuals THIS UNIT filed, addressed by TITLE.
UNIT_RESIDUAL_TITLES = (
    "Four report verbs were owed by a unit that was about to close, and named a module nobody could build",
    "The review-queue countdown is satisfied by an offer that never runs",
    "A third copy of the import-graph walk now lives in the reports suite",
    "The option a person picks is addressed by an identifier a re-import changes",
    "Two reflection spellings reach a writer past both structural guards",
    "One reflective call shape stays out of reach, and it is named",
    "A namespace method with no argument is an unreadable lookup",
    "Two reflection spellings stay quiet, and each needs a refused import",
    "A container built by a comprehension binds none of its elements",
    "A class rebound after its own definition is no longer reachable by name",
    "A base binding reachable only through a branch is read as unreachable",
    "Two write-path enumerations still read an unreadable node as an absent one",
)

#: What the pair above cannot fall below when BOTH sides go quiet at once.
RESIDUALS_FILED_FLOOR = 12

_CITATION = re.compile(r"\bR-(\d+)\b")

#: A residual heading as the DOCUMENT writes it: the number it carries today, and
#: the title, which is the part that survives a renumber.
_DOCUMENT_HEADING = re.compile(r"^## R-(\d+)\. (.+?)[ \t]*$", re.MULTILINE)

#: The same heading as a DIFF writes it when a commit adds one, which is what
#: says the finding was FILED rather than merely mentioned.
_FILED_HEADING = re.compile(r"^\+## R-(\d+)\. (.+?)[ \t]*$", re.MULTILINE)


def _residual_titles_this_unit_filed() -> tuple[str, ...]:
    """Every residual heading this unit's own commits added, by title."""
    diff = _unit_log("-p", "--", RESIDUAL_FINDINGS_NAME)
    return tuple(dict.fromkeys(title for _, title in _FILED_HEADING.findall(diff)))


def _residual_numbers_by_title(text: str | None = None) -> dict[str, str]:
    """What the residual document calls each finding TODAY."""
    found: dict[str, list[str]] = {}
    if text is None:
        text = (REPO_ROOT / RESIDUAL_FINDINGS_NAME).read_text()
    for number, title in _DOCUMENT_HEADING.findall(text):
        found.setdefault(title, []).append(number)
    doubled = sorted(one for one, numbers in found.items() if len(numbers) > 1)
    assert doubled == [], f"one title is the heading of more than one residual: {doubled}"
    return {title: numbers[0] for title, numbers in found.items()}


def _banned_addresses(
    titles: tuple[str, ...],
    *,
    filed: tuple[str, ...],
    numbers: dict[str, str] | None = None,
) -> tuple[str, ...]:
    """Today's numbers for this unit's residuals, resolved from their titles."""
    listed, actually = set(titles), set(filed)
    assert len(actually) >= RESIDUALS_FILED_FLOOR, (
        f"fewer residuals filed than this unit is known to have filed: {sorted(actually)}"
    )
    uncovered = sorted(actually - listed)
    assert uncovered == [], f"the ban list stopped covering this unit's residuals: {uncovered}"
    invented = sorted(listed - actually)
    assert invented == [], f"the ban list names residuals this unit never filed: {invented}"
    if numbers is None:
        numbers = _residual_numbers_by_title()
    unresolved = sorted(one for one in titles if one not in numbers)
    assert unresolved == [], (
        f"a residual this unit filed no longer answers to its title: {unresolved}"
    )
    return tuple(f"R-{numbers[one]}" for one in titles)


#: The ONE passage whose subject is the numbers themselves, delimited rather than
#: guessed at. A statement that says which numbers collide has to spell them, and
#: an exemption that is a pair of markers can be grepped, cannot widen by accident,
#: and shows up in a diff when somebody moves it.
_COLLISION_OPEN = "[[collision-set]]"
_COLLISION_CLOSE = "[[/collision-set]]"


def _is_delimiter(line: str, marker: str) -> bool:
    """Whether one line IS a marker rather than merely containing one."""
    return line.strip().lstrip("# ").strip() == marker


def _citing_lines(text: str):
    """Every line of one file that is not inside the collision-set passage."""
    exempt = False
    for number, line in enumerate(text.splitlines(), start=1):
        if _is_delimiter(line, _COLLISION_OPEN):
            exempt = True
        elif _is_delimiter(line, _COLLISION_CLOSE):
            exempt = False
        elif not exempt:
            yield number, line


def test_this_units_residuals_are_cited_by_title_and_never_by_number():
    """The citation rule, measured over `docs/` too rather than asserted about it."""
    banned = set(_banned_addresses(UNIT_RESIDUAL_TITLES, filed=_residual_titles_this_unit_filed()))
    # THE COVERAGE IS DERIVED AND THEN ASSERTED, not left to be inferred from a
    # typed list. The claim this replaces was true of source, docstrings and tests
    # and false of `docs/`, and the list that replaced THAT was true of nine files
    # and silent about eight more the same branch writes. `_citing_files` reads
    # git twice by two routes, so a file this branch adds is covered the moment it
    # exists and a narrowing of either derivation is refused by the other.
    covered = _citing_files()
    assert RESIDUAL_FINDINGS_NAME not in covered, "the file that DEFINES them is not policed"
    offenders: list[str] = []
    for name in covered:
        path = REPO_ROOT / name
        for number, line in _citing_lines(path.read_text()):
            hits = {f"R-{one}" for one in _CITATION.findall(line)}
            if hits & banned:
                offenders.append(f"{name}:{number}: {line.strip()}")
    assert offenders == [], offenders


def test_a_coverage_list_narrowed_by_one_file_is_refused_whichever_file_it_is():
    """The property, over the derived list rather than over a typed subset."""
    written = _files_this_unit_writes()
    expected = _files_this_unit_writes_by_a_second_route()
    assert set(expected) <= set(written), sorted(set(expected) - set(written))
    assert len(expected) > len(CITED_FLOOR), "the two would be indistinguishable"
    for dropped in expected:
        narrowed = tuple(one for one in written if one != dropped)
        with pytest.raises(AssertionError):
            _covered_files(narrowed, expected=expected)


def test_the_named_floor_still_bites_when_both_derivations_narrow_together():
    """What the floor is for, driven, because both routes rest on one git."""
    on_disk = _files_this_unit_puts_on_disk()
    assert on_disk, "the bound is empty, so it bounds nothing"
    uncovered = sorted(set(on_disk) - set(CITED_FLOOR))
    assert uncovered == [], f"the floor stopped naming files this unit puts on disk: {uncovered}"
    written = _files_this_unit_writes()
    refused = 0
    for named in CITED_FLOOR:
        narrowed = tuple(one for one in written if one != named)
        with pytest.raises(AssertionError):
            _covered_files(narrowed, expected=narrowed)
        refused += 1
    assert refused == len(CITED_FLOOR)


def test_the_ban_list_is_the_residuals_this_unit_filed_and_nothing_else():
    """The ban list, pinned to what this unit filed rather than to a typed range."""
    filed = _residual_titles_this_unit_filed()
    assert filed, "no residual heading in this unit's own commits is a diff this reads"
    numbers = _residual_numbers_by_title()
    banned = _banned_addresses(UNIT_RESIDUAL_TITLES, filed=filed)
    assert banned == tuple(f"R-{numbers[one]}" for one in UNIT_RESIDUAL_TITLES)

    # NOBODY ELSE'S ADDRESS. The intruder is read out of the document rather than
    # typed, so this stays a property of the document and not of one spelling.
    others = sorted(set(numbers) - set(filed))
    assert others, "the document holds no residual another unit filed, so this proves nothing"
    assert not {one.removeprefix("R-") for one in banned} & {numbers[one] for one in others}

    for narrowed in (UNIT_RESIDUAL_TITLES[1:], UNIT_RESIDUAL_TITLES[:-1], ()):
        with pytest.raises(AssertionError):
            _banned_addresses(narrowed, filed=filed)
    for widened in ((*UNIT_RESIDUAL_TITLES, others[0]), (others[-1], *UNIT_RESIDUAL_TITLES)):
        with pytest.raises(AssertionError):
            _banned_addresses(widened, filed=filed)


def test_a_residual_the_document_renames_or_drops_is_refused_and_never_dropped():
    """A title that stops resolving goes RED rather than banning a smaller set."""
    filed = _residual_titles_this_unit_filed()
    text = (REPO_ROOT / RESIDUAL_FINDINGS_NAME).read_text()
    renamed = 0
    for number, title in _DOCUMENT_HEADING.findall(text):
        if title not in UNIT_RESIDUAL_TITLES:
            continue
        moved = text.replace(f"## R-{number}. {title}", f"## R-{number}. {title}, withdrawn")
        assert moved != text, f"the rename changed no byte for R-{number}"
        with pytest.raises(AssertionError):
            _banned_addresses(
                UNIT_RESIDUAL_TITLES, filed=filed, numbers=_residual_numbers_by_title(moved)
            )
        renamed += 1
    assert renamed == len(UNIT_RESIDUAL_TITLES), "not every address this unit bans was driven"


def test_a_renumber_moves_every_address_and_the_ban_list_follows_it():
    """Every address moved, applied to the document and driven."""
    filed = _residual_titles_this_unit_filed()
    text = (REPO_ROOT / RESIDUAL_FINDINGS_NAME).read_text()
    shifted = _DOCUMENT_HEADING.sub(lambda one: f"## R-{int(one[1]) + 100}. {one[2]}", text)
    assert shifted != text, "the renumber moved nothing, so this proves nothing"
    before = _banned_addresses(UNIT_RESIDUAL_TITLES, filed=filed)
    after = _banned_addresses(
        UNIT_RESIDUAL_TITLES, filed=filed, numbers=_residual_numbers_by_title(shifted)
    )
    assert len(after) == len(before) == len(UNIT_RESIDUAL_TITLES)
    assert set(after).isdisjoint(before), "the addresses did not move, so nothing was tested"
    assert after == tuple(f"R-{int(one.removeprefix('R-')) + 100}" for one in before)


def test_the_collision_passage_is_the_only_exemption_and_it_is_delimited():
    """The exemption's own guard, because an unmeasured exemption is the same hole."""
    exempted = ("docs/mutation-u34.md", "docs/mutation/u34-round-8-reverts.py")
    for name in _citing_files():
        lines = (REPO_ROOT / name).read_text().splitlines()
        opens = [one for one, line in enumerate(lines) if _is_delimiter(line, _COLLISION_OPEN)]
        closes = [one for one, line in enumerate(lines) if _is_delimiter(line, _COLLISION_CLOSE)]
        if name not in exempted:
            assert opens == [] and closes == [], f"{name}: an exemption nobody declared"
            continue
        assert len(opens) == 1, f"{name}: passage moved or multiplied"
        assert len(closes) == 1, f"{name}: passage is not closed"
        assert opens[0] < closes[0], name
    covered = set(_citing_files())
    assert set(exempted) <= covered, "an exempted file this guard never reads"


def test_the_walk_finds_every_module_in_the_package():
    """The guards below are worth nothing if the walk that feeds them is empty."""
    names = {name for name, _ in _report_modules()}
    assert names >= {
        "cratekit.modules.reports",
        "cratekit.modules.reports.aging",
        "cratekit.modules.reports.duplicates",
        "cratekit.modules.reports.export",
    }


def test_the_walk_is_bounded_to_the_package_and_the_allowlist_covers_the_boundary():
    """The two halves of the sibling hole, asserted together because they are one."""
    assert all(
        name.startswith(f"{REPORTS_PACKAGE}.") or name == REPORTS_PACKAGE
        for name, _ in _report_modules()
    )
    assert not _permitted("cratekit.modules.reports_ledger")
    assert not _permitted("cratekit.modules.reportsx")
    assert _permitted(REPORTS_PACKAGE)
    assert _permitted(f"{REPORTS_PACKAGE}.export")


def test_no_report_module_imports_anything_that_can_write():
    problems = {
        module: forbidden_imports(source, module)
        for module, source in _report_modules()
        if forbidden_imports(source, module)
    }
    assert not problems, (
        f"the reports package reached something outside its allowlist: {problems}. "
        f"A read-only report that imports a writer is one line away from being a "
        f"writer, and no test that drives it would notice."
    )


def test_no_report_module_calls_a_filesystem_mutation():
    problems = {
        module: filesystem_mutations(source)
        for module, source in _report_modules()
        if filesystem_mutations(source)
    }
    assert not problems, f"the reports package can change a file: {problems}"


#: The one module in ``ALLOWED_IMPORTS`` that is ALLOWED to write, which is the
#: whole of R12 and the reason the allowlist is an allowlist. Named once so the
#: audit below can exempt it without spelling it a second time.
SANCTIONED_PERSISTENCE = "cratekit.core.review"


def _admitted_repository_modules(
    entries=ALLOWED_IMPORTS, root: Path = SRC_ROOT
) -> list[tuple[str, Path]]:
    """Every module in THIS repository that the allowlist admits."""
    out: list[tuple[str, Path]] = []
    for dotted in sorted(entries):
        if not dotted.startswith("cratekit."):
            continue
        base = root.joinpath(*dotted.split("."))
        if base.with_suffix(".py").is_file():
            out.append((dotted, base.with_suffix(".py")))
            continue
        for path in sorted(base.rglob("*.py")):
            parts = list(path.relative_to(root).with_suffix("").parts)
            if parts[-1] == "__init__":
                parts.pop()
            out.append((".".join(parts), path))
    return out


def _first_party_module(target: str, root: Path = SRC_ROOT) -> tuple[str, Path] | None:
    """The file one resolved first party import executes, or None."""
    base = root.joinpath(*target.split("."))
    if base.with_suffix(".py").is_file():
        return target, base.with_suffix(".py")
    if (base / "__init__.py").is_file():
        return target, base / "__init__.py"
    parent, _, name = target.rpartition(".")
    initializer = root.joinpath(*parent.split("."), "__init__.py")
    if parent and initializer.is_file() and name in _names_bound_by(initializer.read_text()):
        return parent, initializer
    return None


def _names_bound_by(source: str) -> frozenset[str]:
    """Every name a module's top level binds, read off its own statements."""
    names: set[str] = set()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names.update(target.id for target in targets if isinstance(target, ast.Name))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update(
                alias.asname or alias.name.split(".", 1)[0]
                for alias in node.names
                if alias.name != "*"
            )
    return frozenset(names)


def _import_module_calls(source: str) -> list[str]:
    """Every ``importlib.import_module`` in ``source``, as a target or as unreadable."""
    tree = ast.parse(source)
    bare = {"import_module"} | {
        alias.asname
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "importlib"
        for alias in node.names
        if alias.name == "import_module" and alias.asname
    }
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (
            (isinstance(func, ast.Attribute) and func.attr == "import_module")
            or (isinstance(func, ast.Name) and func.id in bare)
        ):
            continue
        first = node.args[0] if node.args else None
        literal = (
            first.value if isinstance(first, ast.Constant) and isinstance(first.value, str) else ""
        )
        found.append(literal if literal and not literal.startswith(".") else _COMPUTED_IMPORT)
    return found


def _admitted_closure(
    entries=ALLOWED_IMPORTS, root: Path = SRC_ROOT
) -> tuple[list[tuple[str, Path]], list[str]]:
    """Every first party module the allowlist admits OR REACHES, and what it could not follow.

    The residual "The reports allowlist audit is one hop deep" is why: an admitted
    module's imports are its attributes, so a write it delegates is reachable too.
    """
    found = dict(_admitted_repository_modules(entries, root))
    waiting = sorted(found)
    unfollowed: list[str] = []
    while waiting:
        dotted = waiting.pop()
        source = found[dotted].read_text()
        for target in _resolved_imports(source, dotted, root) + _import_module_calls(source):
            if target == _COMPUTED_IMPORT:
                unfollowed.append(f"{dotted}: {target}")
                continue
            if target != "cratekit" and not target.startswith("cratekit."):
                continue
            landed = _first_party_module(target, root)
            if landed is None:
                unfollowed.append(f"{dotted}: {target}")
            elif landed[0] not in found:
                found[landed[0]] = landed[1]
                waiting.append(landed[0])
    return sorted(found.items()), unfollowed


def _unnamed_writers_in(audited: list[tuple[str, Path]]) -> dict[str, list[str]]:
    """The audit's loop, named once so a planted closure runs the same one."""
    unnamed: dict[str, list[str]] = {}
    for dotted, path in audited:
        if dotted == SANCTIONED_PERSISTENCE:
            continue
        found = _unnamed_writers(dotted, path.read_text())
        if found:
            unnamed[dotted] = found
    return unnamed


def _unnamed_writers(dotted: str, source: str) -> list[str]:
    """The writers in one admitted module that this guard's sets cannot name."""
    tree = ast.parse(source)
    imported, from_admitted = _writer_bindings(tree)
    own = _writer_names_of(dotted) | from_admitted
    # THE WHOLE FILE ANSWERS BOTH OF THESE and one statement cannot. A reflective
    # read in one function is bound to a module level name and called in another,
    # and the import that says ``os`` is a module sits at the top of a file this
    # loop reads a statement at a time.
    invoked = _invoked_reads(tree)
    libraries = _imported_modules(tree)
    # A FUNCTION ATTACHED TO A CLASS is a method of it, and the audit reads one
    # top level statement at a time, so the pairing has to be read off the whole
    # module before the loop starts. ``Row.go = _go`` puts a writer on a class
    # with the writing method written nowhere near it.
    attached = _attachments(tree)
    short = dotted.rsplit(".", 1)[-1]
    unnamed: list[str] = []
    loose: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # The reachable name is what a caller in the reports package
            # would have to spell: the function, or the class it constructs
            # to get at a writing method or a context manager.
            named = (
                node.name in FILESYSTEM_MUTATIONS or f"{short}.{node.name}" in QUALIFIED_MUTATIONS
            )
            # A CLASS IS ITS OWN OWNER here, because the audit reads one top
            # level statement at a time and there is no walk above it to say so.
            # Without it every method's ``self`` renders unqualified and the
            # class body's attributes are keyed under nothing. It is keyed by
            # DEFINITION SITE rather than by name, which is what the binding
            # table above is keyed by, and deriving both from the node is what
            # keeps the two from drifting.
            owner = (
                _class_key(node) if isinstance(node, ast.ClassDef) else attached.get(node.name, "")
            )
            found = mutations_in(
                node,
                reflection=False,
                modules=imported,
                direct=own,
                invoked=invoked,
                libraries=libraries,
                owner=owner,
                instance=(
                    _Instance() if isinstance(node, ast.ClassDef) else _method_instance(node, owner)
                ),
            )
            if found and not named:
                unnamed.append(node.name)
        else:
            # A write at module level has no name to guard at all, so
            # importing the module performs it. That is never acceptable on
            # the allowlist, whatever it is called.
            loose += mutations_in(
                node,
                reflection=False,
                modules=imported,
                direct=own,
                invoked=invoked,
                libraries=libraries,
            )
    if loose:
        unnamed.append(f"<at import time> {sorted(set(loose))}")
    return unnamed


def test_the_allowlist_admits_no_writer_this_guard_cannot_name():
    """The allowlist's ARGUMENT, checked instead of asserted."""
    audited, unfollowed = _admitted_closure()
    assert not unfollowed, (
        f"the audit could not follow {unfollowed} out of the allowlist. A module "
        f"it cannot read is a module whose writers it cannot name."
    )
    assert {dotted for dotted, _ in audited} >= {
        "cratekit.core.config",
        "cratekit.core.naming",
        SANCTIONED_PERSISTENCE,
        "cratekit.core.taxonomy",
        "cratekit.write.rbxml",
        "cratekit.cli.output",
        "cratekit.core.rb_writer",
        "cratekit.core.tree_registry",
    }, (
        f"the audit walked {sorted(dotted for dotted, _ in audited)}, which does "
        f"not include the modules whose writers this test was written about. An "
        f"audit that walks nothing reports nothing, and reads as a pass."
    )
    unnamed = _unnamed_writers_in(audited)

    assert not unnamed, (
        f"the reports allowlist admits modules whose writers this guard cannot "
        f"name: {unnamed}. Either add each name to FILESYSTEM_MUTATIONS, or to "
        f"QUALIFIED_MUTATIONS with the module in front of it, so a report calling "
        f"it is caught, or drop the module from ALLOWED_IMPORTS. The allowlist's "
        f"comment claims nothing it admits can touch a file except through "
        f"pathlib, and that claim is what this asserts."
    )


#: An admitted module whose writer is spelled through ``getattr`` with a LITERAL
#: name, which is the shape that walks past an audit with reflection off. Nothing
#: about it is exotic: the helper is four tokens long, it reads as a wrapper, and
#: with the literal half of rule 4 gated off the audit reports nothing, so the
#: helper is never forced into the mutation set. A report then reaches it through
#: the allowlisted module by name, ``forbidden_imports`` is empty because the
#: module is allowlisted, and ``filesystem_mutations`` is empty because there is
#: no mutating attribute, no ``getattr``, no ``open`` and no ``replace`` anywhere
#: in the report. Both structural guards green, and a private ignore ledger
#: written.
ADMITTED_REFLECTIVE_WRITER = """
def stash(path, data):
    getattr(path, "write_text")(data)
"""

#: THE SAME HELPER ONE TOKEN LONGER, three ways. Ungating the LITERAL half of
#: rule 4 was round three's fix and it lost nothing, but it did not close the
#: hole, it moved it: a concatenation, a module constant and an f-string each
#: spell exactly the same four-token wrapper and each was invisible to the audit
#: again. The switch has to be on something other than literal versus computed.
ADMITTED_REFLECTIVE_WRITER_BY_CONCATENATION = """
def stash(path, data):
    getattr(path, "write_" + "text")(data)
"""

ADMITTED_REFLECTIVE_WRITER_BY_CONSTANT = """
VERB = "write_text"


def stash(path, data):
    getattr(path, VERB)(data)
"""

ADMITTED_REFLECTIVE_WRITER_BY_FORMAT = """
def stash(path, data):
    getattr(path, f"write_text")(data)
"""

#: And the spelling that reaches the function object without a reflective read at
#: all, which no rule in the guard could name before round four.
ADMITTED_SUBSCRIPTED_WRITER = """
from pathlib import Path


def stash(path, data):
    Path.__dict__["write_text"](path, data)
"""

#: The four helpers the reflection switch was turned off FOR, in the shape they
#: really have: a computed attribute read off a dataclass. Every one of the four
#: was reported by the computed half and none by the literal half, which is why
#: gating the literal half with it was a hole that bought nothing.
ADMITTED_REFLECTIVE_READER = """
def _field_value(name, spec):
    return getattr(spec, name)
"""

#: An admitted module reaching ANOTHER admitted module's writer. The audit reads
#: one function at a time, so before round four it had no import table to resolve
#: ``config`` with and this was invisible: a one-line helper in ``naming``, which
#: ``duplicates`` already imports, writing the configuration file. No module on
#: the allowlist does this today, which is exactly why it is a fixture.
ADMITTED_MODULE_REACHING_ANOTHER_MODULES_WRITER = """
from cratekit.core import config


def refresh(cfg):
    config.save(cfg)
"""

#: And the same writer imported by name rather than reached through its module,
#: which is the other half of the binding table the audit now reads.
ADMITTED_MODULE_IMPORTING_ANOTHER_MODULES_WRITER = """
from cratekit.core.config import save as persist


def refresh(cfg):
    persist(cfg)
"""

#: An admitted module that writes when it is IMPORTED, so there is no name for
#: the set to carry and no call for a report to avoid.
ADMITTED_MODULE_LEVEL_WRITE = """
from pathlib import Path

Path("ledger").write_text("seen")


def read(path):
    return Path(path).read_text()
"""

#: An admitted module exposing an ordinary attribute read whose name collides
#: with a filesystem verb. This is the false positive the receiver check exists
#: to prevent, and it fails the audit outright while ``load`` is a bare member of
#: the mutation set.
ADMITTED_GENERIC_ATTRIBUTE_READ = """
def describe(spec):
    return spec.load
"""

#: An admitted module reaching its OWN writer, which has no receiver to read
#: because inside ``config.py`` there is nothing to spell. This is the shape a
#: receiver qualified set loses if a bare name inside a module is not qualified
#: by that module, and losing it would mean a new entry point reaching a writer
#: through a one-line private wrapper is admitted unnamed.
ADMITTED_MODULE_REACHING_ITS_OWN_WRITER = """
def refresh(cfg):
    return load()
"""


def test_the_audit_names_a_writer_spelled_through_a_literal_getattr():
    """The door the reflection switch opened, driven end to end."""
    assert _unnamed_writers("cratekit.core.naming", ADMITTED_REFLECTIVE_WRITER) == ["stash"]


@pytest.mark.parametrize(
    "source",
    [
        ADMITTED_REFLECTIVE_WRITER,
        ADMITTED_REFLECTIVE_WRITER_BY_CONCATENATION,
        ADMITTED_REFLECTIVE_WRITER_BY_CONSTANT,
        ADMITTED_REFLECTIVE_WRITER_BY_FORMAT,
        ADMITTED_SUBSCRIPTED_WRITER,
    ],
)
def test_the_audit_names_a_writer_however_the_method_name_was_spelled(source):
    """The relocation, closed at the place it kept moving to."""
    assert _unnamed_writers("cratekit.core.naming", source) == ["stash"]


@pytest.mark.parametrize(
    "source",
    [
        ADMITTED_MODULE_REACHING_ANOTHER_MODULES_WRITER,
        ADMITTED_MODULE_IMPORTING_ANOTHER_MODULES_WRITER,
    ],
)
def test_the_audit_reads_the_imports_of_the_module_it_is_auditing(source):
    """The binding table the audit had no way to see."""
    assert _unnamed_writers("cratekit.core.naming", source) == ["refresh"]


def test_the_audit_stays_quiet_on_the_reflective_reads_it_was_loosened_for():
    """The other direction, and the reason only ONE half is gated."""
    assert _unnamed_writers("cratekit.core.naming", ADMITTED_REFLECTIVE_READER) == []
    assert filesystem_mutations(ADMITTED_REFLECTIVE_READER)


def test_the_audit_refuses_a_module_that_writes_when_it_is_imported():
    """The ``loose`` branch, which no admitted module takes today."""
    found = _unnamed_writers("cratekit.core.planted", ADMITTED_MODULE_LEVEL_WRITE)
    assert len(found) == 1
    assert found[0].startswith("<at import time>")
    assert "write_text" in found[0]


def test_the_audit_does_not_call_an_ordinary_attribute_read_a_writer():
    """P7 inside the audit itself, which is where the over-restriction landed."""
    assert _unnamed_writers("cratekit.core.planted", ADMITTED_GENERIC_ATTRIBUTE_READ) == []


def test_the_audit_reads_a_modules_own_bare_call_as_qualified_by_that_module():
    """The half of the receiver rule that has no receiver to read."""
    assert _unnamed_writers("cratekit.core.config", ADMITTED_MODULE_REACHING_ITS_OWN_WRITER) == [
        "refresh"
    ]
    assert _unnamed_writers("cratekit.core.taxonomy", ADMITTED_MODULE_REACHING_ITS_OWN_WRITER) == []


def test_a_package_on_the_allowlist_audits_every_module_underneath_it():
    """The allowlist entry shape the audit used to walk straight past."""
    audited = dict(_admitted_repository_modules({"cratekit.core"}))
    assert "cratekit.core.rb_writer" in audited
    assert "cratekit.core.config" in audited
    assert audited["cratekit.core.config"] == SRC_ROOT / "cratekit" / "core" / "config.py"
    assert _admitted_repository_modules({"cratekit.core.config"}) == [
        ("cratekit.core.config", SRC_ROOT / "cratekit" / "core" / "config.py")
    ]


def _plant(root: Path, modules: dict[str, str]) -> Path:
    """Write a source tree of dotted modules under ``root``, and return it."""
    for dotted, source in modules.items():
        path = root.joinpath(*dotted.split(".")).with_suffix(".py")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
    return root


#: The one hop audit's own driven relocation. ``cause`` keeps a thin caller and the raw
#: ``os.open`` moves into ``access_probe``, a module the allowlist does not name.
#: Driven on the real tree on 2026-08-14, it took the one hop audit from red to
#: green with the package's reach to a write capable handle unchanged.
DELEGATING_CAUSE = """
from cratekit.core import access_probe


def probe(path):
    return access_probe.open_for_probe(path)
"""

DELEGATED_PROBE = """
import os


def open_for_probe(path):
    return os.open(path, os.O_RDWR | os.O_CREAT)
"""

#: The SIDEWAYS case the layering guard cannot see: an admitted module
#: delegating to a module at its own layer, two hops deep, with a cycle back to
#: the admitted module so the walk has to end on what it has seen.
SIDEWAYS_RBXML = """
from cratekit.write import helper


def build(path, data):
    return helper.relay(path, data)
"""

SIDEWAYS_HELPER = """
from cratekit.write import deeper


def relay(path, data):
    return deeper.stash(path, data)
"""

SIDEWAYS_DEEPER = """
from cratekit.write import rbxml


def stash(path, data):
    path.write_text(data)
"""

#: The sanctioned module delegating. ``review`` is exempt as itself, and the
#: exemption is not a door: a writer it imports is audited like any other.
SANCTIONED_REVIEW = """
from cratekit.core import ledger


def offer(path):
    ledger.keep(path)
"""

SANCTIONED_LEDGER = """
def keep(path):
    path.touch()
"""

#: The same delegation with NO import statement for the closure to read, once
#: through the module attribute and once through an aliased bare name. The
#: built in review drove the first against the closure's first version and it
#: came back green.
IMPORT_MODULE_CAUSE = """
import importlib


def probe(path):
    return importlib.import_module("cratekit.core.access_probe").open_for_probe(path)
"""

ALIASED_IMPORT_MODULE_CAUSE = """
from importlib import import_module as load


def probe(path):
    return load("cratekit.core.access_probe").open_for_probe(path)
"""

#: A relative import inside a THREE level package, which the resolver answers
#: by asking the tree whether the base is a directory. Asked of the real tree,
#: the planted ``cratekit.modules.planted`` is no directory, the import reads as
#: the package itself, and ``stash`` is never reached.
RELATIVE_OPENER = """
from . import keeper


def go(path, data):
    return keeper.stash(path, data)
"""

RELATIVE_KEEPER = """
def stash(path, data):
    path.write_bytes(data)
"""


@pytest.mark.parametrize(
    ("entries", "modules", "reported"),
    [
        (
            {"cratekit.core.cause"},
            {
                "cratekit.core.cause": DELEGATING_CAUSE,
                "cratekit.core.access_probe": DELEGATED_PROBE,
            },
            {"cratekit.core.access_probe": ["open_for_probe"]},
        ),
        (
            {"cratekit.write.rbxml"},
            {
                "cratekit.write.rbxml": SIDEWAYS_RBXML,
                "cratekit.write.helper": SIDEWAYS_HELPER,
                "cratekit.write.deeper": SIDEWAYS_DEEPER,
            },
            {"cratekit.write.deeper": ["stash"]},
        ),
        (
            {SANCTIONED_PERSISTENCE},
            {
                SANCTIONED_PERSISTENCE: SANCTIONED_REVIEW,
                "cratekit.core.ledger": SANCTIONED_LEDGER,
            },
            {"cratekit.core.ledger": ["keep"]},
        ),
        (
            {"cratekit.core.cause"},
            {
                "cratekit.core.cause": IMPORT_MODULE_CAUSE,
                "cratekit.core.access_probe": DELEGATED_PROBE,
            },
            {"cratekit.core.access_probe": ["open_for_probe"]},
        ),
        (
            {"cratekit.core.cause"},
            {
                "cratekit.core.cause": ALIASED_IMPORT_MODULE_CAUSE,
                "cratekit.core.access_probe": DELEGATED_PROBE,
            },
            {"cratekit.core.access_probe": ["open_for_probe"]},
        ),
        (
            {"cratekit.modules.planted.opener"},
            {
                "cratekit.modules.planted.opener": RELATIVE_OPENER,
                "cratekit.modules.planted.keeper": RELATIVE_KEEPER,
            },
            {"cratekit.modules.planted.keeper": ["stash"]},
        ),
    ],
    ids=[
        "delegated-down",
        "sideways-two-hops-with-a-cycle",
        "through-the-sanctioned-module",
        "through-import-module",
        "through-an-aliased-import-module",
        "relative-in-a-three-level-package",
    ],
)
def test_the_audit_follows_an_admitted_module_to_the_module_that_writes(
    tmp_path, entries, modules, reported
):
    """The one hop audit's hole, driven on a planted tree rather than argued."""
    root = _plant(tmp_path, modules)
    one_hop = _admitted_repository_modules(entries, root)
    assert _unnamed_writers_in(one_hop) == {}

    audited, unfollowed = _admitted_closure(entries, root)
    assert unfollowed == []
    assert {dotted for dotted, _ in audited} == set(modules)
    assert _unnamed_writers_in(audited) == reported


def test_the_closure_reports_an_import_it_cannot_follow(tmp_path):
    """A module the closure cannot read is reported, never skipped."""
    root = _plant(
        tmp_path,
        {
            "cratekit.core.__init__": "",
            "cratekit.core.cause": (
                "import importlib\n"
                "import cratekit.nowhere.probe\n"
                "import cratekit.core.probe_generated\n\n\n"
                "def load(name):\n    return __import__(name)\n\n\n"
                "def later(name):\n    return importlib.import_module(name)\n\n\n"
                "def sibling():\n"
                "    return importlib.import_module('.probe', 'cratekit.core')\n"
            ),
        },
    )
    audited, unfollowed = _admitted_closure({"cratekit.core.cause"}, root)
    assert [dotted for dotted, _ in audited] == ["cratekit.core.cause"]
    assert sorted(unfollowed) == sorted(
        [
            f"cratekit.core.cause: {_COMPUTED_IMPORT}",
            f"cratekit.core.cause: {_COMPUTED_IMPORT}",
            f"cratekit.core.cause: {_COMPUTED_IMPORT}",
            "cratekit.core.cause: cratekit.core.probe_generated",
            "cratekit.core.cause: cratekit.nowhere.probe",
        ]
    )


def test_a_symbol_imported_from_a_package_follows_the_package_initializer(tmp_path):
    """``from cratekit.core import thing`` where ``thing`` is not a module."""
    root = _plant(
        tmp_path,
        {
            "cratekit.core.__init__": "def thing():\n    return 1\n",
            "cratekit.core.cause": "from cratekit.core import thing\n",
        },
    )
    assert _first_party_module("cratekit.core.thing", root) == (
        "cratekit.core",
        root / "cratekit" / "core" / "__init__.py",
    )
    assert _first_party_module("cratekit.core.absent.deeper", root) is None
    assert _first_party_module("cratekit.core.unbound", root) is None
    audited, unfollowed = _admitted_closure({"cratekit.core.cause"}, root)
    assert unfollowed == []
    assert [dotted for dotted, _ in audited] == ["cratekit.core", "cratekit.core.cause"]


#: The REAL module every shape below is driven against. ``aging`` imports
#: ``config`` at line 61 and ``taxonomy`` beside it, which is what makes it the
#: right file: a false positive here is not a fixture's problem, it is a line
#: somebody could write in this package tomorrow.
AGING_SOURCE = (REPORTS_ROOT / "aging.py").read_text()

#: Ten shapes an ORDINARY AUTHOR writes, each appended to the real ``aging`` and
#: each a finding before this round. The defect they share is one defect: the
#: binding table was swept FLAT off the whole file and only a PARAMETER could
#: take a name back, so every other way of rebinding a name left the stale import
#: binding live underneath it.
ORDINARY_SHAPES_IN_A_REPORT = [
    (
        "a loop target",
        """

def go(rows, out):
    for config in rows:
        out.append(config.load)
    return out
""",
    ),
    (
        "a plain assignment",
        """

def go(raw):
    config = dict(raw)
    return config.load
""",
    ),
    (
        "a comprehension target",
        """

def go(rows):
    return [config.load for config in rows]
""",
    ),
    (
        "a with target",
        """

def go(handle):
    with handle as config:
        return config.load
""",
    ),
    (
        "a walrus",
        """

def go(raw):
    if (config := dict(raw)):
        return config.load
    return None
""",
    ),
    (
        "an except target",
        """

def go(fn):
    try:
        return fn()
    except ValueError as config:
        return config.load
""",
    ),
    (
        "an unpacking target",
        """

def go(pair):
    config, other = pair
    return config.load, other
""",
    ),
    (
        "a module level assignment",
        """

config = {"a": 1}


def go():
    return config.load
""",
    ),
    (
        "a local built by augmented assignment",
        """
from cratekit.core import naming


def go(parts):
    naming = ""
    for part in parts:
        naming += part
    return naming.claim_target
""",
    ),
    (
        "constructor injection",
        """

class Row:
    def __init__(self, config):
        self.config = config

    def go(self):
        return self.config.load
""",
    ),
]

#: Four ordinary MAPPING LOOKUPS whose key happens to spell a filesystem verb.
#: ``touch``, ``rename``, ``truncate``, ``mkdir`` and ``chmod`` are all plausible
#: keys, and rule 5 compared every constant subscript against the mutation set
#: with no receiver read at all while its own docstring claimed an ordinary
#: dispatch table never sees it.
ORDINARY_MAPPING_LOOKUPS = [
    (
        "a counter read twice",
        """

def go(counts):
    return counts["rename"] + counts["unlink"]
""",
    ),
    ("a row field", '\n\ndef go(row):\n    return row["truncate"]\n'),
    (
        "a label table",
        '\n\nLABELS = {"touch": "Touched"}\n\n\ndef go():\n    return LABELS["touch"]\n',
    ),
    (
        "an action table",
        '\n\nACTIONS = {"mkdir": 1}\n\n\ndef go():\n    return ACTIONS["mkdir"]\n',
    ),
]

#: The most ordinary thing anybody writes with the dunder rule 4 names. It
#: forwards the name the interpreter already handed it and calls nothing.
ORDINARY_DUNDER_DELEGATION = """

class Row:
    def __getattribute__(self, name):
        return super().__getattribute__(name)
"""

#: Three REAL WRITES that were missed, all through the same flat table. The first
#: two never rendered a receiver key at all: a tuple right hand side and a
#: conditional are neither a name, a subscript nor an attribute. The third was
#: read one container level deep and stopped.
MISSED_WRITES_IN_A_REPORT = [
    (
        "a parallel unpacking",
        """

def go(cfg):
    alias, other = config, 1
    alias.save(cfg)
    return other
""",
    ),
    (
        "a conditional",
        """

def go(cfg, flag):
    alias = config if flag else config
    alias.save(cfg)
""",
    ),
    (
        "a nested container",
        """

MODS = [[config]]


def go(cfg):
    MODS[0][0].save(cfg)
""",
    ),
    (
        "a boolean fallback",
        """

def go(cfg, override):
    alias = override or config
    alias.save(cfg)
""",
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    ORDINARY_SHAPES_IN_A_REPORT,
    ids=[one[0] for one in ORDINARY_SHAPES_IN_A_REPORT],
)
def test_an_ordinary_rebinding_in_a_real_report_is_not_a_write(shape, snippet):
    """The ten false positives, driven against the module they were found in."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


@pytest.mark.parametrize(
    "shape,snippet", MISSED_WRITES_IN_A_REPORT, ids=[one[0] for one in MISSED_WRITES_IN_A_REPORT]
)
def test_a_write_through_an_unread_binding_shape_is_still_a_write(shape, snippet):
    """The other direction of the same defect, and the one that costs a file."""
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet", ORDINARY_MAPPING_LOOKUPS, ids=[one[0] for one in ORDINARY_MAPPING_LOOKUPS]
)
def test_a_mapping_keyed_on_a_filesystem_verb_is_not_a_write(shape, snippet):
    """Rule 5 with its receiver, against the module the rule would have fired in."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_the_dunder_that_forwards_its_own_name_is_not_a_write():
    """The collateral rule 4's own comment said naming the dunder did not have."""
    assert filesystem_mutations(AGING_SOURCE + ORDINARY_DUNDER_DELEGATION) == []
    assert filesystem_mutations("def stash(p, n, d):\n    object.__getattribute__(p, n)(d)\n")


@pytest.mark.parametrize(
    "source",
    [
        "def go(*, config):\n    return config.load\n",
        "def go(**config):\n    return config.load\n",
        "def go(*config):\n    return config.load\n",
    ],
    ids=["keyword only", "keyword catch all", "positional catch all"],
)
def test_every_parameter_shape_takes_its_name_back(source):
    """The three parameter kinds the shadow list carries and nothing drove."""
    assert filesystem_mutations("from cratekit.core import config\n\n\n" + source) == []


def test_a_receiver_key_is_only_rendered_for_a_call_that_takes_nothing():
    """Both halves of the condition that decides whether a call has one answer."""
    bare = ast.parse("_mod()").body[0].value
    positional = ast.parse("_mod(cfg)").body[0].value
    keyword = ast.parse("_mod(fallback=cfg)").body[0].value
    assert _receiver_key(bare) == "_mod()"
    assert _receiver_key(positional) == ""
    assert _receiver_key(keyword) == ""


def test_a_container_key_this_cannot_read_binds_nothing():
    """The constant-key condition, which a dict with a computed key drives."""
    computed = "from cratekit.core import config\n\nKEY = 'c'\nMODS = {KEY: config}\n"
    assert filesystem_mutations(computed + "\n\ndef go(cfg):\n    MODS['c'].save(cfg)\n") == []
    constant = "from cratekit.core import config\n\nMODS = {'c': config}\n"
    assert filesystem_mutations(constant + "\n\ndef go(cfg):\n    MODS['c'].save(cfg)\n")


#: Eight INDIRECT spellings of one act: a reflective read whose result is called.
#: The switch that decides rule 4's computed half was read off nothing but a
#: ``Call`` whose ``func`` was itself a ``Call``, so it saw the inline spelling
#: and none of these. Every one of them is a wrapper somebody writes on purpose,
#: and against the audit with reflection off every one of them returned nothing.
INDIRECTLY_INVOKED_REFLECTIVE_READS = [
    (
        "bound to a name and called",
        "def stash(path, name, data):\n    writer = getattr(path, name)\n    writer(data)\n",
    ),
    (
        "returned and called by the caller",
        "def stash(path, name):\n    return getattr(path, name)\n\n\n"
        "def go(p, n, d):\n    stash(p, n)(d)\n",
    ),
    (
        "put in a list and called by index",
        "def stash(p, n, d):\n    fns = [getattr(p, n)]\n    fns[0](d)\n",
    ),
    (
        "used as a decorator",
        "def stash(p, n):\n    @getattr(p, n)\n    def inner():\n        return 1\n\n    return inner\n",
    ),
    (
        "bound at module level and called in a function",
        "WRITER = None\n\n\ndef stash(p, n):\n    global WRITER\n\n    WRITER = getattr(p, n)\n\n\n"
        "def go(d):\n    WRITER(d)\n",
    ),
    (
        "handed to a factory invoked on the spot",
        "from functools import partial\n\n\ndef stash(p, n, d):\n    partial(getattr(p, n))(d)\n",
    ),
    (
        "put in a tuple literal and called by index",
        "def stash(p, n, d):\n    (getattr(p, n),)[0](d)\n",
    ),
    (
        "reached through the unbound dunder",
        "def stash(p, n, d):\n    object.__getattribute__(p, n)(d)\n",
    ),
    (
        "bound through a conditional and called",
        "def stash(p, n, d, flag):\n    writer = getattr(p, n) if flag else None\n    writer(d)\n",
    ),
    (
        "bound by a walrus and called",
        "def stash(p, n, d):\n    if (writer := getattr(p, n)):\n        writer(d)\n",
    ),
    (
        "bound by an annotated assignment and called",
        "from typing import Callable\n\n\n"
        "def stash(p, n, d):\n    writer: Callable = getattr(p, n)\n    writer(d)\n",
    ),
    (
        "bound to a name used only as a decorator",
        "def stash(p, n):\n    writer = getattr(p, n)\n\n"
        "    @writer\n    def inner():\n        return 1\n\n    return inner\n",
    ),
    (
        "returned by a nested function the scope around it calls",
        "def stash(p, n, d):\n    def inner():\n        return getattr(p, n)\n\n    inner()(d)\n",
    ),
    (
        "returned by a nested function used as a decorator factory",
        "def stash(p, n):\n    def inner():\n        return getattr(p, n)\n\n"
        "    @inner()\n    def wrapped():\n        return 1\n\n    return wrapped\n",
    ),
]


@pytest.mark.parametrize(
    "shape,source",
    INDIRECTLY_INVOKED_REFLECTIVE_READS,
    ids=[one[0] for one in INDIRECTLY_INVOKED_REFLECTIVE_READS],
)
def test_the_audit_names_a_writer_whose_reflective_read_is_called_indirectly(shape, source):
    """The switch, decided on the binding table rather than on local syntax."""
    assert _unnamed_writers("cratekit.core.naming", source) == ["stash"], shape


def test_the_audit_stays_quiet_on_a_reflective_read_nothing_calls():
    """The other side of the switch, which is why only one half is gated."""
    assert _unnamed_writers("cratekit.core.naming", ADMITTED_REFLECTIVE_READER) == []
    assert (
        _unnamed_writers(
            "cratekit.core.naming",
            "def declared(spec, flag, names):\n    return getattr(spec, flag) and flag not in names\n",
        )
        == []
    )


def test_a_module_level_open_does_not_have_its_file_read_as_its_mode():
    """Finding 8, and the one live example of it in the tree."""
    jobs = SRC_ROOT / "cratekit" / "core" / "jobs.py"
    assert "_fsync_directory" not in _unnamed_writers("cratekit.core.jobs", jobs.read_text())
    quiet = [
        'import io\n\n\ndef read(p):\n    return io.open(p, "rb")\n',
        'import gzip\n\n\ndef read(p):\n    return gzip.open(p, "rb")\n',
        'import codecs\n\n\ndef read(p):\n    return codecs.open(p, "r", "utf-8")\n',
        'import tarfile\n\n\ndef read(p):\n    return tarfile.open(p, "r")\n',
        "import os\n\n\ndef sync(p):\n    return os.open(str(p), os.O_RDONLY)\n",
        "import os\n\n\ndef walk(p):\n    return os.open(p, os.O_RDONLY | os.O_DIRECTORY)\n",
        # THE BARE IMPORTED FLAG, which was a pure read reported as a write.
        # ``_READING_FLAGS`` holds bare names and ``_flag_names`` could only ever
        # produce one from the dotted spelling, so the identical call written
        # with ``from os import O_RDONLY`` was an unreadable flag set and
        # therefore a finding. The real ``jobs.py`` happens to spell it dotted,
        # which is the only reason this was not live in the tree.
        "import os\nfrom os import O_RDONLY\n\n\ndef sync(p):\n    return os.open(str(p), O_RDONLY)\n",
        "import os\nfrom os import O_DIRECTORY, O_RDONLY\n\n\n"
        "def walk(p):\n    return os.open(p, O_RDONLY | O_DIRECTORY)\n",
        "import os\nfrom os import O_RDONLY\n\n\n"
        "def walk(p):\n    return os.open(p, O_RDONLY | os.O_DIRECTORY)\n",
        "import os\nfrom os import O_RDONLY\n\n\ndef sync(p):\n    return os.open(p, flags=O_RDONLY)\n",
    ]
    for source in quiet:
        assert filesystem_mutations(source) == [], source
    writing = [
        'import io\n\n\ndef write(p):\n    return io.open(p, "w")\n',
        "import os\n\n\ndef make(p):\n    return os.open(p, os.O_CREAT | os.O_EXCL)\n",
        "import os\n\n\ndef make(p, flags):\n    return os.open(p, flags)\n",
        "import io\n\n\ndef go(p, mode):\n    return io.open(p, mode)\n",
        # Every WRITING flag still fires in the bare spelling, and so does a flag
        # held in a VARIABLE, which is what keeps reading a name from being the
        # same thing as accepting one.
        "import os\nfrom os import O_CREAT\n\n\ndef make(p):\n    return os.open(p, O_CREAT)\n",
        "import os\nfrom os import O_WRONLY\n\n\ndef make(p):\n    return os.open(p, O_WRONLY)\n",
        "import os\nfrom os import O_RDWR\n\n\ndef make(p):\n    return os.open(p, O_RDWR)\n",
        "import os\nfrom os import O_TRUNC\n\n\ndef make(p):\n    return os.open(p, O_TRUNC)\n",
        "import os\nfrom os import O_APPEND\n\n\ndef make(p):\n    return os.open(p, O_APPEND)\n",
        "import os\nfrom os import O_EXCL, O_RDONLY\n\n\n"
        "def make(p):\n    return os.open(p, O_RDONLY | O_EXCL)\n",
        # A flag EXPRESSION that is neither a name nor an attribute is unreadable,
        # and unreadable is reported. Reading a bare name is not the same act as
        # accepting one, and this is the line that says so.
        "import os\n\n\ndef make(p, chosen):\n    return os.open(p, chosen())\n",
    ]
    for source in writing:
        assert filesystem_mutations(source), source


def test_the_binding_table_is_scoped_and_the_object_half_is_not():
    """The one asymmetry in the table, asserted rather than described."""
    injected = (
        "from cratekit.core import config\n\n\n"
        "class Row:\n"
        "    def __init__(self, config):\n"
        "        self.config = config\n\n"
        "    def go(self, cfg):\n"
        "        self.config.save(cfg)\n"
    )
    assert filesystem_mutations(injected) == []
    stored = (
        "from cratekit.core import config\n\n\n"
        "class Row:\n"
        "    def __init__(self):\n"
        "        self.mod = config\n\n"
        "    def go(self, cfg):\n"
        "        self.mod.save(cfg)\n"
    )
    assert filesystem_mutations(stored)


#: TWO CLASSES, ONE SPELLING, and the reason the test above cannot see the defect
#: it was written for: it uses ONE class, so the table's key can be as coarse as
#: it likes and nothing disagrees.
TWO_SELVES_IN_ONE_FILE = """

class Injected:
    def __init__(self, config):
        self.config = config

    def go(self):
        return self.config.load


class Holder:
    def __init__(self):
        self.config = config

    def refresh(self, cfg):
        self.config.save(cfg)
"""


def test_two_classes_spelling_one_attribute_do_not_share_a_binding():
    """Both directions of the qualified key, in one file, against the real module."""
    found = filesystem_mutations(AGING_SOURCE + TWO_SELVES_IN_ONE_FILE)
    assert [one for one in found if "config.load" in one] == [], found
    assert [one for one in found if "config.save" in one], found


def test_the_instance_is_the_first_parameter_rather_than_the_word_self():
    """``self`` is a convention, and a key keyed on a convention is one rename out."""
    renamed = """

class Keeper:
    def __init__(this):
        this.mod = config

    def go(self, cfg):
        self.mod.save(cfg)
"""
    assert filesystem_mutations(AGING_SOURCE + renamed)
    static = """

class Keeper:
    def __init__(self):
        self.mod = config

    @staticmethod
    def go(self, cfg):
        return self.mod.load
"""
    assert filesystem_mutations(AGING_SOURCE + static) == []
    through_the_class = """

class Keeper:
    mod = config

    @classmethod
    def go(cls, cfg):
        cls.mod.save(cfg)
"""
    assert filesystem_mutations(AGING_SOURCE + through_the_class)
    # A CLASS ATTRIBUTE OVERRIDDEN PER INSTANCE, which is ordinary and runnable.
    # ``cls.mod`` is the class's ``None``, not the constructor's module. Read as
    # an instance, ``cls`` would resolve to the constructor's binding and this
    # ordinary classmethod would be a write to the library.
    overridden = """

class Keeper:
    mod = None

    def __init__(self):
        self.mod = config

    @classmethod
    def describe(cls):
        return cls.mod.load
"""
    assert filesystem_mutations(AGING_SOURCE + overridden) == []


#: A CLASS ATTRIBUTE BOUND TO AN ADMITTED MODULE, in every spelling that reaches
#: it. ``self.mod = config`` in a constructor was caught and had a test; the
#: identical assignment written in the class body was not, because a class body
#: was read as part of the scope around it and bound only the bare name ``mod``.
#: Two lines wrote the configuration file with ruff, both structural guards and
#: the audit green.
CLASS_ATTRIBUTE_REACHES_A_WRITER = [
    (
        "read through the instance",
        "\n\nclass Keeper:\n    mod = config\n\n    def go(self, cfg):\n        self.mod.save(cfg)\n",
    ),
    (
        "read through the class inside a method",
        "\n\nclass Keeper:\n    mod = config\n\n    def go(self, cfg):\n        Keeper.mod.save(cfg)\n",
    ),
    (
        "read through the class from outside it",
        "\n\nclass Keeper:\n    mod = config\n\n\ndef go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "an annotated class attribute",
        "\n\nclass Keeper:\n    mod: object = config\n\n    def go(self, cfg):\n        self.mod.save(cfg)\n",
    ),
    (
        "an attribute of a NESTED class",
        "\n\nclass Outer:\n    class Keeper:\n        mod = config\n\n\ndef go(cfg):\n    Outer.Keeper.mod.save(cfg)\n",
    ),
    (
        "an instance read through a closure",
        "\n\nclass Keeper:\n    mod = config\n\n    def go(self, cfg):\n"
        "        def inner():\n            self.mod.save(cfg)\n\n        return inner\n",
    ),
]

#: The other side of the class body being a scope, and every one of these was
#: either wrong before or is wrong the moment the scope rule is relaxed.
CLASS_BODY_STAYS_IN_THE_CLASS = [
    (
        "a class body name is not visible inside its methods",
        "\n\nclass Keeper:\n    mod = config\n\n    def go(self, cfg):\n        return mod.load\n",
    ),
    (
        "a class body name is not visible after the class",
        "\n\nclass Keeper:\n    mod = config\n\n\ndef go(cfg):\n    return mod.load\n",
    ),
    (
        "a NESTED class does not lend its attribute to the class around it",
        "\n\nclass Outer:\n    class Keeper:\n        mod = config\n\n    def go(self, cfg):\n        return self.mod.load\n",
    ),
    (
        "an instance name taken back by a nested scope stops being the instance",
        "\n\nclass Keeper:\n    mod = config\n\n    def go(self, cfg):\n"
        "        def inner(self):\n            return self.mod.load\n\n        return inner\n",
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    CLASS_ATTRIBUTE_REACHES_A_WRITER,
    ids=[one[0] for one in CLASS_ATTRIBUTE_REACHES_A_WRITER],
)
def test_a_module_aliased_in_a_class_body_is_still_that_module(shape, snippet):
    """The evasion the round already caught one line lower, closed at its own line."""
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    CLASS_BODY_STAYS_IN_THE_CLASS,
    ids=[one[0] for one in CLASS_BODY_STAYS_IN_THE_CLASS],
)
def test_a_class_body_binds_for_its_class_and_for_nothing_else(shape, snippet):
    """A class body is a scope, and the false positive direction says so."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_a_method_that_hands_back_a_module_is_keyed_under_its_class():
    """``_mod()`` is a fact about ONE function, and a method is not that function."""
    source = """

class Keeper:
    def _mod(self):
        return config

    def go(self, cfg):
        self._mod().save(cfg)


def _mod():
    return None


def elsewhere():
    return _mod().load
"""
    found = filesystem_mutations(AGING_SOURCE + source)
    assert [one for one in found if "config.save" in one], found
    assert [one for one in found if "config.load" in one] == [], found


def test_a_class_attribute_does_not_take_a_modules_name_from_the_file():
    """The shadow the old reading had, which was the quiet half of the same defect."""
    shadowed = "\n\nclass Keeper:\n    config = 1\n\n\ndef go(cfg):\n    config.save(cfg)\n"
    assert filesystem_mutations(AGING_SOURCE + shadowed)


def test_the_audit_names_a_class_that_reaches_a_writer_through_its_body():
    """The same two lines through the allowlist audit, which reads one class at a time."""
    keeper = (
        "from cratekit.core import config\n\n\n"
        "class Keeper:\n"
        "    mod = config\n\n"
        "    def go(self, cfg):\n"
        "        self.mod.save(cfg)\n"
    )
    assert _unnamed_writers("cratekit.core.naming", keeper) == ["Keeper"]
    injected = (
        "from cratekit.core import config\n\n\n"
        "class Keeper:\n"
        "    def __init__(self, config):\n"
        "        self.config = config\n\n"
        "    def go(self):\n"
        "        return self.config.load\n"
    )
    assert _unnamed_writers("cratekit.core.naming", injected) == []


#: A KEY THAT LANDED ON THE CLASS THAT DECLARES IT rather than on the class that
#: REACHES it. Every one of these is two or three lines appended to the real
#: ``aging``, every one of them wrote the configuration file with both structural
#: guards and the audit green, and not one of them is evasion: a base class, a
#: mixin and a method attached after the fact are ordinary author code.
INHERITED_ATTRIBUTE_REACHES_A_WRITER = [
    (
        "a base class constructor's binding, read in a subclass",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def go(self, cfg):\n        self.mod.save(cfg)\n",
    ),
    (
        "a MIXIN's writer over the binding its subclass makes",
        "\n\nclass WriterMixin:\n    def go(self, cfg):\n        self.mod.save(cfg)\n\n\n"
        "class Row(WriterMixin):\n    def __init__(self):\n        self.mod = config\n",
    ),
    (
        "an inherited class body attribute, read through the instance",
        "\n\nclass Base:\n    mod = config\n\n\n"
        "class Row(Base):\n    def go(self, cfg):\n        self.mod.save(cfg)\n",
    ),
    (
        "an inherited class body attribute, read through the subclass",
        "\n\nclass Base:\n    mod = config\n\n\nclass Row(Base):\n    pass\n\n\n"
        "def go(cfg):\n    Row.mod.save(cfg)\n",
    ),
    (
        "three classes deep, with the middle one binding nothing",
        "\n\nclass Base:\n    mod = config\n\n\nclass Middle(Base):\n    pass\n\n\n"
        "class Row(Middle):\n    def go(self, cfg):\n        self.mod.save(cfg)\n",
    ),
    (
        "a method attached to its class after the class was written",
        "\n\ndef _go(self, cfg):\n    self.mod.save(cfg)\n\n\n"
        "class Row:\n    def __init__(self):\n        self.mod = config\n\n\nRow.go = _go\n",
    ),
]

#: The other direction, and the one a family-wide key would get wrong. Two
#: subclasses of one base are not each other's business, a base does not borrow
#: from its subclass through the CLASS spelling, and a class is identified by
#: where it is written rather than by what it is called.
INHERITANCE_STAYS_IN_THE_FAMILY = [
    (
        "a sibling subclass's binding is not this subclass's",
        "\n\nclass Base:\n    pass\n\n\n"
        "class Injected(Base):\n    def __init__(self, config):\n        self.config = config\n\n"
        "    def go(self):\n        return self.config.load\n\n\n"
        "class Holder(Base):\n    def __init__(self):\n        self.config = config\n",
    ),
    (
        "a base does not reach its subclass's class attribute through the class",
        "\n\nclass Base:\n    def go(self, cfg):\n        return Base.mod.load\n\n\n"
        "class Row(Base):\n    mod = config\n",
    ),
    (
        "two classes of one name in two factories",
        "\n\ndef one():\n    class Keeper:\n        mod = config\n\n    return Keeper\n\n\n"
        "def two(config):\n    class Keeper:\n        def __init__(self):\n            self.mod = config\n\n"
        "        def go(self):\n            return self.mod.load\n\n    return Keeper\n",
    ),
    (
        "a class name redefined at module level",
        "\n\nclass Keeper:\n    mod = config\n\n\n"
        "class Keeper:\n    def __init__(self, config):\n        self.mod = config\n\n"
        "    def go(self):\n        return self.mod.load\n",
    ),
    (
        "a parameter that shadows a class name",
        "\n\nclass Keeper:\n    mod = config\n\n\ndef go(Keeper):\n    return Keeper.mod.load\n",
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    INHERITED_ATTRIBUTE_REACHES_A_WRITER,
    ids=[one[0] for one in INHERITED_ATTRIBUTE_REACHES_A_WRITER],
)
def test_a_module_bound_anywhere_in_a_class_family_is_still_that_module(shape, snippet):
    """The key resolved through the family rather than parked on one member of it."""
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    INHERITANCE_STAYS_IN_THE_FAMILY,
    ids=[one[0] for one in INHERITANCE_STAYS_IN_THE_FAMILY],
)
def test_a_class_key_names_one_class_and_never_two(shape, snippet):
    """The false positives a coarser key produces, which are ordinary code."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


#: SIX ORDINARY SHAPES, every one of them a subclass overriding an attribute its
#: base binds, and every one of them reported as a write to the library by the
#: round that added inheritance. Not one is evasion. Overriding an inherited
#: attribute in a constructor is the most ordinary thing inheritance does.
AN_OVERRIDE_TAKES_THE_ATTRIBUTE_BACK = [
    (
        "a subclass overrides in its own constructor with a plain dict",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a subclass sets it to None and then to a parameter",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, mod):\n        self.mod = None\n"
        "        self.mod = mod\n\n    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "three classes deep, with the middle one rebinding to a parameter",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Middle(Base):\n    def __init__(self, mod):\n        self.mod = mod\n\n\n"
        "class Row(Middle):\n    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "multiple inheritance, with two bases binding the name differently",
        "\n\nclass Alpha:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Beta:\n    def __init__(self, mod):\n        self.mod = mod\n\n\n"
        "class Row(Beta, Alpha):\n    def __init__(self, mod):\n        self.mod = dict(mod)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a subclass whose constructor never calls its base's",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n\n\n"
        "class Other(Base):\n    pass\n",
    ),
    (
        "a class body attribute set to None over a base that binds the module",
        "\n\nclass Base:\n    mod = config\n\n\n"
        "class Row(Base):\n    mod = None\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
]


#: The writes the failed attempt rule must not cost, and they are the ones a rule
#: written one degree too wide would take. An override is a fact about the class
#: that wrote it, so it blocks what is ABOVE it and nothing else: not a sibling,
#: not a mixin reading the same attribute through a different subclass, and not
#: another method of the same class that binds the real module.
AN_OVERRIDE_BLOCKS_NOTHING_ELSE = [
    (
        "a sibling subclass that binds the real module is still reached",
        "\n\nclass WriterMixin:\n    def go(self, cfg):\n        self.mod.save(cfg)\n\n\n"
        "class Injected(WriterMixin):\n    def __init__(self, mod):\n        self.mod = mod\n\n\n"
        "class Holder(WriterMixin):\n    def __init__(self):\n        self.mod = config\n",
    ),
    (
        "one class binding the attribute twice, the module last",
        "\n\nclass Row:\n    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
        "    def load(self):\n        self.mod = config\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "one class binding the attribute twice, the module first",
        "\n\nclass Row:\n    def load(self):\n        self.mod = config\n\n"
        "    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a base that binds the module below a subclass that overrides it",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        self.mod = dict(raw)\n",
    ),
    (
        "a class body attribute the subclass leaves alone",
        "\n\nclass Base:\n    mod = config\n\n\n"
        "class Row(Base):\n    other = None\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    AN_OVERRIDE_TAKES_THE_ATTRIBUTE_BACK,
    ids=[one[0] for one in AN_OVERRIDE_TAKES_THE_ATTRIBUTE_BACK],
)
def test_an_attribute_a_subclass_takes_for_itself_is_not_its_bases(shape, snippet):
    """The false positive direction of the table the round before rebuilt."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape
    assert _unnamed_writers(REPORTS_PACKAGE + ".aging", AGING_SOURCE + snippet) == [], shape


@pytest.mark.parametrize(
    "shape,snippet",
    AN_OVERRIDE_BLOCKS_NOTHING_ELSE,
    ids=[one[0] for one in AN_OVERRIDE_BLOCKS_NOTHING_ELSE],
)
def test_an_override_blocks_upward_and_never_sideways_or_down(shape, snippet):
    """The miss direction of the same rule, asserted rather than reasoned about."""
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


#: AN OVERRIDE ONE INDENT IN, which is the same false positive as the six above
#: with a branch around it, and which the branch rule put back for six rounds
#: because the rule's scope was stated in PROSE and driven on the NAME half only.
AN_OVERRIDE_INSIDE_A_BRANCH_REACHES_NOTHING = [
    (
        "both arms of an if/else override it",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        if raw:\n"
        "            self.mod = dict(raw)\n        else:\n            self.mod = {}\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a bare if with no else and no chaining call",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        if raw:\n"
        "            self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "both arms of a try/except override it",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        try:\n"
        "            self.mod = dict(raw)\n        except TypeError:\n"
        "            self.mod = {}\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a while body overrides it",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        while raw:\n"
        "            self.mod = dict(raw)\n            raw = None\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "every case of a match overrides it",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        match raw:\n"
        "            case None:\n                self.mod = {}\n"
        "            case _:\n                self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a for body and its else both override it",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, rows):\n        for one in rows:\n"
        "            self.mod = dict(one)\n        else:\n            self.mod = {}\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "the chaining call sits inside the same arm as the override",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        if raw:\n"
        "            super().__init__()\n            self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "the constructor calls another method but never chains",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        self.reset()\n"
        "        if raw:\n            self.mod = dict(raw)\n\n"
        "    def reset(self):\n        self.count = 0\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
]


#: THE MISS DIRECTION OF THE SAME RULE, and the reason a flag on the key's spelling
#: was not enough. The base's binding really is reachable in each of these, so each
#: has to keep firing, and a restriction that only asked whether the key was an
#: identifier made the first one quiet.
A_BRANCHED_OVERRIDE_THE_BASE_STILL_SURVIVES = [
    (
        "a conditional override in a constructor that chains first",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        super().__init__()\n"
        "        if raw:\n            self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a conditional override in a constructor that chains by name",
        "\n\nclass Base:\n    def __init__(self):\n        self.mod = config\n\n\n"
        "class Row(Base):\n    def __init__(self, raw):\n        Base.__init__(self)\n"
        "        if raw:\n            self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a conditional override of an attribute the class body binds",
        "\n\nclass Keeper:\n    mod = config\n\n"
        "    def __init__(self, raw):\n        if raw:\n            self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
    (
        "a conditional override under an unconditional one that resolved",
        "\n\nclass Row:\n    def __init__(self, raw):\n        self.mod = config\n"
        "        if raw:\n            self.mod = dict(raw)\n\n"
        "    def go(self, cfg):\n        return self.mod.save(cfg)\n",
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    AN_OVERRIDE_INSIDE_A_BRANCH_REACHES_NOTHING,
    ids=[one[0] for one in AN_OVERRIDE_INSIDE_A_BRANCH_REACHES_NOTHING],
)
def test_a_branched_override_of_an_attribute_no_path_supplies_is_not_a_write(shape, snippet):
    """The branch rule read on the OBJECT half, driven instead of described."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape
    assert _unnamed_writers(REPORTS_PACKAGE + ".aging", AGING_SOURCE + snippet) == [], shape


@pytest.mark.parametrize(
    "shape,snippet",
    A_BRANCHED_OVERRIDE_THE_BASE_STILL_SURVIVES,
    ids=[one[0] for one in A_BRANCHED_OVERRIDE_THE_BASE_STILL_SURVIVES],
)
def test_a_branched_override_still_loses_to_a_binding_that_survives_it(shape, snippet):
    """The half a restriction on the key's SPELLING would have cost."""
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


#: A CLASS BODY BINDING UNDER AN ORDINARY CONSTRUCTOR, which is the most common
#: class in the language and which the table read as a write.
CLASS_BODY_READ_THROUGH_THE_INSTANCE = (
    "\n\nclass Keeper:\n    mod = config\n\n"
    "    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
    "    def go(self, cfg):\n        return self.mod.save(cfg)\n"
)

CLASS_BODY_READ_THROUGH_THE_CLASS = (
    "\n\nclass Keeper:\n    mod = config\n\n"
    "    def __init__(self, raw):\n        self.mod = dict(raw)\n\n\n"
    "def through_the_class(cfg):\n    return Keeper.mod.save(cfg)\n"
)

#: The CLASS spelling under a method that rebinds it, which is the write a weak
#: class spelling would lose. ``Keeper.mod`` is the module until ``clear`` runs
#: and the read is reachable before it does, so this fires.
CLASS_BODY_REBOUND_THROUGH_THE_CLASS = (
    "\n\nclass Keeper:\n    mod = config\n\n"
    "    def clear(self):\n        Keeper.mod = None\n\n"
    "    def go(self, cfg):\n        return Keeper.mod.save(cfg)\n"
)


def test_an_instance_override_shadows_a_class_body_binding_but_not_the_class():
    """Both spellings of one attribute, because the two disagree at runtime."""
    assert filesystem_mutations(AGING_SOURCE + CLASS_BODY_READ_THROUGH_THE_INSTANCE) == []
    assert filesystem_mutations(AGING_SOURCE + CLASS_BODY_READ_THROUGH_THE_CLASS)
    assert filesystem_mutations(AGING_SOURCE + CLASS_BODY_REBOUND_THROUGH_THE_CLASS)


#: THE ORDER THE WALK HAPPENS TO VISIT TWO SCOPES IN, which must not decide. The
#: class body is written after the constructor here and before it above, and the
#: table has to give the same answer to both.
CLASS_BODY_WRITTEN_AFTER_THE_CONSTRUCTOR = (
    "\n\nclass Keeper:\n"
    "    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
    "    mod = config\n\n"
    "    def go(self, cfg):\n        return self.mod.save(cfg)\n"
)


def test_the_faint_tier_does_not_depend_on_which_scope_the_walk_reached_first():
    """The order independence ``_record`` claims, driven in both orders."""
    assert filesystem_mutations(AGING_SOURCE + CLASS_BODY_WRITTEN_AFTER_THE_CONSTRUCTOR) == []


#: TWO INSTANCE WRITES TO ONE ATTRIBUTE, one resolved and one not, under a class
#: body that binds the same name. ``_record``'s rule is that a key which RESOLVED
#: is never taken back by one that did not, and the class body's mark is what
#: would let it happen anyway: a mark admits an unresolved write, so the write
#: that resolved the key has to clear it on the way out.
A_RESOLVED_INSTANCE_WRITE_BEFORE_AN_UNRESOLVED_ONE = (
    "\n\nclass Keeper:\n    mod = config\n\n"
    "    def __init__(self, raw):\n        self.mod = config\n\n"
    "    def forget(self, raw):\n        self.mod = dict(raw)\n\n"
    "    def go(self, cfg):\n        return self.mod.save(cfg)\n"
)

A_RESOLVED_INSTANCE_WRITE_AFTER_AN_UNRESOLVED_ONE = (
    "\n\nclass Keeper:\n    mod = config\n\n"
    "    def forget(self, raw):\n        self.mod = dict(raw)\n\n"
    "    def __init__(self, raw):\n        self.mod = config\n\n"
    "    def go(self, cfg):\n        return self.mod.save(cfg)\n"
)

#: The same pair with the class body binding something that is NOT the module,
#: which is the shape that separates the mark from the value under it. ``mod =
#: None`` still takes the attribute for the class, so the mark is still written,
#: and the resolved instance write is still the strongest fact about the key.
A_CLASS_BODY_THAT_BOUND_NOTHING_UNDER_TWO_INSTANCE_WRITES = (
    "\n\nclass Keeper:\n    mod = None\n\n"
    "    def __init__(self, raw):\n        self.mod = config\n\n"
    "    def forget(self, raw):\n        self.mod = dict(raw)\n\n"
    "    def go(self, cfg):\n        return self.mod.save(cfg)\n"
)


@pytest.mark.parametrize(
    "snippet",
    [
        A_RESOLVED_INSTANCE_WRITE_BEFORE_AN_UNRESOLVED_ONE,
        A_RESOLVED_INSTANCE_WRITE_AFTER_AN_UNRESOLVED_ONE,
        A_CLASS_BODY_THAT_BOUND_NOTHING_UNDER_TWO_INSTANCE_WRITES,
    ],
    ids=["resolved first", "resolved second", "the class body bound nothing"],
)
def test_an_unresolved_instance_write_never_takes_back_a_resolved_one(snippet):
    """The half of ``_record`` that clears the mark, which nothing drove."""
    assert filesystem_mutations(AGING_SOURCE + snippet)


#: ``del`` PUTS THE CLASS ATTRIBUTE BACK, which is a real write and was quiet.
#: Executed, the deleting method returns the module's own result, so the guard
#: reporting nothing was a miss rather than a judgement.
A_DELETE_THAT_REACHES_THE_CLASS_ATTRIBUTE = (
    "\n\nclass Deleter:\n    mod = config\n\n"
    "    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
    "    def go(self, cfg):\n        del self.mod\n        return self.mod.save(cfg)\n"
)

#: The same statement with nothing underneath it to reach. ``del self.mod`` here
#: leaves an ``AttributeError`` rather than a module, so the restore must be a
#: FILL rather than an assertion: it takes what the class spelling holds, and the
#: class spelling holds nothing.
A_DELETE_THAT_REACHES_NOTHING = (
    "\n\nclass Deleter:\n"
    "    def __init__(self, raw):\n        self.mod = dict(raw)\n\n"
    "    def go(self, cfg):\n        del self.mod\n        return self.mod.save(cfg)\n"
)


def test_deleting_an_instance_attribute_reaches_the_class_attribute_under_it():
    """Both directions of the restore, because only one of them is a write."""
    assert filesystem_mutations(AGING_SOURCE + A_DELETE_THAT_REACHES_THE_CLASS_ATTRIBUTE)
    assert filesystem_mutations(AGING_SOURCE + A_DELETE_THAT_REACHES_NOTHING) == []


#: TWO CLASS DEFINITIONS OF ONE NAME, and the distinction the residual "A class
#: rebound after its own definition is no longer reachable by name" was missing. Read
#: at module level, ``class Keeper`` twice in one statement list leaves one
#: reachable ``Keeper`` and the first one's attributes are an ``AttributeError``,
#: so reporting nothing is right. In two ARMS of one conditional only one arm runs
#: and nothing was taken from anything, so a module bound in either arm can write.
#: That residual transferred the first judgement onto the second and called it
#: correct.
A_NAME_THAT_STILL_MEANS_ITS_CLASS = [
    (
        "two class definitions in the arms of one conditional",
        "\n\n_ARM = True\n\nif _ARM:\n\n    class Keeper:\n        mod = config\n\nelse:\n\n"
        "    class Keeper:\n        pass\n\n\ndef go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "a class name rebound to itself",
        "\n\nclass Keeper:\n    mod = config\n\n\nKeeper = Keeper\n\n\n"
        "def go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "a class name rebound to itself or a fallback",
        "\n\nclass Keeper:\n    mod = config\n\n\nKeeper = Keeper or None\n\n\n"
        "def go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "a class name rebound to itself through a conditional expression",
        "\n\nclass Keeper:\n    mod = config\n\n\nKeeper = Keeper if True else None\n\n\n"
        "def go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "a module name rebound to itself or a fallback",
        "\n\ndef go(cfg, fallback):\n    config = config or fallback\n    return config.save(cfg)\n",
    ),
    (
        "a local bound to itself or the module, where only the module resolves",
        "\n\ndef go(cfg):\n    alias = alias or config\n    return alias.save(cfg)\n",
    ),
    (
        "a module name rebound to itself",
        "\n\nconfig = config\n\n\ndef go(cfg):\n    config.save(cfg)\n",
    ),
    (
        "a class body pinning a module under its own name, read through the instance",
        "\n\nclass Keeper:\n    config = config\n\n"
        "    def go(self, cfg):\n        return self.config.save(cfg)\n",
    ),
    (
        "a class body pinning a module under its own name, read through the class",
        "\n\nclass Keeper:\n    config = config\n\n\n"
        "def go(cfg):\n    return Keeper.config.save(cfg)\n",
    ),
    (
        "a wrapper applied to the class inside a conditional",
        "\n\nfrom dataclasses import dataclass\n\n\nclass Keeper:\n    mod = config\n\n\n"
        "if True:\n    Keeper = dataclass(Keeper)\n\n\ndef go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "a module rebound in an except arm the import path never reaches",
        "\n\ntry:\n    alias = config\nexcept ImportError:\n    alias = None\n\n\n"
        "def go(cfg):\n    alias.save(cfg)\n",
    ),
    (
        "a module bound before a branch that rebinds it",
        "\n\ndef go(spec, cfg):\n    view = config\n    if spec:\n        view = spec.view\n"
        "    return view.save(cfg)\n",
    ),
]


#: What the two fixes above must not cost. The first is that residual's own shape, which
#: stays quiet because it stays correct. The second and third are the shadows a
#: self rebinding must not weaken: a parameter of that name still takes it, and an
#: assignment that is not a self rebinding still does.
A_NAME_THAT_NO_LONGER_MEANS_ITS_CLASS = [
    (
        "two class definitions in ONE statement list",
        "\n\nclass Keeper:\n    mod = config\n\n\nclass Keeper:\n"
        "    def __init__(self, config):\n        self.mod = config\n\n\n"
        "def go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
    (
        "a parameter of that name, after a self rebinding",
        "\n\ndef go(config, cfg):\n    config = config\n    return config.save(cfg)\n",
    ),
    (
        "an ordinary rebinding beside a self rebinding of another name",
        "\n\ndef go(raw, cfg):\n    naming = naming\n    config = dict(raw)\n"
        "    return config.save(cfg)\n",
    ),
    (
        "a name whose ONLY binding is inside a branch is still taken",
        "\n\ndef go(rows, cfg):\n    if rows:\n        config = dict(rows)\n"
        "    return config.save(cfg)\n",
    ),
    (
        "a loop that rebinds the name, with the rebinding inside the body",
        "\n\ndef go(rows, cfg):\n    for row in rows:\n        config = row\n"
        "    return config.save(cfg)\n",
    ),
    (
        "an unconditional rebinding is still a veto, branch or no branch",
        "\n\ndef go(raw, cfg):\n    config = dict(raw)\n    if raw:\n        config = raw\n"
        "    return config.save(cfg)\n",
    ),
    (
        "a rebinding in a finally block, which every path runs",
        "\n\ndef go(fn, cfg):\n    alias = config\n    try:\n        fn()\n    finally:\n"
        "        alias = None\n    return alias.save(cfg)\n",
    ),
    (
        "an or expression that does not name the target is still a veto",
        "\n\ndef go(raw, cfg):\n    config = raw or {}\n    return config.save(cfg)\n",
    ),
    (
        "a conditional expression that does not name the target is still a veto",
        "\n\ndef go(raw, flag, cfg):\n    config = raw if flag else {}\n"
        "    return config.save(cfg)\n",
    ),
    (
        "a call that takes the target as an argument is still undecidable",
        "\n\nfrom dataclasses import dataclass\n\n\nclass Keeper:\n    mod = config\n\n\n"
        "Keeper = dataclass(Keeper)\n\n\ndef go(cfg):\n    Keeper.mod.save(cfg)\n",
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    A_NAME_THAT_STILL_MEANS_ITS_CLASS,
    ids=[one[0] for one in A_NAME_THAT_STILL_MEANS_ITS_CLASS],
)
def test_a_binding_that_replaced_nothing_leaves_the_name_alone(shape, snippet):
    """Two real writes filed as undecidable by the residual "A class rebound after
    its own definition is no longer reachable by name", one of which it called
    correct.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    A_NAME_THAT_NO_LONGER_MEANS_ITS_CLASS,
    ids=[one[0] for one in A_NAME_THAT_NO_LONGER_MEANS_ITS_CLASS],
)
def test_a_binding_that_really_replaced_something_still_takes_the_name(shape, snippet):
    """The quiet direction of the same two fixes, which is where they could go wrong."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_a_class_written_inside_a_factory_still_reaches_its_own_attribute():
    """The write the unique key must not cost, beside the false positive it fixes."""
    inside = """

def build(cfg):
    class Keeper:
        mod = config

        def go(self, cfg):
            self.mod.save(cfg)

    return Keeper
"""
    assert filesystem_mutations(AGING_SOURCE + inside)
    through_the_class = """

def build(cfg):
    class Keeper:
        mod = config

    Keeper.mod.save(cfg)
    return Keeper
"""
    assert filesystem_mutations(AGING_SOURCE + through_the_class)


def test_the_audit_names_a_writer_attached_to_a_class_after_the_fact():
    """``Row.go = _go`` through the audit, which reads one statement at a time."""
    attached = (
        "from cratekit.core import config\n\n\n"
        "def _go(self, cfg):\n"
        "    self.mod.save(cfg)\n\n\n"
        "class Row:\n"
        "    def __init__(self):\n"
        "        self.mod = config\n\n\n"
        "Row.go = _go\n"
    )
    assert _unnamed_writers("cratekit.core.naming", attached) == ["_go"]
    unattached = (
        "from cratekit.core import config\n\n\n"
        "def _go(self, cfg):\n"
        "    self.mod.save(cfg)\n\n\n"
        "class Row:\n"
        "    def __init__(self, mod):\n"
        "        self.mod = mod\n"
    )
    assert _unnamed_writers("cratekit.core.naming", unattached) == []


def test_the_audit_names_a_writer_a_subclass_reaches_through_its_base():
    """The same family resolution through the audit, whose owner is one statement."""
    inherited = (
        "from cratekit.core import config\n\n\n"
        "class Base:\n"
        "    mod = config\n\n\n"
        "class Row(Base):\n"
        "    def go(self, cfg):\n"
        "        self.mod.save(cfg)\n"
    )
    assert _unnamed_writers("cratekit.core.naming", inherited) == ["Row"]


#: A TYPE'S ATTRIBUTE MAPPING, reached through a BINDING rather than inline.
#: Round four caught ``vars(Path)["write_text"]`` with a receiver free rule that
#: fired on ``counts["rename"]`` too. Round five gave the rule its receiver and
#: read it off the subscript's own ``value``, which is one binding out: the round
#: built a binding table that follows ``alias = config`` and then did not ask it
#: about ``table = vars(Path)``.
NAMESPACE_REACHES_A_WRITER = [
    (
        "bound to a name from vars",
        '\n\ndef go(p, d):\n    table = vars(Path)\n    table["write_text"](p, d)\n',
    ),
    (
        "bound to a name from __dict__",
        '\n\ndef go(p, d):\n    table = Path.__dict__\n    table["write_text"](p, d)\n',
    ),
    (
        "asked rather than indexed",
        '\n\ndef go(p, d):\n    Path.__dict__.get("write_text")(p, d)\n',
    ),
    (
        "asked through a bound name",
        '\n\ndef go(p, d):\n    table = vars(Path)\n    table.pop("write_text")(p, d)\n',
    ),
    (
        "copied through dict()",
        '\n\ndef go(p, d):\n    dict(vars(Path))["write_text"](p, d)\n',
    ),
    (
        "copied through a spread literal",
        '\n\ndef go(p, d):\n    {**vars(Path)}["write_text"](p, d)\n',
    ),
    (
        "returned by a helper",
        '\n\ndef _table():\n    return vars(Path)\n\n\ndef go(p, d):\n    _table()["write_text"](p, d)\n',
    ),
    (
        "held in a container element",
        '\n\nTABLES = [vars(Path)]\n\n\ndef go(p, d):\n    TABLES[0]["write_text"](p, d)\n',
    ),
    (
        "stored on an instance",
        "\n\nclass Keeper:\n    def __init__(self):\n        self.table = vars(Path)\n\n"
        '    def go(self, p, d):\n        self.table["write_text"](p, d)\n',
    ),
    (
        "handed in as a default argument",
        '\n\ndef go(p, d, table=vars(Path)):\n    table["write_text"](p, d)\n',
    ),
    (
        "bound through a conditional",
        "\n\ndef go(p, d, flag):\n    table = vars(Path) if flag else Path.__dict__\n"
        '    table["write_text"](p, d)\n',
    ),
    (
        "bound through a loop over a literal",
        '\n\ndef go(p, d):\n    for table in [vars(Path)]:\n        table["write_text"](p, d)\n',
    ),
    (
        "a key this cannot read at all",
        '\n\ndef go(p, d):\n    Path.__dict__["write" + "_text"](p, d)\n',
    ),
    (
        "a generic writer named only by the module it belongs to",
        '\n\ndef go(cfg):\n    vars(config)["save"](cfg)\n',
    ),
    # FOUR SPELLINGS ONE OPERATOR OUT FROM ONES ALREADY HELD, and the reason the
    # rule stopped enumerating. ``dict(vars(Path))`` and ``{**vars(Path)}`` were
    # each written out by hand; a dict union and a ``.copy()`` are the same act
    # on the same object, they were measured quiet, and all three were executed
    # to confirm they write a real file. The ``ChainMap`` needs no forbidden
    # import either, because ``collections`` is on the allowlist.
    (
        "carried through a dict UNION",
        '\n\ndef go(p, d):\n    (Path.__dict__ | {})["write_text"](p, d)\n',
    ),
    (
        "carried through a COPY that takes no arguments",
        '\n\ndef go(p, d):\n    vars(Path).copy()["write_text"](p, d)\n',
    ),
    (
        "carried into a ChainMap",
        "\nfrom collections import ChainMap\n\n\n"
        'def go(p, d):\n    ChainMap(vars(Path))["write_text"](p, d)\n',
    ),
    (
        "carried through a KEYWORD spread",
        '\n\ndef go(p, d):\n    dict(**vars(Path))["write_text"](p, d)\n',
    ),
]

#: The same rule pointed at ordinary code, because a namespace binding that fires
#: on a dispatch table is round four's defect with a longer reach.
ORDINARY_LOOKUPS_THROUGH_A_BINDING = [
    (
        "a mapping bound to a name",
        '\n\ndef go(counts):\n    table = dict(counts)\n    return table["rename"]\n',
    ),
    (
        "a mapping literal bound to a name",
        '\n\ndef go():\n    table = {"unlink": 1}\n    return table["unlink"]\n',
    ),
    (
        "a spread of an ordinary mapping",
        '\n\ndef go(counts):\n    return {**counts}["rename"]\n',
    ),
    (
        "a namespace asked for a key that is not a writer",
        '\n\ndef go(spec):\n    return vars(spec).get("stale_days")\n',
    ),
    (
        "a namespace read for something else entirely",
        "\n\ndef go(spec):\n    return sorted(vars(spec))\n",
    ),
    (
        "a generic name on a namespace nobody admits",
        '\n\ndef go(view):\n    return vars(view)["save"]\n',
    ),
    # THE SAME MAPPING OPERATIONS ON AN ORDINARY MAPPING. Propagation is what
    # carries a namespace through a union, a copy and a constructor, and if it
    # carried mapping-ness itself rather than the namespace it found, every one
    # of these would be a finding on a dispatch table.
    (
        "an ordinary mapping through a union",
        '\n\ndef go(counts):\n    return (counts | {})["rename"]\n',
    ),
    (
        "an ordinary mapping copied",
        '\n\ndef go(counts):\n    return counts.copy()["rename"]\n',
    ),
    (
        "an ordinary mapping through a constructor",
        "\nfrom collections import ChainMap\n\n\n"
        'def go(counts):\n    return ChainMap(counts)["rename"]\n',
    ),
]


@pytest.mark.parametrize(
    "shape,snippet",
    NAMESPACE_REACHES_A_WRITER,
    ids=[one[0] for one in NAMESPACE_REACHES_A_WRITER],
)
def test_an_attribute_mapping_bound_to_a_name_is_still_that_mapping(shape, snippet):
    """Rule 5 asked of the table rather than of the expression under its own nose."""
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    ORDINARY_LOOKUPS_THROUGH_A_BINDING,
    ids=[one[0] for one in ORDINARY_LOOKUPS_THROUGH_A_BINDING],
)
def test_an_ordinary_mapping_bound_to_a_name_is_not_a_namespace(shape, snippet):
    """The receiver, still doing the separating once the receiver can be a binding."""
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_a_namespace_key_this_cannot_read_is_a_finding_only_where_writing_is_banned():
    """Rule 5's computed half, on the same switch rule 4's computed half is on."""
    computed = "\n\ndef go(p, d, name):\n    Path.__dict__[name](p, d)\n"
    assert filesystem_mutations(AGING_SOURCE + computed)
    assert (
        _unnamed_writers(
            "cratekit.core.naming",
            "def describe(spec, field):\n    return vars(spec)[field]\n",
        )
        == []
    )


def test_a_mapping_method_that_takes_no_argument_is_a_key_this_cannot_read():
    """The ASKED branch with no argument to read, which is its own act."""
    unread = "\n\ndef go():\n    return vars(Path).popitem()\n"
    assert filesystem_mutations(AGING_SOURCE + unread)
    assert (
        _unnamed_writers("cratekit.core.naming", "def go(spec):\n    return vars(spec).popitem()\n")
        == []
    )


def test_a_namespace_carried_through_a_copy_is_named_by_the_audit_too():
    """The propagation with no help from the reflection switch, which is its own act."""
    copied = 'from pathlib import Path\n\n\ndef stash(p, d):\n    vars(Path).copy()["write_text"](p, d)\n'
    assert _unnamed_writers("cratekit.core.naming", copied) == ["stash"]


def test_a_module_reached_through_the_globals_mapping_is_still_that_module():
    """The alias spelled as a lookup, which puts the module's name inside a string."""
    assert filesystem_mutations(
        AGING_SOURCE + '\n\ndef go(cfg):\n    globals()["config"].save(cfg)\n'
    )
    assert (
        filesystem_mutations(
            AGING_SOURCE + '\n\ndef go(view, cfg):\n    globals()["view"].save(cfg)\n'
        )
        == []
    )


#: Six more ways a scope takes a name back, each one the ONLY thing driving a
#: line of the shadow list. Some are odder than the ten above and they are
#: written out rather than argued: a shadow that nothing exercises is a shadow
#: somebody deletes, and this file has already shipped six of those.
SHADOWS_IN_A_SCOPE = [
    (
        "an import of something else under the same name",
        """from cratekit.core import config


def go(raw):
    import json as config

    return config.load
""",
    ),
    (
        "a class of the same name",
        """from cratekit.core import config


class config:
    pass


def go():
    return config.load
""",
    ),
    (
        "a nested definition of the same name",
        """from cratekit.core import config


def go(raw):
    def config():
        return dict(raw)

    return config.load
""",
    ),
    (
        "a starred unpacking target",
        """from cratekit.core import config


def go(rows):
    *config, last = rows
    return config.load, last
""",
    ),
    (
        "a definition of the same name beside the import",
        """from cratekit.core import config


def config():
    return {}


def go():
    return config.load
""",
    ),
]

#: The other direction of the same two lines: a scope that DOES still see the
#: module, where a shadow read one level too wide would lose the write.
WRITES_A_WIDER_SHADOW_WOULD_LOSE = [
    (
        "a comprehension target does not shadow the function around it",
        """from cratekit.core import config


def go(rows, cfg):
    names = [config for config in rows]
    config.save(cfg)
    return names
""",
    ),
    (
        "an object binding fed by another object binding, written out of order",
        """from cratekit.core import config


class Row:
    def load(self):
        self.mod = _mod()

    def use(self, cfg):
        self.mod.save(cfg)


def _mod():
    return config
""",
    ),
]


@pytest.mark.parametrize(
    "shape,source", SHADOWS_IN_A_SCOPE, ids=[one[0] for one in SHADOWS_IN_A_SCOPE]
)
def test_every_shadow_this_table_claims_takes_the_name_back(shape, source):
    """Four shadows nothing drove, which is four lines that read as coverage."""
    assert filesystem_mutations(source) == [], shape


def test_a_name_bound_twice_in_ONE_scope_settles_to_neither():
    """The FAILED ATTEMPT, driven where shadowing alone cannot answer it."""
    beside = (
        "from cratekit.core import config\n\n\n"
        'with open("defaults.json") as config:\n'
        "    DEFAULTS = config.read()\n\n\n"
        "def go(cfg):\n"
        "    config.save(cfg)\n"
    )
    assert filesystem_mutations(beside) == []
    alone = "from cratekit.core import config\n\n\ndef go(cfg):\n    config.save(cfg)\n"
    assert filesystem_mutations(alone)


@pytest.mark.parametrize(
    "shape,source",
    WRITES_A_WIDER_SHADOW_WOULD_LOSE,
    ids=[one[0] for one in WRITES_A_WIDER_SHADOW_WOULD_LOSE],
)
def test_a_shadow_read_too_wide_would_lose_a_real_write(shape, source):
    """The cost of getting the scope boundaries wrong, in the expensive direction."""
    assert filesystem_mutations(source), shape


#: A module that hides its writer behind an alias, which is the shape that
#: defeated the armed copy of U11's comma-separated-file guard.
EVASIVE_IMPORT = """
import shutil as tidy
from os import replace as swap


def clean(a, b):
    tidy.rmtree(a)
    swap(a, b)
"""

#: The same evasion one layer further out: the writer reached through the package
#: rather than through the module, which is the shape a layering-aware author
#: reaches for first.
EVASIVE_PACKAGE_IMPORT = """
from cratekit.core import rb_writer


def snapshot(cfg):
    return rb_writer.open_db(cfg)
"""

#: And through a relative import, which nothing in the package uses today.
EVASIVE_RELATIVE_IMPORT = """
from ...core import rb_writer


def snapshot(cfg):
    return rb_writer.open_db(cfg)
"""

#: The same writer reached through a LAZY import inside a function body, which is
#: the shape both of the source system's live layering violations take and the
#: reason ``tests/test_layering.py`` walks the whole tree rather than the header.
EVASIVE_LAZY_IMPORT = """
def snapshot(cfg):
    import sqlite3

    return sqlite3.connect(str(cfg.library.db_path))
"""

#: A module that writes a private ignore file, which is the exact defect the
#: countdown against this unit forbids by name.
EVASIVE_PRIVATE_LEDGER = """
from pathlib import Path


def remember(path, decided):
    Path(path).write_text(decided)
"""

#: The same thing through a handle, so the mutating method never appears.
EVASIVE_WRITE_HANDLE = """
from pathlib import Path


def remember(path, decided):
    with open(Path(path), "w") as handle:
        handle.write(decided)
"""

#: The same handle through the BOUND method, which is the idiomatic spelling and
#: is the one that got through: ``Path.open`` takes the mode as its first
#: argument because its receiver is already the file, so a guard reading position
#: one saw the default read mode and said nothing.
EVASIVE_BOUND_OPEN_HANDLE = """
from pathlib import Path


def remember(path, decided):
    handle = Path(path).open("w")
    handle.write(decided)
    handle.close()
"""

#: And with a mode this guard cannot read, which is how a literal check is walked
#: past without ever writing the letter w.
EVASIVE_COMPUTED_MODE = """
from pathlib import Path

MODE = "".join(["w"])


def remember(path, decided):
    with open(Path(path), MODE) as handle:
        handle.write(decided)
"""

#: ``Path.replace`` overwrites its destination without asking, which is strictly
#: worse than the ``rename`` sitting beside it in the mutation set, and it is
#: how a private ledger gets swapped into place atomically.
EVASIVE_PATH_REPLACE = """
from pathlib import Path


def remember(scratch, ledger):
    Path(scratch).replace(ledger)
"""

#: The writer loaded with no import statement at all. Three modules, because the
#: allowlist's whole argument is that nothing in it can open a database, spawn a
#: process, or touch a file, and the builtin reaches all three.
EVASIVE_DYNAMIC_IMPORT = """
def remember(path, argv, db):
    __import__("os").truncate(path, 0)
    __import__("subprocess").run(argv)
    return __import__("sqlite3").connect(db)
"""

#: The same builtin with a name this guard cannot read, which is the computed
#: mode's trick applied to the import instead of to the handle.
EVASIVE_COMPUTED_DYNAMIC_IMPORT = """
NAME = "".join(["o", "s"])


def remember(path):
    __import__(NAME).truncate(path, 0)
"""

#: The mutating method reached through a computed attribute name, so the method
#: never appears as text and the outer call's ``func`` is itself a Call.
EVASIVE_COMPUTED_ATTRIBUTE = """
from pathlib import Path


def remember(path, decided):
    getattr(Path(path), "write_" + "text")(decided)
"""

#: The mutating method BOUND AND NOT CALLED, then called through the local it
#: was bound to. Every mutating name has left the call positions the guard read,
#: which is round one's bound-``open`` hole one step further out.
EVASIVE_CAPTURED_BOUND_METHOD = """
from pathlib import Path


def remember(path, decided):
    keep = Path(path).write_text
    keep(decided)
"""

#: The writer reached through a module the ALLOWLIST admits, with no forbidden
#: import anywhere in the file. ``config.save`` writes the configuration file and
#: ``config.load_from_path`` writes it back too, which its name does not say.
EVASIVE_ALLOWLISTED_WRITER = """
from cratekit.core import config


def remember(cfg, path):
    config.save(cfg)
    return config.load_from_path(path)
"""

#: And through the other admitted module that opens a file for writing.
#: ``duplicates`` already imports ``cratekit.core.naming`` for the head stripping,
#: so this one needs no new import at all.
EVASIVE_ALLOWLISTED_CLAIM = """
from cratekit.core import naming


def remember(target):
    return naming.claim_target(target)
"""

#: The admitted writer reached through an ALIASED MODULE, which is what the
#: receiver check has to survive to be worth having. The word ``config`` appears
#: nowhere beside the call, and an alias is the shape that has already defeated a
#: guard in this repository once.
EVASIVE_ALIASED_ALLOWLISTED_WRITER = """
from cratekit.core import config as settings


def remember(cfg):
    settings.save(cfg)
"""

#: The admitted writer imported STRAIGHT OFF its module and renamed, so there is
#: no receiver to qualify at all. Both halves of that import are permitted, and
#: making the generic names receiver qualified is exactly what would lose this
#: shape if the bare local were not tracked back to what it was bound to.
EVASIVE_IMPORTED_ALLOWLISTED_WRITER = """
from cratekit.core.naming import claim_target as reserve


def remember(target):
    return reserve(target)
"""

#: The mutating name reached as a BARE CALL, with the attribute the widened rule
#: reads nowhere in the file. Every other planted module here reaches its writer
#: through an attribute, so this is the only thing driving the bare-name branch,
#: and until it existed that branch could be deleted with the suite green. The
#: import guard catches this file too, which is the point: the two rules are not
#: supposed to depend on each other.
EVASIVE_BARE_NAME_WRITER = """
from shutil import rmtree
from os import truncate


def clean(a, path):
    rmtree(a)
    truncate(path, 0)
"""

#: The mutating method named as a LITERAL string inside ``getattr``. It never
#: appears as an attribute, so rule 1 cannot see it, and the mode and arity rules
#: have nothing to read. Only the literal half of rule 4 catches it, and that
#: half had no fixture at all: ``CORRECT_MODULE`` exercises it in the negative
#: with ``getattr(review, "Queue")`` and nothing exercised it in the positive.
EVASIVE_LITERAL_GETATTR = """
from pathlib import Path


def remember(path, decided):
    getattr(Path(path), "write_text")(decided)
"""

#: The same trick pointed at a writer the ALLOWLIST admits, so the receiver has
#: to be read inside ``getattr`` as well as outside it.
EVASIVE_LITERAL_GETATTR_ON_AN_ADMITTED_MODULE = """
from cratekit.core import config


def remember(cfg):
    getattr(config, "save")(cfg)
"""

#: THE NINE SHAPES A RECEIVER CHECK READ OFF THE IMPORT TABLE ALONE LOST.
EVASIVE_REBOUND_ALLOWLISTED_WRITER = """
from cratekit.core import config


def remember(cfg):
    alias = config
    alias.save(cfg)
"""

#: The module reached through its own DOTTED PATH after a plain ``import``,
#: which is the one receiver shape that names no local at all. Round three read
#: it off the attribute chain's last name, and that reading is what fired on
#: ``row.config`` and ``view.naming``; resolving it as a BINDING instead keeps
#: this shape and drops those, and without a fixture the swap would have lost it
#: silently, which is the relocation failure a fix round is for.
EVASIVE_DOTTED_IMPORT_ALLOWLISTED_WRITER = """
import cratekit.core.config


def remember(cfg):
    cratekit.core.config.save(cfg)
"""

#: The module parked in a LIST and reached by index.
EVASIVE_ALLOWLISTED_WRITER_IN_A_LIST = """
from cratekit.core import config

MODS = [config]


def remember(cfg):
    MODS[0].save(cfg)
"""

#: The module parked in a DICT, reaching the writer whose name reads as a load.
EVASIVE_ALLOWLISTED_WRITER_IN_A_DICT = """
from cratekit.core import config

MODS = {"c": config}


def remember(path):
    return MODS["c"].load_from_path(path)
"""

#: The module HANDED BACK by a function, so the receiver is a call result.
EVASIVE_ALLOWLISTED_WRITER_FROM_A_CALL = """
from cratekit.core import config


def _mod():
    return config


def remember(cfg):
    _mod().save(cfg)
"""

#: The module reached through a LOOP VARIABLE.
EVASIVE_ALLOWLISTED_WRITER_IN_A_LOOP = """
from cratekit.core import config


def remember(cfg):
    for mod in (config,):
        mod.save(cfg)
"""

#: The module injected as a DEFAULT ARGUMENT, which is how a module gets swapped
#: out for a test and is the one shape where a parameter name is not a shadow.
EVASIVE_ALLOWLISTED_WRITER_AS_A_DEFAULT = """
from cratekit.core import config


def remember(cfg, mod=config):
    mod.save(cfg)
"""

#: The module STORED ON AN INSTANCE in one method and used in another, which is
#: an ordinary constructor and is why a parameter shadows its own name only.
EVASIVE_ALLOWLISTED_WRITER_ON_AN_ATTRIBUTE = """
from cratekit.core import config


class Keeper:
    def __init__(self):
        self.mod = config

    def remember(self, cfg):
        self.mod.save(cfg)
"""

#: The module bound by a WALRUS, which is a rebinding written inside the
#: expression that uses it and has no assignment statement to read.
EVASIVE_WALRUS_BOUND_ALLOWLISTED_WRITER = """
from cratekit.core import config


def remember(cfg):
    if (alias := config) is not None:
        alias.save(cfg)
"""

#: And bound by a COMPREHENSION, which is a loop with no ``for`` statement.
EVASIVE_COMPREHENSION_BOUND_ALLOWLISTED_WRITER = """
from cratekit.core import config


def remember(cfg):
    return [mod.save(cfg) for mod in (config,)]
"""

#: The rebound module reached through ``getattr``, so the receiver has to be
#: resolved by binding inside rule 4 as well as outside it.
EVASIVE_REBOUND_WRITER_THROUGH_GETATTR = """
from cratekit.core import config


def remember(cfg):
    alias = config
    getattr(alias, "save")(cfg)
"""

#: A STAR import, which binds every writer the module exposes with no name in the
#: file for a check to read. Both halves of the import are permitted.
EVASIVE_STAR_IMPORTED_ALLOWLISTED_WRITER = """
from cratekit.core.config import *


def remember(cfg):
    save(cfg)
"""

#: THE FOUR SPELLINGS THAT REACH A METHOD WITHOUT NAMING IT AS AN ATTRIBUTE.
EVASIVE_TYPE_DICT_SUBSCRIPT = """
from pathlib import Path


def remember(path, decided):
    Path.__dict__["write_text"](path, decided)
"""

#: The same function object through ``vars``, so even ``__dict__`` is gone.
EVASIVE_VARS_SUBSCRIPT = """
from pathlib import Path


def remember(path, decided):
    vars(Path)["write_text"](path, decided)
"""

#: The UNBOUND dunder ``getattr`` itself calls, which takes the receiver first.
EVASIVE_UNBOUND_GETATTRIBUTE = """
def remember(path, decided):
    object.__getattribute__(path, "write_text")(decided)
"""

#: And the BOUND one, which has spent its receiver on the attribute it was
#: reached through, so its single argument is the method name. The arity is what
#: separates the two, which is the reading ``replace`` already gets.
EVASIVE_BOUND_GETATTRIBUTE = """
def remember(path, decided):
    path.__getattribute__("write_text")(decided)
"""

#: A private ledger in a SIBLING module whose name merely starts with this
#: package's. It is not inside the package, so ``_report_modules`` never scans
#: it, and the bare-prefix allowlist waved the import through, which is the pair
#: of holes that let it be written, imported and called with both guards green.
EVASIVE_SIBLING_PACKAGE = """
from cratekit.modules import reports_ledger


def remember(path, decided):
    reports_ledger.remember(path, decided)
"""

#: Correct code, in both directions: the one persistence this package is allowed,
#: a read through every read primitive available including a BOUND READ METHOD
#: captured before it is called, and the methods whose names collide with
#: filesystem verbs. ``dataclasses.replace`` is the third of those and is the one
#: that matters, because ``dataclasses`` is on the allowlist while ``str`` and
#: ``date`` merely turn up: it takes one positional argument, so only the
#: keywords beside it keep the arity rule off correct code.
CORRECT_MODULE = """
import dataclasses
from pathlib import Path

from cratekit.core import review
from cratekit.core.review import Option


def run(store, path, name, today, option):
    content = Path(path).read_bytes()
    bound = Path(path).open("rb")
    bound.close()
    builtin = open(path, "rb")
    builtin.close()
    reader = Path(path).read_text
    reader()
    tidied = name.replace("_", " ").casefold()
    first_of_month = today.replace(day=1)
    renamed = dataclasses.replace(option, summary=tidied)
    queue = getattr(review, "Queue")
    assert renamed is not None
    return review.offer(
        store,
        queue=queue.DUPLICATES,
        kind="duplicate-recording",
        identity={"title": tidied},
        payload={"bytes": len(content), "month": str(first_of_month)},
        options=(Option(option_id="1", summary=tidied),),
    )
"""

#: Correct code that imports a SIBLING module of this package, the shape the dot
#: boundary must keep legal. Nothing here uses one today; a guard that failed the
#: first correct one is a guard that gets deleted rather than obeyed (P7).
CORRECT_IN_PACKAGE_IMPORT = """
from cratekit.modules.reports import aging
from cratekit.modules.reports.export import LibraryView


def run(view: LibraryView, intake, today):
    return aging.intake_groupings(view, intake=intake, today=today)
"""

#: Correct code whose attribute names COLLIDE with the generic writers, which is
#: the shape the receiver check exists for. A view that can save itself, a
#: taxonomy loaded from a call, and a spec field read off a parameter are three
#: ordinary things, and while ``load`` and ``save`` sat bare in the mutation set
#: all three were reported as writes to the library. Nothing in the tree spells
#: any of them today, which is the only reason the suite was green, and a guard
#: that fires the first time somebody writes correct code is one that gets
#: deleted rather than obeyed (P7).
CORRECT_GENERIC_ATTRIBUTE_NAMES = """
from cratekit.core import taxonomy


def describe(view, spec):
    saved = view.save
    loaded = taxonomy.default_taxonomy().load
    return saved, loaded, spec.load
"""

#: THE FIVE FALSE POSITIVES THE RECEIVER CHECK WAS FIRING TODAY, and they are
#: the same P7 shape as the one above moved one level along.
CORRECT_UNBOUND_RECEIVERS_NAMED_LIKE_MODULES = """
def describe(config, naming, row, view, target):
    first = config.load
    second = row.config.load_from_path(target)
    third = view.naming.claim_target(target)
    return first, second, third, naming.claim_target(target)
"""

#: The harder half of the same thing: a module that really does import ``config``
#: AND takes a parameter of that name, which ``aging`` is two characters away
#: from being. A parameter SHADOWS, and without that the fix for the five above
#: would have been a fix that only worked in files with no import in them.
CORRECT_PARAMETER_SHADOWING_AN_IMPORTED_MODULE = """
from cratekit.core import config


def describe(config, spec):
    return config.load, config.save, spec.load


def elsewhere(cfg):
    return config.state_path("x", cfg)
"""

#: A method whose ``self`` is a parameter, reading an attribute named after an
#: admitted module. Every method carries ``self``, so a shadow rule that took the
#: whole chain would have lost ``self.mod = config`` in a constructor; this is
#: the direction that rule must NOT break.
CORRECT_ATTRIBUTE_NAMED_LIKE_A_MODULE = """
class View:
    def describe(self):
        return self.config.load, self.naming.claim_target
"""

#: A LAMBDA whose parameter is named after an admitted module, in a file that
#: imports that module. A lambda carries a parameter list and therefore shadows,
#: and it is the one scope with no statement body for a walk to notice.
CORRECT_LAMBDA_PARAMETER_SHADOWING_A_MODULE = """
from cratekit.core import config

describe = lambda config: config.load
"""


@pytest.mark.parametrize(
    "source",
    [
        EVASIVE_IMPORT,
        EVASIVE_PACKAGE_IMPORT,
        EVASIVE_RELATIVE_IMPORT,
        EVASIVE_LAZY_IMPORT,
        EVASIVE_DYNAMIC_IMPORT,
        EVASIVE_COMPUTED_DYNAMIC_IMPORT,
        EVASIVE_SIBLING_PACKAGE,
    ],
)
def test_the_import_allowlist_bites_every_shape_of_the_evasion(source):
    """P7's first half, run against the thing the guard exists to catch."""
    assert forbidden_imports(source, "cratekit.modules.reports.planted")


@pytest.mark.parametrize(
    "source",
    [
        EVASIVE_PRIVATE_LEDGER,
        EVASIVE_WRITE_HANDLE,
        EVASIVE_BOUND_OPEN_HANDLE,
        EVASIVE_COMPUTED_MODE,
        EVASIVE_PATH_REPLACE,
        EVASIVE_COMPUTED_ATTRIBUTE,
        EVASIVE_CAPTURED_BOUND_METHOD,
        EVASIVE_ALLOWLISTED_WRITER,
        EVASIVE_ALLOWLISTED_CLAIM,
        EVASIVE_ALIASED_ALLOWLISTED_WRITER,
        EVASIVE_IMPORTED_ALLOWLISTED_WRITER,
        EVASIVE_BARE_NAME_WRITER,
        EVASIVE_LITERAL_GETATTR,
        EVASIVE_LITERAL_GETATTR_ON_AN_ADMITTED_MODULE,
        EVASIVE_REBOUND_ALLOWLISTED_WRITER,
        EVASIVE_DOTTED_IMPORT_ALLOWLISTED_WRITER,
        EVASIVE_ALLOWLISTED_WRITER_IN_A_LIST,
        EVASIVE_ALLOWLISTED_WRITER_IN_A_DICT,
        EVASIVE_ALLOWLISTED_WRITER_FROM_A_CALL,
        EVASIVE_ALLOWLISTED_WRITER_IN_A_LOOP,
        EVASIVE_ALLOWLISTED_WRITER_AS_A_DEFAULT,
        EVASIVE_ALLOWLISTED_WRITER_ON_AN_ATTRIBUTE,
        EVASIVE_WALRUS_BOUND_ALLOWLISTED_WRITER,
        EVASIVE_COMPREHENSION_BOUND_ALLOWLISTED_WRITER,
        EVASIVE_REBOUND_WRITER_THROUGH_GETATTR,
        EVASIVE_STAR_IMPORTED_ALLOWLISTED_WRITER,
        EVASIVE_TYPE_DICT_SUBSCRIPT,
        EVASIVE_VARS_SUBSCRIPT,
        EVASIVE_UNBOUND_GETATTRIBUTE,
        EVASIVE_BOUND_GETATTRIBUTE,
    ],
)
def test_the_mutation_guard_bites_the_private_ledger_in_every_shape(source):
    """Twenty seven spellings of one act, six of which used to pass."""
    assert filesystem_mutations(source)


#: Every name ``FILESYSTEM_MUTATIONS`` carries, WRITTEN OUT A SECOND TIME.
_EVERY_MUTATING_NAME = (
    "append_durable_bytes",
    "atomic_write_bytes",
    "chmod",
    "hardlink_to",
    "lchmod",
    "mkdir",
    "rename",
    "rmdir",
    "rmtree",
    "symlink_to",
    "touch",
    "truncate",
    "unlink",
    "write_bytes",
    "write_text",
)

#: Every character ``_WRITING_MODES`` carries, on the same terms and for the same
#: reason: only ``w`` was driven, so ``open(p, "a")`` and ``open(p, "r+")`` rested
#: on set members nothing exercised.
_EVERY_WRITING_MODE = ("w", "a", "x", "+")

#: A mode each of those characters really appears in. ``+`` is never a mode by
#: itself, so it is driven where it is actually written.
_MODES_THAT_WRITE = ("w", "a", "x", "r+", "w+b", "ab")

#: Modes that must stay quiet, because a guard that fires on ``open(p, "rb")`` is
#: a guard somebody routes around (P7) and this package reads files for a living.
_MODES_THAT_READ = ("r", "rb")


def test_the_mutation_set_is_the_list_this_suite_drives():
    """The two spellings of the same set, held together."""
    assert set(_EVERY_MUTATING_NAME) == FILESYSTEM_MUTATIONS


def test_the_writing_modes_are_the_list_this_suite_drives():
    """The same holding, for the mode characters."""
    assert set(_EVERY_WRITING_MODE) == _WRITING_MODES


@pytest.mark.parametrize("verb", _EVERY_MUTATING_NAME)
def test_every_mutating_name_is_caught_on_its_own(verb):
    """One case per member, so each member DIES ALONE."""
    assert filesystem_mutations(f"def remember(path):\n    path.{verb}()\n") == [f"line 2: {verb}"]


@pytest.mark.parametrize("mode", _MODES_THAT_WRITE)
def test_open_is_caught_in_every_mode_that_can_write(mode):
    """``a``, ``x`` and ``+`` were carried by the set and driven by nothing."""
    assert filesystem_mutations(f'def remember(path):\n    return open(path, "{mode}")\n')


@pytest.mark.parametrize("mode", _MODES_THAT_READ)
def test_open_stays_quiet_in_a_mode_that_only_reads(mode):
    """The other direction, which is the one that gets a guard switched off."""
    assert filesystem_mutations(f'def remember(path):\n    return open(path, "{mode}")\n') == []


def test_a_dynamic_import_this_cannot_read_is_reported_as_unnameable():
    """A computed module name gets the computed mode's answer, not the benefit."""
    assert forbidden_imports(
        EVASIVE_COMPUTED_DYNAMIC_IMPORT, "cratekit.modules.reports.planted"
    ) == [_COMPUTED_IMPORT]


@pytest.mark.parametrize(
    "source",
    [
        CORRECT_MODULE,
        CORRECT_IN_PACKAGE_IMPORT,
        CORRECT_GENERIC_ATTRIBUTE_NAMES,
        CORRECT_UNBOUND_RECEIVERS_NAMED_LIKE_MODULES,
        CORRECT_PARAMETER_SHADOWING_AN_IMPORTED_MODULE,
        CORRECT_ATTRIBUTE_NAMED_LIKE_A_MODULE,
        CORRECT_LAMBDA_PARAMETER_SHADOWING_A_MODULE,
    ],
)
def test_the_guards_stay_quiet_on_correct_code(source):
    """P7's second half, which is the half that keeps getting skipped."""
    assert forbidden_imports(source, "cratekit.modules.reports.planted") == []
    assert filesystem_mutations(source) == []


def test_the_package_initializer_may_import_its_own_siblings_relatively():
    """The false positive the dotted-name shortcut would have produced."""
    resolved = _resolved_imports(
        "from . import aging\nfrom .export import LibraryView\n", REPORTS_PACKAGE
    )
    assert resolved == [f"{REPORTS_PACKAGE}.aging", f"{REPORTS_PACKAGE}.export"]
    assert forbidden_imports("from . import aging\n", REPORTS_PACKAGE) == []


def test_a_from_import_of_a_package_resolves_to_the_module_it_names():
    """``_PACKAGE_DEPTH``, which round one's filesystem read quietly subsumed."""
    planted = "cratekit.modules.reports.planted"
    assert _resolved_imports("from collections import abc\n", planted) == ["collections.abc"]
    assert _resolved_imports("from cratekit.core import review\n", planted) == [
        "cratekit.core.review"
    ]
    assert _resolved_imports("from cratekit.core.review import Option\n", planted) == [
        "cratekit.core.review"
    ]


def test_the_real_package_reaches_the_review_queue_at_all():
    """Otherwise the two guards above are satisfied by a package that does nothing."""
    reached = [
        module
        for module, source in _report_modules()
        if "cratekit.core.review" in _resolved_imports(source, module)
    ]
    assert reached == ["cratekit.modules.reports.duplicates"]


def test_the_package_is_gated_by_declared_module_toggles():
    """R5: both rows are Module rather than Core, so both need a toggle to follow."""
    from cratekit.core import profiles

    assert {"duplicates", "reports"} <= set(profiles.MODULES)
    assert not ({"duplicates", "reports"} & profiles.PROFILES["slim"])
    assert {"duplicates", "reports"} <= profiles.PROFILES["full"]


def test_the_reports_never_name_a_taxonomy_display_name():
    """R19 from the other side. The guard in test_layering only covers LOWER layers."""
    displays = {node.display for node in (default_taxonomy().intake, default_taxonomy().tree)}
    displays |= {bucket.display for bucket in default_taxonomy().buckets}
    for module, source in _report_modules():
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert node.value not in displays, (
                    f"{module} spells the taxonomy display name {node.value!r}; "
                    f"the declared node is a parameter, not a literal (R19)"
                )


def test_the_intake_node_is_a_declared_taxonomy_node_rather_than_a_name(view, cfg):
    """A second taxonomy gets a second answer, which is what R19 is worth."""
    renamed = taxonomy.Node(id=INTAKE.id, display="Deep House")
    groupings = aging.intake_groupings(view, intake=renamed, today=TODAY)
    assert [group.display for group in groupings] == ["High"]


def test_a_declared_intake_flow_that_is_nowhere_in_the_tree_refuses(view):
    """Absent is not empty, and rendering them the same way is the whole defect."""
    absent = taxonomy.Node(id=INTAKE.id, display="Bandcamp Queue")
    with pytest.raises(CratekitError) as raised:
        aging.intake_groupings(view, intake=absent, today=TODAY)
    assert raised.value.cause.reason == "intake-flow-absent"
    assert raised.value.cause.detail["declared"] == "Bandcamp Queue"


def test_an_intake_flow_nested_inside_another_folder_is_still_the_intake_flow():
    """The filter used to be anchored at position zero of the path."""
    tracks = [(1, "n", "a", "file://localhost/library/a.flac")]
    root_children = [
        _folder("Old", 1, 1),
        _folder(INTAKE.display, 1, 2),
        *_playlist("phil_1_1_26", [1], 3),
        _close(2),
        _close(1),
        _folder(INTAKE.display, 1, 1),
        *_playlist("phil_2_1_26", [1], 2),
        _close(1),
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=root_children, root_count=2)
    )
    groupings = aging.intake_groupings(view, intake=INTAKE, today=TODAY)
    assert {group.path for group in groupings} == {
        ("Old", INTAKE.display, "phil_1_1_26"),
        (INTAKE.display, "phil_2_1_26"),
    }


def test_an_intake_flow_holding_only_the_nested_one_is_still_found():
    """The reviewer's sharper case: the report used to be completely silent."""
    tracks = [(1, "n", "a", "file://localhost/library/a.flac")]
    root_children = [
        _folder("Old", 1, 1),
        _folder(INTAKE.display, 1, 2),
        *_playlist("phil_1_1_26", [1], 3),
        _close(2),
        _close(1),
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=root_children, root_count=1)
    )
    groupings = aging.intake_groupings(view, intake=INTAKE, today=TODAY)
    assert [group.display for group in groupings] == ["phil_1_1_26"]


def test_an_intake_flow_present_and_empty_reports_nothing_without_refusing(cfg):
    """The other side of the refusal, and the reason it needs the folder list."""
    view = export.read_export(
        _document(
            collection=_collection([]),
            root_children=[_folder(INTAKE.display, 0, 1), _close(1)],
            root_count=1,
        )
    )
    report = aging.intake_aging(
        view, intake=INTAKE, thresholds=aging.thresholds_from(cfg), today=TODAY
    )
    assert report.groupings == ()


def test_a_grouping_dated_in_the_future_is_undated_rather_than_permanently_current():
    """A typo in a year must not buy a grouping immunity from the report."""
    tracks = [(1, "n", "a", "file://localhost/library/a.flac")]
    root_children = [
        _folder(INTAKE.display, 1, 1),
        *_playlist("phil_1_5_99", [1], 2),
        _close(1),
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=root_children, root_count=1)
    )
    report = aging.intake_aging(
        view,
        intake=INTAKE,
        thresholds=aging.AgingThresholds(stale_days=30, expired_days=90),
        today=TODAY,
    )
    assert [group.display for group in report.undated] == ["phil_1_5_99"]
    assert report.current == ()
    assert report.undated[0].age_days is None
    assert report.undated[0].intake_date is None
