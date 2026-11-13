"""The job HANDLER registry: which function runs one queued item, resolved late.

``cratekit.core.jobs.drive`` is the loop that claims a job's items, runs a handler
against each, commits artifacts and records failures. Until this module landed it
had no caller anywhere in ``src``: every long-running verb froze its configuration,
queued, and reported, and ``crate job resume`` respawned a child that reported the
same job again. The items stayed ``pending`` for ever. That is residual R-198, and
this file is the half that was missing.

**WHY THE TABLE IS STRINGS AND NOT IMPORTS.** KTD26 has the job engine re-invoke
``crate`` as a subprocess rather than importing handlers, precisely so a process
that is merely listing or validating jobs does not pull every feature module in
through the back door and walk around the lazy-import stubs. A registry built as a
package of imports defeats the property the scheme exists for, and it defeats it
silently: the table still looks lazy while the import already happened at module
scope. :mod:`cratekit.modules.tools` states the same rule for the same reason. So
each entry below names its implementation as a dotted ``module:function`` string,
and :func:`resolve` is the ONLY place an import happens.

The ordering in :func:`resolve` is the one :func:`cratekit.cli.jobs.argv_for`
already established: look the key up, refuse, and only then import the one module
that owns it. Every line above the import is a line the supervisor runs against a
key it does not trust.

**WHY THIS IS NOT A FIELD ON ``registry.Entry``.** A ``worker: str | None`` field
validated in ``Entry.__post_init__`` would make a declaration unable to outlive its
verb by construction, which is genuinely better, and it was rejected for three
reasons. The absence needs a REASON and a residual number, which is a second field
``Entry`` has no room for. ``ENTRIES`` is appended to by every unit, so a field
carrying eighteen ``None`` values invites the next author to leave it ``None``
without noticing. And the unbound reason is data the reporting surface reads, not a
validation message. Keeping the binding and the absence in one small table beside
the registry says both things in one readable place.

**WHY THE DRIVER LIVES HERE RATHER THAN IN ``core``.** Issue #64 asked for
``core/handlers.py`` and the layering guard refuses it twice: a core module may not
import :mod:`cratekit.cli.registry`, and it may not hold a string that is a verb
name or that names a feature package, which every handler key and every declaration
below is. The verbs cannot import this module either, for the mirrored reason: a
verb is modules-ranked and this is CLI-ranked. They reach :func:`run_job` through
``Context.run_job`` instead, which is the one route the ladder allows.

Layer: cli.
"""

from __future__ import annotations

import importlib
from contextlib import AbstractContextManager, nullcontext
from pathlib import Path
from typing import Callable, Mapping

from cratekit.core import config, jobs
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy

#: What a handler is: it receives the job, the one item it must do, and the
#: configuration that job was FROZEN against. The configuration is a parameter
#: rather than something the handler loads, because KTD9 closes exactly the resume
#: bug that reloading reintroduces and a handler holding a fresh config is that
#: defect wearing a new hat. The parameter removes the NEED to load one. It does
#: not remove the ability, and neither does the guard in ``tests/test_handlers.py``
#: that goes with it: that guard reads three spellings of the reload and says so,
#: and it cannot see one reached through a helper. Stated at both ends rather than
#: at neither, because a guard described as closing a hole it only narrows is the
#: thing a later reader trusts.
#:
#: The configuration is spelled as a forward reference because the guard in
#: ``tests/test_config.py`` refuses any module-level binding that reaches into
#: ``config``, and it is right to: it cannot tell an annotation from a snapshot,
#: and a snapshot is the defect that guard exists for.
ItemHandler = Callable[[jobs.Job, jobs.Item, "config.Config"], "jobs.Produced | None"]

#: U270. The attribute a worker carries when the driver may hand it several
#: of a job's items in one call: ``(function, size)``, the function taking the
#: job, the claimed items, the frozen configuration and the stop callable, and
#: answering one outcome per item (:data:`cratekit.core.jobs.BatchHandler`).
#:
#: AN ATTRIBUTE OF THE RESOLVED WORKER RATHER THAN A SECOND TABLE, so the batch
#: form can never run where the per item worker it belongs to was not the one
#: resolved: a substituted worker carries no batch form and is driven one item
#: at a time, the way it was written to be.
BATCH_ATTRIBUTE = "batched"

