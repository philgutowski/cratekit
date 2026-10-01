"""``crate label`` and ``crate sync labels``: registry, sweep, import, harvest.

Builders take an untyped ``entry`` so this file does not import the CLI
registry (KTD23). Long-running work queues a job. The increment engine is
``cratekit.sync.run.increment``; this shell freezes the source id and the
run id so two sources queued by ``sync all`` still share one intake file.
"""

from __future__ import annotations

from collections.abc import Callable, Container, Sequence
from pathlib import Path

from cratekit.acquire import match_cli
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config, jobs, review, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, harvest, sweep
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.sync import artifacts, run, watermarks

#: The two handler keys one label worker serves, and the only jobs a label
#: verb's ``--job`` will drive. The same two strings ``cli/handlers.py`` binds
#: to this module's ``handle``, and ``tests/test_label_workers.py`` pins them
#: against the registry so a renamed key fails there rather than here.
LABEL_KEYS: frozenset[str] = frozenset({"sync.labels", "label.import"})


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


def positive_limit(text: str) -> int:
    """Parse ``--track-limit``, refusing zero and negatives AT THE PARSER.

    ``registry.effective_limit`` reads a limit below one as the default, so a
    zero stored here would be a confident answer to a question nobody asked.
    Raising ``ValueError`` is what argparse turns into its own usage error.
    """
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive track limit")
    return value


def positive_offer(text: str) -> int:
    """Parse ``--offer``, refusing zero and negatives at the parser, as the limit does."""
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive offer")
    return value


def build_registry(parser, entry) -> None:
    parser.add_argument(
        "action",
        nargs="?",
        default="list",
        choices=("list", "add", "set", "remove", "rename", "adopt"),
        help=(
            "list (default), add, set fields on, remove, or rename a favourite "
            "label, or adopt every harvested label accepted in review"
        ),
    )
    parser.add_argument("name", nargs="?", help="display name or identifier")
    parser.add_argument("--to", dest="new_name", default=None, help="new display name")
    parser.add_argument("--match", default=None, help="copyright match needle")
    parser.add_argument(
        "--track-limit",
        dest="track_limit",
        type=positive_limit,
        default=None,
        metavar="N",
        help="newest N tracks to take from this label",
    )
    parser.add_argument(
        "--seed",
        dest="seeds",
        action="append",
        default=None,
        metavar="VALUE",
        help="seed artist, a name or id:<digits>; repeat for more, replaces the held list",
    )
    parser.add_argument(
        "--offer",
        dest="offer",
        type=positive_offer,
        default=None,
        metavar="N",
        help=(
            "how many of this label's newest releases one sweep keeps in review, "
            "counting those already there; overrides labels.offer_per_sweep"
        ),
    )
    parser.add_argument(
        "--kind",
        dest="kind",
        default=None,
        metavar="KIND",
        help=(
            "the kind of music this label is followed for, one the library's "
            "taxonomy names under label_gate, or any; it decides which releases "
            "the genre gate passes, and a label with none is the default kind"
        ),
    )
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


def _detail(entry: labels.LabelEntry) -> str:
    """The identifier, then every field a person set, so ``list`` shows them."""
    parts = [entry.label_id]
    if entry.match:
        parts.append(f"match {entry.match!r}")
    if entry.track_limit is not None:
        parts.append(f"track limit {entry.track_limit}")
    if entry.offer is not None:
        bound = labels.effective_limit(entry)
        parts.append(
            f"offer {entry.offer}"
            + (f", bounded by the track limit to {bound}" if entry.offer > bound else "")
        )
    if entry.kind is not None:
        parts.append(f"kind {entry.kind}")
    if entry.seed_artists:
        parts.append("seeds " + " | ".join(entry.seed_artists))
    return ", ".join(parts)


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
            "detail": _detail(entry),
            "remedy": None,
        }
        for entry in held.labels.values()
    ]


def _labels_json(held: labels.Registry) -> list[dict]:
    """Every held field, for a reader that is not a person."""
    return [entry.to_json() for entry in held.labels.values()]


