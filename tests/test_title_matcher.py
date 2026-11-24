"""R-1534, R-1631, R-1636 and R-1646: a title matches only its own recording, in every source.

Titles match when they name the same words once each has shed what is not its title;
"Artist - X" with X ending in a version matches only a row writing that split (R-1646).
Nothing is compared by characters, a side with no letter or digit matches nothing, and a
title only inside the other's trailing brackets is a pinned cost. Section L pins the parse
(U280). Pages are synthetic text handed to the injected fetch seam.
"""

from __future__ import annotations

import functools
import random
from pathlib import Path

import pytest

from cratekit.core import routing, tags
from cratekit.core.naming import MarkerRule, NameSpec, NameTemplate, render_all
from cratekit.tagging import searchers, tag, titles
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
from tests.test_discogs_searcher import (
    TAXONOMY,
    discogs_answer,
    release,
    results,
    routed,
    searcher,
)

OTHER = "Sunrise Mood"
BRACKETED = "(Not Just) Knee Deep (Part 1)"

#: Titles nothing can be read off: empty, blank, punctuation, empty brackets.
NOISE = ("", "   ", "-", "...", "()", "( )", "!?", "___")


def _matches(searched: str, found: str) -> bool:
    """The shared matcher for a file by the suite's artist, as every source asks it."""
    return searchers._title_matches(searched, found, artist=ARTIST)


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


def _file(tmp_path: Path, silence: Path, name: str, wanted: dict[str, str]) -> Path:
    path = tmp_path / f"{name}.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, wanted)
    return path


def _written(tmp_path, silence, fetch, *, title=None, artist=ARTIST, name="a"):
    """The genre ``tag_one`` writes on a file so tagged (no title: none), as read back off it."""
    wanted = {"artist": artist} if title is None else {"artist": artist, "title": title}
    path = _file(tmp_path, silence, name, wanted)
    if title is None:
        assert tags.read_tag(path, "title") is None
    result = tag.tag_one(path, searcher=searcher(fetch))
    assert tags.read_genre_from_file(path) == result.genre_written
    return result.genre_written


def _page(rows: list[dict]) -> searchers.Fetched:
    return searchers.Fetched(text=_beatport_page(rows), status=200)


def _beatport_and_discogs(row: str, number: int, artist: str = ARTIST):
    """A Beatport row and a Discogs track, each ``row`` by ``artist``, on release ``number``."""
    beatport = _page([_beatport_track(artist, row, BUCKET_GENRE, mix="Original Mix")])
    tracks = [{"position": "A1", "type_": "track", "title": row}]
    return routed(search=results(number), releases={number: release(number, tracks=tracks)}, beatport=beatport)


# A. The shared matcher, both ways round


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
    # R-1631: a mid title bracket is kept, and what a title sheds is its own.
    ("Knee (Not Just) Deep (Part 1)", "Knee (Not Just) Deep"),
    ("Knee (Not Just) Deep (Part 1)", "Knee Not Just Deep (Extended Mix)"),
    ("Sunrise Mood Extended Mix", "Sunrise Mood"),
    ("Sunrise Mood ft. Someone", "Sunrise Mood (Original Mix)"),
    ("Sunrise Mood (feat. Someone) - Original Mix", "Sunrise Mood"),
    ("Sunrise Mood (Kerri Chandler Remix)", "Sunrise Mood - Kerri Chandler Remix"),
    ("Sunrise Mood - 2014 Remaster", "Sunrise Mood (Extended Mix)"),
    ("Sunrise Mood (Mike's (Dub) Mix)", "Sunrise Mood"),
    ("Original", "Original (Extended Mix)"),
    ("Club!", "Club (Original Mix)"),
    ("Vocal Mix", "Vocal Mix"),
    ("Sun Path", "Sun Path [Nightwave Remix]"),
    ("Sunrise Mood Kerri Chandler Remix", "Sunrise Mood (Kerri Chandler Remix)"),
    # Round one: a title of numbers is a title.
    ("1998", "1998"),
    ("808 (Extended Mix)", "808 (Original Mix)"),
    ("Kitchen Session 2 (Extended Mix)", "Kitchen Session 2"),
    ("Sunrise Mood - Remastered 2011", "Sunrise Mood (Extended Mix)"),
    ("Sunrise Mood 2014 Remaster", "Sunrise Mood"),
    ("Summer 1999 (Original Mix)", "Summer 1999"),
]

#: SAME pairs whose file names a mix its row lacks: Discogs takes no release on them (U318).
NAMED_MIX_UNWRITTEN = [("Sunrise Mood (Mike's (Dub) Mix)", "Sunrise Mood")]

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
    # R-1631: a mid title bracket cut the title at its first bracket.
    ("Knee (Not Just) Deep (Part 1)", "Knee Slapper"),
    ("Knee (Not Just) Deep (Part 1)", "Knee"),
    ("Not Just", "Knee (Not Just) Deep (Part 1)"),
    # A word inside one title's brackets was read as the other title.
    (f"{OTHER} (Intro)", "Intro"),
    (f"{OTHER} (Intro)", "(Intro)"),
    ("Mood", "(Sunrise Mood)"),
    ("Kerri Chandler Remix", f"{OTHER} (Kerri Chandler Remix)"),
    ("Part 1", "Shout (Part 1)"),
    # Version words the hand list missed.
    ("Vocal Mix", "Other Song (Vocal Mix)"),
    ("Acapella", "Other Song (Acapella)"),
    ("Reprise", f"{OTHER} (Reprise)"),
    ("Mixed", f"{OTHER} (Mixed)"),
    ("Remixes", f"{OTHER} (Remixes)"),
    ("Dub Mix", f"{OTHER} (Dub Mix)"),
    # Two titles compared by characters, and a dash tail read as a title.
    ("Club", "Nightclub"),
    ("Re", "There She Goes"),
    ("Original Mix", f"{OTHER} - Original Mix"),
    ("Mood", OTHER),
    ("Dub", "Dub Siren"),
    ("Remix", f"{OTHER} Remix"),
    ("Love", "Love Is The Message"),
    ("Track 2", "Track"),
    ("(Hate) Is The Message", "(Love) Is The Message"),
    # Round one: a number is never shed with a bracket's words or a version.
    ("909 (Jack Mix)", "Jack"),
    ("303 (Acid Mix)", "Acid"),
    ("100% (Vocal Mix)", "Vocal (Original Mix)"),
    ("Kitchen Session 2", "Kitchen Session 1"),
    ("Shout Part 2 (Extended Mix)", "Shout Part 1 (Original Mix)"),
    ("Track 2 (Extended Mix)", "Track"),
    # Round two: a year names the recording unless a remaster carries it.
    ("Summer 1999 (Original Mix)", "Summer 2000 (Original Mix)"),
    ("Ibiza 2001 (Club Mix)", "Ibiza 2002 (Club Mix)"),
    ("Summer 1999 Club Mix", "Summer 2000 Club Mix"),
]

#: (file title, catalogue row) pairs naming one recording, read one way round: the
#: file's head before a dash (``KEY - BPM - `` or "Artist - Title") no row carries.
HEADED = [
    ("04A - 126 - Burning (Extended Mix)", "Burning"),
    ("04A - 126 - Burning (Extended Mix)", "Burning (Original Mix)"),
    ("08A - 124 - Sunrise Mood", "Sunrise Mood feat. Someone"),
    ("Bernard Badie - Sunrise Mood", "Sunrise Mood"),
    ("08A - 124 - (Intro)", "Intro"),
    ("08A - 124 - (Not Just) Knee Deep (Part 1)", "Knee Deep"),
    ("08A - 124 - Interlude", "Interlude"),
    ("04A - 126 - Dub", "Dub (Original Mix)"),
    ("01 Sunrise Mood", "Sunrise Mood (Extended Mix)"),
    ("Bernard Badie - Sun Path - 02 Sunrise Mood", "Sunrise Mood"),
    ("08A - 124 - [MP3] Sunrise Mood", "Sunrise Mood"),
    ("08A - 124 - Make Luv - Room 5", "Make Luv"),
    ("Sun Path - 08A - 124", "Sun Path"),
    ("08A - 124 - 1998 (Original Mix)", "1998"),
    ("08A - 124 - 909", "909 (Original Mix)"),
]

