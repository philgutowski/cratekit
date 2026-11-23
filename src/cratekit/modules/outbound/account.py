"""The one place a worker gets the streaming account it writes through.

``cratekit.modules.outbound.tidal_account`` implements
:class:`~cratekit.modules.outbound.service.RemoteAccount` over the provider
client ``acquire.provider_session.session_for`` holds for the process (U63,
U261). ``outbound-account-unbound`` is kept for the one case it still describes
truthfully: a build in which the adapter or its client library does not import.

**IT IS NOT A SECOND OWNER OF THE PROVIDER CREDENTIAL.**
``acquire.provider_session`` is its sole owner (R4), so this module reads only
whether ``secrets.Credential.PROVIDER_SESSION`` is RECORDED.

**MATCHING IS EXACT OR IT IS NOTHING**: by ISRC or an equally exact identity,
never a text search over title and artist, which would heart the wrong recording
on a catalogue full of remasters and edits.

**ONE ADAPTER PER PROCESS, ONE LOGIN SHARED WITH THE CATALOGUE (U261).** Both
workers call :func:`resolve` once per ITEM, and an adapter per item would log in
and read the favourites per item. So the first adapter resolved is held, and
handed out while the session it was built over is still the one
``provider_session`` holds: a 401 or 403 answered through the shared client
drops it, and so does a catalogue resolve that finds the keychain no longer
holds it. A reuse asks neither the keychain nor the gate. A session refused
through :func:`provider_failure` drops the adapter and the session it was built
over, so the catalogue logs in again too; :func:`forget` drops every hold. A
detached ``crate job resume`` is its own process and resolves its own.

Layer: modules.
"""

from __future__ import annotations

import importlib

from cratekit.acquire import provider_session
from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken
from cratekit.acquire.provider_session import ProviderUnavailable, answered_status, failure_links
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound.service import RemoteAccount

#: The module that implements :class:`RemoteAccount`, imported by NAME for the
#: reason ``label.catalogue.ADAPTER_MODULE`` gives: a ``from`` import answers from
#: the package attribute once the module has loaded anywhere in the process.
ADAPTER_MODULE = "cratekit.modules.outbound.tidal_account"

#: The adapter this process already opened, if any.
_OPENED: RemoteAccount | None = None

#: The shared session :data:`_OPENED` was built over, read off
#: ``provider_session.held`` when it was opened; None for an adapter over no
#: shared session, which then stays valid while none is held.
_OPENED_OVER: provider_session.HeldSession | None = None

#: The session module's remedies, carried into the product's vocabulary.
_REMEDIES = {
    remedy.value: remedy
    for remedy in (Remedy.REAUTHENTICATE_PROVIDER, Remedy.REPAIR_CREDENTIAL_STORE)
}

#: Statuses that judge the SESSION on a call after login, the session module's
#: own set. Narrower than ``provider_session.REJECTED_STATUSES``, which holds 400
#: because a login's bad request is a bad token; a heart answered 400 is a bad
#: request about that item.
SESSION_REFUSED_STATUSES = provider_session.SESSION_REFUSED_STATUSES


def _credential_missing(message: str, remedy: Remedy, scope: Scope) -> CratekitError:
    """A refusal a person answers by recording or renewing the provider session."""
    return refuse(
        "credential-missing", message, remedy=remedy, scope=scope, origin=("outbound", "account"),
        detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
    )


def bound() -> bool:
    """Whether this build can produce an account at all, asked WITHOUT trying.

    A queueing verb asks it to warn a person BEFORE they confirm. It answers
    about THIS BUILD, whether the adapter module and its client library import,
    so it reads no credential and spends no login, as :func:`resolve` would.
    """
    return provider_session.importable(ADAPTER_MODULE)


def forget() -> None:
    """Drop the adapter this process holds and the session it shares with the
    catalogue, so the next resolve of either logs in again."""
    global _OPENED, _OPENED_OVER
    _OPENED = None
    _OPENED_OVER = None
    provider_session.forget()


def _forget_refused() -> None:
    """Drop the held adapter and the shared session IT was built over.

    Only that session: one the catalogue logged in since was not the one
    refused, and dropping it would cost a login for nothing. An adapter built
    over no shared session forgets every hold, the safe direction.
    """
    global _OPENED, _OPENED_OVER
    over = _OPENED_OVER
    _OPENED = _OPENED_OVER = None
    if over is None:
        provider_session.forget()
    else:
        provider_session.drop(over)


def _session_refused(exc: BaseException) -> bool:
    """Whether a failure after login is the provider refusing the session.

    The walk follows context as well as cause (``core.cause.failure_links``,
    R-1305): the client decodes an error answer's body inside its own handler,
    so a 401 whose body is not JSON arrives as the decode error with the 401 as
    its context. A status counts on any link; the client's authentication error
    by name only on the declared cause chain.
    """
    for link, declared in failure_links(exc):
        if answered_status(link) in SESSION_REFUSED_STATUSES:
            return True
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False


def provider_failure(exc: BaseException, doing: str) -> CratekitError:
    """One provider call's failure, as the cause of the ITEM that made it.

    ITEM SCOPE ON PURPOSE: the job engine fails that item and claims the next,
    where a foreign exception would read as an internal defect and a run scoped
    cause would read one refused track as a dead sweep. A cause the product
    already raised passes through. A rejected session keeps the reauthenticate
    remedy, since a person told only to wait would wait for an outage that is
    not happening. Everything else is a wait.
    """
    if isinstance(exc, CratekitError):
        return exc
    if _session_refused(exc):
        # The held client is dead, so the next item resolves a fresh one.
        _forget_refused()
        return _credential_missing(
            f"the streaming provider rejected the session while trying to {doing} "
            f"({exc}); nothing further was written for this item",
            Remedy.REAUTHENTICATE_PROVIDER,
            Scope.ITEM,
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

    FOUR REFUSALS, EACH UNDONE BY A DIFFERENT ACT, the four
    ``label.catalogue.resolve`` raises: a provider not reached is a wait and the
    session is kept; a missing credential is the person's to record; a session
    the provider rejects, or an unreadable keychain, takes the session module's
    remedy; an adapter that does not import is this build's own gap.
    """
    global _OPENED, _OPENED_OVER
    # The credential is installation scoped; ``cfg`` is still handed on, since
    # the pacing gate reads the FROZEN one a job carries (R-705).
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise _credential_missing(
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
            Remedy.AUTHENTICATE_PROVIDER,
            Scope.RUN,
        )
    if _OPENED is not None and _OPENED_OVER is provider_session.held():
        return _OPENED
    _OPENED = _OPENED_OVER = None
    try:
        adapter = importlib.import_module(ADAPTER_MODULE)
    except ImportError as exc:
        raise refuse(
            "outbound-account-unbound",
            "a provider session is stored and the account adapter that would use "
            f"it to write a playlist or a heart does not import in this build "
            f"({exc}), so the queued work cannot be carried out. Nothing was "
            "written to the streaming account",
            steps=("reinstall the product so its core dependencies are present, then retry",),
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
        raise _credential_missing(
            f"the stored streaming provider session could not be used to open "
            f"the account ({exc})",
            _REMEDIES.get(exc.remedy.value, Remedy.REAUTHENTICATE_PROVIDER),
            Scope.RUN,
        ) from exc
    _OPENED = opened
    _OPENED_OVER = provider_session.held()
    return opened


__all__ = [
    "ADAPTER_MODULE", "SESSION_REFUSED_STATUSES", "bound", "forget", "provider_failure", "resolve",
]
