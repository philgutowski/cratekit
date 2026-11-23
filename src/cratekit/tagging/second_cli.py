"""``crate tag second``: set or clear a track's second genre (U340).

A second genre files a track into a second genre folder of the routing tree
beside the one its genre names, each in its own energy band. This verb writes
it onto the chosen rows' files and nothing else, behind one explicit gate over
a digested plan that lists every chosen row with its second genre before and
after and why any is left. THE ORDER IS ``tag remap``'S, an empty plan still
asking. It reads the library's database to resolve the rows and writes none,
so the run that wrote names the step that files the tracks.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy
from cratekit.core.cause import Outcome, refuse
from cratekit.tagging import plan_verbs, second
from cratekit.tagging.plan_verbs import counted, named, warning

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "tag.second.confirm"

#: The warnings: nothing to write, what was written and read back, rows left.
NOTHING_TO_WRITE = "second-genre-nothing-to-write"
WRITTEN = "second-genre-written"
ROWS_LEFT = "second-genre-left"

_ORIGIN = ("tagging", "second_cli")

#: What the read is blocked by, named in the refusal of a library read wrong.
_BLOCKED = "a second genre cannot be set until its rows can be found on disk"

#: The step that files a track by its second genre, named by a run that wrote.
FILES_FOLLOW = (
    "the tree follows the files at the next filing: `crate adopt apply`, or "
    "`crate organize --only adopt`, files each track into its second genre's "
    "folder in the band its energy names; a track whose second genre is "
    "cleared here stays in that folder until it is taken out there (a Soul "
    "track's cleared R&B is the one exception, which `crate adopt move` "
    "takes it out of, as for any Soul track in an R&B band), and "
    "`crate converge` names it only while that playlist holds another track "
    "filed into it"
)


def build(parser, entry) -> None:
    """Declare the verb: the genre or ``--clear``, and the rows."""
    del entry
    parser.add_argument(
        "genre", nargs="?", default=None,
        help="the second genre to set, one the taxonomy files into a folder of its own",
    )
    parser.add_argument(
        "--clear", action="store_true",
        help="clear the second genre instead of setting one",
    )
    parser.add_argument(
        "--row", action="append", default=[], metavar="CONTENT_ID",
        help="a row to set or clear, by content identifier; repeatable",
    )
    parser.add_argument(
        "--rows-file", default=None, metavar="PATH",
        help="a file of content identifiers, one per line",
    )
    parser.add_argument(
        "--playlist", default=None, metavar="PATH",
        help="every track of one playlist, named folder by folder joined by ' / '",
    )
    parser.add_argument(
        "--leave", action="append", default=[], metavar="CONTENT_ID",
        help="a chosen row to hold out of the write; repeatable",
    )
    parser.set_defaults(_handler=tag_second)


def _genre(args: Any) -> str:
    """The genre to set, empty to clear; exactly one of the two is asked for."""
    genre = (getattr(args, "genre", None) or "").strip()
    clear = bool(getattr(args, "clear", False))
    if clear == bool(genre):
        raise refuse(
            "tag-second-usage",
            "name a second genre to set or pass --clear, and not both",
            steps=(
                "run `crate tag second GENRE --row ID`, or `crate tag second --clear --row ID`",
            ),
            origin=_ORIGIN,
            detail={"genre": genre, "clear": clear},
        )
    return genre


def _payload(plan: second.SecondPlan) -> dict[str, Any]:
    return plan_verbs.payload(plan, rows=plan.rows, genre=plan.genre, outcomes=dict(plan.counts))


def _facts(plan: second.SecondPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the genre, the rows and the counts."""
    return {
        "second_genre": plan.genre or "(cleared)",
        "rows": plan.rows,
        "outcomes": dict(plan.counts),
    }


