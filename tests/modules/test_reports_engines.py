"""The two report engines: tree coverage and library statistics.

Kept apart from ``tests/modules/test_reports.py``, whose residual citation
floor is derived from another unit's commits. The documents are built with that
module's builders, never a second XML writer, and nothing here opens a database
or writes a file.
"""

from __future__ import annotations

from datetime import date

import pytest

from cratekit.core import taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.core.taxonomy import default_taxonomy
from cratekit.modules.reports import coverage, export
from cratekit.modules.reports import library as library_report
from tests.modules.test_reports import _close, _collection, _document, _folder, _playlist

TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))
TREE = default_taxonomy().tree
INTAKE = default_taxonomy().intake

#: Two declared buckets, looked up by id from the shipped template (R19).
DEEP = default_taxonomy().bucket("deep_house")
MELODIC = default_taxonomy().bucket("melodic_house")

#: One track with a readable head, for documents that need only one.
ONE = [(1, "08A - 124 - A", "X", "file://localhost/a.flac")]
#: A tree holding nothing.
EMPTY_TREE = (_folder(TREE.display, 0, 1), _close(1))


def _library(*, second_placement: bool = False, tree_present: bool = True) -> bytes:
    """Two genre folders, an intake flow, and four tracks: 1 filed under one
    genre, 2 under another, 3 only in intake, 4 nowhere. ``second_placement``
    files track 1 under the other genre too.
    """
    tracks = [
        (1, "08A - 124 - Cold Light", "Recondite", "file://localhost/library/a.flac"),
        (2, "05B - 120 - Other Thing", "Somebody", "file://localhost/library/b.flac"),
        (3, "11A - 126 - [MP3] Third", "Nobody", "file://localhost/library/c.flac"),
        (4, "no head at all", "Untagged", "file://localhost/library/d.flac"),
    ]
    melodic_ids = [2, 1] if second_placement else [2]
    tree_block = [
        _folder(TREE.display, 2, 1),
        _folder(DEEP.display, 1, 2),
        *_playlist("High", [1], 3),
        _close(2),
        _folder(MELODIC.display, 1, 2),
        *_playlist("Med", melodic_ids, 3),
        _close(2),
        _close(1),
    ]
    intake_block = [
        _folder(INTAKE.display, 1, 1),
        *_playlist("2026-06-15 bandcamp", [3], 2),
        _close(1),
    ]
    children = ([*tree_block, *intake_block]) if tree_present else intake_block
    return _document(
        collection=_collection(tracks),
        root_children=children,
        root_count=2 if tree_present else 1,
    )


def _view(tracks, *children) -> export.LibraryView:
    """The view of an export holding ``tracks`` under one root node."""
    return export.read_export(
        _document(collection=_collection(tracks), root_children=list(children), root_count=1)
    )


def _stats(view: export.LibraryView) -> library_report.LibraryStatistics:
    return library_report.statistics(view, declared=default_taxonomy(), template=TEMPLATE)


@pytest.fixture
def view() -> export.LibraryView:
    return export.read_export(_library())


# Coverage


def test_covered_and_uncovered_partition_the_collection(view):
    """Asserted over identifiers, since two counts that add up can hide a failure."""
    report = coverage.survey(view, tree=TREE)
    covered = {item.entry.track_id for item in report.covered}
    uncovered = {item.entry.track_id for item in report.uncovered}
    assert covered & uncovered == set()
    assert covered | uncovered == {entry.track_id for entry in view.entries}
    assert report.total == len(view.entries)


def test_a_track_only_in_the_intake_flow_or_in_no_playlist_is_uncovered(view):
    """Track 3 is where a fresh import leaves every track; track 4 is nowhere."""
    report = coverage.survey(view, tree=TREE)
    uncovered = {item.entry.track_id for item in report.uncovered}
    assert "3" in uncovered
    assert "3" not in {item.entry.track_id for item in report.covered}
    assert "4" in uncovered


def test_a_covered_track_names_every_path_under_the_tree_that_holds_it():
    """A track filed under two genres is one covered track and two placements."""
    report = coverage.survey(export.read_export(_library(second_placement=True)), tree=TREE)
    doubled = [item for item in report.covered if item.entry.track_id == "1"]
    assert len(doubled) == 1
    assert len(doubled[0].paths) == 2
    assert report.placements == len(report.covered) + 1


def test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything():
    """The refusal names the declared display, the string a person looks for."""
    with pytest.raises(CratekitError) as raised:
        coverage.survey(export.read_export(_library(tree_present=False)), tree=TREE)
    assert raised.value.cause.reason == "governed-tree-absent"
    assert raised.value.cause.detail["declared"] == TREE.display
    assert raised.value.cause.code is ExitCode.LIBRARY_PREREQUISITE


def test_a_tree_that_is_present_and_empty_reports_rather_than_refuses():
    """A present, empty tree is an unswept library: every entry is uncovered."""
    report = coverage.survey(
        _view([(1, "08A - 124 - A", "B", "file://localhost/a.flac")], *EMPTY_TREE), tree=TREE
    )
    assert len(report.uncovered) == 1
    assert report.covered == ()
    assert report.folders == ()


