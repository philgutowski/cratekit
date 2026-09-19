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


#: How many rows :meth:`Catalogue.search_tracks` returns at most. ON THE SEAM
#: because the caller reads it: an answer this long may have been cut off, so
#: a candidate past the cut could be a second exact one nobody can see, and
#: ``intake.candidates`` never lists a row on the strength of a full page.
TRACK_SEARCH_PAGE = 50


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


@dataclass(frozen=True, slots=True)
class Unread:
    """One part of a label's catalogue a crawl could not read, and why.

    R-261 and R-393. A crawl skips a listing the client does not expose, and
    discovery skips an artist whose listing failed after its retry ladder was
    spent, and both skips are deliberate: refusing the label over one of them
    would withhold everything else the crawl did read. What was missing was a
    record. Without one the releases on the skipped part were indistinguishable
    from releases that were never there, and the sweep reported success.

    ``artist`` is the provider's name for the artist, or its identifier when it
    has no name. ``listing`` is the method that was not read, or
    ``artist_releases`` when the whole of one artist's listing failed.
    ``reason`` is what the person is told. ``transient`` says whether another
    attempt can differ: a rate limit clears, a method the client lacks does not.
    """

    artist: str
    listing: str
    reason: str
    transient: bool


def missing_listing(artist: Any, method: str) -> Unread:
    """The record for a listing method ``artist`` does not expose."""
    name = str(getattr(artist, "name", "") or getattr(artist, "id", "") or "")
    return Unread(
        artist=name or type(artist).__name__,
        listing=method,
        reason=f"the provider client exposes no {method} listing",
        transient=False,
    )


class ReleaseUnresolvable(LookupError):
    """A release identifier the provider has nothing for, or none at all.

    DECLARED ON THE SEAM, because it is the one failure of
    :meth:`Catalogue.release_tracks` a caller acts on differently: a withdrawn
    release is settled by revoking its acceptance, and every other failure is
    settled by asking again. The caller therefore catches THIS class and never
    ``LookupError``, which ``KeyError`` and ``IndexError`` also are, so a client
    that failed to parse a payload is not reported as a release that is gone.
    """


class HeartsShortfall(Exception):
    """The hearts listing came back shorter than the account declares (R-504).

    DECLARED ON THE SEAM, because it is the one failure of
    :meth:`Catalogue.favourite_tracks` that still carries an answer. The
    provider counts hearts it will not serve and leaves them out of every page,
    so the listing can end where the count says and still hold fewer rows. The
    rows that did come back are real hearts and ride on the exception, so a
    caller that knows this class lists them and reports the difference.

    AN EXCEPTION AND NOT A SECOND RETURN SHAPE, so a caller that does not know
    this class fails closed. ``label.cli.favourite_tracks_or_refuse`` refuses
    anything it does not recognise as an unreadable listing, which is what a
    short listing passed off as the account would otherwise be.

    Which hearts were withheld is not known and is not guessed at. Only the
    count is.
    """

    def __init__(self, rows: Any, declared: int) -> None:
        self.rows = tuple(rows)
        self.declared = declared
        super().__init__(self.summary())

    @property
    def listed(self) -> int:
        return len(self.rows)

    @property
    def withheld(self) -> int:
        return self.declared - self.listed

    def summary(self) -> str:
        """The three numbers as a person reads them, one spelling everywhere."""
        return (
            f"{self.declared} declared, {self.listed} listed, "
            f"{self.withheld} withheld by the provider"
        )

    def block(self) -> dict[str, int]:
        """The three numbers as a report carries them."""
        return {"declared": self.declared, "listed": self.listed, "withheld": self.withheld}


class Catalogue(Protocol):
    """Every provider read the product makes through this seam, and nothing more.

    NINE MEMBERS BECAUSE THERE ARE NINE CALL SITES, and the protocol is the list
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

        THE OBJECT MAY CARRY ``unread``, a tuple of :class:`Unread` naming the
        parts of the roster that could not be read while it was built. The sweep
        reads it with a default of nothing, so a plain artist object needs no
        such attribute, and an adapter that skips anything while building a
        roster must put it here rather than drop it (R-261, R-393).
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
        ``match.read_tidal_tracks`` reads. RAISES when the listing cannot be read,
        on the same contract as the reads above: no page shape may end it early,
        and an empty tuple means the account has no hearts, never that nobody
        could ask.

        WHAT THE READ CAN PROMISE is every heart the provider serves, and that
        is not always every heart the account holds. The provider counts hearts
        it will not serve and leaves them out of the pages. When the rows come
        back fewer than that count, this RAISES :class:`HeartsShortfall` carrying
        the rows and the count, so the difference is reported rather than passed
        off as the account. A tuple returned is a listing that reached the count.
        """

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None]:
        """Every track on one release, and the year the provider dates it.

        Consumed by ``label.approved_cli``, which turns an ACCEPTED label release
        into rows for the list document. The release is read again BY IDENTIFIER
        and nothing the review item's payload says about it is passed in, because
        a payload written before R-379 carries a memory address where the artist
        belongs. The rows are the shape ``match.read_tidal_tracks`` reads.

        RAISES :class:`ReleaseUnresolvable` for a release the provider has nothing
        for, and whatever the provider raised for one it could not answer about,
        and raises rather than returning a short listing. An
        empty tuple means the provider answered and the release holds no track,
        never that nobody could ask. The year is ``None`` when the provider dates
        the release with nothing this seam can read as a year, which is unknown
        and is carried as unknown rather than guessed.
        """

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        """Every provider track the catalogue files under one ISRC.

        Consumed by ``intake.missing_cli``, which names a missing row that
        carries no provider identifier, a recognised set track, by its ISRC. The
        caller lists the row only when the answer holds exactly ONE distinct
        identifier, because one ISRC is commonly on the provider several times,
        a single, an album cut and a compilation (R-356), and which release is
        downloaded is not something the ISRC decides. The rows carry at least
        ``id``.

        An empty tuple means the provider answered and files no track under the
        code. RAISES when the provider could not answer, never a short or empty
        stand-in, on the same contract as the reads above: an outage read as
        "no track" would hand a nameable row on as unnameable, and one read as a
        short answer could turn two releases into one and list a guess.
        """

    def search_tracks(self, artist: str, title: str) -> tuple[Any, ...]:
        """The provider tracks a text search for one artist and title returns.

        Consumed by ``intake.candidates``, which gives a missing row that has no
        provider identifier and no usable ISRC, a typed tracklist line or a
        recognised set track, a route to one (U79, R-302). A SEARCH IS A
        PROPOSAL AND NEVER A PICK. The answer is ranked by the provider's own
        relevance, which returns a remix beside the original and an unrelated
        act of the same name beside both, so this method chooses nothing and the
        caller lists a row only on its own exact test and offers everything
        else to a person. ``title`` carries the version when the row names one,
        since the provider searches one string. The rows are the shape
        ``match.read_tidal_tracks`` reads, in the provider's order, and at most
        :data:`TRACK_SEARCH_PAGE` of them: an answer that long is one the
        caller must read as possibly cut short.

        An empty tuple means the provider answered and found nothing. RAISES
        when the provider could not answer, on the same contract as the reads
        above: an outage read as "no candidate" would tell a person a track the
        provider carries cannot be found there.
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


__all__ = [
    "ADAPTER_MODULE",
    "AccountPlaylist",
    "Catalogue",
    "HeartsShortfall",
    "ReleaseUnresolvable",
    "TRACK_SEARCH_PAGE",
    "Unread",
    "bound",
    "missing_listing",
    "resolve",
]
