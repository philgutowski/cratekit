"""``acquire.bandcamp`` and ``acquire.bandcamp-fetch``: the account's purchases, into staging.

U176. Sitting 46 took 45 releases from one seller to download staging by hand:
a third party tool, a cookie pasted into a file, a name match on file paths
that read 49 of 102 releases as owned and missed a compilation track already in
the library, an ignore file kept by hand and a flatten with ``mv``. These two
verbs are that lane.

``crate acquire bandcamp [--seller NAME]...`` PLANS AND WRITES NOTHING. It lists
every purchase the account holds, newest first, each with its seller account
and one disposition:

* ``new``, nothing of it is in the library, so all of it is fetched;
* ``owned``, every track of it is, and the owned files are named;
* ``held``, some tracks are, those are named and held back, the rest fetched;
* ``not-downloadable``, a preorder, or a purchase with no digital download;
* ``hidden``, a purchase the account hid;
* ``filtered``, a seller ``--seller`` did not name;
* ``fetched``, an earlier run of this library took it.

``crate acquire bandcamp-fetch [--seller NAME]... [--batch NAME]`` plans the
same way, queues one job item per ``new`` or ``held`` purchase, and drives the
job here; ``--job JOB_ID`` continues one. The worker downloads each release in
the format the lossless policy calls for, checks every file against the library
again, moves the rest flat into ``<download_staging>/<batch>`` and records the
purchase as fetched.

OWNERSHIP IS THE PRODUCT'S MATCHER, per track. Each track of a release's list
is resolved with :func:`cratekit.acquire.match.resolve_one` over the library
view every other acquisition verb reads, never by a substring of a path. A
track the library holds, or one somebody deleted on purpose and left a
tombstone over, is held back. A track the matcher only has a question about is
not held: the library holds something else, and the landing is where a person
answers that. The files are checked a SECOND time after the download, by their
own tags, because a release's list and its files can spell a track two ways.

AN ABSENT LIBRARY IS NOT AN EMPTY ONE. Every track would resolve missing and
every purchase would read new, so the plan refuses when the music folder is not
there. AN ABSENT SESSION IS NOT AN EMPTY ACCOUNT EITHER: a missing, expired or
refused session is ``auth-failed`` naming the login step, never a plan of zero.
A RECORD THAT CANNOT BE READ IS NOT AN EMPTY RECORD: it refuses rather than
offering every purchase again.

THE RECORD IS BY PURCHASE AND NEVER A CHECKPOINT. A later run plans only the
purchases not yet fetched, and a purchase ``--seller`` filtered out today is
offered tomorrow, because nothing records it until it is fetched.

THE SESSION AND EVERY SIGNED LINK STAY OUT OF EVERYTHING THAT IS KEPT. The job
freezes what each purchase is, never the link it downloads from: the worker
lists the collection again for the link, holds it in this process only, and no
message, cause or file it writes names one. The session is read from the
keychain at the moment it is used and passed to the transport and nowhere else.

NOT GATED, for the reason ``acquire download`` and ``acquire fallback-fetch``
declare none: the verb ADDS files into download staging, replaces nothing and
publishes nothing. Nothing is written outside the batch folder, the holding
folder under staging that each release is emptied out of, and the record.
Never the music folder, never the database.

WHAT IT DOES NOT DO. The label is U177's, the genre U178's, the tagging, the
landing and the one command over all of it U179's. A purchase already recorded
is not fetched again here; a person who wants it again takes its entry out of
the record.
"""

from __future__ import annotations

import filecmp
import json
import re
import shutil
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

from cratekit.acquire import bandcamp, match, match_cli
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire.adapter import AdapterSettings, decide_lossless
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, secrets, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import landing

#: The plan verb's origin on every refusal it raises.
ORIGIN = ("acquire.bandcamp",)

#: The fetch verb's origin on every refusal it raises.
FETCH_ORIGIN = ("acquire.bandcamp-fetch",)

#: The ``origin`` a release's track carries into the matcher, as provenance.
SOURCE = "bandcamp"

#: The command a person records a session with. Named in every refusal that a
#: session would answer, because a refusal that does not say how to satisfy it
#: is a dead end.
LOGIN_STEP = (
    f"copy the Cookie request header your browser sends to bandcamp.com into a "
    f"file only you can read, then run: crate login "
    f"{secrets.Credential.BANDCAMP_SESSION} --from-file PATH"
)

