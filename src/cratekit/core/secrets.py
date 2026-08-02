"""Service credentials, in the OS keychain, with three distinct failure types.

WHY THE KEYCHAIN. The source system keeps its credentials in two plaintext files
under a state directory. Neither is chmodded by any code: the 0600 on the live
files comes from the author's umask, so on a machine with a laxer umask both
land world readable. One of them holds a long-lived refresh token, written by a
third-party library that does no chmod at all. R4 moves all of it to the OS
keychain, which is cross-platform by construction (KTD6) and is the one store
whose permissions do not depend on how the user's shell was configured.

WHY THREE FAILURES AND NOT ONE. This is the part worth reading. A missing
credential and a rejected one need OPPOSITE remediations, and a backend that is
not there needs a third:

* ``CredentialBackendUnavailable`` - there is no keychain to ask. Telling the
  user to re-enter their password here is useless; there is nowhere to put it.
* ``CredentialMissing`` - the keychain works and has no entry. Telling the user
  to re-authenticate is useless; the service never rejected anything.
* ``CredentialRejected`` - the entry exists and the service refused it. Telling
  the user to set the credential is useless; it IS set, it is stale.

Collapse those into one error and every caller has to parse a message string to
find out which advice to give, which is precisely the failure KTD25 names: a
typed failure that flattens at any hop cannot be recovered downstream. The
concrete failure being avoided is the source system's, where an absent key
produced an unauthenticated request that surfaced to the user as a service
outage.

NO SILENT FALLBACKS. Not to a file, not to an empty string, and not to the
environment unless the user opted in by name. A read on a machine with no
reachable backend RAISES. Returning None there is how a caller ends up sending a
request with no credential at all and reading the 401 as the service being down.

STILL TO COME, and deliberately not here. During the migration overlap the user's
real credentials live in the old system's two plaintext files, and a one-time
importer should read both, record them here, and then PRINT rather than perform
the removal. It must never delete the source files, because the old system needs
them for the whole overlap. That importer is a command, and commands belong to
the CLI layer (D2), so it is named in the CLI registry and not in this module.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path

import keyring
import keyring.errors

from cratekit.core import config

#: One keychain service for the whole installation. NOT namespaced per library:
#: a credential is an account fact, not a library fact, which is why KTD21 puts
#: it in the installation root. Namespacing by library would make the same
#: account's token get re-entered once per library the user owns.
SERVICE = "cratekit"

#: Opt-in escape hatch for a headless machine with no keychain daemon. Off unless
#: set, and every refusal names it, so the fallback is a decision the user made
#: rather than a behaviour they discover after a credential leaks into a process
#: listing.
ENV_ALLOW_ENV_CREDENTIALS = "CRATE_ALLOW_ENV_CREDENTIALS"
ENV_CREDENTIAL_PREFIX = "CRATEKIT_CREDENTIAL_"


class Credential(StrEnum):
    """Every credential the product stores. Names only; values never appear here.

    Two of these carry the identification service's access key and the shared
    value it uses to sign requests. They are spelled without the obvious word on
    purpose: the repository scanner treats ``<that word> = "<long string>"`` as a
    leaked credential, and a constant that trips the guard trains people to
    silence the guard.
    """

    IDENTIFY_KEY = "identify-key"
    IDENTIFY_SIGNING_KEY = "identify-signing-key"
    PROVIDER_SESSION = "provider-session"


class Remedy(StrEnum):
    """What to do about a credential failure, as a TOKEN rather than a command.

    D2: no foundation module contains the text a user types. The CLI layer, and
    only the CLI layer, renders one of these into a command line, because the
    command depends on the interface the user is actually sitting in front of and
    this layer does not know which one that is.

    U5 owns the product-wide vocabulary and reserves a code and a remediation for
    every refusal in the system (S4). These three are this module's contribution
    to that reservation, not a competing scheme.
    """

    INSTALL_KEYCHAIN_BACKEND = "install-keychain-backend"
    SET_CREDENTIAL = "set-credential"
    REAUTHENTICATE = "reauthenticate"


class CredentialError(Exception):
    """Base for credential failures. Always carries a structured remedy token."""

    remedy: Remedy = Remedy.SET_CREDENTIAL

    def __init__(self, message: str, *, name: str | None = None) -> None:
        super().__init__(message)
        self.name = name


class CredentialBackendUnavailable(CredentialError):
    """No usable keychain backend. Remediation: install one, not re-enter anything."""

    remedy = Remedy.INSTALL_KEYCHAIN_BACKEND


class CredentialMissing(CredentialError):
    """The backend works and holds no entry. Remediation: record the credential."""

    remedy = Remedy.SET_CREDENTIAL


class CredentialRejected(CredentialError):
    """The service refused a credential that IS set. Remediation: re-authenticate.

    Raised by the caller that got the refusal, not by this module: only the code
    talking to the service can tell a 401 from a network failure. It lives here
    so every caller raises the SAME type, which is the whole point of typing the
    failure at all.
    """

    remedy = Remedy.REAUTHENTICATE


def backend_available() -> bool:
    """A DOCTOR-only probe: does this machine resolve a backend that can store?

    Deliberately not called by ``get``/``set``/``delete``. It asks keyring which
    backend it would choose and reads that backend's priority, which is a
    heuristic about a class rather than an observation about a call. Doctor wants
    the heuristic, because its job is to warn before a workflow starts. The
    read and write paths want the observation, because a heuristic that is wrong
    either refuses a machine that works or accepts one that does not.

    BOTH lines are inside the try, and that is the whole point of the shape.
    ``getattr`` with a default suppresses a MISSING attribute, not an attribute
    that raises, and keyring's backends define ``priority`` as a classproperty
    that raises when the backend is not viable here: the macOS backend raises
    "Security API unavailable", the SecretService backend raises after a live
    D-Bus round trip. Reading it outside the try turned a health check into an
    unhandled traceback on exactly the machine it exists to diagnose.
    """
    try:
        backend = keyring.get_keyring()
        return bool(getattr(backend, "priority", 0) > 0)
    except Exception:  # keyring raises several unrelated types while resolving
        return False


def _unavailable(action: str, name: str, exc: Exception) -> CredentialBackendUnavailable:
    """Turn "there is no usable keychain here" into the typed refusal.

    ``NoKeyringError`` is the backend TELLING us it cannot store anything, which
    is a stronger signal than any probe of ours. That is why the read and write
    paths key on the exception rather than checking a backend up front: the
    exception is an observation, and it is also the only form the answer takes on
    a machine where keyring resolves a chain rather than a single backend.

    WHY THE CALLERS CATCH ``Exception`` AND NOT ``KeyringError``. The keychain is
    an external system, and its failure modes are not a closed set that this
    module gets to enumerate. On Linux, the second platform R1 cares about,
    keyring's SecretService backend calls into D-Bus OUTSIDE its own try block, so
    a headless box with no session bus raises ``SecretServiceNotAvailableException``,
    which is not a ``KeyringError``; and the chainer re-reads each backend's
    ``priority``, which raises a bare ``RuntimeError`` when D-Bus is gone. Either
    escapes a narrow handler untyped and with no remedy, so the CLI's
    ``CredentialError`` handler never sees it and the user gets a traceback
    instead of the one sentence that would help. Anything the keychain raises
    means the same thing: this machine cannot handle credentials right now.
    """
    return CredentialBackendUnavailable(
        f"the OS keychain could not {action} {name!r} ({exc}). Credentials are "
        f"never written to a plain file, so this machine cannot handle them until "
        f"a keychain backend is installed. Set "
        f"{ENV_ALLOW_ENV_CREDENTIALS}=1 to opt in to environment-supplied "
        f"credentials instead; nothing falls back to it silently.",
        name=name,
    )


def _env_name(name: str) -> str:
    return ENV_CREDENTIAL_PREFIX + name.upper().replace("-", "_")


def _env_override(name: str) -> str | None:
    """The opt-in environment value for ``name``, or None when not opted in."""
    if os.environ.get(ENV_ALLOW_ENV_CREDENTIALS) != "1":
        return None
    return os.environ.get(_env_name(name)) or None


def environment_value(name: str) -> str | None:
    """The opt-in environment value for ``name``, or None when it is not opted in.

    Public so that a caller who needs to know whether the fallback has a value,
    rather than whether the credential resolves, asks THIS module instead of
    re-reading the two variables itself. There is exactly one rule about when the
    environment may supply a credential, and a second reader spelling it again is
    a second rule that will eventually disagree with this one: the fallback would
    then be on for one caller and off for another with nothing in the config to
    explain it.
    """
    return _env_override(str(name))


def get(name: str) -> str:
    """Return the credential, or raise. Never returns None, never returns "".

    The return type is the contract. A function that can return None for "no
    keychain here" forces every caller to distinguish an absent credential from a
    broken machine by inspecting a falsy value, and callers do not, which is how
    an unauthenticated request goes out and comes back looking like an outage.
    """
    override = _env_override(name)
    if override:
        return override

    try:
        value = keyring.get_password(SERVICE, str(name))
    except Exception as exc:  # see _unavailable: the keychain's failures are open-ended
        raise _unavailable("read", str(name), exc) from exc
    if not value:
        raise CredentialMissing(
            f"no credential recorded for {name!r}. Record it before running a "
            f"workflow that needs it; Cratekit ships no credentials and will not "
            f"send an unauthenticated request in place of one.",
            name=str(name),
        )
    return value


def set(name: str, value: str) -> None:
    """Record a credential and note its NAME in the presence index.

    Named ``set`` even though it shadows the builtin inside this module, because
    every caller reaches it as ``secrets.set(...)`` where the builtin is not in
    play and the alternative names all read worse at the call site.

    Writing an empty value is refused rather than stored. An empty credential
    reads back as missing on some backends and as present-but-empty on others, so
    storing one makes the presence question unanswerable.

    THE WRITE IS VERIFIED BY READING IT BACK, and that costs one extra keychain
    call on a path that runs once per credential. ``keyring.backends.null.Keyring``
    is the documented way to disable keyring on a headless machine, and its
    ``set_password`` is a no-op that raises nothing. This module's argument for
    keying on the exception rather than probing a backend is that "the exception
    is an observation" - but a null backend offers no exception, so there is no
    observation to make, and something else has to be the one that fails loudly
    (R4).

    Without the read-back the failure is silent and then permanent: the value is
    discarded, the presence index records the name anyway, doctor reports the
    credential as set, every read raises ``CredentialMissing``, and the user
    follows that remedy, re-records it successfully, and loops forever.
    """
    if not value:
        raise CredentialMissing(
            f"refusing to record an empty value for {name!r}: an empty credential "
            f"reads back as absent on some keychain backends and as present on "
            f"others, so the presence check could not answer honestly.",
            name=str(name),
        )
    try:
        keyring.set_password(SERVICE, str(name), value)
        stored = keyring.get_password(SERVICE, str(name))
    except Exception as exc:  # see _unavailable: the keychain's failures are open-ended
        raise _unavailable("record", str(name), exc) from exc
    if stored != value:
        raise _unavailable(
            "record",
            str(name),
            RuntimeError("the keychain accepted the write and stored nothing"),
        )
    # Only after the read-back. The index must never claim a credential the
    # keychain does not actually hold, because the whole reason the index exists
    # is to answer the presence question without retrieving anything.
    _index_add(str(name))


def delete(name: str) -> None:
    """Remove a credential. Absent is not an error; the end state is what matters."""
    try:
        keyring.delete_password(SERVICE, str(name))
    except keyring.errors.PasswordDeleteError:
        pass
    except Exception as exc:  # see _unavailable: the keychain's failures are open-ended
        raise _unavailable("remove", str(name), exc) from exc
    _index_remove(str(name))


def get_json(name: str) -> dict:
    """Read a credential stored as one JSON blob.

    Multi-field credentials (a token, its refresh token, and the session fields
    that go with them) are stored as ONE entry rather than several. Several
    entries can be updated apart, and a half-refreshed session authenticates once
    and then fails in a way that looks like the service being down.
    """
    raw = get(name)
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise CredentialRejected(
            f"the stored credential for {name!r} is not readable as a session "
            f"blob; re-authenticate to replace it.",
            name=str(name),
        ) from exc
    if not isinstance(payload, dict) or not payload:
        raise CredentialRejected(
            f"the stored session for {name!r} is empty; re-authenticate.",
            name=str(name),
        )
    return payload


def set_json(name: str, payload: dict) -> None:
    """Store a multi-field credential as one blob, sorted so rewrites are stable."""
    set(name, json.dumps(payload, sort_keys=True))


# ---------------------------------------------------------------------------
# Presence, without retrieval
# ---------------------------------------------------------------------------


def exists(name: str) -> bool:
    """Answer "is this credential recorded" WITHOUT reading its value.

    Doctor asks this on every run. Answering it through the keychain would
    retrieve the value, and on macOS retrieving a value from a process the user
    has not already authorized raises an interactive authorization prompt, which
    in an unattended health check means the run hangs rather than reports.

    So presence is tracked separately, in an installation-scoped index that
    stores NAMES and never values. The honest limit: the index records what this
    installation wrote. A credential deleted out from under it through the OS
    keychain UI still reads as present here, and the code that actually uses the
    credential is what discovers otherwise, as ``CredentialMissing``.
    """
    if _env_override(str(name)):
        return True
    return str(name) in _index_read()


def recorded() -> frozenset[str]:
    """Every credential name this installation has recorded. Names only."""
    return _index_read()


def _index_path() -> Path:
    return config.state_path("credential_index")


def _index_read() -> frozenset[str]:
    """Read the recorded names.

    Returns a FROZEN set, and the helpers below build new ones with ``|`` and
    ``-`` rather than mutating. That is not a style preference: this module
    defines a function called ``set``, which shadows the builtin for every line
    below it, so a bare ``set()`` in a helper silently calls the credential
    writer instead of constructing a container. Working in immutable sets removes
    the landmine rather than stepping around it.
    """
    path = _index_path()
    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError):
        # A missing or mangled index is not a failure: it is "nothing recorded".
        # The index is derived data, and the keychain remains the truth.
        return frozenset()
    names = payload.get("recorded") if isinstance(payload, dict) else None
    if not isinstance(names, Iterable) or isinstance(names, str):
        return frozenset()
    return frozenset(str(n) for n in names)


def _index_write(names: Iterable[str]) -> None:
    """Write the presence index at 0600, atomically, on any umask.

    Through the config module's shared writer rather than ``Path.write_text``.
    This module exists because the source system's credential files are 0600 by
    the author's umask rather than by any code, so on a machine with a laxer umask
    they land world readable; writing this module's OWN sidecar with a plain text
    write re-introduced exactly that dependence, twenty lines from the correct
    primitive it already imports.

    The file carries no credential VALUES, and that is not the point. Under umask
    000 it lands world WRITABLE, so any other local account can forge or erase the
    answer doctor gives: add a name and a working install reports a credential
    that the keychain does not hold, remove one and a configured install reports
    as unconfigured.
    """
    payload = json.dumps({"recorded": sorted(names)}, indent=2) + "\n"
    config.atomic_write_bytes(payload.encode("utf-8"), _index_path())


def _index_add(name: str) -> None:
    names = _index_read()
    if name not in names:
        _index_write(names | {name})


def _index_remove(name: str) -> None:
    names = _index_read()
    if name in names:
        _index_write(names - {name})


__all__ = [
    "ENV_ALLOW_ENV_CREDENTIALS",
    "ENV_CREDENTIAL_PREFIX",
    "SERVICE",
    "Credential",
    "CredentialBackendUnavailable",
    "CredentialError",
    "CredentialMissing",
    "CredentialRejected",
    "Remedy",
    "backend_available",
    "delete",
    "environment_value",
    "exists",
    "get",
    "get_json",
    "recorded",
    "set",
    "set_json",
]
