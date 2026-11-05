"""U207: many ISRCs are screened in a few requests, and a track found is never fetched again.

The catalogue API takes up to twenty ISRCs in one request and answers ONE TRACK
PER CODE when it is given several (``docs/solutions``, the entry on the multi
ISRC filter), so a batch never answers a lookup: it says only which codes the
catalogue files anything under. These claims are the brief's test scenarios,
each counted through the real pacing gate on a temporary state file, so a
request count is read off what the gate counted and never off a counter the
test kept:

1. **An ISRC with five releases costs one read**, the names read off
   ``included``, and no track is fetched again.
2. **Codes the catalogue files nothing under cost a batch, not a request
   each**: fifty such codes cost three, before and after on one fixture, and a
   held code is still asked alone so every release comes back.
3. **A code absent from a batch answer is not found and the others are
   answered.**
4. **A malformed code, or one not spelled as its own fold, never enters a
   batch**, and a lone code is never screened.
5. **A batch that fails marks nothing**: a 5xx falls back to each code's own
   lookup, where the one bad answer is refused alone; a 429 is counted, marks
   nothing and stops the screening; a rejected credential stops it; the
   gate's own park passes through.
6. **An answer the screen cannot attribute marks nothing absent**: a track
   with no ISRC, a code nobody asked, a page that says there is more.
7. **Without the app client nothing is screened**, and every lookup is asked
   as before.
8. **``sync pair``, the mirror and ``intake missing`` screen before they ask.**
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from cratekit.acquire import catalogue_api, isrc_screen, match
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.provider_gate import APP, Gate, GateSettings
from cratekit.intake import missing_cli
from cratekit.label import tidal_catalogue
from cratekit.modules.outbound import mirror, tidal_account
from tests import outbound_fakes
from tests.label_fakes import FakeCatalogue

#: Every code here is in a registrant range nobody holds (D1).
TOKEN_ANSWER = {"access_token": "FAKE-token", "token_type": "Bearer", "expires_in": 86400}


def code(n: int) -> str:
    return f"GBAAA24{n:05d}"


# ═══════════════════════════════════════════════════════════════════════════
# The catalogue API, as its published document says it answers
# ═══════════════════════════════════════════════════════════════════════════


class Answer:
    def __init__(self, status_code: int = 200, body: Any = None) -> None:
        self.status_code = status_code
        self.headers: dict[str, str] = {}
        self._body = body

    def json(self) -> Any:
        return self._body


def track(track_id: str, isrc: Any, title: str = "Sun Path") -> dict:
    return {
        "id": track_id,
        "type": "tracks",
        "attributes": {"title": title, "isrc": isrc, "availability": ["STREAM"]},
        "relationships": {
            "artists": {"data": [{"id": "a1", "type": "artists"}]},
            "albums": {"data": [{"id": f"r{track_id}", "type": "albums"}]},
        },
    }


def included(tracks: list[dict]) -> list[dict]:
    return [{"id": "a1", "type": "artists", "attributes": {"name": "Aurora Bloom"}}] + [
        {"id": f"r{one['id']}", "type": "albums", "attributes": {"title": f"Release {one['id']}"}}
        for one in tracks
    ]


class Api:
    """``openapi.tidal.com/v2`` over a catalogue of ``held`` codes to release ids.

    One code is answered with every release it is filed under, several with ONE
    release each and no pagination, which is what the platform's document says.
    ``batch`` and ``single`` replace the answer to a batch, or to one code asked
    alone, with a status or a body; ``sent`` records every request.
    """

    def __init__(self, held: dict[str, list[str]]) -> None:
        self.held = held
        self.batch: list[Any] = []
        self.single: dict[str, Any] = {}
        self.sent: list[dict[str, Any]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        self.sent.append({"method": method, "url": url, **kwargs})
        if url == catalogue_api.TOKEN_URL:
            return Answer(200, TOKEN_ANSWER)
        asked = kwargs["params"]["filter[isrc]"]
        if isinstance(asked, list):
            if self.batch:
                return self._said(self.batch.pop(0))
            tracks = [track(self.held[one][0], one) for one in asked if self.held.get(one)]
        else:
            if asked in self.single:
                return self._said(self.single[asked])
            tracks = [track(rid, asked) for rid in self.held.get(asked, [])]
        return Answer(200, {"data": tracks, "included": included(tracks), "links": {}})

    @staticmethod
    def _said(said: Any) -> Any:
        if isinstance(said, BaseException):
            raise said
        return Answer(said) if isinstance(said, int) else Answer(200, said)

    def reads(self) -> list[dict[str, Any]]:
        return [one for one in self.sent if one["url"] != catalogue_api.TOKEN_URL]

    def batches(self) -> list[list[str]]:
        return [
            one["params"]["filter[isrc]"]
            for one in self.reads()
            if isinstance(one["params"]["filter[isrc]"], list)
        ]

    def singles(self) -> list[str]:
        return [
            one["params"]["filter[isrc]"]
            for one in self.reads()
            if not isinstance(one["params"]["filter[isrc]"], list)
        ]


@pytest.fixture
def gate(tmp_path: Path) -> Gate:
    return Gate(
        GateSettings(min_interval_s=0.0, cooldown_s=900.0),
        path=tmp_path / "gate" / "provider_gate.json",
        lock_path=tmp_path / "gate" / "provider_gate.lock",
        sleep=lambda seconds: None,
    )


@pytest.fixture(autouse=True)
def no_ladder_sleep(monkeypatch):
    monkeypatch.setattr(tidal_catalogue, "_pause", lambda seconds: None)


def no_sleep(seconds: float) -> None:
    del seconds


class Account:
    """The account session: every lookup it would answer is a failure here,
    so a test reading the app's answers proves the account was never asked."""

    country_code = "GB"

    def get_tracks_by_isrc(self, isrc: str) -> Any:
        raise AssertionError(f"the account was asked about {isrc}")


