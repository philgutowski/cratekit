"""``sync.mark``: a landed sync pass marks the playlists it finished, behind one gate.

R-358's production half. A pass resolves each account playlist and acquires
nothing, ``intake missing --run`` lists what it found missing, ``acquire
download`` fetches that, and ``intake land`` writes one intake file. Only then
does an importable file exist, which is what ``sync/marks.py`` makes a rename
wait for. This verb is handed that file and is the one caller of
:func:`cratekit.sync.playlists.mark_swept`.

THE FILE NAMES THE PASS. ``intake missing --run`` names its list after the run,
``<run without colons>_synced``, and tells the person to land under that name,
so the intake file is ``<name>_inboxed.xml``. Nothing here is told a run
identifier. The name is read off the intake file, and the pass's jobs are the
ones whose own run spells that name, which is a comparison in the direction the
name was built and never an attempt to put the colons back.

ONLY A FINISHED PLAYLIST IS MARKED, AND THE JOB'S OWN REPORTS SAY WHAT FINISHED
MEANS. Each playlist of the pass has one intake job, and that job committed one
report per track: owned, suppressed, offered or missing. Every track the pass
did not find, the offered and the missing, is resolved against the library
again NOW, by the view ``acquire match`` uses. A playlist is planned only when
its job SUCCEEDED and every such track is LANDED, the intake file names the
file, OWNED, the library holds it and the file does not name it, or SUPPRESSED,
somebody has since deleted it on purpose and the pass itself never owed a
suppressed track. One track outstanding leaves the playlist alone with the
track named.

NOT THE MANIFEST, which the brief named and ``/code-review`` showed cannot
carry the decision. The manifest beside the pass's list is derived from these
reports and drops two kinds of track on the way: one the pass OFFERED for
review, which is never listed for download, and one it handed on to the text
list because the provider gave it no id. A playlist holding either would have
had no row owed and been marked DOWNLOADED over a track that is not in the
library. A manifest can also be another pass's, and a pass whose every missing
track was handed on has none at all. The reports are per playlist, are written
once and are what the manifest was made from, so they are read instead and the
verb takes no manifest.

A FILE OF NO PASS IS A PLAN OF NOTHING, NOT A REFUSAL, on the precedent
``intake land`` set for an empty folder: no playlist job on this library spells
the file's name, so there is nothing this verb could ever rename from it. That
is decided before the account is listed or a credential is asked for, the empty
plan is still gated, and the run ends NO_OP under a warning that says why.

THE PLAN IS SHOWN BEFORE ANYTHING IS RENAMED, and what runs after the answer is
the engine's own recheck against a second listing, so a playlist retitled or
removed since the plan is skipped and said, never forced.

A FAILURE PART WAY NAMES WHAT WAS MARKED. Each rename is its own write to the
account. A refusal the account raised keeps its reason, anything else is this
build's own defect and says so, and either way the message and detail carry the
playlists already renamed, which stay renamed.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, locations
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli, missing_cli
from cratekit.sync import cli as sync_cli
from cratekit.sync import marks, playlists, sources
from cratekit.write import rbxml

_ORIGIN = ("sync.mark",)

#: What a planned item carries, and what the apply turns it into.
MARK = "mark"
MARKED = "marked"
SKIP = "skip"

#: Why a playlist of the pass is not planned, one word each.
ALREADY_MARKED = "already-marked"
NOT_LISTED = "not-listed"
JOB_UNFINISHED = "job-unfinished"
#: The pass's own word for the label batch's ` LIBRARY` debris, read through
#: the enum so the two verbs cannot spell it two ways (R-361). A job for one
#: reaches the pass only from before the rule or by hand, and the source
#: system's throwaway is never renamed under it.
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
REPORTS_UNREADABLE = "reports-unreadable"
ROWS_OUTSTANDING = "rows-outstanding"
#: Why a planned playlist was not renamed after all: the engine's recheck.
CHANGED_SINCE = "changed-since-plan"

#: What the gate screen and the warning say about a file of no pass.
NO_PASS_SAID = (
    "no playlist job a sync pass queued on this library belongs to this file, so "
    "there is nothing to rename from it"
)

#: The three ways a track the pass did not find is no longer owed.
LANDED = "landed"
OWNED = "owned"
SUPPRESSED = "suppressed"

#: The report states that say the pass did not find the track in the library.
#: ``owned`` and ``suppressed`` are the other two, and neither was ever owed.
_NOT_FOUND = frozenset({"missing", "offered"})


def build_mark(parser, entry) -> None:
    del entry
    parser.add_argument(
        "--xml",
        required=True,
        metavar="XML",
        help="the intake file crate intake land wrote for the sync pass",
    )
    parser.set_defaults(_handler=sync_mark)


def _blocked(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-marks-blocked",
        message,
        steps=steps,
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail=detail,
    )


@dataclass
class _Playlist:
    """One playlist of the pass, and whether the landed file finishes it."""

    identity: str
    name: str
    job: jobs.Job
    wanted: tuple[match.Wanted, ...] = ()
    settled: dict[str, int] = field(
        default_factory=lambda: {LANDED: 0, OWNED: 0, SUPPRESSED: 0}
    )
    outstanding: list[dict[str, str]] = field(default_factory=list)
    reason: str | None = None
    why: str = ""

    @property
    def planned(self) -> bool:
        return self.reason is None


def _pass_name(xml: Path) -> str:
    """The name the pass's list, batch and intake file share, read off the file."""
    # RETIRED OR NOT (R-501). ``intake imported`` renames the file once the
    # import is proven, and a person who proved it before marking passes that
    # name. It is the same file and it names the same pass.
    written = land_cli.unretired_name(xml.name)
    if not written.endswith(land_cli.INTAKE_SUFFIX) or written == land_cli.INTAKE_SUFFIX:
        raise _blocked(
            f"{xml.name} is not named as an intake file, so it does not say which "
            f"sync pass it landed and nothing can be marked from it",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return written[: -len(land_cli.INTAKE_SUFFIX)]


def _comparable(path: str | Path) -> str:
    """A path as both sides spell it, THROUGH THE FILESYSTEM and then the form.

    Resolved first, which is what ``landing._file_labels`` does for the same
    question, because a library root reached through a link spells every landed
    file one way in the intake file and another in the index.
    """
    return locations.norm_for_compare(str(Path(path).resolve()))


def _locations(xml: Path) -> frozenset[str]:
    """Every local file the intake file names, comparable to a path off the disk."""
    try:
        content = xml.read_bytes()
    except OSError as exc:
        raise _blocked(
            f"{xml.name} could not be read ({exc.strerror or exc}), so what it landed "
            f"is unknown and nothing was marked",
            "write the importable file, then mark the remote side",
            path=str(xml),
        ) from exc
    named: set[str] = set()
    for track in rbxml.collection_tracks(content):
        recorded = rbxml.attributes(content, track).get("Location") or ""
        if not recorded:
            continue
        try:
            named.add(_comparable(locations.location_to_path(recorded)))
        except locations.LocationDecodeError:
            # A location on another host is not a file this landing put here,
            # so it is nothing a track could have landed as. Passed over, and
            # never a traceback out of a verb whose failures are refusals.
            continue
    if not named:
        raise _blocked(
            f"{xml.name} names no track on this machine, so it is not an intake file "
            f"a landing wrote and nothing was marked",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return frozenset(named)


def _pass_jobs(store, cfg: config.Config, name: str, handler_key: str) -> list[jobs.Job]:
    """The playlist jobs of the pass the intake file is named after, oldest first."""
    return sorted(
        (
            job
            for job in playlists.source_jobs(store, cfg, handler_key=handler_key)
            if missing_cli.synced_name(str((job.payload or {}).get(missing_cli.RUN_ID) or ""))
            == name
        ),
        key=lambda job: (job.created, job.job_id),
    )


def _spelled(wanted: match.Wanted) -> str:
    return f"{wanted.artist} - {wanted.title}" + (f" ({wanted.version})" if wanted.version else "")


_WHY = {
    NOT_LISTED: "the account no longer lists it, so there is no name to prefix",
    ALREADY_MARKED: "its name already carries the prefix",
    LABEL_DEBRIS: (
        "its name is the source system's label run debris, which a sync never "
        "offers and never renames"
    ),
    JOB_UNFINISHED: "its intake job did not succeed, so its tracks were never all resolved",
}


def _decided(store, sweep: playlists.Sweep, found: list[jobs.Job]) -> list[_Playlist]:
    """Every playlist of the pass, with the cheap reasons decided and the rest's
    unfound tracks read off their reports. Nothing here walks the library."""
    listed = sweep.names()
    latest: dict[str, jobs.Job] = {}
    for job in found:
        identity = playlists.playlist_of(job)
        if identity:
            latest[identity] = job
    decided: list[_Playlist] = []
    for identity, job in latest.items():
        entry = _Playlist(identity=identity, name=listed.get(identity, ""), job=job)
        decided.append(entry)
        if not entry.name:
            entry.reason = NOT_LISTED
        elif playlists.is_swept_name(entry.name):
            entry.reason = ALREADY_MARKED
        elif playlists.is_library_debris(entry.name):
            entry.reason = LABEL_DEBRIS
        elif job.state is not jobs.JobState.SUCCEEDED:
            entry.reason = JOB_UNFINISHED
        if entry.reason is not None:
            entry.why = _WHY[entry.reason]
            continue
        try:
            reports = missing_cli.job_reports(store, job)
        except CratekitError as exc:
            # UNREAD IS NOT NOTHING OWED. A playlist whose reports cannot be
            # read is one this run cannot say is finished, so it is left alone.
            entry.reason = REPORTS_UNREADABLE
            entry.why = exc.cause.message
            continue
        entry.wanted = tuple(
            intake_cli.thawed(report["track"])
            for report in reports
            if report["state"] in _NOT_FOUND
        )
    return decided


def _settle(decided: list[_Playlist], named: frozenset[str], cfg: config.Config) -> None:
    """Resolve every track the pass did not find, against the library as it is now.

    THE LIBRARY IS WALKED ONLY WHEN SOMETHING ASKS. A second run over a pass
    that is wholly marked, or a pass whose every track was owned, has nothing
    to resolve, and the walk is every file on the music volume.

    THE VIEW IS ``acquire match``'s OWN, tombstones included, so a track is
    owned here by the rule that called it missing. A track that is close and not
    exact is OUTSTANDING, since whether that file is the record is a person's
    to say. The review store is NOT consulted, so a track somebody has since
    accepted through review still holds its playlist back, which is recorded as
    a residual and errs on the side of not renaming.
    """
    asking = [entry for entry in decided if entry.planned and entry.wanted]
    if not asking:
        return
    index, suppresses, identify = match_cli.library_view(cfg)
    for entry in asking:
        for wanted in entry.wanted:
            found = match.resolve_one(
                wanted, index, suppresses=suppresses, suppression_id=identify
            )
            if found.state is match.MatchState.MATCHED:
                held = {_comparable(path) for path in found.paths}
                entry.settled[LANDED if held & named else OWNED] += 1
            elif found.state is match.MatchState.SUPPRESSED:
                entry.settled[SUPPRESSED] += 1
            else:
                entry.outstanding.append(
                    {
                        "id": wanted.ref,
                        "track": _spelled(wanted),
                        "why": f"{found.state}, {found.why}",
                    }
                )
        if entry.outstanding:
            entry.reason = ROWS_OUTSTANDING
            entry.why = (
                f"{len(entry.outstanding)} track(s) the pass did not find are still not "
                f"in the library: "
                + "; ".join(f"{row['track']} ({row['why']})" for row in entry.outstanding)
            )


def _item(entry: _Playlist) -> dict[str, Any]:
    base: dict[str, Any] = {"id": entry.identity, "name": entry.name, "job_id": entry.job.job_id}
    if entry.planned:
        return {**base, "action": MARK, "to": playlists.SWEPT_PREFIX + entry.name, **entry.settled}
    return {
        **base,
        "action": SKIP,
        "reason": entry.reason,
        "why": entry.why,
        "outstanding": list(entry.outstanding),
    }


def _payload(decided: list[_Playlist], *, xml: Path, seen) -> dict[str, Any]:
    items = [_item(entry) for entry in decided]
    identity = {
        "kind": "sync-mark",
        "xml": str(xml),
        # THE ONE STAT ``marks.require_output`` TOOK. A file rewritten since the
        # person was shown the plan is another landing, and its size and time
        # move with it.
        "xml_size": seen.st_size,
        "xml_mtime_ns": seen.st_mtime_ns,
        "marks": sorted((item["id"], item["to"]) for item in items if item["action"] == MARK),
    }
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            MARK: sum(1 for item in items if item["action"] == MARK),
            SKIP: sum(1 for item in items if item["action"] == SKIP),
        },
        "chunk": None,
    }


