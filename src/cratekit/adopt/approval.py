"""R34's half of adoption: approval is an act, and nothing else can stand in.

R34 names two assertions no blanket affirmative may satisfy: the R15 backup
acknowledgment, landed with U8, and the R26 adoption approval, here.

NON-BYPASSABLE MEANS THREE THINGS IN CODE:

1. **No truthy shape approves.** :func:`require_approval` takes an
   :class:`Approval` or refuses, with the DECISION_REQUIRED cause, so ``True``,
   ``"yes"`` and a mapping with the right keys are refused like ``None``.
2. **An approval names the plan it was given for**, by digest, so a plan that
   moved since the person saw it is refused.
3. **An approval names who gave it.** An empty actor is refused rather than
   defaulted to the process.

IT READS NO ENVIRONMENT VARIABLE, CONFIGURATION KEY OR FLAG: each would satisfy
every gate at once (see :class:`cratekit.cli.gates.Gates`).
``tests/test_adoption.py`` asserts no module in this package reads the
environment, and runs that guard against an evasion too.

Layer: modules. The CLI gate this answers is named as a value, so the shell that
raises the gate and this module cannot disagree about which gate it was.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from cratekit.adopt.plan import AdoptionPlan
from cratekit.cli.output import timestamp
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy

#: The gate this approval answers, in the registry's own vocabulary.
APPROVAL_GATE = "adopt.apply.approve"

#: The one option that approves. Not approving needs no name here.
APPROVE = "approve"


def _required(message: str, step: str, *, offered: bool = False) -> CratekitError:
    """A ``decision-required`` refusal at this gate; ``offered`` names the option
    that approves and makes it retryable."""
    detail: dict[str, Any] = {"gate": APPROVAL_GATE}
    if offered:
        detail["options"] = [APPROVE]
    return refuse(
        "decision-required",
        message,
        steps=(step,),
        retryable=offered,
        origin=("adopt",),
        detail=detail,
    )


@dataclass(frozen=True, slots=True)
class Approval:
    """A person's recorded approval of ONE plan.

    Frozen and slotted, so it cannot be edited into approving another plan or
    given an attribute the checker relies on.
    """

    digest: str
    actor: str
    granted: str
    option: str = APPROVE

    def to_json(self) -> dict[str, Any]:
        return {**asdict(self), "gate": APPROVAL_GATE}


def grant(plan: AdoptionPlan, *, actor: str, now: datetime | None = None) -> Approval:
    """Record an approval for the plan AS IT IS NOW.

    The digest is taken from the plan, never from the caller, who could supply
    the wrong one.
    """
    if not str(actor).strip():
        raise _required(
            "approving an adoption plan records WHO approved it, and this "
            "approval names nobody; R34 says each write session records which "
            "actor asserted, so an unattributed approval is not an approval",
            "re-run the approval naming the person or account approving it",
        )
    return Approval(digest=plan.digest(), actor=str(actor), granted=timestamp(now))


def require_approval(plan: AdoptionPlan, approval: object) -> Approval:
    """Return the approval that permits applying ``plan``, or refuse.

    ``approval`` IS TYPED ``object`` ON PURPOSE: the shapes to refuse are the
    ones a caller reaches for to get past it, and they arrive at runtime, where a
    type checker protects nobody. A stale approval is ``decision-stale``, whose
    remedy is to re-plan and approve again.
    """
    if not isinstance(approval, Approval):
        raise _required(
            f"applying an adoption plan needs an explicit approval for THIS plan "
            f"and this run supplied {type(approval).__name__}; R34 says no "
            f"blanket affirmative flag, configuration key, or environment "
            f"variable satisfies the adoption approval",
            f"review the plan, then answer the {APPROVAL_GATE} gate as a separate, attributed act",
            offered=True,
        )
    if approval.option != APPROVE:
        raise _required(
            f"the recorded answer to {APPROVAL_GATE} is {approval.option!r}, "
            f"which is not an approval; nothing is applied",
            "approve the plan, or leave it unapplied",
            offered=True,
        )
    if not str(approval.actor).strip():
        raise _required(
            "the recorded approval names no actor, so this run cannot say who "
            "approved the writes it is about to make",
            "approve the plan again, naming the person or account approving it",
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
            retryable=True,
            origin=("adopt",),
            detail={"gate": APPROVAL_GATE, "expected": current, "approved": approval.digest},
        )
    return approval
