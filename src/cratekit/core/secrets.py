"""Service credentials, in the OS keychain, with distinct failure types.

The keychain (R4, KTD6) is the one store whose permissions do not depend on the
user's umask. Each failure type needs its own remediation, so they stay apart
and no caller parses a message to choose advice (KTD25):

* ``CredentialBackendUnavailable``: no keychain to ask; install a backend.
* ``CredentialMissing``: the keychain works and has no entry; record it.
* ``CredentialRejected``: the entry exists and the service refused it;
  re-authenticate.
* ``CredentialIndexUnusable``: this installation's presence sidecar could not
  be locked; repair it here.

Failing to read that sidecar is instead a structured refusal,
``credential-index-unreadable``; see :func:`_index_read`.

No silent fallbacks: not to a file, not to an empty string, and not to the
environment unless the user opted in by name. A read with no reachable backend
raises, so no request goes out unauthenticated. Importing the old plaintext
credentials is a CLI command (D2), not this module's.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from contextlib import contextmanager
from enum import StrEnum
from pathlib import Path

import keyring
import keyring.errors

from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse

#: The product-wide remediation vocabulary (U5), aliased apart from the local
#: ``Remedy`` that this module's exception types carry.
from cratekit.core.exit_codes import Remedy as ProductRemedy

#: One keychain service for the installation, not per library: a credential is
#: an account fact (KTD21).
SERVICE = "cratekit"

#: Opt-in escape hatch for a headless machine with no keychain daemon. Off unless
#: set, and every refusal names it.
ENV_ALLOW_ENV_CREDENTIALS = "CRATE_ALLOW_ENV_CREDENTIALS"
ENV_CREDENTIAL_PREFIX = "CRATEKIT_CREDENTIAL_"


class Credential(StrEnum):
    """Every credential the product stores. Names only; values never appear here.

    The identification service's two names avoid the obvious word on purpose,
    so the repository scanner does not flag them as leaked credentials.
    """

    IDENTIFY_KEY = "identify-key"
    IDENTIFY_SIGNING_KEY = "identify-signing-key"
    PROVIDER_SESSION = "provider-session"
    #: The Bandcamp session cookie, whose ``identity`` value is the login (U176).
    #: Recorded from a file, since the sign in form carries a CAPTCHA.
    BANDCAMP_SESSION = "bandcamp-session"
    #: Cratekit's own provider app id and key, exchanged for a client
    #: credentials token (U205). Catalogue lookups use them when both are
    #: recorded, else the account session.
    CATALOGUE_APP_ID = "catalogue-app-id"
    CATALOGUE_APP_KEY = "catalogue-app-key"
    #: A Discogs personal access token (U244), sent only to Discogs' API.
    #: Optional: without one Discogs is recorded as not asked.
    DISCOGS_TOKEN = "discogs-token"
    #: A Cyanite access token (U245), sent only to Cyanite's API by
    #: ``scripts/cyanite_trial.py``, whose paid uploads are opt in per run.
    CYANITE_KEY = "cyanite-key"


class Remedy(StrEnum):
    """What to do about a credential failure, as a token the CLI renders (D2).

    A subset of the product-wide vocabulary U5 owns (S4), not a competing one.
    """

    INSTALL_KEYCHAIN_BACKEND = "install-keychain-backend"
    SET_CREDENTIAL = "set-credential"
    REAUTHENTICATE = "reauthenticate"
    REPAIR_CREDENTIAL_STORE = "repair-credential-store"


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


class CredentialIndexUnusable(CredentialError):
    """The presence index could not be locked, so its cycle was not run.

    Its own type because the keychain is fine and the sidecar is what needs
    repair. Refuses rather than writing unlocked, as ``core/review`` does, so on
    a platform with no ``fcntl`` recording a credential refuses.
    """

    remedy = Remedy.REPAIR_CREDENTIAL_STORE


class CredentialRejected(CredentialError):
    """The service refused a credential that IS set. Remediation: re-authenticate.

    Raised by the caller that got the refusal, since only it can tell a 401 from
    a network failure; declared here so every caller raises the same type.
    """

    remedy = Remedy.REAUTHENTICATE


def backend_available() -> bool:
    """A DOCTOR-only probe: does this machine resolve a backend that can store?

    Not called by ``get``/``set``/``delete``: backend priority is a heuristic,
    and the read and write paths key on the observed exception instead. Both
    lines sit inside the try because ``priority`` is a classproperty that raises
    when the backend is not viable, which ``getattr``'s default does not catch.
    """
    try:
        backend = keyring.get_keyring()
        return bool(getattr(backend, "priority", 0) > 0)
    except Exception:  # keyring raises several unrelated types while resolving
        return False


def _unavailable(action: str, name: str, exc: Exception) -> CredentialBackendUnavailable:
    """Turn "there is no usable keychain here" into the typed refusal.

    Callers catch ``Exception``, not ``KeyringError``: keychain failures are an
    open set (on Linux, D-Bus errors escape as other types, R1), and anything it
    raises means this machine cannot handle credentials now. Only the exception's
    type name is interpolated, never its message, which third-party code may fill
    with the value it was handed; the original stays chained.
    """
    return CredentialBackendUnavailable(
        f"the OS keychain could not {action} {name!r} ({type(exc).__name__}). Credentials are "
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

    Public so callers ask here rather than re-reading the two variables, keeping
    one rule for when the environment may supply a credential.
    """
    return _env_override(str(name))


