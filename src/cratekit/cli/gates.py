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
from datetime import datetime, timedelta, timezone
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

    def __init__(
        self,
        spec: GateSpec,
        run_id: str,
        expected: str,
        actual: str,
        *,
        pinned: str | None = None,
    ) -> None:
        self.spec = spec
        self.run_id = run_id
        message = (
            f"the decision on {spec.name!r} was made against a "
            f"{spec.digest_source} that has since changed"
        )
        if pinned is not None:
            # A PINNED FACT MOVED, not the digest (U161): name both values,
            # since the plan itself digests the same.
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
    #: gate name -> the facts the person was shown that the answer binds to
    #: OUTSIDE the digest (U161), recorded when the gate is left open and
    #: compared when a recorded answer is used. A native landing pins the
    #: database file here, so its digest can name the library alone and a
    #: copy rehearsal digest the same, while the answer still holds only for
    #: the file the screen named.
    pins: dict[str, dict[str, str]] = field(default_factory=dict)
    pending: output.PendingHumanAction | None = None
    open_gate: str | None = None
    #: The verb's own command line as its first invocation gave it (U168),
    #: the verb's path and every argument after it, without the global
    #: ``--run``, ``-d`` and ``--output``. What ``run decide --continue``
    #: dispatches again under ``--run``. None for a run recorded before it.
    argv: tuple[str, ...] | None = None
    #: Other runs this run is bound to, by role (U183). ``crate sync land``
    #: names the ``sync all`` pass it queued or continued under ``pass_run``
    #: the moment that pass is known, so the land run's own identifier
    #: continues the pass, even after a run that failed or was interrupted.
    related_runs: dict[str, str] = field(default_factory=dict)

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
        # ONLY WHEN THERE ARE ANY, so a run no pinning gate reached keeps the
        # record it had before U161.
        if self.pins:
            record["pins"] = {name: dict(sorted(one.items())) for name, one in sorted(self.pins.items())}
        # AND THE COMMAND LINE ONLY WHEN THERE IS ONE (U168), for the same reason.
        if self.argv is not None:
            record["argv"] = list(self.argv)
        # AND THE RELATED RUNS ONLY WHEN THERE ARE ANY (U183), the same reason.
        if self.related_runs:
            record["related_runs"] = dict(sorted(self.related_runs.items()))
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


#: The keys :func:`shown_plan` fills from the plan. A fact under one of these
#: names would be overwritten without a word, so it is refused instead.
SHOWN_PLAN_KEYS = ("digest", "count", "items")


