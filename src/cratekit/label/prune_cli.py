"""``label.prune``: take dropped tracks off a label's year playlists (R-836).

``label playlists`` builds a followed label's folder of year playlists and adds,
never removes. This verb is the other half: it plans which tracks each year
playlist this product CREATED should no longer hold, a release the genre gate
now holds or the catalogue no longer confirms, or a track the library removed
through ``crate delete review`` (U243), shows every one of them by
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
from cratekit.core import active_taxonomy, review
from cratekit.core.cause import CratekitError, Outcome
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


def held_releases(cfg, entry: labels.LabelEntry) -> frozenset[str]:
    """The releases of one label the genre gate holds in force, by identifier.

    JUDGED AGAIN FROM THEIR OWN WORDS first, as the sweep does with a standing
    hold: a hold the label's kind or the taxonomy's rules would now release is
    not a reason to take a release's tracks off the account. A hold a person
    took back out of review stays held, as the sweep keeps it. No request.
    """
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
        try:
            rows, _year, _short = tracks.release_tracks(release_id)
        except catalogue.ReleaseUnresolvable:
            return ()
        except CratekitError:
            raise
        except Exception as exc:  # noqa: BLE001 - refused, never swallowed
            raise playlists_cli.incomplete(
                entry,
                f"the tracks of the release {release_id} could not be read "
                f"({type(exc).__name__}: {exc})",
            ) from exc
        return tuple(
            one for one in dict.fromkeys(str(getattr(row, "id", "") or "") for row in rows) if one
        )

    return tracks_of


def label_prune(ctx) -> Envelope:
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
