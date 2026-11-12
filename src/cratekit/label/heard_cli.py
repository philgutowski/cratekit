"""``label.heard``: a label's dated playlist heard, merged and removed (U123).

``crate label heard <label> <year> <date>`` names one dated playlist,
``<Label> <year> new <date>``, the way :mod:`cratekit.label.dated` named it.
The verb plans what hearing it writes, shows every release and both playlists
at one explicit gate, and on ``apply`` puts the dated playlist's tracks in the
year playlist, removes the dated playlist, and records its releases heard.
``--release`` names some of them instead of all. The engine is
:mod:`cratekit.label.heard`, and its docstring says what each step holds.

EXPLICIT, as every other write to the account is (R34), and more so: this
verb removes a playlist from it. AN EMPTY PLAN STILL ASKS, on ``label
prune``'s precedent, so a second run is a question answered over nothing.

THE CATALOGUE IS READ AS ``label playlists`` READS IT, through
:func:`cratekit.label.playlists_cli.read_catalogue`, because a release's year
is the catalogue's and the dated plan read it there.

A LABEL THAT IS NOT FOLLOWED IS A PLAN OF NOTHING, still gated, decided before
a credential is asked for, on ``label playlists``' precedent.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import Outcome
from cratekit.label import catalogue, heard, playlists_cli, sync_cli
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels

#: What the gate screen and the warning say about the rekordbox half.
TREE_UNCHANGED = "label-heard-tree-unchanged"


def build_heard(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )
    parser.add_argument("year", metavar="YEAR", help="the dated playlist's release year")
    parser.add_argument(
        "day", metavar="DATE", help="the dated playlist's date, as its name carries it"
    )
    parser.add_argument(
        "--release",
        dest="releases",
        action="append",
        default=[],
        metavar="ID",
        help=(
            "mark only this release of the dated playlist heard; repeat for more. "
            "Without it every release of the playlist is marked heard"
        ),
    )
    parser.set_defaults(_handler=label_heard)


def _shown(planned: heard.HeardPlan | None, *, name: str) -> dict[str, Any]:
    if planned is None:
        return {"label": name, "nothing to hear": playlists_cli.NOT_FOLLOWED_SAID}
    shown: dict[str, Any] = {
        "label": planned.label,
        "dated playlist": f"{planned.name}: {planned.action}",
        "releases": (
            f"{len(planned.releases)} in the playlist; {len(planned.newly)} marked heard "
            f"now, {len(planned.target) - len(planned.newly)} already heard, "
            f"{len(planned.unheard)} left unheard"
        ),
        "year playlist": (
            f"{len(planned.add)} track(s) added, "
            f"{len(planned.merging) - len(planned.add) - len(planned.tombstoned)} already there"
            + (
                f", {len(planned.tombstoned)} left out as removed from the library"
                if planned.tombstoned
                else ""
            )
        ),
        "rekordbox": heard.TREE_SAID,
    }
    return shown


def _tree_warning() -> dict[str, str]:
    return {"code": TREE_UNCHANGED, "message": heard.TREE_SAID}


def _applied_warnings(planned: heard.HeardPlan, done: heard.Heard) -> list[dict[str, str]]:
    warnings = [_tree_warning()]
    if done.missing:
        warnings.append(
            {
                "code": "label-heard-tracks-refused",
                "message": (
                    f"the provider would not add {len(done.missing)} track(s) of "
                    f"{planned.name!r} to the year, so "
                    + (
                        "the playlist was left on the account with them"
                        if done.kept
                        else "they stay on the playlist"
                    )
                ),
            }
        )
    return warnings


def label_heard(ctx) -> Envelope:
    cfg = label_cli._load()
    name = str(ctx.args.name)
    year = heard.checked_year(ctx.args.year)
    day = heard.checked_day(ctx.args.day)
    entry = labels.RegistryStore().load().resolve(name)
    planned: heard.HeardPlan | None = None
    remote = None
    if entry is not None:
        from cratekit.modules.outbound import account

        found = catalogue.resolve(cfg)
        read = playlists_cli.read_catalogue(cfg, entry, found)
        document = sync_cli.load_record(cfg)
        remote = account.resolve(cfg)
        planned = heard.plan(
            cfg, read, remote, document, year=year, day=day, named=ctx.args.releases
        )
    if planned is not None:
        payload = planned.payload()
    else:
        payload = {
            "digest": digest_of({"kind": "label-heard", "label": name, "year": year, "day": day}),
            "items": [],
            "totals": {"count": 0, "heard": 0, "add": 0, "remove": 0, "take off": 0, "writes": False},
            "chunk": None,
        }
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=_shown(planned, name=name))
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
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=[_tree_warning()])
    done = heard.apply(cfg, remote, planned)
    totals = {
        **payload["totals"],
        "applied": {
            "added": done.added,
            "taken off": done.taken_off,
            "removed": done.removed,
            "kept": done.kept,
            "heard": done.recorded,
        },
    }
    return ctx.envelope(
        data={**payload, "totals": totals},
        outcome=Outcome.OK,
        warnings=_applied_warnings(planned, done),
    )


__all__ = ["TREE_UNCHANGED", "build_heard", "label_heard"]