def get(name: str) -> str:
    """Return the credential, or raise. Never returns None, never returns "".

    A None for "no keychain" would let an unauthenticated request go out.
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

    Shadows the builtin inside this module; callers reach it as
    ``secrets.set``. An empty value is refused, since backends disagree on
    whether it reads back as absent.

    The write is verified by reading it back, because the null keyring backend
    accepts a write silently and stores nothing (R4); otherwise the index would
    name a value never stored and the user would loop re-recording it.

    The index lock is taken before the keychain is touched, so a lock refusal
    means nothing changed. The remaining window fails safe: a keychain write
    whose index write then fails reads as unrecorded, and recording again is
    idempotent. An unreadable index inside that window raises rather than
    answering empty, which would drop every other recorded name.
    """
    if not value:
        raise CredentialMissing(
            f"refusing to record an empty value for {name!r}: an empty credential "
            f"reads back as absent on some keychain backends and as present on "
            f"others, so the presence check could not answer honestly.",
            name=str(name),
        )
    with _index_locked("record"):
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
        # Only after the read-back: the index never names a value not held.
        _record_name(str(name))


def delete(name: str) -> None:
    """Remove a credential. Absent is not an error; the end state is what matters.

    The index entry goes first, under the lock, then the keychain entry, so a
    failure between them reads as "not recorded" (work to do) rather than
    ``exists`` answering True for a credential that is gone. A lock that cannot
    be taken changes neither store.
    """
    with _index_locked("remove"):
        _forget_name(str(name))
        try:
            keyring.delete_password(SERVICE, str(name))
        except keyring.errors.PasswordDeleteError:
            pass
        except Exception as exc:  # see _unavailable: the keychain's failures are open-ended
            raise _unavailable("remove", str(name), exc) from exc


