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
for itself. So the ``place`` handed down to the loop COLLECTS the memberships
this run resolved and writes nothing.
:func:`cratekit.write.trees.write_tree_membership` owns its own session and
refuses a caller-supplied gates factory, so calling it from inside this one would
refuse every apply. Two SEQUENTIAL sessions are not a nesting, and that is what
:func:`handle` does.

THE COLLECTION READER LANDED IN U55, so the paragraph that used to sit here about
a census nothing could fill is gone rather than left standing.
:func:`census` reads the configured database, the plan is a plan about the
person's own tracks, and :func:`handle` is the worker behind the ``adopt.apply``
handler key.

WHAT IT STILL DOES NOT DO, said here rather than discovered by somebody watching
an apply refuse. It writes NO TAG. ``apply_plan``'s ``tag_value`` is left at
``None``, which is the value that writes nothing, because a tag write is the one
act no snapshot undoes and this build registers no ``adopt.revert`` verb, so a
person could not undo one. That is recorded in ``docs/residual-findings.md``
with its measured cost.

ITS MEMBERSHIP WRITE NEEDS A TREE THAT HAS CUT OVER, and until R-235 closed that
was a remedy nobody could perform: the write refuses a tree still on the XML
bridge, a tree with no registry record is on the bridge, and nothing under
``src`` recorded a cutover. ``crate tree cutover`` records one now, so the
refusal a person meets on an uncut library names that verb as its step.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.scan_cli`` gives at length: a
modules-layer file reaching for ``registry.Entry`` to annotate a builder is the
layering violation KTD23 refuses, and the output contract is foundation-ranked.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from pathlib import Path

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import artifacts, collection, placements, scan, shell
from cratekit.adopt import plan as plan_engine
from cratekit.adopt.approval import grant
from cratekit.cli.output import Envelope
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    jobs,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Outcome,
    Remediation,
    rebuilt,
    refuse,
)
from cratekit.core.exit_codes import Remedy
from cratekit.write import trees
from cratekit.write.routing_pass import destination

#: The name this run is recorded under in the session log. It is the verb's own
#: name because ``assert_gates`` takes one as a parameter rather than deriving
#: it: that layer names no verb (D2), so the layer that owns verb names supplies
#: one, and a session somebody finds in the log has to say which command opened
#: it rather than which module did.
WORKFLOW = "adopt.apply"

#: The payload key holding who answered the approval gate.
#:
#: FROZEN BECAUSE THE WORKER CANNOT ASK. ``handle`` receives the job, the item
#: and the frozen configuration, and no run, while
#: :func:`cratekit.adopt.approval.grant` refuses an empty actor. Without this key
#: the only actor a worker could supply is one it invented, and an approval
#: naming nobody is exactly what R34 forbids.
ACTOR_KEY = "approved_by"


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


def census(cfg: config.Config, declared: taxonomy.Taxonomy) -> tuple:
    """The scanned rows this run applies: the person's own collection, classified.

    THE READER LANDED IN U55 AND THIS BODY IS WHAT IT WAS FOR. Everything this
    docstring used to say about being empty is now false. It reads the configured
    rekordbox database through :func:`cratekit.adopt.collection.read_collection`,
    which opens it read only, and hands every live row to
    :func:`cratekit.adopt.scan.scan_rows`, which stats the file each row records.
    So this call is the expensive one in an adoption pass and it is where a
    library with unreachable files takes its time.

    AN EMPTY RETURN NOW MEANS AN EMPTY LIBRARY, which is a different fact from
    the missing feature it used to mean, and the two verbs above report it as
    such rather than queueing a job with nothing in it.

    ``declared`` IS A PARAMETER AND WAS NOT. Resolving the taxonomy inside here
    while :func:`current_plan` resolves ``sub`` from the one IT was handed would
    let one plan entry be built from two taxonomies at once, and
    ``test_the_tree_comes_off_the_declared_taxonomy_rather_than_a_flag`` drives
    exactly that call with a modified taxonomy and would have kept passing. That
    is an assertion measuring nothing while genuinely exercising the code, which
    is the first thing ``docs/METHOD.md`` says a green suite cannot see.
    """
    return tuple(
        scan.scan_rows(
            collection.read_collection(cfg),
            declared,
            root=cfg.library.root,
            prefix_map=collection.prefix_rules(cfg),
        )
    )


