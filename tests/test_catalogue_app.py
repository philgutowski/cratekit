"""U205: catalogue lookups go under Cratekit's own app credentials.

The first two way sync asked the provider thousands of catalogue questions
under the person's own account session. These claims are the brief's test
scenarios, each driven through the real pacing gate on a temporary state file,
so "counted per identity" is read off the file the gate wrote and never off a
counter the test kept:

1. **With the app's two values recorded, an ISRC lookup makes no account
   call** and its token request and read are counted under ``app``.
2. **Without them every lookup goes to the account exactly as before**, and
   one value of the two is the same as none.
3. **A not found is the one absence.** A server error and a rejected app token
   climb the ladder and refuse, the rejection naming the app's credentials and
   never the account session, and a transport failure whose text carries the
   digits of a not found is not read as one.
4. **A rate limit on the app trips the one gate**, and the account is refused
   inside the same cooldown.
5. **The label crawl stays on the account and is counted there, and no write
   reaches the app client**, which has no write to reach.
6. **A state file today's version wrote still loads**, its calls the account's.
7. **Doctor names the credentials and both counts**, and says when it could
   not read them.
8. **The app client is built at one site**, beside the account opener.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import requests

from cratekit import cli as cli_package
from cratekit.acquire import adapter, catalogue_api, match, provider_session
from cratekit.cli import doctor
from cratekit.cli.output import Envelope
from cratekit.core import provider_gate, secrets
from cratekit.core.cause import CratekitError, Outcome, Scope
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.provider_gate import APP, TRIP_AFTER, Gate, GateSettings, Spend
from cratekit.label import tidal_catalogue
from cratekit.modules.outbound import service, tidal_account

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

ISRC = "GBAAA2400001"
APP_ID = "FAKE-app-identifier"
APP_KEY = "FAKE-app-value"


# ═══════════════════════════════════════════════════════════════════════════
# Doubles
# ═══════════════════════════════════════════════════════════════════════════


class Clock:
    def __init__(self, start: float = 1_700_000_000.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds


class Answer:
    """One HTTP answer: a status, a body the client decodes, and headers."""

    def __init__(self, status_code: int = 200, body: Any = None, *, text: bool = False) -> None:
        self.status_code = status_code
        self.headers: dict[str, str] = {}
        self._body = body
        self._text = text

    def json(self) -> Any:
        if self._text:
            raise ValueError("Expecting value: line 1 column 1")
        return self._body


def token(expires_in: Any = 86400) -> Answer:
    return Answer(200, {"access_token": "FAKE-token", "token_type": "Bearer", "expires_in": expires_in})


def resource(track_id: str, title: str, *, artists=("a1",), album="r1", version=None,
             availability=("STREAM", "DJ")) -> dict:
    attributes: dict[str, Any] = {"title": title, "isrc": ISRC, "version": version}
    if availability is not None:
        attributes["availability"] = list(availability)
    return {
        "id": track_id,
        "type": "tracks",
        "attributes": attributes,
        "relationships": {
            "artists": {"data": [{"id": one, "type": "artists"} for one in artists]},
            "albums": {"data": [{"id": album, "type": "albums"}] if album else []},
        },
    }


INCLUDED = [
    {"id": "a1", "type": "artists", "attributes": {"name": "Aurora Bloom"}},
    {"id": "a2", "type": "artists", "attributes": {"name": "Nova Reef"}},
    {"id": "r1", "type": "albums", "attributes": {"title": "Sun Path"}},
    {"id": "r2", "type": "albums", "attributes": {"title": "Night Signals Vol 4"}},
]


def answer_with(*tracks: dict, included=INCLUDED) -> Answer:
    return Answer(200, {"data": list(tracks), "included": list(included)})


class AppTransport:
    """The app client's ``requests.Session``: the token service answers from
    ``tokens``, every read from ``reads``, the last answer of each repeating,
    and every request is recorded with what was sent."""

    def __init__(self, reads: list[Any] | None = None, tokens: list[Any] | None = None) -> None:
        self.reads = list(reads or [answer_with()])
        self.tokens = list(tokens or [token()])
        self.sent: list[dict[str, Any]] = []

    @staticmethod
    def _next(queue: list[Any]) -> Any:
        answer = queue.pop(0) if len(queue) > 1 else queue[0]
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        self.sent.append({"method": method, "url": url, **kwargs})
        if url == catalogue_api.TOKEN_URL:
            return self._next(self.tokens)
        return self._next(self.reads)

    def reads_sent(self) -> list[dict[str, Any]]:
        return [one for one in self.sent if one["url"] != catalogue_api.TOKEN_URL]


class AccountTransport:
    def __init__(self, status: int = 200) -> None:
        self.status = status
        self.sent: list[tuple[str, str]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        del kwargs
        self.sent.append((method, url))
        return Answer(self.status)


class Track:
    def __init__(self, track_id: str, name: str = "Sun Path", artist: str = "Aurora Bloom") -> None:
        self.id = track_id
        self.name = name
        self.version = None
        self.artists = [SimpleNamespace(name=artist)]
        self.artist = self.artists[0]
        self.album = SimpleNamespace(name="Sun Path")
        self.available = True


class AccountClient:
    """The account's logged in client. Every method sends one request through
    its own transport, as the provider library's do, so the gate counts it."""

    def __init__(self, *, country_code: Any = "GB", isrcs: dict[str, list[str]] | None = None) -> None:
        self.request_session = AccountTransport()
        self.country_code = country_code
        self.isrcs = dict(isrcs or {})
        self.hearts: list[str] = []
        self.user = SimpleNamespace(
            id="u1", favorites=SimpleNamespace(add_track=self._heart, tracks=self._hearts)
        )

    def _send(self, what: str) -> None:
        self.request_session.request("GET", f"https://api.invalid/{what}")

    def get_tracks_by_isrc(self, isrc: str) -> list[Track]:
        self._send("isrc")
        return [Track(one) for one in self.isrcs.get(isrc, [])]

    def track(self, track_id: str) -> Track:
        self._send("track")
        return Track(track_id)

    def album(self, release_id: str) -> Any:
        self._send("album")
        return SimpleNamespace(id=release_id, artist=SimpleNamespace(name="Aurora Bloom"),
                               artists=[SimpleNamespace(name="Aurora Bloom")])

    def _heart(self, track_id: str) -> bool:
        self._send("heart")
        self.hearts.append(track_id)
        return True

    def _hearts(self, limit: int = 50, offset: int = 0) -> list[Track]:
        self._send("hearts")
        return [Track(one) for one in self.hearts[offset : offset + limit]]


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def gate(tmp_path: Path, clock: Clock) -> Gate:
    return Gate(
        GateSettings(min_interval_s=0.0, cooldown_s=900.0),
        path=tmp_path / "gate" / "provider_gate.json",
        lock_path=tmp_path / "gate" / "provider_gate.lock",
        clock=clock,
        sleep=clock.sleep,
    )


