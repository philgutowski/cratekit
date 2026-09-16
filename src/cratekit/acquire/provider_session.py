"""The adapter is the sole owner of the provider credential (R4, plan U14.5).

WHAT IS WRONG TODAY. The vendored downloader authorises itself and persists its
own session to a plaintext file in the user's configuration directory. Nothing in
the product put it there and nothing in the product knows when it changes, so
R4's promise that credentials live in the OS keychain is false on the one surface
that holds a long-lived refresh token. The keychain would hold everything except
the credential that actually matters.

WHAT THIS DOES INSTEAD. The keychain is the system of record. For the life of ONE
invocation the adapter materialises the stored session into a private runtime
file, hands the wrapped tool that path, takes back whatever the tool refreshed,
writes it to the keychain, and erases the file. Between invocations there is no
token on disk at all.

THREE PROPERTIES, EACH LOAD-BEARING:

* **The file and its directory are both private.** A 0600 file inside a
  world-writable directory is not protected: any local account can unlink it and
  put its own file in place, and the mode on the file it replaced is irrelevant.
  Both modes come from ``core/config``'s private writers rather than from this
  module's own chmod, so there is one implementation of "private" (P1).
* **The erase runs on every exit path.** A run that raised is exactly the run
  most likely to leave a token behind, so the cleanup is in a ``finally`` and is
  not conditional on success.
* **The write-back is validated before it replaces the keychain entry.** A tool
  killed mid-write leaves a truncated file, and copying that over the stored
  session destroys the only good copy. An unreadable file is left alone and the
  keychain keeps what it had.

WHAT THIS IS NOT. It is not a lock. Two invocations in one installation would
each materialise their own file in their own directory, which is correct for
reading and is a last-writer-wins race for the refreshed token. Serialising
acquisition belongs to the job engine, not here.
"""

from __future__ import annotations

import json
import shutil
import tempfile
import tomllib
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import tomli_w

from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken, AdapterError, Remedy
from cratekit.core import config, secrets

#: Fields that make a session blob usable. A write-back missing all of them is a
#: truncated or empty file rather than a refreshed session, and replacing a good
#: keychain entry with it would cost the user their authorisation.
SESSION_FIELDS = ("access_token", "refresh_token", "token_type", "expiry_time")


@dataclass(frozen=True, slots=True)
class Codec:
    """How one tool expects its credential file encoded.

    This exists because the credential is the thing acquisition tools agree on
    LEAST. The vendored downloader reads a JSON token file written by its client
    library; the alternative reads its own configuration file. Both hold the same
    session, so the keychain stores one blob and the codec decides its shape on
    disk. Without this, either the second adapter reads a file it cannot parse,
    or the credential module grows a branch per tool.
    """

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
    """The live, private token file for one invocation."""

    #: The private directory holding it. Erased whole when the scope closes.
    directory: Path
    #: The file the wrapped tool reads and rewrites.
    path: Path


def _to_auth_failure(exc: secrets.CredentialError) -> AdapterAuthFailed | AdapterBroken:
    """Translate a credential failure into the adapter vocabulary.

    Kept as a translation rather than a re-raise because the two vocabularies
    answer different questions and collapsing them loses the one distinction that
    changes what the user does. No keychain at all is an adapter that cannot run,
    and telling that user to re-authorise sends them to a dialog that has nowhere
    to write the answer. A missing or stale entry is an authorisation problem,
    and telling that user to repair their keychain sends them to fix something
    that is working.
    """
    if isinstance(exc, secrets.CredentialBackendUnavailable):
        return AdapterBroken(str(exc), remedy=Remedy.REPAIR_CREDENTIAL_STORE)
    return AdapterAuthFailed(str(exc), remedy=Remedy.REAUTHENTICATE_PROVIDER)


@contextmanager
def materialised_session(
    name: str = secrets.Credential.PROVIDER_SESSION,
    *,
    filename: str = "session.json",
    codec: Codec = JSON,
) -> Iterator[SessionScope]:
    """Yield a private, short-lived file holding the stored provider session.

    ``filename`` and ``codec`` are parameters because the adapters wrap tools
    that disagree about both. Forking this module per tool would put the erase,
    the mode, and the write-back guard in two places, and the one that got fixed
    would not be the one running.
    """
    try:
        payload = secrets.get_json(name)
    except secrets.CredentialError as exc:
        raise _to_auth_failure(exc) from exc

    # mkdtemp creates at 0700 already; the private writer below re-asserts both
    # the directory and the file mode so the guarantee does not depend on the
    # standard library's default staying what it is today (P1).
    directory = Path(tempfile.mkdtemp(prefix="cratekit-session-"))
    path = directory / filename
    try:
        config.atomic_write_bytes(codec.dumps(payload), path, mode=config.PRIVATE_FILE_MODE)
        yield SessionScope(directory=directory, path=path)
        write_back(name, path, codec=codec)
    finally:
        # Unconditional. The run that raised is the run most likely to have left
        # a live refresh token sitting in a temporary directory.
        shutil.rmtree(directory, ignore_errors=True)


