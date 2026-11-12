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
groups from the end; a catalogue row's dash tail, or any run of the file's dash
segments, since the live library writes its ``KEY - BPM - `` head into the
title tag; a feature credit; a trailing run of the domain's version words; its
leading bracket groups. Nothing is compared by characters, and a word read only
inside the other title's brackets is never its title. A side with no letter or
digit matches nothing. A title that matched its own row before still does,
which the tables below drive on every source, the headed title included. The
one kind known lost is a title written only inside the other's trailing
brackets ("How Does It Feel" against "Untitled (How Does It Feel)"), whose
evidence is the same as the wrong shape "Intro" against "Sunrise Mood
(Intro)", pinned below as a known cost.

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
]


@pytest.mark.parametrize(("searched", "found"), SAME)
def test_a_title_matches_its_own_recording_either_way_round(searched, found):
    assert searchers._title_matches(searched, found)
    assert searchers._title_matches(found, searched)


@pytest.mark.parametrize(("searched", "found"), DIFFERENT)
def test_a_title_matches_no_other_recording_either_way_round(searched, found):
    assert not searchers._title_matches(searched, found)
    assert not searchers._title_matches(found, searched)


@pytest.mark.parametrize(("searched", "found"), HEADED)
def test_a_headed_file_title_matches_its_own_row(searched, found):
    assert searchers._title_matches(searched, found)


@pytest.mark.parametrize(("searched", "found"), HEADED_NOT)
def test_a_files_head_is_never_its_title(searched, found):
    assert not searchers._title_matches(searched, found)
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
    assert not searchers._title_matches(searched, found)
    assert not searchers._title_matches(found, searched)
    assert searchers._title_matches(f"{searched}!", searched)


def test_a_catalogue_rows_dash_tail_is_never_its_title():
    """A catalogue writes a version after a dash; a file writes its head before
    one. So the row is read by its head and the file by any run of its
    segments, and a tail of version words alone is no title on either side."""
    assert not searchers._title_matches("Original Mix", f"{OTHER} - Original Mix")
    assert not searchers._title_matches(f"{OTHER} - Original Mix", "Original Mix")
    assert searchers._title_matches(f"{OTHER} - Original Mix", OTHER)
    assert searchers._title_matches(OTHER, f"{OTHER} - Original Mix")
    assert not searchers._title_matches("Hate", "Love - Hate")


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
    assert not searchers._title_matches("How Does It Feel", name)


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
]


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
