"""U34: the read-only library reports, and the promise that they are read-only.

The plan gives this unit four test scenarios, and each one has a test named after
it below:

1. both modules' outputs are review-queue items, not files;
2. the duplicate audit never deletes and its ignore list persists across runs and
   processes;
3. duplicates across two folders are detected, not only within one playlist;
4. aging thresholds come from config, not from a hardcoded policy.

Scenario 1 is the one worth reading carefully, because the honest answer to it is
not "yes" for both modules and the difference is a decision rather than a gap.
``core.review`` declares the split R12 rests on: a question a person must ANSWER
becomes a persisted review item, and a result a person merely READS stays an
output. The duplicate audit is the first and offers into ``Queue.DUPLICATES``;
the intake aging report is the second, and the verb registry has said so since U5
by declaring it ``emits={"diagnostic"}`` with ``adjudicates=False``. What both
modules owe, and what is asserted here in full, is the half of the scenario that
is really load bearing: **neither one writes a file of its own**, which is the
private-ledger shape R12 exists to remove and which the source system has one of.

THE READ-ONLY PROMISE IS PROVED TWICE, on purpose, because neither proof alone is
enough. Behaviourally, a report runs over a whole synthetic library and every
byte on disk and every database row is compared before and after. Structurally,
the package's own syntax tree is walked and held to an import allowlist and to a
rule about filesystem mutation, so a write on a path no test exercises is caught
too. The behavioural half can only see the paths the test drives; the structural
half can only see what it knows how to name. Together they cover what a reviewer
would otherwise have to take on trust.
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


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures: a whole synthetic library, in bytes
# ═══════════════════════════════════════════════════════════════════════════


def _collection(tracks: list[tuple[int, str, str, str]], *, declared: int | None = None) -> list[str]:
    """The COLLECTION section for ``(track_id, name, artist, location)`` rows.

    ``declared`` overrides the entry count, which is the only way to build the
    truncated document the reader has to refuse.
    """
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
    """One export carrying every shape the two reports have to handle.

    Two copies of one recording filed under two DIFFERENT genre folders (1 and
    4), one unique track, one entry with nothing to compare, and an intake flow
    holding groupings of four different ages plus one nested a level deeper.
    """
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
    return _document(
        collection=_collection(tracks), root_children=root_children, root_count=2
    )


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library, saved, so a second process resolves the same one.

    The environment variable is set as well as the file, because the suite's
    isolation fixture already points the library root somewhere and ``from_dict``
    relocates a configured root onto whatever the environment says. Writing only
    the file would leave the value under test and the value in force as two
    different directories, which is P2 exactly.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The export reader: a wrong document is never an empty library
# ═══════════════════════════════════════════════════════════════════════════


def test_a_document_that_is_not_an_export_refuses_rather_than_reading_as_empty():
    """The U11 shape, one package along.

    There, a store reader caught only a parse error, so every well-formed
    document that was not the store read as "nothing is suppressed". Here the
    equivalent is worse in one way: the correct answer for a clean library is
    also "nothing", so a report over the wrong file is indistinguishable from a
    report over a library with nothing wrong with it.
    """
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
    """Something else that happens to contain both names is not a damaged export.

    The check that the sections sit INSIDE the document element killed no test
    when it was reverted, so the inline comment explaining it was the only thing
    holding it up. The shape is real: concatenate a fragment of an export onto
    the front of anything and the two leads are both present, in a file where
    the collection is not part of any document this build understands.
    """
    body = _document(collection=_collection([]), root_children=[], root_count=0)
    opening = b'<DJ_PLAYLISTS Version="1.0.0">\r\n'
    section = b'  <COLLECTION Entries="0">\r\n  </COLLECTION>\r\n'
    assert section in body and opening in body
    moved = body.replace(section, b"").replace(opening, section + opening)

    with pytest.raises(CratekitError) as raised:
        export.read_export(moved)
    assert "outside the document element" in raised.value.cause.message


def test_the_entry_count_is_read_from_the_section_and_never_from_a_track():
    """The window that bounds the attribute search, which nothing used to reach.

    ``attribute_span`` returns the FIRST match in the window it is given, so
    widening the window changes nothing while the COLLECTION tag carries its own
    count. The case that separates them is a section that carries NONE, where an
    unbounded search walks on into the tracks and reads a number out of a value
    somebody typed. The document below is malformed, deliberately: an unescaped
    quote inside a display name is exactly the class of file this reader exists
    to refuse over, and the refusal has to be "no entry count" rather than a
    count invented from a track's name.
    """
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
    """The half-copied file, which is the case the count check exists for.

    A document that says it holds four tracks and holds one was not exported that
    way. Reporting on the one is not a smaller answer, it is a wrong one, and
    every duplicate the missing three were part of silently stops existing.
    """
    content = _document(
        collection=_collection(
            [(1, "a", "b", "file://localhost/library/a.flac")], declared=4
        ),
        root_children=[],
        root_count=0,
    )
    with pytest.raises(CratekitError) as raised:
        export.read_export(content)
    assert raised.value.cause.detail["declared"] == 4
    assert raised.value.cause.detail["located"] == 1


def test_a_track_element_with_no_identifier_makes_the_count_disagree():
    """The other way a document can be wrong while looking well formed.

    A row with no ``TrackID`` cannot be addressed by anything, so the byte engine
    drops it. Dropping it silently would mean the reader saw fewer tracks than
    the library holds and reported on the difference as though it were the whole
    thing, which is the same failure as a truncated file with a different cause.
    """
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
    """The shape a REAL export has, which a minimal fixture does not.

    rekordbox writes a collection track's attributes across several lines with a
    separate close tag. A reader that bounded the open tag at the next angle
    bracket, or the element at the next self-closing slash, would take the first
    line's attributes and miss the rest, and the failure would look like a
    library full of tracks with no artist.
    """
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
    """An identifier is what every later answer is addressed BY.

    A duplicate group offers one option per copy keyed on the track id, so two
    rows sharing one identifier produce two options a person cannot tell apart,
    and an ACCEPTED verdict naming that option says nothing about which copy
    survives. The deletion surface would then be licensed by an answer that is
    ambiguous rather than by one that is wrong, and only one of those two can be
    argued with afterwards.
    """
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
    """Carried because an absent structure and an empty one are not one fact.

    A folder holds no tracks, so it never becomes a playlist, and a report with
    only the playlists cannot tell an intake flow that was emptied from one that
    was never exported. Both would render as nothing to do.
    """
    assert view.has_folder(INTAKE.display)
    assert view.has_folder("Old")
    assert not view.has_folder("Bandcamp Queue")


def test_a_genuinely_empty_library_reads_as_empty_rather_than_refusing():
    """P7's other half: the guard must not fire on the correct document.

    A new user's library really is empty, and a reader that refused it would send
    somebody to re-export a file that was right the first time.
    """
    view = export.read_export(
        _document(collection=_collection([]), root_children=[], root_count=0)
    )
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
#:
#: THE SUBSTITUTION IS APPLIED TO THE PLAYLISTS, not to the folders, because that
#: is the direction with the cost: a folder misread as a folder changes nothing,
#: and a playlist misread as a folder takes its groupings and its memberships out
#: of the report while leaving its path in the tuple the guard consults.
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
def test_a_node_whose_kind_cannot_be_read_refuses_rather_than_reading_as_a_folder(
    old, new, cfg
):
    """The two answers side by side, which is the whole finding.

    The same tree twice: once as it ships, where the intake report names one
    expired grouping and two stale ones, and once with the kinds unreadable,
    where the classification that shipped answered FOLDER to every node, found no
    playlists at all, and rendered a clean queue over a library it could not read.

    The healthy half is asserted here rather than left to the other tests
    because a refusal that also refuses the correct document is worthless (P7),
    and because the pair is what makes the cost legible: the difference between
    the two runs is one attribute value, and the report's answer went from "act
    on these three" to "there is nothing to do".
    """
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
    """Every node a "playlist, or else a folder" rule would have filed as a folder.

    Derived from the real document rather than typed, so the view below holds
    exactly what the classification that shipped would have put in it.
    """
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
    """Why one more check inside the aging report could not have closed this.

    ``has_folder`` exists so that "the intake flow is not in this tree" and "it is
    here and it is empty" cannot render identically. It is satisfied on both
    routes, and neither one is a folder the report can trust:

    * with only the playlists unreadable, the intake folder is still a real
      folder, so the guard answers yes on a structure that is genuinely there and
      every grouping under it has silently stopped existing;
    * with every node unreadable, the intake folder is misread too, and the path
      it pushes into ``folders`` as a misread node is what satisfies the guard.

    Driven rather than argued, through the still-live aging code, which renders
    both as a clear queue and refuses nothing. That is the third state, and no
    guard downstream of the classification can tell it from the second.
    """
    content = library_export()
    for old, new in substitutions:
        assert old in content, "the substitution matched nothing"
        content = content.replace(old, new)

    root = rbxml.root_node(content)
    assert root is not None
    kinds = {
        path[-1]: rbxml.node_kind(node.node_type)
        for path, node in rbxml.walk_nodes(content, root)
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
    """The other side of the same classification, so it cannot be vacuous.

    A three valued kind whose third value is never reached on a real document is
    worth nothing, and a third value the healthy document reaches would refuse
    every export this product writes. Both halves are asserted against the tree
    the writers actually emit.
    """
    content = library_export()
    root = rbxml.root_node(content)
    assert root is not None
    kinds = {
        rbxml.node_kind(node.node_type) for _, node in rbxml.walk_nodes(content, root)
    }
    assert kinds == {rbxml.KIND_FOLDER, rbxml.KIND_PLAYLIST}


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 3: duplicates across two folders, not only within one playlist
# ═══════════════════════════════════════════════════════════════════════════


def test_duplicates_across_two_folders_are_detected(view):
    """The case the source system cannot see at all.

    Its audit walks one playlist and reports a track id present in it twice, so
    two separate collection rows for one recording, filed under two different
    genre folders, are invisible by construction. That is also the case a library
    actually accumulates.
    """
    groups = duplicates.audit(view, template=TEMPLATE)
    assert len(groups) == 1
    group = groups[0]
    assert {member.track_id for member in group.members} == {"1", "4"}
    assert group.spans_playlists
    placements = {path for member in group.members for path in member.playlists}
    assert (TREE.display, "Deep House", "High") in placements
    assert (TREE.display, "Melodic House", "Med") in placements


def test_two_copies_are_one_recording_across_head_marker_case_and_spacing(view):
    """Every difference between the two copies is one the head or case explains.

    ``08A - 124 - Cold Light`` and ``11A - 126 - [MP3] Cold  Light`` are the same
    record analysed at different times, one of them acquired lossy. A comparison
    against the raw display field would call them different, which is the state
    the source system's set builder shipped in for exactly this reason: a private
    pattern that hardcoded the head shape and had never heard of the marker.
    """
    entries = {entry.track_id: entry for entry in view.entries}
    left = duplicates.recording_of(entries["1"], template=TEMPLATE)
    right = duplicates.recording_of(entries["4"], template=TEMPLATE)
    assert left == right == duplicates.Recording(artist="recondite", title="cold light")


def test_entries_with_nothing_to_compare_are_never_grouped(view):
    """An untagged file has no recording identity, and pretending it does is worse.

    Grouping on two empty fields would collapse every untagged file in a library
    onto one item, and the collapse would look exactly like the audit working,
    which is the failure ``review.item_id_for`` refuses an empty identity over.
    """
    groups = duplicates.audit(view, template=TEMPLATE)
    grouped = {member.track_id for group in groups for member in group.members}
    assert "5" not in grouped


def test_entries_carrying_only_an_artist_are_never_grouped():
    """The half-tagged case, which fails the same way the untagged one does.

    The rule used to be "skip when BOTH halves are empty", so three files with no
    title and the artist ``Recondite`` became one group with three members and
    three options: the collapse the docstring above says would look exactly like
    the audit working, happening. The dangerous direction is the ACCEPTED
    verdict, which names which copy survives and hands the deletion surface a
    licence over three unrelated recordings.
    """
    tracks = [
        (index, "", "Recondite", f"file://localhost/library/{index}.flac")
        for index in (1, 2, 3)
    ]
    view = export.read_export(
        _document(collection=_collection(tracks), root_children=[], root_count=0)
    )
    assert duplicates.audit(view, template=TEMPLATE) == ()


def test_entries_carrying_only_a_title_are_never_grouped():
    """The mirror of the case above, refused by the same rule for the same reason.

    Three files called ``Untitled`` with no artist are three records, and a rule
    that only guarded the artist half would collapse them.
    """
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
    """The NFC split, which the timid normalization is not allowed to be timid about.

    A tagger writing NFC and a filesystem handing back NFD is not an exotic case,
    it is macOS, and ``core.locations`` opens on the incident where treating the
    two as different names deleted 144 still-referenced files. Here the same
    split reports zero duplicate groups where the answer is one.
    """
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
    """The consequence that is worse than the missed duplicate.

    The module docstring promises that renaming, re-importing or moving a copy
    does not orphan the decision. A re-tag that flips the composition form is
    none of those three and used to change the item id anyway, which re-asks a
    settled question and strands the earlier REJECTED verdict in the queue with
    nothing pointing at it.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 1: the audit's output is a review item, never a file
# ═══════════════════════════════════════════════════════════════════════════


def test_the_audit_puts_its_pairs_in_the_review_queue(view, store):
    report = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert len(report.items) == 1
    item = report.items[0]
    assert item.queue == review.Queue.DUPLICATES
    assert item.kind == duplicates.KIND
    assert review.count_unresolved(store, queue=review.Queue.DUPLICATES) == 1
    assert {option.option_id for option in item.options} == {"1", "4"}


def test_every_item_carries_the_handler_key_the_registry_declares(view, store):
    """Addressability, which the default of "" silently opted every item out of.

    ``test_conformance_4`` asserts, once per declared adjudicating verb, that an
    item is findable under that verb's own key. An item produced with an empty
    key satisfies nothing a person can type: asking the queue for
    ``audit.duplicates`` returns nothing, and the only query that finds it is the
    empty string. The registry has declared this key for this verb since U5, so
    the default is read from the one place that already answers the question
    rather than left to whichever caller remembers to pass it.
    """
    report = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert duplicates.HANDLER_KEY == "audit.duplicates"
    assert {item.handler_key for item in report.items} == {duplicates.HANDLER_KEY}
    addressed = review.list_items(store, handler_key=duplicates.HANDLER_KEY).items
    assert [item.item_id for item in addressed] == [report.items[0].item_id]
    assert review.list_items(store, handler_key="").items == ()