#: The batch folder's name when ``--batch`` names none. A folder of its own
#: under download staging, so a landing of staging itself never sweeps it.
BATCH_PREFIX = "Bandcamp"

#: Payload keys. ``BATCH`` is the folder name under staging every item of the
#: job stages into. ``RELEASES`` is what each item IS, keyed by purchase id,
#: frozen at the queue so the worker reads nothing but the job and the account
#: (KTD9); it never holds a signed link.
BATCH = "batch"
RELEASES = "releases"

#: The record's format version.
RECORD_VERSION = 1


class Disposition(StrEnum):
    """What a plan does with one purchase. Stable slugs, read by a person and a tool."""

    NEW = "new"
    OWNED = "owned"
    HELD = "held"
    NOT_DOWNLOADABLE = "not-downloadable"
    HIDDEN = "hidden"
    FILTERED = "filtered"
    FETCHED = "fetched"


#: The dispositions a fetch takes a purchase for.
TO_FETCH = frozenset({Disposition.NEW, Disposition.HELD})


# ---------------------------------------------------------------------------
# The seams
# ---------------------------------------------------------------------------


def transport() -> bandcamp.Transport:
    """The transport a run uses, looked up on the module at call time.

    THE NETWORK SEAM. The suite replaces this function, so no test builds the
    shipped transport and no test reaches Bandcamp.
    """
    return bandcamp.CurlTransport()


def _auth_failed(message: str, *, origin: Sequence[str], remedy: Remedy) -> CratekitError:
    return refuse(
        "auth-failed",
        f"{message}, so the account's purchases could not be read",
        remedy=remedy,
        steps=(LOGIN_STEP,),
        origin=origin,
        detail={"credential": str(secrets.Credential.BANDCAMP_SESSION)},
    )


def session_cookie(origin: Sequence[str]) -> str:
    """The recorded Bandcamp session, or the refusal that names the login step.

    A MISSING SESSION IS ``auth-failed``, the code a refused one gets, because
    for the person both are the same act: sign in and record it. A keychain
    that cannot be reached is the store's own failure and keeps the remedy the
    store gave it, since telling that person to sign in again fixes nothing.
    """
    name = str(secrets.Credential.BANDCAMP_SESSION)
    try:
        return secrets.get(name)
    except secrets.CredentialMissing:
        raise _auth_failed(
            "no Bandcamp session is recorded",
            origin=origin,
            remedy=Remedy.AUTHENTICATE_PROVIDER,
        ) from None
    except secrets.CredentialError as exc:
        raise CratekitError(
            Cause(
                reason="credential-missing",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                scope=Scope.RUN,
                origin=tuple(origin),
                detail={"credential": name},
            )
        ) from None


def _rejected(exc: bandcamp.SessionRejected, origin: Sequence[str]) -> CratekitError:
    return _auth_failed(
        f"Bandcamp refused the recorded session ({exc})",
        origin=origin,
        remedy=Remedy.REAUTHENTICATE_PROVIDER,
    )


def _unavailable(exc: bandcamp.BandcampError, origin: Sequence[str], **detail: Any) -> CratekitError:
    return refuse(
        "unavailable-transient",
        f"Bandcamp could not be read ({exc}); nothing was planned or fetched",
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=origin,
        detail=detail,
    )


def collection(origin: Sequence[str], cookie: str | None = None) -> bandcamp.Collection:
    """The account's purchases, read through the seam with the recorded session."""
    if cookie is None:
        cookie = session_cookie(origin)
    try:
        return bandcamp.read_collection(transport(), cookie)
    except bandcamp.SessionRejected as exc:
        raise _rejected(exc, origin) from None
    except bandcamp.BandcampError as exc:
        raise _unavailable(exc, origin) from None


# ---------------------------------------------------------------------------
# The record of what this library fetched
# ---------------------------------------------------------------------------


def _record_unusable(path: Path, what: str) -> CratekitError:
    return refuse(
        "bandcamp-record-unusable",
        f"the record of the Bandcamp purchases this library fetched, {path.name}, "
        f"could not be read ({what}); read as empty it would fetch every purchase "
        f"again, so nothing was planned",
        steps=(f"repair or remove {path} and run it again",),
        origin=ORIGIN,
        detail={"path": str(path), "problem": what},
    )


