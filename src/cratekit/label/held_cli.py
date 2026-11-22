"""``label.held``: what the genre gate is holding back, and the way to get one back.

R-798. A sweep holds back a release that is not the kind of music its label is
followed for: neither in review nor rejected. This verb lists every hold with
its reason, counted per label, and ``return`` files one for review after all.

IT ALSO SAYS WHAT THE NEWEST SWEEP OF EACH LABEL COULD NOT JUDGE, read back
from what the sweep left, since its worker has no warning channel. A sweep
whose every question went unread is a failing line, because zero held reads
exactly like a label with nothing to hold.

RETURNING IS A PERSON OVERRULING THE GATE. The release is filed with the
payload the sweep would have filed, marked returned, and its hold is kept and
marked too, so neither a later sweep nor ``label approved`` holds it again.
A release already in review (held by ``label approved``, never by a sweep)
can be returned too, and takes the same mark.

Not a confirm gate and not destructive. ``list`` writes nothing. ``return``
files one review item per release named and changes one hold's state.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import partial
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import review, routing
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.review import Queue
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.label import review_common, sweep
from cratekit.sync import run
from cratekit.tagging import published, searchers
from cratekit.tagging.tag import NO_ISRC

LIST = "list"
RETURN = "return"
ORIGIN = ("label.held",)

_check = partial(review_common.check, "label.held")
_release_id = genre_gate.hold_release_id


def build_held(parser, entry) -> None:
    parser.add_argument(
        "action", nargs="?", default=LIST, choices=(LIST, RETURN),
        help=(
            "list (default) the releases the genre gate is holding back, or "
            "return the named ones to review"
        ),
    )
    parser.add_argument(
        "releases", nargs="*", metavar="RELEASE_ID",
        help="with return, the release identifiers to file for review",
    )
    parser.set_defaults(_handler=label_held)


def _named(held: review.Hold) -> str:
    title, artist = (str(held.payload.get(name) or "") for name in ("title", "artist"))
    return review_common.named(_release_id(held), title, held.name, artist)


def _genres(held: review.Hold) -> tuple[str, ...] | None:
    return genre_gate.recorded_genres(held.detail, "genres")


def _label_rows(held: Sequence[review.Hold]) -> list[dict[str, Any]]:
    """One row per label with a hold in force: how many, and called what."""
    rows: dict[str, dict[str, Any]] = {}
    for one in held:
        row = rows.setdefault(
            one.group, {"label_id": one.group, "label_name": one.name, "held": 0, "called": {}}
        )
        row["held"] += 1
        genres = _genres(one)
        words = ", ".join(genres) if genres else "words this build could not read back"
        row["called"][words] = row["called"].get(words, 0) + 1
    return sorted(rows.values(), key=lambda row: str(row["label_name"]).casefold())


def _sweep_rows(store: review.ReviewStore) -> list[dict[str, Any]]:
    """What the gate did in the NEWEST recorded sweep of each label.

    Read off what that sweep left: its items carry the gate's answer, its holds
    its run. A label with no recorded round has no row.
    """
    queue = str(Queue.LABEL_RELEASE)
    newest = {found.group: found for found in review.rounds(store, queue=queue)}
    if not newest:
        return []
    zero = dict.fromkeys(("filed", "asked", "not_judged", "unread", "held"), 0)
    rows = {
        group: {"label_id": group, "label_name": found.name, "run": found.run_id, **zero}
        for group, found in newest.items()
    }
    cursor: int | None = None
    while True:
        page = review.list_items(
            store, queue=queue, kinds=(sweep.KIND,), include_resolved=True,
            limit=review.DEFAULT_PAGE, after=cursor,
        )
        for item in page.items:
            row = rows.get(str(item.payload.get("label_id") or ""))
            if row is None or item.payload.get(sweep.SWEEP_RUN) != row["run"]:
                continue
            row["filed"] += 1
            # Not judged is a fact about the release as it stands, whoever stamped it.
            if item.payload.get(genre_gate.GATE_FIELD) == routing.KindVerdict.NOT_JUDGED.value:
                row["not_judged"] += 1
            # A stamp naming a judging job was written after the sweep, and its
            # answer is not what this sweep asked (R-815).
            if item.payload.get(genre_gate.GATE_RUN_FIELD):
                continue
            answer = item.payload.get(genre_gate.GATE_ANSWER_FIELD)
            # A release with no ISRC was not asked about; counting it would hide
            # a sweep whose every real question went unread.
            if answer is not None and answer not in (searchers.NOT_ASKED, NO_ISRC):
                row["asked"] += 1
            if answer in published.UNREAD:
                row["unread"] += 1
        if page.next_cursor is None:
            break
        cursor = page.next_cursor
    for one in review.holds(store, queue=queue):
        row = rows.get(one.group)
        if row is not None and one.run_id == row["run"]:
            # A release held in this sweep was asked about and answered.
            row["held"] += 1
            row["asked"] += 1
    return sorted(rows.values(), key=lambda row: str(row["label_name"]).casefold())


def _sweep_check(row: dict[str, Any]) -> dict[str, Any] | None:
    """The line for one label's newest sweep, or None when the gate judged it all."""
    name = row["label_name"] or row["label_id"]
    if row["asked"] and row["unread"] == row["asked"]:
        return _check(
            f"sweep.{row['label_id']}",
            "fail",
            f"the general catalogue could not be read for any of the {row['asked']} "
            f"release(s) the newest sweep of {name} asked it about, so the genre gate "
            f"judged none of them and HELD NOTHING; they are in review, not judged, "
            f"and are judged when accepted, by: crate label approved",
        )
    if not row["not_judged"]:
        return None
    unread = (
        f", {row['unread']} because the general catalogue could not be read"
        if row["unread"] else ""
    )
    return _check(
        f"sweep.{row['label_id']}",
        "info",
        f"the newest sweep of {name} filed {row['filed']} release(s) and the genre "
        f"gate could not judge {row['not_judged']} of them{unread}"
        "; each says why in: crate review list --queue label-release",
    )


