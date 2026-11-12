"""U261: one process validates the stored provider session once, and an
unchanged session is not written back to the keychain.

Before this unit every opener logged in on its own: two paced requests, two
keychain reads and a keychain write of the value already stored, per resolve
of the label catalogue and once more for the outbound account. These are the
brief's scenarios, driven against the in memory keychain and a counting client
whose login sends the two requests the provider library's login sends, through
a transport the real gate wraps, so a request counted here is a request the
gate counted.

1. **An unchanged session makes no keychain write**, and a refreshed one is
   written exactly once, through ``secrets.set`` and its index.
2. **One process validates the session once** however many times either seam
   resolves, and each seam still gets its own adapter.
3. **A refused session is forgotten for every seam that shares the client**:
   the account's 401, any 401 or 403 answered through the shared client, a
   session the index no longer records, and a keychain that no longer holds it.
4. **The gate is asked before every use**, and a login that failed holds
   nothing.

D1 applies. Nothing here names a real account, a real token or a real path.
"""

from __future__ import annotations

from typing import Any

import keyring
import pytest

from cratekit.acquire import catalogue_api, provider_session
from cratekit.core import config, provider_gate, secrets
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, tidal_catalogue
from cratekit.modules.outbound import account, tidal_account
from tests.test_catalogue_app import AppTransport, record_app
from tests.test_config import valid_data

SESSION = secrets.Credential.PROVIDER_SESSION

STORED = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": 946684800.0,
}

#: The two requests the provider library's ``load_oauth_session`` sends.
LOGIN = [("GET", "https://api.invalid/sessions"), ("GET", "https://api.invalid/users/u1")]


# ═══════════════════════════════════════════════════════════════════════════
# Doubles
# ═══════════════════════════════════════════════════════════════════════════


class Answer:
    def __init__(self, status_code: int = 200) -> None:
        self.status_code = status_code
        self.headers: dict[str, str] = {}

    def json(self) -> dict:
        return {}


class HTTPFailure(Exception):
    """The provider library's HTTP error, with the answer it was raised over."""

    def __init__(self, response: Answer) -> None:
        super().__init__(f"HTTP {response.status_code}")
        self.response = response