def fetched(cfg: config.Config) -> dict[str, dict[str, Any]]:
    """Purchase id to what was recorded when it was fetched. Empty when none was."""
    path = config.state_path("bandcamp_fetched", cfg)
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise _record_unusable(path, f"it could not be opened: {exc.strerror}") from exc
    except ValueError as exc:
        raise _record_unusable(path, "it is not JSON") from exc
    if not isinstance(raw, Mapping):
        raise _record_unusable(path, f"the document is a {type(raw).__name__}, not a map")
    if raw.get("version") != RECORD_VERSION:
        raise _record_unusable(
            path, f"it says version {raw.get('version')!r} and this build reads {RECORD_VERSION}"
        )
    records = raw.get("purchases")
    if not isinstance(records, Mapping):
        raise _record_unusable(path, "it has no purchases map")
    return {str(key): dict(value) if isinstance(value, Mapping) else {} for key, value in records.items()}


def record_fetched(cfg: config.Config, item_id: str, entry: Mapping[str, Any]) -> None:
    """Add one purchase to the record, under its lock, read again inside it."""
    path = config.state_path("bandcamp_fetched", cfg)
    lock = config._exclusive_lock(config.state_path("bandcamp_fetched_lock", cfg))
    try:
        lock.__enter__()
    except config.ConfigLockUnavailable as exc:
        raise _record_unusable(path, f"it could not be locked: {exc}") from exc
    try:
        records = fetched(cfg)
        records[item_id] = dict(entry)
        payload = {"version": RECORD_VERSION, "purchases": dict(sorted(records.items()))}
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), path
        )
    finally:
        lock.__exit__(None, None, None)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Held:
    """One track of a purchase the library already holds, and where."""

    track: bandcamp.Track
    why: str
    paths: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {**self.track.to_json(), "why": self.why, "paths": list(self.paths)}


@dataclass(frozen=True, slots=True)
class Planned:
    """One purchase and what the plan does with it."""

    purchase: bandcamp.Purchase
    disposition: Disposition
    held: tuple[Held, ...] = ()

    def to_json(self) -> dict[str, Any]:
        kept_back = {one.track for one in self.held}
        return {
            **self.purchase.to_json(),
            "disposition": str(self.disposition),
            "held": [one.to_json() for one in self.held],
            "stage": [
                track.to_json() for track in self.purchase.tracks if track not in kept_back
            ]
            if self.disposition in TO_FETCH
            else [],
        }


#: ``Artist - Title`` in a track title, the shape a compilation's list takes
#: when the release names no artist per track.
_CREDITED = re.compile(r"^(?P<artist>.+?) - (?P<title>.+)$")


def track_wanted(track: bandcamp.Track, purchase: bandcamp.Purchase, position: int) -> match.Wanted | None:
    """The track as the matcher reads it, or None when it names too little.

    A track's own artist wins over the release's. A compilation that lists its
    tracks as ``Artist - Title`` under the release artist is read that way,
    which is the compilation track sitting 46's path match missed.
    """
    artist, title = track.artist, track.title
    if not artist:
        credited = _CREDITED.match(title)
        if credited:
            artist, title = credited["artist"].strip(), credited["title"].strip()
        else:
            artist = purchase.artist
    try:
        return match.read_row(
            {"artist": artist, "title": title, "id": f"{purchase.item_id}:{position}"},
            origin=SOURCE,
            position=position,
        )
    except match.UnreadableList:
        return None


def holding(found: match.TrackMatch) -> tuple[str, tuple[str, ...]] | None:
    """Why and where the library holds a resolved track, or None when it does not.

    Matched is held, with its paths. Suppressed is held too: a tombstone is a
    deliberate decision not to hold that recording, and fetching it would undo
    it. A question is NOT held, because the library holds something else.
    """
    if found.state is match.MatchState.MATCHED:
        return str(found.why), tuple(found.paths)
    if found.state is match.MatchState.SUPPRESSED:
        return str(found.why), ()
    return None


