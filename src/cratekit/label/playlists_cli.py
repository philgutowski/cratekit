"""``label.playlists``: a followed label as a folder of year playlists (R-835).

One ``<Label>`` folder holding a private ``<Label> <year>`` playlist per year,
planned from the catalogue the label sweep already crawls, shown at one
explicit gate and built on ``apply``. It adds, never removes, and a second run
over an unchanged catalogue plans nothing. A catalogue read in part is refused
before the gate; a release the provider no longer has is counted. A label
nobody follows is a plan of nothing, still gated, ending NO_OP.

``--releases`` reads only the releases a label sync took (U191). A full build
is counted before it is read and over :data:`FULL_BUILD_CALLS` stops at its own
gate, ``label.playlists.crawl``; it keeps its reads (R-1091) so a stopped crawl
resumes, the crawl digest staying over the listing's count.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

import shlex
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config as core_config
from cratekit.core import provider_gate
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, dated, kept_reads, sweep, sync_cli, tombstoned
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.sync import run

if TYPE_CHECKING:
    from cratekit.modules.outbound import folders

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

#: Provider calls one release's tracks cost at least, the album and its tracks.
CALLS_PER_RELEASE = 2

#: The estimated provider calls over which a full build asks first (U191).
FULL_BUILD_CALLS = 500

#: What the warning says when a label sync took nothing for the label.
NOTHING_TAKEN_SAID = (
    "no label sync go has taken a release of this label, so there is nothing to "
    "add without reading its whole catalogue"
)
#: What it says when a go took releases and none has a dated track to add.
NOTHING_LEFT_SAID = (
    "label sync goes took {taken} release(s) of this label and none of them has "
    "a dated track the provider still lists: {gone} gone from the provider, "
    "{undated} with no year, {unnamed} named by no release"
)
#: What it says instead when tracks were left out as removed from the library.
NOTHING_LEFT_TOMBSTONED_SAID = (
    "label sync goes took {taken} release(s) of this label and none of them has "
    "a dated track left to add, since {tombstoned} track(s) of them were removed "
    "from the library through crate delete review and are never added"
)


def tombstoned_said(count: int) -> str:
    """What a screen says of the tracks the library removed on purpose (U243)."""
    return (
        f"{count} track(s) of this catalogue were removed from the library through "
        f"crate delete review, so no build adds them and crate label prune takes "
        f"them off the year playlists this product made"
    )


def not_followed(ctx, payload: dict[str, Any], name: str) -> Envelope:
    """A label nobody follows: the plan of nothing, ended NO_OP under its warning."""
    return ctx.envelope(
        data=payload,
        outcome=Outcome.NO_OP,
        warnings=[
            {"code": "label-playlists-not-followed", "message": f"{name}: {NOT_FOLLOWED_SAID}"}
        ],
    )


def label_argument(parser) -> None:
    """The followed label every label verb is named for."""
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )


def _unnamed(identity: str) -> bool:
    """A release the sync named only by its review item, which no provider read can name."""
    return not identity or identity.startswith("item:")


def build_playlists(parser, entry) -> None:
    del entry
    label_argument(parser)
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


def list_catalogue(cfg, entry: labels.LabelEntry, found: catalogue.Catalogue) -> sweep.Listed:
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
    tombstoned: tuple[str, ...] = ()


def release_rows(
    entry: labels.LabelEntry, tracks: catalogue.ReleaseTracks, release_id: str
) -> tuple[Sequence[Any], Any] | None:
    """One release's rows and stated year read now, ``None`` when the provider no
    longer has it, or the refusal of any other failed read."""
    try:
        rows, stated, _short = tracks.release_tracks(release_id)
    except catalogue.ReleaseUnresolvable:
        return None
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - refused, never swallowed
        raise incomplete(
            entry,
            f"the tracks of the release {release_id} could not be read "
            f"({type(exc).__name__}: {exc})",
        ) from exc
    return rows, stated


def _read_one(
    entry: labels.LabelEntry,
    tracks: catalogue.ReleaseTracks,
    release_id: str,
    reads: kept_reads.KeptReads | None,
) -> tuple[Sequence[Any], Any] | None:
    """One release's rows and stated year, kept or read now (and then kept), ``None``
    when it is gone."""
    held = reads.fresh(release_id) if reads is not None else None
    if held is not None:
        return None if held.gone else (held.tracks, held.year)
    answered = release_rows(entry, tracks, release_id)
    if reads is not None:
        if answered is None:
            reads.keep_gone(release_id)
        else:
            reads.keep(release_id, *answered)
    return answered


def _grouped(
    entry: labels.LabelEntry,
    found: catalogue.Catalogue,
    wanted: Sequence[tuple[str, str]],
    gone_from_library: tombstoned.Tombstoned,
    reads: kept_reads.KeptReads | None = None,
) -> _Grouped:
    """Each ``(identifier, listed year)`` release's tracks read once and grouped by
    year, or the refusal. ``reads`` (R-1091) are written once more on the way out,
    a park included; a track ``gone_from_library`` answers for (U243) is left out
    of every year and named in ``tombstoned``."""
    if reads is None:
        return _group(entry, catalogue.ReleaseTracks(found), wanted, None, gone_from_library)
    try:
        grouped = _group(entry, catalogue.ReleaseTracks(found), wanted, reads, gone_from_library)
    except BaseException as exc:
        # THE STOP IS WHAT THE PERSON IS TOLD; a failure to keep reads is a note.
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
    gone_from_library: tombstoned.Tombstoned,
) -> _Grouped:
    years: dict[str, list[str]] = {}
    by_release: dict[str, tuple[str, tuple[str, ...]]] = {}
    taken_away: dict[str, None] = {}
    #: The years a removed track was left out of, so one emptied by them is not made.
    emptied_by: set[str] = set()
    undated = gone = 0
    for release_id, listed_year in wanted:
        answered = _read_one(entry, tracks, release_id, reads)
        if answered is None:
            gone += 1
            continue
        rows, stated = answered
        # A TRACK THE LIBRARY REMOVED is judged on every release, dated or not (U243).
        for row in rows:
            identifier = _id(row)
            if identifier and gone_from_library(
                tombstoned.track_artist(row), tombstoned.track_title(row)
            ):
                taken_away[identifier] = None
        year = _year(stated, listed_year)
        # EVERY TRACK, playable or not, is the label's to the prune (R-836).
        by_release[release_id] = (year, tuple(dict.fromkeys(_id(row) for row in rows if _id(row))))
        if not year:
            undated += 1
            continue
        held = years.setdefault(year, [])
        for row in rows:
            identifier = _id(row)
            # NOT ONE THE LIBRARY REMOVED (U243), NOR ONE THE PROVIDER WON'T PLAY.
            if identifier in taken_away:
                emptied_by.add(year)
                continue
            if identifier and getattr(row, "available", True) is not False:
                if identifier not in held:
                    held.append(identifier)
    return _Grouped(
        # A YEAR EMPTIED BY REMOVALS ALONE IS NOT MADE.
        years={
            year: tuple(ids)
            for year, ids in years.items()
            if ids or year not in emptied_by
        },
        by_release=by_release,
        undated=undated,
        gone=gone,
        tombstoned=tuple(sorted(taken_away)),
    )


def read_catalogue(
    cfg,
    entry: labels.LabelEntry,
    found: catalogue.Catalogue,
    *,
    listed: sweep.Listed | None = None,
    reads: kept_reads.KeptReads | None = None,
) -> folders.LabelCatalogue:
    """The label's confirmed catalogue, grouped by year, or the refusal; ``listed``
    a listing already read, ``reads`` the kept release reads (R-1091)."""
    from cratekit.modules.outbound import folders

    if listed is None:
        listed = list_catalogue(cfg, entry, found)
    try:
        confirmed = sweep.confirm_listed(cfg, listed)
    except run.LookupFailure as exc:
        raise incomplete(entry, str(exc)) from exc
    # A CATALOGUE THAT CONFIRMS NOTHING IS A DEGRADED VERIFIER, not an empty label.
    if confirmed.dropped and not confirmed.releases:
        raise incomplete(
            entry,
            f"{len(confirmed.dropped)} release(s) were read and the catalogue "
            f"confirmed none of them as the label's",
        )
    gone_from_library = tombstoned.Tombstoned(cfg)

    def grouped_of(releases: Sequence[Any]) -> _Grouped:
        wanted = [(_id(release), sweep.year_of(release)) for release in releases]
        return _grouped(entry, found, wanted, gone_from_library, reads)

    grouped = grouped_of(confirmed.releases)
    # A SUPPRESSED RELEASE IS READ FOR ITS TOMBSTONED TRACKS ALONE (U243).
    held_back = (
        grouped_of(confirmed.suppressed_releases).tombstoned
        if confirmed.suppressed_releases
        else ()
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
        tombstoned=tuple(sorted({*grouped.tombstoned, *held_back})),
        # ONLY A MISMATCH IS "NO LONGER CONFIRMS" TO THE PRUNE (R-836).
        mismatched=tuple(one.identity for one in confirmed.dropped if one.reason == "mismatch"),
    )


@dataclass(frozen=True, slots=True)
class TakenRelease:
    """One release a go took for the label, as its answer recorded it."""

    identity: str
    artist: str
    title: str
    year: str


def taken_releases(document: Mapping[str, Any], label_id: str) -> tuple[TakenRelease, ...]:
    """Every release :func:`cratekit.label.dated.taken_by_goes` names, in the order
    the goes took them, with what its answer recorded of it."""
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
    cfg,
    entry: labels.LabelEntry,
    found: catalogue.Catalogue,
    taken: Sequence[TakenRelease],
) -> folders.LabelCatalogue:
    """The taken releases' tracks grouped by year, one named by no release unasked."""
    from cratekit.modules.outbound import folders

    readable = [one for one in taken if not _unnamed(one.identity)]
    grouped = _grouped(
        entry, found, [(one.identity, one.year) for one in readable], tombstoned.Tombstoned(cfg)
    )
    return folders.LabelCatalogue(
        label_id=entry.label_id,
        name=entry.name,
        years=grouped.years,
        releases=len(readable),
        undated=grouped.undated,
        gone=grouped.gone,
        by_release=grouped.by_release,
        tombstoned=grouped.tombstoned,
    )


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
    #: The command's call ceiling and what the listing spent of it (U193).
    ceiling: int = field(
        default_factory=lambda: int(core_config.DEFAULT_PROVIDER_CALLS_PER_COMMAND)
    )
    spent: int = 0
    #: The hour's budget (U278).
    budget: int = field(default_factory=lambda: int(core_config.DEFAULT_PROVIDER_CALLS_PER_HOUR))
    #: Where the label's listing came from, kept or asked and why (U217).
    listing: str = ""

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
        # OVER THE CEILING ASKS TOO, even under the build's own line.
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
        return dated.gate_plan(
            # OVER THE LISTING'S COUNT, so a resumed run is not stale.
            digest_of(
                {"kind": CRAWL_GATE, "label": self.label_id, "releases": self.releases}
            ),
            items,
            {"create": 0, "add": 0, "writes": False},
        )

    def shown(self) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "label": self.name,
            "estimate": self.said(),
            "why this asks": (
                f"a full build over {FULL_BUILD_CALLS} provider calls reads the "
                f"whole catalogue, so it starts only once you choose it"
                if self.calls > FULL_BUILD_CALLS
                else f"a crawl past this command's ceiling of {self.ceiling} provider "
                f"calls would stop part way, so it starts only once you choose it"
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
        if self.listing:
            shown["listing"] = self.listing
        if self.over_ceiling:
            shown["call ceiling"] = (
                f"this is more than the {self.ceiling} provider calls one command may "
                f"make, {self.spent} of them spent on the listing already, so a crawl "
                f"stops at the ceiling and keeps what it read; to read it in one run, "
                f"answer crawl with --calls {self.one_run}"
                + (f" --calls-per-hour {self.one_run}" if self.one_run > self.budget else "")
                + " before the command"
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
    kept, oldest = reads.kept(_id(one) for one in listed.releases) if reads else (0, "")
    settings = provider_gate.GateSettings.from_config(cfg)
    return Estimate(
        label_id=entry.label_id,
        name=entry.name,
        releases=len(listed.releases),
        pace_s=float(cfg.provider.min_interval_s),
        kept=kept,
        kept_age=oldest,
        ceiling=provider_gate.ceiling(settings),
        spent=provider_gate.command_spent(),
        budget=provider_gate.hourly(settings),
        listing=listed.kept.said() if listed.kept is not None else "",
    )


def _items(planned: folders.Plan | None) -> list[dict[str, Any]]:
    if planned is None:
        return []
    folder = {"id": planned.folder_id, "kind": "folder", "name": planned.catalogue.name}
    return [
        {**folder, "action": planned.folder_action},
        *(
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
            for step in planned.years
        ),
    ]


def _payload(planned: folders.Plan | None, *, name: str, scope: str = "") -> dict[str, Any]:
    identity = planned.identity() if planned is not None else {"kind": "label-playlists", "label": name}
    if scope:
        # A RELEASES PLAN IS ITS OWN DECISION, never a full build's answer.
        identity = {**identity, "scope": scope}
    items = _items(planned)
    return dated.gate_plan(
        digest_of(identity),
        items,
        {
            "create": sum(1 for item in items if item["action"] == dated.CREATE),
            "add": sum(int(item.get("add") or 0) for item in items),
            "writes": bool(planned is not None and planned.writes),
        },
    )


def _line(step: folders.YearStep) -> str:
    from cratekit.modules.outbound import folders

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


def _nothing_said(taken: Sequence[TakenRelease], read: folders.LabelCatalogue | None) -> str:
    """Why a releases build of a followed label plans nothing to make."""
    if not taken or read is None:
        return NOTHING_TAKEN_SAID
    said = NOTHING_LEFT_SAID.format(
        taken=len(taken),
        gone=read.gone,
        undated=read.undated,
        unnamed=sum(1 for one in taken if _unnamed(one.identity)),
    )
    if read.tombstoned:
        # THE REMOVAL LEADS: the provider may still list every such track.
        return NOTHING_LEFT_TOMBSTONED_SAID.format(
            taken=len(taken), tombstoned=len(read.tombstoned)
        ) + said[said.index(":"):]
    return said


def _shown(
    planned: folders.Plan | None,
    *,
    name: str,
    taken: Sequence[TakenRelease] | None = None,
    listed: Estimate | None = None,
    read: folders.LabelCatalogue | None = None,
    reads: kept_reads.KeptReads | None = None,
) -> dict[str, Any]:
    from cratekit.modules.outbound import folders

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
    if read.tombstoned:
        shown["removed from the library"] = tombstoned_said(len(read.tombstoned))
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
    if listed is not None and listed.listing:
        shown["listing"] = listed.listing
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


def _failed_part_way(exc: Exception, done: folders.Applied, planned: folders.Plan) -> CratekitError:
    """The failure, with what was already written named in it."""
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
    return dated.refused_part_way(
        exc, wrote, again, detail, failed="The build", origin=_ORIGIN, steps=False
    )


def plan_label(cfg, entry: labels.LabelEntry, found: catalogue.Catalogue, remote) -> folders.Plan:
    """One followed label's plan against the account, or its refusal; public for
    ``crate organize`` (U112), so a label is planned there as here."""
    from cratekit.modules.outbound import folders

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
    """Build what one label's plan names, or raise naming what was written first."""
    from cratekit.modules.outbound import folders

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
        from cratekit.modules.outbound import account, folders

        found = catalogue.resolve(cfg)
        if from_releases:
            taken = taken_releases(sync_cli.load_record(cfg), entry.label_id)
            read = read_taken(cfg, entry, found, taken)
        else:
            # THE KEPT READS FIRST, so an unreadable store refuses first (R-1091).
            reads = kept_reads.KeptReads.load(entry.label_id)
            listed = list_catalogue(cfg, entry, found)
            counted = estimate(cfg, entry, listed, reads)
            if counted.over:
                # STOPPED BEFORE ANY RELEASE IS READ, until answered ``crawl``.
                crawl = counted.plan()
                option = ctx.gate.require(
                    _gate(ctx, CRAWL_GATE), plan=crawl, context=counted.shown()
                )
                if option != "crawl":
                    return ctx.envelope(data=crawl, outcome=Outcome.NO_OP)
            read = read_catalogue(cfg, entry, found, listed=listed, reads=reads)
        # A RELEASES PLAN WITH NO YEAR MAKES NOTHING, not even the folder.
        if not (from_releases and not read.years):
            remote = account.resolve(cfg)
            planned = folders.plan(cfg, read, remote)
    scope = "releases" if from_releases else ""
    payload = _payload(planned, name=name, scope=scope)
    # THE PLAN ITSELF, so the screen shows every item the digest covers (R-693).
    option = ctx.gate.require(
        _gate(ctx, BUILD_GATE),
        plan=payload,
        context=_shown(planned, name=name, taken=taken, listed=counted, read=read, reads=reads),
    )
    if planned is None:
        if entry is None:
            return not_followed(ctx, payload, name)
        elif not taken:
            code, said = "label-playlists-nothing-taken", NOTHING_TAKEN_SAID
        else:
            code, said = "label-playlists-nothing-left", _nothing_said(taken, read)
        warning = {"code": code, "message": f"{name}: {said}"}
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=[warning])
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=_unkept_warnings(reads))

    done = apply_plan(cfg, remote, planned)
    # WHAT WAS WRITTEN RIDES ON THE TOTALS, as ``plan/1`` admits no other key.
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
    "tombstoned_said",
    "taken_releases",
]
