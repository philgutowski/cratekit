"""The adapter is the sole owner of the provider credential (R4, plan U14.5).

The keychain is the system of record. For one invocation, or one drive of a job
(U274), the session is materialised into a private file (P1) that is erased on every
exit path, and a validated refresh goes back to the keychain. The catalogue and the
account share one login per process through :func:`session_for` (U261), and a
refresh the keychain cannot take never fails that login (R-1694).
"""

from __future__ import annotations

import importlib
import json
import os
import re
import shutil
import stat
import tempfile
import tomllib
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import tomli_w

from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken, AdapterError, Remedy
from cratekit.core import config, provider_gate, secrets
from cratekit.core.cause import CratekitError, answered_status, failure_links

#: Fields that make a session blob usable; a write back missing all of them is a
#: truncated file and must never replace a good keychain entry.
SESSION_FIELDS = ("access_token", "refresh_token", "token_type", "expiry_time")


@dataclass(frozen=True, slots=True)
class Codec:
    """How one tool expects its credential file encoded; the keychain keeps one blob."""

    name: str
    dumps: Callable[[dict], bytes]
    loads: Callable[[str], object]


JSON = Codec(
    name="json",
    dumps=lambda payload: json.dumps(payload, sort_keys=True).encode("utf-8"),
    loads=json.loads,
)

TOML = Codec(name="toml", dumps=lambda payload: tomli_w.dumps(payload).encode("utf-8"),
             loads=tomllib.loads)


@dataclass(frozen=True, slots=True)
class SessionScope:
    """The live, private token file for one invocation, or one drive (U274)."""

    #: The private directory holding it. Erased whole when the scope closes.
    directory: Path
    #: The file the wrapped tool reads and rewrites.
    path: Path
    #: The session the keychain held at open, for the write back. Never in a repr.
    stored: Any = field(default=None, repr=False, compare=False)


#: The name every token directory starts with, followed by the process id (U274).
SESSION_PREFIX = "cratekit-session-"

#: A token directory this build made; one named any other way is never swept.
_OWNED_BY = re.compile(rf"^{re.escape(SESSION_PREFIX)}([1-9][0-9]*)-[A-Za-z0-9_]+$")


