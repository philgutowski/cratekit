"""One area of ``crate organize`` and the steps it is made of (U112).

A STEP is one plan a composed verb made: one label's folder, one pass's marks,
one set's archive, the adoption, the rotation. Each is of one KIND, the word
``--only`` selects it by (U137). It is in exactly one state:

==============  ===============================================================
``planned``     the step's own plan writes, and runs once its area is approved
``nothing``     the step's own plan writes nothing; a second run's every step
``refused``     the step's own precondition refused; the refusal is shown and
                no other step is hidden by it
``listed``      something no verb owns is named and nothing is planned for it
==============  ===============================================================

THE AREA'S DIGEST IS TAKEN OVER EVERY STEP'S KEY, STATE AND OWN DIGEST, a
refused step's reason standing in for a digest. So an approval binds to the
plans the screen showed: a step that refused when the question was asked and
plans by the time it is answered moves the digest, and the answer is stale
rather than honoured over a write nobody saw.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core.cause import Cause, CratekitError

#: A step's states, one word each.
PLANNED = "planned"
NOTHING = "nothing"
REFUSED = "refused"
LISTED = "listed"

#: What an applied step became.
APPLIED = "applied"
FAILED = "failed"


@dataclass
class Step:
    """One composed plan, and what became of it."""

    key: str
    title: str
    state: str
    detail: str
    digest: str | None = None
    counts: dict[str, Any] = field(default_factory=dict)
    items: list[dict[str, Any]] = field(default_factory=list)
    cause: Cause | None = None
    #: What runs once the area is approved; ``None`` for every state but planned.
    apply: Callable[[], dict[str, Any]] | None = None
    applied: dict[str, Any] | None = None
    #: The refusal an apply raised, kept whole so a re-raise keeps its type.
    error: CratekitError | None = None
    warnings: list[dict[str, str]] = field(default_factory=list)

    @property
    def writes(self) -> bool:
        return self.state == PLANNED

    @property
    def failed(self) -> Cause | None:
        return self.error.cause if self.error is not None else None

    def identity(self) -> list[Any]:
        """What the area's digest covers of this step."""
        said = self.digest if self.cause is None else f"refused:{self.cause.reason}"
        return [self.key, self.state, said]

    def item(self) -> dict[str, Any]:
        """The step as its area's gate shows it."""
        shown: dict[str, Any] = {
            "step": self.key,
            "title": self.title,
            "state": self.state,
            "detail": self.detail,
            "counts": dict(self.counts),
            "plan": list(self.items),
        }
        if self.digest is not None:
            shown["digest"] = self.digest
        if self.cause is not None:
            shown["reason"] = self.cause.reason
        return shown


def refused(key: str, title: str, cause: Cause) -> Step:
    """A step whose own precondition refused, shown with its reason."""
    return Step(key=key, title=title, state=REFUSED, detail=cause.message, cause=cause)


#: The fact a narrowed area shows in front of its steps (U137).
ONLY_FACT = "only these steps"


def selection(kinds: tuple[str, ...], only: frozenset[str] | None) -> tuple[str, ...] | None:
    """The area's own kinds ``--only`` chose, in the area's order; ``None`` for every one."""
    if only is None:
        return None
    return tuple(kind for kind in kinds if kind in only)


