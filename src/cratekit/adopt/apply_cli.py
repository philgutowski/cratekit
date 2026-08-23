"""``crate adopt apply``: approve one adoption plan, then apply it under one session.

WHY THIS IS A MODULE OF ITS OWN, and not beside its sibling. ``adopt.scan``
reads, declares no gate and is not destructive; this verb writes a genre tag onto
a user's own file, which is the one operation in this product that no snapshot
holds and no re-import puts back. The two shared a ``module=`` string once and
the half that was ready was held behind the half that was not. See
``ADOPT_APPLY_CLI_UNIT`` in :mod:`cratekit.cli.registry` for the whole judgement.

THE WALL IN FRONT OF THIS VERB IS DOWN, and it was never the absence of a
database. It was two properties of ``test_conformance_3`` itself, recorded as the
residual titled "Conformance 3 cannot pass a verb with an explicit gate, and the
reason is not the database": the suite answered every gate inline with ``-d``,
which ``Gates.require`` correctly refuses for an ``explicit=True`` gate, and it
drove once per gate on a fresh run, so a verb declaring two gates always exited
DECISION_REQUIRED on the other one. This verb has both shapes at once. Conformance
3 now answers an explicit gate the way a person does, through ``crate run decide``
on the run it already reached, and resumes that run for the next gate.

THE SESSION IS THE POINT OF THIS UNIT, not the argument parser. The residual
titled "Adoption's tag write takes no destructive session and no library lock"
says :func:`cratekit.adopt.apply.apply_plan` writes a file with nothing asserting
that rekordbox is closed, that a backup was acknowledged, or that the volume
identity still matches, and with nothing stopping two runs reaching one file
twice. That module says so in its own docstring and declines to fix it there,
correctly: R29 declares the destructive-session boundary as one source per run
and a loop is not a run. :func:`apply_outstanding` below is the run, so the
session opens there, once, around the whole loop.

SESSIONS DO NOT NEST, and that is enforced rather than advised:
:func:`cratekit.core.session.session_lock` raises ``SessionComposition`` when one
is opened inside another in the same process, because the second acquisition can
never succeed and reporting it as a foreign holder would tell a caller to wait
for itself. So the ``place`` handed down here COLLECTS the memberships this run
resolved and writes nothing.
:func:`cratekit.write.trees.write_tree_membership` owns its own session and
refuses a caller-supplied gates factory, so calling it from inside this one would
refuse every apply. The collected mapping is returned instead, in the shape
:func:`cratekit.adopt.apply.membership_plan` produces, so the caller that holds a
database writes it after this session has closed.

WHAT THIS UNIT DOES NOT LAND, said here rather than discovered by somebody
watching an apply report zero entries. It does not read the collection. Turning a
rekordbox library into :class:`cratekit.adopt.scan.CollectionRow` values needs a
collection reader that no unit in this build lands, which is the same position
``adopt.scan`` shipped in and says so in the same words. The census this verb
rebuilds is therefore empty, the plan it digests is the empty plan, and nothing
is outstanding. The session boundary is real and driven on a synthetic plan in
``tests/test_adopt_apply_cli.py``; what is absent is the input, not the guard.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.scan_cli`` gives at length: a
modules-layer file reaching for ``registry.Entry`` to annotate a builder is the
layering violation KTD23 refuses, and the output contract is foundation-ranked.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import plan as plan_engine
from cratekit.adopt.approval import grant
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, session, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy

#: The name this run is recorded under in the session log. It is the verb's own
#: name because ``assert_gates`` takes one as a parameter rather than deriving
#: it: that layer names no verb (D2), so the layer that owns verb names supplies
#: one, and a session somebody finds in the log has to say which command opened
#: it rather than which module did.
WORKFLOW = "adopt.apply"


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token rides through from the configuration error that raised it,
    so "no config at all" and "config written by a newer build" keep their
    different answers all the way out to the shell. Flattening them here would
    put this layer back in the business of writing instructions, which is what D2
    removes from every layer but the outermost.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("adopt.apply_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def census(cfg: config.Config) -> tuple:
    """The scanned rows this run applies. Empty until a collection reader lands.

    A FUNCTION RATHER THAN A LITERAL AT THE ONE CALL SITE, because the thing that
    is missing is worth naming once where a later unit will look for it. It takes
    the config it will eventually need so that supplying a reader is a change to
    this body and to nothing that calls it.

    IT RETURNS EMPTY RATHER THAN REFUSING. An apply with nothing to apply is a
    correct outcome and the state every library is in before its first census; a
    refusal here would make the verb unreachable and would report a missing
    feature as a broken machine.
    """
    del cfg
    return ()


def current_plan(cfg: config.Config, declared: taxonomy.Taxonomy) -> plan_engine.AdoptionPlan:
    """Rebuild the plan this run is approving, from the census rather than a file.

    THE PLAN IS NOT A FILE, and that is R26's decision rather than an omission
    here. A plan approved thirty percent through and resumed in a later session
    needs verdicts that outlive the process that collected them, which is what
    the review queue holds and what a file somebody edits cannot give it. So the
    plan is rebuilt on every run and the applied ledger, not the plan, is what
    carries progress across runs.

    THE TREE COMES OFF THE DECLARED TAXONOMY, never off a flag. A taxonomy
    declares exactly one routing tree by stable identifier (R19), so an argument
    naming one could only hold that identifier or a mistake.
    """
    return plan_engine.build_adoption_plan(census(cfg), declared, tree=declared.tree.id)


def _reported(store, job) -> dict:
    """One job as the ``job_state`` payload, which is what this verb emits."""
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def _collector(
    into: dict[tuple[str, str], list[str]],
) -> Callable[[plan_engine.PlanEntry, str, str], None]:
    """A ``place`` that records one entry's destination and writes nothing.

    It is handed the display names :mod:`cratekit.adopt.apply` already resolved,
    and groups by that pair, so what comes back is the mapping
    :func:`cratekit.adopt.apply.membership_plan` produces and
    :func:`cratekit.write.trees.write_tree_membership` consumes. Building it here
    rather than calling ``membership_plan`` afterwards keeps the collected set
    equal to what the loop ACTUALLY reached: an entry the loop failed or skipped
    is absent from this mapping, where a second derivation from the plan would
    put it back in.
    """

    def place(entry: plan_engine.PlanEntry, folder: str, sub: str) -> None:
        into.setdefault((folder, sub), []).append(entry.content_id)

    return place


def apply_outstanding(
    cfg: config.Config,
    plan: plan_engine.AdoptionPlan,
    declared: taxonomy.Taxonomy,
    *,
    actor: str,
    tag_value: Callable[[plan_engine.PlanEntry, taxonomy.Taxonomy], str | None] | None = None,
    identity_provider: object | None = None,
    mount_enumerator: object | None = None,
) -> tuple[apply_engine.ApplyReport, Mapping[tuple[str, str], list[str]]]:
    """Apply the outstanding entries of one plan inside ONE destructive session.

    This is the function the residual named at the top of this module closes.
    Every tag write in the loop now happens with the volume identity asserted,
    the backup acknowledgment asserted, and the whole-run lock held, and two
    concurrent applies over one library meet that lock instead of meeting one
    file twice.

    ``analysis_roots`` NAMES THE LIBRARY ROOT rather than being left empty. The
    watch it arms is the runtime half of R17's fifth surface, and it watches
    nothing when nobody names a root, which is worse than an absent guard because
    it reports a clean session either way. A tag write can touch any file under
    the library, so the library root is the honest answer and not a conservative
    one.

    THE TWO PREFLIGHT SEAMS ARE FORWARDED AS THEY ARRIVE, ``None`` included.
    ``assert_gates`` reads ``None`` as "resolve the default", which is exactly
    what a caller supplying nothing means, so a branch here choosing between
    omitting the argument and passing ``None`` would be two spellings of one
    behaviour and a branch no test could tell apart. The seams exist so a test can
    drive the three refusals without a real volume.

    THE APPROVAL IS MINTED FROM THE DECISION, not from a flag. ``actor`` is who
    the run record says answered the explicit gate, so the approval this plan is
    applied under names the person who gave it. R34's whole content is that this
    class of decision cannot be typed onto the command that was already running,
    and an approval whose actor came from ``--actor`` would put it back.

    IT RETURNS THE MEMBERSHIPS RATHER THAN WRITING THEM, for the nesting reason
    the module docstring gives. The mapping is empty when the loop placed
    nothing, which is a different fact from an empty plan and the caller can tell
    them apart by the report.
    """
    gathered: dict[tuple[str, str], list[str]] = {}
    watched: tuple[Path, ...] = (cfg.library.root,)
    with session.assert_gates(
        cfg,
        workflow=WORKFLOW,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ):
        report = apply_engine.apply_plan(
            cfg,
            plan,
            declared,
            approval=grant(plan, actor=actor),
            place=_collector(gathered),
            tag_value=tag_value,
        )
    return report, gathered


def build(parser, entry) -> None:
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this layer importing the one above it. See the module docstring.

    THERE IS NO ``--approve`` AND NO ``--yes``. The approval is the recorded
    answer to the explicit gate and there is no flag anywhere in this package
    that stands in for one (R34).
    """
    del entry
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue the adoption pass already queued under this identifier "
            "rather than queueing a new one; this is how a resume re-invokes "
            "the verb"
        ),
    )
    parser.set_defaults(_handler=apply_adoption)


