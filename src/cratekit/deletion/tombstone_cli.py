"""``crate tombstone list``: the half of R36 a person can actually reach.

R36 says a tombstone is **listable and revocable**, both about a PERSON. This
verb declares no gate, is not destructive and opens no database, so it is its
own module rather than waiting behind ``delete.review``'s explicit gate.
Revoking lives on the listing verb because nobody revokes an identifier they did
not just read: it is content derived and the listing is the only place to get one.

Layer note: MODULES. It imports ``cratekit.cli.output`` (FOUNDATION by KTD25) and
nothing else of the command-line layer, so the registry row and the context are
taken as plain parameters.
"""

from __future__ import annotations

import argparse
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, review
from cratekit.deletion import run, stores


def build_tombstones(parser: argparse.ArgumentParser, entry: Any) -> None:
    """Declare the surface. ``entry`` is the registry row, taken untyped by layer."""
    parser.add_argument(
        "--all",
        action="store_true",
        help=(
            "include tombstones somebody has already revoked, so a version nobody ever suppressed "
            "can be told from one that was suppressed and lifted"
        ),
    )
    parser.add_argument(
        "--revoke",
        metavar="ID",
        default=None,
        help="lift the tombstone with this identifier, making that version acquirable again",
    )
    parser.add_argument(
        "--actor",
        default="cli",
        help="who is lifting the suppression; recorded on the revocation (R34)",
    )
    parser.set_defaults(_handler=tombstones)


def tombstones(ctx: Any) -> Envelope:
    """List the tombstones, having first lifted one if asked to.

    The revocation goes through ``run.revoke``, so a decline identifier reaches
    the decline store's handling and one that resolves nowhere gets the store's
    own sentence. After a revocation the listing includes revoked records, so
    the one just lifted is shown.
    """
    cfg = config.load()
    lifted = None
    if ctx.args.revoke:
        lifted = run.revoke(cfg, ctx.args.revoke, actor=ctx.args.actor)

    records = stores.list_tombstones(cfg, include_revoked=bool(ctx.args.all) or lifted is not None)
    with review.open_store(cfg) as store:
        outstanding = review.count_unresolved(store, queue=review.Queue.DELETION)

    return ctx.envelope(
        data={
            # ``unresolved`` is what is OPEN in the deletion queue, never the
            # number of tombstones, which are settled decisions, not a backlog.
            "queue": str(review.Queue.DELETION),
            "items": [dict(stores.summarize(record)) for record in records],
            "unresolved": outstanding,
        }
    )


__all__ = ["build_tombstones", "tombstones"]
