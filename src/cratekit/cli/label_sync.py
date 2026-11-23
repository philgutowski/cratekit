"""``crate label sync``, its go taken on through the tail to the landing's gate (U190).

The go, :mod:`cratekit.label.go`, is a feature module and may not reach the CLI
dispatcher, so the ``label.sync`` entry names this module: it runs the verb's
own handler unchanged, then, when the go's report names a tail, runs it through
:mod:`cratekit.cli.tail`, the chain ``sync land`` runs, so both answer the same.
It ends PENDING at the landing's gate, or on a step's own refusal with the rest
of the tail named, the download kept either way. The landing reached is recorded
on the go's run and what the folder holds is kept under the job (U239, R-1467),
so a later ``--go`` under that run reads its own tracks. Nothing that arrived
while the tail ran is landed with it (R-1499). A go holds the staging lock
(U293). A go that names no tail is returned untouched.
"""

from __future__ import annotations

import dataclasses
import shlex
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, tail
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.core import jobs, staging_lock
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import beside as staged

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.label_sync",)
#: The warning a landing the go's own run could not record is named under (U239).
UNRECORDED_WARNING = "label-sync-landing-unrecorded"
#: The origin the go's own refusals carry, so only they are read for a landing.
_GO_ORIGIN = "label.go"

#: The key every check the chain adds to the go's report carries, before its step.
NAMESPACE = "label.sync.go"


def build_sync(parser, entry) -> None:
    """The verb's own arguments, with this module's handler in front of its own."""
    from cratekit.label import sync_cli

    sync_cli.build_sync(parser, entry)
    parser.set_defaults(_handler=label_sync)


def _land_of(envelope: Envelope) -> Mapping[str, Any] | None:
    """The tail the go's report names, or None when it names none."""
    summary = envelope.data.get("summary")
    report = summary.get("go") if isinstance(summary, Mapping) else None
    return _land_in(report)


def _land_in(report: Any) -> Mapping[str, Any] | None:
    """The landing a go's report or refusal names under its key, or None."""
    from cratekit.label import go

    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
    if not isinstance(land, Mapping):
        return None
    if not all(isinstance(land.get(key), str) and land.get(key) for key in ("folder", "pass")):
        return None
    return land


def _with_commands(error: CratekitError) -> CratekitError:
    """A go's refusal that names a landing, with the tail as a person types it (U239).

    Only the go's own refusal, by its origin, since only it puts a landing in
    its detail.
    """
    cause = error.cause
    land = _land_in(cause.detail) if _GO_ORIGIN in cause.origin else None
    if land is None:
        return error
    folder = Path(str(land["folder"])).expanduser().absolute()
    steps = (
        *cause.remediation.steps,
        "the tail by hand, in this order: "
        + "; then ".join(_commands(folder, _landing_args(land), tail.TAG)),
    )
    return rebuilt(
        error,
        dataclasses.replace(cause, remediation=dataclasses.replace(cause.remediation, steps=steps)),
    )


def _chain(ctx: Context) -> tail.Chain:
    return tail.Chain(
        progress=ctx.progress,
        namespace=NAMESPACE,
        title="label sync --go",
        steps=tail.STEPS,
        origin=_ORIGIN,
        again="run the rest of the tail as this refusal names it",
    )


def _landing_args(land: Mapping[str, Any]) -> list[str]:
    manifest = land.get("manifest")
    return [
        *(["--manifest", str(manifest)] if isinstance(manifest, str) and manifest else []),
        "--pass",
        str(land["pass"]),
    ]


def _commands(folder: Path, landing: Sequence[str], step: str) -> list[str]:
    """The tail as a person types it, from ``step`` to the landing.

    ``name apply`` without its confirm answered, so a person reads its plan.
    """
    words = {one: ["crate", *argv, str(folder)] for one, _verb, argv in tail.TAIL}
        # No pass (U172): no account playlist asked for a label go's tracks.
    words[tail.GUESS] = ["crate", *tail.guess_argv(folder)]
    words[tail.NAME] = ["crate", "name", "apply", "--root", str(folder)]
    words[tail.LAND] = ["crate", "intake", "land", str(folder), *landing]
    return [shlex.join(words[one]) for one in tail.STEPS[tail.STEPS.index(step):]]


