"""``export.prune``: take tracks that left a library playlist off its remote copy (R-836).

``export playlist`` never removes, so this verb plans the tracks the outbound
ledger records as added to the remote playlist that no row of the library
playlist matches any more, shows each at one explicit gate and on ``apply``
takes them off, by :mod:`cratekit.modules.outbound.prune`. The library
playlist is read from a collection export, its age on the gate: an export
older than the one last written from would read every track added since as
gone, so it leaves the playlist alone, as does a row the provider does not
match or the export does not carry. NOT QUEUED: each removal is recorded as
it lands, so a run started again plans only what is left.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import refuse
from cratekit.modules.outbound import export as outbound_export
from cratekit.modules.outbound import ledger, prune, shell, source

_ORIGIN = ("export.prune",)


def build_prune(parser, entry) -> None:
    del entry
    parser.add_argument("playlist", help="stable identifier of the library playlist")
    parser.add_argument(
        "--export",
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
    # AN EXPORT OLDER THAN THE ONE THE PLAYLIST WAS LAST WRITTEN FROM is not
    # read for a prune: every track added since would read as gone. A record
    # written before the date was kept has none, and only the age is shown.
    given = age.written.isoformat() if age.written is not None else ""
    older = record.written if record is not None and ledger.older_than(given, record.written) else ""
    planned = prune.plan_export(
        cfg,
        resolved.key,
        resolved.name,
        (*resolved.track_ids, *resolved.dangling),
        wanted,
        unmatched,
        remote,
        older=older,
    )
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
    again = "run crate export prune again; what was taken off is recorded and never asked twice"
    return prune.settle(
        ctx, cfg, remote, payload, planned, option=option, origin=_ORIGIN, again=again
    )


__all__ = ["build_prune", "export_prune"]
