"""A label catalogue as a sync source: newest N, verified, not tombstoned.

``list_recent`` reads no watermark and applies no date floor; the increment
owns the cursor. This module owns verification, the tombstone consult, the
review queue offer and which releases the library holds (:class:`OwnedReleases`,
R-259).

Its sharpest rule: a catalogue that could not be read raises
``run.LookupFailure`` and never returns an empty listing. Empty means the crawl
was exhausted and nothing else (R-135).
"""

from __future__ import annotations

from collections.abc import Callable, Container, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.acquire.download import RATE_LIMIT_STATUSES, status_of
from cratekit.acquire.vendored import is_rate_limit
from cratekit.core import config, review, tombstone
from cratekit.core.cause import CratekitError
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import crawl, harvest, kept_listing, registry
from cratekit.label import gate as genre_gate
from cratekit.label import verify as label_verify
from cratekit.label.catalogue import (
    READS_FAILED_IN_A_ROW,
    RELEASE_GONE,
    Catalogue,
    ReleaseTracks,
    Unread,
    artist_name,
    missing_listing,
    translated,
)
from cratekit.sync import run

#: The review kind a release is filed under, the gate module's word.
KIND = genre_gate.RELEASE_KIND
HANDLER_KEY = "sync.labels"


@dataclass(frozen=True, slots=True)
class Dropped:
    """A release that will not be acquired, and why."""

    identity: str
    reason: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class Gated:
    """One release the genre gate is holding back, and what it judged (R-798).

    ``standing`` is a hold an earlier sweep recorded, judged again from its own
    words and not verified this sweep, so the worker's "confirmed none" refusal
    counts it with the queued ones.
    """

    candidate: run.Candidate
    judged: genre_gate.Judged
    standing: bool = False


@dataclass(frozen=True, slots=True)
class Canary:
    """The one held release a sweep verified again, and what the verifier answered (U277).

    Asked only when the sweep turned down every release it asked about, chosen as
    :func:`_canary_order` says. ``unconfirmed`` is no label credit, ``mismatch`` a
    credit the needle does not match (the name in ``notes``), and ``gone`` a
    release the provider no longer has (R-1634).

    ``basis`` is what the answer rested on (R-1634): :data:`READ_PROVIDER`,
    :data:`READ_LINE` (its own copyright line, nothing of the provider), or
    :data:`READ_NONE` (not asked, counted as not confirmed).
    """

    identity: str
    artist: str
    title: str
    verdict: str
    notes: str = ""
    basis: str = ""

    @property
    def confirmed(self) -> bool:
        return self.verdict == "confirmed"

    def how(self) -> str:
        """How the release was verified again, read before :meth:`said`."""
        return _BASIS_SAID.get(self.basis, "")

    def said(self) -> str:
        """The release and its answer, in words a refusal or a check can carry."""
        named = f"{self.title!r} by {self.artist}" if self.artist else repr(self.title)
        answer = f"answered {self.verdict}"
        if self.notes:
            answer += f" ({self.notes})"
        return f"{named}, release {self.identity}, {answer}"

    def to_json(self) -> dict[str, str]:
        return asdict(self)


#: What a re-verified release's answer rested on (R-1634), :attr:`Canary.basis`.
READ_PROVIDER = "provider"
READ_LINE = "line"
READ_NONE = "none"

_BASIS_SAID = {
    READ_PROVIDER: "read again from the provider",
    READ_LINE: "from its own copyright line, with no provider read",
    READ_NONE: "not asked, since no provider read was to hand for it",
}


@dataclass(frozen=True, slots=True)
class LabelListing:
    """What one label's crawl produced after verification and tombstones.

    ``listed`` is how many releases the crawl read, since the tuples do not add up
    to it: an owned release is skipped without a record and the window stops the
    loop early. The worker's "read N and confirmed none" refusal needs the N.
    """

    candidates: tuple[run.Candidate, ...]
    dropped: tuple[Dropped, ...]
    suppressed: tuple[run.Candidate, ...]
    listed: int = 0
    #: The parts of the catalogue the crawl could not read; non empty means
    #: ``listed`` counts part of the label (R-261).
    unread: tuple[Unread, ...] = ()
    #: Releases already in the review queue that took a place in the window (R-790).
    held: int = 0
    #: Releases listed past the full window that may still be the label's: each
    #: whose copyright line names the label's needle, and each with no line (U238).
    #: Nothing past the window was verified, tombstone checked or asked about
    #: ownership; it is the most the label could still offer.
    beyond: int = 0
    #: The part of ``beyond`` with no copyright line, unknown until read (U238).
    beyond_unchecked: int = 0
    #: ``held``, plus the standing gate holds, when the sweep confirmed nothing new
    #: and the held release re-verified did not confirm either, else zero (R-790,
    #: R-798). The worker counts these with ``dropped``.
    held_unconfirmed: int = 0
    #: The held release re-verified for ``held_unconfirmed``, or ``None`` (U277).
    canary: Canary | None = None
    #: Releases the genre gate is holding back, each taking a place in the window
    #: and not filed (R-798). Not ``held``, which is the queue's.
    gated: tuple[Gated, ...] = ()
    #: Standing holds this pass released; each is in ``candidates`` and its hold is
    #: dropped once filed.
    released: tuple[str, ...] = ()
    #: Holds in force that are holds no longer and will not be filed by this pass:
    #: deleted on purpose, now owned, or past the window and now passing. Each hold
    #: is dropped.
    stale: tuple[str, ...] = ()
    #: What the roster made of its kept listing (U217), ``None`` if it keeps none.
    kept: kept_listing.Summary | None = None


