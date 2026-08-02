"""R34's half of adoption: approval is an act, and nothing else can stand in.

R34 names two assertions that no blanket affirmative may satisfy: the R15 backup
acknowledgment and the R26 adoption approval. The backup half landed with U8, as
a record on the disk with the actor who made it. This is the other half.

WHAT "NON-BYPASSABLE" HAS TO MEAN IN CODE, rather than in a docstring. Three
things, and each of them is a thing somebody would otherwise add later without
noticing what they undid:

1. **There is no truthy shape that approves.** :func:`require_approval` takes an
   :class:`Approval` or nothing. ``True``, ``"yes"``, ``1``, and a mapping that
   happens to carry the right keys are all refused by the same branch that
   refuses ``None``, because none of them is an approval and a check that
   accepted them would be a check on typing rather than on consent. The refusal
   is the DECISION_REQUIRED cause, so the boundary above renders it as the gate
   it is rather than as an internal defect.

2. **An approval names the plan it was given for.** It carries the digest the
   plan had when the person saw it, and a digest that no longer matches refuses.
   Approving a plan and then applying a different one is the failure the digest
   exists to prevent, and it is not hypothetical: adoption's plan is built from a
   library that a person may have edited in rekordbox in between.

3. **An approval names who gave it.** An approval with no actor is the product
   asserting something about itself, which is the one thing it must never do
   here. R34 says each write session records which actor asserted, so an empty
   actor is refused rather than defaulted to the process.

WHAT THIS MODULE DELIBERATELY DOES NOT DO. It reads no environment variable, no
configuration key, and no flag. There is no fourth source, for the reason
:class:`cratekit.cli.gates.Gates` gives for having only three: a blanket flag, a
config key, or an environment variable each satisfies every gate at once, which
is what R34 forbids and what "the user pressed yes to something" already means in
practice. ``tests/test_adoption.py`` walks this package's syntax tree and asserts
that no module in it reads the environment at all, and runs that guard against an
evasion as well as against this tree, because a guard nobody ran against the
thing it forbids is a guard nobody has tested.

Layer: modules. It names the CLI gate this approval corresponds to as a VALUE,
the same way the review queue takes a handler key as a value, so the CLI shell
that raises the gate and this module cannot disagree about which gate it was.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cratekit.adopt.plan import AdoptionPlan
from cratekit.cli.output import timestamp
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The gate this approval answers, in the registry's own vocabulary. Declared
#: here as the one place the two spellings meet, so a refusal raised from the
#: engine and a gate raised from a command line name the same thing.
APPROVAL_GATE = "adopt.apply.approve"

#: The one option that approves. A closed set of one, because the alternative to
#: approving is not approving, and giving that a name here would make it look
#: like an option this module has to handle.
APPROVE = "approve"


@dataclass(frozen=True, slots=True)
class Approval:
    """A person's recorded approval of ONE plan.

    Frozen and slotted, so an approval cannot be edited into approving a
    different plan after the fact, and so an attribute the checker relies on
    cannot be attached to it by a caller.
    """

    digest: str
    actor: str
    granted: str
    option: str = APPROVE

    def to_json(self) -> dict[str, Any]:
        return {
            "digest": self.digest,
            "actor": self.actor,
            "granted": self.granted,
            "option": self.option,
            "gate": APPROVAL_GATE,
        }


def grant(plan: AdoptionPlan, *, actor: str, now: datetime | None = None) -> Approval:
    """Record an approval for the plan AS IT IS NOW.

    The digest is taken from the plan rather than from the caller, for the reason
    :func:`cratekit.cli.gates.record` takes it from what the run offered: a person
    answering in a later session has no way to quote the identity of something
    they were shown by a process that has already exited, and a digest a caller
    supplies is a digest a caller can supply the wrong value for.
    """
    if not str(actor).strip():
        raise refuse(
            "decision-required",
            "approving an adoption plan records WHO approved it, and this "
            "approval names nobody; R34 says each write session records which "
            "actor asserted, so an unattributed approval is not an approval",
            steps=("re-run the approval naming the person or account approving it",),
            scope=Scope.RUN,
            origin=("adopt",),
            detail={"gate": APPROVAL_GATE},
        )
    return Approval(digest=plan.digest(), actor=str(actor), granted=timestamp(now))


def require_approval(plan: AdoptionPlan, approval: object) -> Approval:
    """Return the approval that permits applying ``plan``, or refuse.

    THE TYPE CHECK IS THE POINT, not defensiveness. ``approval`` is typed as
    ``object`` deliberately: the shapes this has to refuse are exactly the shapes
    a caller reaches for when they want to get past it, and a signature that
    accepted ``Approval | None`` would put the refusal in the type checker, where
    it protects the author and not the user. A blanket affirmative arrives at
    runtime as ``True``, as the string a flag parser produced, or as a dictionary
    somebody deserialized; every one of them lands here.

    ``review-already-resolved`` is deliberately NOT the slug for a stale
    approval. The remedy differs: a stale approval is answered by re-planning and
    approving again, which is what ``decision-stale`` already means and what its
    remediation token already says.
    """
    if not isinstance(approval, Approval):
        raise refuse(
            "decision-required",
            f"applying an adoption plan needs an explicit approval for THIS plan "
            f"and this run supplied {type(approval).__name__}; R34 says no "
            f"blanket affirmative flag, configuration key, or environment "
            f"variable satisfies the adoption approval",
            steps=(
                f"review the plan, then answer the {APPROVAL_GATE} gate as a "
                f"separate, attributed act",
            ),
            scope=Scope.RUN,
            retryable=True,
            origin=("adopt",),
            detail={"gate": APPROVAL_GATE, "options": [APPROVE]},
        )
    if approval.option != APPROVE:
        raise refuse(
            "decision-required",
            f"the recorded answer to {APPROVAL_GATE} is {approval.option!r}, "
            f"which is not an approval; nothing is applied",
            steps=("approve the plan, or leave it unapplied",),
            scope=Scope.RUN,
            retryable=True,
            origin=("adopt",),
            detail={"gate": APPROVAL_GATE, "options": [APPROVE]},
        )
    if not str(approval.actor).strip():
        raise refuse(
            "decision-required",
            "the recorded approval names no actor, so this run cannot say who "
            "approved the writes it is about to make",
            steps=("approve the plan again, naming the person or account approving it",),
            scope=Scope.RUN,
            origin=("adopt",),
            detail={"gate": APPROVAL_GATE},
        )
    current = plan.digest()
    if approval.digest != current:
        raise refuse(
            "decision-stale",
            f"this approval was given for a plan whose digest was "
            f"{approval.digest!r} and the plan now digests to {current!r}; the "
            f"library, the taxonomy, or an answered question has moved since, so "
            f"applying now would apply something nobody approved",
            remedy=Remedy.REPLAN_THEN_DECIDE,
            scope=Scope.RUN,
            retryable=True,
            origin=("adopt",),
            detail={
                "gate": APPROVAL_GATE,
                "expected": current,
                "approved": approval.digest,
            },
        )
    return approval


__all__ = [
    "APPROVAL_GATE",
    "APPROVE",
    "Approval",
    "grant",
    "require_approval",
]