def current_plan(
    cfg: config.Config, declared: taxonomy.Taxonomy, *, vocals: bool = True
) -> plan_engine.AdoptionPlan:
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

    THE TREE IS READ AS WELL AS THE COLLECTION (R-731), from the database the
    census read, so an entry whose track already holds a competing sub in its
    bucket is withheld and listed rather than added beside it. The census goes
    first, so a library that cannot be read at all refuses the way it always
    did.

    THE VOX TAG AND THE VOCAL SUBS ARE READ IN THAT SAME READ (R-788), so a
    track carrying the tag is planned into its bucket's vocal sub against the
    tree the placements describe and no other.

    ``vocals`` IS FALSE FOR THE MOVE VERB, which builds its plan from this
    one and asks nothing about vocals. It then reads neither the tag tables
    nor the calibration, so a refusal about either cannot stop a move, and
    the plan it gets back plans no vocal membership.
    """
    scanned = census(cfg, declared)
    if not vocals:
        return plan_engine.build_adoption_plan(
            scanned,
            declared,
            tree=declared.tree.id,
            placements=placements.read_placements(cfg, declared),
        )
    held, sung = placements.read_holdings(cfg, declared)
    return plan_engine.build_adoption_plan(
        scanned,
        declared,
        tree=declared.tree.id,
        placements=held,
        vocals=sung,
    )


def _collector(
    into: dict[tuple[str, str], list[str]],
) -> Callable[[plan_engine.PlanEntry, str, str], None]:
    """A ``place`` that records one entry's destination and writes nothing.

    IT GROUPS THE ENTRY'S LOCATION, AND IT USED TO GROUP ITS CONTENT IDENTIFIER.
    This docstring said what it collected was "the mapping
    :func:`cratekit.adopt.apply.membership_plan` produces and
    :func:`cratekit.write.trees.write_tree_membership` consumes", and those are
    two different shapes. ``membership_plan`` groups ``entry.content_id``.
    ``write_tree_membership`` passes every value of its ``plan`` through
    :func:`cratekit.write.trees.match_indexed_rows`, which DECODES it as a
    recorded location and looks it up in an index keyed on resolved paths. A
    content identifier decodes to nothing, every entry comes back ``UNRESOLVED``,
    ``added`` stays zero, and ``MembershipReport`` reports a session that wrote
    nothing as a session that ran. Nothing could see it, because no caller had
    ever handed one mapping to the other function.

    ``membership_plan`` IS LEFT ALONE. It belongs to :mod:`cratekit.adopt.apply`
    with its own contract, and changing what it groups from here would be a second
    opinion about a surface this unit does not own. Recorded as a residual
    instead.

    IT IS STILL A COLLECTOR RATHER THAN A WRITER, and that is the nesting rule the
    module docstring gives: ``write_tree_membership`` owns its own session and
    ``session_lock`` refuses a nested one, so the write happens after this run's
    session has closed. What comes back is what the loop ACTUALLY reached, which
    is a different set from what the plan proposes and is reported as such.
    """

    def place(entry: plan_engine.PlanEntry, folder: str, sub: str) -> None:
        if entry.path:
            into.setdefault((folder, sub), []).append(entry.path)

    return place


def membership_locations(
    entries: Sequence[plan_engine.PlanEntry], declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """The mapping :func:`cratekit.write.trees.write_tree_membership` actually takes.

    KEYED ON DISPLAY NAMES, VALUED WITH LOCATIONS. It is
    :func:`cratekit.adopt.apply.membership_plan` with ``entry.path`` where that
    function has ``entry.content_id``, for the reason :func:`_collector` gives at
    length.

    DERIVED FROM THE PLAN AND NOT FROM THE RUN, which is what makes a crash
    survivable. ``apply_plan`` marks the applied ledger inside its own session and
    the membership write happens after that session closes, so a kill between the
    two leaves entries marked and unwritten. A mapping built from THIS RUN's
    applied set is empty on the re-run, which would make that gap permanent; a
    mapping built from the plan is rewritten in full and ``write_tree_membership``
    reports the rows already there as ``already_present``. On a first run the two
    are equal, which ``tests/test_adopt_workers.py`` asserts rather than assumes.

    AN ENTRY WHOSE DESTINATION THE TAXONOMY NO LONGER DECLARES IS SKIPPED rather
    than raised out of the whole mapping, which is the per-track versus per-pass
    rule ``membership_plan`` already states and U19 already paid for.

    AN ENTRY WITH NO PATH IS SKIPPED TOO. ``plan.applicable()`` already excludes
    every disposition that has none, so this is a belt: a ``None`` path would
    reach ``match_indexed_rows`` as the four character string ``"None"`` and be
    reported as an unresolved location rather than as a bug.
    """
    grouped: dict[tuple[str, str], list[str]] = {}
    for entry in entries:
        if not entry.path:
            continue
        try:
            folder, sub = destination(declared, entry.bucket, entry.sub)
        except KeyError:
            continue
        grouped.setdefault((folder, sub), []).append(entry.path)
    return grouped


def vocal_locations(
    plan: plan_engine.AdoptionPlan, declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """The vocal memberships this plan adds, in the mapping the tree writer takes.

    ONLY THE ADDITIONS, never a track the tree already files there. The plan
    read the tree to tell the two apart, and one of the ways a track is
    already there is through a playlist the writer cannot find by name, where
    handing the row over again would file it a second time.

    NAMED THROUGH :func:`cratekit.write.routing_pass.destination`, the
    resolver the routing pass names a vocal placement through, with the two
    skips :func:`membership_locations` makes and for its reasons.

    DERIVED FROM THE PLAN AND NOT FROM THE RUN, as that mapping is. A run
    stopped after its memberships landed rebuilds a plan that reads those
    tracks as present, so there is nothing to write twice and nothing owed.
    """
    grouped: dict[tuple[str, str], list[str]] = {}
    for entry in plan.vocal_additions():
        if not entry.path:
            continue
        try:
            folder, sub = destination(declared, entry.bucket, entry.vocal_sub)
        except KeyError:
            continue
        grouped.setdefault((folder, sub), []).append(entry.path)
    return grouped


def planned_memberships(
    plan: plan_engine.AdoptionPlan, declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """Every membership one apply hands the tree writer: the entries, then the vocal subs.

    ONE MAPPING AND ONE WRITE, so a vocal membership lands in the session, and
    behind the capture, that the entry beside it does. A VOCAL SUB AND A
    BUCKET'S OWN SUB NEVER SHARE A KEY, and the loader is not what holds
    that: it accepts a bucket whose sub carries the vocal sub's name. The
    plan does, through :func:`cratekit.adopt.plan.vocal_sub`, which answers
    that such a bucket has no vocal sub, so no vocal addition names it.
    """
    wanted = membership_locations(plan.applicable(), declared)
    for key, rows in vocal_locations(plan, declared).items():
        wanted.setdefault(key, []).extend(rows)
    return wanted


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
    one. The analysis share rides with it when the database sits outside the
    root, because in that layout the root holds no grid at all (R-14).

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
    watched: tuple[Path, ...] = analysis_store.watch_roots(cfg)
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


def _digested(plan: plan_engine.AdoptionPlan) -> tuple[dict, dict]:
    """The plan as the approval gate shows it, and the facts beside it (R-693).

    THE ITEMS ARE THE APPLICABLE ENTRIES, because those are the entries the
    digest lists: an approval binds to the work an apply may write, and a
    screen listing every scanned track would move when a track the digest
    does not name changed its recorded location, so a recorded answer would
    stand over a screen that reads differently. What the plan will not touch
    is on the screen as the counts per disposition, which the digest covers
    as well, beside the tree and the collisions. Read off the plan's own
    document, so the two say the same thing.

    THE ENTRIES WITHHELD OVER A PLACE THE TRACK HOLDS ARE LISTED IN FULL
    (R-731), under their own name and with their own count split by kind.
    They are not items, since an apply writes none of them, and they are not
    left as a number either: each is a track whose tag and whose placement
    disagree, and the list is what a person settles that from. The digest
    is taken over the rows as they are shown here, every field.

    EVERY VOCAL MEMBERSHIP AN APPLY MAY WRITE IS LISTED TOO (R-788), under
    its own name, beside the count of every vox tagged track by what the plan
    does about it. The ones the tree already holds are in the list with the
    ones to add, each saying which it is, because the digest covers both and
    a row that goes missing after the answer is written back on the strength
    of it. So no vocal row is written that the person answering was not
    shown.
    """
    document = plan_engine.to_json(plan)
    listed = {entry.entry_id for entry in plan.applicable()}
    return (
        {
            "digest": document["digest"],
            "items": [entry for entry in document["entries"] if entry["id"] in listed],
        },
        {
            "tree": document["tree"],
            "counts": document["counts"],
            "energy": document["energy"],
            "collisions": document["collisions"],
            "placements": document["placements"],
            "withheld_by_placement": document["withheld_by_placement"],
            "held_elsewhere": document["held_elsewhere"],
            "vocals": document["vocals"],
            "vocal": document["vocal"],
            "vocal_memberships": document["vocal_memberships"],
        },
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

    ONE ITEM, AND IT IS THE PLAN. The engine's per item resume is not what makes
    an apply resumable; the applied ledger is, and it is older. One item per
    entry would put two resume mechanisms on one job and would take one full
    ``snapshot.capture`` per track, because ``write_tree_membership`` runs one
    inside its own session. So the item is the plan digest and the zero item rule
    is enforced HERE, by refusing to create a job at all when the plan has
    nothing applicable. A vocal addition is always an applicable entry's, so
    a plan with nothing applicable adds no vocal membership either.

    THE APPROVING ACTOR IS FROZEN. The worker gets ``(job, item, cfg)`` and no
    run, and ``approval.grant`` refuses an empty actor, so the person who
    answered the gate has to travel in the payload or the approval R34 requires
    could only be invented by the worker.
    """
    cfg = _load()
    declared = active_taxonomy.load(cfg)

    if ctx.args.job:
        return _resume(ctx, cfg)

    plan = current_plan(cfg, declared)
    spec = _approval_gate(ctx.entry)
    digested, facts = _digested(plan)
    option = ctx.gate.require(spec, plan=digested, context=facts)
    if option == "abort":
        # ``job_id`` IS THE EMPTY STRING RATHER THAN ``None``. ``cli.output``
        # closes the declared ``job_state/1`` surface with
        # ``additionalProperties: false`` and requires every field as a string,
        # so a null failed this verb's own schema. Nothing validated it, which is
        # why it shipped: the schema fingerprint hashes the DECLARED fields and
        # the golden envelope is a hand written literal. Recorded as R-234 by U51
        # and closed here.
        return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)

    applicable = plan.applicable()
    if not applicable:
        return ctx.envelope(
            data=shell.no_op("no-op"),
            outcome=Outcome.NO_OP,
            warnings=(
                {
                    "code": "adoption-nothing-applicable",
                    "message": (
                        f"this plan holds {len(plan.entries)} track(s) and none of "
                        f"them can be placed, so there is nothing to queue"
                    ),
                },
            ),
        )

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                "tree": plan.tree,
                "digest": plan.digest(),
                # WHO ANSWERED, read off the run record rather than off a flag.
                # R34's whole content is that this class of decision cannot be
                # typed onto the command that was already running.
                ACTOR_KEY: _approving_actor(ctx, spec),
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
            item_ids=(plan.digest(),),
            cfg=cfg,
        )
        return ctx.envelope(data=shell.reported(store, job))


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Answer the gate from the frozen plan, then drive the job's one item.

    THE GATE IS ASKED AGAINST THE REBUILT PLAN, exactly as it was on the way in.
    A digest that has moved meets ``DecisionStale`` here rather than inside the
    worker, which is the earlier and the better place: nothing has been opened
    and nothing has been marked.

    RECONCILE BEFORE DRIVING. A resume arrives after something stopped, and a
    claim left behind by a driver that died is state the queue cannot see for
    itself.

    IT RAISES ON A JOB THAT DID NOT FINISH rather than reporting one. That is
    R-225, and the predicate is ANY CLOSED JOB CARRYING A CAUSE rather than
    FAILED alone: a run stopped with a signal is CANCELLED and carries the cause
    ``jobs.cancel`` builds, so the narrower predicate exits 0 over an interrupted
    apply. SUCCEEDED carries no cause and is unaffected.
    """
    declared = active_taxonomy.load(cfg)
    plan = current_plan(cfg, declared)
    spec = _approval_gate(ctx.entry)
    digested, facts = _digested(plan)
    if ctx.gate.require(spec, plan=digested, context=facts) == "abort":
        return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)

    with jobs.open_store() as store:
        job, warnings = shell.advance(
            ctx,
            store,
            jobs.get(store, ctx.args.job),
            origin=("adopt", "apply_cli"),
            nothing_to_run="report an adoption over a library it never touched",
        )
        return ctx.envelope(
            data=shell.reported(store, job, {"adoption": _summary(cfg, job.job_id)}),
            warnings=warnings,
        )


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say the apply landed.

    READ BACK RATHER THAN ACCUMULATED, so a job continued tomorrow reports what
    every attempt did and not only what this process saw.
    """
    applied: list[str] = []
    failed: dict[str, str] = {}
    added = 0
    already = 0
    playlists: list[str] = []
    for report in artifacts.committed(cfg, job_id):
        applied.extend(str(entry) for entry in report.get("applied") or ())
        failed.update({str(k): str(v) for k, v in (report.get("failed") or {}).items()})
        added += int(report.get("added") or 0)
        already += int(report.get("already_present") or 0)
        playlists.extend(str(name) for name in report.get("playlists") or ())
    return {
        "applied": sorted(set(applied)),
        "failed": failed,
        "added": added,
        "already_present": already,
        "playlists": sorted(set(playlists)),
    }


