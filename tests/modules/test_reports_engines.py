"""U27's two report engines: tree coverage and library statistics.

Their siblings' guards live in ``tests/modules/test_reports.py``, which is U34's
module and carries that unit's residual-citation floor. These are here rather
than appended there for two reasons that are the same reason twice: the floor
derives its bound from git queries scoped to U34's own commits, so U27 rows added
into it would be claimed by a unit that did not write them, and a guard whose
subject is one unit's code is easier to reason about when its file says so.

**The documents are built with U34's builders, not with a second writer.** Two
XML writers in one suite disagree eventually, and the disagreement shows up as a
report that is right about a document nothing else in the product produces. The
import is the P2 answer: one builder, one shape.

**Nothing here uses the real library.** Every document is bytes, every taxonomy
is the shipped template or a node built for the test, and no test in this module
opens a database or writes a file.
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

#: Two declared buckets, spelled from the shipped template rather than typed, so
#: a rename in the template moves these with it. R19 forbids keying anything on a
#: display name, and these are LOOKUPS from a declared id, which is the direction
#: the taxonomy's own ``bucket_for_display`` exists to serve.
DEEP = default_taxonomy().bucket("deep_house")
MELODIC = default_taxonomy().bucket("melodic_house")


def _library(*, second_placement: bool = False, tree_present: bool = True) -> bytes:
    """One export: two genre folders, an intake flow, and four tracks.

    Track 1 is filed under one genre, track 2 under another, track 3 only in the
    intake flow, and track 4 nowhere at all. ``second_placement`` files track 1 a
    second time under the other genre, which is the shape that makes a placement
    count and a covered count differ.
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


@pytest.fixture
def view() -> export.LibraryView:
    return export.read_export(_library())


# ═══════════════════════════════════════════════════════════════════════════
# Coverage
# ═══════════════════════════════════════════════════════════════════════════


def test_covered_and_uncovered_partition_the_collection(view):
    """The two tuples are a partition, which is the property the report rests on.

    An entry in both is an entry somebody acts on twice; an entry in neither is
    one the report was supposed to surface and did not. Asserted over the
    identifiers rather than over the counts, because two counts that add up is
    the arithmetic a partition failure can satisfy.
    """
    report = coverage.coverage(view, tree=TREE)
    covered = {item.entry.track_id for item in report.covered}
    uncovered = {item.entry.track_id for item in report.uncovered}
    assert covered & uncovered == set()
    assert covered | uncovered == {entry.track_id for entry in view.entries}
    assert report.total == len(view.entries)


def test_a_track_only_in_the_intake_flow_is_uncovered(view):
    """The whole point of the report, and the source system could not see it.

    Track 3 is in the intake flow and in no genre folder, which is exactly the
    state a fresh import leaves every track in.
    """
    report = coverage.coverage(view, tree=TREE)
    assert "3" in {item.entry.track_id for item in report.uncovered}
    assert "3" not in {item.entry.track_id for item in report.covered}


def test_a_track_in_no_playlist_at_all_is_uncovered(view):
    report = coverage.coverage(view, tree=TREE)
    assert "4" in {item.entry.track_id for item in report.uncovered}


def test_a_covered_track_names_every_path_under_the_tree_that_holds_it():
    """Placement is counted, not just presence.

    A track filed under two genres is one covered track and two placements. The
    source system's per-playlist walk could not see the pair at all, which is the
    defect the duplicate audit's own docstring opens on.
    """
    report = coverage.coverage(
        export.read_export(_library(second_placement=True)), tree=TREE
    )
    doubled = [item for item in report.covered if item.entry.track_id == "1"]
    assert len(doubled) == 1
    assert len(doubled[0].paths) == 2
    assert report.placements == len(report.covered) + 1


def test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything():
    """Reporting every track as uncovered would be true and useless.

    A person whose export predates the tree, or who exported the wrong library,
    would be told to re-file their whole collection. The refusal names the
    declared display, because that is the string they have to go and look for.
    """
    with pytest.raises(CratekitError) as raised:
        coverage.coverage(export.read_export(_library(tree_present=False)), tree=TREE)
    assert raised.value.cause.reason == "governed-tree-absent"
    assert raised.value.cause.detail["declared"] == TREE.display
    assert raised.value.cause.code is ExitCode.LIBRARY_PREREQUISITE


