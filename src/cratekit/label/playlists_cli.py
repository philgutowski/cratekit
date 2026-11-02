"""``label.playlists``: a followed label as a folder of year playlists (R-835).

The source system's label shape on the account, kept once it retires: one
``<Label>`` folder holding one private ``<Label> <year>`` playlist per release
year, each filled with that year's tracks from the label's catalogue. This verb
plans that shape, shows it at one explicit gate, and on ``apply`` builds what is
missing. It adds and never removes, and a second run over an unchanged
catalogue plans nothing to write.

THE CATALOGUE IS THE ONE THE PRODUCT ALREADY CRAWLS. The roster, the release
listing, the tombstone question and the verifier are the label sweep's own,
through :func:`cratekit.label.sweep.confirmed_releases`, and each release's
tracks are read through :class:`cratekit.label.catalogue.ReleaseTracks`. Every
call passes the provider gate's pacing, since both the catalogue and the
account are built over the gated session. Nothing here is a second crawler.

A CATALOGUE READ IN PART IS REFUSED BEFORE THE GATE, ``label-playlists-
incomplete``. A plan built from half a label would be shown as the label, and
the person approving it could not tell. A release the provider no longer has
is the provider answering, and is counted rather than refused.

A LABEL THAT IS NOT FOLLOWED IS A PLAN OF NOTHING, still gated, decided before
a credential is asked for, on ``sync unmark``'s precedent. It ends NO_OP under
a warning that says why.

``--releases`` READS ONLY WHAT A LABEL SYNC TOOK (U191). A full build reads the
whole catalogue, two provider calls a release, and on a label the size of
Defected that is thousands of calls before a plan is shown. With the flag the
catalogue is never listed: the releases are the ones a go settled for the
label, read from the label sync record as :func:`cratekit.label.dated.taken_by_goes`
reads them, and only their tracks are asked for. The years they fall in are
planned through the same :func:`cratekit.modules.outbound.folders.plan`, which
walks only the years it is handed, so a year no taken release names is never
read and never touched, and the plan adds only. What the ledger records as
added is not asked for again, so a second run plans nothing.

A FULL BUILD IS COUNTED BEFORE IT IS READ (U191). The listing is read first,
which is the roster and the paged listing and nothing per release, and the
calls the rest would make are estimated from its count. Over
:data:`FULL_BUILD_CALLS` the build stops at its own explicit gate,
``label.playlists.crawl``, with the estimate in front of the person, and reads
nothing more until that gate is answered ``crawl``.

A FULL BUILD KEEPS WHAT IT READS (R-1091). Each release's tracks are kept per
label by :mod:`cratekit.label.kept_reads` for that module's stated age, so a
crawl the provider's breaker stops part way resumes from where it stopped, and
the run that carries out an approved plan reads none of the catalogue again.
The crawl gate is asked over the calls still to make, and its digest stays over
the listing's count, so a run resumed under the same answer is not stale. The
build gate's digest stays the plan's identity alone, and both screens say how
many reads were reused and how old the oldest is. The listing itself is read
again by every run, so a release the label put out since is never hidden by a
kept one. ``--releases`` and ``crate organize`` keep nothing.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

import shlex
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config as core_config
from cratekit.core import provider_gate
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, dated, kept_reads, sweep, sync_cli
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.modules.outbound import folders
from cratekit.sync import run

_ORIGIN = ("label.playlists",)

#: What the gate screen and the warning say about a label nobody follows.
NOT_FOLLOWED_SAID = (
    "no followed label goes by this name, so there is no catalogue to build a "
    "folder from"
)


#: The gate a full build stops at when its estimate is over the threshold.
CRAWL_GATE = "label.playlists.crawl"
#: The gate every build asks before it writes to the account.
BUILD_GATE = "label.playlists.confirm"

#: Provider calls one release's tracks cost: the album, then its track listing,
#: which is ``TidalCatalogue.release_tracks``' two reads. A release longer than
#: one page of tracks costs more, so the estimate is a floor and says so.
CALLS_PER_RELEASE = 2

#: The estimated provider calls over which a full build stops and asks first
#: (U191). Five hundred is about eight minutes at the default pace of one call
#: a second, and two hundred and fifty releases: a label of that size builds
#: without a question, and Defected's twelve thousand releases do not.
FULL_BUILD_CALLS = 500

#: What the warning says when a label sync took nothing for the label.
NOTHING_TAKEN_SAID = (
    "no label sync go has taken a release of this label, so there is nothing to "
    "add without reading its whole catalogue"
)
#: What it says when a go took releases and none of them has a dated track to
#: add: every one is gone from the provider, dated by nothing, or named by no
#: release. Not "nothing taken", which would be false.
NOTHING_LEFT_SAID = (
    "label sync goes took {taken} release(s) of this label and none of them has "
    "a dated track the provider still lists: {gone} gone from the provider, "
    "{undated} with no year, {unnamed} named by no release"
)


def _unnamed(identity: str) -> bool:
    """A release the sync named only by its review item, which no provider read can name."""
    return not identity or identity.startswith("item:")


def build_playlists(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )
    parser.add_argument(
        "--releases",
        action="store_true",
        help=(
            "add only the releases a label sync go took for this label, reading "
            "only those releases and never the whole catalogue"
        ),
    )
    parser.set_defaults(_handler=label_playlists)


def incomplete(entry: labels.LabelEntry, what: str) -> CratekitError:
    return refuse(
        "label-playlists-incomplete",
        f"the catalogue of {entry.name!r} was not read in full ({what}), so no plan "
        f"was made from it and nothing was written to the account",
        steps=("run it again once the provider is answering",),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"label_id": entry.label_id},
    )


def _year(stated: Any, listed: str) -> str:
    """The release's year: the provider's own dating of it, else the listing's."""
    if isinstance(stated, int) and stated > 0:
        return f"{stated:04d}"
    return listed if len(listed) == 4 and listed.isdigit() else ""