def kept_of(artist: Any) -> kept_listing.Summary | None:
    """The kept listing summary a roster carries, or ``None`` when it carries none."""
    held = getattr(artist, "kept", None)
    return held if isinstance(held, kept_listing.Summary) else None


def _year_of(release: Any) -> str:
    year = getattr(release, "year", None)
    if year is None:
        year = getattr(release, "release_date", "") or ""
    text = str(year)
    return text[:4] if len(text) >= 4 and text[:4].isdigit() else text


def _title_of(release: Any) -> str:
    return str(getattr(release, "title", "") or getattr(release, "name", "") or "")


def _suppression_reader(cfg: config.Config) -> Callable[[Any], bool]:
    """One tombstone question, answered against one read of the store.

    ``DecisionStore.suppresses`` reads the whole document per call, so the store is
    snapshotted once, as its docstring intends. The read is lazy, at the first
    release that asks, so an unreadable store refuses only a sweep with releases.
    A release with neither artist nor title is answered without reading.
    """
    snapshot: set[str] | None = None

    def tombstoned(release: Any) -> bool:
        nonlocal snapshot
        artist = artist_name(release)
        title = _title_of(release)
        if not artist and not title:
            return False
        if snapshot is None:
            store = DecisionStore(tombstone.STORE_KEY, cfg)
            # Suppressing records only: a revoked tombstone stays in the document.
            snapshot = {record.suppression_id for record in store.suppressions()}
        identity = tombstone.version_identity(artist=artist, title=title)
        return (
            review.suppression_id_for(
                tombstone.STORE_KEY, tombstone.KIND_VERSION, identity
            )
            in snapshot
        )

    return tombstoned


def _candidate(
    entry: registry.LabelEntry, release: Any, stamp: Mapping[str, Any] | None = None
) -> run.Candidate:
    """One release as the increment's candidate. ``stamp`` is what the gate said of it."""
    identity = str(getattr(release, "id", "") or "")
    return run.Candidate(
        identity=identity,
        recency=_year_of(release),
        payload={
            # The seam's reader, never ``str`` of a provider object (R-379).
            "artist": artist_name(release),
            "title": _title_of(release),
            "label_id": entry.label_id,
            "label_name": entry.name,
            "identity": identity,
            **(stamp or {}),
        },
    )


def _lookup_failure(message: str, exc: BaseException) -> run.LookupFailure:
    """``message`` as a lookup failure, marked rate limited when the provider said so (R-704).

    Asked of the error and every ``__cause__``, by the classifier the download
    adapter uses, so a resume retries what a wait would clear. An implicit
    ``__context__`` counts only when it carries the 429 status itself, as when a
    non JSON 429 body arrives as a decode error. A limit that trips the provider
    gate (R-705) parks the item as a ``CratekitError`` and never reaches here.
    """
    if any(is_rate_limit(link) for link in _linked(exc, "__cause__")):
        return run.LookupFailure(message, rate_limited=True)
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
        return run.LookupFailure(message, rate_limited=True)
    return run.LookupFailure(message)


def _linked(exc: BaseException, attribute: str) -> Iterator[BaseException]:
    """``exc`` and every error one link attribute leads to, once each, since links can loop."""
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = getattr(current, attribute, None)


