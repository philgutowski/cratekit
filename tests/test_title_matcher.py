"""R-1534: a title that strips to nothing never matches, in every source.

THE DEFECT. The shared matcher strips a trailing bracket from the first "(" to
the last ")", so a title that starts and ends with a bracket, "(Intro)" or
"(Not Just) Knee Deep (Part 1)", strips to the empty string, which is a
substring of every title. Any row by the artist then matched, and its genre was
written onto the file for good, since a genre is fill if empty. Beatport scored
its rows on the same strip, the two scraped parsers read the shared matcher,
and Discogs carried its own guard since U244.

WHAT HOLDS NOW. A side with no letter or digit matches nothing. A title the
strip empties is read by its core: the leading bracket groups and the text
after them, or for a title of brackets alone, the groups' words, compared
exactly. A title made only of version words ("Original Mix", "Dub") is never
read as contained in another title's bracketed suffix, and still finds its own
row ("Original" in "Original feat. Someone"). A title that matched its own
row before still does, which the tables below drive on every source. The kind
known lost is a title of brackets alone, or one opening with bracket groups,
against a row that differs by more than its brackets ("(Intro)" against
"Intro feat. X"), which the base matched only because it matched every row,
and which is a residual. Two ordinary titles still match by raw substring
between their cores ("Club" in "Nightclub"), as they did before; that is a
residual too, and pinned below as known so a change to it is seen.

NOTHING HERE OPENS A SOCKET. Pages are synthetic text in the shapes the
parsers read, handed to the injected fetch seam.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core import tags
from cratekit.tagging import searchers, tag
from tests._containers import synth_container
from tests.test_catalogue_searcher import (
    ARTIST,
    BANDCAMP_TRACK_URL,
    BUCKET_GENRE,
    _all_three,
    _bandcamp_search_page,
    _beatport_page,
    _beatport_track,
    _searcher,
    _traxsource_page,
)
from tests.test_discogs_searcher import discogs_answer, release, results, routed, searcher

OTHER = "Sunrise Mood"
BRACKETED = "(Not Just) Knee Deep (Part 1)"

#: Titles nothing can be read off: empty, blank, punctuation, empty brackets.
NOISE = ("", "   ", "-", "...", "()", "( )", "!?", "___")


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


# ---------------------------------------------------------------------------
# A. The shared matcher, both ways round
# ---------------------------------------------------------------------------


#: (searched, found) pairs that name the same recording and must match.
SAME = [
    ("Sunrise Mood", "Sunrise Mood"),
    ("Sunrise Mood", "Sunrise Mood (Extended Mix)"),
    ("Sunrise Mood (Extended Mix)", "Sunrise Mood"),
    ("Sunrise Mood (Original Mix)", "Sunrise Mood (Extended Mix)"),
    ("Sunrise Mood", "SUNRISE MOOD"),
    ("Sunrise Mood feat. Someone", "Sunrise Mood"),
    ("Sunrise Mood", "Sunrise Mood feat. Someone (Club Mix)"),
    ("Sunrise Mood (feat. Someone) (Extended Mix)", "Sunrise Mood"),
    (BRACKETED, BRACKETED),
    (BRACKETED, "(Not Just) Knee Deep"),
    (BRACKETED, "(Not Just) Knee Deep (Part 1) (Extended Mix)"),
    (BRACKETED, "Not Just Knee Deep"),
    ("(Foo) Bar (feat. X) (Extended Mix)", "(Foo) Bar"),
    ("(Intro)", "(Intro)"),
    ("(Intro)", "Intro"),
    ("(Intro)", "Intro (Original Mix)"),
    ("(Intro) (Extended Mix)", "(Intro)"),
    ("(Love) (Is) The Message (Extended Mix)", "(Love) (Is) The Message feat. X"),
    ("Dub", "Dub"),
    ("Dub", "Dub (Original Mix)"),
    ("Original Mix", "Original Mix"),
    ("Original feat. Toni Halliday", "Original"),
    ("Radio - Radio Edit", "Radio"),
    ("Club!", "Club"),
    ("Dub", "Dub - 2014 Remaster"),
    ("VIP", "VIP."),
    ("Version feat. Someone", "Version"),
]

#: (searched, found) pairs that name different recordings and must not match.
DIFFERENT = [
    ("(Intro)", OTHER),
    ("(Intro)", "Introspection"),
    ("(Intro)", "Intro Theme"),
    ("(Skit)", OTHER),
    (BRACKETED, OTHER),
    (BRACKETED, "Maggot Brain"),
    ("(Intro) (Extended Mix)", OTHER),
    ("Original Mix", f"{OTHER} (Original Mix)"),
    ("Extended Mix", f"{OTHER} (Extended Mix)"),
    ("Mix", f"{OTHER} (Original Mix)"),
    ("Remix", f"{OTHER} (Kerri Chandler Remix)"),
    ("(Intro)", f"{OTHER} (Intro)"),
    (f"{OTHER} (Dub)", "Dub"),
    ("- (Intro)", "- (Outro)"),
]


@pytest.mark.parametrize(("searched", "found"), SAME)
def test_a_title_matches_its_own_recording_either_way_round(searched, found):
    assert searchers._title_matches(searched, found)
    assert searchers._title_matches(found, searched)


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_a_title_matches_no_other_recording_either_way_round(searched, found):
    assert not searchers._title_matches(searched, found)
    assert not searchers._title_matches(found, searched)


@pytest.mark.parametrize("noise", NOISE)
@pytest.mark.parametrize("other", [OTHER, "(Intro)", BRACKETED, "Original Mix", "-"])
def test_a_title_with_no_letter_or_digit_matches_nothing(noise, other):
    assert not searchers._title_matches(noise, other)
    assert not searchers._title_matches(other, noise)


@pytest.mark.parametrize("noise", NOISE)
def test_a_title_with_no_letter_or_digit_does_not_match_itself(noise):
    """Nothing identifies the recording, so even an identical row is no match."""
    assert not searchers._title_matches(noise, noise)


# ---------------------------------------------------------------------------
# B. Beatport, which scores its rows rather than asking the shared matcher
# ---------------------------------------------------------------------------


def _beatport_hit(title: str, rows: list[dict]):
    fetch = _all_three(beatport=_beatport_page(rows), traxsource="", bandcamp="")
    return _searcher(fetch)(ARTIST, title)


def _beatport_answer(hit) -> str:
    (one,) = [entry for entry in hit.answers if entry.source == searchers.BEATPORT]
    return one.answer


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_beatport_writes_no_genre_off_another_track_by_the_artist(searched, found):
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE)])
    assert _beatport_answer(hit) == "miss"
    assert hit.genre is None


@pytest.mark.parametrize("noise", NOISE)
def test_beatport_scores_no_row_for_a_title_with_no_letter_or_digit(noise):
    rows = [
        _beatport_track(ARTIST, OTHER, BUCKET_GENRE),
        _beatport_track(ARTIST, noise, BUCKET_GENRE),
    ]
    assert _beatport_answer(_beatport_hit(noise, rows)) == "miss"


@pytest.mark.parametrize("noise", NOISE)
def test_beatport_passes_over_a_row_whose_name_has_no_letter_or_digit(noise):
    rows = [_beatport_track(ARTIST, noise, BUCKET_GENRE, mix="Original Mix")]
    assert _beatport_answer(_beatport_hit(OTHER, rows)) == "miss"


@pytest.mark.parametrize(
    ("searched", "name", "mix"),
    [
        (OTHER, OTHER, ""),
        (f"{OTHER} (Extended Mix)", OTHER, "Extended Mix"),
        (f"{OTHER} (Original Mix)", OTHER, "Extended Mix"),
        (f"{OTHER} feat. Someone", OTHER, "Original Mix"),
        (BRACKETED, "(Not Just) Knee Deep", "Part 1"),
        (BRACKETED, "Not Just Knee Deep", "Original Mix"),
        ("(Intro)", "Intro", "Original Mix"),
        ("Dub", "Dub", "Original Mix"),
        ("Original feat. Toni Halliday", "Original", "Original Mix"),
        ("Radio - Radio Edit", "Radio", "Original Mix"),
    ],
)
def test_beatport_still_matches_a_title_to_its_own_row(searched, name, mix):
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE, mix=mix)])
    assert hit.genre == BUCKET_GENRE
    assert hit.source == searchers.BEATPORT


def test_beatport_prefers_its_own_row_over_another_by_the_artist():
    rows = [
        _beatport_track(ARTIST, OTHER, "Techno"),
        _beatport_track(ARTIST, "Intro", BUCKET_GENRE, mix="Original Mix"),
    ]
    assert _beatport_hit("(Intro)", rows).genre == BUCKET_GENRE


def test_beatport_never_lets_a_short_row_name_outscore_the_files_own_row():
    """Round two's BLOCKING: a row named "Love (feat. X)" has the core "love",
    and a middle tier on cores scored it level with the file's own row, so page
    order wrote the first row's genre."""
    rows = [
        _beatport_track(ARTIST, "Love (feat. X)", "Techno"),
        _beatport_track(ARTIST, "Love Is The Message", BUCKET_GENRE),
    ]
    assert _beatport_hit("Love Is The Message - Original Mix", rows).genre == BUCKET_GENRE
    shout = [
        _beatport_track(ARTIST, "Shout (Part 1)", "Techno"),
        _beatport_track(ARTIST, "Shout It Out", BUCKET_GENRE),
    ]
    assert _beatport_hit("Shout It Out feat. Y", shout).genre == BUCKET_GENRE


