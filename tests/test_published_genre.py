"""R-796: a published genre by ISRC, from a general catalogue, after Beatport.

WHAT THIS SUITE IS GUARDING. The tagger gained a source that knows music the
record shops do not sell, and the ways that goes wrong are the ways the
searchers went wrong before it, plus two of its own:

* a catalogue that could not be read, or a file that could not be asked about,
  reported as a track nobody carries. Six answers are told apart here, and only
  one of them is allowed to mean absence;
* a refusal answered rather than recorded. A block, a rate limit and the
  catalogue's own quota error are driven below, each ends the question, and
  after the first one nothing more is asked in the run;
* an album level answer standing in for Beatport's. The general catalogue is
  asked only when Beatport answered, and never over a usable answer;
* a broad word written onto a file no folder holds. Only an answer that maps to
  a folder is written.

NOTHING HERE OPENS A SOCKET. Every answer is synthetic JSON in the shape
measured from the catalogue on 2026-10-01, handed to the injected fetch seam.

The taxonomy strings are read off ``default_taxonomy()`` wherever the taxonomy
is what is under test. The catalogue's own words are typed, in one table, because
they are a measurement of somebody else's vocabulary and not a value this
repository declares.
"""

from __future__ import annotations

import ast
import json
import shutil
import tomllib
from importlib import resources
from pathlib import Path

import pytest

from cratekit.core import routing, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import Taxonomy, build_taxonomy
from cratekit.tagging import published, searchers, tag
from cratekit.tagging.searchers import Answer, Fetched
from cratekit.tagging.tag import SearchHit, SourceAnswer
from tests._containers import synth_container
from tests.test_catalogue_searcher import (
    BUCKET_GENRE,
    DISPLAYS,
    FALLBACK_GENRE,
    REFUSED,
    SUB_GENRE,
    TAXONOMY,
    _all_three,
    _beatport_page,
    _beatport_track,
)

ISRC = "USRC17607839"
OTHER_ISRC = "GBAYE0601498"
ALBUM_ID = 302127
COVER = "https://cdn-images.dzcdn.net/images/cover/0123abcd/1000x1000-000000-80-0-0.jpg"
BEATPORT_ART = "https://geo-media.beatport.com/image_size/250x250/cover-one.jpg"

ARTIST = "Vulfpeck"
TITLE = "track"

#: A word no rule, alias or display in the template claims. Asserted below, so a
#: template that one day declares it fails here rather than quietly changing
#: what the tests around it prove.
UNDECLARED = "a genre word nothing declares"


def _tag_with_no_bucket() -> str:
    """A source string a declared rule answers with a TAG and no bucket.

    Read off the rules, because the rule is the only place that shape lives. It
    is the one answer that is neither declined nor off taxonomy and still maps
    to no folder.
    """
    for rule in TAXONOMY.suggest:
        if rule.tag and not rule.bucket and rule.all_of:
            word = " ".join(rule.all_of)
            answer = routing.suggest_tag(TAXONOMY, word)
            if answer.tag and answer.bucket_id is None and not answer.off_taxonomy:
                return word
    raise AssertionError("the template declares no rule with a tag and no bucket")


TAG_ONLY = _tag_with_no_bucket()


def _with_no_vocabulary() -> Taxonomy:
    """The shipped template as a copy written before R-799 holds it.

    No table of the general catalogue's own, so its words are resolved by the
    buckets' aliases, the way every library's active copy does until it takes
    the edit. Section B drives the chooser's own tests on that path, since a
    declared table answers before any of them is reached.
    """
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    raw = tomllib.loads(source.read_text(encoding="utf-8"))
    del raw["vocabulary"]
    return build_taxonomy(raw)


NO_TABLE = _with_no_vocabulary()


def test_the_fixture_words_are_what_the_tests_below_take_them_for():
    undeclared = routing.suggest_tag(TAXONOMY, UNDECLARED)
    assert undeclared.off_taxonomy and undeclared.bucket_id is None
    coarse = routing.suggest_tag(TAXONOMY, FALLBACK_GENRE)
    assert coarse.bucket_id is not None and TAXONOMY.is_too_coarse_as_source(coarse.tag)
    assert routing.suggest_tag(TAXONOMY, SUB_GENRE).sub_id is not None
    assert routing.suggest_tag(TAXONOMY, REFUSED[0]).declined


# ---------------------------------------------------------------------------
# Synthetic answers, in the shape measured on 2026-10-01
# ---------------------------------------------------------------------------


def deezer_track(isrc: str | None = ISRC, *, album_id: object = ALBUM_ID) -> str:
    body: dict = {"id": 3135556, "title": "Some Track", "type": "track"}
    if isrc is not None:
        body["isrc"] = isrc
    if album_id is not None:
        body["album"] = {"id": album_id, "title": "Some Album", "cover_xl": COVER}
    return json.dumps(body)


def deezer_album(genres: list[str]) -> str:
    return json.dumps(
        {
            "id": ALBUM_ID,
            "genre_id": 1,
            "genres": {
                "data": [
                    {"id": index, "name": name, "type": "genre"}
                    for index, name in enumerate(genres, start=1)
                ]
            },
        }
    )


def deezer_error(code: int, kind: str = "Exception", message: str = "") -> str:
    return json.dumps({"error": {"type": kind, "message": message, "code": code}})


UNKNOWN = deezer_error(800, "DataException", "no data")
QUOTA = deezer_error(4, "Exception", "Quota limit exceeded")
RATE_LIMITED = Fetched(note="rate limited, 3 attempts spent without an answer", status=429)


def deezer_fetch(track, album=None, seen: list[str] | None = None):
    """A fetch seam answering the two URLs the lookup asks, and nothing else.

    A request for anything else, or for an album no test supplied, fails the
    test, so "the album was never asked" is asserted by construction.
    """

    def fetch(url: str) -> Fetched:
        if seen is not None:
            seen.append(url)
        if url.startswith(published.TRACK_BY_ISRC):
            answer = track
        elif url.startswith(published.ALBUM):
            answer = album
        else:
            answer = None
        if answer is None:
            raise AssertionError(f"the lookup made a request no test expected, {url}")
        return answer if isinstance(answer, Fetched) else Fetched(text=answer, status=200)

    return fetch


def lookup_over(track, album=None, *, seen=None, naps: list[float] | None = None):
    return published.genre_lookup(
        fetch=deezer_fetch(track, album, seen),
        sleep=naps.append if naps is not None else (lambda _seconds: None),
    )


def never_asked(isrc: object) -> published.Published:
    raise AssertionError(f"the general catalogue was asked about {isrc!r}")


# ---------------------------------------------------------------------------
# A. The lookup: six answers, and what each is claimed on
# ---------------------------------------------------------------------------


