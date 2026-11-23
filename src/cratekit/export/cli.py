"""``crate export playlist``: confirm, then queue the outbound write, then run it.

``handle`` is the per item worker behind ``export.playlist`` (U51). ONE ITEM IS
ONE TRACK, so a failed write redoes one track and an empty playlist is an empty
job; since U270 the driver hands :func:`handle_batch` a hundred at a time, added
in one request. THE CONFIRM DIGEST COVERS THE RESOLVED KEY, THE ABSOLUTE EXPORT
PATH AND THE TRACKS (R34), so a decision recorded against one collection
document authorises no other, and the resumed child, rebuilt from the frozen
payload, digests the same. ``outbound_export`` writes, ``source`` reads.

Layer: modules. Builders take an untyped ``entry`` so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import account, artifacts, kinds, ledger, shell, source
from cratekit.modules.outbound import export as outbound_export

#: The payload keys both outbound verbs freeze, spelled once in the shell,
#: whose resume reads them to rebuild the confirm digest.
PLAYLIST = shell.PLAYLIST
EXPORT = shell.EXPORT

#: The remote playlist's display name, frozen so the worker never rebuilds it
#: by splitting the key, which would create it under a name nobody chose.
NAME = "name"

#: The recorded ledger key this crate used to live under, frozen when the verb
#: recognised one and a person confirmed it (R-229); empty or absent is none.
ADOPTS = "adopts"

#: The remote playlist the gate showed this write landing on, or none for a
#: create: the worker finds the ledger record by it if the crate has moved.
REMOTE = "remote_id"
#: Where a playlist this export creates is filed, the Exports folder decision
#: :func:`kinds.token` spells, frozen and digested (U131); empty for no create.
FILING = "filing"
#: A playlist created and left at the account root, with the reason (U131).
UNFILED_WARNING = "export-playlist-unfiled"

#: What the confirm gate says the write will do to the account's playlists.
ACTION_CREATE = "create"
ACTION_UPDATE = "update"
ACTION_ADOPT = "adopt"

#: What an unmatched row is said to be when the account gave no reason (R-850).
NO_MATCH = shell.NO_MATCH

#: The warning a finished export carries when any of its tracks went unwritten.
UNMATCHED_WARNING = "export-tracks-unmatched"


def summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What this job's committed artifacts say it wrote, in one summary.

    READ OFF DISK, so a job driven over two sessions counts each item once.
    ``unmatched_tracks`` names every track left out with its reason (R-850);
    ``reasons`` only those the account said something about.
    """
    added: list[str] = []
    already: list[str] = []
    reasons: list[str] = []
    left_out: list[dict[str, str]] = []
    unfiled: list[str] = []
    for report in artifacts.committed(cfg, job_id):
        if report.get("unfiled"):
            unfiled.append(str(report["unfiled"]))
        added.extend(str(item) for item in report.get("added") or ())
        already.extend(str(item) for item in report.get("already") or ())
        for item in report.get("unmatched") or ():
            # ONE ROW BUILT ONCE, the identity and the reason read off it, so
            # the lists cannot disagree; a reason only for a row the account
            # said something about (R-356), named as the library shows it.
            listed = _left_out(item)
            left_out.append(listed)
            if _said(item):
                reasons.append(
                    f"{listed['artist']} - {listed['title']} "
                    f"(row {listed['identity']}): {listed['reason']}"
                )
    unmatched = [listed["identity"] for listed in left_out]
    return {
        "added": added,
        "already": already,
        "unmatched": unmatched,
        "reasons": reasons,
        "counts": {"written": len(added), "already": len(already), "unmatched": len(unmatched)},
        "unmatched_tracks": left_out,
        "unfiled": unfiled,
    }


def _said(row: Any) -> str:
    """What the account said about one unmatched row, or empty when nothing."""
    said = str(row.get("reason") or "") if isinstance(row, dict) else ""
    return "" if said == "unmatched" else said


def _left_out(row: Any) -> dict[str, str]:
    """One unmatched row as the answer lists it, named as the library shows it."""
    named = row if isinstance(row, dict) else {}
    return {
        "identity": str(row.get("identity") or "") if isinstance(row, dict) else str(row),
        "artist": str(named.get("artist") or ""),
        "title": str(named.get("title") or ""),
        "reason": _said(row) or NO_MATCH,
    }


