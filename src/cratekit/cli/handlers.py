"""The job handler registry: which function runs one queued item, resolved late.

Each entry names its worker as a dotted ``module:function`` string and
:func:`resolve` is the only import, so a process merely listing jobs never
pulls every feature module in (KTD26). It lives in the CLI layer because a
core module may not import the registry or name verbs, and verbs reach
:func:`run_job` through ``Context.run_job`` (R-198).
"""

from __future__ import annotations

import importlib
from contextlib import AbstractContextManager, nullcontext
from pathlib import Path
from typing import Callable, Mapping

from cratekit.core import config, jobs
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy

#: A handler receives the job, the one item, and the configuration the job was
#: frozen against, passed in so the handler never reloads one (KTD9). The guard
#: in ``tests/test_handlers.py`` only narrows that hole, it cannot see a reload
#: through a helper. The forward reference keeps ``tests/test_config.py``'s
#: guard against module level bindings into ``config`` satisfied.
ItemHandler = Callable[[jobs.Job, jobs.Item, "config.Config"], "jobs.Produced | None"]

#: The attribute ``(function, size)`` a worker carries when the driver may hand
#: it several items in one call (:data:`cratekit.core.jobs.BatchHandler`, U270).
#: An attribute of the resolved worker, so a substituted worker carries none and
#: is driven one item at a time.
BATCH_ATTRIBUTE = "batched"

#: The attribute a worker carries for something held over one whole drive: a
#: callable answering a context manager, which :func:`run_job` enters around
#: the drive so it closes on every way out (U274). A held credential needs this
#: rather than a module cache because it must be erased when the drive ends.
PER_DRIVE_ATTRIBUTE = "per_drive"

#: ``handler_key`` to ``"dotted.module:function"``. Strings, never functions.
HANDLERS: Mapping[str, str] = {
    "acquire.download": "cratekit.acquire.cli:handle",
    "acquire.bandcamp-fetch": "cratekit.acquire.bandcamp_cli:handle_fetch",
    "acquire.fallback-fetch": "cratekit.acquire.fallback_cli:handle_fetch",
    "adopt.apply": "cratekit.adopt.apply_cli:handle",
    "adopt.move": "cratekit.adopt.move_cli:handle",
    "adopt.scan": "cratekit.adopt.scan_cli:handle",
    # Two workers in one module, each named for what it does, never ``handle``.
    "analyze.restamp": "cratekit.analysis.cli:handle_restamp",
    "analyze.run": "cratekit.analysis.cli:handle_run",
    "analyze.vocals": "cratekit.vocals.cli:handle",
    "backup.run": "cratekit.backup.cli:handle",
    "export.playlist": "cratekit.export.cli:handle",
    # One worker under two keys: a set and a playlist differ only in how their
    # tracks are listed.
    "intake.playlist": "cratekit.intake.cli:handle",
    "intake.set": "cratekit.intake.cli:handle",
    # One worker under two keys: the sweep and the import differ only in how
    # many labels they queue.
    "label.import": "cratekit.label.cli:handle",
    # One release in review per item, read from the review queue (R-815).
    "label.judge": "cratekit.label.judge_cli:handle",
    "master": "cratekit.master.cli:handle",
    # Two workers over one engine, ``rebuild_governed_tree``, in different
    # layers, each writing under its own workflow name for the session log.
    "rebuild": "cratekit.cli.rebuild:handle",
    "route.resort": "cratekit.write.routing_cli:handle_resort",
    "sync.favorites": "cratekit.favorites.cli:handle",
    "sync.labels": "cratekit.label.cli:handle",
    "tag.folder": "cratekit.tagging.cli:handle",
    "tag.retag": "cratekit.tagging.retag_cli:handle",
}

#: ``handler_key`` to why this build runs nothing for it. Every long-running
#: verb is in exactly one of these two mappings, which ``tests/test_handlers.py``
#: checks against the registry.
HANDLERS_NOT_YET_BOUND: Mapping[str, str] = {
    "job.resume": (
        "the resume verb itself: it spawns the child that drives a job, and is "
        "never queued under its own key"
    ),
}


def is_known(key: str) -> bool:
    """Whether this build has a handler for ``key``, without importing anything (KTD26)."""
    return key in HANDLERS


def unbound_reason(key: str) -> str | None:
    """Why ``key`` has no worker in this build, or ``None`` when it has one."""
    if is_known(key):
        return None
    return HANDLERS_NOT_YET_BOUND.get(key) or (
        f"{key!r} is not a handler key this build declares at all, so the job was "
        f"queued by a different build or under a verb that has since been removed"
    )


def drift_warnings(keys: "tuple[str, ...]") -> tuple[dict[str, str], ...]:
    """The one wording for "your configuration moved and this run did not" (KTD9).

    A warning, not a refusal, since the job runs on its frozen inputs anyway.
    One wording so the reporting sites cannot disagree.
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

    The only import in this module, made after the key is known to be real.
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
    """Run one job's queued items to completion, the one caller of ``jobs.drive``.

    Resolve the handler, bind the frozen configuration read off the job (never
    loaded, KTD9), then delegate; the loop's rules belong to
    :func:`cratekit.core.jobs.drive`. It does not always return: when every
    attempted item failed, ``drive`` records the job failed and raises
    ``no-evidence``.
    """
    handler = resolve(job.handler_key)
    frozen = jobs.frozen_config(job)

    def handle(driven: jobs.Job, item: jobs.Item) -> "jobs.Produced | None":
        return handler(driven, item, frozen)

    # Several items a call where the worker says so, on the same frozen config (U270).
    batching: jobs.Batching | None = None
    named = batching_of(handler)
    if named is not None:
        many, size = named

        def handle_many(driven: jobs.Job, claimed, stop):
            return many(driven, claimed, frozen, stop)

        batching = jobs.Batching(handle=handle_many, size=size)

    # Drift is reported, not enforced: an unloadable configuration drops the
    # drift report, never the frozen run. OSError is caught because a stat in
    # an untraversable folder raises PermissionError, not ConfigError.
    try:
        current: config.Config | None = config.load()
    except (config.ConfigError, OSError):
        current = None

    # What the worker holds for the whole drive, opened once and closed on every
    # way out (U274). Its warnings are read after the close, where a write back
    # happens.
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