def test_a_known_isrc_answers_the_albums_genres_in_the_catalogues_order():
    seen: list[str] = []
    naps: list[float] = []
    said = lookup_over(
        deezer_track(), deezer_album(["Second Word", "First Word"]), seen=seen, naps=naps
    )(ISRC)

    assert said == published.Published(
        published.SOURCE, "matched", genres=("Second Word", "First Word")
    )
    assert seen == [f"{published.TRACK_BY_ISRC}{ISRC}", f"{published.ALBUM}{ALBUM_ID}"]
    assert len(naps) == 2, "every touch is paced, the first included"
    assert all(nap >= searchers.MIN_INTERVAL_S for nap in naps)


def test_an_isrc_the_catalogue_does_not_know_is_a_miss_and_asks_for_no_album():
    seen: list[str] = []
    said = lookup_over(UNKNOWN, seen=seen)(ISRC)
    assert (said.answer, said.genres) == ("miss", ())
    assert len(seen) == 1


@pytest.mark.parametrize("given", ["", "   ", None])
def test_no_isrc_is_its_own_answer_and_nothing_is_asked(given):
    seen: list[str] = []
    said = lookup_over(deezer_track(), deezer_album(["Rock"]), seen=seen)(given)
    assert said.answer == tag.NO_ISRC
    assert said.note == "no ISRC was given"
    assert seen == []


@pytest.mark.parametrize(
    "given",
    ["CAT-0042", "USRC1760783", "../album/1", "USRC17607839X", "XUSRC17607839", "9USRC17607839"],
)
def test_a_value_that_is_not_an_isrc_never_becomes_a_request(given):
    """The tag is text somebody else wrote and the lookup turns it into a URL."""
    seen: list[str] = []
    said = lookup_over(deezer_track(), deezer_album(["Rock"]), seen=seen)(given)
    assert said.answer == tag.NO_ISRC
    assert given in said.note and "does not read as an ISRC" in said.note
    assert seen == []


def test_an_isrc_is_folded_before_it_is_asked_about():
    seen: list[str] = []
    said = lookup_over(deezer_track(), deezer_album(["Rock"]), seen=seen)("us-rc1-76-07839")
    assert said.answer == "matched"
    assert seen[0] == f"{published.TRACK_BY_ISRC}{ISRC}"


@pytest.mark.parametrize(
    "given",
    [
        f"{ISRC}\x00{OTHER_ISRC}",
        f"{ISRC}; {OTHER_ISRC}",
        f"{ISRC} / {OTHER_ISRC}",
        f"{ISRC} {OTHER_ISRC}",
        f"{ISRC}\n{OTHER_ISRC}",
        f"CAT-0042,{ISRC}",
        f"ISRC: {ISRC}",
        "isrc US-RC1-76-07839 (remaster)",
    ],
)
def test_a_field_holding_several_values_is_read_as_its_first_isrc(given):
    """Driven on 2026-10-01: an ID3 frame written with two ISRCs reads back as
    one string joined by a null, which folds to nothing as a whole."""
    seen: list[str] = []
    said = lookup_over(deezer_track(), deezer_album(["Rock"]), seen=seen)(given)
    assert said.answer == "matched"
    assert seen[0] == f"{published.TRACK_BY_ISRC}{ISRC}"


def test_the_two_value_id3_frame_is_the_shape_the_reader_really_hands_back(tmp_path):
    """The producer, driven: the string the split above is written against is
    what ``core.tags`` reads off a real ID3 container carrying two values."""
    path = synth_container(tmp_path, ".mp3")
    assert tags.write_tag_values(path, "isrc", [ISRC, OTHER_ISRC])
    held = tags.read_tag(path, "isrc")
    assert held == f"{ISRC}\x00{OTHER_ISRC}"
    seen: list[str] = []
    lookup_over(deezer_track(), deezer_album(["Rock"]), seen=seen)(held)
    assert seen[0] == f"{published.TRACK_BY_ISRC}{ISRC}"


@pytest.mark.parametrize(
    ("page", "answer", "said_in_note"),
    [
        (RATE_LIMITED, "blocked", "rate limited"),
        (Fetched(note="HTTP 403", status=403), "blocked", "HTTP 403"),
        (
            Fetched(text="<html><head><title>Just a moment...</title></head></html>", status=200),
            "blocked",
            "bot check",
        ),
        (QUOTA, "blocked", "Quota limit exceeded"),
        (deezer_error(200, "OAuthException", "needs a token"), "blocked", "OAuthException"),
        (deezer_error(700, "Exception", "Service busy"), "unreachable", "busy"),
        (Fetched(note="transport failure: down"), "unreachable", "transport failure"),
        (Fetched(note="HTTP 500", status=500), "unreachable", "HTTP 500"),
        (deezer_error(600, "InvalidQueryException", "bad"), "parse-break", "code 600"),
        ("<html>not json</html>", "unreachable", "was not JSON"),
        ("[1, 2]", "parse-break", "not the JSON object"),
        (json.dumps({"error": "a string"}), "parse-break", "does not know"),
    ],
)
def test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss(page, answer, said_in_note):
    """Each unread shape, on the first touch. None asks for the album."""
    seen: list[str] = []
    said = lookup_over(page, seen=seen)(ISRC)
    assert said.answer == answer
    assert said_in_note in said.note
    assert said.genres == ()
    assert len(seen) == 1, "a refusal ends the question, and is not asked again"


def test_a_429_is_waited_on_by_the_shared_backoff_and_then_is_blocked():
    """The 429 scenario through the real fetch. Three attempts, two waits, and
    then the answer is that the catalogue refused, with nothing tried after."""
    calls: list[dict] = []
    waits: list[float] = []

    class Limited:
        status_code = 429
        text = ""

    def get(url, **kwargs):
        calls.append({"url": url, **kwargs})
        return Limited()

    fetch = searchers.default_fetch(get=get, sleep=waits.append, headers=published.HEADERS)
    said = published.genre_lookup(fetch=fetch, sleep=lambda _seconds: None)(ISRC)

    assert said.answer == "blocked"
    assert len(calls) == searchers.RATE_LIMIT_ATTEMPTS
    assert waits == [searchers.RATE_LIMIT_BASE_WAIT_S, 2 * searchers.RATE_LIMIT_BASE_WAIT_S]
    assert {call["url"] for call in calls} == {f"{published.TRACK_BY_ISRC}{ISRC}"}