def _declared_kind(kind: str) -> str:
    """``--kind`` as the library's taxonomy names it, or a refusal naming what it does.

    CHECKED HERE AND NOT IN THE STORE (R-798). The registry is the
    installation's and the taxonomy is the library's, so only a verb, which has
    a configuration, can ask whether a kind exists. A kind nothing names would
    be stored without complaint and then never judged, which reads at the next
    sweep exactly like a catalogue that had nothing to say.
    """
    wanted = labels.check_kind(kind)
    named = active_taxonomy.load(_load()).label_gate.kinds
    if wanted == taxonomy.ANY_KIND or wanted in named:
        return wanted
    raise refuse(
        "label-name-invalid",
        f"{wanted!r} is not a kind the library's taxonomy names"
        + (
            f"; it names {', '.join(named)}, and {taxonomy.ANY_KIND} passes everything"
            if named
            else f"; it declares no kinds at all, so only {taxonomy.ANY_KIND} can be "
            f"set until its label_gate section gains the published rules"
        ),
        steps=("pass --kind with one of those, or add a rule for it to the taxonomy",),
        origin=("label.cli",),
        detail={"kind": wanted, "kinds": [*named, taxonomy.ANY_KIND]},
    )


def registry_cmd(ctx) -> Envelope:
    store = labels.RegistryStore()
    action = ctx.args.action
    seeds = ctx.args.seeds
    track_limit = ctx.args.track_limit
    offer = ctx.args.offer
    kind = ctx.args.kind
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind)
    if action not in ("add", "set") and any(given is not None for given in fields_given):
        raise refuse(
            "label-name-invalid",
            f"label registry {action} does not set --seed, --track-limit, "
            f"--offer, --kind or --match, and ignoring them would report a change "
            f"that was never written",
            steps=("use label registry set, or add, to change those fields",),
            origin=("label.cli",),
        )
    if action == "list":
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"count": len(held.labels), "labels": _labels_json(held)},
            }
        )
    if action == "adopt":
        return adopt_harvested(ctx, store)
    name = ctx.args.name
    if not name:
        raise refuse(
            "label-name-invalid",
            f"label registry {action} needs a name",
            steps=("pass the label name after the action",),
            origin=("label.cli",),
        )
    if kind is not None:
        kind = _declared_kind(kind)
    if action == "add":
        label_id = store.add(
            name,
            match=ctx.args.match,
            seed_artists=tuple(seeds or ()),
            track_limit=track_limit,
            offer=offer,
            kind=kind,
        )
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"added": label_id, "count": len(held.labels)},
            }
        )
    if action == "set":
        if all(given is None for given in fields_given):
            raise refuse(
                "label-name-invalid",
                "label registry set needs a field to change, and a set that "
                "changed nothing would report an edit that never happened",
                steps=("pass --track-limit, --offer, --kind, --seed, or --match",),
                origin=("label.cli",),
            )
        edited = store.edit(
            name,
            match=ctx.args.match,
            seed_artists=seeds,
            track_limit=track_limit,
            offer=offer,
            kind=kind,
        )
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"updated": edited.label_id, "count": len(held.labels)},
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


def _adopt_check(item_id: str, result: labels.Adopted) -> dict:
    if result.refused is not None:
        status = "fail"
        detail = (
            f"{result.name}: yields no identifier, so it cannot be a favourite "
            f"label ({result.refused}); clear the verdict and reject it in review"
        )
    elif result.added:
        status, detail = "ok", f"{result.name}: added as {result.label_id}"
    else:
        status = "info"
        detail = f"{result.name}: already held as {result.label_id}"
        if result.held_name != result.name:
            detail += f", under the name {result.held_name}"
    return {
        "key": f"adopt.{item_id}",
        "title": result.name,
        "status": status,
        "detail": detail,
        "remedy": None,
    }