def _data(envelope: Envelope, chain: tail.Chain) -> dict[str, Any]:
    """The go's report with the chain's checks after its own, and its record beside it."""
    data = dict(envelope.data)
    summary = dict(data.get("summary") or {})
    summary["tail"] = dict(chain.summary)
    return {**data, "checks": [*(data.get("checks") or ()), *chain.checks], "summary": summary}


def label_sync(ctx: Context) -> Envelope:
    """Run the verb, then the tail its go names. See the module docstring."""
    if not getattr(ctx.args, "go", False):
        return _label_sync(ctx)
    # A go stages, so it holds the staging lock for its whole length (U293).
    with staging_lock.held("crate label sync --go", run_id=ctx.run.run_id):
        return _label_sync(ctx)


def _label_sync(ctx: Context) -> Envelope:
    from cratekit.label import sync_cli

    try:
        envelope = sync_cli.label_sync(ctx)
    except CratekitError as exc:
        carried = _with_commands(exc)
        if carried is exc:
            raise
        raise carried from None
    land = _land_of(envelope)
    if land is None:
        return envelope
    cfg = tail.load_config(_ORIGIN)
    chain = _chain(ctx)
    folder = Path(str(land["folder"])).expanduser().absolute()
    landing = _landing_args(land)
    warnings = [*envelope.warnings]
    before = _settled(land, folder)
    try:
        if isinstance(before, CratekitError):
            raise tail.Stop(tail.TAG, before)
        tail.through_name(chain, folder, cfg)
        # Nothing may have arrived while the tail ran, or the landing would
        # take it under the go's pass (R-1499).
        changed = _arrived(land, folder, landing, before)
        if changed is not None:
            raise tail.Stop(tail.LAND, changed, continues=False)
        try:
            tail.land(chain, folder, landing)
        except tail.Attend as stop:
            # Read once more after the plan: an arrival before the landing's
            # own listing is in the plan, so the plan is refused.
            changed = _arrived(land, folder, landing, before)
            if changed is None:
                raise
            raise tail.Stop(tail.LAND, _planned_over(changed, stop), continues=False) from None
    except tail.Done as done:
        chain.summary["stopped_at"] = done.step
    except tail.Attend as stop:
        warnings.extend(_kept(cfg, land, folder, before))
        warnings.extend(_remember(ctx, stop, land))
        return _attended(ctx, envelope, chain, stop, folder, landing, warnings)
    except tail.Stop as stop:
        # The record's warning rides the refusal.
        chain.warnings.extend(_kept(cfg, land, folder, before))
        raise _ended(envelope, chain, stop, folder, landing) from None
    warnings.extend(_kept(cfg, land, folder, before))
    return ctx.envelope(
        data=_data(envelope, chain),
        outcome=envelope.outcome,
        warnings=[*warnings, *chain.warnings],
    )


def _remember(
    ctx: Context, stop: tail.Attend, land: Mapping[str, Any]
) -> list[dict[str, str]]:
    """Keep the landing's run on the go's run once the tail stopped at its gate (U239).

    Only a stop at the landing's own gate, since a stop for the backup
    acknowledgment planned no landing. Recorded under the job, on the run whose
    go queued it, the run a later ``--go`` takes the job on under; a record
    that cannot be saved is a warning, never a refusal.
    """
    from cratekit.label import go

    landed = (stop.cause.detail or {}).get("run_id")
    if not (stop.step == tail.LAND and stop.cause.reason == tail.GATE_STOP and landed):
        return []
    return _record(
        ctx,
        land,
        go.landing_role,
        str(landed),
        what=f"the landing under run {landed}",
        lost="does not know this landing was planned",
    )


