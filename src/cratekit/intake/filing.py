"""A native landing files the rows it made into the library tree, under the landing's one answer (U165).

WHY THIS IS NOT ONE COMMIT. Adoption's plan names its work by content id, and
the rows a landing makes have none until it commits, so the adoption cannot
join the landing's digest. What can is a PREDICTION: before any row exists
the landing asks adoption's own rule, :func:`cratekit.adopt.plan.predicted_place`,
where each file to be added would be filed, lists it on the gate screen and
digests it with the rest of the plan. After the commit the same run plans
adoption over the landed ids, and files them through the adopt worker's own
order, :func:`cratekit.adopt.apply_cli.file_plan`, when every entry equals its
prediction. Two commits, one answer.

WHEN THEY DIFFER NOTHING IS FILED AND NOTHING IS ROLLED BACK. A tree moved, a
sub undeclared, a file retagged or a vocal sub renamed between the plan and
the apply is a filing nobody approved, and the landing it follows is already
true. The run says which rows differ and names ``crate adopt apply``, which
asks its own question over the plan as it is.

LAYER: modules. It composes the landing and adoption and writes through
adoption's own writers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping, Sequence

from cratekit.adopt import apply_cli, collection
from cratekit.adopt import plan as plan_engine
from cratekit.adopt.scan import Disposition
from cratekit.core import config, tags, taxonomy
from cratekit.core.cause import CratekitError, refuse

if TYPE_CHECKING:
    from cratekit.intake import native

_ORIGIN = ("intake", "filing")

#: What :func:`file_landed` did, in one word each.
FILED = "filed"
FILED_DIFFERENTLY = "filed-differently"
NOT_FILED = "not-filed"
NOTHING_TO_FILE = "nothing-to-file"

#: The warning a landing carries when the filing did not follow it.
FILED_DIFFERENTLY_WARNING = "landing-filed-differently"
NOT_FILED_WARNING = "landing-not-filed"

#: The verb a person runs to file what a landing could not.
ADOPT_APPLY = "crate adopt apply"


@dataclass(frozen=True, slots=True)
class Prediction:
    """One file to be added and where adoption would file its row."""

    target: Path
    place: plan_engine.Predicted

    def identity(self) -> list[str]:
        return [str(self.target), *self.place.identity()]

    def shown(self) -> str:
        """The place on the gate screen, by the taxonomy's identifiers."""
        return shown_place(self.place)


def shown_place(place: plan_engine.Predicted) -> str:
    """One prediction in words: its bucket and sub, or why it is placed nowhere."""
    if place.disposition is Disposition.ROUTE:
        vocal = f", and its vocal sub {place.vocal_sub}" if place.vocal_sub else ""
        return f"{place.bucket} / {place.sub}{vocal}"
    if place.disposition is Disposition.NEEDS_GENRE:
        return "placed nowhere: no genre adoption can file"
    return f"placed nowhere: {place.disposition}"


def predict(declared: taxonomy.Taxonomy, rows: Sequence[native.RowPlan]) -> tuple[Prediction, ...]:
    """Where adoption would file each row to be added, read off the plan and its file.

    THE GENRE IS THE ROW'S, as the landing writes it (U163), since that is the
    word adoption will read off the row. The energy is the file's, through
    adoption's own checked reader, and an unreadable reading predicts as none,
    which is what the scan records for it. The vocal sub is asked only for a
    row the plan gives the vox tag.
    """
    predicted: list[Prediction] = []
    for row in rows:
        genre = row.genre.name if row.genre is not None else ""
        try:
            energy = tags.read_energy_checked(row.source)
        except (tags.TagReadFailed, OSError):
            energy = None
        predicted.append(
            Prediction(
                target=row.target,
                place=plan_engine.predicted_place(declared, genre, energy, vox=row.vox),
            )
        )
    return tuple(predicted)


def fact(predicted: Sequence[Prediction] | None, *, why: str, tree: str) -> str:
    """The gate screen's one line on the filing after the landing."""
    if predicted is None:
        return f"nothing, {why}" if why else "nothing"
    nowhere = sum(1 for one in predicted if one.place.disposition is not Disposition.ROUTE)
    placed = len(predicted) - nowhere
    said = f"{placed} new row(s) into {tree} under this answer"
    if nowhere:
        said += f", {nowhere} placed nowhere"
    return said + ", when adoption plans each as shown; otherwise nothing is filed"


def identity(predicted: Sequence[Prediction]) -> list[list[str]]:
    """What the landing's digest covers of the filing: every prediction."""
    return [one.identity() for one in predicted]