@pytest.mark.parametrize(
    ("searched", "name"),
    [
        ("Love Me Again", "Love (feat. X)"),
        ("Track Two", "Track (Interlude)"),
        ("Intro Music", "(Intro)"),
        ("Mix", f"{OTHER} (Original Mix)"),
    ],
)
def test_beatport_scores_no_row_by_a_part_of_its_name(searched, name):
    assert _beatport_answer(_beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE)])) == "miss"


@pytest.mark.parametrize(
    ("searched", "name"),
    [
        ("Knee Deep", "(Not Just) Knee Deep"),
        ("How Does It Feel", "Untitled (How Does It Feel)"),
        ("Dub", "Dub (Original Mix)"),
    ],
)
def test_beatport_still_finds_a_title_inside_its_rows_name(searched, name):
    assert _beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE)]).genre == BUCKET_GENRE


@pytest.mark.parametrize(
    ("searched", "found"),
    [("Club", "Nightclub"), ("Dub", "Dub Siren"), ("Remix", f"{OTHER} Remix")],
)
def test_two_cores_still_match_by_raw_substring_as_before_a_known_residual(searched, found):
    """Not a property to keep: the looseness the base had between two ordinary
    titles, filed as a residual at R-1534. Pinned so a fix to it is seen."""
    assert searchers._title_matches(searched, found)


