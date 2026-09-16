"""``crate sync favorites``: confirm the remote half, queue it, then run it.

The outbound confirm is a separate gate from any local colour or tag write
this verb may later accompany. The engine in
``cratekit.modules.outbound.hearts`` is add-only. This shell never un-hearts and
never un-colours, and since U51 it also DRIVES the sweep: ``handle`` below is the
per item worker behind the ``sync.favorites`` handler key, and it is the first
caller in ``src`` of ``hearts.heart_back``.

**WHAT A FAVOURITE IS HERE, AND HOW THAT DIFFERS FROM THE SOURCE SYSTEM.** The
engine below calls its input "pink local favourites", and in the live system pink
is the operator's standing signal that a row should be hearted. This shell cannot
see pink: it reads a rekordbox collection export, and that document's track rows
carry no colour, so a hand coloured row is invisible to it. What it reads instead
is membership in a named playlist, defaulting to the one the source system
maintains. A pink row outside that playlist is not swept, which is R-228 rather
than something papered over.

**NO LOCAL WRITE HAPPENS HERE.** ``heart_back`` accepts a ``LocalColors`` writer
and would colour the library row. That is a write to the live rekordbox database
and belongs behind the guarded write session, so ``colors`` is ``None`` and this
verb reaches the remote half only.

**ADD ONLY IS A PROPERTY OF THE TYPE, NOT OF THIS FILE'S RESTRAINT.**
``modules/outbound/service.RemoteAccount`` declares no remove, so a caller that
wanted one would have nowhere to call it. This shell passes no ``flags`` at all,
which is one fewer surface for a remove-shaped request to arrive on.

Layer: modules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import Outcome, refuse
from cratekit.favorites import placeholders
from cratekit.modules.outbound import account, artifacts, hearts, shell, source

#: The two payload keys both outbound verbs freeze, spelled once in
#: :mod:`cratekit.modules.outbound.shell` because the shared resume branch reads
#: them to rebuild the confirm digest.
PLAYLIST = shell.PLAYLIST
EXPORT = shell.EXPORT

#: The quarterly placeholder playlists this source owns, spelled in
#: :mod:`cratekit.favorites.placeholders` so the core playlists source can
#: exclude them without importing this CLI.
PLACEHOLDER_NAME = placeholders.PLACEHOLDER_NAME
BACKLOG = placeholders.BACKLOG
placeholder_name = placeholders.placeholder_name


def summary(cfg: config.Config, job_id: str) -> dict[str, list[str]]:
    """What this sweep's committed artifacts say it wrote.

    THE ``already`` SET IS THE ONE WORTH REPORTING, because it is the difference
    between a sweep that had nothing to do and a sweep that did nothing. Both
    show every item done, and only one of them means the account changed.
    """
    hearted: list[str] = []
    already: list[str] = []
    unmatched: list[str] = []
    for report in artifacts.committed(cfg, job_id):
        hearted.extend(str(item) for item in report.get("hearted") or ())
        already.extend(str(item) for item in report.get("already") or ())
        unmatched.extend(str(item) for item in report.get("unmatched") or ())
    return {"hearted": hearted, "already": already, "unmatched": unmatched}


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

    Same shape and the same reason as the export verb's: the enqueue path builds
    it from a freshly resolved playlist and the resume path builds it from the
    frozen payload, and the whole point is that they agree. Before this the
    digest named only ``{"kind": ..., "direction": "heartback"}``, which is a
    constant, so one recorded confirmation authorised a sweep of any playlist in
    any document.
    """
    return digest_of(
        {
            "kind": "sync.favorites",
            "playlist": playlist_key,
            "export": export_path,
            # THE TRACK SET, not just the file it came from. A path names where
            # the answer was read; only this names what will be written.
            "tracks": list(tracks),
        }
    )


def sync_favorites_argv(job) -> list[str]:
    """The command line that continues one queued favourites increment.

    TWO RUNS TRAVEL HERE AND THEY ARE NOT THE SAME RUN. ``--run-id`` is this
    verb's own argument and carries the INTAKE run shared with the other sources
    in a sync. ``--run`` is the root parser's flag and carries the GATE run, the
    one the confirm decision was recorded against. They defaulted to the same
    value, which is exactly why emitting only the first looked like carrying the
    run and restored no gate state at all: ``cli._run_state_for`` reads
    ``args.run`` and never ``args.run_id``.

    So this builder emitted ``--run-id`` and the child still minted a fresh run,
    met the explicit confirm gate with nothing recorded, and exited
    DECISION_REQUIRED on every respawn. The queue held a confirmed sync nothing
    could advance. Measured by driving this function's own output through the
    dispatcher on 2026-08-23. A predicate that searched the source for the
    substring ``--run`` reported this verb CLEAN, because ``--run-id`` contains
    it, which is the other half of why it survived.

    ``--export`` AND ``--favorites-playlist`` ARE REBUILT FROM THE PAYLOAD, and
    the playlist is the RESOLVED key rather than whatever was typed. The resumed
    child recomputes the confirm digest over those two values, so emitting the
    original argument would produce a different digest and meet ``DecisionStale``
    on every respawn, which is this docstring's own defect wearing a new hat.

    A job frozen by a build older than this one carries no gate run and resumes
    without the flag, which returns it to the refusal it was already in.
    """
    payload = job.payload or {}
    argv = ["sync", "favorites", "--job", job.job_id]
    run_id = payload.get("run_id")
    if run_id:
        argv.extend(["--run-id", str(run_id)])
    exported = payload.get(EXPORT)
    if exported:
        argv.extend(["--export", str(exported)])
    playlist = payload.get(PLAYLIST)
    if playlist:
        argv.extend(["--favorites-playlist", str(playlist)])
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, *argv]


