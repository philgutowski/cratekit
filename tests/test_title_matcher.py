"""R-1534 and R-1631: a title matches only its own recording, in every source.

THE DEFECTS. The shared matcher stripped a trailing bracket from the first "("
to the last ")" and then compared the two titles by raw substring. A title that
starts and ends with a bracket stripped to the empty string, which is in every
title (R-1534). A title with a bracket in mid title was cut at it, so "Knee
(Not Just) Deep (Part 1)" read as "knee", in "Knee Slapper"; a containment
between whole titles read a word inside one title's brackets as the other
title ("Intro" in "Sunrise Mood (Intro)"), refused only for a hand list of
version words that missed "vocal", "acapella", "reprise" and more; and two
titles compared by characters, so "Club" was in "Nightclub" and "Original Mix"
in "Sunrise Mood - Original Mix" (R-1631). Each wrote another recording's genre
onto the file for good, since a genre is fill if empty.

WHAT HOLDS NOW. Two titles match when they name the same words once each has
shed what is not its title: its trailing bracket groups, read as balanced
groups from the end; a catalogue row's dash tail; the file's head, the
``KEY - BPM - `` the live library writes into the title tag, and every dash
part of it that is not its title, the searched artist's name, a version, an
album (R-1636); a feature credit; a trailing run of the domain's version words; its
leading bracket groups. Nothing is compared by characters, and a word read only
inside the other title's brackets is never its title. A side with no letter or
digit matches nothing, and a number is part of the title. The tables below
drive the shapes the matcher must keep on every source, the headed title
included. What it gives up is recorded in R-1631's residuals: a title written
only inside the other's trailing brackets ("How Does It Feel" against
"Untitled (How Does It Feel)"), whose evidence is the same as the wrong shape
"Intro" against "Sunrise Mood (Intro)", pinned below as a known cost, and some
shapes of a file with no title tag, asked by its name.

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


def _matches(searched: str, found: str) -> bool:
    """The shared matcher for a file by the suite's artist, as every source asks it."""
    return searchers._title_matches(searched, found, artist=ARTIST)


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

#: (file title, catalogue row) pairs that name the same recording, read one way
#: round: the file's title carries a head before a dash, the ``KEY - BPM - ``
#: the live library writes into the title tag or the "Artist - Title" stem of a
#: file with no title tag, and a catalogue row never does.
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

#: (file title, catalogue row) pairs that name different recordings, read one
#: way round: what the file's head is, a key, a tempo or an artist's name, is
#: never its title, and a row that is the artist's name and another title is
#: never the file's.
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


@pytest.mark.parametrize(("searched", "found"), HEADED_NOT)
def test_a_files_head_is_never_its_title(searched, found):
    assert not _matches(searched, found)
    assert _traxsource_hit(searched, found).genre is None
    assert _bandcamp_hit(searched, found).genre is None
    assert discogs_answer(_discogs_hit(searched, found)).answer == "miss"
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
    """The pairs R-1534 pinned as a known residual, two cores matched by raw
    substring. A title is its words, so a word inside another word is no
    match, and a title is never a part of another title's words."""
    assert not _matches(searched, found)
    assert not _matches(found, searched)
    assert _matches(f"{searched}!", searched)


def test_a_catalogue_rows_dash_tail_is_never_its_title():
    """A catalogue writes a version after a dash; a file writes its head before
    one. So the row is read by its head and the file from where its title
    starts, and a tail of version words alone is no title on either side."""
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
    """Not a property to keep: a known cost of R-1631, recorded as a residual.
    "How Does It Feel" against "Untitled (How Does It Feel)" carries the same
    evidence as "Intro" against "Sunrise Mood (Intro)", a title read only inside
    the other's brackets, and only a list of version words could tell the two
    apart, so both are refused. Pinned so a change to it is seen."""
    name = "Untitled (How Does It Feel)"
    hit = _beatport_hit("How Does It Feel", [_beatport_track(ARTIST, name, BUCKET_GENRE)])
    assert _beatport_answer(hit) == "miss"
    assert not _matches("How Does It Feel", name)


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


