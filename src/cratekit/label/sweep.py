"""A label catalogue as a sync source: newest-N, verified, not tombstoned.

``list_recent`` does not read a watermark and does not apply a date floor.
U22's increment owns owned-dedup and the source cursor. This module owns
verification, tombstone consultation, and the review-queue offer.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from cratekit.core import config, review, tombstone
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import crawl, registry
from cratekit.label import verify as label_verify
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
    """
    del last_pulled
    claimed = entry.match or entry.name
    listed = list(crawl.releases(artist))
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

    def __init__(
        self,
        cfg: config.Config,
        *,
        registry: registry.Registry,
        artists: Mapping[str, Any] | None = None,
        verify: Callable[[str, Any], Mapping[str, Any]] | None = None,
    ) -> None:
        self.cfg = cfg
        self.registry = registry
        self.artists = dict(artists or {})
        self.verify = verify

    def list_recent(self, n: int) -> list[run.Candidate]:
        if self.verify is None:
            return []
        found: list[run.Candidate] = []
        for entry in self.registry.labels.values():
            artist = self.artists.get(entry.label_id)
            if artist is None:
                continue
            listing = list_for_label(
                self.cfg,
                entry,
                artist=artist,
                verify=self.verify,
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
