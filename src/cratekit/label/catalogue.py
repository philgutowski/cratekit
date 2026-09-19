"""The one place the label package gets the catalogue it reads a provider through.

**U62 BOUND IT.** ``cratekit.label.tidal_catalogue`` implements :class:`Catalogue`
over a provider client that ``acquire.provider_session.client_session`` logs in
from the stored session. Before that unit no implementation shipped, and this
module refused every call with ``label-catalogue-unbound``. That refusal is kept
for the one case it still describes truthfully: a build in which the adapter or
its client library does not import.

**IT IS NOT A SECOND OWNER OF THE PROVIDER CREDENTIAL.**
``cratekit.acquire.provider_session`` opens by declaring itself the sole owner
under R4, and ``cratekit.modules.outbound.account`` already reads presence for
the outbound half of the product. So this module reads whether
``secrets.Credential.PROVIDER_SESSION`` is RECORDED, and every read of the token
itself is the session module's. Without the split, ``crate doctor`` would report
the provider credential healthy while the verb said only that nothing was bound,
and a person would go looking for a login problem they do not have.

**WHY IT IS ITS OWN SEAM AND NOT THE OUTBOUND ONE.** ``RemoteAccount`` is
add-only writes against an account. This is reads against a catalogue, and the
two share a credential rather than a capability. A build could plausibly gain one
and not the other, and a person asked to sweep their favourite labels who was
told the streaming ACCOUNT is unbound would go looking at the wrong half of the
product.

**THE TEST SUBSTITUTION IS IN PROCESS ONLY.** A test replaces :func:`resolve` on
this module and the callers pick it up because they look it up at call time. The
child ``crate job resume`` spawns is a fresh process and inherits nothing, which
since U62 is harmless in a shipped build: the child resolves the real adapter
from the same keychain.

Layer: modules.
"""

from __future__ import annotations

import importlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken
from cratekit.acquire.provider_session import ProviderUnavailable
from cratekit.core import config, secrets
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import registry

#: The module that implements :class:`Catalogue`. Imported by NAME through
#: ``importlib`` rather than by a ``from`` import, because a ``from`` import
#: answers from the package attribute once the module has loaded anywhere in the
#: process, and would then say the adapter imports in a build that has just been
#: told it does not.
ADAPTER_MODULE = "cratekit.label.tidal_catalogue"


@dataclass(frozen=True, slots=True)
class AccountPlaylist:
    """One playlist the account itself created, reduced to what a sweep decides on.

    ``playlist_id`` is the identity every record keys on (D5). ``name`` is read
    only for the swept prefix and the favourites placeholder pattern, which are
    conventions spelled in the name by the systems that apply them, and is never
    stored. ``tracks`` is the count the listing reported, or ``None`` when it
    reported none, which is unknown rather than empty.
    """

    playlist_id: str
    name: str
    tracks: int | None = None