def test_the_quota_error_is_not_retried_at_all():
    calls: list[str] = []

    class Answered:
        status_code = 200
        text = QUOTA

    def get(url, **_kwargs):
        calls.append(url)
        return Answered()

    waits: list[float] = []
    fetch = searchers.default_fetch(get=get, sleep=waits.append, headers=published.HEADERS)
    said = published.genre_lookup(fetch=fetch, sleep=lambda _seconds: None)(ISRC)

    assert said.answer == "blocked"
    assert len(calls) == 1
    assert waits == []


@pytest.mark.parametrize(
    "track",
    [deezer_track(OTHER_ISRC), deezer_track(None), deezer_track("")],
)
def test_an_answer_about_another_recording_is_not_read_as_this_tracks(track):
    seen: list[str] = []
    said = lookup_over(track, deezer_album(["Rock"]), seen=seen)(ISRC)
    assert said.answer == "parse-break"
    assert ISRC in said.note
    assert len(seen) == 1


@pytest.mark.parametrize("album_id", [None, "302127", "1/../../track/9", True, 0, -4, 3.5])
def test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url(album_id):
    seen: list[str] = []
    said = lookup_over(deezer_track(album_id=album_id), deezer_album(["Rock"]), seen=seen)(ISRC)
    assert said.answer == "parse-break"
    assert "names no album" in said.note
    assert len(seen) == 1


@pytest.mark.parametrize(
    ("album", "answer"),
    [
        (RATE_LIMITED, "blocked"),
        (QUOTA, "blocked"),
        (Fetched(note="transport failure: down"), "unreachable"),
        (json.dumps({"id": ALBUM_ID}), "parse-break"),
        (json.dumps({"id": ALBUM_ID, "genres": {"data": "Rock"}}), "parse-break"),
        (json.dumps({"id": ALBUM_ID, "genres": {"data": [{"id": 1}, {"name": "  "}]}}), "parse-break"),
        ("not json", "unreachable"),
        ("[]", "parse-break"),
    ],
)
def test_a_known_track_whose_album_could_not_be_read_is_unread_and_not_a_match(album, answer):
    said = lookup_over(deezer_track(), album)(ISRC)
    assert said.answer == answer
    assert said.genres == ()


def test_an_album_with_no_genre_is_a_match_that_publishes_none():
    said = lookup_over(deezer_track(), deezer_album([]))(ISRC)
    assert (said.answer, said.genres) == ("matched", ())
    assert "publishes no genre" in said.note


def test_a_track_whose_album_the_catalogue_does_not_list_is_not_a_miss():
    said = lookup_over(deezer_track(), UNKNOWN)(ISRC)
    assert (said.answer, said.genres) == ("matched", ())
    assert "lists no album" in said.note


def test_a_refusal_is_remembered_and_nothing_more_is_asked_in_the_run():
    """The first BLOCKED answer ends the catalogue's part in the run. The next
    ISRC is answered BLOCKED without a request, and says it was not asked."""
    seen: list[str] = []
    lookup = lookup_over(QUOTA, seen=seen)

    first = lookup(ISRC)
    second = lookup(OTHER_ISRC)

    assert (first.answer, second.answer) == ("blocked", "blocked")
    assert len(seen) == 1, "the catalogue said stop and was asked nothing further"
    assert second.note.startswith("not asked: the catalogue refused this client earlier")
    assert "Quota limit exceeded" in second.note
    assert lookup("").answer == tag.NO_ISRC, "a file with no ISRC is still said to have none"


def test_a_block_on_the_album_is_remembered_too():
    seen: list[str] = []
    lookup = lookup_over(deezer_track(), RATE_LIMITED, seen=seen)
    assert lookup(ISRC).answer == "blocked"
    assert lookup(ISRC).answer == "blocked"
    assert len(seen) == 2


@pytest.mark.parametrize(
    "page",
    [
        Fetched(note="transport failure: down"),
        deezer_error(700, "Exception", "Service busy"),
        "<html>not json</html>",
        UNKNOWN,
    ],
)
def test_only_a_refusal_is_remembered(page):
    """An outage, a parse break and a miss are answers about one request, and
    the next ISRC is asked about."""
    seen: list[str] = []
    lookup = lookup_over(page, seen=seen)
    lookup(ISRC)
    lookup(OTHER_ISRC)
    assert len(seen) == 2


def test_an_album_already_read_is_not_asked_for_again():
    """A release's tracks share an album. The second track costs one request."""
    seen: list[str] = []
    answers = {
        f"{published.TRACK_BY_ISRC}{ISRC}": deezer_track(ISRC),
        f"{published.TRACK_BY_ISRC}{OTHER_ISRC}": deezer_track(OTHER_ISRC),
        f"{published.ALBUM}{ALBUM_ID}": deezer_album(["Rock"]),
    }

    def fetch(url: str) -> Fetched:
        seen.append(url)
        return Fetched(text=answers[url], status=200)

    lookup = published.genre_lookup(fetch=fetch, sleep=lambda _seconds: None)
    assert lookup(ISRC).genres == ("Rock",)
    assert lookup(OTHER_ISRC).genres == ("Rock",)
    assert seen == [
        f"{published.TRACK_BY_ISRC}{ISRC}",
        f"{published.ALBUM}{ALBUM_ID}",
        f"{published.TRACK_BY_ISRC}{OTHER_ISRC}",
    ]


def test_an_album_that_could_not_be_read_is_asked_for_again():
    seen: list[str] = []
    albums = iter(["[]", deezer_album(["Rock"])])

    def fetch(url: str) -> Fetched:
        seen.append(url)
        if url.startswith(published.TRACK_BY_ISRC):
            return Fetched(text=deezer_track(), status=200)
        return Fetched(text=next(albums), status=200)

    lookup = published.genre_lookup(fetch=fetch, sleep=lambda _seconds: None)
    assert lookup(ISRC).answer == "parse-break"
    assert lookup(ISRC).genres == ("Rock",)
    assert len(seen) == 4


def test_no_picture_is_read_off_the_general_catalogues_answer():
    """The answer carries a cover and this reader takes none. Pictures stay the
    record shops' rows."""
    said = lookup_over(deezer_track(), deezer_album(["Rock"]))(ISRC)
    assert COVER not in repr(said)


def test_the_request_names_this_tool_and_not_a_browser(monkeypatch):
    """KTD7. The lookup's own fetch, built with no seam injected, reaches the one
    HTTP getter with headers that say what is asking."""
    sent: list[dict] = []

    class Answered:
        status_code = 200
        text = UNKNOWN

    def get(url, *, headers, timeout):
        sent.append(headers)
        return Answered()

    monkeypatch.setattr(searchers, "_requests_get", get)
    said = published.genre_lookup(sleep=lambda _seconds: None)(ISRC)

    assert said.answer == "miss"
    assert sent == [published.HEADERS]
    agent = published.HEADERS["User-Agent"]
    assert agent.startswith("cratekit/") and "Mozilla" not in agent
    assert published.HEADERS != searchers.HEADERS


