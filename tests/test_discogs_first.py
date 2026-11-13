"""U282: a tag sweep asks Discogs first, and Beatport only when Discogs gives no genre.

WHAT THIS SUITE GUARDS, the card's merge blockers first:

* WITH NO DISCOGS TOKEN BEATPORT IS ASKED EXACTLY AS BEFORE, so a person who
  never recorded one sees no change but the order of a record's answers.
* A DISCOGS DECLINE GOES ON TO BEATPORT. An unmapped style, or one landing
  only on the fallback bucket, writes nothing and leaves the question open,
  so the walk asks the next catalogue; when that one cannot settle it either,
  the file keeps Discogs' word, never a ``no-hit`` and never an outage.
* A REFUSED OR UNREAD CATALOGUE IS NEVER A MISS, on the walk and on the
  picture's ask alike.
* THE COVER STILL ARRIVES. Discogs names no picture, so a file Discogs tagged
  and missing one asks Beatport for its row's cover, and only such a file: a
  file with a picture, ``tag suggest`` and ``tag retag`` send Beatport
  nothing after a Discogs match.
* A FILE ALREADY TAGGED IS NEVER RE-TAGGED.

NOTHING HERE TOUCHES THE NETWORK. Every answer is a recorded page or payload
handed to the fetch seam, and the token is a fixture word.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core import routing, secrets, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import searchers, tag
from cratekit.tagging.tag import SearchHit, SourceAnswer
from tests._containers import synth_container
from tests.test_catalogue_searcher import (
    ARTIST,
    BUCKET_GENRE,
    FALLBACK_GENRE,
    TITLE,
    _beatport_page,
    _beatport_track,
)
from tests.test_discogs_searcher import SENT, release, results, routed

TAXONOMY = default_taxonomy()

#: Beatport's cover, as its payload names it, and the address it is asked at.
COVER = "https://geo-media.beatport.com/image_size/1400x1400/cover.jpg"

#: A Discogs style no folder holds and no alias knows.
UNMAPPED = "Hauntological Hymnals"

#: Beatport's refusal, as sitting 97 measured it.
CHALLENGE = searchers.Fetched(note="Cloudflare challenge, HTTP 403", status=403)


def beatport_row(genre: str = BUCKET_GENRE, *, cover: str = COVER) -> str:
    track = _beatport_track(ARTIST, TITLE, genre)
    if cover:
        track["release"] = {"release_image_uri": cover}
    return _beatport_page([track])


def matching_release(*styles: str) -> dict[int, str]:
    return {7: release(7, styles=styles)}


def build(fetch, *, token: str | None = SENT, walk=None, refusals=None):
    asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    extra = {} if walk is None else {"walk": walk}
    return searchers.catalogue_searcher(
        TAXONOMY,
        fetch=fetch,
        sleep=lambda _s: None,
        discogs=asker,
        refusals=refusals,
        **extra,
    )


def said(hit: SearchHit) -> list[tuple[str, str]]:
    return [(one.source, one.answer) for one in hit.answers]


def answer_of(hit: SearchHit, source: str) -> SourceAnswer:
    (one,) = [entry for entry in hit.answers if entry.source == source]
    return one


def beatport_asked(seen: list[str]) -> int:
    return sum(url.startswith(searchers.BEATPORT_SEARCH) for url in seen)


def discogs_tag(style: str) -> str:
    tag_ = routing.suggest_tag(TAXONOMY, style, source=searchers.DISCOGS).tag
    assert tag_ and TAXONOMY.named_folder(tag_) is not None, "the fixture style names a folder"
    return tag_


def beatport_tag() -> str:
    return routing.suggest_tag(TAXONOMY, BUCKET_GENRE).tag


# ---------------------------------------------------------------------------
# A. The order
# ---------------------------------------------------------------------------


def test_the_default_walk_is_discogs_then_beatport():
    assert searchers.WALK == (searchers.DISCOGS, searchers.BEATPORT)


def test_a_record_and_a_summary_list_discogs_first():
    assert searchers.SOURCES[0] == searchers.DISCOGS
    assert set(searchers.SOURCES) == {
        searchers.DISCOGS,
        searchers.BEATPORT,
        searchers.TRAXSOURCE,
        searchers.BANDCAMP,
    }


def test_a_discogs_match_decides_and_beatport_is_not_asked():
    seen: list[str] = []
    fetch = routed(
        search=results(7),
        releases=matching_release("Deep House"),
        beatport=beatport_row(),
        seen=seen,
    )
    hit = build(fetch)(ARTIST, TITLE)
    assert (hit.source, hit.genre) == (searchers.DISCOGS, discogs_tag("Deep House"))
    assert said(hit) == [(searchers.DISCOGS, "matched"), (searchers.BEATPORT, searchers.NOT_ASKED)]
    assert beatport_asked(seen) == 0
    assert hit.unread == ()


def test_a_discogs_miss_asks_beatport_and_beatport_decides():
    seen: list[str] = []
    fetch = routed(search=results(), beatport=beatport_row(), seen=seen)
    hit = build(fetch)(ARTIST, TITLE)
    assert (hit.source, hit.genre) == (searchers.BEATPORT, beatport_tag())
    assert hit.art_url.endswith("cover.jpg")
    assert hit.art_source is None, "Beatport's own row carries its own picture"
    assert said(hit) == [(searchers.DISCOGS, "miss"), (searchers.BEATPORT, "matched")]
    assert hit.ask_picture is None
    # The question is asked of Discogs first, then of Beatport.
    asked = [url.split("?")[0] for url in seen]
    assert asked[0] == searchers.DISCOGS_SEARCH and asked[-1] == searchers.BEATPORT_SEARCH


@pytest.mark.parametrize(
    "styles",
    [(UNMAPPED,), (FALLBACK_GENRE,), (UNMAPPED, FALLBACK_GENRE), ()],
    ids=["unmapped", "fallback-only", "both", "styleless"],
)
def test_a_discogs_decline_goes_on_to_beatport_which_decides(styles):
    seen: list[str] = []
    fetch = routed(
        search=results(7), releases=matching_release(*styles), beatport=beatport_row(), seen=seen
    )
    hit = build(fetch)(ARTIST, TITLE)
    assert beatport_asked(seen) == 1
    assert (hit.source, hit.genre) == (searchers.BEATPORT, beatport_tag())
    assert hit.art_url.endswith("cover.jpg")
    assert said(hit) == [(searchers.DISCOGS, "matched"), (searchers.BEATPORT, "matched")]


def test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit():
    fetch = routed(search=results(7), releases=matching_release(UNMAPPED))
    hit = build(fetch)(ARTIST, TITLE)
    assert hit.genre is None
    assert (hit.source, hit.source_genre) == (searchers.DISCOGS, UNMAPPED)
    assert said(hit) == [(searchers.DISCOGS, "matched"), (searchers.BEATPORT, "miss")]
    assert hit.unread == ()
    assert hit.art_url == "" and hit.art_source == "", "Discogs names no picture"


@pytest.mark.parametrize(
    "refusal, answer",
    [
        (CHALLENGE, "blocked"),
        (searchers.Fetched(note="timed out"), "unreachable"),
        (searchers.Fetched(text="<html>no payload</html>", status=200), "parse-break"),
    ],
    ids=["refused", "outage", "reshaped"],
)
def test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage(
    refusal, answer
):
    fetch = routed(search=results(7), releases=matching_release(UNMAPPED), beatport=refusal)
    hit = build(fetch)(ARTIST, TITLE)
    assert hit.genre is None
    assert (hit.source, hit.source_genre) == (searchers.DISCOGS, UNMAPPED)
    assert said(hit) == [(searchers.DISCOGS, "matched"), (searchers.BEATPORT, answer)]
    assert hit.unread == (searchers.BEATPORT,)


def test_two_declines_keep_discogs_word_and_beatport_s_picture():
    fetch = routed(
        search=results(7),
        releases=matching_release(UNMAPPED),
        beatport=beatport_row(FALLBACK_GENRE),
    )
    hit = build(fetch)(ARTIST, TITLE)
    assert hit.genre is None
    assert (hit.source, hit.source_genre) == (searchers.DISCOGS, UNMAPPED)
    assert answer_of(hit, searchers.BEATPORT).source_genre == FALLBACK_GENRE
    assert (hit.art_url, hit.art_source) == (
        beatport_row_art(),
        searchers.BEATPORT,
    )


def beatport_row_art() -> str:
    return searchers._beatport_art({"release": {"release_image_uri": COVER}})


def test_with_no_token_beatport_decides_exactly_as_before():
    seen: list[str] = []
    fetch = routed(search=results(7), releases=matching_release("Deep House"),
                   beatport=beatport_row(), seen=seen)
    hit = build(fetch, token=None)(ARTIST, TITLE)
    assert (hit.source, hit.genre) == (searchers.BEATPORT, beatport_tag())
    assert hit.art_url == beatport_row_art() and hit.art_source is None
    assert said(hit) == [(searchers.DISCOGS, searchers.NOT_ASKED), (searchers.BEATPORT, "matched")]
    assert answer_of(hit, searchers.DISCOGS).note == searchers.DISCOGS_NO_TOKEN
    assert hit.unread == (searchers.DISCOGS,)
    assert [url.split("?")[0] for url in seen] == [searchers.BEATPORT_SEARCH]


def test_with_no_token_a_beatport_miss_is_still_sources_unread_and_never_no_hit():
    hit = build(routed(search=results()), token=None)(ARTIST, TITLE)
    assert hit.genre is None and hit.source == ""
    assert hit.unread == (searchers.DISCOGS,)


@pytest.mark.parametrize(
    "discogs, answer",
    [
        (CHALLENGE, "blocked"),
        (searchers.Fetched(note="timed out"), "unreachable"),
    ],
    ids=["refused", "outage"],
)
def test_an_unread_discogs_goes_on_to_beatport_and_beside_its_miss_is_never_no_hit(
    discogs, answer
):
    fetch = routed(search=discogs)
    hit = build(fetch)(ARTIST, TITLE)
    assert said(hit) == [(searchers.DISCOGS, answer), (searchers.BEATPORT, "miss")]
    assert hit.genre is None and hit.source == ""
    assert hit.unread == (searchers.DISCOGS,)


def test_an_unread_discogs_goes_on_to_beatport_which_decides():
    fetch = routed(search=CHALLENGE, beatport=beatport_row())
    hit = build(fetch)(ARTIST, TITLE)
    assert (hit.source, hit.genre) == (searchers.BEATPORT, beatport_tag())
    assert hit.unread == (searchers.DISCOGS,)


def test_a_refused_beatport_beside_a_discogs_match_tags_the_file():
    """U281's outcome: Beatport stopped after three refusals, and Discogs still decides."""
    refusals = searchers.Refusals()
    seen: list[str] = []
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=CHALLENGE, seen=seen
    )
    for _ in range(searchers.REFUSALS_BEFORE_STOP):
        # Three files Discogs misses, each refused by Beatport.
        build(routed(search=results(), beatport=CHALLENGE, seen=seen), refusals=refusals)(
            ARTIST, TITLE
        )
    assert beatport_asked(seen) == searchers.REFUSALS_BEFORE_STOP
    hit = build(fetch, refusals=refusals)(ARTIST, TITLE)
    assert (hit.source, hit.genre) == (searchers.DISCOGS, discogs_tag("Deep House"))
    assert beatport_asked(seen) == searchers.REFUSALS_BEFORE_STOP


