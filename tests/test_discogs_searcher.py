"""U244: a track Beatport misses gets its genre from the Discogs API, with a person's own token.

WHAT THIS SUITE GUARDS, in the order a wrong answer would cost a library:

* ABSENCE IS NEVER READ AS AN ANSWER. No token, a rejected token, a refusal, an
  outage and a reshaped answer each say something other than MISS, so a folder
  swept without Discogs is never recorded as tracks no catalogue carries.
* A WRONG RELEASE IS WORSE THAN A MISS. A release is taken only when one of its
  tracks, or its own title for a single, and an artist match the file.
* THE TOKEN GOES IN ONE PLACE. The Authorization header, and nowhere a person or
  a log can read it: no URL, note, record, log line or refusal.
* THE GENRE IS THE RESOLVER'S. A style becomes a tag only through
  ``routing.suggest_tag``, and only when it names a folder that is not the
  fallback's.

NOTHING HERE TOUCHES THE NETWORK OR A REAL TOKEN. Every answer is recorded JSON
handed to the fetch seam, or to the shipped fetch through an injected getter,
and the token is a fixture word.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from types import MappingProxyType

import pytest

from cratekit import __version__
from cratekit.core import routing, secrets, tags
from cratekit.core.cause import CratekitError, Scope
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import cli as tag_cli
from cratekit.tagging import published, searchers, tag
from tests._containers import synth_container
from tests.test_catalogue_searcher import (
    ARTIST,
    BUCKET_GENRE,
    FALLBACK_GENRE,
    TITLE,
    _beatport_page,
    _beatport_track,
)

TAXONOMY = default_taxonomy()


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


#: A fixture word standing in for a personal token. Never a real one.
SENT = "fixture0discogs0value"

#: The styles the brief requires the default template to file in a folder.
BRIEF_STYLES = (
    "Nu-Disco",
    "Disco",
    "Deep House",
    "House",
    "Tech House",
    "Afro House",
    "Italo-Disco",
    "Boogie",
    "Funk",
    "Electro",
    "Balearic",
    "Downtempo",
    "Leftfield",
    "Acid House",
    "Minimal",
    "Techno",
    "Progressive House",
    "Garage House",
    "UK Garage",
    "Soulful House",
)


# ---------------------------------------------------------------------------
# Recorded answers, in the shapes Discogs' database search and release read serve
# ---------------------------------------------------------------------------


def results(*numbers: int, kind: str = "release") -> str:
    return json.dumps(
        {
            "pagination": {"page": 1, "pages": 1, "items": len(numbers)},
            "results": [
                {"id": number, "type": kind, "title": f"{ARTIST} - {TITLE}"}
                for number in numbers
            ],
        }
    )


def release(
    number: int,
    *,
    artist: str = ARTIST,
    title: str = "An EP",
    tracks: list[dict] | None = None,
    styles: tuple[str, ...] = ("Nu-Disco",),
    genres: tuple[str, ...] = ("Electronic",),
) -> str:
    return json.dumps(
        {
            "id": number,
            "title": title,
            "artists": [{"name": artist}],
            "tracklist": (
                tracks
                if tracks is not None
                else [
                    {"position": "A1", "type_": "track", "title": "Opener"},
                    {"position": "A2", "type_": "track", "title": TITLE},
                ]
            ),
            "styles": list(styles),
            "genres": list(genres),
        }
    )


EMPTY_BEATPORT = searchers.Fetched(text=_beatport_page([]), status=200)


def routed(
    *,
    search: searchers.Fetched | str,
    releases: dict[int, searchers.Fetched | str] | None = None,
    beatport: searchers.Fetched | str = EMPTY_BEATPORT,
    seen: list[str] | None = None,
):
    """A fetch answering Beatport and Discogs by URL, a release by its exact URL."""
    by_release = {f"{searchers.DISCOGS_RELEASE}{n}": page for n, page in (releases or {}).items()}

    def fetch(url: str) -> searchers.Fetched:
        if seen is not None:
            seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            answer = beatport
        elif url.startswith(searchers.DISCOGS_SEARCH):
            answer = search
        elif url in by_release:
            answer = by_release[url]
        else:
            return searchers.Fetched(note=f"no route for {url}")
        if isinstance(answer, searchers.Fetched):
            return answer
        return searchers.Fetched(text=answer, status=200)

    return fetch


def asker(fetch, *, token: str | None = SENT, naps: list[float] | None = None):
    return searchers.discogs_asker(
        token=token,
        fetch=fetch,
        sleep=(naps.append if naps is not None else lambda _s: None),
    )


def searcher(fetch, *, token: str | None = SENT, naps: list[float] | None = None, discogs=None):
    sleep = naps.append if naps is not None else (lambda _s: None)
    return searchers.catalogue_searcher(
        TAXONOMY,
        fetch=fetch,
        sleep=sleep,
        discogs=discogs if discogs is not None else asker(fetch, token=token, naps=naps),
    )


def said(hit) -> list[tuple[str, str]]:
    return [(one.source, one.answer) for one in hit.answers]


def discogs_answer(hit):
    (one,) = [entry for entry in hit.answers if entry.source == searchers.DISCOGS]
    return one


# ---------------------------------------------------------------------------
# A. The walk: Beatport first, Discogs when it does not match
# ---------------------------------------------------------------------------


def test_the_default_walk_is_beatport_then_discogs_and_names_no_scraped_shop():
    assert searchers.WALK == (searchers.BEATPORT, searchers.DISCOGS)
    assert searchers.TRAXSOURCE not in searchers.WALK
    assert searchers.BANDCAMP not in searchers.WALK
    # Every source a record can name stays countable, the old three included.
    assert set(searchers.SCRAPED_WALK) | set(searchers.WALK) == set(searchers.SOURCES)


def test_the_scraped_shops_are_never_asked_by_the_default_walk():
    seen: list[str] = []
    fetch = routed(search=results(), seen=seen)
    searcher(fetch)(ARTIST, TITLE)
    assert not any(
        url.startswith((searchers.TRAXSOURCE_SEARCH, searchers.BANDCAMP_SEARCH)) for url in seen
    )
    assert [url.split("?")[0] for url in seen] == [
        searchers.BEATPORT_SEARCH,
        searchers.DISCOGS_SEARCH,
    ]


def test_a_beatport_match_never_asks_discogs():
    seen: list[str] = []
    beatport = _beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)])
    hit = searcher(routed(search=results(1), beatport=beatport, seen=seen))(ARTIST, TITLE)
    assert hit.source == searchers.BEATPORT
    assert said(hit) == [(searchers.BEATPORT, "matched"), (searchers.DISCOGS, searchers.NOT_ASKED)]
    assert not any(url.startswith(searchers.DISCOGS_API) for url in seen)


def test_a_matched_release_whose_first_style_resolves_is_written():
    fetch = routed(search=results(7), releases={7: release(7, styles=("Nu-Disco", "Disco"))})
    hit = searcher(fetch)(ARTIST, TITLE)

    expected = routing.suggest_tag(TAXONOMY, "Nu-Disco", source=searchers.DISCOGS).tag
    assert expected and TAXONOMY.named_folder(expected) is not None
    assert hit.genre == expected
    assert (hit.source, hit.source_genre) == (searchers.DISCOGS, "Nu-Disco")
    assert hit.off_taxonomy is False
    assert said(hit) == [(searchers.BEATPORT, "miss"), (searchers.DISCOGS, "matched")]
    note = discogs_answer(hit).note
    assert "release 7" in note and "Nu-Disco, Disco" in note and "Electronic" in note
    assert hit.unread == ()


def test_a_first_style_that_resolves_only_to_the_fallback_gives_way_to_the_second():
    suggestion = routing.suggest_tag(TAXONOMY, FALLBACK_GENRE, source=searchers.DISCOGS)
    assert suggestion.bucket_id == TAXONOMY.fallback.bucket, "the fixture word lands on the fallback"
    fetch = routed(
        search=results(3), releases={3: release(3, styles=(FALLBACK_GENRE, "Deep House"))}
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert hit.source_genre == "Deep House"
    assert hit.genre == routing.suggest_tag(TAXONOMY, "Deep House", source=searchers.DISCOGS).tag
    assert FALLBACK_GENRE in discogs_answer(hit).note, "every style read rides the record"


def test_no_style_that_names_a_folder_is_a_decline_naming_the_first_style():
    words = ("Hauntological Hymnals", FALLBACK_GENRE)
    for word in words:
        assert searchers.choose_word(TAXONOMY, [word], source=searchers.DISCOGS, named_only=True) is None
    fetch = routed(search=results(4), releases={4: release(4, styles=words)})
    hit = searcher(fetch)(ARTIST, TITLE)
    assert hit.genre is None
    assert (hit.source, hit.source_genre) == (searchers.DISCOGS, words[0])
    assert hit.off_taxonomy is False, "a pass through word is never written for Discogs"


def test_a_matched_release_with_no_style_declines_with_nothing_to_map():
    fetch = routed(search=results(5), releases={5: release(5, styles=())})
    hit = searcher(fetch)(ARTIST, TITLE)
    assert hit.genre is None and hit.source == searchers.DISCOGS and hit.source_genre == ""
    assert "styles none" in discogs_answer(hit).note


def test_an_empty_result_set_is_a_miss_and_two_misses_are_no_hit():
    hit = searcher(routed(search=results()))(ARTIST, TITLE)
    assert said(hit) == [(searchers.BEATPORT, "miss"), (searchers.DISCOGS, "miss")]
    assert hit.genre is None and hit.source == "" and hit.unread == ()


def test_a_release_whose_artist_matches_and_title_does_not_is_no_match():
    other = [{"position": "A1", "type_": "track", "title": "Completely Different Song"}]
    fetch = routed(
        search=results(9), releases={9: release(9, title="Another Record", tracks=other)}
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "miss"
    assert hit.genre is None


def test_a_release_whose_title_matches_and_artist_does_not_is_no_match():
    fetch = routed(search=results(9), releases={9: release(9, artist="Somebody Else Entirely")})
    hit = searcher(fetch)(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "miss"


def test_a_compilation_matches_on_the_tracks_own_credit():
    tracks = [
        {"position": "1", "type_": "track", "title": "Not This", "artists": [{"name": "Nobody"}]},
        {"position": "2", "type_": "track", "title": TITLE, "artists": [{"name": ARTIST}]},
    ]
    fetch = routed(
        search=results(11), releases={11: release(11, artist="Various", tracks=tracks)}
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "matched"


def test_a_compilation_track_credited_to_another_artist_is_not_a_match():
    tracks = [{"position": "1", "type_": "track", "title": TITLE, "artists": [{"name": "Nobody"}]}]
    fetch = routed(search=results(12), releases={12: release(12, tracks=tracks)})
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "miss"


def test_a_single_matches_on_its_own_title():
    fetch = routed(
        search=results(13),
        releases={13: release(13, title=TITLE, tracks=[{"position": "A", "title": "Dub"}])},
    )
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "matched"


def test_a_heading_and_an_index_row_are_not_tracks():
    tracks = [{"position": "", "type_": "heading", "title": TITLE}]
    fetch = routed(search=results(14), releases={14: release(14, tracks=tracks)})
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "miss"


def test_the_search_asks_by_artist_and_the_title_without_its_mix():
    seen: list[str] = []
    searcher(routed(search=results(), seen=seen))(ARTIST, f"{TITLE} (Extended Mix)")
    (asked,) = [url for url in seen if url.startswith(searchers.DISCOGS_SEARCH)]
    assert "type=release" in asked
    assert "artist=Bernard+Badie" in asked
    assert "track=Sunrise+Mood&" in asked or asked.endswith("track=Sunrise+Mood")


def test_only_the_first_releases_are_read_and_by_their_own_number():
    seen: list[str] = []
    numbers = (21, 22, 23, 24, 25)
    misses = {n: release(n, artist="Somebody Else Entirely") for n in numbers}
    searcher(routed(search=results(*numbers), releases=misses, seen=seen))(ARTIST, TITLE)
    read = [url for url in seen if url.startswith(searchers.DISCOGS_RELEASE)]
    assert read == [f"{searchers.DISCOGS_RELEASE}{n}" for n in numbers[: searchers.DISCOGS_RELEASES_READ]]


def test_a_result_that_names_a_master_or_no_number_is_not_read():
    seen: list[str] = []
    payload = json.dumps(
        {"results": [{"id": "77", "type": "release"}, {"id": 78, "type": "master"}, {"id": 79}]}
    )
    fetch = routed(search=payload, releases={79: release(79)}, seen=seen)
    hit = searcher(fetch)(ARTIST, TITLE)
    assert [url for url in seen if url.startswith(searchers.DISCOGS_RELEASE)] == [
        f"{searchers.DISCOGS_RELEASE}79"
    ]
    assert discogs_answer(hit).answer == "matched"


def test_a_walk_names_known_sources_once():
    with pytest.raises(ValueError):
        searchers.catalogue_searcher(TAXONOMY, walk=(searchers.BEATPORT, "juno"))
    with pytest.raises(ValueError):
        searchers.catalogue_searcher(TAXONOMY, walk=(searchers.BEATPORT, searchers.BEATPORT))


# ---------------------------------------------------------------------------
# B. What is not an answer: no token, a rejection, refusals, outages, reshapes
# ---------------------------------------------------------------------------


def test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit():
    seen: list[str] = []
    hit = searcher(routed(search=results(1), seen=seen), token=None)(ARTIST, TITLE)

    entry = discogs_answer(hit)
    assert entry.answer == searchers.NOT_ASKED
    assert entry.note == searchers.DISCOGS_NO_TOKEN
    assert "crate login discogs-token --from-file" in entry.note
    assert hit.unread == (searchers.DISCOGS,)
    assert not any(url.startswith(searchers.DISCOGS_API) for url in seen)


def test_a_searcher_built_with_no_asker_has_no_token_and_reads_no_keychain(monkeypatch):
    def detonate(*_a, **_k):
        raise AssertionError("a direct caller reached the keychain")

    monkeypatch.setattr(secrets, "exists", detonate)
    monkeypatch.setattr(secrets, "get", detonate)
    hit = searchers.catalogue_searcher(
        TAXONOMY, fetch=routed(search=results()), sleep=lambda _s: None
    )(ARTIST, TITLE)
    assert discogs_answer(hit).note == searchers.DISCOGS_NO_TOKEN


def test_a_file_swept_without_a_token_is_sources_unread_not_no_hit(tmp_path, silence):
    path = tmp_path / "a.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE})

    result = tag.tag_one(path, searcher=searcher(routed(search=results()), token=None))

    assert result.skipped == tag.SOURCES_UNREAD
    assert result.skipped != tag.NO_HIT
    assert tags.read_genre_from_file(path) is None


def test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs(tmp_path, silence):
    """Beatport answered, so the general catalogue is asked; its miss leaves the
    file askable, because Discogs was never asked."""
    path = tmp_path / "b.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE, "isrc": "GBAYE0000001"})
    asked: list[object] = []

    def lookup(isrc):
        asked.append(isrc)
        return published.Published(published.SOURCE, "miss")

    result = tag.tag_one(
        path,
        searcher=searcher(routed(search=results()), token=None),
        published=published.second_opinion(TAXONOMY, lookup=lookup),
    )
    assert asked, "the general catalogue was asked"
    assert result.skipped == tag.SOURCES_UNREAD


def test_a_rejected_token_is_a_run_refusal_typed_as_a_rejection():
    fetch = routed(search=searchers.Fetched(note="HTTP 401", status=401))
    with pytest.raises(CratekitError) as raised:
        searcher(fetch)(ARTIST, TITLE)
    cause = raised.value.cause
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy is Remedy.REAUTHENTICATE
    assert cause.scope is Scope.RUN
    assert isinstance(raised.value.__cause__, secrets.CredentialRejected)
    assert "crate login discogs-token" in " ".join(cause.remediation.steps)
    assert SENT not in cause.message and SENT not in json.dumps(cause.detail)


def test_a_401_on_a_release_read_is_the_same_rejection():
    fetch = routed(search=results(1), releases={1: searchers.Fetched(note="HTTP 401", status=401)})
    with pytest.raises(CratekitError) as raised:
        searcher(fetch)(ARTIST, TITLE)
    assert isinstance(raised.value.__cause__, secrets.CredentialRejected)


def test_a_token_that_is_not_one_printable_word_is_refused_and_never_sent():
    seen: list[str] = []
    with pytest.raises(CratekitError) as raised:
        searcher(routed(search=results(), seen=seen), token="two words")(ARTIST, TITLE)
    assert isinstance(raised.value.__cause__, secrets.CredentialRejected)
    assert "two words" not in raised.value.cause.message
    assert not any(url.startswith(searchers.DISCOGS_API) for url in seen)


def test_a_403_or_a_challenge_is_blocked_not_a_miss():
    for page in (
        searchers.Fetched(note="HTTP 403", status=403),
        searchers.Fetched(text="<html><title>Just a moment...</title></html>", status=200),
    ):
        hit = searcher(routed(search=page))(ARTIST, TITLE)
        assert discogs_answer(hit).answer == "blocked"
        assert hit.unread == (searchers.DISCOGS,)


def test_a_5xx_or_a_body_that_is_not_json_is_unreachable():
    for page in (
        searchers.Fetched(note="HTTP 503", status=503),
        searchers.Fetched(note="transport failure: timed out"),
        searchers.Fetched(text="<html>captive portal</html>", status=200),
    ):
        hit = searcher(routed(search=page))(ARTIST, TITLE)
        assert discogs_answer(hit).answer == "unreachable"
        assert hit.unread == (searchers.DISCOGS,)


def test_json_in_a_shape_this_reader_does_not_know_is_a_parse_break():
    for page in (
        json.dumps({"pagination": {}}),
        json.dumps([1, 2, 3]),
        json.dumps({"results": [{"title": "no number here"}]}),
    ):
        hit = searcher(routed(search=page))(ARTIST, TITLE)
        assert discogs_answer(hit).answer == "parse-break", page
        assert hit.unread == (searchers.DISCOGS,)


def test_a_release_without_a_tracklist_is_held_as_a_parse_break_not_a_miss():
    broken = json.dumps({"id": 1, "styles": ["Disco"]})
    hit = searcher(routed(search=results(1), releases={1: broken}))(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "parse-break"


def test_a_release_that_could_not_be_read_beside_misses_is_not_a_miss():
    fetch = routed(
        search=results(1, 2),
        releases={
            1: searchers.Fetched(note="HTTP 502", status=502),
            2: release(2, artist="Somebody Else Entirely"),
        },
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "unreachable"


def test_a_release_read_that_could_not_be_had_gives_way_to_a_later_match():
    fetch = routed(
        search=results(1, 2),
        releases={1: searchers.Fetched(note="HTTP 502", status=502), 2: release(2)},
    )
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "matched"


def test_a_gone_release_is_passed_over():
    fetch = routed(
        search=results(1, 2),
        releases={1: searchers.Fetched(note="HTTP 404", status=404), 2: release(2)},
    )
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "matched"
    only_gone = routed(search=results(1), releases={1: searchers.Fetched(note="HTTP 404", status=404)})
    assert discogs_answer(searcher(only_gone)(ARTIST, TITLE)).answer == "miss"


def test_a_block_on_a_release_read_ends_the_walk_over_releases():
    seen: list[str] = []
    fetch = routed(
        search=results(1, 2),
        releases={1: searchers.Fetched(note="HTTP 403", status=403), 2: release(2)},
        seen=seen,
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "blocked"
    assert f"{searchers.DISCOGS_RELEASE}2" not in seen


def test_beatport_unreachable_and_discogs_unasked_refuse_as_an_outage_naming_the_token():
    fetch = routed(search=results(), beatport=searchers.Fetched(note="HTTP 503", status=503))
    with pytest.raises(CratekitError) as raised:
        searcher(fetch, token=None)(ARTIST, TITLE)
    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert any(searchers.DISCOGS_NO_TOKEN in step for step in cause.remediation.steps)


def test_beatport_unreachable_and_a_discogs_parse_break_refuse_as_a_defect():
    fetch = routed(
        search=json.dumps({"pagination": {}}),
        beatport=searchers.Fetched(note="HTTP 503", status=503),
    )
    with pytest.raises(CratekitError) as raised:
        searcher(fetch)(ARTIST, TITLE)
    assert raised.value.cause.reason == searchers.PARSE_BREAK_REASON
    assert raised.value.cause.detail["sources"] == [searchers.DISCOGS]


def test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over():
    hit = searchers.catalogue_searcher(
        TAXONOMY, walk=(searchers.DISCOGS,), sleep=lambda _s: None
    )(ARTIST, TITLE)
    assert hit.genre is None and hit.unread == (searchers.DISCOGS,)


# ---------------------------------------------------------------------------
# C. The rate limit: one pacer, the remaining count, the ladder, the memory
# ---------------------------------------------------------------------------


class Reply:
    """What the shipped fetch reads off a response: a status, a body, headers."""

    def __init__(self, status: int, text: str = "", headers: dict | None = None) -> None:
        self.status_code = status
        self.text = text
        self.headers = headers or {}


def over_the_wire(replies: dict, *, sent: list | None = None, naps: list[float] | None = None):
    """The shipped asker over the shipped fetch, its getter answering by URL.

    ``replies`` maps a URL prefix to a reply or to a list of replies served in
    turn. ``sent`` records every (url, headers) pair the getter was handed.
    """
    queues = {key: list(value) if isinstance(value, list) else value for key, value in replies.items()}
    naps = naps if naps is not None else []

    def get(url, headers, timeout):
        if sent is not None:
            sent.append((url, dict(headers)))
        for prefix in sorted(queues, key=len, reverse=True):
            if url == prefix or (prefix.endswith("search") and url.startswith(prefix)):
                answer = queues[prefix]
                return answer.pop(0) if isinstance(answer, list) else answer
        raise OSError(f"no route for {url}")

    fetch = searchers.default_fetch(get=get, sleep=naps.append, headers=searchers.discogs_headers(SENT))
    return searchers.discogs_asker(token=SENT, fetch=fetch, sleep=naps.append)


def test_a_429_then_an_answer_within_the_ladder_is_read():
    naps: list[float] = []
    discogs = over_the_wire(
        {
            searchers.DISCOGS_SEARCH: [Reply(429), Reply(200, results(1))],
            f"{searchers.DISCOGS_RELEASE}1": Reply(200, release(1)),
        },
        naps=naps,
    )
    said_ = discogs.ask(ARTIST, TITLE)
    assert said_.answer is searchers.Answer.MATCHED
    assert searchers.RATE_LIMIT_BASE_WAIT_S in naps


def test_a_429_on_every_attempt_is_blocked_and_remembered_for_the_run():
    sent: list = []
    naps: list[float] = []
    discogs = over_the_wire({searchers.DISCOGS_SEARCH: Reply(429)}, sent=sent, naps=naps)

    first = discogs.ask(ARTIST, TITLE)
    assert first.answer is searchers.Answer.BLOCKED
    assert len(sent) == searchers.RATE_LIMIT_ATTEMPTS
    ladder = naps.count(searchers.RATE_LIMIT_BASE_WAIT_S) + naps.count(2 * searchers.RATE_LIMIT_BASE_WAIT_S)

    second = discogs.ask("Another Artist", "Another Title")
    assert second.answer is searchers.Answer.BLOCKED
    assert "earlier in this run" in second.note
    assert len(sent) == searchers.RATE_LIMIT_ATTEMPTS, "nothing more was sent"
    assert (
        naps.count(searchers.RATE_LIMIT_BASE_WAIT_S) + naps.count(2 * searchers.RATE_LIMIT_BASE_WAIT_S)
        == ladder
    ), "no file after the first sleeps the ladder again"


def test_a_low_remaining_count_slows_the_next_request_and_a_high_one_does_not():
    naps: list[float] = []
    low = {searchers.DISCOGS_REMAINING_HEADER.upper(): str(searchers.DISCOGS_REMAINING_FLOOR)}
    discogs = over_the_wire(
        {
            searchers.DISCOGS_SEARCH: Reply(200, results(1), low),
            f"{searchers.DISCOGS_RELEASE}1": Reply(200, release(1), {"X-Discogs-Ratelimit-Remaining": "50"}),
        },
        naps=naps,
    )
    discogs.ask(ARTIST, TITLE)
    assert naps.count(searchers.DISCOGS_SLOWDOWN_S) == 1, naps
    discogs.ask(ARTIST, TITLE)
    assert naps.count(searchers.DISCOGS_SLOWDOWN_S) == 2, "the low count is read again"


def test_one_floor_above_does_not_slow_down():
    naps: list[float] = []
    count = {"X-Discogs-Ratelimit-Remaining": str(searchers.DISCOGS_REMAINING_FLOOR + 1)}
    discogs = over_the_wire(
        {
            searchers.DISCOGS_SEARCH: Reply(200, results(1), count),
            f"{searchers.DISCOGS_RELEASE}1": Reply(200, release(1), count),
        },
        naps=naps,
    )
    discogs.ask(ARTIST, TITLE)
    discogs.ask(ARTIST, TITLE)
    assert searchers.DISCOGS_SLOWDOWN_S not in naps


def test_every_touch_is_paced_by_one_pacer_across_files():
    waits: list[float] = []
    pacer = searchers.Pacer(sleep=waits.append)
    fetch = routed(search=results(1), releases={1: release(1)})
    discogs = searchers.discogs_asker(token=SENT, fetch=fetch, pacing=pacer)
    discogs.ask(ARTIST, TITLE)
    discogs.ask(ARTIST, TITLE)
    assert len(waits) == 4, "a search and a release read per file, each paced"
    assert all(searchers.MIN_INTERVAL_S <= wait for wait in waits)


def test_the_shipped_fetch_carries_the_answer_headers_lowercased():
    fetch = searchers.default_fetch(
        get=lambda url, headers, timeout: Reply(200, "{}", {"X-Thing": "1"}), sleep=lambda _s: None
    )
    page = fetch("https://example.invalid/")
    assert dict(page.headers) == {"x-thing": "1"}
    assert isinstance(page.headers, MappingProxyType)
    refused = searchers.default_fetch(
        get=lambda url, headers, timeout: Reply(503, "", {"X-Thing": "1"}), sleep=lambda _s: None
    )("https://example.invalid/")
    assert dict(refused.headers) == {}


# ---------------------------------------------------------------------------
# D. The token goes in one place
# ---------------------------------------------------------------------------


def test_the_token_is_sent_in_the_authorization_header_and_the_agent_names_cratekit():
    sent: list = []
    discogs = over_the_wire(
        {
            searchers.DISCOGS_SEARCH: Reply(200, results(1)),
            f"{searchers.DISCOGS_RELEASE}1": Reply(200, release(1)),
        },
        sent=sent,
    )
    discogs.ask(ARTIST, TITLE)
    assert sent
    for url, headers in sent:
        assert headers["Authorization"] == f"Discogs token={SENT}"
        assert headers["User-Agent"] == f"Cratekit/{__version__}"
        assert SENT not in url


def test_the_token_reaches_no_url_note_record_log_or_refusal(caplog, tmp_path, silence):
    """Every path a Discogs answer takes to a person, scanned for the token.

    A transport failure whose message names the token, as a client library's
    refusal of an invalid header does, is scrubbed before it becomes a note.
    """
    caplog.set_level(logging.DEBUG)
    sent: list = []
    seen_text: list[str] = []

    def leaky(url, headers, timeout):
        sent.append((url, dict(headers)))
        raise ValueError(f"Invalid header value {headers['Authorization']!r}")

    leaking = searchers.discogs_asker(
        token=SENT,
        fetch=searchers.default_fetch(get=leaky, sleep=lambda _s: None, headers=searchers.discogs_headers(SENT)),
        sleep=lambda _s: None,
    )
    hits = [searcher(routed(search=results()), discogs=leaking)(ARTIST, TITLE)]
    for replies in (
        {searchers.DISCOGS_SEARCH: Reply(200, results(1)), f"{searchers.DISCOGS_RELEASE}1": Reply(200, release(1))},
        {searchers.DISCOGS_SEARCH: Reply(429)},
        {searchers.DISCOGS_SEARCH: Reply(200, "not json")},
        {searchers.DISCOGS_SEARCH: Reply(200, json.dumps({"x": 1}))},
    ):
        discogs = over_the_wire(replies, sent=sent)
        hits.append(searcher(routed(search=results()), discogs=discogs)(ARTIST, TITLE))
    try:
        over_the_wire({searchers.DISCOGS_SEARCH: Reply(401)}, sent=sent).ask(ARTIST, TITLE)
    except CratekitError as exc:
        seen_text.append(exc.cause.message)
        seen_text.append(json.dumps(exc.cause.detail))
        seen_text.extend(exc.cause.remediation.steps)

    path = tmp_path / "c.flac"
    path.write_bytes(Path(silence).read_bytes())
    assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE})
    result = tag.tag_one(path, searcher=searcher(routed(search=results()), discogs=leaking))

    assert "Invalid header value" in discogs_answer(hits[0]).note, "the leak was exercised"
    for hit in hits:
        seen_text.extend(entry.note for entry in hit.answers)
        seen_text.append(repr(hit))
    seen_text.append(repr(result))
    seen_text.append(caplog.text)
    seen_text.extend(url for url, _headers in sent)
    assert sent, "requests were made"
    for text in seen_text:
        assert SENT not in text, text


# ---------------------------------------------------------------------------
# E. The token's keychain read, and the worker's process wide asker
# ---------------------------------------------------------------------------


@pytest.fixture
def fresh_asker(monkeypatch):
    monkeypatch.setattr(searchers, "_shared_discogs", [])


def test_no_recorded_token_reads_no_keychain_and_is_not_asked(monkeypatch, fresh_asker):
    monkeypatch.setattr(secrets, "exists", lambda name: False)

    def detonate(_name):
        raise AssertionError("the keychain was read for a token nobody recorded")

    monkeypatch.setattr(secrets, "get", detonate)
    discogs = searchers.for_discogs()
    assert discogs.token is None
    assert discogs.ask(ARTIST, TITLE) == searchers.NotAsked(searchers.DISCOGS, searchers.DISCOGS_NO_TOKEN)


def test_a_recorded_token_the_keychain_lost_is_not_asked_and_says_so(monkeypatch, fresh_asker):
    monkeypatch.setattr(secrets, "exists", lambda name: True)

    def missing(name):
        raise secrets.CredentialMissing("gone", name=name)

    monkeypatch.setattr(secrets, "get", missing)
    said_ = searchers.for_discogs().ask(ARTIST, TITLE)
    assert said_ == searchers.NotAsked(searchers.DISCOGS, searchers.DISCOGS_TOKEN_LOST)
    assert searchers.DISCOGS_TOKEN_LOST in searchers.DISCOGS_UNASKED_NOTES


def test_a_keychain_that_cannot_be_read_is_refused_not_read_as_no_token(monkeypatch, fresh_asker):
    monkeypatch.setattr(secrets, "exists", lambda name: True)

    def broken(name):
        raise secrets.CredentialBackendUnavailable("no backend", name=name)

    monkeypatch.setattr(secrets, "get", broken)
    with pytest.raises(CratekitError) as raised:
        searchers.for_discogs()
    assert raised.value.cause.remediation.remedy is Remedy.INSTALL_KEYCHAIN_BACKEND
    assert searchers._shared_discogs == [], "a refusal is not remembered as an asker"


def test_the_worker_asker_is_one_per_process_and_reads_the_recorded_token(monkeypatch, fresh_asker):
    reads: list[str] = []
    monkeypatch.setattr(secrets, "exists", lambda name: name == "discogs-token")

    def get(name):
        reads.append(name)
        return SENT

    monkeypatch.setattr(secrets, "get", get)
    first, second = searchers.for_discogs(), searchers.for_discogs()
    assert first is second and first.token == SENT
    assert reads == ["discogs-token"]
    assert first.fetch is not None


def test_for_taxonomy_hands_the_worker_asker_to_the_searcher(monkeypatch):
    calls: list[tuple[str, str]] = []

    class Recording:
        def ask(self, artist, title):
            calls.append((artist, title))
            return searchers.SourceOutcome(searchers.DISCOGS, searchers.Answer.MISS)

    monkeypatch.setattr(searchers, "for_discogs", lambda: Recording())
    monkeypatch.setattr(searchers, "default_fetch", lambda **_k: routed(search=results()))
    monkeypatch.setattr(searchers.Pacer, "wait", lambda self: 0.0)
    hit = searchers.for_taxonomy(TAXONOMY)(ARTIST, TITLE)
    assert calls == [(ARTIST, TITLE)]
    assert said(hit) == [(searchers.BEATPORT, "miss"), (searchers.DISCOGS, "miss")]


# ---------------------------------------------------------------------------
# F. The taxonomy files every listed style, through the resolver
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("style", BRIEF_STYLES)
def test_every_listed_style_names_a_folder_in_the_default_taxonomy(style):
    picked = searchers.choose_word(TAXONOMY, [style], source=searchers.DISCOGS, named_only=True)
    assert picked is not None, style
    word, written = picked
    assert word == style
    place = TAXONOMY.named_folder(written)
    assert place is not None and place[0] != TAXONOMY.fallback.bucket
    assert not TAXONOMY.is_too_coarse_as_source(written)


def test_the_discogs_table_holds_only_words_the_aliases_did_not_file():
    """A row for a word the aliases already file would be a second answer to one
    question; the measured nine are the rows, and four more from round one."""
    (table,) = [one for one in TAXONOMY.vocabularies if one.source == searchers.DISCOGS]
    rows = {row.word for row in table.words}
    assert rows == {
        "Nu-Disco",
        "Italo-Disco",
        "Boogie",
        "Electro",
        "Leftfield",
        "Acid House",
        "Techno",
        "Garage House",
        "Soulful House",
        # Round one's: three the substring rules filed as Progressive House,
        # and Heavy Metal beside them. No row writes Jazz: a copy made before
        # the Jazz folder would not load with one once its hold's edits are
        # made (round two).
        "Progressive Trance",
        "Progressive Rock",
        "Progressive Metal",
        "Heavy Metal",
    }
    plain = TAXONOMY.vocabulary(searchers.DISCOGS)
    assert plain is not None and set(plain) == {word.lower() for word in rows}


def test_the_genre_is_resolved_by_suggest_tag_and_not_by_a_map(monkeypatch):
    """Replace the resolver and the written tag follows it: nothing in the
    searcher holds a second answer."""
    real = routing.suggest_tag

    def moved(declared, raw, *, bpm=None, source=None):
        if raw == "Nu-Disco":
            return real(declared, "Deep House", source=source)
        return real(declared, raw, bpm=bpm, source=source)

    monkeypatch.setattr(routing, "suggest_tag", moved)
    fetch = routed(search=results(7), releases={7: release(7, styles=("Nu-Disco",))})
    hit = searcher(fetch)(ARTIST, TITLE)
    assert hit.genre == real(TAXONOMY, "Deep House", source=searchers.DISCOGS).tag


def test_the_general_catalogue_chooses_by_the_same_chooser(monkeypatch):
    calls: list[tuple] = []
    monkeypatch.setattr(
        searchers, "choose_word", lambda declared, words, **kw: calls.append((tuple(words), kw))
    )
    published.choose(TAXONOMY, ["Rock"])
    assert calls == [(("Rock",), {"source": published.SOURCE, "named_only": True})]


# ---------------------------------------------------------------------------
# G. The reports: old records still summarise, a missing token is said
# ---------------------------------------------------------------------------


def _summarised(monkeypatch, reports: list[dict]) -> dict:
    monkeypatch.setattr(tag_cli.artifacts, "committed", lambda cfg, job_id: iter(reports))
    return tag_cli._summary(None, "job", {})


def test_a_record_written_by_the_old_three_sources_still_summarises(monkeypatch):
    old = {
        "item": "a.flac",
        "skipped": tag.SOURCES_UNREAD,
        "answers": [
            {"source": "beatport", "answer": "miss"},
            {"source": "traxsource", "answer": "blocked"},
            {"source": "bandcamp", "answer": "blocked"},
            {"source": "deezer", "answer": "miss"},
        ],
    }
    summary = _summarised(monkeypatch, [old])
    assert summary["answers"][searchers.TRAXSOURCE]["blocked"] == 1
    assert summary["answers"][searchers.BANDCAMP]["blocked"] == 1
    assert summary["answers"][searchers.DISCOGS] == dict.fromkeys(
        summary["answers"][searchers.DISCOGS], 0
    )
    assert summary["discogs_without_token"] == 0
    assert tag_cli._discogs_warnings(summary) == ()


def test_files_discogs_was_not_asked_about_for_want_of_a_token_are_counted_and_warned(monkeypatch):
    def report(item: str, note: str) -> dict:
        return {
            "item": item,
            "skipped": tag.SOURCES_UNREAD,
            "answers": [
                {"source": "beatport", "answer": "miss"},
                {"source": "discogs", "answer": searchers.NOT_ASKED, "note": note},
            ],
        }

    matched_first = {
        "item": "c.flac",
        "genre_written": "Deep House",
        "source": "beatport",
        "answers": [
            {"source": "beatport", "answer": "matched"},
            {"source": "discogs", "answer": searchers.NOT_ASKED, "note": ""},
        ],
    }
    summary = _summarised(
        monkeypatch,
        [
            report("a.flac", searchers.DISCOGS_NO_TOKEN),
            report("b.flac", searchers.DISCOGS_TOKEN_LOST),
            matched_first,
        ],
    )
    assert summary["discogs_without_token"] == 2
    assert summary["answers"][searchers.DISCOGS][searchers.NOT_ASKED] == 3
    (warning,) = tag_cli._discogs_warnings(summary)
    assert warning["code"] == tag_cli.DISCOGS_NO_TOKEN_FILES == "tag-folder-discogs-no-token"
    assert "2 file(s)" in warning["message"]
    assert "crate login discogs-token --from-file PATH" in warning["message"]


def test_a_discogs_blocked_on_every_search_is_named_like_any_shop():
    summary = {
        "skipped": {tag.SOURCES_UNREAD: 2},
        "answers": {
            searchers.BEATPORT: {"miss": 2},
            searchers.DISCOGS: {"blocked": 2, searchers.NOT_ASKED: 0},
        },
    }
    codes = [w["code"] for w in tag_cli._unread_warnings(summary)]
    assert tag_cli.SOURCE_BLOCKED in codes
    blocked = [w for w in tag_cli._unread_warnings(summary) if w["code"] == tag_cli.SOURCE_BLOCKED]
    assert searchers.DISCOGS in blocked[0]["message"]


# ---------------------------------------------------------------------------
# H. Round one's fixes
# ---------------------------------------------------------------------------


BRACKETED = "(Not Just) Knee Deep (Part 1)"


def test_a_title_of_brackets_is_searched_whole_and_matches_no_other_track():
    """B1. The shared strip empties this title, which asked Discogs for every
    release by the artist and read the empty remainder as a match."""
    seen: list[str] = []
    other = [{"position": "A1", "type_": "track", "title": "Maggot Brain"}]
    fetch = routed(
        search=results(31), releases={31: release(31, title="Maggot Brain", tracks=other)}, seen=seen
    )
    hit = searcher(fetch)("Funkadelic", BRACKETED)
    assert discogs_answer(hit).answer == "miss"
    assert hit.genre is None
    (asked,) = [url for url in seen if url.startswith(searchers.DISCOGS_SEARCH)]
    assert "track=%28Not+Just%29+Knee+Deep&" in asked


def test_a_title_of_brackets_still_matches_its_own_track():
    tracks = [{"position": "A1", "type_": "track", "title": "(Not Just) Knee Deep"}]
    fetch = routed(search=results(32), releases={32: release(32, artist="Funkadelic", tracks=tracks)})
    assert discogs_answer(searcher(fetch)("Funkadelic", BRACKETED)).answer == "matched"


def test_a_skit_row_matches_no_searched_title():
    tracks = [{"position": "A1", "type_": "track", "title": "(Skit)"}]
    fetch = routed(search=results(33), releases={33: release(33, tracks=tracks)})
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "miss"


def test_an_empty_title_on_either_side_matches_nothing():
    assert not searchers._discogs_title_matches("", TITLE)
    assert not searchers._discogs_title_matches(TITLE, "")
    assert searchers._discogs_title_matches(f"{TITLE} (Extended Mix)", TITLE)


def test_a_rejected_token_is_not_sent_again_in_the_run():
    """R1. After the first 401 every later file is refused the same way with
    no request, so the rejected token is not resent per file."""
    sent: list = []
    discogs = over_the_wire({searchers.DISCOGS_SEARCH: Reply(401)}, sent=sent)
    for _ in range(3):
        with pytest.raises(CratekitError) as raised:
            discogs.ask(ARTIST, TITLE)
        assert isinstance(raised.value.__cause__, secrets.CredentialRejected)
    assert len(sent) == 1
    assert "earlier in this run" in raised.value.cause.message


def test_the_general_catalogue_waits_for_a_discogs_that_was_asked_and_unread():
    """R2. An album word written while Discogs could not be read would stand in
    for its style for good."""
    asked: list[object] = []

    def lookup(isrc):
        asked.append(isrc)
        return published.Published(published.SOURCE, "matched", genres=("Rock",))

    hit = searcher(routed(search=searchers.Fetched(note="HTTP 503", status=503)))(ARTIST, TITLE)
    decided = published.second_opinion(TAXONOMY, lookup=lookup)(hit, "GBAYE0000001")
    assert asked == []
    assert decided.genre is None
    assert decided.answers[-1].answer == searchers.NOT_ASKED
    assert "discogs was asked and not read" in decided.answers[-1].note
    unasked = searcher(routed(search=results()), token=None)(ARTIST, TITLE)
    published.second_opinion(TAXONOMY, lookup=lookup)(unasked, "GBAYE0000001")
    assert asked == ["GBAYE0000001"], "a Discogs nobody asked does not hold it back"


def test_discogs_names_are_read_as_a_tag_spells_them():
    """R4. "Prodigy, The" is one artist, so The Orb does not match it."""
    assert searchers._discogs_name("Prodigy, The") == "The Prodigy"
    assert searchers._discogs_name("Moodymann (2)") == "Moodymann"
    assert searchers._discogs_name("Theo Parrish*") == "Theo Parrish"
    tracks = [{"position": "1", "type_": "track", "title": "Higher", "artists": [{"name": "Prodigy, The"}]}]
    fetch = routed(search=results(34), releases={34: release(34, artist="Various", tracks=tracks)})
    assert discogs_answer(searcher(fetch)("The Orb", "Higher")).answer == "miss"
    fetch = routed(search=results(35), releases={35: release(35, artist="Moodymann (2)")})
    assert discogs_answer(searcher(fetch)("Moodymann", TITLE)).answer == "matched"


def test_a_pressing_with_no_style_gives_way_to_one_with_styles():
    """R5. The styleless match is kept only when no later pressing has styles."""
    fetch = routed(
        search=results(36, 37),
        releases={36: release(36, styles=()), 37: release(37, styles=("Deep House",))},
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert hit.source_genre == "Deep House" and hit.genre is not None


def test_a_track_under_an_index_row_is_read():
    tracks = [
        {
            "position": "A",
            "type_": "index",
            "title": "Suite",
            "sub_tracks": [{"position": "A.1", "type_": "track", "title": TITLE}],
        }
    ]
    fetch = routed(search=results(38), releases={38: release(38, tracks=tracks)})
    assert discogs_answer(searcher(fetch)(ARTIST, TITLE)).answer == "matched"


def test_a_file_searched_only_for_its_picture_is_not_counted_as_owed_discogs(monkeypatch):
    """R6. It already has a genre, so Discogs was owed it nothing."""
    summary = _summarised(
        monkeypatch,
        [
            {
                "item": "a.flac",
                "skipped": tag.HAS_GENRE,
                "answers": [
                    {"source": "beatport", "answer": "miss"},
                    {"source": "discogs", "answer": searchers.NOT_ASKED, "note": searchers.DISCOGS_NO_TOKEN},
                ],
            }
        ],
    )
    assert summary["discogs_without_token"] == 0


def test_the_token_is_not_in_the_askers_repr():
    """R9."""
    assert SENT not in repr(searchers.discogs_asker(token=SENT, fetch=routed(search=results())))


def test_a_remaining_count_that_is_not_ascii_digits_is_no_count():
    assert searchers._remaining({searchers.DISCOGS_REMAINING_HEADER: "²"}) is None
    assert searchers._remaining({searchers.DISCOGS_REMAINING_HEADER: " 7 "}) == 7
    assert searchers._remaining({}) is None


def test_a_search_answering_404_is_unreachable_not_a_miss():
    hit = searcher(routed(search=searchers.Fetched(note="HTTP 404", status=404)))(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "unreachable"


def test_the_shipped_asker_sends_the_token_to_discogs_only(monkeypatch):
    """The default fetch's wiring, through the one getter that names requests:
    the token and the agent go to Discogs, and Beatport is asked as a browser."""
    sent: list[tuple[str, dict]] = []

    def get(url, *, headers, timeout):
        sent.append((url, dict(headers)))
        if url.startswith(searchers.BEATPORT_SEARCH):
            return Reply(200, _beatport_page([]))
        if url.startswith(searchers.DISCOGS_SEARCH):
            return Reply(200, results())
        raise OSError(url)

    monkeypatch.setattr(searchers, "_requests_get", get)
    discogs = searchers.discogs_asker(token=SENT, sleep=lambda _s: None)
    searchers.catalogue_searcher(TAXONOMY, sleep=lambda _s: None, discogs=discogs)(ARTIST, TITLE)
    by_host = {url.split("?")[0]: headers for url, headers in sent}
    assert by_host[searchers.DISCOGS_SEARCH]["Authorization"] == f"Discogs token={SENT}"
    assert by_host[searchers.DISCOGS_SEARCH]["User-Agent"] == f"Cratekit/{__version__}"
    assert "Authorization" not in by_host[searchers.BEATPORT_SEARCH]
    assert by_host[searchers.BEATPORT_SEARCH] == searchers.HEADERS


def test_the_numbers_this_source_spends_are_the_ones_stated():
    """Pinned as numbers, so a change to one is a decision a reviewer reads:
    three releases a miss, ten results a page, a ten second wait at five left."""
    assert searchers.DISCOGS_RELEASES_READ == 3
    assert searchers.DISCOGS_RESULTS_PER_PAGE == 10
    assert searchers.DISCOGS_REMAINING_FLOOR == 5
    assert searchers.DISCOGS_SLOWDOWN_S == 10.0


def test_discogs_chooses_only_a_named_folder_even_on_a_copy_with_no_table():
    """``named_only`` is always on for Discogs: a word the aliases file by a
    bucket's bare name, with no exact declaration, is not written."""
    word = "NonElectronic"
    assert TAXONOMY.named_folder(word) is None
    assert searchers.choose_word(TAXONOMY, [word], source=searchers.DISCOGS, named_only=True) is None
    fetch = routed(search=results(39), releases={39: release(39, styles=(word,))})
    assert searcher(fetch)(ARTIST, TITLE).genre is None


