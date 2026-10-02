"""``label.held``: what the genre gate is holding back, and the way to get one back.

R-798. A label sweep judges each release it is about to file by what a general
catalogue publishes for its tracks, and holds back one that is not the kind of
music its label is followed for. A held release is not in review and is not
rejected. This verb is where a person sees them: every held release with the
reason it was held, counted per label, and ``return`` to file one for review
after all.

IT ALSO SAYS WHAT THE NEWEST SWEEP OF EACH LABEL COULD NOT JUDGE. The sweep's
worker has no warning channel, so what its gate did is read back here from what
it left: the holds it made and the gate's answer on each release it filed. A
sweep whose every question to the general catalogue went unread held nothing,
and this verb says that as a failing line, because a count of zero held reads
exactly like a label with nothing to hold.

RETURNING IS A PERSON OVERRULING THE GATE. The release is filed with the payload
the sweep would have filed, marked as returned, and its hold is kept and marked
too, so neither a later sweep nor ``label approved`` holds it again. Nothing is
downloaded: the release waits in review like any other.

A RELEASE ALREADY IN REVIEW CAN BE RETURNED TOO. ``label approved`` judges an
accepted release by the same rule and holds one of another kind, and that
release was never held by a sweep: it was filed before the gate existed, or
filed unjudged. Returning it records the same mark, so the next
``label approved`` lists it. Without this the only way back was to change the
kind of its whole label.

Not a confirm gate and not destructive. ``list`` writes nothing. ``return``
files one review item per release named and changes one hold's state.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import review, routing
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.review import Queue
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.label import sweep
from cratekit.sync import run
from cratekit.tagging import published, searchers
from cratekit.tagging.tag import NO_ISRC

LIST = "list"
RETURN = "return"


def build_held(parser, entry) -> None:
    parser.add_argument(
        "action",
        nargs="?",
        default=LIST,
        choices=(LIST, RETURN),
        help=(
            "list (default) the releases the genre gate is holding back, or "
            "return the named ones to review"
        ),
    )
    parser.add_argument(
        "releases",
        nargs="*",
        metavar="RELEASE_ID",
        help="with return, the release identifiers to file for review",
    )
    parser.set_defaults(_handler=label_held)


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.held.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _release_id(held: review.Hold) -> str:
    return genre_gate.hold_release_id(held)


def _named(held: review.Hold) -> str:
    """One held release as a person names it: identifier, title, artist, label."""
    said = f"release {_release_id(held) or '(no identifier)'}"
    title = str(held.payload.get("title") or "")
    artist = str(held.payload.get("artist") or "")
    if title:
        said += f" ({title!r}" + (f" by {artist}" if artist else "") + ")"
    return said + (f" on {held.name}" if held.name else "")


def _words(held: review.Hold) -> str:
    """The catalogue's words a hold was made on, as one phrase, for counting by."""
    genres = genre_gate.recorded_genres(held.detail, "genres")
    return ", ".join(genres) if genres else "words this build could not read back"


def _label_rows(held: Sequence[review.Hold]) -> list[dict[str, Any]]:
    """One row per label with a hold in force: how many, and called what."""
    rows: dict[str, dict[str, Any]] = {}
    for one in held:
        row = rows.setdefault(
            one.group, {"label_id": one.group, "label_name": one.name, "held": 0, "called": {}}
        )
        row["held"] += 1
        words = _words(one)
        row["called"][words] = row["called"].get(words, 0) + 1
    return sorted(rows.values(), key=lambda row: str(row["label_name"]).casefold())