class Transport:
    """The client's ``requests.Session``: answers ``status`` to everything and
    records every request, so the gate wraps it as it wraps the real one."""

    def __init__(self, status: int = 200) -> None:
        self.status = status
        #: A status to RAISE rather than answer, as a transport whose refusal
        #: comes out as an exception carrying the answer.
        self.raises: int | None = None
        self.sent: list[tuple[str, str]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> Answer:
        del kwargs
        self.sent.append((method, url))
        if self.raises is not None:
            raise HTTPFailure(Answer(self.raises))
        return Answer(self.status)


class Client:
    """A provider client whose login sends the library's two requests through
    its transport, and refuses on any answer that is not a 200, as the library
    raises off ``raise_for_status``. ``refresh_to`` stands for a login that
    refreshed the access token."""

    def __init__(self, *, status: int = 200, refresh_to: str | None = None,
                 country_code: str | None = None) -> None:
        self.request_session = Transport(status)
        self.refresh_to = refresh_to
        self.country_code = country_code
        self.logged_in_with: str | None = None
        self.token_type = self.access_token = self.refresh_token = self.expiry_time = None

    def load_oauth_session(self, token_type, access_token, refresh_token=None,
                           expiry_time=None, is_pkce=False) -> bool:
        del is_pkce
        self.logged_in_with = access_token
        for method, url in LOGIN:
            answer = self.request_session.request(method, url)
            if answer.status_code != 200:
                raise HTTPFailure(answer)
        self.token_type, self.refresh_token, self.expiry_time = token_type, refresh_token, expiry_time
        self.access_token = self.refresh_to or access_token
        return True

    def read(self) -> int:
        """One catalogue read after login, as the catalogue's calls make them."""
        return self.request_session.request("GET", "https://api.invalid/tracks").status_code


class Factory:
    """``CLIENT_FACTORY``: a fresh client per build, every one kept."""

    def __init__(self, **client: Any) -> None:
        self.client = client
        self.built: list[Client] = []

    def __call__(self) -> Client:
        self.built.append(Client(**self.client))
        return self.built[-1]

    @property
    def requests(self) -> list[tuple[str, str]]:
        return [one for client in self.built for one in client.request_session.sent]


class Keychain:
    """Counts the keychain calls the in memory keychain answers."""

    def __init__(self, monkeypatch) -> None:
        self.writes: list[str] = []
        self.reads = 0
        real_set, real_get = keyring.set_password, keyring.get_password

        def set_password(service: str, username: str, password: str) -> None:
            self.writes.append(password)
            real_set(service, username, password)

        def get_password(service: str, username: str):
            self.reads += 1
            return real_get(service, username)

        monkeypatch.setattr(keyring, "set_password", set_password)
        monkeypatch.setattr(keyring, "get_password", get_password)


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """An installation paced at a millisecond, so no test sleeps out the gate."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return config.from_dict(valid_data(root, provider={"min_interval_s": 0.001}))


def use(monkeypatch, factory: Factory) -> Factory:
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", factory)
    return factory


def record(session: dict | None = None) -> None:
    secrets.set_json(SESSION, dict(session or STORED))


def quick_gate() -> provider_gate.Gate:
    return provider_gate.Gate(provider_gate.GateSettings(min_interval_s=0.001))


def refused_with(excinfo) -> tuple[str, Any]:
    return excinfo.value.cause.reason, excinfo.value.cause.remediation.remedy


# ═══════════════════════════════════════════════════════════════════════════
# 1. The write back
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unchanged_session_makes_no_keychain_write(monkeypatch):
    use(monkeypatch, Factory())
    record()
    keychain = Keychain(monkeypatch)

    provider_session.client_session(gate=quick_gate())

    assert keychain.writes == []
    assert secrets.get_json(SESSION) == STORED


def test_a_refreshed_session_is_written_once_through_the_index(monkeypatch):
    use(monkeypatch, Factory(refresh_to="FAKE-value-3"))
    record()
    keychain = Keychain(monkeypatch)
    recorded: list[str] = []
    real_record = secrets._record_name
    monkeypatch.setattr(secrets, "_record_name", lambda name: (recorded.append(name), real_record(name)))

    provider_session.client_session(gate=quick_gate())

    assert len(keychain.writes) == 1
    assert secrets.get_json(SESSION) == dict(STORED, access_token="FAKE-value-3")
    assert recorded == [str(SESSION)]
    assert str(SESSION) in secrets.recorded()


def test_write_back_compares_the_value_and_not_the_spelling(tmp_path):
    """Equal values are equal whatever the file's key order or spacing; a
    value that changed type is not, since the keychain would then hold other
    bytes than the ones read."""
    record()
    path = tmp_path / "session.json"
    path.write_text('{"expiry_time": 946684800.0,  "refresh_token": "FAKE-value-2", '
                    '"access_token": "FAKE-value-1", "token_type": "Bearer"}')
    assert provider_session.write_back(SESSION, path, stored=dict(STORED)) is False

    path.write_text('{"expiry_time": 946684800, "refresh_token": "FAKE-value-2", '
                    '"access_token": "FAKE-value-1", "token_type": "Bearer"}')
    assert provider_session.write_back(SESSION, path, stored=dict(STORED)) is True
    assert secrets.get_json(SESSION)["expiry_time"] == 946684800


def test_a_write_back_with_nothing_to_compare_against_writes_as_before(tmp_path):
    record()
    path = tmp_path / "session.json"
    path.write_text('{"access_token": "FAKE-value-1"}')
    assert provider_session.write_back(SESSION, path) is True


def test_an_unchanged_toml_session_is_not_written_back(monkeypatch):
    """The alternative tool's encoding takes the same comparison."""
    record()
    keychain = Keychain(monkeypatch)

    with provider_session.materialised_session(filename="config.toml", codec=provider_session.TOML):
        pass

    assert keychain.writes == []


def test_a_session_the_tool_changed_is_written_back_from_the_scope(monkeypatch):
    record()
    keychain = Keychain(monkeypatch)

    with provider_session.materialised_session() as scope:
        scope.path.write_text('{"access_token": "FAKE-value-9", "token_type": "Bearer"}')

    assert len(keychain.writes) == 1
    assert secrets.get_json(SESSION) == {"access_token": "FAKE-value-9", "token_type": "Bearer"}


# ═══════════════════════════════════════════════════════════════════════════
# 2. One validation per process
# ═══════════════════════════════════════════════════════════════════════════


def test_a_process_resolving_both_seams_validates_the_session_once(cfg, monkeypatch):
    factory = use(monkeypatch, Factory())
    record()
    keychain = Keychain(monkeypatch)

    first = catalogue.resolve(cfg)
    second = catalogue.resolve(cfg)
    remote = account.resolve(cfg)

    assert account.resolve(cfg) is remote
    assert len(factory.built) == 1
    assert factory.requests == LOGIN
    assert keychain.writes == []
    # One read for the login, one per reuse to see the session is still held.
    assert keychain.reads == 3
    assert isinstance(first, tidal_catalogue.TidalCatalogue)
    assert isinstance(remote, tidal_account.TidalAccount)
    assert first is not second
    assert first._session is second._session is factory.built[0]


def test_the_surveys_drive_logs_in_once_and_writes_nothing(cfg, monkeypatch):
    """The card's reproduction: catalogue twice and account twice."""
    factory = use(monkeypatch, Factory())
    record()
    keychain = Keychain(monkeypatch)

    catalogue.resolve(cfg)
    catalogue.resolve(cfg)
    account.resolve(cfg)
    account.resolve(cfg)

    assert len(factory.built) == 1
    assert len(factory.requests) == 2
    assert keychain.writes == []


def test_the_app_client_is_held_with_the_session_and_asks_one_token(cfg, monkeypatch):
    """R-1218: two openers in one process built two app clients and asked the
    token service twice."""
    use(monkeypatch, Factory(country_code="GB"))
    record()
    record_app()
    transport = AppTransport()
    monkeypatch.setattr(provider_session, "CATALOGUE_TRANSPORT_FACTORY", lambda: transport)

    found = catalogue.resolve(cfg)
    remote = account.resolve(cfg)

    assert isinstance(found._lookups, catalogue_api.AppCatalogue)
    assert remote._lookups is found._lookups
    found._lookups.get_tracks_by_isrc("GBAAA2400001")
    remote._lookups.get_tracks_by_isrc("GBAAA2400001")
    tokens = [one for one in transport.sent if one["url"] == catalogue_api.TOKEN_URL]
    assert len(tokens) == 1


def test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve(cfg, monkeypatch):
    use(monkeypatch, Factory(country_code="GB"))
    record()
    monkeypatch.setattr(provider_session, "CATALOGUE_TRANSPORT_FACTORY", AppTransport)

    assert catalogue.resolve(cfg)._lookups is not None
    assert not isinstance(catalogue.resolve(cfg)._lookups, catalogue_api.AppCatalogue)
    record_app()
    assert isinstance(catalogue.resolve(cfg)._lookups, catalogue_api.AppCatalogue)


def test_a_lost_app_value_is_noted_on_every_resolve_that_falls_back(cfg, monkeypatch):
    """The spend line's note is cleared per command, so a reuse must make it again."""
    use(monkeypatch, Factory(country_code="GB"))
    record()
    record_app()
    keyring.delete_password(secrets.SERVICE, str(catalogue_api.CREDENTIALS[0]))
    monkeypatch.setattr(provider_session, "CATALOGUE_TRANSPORT_FACTORY", AppTransport)
    provider_gate._APP_LOST.clear()

    catalogue.resolve(cfg)
    assert provider_gate.app_lost() == (str(catalogue_api.CREDENTIALS[0]),)
    provider_gate._APP_LOST.clear()
    catalogue.resolve(cfg)
    assert provider_gate.app_lost() == (str(catalogue_api.CREDENTIALS[0]),)
    provider_gate._APP_LOST.clear()


def test_other_gate_settings_open_a_session_of_their_own(cfg, tmp_path, monkeypatch):
    factory = use(monkeypatch, Factory())
    record()
    slower = config.from_dict(
        valid_data(tmp_path / "library", provider={"min_interval_s": 0.002})
    )

    catalogue.resolve(cfg)
    found = catalogue.resolve(slower)

    assert len(factory.built) == 2
    assert found._session.request_session._cratekit_gate.settings.min_interval_s == 0.002


# ═══════════════════════════════════════════════════════════════════════════
# 3. A refused session is forgotten for every seam
# ═══════════════════════════════════════════════════════════════════════════


def test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again(
    cfg, monkeypatch
):
    factory = use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)
    remote = account.resolve(cfg)

    cause = account.provider_failure(HTTPFailure(Answer(401)), "heart a track")

    assert cause.cause.reason == "credential-missing"
    found = catalogue.resolve(cfg)
    assert len(factory.built) == 2
    assert found._session is factory.built[1]
    assert account.resolve(cfg) is not remote
    assert len(factory.built) == 2


