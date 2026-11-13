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
writes it to the keychain, and erases the file. A download job's invocation is
one drive of the job, every track it acquires (U274, Phillip's answer on the
card): one file, one login, one write back. Between invocations there is no
token on disk at all.

THREE PROPERTIES, EACH LOAD-BEARING:

* **The file and its directory are both private.** A 0600 file inside a
  world-writable directory is not protected: any local account can unlink it and
  put its own file in place, and the mode on the file it replaced is irrelevant.
  Both modes come from ``core/config``'s private writers rather than from this
  module's own chmod, so there is one implementation of "private" (P1).
* **The erase runs on every exit path.** A run that raised is exactly the run
  most likely to leave a token behind, so the cleanup is in a ``finally`` and is
  not conditional on success. A process killed outright runs no exit path, so
  each directory is named for its process and every new scope first sweeps the
  ones whose process is gone (:func:`sweep_orphans`, U274).
* **The write-back is validated before it replaces the keychain entry.** A tool
  killed mid-write leaves a truncated file, and copying that over the stored
  session destroys the only good copy. An unreadable file is left alone and the
  keychain keeps what it had.

WHAT THIS IS NOT. It is not a lock. Two invocations in one installation would
each materialise their own file in their own directory, which is correct for
reading and is a last-writer-wins race for the refreshed token. Serialising
acquisition belongs to the job engine, not here. A scope whose tool left the
session as it was writes nothing back (U261), so only a run that refreshed the
token takes part in that race.

ONE LOGIN PER PROCESS FOR THE CATALOGUE AND THE ACCOUNT (U261). Their openers
take :func:`session_for`, which logs in once and hands every later opener the
same client while the keychain still holds the session it was opened from; a
refusal from the provider, or a forget, drops it for every opener at once.
A refresh the keychain cannot take never fails that login (R-1694): the client
goes on, the next run logs in again from whatever the keychain holds, and the
verb's report says so.
"""

from __future__ import annotations

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
    """The live, private token file for one invocation, or one drive (U274)."""

    #: The private directory holding it. Erased whole when the scope closes.
    directory: Path
    #: The file the wrapped tool reads and rewrites.
    path: Path
    #: The session the keychain held when the scope opened, which the write
    #: back compares against. Never in a repr: it is the token.
    stored: Any = field(default=None, repr=False, compare=False)


#: The name every token directory starts with. The process id follows it, so a
#: directory a killed process left behind can be told from a live one's (U274).
SESSION_PREFIX = "cratekit-session-"

#: A token directory this build made: the prefix, the owning process id, and
#: what ``mkdtemp`` added. A directory named any other way, one a build before
#: U274 made among them, is never swept.
_OWNED_BY = re.compile(rf"^{re.escape(SESSION_PREFIX)}([1-9][0-9]*)-[A-Za-z0-9_]+$")


def _gone(pid: int) -> bool:
    """Whether no process has this id. Only a lookup the kernel answered with
    "no such process" is gone; a process of another account, or any other
    answer, is read as alive, so the sweep never removes a live run's file."""
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

    A SIGKILL, a power cut or a crash of the interpreter runs no exit path, so
    the erase below cannot run for it, and since U274 a download holds its
    token file for a whole drive of a job rather than for one track. This is
    the erase for that case, run before every new scope is made: a directory
    is removed only when its name is this build's form, it is a directory and
    not a link, this account owns it, and the process its name records is
    gone. This process's own directories are never touched, and nothing else
    in the temporary directory is read past its name.
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
        # This process's own directories are alive by the same lookup.
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


#: The warning a report carries when a session the provider refreshed could
#: not be stored: at the close of a download's drive (U274), and at a
#: catalogue or account login (R-1694).
SESSION_NOT_STORED = "provider-session-not-stored"

#: What storing a refreshed session can meet that is not a defect: the
#: keychain's own refusal (the product's opt in for a machine with no keychain
#: among them) and the presence index's lock, both ``secrets.CredentialError``;
#: the index's unreadable refusal, a ``CratekitError``; and a file the write
#: could not make, an ``OSError``. Anything else is a defect, and raises.
STORE_FAILURES: tuple[type[BaseException], ...] = (
    secrets.CredentialError,
    CratekitError,
    OSError,
)