@dataclass
class Area:
    """One side of the library: its steps, what the author made, and its own refusal."""

    name: str
    steps: list[Step] = field(default_factory=list)
    #: The author's own playlists and folders, listed and never written.
    yours: list[dict[str, Any]] = field(default_factory=list)
    #: Writes no verb owns, suggested and never made.
    suggested: list[dict[str, Any]] = field(default_factory=list)
    #: Facts the screen shows in front of the steps.
    facts: dict[str, Any] = field(default_factory=dict)
    #: A refusal of the whole area, before any step: the database area with no
    #: backup acknowledgment. Its gate is not asked, since it could write nothing.
    cause: Cause | None = None
    #: The step kinds ``--only`` selected (U137), or ``None`` for every step.
    only: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if self.only is not None:
            self.facts[ONLY_FACT] = ", ".join(self.only)

    def wants(self, kind: str) -> bool:
        """Whether a step of this kind is planned here."""
        return self.only is None or kind in self.only

    @property
    def writes(self) -> bool:
        return self.cause is None and any(step.writes for step in self.steps)

    def counts(self) -> dict[str, int]:
        tally = {PLANNED: 0, NOTHING: 0, REFUSED: 0, LISTED: 0}
        for step in self.steps:
            tally[step.state] = tally.get(step.state, 0) + 1
        return tally

    def identity(self) -> dict[str, Any]:
        """The document the area's digest is taken over, every step's own digest in it.

        A NARROWED AREA NAMES ITS SELECTION (U137), so an answer given over the
        steps ``--only`` chose is never read as one given over the whole area.
        The key is absent with no selection, which keeps the full digest as it was.
        """
        identity: dict[str, Any] = {
            "kind": "organize",
            "area": self.name,
            "steps": [step.identity() for step in self.steps],
        }
        if self.only is not None:
            identity["only"] = list(self.only)
        return identity

    def digest(self) -> str:
        return digest_of(self.identity())

    def payload(self) -> dict[str, Any]:
        """The area as its gate digests and shows it, every step an item."""
        return {"digest": self.digest(), "items": [step.item() for step in self.steps]}

    def shown(self) -> dict[str, Any]:
        """The facts in front of the steps, the author's own things among them."""
        tally = self.counts()
        shown: dict[str, Any] = {
            "area": self.name,
            "steps": (
                f"{tally[PLANNED]} to apply, {tally[NOTHING]} with nothing to do, "
                f"{tally[REFUSED]} refused, {tally[LISTED]} listed only"
            ),
            **self.facts,
            "yours, not moved": [_your_line(one) for one in self.yours],
            "deletes": "nothing: no playlist, folder or track is deleted by organize",
        }
        if self.suggested:
            shown["suggested, not written"] = [one["suggestion"] for one in self.suggested]
        if not self.writes:
            shown["nothing to do"] = (
                "no step in this area has anything to write; answering still records "
                "the decision"
            )
        return shown

    def block(self) -> dict[str, Any]:
        """The area as the envelope's summary carries it."""
        block: dict[str, Any] = {
            "digest": self.digest(),
            "counts": self.counts(),
            "steps": [
                {
                    **step.item(),
                    **({"applied": step.applied} if step.applied is not None else {}),
                    **({"failed": step.failed.to_json()} if step.failed is not None else {}),
                }
                for step in self.steps
            ],
            "yours": list(self.yours),
            "suggested": list(self.suggested),
            # THE FACTS RIDE THE REPORT TOO, not only the gate's screen, since
            # ``--report`` asks nothing and a missing backup acknowledgment it
            # notes would otherwise reach no one.
            "facts": dict(self.facts),
        }
        if self.cause is not None:
            block["refused"] = self.cause.to_json()
        return block


def _your_line(one: dict[str, Any]) -> str:
    home = one.get("suggested_home")
    return f"{one['name']} ({one['place']})" + (
        f": suggested home {home}, not moved" if home else ": not moved"
    )


def check(area: Area, step: Step) -> dict[str, Any]:
    """One step as a ``diagnostic/1`` check row, since the default output prints rows."""
    status = {PLANNED: "info", NOTHING: "ok", REFUSED: "fail", LISTED: "info"}[step.state]
    detail = step.detail
    remedy = None
    if step.cause is not None:
        remedy = str(step.cause.remediation.remedy)
        if step.cause.remediation.steps:
            detail += "; " + "; ".join(step.cause.remediation.steps)
    if step.failed is not None:
        status = "fail"
        detail = f"failed on apply: {step.failed.message}"
        remedy = str(step.failed.remediation.remedy)
    elif step.applied is not None:
        status = "ok"
        detail = f"{APPLIED}: {step.detail}"
    return {
        "key": f"organize.{area.name}.{step.key}",
        "title": f"{area.name}: {step.title}",
        "status": status,
        "detail": detail,
        "remedy": remedy,
    }


def area_check(area: Area) -> dict[str, Any]:
    """The area's own row: its refusal, or what the author made, listed."""
    if area.cause is not None:
        detail = area.cause.message
        if area.cause.remediation.steps:
            detail += "; " + "; ".join(area.cause.remediation.steps)
        return {
            "key": f"organize.{area.name}",
            "title": area.name,
            "status": "fail",
            "detail": f"not planned: {detail}",
            "remedy": str(area.cause.remediation.remedy),
        }
    facts = "; ".join(
        f"{key}: {value}" for key, value in area.facts.items() if isinstance(value, (str, int))
    )
    return {
        "key": f"organize.{area.name}",
        "title": area.name,
        "status": "info",
        "detail": (
            (f"{facts}; " if facts else "")
            + f"{len(area.yours)} of your own listed and not moved"
            + (
                ": " + "; ".join(_your_line(one) for one in area.yours)
                if area.yours
                else ""
            )
            + (
                f"; {len(area.suggested)} suggestion(s) nothing writes: "
                + "; ".join(one["suggestion"] for one in area.suggested)
                if area.suggested
                else ""
            )
        ),
        "remedy": None,
    }


__all__ = [
    "APPLIED",
    "FAILED",
    "LISTED",
    "NOTHING",
    "ONLY_FACT",
    "PLANNED",
    "REFUSED",
    "Area",
    "Step",
    "area_check",
    "check",
    "refused",
    "selection",
]