#: (file title, catalogue row) pairs naming different recordings, read one way round:
#: the file's head is never its title, nor is the artist's name and another title.
HEADED_NOT = [
    ("04A - 126 - Burning (Extended Mix)", "126"),
    ("04A - 126 - Burning (Extended Mix)", "04A"),
    ("Bernard Badie - Sunrise Mood", "Bernard Badie"),
    ("Bernard Badie - Sunrise Mood", "Bernard Badie - Tide"),
    ("Bernard Badie - Corner Talk (Club Mix)", "Bernard Badie - Glass Hour (Extended Mix)"),
    ("08A - 124 - 22 (Original Mix)", "Original Mix"),
    ("08A - 124 - 909 (Jack Mix)", "Jack"),
    ("08A - 124 - Kitchen Session 2", "Kitchen Session 1"),
    ("08A - 124 - Summer 1999 (Original Mix)", "Summer 2000 (Original Mix)"),
    ("Sun Path - 08A - 124", "08A"),
    ("22 Bullets", "Bullets"),
]


@pytest.mark.parametrize(("searched", "found"), SAME)
def test_a_title_matches_its_own_recording_either_way_round(searched, found):
    assert _matches(searched, found)
    assert _matches(found, searched)


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_a_title_matches_no_other_recording_either_way_round(searched, found):
    assert not _matches(searched, found)
    assert not _matches(found, searched)


@pytest.mark.parametrize(("searched", "found"), HEADED)
def test_a_headed_file_title_matches_its_own_row(searched, found):
    assert _matches(searched, found)


def _missed(searched: str, found: str) -> None:
    """Neither the matcher, a scraped parser, Discogs nor Beatport takes ``found`` for the file."""
    assert not _matches(searched, found)
    assert _traxsource_hit(searched, found).genre is None
    assert _bandcamp_hit(searched, found).genre is None
    assert discogs_answer(_discogs_hit(searched, found)).answer == "miss"


def _found(searched: str, found: str) -> None:
    """The matcher, both scraped parsers, Discogs and Beatport each take ``found`` for the file."""
    assert _matches(searched, found)
    assert _traxsource_hit(searched, found).genre == BUCKET_GENRE
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre == BUCKET_GENRE
    assert discogs_answer(_discogs_hit(searched, found)).answer == "matched"
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE)])
    assert hit.genre == BUCKET_GENRE


@pytest.mark.parametrize(("searched", "found"), HEADED_NOT)
def test_a_files_head_is_never_its_title(searched, found):
    _missed(searched, found)
    assert _beatport_answer(_beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE)])) == "miss"


@pytest.mark.parametrize(
    ("searched", "found"),
    [
        ("Club", "Nightclub"),
        ("Re", "There She Goes"),
        ("Dub", "Dub Siren"),
        ("Remix", f"{OTHER} Remix"),
    ],
)
def test_two_titles_are_compared_by_whole_words_never_by_characters(searched, found):
    """R-1534's residual pairs: a word inside another word, or part of a title, is no match."""
    assert not _matches(searched, found)
    assert not _matches(found, searched)
    assert _matches(f"{searched}!", searched)


def test_a_catalogue_rows_dash_tail_is_never_its_title():
    """A row is read by its head, a file from its title on; a tail of version words is no title."""
    assert not _matches("Original Mix", f"{OTHER} - Original Mix")
    assert not _matches(f"{OTHER} - Original Mix", "Original Mix")
    assert _matches(f"{OTHER} - Original Mix", OTHER)
    assert _matches(OTHER, f"{OTHER} - Original Mix")
    assert not _matches("Hate", "Love - Hate")


@pytest.mark.parametrize("noise", NOISE)
@pytest.mark.parametrize("other", [OTHER, "(Intro)", BRACKETED, "Original Mix", "-"])
def test_a_title_with_no_letter_or_digit_matches_nothing(noise, other):
    assert not _matches(noise, other)
    assert not _matches(other, noise)


@pytest.mark.parametrize("noise", NOISE)
def test_a_title_with_no_letter_or_digit_does_not_match_itself(noise):
    """Nothing identifies the recording, so even an identical row is no match."""
    assert not _matches(noise, noise)


# B. Beatport, which scores its rows rather than asking the shared matcher


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
        ("04A - 126 - Burning (Extended Mix)", "Burning", "Extended Mix"),
        ("Bernard Badie - Sunrise Mood", OTHER, "Original Mix"),
        ("Knee (Not Just) Deep (Part 1)", "Knee (Not Just) Deep", "Part 1"),
        (f"{OTHER} Extended Mix", OTHER, "Extended Mix"),
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
    """Round two: a core tier scored "Love (feat. X)" level with the file's own row."""
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
        # R-1631: the lowest tier and the suffix clause of the middle tier.
        (f"{OTHER} (Intro)", "(Intro)"),
        (f"{OTHER} (Intro)", "Intro"),
        ("Mood", "(Sunrise Mood)"),
        ("Intro", f"{OTHER} (Intro)"),
        ("Knee (Not Just) Deep (Part 1)", "Knee Slapper"),
    ],
)
def test_beatport_scores_no_row_by_a_part_of_its_name(searched, name):
    assert _beatport_answer(_beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE)])) == "miss"


@pytest.mark.parametrize(
    ("searched", "name"),
    [
        ("Knee Deep", "(Not Just) Knee Deep"),
        ("Dub", "Dub (Original Mix)"),
        ("Burning", "Burning feat. Someone"),
    ],
)
def test_beatport_still_finds_a_title_inside_its_rows_name(searched, name):
    assert _beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE)]).genre == BUCKET_GENRE


def test_beatport_prefers_the_headed_files_own_row_over_another_by_the_artist():
    rows = [
        _beatport_track(ARTIST, "Burning Bridges", "Techno", mix="Original Mix"),
        _beatport_track(ARTIST, "Burning", BUCKET_GENRE, mix="Extended Mix"),
    ]
    assert _beatport_hit("04A - 126 - Burning (Extended Mix)", rows).genre == BUCKET_GENRE


def test_a_title_written_only_inside_the_rows_trailing_brackets_is_a_known_cost():
    """A known cost of R-1631, pinned: a title written only inside the other's brackets."""
    name = "Untitled (How Does It Feel)"
    hit = _beatport_hit("How Does It Feel", [_beatport_track(ARTIST, name, BUCKET_GENRE)])
    assert _beatport_answer(hit) == "miss"
    assert not _matches("How Does It Feel", name)


def test_beatport_reads_no_artist_from_a_row_crediting_an_empty_name():
    """An empty credit was read as contained in every searched artist."""
    row = _beatport_track("", OTHER, BUCKET_GENRE)
    assert _beatport_answer(_beatport_hit(OTHER, [row])) == "miss"


# C. The scraped parsers, which read the shared matcher


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


def test_bandcamp_never_reads_a_headings_artist_as_its_title():
    """A heading "Artist - Friday Night Mix" read whole met the file on the artist's name."""
    hit = _bandcamp_hit(f"05B - 98 - {ARTIST} - Body", f"{ARTIST} - Friday Night Mix")
    assert hit.genre is None
    assert _bandcamp_hit("Body", f"{ARTIST} - Body (Extended Mix)").genre == BUCKET_GENRE


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_bandcamp_writes_no_genre_off_another_track_by_the_artist(searched, found):
    assert _bandcamp_hit(searched, found).genre is None
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre is None


@pytest.mark.parametrize(("searched", "found"), SAME + HEADED)
def test_the_scraped_parsers_still_match_a_title_to_its_own_row(searched, found):
    trax = _traxsource_hit(searched, found)
    assert (trax.genre, trax.source) == (BUCKET_GENRE, searchers.TRAXSOURCE)
    band = _bandcamp_hit(searched, f"{ARTIST} - {found}")
    assert (band.genre, band.source) == (BUCKET_GENRE, searchers.BANDCAMP)


# D. Discogs, moved onto the shared matcher


def _discogs_hit(title: str, track: str):
    tracks = [{"position": "A1", "type_": "track", "title": track}]
    fetch = routed(search=results(41), releases={41: release(41, tracks=tracks)})
    return searcher(fetch)(ARTIST, title)


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_discogs_writes_no_style_off_another_track_by_the_artist(searched, found):
    hit = _discogs_hit(searched, found)
    assert discogs_answer(hit).answer == "miss"
    assert hit.genre is None


@pytest.mark.parametrize(
    ("searched", "found"), [case for case in SAME + HEADED if case not in NAMED_MIX_UNWRITTEN]
)
def test_discogs_still_matches_a_title_to_its_own_track(searched, found):
    assert discogs_answer(_discogs_hit(searched, found)).answer == "matched"


@pytest.mark.parametrize(("searched", "found"), NAMED_MIX_UNWRITTEN)
def test_discogs_takes_no_track_that_does_not_write_the_files_named_mix(searched, found):
    assert _matches(searched, found), "the shared matcher is unchanged"
    assert discogs_answer(_discogs_hit(searched, found)).answer == "miss"


def test_discogs_reads_no_single_whose_title_is_noise():
    fetch = routed(search=results(42), releases={42: release(42, title="()", tracks=[])})
    assert discogs_answer(searcher(fetch)(ARTIST, OTHER)).answer == "miss"