def test_the_record_shops_are_still_asked_with_the_headers_they_were():
    """The headers seam is new on the shared fetch, and its default is the old
    constant, so the three catalogues are asked exactly as before."""
    sent: list[dict] = []

    class Answered:
        status_code = 200
        text = "<html></html>"

    def get(url, *, headers, timeout):
        sent.append(headers)
        return Answered()

    searchers.default_fetch(get=get, sleep=lambda _s: None)("https://example.test/search")
    assert sent == [searchers.HEADERS]


def test_the_suite_cannot_reach_the_live_catalogue_through_the_shared_lookup():
    """The conftest guard. A worker test that binds only the searcher still
    hands every file to this lookup, and it fails the test before a request."""
    with pytest.raises(AssertionError, match="reached the live general catalogue"):
        published.for_lookup()(ISRC)
    assert published.for_lookup()("").answer == tag.NO_ISRC


def test_the_binders_build_without_touching_the_network(monkeypatch):
    def detonate(*args, **kwargs):
        raise AssertionError("a binder reached the network")

    monkeypatch.setattr(searchers, "_requests_get", detonate)
    monkeypatch.setattr(published, "_shared", [])
    assert callable(published.for_lookup())
    assert callable(published.for_taxonomy(TAXONOMY))


def test_the_lookup_binder_hands_back_one_lookup_per_process(monkeypatch):
    """A worker asks for its seam once per file. The refusal a lookup remembers
    is only remembered across files if every file meets the same lookup."""
    monkeypatch.setattr(published, "_shared", [])
    assert published.for_lookup() is published.for_lookup()


def test_a_refusal_on_one_file_reaches_the_next_files_seam(monkeypatch):
    """The latch, through the binders a worker uses: two seams, built one per
    file as the worker builds them, over one refused catalogue."""
    seen: list[str] = []
    shared = lookup_over(QUOTA, seen=seen)
    monkeypatch.setattr(published, "_shared", [shared])
    hit = SearchHit(answers=(SourceAnswer(searchers.BEATPORT, "miss"),))

    first = published.for_taxonomy(TAXONOMY)(hit, ISRC)
    second = published.for_taxonomy(TAXONOMY)(hit, OTHER_ISRC)

    assert [out.answers[-1].answer for out in (first, second)] == ["blocked", "blocked"]
    assert len(seen) == 1


def test_the_workers_seam_is_built_over_the_lookup_binder(monkeypatch):
    """Replacing ``for_lookup`` replaces what a worker asks, which is the only
    way a test, or the label gate's, hands a fake in."""
    asked: list[object] = []

    def fake(isrc: object) -> published.Published:
        asked.append(isrc)
        return published.Published(published.SOURCE, "miss")

    monkeypatch.setattr(published, "for_lookup", lambda: fake)
    hit = SearchHit(answers=(SourceAnswer(searchers.BEATPORT, "miss"),))
    published.for_taxonomy(TAXONOMY)(hit, ISRC)
    assert asked == [ISRC]


