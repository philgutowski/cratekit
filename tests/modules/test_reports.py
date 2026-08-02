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
        ("phil_5_01_99", date(2099, 5, 1)),
    ],
)
def test_the_intake_naming_conventions_all_parse(name, expected):
    """Every shape the live library actually uses, plus the ones that must not.

    ``13_45_26`` is not a date and ``2_30_26`` is not a day that exists; both are
    reported as undated rather than coerced into the nearest thing that parses,
    because a name in front of a person is what gets the name fixed.

    A four-digit year outside this century reads as undated. A TWO-digit one
    always lands in it, so ``_99`` is 2099 rather than 1999, and a grouping dated
    in the future is simply not stale. Reading it as 1999 instead would report an
    age of nine thousand days and tell somebody to throw the list away.
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


# ═══════════════════════════════════════════════════════════════════════════
# The verification: both run against a copy and write nothing
# ═══════════════════════════════════════════════════════════════════════════


def _tree_digest(root: Path) -> dict[str, str]:
    """Every file under ``root``, by repo-relative path and content hash.

    Walked rather than enumerated (P3). A test that listed the files it expected
    to be unchanged would be blind to the one a report created, which is the
    interesting case.
    """
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


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
    """
    before = _tree_digest(tmp_path)
    rows_before = _database_rows(cfg.library.db_path)

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
    before = _tree_digest(tmp_path)
    rows_before = _database_rows(cfg.library.db_path)

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


# ═══════════════════════════════════════════════════════════════════════════
# The structural half: the package cannot write, whatever a test drives
# ═══════════════════════════════════════════════════════════════════════════

#: Every top-level module the reports package may import, and every dotted target
#: inside this one. DERIVED FROM WHAT READING NEEDS, so the allowlist is the
#: argument: nothing here can open a database, spawn a process, or touch a file
#: except through ``pathlib``, whose write methods are forbidden separately below.
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
        "cratekit.core.naming",
        "cratekit.core.review",
        "cratekit.core.taxonomy",
        "cratekit.write.rbxml",
    }
)

#: Method names that mutate the filesystem and are not also ordinary methods on a
#: string, a mapping, or a sequence. ``replace`` is deliberately absent: it is
#: ``str.replace`` far more often than it is ``Path.replace``, and a guard that
#: fires on correct code is a guard somebody routes around (P7). The import
#: allowlist is what covers the module-level route to it, since ``os.replace``
#: needs an import this package may not make.
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
        "unlink",
        "write_bytes",
        "write_text",
    }
)

#: Characters in an ``open`` mode that mean the handle can write.
_WRITING_MODES = frozenset({"w", "a", "x", "+"})

#: How many dotted parts make a PACKAGE rather than a module, for reading a
#: ``from X import y``. ``cratekit`` and ``cratekit.<subpackage>``, plus the
#: stdlib's own one and two level packages.
_PACKAGE_DEPTH = 2


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
    """
    package = module.rsplit(".", 1)[0]
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = package.split(".")
                base = ".".join([*parts[: len(parts) - node.level + 1], *([base] if base else [])])
            if len(base.split(".")) <= _PACKAGE_DEPTH:
                found += [f"{base}.{alias.name}" for alias in node.names]
            else:
                found.append(base)
    return found


def _permitted(target: str) -> bool:
    """Whether one resolved import is inside the allowlist or inside this package.

    A prefix match against an allowlisted entry is accepted, so
    ``from cratekit.core.review import Option`` resolves through
    ``cratekit.core.review`` rather than being read as a module of its own.
    """
    if target.startswith("cratekit.modules.reports"):
        return True
    return any(target == allowed or target.startswith(f"{allowed}.") for allowed in ALLOWED_IMPORTS)


def forbidden_imports(source: str, module: str) -> list[str]:
    """Every dependency the reports package is not allowed to have."""
    return [target for target in _resolved_imports(source, module) if not _permitted(target)]


def filesystem_mutations(source: str) -> list[str]:
    """Every call in ``source`` that could change a file, with its line.

    Two rules. A call to one of the named mutating methods, and a call to
    ``open`` whose mode is anything other than a literal read mode. The second is
    narrowed rather than banned outright because ``open(path, "rb")`` is a
    perfectly correct read, and forbidding it would be a guard that fires on
    correct code. A mode this cannot READ is a violation, since a computed mode
    is exactly how the check would be walked past.
    """
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name in FILESYSTEM_MUTATIONS:
            found.append(f"line {node.lineno}: {name}")
        elif name == "open":
            mode = _open_mode(node)
            if mode is None or _WRITING_MODES & set(mode):
                found.append(f"line {node.lineno}: open(mode={mode!r})")
    return found


def _open_mode(node: ast.Call) -> str | None:
    """The literal mode an ``open`` call was given, or None when it is not literal.

    An absent mode is the default, which reads, so it comes back as ``"r"``.
    """
    supplied: ast.AST | None = None
    if len(node.args) >= 2:
        supplied = node.args[1]
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

#: And with a mode this guard cannot read, which is how a literal check is walked
#: past without ever writing the letter w.
EVASIVE_COMPUTED_MODE = """
from pathlib import Path

