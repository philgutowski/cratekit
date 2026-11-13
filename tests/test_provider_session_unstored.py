"""R-1694: a catalogue or account login whose access token the client library
refreshed goes on when the keychain cannot take the refreshed session, and the
verb says so, the way a download's drive does since U274.

Before this card ``provider_session._login`` wrote the refresh back at its
scope's close and nothing caught a refusal of that write, so on the product's
own opt in for a machine with no keychain, ``CRATE_ALLOW_ENV_CREDENTIALS=1``
with the session in the environment and keyring's fail backend, every verb
that opens the catalogue or the account failed once the stored access token
had expired.

1. **The login goes on**: ``client_session`` and ``session_for`` hand back the
   logged in client, the keychain keeps what it held, and the failure is noted
   by its class alone.
2. **The verb says so**: one ``provider-session-not-stored`` warning on the
   envelope, through the real dispatcher, beside the verb's own answer.
3. **Nothing else is caught**: an unchanged session writes and warns nothing,
   a rejected login still raises its typed rejection and holds nothing, a
   defect in the capture still raises, and a scope that asked for no tolerance
   still raises its write back failure.

D1 applies. Nothing here names a real account, a real token or a real path.
"""

from __future__ import annotations

import json
from pathlib import Path

import keyring
import pytest

from cratekit.acquire import provider_session, vendored
from cratekit.acquire.adapter import AdapterAuthFailed
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, refuse
from cratekit.label import catalogue
from cratekit.modules.outbound import account
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_provider_gate import _config_data
from tests.test_provider_session_hold import STORED, Factory, Keychain, quick_gate, record

SESSION = secrets.Credential.PROVIDER_SESSION
REFRESHED = "FAKE-value-3"
HARVEST = ["label", "harvest", "https://example.invalid/playlist/harvest"]


def no_keychain(monkeypatch) -> None:
    """The product's own opt in for a machine with no keychain: the session is
    read from the environment, and keyring's real fail backend refuses a write."""
    from keyring.backends import fail

    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv(secrets.ENV_CREDENTIAL_PREFIX + "PROVIDER_SESSION", json.dumps(STORED))
    backend = fail.Keyring()
    monkeypatch.setattr(keyring, "set_password", backend.set_password)
    monkeypatch.setattr(keyring, "get_password", backend.get_password)


def use(monkeypatch, factory: Factory) -> Factory:
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", factory)
    return factory


def noted_since(before: int) -> tuple[str, ...]:
    return provider_session.unstored()[before:]


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


# ═══════════════════════════════════════════════════════════════════════════
# 1. The login goes on
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refreshed_login_the_keychain_cannot_take_returns_the_client(monkeypatch):
    factory = use(monkeypatch, Factory(refresh_to=REFRESHED))
    no_keychain(monkeypatch)
    before = len(provider_session.unstored())

    client = provider_session.client_session(gate=quick_gate())

    assert client is factory.built[0]
    assert client.access_token == REFRESHED
    assert noted_since(before) == ("CredentialBackendUnavailable",)
    # The keychain keeps what it held: the environment's session, untouched.
    assert secrets.get_json(SESSION) == STORED


def test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again(
    cfg, monkeypatch
):
    """The keychain still holds the session the client was opened from, so the
    next resolve reuses the client rather than logging in and failing again."""
    factory = use(monkeypatch, Factory(refresh_to=REFRESHED))
    no_keychain(monkeypatch)
    before = len(provider_session.unstored())

    catalogue.resolve(cfg)
    catalogue.resolve(cfg)
    account.resolve(cfg)

    assert len(factory.built) == 1
    assert noted_since(before) == ("CredentialBackendUnavailable",)
    held = provider_session.held()
    assert held is not None
    assert held.blob == json.dumps(STORED, sort_keys=True)


def test_an_unchanged_session_on_the_opt_in_writes_nothing_and_notes_nothing(monkeypatch):
    use(monkeypatch, Factory())
    no_keychain(monkeypatch)
    before = len(provider_session.unstored())

    provider_session.client_session(gate=quick_gate())

    assert noted_since(before) == ()


def test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted(monkeypatch):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()
    before = len(provider_session.unstored())

    def unreadable(name):
        raise refuse("credential-index-unreadable", "the credential index could not be read")

    monkeypatch.setattr(secrets, "_record_name", unreadable)

    client = provider_session.client_session(gate=quick_gate())

    assert client.access_token == REFRESHED
    assert noted_since(before) == ("CratekitError",)


def test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched(monkeypatch):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()
    keychain = Keychain(monkeypatch)
    before = len(provider_session.unstored())

    def unlockable(action="update"):
        raise secrets.CredentialIndexUnusable("the index could not be locked")

    monkeypatch.setattr(secrets, "_index_locked", unlockable)

    provider_session.client_session(gate=quick_gate())

    assert keychain.writes == []
    assert noted_since(before) == ("CredentialIndexUnusable",)
    assert secrets.get_json(SESSION) == STORED