def handle(job, item, cfg) -> jobs.Produced:
    """Apply one queued plan, then write its memberships. The ``adopt.apply`` worker.

    FIVE STEPS, AND THE ORDER IS THE WHOLE DESIGN.

    1. Rebuild the plan from a fresh census. It is NOT frozen: ``jobs.enqueue``
       freezes the payload and the configuration and neither carries a library.
    2. Refuse ``decision-stale`` when the rebuilt digest is not the frozen one.
       Without this the worker would apply a write set the person never saw, and
       the gate's whole purpose would be answered by a plan that has since moved.
    3. The MEMBERSHIPS, in a session of their own, BEFORE anything is marked.
    4. ``apply_outstanding``, which opens the ONE destructive session and marks
       the applied ledger per entry. It is handed no ``tag_value``, so no tag is
       written: the tag write is the one act no snapshot undoes, the registry
       declares no ``adopt.revert`` verb so a person could not undo one, and seven
       ledger findings against the revert path are unreachable today precisely
       because nothing writes a tag.
    5. Commit the artifact, and only then raise if anything failed.

    THE RECOVERABLE WRITE GOES FIRST, AND THAT ORDER WAS MEASURED RATHER THAN
    REASONED. ``apply_plan``'s own comment argues it for the tag write, and the
    first draft of this worker had the two the other way round: apply, then write
    memberships. Driven on 2026-09-02 against a library whose tree had not been
    cut over, the ledger came back holding every entry while the database held no
    membership row at all, and the next run then found nothing outstanding. A
    membership row lives inside the database snapshot and a ledger mark is what
    suppresses the next attempt, so the write that can be repeated goes first and
    the mark that stops repetition goes last. A kill between them costs one
    re-run, which reports every row as ``already_present``.

    THE TWO SESSIONS ARE SEQUENTIAL AND NEVER NESTED.
    ``write_tree_membership`` owns its own and ``session_lock`` raises
    ``SessionComposition`` on a nested acquisition, so the membership write cannot
    happen inside ``apply_outstanding`` and does not need to.

    IT RAISES RATHER THAN RETURNING A REPORT FULL OF FAILURES.
    ``apply_plan`` catches a ``CratekitError`` from ``place``, records it in
    ``ApplyReport.failed``, and returns normally, and ``jobs.drive`` fails an item
    only when the handler RAISES. A worker that returned here would flip the item
    to done and drive the job to SUCCEEDED over an apply that wrote nothing, which
    is the clean-report-over-unreadable-state cost ``docs/METHOD.md`` names. The
    artifact is committed BEFORE the raise, so what happened survives the failure.

    ON A LIBRARY THAT HAS NOT BEEN CUT OVER THIS ALWAYS RAISES.
    ``tree_registry.anchored_root`` refuses a tree still on the bridge, and an
    unrecorded tree IS on the bridge because ``Registry.mode`` defaults to XML.
    The applied ledger stays empty because nothing was marked, so nothing is
    lost, and the job ends FAILED on a cause a resume does not retry. The way
    on is ``crate tree cutover`` and then this verb again, which are the two
    steps :func:`_write_memberships` puts on the refusal (R-235). Driven in
    ``tests/test_cutover_cli.py``, which is how the second step came to name a
    fresh apply: the first draft named a resume, and the engine refuses one.
    """
    del item
    declared = active_taxonomy.load(cfg)
    plan = current_plan(cfg, declared)
    frozen_digest = str((job.payload or {}).get("digest") or "")
    if plan.digest() != frozen_digest:
        raise refuse(
            "decision-stale",
            "the collection has changed since this adoption was approved, so the "
            "plan this job would apply is not the plan anybody agreed to",
            steps=("run `crate adopt apply` again and approve the plan as it is now",),
            origin=("adopt", "apply_cli"),
            detail={"approved": frozen_digest, "current": plan.digest()},
        )

    # THE APPROVAL IS MINTED BEFORE ANYTHING IS WRITTEN, and is minted again
    # inside ``apply_outstanding`` from the same inputs. That looks redundant and
    # is not: ``require_approval`` runs inside ``apply_plan``, which is AFTER the
    # membership write, so a payload carrying no actor, or an actor
    # ``approval.grant`` refuses, would have written playlist rows into a person's
    # database and only then discovered that the run was never authorised. The
    # result is discarded because the loop owns its own; what is wanted here is
    # the refusal, at the moment it still costs nothing.
    actor = str((job.payload or {}).get(ACTOR_KEY) or "")
    grant(plan, actor=actor)

    membership = _write_memberships(cfg, plan, declared)
    _refuse_unplaced(membership, job, cfg)

    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)

    produced = artifacts.produced(
        cfg,
        job,
        _ITEM_ZERO,
        {
            "tree": report.tree,
            "actor": report.actor,
            "digest": report.digest,
            "applied": list(report.applied),
            "already_applied": list(report.already_applied),
            "failed": dict(report.failed),
            # A LIST OF THREE FIELD OBJECTS RATHER THAN A JOINED KEY. The
            # obvious ``f"{folder}/{sub}"`` collapses two destinations onto one
            # key whenever a display name holds a slash, and the SHIPPED taxonomy
            # has several that do. That is the duplicate-key-in-a-mapping shape
            # ``docs/METHOD.md`` says to hunt, and here it would silently lose
            # half a report.
            "gathered": [
                {"folder": folder, "sub": sub, "rows": rows}
                for (folder, sub), rows in sorted(gathered.items())
            ],
            "added": membership.added,
            "already_present": membership.already_present,
            "playlists": list(membership.playlists),
            "unplaced": [str(match.requested) for match in membership.skipped],
            "skipped": [match.requested for match in membership.skipped],
        },
    )
    if report.failed:
        _commit(produced)
        raise refuse(
            "adopt-entries-failed",
            f"{len(report.failed)} of this plan's entries could not be applied: "
            f"{', '.join(sorted(report.failed))}",
            steps=("read the committed artifact under the queue root for each entry's reason",),
            origin=("adopt", "apply_cli"),
            detail={"failed": sorted(report.failed)},
        )
    return produced


