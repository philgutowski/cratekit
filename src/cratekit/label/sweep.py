"""A label catalogue as a sync source: newest-N, verified, not tombstoned.

``list_recent`` does not read a watermark and does not apply a date floor.
U22's increment owns the source cursor. This module owns verification,
tombstone consultation, the review-queue offer, and since R-259 the question of
which releases the library already holds, :class:`OwnedReleases`.

It also owns one refusal, and it is the module's sharpest rule: a catalogue
that could not be READ raises ``run.LookupFailure`` and never returns an empty
listing. Empty means the crawl was exhausted, and nothing else may mean it.
R-135 is what happens when those two answers share a shape.
"""

from __future__ import annotations

from collections.abc import Callable, Container, Mapping
from dataclasses import dataclass
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.acquire.vendored import is_rate_limit
from cratekit.core import config, review, tombstone
from cratekit.core.cause import CratekitError
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import crawl, registry
from cratekit.label import verify as label_verify
from cratekit.label.catalogue import Catalogue, ReleaseUnresolvable, Unread, missing_listing
from cratekit.sync import run

KIND = "label-release"
HANDLER_KEY = "sync.labels"


@dataclass(frozen=True, slots=True)
class Dropped:
    """A release that will not be acquired, and why."""

    identity: str
    reason: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class LabelListing:
    """What one label's crawl produced after verification and tombstones.

    ``listed`` IS HOW MANY RELEASES THE CRAWL READ, before any of them was
    classified, and it is carried because the three tuples do not add up to it.
    A release the library already owns is skipped without a record, and the
    newest-N cap stops the loop with releases still unread. The worker that
    refuses "read N and confirmed none" needs the N, and ``len(dropped)`` alone
    was that number only when nothing else happened to the listing: a label
    whose confirmed releases were all tombstoned and whose others were dropped
    was refused as a catalogue nobody could verify a line of, with
    ``confirmed: 0``, over a release that verified fine.
    """

    candidates: tuple[run.Candidate, ...]
    dropped: tuple[Dropped, ...]
    suppressed: tuple[run.Candidate, ...]
    listed: int = 0
    #: The parts of the catalogue the crawl could not read. Non empty means
    #: ``listed`` is a count of part of the label, not of all of it (R-261).
    unread: tuple[Unread, ...] = ()


def _year_of(release: Any) -> str:
    year = getattr(release, "year", None)
    if year is None:
        year = getattr(release, "release_date", "") or ""
    text = str(year)
    return text[:4] if len(text) >= 4 and text[:4].isdigit() else text


def _artist_of(release: Any) -> str:
    """The artist's name, never a provider object's repr.

    ``album.artist`` on this provider is an Artist object. ``str`` of that
    object is a memory address, which is what 98 live review rows already
    carry. A plain string is already the name, and that is what the suite's
    stand-ins have always used, which is why the address survived every green
    battery.
    """
    artist = getattr(release, "artist", None)
    if artist is None:
        return ""
    if isinstance(artist, str):
        return artist
    name = getattr(artist, "name", None)
    return name if isinstance(name, str) else ""


def _title_of(release: Any) -> str:
    return str(getattr(release, "title", "") or getattr(release, "name", "") or "")