def sync_favorites(ctx) -> Envelope:
    """Confirm the remote heart-back, then queue it, or drive the queued sweep."""
    spec = next(gate for gate in ctx.entry.gates if gate.name.endswith(".confirm"))
    if ctx.args.job:
        return shell.resume(
            ctx, spec, ctx.args.job, digest=confirm_digest, summary=summary
        )

    exported, resolved = resolve_sweep(
        getattr(ctx.args, "export", None), getattr(ctx.args, "favorites_playlist", None)
    )

    option = ctx.gate.require(spec, digest=sweep_digest(exported, resolved))
    if option == "abort":
        # THE DECLARED SHAPE, and nothing about the playlist. See
        # ``shell.declined``: this verb declares ``job_state/1`` and the payload
        # that named the playlist carried none of that surface's four fields.
        return ctx.envelope(data=shell.declined(), outcome=Outcome.NO_OP)
    cfg = shell.load_config("favorites.cli")
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
            warnings=shell.queue_warnings(resolved, noun="favourite"),
        )


def resolve_sweep(
    export: str | None, playlist: str | None
) -> tuple[Path, source.ResolvedPlaylist]:
    """The export and the favourites playlist a sweep would queue, or a refusal.

    PUBLIC because ``crate sync all`` resolves the same sweep before it asks its
    own confirm, and the digest it asks over has to be the one this verb would
    compute. One resolution, two callers, one digest.
    """
    exported = source.required_path(export)
    wanted = str(playlist or source.DEFAULT_FAVORITES_PLAYLIST)
    return exported, source.resolve(source.read_library(exported), wanted)


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
    job. The resume :func:`sync_favorites_argv` builds loads it with ``--run``,
    and the dispatcher refuses a run whose record belongs to another verb, so
    ``crate sync all`` hands its recorded answer to a run of this verb before it
    calls here (``Gates.hand_off``) rather than passing its own run.
    """
    return jobs.enqueue(
        store,
        handler_key=handler_key,
        # TWO RUNS, TWO KEYS, on purpose. ``run_id`` is the intake run this
        # sync shares across its sources. The gate run is the one the
        # confirm decision was recorded against, and conflating them is the
        # defect ``sync_favorites_argv`` describes.
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

    PURE OF THE JOB ENGINE, taking the payload and an account. The property that
    matters most, that a track the account already hearts is reported rather than
    written again, is then drivable without a queue.

    ``colors=None`` AND NO ``flags``. The colour writer would touch the live
    rekordbox database; ``flags`` exists so a caller that still thinks in mirror
    mode cannot reach a different function, and the safest value for a shell that
    never wants one is not to pass it.
    """
    library = source.read_library(Path(str(payload[EXPORT])))
    candidates = source.heart_candidates(library, (row_id,))
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
    return {
        "row": row_id,
        "hearted": list(report.hearted),
        "already": list(report.already),
        "colored": list(report.colored),
        "unmatched": list(report.unmatched),
    }


def handle(job, item, cfg) -> jobs.Produced:
    """Heart one queued favourite. The per item worker behind ``sync.favorites``.

    THE ITEM NAMES THE ROW, not the payload, for the reason ``master/cli.py``
    measured: reading the payload would make every item of a multi item job
    heart the same track.

    ``cfg`` is the frozen configuration (KTD9). It is passed straight to
    ``heart_back``, which resolves the outbound ledger against it, so a sweep
    records its hearts in the library it was queued for even if the current
    configuration now names another.
    """
    payload = dict(job.payload or {})
    report = run_heart_item(payload, str(item.item_id), cfg, account.resolve(cfg))
    return artifacts.produced(cfg, job, item, report)


__all__ = [
    "BACKLOG",
    "PLACEHOLDER_NAME",
    "build_sync",
    "confirm_digest",
    "handle",
    "placeholder_name",
    "queue_sweep",
    "resolve_sweep",
    "run_heart_item",
    "summary",
    "sweep_digest",
    "sync_favorites",
    "sync_favorites_argv",
]