def _sweep_rows(store: review.ReviewStore) -> list[dict[str, Any]]:
    """What the gate did in the NEWEST recorded sweep of each label.

    Read off what that sweep left, because it had nowhere to say it: the items
    it filed carry the gate's answer, and the holds it first made carry its
    run. ``asked`` counts the releases the general catalogue was asked about,
    ``unread`` the ones it could not be read for, and ``not_judged`` every
    filed release the gate gave no verdict on, whatever the reason.

    A LABEL WITH NO RECORDED ROUND HAS NO ROW. Its items were filed before
    rounds were recorded, and nothing says which sweep was its newest.
    """
    newest: dict[str, review.Round] = {}
    for found in review.rounds(store, queue=str(Queue.LABEL_RELEASE)):
        newest[found.group] = found
    if not newest:
        return []
    rows = {
        group: {
            "label_id": group,
            "label_name": found.name,
            "run": found.run_id,
            "filed": 0,
            "asked": 0,
            "not_judged": 0,
            "unread": 0,
            "held": 0,
        }
        for group, found in newest.items()
    }
    cursor: int | None = None
    while True:
        page = review.list_items(
            store,
            queue=str(Queue.LABEL_RELEASE),
            kinds=(sweep.KIND,),
            include_resolved=True,
            limit=review.DEFAULT_PAGE,
            after=cursor,
        )
        for item in page.items:
            row = rows.get(str(item.payload.get("label_id") or ""))
            if row is None or item.payload.get(sweep.SWEEP_RUN) != row["run"]:
                continue
            row["filed"] += 1
            # NOT JUDGED IS A FACT ABOUT THE RELEASE AS IT STANDS, whoever
            # stamped it, so it is counted first and for every item.
            if item.payload.get(genre_gate.GATE_FIELD) == routing.KindVerdict.NOT_JUDGED.value:
                row["not_judged"] += 1
            # WHAT ``label judge`` WAS TOLD LATER IS NOT WHAT THIS SWEEP ASKED.
            # A stamp naming a judging job was written after the sweep, over a
            # release the sweep may never have asked about, and counting its
            # answer here would put that job's unread catalogue in a sentence
            # about the sweep (R-815).
            if item.payload.get(genre_gate.GATE_RUN_FIELD):
                continue
            answer = item.payload.get(genre_gate.GATE_ANSWER_FIELD)
            # A RELEASE WITH NO ISRC WAS NOT ASKED ABOUT. Counting it would let
            # one such release hide a sweep whose every real question went
            # unread, since unread would no longer equal asked.
            if answer is not None and answer not in (searchers.NOT_ASKED, NO_ISRC):
                row["asked"] += 1
            if answer in published.UNREAD:
                row["unread"] += 1
        if page.next_cursor is None:
            break
        cursor = page.next_cursor
    for one in review.holds(store, queue=str(Queue.LABEL_RELEASE)):
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
    return _check(
        f"sweep.{row['label_id']}",
        "info",
        f"the newest sweep of {name} filed {row['filed']} release(s) and the genre "
        f"gate could not judge {row['not_judged']} of them"
        + (
            f", {row['unread']} because the general catalogue could not be read"
            if row["unread"]
            else ""
        )
        + "; each says why in: crate review list --queue label-release",
    )


def _unfollowed(held: Sequence[review.Hold]) -> frozenset[str]:
    """The labels with a hold in force that the registry no longer holds.

    A hold is judged again only by a sweep of its label, so one on a label
    nobody follows any more stands until a person returns it, and its line
    says so. AN UNREADABLE REGISTRY NAMES NONE: this is a note on a listing,
    and the registry's own verbs are where that refusal belongs.
    """
    try:
        followed = labels.RegistryStore().load()
    except CratekitError:
        return frozenset()
    return frozenset(one.group for one in held if followed.by_id(one.group) is None)


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
        *(
            _check(
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
            for one in held
        ),
        *(line for line in map(_sweep_check, sweeps) if line is not None),
    ]
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {
                "held": len(held),
                "labels": by_label,
                "releases": [
                    {
                        "release_id": _release_id(one),
                        "item_id": one.item_id,
                        "label_id": one.group,
                        "label_name": one.name,
                        "title": one.payload.get("title"),
                        "artist": one.payload.get("artist"),
                        "genres": list(genre_gate.recorded_genres(one.detail, "genres") or ()),
                        "kind": one.detail.get("kind"),
                        "reason": one.reason,
                        "run": one.run_id or None,
                    }
                    for one in held
                ],
                "sweeps": sweeps,
            },
        },
        outcome=Outcome.OK if held else Outcome.NO_OP,
    )


