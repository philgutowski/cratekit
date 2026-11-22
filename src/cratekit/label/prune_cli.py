"""``label.prune``: take dropped tracks off a label's year playlists (R-836).

The other half of ``label playlists``: plans which tracks each year playlist
this product CREATED should no longer hold (a release the genre gate holds or
the catalogue no longer confirms, or a track the library removed, U243), shows
them at one explicit gate, and on ``apply`` takes them off, by
:mod:`cratekit.modules.outbound.prune`. The catalogue is read as ``label
playlists`` reads it. A label nobody follows is a plan of nothing.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import active_taxonomy, review
from cratekit.core.review import Queue
from cratekit.label import catalogue, playlists_cli
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels

_ORIGIN = ("label.prune",)


def build_prune(parser, entry) -> None:
    del entry
    playlists_cli.label_argument(parser)
    parser.set_defaults(_handler=label_prune)


def held_releases(cfg, entry: labels.LabelEntry) -> frozenset[str]:
    """The releases of one label the genre gate holds in force, by identifier,
    JUDGED AGAIN FROM THEIR OWN WORDS as the sweep does; a withheld one stays."""
    judge = genre_gate.SweepGate(active_taxonomy.load(cfg), tracks=_no_tracks)
    with review.open_store(cfg) as store:
        held = review.holds(store, queue=Queue.LABEL_RELEASE, group=entry.label_id)
    return frozenset(
        release
        for hold in held
        if (release := genre_gate.hold_release_id(hold))
        and (hold.payload.get(review.WITHHELD_FIELD) or judge.rejudge(entry, hold).held)
    )


def _no_tracks(release_id: str):
    raise AssertionError(f"a rejudge read the tracks of {release_id}, which it never does")


def _reader(entry: labels.LabelEntry, found: catalogue.Catalogue):
    """Every track one release carries, for a release the catalogue read skipped."""
    tracks = catalogue.ReleaseTracks(found)

    def tracks_of(release_id: str) -> tuple[str, ...]:
        answered = playlists_cli.release_rows(entry, tracks, release_id)
        rows = answered[0] if answered is not None else ()
        return tuple(
            one for one in dict.fromkeys(str(getattr(row, "id", "") or "") for row in rows) if one
        )

    return tracks_of


def label_prune(ctx) -> Envelope:
    from cratekit.modules.outbound import prune

    cfg = label_cli._load()
    name = str(ctx.args.name)
    entry = labels.RegistryStore().load().resolve(name)
    planned: prune.Plan | None = None
    remote = None
    read = None
    if entry is not None:
        from cratekit.modules.outbound import account

        found = catalogue.resolve(cfg)
        read = playlists_cli.read_catalogue(cfg, entry, found)
        held = held_releases(cfg, entry)
        remote = account.resolve(cfg)
        planned = prune.plan_label(cfg, read, held, remote, tracks_of=_reader(entry, found))
    subject = entry.label_id if entry is not None else name
    payload = prune.payload(planned, kind=prune.LABEL, subject=subject, digest=digest_of)
    shown = (
        {"label": entry.name if entry is not None else name, **prune.shown(planned)}
        if planned is not None
        else {"label": name, "nothing to take off": playlists_cli.NOT_FOLLOWED_SAID}
    )
    if read is not None and read.tombstoned:
        shown["removed from the library"] = playlists_cli.tombstoned_said(len(read.tombstoned))
    # AN EMPTY PLAN STILL ASKS, so a person always sees what the prune judged.
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
    if planned is None:
        return playlists_cli.not_followed(ctx, payload, name)
    return prune.settle(
        ctx,
        cfg,
        remote,
        payload,
        planned,
        option=option,
        origin=_ORIGIN,
        again="run crate label prune again; what was taken off is recorded and never asked twice",
    )


__all__ = ["build_prune", "held_releases", "label_prune"]