def _gone(pid: int) -> bool:
    """Whether no process has this id; only "no such process" is gone, so the sweep
    never removes a live run's file."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    except (OSError, OverflowError, ValueError):
        # Another account's process, or an id no process can have, which only
        # a directory someone else named could carry: never proven gone.
        return False
    return False


def sweep_orphans(root: Path | None = None) -> tuple[Path, ...]:
    """Remove token directories whose process is gone, and return them (U274).

    Only a real directory this account owns, named in this build's form, goes.
    """
    base = Path(root) if root is not None else Path(tempfile.gettempdir())
    try:
        entries = list(base.iterdir())
    except OSError:
        return ()
    account = os.getuid()
    removed: list[Path] = []
    for entry in entries:
        owned = _OWNED_BY.match(entry.name)
        if owned is None or not _gone(int(owned.group(1))):
            continue
        try:
            info = entry.lstat()
        except OSError:
            continue
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:
            continue
        shutil.rmtree(entry, ignore_errors=True)
        removed.append(entry)
    return tuple(removed)


#: The warning a report carries when a refreshed session could not be stored (U274,
#: R-1694).
SESSION_NOT_STORED = "provider-session-not-stored"

#: What storing a refreshed session can meet that is not a defect; anything else raises.
STORE_FAILURES: tuple[type[BaseException], ...] = (
    secrets.CredentialError,
    CratekitError,
    OSError,
)

#: The class of each store failure a login met, in order (R-1694). Only appended to,
#: so the dispatcher diffs it per verb; never the words, written for a person.
_UNSTORED: list[str] = []


def importable(module: str) -> bool:
    """Whether this build can import ``module``, reading no credential."""
    try:
        importlib.import_module(module)
    except ImportError:
        return False
    return True


def unstored() -> tuple[str, ...]:
    """The class of every store failure a login in this process met, in order."""
    return tuple(_UNSTORED)


def _to_auth_failure(exc: secrets.CredentialError) -> AdapterAuthFailed | AdapterBroken:
    """Translate a credential failure: no keychain is broken, a bad entry is auth."""
    if isinstance(exc, secrets.CredentialBackendUnavailable):
        return AdapterBroken(str(exc), remedy=Remedy.REPAIR_CREDENTIAL_STORE)
    return AdapterAuthFailed(str(exc), remedy=Remedy.REAUTHENTICATE_PROVIDER)


@contextmanager
def materialised_session(
    name: str = secrets.Credential.PROVIDER_SESSION,
    *,
    filename: str = "session.json",
    codec: Codec = JSON,
    unstored: Callable[[BaseException], None] | None = None,
) -> Iterator[SessionScope]:
    """Yield a private, short-lived file holding the stored provider session.

    ``unstored``, when given, receives a write back failure of :data:`STORE_FAILURES`
    instead of it raising (R-1694); an exception from the body is never caught.
    """
    try:
        payload = secrets.get_json(name)
    except secrets.CredentialError as exc:
        raise _to_auth_failure(exc) from exc

    # What a killed process left behind goes first (U274).
    sweep_orphans()
    # mkdtemp creates at 0700 already; the private writer re-asserts it (P1).
    directory = Path(tempfile.mkdtemp(prefix=f"{SESSION_PREFIX}{os.getpid()}-"))
    path = directory / filename
    try:
        config.atomic_write_bytes(codec.dumps(payload), path, mode=config.PRIVATE_FILE_MODE)
        yield SessionScope(directory=directory, path=path, stored=payload)
        if unstored is None:
            write_back(name, path, codec=codec, stored=payload)
        else:
            try:
                write_back(name, path, codec=codec, stored=payload)
            except STORE_FAILURES as exc:
                unstored(exc)
    finally:
        # Unconditional: a run that raised is the likeliest to leave a token.
        shutil.rmtree(directory, ignore_errors=True)


def _tidalapi_client() -> Any:
    """A fresh, unauthenticated client, imported late so the downloader skips it."""
    import tidalapi  # noqa: PLC0415 - deferred on purpose, see docstring

    return tidalapi.Session()


#: How :func:`client_session` builds its unauthenticated client, looked up at call
#: time so the conftest guard can replace it and no test reaches the live provider.
CLIENT_FACTORY: Callable[[], Any] = _tidalapi_client


#: Response statuses that mean the provider judged the credential; any other login
#: failure says nothing about the session.
REJECTED_STATUSES = frozenset({400, 401, 403})


class ProviderUnavailable(AdapterError):
    """The login could not be ASKED, as distinct from being refused."""

    remedy = Remedy.RETRY_LATER


def _rejected(exc: BaseException) -> bool:
    """Whether a login failure is the provider refusing this session (R-1305)."""
    for link, declared in failure_links(exc):
        if answered_status(link) in REJECTED_STATUSES:
            return True
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False


def _epoch(value: Any) -> Any:
    """An expiry the session file can hold: a datetime as epoch, naive read as UTC."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.timestamp()
    return value


def client_session(
    name: str = secrets.Credential.PROVIDER_SESSION,
    *,
    gate: provider_gate.Gate | None = None,
) -> Any:
    """An authenticated provider client, built from the stored session.

    The gate is asked first and attached before login (R-705). PKCE always, since a
    device flow session was served lossy audio (R-210). A refresh the keychain cannot
    take is noted, not failed (R-1694). A verb takes :func:`session_for` instead.
    """
    return _login(name, gate or provider_gate.Gate())[0]


