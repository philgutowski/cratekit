"""``crate label`` and ``crate sync labels``: registry, sweep, import, harvest.

Builders take an untyped ``entry`` so this file does not import the CLI
registry (KTD23). Long running work queues a job, through the increment engine
``cratekit.sync.run.increment``; the job carries its source and run id, so a
sweep's workers write that run's intake file.

``crate sync labels`` queues nothing since U109: ``crate label sync`` takes
label releases, and this verb only resumes a sweep queued before it, on the one
worker the sweep and the import share.
"""

from __future__ import annotations

from collections.abc import Callable, Container
from pathlib import Path
from typing import Any

from cratekit.acquire import listing, match_cli
from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, config, jobs, review, routing, taxonomy
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, harvest, sweep
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.sync import artifacts, run, sources, watermarks

#: The two handler keys one label worker serves, and the only jobs a label
#: verb's ``--job`` will drive; ``cli/handlers.py`` binds both to :func:`handle`.
LABEL_KEYS: frozenset[str] = frozenset({"sync.labels", "label.import"})


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    return load_config(("label.cli",))


def _refused(reason: str, message: str, *steps: str, **kwargs: Any) -> CratekitError:
    """A refusal raised by this module, its steps given in order."""
    return refuse(reason, message, steps=steps, origin=("label.cli",), **kwargs)


