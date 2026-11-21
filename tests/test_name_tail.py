"""R-1724: a file asked by its name is asked with the title the name carries,
never the ``_PN`` tail the older naming wrote after it.

Measured at sitting 101: 5,637 of the library's 10,997 audio files end their
name in ``_PN``, 1,692 of them right after a bracket group, and 3 of the 4
by-name misses of job ``2026-11-21T15:04:44Z-c032`` were asked as
"Attention_PN", "Promise to Stay Here_PN" and "Sunshine Hotel_PN". The tail
also kept Discogs from setting a mix aside, and the shared matcher read
``mix)_pn`` as the title's words, so "On The Rocks (Cafe Del Mar Mix)_PN"
matched no release of "On The Rocks (Cafe Del Mar Mix)".

WHAT THIS SUITE GUARDS, the card's merge blockers first:

* A NAME LOSES ITS TAIL, in the question every source is asked and in the
  text every row is matched against, through ``tag folder`` and ``tag
  retag`` alike, so the Obiman release is the file's own.
* A TITLE TAG IS NEVER TOUCHED: a tag ending in "_PN" is asked as written.
* A NAME WITH NO TAIL IS READ EXACTLY AS BEFORE, byte for byte, and every
  case of the matcher's corpus keeps its verdict.
* A NAME WHOSE TITLE IS THE TAIL ALONE ASKS NO CATALOGUE, and keeps its
  ISRC's question of the general catalogue.

Nothing here touches the network; the token is a fixture word.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

from cratekit.core import review, tags
from cratekit.tagging import retag, searchers, tag, titles
from tests._containers import synth_container
from tests.test_catalogue_searcher import _beatport_page
from tests.test_discogs_question import beatport_queries, build, discogs_questions, genre_of, tagged
from tests.test_discogs_searcher import release, results
from tests.test_genre_retag import CATCH_ALL, SPECIFIC, answering, place
from tests.test_genre_retag import TAXONOMY as RETAG_TAXONOMY
from tests.test_title_matcher import DIFFERENT, HEADED, HEADED_NOT, SAME

SUNSHINE = "06A - 126 - Sean Doron - Sunshine Hotel_PN"
OBIMAN = "9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN"
OBIMAN_RELEASE = "On The Rocks (Cafe Del Mar Mix)"
OBIMAN_STYLE = "Balearic"


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    out = tmp_path / "Music"
    out.mkdir()
    return out


@pytest.fixture
def store(tmp_path):
    with review.open_store(path=tmp_path / "review.db") as opened:
        yield opened


def answering_every_question(seen: list[str]):
    """A Discogs that answers the Obiman release whatever it is asked.

    So a miss is the shared matcher's, never the search's: on main the
    release came back and its track was read as no part of the file's
    name, because the name's title read ``mix)_pn``.
    """
    tracks = [{"position": "A1", "type_": "track", "title": OBIMAN_RELEASE}]

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.DISCOGS_SEARCH):
            return searchers.Fetched(text=results(14), status=200)
        if url == f"{searchers.DISCOGS_RELEASE}14":
            page = release(
                14, artist="Obiman", title=OBIMAN_RELEASE, tracks=tracks, styles=(OBIMAN_STYLE,)
            )
            return searchers.Fetched(text=page, status=200)
        return searchers.Fetched(text=_beatport_page([]), status=200)

    return fetch


def typed(seen: list[str], wanted: dict[tuple[str, str], str]):
    """A Discogs that answers a release only for the artist and track a
    person types, as sent: ``wanted`` maps one to the release's title, its
    track and its style ``Balearic``. Every other source answers nothing."""
    numbered = {question: 20 + index for index, question in enumerate(wanted)}
    pages = {
        f"{searchers.DISCOGS_RELEASE}{numbered[question]}": release(
            numbered[question],
            artist=question[0],
            title=title,
            tracks=[{"position": "A1", "type_": "track", "title": title}],
            styles=(OBIMAN_STYLE,),
        )
        for question, title in wanted.items()
    }

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.DISCOGS_SEARCH):
            asked = parse_qs(urlsplit(url).query, keep_blank_values=True)
            number = numbered.get((asked["artist"][0], asked["track"][0]))
            return searchers.Fetched(text=results(*(() if number is None else (number,))), status=200)
        if url in pages:
            return searchers.Fetched(text=pages[url], status=200)
        return searchers.Fetched(text=_beatport_page([]), status=200)

    return fetch


# ---------------------------------------------------------------------------
# A. The reading: the title a file's name carries
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("stem", "title"),
    [
        (SUNSHINE, "06A - 126 - Sean Doron - Sunshine Hotel"),
        (OBIMAN, "9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)"),
        ("Attention_PN", "Attention"),
        ("Promise to Stay Here_PN", "Promise to Stay Here"),
        ("Sunrise Mood _PN", "Sunrise Mood"),
        ("8A - 124 - [MP3] Lane 8 - Aba_PN", "8A - 124 - [MP3] Lane 8 - Aba"),
        ("Sunrise Mood [Nightwave Remix]_PN", "Sunrise Mood [Nightwave Remix]"),
    ],
)
def test_a_name_loses_the_tail_after_its_title(stem, title):
    assert titles.name_title(stem) == title


@pytest.mark.parametrize(
    "stem",
    [
        "Sunrise Mood",
        "9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)",
        # Only the older naming's own tail, exactly as it wrote it.
        "Sunrise Mood_pn",
        "Sunrise Mood PN",
        "Sunrise Mood_PNX",
        "Sunrise Mood_PN (1)",
        "PN",
        "Sunrise_PN Mood",
        "Sunrise Mood - PN",
        " Sunrise Mood ",
        "",
    ],
)
def test_a_name_with_no_tail_is_read_byte_for_byte(stem):
    assert titles.name_title(stem) is stem


@pytest.mark.parametrize(
    "stem", ["_PN", " _PN", "8A - 124 - Sean Doron - _PN", "Sean Doron - _PN", "8A - 124 - _PN"]
)
def test_a_name_whose_title_is_the_tail_alone_reads_no_title(stem):
    assert titles.name_title(stem) == ""
    assert titles.by_name(stem) == titles.Question("", "", titles.Read.NO_TITLE)


@pytest.mark.parametrize(
    ("stem", "asked"),
    [
        (SUNSHINE, titles.Question("Sean Doron", "Sunshine Hotel", titles.Read.BY_NAME)),
        (OBIMAN, titles.Question("Obiman", OBIMAN_RELEASE, titles.Read.BY_NAME)),
        ("8A - 124 - [MP3] Lane 8 - Aba_PN", titles.Question("Lane 8", "Aba", titles.Read.BY_NAME)),
        (
            "8A - 124 - Make Luv - Room 5 - Album_PN",
            titles.Question("", "Make Luv - Room 5 - Album", titles.Read.NAME_AMBIGUOUS),
        ),
        ("Sunshine Hotel_PN", titles.Question("", "Sunshine Hotel", titles.Read.AS_WRITTEN)),
        ("8A - 124_PN", titles.Question("", "8A - 124", titles.Read.HEAD_ALONE)),
    ],
)
def test_the_name_read_reads_past_the_tail(stem, asked):
    assert titles.by_name(stem) == asked


@pytest.mark.parametrize(
    ("stem", "asked"),
    [
        ("06A - 126 - Sean Doron - Sunshine Hotel", ("Sean Doron", "Sunshine Hotel", "by-name")),
        ("Sunshine Hotel", ("", "Sunshine Hotel", "as-written")),
        ("8A - 124 - Make Luv - Room 5 - Album", ("", "Make Luv - Room 5 - Album", "name-ambiguous")),
        ("8A - 124", ("", "8A - 124", "head-alone")),
    ],
)
def test_the_name_read_of_a_name_with_no_tail_is_unchanged(stem, asked):
    found = titles.by_name(stem)
    assert (found.artist, found.title, found.read.value) == asked


# ---------------------------------------------------------------------------
# B. The card's scenarios, through tag_one and the shipped searcher
# ---------------------------------------------------------------------------


def test_sunshine_hotel_is_asked_by_its_artist_and_title_and_no_source_sees_the_tail(
    tmp_path, silence
):
    path = tagged(tmp_path, silence, f"{SUNSHINE}.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed(seen, {})))
    (question,) = discogs_questions(seen)
    assert (question["artist"], question["track"]) == ("Sean Doron", "Sunshine Hotel")
    # The record shop is asked the same question, past the tail.
    assert beatport_queries(seen) and all("Sunshine+Hotel" in url for url in beatport_queries(seen))
    assert not any("PN" in url for url in seen)
    assert (result.asked_artist, result.asked_title, result.asked_read) == (
        "Sean Doron",
        "Sunshine Hotel",
        titles.Read.BY_NAME.value,
    )


def test_the_obiman_name_is_asked_its_title_and_takes_the_release_a_person_would_type(
    tmp_path, silence
):
    """Discogs sets the mix aside once the tail no longer follows it, and the
    release a person finds by typing "On The Rocks" is the file's own."""
    path = tagged(tmp_path, silence, f"{OBIMAN}.flac")
    seen: list[str] = []
    fetch = typed(seen, {("Obiman", "On The Rocks"): OBIMAN_RELEASE})
    result = tag.tag_one(path, searcher=build(fetch))
    assert discogs_questions(seen)[0] == {
        "type": "release",
        "artist": "Obiman",
        "track": "On The Rocks",
        "per_page": "10",
    }
    assert (result.asked_artist, result.asked_title, result.asked_read) == (
        "Obiman",
        OBIMAN_RELEASE,
        titles.Read.BY_NAME.value,
    )
    assert (result.source, result.source_genre) == (searchers.DISCOGS, OBIMAN_STYLE)
    assert result.genre_written == genre_of(OBIMAN_STYLE)
    assert tags.read_genre_from_file(path) == genre_of(OBIMAN_STYLE)