# E. The write itself, driven through tag_one as the review drove it


@pytest.mark.parametrize("title", ["(Intro)", BRACKETED, "(Intro) (Extended Mix)"])
def test_a_file_titled_in_brackets_takes_no_genre_off_another_track(tmp_path, silence, title):
    """B1 of R-1534, as U244's review drove it: the genre was written for good."""
    assert _written(tmp_path, silence, _beatport_and_discogs(OTHER, 43), title=title) is None


def test_a_file_titled_in_brackets_still_takes_its_own_tracks_genre(tmp_path, silence):
    beatport = _page([
        _beatport_track(ARTIST, OTHER, "Techno", mix="Original Mix"),
        _beatport_track(ARTIST, "Intro", BUCKET_GENRE, mix="Original Mix"),
    ])
    fetch = routed(search=results(), beatport=beatport)
    assert _written(tmp_path, silence, fetch, title="(Intro)") == BUCKET_GENRE


#: (file title, another recording by the artist) pairs R-1631 drove to a wrong genre.
R1631_WRITES = [
    ("Knee (Not Just) Deep (Part 1)", "Knee Slapper"),
    (f"{OTHER} (Intro)", "Intro"),
    ("Vocal Mix", "Other Song (Vocal Mix)"),
    ("Club", "Nightclub"),
    ("Original Mix", f"{OTHER} - Original Mix"),
    ("Mood", "(Sunrise Mood)"),
    ("08A - 124 - 909 (Jack Mix)", "Jack"),
    ("08A - 124 - Kitchen Session 2", "Kitchen Session 1"),
    ("100% (Vocal Mix)", "Vocal (Original Mix)"),
]


@pytest.mark.parametrize(
    ("title", "other", "own", "mix"),
    [
        ("08A - 124 - Kitchen Session 2", "Kitchen Session 1", "Kitchen Session 2", ""),
        ("08A - 124 - Burning (Extended Mix)", "Burning", "Burning", "Extended Mix"),
        ("08A - 124 - 909 (Jack Mix)", "Jack", "909", "Jack Mix"),
    ],
)
def test_a_headed_file_takes_its_own_rows_genre_over_another_listed_first(
    tmp_path, silence, title, other, own, mix
):
    """Round one: the top tier read the head's words too, so page order chose."""
    rows = [
        _beatport_track(ARTIST, other, "Techno", mix="Original Mix"),
        _beatport_track(ARTIST, own, BUCKET_GENRE, mix=mix),
    ]
    fetch = routed(search=results(), beatport=_page(rows))
    assert _written(tmp_path, silence, fetch, title=title) == BUCKET_GENRE


@pytest.mark.parametrize(("title", "other"), R1631_WRITES)
def test_a_file_takes_no_genre_off_another_recording_named_in_its_title(
    tmp_path, silence, title, other
):
    """R-1631: neither another recording's Beatport row nor Discogs track writes its genre."""
    assert _written(tmp_path, silence, _beatport_and_discogs(other, 44), title=title) is None


@pytest.mark.parametrize("source", ["beatport", "discogs"])
def test_a_file_whose_title_tag_carries_its_head_still_takes_its_own_genre(
    tmp_path, silence, source
):
    """The live library writes ``KEY - BPM - `` into the title tag; its own row is still found."""
    if source == "beatport":
        rows = [
            _beatport_track(ARTIST, "Burning Bridges", "Techno", mix="Original Mix"),
            _beatport_track(ARTIST, "Burning", BUCKET_GENRE, mix="Extended Mix"),
        ]
        fetch = routed(search=results(), beatport=_page(rows))
    else:
        tracks = [
            {"position": "A1", "type_": "track", "title": "Burning Bridges"},
            {"position": "A2", "type_": "track", "title": "Burning (Extended Mix)"},
        ]
        fetch = routed(search=results(45), releases={45: release(45, tracks=tracks)})
    title = "04A - 126 - Burning (Extended Mix)"
    assert _written(tmp_path, silence, fetch, title=title) is not None


# F. R-1636: a dash part of the file's title that is not its title