@pytest.fixture(autouse=True)
def no_ladder_sleep(monkeypatch):
    monkeypatch.setattr(tidal_catalogue, "_pause", lambda seconds: None)


def record_app(*names: str) -> None:
    for name in names or [str(one) for one in catalogue_api.CREDENTIALS]:
        secrets.set(name, APP_ID if name.endswith("id") else APP_KEY)


def use_transport(monkeypatch, transport: AppTransport) -> AppTransport:
    monkeypatch.setattr(provider_session, "CATALOGUE_TRANSPORT_FACTORY", lambda: transport)
    return transport


def opened(monkeypatch, gate: Gate, transport: AppTransport | None = None,
           account: AccountClient | None = None) -> tuple[AccountClient, Any, AppTransport]:
    """An account client attached to ``gate``, and the app client the opener
    builds beside it, as ``open_account`` builds both."""
    account = account or AccountClient()
    transport = use_transport(monkeypatch, transport or AppTransport())
    assert gate.attach(account) is True
    return account, provider_session.catalogue_client(account, gate=gate), transport


def on_disk(gate: Gate) -> dict[str, Any]:
    return json.loads(gate.path.read_text(encoding="utf-8"))


def no_sleep(seconds: float) -> None:
    del seconds


# ═══════════════════════════════════════════════════════════════════════════
# 1. With the app recorded, the lookup leaves the account
# ═══════════════════════════════════════════════════════════════════════════


def test_an_isrc_match_with_the_app_recorded_makes_no_account_call(monkeypatch, gate):
    record_app()
    account, app, transport = opened(
        monkeypatch, gate, AppTransport([answer_with(resource("101", "Sun Path"))])
    )
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    assert adapter_.match_track(identity="row-1", isrc=ISRC) == "101"

    assert account.request_session.sent == []
    assert [one["method"] for one in transport.sent] == ["POST", "GET"]
    spent = gate.spend()
    assert (spent.calls, spent.app_calls, spent.account_calls) == (2, 2, 0)
    assert on_disk(gate)["identities"] == {
        "account": {"calls": 0, "rate_limited": 0},
        "app": {"calls": 2, "rate_limited": 0},
    }