def app_on(gate: Gate, api: Api) -> catalogue_api.AppCatalogue:
    client = catalogue_api.AppCatalogue("FAKE-app-identifier", "FAKE-app-value", "GB", transport=api)
    assert gate.attach(client, identity=APP) is True
    return client


def adapter(gate: Gate, api: Api) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(Account(), sleep=no_sleep, catalogue=app_on(gate, api))


def app_reads(gate: Gate) -> int:
    """Every call the gate counted under the app, less the one token request."""
    return gate.spend().app_calls - 1


def held_and_lacking(held: int, lacking: int, *, releases: int = 1) -> dict[str, list[str]]:
    catalogue = {code(n): [f"{n}{r}" for r in range(releases)] for n in range(held)}
    catalogue.update({code(n): [] for n in range(held, held + lacking)})
    return catalogue


# ═══════════════════════════════════════════════════════════════════════════
# 1. A track found is never fetched a second time
# ═══════════════════════════════════════════════════════════════════════════


def test_an_isrc_filed_under_five_releases_costs_one_read_and_no_track_is_read_again(gate):
    api = Api({code(1): ["11", "12", "13", "14", "15"]})
    account = adapter(gate, api)

    found = account.match_track(identity="row-1", isrc=code(1))

    # Five releases and no row to choose among them by: _among refuses having
    # been handed every one of them off the one answer.
    assert found is None
    assert "names 5 provider tracks" in account.unmatched_reason("row-1")
    assert app_reads(gate) == 1
    assert api.singles() == [code(1)]
    assert [one["url"] for one in api.reads()] == [catalogue_api.API_ROOT + "tracks"]


# ═══════════════════════════════════════════════════════════════════════════
# 2. Codes the catalogue files nothing under cost a batch, not a request each
# ═══════════════════════════════════════════════════════════════════════════


def ask_every(account: tidal_account.TidalAccount, codes: list[str]) -> dict[str, str | None]:
    return {one: account.match_track(identity=one, isrc=one) for one in codes}


def test_fifty_codes_the_catalogue_files_nothing_under_cost_three_requests_not_fifty(tmp_path):
    codes = [code(n) for n in range(50)]
    catalogue = held_and_lacking(0, 50)
    before_gate = Gate(GateSettings(min_interval_s=0.0), path=tmp_path / "before.json",
                       lock_path=tmp_path / "before.lock", sleep=no_sleep)
    after_gate = Gate(GateSettings(min_interval_s=0.0), path=tmp_path / "after.json",
                      lock_path=tmp_path / "after.lock", sleep=no_sleep)

    before = ask_every(adapter(before_gate, Api(catalogue)), codes)
    screened = adapter(after_gate, api := Api(catalogue))
    made = screened.screen_isrcs(codes)
    after = ask_every(screened, codes)

    assert before == after == dict.fromkeys(codes)
    # Before: one request a code. After: one a batch of twenty, the last of ten.
    assert app_reads(before_gate) == 50
    assert app_reads(after_gate) == made == 3
    assert [len(one) for one in api.batches()] == [20, 20, 10]
    assert api.singles() == []


