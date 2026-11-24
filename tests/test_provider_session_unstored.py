"""R-1694: a login whose refreshed token the keychain cannot take goes on, and the verb
says so with one ``provider-session-not-stored`` warning, as a download does (U274).

Nothing else is caught: an unchanged session warns nothing, and a rejected login, a
capture defect and a scope asking no tolerance still raise.
"""

from __future__ import annotations

import json
from pathlib import Path

import keyring
import pytest
from keyring.backends import fail

from cratekit.acquire import provider_session, vendored
from cratekit.acquire.adapter import AdapterAuthFailed
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, refuse
from cratekit.label import catalogue, tidal_catalogue
from cratekit.modules.outbound import account
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_provider_gate import _config_data
from tests.test_provider_session_hold import STORED, Factory, Keychain, quick_gate, record

SESSION = secrets.Credential.PROVIDER_SESSION
REFRESHED = "FAKE-value-3"
HARVEST = ["label", "harvest", "https://example.invalid/playlist/harvest"]


def no_keychain(monkeypatch, factory: Factory | None = None) -> Factory | None:
    """The opt in for a machine with no keychain: keyring's fail backend refuses a write."""
    if factory is not None:
        use(monkeypatch, factory)
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv(secrets.ENV_CREDENTIAL_PREFIX + "PROVIDER_SESSION", json.dumps(STORED))
    backend = fail.Keyring()
    monkeypatch.setattr(keyring, "set_password", backend.set_password)
    monkeypatch.setattr(keyring, "get_password", backend.get_password)
    return factory


def use(monkeypatch, factory: Factory) -> Factory:
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", factory)
    return factory


@pytest.fixture
def noted():
    """The classes the process notes as not stored from the start of the test on."""
    before = len(provider_session.unstored())
    return lambda: provider_session.unstored()[before:]


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """An installation paced at a millisecond, so no test sleeps out the gate."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return config.from_dict(valid_data(root, provider={"min_interval_s": 0.001}))


@pytest.fixture
def installed(tmp_path, monkeypatch) -> config.Config:
    """A machine the real dispatcher can load, with every module on."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True, exist_ok=True)
    (root / "db").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 0.001}))
    config.save(built)
    config.reset_cache()
    return built


def not_stored(envelope: dict) -> list[str]:
    return [
        w["message"]
        for w in envelope.get("warnings", ())
        if w.get("code") == provider_session.SESSION_NOT_STORED
    ]


def test_a_refreshed_login_the_keychain_cannot_take_returns_the_client(monkeypatch, noted):
    factory = no_keychain(monkeypatch, Factory(refresh_to=REFRESHED))
    client = provider_session.client_session(gate=quick_gate())
    assert client is factory.built[0]
    assert client.access_token == REFRESHED
    assert noted() == ("CredentialBackendUnavailable",)
    assert secrets.get_json(SESSION) == STORED


def test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again(
    cfg, monkeypatch, noted
):
    """The keychain still holds the opened session, so the next resolve reuses the client."""
    factory = no_keychain(monkeypatch, Factory(refresh_to=REFRESHED))
    catalogue.resolve(cfg)
    catalogue.resolve(cfg)
    account.resolve(cfg)
    assert len(factory.built) == 1
    assert noted() == ("CredentialBackendUnavailable",)
    held = provider_session.held()
    assert held is not None
    assert held.blob == json.dumps(STORED, sort_keys=True)


def test_an_unchanged_session_on_the_opt_in_writes_nothing_and_notes_nothing(monkeypatch, noted):
    no_keychain(monkeypatch, Factory())
    provider_session.client_session(gate=quick_gate())
    assert noted() == ()


def test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted(monkeypatch, noted):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()

    def unreadable(name):
        raise refuse("credential-index-unreadable", "the credential index could not be read")

    monkeypatch.setattr(secrets, "_record_name", unreadable)

    client = provider_session.client_session(gate=quick_gate())

    assert client.access_token == REFRESHED
    assert noted() == ("CratekitError",)


def test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched(
    monkeypatch, noted
):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()
    keychain = Keychain(monkeypatch)

    def unlockable(action="update"):
        raise secrets.CredentialIndexUnusable("the index could not be locked")

    monkeypatch.setattr(secrets, "_index_locked", unlockable)

    provider_session.client_session(gate=quick_gate())

    assert keychain.writes == []
    assert noted() == ("CredentialIndexUnusable",)
    assert secrets.get_json(SESSION) == STORED