def test_the_lookup_asks_the_isrc_in_the_accounts_own_country_with_the_names_included(
    monkeypatch, gate
):
    record_app()
    account, app, transport = opened(monkeypatch, gate, account=AccountClient(country_code="nl"))

    app.get_tracks_by_isrc(ISRC)

    read = transport.reads_sent()[0]
    assert read["url"] == catalogue_api.API_ROOT + "tracks"
    assert read["params"] == {"filter[isrc]": ISRC, "include": "artists,albums", "countryCode": "NL"}
    assert read["headers"]["Authorization"] == "Bearer FAKE-token"
    posted = transport.sent[0]
    assert posted["auth"] == (APP_ID, APP_KEY)
    assert posted["data"] == {"grant_type": "client_credentials"}


def test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it(monkeypatch, gate):
    record_app()
    account, app, transport = opened(
        monkeypatch, gate, AppTransport([answer_with(resource("101", "Sun Path"))])
    )
    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=app)

    found = catalogue.tracks_for_isrc(ISRC)

    assert [one.id for one in found] == ["101"]
    assert account.request_session.sent == []
    assert gate.spend().app_calls == 2


def test_the_token_is_fetched_once_and_reused_until_it_nears_expiry(monkeypatch, gate, clock):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport(tokens=[token(600)]))
    app._clock = clock

    app.get_tracks_by_isrc(ISRC)
    app.get_tracks_by_isrc(ISRC)
    clock.now += 600 - catalogue_api.TOKEN_MARGIN_S - 1
    app.get_tracks_by_isrc(ISRC)
    clock.now += 2
    app.get_tracks_by_isrc(ISRC)

    tokens = [one for one in transport.sent if one["url"] == catalogue_api.TOKEN_URL]
    assert len(tokens) == 2
    assert len(transport.reads_sent()) == 4


def test_a_token_with_no_readable_lifetime_serves_one_margin_and_is_asked_again(
    monkeypatch, gate, clock
):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport(tokens=[token("soon")]))
    app._clock = clock

    app.get_tracks_by_isrc(ISRC)
    clock.now += catalogue_api.TOKEN_MARGIN_S - 1
    app.get_tracks_by_isrc(ISRC)
    clock.now += 2
    app.get_tracks_by_isrc(ISRC)

    tokens = [one for one in transport.sent if one["url"] == catalogue_api.TOKEN_URL]
    assert len(tokens) == 2


def test_the_answer_is_read_into_the_shape_the_choosing_logic_reads(monkeypatch, gate):
    record_app()
    account, app, transport = opened(
        monkeypatch,
        gate,
        AppTransport([answer_with(
            resource("101", "Sun Path", artists=("a1", "a2"), version="Extended Mix"),
            resource("102", "Sun Path", album="r2", availability=("DJ",)),
            resource("103", "Sun Path", availability=None),
        )]),
    )

    first, second, third = app.get_tracks_by_isrc(ISRC)

    assert (first.id, first.name, first.version, first.isrc) == ("101", "Sun Path", "Extended Mix", ISRC)
    assert [one.name for one in first.artists] == ["Aurora Bloom", "Nova Reef"]
    assert first.artist.name == "Aurora Bloom"
    assert first.album.name == "Sun Path"
    assert first.available is True
    assert second.album.name == "Night Signals Vol 4"
    assert second.available is False
    assert third.available is None
    read = match.read_row(first, origin=match.TIDAL, position=1)
    assert (read.artist, read.title, read.version) == ("Aurora Bloom", "Sun Path", "Extended Mix")


def test_several_releases_from_the_app_are_chosen_among_by_the_unchanged_rules(monkeypatch, gate):
    """The single and the compilation cut agree with the row; the file's album
    names the compilation, so the third rule chooses it, off names the app
    answer carried in ``included``."""
    record_app()
    account, app, transport = opened(
        monkeypatch,
        gate,
        AppTransport([answer_with(resource("101", "Sun Path"), resource("102", "Sun Path", album="r2"))]),
    )
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    chosen = adapter_.match_track(
        identity="row-1", isrc=ISRC, title="Sun Path", artist="Aurora Bloom",
        album="Night Signals Vol 4",
    )

    assert chosen == "102"
    # The hearts the second rule asks are the account's own, and went there.
    assert account.request_session.sent == [("GET", "https://api.invalid/hearts")]


def test_a_release_whose_artists_did_not_come_back_is_unreadable_and_chooses_nothing(
    monkeypatch, gate
):
    record_app()
    account, app, transport = opened(
        monkeypatch,
        gate,
        AppTransport([answer_with(
            resource("101", "Sun Path"), resource("102", "Sun Path", artists=("missing",)),
        )]),
    )
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    chosen = adapter_.match_track(identity="row-1", isrc=ISRC, title="Sun Path", artist="Aurora Bloom")

    assert chosen is None
    assert f"1 {service.UNREADABLE_CANDIDATE}" in adapter_.unmatched_reason("row-1")


