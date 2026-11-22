"""R-1305. A rejected session whose answer body is not JSON still asks for a login.

The client decodes an error body inside its own handler of the HTTP error, so a
401 or 403 carrying a gateway's page surfaces as a decode error with the HTTP
error as its context, three links down. Every failure here is raised by the
installed client's own handler (``tests.provider_answers``). The two readers:
``account.provider_failure`` after login, ``provider_session.client_session`` at it.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from cratekit.acquire import provider_session
from cratekit.core import secrets
from cratekit.core.cause import CratekitError, Scope
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import account
from tests.provider_answers import HTML, JSON_BODY, client_failure
from tests.test_outbound_tidal_account import STORED, FakeClient, adapter, use_client
from tests.test_outbound_tidal_account import installed as installed  # noqa: PLC0414 - fixture

#: Answers that judge the session, each with a body the client can and cannot read.
REJECTED = [
    pytest.param(status, body, id=f"{status}-{kind}")
    for kind, body in (("html", HTML), ("empty", b""), ("json", JSON_BODY))
    for status in (401, 403)
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

    Each read of a link is counted, and past a bound far above any honest walk's
    the read raises, once, so an unguarded walk fails rather than hanging the
    suite. The links are the interpreter's own fields, set through the base
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

    The shape ``core.cause._chain`` refuses to read context over. The refusal is
    raised from the 401 as the adapter's ``_call`` raises it, so the 401 is
    reachable under it and only the walk's refusal limit keeps it out.
    """
    rejected = client_failure(401, HTML)
    refusal = account.provider_failure(rejected, "heart the track 8")
    assert refusal.cause.reason == "credential-missing"
    try:
        raise refusal from rejected
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


def login_with(monkeypatch, failure: Exception) -> FakeClient:
    client = use_client(monkeypatch, FakeClient(login_raises=failure))
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))
    return client


def heart_refused(status: int, body: bytes):
    """The cause of a heart whose two attempts the provider answers ``status`` with ``body``."""
    client = FakeClient()
    client.user.favorites.fail = [client_failure(status, body), client_failure(status, body)]
    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")
    return excinfo.value.cause


def reason_of(failure: BaseException) -> str:
    return account.provider_failure(failure, "heart the track 8").cause.reason


# ── 0. the chain the client makes, measured, so the tests below test that one ──


def test_a_401_whose_body_is_not_json_carries_its_status_only_as_context():
    """If the client ever declares the cause, this test changes, and R-1305 with it."""
    links = []
    current: BaseException | None = client_failure(401, HTML)
    while current is not None:
        links.append(current)
        assert current.__cause__ is None
        current = current.__context__
    statuses = [getattr(getattr(one, "response", None), "status_code", None) for one in links]
    assert statuses[0] is None
    assert statuses[-1] == 401
    assert len(links) > 2


# ── 1. a call after login: account.provider_failure ─────────────────────────


@pytest.mark.parametrize(("status", "body"), REJECTED)
def test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body(status, body):
    cause = heart_refused(status, body)
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy == Remedy.REAUTHENTICATE_PROVIDER
    assert cause.scope is Scope.ITEM


@pytest.mark.parametrize(("status", "body"), UNAVAILABLE)
def test_a_server_error_mid_sweep_is_still_a_wait_whatever_the_body(status, body):
    cause = heart_refused(status, body)
    assert cause.reason == "unavailable-transient"
    assert cause.remediation.remedy == Remedy.RETRY_LATER


def test_a_rejection_whose_body_is_not_json_drops_the_held_account(installed, monkeypatch):
    login_with(monkeypatch, None)
    held = account.resolve(installed)
    account.provider_failure(client_failure(401, HTML), "heart the track 8")
    assert account.resolve(installed) is not held


def test_a_server_error_whose_body_is_not_json_keeps_the_held_account(installed, monkeypatch):
    login_with(monkeypatch, None)
    held = account.resolve(installed)
    account.provider_failure(client_failure(503, HTML), "heart the track 8")
    assert account.resolve(installed) is held


def test_a_cyclic_chain_after_login_ends_and_is_a_wait():
    assert reason_of(cyclic()) == "unavailable-transient"


def test_an_outage_met_while_handling_a_rejected_session_is_a_wait_not_a_login():
    """A context link into a refusal the product raised is not followed."""
    assert reason_of(inside_a_refusal(lambda: client_failure(503, HTML))) == "unavailable-transient"


def test_an_authentication_error_reached_only_as_context_is_not_a_rejected_session():
    """A status is the provider's word; a name reached only as context is a guess."""
    assert reason_of(auth_error_as_context()) == "unavailable-transient"


# ── 2. the login itself: provider_session.client_session ────────────────────


@pytest.mark.parametrize(("status", "body"), [*REJECTED, pytest.param(400, HTML, id="400-html")])
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
    assert excinfo.value.cause.reason == "credential-missing"
    assert excinfo.value.cause.remediation.remedy == Remedy.REAUTHENTICATE_PROVIDER


@pytest.mark.parametrize(
    "failure",
    [
        pytest.param(cyclic, id="cyclic"),
        pytest.param(lambda: inside_a_refusal(lambda: client_failure(503, HTML)), id="outage"),
        pytest.param(auth_error_as_context, id="context"),
    ],
)
def test_a_login_failure_that_is_no_rejection_is_a_wait(monkeypatch, failure):
    """A cyclic chain, an outage met while a rejection was handled, and an authentication
    error reached only as context: each a wait at login, as after it."""
    login_with(monkeypatch, failure())
    with pytest.raises(provider_session.ProviderUnavailable):
        provider_session.client_session()


# ── 3. the walk itself ──────────────────────────────────────────────────────


def test_the_walk_reaches_every_link_once_with_the_declared_chain_first():
    """Declared causes first and marked so; then context, and causes off it, once each."""
    deepest = ValueError("deepest, the cause of a context")
    handled = ValueError("handled, a context")
    handled.__cause__ = deepest
    inner = ValueError("inner, declared")
    inner.__context__ = handled
    outer = ValueError("outer, the failure")
    outer.__cause__ = inner
    outer.__context__ = inner
    assert [(str(link), declared) for link, declared in provider_session.failure_links(outer)] == [
        ("outer, the failure", True),
        ("inner, declared", True),
        ("handled, a context", False),
        ("deepest, the cause of a context", False),
    ]


def test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login(
    monkeypatch,
):
    """The context to follow can hang off a declared cause, not only the failure itself."""
    try:
        raise RuntimeError("the client's own error") from client_failure(401, HTML)
    except RuntimeError as exc:
        wrapped = exc
    assert reason_of(wrapped) == "credential-missing"
    login_with(monkeypatch, wrapped)
    with pytest.raises(provider_session.AdapterAuthFailed):
        provider_session.client_session()