#: U274. The attribute a worker carries when something must be held for one
#: whole drive of a job rather than built per item: a callable taking nothing
#: and answering a context manager, which :func:`run_job` enters around the
#: drive and which therefore closes on every way out of it, finished, parked,
#: interrupted or raised. The download worker names the vendored adapter's
#: drive, which holds one token file and one login for every track of a job.
#:
#: AN ATTRIBUTE OF THE RESOLVED WORKER, for the batch form's reason: a
#: substituted worker carries none, and is driven the way it was written to be.
#: The job engine has no per drive setup seam of its own; the intake worker's
#: one library index per drive is a module cache keyed by the drive for that
#: reason, and a held credential cannot be, because it must be erased when the
#: drive ends.
PER_DRIVE_ATTRIBUTE = "per_drive"

#: ``handler_key`` to ``"dotted.module:function"``. Strings, never functions.
HANDLERS: Mapping[str, str] = {
    "acquire.download": "cratekit.acquire.cli:handle",
    "acquire.bandcamp-fetch": "cratekit.acquire.bandcamp_cli:handle_fetch",
    "acquire.fallback-fetch": "cratekit.acquire.fallback_cli:handle_fetch",
    "adopt.apply": "cratekit.adopt.apply_cli:handle",
    "adopt.move": "cratekit.adopt.move_cli:handle",
    "adopt.scan": "cratekit.adopt.scan_cli:handle",
    # TWO WORKERS IN ONE MODULE, named for what each does to a file: the run
    # analyses and finalizes it, the restamp rescores one tag on it. Neither is
    # ``handle``, because a module owning two workers under one anonymous name
    # would have the second one's binding read as the first's.
    "analyze.restamp": "cratekit.analysis.cli:handle_restamp",
    "analyze.run": "cratekit.analysis.cli:handle_run",
    "analyze.vocals": "cratekit.vocals.cli:handle",
    "backup.run": "cratekit.backup.cli:handle",
    "export.playlist": "cratekit.export.cli:handle",
    # ONE WORKER UNDER TWO KEYS, for the reason the label pair below gives: a
    # set and a playlist differ in how their tracks are LISTED, recognition
    # against a recording or a catalogue read, and in nothing about what is
    # done with one track once it is queued.
    "intake.playlist": "cratekit.intake.cli:handle",
    "intake.set": "cratekit.intake.cli:handle",
    # ONE WORKER UNDER TWO KEYS, which the string table makes ordinary rather than
    # special: the sweep and the import differ in how many favourite labels they
    # queue and in nothing about how one is swept, and the worker takes its label
    # from the item either way.
    "label.import": "cratekit.label.cli:handle",
    # ONE RELEASE ALREADY IN REVIEW PER ITEM, and a worker of its own: it reads
    # the review queue where the pair around it list a catalogue (R-815).
    "label.judge": "cratekit.label.judge_cli:handle",
    "master": "cratekit.master.cli:handle",
    # ONE ENGINE UNDER TWO KEYS, and unlike the pairs above these two are not one
    # worker: they are two workers over one engine, in two modules that cannot
    # import each other because ``rebuild`` is a CLI verb and ``route.resort`` is
    # a write-layer one. What they share is
    # ``cratekit.write.rebuild.rebuild_governed_tree``, and what differs is the
    # workflow name each writes under, so the session log can say which verb
    # touched the library.
    "rebuild": "cratekit.cli.rebuild:handle",
    "route.resort": "cratekit.write.routing_cli:handle_resort",
    "sync.favorites": "cratekit.favorites.cli:handle",
    "sync.labels": "cratekit.label.cli:handle",
    "tag.folder": "cratekit.tagging.cli:handle",
    "tag.retag": "cratekit.tagging.retag_cli:handle",
}

#: ``handler_key`` to why this build runs nothing for it. Every landed
#: long-running verb is in exactly one of these two mappings, and
#: ``tests/test_handlers.py`` derives that population from the registry rather
#: than listing it, so a verb added later without a handler fails the suite
#: instead of failing at somebody's queue.
HANDLERS_NOT_YET_BOUND: Mapping[str, str] = {
    "job.resume": (
        "the resume verb itself: it spawns the child that drives a job, and is "
        "never queued under its own key"
    ),
}


