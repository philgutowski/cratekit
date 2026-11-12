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

from collections.abc import Callable, Container, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
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
    Catalogue,
    ReleaseTracks,
    Unread,
    artist_name,
    missing_listing,
)
from cratekit.sync import run

#: The review kind a release is filed under. The gate module declares the
#: word, since this module imports that one, and this is the same object.
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

    ``standing`` says the hold was already recorded by an earlier sweep and was
    judged again from its own words. Such a release was not verified this
    sweep, which is why the worker's "confirmed none" refusal counts it with
    the queued ones.
    """

    candidate: run.Candidate
    judged: genre_gate.Judged
    standing: bool = False


@dataclass(frozen=True, slots=True)
class Canary:
    """The one held release a sweep verified again, and what the verifier answered (U277).

    Asked only when the sweep turned down every release it asked about and
    holds one, chosen as :func:`_canary_of` says. Carried on the listing so the
    run can say which release it was and what it answered: ``unconfirmed`` is
    a release the verifier found no label credit for, the answer a provider
    that is not answering gives, and ``mismatch`` one credited to a name the
    needle does not match, with the name in ``notes``.
    """

    identity: str
    artist: str
    title: str
    verdict: str
    notes: str = ""

    @property
    def confirmed(self) -> bool:
        return self.verdict == "confirmed"

    def said(self) -> str:
        """The release and its answer, in words a refusal or a check can carry."""
        named = f"{self.title!r} by {self.artist}" if self.artist else repr(self.title)
        answer = f"answered {self.verdict}"
        if self.notes:
            answer += f" ({self.notes})"
        return f"{named}, release {self.identity}, {answer}"

    def to_json(self) -> dict[str, str]:
        return {
            "identity": self.identity,
            "artist": self.artist,
            "title": self.title,
            "verdict": self.verdict,
            "notes": self.notes,
        }


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
    #: Releases ALREADY IN THE REVIEW QUEUE that took a place in the offer
    #: window and were not filed again (R-790).
    held: int = 0
    #: Releases the crawl listed past the full window that may still be the
    #: label's: each whose copyright line names the label by its needle, and
    #: each with no line at all (U238). A release whose line plainly names
    #: another label is left out, since verification would call it a mismatch
    #: and it is only another artist of the roster's release elsewhere. NOT a
    #: count of unowned releases: nothing past the window was verified with a
    #: provider read, tombstone checked or asked about ownership, because each
    #: of those questions costs a call or a judgement the window never made. It
    #: is the most the label could still offer, and the number a person raises
    #: the window against.
    beyond: int = 0
    #: The part of ``beyond`` with NO COPYRIGHT LINE, so whether each is the
    #: label's is unknown until the provider is read again, the read a sweep
    #: makes only inside its window (U238). Counted in ``beyond`` rather than
    #: dropped from it, because a field the listing omitted is not evidence of
    #: another label, and said as a bound rather than as the label's releases.
    beyond_unchecked: int = 0
    #: ``held`` when the sweep confirmed nothing new and the one held release
    #: it then re-verified did not confirm either, else zero. The worker's
    #: "confirmed none of what it read" refusal counts these with ``dropped``,
    #: because before R-790 every held release was verified again and a dead
    #: endpoint dropped them too; without this, a label with anything in the
    #: queue would report "nothing new" over a verifier that answers nothing.
    #: A release the genre gate was already holding counts here too, since it
    #: is not verified again either (R-798).
    held_unconfirmed: int = 0
    #: The held release re-verified for ``held_unconfirmed`` and its answer, or
    #: ``None`` when none was asked (U277). The run says it, so a person
    #: reading a refusal knows what was asked and what the verifier answered.
    canary: Canary | None = None
    #: Releases THE GENRE GATE IS HOLDING BACK, each of which took a place in
    #: the offer window and was not filed (R-798). Not ``held`` above, which is
    #: the releases already in the queue: the two words met by accident, and
    #: this one is the gate's.
    gated: tuple[Gated, ...] = ()
    #: The identities of standing holds this pass RELEASED, because the gate no
    #: longer holds them. Each is in ``candidates``, and its hold is dropped
    #: once it is filed.
    released: tuple[str, ...] = ()
    #: The identities of holds in force that are HOLDS NO LONGER and will not be
    #: filed by this pass: the release was deleted on purpose, the library came
    #: to own it, or the window does not reach it and the gate would now pass
    #: it. Each hold is dropped, so the held count is of releases the gate is
    #: actually keeping out. One the window does not reach becomes what any
    #: release past the window is, unexamined, and is judged when it is reached.
    stale: tuple[str, ...] = ()
    #: What the label's roster made of its kept listing (U217): reused from an
    #: earlier run, asked now and why. ``None`` from a catalogue that keeps none.
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
        artist = artist_name(release)
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


def _candidate(
    entry: registry.LabelEntry, release: Any, stamp: Mapping[str, Any] | None = None
) -> run.Candidate:
    """One release as the increment's candidate. ``stamp`` is what the gate said of it."""
    identity = str(getattr(release, "id", "") or "")
    return run.Candidate(
        identity=identity,
        recency=_year_of(release),
        payload={
            # The seam's reader, never ``str``: the provider's artist is an
            # object and its text is a memory address (R-379).
            "artist": artist_name(release),
            "title": _title_of(release),
            "label_id": entry.label_id,
            "label_name": entry.name,
            "identity": identity,
            **(stamp or {}),
        },
    )