def positive_limit(text: str) -> int:
    """Parse ``--track-limit``, refusing zero and negatives at the parser.

    ``registry.effective_limit`` reads a limit below one as the default, so a
    stored zero would be an answer nobody asked for. Argparse turns the
    ``ValueError`` into its own usage error.
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
        type=positive_limit,
        metavar="N",
        help="newest N tracks to take from this label",
    )
    parser.add_argument(
        "--seed",
        dest="seeds",
        action="append",
        metavar="VALUE",
        help="seed artist, a name or id:<digits>; repeat for more, replaces the held list",
    )
    parser.add_argument(
        "--offer",
        type=positive_offer,
        metavar="N",
        help=(
            "how many of this label's newest releases one sweep keeps in review, "
            "counting those already there; overrides labels.offer_per_sweep"
        ),
    )
    for flag, metavar, said in (
        (
            "--kind",
            "KIND",
            "the kind of music this label is followed for, one the library's "
            "taxonomy names under label_gate, or any; it decides which releases "
            "the genre gate passes. A label with none is the taxonomy's default "
            "kind, and --kind default clears a kind back to none",
        ),
        (
            "--genre",
            "WORD",
            "the genre every track of this label is tagged with when it has none, "
            "so tag folder asks no catalogue for it; checked against the "
            "library's taxonomy, and --genre default clears it back to none",
        ),
        (
            "--bandcamp",
            "ACCOUNT",
            "the Bandcamp seller account this label's releases are sold from, the "
            "name in their address (ACCOUNT.bandcamp.com) or the address itself; a "
            "purchase from it is staged tagged with this label and filed under it. "
            "One account names one label, and --bandcamp default clears it",
        ),
    ):
        parser.add_argument(flag, metavar=metavar, help=said)
    parser.add_argument(
        "--accept-fallback",
        action="store_true",
        help=(
            "keep a --genre the library's taxonomy routes only to its fallback "
            "bucket, knowing every track of the label would be filed there"
        ),
    )
    parser.set_defaults(_handler=registry_cmd)


def build_sync(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue a labels sweep queued before crate label sync replaced it; "
            "without this the verb queues nothing and names crate label sync"
        ),
    )
    parser.add_argument(
        "--run-id",
        help=(
            "accepted for the argv a resume is spawned with and otherwise "
            "ignored: a queued sweep keeps the intake run it was filed under"
        ),
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
    for said, value in (("kind", entry.kind), ("genre", entry.genre), ("Bandcamp", entry.bandcamp)):
        if value is not None:
            parts.append(f"{said} {value}")
    if entry.seed_artists:
        parts.append("seeds " + " | ".join(entry.seed_artists))
    return ", ".join(parts)


def _check(key: str, title: str, status: str, detail: str) -> dict:
    """One ``diagnostic/1`` check, which carries no remedy here."""
    return {"key": key, "title": title, "status": status, "detail": detail, "remedy": None}


def _checks_for(held: labels.Registry, routed: dict[str, str]) -> list[dict]:
    """One check per label. ``routed`` adds, for the label a verb just gave a
    genre, the sentence saying where that genre routes (U178)."""
    if not held.labels:
        return [_check("labels.empty", "favourite labels", "ok", "no labels are registered")]
    return [
        _check(
            f"labels.{entry.label_id}",
            entry.name,
            "ok",
            _detail(entry) + (f", {routed[entry.label_id]}" if entry.label_id in routed else ""),
        )
        for entry in held.labels.values()
    ]


def _declared_kind(kind: str) -> str:
    """``--kind`` as the library's taxonomy names it, or a refusal naming what it does.

    Checked here and not in the store (R-798): the registry is the
    installation's and the taxonomy the library's, so only a verb can ask
    whether a kind exists, and a kind nothing names would never be judged.
    """
    wanted = labels.check_kind(kind)
    if wanted == taxonomy.NO_KIND:
        # Clears the kind, and needs no taxonomy to say so.
        return wanted
    named = active_taxonomy.load(_load()).label_gate.kinds
    if wanted == taxonomy.ANY_KIND or wanted in named:
        return wanted
    raise _refused(
        "label-name-invalid",
        f"{wanted!r} is not a kind the library's taxonomy names"
        + (
            f"; it names {', '.join(named)}, and {taxonomy.ANY_KIND} passes everything"
            if named
            else f"; it declares no kinds at all, so only {taxonomy.ANY_KIND} can be "
            f"set until its label_gate section gains the published rules"
        ),
        "pass --kind with one of those, or add a rule for it to the taxonomy",
        detail={"kind": wanted, "kinds": [*named, taxonomy.ANY_KIND]},
    )


#: The ``--genre`` word that clears a label's genre, the word ``--kind`` clears
#: with, so the two fields are undone alike. Matched whatever its case.
CLEAR_GENRE = taxonomy.NO_KIND

#: How a genre reached its bucket, in the words the registry's screen uses.
_ROUTED_BY: dict[routing.Match, str] = {
    routing.Match.EXACT: "by an alias the taxonomy declares",
    routing.Match.PASSTHROUGH: "as that bucket's own name",
    routing.Match.FUZZY: "by the taxonomy's keyword rule",
    routing.Match.FALLBACK: "only as the taxonomy's fallback, kept with --accept-fallback",
}


def _declared_genre(genre: str, accept_fallback: bool) -> tuple[str, dict | None]:
    """``--genre`` as stored, and where the library's taxonomy routes it.

    Checked by routing, not by tagging (U178), since the word is written onto
    every file of the label and then filed by
    :func:`cratekit.core.routing.resolve_bucket`. A word that reaches only the
    fallback is refused unless the person confirms it, since every track of the
    label would land in the catch all. Checked here for the reason a kind is.

    Returns the word and a mapping describing the route, or None for the word
    that clears a genre.
    """
    wanted = labels.check_genre(genre)
    if wanted.casefold() == CLEAR_GENRE:
        return CLEAR_GENRE, None
    declared = active_taxonomy.load(_load())
    resolution = routing.resolve_bucket(declared, wanted)
    display = declared.bucket(resolution.bucket_id).display
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
        raise _refused(
            "label-name-invalid",
            f"{wanted!r} reaches no bucket of the library's taxonomy but its "
            f"fallback, {display}, so every track of this label would be filed "
            f"there; nothing was written",
            "pass --accept-fallback to keep the genre anyway, or a genre the "
            "taxonomy routes, or add an alias for it to the taxonomy",
            detail={
                "genre": wanted,
                "bucket": resolution.bucket_id,
                "match": resolution.match.value,
            },
        )
    rule = f" {resolution.matched_on!r}" if resolution.match is routing.Match.FUZZY else ""
    return wanted, {
        "genre": wanted,
        "bucket": resolution.bucket_id,
        "bucket_display": display,
        "match": resolution.match.value,
        "matched_on": resolution.matched_on,
        "sentence": f"genre {wanted} routes to {display} {_ROUTED_BY[resolution.match]}{rule}",
    }


def _answer(
    ctx, store: labels.RegistryStore, done: dict, label_id: str = "", route: dict | None = None
) -> Envelope:
    """The registry as it now stands, one check per label, beside what the verb did.

    ``done`` names the change; a listing names none and carries every held field,
    for a reader that is not a person. ``route`` adds where a genre the verb just
    set routes: in full to the summary, as its sentence to that label's check.
    """
    held = store.load()
    summary = {**done, "count": len(held.labels)}
    if route:
        summary["genre_route"] = {key: value for key, value in route.items() if key != "sentence"}
    if not done:
        summary["labels"] = [entry.to_json() for entry in held.labels.values()]
    routed = {label_id: route["sentence"]} if route else {}
    return ctx.envelope(data={"checks": _checks_for(held, routed), "summary": summary})


def registry_cmd(ctx) -> Envelope:
    store = labels.RegistryStore()
    args = ctx.args
    action, seeds, track_limit, offer = args.action, args.seeds, args.track_limit, args.offer
    kind, genre, bandcamp = args.kind, args.genre, args.bandcamp
    accept_fallback = bool(args.accept_fallback)
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre, bandcamp)
    if action not in ("add", "set") and (
        accept_fallback or any(given is not None for given in fields_given)
    ):
        raise _refused(
            "label-name-invalid",
            f"label registry {action} does not set --seed, --track-limit, "
            f"--offer, --kind, --genre, --bandcamp or --match, and ignoring them "
            f"would report a change that was never written",
            "use label registry set, or add, to change those fields",
        )
    if action == "list":
        return _answer(ctx, store, {})
    if action == "adopt":
        return adopt_harvested(ctx, store)
    name = ctx.args.name
    if not name:
        raise _refused(
            "label-name-invalid",
            f"label registry {action} needs a name",
            "pass the label name after the action",
        )
    if accept_fallback and genre is None:
        raise _refused(
            "label-name-invalid",
            "--accept-fallback confirms a --genre and none was given, so there is "
            "nothing for it to confirm",
            "pass --genre with the genre to keep, beside --accept-fallback",
        )
    if kind is not None:
        kind = _declared_kind(kind)
    route: dict | None = None
    if genre is not None:
        genre, route = _declared_genre(genre, accept_fallback)
    # A field's clearing word clears it, and the store keeps None for a label
    # that follows the taxonomy's default kind, so a later change of that
    # default reaches it.
    clear_genre = genre == CLEAR_GENRE
    clear_kind = kind == taxonomy.NO_KIND
    # Matched as typed whatever its case, so an account named that is set by its address.
    clear_bandcamp = bandcamp is not None and bandcamp.strip().lower() == labels.CLEAR_BANDCAMP
    # Every field but the seeds, which add and set read differently.
    fields = dict(
        match=ctx.args.match,
        track_limit=track_limit,
        offer=offer,
        kind=None if clear_kind else kind,
        clear_kind=clear_kind,
        genre=None if clear_genre else genre,
        clear_genre=clear_genre,
        bandcamp=None if clear_bandcamp else bandcamp,
        clear_bandcamp=clear_bandcamp,
    )
    if action == "add":
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)
        return _answer(ctx, store, {"added": label_id}, label_id, route)
    if action == "set":
        if all(given is None for given in fields_given):
            raise _refused(
                "label-name-invalid",
                "label registry set needs a field to change, and a set that "
                "changed nothing would report an edit that never happened",
                "pass --track-limit, --offer, --kind, --genre, --bandcamp, --seed, "
                "or --match",
            )
        edited = store.edit(name, seed_artists=seeds, **fields)
        return _answer(ctx, store, {"updated": edited.label_id}, edited.label_id, route)
    if action == "remove":
        return _answer(ctx, store, {"removed": store.remove(name)})
    if ctx.args.new_name is None:
        raise _refused(
            "label-name-invalid",
            "renaming a label needs the new display name on --to",
            "pass --to with the new name",
        )
    entry = store.load().resolve(name)
    if entry is None:
        raise _refused(
            "label-unknown",
            f"no favourite label is named {name!r}",
            "list the registry and take the identifier from it",
            detail={"name": name},
        )
    store.rename(entry.label_id, ctx.args.new_name)
    return _answer(ctx, store, {"renamed": entry.label_id})


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
    return _check(f"adopt.{item_id}", result.name, status, detail)


def adopt_harvested(ctx, store: labels.RegistryStore) -> Envelope:
    """Add every harvested label accepted in review to the registry (R-419).

    A verb of its own rather than part of ``review resolve``, which would make
    answering a review a write to a second store. Idempotent by resolution, not
    by bookkeeping: nothing is marked on the review item, and a label the
    registry already holds is skipped, so one removed since is added again,
    which is what the accepted verdict says.

    One check per accepted item, keyed on the review item, since two items can
    name one label; ``diagnostic/1`` renders checks to a person.
    """
    if ctx.args.name or ctx.args.new_name is not None:
        raise _refused(
            "label-name-invalid",
            "label registry adopt takes every harvested label accepted in review "
            "and no name; ignoring the one given would report a choice that was "
            "never applied",
            "run label registry adopt with no name",
            "or add one label with: crate label registry add <name>",
        )
    with review.open_store(_load()) as items:
        found = harvest.decided(items)
    results = store.adopt([name for _, name in found.accepted]) if found.accepted else ()
    checks = [
        _adopt_check(item_id, result)
        for (item_id, _), result in zip(found.accepted, results, strict=True)
    ]
    checks.extend(
        _check(
            f"adopt.{item_id}", item_id, "fail", f"{item_id}: accepted in review and names no label"
        )
        for item_id in found.nameless
    )
    if not checks:
        checks.append(
            _check(
                "adopt.none",
                "harvested labels",
                "info",
                f"no harvested label is accepted in review; "
                f"{found.still_open} open, {found.rejected} rejected",
            )
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

    An unbound catalogue is a warning, not a refusal: :func:`catalogue.resolve`
    raises in the worker, and asking it at enqueue would refuse work a later
    build could run, while the worker's only output is a log nobody watches.

    The same thing as ``cratekit.modules.outbound.shell.queue_warnings`` on a
    second seam (U298), not a second meaning for one name; a label sweep
    resolves nothing at enqueue (KTD2), so this one takes no arguments.
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
    """Queue one label job. The queueing path only; a resume never reaches here.

    ``item_ids`` is required (U52): ``jobs.drive`` reports a job with no items
    as SUCCEEDED, so each verb must say what its job is made of.
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
        return ctx.envelope(data=jobs.reported(store, job), warnings=queue_warnings())


