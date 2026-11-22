"""``acquire.bandcamp`` and ``acquire.bandcamp-fetch``: the account's purchases, into staging.

``crate acquire bandcamp`` plans and writes nothing: every purchase, newest first,
with its seller, label and :class:`Disposition`. ``bandcamp-fetch`` queues one job
item per ``new`` or ``held`` purchase and drives it; the worker fetches each
release by the lossless policy and stages the files the library lacks flat into
``<download_staging>/<batch>`` (U176). Not gated: it only adds files there.

Ownership is the product's matcher per track, checked again by each file's tags
after download. A missing library, session, record or label registry refuses
rather than reading as empty. The record is by purchase and never a checkpoint.
The session and every signed link stay out of the job, every message and file.

A registered label names its seller account (U177), and its files are staged with
its name in the ``label`` tag, which ``crate intake land --label-from-tags`` files
by; an unregistered seller's files stay untagged.
"""

from __future__ import annotations

import filecmp
import json
import re
import shlex
import shutil
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import bandcamp, match, match_cli
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire.adapter import AdapterSettings, decide_lossless
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, secrets, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import landing

if TYPE_CHECKING:
    from cratekit.label import registry as labels

#: The plan verb's origin on every refusal it raises.
ORIGIN = ("acquire.bandcamp",)

#: The fetch verb's origin on every refusal it raises.
FETCH_ORIGIN = ("acquire.bandcamp-fetch",)

#: The ``origin`` a release's track carries into the matcher, as provenance.
SOURCE = "bandcamp"

#: The command that records a session, named in every refusal a session answers.
LOGIN_STEP = (
    f"copy the Cookie request header your browser sends to bandcamp.com into a "
    f"file only you can read, then run: crate login "
    f"{secrets.Credential.BANDCAMP_SESSION} --from-file PATH"
)

#: The default batch folder, its own under staging so a landing of staging skips it.
BATCH_PREFIX = "Bandcamp"

#: Payload keys: the batch folder, and each purchase frozen at the queue, never its link (KTD9).
BATCH = "batch"
RELEASES = "releases"

#: The record's format version.
RECORD_VERSION = 1

#: An item's refusal when a file would not take its label tag; it is staged anyway (U177).
LABEL_UNWRITTEN = "bandcamp-label-unwritten"

#: The plan's warning per seller to fetch from that no registered label names.
SELLER_UNREGISTERED = "bandcamp-seller-unregistered"

#: The ``crate intake land`` flag that files each file under its own label tag.
LAND_FLAG = "--label-from-tags"

#: The fetch's warning naming that landing; ``job_state/1`` has no field for it.
LAND_BY_LABEL = "bandcamp-land-by-label"


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


def transport() -> bandcamp.Transport:
    """The transport a run uses, looked up at call time so the suite replaces it."""
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
    """The recorded session; missing is ``auth-failed``, while an unreachable keychain
    keeps the store's own remedy, since signing in again fixes nothing."""
    name = str(secrets.Credential.BANDCAMP_SESSION)
    try:
        return secrets.get(name)
    except secrets.CredentialMissing:
        raise _auth_failed(
            "no Bandcamp session is recorded", origin=origin, remedy=Remedy.AUTHENTICATE_PROVIDER,
        ) from None
    except secrets.CredentialError as exc:
        raise CratekitError(
            Cause(
                reason="credential-missing", message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))), scope=Scope.RUN,
                origin=tuple(origin), detail={"credential": name},
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
        remedy=Remedy.RETRY_LATER, retryable=True, origin=origin, detail=detail,
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