def test_a_styleless_match_beside_an_unread_pressing_is_unread_not_a_match():
    """Round two: what the unread pressing held is unknown, and a match with no
    style would let the general catalogue write over it."""
    fetch = routed(
        search=results(40, 41),
        releases={40: release(40, styles=()), 41: searchers.Fetched(note="HTTP 503", status=503)},
    )
    hit = searcher(fetch)(ARTIST, TITLE)
    assert discogs_answer(hit).answer == "unreachable"
    assert hit.unread == (searchers.DISCOGS,)


def test_a_word_resolving_to_the_fallback_is_passed_over_where_its_name_is_not_too_coarse():
    """The fallback check stands alone on a copy whose fallback name is not in
    its too coarse list: the shipped template's lists it, which covered the
    check and left it killing nothing (the mutation table's M19)."""
    from cratekit.core.taxonomy import load_taxonomy, shipped_template_text

    text = shipped_template_text("default")
    line = 'too_coarse_as_source = ["", "Electronica", "Electronic", "Electronica / Other"]'
    assert text.count(line) == 1
    copy = load_taxonomy(text.replace(line, 'too_coarse_as_source = [""]'))
    suggestion = routing.suggest_tag(copy, FALLBACK_GENRE, source=searchers.DISCOGS)
    assert suggestion.bucket_id == copy.fallback.bucket
    assert not copy.is_too_coarse_as_source(suggestion.tag)
    assert searchers.choose_word(copy, [FALLBACK_GENRE], source=published.SOURCE, named_only=False) is None