def _refuse_an_itemless_job(store, job) -> None:
    """Refuse to drive a label job with no items, rather than succeeding at it.

    A build before U52 queued label jobs with no items, and the queue is durable,
    so an upgrade still holds them; ``jobs.drive`` would report one SUCCEEDED
    over a registry nothing was read from. A refusal rather than a repair, since
    items invented from today's registry would run under a snapshot nobody
    checked. The backup and outbound shells say the same thing; only the job
    engine could own it for all three.
    """
    if jobs.items(store, job.job_id):
        return
    # The steps name the way out: the job stays open after this refusal.
    raise _refused(
        "internal-error",
        f"job {job.job_id} has no items to run, so driving it would report a "
        f"success over work it never did. It was queued by a build that did not "
        f"record what its items were",
        f"cancel it with: crate job cancel {job.job_id}",
        # A sweep cannot be queued again since U109, so its way back is the
        # verb that replaced it.
        (
            f"then take label releases with: {GUIDED_VERB}"
            if job.handler_key == sweep.HANDLER_KEY
            else "then queue the import again, which records its items"
        ),
        remedy=Remedy.REPORT_DEFECT,
        detail={"job_id": job.job_id},
    )


def _resume(ctx, job_id: str) -> Envelope:
    """Continue the label job named on ``--job``, and report how it ended.

    One owner for both verbs, which differ only in what they queue. Not the
    outbound shell's resume, which requires a gate and an outbound payload
    neither label verb carries (KTD8). A claim a dead driver left is reconciled
    first. Neither the live configuration nor the registry is read here: the
    job carries the configuration it was frozen against, and the worker asks
    the registry per item.
    """
    with jobs.open_store() as store:
        job = jobs.reconcile(store, job_id)
        # The job has to be a label job: ``handlers.run_job`` resolves the worker
        # from the job row, so otherwise this verb would drive any queued job
        # without that verb's own resume time checks.
        if job.handler_key not in LABEL_KEYS:
            raise _refused(
                "job-unknown",
                f"job {job.job_id} was queued for {job.handler_key!r}, which is "
                f"not a label job, so this verb will not drive it",
                f"resume it through its own verb, or with: crate job resume {job.job_id}",
                detail={"job_id": job.job_id, "handler": job.handler_key},
            )
        warnings: tuple[dict[str, str], ...] = ()
        if job.is_open():
            _refuse_an_itemless_job(store, job)
            # A job every item of which failed raises out of here, as recorded.
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
        # A job that ended badly is not an OK exit. Outside the ``is_open``
        # branch, since a job already failed on entry is not open, and for any
        # closed job carrying a cause or a parked one (R-290).
        jobs.raise_for_state(job)
        return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)