def test_the_module_names_no_declared_genre_display():
    """R19 over this module's own literals, as the searchers' suite holds it."""
    source = Path(published.__file__).read_text(encoding="utf-8")
    literals = {
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    assert not literals & DISPLAYS


def test_the_answer_set_is_the_searchers_and_the_two_words_of_its_own():
    assert set(published.ANSWERS) == {answer.value for answer in Answer} | {
        tag.NO_ISRC,
        searchers.NOT_ASKED,
    }
    assert set(published.UNREAD) == {"blocked", "unreachable", "parse-break"}


# ---------------------------------------------------------------------------
# B. Choosing among several genres
# ---------------------------------------------------------------------------


def test_the_first_genre_that_maps_to_a_folder_is_chosen():
    expected = routing.suggest_tag(NO_TABLE, SUB_GENRE).tag
    assert published.choose(NO_TABLE, [SUB_GENRE, BUCKET_GENRE]) == (SUB_GENRE, expected)
    assert published.choose(NO_TABLE, [BUCKET_GENRE, SUB_GENRE])[0] == BUCKET_GENRE


@pytest.mark.parametrize("passed_over", [UNDECLARED, FALLBACK_GENRE, TAG_ONLY, REFUSED[0], ""])
def test_a_word_that_maps_to_no_folder_is_passed_over_for_the_next(passed_over):
    """Each way a word fails to map: nothing declares it, it resolves to a name
    too coarse to be a tag, a rule gives it a tag with no bucket, the taxonomy
    refuses it outright, or it is empty."""
    assert published.choose(NO_TABLE, [passed_over]) is None
    chosen = published.choose(NO_TABLE, [passed_over, SUB_GENRE])
    assert chosen is not None and chosen[0] == SUB_GENRE


def _bucket_named_by_no_alias() -> str:
    """A bucket display the resolver answers with no bucket identifier.

    The template holds at least one bucket no alias names, and the resolver's
    last tier passes its display through, not off taxonomy, since routing
    files it exactly. Read off the template so the fixture moves with it.
    """
    for bucket in TAXONOMY.buckets:
        answer = routing.suggest_tag(TAXONOMY, bucket.display)
        if (
            not answer.declined
            and answer.bucket_id is None
            and not answer.off_taxonomy
            and not TAXONOMY.is_too_coarse_as_source(bucket.display)
        ):
            return bucket.display
    raise AssertionError("every bucket in the template is named by an alias of its own")


def test_a_word_that_is_a_buckets_own_name_maps_to_that_folder():
    """The review drove this: a folder exists, routing files the word in it by
    display, and asking only for a bucket identifier declined it."""
    word = _bucket_named_by_no_alias()
    assert published.choose(NO_TABLE, [word]) == (word, word)
    assert routing.resolve_bucket(NO_TABLE, word).match is routing.Match.PASSTHROUGH


def test_no_genres_chooses_nothing():
    assert published.choose(TAXONOMY, []) is None


#: The catalogue's own top level words, measured on 2026-10-01, that the shipped
#: template files, and the two it must not. Typed because they are the
#: catalogue's vocabulary. The last two of the first list are the aliases this
#: unit added.
PLACED = [
    "Rock", "R&B", "Folk", "Reggae", "Jazz", "Classical", "Pop", "Alternative",
    "Country", "Soul & Funk", "Rap/Hip Hop",
]  # fmt: skip
NOT_PLACED = ["Electro", "Dance"]


@pytest.mark.parametrize("word", PLACED)
def test_the_shipped_template_files_the_catalogues_measured_words(word):
    chosen = published.choose(TAXONOMY, [word])
    assert chosen is not None, f"{word} maps to no folder on the shipped template"
    assert routing.resolve_bucket(TAXONOMY, chosen[1]).bucket_id != TAXONOMY.fallback.bucket


@pytest.mark.parametrize("word", NOT_PLACED)
def test_the_catalogues_catch_all_words_for_dance_music_are_declined(word):
    """AE2's half of the vocabulary. The general catalogue calls most dance
    music by one of these, and neither may become a file's genre."""
    assert published.choose(TAXONOMY, [word]) is None


def test_the_aliased_word_for_a_style_resolves_to_a_sub_and_routes_into_it():
    """Reggae, since U118 gave Hip-Hop, the word this asked of first, a folder."""
    suggestion = routing.suggest_tag(TAXONOMY, "Reggae")
    assert suggestion.sub_id is not None
    landed = routing.resolve_bucket(TAXONOMY, suggestion.tag)
    assert landed.bucket_id == suggestion.bucket_id
    sub = routing.energy_sub(TAXONOMY, landed.bucket_id, None, source_genre=suggestion.tag)
    assert sub is not None and sub.id == suggestion.sub_id


@pytest.mark.parametrize(("word", "folder"), [("Soul & Funk", "Soul"), ("Rap/Hip Hop", "Hip-Hop")])
def test_the_aliased_word_for_soul_or_hip_hop_resolves_to_the_folder_u118_gave_it(word, folder):
    """Each resolved to a style sub until R-797 and U118 moved those subs to
    folders of their own, split by energy, and "Soul & Funk" to Soul by its
    first word. The word is the bucket's now, the tag written is the folder's
    name, and that name routes back into the same folder's bands."""
    suggestion = routing.suggest_tag(TAXONOMY, word)
    promoted = next(bucket for bucket in TAXONOMY.buckets if bucket.display == folder)
    assert promoted.formerly or promoted.split_from
    assert (suggestion.bucket_id, suggestion.sub_id, suggestion.tag) == (
        promoted.id, None, promoted.display
    )
    landed = routing.resolve_bucket(TAXONOMY, suggestion.tag)
    assert landed.bucket_id == promoted.id
    band = routing.energy_sub(TAXONOMY, landed.bucket_id, 5, source_genre=suggestion.tag)
    assert band is not None and band.id in {b.id for b in TAXONOMY.energy.bands}


# ---------------------------------------------------------------------------
# C. When the catalogue is asked, and what the hit becomes
# ---------------------------------------------------------------------------

MISSED = (
    SourceAnswer(searchers.BEATPORT, "miss"),
    SourceAnswer(searchers.TRAXSOURCE, "blocked", note="HTTP 403"),
    SourceAnswer(searchers.BANDCAMP, "blocked"),
)
MISSED_HIT = SearchHit(answers=MISSED, unread=(searchers.TRAXSOURCE, searchers.BANDCAMP))


def said(answer: str, *genres: str, note: str = "") -> published.Lookup:
    def lookup(_isrc: object) -> published.Published:
        return published.Published(published.SOURCE, answer, genres=tuple(genres), note=note)

    return lookup


def opinion(lookup: published.Lookup):
    return published.second_opinion(TAXONOMY, lookup=lookup)


def test_a_hit_with_no_answers_is_returned_untouched_and_nothing_is_asked():
    hit = SearchHit(genre=None, source="", source_genre="")
    assert opinion(never_asked)(hit, ISRC) is hit


def test_a_usable_answer_is_never_replaced_and_the_record_says_not_asked():
    """R4. Whatever the general catalogue would say, it is not asked."""
    hit = SearchHit(
        genre=BUCKET_GENRE,
        source=searchers.BEATPORT,
        source_genre=BUCKET_GENRE,
        answers=(SourceAnswer(searchers.BEATPORT, "matched", source_genre=BUCKET_GENRE),),
    )
    out = opinion(never_asked)(hit, ISRC)
    assert (out.genre, out.source) == (BUCKET_GENRE, searchers.BEATPORT)
    assert out.answers[-1] == SourceAnswer(published.SOURCE, searchers.NOT_ASKED)
    assert out.answers[:-1] == hit.answers


def test_a_file_that_needs_no_genre_is_not_asked_about():
    out = opinion(never_asked)(MISSED_HIT, None)
    assert out.answers[-1] == SourceAnswer(published.SOURCE, searchers.NOT_ASKED)
    assert out.unread == MISSED_HIT.unread


@pytest.mark.parametrize("beatport", ["unreachable", "parse-break", "blocked", searchers.NOT_ASKED])
def test_beatport_must_have_answered_before_the_general_catalogue_is_asked(beatport):
    """KTD4. A fallback's MISS made this a decline, and Beatport itself was not
    read, so an album level answer written now would stand in for Beatport's."""
    hit = SearchHit(
        answers=(
            SourceAnswer(searchers.BEATPORT, beatport),
            SourceAnswer(searchers.TRAXSOURCE, "miss"),
            SourceAnswer(searchers.BANDCAMP, "miss"),
        ),
        unread=(searchers.BEATPORT,),
    )
    out = opinion(never_asked)(hit, ISRC)
    last = out.answers[-1]
    assert (last.source, last.answer) == (published.SOURCE, searchers.NOT_ASKED)
    assert searchers.BEATPORT in last.note
    assert out.genre is None and out.unread == (searchers.BEATPORT,)


@pytest.mark.parametrize("given", ["", "CAT-0042"])
def test_a_file_with_no_isrc_is_said_to_have_none_whatever_beatport_answered(given):
    """KTD8. Beatport was not read, so nothing would be asked anyway, and the
    file still counts as one with no ISRC, since another run will not change
    that. Before, it was recorded ``not-asked`` and the warning undercounted."""
    hit = SearchHit(
        answers=(
            SourceAnswer(searchers.BEATPORT, "unreachable"),
            SourceAnswer(searchers.TRAXSOURCE, "miss"),
        ),
        unread=(searchers.BEATPORT,),
    )
    out = opinion(never_asked)(hit, given)
    assert out.answers[-1].answer == tag.NO_ISRC
    assert out.unread == (searchers.BEATPORT,)


def test_a_file_with_no_isrc_whose_genre_a_shop_settled_is_still_not_asked():
    hit = SearchHit(
        genre=BUCKET_GENRE,
        source=searchers.BEATPORT,
        answers=(SourceAnswer(searchers.BEATPORT, "matched", source_genre=BUCKET_GENRE),),
    )
    out = opinion(never_asked)(hit, "")
    assert out.answers[-1].answer == searchers.NOT_ASKED


def test_a_hit_that_names_no_beatport_answer_is_not_asked_about():
    hit = SearchHit(answers=(SourceAnswer(searchers.TRAXSOURCE, "miss"),))
    out = opinion(never_asked)(hit, ISRC)
    assert out.answers[-1].answer == searchers.NOT_ASKED


def test_a_published_genre_that_maps_becomes_the_hits_genre_with_no_inferred_mark():
    expected = routing.suggest_tag(TAXONOMY, SUB_GENRE).tag
    out = opinion(said("matched", SUB_GENRE))(MISSED_HIT, ISRC)
    assert (out.genre, out.source, out.source_genre) == (expected, published.SOURCE, SUB_GENRE)
    assert out.off_taxonomy is False
    assert out.answers == (*MISSED, SourceAnswer(published.SOURCE, "matched", SUB_GENRE))
    assert out.unread == MISSED_HIT.unread
    assert (out.art_url, out.art_source) == ("", ""), "no shop's row matched"


def test_several_genres_use_the_first_that_maps_and_the_record_lists_them_all():
    out = opinion(said("matched", UNDECLARED, FALLBACK_GENRE, SUB_GENRE, BUCKET_GENRE))(
        MISSED_HIT, ISRC
    )
    assert out.source_genre == SUB_GENRE
    assert out.genre == routing.suggest_tag(TAXONOMY, SUB_GENRE).tag
    last = out.answers[-1]
    assert last.source_genre == SUB_GENRE
    assert last.note == (
        f"the album lists {UNDECLARED}, {FALLBACK_GENRE}, {SUB_GENRE}, {BUCKET_GENRE}"
    )


@pytest.mark.parametrize("word", [UNDECLARED, FALLBACK_GENRE, TAG_ONLY])
def test_an_answer_that_maps_to_no_folder_is_declined_and_says_what_was_answered(word):
    """R3. The hit stays a decline, and the word is on it for the record."""
    out = opinion(said("matched", word))(MISSED_HIT, ISRC)
    assert out.genre is None
    assert (out.source, out.source_genre) == (published.SOURCE, word)
    assert out.answers[-1] == SourceAnswer(published.SOURCE, "matched", word)


def test_a_declined_answer_beside_beatports_own_declined_word_keeps_beatports():
    """AE2 at the seam. Both answers are in the record, and the file's own
    source genre stays the record shop's."""
    hit = SearchHit(
        genre=None,
        source=searchers.BEATPORT,
        source_genre=REFUSED[0],
        art_url=BEATPORT_ART,
        answers=(SourceAnswer(searchers.BEATPORT, "matched", source_genre=REFUSED[0]),),
    )
    out = opinion(said("matched", FALLBACK_GENRE))(hit, ISRC)
    assert out.genre is None
    assert (out.source, out.source_genre) == (searchers.BEATPORT, REFUSED[0])
    assert [(one.source, one.source_genre) for one in out.answers] == [
        (searchers.BEATPORT, REFUSED[0]),
        (published.SOURCE, FALLBACK_GENRE),
    ]
    assert (out.art_url, out.art_source) == (BEATPORT_ART, None)


def test_a_published_genre_over_beatports_declined_word_is_written_and_keeps_beatports_picture():
    """Beatport answered with a catch-all, which is not a usable answer, so the
    general catalogue is asked and its answer is written. The picture Beatport's
    row named stays, and says it is Beatport's."""
    hit = SearchHit(
        genre=None,
        source=searchers.BEATPORT,
        source_genre=REFUSED[0],
        art_url=BEATPORT_ART,
        answers=(SourceAnswer(searchers.BEATPORT, "matched", source_genre=REFUSED[0]),),
    )
    out = opinion(said("matched", SUB_GENRE))(hit, ISRC)
    assert (out.source, out.source_genre) == (published.SOURCE, SUB_GENRE)
    assert out.genre == routing.suggest_tag(TAXONOMY, SUB_GENRE).tag
    assert (out.art_url, out.art_source) == (BEATPORT_ART, searchers.BEATPORT)


def test_a_match_that_publishes_no_genre_is_a_decline_with_no_word():
    note = "the catalogue knows the track and publishes no genre for its album"
    out = opinion(said("matched", note=note))(MISSED_HIT, ISRC)
    assert out.genre is None
    assert (out.source, out.source_genre, out.art_source) == ("", "", None), (
        "a catalogue that supplied no word is not the file's source"
    )
    assert out.answers[-1] == SourceAnswer(published.SOURCE, "matched", note=note)


@pytest.mark.parametrize("answer", published.UNREAD)
def test_an_unread_general_catalogue_joins_the_unread_names(answer):
    out = opinion(said(answer, note="why"))(MISSED_HIT, ISRC)
    assert out.genre is None
    assert out.unread == (*MISSED_HIT.unread, published.SOURCE)
    assert out.answers[-1] == SourceAnswer(published.SOURCE, answer, note="why")


@pytest.mark.parametrize("answer", ["miss", tag.NO_ISRC])
def test_a_miss_and_a_missing_isrc_are_recorded_and_are_not_unread(answer):
    out = opinion(said(answer, note="why"))(MISSED_HIT, ISRC)
    assert out.unread == MISSED_HIT.unread
    assert out.answers[-1] == SourceAnswer(published.SOURCE, answer, note="why")
    assert (out.source, out.source_genre) == ("", "")


# ---------------------------------------------------------------------------
# D. Through the engine, on a real file, with the shipped searcher
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def track(tmp_path, silence) -> Path:
    """One real FLAC carrying an artist, a title and an ISRC, and no genre."""
    path = tmp_path / f"{TITLE}.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE, "isrc": ISRC})
    return path


EMPTY_BEATPORT = _beatport_page([])
TRAXSOURCE_403 = Fetched(note="HTTP 403", status=403)
BANDCAMP_CHALLENGE = Fetched(
    text="<html><head><title>Client Challenge</title></head></html>", status=200
)


def shops(beatport: str = EMPTY_BEATPORT, *, traxsource=TRAXSOURCE_403, bandcamp=BANDCAMP_CHALLENGE):
    """The shipped searcher, in the state measured on the author's machine:
    Beatport answering and both fallbacks refusing."""
    return searchers.catalogue_searcher(
        TAXONOMY,
        fetch=_all_three(beatport=beatport, traxsource=traxsource, bandcamp=bandcamp),
        sleep=lambda _seconds: None,
    )


def test_ae1_a_track_beatport_does_not_carry_gets_the_published_genre(track):
    """AE1. Beatport misses, the general catalogue calls the album by a word the
    taxonomy has a folder for, and that is written. Routing then files the
    written tag in the sub the taxonomy declared for the word."""
    word = "Rock"
    suggestion = routing.suggest_tag(TAXONOMY, word)
    # THE FOLDER IS PINNED BY IDENTIFIER, not only by asking the resolver the
    # code under test asks: AE1 names NonElectronic / Rock, and the tag written
    # is that sub's own display, read off the template.
    assert (suggestion.bucket_id, suggestion.sub_id) == ("non_electronic", "rock")
    (rock,) = [sub for sub in TAXONOMY.bucket("non_electronic").subs if sub.id == "rock"]
    assert suggestion.tag == rock.display

    result = tag.tag_one(
        track,
        searcher=shops(),
        published=opinion(lookup_over(deezer_track(), deezer_album([word]))),
    )

    assert result.skipped is None
    assert result.genre_written == suggestion.tag
    assert tags.read_genre_from_file(track) == suggestion.tag
    assert (result.source, result.source_genre) == (published.SOURCE, word)
    assert result.off_taxonomy is False
    assert [(one.source, one.answer) for one in result.answers] == [
        (searchers.BEATPORT, "miss"),
        (searchers.TRAXSOURCE, "blocked"),
        (searchers.BANDCAMP, "blocked"),
        (published.SOURCE, "matched"),
    ]
    landed = routing.resolve_bucket(TAXONOMY, result.genre_written)
    assert landed.bucket_id == suggestion.bucket_id
    sub = routing.energy_sub(TAXONOMY, landed.bucket_id, None, source_genre=result.genre_written)
    assert sub is not None and sub.id == suggestion.sub_id


def test_ae2_two_coarse_answers_write_nothing_and_the_record_shows_both(track):
    """AE2. Beatport's catch-all and the general catalogue's, in the words each
    was measured to use."""
    beatport = _beatport_page([_beatport_track(ARTIST, TITLE, "Electronica")])

    result = tag.tag_one(
        track,
        searcher=shops(beatport),
        published=opinion(lookup_over(deezer_track(), deezer_album(["Electro"]))),
    )

    assert result.genre_written is None
    assert tags.read_genre_from_file(track) is None
    assert result.skipped == tag.UNMAPPED_GENRE
    assert [(one.source, one.answer, one.source_genre) for one in result.answers] == [
        (searchers.BEATPORT, "matched", "Electronica"),
        (searchers.TRAXSOURCE, searchers.NOT_ASKED, ""),
        (searchers.BANDCAMP, searchers.NOT_ASKED, ""),
        (published.SOURCE, "matched", "Electro"),
    ]


def test_ae3_a_usable_beatport_answer_is_written_and_the_general_catalogue_is_not_asked(track):
    beatport = _beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)])

    result = tag.tag_one(track, searcher=shops(beatport), published=opinion(never_asked))

    assert result.genre_written == BUCKET_GENRE
    assert result.source == searchers.BEATPORT
    assert result.answers[-1] == SourceAnswer(published.SOURCE, searchers.NOT_ASKED)