def test_a_tree_nested_inside_another_folder_is_still_the_governed_tree():
    nested = _view(
        [(1, "08A - 124 - A", "B", "file://localhost/a.flac")],
        _folder("Archive", 1, 1),
        _folder(TREE.display, 1, 2),
        *_playlist("High", [1], 3),
        _close(2),
        _close(1),
    )
    report = coverage.survey(nested, tree=TREE)
    assert [item.entry.track_id for item in report.covered] == ["1"]


def test_the_uncovered_list_is_ordered_BY_ARTIST_AND_NOT_BY_THE_WALK():
    """The collection DECLARES its entries in the reverse of the order the report
    must produce, so nothing but the sort can turn one into the other.
    """
    reversed_collection = _view(
        [
            (1, "05B - 120 - Zulu", "Yolanda", "file://localhost/a.flac"),
            (2, "05B - 120 - Yankee", "Xavier", "file://localhost/b.flac"),
            (3, "05B - 120 - Alpha", "Adele", "file://localhost/c.flac"),
        ],
        *EMPTY_TREE,
    )
    report = coverage.survey(reversed_collection, tree=TREE)
    assert [item.entry.artist for item in report.uncovered] == ["Adele", "Xavier", "Yolanda"]


def test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order():
    """The identifier is the third key, the tie break the pair above never reaches."""
    tied = _view(
        [
            (9, "05B - 120 - Same", "One", "file://localhost/b.flac"),
            (2, "05B - 120 - Same", "One", "file://localhost/a.flac"),
        ],
        *EMPTY_TREE,
    )
    report = coverage.survey(tied, tree=TREE)
    assert [item.entry.track_id for item in report.uncovered] == ["2", "9"]


def test_governed_paths_names_the_playlists_and_not_the_folders(view):
    """The folders hold no tracks, so a report over them would count nothing."""
    paths = coverage.governed_paths(view, tree=TREE)
    assert all(path[-1] in {"High", "Med"} for path in paths)
    assert len(paths) == 2


def test_a_folder_count_never_exceeds_what_the_collection_can_account_for():
    """A playlist may reference a track the collection lacks; the folder rows
    must still sum to the placement count printed beside them.
    """
    orphaned = _view(
        ONE,
        _folder(TREE.display, 1, 1),
        _folder(DEEP.display, 1, 2),
        *_playlist("High", [1, 999], 3),
        _close(2),
        _close(1),
    )
    report = coverage.survey(orphaned, tree=TREE)
    assert sum(held for _path, held in report.folders) == report.placements
    assert report.folders == ((("BY GENRE + ENERGY", "Deep House", "High"), 1),)


def test_two_playlists_sharing_a_display_path_add_up_rather_than_overwrite():
    """Driven on a view built directly, since whether rekordbox emits two siblings
    of one name is unmeasured; what it pins is that the rows sum to the placements.
    """
    entries = (
        export.CollectionEntry(track_id="1", name="A", artist="X", location="a"),
        export.CollectionEntry(track_id="2", name="B", artist="Y", location="b"),
    )
    path = (TREE.display, DEEP.display, "High")
    view = export.LibraryView(
        entries=entries,
        playlists=(
            export.Playlist(path=path, track_ids=("1",)),
            export.Playlist(path=path, track_ids=("2",)),
        ),
        folders=((TREE.display,), (TREE.display, DEEP.display)),
    )
    report = coverage.survey(view, tree=TREE)
    assert report.folders == ((path, 2),)
    assert sum(held for _path, held in report.folders) == report.placements


# Library statistics


def test_a_genre_counts_distinct_tracks_rather_than_summing_its_playlists():
    """One track in two energy bands of one genre is one track in that genre."""
    doubled = _view(
        [
            (1, "08A - 124 - A", "X", "file://localhost/a.flac"),
            (2, "05B - 120 - B", "Y", "file://localhost/b.flac"),
        ],
        _folder(TREE.display, 1, 1),
        _folder(DEEP.display, 2, 2),
        *_playlist("High", [1, 2], 3),
        *_playlist("Med", [1], 3),
        _close(2),
        _close(1),
    )
    row = next(one for one in _stats(doubled).genres if one.display == DEEP.display)
    assert row.tracks == 2, "the two playlists hold three memberships and two tracks"
    assert row.playlists == 2


def test_a_folder_the_taxonomy_does_not_declare_is_reported_and_not_refused():
    """Its row carries no bucket id, which puts it in ``gaps.undeclared_folders``."""
    undeclared = _view(
        ONE,
        _folder(TREE.display, 1, 1),
        _folder("Bootlegs", 1, 2),
        *_playlist("High", [1], 3),
        _close(2),
        _close(1),
    )
    stats = _stats(undeclared)
    assert [row.display for row in stats.genres] == ["Bootlegs"]
    assert stats.genres[0].bucket_id is None
    assert stats.gaps.undeclared_folders == (stats.genres[0].path,)


