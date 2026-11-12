"""The one place the label package gets the catalogue it reads a provider through.

**U62 BOUND IT.** ``cratekit.label.tidal_catalogue`` implements :class:`Catalogue`
over a provider client logged in from the stored session, the one
``acquire.provider_session.session_for`` holds for the process (U261). Before that unit no implementation shipped, and this
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
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import urlsplit

from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken
from cratekit.acquire.provider_session import ProviderUnavailable
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
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


# THE REFERENCE PARSER IS PURE AND LIVES ON THE SEAM, NOT IN THE ADAPTER,
# because a core reader needs it too: the playlists cursor records the
# identifier a typed reference names, and core cannot import the adapter,
# which imports the provider's client library. The adapter re-exports it.

#: A provider playlist identifier. The provider mints playlists as UUIDs, so a
#: reference that is not one cannot name a playlist and is refused before a
#: request is spent on it.
_UUID = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE
)

#: Hosts a playlist URL or a share link is read from. A share link is the same
#: URL with a query string on it, so it needs no host of its own.
PLAYLIST_HOSTS = frozenset({"tidal.com", "www.tidal.com", "listen.tidal.com"})

#: The short link host. Its path is an opaque code that only the provider can
#: expand, so it is refused BY NAME rather than followed: following it is a
#: network redirect this parser would have to trust.
SHORT_LINK_HOST = "link.tidal.com"


class PlaylistReferenceInvalid(ValueError):
    """A reference that is not a playlist URL, a share link, or an identifier."""


def playlist_id(reference: str) -> str:
    """The playlist identifier inside what a person typed, or a named refusal.

    THREE SHAPES AND NO FOURTH: a bare identifier, a full URL on a provider host
    whose path ends ``playlist/<id>``, and a share link, which is that URL with a
    query string. Anything else is refused rather than searched for, because a
    guess that lands on a different playlist would list someone else's tracks
    under the one the person named.
    """
    text = str(reference or "").strip()
    if _UUID.fullmatch(text):
        return text.lower()
    parts = urlsplit(text)
    host = (parts.hostname or "").lower()
    if parts.scheme in {"http", "https"} and host == SHORT_LINK_HOST:
        raise PlaylistReferenceInvalid(
            f"{reference!r} is a short share link, which only the provider can "
            f"expand; open it and pass the playlist URL it lands on"
        )
    if parts.scheme in {"http", "https"} and host in PLAYLIST_HOSTS:
        segments = [segment for segment in parts.path.split("/") if segment]
        if (
            len(segments) >= 2
            and segments[-2] == "playlist"
            and _UUID.fullmatch(segments[-1])
        ):
            return segments[-1].lower()
    raise PlaylistReferenceInvalid(
        f"{reference!r} is not a playlist URL, a share link, or a playlist "
        f"identifier"
    )


@dataclass(frozen=True, slots=True)
class AccountPlaylist:
    """One playlist the account itself created, reduced to what a sweep decides on.

    ``playlist_id`` is the identity every record keys on (D5). ``name`` is read
    only for the swept prefix, the label batch's ` LIBRARY` debris suffix and
    the favourites placeholder pattern, which are conventions spelled in the
    name by the systems that apply them, and is never stored. ``tracks`` is the count the listing reported, or ``None`` when it
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


#: The verdict :meth:`Catalogue.reread_release` answers for a release the
#: provider no longer has (R-1634). Not ``unconfirmed``: the provider answered,
#: so it is not a provider that is not answering, and not ``confirmed``: a
#: missing album says nothing of whether the provider's reads carry a credit.
#: The sweep asks the next held release rather than refusing on it.
RELEASE_GONE = "gone"


def artist_name(release: Any) -> str:
    """The name of a release's artist, never a provider object's repr.

    ``album.artist`` on this provider is an Artist object, and ``str`` of that
    object is a memory address, which is what R-379 found in 98 live review
    rows. A plain string is already the name, and that is what the suite's
    stand-ins had always used, which is why the address survived every green
    battery. Anything else is read off the object's ``name``, and an object
    with no name to give is the empty string.

    ONE READER, ON THE SEAM, for the sweep that files a release and for the
    repair that reads an artist again (R-840), so a repaired item carries
    exactly what a sweep would file for the same release today.
    """
    artist = getattr(release, "artist", None)
    if artist is None:
        return ""
    if isinstance(artist, str):
        return artist
    name = getattr(artist, "name", None)
    return name if isinstance(name, str) else ""


#: How many reads of release tracks IN A ROW may fail before
#: :class:`ReleaseTracks` stops asking the provider. Three, on the reasoning the
#: sweep's and the approval's own bounds give: one is a bad release, two a
#: coincidence, and each has already spent a full retry ladder.
READS_FAILED_IN_A_ROW = 3


class ReleasesUnasked(RuntimeError):
    """A release whose tracks were NOT ASKED FOR, because the provider is failing.

    Raised by :class:`ReleaseTracks` and never by the provider. It is not a
    failed read and not a release that is gone: nobody asked, so a caller says
    exactly that.
    """


