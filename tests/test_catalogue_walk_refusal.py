"""U322: a refusing catalogue no longer stops tag suggest and tag backlog asking the ones that answer.

At sitting 102 a backlog stopped after 10 of 675 rows: a row only Beatport refused read as unread.
"""

from __future__ import annotations

from collections import defaultdict

import pytest

from cratekit.core.cause import refuse
from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import published, searchers, suggest, suggest_cli
from cratekit.tagging.tag import SearchHit, SourceAnswer
from tests import test_tag_suggest as _suggest_suite
from tests.test_beatport_refusal import (
    REFUSED,
    _beatport_requests,
    _discogs_searches,
    _over_the_wire,
    _Response,
)
from tests.test_catalogue_searcher import ARTIST, TITLE
from tests.test_discogs_searcher import SENT

machine = _suggest_suite.machine

TAXONOMY = default_taxonomy()

#: An ISRC per row, so the general catalogue has something to be asked by.
ISRCS = tuple(f"GBAYE00000{n:02d}" for n in range(8))

#: What a refusal by every catalogue asked stops the walk with, as it is now.
STOPPED = (
    f"not asked: the catalogues could not be read for {suggest.STOP_AFTER_UNREAD} rows in a row"
)


class _General:
    """The general catalogue, answering one word for every ISRC it is asked."""

    def __init__(self, answer: str = "miss", genres: tuple[str, ...] = ()):
        self.answer = answer
        self.genres = genres
        self.asked: list[object] = []

    def __call__(self, isrc: object) -> published.Published:
        self.asked.append(isrc)
        return published.Published(published.SOURCE, self.answer, genres=self.genres)


def _walk(beatport=REFUSED, *, discogs=None, token=SENT, general=None, rows=8, suggestions=True):
    """``rows`` rows asked as ``tag suggest --catalogue`` asks them, one searcher a run."""
    seen: list[str] = []
    fetch = _over_the_wire(beatport, discogs=discogs, seen=seen)
    asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    search = searchers.catalogue_searcher(
        TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker)
    if general is None:
        return search, None, seen
    shops = {"lookup": general, "past_a_refusing_shop": suggestions}
    return search, published.second_opinion(TAXONOMY, **shops), seen


def _asked(machine, search, opinion, rows=8, unasked=frozenset()):
    lookup = suggest.catalogue_lookup(search, opinion)
    with suggest.KeptCatalogue(machine, lookup, unasked=unasked) as kept:
        answers = [
            kept.answer(str(n), ARTIST, f"{TITLE} {n}", ISRCS[n % len(ISRCS)]) for n in range(rows)
        ]
    return kept, answers


# A. The defect: a refusing Beatport beside a Discogs that answers
def test_a_discogs_miss_beside_a_refusing_beatport_does_not_stop_the_walk(machine):
    """The card's defect, red on main: the walk stopped at the third row."""
    search, _opinion, seen = _walk()
    kept, answers = _asked(machine, search, None)
    assert not kept.stopped
    assert kept.asked == 8
    assert _discogs_searches(seen) == 8
    # U281's own stop is what passes Beatport over, after its third refusal.
    assert _beatport_requests(seen) == searchers.REFUSALS_BEFORE_STOP
    assert all(STOPPED not in answer.note for answer in answers)


def test_a_row_read_beside_a_refusal_stays_unread_and_askable(machine):
    search, _opinion, _seen = _walk()
    _kept, answers = _asked(machine, search, None, rows=4)
    for answer in answers:
        assert answer.said == suggest.UNREAD
        assert answer.partly_read
        assert answer.note == "unread: beatport"
    words = dict(answers[0].answers)
    assert words == {searchers.DISCOGS: "miss", searchers.BEATPORT: "blocked"}
    # Past U281's stop, Beatport's word says it was never sent.
    assert dict(answers[3].answers)[searchers.BEATPORT] == suggest.NOT_SENT


def test_deezer_is_asked_on_every_row_with_an_isrc_while_beatport_refuses(machine):
    general = _General()
    search, opinion, seen = _walk(general=general)
    kept, answers = _asked(machine, search, opinion)
    assert not kept.stopped
    assert general.asked == list(ISRCS)
    assert _beatport_requests(seen) == searchers.REFUSALS_BEFORE_STOP
    for answer in answers:
        assert dict(answer.answers)[published.SOURCE] == "miss"