def _suppression_reader(cfg: config.Config) -> Callable[[Any], bool]:
    """One tombstone question, answered against ONE read of the store.

    **THIS BRANCH IS WHAT MADE THE OLD SHAPE COST ANYTHING.** The previous form
    built a :class:`DecisionStore` and called ``suppresses`` per release, and
    ``suppresses`` reads the whole document and re-materializes every record on
    every call. Nothing drove this path from ``src`` before the label handlers
    were bound, so a per release re-read of a file that cannot change mid loop
    was free in the only way that matters: nobody ran it. Measured on a five
    hundred record store at roughly 367 microseconds per call, a hundred release
    crawl of one label spent about 37 milliseconds re-reading one unchanging
    document, multiplied by the number of favourite labels in the sweep.

    ``DecisionStore``'s own docstring already says the intended shape, that a
    decision store is "read whole by an acquisition pass", so this is the class
    being used as documented rather than a new optimization.

    **THE READ IS LAZY ON PURPOSE, AND THAT IS THE BEHAVIOUR PRESERVING HALF.**
    ``_read`` REFUSES a store it cannot recognize rather than reading it as
    empty, because an unreadable suppression list read as empty un-suppresses
    everything in it. Reading at the top of the sweep would fire that refusal for
    a label whose crawl listed nothing, which the per release form never did.
    Deferring to the first release that actually asks keeps the refusal off
    exactly those runs. The question is now asked BEFORE verification rather
    than after it, so a label with releases and an unreadable store refuses
    whether or not any of them would have confirmed; that is one more run than
    the per release form refused on, and it is the right one, because the
    alternative was a provider call per release whose answer the tombstone
    then discarded.

    A release with neither an artist nor a title is answered without reading at
    all, which is the same short circuit the per release form had and the reason
    it comes before the snapshot.
    """
    snapshot: set[str] | None = None

    def tombstoned(release: Any) -> bool:
        nonlocal snapshot
        artist = _artist_of(release)
        title = _title_of(release)
        if not artist and not title:
            return False
        if snapshot is None:
            store = DecisionStore(tombstone.STORE_KEY, cfg)
            # SUPPRESSING RECORDS ONLY, which is what ``suppresses`` reports:
            # it answers ``found is not None and found.suppressing``, and
            # ``suppressions`` with its default filters to exactly that set. A
            # revoked tombstone is kept in the document and must not suppress.
            snapshot = {record.suppression_id for record in store.suppressions()}
        identity = tombstone.version_identity(artist=artist, title=title)
        return (
            review.suppression_id_for(
                tombstone.STORE_KEY, tombstone.KIND_VERSION, identity
            )
            in snapshot
        )

    return tombstoned


def _candidate(entry: registry.LabelEntry, release: Any) -> run.Candidate:
    identity = str(getattr(release, "id", "") or "")
    return run.Candidate(
        identity=identity,
        recency=_year_of(release),
        payload={
            "artist": _artist_of(release),
            "title": _title_of(release),
            "label_id": entry.label_id,
            "label_name": entry.name,
            "identity": identity,
        },
    )


def _lookup_failure(message: str, exc: BaseException) -> run.LookupFailure:
    """``message`` as a lookup failure, marked rate limited when the provider said so.

    R-704. The eleventh sitting's sweep failed 20 of 47 labels over
    ``TooManyRequests: Album unavailable`` and recorded every one permanent,
    so resuming could not retry what a wait would have cleared. The question
    is asked of the error and of every error it was declared from, ``raise X
    from exc``, because a client that wraps the provider's answer still carries
    it; the implicit ``__context__`` is not followed, on
    ``core.cause._chain``'s argument. The classifier is the one R-703's
    download adapter uses, so the two readers of one answer cannot disagree.

    Six rate limit answers in a row trip the provider gate (R-705), which
    parks the item as ``Parked``, a ``CratekitError`` that passes every
    boundary here unchanged. What reaches this helper is a limit that did not
    trip it, most often on a call with no retry ladder of its own,
    verification or the artist resolve.
    """
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        if is_rate_limit(current):
            return run.LookupFailure(message, rate_limited=True)
        seen.add(id(current))
        current = current.__cause__
    return run.LookupFailure(message)