#: The verb that took the sweep's place (U109), as a person types it, read off
#: the labels spec.
GUIDED_VERB = str(
    next(spec for spec in sources.SPECS if spec.source_id == "labels").command()
)


def sync_labels(ctx) -> Envelope:
    """Resume a labels sweep queued before U109, and refuse to queue a new one.

    ``crate label sync`` replaced the sweep, which filled review with back
    catalogue on every run. The resume half stays because a queued sweep is a
    durable row that ``crate job resume`` rebuilds as ``sync labels --job``. It
    is answered first, and nothing below reads the configuration or registry.
    """
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise _refused(
        "verb-retired",
        "sync labels no longer queues a sweep. Label releases are taken label "
        f"by label with {GUIDED_VERB}, which asks before it downloads anything",
        f"take label releases with: {GUIDED_VERB}",
        "a sweep queued before this change still runs with: crate sync labels "
        "--job JOB_ID",
    )


def import_label(ctx) -> Envelope:
    # A resume is answered first: the worker refuses a removed label per item.
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    # The configuration is read before the registry, which reads on a machine
    # never set up, so a fresh install is refused for its configuration first.
    _load()
    entry = labels.RegistryStore().load().resolve(ctx.args.name)
    if entry is None:
        raise _refused(
            "label-unknown",
            f"no favourite label is named {ctx.args.name!r}",
            "add the label to the registry before importing it",
            detail={"name": ctx.args.name},
        )
    # One label is one item; the refusal above makes a zero item job unreachable.
    return _queue(
        ctx,
        payload={"source_id": "labels", "name": entry.name, "label_id": entry.label_id},
        item_ids=(entry.label_id,),
    )


