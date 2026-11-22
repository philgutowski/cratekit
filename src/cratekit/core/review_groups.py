"""The review queue's rounds and grouping: what a round left unoffered, counted by group (R-790).

Imported back into ``core.review`` at its foot, and only from there.
``list_items`` is read through ``core.review``, so a test that patches it
there reaches this module too.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from cratekit.cli.output import timestamp
from cratekit.core import review as _review
from cratekit.core.cause import Scope, refuse
from cratekit.core.review import (
    DEFAULT_PAGE,
    RUN_FIELD,
    ReviewStore,
    _assert_declared_queue,
)
from cratekit.core.review_holds import holds


@dataclass(frozen=True, slots=True)
class Round:
    """How much one producer's round left unoffered in one group (R-790)."""

    queue: str
    run_id: str
    group: str
    name: str
    beyond: int
    created: str


def record_round(
    store: ReviewStore,
    *,
    queue: str,
    run_id: str,
    group: str,
    name: str,
    beyond: int,
) -> Round:
    """Record what a round left beyond its offer, replacing that run's earlier answer.

    Replaced, not added: a resumed item reruns its round under the same run id.
    """
    declared = _assert_declared_queue(queue)
    now = timestamp()
    with store.immediate() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO offer_rounds "
            "(queue, run_id, group_key, group_name, beyond, created) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (declared, run_id, group, name, int(beyond), now),
        )
    return Round(
        queue=declared, run_id=run_id, group=group, name=name, beyond=int(beyond), created=now
    )


#: What ``review list --group-by`` can group each queue by: the payload field
#: holding a group's key, and the one holding its display name, if any.
GROUPINGS: Mapping[str, Mapping[str, tuple[str, str | None]]] = {
    "label-release": {"label": ("label_id", "label_name"), "run": (RUN_FIELD, None)},
}

#: The kinds a grouping counts when the caller names none, so harvested label
#: names, which carry no label or run, do not form one nameless group.
GROUPED_KINDS: Mapping[str, tuple[str, ...]] = {"label-release": ("label-release",)}


def grouped(
    store: ReviewStore,
    *,
    queue: str,
    by: str,
    kinds: Sequence[str] | None = None,
    include_resolved: bool = False,
    include_suppressed: bool = False,
) -> list[dict[str, Any]]:
    """One row per group of ``queue``, counting the items the same filters list.

    Reads the whole selection a page at a time. Rows also come from recorded
    rounds and holds, so a label with no open items still shows.

    ``beyond`` is the recorded count of releases a round never examined, less
    those read as another label's by copyright line (U238): a label's latest
    round, or a run's sum over its labels; None where nothing was recorded.
    ``held`` counts holds (R-798): a label's in force, or those a run first held.
    """
    declared = _assert_declared_queue(queue)
    fields = GROUPINGS.get(declared, {}).get(by)
    if fields is None:
        raise refuse(
            "review-selection-invalid",
            f"the {declared} queue cannot be grouped by {by!r}; it groups by "
            f"{', '.join(sorted(GROUPINGS.get(declared, {}))) or 'nothing'}",
            steps=("group the label-release queue by label or by run",),
            scope=Scope.RUN, origin=("review",),
            detail={"queue": declared, "group_by": by},
        )
    key_field, name_field = fields
    kinds = kinds or GROUPED_KINDS.get(declared)
    counts: dict[Any, int] = {}
    names: dict[Any, str] = {}
    labels_per_run: dict[Any, set[str]] = {}
    label_key = GROUPINGS[declared].get("label", (None, None))[0]
    cursor: int | None = None
    while True:
        page = _review.list_items(
            store,
            queue=declared,
            kinds=kinds,
            include_resolved=include_resolved,
            include_suppressed=include_suppressed,
            limit=DEFAULT_PAGE,
            after=cursor,
        )
        for item in page.items:
            key = item.payload.get(key_field) or None
            counts[key] = counts.get(key, 0) + 1
            if name_field and item.payload.get(name_field):
                names.setdefault(key, str(item.payload[name_field]))
            if by == "run" and label_key and item.payload.get(label_key):
                labels_per_run.setdefault(key, set()).add(str(item.payload[label_key]))
        if page.next_cursor is None:
            break
        cursor = page.next_cursor
    recorded = rounds(store, queue=declared)
    withheld = holds(store, queue=declared)
    held: dict[Any, int] = {}
    if by == "label":
        latest: dict[Any, Round] = {}
        for found in recorded:
            latest[found.group] = found
            names.setdefault(found.group, found.name)
        for one in withheld:
            key = one.group or None
            held[key] = held.get(key, 0) + 1
            names.setdefault(key, one.name)
        keys = sorted(
            set(counts) | set(latest) | set(held),
            key=lambda k: (names.get(k) or str(k or "")).casefold(),
        )
        return [
            {
                "label": key,
                "label_name": names.get(key, ""),
                "items": counts.get(key, 0),
                "beyond": latest[key].beyond if key in latest else None,
                "swept": latest[key].run_id if key in latest else None,
                "held": held.get(key, 0),
            }
            for key in keys
        ]
    beyond_per_run: dict[Any, int] = {}
    for found in recorded:
        beyond_per_run[found.run_id] = beyond_per_run.get(found.run_id, 0) + found.beyond
        labels_per_run.setdefault(found.run_id, set()).add(found.group)
    for one in withheld:
        key = one.run_id or None
        held[key] = held.get(key, 0) + 1
        if one.group:
            labels_per_run.setdefault(key, set()).add(one.group)
    keys = list(counts) + [key for key in beyond_per_run if key not in counts]
    keys += [key for key in held if key not in keys]
    return [
        {
            "run": key,
            "items": counts.get(key, 0),
            "labels": len(labels_per_run.get(key, set())),
            "beyond": beyond_per_run.get(key),
            "held": held.get(key, 0),
        }
        for key in keys
    ]


def rounds(store: ReviewStore, *, queue: str) -> tuple[Round, ...]:
    """Every recorded round for ``queue``, oldest first."""
    rows = store.conn.execute(
        "SELECT * FROM offer_rounds WHERE queue = ? ORDER BY created, run_id, group_key",
        (_assert_declared_queue(queue),),
    ).fetchall()
    return tuple(
        Round(queue=row["queue"], run_id=row["run_id"], group=row["group_key"],
              name=row["group_name"], beyond=int(row["beyond"]), created=row["created"])
        for row in rows
    )
