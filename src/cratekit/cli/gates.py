"""Named decisions, and the run state that makes them answerable later (R33).

The source system has the right idea and the wrong seam. Its orchestrator takes
a ``--decision`` flag, builds a fake input function that returns that answer
once, and threads it into whatever asks first. Four things are wrong with it,
and all four are visible in the shipped code:

1. **The answer binds to prompt ORDER, not to a question.** Insert a prompt
   anywhere upstream and the decision silently answers the new question.
2. **The seam already leaks.** One call site omits the injected function
   entirely, so a retry prompt falls back to the built-in input and sits outside
   the non-interactive contract the docstring claims is complete.
3. **Three prompts have no seam at all**, guarded only by a check for a
   terminal. A terminal check is a behaviour change under a pipe, not an absence
   of a read.
4. **It makes the property untestable in substance.** Because every consumer
   resolves its input function at call time, "no verb reads standard input"
   becomes a whole-call-graph property that can only be asserted about one exact
   run, never about a function.

So a decision here is DATA ON THE RUN, not an answer to a prompt:

* Gates are declared statically on the registry entry (``GateSpec``), with a
  stable name and a closed option set.
* Answers arrive from a named flag, or from a decision recorded against the run
  by a separate act, and from nowhere else. No blanket affirmative, no config
  key, no environment variable (R34).
* An unanswered gate RAISES. The verb catches nothing; the CLI dispatcher
  persists the run so it is resumable, puts the gate and its options in the
  envelope, and exits with the documented code.

Layer note: CLI. It resolves state paths through the config inventory rather
than composing its own, so the run record is a declared state file with a root
somebody decided on, not a directory this module invented.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from cratekit.cli import output
from cratekit.cli.registry import Entry, GateSpec
from cratekit.cli.registry import entry as declared_entry
from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import ExitCode, Remedy

#: The run record's own schema version. The source system versions exactly one
#: of its twenty-one state files, and every unversioned one is a file that
#: cannot be migrated without guessing what wrote it.
RUN_SCHEMA_VERSION = 1


class DecisionRequired(CratekitError):
    """A gate was reached and nothing had answered it.

    ``context`` is WHAT THE VERB CONSULTED before it asked, carried through to
    the refusal under ``shown`` so the question arrives with the facts it was
    asked over. A prompt string is fixed at declaration and cannot name a backup
    age or a lock holder, and a verb that built its own ``decision-required``
    cause to say so would skip :attr:`RunState.open_gate` and the run record the
    dispatcher saves on the way out, which is the thing that makes a refusal
    resumable rather than one a person answers by starting over.

    ABSENT AND EMPTY STAY DIFFERENT. A caller that passes nothing leaves no
    ``shown`` key at all rather than an empty mapping, because "this verb shows
    nothing here" and "this verb looked and found nothing" are two conditions,
    and :mod:`cratekit.core.backup_facts` argues at length that collapsing them
    is how a person is told the wrong thing about their own library.

    The values must be JSON already. The envelope serializes this detail, so a
    caller hands over ``holder.to_json()`` rather than the frozen dataclass.
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
    """A decision was supplied, but the artifact it was made against moved."""

    def __init__(self, spec: GateSpec, run_id: str, expected: str, actual: str) -> None:
        self.spec = spec
        self.run_id = run_id
        super().__init__(
            Cause(
                reason="decision-stale",
                message=(
                    f"the decision on {spec.name!r} was made against a "
                    f"{spec.digest_source} that has since changed"
                ),
                remediation=Remediation(remedy=Remedy.REPLAN_THEN_DECIDE),
                scope=Scope.RUN,
                retryable=True,
                origin=("gates",),
                detail={
                    "gate": spec.name,
                    "run_id": run_id,
                    "expected": expected,
                    "actual": actual,
                },
            )
        )


class UnknownOption(CratekitError):
    """A decision named an option the gate does not offer."""

    def __init__(self, spec: GateSpec, option: str) -> None:
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
                detail={"gate": spec.name, "options": list(spec.options)},
            )
        )