def playlist_tracks_or_refuse(found: catalogue.Catalogue, reference: str) -> list:
    """The rows of :func:`playlist_listing_or_refuse`, for a caller that reports no shortfall."""
    return playlist_listing_or_refuse(found, reference)[0]


def playlist_listing_or_refuse(
    found: catalogue.Catalogue, reference: str
) -> tuple[list, catalogue.ListingShortfall | None]:
    """Resolve and list one playlist, translating a provider failure at the boundary.

    Returns the rows and, when fewer than the playlist's declared count, the
    :class:`~cratekit.label.catalogue.ListingShortfall` (R-515); a short listing
    is never refused.

    One of the two places ``label-playlist-unreadable`` is earned, with
    :func:`_label_verifier`: a bound provider was asked about this playlist and
    could not answer. The catch is broad, since the provider's own exception
    type is the installed client's, and a ``CratekitError`` passes through so
    an adapter's own refusal keeps the act it names.
    """
    return _listed(found, reference, current=False)[:2]


def playlist_listing_judged(
    found: catalogue.Catalogue, reference: str
) -> tuple[list, catalogue.ListingShortfall | None, str]:
    """:func:`playlist_listing_or_refuse`, with the client's unpaged read beside the window (U226).

    For a caller that plans a write from the order it reads: the window read
    can serve a playlist's old order for minutes after a move. The third value
    is :func:`cratekit.acquire.listing.judge_window`'s answer: on
    ``WINDOW_UNPAGED`` the rows are the unpaged read's, on ``WINDOW_LAGS`` they
    are the window's and must not be planned from. One request more.
    """
    return _listed(found, reference, current=True)


def _listed(
    found: catalogue.Catalogue, reference: str, *, current: bool
) -> tuple[list, catalogue.ListingShortfall | None, str]:
    """The two listings' one body and one boundary, see :func:`playlist_listing_or_refuse`."""
    with catalogue.translated(lambda exc: _refused(
        "label-playlist-unreadable",
        f"the playlist {reference!r} could not be listed by the provider "
        f"({exc}); harvest needs a reachable provider playlist and will not "
        f"invent labels",
        "pass a playlist this account can read, then retry",
        detail={"playlist": reference, "kind": type(exc).__name__},
    )):
        playlist = found.playlist_for(reference)
        rows = harvest.playlist_tracks(playlist)
        declared = getattr(playlist, "num_tracks", None)
        window = listing.WINDOW_AGREES
        if current:
            unpaged = listing.playlist_tracks_unpaged(playlist)
            window = listing.judge_window(
                [listing.row_id(row) for row in rows],
                [listing.row_id(row) for row in unpaged],
                declared,
            )
            if window == listing.WINDOW_UNPAGED:
                rows = unpaged
        return rows, catalogue.ListingShortfall.of(rows, declared), window


#: The warning code a harvest carries when its playlist listed short (R-515).
HARVEST_WITHHELD = "label-harvest-playlist-withheld"