def _refuse_unplaced(
    membership: trees.MembershipReport, job, cfg: config.Config
) -> None:
    """Refuse before the ledger is marked when a row could not be placed.

    THE HAZARD THIS CLOSES IS R-148 WEARING A NEW SHAPE.
    ``write_tree_membership`` SURFACES a row it could not resolve to exactly one
    active library row rather than raising on it, correctly: one unresolvable
    file is not a reason to abandon a session. But the caller then marks every
    outstanding entry applied, including the ones that were surfaced, so a track
    that never reached a playlist is recorded as adopted and
    ``apply.outstanding`` never offers it again. The ledger would say the library
    holds something it does not.

    IT REFUSES RATHER THAN MARKING THE REST, which is the conservative direction
    and costs nothing that a re-run does not recover. Nothing has been marked
    when this fires, so every membership row that DID land is reported
    ``already_present`` on the next attempt and the entries behind them are
    marked then. The alternative, dropping the surfaced entries from the plan and
    marking the others, keeps the run green at the price of a plan whose digest
    no longer matches the approval it is being applied under.

    THE REFUSAL NAMES THE ROWS. A count is not something a person can act on; the
    recorded location is, because the two shapes that reach here are a location
    the library has two live rows for and a location it has none for, and both
    are fixed in rekordbox rather than here.
    """
    if not membership.skipped:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    artifacts.write(
        artifacts.staged_path(cfg, job.job_id, _ITEM_ZERO.ordinal),
        {"unplaced": unplaced, "added": membership.added, "playlists": list(membership.playlists)},
    )
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} track(s) in this plan could not be placed in the "
        f"library tree, so nothing has been recorded as adopted: "
        f"{', '.join(unplaced)}",
        steps=(
            "check each named file in rekordbox: the library holds either two "
            "live rows for it or none, and both are repaired there",
        ),
        origin=("adopt", "apply_cli"),
        detail={"unplaced": unplaced},
    )