def _crawl_or_refuse(
    entry: registry.LabelEntry, artist: Any
) -> tuple[list[Any], tuple[Unread, ...]]:
    """Every release for one label and what could not be read, or a refusal.

    Never a silent empty list (R-135) and never a silent half of one (R-261): the
    second value names every listing skipped, missing methods found here and the
    roster's own ``unread``. An object exposing no listing method, and an
    exception out of the probe or the crawl, raise ``run.LookupFailure``, which
    the increment turns into ``sync-source-lookups-failed``. An empty first page
    from a method that exists is a genuinely exhausted crawl. A
    ``CratekitError`` passes through unchanged, since an expired session names an
    act the person can take.
    """
    with translated(lambda exc: _lookup_failure(
        f"the catalogue object for {entry.name!r} could not be examined "
        f"({type(exc).__name__}: {exc}), so its releases were never read; "
        f"that is not an empty catalogue",
        exc,
    )):
        listable = crawl.can_list(artist)
    if not listable:
        raise run.LookupFailure(
            f"the catalogue object for {entry.name!r} exposes none of the listing "
            f"methods {', '.join(crawl.LISTING_METHODS)}, so its releases were "
            f"never read; that is not an empty catalogue"
        )
    skipped: list[str] = []
    with translated(lambda exc: _lookup_failure(
        f"the catalogue listing for {entry.name!r} could not be read "
        f"({type(exc).__name__}: {exc}); that is not an empty catalogue",
        exc,
    )):
        releases = list(crawl.releases(artist, skipped=skipped))
        built = tuple(getattr(artist, "unread", None) or ())
    return releases, (*built, *(missing_listing(artist, method) for method in skipped))


#: The library as the match engine sees it, what ``match_cli.library_view`` returns.
LibraryView = tuple[match.LibraryIndex, Callable[..., bool], Callable[..., str]]

#: How many release track reads in a row may fail before a label's other
#: releases are not asked; the shared reader's rule (R-798), kept by this name.
OUTAGE_AFTER = READS_FAILED_IN_A_ROW


def every_track_owned(resolved: Iterable[match.Match]) -> bool:
    """Whether a release's resolved tracks say the library holds it in full.

    Every track, and at least one, since ``all`` over nothing says owned. One
    spelling for the sweep and ``label approved`` (R-798).
    """
    states = [one.state for one in resolved]
    return bool(states) and all(state is match.MatchState.MATCHED for state in states)


class OwnedReleases:
    """The release identities the library already holds, asked one at a time (R-259).

    Ownership is a read: the release's tracks, each resolved against the library
    index. So this is a container that answers each identity when asked and keeps
    the answer, since the sweep and the increment both ask.

    Owned means every track, and at least one, resolves ``MATCHED``. Anything
    short of that, an unreadable row, another version, a gone release or a track
    read the provider could not answer, is not owned and so is offered: a wrong
    offer costs one decline, a wrong owned costs music never seen. The shared
    reader stops asking after :data:`OUTAGE_AFTER` failures in a row. A
    ``CratekitError`` passes through. The library is walked once, only when a
    release has tracks to resolve, and ``library`` lets a job share one walk.
    """

    def __init__(
        self,
        cfg: config.Config,
        catalogue: Catalogue | ReleaseTracks,
        *,
        library: Callable[[], LibraryView] | None = None,
    ) -> None:
        self.cfg = cfg
        #: Always a :class:`ReleaseTracks`, the worker's when it hands one, so the gate
        #: shares its reads and the outage rule is counted once (R-798).
        self.catalogue = (
            catalogue if isinstance(catalogue, ReleaseTracks) else ReleaseTracks(catalogue)
        )
        #: Looked up when first asked, so a release with no tracks walks nothing.
        self._library_of = library if library is not None else (
            lambda: match_cli.library_view(self.cfg)
        )
        self._view: LibraryView | None = None
        self._answers: dict[str, bool] = {}

    def __contains__(self, identity: object) -> bool:
        if not isinstance(identity, str) or not identity:
            return False
        if identity not in self._answers:
            self._answers[identity] = self._holds(identity)
        return self._answers[identity]

    def _library(self) -> LibraryView:
        if self._view is None:
            self._view = self._library_of()
        return self._view

    def _holds(self, release_id: str) -> bool:
        try:
            rows, _year, _short = self.catalogue.release_tracks(release_id)
        except CratekitError:
            raise
        except Exception:  # noqa: BLE001 - not owned, and the release is offered
            # Gone, failed, or not asked: each is not owned, and the reader keeps count.
            return False
        if not rows:
            return False
        try:
            wanted = match.read_tidal_tracks(rows)
        except match.UnreadableList:
            return False
        index, suppresses, identify = self._library()
        return every_track_owned(
            match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
            for one in wanted
        )


class QueuedReleases:
    """The release identities the label-release queue already holds, in any state (R-790).

    Such a release is never filed again and counts toward the window. ``also``
    holds identities that take a place the same way (U107), the releases the
    guided sync asked about, asked first as a set lookup.
    """

    def __init__(self, store: review.ReviewStore, also: Container[str] | None = None) -> None:
        self.store = store
        self.also = also

    def __contains__(self, identity: object) -> bool:
        if not isinstance(identity, str) or not identity:
            return False
        if self.also is not None and identity in self.also:
            return True
        return review.find(self.store, genre_gate.release_item_id(identity)) is not None


#: How a release's own copyright line reads against a label's needle, with no
#: provider call (U238, U277), in this order.
LINE_NAMES_LABEL = 0
LINE_ABSENT = 1
LINE_NAMES_OTHER = 2