@dataclass(frozen=True, slots=True)
class Filed:
    """What the filing after a landing did, and why when it did not."""

    state: str
    #: Each row whose plan after the commit is not its prediction, in words.
    differing: tuple[str, ...] = ()
    #: The landed rows adoption places nowhere, by file name, and why.
    nowhere: tuple[str, ...] = ()
    #: The rows filed, the memberships the tree writer added, and the Favorites.
    filed: int = 0
    memberships: int = 0
    favorites: Mapping[str, object] | None = None
    #: The refusal that stopped the filing, in a sentence, when one did.
    why: str = ""


def file_landed(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    predicted: Sequence[Prediction],
    landed: native.NativeLanded,
    *,
    actor: str,
) -> Filed:
    """Plan adoption over the rows the landing made and file them when every one is as predicted.

    AFTER THE LANDING'S HANDLE IS CLOSED, since every writer it calls opens its
    own. The collection cache is forgotten first: it may hold the library as
    it was before the landing's commit.

    A REFUSAL IS A FILING THAT DID NOT HAPPEN, NEVER A LANDING THAT FAILED. The
    rows are in the library by now, so a refusal from adoption's writers comes
    back as :data:`NOT_FILED` with its sentence for the landing to report.
    """
    by_target = {str(row.target): row.content_id for row in landed.added}
    expected = {
        by_target[str(one.target)]: one for one in predicted if str(one.target) in by_target
    }
    if not expected:
        return Filed(state=NOTHING_TO_FILE)
    collection.reset_cache()
    try:
        plan = apply_cli.current_plan(cfg, declared, scope=frozenset(expected))
    except CratekitError as exc:
        return Filed(state=NOT_FILED, why=exc.cause.message)
    found = {entry.content_id: entry for entry in plan.entries}
    differing: list[str] = []
    for content_id, one in expected.items():
        entry = found.get(content_id)
        now = plan_engine.Predicted.of(entry) if entry is not None else None
        if now != one.place:
            said = shown_place(now) if now is not None else "not in the census at all"
            differing.append(f"{one.target.name}: predicted {one.shown()}, planned {said}")
    if differing:
        return Filed(state=FILED_DIFFERENTLY, differing=tuple(differing))
    nowhere = tuple(
        f"{one.target.name}: {one.shown()}"
        for one in expected.values()
        if one.place.disposition is not Disposition.ROUTE
    )
    if not plan.applicable():
        return Filed(state=FILED, nowhere=nowhere)
    try:
        membership, report, _gathered, favorites = apply_cli.file_plan(
            cfg, plan, declared, actor=actor, refuse_unplaced=_refuse_unplaced
        )
    except CratekitError as exc:
        return Filed(state=NOT_FILED, nowhere=nowhere, why=exc.cause.message)
    if report.failed:
        return Filed(
            state=NOT_FILED,
            nowhere=nowhere,
            memberships=membership.added,
            why=(
                f"{len(report.failed)} of the landed rows could not be recorded as "
                f"filed: {', '.join(sorted(report.failed))}"
            ),
        )
    return Filed(
        state=FILED,
        nowhere=nowhere,
        filed=len(report.applied) + len(report.already_applied),
        memberships=membership.added,
        favorites=favorites,
    )


def _refuse_unplaced(membership: Any) -> None:
    """Refuse before the ledger is marked when a landed row could not be placed in the tree.

    The adopt worker's own rule (R-148), without its artifact: a landing has
    no job to commit one under, and its envelope carries the rows instead.
    """
    if not membership.skipped:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} landed row(s) could not be placed in the library tree, "
        f"so nothing was recorded as filed: {', '.join(unplaced)}",
        origin=_ORIGIN,
        detail={"unplaced": unplaced},
    )


def warnings(filed: Filed) -> list[dict[str, str]]:
    """What a landing says about its filing, when there is something to say."""
    if filed.state == FILED_DIFFERENTLY:
        return [
            {
                "code": FILED_DIFFERENTLY_WARNING,
                "message": (
                    f"the rows landed and none was filed, because adoption plans "
                    f"{len(filed.differing)} of them differently from what this "
                    f"landing's answer approved: {'; '.join(filed.differing)}; run "
                    f"{ADOPT_APPLY} to file them as they are planned now"
                ),
            }
        ]
    if filed.state == NOT_FILED:
        return [
            {
                "code": NOT_FILED_WARNING,
                "message": (
                    f"the rows landed and were not filed: {filed.why}; run "
                    f"{ADOPT_APPLY} to file them"
                ),
            }
        ]
    return []


__all__ = [
    "ADOPT_APPLY",
    "FILED",
    "FILED_DIFFERENTLY",
    "FILED_DIFFERENTLY_WARNING",
    "NOTHING_TO_FILE",
    "NOT_FILED",
    "NOT_FILED_WARNING",
    "Filed",
    "Prediction",
    "fact",
    "file_landed",
    "identity",
    "predict",
    "shown_place",
    "warnings",
]