#: (file title, another recording by the artist) pairs read from a dash part that is
#: not the title: a version tail the list lacks ("vocal"), an untagged name's album,
#: or the artist of a "KEY - BPM - Artist - Title" name.
NOT_THE_TITLE = [
    ("08A - 124 - Other Song - Vocal Mix", "Vocal Mix"),
    ("08A - 124 - Other Song - Vocal Mix", "Vocal"),
    ("Other Song - Vocal Mix", "Vocal"),
    ("Other Song - Vocal Mix", "Vocal Mix"),
    ("Other Song - Vocal", "Vocal"),
    ("08A - 124 - Other Song - Vocal Dub", "Vocal"),
    (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Sun Path"),
    (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Sun Path (Original Mix)"),
    (f"Tide - {ARTIST} - Sun Path", "Sun Path"),
    (f"08A - 124 - {ARTIST} - Sun Path", ARTIST),
    (f"08A - 124 - {ARTIST} - Sun Path", f"{ARTIST} (Extended Mix)"),
    (f"08A - 124 - {ARTIST} feat. Someone - Sun Path", ARTIST),
    (f"{ARTIST} - Sun Path - 02 Tide", "Sun Path"),
]

#: (file title, its own row) pairs the same rule keeps.
OWN_TITLE = [
    (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Tide"),
    (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Tide (Extended Mix)"),
    (f"Tide - {ARTIST} - Sun Path", "Tide"),
    (f"Tide - {ARTIST}", "Tide"),
    (f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
    (f"{ARTIST} - Sun Path", "Sun Path (Extended Mix)"),
    (f"08A - 124 - {ARTIST} feat. Someone - Sun Path", "Sun Path"),
    (f"{ARTIST} - Sun Path - 02 Tide", "Tide"),
    ("08A - 124 - Other Song - Vocal Mix", "Other Song"),
    ("08A - 124 - Other Song - Vocal Mix", "Other Song (Vocal Mix)"),
    ("Other Song - Vocal Mix", "Other Song"),
    ("08A - 124 - Make Luv - Room 5", "Make Luv"),
    (f"08A - 124 - {ARTIST}", ARTIST),
    (f"{ARTIST} - Original Mix", ARTIST),
    (f"08A - 124 - {ARTIST} - Original Mix", f"{ARTIST} (Extended Mix)"),
]


@pytest.mark.parametrize(("searched", "found"), NOT_THE_TITLE)
def test_a_files_dash_part_that_is_not_its_title_matches_nothing(searched, found):
    _missed(searched, found)
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre is None
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE)])
    assert _beatport_answer(hit) == "miss"


@pytest.mark.parametrize(("searched", "found"), OWN_TITLE)
def test_a_files_title_among_its_dash_parts_still_finds_its_own_row(searched, found):
    _found(searched, found)


def test_the_artists_part_is_read_word_for_word_never_by_characters():
    """"Badie" is not "Bernard Badie", so it is the title and its later part is not."""
    assert _matches("08A - 124 - Badie - Sun Path", "Badie")
    assert not _matches("08A - 124 - Badie - Sun Path", "Sun Path")


def test_a_name_with_no_artist_is_read_from_its_first_part():
    """With no artist the later part is never read alone: a miss, never another recording."""
    assert not searchers._title_matches("Other Song - Vocal Mix", "Vocal", artist="")
    assert searchers._title_matches("Other Song - Vocal Mix", "Other Song", artist="")
    assert not searchers._title_matches(f"{ARTIST} - Sun Path", ARTIST, artist="")


#: The genre the file's own row gives; Discogs is asked first since U282, styled Nu-Disco.
OWN_ROWS_GENRE = routing.suggest_tag(TAXONOMY, "Nu-Disco", source=searchers.DISCOGS).tag


@pytest.mark.parametrize(("title", "other"), NOT_THE_TITLE)
def test_a_files_title_tag_writes_no_genre_off_a_dash_part_that_is_not_its_title(
    tmp_path, silence, title, other
):
    """R-1631's review: neither another recording's row nor track writes its genre."""
    assert _written(tmp_path, silence, _beatport_and_discogs(other, 46), title=title) is None


@pytest.mark.parametrize(
    ("name", "other"),
    [
        (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Sun Path"),
        (f"08A - 124 - {ARTIST} - Sun Path", ARTIST),
        ("08A - 124 - Other Song - Vocal Mix", "Vocal"),
    ],
)
def test_an_untagged_file_writes_no_genre_off_its_names_album_or_artist(
    tmp_path, silence, name, other
):
    """An untagged name's album and artist dash parts are never its title."""
    assert _written(tmp_path, silence, _beatport_and_discogs(other, 47), name=name) is None


@pytest.mark.parametrize(
    ("name", "own"),
    [
        (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Tide"),
        (f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
        (f"{ARTIST} - Sun Path - 02 Tide", "Tide"),
    ],
)
def test_an_untagged_file_still_takes_its_own_rows_genre_by_its_name(tmp_path, silence, name, own):
    assert _written(tmp_path, silence, _beatport_and_discogs(own, 48), name=name) == OWN_ROWS_GENRE


# G. R-1636, review round one: the artist's part as a name writes it

#: (artist tag, file title, its own row): the artist's part written as a name writes
#: it; each found its own row on main and lost it at round one's head.
ARTIST_AS_WRITTEN = [
    (ARTIST, f"08A - 124 - [MP3] {ARTIST} - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - {ARTIST} & Tide - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - Tide & {ARTIST} - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - {ARTIST}, Tide - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - {ARTIST} x Tide - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - {ARTIST} vs Tide - Sun Path", "Sun Path"),
    (ARTIST, f"01 - {ARTIST} - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - 01 - {ARTIST} - Sun Path", "Sun Path"),
    (ARTIST, f"{ARTIST} - Sun Path - 02 - Tide", "Tide"),
    (ARTIST, f"08A - 124 - {ARTIST} - Sun Path - 02 - Tide", "Tide"),
    ("Black Madonna", "The Black Madonna - Sun Path", "Sun Path"),
    ("The Black Madonna", "08A - 124 - Black Madonna - Sun Path", "Sun Path"),
    ("Âme", "08A - 124 - Ame - Sun Path", "Sun Path"),
    ("Ame", "08A - 124 - Âme - Sun Path", "Sun Path"),
    (f"{ARTIST}; Tide", f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
    (f"{ARTIST} & Tide", f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
    (f"{ARTIST} feat. Tide", f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
    (f"{ARTIST} x Tide", f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
]


@pytest.mark.parametrize(("artist", "title", "own"), ARTIST_AS_WRITTEN)
def test_the_artists_part_is_known_as_a_name_writes_it(artist, title, own):
    assert searchers._title_matches(title, own, artist=artist)
    if not artist.startswith(ARTIST):
        return
    assert not searchers._title_matches(title, ARTIST, artist=artist)
    hit = _beatport_hit(title, [_beatport_track(ARTIST, own, BUCKET_GENRE)])
    assert hit.genre == BUCKET_GENRE
    assert discogs_answer(_discogs_hit(title, own)).answer == "matched"


@pytest.mark.parametrize(
    ("name", "own"),
    [
        (f"08A - 124 - [MP3] {ARTIST} - Sun Path", "Sun Path"),
        (f"08A - 124 - {ARTIST} & Tide - Sun Path", "Sun Path"),
        (f"01 - {ARTIST} - Sun Path", "Sun Path"),
        (f"{ARTIST} - Sun Path - 02 - Tide", "Tide"),
    ],
)
def test_an_untagged_file_named_with_its_artist_as_written_takes_its_own_genre(
    tmp_path, silence, name, own
):
    assert _written(tmp_path, silence, _beatport_and_discogs(own, 49), name=name) == OWN_ROWS_GENRE


def test_a_self_titled_tracks_dash_version_the_list_lacks_finds_its_own_row_only_when_it_writes_the_version(
    tmp_path, silence
):
    """R-1646: "Artist - Vocal Mix" is read neither way alone, the cost recorded on #788."""
    title = f"08A - 124 - {ARTIST} - Vocal Mix"
    assert not _matches(title, ARTIST)
    assert not _matches(title, f"{ARTIST} (Extended Mix)")
    assert _matches(title, f"{ARTIST} (Vocal Mix)")
    assert not _matches(f"08A - 124 - {ARTIST} - Sun Path", ARTIST)
    rows = [
        _beatport_track(ARTIST, ARTIST, BUCKET_GENRE, mix="Extended Mix"),
        _beatport_track(ARTIST, "Vocal", "Techno"),
    ]
    fetch = routed(search=results(), beatport=_page(rows))
    assert _written(tmp_path, silence, fetch, title=title) is None


#: (artist tag, file title, its own row, another recording): each rule of the title's start.
TITLE_START = [
    # The next part naming the artist keeps a self titled first part the title.
    (ARTIST, f"08A - 124 - {ARTIST} - {ARTIST} - Sun Path", ARTIST, "Sun Path"),
    # A tag crediting two names, or a feature, knows the name alone.
    (f"{ARTIST} & Tide", f"08A - 124 - {ARTIST} - Sun Path", "Sun Path", ARTIST),
    (f"{ARTIST} feat. Tide", f"08A - 124 - {ARTIST} - Sun Path", "Sun Path", ARTIST),
    # A number outside a tempo's range before anything else is a title.
    (ARTIST, f"909 - {ARTIST} - Sun Path", "909", "Sun Path"),
    # A number after a key is its tempo whatever its value.
    (ARTIST, "08A - 300 - Sun Path - Tide", "Sun Path", "Tide"),
    # The part before a track numbered title is its album, never read alone.
    (ARTIST, "08A - 124 - Sun Path - 02 Tide", "Tide", "Sun Path"),
    (ARTIST, f"{ARTIST} - Sun Path - 02 Tide Extended Mix", "Tide", "Sun Path"),
]


# H. R-1636, review round two: a title holding the artist's name, and both ways' end

#: (artist tag, file title, its own row, another recording by the artist).
ROUND_TWO = [
    # A title holding the artist's name is a title, never the artist's credit.
    (ARTIST, f"08A - 124 - {ARTIST} Theme - Pt. 2", f"{ARTIST} Theme (Pt. 2)", "Pt. 2"),
    ("Tide", "08A - 124 - Riding The Tide - Part 2", "Riding The Tide (Part 2)", "Part 2"),
    ("Tide", "08A - 124 - Riding The Tide - Intro", "Riding The Tide (Intro)", "Intro"),
    (ARTIST, f"{ARTIST} - {ARTIST} Theme", f"{ARTIST} Theme", ARTIST),
    ("Tide", "Tide - Riding The Tide", "Riding The Tide", "Tide"),
    ("Tide", "08A - 124 - Riding The Tide - Vocal Mix", "Riding The Tide", "Vocal Mix"),
    (ARTIST, f"08A - 124 - {ARTIST} Theme - Vocal Mix", f"{ARTIST} Theme", "Vocal Mix"),
    # The artist after the title, or in its version, is never read alone.
    ("Tide", "08A - 124 - Sun Path - Tide - Fabric Live", "Sun Path", "Tide"),
    ("Tide", "08A - 124 - Sun Path - Tide", "Sun Path", "Tide"),
    ("Tide", "Sun Path - Tide", "Sun Path", "Tide"),
    (ARTIST, f"08A - 124 - Sun Path - {ARTIST} Remix", "Sun Path", ARTIST),
    ("Tide", "08A - 124 - Sun Path - Tide Dub", "Sun Path", "Tide"),
    # The artist's part is read both ways only before a version, never a title.
    (ARTIST, f"08A - 124 - {ARTIST} - Sun Path - Original Mix", "Sun Path", ARTIST),
    # A number of three figures, or one before a version, is a title.
    (ARTIST, "08A - 124 - 007 - Original Mix", "007", "Original Mix"),
    ("Tide", "007 - Tide - Sun Path", "007", "Sun Path"),
    (ARTIST, "08A - 124 - 05 - Original Mix", "05", "Original Mix"),
]


@pytest.mark.parametrize(("artist", "title", "own", "other"), TITLE_START + ROUND_TWO)
def test_round_two_a_title_keeps_its_own_row_and_takes_no_other(artist, title, own, other):
    assert searchers._title_matches(title, own, artist=artist)
    assert not searchers._title_matches(title, other, artist=artist)


@pytest.mark.parametrize(
    ("artist", "title", "other"),
    [
        (ARTIST, f"08A - 124 - Sun Path - {ARTIST} Remix", ARTIST),
        ("Tide", "08A - 124 - Sun Path - Tide - Fabric Live", "Tide"),
        (ARTIST, f"08A - 124 - {ARTIST} - Sun Path - Original Mix", ARTIST),
        ("Tide", "08A - 124 - Riding The Tide - Vocal Mix", "Vocal Mix"),
    ],
)
def test_round_two_no_genre_is_written_off_another_recording(tmp_path, silence, artist, title, other):
    fetch = _beatport_and_discogs(other, 50, artist=artist)
    assert _written(tmp_path, silence, fetch, title=title, artist=artist) is None


#: (artist tag, file title, its own row): each way a credit is written is known.
CREDIT_WAYS = [
    # An initial stands for a word of a name of two words or more.
    (ARTIST, "08A - 124 - B. Badie - Sun Path", "Sun Path"),
    # "The" opens a name on either side.
    ("The Black Madonna", "08A - 124 - Black Madonna - Sun Path", "Sun Path"),
    # Every join a credit is written with.
    (f"{ARTIST}; Tide", "08A - 124 - Tide - Sun Path", "Sun Path"),
    (f"{ARTIST} + Tide", "08A - 124 - Tide - Sun Path", "Sun Path"),
    (ARTIST, f"08A - 124 - {ARTIST} pres. Tide - Sun Path", "Sun Path"),
    # A track number glued to the first part, or alone before it.
    (ARTIST, f"01 {ARTIST} - Sun Path", "Sun Path"),
    (ARTIST, f"01 - {ARTIST} - Sun Path", "Sun Path"),
    # A part after a lone track number is the title, even the artist's name.
    (ARTIST, f"{ARTIST} - Sun Path - 02 - {ARTIST}", ARTIST),
    # Two parts crediting the artist read the second too.
    (ARTIST, f"08A - 124 - Tide & {ARTIST} - {ARTIST}", ARTIST),
]

#: (artist tag, file title, a row): what is not the artist's credit is never passed over.
NOT_A_CREDIT = [
    (ARTIST, "08A - 124 - B. Badie - Sun Path", "B Badie"),
    (ARTIST, f"{ARTIST} - Sun Path - 02 - {ARTIST}", "Sun Path"),
    (ARTIST, "08A - 124 - Badie - Sun Path", "Sun Path"),
    ("Tide", "08A - 124 - Love And Tides - Sun Path", "Sun Path"),
    # "with" and "and" are in titles: a title is never taken for a credit.
    (ARTIST, f"{ARTIST} - Dancing With {ARTIST}", ARTIST),
    (ARTIST, f"08A - 124 - Love And {ARTIST} - Sun Path", "Sun Path"),
]


# I. R-1646: "Artist - X" with X ending in a version is read neither way alone

#: (file title, a row) pairs in the card's shape: the artist's part, then a part
#: ending in a version word, which only a list could read as a title X or the self
#: titled track in version X, so a row reading one way only is a miss.
SPLIT_UNCONFIRMED = [
    (f"08A - 124 - {ARTIST} - Vocal Mix", "Vocal"),
    (f"08A - 124 - {ARTIST} - Vocal Mix", "Vocal Mix"),
    (f"08A - 124 - {ARTIST} - Vocal Mix", ARTIST),
    (f"08A - 124 - {ARTIST} - Vocal Mix", f"{ARTIST} (Extended Mix)"),
    (f"08A - 124 - {ARTIST} - Vocal Mix", "Vocal (Original Mix)"),
    (f"{ARTIST} - Vocal Mix", "Vocal"),
    (f"{ARTIST} - Vocal Mix", ARTIST),
    (f"08A - 124 - {ARTIST} - Vocal Mix (Radio Edit)", "Vocal Mix (Radio Edit)"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", ARTIST),
    (f"{ARTIST} - Sunrise Mood Extended Mix", f"{ARTIST} (Original Mix)"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood Extended Mix"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood (Original Mix)"),
    (f"08A - 124 - {ARTIST} - Kerri Chandler Remix", "Kerri Chandler"),
    (f"08A - 124 - {ARTIST} - Kerri Chandler Remix", ARTIST),
    (f"{ARTIST} & Tide - Vocal Mix", "Vocal"),
    (f"[MP3] {ARTIST} - Vocal Dub", "Vocal"),
]

#: The same shape where the row writes the split itself, so the catalogue says which.
SPLIT_CONFIRMED = [
    (f"08A - 124 - {ARTIST} - Vocal Mix", f"{ARTIST} (Vocal Mix)"),
    (f"08A - 124 - {ARTIST} - Vocal Mix", f"{ARTIST} - Vocal Mix"),
    (f"{ARTIST} - Vocal Mix", f"{ARTIST} [Vocal Mix]"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood (Extended Mix)"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood - Extended Mix"),
    (f"{ARTIST} - Sunrise Mood Extended Mix", f"{ARTIST} (Sunrise Mood Extended Mix)"),
    (f"08A - 124 - {ARTIST} - Kerri Chandler Remix", f"{ARTIST} (Kerri Chandler Remix)"),
    (f"08A - 124 - {ARTIST} - Sunrise Mood 2011 Remaster", "Sunrise Mood (2011 Remaster)"),
    (f"08A - 124 - {ARTIST} - Vocal Mix (Radio Edit)", f"{ARTIST} (Vocal Mix) (Radio Edit)"),
    (f"{ARTIST} & Tide - Vocal Mix", f"{ARTIST} & Tide (Vocal Mix)"),
    (f"[MP3] {ARTIST} - Vocal Dub", f"{ARTIST} (Vocal Dub)"),
]

#: One reading only, as before: no version ending, a version alone or in brackets.
SPLIT_NOT_THE_SHAPE = [
    (f"{ARTIST} - Sunrise Mood (Extended Mix)", "Sunrise Mood", ARTIST),
    (f"{ARTIST} - Sunrise Mood", "Sunrise Mood", ARTIST),
    (f"{ARTIST} - Original Mix", ARTIST, "Original Mix"),
    (f"08A - 124 - {ARTIST} - Extended Mix", f"{ARTIST} (Original Mix)", "Extended Mix"),
    ("08A - 124 - Other Song - Vocal Mix", "Other Song", "Vocal"),
    (f"{ARTIST} - Sun Path - 02 Tide Extended Mix", "Tide", "Sun Path"),
]


@pytest.mark.parametrize(("searched", "found"), SPLIT_UNCONFIRMED)
def test_artist_then_a_version_ending_part_matches_no_row_that_reads_one_way(searched, found):
    _missed(searched, found)
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre is None
    for mix in ("", "Original Mix", "Radio Edit"):
        hit = _beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE, mix=mix)])
        assert _beatport_answer(hit) == "miss"


@pytest.mark.parametrize(("searched", "found"), SPLIT_CONFIRMED)
def test_artist_then_a_version_ending_part_matches_a_row_that_writes_the_same_split(searched, found):
    _found(searched, found)


@pytest.mark.parametrize(
    ("searched", "name", "mix"),
    [
        (f"08A - 124 - {ARTIST} - Vocal Mix", ARTIST, "Vocal Mix"),
        (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood", "Extended Mix"),
        (f"08A - 124 - {ARTIST} - Kerri Chandler Remix", ARTIST, "Kerri Chandler Remix"),
    ],
)
def test_beatport_reads_a_rows_name_and_mix_as_its_split(searched, name, mix):
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE, mix=mix)])
    assert hit.genre == BUCKET_GENRE


@pytest.mark.parametrize(
    ("searched", "name", "mix"),
    [
        (f"08A - 124 - {ARTIST} - Vocal Mix", "Vocal", "Original Mix"),
        (f"08A - 124 - {ARTIST} - Vocal Mix", ARTIST, "Original Mix"),
        (f"{ARTIST} - Sunrise Mood Extended Mix", ARTIST, "Extended Mix"),
        (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood", "Original Mix"),
        (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood Extended Mix", "Original Mix"),
    ],
)
def test_beatport_reads_no_row_whose_name_and_mix_split_it_otherwise(searched, name, mix):
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE, mix=mix)])
    assert _beatport_answer(hit) == "miss"


@pytest.mark.parametrize(("searched", "own", "other"), SPLIT_NOT_THE_SHAPE)
def test_the_artists_part_before_any_other_part_reads_as_it_did(searched, own, other):
    assert _matches(searched, own)
    assert not _matches(searched, other)


def _split_page(rows: list[tuple[str, str, str]], tracks: list[str], number: int):
    beatport = _page([_beatport_track(ARTIST, name, genre, mix=mix) for name, mix, genre in rows])
    listed = [{"position": f"A{index}", "type_": "track", "title": track} for index, track in enumerate(tracks, 1)]
    return routed(search=results(number), releases={number: release(number, tracks=listed)}, beatport=beatport)


@pytest.mark.parametrize(
    ("title", "rows", "tracks"),
    [
        # The card's first scenario: a "Vocal" row and a "Vocal Mix" track are another recording.
        (f"08A - 124 - {ARTIST} - Vocal Mix", [("Vocal", "Original Mix", BUCKET_GENRE)], ["Vocal Mix"]),
        (f"08A - 124 - {ARTIST} - Vocal Mix", [("Vocal", "", BUCKET_GENRE)], ["Vocal"]),
        # The second: a self titled row is another recording.
        (f"{ARTIST} - Sunrise Mood Extended Mix", [(ARTIST, "Original Mix", BUCKET_GENRE)], [ARTIST]),
        (f"{ARTIST} - Sunrise Mood Extended Mix", [(ARTIST, "Extended Mix", BUCKET_GENRE)], [f"{ARTIST} (Extended Mix)"]),
        # The recorded cost: the own row under another mix is a miss rather than a guess.
        (f"08A - 124 - {ARTIST} - Vocal Mix", [(ARTIST, "Extended Mix", BUCKET_GENRE)], [ARTIST]),
    ],
)
def test_no_genre_is_written_off_a_row_that_reads_the_name_one_way(tmp_path, silence, title, rows, tracks):
    assert _written(tmp_path, silence, _split_page(rows, tracks, 51), title=title) is None


@pytest.mark.parametrize("order", [1, -1])
@pytest.mark.parametrize(
    ("title", "own", "other"),
    [
        (f"08A - 124 - {ARTIST} - Vocal Mix", (ARTIST, "Vocal Mix"), ("Vocal", "Original Mix")),
        (f"08A - 124 - {ARTIST} - Vocal Mix", (ARTIST, "Vocal Mix"), (ARTIST, "Extended Mix")),
        (f"{ARTIST} - Sunrise Mood Extended Mix", ("Sunrise Mood", "Extended Mix"), (ARTIST, "Original Mix")),
        (f"{ARTIST} - Sunrise Mood Extended Mix", ("Sunrise Mood", "Extended Mix"), ("Sunrise Mood", "Original Mix")),
    ],
)
def test_the_row_that_writes_the_same_split_wins_on_a_page_in_either_order(
    tmp_path, silence, title, own, other, order
):
    rows = [(*own, BUCKET_GENRE), (*other, "Techno")][::order]
    assert _written(tmp_path, silence, _split_page(rows, [], 52), title=title) == BUCKET_GENRE


@pytest.mark.parametrize(
    ("title", "own", "other"),
    [
        (f"08A - 124 - {ARTIST} - Vocal Mix", f"{ARTIST} (Vocal Mix)", "Vocal Mix"),
        (f"{ARTIST} - Sunrise Mood Extended Mix", "Sunrise Mood (Extended Mix)", ARTIST),
    ],
)
def test_discogs_takes_the_track_that_writes_the_same_split(tmp_path, silence, title, own, other):
    assert _written(tmp_path, silence, _split_page([], [other, own], 53), title=title) is not None


@pytest.mark.parametrize(
    ("name", "other"),
    [
        (f"08A - 124 - {ARTIST} - Vocal Mix", "Vocal"),
        (f"{ARTIST} - Sunrise Mood Extended Mix", ARTIST),
    ],
)
def test_an_untagged_file_in_the_shape_writes_no_genre_off_a_row_that_reads_it_one_way(
    tmp_path, silence, name, other
):
    assert _written(tmp_path, silence, _beatport_and_discogs(other, 54), name=name) is None


# J. R-1646, review round one: the whole title never collapses onto the artist's part

#: (file title, the self titled row it must not match): a feature credit cut the
#: whole title to the artist's name (round one's B1), in the card's shape and out.
FEATURED_ARTIST = [
    f"{ARTIST} feat. Tide - Sunrise Mood Extended Mix",
    f"{ARTIST} ft. Tide - Sunrise Mood Extended Mix",
    f"{ARTIST} featuring Tide - Kerri Chandler Remix",
    f"{ARTIST} (feat. Tide) - Sunrise Mood Extended Mix",
    f"[MP3] {ARTIST} feat. Tide - Sunrise Mood Extended Mix",
    f"01 {ARTIST} feat. Tide - Sunrise Mood Extended Mix",
    f"{ARTIST} feat. Tide - Vocal Mix",
    f"{ARTIST} feat. Tide - Sunrise Mood",
]


@pytest.mark.parametrize("title", FEATURED_ARTIST)
def test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track(title):
    assert not _matches(title, ARTIST)
    assert not _matches(title, f"{ARTIST} (Original Mix)")
    assert _traxsource_hit(title, ARTIST).genre is None
    assert discogs_answer(_discogs_hit(title, ARTIST)).answer == "miss"
    for mix in ("", "Original Mix", "Extended Mix"):
        hit = _beatport_hit(title, [_beatport_track(ARTIST, ARTIST, BUCKET_GENRE, mix=mix)])
        assert _beatport_answer(hit) == "miss"


@pytest.mark.parametrize("tagged", [True, False])
@pytest.mark.parametrize("order", [1, -1])
def test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page(
    tmp_path, silence, tagged, order
):
    """Round one: the title reading dropped and the collapse kept let the self titled row win."""
    name = f"{ARTIST} feat. Tide - Sunrise Mood Extended Mix"
    rows = [("Sunrise Mood", "Extended Mix", BUCKET_GENRE), (ARTIST, "Original Mix", "Techno")][::order]
    fetch = _split_page(rows, [], 55)
    title = name if tagged else None
    assert _written(tmp_path, silence, fetch, title=title, name=name) == BUCKET_GENRE


@pytest.mark.parametrize(
    ("searched", "found"),
    [
        (f"{ARTIST} feat. Tide - Sunrise Mood Extended Mix", f"{ARTIST} (Sunrise Mood Extended Mix)"),
        (f"{ARTIST} feat. Tide - Sunrise Mood Extended Mix", "Sunrise Mood (Extended Mix)"),
        (f"{ARTIST} feat. Tide - Sunrise Mood", "Sunrise Mood"),
        (f"{ARTIST} - Sunrise Mood Extended Mix (Tide Edit)", "Sunrise Mood (Extended Mix) (Tide Edit)"),
        (f"{ARTIST} - Sunrise Mood Remix (2014)", "Sunrise Mood (Remix) (2014)"),
    ],
)
def test_a_split_reads_past_a_feature_credit_and_the_files_own_brackets(searched, found):
    assert _matches(searched, found)


@pytest.mark.parametrize(
    ("searched", "name", "mix"),
    [
        # The marker and the track number the artist's part is read past.
        (f"[MP3] {ARTIST} - Vocal Dub", ARTIST, "Vocal Dub"),
        (f"01 {ARTIST} - Vocal Mix", ARTIST, "Vocal Mix"),
    ],
)
def test_the_self_titled_split_reads_the_artists_part_past_its_marker(searched, name, mix):
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, name, BUCKET_GENRE, mix=mix)])
    assert hit.genre == BUCKET_GENRE
    assert _matches(searched, f"{name} ({mix})")


@pytest.mark.parametrize(
    "title",
    [
        f"{ARTIST} - Summer Mix - 01 Sunrise Mood Extended Mix",
        f"{ARTIST} - Summer Mix - 01 - Sunrise Mood",
    ],
)
def test_a_track_numbered_title_after_a_version_ending_album_is_still_the_title(title):
    """The part before a track numbered title is the album, so this is not the card's shape."""
    assert _matches(title, "Sunrise Mood")
    assert not _matches(title, ARTIST)
    assert not _matches(title, "Summer")


# K. R-1646, review round two: only the artist's own name before a feature keeps it whole


@pytest.mark.parametrize(
    "title",
    ["Sunrise Mood feat. Tide - Bernard Badie", "Sunrise Mood (feat. Tide) - Bernard Badie"],
)
def test_a_title_crediting_a_featured_artist_is_still_read_without_the_credit(title):
    """Round two: read unshed, the name lost "sunrise mood" to another self titled row."""
    assert searchers._title_matches(title, "Sunrise Mood", artist="Tide")


def test_a_title_crediting_a_featured_artist_takes_its_own_genre_listed_first(tmp_path, silence):
    """As on main, listed second the other artist's self titled row wins on page order (R-1636)."""
    rows = [("Sunrise Mood", "Original Mix", BUCKET_GENRE), (ARTIST, "Original Mix", "Techno")]
    both = [{"artist_name": ARTIST}, {"artist_name": "Tide"}]
    listed = [_beatport_track(ARTIST, row, genre, mix=mix) for row, mix, genre in rows]
    beatport = _page([{**row, "artists": both} for row in listed])
    fetch = routed(search=results(), beatport=beatport)
    title = "Sunrise Mood feat. Tide - Bernard Badie"
    assert _written(tmp_path, silence, fetch, title=title, artist="Tide") == BUCKET_GENRE


@pytest.mark.parametrize(
    "searched",
    [f"[MP3] {ARTIST} feat. Tide - Vocal Mix", f"01 {ARTIST} feat. Tide - Vocal Mix"],
)
def test_the_self_titled_split_reads_past_a_marker_and_a_feature_credit_together(searched):
    assert _matches(searched, f"{ARTIST} (Vocal Mix)")
    assert not _matches(searched, ARTIST)


@pytest.mark.parametrize(
    ("title", "own"),
    [
        (f"(Dub Mix) feat. {ARTIST} - Tide", "Dub Mix"),
        (f"(Intro) feat. {ARTIST} - Tide - Album", "(Intro)"),
    ],
)
def test_a_bracketed_title_before_a_feature_is_read_without_the_credit(title, own):
    """The marker strip took the title's brackets too, losing the title's own row."""
    assert _matches(title, own)


# L. U280: a title read once into typed parts, ambiguity an outcome

#: (artist tag, file title, each part's role, the outcome): a name only a version
#: list could read is ambiguous.
PARSED = [
    (ARTIST, "08A - 124 - Sunrise Mood", "head head title", "titled"),
    (ARTIST, f"08A - 124 - {ARTIST} - Sun Path - Original Mix", "head head credit title after", "titled"),
    (ARTIST, f"{ARTIST} - Sun Path - 02 Tide", "credit album title", "titled"),
    (ARTIST, f"{ARTIST} - Sun Path - 02 - Tide", "credit album number title", "titled"),
    (ARTIST, f"01 - {ARTIST} - Sun Path", "number credit title", "titled"),
    (ARTIST, f"{ARTIST} - Original Mix", "title after", "titled"),
    (ARTIST, f"{ARTIST} - {ARTIST} - Sun Path", "title credit after", "titled"),
    (ARTIST, "Sun Path - 08A - 124", "title head head", "titled"),
    (ARTIST, f"Tide - {ARTIST} - Sun Path", "title credit after", "titled"),
    (ARTIST, f"{ARTIST} - Vocal Mix", "credit title", "ambiguous"),
    (ARTIST, f"08A - 124 - {ARTIST} - Sunrise Mood Extended Mix", "head head credit title", "ambiguous"),
    # R-1651: a feature after the version, and two credits before it, hide the shape no longer.
    (ARTIST, f"{ARTIST} - Vocal Mix feat. Tide", "credit title", "ambiguous"),
    (f"{ARTIST} & Tide", f"{ARTIST} - Tide - Sunrise Mood Extended Mix", "credit credit title", "ambiguous"),
    (ARTIST, "()", "", "unreadable"),
]

_ROLE_WORDS = {
    titles.Role.HEAD: "head",
    titles.Role.NUMBER: "number",
    titles.Role.CREDIT: "credit",
    titles.Role.TITLE: "title",
    titles.Role.ALBUM: "album",
    titles.Role.LATER: "after",
}


@pytest.mark.parametrize(("artist", "name", "roles", "outcome"), PARSED)
def test_a_name_is_read_once_into_its_parts(artist, name, roles, outcome):
    read = titles.read_file(name, artist)
    assert " ".join(_ROLE_WORDS[part.role] for part in read.parts) == roles
    assert read.outcome.value == outcome


def test_each_part_says_how_its_role_was_told():
    read = titles.read_file(f"08A - 124 - {ARTIST} - Vocal Mix", ARTIST)
    assert [part.told for part in read.parts] == [
        titles.Told.SHAPE,
        titles.Told.SHAPE,
        titles.Told.CREDIT,
        titles.Told.LIST,
    ]
    titled = titles.read_file(f"{ARTIST} - Sun Path - 02 Tide", ARTIST)
    assert [part.told for part in titled.parts] == [titles.Told.CREDIT, titles.Told.POSITION, titles.Told.POSITION]


def test_a_titled_name_says_where_each_title_it_reads_comes_from():
    read = titles.read_file("08A - 124 - Sunrise Mood - Original Mix", ARTIST)
    assert len(read.titles) == len(read.why) > 0
    assert all(why.startswith("parts ") for why in read.why)


#: (artist tag, file title, a row one reading fits, a row writing the split): R-1651's
#: first two shapes are ambiguous now, so only the split row writes.
R1651 = [
    (ARTIST, f"{ARTIST} - Vocal Mix feat. Tide", "Vocal", f"{ARTIST} (Vocal Mix)"),
    (ARTIST, f"08A - 124 - {ARTIST} - Vocal Mix feat. Tide", "Vocal Mix", f"{ARTIST} (Vocal Mix feat. Tide)"),
    (f"{ARTIST} & Tide", f"{ARTIST} - Tide - Sunrise Mood Extended Mix", ARTIST, "Sunrise Mood (Extended Mix)"),
    (f"{ARTIST} & Tide", f"{ARTIST} - Tide - Sunrise Mood Extended Mix", "Tide", "Sunrise Mood - Extended Mix"),
    (ARTIST, f"{ARTIST} - {ARTIST} - Vocal Mix", ARTIST, f"{ARTIST} (Vocal Mix)"),
]


@pytest.mark.parametrize(("artist", "title", "one_way", "split"), R1651)
def test_a_name_hiding_the_shape_is_ambiguous_too(artist, title, one_way, split):
    assert not searchers._title_matches(title, one_way, artist=artist)
    assert searchers._title_matches(title, split, artist=artist)


@pytest.mark.parametrize("source", ["beatport", "discogs"])
@pytest.mark.parametrize(
    ("artist", "title", "one_way"),
    [(artist, title, one_way) for artist, title, one_way, _ in R1651]
    + [(ARTIST, searched, found) for searched, found in SPLIT_UNCONFIRMED],
)
def test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way(
    tmp_path, silence, source, artist, title, one_way
):
    if source == "beatport":
        rows = [_beatport_track(artist, one_way, BUCKET_GENRE, mix=mix) for mix in ("", "Original Mix")]
        fetch = routed(search=results(), beatport=_page(rows))
    else:
        tracks = [{"position": "A1", "type_": "track", "title": one_way}]
        fetch = routed(search=results(56), releases={56: release(56, tracks=tracks)})
    assert _written(tmp_path, silence, fetch, title=title, artist=artist) is None


# The property: names the naming verb renders find their own row and no other.

#: Titles no catalogue could take for one recording, none a version word, head or
#: artist, one of bracket groups alone (review round one's F6).
GENERATED_TITLES = (
    "Sunrise Mood",
    "Glass Hour",
    "Corner Talk",
    "(Not Just) Knee Deep",
    "909",
    "Kitchen Session 2",
    "Summer 1999",
    "Love Is The Message",
    "Riding The Tide",
    "Shout It Out",
    "Make Luv",
    "Burning Bridges",
    "(Intro)",
    "007 (Interlude)",
)

#: (artist tag, the credit as a name writes it).
GENERATED_CREDITS = (
    (ARTIST, ARTIST),
    (ARTIST, f"{ARTIST} & Tide"),
    (ARTIST, f"Tide & {ARTIST}"),
    (ARTIST, "B. Badie"),
    ("The Black Madonna", "Black Madonna"),
    ("Âme", "Ame"),
    ("Tide", "Tide"),
)

#: The file's version, written after its title, and a catalogue's.
GENERATED_VERSIONS = ("", " (Extended Mix)", " (Kerri Chandler Remix)", " - Original Mix", " [Dub Mix]")
ROW_VERSIONS = ("", " (Extended Mix)", " - Original Mix", " (Original Mix)")
ALBUMS = ("Sun Path", "Night Shapes", "Summer Mix")

#: The bodies a file's name or title tag is written with.
BODIES = (
    "{credit} - {title}",
    "{title} - {credit}",
    "{title} - {credit} - {album}",
    "{credit} - {album} - {number} {title}",
    "{credit} - {album} - {number} - {title}",
    "{number} - {credit} - {title}",
    "{title}",
)

_TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))


