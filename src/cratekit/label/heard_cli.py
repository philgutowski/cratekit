"""``label.heard``: a label's dated playlist heard, merged and removed (U123).

``crate label heard <label> <year> <date>`` plans what hearing one dated
playlist writes, shows it at one explicit gate (an empty plan still asks), and
on ``apply`` merges it into the year, removes it and records its releases
heard; ``--release`` names some of them. The engine is
:mod:`cratekit.label.heard`. A label nobody follows is a plan of nothing.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import Outcome
from cratekit.label import catalogue, dated, heard, playlists_cli, sync_cli
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels

#: What the gate screen and the warning say about the rekordbox half.
TREE_UNCHANGED = "label-heard-tree-unchanged"


def build_heard(parser, entry) -> None:
    del entry
    playlists_cli.label_argument(parser)
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
    return {
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
                f", {len(planned.tombstoned)} left out as removed from the library "
                f"or taken off the year by a prune"
                if planned.tombstoned
                else ""
            )
            if planned.year_id or not planned.tombstoned
            else (
                f"nothing goes in the year: all {len(planned.tombstoned)} track(s) were "
                f"removed from the library or taken off the year by a prune"
            )
        ),
        "rekordbox": heard.TREE_SAID,
    }


def _tree_warning() -> dict[str, str]:
    return {"code": TREE_UNCHANGED, "message": heard.TREE_SAID}


def _applied_warnings(planned: heard.HeardPlan, done: heard.Heard) -> list[dict[str, str]]:
    warnings = [_tree_warning()]
    if done.missing:
        left = "the playlist was left on the account with them"
        message = (
            f"the provider would not add {len(done.missing)} track(s) of {planned.name!r} "
            f"to the year, so {left if done.kept else 'they stay on the playlist'}"
        )
        warnings.append({"code": "label-heard-tracks-refused", "message": message})
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
    payload = planned.payload() if planned is not None else dated.gate_plan(
        digest_of({"kind": "label-heard", "label": name, "year": year, "day": day}),
        [],
        {"heard": 0, "add": 0, "remove": 0, "take off": 0, "writes": False},
    )
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=_shown(planned, name=name))
    if planned is None:
        return playlists_cli.not_followed(ctx, payload, name)
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=[_tree_warning()])
    done = heard.apply(cfg, remote, planned)
    written = {"added": done.added, "taken off": done.taken_off, "removed": done.removed}
    written.update(kept=done.kept, heard=done.recorded)
    return playlists_cli.applied(ctx, payload, written, _applied_warnings(planned, done))


__all__ = ["TREE_UNCHANGED", "build_heard", "label_heard"]