def is_known(key: str) -> bool:
    """Whether this build has a handler for ``key``, WITHOUT importing anything.

    This is the supervising question, asked by a process that may be doing nothing
    more than listing jobs. Answering it by import would load every feature module
    into that process, which is the whole thing KTD26 exists to prevent.
    """
    return key in HANDLERS


def unbound_reason(key: str) -> str | None:
    """Why ``key`` has no worker in this build, or ``None`` when it has one.

    Reported rather than hidden. Before this seam every queued verb was equally
    broken, which at least taught the user that queues do not run; one working
    verb and nineteen silent ones would teach the opposite.
    """
    if is_known(key):
        return None
    return HANDLERS_NOT_YET_BOUND.get(key) or (
        f"{key!r} is not a handler key this build declares at all, so the job was "
        f"queued by a different build or under a verb that has since been removed"
    )


def drift_warnings(keys: "tuple[str, ...]") -> tuple[dict[str, str], ...]:
    """The one wording for "your configuration moved and this run did not" (KTD9).

    A warning rather than a refusal. The job runs against its frozen inputs
    whatever this says; what the person needs is to know that the setting they
    just edited is not the setting this run is using. It lives here rather than in
    each reporting site because two sentences for one fact is how the two come to
    disagree, and one of them is then wrong about which copy a run used.
    """
    if not keys:
        return ()
    return (
        {
            "code": "config-drift",
            "message": (
                f"configuration changed since this job was queued; it runs against "
                f"the frozen copy. Changed: {', '.join(keys)}"
            ),
        },
    )


def _declaration(key: str) -> str:
    try:
        return HANDLERS[key]
    except KeyError:
        raise refuse(
            "internal-error",
            f"this build declares no handler for {key!r}, so a job queued under "
            f"it has nothing to run its items",
            remedy=Remedy.REPORT_DEFECT,
            origin=("cli.handlers",),
            detail={"handler": key},
        ) from None


def resolve(key: str) -> ItemHandler:
    """The function that runs one item of a job queued under ``key``.

    The ONLY import in this module, and it happens after the key is known to be
    real, for the one module that owns it.
    """
    declaration = _declaration(key)
    dotted, separator, attribute = declaration.partition(":")
    if not separator or not dotted or not attribute:
        raise refuse(
            "internal-error",
            f"the handler declared for {key!r} is {declaration!r}, which is not "
            f"a 'module:function' declaration",
            remedy=Remedy.REPORT_DEFECT,
            origin=("cli.handlers",),
            detail={"handler": key, "declaration": declaration},
        )
    module = importlib.import_module(dotted)
    found = getattr(module, attribute, None)
    if found is None:
        raise refuse(
            "internal-error",
            f"the handler declared for {key!r} names {attribute!r} in {dotted}, "
            f"and that module has no such member",
            remedy=Remedy.REPORT_DEFECT,
            origin=("cli.handlers",),
            detail={"handler": key, "declaration": declaration},
        )
    if not callable(found):
        raise refuse(
            "internal-error",
            f"the handler declared for {key!r} names {attribute!r} in {dotted}, "
            f"and that member is not callable",
            remedy=Remedy.REPORT_DEFECT,
            origin=("cli.handlers",),
            detail={"handler": key, "declaration": declaration},
        )
    return found


def batching_of(handler: object) -> "tuple[Callable[..., Mapping[str, object]], int] | None":
    """The batch form a worker names for itself, checked, or None when it names none (U270)."""
    named = getattr(handler, BATCH_ATTRIBUTE, None)
    if named is None:
        return None
    function, size = named if isinstance(named, tuple) and len(named) == 2 else (None, None)
    if not callable(function) or not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise refuse(
            "internal-error",
            f"a worker names {named!r} as its batch form, which is not a callable "
            f"and a size of at least one",
            remedy=Remedy.REPORT_DEFECT,
            origin=("cli.handlers",),
            detail={"handler": getattr(handler, "__qualname__", repr(handler))},
        )
    return function, size