def _rendered(chance) -> tuple[str, str, str, str]:
    """One rendered name as the reader asks it: (artist tag, searched title, title, album)."""
    artist, credit = chance.choice(GENERATED_CREDITS)
    title = chance.choice(GENERATED_TITLES)
    album = chance.choice(ALBUMS)
    body = chance.choice(BODIES).format(
        credit=credit,
        title=title + chance.choice(GENERATED_VERSIONS),
        album=album,
        number=f"0{chance.randint(1, 9)}",
    )
    headed = chance.random() < 0.7
    tagged = chance.random() < 0.5
    spec = NameSpec(
        stem=body,
        suffix=".flac",
        key=chance.choice(["8A", "11B", "1A"]) if headed else None,
        bpm=chance.randint(70, 180) if headed else None,
        title=body if tagged and "{credit}" not in body else None,
        lossy=chance.random() < 0.3,
    )
    rendered = render_all(spec, template=_TEMPLATE)
    searched = rendered.title_tag if tagged else rendered.filename.removesuffix(".flac")
    return artist, searched, title, album


def test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other(monkeypatch):
    """Rendered names match their own row only, through the shipped matcher (U306)."""
    monkeypatch.setattr(titles, "read_file", functools.lru_cache(maxsize=None)(titles.read_file))
    monkeypatch.setattr(titles, "read_row", functools.lru_cache(maxsize=None)(titles.read_row))
    chance = random.Random(791)
    for _ in range(3000):
        artist, searched, title, album = _rendered(chance)
        for version in ROW_VERSIONS:
            assert searchers._title_matches(searched, title + version, artist=artist), (searched, title + version)
        others = [other for other in GENERATED_TITLES if other != title]
        wrong = [*(other + chance.choice(ROW_VERSIONS) for other in others), album, "Original Mix", "Extended Mix"]
        wrong += [name for name in ("Bernard Badie", "Tide", "Black Madonna", "Ame") if name not in title]
        for row in wrong:
            assert not searchers._title_matches(searched, row, artist=artist), (searched, row)