def harvest_withheld_warning(
    short: catalogue.ListingShortfall, reference: str
) -> dict[str, str]:
    """The words a person reads for a harvest over a short playlist listing."""
    return {
        "code": HARVEST_WITHHELD,
        "message": (
            f"the playlist {reference!r} listed short: {short.summary()}. The "
            f"provider counts tracks it will not serve and does not say which, so "
            f"no label was read off the {short.withheld} withheld"
        ),
    }


def favourite_tracks_or_refuse(
    found: catalogue.Catalogue, reference: str
) -> tuple[list, catalogue.HeartsShortfall | None]:
    """List the account's hearts, translating a provider failure at the same boundary.

    Returns the rows and, when shorter than the account declares, the
    :class:`~cratekit.label.catalogue.HeartsShortfall` (R-504), caught before
    the broad translation. Otherwise as :func:`playlist_tracks_or_refuse`; a
    truncated listing is refused whole, since it would read every heart past
    the cut as one the account does not hold. ``reference`` is what the person
    typed, for the detail.
    """
    try:
        with catalogue.translated(lambda exc: _refused(
            "label-playlist-unreadable",
            f"the account's favourites could not be listed by the provider "
            f"({exc}); a partial listing would miss hearts, so none is used",
            "retry once the provider can list this account's favourites",
            detail={"playlist": reference, "kind": type(exc).__name__},
        ), passing=(CratekitError, catalogue.HeartsShortfall)):
            return list(found.favourite_tracks()), None
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short


def _label_verifier(
    found: catalogue.Catalogue, reference: str
) -> Callable[[str], dict]:
    """``check_label`` with a failure boundary, and a memory of what it confirmed.

    The third provider call harvest makes. The boundary sits on the call itself,
    not around ``from_tracks``, so a failure of the local review queue is never
    reported as the provider's. ``from_tracks`` offers each name right after it
    is confirmed, and ``review.offer`` commits per call and is idempotent, so the
    refusal can say how many are already waiting and that a retry will not
    queue them twice. A ``CratekitError`` passes through unchanged.
    """
    confirmed: list[str] = []

    def check(name: str) -> dict:
        with catalogue.translated(lambda exc: _refused(
            "label-playlist-unreadable",
            f"the provider stopped answering while harvest was confirming "
            f"the label names read off {reference!r} ({exc}); the "
            f"{len(confirmed)} it had already confirmed are offered in the "
            f"review queue and are waiting there, and the rest of the "
            f"playlist was never verified",
            "retry this harvest when the provider is answering; the "
            "labels already offered will not be queued twice",
            "or read what is waiting with: crate review list",
            detail={
                "playlist": reference,
                "kind": type(exc).__name__,
                "offered": list(confirmed),
            },
        )):
            verdict = found.check_label(name)
        if str(verdict.get("verdict") or "") == "confirmed":
            confirmed.append(name)
        return verdict

    return check


def _offered(item: review.Item) -> dict:
    """One offered label: the identity ``crate review list`` keys on, and its name."""
    return {
        "id": item.item_id,
        "queue": item.queue,
        "kind": item.kind,
        "name": str(item.payload.get("name") or ""),
    }