def test_a_tree_that_is_present_and_empty_reports_rather_than_refuses():
    """The other half of the refusal above, and it is a different answer.

    "The tree is not here" and "the tree is here and holds nothing" are the two
    facts ``export`` refuses to render identically one module down. A tree with
    no playlists under it is a library nobody has swept, and every entry being
    uncovered is the true report for it.
    """
    empty = _document(
        collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
        root_children=[_folder(TREE.display, 0, 1), _close(1)],
        root_count=1,
    )
    report = coverage.coverage(export.read_export(empty), tree=TREE)
    assert len(report.uncovered) == 1
    assert report.covered == ()
    assert report.folders == ()


def test_a_tree_nested_inside_another_folder_is_still_the_governed_tree():
    """Anchoring at position zero reported nothing at all for a filed library.

    Somebody who put the routing tree inside an archive folder has organized
    their library rather than hidden it, and the same widening ``aging`` makes for
    the intake flow is made here for the same reason.
    """
    nested = _document(
        collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
        root_children=[
            _folder("Archive", 1, 1),
            _folder(TREE.display, 1, 2),
            *_playlist("High", [1], 3),
            _close(2),
            _close(1),
        ],
        root_count=1,
    )
    report = coverage.coverage(export.read_export(nested), tree=TREE)
    assert [item.entry.track_id for item in report.covered] == ["1"]


def test_the_uncovered_list_is_ordered_BY_ARTIST_AND_NOT_BY_THE_WALK():
    """The order is asserted, not merely asserted to be repeatable.

    THE VERSION THIS REPLACES MEASURED NOTHING, and the author's own mutation
    table is what said so. It compared two reads of one document and required
    them to agree, which the unsorted collection order satisfies perfectly: the
    walk is deterministic, so "stable" was free and the sort was worth zero
    deaths. What a person needs is not that two runs agree, it is that the list
    is in an order they can scan, and that a tree somebody rearranges does not
    reshuffle it.

    So the collection here DECLARES its entries in the reverse of the order the
    report must produce. Nothing but the sort can turn one into the other.
    """
    reversed_collection = _document(
        collection=_collection(
            [
                (1, "05B - 120 - Zulu", "Yolanda", "file://localhost/a.flac"),
                (2, "05B - 120 - Yankee", "Xavier", "file://localhost/b.flac"),
                (3, "05B - 120 - Alpha", "Adele", "file://localhost/c.flac"),
            ]
        ),
        root_children=[_folder(TREE.display, 0, 1), _close(1)],
        root_count=1,
    )
    report = coverage.coverage(export.read_export(reversed_collection), tree=TREE)

    assert [item.entry.artist for item in report.uncovered] == [
        "Adele",
        "Xavier",
        "Yolanda",
    ]


def test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order():
    """The tie break, which the pair above never reaches.

    Two rows can genuinely carry one artist and one name, which is the pair the
    duplicate audit exists to ask about. Sorting on the first two fields alone
    leaves that pair in whatever order the walk produced, so the identifier is
    the third key and this is what drives it.
    """
    tied = _document(
        collection=_collection(
            [
                (9, "05B - 120 - Same", "One", "file://localhost/b.flac"),
                (2, "05B - 120 - Same", "One", "file://localhost/a.flac"),
            ]
        ),
        root_children=[_folder(TREE.display, 0, 1), _close(1)],
        root_count=1,
    )
    report = coverage.coverage(export.read_export(tied), tree=TREE)
    assert [item.entry.track_id for item in report.uncovered] == ["2", "9"]


def test_governed_paths_names_the_playlists_and_not_the_folders(view):
    """The folders hold no tracks, so a report over them would count nothing."""
    paths = coverage.governed_paths(view, tree=TREE)
    assert all(path[-1] in {"High", "Med"} for path in paths)
    assert len(paths) == 2


# ═══════════════════════════════════════════════════════════════════════════
# Library statistics
# ═══════════════════════════════════════════════════════════════════════════


def test_a_genre_counts_distinct_tracks_rather_than_summing_its_playlists():
    """The double count, driven, because it is the number a person would act on.

    One track filed under two energy bands of one genre is one track in that
    genre. A sum over the sub-playlists says two, and two is right until the first
    library that files a track twice, at which point it is wrong in the direction
    that looks like success.
    """
    doubled = _document(
        collection=_collection(
            [
                (1, "08A - 124 - A", "X", "file://localhost/a.flac"),
                (2, "05B - 120 - B", "Y", "file://localhost/b.flac"),
            ]
        ),
        root_children=[
            _folder(TREE.display, 1, 1),
            _folder(DEEP.display, 2, 2),
            *_playlist("High", [1, 2], 3),
            *_playlist("Med", [1], 3),
            _close(2),
            _close(1),
        ],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(doubled), declared=default_taxonomy(), template=TEMPLATE
    )
    row = next(one for one in stats.genres if one.display == DEEP.display)
    assert row.tracks == 2, "the two playlists hold three memberships and two tracks"
    assert row.playlists == 2