#: (artist tag, file title, a row): a whole name is read as written, never shed
#: across its dashes, so a cut feature never leaves the artist alone (R-1646).
WHOLE_NAME_NOT = [
    (f"{ARTIST} & Tide", f"{ARTIST} feat. Someone - Tide - Vocal Mix", ARTIST),
    (f"{ARTIST} & Tide", f"{ARTIST} - Tide feat. Someone - Sunrise Mood Extended Mix", ARTIST),
    (ARTIST, "08A - 124 - Interlude", "08A - 124 - (Intro)"),
    # A tempo is a title only before nothing but a version.
    (ARTIST, "124 - Dub - Sunrise Mood", "124"),
    # Review round one: a track number past the marker across a dash (F1) and a bracket
    # group shed across a dash (F2) each left the artist's name alone.
    (ARTIST, f"[MP3] 01 - {ARTIST} - (Intro)", ARTIST),
    (ARTIST, f"[MP3] 01 - {ARTIST} - Vocal (Live)", ARTIST),
    (ARTIST, f"{ARTIST} - (Intro)", ARTIST),
    (ARTIST, f"{ARTIST} - (Intro) (Live)", ARTIST),
    (ARTIST, f"01A - 150 - (Intro) - {ARTIST} - Night Shapes", ARTIST),
    # A first part naming the artist only as featured is a title only with no head (F3).
    ("Tide", f"08A - 124 - {ARTIST} feat. Tide - Sunrise Mood", ARTIST),
    # Review round two: three figures before brackets are the title's own.
    (ARTIST, "007 (Intro)", "Intro"),
    (ARTIST, "010 (Intro)", "(Intro)"),
    (ARTIST, f"08A - 124 - {ARTIST} - 007 (Intro)", "Intro"),
    # The mutation table's zeros: a number past the marker is its part's own (M29), and
    # a square group is read past only where the naming verb writes its marker (M06).
    (ARTIST, "[MP3] 01 - Original Mix", "Original Mix"),
    (ARTIST, f"{ARTIST} - [Love] Is The Message", "(Hate) Is The Message"),
]
WHOLE_NAME_STILL = [
    # The first part names the artist only as featured: a title featuring them.
    ("Tide", "Sunrise Mood feat. Tide - Bernard Badie", "Sunrise Mood"),
    # A number in a tempo's range before a version alone is a title too.
    (ARTIST, "100 - Original Mix", "100"),
    (ARTIST, "124 - Interlude", "Interlude"),
    (ARTIST, "124 - Interlude", "124"),
    # A track number glued to a title past the marker is still shed.
    (ARTIST, "[MP3] 01 Sunrise Mood", "Sunrise Mood"),
    (ARTIST, f"{ARTIST} - (Intro)", "Intro"),
    (ARTIST, f"[MP3] 01 - {ARTIST} - (Intro)", "(Intro)"),
    # An artist only featured is no credit among several, so the title is read (M11).
    (f"{ARTIST} & Tide", f"08A - 124 - Sunrise Mood (feat. Tide) - {ARTIST} - Vocal Mix", "Sunrise Mood"),
]


