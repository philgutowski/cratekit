"""``crate tag remap``: rewrite the genres an older mapping wrote.

WHY THIS IS A VERB OF ITS OWN (R-799) and not a mode of ``tag retag``. That
verb selects a genre the taxonomy calls too coarse and asks a catalogue what
it should be, which is long running work behind a job. This one selects by
what a tagging job RECORDED, asks nobody, and resolves the recorded word again
under the taxonomy as it stands. A gate is declared per verb and every declared
gate has to fire, so a gate asked in one mode only is a gate the registry
cannot state.

THE ORDER IS ``tag rows``'S: the plan is built by reading, the explicit gate is
asked over its digest, AND AN EMPTY PLAN STILL ASKS, for the reason ``tag
retag`` gives. Only ``apply`` over a plan that writes touches a file.

THE SECOND INVOCATION REBUILDS THE PLAN from the records and the files, and the
gate compares its digest with the one the answer was recorded against. A file
whose genre changed in between moves the digest and the run refuses
``decision-stale`` with nothing written.

IT WRITES FILES AND OPENS NO DATABASE. A corrected file's row goes on carrying
the old genre until ``tag rows`` writes it from the file, and a run that wrote
says so and names that verb. Not a reload in rekordbox, which takes every tag
field from the file. For a genre the library has never held, that verb names
the one act it needs first.

WHAT A PERSON READS. The gate carries the outcome counts and the word pairs in
front of the items. A run that left a file alone says how many and why on
every path, and a run over a taxonomy that declares no table for the general
catalogue says that, since on such a copy nothing can have changed and a clean
answer would read as a library already corrected. A run in which a file did
not take its genre refuses, and the refusal still names the row verb for the
files that did, since the next run plans none of them and would not say it.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import remap

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

#: How many offending files a refusal's sentence names. The detail carries all.
_NAMED_FILES = 5

_ORIGIN = ("tagging", "remap_cli")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.remap_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb. It takes no argument: it reads every tagging record."""
    del entry
    parser.set_defaults(_handler=tag_remap)


def _confirm_gate(entry):
    """The verb's own gate by name, never by position."""
    for spec in entry.gates:
        if spec.name == CONFIRM_GATE:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {CONFIRM_GATE!r}, so there is no "
        f"question to ask before it writes",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"verb": entry.name, "gate": CONFIRM_GATE},
    )


def _payload(plan: remap.RemapPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {
            "count": len(plan.items),
            "files": plan.files,
            "outcomes": dict(plan.counts),
            "pairs": plan.pairs(),
            "records_unread": plan.records_unread,
            "written": 0,
            "read_back": 0,
        },
        "chunk": None,
    }