def _shown(payload: dict[str, Any], *, xml: Path) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    shown: dict[str, Any] = {
        "intake file": str(xml),
        "renamed on the account": [
            f"{item['name']} -> {item['to']}"
            for item in payload["items"]
            if item["action"] == MARK
        ],
        "left alone": [
            f"{item['name'] or item['id']}: {item['why']}"
            for item in payload["items"]
            if item["action"] == SKIP
        ],
    }
    if not payload["items"]:
        shown["nothing to rename"] = NO_PASS_SAID
    return shown


def _failed_part_way(
    exc: Exception, landed: list[str], names: dict[str, str], planned: list[str]
) -> CratekitError:
    """The failure, with what was already marked named in it.

    A REFUSAL THE ACCOUNT RAISED KEEPS ITS REASON AND ITS REMEDY. The adapter
    turns its provider's failures into causes itself, so anything else arriving
    here is this build's own defect, and calling that a provider outage would
    send a person to retry against a bug.
    """
    marked = [names.get(identity, identity) for identity in landed]
    said = (
        f"{len(marked)} playlist(s) were marked before this failed and stay marked: "
        + ", ".join(marked)
        if marked
        else "no playlist was marked before this failed"
    )
    detail = {
        "marked": list(landed),
        "unmarked": [identity for identity in planned if identity not in landed],
    }
    again = "run crate sync mark again; a marked playlist is skipped by its name"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.SOURCE,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{said}. The mark step failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def sync_mark(ctx) -> Envelope:
    cfg = sync_cli._load()
    xml = Path(ctx.args.xml)
    # THE FILE FIRST, before the account is listed or a credential is asked
    # for, by the same single read the engine makes again before it renames.
    seen = marks.require_output(xml)
    name = _pass_name(xml)
    named = _locations(xml)

    spec = next(one for one in sources.SPECS if one.source_id == playlists.SOURCE_ID)
    handler_key = str(spec.handler_key)
    with jobs.open_store() as store:
        found = _pass_jobs(store, cfg, name, handler_key)
    if not found:
        # BEFORE THE LISTING AND THE CREDENTIAL. Neither can change the answer,
        # and a person with no session stored is owed "this file is no pass's"
        # rather than "log in" followed by it.
        payload = _payload([], xml=xml, seen=seen)
        ctx.gate.require(
            ctx.entry.gates[0], digest=payload["digest"], context=_shown(payload, xml=xml)
        )
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "sync-mark-no-pass", "message": f"{xml.name}: {NO_PASS_SAID}"}],
        )

    from cratekit.label import catalogue

    catalogue_found = catalogue.resolve(cfg)
    with jobs.open_store() as store:
        sweep = playlists.marking_sweep(store, cfg, catalogue_found, handler_key=handler_key)
        decided = _decided(store, sweep, found)
    _settle(decided, named, cfg)

    payload = _payload(decided, xml=xml, seen=seen)
    option = ctx.gate.require(
        ctx.entry.gates[0], digest=payload["digest"], context=_shown(payload, xml=xml)
    )
    planned = [entry.identity for entry in decided if entry.planned]
    if option != "apply" or not planned:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    from cratekit.modules.outbound import account

    remote = account.resolve(cfg)
    landed: list[str] = []
    try:
        playlists.mark_swept(
            sweep,
            catalogue_found,
            remote,
            local_output=xml,
            applied=landed,
            only=frozenset(planned),
        )
    except Exception as exc:
        raise _failed_part_way(exc, landed, sweep.names(), planned) from exc

    items: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for item in payload["items"]:
        if item["action"] != MARK:
            items.append(item)
        elif item["id"] in landed:
            items.append({**item, "action": MARKED})
        else:
            items.append(
                {
                    **item,
                    "action": SKIP,
                    "reason": CHANGED_SINCE,
                    "why": (
                        "the account lists it under another name, or not at all, "
                        "since the plan was shown, so it was not renamed"
                    ),
                }
            )
            warnings.append(
                {
                    "code": "sync-mark-changed-since-plan",
                    "message": f"{item['name']} changed on the account since the plan "
                    f"was shown and was not renamed",
                }
            )
    totals = {
        "count": len(items),
        MARKED: len(landed),
        SKIP: sum(1 for item in items if item["action"] == SKIP),
    }
    return ctx.envelope(
        data={**payload, "items": items, "totals": totals},
        outcome=Outcome.OK if landed else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = ["build_mark", "sync_mark"]