def _returned(ctx) -> Envelope:
    wanted = [str(one).strip() for one in ctx.args.releases if str(one).strip()]
    if not wanted:
        raise refuse(
            "review-selection-invalid",
            "label held return needs the release to return, and returning nothing "
            "would report a release filed that never was",
            steps=("pass a release identifier from: crate label held",),
            origin=("label.held",),
        )
    cfg = label_cli._load()
    queue = str(Queue.LABEL_RELEASE)
    checks: list[dict[str, Any]] = []
    filed: list[str] = []
    marked: list[str] = []
    already: list[str] = []
    with review.open_store(cfg) as store:
        # EVERY NAME IS RESOLVED BEFORE ANYTHING IS FILED, so one mistyped
        # identifier refuses the run with nothing changed, not after the
        # releases named before it were already returned. A name is a hold, or
        # failing that a release already in review.
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
                f"no release named {', '.join(repr(one) for one in unknown)} is held "
                f"by the genre gate or waiting in review, so there is nothing to "
                f"return; nothing was filed",
                steps=(
                    "take the identifier from: crate label held",
                    "or from the held line of: crate label approved",
                ),
                origin=("label.held",),
                detail={"unknown": unknown},
            )
        for release_id, one in found.items():
            if isinstance(one, review.Item):
                # IN REVIEW AND NEVER HELD BY A SWEEP. Nothing to file: the
                # mark is made, already returned, in one write.
                made = review.hold(
                    store,
                    queue=queue,
                    kind=sweep.KIND,
                    identity={"release_id": release_id},
                    payload=dict(one.payload),
                    group=str(one.payload.get("label_id") or ""),
                    name=str(one.payload.get("label_name") or ""),
                    reason="returned by hand while it was in review",
                    detail={},
                    run_id=str(one.payload.get(sweep.SWEEP_RUN) or ""),
                    returned=True,
                )
                marked.append(release_id)
                checks.append(
                    _check(
                        f"release.{release_id}",
                        "ok",
                        f"{_named(made)} is already in review as {one.item_id}; it is "
                        f"marked returned, so crate label approved will not hold it",
                    )
                )
                continue
            if one is None:
                continue
            if one.state == review.HOLD_RETURNED:
                already.append(release_id)
                checks.append(
                    _check(
                        f"release.{release_id}",
                        "ok",
                        f"{_named(one)} was already returned to review; nothing changed",
                    )
                )
                continue
            # THE OFFER FIRST, THEN THE MARK. A hold marked returned whose item
            # was never filed is a release nothing holds and nothing offers.
            # A RELEASE TAKEN BACK OUT OF REVIEW GOES BACK AS IT WAS FILED
            # (R-815): under the run its payload names, and under none when it
            # names none, as an item filed before runs were recorded reads.
            # Never under the hold's own run, which is the judging job and
            # filed nothing. A release a sweep held was never filed, and takes
            # the sweep that held it. The word that says it was taken back is
            # the hold's, and does not travel onto the item.
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
            filed.append(release_id)
            checks.append(
                _check(
                    f"release.{release_id}",
                    "ok",
                    f"{_named(one)} is filed for review as {item.item_id} and will "
                    f"not be held again; decide it with: crate review list --queue "
                    f"{Queue.LABEL_RELEASE}",
                )
            )
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {"returned": filed, "marked": marked, "already_returned": already},
        },
        outcome=Outcome.OK if filed or marked else Outcome.NO_OP,
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
            origin=("label.held",),
        )
    return _listed(ctx)


__all__ = ["LIST", "RETURN", "build_held", "label_held"]
