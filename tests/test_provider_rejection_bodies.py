"""R-1305. A rejected session whose answer body is not JSON still asks for a login.

Found at round two of U220's review. The provider client decodes an error
answer's body inside its own handler of the HTTP error, so a 401 or a 403 whose
body is a gateway's page surfaces as a decode error with the HTTP error as its
context, three links down, and no declared cause. Both readers of a rejected
session walked the declared cause chain alone, so that person was told the
provider was unavailable and to wait, for an outage that was not happening.

Every failure here is raised by the installed client's own request handler
(``tests.provider_answers``), not built by hand, so the chain is the client's.
The two readers: ``account.provider_failure`` for a call after login, and
``provider_session.client_session`` for the login itself.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from cratekit.acquire import provider_session
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, Scope
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import account, source
from tests.provider_answers import HTML, JSON_BODY, client_failure
from tests.test_config import valid_data
from tests.test_outbound_tidal_account import STORED, FakeClient, adapter

#: Answers that judge the session, each with a body the client can and cannot read.
REJECTED = [
    pytest.param(401, HTML, id="401-html"),
    pytest.param(403, HTML, id="403-html"),
    pytest.param(401, b"", id="401-empty"),
    pytest.param(403, b"", id="403-empty"),
    pytest.param(401, JSON_BODY, id="401-json"),
    pytest.param(403, JSON_BODY, id="403-json"),
]

#: Answers that say nothing about the session, whatever their body.
UNAVAILABLE = [
    pytest.param(503, HTML, id="503-html"),
    pytest.param(502, HTML, id="502-html"),
    pytest.param(503, b"", id="503-empty"),
    pytest.param(500, JSON_BODY, id="500-json"),
]


class AuthenticationError(Exception):
    """Named as the provider client names its own authentication failure."""


class Looping(ValueError):
    """A failure whose links lead back to it, and that will not be walked forever.

    A walk with no cycle guard does not raise, it spins, and a spinning test
    hangs the suite and every mutation row after it. So each read of a link
    through Python is counted, and past a bound far above any honest walk's
    the read raises instead, once, so an unguarded walk fails in milliseconds
    and the report that formats the failure can still read the chain. The
    links themselves are the interpreter's own fields, set through the base
    descriptors, so the chain is a real one.
    """

    #: Reads of a link past which the walk is taken not to end.
    BOUND = 1000

    def __init__(self, name: str, budget: dict[str, int]) -> None:
        super().__init__(name)
        #: Shared by every failure in one cycle: reads so far, and whether it tripped.
        self.budget = budget

    def _read(self, link) -> BaseException | None:
        self.budget["reads"] += 1
        if self.budget["reads"] > self.BOUND and not self.budget["tripped"]:
            self.budget["tripped"] = 1
            raise AssertionError(f"the walk read past {self.BOUND} links: it does not end")
        return link.__get__(self)

    @property
    def __cause__(self) -> BaseException | None:
        return self._read(BaseException.__cause__)

    @__cause__.setter
    def __cause__(self, value: BaseException | None) -> None:
        BaseException.__cause__.__set__(self, value)

    @property
    def __context__(self) -> BaseException | None:
        return self._read(BaseException.__context__)

    @__context__.setter
    def __context__(self, value: BaseException | None) -> None:
        BaseException.__context__.__set__(self, value)


def cyclic() -> Looping:
    """A failure whose cause and context lead back to it, carrying no status."""
    budget = {"reads": 0, "tripped": 0}
    first = Looping("first", budget)
    second = Looping("second", budget)
    first.__cause__ = second
    second.__cause__ = first
    second.__context__ = first
    first.__context__ = second
    return first


def inside_a_refusal(later: Callable[[], Exception]) -> Exception:
    """``later``'s failure, raised while a rejected session's refusal is being handled.

    The shape ``core.cause._chain`` refuses to read context over: a handler
    that caught a refusal and then met an unrelated failure.
    """
    refusal = account.provider_failure(client_failure(401, HTML), "heart the track 8")
    assert refusal.cause.reason == "credential-missing"
    try:
        raise refusal
    except CratekitError:
        return later()


def auth_error_as_context() -> Exception:
    """A connection reset raised while the client's authentication error was handled."""
    try:
        raise AuthenticationError("expired")
    except AuthenticationError:
        try:
            raise ConnectionError("connection reset")
        except ConnectionError as exc:
            return exc