def per_drive_of(handler: object) -> "Callable[[], AbstractContextManager[object]] | None":
    """What a worker holds for a whole drive, checked, or None when it names nothing (U274)."""
    named = getattr(handler, PER_DRIVE_ATTRIBUTE, None)
    if named is None:
        return None
    if not callable(named):
        raise refuse(
            "internal-error",
            f"a worker names {named!r} as what it holds for a drive, which is not "
            f"a callable answering a context manager",
            remedy=Remedy.REPORT_DEFECT,
            origin=("cli.handlers",),
            detail={"handler": getattr(handler, "__qualname__", repr(handler))},
        )
    return named


def run_job(store: jobs.JobStore, job: jobs.Job, *, root: Path | None = None) -> jobs.DriveResult:
    """Run one job's queued items to completion. The ONE caller of ``jobs.drive``.

    Three steps and nothing else. Resolve the handler, read the frozen
    configuration ONCE and bind it, to its batch form too when the worker
    names one (:data:`BATCH_ATTRIBUTE`, U270), then delegate. The loop's shape is the
    engine's contract and is documented on :func:`cratekit.core.jobs.drive`: the
    driver lock first, orphaned claims released once, the interrupt flag checked
    between items and before a commit, an artifact durable before its row flips to
    done, and a total failure recorded as failed rather than returned as an empty
    success. Reimplementing any of that here would be a second opinion about a
    rule that already has an owner.

    IT DOES NOT ALWAYS RETURN. When items were attempted and none succeeded,
    ``drive`` records the job as failed and then raises ``no-evidence``, so a
    caller that always expects a ``DriveResult`` is wrong about the common failure
    path of a one-item job.

    THE FROZEN CONFIGURATION IS READ OFF THE JOB, never loaded. KTD9 closes the
    recorded resume bug where a queued run re-resolved its configuration and could
    empty its own output.
    """
    handler = resolve(job.handler_key)
    frozen = jobs.frozen_config(job)

    def handle(driven: jobs.Job, item: jobs.Item) -> "jobs.Produced | None":
        return handler(driven, item, frozen)

    # SEVERAL ITEMS A CALL WHERE THE WORKER SAYS SO (U270), with the same frozen
    # configuration bound, so a batch is never driven against a fresher one.
    batching: jobs.Batching | None = None
    named = batching_of(handler)
    if named is not None:
        many, size = named

        def handle_many(driven: jobs.Job, claimed, stop):
            return many(driven, claimed, frozen, stop)

        batching = jobs.Batching(handle=handle_many, size=size)

    # DRIFT IS COMPUTED, NOT ENFORCED. A configuration that cannot be loaded at
    # all is not a reason to refuse to finish work that was already queued and
    # frozen, so the drift report is dropped rather than the run.
    #
    # OSError IS IN THE TUPLE FOR A REASON THIS PACKAGE ALREADY PAID FOR.
    # ``config.load`` stats the file before reading it and converts only
    # ``FileNotFoundError``, so a stat under a directory this account cannot
    # traverse raises ``PermissionError`` and no ``ConfigError`` at all.
    # ``cli.__init__._membership`` records that exact incident: the same call, the
    # same narrow except, and a traceback out of ``crate --help``. Here it would
    # abort a job that was queued and frozen precisely so it would not need the
    # current configuration.
    try:
        current: config.Config | None = config.load()
    except (config.ConfigError, OSError):
        current = None

    # WHAT THE WORKER HOLDS FOR THE WHOLE DRIVE (U274), around the drive and
    # nothing else, so it is opened once whatever the item count and closed on
    # every way out, a park and the no evidence raise included.
    # What it could not do when it closed comes back as warnings, read AFTER
    # the close, since the close is where a write back happens.
    held = per_drive_of(handler)
    with held() if held is not None else nullcontext() as holding:
        result = jobs.drive(
            store, job.job_id, handle, root=root, current_config=current, batch=batching
        )
    noted = tuple(getattr(holding, "warnings", None) or ())
    if noted:
        result.warnings = (*result.warnings, *noted)
    return result


__all__ = [
    "BATCH_ATTRIBUTE",
    "HANDLERS",
    "HANDLERS_NOT_YET_BOUND",
    "PER_DRIVE_ATTRIBUTE",
    "ItemHandler",
    "batching_of",
    "drift_warnings",
    "is_known",
    "per_drive_of",
    "resolve",
    "run_job",
    "unbound_reason",
]