def _lookup_failure(message: str, exc: BaseException) -> run.LookupFailure:
    """``message`` as a lookup failure, marked rate limited when the provider said so.

    R-704. The eleventh sitting's sweep failed 20 of 47 labels over
    ``TooManyRequests: Album unavailable`` and recorded every one permanent,
    so resuming could not retry what a wait would have cleared. The question
    is asked of the error and of every error it was declared from, ``raise X
    from exc``, because a client that wraps the provider's answer still carries
    it. The classifier is the one R-703's download adapter uses, so the two
    readers of one answer cannot disagree.

    AN IMPLICIT ``__context__`` COUNTS ONLY WHEN IT CARRIES THE STATUS ITSELF.
    ``core.cause._chain`` does not follow context, because "raised while
    handling" is not "is", and a guess from a context's type or words would be
    exactly that. The provider's structured 429 is not a guess. The client
    translates an HTTP error by reading the response body as JSON first, so a
    429 whose body is not JSON, a gateway's page, arrives as a decode error
    raised while handling the 429 and names the limit nowhere else; the 429
    sits two contexts down, under the standard library's own decode error.

    Six rate limit answers in a row trip the provider gate (R-705), which
    parks the item as ``Parked``, a ``CratekitError`` that passes every
    boundary here unchanged. What reaches this helper is a limit that did not
    trip it, most often on a call with no retry ladder of its own,
    verification or the artist resolve.
    """
    if any(is_rate_limit(link) for link in _linked(exc, "__cause__")):
        return run.LookupFailure(message, rate_limited=True)
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
        return run.LookupFailure(message, rate_limited=True)
    return run.LookupFailure(message)


def _linked(exc: BaseException, attribute: str) -> Iterator[BaseException]:
    """``exc`` and every error one link attribute leads to, once each.

    The ``seen`` set is ``core.cause._chain``'s: both links are assignable, so
    two errors can name each other and the walk would never end.
    """
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
#: THE SAME NUMBER AS THE SHARED READER'S, by being it. The rule itself lives
#: in :class:`~cratekit.label.catalogue.ReleaseTracks` since R-798, and this
#: name is kept for the callers and the docstrings that cite it.
OUTAGE_AFTER = READS_FAILED_IN_A_ROW


