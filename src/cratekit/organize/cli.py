"""``crate organize``: plan both areas, ask each its own question, then write (U112).

THE ORDER IS PLAN, ASK, WRITE, ``sync all``'s order and for its reason. Both
areas are planned first, which is where every step's own precondition refuses.
Then the database area's gate is asked, then the account area's. Only once both
are answered does anything write, so a refusal at either gate has written
nothing, and the run that answers the second gate rebuilds the first area's
plan from a library nothing has touched yet, which is the plan its recorded
answer was given against.

ONE GATE PER AREA, EACH EXPLICIT AND BOUND TO ITS AREA'S DIGEST. Approving one
and aborting the other writes only the approved area. An area with nothing to
do says so and still asks. The database area is not asked when the backup
acknowledgment is missing: it was refused before it was planned, and it is the
account area alone that is asked and may write.

AN APPLIED STEP THAT FAILS DOES NOT STOP THE STEPS AFTER IT. Each step is its
own verb's write and none depends on another. Once every approved step has
run, a failure is raised with its own reason, the steps that did write named
in its message and the whole report in its detail, so a person is never told a
clean organize over a write that failed.

``--report`` plans both areas, asks nothing and writes nothing.

``--only KIND``, repeatable, NARROWS BOTH AREAS TO THE STEP KINDS IT NAMES
(U137). An area none of whose kinds is named is not planned, not asked and not
written, so ``--only file`` reads no backup acknowledgment and no database. An
area that is planned keeps its own preconditions, plans only the named kinds,
and its gate shows and its digest covers only those, with the selection named
in both. An unknown kind is refused by name by the parser, before anything is
read. With no ``--only`` the verb is exactly U112's.

THE MIRROR'S PLAN IS FROZEN ON THE RUN THAT SHOWS ITS GATE (R-1031), and the
run that answers rebuilds it from that record, so the mirror's digest is the
one the person approved however the library moved between the two acts. The
other account steps are planned again as before, so a write one of them reads,
a set landing for the sets step, can still stale the account gate.
``--rematch`` asks the provider again about every row the mirror remembers as
unmatched, on the run that shows the gate.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

import dataclasses
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import profiles
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import rotate_cli
from cratekit.modules.outbound import shell
from cratekit.organize import account, account_mirror, rekordbox
from cratekit.organize.steps import FAILED, Area, area_check, check, selection

#: The two gates, one per area. Looked up on ``ctx.entry.gates`` by name.
REKORDBOX_GATE = "organize.rekordbox.approve"
ACCOUNT_GATE = "organize.account.apply"

#: Every step kind ``--only`` may name, each area's in its own order. ``yours``
#: is a kind of both areas, and names both.
KINDS = tuple(dict.fromkeys((*rekordbox.STEPS, *account.STEPS)))

#: What each gate's go option is.
APPROVE = "approve"
APPLY = "apply"

_ORIGIN = ("organize", "cli")


def build(parser, entry) -> None:
    """Declare the verb. THERE IS NO ``--yes``: each area's gate is its only answer."""
    del entry
    parser.add_argument(
        "--report",
        action="store_true",
        default=False,
        help="print both plans and write nothing; no question is asked",
    )
    parser.add_argument(
        "--only",
        dest="only",
        action="append",
        choices=KINDS,
        default=None,
        metavar="KIND",
        help=(
            "plan, ask and write only this kind of step; repeat it for more. An "
            "area with no step named is not asked. One of: " + ", ".join(KINDS)
        ),
    )
    parser.add_argument(
        "--as-of",
        dest="as_of",
        default=None,
        metavar="DATE",
        help=(
            "the ISO date INBOX batches are aged against; today by default. Give "
            "the same date on the run that applies, or the plan is a different one"
        ),
    )
    parser.add_argument(
        "--rematch",
        action="store_true",
        default=False,
        help=(
            "ask the provider again about every row the account mirror remembers "
            "as unmatched, rather than only the rows that changed"
        ),
    )
    parser.set_defaults(_handler=organize)


def _gate(entry, name: str):
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=f"{entry.name} declares no gate named {name!r}, so an area has no question",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=_ORIGIN,
            detail={"verb": entry.name, "gate": name},
        )
    )


def _followed() -> tuple[tuple, CratekitError | None]:
    """Every followed label, or none and the registry's refusal when it cannot be read.

    THE REFUSAL IS THE LABEL STEP'S AND THE FILING'S, not the verb's: the
    database area reads the labels only for a suggested home, the filing to
    leave a label's playlist for the label step (U137), and the other account
    steps not at all, so an unreadable registry refuses the steps that need it.
    """
    from cratekit.label import registry as labels

    try:
        held = labels.RegistryStore().load()
    except CratekitError as exc:
        return (), exc
    entries = sorted(held.labels.values(), key=lambda entry: (entry.name, entry.label_id))
    return tuple(entries), None


def _ask(ctx, area: Area, name: str) -> str | None:
    """The area's answer, or ``None`` for an area refused before it was planned."""
    if area.cause is not None:
        return None
    return ctx.gate.require(_gate(ctx.entry, name), plan=area.payload(), context=area.shown())


