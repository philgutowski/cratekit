"""``export.prune``: take tracks that left a library playlist off its remote copy (R-836).

``export playlist`` adds a library playlist's tracks to a remote playlist and
never removes, so a track taken out of the library playlist stays on the
account. This verb plans which tracks the outbound ledger records as added to
that remote playlist and no row of the library playlist matches any more, shows
every one of them by artist and title at one explicit gate, and on ``apply``
takes them off. The planning and the apply are
:mod:`cratekit.modules.outbound.prune`'s.

THE LIBRARY PLAYLIST IS READ FROM A COLLECTION EXPORT, as ``export playlist``
reads it, and its age is shown on the gate: an export older than the playlist
reads every track added since as gone, which is why the person sees the date
beside the tracks it would take off. A row the provider does not match, or a
row the export names and does not carry, leaves the playlist alone, since its
track may be one the ledger recorded.

NOT QUEUED. A prune is one plan, one gate and a handful of removals, each
recorded as it lands, so a run started again plans only what is left.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import Outcome, refuse
from cratekit.modules.outbound import export as outbound_export
from cratekit.modules.outbound import ledger, prune, shell, source

_ORIGIN = ("export.prune",)


def build_prune(parser, entry) -> None:
    del entry
    parser.add_argument("playlist", help="stable identifier of the library playlist")
    parser.add_argument(
        "--export",
        default=None,
        metavar="EXPORT",
        help=(
            "the rekordbox collection export holding the playlist as it is now; the "
            "live database is never read"
        ),
    )
    parser.set_defaults(_handler=export_prune)


def export_prune(ctx) -> Envelope:
    playlist = str(ctx.args.playlist or "")
    if not playlist:
        raise refuse(
            "export-playlist-unknown",
            "export prune needs the library playlist identifier",
            steps=("pass the playlist identifier after the verb",),
            origin=_ORIGIN,
        )
    exported = source.required_path(getattr(ctx.args, "export", None))
    library = source.read_library(exported)
    resolved = source.resolve(library, playlist)
    cfg = shell.load_config("export.prune")
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
    record = ledger.exported_playlist(cfg, resolved.key)
    remote = None
    wanted: frozenset[str] = frozenset()
    unmatched = 0
    if record is not None and record.added:
        from cratekit.modules.outbound import account

        remote = account.resolve(cfg)
        matched = outbound_export.plan(
            source.local_tracks(library, resolved.track_ids, cfg=cfg),
            playlist_key=resolved.key,
            name=resolved.name,
            account=remote,
        )
        wanted = frozenset(one for _row, one in matched.matched)
        unmatched = len(matched.unmatched) + len(resolved.dangling)
    planned = prune.plan_export(cfg, resolved.key, resolved.name, wanted, unmatched, remote)
    payload = prune.payload(planned, kind=prune.EXPORTED, subject=resolved.key, digest=digest_of)
    # AN EMPTY PLAN STILL ASKS, so a person always sees what the prune judged.
    option = ctx.gate.require(
        ctx.entry.gates[0],
        plan=payload,
        context={
            shell.PLAYLIST: resolved.key,
            shell.EXPORT_PATH: str(exported),
            **shell.shown_export(age),
            **prune.shown(planned),
        },
    )
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    done = prune.Pruned()
    try:
        prune.apply(cfg, remote, planned, done)
    except Exception as exc:
        raise prune.failed_part_way(
            exc,
            done,
            origin=_ORIGIN,
            again="run crate export prune again; what was taken off is recorded and never asked twice",
        ) from exc
    return prune.finished(ctx, payload, planned, done)


__all__ = ["build_prune", "export_prune"]