def _facts(plan: remap.RemapPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the counts and the pairs."""
    return {
        "source": remap.SOURCE,
        "files": plan.files,
        "outcomes": dict(plan.counts),
        "pairs": plan.pairs(),
    }


def _counted(plan: remap.RemapPlan, names: tuple[str, ...]) -> str:
    return ", ".join(f"{plan.counts[name]} {name}" for name in names if plan.counts[name])


def _left(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries when a file was read and left, on every path."""
    count = sum(plan.counts[name] for name in remap.LEFT)
    if not count:
        return []
    return [
        {
            "code": FILES_LEFT,
            "message": (
                f"{count} file(s) do not carry the genre the taxonomy now gives "
                f"their word and were left alone ({_counted(plan, remap.LEFT)}), "
                f"each listed with its reason: {remap.CHANGED_SINCE} is a genre no "
                f"tagging job recorded writing, {remap.WORD_DECLINED} a word the "
                f"taxonomy has no folder for, and {remap.AMBIGUOUS_RECORD} a genre "
                f"two records explain differently"
            ),
        }
    ]


def _not_read(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries when a file's genre could not be learned."""
    count = sum(plan.counts[name] for name in remap.UNREAD)
    if not count:
        return []
    return [
        {
            "code": FILES_NOT_READ,
            "message": (
                f"{count} of {plan.files} file(s) a tagging job wrote a genre from "
                f"{remap.SOURCE} onto could not be read ({_counted(plan, remap.UNREAD)}), "
                f"each listed; a file that has moved since, and a volume that is "
                f"not mounted, both read as {remap.FILE_MISSING}, and nothing here "
                f"says those files are correct"
            ),
        }
    ]


def _outside(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries when a record names a file outside the library."""
    count = plan.counts[remap.OUTSIDE_LIBRARY]
    if not count:
        return []
    return [
        {
            "code": FILES_OUTSIDE,
            "message": (
                f"{count} of {plan.files} file(s) a tagging job wrote a genre from "
                f"{remap.SOURCE} onto are not under this library's root and were "
                f"not opened: a folder tagged before it was landed, or another "
                f"library's; a file is followed only where it was tagged, so one "
                f"landed since is not among the files this plan looked at"
            ),
        }
    ]


def _no_vocabulary(plan: remap.RemapPlan) -> list[dict[str, str]]:
    """The warning a run carries over a taxonomy with no table for the source."""
    if plan.declared:
        return []
    return [
        {
            "code": NO_VOCABULARY,
            "message": (
                f"the active taxonomy declares no vocabulary for {remap.SOURCE}, so "
                f"its words are still resolved by the buckets' aliases and this "
                f"plan compares each file with that; add the [vocabulary."
                f"{remap.SOURCE}] table the shipped template carries to the "
                f"library's copy, then run this again"
            ),
        }
    ]


def _records_unread(plan: remap.RemapPlan) -> list[dict[str, str]]:
    if not plan.records_unread:
        return []
    return [
        {
            "code": RECORDS_UNREAD,
            "message": (
                f"{plan.records_unread} committed tagging record(s) could not be "
                f"parsed and were not read, so a file one of them names was not "
                f"looked at"
            ),
        }
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
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"no file's genre is to be rewritten: {plan.counts[remap.AGREE]} of "
            f"{plan.files} file(s) a tagging job wrote a genre from {remap.SOURCE} "
            f"onto carry the genre the taxonomy gives their word"
        ),
    }


#: What a run that rewrote a file owes its rows. One text, on the envelope of a
#: clean run and among the steps of a refusal that wrote some.
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
    return {
        "code": GENRES_WRITTEN,
        "message": (
            f"{written.written} file(s) now carry the genre the taxonomy gives "
            f"their word and {written.read_back} read back as written: {pairs}; "
            f"the items list each file with the genre it carried, which is the "
            f"undo; {ROWS_FOLLOW}"
        ),
    }


def _named(paths: tuple[str, ...]) -> str:
    shown = ", ".join(paths[:_NAMED_FILES])
    return shown if len(paths) <= _NAMED_FILES else f"{shown} and {len(paths) - _NAMED_FILES} more"


def assert_written(written: remap.Written) -> None:
    """Refuse when a file did not take the genre the plan gave it.

    AFTER THE OTHER FILES WERE WRITTEN, and the message says how many, so a
    person is not told nothing happened. A second run plans what is left.

    THE ROW VERB IS NAMED HERE TOO WHEN ANY FILE WAS REWRITTEN. This run ends
    in the refusal and never reaches the envelope that names it, and the next
    run finds those files agreeing and plans none of them, so neither would
    say their rows are stale.
    """
    if written.clean:
        return
    parts = []
    if written.moved:
        parts.append(
            f"{len(written.moved)} carried something else by the time the write "
            f"reached them and were not written: {_named(written.moved)}"
        )
    if written.failed:
        parts.append(
            f"{len(written.failed)} could not be written and are untouched: "
            f"{_named(written.failed)}"
        )
    if written.wrong:
        parts.append(
            f"{len(written.wrong)} were written and do not read back as the genre "
            f"wanted: {_named(written.wrong)}"
        )
    if written.unrecorded:
        parts.append(
            f"{len(written.unrecorded)} were rewritten and read back and no record "
            f"of the rewrite could be committed, so a later run reads their genre "
            f"as set by hand: {_named(written.unrecorded)}"
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
        },
    )


def tag_remap(ctx) -> Envelope:
    """Plan from the tagging records, ask, then rewrite the genre and read it back."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    spec = _confirm_gate(ctx.entry)

    plan = remap.plan(cfg, declared)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
    if not plan.writes:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[_nothing(plan), *_advisories(plan)],
        )

    written = remap.apply(cfg, plan)
    assert_written(written)
    data["totals"] = {
        **data["totals"],
        "written": written.written,
        "read_back": written.read_back,
    }
    return ctx.envelope(data=data, warnings=[_written(plan, written), *_advisories(plan)])


__all__ = [
    "CONFIRM_GATE",
    "FILES_LEFT",
    "FILES_NOT_READ",
    "FILES_OUTSIDE",
    "GENRES_WRITTEN",
    "NOTHING_TO_WRITE",
    "NO_VOCABULARY",
    "RECORDS_UNREAD",
    "ROWS_FOLLOW",
    "assert_written",
    "build",
    "tag_remap",
]
