"""What the two outbound verbs share, so a rule has one owner rather than two.

``crate export playlist`` and ``crate sync favorites`` differ in what they write
and what an item is, not in how a queued job is resumed, how a frozen
configuration is loaded, or what a person is warned of before confirming.

THE RESUME CARRIES R-225: a job that half failed exits with its own cause, never
a normal envelope, through ``jobs.raise_for_state``, which also refuses a parked
job (R-290).

NOT HERE: ``confirm_digest`` and ``summary`` stay one per shell, since the two
verbs digest different keys and report an unmatched row in different shapes;
both are passed in. ``ctx`` is untyped because ``cratekit.cli`` is above this
layer (KTD23).

Layer: modules.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import account
from cratekit.modules.outbound.source import ExportAge, ResolvedPlaylist

#: The two payload keys both verbs freeze, spelled once, since a key spelled
#: two ways is a resume that does different work from the run it continues.
PLAYLIST = "playlist"
EXPORT = "export"

#: The resolved track identifiers the job writes, frozen so the confirm digest
#: covers the write set itself rather than a path whose document can change.
TRACKS = "tracks"

#: The fact a gate screen names the export document's path under (R-693), not
#: ``EXPORT``, which :func:`shown_export` already shows.
EXPORT_PATH = "export path"

#: An unmatched row the account gave no reason for, in both verbs' words (R-850, R-856).
NO_MATCH = "the provider returned no track for it"


def unmatched_tally(outbound: Mapping[str, Any]) -> tuple[int, int] | None:
    """How many rows a finished job left unmatched, and of how many, or none.

    The arithmetic both ``concluded`` hooks share: ``None`` when the summary
    does not count or matched everything. A bool is no count.
    """
    counts = outbound.get("counts")
    if not isinstance(counts, Mapping):
        return None
    missed = counts.get("unmatched")
    if not _whole(missed) or missed <= 0:
        return None
    return missed, sum(n for n in counts.values() if _whole(n))


def _whole(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def load_config(origin: str) -> config.Config:
    """The current configuration, or the refusal a person can act on.

    ``cli.output.load_config`` (U298) gives the same cause, but this layer
    cannot import it and this one takes the origin as one string.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=(origin,),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def reported(
    store,
    job,
    cfg: config.Config,
    summary: Callable[[config.Config, str], Mapping[str, Any]],
) -> dict[str, Any]:
    """One queued job, flattened for the envelope, with what it actually wrote."""
    # UNDER ``progress``, NOT BESIDE IT: ``job_state/1`` forbids an undeclared
    # top level key, and ``progress`` is declared an open object.
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": {
            **jobs.progress(store, job.job_id),
            "outbound": dict(summary(cfg, job.job_id)),
        },
    }


#: The four things :func:`shown_export` can say about an export's date, as
#: words, since a missing boolean renders as "none", which reads as fresh.
AGE_STALE = "stale"
AGE_WITHIN_LIMIT = "within-limit"
AGE_FUTURE_DATED = "future-dated"
AGE_UNKNOWN = "unknown"


def freshness(age: ExportAge) -> str:
    """Which of the four an age is. The two that cannot be judged are asked FIRST."""
    if not age.known:
        return AGE_UNKNOWN
    if age.future_dated:
        return AGE_FUTURE_DATED
    return AGE_STALE if age.stale else AGE_WITHIN_LIMIT


def _local_date(moment) -> str:
    """The date as the person's own machine spells it, as Finder shows it."""
    return moment.astimezone().date().isoformat()


def _spelled(age: ExportAge) -> str | None:
    """The age in days and hours, so "past seven days" never reads as seven."""
    elapsed = age.age
    if elapsed is None:
        return None
    hours = elapsed.seconds // 3600
    return f"{elapsed.days} days {hours} hours"


def shown_export(age: ExportAge) -> dict[str, Any]:
    """What the confirm gate shows about the document the write is read from.

    SHOWN EVERY TIME (R-227), so a missing line never means recent, with the
    warning's sentence too, since a refusal carries no warnings. A display
    value, outside the digest, which an age would stale at midnight.
    """
    export: dict[str, Any] = {
        "file": age.path.name,
        "written": (
            age.written.astimezone().replace(microsecond=0).isoformat()
            if age.written is not None
            else None
        ),
        "age": _spelled(age),
        "age_days": age.age_days,
        "stale_after_days": age.limit_days,
        "freshness": freshness(age),
    }
    for warning in age_warnings(age):
        export["warning"] = warning["message"]
    return {"export": export}


def age_warnings(age: ExportAge) -> tuple[dict[str, str], ...]:
    """The sentence a person reads when the export is old, or its age unreadable.

    A WARNING AND NEVER A REFUSAL, since only the person knows whether an old
    export is still right. At most one, which :func:`shown_export` relies on.
    """
    written = age.written
    if written is None:
        code, message = "outbound-export-age-unknown", (
            f"the date {age.path.name} was last written could not be "
            f"read, so nothing here can say whether it still describes "
            f"the library"
        )
    elif age.future_dated:
        code, message = "outbound-export-age-unknown", (
            f"{age.path.name} is dated {_local_date(written)}, which is "
            f"in the future, so its age cannot be judged and nothing "
            f"here can say whether it still describes the library. "
            f"Export the collection again if it may have moved"
        )
    elif age.stale:
        code, message = "outbound-export-stale", (
            f"{age.path.name} was last written on "
            f"{_local_date(written)}, {_spelled(age)} ago, which is "
            f"past the {age.limit_days} days "
            f"outbound.export_stale_days allows. Anything the library "
            f"gained or lost since then is not in this write. Export "
            f"the collection again if it has moved"
        )
    else:
        return ()
    return ({"code": code, "message": message},)