def test_both_unread_still_refuse_as_unreadable():
    with pytest.raises(Exception) as caught:
        build(routed(search=CHALLENGE, beatport=CHALLENGE))(ARTIST, TITLE)
    assert getattr(caught.value, "cause", None) is not None
    assert caught.value.cause.reason == searchers.UNREACHABLE_REASON


def test_an_explicit_walk_naming_beatport_first_is_honoured():
    seen: list[str] = []
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=beatport_row(), seen=seen
    )
    hit = build(fetch, walk=(searchers.BEATPORT, searchers.DISCOGS))(ARTIST, TITLE)
    assert hit.source == searchers.BEATPORT
    assert said(hit) == [(searchers.BEATPORT, "matched"), (searchers.DISCOGS, searchers.NOT_ASKED)]
    assert not any(url.startswith(searchers.DISCOGS_API) for url in seen)
    assert hit.ask_picture is None


# ---------------------------------------------------------------------------
# B. The picture's ask, which only a file missing one spends
# ---------------------------------------------------------------------------


def test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked():
    seen: list[str] = []
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=beatport_row(), seen=seen
    )
    hit = build(fetch)(ARTIST, TITLE)
    assert hit.ask_picture is not None
    assert (hit.art_url, hit.art_source) == ("", "")
    note = answer_of(hit, searchers.BEATPORT).note
    assert note.startswith(searchers.NOT_SENT) and "picture" in note
    assert beatport_asked(seen) == 0

    pictured = hit.ask_picture(hit)
    assert beatport_asked(seen) == 1
    assert pictured.genre == hit.genre and pictured.source == searchers.DISCOGS
    assert (pictured.art_url, pictured.art_source) == (beatport_row_art(), searchers.BEATPORT)
    beatport = answer_of(pictured, searchers.BEATPORT)
    assert (beatport.answer, beatport.source_genre) == ("matched", BUCKET_GENRE)
    assert pictured.unread == ()