#: The class of each failure a catalogue or account login met storing the
#: session its client refreshed, in the order met (R-1694). Process wide and
#: only ever appended to, so the dispatcher reads what one verb added by
#: reading it before and after; the class and never the words, since a
#: credential refusal's words are written for a person setting one up.
_UNSTORED: list[str] = []


def unstored() -> tuple[str, ...]:
    """The class of every store failure a login in this process met, in order."""
    return tuple(_UNSTORED)


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
    unstored: Callable[[BaseException], None] | None = None,
) -> Iterator[SessionScope]:
    """Yield a private, short-lived file holding the stored provider session.

    ``filename`` and ``codec`` are parameters because the adapters wrap tools
    that disagree about both. Forking this module per tool would put the erase,
    the mode, and the write-back guard in two places, and the one that got fixed
    would not be the one running.

    ``unstored``, when given, is handed a write back at the close that failed
    with one of :data:`STORE_FAILURES`, in place of raising it (R-1694): the
    caller goes on with what the scope gave it and says so. The keychain
    holds what it held, unless only the index refused after the keychain
    took the refresh, as ``secrets.set`` says it can. Only the write back is inside that catch. An
    exception raised in the body, a provider's rejection, a gate's refusal, a
    login that could not be asked, is thrown at the ``yield`` and never reaches
    it, whatever its class. Without it a write back failure raises, as it
    always has.
    """
    try:
        payload = secrets.get_json(name)
    except secrets.CredentialError as exc:
        raise _to_auth_failure(exc) from exc

    # What a killed process left behind goes first (U274), then this scope's
    # own directory is named for this process so a later one can tell.
    sweep_orphans()
    # mkdtemp creates at 0700 already; the private writer below re-asserts both
    # the directory and the file mode so the guarantee does not depend on the
    # standard library's default staying what it is today (P1).
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

    Read off the response status the client attaches, on any link
    :func:`failure_links` reaches, since a status whose body was not JSON sits
    under the client's decode error as context (R-1305); or the client's own
    authentication error by name, on the declared cause chain only, because the
    client re-raises its HTTP error under its own types and a name reached
    only as context is a guess.
    """
    for link, declared in failure_links(exc):
        if answered_status(link) in REJECTED_STATUSES:
            return True
        if declared and type(link).__name__ == "AuthenticationError":
            return True
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


def client_session(
    name: str = secrets.Credential.PROVIDER_SESSION,
    *,
    gate: provider_gate.Gate | None = None,
) -> Any:
    """An authenticated provider client, built from the stored session.

    THE ONE LOGIN A CATALOGUE OR ACCOUNT MAKES, and it is built inside
    :func:`materialised_session` rather than beside it so that the downloader
    and the catalogue read the same stored blob through the same scope, and a
    refresh the login performed goes back to the keychain through the same
    validated :func:`write_back`. Since U261 the openers reach it through
    :func:`session_for`, which also reads the keychain on a reuse to see the
    session it holds is still the stored one, and writes nothing there.

    THE GATE IS ASKED BEFORE THE CLIENT IS BUILT AND ATTACHED BEFORE IT LOGS IN
    (R-705). A verb started inside the cooldown a rate limited run left behind
    refuses here, naming the time it lifts, and makes no call; and the login
    itself is the first paced call of the run, since the transport is wrapped
    before it goes out. A caller with no configuration gets a gate at the
    defaults, which is still a gate: there is no way to open a client past it.

    PKCE ALWAYS, matching the downloader's ``login_token(do_pkce=True)``, because
    that is the path the attended sitting proved against the live provider. A
    device flow session on the same account was served lossy audio (R-210).

    A REFRESH THE KEYCHAIN CANNOT TAKE IS NOT A FAILED LOGIN (R-1694). The
    client is logged in, so it is returned; the keychain holds a session
    whose refresh token still logs in, the one it held or, when only the
    index refused after the keychain took it, the refresh, and the failure's
    class is noted
    (:func:`unstored`) for the verb's report to say the session was not stored
    and the next run logs in again. Only a failure to store is taken so: a
    rejected or expired session raises as it always did, and so does a defect.

    THE SCOPE CLOSES BEFORE THE CLIENT IS RETURNED. The client is an in memory
    object and does not need the file, so no token sits on disk for the life of
    a long crawl. What that costs is named rather than hidden: a refresh the
    client performs AFTER this returns lives only in memory. The stored refresh
    token stays valid, so the next invocation logs in again from it.

    Raises :class:`AdapterAuthFailed` for a stored blob that is not a session or
    that the provider rejects, :class:`ProviderUnavailable` for a login that
    could not be asked at all, and lets :func:`materialised_session`'s own
    translation of a keychain failure through unchanged.

    A VERB DOES NOT CALL THIS: it takes the process's held session from
    :func:`session_for`, which calls this once and reuses the client (U261).
    """
    return _login(name, gate or provider_gate.Gate())[0]


def _login(name: str, gate: provider_gate.Gate) -> tuple[Any, dict]:
    """:func:`client_session`'s login, and the session the keychain holds for
    the client it returns once the scope has closed: the stored one, or the
    refresh the scope wrote back over it. A refresh that could not be stored
    is taken to leave the stored one there, so that is the one returned, and a
    later reuse compares the keychain against it (R-1694). When only the index
    refused, after the keychain took the refresh, that reuse finds the
    keychain changed and logs in afresh, one login more, never a refused one."""
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
            # THE GATE'S OWN REFUSAL PASSES THROUGH (R-705). The login is a
            # paced call like any other, and a rate limit answered to it that
            # trips the breaker is the park, which must reach the engine as
            # itself: read as "could not be reached" it would be retried into
            # the cooldown, and read as rejected it would send a person to log
            # in again over a session that is fine.
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
        # ONLY A CHANGED SESSION IS WRITTEN to the token file, which the
        # write back would find unchanged anyway, so a file that cannot be
        # written is never reported over a session with nothing to store. A
        # field the file cannot encode is a defect and raises here.
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


#: How :func:`catalogue_client` builds the transport its client sends through.
#: Looked up at call time, so a suite substitutes a fake transport here and
#: nowhere else, and the conftest guard replaces it for every test as it
#: replaces :data:`CLIENT_FACTORY`: no test can reach the live catalogue by
#: recording the app's credentials and opening an account.
CATALOGUE_TRANSPORT_FACTORY: Callable[[], Any] = _requests_session


def _country(account: Any) -> str | None:
    """The account's two letter country, or None when it did not say one."""
    code = getattr(account, "country_code", None)
    if isinstance(code, str) and len(code.strip()) == 2 and code.strip().isalpha():
        return code.strip().upper()
    return None