def _record_unusable(path: Path, what: str) -> CratekitError:
    return refuse(
        "bandcamp-record-unusable",
        f"the record of the Bandcamp purchases this library fetched, {path.name}, "
        f"could not be read ({what}); read as empty it would fetch every purchase "
        f"again, so nothing was planned",
        steps=(f"repair or remove {path} and run it again",), origin=ORIGIN,
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
    lock = config.exclusive_lock(config.state_path("bandcamp_fetched_lock", cfg))
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
    #: The registered label the purchase's seller names, or None (U177).
    label: labels.LabelEntry | None = None

    def to_json(self) -> dict[str, Any]:
        kept_back = {one.track for one in self.held}
        return {
            **self.purchase.to_json(), "label": self.label.name if self.label is not None else None,
            "label_id": self.label.label_id if self.label is not None else None,
            "disposition": str(self.disposition), "held": [one.to_json() for one in self.held],
            "stage": [
                track.to_json() for track in self.purchase.tracks if track not in kept_back
            ]
            if self.disposition in TO_FETCH
            else [],
        }


#: ``Artist - Title`` in a track title, a compilation's list naming no artist per track.
_CREDITED = re.compile(r"^(?P<artist>.+?) - (?P<title>.+)$")


def track_wanted(track: bandcamp.Track, purchase: bandcamp.Purchase, position: int) -> match.Wanted | None:
    """The track as the matcher reads it, or None; ``Artist - Title`` is split."""
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
            origin=SOURCE, position=position,
        )
    except match.UnreadableList:
        return None


def holding(found: match.TrackMatch) -> tuple[str, tuple[str, ...]] | None:
    """Why and where the library holds a track: matched, or suppressed since a tombstone
    is deliberate. A question is not held."""
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
                remedy=Remedy.MOUNT_LIBRARY_VOLUME, origin=origin, detail={"music": str(music)},
            )
        self.index, self.suppresses, self.identify = match_cli.library_view(cfg)

    def holds(self, wanted: match.Wanted) -> tuple[str, tuple[str, ...]] | None:
        found = match.resolve_one(
            wanted, self.index, suppresses=self.suppresses, suppression_id=self.identify
        )
        return holding(found)


def registry(origin: Sequence[str]) -> labels.Registry:
    """The label registry; unreadable refuses rather than stage every purchase untagged."""
    from cratekit.label import registry as labels

    del origin
    return labels.RegistryStore().load()


def _sellers(named: Iterable[str] | None, held: labels.Registry) -> frozenset[str]:
    """The accounts ``--seller`` names; a registered label's name reads as its account."""
    found: set[str] = set()
    for raw in named or ():
        name = raw.strip()
        if not name:
            continue
        entry = held.resolve(name)
        found.add(entry.bandcamp if entry is not None and entry.bandcamp else name.casefold())
    return frozenset(found)


def plan(
    purchases: Sequence[bandcamp.Purchase], library: Library, *, sellers: frozenset[str],
    record: Mapping[str, Any], registered: labels.Registry | None = None,
) -> tuple[Planned, ...]:
    """Every purchase with its disposition and label, the cheapest question first."""
    from cratekit.label import registry as labels

    known = registered if registered is not None else labels.empty()
    planned: list[Planned] = []
    for purchase in purchases:
        label = known.by_bandcamp(purchase.seller) if purchase.seller else None
        if purchase.hidden:
            planned.append(Planned(purchase, Disposition.HIDDEN, label=label))
            continue
        if sellers and purchase.seller.casefold() not in sellers:
            planned.append(Planned(purchase, Disposition.FILTERED, label=label))
            continue
        if purchase.item_id in record:
            planned.append(Planned(purchase, Disposition.FETCHED, label=label))
            continue
        if not purchase.downloadable:
            planned.append(Planned(purchase, Disposition.NOT_DOWNLOADABLE, label=label))
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
        planned.append(Planned(purchase, disposition, tuple(held), label=label))
    return tuple(planned)


@dataclass(frozen=True, slots=True)
class Asked:
    """What one plan asked and was answered: the account, the plan, and what it read."""

    found: bandcamp.Collection
    planned: tuple[Planned, ...]
    library: Library
    held: labels.Registry
    sellers: frozenset[str]


def _planned(cfg: config.Config, named: Iterable[str] | None, origin: Sequence[str]) -> Asked:
    """The plan, local questions before the account, so a refusal costs no request."""
    cookie = session_cookie(origin)
    record = fetched(cfg)
    held = registry(origin)
    sellers = _sellers(named, held)
    library = Library(cfg, origin)
    found = collection(origin, cookie)
    planned = plan(found.purchases, library, sellers=sellers, record=record, registered=held)
    return Asked(found=found, planned=planned, library=library, held=held, sellers=sellers)


