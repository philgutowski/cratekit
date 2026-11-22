"""``crate sync favorites``: confirm the remote half, queue it, then run it.

``handle`` is the per item worker behind ``sync.favorites``, the caller of the
add only ``hearts.heart_back``. A favourite is a member of the named playlist
unioned with every pink row, read from a read only open of the live database
(R-228); a pink row the export lacks is named beside dangling.

**NO LOCAL WRITE HAPPENS HERE, AND NOTHING SAYS OTHERWISE (R-424)**: ``colors``
is ``None`` and :data:`LOCAL_WRITE_WARNING` says so where a person reads it.
**ADD ONLY IS A PROPERTY OF THE TYPE**: ``RemoteAccount`` declares no remove.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, rb_writer
from cratekit.core.cause import Outcome, refuse
from cratekit.favorites import colour, placeholders
from cratekit.modules.outbound import hearts, shell, source

#: The two payload keys both outbound verbs freeze, spelled in ``outbound.shell``.
PLAYLIST = shell.PLAYLIST
EXPORT = shell.EXPORT

#: The quarterly placeholder playlists this source owns, spelled in ``placeholders``.
PLACEHOLDER_NAME = placeholders.PLACEHOLDER_NAME
BACKLOG = placeholders.BACKLOG
placeholder_name = placeholders.placeholder_name

#: What every pass of this verb tells a person about the LOCAL half (R-424): a
#: standing condition, on the warning channel because the default renderer has
#: no case for a ``job_state/1`` payload. Read by ``crate sync all`` too, and it
#: names its subject, since there it prints beside sources that do write.
LOCAL_WRITE_WARNING: dict[str, str] = {
    "code": "favorites-local-write-unbound",
    "message": (
        "the favourites sweep hearts matching tracks on the streaming service "
        "and changes nothing in the library: it writes no colour, no Favorite "
        "tag and no playlist membership locally"
    ),
}


def local_write_warning() -> tuple[dict[str, str], ...]:
    """:data:`LOCAL_WRITE_WARNING` as a warnings tuple, a COPY per call so no caller mutates it."""
    return (dict(LOCAL_WRITE_WARNING),)


#: The Pink lookup lives in ``favorites.colour`` (U153); the names stay here too.
PINK_COLOUR_NAME = colour.PINK_COLOUR_NAME
PINK_COLOUR_MISSING = colour.PINK_COLOUR_MISSING
pink_colour_id = colour.pink_colour_id
pink_content_ids = colour.pink_content_ids


def read_pink_track_ids(cfg: config.Config) -> tuple[str, ...]:
    """Pink content ids from a read only open of the configured library.

    THE READ'S OWN REFUSAL PROPAGATES (R-228), so the playlist alone never
    reports complete over colour the sweep never saw.
    """
    with rb_writer.read_only_copy(rb_writer.live_db_path(cfg), cfg=cfg) as db:
        return pink_content_ids(db)


def union_with_pink(
    library: source.Library,
    playlist: source.ResolvedPlaylist,
    pink_ids: Sequence[str],
) -> source.ResolvedPlaylist:
    """Playlist members union pink rows that the export carries, deduplicated, playlist order first.

    Pink rows the export lacks are named on ``pink_missing`` and left out.
    ``from_playlist`` and ``from_colour`` count each source's candidates, so a
    row in both is counted in both and queued once.
    """
    missing: list[str] = []
    in_export: list[str] = []
    for track_id in pink_ids:
        if track_id in library.entries:
            in_export.append(track_id)
        else:
            missing.append(track_id)
    seen: set[str] = set()
    kept: list[str] = []
    for track_id in playlist.track_ids:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    for track_id in in_export:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    return replace(
        playlist,
        track_ids=tuple(kept),
        from_playlist=len(playlist.track_ids),
        from_colour=len(in_export),
        pink_missing=tuple(missing),
    )


def sweep_source_facts(resolved: source.ResolvedPlaylist) -> dict[str, Any]:
    """The colour and playlist counts the gate shows beside the digest (R-228)."""
    facts: dict[str, Any] = {
        "from_playlist": resolved.from_playlist,
        "from_colour": resolved.from_colour,
    }
    if resolved.pink_missing:
        facts["pink_missing"] = list(resolved.pink_missing)
    return facts


#: What an unmatched favourite is said to be when the account gave no reason
#: (R-856), spelled in the shell so the export says the same.
NO_MATCH = shell.NO_MATCH

#: The warning a finished sweep carries when any favourite went unhearted.
UNMATCHED_WARNING = "favorites-hearts-unmatched"


def summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What this sweep's committed artifacts say it wrote, per committed item.

    ``already`` tells a sweep with nothing to do from one that did nothing.
    COUNTED, AND EVERY UNMATCHED FAVOURITE LISTED (R-856), since the default
    renderer prints an outbound summary only when it carries ``counts``; the
    count keys are this verb's own, and ``unmatched_tracks`` is the export's
    shape, a row the account said nothing about included.
    """
    from cratekit.modules.outbound import artifacts

    hearted: list[str] = []
    already: list[str] = []
    unmatched: list[str] = []
    reasons: list[str] = []
    left_out: list[dict[str, str]] = []
    for report in artifacts.committed(cfg, job_id):
        hearted.extend(str(item) for item in report.get("hearted") or ())
        already.extend(str(item) for item in report.get("already") or ())
        unmatched.extend(str(item) for item in report.get("unmatched") or ())
        # One sentence per favourite the account would not choose a release for (R-356).
        said = [one for one in report.get("reasons") or () if isinstance(one, dict)]
        reasons.extend(
            f"{one.get('artist') or ''} - {one.get('title') or ''} "
            f"(row {one.get('row') or ''}): {one.get('reason') or ''}"
            for one in said
        )
        left_out.extend(_left_out(report, said))
    return {
        "hearted": hearted,
        "already": already,
        "unmatched": unmatched,
        "reasons": reasons,
        "counts": {
            "hearted": len(hearted),
            "already_hearted": len(already),
            "unmatched": len(unmatched),
        },
        "unmatched_tracks": left_out,
    }


