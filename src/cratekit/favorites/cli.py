"""``crate sync favorites``: confirm the remote half, queue it, then run it.

The outbound confirm is a separate gate from any local colour or tag write
this verb may later accompany. The engine in
``cratekit.modules.outbound.hearts`` is add-only. This shell never un-hearts and
never un-colours, and since U51 it also DRIVES the sweep: ``handle`` below is the
per item worker behind the ``sync.favorites`` handler key, and it is the first
caller in ``src`` of ``hearts.heart_back``.

**WHAT A FAVOURITE IS HERE.** The engine below calls its input "pink local
favourites", and in the live system pink is the operator's standing signal that a
row should be hearted. A rekordbox collection export carries no colour, so this
shell reads pink from a read only open of the live database (R-228), unions those
content ids with membership of a named playlist (defaulting to the one the source
system maintains), and deduplicates by content id. Each source is named in the
plan. A pink row the export lacks is left out of the queue and named beside
dangling. The empty playlist refusal stays ahead of the colour read.

**NO LOCAL WRITE HAPPENS HERE, AND SINCE R-424 NOTHING SAYS OTHERWISE.**
``heart_back`` accepts a ``LocalColors`` writer and would colour the library row.
That is a write to the live rekordbox database and belongs behind the guarded
write session, so ``colors`` is ``None`` and this verb reaches the remote half
only. That was true before R-424 and only this docstring said it: the registry
declared four local write surfaces, the guide promised a colour, a Favorite tag
and playlist membership, and each item's report carried a ``colored`` list that
was empty on every path. :data:`LOCAL_WRITE_WARNING` is the correction a person
actually reads, because the default renderer prints a verb's outcome, its
warnings and its run id, and nothing else.

**ADD ONLY IS A PROPERTY OF THE TYPE, NOT OF THIS FILE'S RESTRAINT.**
``modules/outbound/service.RemoteAccount`` declares no remove, so a caller that
wanted one would have nowhere to call it. This shell passes no ``flags`` at all,
which is one fewer surface for a remove-shaped request to arrive on.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, rb_writer
from cratekit.core.cause import Outcome, Scope, refuse
from cratekit.favorites import placeholders
from cratekit.modules.outbound import account, artifacts, hearts, shell, source
from cratekit.write import trees

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

#: What every pass of this verb tells a person about the LOCAL half (R-424).
#:
#: A STANDING CONDITION RATHER THAN AN EVENT, which is the same shape as
#: ``outbound-account-unbound`` in :mod:`cratekit.modules.outbound.shell`: it is
#: true of this build on every pass, and a person is told at the moment the
#: report would otherwise let them assume the opposite. It is a warning and not
#: a line of rendered data because the default renderer has no case for a
#: ``job_state/1`` payload, so the warning channel is the only place a sentence
#: reaches the person who did not ask for json.
#:
#: Spelled once and read by two composers. ``crate sync all`` builds the
#: favourites plan itself rather than calling this verb's queueing branch, so a
#: message living in that branch alone would be absent from the pass most people
#: actually run.
#:
#: IT NAMES ITS SUBJECT. Under ``crate sync all`` this sentence prints beside
#: warnings from sources that genuinely do write the library, and "this sweep"
#: in that company reads as a claim about the whole pass. The one place a
#: warning can be misread is the place it appears next to other warnings.
LOCAL_WRITE_WARNING: dict[str, str] = {
    "code": "favorites-local-write-unbound",
    "message": (
        "the favourites sweep hearts matching tracks on the streaming service "
        "and changes nothing in the library: it writes no colour, no Favorite "
        "tag and no playlist membership locally"
    ),
}


def local_write_warning() -> tuple[dict[str, str], ...]:
    """:data:`LOCAL_WRITE_WARNING` as a warnings tuple, copied per call.

    A COPY, because the envelope's warnings travel into a renderer and into json,
    and a caller handed the module level dict could mutate the sentence every
    later pass of this verb reports.
    """
    return (dict(LOCAL_WRITE_WARNING),)


#: The colour name rekordbox stores on ``djmdColor.Commnt`` for pink rows.
#:
#: LOOKED UP BY THIS NAME rather than hard coded as ColourID 1 (R-228). The
#: column is ``Commnt`` in the binding; that is the colour's display name.
PINK_COLOUR_NAME = "Pink"

#: The refusal when the colour table has no live Pink row.
PINK_COLOUR_MISSING = "favorites-pink-colour-missing"


def pink_colour_id(db: Any) -> str:
    """The ColourID whose name is Pink inside an already open library, or a refusal.

    Soft deleted colour rows are skipped through the one soft delete reader, as
    ``collection_export.read_tracks`` skips tombstoned content. No live Pink row
    is a named refusal rather than a silent empty colour source.
    """
    for row in db.get_color(Commnt=PINK_COLOUR_NAME):
        if trees.soft_delete_marker(row):
            continue
        return str(row.ID)
    raise refuse(
        PINK_COLOUR_MISSING,
        "the library's colour table has no live row named Pink, so this sweep "
        "cannot tell which rows are pink and would report complete over rows "
        "it never considered",
        steps=(
            "restore the Pink colour in rekordbox, or colour one row pink so "
            "the table carries it again",
        ),
        scope=Scope.RUN,
        origin=("favorites", "cli"),
    )


def pink_content_ids(db: Any) -> tuple[str, ...]:
    """Every live content id coloured pink in ``db``, ordered as the binding yields them.

    Soft deleted content rows are skipped through the same reader
    ``collection_export.read_tracks`` uses. The Pink ColourID is looked up in
    this same open, never hard coded.
    """
    pink = pink_colour_id(db)
    found: list[str] = []
    for row in db.get_content():
        if trees.soft_delete_marker(row):
            continue
        if str(getattr(row, "ColorID", "") or "") == pink:
            found.append(str(row.ID))
    return tuple(found)


def read_pink_track_ids(cfg: config.Config) -> tuple[str, ...]:
    """Pink content ids from a read only open of the configured library.

    THE READ'S OWN REFUSAL PROPAGATES (R-228). A missing database, a running
    rekordbox, or a file that is not a library must stop the sweep the way a
    missing export does, rather than let the playlist alone report as complete
    over colour the sweep never saw.
    """
    with rb_writer.read_only_copy(rb_writer.live_db_path(cfg), cfg=cfg) as db:
        return pink_content_ids(db)


def union_with_pink(
    library: source.Library,
    playlist: source.ResolvedPlaylist,
    pink_ids: Sequence[str],
) -> source.ResolvedPlaylist:
    """Playlist members union pink rows that the export carries, deduplicated.

    Playlist order is kept; pink rows the playlist already carries stay once.
    Pink rows the export lacks are named on ``pink_missing`` and left out of
    ``track_ids``, beside dangling. ``from_playlist`` and ``from_colour`` count
    each source's candidates, so a row in both is counted in both and queued
    once.
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
#: for it. The engine names such a row in ``unmatched`` and nowhere else, so
#: without this sentence it reached no line a person reads (R-856). Spelled in
#: the shell, so the export says the same thing in the same words.
NO_MATCH = shell.NO_MATCH