def test_the_declared_handler_key_is_the_one_the_registry_carries():
    """Read from the registry rather than restated, so a rename fails here.

    A second spelling of one key is the shape that makes the queue answer an
    empty list to the only query a person has, and nothing else would notice.
    """
    from cratekit.cli import registry

    declared = {
        entry.handler_key
        for entry in registry.entries()
        if entry.name == "audit.duplicates"
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
    """The identity is the RECORDING, so nothing about the file is in it.

    Re-importing a library gives every row a new track id and a rename gives it a
    new location. Either one would orphan a decision keyed on those, and the
    person would be asked the same question again with no way to know they had
    already answered it.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 2: never deletes, and the ignore persists across runs and processes
# ═══════════════════════════════════════════════════════════════════════════


_REJECT_IN_ANOTHER_PROCESS = """
import sys

from cratekit.core import config, review

cfg = config.load()
with review.open_store(cfg) as store:
    review.resolve(store, sys.argv[1], review.Verdict.REJECTED, actor="another-process")
"""


def _in_another_process(script: str, *arguments: str) -> None:
    """Run a short script in a genuinely separate interpreter, and check it.

    A second handle in this interpreter shares its memory and its locks, so it
    can only prove that a value was kept. Only a second process can show what
    reached the disk, which is the whole question a persistent ignore has to
    answer.
    """
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
    """The scenario, end to end, with the verdict recorded by a real process.

    A REJECTED verdict IS the persistent ignore. Nothing beside the report keeps
    a list, which is why the countdown that governs this unit forbids one by
    name: a private ignore file would satisfy the brief's words and re-create the
    defect the queue exists to remove.
    """
    first = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    assert len(first.outstanding) == 1

    _in_another_process(_REJECT_IN_ANOTHER_PROCESS, first.items[0].item_id)

    with review.open_store(cfg) as reopened:
        second = duplicates.audit_and_offer(view, reopened, template=TEMPLATE)
    assert second.groups, "the pair is still a duplicate; it is just no longer a question"
    assert second.outstanding == ()
    assert [item.item_id for item in second.suppressed] == [first.items[0].item_id]


def test_a_revoked_ignore_puts_the_pair_back_in_front_of_a_person(view, store):
    """R12 and R36 both need the door to open both ways.

    An ignore that could only be added is a one-way door, and a person who
    rejected a pair by mistake would have no route back to it at all.
    """
    first = duplicates.audit_and_offer(view, store, template=TEMPLATE)
    review.resolve(
        store, first.items[0].item_id, review.Verdict.REJECTED, actor="me"
    )
    review.clear(store, first.items[0].item_id, actor="me")
    assert len(duplicates.audit_and_offer(view, store, template=TEMPLATE).outstanding) == 1


def test_the_audit_deletes_nothing_from_the_library(cfg, store):
    """The behavioural half of "never deletes", over real files on disk."""
    music = cfg.library.root / "Music"
    for name in ("a.flac", "b.flac", "d.flac", "e.flac"):
        (music / name).write_bytes(b"not really audio, but really bytes")
    exported = music / "collection.xml"
    exported.write_bytes(library_export())

    duplicates.audit_and_offer(
        export.read_export_file(exported), store, template=TEMPLATE
    )

    assert sorted(path.name for path in music.iterdir()) == [
        "a.flac",
        "b.flac",
        "collection.xml",
        "d.flac",
        "e.flac",
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 4: aging thresholds come from config, never from a module constant
# ═══════════════════════════════════════════════════════════════════════════


def test_the_thresholds_have_no_defaults_so_a_hardcoded_policy_cannot_exist():
    """Structural, and it is what makes the scenario true rather than observed.

    ``AgingThresholds`` is not constructible without both numbers, exactly as
    ``naming.NameBudget`` is not. A default here would be a second answer to a
    question the config file already answers, and the second answer is the one
    that ships when somebody forgets to pass the first.
    """
    import dataclasses

    for field in dataclasses.fields(aging.AgingThresholds):
        assert field.default is dataclasses.MISSING, (
            f"{field.name} carries a default, so a caller can build a policy "
            f"without reading configuration"
        )
    with pytest.raises(TypeError):
        aging.AgingThresholds()  # type: ignore[call-arg]


def test_the_thresholds_come_from_the_configured_values(cfg):
    assert aging.thresholds_from(cfg) == aging.AgingThresholds(
        stale_days=30, expired_days=90
    )


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
    """Reported with the key that is wrong, which is what a file needs.

    The value object refuses the same rule, but a stack trace out of a report is
    not a thing anybody can act on. Note the fourth case: leaving one of the two
    out takes its default, so changing only ``intake_stale_days`` is enough to
    invert the pair.
    """
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
    """The message has to name the line the person can go and fix.

    With ``intake_stale_days`` set to text and ``intake_expired_days`` set to 5,
    the pair check substituted the DEFAULT thirty for the field the user did set,
    and reported that 5 is earlier than 30. Thirty appears nowhere in their file,
    so the message sends them to a line that does not exist while the line that
    is actually wrong already had its own message. The pair check is skipped when
    either half was set and rejected, and still runs when a half was simply left
    out, because that is the case that makes changing one of the two able to
    invert the pair.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The aging report itself
# ═══════════════════════════════════════════════════════════════════════════


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
    """Somebody who filed their intake into a folder has organized it, not hidden it.

    The source system aged the top level one way and one hardcoded folder called
    by its display name another way, so any OTHER folder a person made was
    invisible. Here every playlist under the declared intake node is a grouping,
    at any depth, and its path is reported as context.
    """
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
        group.display: group
        for group in aging.intake_groupings(view, intake=INTAKE, today=TODAY)
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
    """Every shape the live library actually uses, plus the ones that must not.

    ``13_45_26`` is not a date and ``2_30_26`` is not a day that exists; both are
    reported as undated rather than coerced into the nearest thing that parses,
    because a name in front of a person is what gets the name fixed.

    A four-digit year outside this century reads as undated, ON BOTH SIDES. Only
    the floor used to be reached: ``_1999`` was here and ``_2500`` was not, so
    the ceiling survived being moved to 9999 with the whole suite green, which
    made it a number nobody was holding. A TWO-digit year always lands inside the
    window, so ``_99`` is 2099 rather than 1999, and a grouping dated in the
    future is simply not stale. Reading it as 1999 instead would report an age of
    nine thousand days and tell somebody to throw the list away.
    """
    assert aging.parse_intake_date(name) == expected


def test_a_name_with_two_dates_is_dated_by_the_first():
    """The intake date is at the front; the second is usually a source list.

    Taking the last would age a grouping from whenever somebody last edited its
    name, which is the opposite of what the report is for.
    """
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
    """The TIE-BREAK, which the fixture above never reached.

    Every grouping there carries a different date, so the secondary key was never
    consulted and dropping it killed no test at all: the guard was held up by its
    own docstring. Two lists dated the same day are ordinary, since a person
    files two intakes in one evening, and they are emitted here in the reverse of
    their path order. Sorting on the age alone is STABLE, so it hands them back
    in walk order, and two runs of a library somebody merely reordered disagree
    about a report that should not have changed.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The verification: both run against a copy and write nothing
# ═══════════════════════════════════════════════════════════════════════════


def _tree_digest(root: Path) -> dict[str, tuple[str, int]]:
    """Every file under ``root``, by relative path, content hash AND modified time.

    Walked rather than enumerated (P3). A test that listed the files it expected
    to be unchanged would be blind to the one a report created, which is the
    interesting case.

    THE MODIFIED TIME IS PART OF THE DIGEST, because a hash alone cannot see a
    rewrite of identical bytes and cannot see a bare ``touch`` at all. Both are
    writes to the library, and the second is the one a sighting ledger would
    reach for: the source system's aging report kept a file recording when it
    first SAW each name, and the cheapest possible version of that is stamping
    the thing it saw. A report that leaves the content alone and moves the clock
    has still written to somebody's library.

    AND IT IS THE ACT THE READ-ONLY PROOF BELOW CANNOT SEE. A ``touch``, an
    ``os.utime`` and a ``chmod`` all succeed through a 0o555 directory holding
    0o444 files, because the process still owns them, which that test now asserts
    rather than assumes. So this is not the weaker of the two halves and the
    property does not supersede the observation: for the one act the source
    system really performed, this is the only half that can see it.
    """
    return {
        str(path.relative_to(root)): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            path.stat().st_mtime_ns,
        )
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_the_digest_sees_a_write_that_changed_no_byte(tmp_path):
    """The INSTRUMENT, checked before anything is concluded from it.

    Two tests below assert that a report changed nothing by comparing this
    digest before and after. What they are really asserting is whatever the
    digest is capable of noticing, and a content hash alone cannot notice a
    rewrite of identical bytes or a bare ``touch``. Both are writes to somebody's
    library, and the second is the shape the source system's aging report
    actually reached for: it kept a file recording when it first SAW each name.

    So the modified time is part of the digest, and this is what makes that fact
    load bearing rather than a comment. Without it this test is the only thing in
    the suite that fails.
    """
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
    """Every row of the synthetic database, so a write to it would be visible.

    Not a rekordbox database and never a copy of one. It stands in for the real
    thing on exactly the property under test: a report must leave the rows it
    finds where they were, and nothing about that question needs a real schema.
    """
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
    """The strongest form of the claim: nothing on disk moves, at all.

    The aging report offers nothing and therefore has no exception to declare.
    Every file under the temporary tree, the library and the installation state
    alike, is hashed before and after.

    The rows are read FIRST and the digest second, so that opening the database
    to read them sits outside the window under test. Otherwise the harness's own
    connection is inside the measurement, and a digest that carries the modified
    time would report the test's own read as the report's write.
    """
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
    """The one write, named, and everything else asserted byte-identical.

    The audit records verdicts, so it is not write-free and claiming otherwise
    would be a lie the tests told for it. What it owes instead is that the review
    queue is the ONLY thing it touches: no audio file, no export, no database
    row, and above all no private ledger of its own.
    """
    rows_before = _database_rows(cfg.library.db_path)
    before = _tree_digest(tmp_path)

    with review.open_store(cfg) as store:
        duplicates.audit_and_offer(
            export.read_export_file(library_on_disk), store, template=TEMPLATE
        )

    after = _tree_digest(tmp_path)
    queue_dir = review.store_dir(cfg).resolve()
    changed = {
        name
        for name in set(before) | set(after)
        if before.get(name) != after.get(name)
    }
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
    """Which of these directories REFUSE a new file, measured rather than assumed.

    Split out of the read-only proof below so the measurement can be driven. The
    proof's first act is to confirm its own lock, and until this existed that
    confirmation was itself unchecked: on a filesystem that ignores the mode, or
    as a user who outranks it, a broken measurement and a working one give the
    same answer everywhere the suite looks.

    A probe that succeeds is removed here rather than by the caller, so the only
    file this can leave behind is one in a directory that was supposed to have
    refused it, which is evidence rather than litter.
    """
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
    """The INSTRUMENT, checked before the read-only proof concludes from it.

    Same shape as ``test_the_duplicate_element_check_sees_a_name_written_twice``
    and for the same reason. The proof below opens by asserting that every locked
    directory refused a write, and that assertion is worth exactly what the
    measurement behind it is worth. Here one directory is locked and one is not,
    so a measurement that always reported refusal and a measurement that always
    reported success are both visible, which they are nowhere else.

    It also confirms the probe cleans up after a directory that ACCEPTED it,
    because the proof below runs inside a real library fixture and a stray file
    there would be read as a report having written one.
    """
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


def test_every_report_runs_with_the_library_directory_read_only(
    cfg, library_on_disk, tmp_path
):
    """READ ONLY, proved by taking the permission away rather than by watching.

    The digests above are an OBSERVATION: they say nothing moved on the paths
    those two calls happened to take. This is a PROPERTY, and it is a narrower
    one than an earlier version of this docstring claimed. With the library root,
    the audio folder, the database folder and every file in them stripped of
    write permission, both reports still produce their answers.

    WHAT THE LOCK PROVES: nothing was CREATED beside the export or at the library
    root, nothing was REWRITTEN, nothing was DELETED. A scratch file, a lock file,
    a private ignore ledger, a rewritten export, all of them fail here whatever
    the digest happened to be looking at.

    WHAT IT DOES NOT PROVE, measured rather than assumed: a bare ``touch``, an
    ``os.utime`` and a ``chmod`` all SUCCEED through this lock, because the
    process still owns the files and none of those three needs the write bit.
    That is asserted inside the window below rather than described, since a
    docstring naming a limit nothing checks is how this proof came to claim a
    ``chmod`` fails here when it does not.

    So the two halves are not ranked, they are complementary, and the ordering
    matters most for the one act that matters most. A sighting ledger is what the
    source system's aging report actually kept, the cheapest version of one is a
    stamp on the file it saw, and the stamp is exactly what this cannot see. The
    DIGEST is what covers it: ``_tree_digest`` carries each file's modified time
    for that reason, and ``test_the_digest_sees_a_write_that_changed_no_byte``
    is what keeps that fact load bearing.

    THE LOCK IS PROVED BEFORE IT IS TRUSTED. A test that only asserts success
    under a permission change it never confirmed is the absence-read-as-absence
    shape aimed at itself: on a filesystem that ignores the mode, or as a user
    who outranks it, it would pass while proving nothing. So the first thing
    inside the window is a write that MUST fail, at every directory locked. The
    measurement behind that is ``_directories_refusing_a_write`` and it is driven
    against an unlocked directory in its own test, because a proof that opens by
    checking itself still needs the check to be worth something.

    AND IT FAILS RATHER THAN SKIPS when the lock does not hold, which is
    deliberate and is the repository's own rule rather than a preference:
    ``tests/test_pending_units.py`` allows no skip constructed outside the
    pending register, because a skip is a guard switched off with nothing
    counting down to its return. A run that cannot express this property has not
    checked the unit's central claim, and saying so out loud is the only honest
    report of that.

    THE REVIEW QUEUE IS INSIDE THE LIBRARY ROOT, which an earlier version of this
    docstring denied. ``config.state_path`` declares it library scoped, so it
    resolves under ``library_state_dir``, a dot directory beside the audio. What
    is true is the narrower thing: the queue is the one directory this package
    writes into, it is not the collection, and locking the root does not protect
    it. The directory is opened once before the lock for that reason, which is
    also its real lifecycle: on any library that has ever been offered anything,
    it already exists.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The structural half: the package cannot write, whatever a test drives
# ═══════════════════════════════════════════════════════════════════════════

#: Every top-level module the reports package may import, and every dotted target
#: inside this one. DERIVED FROM WHAT READING NEEDS.
#:
#: THE LIST IS NOT THE WHOLE ARGUMENT, and an earlier version of this comment
#: said it was: nothing admitted here can open a database, spawn a process, or
#: touch a file except through ``pathlib``. That is not true and was never
#: checked. ``cratekit.core.config`` writes the configuration file from two
#: public functions, one of them called ``load_from_path``, and
#: ``cratekit.core.naming`` opens a file in ``claim_target``. What makes the list
#: safe is the list PLUS ``FILESYSTEM_MUTATIONS`` naming every writer the
#: admitted modules expose, and
#: ``test_the_allowlist_admits_no_writer_this_guard_cannot_name`` is what keeps
#: those two in step as those modules change.
#:
#: WHAT THE LIST ADMITS IS NOT WHAT IT REACHES, and the audit read only the first
#: until the residual "The reports allowlist audit is one hop deep" was closed.
#: An admitted module's own imports are attributes of it, so
#: ``rbxml.tree_registry`` is reachable from here without ``tree_registry`` being
#: listed, and the walk out of ``rbxml`` through ``tree_registry`` and ``session``
#: arrives at ``cratekit.core.rb_writer``, which opens the rekordbox database. The
#: audit now follows every first party import to its closure, and forty nine
#: writers it had never read are named below as a result.
#:
#: ``cratekit.core.review`` is the single deliberate exception and is the reason
#: this is an allowlist rather than a blocklist. The package IS allowed to
#: persist, through exactly one surface, which is the whole of R12. Anything else
#: that can reach a disk has to be added here by name, in a diff.
#:
#: ``cratekit.core.exit_codes`` is listed while nothing here imports it yet, on
#: purpose. It is where a remediation TOKEN comes from, every refusal in this
#: package will eventually want one, and a guard that fires the first time
#: somebody writes correct code is a guard that gets deleted rather than obeyed
#: (P7). It carries no capability of its own: it is an enumeration.
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
#:
#: ``replace`` is NOT here, and it is not absent either: it is handled separately
#: below on its arity, because it is ``str.replace`` far more often than it is
#: ``Path.replace`` and a guard that fires on correct code is a guard somebody
#: routes around (P7). Leaving it out entirely was the other error, since
#: ``Path(a).replace(b)`` silently overwrites its destination while its sibling
#: ``rename`` is in this set, so the one of the pair that destroys more was the
#: one that was allowed.
FILESYSTEM_MUTATIONS = frozenset(
    {
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
#:
#: APPENDED as a second set rather than into the one above, for the reason the
#: verb registry, the pending register and the cause mapping all give: two units
#: inserting into the middle of one literal auto-merge, and an append conflicts
#: textually, which is a conflict somebody reads.
#:
#: The names above are pathlib and shutil. These are this repository's own, and
#: they are here because the allowlist's argument was WRONG. That comment said
#: nothing admitted here can touch a file except through pathlib, and
#: ``test_the_allowlist_admits_no_writer_this_guard_cannot_name`` walks the
#: admitted modules and shows otherwise: ``cratekit.core.config`` exposes three
#: writers and a locking context manager, and ``cratekit.core.naming``, which
#: ``duplicates`` already imports, exposes one. ``load`` and ``load_from_path``
#: are the dangerous pair, because their names read as pure loads and they write
#: the file back.
#:
#: THE RECEIVER IS PART OF THE NAME, and leaving it off was an over-restriction
#: this guard shipped with. ``load`` and ``save`` are ordinary method names on
#: anything at all, and the check reads the attribute wherever it appears, so a
#: report reading ``view.save`` or ``taxonomy.default_taxonomy().load`` was
#: reported as a writer and an admitted module exposing ``return spec.load``
#: failed the audit. ``replace`` was deliberately kept out of the set above for
#: exactly that reason, and then two more generic names went in flat. Nothing in
#: the tree trips it today, which is the only reason the suite was green.
#:
#: A bare name is still qualified INSIDE the module that defines it, which is
#: what ``_writer_names_of`` carries into the audit: a call to ``_mkdir_private``
#: with no receiver, in ``config.py``, is ``config._mkdir_private``.
#:
#: None of these is reachable from correct code in this package: a report is
#: HANDED a ``Config`` by its caller and neither loads nor saves one, and
#: claiming a target filename is what a WRITER does with a name this package only
#: ever parses. The walking audit is what keeps this list true as those modules
#: change, rather than a reviewer's snapshot of them.
#:
#: THE SECOND BLOCK IS THE CLOSURE'S, and it is long because the closure reaches
#: the write path itself. The audit was found one hop deep: it read the admitted
#: modules and nothing they import. Following the imports out of ``rbxml``,
#: ``review`` and ``taxonomy`` reaches ``tree_registry``, ``session``,
#: ``snapshot``, ``reconcile``, ``backup_facts`` and ``rb_writer``, and every name
#: below is one the audit found there, measured to a fixed point in five rounds.
#: Most of ``rb_writer``'s are writers only because they call ``config.load``,
#: which writes the file back. That is the audit being consistent rather than
#: generous: a report calling any of them changes a file.
QUALIFIED_MUTATIONS = frozenset(
    {
        "config._back_up_version",
        "config._exclusive_lock",
        "config._mkdir_private",
        "config._write_lock",
        "config.load",
        "config.load_from_path",
        "config.save",
        "config.update",
        "naming.claim_target",
        "backup_facts.record",
        "backup_facts.write_outcome",
        "rb_writer._candidate_app_paths",
        "rb_writer._loaded_config",
        "rb_writer._pins",
        "rb_writer.assert_app_version",
        "rb_writer.assert_binding_version",
        "rb_writer.assert_schema_version",
        "rb_writer.default_protected_snapshot_paths",
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
        "reconcile._write",
        "reconcile.close_marker",
        "reconcile.record_markers",
        "reconcile.retract_in_flight",
        "session._open_lock_file",
        "session._recorded",
        "session._write_holder",
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
        "snapshot._verify",
        "snapshot.capture",
        "tree_registry.flip",
        "tree_registry.record_cutover",
        "tree_registry.revert_cutover",
        "tree_registry.write",
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
    """Whether a dotted path names a DIRECTORY in this repository's source tree.

    The depth rule below covers ``cratekit``, ``cratekit.<subpackage>`` and the
    standard library's shallow packages, and it stops there because a symbol
    treated as a module makes a checker report imports that do not exist. It does
    not cover a three level package, and this repository now has one, so
    ``from cratekit.modules.reports import aging`` would read as a dependency on
    the package with ``aging`` mistaken for a symbol. Asking the filesystem is
    the answer that cannot drift, and it answers False for everything outside the
    tree, which is where guessing would be dangerous.
    """
    return root.joinpath(*dotted.split(".")).is_dir()


def _package_of(module: str, root: Path = SRC_ROOT) -> str:
    """The package a module's relative imports resolve against.

    A PACKAGE's own ``__init__`` resolves ``from . import aging`` against itself;
    a module inside it resolves against its parent. Read off the filesystem
    rather than off the dotted name, because the two coincide here: taking the
    parent unconditionally made ``cratekit.modules.reports``'s own initializer
    resolve ``from . import aging`` to ``cratekit.modules.aging``, a module that
    does not exist and that this guard would then report as forbidden. A false
    positive, which is the failure that gets a guard switched off, and it would
    have fired on the first correct relative import anybody wrote there.
    """
    if root.joinpath(*module.split(".")).is_dir():
        return module
    return module.rsplit(".", 1)[0]


def _resolved_imports(source: str, module: str, root: Path = SRC_ROOT) -> list[str]:
    """Every module ``source`` depends on, as absolute dotted paths.

    Resolved through the import GRAPH rather than matched by name, in all four
    shapes the repository allows, because a guard that matches a bare name is
    satisfied by anything spelled that way and defeated by one alias. U11's
    countdowns were defeated by ``import csv as spreadsheet`` for exactly this
    reason, and the alias is read here from ``alias.name``, which is the module
    that is actually loaded, never from the local name it is bound to.

    Relative imports are resolved against the importing module's own package, so
    a future ``from . import export`` is recognized as the package it names
    rather than waved through as unrecognizable.

    A ``from X import y`` where X is a PACKAGE resolves to ``X.y``, and where X
    is a module resolves to X with ``y`` left alone as a symbol. Getting that
    backwards is what makes a checker report imports that do not exist, which is
    the same distinction ``tests/test_layering.py`` draws for the same reason.

    THE STATEMENT IS NOT THE ONLY IMPORT. ``__import__("os").truncate(path, 0)``
    loads a module with no import statement anywhere in the file, and a walk over
    ``ast.Import`` and ``ast.ImportFrom`` alone reports it clean, which put
    ``os``, ``subprocess`` and ``sqlite3`` one builtin call away from this
    package. The builtin is read here too, and an argument this cannot read is
    reported as an import of something unnameable rather than ignored.

    ``root`` is the tree the package and relative import questions are asked of.
    It defaults to this repository, and the import closure passes a planted one,
    since a planted three level package asked about here would otherwise be read
    against the real tree and resolve to the wrong module.
    """
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
    """Whether one resolved import is inside the allowlist or inside this package.

    A prefix match against an allowlisted entry is accepted, so
    ``from cratekit.core.review import Option`` resolves through
    ``cratekit.core.review`` rather than being read as a module of its own.

    EVERY MATCH TAKES A DOT BOUNDARY, including the one for this package's own
    name. Without it, ``cratekit.modules.reports_ledger`` is a sibling of the
    package that reads as part of it, and a sibling is not walked by
    ``_report_modules`` either, so a file with that name could hold the private
    ignore ledger this unit's countdown forbids and pass both guards at once.
    """
    if target == REPORTS_PACKAGE or target.startswith(f"{REPORTS_PACKAGE}."):
        return True
    return any(target == allowed or target.startswith(f"{allowed}.") for allowed in ALLOWED_IMPORTS)


def forbidden_imports(source: str, module: str) -> list[str]:
    """Every dependency the reports package is not allowed to have."""
    return [target for target in _resolved_imports(source, module) if not _permitted(target)]


def filesystem_mutations(source: str) -> list[str]:
    """Every call in ``source`` that could change a file, with its line.

    WHAT THIS IS FOR, said once and plainly, because every round has been
    tempted to claim more. It is aimed at an ORDINARY AUTHOR writing ordinary
    code that happens to write: an alias, a container, a default argument, a
    bound method, a helper reached through a module the allowlist admits. It is
    NOT a defence against an author who has read this function and means to get
    past it. A checker reading names cannot win that, and the four dunder and
    subscript spellings below are named rather than left silent so that nobody
    later reads silence as coverage.

    THAT SENTENCE WAS AN AIM WRITTEN AS AN ACHIEVEMENT, and the round it was
    written in falsified it in both directions at once. Ten shapes an ordinary
    author writes were reported as writes to the library, including ``for config
    in rows``, ``config = dict(raw)``, ``counts["rename"] + counts["unlink"]``
    and a constructor taking a parameter called ``config``; three real writes
    through a tuple, a conditional and a nested list were missed. The tree was
    green throughout, because no governed module had yet been written in any of
    the ten. Every one of them is now a fixture, and the ten quiet ones are
    driven from the REAL ``aging`` rather than from a fixture of their own, since
    that is where they were found.

    Five rules, and each of the last four is narrowed so it cannot fire on
    correct code, because a guard that does is a guard somebody routes around
    (P7).

    1. One of the named mutating methods, spelled as an ATTRIBUTE, reached
       rather than merely called.
       An attribute access spelling one of those names is reported wherever it
       appears, because ``keep = Path(p).write_text`` followed by ``keep(x)``
       writes a file with no mutating name in any call position at all: the
       outer call's ``func`` is a plain local. That is round one's bound-``open``
       hole one step further out, and the same answer closes it. A bare name
       call is still checked separately, since ``rmtree(a)`` after a ``from
       shutil import rmtree`` has no attribute to read (the import guard is what
       catches that one first).

       The names in ``QUALIFIED_MUTATIONS`` take the same rule with the RECEIVER
       read as well, because ``load`` and ``save`` are ordinary method names and
       a check that fires on ``view.save`` is a check somebody routes around
       (P7). The receiver is resolved through the file's BINDINGS, not through
       its imports alone, so an alias, a container element, a returned module, a
       loop variable, a default argument and an attribute store are each
       followed; and a receiver with no binding is UNRESOLVED rather than a
       module named after the variable. A name imported straight off an admitted
       module is matched bare because that is what it then is.

       AN OBJECT KEY CARRIES ITS OWNER, because it is the one half of the table
       that is not lexical. Keyed on the bare spelling, ``self.config`` was one
       binding for the whole file, so one class storing the module there made
       every other class's ``self.config.load`` a write to the library.
    2. A call to ``open`` whose mode is anything other than a literal read mode.
       Narrowed rather than banned outright because ``open(path, "rb")`` is a
       perfectly correct read. A mode this cannot READ is a violation, since a
       computed mode is exactly how the check would be walked past.

       WHICH ARGUMENT IS THE MODE depends on whether the receiver is the file.
       ``Path(p).open("w")`` puts it first; the builtin and every module level
       ``open`` put the file first and the mode second. Deciding that on "is
       there an attribute" made ``io.open``, ``gzip.open``, ``codecs.open`` and
       ``tarfile.open`` report their FILE as an unreadable mode, and
       ``os.open(str(path), os.O_RDONLY)`` in ``cratekit/core/jobs.py``, a
       directory opened read only for an fsync, was a live example in the tree.
       ``os.open`` is read through its FLAGS, which is the one module level open
       that takes no mode string at all.
    3. A ``replace`` call with exactly one positional argument and no keywords,
       which is ``Path.replace`` and ``os.replace`` and is never ``str.replace``.
       The arity is what separates them: the string method needs the old text and
       the new, so it always carries at least two, and ``date.replace(year=...)``
       carries none positionally. That is why ``replace`` is not simply a member
       of the set above, which would fire on the ``str.replace`` in
       ``CORRECT_MODULE`` and be the P7 failure this whole guard is written
       around.
    4. A reflective read naming one of the mutating methods, or naming an
       attribute this cannot read. ``getattr(Path(p), "write_" + "text")(decided)``
       writes a file while the outer call's ``func`` is itself a Call and its
       ``attr`` never appears anywhere, which is the same walk-past as the
       computed mode and gets the same answer. ``__getattribute__`` is what
       ``getattr`` calls and is reachable both bound and unbound, so it is read
       on the same terms for a LITERAL name; for a computed one it is read on
       whether its result is called, because ``return super().__getattribute__(
       name)`` is the ordinary spelling of the dunder and reporting it was
       collateral this rule claimed not to have.
    5. A LOOKUP INTO A TYPE'S ATTRIBUTE MAPPING whose constant key names a
       mutating method. ``Path.__dict__["write_text"](p, d)``,
       ``vars(Path)["write_text"](p, d)`` and ``Path.__dict__.get("write_text")(
       p, d)`` reach the function object without an attribute access and without
       a callee this can name.

       THE RECEIVER IS PART OF THIS RULE and leaving it out is what the old
       comment here got wrong. It claimed an ordinary dispatch table keyed on
       anything else never sees the rule, while comparing the key against
       ``FILESYSTEM_MUTATIONS`` with no receiver read at all. ``touch``,
       ``rename``, ``truncate``, ``mkdir`` and ``chmod`` are all plausible
       mapping keys, and ``counts["rename"] + counts["unlink"]`` was two
       findings. A ``__dict__`` and a ``vars`` are the only two spellings that
       hand back the function object; a mapping is a mapping.

       THE RECEIVER IS RESOLVED THROUGH THE BINDING TABLE, which rule 1's already
       was and this one was not. Read off the lookup's own expression, ``table =
       vars(Path)`` followed by ``table["write_text"](path, data)`` was two
       ordinary lines that wrote a file, and so were the ``dict()``, spread,
       returned, stored and default-argument spellings of the same binding. The
       round before had built a table that follows ``alias = config`` and then
       did not ask it about ``table = vars(Path)``. There is ONE place a receiver
       resolves now, ``_bound_value``, and every rule asks it.
    """
    tree = ast.parse(source)
    modules, direct = _writer_bindings(tree)
    return mutations_in(tree, modules=modules, direct=direct)


class _Instance(NamedTuple):
    """Which local name, in one scope, is an instance of which class.

    ``self`` is a PARAMETER, so it means a different object in every method of
    every class, and an object key rooted at it is carried file-wide. Without
    this pair the table keyed ``self.config`` once for the whole file, so one
    class binding ``self.config`` to an admitted module made every other class's
    ``self.config`` a finding: ``def go(self): return self.config.load`` in a
    class whose constructor takes ``config`` as an argument was reported as a
    write to the library. That is this repository's second recurring defect,
    identity that is not unique, aimed at the round's own table.

    ``root`` is the canonical spelling the name renders as, which is why it is
    stored rather than derived. A class that spells the instance ``self`` in one
    method and ``this`` in another has ONE object, and both render
    ``Keeper::self``; a ``classmethod``'s first parameter is the CLASS, so it
    renders as the class path itself and ``cls.mod`` resolves where
    ``Keeper.mod`` does.
    """

    name: str = ""
    root: str = ""


#: What an instance of a class renders as inside the binding table. Written as a
#: suffix on the class path rather than as the parameter's own spelling, because
#: the parameter's spelling is the thing that is not stable.
#:
#: It is off the alphabet an identifier chain can produce, which is the point:
#: ``Keeper.mod`` is how the class attribute is spelled from outside and
#: ``Keeper::self.mod`` is how the same attribute is reached from inside, and no
#: chain of names, dots and calls renders the second.
#:
#: THE ONE WAY TO SPELL IT ANYWAY is a subscript whose constant key is that text,
#: ``MODS["Keeper::self"]``, because a subscript key is rendered with ``repr``.
#: That is stated rather than hidden, and it is the same shape the whole table
#: has: a key is a rendering, and a rendering can in principle be forged by
#: somebody who has read this file. It is not a shape an ordinary refactor
#: produces, which is what this guard is aimed at.
_INSTANCE = "::self"


def _receiver_key(node: ast.AST | None, instance: _Instance = _Instance()) -> str:
    """A canonical spelling of one receiver EXPRESSION, or "" when it has none.

    The binding table below is keyed on this rather than on a bare name, because
    the shapes an ordinary refactor produces are not all bare names. ``self.mod``,
    ``MODS[0]``, ``MODS["c"]`` and ``_mod()`` are each a receiver somebody writes
    without thinking about a guard at all, and each of them reaches an admitted
    module's writer with the module's own name nowhere beside the call.

    A key is rendered only for a spelling that can be resolved back to ONE
    binding. ``Path(p)`` carries arguments, so it renders nothing: what it
    returns depends on what it was handed. KEYWORD arguments are arguments, so
    ``_mod(fallback=cfg)`` renders nothing either, and both halves of that
    condition are driven by
    ``test_a_receiver_key_is_only_rendered_for_a_call_that_takes_nothing``.
    A receiver this cannot read is UNRESOLVED, and an earlier version answered
    unresolved with the variable's own name, which reported
    ``def f(config): return config.load`` as a write to the library.

    THE OWNING CLASS IS PART OF THE KEY, through ``instance``, and leaving it out
    was the same defect one level in. ``self`` is a parameter and the key rooted
    at it is carried file-wide, so two classes that both spell ``self.config``
    shared one binding and the one that resolved decided for both.

    ``None`` is what an ``x: int`` annotation has in place of a value, and it
    falls through to the same "" every other unreadable expression gets. That is
    why there is no separate guard for it: a guard that only restates the default
    answer is a line no mutation can kill.
    """
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
#:
#: A comprehension is one of them, and leaving it out was not a simplification.
#: ``[config.load for config in rows]`` binds ``config`` for the comprehension
#: and for nothing else, so reading it as part of the enclosing function would
#: either report that ordinary line as a write to the library or, once the target
#: shadowed the whole function, lose a real ``config.save`` written after it.
#:
#: A CLASS BODY is one of them, and an earlier version said it deliberately was
#: not. The stated cost of leaving it out was that a class attribute colliding
#: with an imported module took the name back for the ENCLOSING scope, which is
#: the quiet direction; the unstated one was louder. ``class Keeper: mod =
#: config`` bound the bare name ``mod`` at module level and created no object key
#: at all, so ``self.mod.save(cfg)`` in a method of that class wrote the
#: configuration file with both structural guards and the audit green, while the
#: identical assignment written ``self.mod = config`` in a constructor fired.
#:
#: A class body is a scope with one rule of its own: its names are NOT visible to
#: its methods, which is why ``_walk_bindings`` hands a method the table its class
#: inherited rather than the table its class built. What the body binds becomes an
#: OBJECT key instead, under both spellings the attribute has.
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


def _scope_nodes(node: ast.AST):
    """Every node inside one scope, stopping where a nested scope begins."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPES):
            continue
        yield child
        yield from _scope_nodes(child)


def _nested_scopes(node: ast.AST):
    """Every function, lambda and comprehension directly inside one scope."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPES):
            yield child
        else:
            yield from _nested_scopes(child)


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
    """Every statement in one scope a single run can skip, by node identity.

    A FAILED ATTEMPT VETOES A BINDING, which is the rule that keeps ``config =
    dict(raw)`` from leaving an import's answer live underneath it, and a veto
    written inside a branch is a veto that may never happen. ``class Keeper`` at
    module level followed by ``if True: Keeper = dataclass(Keeper)`` has a path on
    which the name is still the class, so ``Keeper.mod.save(cfg)`` writes the
    configuration file on that path and the veto is not the whole story.

    This changes only the VETO. A conditional statement that resolves still binds
    what it resolved to, and a name that NOTHING unconditional binds is still
    taken by ``_names_taken`` and still comes back unresolved, so the ten ordinary
    shadow shapes are untouched: their names are taken by a loop target, a ``with``
    target or an ``except`` target and nothing puts them back.

    THE SET IS NOT THE RULE. This says which statements a run can skip, and it is
    the same fact for a name and for an attribute. Whether skipping one MATTERS is
    a different question with a different answer for each, and ``_chains_to_base``
    is where the attribute half is decided. A docstring here that stated the rule
    over the whole table while only the name half had been driven is what let six
    ordinary branch spellings fire on the object half.

    Read as node identity rather than as a line range because ``_scope_nodes``
    hands out nodes, and comparing what two functions each computed off the same
    nodes is what stops them drifting.
    """
    found: set[int] = set()
    for holder in _scope_nodes(scope):
        if not isinstance(holder, _BRANCHING):
            continue
        for field in _BRANCHED_FIELDS:
            for one in getattr(holder, field, None) or []:
                found.update(id(inner) for inner in ast.walk(one))
    return frozenset(found)


def _chains_to_base(scope: ast.AST) -> bool:
    """Whether one scope UNCONDITIONALLY runs a base class's initializer.

    THE OTHER HALF OF THE BRANCH RULE, and the half that reads an OBJECT key. A
    veto cast inside a block a run can skip is not a veto that run cast, which is
    true of a NAME whatever else the scope does: the ``class`` statement that
    bound it ran on every path, so the name is still the class on the path that
    skipped the rebinding, and that direction is driven clean across every branch
    shape there is.

    AN ATTRIBUTE IS NOT LIKE THAT, and the rule was stated in prose over the whole
    table while it had only ever been measured on the name half. ``self.mod`` is
    not bound by ``class Base`` at all: it is bound by the statement inside
    ``Base.__init__`` that assigns it. So a subclass whose own ``__init__``
    overrides that attribute inside an ``if`` and never calls the base's
    ``__init__`` has NO path on which the base's binding is reachable. On the arm
    that ran, the attribute is the override; on the arm that did not, the
    attribute was never created and the read is an ``AttributeError``. Six
    ordinary branch spellings were reported as writes to the configuration file on
    the other reading, every one of them a subclass overriding an attribute one
    indent in, which is the most ordinary thing inheritance does.

    What makes the base's binding reachable again is a scope that CHAINS: an
    unconditional ``super().__init__()`` or ``Base.__init__(self)`` runs the
    statement that binds the attribute, so the arm that skips the override really
    does leave the module in place and really does write.

    UNCONDITIONALLY, because a chaining call written inside a branch is skippable
    on the same rule that made the override skippable, and a run that skips both
    reaches neither. The cost is stated rather than hidden: a base initializer
    called from the OTHER arm of the same conditional is a reachable binding this
    reads as unreachable. That is a miss rather than a false positive, which is
    the direction this guard takes when it has to take one.
    """
    skippable = _branched(scope)
    for child in _scope_nodes(scope):
        if id(child) in skippable or not isinstance(child, ast.Call):
            continue
        if isinstance(child.func, ast.Attribute) and child.func.attr == "__init__":
            return True
    return False


def _alternatives(node: ast.AST | None):
    """The values ONE expression can evaluate to, when it is a choice between some.

    ``config or fallback`` and ``config if flag else fallback`` are the two
    spellings, and ``_bound_value`` already reads both through on the stated rule
    that a receiver which is the module on ONE path can write on that path. This
    is the other half of the same rule, read from the target's side: an assignment
    whose right hand side can evaluate to the SPELLING OF ITS OWN TARGET is an
    assignment the target survives on one path, so ``Keeper = Keeper or None``
    leaves ``Keeper`` the class exactly as ``Keeper = Keeper`` does, and a class
    object is always truthy so there is nothing undecidable in it.

    Everything else yields ITSELF, so the ordinary case is one element and
    unchanged. A call is not read through, because what a callee hands back is the
    question the residual titled "A class rebound after its own definition is no
    longer reachable by name" declines to answer.
    """
    if isinstance(node, ast.BoolOp):
        for one in node.values:
            yield from _alternatives(one)
    elif isinstance(node, ast.IfExp):
        yield from _alternatives(node.body)
        yield from _alternatives(node.orelse)
    elif node is not None:
        yield node


def _restored_attributes(scope: ast.AST, instance: _Instance) -> dict[str, str]:
    """Each instance attribute one scope DELETES, with the class spelling under it.

    ``del self.mod`` removes the INSTANCE attribute and leaves the class one, so a
    class that binds the module in its body and rebinds it in ``__init__`` is
    writing the configuration file again from the ``del`` onwards. Measured rather
    than reasoned about: the shape returns the module's own result and the call
    really runs.

    Both halves are computed HERE rather than one here and one at the call site,
    because the pair is one fact: which key comes back, and what it comes back to.
    Split across two places they can disagree about which spelling is which, and a
    fix landing on the wrong one of two spellings is this repository's third
    recurring defect.

    Only an INSTANCE spelling is restored. A bare ``del name`` is a name and is
    already taken by ``_bound_here``; ``del Keeper.mod`` deletes the class
    attribute rather than uncovering it, so there is nothing under it to come
    back to.
    """
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
    """The bare names ONE statement or expression binds in the scope it sits in.

    Every spelling Python has for taking a name back is listed, because the
    previous version listed exactly one of them. Only a PARAMETER could shadow, so
    a loop target, a ``with`` target, an ``except`` target, a walrus, a
    comprehension target, an unpacking target, an augmented assignment and a
    plain assignment each left the file's import binding live underneath a name
    that no longer meant it. Ten ordinary shapes were reported as writes to the
    library on that reading, and the list below is the answer to all ten at once.
    """
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
    """The names nested DEFINITIONS bind in the scope that holds them.

    Named once because two callers need the same fact and they must not disagree:
    the scope that shadows on it and the scope that records it as a binding it
    cannot resolve. ``_scope_nodes`` deliberately stops where a nested scope
    begins, so a ``def`` inside a function is invisible from that side and has to
    be read from this one.

    A CLASS is one of them, and it used to be read by ``_bound_here`` instead.
    Once a class body became a scope, ``_scope_nodes`` stopped yielding the
    ``ClassDef`` at all, so that branch was dead and the name it bound was no
    longer taken: ``class config: pass`` beside ``from cratekit.core import
    config`` left the import's answer live for the whole module. One fact, one
    place, and the place is the side that can still see it.
    """
    return frozenset(
        nested.name
        for nested in _nested_scopes(node)
        if isinstance(nested, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )


def _rebound_to_itself(node: ast.AST, instance: _Instance = _Instance()) -> frozenset[str]:
    """The receiver keys one assignment binds to the value they already hold.

    ``Keeper = Keeper`` is the whole of it, and it is not a curiosity: it is what
    a re-export, a ``global`` handoff and a conditional wrapper collapse to once
    the wrapper is edited out. Read as an ordinary assignment it is a name bound
    TWICE, once by the ``class`` statement and once here, and the second binding
    resolves to nothing on the first pass because the name is not in the table
    yet. A name is kept only when every binding of it agrees, so the class was
    thrown away and ``Keeper.mod.save(cfg)`` wrote the configuration file quietly.

    Nothing is undecidable about this one. A statement whose right hand side is
    the SPELLING of its own target cannot change what that target is bound to,
    whatever the target was bound to and whether or not this guard can read it.
    That is what separates it from ``Keeper = dataclass(Keeper)``, where the
    answer depends on what the callee hands back, which is what the residual
    "A class rebound after its own definition is no longer reachable by name"
    files as undecidable.

    Recorded as a set of KEYS rather than of names so ``self.mod = self.mod`` is
    the same fact under the same rule, and so the two callers, the scope table and
    the shadow, cannot disagree about which statements are idle.

    IDLE IS NOT SILENT. The caller records what the key ALREADY HELD, which is the
    only reading that gets both directions: it is why ``class Keeper: config =
    config`` still binds the module as a class attribute, the ordinary way a module
    is pinned for injection, and why it does so without needing to know what the
    right hand side would have resolved to. When the held value cannot be read the
    statement contributes nothing at all rather than a failed attempt, because a
    statement that provably changed nothing cannot be evidence that something
    changed.

    A CHOICE BETWEEN VALUES IS READ THROUGH, so the right hand side is a SET of
    spellings rather than one. ``Keeper = Keeper or None`` and ``Keeper = Keeper
    if True else None`` were both quiet while the plain spelling fired, and a
    residual that said the remaining silence was "for the three wrapper spellings
    only" was describing a shape nobody had measured. Neither of these is
    undecidable: ``_bound_value`` already reads ``or`` and a conditional
    expression through, on the rule that a value reachable on one path is
    reachable, and a class object is always truthy besides. A CALL is still not
    read through, which is what keeps ``Keeper = dataclass(Keeper)`` on the other
    side of the line.
    """
    if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
        return frozenset()
    sources = {
        key
        for key in (_receiver_key(one, instance) for one in _alternatives(node.value))
        if key
    }
    if not sources:
        return frozenset()
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return frozenset(
        key for key in (_receiver_key(one, instance) for one in targets) if key in sources
    )


def _names_taken(node: ast.AST) -> frozenset[str]:
    """Every bare name one scope binds to something of its OWN.

    A NESTED DEFINITION is one of them. ``def config(): ...`` inside a function
    that also imports a module of that name binds the name for the whole
    function, and ``_scope_nodes`` deliberately stops at a nested scope, so the
    name has to be picked up from the other side.

    A ``global`` declaration is NOT subtracted, and an earlier version of this
    subtracted it. The stated reason was that such a name is about the enclosing
    scope, which is true and is not the question: ``global config`` followed by
    ``config = dict(raw)`` really does take the name back, in this scope and in
    the module, so treating it as taken is the correct read for the scope doing
    it. What is not modelled is the write BACK, so a later scope still sees what
    the import said. That is a stated limit rather than a claim.
    """
    taken = set(_defined_here(node))
    for child in _scope_nodes(node):
        taken |= _bound_here(child) - _rebound_to_itself(child)
    return frozenset(taken)


class _Namespace(NamedTuple):
    """A TYPE'S ATTRIBUTE MAPPING, as a thing a name can be BOUND to.

    Rule 5 exists for ``Path.__dict__["write_text"]`` and
    ``vars(Path)["write_text"]``, which reach a writing function through a
    subscript that no attribute rule and no call rule can read. It read that
    receiver INLINE, off the subscript's own ``value`` and nowhere else, so one
    binding was enough to walk past it:

        table = vars(Path)
        table["write_text"](path, data)

    Both lines are ordinary Python and the pair writes a file. That is the same
    two-line refactor ``alias = config`` already goes through the binding table
    for, and the answer is to put the namespace IN the table rather than to add a
    second place where a receiver is resolved. One resolution path, asked by every
    rule, is the whole of this round's fix.

    ``owner`` is the receiver key of the type the mapping belongs to, so
    ``QUALIFIED_MUTATIONS`` can still be checked against an admitted module, and
    it is "" when the owner is an expression this cannot name. A mapping whose
    owner is unreadable is still a mapping, so the empty string is a value here
    rather than an absence.

    WHAT A RECEIVER KEY CAN BE BOUND TO is now two things: an admitted module by
    its short name, or one of these. Two meanings in one table is the defect this
    file keeps producing, so the second one is a TYPE rather than a marked string,
    and every reader asks ``isinstance`` for the kind it can use.
    """

    owner: str = ""


class _Class(NamedTuple):
    """ONE CLASS DEFINITION, as a thing a name can be BOUND to.

    A class was a SPELLING before this, ``Keeper`` or ``Outer.Keeper``, computed
    from the lexical path and used as the root of every attribute key the class
    owns. A spelling is not an identity, and two of the three shapes this file
    keeps failing on came straight out of that: two classes called ``Keeper`` in
    two different factory functions shared one root, so one factory's class body
    decided for the other's; and a parameter called ``Keeper`` could not take the
    name back, because a name is only shadowed while it IS a name and an object
    key spelled with a dot never was one.

    So a class NAME is an ordinary lexical binding now, exactly like ``alias =
    config``, and what it is bound to is this. The identity underneath is the
    DEFINITION SITE, which is unique by construction and which two different
    ``class Keeper`` statements cannot share.

    ``bases`` is the identity of each class this one inherits, resolved through
    the same table, and it is what makes ``class Row(Base)`` see what ``Base``
    bound. A key landed on the class that DECLARED an attribute and never on the
    class that REACHES it, so a base class, a mixin and an inherited class body
    attribute were each two ordinary lines that wrote a file.

    WHAT A RECEIVER KEY CAN BE BOUND TO is three things now: an admitted module
    by its short name, an attribute mapping, or one of these. Two meanings in one
    table is the defect this file keeps producing, so each of the two that are
    not a module is a TYPE rather than a marked string, and every reader asks
    ``isinstance`` for the kind it can use.
    """

    key: str = ""
    bases: tuple[str, ...] = ()


#: What any receiver key in the binding table can be bound to.
_Bound = str | _Namespace | _Class


#: What separates a class's NAME from its definition site in a class key.
#:
#: It is off the alphabet an identifier chain can produce, for the same reason
#: ``_INSTANCE`` is: ``Keeper#412.mod`` is how one particular class's attribute is
#: keyed, and no chain of names, dots and calls renders it. A subscript with that
#: exact constant key can forge it, which is the same admitted shape ``_INSTANCE``
#: has and is not a shape an ordinary refactor produces.
_DEFINED = "#"


def _class_key(node: ast.ClassDef) -> str:
    """The identity of ONE class definition, which is where it is written.

    A pure function of the node, because three callers have to agree on it and
    they see the tree from different heights: the binding walk, the mutation walk
    and the allowlist audit, which reads one top level statement at a time and
    has no walk above it at all. Derived rather than passed, so they cannot drift.
    """
    return f"{node.name}{_DEFINED}{node.lineno}"


def _sequences(scope: ast.AST):
    """Every STATEMENT LIST one scope holds, stopping where a nested scope begins.

    Two statements in one list run one after the other. Two statements in two
    lists of one ``if`` or one ``try`` do not, and that is the only distinction
    ``_alternate_classes`` needs.
    """
    for holder in (scope, *_scope_nodes(scope)):
        for _, value in ast.iter_fields(holder):
            if isinstance(value, list) and any(isinstance(one, ast.stmt) for one in value):
                yield value


def _alternate_classes(scope: ast.AST) -> dict[str, tuple[str, ...]]:
    """Same-named class definitions in one scope that NO SINGLE RUN reaches twice.

    A scope that writes ``class Keeper`` twice in one statement list has one
    reachable ``Keeper``, the last, and the first one's attributes are gone: the
    name has been taken and ``Keeper.mod`` is an ``AttributeError``. Reporting
    nothing there is correct, and the residual "A class rebound after its own
    definition is no longer reachable by name" records it.

    That judgement is FALSE the moment the two definitions sit in two arms of one
    conditional, because only one arm runs and no name was taken from anything.
    ``Keeper.mod`` is then whatever the arm that ran bound, so a module bound in
    EITHER arm can write, on the same reading ``_bound_value`` already gives
    ``alias = config if flag else other``.

    What comes back is keyed by the definition the NAME settles to, which is the
    last one, and lists the definitions that no run can have replaced it. It is
    kept apart from ``families`` on purpose. Two arms are not two classes in an
    inheritance relation: an alternate is reachable through the CLASS spelling and
    through nothing else, because ``self`` inside one arm's method is an instance
    of that arm's class and never of the other's.
    """
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
    """Every sub-expression an expression could carry a MAPPING out of.

    A NAMESPACE IS A VALUE THAT PROPAGATES, which is what four rounds of
    enumerating spellings kept missing. ``dict(vars(Path))`` and
    ``{**vars(Path)}`` were written out one at a time, and then
    ``Path.__dict__ | {}``, ``vars(Path).copy()`` and ``ChainMap(vars(Path))``
    were each the same act one operator out, all three measured quiet and all
    three executed to confirm they write a real file. ``collections`` is on the
    allowlist, so the third needs no forbidden import either.

    The rule underneath is not a list: a namespace is a mapping derived from a
    type's ``__dict__``, and any expression that preserves mapping-ness preserves
    the risk. So the OPERAND POSITIONS are what is named here rather than the
    operations, and a namespace found in any of them comes back out.

    A CALL carries one through its arguments, through its keywords, which is what
    ``dict(**vars(Path))`` is, and through its RECEIVER, which is what
    ``vars(Path).copy()`` is. A BINARY OPERATOR carries one through either side.
    A dict literal carries one through a ``**`` spread, and through nothing else:
    ``{"a": vars(Path)}`` is a mapping whose VALUE is a namespace, which is not
    the same thing and is already read as an element binding.

    What keeps this off ordinary code is unchanged and is the receiver: the
    lookup still has to name a mutating method, and an expression with no
    ``__dict__`` and no ``vars`` at its root is not a namespace however it is
    combined.
    """
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            yield node.func.value
        yield from node.args
        yield from (word.value for word in node.keywords)
    elif isinstance(node, ast.BinOp):
        yield node.left
        yield node.right
    elif isinstance(node, ast.Dict):
        yield from (
            value for key, value in zip(node.keys, node.values) if key is None
        )


def _namespace_of(
    node: ast.AST | None, table: dict[str, _Bound], instance: _Instance
) -> _Namespace | None:
    """The attribute mapping one expression IS, or None.

    TWO ROOTS AND ONE PROPAGATION RULE, rather than a list of spellings. A type's
    ``__dict__`` and the ``vars`` of one are the only two expressions that
    ORIGINATE a namespace, and they are exact rather than heuristic: they are the
    only two that hand back the function object itself. Everything else that has
    ever been added here was a way of carrying one of those two along, and adding
    them one at a time is a race the author reading this file wins.

    The receiver is what keeps this narrow. ``counts["rename"]``,
    ``row["truncate"]``, ``LABELS["touch"]`` and ``ACTIONS["mkdir"]`` are ordinary
    mappings and every one of them was a finding on the reading that left the
    receiver out, and none of them has a ``__dict__`` or a ``vars`` anywhere
    underneath it.
    """
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
    """What one expression evaluates to in the table, or the empty string.

    A CONDITIONAL is read through, because ``alias = config if flag else config``
    and ``alias = config or fallback`` are both ordinary refactors that hand the
    module on, and both rendered no receiver key at all: the whole expression is
    not a name, a subscript or an attribute. Either branch resolving is enough,
    since a receiver that is the module on one path can write on that path.

    THIS IS THE ONE PLACE A RECEIVER IS RESOLVED, which is the point. Rule 1 asks
    it about ``alias.save``, rule 5 asks it about ``table["write_text"]``, and a
    binding asks it about its own right hand side. While rule 5 read its receiver
    inline instead, ``table = vars(Path)`` was one line away from a written file.

    AN ATTRIBUTE OF A CLASS IS READ THROUGH THE CLASS, in two hops rather than as
    one flat spelling, and that is what lets a class be identified by its
    definition site instead of by its name. ``Keeper.mod`` resolves ``Keeper``
    first, and only a scope that can still see that name gets the attribute:
    ``def go(Keeper)`` takes the name back and the parameter really is a different
    object. ``Outer.Keeper.mod`` is the same two hops twice.

    The FLAT key is still tried underneath, because ``Keeper.mod = config``
    written from outside the class binds the spelling and nothing else.
    """
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


def _class_of(
    node: ast.ClassDef, table: dict[str, _Bound], instance: _Instance
) -> _Class:
    """One class definition's identity, with its BASES resolved through the table.

    A base is an ordinary expression evaluated where the ``class`` statement is
    written, so it is resolved the way every other receiver is rather than read
    off its own spelling. ``class Row(Base)`` in a file where ``Base`` was taken
    back by something else inherits nothing, which is the correct answer and is
    the same answer ``alias.save`` gets under a shadowed ``alias``.

    A base this cannot resolve is dropped rather than guessed. ``class
    Row(namedtuple("Row", "a"))`` and ``class Row(SomeImportedThing)`` are both
    ordinary, neither names a class this file defines, and a guard that invented
    an identity for them would be the second recurring defect one more time.
    """
    return _Class(
        _class_key(node),
        tuple(
            found.key
            for found in (_bound_value(one, table, instance) for one in node.bases)
            if isinstance(found, _Class)
        ),
    )


def _elements(value: ast.AST | None):
    """Every constant-addressed element of a container literal, index and node.

    The CONSTANT KEY condition on a dict is what keeps this readable: a key that
    is a name or an expression has no spelling a subscript receiver could be
    matched against, and reading one would ask an ``ast.Name`` for a ``.value``
    it does not have. ``test_a_container_key_this_cannot_read_binds_nothing``
    drives it.

    A LITERAL AND NOTHING ELSE, which is a standing limit rather than an
    oversight: ``self.mods = [config for _ in range(1)]`` followed by
    ``self.mods[0].save(cfg)`` is quiet, because a comprehension is a scope with
    its own bindings and its element is an expression evaluated per iteration.
    Filed as the residual finding titled "A container built by a comprehension
    binds none of its elements", by TITLE rather than by number: this branch and
    ``main`` have both appended to that file and five of this branch's residual
    numbers name different findings there.
    """
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
    """What a container literal binds, element by element and NESTED.

    ``MODS = [config]`` and ``MODS = {"c": config}`` are ordinary code, and
    ``MODS[0].save(cfg)`` and ``MODS["c"].load_from_path(p)`` reach the writer
    through them. So is ``MODS = [[config]]``, and reading only the outer level
    lost ``MODS[0][0].save(cfg)`` outright: the element was a list, a list
    renders no receiver key, and the binding stopped there. The recursion costs
    one line and closes the whole family rather than its first member.
    """
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
    """Every admitted module or namespace a loop could hand its target.

    A literal is read element by element; a name is read through whatever its
    elements were already bound to, so ``MODS = [config]`` followed by ``for mod
    in MODS`` resolves the same way ``MODS[0]`` does.
    """
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
    """Parameters whose DEFAULT is an admitted module or a namespace.

    ``def f(cfg, mod=config)`` binds ``mod`` inside the function while the
    parameter list otherwise shadows everything it names, so this has to be read
    back after the shadowing rather than before it. The default EXPRESSION is
    resolved against the enclosing scope, because that is where it is evaluated.
    """
    found: dict[str, _Bound] = {}
    positional = [*args.posonlyargs, *args.args]
    supplied = positional[len(positional) - len(args.defaults) :]
    pairs = [*zip(supplied, args.defaults), *zip(args.kwonlyargs, args.kw_defaults)]
    for parameter, default in pairs:
        owner = _bound_value(default, modules, instance) if default is not None else ""
        if owner:
            found[parameter.arg] = owner
    return found


def _returned_value(
    node: ast.AST, modules: dict[str, _Bound], instance: _Instance
) -> _Bound:
    """What a function hands back, so ``_mod().save(cfg)`` resolves.

    A namespace comes back on the same terms a module does, because ``def
    _table(): return vars(Path)`` followed by ``_table()["write_text"](p, d)`` is
    the returned spelling of the same two lines rule 5 shipped blind to.
    """
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
    """The admitted modules one assignment target takes, keyed by receiver.

    PARALLEL UNPACKING is read element by element against the right hand side,
    and the branch this replaces never fired for the shape it looked like it
    handled. It asked ``_bound_module`` about the WHOLE right hand side, which
    for ``alias, other = config, 1`` is a tuple and renders no receiver key, and
    then asked ``_element_bindings`` to index each TARGET by position, which
    produced the meaningless keys ``alias[0]`` and ``other[0]``. Reverting the
    whole branch killed nothing, which is the measurement that found it.

    A NAME comes back whether or not it resolved, and an earlier docstring here
    said "only what RESOLVED comes back", which was true of the OBJECT half only
    and loose about the other. The empty owner on a name is the point rather than
    a leftover: ``_scope_own_bindings`` needs to hear that an assignment happened
    and failed to resolve, because a name is kept only when EVERY binding of it
    agrees. An unreadable TARGET, one that renders no receiver key at all, is the
    case that really comes back with nothing, and the caller reads that name from
    ``_bound_here`` instead: a name taken back by an unpacking this cannot follow
    is the same fact as a name taken back by a ``with``, and one mechanism
    answering both is one thing to keep true rather than two that can drift apart.
    """
    if isinstance(target, (ast.Tuple, ast.List)):
        if isinstance(value, (ast.Tuple, ast.List)) and len(target.elts) == len(
            value.elts
        ):
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
    """Every binding ONE statement makes, and the bare WRITER names it imports.

    None of these is an attack. ``alias = config`` is a plain refactor,
    ``self.mod = config`` is a constructor, and a default argument is how a
    module gets injected for a test. They are listed together because they are
    all the SAME act: the receiver a report finally writes through is no longer
    spelled with the module's name, and the guard is for the ordinary author who
    wrote one of them without meaning anything by it.

    An IMPORT is one of them rather than a separate table, and that is what makes
    the shadowing correct. While the imports were swept flat and the rebindings
    layered on top, a module that imported ``config`` and then assigned that name
    something else kept the import binding forever, because nothing in the sweep
    could see that the two were about the same name in the same scope.
    """
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
    """What one scope binds for itself, resolved against what it can already see.

    A NAME is kept only when EVERY binding of it in this scope resolves to the
    same module. That is what separates ``from cratekit.core import config`` in a
    file that leaves the name alone from the same import in a file that later
    writes ``config = dict(raw)``: the second has one binding that resolves and
    one that does not, so the name is nobody's module and ``config.load`` under
    it is an ordinary attribute read.

    A name that did not settle comes back with an EMPTY answer rather than not
    coming back at all, which is the same distinction the object half draws below
    and is needed for the same reason. ``class Row(Base): mod = None`` over
    ``class Base: mod = config`` binds nothing this table can read, and while that
    was recorded as silence the caller had no attribute to write for ``Row`` and
    ``Base``'s was carried into the gap. Every reader of this table tests the
    answer for truth, so an empty one is inert everywhere except where a key being
    PRESENT is itself the fact.

    EVERY binding means every one, including the ones ``_binds`` cannot read at
    all. A ``with`` target, an ``except`` target, an augmented assignment and an
    import of something that is not an admitted module each take a name and hand
    it a value this has no way to resolve, and each one therefore records a
    FAILED attempt rather than nothing. Recording nothing was the version before,
    and under it a file that imported ``config`` and then rebound the name kept
    the import's answer for the whole scope: the import resolved, the other
    statement said nothing, and nothing beats something.

    A veto written INSIDE A BRANCH is not counted, because a run that skipped that
    branch never cast it. ``class Keeper`` followed by ``if flag: Keeper =
    dataclass(Keeper)`` still has a path on which the name is the class, and a
    write reachable on one path is a write. What that does NOT do is put a name
    back: ``_names_taken`` is unchanged, so a name whose only binding is inside a
    branch is still taken and still comes back unresolved.

    AN OBJECT KEY IS NOT EXEMPTED BY THE SAME BRANCH, and it was, in prose, for
    six rounds. A name survives a skipped rebinding because the statement that
    bound it ran anyway; an attribute set only in a base's ``__init__`` does not,
    because on the arm that skipped the subclass's override the attribute was
    never created at all. The condition below asks ``_chains_to_base`` and the
    scope's own table which of the two it is looking at, and six ordinary branch
    spellings that reported a write are the measurement that put it there.

    A NESTED DEFINITION is read for what it BINDS rather than only as a name this
    cannot resolve. A ``def`` still binds something with no value in this table,
    so it is a failed attempt; a ``class`` binds a ``_Class``, which is a value
    like any other and which is what makes the class's own attributes reachable
    through its name. Two ``class Keeper`` statements in one scope are one name
    and the LAST one wins, which is what the interpreter does with them, and the
    first one's attributes become unreachable exactly as they are at runtime.

    An OBJECT key, anything spelled with a dot, a bracket or a pair of
    parentheses, is not a name and is not treated as one. ``self.mod`` is a fact
    about an object, it is set in one method and read in another, and lexical
    scoping is the wrong shape for it. What makes that safe is that the object
    binding is only CREATED when its right hand side resolves in the scope doing
    the assigning, so ``self.config = config`` inside ``def __init__(self,
    config)`` binds nothing at all: there, ``config`` is the parameter. What makes
    it UNIQUE is ``instance``: the key is ``Keeper#412::self.mod`` rather than
    ``self.mod``, so the fact stays a fact about one class DEFINITION rather than
    about every class anybody spelled that way.

    AN OBJECT KEY RECORDS A FAILED ATTEMPT TOO, on the same rule as a name and for
    the same reason. Binding nothing and taking the key back are two different
    facts, and while an unreadable right hand side recorded NOTHING, the second
    was invisible: ``self.mod = dict(raw)`` in ``Row.__init__`` left no key under
    ``Row``, and the key ``Base`` declared was carried down into that hole. Six
    ordinary shapes wrote the configuration file with both structural guards and
    the audit green on that reading, every one of them a subclass overriding an
    attribute its base binds, which is the most ordinary thing inheritance does.
    A key that resolves still wins over one that did not, because two assignments
    to one attribute of one class mean the attribute IS the module on one path.

    The loop is a FIXED POINT for the same reason the outer one is. ``alias =
    config`` followed by ``beta = alias`` needs two passes, and a pass count
    written as a number is a constant nothing can drive. It terminates because
    the table only ever grows and its keys come from the finite set of receiver
    expressions this scope spells.
    """
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
    """The bindings one scope really sees: inherited, shadowed, then its own.

    THIS IS THE WHOLE OF THE SCOPE FIX. The previous version removed PARAMETER
    names from a table swept flat off the entire file, so a parameter was the only
    thing in Python that could take a name back. Every other rebinding left the
    stale import binding live: ``for config in rows``, ``config = dict(raw)``,
    ``with handle as config``, ``except ValueError as config``, ``config, other =
    pair``, a walrus, a comprehension target and a module-level assignment were
    each reported as a write to the library, on a package whose only import of
    that name is line 61 of ``aging``.

    The order is shadow first, add second, and it has to be. A scope's own
    ``alias = config`` binds a name the scope also takes, so removing everything
    the scope binds and then putting back only what resolved is the one ordering
    that gets both directions right.

    DEFAULTS ARE READ AGAINST THE ENCLOSING TABLE, after the shadowing, because
    ``def f(cfg, mod=config)`` evaluates that default where the ``def`` is written
    while the parameter list otherwise shadows everything it names.

    The scope's OWN bindings come back separately as well as merged, because a
    CLASS BODY needs exactly them: what a class binds for itself becomes an
    attribute of that class, and what it merely inherited does not.
    """
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
    """Which parameter of one method is the instance, and what it renders as.

    THE FIRST POSITIONAL PARAMETER, whatever it is called, because ``self`` is a
    convention and a guard keyed on a convention is a guard one rename walks past.
    A ``staticmethod`` has no instance at all and a ``classmethod``'s first
    parameter is the CLASS, so ``cls.mod`` resolves exactly where ``Keeper.mod``
    does rather than where ``Keeper::self.mod`` does.
    """
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
    """Every function one scope ATTACHES to a class it defines, by ``Row.go = _go``.

    A method written outside its class and bound to it afterwards is ordinary
    Python and is how a mixin gets assembled at runtime, how a monkeypatch is
    spelled, and how a decorator's inner function ends up on a type. The function
    is walked as a plain module level function otherwise, so its first parameter
    is nobody's instance and ``self.mod.save(cfg)`` inside it resolves against
    nothing at all.

    Read off the ASSIGNMENT rather than off the function, because the assignment
    is the only place the pairing is written. The class is named by its definition
    site the same way every other class key is, so the two walks and the audit all
    agree without any of them being told.
    """
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
    """The class identity and instance one NESTED scope is read under.

    Four cases and they are not the same. A class is read under its own
    DEFINITION SITE, whatever scope it was written in. A method of a class gets a
    fresh instance from ``_method_instance``. A function ATTACHED to a class by a
    later assignment is a method of that class wherever it was written. Anything
    else INHERITS the instance it was written inside, because a function nested in
    a method reads ``self`` through the closure, and it loses it again if it binds
    that name itself.

    WHAT THIS COSTS, measured rather than left implicit: a class REBOUND after
    its own definition, ``Keeper = dataclass(Keeper)``, is no longer reachable by
    name, because the assignment and the ``class`` statement are two bindings of
    one name that do not agree. Round six kept it by keying the attribute as flat
    TEXT, which is the same reading that made a parameter called ``Keeper``
    unable to take the name back. Filed as the residual finding titled "A class
    rebound after its own definition is no longer reachable by name", by TITLE
    rather than by number.

    THE DEFINITION SITE IS THE IDENTITY, and the lexical path was the version
    before. A path is the class's outside SPELLING, which is a different thing
    from what it names: a class in a class was ``A.Keeper`` and a class in a
    FUNCTION was the bare ``Keeper``, so two factories each returning a ``Keeper``
    shared one root and one factory's class body decided for the other's. That is
    the second recurring defect, identity that is not unique, aimed at a class
    whose enclosing scope does not name it. The outside spelling is not lost by
    this: it is resolved through the table, where ``Keeper`` is a name bound to a
    ``_Class`` and a parameter of that name can take it back.
    """
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
    """What a nested scope is handed: the parent's view, or the parent's OWN INPUT.

    A CLASS BODY is the only scope in Python whose names its nested scopes cannot
    see, so a method is handed the table its class inherited rather than the one
    its class built. Read the other way, ``mod.save(cfg)`` in a method of ``class
    Keeper: mod = config`` is a write, on a line the interpreter answers with a
    NameError.

    Named once because the binding walk and the mutation walk both need it and
    they must not disagree. Written out twice, one of the two copies measured
    zero, which is what a duplicated fact looks like from the mutation table.
    """
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
    """One scoped pass over a tree, collecting every OBJECT binding it DECLARES.

    Names stay where they were written. Objects are carried out into one
    file-wide table, because ``self.mod`` set in a constructor is read in a
    sibling method and ``_mod()`` is a fact about a function rather than about
    the scope that calls it. Every object key carries its OWNER, so ``self.mod``
    in two classes is two facts rather than one.

    ONLY THE SCOPE'S OWN bindings are carried out, and reading them off the
    scope's whole VIEW was the version before. The two were the same answer while
    everything in the view had come from this table in the first place. They stop
    being the same answer the moment the table is also handed keys a class
    REACHES through its bases: those are derived, not declared, and letting a
    derived key back in as a declared one is how a fact about one class becomes a
    fact about its siblings.

    ``families`` is the other half of that, and it is recorded here because this
    is the walk that knows which scope a ``class`` statement sits in. Who
    inherits from whom is a fact about the file rather than about any one scope,
    so it goes into one file-wide record and the closure is taken once, above.

    A CLASS BODY is where the two halves meet. What it binds for itself is an
    attribute, reachable as ``Keeper.mod`` from outside and as ``self.mod`` from
    any method, so both keys are written; and its methods are handed the table
    the class INHERITED rather than the one the class built, because a class
    body's names are not visible inside its methods.

    THE TWO SPELLINGS ARE NOT THE SAME STRENGTH, and writing them as if they were
    reported the most ordinary class there is as a write. ``Keeper.mod`` really is
    the module and a read through the class really does write. ``self.mod`` in a
    class whose ``__init__`` assigns that attribute does not, because an INSTANCE
    attribute shadows a class attribute unconditionally: measured, ``Keeper.mod``
    is the module, ``Keeper(raw).mod`` is a dict on every input, and the call
    raises ``AttributeError`` every time. So the instance spelling is written
    FAINT, which yields to any instance scope's own write and to nothing else.

    A ``del`` PUTS THE CLASS SPELLING BACK, which is the other direction of the
    same fact and is a real write rather than a curiosity: ``del self.mod`` in a
    method of that same class makes the next read reach the module again.

    A BINDING THAT DID NOT RESOLVE IS STILL WRITTEN, under both spellings, and
    that is the class body's half of the failed attempt rule. ``class Row(Base):
    mod = None`` takes the attribute back from ``Base`` at runtime whatever
    ``None`` is, and while a falsy value was skipped here the key stayed empty for
    ``Row`` and inheritance filled it from ``Base``. A key that resolves still
    overwrites one that did not, and one that did not never overwrites one that
    did, so the answer does not depend on which scope this walk reached first.
    """
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
    """Write one declared attribute key: resolved wins, unresolved only fills.

    Both directions of one rule, in the one place both halves of the walk use it,
    because they must not disagree. A key that RESOLVED is the strongest fact
    available and overwrites anything, so a class that binds its attribute to the
    module in one method and to an argument in another is still a class that can
    write. A key that did NOT resolve is weaker than that and stronger than
    silence: it says the class took the attribute for itself, which is what stops
    a base's binding being carried into it, and it never overwrites a resolved
    answer, so the result does not depend on the order the walk visited scopes in.

    A THIRD TIER SITS UNDER BOTH, and reading it as the first was a false positive
    on ``class Keeper: mod = config`` with an ordinary ``__init__`` under it. The
    class body's INSTANCE spelling is a WEAK claim: it says what ``self.mod``
    means to an instance that never had one assigned, and an instance assignment
    unconditionally shadows it. So a weak write yields to any key an instance
    scope has already claimed, and an instance scope's write overwrites a weak one
    whether or not it resolved. The class spelling ``Keeper.mod`` is not weak,
    because nothing an instance does changes what the class attribute is.

    ``faint`` IS A MARK RATHER THAN AN ORDER, and what it rests on is stated
    rather than implied: ``_walk_bindings`` records a class body's own keys BEFORE
    it walks into any of that class's methods, so the weak write is always first
    and every later write to that key is an instance scope's. A guard against the
    other order was written here and measured zero on every fixture in the suite,
    because no walk produces it, and a clause no input reaches is a clause nobody
    can check. The source order a person controls is driven instead: the class body
    is written above the constructor in one fixture and below it in another.
    """
    if weak:
        objects[key] = value
        faint.add(key)
        return
    if value or key not in objects or key in faint:
        objects[key] = value
    faint.discard(key)


def _related(
    start: str, families: dict[str, tuple[str, ...]], *, upward: bool
) -> list[str]:
    """One class and the classes an attribute lookup on it can reach, NEAREST FIRST.

    Two directions, and reading them as one is what would put this defect back.
    UPWARD is inheritance: ``class Row(Base)`` sees everything ``Base`` bound,
    because that is what attribute lookup does. DOWNWARD is the mixin: a method
    written in ``WriterMixin`` is called with a ``Row`` as its ``self``, so what
    ``Row`` binds is what that method can reach.

    NEITHER DIRECTION CROSSES SIDEWAYS, which is the whole reason this is a walk
    rather than a connected component. Two subclasses of one base are not each
    other's business: an ``Injected`` that takes its module as a constructor
    argument and a ``Holder`` that binds the real one are the pair this file
    already has a test for, and reading the family as one component would hand
    ``Holder``'s binding to ``Injected`` through their shared base.

    Breadth first so the nearest relative is first, since an override is the
    nearest one and the caller keeps the first answer it is given.
    """
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
    """Every attribute key a class REACHES, from the keys its family DECLARED.

    THE KEY LANDED ON THE CLASS THAT DECLARES rather than on the class that
    reaches, which is the third round running that a fix on this unit landed on
    the wrong object. ``class Row(Base)`` with ``self.mod = config`` in
    ``Base.__init__`` had a key under ``Base`` and none under ``Row``, so the
    subclass reached the writer with nothing bound anywhere it looked. A mixin and
    an inherited class body attribute are the same fact from the same hole, and a
    mixin is ordinary author code rather than evasion.

    A CLASS ATTRIBUTE is resolved UPWARD only, because ``Row.mod`` is whatever the
    nearest ancestor bound and a subclass's binding is no business of the base's.
    An INSTANCE attribute is resolved upward AND downward, because ``self`` in a
    base's method is an instance of that class or of anything under it, which is
    exactly what a mixin relies on. The two are separated here rather than merged
    because merging them is what would let one subclass see a sibling's binding.

    AN OVERRIDE BLOCKS UPWARD AND NEVER DOWNWARD, which is the same asymmetry the
    two directions already have and is the half a failed attempt makes visible. A
    nearer ancestor that took the attribute for itself really does stand between
    the reader and the farther one, so its unresolved key is carried and stops the
    carry there: that is what makes ``Base`` bind the module, ``Middle`` rebind it
    to an argument and ``Row`` read it come out quiet. A SUBCLASS that takes the
    attribute for itself stands between nobody and nothing, because ``self`` in a
    mixin's method is an instance of some OTHER subclass just as easily, so an
    unresolved key is skipped on the way down and a sibling that binds the real
    module is still reached.

    Kept apart from the declared table rather than folded into it, so that a
    derived key is never re-derived from. The caller merges with declared on top.
    """
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
    """Copy one class's declared keys onto another class's root, nearest wins.

    ``overriding`` says whether a key the source declared but could not resolve is
    worth carrying. Up the inheritance chain it is, because a nearer class that
    took the attribute is between the reader and everything above it. Across a
    mixin or an alternate definition it is not, because neither of those is
    between anything and anything.
    """
    for key, value in declared.items():
        if not key.startswith(prefix) or (not value and not overriding):
            continue
        found.setdefault(f"{target}{key[len(source):]}", value)


def _global_aliases(
    modules: dict[str, _Bound],
) -> dict[str, _Bound]:
    """``globals()["config"]``, which is the module reached without its name.

    A module level name IS an entry in the module's own globals mapping, so
    ``globals()["config"].save(cfg)`` writes the configuration file with the word
    ``config`` appearing only inside a string. That is the same act as ``alias =
    config`` with the alias spelled as a lookup, and it belongs in the same table
    rather than in a rule of its own.
    """
    return {
        f"globals()[{name!r}]": value
        for name, value in modules.items()
        if name.isidentifier()
    }


def _writer_bindings(
    tree: ast.AST,
) -> tuple[dict[str, _Bound], frozenset[str]]:
    """Receivers bound to an admitted module, and names bound to a writer itself.

    Read off the import statements for the same reason ``_resolved_imports``
    reads ``alias.name``: an alias is how a name check gets walked past, and
    ``from cratekit.core import config as settings`` followed by
    ``settings.save(cfg)`` spells no admitted module anywhere in the file.

    THE IMPORTS ARE NOT THE WHOLE BINDING TABLE, and an earlier version of this
    was only them. ``aging`` already spells ``from cratekit.core import config``,
    so two added lines, ``alias = config`` and ``alias.save(cfg)``, wrote the
    configuration file with both structural guards green. Everything ``_binds``
    reads is one more spelling of that same two-line refactor, and the receiver
    check is worth nothing until it follows them.

    THE TABLE IS ALSO NOT FLAT, which is the other half and cost more. A file's
    bindings are not a set of facts about the file, they are facts about scopes,
    and sweeping them flat made the guard fire on ten ordinary shapes while
    missing three real ones. The walk is by scope now, and what comes back is the
    MODULE scope's names plus every object binding any scope made, each one keyed
    with the class that owns it so two ``self.config`` are two facts.

    The second half is the shape a receiver check would otherwise lose outright.
    ``from cratekit.core.config import save`` binds the writer to a bare local,
    and both halves of that import are permitted, so the bare name IS the writer
    from there on and is matched as one. A STAR import binds every one of them at
    once, with no name in the file to read, so it is expanded from the set.

    DECLARED AND REACHED ARE TWO TABLES, and the closure between them is taken
    here because inheritance is a fact about the whole file rather than about any
    one scope. What a class body and a constructor bind is DECLARED; what a
    subclass, a base and a mixin can therefore see is REACHED. They are kept apart
    so a reached key is never re-derived from, which is what would carry one
    subclass's binding sideways into a sibling through their shared base. Declared
    wins on a collision, because a subclass that binds the name itself has
    overridden what it inherited.

    The outer loop is a FIXED POINT rather than a pass count. An object binding
    made in one scope is read in another, and valid Python does not promise the
    two are in document order. Measured, a sixty hop chain written entirely use
    before definition resolves, which a pass count of one would not. Inheritance
    needs the same loop for the same reason: ``class Row(Base)`` may be written
    above ``Base``, and a chain of three classes needs a pass per link.
    """
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
    """Every name an ``import X`` statement binds to a MODULE.

    Read for one reason, and it is a live one. ``open`` reached through a module
    is a different function from ``open`` reached through a path: the module takes
    the file first, and the path object IS the file and takes the mode first.
    Without this, every module level ``open`` had its FILE argument read as its
    mode, and ``os.open(str(path), os.O_RDONLY)`` at ``cratekit/core/jobs.py``
    line 788, a pure read for an fsync, was a write.
    """
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.asname or alias.name.split(".", 1)[0])
    return frozenset(found)


def _receiver_module(
    node: ast.AST, modules: dict[str, _Bound], instance: _Instance
) -> str:
    """Which admitted module a receiver was BOUND to, or the empty string.

    Resolution is by binding and by nothing else. A receiver with no binding is
    UNRESOLVED, which is not the same answer as a module named after the
    variable: absence read as evidence of absence is the defect this file keeps
    producing, and here it produced it aimed at correct code. ``view.save``,
    ``spec.load``, ``self.config.load`` and a parameter called ``naming`` are all
    ordinary, and a guard that fires on them is a guard somebody weakens (P7).

    A NAMESPACE is not a module, so it comes back as the empty string here and is
    read by rule 5 through ``_bound_value`` instead. One table, two kinds of
    value, and each rule asks for the kind it can use.
    """
    found = _bound_value(node, modules, instance)
    return found if isinstance(found, str) else ""


def _writer_names_of(dotted: str) -> frozenset[str]:
    """The qualified writers one module's OWN bare names spell.

    Inside ``config.py`` a call to ``_mkdir_private`` has no receiver, and it is
    still ``config._mkdir_private``: a bare name inside a module is qualified by
    that module. Without this the audit would stop seeing the shape it exists for
    the moment the generic names became receiver qualified, which is the way a
    fix for over-restriction turns into a hole.
    """
    short = dotted.rsplit(".", 1)[-1]
    return frozenset(
        name.split(".", 1)[1]
        for name in QUALIFIED_MUTATIONS
        if name.split(".", 1)[0] == short
    )


def _namespace_reads(
    space: _Namespace,
    wanted: ast.AST | None,
    modules: dict[str, _Bound],
    instance: _Instance,
    *,
    reflection: bool,
) -> str | None:
    """What one lookup INTO a type's attribute mapping reports, or None.

    Named once because two rules ask it: the subscript ``table["write_text"]`` and
    the call ``Path.__dict__.get("write_text")``, which are the same act and
    differ only in whether the mapping was indexed or asked. A second copy of the
    key check answering one of them would be the divergence this file already
    has one of.

    A COMPUTED key is read the way rule 4's computed half is, on the reflection
    switch and for the same reason rather than by analogy. ``Path.__dict__["write"
    + "_text"]`` inside a package that has promised not to write is a lookup this
    checker cannot read, which is the violation there; ``vars(spec)[field]`` is
    ordinary everywhere else, and an audit that calls it a writer is an audit
    somebody switches off (P7).
    """
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
            (_receiver_key(target), node.value)
            for target in node.targets
            if _receiver_key(target)
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
    """Every reflective read in ``tree`` whose RESULT is called somewhere.

    THE SWITCH WAS DECIDED SYNTACTICALLY AND LOCALLY, and that is what this
    replaces. It read ``called`` off nothing but ``Call`` nodes whose ``func`` was
    itself a ``Call``, so it saw ``getattr(path, name)(data)`` and nothing else.
    Eight indirect spellings of the identical act walked past it, every one of
    them a shape somebody writes on purpose: bind it and call the name, return it
    and call the result, put it in a list and call the element, use it as a
    decorator, hand it to a factory that is invoked on the spot.

    The binding table is what closes them, which is why this waited for the table
    to have scope. A read bound to a name that this file CALLS is the same act as
    calling it inline, and so is a read stored in a container element that is
    called, and so is a read returned by a function whose result is called.

    ONE SHAPE IS OUT OF REACH AND IS NAMED RATHER THAN LEFT SILENT.
    ``map(getattr(p, n), items)`` hands the read to a callee that will invoke it,
    and whether a callee invokes its argument is a fact about the callee, not
    about this file. A rule that assumed it would fire on
    ``print(getattr(row, field))``, which is the P7 shape this guard is written
    around. The one argument case that IS read is the factory invoked in place,
    ``partial(getattr(p, n))(d)``, because there the invocation is written here.

    THAT LIMIT IS A MAINTENANCE CHOICE AND NOT A FORCED ONE, and saying so is the
    honest version of the paragraph above. ``map``, ``filter``, ``sorted(key=)``
    and ``functools.reduce`` do unconditionally invoke the callable they are
    handed, so a bounded list of them would close this without touching
    ``print``. What that list costs is a NAME CHECK on a builtin, which is the
    one thing a local ``def map(...)`` walks past and the kind of list that goes
    stale silently. It is left open deliberately, and the LITERAL half already
    catches ``map(getattr(p, "write_text"), items)``, so what is open is the
    computed name handed to a known-invoking callee and nothing wider.
    """
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
            if isinstance(node.func, ast.Subscript) and isinstance(
                node.func.slice, ast.Constant
            ):
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
    """The five rules above, applied to any node rather than to a whole module.

    Split out so the allowlist audit below can ask the same question about ONE
    function. A second copy of these rules answering it would be the divergence
    ``tests/_source_guards.py`` exists because of, and it would diverge in the
    direction that matters: the audit would stop recognizing a write shape this
    guard had just learned.

    ``modules`` and ``direct`` are what a bare node cannot read for itself: the
    bindings that say which receiver is an admitted module and which local name
    is an admitted writer. ``invoked`` and ``libraries`` are the same thing for
    two questions that are only answerable from the WHOLE file: whether a
    reflective read's result is called somewhere else in it, and which names are
    imported modules. The audit reads all four off the module and hands them
    down, because a function read on its own has no import statement in it.

    THE WALK IS BY SCOPE rather than flat, and so is the binding table it walks
    with. A parameter shadows, and so does a loop target, a ``with`` target, an
    ``except`` target, a walrus, a comprehension target and a plain assignment,
    and while only parameters shadowed, ten ordinary shapes in ``aging`` were
    reported as writes to the library.

    ``reflection`` turns off ONE HALF of rule 4, the COMPUTED attribute reached
    through ``getattr``, and only the audit does that. Rules 1 to 3 and 5 each
    describe an act that CHANGES A FILE; the computed half describes an act this
    checker cannot read, which is a violation inside a package that has promised
    not to write and is ordinary everywhere else. Left on, it reported six
    reflective helpers in ``config``, ``naming`` and ``taxonomy`` as writers, and
    an audit that cries wolf about ``getattr(row, field)`` is an audit somebody
    switches off.

    THE SWITCH IS ON THE RESULT BEING CALLED, not on literal versus computed.
    Gating the literal half was the first version and it lost ``getattr(path,
    "write_text")(data)``; ungating only the literal half was the second and it
    lost ``getattr(path, "write_" + "text")(data)``, the same helper one token
    longer; deciding it on the local syntax of one expression was the third and
    it lost eight indirect spellings, the same helper one LINE longer. It is
    decided on the binding table now, which is the first version of it that is
    not a token count.
    """
    if invoked is None:
        invoked = _invoked_reads(tree)
    if libraries is None:
        libraries = _imported_modules(tree)
    resolved, reachable, _ = _visible_bindings(
        tree, dict(modules or {}), direct, instance
    )
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
                node, resolved, reflection=reflection, invoked=invoked,
                libraries=libraries, instance=instance,
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
        #
        # NO ARGUMENT IS A KEY THIS CANNOT READ, and requiring one was a hole
        # shaped exactly like the ones this rule keeps growing: a method that
        # takes nothing was invisible, so ``vars(Path).copy()`` walked past the
        # branch on arity alone. It is the same answer the computed key gets and
        # it is on the same switch, so inside the governed package a lookup this
        # cannot read is the violation and everywhere else it is quiet.
        #
        # Its cost across the whole tree is ONE line, ``state.items()`` at
        # ``core/rb_writer.py`` 1843, in a module that is neither governed nor
        # admitted. Recorded as the residual finding titled "A namespace method
        # with no argument is an unreadable lookup", by TITLE rather than by
        # number, because this branch's residual numbers collide with different
        # findings on ``main``.
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
    owner = (
        _receiver_module(receiver, resolved, instance) if receiver is not None else ""
    )
    if wanted.value in FILESYSTEM_MUTATIONS or (
        owner and f"{owner}.{wanted.value}" in QUALIFIED_MUTATIONS
    ):
        return [f"line {node.lineno}: {name}({wanted.value!r})"]
    return []


#: The builtin and the dunder that read an attribute by NAME. ``getattr`` is the
#: one anybody writes; ``__getattribute__`` is what it calls, it is reachable in
#: both a bound and an unbound spelling, and both of them write when they are
#: handed ``"write_text"``.
#:
#: NAMING THE DUNDER IS NOT FREE, and an earlier comment here said it cost one
#: set member and closed a spelling that otherwise falls through every rule. The
#: first half was true. The second was not: the most ordinary thing anybody
#: writes with the dunder is ``def __getattribute__(self, name): return
#: super().__getattribute__(name)``, and with the computed half of rule 4 on,
#: that delegation was a finding. Nothing in ``src`` spells it, so the suite was
#: green, which is the only reason the claim survived being written.
_REFLECTIVE_READERS = frozenset({"getattr", "__getattribute__"})


def _reflective_arguments(
    node: ast.Call, name: str
) -> tuple[ast.AST | None, ast.AST | None]:
    """The receiver and the attribute NAME one reflective read was handed.

    ``getattr(obj, name)`` and ``object.__getattribute__(obj, name)`` put the
    receiver first; the bound ``obj.__getattribute__(name)`` has already spent it
    on the attribute it was reached through, so its only argument IS the name.
    The ARITY separates them, which is the reading ``replace`` already gets.
    """
    if len(node.args) >= 2:
        return node.args[0], node.args[1]
    if name == "__getattribute__" and node.args and isinstance(node.func, ast.Attribute):
        return node.func.value, node.args[0]
    return None, None


def _library_receiver(func: ast.AST, libraries: frozenset[str]) -> str:
    """The imported MODULE an attribute call was reached through, or "".

    ``io.open``, ``gzip.open``, ``codecs.open`` and ``tarfile.open`` are the
    builtin's shape: the file first, the mode second. ``Path(p).open`` and
    ``info.open`` are the other shape, because the receiver already IS the file.
    Nothing separated them, so every module level ``open`` had its FILE read as
    its mode and came back unreadable.
    """
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id if func.value.id in libraries else ""
    return ""


#: The ``os.open`` flags that cannot change a file. ``os.open`` is the one module
#: level ``open`` whose second argument is a FLAG SET rather than a mode string,
#: so reading it as a mode gives an unreadable answer and an unreadable answer is
#: a finding. ``cratekit/core/jobs.py`` line 788 opens a DIRECTORY read only to
#: fsync it, and that is what was being reported as a write.
#:
#: Listed as what READS rather than as what writes, because a flag this does not
#: know is answered the same way an unreadable mode is: reported.
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
    """Every flag name one ``os.open`` flag expression ORs, or None if unreadable.

    A BARE NAME is one of them, and leaving it out was a false positive on
    ordinary code. ``_READING_FLAGS`` holds bare names, and this could only ever
    produce one from ``os.O_RDONLY``, so ``from os import O_RDONLY`` followed by
    ``os.open(str(path), O_RDONLY)`` was an unreadable flag set and therefore a
    write. The real ``cratekit/core/jobs.py`` happens to spell it dotted, which is
    the only reason that was not live.

    Reading the name is exactly as tight as reading the attribute already was:
    neither checks that what it came off is ``os``, both answer with the last
    identifier, and an unrecognised one is still reported. A flag held in a
    variable comes back as that variable's name, which is not in
    ``_READING_FLAGS``, so ``os.open(p, flags)`` remains a finding.
    """
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
    """The literal mode an ``open`` call was given, or None when it is not literal.

    ``bound`` says which call this is, and getting it wrong is not a detail. The
    builtin takes the file first and the mode second; ``Path.open`` takes the
    mode FIRST, because its receiver already is the file. Reading position one
    for both made ``Path(p).open("w")`` report as mode ``"r"`` while the
    ``open(Path(p), "w")`` fixture was caught, so the idiomatic spelling was the
    one that got through, on a package that already reaches for ``Path`` and has
    ``pathlib`` on its allowlist.

    IT IS NOT THE SAME QUESTION AS "IS THERE AN ATTRIBUTE", which is what it was
    asked before. Every module level ``open`` is spelled as an attribute and
    every one of them takes the file first, so ``io.open(p, "rb")``,
    ``gzip.open(p, "rb")``, ``codecs.open(p, "r", "utf-8")`` and
    ``tarfile.open(p, "r")`` all reported their FILE as an unreadable mode. The
    caller reads the import table and answers the real question.

    An absent mode is the default, which reads, so it comes back as ``"r"``.
    """
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
    """Values a module-level set literal in ``source`` spells more than once.

    Read from the SOURCE rather than from the runtime object, because the runtime
    object is exactly what cannot answer this: a set deduplicates its literal at
    parse time and keeps no record of having done so.
    """
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
    """The INSTRUMENT, checked before anything is concluded from it.

    The test below asserts that three literals have no repeated element, and what
    it is really asserting is whatever this is capable of noticing. Nothing in
    this file repeats an element, so a broken reader would agree with a correct
    one everywhere the suite looks and the check would read as a pass forever.

    The missing-name assertion is driven too, because a reader that quietly found
    nothing would give the same answer as a literal with no duplicate in it.
    """
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
    """A duplicate in a set literal is silent: the runtime object deduplicates it.

    This repository has shipped that shape once with the whole suite green, in
    ``EXPECTED_PENDING``. Every other test over these sets iterates the RUNTIME
    object and is therefore blind to it, and here it would matter in the
    direction that hurts: an entry believed to be present because a reviewer read
    it in the diff, collapsed onto another, so the guard covers one fewer name
    than anybody thinks.

    THE LENGTH CHECK THAT USED TO SIT HERE IS GONE. It compared the literal's
    element count against the runtime set's, and for a set literal of string
    constants there is no input on which it and the duplicate check disagree:
    every repeated element is one the runtime drops, so the two fire together or
    not at all. It was a guard covered by the shape of its own sibling, which is
    the same defect as a guard covered by a docstring, and removing it alone
    killed nothing.
    """
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
#:
#: `docs/` IS IN IT, and leaving it out was the first version of the same hole.
#: The claim that every citation is a title was checked by reading the source, the
#: docstrings and the tests, all three of which were clean, while the handoff
#: document the same commit wrote cited a number twice. A claim checked over a
#: smaller set than it covers is this repository's fourth recurring defect, and
#: the answer to it is a check rather than a more careful reading.
#:
#: What the floor is FOR, now that the list is derived AND checked against a
#: second derivation: the two routes below both read git, so a git derivation that
#: answers emptily empties BOTH of them and they agree about almost nothing. That
#: is measured rather than imagined. On a pushed main the merge base this module
#: used to rest on resolves to HEAD, and every derivation here returned nothing at
#: the same moment. The floor is what that shared failure has to get past. It is
#: NOT what a narrowing of one derivation has to get past, which is what it was
#: and which made it a list that covered only what it enumerated: eight of the
#: eighteen files could be dropped silently, including the reverts file the same
#: commit created.
#:
#: AND THE FLOOR HAS A FLOOR OF ITS OWN, `_files_this_unit_puts_on_disk`, because
#: this constant could be emptied to `()` with the whole suite green. See the
#: residual titled "The cited floor can be emptied with the whole suite green, and
#: its own test then asserts nothing".
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
#:
#: THIS REPLACES A MERGE BASE, and the replacement is the whole point of this
#: round. `merge-base(origin/main, HEAD)` answers "where did this branch leave
#: main", which is a question with no answer left once the branch IS main. On a
#: pushed, clean `main` the base resolves to HEAD itself, every diff taken against
#: it is empty, and every derivation resting on it collapses to nothing while
#: reporting no error of its own. Measured on a reproduction of this unit's real
#: merge: with `origin/main` at the merge commit, FOUR tests in this module fail
#: and a fifth passes over an empty loop. That is a guard that goes red on main
#: after the merge that was supposed to land it, which is worse than a guard that
#: never existed.
#:
#: A commit subject is immutable and a merge carries it across unchanged, so the
#: same query answers the same way on the branch, on the merged tree, and on a
#: pushed main afterwards. Measured: 13 of this branch's 13 commits carry the tag
#: and none of `main`'s do.
UNIT_COMMIT_TAG = "(U34)"


def _git(*argv: str) -> str:
    """One git read, from the repository root, for the derivations below."""
    return subprocess.run(
        ["git", *argv], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout


def _unit_log(*argv: str) -> str:
    """One `git log` restricted to the commits this unit made.

    `-F` is not decoration. Without it the tag is a regular expression and its
    parentheses are a group, so `(U34)` would match a subject saying `U34` with
    no brackets at all, which is most of the prose in this repository.

    THE CALLER'S ARGUMENTS GO LAST, and that ordering is paid for. Written the
    other way round, a caller passing a pathspec put `--` before the selection
    flags, git read `-F`, `--grep` and `HEAD` as PATHS, and the filter silently
    stopped applying: the derivation then reported every residual in the document
    as one this unit had filed, including thirteen belonging to other units.
    """
    return _git("log", "--format=", "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD", *argv)


def _unit_commits() -> tuple[str, ...]:
    return tuple(_git("log", "--format=%H", "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD").split())


def _existing(named: set[str]) -> tuple[str, ...]:
    return tuple(sorted(one for one in named if (REPO_ROOT / one).is_file()))


def _files_this_unit_writes() -> tuple[str, ...]:
    """Every file this unit changes, read from git rather than kept by hand.

    THE LIST IS DERIVED, and the version it replaces was typed. Both are answers
    to the question "which files can this unit keep true", and only one of them
    stays right when the unit touches a file nobody remembered. Measured on this
    branch, the typed list named nine of seventeen, and two of the eight it missed
    carry residual citations that another unit wrote.

    IT IS DERIVED FROM THIS UNIT'S OWN COMMITS AND NOT FROM A MERGE BASE. The
    version this replaces diffed the working tree against
    `merge-base(origin/main, HEAD)`, which names the right files on a feature
    branch and names NOTHING once the branch has merged and main is pushed,
    because the base is then HEAD. `UNIT_COMMIT_TAG` says why that matters and
    what it was measured to cost. Asking the log which commits are this unit's
    gives the same 23 files on the branch and on the merged tree, measured on
    both.

    The working tree is read as well as the commits, because a file edited and not
    yet committed is a file this unit writes, and untracked files are added for
    the same reason: a mutation row that adds a document should be covered by the
    guard the moment it exists.
    """
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

    A DERIVATION CAN BE NARROWED, which is what the named floor above could not
    see: it only ever caught a narrowing that removed a file somebody had thought
    to name, so eight of this branch's eighteen files could be dropped out of the
    coverage with the suite green, and one of them was the reverts file the same
    commit added. A floor that covers what it enumerates is not a property, it is
    the identity of the files it lists.

    The two routes are composed differently on purpose. The one above asks `log`
    to list the names itself and reads the working tree with `diff` and
    `ls-files`; this one walks the unit's commits and asks `diff-tree` for each
    one separately, then asks `status` for everything the working tree has done
    since, which is a different command reading a different index and reporting
    renames with both paths. A filter added to either one shows up as a file the
    other still names.

    It is a FLOOR and not an equality. The two answers can legitimately differ by
    a file committed by this unit and then reverted in the working tree, which
    this route reports and the other does not, and coverage that is WIDER than
    required is not a defect. Narrower is.
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
    """The derived list, checked against what it must cover, minus one file.

    TWO CHECKS, and they answer different failures. The first is the property:
    every file the second route names is covered, so narrowing the derivation by
    any one of the eighteen is refused rather than by the nine somebody typed. The
    second is the floor, which is what remains when BOTH routes narrow together,
    since both rest on one merge base.

    Both are arguments rather than reads, so each one can be driven with a
    narrowing that reaches it and neither can be removed quietly.
    """
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
#:
#: THE GLOB OVER-CLAIMED AND THIS IS THE CORRECTION, not a relaxation. The bound
#: reads every ``.py`` under the package and asserts `CITED_FLOOR` names all of
#: them, on the reasoning that the package IS this unit. That was true while U34
#: was the only unit shipping into it. U27 ships the tree-coverage engine and the
#: library-statistics engine here, because the two report verbs that had no engine
#: anywhere in the tree belong beside their siblings and behind the same import
#: allowlist, and neither is a file this unit writes, keeps true, or can be held
#: to this unit's residual citations.
#:
#: LISTED RATHER THAN DERIVED FROM GIT, and that is the point rather than a
#: shortcut. Every git derivation in this module can answer emptily at once, which
#: is the single failure this bound exists to survive; a git query asking who added
#: each module would shrink the bound to nothing on exactly that failure and go
#: quiet. A typed name cannot. Its own hazard, a name added here to escape the
#: floor, is answered by the two assertions in the bound: an entry naming a file
#: the package does not hold fails, and an exclusion that empties the bound fails.
_PACKAGE_MODULES_ANOTHER_UNIT_OWNS: frozenset[str] = frozenset(
    {
        "src/cratekit/modules/reports/coverage.py",
        "src/cratekit/modules/reports/library.py",
    }
)


def _files_this_unit_puts_on_disk() -> tuple[str, ...]:
    """What `CITED_FLOOR` cannot fall below, read off the filesystem.

    THE FLOOR NEEDED A FLOOR, which is finding 2 of this unit's round ten
    verification, filed as the residual titled "The cited floor can be emptied
    with the whole suite green, and its own test then asserts nothing". `CITED_FLOOR` is the backstop for both git derivations
    narrowing together, and it could itself be emptied to `()` with the whole
    suite green, because the only test whose subject is that constant wraps its
    body in `for named in CITED_FLOOR:` and a loop over an empty tuple asserts
    nothing. Three full suite runs measured it at zero deaths. That is the exact
    shape the round's own docstring names one level up, a floor that is the
    identity of what it lists rather than a property, reproduced in the constant
    written to backstop it.

    So the floor is given a floor that is DERIVED and cannot go quiet. This reads
    the filesystem and never git, which matters because the failure `CITED_FLOOR`
    exists for is every git derivation in this module answering emptily at once.
    It cannot return nothing while this module runs at all: the package it globs
    is the package this module imports at line one, and its own path is always in
    the answer.

    IT IS THE FILES THIS UNIT OWNS BY NAME, not the files it touches. The package
    and this module are the code; the documents are the ones whose names carry the
    unit, which is a convention this unit has followed for every round. What it
    deliberately does NOT reach is the files this unit shares with others,
    `write/rbxml.py`, `tests/test_rbxml.py` and the handoff, because a floor that
    claimed those would be claiming ownership it does not have.
    """
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
#:
#: A NUMBER IS NOT AN ADDRESS, and this constant used to be twelve of them. Both
#: sides of a merge append to this one document from one counter, so the number a
#: residual is FILED under is not the number it ends up with. Numbering is APPEND
#: ONLY as of 2026-08-10, which means main's numbers never move and an incoming
#: branch's residuals take fresh numbers above main's highest. That is kinder than
#: the sequential renumber it replaces and it does not help a numeric ban list at
#: all: this branch's residuals still land somewhere other than where they were
#: filed. Measured on a reproduction of this unit's real merge, every one of the
#: twelve moved, and two tests in this module failed on the merged tree with the
#: ban list naming fifteen numbers it no longer covered.
#:
#: A TITLE DOES NOT MOVE, under either rule. Renumbering rewrites the number in a
#: heading and leaves the sentence after it alone, and appending does not touch
#: the heading at all, so these strings addressed the same twelve findings before
#: the merge and after it. They are resolved to whatever numbers the document
#: gives them TODAY, in `_banned_addresses`, so the guard is correct under both
#: numbering rules without knowing which one is in force.
#:
#: TYPED HERE AND DERIVED FROM GIT IN `_residual_titles_this_unit_filed`, and the
#: two hold each other in both directions. Emptying this tuple is refused by the
#: derivation, and a derivation that stops matching is refused by this tuple.
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
#:
#: The typed tuple and the derived one refuse each other's narrowing, so each
#: catches the other. Neither catches both emptying together, and that is not a
#: hypothetical here: on a pushed main every git derivation in this module
#: returned nothing at the same moment, for one shared reason. A unit only ever
#: files MORE residuals, so a lower bound is the one claim about this number that
#: cannot go stale in the direction that would hide something.
RESIDUALS_FILED_FLOOR = 12

_CITATION = re.compile(r"\bR-(\d+)\b")

#: A residual heading as the DOCUMENT writes it: the number it carries today, and
#: the title, which is the part that survives a renumber.
_DOCUMENT_HEADING = re.compile(r"^## R-(\d+)\. (.+?)[ \t]*$", re.MULTILINE)

#: The same heading as a DIFF writes it when a commit adds one, which is what
#: says the finding was FILED rather than merely mentioned.
_FILED_HEADING = re.compile(r"^\+## R-(\d+)\. (.+?)[ \t]*$", re.MULTILINE)


def _residual_titles_this_unit_filed() -> tuple[str, ...]:
    """Every residual heading this unit's own commits added, by title.

    The commits are read rather than a diff against a base, because the file holds
    every unit's residuals and the question here is which ones are THIS UNIT'S to
    keep citable by title. A heading somebody else wrote is somebody else's
    address, and banning it would be a guard the next author deletes.

    THE TITLE IS TAKEN AND THE NUMBER IS DISCARDED. The number in a commit's diff
    is the number the residual had WHEN IT WAS FILED, and the merge is exactly the
    event that makes that number wrong, whether the document renumbers or appends.
    The title in that same diff is the title it still has. Reading the stable half
    of a heading out of an immutable commit is what makes this derivation give the
    same twelve answers on the branch and on the merged tree, measured on both.
    """
    diff = _unit_log("-p", "--", RESIDUAL_FINDINGS_NAME)
    return tuple(dict.fromkeys(title for _, title in _FILED_HEADING.findall(diff)))


def _residual_numbers_by_title(text: str | None = None) -> dict[str, str]:
    """What the residual document calls each finding TODAY.

    The file is read rather than a diff, because the number is the part that moves
    and the current file is the only thing that says where it moved to.

    A title carried by two headings is REFUSED rather than resolved. An ambiguous
    address is not an address, and silently taking the first would ban one finding
    while leaving the other citable by a number nothing checks.
    """
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
    """Today's numbers for this unit's residuals, resolved from their titles.

    Four failures, and each one is a way this guard has already been wrong or
    could quietly become wrong.

    TOO FEW FILED. Both inputs can narrow, and they refuse each other, so what is
    left is both narrowing at once. `RESIDUALS_FILED_FLOOR` is what that has to
    get past, and it is checked first because it is the only one of the four that
    is not vacuous when everything else is empty.

    UNCOVERED. A residual this unit filed whose title is not typed in
    `UNIT_RESIDUAL_TITLES` is an address a citation could use with nothing left to
    catch it. The numeric range this replaces could not express this check at all
    after a renumber, since every number in it had moved.

    INVENTED. A title typed here that this unit never filed bans somebody else's
    address, which is a guard the next author deletes rather than a guard that
    holds.

    UNRESOLVED. A title that no longer appears in the document is a residual that
    was renamed or deleted. It has to be REFUSED rather than dropped: a ban list
    that quietly shrinks when the document moves under it is the failure this
    whole block exists to answer, one indirection along.
    """
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
    assert unresolved == [], f"a residual this unit filed no longer answers to its title: {unresolved}"
    return tuple(f"R-{numbers[one]}" for one in titles)

#: The ONE passage whose subject is the numbers themselves, delimited rather than
#: guessed at. A statement that says which numbers collide has to spell them, and
#: an exemption that is a pair of markers can be grepped, cannot widen by accident,
#: and shows up in a diff when somebody moves it.
_COLLISION_OPEN = "[[collision-set]]"
_COLLISION_CLOSE = "[[/collision-set]]"


def _is_delimiter(line: str, marker: str) -> bool:
    """Whether one line IS a marker rather than merely containing one.

    A marker is a line of its own, optionally commented. That distinction is
    load-bearing rather than tidiness: the mutation row that reverts a citation
    back to a number carries the closing marker as DATA, inside a string, and a
    substring test would read that as a second delimiter and lose count.
    """
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
    """The citation rule, measured over `docs/` too rather than asserted about it.

    Only THIS UNIT'S numbers are banned, and only in the files this unit writes.
    A citation of the residual titled "Four routing verbs name a CLI module no
    unit's file list declares", written by another unit before this branch
    existed, is
    somebody else's address to keep stable, and a guard that failed on it would be
    a guard somebody deletes.

    The addresses are TITLES resolved to today's numbers, never a typed range, so
    the ban list is the same twelve findings before a renumber and after one.
    """
    banned = set(
        _banned_addresses(UNIT_RESIDUAL_TITLES, filed=_residual_titles_this_unit_filed())
    )
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
    """The property, over the derived list rather than over a typed subset.

    The check this replaces was a floor of nine names, so eight of the eighteen
    files this branch writes could be dropped out of the coverage in silence,
    including the reverts file the same commit created. Every file the second
    route names is dropped here, one at a time, and every one of them has to be
    refused. A floor cannot pass this: it would only refuse the nine.
    """
    written = _files_this_unit_writes()
    expected = _files_this_unit_writes_by_a_second_route()
    assert set(expected) <= set(written), sorted(set(expected) - set(written))
    assert len(expected) > len(CITED_FLOOR), "the two would be indistinguishable"
    for dropped in expected:
        narrowed = tuple(one for one in written if one != dropped)
        with pytest.raises(AssertionError):
            _covered_files(narrowed, expected=expected)


def test_the_named_floor_still_bites_when_both_derivations_narrow_together():
    """What the floor is for, driven, because both routes rest on one git.

    A git derivation that answers emptily narrows both routes at once, and the
    property above compares them to each other, so it would agree with itself
    about a coverage list holding almost nothing. Each named file is dropped from
    BOTH sides here and the floor has to refuse anyway.

    THE LOOP IS GIVEN A BOUND IT CANNOT SATISFY VACUOUSLY, which closes finding 2
    of the round ten verification, filed as the residual titled "The cited floor
    can be emptied with the whole suite green, and its own test then asserts
    nothing". The body of this test was the loop
    alone, so emptying `CITED_FLOOR` to `()` left it iterating over nothing and
    passing while asserting nothing, measured at zero deaths over three full suite
    runs. The bound is `_files_this_unit_puts_on_disk`, which reads the filesystem
    and never git, so the one failure `CITED_FLOOR` exists for cannot empty the
    check on `CITED_FLOOR` at the same time.
    """
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
    """The ban list, pinned to what this unit filed rather than to a typed range.

    The assertion this replaces held a numeric range at both edges against the
    residual numbers a merge base diff reported. Both halves of that broke on the
    real merge: the range stopped describing anything after the renumber, and the
    diff went empty once `origin/main` reached HEAD. Titles are checked here
    instead, in both directions, and NOTHING ELSE IS BANNED, because a ban list
    that reaches another unit's address is a guard the next author deletes.
    """
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
    """A title that stops resolving goes RED rather than banning a smaller set.

    This is the failure a title-keyed ban list has that a numeric one did not: a
    number is either in the range or out of it, while a title can simply stop
    being in the document, and a lookup that skips what it cannot find would go on
    passing over a ban list quietly missing an address. Every one of this unit's
    residuals is renamed in a copy of the document here, one at a time, and every
    one has to be refused by name.
    """
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
    """Every address moved, applied to the document and driven.

    This is the defect that blocked the merge, held open so it cannot come back.
    The ban list is rebuilt against a copy of the document in which every residual
    carries a different number, and it has to name the twelve findings it named
    before, at their new addresses. A typed range cannot pass this at all, which
    is the point: the old constant failed on the real merged tree with fifteen
    numbers it no longer covered.

    A SHIFT IS THE WORST CASE AND IT IS DRIVEN DELIBERATELY. Numbering became
    APPEND ONLY on 2026-08-10, so main's numbers now hold still and only the
    incoming branch's move. Driving the harder rule here rather than the current
    one means the guard does not have to be revisited if the decision moves again,
    and a guard that survives every number changing survives some of them changing.
    """
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
    """The exemption's own guard, because an unmeasured exemption is the same hole.

    Exactly two passages, in two named files, are allowed to spell this unit's
    numbers: the statement that says WHICH numbers collide, and the one mutation
    row that reverts a citation back to a number and therefore has to record it.
    Both are subjects rather than uses. A marker left open would exempt everything
    after it to the end of the file, so both markers are required, in order, once
    each, and no other covered file may carry either.

    THIS MODULE IS CHECKED LIKE EVERY OTHER, and exempting it was the hole inside
    the guard's own blind spot. It was skipped here on the grounds that it DEFINES
    the markers, which is true and does not follow: the definitions are
    assignments and are not delimiter lines, while ``_citing_lines`` honours a
    delimiter found in this file exactly as it honours one anywhere else. Measured,
    an unclosed open marker plus a bare citation left both guards green, which is
    the failure mode the pair exists to catch, in the one file the pair was told
    not to look at.

    Every covered file is asked the same question and the answer is a COUNT rather
    than a presence, so a stray CLOSE marker is caught as well as a stray open.
    """
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
    """The two halves of the sibling hole, asserted together because they are one.

    The walk covers the package DIRECTORY, so a file beside it is not scanned for
    a mutation, and that is correct: a module the package cannot reach cannot
    write anything on its behalf. What makes it correct is the second half. If
    the allowlist accepted a bare prefix, ``cratekit.modules.reports_ledger``
    would be both unreachable by the walk and importable by the package, and the
    pair of holes is what the countdown against this unit forbids by name.
    """
    assert all(name.startswith(f"{REPORTS_PACKAGE}.") or name == REPORTS_PACKAGE
               for name, _ in _report_modules())
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
    """Every module in THIS repository that the allowlist admits.

    Walked from the allowlist rather than listed (P3). A module added to the
    allowlist in a future diff is audited by the test below without anybody
    remembering to add it here, which is the property a hand-listed copy loses
    on its first edit.

    A PACKAGE ENTRY RESOLVES TO EVERY MODULE UNDER IT, and keeping only the
    entries that resolved to a ``.py`` file made that promise false in the one
    direction that matters. ``_permitted`` admits every dotted child of an
    allowlisted entry, so adding ``cratekit.core`` to the list would admit
    ``cratekit.core.rb_writer``, and an audit that kept only files would walk
    past the whole package and report nothing. Absence read as evidence of
    absence, aimed at the auditor.

    ``entries`` is a parameter so the resolution itself can be driven, since the
    allowlist has no package entry today and a rule nothing exercises is the
    shape this suite exists to remove. ``root`` is one for the same reason: the
    closure below is driven over a planted tree, and a planted tree is not here.
    """
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
    """The file one resolved first party import executes, or None.

    ``_resolved_imports`` spells ``from X import y`` as ``X.y`` whenever X is a
    package, and ``y`` may be a module or only a name X's initializer binds. So
    the target itself is tried first, and the package's initializer only when it
    BINDS that name. Falling back to the parent unconditionally made
    ``import cratekit.core.probe_generated``, with no file behind it, land on
    ``cratekit/core/__init__.py`` and read as followed, which the built in review
    drove on a planted tree. A star import in the initializer binds nothing this
    can read, so it stays unfollowed and is reported.
    """
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
    """Every ``importlib.import_module`` in ``source``, as a target or as unreadable.

    ``_resolved_imports`` reads the statement and the ``__import__`` builtin, and
    this is the third spelling, which the report side never needed because
    ``importlib`` is not on the allowlist. A module in the closure is held to no
    allowlist, so ``importlib.import_module("cratekit.core.access_probe")`` in
    ``cause`` was the one hop delegation with no import statement for the closure to
    follow, driven by the built in review and green.

    The call is matched on any receiver's ``import_module`` and on a bare name
    ``from importlib import import_module`` bound, alias included. A literal
    absolute name is a target. Anything else, a computed name or a relative one
    whose package this does not resolve, is unreadable and is reported as such.
    """
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
            first.value
            if isinstance(first, ast.Constant) and isinstance(first.value, str)
            else ""
        )
        found.append(literal if literal and not literal.startswith(".") else _COMPUTED_IMPORT)
    return found


def _admitted_closure(
    entries=ALLOWED_IMPORTS, root: Path = SRC_ROOT
) -> tuple[list[tuple[str, Path]], list[str]]:
    """Every first party module the allowlist admits OR REACHES, and what it could not follow.

    The residual "The reports allowlist audit is one hop deep". The audit read
    the admitted modules and nothing they import, and
    nothing constrains what an admitted module may import, so a thin caller in
    ``cause`` could hand the actual write to a module the list does not name and
    the audit would read the caller as ordinary code. An admitted module's
    imports are its attributes, which makes them reachable from the reports
    package whatever the allowlist says.

    ONE PASS, A WORKLIST, rather than a layer per run: each module is read once,
    what it imports is queued if it has not been seen, and a cycle ends because
    a seen module is never queued again. Imports are read through
    ``_resolved_imports``, so an alias, a relative import and a literal
    ``__import__`` are followed the way the report side reads them, and through
    ``_import_module_calls``, which is the spelling only the closure needs.

    WHAT CANNOT BE FOLLOWED IS RETURNED, NOT DROPPED. A computed ``__import__``
    and a first party target with no file behind it are modules the audit cannot
    read, and a closure that skipped them would be absence read as evidence of
    absence one more time. Implicit parent package initializers are NOT followed:
    importing ``cratekit.cli.output`` runs ``cratekit/cli/__init__.py``, which is
    import time behaviour rather than a callable the package can reach, and
    following it would pull the whole command line in.
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
    """The audit's loop, named once so a planted closure runs the same one.

    ``SANCTIONED_PERSISTENCE`` is exempt as ITSELF and not as a door: what it
    imports is in the closure and is audited like anything else.
    """
    unnamed: dict[str, list[str]] = {}
    for dotted, path in audited:
        if dotted == SANCTIONED_PERSISTENCE:
            continue
        found = _unnamed_writers(dotted, path.read_text())
        if found:
            unnamed[dotted] = found
    return unnamed


def _unnamed_writers(dotted: str, source: str) -> list[str]:
    """The writers in one admitted module that this guard's sets cannot name.

    The body of the audit, split out so a planted module can drive it. The audit
    itself walks only the real allowlist, and every branch in here is a branch
    the real modules do not currently take, which is how three of them came to be
    held up by nothing at all.

    THE MODULE'S OWN BINDINGS ARE READ FIRST and handed down, because a function
    read on its own carries no import statement. Without them an admitted module
    reaching ANOTHER admitted module's writer, ``naming`` calling
    ``config.save``, was invisible to the audit while being exactly the shape the
    audit exists for. No module on the allowlist does that today, which is why it
    is driven by a fixture rather than found by the walk.
    """
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
            named = node.name in FILESYSTEM_MUTATIONS or f"{short}.{node.name}" in QUALIFIED_MUTATIONS
            # A CLASS IS ITS OWN OWNER here, because the audit reads one top
            # level statement at a time and there is no walk above it to say so.
            # Without it every method's ``self`` renders unqualified and the
            # class body's attributes are keyed under nothing. It is keyed by
            # DEFINITION SITE rather than by name, which is what the binding
            # table above is keyed by, and deriving both from the node is what
            # keeps the two from drifting.
            owner = (
                _class_key(node)
                if isinstance(node, ast.ClassDef)
                else attached.get(node.name, "")
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
                    _Instance()
                    if isinstance(node, ast.ClassDef)
                    else _method_instance(node, owner)
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
    """The allowlist's ARGUMENT, checked instead of asserted.

    The comment above ``ALLOWED_IMPORTS`` says the list is the argument: nothing
    admitted can open a database, spawn a process, or touch a file except through
    ``pathlib``, whose write methods are forbidden separately. That sentence was
    false, and nothing in the suite could see it, which is the exact shape this
    repository keeps producing: a guard whose docstring calls it the answer while
    nothing exercises the claim.

    ``cratekit.core.config`` exposes ``save``, ``load_from_path``,
    ``atomic_write_bytes``, ``_mkdir_private`` and an ``_exclusive_lock`` that
    chmods; ``cratekit.core.naming``, which ``duplicates`` imports already,
    exposes ``claim_target``, which opens a file. A report module calling any of
    them wrote a file with no forbidden import and no forbidden call name
    anywhere in it.

    So the rule is: every reachable entry point of an admitted module that can
    change a file must itself be a name ``FILESYSTEM_MUTATIONS`` or
    ``QUALIFIED_MUTATIONS`` carries, and the only exemption is the one module R12
    licenses to persist. There are two ways to answer a failure and both are
    correct: name the writer in the set, or take the module off the allowlist.
    What is not available is leaving the argument written down and untrue.

    THE WALK IS THE CLOSURE, not the list. An admitted module that
    delegates its write to a module the list does not name is still reachable
    from the package, and the modules named below past the first five are the
    ones only the closure reaches. A walk that collapsed back to one hop would
    drop them, and this floor is what says so.
    """
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
#:
#: WHAT SEPARATES THEM FROM THE FOUR WRITERS ABOVE is not that their attribute
#: name is readable, because it is not. It is that they do not CALL what they got
#: back. Every one of the four ends in a return or a comparison, and every writer
#: above puts a call straight onto the result. That is the switch round four
#: moved to, and it is why the writers can be caught without the readers crying
#: wolf. Verified against the real modules: ``config``, ``naming`` and
#: ``taxonomy`` between them spell six reflective reads and not one of them calls
#: its result.
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
    """The door the reflection switch opened, driven end to end.

    With the literal half gated off, ``stash`` is invisible to the audit and is
    therefore never forced into ``FILESYSTEM_MUTATIONS``. That is the whole
    evasion: the report that calls it needs no forbidden import, no mutating
    attribute and no reflection of its own.
    """
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
    """The relocation, closed at the place it kept moving to.

    Round two gated the whole of rule 4 behind the reflection switch and lost
    ``getattr(path, "write_text")(data)``. Round three ungated the literal half
    and lost ``getattr(path, "write_" + "text")(data)``, which is the same
    wrapper one token longer, plus the module-constant and f-string spellings of
    it. Each fix was a real fix and each left the identical helper unnamed, which
    is what a fix round fails at: relocating a hole rather than closing it.

    The switch is now on the RESULT BEING CALLED. All five of these put a call
    straight onto what they reached, and a call to a method this checker cannot
    name, inside a module the reports package may import, is a writer nothing can
    be made to name. The reads the switch exists for are the test below.
    """
    assert _unnamed_writers("cratekit.core.naming", source) == ["stash"]


@pytest.mark.parametrize(
    "source",
    [
        ADMITTED_MODULE_REACHING_ANOTHER_MODULES_WRITER,
        ADMITTED_MODULE_IMPORTING_ANOTHER_MODULES_WRITER,
    ],
)
def test_the_audit_reads_the_imports_of_the_module_it_is_auditing(source):
    """The binding table the audit had no way to see.

    ``_unnamed_writers`` walks one top-level statement at a time, so a function
    handed over on its own carries no import with it and ``config`` inside it was
    an unresolvable name. A one-line helper in ``naming`` calling ``config.save``
    was therefore invisible to the audit, never forced into the mutation set, and
    reachable from a report through a module the allowlist admits. The module's
    own bindings are now read once and handed down, in both the shape that
    reaches the writer through its module and the shape that imports it by name.
    """
    assert _unnamed_writers("cratekit.core.naming", source) == ["refresh"]


def test_the_audit_stays_quiet_on_the_reflective_reads_it_was_loosened_for():
    """The other direction, and the reason only ONE half is gated.

    ``config._to_toml_value``, ``naming._field_value``, ``naming._render_markers``
    and ``taxonomy._build_suggest`` are pure attribute reads, and an audit that
    called them writers is an audit somebody switches off. The same source is a
    finding for ``filesystem_mutations``, which is correct: inside a package that
    has promised not to write, an attribute this checker cannot read is a
    violation, and everywhere else it is ordinary code.
    """
    assert _unnamed_writers("cratekit.core.naming", ADMITTED_REFLECTIVE_READER) == []
    assert filesystem_mutations(ADMITTED_REFLECTIVE_READER)


def test_the_audit_refuses_a_module_that_writes_when_it_is_imported():
    """The ``loose`` branch, which no admitted module takes today.

    A write at module level has no entry point to name, so naming it in the
    mutation set is not one of the two available answers: the only answer is to
    drop the module. The branch was written for that and was held up by nothing
    until this drove it.
    """
    found = _unnamed_writers("cratekit.core.planted", ADMITTED_MODULE_LEVEL_WRITE)
    assert len(found) == 1
    assert found[0].startswith("<at import time>")
    assert "write_text" in found[0]


def test_the_audit_does_not_call_an_ordinary_attribute_read_a_writer():
    """P7 inside the audit itself, which is where the over-restriction landed.

    ``load`` and ``save`` are ordinary names on anything, and while they sat bare
    in the mutation set this module failed the audit for returning an attribute.
    Nothing in the tree spells it today, which is the only reason the suite was
    green, and a guard that fails correct code is one somebody routes around.
    """
    assert _unnamed_writers("cratekit.core.planted", ADMITTED_GENERIC_ATTRIBUTE_READ) == []


def test_the_audit_reads_a_modules_own_bare_call_as_qualified_by_that_module():
    """The half of the receiver rule that has no receiver to read.

    Inside ``config.py`` a call to ``load`` spells no module, and it is still
    ``config.load``. Without that, making the generic names receiver qualified
    would have quietly stopped the audit seeing a new entry point that reaches a
    writer through a private wrapper, which is a fix for over-restriction turning
    into a hole. The same source is silent for a module that does not own the
    name, because there it really is an ordinary call.
    """
    assert _unnamed_writers(
        "cratekit.core.config", ADMITTED_MODULE_REACHING_ITS_OWN_WRITER
    ) == ["refresh"]
    assert _unnamed_writers(
        "cratekit.core.taxonomy", ADMITTED_MODULE_REACHING_ITS_OWN_WRITER
    ) == []


def test_a_package_on_the_allowlist_audits_every_module_underneath_it():
    """The allowlist entry shape the audit used to walk straight past.

    ``_permitted`` admits every dotted child of an allowlisted entry, so
    ``cratekit.core`` on the list admits ``cratekit.core.rb_writer``, which opens
    the rekordbox database. Keeping only entries that resolved to a ``.py`` file
    meant the audit walked ZERO modules for that entry and reported nothing,
    which reads exactly like a pass.
    """
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
    """The one hop audit's hole, driven on a planted tree rather than argued.

    Each tree is one an ordinary tidy up produces: a write moved out of an
    admitted module into a new one beside it. The ONE HOP walk is asserted to
    miss it first, because a closure test that passes on a tree the old walk
    also caught would be proving nothing about the hole. Then the closure is
    asserted to reach every planted module and the audit's own loop to report
    exactly the writer.
    """
    root = _plant(tmp_path, modules)
    one_hop = _admitted_repository_modules(entries, root)
    assert _unnamed_writers_in(one_hop) == {}

    audited, unfollowed = _admitted_closure(entries, root)
    assert unfollowed == []
    assert {dotted for dotted, _ in audited} == set(modules)
    assert _unnamed_writers_in(audited) == reported


def test_the_closure_reports_an_import_it_cannot_follow(tmp_path):
    """A module the closure cannot read is reported, never skipped.

    A computed ``__import__`` names nothing this can open, and a first party
    target with no file behind it is either a typo or a module made at run time.
    Either way the audit cannot name its writers, and treating it as clean is the
    shape this file keeps finding.
    """
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
    """``from cratekit.core import thing`` where ``thing`` is not a module.

    ``_resolved_imports`` spells it ``cratekit.core.thing`` either way, so the
    closure falls back to the package's initializer exactly once, and a target
    whose parent is not a module either stays unfollowed rather than climbing to
    ``cratekit/__init__.py`` and reading as followed.
    """
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
#:
#: Read from disk rather than pasted, because a pasted copy is a fixture again
#: and the whole point of these two lists is that they were found against the
#: module rather than against a fiction of it.
AGING_SOURCE = (REPORTS_ROOT / "aging.py").read_text()

#: Ten shapes an ORDINARY AUTHOR writes, each appended to the real ``aging`` and
#: each a finding before this round. The defect they share is one defect: the
#: binding table was swept FLAT off the whole file and only a PARAMETER could
#: take a name back, so every other way of rebinding a name left the stale import
#: binding live underneath it.
#:
#: The last one is the worst of them, and it is the most common spelling of the
#: assignment it turns on. ``self.config = config`` inside ``def __init__(self,
#: config)`` is constructor injection. Read flat, the right hand side was the
#: MODULE, so ``self.config`` was bound to the library for the whole file and
#: every ``self.config.load`` in every other method was a write.
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
    "shape,snippet", ORDINARY_SHAPES_IN_A_REPORT, ids=[one[0] for one in ORDINARY_SHAPES_IN_A_REPORT]
)
def test_an_ordinary_rebinding_in_a_real_report_is_not_a_write(shape, snippet):
    """The ten false positives, driven against the module they were found in.

    Every one of these is two or three lines somebody adds to ``aging`` without
    thinking about a guard, and every one of them failed
    ``test_no_report_module_calls_a_filesystem_mutation`` before the binding table
    had scope. The tree was green the whole time, and reading that zero as safety
    is the mistake: it was green because no governed module had yet been written
    in any of these ten shapes, not because the guard could tell them apart.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


@pytest.mark.parametrize(
    "shape,snippet", MISSED_WRITES_IN_A_REPORT, ids=[one[0] for one in MISSED_WRITES_IN_A_REPORT]
)
def test_a_write_through_an_unread_binding_shape_is_still_a_write(shape, snippet):
    """The other direction of the same defect, and the one that costs a file.

    The unpacking branch it replaces never fired for the shape it looked like it
    handled. It asked whether the WHOLE right hand side was a module, which for
    ``alias, other = config, 1`` is a tuple and is not, and then indexed each
    TARGET by position to invent ``alias[0]``. Reverting the branch outright
    killed nothing, which is the measurement that found it.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet", ORDINARY_MAPPING_LOOKUPS, ids=[one[0] for one in ORDINARY_MAPPING_LOOKUPS]
)
def test_a_mapping_keyed_on_a_filesystem_verb_is_not_a_write(shape, snippet):
    """Rule 5 with its receiver, against the module the rule would have fired in.

    ``counts["rename"] + counts["unlink"]`` was two findings, not one, which is
    what a rule with no receiver does to code that reads a counter twice.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_the_dunder_that_forwards_its_own_name_is_not_a_write():
    """The collateral rule 4's own comment said naming the dunder did not have.

    Nothing in ``src`` spells ``__getattribute__``, so the suite was green and
    the claim survived being written. The rule is what changed rather than the
    claim: for a COMPUTED name the dunder is read on whether its result is
    called, which still catches ``object.__getattribute__(p, n)(d)`` and leaves
    the delegation alone.
    """
    assert filesystem_mutations(AGING_SOURCE + ORDINARY_DUNDER_DELEGATION) == []
    assert filesystem_mutations(
        "def stash(p, n, d):\n    object.__getattribute__(p, n)(d)\n"
    )


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
    """The three parameter kinds the shadow list carries and nothing drove.

    ``def go(*, config)`` is ordinary keyword-only injection and the other two are
    the catch-alls beside it. Each is a name the enclosing file may also import,
    and a parameter list that only shadowed its plain arguments would report the
    body of every one of them.
    """
    assert filesystem_mutations(
        "from cratekit.core import config\n\n\n" + source
    ) == []


def test_a_receiver_key_is_only_rendered_for_a_call_that_takes_nothing():
    """Both halves of the condition that decides whether a call has one answer.

    ``_mod()`` resolves to whatever ``_mod`` returns, always. ``Path(p)`` and
    ``_mod(fallback=cfg)`` resolve to whatever they were HANDED, and a keyword
    argument is an argument. Rendering a key for either would make two different
    expressions share one binding, which is this repository's second recurring
    defect aimed at the table itself.
    """
    bare = ast.parse("_mod()").body[0].value
    positional = ast.parse("_mod(cfg)").body[0].value
    keyword = ast.parse("_mod(fallback=cfg)").body[0].value
    assert _receiver_key(bare) == "_mod()"
    assert _receiver_key(positional) == ""
    assert _receiver_key(keyword) == ""


def test_a_container_key_this_cannot_read_binds_nothing():
    """The constant-key condition, which a dict with a computed key drives.

    A key that is a name has no spelling a subscript receiver could be matched
    against, and asking an ``ast.Name`` for the ``.value`` a constant has is not
    a wrong answer, it is an exception. The constant-keyed sibling is asserted
    beside it so this is a statement about the CONDITION rather than about
    dictionaries.
    """
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
    """The switch, decided on the binding table rather than on local syntax.

    Round two lost the four token wrapper, round three lost it one TOKEN longer,
    and round four lost it one LINE longer: it stated that a reflective read whose
    result is called is a writer nothing can be made to name, and then decided
    "is it called" by looking at one expression. Bind it and call the name, return
    it and call the result, store it in a container and call the element, use it
    as a decorator: eight wrappers, none of them exotic, all of them invisible.
    """
    assert _unnamed_writers("cratekit.core.naming", source) == ["stash"], shape


def test_the_audit_stays_quiet_on_a_reflective_read_nothing_calls():
    """The other side of the switch, which is why only one half is gated.

    ``config``, ``naming`` and ``taxonomy`` between them spell six reflective
    reads and not one of them calls its result. An audit that called them writers
    is an audit somebody switches off, and the binding table has to be able to
    say NO as well as yes or it is just the reflection switch again.
    """
    assert _unnamed_writers("cratekit.core.naming", ADMITTED_REFLECTIVE_READER) == []
    assert (
        _unnamed_writers(
            "cratekit.core.naming",
            "def declared(spec, flag, names):\n    return getattr(spec, flag) and flag not in names\n",
        )
        == []
    )


def test_a_module_level_open_does_not_have_its_file_read_as_its_mode():
    """Finding 8, and the one live example of it in the tree.

    ``cratekit/core/jobs.py`` line 788 opens a DIRECTORY read only so it can
    fsync it, which is a pure read, and the audit called ``_fsync_directory`` a
    writer. ``jobs`` is not on the allowlist today, so nothing failed, which is
    exactly how it would still be there the day the allowlist widened.

    The writing spellings are asserted beside it, because a rule that stopped
    reporting every module level ``open`` would pass the first assertion on its
    own.
    """
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
    """The one asymmetry in the table, asserted rather than described.

    A NAME is lexical: bound in a scope, visible in that scope and the scopes
    inside it, taken back by anything that rebinds it. An OBJECT key is not, and
    cannot be, because ``self.mod`` is set in a constructor and read in a sibling
    method. What keeps that safe is that the object binding is only created when
    its right hand side resolves in the scope doing the assigning, so the miss
    direction survives and the false positive does not.
    """
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
#:
#: ``Injected.go`` reads the constructor argument it was handed and touches
#: nothing else. ``Holder`` really does bind the module. Keyed on ``self.config``
#: with no owning class, one binding decided for both and the ordinary method was
#: a write to the library. That is this repository's second recurring defect,
#: identity that is not unique, aimed at the round's own binding table.
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
    """Both directions of the qualified key, in one file, against the real module.

    The write must still be found and the ordinary read must not be reported, and
    asserting only the first would pass on a table that answered "everything is a
    write". Reverting the class out of the key makes the second assertion fail.
    """
    found = filesystem_mutations(AGING_SOURCE + TWO_SELVES_IN_ONE_FILE)
    assert [one for one in found if "config.load" in one] == [], found
    assert [one for one in found if "config.save" in one], found


def test_the_instance_is_the_first_parameter_rather_than_the_word_self():
    """``self`` is a convention, and a key keyed on a convention is one rename out.

    A class that spells the instance ``this`` in one method and ``self`` in
    another has ONE object, so both render the same root. A ``staticmethod`` has
    no instance at all even when its first parameter is called ``self``, and a
    ``classmethod``'s first parameter is the class rather than an instance of it.
    """
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
    """The evasion the round already caught one line lower, closed at its own line.

    ``self.mod = config`` in ``__init__`` fired. ``mod = config`` in the class
    body did not, and the two are the same assignment written one indent apart.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    CLASS_BODY_STAYS_IN_THE_CLASS,
    ids=[one[0] for one in CLASS_BODY_STAYS_IN_THE_CLASS],
)
def test_a_class_body_binds_for_its_class_and_for_nothing_else(shape, snippet):
    """A class body is a scope, and the false positive direction says so.

    A name bound in a class body is reached through the class or through an
    instance and never bare, so reading it as a plain binding of the scope around
    it is both a false positive here and, when the name collides with an imported
    module, a shadow that loses a real write one scope out.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_a_method_that_hands_back_a_module_is_keyed_under_its_class():
    """``_mod()`` is a fact about ONE function, and a method is not that function.

    Keyed as ``_mod()`` with no class, a method returning the module and a module
    level function of the same name are one binding, so ``_mod().load`` written
    beside the class was a write to the library. Both directions are asserted,
    because a key that resolved nothing would pass the second on its own.
    """
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
    """The shadow the old reading had, which was the quiet half of the same defect.

    ``class Keeper: config = 1`` read as a module level assignment took the name
    ``config`` back for the whole file, so a real ``config.save(cfg)`` written
    after it was no longer a write to the library. It is stated here as a WRITE
    that must still be found rather than as a cost in a comment.
    """
    shadowed = "\n\nclass Keeper:\n    config = 1\n\n\ndef go(cfg):\n    config.save(cfg)\n"
    assert filesystem_mutations(AGING_SOURCE + shadowed)


def test_the_audit_names_a_class_that_reaches_a_writer_through_its_body():
    """The same two lines through the allowlist audit, which reads one class at a time.

    The audit has no walk above the statement it is reading, so the class has to
    name itself as the owner or every method's ``self`` renders unqualified.
    """
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
#:
#: The round before caught the shape one indent in, ``self.mod = config`` in a
#: constructor and ``mod = config`` in a class body, and keyed both under the
#: class that wrote the line. Python does not look an attribute up that way. A
#: subclass sees what its bases bound, and a base's method is handed a subclass
#: as its ``self``, so the key has to be resolved through the family rather than
#: parked on one member of it.
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
    """The key resolved through the family rather than parked on one member of it.

    The round before this one had the right diagnosis for the wrong object twice
    over and paid for it here: ``self.mod = config`` in ``Base.__init__`` created
    a key under ``Base``, and ``Row(Base)`` reading the same attribute looked up
    a key under ``Row`` that nothing had ever written. A mixin is the same hole
    read the other way round, and a method attached by ``Row.go = _go`` is the
    same hole with the class and the method in two different statements.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    INHERITANCE_STAYS_IN_THE_FAMILY,
    ids=[one[0] for one in INHERITANCE_STAYS_IN_THE_FAMILY],
)
def test_a_class_key_names_one_class_and_never_two(shape, snippet):
    """The false positives a coarser key produces, which are ordinary code.

    A family read as one connected component hands ``Holder``'s binding to
    ``Injected`` through the base they share, which is the ``self.config``
    collision this file already has a test for, one level out. A class keyed by
    its NAME does the same to two factories that each return a ``Keeper`` and to
    a module that defines the name twice, and it leaves a parameter of that name
    unable to take it back, because a name is only shadowed while it is a name.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


#: SIX ORDINARY SHAPES, every one of them a subclass overriding an attribute its
#: base binds, and every one of them reported as a write to the library by the
#: round that added inheritance. Not one is evasion. Overriding an inherited
#: attribute in a constructor is the most ordinary thing inheritance does.
#:
#: The hole is one line wide and the fix already existed thirty lines away.
#: ``_scope_own_bindings`` records a FAILED ATTEMPT for a NAME an assignment took
#: and could not resolve, because binding nothing and taking the name back are two
#: different facts and silence cannot tell them apart. The OBJECT half of the same
#: table recorded silence, so ``self.mod = dict(raw)`` in ``Row.__init__`` left no
#: key under ``Row`` at all and ``_carry`` filled the gap from ``Base``.
#:
#: The direction matters and is measured both ways below: an override blocks
#: UPWARD, where a nearer class really does stand between the reader and the
#: farther one, and never DOWNWARD, where a mixin's ``self`` is as likely to be
#: some other subclass.
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
    """The false positive direction of the table the round before rebuilt.

    Six shapes, each two or three lines appended to the real ``aging``, each one
    reported as ``config.save`` on code that binds a dict, a ``None`` or a
    constructor argument. Reverting the failed attempt rule out of the object half
    of ``_scope_own_bindings`` makes every one of them fire again.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape
    assert _unnamed_writers(REPORTS_PACKAGE + ".aging", AGING_SOURCE + snippet) == [], shape


@pytest.mark.parametrize(
    "shape,snippet",
    AN_OVERRIDE_BLOCKS_NOTHING_ELSE,
    ids=[one[0] for one in AN_OVERRIDE_BLOCKS_NOTHING_ELSE],
)
def test_an_override_blocks_upward_and_never_sideways_or_down(shape, snippet):
    """The miss direction of the same rule, asserted rather than reasoned about.

    A rule that let an unresolved key travel DOWN would take the mixin with it:
    ``Injected`` and ``Holder`` are two subclasses of one writer mixin, and the
    one that binds the real module still has to be reached through it. A rule that
    let the FIRST binding a walk happened to see decide would make the answer
    depend on the order two methods are written in, which is why the same class
    binding the attribute twice is driven in both orders.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


#: AN OVERRIDE ONE INDENT IN, which is the same false positive as the six above
#: with a branch around it, and which the branch rule put back for six rounds
#: because the rule's scope was stated in PROSE and driven on the NAME half only.
#:
#: Every one of these is a subclass overriding an attribute its base sets in
#: ``__init__``, without calling that ``__init__``. Executed with a stand-in
#: ``config``, every input to every one of them gives ``self.mod is config`` False
#: and an ``AttributeError`` from ``go``, on the arm that overrode and on the arm
#: that did not: the override wins where it ran, and where it did not run the
#: attribute was never created, because ``class Base`` binds nothing by itself.
#: The write is unreachable on all paths and reporting it is a false positive on
#: the most ordinary thing inheritance does.
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
#:
#: The two suppliers are the two the rule names. A scope that CHAINS runs the
#: statement that binds the attribute, so the arm that skipped the override leaves
#: the module in place. A CLASS BODY binds the attribute without any constructor
#: running at all, so the arm that skipped the override reaches it too.
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
def test_a_branched_override_of_an_attribute_no_path_supplies_is_not_a_write(
    shape, snippet
):
    """The branch rule read on the OBJECT half, driven instead of described.

    ``_branched`` says which statements a run can skip, which is one fact and the
    same fact for both halves of the table. Whether skipping one MATTERS is a
    different question: a name survives because the ``class`` statement that bound
    it ran anyway, and an attribute set only inside a base's ``__init__`` does not,
    because on the arm that skipped the override nothing ever created it.

    Reverting the condition in ``_scope_own_bindings`` to ``optional and not
    owner`` makes all six fire again, on code a person writes without thinking
    about a guard at all.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape
    assert _unnamed_writers(REPORTS_PACKAGE + ".aging", AGING_SOURCE + snippet) == [], shape


@pytest.mark.parametrize(
    "shape,snippet",
    A_BRANCHED_OVERRIDE_THE_BASE_STILL_SURVIVES,
    ids=[one[0] for one in A_BRANCHED_OVERRIDE_THE_BASE_STILL_SURVIVES],
)
def test_a_branched_override_still_loses_to_a_binding_that_survives_it(shape, snippet):
    """The half a restriction on the key's SPELLING would have cost.

    Each of these has a real path on which the attribute is the module, so each
    has to keep firing. Restricting the branch rule to identifier keys, which is
    the one line fix that makes the six above go quiet, makes the first of these
    quiet too, and that is the measurement that says the flag was not the answer.
    Deleting the ``chained`` term makes the first two quiet; deleting the
    ``table.get(key)`` term makes the last two quiet.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


#: A CLASS BODY BINDING UNDER AN ORDINARY CONSTRUCTOR, which is the most common
#: class in the language and which the table read as a write.
#:
#: ``Keeper.mod`` really IS the module, so a read through the class writes and has
#: to fire. ``self.mod`` is not, because an instance attribute unconditionally
#: shadows a class attribute: executed, ``Keeper.mod is config`` is True while
#: ``Keeper({"a": 1}).mod is config`` is False and the call raises
#: ``AttributeError``. One binding, two spellings, two different answers.
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
    """Both spellings of one attribute, because the two disagree at runtime.

    Asserting only that the instance read goes quiet would pass on a table that
    threw the class body away, which would lose every class that pins a module as
    a class attribute and never touches it again. Asserting only that the class
    read fires is what the table did before, and it reported the constructor.

    Reverting ``weak`` out of ``_record`` puts the false positive back. Making the
    CLASS spelling a weak write too makes the third assertion fail, because a
    method that rebinds ``Keeper.mod`` would then take it back from the class body
    instead of standing beside it.
    """
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
    """The order independence ``_record`` claims, driven in both orders.

    A tier written as an ORDER rather than as a set would answer one of these two
    differently from the other, and the walk's order is an implementation detail
    that no rule should rest on.
    """
    assert filesystem_mutations(AGING_SOURCE + CLASS_BODY_WRITTEN_AFTER_THE_CONSTRUCTOR) == []


#: TWO INSTANCE WRITES TO ONE ATTRIBUTE, one resolved and one not, under a class
#: body that binds the same name. ``_record``'s rule is that a key which RESOLVED
#: is never taken back by one that did not, and the class body's mark is what
#: would let it happen anyway: a mark admits an unresolved write, so the write
#: that resolved the key has to clear it on the way out.
#:
#: The write is real. On the path where ``forget`` has not been called,
#: ``self.mod`` is the module and ``go`` writes the configuration file, which is
#: the same "reachable on one path is reachable" rule the rest of this table
#: rests on. Losing it is silent: the guard reports nothing and the file is
#: written.
#:
#: BOTH ORDERS, because the walk's order is an implementation detail. Only one of
#: the two is the order that costs something, and a fixture written in the other
#: order alone would report the guard as covered while the hole stayed open.
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
    """The half of ``_record`` that clears the mark, which nothing drove.

    The rule is stated in both directions and only one of them had a fixture. A
    key that did not resolve is admitted while the key is marked, so a class body
    that marks ``self.mod`` and a constructor that resolves it leave a key that is
    resolved and still marked, and the next unresolved write to it wins. The
    module binding is then gone from the table, ``self.mod.save(cfg)`` resolves to
    nothing, and a real configuration write goes unreported.

    Dropping ``faint.discard`` from ``_record`` makes the first and third of these
    quiet. The second stays green on its own, which is why it is here: it is the
    order in which the hole costs nothing, and it was the only order this suite
    had.
    """
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
    """Both directions of the restore, because only one of them is a write.

    Reverting ``_deleted_attributes`` out of ``_walk_bindings`` makes the first
    quiet. Making the restore an unconditional overwrite rather than a fill makes
    the second fire, on a shape whose every path is an ``AttributeError``.
    """
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
#:
#: ``Keeper = Keeper`` is the other one, and it needs no judgement at all about
#: what a callee hands back, which is the undecidability that residual rests on for
#: ``Keeper = dataclass(Keeper)``. A statement whose right hand side is the
#: spelling of its own target cannot change what the target is bound to.
#:
#: The third is the same wrapper that residual files, one indent in. ``if flag: Keeper =
#: dataclass(Keeper)`` leaves a path on which the name is still the class, and a
#: veto cast inside a branch a run can skip is not a veto that run cast. The
#: undecidable part is untouched: the unconditional spelling is still quiet.
#:
#: The fourth and fifth are ``Keeper = Keeper or None`` and ``Keeper = Keeper if
#: True else None``, and they were quiet while that residual said the remaining
#: silence was "for the three wrapper spellings only". Neither is a wrapper and
#: neither is undecidable: ``_bound_value`` already reads ``or`` and a conditional
#: expression through, on the stated rule that a value reachable on one path is
#: reachable, and a class object is always truthy besides. Executed, both leave
#: ``Keeper.mod is config`` True.
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

    Both execute. ``Keeper.mod is config`` is true at runtime in the conditional,
    because only the arm that binds it runs, and true after ``Keeper = Keeper``
    because both bindings are the same class. Neither needs a decision about what
    a callee hands back.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    A_NAME_THAT_NO_LONGER_MEANS_ITS_CLASS,
    ids=[one[0] for one in A_NAME_THAT_NO_LONGER_MEANS_ITS_CLASS],
)
def test_a_binding_that_really_replaced_something_still_takes_the_name(shape, snippet):
    """The quiet direction of the same two fixes, which is where they could go wrong.

    That residual's own shape is here rather than only in the residual list,
    because a rule about conditional arms that also fired on two definitions in
    one statement list would be the same over-reach one statement wider.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_a_class_written_inside_a_factory_still_reaches_its_own_attribute():
    """The write the unique key must not cost, beside the false positive it fixes.

    Two factories each returning a ``Keeper`` must not share a binding, and the
    ``Keeper`` inside one factory must still resolve to its own class body. A key
    that answered nothing would pass the quiet assertions above on its own.
    """
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
    """``Row.go = _go`` through the audit, which reads one statement at a time.

    The function is written at module level, so on its own its first parameter is
    nobody's instance and ``self.mod`` resolves against nothing. The pairing is
    written in a third statement, which is why the audit reads the whole module
    for it before the loop starts rather than asking each statement about itself.
    """
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
    """The same family resolution through the audit, whose owner is one statement.

    The audit keys a class by its DEFINITION SITE for the same reason the walk
    does, and both derive it from the node so the two cannot drift. Read under the
    class's NAME instead, the two would agree by accident for as long as no file
    spelled one name twice.
    """
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
        '\n\ndef go(p, d, flag):\n    table = vars(Path) if flag else Path.__dict__\n'
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
    """Rule 5 asked of the table rather than of the expression under its own nose.

    Every one of these is two lines appended to the real ``aging``, and every one
    of them wrote a file with both structural guards and the audit green.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet), shape


@pytest.mark.parametrize(
    "shape,snippet",
    ORDINARY_LOOKUPS_THROUGH_A_BINDING,
    ids=[one[0] for one in ORDINARY_LOOKUPS_THROUGH_A_BINDING],
)
def test_an_ordinary_mapping_bound_to_a_name_is_not_a_namespace(shape, snippet):
    """The receiver, still doing the separating once the receiver can be a binding.

    A rule that followed ``table = ...`` and then compared the key against the
    mutation set would be round four's receiver free rule with a binding table
    bolted on, which is worse than round four's: it would reach the dispatch
    tables an inline reading could not see.
    """
    assert filesystem_mutations(AGING_SOURCE + snippet) == [], shape


def test_a_namespace_key_this_cannot_read_is_a_finding_only_where_writing_is_banned():
    """Rule 5's computed half, on the same switch rule 4's computed half is on.

    Inside the governed package a lookup this cannot read IS the violation,
    because that package has promised not to write at all. Everywhere else
    ``vars(spec)[field]`` is ordinary, and an audit that calls it a writer is an
    audit somebody switches off (P7).
    """
    computed = '\n\ndef go(p, d, name):\n    Path.__dict__[name](p, d)\n'
    assert filesystem_mutations(AGING_SOURCE + computed)
    assert (
        _unnamed_writers(
            "cratekit.core.naming",
            "def describe(spec, field):\n    return vars(spec)[field]\n",
        )
        == []
    )


def test_a_mapping_method_that_takes_no_argument_is_a_key_this_cannot_read():
    """The ASKED branch with no argument to read, which is its own act.

    A method of a namespace that takes nothing hands back something derived from
    a type's attribute mapping and names no key at all, so there is nothing for
    the key check to compare and the answer is the one every unreadable lookup
    gets. Requiring an argument made the branch decidable on ARITY, which is how
    ``vars(Path).copy()`` walked past it.

    Asserted where the two mechanisms come apart rather than where they overlap.
    A ``copy`` whose result is then subscripted is caught twice over, once here
    and once by the propagation, so it says nothing about either. This one is
    never subscripted, so only this branch can see it; and it is quiet in the
    audit, because outside the governed package an unreadable lookup is ordinary.
    """
    unread = "\n\ndef go():\n    return vars(Path).popitem()\n"
    assert filesystem_mutations(AGING_SOURCE + unread)
    assert _unnamed_writers("cratekit.core.naming", "def go(spec):\n    return vars(spec).popitem()\n") == []


def test_a_namespace_carried_through_a_copy_is_named_by_the_audit_too():
    """The propagation with no help from the reflection switch, which is its own act.

    The audit runs with the switch OFF, so an unreadable lookup says nothing
    there and the ASKED branch cannot answer for this shape at all. What is left
    is the key, which is named, reached through a mapping the propagation carried
    from ``vars(Path)`` through a method call that took no arguments. Without the
    receiver in ``_mapping_operands`` the audit is silent on a helper that writes.
    """
    copied = 'from pathlib import Path\n\n\ndef stash(p, d):\n    vars(Path).copy()["write_text"](p, d)\n'
    assert _unnamed_writers("cratekit.core.naming", copied) == ["stash"]


def test_a_module_reached_through_the_globals_mapping_is_still_that_module():
    """The alias spelled as a lookup, which puts the module's name inside a string.

    ``globals()["config"].save(cfg)`` is ``alias = config`` with the alias never
    bound, and the whole file spells ``config`` only between quotes.
    """
    assert filesystem_mutations(AGING_SOURCE + '\n\ndef go(cfg):\n    globals()["config"].save(cfg)\n')
    assert (
        filesystem_mutations(AGING_SOURCE + '\n\ndef go(view, cfg):\n    globals()["view"].save(cfg)\n')
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
    """Four shadows nothing drove, which is four lines that read as coverage.

    An import of something else under the same name is the ordinary one and the
    other three are plainer than they look: each is a name meaning two things in
    one file, which is this repository's second recurring defect pointed at the
    binding table.
    """
    assert filesystem_mutations(source) == [], shape


def test_a_name_bound_twice_in_ONE_scope_settles_to_neither():
    """The FAILED ATTEMPT, driven where shadowing alone cannot answer it.

    Every shadow fixture above puts the import at module level and the rebinding
    inside a function, and there the two mechanisms give the same answer: the
    inner scope takes the name, so the inherited binding is removed before
    anything has to disagree with it. The failed attempt is the only thing that
    answers when both bindings are in the SAME scope, because there the import
    resolves, the other statement says nothing, and nothing beats something.

    A handle bound to a name a module also imports is the ordinary spelling of
    that, and the write beside it is what stops this from passing on a table that
    resolved nothing at all.
    """
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
    """The cost of getting the scope boundaries wrong, in the expensive direction.

    A comprehension binds its target for the comprehension. Reading it as part of
    the enclosing function would make the first line quiet AND the second, which
    is a real ``config.save`` lost to a fix for a false positive. The second case
    is the outer fixed point: an object binding fed by another object binding,
    with the feeding function written after the method that uses it, which one
    pass cannot see.
    """
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
#:
#: None of these is an attack, and that is the whole reason they are here.
#: ``aging`` already spells ``from cratekit.core import config`` at line 61, so
#: every one of them is TWO ADDED LINES in a module that exists, written by
#: somebody who has never read this guard. The receiver check that shipped
#: resolved a module from the import table or from a dotted attribute chain and
#: from nowhere else, so each of these returned the empty string and both
#: structural guards went green over a call that writes the configuration file.
#:
#: They are one fixture each rather than one combined module on purpose: a
#: combined one dies as a unit, and then eight of the nine are held up by the
#: ninth, which is the shape ``rmtree`` and ``truncate`` were already in.
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
#:
#: Unlike the nine above, these ARE deliberate: nobody writes
#: ``Path.__dict__["write_text"]`` by accident. They are caught anyway because
#: catching them is two narrow rules rather than an arms race, and because
#: leaving them out would have meant filing a residual that says the guard is
#: blind to four named spellings. What must not be read into their presence is a
#: claim of completeness. A checker reading names cannot beat an author who is
#: reading it back.
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
#:
#: ``CORRECT_GENERIC_ATTRIBUTE_NAMES`` covers a receiver whose name is ordinary.
#: These cover a receiver whose name is ``config`` or ``naming``, which is
#: ordinary too and was reported as a write to the library, because a receiver
#: the check could not resolve was answered with the variable's own name. Adding
#: those names to the correct-code fixture above would have been the same shape a
#: third time; resolving by BINDING is what makes them quiet, and an unresolvable
#: receiver is now unresolved rather than a module.
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
    """P7's first half, run against the thing the guard exists to catch.

    Seven import shapes are covered, and three of them were live holes.

    The ALIASED one is the shape that has already defeated a guard here: the
    armed copy of U11's comma-separated-file guard checked ``import csv`` and
    ``from csv import DictWriter`` and never the alias, so it was one keyword
    away from being switched off.

    The DYNAMIC one needs no import statement at all, so a walk over ``ast.Import``
    and ``ast.ImportFrom`` reported it clean while it loaded ``os``,
    ``subprocess`` and ``sqlite3``, which is every capability the allowlist's
    argument rests on excluding.

    The SIBLING one is the shape the allowlist itself let through: a module named
    ``cratekit.modules.reports_ledger`` matched this package on a bare prefix and
    sits outside the directory the walk covers, so the private ignore ledger the
    countdown against this unit forbids by name could have been written, imported
    and called with both structural guards green.
    """
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
    """Twenty seven spellings of one act, six of which used to pass.

    ``Path(p).open("w")`` is the idiomatic one and was read as mode ``"r"``,
    because the mode was taken from the position the BUILTIN puts it in.
    ``Path(a).replace(b)`` overwrites its destination while its sibling
    ``rename`` was already forbidden. And ``getattr`` with a computed attribute
    name never spells the method at all.

    Three of round two's need no evasion at all. BINDING WITHOUT CALLING takes
    every mutating name out of the call positions the guard read, which is the
    bound ``open`` hole one step further out. The other two write through modules
    the ALLOWLIST admits: the allowlist's stated argument was that nothing it
    lets in can touch a file except through ``pathlib``, and
    ``test_the_allowlist_admits_no_writer_this_guard_cannot_name`` walks the
    admitted modules and finds four writers that are not ``pathlib``. A report
    calling ``config.load_from_path`` would not even look like a write.

    ROUND THREE'S FIVE ARE THE BRANCHES THE OTHER NINE LEFT UNDRIVEN. The ALIASED
    module and the IMPORTED writer are the receiver check's own two evasions, and
    an alias is the shape that has already defeated a guard in this repository
    once. The BARE NAME is the only one of the fourteen that reaches a pathlib
    writer without an attribute, so it is the only thing holding up rule 1's name
    branch, which round two justified with a spelling no fixture used. And the
    two LITERAL ``getattr``
    spellings are the half of rule 4 that had no positive fixture at all: with
    that half gated off behind the reflection switch, a four-token helper named
    ``stash`` is invisible to the audit, never forced into the mutation set, and
    reachable by name from a report with both structural guards green.

    ROUND FOUR'S THIRTEEN SPLIT INTO TWO GROUPS THAT DESERVE DIFFERENT ANSWERS.
    Nine of them are ORDINARY CODE: an alias, a list, a dict, a returned module,
    a loop variable, a default argument, an attribute store, a rebound
    ``getattr`` receiver and a star import. Every one is two added lines in
    ``aging``, which already imports ``config``, and every one wrote the
    configuration file with both structural guards green, because the receiver
    check read the import table and nothing else. That is the threat this guard
    is FOR and it is closed in code.

    The other four, the type dictionary, ``vars``, and the bound and unbound
    ``__getattribute__``, are DELIBERATE. They are caught because catching them
    is two narrow rules rather than an arms race, and their presence is not a
    claim that a determined author can be stopped by reading names. That claim
    would be false, and this file has shipped enough of those.
    """
    assert filesystem_mutations(source)


#: Every name ``FILESYSTEM_MUTATIONS`` carries, WRITTEN OUT A SECOND TIME.
#:
#: Duplicating a literal is normally the wrong answer, and here it is the only
#: one that works. Parametrizing over the set itself would delete the test case
#: along with the set member, so the set would certify its own coverage: measured,
#: removing all twelve of ``chmod`` through ``write_bytes`` together cost exactly
#: one test and removing any one of them alone cost nothing at all. ``rmtree`` and
#: ``truncate`` were the clearest case, each held up only by the other because one
#: fixture spelled both. The equality check below is what keeps the two lists in
#: step, so dropping a name from the set fails here as well as in its own case.
_EVERY_MUTATING_NAME = (
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
    """The two spellings of the same set, held together.

    Without this, dropping a name from ``FILESYSTEM_MUTATIONS`` would leave the
    case below passing against a set that no longer carries it, which is a test
    certifying a constant it was supposed to check.

    A LENGTH CHECK USED TO SIT BESIDE THIS and it is gone, for the reason round
    three removed its twin next to ``_elements_written_twice``: for a literal of
    string constants there is no input on which a duplicate and a length
    disagree, so it was a guard covered by the shape of its sibling. Duplicates
    in these two literals are covered where every other literal in this file has
    them covered, by the parse-time check below, which reads the SOURCE and is
    therefore the only thing that can see a repeat at all.
    """
    assert set(_EVERY_MUTATING_NAME) == FILESYSTEM_MUTATIONS


def test_the_writing_modes_are_the_list_this_suite_drives():
    """The same holding, for the mode characters."""
    assert set(_EVERY_WRITING_MODE) == _WRITING_MODES


@pytest.mark.parametrize("verb", _EVERY_MUTATING_NAME)
def test_every_mutating_name_is_caught_on_its_own(verb):
    """One case per member, so each member DIES ALONE.

    A set whose members are only ever driven in clusters is a set that can lose
    any one of them silently, and this one could lose twelve of fourteen.
    """
    assert filesystem_mutations(f"def remember(path):\n    path.{verb}()\n") == [
        f"line 2: {verb}"
    ]


@pytest.mark.parametrize("mode", _MODES_THAT_WRITE)
def test_open_is_caught_in_every_mode_that_can_write(mode):
    """``a``, ``x`` and ``+`` were carried by the set and driven by nothing."""
    assert filesystem_mutations(f'def remember(path):\n    return open(path, "{mode}")\n')


@pytest.mark.parametrize("mode", _MODES_THAT_READ)
def test_open_stays_quiet_in_a_mode_that_only_reads(mode):
    """The other direction, which is the one that gets a guard switched off."""
    assert filesystem_mutations(f'def remember(path):\n    return open(path, "{mode}")\n') == []


def test_a_dynamic_import_this_cannot_read_is_reported_as_unnameable():
    """A computed module name gets the computed mode's answer, not the benefit.

    Reporting it as clean would mean the whole allowlist is one string
    concatenation away from being advisory.
    """
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
    """P7's second half, which is the half that keeps getting skipped.

    The first fixture reaches the review queue in two import shapes, reads a file
    through every read primitive available including the bound ``Path.open``,
    and calls ``str.replace``, ``date.replace`` and a literal ``getattr``, which
    are the three shapes the widened mutation rules had to be narrowed around.
    The second imports a real sibling inside this package, which is what the dot
    boundary must keep legal. A guard that failed either would be routed around
    within a week, and being routed around is the failure the guard exists to
    prevent.

    The third is round three's, and it is the direction this project fails in as
    often as the other. ``view.save`` and ``spec.load`` are ordinary attribute
    reads whose names collide with two writers the allowlist admits, and while
    those two names sat BARE in the mutation set all three lines in it were
    reported as writes to the library. The receiver is the difference, and this
    is what says so.

    THE LAST THREE ARE THE SAME FAILURE ONE LEVEL ALONG, and it was LIVE when
    round four opened. A receiver the check could not resolve was answered with
    the variable's own name, so a parameter called ``config``, an attribute
    called ``self.config``, a field called ``row.config`` and a field called
    ``view.naming`` were each reported as a write to the library. The answer is
    not a longer list of blessed spellings, which is the shape that has now been
    reached for three times: it is that an unresolved receiver is UNRESOLVED. The
    middle one is the hard case, a file that really imports ``config`` and also
    takes a parameter of that name, and it is the one that says the shadow rule
    is doing work rather than the absence of an import.
    """
    assert forbidden_imports(source, "cratekit.modules.reports.planted") == []
    assert filesystem_mutations(source) == []


def test_the_package_initializer_may_import_its_own_siblings_relatively():
    """The false positive the dotted-name shortcut would have produced.

    A package's ``__init__`` resolves ``from . import aging`` against ITSELF, and
    reading the package off the dotted name gave ``cratekit.modules.aging``: a
    module that does not exist, reported forbidden. Nothing in the package writes
    a relative import today, which is exactly why this is a fixture rather than a
    bug report; the day somebody adds one, the guard would have failed correct
    code.
    """
    resolved = _resolved_imports(
        "from . import aging\nfrom .export import LibraryView\n", REPORTS_PACKAGE
    )
    assert resolved == [f"{REPORTS_PACKAGE}.aging", f"{REPORTS_PACKAGE}.export"]
    assert forbidden_imports(
        "from . import aging\n", REPORTS_PACKAGE
    ) == []


def test_a_from_import_of_a_package_resolves_to_the_module_it_names():
    """``_PACKAGE_DEPTH``, which round one's filesystem read quietly subsumed.

    ``_is_package`` asks the source tree, and the source tree answers for every
    package in this repository, so the depth rule stopped being reachable for
    anything under ``cratekit`` the moment that read landed. It survived being
    moved to ZERO with the whole suite green, which is a tuning constant nobody
    is holding.

    What it still does is the STANDARD LIBRARY, which is not in the source tree
    and which ``_is_package`` therefore answers False for. Without the depth
    rule, ``from collections import abc`` resolves to the bare package rather
    than to the module it names. Both are permitted today because both are on
    the allowlist, so no verdict moves, and that is exactly why the resolution
    itself has to be the assertion: an allowlist that later admits a submodule
    without its parent would start waving through the parent instead.
    """
    planted = "cratekit.modules.reports.planted"
    assert _resolved_imports("from collections import abc\n", planted) == ["collections.abc"]
    assert _resolved_imports("from cratekit.core import review\n", planted) == [
        "cratekit.core.review"
    ]
    assert _resolved_imports("from cratekit.core.review import Option\n", planted) == [
        "cratekit.core.review"
    ]


def test_the_real_package_reaches_the_review_queue_at_all():
    """Otherwise the two guards above are satisfied by a package that does nothing.

    A read-only promise is trivially true of code that never runs. This is the
    positive control that keeps the negative ones honest, and it is the same
    property the armed countdown in ``tests/test_review_queue.py`` asserts from
    the other side.
    """
    reached = [
        module
        for module, source in _report_modules()
        if "cratekit.core.review" in _resolved_imports(source, module)
    ]
    assert reached == ["cratekit.modules.reports.duplicates"]


def test_the_package_is_gated_by_declared_module_toggles():
    """R5: both rows are Module rather than Core, so both need a toggle to follow.

    Read from the profile layer rather than restated, so a rename there fails
    here instead of leaving a report that no profile can switch off.
    """
    from cratekit.core import profiles

    assert {"duplicates", "reports"} <= set(profiles.MODULES)
    assert not ({"duplicates", "reports"} & profiles.PROFILES["slim"])
    assert {"duplicates", "reports"} <= profiles.PROFILES["full"]


def test_the_reports_never_name_a_taxonomy_display_name():
    """R19 from the other side. The guard in test_layering only covers LOWER layers.

    ``higher_concept_violations`` returns nothing for a modules-layer file, so
    this package is outside it by design and a hardcoded ``INBOX`` here would
    pass the repository-wide check. The intake flow arrives as a declared
    taxonomy node instead, and this asserts that it has to.
    """
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
    """A second taxonomy gets a second answer, which is what R19 is worth.

    A library whose intake flow is called something else is not an exotic case,
    it is the default for anyone who did not copy this author's library. The
    declared display is followed wherever it points: a taxonomy naming a folder
    this tree really has gets that folder's playlists, and nothing about ``INBOX``
    is written into this module for either answer to depend on.
    """
    renamed = taxonomy.Node(id=INTAKE.id, display="Deep House")
    groupings = aging.intake_groupings(view, intake=renamed, today=TODAY)
    assert [group.display for group in groupings] == ["High"]


def test_a_declared_intake_flow_that_is_nowhere_in_the_tree_refuses(view):
    """Absent is not empty, and rendering them the same way is the whole defect.

    An intake queue with nothing waiting in it and a report that never found the
    intake flow produce the same output: no groupings. Only one of them means the
    person can stop reading. This is ``export``'s own doctrine one module along,
    and the filter it replaces returned an empty report with no refusal and no
    signal for a taxonomy whose display this library does not use.
    """
    absent = taxonomy.Node(id=INTAKE.id, display="Bandcamp Queue")
    with pytest.raises(CratekitError) as raised:
        aging.intake_groupings(view, intake=absent, today=TODAY)
    assert raised.value.cause.reason == "intake-flow-absent"
    assert raised.value.cause.detail["declared"] == "Bandcamp Queue"


def test_an_intake_flow_nested_inside_another_folder_is_still_the_intake_flow():
    """The filter used to be anchored at position zero of the path.

    Somebody who moved their intake folder inside an archive folder got an empty
    report, silently. Two intake nodes at two depths both yield groupings, which
    is what this module's docstring has always claimed and what only used to be
    true of the top level.
    """
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
    """The other side of the refusal, and the reason it needs the folder list.

    An intake queue somebody has just cleared is the good outcome, and a report
    that refused it would be a guard firing on correct code.
    """
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
    """A typo in a year must not buy a grouping immunity from the report.

    ``phil_1_5_99`` parses to 2099, which bands current, renders as an age of
    minus twenty six thousand days, and can never become stale. A date later than
    the day the report is run for is a bad SHAPE, and this module already has an
    answer for a bad shape: report it undated, with the name in front of a
    person, because that is what gets the name fixed.
    """
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
