"""``label.prune``: take dropped tracks off a label's year playlists (R-836).

``label playlists`` builds a followed label's folder of year playlists and adds,
never removes. This verb is the other half: it plans which tracks each year
playlist this product CREATED should no longer hold, a release the genre gate
now holds or the catalogue no longer confirms, shows every one of them by
artist and title at one explicit gate, and on ``apply`` takes them off. A year
playlist adopted from the account is said and left alone. The planning and
the apply are :mod:`cratekit.modules.outbound.prune`'s.

THE CATALOGUE IS READ AS ``label playlists`` READS IT, through
:func:`cratekit.label.playlists_cli.read_catalogue`, so a catalogue read in
part is refused before the gate the same way, ``label-playlists-incomplete``.
The holds are the review database's, which is local.

A LABEL THAT IS NOT FOLLOWED IS A PLAN OF NOTHING, still gated, decided before
a credential is asked for, on ``label playlists``' precedent.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import review
from cratekit.core.cause import Outcome
from cratekit.core.review import Queue
from cratekit.label import catalogue, playlists_cli
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.modules.outbound import prune

_ORIGIN = ("label.prune",)


def build_prune(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )
    parser.set_defaults(_handler=label_prune)


def held_releases(cfg, label_id: str) -> frozenset[str]:
    """The releases of one label the genre gate holds in force, by identifier."""
    with review.open_store(cfg) as store:
        held = review.holds(store, queue=Queue.LABEL_RELEASE, group=label_id)
    return frozenset(one for one in (genre_gate.hold_release_id(h) for h in held) if one)


def label_prune(ctx) -> Envelope:
    cfg = label_cli._load()
    name = str(ctx.args.name)
    entry = labels.RegistryStore().load().resolve(name)
    planned: prune.Plan | None = None
    remote = None
    if entry is not None:
        from cratekit.modules.outbound import account

        found = catalogue.resolve(cfg)
        read = playlists_cli.read_catalogue(cfg, entry, found)
        held = held_releases(cfg, entry.label_id)
        remote = account.resolve(cfg)
        planned = prune.plan_label(cfg, read, held, remote)
    subject = entry.label_id if entry is not None else name
    payload = prune.payload(planned, kind=prune.LABEL, subject=subject, digest=digest_of)
    shown = (
        {"label": entry.name if entry is not None else name, **prune.shown(planned)}
        if planned is not None
        else {"label": name, "nothing to take off": playlists_cli.NOT_FOLLOWED_SAID}
    )
    # AN EMPTY PLAN STILL ASKS, so a person always sees what the prune judged.
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
    if planned is None:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": "label-playlists-not-followed",
                    "message": f"{name}: {playlists_cli.NOT_FOLLOWED_SAID}",
                }
            ],
        )
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    done = prune.Pruned()
    try:
        prune.apply(cfg, remote, planned, done)
    except Exception as exc:
        raise prune.failed_part_way(
            exc,
            done,
            origin=_ORIGIN,
            again="run crate label prune again; what was taken off is recorded and never asked twice",
        ) from exc
    return prune.finished(ctx, payload, planned, done)


__all__ = ["build_prune", "held_releases", "label_prune"]