def _login(name: str, gate: provider_gate.Gate) -> tuple[Any, dict]:
    """:func:`client_session`'s login, and the session the keychain holds for its
    client: the refresh written back, or the stored one when it could not be (R-1694)."""
    gate.assert_open()
    failed: list[BaseException] = []
    with materialised_session(name, unstored=failed.append) as scope:
        stored = JSON.loads(scope.path.read_text(encoding="utf-8"))
        if not isinstance(stored, dict) or not stored.get("access_token"):
            raise AdapterAuthFailed(
                "the stored provider session carries no access token",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )
        client = CLIENT_FACTORY()
        gate.attach(client)
        try:
            authorised = client.load_oauth_session(
                stored.get("token_type") or "Bearer",
                stored["access_token"],
                stored.get("refresh_token"),
                stored.get("expiry_time"),
                is_pkce=True,
            )
        except CratekitError:
            # The gate's own refusal passes through as itself (R-705).
            raise
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            if _rejected(exc):
                raise AdapterAuthFailed(
                    f"the provider rejected the stored session ({exc})",
                    remedy=Remedy.REAUTHENTICATE_PROVIDER,
                ) from exc
            raise ProviderUnavailable(
                f"the provider could not be reached to open the stored session ({exc})",
                remedy=Remedy.RETRY_LATER,
            ) from exc
        if not authorised:
            raise AdapterAuthFailed(
                "the stored provider session is no longer valid",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )
        refreshed = dict(stored)
        for field in SESSION_FIELDS:
            value = getattr(client, field, None)
            if value is not None:
                refreshed[field] = _epoch(value)
        # Only a changed session is written, so a file that cannot be written is
        # never reported over a session with nothing to store.
        if _canonical(refreshed) != _canonical(stored):
            try:
                config.atomic_write_bytes(
                    JSON.dumps(refreshed), scope.path, mode=config.PRIVATE_FILE_MODE
                )
            except OSError as exc:
                failed.append(exc)
    if failed:
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
        return client, stored
    return client, refreshed


def _requests_session() -> Any:
    """A fresh transport for the catalogue client, the library the provider's own uses."""
    import requests  # noqa: PLC0415 - deferred like the client library, see _tidalapi_client

    return requests.Session()


#: How :func:`catalogue_client` builds its transport, replaced by the conftest guard
#: like :data:`CLIENT_FACTORY`.
CATALOGUE_TRANSPORT_FACTORY: Callable[[], Any] = _requests_session


def _country(account: Any) -> str | None:
    """The account's two letter country, or None when it did not say one."""
    code = getattr(account, "country_code", None)
    if isinstance(code, str) and len(code.strip()) == 2 and code.strip().isalpha():
        return code.strip().upper()
    return None


def catalogue_client(account: Any, *, gate: provider_gate.Gate) -> Any | None:
    """The client catalogue lookups go to under Cratekit's own app credentials, or None.

    Built only here (U205), paced by the same gate. None means ask the account: no
    country, a value not recorded, or one the keychain lost, which is noted with
    ``provider_gate.note_app_lost``. An unreadable keychain still refuses.
    """
    from cratekit.acquire import catalogue_api  # noqa: PLC0415 - see _tidalapi_client

    names = [str(name) for name in catalogue_api.CREDENTIALS]
    if not all(secrets.exists(name) for name in names):
        return None
    country = _country(account)
    if country is None:
        return None
    try:
        client_id, client_key = (secrets.get(name) for name in names)
    except secrets.CredentialMissing as exc:
        provider_gate.note_app_lost(str(getattr(exc, "name", "") or names[0]))
        return None
    except secrets.CredentialError as exc:
        raise catalogue_api.unreadable(exc) from exc
    client = catalogue_api.AppCatalogue(
        client_id, client_key, country, transport=CATALOGUE_TRANSPORT_FACTORY()
    )
    if not gate.attach(client, identity=provider_gate.APP):
        # Unreachable with the shipped transport; never hand out an unpaced client.
        raise AdapterBroken(
            "the catalogue client's transport cannot be paced by the provider gate",
            remedy=Remedy.REPORT_DEFECT,
        )
    return client


#: Statuses that judge the session on a call after login; 400 there is about the
#: read, not the token (``account.SESSION_REFUSED_STATUSES`` matches).
SESSION_REFUSED_STATUSES = frozenset({401, 403})


@dataclass(eq=False, slots=True)
class HeldSession:
    """The logged in session one process shares between its openers, by identity (U261)."""

    #: The keychain entry it was opened from.
    name: str
    #: The gate settings it was opened under; other settings open their own session.
    settings: provider_gate.GateSettings
    #: The gate both the client and the app client are attached to.
    gate: provider_gate.Gate
    #: The logged in provider client, out of the repr since it carries the tokens.
    client: Any = field(repr=False)
    #: The bytes the keychain holds for this client, which a reuse compares against.
    blob: str = field(repr=False)
    #: The app client :func:`catalogue_client` built beside it, or None.
    app: Any = None


#: The session this process holds, or None.
_HELD: HeldSession | None = None


