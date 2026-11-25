"""Named decisions, and the run state that makes them answerable later (R33).

A decision is data on the run, bound to a gate's name rather than to prompt
order. Gates are declared on the registry entry (``GateSpec``) with a closed
option set; answers come from a named flag or a decision recorded against the
run, and from nowhere else, no blanket affirmative, config key or environment
variable (R34). An unanswered gate raises, and the dispatcher persists the run
so it is resumable. Run records are a declared state file in the config
inventory.
"""

from __future__ import annotations

import json
import shlex
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

from cratekit.cli import output
from cratekit.cli.registry import DB_WRITE_SURFACES, Entry, GateSpec
from cratekit.cli.registry import entry as declared_entry
from cratekit.core import config, processes
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import ExitCode, Remedy

#: The run record's schema version, so a record is never migrated by guessing.
RUN_SCHEMA_VERSION = 1


class DecisionRequired(CratekitError):
    """A gate was reached and nothing had answered it.

    ``context`` is what the verb consulted, carried under ``shown`` so the
    question arrives with its facts. Absent and empty stay different: no
    context leaves no ``shown`` key, since showing nothing and finding nothing
    are two conditions. The values must be JSON already.
    """

    def __init__(
        self,
        spec: GateSpec,
        run_id: str,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        self.spec = spec
        self.run_id = run_id
        self.context = context
        detail: dict[str, Any] = {
            "gate": spec.name,
            "options": list(spec.options),
            "prompt": spec.prompt,
            "explicit": spec.explicit,
            "run_id": run_id,
        }
        if context is not None:
            detail["shown"] = dict(context)
        super().__init__(
            Cause(
                reason="decision-required",
                message=f"the gate {spec.name!r} needs a decision before this run continues",
                remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                scope=Scope.RUN,
                retryable=True,
                origin=("gates",),
                detail=detail,
            )
        )


class DecisionStale(CratekitError):
    """A decision was supplied, but the artifact it was made against moved.

    ``offered`` marks the gate's own stale (R-1334): :meth:`Gates.require` has
    recorded the moved digest as the offer the next answer binds, so the
    refusal carries the open gate's screen over the moved plan, ``context``
    as its ``shown``. A stale a verb raises on its write handle moved no offer,
    so ``offered`` defaults to false.
    """

    def __init__(
        self,
        spec: GateSpec,
        run_id: str,
        expected: str,
        actual: str,
        *,
        pinned: str | None = None,
        offered: bool = False,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        self.spec = spec
        self.run_id = run_id
        message = (
            f"the decision on {spec.name!r} was made against a "
            f"{spec.digest_source} that has since changed"
        )
        if pinned is not None:
            # A pinned fact moved, not the digest (U161), so name both values.
            message = (
                f"the decision on {spec.name!r} was answered with its {pinned} "
                f"{expected!r} on the screen, and this run reads {actual!r}"
            )
        detail: dict[str, Any] = {
            "gate": spec.name,
            "run_id": run_id,
            "expected": expected,
            "actual": actual,
        }
        if pinned is not None:
            detail["pinned"] = pinned
        if offered:
            detail.update(_screen(spec, context))
        super().__init__(
            Cause(
                reason="decision-stale",
                message=message,
                remediation=Remediation(remedy=Remedy.REPLAN_THEN_DECIDE),
                scope=Scope.RUN,
                retryable=True,
                origin=("gates",),
                detail=detail,
            )
        )


def _screen(spec: GateSpec, context: Mapping[str, Any] | None) -> dict[str, Any]:
    """What an open gate puts in front of the person, for a refusal that binds an offer.

    The keys :class:`DecisionRequired` carries, so every refusal reads one shape.
    """
    screen: dict[str, Any] = {
        "options": list(spec.options),
        "prompt": spec.prompt,
        "explicit": spec.explicit,
    }
    if context is not None:
        screen["shown"] = dict(context)
    return screen


class UnknownOption(CratekitError):
    """A decision named an option the gate does not offer.

    ``context`` is the screen of the gate it was raised at (R-1334), passed by
    :meth:`Gates.require` only, so the plan the next answer binds is shown.
    ``crate run decide`` passes none, since it records no offer.
    """

    def __init__(
        self,
        spec: GateSpec,
        option: str,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        detail: dict[str, Any] = {"gate": spec.name, "options": list(spec.options)}
        if context is not None:
            detail["shown"] = dict(context)
        super().__init__(
            Cause(
                reason="decision-required",
                message=(
                    f"{option!r} is not an option for {spec.name!r}; "
                    f"it offers {', '.join(spec.options)}"
                ),
                remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                scope=Scope.RUN,
                retryable=True,
                origin=("gates",),
                detail=detail,
            )
        )


class GateNotReached(CratekitError):
    """A decision named a gate that binds a plan, and the run has not reached it (R-1349).

    Its own reason and no ``answer-decision`` remedy, since both mean an open
    gate and would invite the answer this refuses. The steps say what reaches
    the gate: any gate the run waits at, the run continued, then the answer.
    """

    def __init__(self, state: RunState, spec: GateSpec) -> None:
        command = continue_command(state)
        waiting = state.open_gate
        # No stop is promised (R-1349): a refusal earlier in the run may keep
        # it from the gate, and its report then says why.
        reach = (
            f"continue the run: {command}; it puts {spec.name} and its plan on the "
            f"screen if it reaches it, and its report says why if it does not"
        )
        answer = (
            f"then, once the run shows {spec.name}, answer it: crate run decide "
            f"{state.run_id} {spec.name} <option>"
        )
        if waiting is not None:
            steps: tuple[str, ...] = (
                f"answer the gate the run waits at first: crate run decide "
                f"{state.run_id} {waiting} <option>",
                f"then {reach}",
                answer,
            )
            where = f", and it waits at {waiting!r} first"
        else:
            steps = (reach, answer)
            where = ""
        super().__init__(
            Cause(
                reason="gate-not-reached",
                message=(
                    f"run {state.run_id} has not reached the gate {spec.name!r}, so "
                    f"no plan of it has been shown for an answer to bind to{where}; "
                    f"nothing was recorded"
                ),
                remediation=Remediation(steps=steps),
                scope=Scope.RUN,
                retryable=True,
                origin=("gates",),
                detail={
                    "gate": spec.name,
                    "run_id": state.run_id,
                    "verb": state.verb,
                    "open_gate": waiting,
                    "continue": command,
                },
            )
        )


def continue_command(state: RunState) -> str:
    """The command that continues a kept run with every answer it holds (U211).

    The verb's recorded command line under ``--run``; a run recorded before
    U168 has none, so its words stand with an ellipsis.
    """
    if state.argv is not None:
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
    return f"crate --run {state.run_id} {state.verb.replace('.', ' ')} ..."


@dataclass(frozen=True, slots=True)
class Decision:
    """One recorded answer, with the actor who gave it and when.

    The actor is recorded on every decision (R34), so the audit does not hang
    on a gate being classed explicit.
    """

    option: str
    actor: str
    recorded: str
    digest: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "option": self.option,
            "actor": self.actor,
            "recorded": self.recorded,
            "digest": self.digest,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Decision:
        return cls(
            option=data["option"],
            actor=data.get("actor", "unknown"),
            recorded=data.get("recorded", ""),
            digest=data.get("digest"),
        )


#: What a kept screen was raised as (U961): an open gate's refusal, the gate's
#: own stale over a moved plan, or an option the gate does not offer. Words of
#: their own, never a cause's reason, since a screen is not a refusal.
SCREEN_OPEN = "open"
SCREEN_STALE = "stale"
SCREEN_UNKNOWN_OPTION = "unknown-option"
SCREEN_KINDS: tuple[str, ...] = (SCREEN_OPEN, SCREEN_STALE, SCREEN_UNKNOWN_OPTION)

#: The most a kept screen's ``shown`` takes, in characters of its compact JSON
#: (U961). Every reader that scans the run records reads each one whole, the
#: sibling warning on each gated database verb, ``run retire`` and ``crate
#: status`` among them, so a plan of thousands of items kept whole would slow
#: every gated verb. 64 KiB keeps a few hundred plan items, more than a person
#: reads on one screen, and the verb run again with ``--run`` shows the rest.
SCREEN_LIMIT = 64 * 1024

#: The plan's facts a cut keeps when nothing else fits (U961).
CUT_KEEPS: tuple[str, ...] = ("digest", "count")


@dataclass(frozen=True, slots=True)
class Screen:
    """What a gate put in front of the person when it refused, kept with its run (U961).

    :meth:`Gates.require` keeps it in the same record as the offer it binds,
    so ``crate run show`` in another process shows what the refusal showed.
    ``digest`` is the offer it was raised over, None for a gate offered no
    digest; ``shown`` is the refusal's context as given, None when it carried
    none, held to :data:`SCREEN_LIMIT` by :func:`cut_shown`, with ``cut``
    saying what was left out; ``pins`` are the facts the run binds the gate's
    answer to (U161) as the run held them then.
    """

    kind: str
    prompt: str
    options: tuple[str, ...]
    explicit: bool
    digest: str | None
    shown: dict[str, Any] | None
    pins: dict[str, str]
    saved: str
    cut: dict[str, Any] | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "prompt": self.prompt,
            "options": list(self.options),
            "explicit": self.explicit,
            "digest": self.digest,
            # JSON text, so the order its facts were shown in survives the
            # record's sorted keys and the screen renders as the refusal did.
            "shown": None if self.shown is None else _compact(self.shown),
            "pins": dict(sorted(self.pins.items())),
            "saved": self.saved,
            "cut": self.cut,
        }

    @classmethod
    def from_json(cls, data: Any) -> Screen | None:
        """A kept screen, or None for an entry that is not one, which no reader shows."""
        if not isinstance(data, Mapping):
            return None
        shown = data.get("shown")
        if isinstance(shown, str):
            try:
                shown = json.loads(shown)
            except json.JSONDecodeError:
                return None
        options, pins, cut = data.get("options"), data.get("pins"), data.get("cut")
        if (
            data.get("kind") not in SCREEN_KINDS
            or not isinstance(data.get("prompt"), str)
            or not isinstance(options, list)
            or not all(isinstance(one, str) for one in options)
            or not isinstance(data.get("explicit"), bool)
            or not isinstance(data.get("digest"), (str, type(None)))
            or not isinstance(shown, (dict, type(None)))
            or not isinstance(pins, dict)
            or not isinstance(data.get("saved"), str)
            or not isinstance(cut, (dict, type(None)))
        ):
            return None
        return cls(
            kind=data["kind"],
            prompt=data["prompt"],
            options=tuple(options),
            explicit=data["explicit"],
            digest=data["digest"],
            shown=shown,
            pins={str(key): str(value) for key, value in pins.items()},
            saved=data["saved"],
            cut=cut,
        )


def _compact(document: Any) -> str:
    """One JSON text with no whitespace, the form :data:`SCREEN_LIMIT` is measured in."""
    return json.dumps(document, separators=(",", ":"))


def cut_shown(
    shown: Mapping[str, Any], limit: int = SCREEN_LIMIT
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """``shown`` held to ``limit``, and what was left out, None when nothing was (U961).

    Whole when its compact JSON fits. Otherwise every list among its facts
    keeps its first items, the same number for each and as many as fit, and
    every other fact stays, the plan's digest and count among them; the cut
    names each list it shortened, with how many it kept and left out. When the
    other facts alone pass the limit, only the digest and the count stay, and
    the cut names every fact dropped. A shortened list never reads as whole.
    """
    whole = dict(shown)
    if len(_compact(whole)) <= limit:
        return whole, None
    lists = {name: value for name, value in whole.items() if isinstance(value, list)}

    def keeping(count: int) -> dict[str, Any]:
        return {name: value[:count] if name in lists else value for name, value in whole.items()}

    # The most items each list keeps; keeping the longest list whole is the
    # whole, which does not fit.
    low, high, kept = 0, max((len(value) for value in lists.values()), default=0) - 1, None
    while low <= high:
        middle = (low + high) // 2
        if len(_compact(keeping(middle))) <= limit:
            kept, low = middle, middle + 1
        else:
            high = middle - 1
    if kept is not None:
        shortened = {
            name: {"kept": kept, "left_out": len(value) - kept}
            for name, value in lists.items()
            if len(value) > kept
        }
        return keeping(kept), {"limit": limit, "lists": shortened}
    bare = {name: whole[name] for name in CUT_KEEPS if name in whole}
    if len(_compact(bare)) > limit:
        bare = {}
    return bare, {"limit": limit, "dropped": [name for name in whole if name not in bare]}


@dataclass
class RunState:
    """What survives the process that hit a gate.

    Keyed by a generated ``run_id`` (R19); decisions are keyed by the gate's
    declared name, never its prompt text.
    """

    run_id: str
    verb: str
    created: str
    decisions: dict[str, Decision] = field(default_factory=dict)
    #: gate name -> the digest of the artifact the user was offered, recorded
    #: when the gate refuses, since a later answerer cannot quote it. This is
    #: what makes a stale answer detectable.
    offers: dict[str, str] = field(default_factory=dict)
    #: gate name -> facts shown that the answer binds to outside the digest
    #: (U161), recorded while the gate is open and compared when used, such as
    #: the database file a landing reads.
    pins: dict[str, dict[str, str]] = field(default_factory=dict)
    pending: output.PendingHumanAction | None = None
    open_gate: str | None = None
    #: The verb's path and arguments from its first invocation (U168), without
    #: the global options, for ``run decide --continue``. None before U168.
    argv: tuple[str, ...] | None = None
    #: Other runs this run is bound to, by role (U183), such as the ``sync
    #: all`` pass a ``sync land`` run continues under ``pass_run``.
    related_runs: dict[str, str] = field(default_factory=dict)
    #: gate name -> the screen its last refusal showed (U961), kept beside the
    #: offer it binds and dropped when the gate passes, so ``run show`` can
    #: show a waiting gate without running the verb again.
    screens: dict[str, Screen] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        record = {
            "version": RUN_SCHEMA_VERSION,
            "run_id": self.run_id,
            "verb": self.verb,
            "created": self.created,
            "decisions": {name: d.to_json() for name, d in sorted(self.decisions.items())},
            "offers": dict(sorted(self.offers.items())),
            "pending_human_action": self.pending.to_json() if self.pending else None,
            "open_gate": self.open_gate,
        }
        # The later keys only when set, so an older record keeps its shape.
        if self.pins:
            record["pins"] = {name: dict(sorted(one.items())) for name, one in sorted(self.pins.items())}
        if self.argv is not None:
            record["argv"] = list(self.argv)
        if self.related_runs:
            record["related_runs"] = dict(sorted(self.related_runs.items()))
        if self.screens:
            record["screens"] = {name: one.to_json() for name, one in sorted(self.screens.items())}
        return record

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> RunState:
        version = data.get("version")
        if version != RUN_SCHEMA_VERSION:
            raise CratekitError(
                Cause(
                    reason="internal-error",
                    message=(
                        f"run record schema {version!r} is not {RUN_SCHEMA_VERSION}; "
                        f"refusing to guess what wrote it"
                    ),
                    remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                    origin=("gates",),
                )
            )
        pending = data.get("pending_human_action")
        return cls(
            run_id=data["run_id"],
            verb=data["verb"],
            created=data["created"],
            decisions={
                name: Decision.from_json(value)
                for name, value in (data.get("decisions") or {}).items()
            },
            offers=dict(data.get("offers") or {}),
            pins={
                name: {str(key): str(value) for key, value in (one or {}).items()}
                for name, one in (data.get("pins") or {}).items()
            },
            pending=output.PendingHumanAction.from_json(pending) if pending else None,
            open_gate=data.get("open_gate"),
            argv=(
                tuple(str(one) for one in data["argv"])
                if isinstance(data.get("argv"), list)
                else None
            ),
            related_runs=(
                {str(role): str(run) for role, run in data["related_runs"].items()}
                if isinstance(data.get("related_runs"), dict)
                else {}
            ),
            screens=_screens_from(data.get("screens")),
        )


def _screens_from(raw: Any) -> dict[str, Screen]:
    """The kept screens a record holds (U961); an entry that is not one is left out.

    A record from before U961 has none. :func:`waiting` says a gate's screen
    cannot be shown rather than reading its absence as no gate.
    """
    if not isinstance(raw, dict):
        return {}
    kept = {str(name): Screen.from_json(one) for name, one in raw.items()}
    return {name: one for name, one in kept.items() if one is not None}


def run_dir() -> Path:
    """Where run records live, resolved through the declared state inventory."""
    return config.state_path("run_state")


def run_path(run_id: str) -> Path:
    """One run's record. The identifier is generated, so it needs no escaping."""
    return run_dir() / f"{run_id}.json"


def save(state: RunState) -> Path:
    """Persist a run record atomically, owner-readable only.

    Atomic, since a torn record is a run that cannot be resumed.
    """
    path = run_path(state.run_id)
    config.atomic_write_bytes(
        json.dumps(state.to_json(), indent=2, sort_keys=True).encode() + b"\n", path
    )
    return path


def load(run_id: str) -> RunState:
    """Read a run record, or refuse naming the run."""
    path = run_path(run_id)
    try:
        raw = json.loads(path.read_text())
    except FileNotFoundError:
        raise CratekitError(
            Cause(
                reason="decision-unknown-gate",
                message=f"no run recorded with the identifier {run_id!r}",
                remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                origin=("gates",),
                detail={"run_id": run_id},
            )
        ) from None
    except json.JSONDecodeError as exc:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=f"the run record for {run_id!r} is not readable JSON",
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("gates",),
                detail={"run_id": run_id, "error": str(exc)},
            )
        ) from None
    # A record must be an object (U183), or ``from_json`` raises past every
    # reader that catches this module's refusals.
    if not isinstance(raw, dict):
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=f"the run record for {run_id!r} is not a JSON object",
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("gates",),
                detail={"run_id": run_id, "found": type(raw).__name__},
            )
        )
    return RunState.from_json(raw)


