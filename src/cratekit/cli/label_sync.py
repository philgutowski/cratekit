"""``crate label sync``, its go taken on through the tail to the landing's gate (U190).

The attended Defected label sync of 2026-10-31 answered the gate, said go, and
the go downloaded ten tracks and printed five commands to type in order: ``tag
folder``, ``analyze run``, ``analyze restamp``, ``name apply`` and ``intake
land`` with the manifest and the pass, three of which queue a job a second
command has to drive. A sync pass already ran that chain in one verb, ``crate
sync land`` (U152). Now the go does too.

WHY THIS MODULE AND NOT THE GO. The go, :mod:`cratekit.label.go`, is ranked a
feature module, and the chain runs each step through the real dispatcher, which
is the CLI layer's: ``tests/test_layering.py`` refuses a feature module that
reaches up for it, at module scope or inside a function. So the ``label.sync``
registry entry names this module. Its builder is the verb's own,
:func:`cratekit.label.sync_cli.build_sync`, its handler runs the verb's own
handler unchanged, and only then, when the go's report names a tail
(:data:`cratekit.label.go.LAND_KEY`), runs it here through
:mod:`cratekit.cli.tail`, the one chain ``sync land`` runs, so the two verbs
answer every question of the tail the same way by construction.

WHAT IT ENDS ON. The landing is planned by ``intake land`` itself with the go's
manifest and pass, and stops at its explicit gate on its own run, so the verb
ends PENDING naming that run, the two commands that answer and apply it as the
session, and the rekordbox visit after. A tail step that does not succeed ends
the verb there with the step's own refusal, the go's report in its detail and
the rest of the tail named as the way on, so nothing is landed over files the
tail did not finish. The download is kept either way, and the answers it took
are settled, so a second go would not take them again: the tail is run on by
hand from the step that stopped.

A GO THAT NAMES NO TAIL IS RETURNED AS IT WAS. An abort, a go that listed
nothing, one that downloaded nothing, and every walk or question that never
reached the go are the verb's own envelopes, untouched.
"""

from __future__ import annotations

import dataclasses
import shlex
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import tail
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.core.cause import CratekitError, Outcome, rebuilt
from cratekit.core.exit_codes import ExitCode
from cratekit.label import go, sync_cli

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.label_sync",)

#: The key every check the chain adds to the go's report carries, before its step.
NAMESPACE = "label.sync.go"


def build_sync(parser, entry) -> None:
    """The verb's own arguments, with this module's handler in front of its own."""
    sync_cli.build_sync(parser, entry)
    parser.set_defaults(_handler=label_sync)


def _land_of(envelope: Envelope) -> Mapping[str, Any] | None:
    """The tail the go's report names, or None when it names none."""
    summary = envelope.data.get("summary")
    report = summary.get("go") if isinstance(summary, Mapping) else None
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
    if not isinstance(land, Mapping):
        return None
    if not all(isinstance(land.get(key), str) and land.get(key) for key in ("folder", "pass")):
        return None
    return land


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

    ``name apply`` without its confirm answered, as the go has always named it:
    a person running it by hand reads its plan first.
    """
    words = {one: ["crate", *argv, str(folder)] for one, _verb, argv in tail.TAIL}
    # NO PASS (U172, review round 2): a label go's pass names its landing, and
    # no account playlist asked for its tracks, so none votes in the guess.
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
    envelope = sync_cli.label_sync(ctx)
    land = _land_of(envelope)
    if land is None:
        return envelope
    cfg = tail.load_config(_ORIGIN)
    chain = _chain(ctx)
    folder = Path(str(land["folder"])).expanduser().absolute()
    landing = _landing_args(land)
    warnings = [*envelope.warnings]
    try:
        tail.run(chain, folder, cfg, landing)
    except tail.Done as done:
        chain.summary["stopped_at"] = done.step
    except tail.Attend as stop:
        return _attended(ctx, envelope, chain, stop, folder, landing, warnings)
    except tail.Stop as stop:
        raise _ended(envelope, chain, stop, folder, landing) from None
    return ctx.envelope(
        data=_data(envelope, chain),
        outcome=envelope.outcome,
        warnings=[*warnings, *chain.warnings],
    )


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


def _ended(
    envelope: Envelope,
    chain: tail.Chain,
    stop: tail.Stop,
    folder: Path,
    landing: Sequence[str],
) -> CratekitError:
    """The refusal a stopped tail ends the go with: the step's own, the way on added.

    THE WAY ON IS THE TAIL BY HAND, FROM THE STEP THAT STOPPED. The download is
    kept and its answers are settled, so ``label sync --go`` again would take
    nothing, and the go's report, in the detail, says what it downloaded.
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
            detail={**dict(cause.detail or {}), "label_sync": _data(envelope, chain)},
        ),
    )


__all__ = ["NAMESPACE", "build_sync", "label_sync"]