def test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread():
    fetch = routed(search=results(7), releases=matching_release("Deep House"))
    hit = build(fetch)(ARTIST, TITLE)
    pictured = hit.ask_picture(hit)
    assert answer_of(pictured, searchers.BEATPORT).answer == "miss"
    assert (pictured.art_url, pictured.art_source, pictured.unread) == ("", "", ())


def test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop():
    refusals = searchers.Refusals()
    seen: list[str] = []
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=CHALLENGE, seen=seen
    )
    for _ in range(searchers.REFUSALS_BEFORE_STOP):
        hit = build(fetch, refusals=refusals)(ARTIST, TITLE)
        pictured = hit.ask_picture(hit)
        assert answer_of(pictured, searchers.BEATPORT).answer == "blocked"
        assert pictured.unread == (searchers.BEATPORT,)
        assert pictured.genre == discogs_tag("Deep House")
    assert beatport_asked(seen) == searchers.REFUSALS_BEFORE_STOP
    hit = build(fetch, refusals=refusals)(ARTIST, TITLE)
    pictured = hit.ask_picture(hit)
    assert beatport_asked(seen) == searchers.REFUSALS_BEFORE_STOP, "stopped, not sent"
    assert answer_of(pictured, searchers.BEATPORT).note.startswith(searchers.NOT_SENT)
    assert pictured.unread == (searchers.BEATPORT,)