def test_an_exact_track_reference_is_read_from_the_app(monkeypatch, gate):
    record_app()
    account, app, transport = opened(
        monkeypatch, gate, AppTransport([Answer(200, {"data": resource("555", "Sun Path"), "included": INCLUDED})])
    )
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    assert adapter_.match_track(identity="https://tidal.com/browse/track/555") == "555"
    assert transport.reads_sent()[0]["url"] == catalogue_api.API_ROOT + "tracks/555"
    assert account.request_session.sent == []


def test_a_track_identifier_that_is_not_a_number_is_never_put_in_a_path(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate)

    with pytest.raises(ValueError):
        app.track("../users/1")
    assert transport.sent == []


# ═══════════════════════════════════════════════════════════════════════════
# 2. Without the app, the account exactly as before
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("recorded", [(), ("catalogue-app-id",), ("catalogue-app-key",)])
def test_without_both_values_the_opener_builds_no_app_client(monkeypatch, gate, recorded):
    for name in recorded:
        record_app(name)
    transport = use_transport(monkeypatch, AppTransport())

    assert provider_session.catalogue_client(AccountClient(), gate=gate) is None
    assert transport.sent == []


def test_without_the_app_an_isrc_lookup_goes_to_the_account_and_is_counted_there(gate):
    account = AccountClient(isrcs={ISRC: ["101"]})
    gate.attach(account)
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=None)
    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=None)

    assert adapter_.match_track(identity="row-1", isrc=ISRC) == "101"
    assert [one.id for one in catalogue.tracks_for_isrc(ISRC)] == ["101"]

    assert account.request_session.sent == [("GET", "https://api.invalid/isrc")] * 2
    spent = gate.spend()
    assert (spent.calls, spent.account_calls, spent.app_calls) == (2, 2, 0)


def test_open_account_and_open_catalogue_hand_the_app_client_on(monkeypatch, tmp_path):
    """Both openers, with the account's login faked, hold the app client
    built over the same gate."""
    account = AccountClient()
    account.load_oauth_session = lambda *args, **kwargs: True
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: account)
    secrets.set_json(
        secrets.Credential.PROVIDER_SESSION,
        {"token_type": "Bearer", "access_token": "FAKE-1", "refresh_token": "FAKE-2", "expiry_time": 1.0},
    )
    use_transport(monkeypatch, AppTransport())

    assert tidal_account.open_account()._lookups is account
    assert tidal_catalogue.open_catalogue()._lookups is account

    record_app()
    held = tidal_account.open_account()._lookups
    catalogue_held = tidal_catalogue.open_catalogue()._lookups
    assert isinstance(held, catalogue_api.AppCatalogue)
    assert isinstance(catalogue_held, catalogue_api.AppCatalogue)
    assert held.request_session._cratekit_gate is account.request_session._cratekit_gate


def test_an_account_that_names_no_country_gets_no_app_client(monkeypatch, gate):
    record_app()
    transport = use_transport(monkeypatch, AppTransport())

    for country in (None, "", "GBR", "1A"):
        assert provider_session.catalogue_client(AccountClient(country_code=country), gate=gate) is None
    assert transport.sent == []


def test_a_value_the_index_records_and_the_keychain_lost_is_absent_and_asks_the_account(
    monkeypatch, gate
):
    """U205's review, round one: a value deleted through the operating
    system's own keychain is not there, and refusing over it would lock every
    verb that opens the account with no way back short of registering again."""
    record_app()
    transport = use_transport(monkeypatch, AppTransport())
    account = AccountClient(isrcs={ISRC: ["101"]})
    gate.attach(account)
    real_get = secrets.get

    def lost(name: str) -> str:
        if name == "catalogue-app-key":
            raise secrets.CredentialMissing(f"no credential recorded for {name!r}", name=name)
        return real_get(name)

    monkeypatch.setattr(secrets, "get", lost)

    assert secrets.exists("catalogue-app-key") is True
    assert provider_session.catalogue_client(account, gate=gate) is None
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=None)
    assert adapter_.match_track(identity="row-1", isrc=ISRC) == "101"
    assert transport.sent == []
    assert gate.spend().account_calls == 1


def test_a_keychain_that_could_not_be_read_for_the_app_is_refused_not_read_as_absent(
    monkeypatch, gate
):
    record_app()
    use_transport(monkeypatch, AppTransport())

    def broken(name: str) -> str:
        raise secrets.CredentialBackendUnavailable("no keychain backend could be reached", name=name)

    monkeypatch.setattr(secrets, "get", broken)

    with pytest.raises(CratekitError) as caught:
        provider_session.catalogue_client(AccountClient(), gate=gate)
    assert caught.value.cause.reason == "credential-missing"
    assert caught.value.cause.remediation.remedy is Remedy.SET_CREDENTIAL