def _apply(area: Area) -> None:
    for step in area.steps:
        if step.apply is None:
            continue
        try:
            step.applied = step.apply()
        except CratekitError as exc:
            step.error = exc
        except Exception as exc:  # noqa: BLE001 - recorded, never swallowed
            # ANY OTHER FAILURE IS THIS BUILD'S OWN, and it is the step's: the
            # steps after it are their own verbs' writes and still run, and the
            # failure is raised once they have, naming what did land.
            step.error = refuse(
                "internal-error",
                f"{step.title} failed in a way this build does not expect "
                f"({type(exc).__name__}: {exc})",
                remedy=Remedy.REPORT_DEFECT,
                origin=_ORIGIN,
                detail={"step": step.key, "kind": type(exc).__name__},
            )


def _report(areas: list[Area], *, report: bool, answers: dict[str, str | None]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    for area in areas:
        checks.append(area_check(area))
        checks.extend(check(area, step) for step in area.steps)
    return {
        "checks": checks,
        "summary": {
            "report": report,
            "answers": answers,
            "areas": {area.name: area.block() for area in areas},
        },
    }


def _warnings(areas: list[Area]) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for area in areas:
        if area.cause is not None:
            found.append(
                {
                    "code": "organize-area-refused",
                    "message": f"{area.name}: {area.cause.message}",
                }
            )
        for step in area.steps:
            found.extend(step.warnings)
            if step.cause is not None:
                found.append(
                    {
                        "code": "organize-step-refused",
                        "message": f"{area.name}, {step.title}: {step.cause.message}",
                    }
                )
    return found


def _raise_failed(areas: list[Area], data: dict[str, Any]) -> None:
    failed = [(area, step) for area in areas for step in area.steps if step.failed is not None]
    if not failed:
        return
    wrote = [
        f"{area.name}, {step.title}"
        for area in areas
        for step in area.steps
        if step.applied is not None
    ]
    area, step = failed[0]
    first = step.failed
    said = (
        f"{len(failed)} approved step(s) failed, the first {area.name}, {step.title}: "
        f"{first.message}. "
        + (
            "These were written and stay written: " + "; ".join(wrote)
            if wrote
            else "No other step was written"
        )
    )
    # THROUGH ``rebuilt``, so a parked adoption job's ``JobBlocked`` leaves as
    # the blocked refusal it is rather than as a plain failure.
    raise rebuilt(
        step.error,
        dataclasses.replace(
            first,
            message=said,
            origin=(*first.origin, *_ORIGIN),
            detail={**dict(first.detail or {}), "organize": data, "state": FAILED},
        ),
    )


def _named(kinds: tuple[str, ...], only: frozenset[str] | None) -> bool:
    """Whether ``--only`` named any of these kinds, or named nothing at all."""
    return selection(kinds, only) != ()


def organize(ctx) -> Envelope:
    """Plan both areas, ask each its own question, then write what was approved."""
    cfg = shell.load_config("organize.cli")
    report = bool(getattr(ctx.args, "report", False))
    chosen = getattr(ctx.args, "only", None)
    only = frozenset(chosen) if chosen else None
    membership = profiles.resolve(cfg.profile.name, cfg.modules.explicit)
    # THE REGISTRY IS READ ONLY FOR A STEP THAT USES IT: every account step
    # may, and on the database side only the author's own, for a home.
    followed, unfollowed = (
        _followed()
        if _named(account.STEPS, only) or _named((rekordbox.YOURS,), only)
        else ((), None)
    )
    today = rotate_cli.as_of(ctx)

    # EACH AREA IS PLANNED ONLY WHEN ONE OF ITS KINDS IS NAMED (U137), and an
    # area that is not planned is neither asked nor written.
    areas: list[Area] = []
    gates: list[tuple[Area, str, str]] = []
    if _named(rekordbox.STEPS, only):
        database = rekordbox.plan_area(
            cfg,
            ctx,
            gate=REKORDBOX_GATE,
            today=today,
            labels=tuple(entry.name for entry in followed),
            report=report,
            only=only,
            available=membership.available,
        )
        areas.append(database)
        gates.append((database, REKORDBOX_GATE, APPROVE))
    if _named(account.STEPS, only):
        state = ctx.gate.state
        remote = account.plan_area(
            cfg,
            available=membership.available,
            followed=followed,
            unfollowed=unfollowed,
            only=only,
            run=account_mirror.Run(
                run_id=state.run_id,
                record=not report,
                decided=not report and ACCOUNT_GATE in state.decisions,
                rematch=bool(getattr(ctx.args, "rematch", False)),
            ),
        )
        areas.append(remote)
        gates.append((remote, ACCOUNT_GATE, APPLY))

    if report:
        data = _report(areas, report=True, answers={})
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_warnings(areas))

    answers = {area.name: _ask(ctx, area, name) for area, name, _go in gates}
    for area, _name, go in gates:
        if answers[area.name] == go and area.writes:
            _apply(area)

    data = _report(areas, report=False, answers=answers)
    _raise_failed(areas, data)
    wrote = any(step.applied is not None for area in areas for step in area.steps)
    return ctx.envelope(
        data=data,
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        warnings=_warnings(areas),
    )


__all__ = ["ACCOUNT_GATE", "KINDS", "REKORDBOX_GATE", "build", "organize"]
