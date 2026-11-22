"""``crate tag remap``: rewrite the genres an older mapping wrote.

A VERB OF ITS OWN (R-799), not a mode of ``tag retag``: that verb selects a
genre too coarse and asks a catalogue behind a job; this one selects by what a
tagging job RECORDED, asks nobody, and resolves the recorded word again under
the taxonomy as it stands. A gate asked in one mode only is one the registry
cannot state.

THE ORDER IS ``tag rows``'S: the plan by reading, the gate over its digest, AN
EMPTY PLAN STILL ASKS, and only ``apply`` over a plan that writes touches a
file. The second invocation rebuilds the plan, so a file that changed in
between refuses ``decision-stale`` with nothing written.

IT WRITES FILES AND OPENS NO DATABASE. A corrected file's row keeps the old
genre until ``tag rows`` writes it, and a run that wrote names that verb, not a
reload in rekordbox, which takes every tag field from the file.

WHAT A PERSON READS. The gate carries the counts and word pairs. Every path
says how many files were left and why, and a taxonomy with no table for the
general catalogue is said, since a clean answer there would read as a library
already corrected. A file that did not take its genre refuses, and the refusal
still names the row verb for the files that did, since the next run plans none
of them.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy
from cratekit.core.cause import Outcome, refuse
from cratekit.tagging import plan_verbs, remap
from cratekit.tagging.plan_verbs import counted, named, warning

#: The explicit gate a rewrite is asked behind.
CONFIRM_GATE = "tag.remap.confirm"

#: The plan writes nothing.
NOTHING_TO_WRITE = "remap-nothing-to-write"

#: What the apply wrote and read back, and the verb the rows follow by.
GENRES_WRITTEN = "remap-genre-written"

#: Files that do not carry what the taxonomy now gives their word, and were left.
FILES_LEFT = "remap-left-alone"

#: Files whose genre could not be learned.
FILES_NOT_READ = "remap-file-not-read"

#: Files a record names that are not under this library's root.
FILES_OUTSIDE = "remap-outside-library"

#: The active taxonomy declares no table for the general catalogue.
NO_VOCABULARY = "remap-no-vocabulary"

#: Committed tagging records that could not be parsed.
RECORDS_UNREAD = "remap-records-unread"

_ORIGIN = ("tagging", "remap_cli")


def build(parser, entry) -> None:
    """Declare the verb. It takes no argument: it reads every tagging record."""
    del entry
    parser.set_defaults(_handler=tag_remap)


def _payload(plan: remap.RemapPlan) -> dict[str, Any]:
    return plan_verbs.payload(
        plan,
        files=plan.files,
        outcomes=dict(plan.counts),
        pairs=plan.pairs(),
        records_unread=plan.records_unread,
    )


def _facts(plan: remap.RemapPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the counts and the pairs."""
    return {
        "source": remap.SOURCE,
        "files": plan.files,
        "outcomes": dict(plan.counts),
        "pairs": plan.pairs(),
    }