def queue_warnings(
    resolved: ResolvedPlaylist, *, noun: str, age: ExportAge
) -> tuple[dict[str, str], ...]:
    """What the person should know at the moment they are asked to confirm.

    ``age`` is required, so a new caller cannot leave the export's age out
    (R-227). An unbound provider is warned of here, since a missing adapter
    cannot appear before the worker runs. Dangling, repeated and missing pink
    rows are named, since a count alone is nothing to act on.
    """
    warnings: list[dict[str, str]] = [*age_warnings(age)]
    found = (
        (
            not account.bound(),
            "outbound-account-unbound",
            "this build has no streaming provider adapter, so this job "
            "will queue and then fail at the provider seam",
        ),
        (
            resolved.dangling,
            "playlist-track-missing",
            f"{len(resolved.dangling)} {noun}(s) this playlist names are "
            f"not in the export's collection and are not queued: "
            f"{', '.join(resolved.dangling)}",
        ),
        (
            resolved.repeated,
            "playlist-track-repeated",
            f"{len(resolved.repeated)} {noun}(s) appear more than once in "
            f"this playlist and are queued once: "
            f"{', '.join(resolved.repeated)}",
        ),
        (
            resolved.pink_missing,
            "favorites-pink-export-missing",
            f"{len(resolved.pink_missing)} pink row(s) the library "
            f"carries are not in the export's collection and are not "
            f"queued: {', '.join(resolved.pink_missing)}",
        ),
    )
    warnings.extend({"code": code, "message": message} for due, code, message in found if due)
    return tuple(warnings)


def declined(job_id: str = "") -> dict[str, Any]:
    """The payload for a confirmation answered with abort: the declared ``job_state`` shape.

    ``adopt.apply_cli`` passes ``job_id: None``, which fails the same
    validator; that divergence is R-234.
    """
    return {"job_id": job_id, "state": "declined", "cause": None, "progress": {}}


def resume(
    ctx,
    spec,
    job_id: str,
    *,
    digest: Callable[..., str],
    summary: Callable[[config.Config, str], Mapping[str, Any]],
    standing: tuple[dict[str, str], ...] = (),
    frozen_extra: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
    concluded: Callable[[Mapping[str, Any]], tuple[dict[str, str], ...]] | None = None,
):
    """Answer the gate from the frozen payload, then drive the job's items.

    NOTHING IS READ FROM THE EXPORT DOCUMENT: the items are queued and the
    digest is taken off the payload, which ``jobs.spawn`` rebuilds a child's
    command line from, so a moved file never refuses a resume and a
    regenerated one never changes a confirmed job.

    ``standing`` is what every pass of the verb says (R-424), ahead of the
    run's own warnings; ``frozen_extra`` reads off the payload what one verb
    adds to its digest; ``concluded`` turns the job's own summary into
    warnings once it is driven (R-850). A failed job raises its cause (R-225,
    ``jobs.raise_for_state``) rather than reporting.
    """
    with jobs.open_store() as store:
        queued = jobs.get(store, job_id)
        payload = queued.payload or {}
        playlist = str(payload.get(PLAYLIST) or "")
        exported = str(payload.get(EXPORT) or "")
        tracks = [str(track) for track in payload.get(TRACKS) or ()]
        extra = dict(frozen_extra(payload)) if frozen_extra is not None else {}
        # THE FROZEN PLAN IS SHOWN THROUGH THE GATE LAYER (R-693).
        option = ctx.gate.require(
            spec,
            plan={"digest": digest(playlist, exported, tracks, **extra), "items": tracks},
            context={PLAYLIST: playlist, EXPORT_PATH: exported, **extra},
        )
        if option == "abort":
            return ctx.envelope(data=declined(queued.job_id), outcome=Outcome.NO_OP)
        frozen = jobs.frozen_config(queued)
        # RECONCILE BEFORE DRIVING, since a dead driver's claim is invisible.
        job = jobs.reconcile(store, job_id)
        warnings: tuple[dict[str, str], ...] = ()
        if job.is_open():
            # A JOB WITH NO ITEMS, frozen by an older build, would drive to a
            # clean success over work it never did.
            if not jobs.items(store, job.job_id):
                raise refuse(
                    "internal-error",
                    f"job {job.job_id} has no items to run, so driving it would "
                    f"report a success over work it never did. It was queued by "
                    f"a build that did not record what its items were",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=("outbound", "shell"),
                    detail={"job_id": job.job_id},
                )
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
        # ANY CLOSED JOB CARRYING A CAUSE, a cancelled one included.
        jobs.raise_for_state(job)
        data = reported(store, job, frozen, summary)
        said = concluded(data["progress"]["outbound"]) if concluded is not None else ()
        return ctx.envelope(data=data, warnings=(*standing, *warnings, *said))


__all__ = [
    "EXPORT", "EXPORT_PATH", "NO_MATCH", "PLAYLIST", "TRACKS", "age_warnings", "freshness",
    "load_config", "queue_warnings", "reported", "resume", "shown_export", "unmatched_tally",
]
