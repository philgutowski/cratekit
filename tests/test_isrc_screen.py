"""U207: many ISRCs are screened in a few requests, and a track found is never fetched again.

A batch answers one track per code (``docs/solutions``, the multi ISRC filter entry), so it
only says which codes hold anything; a held code is still asked alone, each claim is counted
through the real pacing gate, and a failed batch marks nothing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from cratekit.acquire import catalogue_api, isrc_cache, isrc_screen, match
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


class Answer:
    def __init__(self, status_code: int = 200, body: Any = None) -> None:
        self.status_code = status_code
        self.headers: dict[str, str] = {}
        self._body = body

    def json(self) -> Any:
        return self._body


def track(track_id: str, isrc: Any, title: str = "Sun Path") -> dict:
    return {
        "id": track_id, "type": "tracks",
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
    """``openapi.tidal.com/v2`` over ``held``; ``batch`` and ``single`` replace an answer."""

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
        return [one for one in self._filters() if isinstance(one, list)]

    def singles(self) -> list[str]:
        return [one for one in self._filters() if not isinstance(one, list)]

    def _filters(self) -> list[Any]:
        return [one["params"]["filter[isrc]"] for one in self.reads()]


@pytest.fixture
def gate(tmp_path: Path) -> Gate:
    return Gate(
        GateSettings(min_interval_s=0.0, cooldown_s=900.0),
        path=tmp_path / "gate" / "provider_gate.json",
        lock_path=tmp_path / "gate" / "provider_gate.lock", sleep=lambda seconds: None,
    )


@pytest.fixture(autouse=True)
def no_ladder_sleep(monkeypatch):
    monkeypatch.setattr(tidal_catalogue, "_pause", lambda seconds: None)


def no_sleep(seconds: float) -> None:
    del seconds


class Account:
    """The account session: any lookup fails, so a pass proves the account was never asked."""

    country_code = "GB"

    def get_tracks_by_isrc(self, isrc: str) -> Any:
        raise AssertionError(f"the account was asked about {isrc}")


def app_on(gate: Gate, api: Api) -> catalogue_api.AppCatalogue:
    client = catalogue_api.AppCatalogue("FAKE-app-identifier", "FAKE-app-value", "GB", transport=api)
    assert gate.attach(client, identity=APP) is True
    return client


def adapter(gate: Gate, api: Api) -> tidal_account.TidalAccount:
    """The account over the app client, with the ISRC cache off (U206) so the saving is counted."""
    return tidal_account.TidalAccount(
        Account(), sleep=no_sleep, catalogue=app_on(gate, api), cache=isrc_cache.Cache(days=0)
    )


def app_reads(gate: Gate) -> int:
    """Every call the gate counted under the app, less the one token request."""
    return gate.spend().app_calls - 1


def held_and_lacking(held: int, lacking: int, *, releases: int = 1) -> dict[str, list[str]]:
    catalogue = {code(n): [f"{n}{r}" for r in range(releases)] for n in range(held)}
    catalogue.update({code(n): [] for n in range(held, held + lacking)})
    return catalogue


def batch_answered(gate: Gate, held: int, lacking: int, said: Any):
    """The codes, an api whose first batch answers ``said``, and the account over it."""
    api = Api(held_and_lacking(held, lacking))
    api.batch = [said]
    return list(api.held), api, adapter(gate, api)


def test_an_isrc_filed_under_five_releases_costs_one_read_and_no_track_is_read_again(gate):
    account = adapter(gate, api := Api({code(1): ["11", "12", "13", "14", "15"]}))
    found = account.match_track(identity="row-1", isrc=code(1))
    assert found is None
    assert "names 5 provider tracks" in account.unmatched_reason("row-1")
    assert app_reads(gate) == 1
    assert api.singles() == [code(1)]
    assert [one["url"] for one in api.reads()] == [catalogue_api.API_ROOT + "tracks"]


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
    assert app_reads(before_gate) == 50
    assert app_reads(after_gate) == made == 3
    assert [len(one) for one in api.batches()] == [20, 20, 10]
    assert api.singles() == []


def test_a_held_code_is_still_asked_alone_so_every_release_comes_back(gate):
    catalogue = held_and_lacking(5, 15, releases=3)
    codes = list(catalogue)
    account = adapter(gate, api := Api(catalogue))
    assert account.screen_isrcs(codes) == 1
    ask_every(account, codes)
    # One batch, then one lookup per held code.
    assert app_reads(gate) == 6
    assert api.singles() == codes[:5]
    for one in codes[:5]:
        assert "names 3 provider tracks" in account.unmatched_reason(one)


def test_a_code_absent_from_a_batch_answer_is_not_found_and_the_others_are_answered(gate):
    account = adapter(gate, api := Api({code(1): ["101"], code(2): [], code(3): ["301"]}))
    account.screen_isrcs([code(1), code(2), code(3)])
    assert account.match_track(identity="a", isrc=code(1)) == "101"
    assert account.match_track(identity="b", isrc=code(2)) is None
    assert account.unmatched_reason("b") == ""
    assert account.match_track(identity="c", isrc=code(3)) == "301"
    assert api.singles() == [code(1), code(3)]


def test_a_batch_asks_every_code_by_name_in_the_accounts_country_and_nothing_else(gate):
    account = adapter(gate, api := Api(held_and_lacking(1, 1)))
    account.screen_isrcs([code(0), code(1)])
    (sent,) = api.reads()
    assert sent["method"] == "GET"
    assert sent["url"] == catalogue_api.API_ROOT + "tracks"
    assert sent["params"] == {"filter[isrc]": [code(0), code(1)], "countryCode": "GB"}


def test_a_code_already_screened_is_not_sent_again(gate):
    account = adapter(gate, api := Api(held_and_lacking(0, 4)))
    assert account.screen_isrcs([code(0), code(1)]) == 1
    assert account.screen_isrcs([code(1), code(0)]) == 0
    assert account.screen_isrcs([code(0), code(2), code(3)]) == 1
    assert api.batches() == [[code(0), code(1)], [code(2), code(3)]]


def test_a_malformed_code_or_a_spelling_not_its_own_fold_never_enters_a_batch(gate):
    account = adapter(gate, api := Api(held_and_lacking(0, 3)))
    lower = code(2).lower()
    made = account.screen_isrcs(["not-an-isrc", "", lower, code(0), code(1), code(0)])
    assert made == 1
    assert api.batches() == [[code(0), code(1)]]
    # The lowercase spelling was never screened.
    account.match_track(identity="x", isrc=lower)
    assert api.singles() == [lower]


def test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same(gate):
    account = adapter(gate, api := Api(held_and_lacking(0, 21)))
    assert account.screen_isrcs([code(0)]) == 0
    assert account.screen_isrcs([code(n) for n in range(1, 22)]) == 1
    assert api.batches() == [[code(n) for n in range(1, 21)]]
    account.match_track(identity="x", isrc=code(21))
    account.match_track(identity="y", isrc=code(0))
    assert api.singles() == [code(21), code(0)]


def test_the_app_client_refuses_a_batch_it_was_not_built_to_ask(gate):
    app = app_on(gate, Api({}))
    for wrong in ([code(0)], [code(n) for n in range(21)], [code(0), code(0)],
                  [code(0), code(1).lower()], [code(0), "not-an-isrc"]):
        with pytest.raises(ValueError):
            app.isrcs_held(wrong)


def test_a_server_error_on_a_batch_falls_back_to_singles_and_finds_the_one_bad_answer(gate):
    codes, api, account = batch_answered(gate, 1, 3, 500)
    api.single = {code(2): 500}
    assert account.screen_isrcs(codes) == 1
    assert account.match_track(identity="a", isrc=code(0)) == "00"
    assert account.match_track(identity="b", isrc=code(1)) is None
    with pytest.raises(CratekitError):
        account.match_track(identity="c", isrc=code(2))
    assert account.match_track(identity="d", isrc=code(3)) is None
    assert [one for one in api.singles() if one != code(2)] == [code(0), code(1), code(3)]


def test_a_batch_that_failed_is_not_sent_again_by_the_next_plan(gate):
    codes, api, account = batch_answered(gate, 0, 3, 503)
    assert account.screen_isrcs(codes) == 1
    assert account.screen_isrcs(codes) == 0
    assert len(api.batches()) == 1


def test_a_failed_batch_does_not_stop_the_next_one(gate):
    codes, api, account = batch_answered(gate, 0, 40, 503)
    assert account.screen_isrcs(codes) == 2
    ask_every(account, codes)
    assert api.singles() == codes[:20]


def test_a_rate_limit_on_a_batch_is_counted_marks_nothing_and_stops_the_screening(gate):
    codes, api, account = batch_answered(gate, 0, 60, 429)
    assert account.screen_isrcs(codes) == 1
    assert gate.spend().app_rate_limited == 1
    assert account.screen_isrcs([code(98), code(99)]) == 0
    assert len(api.batches()) == 1
    ask_every(account, codes[:3])
    assert api.singles() == codes[:3]


def test_a_rejected_app_credential_on_a_batch_marks_nothing_and_stops_the_screening(gate):
    codes, api, account = batch_answered(gate, 0, 40, 401)
    assert account.screen_isrcs(codes) == 1
    assert account.screen_isrcs([code(98), code(99)]) == 0
    assert account.match_track(identity="a", isrc=code(0)) is None
    assert api.singles() == [code(0)]


@pytest.mark.parametrize("status", [400, 404, 422])
def test_a_refused_request_form_stops_the_screening_and_marks_nothing(gate, status):
    codes, api, account = batch_answered(gate, 0, 60, status)
    assert account.screen_isrcs(codes) == 1
    assert len(api.batches()) == 1
    ask_every(account, codes[:2])
    assert api.singles() == codes[:2]


def test_the_gates_own_park_passes_through_the_screen(gate):
    said = "the gate is cooling down"
    parked = refuse("unavailable-transient", said, remedy=Remedy.RETRY_LATER, origin=("test",))
    _codes, _api, account = batch_answered(gate, 0, 2, parked)
    with pytest.raises(CratekitError) as raised:
        account.screen_isrcs([code(0), code(1)])
    assert raised.value is parked


@pytest.mark.parametrize(
    "said",
    [
        {"data": [track("1", None)], "included": []},
        {"data": [track("1", "not an isrc")], "included": []},
        {"data": [track("1", code(7))], "included": []},
        {"data": [], "links": {"next": "/tracks?page[cursor]=abc"}}, {"data": ["not a resource"]},
        {"data": "not a list"},
    ],
    ids=["no-isrc", "unreadable-isrc", "a-code-not-asked", "paged", "not-a-resource", "no-list"],
)
def test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent(gate, said):
    codes, api, account = batch_answered(gate, 0, 3, said)
    assert account.screen_isrcs(codes) == 1
    ask_every(account, codes)
    assert api.singles() == codes


def test_a_resource_that_is_not_a_track_is_not_read_as_an_answer_about_a_code(gate):
    said = {"data": [track("00", code(0)), {"id": "a1", "type": "artists"}], "included": []}
    codes, api, account = batch_answered(gate, 1, 1, said)
    account.screen_isrcs(codes)
    ask_every(account, codes)
    assert api.singles() == [code(0)]


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


def row(n: int, *, isrc: str = "") -> mirror.Row:
    return mirror.Row(content_id=f"c{n}", title=f"Title {n}", artist=f"Artist {n}", isrc=isrc)


def test_the_mirror_screens_only_the_rows_it_would_ask_the_provider_about():
    account = outbound_fakes.FakeAccount({})
    identified: list[str] = []
    def identify(one: mirror.Row) -> mirror.Identity:
        identified.append(one.content_id)
        return mirror.Identity(isrc=one.isrc or (code(9) if one.content_id == "c5" else ""))
    matcher = mirror.Matcher(
        account, {"c1": ("r1", code(1))}, identify,
        misses={"c3": ("no match", (code(3), "Title 3", "Artist 3", "", ""))}, known={"c2": "r2"},
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


def test_a_provider_track_under_another_emoji_title_does_not_agree():
    """Emoji-only titles fold alike, so the title is read by its identity."""
    from types import SimpleNamespace
    def provider(title: str) -> SimpleNamespace:
        artist = SimpleNamespace(name="Aurora Bloom")
        return SimpleNamespace(
            id="1", name=title, version=None, artist=artist, artists=[artist], isrc="X"
        )
    drop = match.Wanted(artist="Aurora Bloom", title="\U0001f4a7")
    assert tidal_account._agrees(drop, provider("\U0001f525")) is False
    assert tidal_account._agrees(drop, provider("\U0001f4a7")) is True
    plain = match.Wanted(artist="Aurora Bloom", title="Sun Path")
    assert tidal_account._agrees(plain, provider("SUN PATH")) is True