def test_a_held_code_is_still_asked_alone_so_every_release_comes_back(gate):
    # Five codes held, each filed under three releases; fifteen lacking.
    catalogue = held_and_lacking(5, 15, releases=3)
    codes = list(catalogue)
    account = adapter(gate, api := Api(catalogue))

    assert account.screen_isrcs(codes) == 1
    ask_every(account, codes)

    # One batch, then one lookup per held code: six requests where twenty were.
    assert app_reads(gate) == 6
    assert api.singles() == codes[:5]
    for one in codes[:5]:
        assert "names 3 provider tracks" in account.unmatched_reason(one)


def test_a_code_absent_from_a_batch_answer_is_not_found_and_the_others_are_answered(gate):
    api = Api({code(1): ["101"], code(2): [], code(3): ["301"]})
    account = adapter(gate, api)

    account.screen_isrcs([code(1), code(2), code(3)])

    assert account.match_track(identity="a", isrc=code(1)) == "101"
    assert account.match_track(identity="b", isrc=code(2)) is None
    assert account.unmatched_reason("b") == ""
    assert account.match_track(identity="c", isrc=code(3)) == "301"
    assert api.singles() == [code(1), code(3)]


def test_a_batch_asks_every_code_by_name_in_the_accounts_country_and_nothing_else(gate):
    api = Api(held_and_lacking(1, 1))
    account = adapter(gate, api)

    account.screen_isrcs([code(0), code(1)])

    (sent,) = api.reads()
    assert sent["method"] == "GET"
    assert sent["url"] == catalogue_api.API_ROOT + "tracks"
    assert sent["params"] == {"filter[isrc]": [code(0), code(1)], "countryCode": "GB"}


def test_a_code_already_screened_is_not_sent_again(gate):
    api = Api(held_and_lacking(0, 4))
    account = adapter(gate, api)

    assert account.screen_isrcs([code(0), code(1)]) == 1
    assert account.screen_isrcs([code(1), code(0)]) == 0
    assert account.screen_isrcs([code(0), code(2), code(3)]) == 1

    assert api.batches() == [[code(0), code(1)], [code(2), code(3)]]


# ═══════════════════════════════════════════════════════════════════════════
# 3. What never enters a batch
# ═══════════════════════════════════════════════════════════════════════════


def test_a_malformed_code_or_a_spelling_not_its_own_fold_never_enters_a_batch(gate):
    api = Api(held_and_lacking(0, 3))
    account = adapter(gate, api)
    lower = code(2).lower()

    made = account.screen_isrcs(["not-an-isrc", "", lower, code(0), code(1), code(0)])

    assert made == 1
    assert api.batches() == [[code(0), code(1)]]
    # The lowercase spelling was never screened, so it is asked as it was given.
    account.match_track(identity="x", isrc=lower)
    assert api.singles() == [lower]


def test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same(gate):
    api = Api(held_and_lacking(0, 21))
    account = adapter(gate, api)

    assert account.screen_isrcs([code(0)]) == 0
    assert account.screen_isrcs([code(n) for n in range(1, 22)]) == 1

    assert api.batches() == [[code(n) for n in range(1, 21)]]
    # The one left over after the full batch is asked alone, as is the lone one.
    account.match_track(identity="x", isrc=code(21))
    account.match_track(identity="y", isrc=code(0))
    assert api.singles() == [code(21), code(0)]


def test_the_app_client_refuses_a_batch_it_was_not_built_to_ask(gate):
    app = app_on(gate, Api({}))

    for wrong in ([code(0)], [code(n) for n in range(21)], [code(0), code(0)],
                  [code(0), code(1).lower()], [code(0), "not-an-isrc"]):
        with pytest.raises(ValueError):
            app.isrcs_held(wrong)


# ═══════════════════════════════════════════════════════════════════════════
# 4. A batch that fails marks nothing
# ═══════════════════════════════════════════════════════════════════════════