def test_bandcamp_never_reads_a_headings_artist_as_its_title():
    """A heading "Artist - Friday Night Mix" read whole is the artist's name
    and a version; the file asked by its name "KEY - BPM - Artist - Title"
    carries the same name, and the two met on it."""
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


@pytest.mark.parametrize(("searched", "found"), SAME + HEADED)
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


#: (file title, another recording by the artist) pairs R-1631 drove to a wrong
#: genre written through ``tag_one``.
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
    """Round one: the top tier read the head's words too, so a headed title
    never reached it, and page order chose between the file's own row and
    another by the artist."""
    path = tmp_path / "a.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": title})
    rows = [
        _beatport_track(ARTIST, other, "Techno", mix="Original Mix"),
        _beatport_track(ARTIST, own, BUCKET_GENRE, mix=mix),
    ]
    fetch = routed(search=results(), beatport=searchers.Fetched(text=_beatport_page(rows), status=200))

    result = tag.tag_one(path, searcher=searcher(fetch))

    assert result.genre_written == BUCKET_GENRE
    assert tags.read_genre_from_file(path) == BUCKET_GENRE


@pytest.mark.parametrize(("title", "other"), R1631_WRITES)
def test_a_file_takes_no_genre_off_another_recording_named_in_its_title(
    tmp_path, silence, title, other
):
    """R-1631, as its review drove it: Beatport's row and Discogs' track are
    another recording by the artist, and neither may write its genre."""
    path = tmp_path / "a.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": title})
    beatport = searchers.Fetched(
        text=_beatport_page([_beatport_track(ARTIST, other, BUCKET_GENRE, mix="Original Mix")]),
        status=200,
    )
    tracks = [{"position": "A1", "type_": "track", "title": other}]
    fetch = routed(search=results(44), releases={44: release(44, tracks=tracks)}, beatport=beatport)

    result = tag.tag_one(path, searcher=searcher(fetch))

    assert result.genre_written is None
    assert tags.read_genre_from_file(path) is None


@pytest.mark.parametrize("source", ["beatport", "discogs"])
def test_a_file_whose_title_tag_carries_its_head_still_takes_its_own_genre(
    tmp_path, silence, source
):
    """The live library writes ``KEY - BPM - `` into the title tag, so a file
    is asked by that title and must still find its own row on either source."""
    path = tmp_path / "a.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": "04A - 126 - Burning (Extended Mix)"})
    if source == "beatport":
        rows = [
            _beatport_track(ARTIST, "Burning Bridges", "Techno", mix="Original Mix"),
            _beatport_track(ARTIST, "Burning", BUCKET_GENRE, mix="Extended Mix"),
        ]
        fetch = routed(search=results(), beatport=searchers.Fetched(text=_beatport_page(rows), status=200))
    else:
        tracks = [
            {"position": "A1", "type_": "track", "title": "Burning Bridges"},
            {"position": "A2", "type_": "track", "title": "Burning (Extended Mix)"},
        ]
        fetch = routed(search=results(45), releases={45: release(45, tracks=tracks)})

    result = tag.tag_one(path, searcher=searcher(fetch))

    assert result.genre_written is not None
    assert tags.read_genre_from_file(path) == result.genre_written


# ---------------------------------------------------------------------------
# F. R-1636: a dash part of the file's title that is not its title
# ---------------------------------------------------------------------------

#: (file title, another recording by the artist) pairs in which the file's
#: title was read from a dash part that is not its title: a version tail with a
#: word the version list lacks ("vocal"), the album of an untagged "KEY - BPM -
#: Title - Artist - Album" name, or the artist of a "KEY - BPM - Artist -
#: Title" name. R-1631's review drove the first two shapes to a wrong genre
#: through ``tag_one``.
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

#: (file title, its own row) pairs the same rule must keep: the title after the
#: head, after the artist's part, before a version, an artist or an album, a
#: self titled record, and the track numbered title of an untagged name.
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
    assert not _matches(searched, found)
    assert _traxsource_hit(searched, found).genre is None
    assert _bandcamp_hit(searched, found).genre is None
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre is None
    assert discogs_answer(_discogs_hit(searched, found)).answer == "miss"
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE)])
    assert _beatport_answer(hit) == "miss"


