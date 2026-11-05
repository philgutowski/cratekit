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

A fourth joined them later, for the same reason and not as an exception to it:
``CredentialIndexUnusable`` means this installation's own presence sidecar could
not be locked, so the keychain is fine and what needs repairing is here.

A FIFTH IS NOT ONE OF THIS MODULE'S TYPES AT ALL, and the asymmetry is the point.
Reading that same sidecar and failing is a structured refusal carrying
``credential-index-unreadable``, because the locking failure is raised at two
call sites that both convert it and the READ has five call sites that convert
nothing. See :func:`_index_read`, which states what that cost before it refused.

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
from contextlib import contextmanager
from enum import StrEnum
from pathlib import Path

import keyring
import keyring.errors

from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse

#: The product-wide remediation vocabulary, aliased because this module declares
#: a ``Remedy`` of its own below and the two must not be confused. The local one
#: is the token carried on this module's four exception types; this one is the
#: token a structured refusal carries into the envelope, and U5 owns it.
from cratekit.core.exit_codes import Remedy as ProductRemedy

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
    #: The Bandcamp session: the browser's cookie for bandcamp.com, whose
    #: ``identity`` value is the login (U176). Recorded from a file, since the
    #: sign in form carries a CAPTCHA and the cookie is the only way in.
    BANDCAMP_SESSION = "bandcamp-session"
    #: Cratekit's own app on the streaming provider's developer platform (U205):
    #: the app's identifier and the key it is issued beside it, exchanged for a
    #: token under the client credentials flow. Catalogue lookups go under them
    #: when both are recorded, and under the account session when either is not.
    CATALOGUE_APP_ID = "catalogue-app-id"
    CATALOGUE_APP_KEY = "catalogue-app-key"


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

    A FOURTH type for the reason there are three: it needs its own remediation.
    The keychain is fine, the entry may be fine, and what is broken is this
    installation's own sidecar, so telling the user to install a backend or to
    re-enter a value is advice about the wrong thing.

    Refusing rather than writing unlocked is the same decision ``core/review``
    makes about its stores. Proceeding unlocked IS the defect being fixed, so
    degrading to it on a platform where advisory locking is unavailable would
    leave exactly that defect reachable by anybody on that platform.

    THE CONSEQUENCE, STATED RATHER THAN DISCOVERED: on a platform with no
    ``fcntl``, recording a credential refuses. That is the same thing the two
    decision stores in ``core/review`` already do there, so it is one product
    behaviour rather than a new one, and the unit that brings a lock primitive to
    that platform closes all three at once. It is not the shape ``core/jobs``
    uses; that one proceeds unlocked, on the argument that its claim is a
    transaction and the lock is only an early refusal, which is not true here.
    """

    remedy = Remedy.REPAIR_CREDENTIAL_STORE


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

    WHAT IS NOT INTERPOLATED: the backend's own MESSAGE. Only its type name goes
    into the refusal. This string reaches the wizard's check table, standard
    error and the JSON envelope, so a backend that puts the value it was handed
    into its exception message would put a credential into all three, and a
    backend is third-party code whose message text is not ours to bound. The type
    name is what tells the failures apart; the message is what could carry a
    secret. The original exception is still chained for a developer reading a
    traceback, which no user-facing path prints.
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

    THE INDEX LOCK IS TAKEN BEFORE THE KEYCHAIN IS TOUCHED, and the order is the
    fix for a defect the lock itself introduced. Taken afterwards, an
    unobtainable lock refused a write that had ALREADY happened: the keychain
    held the value, the index did not name it, ``exists`` answered False, and
    doctor sent the user to record a credential the machine was already holding,
    which is the exact failure the lock was added to prevent, reachable through
    the lock's own refusal. Now the refusal happens while both stores are still
    untouched, so a refusal means nothing changed anywhere.

    What that leaves is one narrow window and it fails in the safe direction: the
    keychain write succeeds and the index write then fails on its own (a full
    disk). The value is stored and reads as unrecorded, so the user records it
    again, which is idempotent. The opposite order would leave the index naming a
    credential the keychain never accepted, which is the loop above.

    THE SAME WINDOW, WHEN WHAT FAILS IS THE READ INSIDE IT, IS LOUD INSTEAD. The
    cycle at the end reads the existing names before writing them back, so an
    index it cannot read refuses and this call raises after the keychain already
    holds the value. That is the right end of the trade. Answering empty there
    and writing the one new name would drop every other recorded name from the
    index, turning one unreadable read into a permanent false report about the
    credentials it was not even asked about.
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
        # Only after the read-back. The index must never claim a credential the
        # keychain does not actually hold, because the whole reason the index
        # exists is to answer the presence question without retrieving anything.
        _record_name(str(name))


def delete(name: str) -> None:
    """Remove a credential. Absent is not an error; the end state is what matters.

    THE INDEX ENTRY GOES FIRST, under the lock, and the keychain entry second.
    The reverse order is what shipped and it produced the one disagreement that
    makes a report lie: the keychain entry was removed, the index write then
    failed or was refused, and ``exists`` answered TRUE for a credential that was
    gone, so doctor reported green over nothing and the workflow that spent it
    failed later with a missing credential.

    This order cannot produce that. A failure between the two leaves the index
    saying "not recorded" for a value the keychain may still hold, which reads as
    work to do rather than as work already done, and re-recording is idempotent.
    Taking the lock first means a lock that cannot be taken changes neither
    store at all.
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

    FALSE IS AN ANSWER AND IT IS ONLY GIVEN WHEN ONE WAS OBSERVED. An index this
    account cannot open, or one whose bytes do not say what is recorded, raises
    rather than answering, because the caller cannot tell those from a real
    absence and the whole product downstream reads False as a statement of fact.
    See :func:`_index_read`.
    """
    if _env_override(str(name)):
        return True
    return str(name) in _index_read()


def recorded() -> frozenset[str]:
    """Every credential name this installation has recorded. Names only.

    Raises rather than answering empty for an index that could not be read, for
    the reason :func:`exists` states: an empty answer here is rendered to a
    person as a list of what they have, and a list that is short because nobody
    could look is the worst of the three states to report as the first.
    """
    return _index_read()


def _index_path() -> Path:
    return config.state_path("credential_index")


#: What a refusal from the reader says about the two stores, one sentence per
#: caller. Declared here rather than written inline so the three read as a set and
#: a fourth caller has to pick one rather than inherit whichever was nearest.
READ_LEFT_UNTOUCHED = (
    "Nothing was stored or removed by the attempt to read it, and the keychain "
    "still holds whatever it held; what is unknown is the list of names, never "
    "the values."
)

#: ``_record_name`` is reached from ``set`` only after the keychain write and its
#: read back have both succeeded, so this one has to say that the value LANDED.
#: Without it the person repairs the sidecar believing nothing was written, and
#: the act they would otherwise take, recording it again, cannot move the file
#: that refused.
RECORD_ALREADY_IN_THE_KEYCHAIN = (
    "THE VALUE IS IN THE KEYCHAIN. It was stored and read back before this index "
    "was opened, and what could not be done is note its name here, so it reads "
    "as not recorded until the index is repaired. Recording it again is harmless "
    "and does not fix that."
)

#: ``delete`` clears the index entry BEFORE the keychain entry, so a refusal from
#: the read at the start of that cycle has touched neither store.
REMOVE_NOTHING_TOUCHED = (
    "Nothing was removed. The index entry is cleared before the keychain entry, "
    "so a refusal here leaves both stores exactly as they were."
)


def _index_read(left: str = READ_LEFT_UNTOUCHED) -> frozenset[str]:
    """Read the recorded names, or refuse. THREE STATES, NOT ONE.

    Returns a FROZEN set, and the helpers below build new ones with ``|`` and
    ``-`` rather than mutating. That is not a style preference: this module
    defines a function called ``set``, which shadows the builtin for every line
    below it, so a bare ``set()`` in a helper silently calls the credential
    writer instead of constructing a container. Working in immutable sets removes
    the landmine rather than stepping around it.

    WHAT THIS USED TO DO AND WHY IT WAS WRONG. It caught ``OSError``
    and ``ValueError`` alike and answered with an empty set, on the argument that
    the index is derived data and the keychain remains the truth. The argument is
    correct about the DATA and wrong about the ANSWER. Nothing downstream re-reads
    the keychain: ``exists`` is the only presence question the product asks, so an
    index this account cannot open made doctor report a stored credential as not
    recorded with ``set-credential`` beside it, and made three verbs refuse
    ``credential-missing`` over a keychain that was holding the value. Recording
    it again does not move the index, so the person follows that remedy for ever,
    which is the loop R-116 measured, reached here from a permission rather than
    from a race. It is the first of this project's four recurring patterns,
    absence read as evidence of absence.

    THE ONE STATE THAT MEANS NOTHING RECORDED IS ENOENT. A fresh installation has
    no index and must answer empty rather than refuse, or the product cannot be
    set up at all. Everything else is a read that established nothing:

    * another ``OSError``, so the file is there and this account could not get
      its bytes. Raised ``from`` the original, which is what lets
      ``cause.classified`` turn EACCES or EPERM into ``path-permission-denied``
      with ``grant-path-access``, and EROFS into its own act, without a word
      about permissions being written here. That reclassification is why this
      site names the FILE and never the reason a kernel refused it.
    * bytes that are not JSON, or a payload whose ``recorded`` key is not a list
      of names. The file was read and does not say what is recorded, which is a
      different act to repair and keeps ``repair-credential-store``.

    A STRUCTURED REFUSAL RATHER THAN ``CredentialIndexUnusable``, which is the
    sibling type the lock raises. The lock's refusal is caught by both call sites
    that take it, the login verb and the setup wizard, and converted there.
    ``exists`` has five call sites and no handler at any of them, so a bare
    exception would reach the dispatcher's unstructured blanket and come out as
    ``internal-error`` with "report this defect" for the damaged case, over a
    person's own state directory. A ``CratekitError`` lands with its reserved
    code through the ``except CratekitError`` leg that doctor's check runner and
    the dispatcher both already have.

    ``left`` IS THE CALLER'S SENTENCE ABOUT THE TWO STORES, and it is a parameter
    for the same reason ``_index_locked`` takes ``action``: this function is
    reached from a plain read, from the middle of a record and from the start of
    a remove, and those leave the keychain in three different states. Written as
    one sentence here it was wrong twice. It said nothing had been stored, while
    ``_record_name`` is only reached from ``set`` AFTER the keychain write and its
    read back have both succeeded, so the person was told to repair the sidecar
    believing the value had not landed, and the obvious next act, recording it
    again, cannot fix the thing that actually refused.
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

    One slug with the unreadable case above, because the act that repairs both is
    the same one and ``cause.REASONS`` gives a slug per ACT rather than per
    trigger. What differs is the sentence, which is the half a call site is still
    allowed to own, and ``detail`` carries the two apart for a machine consumer.
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