def test_beatport_reads_no_artist_from_a_row_crediting_an_empty_name():
    """The same empty substring on the artist side: a credit with no name was
    read as contained in every searched artist."""
    row = _beatport_track("", OTHER, BUCKET_GENRE)
    assert _beatport_answer(_beatport_hit(OTHER, [row])) == "miss"


# ---------------------------------------------------------------------------
# C. The scraped parsers, which read the shared matcher
# ---------------------------------------------------------------------------


def _traxsource_hit(title: str, found: str):
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([(ARTIST, found, BUCKET_GENRE)]),
        bandcamp="",
    )
    return _searcher(fetch)(ARTIST, title)


def _bandcamp_hit(title: str, heading: str):
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([(BANDCAMP_TRACK_URL, heading, ARTIST, BUCKET_GENRE)]),
    )
    return _searcher(fetch)(ARTIST, title)


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_traxsource_writes_no_genre_off_another_track_by_the_artist(searched, found):
    assert _traxsource_hit(searched, found).genre is None


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_bandcamp_writes_no_genre_off_another_track_by_the_artist(searched, found):
    assert _bandcamp_hit(searched, found).genre is None
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre is None


@pytest.mark.parametrize(("searched", "found"), SAME)
def test_the_scraped_parsers_still_match_a_title_to_its_own_row(searched, found):
    trax = _traxsource_hit(searched, found)
    assert (trax.genre, trax.source) == (BUCKET_GENRE, searchers.TRAXSOURCE)
    band = _bandcamp_hit(searched, f"{ARTIST} - {found}")
    assert (band.genre, band.source) == (BUCKET_GENRE, searchers.BANDCAMP)


# ---------------------------------------------------------------------------
# D. Discogs, moved onto the shared matcher
# ---------------------------------------------------------------------------


def _discogs_hit(title: str, track: str):
    tracks = [{"position": "A1", "type_": "track", "title": track}]
    fetch = routed(search=results(41), releases={41: release(41, tracks=tracks)})
    return searcher(fetch)(ARTIST, title)


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_discogs_writes_no_style_off_another_track_by_the_artist(searched, found):
    hit = _discogs_hit(searched, found)
    assert discogs_answer(hit).answer == "miss"
    assert hit.genre is None


@pytest.mark.parametrize(("searched", "found"), SAME)
def test_discogs_still_matches_a_title_to_its_own_track(searched, found):
    assert discogs_answer(_discogs_hit(searched, found)).answer == "matched"


def test_discogs_reads_no_single_whose_title_is_noise():
    fetch = routed(
        search=results(42),
        releases={42: release(42, title="()", tracks=[])},
    )
    assert discogs_answer(searcher(fetch)(ARTIST, OTHER)).answer == "miss"


# ---------------------------------------------------------------------------
# E. The write itself, driven through tag_one as the review drove it
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("title", ["(Intro)", BRACKETED, "(Intro) (Extended Mix)"])
def test_a_file_titled_in_brackets_takes_no_genre_off_another_track(tmp_path, silence, title):
    """B1 of R-1534, as U244's review drove it: the genre was written for good."""
    path = tmp_path / "a.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": title})
    beatport = searchers.Fetched(
        text=_beatport_page([_beatport_track(ARTIST, OTHER, BUCKET_GENRE, mix="Original Mix")]),
        status=200,
    )
    tracks = [{"position": "A1", "type_": "track", "title": OTHER}]
    fetch = routed(search=results(43), releases={43: release(43, tracks=tracks)}, beatport=beatport)

    result = tag.tag_one(path, searcher=searcher(fetch))

    assert result.genre_written is None
    assert tags.read_genre_from_file(path) is None


def test_a_file_titled_in_brackets_still_takes_its_own_tracks_genre(tmp_path, silence):
    path = tmp_path / "a.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": "(Intro)"})
    beatport = searchers.Fetched(
        text=_beatport_page(
            [
                _beatport_track(ARTIST, OTHER, "Techno", mix="Original Mix"),
                _beatport_track(ARTIST, "Intro", BUCKET_GENRE, mix="Original Mix"),
            ]
        ),
        status=200,
    )
    result = tag.tag_one(path, searcher=searcher(routed(search=results(), beatport=beatport)))
    assert result.genre_written == BUCKET_GENRE
    assert tags.read_genre_from_file(path) == BUCKET_GENRE