def _id(row: Any) -> str:
    return str(getattr(row, "id", "") or "")


def list_catalogue(
    cfg, entry: labels.LabelEntry, found: catalogue.Catalogue
) -> sweep.Listed:
    """The label's listing, read in full, and nothing read per release, or the refusal."""
    try:
        listed = sweep.listed_releases(cfg, entry, found)
    except run.LookupFailure as exc:
        raise incomplete(entry, str(exc)) from exc
    if listed.unread:
        raise incomplete(
            entry,
            "; ".join(f"{one.artist} ({one.listing}: {one.reason})" for one in listed.unread),
        )
    return listed


@dataclass(frozen=True, slots=True)
class _Grouped:
    years: dict[str, tuple[str, ...]]
    by_release: dict[str, tuple[str, tuple[str, ...]]]
    undated: int
    gone: int


def _read_one(
    entry: labels.LabelEntry,
    tracks: catalogue.ReleaseTracks,
    release_id: str,
    reads: kept_reads.KeptReads | None,
) -> tuple[Sequence[Any], Any] | None:
    """One release's rows and stated year, kept or read now, ``None`` when it is gone.

    A read the store keeps fresh is answered without the provider. A read made
    now is kept, and a release the provider no longer has is kept as gone,
    since that is the provider answering. A failed read is never kept.
    """
    held = reads.fresh(release_id) if reads is not None else None
    if held is not None:
        return None if held.gone else (held.tracks, held.year)
    try:
        rows, stated, _short = tracks.release_tracks(release_id)
    except catalogue.ReleaseUnresolvable:
        if reads is not None:
            reads.keep_gone(release_id)
        return None
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - refused, never swallowed
        raise incomplete(
            entry,
            f"the tracks of the release {release_id} could not be read "
            f"({type(exc).__name__}: {exc})",
        ) from exc
    if reads is not None:
        reads.keep(release_id, rows, stated)
    return rows, stated