def test_a_record_shop_decline_still_ends_an_explicit_walk():
    """Only a source that names no picture gives way on a decline. A record
    shop's decline is its own word for the track and carries its row's
    picture, so on a walk naming Beatport first it settles the file as before
    and Discogs is not asked."""
    seen: list[str] = []
    fetch = routed(
        search=results(7),
        releases=matching_release("Deep House"),
        beatport=beatport_row(FALLBACK_GENRE),
        seen=seen,
    )
    hit = build(fetch, walk=(searchers.BEATPORT, searchers.DISCOGS))(ARTIST, TITLE)
    assert hit.genre is None
    assert (hit.source, hit.source_genre) == (searchers.BEATPORT, FALLBACK_GENRE)
    assert (hit.art_url, hit.art_source) == (beatport_row_art(), None)
    assert hit.ask_picture is None
    assert not any(url.startswith(searchers.DISCOGS_API) for url in seen)


# ---------------------------------------------------------------------------
# C. Through tag_one: the cover arrives, and only where it is missing
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


def a_file(folder: Path, silence: Path, *, genre: str | None = None, picture: bool = False) -> Path:
    from tests.test_tagging_engine import _jpeg, place, plant

    path = place(folder, silence, TITLE, genre=genre)
    assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE})
    if picture:
        plant(path, _jpeg(320, 200), dims=(320, 200, 24))
    return path


class Images:
    """An image fetch that records each address and answers one picture."""

    def __init__(self) -> None:
        self.asked: list[str] = []

    def __call__(self, url: str) -> bytes:
        from tests.test_tagging_engine import _jpeg

        self.asked.append(url)
        return _jpeg(1000, 1000)


def test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover(tmp_path, silence):
    seen: list[str] = []
    path = a_file(tmp_path, silence)
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=beatport_row(), seen=seen
    )
    images = Images()
    result = tag.tag_one(path, searcher=build(fetch), fetch_image=images)
    assert result.genre_written == discogs_tag("Deep House")
    assert tags.read_genre_from_file(path) == discogs_tag("Deep House")
    assert result.source == searchers.DISCOGS
    assert result.art_fetch == tag.ART_EMBEDDED
    assert searchers.BEATPORT in result.art_fetch_detail
    assert images.asked == [beatport_row_art()]
    assert beatport_asked(seen) == 1
    assert [(one.source, one.answer) for one in result.answers] == [
        (searchers.DISCOGS, "matched"),
        (searchers.BEATPORT, "matched"),
    ]