def test_the_obiman_name_matches_its_release_whatever_discogs_is_asked(tmp_path, silence):
    """The match half alone: Discogs answers the release to any question, so
    the file takes it only if the name's title is read past its tail."""
    path = tagged(tmp_path, silence, f"{OBIMAN}.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(answering_every_question(seen)))
    assert (result.source, result.source_genre) == (searchers.DISCOGS, OBIMAN_STYLE)
    assert result.genre_written == genre_of(OBIMAN_STYLE)


def test_a_title_tag_ending_in_the_tail_is_asked_and_matched_as_written(tmp_path, silence):
    path = tagged(
        tmp_path,
        silence,
        f"{OBIMAN}.flac",
        title="On The Rocks (Cafe Del Mar Mix)_PN",
        artist="Obiman",
    )
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(answering_every_question(seen)))
    assert discogs_questions(seen)[0]["track"] == "On The Rocks (Cafe Del Mar Mix)_PN"
    assert result.asked_title == "On The Rocks (Cafe Del Mar Mix)_PN"
    # Matched against the tag as written, as on main: the tail reads as words.
    assert result.genre_written is None
    assert result.skipped == tag.NO_HIT


def test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail(
    tmp_path, silence
):
    path = tagged(tmp_path, silence, "Sunshine Hotel_PN.flac", artist="Sean Doron")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed(seen, {})))
    (question,) = discogs_questions(seen)
    assert (question["artist"], question["track"]) == ("Sean Doron", "Sunshine Hotel")
    assert (result.asked_title, result.asked_read) == ("Sunshine Hotel", titles.Read.AS_WRITTEN.value)


