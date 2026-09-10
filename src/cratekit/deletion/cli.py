"""``crate delete review``: offer removals, then trash the confirmed files.

R35 presents removals with resolved path and size. R34 makes the confirm
gate a separate recorded act. This module is the shell that puts those two
sentences on a command a person can type. The engine in ``run`` already did
the work; nothing here invents a second proof.

WHY THIS CAN LAND NOW. The explicit-gate wall is down: conformance 3 answers
an explicit gate with R34's two acts. What remained was the database. This
verb reads the collection, so it cannot exit OK on a machine with no
rekordbox database. The conformance fixture now substitutes a disposable
database (the ``CRATEKIT_TEST_DB`` convention: a supplied snapshot wins,
otherwise a synthetic file is built), so the battery runs either way.

UNLOCK. A live rekordbox database is encrypted and needs the key. The
synthetic fixture is plain SQLite and the canary cannot read it with the key
on. The header tells the two apart, so the same handler opens both.

Layer note: MODULES. Same shape as ``tombstone_cli``: it imports
``cratekit.cli.output`` and nothing else from the command-line layer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, rb_writer, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.deletion import run

_SQLITE_HEADER = b"SQLite format 3"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("deletion.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _needs_unlock(path: Path) -> bool:
    """True when the file is encrypted, so the binding must supply the key."""
    try:
        return not path.read_bytes()[:16].startswith(_SQLITE_HEADER)
    except OSError:
        return True


def _open(cfg: config.Config) -> Any:
    target = rb_writer.live_db_path(cfg)
    return rb_writer.open_db(target, unlock=_needs_unlock(target), cfg=cfg)


def _plan_digest(found: run.Plan) -> str:
    """Digest the files being confirmed, not the watermark state.

    A first run baselines inside ``plan`` before the gate returns. If the
    digest carried ``baselined``, the recorded decision would be stale on
    resume of every first run, which is the one run that must succeed.
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

    A first run baselines inside ``plan``, before the gate can refuse, so by the
    time anybody is asked "move these files to the Trash?" the prior removals are
    already accepted as history. Aborting does not undo that, and R35 wants the
    baseline, so what this fixes is that it was SILENT: the refusal now says so.

    A display value and never an input: ``_plan_digest`` does not read it, so a
    first run's recorded decision is not stale on the resume that no longer
    baselines.
    """
    return {
        "baselined": found.baselined,
        "accepted_as_history": found.baselined_over,
        "offered": len(found.deletable),
    }


def review_removals(ctx) -> Envelope:
    """Read the collection, offer what is deletable, then honour the confirm gate.

    THE PLAN IS BUILT BEFORE THE GATE, because the gate's digest is the plan.
    An empty or first-run baseline still asks the gate: conformance 3 holds
    every declared gate to firing, and "nothing to trash" is a plan a person
    can still abort.

    APPLY RUNS ONLY WHEN THERE IS SOMETHING DELETABLE. A baseline writes the
    watermark inside ``plan`` and must not open a destructive session to move
    zero files. Confirmed files go through ``run.apply``, which rebuilds the
    plan under the session gates and re-checks every precondition.

    INLINE, AND THAT IS THE DESIGN RATHER THAN A MISSING WORKER (U60). Nothing
    here enqueues and the registry entry no longer claims otherwise. The person
    who confirmed the set watches it go; a detached child would rebuild a plan
    that nobody digested, which is what the explicit gate exists to prevent.
    """
    cfg = _load()
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
        # THE GATE IS THE CONFIRMATION OF THE OFFERED SET. apply only moves
        # items that already have a verdict, so an unanswered offer would
        # make "trash" a no-op. Honour a recorded reject; accept the rest.
        with review.open_store(cfg) as store:
            for item in offered:
                if item.verdict is None:
                    review.resolve(
                        store,
                        item.item_id,
                        review.Verdict.ACCEPTED,
                        actor=ctx.args.actor,
                    )
        run.apply(cfg, handle, actor=ctx.args.actor)
        return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.OK)
    finally:
        rb_writer.close_db(handle)


__all__ = ["build_review", "review_removals"]