def _grouped(
    entry: labels.LabelEntry,
    found: catalogue.Catalogue,
    wanted: Sequence[tuple[str, str]],
    reads: kept_reads.KeptReads | None = None,
) -> _Grouped:
    """Each release's tracks read once and grouped by year, or the refusal.

    ``wanted`` is each release as ``(identifier, the year it was listed
    under)``. A release the provider no longer has is counted as gone; any other
    failed read refuses the plan, since a year built from half its releases
    would be shown as the year.

    ``reads`` is a full build's kept reads (R-1091). What it keeps fresh is not
    asked again, and what is read now is kept, written as it goes and once
    more on the way out, a breaker's park or a refusal included, so a stopped
    build keeps everything it read.
    """
    if reads is None:
        return _group(entry, catalogue.ReleaseTracks(found), wanted, None)
    try:
        grouped = _group(entry, catalogue.ReleaseTracks(found), wanted, reads)
    except BaseException as exc:
        # THE STOP IS WHAT THE PERSON IS TOLD, never a failure to keep the
        # reads behind it: a park read as a disk error would send somebody to
        # repair a file over a provider that only asked them to wait.
        # A write the filesystem refuses is the store's ``unkept`` already;
        # anything else out of the write is this build's own defect, and is
        # still only noted on the stop.
        try:
            reads.flush()
        except Exception as lost:  # noqa: BLE001 - noted on the stop, never in its place
            exc.add_note(
                f"the release reads made before this could not be kept "
                f"({type(lost).__name__}: {lost}), so the next run reads them again"
            )
        if reads.unkept:
            exc.add_note(_unkept_said(reads))
        raise
    reads.flush()
    return grouped


def _group(
    entry: labels.LabelEntry,
    tracks: catalogue.ReleaseTracks,
    wanted: Sequence[tuple[str, str]],
    reads: kept_reads.KeptReads | None,
) -> _Grouped:
    years: dict[str, list[str]] = {}
    by_release: dict[str, tuple[str, tuple[str, ...]]] = {}
    undated = gone = 0
    for release_id, listed_year in wanted:
        answered = _read_one(entry, tracks, release_id, reads)
        if answered is None:
            gone += 1
            continue
        rows, stated = answered
        year = _year(stated, listed_year)
        # EVERY TRACK the release carries, playable or not, is what the prune
        # reads as still the label's (R-836): a track that stopped playing is
        # still on a release the catalogue confirms.
        by_release[release_id] = (
            year,
            tuple(dict.fromkeys(_id(row) for row in rows if _id(row))),
        )
        if not year:
            undated += 1
            continue
        held = years.setdefault(year, [])
        for row in rows:
            identifier = _id(row)
            # A TRACK THE PROVIDER WILL NOT PLAY is never asked for, since the
            # client skips it on an add and it would be refused every run.
            if identifier and getattr(row, "available", True) is not False:
                if identifier not in held:
                    held.append(identifier)
    return _Grouped(
        years={year: tuple(ids) for year, ids in years.items()},
        by_release=by_release,
        undated=undated,
        gone=gone,
    )


def read_catalogue(
    cfg,
    entry: labels.LabelEntry,
    found: catalogue.Catalogue,
    *,
    listed: sweep.Listed | None = None,
    reads: kept_reads.KeptReads | None = None,
) -> folders.LabelCatalogue:
    """The label's confirmed catalogue, grouped by year, or the refusal.

    ``listed`` is a listing :func:`list_catalogue` already read, so a full build
    that counted it before its estimate gate does not list the label twice.
    ``reads`` is the label's kept release reads, which only ``crate label
    playlists`` hands in (R-1091); without it every release is read now.
    """
    if listed is None:
        listed = list_catalogue(cfg, entry, found)
    try:
        confirmed = sweep.confirm_listed(cfg, listed)
    except run.LookupFailure as exc:
        raise incomplete(entry, str(exc)) from exc
    # A CATALOGUE THAT CONFIRMS NOTHING IS NOT A LABEL WITH NOTHING ON IT, the
    # sweep worker's own refusal (``label.cli._refuse_unfinished``): releases
    # were read and the verifier would vouch for none, which is what a degraded
    # credit endpoint answers. Shown, it would be an empty folder under the
    # label's name, approved as the label.
    if confirmed.dropped and not confirmed.releases:
        raise incomplete(
            entry,
            f"{len(confirmed.dropped)} release(s) were read and the catalogue "
            f"confirmed none of them as the label's",
        )
    grouped = _grouped(
        entry,
        found,
        [
            (str(getattr(release, "id", "") or ""), sweep.year_of(release))
            for release in confirmed.releases
        ],
        reads,
    )
    return folders.LabelCatalogue(
        label_id=entry.label_id,
        name=entry.name,
        years=grouped.years,
        releases=len(confirmed.releases),
        undated=grouped.undated,
        dropped=len(confirmed.dropped),
        gone=grouped.gone,
        suppressed=confirmed.suppressed,
        by_release=grouped.by_release,
        # A VERDICT OF MISMATCH IS THE CATALOGUE SAYING ANOTHER LABEL, which is
        # what "no longer confirms" means to the prune. "unconfirmed" is no
        # credit found, an absence, and is not evidence of anything (R-836).
        mismatched=tuple(one.identity for one in confirmed.dropped if one.reason == "mismatch"),
    )