def _commit(produced: jobs.Produced) -> None:
    """Make the staged artifact durable before raising past the engine.

    ``jobs.drive`` commits a handler's ``Produced`` only on the path where the
    handler RETURNS one. A worker that raises therefore loses its report unless it
    commits first, and losing the report is losing the only record of which
    entries failed and why.
    """
    if produced.staged is not None and produced.final is not None:
        jobs.commit_artifact(produced.staged, produced.final)


def _write_memberships(
    cfg: config.Config,
    plan: plan_engine.AdoptionPlan,
    declared: taxonomy.Taxonomy,
) -> trees.MembershipReport:
    """Write the plan's memberships in a session of their own.

    THE HANDLE IS THIS FUNCTION'S OWN AND IT IS A WRITE. ``write_tree_membership``
    commits through the handle it is given, so this one is opened with
    ``require_closed=True``: the two-process refusal and the application pin both
    run before anything opens, which is the open a write is supposed to make. That
    is stricter than ``cratekit.write.routing_cli``, which writes through a
    ``require_closed=False`` open; the divergence is deliberate and is recorded
    rather than copied.

    THE READER'S HANDLE COULD NOT BE REUSED. It is closed before
    :func:`cratekit.adopt.collection.read_collection` returns, and that module
    holds no write capable open by construction.

    THE ROWS COME FROM THE READER, which returns
    :class:`cratekit.adopt.scan.CollectionRow` rather than
    :class:`cratekit.write.trees.ContentRow`. ``index_active_rows`` reads exactly
    three attributes, ``content_id``, ``recorded`` and ``deleted``, and both
    records carry all three, so the substitution is structural and deliberate
    rather than a type error nobody noticed.
    """
    target = rb_writer.live_db_path(cfg)
    handle = rb_writer.open_db(
        target,
        require_closed=True,
        cfg=cfg,
    )
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        return trees.write_tree_membership(
            cfg,
            handle,
            tree_id=plan.tree,
            registry=tree_registry.read(cfg),
            plan=planned_memberships(plan, declared),
            rows=collection.read_collection(cfg),
            root_exists=lambda root_id: root_id in known,
            # THE LIBRARY ROOT and the analysis share, never empty. The watch it
            # arms is the runtime half of R17's fifth surface and it watches
            # nothing when nobody names a root, which reports a clean session
            # either way.
            analysis_roots=analysis_store.watch_roots(cfg),
            prefix_map=collection.prefix_rules(cfg),
        )
    except tree_registry.TreeModeRefused as exc:
        named = _naming_the_cutover(exc)
        if named is None:
            raise
        raise named from exc
    finally:
        rb_writer.close_db(handle)