def test_a_file_discogs_tagged_that_has_a_picture_sends_beatport_nothing(tmp_path, silence):
    seen: list[str] = []
    path = a_file(tmp_path, silence, picture=True)
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=beatport_row(), seen=seen
    )
    images = Images()
    result = tag.tag_one(path, searcher=build(fetch), fetch_image=images)
    assert result.genre_written == discogs_tag("Deep House")
    assert result.art_fetch == tag.ART_PRESENT
    assert beatport_asked(seen) == 0 and images.asked == []
    beatport = [one for one in result.answers if one.source == searchers.BEATPORT]
    assert [one.answer for one in beatport] == [searchers.NOT_ASKED]


def test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover(tmp_path, silence):
    seen: list[str] = []
    path = a_file(tmp_path, silence, genre="Somebody's Own Word")
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=beatport_row(), seen=seen
    )
    images = Images()
    result = tag.tag_one(path, searcher=build(fetch), fetch_image=images)
    assert result.skipped == tag.HAS_GENRE and result.genre_written is None
    assert tags.read_genre_from_file(path) == "Somebody's Own Word", "never re-tagged"
    assert result.art_fetch == tag.ART_EMBEDDED
    assert beatport_asked(seen) == 1


def test_a_tagged_file_with_a_picture_is_never_searched(tmp_path, silence):
    seen: list[str] = []
    path = a_file(tmp_path, silence, genre="Somebody's Own Word", picture=True)
    fetch = routed(search=results(7), releases=matching_release("Deep House"), seen=seen)
    result = tag.tag_one(path, searcher=build(fetch), fetch_image=Images())
    assert result.skipped == tag.HAS_GENRE
    assert seen == []
    assert tags.read_genre_from_file(path) == "Somebody's Own Word"


def test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread(tmp_path, silence):
    path = a_file(tmp_path, silence)
    fetch = routed(search=results(7), releases=matching_release("Deep House"), beatport=CHALLENGE)
    images = Images()
    result = tag.tag_one(path, searcher=build(fetch), fetch_image=images)
    assert result.genre_written == discogs_tag("Deep House")
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert "beatport went unread" in result.art_fetch_detail
    assert "discogs answered about the genre" in result.art_fetch_detail
    assert result.unread == (searchers.BEATPORT,)
    assert images.asked == []


def test_a_picture_ask_that_raises_never_fails_the_file(tmp_path, silence):
    path = a_file(tmp_path, silence)
    fetch = routed(search=results(7), releases=matching_release("Deep House"))

    def exploding(hit: SearchHit) -> SearchHit:
        raise RuntimeError("the picture seam fell over")

    real = build(fetch)

    def searcher(artist: str, title: str) -> SearchHit | None:
        from dataclasses import replace

        return replace(real(artist, title), ask_picture=exploding)

    result = tag.tag_one(path, searcher=searcher, fetch_image=Images())
    assert result.genre_written == discogs_tag("Deep House")
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert "fell over" in result.art_fetch_detail


def test_tag_suggest_sends_beatport_nothing_after_a_discogs_match():
    from cratekit.tagging import suggest

    seen: list[str] = []
    fetch = routed(
        search=results(7), releases=matching_release("Deep House"), beatport=beatport_row(), seen=seen
    )
    asked = suggest.catalogue_lookup(build(fetch))(ARTIST, TITLE, "")
    assert asked.source_genre == "Deep House"
    assert beatport_asked(seen) == 0


# ---------------------------------------------------------------------------
# D. A rejected token waits for the record shops (round one's finding)
# ---------------------------------------------------------------------------


def test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover():
    seen: list[str] = []
    fetch = routed(search=results(7), releases=matching_release("Deep House"),
                   beatport=beatport_row(), seen=seen)
    hit = build(fetch, token="two words")(ARTIST, TITLE)
    assert (hit.source, hit.genre) == (searchers.BEATPORT, beatport_tag())
    assert hit.art_url == beatport_row_art()
    discogs = answer_of(hit, searchers.DISCOGS)
    assert discogs.answer == searchers.NOT_ASKED
    assert discogs.note.startswith(searchers.NOT_SENT) and "printable word" in discogs.note
    assert discogs.note not in searchers.DISCOGS_UNASKED_NOTES, "not counted as no token"
    assert not any(url.startswith(searchers.DISCOGS_API) for url in seen)