# ═══════════════════════════════════════════════════════════════════════════
# 3. A not found is the one absence
# ═══════════════════════════════════════════════════════════════════════════


def test_a_404_on_a_track_read_is_no_track_and_is_asked_once(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport([Answer(404, {})]))
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    assert adapter_.match_track(identity="https://tidal.com/browse/track/555") is None
    assert len(transport.reads_sent()) == 1


def test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track(monkeypatch, gate):
    """The collection answers a code matching nothing with an empty list, so a
    404 there says the address moved; read as no track, ``sync pair`` would
    remember a miss for every row (U205's review, round one)."""
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport([Answer(404, {})]))
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)
    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=app)

    with pytest.raises(CratekitError) as caught:
        adapter_.match_track(identity="row-1", isrc=ISRC)
    assert caught.value.cause.reason == "unavailable-transient"
    with pytest.raises(catalogue_api.CatalogueUnavailable) as raised:
        catalogue.tracks_for_isrc(ISRC)
    assert adapter.classify_unavailable(raised.value) is adapter.TrackOutcome.UNAVAILABLE_TRANSIENT


def test_an_isrc_the_catalogue_files_nothing_under_is_the_empty_answer(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport([answer_with()]))

    assert tidal_catalogue.TidalCatalogue(account, catalogue=app).tracks_for_isrc(ISRC) == ()


@pytest.mark.parametrize(
    "answer",
    [Answer(500, {}), Answer(503, {}), Answer(200, text=True), Answer(200, {"data": {"id": "1"}}),
     Answer(200, ["not", "an", "object"]), Answer(400, {})],
    ids=["500", "503", "not-json", "data-not-a-list", "not-an-object", "400"],
)
def test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match(
    monkeypatch, gate, answer
):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport([answer]))
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)
    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=app)

    with pytest.raises(CratekitError) as caught:
        adapter_.match_track(identity="row-1", isrc=ISRC)
    assert caught.value.cause.reason == "unavailable-transient"
    assert len(transport.reads_sent()) == 1 + tidal_account.WRITE_RETRIES

    before = len(transport.reads_sent())
    with pytest.raises(catalogue_api.CatalogueUnavailable):
        catalogue.tracks_for_isrc(ISRC)
    assert len(transport.reads_sent()) - before == 6


@pytest.mark.parametrize("status", [401, 403])
def test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app(
    monkeypatch, gate, status
):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport([Answer(status, {})]))
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    with pytest.raises(CratekitError) as caught:
        adapter_.match_track(identity="row-1", isrc=ISRC)

    cause = caught.value.cause
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy is Remedy.SET_CREDENTIAL
    assert cause.scope is Scope.RUN
    assert cause.detail["credential"] == "catalogue-app-id"
    assert "app credentials" in cause.message
    # Each attempt asked for a fresh token, since an expired one is the
    # ordinary reason for the refusal.
    tokens = [one for one in transport.sent if one["url"] == catalogue_api.TOKEN_URL]
    assert len(tokens) == len(transport.reads_sent()) == 1 + tidal_account.WRITE_RETRIES

    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=app)
    with pytest.raises(CratekitError) as again:
        catalogue.tracks_for_isrc(ISRC)
    assert again.value.cause.reason == "credential-missing"
    assert again.value.cause.remediation.remedy is Remedy.SET_CREDENTIAL


def test_a_rejected_app_token_that_was_only_expired_is_answered_on_the_next_rung(
    monkeypatch, gate
):
    record_app()
    account, app, transport = opened(
        monkeypatch, gate, AppTransport([Answer(401, {}), answer_with(resource("101", "Sun Path"))])
    )
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    assert adapter_.match_track(identity="row-1", isrc=ISRC) == "101"


@pytest.mark.parametrize("status", [400, 401, 403])
def test_a_token_service_refusing_the_app_is_a_rejected_app_credential(monkeypatch, gate, status):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport(tokens=[Answer(status, {})]))

    with pytest.raises(CratekitError) as caught:
        tidal_catalogue.TidalCatalogue(account, catalogue=app).tracks_for_isrc(ISRC)
    assert caught.value.cause.remediation.remedy is Remedy.SET_CREDENTIAL
    assert transport.reads_sent() == []


@pytest.mark.parametrize(
    "answer", [Answer(500, {}), Answer(404, {}), Answer(200, text=True), Answer(200, {"token_type": "x"})],
    ids=["500", "no-such-address", "not-json", "no-token"],
)
def test_a_token_service_that_did_not_answer_is_an_outage_never_an_absence(monkeypatch, gate, answer):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport(tokens=[answer]))

    with pytest.raises(catalogue_api.CatalogueUnavailable) as caught:
        app.get_tracks_by_isrc(ISRC)
    assert adapter.classify_unavailable(caught.value) is adapter.TrackOutcome.UNAVAILABLE_TRANSIENT