def harvest_playlist(ctx) -> Envelope:
    """Offer the record labels behind a playlist's tracks. Imports nothing.

    The catalogue is looked up on the module at call time, so a test can
    substitute the seam; a shipped build without one refuses
    ``credential-missing`` or ``label-catalogue-unbound``. No ``--job`` and no
    gate: harvest queues nothing and writes only review rows.

    ``unresolved`` is this playlist's own failure to resolve, not the queue's
    backlog: the names a catalogue refused plus the tracks with no copyright
    string at all, which ``from_tracks`` counts as it goes.
    """
    cfg = _load()
    # Resolved before the playlist is touched, so an unbound build never lists.
    found = catalogue.resolve(cfg)
    reference = str(ctx.args.playlist)
    tracks, short = playlist_listing_or_refuse(found, reference)
    with review.open_store(cfg) as store:
        report = harvest.from_tracks(
            tracks,
            store=store,
            # Wrapped, never the bare seam method: every provider call is bounded.
            verify=_label_verifier(found, reference),
        )
    # A short playlist is said on the warnings channel, never refused (R-515).
    return ctx.envelope(
        data={
            "queue": str(review.Queue.LABEL_RELEASE),
            "items": [_offered(item) for item in report.offered],
            "unresolved": len(report.dropped) + report.nameless,
        },
        warnings=(harvest_withheld_warning(short, reference),) if short is not None else (),
        # An empty playlist is a success that found nothing.
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


#: The library view of the one job being driven, keyed by the job and its music
#: folder: a job's items run one after another in one process, so one walk
#: serves every label, and holding no other job's keeps a library from going stale.
_JOB_LIBRARY: dict[tuple[str, str], sweep.LibraryView] = {}


#: How the general catalogue is asked for the one job being driven, kept for the
#: same reason, so an unreachable catalogue is given up on once per job (R-798).
_JOB_ASKING: dict[str, genre_gate.Asking] = {}


def _asked_for(cfg: config.Config, label_id: str) -> frozenset[str]:
    """The releases ``label sync`` already asked a person about for one label.

    Imported here, since ``label.sync_cli`` imports this module.
    """
    from cratekit.label import sync_cli

    return sync_cli.asked_releases(sync_cli.load_record(cfg), label_id)


def _kept_for(held: dict, key: Any, make: Callable[[], Any]) -> Any:
    """``held[key]``, made on first use; ``held`` keeps the one job being driven alone."""
    if key not in held:
        held.clear()
        held[key] = make()
    return held[key]


def _job_asking(job) -> genre_gate.Asking:
    """The asking for ``job``, made on first use and kept for that job alone."""
    return _kept_for(_JOB_ASKING, str(job.job_id), genre_gate.Asking)


def _job_library(job, cfg: config.Config) -> Callable[[], sweep.LibraryView]:
    """The library view for ``job``, walked on first use and once per job."""
    key = (str(job.job_id), str(cfg.library.root / cfg.library.music_dir))
    return lambda: _kept_for(_JOB_LIBRARY, key, lambda: match_cli.library_view(cfg))


def _refuse_unfinished(entry, result: run.IncrementResult, source: sweep.LabelSource) -> None:
    """Refuse a sweep that did not finish, before anything records it as one (R-790).

    Asked while the item's review store is still open, so the label's round is
    recorded only once it has passed.
    """
    if result.errors:
        raise _refused(
            "label-sweep-incomplete",
            f"the sweep of {entry.name!r} could not offer "
            f"{len(result.errors)} of the releases it listed "
            f"({'; '.join(result.errors)}); the offers it did make are already in "
            f"the review queue and this label was not swept in full",
            # The raise site owns the remedy: the successful offers are durable,
            # and a resume redoes only the items that failed.
            remedy=Remedy.RESUME_JOB,
            detail={
                "label_id": entry.label_id,
                "offered": len(result.processed),
                "failed": len(result.errors),
            },
        )
    if source.unread:
        # A crawl that skipped part of the label (R-261, R-393), raised after the
        # increment, so what it read is already offered; a job item has no warning
        # channel, only a cause. Resumable only when something can change: a rate
        # limit clears, a listing the client lacks does not.
        unread = source.unread
        transient = any(one.transient for one in unread)
        parts = "; ".join(f"{one.artist} ({one.listing}: {one.reason})" for one in unread)
        raise _refused(
            "label-sweep-incomplete",
            f"the sweep of {entry.name!r} offered what it read and could not read "
            f"{len(unread)} listings of the label: {parts}. The releases on those "
            f"listings are missing from this sweep, not absent from the label",
            remedy=Remedy.RESUME_JOB if transient else Remedy.REPORT_DEFECT,
            retryable=transient,
            detail={
                "label_id": entry.label_id,
                "offered": len(result.processed),
                "unread": [
                    {"artist": one.artist, "listing": one.listing, "reason": one.reason}
                    for one in unread
                ],
            },
        )
    # A catalogue that confirms nothing is not a label with nothing new.
    # ``list_for_label`` drops every release a degraded verifier will not
    # confirm, and the increment then answers ``shortfall="empty"``. Keyed on
    # every release read having been dropped, since a label whose releases are
    # all tombstoned, or partly tombstoned and partly dropped, is an honest no
    # op. A held release counts with the dropped ones when it could not be
    # confirmed again (R-790), and the release re-verified is named with its
    # answer and how it was asked (U277, R-1634). Reaching the provider and
    # confirming nothing is usually a distributor credit, so the step names the
    # ``--match`` needle; not reaching it refuses earlier, from the increment.
    unconfirmed = len(source.dropped) + source.held_unconfirmed
    if result.shortfall == "empty" and source.dropped and unconfirmed == source.read:
        canaries = [listing.canary for _, listing in source.listings if listing.canary]
        asked_again = "".join(
            f" A release already asked about or in review was verified again, "
            f"{one.how()}: {one.said()}."
            for one in canaries
        )
        raise _refused(
            "label-sweep-incomplete",
            f"the sweep of {entry.name!r} read {unconfirmed} releases "
            f"from the catalogue and could not confirm a single one of them, so "
            f"it offered nothing and this is not a label with nothing new. The "
            f"provider answered: what failed is verification rather than reach."
            f"{asked_again}",
            f"check what the catalogue credits these releases to, then set "
            f"the needle with: crate label registry add {entry.name} --match "
            f"<credited name>",
            "or resume this job once the verification endpoint is answering",
            detail={
                "label_id": entry.label_id,
                "read": unconfirmed,
                "confirmed": 0,
                "reasons": sorted({drop.reason for drop in source.dropped}),
                **({"reverified": canaries[0].to_json()} if canaries else {}),
            },
        )


def handle(job, item, cfg) -> jobs.Produced | None:
    """Sweep one queued favourite label. The per item worker behind both keys.

    The item names the label, never the payload, or every item of a multi item
    job would do the same work. The registry is loaded with a plain
    ``RegistryStore()``: it is installation scoped and takes no configuration
    (KTD6), so frozen configuration is pinned on the review store instead
    (R17). A queued identifier the registry no longer holds is refused rather
    than swept as nothing.

    The catalogue is looked up on the module at call time, so a test can
    substitute the seam. One :class:`~cratekit.label.sweep.OwnedReleases` goes
    to the source and the increment, so each release is read once (R-259).
    Nothing is produced: the sweep offers into the review queue, the durable
    record, and ``LabelSource.acquires`` is False, so no intake file is written
    and no watermark moves (KTD7).
    """
    label_id = str(item.item_id or "")
    entry = labels.RegistryStore().load().by_id(label_id)
    if entry is None:
        raise _refused(
            "label-unknown",
            f"this job was queued for the favourite label {label_id!r} and the "
            f"registry no longer holds it, so there is nothing to sweep; a label "
            f"that was removed after the job was filed is not a label with "
            f"nothing new",
            f"re-add it with: crate label registry add {label_id}",
            "or cancel this job, since its items name labels you removed",
            detail={"label_id": label_id, "job_id": job.job_id},
        )

    # One review store for the whole item, opened against the frozen
    # configuration (R17) before the catalogue is resolved, so offers share it.
    with review.open_store(cfg) as store:
        # The declaration and what the guided sync already asked about (U107)
        # are read before the first login, so an unreadable one refuses first
        # (R-685).
        declared = active_taxonomy.load(cfg)
        asked = _asked_for(cfg, entry.label_id)
        found = catalogue.resolve(cfg)
        # One reader for ownership and the genre gate, which read the same rows.
        tracks = catalogue.ReleaseTracks(found)
        owned = sweep.OwnedReleases(cfg, tracks, library=_job_library(job, cfg))
        run_id = str((job.payload or {}).get("run_id") or job.job_id)
        source = sweep.LabelSource(
            cfg,
            registry=labels.Registry(labels={entry.label_id: entry}),
            catalogue=found,
            store=store,
            owned=owned,
            gate=genre_gate.SweepGate(
                declared,
                tracks=tracks.release_tracks,
                standing=genre_gate.StandingHolds(store),
                asking=_job_asking(job),
            ),
            run_id=run_id,
            # What the guided sync already asked about takes a place (U107).
            offered=asked,
        )
        result = run_increment(
            cfg,
            source,
            owned=owned,
            limit=labels.effective_limit(entry),
            # The payload's run id first, so two sources one sync queued share
            # an intake run (R29), else the job's.
            run_id=run_id,
        )
        _refuse_unfinished(entry, result, source)
        # What the window did not reach is recorded, never dropped (R-790,
        # U238), where the person deciding reads it, ``crate review list
        # --queue label-release --group-by label``, and only once
        # ``_refuse_unfinished`` has passed.
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
    "harvest_withheld_warning",
    "HARVEST_WITHHELD",
    "playlist_listing_judged",
    "playlist_listing_or_refuse",
    "playlist_tracks_or_refuse",
    "import_label",
    "label_import_argv",
    "queue_warnings",
    "registry_cmd",
    "run_increment",
    "sync_labels",
    "sync_labels_argv",
]