def adopt_apply_argv(job) -> list[str]:
    """The command line that continues one queued adoption pass.

    The contract every long-running verb owes. The payload is frozen at queue
    time (KTD9), so only the verb that queued it knows how to turn it back into
    an invocation, and it names the JOB rather than re-stating the request, which
    is what stops a resume queueing a second record for one piece of work.
    ``job`` is a ``cratekit.core.jobs.Job`` and is unannotated for the layering
    reason the module docstring gives.

    IT CARRIES ``--run``, AND WITHOUT IT THIS JOB COULD NEVER BE DRIVEN. The
    approval gate is ``explicit``, so R34 makes it answerable only by a separate
    recorded act against a run, never inline. A resume that minted a fresh run
    would meet the gate again with nothing recorded against it and exit
    DECISION_REQUIRED, every time, for ever: the job driver would respawn a child
    that refuses, and the queue would hold a job nobody could advance. Measured on
    2026-08-23 by driving exactly the argv this function returns.

    SO THE RUN IS FROZEN IN THE PAYLOAD, and the resume continues the run that
    holds the approval rather than asking for it again. That is the same act
    ``crate run decide`` records and the same resume the conformance suite drives,
    and it is why the approval cannot be laundered: a run with no recorded
    decision resumes to the same refusal a fresh one would.

    A JOB QUEUED BY AN OLDER BUILD HAS NO ``run_id`` and is handled rather than
    crashed on. It resumes without the flag, meets the gate, and refuses
    resumably, which is the state it was already in.
    """
    run_id = (job.payload or {}).get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(run_id)] if run_id else []
    return [*resume, "adopt", "apply", "--job", job.job_id]