@pytest.mark.parametrize(("searched", "found"), OWN_TITLE)
def test_a_files_title_among_its_dash_parts_still_finds_its_own_row(searched, found):
    assert _matches(searched, found)
    assert _traxsource_hit(searched, found).genre == BUCKET_GENRE
    assert _bandcamp_hit(searched, f"{ARTIST} - {found}").genre == BUCKET_GENRE
    assert discogs_answer(_discogs_hit(searched, found)).answer == "matched"
    hit = _beatport_hit(searched, [_beatport_track(ARTIST, found, BUCKET_GENRE)])
    assert hit.genre == BUCKET_GENRE


def test_the_artists_part_is_read_word_for_word_never_by_characters():
    """Only a part that is the artist's name is passed over: "Badie" is not
    "Bernard Badie", so it is the title, and its later part is not."""
    assert _matches("08A - 124 - Badie - Sun Path", "Badie")
    assert not _matches("08A - 124 - Badie - Sun Path", "Sun Path")


def test_a_name_with_no_artist_is_read_from_its_first_part():
    """With no artist to tell "Artist - Title" from "Title - Version", the part
    after the first is never read alone: a miss, never another recording."""
    assert not searchers._title_matches("Other Song - Vocal Mix", "Vocal", artist="")
    assert searchers._title_matches("Other Song - Vocal Mix", "Other Song", artist="")
    assert not searchers._title_matches(f"{ARTIST} - Sun Path", ARTIST, artist="")


def _file(tmp_path: Path, silence: Path, name: str, wanted: dict[str, str]) -> Path:
    path = tmp_path / f"{name}.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, wanted)
    return path


def _beatport_and_discogs(row: str, number: int):
    beatport = searchers.Fetched(
        text=_beatport_page([_beatport_track(ARTIST, row, BUCKET_GENRE, mix="Original Mix")]),
        status=200,
    )
    tracks = [{"position": "A1", "type_": "track", "title": row}]
    return routed(search=results(number), releases={number: release(number, tracks=tracks)}, beatport=beatport)


@pytest.mark.parametrize(("title", "other"), NOT_THE_TITLE)
def test_a_files_title_tag_writes_no_genre_off_a_dash_part_that_is_not_its_title(
    tmp_path, silence, title, other
):
    """The card's shapes as R-1631's review drove them: Beatport's row and
    Discogs' track are another recording by the artist, and neither may write
    its genre onto a file whose title tag carries the shape."""
    path = _file(tmp_path, silence, "a", {"artist": ARTIST, "title": title})

    result = tag.tag_one(path, searcher=searcher(_beatport_and_discogs(other, 46)))

    assert result.genre_written is None
    assert tags.read_genre_from_file(path) is None


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
    """A file with no title tag is asked by its name, which carries its album
    and its artist as dash parts; neither is its title."""
    path = _file(tmp_path, silence, name, {"artist": ARTIST})
    assert tags.read_tag(path, "title") is None

    result = tag.tag_one(path, searcher=searcher(_beatport_and_discogs(other, 47)))

    assert result.genre_written is None
    assert tags.read_genre_from_file(path) is None


@pytest.mark.parametrize(
    ("name", "own"),
    [
        (f"08A - 124 - Tide - {ARTIST} - Sun Path", "Tide"),
        (f"08A - 124 - {ARTIST} - Sun Path", "Sun Path"),
        (f"{ARTIST} - Sun Path - 02 Tide", "Tide"),
    ],
)
def test_an_untagged_file_still_takes_its_own_rows_genre_by_its_name(tmp_path, silence, name, own):
    path = _file(tmp_path, silence, name, {"artist": ARTIST})

    result = tag.tag_one(path, searcher=searcher(_beatport_and_discogs(own, 48)))

    assert result.genre_written == BUCKET_GENRE
    assert tags.read_genre_from_file(path) == BUCKET_GENRE


# ---------------------------------------------------------------------------
# G. R-1636, review round one: the artist's part as a name writes it
# ---------------------------------------------------------------------------