def held() -> HeldSession | None:
    """The session this process holds, if any."""
    return _HELD


def forget() -> None:
    """Drop the held session, so the next :func:`session_for` logs in again."""
    global _HELD
    _HELD = None


def drop(session: HeldSession) -> None:
    """Drop ``session`` only if it is still the held one."""
    global _HELD
    if _HELD is session:
        _HELD = None


def _watch(session: HeldSession) -> None:
    """Drop ``session`` the moment the provider refuses it on any account call."""
    transport = getattr(session.client, "request_session", None)
    send = getattr(transport, "request", None)
    if not callable(send):
        return

    def watched(method: Any, url: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            response = send(method, url, *args, **kwargs)
        except Exception as exc:
            if answered_status(exc) in SESSION_REFUSED_STATUSES:
                drop(session)
            raise
        if getattr(response, "status_code", None) in SESSION_REFUSED_STATUSES:
            drop(session)
        return response

    transport.request = watched


def session_for(
    cfg: Any = None, name: str = secrets.Credential.PROVIDER_SESSION
) -> HeldSession:
    """The process's logged in session, opened once and reused (U261).

    A reuse asks the gate and reads the keychain once, reusing the client only while
    the keychain holds the session it was opened from. The app client is held with it
    (R-1218).
    """
    global _HELD
    settings = (
        provider_gate.GateSettings.from_config(cfg)
        if cfg is not None
        else provider_gate.GateSettings()
    )
    current = _HELD
    if current is not None and current.name == str(name) and current.settings == settings:
        current.gate.assert_open()
        try:
            stored = secrets.get_json(name)
        except secrets.CredentialError as exc:
            drop(current)
            raise _to_auth_failure(exc) from exc
        if _canonical(stored) == current.blob:
            if current.app is None:
                current.app = catalogue_client(current.client, gate=current.gate)
            return current
    forget()
    gate = provider_gate.Gate(settings)
    client, refreshed = _login(name, gate)
    app = catalogue_client(client, gate=gate)
    blob = _canonical(refreshed)
    opened = HeldSession(
        name=str(name), settings=settings, gate=gate, client=client,
        blob=blob if blob is not None else "", app=app,
    )
    _watch(opened)
    _HELD = opened
    return opened


def captured(client: Any, stored: Any) -> dict | None:
    """The stored session with the client's changed token fields over it, or None (U274)."""
    if not isinstance(stored, dict):
        return None
    refreshed = dict(stored)
    for name in SESSION_FIELDS:
        value = getattr(client, name, None)
        if value is None:
            continue
        value = _epoch(value)
        if value != stored.get(name):
            refreshed[name] = value
    return refreshed


def _canonical(payload: Any) -> str | None:
    """The bytes ``secrets.set_json`` would store, or None when it cannot encode."""
    try:
        return json.dumps(payload, sort_keys=True)
    except (TypeError, ValueError):
        return None


def write_back(
    name: str, path: Path, *, codec: Codec = JSON, stored: dict | None = None
) -> bool:
    """Return a refreshed session to the keychain, or leave it alone; True when written.

    An unreadable file keeps the last good credential, and an unchanged one is not
    written (U261).
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return False
    try:
        refreshed = codec.loads(raw)
    except Exception:  # noqa: BLE001 - every codec fails differently; none may raise out
        return False
    if not isinstance(refreshed, dict):
        return False
    if not any(field in refreshed for field in SESSION_FIELDS):
        return False
    if stored is not None:
        unchanged = _canonical(refreshed)
        if unchanged is not None and unchanged == _canonical(stored):
            return False
    secrets.set_json(name, refreshed)
    return True


__all__ = [
    "CATALOGUE_TRANSPORT_FACTORY", "CLIENT_FACTORY", "HeldSession", "JSON", "REJECTED_STATUSES",
    "SESSION_FIELDS", "SESSION_REFUSED_STATUSES", "TOML", "Codec", "ProviderUnavailable",
    "SessionScope", "SESSION_NOT_STORED", "SESSION_PREFIX", "STORE_FAILURES", "answered_status",
    "captured", "catalogue_client", "client_session", "drop", "failure_links", "forget", "held",
    "materialised_session", "session_for", "sweep_orphans", "unstored", "write_back",
]