class ReleaseTracks:
    """One sweep item's reads of release tracks, each release read once (R-798).

    Two questions read the same rows, whether the library owns the release and
    what the general catalogue publishes for it, and each read is two provider
    calls on a full retry ladder. The worker hands this to both, so the second
    asker gets the first one's answer.

    A FAILURE IS REMEMBERED TOO, and raised again as it was, a release that is
    gone included. The second asker would otherwise climb the ladder a second
    time for a release the provider just failed on. A ``CratekitError`` is not
    remembered: it stops the item, so nobody asks twice.

    THE OUTAGE RULE LIVES HERE, ONCE. After :data:`READS_FAILED_IN_A_ROW` reads
    in a row the provider could not answer, a release not yet read raises
    :class:`ReleasesUnasked` and the provider is not called. Each asker
    counting for itself was the first draft, and the review drove it wrong: an
    asker that is only sometimes asked never sees the successes between two
    failures, so it counted three failures in a row that were not. A release
    that is gone is the provider answering, and ends a run of failures.

    FOR ONE ITEM AND NO LONGER. The worker builds one per label, so neither a
    remembered failure nor the outage outlives the sweep that met it.
    """

    def __init__(self, catalogue: "Catalogue") -> None:
        self.catalogue = catalogue
        self._read: dict[str, ReleaseRead | Exception] = {}
        self._failed_in_a_row = 0

    @property
    def given_up(self) -> bool:
        """Whether the outage rule has ended the asking for a release not yet read.

        For a caller that would rather stop its run than record every later
        release as unasked (R-815).
        """
        return self._failed_in_a_row >= READS_FAILED_IN_A_ROW

    def forget(self) -> None:
        """Drop every remembered read, and keep the count of failures in a row.

        For a reader that outlives one sweep item (R-815): a job that reads
        each release exactly once has no second asker to remember for, and
        would otherwise carry every release's rows, and every failure with
        its traceback, to the end of a run of thousands.
        """
        self._read.clear()

    def release_tracks(self, release_id: str) -> ReleaseRead:
        held = self._read.get(release_id)
        if isinstance(held, Exception):
            raise held
        if held is not None:
            return held
        if self.given_up:
            raise ReleasesUnasked(
                f"the provider failed {READS_FAILED_IN_A_ROW} releases in a row, so "
                f"the rest were not asked for"
            )
        try:
            rows, year, short = self.catalogue.release_tracks(release_id)
        except CratekitError:
            raise
        except ReleaseUnresolvable as exc:
            self._failed_in_a_row = 0
            self._read[release_id] = exc
            raise
        except Exception as exc:
            self._failed_in_a_row += 1
            self._read[release_id] = exc
            raise
        self._failed_in_a_row = 0
        answer = (tuple(rows), year, short)
        self._read[release_id] = answer
        return answer


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


@dataclass(frozen=True, slots=True)
class ListingShortfall:
    """A playlist or release listing that came back shorter than its declared count (R-515).

    The provider counts tracks it will not serve and leaves them out of every
    page, so a listing can end where the count says and still hold fewer rows.
    THIS IS NOT A FAILURE TO READ, and unlike :class:`HeartsShortfall` it is
    carried beside the rows rather than raised: a short listing is still
    useful, and a caller that does not know this class must keep working
    rather than refuse. It only must not be reported as complete.

    Which tracks were withheld is not known and is not guessed at. Only the
    count is, which is the CONCEPTS entry for **Withheld**.
    """

    declared: int
    listed: int

    @property
    def withheld(self) -> int:
        return self.declared - self.listed

    @classmethod
    def of(cls, rows: Any, declared: Any) -> "ListingShortfall | None":
        """The shortfall of ``rows`` against ``declared``, or ``None`` when there is none.

        ``None`` too when the provider published no usable count, on the rule
        ``listing.paginate`` applies: a zero, negative or non integer count is
        not trusted as one, and a missing count leaves nothing to compare.
        """
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
            return None
        listed = len(tuple(rows))
        if listed >= declared:
            return None
        return cls(declared=declared, listed=listed)

    def summary(self) -> str:
        """The three numbers as a person reads them, one spelling everywhere."""
        return (
            f"{self.declared} declared, {self.listed} listed, "
            f"{self.withheld} withheld by the provider"
        )

    def block(self) -> dict[str, int]:
        """The three numbers as a report carries them."""
        return {"declared": self.declared, "listed": self.listed, "withheld": self.withheld}


#: What :meth:`Catalogue.release_tracks` answers: the rows, the year, and the
#: shortfall when the release listed short of its declared count (R-515).
ReleaseRead = tuple[tuple[Any, ...], int | None, ListingShortfall | None]