def _left_out(report: dict, said: list[dict]) -> list[dict[str, str]]:
    """Each favourite one item report left unhearted, named as the answer lists it.

    OFF THE REPORT'S ``unmatched`` LIST, which names every such row; the names
    come from ``unmatched_tracks``, else ``reasons``, else the identity alone.
    """
    named: dict[str, dict] = {}
    for one in (*said, *(report.get("unmatched_tracks") or ())):
        if isinstance(one, dict):
            named[str(one.get("row") or "")] = one
    rows = []
    for item in report.get("unmatched") or ():
        identity = str(item)
        one = named.get(identity, {})
        rows.append(
            {
                "identity": identity,
                "artist": str(one.get("artist") or ""),
                "title": str(one.get("title") or ""),
                "reason": str(one.get("reason") or "") or NO_MATCH,
            }
        )
    return rows


def concluded(outbound: Mapping[str, Any]) -> tuple[dict[str, str], ...]:
    """The warning a finished sweep carries when it left favourites unhearted.

    THE OUTCOME STAYS ``ok``, as ``export.cli.concluded`` says: the vocabulary
    has no partial word, so this is the line a script keys on.
    """
    tally = shell.unmatched_tally(outbound)
    if tally is None:
        return ()
    missed, total = tally
    # "WERE NOT HEARTED": only what the provider could not match is this
    # warning's to state (R-855).
    return (
        {
            "code": UNMATCHED_WARNING,
            "message": (
                f"{missed} of the {total} favourite(s) in this sweep were not "
                f"hearted on the streaming service, because the provider could "
                f"not match them; each is listed with its reason in this answer"
            ),
        },
    )


def build_sync(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the favourites increment already queued under this identifier",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        dest="run_id",
        help="intake run shared with the other sources in this sync",
    )
    parser.add_argument(
        "--export",
        default=None,
        metavar="EXPORT",
        help=(
            "the rekordbox collection export holding the favourites playlist; "
            "the live database is never read"
        ),
    )
    parser.add_argument(
        "--favorites-playlist",
        default=source.DEFAULT_FAVORITES_PLAYLIST,
        dest="favorites_playlist",
        metavar="NAME",
        help=(
            "the playlist whose members are swept; the default is the one the "
            "source system maintains"
        ),
    )
    parser.set_defaults(_handler=sync_favorites)


def confirm_digest(
    playlist_key: str, export_path: str, tracks: list[str] | tuple[str, ...]
) -> str:
    """The identity the confirm decision is recorded against.

    The enqueue path builds it from a freshly resolved playlist and the resume
    path from the frozen payload, and they must agree.
    """
    return digest_of(
        {
            "kind": "sync.favorites",
            "playlist": playlist_key,
            "export": export_path,
            # THE TRACK SET, which names what will be written.
            "tracks": list(tracks),
        }
    )