def test_a_server_error_on_a_batch_falls_back_to_singles_and_finds_the_one_bad_answer(gate):
    catalogue = held_and_lacking(1, 3)
    api = Api(catalogue)
    api.batch = [500]
    api.single = {code(2): 500}
    account = adapter(gate, api)

    assert account.screen_isrcs(list(catalogue)) == 1
    assert account.match_track(identity="a", isrc=code(0)) == "00"
    assert account.match_track(identity="b", isrc=code(1)) is None
    with pytest.raises(CratekitError):
        account.match_track(identity="c", isrc=code(2))
    assert account.match_track(identity="d", isrc=code(3)) is None

    # Nothing was read as absent: every code was asked alone.
    assert [one for one in api.singles() if one != code(2)] == [code(0), code(1), code(3)]


def test_a_failed_batch_does_not_stop_the_next_one(gate):
    catalogue = held_and_lacking(0, 40)
    api = Api(catalogue)
    api.batch = [503]
    account = adapter(gate, api)

    assert account.screen_isrcs(list(catalogue)) == 2

    ask_every(account, list(catalogue))
    assert api.singles() == list(catalogue)[:20]


def test_a_rate_limit_on_a_batch_is_counted_marks_nothing_and_stops_the_screening(gate):
    catalogue = held_and_lacking(0, 60)
    api = Api(catalogue)
    api.batch = [429]
    account = adapter(gate, api)

    assert account.screen_isrcs(list(catalogue)) == 1
    assert gate.spend().app_rate_limited == 1
    assert account.screen_isrcs([code(98), code(99)]) == 0
    assert len(api.batches()) == 1

    ask_every(account, list(catalogue)[:3])
    assert api.singles() == list(catalogue)[:3]


def test_a_rejected_app_credential_on_a_batch_marks_nothing_and_stops_the_screening(gate):
    catalogue = held_and_lacking(0, 40)
    api = Api(catalogue)
    api.batch = [401]
    account = adapter(gate, api)

    assert account.screen_isrcs(list(catalogue)) == 1
    assert account.screen_isrcs([code(98), code(99)]) == 0

    assert account.match_track(identity="a", isrc=code(0)) is None
    assert api.singles() == [code(0)]


def test_the_gates_own_park_passes_through_the_screen(gate):
    api = Api(held_and_lacking(0, 2))
    parked = refuse(
        "unavailable-transient", "the gate is cooling down", remedy=Remedy.RETRY_LATER, origin=("test",)
    )
    api.batch = [parked]
    account = adapter(gate, api)

    with pytest.raises(CratekitError) as raised:
        account.screen_isrcs([code(0), code(1)])
    assert raised.value is parked


# ═══════════════════════════════════════════════════════════════════════════
# 5. An answer the screen cannot attribute marks nothing absent
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "said",
    [
        {"data": [track("1", None)], "included": []},
        {"data": [track("1", "not an isrc")], "included": []},
        {"data": [track("1", code(7))], "included": []},
        {"data": [], "links": {"next": "/tracks?page[cursor]=abc"}},
        {"data": ["not a resource"]},
        {"data": "not a list"},
    ],
    ids=["no-isrc", "unreadable-isrc", "a-code-not-asked", "paged", "not-a-resource", "no-list"],
)
def test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent(gate, said):
    catalogue = held_and_lacking(0, 3)
    api = Api(catalogue)
    api.batch = [said]
    account = adapter(gate, api)

    assert account.screen_isrcs(list(catalogue)) == 1

    ask_every(account, list(catalogue))
    assert api.singles() == list(catalogue)


def test_a_resource_that_is_not_a_track_is_not_read_as_an_answer_about_a_code(gate):
    catalogue = held_and_lacking(1, 1)
    api = Api(catalogue)
    api.batch = [{"data": [track("00", code(0)), {"id": "a1", "type": "artists"}], "included": []}]
    account = adapter(gate, api)

    account.screen_isrcs(list(catalogue))

    ask_every(account, list(catalogue))
    assert api.singles() == [code(0)]


# ═══════════════════════════════════════════════════════════════════════════
# 6. Without the app client nothing is screened
# ═══════════════════════════════════════════════════════════════════════════


class Session:
    """The account's client library: one lookup a code, and no batch form."""

    def __init__(self) -> None:
        self.asked: list[str] = []

    def get_tracks_by_isrc(self, isrc: str) -> list[Any]:
        self.asked.append(isrc)
        return []


def test_without_the_app_client_the_screen_makes_no_request_and_every_lookup_is_asked():
    session = Session()
    account = tidal_account.TidalAccount(session, sleep=no_sleep)

    assert account.screen_isrcs([code(0), code(1), code(2)]) == 0
    account.match_track(identity="a", isrc=code(0))

    assert session.asked == [code(0)]