class Library:
    """The library as this verb asks it: one view, built once, asked per track."""

    def __init__(self, cfg: config.Config, origin: Sequence[str]) -> None:
        music = Path(cfg.library.root) / cfg.library.music_dir
        if not music.is_dir():
            raise refuse(
                "library-volume-unmounted",
                f"this library's music folder {str(music)!r} is not there, so no "
                f"purchase can be told from a release the library already holds",
                remedy=Remedy.MOUNT_LIBRARY_VOLUME,
                origin=origin,
                detail={"music": str(music)},
            )
        self.index, self.suppresses, self.identify = match_cli.library_view(cfg)

    def holds(self, wanted: match.Wanted) -> tuple[str, tuple[str, ...]] | None:
        found = match.resolve_one(
            wanted, self.index, suppresses=self.suppresses, suppression_id=self.identify
        )
        return holding(found)


def _sellers(named: Iterable[str] | None) -> frozenset[str]:
    return frozenset(name.strip().casefold() for name in (named or ()) if name.strip())


def plan(
    purchases: Sequence[bandcamp.Purchase],
    library: Library,
    *,
    sellers: frozenset[str],
    record: Mapping[str, Any],
) -> tuple[Planned, ...]:
    """Every purchase, in the order given, with its disposition.

    THE ORDER OF THE QUESTIONS is the order of what each one costs to ask: a
    hidden or filtered purchase is never matched, a recorded one never fetched
    again, and only a purchase that can be downloaded is asked of the library.
    """
    planned: list[Planned] = []
    for purchase in purchases:
        if purchase.hidden:
            planned.append(Planned(purchase, Disposition.HIDDEN))
            continue
        if sellers and purchase.seller.casefold() not in sellers:
            planned.append(Planned(purchase, Disposition.FILTERED))
            continue
        if purchase.item_id in record:
            planned.append(Planned(purchase, Disposition.FETCHED))
            continue
        if not purchase.downloadable:
            planned.append(Planned(purchase, Disposition.NOT_DOWNLOADABLE))
            continue
        held: list[Held] = []
        for position, track in enumerate(purchase.tracks, start=1):
            wanted = track_wanted(track, purchase, position)
            said = library.holds(wanted) if wanted is not None else None
            if said is not None:
                held.append(Held(track, said[0], said[1]))
        if not held:
            disposition = Disposition.NEW
        elif len(held) == len(purchase.tracks):
            disposition = Disposition.OWNED
        else:
            disposition = Disposition.HELD
        planned.append(Planned(purchase, disposition, tuple(held)))
    return tuple(planned)


def _load() -> config.Config:
    return match_cli._load()


def _planned(
    cfg: config.Config, sellers: frozenset[str], origin: Sequence[str]
) -> tuple[bandcamp.Collection, tuple[Planned, ...], Library]:
    """The plan, with each question asked before the one that costs more.

    The session is asked of the keychain first, since that is local and a
    missing one would make the library walk wasted. The record and the library
    come next, so a refusal over either costs no request, and the account last.
    """
    cookie = session_cookie(origin)
    record = fetched(cfg)
    library = Library(cfg, origin)
    found = collection(origin, cookie)
    return found, plan(found.purchases, library, sellers=sellers, record=record), library


def _count(planned: Sequence[Planned]) -> dict[str, int]:
    counts = {str(disposition): 0 for disposition in Disposition}
    for one in planned:
        counts[str(one.disposition)] += 1
    return counts


def _unmatched_sellers(sellers: frozenset[str], purchases: Sequence[bandcamp.Purchase]) -> list[str]:
    known = {purchase.seller.casefold() for purchase in purchases}
    return sorted(name for name in sellers if name not in known)


def _seller_warnings(unmatched: Sequence[str]) -> tuple[dict[str, str], ...]:
    if not unmatched:
        return ()
    return (
        {
            "code": "bandcamp-seller-unmatched",
            "message": (
                f"no purchase in the account belongs to {', '.join(unmatched)}; a "
                f"seller is the account name in the address of its releases, as in "
                f"<name>.bandcamp.com"
            ),
        },
    )


# ---------------------------------------------------------------------------
# acquire.bandcamp: the plan
# ---------------------------------------------------------------------------


def _add_sellers(parser) -> None:
    parser.add_argument(
        "--seller",
        action="append",
        default=None,
        metavar="NAME",
        help=(
            "only this seller's purchases, by the account name in its address "
            "(NAME.bandcamp.com); repeat it for several"
        ),
    )


def build(parser, entry) -> None:
    del entry
    _add_sellers(parser)
    parser.set_defaults(_handler=acquire_bandcamp)


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"acquire.bandcamp.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _named(planned: Sequence[Planned]) -> str:
    return "; ".join(
        f"{one.purchase.artist} - {one.purchase.title} ({one.purchase.seller})" for one in planned
    )