def sync_favorites_argv(job) -> list[str]:
    """The command line that continues one queued favourites increment.

    TWO RUNS, NOT ONE: ``--run-id`` carries the INTAKE run shared with the other
    sources in a sync, ``--run`` the GATE run the confirm was recorded against,
    which ``cli._run_state_for`` reads; without it every respawn met the confirm
    gate with nothing recorded. ``--export`` AND ``--favorites-playlist`` ARE
    REBUILT FROM THE PAYLOAD, the playlist as the resolved key, so the resumed
    child computes the same confirm digest. A job frozen with no gate run
    resumes without the flag.
    """
    payload = job.payload or {}
    argv = ["sync", "favorites", "--job", job.job_id]
    rebuilt = (("--run-id", "run_id"), ("--export", EXPORT), ("--favorites-playlist", PLAYLIST))
    for flag, key in rebuilt:
        if payload.get(key):
            argv.extend([flag, str(payload[key])])
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, *argv]


def sync_favorites(ctx) -> Envelope:
    """Confirm the remote heart-back, then queue it, or drive the queued sweep."""
    spec = next(gate for gate in ctx.entry.gates if gate.name.endswith(".confirm"))
    if ctx.args.job:
        return shell.resume(
            ctx,
            spec,
            ctx.args.job,
            digest=confirm_digest,
            summary=summary,
            # THE RESUME IS WHERE THE HEARTING HAPPENS, so it says so too.
            standing=local_write_warning(),
            concluded=concluded,
        )

    # LOADED BEFORE THE GATE (R-227), for the person's own day count, and before
    # the colour read, which needs the configured database path.
    cfg = shell.load_config("favorites.cli")
    exported, resolved = resolve_sweep(
        getattr(ctx.args, "export", None),
        getattr(ctx.args, "favorites_playlist", None),
        cfg=cfg,
    )
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)

    # THE TRACKS THE DIGEST COVERS ARE SHOWN (R-693), beside the export's age
    # and the colour versus playlist counts (R-228).
    option = ctx.gate.require(
        spec,
        plan={"digest": sweep_digest(exported, resolved), "items": list(resolved.track_ids)},
        context={
            shell.PLAYLIST: resolved.key,
            shell.EXPORT_PATH: str(exported),
            **shell.shown_export(age),
            **sweep_source_facts(resolved),
        },
    )
    if option == "abort":
        # THE DECLARED SHAPE, ``job_state/1``; see ``shell.declined``.
        return ctx.envelope(data=shell.declined(), outcome=Outcome.NO_OP)
    run_id = getattr(ctx.args, "run_id", None) or ctx.run.run_id
    with jobs.open_store() as store:
        job = queue_sweep(
            store,
            cfg,
            handler_key=ctx.entry.handler_key,
            run_id=run_id,
            gate_run=ctx.run.run_id,
            exported=exported,
            resolved=resolved,
        )
        return ctx.envelope(
            data=shell.reported(store, job, cfg, summary),
            warnings=(
                *shell.queue_warnings(resolved, noun="favourite", age=age),
                *local_write_warning(),
            ),
        )


def resolve_sweep(
    export: str | None,
    playlist: str | None,
    *,
    cfg: config.Config | None = None,
    pink_ids: Sequence[str] | None = None,
) -> tuple[Path, source.ResolvedPlaylist]:
    """The export and the favourites union a sweep would queue, or a refusal.

    PUBLIC because ``crate sync all`` asks its confirm over the same digest.
    THE PLAYLIST IS RESOLVED FIRST, so an empty ``All Favorites`` refuses before
    any colour is read; pink rows then join through a read only open, or
    ``pink_ids`` when a caller holds them, a failed read refusing with its cause.
    """
    exported = source.required_path(export)
    wanted = str(playlist or source.DEFAULT_FAVORITES_PLAYLIST)
    library = source.read_library(exported)
    resolved = source.resolve(library, wanted)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)


def sweep_digest(exported: Path, resolved: source.ResolvedPlaylist) -> str:
    """The confirm digest for one resolved sweep, as both queueing verbs ask it."""
    return confirm_digest(resolved.key, str(exported), resolved.track_ids)