def catalogue_client(account: Any, *, gate: provider_gate.Gate) -> Any | None:
    """The client catalogue lookups go to under Cratekit's own app credentials, or None.

    THE ONE PLACE THE APP CLIENT IS BUILT (U205), beside :func:`client_session`
    and attached to the SAME gate, under the ``app`` identity, before it makes
    its first request, so the interval, the breaker, the cooldown and the call
    ceiling the account's calls run under are the ones its calls run under too.

    NONE MEANS ASK THE ACCOUNT, EXACTLY AS BEFORE THIS UNIT, and is answered
    when either value is not recorded, so an installation that never set the
    app up behaves as it always did. Presence is asked of the index first, so
    an installation with no app makes no keychain read for it.

    THE KEYCHAIN IS THE EFFECTIVE VALUE, AND THE INDEX ONLY WHAT WAS WRITTEN.
    A value the index records and the keychain answers is not there for, which
    is what deleting it through the operating system's own keychain does, is
    NOT recorded, and the lookups go to the account as for any installation
    without the app (U205's review, round one). Refusing there would lock the
    person out of every verb that opens the account, and the product has no
    way to un-record a value, so the refusal would have no remedy short of
    registering the app again. THE FALLBACK IS NEVER SILENT (round two): the
    lost name is noted with ``provider_gate.note_app_lost``, and the run's spend
    line says the value is recorded and missing, that the lookups went to the
    account, and how to record it again. A keychain that could not be READ
    at all is still refused, see ``catalogue_api.unreadable``: that is a
    broken machine, not an absent value.

    THE COUNTRY IS THE ACCOUNT'S OWN, read off the account client the login
    filled, so an availability answer is the one the account would get. An
    account client that names no country, which no logged in client of the
    provider library is, also answers None: the app cannot be asked a question
    whose answer depends on a country nobody named.
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
        # Unreachable with the shipped transport, which always has a request
        # method; a client the gate cannot pace is never handed out unpaced.
        raise AdapterBroken(
            "the catalogue client's transport cannot be paced by the provider gate",
            remedy=Remedy.REPORT_DEFECT,
        )
    return client


#: Statuses that judge the SESSION on a call made after login. Narrower than
#: :data:`REJECTED_STATUSES`, which includes 400 because a login's bad request
#: is a bad token; a read answered 400 is a bad request about that read. The
#: outbound account reads the same set (``account.SESSION_REFUSED_STATUSES``).
SESSION_REFUSED_STATUSES = frozenset({401, 403})


@dataclass(eq=False, slots=True)
class HeldSession:
    """The logged in session one process shares between its openers (U261).

    Compared by identity, never by value: an adapter built over this session
    asks whether the session it was built over is STILL the held one, and two
    logins that happened to answer alike are still two logins.
    """

    #: The keychain entry it was opened from.
    name: str
    #: The gate settings it was opened under, so a caller handing over other
    #: settings, a job's frozen configuration, opens a session of its own.
    settings: provider_gate.GateSettings
    #: The gate both the client and the app client are attached to.
    gate: provider_gate.Gate
    #: The logged in provider client every opener builds its adapter over.
    #: Kept out of the repr, since the client carries the tokens.
    client: Any = field(repr=False)
    #: The bytes the keychain holds for this client, as ``secrets.set_json``
    #: stores them: what a reuse compares the keychain against. Kept out of
    #: the repr, since it IS the session, tokens and all.
    blob: str = field(repr=False)
    #: The app client :func:`catalogue_client` built beside it, or None.
    app: Any = None


#: The session this process holds, or None before the first open and after a
#: refusal or :func:`forget`.
_HELD: HeldSession | None = None


def held() -> HeldSession | None:
    """The session this process holds, if any. Read, never kept, by an adapter
    holder that must know whether its client is still the held one."""
    return _HELD


def forget() -> None:
    """Drop the held session, so the next :func:`session_for` logs in again."""
    global _HELD
    _HELD = None


def drop(session: HeldSession) -> None:
    """Drop ``session`` if it is still the held one, and nothing newer: what a
    refusal of one client forgets, since a session logged in since was not
    the one refused."""
    global _HELD
    if _HELD is session:
        _HELD = None


def _watch(session: HeldSession) -> None:
    """Drop ``session`` the moment the provider refuses it on any call.

    The refusal is read where every call of the shared client passes, its
    transport, over the gate's own wrap, so it does not matter which seam made
    the call or how that seam reads the failure: the label catalogue, which
    has no forget of its own, and the account, which has, both leave the next
    resolve to log in again rather than hand the next opener a client the
    provider has refused. A status that judges no session, a not found or a
    rate limit, keeps it. Only the account identity's transport is watched; the
    app client's refusals are about the app's credentials, not the session.
    """
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

    THE FIRST USE LOGS IN EXACTLY AS :func:`client_session` DOES: the gate is
    asked, the stored session is materialised, the provider validates it, a
    refresh goes back to the keychain, and every failure raises the typed
    failure it raised before. Nothing is held unless all of that succeeded,
    save a refresh the keychain could not take, which is noted rather than
    raised (R-1694): the client is held over the session the keychain still
    holds, so a later use reuses it and neither logs in nor fails to store
    again; when only the index refused after the keychain took the refresh,
    the keychain no longer matches and the later use logs in afresh.

    A LATER USE MAKES NO REQUEST, and is still asked three things first. The
    gate, so a verb started inside a cooldown refuses here as a first open
    does. The gate settings, so a caller with other settings opens its own.
    And the keychain, read once: the client is reused only while the keychain
    still holds the session it was opened from. A session another process
    refreshed, or a different login recorded since, is logged in afresh from
    the new value; one that is missing, unreadable or not a session raises the
    same translation a login raises and drops the hold, so a session removed
    after an open is refused rather than reused.

    WHAT IS FORGOTTEN IS FORGOTTEN FOR EVERY OPENER. The outbound account's
    forget on a refused session drops this hold, and so does any 401 or 403
    answered through the shared client (:func:`_watch`), so the label
    catalogue and the account never hand out a client the provider refused.

    The app client is held with it (R-1218), so a process that opens both the
    catalogue and the account asks the token service once. When none was
    built, a reuse asks :func:`catalogue_client` again, which reads presence
    only and notes a lost app value for this run's spend line as before.
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
    """The stored session with the client's token fields over it (U274).

    For a scope that outlives its login, a drive of a download job: the client
    library refreshes an expired access token in memory and writes no file, so
    the scope writes the client's session into the token file before it closes,
    and :func:`write_back` takes it from there. A field is taken only where the
    client holds a value and it differs from the stored one by value, so a
    login that refreshed nothing hands back the stored session unchanged (an
    expiry the tool read back as ``1700000000.0`` is the stored ``1700000000``)
    and the keychain is not written. An expiry the client holds as a datetime
    is stored as the epoch, as :func:`client_session`'s login stores it. None
    when there is no stored session to lay the fields over.
    """
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
    """The bytes ``secrets.set_json`` would store for ``payload``, or None when
    it cannot be encoded, which then compares equal to nothing."""
    try:
        return json.dumps(payload, sort_keys=True)
    except (TypeError, ValueError):
        return None


def write_back(
    name: str, path: Path, *, codec: Codec = JSON, stored: dict | None = None
) -> bool:
    """Return a refreshed session to the keychain, or leave the keychain alone.

    Returns whether the keychain was updated, so a caller can tell "the tool
    refreshed nothing" from "the tool wrote something unusable". Silence on an
    unreadable file is deliberate: raising turns a cosmetic problem at the end of
    a successful run into a failed run, and writing it anyway destroys the stored
    session. Doing nothing keeps the last known good credential, which is the
    only one of the three outcomes the user can recover from unaided.

    AN UNCHANGED SESSION IS NOT WRITTEN (U261). ``stored`` is the session the
    scope read out of the keychain, and a file that comes back holding the same
    value is left where it is: the keychain already holds it, and the write
    would only spend a keychain write and a read back on every login. Same
    means the same bytes ``secrets.set_json`` would store, so key order and
    spacing in the file do not count as a change and a value that changed type
    does. A session that differs is written exactly as before, through
    ``secrets.set_json``, the index lock, the read back and the index. With no
    ``stored`` to compare against, the file is written as before.
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
    "CATALOGUE_TRANSPORT_FACTORY",
    "CLIENT_FACTORY",
    "HeldSession",
    "JSON",
    "REJECTED_STATUSES",
    "SESSION_FIELDS",
    "SESSION_REFUSED_STATUSES",
    "TOML",
    "Codec",
    "ProviderUnavailable",
    "SessionScope",
    "SESSION_NOT_STORED",
    "SESSION_PREFIX",
    "STORE_FAILURES",
    "answered_status",
    "captured",
    "catalogue_client",
    "client_session",
    "drop",
    "failure_links",
    "forget",
    "held",
    "materialised_session",
    "session_for",
    "sweep_orphans",
    "unstored",
    "write_back",
]