@pytest.fixture
def installed(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(valid_data(root, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    source.forget_libraries()
    yield built
    source.forget_libraries()


def login_with(monkeypatch, failure: Exception) -> FakeClient:
    client = FakeClient(login_raises=failure)
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))
    return client


# ═══════════════════════════════════════════════════════════════════════════
# 0. The chain the client makes, measured, so the tests below test that one
# ═══════════════════════════════════════════════════════════════════════════


def test_a_401_whose_body_is_not_json_carries_its_status_only_as_context():
    """If the client ever declares the cause, this test changes, and R-1305 with it."""
    failure = client_failure(401, HTML)

    links = []
    current: BaseException | None = failure
    while current is not None:
        links.append(current)
        assert current.__cause__ is None
        current = current.__context__

    statuses = [getattr(getattr(one, "response", None), "status_code", None) for one in links]
    assert statuses[0] is None
    assert statuses[-1] == 401
    assert len(links) > 2


# ═══════════════════════════════════════════════════════════════════════════
# 1. A call after login: account.provider_failure
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(("status", "body"), REJECTED)
def test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body(status, body):
    client = FakeClient()
    client.user.favorites.fail = [client_failure(status, body), client_failure(status, body)]

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")

    cause = excinfo.value.cause
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy == Remedy.REAUTHENTICATE_PROVIDER
    assert cause.scope is Scope.ITEM


@pytest.mark.parametrize(("status", "body"), UNAVAILABLE)
def test_a_server_error_mid_sweep_is_still_a_wait_whatever_the_body(status, body):
    client = FakeClient()
    client.user.favorites.fail = [client_failure(status, body), client_failure(status, body)]

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")

    cause = excinfo.value.cause
    assert cause.reason == "unavailable-transient"
    assert cause.remediation.remedy == Remedy.RETRY_LATER


def test_a_rejection_whose_body_is_not_json_drops_the_held_account(installed, monkeypatch):
    client = FakeClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))
    held = account.resolve(installed)

    account.provider_failure(client_failure(401, HTML), "heart the track 8")

    assert account.resolve(installed) is not held


def test_a_server_error_whose_body_is_not_json_keeps_the_held_account(installed, monkeypatch):
    client = FakeClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))
    held = account.resolve(installed)

    account.provider_failure(client_failure(503, HTML), "heart the track 8")

    assert account.resolve(installed) is held


def test_a_cyclic_chain_after_login_ends_and_is_a_wait():
    refusal = account.provider_failure(cyclic(), "heart the track 8")

    assert refusal.cause.reason == "unavailable-transient"


def test_an_outage_met_while_handling_a_rejected_session_is_a_wait_not_a_login():
    """A context link into a refusal the product raised is not followed."""
    later = inside_a_refusal(lambda: client_failure(503, HTML))

    assert account.provider_failure(later, "heart the track 9").cause.reason == (
        "unavailable-transient"
    )


def test_an_authentication_error_reached_only_as_context_is_not_a_rejected_session():
    """A status is the provider's word; a name reached only as context is a guess."""
    assert account.provider_failure(auth_error_as_context(), "heart the track 8").cause.reason == (
        "unavailable-transient"
    )


# ═══════════════════════════════════════════════════════════════════════════
# 2. The login itself: provider_session.client_session
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    ("status", "body"), [*REJECTED, pytest.param(400, HTML, id="400-html")]
)
def test_a_login_rejected_whatever_the_body_asks_for_a_login(monkeypatch, status, body):
    login_with(monkeypatch, client_failure(status, body))

    with pytest.raises(provider_session.AdapterAuthFailed):
        provider_session.client_session()


@pytest.mark.parametrize(("status", "body"), UNAVAILABLE)
def test_a_login_the_server_failed_whatever_the_body_is_a_wait(monkeypatch, status, body):
    login_with(monkeypatch, client_failure(status, body))

    with pytest.raises(provider_session.ProviderUnavailable):
        provider_session.client_session()

    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == STORED


def test_a_login_rejected_with_a_page_tells_the_person_to_log_in_again(installed, monkeypatch):
    """What a person reads: the account's refusal, not a wait."""
    login_with(monkeypatch, client_failure(401, HTML))

    with pytest.raises(CratekitError) as excinfo:
        account.resolve(installed)

    cause = excinfo.value.cause
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy == Remedy.REAUTHENTICATE_PROVIDER


def test_a_cyclic_chain_at_login_ends_and_is_a_wait(monkeypatch):
    login_with(monkeypatch, cyclic())

    with pytest.raises(provider_session.ProviderUnavailable):
        provider_session.client_session()


def test_a_login_outage_met_while_handling_a_rejected_session_is_a_wait(monkeypatch):
    login_with(monkeypatch, inside_a_refusal(lambda: client_failure(503, HTML)))

    with pytest.raises(provider_session.ProviderUnavailable):
        provider_session.client_session()


def test_a_login_authentication_error_reached_only_as_context_is_a_wait(monkeypatch):
    login_with(monkeypatch, auth_error_as_context())

    with pytest.raises(provider_session.ProviderUnavailable):
        provider_session.client_session()