def line_reading(release: Any, claimed: str) -> int:
    """Whether ``release``'s own copyright line names the label ``claimed`` is the needle of."""
    names = harvest.labels_from_copyright(release)
    if not names:
        return LINE_ABSENT
    if any(label_verify.labels_match(claimed, name) for name in names):
        return LINE_NAMES_LABEL
    return LINE_NAMES_OTHER


#: The verdict ``verify_release`` gives a credit the needle does not match.
MISMATCH = "mismatch"


def _answered_by_name(dropped: Sequence[Dropped]) -> bool:
    """Whether every release the sweep turned down was credited to another label's name."""
    return all(one.reason == MISMATCH for one in dropped)


def _canary_order(
    held: Sequence[Any], claimed: str, dropped: Sequence[Dropped]
) -> list[Any]:
    """The held releases in the order they are verified again, chosen by the sweep's drops.

    Only the first is asked, except that a forced read answering gone asks the
    next in its place (R-1634). A held release can be another act's, which the
    newest first order before U277 refused a label over.

    Every drop a mismatch: the verifier is answering, so the question is whether
    the needle still names the label's releases, and a held release whose line
    names the label goes first, then no line, then another label's line.

    Any other drop: the question is whether the provider answers at all, so the
    release is read from the provider whatever its line (R-1634), no line first,
    then the label's line, then another act's, which answers ``mismatch`` however
    healthy the provider is (R-1635). Always asked of a verifier.
    """
    if _answered_by_name(dropped):
        return sorted(held, key=lambda release: line_reading(release, claimed))

    def read_first(release: Any) -> tuple[bool, int]:
        reading = line_reading(release, claimed)
        return reading != LINE_ABSENT, reading

    return sorted(held, key=read_first)


def _past_window(beyond: Iterable[Any], claimed: str) -> tuple[int, int]:
    """How many releases past the window may be the label's, and how many of those are unchecked.

    Judged by each release's own copyright line with no provider call (U238): a
    line naming the label counts, another label's does not, no line is unchecked.
    """
    own = unchecked = 0
    for release in beyond:
        reading = line_reading(release, claimed)
        if reading == LINE_ABSENT:
            unchecked += 1
        elif reading == LINE_NAMES_LABEL:
            own += 1
    return own, unchecked


def _turned_down(
    claimed: str, release: Any, verify: Callable[[str, Any], Mapping[str, Any]]
) -> Dropped | None:
    """The drop for a release the verifier does not confirm as the label's, else None."""
    verdict = label_verify.verify_release(claimed, release, search=verify)
    status = str(verdict.get("verdict") or "unconfirmed")
    if status == "confirmed":
        return None
    return Dropped(
        identity=str(getattr(release, "id", "") or ""),
        reason=status,
        notes=str(verdict.get("notes") or ""),
    )