def test_a_transport_failure_whose_text_holds_404_is_not_read_as_no_track(monkeypatch, gate):
    """The ISRC GBAAA2404040 holds the digits of a not found, and the
    transport's own message quotes the URL that carries it."""
    code = "GBAAA2404040"
    record_app()
    failure = requests.ConnectionError(
        f"HTTPSConnectionPool(host='openapi.tidal.com'): Max retries exceeded with url: "
        f"/v2/tracks?filter%5Bisrc%5D={code}"
    )
    account, app, transport = opened(monkeypatch, gate, AppTransport([failure]))
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    with pytest.raises(catalogue_api.CatalogueUnavailable) as caught:
        app.get_tracks_by_isrc(code)
    assert "404" not in str(caught.value)
    assert caught.value.__cause__ is failure
    assert adapter.classify_unavailable(caught.value) is adapter.TrackOutcome.UNAVAILABLE_TRANSIENT

    with pytest.raises(CratekitError) as refused:
        adapter_.match_track(identity="row-1", isrc=code)
    assert refused.value.cause.reason == "unavailable-transient"


def test_no_failure_message_carries_the_isrc_or_a_not_found(monkeypatch, gate):
    code = "GBAAA2404040"
    record_app()
    for status in (400, 401, 403, 429, 500, 503):
        account, app, transport = opened(monkeypatch, gate, AppTransport([Answer(status, {})]))
        with pytest.raises(catalogue_api.CatalogueError) as caught:
            app.get_tracks_by_isrc(code)
        text = str(caught.value).lower()
        assert code.lower() not in text and "404" not in text and "not found" not in text
        assert caught.value.status == status


# ═══════════════════════════════════════════════════════════════════════════
# 4. A rate limit on the app trips the one gate
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too(
    monkeypatch, gate
):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport([Answer(429, {})]))
    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=app)

    with pytest.raises(CratekitError) as caught:
        catalogue.tracks_for_isrc(ISRC)
    assert caught.value.cause.reason == provider_gate.COOLDOWN
    assert len(transport.reads_sent()) == TRIP_AFTER
    spent = gate.spend()
    assert (spent.app_rate_limited, spent.account_rate_limited) == (TRIP_AFTER, 0)

    with pytest.raises(CratekitError) as refused:
        account.track("1")
    assert refused.value.cause.reason == provider_gate.COOLDOWN
    assert account.request_session.sent == []


def test_the_gates_park_raised_inside_the_app_transport_passes_through_as_itself(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate)
    gate._write(provider_gate._State(tripped_at=gate._clock(), lifts_at=gate._clock() + 900))

    with pytest.raises(CratekitError) as caught:
        app.get_tracks_by_isrc(ISRC)
    assert caught.value.cause.reason == provider_gate.COOLDOWN
    assert transport.sent == []


# ═══════════════════════════════════════════════════════════════════════════
# 5. The crawl stays on the account; no write reaches the app
# ═══════════════════════════════════════════════════════════════════════════


def test_a_label_read_stays_on_the_account_and_is_counted_there(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate)
    catalogue = tidal_catalogue.TidalCatalogue(account, catalogue=app)

    assert catalogue.release_artist("777") == "Aurora Bloom"

    assert account.request_session.sent == [("GET", "https://api.invalid/album")]
    assert transport.sent == []
    spent = gate.spend()
    assert (spent.account_calls, spent.app_calls) == (1, 0)


def test_a_write_goes_to_the_account_and_never_to_the_app(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate)
    adapter_ = tidal_account.TidalAccount(account, sleep=no_sleep, catalogue=app)

    adapter_.add_heart("101")

    assert account.hearts == ["101"]
    assert transport.sent == []


def test_the_app_client_has_no_write_and_sends_only_reads_and_its_token_request():
    """Its public surface is the two reads, and the only methods it ever sends
    are a GET under the API root and a POST to the token service."""
    public = sorted(
        name for name in vars(catalogue_api.AppCatalogue) if not name.startswith("_")
    )
    assert public == ["get_tracks_by_isrc", "track"]
    tree = ast.parse((SRC_ROOT / "cratekit/acquire/catalogue_api.py").read_text(encoding="utf-8"))
    sent = sorted(
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "_send"
        and node.args
        and isinstance(node.args[0], ast.Constant)
    )
    assert sent == ["GET", "POST"]


# ═══════════════════════════════════════════════════════════════════════════
# 6. The state file today's version wrote
# ═══════════════════════════════════════════════════════════════════════════