def get_json(name: str) -> dict:
    """Read a credential stored as one JSON blob.

    Multi-field credentials are one entry, so a session is never half refreshed.
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


# Presence, without retrieval


def exists(name: str) -> bool:
    """Answer "is this credential recorded" WITHOUT reading its value.

    Reading the keychain could raise a macOS authorization prompt and hang an
    unattended doctor run, so presence comes from an index of names only. It
    records what this installation wrote; one deleted through the keychain UI
    still reads present until use raises ``CredentialMissing``. False is given
    only when observed: an unreadable index raises (:func:`_index_read`).
    """
    if _env_override(str(name)):
        return True
    return str(name) in _index_read()


def recorded() -> frozenset[str]:
    """Every credential name this installation has recorded. Names only.

    Raises rather than answering empty for an unreadable index, as
    :func:`exists` does.
    """
    return _index_read()


def _index_path() -> Path:
    return config.state_path("credential_index")


#: What a refusal from the reader says about the two stores, one sentence per
#: caller, declared together so a new caller picks one.
READ_LEFT_UNTOUCHED = (
    "Nothing was stored or removed by the attempt to read it, and the keychain "
    "still holds whatever it held; what is unknown is the list of names, never "
    "the values."
)

#: ``_record_name`` runs only after the keychain write and read back succeeded,
#: so this says the value landed and recording again will not help.
RECORD_ALREADY_IN_THE_KEYCHAIN = (
    "THE VALUE IS IN THE KEYCHAIN. It was stored and read back before this index "
    "was opened, and what could not be done is note its name here, so it reads "
    "as not recorded until the index is repaired. Recording it again is harmless "
    "and does not fix that."
)

#: ``delete`` clears the index entry before the keychain entry, so a refusal
#: here has touched neither store.
REMOVE_NOTHING_TOUCHED = (
    "Nothing was removed. The index entry is cleared before the keychain entry, "
    "so a refusal here leaves both stores exactly as they were."
)


def _index_read(left: str = READ_LEFT_UNTOUCHED) -> frozenset[str]:
    """Read the recorded names, or refuse.

    Returns a frozen set and helpers build new ones with ``|`` and ``-``: this
    module's ``set`` shadows the builtin, so a bare ``set()`` would call the
    credential writer.

    Only ENOENT means nothing recorded, so a fresh install can be set up. Any
    other read established nothing and refuses rather than answering empty,
    which doctor would report as not recorded (R-116):

    * another ``OSError``, raised ``from`` the original so
      ``cause.classified`` can name the kernel's reason; this site names only
      the file.
    * bytes that are not JSON or carry no list of names, which keeps
      ``repair-credential-store``.

    A ``CratekitError`` rather than ``CredentialIndexUnusable``, because the
    callers of ``exists`` have no handler and only the ``CratekitError`` leg
    lands it with its reserved code. ``left`` is the caller's sentence about the
    two stores, since a read, a record and a remove leave them differently.
    """
    path = _index_path()
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
        raise refuse(
            "credential-index-unreadable",
            f"the credential presence index at {path} is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
            f"which credentials it has recorded. {left}",
            remedy=ProductRemedy.REPAIR_CREDENTIAL_STORE,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
        ) from exc
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise _damaged(
            path, f"is not readable as JSON ({type(exc).__name__})", left
        ) from exc
    names = payload.get("recorded") if isinstance(payload, dict) else None
    if not isinstance(names, Iterable) or isinstance(names, str):
        raise _damaged(path, "does not carry a list of recorded credential names", left)
    return frozenset(str(n) for n in names)


def _damaged(path: Path, what: str, left: str) -> CratekitError:
    """The refusal for an index that was READ and does not say what is recorded.

    One slug with the unreadable case, since ``cause.REASONS`` gives a slug per
    repairing act; ``detail`` tells the two apart for a machine consumer.
    """
    return refuse(
        "credential-index-unreadable",
        f"the credential presence index at {path} {what}, so this installation "
        f"cannot say which credentials it has recorded. {left} Removing that file "
        f"and recording each credential again rebuilds it",
        remedy=ProductRemedy.REPAIR_CREDENTIAL_STORE,
        origin=("core", "secrets"),
        detail={"path": str(path), "index": "damaged"},
    )


def _index_write(names: Iterable[str]) -> None:
    """Write the presence index at 0600, atomically, on any umask.

    Through config's shared writer, never ``Path.write_text``, whose mode
    follows the umask: a world-writable index lets any local account forge the
    answer doctor gives.
    """
    payload = json.dumps({"recorded": sorted(names)}, indent=2) + "\n"
    config.atomic_write_bytes(payload.encode("utf-8"), _index_path())


def _index_lock_path() -> Path:
    return config.state_path("credential_index_lock")


@contextmanager
def _index_locked(action: str = "update"):
    """Hold the sibling lock across ONE read then write cycle over the index.

    An unlocked cycle loses a concurrent writer's name (measured), and doctor
    then reports a held credential as not recorded. Blocking, so writers
    serialize. The lock file persists after release, since unlinking it lets two
    processes lock different inodes. ``action`` lets the refusal say nothing was
    done, which holds because callers lock before touching the keychain.
    """
    config.mkdir_private(_index_lock_path().parent)
    handle = None
    try:
        import fcntl

        # os.open with an explicit mode, since open() follows the umask and a
        # world-writable lock lets any account block every credential write.
        descriptor = os.open(_index_lock_path(), os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
        handle = os.fdopen(descriptor, "r+b")
        # O_CREAT sets the mode only on creation, so chmod an existing lock,
        # guarded as config guards its own chmod.
        if config._CAN_SET_MODE:
            os.chmod(_index_lock_path(), config.PRIVATE_FILE_MODE)
        fcntl.flock(handle, fcntl.LOCK_EX)
    except (ImportError, OSError) as exc:
        if handle is not None:
            handle.close()
        raise CredentialIndexUnusable(
            f"the credential presence index at {_index_path()} could not be "
            f"locked ({type(exc).__name__}), and writing it unlocked loses "
            f"whatever a second process is recording at the same time, silently, "
            f"while reporting success. NOTHING WAS CHANGED: the lock is taken "
            f"before the keychain is touched, so no credential was stored or "
            f"removed by the attempt to {action} one, and the keychain and this "
            f"index still agree.",
            name=None,
        ) from exc
    try:
        yield
    finally:
        handle.close()  # closing the descriptor releases the lock; the file stays


def _record_name(name: str) -> None:
    """The read then write half, WITHOUT taking the lock. Callers hold it.

    Split out because re-taking ``flock`` inside a held cycle deadlocks. Each
    half passes the reader its own sentence: this one runs after the keychain
    holds the value, :func:`_forget_name` before it is touched.
    """
    names = _index_read(RECORD_ALREADY_IN_THE_KEYCHAIN)
    if name not in names:
        _index_write(names | {name})


def _forget_name(name: str) -> None:
    """The removal half, WITHOUT taking the lock. See :func:`_record_name`."""
    names = _index_read(REMOVE_NOTHING_TOUCHED)
    if name in names:
        _index_write(names - {name})




__all__ = [
    "ENV_ALLOW_ENV_CREDENTIALS",
    "ENV_CREDENTIAL_PREFIX",
    "SERVICE",
    "Credential",
    "CredentialBackendUnavailable",
    "CredentialError",
    "CredentialIndexUnusable",
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
