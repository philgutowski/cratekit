"""R-797: the report that names a genre which has outgrown having no folder.

``crate report genres`` counts the live collection by genre, names every genre
holding fifty or more tracks that no top level folder answers for, and creates
nothing. The resolver's answer is held first, then the count, then the verb
through the real dispatcher against a disposable library, with every file
under the library root compared byte for byte across the run.

Every folder and sub is derived from the shipped taxonomy's declarations. The
genre words that nothing claims are made up, and are checked to be unclaimed.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.adopt import genres as adopt_genres
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import registry
from cratekit.core import config, jobs, routing, taxonomy
from cratekit.core.exit_codes import ExitCode
from tests import adopt_fixtures
from tests.cli_drive import drive, drive_human
from tests.test_adopt_workers import (  # noqa: F401
    _platform_seams,
    _reader_cache,
    _release_process_locks,
    library,
    machine,
)

DECLARED = taxonomy.default_taxonomy()
VERB = ["report", "genres"]

#: The folder that routes by source genre, and one of its style subs with the
#: source strings its map files there.
STYLE = next(bucket for bucket in DECLARED.buckets if bucket.sub_by_source is not None)
DEFAULT_SUB = next(sub for sub in STYLE.subs if sub.id == STYLE.sub_by_source.default)
#: A style sub two source strings file under, so one genre has two spellings.
SHARED_SUB = DEFAULT_SUB
SHARED_SOURCES = sorted(
    source for source, sub in STYLE.sub_by_source.map.items() if sub == SHARED_SUB.id
)
OWN = next(
    bucket for bucket in DECLARED.buckets if bucket.sub_by_source is None and bucket.energy.enabled
)

#: A word no alias, no bucket name and no keyword rule claims.
UNCLAIMED = "Zydeco"
#: A word a keyword rule sends to the source routed folder, with no map row.
DEFAULTED = next(
    f"New {rule.keyword.title()}"
    for rule in DECLARED.fuzzy
    if rule.bucket == STYLE.id
)


def _rows(*genres: tuple[str, int], deleted: tuple[str, int] | None = None):
    rows = []
    for genre, how_many in genres:
        rows.extend(
            adopt_scan.CollectionRow(
                content_id=f"{genre or 'none'}-{index}",
                recorded=f"/library/Music/{genre or 'none'}-{index}.flac",
                genre=genre,
                deleted=False,
            )
            for index in range(how_many)
        )
    if deleted is not None:
        genre, how_many = deleted
        rows.extend(
            adopt_scan.CollectionRow(
                content_id=f"gone-{index}", recorded="", genre=genre, deleted=True
            )
            for index in range(how_many)
        )
    return rows


# ── what a genre has in the tree ───────────────────────────────────────────


def test_the_fixture_words_are_what_they_claim_to_be():
    assert len(SHARED_SOURCES) >= 2
    assert routing.resolve_bucket(DECLARED, UNCLAIMED).match is routing.Match.FALLBACK
    assert routing.resolve_bucket(DECLARED, DEFAULTED).match is routing.Match.FUZZY
    assert DEFAULTED not in STYLE.sub_by_source.map


def test_a_genre_a_top_level_folder_answers_for_has_a_folder_of_its_own():
    for genre in (OWN.display, *OWN.aliases):
        assert routing.folder_of(DECLARED, genre) == routing.GenreFolder(
            routing.Folder.OWN, OWN.id
        ), genre


def test_a_source_string_filed_in_a_style_sub_has_no_folder_of_its_own():
    for source in SHARED_SOURCES:
        assert routing.folder_of(DECLARED, source) == routing.GenreFolder(
            routing.Folder.SUB, STYLE.id, SHARED_SUB.id
        ), source


def test_a_word_that_lands_in_a_default_sub_is_not_that_subs_genre():
    assert routing.folder_of(DECLARED, DEFAULTED) == routing.GenreFolder(
        routing.Folder.DEFAULT, STYLE.id, STYLE.sub_by_source.default
    )


def test_the_source_routed_folders_own_name_has_that_folder():
    """The tagger writes the folder's name onto a file, and a track carrying it
    has a top level folder by name whatever sub it sits in."""
    assert routing.folder_of(DECLARED, STYLE.display).kind is routing.Folder.OWN


def test_a_word_nothing_declared_claims_has_no_folder_at_all():
    found = routing.folder_of(DECLARED, UNCLAIMED)
    assert found.kind is routing.Folder.NONE and found.sub_id is None


def test_every_declared_alias_of_a_bucket_that_splits_by_energy_has_its_folder():
    """The promoted bucket included: once a genre has a folder it is not named."""
    for bucket in DECLARED.buckets:
        if bucket.sub_by_source is not None:
            continue
        for alias in bucket.aliases:
            assert routing.folder_of(DECLARED, alias).kind is routing.Folder.OWN, alias


# ── the count ──────────────────────────────────────────────────────────────


def test_ae8_a_style_sub_at_109_is_named_with_109():
    report = adopt_genres.count(_rows((SHARED_SUB.display, 109)), DECLARED)
    (named,) = report.named
    assert (named.name, named.tracks) == (SHARED_SUB.display, 109)
    assert named.filed_under == (STYLE.display, SHARED_SUB.display)
    assert (report.tracks, report.with_folder, report.without_folder) == (109, 0, 109)


def test_a_genre_at_49_is_counted_and_not_named_and_one_at_50_is_named():
    report = adopt_genres.count(
        _rows((SHARED_SOURCES[0], 50), (UNCLAIMED, 49)), DECLARED
    )
    assert adopt_genres.FOLDER_WORTH == 50
    assert [(genre.name, genre.tracks) for genre in report.named] == [(SHARED_SUB.display, 50)]
    assert [(genre.name, genre.tracks) for genre in report.genres] == [
        (SHARED_SUB.display, 50),
        (UNCLAIMED, 49),
    ]


def test_the_boundary_is_the_same_on_both_sides_of_one_genre():
    assert adopt_genres.count(_rows((UNCLAIMED, 49)), DECLARED).named == ()
    (named,) = adopt_genres.count(_rows((UNCLAIMED, 50)), DECLARED).named
    assert named.tracks == 50


def test_a_genre_no_folder_claims_at_all_is_counted_under_its_own_word():
    (found,) = adopt_genres.count(_rows((UNCLAIMED, 60)), DECLARED).named
    assert (found.name, found.kind, found.bucket, found.sub, found.filed_under) == (
        UNCLAIMED, routing.Folder.NONE.value, "", "", None
    )


def test_the_strings_one_style_sub_holds_are_one_genre_with_its_sources_listed():
    first, second = SHARED_SOURCES[0], SHARED_SOURCES[1]
    (found,) = adopt_genres.count(_rows((first, 30), (second, 25)), DECLARED).named
    assert (found.name, found.tracks) == (SHARED_SUB.display, 55)
    assert found.sources == ((first, 30), (second, 25))


def test_a_word_in_a_default_sub_is_counted_apart_from_that_subs_own_genre():
    report = adopt_genres.count(
        _rows((SHARED_SOURCES[0], 40), (DEFAULTED, 40)), DECLARED
    )
    assert report.named == ()
    assert {(genre.name, genre.kind, genre.tracks) for genre in report.genres} == {
        (SHARED_SUB.display, routing.Folder.SUB.value, 40),
        (DEFAULTED, routing.Folder.DEFAULT.value, 40),
    }
    defaulted = next(g for g in report.genres if g.kind == routing.Folder.DEFAULT.value)
    assert defaulted.filed_under == (STYLE.display, DEFAULT_SUB.display)


def test_another_spelling_of_a_style_subs_own_name_is_counted_with_it():
    """Found by the review, with these numbers. Routing matches a source
    string exactly, so the lowercase spelling lands in a default sub or
    nowhere, and counted apart neither row reached a threshold the genre had
    passed."""
    lowered = SHARED_SUB.display.lower()
    assert lowered != SHARED_SUB.display
    assert routing.folder_of(DECLARED, lowered).kind is not routing.Folder.SUB
    report = adopt_genres.count(_rows((SHARED_SUB.display, 45), (lowered, 10)), DECLARED)
    (found,) = report.named
    assert (found.name, found.tracks, found.kind) == (
        SHARED_SUB.display, 55, routing.Folder.SUB.value
    )
    assert found.sources == ((SHARED_SUB.display, 45), (lowered, 10))
    assert len(report.genres) == 1
    # THE ROW DOES NOT SAY ROUTING FILES THE OTHER SPELLING THERE. Found by
    # the second review: it said so, and a person looking found none of them.
    assert (found.strays, found.not_filed_there) == ((lowered,), 10)
    assert "except 10 under another spelling" in adopt_genres.where(found)
    row = adopt_genres.row_json(found)
    assert row["not_filed_there"] == 10
    assert [(s["genre"], s["filed_there"]) for s in row["sources"]] == [
        (SHARED_SUB.display, True),
        (lowered, False),
    ]


def test_a_genre_filed_whole_in_its_sub_names_no_other_spelling():
    (found,) = adopt_genres.count(_rows((SHARED_SUB.display, 50)), DECLARED).named
    assert (found.strays, found.not_filed_there) == ((), 0)
    assert "except" not in adopt_genres.where(found)


def test_another_spelling_of_a_source_string_is_counted_with_its_sub():
    source = next(s for s in SHARED_SOURCES if s != SHARED_SUB.display)
    report = adopt_genres.count(_rows((source, 30), (source.upper(), 20)), DECLARED)
    (found,) = report.named
    assert (found.name, found.tracks) == (SHARED_SUB.display, 50)


def test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre():
    """A sub whose lowercase name no keyword rule claims falls to the fallback,
    and is the sub's genre all the same."""
    unrouted = next(
        sub
        for sub in STYLE.subs
        if routing.folder_of(DECLARED, sub.display.lower()).kind is routing.Folder.NONE
    )
    (found,) = adopt_genres.count(_rows((unrouted.display.lower(), 50)), DECLARED).named
    assert (found.name, found.kind, found.filed_under) == (
        unrouted.display, routing.Folder.SUB.value, (STYLE.display, unrouted.display)
    )