def _left(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries when a file was read and left, on every path."""
    count = sum(plan.counts[name] for name in remap.LEFT)
    if not count:
        return []
    return [
        warning(
            FILES_LEFT,
            f"{count} file(s) do not carry the genre the taxonomy now gives "
            f"their word and were left alone ({counted(plan.counts, remap.LEFT)}), "
            f"each listed with its reason: {remap.CHANGED_SINCE} is a genre no "
            f"tagging job recorded writing, {remap.WORD_DECLINED} a word the "
            f"taxonomy has no folder for, and {remap.AMBIGUOUS_RECORD} a genre "
            f"two records explain differently",
        )
    ]


def _not_read(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries when a file's genre could not be learned."""
    count = sum(plan.counts[name] for name in remap.UNREAD)
    if not count:
        return []
    return [
        warning(
            FILES_NOT_READ,
            f"{count} of {plan.files} file(s) a tagging job wrote a genre from "
            f"{remap.SOURCE} onto could not be read ({counted(plan.counts, remap.UNREAD)}), "
            f"each listed; a file that has moved since, and a volume that is "
            f"not mounted, both read as {remap.FILE_MISSING}, and nothing here "
            f"says those files are correct",
        )
    ]


def _outside(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries when a record names a file outside the library."""
    count = plan.counts[remap.OUTSIDE_LIBRARY]
    if not count:
        return []
    return [
        warning(
            FILES_OUTSIDE,
            f"{count} of {plan.files} file(s) a tagging job wrote a genre from "
            f"{remap.SOURCE} onto are not under this library's root and were "
            f"not opened: a folder tagged before it was landed, or another "
            f"library's; a file is followed only where it was tagged, so one "
            f"landed since is not among the files this plan looked at",
        )
    ]


def _no_vocabulary(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries over a taxonomy with no table for the source."""
    if plan.declared:
        return []
    return [
        warning(
            NO_VOCABULARY,
            f"the active taxonomy declares no vocabulary for {remap.SOURCE}, so "
            f"its words are still resolved by the buckets' aliases and this "
            f"plan compares each file with that; give the library's copy the "
            f"[vocabulary.{remap.SOURCE}] table the shipped template carries, "
            f"together with every routing alias and sub_by_source map row that "
            f"template declares for the table's tags, since a tag that names "
            f"no folder is refused and the copy would not load, then run this "
            f"again",
        )
    ]


def _records_unread(plan: remap.RemapPlan) -> list[dict[str, str]]:
    if not plan.records_unread:
        return []
    return [
        warning(
            RECORDS_UNREAD,
            f"{plan.records_unread} committed tagging record(s) could not be "
            f"parsed and were not read, so a file one of them names was not "
            f"looked at",
        )
    ]


def _advisories(plan: remap.RemapPlan) -> list[dict[str, str]]:
    return [
        *_no_vocabulary(plan),
        *_left(plan),
        *_not_read(plan),
        *_outside(plan),
        *_records_unread(plan),
    ]


def _nothing(plan: remap.RemapPlan) -> dict[str, str]:
    return warning(
        NOTHING_TO_WRITE,
        f"no file's genre is to be rewritten: {plan.counts[remap.AGREE]} of "
        f"{plan.files} file(s) a tagging job wrote a genre from {remap.SOURCE} "
        f"onto carry the genre the taxonomy gives their word",
    )


#: What a run that rewrote a file owes its rows, on a clean run's envelope and
#: among the steps of a refusal that wrote some.
ROWS_FOLLOW = (
    "the library rows of the rewritten files go on carrying the old genre, so "
    "run `crate tag rows`, which writes each row's genre from its file and no "
    "other column, where a reload in rekordbox overwrites every tag field; for a "
    "genre the library has never held that verb names the one act it needs first"
)


def _written(plan: remap.RemapPlan, written: remap.Written) -> dict[str, str]:
    pairs = "; ".join(
        f"{pair['from']!r} to {pair['to']!r}, {pair['files']}" for pair in plan.pairs()
    )
    return warning(
        GENRES_WRITTEN,
        f"{written.written} file(s) now carry the genre the taxonomy gives "
        f"their word and {written.read_back} read back as written: {pairs}; "
        f"the items list each file with the genre it carried, which is the "
        f"undo; {ROWS_FOLLOW}",
    )


def assert_written(written: remap.Written) -> None:
    """Refuse when a file did not take the genre the plan gave it, after the
    others were written, saying how many. A second run plans what is left.

    THE ROW VERB IS NAMED HERE TOO WHEN ANY FILE WAS REWRITTEN: this run never
    reaches the envelope that names it, and the next plans none of those files.
    """
    if written.clean:
        return
    parts = []
    if written.moved:
        parts.append(
            f"{len(written.moved)} carried something else by the time the write "
            f"reached them and were not written: {named(written.moved)}"
        )
    if written.failed:
        parts.append(
            f"{len(written.failed)} could not be written and are untouched: "
            f"{named(written.failed)}"
        )
    if written.wrong:
        parts.append(
            f"{len(written.wrong)} were written and do not read back as the genre "
            f"wanted: {named(written.wrong)}"
        )
    if written.unrecorded:
        parts.append(
            f"{len(written.unrecorded)} were rewritten and read back and no record "
            f"of the rewrite could be committed, so a later run reads their genre "
            f"as set by hand: {named(written.unrecorded)}"
        )
    steps = [
        "check each named file can be written and is not open elsewhere",
        "run the verb again, which plans what is left",
    ]
    if written.written:
        steps.append(ROWS_FOLLOW)
    raise refuse(
        "tag-remap-unwritten",
        f"{written.read_back} file(s) were rewritten and read back, and "
        + "; ".join(parts),
        steps=tuple(steps),
        origin=_ORIGIN,
        detail={
            "wrong": list(written.wrong),
            "moved": list(written.moved),
            "failed": list(written.failed),
            "unrecorded": list(written.unrecorded),
            "written": written.written,
            "read_back": written.read_back,
            # THE UNDO, which a clean run's envelope carries as its items.
            "rewritten": [
                {"path": item.path, "from": item.current, "to": item.wanted}
                for item in written.rewritten
            ],
        },
    )


def tag_remap(ctx) -> Envelope:
    """Plan from the tagging records, ask, then rewrite the genre and read it back."""
    cfg = load_config(_ORIGIN)
    declared = active_taxonomy.load(cfg)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)

    plan = remap.plan(cfg, declared)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))

    def apply() -> remap.Written:
        written = remap.apply(cfg, plan)
        assert_written(written)
        return written

    return plan_verbs.applied(
        ctx,
        plan,
        data,
        _advisories,
        nothing=_nothing,
        apply=apply,
        said=lambda written: _written(plan, written),
    )


__all__ = [
    "CONFIRM_GATE", "FILES_LEFT", "FILES_NOT_READ", "FILES_OUTSIDE", "GENRES_WRITTEN",
    "NOTHING_TO_WRITE", "NO_VOCABULARY", "RECORDS_UNREAD", "ROWS_FOLLOW", "assert_written", "build",
    "tag_remap",
]