def test_a_declared_bucket_with_no_folder_is_a_gap(view):
    """Derived from the template, so the count moves with it."""
    stats = _stats(view)
    declared = {bucket.id for bucket in default_taxonomy().buckets}
    assert set(stats.gaps.unused_buckets) == declared - {DEEP.id, MELODIC.id}
    assert DEEP.id not in stats.gaps.unused_buckets


def test_the_tempo_spread_reads_a_marked_head_and_counts_what_it_could_not_read(view):
    """Track 3 carries the lossy marker and must parse; track 4 has no head."""
    stats = _stats(view)
    assert stats.tempo.readable == 3, "the marked head must parse"
    assert stats.tempo.unreadable == 1
    assert (stats.tempo.lowest, stats.tempo.highest) == (120.0, 126.0)
    assert stats.tempo.median == 124.0


def test_a_library_with_no_readable_head_reports_none_rather_than_zero():
    """Zero is a tempo a head can carry, so it cannot mean absent."""
    stats = _stats(_view([(1, "no head", "X", "file://localhost/a.flac")], *EMPTY_TREE))
    assert (stats.tempo.lowest, stats.tempo.highest, stats.tempo.median) == (None, None, None)
    assert (stats.tempo.readable, stats.tempo.unreadable) == (0, 1)


def test_a_tempo_median_over_an_even_population_averages_the_middle_pair():
    even = _view(
        [
            (1, "08A - 120 - A", "X", "file://localhost/a.flac"),
            (2, "08A - 124 - B", "X", "file://localhost/b.flac"),
            (3, "08A - 126 - C", "X", "file://localhost/c.flac"),
            (4, "08A - 130 - D", "X", "file://localhost/d.flac"),
        ],
        *EMPTY_TREE,
    )
    assert _stats(even).tempo.median == 125.0


def test_the_shape_measures_the_governed_tree_from_its_own_node(view):
    """Depth three is tree, folder, playlist, the fixture's deepest governed path."""
    stats = _stats(view)
    assert stats.shape.declared_depth == default_taxonomy().tree_depth
    assert stats.shape.deepest == 3
    assert not stats.shape.deeper_than_declared
    assert (stats.shape.folders, stats.shape.playlists) == (3, 2)


#: A genre with a sub folder, four deep: tree, genre, sub folder, playlist.
SUB_FOLDERED = (
    _folder(TREE.display, 1, 1),
    _folder(DEEP.display, 1, 2),
    _folder("Sub", 1, 3),
    *_playlist("High", [1], 4),
    _close(3),
    _close(2),
    _close(1),
)


def test_a_folder_below_a_genre_is_not_itself_a_genre():
    """A genre is a folder whose PARENT is the tree, not one anywhere beneath it."""
    stats = _stats(_view(ONE, *SUB_FOLDERED))
    assert [row.display for row in stats.genres] == [DEEP.display]
    assert "Sub" not in {row.display for row in stats.genres}


def test_a_tree_deeper_than_the_template_declares_is_reported_as_deeper():
    """The shape the XML bridge cannot write, known before a write is attempted."""
    stats = _stats(_view(ONE, *SUB_FOLDERED))
    assert stats.shape.deepest == 4
    assert stats.shape.deeper_than_declared


def test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder():
    """The archive's other children are not genres, and depth counts from the tree."""
    nested = _view(
        ONE,
        _folder("Archive", 2, 1),
        _folder(TREE.display, 1, 2),
        _folder(DEEP.display, 1, 3),
        *_playlist("High", [1], 4),
        _close(3),
        _close(2),
        _folder("Scratch", 0, 2),
        _close(2),
        _close(1),
    )
    stats = _stats(nested)
    assert [row.display for row in stats.genres] == [DEEP.display]
    assert stats.shape.deepest == 3, (
        "the depth is measured from the governed tree's own node, so a correctly "
        "shaped tree that somebody filed inside another folder is not deeper"
    )
    assert not stats.shape.deeper_than_declared


def test_the_gaps_count_entries_with_no_head_and_entries_in_no_playlist(view):
    """Two absences closed by two different acts, so two numbers."""
    stats = _stats(view)
    assert stats.gaps.entries_without_head == 1
    assert stats.gaps.entries_in_no_playlist == 1


def test_a_taxonomy_whose_tree_this_library_does_not_use_reports_no_genres():
    """Statistics do not refuse where coverage does: no folders is a true count."""
    stats = library_report.statistics(
        export.read_export(_library(tree_present=False)),
        declared=taxonomy.default_taxonomy(),
        template=TEMPLATE,
    )
    assert stats.genres == ()
    assert stats.shape.folders == 0
    assert stats.tree_display == TREE.display


def test_nothing_in_either_engine_needs_a_date_or_a_clock(view):
    """Both engines are pure functions of their arguments."""
    assert coverage.survey(view, tree=TREE) == coverage.survey(view, tree=TREE)
    assert _stats(view) == _stats(view)
    assert isinstance(date.today(), date)  # the module under test never asks this
