"""``crate tag retag``: confirm the selection, then queue the correction.

WHAT THE PERSON IS CONFIRMING. The plan is the SELECTION, every file under the
folder whose genre the declared taxonomy calls too coarse to be a final tag, and
nothing else. It deliberately does not carry what each file will become, because
the lookup that answers that is the long-running work and running it before the
gate would make the gate decorative: the sweep would already have happened.

THE DIGEST IS OVER THAT SELECTION, so a person who approves forty files and then
drops another hundred into the folder gets a stale decision rather than a wider
sweep than the one they agreed to. :func:`cratekit.tagging.retag.select` sorts,
which is what makes the digest stable across two runs over one unchanged folder.

THE GATE IS FOUND BY ITS DIGEST SOURCE AND NOT BY POSITION. This handler answers
the gate that was raised against the plan; the cloud-sync decision beside it
belongs to the guarded writer and is answered wherever that refusal is raised.
Indexing ``gates[0]`` would silently answer the wrong question the day somebody
reorders the tuple.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import retag

#: The digest source the registry declares for the gate this handler answers.
PLAN = "plan"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.retag_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def _plan_gate(ctx):
    """The declared gate whose decision is made against the plan.

    Refuses rather than defaulting when there is none. A handler that quietly
    skipped its confirmation because a registry edit dropped the gate would run a
    destructive sweep with nobody asked, and the conformance suite's reach check
    reads the registry rather than this file, so it would report the verb clean.
    """
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
    raise refuse(
        "refused-by-policy",
        "this verb is destructive and its registry entry declares no decision "
        "made against the plan, so there is nothing for a person to confirm",
        remedy=Remedy.REPORT_DEFECT,
        origin=("tagging", "retag_cli"),
        detail={"verb": ctx.entry.name},
    )


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("folder", help="folder of audio whose genres may be too coarse")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the retag already queued under this identifier",
    )
    parser.set_defaults(_handler=retag_genres)


def retag_argv(job) -> list[str]:
    """The command line that continues one queued retag.

    IT CARRIES ``--run``. The confirm gate is ``explicit``, so R34 makes it
    answerable only by a separate act recorded against a run, and the child
    :mod:`cratekit.core.jobs` spawns is a fresh process in which ``cli.run`` mints
    a NEW run whenever ``--run`` is absent. A resume naming only the job would meet
    the gate with nothing recorded and exit DECISION_REQUIRED, and so would every
    respawn after it, leaving a confirmed sweep in the queue for ever. Two shipped
    verbs were driven to exactly that on 2026-08-23.

    The flag goes BEFORE the verb path because ``--run`` belongs to the root
    parser: a decision belongs to the invocation rather than to the subcommand.

    A job frozen by an older build carries no gate run and resumes without the
    flag, which returns it to the refusal it was already in rather than crashing a
    detached child whose only output is a log nobody is watching.
    """
    payload = job.payload or {}
    folder = str(payload.get("folder") or "")
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]


def retag_genres(ctx) -> Envelope:
    """Offer the selection, wait for the confirmation, then queue the sweep."""
    folder = str(ctx.args.folder or "")
    if not folder:
        raise refuse(
            "tag-retag-folder-unknown",
            "tag retag needs the folder whose genres it should correct",
            steps=("pass the folder after the verb",),
            origin=("tagging", "retag_cli"),
        )
    cfg = _load()
    declared = taxonomy.default_taxonomy()
    items = retag.plan_items(retag.select(Path(folder), declared=declared))
    plan = {
        "digest": digest_of({"kind": "tag.retag", "folder": folder, "items": items}),
        "items": items,
        "totals": {"count": len(items)},
    }
    option = ctx.gate.require(_plan_gate(ctx), digest=plan["digest"])
    if option == "abort":
        return ctx.envelope(
            data={"folder": folder, "totals": plan["totals"], "summary": {"queued": False}},
            outcome=Outcome.NO_OP,
        )
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # THE GATE RUN IS FROZEN so the respawned child can name the run the
            # confirmation was recorded against. See ``retag_argv``.
            payload={"folder": folder, jobs.GATE_RUN_KEY: ctx.run.run_id},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


__all__ = ["build", "retag_argv", "retag_genres"]