def test_a_deezer_genre_past_a_refusing_beatport_is_the_rows_match(machine):
    word, genre = published.choose(TAXONOMY, ["Soul & Funk"])
    general = _General("matched", (word,))
    search, opinion, _seen = _walk(general=general)
    _kept, answers = _asked(machine, search, opinion, rows=2)
    for answer in answers:
        assert (answer.said, answer.genre) == (suggest.MATCHED, genre)
        assert answer.source == published.SOURCE


# B. The walk's stop, which still holds where every catalogue refused
def test_every_catalogue_refusing_three_rows_in_a_row_still_stops_the_walk(machine):
    general = _General()
    search, opinion, seen = _walk(discogs=_Response(403, "", {}), general=general)
    kept, answers = _asked(machine, search, opinion, rows=6)
    assert kept.stopped and kept.asked == suggest.STOP_AFTER_UNREAD
    assert all(answer.said == suggest.UNREAD for answer in answers)
    assert not any(answer.partly_read for answer in answers)
    assert [answer.note for answer in answers[3:]] == [STOPPED] * 3
    assert general.asked == []


def _fake(words: dict[str, str], said: str = suggest.UNREAD, **rest) -> suggest.Asked:
    return suggest.Asked(said, answers=tuple(words.items()), **rest)


REFUSED_ROW = _fake({"discogs": "blocked", "beatport": "blocked"}, note="unread: discogs, beatport")
PARTLY = _fake({"discogs": "miss", "beatport": "blocked"}, note="unread: beatport")
PASSED = _fake(
    {"discogs": searchers.NOT_ASKED, "beatport": "miss"}, note="unread: discogs, no token",
    passed_over=("discogs",))
#: A row passed over because the recorded Discogs token could not be used.
UNUSABLE = suggest.Asked(
    suggest.UNREAD, note=f"unread: discogs, {suggest.TOKEN_UNUSABLE}", passed_over=("discogs",))


class _Table:
    def __init__(self, *answers: suggest.Asked):
        self.answers = list(answers)
        self.asked = 0

    def __call__(self, artist, title, isrc):
        self.asked += 1
        return self.answers.pop(0)


def _run(machine, *answers, walk: str = "w"):
    """One walk over as many rows as ``answers``, each row a title of its own."""
    table = _Table(*answers)
    with suggest.KeptCatalogue(machine, table) as kept:
        said = [kept.answer(f"{walk}{n}", "a", f"{walk}{n}", "") for n in range(len(answers))]
    return kept, table, said


@pytest.mark.parametrize(
    "answers", [(REFUSED_ROW, REFUSED_ROW, PARTLY) * 2, (PARTLY,) * 6],
    ids=["a-partly-read-row-resets-the-run-of-refusals", "partly-read-rows-never-count"])
def test_a_partly_read_row_never_lets_a_run_of_refusals_stop_the_walk(machine, answers):
    kept, table, _said = _run(machine, *answers)
    assert not kept.stopped and table.asked == 6


def test_a_catalogue_nobody_asked_neither_counts_nor_resets(machine):
    """U244: a row unread only by an unasked catalogue does not end a refusal run."""
    kept, table, said = _run(machine, REFUSED_ROW, REFUSED_ROW, PASSED, REFUSED_ROW, PARTLY)
    assert kept.stopped and table.asked == 4
    assert said[4].note == STOPPED
    kept, table, _said = _run(machine, *[PASSED] * 4, walk="passed")
    assert not kept.stopped and table.asked == 4


# C. What a row's answer carries and is kept with
def _refusal(message: str = "refused", **detail):
    """The lookup's answer when every catalogue asked refused with ``detail``."""
    cause = refuse(searchers.UNREACHABLE_REASON, message, origin=("test",), detail=detail)

    def search(artist, title):
        raise cause
    return suggest.catalogue_lookup(search)("a", "t", "")


def test_the_words_of_a_refusal_by_every_catalogue_are_read_off_its_detail():
    answer = _refusal(
        "every catalogue asked refused", sources=["discogs", "beatport"],
        answers=["blocked", "blocked"], notes=["", f"{searchers.NOT_SENT}refused"],
        **{searchers.DISCOGS_DETAIL: ""})
    assert answer.said == suggest.UNREAD and not answer.partly_read
    assert dict(answer.answers) == {"discogs": "blocked", "beatport": suggest.NOT_SENT}


def test_a_refusal_with_no_detail_carries_no_words():
    def search(artist, title):
        raise refuse("catalogue-unreachable", "no network", origin=("test",))
    answer = suggest.catalogue_lookup(search)("a", "t", "")
    assert answer.said == suggest.UNREAD and answer.answers == () and not answer.partly_read