def _own(land: Mapping[str, Any]) -> set[str]:
    job = land.get("job")
    return {job} if isinstance(job, str) and job else set()


def _settled(land: Mapping[str, Any], folder: Path) -> staged.Settled | CratekitError:
    """What the folder holds of other downloads as the go's tail starts (R-1499).

    A folder or queue that cannot be read is the refusal, returned for the
    caller to end the tail with.
    """
    try:
        with jobs.open_store() as store:
            return staged.settled(store, folder, _own(land))
    except CratekitError as exc:
        return exc
    except OSError as exc:
        return staged_refusal(folder, exc)


def staged_refusal(folder: Path, exc: OSError) -> CratekitError:
    """The refusal for a staging folder the go's tail cannot list (R-1499)."""
    return refuse(
        "intake-list-unusable",
        f"the staging folder {folder} could not be listed ({exc}), so what arrives in "
        f"it while the tail runs cannot be read; the tail was not run",
        steps=(f"make {folder} readable, then run the go again",),
        origin=(_GO_ORIGIN,),
        detail={"folder": str(folder)},
    )


def _arrived(
    land: Mapping[str, Any], folder: Path, landing: Sequence[str], before: staged.Settled
) -> CratekitError | None:
    """The refusal for what arrived while the go's tail ran, or None (R-1499).

    Read against what the folder held as the tail started; an unreadable queue
    refuses too.
    """
    try:
        with jobs.open_store() as store:
            return staged.arrived(
                store,
                folder,
                _own(land),
                before,
                origin=(_GO_ORIGIN,),
                batch=f"the go's download {land.get('job')}",
                land_command=_commands(folder, landing, tail.LAND)[0],
            )
    except CratekitError as exc:
        return exc


def _unkept(folder: Path, job: str, why: str) -> dict[str, str]:
    return {
        "code": UNRECORDED_WARNING,
        "message": (
            f"what the tail left in {folder} was not kept for job {job}, since {why}; a "
            f"later go under its run reads its own tracks there as not its own, and names "
            f"the tail by hand"
        ),
    }


def _planned_over(changed: CratekitError, stop: tail.Attend) -> CratekitError:
    """The arrival refusal for a landing already planned over what arrived."""
    run = (stop.cause.detail or {}).get("run_id")
    cause = changed.cause
    steps = (
        f"do not answer the landing planned under run {run}: it took what arrived",
        *cause.remediation.steps,
    )
    return rebuilt(
        changed,
        dataclasses.replace(
            cause,
            remediation=dataclasses.replace(cause.remediation, steps=steps),
            detail={**dict(cause.detail or {}), "planned_run": run},
        ),
    )


def _kept(
    cfg, land: Mapping[str, Any], folder: Path, before: staged.Settled | CratekitError
) -> list[dict[str, str]]:
    """Keep what the folder holds as the tail stops, under the go's job (R-1467).

    ``name apply`` renamed every track, so ``keep_tail`` records them by name,
    size and time for a later ``--go`` to read as its own. One that cannot be
    kept is a warning. Not kept when anything arrived while the tail ran, since
    it may have been renamed with the go's own (R-1499).
    """
    from cratekit.label import go

    job = land.get("job")
    if not (isinstance(job, str) and job):
        return []
    try:
        changed = (
            before if isinstance(before, CratekitError) else _arrived(land, folder, (), before)
        )
    except Exception as exc:  # noqa: BLE001 - a queue that fails here is the record lost
        return [_unkept(folder, job, f"the queue could not be read ({type(exc).__name__}: {exc})")]
    if changed is not None:
        return [_unkept(folder, job, tail.changed_said(changed))]
    try:
        with jobs.open_store() as store:
            go.keep_tail(cfg, store, job, folder)
    except Exception as exc:  # noqa: BLE001 - a record lost is a warning, see above
        return [
            {
                "code": UNRECORDED_WARNING,
                "message": (
                    f"what the tail left in {folder} could not be kept for job {job} "
                    f"({type(exc).__name__}: {exc}); a later go under its run reads "
                    f"the tracks its tail renamed as not its own, and names the tail by hand"
                ),
            }
        ]
    return []