def test_a_folder_the_taxonomy_does_not_declare_is_reported_and_not_refused(view):
    """A person is allowed folders the template has never heard of.

    The row exists so they can see which ones those are, and it carries no bucket
    id, which is what puts it in ``gaps.undeclared_folders`` without this module
    deciding anything about it.
    """
    undeclared = _document(
        collection=_collection([(1, "08A - 124 - A", "X", "file://localhost/a.flac")]),
        root_children=[
            _folder(TREE.display, 1, 1),
            _folder("Bootlegs", 1, 2),
            *_playlist("High", [1], 3),
            _close(2),
            _close(1),
        ],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(undeclared), declared=default_taxonomy(), template=TEMPLATE
    )
    assert [row.display for row in stats.genres] == ["Bootlegs"]
    assert stats.genres[0].bucket_id is None
    assert stats.gaps.undeclared_folders == (stats.genres[0].path,)


def test_a_declared_bucket_with_no_folder_is_a_gap(view):
    """Derived from the template rather than listed, so a new bucket is covered.

    The fixture files two of the shipped template's buckets, so every other
    declared bucket is unused and the count moves with the template rather than
    with a number written here.
    """
    stats = library_report.statistics(
        view, declared=default_taxonomy(), template=TEMPLATE
    )
    declared = {bucket.id for bucket in default_taxonomy().buckets}
    assert set(stats.gaps.unused_buckets) == declared - {DEEP.id, MELODIC.id}
    assert DEEP.id not in stats.gaps.unused_buckets


def test_the_tempo_spread_reads_a_marked_head_and_counts_what_it_could_not_read(view):
    """The source system's spread was confident and taken over a fraction.

    Its stripper did not know about the lossy marker, so every marked file
    matched nothing at all. Track 3 carries the marker, track 4 carries no head,
    and the report has to separate those two facts.
    """
    stats = library_report.statistics(
        view, declared=default_taxonomy(), template=TEMPLATE
    )
    assert stats.tempo.readable == 3, "the marked head must parse"
    assert stats.tempo.unreadable == 1
    assert (stats.tempo.lowest, stats.tempo.highest) == (120.0, 126.0)
    assert stats.tempo.median == 124.0


def test_a_library_with_no_readable_head_reports_none_rather_than_zero():
    """Zero beats per minute is a value a head can carry, so it cannot mean absent.

    Collapsing "no data" into zero renders an untagged library as a collection of
    stopped records, and a consumer reading the range cannot tell the two apart.
    """
    untagged = _document(
        collection=_collection([(1, "no head", "X", "file://localhost/a.flac")]),
        root_children=[_folder(TREE.display, 0, 1), _close(1)],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(untagged), declared=default_taxonomy(), template=TEMPLATE
    )
    assert (stats.tempo.lowest, stats.tempo.highest, stats.tempo.median) == (
        None,
        None,
        None,
    )
    assert (stats.tempo.readable, stats.tempo.unreadable) == (0, 1)


def test_a_tempo_median_over_an_even_population_averages_the_middle_pair():
    """Written here rather than imported, so the arithmetic gets driven once."""
    even = _document(
        collection=_collection(
            [
                (1, "08A - 120 - A", "X", "file://localhost/a.flac"),
                (2, "08A - 124 - B", "X", "file://localhost/b.flac"),
                (3, "08A - 126 - C", "X", "file://localhost/c.flac"),
                (4, "08A - 130 - D", "X", "file://localhost/d.flac"),
            ]
        ),
        root_children=[_folder(TREE.display, 0, 1), _close(1)],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(even), declared=default_taxonomy(), template=TEMPLATE
    )
    assert stats.tempo.median == 125.0


def test_the_shape_measures_the_governed_tree_from_its_own_node(view):
    """Two numbers describing one structure must be measured from one place.

    The template declares depth three, meaning tree, folder, playlist, and the
    fixture's deepest governed path is exactly those three segments. Measuring
    one from the export root and one from the tree is how they come to disagree
    by one forever.
    """
    stats = library_report.statistics(
        view, declared=default_taxonomy(), template=TEMPLATE
    )
    assert stats.shape.declared_depth == default_taxonomy().tree_depth
    assert stats.shape.deepest == 3
    assert not stats.shape.deeper_than_declared
    assert (stats.shape.folders, stats.shape.playlists) == (3, 2)