# ---------------------------------------------------------------------------
# The releases a label sync took (U191)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TakenRelease:
    """One release a go took for the label, as its answer recorded it."""

    identity: str
    artist: str
    title: str
    year: str


def taken_releases(document: Mapping[str, Any], label_id: str) -> tuple[TakenRelease, ...]:
    """Every release a go took for the label, in the order the goes took them.

    WHICH RELEASES is :func:`cratekit.label.dated.taken_by_goes`' answer, the
    one the dated playlist reads: an ``all`` or a ``pick`` a go settled. An
    answer no go has taken is not read, since its tracks are not downloaded
    yet. What each answer recorded about a release, its artist, title and
    listed year, is kept for the screen and for a release the provider dates
    by nothing.
    """
    took = dated.taken_by_goes(document, label_id)
    recorded: dict[str, TakenRelease] = {}
    for entry in document.get("answers") or ():
        if not isinstance(entry, Mapping) or entry.get("label_id") != label_id:
            continue
        releases = entry.get("releases")
        for raw in releases if isinstance(releases, list) else ():
            if not isinstance(raw, Mapping):
                continue
            identity = str(raw.get("identity") or "")
            if identity in took and identity not in recorded:
                recorded[identity] = TakenRelease(
                    identity=identity,
                    artist=str(raw.get("artist") or ""),
                    title=str(raw.get("title") or ""),
                    year=str(raw.get("year") or ""),
                )
    ordered = sorted(took.items(), key=lambda kv: (kv[1], kv[0]))
    return tuple(
        recorded.get(identity) or TakenRelease(identity=identity, artist="", title="", year="")
        for identity, _day in ordered
    )


def read_taken(
    entry: labels.LabelEntry,
    found: catalogue.Catalogue,
    taken: Sequence[TakenRelease],
) -> folders.LabelCatalogue:
    """The taken releases' tracks grouped by year, and nothing else the label has.

    A release the sync named only by its review item, ``item:...``, names no
    release the provider can be asked about, so it is never asked for; the
    screen counts it on its own.
    """
    readable = [one for one in taken if not _unnamed(one.identity)]
    grouped = _grouped(entry, found, [(one.identity, one.year) for one in readable])
    return folders.LabelCatalogue(
        label_id=entry.label_id,
        name=entry.name,
        years=grouped.years,
        releases=len(readable),
        undated=grouped.undated,
        gone=grouped.gone,
        by_release=grouped.by_release,
    )