def list_for_label(
    cfg: config.Config,
    entry: registry.LabelEntry,
    *,
    artist: Any,
    verify: Callable[[str, Any], Mapping[str, Any]],
    reread: Callable[[str, Any], Mapping[str, Any]] | None = None,
    last_pulled: str | None = None,
    owned: Container[str] | None = None,
    offered: Container[str] | None = None,
    limit: int | None = None,
    gate: genre_gate.SweepGate | None = None,
) -> LabelListing:
    """Crawl, verify, drop unconfirmed, report tombstones. Ignore ``last_pulled``.

    ``reread`` is the forced provider read (R-1634), asked only for the one held
    release re-verified when a drop was not a mismatch; ``None`` leaves a held
    release carrying a line unasked and not confirmed. ``last_pulled`` is accepted
    and not read. A listing that could not be read raises ``run.LookupFailure``.

    The offer is a window over the newest releases, never a date (R-790, KTD11):
    ``limit``, or :func:`registry.effective_offer`, places. A release already in
    the queue (``offered``) takes a place and is not filed again, even once owned;
    a release filed now takes a place; one owned without being offered, or
    tombstoned, takes none. What the window never reached is counted in
    ``beyond``, less each release whose line names another label (U238).

    The genre gate (R-798) is asked last, about a release that would otherwise be
    filed; a held release is reported in ``gated``, takes a place in the window so
    a label of another kind is not read to its end, and is never filed. A release
    the gate already holds is judged again from its recorded words before
    verification, and every hold in force is judged again, reached or not: one
    past the window that would now pass, deleted on purpose or now owned is
    reported in ``stale`` and its hold dropped, except one ``label judge``
    withheld from review (R-815), whose hold stands.
    """
    del last_pulled
    claimed = entry.match or entry.name
    listed, unread = _crawl_or_refuse(entry, artist)
    listed.sort(key=_year_of, reverse=True)
    owned_ids: Container[str] = owned if owned is not None else frozenset()
    offered_ids: Container[str] = offered if offered is not None else frozenset()
    cap = (
        limit
        if limit is not None
        else registry.effective_offer(entry, cfg.labels.offer_per_sweep)
    )

    candidates: list[run.Candidate] = []
    dropped: list[Dropped] = []
    suppressed: list[run.Candidate] = []
    tombstoned = _suppression_reader(cfg)
    # The local questions first: a tombstone is the person's decision, so a
    # tombstoned release is suppressed before any provider call. Ownership is asked
    # after verification, since it reads the release's tracks (R-259), and an owned
    # release takes no place (R-137). A release already in the queue is asked before
    # verification too: it was verified when filed and takes a place (R-790).
    held = 0
    held_releases: list[Any] = []
    examined = 0
    gated: list[Gated] = []
    released: list[str] = []
    stale: list[str] = []
    reached: set[str] = set()
    for release in listed:
        if held + len(gated) + len(candidates) >= cap:
            break
        examined += 1
        identity = str(getattr(release, "id", "") or "")
        reached.add(identity)
        if tombstoned(release):
            suppressed.append(_candidate(entry, release))
            # Deleted on purpose outranks held, so its hold goes.
            was = gate.standing(identity) if gate is not None else None
            if was is not None and was.state == review.HOLD_HELD:
                stale.append(identity)
            continue
        standing = gate.standing(identity) if gate is not None else None
        if identity in offered_ids:
            held += 1
            held_releases.append(release)
            # In the queue and still held, which a process dying between two writes or a
            # moved queue can leave: the queue is the truth, so its hold goes.
            if standing is not None and standing.state == review.HOLD_HELD:
                stale.append(identity)
            continue
        if standing is not None and standing.state == review.HOLD_RETURNED:
            # A person returned it and the queue does not hold it: filed, never judged.
            candidates.append(_candidate(entry, release, genre_gate.returned_stamp()))
            continue
        if standing is not None:
            again = gate.rejudge(entry, standing)
            if again.held:
                gated.append(Gated(_candidate(entry, release), again, standing=True))
                held_releases.append(release)
            elif identity in owned_ids:
                # Owned while held: nothing to file or hold, and no place taken. Asked only
                # of a hold being released, since the answer is a provider read.
                stale.append(identity)
            else:
                candidates.append(_candidate(entry, release, again.stamp()))
                released.append(identity)
            continue
        drop = _turned_down(claimed, release, verify)
        if drop is not None:
            dropped.append(drop)
            continue
        if identity in owned_ids:
            continue
        if gate is None:
            candidates.append(_candidate(entry, release))
            continue
        judged = gate.judge(entry, identity)
        if judged.held:
            gated.append(Gated(_candidate(entry, release), judged))
        else:
            candidates.append(_candidate(entry, release, judged.stamp()))
    # One held release is re-verified, only when the sweep confirmed nothing it
    # asked about: it was confirmed when filed, so its answer says whether the
    # endpoint is up. The first of :func:`_canary_order` (U277).
    #
    # Every drop a mismatch: the ordinary verifier is asked, which judges a held
    # label line from that line. Any other drop: the provider is read through
    # ``reread`` whatever the line (R-1634). Without ``reread`` a release with no
    # line is asked of the verifier and one with a line counts as not confirmed.
    held_unconfirmed = 0
    canary: Canary | None = None
    if held_releases and dropped and not candidates:
        order = _canary_order(held_releases, claimed, dropped)
        chosen = order[0]
        lined = line_reading(chosen, claimed) != LINE_ABSENT
        # The ordinary verifier for every drop a mismatch, and for a release with no
        # line when there is no forced read to hand.
        if _answered_by_name(dropped) or (reread is None and not lined):
            answered = label_verify.verify_release(claimed, chosen, search=verify)
            basis = READ_LINE if lined else READ_PROVIDER
        elif reread is not None:
            answered = label_verify.verify_release(claimed, chosen, search=reread)
            basis = READ_PROVIDER
            # A held release the provider has withdrawn is still listed by a kept listing
            # for up to seven days, and its 404 says nothing of credits, so the next held
            # release the label can still confirm is read in its place, once (R-1634). A
            # second gone answer, or none to ask, stands and refuses.
            following = [
                one for one in order[1:] if line_reading(one, claimed) != LINE_NAMES_OTHER
            ]
            if answered.get("verdict") == RELEASE_GONE and following:
                first = str(getattr(chosen, "id", "") or "")
                chosen = following[0]
                answered = dict(
                    label_verify.verify_release(claimed, chosen, search=reread)
                )
                said = f"read in place of release {first}, which the provider no longer has"
                notes = str(answered.get("notes") or "")
                answered["notes"] = f"{notes}; {said}" if notes else said
        else:
            answered = {"verdict": "unconfirmed", "notes": "no provider read"}
            basis = READ_NONE
        canary = Canary(
            identity=str(getattr(chosen, "id", "") or ""),
            artist=artist_name(chosen),
            title=_title_of(chosen),
            verdict=str(answered.get("verdict") or "unconfirmed"),
            notes=str(answered.get("notes") or ""),
            basis=basis,
        )
        if not canary.confirmed:
            held_unconfirmed = held + sum(1 for one in gated if one.standing)
    own_past, unchecked_past = _past_window(listed[examined:], claimed)
    if gate is not None:
        for standing in gate.in_force(entry.label_id):
            beyond_id = str(standing.identity.get("release_id") or "")
            if not beyond_id or beyond_id in reached:
                continue
            if standing.payload.get(review.WITHHELD_FIELD):
                continue
            if not gate.rejudge(entry, standing).held:
                stale.append(beyond_id)
    return LabelListing(
        candidates=tuple(candidates),
        dropped=tuple(dropped),
        suppressed=tuple(suppressed),
        listed=len(listed),
        unread=unread,
        held=held,
        beyond=own_past + unchecked_past,
        beyond_unchecked=unchecked_past,
        held_unconfirmed=held_unconfirmed,
        canary=canary,
        gated=tuple(gated),
        released=tuple(released),
        stale=tuple(stale),
        kept=kept_of(artist),
    )