MODE = "".join(["w"])


def remember(path, decided):
    with open(Path(path), MODE) as handle:
        handle.write(decided)
"""

#: Correct code, in both directions: the one persistence this package is allowed,
#: a read through the one read primitive, and ordinary string and mapping methods
#: whose names collide with filesystem verbs.
CORRECT_MODULE = """
from pathlib import Path

from cratekit.core import review
from cratekit.core.review import Option


def run(store, path, name):
    content = Path(path).read_bytes()
    handle = open(path, "rb")
    handle.close()
    tidied = name.replace("_", " ").casefold()
    return review.offer(
        store,
        queue=review.Queue.DUPLICATES,
        kind="duplicate-recording",
        identity={"title": tidied},
        payload={"bytes": len(content)},
        options=(Option(option_id="1", summary=tidied),),
    )
"""


@pytest.mark.parametrize(
    "source",
    [
        EVASIVE_IMPORT,
        EVASIVE_PACKAGE_IMPORT,
        EVASIVE_RELATIVE_IMPORT,
        EVASIVE_LAZY_IMPORT,
    ],
)
def test_the_import_allowlist_bites_every_shape_of_the_evasion(source):
    """P7's first half, run against the thing the guard exists to catch.

    All four import shapes are covered, and the aliased one is the one that
    matters most: the armed copy of U11's comma-separated-file guard checked
    ``import csv`` and ``from csv import DictWriter`` and never the alias, so it
    was one keyword away from being switched off.
    """
    assert forbidden_imports(source, "cratekit.modules.reports.planted")


@pytest.mark.parametrize(
    "source", [EVASIVE_PRIVATE_LEDGER, EVASIVE_WRITE_HANDLE, EVASIVE_COMPUTED_MODE]
)
def test_the_mutation_guard_bites_the_private_ledger_in_every_shape(source):
    assert filesystem_mutations(source)


def test_the_guards_stay_quiet_on_correct_code():
    """P7's second half, which is the half that keeps getting skipped.

    The fixture reaches the review queue in two import shapes, reads a file
    through both read primitives, and calls ``str.replace``, which is why
    ``replace`` is not in the mutation set. A guard that failed this module would
    be routed around within a week, and being routed around is the failure the
    guard exists to prevent.
    """
    assert forbidden_imports(CORRECT_MODULE, "cratekit.modules.reports.planted") == []
    assert filesystem_mutations(CORRECT_MODULE) == []


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
    it is the default for anyone who did not copy this author's library.
    """
    renamed = taxonomy.Node(id=INTAKE.id, display="Deep House")
    groupings = aging.intake_groupings(view, intake=renamed, today=TODAY)
    assert [group.path for group in groupings] == []