def test_a_lossy_file_named_with_a_track_number_takes_no_self_titled_genre(tmp_path, silence):
    """F1: "[MP3] 01 - Artist - (Intro)" read past the marker left the artist's name."""
    rendered = render_all(NameSpec(stem=f"01 - {ARTIST} - (Intro)", suffix=".flac", lossy=True), template=_TEMPLATE)
    fetch = _beatport_and_discogs(ARTIST, 57)

    assert _written(tmp_path, silence, fetch, title=rendered.title_tag) is None
    assert rendered.title_tag == f"[MP3] 01 - {ARTIST} - (Intro)"


@pytest.mark.parametrize(
    "title", [f"{ARTIST} - (Intro)", f"{ARTIST} - (Intro) (Live)", f"{ARTIST} - [Intro]", "007 (Intro)"]
)
def test_beatport_ranks_no_row_by_brackets_shed_across_a_dash(title):
    """Round two: a core read across a dash scored the self titled row above the file's own."""
    rows = [_beatport_track(ARTIST, ARTIST, "Techno"), _beatport_track(ARTIST, "Intro", BUCKET_GENRE)]
    for page in (rows, rows[::-1]):
        assert _beatport_hit(title, page).genre in (BUCKET_GENRE, None)
    assert _beatport_answer(_beatport_hit(title, rows[:1])) == "miss"