def queue_sweep(
    store,
    cfg: config.Config,
    *,
    handler_key: str,
    run_id: str,
    gate_run: str,
    exported: Path,
    resolved: source.ResolvedPlaylist,
) -> jobs.Job:
    """Queue one favourites sweep. The one spelling of what a sweep job is.

    ``gate_run`` IS A RUN OWNED BY ``sync.favorites``, whichever verb queued the
    job, since the dispatcher refuses a run of another verb on resume, so
    ``crate sync all`` hands its answer over first (``Gates.hand_off``).
    """
    return jobs.enqueue(
        store,
        handler_key=handler_key,
        # TWO RUNS, TWO KEYS, as ``sync_favorites_argv`` says.
        payload={
            "source_id": "favorites",
            "run_id": run_id,
            PLAYLIST: resolved.key,
            EXPORT: str(exported),
            shell.TRACKS: list(resolved.track_ids),
            jobs.GATE_RUN_KEY: gate_run,
        },
        # ONE FAVOURITE IS ONE ITEM, so the sweep cannot queue empty work.
        item_ids=resolved.track_ids,
        cfg=cfg,
    )


def run_heart_item(
    payload: dict[str, Any], row_id: str, cfg: config.Config, remote
) -> dict:
    """Heart ONE library favourite, and report what happened. Never a remove.

    PURE OF THE JOB ENGINE, so a track the account already hearts being
    reported rather than written again is drivable without a queue.
    ``colors=None`` AND NO ``flags``: the colour writer would touch the live
    database. THE REPORT CARRIES NO ``colored`` KEY (R-424), which would read
    as a write that found nothing to do rather than one that cannot happen.
    """
    library = source.read_library(Path(str(payload[EXPORT])))
    candidates = source.heart_candidates(library, (row_id,), cfg=cfg)
    if not candidates:
        raise refuse(
            "outbound-item-absent",
            f"the export at {Path(str(payload[EXPORT])).name} no longer carries "
            f"row {row_id!r}, which this sweep queued, so there is nothing to "
            f"heart for this item and nothing was written",
            steps=(
                "export the collection again and queue a new sweep rather than "
                "resuming this one",
            ),
            origin=("favorites", "cli"),
            detail={"row": row_id},
        )
    report = hearts.heart_back(cfg, remote, candidates, colors=None)
    named = {item.row_id: item for item in candidates}
    said = dict(report.reasons)

    def row_named(row: str, reason: str) -> dict[str, str]:
        return {
            "row": row,
            "title": named[row].release_title if row in named else "",
            "artist": named[row].artist if row in named else "",
            "reason": reason,
        }

    return {
        "row": row_id,
        "hearted": list(report.hearted),
        "already": list(report.already),
        "unmatched": list(report.unmatched),
        # WITH THE ROW'S OWN NAMES, the release title being the one a candidate carries.
        "reasons": [row_named(row, reason) for row, reason in report.reasons],
        # EVERY UNMATCHED ROW NAMED, the account's reason or none (R-856).
        "unmatched_tracks": [row_named(row, said.get(row, "")) for row in report.unmatched],
    }


def handle(job, item, cfg) -> jobs.Produced:
    """Heart one queued favourite. The per item worker behind ``sync.favorites``.

    THE ITEM NAMES THE ROW, not the payload, or every item would heart the
    same track. ``cfg`` is the frozen configuration (KTD9), so a sweep records
    its hearts in the library it was queued for.
    """
    from cratekit.modules.outbound import account, artifacts

    payload = dict(job.payload or {})
    report = run_heart_item(payload, str(item.item_id), cfg, account.resolve(cfg))
    return artifacts.produced(cfg, job, item, report)


__all__ = [
    "BACKLOG",
    "LOCAL_WRITE_WARNING",
    "NO_MATCH",
    "PINK_COLOUR_MISSING",
    "PINK_COLOUR_NAME",
    "PLACEHOLDER_NAME",
    "UNMATCHED_WARNING",
    "build_sync",
    "concluded",
    "confirm_digest",
    "handle",
    "local_write_warning",
    "pink_colour_id",
    "pink_content_ids",
    "placeholder_name",
    "queue_sweep",
    "read_pink_track_ids",
    "resolve_sweep",
    "run_heart_item",
    "summary",
    "sweep_digest",
    "sweep_source_facts",
    "sync_favorites",
    "sync_favorites_argv",
    "union_with_pink",
]