def _unfollowed(held: Sequence[review.Hold]) -> frozenset[str]:
    """The labels with a hold in force that the registry no longer holds.

    No sweep judges such a hold again, so its line says so. An unreadable
    registry names none: this is a note on a listing, and the refusal belongs
    to the registry's own verbs.
    """
    try:
        followed = labels.RegistryStore().load()
    except CratekitError:
        return frozenset()
    return frozenset(one.group for one in held if followed.by_id(one.group) is None)


def _held_line(one: review.Hold, unfollowed: frozenset[str]) -> dict[str, Any]:
    return _check(
        f"release.{_release_id(one) or one.item_id}",
        "info",
        f"{_named(one)} is held: {one.reason}; file it for review with: "
        f"crate label held return {_release_id(one) or 'RELEASE_ID'}"
        + (
            "; its label is no longer followed, so no sweep will judge it again"
            if one.group in unfollowed
            else ""
        ),
    )


def _listed(ctx) -> Envelope:
    cfg = label_cli._load()
    with review.open_store(cfg) as store:
        held = review.holds(store, queue=str(Queue.LABEL_RELEASE))
        sweeps = _sweep_rows(store)
    unfollowed = _unfollowed(held)
    by_label = _label_rows(held)
    checks = [
        _check(
            "held",
            "info" if held else "ok",
            f"{len(held)} release(s) held by the genre gate across {len(by_label)} "
            f"label(s); none of them is in review and none is rejected"
            if held
            else "no release is held by the genre gate",
        ),
        *(
            _check(
                f"label.{row['label_id']}",
                "info",
                f"{row['label_name'] or row['label_id']}: {row['held']} held, "
                + "; ".join(
                    f"{count} the general catalogue calls {words}"
                    for words, count in row["called"].items()
                ),
            )
            for row in by_label
        ),
        *(_held_line(one, unfollowed) for one in held),
        *(line for line in map(_sweep_check, sweeps) if line is not None),
    ]
    releases = [
        {
            "release_id": _release_id(one),
            "item_id": one.item_id,
            "label_id": one.group,
            "label_name": one.name,
            "title": one.payload.get("title"),
            "artist": one.payload.get("artist"),
            "genres": list(_genres(one) or ()),
            "kind": one.detail.get("kind"),
            "reason": one.reason,
            "run": one.run_id or None,
        }
        for one in held
    ]
    summary = {"held": len(held), "labels": by_label, "releases": releases, "sweeps": sweeps}
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if held else Outcome.NO_OP,
    )