def test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts(
    monkeypatch, gate
):
    gate.path.parent.mkdir(parents=True)
    gate.path.write_text(json.dumps({
        "last_call": 1.0, "not_before": 0.0, "consecutive": 0, "tripped_at": None,
        "lifts_at": None, "calls": 389_000, "rate_limited": 12, "trips": 1,
    }), encoding="utf-8")

    spent = gate.spend()
    assert (spent.account_calls, spent.account_rate_limited, spent.app_calls) == (389_000, 12, 0)
    assert provider_gate.read_spend(gate.path) == spent

    record_app()
    account, app, transport = opened(monkeypatch, gate)
    app.get_tracks_by_isrc(ISRC)

    written = on_disk(gate)
    assert written["calls"] == 389_002
    assert written["trips"] == 1
    assert written["identities"]["account"] == {"calls": 389_000, "rate_limited": 12}
    assert written["identities"]["app"] == {"calls": 2, "rate_limited": 0}


def test_an_app_share_larger_than_the_total_is_clamped_to_it(gate):
    gate.path.parent.mkdir(parents=True)
    gate.path.write_text(json.dumps({
        "calls": 5, "rate_limited": 1,
        "identities": {"app": {"calls": 50, "rate_limited": 9}},
    }), encoding="utf-8")

    spent = gate.spend()
    assert (spent.app_calls, spent.app_rate_limited, spent.account_calls) == (5, 1, 0)


def test_the_report_reader_says_when_it_could_not_read_the_file(tmp_path):
    path = tmp_path / "provider_gate.json"
    assert provider_gate.read_spend(path) == Spend()
    path.write_text("{not json", encoding="utf-8")
    assert provider_gate.read_spend(path) is None
    path.write_text("[1, 2]", encoding="utf-8")
    assert provider_gate.read_spend(path) is None


def test_attaching_under_a_name_that_is_no_identity_is_refused(gate):
    with pytest.raises(ValueError):
        gate.attach(AccountClient(), identity="person")


def test_the_spend_line_names_the_account_and_the_app_apart(monkeypatch):
    spends = iter([Spend(), Spend(calls=7, rate_limited=1, app_calls=5, app_rate_limited=1)])
    monkeypatch.setattr(cli_package, "_provider_spend", lambda: next(spends))
    envelope = Envelope(
        schema="diagnostic/1", verb="doctor", run_id="r", outcome=Outcome.OK,
        exit_code=ExitCode.OK, started="s", ended="e",
    )

    before = cli_package._provider_spend()
    shown = cli_package._with_provider_spend(envelope, before)

    assert shown.warnings[-1]["message"] == (
        "7 calls to the streaming provider this run, 1 answered with a rate limit; "
        "2 on the account and 5 under Cratekit's app credentials"
    )


def test_process_spend_carries_the_apps_share(monkeypatch, gate):
    before = provider_gate.process_spend()
    record_app()
    account, app, transport = opened(monkeypatch, gate)
    app.get_tracks_by_isrc(ISRC)
    account.track("1")

    spent = provider_gate.process_spend().since(before)
    assert (spent.calls, spent.app_calls, spent.account_calls) == (3, 2, 1)


# ═══════════════════════════════════════════════════════════════════════════
# 7. Doctor
# ═══════════════════════════════════════════════════════════════════════════


def _catalogue_finding(recorded: set[str], spent: Spend | None) -> doctor.Finding:
    probes = doctor.Probes(
        credential_recorded=lambda name: name in recorded, provider_spend=lambda: spent
    )
    inputs = SimpleNamespace(probes=probes, required=lambda key: False)
    return doctor._check_credential("credential.catalogue", inputs)


def test_doctor_names_missing_app_credentials_where_lookups_go_and_how_to_move_them():
    finding = _catalogue_finding(set(), Spend(calls=10, app_calls=0))

    assert finding.status is doctor.Status.INFO
    assert "not recorded (catalogue-app-id, catalogue-app-key)" in finding.detail
    assert "catalogue lookups go to the account session" in finding.detail
    assert "crate login catalogue-app-id --from-file PATH" in finding.detail
    assert "10 calls on the account and 0 under Cratekit's app credentials" in finding.detail


def test_doctor_names_the_one_value_of_two_that_is_missing():
    finding = _catalogue_finding({"catalogue-app-id"}, Spend())

    assert finding.status is doctor.Status.INFO
    assert "not recorded (catalogue-app-key)" in finding.detail
    assert "one value without the other cannot ask for a token" in finding.detail


def test_doctor_with_both_recorded_shows_both_counts():
    finding = _catalogue_finding(
        {"catalogue-app-id", "catalogue-app-key"},
        Spend(calls=30, rate_limited=3, app_calls=20, app_rate_limited=1),
    )

    assert finding.status is doctor.Status.OK
    assert "go under Cratekit's app credentials" in finding.detail
    assert "10 calls on the account and 20 under Cratekit's app credentials" in finding.detail
    assert "of which 2 and 1 were answered with a rate limit" in finding.detail


