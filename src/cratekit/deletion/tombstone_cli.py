"""``crate tombstone list``: the half of R36 a person can actually reach.

R36 says a tombstone is **listable and revocable**. Both halves of that sentence
are about a PERSON, and until this module existed the whole feature shipped with
no user-facing surface for either: the engine could list and revoke, and nothing
a user could type could ask it to. A requirement satisfied only by an internal
function is a requirement satisfied by nobody, which is the same shape as a
decision store that remembers and offers no way back.

**WHY THIS IS A SECOND MODULE RATHER THAN THE HALF OF ONE.** ``delete.review``
and ``tombstone.list`` were declared against a single module and moved together,
and that was right while neither could land. It stopped being right the moment
one of them could. ``delete.review`` declares an EXPLICIT gate, R34 makes an
explicit gate answerable only by a separate recorded act against the run, and
conformance 3 as written drives the inline answer and then requires exit ``OK``,
so no explicitly gated verb in the registry can land today. NONE of that touches
this verb: it declares no gate at all, so conformance 3's loop over its gates
runs zero times. It is also not destructive, writes no surface, and opens no
database. Keeping it behind its sibling would have withheld the only thing a user
can do about a tombstone in order to preserve a file boundary.

**WHY REVOKING LIVES ON THE LISTING VERB.** They are one act with a pause in the
middle. Nobody revokes an identifier they did not just read, because the
identifier is content-derived and there is nowhere else to get one. A separate
``tombstone revoke`` verb would be a second command whose only legal input is the
first command's output, and R36 names the two together in one sentence for the
same reason.

Layer note: MODULES. It imports ``cratekit.cli.output`` and nothing else from
the command-line layer, because that module is FOUNDATION by KTD25: the output
envelope is reserved globally before any verb ships. A verb module living below
the CLI layer may not name the registry or the context type, so the two are taken
as plain parameters. That is the constraint every module-layer verb in this
registry works under, and it costs two annotations.
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
            "include tombstones somebody has already revoked, so a version "
            "nobody ever suppressed can be told from one that was suppressed "
            "and lifted"
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

    THE REVOCATION GOES THROUGH ``run.revoke`` RATHER THAN THE STORE, so one
    identifier resolves the same way whichever surface a person reached it from,
    and so a decline identifier typed here reaches the decline store's own
    handling instead of a refusal that would be true and useless. The refusal for
    an identifier that resolves in neither store comes from the store itself, so
    the sentence is the same wherever a bad identifier arrives.

    THE LISTING AFTER A REVOCATION INCLUDES REVOKED RECORDS whether or not
    ``--all`` was given. The record a person just acted on is the one they need
    to see, and a listing that dropped it would answer "did that work" with
    silence.
    """
    cfg = config.load()
    lifted = None
    if ctx.args.revoke:
        lifted = run.revoke(cfg, ctx.args.revoke, actor=ctx.args.actor)

    records = stores.list_tombstones(
        cfg, include_revoked=bool(ctx.args.all) or lifted is not None
    )
    with review.open_store(cfg) as store:
        outstanding = review.count_unresolved(store, queue=review.Queue.DELETION)

    return ctx.envelope(
        data={
            # The deletion queue, because that is the surface these records came
            # out of and ``review_set`` names one. ``unresolved`` is what is OPEN
            # in that queue and is deliberately not the number of tombstones: a
            # tombstone is a settled decision, and reporting settled decisions as
            # a backlog is how a person concludes they have work they do not.
            "queue": str(review.Queue.DELETION),
            "items": [dict(stores.summarize(record)) for record in records],
            "unresolved": outstanding,
        }
    )


__all__ = ["build_tombstones", "tombstones"]