def concluded(outbound: Mapping[str, Any]) -> tuple[dict[str, str], ...]:
    """The warnings a finished export carries when it left tracks out or unfiled.

    THE OUTCOME STAYS ``ok`` (R-850): any other needs a cause and a non zero exit,
    reading a job with nothing to retry as failed.
    """
    said = tuple(
        {"code": UNFILED_WARNING, "message": (
            f"the remote playlist was written and left at the account root, not "
            f"filed in the {outbound_export.KIND} folder: {reason}. crate "
            f"organize files it on its next pass"
        )}
        for reason in outbound.get("unfiled") or ()
    )
    tally = shell.unmatched_tally(outbound)
    if tally is None:
        return said
    missed, total = tally
    # "WERE NOT WRITTEN", NOT "ARE NOT ON THE PLAYLIST": a track counted as
    # already there may be counted off the ledger rather than the account (R-855).
    message = (
        f"{missed} of the {total} track(s) in this export were not written "
        f"to the remote playlist, because the provider could not match "
        f"them; each is listed with its reason in this answer"
    )
    return ({"code": UNMATCHED_WARNING, "message": message}, *said)


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("playlist", help="stable identifier of the library playlist")
    parser.add_argument(
        "--job", metavar="JOB_ID", help="continue the export already queued under this identifier"
    )
    parser.add_argument(
        "--export",
        metavar="EXPORT",
        help=(
            "the rekordbox collection export holding the playlist to write; the "
            "live database is never read"
        ),
    )
    parser.add_argument(
        "--new-playlist",
        action="store_true",
        help=(
            "create a new remote playlist even when a recorded one looks like "
            "this playlist under an earlier name or folder"
        ),
    )
    parser.set_defaults(_handler=export_playlist)


def confirm_digest(
    playlist_key: str, export_path: str, tracks: Sequence[str], *, adopts="", filing=""
) -> str:
    """The identity the confirm decision is recorded against, for enqueue and resume alike.

    ``adopts`` (R-229) and ``filing`` (U131) change where the tracks go, and each
    JOINS ONLY WHEN SET, so a job frozen by an older build still resumes.
    """
    covered: dict[str, Any] = {
        "kind": "export.playlist",
        "playlist": playlist_key,
        "export": export_path,
        # THE TRACK SET, not just the file it came from.
        "tracks": list(tracks),
    }
    if adopts:
        covered["adopts"] = adopts
    if filing:
        covered["filing"] = filing
    return digest_of(covered)


def _frozen_adoption(payload) -> dict[str, str]:
    """The digest's fourth input, read off a frozen payload for the resume."""
    extra = {"adopts": str(payload.get(ADOPTS) or "")}
    if payload.get(FILING):
        extra["filing"] = str(payload[FILING])
    return extra


def planned_filing(cfg: config.Config, found: ledger.Recognition) -> str:
    """The Exports folder decision for a write that creates, read before the gate (U131).

    Empty for a recorded playlist. AN ACCOUNT THAT CANNOT BE READ PLANS NO FILING:
    the write refuses with its own cause, and a playlist left at the root is warned of.
    """
    if found.own_remote_id or found.adopts:
        return ""
    try:
        root = account.resolve(cfg).folders()
    except CratekitError:
        return ""
    return kinds.token(kinds.decide(cfg, outbound_export.KIND, root))