#: The keys :func:`shown_plan` fills from the plan; a fact under one is refused.
SHOWN_PLAN_KEYS = ("digest", "count", "items")


def shown_plan(plan: Mapping[str, Any], facts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """What a digest bound gate puts in front of the person (R-693).

    The caller's facts, then the plan's digest, its count and every item the
    digest covers, so the screen is the plan approved. There is no bound,
    since a shortened list would approve items nobody saw. A fact named as
    one of ``SHOWN_PLAN_KEYS`` is refused rather than overwritten. The values
    must be JSON already.
    """
    named = dict(facts or {})
    taken = sorted(set(named) & set(SHOWN_PLAN_KEYS))
    if taken:
        raise ValueError(f"shown_plan() fills {taken} from the plan; name the fact differently")
    items = list(plan["items"])
    return {**named, "digest": plan["digest"], "count": len(items), "items": items}


def parse_decision_flags(values: list[str]) -> dict[str, str]:
    """Turn repeated ``gate=option`` arguments into a mapping.

    A malformed pair is rejected, since a dropped decision stops at a gate the
    user believes answered.
    """
    supplied: dict[str, str] = {}
    for raw in values:
        name, sep, option = raw.partition("=")
        if not sep or not name or not option:
            raise CratekitError(
                Cause(
                    reason="decision-unknown-gate",
                    message=f"{raw!r} is not a decision; the form is <gate>=<option>",
                    remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                    origin=("gates",),
                )
            )
        supplied[name] = option
    return supplied


class Gates:
    """Resolves declared gates for one run, from named sources only.

    Precedence, highest first:

    1. a decision supplied by name on this invocation,
    2. a decision recorded against the run by a separate act,
    3. a review-queue verdict, for gates whose options come from a review item.

    Source 3 lands with the review queue (U11). There is no fourth source: a
    blanket flag, config key or environment variable would answer every gate
    at once, which R34 forbids.
    """

    def __init__(
        self,
        *,
        state: RunState,
        supplied: Mapping[str, str] | None = None,
        actor: str = "cli",
    ) -> None:
        self.state = state
        self.supplied = dict(supplied or {})
        self.actor = actor
        self.reached: list[str] = []

    def require(
        self,
        spec: GateSpec,
        *,
        digest: str | None = None,
        context: Mapping[str, Any] | None = None,
        plan: Mapping[str, Any] | None = None,
        pinned: Mapping[str, str] | None = None,
    ) -> str:
        """Return the chosen option, or raise so the CLI can exit resumably.

        ``pinned`` is what the answer binds to outside the digest (U161),
        recorded while the gate is open; a recorded answer whose run pinned
        other values is refused stale, naming the fact.

        ``context`` rides through to every refusal unchanged, so what a person
        sees does not depend on whether they typed a flag. It is display only.

        ``plan`` carries ``digest`` and ``items`` on one mapping (R-693), so
        the screen and the binding are one plan. Passing both ``digest`` and
        ``plan`` is refused.
        """
        if plan is not None:
            if digest is not None:
                raise TypeError("require() takes a digest or a plan, not both")
            digest = plan["digest"]
            context = shown_plan(plan, context)
        self.reached.append(spec.name)

        recorded = self.state.decisions.get(spec.name)
        inline = self.supplied.get(spec.name)
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest
        pins = {str(key): str(value) for key, value in (pinned or {}).items()}
        if recorded is None and pins:
            # Recorded while the gate is open, so ``run decide`` answers over
            # the facts this process showed; never replaced once answered.
            self.state.pins[spec.name] = pins

        if inline is not None and spec.explicit:
            # R34: an explicit gate is answered only by a separate recorded act,
            # never inline, and an inline flag is refused whatever the run holds,
            # so it can never overturn a recorded answer (U49). The gate is
            # marked open only when it holds no answer, so the run stays
            # resumable without reading as both answered and waiting.
            if recorded is None:
                self.state.open_gate = spec.name
            self._keep(spec, SCREEN_OPEN, digest, context)
            raise DecisionRequired(spec, self.state.run_id, context)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
        if chosen is None:
            self.state.open_gate = spec.name
            self._keep(spec, SCREEN_OPEN, digest, context)
            raise DecisionRequired(spec, self.state.run_id, context)
        if chosen not in spec.options:
            self._keep(spec, SCREEN_UNKNOWN_OPTION, digest, context)
            raise UnknownOption(spec, chosen, context)

        if spec.digest_source is not None and digest is not None:
            against = recorded.digest if recorded is not None else None
            if against is not None and against != digest:
                # The moved plan is on the refusal (R-1334), since the next
                # answer binds the offer just recorded.
                self._keep(spec, SCREEN_STALE, digest, context)
                raise DecisionStale(
                    spec, self.state.run_id, against, digest, offered=True, context=context
                )

        if recorded is not None and inline is None:
            held = self.state.pins.get(spec.name, {})
            for key in sorted(set(held) | set(pins)):
                if held.get(key) != pins.get(key):
                    raise DecisionStale(
                        spec,
                        self.state.run_id,
                        held.get(key, ""),
                        pins.get(key, ""),
                        pinned=key,
                    )

        if recorded is None:
            self.state.decisions[spec.name] = Decision(
                option=chosen,
                actor=self.actor,
                recorded=output.timestamp(),
                digest=digest,
            )
        # Passed: the screen it waited on is history, and the record keeps none.
        self.state.screens.pop(spec.name, None)
        self.state.open_gate = None
        return chosen

    def _keep(
        self,
        spec: GateSpec,
        kind: str,
        digest: str | None,
        context: Mapping[str, Any] | None,
    ) -> None:
        """Keep the screen this refusal shows on the run, beside the offer it binds (U961).

        The one path every gate's refusal takes, so a screen is never kept
        apart from its offer: the dispatcher's save writes both in one record,
        and a later refusal at the gate replaces the screen with its offer.
        The digest is the offer :meth:`require` recorded, None when it
        recorded none.
        """
        shown, cut = (None, None)
        if context is not None:
            # Through JSON, as the refusal's envelope is, so the record holds
            # what a reader of it gets back; order kept.
            shown, cut = cut_shown(json.loads(json.dumps(dict(context), default=str)))
        self.state.screens[spec.name] = Screen(
            kind=kind,
            prompt=spec.prompt,
            options=tuple(spec.options),
            explicit=spec.explicit,
            digest=digest if spec.digest_source is not None else None,
            shown=shown,
            pins=dict(self.state.pins.get(spec.name, {})),
            saved=output.timestamp(),
            cut=cut,
        )

    def hand_off(
        self,
        spec: GateSpec,
        *,
        verb: str,
        gate: str,
        part: tuple[Any, str] | None = None,
    ) -> str:
        """Carry the answer recorded on ``spec`` to a new run owned by ``verb``.

        A queued job of another verb needs a run that verb owns, since the
        dispatcher refuses a ``--run`` of a different verb. This copies an
        answer and never supplies one: ``spec`` must hold a recorded decision
        with a digest, the copy keeps its actor, time and digest, and the target
        gate must offer the option and compare a digest.

        ``part`` is for one answer over several plans (U112): the document the
        recorded digest covers and one step's digest inside it, which is handed
        on only when the document digests to the answer's digest.

        Returns the new run's identifier, saved before returning.
        """
        recorded = self.state.decisions.get(spec.name)
        if recorded is None or recorded.digest is None:
            raise CratekitError(
                Cause(
                    reason="internal-error",
                    message=(
                        f"{spec.name!r} holds no recorded decision with a digest, "
                        f"so there is no answer to carry to {verb}"
                    ),
                    remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                    origin=("gates",),
                    detail={"gate": spec.name, "verb": verb},
                )
            )
        target = next((g for g in declared_entry(verb).gates if g.name == gate), None)
        if (
            target is None
            or recorded.option not in target.options
            or target.digest_source is None
        ):
            raise CratekitError(
                Cause(
                    reason="internal-error",
                    message=(
                        f"{verb} declares no digest-compared gate {gate!r} offering "
                        f"{recorded.option!r}, so the answer on {spec.name!r} "
                        f"cannot stand for it"
                    ),
                    remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                    origin=("gates",),
                    detail={"gate": spec.name, "verb": verb, "target": gate},
                )
            )
        digest = recorded.digest
        if part is not None:
            document, digest = part
            if output.digest_of(document) != recorded.digest or digest not in _strings(document):
                raise CratekitError(
                    Cause(
                        reason="internal-error",
                        message=(
                            f"the answer on {spec.name!r} was not given over a plan "
                            f"holding the digest {digest!r}, so it cannot stand for "
                            f"{verb}'s gate {gate!r}"
                        ),
                        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                        origin=("gates",),
                        detail={"gate": spec.name, "verb": verb, "target": gate},
                    )
                )
        handed = RunState(
            run_id=output.new_run_id(),
            verb=verb,
            created=output.timestamp(),
            decisions={
                gate: Decision(
                    option=recorded.option,
                    actor=recorded.actor,
                    recorded=recorded.recorded,
                    digest=digest,
                )
            },
            offers={gate: digest},
        )
        save(handed)
        return handed.run_id


def _strings(document: Any) -> set[str]:
    """Every string anywhere in a JSON shaped document, for ``hand_off``'s part."""
    found: set[str] = set()
    pending = [document]
    while pending:
        value = pending.pop()
        if isinstance(value, str):
            found.add(value)
        elif isinstance(value, Mapping):
            pending.extend(value.values())
        elif isinstance(value, (list, tuple)):
            pending.extend(value)
    return found


def record(state: RunState, spec: GateSpec, option: str, *, actor: str) -> None:
    """Write a decision into a run record, validating it against the gate.

    The digest comes from what the run offered, never from the caller. So a
    gate that binds a plan is answered only once its run reached it (R-1349),
    meaning it holds the offer, holds the gate open, or holds an answer;
    otherwise nothing is written.
    """
    if option not in spec.options:
        raise UnknownOption(spec, option)
    if (
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
    state.decisions[spec.name] = Decision(
        option=option,
        actor=actor,
        recorded=output.timestamp(),
        digest=state.offers.get(spec.name),
    )
    # Answered, the screen is history (U961): run records are never pruned,
    # so an answer or a retirement leaves the record as small as it was.
    state.screens.pop(spec.name, None)
    if state.open_gate == spec.name:
        state.open_gate = None


@dataclass(frozen=True, slots=True)
class Waiting:
    """The gate a run waits at (U961), with its kept screen or why none is shown."""

    gate: str
    screen: Screen | None = None
    missing: str | None = None


#: Before any kept screen, so a screen with an unreadable time sorts first.
_EARLIEST = datetime.min.replace(tzinfo=timezone.utc)


def waiting(state: RunState) -> Waiting | None:
    """The gate ``state`` waits at for an answer, and the screen it was offered (U961).

    A gate waits when it is the run's open gate, when the run offered it a
    plan and holds no answer, or when its answer binds another plan than the
    one offered now, or an option the screen does not offer, since the next
    resume refuses it. A kept screen is shown only while it is current, its
    digest the run's offer for its gate and its pins the run's, so a screen
    left behind a moved offer never reads as the gate's. Of the waiting gates
    with a current screen, the latest kept is named, the refusal the run last
    ended on; otherwise the open gate, or else the first waiting gate by name,
    with ``missing`` saying why no screen is shown. None when nothing waits.
    """
    shown = [
        (_instant(screen.saved) or _EARLIEST, name, screen)
        for name, screen in state.screens.items()
        if _current(state, name, screen) and _waits(state, name, screen)
    ]
    if shown:
        _, name, screen = max(shown, key=lambda one: (one[0], one[1]))
        return Waiting(name, screen=screen)
    named = [state.open_gate] if state.open_gate is not None else []
    named += [
        name
        for name in sorted(set(state.offers) | set(state.screens))
        if name != state.open_gate and _waits(state, name, state.screens.get(name))
    ]
    if not named:
        return None
    gate = named[0]
    if gate in state.screens:
        why = f"the screen kept for {gate} no longer matches the plan and facts the run offers it now"
    else:
        why = (
            f"no screen of {gate} that can be shown is kept on this run: the gate opened "
            f"before a run kept its gate's screen, or the kept one could not be read"
        )
    return Waiting(gate, missing=why)


def _current(state: RunState, gate: str, screen: Screen) -> bool:
    """Whether ``screen`` is still what an answer on ``gate`` binds (U961)."""
    return screen.digest == state.offers.get(gate) and screen.pins == state.pins.get(gate, {})


def _waits(state: RunState, gate: str, screen: Screen | None) -> bool:
    """Whether ``gate`` waits for an answer on this run (U961); see :func:`waiting`."""
    if gate == state.open_gate:
        return True
    answer = state.decisions.get(gate)
    offer = state.offers.get(gate)
    if answer is None:
        return screen is not None or offer is not None
    if screen is not None and answer.option not in screen.options:
        return True
    return answer.digest is not None and offer is not None and answer.digest != offer


def blocked_by(state: RunState, verb: str) -> Cause | None:
    """The cause refusing ``verb`` while this run has an unverified pending action.

    What makes ``pending_human_action`` binding rather than advisory.
    """
    pending = state.pending
    if pending is None or verb not in pending.blocks:
        return None
    return Cause(
        reason="blocked-by-pending-action",
        message=(
            f"{verb} is blocked until the outstanding action on run "
            f"{state.run_id} is completed and verified"
        ),
        remediation=Remediation(
            remedy=Remedy.COMPLETE_PENDING_ACTION, steps=tuple(pending.steps)
        ),
        scope=Scope.RUN,
        retryable=True,
        origin=("gates",),
        detail={
            "run_id": state.run_id,
            "pending_id": pending.id,
            "verify_verb": pending.verify_verb,
        },
    )


def new_run(entry: Entry, run_id: str | None = None) -> RunState:
    """Start a run record for one verb."""
    return RunState(
        run_id=run_id or output.new_run_id(),
        verb=entry.name,
        created=output.timestamp(),
    )


# ---------------------------------------------------------------------------
# Open gates nobody will answer (U170)
# ---------------------------------------------------------------------------

#: The only option an old open gate is retired with: a retirement answers no.
RETIRE_OPTION = "abort"


@dataclass(frozen=True, slots=True)
class OldGate:
    """One open gate that has sat idle for longer than a threshold (U170).

    ``idle_since`` is the later of ``created`` and the record's last write,
    since a resume saves the run. ``kept`` is None when the gate can be
    retired, otherwise why not, for a gate its verb no longer declares or one
    with no ``abort``.
    """

    run_id: str
    verb: str
    gate: str
    created: str
    idle_since: str
    kept: str | None = None

    @property
    def retirable(self) -> bool:
        return self.kept is None

    def item(self) -> dict[str, str]:
        """What a retirement's confirm shows and digests for this gate."""
        return {
            "run_id": self.run_id,
            "verb": self.verb,
            "gate": self.gate,
            "idle_since": self.idle_since,
        }


def _instant(stamp: str) -> datetime | None:
    try:
        moment = datetime.fromisoformat(stamp)
    except (TypeError, ValueError):
        return None
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)


def idle_since(state: RunState, path: Path) -> datetime:
    """When this run was last touched: its start, or its record's last write if later.

    An unreadable file time counts as now, so an unmeasured gate is never old.
    """
    try:
        written = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except OSError:
        return datetime.now(timezone.utc)
    started = _instant(state.created)
    return written if started is None else max(started, written)


def old_gate(
    state: RunState, path: Path, *, older_than: timedelta, now: datetime
) -> OldGate | None:
    """This run's open gate when it has been idle for longer than ``older_than``.

    The one predicate ``crate status`` and ``crate run retire`` share, so they
    name one set. None for a run with no open gate or one touched recently.
    """
    if state.open_gate is None:
        return None
    since = idle_since(state, path)
    if now - since <= older_than:
        return None
    try:
        owner = declared_entry(state.verb)
    except KeyError:
        owner = None
    spec = (
        next((g for g in owner.gates if g.name == state.open_gate), None)
        if owner is not None
        else None
    )
    if owner is None:
        kept: str | None = f"{state.verb} is not a verb in this build"
    elif spec is None:
        kept = f"{state.verb} no longer declares the gate {state.open_gate}"
    elif RETIRE_OPTION not in spec.options:
        kept = f"{state.open_gate} offers {', '.join(spec.options)}, and no {RETIRE_OPTION}"
    else:
        kept = None
    return OldGate(
        run_id=state.run_id,
        verb=state.verb,
        gate=state.open_gate,
        created=state.created,
        idle_since=since.replace(microsecond=0).isoformat(),
        kept=kept,
    )


# ---------------------------------------------------------------------------
# Another run of the same verb at its gate (U186)
# ---------------------------------------------------------------------------

#: How long a recorded answer on another run stays worth naming (U186).
SIBLING_WINDOW = timedelta(hours=12)

#: The warning code a run carries when another run of its verb holds an open
#: gate or answered one within :data:`SIBLING_WINDOW` (U186).
SIBLING_RUN = "gate-sibling-run"


@dataclass(frozen=True, slots=True)
class Sibling:
    """Another run of the same verb that a second plan should know about (U186).

    Either ``gate`` names its open gate and ``at`` is :func:`idle_since`, or
    it answered within the window and ``gate`` is None. ``answers`` holds
    every answer inside the window, oldest first, even with a later gate open,
    since an approved plan stays approved.
    """

    run_id: str
    verb: str
    gate: str | None
    at: str
    answers: tuple[tuple[str, Decision], ...] = ()

    @property
    def open(self) -> bool:
        return self.gate is not None

    def message(self) -> str:
        """The one line naming this run, its actor, its option and the time."""
        if self.gate is not None and not self.answers:
            return (
                f"another run of {self.verb}, {self.run_id}, holds the gate {self.gate} "
                f"open since {self.at}, unanswered; approving both would race two "
                f"writes over one library"
            )
        gate, latest = self.answers[-1]
        if self.gate is not None:
            # An approved plan stopped again is named by its answer and its
            # open gate, never as unanswered.
            return (
                f"another run of {self.verb}, {self.run_id}, answered {gate} "
                f"{latest.option} as {latest.actor} at "
                f"{latest.recorded or 'an unrecorded time'} and holds the gate "
                f"{self.gate} open since {self.at}; approving both would race two "
                f"writes over one library"
            )
        return (
            f"another run of {self.verb}, {self.run_id}, answered {gate} "
            f"{latest.option} as {latest.actor} at {latest.recorded or 'an unrecorded time'}; a plan read "
            f"after or during its write differs from the one it answered"
        )

    def warning(self) -> dict[str, str]:
        return {"code": SIBLING_RUN, "message": self.message()}


def siblings(
    verb: str,
    *,
    exclude: str,
    now: datetime | None = None,
    within: timedelta = SIBLING_WINDOW,
) -> tuple[list[Sibling], list[str]]:
    """Every other run of ``verb`` with an open gate or an answer inside ``within``.

    Read only, and the one reader the dispatcher and ``run decide`` share;
    the warning informs and guards nothing. ``exclude`` is the asking run. The
    second value names every unreadable record, so a caller never reads the
    gap as no sibling. An answer with an unreadable time counts as inside.
    """
    moment = now or datetime.now(timezone.utc)
    try:
        records = sorted(run_dir().glob("*.json"))
    except OSError:
        records = []
    found: list[Sibling] = []
    unreadable: list[str] = []
    for path in records:
        # By file name, so the asking run is never read or named unreadable.
        if path.stem == exclude:
            continue
        try:
            state = load(path.stem)
        except Exception:  # noqa: BLE001 - an unread record is said, never skipped
            unreadable.append(path.stem)
            continue
        if state.verb != verb:
            continue
        recent: list[tuple[datetime, str, Decision]] = []
        for name, decision in state.decisions.items():
            when = _instant(decision.recorded)
            if when is None or moment - when <= within:
                recent.append((when or moment, name, decision))
        recent.sort(key=lambda one: (one[0], one[1]))
        answers = tuple((name, decision) for _, name, decision in recent)
        if state.open_gate is not None:
            since = idle_since(state, path).replace(microsecond=0).isoformat()
            found.append(
                Sibling(
                    run_id=state.run_id, verb=verb, gate=state.open_gate, at=since, answers=answers
                )
            )
        elif answers:
            found.append(
                Sibling(run_id=state.run_id, verb=verb, gate=None, at=answers[-1][1].recorded, answers=answers)
            )
    return found, unreadable


def sibling_warnings(found: list[Sibling], unreadable: list[str], verb: str) -> list[dict[str, str]]:
    """One warning per sibling, and one more when records could not be read (U186)."""
    said = [one.warning() for one in found]
    if unreadable:
        records_word = "record" if len(unreadable) == 1 else "records"
        said.append(
            {
                "code": SIBLING_RUN,
                "message": (
                    f"{len(unreadable)} run {records_word} could not be read "
                    f"({', '.join(unreadable)}), so a run of {verb} among them "
                    f"would not be named here"
                ),
            }
        )
    return said


def writes_the_database(verb: str) -> bool:
    """Whether ``verb`` declares a database writing surface, the scope of U186's warning."""
    try:
        owner = declared_entry(verb)
    except KeyError:
        return False
    return bool(owner.writes & DB_WRITE_SURFACES)


#: Codes this module raises, listed so the dispatcher's mapping is checkable.
GATE_CODES: tuple[ExitCode, ...] = (ExitCode.DECISION_REQUIRED, ExitCode.DECISION_STALE)

#: Refusals outside the gates that keep their run (U211): saved with its
#: answers, ``resumable`` and ``blocked``, with the command that continues it.
#: Only a cause that clears on its own, raised before the step it guards,
#: belongs here. A moved plan is still asked again, every gate being digest
#: bound.
KEPT_RUN_REASONS: tuple[str, ...] = (processes.UNCONFIRMED,)


__all__ = [
    "GATE_CODES",
    "KEPT_RUN_REASONS",
    "RETIRE_OPTION",
    "RUN_SCHEMA_VERSION",
    "SCREEN_KINDS",
    "SCREEN_LIMIT",
    "SCREEN_OPEN",
    "SCREEN_STALE",
    "SCREEN_UNKNOWN_OPTION",
    "SIBLING_RUN",
    "SIBLING_WINDOW",
    "Decision",
    "DecisionRequired",
    "DecisionStale",
    "Gates",
    "OldGate",
    "RunState",
    "Screen",
    "Sibling",
    "UnknownOption",
    "blocked_by",
    "cut_shown",
    "idle_since",
    "load",
    "new_run",
    "old_gate",
    "parse_decision_flags",
    "record",
    "run_dir",
    "run_path",
    "save",
    "shown_plan",
    "SHOWN_PLAN_KEYS",
    "sibling_warnings",
    "siblings",
    "waiting",
    "Waiting",
    "writes_the_database",
]