def _naming_the_cutover(exc: tree_registry.TreeModeRefused) -> CratekitError | None:
    """The bridge refusal, with the verb that answers it as its step (R-235).

    THE REFUSAL IS RAISED IN ``core``, WHICH MAY NAME NO VERB (D2), so it arrives
    carrying a remedy token and no act. This layer may name one, and the act
    exists now. The slug, the sentence and the detail are the refusal's own and
    are carried unchanged; what is added is the step and this hop in the origin.

    ONLY THE DIRECTION THIS VERB CAN MEET IS REWORDED. A database write refused
    because the tree is on the bridge is answered by a cutover. For any other
    refusal of that type this answers None and the caller re-raises it as it
    came.
    """
    if exc.attempted != tree_registry.Mode.DATABASE or exc.mode != tree_registry.Mode.XML:
        return None
    cause = exc.cause
    return rebuilt(
        exc,
        replace(
            cause,
            remediation=Remediation(
                remedy=cause.remediation.remedy,
                steps=(
                    f"take a Fresh Export from rekordbox, then run `crate tree "
                    f"cutover {exc.tree_id} --export <that file>`; it names "
                    f"anything else the library owes before a tree can cut "
                    f"over, a snapshot or an import, and asks for approval "
                    f"once nothing is",
                    "once the tree has cut over, run `crate adopt apply` again "
                    "and approve the plan; this job ended on a cause a resume "
                    "cannot retry, and nothing it planned was marked applied",
                ),
            ),
            origin=(*cause.origin, "adopt.apply_cli"),
        ),
    )


class _Item:
    """The ordinal :mod:`cratekit.adopt.artifacts` needs, for a one item job."""

    def __init__(self, ordinal: int) -> None:
        self.ordinal = ordinal


#: An apply has exactly one item, so its artifact always has ordinal zero.
_ITEM_ZERO = _Item(0)


def _approving_actor(ctx, spec) -> str:
    """Who the run record says answered the approval gate.

    OFF THE RECORDED DECISION rather than off ``ctx.gate.actor``, which is the
    default the CLI carries and is ``"cli"`` for a run nobody decided. R34 asks
    which ACTOR asserted the decision, and the answer lives on the decision.
    """
    decision = ctx.run.decisions.get(spec.name)
    return decision.actor if decision is not None else ""


__all__ = [
    "WORKFLOW",
    "adopt_apply_argv",
    "apply_adoption",
    "apply_outstanding",
    "build",
    "census",
    "current_plan",
    "handle",
    "membership_locations",
    "planned_memberships",
    "vocal_locations",
]
