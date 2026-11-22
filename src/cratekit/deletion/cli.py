"""``crate delete review``: offer removals, then trash the confirmed files.

R35 presents removals with resolved path and size; R34 makes the confirm gate a
separate recorded act. This is the shell over ``run``; nothing here is a second
proof. The conformance fixture supplies a disposable database
(``CRATEKIT_TEST_DB``), and ``open_db`` tells an encrypted live database from a
plain synthetic one by its header (R-239), so one handler opens both.

Layer note: MODULES. It imports ``cratekit.cli.output`` and nothing else from the
command-line layer, as ``tombstone_cli`` does.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import config, rb_writer, review
from cratekit.core.cause import Outcome
from cratekit.deletion import run


def _open(cfg: config.Config) -> Any:
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)


def _plan_digest(found: run.Plan) -> str:
    """Digest the files being confirmed, not the watermark state.

    A first run baselines inside ``plan`` before the gate, so a digest carrying
    ``baselined`` would be stale on the resume of every first run.
    """
    return digest_of(
        {
            "kind": "delete.review",
            "database_identity": found.database_identity,
            "deletable": [
                {
                    "id": item.row.content_id,
                    "path": item.resolved or item.row.recorded,
                    "size": item.observed_size,
                }
                for item in found.deletable
            ],
        }
    )


def _item_payload(item: review.Item) -> dict[str, Any]:
    return {
        "id": item.item_id,
        "queue": str(item.queue),
        "kind": item.kind,
        "verdict": str(item.verdict) if item.verdict is not None else None,
        "option": item.option,
        "path": item.payload.get("path", ""),
        "size": item.payload.get("size"),
    }


def _payload(cfg: config.Config, items: tuple[review.Item, ...]) -> dict[str, Any]:
    with review.open_store(cfg) as store:
        outstanding = review.count_unresolved(store, queue=review.Queue.DELETION)
    return {
        "queue": str(review.Queue.DELETION),
        "items": [_item_payload(item) for item in items],
        "unresolved": outstanding,
    }


def build_review(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    parser.add_argument(
        "--actor",
        default="cli",
        help="who is confirming or declining; recorded on the decision (R34)",
    )
    parser.set_defaults(_handler=review_removals)


def _shown(found: run.Plan) -> dict[str, Any]:
    """What the refusal puts in front of the person, beside the question (R-134).

    A first run has already accepted prior removals as history before anybody is
    asked, and aborting does not undo that, so the screen says so. Display only:
    ``_plan_digest`` never reads it.
    """
    shown: dict[str, Any] = {
        "baselined": found.baselined,
        "accepted_as_history": found.baselined_over,
        "offered": len(found.deletable),
    }
    # The rows the proof excused as naming no local file (U243), so the person
    # approving sees the size of that claim.
    ignored = found.references.ignored if found.references is not None else 0
    if ignored:
        shown["ignored, not local files"] = ignored
    # And the landings read as rolled back (R-1844), whose files are kept: one
    # whose playlist and rows were all removed by hand reads the same as one a
    # restore took away.
    if found.rolled_back:
        shown["landings read as rolled back"] = found.rolled_back
    return shown


def review_removals(ctx) -> Envelope:
    """Read the collection, offer what is deletable, then honour the confirm gate.

    The plan is built before the gate, whose digest it is; an empty or first
    run plan still asks (conformance 3). Apply runs only when something is
    deletable, through ``run.apply``, which rebuilds the plan under the session
    gates. Inline by design (U60): a detached child would rebuild a plan nobody
    digested.
    """
    cfg = load_config(("deletion.cli",))
    spec = ctx.entry.gates[0]
    handle = _open(cfg)
    try:
        found = run.plan(cfg, handle, actor=ctx.args.actor)
        offered = run.present(cfg, found, handler_key=ctx.entry.handler_key)
        option = ctx.gate.require(spec, digest=_plan_digest(found), context=_shown(found))
        if option == "abort":
            return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.NO_OP)
        if found.baselined or not found.deletable:
            return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.OK)
        # The gate confirms the offered set: apply moves only items with a
        # verdict, so accept every unanswered one and honour a recorded reject.
        with review.open_store(cfg) as store:
            for item in offered:
                if item.verdict is None:
                    review.resolve(
                        store, item.item_id, review.Verdict.ACCEPTED, actor=ctx.args.actor
                    )
        run.apply(cfg, handle, actor=ctx.args.actor)
        return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.OK)
    finally:
        rb_writer.close_db(handle)


__all__ = ["build_review", "review_removals"]
