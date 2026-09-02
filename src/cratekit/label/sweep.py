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


def _tombstoned(cfg: config.Config, release: Any) -> bool:
    artist = _artist_of(release)
    title = _title_of(release)
    if not artist and not title:
        return False
    store = DecisionStore(tombstone.STORE_KEY, cfg)
    identity = tombstone.version_identity(artist=artist, title=title)
    return store.suppresses(tombstone.KIND_VERSION, identity)


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
        if _tombstoned(cfg, release):
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
        """
        if self.catalogue is not None:
            try:
                return self.catalogue.artist_for(entry)
            except Exception as exc:
                raise run.LookupFailure(
                    f"the catalogue could not resolve an artist for the label "
                    f"{entry.name!r} ({type(exc).__name__}: {exc}); its releases "
                    f"were never listed"
                ) from exc
        artist = self.artists.get(entry.label_id)
        if artist is None:
            raise run.LookupFailure(
                f"no catalogue object was available for the registered label "
                f"{entry.name!r}, so its releases were never listed; that is not "
                f"a label with nothing new"
            )
        return artist

    def _verifier(self) -> Callable[[str, Any], Mapping[str, Any]]:
        """The release verification callable, or a refusal for the same reason.

        A sweep that cannot verify cannot honestly report anything: every
        release it listed would be dropped as unconfirmed and the run would look
        like a label with nothing new. Returning an empty list here was the same
        absence-as-evidence shape the artist lookup above had.
        """
        if self.verify is not None:
            return self.verify
        if self.catalogue is not None:
            return self.catalogue.search_release
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )

    def list_recent(self, n: int) -> list[run.Candidate]:
        verify = self._verifier()
        found: list[run.Candidate] = []
        for entry in self.registry.labels.values():
            listing = list_for_label(
                self.cfg,
                entry,
                artist=self._artist_for(entry),
                verify=verify,
            )
            found.extend(listing.candidates)
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
