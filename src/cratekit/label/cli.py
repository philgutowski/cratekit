"""``crate label`` and ``crate sync labels``: registry, sweep, import, harvest.

Builders take an untyped ``entry`` so this file does not import the CLI
registry (KTD23). Long-running work queues a job. The increment engine is
``cratekit.sync.run.increment``; this shell freezes the source id and the
run id so two sources queued by ``sync all`` still share one intake file.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, harvest, sweep
from cratekit.label import registry as labels
from cratekit.sync import artifacts, run, watermarks


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("label.cli",),
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


def build_registry(parser, entry) -> None:
    parser.add_argument(
        "action",
        nargs="?",
        default="list",
        choices=("list", "add", "remove", "rename"),
        help="list (default), add, remove, or rename a favourite label",
    )
    parser.add_argument("name", nargs="?", help="display name or identifier")
    parser.add_argument("--to", dest="new_name", default=None, help="new display name")
    parser.add_argument("--match", default=None, help="copyright match needle")
    parser.set_defaults(_handler=registry_cmd)


def build_sync(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the increment already queued under this identifier",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        dest="run_id",
        help="intake run shared with the other sources in this sync",
    )
    parser.set_defaults(_handler=sync_labels)


def build_import(parser, entry) -> None:
    parser.add_argument("name", help="favourite label to import")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the import already queued under this identifier",
    )
    parser.set_defaults(_handler=import_label)


def build_harvest(parser, entry) -> None:
    parser.add_argument("playlist", help="playlist to harvest labels from")
    parser.set_defaults(_handler=harvest_playlist)


def sync_labels_argv(job) -> list[str]:
    argv = ["sync", "labels", "--job", job.job_id]
    run_id = (job.payload or {}).get("run_id")
    if run_id:
        argv.extend(["--run-id", str(run_id)])
    return argv


def label_import_argv(job) -> list[str]:
    name = str((job.payload or {}).get("name") or "")
    return ["label", "import", name, "--job", job.job_id]


def _checks_for(held: labels.Registry) -> list[dict]:
    if not held.labels:
        return [
            {
                "key": "labels.empty",
                "title": "favourite labels",
                "status": "ok",
                "detail": "no labels are registered",
                "remedy": None,
            }
        ]
    return [
        {
            "key": f"labels.{entry.label_id}",
            "title": entry.name,
            "status": "ok",
            "detail": entry.label_id,
            "remedy": None,
        }
        for entry in held.labels.values()
    ]


def registry_cmd(ctx) -> Envelope:
    store = labels.RegistryStore()
    action = ctx.args.action
    if action == "list":
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"count": len(held.labels)},
            }
        )
    name = ctx.args.name
    if not name:
        raise refuse(
            "label-name-invalid",
            f"label registry {action} needs a name",
            steps=("pass the label name after the action",),
            origin=("label.cli",),
        )
    if action == "add":
        label_id = store.add(name, match=ctx.args.match)
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"added": label_id, "count": len(held.labels)},
            }
        )
    if action == "remove":
        removed = store.remove(name)
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"removed": removed, "count": len(held.labels)},
            }
        )
    if ctx.args.new_name is None:
        raise refuse(
            "label-name-invalid",
            "renaming a label needs the new display name on --to",
            steps=("pass --to with the new name",),
            origin=("label.cli",),
        )
    entry = store.load().resolve(name)
    if entry is None:
        raise refuse(
            "label-unknown",
            f"no favourite label is named {name!r}",
            steps=("list the registry and take the identifier from it",),
            origin=("label.cli",),
            detail={"name": name},
        )
    store.rename(entry.label_id, ctx.args.new_name)
    held = store.load()
    return ctx.envelope(
        data={
            "checks": _checks_for(held),
            "summary": {"renamed": entry.label_id, "count": len(held.labels)},
        }
    )


def queue_warnings() -> tuple[dict[str, str], ...]:
    """What a person should know at the moment they queue, rather than later.

    THE UNBOUND CATALOGUE IS A WARNING AND NOT A REFUSAL, which is the honest
    half of leaving the refusal to the worker. ``catalogue.bound`` says why the
    question is asked here at all: :func:`cratekit.label.catalogue.resolve`
    raises, and asking it at enqueue would refuse work a later build could run.
    What it would cost to say nothing is worse than it looks, because the worker
    runs inside a detached child whose only output is a log nobody is watching,
    so a person who is only told at drive time was told at the one moment they
    could do nothing with it.

    THE NAME IS SHARED WITH ``cratekit.modules.outbound.shell.queue_warnings``
    ON PURPOSE, and ``docs/METHOD.md`` warns about exactly one symbol meaning two
    things in two modules, so this is the line that says which of the two this
    is. It is the SAME thing on a second seam, the way ``_load`` and ``_reported``
    are already spelled once per queueing shell, rather than a second meaning for
    one word. What differs is only what each one has to look at: the outbound
    shell also reports the export rows it could not resolve, and a label sweep
    resolves nothing at enqueue by construction (KTD2), so this one asks a single
    question and takes no arguments at all.
    """
    if catalogue.bound():
        return ()
    return (
        {
            "code": "label-catalogue-unbound",
            "message": (
                "this build has no catalogue adapter for the label package, so "
                "this job will queue and then fail at the provider seam"
            ),
        },
    )


def _queue(ctx, *, payload: dict, item_ids: tuple[str, ...]) -> Envelope:
    """Queue one label job. The QUEUEING path only; a resume never reaches here.

    ``item_ids`` IS A REQUIRED ARGUMENT rather than one defaulting to empty, and
    the default is what U52 removed. ``jobs.drive`` transitions a job whose
    item count is zero straight to SUCCEEDED, because nothing was attempted and
    nothing failed, so a shared helper that let a caller forget its items was one
    keyword away from a clean report over work the product never did. Each verb
    now has to say what its job is made of, and each says it in a different way:
    the sweep from the registry, the import from the entry it already resolved.

    IT USED TO REPORT A RESUME TOO, and :func:`_resume` took that half over when
    the workers were bound. The branch is gone rather than left beside a second
    one: a resume now drives, and two functions that both answer ``--job`` is how
    one of them keeps answering it by reporting.
    """
    cfg = _load()
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            item_ids=item_ids,
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job), warnings=queue_warnings())


def _refuse_an_itemless_job(store, job) -> None:
    """Refuse to drive a label job with no items, rather than succeeding at it.

    THE JOB THIS CATCHES WAS QUEUED BY A BUILD THAT COULD NOT RUN IT. Before U52
    both label verbs called ``enqueue`` with no ``item_ids`` at all, and the queue
    is a durable file whose schema this unit does not change, so a person who
    upgrades still has those jobs sitting in it. Binding the handlers is what
    makes them drivable, and driving one is the exact hazard: ``jobs.drive``
    transitions a job whose item count is zero straight to SUCCEEDED, because
    nothing was attempted and nothing failed. The person resumes a sweep filed
    weeks ago and is told it succeeded, over a registry nothing was read from.

    A REFUSAL RATHER THAN A REPAIR. Filling the items in from today's registry
    would be the friendlier answer and it is the wrong one: the payload was frozen
    by a build with a different idea of what a label job is, and inventing items
    for it here would run work under a configuration snapshot nobody checked
    against this shape. Filing a new job costs a command and is honest.

    IT IS THE THIRD SPELLING OF ONE REFUSAL, and that is named rather than
    hidden. ``src/cratekit/backup/cli.py``'s ``_refuse_an_empty_job`` and
    ``src/cratekit/modules/outbound/shell.py``'s inline version say the same
    thing, and the only place that could own it for all three is the job engine,
    where the check belongs to ``drive`` itself. Changing that engine is outside
    this branch by its own stop conditions, so the duplication is accepted here
    and recorded, rather than paid for with a change to the one function every
    queued verb in the product runs through.
    """
    if jobs.items(store, job.job_id):
        return
    raise refuse(
        "internal-error",
        f"job {job.job_id} has no items to run, so driving it would report a "
        f"success over work it never did. It was queued by a build that did not "
        f"record what its items were",
        remedy=Remedy.REPORT_DEFECT,
        origin=("label.cli",),
        detail={"job_id": job.job_id},
    )


def _resume(ctx, job_id: str) -> Envelope:
    """Continue the label job named on ``--job``, and report how it ended.

    ONE OWNER FOR BOTH VERBS, which is a decision rather than an accident of
    factoring. The sweep and the import differ in what they queue and in nothing
    at all about how a queued job is continued: neither declares a gate, neither
    reads its payload here, and both report the same ``job_state/1`` envelope.
    Each guard below is a defect somebody already shipped, and a second copy is
    how one of them gets repaired while the other keeps the bug. U51
    landed a shared owner for the same shape in ``modules/outbound/shell.py`` on
    exactly that reasoning.

    THAT FUNCTION IS NOT REUSED, and KTD8 says why: it calls ``ctx.gate.require``
    unconditionally and computes its digest from the fixed outbound triple of
    playlist, export and tracks. Neither label verb declares a gate and neither
    carries those payload keys, so reusing it would mean teaching it that its own
    contract is optional. Two fragments are lifted, not the function.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim left
    behind by a driver that died is state the queue cannot see for itself.

    THE LIVE CONFIGURATION IS NOT LOADED HERE. The job carries the configuration
    it was frozen against and ``handlers.run_job`` reads it off the job, so a
    resume that loaded one would be able to refuse over a setting this run does
    not use. Drift against the current file is computed by the driver, which
    already tolerates a configuration that cannot be read at all.

    THE REGISTRY IS NOT READ HERE EITHER. The job's items were frozen when it was
    queued, so a label registered since then must not decide whether an existing
    job may be continued, and an emptied registry must not refuse to continue one
    whose items are all still sitting in the queue. The worker asks the registry
    per item, which is where a label that has since been removed is answered for.
    """
    with jobs.open_store() as store:
        job = jobs.reconcile(store, job_id)
        warnings: tuple[dict[str, str], ...] = ()
        if job.is_open():
            _refuse_an_itemless_job(store, job)
            # A job every one of whose items failed raises out of here rather than
            # reaching the report, which is correct: the engine has already
            # recorded the job as failed and the refusal carries the item's own
            # cause nested inside it.
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
        # A JOB THAT ENDED BADLY IS NOT AN OK EXIT, and this is the only place
        # that can say so. ``jobs.drive`` raises only when EVERY attempted item
        # failed, so a sweep where one label offered and another could not be
        # listed returns normally with the job recorded failed, and without this
        # the verb exits 0 over half a sweep.
        #
        # IT SITS OUTSIDE THE ``is_open`` BRANCH. ``backup/cli.py``'s own comment
        # records that putting it inside was its first draft's bug: a job already
        # FAILED on entry is not open, so the drive is skipped and the check would
        # be skipped with it, and the second ask about a half failed job exits 0
        # for ever after. ``master/cli.py``'s resume branch has no re-raise at all,
        # which is R-225 and is the thing this is deliberately not a copy of.
        #
        # ANY CLOSED JOB CARRYING A CAUSE, not FAILED alone. A run stopped with a
        # signal is CANCELLED and carries the cause ``jobs.cancel`` builds; the
        # narrower predicate was measured on 2026-09-02 as exit 0 over a job with
        # 0 of 3 items done. SUCCEEDED carries no cause and is unaffected.
        if not job.is_open() and job.cause is not None:
            raise CratekitError(job.cause)
        return ctx.envelope(data=_reported(store, job), warnings=warnings)


def sweep_items(held: labels.Registry) -> tuple[str, ...]:
    """The items one sweep job carries: one per registered favourite label.

    ONE FAVOURITE LABEL IS ONE ITEM (KTD1), and the identifier is the item id
    rather than the display name. Seam R19 and the registry's own D5 both forbid
    keying a persisted record on a name, and an item row is exactly that: a
    rename would move the name and leave the queue holding a label nothing can
    resolve.

    DERIVED FROM THE REGISTRY AND NEVER FROM A PROVIDER LISTING (KTD2).
    ``src/cratekit/backup/cli.py`` established the rule and states the reason:
    items must be derivable without touching the machine, so queueing cannot
    refuse where the work would have run once claimed. Listing the catalogue here
    would also freeze a snapshot that has moved by the time the driver claims it,
    and the registry is a local state document that needs no provider at all.
    """
    return tuple(entry.label_id for entry in held.labels.values())


def _sweep_items_or_refuse() -> tuple[str, ...]:
    """The sweep's items, or the refusal an empty registry earns.

    THE ZERO ITEM RULE, enforced before anything is written. A job with no items
    drives straight to SUCCEEDED, so queueing one here would file a sweep that
    reports a clean success over a registry it never read a label from. The
    remedy is a COMMAND rather than a diagnostic, because what is missing is a
    decision nobody has made yet rather than a fault in this installation.
    """
    items = sweep_items(labels.RegistryStore().load())
    if items:
        return items
    raise refuse(
        "label-registry-empty",
        "no favourite label is registered, so a sweep would queue a job with "
        "nothing to claim and would then report that it succeeded",
        steps=(
            "register a label with: crate label registry add <name>",
            "then run the sweep again",
        ),
        origin=("label.cli",),
    )


def sync_labels(ctx) -> Envelope:
    # THE RESUME IS ANSWERED FIRST, so the registry is read only on the queueing
    # path. It is a structural guarantee rather than a rule to remember: nothing
    # below this line runs for a job that already exists, so a label registered
    # since a job was queued cannot decide whether that job may be continued.
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    run_id = getattr(ctx.args, "run_id", None) or ctx.run.run_id
    return _queue(
        ctx,
        payload={"source_id": "labels", "run_id": run_id},
        item_ids=_sweep_items_or_refuse(),
    )


def import_label(ctx) -> Envelope:
    # THE SAME ORDER, and it moves one refusal for this verb: a resume no longer
    # refuses ``label-unknown`` for a label removed since the job was queued. That
    # is the correct place to lose it. The job holds one frozen item, and the
    # worker asks the registry for exactly that identifier, so the same condition
    # is still refused, per item, where a person is told which label it was.
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    held = labels.RegistryStore().load()
    entry = held.resolve(ctx.args.name)
    if entry is None:
        raise refuse(
            "label-unknown",
            f"no favourite label is named {ctx.args.name!r}",
            steps=("add the label to the registry before importing it",),
            origin=("label.cli",),
            detail={"name": ctx.args.name},
        )
    # ONE LABEL IS ONE ITEM, and there is NO ZERO ITEM GUARD on this path on
    # purpose. The refusal directly above makes one unreachable: an entry that
    # could not be resolved never reaches here, and one that could always yields
    # exactly one identifier. A guard would be a second check of a condition the
    # refusal already decides, and the copy that goes stale is the one nothing
    # can drive.
    return _queue(
        ctx,
        payload={"source_id": "labels", "name": entry.name, "label_id": entry.label_id},
        item_ids=(entry.label_id,),
    )


def _playlist_tracks_or_refuse(found: catalogue.Catalogue, reference: str) -> list:
    """Resolve and list one playlist, translating a provider failure at the boundary.

    THIS IS WHERE ``label-playlist-unreadable`` IS EARNED, and it is the only
    place it may be raised from. The cause means one thing: a BOUND provider was
    asked for this playlist and could not answer. Everything upstream of the
    ask has already refused with its own cause by the time this runs, which is
    what makes the sentence below true rather than a guess.

    TWO EXCEPTION SHAPES ARRIVE HERE AND NEITHER IS CRATEKIT'S TO PREDICT.
    ``listing.fetch_with_retry`` re-raises the PROVIDER's own exception once its
    retry ladder is spent, and its type is whatever the installed client version
    raises; ``listing.ListingNotPaginated`` is a plain ``RuntimeError`` this
    codebase defines for a client that dropped its pagination arguments. A
    translation narrowed to the type this layer happens to know would let the
    other escape as an unclassified crash, so the catch is broad and the
    breadth is bounded by the re-raise directly above it.

    A ``CratekitError`` PASSES THROUGH UNCHANGED, which is the bound. A refusal
    from further down already names what went wrong, and the failures reachable
    here are not all the provider's: the review queue is a local file, and one
    written at another schema version refuses ``review-schema-mismatch``.
    Flattening that into an unreadable playlist would blame a reachable provider
    for something on this machine, which is the defect this whole function
    replaces, rebuilt one layer lower.
    """
    try:
        playlist = found.playlist_for(reference)
        return harvest.playlist_tracks(playlist)
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
            f"({exc}); harvest needs a reachable provider playlist and will not "
            f"invent labels",
            steps=("pass a playlist this account can read, then retry",),
            origin=("label.cli",),
            detail={"playlist": reference, "kind": type(exc).__name__},
        ) from exc


def _offered(item: review.Item) -> dict:
    """One offered label projected for the envelope, not the whole record.

    The same shape ``cratekit.cli.review`` lists a queue in, with the label name
    added because that is the thing a person harvested. ``crate review show`` is
    where the whole record lives, here as everywhere.
    """
    return {
        "id": item.item_id,
        "queue": item.queue,
        "kind": item.kind,
        "name": str(item.payload.get("name") or ""),
    }


def harvest_playlist(ctx) -> Envelope:
    """Offer the record labels behind a playlist's tracks. Imports nothing.

    IT USED TO REFUSE UNCONDITIONALLY, and the refusal said the playlist could
    not be listed. Nothing had been contacted, so the sentence was false on
    every call, and it sent a person to check a playlist that was fine. A
    refusal whose stated cause is false is worse than an honest one, and the
    honest ones are what this verb now gives: the seam says whether the
    capability is built and whether a credential is recorded, and only a bound
    provider that failed to answer earns ``label-playlist-unreadable``.

    THE CATALOGUE IS LOOKED UP ON THE MODULE AT CALL TIME rather than bound into
    this scope by the import at the top of the file, on the contract
    ``label/catalogue.py`` states: that is what lets a test substitute the seam,
    and this verb runs in process so a substitution actually reaches it. In a
    shipped build ``resolve`` raises ``credential-missing`` or
    ``label-catalogue-unbound``, and both of those ARE this unit's delivery as
    much as the success branch is.

    NO ``--job`` BRANCH AND NO GATE. The registry declares this verb neither
    ``long_running`` nor gated, and it is right not to: harvest queues nothing,
    writes no audio and touches no library file. What it produces is review
    queue rows, which a person decides on later through their own verb.

    ``unresolved`` IS WHAT HARVEST COULD NOT TURN INTO A LABEL, which is a
    different question from the one ``crate review list`` answers with the same
    key, and the difference is stated rather than left to a reader. There it is
    the queue's open backlog; here it is this playlist's own failure to resolve,
    because a person asking what a harvest achieved is asking about the playlist
    they named and not about a queue that may hold months of other work. It sums
    TWO populations, and the second is the one a literal reading loses: the
    names a bound catalogue refused to confirm, and the tracks that carried no
    copyright string for a name to be read off at all. ``from_tracks`` cannot
    see the second, since it only records a drop for a name it was given, so a
    count taken from ``dropped`` alone would report a clean zero over a playlist
    nothing could be read from.
    """
    cfg = _load()
    # RESOLVED BEFORE THE PLAYLIST IS TOUCHED, which is what keeps R13 true. An
    # unbound build must not be able to reach the listing at all, or its refusal
    # would be about a provider it never had.
    found = catalogue.resolve(cfg)
    reference = str(ctx.args.playlist)
    tracks = _playlist_tracks_or_refuse(found, reference)
    # ONE EXTRACTOR, NAMED ONCE AND PASSED IN. ``from_tracks`` defaults to this
    # same function, and taking the default while counting the nameless tracks
    # with a second reference to it is how the two silently come to disagree
    # about what a candidate name is.
    extract = harvest.labels_from_copyright
    with review.open_store(cfg) as store:
        report = harvest.from_tracks(
            tracks,
            store=store,
            verify=found.check_label,
            extract=extract,
        )
    unresolved = len(report.dropped) + sum(1 for track in tracks if not extract(track))
    return ctx.envelope(
        data={
            "queue": str(review.Queue.LABEL_RELEASE),
            "items": [_offered(item) for item in report.offered],
            "unresolved": unresolved,
        },
        # AN EMPTY PLAYLIST IS A SUCCESS, and NO_OP is how it says so without
        # pretending it found something. A build that refused here would make a
        # playlist with nothing in it indistinguishable from one that could not
        # be read, which is the same collapse in the other direction.
        outcome=Outcome.OK if report.offered else Outcome.NO_OP,
    )


def run_increment(
    cfg: config.Config,
    source: sweep.LabelSource,
    *,
    owned: set[str] | frozenset[str],
    limit: int,
    run_id: str,
) -> run.IncrementResult:
    """Drive one labels increment. Shared run id keeps one intake file (R29)."""
    return run.increment(
        source,
        owned=owned,
        limit=limit,
        watermarks=watermarks.WatermarkStore(cfg),
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id=run_id,
        staging=Path(cfg.paths.download_staging),
    )


def handle(job, item, cfg) -> jobs.Produced | None:
    """Sweep one queued favourite label. The per item worker behind BOTH keys.

    THE ITEM NAMES THE LABEL, never the payload. That is the first defect U46's
    end to end drive surfaced, and ``master/cli.py`` and ``favorites/cli.py`` both
    carry the comment: a handler reading its subject from the payload makes every
    item of a multi item job do the same work. A sweep of five favourite labels
    would sweep one label five times, and for this verb the payload does not even
    carry a label, so it would sweep nothing five times and report five items done.

    THE REGISTRY IS LOADED WITH A PLAIN ``RegistryStore()``, AND THE REASON IS
    COUNTER-INTUITIVE ENOUGH TO WRITE DOWN (KTD6). Every other store in this
    package takes the frozen configuration, and this one takes none because there
    is none to take: ``RegistryStore.__init__`` calls
    ``config.state_path("label_intent")`` with NO configuration argument, and
    ``config.state_path`` returns ``installation_state_dir() / relative`` for any
    entry declaring ``root=StateRoot.INSTALLATION`` before it ever looks at a
    ``Config``. ``label_intent`` is one of those. So passing ``cfg`` would resolve
    the identical path, and a test that moved the library root to prove this
    worker respects its frozen configuration would be proving nothing. R17 is
    pinned on the review store instead, which is library scoped and genuinely
    moves. The remaining hazard on this side is ``CRATEKIT_STATE_DIR``, which no
    frozen configuration can pin, and it is recorded rather than papered over.

    THE REGISTRY CAN MOVE BETWEEN ENQUEUE AND DRIVE, so a queued identifier it no
    longer holds is refused rather than swept as an empty registry. The item is
    frozen; the registry is a live document another verb edits.

    THE CATALOGUE IS LOOKED UP ON THE MODULE AT CALL TIME rather than bound into
    this scope by the import at the top of the file, which is what lets a test
    substitute the seam. ``modules/outbound/account.py`` states the same contract
    for the outbound half, and ``label/catalogue.py`` states it for this one.

    AN EMPTY OWNED SET (KTD9), because no producer of owned identities exists on
    the labels path anywhere in ``src``. ``scope.scoped`` and ``list_for_label``
    both filter on membership in the set they are handed, so this is not ownership
    filtering happening in the wrong order, it is ownership filtering not
    happening: a sweep offers releases the library may already hold. Stated here
    and recorded as a residual rather than left for a reader to infer from a
    literal.

    NOTHING IS PRODUCED. The sweep writes no file: it OFFERS into the review
    queue, which is the durable record, so there is no artifact to commit and the
    envelope stays exactly ``job_state/1`` (KTD7). ``LabelSource.acquires`` is
    False, so the increment writes no intake file and moves no watermark either.
    """
    label_id = str(item.item_id or "")
    entry = labels.RegistryStore().load().by_id(label_id)
    if entry is None:
        raise refuse(
            "label-unknown",
            f"this job was queued for the favourite label {label_id!r} and the "
            f"registry no longer holds it, so there is nothing to sweep; a label "
            f"that was removed after the job was filed is not a label with "
            f"nothing new",
            steps=(
                f"re-add it with: crate label registry add {label_id}",
                "or cancel this job, since its items name labels you removed",
            ),
            origin=("label.cli",),
            detail={"label_id": label_id, "job_id": job.job_id},
        )

    payload = dict(job.payload or {})
    result = run_increment(
        cfg,
        # ``cfg`` REACHES THE REVIEW STORE THROUGH THIS OBJECT. ``increment``
        # calls ``LabelSource.process`` without a store, and ``process`` then
        # opens one against ``self.cfg``, so the configuration handed here is the
        # one the offers are written under. That is the whole of R17 on this path.
        sweep.LabelSource(
            cfg,
            registry=labels.Registry(labels={entry.label_id: entry}),
            catalogue=catalogue.resolve(cfg),
        ),
        owned=set(),
        limit=labels.effective_limit(entry),
        # THE RUN ID FALLS BACK TO THE JOB, so a sweep queued outside ``sync all``
        # still has one. R29 is why the payload's is preferred: two sources queued
        # by one sync share an intake run, and an id invented per item would split
        # what a person imports into as many files as the job has labels.
        run_id=str(payload.get("run_id") or job.job_id),
    )
    if result.errors:
        raise refuse(
            "label-sweep-incomplete",
            f"the sweep of {entry.name!r} could not offer "
            f"{len(result.errors)} of the releases it listed "
            f"({'; '.join(result.errors)}); the offers it did make are already in "
            f"the review queue and this label was not swept in full",
            # THE RAISE SITE OWNS THE REMEDY. ``core/cause.py``'s ``REASONS`` maps
            # a slug to an exit code and carries no remedy at all, and the answer
            # here is another attempt at this job rather than the class default:
            # the round was partial, the successful offers are durable, and a
            # resume redoes only the items that failed.
            remedy=Remedy.RESUME_JOB,
            origin=("label.cli",),
            detail={
                "label_id": entry.label_id,
                "offered": len(result.processed),
                "failed": len(result.errors),
            },
        )
    return None


__all__ = [
    "build_harvest",
    "build_import",
    "build_registry",
    "build_sync",
    "handle",
    "harvest_playlist",
    "import_label",
    "label_import_argv",
    "queue_warnings",
    "registry_cmd",
    "run_increment",
    "sweep_items",
    "sync_labels",
    "sync_labels_argv",
]