def fetch_command(sellers: frozenset[str]) -> str:
    return " ".join(
        ["crate acquire bandcamp-fetch", *(f"--seller {name}" for name in sorted(sellers))]
    )


def acquire_bandcamp(ctx) -> Envelope:
    """List every purchase with its disposition. Writes nothing."""
    cfg = _load()
    sellers = _sellers(ctx.args.seller)
    found, planned, _library = _planned(cfg, sellers, ORIGIN)
    counts = _count(planned)
    to_fetch = [one for one in planned if one.disposition in TO_FETCH]
    checks = [
        _check(
            str(disposition),
            "info",
            f"{counts[str(disposition)]} purchase(s) {disposition}"
            + (
                ": " + _named([one for one in planned if one.disposition is disposition])
                if disposition in (*TO_FETCH, Disposition.OWNED)
                and counts[str(disposition)]
                else ""
            ),
        )
        for disposition in Disposition
    ]
    unmatched = _unmatched_sellers(sellers, found.purchases)
    summary = {
        "purchases": len(planned),
        **counts,
        "sellers": sorted(sellers),
        "sellers_unmatched": unmatched,
        "fetch_next": fetch_command(sellers) if to_fetch else None,
        "rows": [one.to_json() for one in planned],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if to_fetch else Outcome.NO_OP,
        warnings=_seller_warnings(unmatched),
    )


# ---------------------------------------------------------------------------
# acquire.bandcamp-fetch: the job
# ---------------------------------------------------------------------------


def build_fetch(parser, entry) -> None:
    del entry
    _add_sellers(parser)
    parser.add_argument(
        "--batch",
        default=None,
        metavar="NAME",
        help=(
            "the folder under download staging to stage into; "
            f"'{BATCH_PREFIX} <today's date>' when omitted"
        ),
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the fetch already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_bandcamp_fetch)


def fetch_argv(job) -> list[str]:
    """The command line that continues one queued fetch. No ``--run``: no gate."""
    return ["acquire", "bandcamp-fetch", "--job", job.job_id]


def _reported(store, job) -> dict[str, Any]:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def frozen_release(planned: Planned) -> dict[str, Any]:
    """What one job item IS. Everything the worker needs but the signed link."""
    purchase = planned.purchase
    return {
        "seller": purchase.seller,
        "artist": purchase.artist,
        "title": purchase.title,
        "item_type": purchase.item_type,
        "tracks": [track.to_json() for track in purchase.tracks],
        "held": [one.to_json() for one in planned.held],
    }


#: Signed download pages, by job and purchase, held in this process only. The
#: queue path seeds it from the listing it planned with, so the drive that
#: follows in the same process asks the account nothing more; a resume in a new
#: process lists the account once and fills it.
_LINKS: dict[str, dict[str, str]] = {}

#: The library each job's worker checks files against, built once per job.
_LIBRARIES: dict[str, Library] = {}


def forget() -> None:
    """Drop what this process holds for running jobs. For the suite, and a resume."""
    _LINKS.clear()
    _LIBRARIES.clear()


def _batch_name(given: str | None) -> str:
    name = given if given is not None else f"{BATCH_PREFIX} {date.today().isoformat()}"
    if not landing.plain_name(name):
        raise refuse(
            "intake-list-unusable",
            f"{name!r} is not a folder name a batch can be staged under, because it "
            f"is empty, starts with a dot, has space at either end or holds a slash",
            steps=("pass --batch a plain folder name",),
            origin=FETCH_ORIGIN,
            detail={"batch": name},
        )
    return name


