"""U289: a tag sweep asks Discogs with the title read past its ``KEY - BPM`` head.

Measured at sitting 100: twenty library files, their genres cleared and four
of them stripped of title and artist, swept with ``tag folder``. Discogs was
asked about nineteen and matched none, because the title tag the naming verb
writes, ``03B - 83 - That's the Way of the World``, went into its structured
``track`` field as written, and a file with no tags was asked by its whole
stem with an empty artist. Asked again with the head off the title, and the
untagged names split into artist and title, fifteen of twenty matched.

WHAT THIS SUITE GUARDS, the card's merge blockers first:

* A HEADED TITLE IS ASKED PAST ITS HEAD, and past the ``[MP3]`` marker the
  naming verb writes after it, of Discogs and of the record shops' free text
  query alike, so the sitting's matches are reproduced.
* AN UNTAGGED FILE IS ASKED BY THE ARTIST AND TITLE ITS NAME READS TO, only
  when the name reads to exactly one split; a name that does not is asked
  with no artist, as before, and its record says so.
* A TITLE WITH NO HEAD IS ASKED EXACTLY AS BEFORE, byte for byte, so a
  freshly downloaded file sees no change.
* THE MATCH IS UNCHANGED. Only the question changes: a release is still taken
  only when the shared matcher reads one of its tracks as the file's own.

THE FETCH BELOW ANSWERS LIKE A CATALOGUE A PERSON TYPES INTO. It returns a
release only for the artist and title a person would type, never for a head,
so a question carrying one misses as it did at the sitting. Nothing here
touches the network, and the token is a fixture word.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

from cratekit.core import routing, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import artifacts, searchers, tag, titles
from tests._containers import synth_container
from tests.test_catalogue_searcher import _beatport_page
from tests.test_discogs_searcher import SENT, release, results
from tests.test_tag_folder_copyright import cfg, sweep  # noqa: F401
from tests.test_tag_workers import bound
from tests.test_title_matcher import DIFFERENT, HEADED, HEADED_NOT, NAMED_MIX_UNWRITTEN, SAME

TAXONOMY = default_taxonomy()

#: The releases the sitting matched, by the artist and title a person types.
#: Each is (artist, title, release number, style).
CATALOGUE = (
    ("Earth, Wind & Fire", "That's the Way of the World", 11, "Funk"),
    ("Lane 8", "Aba", 12, "Progressive House"),
    ("Kerri Chandler", "On My Way", 13, "House"),
    ("Obiman", "On The Rocks (Cafe Del Mar Mix)", 14, "Balearic"),
)


def _typed(value: str) -> str:
    return " ".join(value.lower().split())


def typed_fetch(seen: list[str] | None = None, *, beatport: str | None = None):
    """A fetch answering Discogs as a catalogue a person types into.

    The search answers a release only when its ``artist`` and ``track`` are
    one of :data:`CATALOGUE`'s, as typed, and nothing otherwise. Beatport, if
    asked, answers an empty page unless ``beatport`` is given.
    """
    by_question = {(_typed(artist), _typed(title)): number for artist, title, number, _ in CATALOGUE}
    pages = {
        f"{searchers.DISCOGS_RELEASE}{number}": release(
            number,
            artist=artist,
            title=title,
            tracks=[{"position": "A1", "type_": "track", "title": title}],
            styles=(style,),
        )
        for artist, title, number, style in CATALOGUE
    }

    def fetch(url: str) -> searchers.Fetched:
        if seen is not None:
            seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return searchers.Fetched(text=beatport or _beatport_page([]), status=200)
        if url.startswith(searchers.DISCOGS_SEARCH):
            asked = parse_qs(urlsplit(url).query, keep_blank_values=True)
            key = (_typed(asked.get("artist", [""])[0]), _typed(asked.get("track", [""])[0]))
            number = by_question.get(key)
            return searchers.Fetched(text=results(*(() if number is None else (number,))), status=200)
        if url in pages:
            return searchers.Fetched(text=pages[url], status=200)
        return searchers.Fetched(note=f"no route for {url}")

    return fetch


def build(fetch, *, token: str | None = SENT, walk=None):
    asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    extra = {} if walk is None else {"walk": walk}
    return searchers.catalogue_searcher(
        TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, **extra
    )


def discogs_questions(seen: list[str]) -> list[dict[str, str]]:
    """The artist and track of every Discogs search the fetch was sent."""
    return [
        {key: values[0] for key, values in parse_qs(urlsplit(url).query, keep_blank_values=True).items()}
        for url in seen
        if url.startswith(searchers.DISCOGS_SEARCH)
    ]


def beatport_queries(seen: list[str]) -> list[str]:
    return [url for url in seen if url.startswith(searchers.BEATPORT_SEARCH)]


def genre_of(style: str) -> str:
    written = routing.suggest_tag(TAXONOMY, style, source=searchers.DISCOGS).tag
    assert written, f"the fixture style {style!r} names a folder"
    return written


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


def tagged(tmp_path: Path, silence: Path, name: str, **fields: str) -> Path:
    target = tmp_path / name
    shutil.copy2(silence, target)
    if fields:
        assert tags.write_tags(target, dict(fields))
    return target


# ---------------------------------------------------------------------------
# A. The card's scenarios, through tag_one and the shipped searcher
# ---------------------------------------------------------------------------


def test_a_headed_title_tag_asks_discogs_past_its_head_and_takes_its_match(tmp_path, silence):
    path = tagged(
        tmp_path,
        silence,
        "03B - 83 - Earth, Wind & Fire - That's the Way of the World.flac",
        title="03B - 83 - That's the Way of the World",
        artist="Earth, Wind & Fire",
    )
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen)[0]["track"] == "That's the Way of the World"
    assert discogs_questions(seen)[0]["artist"] == "Earth, Wind & Fire"
    assert result.genre_written == genre_of("Funk")
    assert (result.source, result.source_genre) == (searchers.DISCOGS, "Funk")
    assert tags.read_genre_from_file(path) == genre_of("Funk")
    assert (result.asked_artist, result.asked_title, result.asked_read) == (
        "Earth, Wind & Fire",
        "That's the Way of the World",
        titles.Read.PAST_HEAD.value,
    )


def test_the_same_title_asked_with_its_head_misses_as_it_did_at_the_sitting():
    """The fixture answers a person's question and not the head's: the asker
    handed the title tag as its question misses, as sitting 100 measured, and
    handed the title past the head matches the same release."""
    seen: list[str] = []
    asker = searchers.discogs_asker(token=SENT, fetch=typed_fetch(seen), sleep=lambda _s: None)
    headed = "03B - 83 - That's the Way of the World"
    assert asker.ask("Earth, Wind & Fire", headed).answer is searchers.Answer.MISS
    assert discogs_questions(seen)[-1]["track"] == headed
    said = asker.ask("Earth, Wind & Fire", headed, track="That's the Way of the World")
    assert said.answer is searchers.Answer.MATCHED
    assert said.source_genre == "Funk"


def test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to(tmp_path, silence):
    path = tagged(tmp_path, silence, "9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN.flac")
    assert not tags.read_tag(path, "artist") and not tags.read_tag(path, "title")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    (question,) = discogs_questions(seen)
    assert question["artist"] == "Obiman"
    assert question["track"] == "On The Rocks (Cafe Del Mar Mix)_PN"
    assert (result.asked_artist, result.asked_title, result.asked_read) == (
        "Obiman",
        "On The Rocks (Cafe Del Mar Mix)_PN",
        titles.Read.BY_NAME.value,
    )


def test_an_untagged_file_named_artist_and_title_takes_the_release_that_names_both(tmp_path, silence):
    path = tagged(tmp_path, silence, "8A - 122 - Kerri Chandler - On My Way.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen) == [
        {"type": "release", "artist": "Kerri Chandler", "track": "On My Way", "per_page": "10"}
    ]
    assert result.genre_written == genre_of("House")


def test_an_mp3_named_untagged_file_carries_no_marker_into_the_question(tmp_path, silence):
    path = tagged(tmp_path, silence, "8A - 124 - [MP3] Lane 8 - Aba.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    (question,) = discogs_questions(seen)
    assert (question["artist"], question["track"]) == ("Lane 8", "Aba")
    assert "MP3" not in " ".join(seen)
    assert result.genre_written == genre_of("Progressive House")


def test_an_mp3_marked_title_tag_carries_no_marker_into_the_question(tmp_path, silence):
    path = tagged(tmp_path, silence, "x.flac", title="08A - 124 - [MP3] Aba", artist="Lane 8")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen)[0]["track"] == "Aba"
    assert result.genre_written == genre_of("Progressive House")


def test_a_title_of_a_head_alone_is_asked_as_written_and_the_record_says_so(tmp_path, silence):
    path = tagged(tmp_path, silence, "x.flac", title="08A - 124", artist="Lane 8")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen)[0]["track"] == "08A - 124"
    assert result.skipped == tag.NO_HIT
    assert (result.asked_title, result.asked_read) == ("08A - 124", titles.Read.HEAD_ALONE.value)


def test_a_head_and_a_marker_alone_are_never_an_empty_track_field(tmp_path, silence):
    path = tagged(tmp_path, silence, "x.flac", title="08A - 124 - [MP3]", artist="Lane 8")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen)[0]["track"] == "08A - 124 - [MP3]"
    assert result.asked_read == titles.Read.HEAD_ALONE.value


def test_a_name_that_reads_to_no_one_split_is_asked_with_no_artist_and_says_so(tmp_path, silence):
    path = tagged(tmp_path, silence, "8A - 122 - Kerri Chandler - On My Way - Live At Space.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    (question,) = discogs_questions(seen)
    assert question["artist"] == ""
    assert question["track"] == "Kerri Chandler - On My Way - Live At Space"
    assert result.genre_written is None
    assert (result.asked_artist, result.asked_read) == ("", titles.Read.NAME_AMBIGUOUS.value)


def test_a_beatport_query_for_a_headed_title_carries_no_head(tmp_path, silence):
    path = tagged(
        tmp_path, silence, "x.flac", title="03B - 83 - That's the Way of the World", artist="Earth, Wind & Fire"
    )
    seen: list[str] = []
    tag.tag_one(path, searcher=build(typed_fetch(seen), token=None))
    assert beatport_queries(seen) == [
        f"{searchers.BEATPORT_SEARCH}?q=Earth%2C+Wind+%26+Fire+That%27s+the+Way+of+the+World"
    ]


def test_the_record_shops_free_text_query_carries_no_head():
    seen: list[str] = []
    fetch = typed_fetch(seen)
    walk = (searchers.BEATPORT, searchers.TRAXSOURCE, searchers.BANDCAMP)
    build(fetch, token=None, walk=walk)("Lane 8", "08A - 124 - [MP3] Aba")
    shops = [url for url in seen if not url.startswith(searchers.DISCOGS_SEARCH)]
    assert len(shops) == 3
    for url in shops:
        assert "08A" not in url and "124" not in url and "MP3" not in url
        assert "Lane+8+Aba" in url


# ---------------------------------------------------------------------------
# B. A title with no head is asked exactly as before
# ---------------------------------------------------------------------------


#: Titles a freshly downloaded file carries, and what each was asked as
#: before this unit, written out rather than computed: the Discogs track (its
#: last bracketed group off) and Beatport's escaped query.
FRESH = [
    ("Sunrise Mood (Extended Mix)", "Sunrise Mood", "Bernard+Badie+Sunrise+Mood+%28Extended+Mix%29"),
    ("99 - Luftballons", "99 - Luftballons", "Bernard+Badie+99+-+Luftballons"),
    ("124 - Sunrise Mood", "124 - Sunrise Mood", "Bernard+Badie+124+-+Sunrise+Mood"),
    ("[Remix] Sunrise Mood", "[Remix] Sunrise Mood", "Bernard+Badie+%5BRemix%5D+Sunrise+Mood"),
    ("Bernard Badie - Sunrise Mood", "Bernard Badie - Sunrise Mood", "Bernard+Badie+Bernard+Badie+-+Sunrise+Mood"),
    ("(Intro)", "(Intro)", "Bernard+Badie+%28Intro%29"),
    ("  Sunrise Mood  ", "Sunrise Mood", "Bernard+Badie+++Sunrise+Mood"),
    ("08A", "08A", "Bernard+Badie+08A"),
]


@pytest.mark.parametrize(("title", "track", "query"), FRESH)
def test_a_title_with_no_head_is_asked_exactly_as_before(title, track, query):
    seen: list[str] = []
    build(typed_fetch(seen))("Bernard Badie", title)
    assert discogs_questions(seen)[0]["track"] == track
    assert beatport_queries(seen) == [f"{searchers.BEATPORT_SEARCH}?q={query}"]
    asked = titles.question(title, "Bernard Badie")
    assert (asked.artist, asked.title, asked.read) == ("Bernard Badie", title, titles.Read.AS_WRITTEN)


def test_a_staged_download_is_asked_and_tagged_as_before(tmp_path, silence):
    path = tagged(tmp_path, silence, "x.flac", title="On My Way (Original Mix)", artist="Kerri Chandler")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen)[0]["track"] == "On My Way"
    assert result.genre_written == genre_of("House")
    assert (result.asked_title, result.asked_read) == ("On My Way (Original Mix)", titles.Read.AS_WRITTEN.value)


def test_an_untagged_name_with_no_head_is_asked_as_before(tmp_path, silence):
    path = tagged(tmp_path, silence, "Kerri Chandler - On My Way.flac")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    assert discogs_questions(seen)[0] == {
        "type": "release",
        "artist": "",
        "track": "Kerri Chandler - On My Way",
        "per_page": "10",
    }
    assert result.genre_written is None
    assert (result.asked_artist, result.asked_read) == ("", titles.Read.AS_WRITTEN.value)


# ---------------------------------------------------------------------------
# C. Every earlier matcher case: the question changes, the verdict does not
# ---------------------------------------------------------------------------


#: The shared matcher's own corpus of file titles and rows, both ways round
#: and headed, from ``tests/test_title_matcher.py``.
CORPUS = [*SAME, *DIFFERENT, *HEADED, *HEADED_NOT]


@pytest.mark.parametrize(("searched", "found"), CORPUS)
def test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head(searched, found):
    expected = (searched, found) in SAME or (searched, found) in HEADED
    # A named mix its row does not write is no Discogs match (U318).
    expected = expected and (searched, found) not in NAMED_MIX_UNWRITTEN
    seen: list[str] = []
    tracks = [{"position": "A1", "type_": "track", "title": found}]

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.DISCOGS_SEARCH):
            return searchers.Fetched(text=results(41), status=200)
        if url == f"{searchers.DISCOGS_RELEASE}41":
            return searchers.Fetched(text=release(41, tracks=tracks), status=200)
        return searchers.Fetched(text=_beatport_page([]), status=200)

    hit = build(fetch)("Bernard Badie", searched)
    (discogs,) = [said for said in hit.answers if said.source == searchers.DISCOGS]
    assert (discogs.answer == "matched") is expected
    (question,) = discogs_questions(seen)
    assert hit.asked is not None and hit.asked.artist == "Bernard Badie"
    if hit.asked.read is titles.Read.PAST_HEAD:
        # Only the front is read off, the head and the marker after it: the
        # rest of the title is the file's own.
        assert searched.endswith(hit.asked.title) and len(hit.asked.title) < len(searched)
        assert titles.words(searched)[0] not in titles.words(question["track"])
    else:
        assert hit.asked.title == searched
    # Discogs sets a round bracketed group the title ends with aside, and asks
    # a title that is nothing but one whole, written out here rather than read
    # off the searcher.
    asked = hit.asked.title.strip()
    assert question["track"] == (re.sub(r"\s*\([^()]*\)\s*$", "", asked).strip() or asked)


def test_the_headed_cases_are_asked_past_their_head():
    asked = {searched: titles.question(searched, "Bernard Badie").title for searched, _ in HEADED}
    assert asked["04A - 126 - Burning (Extended Mix)"] == "Burning (Extended Mix)"
    assert asked["08A - 124 - [MP3] Sunrise Mood"] == "Sunrise Mood"
    assert asked["08A - 124 - Make Luv - Room 5"] == "Make Luv - Room 5"
    assert asked["08A - 124 - 1998 (Original Mix)"] == "1998 (Original Mix)"
    # Shapes the question leaves as written: no leading head with a key.
    assert asked["Bernard Badie - Sunrise Mood"] == "Bernard Badie - Sunrise Mood"
    assert asked["Sun Path - 08A - 124"] == "Sun Path - 08A - 124"
    assert asked["01 Sunrise Mood"] == "01 Sunrise Mood"


# ---------------------------------------------------------------------------
# D. The reader's two halves
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("title", "artist", "asked"),
    [
        ("03B - 83 - Kerri Chandler - On My Way", "Kerri Chandler", "On My Way"),
        ("03B - 83 - [MP3] Kerri Chandler - On My Way", "kerri chandler", "On My Way"),
        ("03B - 83 - Kerri Chandler", "Kerri Chandler", "Kerri Chandler"),
        ("03B - 83 - Kerri Chandler & Tide - On My Way", "Kerri Chandler", "Kerri Chandler & Tide - On My Way"),
        ("83 - 03B - On My Way", "Kerri Chandler", "On My Way"),
        ("03B - On My Way", "Kerri Chandler", "On My Way"),
        ("03B - 83 - On My Way", "", "On My Way"),
    ],
)
def test_the_question_reads_past_the_head_the_marker_and_the_artists_own_part(title, artist, asked):
    question = titles.question(title, artist)
    assert (question.artist, question.title, question.read) == (artist, asked, titles.Read.PAST_HEAD)


@pytest.mark.parametrize(
    ("stem", "artist", "read"),
    [
        ("8A - 122 - Kerri Chandler - On My Way", "Kerri Chandler", titles.Read.BY_NAME),
        ("8A - 122 - [MP3] Kerri Chandler - On My Way", "Kerri Chandler", titles.Read.BY_NAME),
        ("8A - 122 - Kerri Chandler - On My Way (Extended Mix)", "Kerri Chandler", titles.Read.BY_NAME),
        ("8A - 122 - Kerri Chandler - Original Mix", "", titles.Read.NAME_AMBIGUOUS),
        ("8A - 122 - Kerri Chandler - On My Way - Album", "", titles.Read.NAME_AMBIGUOUS),
        ("8A - 122 - Kerri Chandler - 01 On My Way", "", titles.Read.NAME_AMBIGUOUS),
        ("8A - 122 - 01 - On My Way", "", titles.Read.NAME_AMBIGUOUS),
        ("8A - 122 - 01 Kerri Chandler - On My Way", "", titles.Read.NAME_AMBIGUOUS),
        ("8A - 122 - On My Way", "", titles.Read.NAME_AMBIGUOUS),
        ("8A - 122", "", titles.Read.HEAD_ALONE),
        ("Kerri Chandler - On My Way", "", titles.Read.AS_WRITTEN),
        ("122 - Kerri Chandler - On My Way", "", titles.Read.AS_WRITTEN),
    ],
)
def test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title(stem, artist, read):
    split = titles.by_name(stem)
    assert (split.artist, split.read) == (artist, read)
    if read is titles.Read.BY_NAME:
        # The searcher, handed the split's artist and the name, asks the split's title.
        assert titles.question(stem, split.artist).title == split.title
        assert split.title.startswith("On My Way")


# ---------------------------------------------------------------------------
# E. The sweep's record says what was asked
# ---------------------------------------------------------------------------


def test_the_sweeps_record_names_the_question_each_file_was_asked(cfg, tmp_path, silence, monkeypatch):  # noqa: F811
    folder = tmp_path / "staging"
    folder.mkdir()
    tagged(folder, silence, "a.flac", title="03B - 83 - That's the Way of the World", artist="Earth, Wind & Fire")
    tagged(folder, silence, "8A - 122 - Kerri Chandler - On My Way - Live At Space.flac")
    tagged(folder, silence, "8A - 122 - Kerri Chandler - On My Way.flac")
    bound(monkeypatch, build(typed_fetch()))

    code, job, resumed = sweep(str(folder))

    assert code == int(ExitCode.OK), resumed
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["a.flac"]["asked"] == {
        "artist": "Earth, Wind & Fire",
        "title": "That's the Way of the World",
        "read": "past-head",
    }
    assert reports["a.flac"]["genre_written"] == genre_of("Funk")
    assert reports["8A - 122 - Kerri Chandler - On My Way - Live At Space.flac"]["asked"] == {
        "artist": "",
        "title": "Kerri Chandler - On My Way - Live At Space",
        "read": "name-ambiguous",
    }
    assert reports["8A - 122 - Kerri Chandler - On My Way.flac"]["asked"] == {
        "artist": "Kerri Chandler",
        "title": "On My Way",
        "read": "by-name",
    }
    assert reports["8A - 122 - Kerri Chandler - On My Way.flac"]["genre_written"] == genre_of("House")


# ---------------------------------------------------------------------------
# F. The guards round one found unpinned
# ---------------------------------------------------------------------------


def test_a_title_tag_with_no_artist_tag_is_never_split_by_its_name(tmp_path, silence):
    """Only a file with neither tag is asked by its name: one with a title tag
    and no artist is asked past its head with no artist, whatever its name says."""
    path = tagged(
        tmp_path, silence, "8A - 122 - Kerri Chandler - On My Way.flac", title="8A - 122 - Kerri Chandler - On My Way"
    )
    assert not tags.read_tag(path, "artist")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)))
    (question,) = discogs_questions(seen)
    assert (question["artist"], question["track"]) == ("", "Kerri Chandler - On My Way")
    assert (result.asked_artist, result.asked_read) == ("", titles.Read.PAST_HEAD.value)
    assert result.genre_written is None


@pytest.mark.parametrize("stem", ["8A - 122 - !! - On My Way", "8A - 122 - [MP3] - On My Way"])
def test_a_name_whose_artist_part_names_nobody_is_not_split(stem):
    assert titles.by_name(stem).read is titles.Read.NAME_AMBIGUOUS


@pytest.mark.parametrize("stem", ["8A - 122 - Kerri Chandler - !!", "8A - 122 - Kerri Chandler - ()"])
def test_a_name_whose_title_part_names_nothing_is_not_split(stem):
    assert titles.by_name(stem).read is titles.Read.NAME_AMBIGUOUS


def test_the_artists_part_is_read_off_only_when_a_title_follows_it():
    asked = titles.question("03B - 83 - Kerri Chandler - !!", "Kerri Chandler")
    assert (asked.title, asked.read) == ("Kerri Chandler - !!", titles.Read.PAST_HEAD)


def test_the_pictures_question_after_a_discogs_genre_carries_no_head(tmp_path, silence):
    """A file Discogs tagged that has no picture asks Beatport for its cover
    (U282), by the same question: the title past its head."""
    path = tagged(tmp_path, silence, "x.flac", title="08A - 124 - [MP3] Aba", artist="Lane 8")
    seen: list[str] = []
    result = tag.tag_one(path, searcher=build(typed_fetch(seen)), fetch_image=lambda _url: None)
    assert result.genre_written == genre_of("Progressive House")
    assert beatport_queries(seen) == [f"{searchers.BEATPORT_SEARCH}?q=Lane+8+Aba"]