def test_two_spellings_of_one_unclaimed_word_are_one_genre():
    (found,) = adopt_genres.count(
        _rows((UNCLAIMED, 30), (UNCLAIMED.lower(), 25)), DECLARED
    ).named
    assert (found.name, found.tracks) == (UNCLAIMED, 55)
    assert dict(found.sources) == {UNCLAIMED: 30, UNCLAIMED.lower(): 25}


def test_a_genre_with_a_folder_is_never_named_however_many_tracks_it_holds():
    report = adopt_genres.count(_rows((OWN.display, 500)), DECLARED)
    assert report.genres == () and report.with_folder == 500


def test_tracks_with_no_genre_are_counted_apart_and_never_named():
    report = adopt_genres.count(_rows(("", 70), ("   ", 5)), DECLARED)
    assert (report.no_genre, report.genres, report.named) == (75, (), ())


def test_a_word_the_taxonomy_calls_too_coarse_is_counted_apart_as_adoption_reads_it():
    """Found by the second review. Routing sends such a word to the catch all
    bucket by an alias, and adoption files none of those tracks."""
    coarse = next(word for word in DECLARED.fallback.too_coarse_as_source if word)
    assert routing.folder_of(DECLARED, coarse).kind is routing.Folder.OWN
    assert adopt_scan.classify_genre(DECLARED, coarse)[0] is adopt_scan.Disposition.NEEDS_GENRE
    report = adopt_genres.count(_rows((coarse, 200), (OWN.display, 3)), DECLARED)
    assert (report.too_coarse, report.with_folder, report.genres) == (200, 3, ())