def recognition_warnings(
    resolved: source.ResolvedPlaylist, found: ledger.Recognition
) -> tuple[dict[str, str], ...]:
    """What a person is told about the remote playlist, AT MOST ONE warning (R-229).

    An adoption, with how to decline it; an ambiguity, which creates; a mismatch.
    """
    if found.adopts:
        evidence = (
            f"which was last written from {found.recorded} track(s), "
            f"{found.shared} of them among the {found.crate} this playlist holds"
            if found.recorded
            else "which was recorded under the same name before this build "
            "recorded what a playlist holds"
        )
        code, message = "outbound-playlist-adopted", (
            f"{resolved.key!r} has no recorded remote playlist, and "
            f"{found.adopts!r} has one and is no longer in this export, "
            f"{evidence}. This write updates that remote playlist "
            f"{found.remote_id} rather than creating a second one. Pass "
            f"--new-playlist to create a new one instead"
        )
    elif found.ambiguous:
        code, message = "outbound-playlist-adoption-ambiguous", (
            f"{resolved.key!r} has no recorded remote playlist, and "
            f"{len(found.candidates)} recorded playlists that are no "
            f"longer in this export could each be it: "
            f"{', '.join(found.candidates)}. None is adopted, so this "
            f"write creates a new remote playlist"
        )
    elif found.mismatched:
        elsewhere = (
            f" It looks like the playlist now at {', '.join(found.claimed_by)}, "
            f"and exporting that one first moves the remote playlist to it and "
            f"leaves this one free to get its own"
            if found.claimed_by
            else ""
        )
        code, message = "outbound-playlist-record-mismatch", (
            f"the remote playlist {found.own_remote_id} recorded for "
            f"{resolved.key!r} was last written from a playlist that "
            f"shared fewer than half its tracks with this one, so it may "
            f"belong to a playlist that has since been renamed. This "
            f"write updates it anyway.{elsewhere}"
        )
    else:
        return ()
    return ({"code": code, "message": message},)


def shown_playlist(
    found: ledger.Recognition, warnings: tuple[dict[str, str], ...]
) -> dict[str, Any]:
    """What the confirm gate shows about the REMOTE playlist this write lands on.

    SHOWN EVERY TIME, its warning too, since the gate's refusal carries none.
    """
    if found.own_remote_id:
        block: dict[str, Any] = {"action": ACTION_UPDATE, "remote_id": found.own_remote_id}
    elif found.adopts:
        block = {"action": ACTION_ADOPT, "remote_id": found.remote_id, "recorded_as": found.adopts}
    else:
        block = {"action": ACTION_CREATE, "remote_id": None}
    for warning in warnings:
        block["warning"] = warning["message"]
    return {"remote_playlist": block}


def export_argv(job) -> list[str]:
    """The command line that continues one queued export.

    IT CARRIES ``--run``, before the verb, so the respawned child names the run its
    explicit gate's decision was recorded against, and ``--export`` and the resolved
    key, so its digest matches. A job frozen without a gate run resumes without it.
    """
    payload = job.payload or {}
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    argv = [*resume, "export", "playlist", str(payload.get(PLAYLIST) or "")]
    exported = payload.get(EXPORT)
    if exported:
        argv += ["--export", str(exported)]
    return [*argv, "--job", job.job_id]


def export_playlist(ctx) -> Envelope:
    """Confirm this playlist, then queue it, or drive the job already queued."""
    spec = ctx.entry.gates[0]
    if ctx.args.job:
        return shell.resume(
            ctx, spec, ctx.args.job, digest=confirm_digest, summary=summary,
            frozen_extra=_frozen_adoption, concluded=concluded,
        )
    playlist = str(ctx.args.playlist or "")
    if not playlist:
        raise refuse(
            "export-playlist-unknown",
            "export playlist needs the library playlist identifier",
            steps=("pass the playlist identifier after the verb",),
            origin=("export.cli",),
        )
    # RESOLVED BEFORE THE GATE, so nobody confirms an export about to refuse,
    # and the configuration with it, since the age is judged by its limit (R-227).
    exported = source.required_path(getattr(ctx.args, "export", None))
    library = source.read_library(exported)
    resolved = source.resolve(library, playlist)
    cfg = shell.load_config("export.cli")
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
    # RECOGNISED BEFORE THE GATE (R-229), so the person confirms the playlist the
    # write lands on; ``--new-playlist`` takes the offer off the reading.
    found = ledger.recognise(
        cfg, resolved.key, name=resolved.name, track_ids=resolved.track_ids,
        live=source.playlist_contents(library),
    )
    if getattr(ctx.args, "new_playlist", False):
        found = found.without_offer()
    said = recognition_warnings(resolved, found)
    filing = planned_filing(cfg, found)
    # THE TRACKS THE DIGEST COVERS ARE SHOWN (R-693), as the resume shows them.
    digest = confirm_digest(
        resolved.key, str(exported), resolved.track_ids, adopts=found.adopts, filing=filing
    )
    option = ctx.gate.require(
        spec,
        plan={"digest": digest, "items": list(resolved.track_ids)},
        context={
            shell.PLAYLIST: resolved.key,
            shell.EXPORT_PATH: str(exported),
            ADOPTS: found.adopts,
            **({FILING: filing} if filing else {}),
            **shell.shown_export(age),
            **shown_playlist(found, said),
        },
    )
    if option == "abort":
        # THE DECLARED SHAPE, and nothing about the playlist: see ``shell.declined``.
        return ctx.envelope(data=shell.declined(), outcome=Outcome.NO_OP)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # THE GATE RUN IS FROZEN for the respawned child, see ``export_argv``.
            payload={
                PLAYLIST: resolved.key,
                NAME: resolved.name,
                EXPORT: str(exported),
                ADOPTS: found.adopts,
                REMOTE: found.own_remote_id or found.remote_id or None,
                FILING: filing,
                shell.TRACKS: list(resolved.track_ids),
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            # ONE TRACK IS ONE ITEM, or the driver reports an empty success.
            item_ids=resolved.track_ids,
            cfg=cfg,
        )
        data = shell.reported(store, job, cfg, summary)
        warnings = (*shell.queue_warnings(resolved, noun="track", age=age), *said)
        return ctx.envelope(data=data, warnings=warnings)