#: The payload field naming the sweep run that filed a label release (R-790),
#: spelled once in the review module for ``review list --group-by run``.
SWEEP_RUN = review.RUN_FIELD


def offer_release(
    store: review.ReviewStore,
    candidate: run.Candidate,
    *,
    handler_key: str = HANDLER_KEY,
    run_id: str | None = None,
) -> review.Item:
    """File one release, recording ``run_id`` as the sweep that filed it.

    An item already in the queue keeps the run that first filed it, so an old
    release never reads as new in a grouping by run.
    """
    payload = dict(candidate.payload or {})
    payload.setdefault("identity", candidate.identity)
    if run_id:
        existing = review.find(store, genre_gate.release_item_id(candidate.identity))
        held_run = existing.payload.get(SWEEP_RUN) if existing is not None else None
        payload[SWEEP_RUN] = held_run or run_id
    return review.offer(
        store,
        queue=Queue.LABEL_RELEASE,
        kind=KIND,
        identity={"release_id": candidate.identity},
        payload=payload,
        handler_key=handler_key,
    )


def _guarded(read: Callable[[str, Any], Mapping[str, Any]]) -> Callable[[str, Any], Mapping[str, Any]]:
    """A catalogue's verifying read, a provider failure turned into ``run.LookupFailure``.

    A ``CratekitError`` passes through unchanged.
    """

    def verified(claimed: str, release: Any) -> Mapping[str, Any]:
        with translated(lambda exc: _lookup_failure(
            f"the catalogue could not confirm who is credited on a "
            f"release ({type(exc).__name__}: {exc}); the releases "
            f"this sweep listed were never verified, and an "
            f"unverified release is not a release with no match",
            exc,
        )):
            return read(claimed, release)

    return verified


