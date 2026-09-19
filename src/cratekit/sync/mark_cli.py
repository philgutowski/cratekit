"""``sync.mark``: a landed sync pass marks the playlists it finished, behind one gate.

R-358's production half. A pass resolves each account playlist and acquires
nothing, ``intake missing --run`` lists what it found missing, ``acquire
download`` fetches that, and ``intake land`` writes one intake file. Only then
does an importable file exist, which is what ``sync/marks.py`` makes a rename
wait for. This verb is handed that file and is the one caller of
:func:`cratekit.sync.playlists.mark_swept`.

THE FILE NAMES THE PASS. ``intake missing --run`` names its list after the run,
``<run without colons>_synced``, and tells the person to land under that name,
so the intake file is ``<name>_inboxed.xml`` and the provenance sidecar is
``<name>.manifest.json`` under download staging. Nothing here is told a run
identifier. The name is read off the intake file, and the pass's jobs are the
ones whose own run spells that name, which is a comparison in the direction the
name was built and never an attempt to put the colons back.

ONLY A FINISHED PLAYLIST IS MARKED. The manifest lists every track the pass
found missing, each under the playlists that asked for it. A playlist is
planned only when its job SUCCEEDED and every manifest row that names it now
resolves to a file in the library, LANDED when the intake file names that file
and OWNED when it does not. A playlist with one row outstanding is shown with
the row and left alone. A playlist the pass found nothing missing on has no
rows, and nothing owed is everything landed.

THE PLAN IS SHOWN BEFORE ANYTHING IS RENAMED, and what runs after the answer is
the engine's own recheck against a second listing, so a playlist retitled or
removed since the plan is skipped and said, never forced.

A FILE OF NO PASS IS A PLAN OF NOTHING, NOT A REFUSAL, on the precedent
``intake land`` set for an empty folder: no playlist job on this library spells
the file's name, so there is nothing this verb could ever rename from it. That
is decided before the manifest is read, the account is listed or a credential
is asked for, the empty plan is still gated, and the run ends NO_OP under a
warning that says why. A pass that HAS jobs and no readable manifest refuses,
because there something is owed and what is unknown.

A FAILURE PART WAY NAMES WHAT WAS MARKED. Each rename is its own write to the
account. The refusal keeps the reason the rename failed with, and its message
and detail carry the playlists already renamed, which stay renamed.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, locations
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
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
ROWS_OUTSTANDING = "rows-outstanding"
#: Why a planned playlist was not renamed after all: the engine's recheck.
CHANGED_SINCE = "changed-since-plan"

#: What the gate screen and the warning say about a file of no pass.
NO_PASS_SAID = (
    "no playlist job a sync pass queued on this library belongs to this file, so "
    "there is nothing to rename from it"
)

#: The two ways a manifest row is no longer owed.
LANDED = "landed"
OWNED = "owned"


def build_mark(parser, entry) -> None:
    del entry
    parser.add_argument(
        "--xml",
        required=True,
        metavar="XML",
        help="the intake file crate intake land wrote for the sync pass",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        metavar="JSON",
        help=(
            "the manifest crate intake missing --run wrote beside the pass's list "
            "(default: the one under download staging named after the intake file)"
        ),
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
    landed: list[str] = field(default_factory=list)
    owned: list[str] = field(default_factory=list)
    outstanding: list[dict[str, str]] = field(default_factory=list)
    reason: str | None = None

    @property
    def planned(self) -> bool:
        return self.reason is None


def _pass_name(xml: Path) -> str:
    """The name the pass's list, batch and intake file share, read off the file."""
    if not xml.name.endswith(land_cli.INTAKE_SUFFIX) or xml.name == land_cli.INTAKE_SUFFIX:
        raise _blocked(
            f"{xml.name} is not named as an intake file, so it does not say which "
            f"sync pass it landed and nothing can be marked from it",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return xml.name[: -len(land_cli.INTAKE_SUFFIX)]


def _locations(xml: Path) -> frozenset[str]:
    """Every file the intake file names, comparable to a path read off the disk."""
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
        if recorded:
            named.add(locations.norm_for_compare(locations.location_to_path(recorded)))
    if not named:
        raise _blocked(
            f"{xml.name} names no track, so it is not an intake file a landing wrote "
            f"and nothing was marked",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return frozenset(named)


def _manifest(path: Path) -> tuple[str, tuple[listdoc.ManifestRow, ...]]:
    """The manifest's fingerprint and rows, FROM ONE READ, or the refusal."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise _blocked(
            f"the manifest {path} could not be read ({exc.strerror or exc}), so which "
            f"tracks the pass still owed is unknown and nothing was marked",
            "list the pass with crate intake missing --run RUN_ID, or name its "
            "manifest with --manifest",
            manifest=str(path),
        ) from exc
    try:
        rows = listdoc.manifest_rows(raw, path)
    except listdoc.ListDocRefused as exc:
        raise _blocked(
            f"{exc}, so nothing was marked",
            "name the manifest crate intake missing --run wrote with --manifest",
            manifest=str(path),
        ) from exc
    return hashlib.sha256(raw).hexdigest(), rows


def _pass_jobs(store, cfg: config.Config, name: str, handler_key: str) -> list[jobs.Job]:
    """The playlist jobs of the pass the intake file is named after, oldest first."""
    found = sorted(
        (
            job
            for job in playlists.source_jobs(store, cfg, handler_key=handler_key)
            if missing_cli.synced_name(str((job.payload or {}).get(missing_cli.RUN_ID) or ""))
            == name
        ),
        key=lambda job: (job.created, job.job_id),
    )
    return found


def _asked_by(row: listdoc.ManifestRow) -> tuple[str, ...]:
    """Every playlist that asked for the row. ``source_refs`` when several did."""
    several = row.provenance.source_refs
    if several:
        return tuple(several)
    return (row.provenance.source_ref,) if row.provenance.source_ref else ()


def _spelled(row: listdoc.ManifestRow) -> str:
    version = str(row.track.get("version") or "")
    said = f"{row.track.get('artist', '')} - {row.track.get('title', '')}"
    return said + (f" ({version})" if version else "")


def _settle(
    pending: list[_Playlist],
    rows: tuple[listdoc.ManifestRow, ...],
    named: frozenset[str],
    cfg: config.Config,
) -> None:
    """Class every manifest row the pass's playlists asked for, in place.

    THE LIBRARY VIEW IS ``acquire match``'s OWN, tombstones included, so a row
    is owned here by exactly the rule that called it missing in the first place.
    A row that is close and not exact, suppressed, or unreadable is OUTSTANDING:
    each is a track this run cannot say is in the library.
    """
    by_identity = {entry.identity: entry for entry in pending}
    wanted_rows = [row for row in rows if any(ref in by_identity for ref in _asked_by(row))]
    if not wanted_rows:
        return
    index, suppresses, identify = match_cli.library_view(cfg)
    for position, row in enumerate(wanted_rows, start=1):
        #: ``LANDED`` or ``OWNED`` when the row is no longer owed, else ``None``
        #: and ``why`` says what stands between it and the library.
        settled: str | None = None
        why = ""
        try:
            wanted = match.read_row(row.track, origin=match.TIDAL, position=position)
        except match.UnreadableList as exc:
            why = f"its manifest row could not be read ({exc})"
        else:
            found = match.resolve_one(
                wanted, index, suppresses=suppresses, suppression_id=identify
            )
            if found.state is match.MatchState.MATCHED:
                held = {locations.norm_for_compare(str(path)) for path in found.paths}
                settled = LANDED if held & named else OWNED
            else:
                why = f"{found.state}, {found.why}"
        for ref in _asked_by(row):
            entry = by_identity.get(ref)
            if entry is None:
                continue
            if settled == LANDED:
                entry.landed.append(row.ref)
            elif settled == OWNED:
                entry.owned.append(row.ref)
            else:
                entry.outstanding.append({"id": row.ref, "track": _spelled(row), "why": why})


def _decided(
    sweep: playlists.Sweep,
    found: list[jobs.Job],
    rows: tuple[listdoc.ManifestRow, ...],
    named: frozenset[str],
    cfg: config.Config,
) -> list[_Playlist]:
    """Every playlist of the pass, each planned or carrying the reason it is not."""
    listed = sweep.names()
    latest: dict[str, jobs.Job] = {}
    for job in found:
        identity = playlists._playlist_of(job)
        if identity:
            latest[identity] = job
    decided = [
        _Playlist(identity=identity, name=listed.get(identity, ""), job=job)
        for identity, job in latest.items()
    ]
    _settle(decided, rows, named, cfg)
    for entry in decided:
        if not entry.name:
            entry.reason = NOT_LISTED
        elif playlists.is_swept_name(entry.name):
            entry.reason = ALREADY_MARKED
        elif entry.job.state is not jobs.JobState.SUCCEEDED:
            entry.reason = JOB_UNFINISHED
        elif entry.outstanding:
            entry.reason = ROWS_OUTSTANDING
    return decided


_WHY = {
    NOT_LISTED: "the account no longer lists it, so there is no name to prefix",
    ALREADY_MARKED: "its name already carries the prefix",
    JOB_UNFINISHED: "its intake job did not succeed, so its tracks were never all resolved",
}


def _item(entry: _Playlist) -> dict[str, Any]:
    base: dict[str, Any] = {"id": entry.identity, "name": entry.name, "job_id": entry.job.job_id}
    if entry.planned:
        return {
            **base,
            "action": MARK,
            "to": playlists.SWEPT_PREFIX + entry.name,
            LANDED: len(entry.landed),
            OWNED: len(entry.owned),
        }
    why = _WHY.get(entry.reason or "") or (
        f"{len(entry.outstanding)} track(s) the pass listed for it are not in the "
        f"library: " + "; ".join(f"{row['track']} ({row['why']})" for row in entry.outstanding)
    )
    return {
        **base,
        "action": SKIP,
        "reason": entry.reason,
        "why": why,
        "outstanding": list(entry.outstanding),
    }


def _payload(
    decided: list[_Playlist],
    *,
    xml: Path,
    seen,
    manifest: Path | None,
    manifest_digest: str | None,
) -> dict[str, Any]:
    items = [_item(entry) for entry in decided]
    identity = {
        "kind": "sync-mark",
        "xml": str(xml),
        # THE ONE STAT ``marks.require_output`` TOOK. A file rewritten since the
        # person was shown the plan is another landing, and its size and time
        # move with it.
        "xml_size": seen.st_size,
        "xml_mtime_ns": seen.st_mtime_ns,
        "manifest": str(manifest) if manifest is not None else None,
        "manifest_bytes": manifest_digest,
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


def _shown(payload: dict[str, Any], *, xml: Path, manifest: Path | None) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    return {
        "intake file": str(xml),
        "manifest": str(manifest) if manifest is not None else NO_PASS_SAID,
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


def _unlisted_warning(manifest: Path) -> list[dict[str, str]]:
    """Say that handed on tracks exist, since no manifest row stands for them.

    ``intake missing`` writes a missing track it could give no provider id to a
    text list beside the manifest, under no playlist. This verb cannot tell
    which playlist such a track belongs to, so it cannot hold that playlist
    back, and it says so rather than letting the plan read as the whole truth.
    """
    if not manifest.name.endswith(listdoc.MANIFEST_SUFFIX):
        return []
    beside = manifest.with_name(
        manifest.name[: -len(listdoc.MANIFEST_SUFFIX)] + listdoc.UNLISTED_SUFFIX
    )
    if not beside.is_file():
        return []
    return [
        {
            "code": "sync-mark-unlisted-uncounted",
            "message": (
                f"{beside} holds missing tracks of this pass that no manifest row "
                f"stands for; they are not counted against any playlist here, so "
                f"read it before answering"
            ),
        }
    ]


def _failed_part_way(
    exc: BaseException, landed: list[str], names: dict[str, str], planned: list[str]
) -> CratekitError:
    """The rename's own refusal, with what was already marked named in it."""
    from cratekit.modules.outbound import account

    cause = account.provider_failure(exc, "retitle a playlist").cause
    marked = [names.get(identity, identity) for identity in landed]
    said = (
        f"{len(marked)} playlist(s) were marked before this failed and stay marked: "
        + ", ".join(marked)
        if marked
        else "no playlist was marked before this failed"
    )
    return refuse(
        cause.reason,
        f"{said}. {cause.message}",
        remedy=cause.remediation.remedy,
        steps=tuple(cause.remediation.steps)
        + ("run crate sync mark again; a marked playlist is skipped by its name",),
        scope=Scope.SOURCE,
        retryable=cause.retryable,
        origin=_ORIGIN,
        detail={
            **dict(cause.detail),
            "marked": list(landed),
            "unmarked": [identity for identity in planned if identity not in landed],
        },
        inner=cause,
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
        # BEFORE THE MANIFEST, THE LISTING AND THE CREDENTIAL. None of them can
        # change the answer, and a person with no session stored is owed "this
        # file is no pass's" rather than "log in" followed by it.
        payload = _payload([], xml=xml, seen=seen, manifest=None, manifest_digest=None)
        ctx.gate.require(
            ctx.entry.gates[0],
            digest=payload["digest"],
            context=_shown(payload, xml=xml, manifest=None),
        )
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "sync-mark-no-pass", "message": f"{xml.name}: {NO_PASS_SAID}"}],
        )

    manifest = (
        Path(ctx.args.manifest)
        if ctx.args.manifest
        else Path(cfg.paths.download_staging)
        / missing_cli.LISTS_DIR
        / f"{name}{listdoc.MANIFEST_SUFFIX}"
    )
    manifest_digest, rows = _manifest(manifest)

    from cratekit.label import catalogue

    catalogue_found = catalogue.resolve(cfg)
    with jobs.open_store() as store:
        sweep = playlists.marking_sweep(store, cfg, catalogue_found, handler_key=handler_key)

    decided = _decided(sweep, found, rows, named, cfg)
    payload = _payload(
        decided, xml=xml, seen=seen, manifest=manifest, manifest_digest=manifest_digest
    )
    warnings = _unlisted_warning(manifest)
    option = ctx.gate.require(
        ctx.entry.gates[0],
        digest=payload["digest"],
        context=_shown(payload, xml=xml, manifest=manifest),
    )
    planned = [entry.identity for entry in decided if entry.planned]
    if option != "apply" or not planned:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

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

    items = []
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
