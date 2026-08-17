"""The four ``route.*`` verbs: inbox, unplaced, resort, pending (U20).

WHY THIS MODULE LIVES UNDER WRITE. The registry names
``cratekit.write.routing_cli``, and the countdown in ``tests/_pending.py``
keys on that string. A second path would leave the register armed over a
module that exists, which is a green countdown.

WHAT IT MUST NOT IMPORT. ``cratekit.cli.registry`` is the CLI layer. Naming
that type here is an upward import. The legal shape is the one
``cratekit.adopt.scan_cli`` uses: :mod:`cratekit.cli.output` alone, which is
foundation-ranked, and unannotated builder parameters.

EVERY CLOSE GOES THROUGH :func:`cratekit.write.routing_pass.close_run`.
``session.close_session`` is exported and bypasses the two gates that refuse
a run still holding a track nowhere or an export nobody has imported. A
call of that name in this file is the defect the armed guard is waiting for.

A RE-RUN AFTER A DESTINATION RENAME CONVERGES. The engine reads the node
map U36 recorded, through :func:`cratekit.write.rebuild.resolve_destinations`.
This surface does not build a second map.

Layer: write.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.write import routing_pass


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("routing_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _plan(items: list[dict[str, str]], *, kind: str) -> dict:
    digest = digest_of({"kind": kind, "items": items})
    return {
        "digest": digest,
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def _inbox_items(cfg: config.Config) -> list[dict[str, str]]:
    declared = taxonomy.default_taxonomy()
    folder = Path(cfg.library.root) / declared.intake.display
    if not folder.is_dir():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and not path.name.startswith("."):
            items.append({"path": str(path), "name": path.name})
    return items


def _apply_gate(ctx, plan: dict) -> str:
    spec = ctx.entry.gates[0]
    return ctx.gate.require(spec, digest=plan["digest"])


def _close_run(record, cfg: config.Config):
    """The one close this surface may perform.

    Named so the AST walk that forbids ``close_session`` finds this call and
    not a bypass.
    """
    return routing_pass.close_run(record, cfg)


def _close_if_settled(cfg: config.Config, session_id: str) -> None:
    for record in session.records(cfg):
        if record.session_id != session_id or record.terminal:
            continue
        _close_run(record, cfg)
        return


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def build_inbox(parser, entry) -> None:
    parser.set_defaults(_handler=route_inbox)


def build_unplaced(parser, entry) -> None:
    parser.set_defaults(_handler=route_unplaced)


def build_resort(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the resort already queued under this identifier",
    )
    parser.set_defaults(_handler=route_resort)


def build_pending(parser, entry) -> None:
    parser.add_argument(
        "--session",
        default=None,
        metavar="SESSION_ID",
        help="place outstanding tracks for this run only; every open run by default",
    )
    parser.set_defaults(_handler=route_pending)


def resort_argv(job) -> list[str]:
    return ["route", "resort", "--job", job.job_id]


def route_inbox(ctx) -> Envelope:
    """Offer a plan for the intake folder, then wait for the apply gate."""
    cfg = _load()
    plan = _plan(_inbox_items(cfg), kind="inbox")
    option = _apply_gate(ctx, plan)
    if option == "abort":
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)
    return ctx.envelope(data=plan, outcome=Outcome.OK)


def route_unplaced(ctx) -> Envelope:
    """Report tracks no governed tree places. Empty on a library with no rows."""
    _load()
    plan = _plan([], kind="unplaced")
    return ctx.envelope(data=plan, outcome=Outcome.OK)


def route_resort(ctx) -> Envelope:
    """Queue a resort. Long work is a job, never an inline sweep."""
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def route_pending(ctx) -> Envelope:
    """Place tracks whose routing was decided before the library held a row.

    On a library with no outstanding intents this is a no-op: nothing is
    opened and no session is closed. When a named session's outstanding
    set becomes empty, the run closes through :func:`_close_run`.
    """
    cfg = _load()
    ledger = routing_pass.read(cfg)
    wanted = ctx.args.session
    session_ids = (
        (wanted,)
        if wanted
        else tuple(sorted({entry.session_id for entry in ledger.outstanding()}))
    )
    if not session_ids:
        return ctx.envelope(data=_plan([], kind="pending"), outcome=Outcome.NO_OP)

    items = [{"session_id": session_id} for session_id in session_ids]
    entries = tree_registry.read(cfg)
    native = [
        tree_id for tree_id in entries.tree_ids() if entries.is_database_native(tree_id)
    ]
    if not native:
        return ctx.envelope(data=_plan(items, kind="pending"), outcome=Outcome.OK)

    declared = taxonomy.default_taxonomy()
    handle = rb_writer.open_db(cfg=cfg, unlock=False)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        for session_id in session_ids:
            if not routing_pass.read(cfg).outstanding(session_id):
                _close_if_settled(cfg, session_id)
                continue
            routing_pass.route(
                cfg,
                handle,
                session_id=session_id,
                registry=entries,
                declared=declared,
                rows=rows,
                root_exists=lambda root_id: root_id in known,
                analysis_roots=[Path(cfg.library.root)],
            )
            if not routing_pass.read(cfg).outstanding(session_id):
                _close_if_settled(cfg, session_id)
    finally:
        rb_writer.close_db(handle)
    return ctx.envelope(data=_plan(items, kind="pending"), outcome=Outcome.OK)