def adopt_harvested(ctx, store: labels.RegistryStore) -> Envelope:
    """Add every harvested label accepted in review to the registry.

    THE SECOND HALF OF HARVEST, AND A VERB OF ITS OWN (R-419). Harvest offers a
    label for review and a verdict is recorded; nothing read that verdict, so
    each approved label was typed again into ``add``. It is not done inside
    ``review resolve``, which would make answering a review a write to a second
    store.

    IDEMPOTENT BY RESOLUTION, NOT BY BOOKKEEPING. Nothing is marked on the review
    item. A label is skipped because the registry already holds it, found the way
    :meth:`labels.RegistryStore.adopt` finds it, so a label removed from the
    registry since is added again on the next run. That is what an accepted
    verdict says, and the verdict is the person's to clear.

    One check per accepted item, keyed on the review item, because two items can
    name one label and a key on the label would repeat. ``diagnostic/1`` renders
    checks to a person, so the answer is on the screen and not only in json.
    """
    if ctx.args.name or ctx.args.new_name is not None:
        raise refuse(
            "label-name-invalid",
            "label registry adopt takes every harvested label accepted in review "
            "and no name; ignoring the one given would report a choice that was "
            "never applied",
            steps=(
                "run label registry adopt with no name",
                "or add one label with: crate label registry add <name>",
            ),
            origin=("label.cli",),
        )
    cfg = _load()
    with review.open_store(cfg) as items:
        found = harvest.decided(items)
    results = store.adopt([name for _, name in found.accepted]) if found.accepted else ()
    checks = [
        _adopt_check(item_id, result)
        for (item_id, _), result in zip(found.accepted, results, strict=True)
    ]
    checks.extend(
        {
            "key": f"adopt.{item_id}",
            "title": item_id,
            "status": "fail",
            "detail": f"{item_id}: accepted in review and names no label",
            "remedy": None,
        }
        for item_id in found.nameless
    )
    if not checks:
        checks.append(
            {
                "key": "adopt.none",
                "title": "harvested labels",
                "status": "info",
                "detail": (
                    f"no harvested label is accepted in review; "
                    f"{found.still_open} open, {found.rejected} rejected"
                ),
                "remedy": None,
            }
        )
    added = [result.label_id for result in results if result.added]
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {
                "added": added,
                "present": [
                    result.label_id
                    for result in results
                    if not result.added and result.refused is None
                ],
                "refused": [result.name for result in results if result.refused is not None],
                "nameless": list(found.nameless),
                "rejected": found.rejected,
                "open": found.still_open,
                "count": len(store.load().labels),
            },
        },
        outcome=Outcome.OK if added else Outcome.NO_OP,
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
    # THE STEPS NAME THE WAY OUT, because the slug does not. The job stays open
    # after this refusal, on purpose, and a person who resumes it again meets
    # the same sentence; without a step naming the cancel they are told only
    # that the job is stale and not what to do about a stale job.
    raise refuse(
        "internal-error",
        f"job {job.job_id} has no items to run, so driving it would report a "
        f"success over work it never did. It was queued by a build that did not "
        f"record what its items were",
        remedy=Remedy.REPORT_DEFECT,
        steps=(
            f"cancel it with: crate job cancel {job.job_id}",
            "then queue the sweep or the import again, which records its items",
        ),
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
        # THE JOB HAS TO BE A LABEL JOB. ``handlers.run_job`` resolves the worker
        # from the job row and not from this verb, so without this line
        # ``sync labels --job`` would drive any queued job of any verb in
        # process, under this verb's envelope and without that verb's own resume
        # time checks: the outbound shell re-requires its gate and its payload
        # digest on resume by design, and a job driven from here would skip
        # both. Either label key is accepted, because one worker serves the two
        # and neither declares a gate. ``job-unknown`` is reused rather than
        # given a sibling: from this verb's side the job named on ``--job`` is
        # one it does not know, and the sentence says which verb does.
        if job.handler_key not in LABEL_KEYS:
            raise refuse(
                "job-unknown",
                f"job {job.job_id} was queued for {job.handler_key!r}, which is "
                f"not a label job, so this verb will not drive it",
                steps=(
                    f"resume it through its own verb, or with: crate job resume "
                    f"{job.job_id}",
                ),
                origin=("label.cli",),
                detail={"job_id": job.job_id, "handler": job.handler_key},
            )
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
        # for ever after.
        #
        # ANY CLOSED JOB CARRYING A CAUSE, not FAILED alone. A run stopped with a
        # signal is CANCELLED and carries the cause ``jobs.cancel`` builds; the
        # narrower predicate was measured on 2026-09-02 as exit 0 over a job with
        # 0 of 3 items done. SUCCEEDED carries no cause and is unaffected.
        #
        # AND A PARKED JOB, which that predicate never saw because ``blocked`` is
        # an open state (R-290). The predicate now has one owner,
        # ``jobs.raise_for_state``, which every queued verb's shell calls.
        jobs.raise_for_state(job)
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


def sweep_items_or_refuse() -> tuple[str, ...]:
    """The sweep's items, or the refusal an empty registry earns.

    PUBLIC because ``crate sync all`` asks it too, before it queues anything,
    so an empty registry is reported for the labels source rather than
    discovered after another source was already queued.

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
    # THE CONFIGURATION IS READ BEFORE THE ITEMS ARE DERIVED, and the order is
    # the fix rather than an ornament. When the items were an ARGUMENT to the
    # shared queue helper they were evaluated before that helper's own
    # ``_load()`` ever ran, and the favourite label registry is installation
    # scoped (KTD6) so it reads perfectly well on a machine that has never been
    # set up. A fresh install therefore got ``label-registry-empty`` and was told
    # to run ``crate label registry add``, which would not have moved the real
    # blocker. ``main`` refused ``config-unusable`` here, and the sibling verb
    # ``label.harvest`` still does, so this had made two verbs in one package
    # disagree about what a fresh install's problem is.
    #
    # THE SECOND LOAD COSTS A ``stat`` AND NOTHING ELSE. ``config.load`` memoizes
    # on ``(path, inode, mtime, size)`` and every write here goes through an
    # atomic replace, so ``_queue``'s call is a memo hit rather than a second
    # parse, and this does not become a reason to thread a ``Config`` through.
    cfg = _load()
    run_id = getattr(ctx.args, "run_id", None) or ctx.run.run_id
    items = sweep_items_or_refuse()
    with jobs.open_store() as store:
        job = queue_sweep(
            store, cfg, handler_key=ctx.entry.handler_key, run_id=run_id, item_ids=items
        )
        return ctx.envelope(data=_reported(store, job), warnings=queue_warnings())


def queue_sweep(
    store, cfg: config.Config, *, handler_key: str, run_id: str, item_ids: tuple[str, ...]
) -> jobs.Job:
    """Queue one label sweep. The one spelling of what a sweep job is.

    TWO CALLERS, ONE JOB. ``sync labels`` passes its own handler key and
    ``crate sync all`` passes the key ``cratekit.sync.sources`` declares for the
    labels source, which is the same key, so a sweep queued by either verb is the
    same job shape and the same worker runs it. A second copy of this payload in
    the composer would be the place the two drift.

    ``item_ids`` comes from :func:`sweep_items_or_refuse`, which refuses an empty
    registry before anything is written, so neither caller can file a sweep with
    nothing to claim (the ZERO ITEM RULE). ``run_id`` is the INTAKE run, shared
    with the other sources of one sync so their workers write one file (R29).
    """
    return jobs.enqueue(
        store,
        handler_key=handler_key,
        payload={"source_id": "labels", "run_id": run_id},
        item_ids=item_ids,
        cfg=cfg,
    )


def import_label(ctx) -> Envelope:
    # THE SAME ORDER, and it moves one refusal for this verb: a resume no longer
    # refuses ``label-unknown`` for a label removed since the job was queued. That
    # is the correct place to lose it. The job holds one frozen item, and the
    # worker asks the registry for exactly that identifier, so the same condition
    # is still refused, per item, where a person is told which label it was.
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    # THE CONFIGURATION IS READ BEFORE THE REGISTRY, for the reason
    # :func:`sync_labels` gives. The registry is installation scoped and reads
    # on a machine that has never been set up, so a fresh install used to be
    # refused ``label-unknown`` here and sent to ``crate label registry add``,
    # and then refused ``config-unusable`` once it had obeyed. The sibling verb
    # had been brought into line and this one had not.
    _load()
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


def playlist_tracks_or_refuse(found: catalogue.Catalogue, reference: str) -> list:
    """Resolve and list one playlist, translating a provider failure at the boundary.

    THIS IS ONE OF THE TWO PLACES ``label-playlist-unreadable`` IS EARNED, and
    :func:`_label_verifier` is the other. The cause means one thing across both:
    a BOUND provider was asked something about this playlist and could not
    answer. Everything upstream of the ask has already refused with its own cause
    by the time either runs, which is what makes the sentence below true rather
    than a guess. This one covers resolving the playlist and listing its tracks;
    the other covers confirming the label names those tracks carry, which is the
    third provider call the verb makes and the one that had no boundary at all.

    TWO EXCEPTION SHAPES ARRIVE HERE AND NEITHER IS CRATEKIT'S TO PREDICT.
    ``listing.fetch_with_retry`` re-raises the PROVIDER's own exception once its
    retry ladder is spent, and its type is whatever the installed client version
    raises; ``listing.ListingNotPaginated`` is a plain ``RuntimeError`` this
    codebase defines for a client that dropped its pagination arguments. A
    translation narrowed to the type this layer happens to know would let the
    other escape as an unclassified crash, so the catch is broad and the
    breadth is bounded by the re-raise directly above it.

    A ``CratekitError`` PASSES THROUGH UNCHANGED, which is the bound, and it is
    DEFENSIVE rather than load bearing today. The justification this docstring
    used to give was unreachable: it named ``review-schema-mismatch``, and
    ``review.open_store(cfg)`` runs in the caller AFTER this boundary has
    returned, so a queue written at another schema version cannot arrive here at
    all. The test that pins the passthrough has to monkeypatch
    ``harvest.playlist_tracks`` to reach it, which is the tell.

    WHAT COULD ACTUALLY ARRIVE is an adapter's own refusal. ``playlist_for``
    belongs to the :class:`~cratekit.label.catalogue.Catalogue` protocol, no
    adapter ships in this build, and an adapter that discovered at call time that
    the stored provider session had expired would refuse ``credential-missing``,
    which names an act a person can take. Flattening that into an unreadable
    playlist would send somebody to check a playlist that is fine, which is the
    defect this whole function replaces, rebuilt one layer lower. The passthrough
    is kept for that seam rather than deleted because the seam is the thing this
    unit built and the adapter is the next unit.
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


def favourite_tracks_or_refuse(
    found: catalogue.Catalogue, reference: str
) -> tuple[list, catalogue.HeartsShortfall | None]:
    """List the account's hearts, translating a provider failure at the same boundary.

    Returns the rows and, when the listing came back shorter than the account
    declares, the :class:`~cratekit.label.catalogue.HeartsShortfall` that says
    by how much (R-504). A shortfall is not a failure to read: the rows it
    carries are hearts the provider served, so they are listed, and the caller
    reports the count withheld. It is caught BEFORE the broad translation
    below, which would otherwise refuse it as an unreadable listing.

    THE SAME TRANSLATION AS :func:`playlist_tracks_or_refuse`, and for the same
    reasons: a ``CratekitError`` passes through so an adapter's own refusal keeps
    the act it names, and anything else is ``label-playlist-unreadable``, because
    the hearts are one more provider listing a bound catalogue could not answer.
    ``listing.ListingTruncated`` is the shape that matters most here. It arrives
    as a plain ``RuntimeError`` and is refused whole, since a short hearts listing
    would read every heart past the cut as one the account does not hold.

    ``reference`` is what the person typed, carried into the detail so the
    refusal names the input the way the playlist refusal does.
    """
    try:
        return list(found.favourite_tracks()), None
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the account's favourites could not be listed by the provider "
            f"({exc}); a partial listing would miss hearts, so none is used",
            steps=("retry once the provider can list this account's favourites",),
            origin=("label.cli",),
            detail={"playlist": reference, "kind": type(exc).__name__},
        ) from exc


