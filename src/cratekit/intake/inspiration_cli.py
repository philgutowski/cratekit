"""``crate intake inspiration``: the set's permanent playlist for a set already landed (U121).

``intake land --set`` writes the playlist in the landing's own commit. This
verb is the backfill for a set job whose files landed before that existed, or
landed without ``--set``: the Vonking set and the sitting 11 sets. It reads
the same job, names the playlist the same way, resolves every row against the
library as it is now, shows the plan, asks its explicit gate, and writes the
playlist in a session of its own through the guarded writer, reading it back
from SQL before it answers. It adds nothing to INBOX and touches no content
row.

THE ORDER IS THE NATIVE LANDING'S, :func:`land_cli.ask_then_write`: the
database opened with write intent before the plan, the acknowledgment read
before the gate (R-733), the write only on ``apply``. Database native intake
trees only, since the playlist is a database node and the bridge's writers
emit an export.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import analysis_store, config, jobs, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Remedy
from cratekit.intake import ingest, land_cli, set_playlist

#: The gate, explicit: a playlist the library keeps for good is a new node
#: written outside the intake flow, answered by a recorded act (R34).
APPROVE_GATE = "intake.inspiration.approve"

_ORIGIN = ("intake", "inspiration_cli")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("intake.inspiration_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    parser.add_argument(
        "--job",
        required=True,
        metavar="JOB",
        help="the intake set job the playlist is made from, as crate intake set printed it",
    )
    set_playlist.add_word_arguments(parser)
    parser.set_defaults(_handler=intake_inspiration)


def _native_or_refuse(cfg: config.Config) -> ingest.IntakeMedium:
    medium = ingest.intake_medium(cfg)
    set_playlist.assert_native(medium, landing=False)
    return medium


def planned(
    cfg: config.Config,
    declared,
    job: jobs.Job,
    words: set_playlist.SetWords,
    reports: tuple[dict[str, Any], ...],
) -> set_playlist.SetPlaylistPlan:
    """The plan over the library as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return set_playlist.plan_for_backfill(cfg, db, declared, job, words, reports)
    finally:
        rb_writer.close_db(db)


def written(
    cfg: config.Config,
    declared,
    plan: set_playlist.SetPlaylistPlan,
    job: jobs.Job,
    words: set_playlist.SetWords,
    reports: tuple[dict[str, Any], ...],
) -> set_playlist.Written | None:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return set_playlist.apply_alone(
            cfg,
            db,
            plan,
            declared=declared,
            job=job,
            words=words,
            reports=reports,
            analysis_roots=analysis_store.watch_roots(cfg),
        )
    finally:
        rb_writer.close_db(db)


def intake_inspiration(ctx) -> Envelope:
    """Name the set, plan its playlist over the library now, ask, write, read back.

    THE ORDER IS THE ROTATION'S: the plan on a read handle, the acknowledgment
    before the gate (R-733), the gate over the digested plan, the write on a
    handle opened with write intent that takes the plan again and refuses a
    digest that moved.
    """
    cfg = _load()
    medium = _native_or_refuse(cfg)
    declared = medium.declared
    with jobs.open_store() as store:
        job = set_playlist.set_job_or_refuse(store, str(ctx.args.job))
        words = set_playlist.words_for(
            job, dj=ctx.args.dj, set_name=ctx.args.set_name, set_date=ctx.args.set_date
        )
        reports = set_playlist.reports_of(store, job)
    spec = land_cli.gate_named(ctx.entry, APPROVE_GATE)
    plan = planned(cfg, declared, job, words, reports)
    payload = set_playlist.payload(plan)
    session.assert_backup_acknowledged(cfg)
    if ctx.gate.require(spec, plan=payload, context=set_playlist.facts(plan)) != "apply":
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    if not plan.members:
        # AN EMPTY PLAN IS STILL A PLAN A PERSON CAN ABORT, as the rotation's
        # is, so the gate was asked; once answered, a set with no member to
        # hold writes nothing and says so.
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[
                *set_playlist.nothing_note(plan),
                *set_playlist.left_warning(plan.left),
            ],
        )
    kept = written(cfg, declared, plan, job, words, reports)
    assert kept is not None, "a plan with members writes"
    set_playlist.assert_read_back(kept)
    data: dict[str, Any] = {
        **payload,
        "items": [
            *payload["items"],
            land_cli.set_playlist_item(kept, session_id=""),
        ],
        "totals": {
            **payload["totals"],
            "added": kept.added,
            "read back": len(kept.read_back),
        },
    }
    return ctx.envelope(
        data=data,
        warnings=[
            *set_playlist.written_note(kept),
            *set_playlist.left_warning(kept.left),
        ],
    )


__all__ = ["APPROVE_GATE", "build", "intake_inspiration", "planned", "written"]