def _crawl_or_refuse(
    entry: registry.LabelEntry, artist: Any
) -> tuple[list[Any], tuple[Unread, ...]]:
    """Every release for one label and what could not be read, or a refusal.

    Never a silent empty list, and since R-261 never a silent half of one
    either. The second value names every listing the crawl skipped: the ones
    this object lacks, found here, and the ones a roster could not read while
    it was built, off its ``unread``. The caller decides what they mean.

    R-135 IS ABSENCE READ AS EVIDENCE OF ABSENCE, and this call had three ways to
    produce ``[]`` from a catalogue nobody had read. Two of them close here, on
    the checking path rather than in each caller that reports a result:

    * an artist object exposing NONE of the listing methods.
      ``listing.artist_releases`` skips a method it cannot find, one at a time,
      until it has skipped all of them and returns an empty list.
    * an exception out of the crawl. ``listing.fetch_with_retry`` re-raises the
      provider's own error once its retry ladder is spent, and
      ``listing._paged_caller`` raises ``ListingNotPaginated`` for a method that
      exists and cannot page. Both mean the listing was not read, and neither is
      caught anywhere between here and the increment.

    The third stays open and U7 records it: ``listing.paginate`` treats a ``None``
    first answer as exhaustion. An EMPTY first page from a method that exists is
    NOT a producer at all. That is a genuinely exhausted crawl, and it has to
    keep reporting empty, or every quiet label becomes an error and R-135 has
    been traded for its mirror image.

    ``run.LookupFailure`` rather than a ``refuse`` cause, because
    ``run.increment`` is the one place that knows a source failed to list and it
    already converts this into ``sync-source-lookups-failed``. Raising a cause
    here would give the same condition two vocabularies.

    A ``CratekitError`` PASSES THROUGH UNCHANGED, as it does at the other two
    seam boundaries in this module and for the same reason: an adapter that
    discovers mid page that the stored session has expired refuses
    ``credential-missing``, and that names an act the person can take. Wrapped
    into a lookup failure it would become "retry when the provider is
    reachable", which sends somebody to wait for a network that is fine.

    THE PROBE IS INSIDE THE BOUNDARY TOO. ``crawl.can_list`` reads attributes
    off the artist object, and an adapter's artist may be a lazy proxy that
    fetches on attribute access, so the probe itself can raise the provider's
    own error. Outside the ``try`` that error would bypass the increment's
    conversion and fail the item as an internal error telling the person to
    file a defect over an outage.
    """
    try:
        listable = crawl.can_list(artist)
    except CratekitError:
        raise
    except Exception as exc:
        raise _lookup_failure(
            f"the catalogue object for {entry.name!r} could not be examined "
            f"({type(exc).__name__}: {exc}), so its releases were never read; "
            f"that is not an empty catalogue",
            exc,
        ) from exc
    if not listable:
        raise run.LookupFailure(
            f"the catalogue object for {entry.name!r} exposes none of the listing "
            f"methods {', '.join(crawl.LISTING_METHODS)}, so its releases were "
            f"never read; that is not an empty catalogue"
        )
    skipped: list[str] = []
    try:
        releases = list(crawl.releases(artist, skipped=skipped))
        built = tuple(getattr(artist, "unread", None) or ())
    except CratekitError:
        raise
    except Exception as exc:
        raise _lookup_failure(
            f"the catalogue listing for {entry.name!r} could not be read "
            f"({type(exc).__name__}: {exc}); that is not an empty catalogue",
            exc,
        ) from exc
    return releases, (*built, *(missing_listing(artist, method) for method in skipped))


#: The library as the match engine sees it: the index and the tombstone view.
#: What :func:`cratekit.acquire.match_cli.library_view` returns.
LibraryView = tuple[match.LibraryIndex, Callable[..., bool], Callable[..., str]]

#: How many release track reads IN A ROW may fail before the rest of a label's
#: releases are not asked. Three, on ``label.approved_cli.OUTAGE_AFTER``'s
#: reasoning: one is a bad release, two a coincidence, and each has already
#: spent a full retry ladder by the time it is counted.
OUTAGE_AFTER = 3


