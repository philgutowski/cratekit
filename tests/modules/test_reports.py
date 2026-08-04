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
import sqlite3
import subprocess
import sys
from datetime import date
from pathlib import Path

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
QUALIFIED_MUTATIONS = frozenset(
    {
        "config._exclusive_lock",
        "config._mkdir_private",
        "config.load",
        "config.load_from_path",
        "config.save",
        "naming.claim_target",
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


def _is_package(dotted: str) -> bool:
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
    return SRC_ROOT.joinpath(*dotted.split(".")).is_dir()


def _package_of(module: str) -> str:
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
    if SRC_ROOT.joinpath(*module.split(".")).is_dir():
        return module
    return module.rsplit(".", 1)[0]


def _resolved_imports(source: str, module: str) -> list[str]:
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
    """
    package = _package_of(module)
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = package.split(".")
                base = ".".join([*parts[: len(parts) - node.level + 1], *([base] if base else [])])
            if len(base.split(".")) <= _PACKAGE_DEPTH or _is_package(base):
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
    tempted to claim more. It is a defence against an ORDINARY AUTHOR writing
    ordinary code that happens to write: an alias, a container, a default
    argument, a bound method, a helper reached through a module the allowlist
    admits. It is NOT a defence against an author who has read this function and
    means to get past it. A checker reading names cannot win that, and the four
    dunder and subscript spellings below are named rather than left silent so
    that nobody later reads silence as coverage.

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
    2. A call to ``open`` whose mode is anything other than a literal read mode.
       Narrowed rather than banned outright because ``open(path, "rb")`` is a
       perfectly correct read. A mode this cannot READ is a violation, since a
       computed mode is exactly how the check would be walked past.
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
       on the same terms.
    5. A SUBSCRIPT whose constant key names a mutating method.
       ``Path.__dict__["write_text"](p, d)`` and ``vars(Path)["write_text"](p, d)``
       reach the function object without an attribute access and without a callee
       this can name. Nothing in this repository subscripts a constant that spells
       a filesystem verb, so the rule costs nothing and is narrow enough that an
       ordinary dispatch table keyed on anything else never sees it.
    """
    tree = ast.parse(source)
    modules, direct = _writer_bindings(tree)
    return mutations_in(tree, modules=modules, direct=direct)


def _receiver_key(node: ast.AST) -> str:
    """A canonical spelling of one receiver EXPRESSION, or "" when it has none.

    The binding table below is keyed on this rather than on a bare name, because
    the shapes an ordinary refactor produces are not all bare names. ``self.mod``,
    ``MODS[0]``, ``MODS["c"]`` and ``_mod()`` are each a receiver somebody writes
    without thinking about a guard at all, and each of them reaches an admitted
    module's writer with the module's own name nowhere beside the call.

    A key is rendered only for a spelling that can be resolved back to ONE
    binding. ``Path(p)`` carries arguments, so it renders nothing: what it
    returns depends on what it was handed. That is the point of the rewrite.
    A receiver this cannot read is UNRESOLVED, and the previous version answered
    unresolved with the variable's own name, which reported
    ``def f(config): return config.load`` as a write to the library.
    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _receiver_key(node.value)
        return f"{base}.{node.attr}" if base else ""
    if isinstance(node, ast.Subscript):
        base = _receiver_key(node.value)
        if base and isinstance(node.slice, ast.Constant):
            return f"{base}[{node.slice.value!r}]"
        return ""
    if isinstance(node, ast.Call):
        base = _receiver_key(node.func)
        return f"{base}()" if base and not node.args and not node.keywords else ""
    return ""


#: The node types that carry a PARAMETER LIST, which is the only thing that can
#: take a name back from a module the file imported. A class body is not one:
#: it binds nothing of its own, so it is walked as part of whatever encloses it
#: and its methods are reached as the scopes they are.
_SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


def _scope_nodes(node: ast.AST):
    """Every node inside one scope, stopping where a nested scope begins."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPES):
            continue
        yield child
        yield from _scope_nodes(child)


def _nested_scopes(node: ast.AST):
    """Every function, lambda and class body directly inside one scope."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPES):
            yield child
        else:
            yield from _nested_scopes(child)


def _bound_module(node: ast.AST, modules: dict[str, str]) -> str:
    """The admitted module one expression evaluates to, or the empty string."""
    key = _receiver_key(node)
    return modules.get(key, "") if key else ""


def _element_bindings(
    target: str, value: ast.AST, modules: dict[str, str]
) -> dict[str, str]:
    """What a container literal binds, element by element.

    ``MODS = [config]`` and ``MODS = {"c": config}`` are ordinary code, and
    ``MODS[0].save(cfg)`` and ``MODS["c"].load_from_path(p)`` reach the writer
    through them. Reading the container is what stops a list literal being an
    escape hatch that costs two characters.
    """
    found: dict[str, str] = {}
    if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
        for index, element in enumerate(value.elts):
            owner = _bound_module(element, modules)
            if owner:
                found[f"{target}[{index!r}]"] = owner
    elif isinstance(value, ast.Dict):
        for key, element in zip(value.keys, value.values):
            owner = _bound_module(element, modules)
            if owner and isinstance(key, ast.Constant):
                found[f"{target}[{key.value!r}]"] = owner
    return found


def _iterated_modules(node: ast.AST, modules: dict[str, str]) -> list[str]:
    """Every admitted module a loop could hand its target.

    A literal is read element by element; a name is read through whatever its
    elements were already bound to, so ``MODS = [config]`` followed by ``for mod
    in MODS`` resolves the same way ``MODS[0]`` does.
    """
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        found = [_bound_module(element, modules) for element in node.elts]
        return [owner for owner in found if owner]
    key = _receiver_key(node)
    if not key:
        return []
    return [owner for bound, owner in modules.items() if bound.startswith(f"{key}[")]


def _default_bindings(args: ast.arguments, modules: dict[str, str]) -> dict[str, str]:
    """Parameters whose DEFAULT is an admitted module.

    ``def f(cfg, mod=config)`` binds ``mod`` inside the function while the
    parameter list otherwise shadows everything it names, so this has to be read
    back after the shadowing rather than before it.
    """
    found: dict[str, str] = {}
    positional = [*args.posonlyargs, *args.args]
    supplied = positional[len(positional) - len(args.defaults) :]
    pairs = [*zip(supplied, args.defaults), *zip(args.kwonlyargs, args.kw_defaults)]
    for parameter, default in pairs:
        owner = _bound_module(default, modules) if default is not None else ""
        if owner:
            found[parameter.arg] = owner
    return found


def _returned_module(node: ast.AST, modules: dict[str, str]) -> str:
    """The admitted module a function hands back, so ``_mod().save(cfg)`` resolves."""
    for child in _scope_nodes(node):
        if isinstance(child, ast.Return) and child.value is not None:
            owner = _bound_module(child.value, modules)
            if owner:
                return owner
    return ""


def _rebindings(node: ast.AST, modules: dict[str, str]) -> dict[str, str]:
    """Every non-import spelling that puts an admitted module behind a new name.

    None of these is an attack. ``alias = config`` is a plain refactor,
    ``self.mod = config`` is a constructor, and a default argument is how a
    module gets injected for a test. They are listed together because they are
    all the SAME act: the receiver a report finally writes through is no longer
    spelled with the module's name, and the guard is for the ordinary author who
    wrote one of them without meaning anything by it.
    """
    found: dict[str, str] = {}
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if node.value is None:
            return found
        owner = _bound_module(node.value, modules)
        for target in targets:
            unpacked = (
                target.elts if isinstance(target, (ast.Tuple, ast.List)) else [target]
            )
            for one in unpacked:
                key = _receiver_key(one)
                if not key:
                    continue
                if owner:
                    found[key] = owner
                found.update(_element_bindings(key, node.value, modules))
    elif isinstance(node, ast.NamedExpr):
        key = _receiver_key(node.target)
        owner = _bound_module(node.value, modules)
        if key and owner:
            found[key] = owner
    elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
        key = _receiver_key(node.target)
        for owner in _iterated_modules(node.iter, modules) if key else []:
            found[key] = owner
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        found.update(_default_bindings(node.args, modules))
        owner = _returned_module(node, modules)
        if owner:
            found[f"{node.name}()"] = owner
    return found


def _writer_bindings(tree: ast.AST) -> tuple[dict[str, str], frozenset[str]]:
    """Receivers bound to an admitted module, and names bound to a writer itself.

    Read off the import statements for the same reason ``_resolved_imports``
    reads ``alias.name``: an alias is how a name check gets walked past, and
    ``from cratekit.core import config as settings`` followed by
    ``settings.save(cfg)`` spells no admitted module anywhere in the file.

    THE IMPORTS ARE NOT THE WHOLE BINDING TABLE, and an earlier version of this
    was only them. ``aging`` already spells ``from cratekit.core import config``,
    so two added lines, ``alias = config`` and ``alias.save(cfg)``, wrote the
    configuration file with both structural guards green. Everything
    ``_rebindings`` reads is one more spelling of that same two-line refactor,
    and the receiver check is worth nothing until it follows them.

    The second half is the shape a receiver check would otherwise lose outright.
    ``from cratekit.core.config import save`` binds the writer to a bare local,
    and both halves of that import are permitted, so the bare name IS the writer
    from there on and is matched as one. A STAR import binds every one of them at
    once, with no name in the file to read, so it is expanded from the set.
    """
    modules: dict[str, str] = {}
    direct: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                short = alias.name.rsplit(".", 1)[-1]
                if short in _QUALIFYING_MODULES:
                    modules[alias.asname or alias.name] = short
        elif isinstance(node, ast.ImportFrom):
            base = (node.module or "").rsplit(".", 1)[-1]
            for alias in node.names:
                if alias.name == "*":
                    direct |= _writer_names_of(node.module or "")
                elif alias.name in _QUALIFYING_MODULES:
                    modules[alias.asname or alias.name] = alias.name
                elif f"{base}.{alias.name}" in QUALIFIED_MUTATIONS:
                    direct.add(alias.asname or alias.name)
    while True:
        # A FIXED POINT rather than a pass count. A rebinding can name another
        # rebinding, and a pass limit written as a number is a constant nothing
        # can drive: measured, dropping it from four to one killed no test,
        # because ``ast.walk`` visits breadth first in document order and valid
        # Python defines a name before it uses one, so every shape this
        # repository can spell settles on the first pass. Repeating until the
        # table stops growing says the same thing without a magic number, and it
        # terminates because the keys come from the finite set of receiver
        # expressions the tree spells.
        before = dict(modules)
        for node in ast.walk(tree):
            modules.update(_rebindings(node, modules))
        if modules == before:
            return modules, frozenset(direct)


def _parameters_of(node: ast.AST) -> frozenset[str]:
    """Every name one scope's parameter list binds to something of its own."""
    args = getattr(node, "args", None)
    if not isinstance(args, ast.arguments):
        return frozenset()
    named = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    named += [one for one in (args.vararg, args.kwarg) if one is not None]
    return frozenset(one.arg for one in named)


def _visible_bindings(
    node: ast.AST, modules: dict[str, str], direct: frozenset[str]
) -> tuple[dict[str, str], frozenset[str]]:
    """The bindings a scope really sees, with the names its parameters take back.

    A PARAMETER SHADOWS, and without this the fix for one false positive would
    have installed another. ``aging`` spells ``from cratekit.core import
    config`` at line 61, so a function there taking a parameter called ``config``
    is talking about its argument, and every ``config.load`` inside it would be
    reported as a write to the library.

    A parameter takes back its OWN NAME and nothing further along. ``self.mod``
    is a binding about an object rather than about the name ``self``, and every
    method carries ``self`` in its parameter list, so shadowing the whole chain
    would lose ``self.mod = config`` in a constructor to the guard's own rule.
    That is a stated limit rather than a claim: two functions whose same-named
    parameters are different objects would share the attribute binding.
    """
    shadowed = _parameters_of(node)
    if not shadowed:
        return modules, direct
    kept = {key: owner for key, owner in modules.items() if key not in shadowed}
    kept.update(_default_bindings(node.args, modules))
    return kept, frozenset(name for name in direct if name not in shadowed)


def _receiver_module(node: ast.AST, modules: dict[str, str]) -> str:
    """Which admitted module a receiver was BOUND to, or the empty string.

    Resolution is by binding and by nothing else. A receiver with no binding is
    UNRESOLVED, which is not the same answer as a module named after the
    variable: absence read as evidence of absence is the defect this file keeps
    producing, and here it produced it aimed at correct code. ``view.save``,
    ``spec.load``, ``self.config.load`` and a parameter called ``naming`` are all
    ordinary, and a guard that fires on them is a guard somebody weakens (P7).
    """
    key = _receiver_key(node)
    return modules.get(key, "") if key else ""


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


def mutations_in(
    tree: ast.AST,
    *,
    reflection: bool = True,
    modules: dict[str, str] | None = None,
    direct: frozenset[str] = frozenset(),
) -> list[str]:
    """The four rules above, applied to any node rather than to a whole module.

    Split out so the allowlist audit below can ask the same question about ONE
    function. A second copy of these rules answering it would be the divergence
    ``tests/_source_guards.py`` exists because of, and it would diverge in the
    direction that matters: the audit would stop recognizing a write shape this
    guard had just learned.

    ``modules`` and ``direct`` are what a bare node cannot read for itself: the
    bindings that say which receiver is an admitted module and which local name
    is an admitted writer. The audit reads them off the whole module and hands
    them down, because a function read on its own has no import statement in it.

    THE WALK IS BY SCOPE rather than flat, and that is not a refactor. A
    parameter shadows, so a function in ``aging`` taking an argument called
    ``config`` is talking about its argument even though the file imports the
    module of that name, and a flat walk cannot tell the two apart.

    ``reflection`` turns off ONE HALF of rule 4, the COMPUTED attribute, and only
    the audit does that. Rules 1 to 3 each describe an act that CHANGES A FILE;
    the computed half describes an act this checker cannot read, which is a
    violation inside a package that has promised not to write and is ordinary
    everywhere else. Left on, it reported four reflective helpers in ``config``,
    ``naming`` and ``taxonomy`` as writers, and an audit that cries wolf about
    ``getattr(row, field)`` is an audit somebody switches off.

    THE SWITCH IS ON THE RESULT BEING CALLED, not on literal versus computed, and
    reading it the other way relocated the hole rather than closing it. Gating
    the literal half was the first version and it lost
    ``getattr(path, "write_text")(data)``; ungating only the literal half was the
    second and it lost ``getattr(path, "write_" + "text")(data)``, which is the
    same helper one token longer. What separates the four reflective READS from
    both is that none of them calls what it got back: they end in ``return
    getattr(spec, name)``. A reflective read whose result is CALLED is a call to
    a method this checker cannot name, and inside a module the reports package
    may import that is a writer nothing can be made to name.
    """
    resolved, reachable = _visible_bindings(tree, dict(modules or {}), direct)
    called = {
        id(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Call)
    }
    found: list[str] = []
    for node in _scope_nodes(tree):
        if isinstance(node, ast.Attribute):
            # The ATTRIBUTE rather than the call around it, so a bound method
            # captured now and called later is caught at the point it is
            # reached. A called one lands here too and only here: the walk
            # visits the enclosing Call first, where the branch below
            # deliberately checks a bare name only, so nothing is reported
            # twice.
            if node.attr in FILESYSTEM_MUTATIONS:
                found.append(f"line {node.lineno}: {node.attr}")
            else:
                owner = _receiver_module(node.value, resolved)
                if owner and f"{owner}.{node.attr}" in QUALIFIED_MUTATIONS:
                    found.append(f"line {node.lineno}: {owner}.{node.attr}")
            continue
        if isinstance(node, ast.Subscript):
            # Rule 5. ``Path.__dict__["write_text"](p, d)`` and
            # ``vars(Path)["write_text"](p, d)`` both write, and neither spells
            # the method as an attribute or as a callee this can name, so every
            # rule above falls through and ``pathlib`` is allowlisted. Read the
            # SUBSCRIPT, on the same terms rule 1 reads an attribute: a constant
            # key naming a mutating method is reported whether it is called here
            # or bound and called later.
            index = node.slice
            if isinstance(index, ast.Constant) and index.value in FILESYSTEM_MUTATIONS:
                found.append(f"line {node.lineno}: [{index.value!r}]")
            continue
        if isinstance(node, ast.Name) and node.id in reachable:
            # A writer imported off an admitted module, or one of that module's
            # own, reached with no receiver to read. Bound rather than called is
            # the same answer rule 1 gives for the same reason.
            found.append(f"line {node.lineno}: {node.id}")
            continue
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if isinstance(func, ast.Name) and name in FILESYSTEM_MUTATIONS:
            found.append(f"line {node.lineno}: {name}")
        elif name == "open":
            mode = _open_mode(node, bound=isinstance(func, ast.Attribute))
            if mode is None or _WRITING_MODES & set(mode):
                found.append(f"line {node.lineno}: open(mode={mode!r})")
        elif name == "replace" and len(node.args) == 1 and not node.keywords:
            found.append(f"line {node.lineno}: replace(one argument)")
        elif name in _REFLECTIVE_READERS:
            receiver, wanted = _reflective_arguments(node, name)
            if wanted is None:
                continue
            if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):
                if reflection or id(node) in called:
                    found.append(f"line {node.lineno}: {name}(<computed attribute>)")
                continue
            owner = _receiver_module(receiver, resolved) if receiver is not None else ""
            if wanted.value in FILESYSTEM_MUTATIONS or (
                owner and f"{owner}.{wanted.value}" in QUALIFIED_MUTATIONS
            ):
                found.append(f"line {node.lineno}: {name}({wanted.value!r})")
    for nested in _nested_scopes(tree):
        found += mutations_in(
            nested, reflection=reflection, modules=resolved, direct=reachable
        )
    return found


#: The builtin and the dunder that read an attribute by NAME. ``getattr`` is the
#: one anybody writes; ``__getattribute__`` is what it calls, it is reachable in
#: both a bound and an unbound spelling, and both of them write when they are
#: handed ``"write_text"``. Naming the dunder costs one set member and closes a
#: spelling that otherwise falls through every rule.
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


def _open_mode(node: ast.Call, *, bound: bool) -> str | None:
    """The literal mode an ``open`` call was given, or None when it is not literal.

    ``bound`` says which call this is, and getting it wrong is not a detail. The
    builtin takes the file first and the mode second; ``Path.open`` takes the
    mode FIRST, because its receiver already is the file. Reading position one
    for both made ``Path(p).open("w")`` report as mode ``"r"`` while the
    ``open(Path(p), "w")`` fixture was caught, so the idiomatic spelling was the
    one that got through, on a package that already reaches for ``Path`` and has
    ``pathlib`` on its allowlist.

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


def _admitted_repository_modules(entries=ALLOWED_IMPORTS) -> list[tuple[str, Path]]:
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
    shape this suite exists to remove.
    """
    out: list[tuple[str, Path]] = []
    for dotted in sorted(entries):
        if not dotted.startswith("cratekit."):
            continue
        base = SRC_ROOT.joinpath(*dotted.split("."))
        if base.with_suffix(".py").is_file():
            out.append((dotted, base.with_suffix(".py")))
            continue
        for path in sorted(base.rglob("*.py")):
            parts = list(path.relative_to(SRC_ROOT).with_suffix("").parts)
            if parts[-1] == "__init__":
                parts.pop()
            out.append((".".join(parts), path))
    return out


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
    short = dotted.rsplit(".", 1)[-1]
    unnamed: list[str] = []
    loose: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # The reachable name is what a caller in the reports package
            # would have to spell: the function, or the class it constructs
            # to get at a writing method or a context manager.
            named = node.name in FILESYSTEM_MUTATIONS or f"{short}.{node.name}" in QUALIFIED_MUTATIONS
            found = mutations_in(node, reflection=False, modules=imported, direct=own)
            if found and not named:
                unnamed.append(node.name)
        else:
            # A write at module level has no name to guard at all, so
            # importing the module performs it. That is never acceptable on
            # the allowlist, whatever it is called.
            loose += mutations_in(node, reflection=False, modules=imported, direct=own)
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
    """
    audited = _admitted_repository_modules()
    assert {dotted for dotted, _ in audited} >= {
        "cratekit.core.config",
        "cratekit.core.naming",
        SANCTIONED_PERSISTENCE,
        "cratekit.core.taxonomy",
        "cratekit.write.rbxml",
    }, (
        f"the audit walked {sorted(dotted for dotted, _ in audited)}, which does "
        f"not include the modules whose writers this test was written about. An "
        f"audit that walks nothing reports nothing, and reads as a pass."
    )
    unnamed: dict[str, list[str]] = {}
    for dotted, path in audited:
        if dotted == SANCTIONED_PERSISTENCE:
            continue
        found = _unnamed_writers(dotted, path.read_text())
        if found:
            unnamed[dotted] = found

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