def test_doctor_says_when_the_gates_file_could_not_be_read_rather_than_showing_nothing():
    finding = _catalogue_finding(set(), None)

    assert "state file could not be read" in finding.detail
    assert "0 calls" not in finding.detail


def test_the_app_credentials_are_recordable_by_the_login_verb():
    from cratekit.cli.verbs import login

    assert {"catalogue-app-id", "catalogue-app-key"} <= set(login.CREDENTIAL_NAMES)


# ═══════════════════════════════════════════════════════════════════════════
# 8. One construction site
# ═══════════════════════════════════════════════════════════════════════════


def test_the_app_client_is_built_beside_the_account_opener_and_nowhere_else():
    package = SRC_ROOT / "cratekit"
    found = sorted(
        str(path.relative_to(package))
        for path in package.rglob("*.py")
        if "AppCatalogue(" in path.read_text(encoding="utf-8")
        and path.name != "catalogue_api.py"
    )
    assert found == ["acquire/provider_session.py"]


def test_the_opener_attaches_the_app_client_under_the_app_identity(monkeypatch, gate):
    record_app()
    account, app, transport = opened(monkeypatch, gate)

    assert app.request_session._cratekit_gate is gate
    app.get_tracks_by_isrc(ISRC)
    assert gate.spend().app_calls == 2
    assert APP == "app"


def test_the_live_catalogue_transport_is_refused_in_every_test(monkeypatch, gate):
    record_app()
    with pytest.raises(AssertionError, match="live catalogue transport"):
        provider_session.catalogue_client(AccountClient(), gate=gate)


# ═══════════════════════════════════════════════════════════════════════════
# The guards round one found killing nothing
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("lifetime", [60, 30])
def test_a_short_lived_token_keeps_half_its_life_rather_than_none(monkeypatch, gate, clock, lifetime):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport(tokens=[token(lifetime)]))
    app._clock = clock

    for _ in range(3):
        app.get_tracks_by_isrc(ISRC)
    clock.now += lifetime / 2 - 1
    app.get_tracks_by_isrc(ISRC)
    clock.now += 2
    app.get_tracks_by_isrc(ISRC)

    tokens = [one for one in transport.sent if one["url"] == catalogue_api.TOKEN_URL]
    assert len(tokens) == 2


def test_a_lifetime_that_is_a_flag_is_not_read_as_one_second(monkeypatch, gate, clock):
    record_app()
    account, app, transport = opened(monkeypatch, gate, AppTransport(tokens=[token(True)]))
    app._clock = clock

    app.get_tracks_by_isrc(ISRC)
    clock.now += 2
    app.get_tracks_by_isrc(ISRC)

    tokens = [one for one in transport.sent if one["url"] == catalogue_api.TOKEN_URL]
    assert len(tokens) == 1


def test_a_resource_in_the_answer_that_is_not_a_track_is_not_a_candidate(monkeypatch, gate):
    record_app()
    stray = {"id": "9", "type": "albums", "attributes": {"title": "Sun Path"}}
    account, app, transport = opened(
        monkeypatch, gate, AppTransport([answer_with(resource("101", "Sun Path"), stray)])
    )

    assert [one.id for one in app.get_tracks_by_isrc(ISRC)] == ["101"]


def test_an_included_resource_is_matched_by_its_kind_and_identifier_both(monkeypatch, gate):
    """An album sharing an artist's identifier is not that artist, and an
    included entry with no kind names nothing."""
    record_app()
    included = [
        {"id": "a1", "type": "albums", "attributes": {"name": "Wrong Kind", "title": "Wrong Kind"}},
        {"id": "a1", "attributes": {"name": "No Kind"}},
        {"id": "r1", "type": "albums", "attributes": {"title": "Sun Path"}},
    ]
    track = resource("101", "Sun Path")
    track["relationships"]["artists"]["data"].append({"id": "a1"})
    account, app, transport = opened(
        monkeypatch, gate, AppTransport([answer_with(track, included=included)])
    )

    (found,) = app.get_tracks_by_isrc(ISRC)
    assert found.artists == ()
    assert found.album.name == "Sun Path"


def test_the_report_reader_says_when_the_file_could_not_be_opened(tmp_path):
    folder = tmp_path / "provider_gate.json"
    folder.mkdir()
    assert provider_gate.read_spend(folder) is None


def test_a_call_named_for_no_identity_is_refused(gate):
    with pytest.raises(ValueError):
        gate.call(lambda: Answer(200), identity="App")
    assert gate.spend() == Spend()