def test_ae4_a_file_with_no_isrc_is_reported_as_that_and_not_as_no_hit(tmp_path, silence):
    """AE4, with every record shop answering MISS, which before this unit was a
    clean ``no-hit``. The general catalogue could not be asked, so whether any
    catalogue carries the track is unknown."""
    path = tmp_path / f"{TITLE}.flac"
    shutil.copy2(silence, path)
    seen: list[str] = []

    result = tag.tag_one(
        path,
        searcher=shops(traxsource="<html></html>", bandcamp="<html><ul></ul></html>"),
        published=opinion(lookup_over(deezer_track(), deezer_album(["Rock"]), seen=seen)),
    )

    assert result.skipped == tag.NO_ISRC
    assert result.skipped != tag.NO_HIT
    assert result.answers[-1] == SourceAnswer(published.SOURCE, tag.NO_ISRC, note="no ISRC was given")
    assert result.unread == ()
    assert seen == [], "a file with no ISRC is never asked about"


def test_a_file_with_no_isrc_beside_blocked_fallbacks_keeps_the_unread_reason(tmp_path, silence):
    """``sources-unread`` keeps its R-791 meaning and wins. The answer still
    says the file has no ISRC, which is what the verb's warning counts."""
    path = tmp_path / f"{TITLE}.flac"
    shutil.copy2(silence, path)

    result = tag.tag_one(path, searcher=shops(), published=opinion(lookup_over(UNKNOWN)))

    assert result.skipped == tag.SOURCES_UNREAD
    assert result.answers[-1].answer == tag.NO_ISRC