def run_export_item(payload: dict[str, Any], track_id: str, cfg: config.Config, remote) -> dict:
    """Write ONE library track to the remote playlist, and report what happened.

    Pure of the job engine; one item of :func:`run_export_items`, raising what it met.
    """
    outcome = (run_export_items(payload, (track_id,), cfg, remote) or {}).get(track_id)
    if isinstance(outcome, Exception):
        raise outcome
    if not isinstance(outcome, dict):
        raise refuse(
            "internal-error",
            f"the export of track {track_id!r} answered nothing for it",
            remedy=Remedy.REPORT_DEFECT,
            origin=("export", "cli"),
            detail={"track": track_id},
        )
    return outcome


def _absent(payload: Mapping[str, Any], track_id: str) -> CratekitError:
    return refuse(
        "outbound-item-absent",
        f"the export at {Path(str(payload[EXPORT])).name} no longer carries "
        f"track {track_id!r}, which this job queued, so there is nothing to "
        f"write for this item and nothing was written",
        steps=("export the collection again and queue a new export rather than resuming this one",),
        origin=("export", "cli"),
        detail={"track": track_id},
    )


def _refused(track: str, remote_id: str) -> CratekitError:
    """The cause ``add_to_playlist`` raised for a track the provider would not add (U270)."""
    return account.provider_failure(
        LookupError(f"the provider added nothing for the track {track!r}"),
        f"add the track {track} to the playlist {remote_id}",
    )


