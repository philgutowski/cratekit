"""A label catalogue as a sync source: newest-N, verified, not tombstoned.

``list_recent`` does not read a watermark and does not apply a date floor.
U22's increment owns owned-dedup and the source cursor. This module owns
verification, tombstone consultation, and the review-queue offer.

It also owns one refusal, and it is the module's sharpest rule: a catalogue
that could not be READ raises ``run.LookupFailure`` and never returns an empty
listing. Empty means the crawl was exhausted, and nothing else may mean it.
R-135 is what happens when those two answers share a shape.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from cratekit.core import config, review, tombstone
from cratekit.core.cause import CratekitError
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import crawl, registry
from cratekit.label import verify as label_verify
from cratekit.label.catalogue import Catalogue
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
    """What one label's crawl produced after verification and tombstones."""

    candidates: tuple[run.Candidate, ...]
    dropped: tuple[Dropped, ...]
    suppressed: tuple[run.Candidate, ...]


def _year_of(release: Any) -> str:
    year = getattr(release, "year", None)
    if year is None:
        year = getattr(release, "release_date", "") or ""
    text = str(year)
    return text[:4] if len(text) >= 4 and text[:4].isdigit() else text


def _artist_of(release: Any) -> str:
    return str(getattr(release, "artist", "") or "")


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
    a label with no confirmed releases, which the per release form never did.
    Deferring to the first release that actually asks keeps the refusal on
    exactly the runs that used to raise it.

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


def _crawl_or_refuse(entry: registry.LabelEntry, artist: Any) -> list[Any]:
    """Every release for one label, or a refusal. Never a silent empty list.

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
    """
    if not crawl.can_list(artist):
        raise run.LookupFailure(
            f"the catalogue object for {entry.name!r} exposes none of the listing "
            f"methods {', '.join(crawl.LISTING_METHODS)}, so its releases were "
            f"never read; that is not an empty catalogue"
        )
    try:
        return list(crawl.releases(artist))
    except Exception as exc:
        raise run.LookupFailure(
            f"the catalogue listing for {entry.name!r} could not be read "
            f"({type(exc).__name__}: {exc}); that is not an empty catalogue"
        ) from exc


def list_for_label(
    cfg: config.Config,
    entry: registry.LabelEntry,
    *,
    artist: Any,
    verify: Callable[[str, Any], Mapping[str, Any]],
    last_pulled: str | None = None,
    owned: set[str] | frozenset[str] | None = None,
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
    listed = _crawl_or_refuse(entry, artist)
    listed.sort(key=_year_of, reverse=True)
    owned_ids = owned or set()
    cap = limit if limit is not None else registry.effective_limit(entry)

    candidates: list[run.Candidate] = []
    dropped: list[Dropped] = []
    suppressed: list[run.Candidate] = []
    tombstoned = _suppression_reader(cfg)
    for release in listed:
        identity = str(getattr(release, "id", "") or "")
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
        item = _candidate(entry, release)
        if tombstoned(release):
            suppressed.append(item)
            continue
        if identity in owned_ids:
            continue
        candidates.append(item)
        if len(candidates) >= cap:
            break
    return LabelListing(
        candidates=tuple(candidates),
        dropped=tuple(dropped),
        suppressed=tuple(suppressed),
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
    ) -> None:
        self.cfg = cfg
        self.registry = registry
        self.artists = dict(artists or {})
        self.verify = verify
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

        EVERY exception from the seam is flattened into this one, and the
        original stays reachable as ``__cause__``. An adapter's own refusal is
        not lost by that, and ``sync-source-lookups-failed`` stays the single
        vocabulary for "this source could not list", which is the distinction the
        increment and the person reading its output both need.

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
            except Exception as exc:
                raise run.LookupFailure(
                    f"the catalogue could not resolve an artist for the label "
                    f"{entry.name!r} ({type(exc).__name__}: {exc}); its releases "
                    f"were never listed"
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
                    raise run.LookupFailure(
                        f"the catalogue could not confirm who is credited on a "
                        f"release ({type(exc).__name__}: {exc}); the releases "
                        f"this sweep listed were never verified, and an "
                        f"unverified release is not a release with no match"
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
        verify = self._verifier()
        found: list[run.Candidate] = []
        discarded: list[Dropped] = []
        for entry in self.registry.labels.values():
            listing = list_for_label(
                self.cfg,
                entry,
                artist=self._artist_for(entry),
                verify=verify,
            )
            found.extend(listing.candidates)
            discarded.extend(listing.dropped)
        self.dropped = tuple(discarded)
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
        if store is not None:
            offer_release(store, candidate)
            return
        with review.open_store(self.cfg) as opened:
            offer_release(opened, candidate)