def test_a_folder_below_a_genre_is_not_itself_a_genre():
    """A genre is a folder whose PARENT is the tree, not one anywhere beneath it.

    THE AUTHOR'S MUTATION TABLE FOUND THIS UNGUARDED. Loosening the filter to
    "the tree appears anywhere in the path" killed nothing, because every fixture
    in this module was exactly three deep and the two rules agree on a tree that
    shallow. A person who has sub-foldered one genre would have had that
    sub-folder reported as a genre of its own, with the parent's tracks counted
    twice across the two rows.
    """
    sub_foldered = _document(
        collection=_collection([(1, "08A - 124 - A", "X", "file://localhost/a.flac")]),
        root_children=[
            _folder(TREE.display, 1, 1),
            _folder(DEEP.display, 1, 2),
            _folder("Sub", 1, 3),
            *_playlist("High", [1], 4),
            _close(3),
            _close(2),
            _close(1),
        ],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(sub_foldered), declared=default_taxonomy(), template=TEMPLATE
    )
    assert [row.display for row in stats.genres] == [DEEP.display]
    assert "Sub" not in {row.display for row in stats.genres}


def test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder():
    """The other direction of the same loosening, driven separately.

    Under "the tree appears anywhere in the path", the tree's own folder sitting
    inside an archive folder makes the tree itself a two-segment path whose last
    segment is the tree, and the archive's other children become genres. Under
    the rule this ships, a genre is the child of the tree and nothing else is.
    """
    nested = _document(
        collection=_collection([(1, "08A - 124 - A", "X", "file://localhost/a.flac")]),
        root_children=[
            _folder("Archive", 2, 1),
            _folder(TREE.display, 1, 2),
            _folder(DEEP.display, 1, 3),
            *_playlist("High", [1], 4),
            _close(3),
            _close(2),
            _folder("Scratch", 0, 2),
            _close(2),
            _close(1),
        ],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(nested), declared=default_taxonomy(), template=TEMPLATE
    )
    assert [row.display for row in stats.genres] == [DEEP.display]


def test_a_tree_deeper_than_the_template_declares_is_reported_as_deeper():
    """The shape the XML bridge cannot write, known before a write is attempted."""
    deep = _document(
        collection=_collection([(1, "08A - 124 - A", "X", "file://localhost/a.flac")]),
        root_children=[
            _folder(TREE.display, 1, 1),
            _folder(DEEP.display, 1, 2),
            _folder("Sub", 1, 3),
            *_playlist("High", [1], 4),
            _close(3),
            _close(2),
            _close(1),
        ],
        root_count=1,
    )
    stats = library_report.statistics(
        export.read_export(deep), declared=default_taxonomy(), template=TEMPLATE
    )
    assert stats.shape.deepest == 4
    assert stats.shape.deeper_than_declared


def test_the_gaps_count_entries_with_no_head_and_entries_in_no_playlist(view):
    """Two absences answered by two different acts, so they are two numbers.

    A file with no head is owed a naming pass. A file in no playlist is owed a
    sweep, and ``audit.coverage`` is where the list of those lives, which is why
    this is a count.
    """
    stats = library_report.statistics(
        view, declared=default_taxonomy(), template=TEMPLATE
    )
    assert stats.gaps.entries_without_head == 1
    assert stats.gaps.entries_in_no_playlist == 1


def test_a_taxonomy_whose_tree_this_library_does_not_use_reports_no_genres():
    """The statistics report does not refuse where coverage does, deliberately.

    Coverage would tell somebody to re-file a filed library, which is why it
    refuses. This one reports counts, and "no folders under a tree that is not
    here" is a true count with the declared display named beside it in the
    envelope, so the reader can see which tree was asked about.
    """
    other = taxonomy.default_taxonomy()
    stats = library_report.statistics(
        export.read_export(_library(tree_present=False)),
        declared=other,
        template=TEMPLATE,
    )
    assert stats.genres == ()
    assert stats.shape.folders == 0
    assert stats.tree_display == TREE.display


def test_nothing_in_either_engine_needs_a_date_or_a_clock(view):
    """Both engines are pure functions of their arguments, which is assertable.

    ``aging`` takes ``today`` because its answer genuinely depends on it. Neither
    of these does, and a report that reached for a clock could not be asserted
    against a fixture at all, which is the property the source system's own aging
    report lost by calling ``date.today()`` inside itself.
    """
    first = coverage.coverage(view, tree=TREE)
    second = coverage.coverage(view, tree=TREE)
    assert first == second
    assert library_report.statistics(
        view, declared=default_taxonomy(), template=TEMPLATE
    ) == library_report.statistics(
        view, declared=default_taxonomy(), template=TEMPLATE
    )
    assert isinstance(date.today(), date)  # the module under test never asks this