# ---------------------------------------------------------------------------
# The estimate before a full build (U191)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Estimate:
    """What a full build would spend on the provider, from its listing's count."""

    label_id: str
    name: str
    releases: int
    pace_s: float
    #: Listed releases a kept read answers fresh, which cost no call (R-1091).
    kept: int = 0
    #: How old the oldest of those kept reads is, as a person reads it.
    kept_age: str = ""
    #: The call ceiling this command runs under, and what it has already spent
    #: on the roster and the listing, so a crawl the ceiling would stop part
    #: way is said at the gate before any release is read (U193).
    ceiling: int = field(
        default_factory=lambda: int(core_config.DEFAULT_PROVIDER_CALLS_PER_COMMAND)
    )
    spent: int = 0

    @property
    def calls(self) -> int:
        return (self.releases - self.kept) * CALLS_PER_RELEASE

    @property
    def seconds(self) -> int:
        return round(self.calls * self.pace_s)

    @property
    def over_ceiling(self) -> bool:
        """The crawl would reach this command's call ceiling before it ends."""
        return self.spent + self.calls > self.ceiling

    @property
    def one_run(self) -> int:
        """A ``--calls`` that reads the whole crawl in one run, a hundred or more spare."""
        return ((self.spent + self.calls) // 100 + 2) * 100

    @property
    def over(self) -> bool:
        # OVER THE CEILING ASKS TOO, even under the build's own line, so a
        # ceiling set lower than that line is said here rather than met part
        # way through the crawl.
        return self.calls > FULL_BUILD_CALLS or self.over_ceiling

    def said(self) -> str:
        from cratekit.label import go

        paced = (
            f"{self.calls} provider call(s), {go.duration_text(self.seconds)} at "
            f"{self.pace_s:g} s a call, before the plan is shown"
        )
        if not self.kept:
            return (
                f"{self.releases} release(s) listed, so reading their tracks is at "
                f"least {paced}"
            )
        return (
            f"{self.releases} release(s) listed and {self.kept} of them read by an "
            f"earlier run within the last {kept_reads.kept_for_said()}, so reading "
            f"the other {self.releases - self.kept} is at least {paced}"
        )

    def plan(self) -> dict[str, Any]:
        """The crawl gate's plan: the label and the count it was decided over."""
        items = [
            {
                "id": self.label_id,
                "kind": "catalogue",
                "name": self.name,
                "action": "crawl",
                "releases": self.releases,
                "kept": self.kept,
                "calls": self.calls,
                "seconds": self.seconds,
            }
        ]
        return {
            # OVER THE LISTING'S COUNT, never over what is left to read: a run
            # resumed after a park under the same answer has fewer releases to
            # read, and a digest over those would call the answer stale.
            "digest": digest_of(
                {"kind": CRAWL_GATE, "label": self.label_id, "releases": self.releases}
            ),
            "items": items,
            "totals": {"count": len(items), "create": 0, "add": 0, "writes": False},
            "chunk": None,
        }

    def shown(self) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "label": self.name,
            "estimate": self.said(),
            "why this asks": (
                f"a full build over {FULL_BUILD_CALLS} provider calls reads the "
                f"whole catalogue, so it starts only once you choose it"
            ),
            "instead": shlex.join(["crate", "label", "playlists", self.name, "--releases"])
            + " adds only the releases a label sync took",
            "nothing read yet": (
                "no release's tracks have been read by this run and nothing was written"
            ),
            "then": (
                "answered crawl, the build reads the catalogue to show its plan and "
                f"keeps its reads, written every {kept_reads.FLUSH_EVERY} releases and "
                "again when it stops, so a build the provider stops part way starts "
                "again where it stopped, and the run that applies an approved plan "
                "reads none of it again"
            ),
        }
        if self.kept:
            shown["kept reads"] = _kept_said(self.kept, self.kept_age)
        if self.over_ceiling:
            shown["call ceiling"] = (
                f"this is more than the {self.ceiling} provider calls one command may "
                f"make, {self.spent} of them spent on the listing already, so a crawl "
                f"stops at the ceiling and keeps what it read; to read it in one run, "
                f"answer crawl with --calls {self.one_run} before the command"
            )
        return shown


def _kept_said(count: int, age: str) -> str:
    return (
        f"{count} release read(s) kept from an earlier run, the oldest {age} old; a "
        f"read is taken again once it is {kept_reads.kept_for_said()} old"
    )


def estimate(
    cfg,
    entry: labels.LabelEntry,
    listed: sweep.Listed,
    reads: kept_reads.KeptReads | None = None,
) -> Estimate:
    kept, oldest = (
        reads.kept(str(getattr(one, "id", "") or "") for one in listed.releases)
        if reads is not None
        else (0, "")
    )
    return Estimate(
        label_id=entry.label_id,
        name=entry.name,
        releases=len(listed.releases),
        pace_s=float(cfg.provider.min_interval_s),
        kept=kept,
        kept_age=oldest,
        ceiling=provider_gate.ceiling(provider_gate.GateSettings.from_config(cfg)),
        spent=provider_gate.command_spent(),
    )


def _items(planned: folders.Plan | None) -> list[dict[str, Any]]:
    if planned is None:
        return []
    items: list[dict[str, Any]] = [
        {
            "id": planned.folder_id,
            "kind": "folder",
            "name": planned.catalogue.name,
            "action": planned.folder_action,
        }
    ]
    for step in planned.years:
        items.append(
            {
                "id": step.remote_id,
                "kind": "playlist",
                "year": step.year,
                "name": step.name,
                "action": step.action,
                "move": step.move,
                "add": len(step.add),
                "tracks": step.tracks,
                **({"why": step.why} if step.why else {}),
            }
        )
    return items