def _left(plan: second.SecondPlan) -> list[dict[str, str]]:
    count = sum(plan.counts[name] for name in second.LEFT)
    if not count:
        return []
    return [warning(
        ROWS_LEFT,
        f"{count} of {plan.rows} chosen row(s) were left ({counted(plan.counts, second.LEFT)}), "
        f"each listed with its reason: {second.SAME_FOLDER} is a second genre naming the "
        f"folder the file's genre already names, and {second.GENRE_FILES_NOWHERE} a file "
        f"whose genre names no folder, so a second genre would file it nowhere",
    )]


def _nothing(plan: second.SecondPlan) -> dict[str, str]:
    return warning(
        NOTHING_TO_WRITE,
        f"no file's second genre is to be written: of {plan.rows} chosen row(s), "
        f"{plan.counts[second.ALREADY] + plan.counts[second.NONE_TO_CLEAR]} already "
        f"carry what was asked",
    )


def _written(plan: second.SecondPlan, written: second.Written) -> dict[str, str]:
    what = f"the second genre {plan.genre!r}" if plan.genre else "no second genre"
    return warning(
        WRITTEN,
        f"{written.written} file(s) now carry {what} and {written.read_back} read back "
        f"as written; the items list each file with the second genre it carried, which "
        f"is the undo; {FILES_FOLLOW}",
    )


def assert_written(written: second.Written) -> None:
    """Refuse when a file did not take, after the others were written."""
    if written.clean:
        return
    parts = []
    if written.moved:
        parts.append(
            f"{len(written.moved)} carried something else by the time the write reached "
            f"them and were not written: {named(written.moved)}"
        )
    if written.failed:
        parts.append(
            f"{len(written.failed)} could not be written and are untouched: "
            f"{named(written.failed)}"
        )
    if written.wrong:
        parts.append(
            f"{len(written.wrong)} were written and do not read back as wanted: "
            f"{named(written.wrong)}"
        )
    steps = [
        "check each named file can be written and is not open elsewhere",
        "run the verb again, which plans what is left",
    ]
    if written.read_back:
        steps.append(FILES_FOLLOW)
    raise refuse(
        "tag-second-unwritten",
        f"{written.read_back} file(s) were written and read back, and " + "; ".join(parts),
        steps=tuple(steps),
        origin=_ORIGIN,
        detail={
            "wrong": list(written.wrong),
            "moved": list(written.moved),
            "failed": list(written.failed),
            "written": written.written,
            "read_back": written.read_back,
            # THE UNDO, which a clean run's envelope carries as its items.
            "rewritten": [
                {"path": item.path, "from": item.current, "to": item.wanted}
                for item in written.rewritten
            ],
        },
    )


def read_plan(cfg, declared, args: Any, genre: str) -> second.SecondPlan:
    """The plan over the chosen rows, through a handle opened to read and closed
    before this returns. A genre naming no folder refuses before it opens."""
    if genre:
        second.assert_genre_files(declared, genre)
    with plan_verbs.reading(cfg, _BLOCKED) as db:
        chosen = second.chosen_rows(
            db,
            rows_given=list(getattr(args, "row", None) or ()),
            rows_file=getattr(args, "rows_file", None),
            playlist=getattr(args, "playlist", None),
        )
        return second.plan(
            cfg, db, declared, genre=genre, chosen=chosen,
            leave=list(getattr(args, "leave", None) or ()),
        )


def tag_second(ctx) -> Envelope:
    """Plan the chosen rows, ask, then write the second genre and read it back."""
    genre = _genre(ctx.args)
    cfg = load_config(_ORIGIN)
    declared = active_taxonomy.load(cfg)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)

    plan = read_plan(cfg, declared, ctx.args, genre)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_left(plan))

    def apply() -> second.Written:
        written = second.apply(plan)
        assert_written(written)
        return written

    return plan_verbs.applied(
        ctx,
        plan,
        data,
        _left,
        nothing=_nothing,
        apply=apply,
        said=lambda written: _written(plan, written),
    )


__all__ = [
    "CONFIRM_GATE", "FILES_FOLLOW", "NOTHING_TO_WRITE", "ROWS_LEFT", "WRITTEN", "assert_written",
    "build", "read_plan", "tag_second",
]