def test_a_removed_row_is_not_counted():
    report = adopt_genres.count(
        _rows((UNCLAIMED, 49), deleted=(UNCLAIMED, 10)), DECLARED
    )
    assert report.tracks == 49 and report.named == ()


def test_every_live_track_is_counted_exactly_once():
    coarse = next(word for word in DECLARED.fallback.too_coarse_as_source if word)
    report = adopt_genres.count(
        _rows((OWN.display, 7), (SHARED_SOURCES[0], 5), (UNCLAIMED, 3), ("", 2), (coarse, 4)),
        DECLARED,
    )
    assert report.tracks == 21
    assert (report.with_folder, report.without_folder, report.no_genre, report.too_coarse) == (
        7, 8, 2, 4
    )


def test_the_order_is_largest_first_then_by_name():
    report = adopt_genres.count(
        _rows(("Bravo Word", 3), ("Alpha Word", 3), (UNCLAIMED, 9)), DECLARED
    )
    assert [genre.name for genre in report.genres] == [UNCLAIMED, "Alpha Word", "Bravo Word"]


def test_the_promoted_genre_is_not_named_once_it_has_its_folder():
    """R&B at 200 tracks is the case this report would have named before."""
    promoted = next(bucket for bucket in DECLARED.buckets if bucket.formerly)
    report = adopt_genres.count(
        _rows(*((alias, 50) for alias in promoted.aliases)), DECLARED
    )
    assert report.named == () and report.with_folder == 50 * len(promoted.aliases)