def test_a_name_with_no_tail_is_asked_as_before(tmp_path, silence):
    path = tagged(tmp_path, silence, "06A - 126 - Sean Doron - Sunshine Hotel.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed(seen, {})))
    (question,) = discogs_questions(seen)
    assert (question["artist"], question["track"]) == ("Sean Doron", "Sunshine Hotel")
    assert result.asked_read == titles.Read.BY_NAME.value


def test_a_name_whose_title_is_the_tail_alone_asks_no_catalogue(tmp_path, silence):
    path = tagged(tmp_path, silence, "8A - 124 - Sean Doron - _PN.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(answering_every_question(seen)))
    assert seen == []
    assert result.genre_written is None
    assert result.skipped == tag.NO_HIT
    assert (result.asked_artist, result.asked_title, result.asked_read) == (
        "",
        "",
        titles.Read.NO_TITLE.value,
    )
    assert tags.read_genre_from_file(path) in (None, "")


def test_a_name_that_reads_no_title_still_asks_the_general_catalogue_its_isrc(tmp_path, silence):
    """Its ISRC is no part of its name, so the question by ISRC the file was
    asked before is asked still; only the artist and title question goes."""
    path = tagged(tmp_path, silence, "_PN.flac", isrc="GBAAA2600001")
    asked: list[tuple[tag.SearchHit, str | None]] = []

    def published(hit: tag.SearchHit, isrc: str | None) -> tag.SearchHit:
        asked.append((hit, isrc))
        return tag.SearchHit(genre="House", source="isrc fixture", source_genre="House")

    result = tag.tag_one(path, searcher=build(answering_every_question([])), published=published)
    ((hit, isrc),) = asked
    assert isrc == "GBAAA2600001"
    assert hit.genre is None and hit.answers == ()
    assert result.genre_written == "House"


# ---------------------------------------------------------------------------
# C. The matcher's corpus: no verdict moves, and a tail is read off a name
# ---------------------------------------------------------------------------

CORPUS = [*SAME, *DIFFERENT, *HEADED, *HEADED_NOT]
MATCHING = [*SAME, *HEADED]


@pytest.mark.parametrize(("searched", "found"), CORPUS)
def test_every_corpus_name_with_no_tail_reads_as_written(searched, found):
    assert titles.name_title(searched) is searched


@pytest.mark.parametrize(("searched", "found"), MATCHING)
def test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it(searched, found):
    named = titles.name_title(f"{searched}_PN")
    assert named == searched.rstrip()
    assert titles.matches(titles.read_file(named, "Bernard Badie"), titles.read_row(found))


# ---------------------------------------------------------------------------
# D. tag retag reads a name the same way
# ---------------------------------------------------------------------------


def test_retag_asks_a_file_with_no_title_tag_its_name_past_the_tail(folder, silence, store):
    path = place(folder, silence, "Sunshine Hotel_PN", CATCH_ALL)
    searcher = answering({"Sunshine Hotel": SPECIFIC})
    retag.retag_folder(folder, searcher=searcher, declared=RETAG_TAXONOMY, store=store)
    assert searcher.asked == [("", "Sunshine Hotel")]
    assert tags.read_genre_from_file(path) == SPECIFIC


def test_retag_asks_a_title_tag_ending_in_the_tail_as_written(folder, silence, store):
    path = place(folder, silence, "x", CATCH_ALL)
    tags.write_tags(path, {"title": "Sunshine Hotel_PN"})
    searcher = answering({})
    retag.retag_folder(folder, searcher=searcher, declared=RETAG_TAXONOMY, store=store)
    assert searcher.asked == [("", "Sunshine Hotel_PN")]


def test_retag_asks_no_catalogue_about_a_name_whose_title_is_the_tail_alone(folder, silence, store):
    path = place(folder, silence, "Sean Doron - _PN", CATCH_ALL)
    searcher = answering({"": SPECIFIC})
    retag.retag_folder(folder, searcher=searcher, declared=RETAG_TAXONOMY, store=store)
    assert searcher.asked == []
    assert tags.read_genre_from_file(path) == CATCH_ALL