class LabelSource:
    """The ``labels`` increment source. ``id`` is the source identifier, not a name."""

    id = "labels"

    #: This source offers, it does not acquire: the increment appends nothing to
    #: the importable file and moves no watermark over it (R-140).
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
        gate: genre_gate.SweepGate | None = None,
        run_id: str | None = None,
        offered: Container[str] | None = None,
    ) -> None:
        self.cfg = cfg
        #: The genre gate every listing is judged by, or None (R-798).
        self.gate = gate
        #: Identities that take a place in the window beside the queued releases: what
        #: the guided sync already asked about (U107).
        self.offered = offered
        #: The sweep run a hold is recorded under; the increment hands the listing none.
        self.run_id = run_id
        #: The standing holds the last pass released, dropped as each is filed.
        self._released: frozenset[str] = frozenset()
        #: The release identities the library holds, handed to every listing so an
        #: owned release is dropped before the window (R-137). The worker passes the
        #: same :class:`OwnedReleases` to the increment, so each release is read once.
        self.owned = owned
        self.registry = registry
        self.artists = dict(artists or {})
        self.verify = verify
        #: An open review store to offer into, or ``None`` to open one per offer. The
        #: worker opens one around the increment so offers do not reopen and checkpoint
        #: the database each time; ``review.offer`` still commits per call.
        self.store = store
        #: A ``label.catalogue.Catalogue``, supplying both pieces above from one object.
        self.catalogue = catalogue
        #: Every release the last pass read and discarded, across its labels, so the
        #: worker can tell a catalogue that confirms nothing from one with nothing new.
        #: Instance state is safe: the worker builds one source per item. This and the
        #: three below are rebuilt per pass.
        self.dropped: tuple[Dropped, ...] = ()
        #: How many releases the last pass read, summed over its labels.
        self.read = 0
        #: What the last pass could not read (R-261, R-393).
        self.unread: tuple[Unread, ...] = ()
        #: Every label the last pass listed, with its listing, for each ``beyond`` (R-790).
        self.listings: tuple[tuple[registry.LabelEntry, LabelListing], ...] = ()
        #: Held releases the last pass could not confirm again, summed.
        self.held_unconfirmed = 0

    def _artist_for(self, entry: registry.LabelEntry) -> Any:
        """The provider artist object for one favourite label, or a refusal.

        A label with no object is reachable through the plain ``artists`` mapping, and
        skipping it would report a sweep that found nothing new (R-135), so it raises.
        A foreign exception from the seam becomes ``run.LookupFailure`` with its cause
        kept; a ``CratekitError`` passes through. One unreadable label refuses the
        whole source: nothing is lost, since the next run lists from scratch. The
        explicit piece wins over the catalogue, as in :meth:`_verifier`.
        """
        artist = self.artists.get(entry.label_id)
        if artist is not None:
            return artist
        if self.catalogue is not None:
            with translated(lambda exc: _lookup_failure(
                f"the catalogue could not resolve an artist for the label "
                f"{entry.name!r} ({type(exc).__name__}: {exc}); its releases "
                f"were never listed",
                exc,
            )):
                return self.catalogue.artist_for(entry)
        raise run.LookupFailure(
            f"no catalogue object was available for the registered label "
            f"{entry.name!r}, so its releases were never listed; that is not "
            f"a label with nothing new"
        )

    def _verifier(self) -> Callable[[str, Any], Mapping[str, Any]]:
        """The release verification callable, or a refusal for the same reason.

        A sweep that cannot verify would drop every release and look like a label
        with nothing new. Explicit piece first, then the catalogue's read, guarded so
        a provider failure is ``run.LookupFailure`` rather than an internal error,
        then a refusal. A ``CratekitError`` passes through unchanged.
        """
        if self.verify is not None:
            return self.verify
        if self.catalogue is not None:
            return _guarded(self.catalogue.search_release)
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )

    def _rereader(self) -> Callable[[str, Any], Mapping[str, Any]] | None:
        """The forced provider read for the one held release re-verified (R-1634), or ``None``.

        The catalogue's ``reread_release``, guarded as :meth:`_verifier` is, taken
        only when the verifier is the catalogue's own.
        """
        if self.verify is not None or self.catalogue is None:
            return None
        catalogue = self.catalogue
        # Looked up when asked, so a pass that never re-verifies never names it.
        return _guarded(lambda claimed, release: catalogue.reread_release(claimed, release))

    def list_recent(self, n: int) -> list[run.Candidate]:
        """The newest N candidates, and a record of what was thrown away getting them.

        The records are rebuilt from this pass and assigned once the loop finishes,
        since a pass that raises refuses the whole source. Truncation to ``n`` does
        not touch them: a deferred candidate was confirmed, a discarded one never was.
        """
        # The verifier is resolved once, and only when there is a label to verify for.
        verify = self._verifier() if self.registry.labels else None
        reread = self._rereader()
        listings: list[tuple[registry.LabelEntry, LabelListing]] = []
        with self._queue() as store:
            offered = QueuedReleases(store, self.offered) if store is not None else None
            for entry in self.registry.labels.values():
                listing = list_for_label(
                    self.cfg,
                    entry,
                    artist=self._artist_for(entry),
                    verify=verify,
                    reread=reread,
                    owned=self.owned,
                    offered=offered,
                    gate=self.gate,
                )
                if store is not None:
                    self._record_holds(store, entry, listing)
                listings.append((entry, listing))
        lists = [listing for _, listing in listings]
        self.dropped = tuple(drop for listing in lists for drop in listing.dropped)
        self.unread = tuple(one for listing in lists for one in listing.unread)
        self.listings = tuple(listings)
        self.held_unconfirmed = sum(listing.held_unconfirmed for listing in lists)
        self._released = frozenset(identity for listing in lists for identity in listing.released)
        self.read = sum(listing.listed for listing in lists)
        found = [candidate for listing in lists for candidate in listing.candidates]
        found.sort(key=lambda item: item.recency, reverse=True)
        return found[:n] if n >= 0 else found

    def _record_holds(
        self, store: review.ReviewStore, entry: registry.LabelEntry, listing: LabelListing
    ) -> None:
        """Record every release the gate held in this listing, as it was judged.

        Written when the listing is made, since a hold is true whatever happens to
        the rest of the sweep. A standing hold is refreshed and keeps its first run;
        a stale hold is dropped here.
        """
        for identity in listing.stale:
            _drop_hold(store, identity)
        for one in listing.gated:
            payload = dict(one.candidate.payload or {})
            payload.setdefault("identity", one.candidate.identity)
            review.hold(
                store,
                queue=Queue.LABEL_RELEASE,
                kind=KIND,
                identity={"release_id": one.candidate.identity},
                payload=payload,
                group=entry.label_id,
                name=entry.name,
                reason=one.judged.reason,
                detail=one.judged.detail(),
                run_id=self.run_id or "",
            )

    @contextmanager
    def _queue(self) -> Iterator[review.ReviewStore | None]:
        """The open store the worker handed, else one for this pass, or None for no label."""
        if self.store is not None:
            yield self.store
            return
        if not self.registry.labels:
            yield None
            return
        with review.open_store(self.cfg) as own:
            yield own

    def process(
        self,
        candidate: run.Candidate,
        artifacts,
        run_id: str,
        store: review.ReviewStore | None = None,
    ) -> None:
        del artifacts
        opened = store if store is not None else self.store
        if opened is not None:
            self._file(opened, candidate, run_id)
            return
        with review.open_store(self.cfg) as own:
            self._file(own, candidate, run_id)

    def _file(self, store: review.ReviewStore, candidate: run.Candidate, run_id: str) -> None:
        """Offer one release, then drop the hold it was released from, if any. The offer first."""
        offer_release(store, candidate, run_id=run_id)
        if candidate.identity in self._released:
            _drop_hold(store, candidate.identity)