def _found(store: review.ReviewStore, wanted: list[str]) -> dict[str, review.Hold | review.Item]:
    """Every name as a hold, or failing that a release in review, or refused.

    EVERY NAME IS RESOLVED BEFORE ANYTHING IS FILED, so one mistyped
    identifier refuses the run with nothing changed.
    """
    queue = str(Queue.LABEL_RELEASE)
    found: dict[str, review.Hold | review.Item | None] = {}
    for release_id in dict.fromkeys(wanted):
        item_id = genre_gate.release_item_id(release_id)
        found[release_id] = review.find_hold(
            store, queue=queue, item_id=item_id
        ) or review.find(store, item_id)
    unknown = [release_id for release_id, one in found.items() if one is None]
    if unknown:
        raise refuse(
            "review-item-unknown",
            f"no release named {review_common.quoted(unknown)} is held "
            f"by the genre gate or waiting in review, so there is nothing to "
            f"return; nothing was filed",
            steps=(
                "take the identifier from: crate label held",
                "or from the held line of: crate label approved",
            ),
            origin=ORIGIN,
            detail={"unknown": unknown},
        )
    return {release_id: one for release_id, one in found.items() if one is not None}


def _return_one(
    store: review.ReviewStore, release_id: str, one: review.Hold | review.Item
) -> tuple[str, str]:
    """Return one release. Which summary list it joins, and its line's words."""
    queue = str(Queue.LABEL_RELEASE)
    if isinstance(one, review.Item):
        # In review and never held by a sweep: the mark is made, already
        # returned, in one write.
        filed = one.payload
        made = review.hold(
            store, queue=queue, kind=sweep.KIND, identity={"release_id": release_id},
            payload=dict(filed), group=str(filed.get("label_id") or ""),
            name=str(filed.get("label_name") or ""),
            reason="returned by hand while it was in review", detail={},
            run_id=str(filed.get(sweep.SWEEP_RUN) or ""), returned=True,
        )
        return "marked", (
            f"{_named(made)} is already in review as {one.item_id}; it is "
            f"marked returned, so crate label approved will not hold it"
        )
    if one.state == review.HOLD_RETURNED:
        return "already_returned", f"{_named(one)} was already returned to review; nothing changed"
    # THE OFFER FIRST, THEN THE MARK: a hold marked returned whose item was never
    # filed is a release nothing holds and nothing offers. A release taken back
    # out of review goes back as it was filed (R-815), under the run its payload
    # names or none, never under the hold's own run, which filed nothing. A
    # release a sweep held takes that sweep. The withheld word stays on the hold.
    taken_back = bool(one.payload.get(review.WITHHELD_FIELD))
    payload = {
        **{k: v for k, v in one.payload.items() if k != review.WITHHELD_FIELD},
        **genre_gate.returned_stamp(),
    }
    item = sweep.offer_release(
        store,
        run.Candidate(identity=release_id, recency="", payload=payload),
        run_id=str(payload.get(sweep.SWEEP_RUN) or "")
        or (None if taken_back else one.run_id or None),
    )
    review.return_hold(store, queue=queue, item_id=one.item_id)
    return "returned", (
        f"{_named(one)} is filed for review as {item.item_id} and will "
        f"not be held again; decide it with: crate review list --queue "
        f"{Queue.LABEL_RELEASE}"
    )


def _returned(ctx) -> Envelope:
    wanted = review_common.wanted(ctx.args.releases)
    if not wanted:
        raise refuse(
            "review-selection-invalid",
            "label held return needs the release to return, and returning nothing "
            "would report a release filed that never was",
            steps=("pass a release identifier from: crate label held",),
            origin=ORIGIN,
        )
    cfg = label_cli._load()
    checks: list[dict[str, Any]] = []
    summary: dict[str, list[str]] = {"returned": [], "marked": [], "already_returned": []}
    with review.open_store(cfg) as store:
        for release_id, one in _found(store, wanted).items():
            joins, said = _return_one(store, release_id, one)
            summary[joins].append(release_id)
            checks.append(_check(f"release.{release_id}", "ok", said))
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if summary["returned"] or summary["marked"] else Outcome.NO_OP,
    )


def label_held(ctx) -> Envelope:
    """List what the genre gate holds, or return the named releases to review."""
    if ctx.args.action == RETURN:
        return _returned(ctx)
    if ctx.args.releases:
        raise refuse(
            "review-selection-invalid",
            "label held lists every held release and takes no release to list; "
            "ignoring the ones named would read as a listing of them",
            steps=("drop the identifiers, or use: crate label held return RELEASE_ID",),
            origin=ORIGIN,
        )
    return _listed(ctx)


__all__ = ["LIST", "RETURN", "build_held", "label_held"]
