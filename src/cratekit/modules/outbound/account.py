"""The one place a worker gets the streaming account it writes through.

**U63 BOUND IT.** ``cratekit.modules.outbound.tidal_account`` implements
:class:`~cratekit.modules.outbound.service.RemoteAccount` over a provider client
that ``acquire.provider_session.client_session`` logs in from the stored session,
the same factory the label catalogue uses. Before that unit no implementation
shipped and this module refused every call with ``outbound-account-unbound``.
That refusal is kept for the one case it still describes truthfully: a build in
which the adapter or its client library does not import.

**IT IS NOT A SECOND OWNER OF THE PROVIDER CREDENTIAL.**
``cratekit.acquire.provider_session`` opens by declaring itself the sole owner
under R4, and both outbound verbs already declare the ``credential.provider``
doctor check, which resolves ``secrets.Credential.PROVIDER_SESSION``. So this
module reads whether that credential is RECORDED, and every read of the token
itself is the session module's.

**MATCHING IS EXACT OR IT IS NOTHING.** Inherited from the source system and not
obvious from the protocol: matching is by ISRC or an equally exact identity,
never by a text search over title and artist. A collection export carries no
ISRC, so the favourites sweep offers this seam a rekordbox row identifier and
nothing more, and an adapter that closed that gap with a search would heart the
wrong recording on a catalogue full of remasters and edits.

**ONE ADAPTER PER PROCESS.** Both workers call :func:`resolve` once per ITEM. A
fresh adapter per item would log in per item and read the favourites per item,
which is the thousand listing calls the adapter's one read rule exists to avoid.
So the first successful resolve is held and handed to every later call in the
process; :func:`forget` drops it. A detached ``crate job resume`` is its own
process and resolves its own.

Layer: modules.
"""

from __future__ import annotations

import importlib

from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken
from cratekit.acquire.provider_session import (
    ProviderUnavailable,
    answered_status,
    failure_links,
)
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound.service import RemoteAccount

#: The module that implements :class:`RemoteAccount`. Imported by NAME for the
#: reason ``label.catalogue.ADAPTER_MODULE`` gives: a ``from`` import answers from
#: the package attribute once the module has loaded anywhere in the process.
ADAPTER_MODULE = "cratekit.modules.outbound.tidal_account"

#: The adapter this process already opened, if any. See the module docstring.
_OPENED: RemoteAccount | None = None

#: The session module's remedy, carried into the product's vocabulary, as
#: ``label.catalogue`` carries it.
_REMEDIES = {
    Remedy.REAUTHENTICATE_PROVIDER.value: Remedy.REAUTHENTICATE_PROVIDER,
    Remedy.REPAIR_CREDENTIAL_STORE.value: Remedy.REPAIR_CREDENTIAL_STORE,
}


def bound() -> bool:
    """Whether this build can produce an account at all, asked WITHOUT trying.

    A queueing verb asks this so it can warn a person BEFORE they confirm, at the
    one moment the information is still useful to them. :func:`resolve` is the
    wrong question there: it is the worker's, it reads the credential and logs a
    client in, and asking it at enqueue would spend a login on a warning.

    It answers about THIS BUILD and not this machine, so it reads no credential:
    whether the adapter module imports, which includes its client library. Until
    U63 it returned a constant ``False``.
    """
    try:
        importlib.import_module(ADAPTER_MODULE)
    except ImportError:
        return False
    return True


def forget() -> None:
    """Drop the adapter this process holds, so the next resolve opens a new one."""
    global _OPENED
    _OPENED = None


#: Statuses that judge the SESSION on a call made after login. Narrower than
#: ``provider_session.REJECTED_STATUSES``, which includes 400 because a login's
#: bad request is a bad token; a heart or a playlist add answered 400 is a bad
#: request about that item, and telling that person to log in again is wrong.
SESSION_REFUSED_STATUSES = frozenset({401, 403})