def run_export_items(
    payload: dict[str, Any],
    track_ids: Sequence[str],
    cfg: config.Config,
    remote,
    stop: Callable[[], bool] = lambda: False,
) -> dict[str, dict | Exception] | None:
    """Write several library tracks to the remote playlist in one add (U270).

    EACH TRACK IS PLANNED ON ITS OWN, so a missing row or refused match fails that
    track alone; the rest go in ONE :func:`apply`, whose raise is all their
    outcomes. A :class:`jobs.Parked` is raised. ``stop`` is asked between tracks,
    and when true nothing is written and None returned.
    """
    exported = Path(str(payload[EXPORT]))
    library = source.read_library(exported)
    shared = {
        "playlist_key": str(payload[PLAYLIST]),
        "name": str(payload.get(NAME) or payload[PLAYLIST]),
        "account": remote,
        "adopts": str(payload.get(ADOPTS) or ""),
        "expected": str(payload.get(REMOTE) or ""),
        # THE WHOLE CRATE, not this item. See ``ExportPlan.contents``.
        "contents": [str(track) for track in payload.get(shell.TRACKS) or ()],
        # THE EXPORT'S DATE, so a later prune can refuse an older export (R-836).
        "written": exported_on(exported, cfg),
        "filing": str(payload.get(FILING) or ""),
    }
    answered: dict[str, dict | Exception] = {}
    planned: dict[str, outbound_export.ExportPlan] = {}
    for track_id in track_ids:
        if stop():
            return None
        try:
            tracks = source.local_tracks(library, (track_id,), cfg=cfg)
            if not tracks:
                raise _absent(payload, track_id)
            planned[track_id] = outbound_export.plan(tracks, **shared)
        except jobs.Parked:
            raise
        except Exception as exc:  # noqa: BLE001 - this track's outcome
            answered[track_id] = exc
    if not planned:
        return answered
    together = replace(
        next(iter(planned.values())),
        matched=tuple(pair for one in planned.values() for pair in one.matched),
        unmatched=tuple(row for one in planned.values() for row in one.unmatched),
    )
    try:
        report = outbound_export.apply(cfg, remote, together)
    except jobs.Parked:
        raise
    except Exception as exc:  # noqa: BLE001 - every written track's outcome
        answered.update({track_id: exc for track_id in planned})
        return answered
    reported = False
    for track_id, one in planned.items():
        rows = {local for local, _remote in one.matched}
        mine = [row for row in report.outcomes if row[0] in rows]
        said = {
            kind: [remote_track for _local, remote_track, how in mine if how == kind]
            for kind in (outbound_export.REFUSED, outbound_export.ADDED, outbound_export.ALREADY)
        }
        refused = said[outbound_export.REFUSED]
        if refused:
            answered[track_id] = _refused(refused[0], report.remote_id)
            continue
        # WHAT THE APPLY DID ONCE IS SAID ONCE, on the first track reported.
        first_said = not reported
        reported = True
        answered[track_id] = {
            "track": track_id,
            "playlist_key": report.playlist_key,
            "remote_id": report.remote_id,
            "created": report.created and first_said,
            "adopted_from": report.adopted_from if first_said else "",
            "unfiled": report.unfiled if first_said else "",
            "added": said[outbound_export.ADDED],
            "already": said[outbound_export.ALREADY],
            "unmatched": [
                {
                    "identity": row.identity,
                    "title": row.title,
                    "artist": row.artist,
                    "reason": row.reason,
                }
                for row in one.unmatched
            ],
        }
    return answered


def exported_on(path: Path, cfg: config.Config) -> str:
    """The collection export's date as ISO text, or empty when it cannot be read."""
    written = source.export_age(path, limit_days=cfg.outbound.export_stale_days).written
    return written.isoformat() if written is not None else ""


def handle(job, item, cfg) -> jobs.Produced:
    """Export one queued track. The per item worker behind ``export.playlist``.

    THE ITEM NAMES THE TRACK, not the payload; ``cfg`` is the frozen configuration
    (KTD9); the account is resolved at call time through the module attribute.
    """
    payload = dict(job.payload or {})
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
    return artifacts.produced(cfg, job, item, report)


#: How many queued tracks the driver hands :func:`handle_batch` at once (U270).
BATCH = outbound_export.BATCH


def handle_batch(job, items, cfg, stop) -> dict[str, jobs.Produced | Exception]:
    """Export up to :data:`BATCH` queued tracks in one add, :func:`handle`'s batch form.

    Each item gets the artifact or failure :func:`handle` would give it.
    """
    payload = dict(job.payload or {})
    answered = run_export_items(
        payload, [str(item.item_id) for item in items], cfg, account.resolve(cfg), stop
    )
    if answered is None:
        return {}
    outcomes: dict[str, jobs.Produced | Exception] = {}
    for item in items:
        got = answered.get(str(item.item_id))
        if got is None:
            # LEFT FOR THE DRIVER, which fails an item given no outcome.
            continue
        try:
            outcomes[item.item_id] = (
                got if isinstance(got, Exception) else artifacts.produced(cfg, job, item, got)
            )
        except Exception as exc:  # noqa: BLE001 - this item's outcome
            outcomes[item.item_id] = exc
    return outcomes


#: The driver hands this worker several items at once (U270), see
#: :data:`cratekit.cli.handlers.BATCH_ATTRIBUTE`.
handle.batched = (handle_batch, BATCH)  # type: ignore[attr-defined]


__all__ = [
    "NO_MATCH", "FILING", "UNFILED_WARNING", "UNMATCHED_WARNING", "build", "concluded",
    "confirm_digest", "export_argv", "export_playlist", "BATCH", "handle", "handle_batch",
    "recognition_warnings", "run_export_item", "run_export_items", "shown_playlist", "summary",
]