def acquire_bandcamp_fetch(ctx) -> Envelope:
    """Queue one item per purchase to fetch and drive the job, or drive one queued.

    THE STAGING SWEEP RUNS ON BOTH PATHS, for the reason ``acquire
    fallback-fetch`` gives: this verb's holding folders live in the tree
    ``acquire download`` sweeps, and a person who works only this lane would
    otherwise grow that tree without bound.
    """
    if ctx.args.job is not None:
        if not ctx.args.job.strip():
            raise refuse(
                "intake-list-unusable",
                "--job was given an empty identifier, so it names no job to continue",
                steps=("pass the identifier of the fetch already queued",),
                origin=FETCH_ORIGIN,
            )
        with jobs.open_store() as store:
            job = jobs.reconcile(store, ctx.args.job)
            acquire_cli.sweep_staging(
                Path(jobs.frozen_config(job).paths.download_staging), store
            )
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
            jobs.raise_for_state(job)
            return ctx.envelope(data=_reported(store, job), warnings=warnings)
    cfg = _load()
    batch = _batch_name(ctx.args.batch)
    sellers = _sellers(ctx.args.seller)
    found, planned, library = _planned(cfg, sellers, FETCH_ORIGIN)
    warnings = _seller_warnings(_unmatched_sellers(sellers, found.purchases))
    releases = {
        one.purchase.item_id: frozen_release(one) for one in planned if one.disposition in TO_FETCH
    }
    if not releases:
        return ctx.envelope(
            data={"job_id": "", "state": "nothing-new", "cause": None, "progress": {}},
            outcome=Outcome.NO_OP,
            warnings=warnings,
        )
    with jobs.open_store() as store:
        acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={BATCH: batch, RELEASES: releases},
            cfg=cfg,
            item_ids=tuple(releases),
        )
        _LINKS[job.job_id] = {
            purchase.item_id: purchase.download_page
            for purchase in found.purchases
            if purchase.item_id in releases
        }
        _LIBRARIES[job.job_id] = library
        _, drift = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
        jobs.raise_for_state(job)
        return ctx.envelope(data=_reported(store, job), warnings=(*warnings, *drift))


# ---------------------------------------------------------------------------
# The worker
# ---------------------------------------------------------------------------


def _parked(cause: Cause) -> jobs.Parked:
    """A park: a fact about the session or the machine, never about one release."""
    return jobs.Parked(cause)


def _links_for(job_id: str) -> dict[str, str]:
    known = _LINKS.get(job_id)
    if known is not None:
        return known
    try:
        listed = collection(FETCH_ORIGIN)
    except CratekitError as exc:
        # PARKED WHATEVER THE REASON. The listing is the account's, not one
        # release's: a refused session and an outage both meet every later
        # item the same way, and failing each one in turn would spend a
        # listing per item and strand the job failed rather than resumable.
        raise _parked(exc.cause) from None
    known = {purchase.item_id: purchase.download_page for purchase in listed.purchases}
    _LINKS[job_id] = known
    return known


def _library_for(job_id: str, cfg: config.Config) -> Library:
    known = _LIBRARIES.get(job_id)
    if known is None:
        try:
            known = Library(cfg, FETCH_ORIGIN)
        except CratekitError as exc:
            # An unmounted volume is a fact about the machine, so every later
            # item would fail the same way: parked, not failed.
            raise _parked(exc.cause) from None
        _LIBRARIES[job_id] = known
    return known


#: ``NN`` at the front of what follows ``Artist - Album - `` in a file's name.
_NUMBERED = re.compile(r"(?P<number>\d{1,3}) ")


def number_in(name: str, artist: str, title: str) -> int | None:
    """The track number in a release's file name, ``Artist - Album - NN Title``.

    READ AFTER THE PREFIX THE RELEASE IS KNOWN BY, never as the first `` - NN ``
    in the name: an album titled ``2 Step Anthems`` puts a number there that
    is not a track's, and holding by it held every file of the release. A name
    that does not begin with the release's own artist and title gives no
    number, and only the file's tags can hold it back.
    """
    prefix = f"{artist} - {title} - "
    if not artist or not title or not name.startswith(prefix):
        return None
    found = _NUMBERED.match(name[len(prefix):])
    return int(found["number"]) if found else None


def file_holding(path: Path, library: Library, artist: str) -> tuple[str, tuple[str, ...]] | None:
    """Whether the library holds the track one downloaded file carries, by its tags."""
    read = tags.read_tags(path, ("artist", "title"))
    title = str(read["title"] or "").strip()
    if not title:
        return None
    try:
        wanted = match.read_row(
            {"artist": str(read["artist"] or "").strip() or artist, "title": title},
            origin=SOURCE,
            position=1,
        )
    except match.UnreadableList:
        return None
    return library.holds(wanted)