def test_a_token_refused_beside_a_beatport_miss_is_still_the_runs_refusal():
    with pytest.raises(CratekitError) as raised:
        build(routed(search=results()), token="two words")(ARTIST, TITLE)
    assert raised.value.cause.reason == "credential-missing"
    assert isinstance(raised.value.__cause__, secrets.CredentialRejected)


def test_a_token_refused_beside_a_refused_beatport_is_still_the_runs_refusal():
    with pytest.raises(CratekitError) as raised:
        build(routed(search=results(), beatport=CHALLENGE), token="two words")(ARTIST, TITLE)
    assert raised.value.cause.reason == "credential-missing"


def test_a_401_is_sent_once_and_beatport_decides_every_file():
    seen: list[str] = []
    fetch = routed(
        search=searchers.Fetched(note="HTTP 401", status=401), beatport=beatport_row(), seen=seen
    )
    searcher = build(fetch)
    for _ in range(3):
        hit = searcher(ARTIST, TITLE)
        assert (hit.source, hit.genre) == (searchers.BEATPORT, beatport_tag())
        assert answer_of(hit, searchers.DISCOGS).note.startswith(searchers.NOT_SENT)
    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 1
    assert beatport_asked(seen) == 3


def test_a_tagged_file_still_gets_its_cover_when_the_token_is_refused(tmp_path, silence):
    path = a_file(tmp_path, silence, genre="Somebody's Own Word")
    fetch = routed(search=results(7), releases=matching_release("Deep House"),
                   beatport=beatport_row())
    result = tag.tag_one(path, searcher=build(fetch, token="two words"), fetch_image=Images())
    assert result.skipped == tag.HAS_GENRE
    assert result.art_fetch == tag.ART_EMBEDDED
    assert tags.read_genre_from_file(path) == "Somebody's Own Word"


def test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises():
    fetch = routed(search=results(), beatport=beatport_row(FALLBACK_GENRE))
    hit = build(fetch, token="two words")(ARTIST, TITLE)
    assert hit.genre is None
    assert (hit.source, hit.source_genre) == (searchers.BEATPORT, FALLBACK_GENRE)
    assert answer_of(hit, searchers.DISCOGS).note.startswith(searchers.DISCOGS_TOKEN_REFUSED)


def test_only_a_refused_token_is_held_and_any_other_refusal_from_discogs_propagates():
    """The asker raises nothing else today; a refusal of another kind is not a
    token's, and holding it would hide it behind Beatport's answer."""

    class Broken:
        def ask(self, artist, title):
            raise refuse("internal-error", "the asker broke", remedy=Remedy.REPORT_DEFECT)

    fetch = routed(search=results(), beatport=beatport_row())
    searcher = searchers.catalogue_searcher(
        TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=Broken()
    )
    with pytest.raises(CratekitError) as raised:
        searcher(ARTIST, TITLE)
    assert raised.value.cause.reason == "internal-error"


def test_the_no_token_count_leaves_out_files_whose_genre_was_their_own_or_their_labels(
    monkeypatch,
):
    """Discogs is asked first, so with no token it is not-asked on every file
    searched; only a file whose genre was owed to a catalogue is counted."""
    from cratekit.tagging import artifacts
    from cratekit.tagging import cli as tag_cli

    def record(**fields):
        return {
            "item": fields.pop("item"),
            "answers": [
                {"source": searchers.DISCOGS, "answer": searchers.NOT_ASKED,
                 "note": searchers.DISCOGS_NO_TOKEN},
                {"source": searchers.BEATPORT, "answer": "matched"},
            ],
            **fields,
        }

    reports = [
        record(item="owed.flac", genre_written="House", source=searchers.BEATPORT),
        record(item="own.flac", skipped=tag.HAS_GENRE),
        record(item="label.flac", genre_written="House", source=tag.LABEL_GENRE),
    ]
    monkeypatch.setattr(artifacts, "committed", lambda cfg, job_id: iter(reports))
    summary = tag_cli._summary(None, "job")
    assert summary["discogs_without_token"] == 1
    assert summary["discogs_token_refused"] == 0