def _session_refused(exc: BaseException) -> bool:
    """Whether a failure after login is the provider refusing the session.

    The walk is the login's, ``core.cause.failure_links`` (moved there from
    ``provider_session`` by R-1313, which still imports it), which departs
    from ``core.cause._chain`` by following context too (R-1305): the client
    decodes an error answer's body inside its own handler of the HTTP error,
    so a 401 whose body is not JSON arrives as the decode error with the 401
    as its context. A status counts on any link it reaches; the client's
    authentication error by name only on the declared cause chain.
    """
    for link, declared in failure_links(exc):
        if answered_status(link) in SESSION_REFUSED_STATUSES:
            return True
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False


def provider_failure(exc: BaseException, doing: str) -> CratekitError:
    """One provider call's failure, as the cause of the ITEM that made it.

    ITEM SCOPE ON PURPOSE. A heart or a playlist add that the provider refused
    condemns that item, and the job engine fails it and claims the next. A
    foreign exception reaching the engine instead would read as an internal
    defect, and a run scoped cause would read one refused track as a dead sweep.

    A cause the product already raised passes through untouched. A rejected
    credential keeps its own slug and the reauthenticate remedy, because a person
    told only that the provider was unavailable would wait for an outage that is
    not happening. Everything else is a wait.
    """
    if isinstance(exc, CratekitError):
        return exc
    if _session_refused(exc):
        # The held adapter's client is dead, so the next item resolves a fresh
        # one from the keychain rather than failing on this one for the rest of
        # the process, and a login made meanwhile is picked up.
        forget()
        return refuse(
            "credential-missing",
            f"the streaming provider rejected the session while trying to {doing} "
            f"({exc}); nothing further was written for this item",
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
            scope=Scope.ITEM,
            origin=("outbound", "account"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        )
    return refuse(
        "unavailable-transient",
        f"the streaming provider failed while trying to {doing} ({exc}); resume "
        f"the job to retry this item",
        remedy=Remedy.RETRY_LATER,
        scope=Scope.ITEM,
        origin=("outbound", "account"),
    )


def resolve(cfg: config.Config) -> RemoteAccount:
    """The account this library's outbound writes go to, or why there is none.

    FOUR REFUSALS, EACH UNDONE BY A DIFFERENT ACT, the same four
    ``label.catalogue.resolve`` raises. A provider that could not be reached is a
    wait, and the stored session is kept because nobody judged it. A missing
    credential is the person's to record and doctor already says how. A stored
    session the provider rejects, or a keychain that cannot be read, is the same
    slug with the remedy the session module chose. An adapter that does not
    import is this build's own gap, and authenticating again would not move it.
    """
    global _OPENED
    # The credential is installation scoped and the library does not pick it;
    # the configuration is still handed on, because the pacing gate reads its
    # interval and cooldown off the FROZEN one a job carries (R-705).
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("outbound", "account"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        )
    if _OPENED is not None:
        return _OPENED
    try:
        adapter = importlib.import_module(ADAPTER_MODULE)
    except ImportError as exc:
        raise refuse(
            "outbound-account-unbound",
            "a provider session is stored and the account adapter that would use "
            f"it to write a playlist or a heart does not import in this build "
            f"({exc}), so the queued work cannot be carried out. Nothing was "
            "written to the streaming account",
            steps=(
                "reinstall the product so its core dependencies are present, then "
                "retry",
            ),
            scope=Scope.RUN,
            origin=("outbound", "account"),
        ) from exc
    try:
        opened = adapter.open_account(cfg)
    except ProviderUnavailable as exc:
        raise refuse(
            "unavailable-transient",
            f"the streaming provider could not be reached to open the account "
            f"({exc}); the stored session was not judged and is kept",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.RUN,
            origin=("outbound", "account"),
        ) from exc
    except (AdapterAuthFailed, AdapterBroken) as exc:
        raise refuse(
            "credential-missing",
            f"the stored streaming provider session could not be used to open "
            f"the account ({exc})",
            remedy=_REMEDIES.get(exc.remedy.value, Remedy.REAUTHENTICATE_PROVIDER),
            scope=Scope.RUN,
            origin=("outbound", "account"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        ) from exc
    _OPENED = opened
    return opened


__all__ = [
    "ADAPTER_MODULE",
    "SESSION_REFUSED_STATUSES",
    "bound",
    "forget",
    "provider_failure",
    "resolve",
]