def every_track_owned(resolved: Iterable[match.Match]) -> bool:
    """Whether a release's resolved tracks say the library holds it in full.

    EVERY TRACK, AND AT LEAST ONE. ``all`` over nothing would say owned. One
    spelling, for the sweep's ownership question and for ``label approved``,
    which asks it to decide whether a release still needs judging (R-798).
    """
    states = [one.state for one in resolved]
    return bool(states) and all(state is match.MatchState.MATCHED for state in states)


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
        catalogue: Catalogue | ReleaseTracks,
        *,
        library: Callable[[], LibraryView] | None = None,
    ) -> None:
        self.cfg = cfg
        #: ALWAYS A :class:`ReleaseTracks`, the worker's when it hands one, so
        #: the genre gate shares its reads, else one of this object's own. The
        #: outage rule is that reader's and is counted nowhere else (R-798):
        #: this class kept a counter of its own until the second review, two
        #: counters on one read path that could come to disagree about when
        #: the provider is down.
        self.catalogue = (
            catalogue if isinstance(catalogue, ReleaseTracks) else ReleaseTracks(catalogue)
        )
        self._library_of = library
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
            if self._library_of is not None:
                self._view = self._library_of()
            else:
                self._view = match_cli.library_view(self.cfg)
        return self._view

    def _holds(self, release_id: str) -> bool:
        try:
            rows, _year, _short = self.catalogue.release_tracks(release_id)
        except CratekitError:
            raise
        except Exception:  # noqa: BLE001 - not owned, and the release is offered
            # A release that is gone, one the provider failed on, and one the
            # reader did not ask for because the provider is failing: each is
            # not owned, and the reader keeps the count.
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
    """The release identities the label-release queue already holds, in any state.

    R-790. A release with an item is a release somebody was already offered:
    open, accepted, declined or superseded, the sweep never files it again,
    and :func:`list_for_label` counts it toward the offer window instead. Asked
    one identity at a time against the open store, because the window stops the
    walk long before a label's catalogue runs out.

    ``also`` is a second container of identities that take a place as a queued
    release does (U107): the releases a person was ASKED about by the guided
    sync and answered for, which were never filed when the answer did not
    take them. Asked first, because its answer is a set lookup and the
    queue's is a database read.
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


#: How a release's own copyright line reads against a label's needle, by
#: harvest's one extractor and ``labels_match``, with no provider call (U238,
#: U277). Ordered: a line naming the label first, no line second, a line
#: naming another label last.
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


#: The verdict ``verify_release`` gives a release whose credit names another
#: label: the verifier answered, with a name the needle does not match.
MISMATCH = "mismatch"


def _canary_of(held: Sequence[Any], claimed: str, dropped: Sequence[Dropped]) -> Any:
    """The held release to verify again, chosen by what the sweep's drops say.

    THE NEWEST HELD RELEASE WAS THE CANARY BEFORE U277, and a held release can
    be another act's: a sync that asked about releases a looser needle once
    confirmed holds them still. Sitting 94 read Rawax's listing with three
    ``RAWAXXX`` releases held newest and four ``Rawax`` ones below them, the
    newest answered mismatch, and the label refused as one whose catalogue
    nothing could confirm.

    EVERY DROP A MISMATCH: the verifier answered each release it was asked
    about with another label's name, so it is answering, and what is left to
    know is whether the needle still names any of the label's releases. A held
    release whose own line names the label shows it does, so it is asked
    first, then one with no line, then one whose line names another label.

    ANY DROP THE VERIFIER GAVE NO ANSWER FOR: the question is whether it is
    answering at all, and a release carrying a line answers nothing about
    that, because the catalogue judges such a release from its line with no
    provider call (round one of U277's review drove a degraded provider to
    "nothing new" over a held Rawax line). So a held release with no line is
    asked first, the one the provider is read for, and otherwise the newest,
    as before U277. Where no held release lacks a line, that newest one is
    judged from its own line too, as it was before U277, and says nothing of
    the provider either (the residual U277 filed). It can answer differently
    from before: a lineless held release the provider answers for clears the
    label where an older newest held release of another act would have
    refused it, and a degraded provider refuses where a newest held label line
    would have let it pass.

    ALWAYS ASKED OF THE VERIFIER, never answered here from the line.
    """
    if all(one.reason == MISMATCH for one in dropped):
        return min(held, key=lambda release: line_reading(release, claimed))
    return min(held, key=lambda release: line_reading(release, claimed) != LINE_ABSENT)


def _past_window(beyond: Iterable[Any], claimed: str) -> tuple[int, int]:
    """How many releases past the window may be the label's, and how many of those are unchecked.

    JUDGED BY EACH RELEASE'S OWN COPYRIGHT LINE, WITH NO PROVIDER CALL (U238).
    The line is already on every listed release, and it is what the provider's
    verifier judges a release by inside the window: harvest's one extractor,
    then ``labels_match`` against the same needle. A line naming the label
    counts; a line naming another label does not; no line counts as
    unchecked, because confirming it is the read the window exists to bound.
    Before this every release of every artist on the roster was counted, and
    a label with about 27 of its own left said 414.
    """
    own = unchecked = 0
    for release in beyond:
        reading = line_reading(release, claimed)
        if reading == LINE_ABSENT:
            unchecked += 1
        elif reading == LINE_NAMES_LABEL:
            own += 1
    return own, unchecked


def list_for_label(
    cfg: config.Config,
    entry: registry.LabelEntry,
    *,
    artist: Any,
    verify: Callable[[str, Any], Mapping[str, Any]],
    last_pulled: str | None = None,
    owned: Container[str] | None = None,
    offered: Container[str] | None = None,
    limit: int | None = None,
    gate: genre_gate.SweepGate | None = None,
) -> LabelListing:
    """Crawl, verify, drop unconfirmed, report tombstones. Ignore ``last_pulled``.

    ``last_pulled`` is accepted so a caller that still thinks in date floors
    cannot accidentally get a different function. It is not read.

    A listing that could not be READ raises ``run.LookupFailure`` rather than
    returning an empty :class:`LabelListing`. See :func:`_crawl_or_refuse`.

    THE OFFER IS A WINDOW OVER THE NEWEST RELEASES, AND NEVER A DATE (R-790,
    KTD11). ``limit``, or the label's :func:`registry.effective_offer`, is how
    many places the window has. A release already in the queue, ``offered``,
    takes a place and is not filed again, EVEN ONCE IT IS OWNED, because a
    release accepted and downloaded must not hand its place to the next slice
    of back catalogue; a release filed now takes a place; a release owned
    without ever being offered, or tombstoned, takes none. So a first sweep
    files the window, and a later one files only what has appeared above the
    releases it already holds, whatever any watermark says. What the window
    never reached is counted in ``beyond`` rather than dropped, less each
    release whose copyright line names another label (U238).

    THE GENRE GATE IS ASKED LAST, ABOUT A RELEASE THAT WOULD OTHERWISE BE FILED
    (R-798). ``gate`` judges it by what a general catalogue publishes for its
    tracks, and a release that is not the kind of music the label is followed
    for is HELD: reported in ``gated``, not a candidate, and never filed. Left
    as None nothing is judged and every candidate is filed as before.

    A HELD RELEASE TAKES A PLACE IN THE WINDOW. A label whose newest releases
    are all another label's music would otherwise be read to the end of its
    catalogue looking for ones that pass, three calls a release, which is the
    bulk reading a provider rate limits. The cost is that such a label offers
    less until its window is raised, and its held count says why.

    A RELEASE THE GATE IS ALREADY HOLDING IS ASKED BEFORE VERIFICATION, as a
    queued one is and for the same reason: its answer is local. It is judged
    again from the words its hold recorded, so a label whose kind changed
    files what now fits with no request made.

    EVERY HOLD IN FORCE ON THE LABEL IS JUDGED AGAIN, NOT ONLY THE ONES THE
    WINDOW REACHES. Newer releases push a held one past the window, and a hold
    nothing looks at again would stay counted as held under a reason that
    stopped being true when the label's kind changed. One the window does not
    reach and the gate would now pass is reported in ``stale`` and its hold is
    dropped. So is a hold on a release deleted on purpose since, and one on a
    release the library has come to own.

    EXCEPT A RELEASE THAT WAS TAKEN BACK OUT OF REVIEW (R-815). Dropping a
    hold past the window is safe for a release never filed: it becomes what
    any release past the window is, unexamined, and is judged when it is
    reached. A release ``label judge`` withheld WAS in front of a person, and
    dropped it would be in neither place with nothing said. Its hold stands,
    ``crate label held`` lists it, and ``return`` files it.
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
    #
    # A RELEASE ALREADY IN THE QUEUE IS ASKED BEFORE VERIFICATION, because it
    # was verified when it was filed and the answer is local. It takes a place
    # in the window, which is what keeps a later sweep from filing the next
    # slice of back catalogue every time (R-790).
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
            # DELETED ON PURPOSE OUTRANKS HELD. The release is not one the gate
            # is keeping out of review any more, so its hold goes.
            was = gate.standing(identity) if gate is not None else None
            if was is not None and was.state == review.HOLD_HELD:
                stale.append(identity)
            continue
        standing = gate.standing(identity) if gate is not None else None
        if identity in offered_ids:
            held += 1
            held_releases.append(release)
            # IN THE QUEUE AND STILL HELD is a state two writes can leave when
            # a process dies between them, and one a queue brought in from
            # another machine can make. The queue is the truth: the release is
            # in review, so its hold goes.
            if standing is not None and standing.state == review.HOLD_HELD:
                stale.append(identity)
            continue
        if standing is not None and standing.state == review.HOLD_RETURNED:
            # A PERSON RETURNED IT AND THE QUEUE DOES NOT HOLD IT, which a
            # queue moved between machines can produce. Filed, and never
            # judged: their answer outranks the catalogue's.
            candidates.append(_candidate(entry, release, genre_gate.returned_stamp()))
            continue
        if standing is not None:
            again = gate.rejudge(entry, standing)
            if again.held:
                gated.append(Gated(_candidate(entry, release), again, standing=True))
                held_releases.append(release)
            elif identity in owned_ids:
                # THE LIBRARY CAME TO OWN IT WHILE IT WAS HELD. Nothing to file
                # and nothing to hold, and like any owned release it takes no
                # place. Asked only of a hold being released, since the answer
                # is a provider read and a hold that stands does not need it.
                stale.append(identity)
            else:
                candidates.append(_candidate(entry, release, again.stamp()))
                released.append(identity)
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
        if gate is None:
            candidates.append(_candidate(entry, release))
            continue
        judged = gate.judge(entry, identity)
        if judged.held:
            gated.append(Gated(_candidate(entry, release), judged))
        else:
            candidates.append(_candidate(entry, release, judged.stamp()))
    # ONE HELD RELEASE IS RE-VERIFIED, AND ONLY WHEN THE SWEEP CONFIRMED NOTHING
    # IT ASKED ABOUT. It was confirmed when it was filed, so it is the one
    # release whose answer is known: confirmed again means the endpoint is up
    # and what failed really is unconfirmed, and unconfirmed means nothing this
    # sweep asked could have been confirmed. One provider call, on the path
    # where the worker is deciding whether to refuse. Which held release is
    # chosen by what the drops say and by each held release's own line
    # (U277), :func:`_canary_of`.
    held_unconfirmed = 0
    canary: Canary | None = None
    if held_releases and dropped and not candidates:
        chosen = _canary_of(held_releases, claimed, dropped)
        answered = label_verify.verify_release(claimed, chosen, search=verify)
        canary = Canary(
            identity=str(getattr(chosen, "id", "") or ""),
            artist=artist_name(chosen),
            title=_title_of(chosen),
            verdict=str(answered.get("verdict") or "unconfirmed"),
            notes=str(answered.get("notes") or ""),
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


#: The payload field naming the sweep run that filed a label release (R-790).
#: Spelled once, in the review module, because ``review list --group-by run``
#: reads the same field.
SWEEP_RUN = review.RUN_FIELD


def offer_release(
    store: review.ReviewStore,
    candidate: run.Candidate,
    *,
    handler_key: str = HANDLER_KEY,
    run_id: str | None = None,
) -> review.Item:
    """File one release, recording ``run_id`` as the sweep that filed it.

    THE FIRST RUN STAYS THE FILING RUN. ``review.offer`` rewrites an open
    item's payload on a re-offer, so an item already in the queue keeps the run
    it carries rather than taking the later one's, which would make an old
    release read as new in a grouping by run.
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
        gate: genre_gate.SweepGate | None = None,
        run_id: str | None = None,
        offered: Container[str] | None = None,
    ) -> None:
        self.cfg = cfg
        #: The genre gate every label's listing is judged by, or None to judge
        #: nothing (R-798). The worker builds one per item.
        self.gate = gate
        #: Identities that take a place in the offer window BESIDE the queued
        #: releases (U107): what the guided sync already asked a person about.
        #: None adds nothing, and the queue alone decides, as before.
        self.offered = offered
        #: The sweep run a hold made by this source is recorded under, so a
        #: grouping by run counts what each sweep held. The listing pass is
        #: handed no run by the increment, which is why it is taken here.
        self.run_id = run_id
        #: The standing holds the last pass released, dropped as each is filed.
        self._released: frozenset[str] = frozenset()
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
        #: EVERY LABEL THE LAST PASS LISTED, with its listing, rebuilt per pass
        #: on the rule ``dropped`` states. The worker records each label's
        #: ``beyond`` from here, since the increment's result carries only
        #: identities (R-790).
        self.listings: tuple[tuple[registry.LabelEntry, LabelListing], ...] = ()
        #: HELD RELEASES THE LAST PASS COULD NOT CONFIRM AGAIN, summed over its
        #: labels. See :attr:`LabelListing.held_unconfirmed`.
        self.held_unconfirmed = 0

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
        listings: list[tuple[registry.LabelEntry, LabelListing]] = []
        read = 0
        with self._queue() as store:
            offered = QueuedReleases(store, self.offered) if store is not None else None
            for entry in self.registry.labels.values():
                listing = list_for_label(
                    self.cfg,
                    entry,
                    artist=self._artist_for(entry),
                    verify=verify,
                    owned=self.owned,
                    offered=offered,
                    gate=self.gate,
                )
                if store is not None:
                    self._record_holds(store, entry, listing)
                found.extend(listing.candidates)
                discarded.extend(listing.dropped)
                unread.extend(listing.unread)
                listings.append((entry, listing))
                read += listing.listed
        self.dropped = tuple(discarded)
        self.unread = tuple(unread)
        self.listings = tuple(listings)
        self.held_unconfirmed = sum(listing.held_unconfirmed for _, listing in listings)
        self._released = frozenset(
            identity for _, listing in listings for identity in listing.released
        )
        self.read = read
        found.sort(key=lambda item: item.recency, reverse=True)
        return found[:n] if n >= 0 else found

    def _record_holds(
        self, store: review.ReviewStore, entry: registry.LabelEntry, listing: LabelListing
    ) -> None:
        """Record every release the gate held in this listing, as it was judged.

        WRITTEN WHEN THE LISTING IS MADE, not when the item succeeds. A hold is a
        judgment of one release and is true whatever happens to the rest of the
        sweep, the way an offer already made stays in the queue when a later
        one fails. A standing hold is written again too, which refreshes its
        reason and keeps the run that first held it. A hold the listing found
        stale is dropped here, for the same reason it is recorded here.
        """
        for identity in listing.stale:
            review.release_hold(
                store, queue=Queue.LABEL_RELEASE, item_id=genre_gate.release_item_id(identity)
            )
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
        """The open store when the worker handed one, else one for this pass.

        None over an empty registry, for the reason the verifier is resolved
        lazily in :meth:`list_recent`: a source with no label to list has no
        queue to ask, and opening one would create a review database for a
        pass that never needed it.
        """
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
        """Offer one release, then drop the hold it was released from, if any.

        THE OFFER FIRST. A hold dropped before its release was filed would be a
        release nothing holds and nothing offers if the offer then failed.
        """
        offer_release(store, candidate, run_id=run_id)
        if candidate.identity in self._released:
            review.release_hold(
                store,
                queue=Queue.LABEL_RELEASE,
                item_id=genre_gate.release_item_id(candidate.identity),
            )


@dataclass(frozen=True, slots=True)
class Confirmed:
    """A label's whole catalogue as the crawl and the verifier confirm it (R-835).

    ``releases`` is every confirmed release that no tombstone suppresses, newest
    first. ``listed`` is everything the crawl read, so the plan can say what it
    left out, and ``unread`` is what the crawl could not read, which a caller
    must not present as the whole label.
    """

    releases: tuple[Any, ...]
    listed: int
    dropped: tuple[Dropped, ...]
    suppressed: int
    unread: tuple[Unread, ...]
    #: The releases a tombstone suppressed, counted in ``suppressed``. Carried
    #: so a reader can judge their tracks (U243): a single is named for its one
    #: track, so the tombstone ``crate delete review`` writes for the track
    #: suppresses the release too, and its track would otherwise go unjudged.
    suppressed_releases: tuple[Any, ...] = ()


@dataclass(frozen=True, slots=True)
class Listed:
    """One label's catalogue as the crawl lists it, before anything is read per release.

    The first half of :func:`confirmed_releases` (U191): the roster and the
    paged listing, and no question asked about any one release. ``releases`` is
    everything the crawl read, in the listing's order, and ``unread`` is every
    listing it could not read, which a caller must not present as the whole
    label. ``claimed`` and ``verify`` are what the second half confirms with,
    built before the crawl so a missing verifier refuses before any call.
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
    """Every release the crawl lists for one label, and nothing read per release.

    What a full build counts before it decides whether to crawl (U191). A
    listing that could not be read raises ``run.LookupFailure``, and a
    ``CratekitError`` passes through unchanged, as :func:`confirmed_releases`
    says.
    """
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

    The tombstone first because it is local, then the verifier, since a roster
    artist's releases on another label are not this label's.
    """
    ordered = sorted(listed.releases, key=_year_of, reverse=True)
    tombstoned = _suppression_reader(cfg)
    confirmed: list[Any] = []
    dropped: list[Dropped] = []
    suppressed = 0
    held_back: list[Any] = []
    for release in ordered:
        if tombstoned(release):
            suppressed += 1
            held_back.append(release)
            continue
        verdict = label_verify.verify_release(listed.claimed, release, search=listed.verify)
        status = str(verdict.get("verdict") or "unconfirmed")
        if status != "confirmed":
            dropped.append(
                Dropped(
                    identity=str(getattr(release, "id", "") or ""),
                    reason=status,
                    notes=str(verdict.get("notes") or ""),
                )
            )
            continue
        confirmed.append(release)
    return Confirmed(
        releases=tuple(confirmed),
        listed=len(ordered),
        dropped=tuple(dropped),
        suppressed=suppressed,
        unread=listed.unread,
        suppressed_releases=tuple(held_back),
    )


def confirmed_releases(
    cfg: config.Config, entry: registry.LabelEntry, found: Catalogue
) -> Confirmed:
    """Every release of one label the catalogue confirms, with no window and no gate.

    THE SAME CRAWL :func:`list_for_label` READS, asked the same questions in the
    same order: the roster through :meth:`LabelSource._artist_for`, the listing
    through :func:`_crawl_or_refuse`, the tombstone first because it is local,
    then the verifier, since a roster artist's releases on another label are
    not this label's. What it leaves out is the review half: no offer window,
    no queue, no ownership and no genre gate, because a label's folder on the
    account mirrors its catalogue and not the library.

    Since U191 it is :func:`listed_releases` then :func:`confirm_listed`, so a
    full build can count the listing before it reads any release.

    A listing that could not be read raises ``run.LookupFailure`` here, as it
    does for the sweep, and a ``CratekitError`` passes through unchanged.
    """
    return confirm_listed(cfg, listed_releases(cfg, entry, found))


#: The year a release reads as, ``""`` when it carries none. Public for the
#: label folder's read (R-835), which groups a catalogue by it.
year_of = _year_of