def _encoding(cfg: config.Config, offers: Mapping[str, str], detail: dict[str, Any]) -> tuple[str, bool]:
    """The format to fetch and whether it is lossy, by the frozen policy."""
    for encoding in bandcamp.LOSSLESS_ENCODINGS:
        if encoding in offers:
            return encoding, False
    policy = AdapterSettings.from_config(cfg).lossless_policy
    decision = decide_lossless(policy, source_is_lossless=False)
    offered = sorted(offers)
    if not decision.permitted:
        raise refuse(
            "lossy-refused",
            f"{detail['artist']} - {detail['title']} is offered in no lossless format "
            f"(offered: {', '.join(offered) or 'nothing'}), and the strict lossless "
            f"policy refuses a lossy file, so nothing was downloaded",
            remedy=decision.remedy or Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail={**detail, "offered": offered},
        )
    if bandcamp.LOSSY_ENCODING not in offers:
        raise refuse(
            "unavailable-permanent",
            f"{detail['artist']} - {detail['title']} is offered in no lossless "
            f"format and not as {bandcamp.LOSSY_ENCODING} "
            f"(offered: {', '.join(offered) or 'nothing'}), so nothing was downloaded",
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail={**detail, "offered": offered},
        )
    return bandcamp.LOSSY_ENCODING, True


def _item_failure(exc: bandcamp.BandcampError, detail: dict[str, Any]) -> CratekitError:
    if isinstance(exc, bandcamp.SessionRejected):
        return _parked(_rejected(exc, FETCH_ORIGIN).cause)
    return refuse(
        "unavailable-transient",
        f"{detail['artist']} - {detail['title']} could not be fetched ({exc}); it "
        f"stays queued",
        remedy=Remedy.RETRY_LATER,
        scope=Scope.ITEM,
        retryable=True,
        origin=FETCH_ORIGIN,
        detail=detail,
    )


def _empty_holding(holding_dir: Path, *, keep: Iterable[Path]) -> None:
    """Empty a release's holding folder, but for the copies a collision refused.

    A refused copy IS KEPT, because it is the only copy of a track the person
    paid for that this run has, and the refusal tells them to compare it with
    the file already in the batch. Everything else, the archive's cover and
    whatever the release held back, goes.
    """
    kept = {path.resolve() for path in keep}
    if not kept:
        shutil.rmtree(holding_dir, ignore_errors=True)
        return
    for leftover in sorted(holding_dir.rglob("*"), reverse=True):
        if leftover.is_file() and leftover.resolve() not in kept:
            leftover.unlink()
        elif leftover.is_dir():
            try:
                leftover.rmdir()
            except OSError:
                continue