@pytest.mark.parametrize("status", [401, 403])
def test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams(
    cfg, monkeypatch, status
):
    factory = use(monkeypatch, Factory())
    record()
    found = catalogue.resolve(cfg)
    remote = account.resolve(cfg)

    found._session.request_session.status = status
    assert found._session.read() == status

    assert catalogue.resolve(cfg)._session is factory.built[1]
    assert account.resolve(cfg) is not remote
    assert len(factory.built) == 2


def test_a_refusal_the_transport_raises_drops_the_client_too(cfg, monkeypatch):
    """A transport that raises its refusal rather than answering it, with the
    answer on the exception as the provider library's HTTP error carries it."""
    factory = use(monkeypatch, Factory())
    record()
    found = catalogue.resolve(cfg)

    found._session.request_session.raises = 401
    with pytest.raises(HTTPFailure):
        found._session.read()

    assert catalogue.resolve(cfg)._session is factory.built[1]


def test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one(cfg, monkeypatch):
    """The first client, still in an adapter's hands after a replaced session
    was logged in afresh, meets a 401: the newer session is not the one refused."""
    factory = use(monkeypatch, Factory())
    record()
    first = catalogue.resolve(cfg)
    record(dict(STORED, access_token="FAKE-value-7"))
    second = catalogue.resolve(cfg)

    first._session.request_session.status = 401
    first._session.read()

    assert catalogue.resolve(cfg)._session is second._session
    assert len(factory.built) == 2