class OwnedReleases:
    """The release identities the library already holds, asked one at a time.

    R-259. A release is known here only by the provider's identifier, and the
    library knows tracks, so ownership is a read: the release's tracks from the
    catalogue, each resolved against the library index the match engine uses,
    :func:`cratekit.acquire.match_cli.library_view`. That is why this is a
    container and not a set. Nobody can list the owned identities up front
    without reading every release on the label, so each is asked when a
    membership test reaches it, and the answer is kept, because the labels path
    asks twice: once in :func:`list_for_label` and again in the increment's
    ``scope.scoped``.

    OWNED MEANS EVERY TRACK, AND AT LEAST ONE. A release is owned when the
    provider lists at least one track on it and every track resolves
    ``MATCHED``. Everything short of that answers not owned, and so is offered:
    no track at all, where ``all`` over nothing would say owned; a row the
    reader cannot read; a track held only in another version, which is a
    question for the person and never an answer; and a release the provider no
    longer has. The direction is deliberate. An offer wrongly made costs a
    person one decline, and a release wrongly called owned is music they never
    see and nothing tells them about.

    A TRACK READ THE PROVIDER COULD NOT ANSWER IS NOT OWNED, and the release is
    offered. This is not the rule the listing and the verifier keep, where one
    unreadable label refuses the source, and the difference is deliberate: by
    the time this is asked the label was listed and the release confirmed, so
    the sweep has real offers in hand, and refusing would withhold every new
    release on the label over a question whose worst answer is one extra row a
    person declines. Before R-259 every release took that path. :data:`OUTAGE_AFTER`
    failures in a row stop the asking, so a provider that is down costs three
    retry ladders and not one per release. A ``CratekitError`` passes through
    unchanged, as at the other seam boundaries in this module, because an
    expired session names an act the person can take.

    THE LIBRARY IS WALKED ONCE, AND ONLY WHEN A RELEASE HAS TRACKS TO RESOLVE.
    A label whose confirmed releases all turn out gone never walks it.
    ``library`` lets the worker share one walk across every label in a job.
    """

    def __init__(
        self,
        cfg: config.Config,
        catalogue: Catalogue,
        *,
        library: Callable[[], LibraryView] | None = None,
    ) -> None:
        self.cfg = cfg
        self.catalogue = catalogue
        self._library_of = library
        self._view: LibraryView | None = None
        self._answers: dict[str, bool] = {}
        self._failed_in_a_row = 0

    def __contains__(self, identity: object) -> bool:
        if not isinstance(identity, str) or not identity:
            return False
        if identity not in self._answers:
            self._answers[identity] = self._holds(identity)
        return self._answers[identity]

    def _library(self) -> LibraryView:
        if self._view is None:
            if self._library_of is not None:
                self._view = self._library_of()
            else:
                self._view = match_cli.library_view(self.cfg)
        return self._view

    def _holds(self, release_id: str) -> bool:
        if self._failed_in_a_row >= OUTAGE_AFTER:
            return False
        try:
            rows, _year = self.catalogue.release_tracks(release_id)
        except CratekitError:
            raise
        except ReleaseUnresolvable:
            # THE PROVIDER ANSWERED, so the run of failures is broken.
            self._failed_in_a_row = 0
            return False
        except Exception:  # noqa: BLE001 - not owned, and the release is offered
            self._failed_in_a_row += 1
            return False
        self._failed_in_a_row = 0
        if not rows:
            return False
        try:
            wanted = match.read_tidal_tracks(rows)
        except match.UnreadableList:
            return False
        index, suppresses, identify = self._library()
        return all(
            match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify).state
            is match.MatchState.MATCHED
            for one in wanted
        )


def list_for_label(
    cfg: config.Config,
    entry: registry.LabelEntry,
    *,
    artist: Any,
    verify: Callable[[str, Any], Mapping[str, Any]],
    last_pulled: str | None = None,
    owned: Container[str] | None = None,
    limit: int | None = None,
) -> LabelListing:
    """Crawl, verify, drop unconfirmed, report tombstones. Ignore ``last_pulled``.

    ``last_pulled`` is accepted so a caller that still thinks in date floors
    cannot accidentally get a different function. It is not read.

    A listing that could not be READ raises ``run.LookupFailure`` rather than
    returning an empty :class:`LabelListing`. See :func:`_crawl_or_refuse`.
    """
    del last_pulled
    claimed = entry.match or entry.name
    listed, unread = _crawl_or_refuse(entry, artist)
    listed.sort(key=_year_of, reverse=True)
    owned_ids: Container[str] = owned if owned is not None else frozenset()
    cap = limit if limit is not None else registry.effective_limit(entry)

    candidates: list[run.Candidate] = []
    dropped: list[Dropped] = []
    suppressed: list[run.Candidate] = []
    tombstoned = _suppression_reader(cfg)
    # THE LOCAL QUESTION COMES FIRST AND THE PROVIDER CALLS AFTER IT. A
    # tombstone is a decision the person already made, answered from this
    # machine. Verifying before asking it spent a provider round trip per
    # release whose answer the tombstone then threw away, which on a label with
    # a long deleted back catalogue is most of the sweep's network calls, and
    # each wasted one is a step closer to the rate limited endpoint the
    # worker's refusal exists for. A tombstoned release therefore counts as
    # suppressed whether or not the catalogue would have confirmed it, which is
    # the honest reading: it was never a candidate, so nothing about it was for
    # the provider to decide.
    #
    # OWNERSHIP IS ASKED AFTER VERIFICATION, and before R-259 it came first.
    # It was a local question only while nothing on this path produced an owned
    # set; :class:`OwnedReleases` answers it by reading the release's tracks
    # from the provider, so asking first would read the tracks of every release
    # the catalogue then refuses to confirm as the label's. Asked here, a
    # release that is not the label's is never read, and the verification
    # outcomes the worker's "confirmed none" refusal counts are exactly the ones
    # it counted before. An owned release does not count toward the cap, which
    # is what drops owned before newest N rather than after it (R-137).
    for release in listed:
        identity = str(getattr(release, "id", "") or "")
        if tombstoned(release):
            suppressed.append(_candidate(entry, release))
            continue
        verdict = label_verify.verify_release(claimed, release, search=verify)
        status = str(verdict.get("verdict") or "unconfirmed")
        if status != "confirmed":
            dropped.append(
                Dropped(
                    identity=identity,
                    reason=status,
                    notes=str(verdict.get("notes") or ""),
                )
            )
            continue
        if identity in owned_ids:
            continue
        candidates.append(_candidate(entry, release))
        if len(candidates) >= cap:
            break
    return LabelListing(
        candidates=tuple(candidates),
        dropped=tuple(dropped),
        suppressed=tuple(suppressed),
        listed=len(listed),
        unread=unread,
    )