def _payload(
    planned: folders.Plan | None, *, name: str, scope: str = ""
) -> dict[str, Any]:
    identity = planned.identity() if planned is not None else {"kind": "label-playlists", "label": name}
    if scope:
        # A RELEASES PLAN IS ITS OWN DECISION. An answer given to a full build
        # is never taken for one built from what a sync took, nor the reverse.
        identity = {**identity, "scope": scope}
    items = _items(planned)
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            "create": sum(1 for item in items if item["action"] == folders.CREATE),
            "add": sum(int(item.get("add") or 0) for item in items),
            "writes": bool(planned is not None and planned.writes),
        },
        "chunk": None,
    }


def _line(step: folders.YearStep) -> str:
    if step.action in (folders.AMBIGUOUS, folders.UNREADABLE):
        return f"{step.name}: left alone, {step.why}"
    doing = {
        folders.CREATE: "create it private",
        folders.ADOPT: "use the one already in the folder",
        folders.REUSE: "use the one already built",
    }[step.action]
    parts = [doing]
    if step.move or step.action == folders.CREATE:
        parts.append("put it in the folder")
    parts.append(f"add {len(step.add)} of {step.tracks} track(s)")
    return f"{step.name}: " + ", ".join(parts)


def _named(one: TakenRelease) -> str:
    said = f"{one.artist} - {one.title}" if one.artist and one.title else one.title or one.identity
    return f"{said} ({one.year})" if one.year else said


def _nothing_said(
    taken: Sequence[TakenRelease], read: folders.LabelCatalogue | None
) -> str:
    """Why a releases build of a followed label plans nothing to make."""
    if not taken or read is None:
        return NOTHING_TAKEN_SAID
    return NOTHING_LEFT_SAID.format(
        taken=len(taken),
        gone=read.gone,
        undated=read.undated,
        unnamed=sum(1 for one in taken if _unnamed(one.identity)),
    )


def _shown(
    planned: folders.Plan | None,
    *,
    name: str,
    taken: Sequence[TakenRelease] | None = None,
    listed: Estimate | None = None,
    read: folders.LabelCatalogue | None = None,
    reads: kept_reads.KeptReads | None = None,
) -> dict[str, Any]:
    if planned is None:
        if taken is not None:
            return {"label": name, "nothing to build": _nothing_said(taken, read)}
        return {"label": name, "nothing to build": NOT_FOLLOWED_SAID}
    read = planned.catalogue
    folder = {
        folders.CREATE: "create it",
        folders.ADOPT: "use the one already on the account under this name",
        folders.REUSE: "use the one already built",
    }[planned.folder_action]
    if taken is None:
        said = (
            f"{read.releases} confirmed release(s) read; left out {read.undated} with "
            f"no year, {read.dropped} the catalogue did not confirm as the label's, "
            f"{read.gone} the provider no longer has, {read.suppressed} deleted on purpose"
        )
    else:
        unnamed = sum(1 for one in taken if _unnamed(one.identity))
        said = (
            f"only the {len(taken) - unnamed} release(s) a label sync took were read, "
            f"and none of the rest of the catalogue; left out {read.undated} with no "
            f"year, {read.gone} the provider no longer has, {unnamed} named by no "
            f"release and never asked for"
        )
    shown: dict[str, Any] = {
        "label": read.name,
        "folder": f"{read.name}: {folder}",
        "year playlists": [_line(step) for step in planned.years],
        "catalogue": said,
        "removes": "nothing, ever: no track, playlist or folder is taken away",
    }
    if taken is not None:
        shown["releases read"] = [_named(one) for one in taken if not _unnamed(one.identity)]
    if listed is not None:
        shown["provider calls"] = (
            f"{listed.releases} release(s) listed, at least {listed.calls} provider "
            f"call(s) to read their tracks"
            if not listed.kept
            else f"{listed.releases} release(s) listed, at least {listed.calls} "
            f"provider call(s) to read the tracks of the "
            f"{listed.releases - listed.kept} not kept from an earlier run"
        )
    if reads is not None:
        shown["release reads"] = _reads_said(reads)
    if planned.stale_folder:
        shown["recorded folder"] = (
            f"the folder recorded for this label, {planned.stale_folder}, is no longer "
            f"on the account, so its record is replaced"
        )
    if not planned.writes:
        shown["nothing to write"] = "the account already holds every year and track planned"
    return shown