def test_a_kept_answer_keeps_its_words(machine):
    table = _Table(PARTLY)
    with suggest.KeptCatalogue(machine, table) as kept:
        kept.answer("1", "a", "t", "")
    with suggest.KeptCatalogue(machine, table) as kept:
        again = kept.answer("1", "a", "t", "")
    assert again == PARTLY and again.partly_read and table.asked == 1


@pytest.mark.parametrize("said", [suggest.MATCHED, suggest.DECLINED, suggest.UNREAD])
def test_an_answer_kept_before_the_words_is_asked_again_once(machine, said):
    """An answer main kept carries no words, so its Discogs match counts as matched."""
    import json
    from datetime import date
    path = suggest.catalogue_path(machine)
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "for": {"artist": "a", "title": "t", "isrc": ""},
        "on": date.today().isoformat(),
        "answer": {"said": said, "genre": "", "note": ""},
    }
    path.write_text(json.dumps({"1": entry}), encoding="utf-8")
    table = _Table(PARTLY)
    with suggest.KeptCatalogue(machine, table) as kept:
        again = kept.answer("1", "a", "t", "")
    assert again == PARTLY and table.asked == 1
    with suggest.KeptCatalogue(machine, table) as kept:
        assert kept.answer("1", "a", "t", "") == PARTLY and kept.asked == 0


# D. The general catalogue's gate, narrowed for the suggest verbs only
def _hit(*answers: tuple[str, str], unread=()) -> SearchHit:
    said = tuple(SourceAnswer(source, word) for source, word in answers)
    return SearchHit(answers=said, unread=tuple(unread))


def _past_a_refusing_shop(general, hit: SearchHit) -> SearchHit:
    """The suggest verbs' second opinion over ``hit`` for the first ISRC."""
    opinion = published.second_opinion(TAXONOMY, lookup=general, past_a_refusing_shop=True)
    return opinion(hit, ISRCS[0])


def _general_word(hit: SearchHit) -> str:
    (said,) = [one for one in hit.answers if one.source == published.SOURCE]
    return said.answer


@pytest.mark.parametrize("discogs", ["miss", "matched"])
def test_the_suggest_binder_asks_deezer_past_a_refusing_beatport_once_discogs_answered(discogs):
    general = _General()
    hit = _hit(("discogs", discogs), ("beatport", "blocked"), unread=("beatport",))
    decided = _past_a_refusing_shop(general, hit)
    assert general.asked == [ISRCS[0]] and _general_word(decided) == "miss"
    assert decided.unread == ("beatport",)


@pytest.mark.parametrize("discogs", ["blocked", "unreachable", "parse-break", searchers.NOT_ASKED])
def test_deezer_still_waits_for_a_discogs_that_did_not_answer(discogs):
    general = _General()
    hit = _hit(("discogs", discogs), ("beatport", "blocked"), unread=("beatport", "discogs"))
    decided = _past_a_refusing_shop(general, hit)
    assert general.asked == [] and _general_word(decided) == searchers.NOT_ASKED


@pytest.mark.parametrize("beatport", ["unreachable", "parse-break", searchers.NOT_ASKED])
def test_deezer_still_waits_for_a_beatport_that_is_down_rather_than_refusing(beatport):
    general = _General()
    hit = _hit(("discogs", "miss"), ("beatport", beatport), unread=("beatport",))
    _past_a_refusing_shop(general, hit)
    assert general.asked == []


def test_tag_folders_gate_is_unchanged():
    general = _General()
    hit = _hit(("discogs", "miss"), ("beatport", "blocked"), unread=("beatport",))
    decided = published.second_opinion(TAXONOMY, lookup=general)(hit, ISRCS[0])
    assert general.asked == [] and _general_word(decided) == searchers.NOT_ASKED
    decided = published.for_taxonomy(TAXONOMY)(hit, ISRCS[0])
    assert _general_word(decided) == searchers.NOT_ASKED


def test_the_suggest_binder_is_built_over_the_one_lookup(monkeypatch):
    general = _General()
    monkeypatch.setattr(published, "for_lookup", lambda: general)
    hit = _hit(("discogs", "miss"), ("beatport", "blocked"), unread=("beatport",))
    published.for_suggestions(TAXONOMY)(hit, ISRCS[1])
    assert general.asked == [ISRCS[1]]


# E. What the two verbs say
def _item(content_id: str, asked: suggest.Asked) -> suggest.Item:
    return suggest.Item(
        content_id=content_id, path="", artist="a", title="t", genre="", band="", options=(),
        votes=(), catalogue=asked, action="leave")