def _label_verifier(
    found: catalogue.Catalogue, reference: str
) -> Callable[[str], dict]:
    """``check_label`` with a failure boundary, and a memory of what it confirmed.

    THE THIRD PROVIDER CALL HARVEST MAKES, AND THE ONE THAT HAD NO BOUNDARY.
    ``found.check_label`` was handed into ``harvest.from_tracks`` outside the
    try/except :func:`playlist_tracks_or_refuse` provides, which wraps only the
    resolve and the listing. ``listing.fetch_with_retry`` re-raises the
    provider's own exception once its retry ladder is spent, so a provider that
    went away mid playlist left the verb as ``internal-error`` with
    ``Remedy.REPORT_DEFECT``: a person whose provider was down was told to file a
    bug against this program. Measured on 2026-09-02 as exit 1, reason
    ``internal-error``, remedy ``report-defect``, retryable false.

    THE BOUNDARY IS ON THE PROVIDER CALL ITSELF rather than around the whole
    ``from_tracks`` pass, and that placement is the accuracy. ``review.offer`` is
    a local write, and a broad catch one level up would report a failure of the
    review queue as a failure of the provider, which is the same collapse
    :func:`playlist_tracks_or_refuse` refuses to make. It also keeps
    ``confirmed`` exact: ``from_tracks`` offers a name immediately after this
    callable confirms it and before it asks about the next one, so every name in
    the list at the moment of the raise is a row that is already in the queue.

    THE PARTIAL STATE IS NAMED, because it is durable and nothing else can name
    it. ``review.offer`` commits per call and is idempotent on the item's
    identity, so the labels confirmed before the outage are sitting in the review
    queue when this refuses, a retry will not duplicate them, and a person who
    was told only that the harvest failed would have no way to know either fact.

    A ``CratekitError`` PASSES THROUGH UNCHANGED, on the same bound and for the
    same reason the function above gives.
    """
    confirmed: list[str] = []

    def check(name: str) -> dict:
        try:
            verdict = found.check_label(name)
        except CratekitError:
            raise
        except Exception as exc:
            raise refuse(
                "label-playlist-unreadable",
                f"the provider stopped answering while harvest was confirming "
                f"the label names read off {reference!r} ({exc}); the "
                f"{len(confirmed)} it had already confirmed are offered in the "
                f"review queue and are waiting there, and the rest of the "
                f"playlist was never verified",
                steps=(
                    "retry this harvest when the provider is answering; the "
                    "labels already offered will not be queued twice",
                    "or read what is waiting with: crate review list",
                ),
                origin=("label.cli",),
                detail={
                    "playlist": reference,
                    "kind": type(exc).__name__,
                    "offered": list(confirmed),
                },
            ) from exc
        if str(verdict.get("verdict") or "") == "confirmed":
            confirmed.append(name)
        return verdict

    return check