def _drop_hold(store: review.ReviewStore, identity: str) -> None:
    """Drop the genre gate's hold on one release."""
    review.release_hold(
        store, queue=Queue.LABEL_RELEASE, item_id=genre_gate.release_item_id(identity)
    )


@dataclass(frozen=True, slots=True)
class Confirmed:
    """A label's whole catalogue as the crawl and the verifier confirm it (R-835).

    ``releases`` is every confirmed release no tombstone suppresses, newest first;
    ``listed`` everything the crawl read; ``unread`` what it could not read.
    """

    releases: tuple[Any, ...]
    listed: int
    dropped: tuple[Dropped, ...]
    suppressed: int
    unread: tuple[Unread, ...]
    #: The releases a tombstone suppressed, so a reader can judge their tracks (U243).
    suppressed_releases: tuple[Any, ...] = ()


@dataclass(frozen=True, slots=True)
class Listed:
    """One label's catalogue as the crawl lists it, before anything is read per release.

    The first half of :func:`confirmed_releases` (U191). ``claimed`` and ``verify``
    are built before the crawl, so a missing verifier refuses before any call.
    """

    releases: tuple[Any, ...]
    unread: tuple[Unread, ...]
    claimed: str
    verify: Callable[[str, Any], Mapping[str, Any]]
    #: What the roster made of the label's kept listing (U217), or ``None``.
    kept: kept_listing.Summary | None = None


def listed_releases(
    cfg: config.Config, entry: registry.LabelEntry, found: Catalogue
) -> Listed:
    """Every release the crawl lists for one label, and nothing read per release (U191)."""
    source = LabelSource(
        cfg, registry=registry.Registry(labels={entry.label_id: entry}), catalogue=found
    )
    artist = source._artist_for(entry)
    verify = source._verifier()
    listed, unread = _crawl_or_refuse(entry, artist)
    return Listed(
        releases=tuple(listed),
        unread=tuple(unread),
        claimed=entry.match or entry.name,
        verify=verify,
        kept=kept_of(artist),
    )


def confirm_listed(cfg: config.Config, listed: Listed) -> Confirmed:
    """The releases of one listing the catalogue confirms, the second half (U191).

    The tombstone first because it is local, then the verifier.
    """
    ordered = sorted(listed.releases, key=_year_of, reverse=True)
    tombstoned = _suppression_reader(cfg)
    confirmed: list[Any] = []
    dropped: list[Dropped] = []
    held_back: list[Any] = []
    for release in ordered:
        if tombstoned(release):
            held_back.append(release)
            continue
        drop = _turned_down(listed.claimed, release, listed.verify)
        if drop is not None:
            dropped.append(drop)
            continue
        confirmed.append(release)
    return Confirmed(
        releases=tuple(confirmed),
        listed=len(ordered),
        dropped=tuple(dropped),
        suppressed=len(held_back),
        unread=listed.unread,
        suppressed_releases=tuple(held_back),
    )


def confirmed_releases(
    cfg: config.Config, entry: registry.LabelEntry, found: Catalogue
) -> Confirmed:
    """Every release of one label the catalogue confirms, with no window and no gate.

    The crawl :func:`list_for_label` reads, asked the same questions in the same
    order, without the review half, since a label's folder on the account mirrors
    its catalogue. A listing that could not be read raises ``run.LookupFailure``.
    """
    return confirm_listed(cfg, listed_releases(cfg, entry, found))


#: The year a release reads as, ``""`` when none, for the label folder (R-835).
year_of = _year_of