class Catalogue(Protocol):
    """Every provider read the product makes through this seam, and nothing more.

    ONE MEMBER PER CALL SITE, and the protocol is the list
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
        discovery found by album search and a credited artist walk. A roster
        whose releases are already in memory is a ``listing.HeldReleases``,
        which the crawl reads whole; paged instead, it would spend one artist's
        request budget on the whole label's releases (R-888).

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

    def reread_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Ask the provider again who is credited on one release, READ BY ITS IDENTIFIER (R-1634).

        The same answer :meth:`search_release` gives, for
        ``verify.verify_release`` to judge, except that it is never answered
        from the copyright line the listed object already carries: the provider
        is read for the release whatever the listing holds. The sweep's
        re-verification of one held release is its one call site, because the
        question there is whether the provider is answering, and a line read
        off the listing says nothing about that. A release the provider no
        longer has answers the verdict :data:`RELEASE_GONE`, and one with no
        identifier is never read and answers ``unconfirmed``.
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

    def release_tracks(self, release_id: str) -> ReleaseRead:
        """Every track on one release, the year the provider dates it, and any shortfall.

        Consumed by ``label.approved_cli``, which turns an ACCEPTED label release
        into rows for the list document. The release is read again BY IDENTIFIER
        and nothing the review item's payload says about it is passed in, because
        a payload written before R-379 carries a memory address where the artist
        belongs. The rows are the shape ``match.read_tidal_tracks`` reads.

        RAISES :class:`ReleaseUnresolvable` for a release the provider has nothing
        for, and whatever the provider raised for one it could not answer about,
        and raises for a release it refuses whole. An
        empty tuple means the provider answered and the release holds no track,
        never that nobody could ask. The year is ``None`` when the provider dates
        the release with nothing this seam can read as a year, which is unknown
        and is carried as unknown rather than guessed.

        A SHORT LISTING IS NOT A REFUSAL (R-515). The provider counts tracks on
        a release it will not serve, so the rows can end short of the count
        with nothing wrong in the walk. The third element is the
        :class:`ListingShortfall` that says by how much, ``None`` for a release
        that listed in full or whose count was not published. A caller that
        reports owned, offered or missing over the rows warns with it.
        """

    def release_artist(self, release_id: str) -> str:
        """The name of the artist one release is filed under, read by identifier.

        Consumed by ``label.artists_cli``, which gives an open review item whose
        recorded artist is a provider object address the name it should have
        carried (R-840). ONE PROVIDER READ, the release itself and none of its
        tracks, which is why this is not :meth:`release_tracks`: that reads the
        tracks too, and a track's artist is not the release's on a compilation.
        The name is read by :func:`artist_name`, the sweep's own reader.

        RAISES :class:`ReleaseUnresolvable` for a release the provider has
        nothing for, and whatever the provider raised for one it could not
        answer about. The empty string means the provider answered and names no
        artist for the release, never that nobody could ask.
        """

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask, in as few requests as the provider allows, which codes it files nothing under.

        Consumed by ``intake.missing_cli`` before its lookups (U207). A later
        :meth:`tracks_for_isrc` of a code the provider answered as filed under
        nothing answers the empty tuple with no request; every other code is
        asked as before, since a batch answer names one release per code and
        never says how many there are. RAISES NOTHING for a batch the provider
        could not answer: the codes are then asked one at a time, which is the
        contract :meth:`tracks_for_isrc` already keeps. Returns the requests
        made, zero for a catalogue with no batch form.
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

    def search_tracks(self, artist: str, title: str, offset: int = 0) -> tuple[Any, ...]:
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

        ``offset`` IS WHERE THE PAGE STARTS in the provider's listing of the
        same search, so a caller that got a full page can ask for the next one
        (R-879). A page shorter than :data:`TRACK_SEARCH_PAGE` is the end of
        the listing.

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

    A FRESH CATALOGUE OVER ONE LOGIN PER PROCESS (U261). Every resolve builds a
    new catalogue, as before, over the client
    ``provider_session.session_for`` holds, so a verb that resolves it twice,
    or resolves it and the outbound account, validates the session once. The
    presence check below still runs first on every resolve, so a session the
    index stopped recording is refused rather than reused.
    """
    # The credential is installation scoped and the library does not pick it;
    # the configuration is still handed on, because the pacing gate reads its
    # interval and cooldown off the FROZEN one a job carries (R-705).
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
        return tidal_catalogue.open_catalogue(cfg)
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
    "PLAYLIST_HOSTS",
    "SHORT_LINK_HOST",
    "AccountPlaylist",
    "Catalogue",
    "HeartsShortfall",
    "ListingShortfall",
    "ReleaseRead",
    "PlaylistReferenceInvalid",
    "READS_FAILED_IN_A_ROW",
    "ReleaseTracks",
    "ReleaseUnresolvable",
    "ReleasesUnasked",
    "TRACK_SEARCH_PAGE",
    "Unread",
    "artist_name",
    "bound",
    "missing_listing",
    "playlist_id",
    "resolve",
]