@dataclass(frozen=True, slots=True)
class Decision:
    """One recorded answer, with the actor who gave it and when.

    R34 requires a write session to record WHICH ACTOR asserted each explicit
    decision. Recording the actor on every decision rather than only the explicit
    ones costs one field and means the audit does not depend on somebody having
    classified the gate correctly first.
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


@dataclass
class RunState:
    """What survives the process that hit a gate.

    Keyed by ``run_id``, which is a generated identifier, never a display name
    (R19). Decisions are keyed by GATE NAME, which is a stable identifier
    declared in the registry and equally not a display name: the prompt text is
    carried separately and exists only to be rendered.
    """

    run_id: str
    verb: str
    created: str
    decisions: dict[str, Decision] = field(default_factory=dict)
    #: gate name -> the digest of the artifact the user was OFFERED.
    #:
    #: Recorded when the gate refuses, not when it is answered, because the
    #: person answering from another process never sees the artifact and cannot
    #: be asked to quote its identity. This is what makes staleness detectable
    #: at all: without it, an answer given yesterday silently applies to a plan
    #: regathered today, which is the "approve one plan, run a wider one"
    #: failure the source system's digest check exists to prevent.
    offers: dict[str, str] = field(default_factory=dict)
    pending: output.PendingHumanAction | None = None
    open_gate: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "version": RUN_SCHEMA_VERSION,
            "run_id": self.run_id,
            "verb": self.verb,
            "created": self.created,
            "decisions": {name: d.to_json() for name, d in sorted(self.decisions.items())},
            "offers": dict(sorted(self.offers.items())),
            "pending_human_action": self.pending.to_json() if self.pending else None,
            "open_gate": self.open_gate,
        }

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
            pending=output.PendingHumanAction.from_json(pending) if pending else None,
            open_gate=data.get("open_gate"),
        )


def run_dir() -> Path:
    """Where run records live, resolved through the declared state inventory."""
    return config.state_path("run_state")


def run_path(run_id: str) -> Path:
    """One run's record. The identifier is generated, so it needs no escaping."""
    return run_dir() / f"{run_id}.json"