def _reads_said(reads: kept_reads.KeptReads) -> str:
    """What the build gate says about the release reads its plan was made from."""
    kept_for = kept_reads.kept_for_said()
    if not reads.reused:
        if reads.unkept:
            return f"all {reads.read_now} release read(s) made by this run; {_unkept_said(reads)}"
        return (
            f"all {reads.read_now} release read(s) made by this run, and kept for "
            f"{kept_for}, so the run that applies the plan reads none of them again"
        )
    said = (
        f"{reads.reused} release read(s) reused from an earlier run, the oldest "
        f"{reads.age_said()} old, and {reads.read_now} read by this run; a read is "
        f"taken again once it is {kept_for} old"
    )
    if reads.unkept:
        said += f"; {_unkept_said(reads)}"
    return said


def _unkept_said(reads: kept_reads.KeptReads) -> str:
    return (
        f"the reads made by this run could not be kept ({reads.unkept}), so a "
        f"later run reads them again"
    )


def _unkept_warnings(reads: kept_reads.KeptReads | None) -> list[dict[str, str]]:
    """What a run whose reads could not be written says about them (R-1091)."""
    if reads is None or not reads.unkept:
        return []
    return [{"code": "label-playlists-reads-unkept", "message": _unkept_said(reads)}]


def _failed_part_way(
    exc: Exception, done: folders.Applied, planned: folders.Plan
) -> CratekitError:
    """The failure, with what was already written named in it.

    ``sync unmark``'s rule: a refusal the account raised keeps its reason and
    remedy, and anything else is this build's own defect and says so. What was
    written is recorded already, so a run started again plans only the rest.
    """
    wrote = (
        f"before this failed the folder was {'created' if done.folder_created else 'in hand'}"
        if done.folder_id
        else "nothing was written before this failed"
    )
    if done.created or done.added:
        wrote += (
            f", {len(done.created)} year playlist(s) were created and "
            f"{sum(done.added.values())} track(s) added"
        )
    detail = {
        "label_id": planned.catalogue.label_id,
        "folder_id": done.folder_id,
        "created": list(done.created),
        "moved": list(done.moved),
        "added": dict(done.added),
    }
    again = "run crate label playlists again; what was written is reused, never made twice"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. The build failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def plan_label(cfg, entry: labels.LabelEntry, found: catalogue.Catalogue, remote) -> folders.Plan:
    """One followed label's plan against the account as it is, or its refusal.

    PUBLIC FOR ``crate organize`` (U112), which plans every followed label
    through this one body, so a label is planned there exactly as here.
    """
    return folders.plan(cfg, read_catalogue(cfg, entry, found), remote)


def refused_warnings(done: folders.Applied) -> list[dict[str, str]]:
    """What an apply says about tracks the provider would not add."""
    if not done.refused:
        return []
    return [
        {
            "code": "label-playlists-tracks-refused",
            "message": (
                f"the provider would not add {sum(done.refused.values())} track(s) "
                f"to {len(done.refused)} year playlist(s); they are recorded and "
                f"not asked for again"
            ),
        }
    ]


def apply_plan(cfg, remote, planned: folders.Plan) -> folders.Applied:
    """Build what one label's plan names, or raise naming what was written first.

    Public for ``crate organize`` (U112), for :func:`plan_label`'s reason.
    """
    done = folders.Applied()
    try:
        folders.apply(cfg, remote, planned, done)
    except Exception as exc:
        raise _failed_part_way(exc, done, planned) from exc
    return done


def applied_totals(done: folders.Applied) -> dict[str, Any]:
    """What was written, as the totals carry it."""
    return {
        "folder_id": done.folder_id,
        "folder_created": done.folder_created,
        "created": list(done.created),
        "moved": list(done.moved),
        "added": dict(done.added),
        "refused": dict(done.refused),
    }


#: Public for ``crate organize`` (U112), whose label step shows these items.
plan_payload = _payload