def test_an_answer_that_judges_no_session_keeps_the_client(cfg, monkeypatch):
    factory = use(monkeypatch, Factory())
    record()
    found = catalogue.resolve(cfg)

    for status in (404, 429, 500):
        found._session.request_session.status = status
        found._session.read()

    found._session.request_session.status = 200
    assert catalogue.resolve(cfg)._session is factory.built[0]
    assert len(factory.built) == 1


def test_a_session_the_index_no_longer_records_is_refused_by_both_seams(cfg, monkeypatch):
    factory = use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)
    account.resolve(cfg)
    monkeypatch.setattr(secrets, "exists", lambda name: False)

    for seam in (catalogue, account):
        with pytest.raises(CratekitError) as excinfo:
            seam.resolve(cfg)
        assert refused_with(excinfo) == ("credential-missing", Remedy.AUTHENTICATE_PROVIDER)
    assert len(factory.requests) == 2


def test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused(cfg, monkeypatch):
    """Deleted through the operating system's own keychain, so the index still
    names it: the reuse reads the keychain and finds nothing."""
    factory = use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)
    keyring.delete_password(secrets.SERVICE, str(SESSION))

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    assert refused_with(excinfo) == ("credential-missing", Remedy.REAUTHENTICATE_PROVIDER)
    assert len(factory.requests) == 2
    assert provider_session.held() is None