def _plan(*items: suggest.Item) -> suggest.SuggestPlan:
    return suggest.SuggestPlan(
        items=items, counts=defaultdict(int), changes=None, band="", catalogue=True)


def _unread_warning(*items: suggest.Item) -> str:
    """The one catalogue unread advisory ``tag suggest`` gives over these rows."""
    advisories = suggest_cli._advisories(_plan(*items))
    (warning,) = [w for w in advisories if w["code"] == suggest_cli.CATALOGUE_UNREAD]
    return warning["message"]


def test_tag_suggest_says_a_partly_read_row_apart_from_one_nobody_could_read():
    message = _unread_warning(_item("1", REFUSED_ROW), _item("2", PARTLY), _item("3", PARTLY))
    assert "the catalogues could not be read for 1 row(s), 1," in message
    assert "beatport could not be read for 2 row(s) another catalogue answered, 2, 3," in message


_COUNTED = ("asked", "matched", "missed", "unread", "not_asked", "not_sent")


def test_the_backlogs_catalogue_line_counts_each_catalogues_answers():
    answers = [
        _fake({"discogs": "matched", "beatport": searchers.NOT_ASKED}, said=suggest.MATCHED),
        PARTLY,
        _fake({"discogs": "miss", "beatport": suggest.NOT_SENT, "deezer": "miss"}),
        REFUSED_ROW,
        suggest.Asked(suggest.UNREAD, note=STOPPED),
        PASSED,
    ]
    counted = suggest.catalogue_counts(answers)
    assert counted["rows"] == 6 and counted["stopped"] == 1
    assert counted["catalogues"] == {
        name: dict(zip(_COUNTED, counts))
        for name, counts in (
            ("discogs", (4, 1, 2, 1, 2, 0)),
            ("beatport", (3, 0, 1, 2, 3, 1)),
            ("deezer", (1, 0, 1, 0, 5, 0)),
        )
    }


# F. Round one of the review
DEEZER_MATCH = _fake(
    {"discogs": "miss", "beatport": "blocked", "deezer": "matched"}, said=suggest.MATCHED,
    genre="Soul", source="deezer")


def test_a_row_written_from_deezer_while_beatport_refused_is_named_in_the_warning():
    """A Deezer genre past a refusing Beatport is suggested with Beatport named."""
    message = _unread_warning(_item("1", DEEZER_MATCH), _item("2", REFUSED_ROW))
    assert "beatport could not be read for 1 row(s) another catalogue answered, 1," in message
    assert "the catalogues could not be read for 1 row(s), 2," in message


def test_rows_are_sorted_by_why_they_were_not_read_whole():
    declined = _fake({"discogs": "matched", "beatport": suggest.NOT_SENT}, said=suggest.DECLINED)
    clean = _fake({"discogs": "matched"}, said=suggest.MATCHED)
    rows = (REFUSED_ROW, PARTLY, DEEZER_MATCH, declined, clean, PASSED, UNUSABLE)
    unread = suggest.sort_unread([(str(n), row) for n, row in enumerate(rows, start=1)])
    assert unread == suggest.Unread(
        refused=("1",), partly=("2", "3", "4"), partly_by="beatport", no_token=("6",),
        token_unusable=("7",))


def test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk(machine):
    """A token Discogs refused does not stop a walk Beatport answered."""
    from tests.test_beatport_refusal import MISSED
    search, _opinion, seen = _walk(MISSED, discogs=_Response(401, "{}", {}))
    kept, answers = _asked(machine, search, None)
    assert not kept.stopped and kept.asked == 8
    assert _beatport_requests(seen) == 8
    for answer in answers:
        assert answer.passed_over == (searchers.DISCOGS,)
        assert answer.answers == ((searchers.DISCOGS, searchers.NOT_ASKED),)
        # One note on every row, since the note is in the plan's digest.
        assert answer.note == f"unread: discogs, {suggest.TOKEN_UNUSABLE}"
    unread = suggest.sort_unread((str(n), a) for n, a in enumerate(answers))
    assert unread.token_unusable == tuple(str(n) for n in range(8)) and not unread.refused


def test_a_rejected_token_beside_a_refusing_beatport_sends_beatport_nothing_past_its_stop(machine):
    search, _opinion, seen = _walk(REFUSED, discogs=_Response(401, "{}", {}))
    _kept, _answers = _asked(machine, search, None)
    assert _beatport_requests(seen) == searchers.REFUSALS_BEFORE_STOP
    assert _discogs_searches(seen) == 1