@pytest.mark.parametrize(("artist", "title", "own"), CREDIT_WAYS + WHOLE_NAME_STILL)
def test_each_way_a_credit_is_written_is_known(artist, title, own):
    assert searchers._title_matches(title, own, artist=artist)


# U324. A credit spelled with a letter accent stripping leaves alone

#: (artist tag, file title, the credit as a row writes it, the title asked): the
#: tag's artist spelled with a letter NFKD leaves whole, written plain on one side,
#: and an initial the fold spells with two letters still stands for its word. The
#: question reads past the artist's name alone, never a collaboration or an initial.
FOLDED_CREDITS = (
    ("Trentemøller", "08A - 124 - Trentemoller - Sun Path", "Trentemoller", "Sun Path"),
    ("Trentemoller", "08A - 124 - Trentemøller - Sun Path", "Trentemøller", "Sun Path"),
    (
        "Łukasz Bloom",
        "08A - 124 - Lukasz Bloom & Tide - Sun Path",
        "Lukasz Bloom & Tide",
        "Lukasz Bloom & Tide - Sun Path",
    ),
    ("Straße Bloom", "08A - 124 - Strasse Bloom - Sun Path", "Strasse Bloom", "Sun Path"),
    ("Æther", "08A - 124 - [MP3] Aether - Sun Path", "Aether", "Sun Path"),
    ("Þórður Badie", "08A - 124 - Þ. Badie - Sun Path", "Þ Badie", "Þ. Badie - Sun Path"),
    ("Æsop Badie", "08A - 124 - Æ. Badie - Sun Path", "Æ Badie", "Æ. Badie - Sun Path"),
    # A table letter carrying an accent as well is an initial, as on main.
    ("Æsir Badie", "08A - 124 - Ǽ. Badie - Sun Path", "Ǽ Badie", "Ǽ. Badie - Sun Path"),
    ("Ǣsir Badie", "08A - 124 - Ǣ. Badie - Sun Path", "Ǣ Badie", "Ǣ. Badie - Sun Path"),
)


@pytest.mark.parametrize(("artist", "title", "credit", "asked"), FOLDED_CREDITS)
def test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists(artist, title, credit, asked):
    assert searchers._title_matches(title, "Sun Path", artist=artist)
    assert not searchers._title_matches(title, credit, artist=artist)
    assert titles.question(title, artist).title == asked


#: (artist tag, file title, a row): a folded name is no wider than its letters.
NOT_FOLDED = [
    # "o" is not "oe": a fold reads a letter one way only.
    ("Trentemøller", "08A - 124 - Trentemoeller - Sun Path", "Sun Path"),
    ("Straße Bloom", "08A - 124 - Strase Bloom - Sun Path", "Sun Path"),
    # An initial stands only for a word it opens (the mutation table's F20).
    ("Þórður Badie", "08A - 124 - Æ. Badie - Sun Path", "Sun Path"),
    ("Bernard Badie", "08A - 124 - C. Badie - Sun Path", "Sun Path"),
    # A word outside the table folding to two letters is no initial, as on main.
    ("Ijsbrand Badie", "08A - 124 - Ĳ. Badie - Sun Path", "Sun Path"),
    # A title holding the folded name is still a title.
    ("Trentemøller", "08A - 124 - Trentemoller Theme - Sun Path", "Sun Path"),
]


@pytest.mark.parametrize(("artist", "title", "row"), NOT_A_CREDIT + WHOLE_NAME_NOT + NOT_FOLDED)
def test_a_whole_name_is_never_shed_across_its_dashes(artist, title, row):
    """Not the artist's credit, never shed across its dashes, nor wider than its letters."""
    assert not searchers._title_matches(title, row, artist=artist)