def test_a_malformed_isrc_tag_is_reported_with_what_it_held(tmp_path, silence):
    path = tmp_path / f"{TITLE}.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(path, {"isrc": "CAT-0042"})

    result = tag.tag_one(
        path,
        searcher=shops(traxsource="<html></html>", bandcamp="<html><ul></ul></html>"),
        published=opinion(lookup_over(deezer_track(), deezer_album(["Rock"]))),
    )

    assert result.skipped == tag.NO_ISRC
    assert "CAT-0042" in result.answers[-1].note


def test_a_track_no_catalogue_knows_with_every_source_read_is_still_no_hit(track):
    """Four misses is the absence ``no-hit`` means, and stays it."""
    result = tag.tag_one(
        track,
        searcher=shops(traxsource="<html></html>", bandcamp="<html><ul></ul></html>"),
        published=opinion(lookup_over(UNKNOWN)),
    )
    assert result.skipped == tag.NO_HIT
    assert [one.answer for one in result.answers] == ["miss"] * 4
    assert result.unread == ()


def test_a_blocked_general_catalogue_leaves_the_file_untagged_and_askable(track):
    result = tag.tag_one(
        track,
        searcher=shops(traxsource="<html></html>", bandcamp="<html><ul></ul></html>"),
        published=opinion(lookup_over(RATE_LIMITED)),
    )
    assert result.skipped == tag.SOURCES_UNREAD
    assert result.unread == (published.SOURCE,)
    assert tags.read_genre_from_file(track) is None


def test_a_file_that_already_has_a_genre_is_not_asked_about(track):
    """Fill if empty. The file is searched for its picture, and the general
    catalogue is never asked for a genre the file does not need."""
    assert tags.write_genre(track, BUCKET_GENRE)

    result = tag.tag_one(track, searcher=shops(), published=opinion(never_asked))

    assert result.skipped == tag.HAS_GENRE
    assert tags.read_genre_from_file(track) == BUCKET_GENRE
    assert result.answers[-1] == SourceAnswer(published.SOURCE, searchers.NOT_ASKED)