def _record(
    ctx: Context,
    land: Mapping[str, Any],
    role_of,
    value: str,
    *,
    what: str,
    lost: str,
) -> list[dict[str, str]]:
    """Record ``value`` under the job's role on the run whose go queued the job (U239).

    A record that cannot be read or saved is a warning, never a refusal.
    """
    job, owner = land.get("job"), land.get("run")
    if not (isinstance(job, str) and job and isinstance(owner, str) and owner):
        return []
    role = role_of(job)
    try:
        if owner == ctx.run.run_id:
            ctx.run.related_runs[role] = value
            return []
        state = gates.load(owner)
        state.related_runs[role] = value
        gates.save(state)
    except Exception as exc:  # noqa: BLE001 - see below
        # Any failure is a warning, since a refusal here would replace the
        # envelope the go ends on.
        return [
            {
                "code": UNRECORDED_WARNING,
                "message": (
                    f"{what} could not be recorded on run {owner}, whose go queued "
                    f"job {job} ({type(exc).__name__}: {exc}); a later go under that "
                    f"run {lost}"
                ),
            }
        ]
    return []


def _attended(
    ctx: Context,
    envelope: Envelope,
    chain: tail.Chain,
    stop: tail.Attend,
    folder: Path,
    landing: Sequence[str],
    warnings: list[Any],
) -> Envelope:
    """The PENDING envelope the go ends on when the landing, or a step, waits for a person."""
    if stop.step == tail.LAND:
        after: Sequence[str] = tail.REKORDBOX_STEPS
    else:
        after = tuple(f"then: {one}" for one in _commands(folder, landing, stop.step)[1:])
    said = tail.attended(chain, stop, after=after)
    summary = "the go " + said.summary
    if stop.step == tail.LAND:
        summary = "the go is downloaded, tagged, analysed and named; " + summary
    pending = PendingHumanAction(
        kind=said.kind,
        id=f"label-sync-{ctx.run.run_id}",
        summary=summary,
        verify_verb=tail.LAND_VERB if stop.step == tail.LAND else ctx.entry.name,
        steps=said.steps,
    )
    return ctx.envelope(
        data=_data(envelope, chain),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=pending,
        warnings=[*warnings, *chain.warnings],
    )


def _with_warnings(envelope: Envelope, chain: tail.Chain) -> dict[str, Any]:
    """The go's report for a refusal, with the chain's warnings, which it has no other place for."""
    data = _data(envelope, chain)
    if chain.warnings:
        data["warnings"] = list(chain.warnings)
    return data


def _ended(
    envelope: Envelope,
    chain: tail.Chain,
    stop: tail.Stop,
    folder: Path,
    landing: Sequence[str],
) -> CratekitError:
    """The refusal a stopped tail ends the go with: the step's own, the way on added.

    The way on is the tail by hand from the step that stopped, since the
    download is kept and a fresh go would take nothing; a ``--go`` under the
    same run reruns the whole tail (U239).
    """
    cause = stop.error.cause
    chain.summary["stopped_at"] = stop.step
    remedy = cause.remediation.remedy
    chain.check(stop.step, "fail", cause.message, remedy=str(remedy) if remedy else None)
    steps = (
        *cause.remediation.steps,
        "the download is kept and nothing was landed; once that is mended, run the "
        "rest of the tail in this order: "
        + "; then ".join(_commands(folder, landing, stop.step)),
    )
    return rebuilt(
        stop.error,
        dataclasses.replace(
            cause,
            remediation=dataclasses.replace(cause.remediation, steps=steps),
            detail={**dict(cause.detail or {}), "label_sync": _with_warnings(envelope, chain)},
        ),
    )


__all__ = ["NAMESPACE", "UNRECORDED_WARNING", "build_sync", "label_sync"]