def _count(planned: Sequence[Planned]) -> dict[str, int]:
    counts = {str(disposition): 0 for disposition in Disposition}
    for one in planned:
        counts[str(one.disposition)] += 1
    return counts


def _unmatched_sellers(sellers: frozenset[str], purchases: Sequence[bandcamp.Purchase]) -> list[str]:
    known = {purchase.seller.casefold() for purchase in purchases}
    return sorted(name for name in sellers if name not in known)


def _seller_warnings(
    unmatched: Sequence[str], held: labels.Registry | None = None
) -> tuple[dict[str, str], ...]:
    if not unmatched:
        return ()
    from cratekit.label import registry as labels

    known = held if held is not None else labels.empty()
    # A followed label with no account is said as that: the cure is to give it one.
    accountless = [
        entry.name
        for name in unmatched
        if (entry := known.resolve(name)) is not None and not entry.bandcamp
    ]
    return (
        {
            "code": "bandcamp-seller-unmatched",
            "message": (
                f"no purchase in the account belongs to {', '.join(unmatched)}; a "
                f"seller is the account name in the address of its releases, as in "
                f"<name>.bandcamp.com"
                + (
                    f", or a followed label that names one; {', '.join(accountless)} "
                    f"names none, and crate label registry set <label> --bandcamp "
                    f"<account> gives it one"
                    if accountless
                    else ""
                )
            ),
        },
    )


def register_command(seller: str) -> str:
    """The command that makes ``seller``'s purchases a label's (U177)."""
    return f"crate label registry add <label name> --bandcamp {seller}"


def unregistered(planned: Sequence[Planned], held: labels.Registry) -> list[str]:
    """Every seller with a purchase to fetch whose label the registry does not name, sorted."""
    return sorted(
        {
            one.purchase.seller
            for one in planned
            if one.disposition in TO_FETCH and one.label is None and one.purchase.seller
        }
    )


def _registration_warnings(
    sellers: Sequence[str], held: labels.Registry
) -> tuple[dict[str, str], ...]:
    """One warning per unregistered seller, naming how to register it, or why two labels tie."""
    from cratekit.label import registry as labels

    warned: list[dict[str, str]] = []
    for seller in sellers:
        tied = held.claimants(seller)
        if len(tied) > 1:
            message = (
                f"{seller} is named as the Bandcamp account of {len(tied)} labels, "
                f"{', '.join(entry.name for entry in tied)}, so its purchases are "
                f"staged with no label tag; clear it on all but one with crate label "
                f"registry set <label> --bandcamp {labels.CLEAR_BANDCAMP}"
            )
        else:
            message = (
                f"{seller} is the seller of purchases to fetch and no followed label "
                f"names it, so its files are staged as they came, with no label tag "
                f"written; to file them under their label, run "
                f"{register_command(seller)}, or set --bandcamp {seller} on a label "
                f"already followed"
            )
        warned.append({"code": SELLER_UNREGISTERED, "message": message})
    return tuple(warned)


def labels_of(planned: Sequence[Planned]) -> dict[str, str]:
    """Each seller with a purchase to fetch and the label it is staged under, sorted."""
    return {
        one.purchase.seller: one.label.name
        for one in sorted(planned, key=lambda one: one.purchase.seller)
        if one.disposition in TO_FETCH and one.label is not None
    }