def test_a_keychain_that_cannot_be_read_on_a_reuse_says_repair_it(cfg, monkeypatch):
    use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)

    def broken(service: str, username: str):
        raise RuntimeError("no backend")

    monkeypatch.setattr(keyring, "get_password", broken)
    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    assert refused_with(excinfo) == ("credential-missing", Remedy.REPAIR_CREDENTIAL_STORE)


def test_a_session_replaced_after_an_open_is_logged_in_afresh_from_the_new_value(
    cfg, monkeypatch
):
    factory = use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)
    record(dict(STORED, access_token="FAKE-value-7"))

    found = catalogue.resolve(cfg)

    assert len(factory.built) == 2
    assert found._session.logged_in_with == "FAKE-value-7"


def test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client(
    cfg, monkeypatch
):
    """Round one's R2: a session recorded afresh whose login fails must not
    leave the account's adapter over the session it replaced."""
    factory = use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)
    account.resolve(cfg)
    record(dict(STORED, access_token="FAKE-value-7"))
    factory.client = {"status": 401}

    for seam in (catalogue, account):
        with pytest.raises(CratekitError) as excinfo:
            seam.resolve(cfg)
        assert refused_with(excinfo) == ("credential-missing", Remedy.REAUTHENTICATE_PROVIDER)
    assert provider_session.held() is None
    assert len(factory.built) == 3


def test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since(
    cfg, monkeypatch
):
    """Round one's R4: the account's adapter over a replaced session meets a
    401, and the session the catalogue logged in since stays held."""
    factory = use(monkeypatch, Factory())
    record()
    account.resolve(cfg)
    record(dict(STORED, access_token="FAKE-value-7"))
    newer = catalogue.resolve(cfg)._session

    account.provider_failure(HTTPFailure(Answer(401)), "heart a track")

    assert catalogue.resolve(cfg)._session is newer
    assert account.resolve(cfg)._session is newer
    assert len(factory.built) == 2


def test_the_held_sessions_repr_carries_no_token(cfg, monkeypatch):
    use(monkeypatch, Factory())
    record()
    catalogue.resolve(cfg)

    shown = repr(provider_session.held())

    assert "FAKE-value-1" not in shown
    assert "FAKE-value-2" not in shown


def test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh(cfg, monkeypatch):
    factory = use(monkeypatch, Factory(refresh_to="FAKE-value-3"))
    record()
    keychain = Keychain(monkeypatch)

    catalogue.resolve(cfg)
    catalogue.resolve(cfg)

    assert len(factory.built) == 1
    assert len(keychain.writes) == 1
    assert secrets.get_json(SESSION)["access_token"] == "FAKE-value-3"


# ═══════════════════════════════════════════════════════════════════════════
# 4. The gate, and a login that failed
# ═══════════════════════════════════════════════════════════════════════════


def test_a_reuse_inside_a_cooldown_refuses_without_a_call(cfg, monkeypatch):
    factory = use(monkeypatch, Factory())
    record()
    found = catalogue.resolve(cfg)
    gate = found._session.request_session._cratekit_gate
    import time

    now = time.time()
    gate._write(provider_gate._State(tripped_at=now, lifts_at=now + 900))

    for seam in (catalogue, account):
        with pytest.raises(CratekitError) as excinfo:
            seam.resolve(cfg)
        assert excinfo.value.cause.reason == provider_gate.COOLDOWN
    assert factory.requests == LOGIN


@pytest.mark.parametrize(
    ("status", "reason"),
    [(401, "credential-missing"), (503, "unavailable-transient")],
    ids=["rejected", "unreachable"],
)
def test_a_login_that_failed_holds_nothing_and_is_asked_again(cfg, monkeypatch, status, reason):
    factory = use(monkeypatch, Factory(status=status))
    record()

    for _ in range(2):
        with pytest.raises(CratekitError) as excinfo:
            catalogue.resolve(cfg)
        assert excinfo.value.cause.reason == reason
    assert len(factory.built) == 2
    assert provider_session.held() is None


def test_forget_drops_the_held_session():
    provider_session.forget()
    assert provider_session.held() is None