def offer_release(
    store: review.ReviewStore,
    candidate: run.Candidate,
    *,
    handler_key: str = HANDLER_KEY,
) -> review.Item:
    payload = dict(candidate.payload or {})
    payload.setdefault("identity", candidate.identity)
    return review.offer(
        store,
        queue=Queue.LABEL_RELEASE,
        kind=KIND,
        identity={"release_id": candidate.identity},
        payload=payload,
        handler_key=handler_key,
    )


class LabelSource:
    """The ``labels`` increment source. ``id`` is the source identifier, not a name."""

    id = "labels"

    #: This source OFFERS, it does not acquire. :meth:`process` calls
    #: ``offer_release``, which is ``review.offer``: it queues an item into the
    #: label-release queue and hands the item back with a verdict of ``None``.
    #: No file was downloaded and nothing entered the library, so the increment
    #: must not append this release to the run's importable file and must not
    #: advance the labels watermark over it. R-140 is what this closes, and
    #: ``run.Source.acquires`` carries the rest of the reasoning.
    acquires = False

    def __init__(
        self,
        cfg: config.Config,
        *,
        registry: registry.Registry,
        artists: Mapping[str, Any] | None = None,
        verify: Callable[[str, Any], Mapping[str, Any]] | None = None,
        catalogue: Catalogue | None = None,
        store: review.ReviewStore | None = None,
        owned: Container[str] | None = None,
    ) -> None:
        self.cfg = cfg
        #: The release identities the library already holds, handed to every
        #: label's listing so an owned release is dropped before the per label
        #: cap rather than after the increment has sliced newest N (R-137).
        #: The worker passes an :class:`OwnedReleases` and the same object to
        #: the increment, so the two filters on this path ask one question and
        #: read each release once. ``None`` holds nothing.
        self.owned = owned
        self.registry = registry
        self.artists = dict(artists or {})
        self.verify = verify
        #: An OPEN review store to offer into, or ``None`` to open one per offer.
        #: ``run.increment`` calls :meth:`process` with no store, so without this
        #: every offered release opened, migrated and checkpointed the review
        #: database on its own: measured at 0.386 ms per round trip, which on a
        #: label at the default cap of four hundred is a hundred and fifty
        #: milliseconds of connection churn per label and four hundred WAL
        #: checkpoints. The worker opens one store around the increment and
        #: hands it here. ``review.offer`` still commits per call, so the per
        #: offer durability the harvest boundary relies on is unchanged.
        self.store = store
        #: A ``label.catalogue.Catalogue``, which supplies both of the other two
        #: from one object. Kept beside them rather than replacing them because
        #: the pre-seam callers pass the pieces and there is no reason to rewrite
        #: them; a caller that has the whole capability passes this instead.
        self.catalogue = catalogue
        #: EVERY RELEASE THIS SOURCE READ AND THEN DISCARDED, across all of the
        #: labels one :meth:`list_recent` pass listed. ``list_for_label`` reports
        #: it per label and this class used to drop it on the floor, which is
        #: what let a catalogue that confirms NOTHING look like a catalogue with
        #: nothing new: no candidate is offered, ``run.increment`` sees no
        #: processed item and no error, and it answers ``shortfall="empty"``.
        #: The two are the same envelope and a caller cannot tell them apart
        #: without this. ``label/cli.py``'s worker is that caller.
        #:
        #: INSTANCE STATE IS SAFE HERE, and it is worth saying why rather than
        #: leaving a reader to work it out. This object is constructed fresh per
        #: queued item, inside ``label.cli.handle``, and it is the only
        #: constructor in ``src``. Nothing shares one across items, across jobs
        #: or across threads, so an attribute a listing pass writes cannot carry
        #: one label's answer into another's. A source that ever became long
        #: lived would have to move this onto the return value instead, which is
        #: :class:`LabelListing`'s job one layer down and R-136's contract change
        #: one layer up.
        self.dropped: tuple[Dropped, ...] = ()
        #: HOW MANY RELEASES THE LAST PASS READ, summed over its labels. The
        #: worker's "read N and confirmed none" refusal is keyed on this against
        #: ``dropped``, and not on ``dropped`` being non-empty, because a
        #: listing whose confirmed releases were all tombstoned and whose others
        #: were dropped is a label with nothing new and not a catalogue nobody
        #: could verify a line of.
        self.read = 0
        #: WHAT THE LAST PASS COULD NOT READ, across its labels, rebuilt per
        #: pass on the rule ``dropped`` states. The worker refuses a sweep that
        #: left anything here, after the increment has offered what was read,
        #: because a crawl that skipped a listing is not a crawl of the label
        #: (R-261, R-393).
        self.unread: tuple[Unread, ...] = ()

    def _artist_for(self, entry: registry.LabelEntry) -> Any:
        """The provider artist object for one favourite label, or a refusal.

        **THE BARE ``continue`` THAT USED TO BE HERE WAS R-135 IN MINIATURE, AND
        THE PATH IS STILL REACHABLE, SO IT RAISES RATHER THAN BEING DECLARED
        DEAD.** ``Catalogue.artist_for`` is contracted to raise rather than
        return ``None``, which closes the seam side of it. It does not close this
        side: ``artists`` is still a plain mapping a caller builds, so a
        favourite label with no entry in it is a condition that can still arrive,
        and skipping it silently means a registry of five labels and five missing
        objects produces a sweep that reports it looked and found nothing new.
        So the path is reachable, and it is closed here rather than annotated
        with a comment claiming it cannot happen.

        A FOREIGN exception from the seam is flattened into this one, and the
        original stays reachable as ``__cause__``, so
        ``sync-source-lookups-failed`` stays the single vocabulary for "this
        source could not list". A ``CratekitError`` PASSES THROUGH UNCHANGED,
        on the same rule :meth:`_verifier` and :func:`_crawl_or_refuse` state:
        an adapter's own refusal names an act the person can take, and the
        first draft of this method flattened it too, which would have told
        somebody whose session had expired to wait for the network.

        ONE UNREADABLE LABEL REFUSES THE WHOLE SOURCE, which is a choice worth
        naming. ``run.increment`` turns this into ``sync-source-lookups-failed``
        and no watermark moves, so the cost is that a run with four readable
        labels and one unreadable one offers nothing rather than offering four.
        The alternative costs more: a person is told the sweep succeeded while
        one of their labels was never read, which is the exact reading R-135
        exists to stop. Nothing is lost by refusing, because the next run
        re-lists from scratch.

        THE EXPLICIT PIECE WINS OVER THE CATALOGUE, and it wins in
        :meth:`_verifier` too, because ONE precedence rule is the whole value of
        having one. The two methods disagreed when this constructor first grew
        its fourth parameter, artist preferring the catalogue and verification
        preferring the piece, which is the shape where a caller that passes both
        gets half of each and nothing says so. Narrower beats broader: a caller
        who names the object for one label means that object. Every shipped
        caller passes exactly one of the two, so the rule decides nothing today
        and is written down for the caller that passes both.
        """
        artist = self.artists.get(entry.label_id)
        if artist is not None:
            return artist
        if self.catalogue is not None:
            try:
                return self.catalogue.artist_for(entry)
            except CratekitError:
                raise
            except Exception as exc:
                raise _lookup_failure(
                    f"the catalogue could not resolve an artist for the label "
                    f"{entry.name!r} ({type(exc).__name__}: {exc}); its releases "
                    f"were never listed",
                    exc,
                ) from exc
        raise run.LookupFailure(
            f"no catalogue object was available for the registered label "
            f"{entry.name!r}, so its releases were never listed; that is not "
            f"a label with nothing new"
        )

    def _verifier(self) -> Callable[[str, Any], Mapping[str, Any]]:
        """The release verification callable, or a refusal for the same reason.

        A sweep that cannot verify cannot honestly report anything: every
        release it listed would be dropped as unconfirmed and the run would look
        like a label with nothing new. Returning an empty list here was the same
        absence-as-evidence shape the artist lookup above had.

        Explicit piece first, then the catalogue, then a refusal. The same order
        :meth:`_artist_for` uses and for the reason stated there.

        **THE SEAM CALL IS WRAPPED, WHICH IS THE HALF THIS METHOD USED TO SKIP.**
        It returned ``self.catalogue.search_release`` bare while
        :meth:`_artist_for` wrapped its own seam call, so an exception out of
        verification, which is exactly what ``listing.fetch_with_retry``
        re-raises once its retry ladder is spent, flew straight past
        ``run.increment``'s ``except LookupFailure`` and failed the item through
        ``jobs.drive``'s generic handler as ``internal-error``. A provider outage
        told the person to file a defect. Guarding only the case where no
        verifier OBJECT exists, which is all this method did, is METHOD's defect
        pattern three: the condition the docstring above describes was left open
        while the missing-object case beside it was closed.

        ``run.LookupFailure`` rather than a cause, for the reason
        :func:`_crawl_or_refuse` states: the increment owns the conversion into
        ``sync-source-lookups-failed``, which stays the single vocabulary for
        "this source could not list".

        A ``CratekitError`` PASSES THROUGH UNCHANGED, which is where this differs
        from :meth:`_artist_for` and the difference is deliberate. An adapter that
        discovers at call time that the stored provider session has expired
        refuses ``credential-missing``, and that names an act the person can take;
        flattening it into "this source could not list" would send somebody to
        wait for a network that is fine.
        """
        if self.verify is not None:
            return self.verify
        if self.catalogue is not None:
            catalogue = self.catalogue

            def verified(claimed: str, release: Any) -> Mapping[str, Any]:
                try:
                    return catalogue.search_release(claimed, release)
                except CratekitError:
                    raise
                except Exception as exc:
                    raise _lookup_failure(
                        f"the catalogue could not confirm who is credited on a "
                        f"release ({type(exc).__name__}: {exc}); the releases "
                        f"this sweep listed were never verified, and an "
                        f"unverified release is not a release with no match",
                        exc,
                    ) from exc

            return verified
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )

    def list_recent(self, n: int) -> list[run.Candidate]:
        """The newest N candidates, and a record of what was thrown away getting them.

        ``self.dropped`` is rebuilt from this pass rather than appended to, so a
        second call answers about the second call. It is assigned once the loop
        has finished because a pass that raises refuses the whole source through
        ``run.LookupFailure``, and a half filled record of a listing nobody is
        going to report on is a thing a later reader would have to reason about.

        THE TRUNCATION TO ``n`` DOES NOT TOUCH IT. A candidate cut by the
        newest-N limit was confirmed and merely deferred to the next run, and a
        discarded release was never a candidate at all. Counting the two together
        would make a busy label look like an unverifiable one.
        """
        # THE VERIFIER IS RESOLVED ONLY ONCE THERE IS A LABEL TO VERIFY FOR, and
        # once rather than per label. A source over an empty registry has nothing
        # to confirm, and refusing it for lacking a way to confirm would turn a
        # no-op into "retry when the provider is reachable" for a source that
        # never needed a provider.
        verify = self._verifier() if self.registry.labels else None
        found: list[run.Candidate] = []
        discarded: list[Dropped] = []
        unread: list[Unread] = []
        read = 0
        for entry in self.registry.labels.values():
            listing = list_for_label(
                self.cfg,
                entry,
                artist=self._artist_for(entry),
                verify=verify,
                owned=self.owned,
            )
            found.extend(listing.candidates)
            discarded.extend(listing.dropped)
            unread.extend(listing.unread)
            read += listing.listed
        self.dropped = tuple(discarded)
        self.unread = tuple(unread)
        self.read = read
        found.sort(key=lambda item: item.recency, reverse=True)
        return found[:n] if n >= 0 else found

    def process(
        self,
        candidate: run.Candidate,
        artifacts,
        run_id: str,
        store: review.ReviewStore | None = None,
    ) -> None:
        del artifacts, run_id
        opened = store if store is not None else self.store
        if opened is not None:
            offer_release(opened, candidate)
            return
        with review.open_store(self.cfg) as own:
            offer_release(own, candidate)