def _gate(ctx, name: str):
    """The declared gate by its name, or a refusal naming the defect, ``label sync``'s rule."""
    for spec in ctx.entry.gates:
        if spec.name == name:
            return spec
    raise refuse(
        "refused-by-policy",
        f"the label playlists registry entry declares no {name} gate, so there is "
        f"nobody to ask and nothing is read or written",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
    )


def label_playlists(ctx) -> Envelope:
    cfg = label_cli._load()
    name = str(ctx.args.name)
    from_releases = bool(getattr(ctx.args, "releases", False))
    entry = labels.RegistryStore().load().resolve(name)
    planned: folders.Plan | None = None
    remote = None
    #: The releases read, when the build is a releases build of a followed label.
    taken: tuple[TakenRelease, ...] | None = None
    counted: Estimate | None = None
    read: folders.LabelCatalogue | None = None
    reads: kept_reads.KeptReads | None = None
    if entry is not None:
        from cratekit.modules.outbound import account

        found = catalogue.resolve(cfg)
        if from_releases:
            taken = taken_releases(sync_cli.load_record(cfg), entry.label_id)
            read = read_taken(entry, found, taken)
        else:
            # THE KEPT READS FIRST, so a store that cannot be read refuses
            # before the provider is asked anything (R-1091).
            reads = kept_reads.KeptReads.load(entry.label_id)
            listed = list_catalogue(cfg, entry, found)
            counted = estimate(cfg, entry, listed, reads)
            if counted.over:
                # STOPPED BEFORE ANY RELEASE IS READ. The count is all that was
                # asked, and the crawl starts only on an answer of ``crawl``.
                crawl = counted.plan()
                option = ctx.gate.require(
                    _gate(ctx, CRAWL_GATE), plan=crawl, context=counted.shown()
                )
                if option != "crawl":
                    return ctx.envelope(data=crawl, outcome=Outcome.NO_OP)
            read = read_catalogue(cfg, entry, found, listed=listed, reads=reads)
        # A RELEASES PLAN WITH NO YEAR TO ADD TO MAKES NOTHING, not even the
        # folder, since an empty folder under the label's name is not what a
        # sync took.
        if not (from_releases and not read.years):
            remote = account.resolve(cfg)
            planned = folders.plan(cfg, read, remote)
    scope = "releases" if from_releases else ""
    payload = _payload(planned, name=name, scope=scope)
    # THE PLAN ITSELF, so the screen shows every item the digest covers
    # (R-693), with the year by year sentences as the facts in front of them.
    option = ctx.gate.require(
        _gate(ctx, BUILD_GATE),
        plan=payload,
        context=_shown(
            planned, name=name, taken=taken, listed=counted, read=read, reads=reads
        ),
    )
    if planned is None:
        if entry is None:
            warning = {
                "code": "label-playlists-not-followed",
                "message": f"{name}: {NOT_FOLLOWED_SAID}",
            }
        elif not taken:
            warning = {
                "code": "label-playlists-nothing-taken",
                "message": f"{name}: {NOTHING_TAKEN_SAID}",
            }
        else:
            warning = {
                "code": "label-playlists-nothing-left",
                "message": f"{name}: {_nothing_said(taken, read)}",
            }
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=[warning])
    if option != "apply" or not planned.writes:
        return ctx.envelope(
            data=payload, outcome=Outcome.NO_OP, warnings=_unkept_warnings(reads)
        )

    done = apply_plan(cfg, remote, planned)
    # WHAT WAS WRITTEN RIDES ON THE TOTALS, since ``plan/1`` admits no other
    # key at the top of the payload.
    totals = {**payload["totals"], "applied": applied_totals(done)}
    return ctx.envelope(
        data={**payload, "totals": totals},
        outcome=Outcome.OK,
        warnings=[*refused_warnings(done), *_unkept_warnings(reads)],
    )


__all__ = [
    "BUILD_GATE",
    "CALLS_PER_RELEASE",
    "CRAWL_GATE",
    "FULL_BUILD_CALLS",
    "Estimate",
    "TakenRelease",
    "applied_totals",
    "apply_plan",
    "build_playlists",
    "incomplete",
    "estimate",
    "label_playlists",
    "list_catalogue",
    "plan_label",
    "plan_payload",
    "read_catalogue",
    "read_taken",
    "refused_warnings",
    "taken_releases",
]