def _index_lock_path() -> Path:
    return config.state_path("credential_index_lock")


@contextmanager
def _index_locked(action: str = "update"):
    """Hold the sibling lock across ONE read then write cycle over the index.

    MEASURED, not theorised. Two processes recording one credential each left the
    keychain holding both and this index naming one, in 23 of 25 trials, and both
    calls returned normally. Three concurrent adds lost at least one in 40 of 40.
    The read and the write are a cycle, and an unlocked cycle over a shared
    document loses whatever the other writer put there between them.

    THE LOSS IS THE ONE THAT MAKES A REPORT LIE. ``exists`` is what doctor asks
    to answer "is this credential recorded" without retrieving a value, so a name
    that never lands reads as ``not recorded`` for a credential the keychain
    holds, and the remedy sends the user to record it again.

    BLOCKING, like the other two stores in this product: two processes recording
    credentials should serialize rather than raise at a person. The lock file
    persists after release, for the reason the config lock states at length:
    unlinking the name lets a second process lock a fresh inode while the first
    still holds the old one, and both then believe they are alone.

    ``action`` names what the caller was about to do, so the refusal can say that
    NOTHING was done. Callers take this lock before touching the keychain, not
    after, so "the index could not be locked" and "nothing changed" are the same
    sentence, and the message has to say so or the user is left guessing whether
    a value was stored.
    """
    config._mkdir_private(_index_lock_path().parent)
    handle = None
    try:
        import fcntl

        # os.open with an explicit mode rather than the builtin open(), which
        # creates at 0666 masked by the umask. A world-writable lock is one any
        # local account can hold, which turns every future credential write into
        # a refusal.
        descriptor = os.open(_index_lock_path(), os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
        handle = os.fdopen(descriptor, "r+b")
        # O_CREAT applies the mode only when it CREATES the file, so a lock left
        # behind at another mode would keep it without this. Guarded the way the
        # config writer guards its own chmod: a POSIX mode is meaningless on some
        # platforms, and a health-adjacent path must not raise over one.
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

    Split from the locking wrapper because ``flock`` is held per open file
    description, so a second acquisition from inside a cycle that already holds
    one deadlocks against itself. ``set`` and ``delete`` take the lock around
    their whole operation, keychain included, so they call these directly.

    EACH HALF TELLS THE READER WHAT ITS OWN POSITION IN THE CYCLE LEFT BEHIND.
    This one runs after the keychain already holds the value; the other runs
    before the keychain has been touched at all. The reader cannot see which it
    was called from, so the sentence comes from here.
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
