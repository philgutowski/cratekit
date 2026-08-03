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


def test_every_report_runs_with_the_library_directory_read_only(
    cfg, library_on_disk, tmp_path
):
    """READ ONLY, proved by taking the permission away rather than by watching.

    The digests above are an OBSERVATION: they say nothing moved on the paths
    those two calls happened to take. This is the PROPERTY: with the library
    directory and every file in it stripped of write permission, both reports
    still produce their answers. A scratch file beside the export, a lock, a
    sighting ledger, a rewrite of the export, a chmod, all of them fail here
    whatever the digest happened to be looking at.

    THE LOCK IS PROVED BEFORE IT IS TRUSTED. A test that only asserts success
    under a permission change it never confirmed is the absence-read-as-absence
    shape aimed at itself: on a filesystem that ignores the mode, or as a user
    who outranks it, it would pass while proving nothing. So the first thing
    inside the window is a write that MUST fail.

    AND IT FAILS RATHER THAN SKIPS when the lock does not hold, which is
    deliberate and is the repository's own rule rather than a preference:
    ``tests/test_pending_units.py`` allows no skip constructed outside the
    pending register, because a skip is a guard switched off with nothing
    counting down to its return. A run that cannot express this property has not
    checked the unit's central claim, and saying so out loud is the only honest
    report of that.

    The review queue stays writable on purpose, because it is not in the library.
    That is the whole architecture in one line: the one thing this package
    persists lives in the decision store, and the library is a document it reads.
    """
    music = cfg.library.root / "Music"
    locked = [library_on_disk, *sorted(music.glob("*.flac"))]
    modes = {path: path.stat().st_mode for path in [music, *locked]}
    scratch = music / "scratch.tmp"
    for path in locked:
        path.chmod(0o444)
    music.chmod(0o555)
    try:
        try:
            scratch.write_bytes(b"the lock has to be real")
            held = False
        except OSError:
            held = True
        assert held, (
            "the library directory is still writable after chmod 0o555, so this "
            "proof would pass without proving anything. It needs an ordinary "
            "user and a filesystem that honours permission bits; running as root "
            "defeats it. There is deliberately no skip here, because a read-only "
            "claim that quietly stops being checked is the defect this unit is."
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
        for path, mode in modes.items():
            path.chmod(mode)
        # Only reachable when the lock did not hold, and the tree digest tests
        # run against their own temporary directories, so this is tidiness rather
        # than isolation. It is here because a file left behind by a failing
        # read-only proof is the one piece of evidence somebody debugging it
        # would most want to be sure came from the test.
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
        # ── APPENDED: the write surface the ALLOWLIST itself admits ─────────
        #
        # Appended rather than filed alphabetically for the reason the verb
        # registry, the pending register and the cause mapping all give: two
        # units inserting into the middle of one literal auto-merge, and an
        # append conflicts textually, which is a conflict somebody reads.
        #
        # The names above are pathlib and shutil. These are this repository's
        # own, and they are here because the allowlist's argument was WRONG.
        # That comment said nothing admitted here can touch a file except
        # through pathlib, and
        # ``test_the_allowlist_admits_no_writer_this_guard_cannot_name`` walks
        # the admitted modules and shows otherwise: ``cratekit.core.config``
        # exposes three writers and a locking context manager, and
        # ``cratekit.core.naming``, which ``duplicates`` already imports,
        # exposes one. ``load`` and ``load_from_path`` are the dangerous pair,
        # because their names read as pure loads and they write the file back.
        #
        # None of these is reachable from correct code in this package: a report
        # is HANDED a ``Config`` by its caller and neither loads nor saves one,
        # and claiming a target filename is what a WRITER does with a name this
        # package only ever parses. The walking test is what keeps this list true
        # as those modules change, rather than a reviewer's snapshot of them.
        "_exclusive_lock",
        "_mkdir_private",
        "claim_target",
        "load",
        "load_from_path",
        "save",
    }
)

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

    Four rules, and each of the last three is narrowed so it cannot fire on
    correct code, because a guard that does is a guard somebody routes around
    (P7).

    1. One of the named mutating methods, REACHED rather than merely called.
       An attribute access spelling one of those names is reported wherever it
       appears, because ``keep = Path(p).write_text`` followed by ``keep(x)``
       writes a file with no mutating name in any call position at all: the
       outer call's ``func`` is a plain local. That is round one's bound-``open``
       hole one step further out, and the same answer closes it. A bare name
       call is still checked separately, since ``rmtree(a)`` after a ``from
       shutil import rmtree`` has no attribute to read (the import guard is what
       catches that one first).
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
    4. A ``getattr`` naming one of the mutating methods, or naming an attribute
       this cannot read. ``getattr(Path(p), "write_" + "text")(decided)`` writes
       a file while the outer call's ``func`` is itself a Call and its ``attr``
       never appears anywhere, which is the same walk-past as the computed mode
       and gets the same answer.
    """
    return mutations_in(ast.parse(source))


def mutations_in(tree: ast.AST, *, reflection: bool = True) -> list[str]:
    """The four rules above, applied to any node rather than to a whole module.

    Split out so the allowlist audit below can ask the same question about ONE
    function. A second copy of these rules answering it would be the divergence
    ``tests/_source_guards.py`` exists because of, and it would diverge in the
    direction that matters: the audit would stop recognizing a write shape this
    guard had just learned.

    ``reflection`` turns rule 4 off, and only the audit does that. Rules 1 to 3
    each describe an act that CHANGES A FILE; rule 4 describes an act this
    checker cannot read, which is a violation inside a package that has promised
    not to write and is ordinary everywhere else. Left on, it reported four
    reflective helpers in ``config``, ``naming`` and ``taxonomy`` as writers, and
    an audit that cries wolf about ``getattr(row, field)`` is an audit somebody
    switches off.
    """
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in FILESYSTEM_MUTATIONS:
            # The ATTRIBUTE rather than the call around it, so a bound method
            # captured now and called later is caught at the point it is
            # reached. A called one lands here too and only here: the walk
            # visits the enclosing Call first, where the branch below
            # deliberately checks a bare name only, so nothing is reported
            # twice.
            found.append(f"line {node.lineno}: {node.attr}")
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
        elif reflection and name == "getattr" and len(node.args) >= 2:
            wanted = node.args[1]
            if not isinstance(wanted, ast.Constant) or not isinstance(wanted.value, str):
                found.append(f"line {node.lineno}: getattr(<computed attribute>)")
            elif wanted.value in FILESYSTEM_MUTATIONS:
                found.append(f"line {node.lineno}: getattr({wanted.value!r})")
    return found


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


@pytest.mark.parametrize("name", ["ALLOWED_IMPORTS", "FILESYSTEM_MUTATIONS"])
def test_the_guard_literals_have_no_element_written_twice(name):
    """A duplicate in a set literal is silent: the runtime object deduplicates it.

    This repository has shipped that shape once with the whole suite green, in
    ``EXPECTED_PENDING``. Every other test over these two sets iterates the
    RUNTIME object and is therefore blind to it, and here it would matter in the
    direction that hurts: an entry believed to be present because a reviewer read
    it in the diff, collapsed onto another, so the guard covers one fewer name
    than anybody thinks. Counting the literal's elements against the runtime
    length is the only check that can see it.
    """
    import inspect

    literal = None
    for node in ast.walk(ast.parse(inspect.getsource(sys.modules[__name__]))):
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        if target == name:
            literal = node.value

    assert literal is not None, f"{name} is no longer a module-level assignment"
    elements = literal.args[0].elts if isinstance(literal, ast.Call) else literal.elts
    written = [element.value for element in elements]
    duplicates = sorted({value for value in written if written.count(value) > 1})
    assert not duplicates, f"written twice and collapsed at parse time: {duplicates}"
    assert len(written) == len(globals()[name])


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


def _admitted_repository_modules() -> list[tuple[str, Path]]:
    """Every entry in the allowlist that is a file in THIS repository.

    Walked from the allowlist rather than listed (P3). A module added to the
    allowlist in a future diff is audited by the test below without anybody
    remembering to add it here, which is the property a hand-listed copy loses
    on its first edit.
    """
    out: list[tuple[str, Path]] = []
    for dotted in sorted(ALLOWED_IMPORTS):
        if not dotted.startswith("cratekit."):
            continue
        path = SRC_ROOT.joinpath(*dotted.split(".")).with_suffix(".py")
        if path.is_file():
            out.append((dotted, path))
    return out


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
    change a file must itself be a name ``FILESYSTEM_MUTATIONS`` carries, and the
    only exemption is the one module R12 licenses to persist. There are two ways
    to answer a failure and both are correct: name the writer in the set, or take
    the module off the allowlist. What is not available is leaving the argument
    written down and untrue.
    """
    unnamed: dict[str, list[str]] = {}
    for dotted, path in _admitted_repository_modules():
        if dotted == SANCTIONED_PERSISTENCE:
            continue
        tree = ast.parse(path.read_text())
        loose: list[str] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # The reachable name is what a caller in the reports package
                # would have to spell: the function, or the class it constructs
                # to get at a writing method or a context manager.
                if mutations_in(node, reflection=False) and node.name not in FILESYSTEM_MUTATIONS:
                    unnamed.setdefault(dotted, []).append(node.name)
            else:
                # A write at module level has no name to guard at all, so
                # importing the module performs it. That is never acceptable on
                # the allowlist, whatever it is called.
                loose += mutations_in(node, reflection=False)
        if loose:
            unnamed.setdefault(dotted, []).append(f"<at import time> {sorted(set(loose))}")

    assert not unnamed, (
        f"the reports allowlist admits modules whose writers this guard cannot "
        f"name: {unnamed}. Either add each name to FILESYSTEM_MUTATIONS so a "
        f"report calling it is caught, or drop the module from ALLOWED_IMPORTS. "
        f"The allowlist's comment claims nothing it admits can touch a file "
        f"except through pathlib, and that claim is what this asserts."
    )


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
    ],
)
def test_the_mutation_guard_bites_the_private_ledger_in_every_shape(source):
    """Nine spellings of one act, six of which used to pass.

    ``Path(p).open("w")`` is the idiomatic one and was read as mode ``"r"``,
    because the mode was taken from the position the BUILTIN puts it in.
    ``Path(a).replace(b)`` overwrites its destination while its sibling
    ``rename`` was already forbidden. And ``getattr`` with a computed attribute
    name never spells the method at all.

    The last three are round two's, and the last two are the more serious pair
    because they need no evasion at all. BINDING WITHOUT CALLING takes every
    mutating name out of the call positions the guard read, which is the bound
    ``open`` hole one step further out. The other two write through modules the
    ALLOWLIST admits: the allowlist's stated argument was that nothing it lets
    in can touch a file except through ``pathlib``, and
    ``test_the_allowlist_admits_no_writer_this_guard_cannot_name`` walks the
    admitted modules and finds four writers that are not ``pathlib``. A report
    calling ``config.load_from_path`` would not even look like a write.
    """
    assert filesystem_mutations(source)


def test_a_dynamic_import_this_cannot_read_is_reported_as_unnameable():
    """A computed module name gets the computed mode's answer, not the benefit.

    Reporting it as clean would mean the whole allowlist is one string
    concatenation away from being advisory.
    """
    assert forbidden_imports(
        EVASIVE_COMPUTED_DYNAMIC_IMPORT, "cratekit.modules.reports.planted"
    ) == [_COMPUTED_IMPORT]


@pytest.mark.parametrize("source", [CORRECT_MODULE, CORRECT_IN_PACKAGE_IMPORT])
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