def test_a_token_file_that_cannot_take_the_refresh_is_noted(monkeypatch, noted):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()
    keychain = Keychain(monkeypatch)
    real = config.atomic_write_bytes

    def full(data, path, **kwargs):
        if json.loads(data).get("access_token") == REFRESHED:
            raise OSError(28, "No space left on device")
        return real(data, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", full)

    client = provider_session.client_session(gate=quick_gate())

    assert client.access_token == REFRESHED
    assert keychain.writes == []
    assert noted() == ("OSError",)


def test_an_unchanged_session_never_rewrites_the_token_file(monkeypatch, noted):
    """A session with nothing to store never reports a file that cannot be written."""
    use(monkeypatch, Factory())
    record()
    real = config.atomic_write_bytes
    writes: list[Path] = []

    def counted(data, path, **kwargs):
        if Path(path).parent.name.startswith(provider_session.SESSION_PREFIX):
            writes.append(Path(path))
        return real(data, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", counted)

    provider_session.client_session(gate=quick_gate())

    assert len(writes) == 1, "only the materialised file, never a rewrite of it"
    assert noted() == ()


def test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns(
    installed, monkeypatch
):
    """Through the real dispatcher: the verb's own answer stands and the warning rides beside it."""
    no_keychain(monkeypatch, Factory())
    _, unchanged = drive(HARVEST)
    assert not_stored(unchanged) == []
    provider_session.forget()

    use(monkeypatch, Factory(refresh_to=REFRESHED))
    _, refreshed = drive(HARVEST)

    assert refreshed["cause"] == unchanged["cause"], refreshed
    said = not_stored(refreshed)
    assert len(said) == 1, refreshed["warnings"]
    assert "CredentialBackendUnavailable" in said[0]
    assert "next run logs in again" in said[0]
    shown = json.dumps(refreshed)
    for token in ("FAKE-value-1", "FAKE-value-2", REFRESHED):
        assert token not in shown


def test_the_warning_is_this_verbs_alone(installed, monkeypatch):
    """A note an earlier verb in the same process made is not the next one's."""
    no_keychain(monkeypatch, Factory(refresh_to=REFRESHED))
    _, first = drive(HARVEST)
    assert len(not_stored(first)) == 1

    _, second = drive(HARVEST)

    assert not_stored(second) == [], "the held client was reused and nothing failed again"


def test_the_drives_warning_keeps_its_code():
    assert vendored.SESSION_NOT_STORED == provider_session.SESSION_NOT_STORED
    assert provider_session.SESSION_NOT_STORED == "provider-session-not-stored"


def test_a_rejected_login_on_the_opt_in_still_raises_the_rejection_and_holds_nothing(
    cfg, monkeypatch, noted
):
    no_keychain(monkeypatch, Factory(status=401, refresh_to=REFRESHED))
    with pytest.raises(AdapterAuthFailed):
        provider_session.client_session(gate=quick_gate())
    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)
    assert excinfo.value.cause.reason == "credential-missing"
    assert provider_session.held() is None
    assert noted() == ()


class Expired(Factory):
    """A login the client answers False to: an expired session."""

    def __call__(self):
        client = super().__call__()
        client.load_oauth_session = lambda *a, **k: False
        return client


class Unencodable(Factory):
    """A login that leaves a field the session file cannot hold."""

    def __call__(self):
        client = super().__call__()
        real = client.load_oauth_session

        def login(*args, **kwargs):
            answered = real(*args, **kwargs)
            client.refresh_token = object()
            return answered

        client.load_oauth_session = login
        return client


@pytest.mark.parametrize(
    ("factory", "raised"),
    [
        pytest.param(Expired, AdapterAuthFailed,
                     id="a-session-the-provider-no-longer-accepts-still-raises"),
        pytest.param(Unencodable, TypeError, id="a-defect-in-the-capture-still-raises"),
    ],
)
def test_a_login_that_is_no_store_failure_still_raises_on_the_opt_in(
    monkeypatch, noted, factory, raised
):
    """An expired session is never reused, and a capture defect is never a warning."""
    no_keychain(monkeypatch, factory())
    with pytest.raises(raised):
        provider_session.client_session(gate=quick_gate())
    assert noted() == ()


def test_a_defect_in_the_write_back_still_raises(monkeypatch, noted):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()

    def broken(name, payload):
        raise RuntimeError("a defect in the write")

    monkeypatch.setattr(secrets, "set_json", broken)
    with pytest.raises(RuntimeError):
        provider_session.client_session(gate=quick_gate())
    assert noted() == ()


def test_a_scope_that_asked_for_no_tolerance_still_raises_its_write_back_failure(
    monkeypatch, tmp_path
):
    """Without the callback, a write back the keychain refuses raises as before."""
    no_keychain(monkeypatch)

    with pytest.raises(secrets.CredentialBackendUnavailable):
        with provider_session.materialised_session() as scope:
            payload = json.loads(scope.path.read_text(encoding="utf-8"))
            payload["access_token"] = REFRESHED
            scope.path.write_text(json.dumps(payload), encoding="utf-8")


def test_a_failure_in_the_body_never_reaches_the_tolerance(monkeypatch):
    """Only the write back is caught: what the body raises is raised and not noted."""
    record()
    seen: list[BaseException] = []

    for raised in (secrets.CredentialBackendUnavailable("x"), OSError("x"), AdapterAuthFailed("x")):
        with pytest.raises(type(raised)):
            with provider_session.materialised_session(unstored=seen.append):
                raise raised
    assert seen == []


def test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once(
    installed, monkeypatch
):
    """A verb whose two logins both failed to store says so once."""
    no_keychain(monkeypatch, Factory(refresh_to=REFRESHED))
    original = tidal_catalogue.open_catalogue

    def opening(cfg=None):
        provider_session.client_session(gate=quick_gate())
        return original(cfg)

    monkeypatch.setattr(tidal_catalogue, "open_catalogue", opening)

    _, envelope = drive(HARVEST)

    said = not_stored(envelope)
    assert len(said) == 1, envelope["warnings"]
    assert said[0].count("CredentialBackendUnavailable") == 1