#: (artist tag, file title, its own row): the artist's part of the title is
#: the tag's artist written as a name writes it, a collaboration, "The", an
#: accent, the naming verb's "[MP3]" marker, a track number before it, or a
#: track number written as its own part. Each found its own row on main and
#: lost it at round one's head.
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
    path = _file(tmp_path, silence, name, {"artist": ARTIST})

    result = tag.tag_one(path, searcher=searcher(_beatport_and_discogs(own, 49)))

    assert result.genre_written == BUCKET_GENRE
    assert tags.read_genre_from_file(path) == BUCKET_GENRE


def test_a_self_titled_tracks_dash_version_the_list_lacks_still_finds_its_own_row(tmp_path, silence):
    """Round one's B1: "Artist - Vocal Mix" is either a title "Vocal Mix" or a
    self titled track and its version, and nothing but a list tells them
    apart, so both are read, as on main. The file's own row listed first wins,
    as it did on main, and the self titled reading is never taken when the
    other part does not end in a version."""
    title = f"08A - 124 - {ARTIST} - Vocal Mix"
    assert _matches(title, ARTIST)
    assert _matches(title, f"{ARTIST} (Extended Mix)")
    assert not _matches(f"08A - 124 - {ARTIST} - Sun Path", ARTIST)
    path = _file(tmp_path, silence, "a", {"artist": ARTIST, "title": title})
    rows = [
        _beatport_track(ARTIST, ARTIST, BUCKET_GENRE, mix="Extended Mix"),
        _beatport_track(ARTIST, "Vocal", "Techno"),
    ]
    fetch = routed(search=results(), beatport=searchers.Fetched(text=_beatport_page(rows), status=200))

    result = tag.tag_one(path, searcher=searcher(fetch))

    assert result.genre_written == BUCKET_GENRE


@pytest.mark.parametrize(
    ("artist", "title", "own", "other"),
    [
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
    ],
)
def test_each_rule_of_the_title_start_holds(artist, title, own, other):
    assert searchers._title_matches(title, own, artist=artist)
    assert not searchers._title_matches(title, other, artist=artist)


# ---------------------------------------------------------------------------
# H. R-1636, review round two: a title holding the artist's name, and where
#    the both ways reading stops
# ---------------------------------------------------------------------------

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


@pytest.mark.parametrize(("artist", "title", "own", "other"), ROUND_TWO)
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
    path = _file(tmp_path, silence, "a", {"artist": artist, "title": title})
    beatport = searchers.Fetched(
        text=_beatport_page([_beatport_track(artist, other, BUCKET_GENRE, mix="Original Mix")]), status=200
    )
    tracks = [{"position": "A1", "type_": "track", "title": other}]
    fetch = routed(search=results(50), releases={50: release(50, tracks=tracks)}, beatport=beatport)

    result = tag.tag_one(path, searcher=searcher(fetch))

    assert result.genre_written is None
    assert tags.read_genre_from_file(path) is None


@pytest.mark.parametrize(
    ("artist", "title", "own"),
    [
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
    ],
)
def test_each_way_a_credit_is_written_is_known(artist, title, own):
    assert searchers._title_matches(title, own, artist=artist)


@pytest.mark.parametrize(
    ("artist", "title", "other"),
    [
        (ARTIST, "08A - 124 - B. Badie - Sun Path", "B Badie"),
        (ARTIST, f"{ARTIST} - Sun Path - 02 - {ARTIST}", "Sun Path"),
        (ARTIST, "08A - 124 - Badie - Sun Path", "Sun Path"),
        ("Tide", "08A - 124 - Love And Tides - Sun Path", "Sun Path"),
        # "with" and "and" are in titles: a title is never taken for a credit.
        (ARTIST, f"{ARTIST} - Dancing With {ARTIST}", ARTIST),
        (ARTIST, f"08A - 124 - Love And {ARTIST} - Sun Path", "Sun Path"),
    ],
)
def test_what_is_not_the_artists_credit_is_never_passed_over(artist, title, other):
    assert not searchers._title_matches(title, other, artist=artist)