def _offered(item: review.Item) -> dict:
    """One offered label projected for the envelope, not the whole record.

    The identity triple ``crate review list`` keys a row on, with the label name
    added because that is the thing a person harvested. NOT that verb's whole
    row: it also carries the ordinal, the verdict and the option, which are
    facts about a queue a person is working through and not about a harvest
    that just offered the item. ``crate review show`` is where the whole record
    lives, here as everywhere.
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
    tracks = playlist_tracks_or_refuse(found, reference)
    # ONE EXTRACTOR, RUN ONCE PER TRACK. ``from_tracks`` defaults to this same
    # function, and taking the default while counting the nameless tracks with a
    # second reference to it is how the two silently come to disagree about what
    # a candidate name is. Counting during the pass ``from_tracks`` already makes
    # is what keeps that literally one execution per track: the earlier form
    # iterated the playlist a second time and ran the extractor again on every
    # track, which asks the same question twice and gives two places for the
    # answer to change.
    nameless = 0

    def extract(track) -> Sequence[str]:
        nonlocal nameless
        names = harvest.labels_from_copyright(track)
        if not names:
            nameless += 1
        return names

    with review.open_store(cfg) as store:
        report = harvest.from_tracks(
            tracks,
            store=store,
            # WRAPPED, NEVER THE BARE SEAM METHOD. Every provider call this verb
            # makes is inside a boundary that converts a provider failure into a
            # refusal a person can act on, and this was the one that was not.
            verify=_label_verifier(found, reference),
            extract=extract,
        )
    unresolved = len(report.dropped) + nameless
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
    owned: Container[str],
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


#: The library view of the one job being driven, keyed by the job and the
#: music folder it reads. One sweep job carries one item per favourite label,
#: and a view per item walked the whole music volume once per label. The job
#: driver runs a job's items one after another in one process, so a view built
#: for the first label is still the library for the last. Holding one job's
#: view and no other keeps a long lived process from carrying a stale library
#: into a later job.
_JOB_LIBRARY: dict[tuple[str, str], sweep.LibraryView] = {}


def _job_library(job, cfg: config.Config) -> Callable[[], sweep.LibraryView]:
    """The library view for ``job``, walked on first use and once per job."""
    key = (str(job.job_id), str(cfg.library.root / cfg.library.music_dir))

    def view() -> sweep.LibraryView:
        held = _JOB_LIBRARY.get(key)
        if held is None:
            _JOB_LIBRARY.clear()
            held = _JOB_LIBRARY[key] = match_cli.library_view(cfg)
        return held

    return view


def _refuse_unread(
    entry: labels.LabelEntry, unread: Sequence[catalogue.Unread], *, offered: int
) -> None:
    """Refuse a sweep whose crawl skipped part of the label. R-261 and R-393.

    RAISED AFTER THE INCREMENT, so every release the crawl did read is already
    offered and durable in the review queue. That is the difference from
    refusing the label outright, which R-352 removed from search and which
    R-261's entry argues against: the skip still happens, and what it cost
    is now said. A job item has no warning channel, only a cause, so the cause
    is the one place a person reads it.

    RESUMABLE ONLY WHEN SOMETHING CAN CHANGE. A rate limit or an outage clears
    and another attempt reads the artist. A listing the client does not expose
    stays missing however often the job is resumed, so that case names a
    defect instead of telling the person to try again.
    """
    transient = any(one.transient for one in unread)
    parts = "; ".join(f"{one.artist} ({one.listing}: {one.reason})" for one in unread)
    raise refuse(
        "label-sweep-incomplete",
        f"the sweep of {entry.name!r} offered what it read and could not read "
        f"{len(unread)} listings of the label: {parts}. The releases on those "
        f"listings are missing from this sweep, not absent from the label",
        remedy=Remedy.RESUME_JOB if transient else Remedy.REPORT_DEFECT,
        retryable=transient,
        origin=("label.cli",),
        detail={
            "label_id": entry.label_id,
            "offered": offered,
            "unread": [
                {"artist": one.artist, "listing": one.listing, "reason": one.reason}
                for one in unread
            ],
        },
    )


def _refuse_unfinished(entry, result: run.IncrementResult, source: sweep.LabelSource) -> None:
    """Refuse a sweep that did not finish, before anything records it as one.

    Lifted out of :func:`handle` so the worker can ask it while the item's one
    review store is still open, and record the label's round only once it has
    passed (R-790).
    """
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
    if source.unread:
        _refuse_unread(entry, source.unread, offered=len(result.processed))
    # A CATALOGUE THAT CONFIRMS NOTHING IS NOT A LABEL WITH NOTHING NEW, and
    # before this branch it was reported as one. ``list_for_label`` drops every
    # release a degraded, rate limited, or distributor-crediting verification
    # endpoint will not confirm, so the increment is handed no candidate at all;
    # it then sees no processed item and no error and answers
    # ``shortfall="empty"``. Measured on 2026-09-02 through the real dispatcher,
    # queue and driver: forty releases read, forty discarded, exit 0, job
    # SUCCEEDED, no cause and no warning. ``sweep._verifier``'s own docstring
    # names this exact scenario as its reason for existing and then guards only
    # the case where no verifier OBJECT exists, which is METHOD's defect pattern
    # three, a fix on the performing path with the checking path left open.
    #
    # KEYED ON EVERY RELEASE READ HAVING BEEN DROPPED, and never on the dropped
    # population being non-empty or on an empty candidate list. A label whose
    # every release is tombstoned, and one whose crawl is genuinely exhausted,
    # also offer nothing, and both are honest no ops a person asked for. So is
    # the MIXED listing: some releases tombstoned and the rest dropped, which a
    # guard keyed on "anything was dropped" refused as a catalogue nobody could
    # verify a line of, with ``confirmed: 0``, over a release the person had
    # confirmed and then deleted on purpose. Only "releases were read and every
    # one of them was discarded as unconfirmed" reaches here, and that is the
    # one case where the success would be a claim about a catalogue nobody
    # managed to verify a line of.
    #
    # THE SENTENCE SEPARATES TWO PROBLEMS WITH TWO REMEDIES. A sweep that could
    # not REACH the provider already refuses ``sync-source-lookups-failed`` from
    # the increment, and a person meeting that one waits for the network. This
    # one reached the provider and could not confirm anything it found, which is
    # usually a release credited to a distributor rather than to the imprint, and
    # is repaired by the registry's ``--match`` needle rather than by waiting.
    #
    # A HELD RELEASE COUNTS WITH THE DROPPED ONES WHEN IT COULD NOT BE CONFIRMED
    # AGAIN (R-790). Held releases are no longer verified on every sweep, and
    # they were what made a dead endpoint drop every release read; the sweep
    # re-verifies one of them on exactly this path, and its answer stands for
    # all of them.
    unconfirmed = len(source.dropped) + source.held_unconfirmed
    if result.shortfall == "empty" and source.dropped and unconfirmed == source.read:
        raise refuse(
            "label-sweep-incomplete",
            f"the sweep of {entry.name!r} read {unconfirmed} releases "
            f"from the catalogue and could not confirm a single one of them, so "
            f"it offered nothing and this is not a label with nothing new. The "
            f"provider answered: what failed is verification rather than reach",
            steps=(
                f"check what the catalogue credits these releases to, then set "
                f"the needle with: crate label registry add {entry.name} --match "
                f"<credited name>",
                "or resume this job once the verification endpoint is answering",
            ),
            origin=("label.cli",),
            detail={
                "label_id": entry.label_id,
                "read": unconfirmed,
                "confirmed": 0,
                "reasons": sorted({drop.reason for drop in source.dropped}),
            },
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

    ONE OWNED CONTAINER FOR BOTH FILTERS (R-259). ``list_for_label`` and
    ``scope.scoped`` both filter on membership in what they are handed, and until
    this unit the worker handed them an empty set, so every sweep offered releases
    the library already held. :class:`~cratekit.label.sweep.OwnedReleases` answers
    by reading a release's tracks and resolving them against the library index,
    and the SAME object goes to the source and to the increment, so the second
    filter reuses the first one's answers rather than reading every release again.

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
    # THE SOURCE IS HELD IN A NAME rather than passed inline, because the result
    # alone cannot answer what the sweep read and discarded and the source can.
    # See the empty-shortfall refusal below.
    # ONE REVIEW STORE FOR THE WHOLE ITEM. ``run.increment`` hands the source no
    # store, so without this every offered release opened and checkpointed the
    # review database on its own, four hundred times on a label at the default
    # cap. The store is opened against the FROZEN configuration, which is the
    # whole of R17 on this path, and it is opened before the catalogue is
    # resolved so an unbound build's refusal costs nothing it did not already.
    with review.open_store(cfg) as store:
        # THE DECLARATION BEFORE THE FIRST LOGIN, as ``label approved`` reads it
        # (R-685). The genre gate judges by the library's own rules, and an
        # active copy that cannot be read refuses here, not after a label was
        # listed and its releases filed unjudged.
        declared = active_taxonomy.load(cfg)
        found = catalogue.resolve(cfg)
        # ONE READER FOR BOTH QUESTIONS (R-798). Ownership and the genre gate
        # read the same rows of the same release, so the second gets the
        # first one's answer and the gate adds no provider call.
        tracks = sweep.ReleaseTracks(found)
        owned = sweep.OwnedReleases(cfg, tracks, library=_job_library(job, cfg))
        run_id = str(payload.get("run_id") or job.job_id)
        source = sweep.LabelSource(
            cfg,
            registry=labels.Registry(labels={entry.label_id: entry}),
            catalogue=found,
            store=store,
            owned=owned,
            gate=genre_gate.SweepGate(
                declared,
                tracks=tracks.release_tracks,
                standing=genre_gate.standing_in(store),
            ),
            run_id=run_id,
        )
        result = run_increment(
            cfg,
            source,
            owned=owned,
            limit=labels.effective_limit(entry),
            # THE RUN ID FALLS BACK TO THE JOB, so a sweep queued outside
            # ``sync all`` still has one. R29 is why the payload's is preferred:
            # two sources queued by one sync share an intake run, and an id
            # invented per item would split what a person imports into as many
            # files as the job has labels.
            run_id=run_id,
        )
        _refuse_unfinished(entry, result, source)
        # WHAT THE WINDOW DID NOT REACH IS RECORDED, NEVER DROPPED (R-790).
        # The job's envelope is ``job_state/1`` and carries no per label count,
        # and this worker runs in a detached child, so the count goes where the
        # person deciding the label's releases reads: ``crate review list
        # --queue label-release --group-by label``. RECORDED ONLY ONCE
        # ``_refuse_unfinished`` HAS PASSED, in the same store: a sweep refused
        # as partial, or as having confirmed nothing, must not leave a count
        # that reads as an answer about the catalogue, which is the clean
        # report over state nobody read that each refusal exists for.
        for swept, listing in source.listings:
            review.record_round(
                store,
                queue=review.Queue.LABEL_RELEASE,
                run_id=run_id,
                group=swept.label_id,
                name=swept.name,
                beyond=listing.beyond,
            )
    return None


__all__ = [
    "adopt_harvested",
    "build_harvest",
    "build_import",
    "build_registry",
    "build_sync",
    "favourite_tracks_or_refuse",
    "handle",
    "harvest_playlist",
    "playlist_tracks_or_refuse",
    "import_label",
    "label_import_argv",
    "queue_sweep",
    "queue_warnings",
    "registry_cmd",
    "run_increment",
    "sweep_items",
    "sweep_items_or_refuse",
    "sync_labels",
    "sync_labels_argv",
]