class Catalogue(Protocol):
    """Every provider read the product makes through this seam, and nothing more.

    SEVEN MEMBERS BECAUSE THERE ARE SEVEN CALL SITES, and the protocol is the list
    rather than a description of a provider. A method nobody calls is a method an
    adapter has to implement for no reason, and it is the shape by which a seam
    stops being a seam and becomes a client library.

    **THE FAILURE CONTRACT IS PART OF THE TYPE, NOT AN IMPLEMENTATION DETAIL.**
    :meth:`artist_for` and :meth:`playlist_for` RAISE for a label or a playlist
    the provider cannot resolve. They never return ``None`` and they never return
    an empty stand-in. That is a contract rather than a preference, because of
    what the caller does with an absence:
    ``cratekit.label.sweep.LabelSource.list_recent`` skips a label whose artist
    object is missing with a bare ``continue`` and raises nothing, so a returned
    ``None`` becomes a sweep that offers no releases and reports that it looked.
    An unreadable catalogue and a catalogue with nothing new in it are then
    indistinguishable in the only place a person reads, which is the R-135 defect
    class exactly. R11 states the obligation and U3 drives it.

    The two callables are declared here as methods rather than left as the bare
    functions the call sites take, so one object carries the whole capability. An
    adapter that could list a label and could not verify one is a half-bound
    catalogue, and passing four independently resolved things around is how a
    caller ends up holding three of them.
    """

    def artist_for(self, entry: registry.LabelEntry) -> Any:
        """The provider artist object this favourite label's catalogue hangs off.

        Consumed by ``sweep.list_for_label`` through ``crawl.releases``, which
        pages it. RAISES for a label the provider cannot resolve; see the failure
        contract above for why an absence may not be returned. The object may be
        a roster: the label's own page, every resolved seed, and artists
        discovery found by album search and a credited artist walk.
        """

    def playlist_for(self, reference: str) -> Any:
        """The provider playlist object for a URL or an identifier a person typed.

        Consumed by ``harvest.playlist_tracks``, which pages it. RAISES for a
        playlist the provider cannot resolve, on the same contract, and that
        refusal is what ``label-playlist-unreadable`` is finally raised from.
        """

    def search_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Ask the catalogue who is actually credited on one release.

        The callable ``verify.verify_release`` takes as its ``search`` argument,
        with that signature. Discovery finds a candidate by copyright text; this
        is the question that decides whether it is kept.
        """

    def check_label(self, name: str) -> dict:
        """Ask the catalogue whether a harvested label name is a real imprint.

        The callable ``harvest.from_tracks`` takes as its ``verify`` argument,
        with that signature. A copyright string is a heuristic, so an unconfirmed
        name is dropped rather than offered.
        """

    def account_playlists(self) -> tuple[AccountPlaylist, ...]:
        """Every playlist the logged in account CREATED, across every page.

        Consumed by ``sync.playlists``, the third R25 source. Followed and
        editorial playlists are not the account's to sweep and are left out.
        RAISES when the listing cannot be read, on the same contract as the two
        lookups above: an empty tuple means the provider answered and the account
        has no playlists, never that nobody could ask.
        """

    def favourite_tracks(self) -> tuple[Any, ...]:
        """Every track the logged in account has hearted, across every page.

        Consumed by ``intake.cli`` for the reserved reference ``favorites``,
        which resolves the account's hearts against the library the way a
        playlist's tracks are resolved. The rows are the shape
        ``match.read_tidal_tracks`` reads. RAISES when the listing cannot be read
        in full, on the same contract as the reads above: a short listing would
        report hearts the library lacks as absent from the account, so no page
        shape may end it early, and an empty tuple means the account has no
        hearts, never that nobody could ask.
        """

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None]:
        """Every track on one release, and the year the provider dates it.

        Consumed by ``label.approved_cli``, which turns an ACCEPTED label release
        into rows for the list document. The release is read again BY IDENTIFIER
        and nothing the review item's payload says about it is passed in, because
        a payload written before R-379 carries a memory address where the artist
        belongs. The rows are the shape ``match.read_tidal_tracks`` reads.

        RAISES for a release the provider cannot resolve, on the same contract as
        the lookups above, and raises rather than returning a short listing. An
        empty tuple means the provider answered and the release holds no track,
        never that nobody could ask. The year is ``None`` when the provider dates
        the release with nothing this seam can read as a year, which is unknown
        and is carried as unknown rather than guessed.
        """


def bound() -> bool:
    """Whether this build can produce a catalogue at all, asked WITHOUT trying.

    A queueing verb asks this so it can warn a person BEFORE they confirm, at the
    one moment the information is still useful to them. :func:`resolve` is the
    wrong question there: it is the worker's, it reads the credential and logs a
    client in, and asking it at enqueue would spend a login on a warning.

    It answers about THIS BUILD and not this machine, so it reads no credential:
    whether the adapter module imports, which includes its client library. Until
    U62 it returned a constant ``False``.
    """
    try:
        importlib.import_module(ADAPTER_MODULE)
    except ImportError:
        return False
    return True


#: The session module's remedy, carried into the product's vocabulary. Named per
#: value rather than converted by lookup, so a remedy the session module grows
#: that has no product token lands on reauthenticating rather than on a crash.
_REMEDIES = {
    Remedy.REAUTHENTICATE_PROVIDER.value: Remedy.REAUTHENTICATE_PROVIDER,
    Remedy.REPAIR_CREDENTIAL_STORE.value: Remedy.REPAIR_CREDENTIAL_STORE,
}


def _unbound(exc: BaseException) -> Exception:
    return refuse(
        "label-catalogue-unbound",
        "a provider session is stored and the catalogue adapter that would use "
        f"it to list a label or a playlist does not import in this build ({exc}), "
        "so the queued work cannot be carried out. Nothing was offered for review",
        steps=(
            "reinstall the product so its core dependencies are present, then "
            "retry",
        ),
        scope=Scope.RUN,
        origin=("label", "catalogue"),
    )


def resolve(cfg: config.Config) -> Catalogue:
    """The catalogue this library's label reads go through, or why there is none.

    FOUR REFUSALS, EACH UNDONE BY A DIFFERENT ACT. A provider that could not be
    reached is a wait, and the stored session is kept because nobody judged it. A missing credential is the
    person's to record and doctor already says how. A stored session the
    provider rejects, or a keychain that cannot be read, is the same slug with
    the remedy the session module chose, because a person told only that a
    credential is missing would record the one they already have. An adapter
    that does not import is this build's own gap, and authenticating again would
    not move it.
    """
    del cfg  # the credential is installation scoped; the library does not pick it
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no catalogue "
            "to read this label or this playlist from",
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        )
    try:
        tidal_catalogue = importlib.import_module(ADAPTER_MODULE)
    except ImportError as exc:
        raise _unbound(exc) from exc
    try:
        return tidal_catalogue.open_catalogue()
    except ProviderUnavailable as exc:
        raise refuse(
            "unavailable-transient",
            f"the streaming provider could not be reached to open the catalogue "
            f"({exc}); the stored session was not judged and is kept",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
        ) from exc
    except (AdapterAuthFailed, AdapterBroken) as exc:
        raise refuse(
            "credential-missing",
            f"the stored streaming provider session could not be used to open "
            f"the catalogue ({exc})",
            remedy=_REMEDIES.get(exc.remedy.value, Remedy.REAUTHENTICATE_PROVIDER),
            scope=Scope.RUN,
            origin=("label", "catalogue"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        ) from exc


__all__ = ["ADAPTER_MODULE", "AccountPlaylist", "Catalogue", "bound", "resolve"]