#: A partly read row whose Beatport request was sent and refused, and one never sent.
SENT_ROW = _fake({"discogs": "miss", "beatport": "blocked"}, note="unread: beatport")
NOT_SENT_ROW = _fake({"discogs": "miss", "beatport": suggest.NOT_SENT}, note="unread: beatport")
_NOT_SENT_WORDS = [["discogs", "miss"], ["beatport", suggest.NOT_SENT]]


def test_the_words_are_left_out_of_a_plans_digest():
    """Which refusing rows were sent is not in the digest, or a plan goes stale overnight."""
    def digest(asked):
        return _plan(_item("1", asked)).digest
    assert digest(SENT_ROW) == digest(NOT_SENT_ROW)
    assert digest(SENT_ROW) != digest(REFUSED_ROW)
    assert _item("1", NOT_SENT_ROW).to_json()["catalogue"]["answers"] == _NOT_SENT_WORDS


def test_a_discogs_passed_over_beside_a_refusal_is_named_among_the_words():
    passed = {searchers.DISCOGS_DETAIL: searchers.DISCOGS_NO_TOKEN}
    answer = _refusal(sources=["beatport"], answers=["blocked"], notes=[""], **passed)
    assert answer.answers == (("discogs", searchers.NOT_ASKED), ("beatport", "blocked"))


def test_a_refusals_detail_of_the_wrong_shape_carries_no_words():
    assert _refusal(sources=["beatport", "discogs"], answers=["blocked"]).answers == ()
    assert _refusal(sources="beatport", answers=["blocked"]).answers == ()
    # Notes of another length are read as none, so no refusal reads as unsent.
    unsent = [f"{searchers.NOT_SENT}x", "y"]
    notes = _refusal(sources=["beatport"], answers=["blocked"], notes=unsent)
    assert notes.answers == (("beatport", "blocked"),)


def test_a_declined_and_a_passed_over_row_carry_their_words():
    said = (SourceAnswer("discogs", "matched"), SourceAnswer("beatport", "miss"))
    declined = suggest._asked_from(SearchHit(source="discogs", source_genre="Weird", answers=said))
    assert declined.said == suggest.DECLINED
    assert declined.answers == (("discogs", "matched"), ("beatport", "miss"))
    said = (
        SourceAnswer("discogs", searchers.NOT_ASKED, note=searchers.DISCOGS_NO_TOKEN),
        SourceAnswer("beatport", "miss"),
    )
    passed = suggest._asked_from(SearchHit(answers=said, unread=("discogs",)))
    assert passed.passed_over == ("discogs",)
    assert passed.answers == (("discogs", searchers.NOT_ASKED), ("beatport", "miss"))


def test_a_row_passed_over_for_a_refused_token_is_kept_for_the_day(machine):
    """A kept row passed over for the recorded token is not asked again."""
    from tests.test_beatport_refusal import MISSED

    def run():
        search, _opinion, seen = _walk(MISSED, discogs=_Response(401, "{}", {}))
        lookup = suggest.catalogue_lookup(search)
        with suggest.KeptCatalogue(machine, lookup, unasked=frozenset()) as kept:
            for n in range(4):
                kept.answer(str(n), ARTIST, f"{TITLE} {n}", "")
        return kept, seen
    first, seen = run()
    assert first.asked == 4 and _beatport_requests(seen) == 4
    again, seen = run()
    assert again.asked == 0 and seen == []


def test_the_suggest_verb_says_a_token_that_could_not_be_used():
    message = _unread_warning(_item("1", UNUSABLE))
    assert message.startswith(
        "Discogs was not read for 1 row(s), 1, because the recorded Discogs token could "
        "not be used, so those were suggested without it; to record a new one: ")
    assert "no Discogs token is recorded" not in message


def test_a_backlog_rows_digest_leaves_the_words_out_and_its_envelope_keeps_them():
    from cratekit.tagging import backlog

    def row(asked):
        return backlog.Row(
            content_id="1", path="p", artist="a", title="t", row_word="", file_word="",
            cause=backlog.NO_GENRE, word="", status=backlog.LEFT, asked=asked)  # fmt: skip
    assert row(SENT_ROW).digested() == row(NOT_SENT_ROW).digested()
    assert "answers" not in row(SENT_ROW).digested()["catalogue"]
    assert row(NOT_SENT_ROW).to_json()["catalogue"]["answers"] == _NOT_SENT_WORDS