def test_a_token_file_that_cannot_take_the_refresh_is_noted(monkeypatch):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()
    keychain = Keychain(monkeypatch)
    before = len(provider_session.unstored())
    real = config.atomic_write_bytes

    def full(data, path, **kwargs):
        if json.loads(data).get("access_token") == REFRESHED:
            raise OSError(28, "No space left on device")
        return real(data, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", full)

    client = provider_session.client_session(gate=quick_gate())

    assert client.access_token == REFRESHED
    assert keychain.writes == []
    assert noted_since(before) == ("OSError",)


def test_an_unchanged_session_never_rewrites_the_token_file(monkeypatch):
    """So a file that cannot be written is never reported over a session that
    had nothing to store."""
    use(monkeypatch, Factory())
    record()
    before = len(provider_session.unstored())
    real = config.atomic_write_bytes
    writes: list[Path] = []

    def counted(data, path, **kwargs):
        writes.append(Path(path))
        return real(data, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", counted)

    provider_session.client_session(gate=quick_gate())

    assert len(writes) == 1, "only the materialised file, never a rewrite of it"
    assert noted_since(before) == ()


# ═══════════════════════════════════════════════════════════════════════════
# 2. The verb says so
# ═══════════════════════════════════════════════════════════════════════════


def test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns(
    installed, monkeypatch
):
    """Driven through the real dispatcher and the real catalogue opener. The
    fake client cannot serve a playlist, so the verb's own answer is a refusal;
    the refresh the keychain could not take must not replace it."""
    use(monkeypatch, Factory())
    no_keychain(monkeypatch)
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
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    no_keychain(monkeypatch)
    _, first = drive(HARVEST)
    assert len(not_stored(first)) == 1

    _, second = drive(HARVEST)

    assert not_stored(second) == [], "the held client was reused and nothing failed again"


def test_the_drives_warning_keeps_its_code():
    assert vendored.SESSION_NOT_STORED == provider_session.SESSION_NOT_STORED
    assert provider_session.SESSION_NOT_STORED == "provider-session-not-stored"


# ═══════════════════════════════════════════════════════════════════════════
# 3. Nothing else is caught
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rejected_login_on_the_opt_in_still_raises_the_rejection_and_holds_nothing(
    cfg, monkeypatch
):
    use(monkeypatch, Factory(status=401, refresh_to=REFRESHED))
    no_keychain(monkeypatch)
    before = len(provider_session.unstored())

    with pytest.raises(AdapterAuthFailed):
        provider_session.client_session(gate=quick_gate())
    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    assert excinfo.value.cause.reason == "credential-missing"
    assert provider_session.held() is None
    assert noted_since(before) == ()


def test_a_session_the_provider_no_longer_accepts_still_raises(monkeypatch):
    """A login the client answers False to is an expired session, never reused."""

    class Expired(Factory):
        def __call__(self):
            client = super().__call__()
            client.load_oauth_session = lambda *a, **k: False
            return client

    use(monkeypatch, Expired())
    no_keychain(monkeypatch)
    before = len(provider_session.unstored())

    with pytest.raises(AdapterAuthFailed):
        provider_session.client_session(gate=quick_gate())
    assert noted_since(before) == ()


def test_a_defect_in_the_capture_still_raises(monkeypatch):
    """A field the session file cannot hold is a defect, never a warning."""

    class Unencodable(Factory):
        def __call__(self):
            client = super().__call__()
            real = client.load_oauth_session

            def login(*args, **kwargs):
                answered = real(*args, **kwargs)
                client.refresh_token = object()
                return answered

            client.load_oauth_session = login
            return client

    use(monkeypatch, Unencodable())
    no_keychain(monkeypatch)
    before = len(provider_session.unstored())

    with pytest.raises(TypeError):
        provider_session.client_session(gate=quick_gate())
    assert noted_since(before) == ()


def test_a_defect_in_the_write_back_still_raises(monkeypatch):
    use(monkeypatch, Factory(refresh_to=REFRESHED))
    record()
    before = len(provider_session.unstored())

    def broken(name, payload):
        raise RuntimeError("a defect in the write")

    monkeypatch.setattr(secrets, "set_json", broken)

    with pytest.raises(RuntimeError):
        provider_session.client_session(gate=quick_gate())
    assert noted_since(before) == ()


def test_a_scope_that_asked_for_no_tolerance_still_raises_its_write_back_failure(
    monkeypatch, tmp_path
):
    """The drive and streamrip keep their own handling: without the callback a
    write back the keychain refuses raises as before."""
    no_keychain(monkeypatch)

    with pytest.raises(secrets.CredentialBackendUnavailable):
        with provider_session.materialised_session() as scope:
            payload = json.loads(scope.path.read_text(encoding="utf-8"))
            payload["access_token"] = REFRESHED
            scope.path.write_text(json.dumps(payload), encoding="utf-8")


def test_a_failure_in_the_body_never_reaches_the_tolerance(monkeypatch):
    """Only the write back is caught: what the body raises is raised, whatever
    its class, and nothing is noted for it."""
    record()
    seen: list[BaseException] = []

    for raised in (
        secrets.CredentialBackendUnavailable("x"),
        OSError("x"),
        AdapterAuthFailed("x"),
    ):
        with pytest.raises(type(raised)):
            with provider_session.materialised_session(unstored=seen.append):
                raise raised
    assert seen == []