def _add_sellers(parser) -> None:
    parser.add_argument(
        "--seller", action="append", default=None, metavar="NAME",
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
    cfg = match_cli._load()
    asked = _planned(cfg, ctx.args.seller, ORIGIN)
    found, planned, sellers = asked.found, asked.planned, asked.sellers
    counts = _count(planned)
    to_fetch = [one for one in planned if one.disposition in TO_FETCH]
    checks = [
        _check(
            str(disposition), "info",
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
    unlabelled = unregistered(planned, asked.held)
    staged_under = labels_of(planned)
    checks.append(
        _check(
            "labels", "info" if not unlabelled else "warn",
            (
                "staged under their label: "
                + "; ".join(f"{seller} as {name}" for seller, name in staged_under.items())
                if staged_under
                else "no seller with a purchase to fetch is a followed label's"
            )
            + (
                f"; no label names {', '.join(unlabelled)}, register with "
                f"{register_command(unlabelled[0])}"
                if unlabelled
                else ""
            ),
        )
    )
    summary = {
        "purchases": len(planned), **counts, "sellers": sorted(sellers),
        "sellers_unmatched": unmatched, "labels": staged_under, "sellers_unregistered": unlabelled,
        "fetch_next": fetch_command(sellers) if to_fetch else None,
        "rows": [one.to_json() for one in planned],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if to_fetch else Outcome.NO_OP,
        warnings=(
            *_seller_warnings(unmatched, asked.held),
            *_registration_warnings(unlabelled, asked.held),
        ),
    )


def build_fetch(parser, entry) -> None:
    del entry
    _add_sellers(parser)
    parser.add_argument(
        "--batch", default=None, metavar="NAME",
        help=(
            "the folder under download staging to stage into; "
            f"'{BATCH_PREFIX} <today's date>' when omitted"
        ),
    )
    parser.add_argument(
        "--job", default=None, metavar="JOB_ID",
        help="continue the fetch already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_bandcamp_fetch)


def fetch_argv(job) -> list[str]:
    """The command line that continues one queued fetch. No ``--run``: no gate."""
    return ["acquire", "bandcamp-fetch", "--job", job.job_id]


def land_command(job) -> str | None:
    """The landing that files the batch by label tag, or None when no release was a label's."""
    payload = job.payload or {}
    releases = payload.get(RELEASES) or {}
    if not any(isinstance(one, Mapping) and one.get("label") for one in releases.values()):
        return None
    folder = Path(jobs.frozen_config(job).paths.download_staging) / str(payload.get(BATCH) or "")
    # Shell quoting, since the batch folder holds a space.
    return shlex.join(["crate", "intake", "land", str(folder), LAND_FLAG])


def _land_warnings(job) -> tuple[dict[str, str], ...]:
    """The warning naming the landing by label; a field would break ``job_state/1``."""
    command = land_command(job)
    if command is None:
        return ()
    releases = (job.payload or {}).get(RELEASES) or {}
    named = sorted(
        {str(one["label"]) for one in releases.values() if isinstance(one, Mapping) and one.get("label")}
    )
    return (
        {
            "code": LAND_BY_LABEL,
            "message": (
                f"the batch holds releases of {', '.join(named)}, each file tagged with "
                f"its label; land it filed under each file's label with {command}"
            ),
        },
    )


def frozen_release(planned: Planned) -> dict[str, Any]:
    """What one job item IS. Everything the worker needs but the signed link."""
    purchase = planned.purchase
    return {
        "seller": purchase.seller,
        # Frozen too (KTD9, U177), so a resume tags by what was registered then.
        "label": planned.label.name if planned.label is not None else None,
        "label_id": planned.label.label_id if planned.label is not None else None,
        "artist": purchase.artist,
        "title": purchase.title,
        "item_type": purchase.item_type,
        "tracks": [track.to_json() for track in purchase.tracks],
        "held": [one.to_json() for one in planned.held],
    }


#: Signed download pages by job and purchase, held in this process only.
_LINKS: dict[str, dict[str, str]] = {}

#: The library each job's worker checks files against, built once per job.
_LIBRARIES: dict[str, Library] = {}


def forget() -> None:
    """Drop what this process holds for running jobs. For the suite, and a resume."""
    _LINKS.clear()
    _LIBRARIES.clear()


def staging_batch(given: str | None) -> str:
    """The batch folder a fetch stages into under download staging: ``given``, or today's."""
    name = given if given is not None else f"{BATCH_PREFIX} {date.today().isoformat()}"
    if not landing.plain_name(name):
        raise refuse(
            "intake-list-unusable",
            f"{name!r} is not a folder name a batch can be staged under, because it "
            f"is empty, starts with a dot, has space at either end or holds a slash",
            steps=("pass --batch a plain folder name",), origin=FETCH_ORIGIN,
            detail={"batch": name},
        )
    return name


def acquire_bandcamp_fetch(ctx) -> Envelope:
    """Queue and drive the fetch, or drive one queued. Both paths sweep staging, which
    this lane's holding folders would otherwise grow without bound."""
    if ctx.args.job is not None:
        if not ctx.args.job.strip():
            raise refuse(
                "intake-list-unusable",
                "--job was given an empty identifier, so it names no job to continue",
                steps=("pass the identifier of the fetch already queued",), origin=FETCH_ORIGIN,
            )
        with jobs.open_store() as store:
            job = jobs.reconcile(store, ctx.args.job)
            acquire_cli.sweep_staging(Path(jobs.frozen_config(job).paths.download_staging), store)
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
            jobs.raise_for_state(job)
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(*warnings, *_land_warnings(job))
            )
    cfg = match_cli._load()
    batch = staging_batch(ctx.args.batch)
    asked = _planned(cfg, ctx.args.seller, FETCH_ORIGIN)
    found, planned, library = asked.found, asked.planned, asked.library
    warnings = (
        *_seller_warnings(_unmatched_sellers(asked.sellers, found.purchases), asked.held),
        *_registration_warnings(unregistered(planned, asked.held), asked.held),
    )
    releases = {
        one.purchase.item_id: frozen_release(one) for one in planned if one.disposition in TO_FETCH
    }
    if not releases:
        return ctx.envelope(
            data={"job_id": "", "state": "nothing-new", "cause": None, "progress": {}},
            outcome=Outcome.NO_OP, warnings=warnings,
        )
    with jobs.open_store() as store:
        acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)
        job = jobs.enqueue(
            store, handler_key=ctx.entry.handler_key, payload={BATCH: batch, RELEASES: releases},
            cfg=cfg, item_ids=tuple(releases),
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
        return ctx.envelope(
            data=jobs.reported(store, job), warnings=(*warnings, *drift, *_land_warnings(job))
        )


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
        # Parked whatever the reason: the listing is the account's, so every item fails alike.
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
            # An unmounted volume would fail every later item: parked, not failed.
            raise _parked(exc.cause) from None
        _LIBRARIES[job_id] = known
    return known


#: ``NN`` at the front of what follows ``Artist - Album - `` in a file's name.
_NUMBERED = re.compile(r"(?P<number>\d{1,3}) ")


def number_in(name: str, artist: str, title: str) -> int | None:
    """The track number after the release's own ``Artist - Album - `` prefix, never the
    first number in the name, which an album title can hold."""
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
            {"artist": str(read["artist"] or "").strip() or artist, "title": title}, origin=SOURCE,
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
            remedy=decision.remedy or Remedy.RELAX_LOSSLESS_POLICY, scope=Scope.ITEM,
            origin=FETCH_ORIGIN, detail={**detail, "offered": offered},
        )
    if bandcamp.LOSSY_ENCODING not in offers:
        raise refuse(
            "unavailable-permanent",
            f"{detail['artist']} - {detail['title']} is offered in no lossless "
            f"format and not as {bandcamp.LOSSY_ENCODING} "
            f"(offered: {', '.join(offered) or 'nothing'}), so nothing was downloaded",
            scope=Scope.ITEM, origin=FETCH_ORIGIN, detail={**detail, "offered": offered},
        )
    return bandcamp.LOSSY_ENCODING, True


def _item_failure(exc: bandcamp.BandcampError, detail: dict[str, Any]) -> CratekitError:
    if isinstance(exc, bandcamp.SessionRejected):
        return _parked(_rejected(exc, FETCH_ORIGIN).cause)
    return refuse(
        "unavailable-transient",
        f"{detail['artist']} - {detail['title']} could not be fetched ({exc}); it "
        f"stays queued",
        remedy=Remedy.RETRY_LATER, scope=Scope.ITEM, retryable=True, origin=FETCH_ORIGIN,
        detail=detail,
    )


def _empty_holding(holding_dir: Path, *, keep: Iterable[Path]) -> None:
    """Empty a release's holding folder but for refused copies, the run's only copy of
    a paid track, which the refusal names."""
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

    A recorded purchase is done, so a resume fetches nothing twice; a refused
    session or unmounted volume parks the job. A name already in the batch with
    other bytes is refused for that file alone, and the purchase is recorded
    whatever was refused, since the release itself was taken.
    """
    said = dict(((job.payload or {}).get(RELEASES) or {}).get(item.item_id) or {})
    batch = str((job.payload or {}).get(BATCH) or "")
    detail: dict[str, Any] = {
        "item_id": item.item_id, "seller": str(said.get("seller") or ""),
        "artist": str(said.get("artist") or ""), "title": str(said.get("title") or ""),
    }
    label = str(said.get("label") or "").strip()
    if not landing.plain_name(batch):
        raise refuse(
            "internal-error", f"job {job.job_id} froze no batch folder a release can stage into",
            remedy=Remedy.REPORT_DEFECT, scope=Scope.ITEM, origin=FETCH_ORIGIN, detail=detail,
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
            scope=Scope.ITEM, origin=FETCH_ORIGIN, detail=detail,
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
            remedy=Remedy.RETRY_LATER, scope=Scope.ITEM, retryable=True, origin=FETCH_ORIGIN,
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
    config.mkdir_private(target)
    staged: list[str] = []
    held: list[str] = []
    refused: dict[str, Path] = {}
    untagged: list[str] = []
    for path in checked:
        number = number_in(path.name, detail["artist"], detail["title"])
        if (number is not None and number in held_numbers) or file_holding(
            path, library, detail["artist"]
        ):
            held.append(path.name)
            continue
        marked = lossy or acquire_cli.lossy_landing(path, policy=policy)
        final = target / acquire_cli.marked_name(path, marker, required=marked)
        # The label is written before the move (U177); a file that will not take it
        # is staged anyway and the item fails naming it.
        if label and not tags.write_tags(path, {"label": label}):
            untagged.append(final.name)
        if final.exists():
            if final.is_file() and filecmp.cmp(path, final, shallow=False):
                # The same bytes, as a resume after a kill finds: staged, not refused.
                staged.append(final.name)
                path.unlink()
                continue
            refused[final.name] = path
            continue
        path.replace(final)
        staged.append(final.name)
    _empty_holding(holding_dir, keep=refused.values())
    record_fetched(
        cfg, item.item_id,
        {
            **{key: detail[key] for key in ("seller", "artist", "title")},
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "job_id": job.job_id,
            "batch": batch, "encoding": encoding, "staged": staged, "held": held,
            "refused": sorted(refused),
            "kept": {name: str(path) for name, path in sorted(refused.items())},
            "label": label or None, "untagged": sorted(untagged),
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
            scope=Scope.ITEM, origin=FETCH_ORIGIN,
            detail={
                **detail, "batch": str(target), "refused": sorted(refused),
                "kept": [str(path) for _name, path in sorted(refused.items())], "staged": staged,
            },
        )
    if untagged:
        raise refuse(
            LABEL_UNWRITTEN,
            f"{len(untagged)} file(s) of {detail['artist']} - {detail['title']} would "
            f"not take the label {label!r} and were staged in {target} without it: "
            f"{'; '.join(untagged)}. A landing files them under no label; the other "
            f"{len(staged) - len(untagged)} file(s) carry it, and the purchase is "
            f"recorded as fetched",
            steps=(
                "check each file named can be written and is not on a read only "
                "volume, then write its label tag or land it filed under no label",
            ),
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail={**detail, "label": label, "batch": str(target), "untagged": untagged},
        )
    return jobs.Produced()


__all__ = [
    "BATCH", "BATCH_PREFIX", "LABEL_UNWRITTEN", "LAND_BY_LABEL", "LAND_FLAG", "SELLER_UNREGISTERED",
    "Disposition", "FETCH_ORIGIN", "Held", "LOGIN_STEP", "Library", "ORIGIN", "Planned",
    "RECORD_VERSION", "RELEASES", "SOURCE", "TO_FETCH", "acquire_bandcamp",
    "acquire_bandcamp_fetch", "build", "build_fetch", "collection", "fetch_argv", "fetch_command",
    "fetched", "file_holding", "forget", "frozen_release", "handle_fetch", "holding",
    "land_command", "labels_of", "plan", "record_fetched", "register_command", "registry",
    "session_cookie", "staging_batch", "track_wanted", "transport", "unregistered",
]