def _approval_gate(entry):
    """The explicit approval gate off the entry, found by digest source.

    BY ``digest_source`` RATHER THAN BY POSITION. This verb declares two gates
    and the shared cloud-sync one is raised by the guarded writer rather than
    asked here, so indexing ``gates[0]`` would bind this handler to the order
    they happen to be written in and would ask the wrong question the day
    somebody reorders them.
    """
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
                f"there is no question to ask before applying one"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("adopt.apply_cli",),
            detail={"verb": entry.name},
        )
    )


def apply_adoption(ctx) -> Envelope:
    """Ask the approval gate against this plan, then queue the pass.

    THE PLAN IS BUILT BEFORE THE GATE, because the gate's digest IS the plan. An
    approval is recorded against a digest so a plan that has since moved is
    refused rather than applied, and a person who approved a different plan does
    not have their answer honoured against this one.

    AN EMPTY PLAN STILL ASKS. Conformance 3 holds every declared gate to firing,
    and "nothing to adopt" is a plan a person can still abort. Skipping the
    question when the plan is empty would also make the one library that most
    needs the question, the one whose census has not run, the one library that is
    never asked.

    NO DESTRUCTIVE SESSION OPENS HERE. Queueing writes nothing to the library, and
    a session opened to do zero work refuses on a machine that has not
    acknowledged a backup, which would make the verb unreachable on exactly the
    machine adoption is for. The session opens in :func:`apply_outstanding`,
    which is the run that touches files.
    """
    cfg = _load()
    declared = taxonomy.default_taxonomy()
    plan = current_plan(cfg, declared)

    spec = _approval_gate(ctx.entry)
    option = ctx.gate.require(spec, digest=plan.digest())
    if option == "abort":
        return ctx.envelope(
            data={"job_id": None, "state": "declined", "cause": None, "progress": {}},
            outcome=Outcome.NO_OP,
        )

    with jobs.open_store() as store:
        if ctx.args.job:
            # RECONCILE FIRST. A resume arrives after something stopped, and a
            # claim left behind by a driver that died is the state the queue
            # cannot see for itself.
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                "tree": plan.tree,
                "digest": plan.digest(),
                # FROZEN SO THE APPROVAL SURVIVES THE RESPAWN. See
                # ``adopt_apply_argv``: the gate is explicit, so a resume on a
                # fresh run can never be answered and the job would be
                # undriveable.
                #
                # UNDER THE SHARED KEY rather than a local spelling, so the one
                # guard that derives this obligation from the registry covers
                # this verb and every later one without being edited.
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


__all__ = [
    "WORKFLOW",
    "adopt_apply_argv",
    "apply_adoption",
    "apply_outstanding",
    "build",
    "census",
    "current_plan",
]