# ── the verb ───────────────────────────────────────────────────────────────


def _tracks(*genres: tuple[str, int]) -> tuple[adopt_fixtures.Track, ...]:
    return tuple(
        adopt_fixtures.Track(f"{genre or 'none'}-{index}", f"g{order}-{index}.flac", genre, on_disk=False)
        for order, (genre, how_many) in enumerate(genres)
        for index in range(how_many)
    )


def _snapshot(root: Path) -> dict[str, str]:
    """Every file under the library root, by its bytes."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


@pytest.fixture
def counted(machine):  # noqa: F811
    """A library holding one genre over the threshold with no folder of its own."""
    adopt_fixtures.build(
        machine,
        _tracks(
            (SHARED_SUB.display, 109),
            (UNCLAIMED, 49),
            (OWN.display, 3),
            ("", 2),
        ),
    )
    collection.reset_cache()
    return machine


def test_ae8_the_verb_names_the_genre_with_its_count_and_the_library_is_unchanged(counted):
    root = Path(counted.library.root)
    before = _snapshot(root)
    assert before, "the fixture wrote no library to compare"

    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["threshold"], summary["named"]) == (50, 1)
    # The two baseline rows every disposable database carries have no genre.
    assert (summary["tracks"], summary["with_folder"], summary["without_folder"]) == (
        163 + len(adopt_fixtures.BASELINE_CONTENT_IDS), 3, 158
    )
    assert summary["no_genre"] == 2 + len(adopt_fixtures.BASELINE_CONTENT_IDS)
    assert summary["too_coarse"] == 0
    (check,) = envelope["data"]["checks"]
    assert (check["title"], check["status"], check["remedy"]) == (
        SHARED_SUB.display, "info", None
    )
    assert "109 tracks" in check["detail"]
    assert f"{STYLE.display} / {SHARED_SUB.display}" in check["detail"]
    assert [(row["genre"], row["tracks"]) for row in summary["genres"]] == [
        (SHARED_SUB.display, 109),
        (UNCLAIMED, 49),
    ]

    # R10: IT CREATES NOTHING. Not a tree node, not a state file, not a job.
    assert _snapshot(root) == before
    assert not config.state_path("genre_gaps", counted).exists()
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 0


def test_a_person_reading_the_report_is_shown_the_genre_and_its_count(counted):
    code, text = drive_human(VERB)
    assert code == int(ExitCode.OK), text
    assert SHARED_SUB.display in text and "109 tracks" in text


def test_with_nothing_at_the_threshold_the_report_says_so_in_a_row(machine):  # noqa: F811
    adopt_fixtures.build(machine, _tracks((UNCLAIMED, 49), (OWN.display, 3)))
    collection.reset_cache()
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    (check,) = envelope["data"]["checks"]
    assert check["status"] == "info" and "none holds 50" in check["detail"]
    assert envelope["data"]["summary"]["named"] == 0
    assert [row["tracks"] for row in envelope["data"]["summary"]["genres"]] == [49]


def test_the_verb_declares_no_write_and_no_gate():
    entry = registry.entry("report.genres")
    assert entry.writes == frozenset() and entry.gates == ()
    assert not entry.destructive and not entry.long_running
    assert entry.emits == frozenset({"diagnostic"})


def test_the_summary_a_person_reads_in_help_states_the_threshold_the_code_uses():
    """The registry cannot import the engine's constant, so the two are held
    together here."""
    summary = registry.entry("report.genres").summary
    assert f"{adopt_genres.FOLDER_WORTH} or more tracks" in summary