def save(state: RunState) -> Path:
    """Persist a run record atomically, owner-readable only.

    Atomic because the dispatcher writes it on the way out of a refusal: a torn
    record is a run that cannot be resumed, which is the one thing exiting with
    ``DECISION_REQUIRED`` promises.
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
    return RunState.from_json(raw)


def parse_decision_flags(values: list[str]) -> dict[str, str]:
    """Turn repeated ``gate=option`` arguments into a mapping.

    Rejects a malformed pair rather than ignoring it. A silently dropped decision
    is a run that stops at a gate the user believes they answered, and the next
    thing they do is answer it again the same way.
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

    Source 3 lands with the review queue (U11); the hook is left explicit rather
    than implicit so that when it arrives it has one place to attach, and
    ``tests/test_cli_contract.py`` holds the countdown.

    There is deliberately no fourth source. A blanket affirmative flag, a config
    key, or an environment variable would each satisfy every gate at once, which
    is what R34 forbids and what "the user pressed yes to something" already
    means in practice.
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
    ) -> str:
        """Return the chosen option, or raise so the CLI can exit resumably.

        ``context`` rides through to both refusals unchanged. BOTH, and that is
        the point rather than an implementation detail: this method refuses at
        two places, once because an explicit gate was answered inline and once
        because nothing answered it at all, and a context carried at only one of
        them would make what a person is shown depend on whether they typed a
        flag. It is a display value and never an input to the decision, so
        nothing below reads it.
        """
        self.reached.append(spec.name)

        recorded = self.state.decisions.get(spec.name)
        inline = self.supplied.get(spec.name)
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest

        if inline is not None and spec.explicit:
            # R34. An explicit gate is answered by a deliberate, separate act
            # that is recorded with its actor, never inline in the same
            # invocation that discovered the gate. Accepting it here would make
            # "each requires its own explicit assertion" satisfiable by typing
            # one more flag on the command that was already running.
            #
            # UNCONDITIONALLY, and it used to carry ``and recorded is None``.
            # That qualifier meant the refusal held only until SOME decision
            # existed, after which the ordinary precedence below preferred the
            # inline value over the recorded one, so a flag could overturn an
            # answer a person had deliberately recorded. It was invisible while
            # no landed verb reached an explicit gate that minted anything: U49
            # landed ``session.ack``, drove the ordering, and found that
            # ``--run R -d session.ack.backup=acknowledged`` recorded the backup
            # acknowledgment over a recorded ``abort``. That is the gate
            # standing in front of every destructive write in the product being
            # answered by the thing it gates, which is the one outcome R34
            # exists to prevent. A supplied flag is now refused whatever the run
            # already holds, so the recorded answer is the only answer.
            #
            # The open gate is still recorded before refusing, WHEN THE GATE IS
            # GENUINELY OPEN. A refusal that does not leave the run resumable is
            # a refusal the user answers by starting over, which is how people
            # learn to reach for the blanket flag this rule exists to deny them.
            # But a gate that already holds a recorded answer is not open, and
            # marking it so would make ``crate run show`` list one gate as both
            # answered and awaiting an answer, which is the run record
            # contradicting itself about the only thing it is for.
            if recorded is None:
                self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id, context)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
        if chosen is None:
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id, context)
        if chosen not in spec.options:
            raise UnknownOption(spec, chosen)

        if spec.digest_source is not None and digest is not None:
            against = recorded.digest if recorded is not None else None
            if against is not None and against != digest:
                raise DecisionStale(spec, self.state.run_id, against, digest)

        if recorded is None:
            self.state.decisions[spec.name] = Decision(
                option=chosen,
                actor=self.actor,
                recorded=output.timestamp(),
                digest=digest,
            )
        self.state.open_gate = None
        return chosen

    def hand_off(self, spec: GateSpec, *, verb: str, gate: str) -> str:
        """Carry the answer recorded on ``spec`` to a new run owned by ``verb``.

        WHY THIS EXISTS. A verb that queues another verb's job has to freeze a
        gate run the job's resume can load, and the dispatcher refuses a
        ``--run`` whose record belongs to a different verb. So ``crate sync all``
        cannot hand the favourites job its own run: the child ``sync favorites``
        would be refused on every respawn. This mints the run that child can
        load, holding the decision already given.

        IT COPIES AN ANSWER, IT NEVER SUPPLIES ONE. It refuses unless ``spec``
        holds a RECORDED decision with a digest, which after ``require`` returned
        is the decision a person gave, with its actor, against the artifact they
        were offered. The copy keeps that actor, that time and that digest, so
        the resumed child meets ``DecisionStale`` if what it rebuilds from the
        payload is not what the person saw. The target gate must be declared by
        ``verb``, must offer the chosen option, and must compare a digest, or the
        copy would answer a question the person was never asked.

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
        handed = RunState(
            run_id=output.new_run_id(),
            verb=verb,
            created=output.timestamp(),
            decisions={
                gate: Decision(
                    option=recorded.option,
                    actor=recorded.actor,
                    recorded=recorded.recorded,
                    digest=recorded.digest,
                )
            },
            offers={gate: recorded.digest},
        )
        save(handed)
        return handed.run_id


def record(state: RunState, spec: GateSpec, option: str, *, actor: str) -> None:
    """Write a decision into a run record, validating it against the gate.

    The digest comes from what the run OFFERED, never from the caller. A person
    answering in a later session has no way to quote the identity of something
    they were shown by a process that has already exited.
    """
    if option not in spec.options:
        raise UnknownOption(spec, option)
    state.decisions[spec.name] = Decision(
        option=option,
        actor=actor,
        recorded=output.timestamp(),
        digest=state.offers.get(spec.name),
    )
    if state.open_gate == spec.name:
        state.open_gate = None


def blocked_by(state: RunState, verb: str) -> Cause | None:
    """The cause refusing ``verb`` while this run has an unverified pending action.

    This is what makes ``pending_human_action`` load-bearing rather than
    advisory. The source system tells the user to import an XML and then forgets;
    nothing stops the next run from writing over the node that import was meant
    to create.
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


#: Codes this module raises, listed so the dispatcher's mapping is checkable.
GATE_CODES: tuple[ExitCode, ...] = (ExitCode.DECISION_REQUIRED, ExitCode.DECISION_STALE)


__all__ = [
    "GATE_CODES",
    "RUN_SCHEMA_VERSION",
    "Decision",
    "DecisionRequired",
    "DecisionStale",
    "Gates",
    "RunState",
    "UnknownOption",
    "blocked_by",
    "load",
    "new_run",
    "parse_decision_flags",
    "record",
    "run_dir",
    "run_path",
    "save",
]