def shown_plan(plan: Mapping[str, Any], facts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """What a digest bound gate puts in front of the person (R-693).

    The facts the caller names, then the plan's digest, its count and EVERY
    ITEM the digest was taken over, so the screen is the plan a person
    approves, and a JSON reader can compare it with the plan a declined run
    returns where the verb returns one. R-670 and R-686 closed this shape one
    verb at a time, and seven gates were still passing a digest and nothing to
    show, so their screens carried the question and not the plan; a declined
    run was the only way to read one. This is the one body every digest bound
    gate shows through, and :meth:`Gates.require` calls it whenever a plan is
    passed.

    THERE IS NO BOUND. The digest covers every item, and a list cut short
    would ask for approval of items nobody was shown. ``count`` is the number
    of items, which is what the digest covers, and a verb whose own totals
    count something narrower names them in its facts under their own names,
    never under one of ``SHOWN_PLAN_KEYS``: a fact under one of those would
    be overwritten by the plan's value without a word, so it is refused.

    The values must be JSON already, the rule :class:`DecisionRequired` states.
    """
    named = dict(facts or {})
    taken = sorted(set(named) & set(SHOWN_PLAN_KEYS))
    if taken:
        raise ValueError(f"shown_plan() fills {taken} from the plan; name the fact differently")
    items = list(plan["items"])
    return {**named, "digest": plan["digest"], "count": len(items), "items": items}


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
        plan: Mapping[str, Any] | None = None,
        pinned: Mapping[str, str] | None = None,
    ) -> str:
        """Return the chosen option, or raise so the CLI can exit resumably.

        ``pinned`` IS WHAT THE ANSWER BINDS TO OUTSIDE THE DIGEST (U161): facts
        the screen shows that two equal plans may differ by, such as which
        database file a copy rehearsal reads. They are recorded on the run
        when the gate is left open, and a recorded answer whose run pinned
        other values is refused stale, naming the fact, so a digest left free
        of a path for the sake of a rehearsal does not free the answer of it.

        ``context`` rides through to both refusals unchanged. BOTH, and that is
        the point rather than an implementation detail: this method refuses at
        two places, once because an explicit gate was answered inline and once
        because nothing answered it at all, and a context carried at only one of
        them would make what a person is shown depend on whether they typed a
        flag. It is a display value and never an input to the decision, so
        nothing below reads it.

        ``plan`` IS THE DIGESTED PLAN, ``digest`` AND ``items`` ON ONE MAPPING
        (R-693). The digest the decision binds to is read off it, and the
        screen shows its items through :func:`shown_plan`, with ``context`` as
        the facts in front of them. One object for both, so what a person is
        shown and what their answer is recorded against cannot be two plans.
        A caller passes ``digest`` or ``plan`` and never both, because two
        sources of the digest is exactly how the screen and the binding come
        to disagree, and that is refused here rather than resolved quietly.
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
        self.state.open_gate = None
        return chosen

    def hand_off(
        self,
        spec: GateSpec,
        *,
        verb: str,
        gate: str,
        part: tuple[Any, str] | None = None,
    ) -> str:
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

        ``part`` IS FOR A COMPOSER WHOSE ONE ANSWER COVERS SEVERAL PLANS (U112).
        ``crate organize`` asks one question over an area whose digest is taken
        over every step's own digest, and a step it hands to ``adopt apply``'s
        job must carry that step's digest, not the area's, or the job's resume
        meets ``DecisionStale``. ``part`` is the document the recorded digest
        was taken over and the step's digest inside it. The copy refuses unless
        the document digests to exactly what the person answered and the
        step's digest is one of its values, so the digest handed on is one the
        recorded answer was given over and never one a caller made up.

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


# ---------------------------------------------------------------------------
# Open gates nobody will answer (U170)
# ---------------------------------------------------------------------------

#: The option an old open gate is retired with, and the only one. Every gate
#: but two offers it, and a retirement answers nothing but no.
RETIRE_OPTION = "abort"


@dataclass(frozen=True, slots=True)
class OldGate:
    """One open gate that has sat idle for longer than a threshold (U170).

    ``idle_since`` is the LATER of the run's ``created`` stamp and the last
    write of its record, because the dispatcher saves a run each time it is
    resumed: a run started a month ago and resumed yesterday is a run somebody
    is still working, and its age runs from yesterday.

    ``kept`` is None when the gate can be retired, and otherwise says why not
    in words. A gate whose verb no longer declares it, or whose options carry
    no ``abort``, is old and still never answered by a retirement, since the
    only safe answer to give on a person's behalf is no.
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

    A record whose file cannot be read for its time is as new as now, so a
    gate whose age cannot be measured is never called old (absence of a
    reading is not age).
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

    THE ONE PREDICATE ``crate status`` AND ``crate run retire`` BOTH READ, so the
    line status collapses and the set the command retires cannot be two sets.
    None for a run with no open gate, a run waiting only on a pending human
    action included, and for one touched within the threshold.
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


#: Codes this module raises, listed so the dispatcher's mapping is checkable.
GATE_CODES: tuple[ExitCode, ...] = (ExitCode.DECISION_REQUIRED, ExitCode.DECISION_STALE)


__all__ = [
    "GATE_CODES",
    "RETIRE_OPTION",
    "RUN_SCHEMA_VERSION",
    "Decision",
    "DecisionRequired",
    "DecisionStale",
    "Gates",
    "OldGate",
    "RunState",
    "UnknownOption",
    "blocked_by",
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
]