def _tidalapi_client() -> Any:
    """A fresh, unauthenticated client of the provider's own library.

    Imported here rather than at module top so the downloader half of the
    product, which never asks for a client, does not pay for the import.
    """
    import tidalapi  # noqa: PLC0415 - deferred on purpose, see docstring

    return tidalapi.Session()


#: How :func:`client_session` builds the unauthenticated client it logs in. A
#: module attribute looked up at call time, so a suite substitutes a fake client
#: here and nowhere else, and the conftest guard replaces it for every test so no
#: test can reach the live provider by recording a session and asking for one.
CLIENT_FACTORY: Callable[[], Any] = _tidalapi_client


#: Response statuses that mean the provider judged the CREDENTIAL. Every other
#: failure of a login, a refused connection, a timeout, a server error page the
#: client then fails to parse, says nothing about the session, and telling that
#: person to log in again sends them to fix a session that is fine.
REJECTED_STATUSES = frozenset({400, 401, 403})


class ProviderUnavailable(AdapterError):
    """The login could not be ASKED, as distinct from being refused."""

    remedy = Remedy.RETRY_LATER


def _rejected(exc: BaseException) -> bool:
    """Whether a login failure is the provider refusing this session.

    Read off the response status the client attaches, or the client's own
    authentication error by name, walking the cause chain because the client
    re-raises its HTTP error under its own types.
    """
    seen: BaseException | None = exc
    while seen is not None:
        status = getattr(getattr(seen, "response", None), "status_code", None)
        if status in REJECTED_STATUSES:
            return True
        if type(seen).__name__ == "AuthenticationError":
            return True
        seen = seen.__cause__
    return False


def _epoch(value: Any) -> Any:
    """An expiry the session file can hold. The client stores a datetime after a
    refresh, and JSON has no datetime, so a refreshed session that cannot be
    encoded would leave the keychain holding the token the refresh replaced.

    The client's datetime is NAIVE UTC, so it is read as UTC here. Read as local
    time, which is what ``timestamp`` does with a naive value, it lands hours off.
    """
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.timestamp()
    return value


def client_session(name: str = secrets.Credential.PROVIDER_SESSION) -> Any:
    """An authenticated provider client, built from the stored session.

    THE ONE PLACE A CATALOGUE OR ACCOUNT READS AND WRITES BACK THE TOKEN, and it
    is built inside :func:`materialised_session` rather than beside it so that
    stays true: the downloader and the catalogue then read the same stored blob
    through the same scope, and a refresh the login performed goes back to the
    keychain through the same validated :func:`write_back`.

    PKCE ALWAYS, matching the downloader's ``login_token(do_pkce=True)``, because
    that is the path the attended sitting proved against the live provider. A
    device flow session on the same account was served lossy audio (R-210).

    THE SCOPE CLOSES BEFORE THE CLIENT IS RETURNED. The client is an in memory
    object and does not need the file, so no token sits on disk for the life of
    a long crawl. What that costs is named rather than hidden: a refresh the
    client performs AFTER this returns lives only in memory. The stored refresh
    token stays valid, so the next invocation logs in again from it.

    Raises :class:`AdapterAuthFailed` for a stored blob that is not a session or
    that the provider rejects, :class:`ProviderUnavailable` for a login that
    could not be asked at all, and lets :func:`materialised_session`'s own
    translation of a keychain failure through unchanged.
    """
    with materialised_session(name) as scope:
        stored = JSON.loads(scope.path.read_text(encoding="utf-8"))
        if not isinstance(stored, dict) or not stored.get("access_token"):
            raise AdapterAuthFailed(
                "the stored provider session carries no access token",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )
        client = CLIENT_FACTORY()
        try:
            authorised = client.load_oauth_session(
                stored.get("token_type") or "Bearer",
                stored["access_token"],
                stored.get("refresh_token"),
                stored.get("expiry_time"),
                is_pkce=True,
            )
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
        config.atomic_write_bytes(
            JSON.dumps(refreshed), scope.path, mode=config.PRIVATE_FILE_MODE
        )
    return client


def write_back(name: str, path: Path, *, codec: Codec = JSON) -> bool:
    """Return a refreshed session to the keychain, or leave the keychain alone.

    Returns whether the keychain was updated, so a caller can tell "the tool
    refreshed nothing" from "the tool wrote something unusable". Silence on an
    unreadable file is deliberate: raising turns a cosmetic problem at the end of
    a successful run into a failed run, and writing it anyway destroys the stored
    session. Doing nothing keeps the last known good credential, which is the
    only one of the three outcomes the user can recover from unaided.
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
    secrets.set_json(name, refreshed)
    return True


__all__ = [
    "CLIENT_FACTORY",
    "JSON",
    "REJECTED_STATUSES",
    "SESSION_FIELDS",
    "TOML",
    "Codec",
    "ProviderUnavailable",
    "SessionScope",
    "client_session",
    "materialised_session",
    "write_back",
]