#: The warning a finished sweep carries when any favourite went unhearted.
UNMATCHED_WARNING = "favorites-hearts-unmatched"


def summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What this sweep's committed artifacts say it wrote.

    THE ``already`` SET IS THE ONE WORTH REPORTING, because it is the difference
    between a sweep that had nothing to do and a sweep that did nothing. Both
    show every item done, and only one of them means the account changed.

    COUNTED, AND EVERY UNMATCHED FAVOURITE LISTED (R-856). The lists alone were
    in the envelope and nowhere a person reads, because the default renderer
    prints an outbound summary only when it carries ``counts``, so a sweep that
    hearted nothing it could not match answered ``ok`` and ``N of N settled``.
    The count keys are this verb's own, ``hearted`` and ``already_hearted``,
    because the export's ``written`` and ``already`` are printed in words about
    a playlist. ``unmatched_tracks`` is the export's shape, one row per
    favourite with its identity, artist, title and reason, a row the account
    said nothing about included, which ``reasons`` omits. Read per committed
    item, so a resumed sweep is counted across both runs and nothing twice.
    """
    hearted: list[str] = []
    already: list[str] = []
    unmatched: list[str] = []
    reasons: list[str] = []
    left_out: list[dict[str, str]] = []
    for report in artifacts.committed(cfg, job_id):
        hearted.extend(str(item) for item in report.get("hearted") or ())
        already.extend(str(item) for item in report.get("already") or ())
        unmatched.extend(str(item) for item in report.get("unmatched") or ())
        # One sentence per favourite the account would not choose a release for
        # (R-356). A report written before that key existed carries none.
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

    OFF THE REPORT'S ``unmatched`` LIST, which names every such row, and not off
    ``reasons``, which names only a row the account said something about. The
    names come from ``unmatched_tracks``, which every item report carries since
    R-856, then from ``reasons`` for a report written before that, and a row
    neither names is listed by its identity alone rather than left out.
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

    THE OUTCOME STAYS ``ok``, for the reason ``export.cli.concluded`` gives:
    the outcome vocabulary has no partial word, and this is the line a script
    reading only the outcome and the warnings can key on. It follows the
    standing warning, which ``shell.resume`` puts first.
    """
    tally = shell.unmatched_tally(outbound)
    if tally is None:
        return ()
    missed, total = tally
    # "WERE NOT HEARTED", NOT "ARE NOT HEARTED". A favourite counted as already
    # hearted may be counted so off the ledger rather than the account, the
    # export's R-855 shape, so only what the provider could not match is this
    # warning's to state.
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
            ctx,
            spec,
            ctx.args.job,
            digest=confirm_digest,
            summary=summary,
            # THE RESUME IS WHERE THE HEARTING HAPPENS, so it is the pass whose
            # report a person reads for what the run did. Telling them only at
            # queue time would put the correction on the invocation that wrote
            # nothing at all.
            standing=local_write_warning(),
            concluded=concluded,
        )

    # LOADED BEFORE THE GATE (R-227), so the age the gate shows is judged against
    # the person's own day count, and before the colour read, which needs the
    # configured database path. See ``export/cli.py`` for the other half of why.
    cfg = shell.load_config("favorites.cli")
    exported, resolved = resolve_sweep(
        getattr(ctx.args, "export", None),
        getattr(ctx.args, "favorites_playlist", None),
        cfg=cfg,
    )
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)

    # THE TRACKS THE DIGEST COVERS ARE SHOWN (R-693), through the gate layer,
    # beside the export's age and the colour versus playlist counts (R-228).
    # The resume shows the same tracks off the frozen payload.
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
        # THE DECLARED SHAPE, and nothing about the playlist. See
        # ``shell.declined``: this verb declares ``job_state/1`` and the payload
        # that named the playlist carried none of that surface's four fields.
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

    PUBLIC because ``crate sync all`` resolves the same sweep before it asks its
    own confirm, and the digest it asks over has to be the one this verb would
    compute. One resolution, two callers, one digest.

    THE PLAYLIST IS RESOLVED FIRST, so an empty ``All Favorites`` still refuses
    before any colour is read. Pink rows then join through a read only open, or
    through ``pink_ids`` when a caller (or a test) already holds them. A colour
    read that cannot finish refuses with that read's own cause.
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

    THE REPORT CARRIES NO ``colored`` KEY, and that is R-424 rather than an
    omission. ``HeartReport.colored`` is the rows the engine coloured, which is
    every row when a caller hands it a writer and none when it does not. Reported
    from here it was an empty list on every pass, and an empty list reads as a
    write that found nothing to do rather than as a write that cannot happen.
    ``summary`` below never read the key, so nothing downstream loses a field.
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
        # WITH THE ROW'S OWN NAMES, because the engine reports a row by its
        # identifier and a person reading why a favourite was not hearted needs
        # to know which favourite. The title is the release title, head off,
        # which is the only one a heart candidate carries.
        "reasons": [row_named(row, reason) for row, reason in report.reasons],
        # EVERY UNMATCHED ROW NAMED, the account's reason or none (R-856).
        # ``reasons`` carries only a row the account said something about, so
        # a favourite the provider has never heard of had no name on disk.
        "unmatched_tracks": [row_named(row, said.get(row, "")) for row in report.unmatched],
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