def test_a_searcher_that_refuses_is_not_offered_to_the_general_catalogue(track):
    """No record shop was read, so the refusal propagates as it did, and the
    general catalogue's answer does not stand in for a Beatport nobody asked."""

    def refusing(artist: str, title: str):
        raise refuse(
            searchers.UNREACHABLE_REASON,
            "no catalogue could be read",
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            origin=("tagging", "searchers"),
        )

    with pytest.raises(CratekitError):
        tag.tag_one(track, searcher=refusing, published=opinion(never_asked))
    assert tags.read_genre_from_file(track) is None


def test_the_shipped_searcher_refusing_reaches_the_same_end(track):
    """The producer driven: Beatport unreachable and both fallbacks blocked is
    the shipped searcher's own refusal, with nothing asked after it."""
    searcher = shops(Fetched(note="transport failure: down"))
    with pytest.raises(CratekitError) as raised:
        tag.tag_one(track, searcher=searcher, published=opinion(never_asked))
    assert raised.value.cause.reason == searchers.UNREACHABLE_REASON


def test_a_published_genre_brings_no_picture_and_the_image_fetch_is_not_called(track):
    """The file has no picture and no record shop named one. The general
    catalogue supplies the genre and nothing is fetched for a cover."""

    def fetch_image(url: str) -> bytes:
        raise AssertionError(f"a picture was fetched, {url}")

    result = tag.tag_one(
        track,
        searcher=shops(),
        fetch_image=fetch_image,
        published=opinion(lookup_over(deezer_track(), deezer_album(["Rock"]))),
    )

    assert result.genre_written is not None
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert result.art_fetch_detail == (
        "traxsource, bandcamp could not be read and no other catalogue that is "
        "asked for pictures carried the track, so no picture was named; deezer "
        "answered about the genre and is not asked for one"
    )


def test_a_declined_published_word_does_not_put_the_picture_question_to_the_catalogue(track):
    result = tag.tag_one(
        track,
        searcher=shops(traxsource="<html></html>", bandcamp="<html><ul></ul></html>"),
        published=opinion(lookup_over(deezer_track(), deezer_album([UNDECLARED]))),
    )
    assert result.skipped == tag.UNMAPPED_GENRE
    assert result.art_fetch_detail == (
        "no catalogue that is asked for pictures carried the track, so no picture "
        "was named; deezer answered about the genre and is not asked for one"
    )


def test_a_match_with_no_genre_leaves_the_file_as_the_shops_left_it(track):
    """Every record shop missed and the general catalogue knows the track with
    no genre published. The record carries the match, and nothing else about
    the file names a catalogue that supplied nothing."""
    result = tag.tag_one(
        track,
        searcher=shops(traxsource="<html></html>", bandcamp="<html><ul></ul></html>"),
        published=opinion(lookup_over(deezer_track(), deezer_album([]))),
    )
    assert result.skipped == tag.NO_HIT
    assert (result.source, result.source_genre) == ("", "")
    assert result.answers[-1].answer == "matched"
    assert result.art_fetch_detail == "no catalogue carried the track, so no picture was named"


def test_beatports_picture_is_embedded_under_a_published_genre_and_says_whose_it_is(track):
    """Beatport matched with a catch-all and named a cover. The general
    catalogue supplies the genre, and the picture is still Beatport's row's."""
    import io

    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (900, 900), (10, 120, 200)).save(buffer, format="JPEG")
    fetched: list[str] = []

    def fetch_image(url: str) -> bytes:
        fetched.append(url)
        return buffer.getvalue()

    row = {
        **_beatport_track(ARTIST, TITLE, "Electronica"),
        "release": {"release_image_uri": BEATPORT_ART},
    }
    result = tag.tag_one(
        track,
        searcher=shops(_beatport_page([row])),
        fetch_image=fetch_image,
        published=opinion(lookup_over(deezer_track(), deezer_album(["Rock"]))),
    )

    assert result.source == published.SOURCE
    assert len(fetched) == 1 and "beatport" in fetched[0]
    assert result.art_fetch == tag.ART_EMBEDDED
    assert result.art_fetch_detail.endswith(f"from {searchers.BEATPORT}")


def test_a_picture_from_beatports_row_is_reported_as_beatports(tmp_path, silence):
    """The hit's source became the general catalogue and the picture did not."""
    path = tmp_path / f"{TITLE}.flac"
    shutil.copy2(silence, path)
    hit = SearchHit(
        genre="anything",
        source=published.SOURCE,
        art_url=BEATPORT_ART,
        art_source=searchers.BEATPORT,
    )

    def searcher(artist: str, title: str) -> SearchHit:
        return hit

    result = tag.tag_one(path, searcher=searcher, fetch_image=lambda _url: None)
    assert result.art_fetch == tag.ART_UNAVAILABLE

    bare = SearchHit(genre=None, source=published.SOURCE, art_source=searchers.BEATPORT)
    result = tag.tag_one(path, searcher=lambda _a, _t: bare)
    assert result.art_fetch_detail == f"{searchers.BEATPORT} named no picture for the track"


def test_the_folder_pass_hands_the_seam_to_every_file(tmp_path, silence):
    for name in ("a", "b"):
        shutil.copy2(silence, tmp_path / f"{name}.flac")
    offered: list[str | None] = []

    def seam(hit: SearchHit, isrc: str | None) -> SearchHit:
        offered.append(isrc)
        return hit

    def searcher(artist: str, title: str) -> SearchHit:
        return SearchHit(answers=(SourceAnswer(searchers.BEATPORT, "miss"),))

    tag.tag_folder(tmp_path, searcher=searcher, published=seam)
    assert offered == ["", ""]


def test_the_isrc_tag_is_not_read_for_a_file_a_record_shop_settled(track, monkeypatch):
    """The seam is told None and the container is not opened for a field
    nothing will use, which on a folder Beatport mostly answers is most files."""
    read: list[str] = []
    real = tags.read_tag

    def recording(path, field):
        read.append(field)
        return real(path, field)

    monkeypatch.setattr(tags, "read_tag", recording)
    offered: list[str | None] = []

    def seam(hit: SearchHit, isrc: str | None) -> SearchHit:
        offered.append(isrc)
        return hit

    settled = SearchHit(genre=BUCKET_GENRE, source=searchers.BEATPORT)
    tag.tag_one(track, searcher=lambda _a, _t: settled, published=seam)

    assert offered == [None]
    assert "isrc" not in read


def test_a_searcher_that_returns_nothing_is_not_offered(tmp_path, silence):
    path = tmp_path / f"{TITLE}.flac"
    shutil.copy2(silence, path)

    def seam(hit: SearchHit, isrc: str | None) -> SearchHit:
        raise AssertionError("None was offered to the general catalogue")

    result = tag.tag_one(path, searcher=lambda _a, _t: None, published=seam)
    assert result.skipped == tag.NO_HIT