def handle_fetch(job, item, cfg) -> jobs.Produced:
    """Fetch ONE purchase into the batch folder, the library's tracks held back.

    The order is the order of what each step can cost:

    * a purchase the record already holds is done, so a resume after a crash
      between the record and the item's completion fetches nothing twice;
    * the session, the link and the library are asked for before anything
      downloads, and a refusal of the session or an unmounted volume PARKS the
      job, since every later item would meet the same;
    * the format is chosen by the frozen policy before the download, FLAC
      whenever it is offered, a lossy file only when no lossless one is and the
      policy permits it, and then marked;
    * every file is checked against the policy by ``checked_landing``, the one
      place every acquisition's file passes, and against the library again by
      its own tags and by the track numbers the plan held;
    * a name already in the batch folder is refused for that file alone, after
      the rest are moved, unless the file there holds the same bytes; the
      refusal names it and the downloaded copy is kept where it names;
    * a file is marked lossy by what it IS, not only by the format offered;
    * the holding folder is emptied of all but a refused copy and the purchase
      recorded whatever was refused, since the release itself was taken.
    """
    said = dict(((job.payload or {}).get(RELEASES) or {}).get(item.item_id) or {})
    batch = str((job.payload or {}).get(BATCH) or "")
    detail: dict[str, Any] = {
        "item_id": item.item_id,
        "seller": str(said.get("seller") or ""),
        "artist": str(said.get("artist") or ""),
        "title": str(said.get("title") or ""),
    }
    if not landing.plain_name(batch):
        raise refuse(
            "internal-error",
            f"job {job.job_id} froze no batch folder a release can stage into",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    if item.item_id in fetched(cfg):
        return jobs.Produced()
    try:
        cookie = session_cookie(FETCH_ORIGIN)
    except CratekitError as exc:
        raise _parked(exc.cause) from None
    page = _links_for(job.job_id).get(item.item_id) or ""
    if not page:
        raise refuse(
            "unavailable-permanent",
            f"{detail['artist']} - {detail['title']} is no longer a purchase the "
            f"account can download, so nothing was fetched",
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    library = _library_for(job.job_id, cfg)
    client = transport()
    try:
        offers = bandcamp.download_offers(client, cookie, page)
    except bandcamp.BandcampError as exc:
        raise _item_failure(exc, detail) from None
    encoding, lossy = _encoding(cfg, offers, detail)
    root = Path(cfg.paths.download_staging)
    holding_dir = acquire_cli.staging_dir(root, job.job_id, item.ordinal)
    try:
        landed = bandcamp.fetch(client, cookie, offers[encoding], holding_dir)
        files = bandcamp.unpack(landed, holding_dir / "release")
    except bandcamp.BandcampError as exc:
        raise _item_failure(exc, detail) from None
    if not files:
        raise refuse(
            "unavailable-transient",
            f"{detail['artist']} - {detail['title']} arrived with no audio file in it; "
            f"it stays queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    policy = AdapterSettings.from_config(cfg).lossless_policy
    checked = [acquire_cli.checked_landing(path, item.item_id, policy=policy) for path in files]
    held_numbers = {
        number
        for one in said.get("held") or ()
        if isinstance(one, Mapping) and (number := one.get("number")) is not None
    }
    marker = cfg.naming.lossy_marker or ""
    target = root / batch
    config._mkdir_private(target)
    staged: list[str] = []
    held: list[str] = []
    refused: dict[str, Path] = {}
    for path in checked:
        number = number_in(path.name, detail["artist"], detail["title"])
        if (number is not None and number in held_numbers) or file_holding(
            path, library, detail["artist"]
        ):
            held.append(path.name)
            continue
        marked = lossy or acquire_cli.lossy_landing(path, policy=policy)
        final = target / acquire_cli.marked_name(path, marker, required=marked)
        if final.exists():
            if final.is_file() and filecmp.cmp(path, final, shallow=False):
                # THE SAME BYTES ARE ALREADY THERE, which is what a resume after
                # a kill between these moves and the record finds. Staged, not
                # refused: nothing differs for a person to choose between.
                staged.append(final.name)
                path.unlink()
                continue
            refused[final.name] = path
            continue
        path.replace(final)
        staged.append(final.name)
    _empty_holding(holding_dir, keep=refused.values())
    record_fetched(
        cfg,
        item.item_id,
        {
            **{key: detail[key] for key in ("seller", "artist", "title")},
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "job_id": job.job_id,
            "batch": batch,
            "encoding": encoding,
            "staged": staged,
            "held": held,
            "refused": sorted(refused),
            "kept": {name: str(path) for name, path in sorted(refused.items())},
        },
    )
    if refused:
        raise refuse(
            "output-exists",
            f"{len(refused)} file(s) of {detail['artist']} - {detail['title']} were "
            f"already in {target} with different contents and were not put in their "
            f"place: {'; '.join(sorted(refused))}. The downloaded copies are kept at "
            f"{'; '.join(str(path) for _name, path in sorted(refused.items()))}. The "
            f"other {len(staged)} file(s) were staged and the purchase is recorded as "
            f"fetched",
            steps=(
                "compare each downloaded copy named with the file of the same name in "
                "the batch folder, and move the one you want into the batch folder",
            ),
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail={
                **detail,
                "batch": str(target),
                "refused": sorted(refused),
                "kept": [str(path) for _name, path in sorted(refused.items())],
                "staged": staged,
            },
        )
    return jobs.Produced()


__all__ = [
    "BATCH",
    "BATCH_PREFIX",
    "Disposition",
    "FETCH_ORIGIN",
    "Held",
    "LOGIN_STEP",
    "Library",
    "ORIGIN",
    "Planned",
    "RECORD_VERSION",
    "RELEASES",
    "SOURCE",
    "TO_FETCH",
    "acquire_bandcamp",
    "acquire_bandcamp_fetch",
    "build",
    "build_fetch",
    "collection",
    "fetch_argv",
    "fetch_command",
    "fetched",
    "file_holding",
    "forget",
    "frozen_release",
    "handle_fetch",
    "holding",
    "plan",
    "record_fetched",
    "session_cookie",
    "track_wanted",
    "transport",
]