def test_a_stand_in_for_the_client_is_never_screened_whatever_it_answers():
    class Anything:
        def __getattr__(self, name: str) -> Any:
            return lambda *args, **kwargs: frozenset()

    screen = isrc_screen.Screen()

    assert screen.screen(Anything(), [code(0), code(1)]) == 0
    assert not screen.absent(code(0))


# ═══════════════════════════════════════════════════════════════════════════
# 7. The label catalogue's lookup, which intake missing asks
# ═══════════════════════════════════════════════════════════════════════════


def test_the_catalogue_answers_a_screened_absent_code_as_no_track_with_no_request(gate):
    catalogue = {code(0): ["01", "02"], code(1): [], code(2): []}
    api = Api(catalogue)
    found = tidal_catalogue.TidalCatalogue(Account(), catalogue=app_on(gate, api))

    assert found.screen_isrcs(list(catalogue)) == 1

    assert [one.id for one in found.tracks_for_isrc(code(0))] == ["01", "02"]
    assert found.tracks_for_isrc(code(1)) == ()
    assert found.tracks_for_isrc(code(2)) == ()
    assert api.singles() == [code(0)]
    assert app_reads(gate) == 2


def test_intake_missing_screens_the_codes_it_will_ask_before_asking_any():
    fake = FakeCatalogue(isrcs={code(0): [], code(1): []})
    wanted = [
        match.Wanted(artist="Aurora Bloom", title="Sun Path", isrc=code(0)),
        match.Wanted(artist="Nova Reef", title="Tide", isrc=code(1).lower()),
        match.Wanted(artist="Nova Reef", title="Again", isrc=code(0)),
        match.Wanted(artist="Nova Reef", title="Bad", isrc="not-an-isrc"),
        match.Wanted(artist="Nova Reef", title="None"),
    ]

    missing_cli._named_by_isrc(wanted, resolve=lambda: fake)

    assert fake.screened == [(code(0), code(1))]
    assert fake.isrcs_asked_for == [code(0), code(1)]


# ═══════════════════════════════════════════════════════════════════════════
# 8. The mirror screens the rows it will ask, and counts what the screen spent
# ═══════════════════════════════════════════════════════════════════════════


def row(n: int, *, isrc: str = "") -> mirror.Row:
    return mirror.Row(content_id=f"c{n}", title=f"Title {n}", artist=f"Artist {n}", isrc=isrc)


def test_the_mirror_screens_only_the_rows_it_would_ask_the_provider_about():
    account = outbound_fakes.FakeAccount({})
    identified: list[str] = []

    def identify(one: mirror.Row) -> mirror.Identity:
        identified.append(one.content_id)
        return mirror.Identity(isrc=one.isrc or (code(9) if one.content_id == "c5" else ""))

    matcher = mirror.Matcher(
        account,
        {"c1": ("r1", code(1))},
        identify,
        misses={"c3": ("no match", (code(3), "Title 3", "Artist 3", "", ""))},
        known={"c2": "r2"},
        seen={"c6": ("r6", code(6), "")},
    )
    rows = [
        row(1, isrc=code(1)),  # linked
        row(2, isrc=code(2)),  # its landing recorded its track
        row(3, isrc=code(3)),  # a remembered miss under what it is asked by
        row(4, isrc=code(4)),  # asked
        row(5),  # asked by its file's code
        row(6, isrc=code(6)),  # a frozen plan's answer
        row(7),  # no code anywhere
    ]

    assert matcher.screen(rows) == 0
    assert account.screened == [(code(4), code(9))]

    for one in rows:
        matcher.match(one)
    # The file's code was read once, for the screen and the match together.
    assert identified.count("c5") == 1
    assert [asked["isrc"] for asked in account.matches] == [code(4), code(9)]


def test_the_mirrors_request_count_holds_what_the_screen_spent_and_no_more():
    class Spending(outbound_fakes.FakeAccount):
        def screen_isrcs(self, codes) -> int:
            super().screen_isrcs(codes)
            return 2

    counted = mirror.Counted(Spending({}))
    assert counted.screen_isrcs([code(0), code(1)]) == 2
    assert counted.requests == 2

    nothing = mirror.Counted(outbound_fakes.FakeAccount({}))
    assert nothing.screen_isrcs([code(0), code(1)]) == 0
    assert nothing.requests == 0
