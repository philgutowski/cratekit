"""``crate tag backlog``: the needs genre backlog sorted by cause, writing nothing (U292).

WHAT IT ANSWERS. Of the rows adoption files nowhere for want of a genre, which
``tag rows`` writes from their file, which ``tag suggest`` would give a genre at
the floor and from what evidence, which carry a word no folder takes, grouped
by word with one question each, and which are left by hand and why. Then the
campaign: the gated verbs in the order they settle it, with the rows each
moves, and needs genre now and after.

A PERSON READS IT AS CHECK ROWS, on doctor's diagnostic surface as ``report
genres`` is read; the summary carries every row and every count.

IT WRITES NOTHING, AND ASKS NOTHING: no gate, no session, no acknowledgment,
and the database opened to read and closed before the envelope. With
``--catalogue`` the answers are kept in ``tag suggest``'s own state entry for a
week, so ``tag suggest --catalogue`` reads the same ones. A library most of
whose rows are under no prefix rule refuses, as ``tag rows`` does, since every
row would read as excluded.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, config
from cratekit.core.cause import Outcome
from cratekit.tagging import backlog, plan_verbs, rows, searchers, suggest
from cratekit.tagging.plan_verbs import named, warning

#: The notes the verb carries on its warnings channel.
WORDS_ASKED = "backlog-words-asked"
LIBRARY_ALONE = "backlog-library-alone"
CATALOGUE_UNREAD = "backlog-catalogue-unread"
REMAINDER = "backlog-remainder"
FILES_UNREAD = "backlog-files-unread"
ROWS_JOINING = "backlog-rows-joining"

#: What the majority refusal says cannot be done until a prefix rule exists.
_BLOCKED = "the needs genre backlog cannot be read"

#: How many words or identifiers a sentence names, :func:`named`'s.
_NAMED = plan_verbs.NAMED


def build(parser, entry) -> None:
    """Declare the verb. It reads the whole collection."""
    del entry
    parser.add_argument(
        "--catalogue",
        action="store_true",
        help="also ask the catalogues tag suggest --catalogue asks about each row "
        "with no genre, paced; the answers are kept a week for tag suggest",
    )
    parser.set_defaults(_handler=tag_backlog)


def read_plan(cfg: config.Config, declared, catalogue: bool, progress) -> backlog.Backlog:
    """The backlog over the library as it stands, through a handle opened to read.

    THE ONE PLAN, this report's and ``tag campaign``'s (U294). The copy's text is
    read the way ``taxonomy alias`` reads it, so each word's answers are planned
    on the copy those verbs would edit.
    """
    _path, text = active_taxonomy.read_text(cfg)
    with plan_verbs.reading(cfg, _BLOCKED) as db:
        if not catalogue:
            return backlog.plan_backlog(cfg, db, declared, text=text, progress=progress)
        with plan_verbs.kept(cfg, declared) as kept:
            return backlog.plan_backlog(
                cfg, db, declared, text=text, catalogue=kept, progress=progress
            )


def advisories(plan: backlog.Backlog) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    asked = [word for word in plan.words if word.options]
    if asked:
        found.append(
            warning(
                WORDS_ASKED,
                f"{len(asked)} genre word(s) no folder takes are carried by "
                f"{sum(word.rows for word in asked)} row(s): "
                f"{named([f'{word.spelling} ({word.rows})' for word in asked])}; "
                f"each has one question, an alias, its own folder or left by "
                f"hand, with the recommendation first",
            )
        )
    no_genre = plan.counts[backlog.NO_GENRE]
    if no_genre and not plan.catalogue:
        found.append(
            warning(
                LIBRARY_ALONE,
                f"the {no_genre} row(s) with no genre were weighed from their "
                f"artist and folder alone; --catalogue asks Discogs, then "
                f"Beatport when Discogs gives no genre, then Deezer by ISRC",
            )
        )
    # Said apart as ``tag suggest`` says them (U244, U322).
    unread = suggest.sort_unread(
        (row.content_id, row.asked) for row in plan.rows if row.asked is not None
    )
    parts = []
    if unread.refused:
        parts.append(
            f"the catalogues could not be read for {len(unread.refused)} row(s), "
            f"{named(list(unread.refused))}, so those were weighed from the library alone"
        )
    if unread.partly:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {named(list(unread.partly))}, so those were "
            f"weighed without it"
        )
    if unread.no_token:
        parts.append(
            f"Discogs was not asked about {len(unread.no_token)} row(s), "
            f"{named(list(unread.no_token))}, because no Discogs token is recorded, so "
            f"those were weighed from the library alone; to record one: "
            f"{searchers.DISCOGS_LOGIN_STEPS}"
        )
    if unread.token_unusable:
        parts.append(
            f"Discogs was not read for {len(unread.token_unusable)} row(s), "
            f"{named(list(unread.token_unusable))}, because the recorded Discogs token "
            f"could not be used, so those were weighed without it; to record a new one: "
            f"{searchers.DISCOGS_LOGIN_STEPS}"
        )
    if parts:
        found.append(warning(CATALOGUE_UNREAD, "; ".join(parts)))
    excluded = sum(plan.unread.values())
    if excluded:
        found.append(
            warning(
                FILES_UNREAD,
                f"{excluded} row(s) are in no cause, because their file is not "
                f"here or could not be read ({_counts(plan.unread)}), so adoption "
                f"excludes them and whether they need a genre is unknown; a volume "
                f"that is not mounted reads as {rows.FILE_MISSING}",
            )
        )
    if plan.joining:
        found.append(
            warning(
                ROWS_JOINING,
                f"{backlog.ROWS_VERB} would also write a genre no folder takes onto "
                f"{len(plan.joining)} row(s) adoption files today, "
                f"{named(list(plan.joining))}, moving them into needs genre; the "
                f"projection counts them, and --leave holds a row out",
            )
        )
    left = plan.statuses[backlog.LEFT]
    if left:
        found.append(
            warning(
                REMAINDER,
                f"{left} row(s) are left by hand, each counted with its reason "
                f"and what would settle it in the remainder",
            )
        )
    return found


#: The status every row carries. The backlog is worth knowing and is nothing
#: this verb fixes, which is what doctor's INFO means.
_INFO = "info"

#: What each cause is, as a check row says it.
_CAUSE_WORDS = {
    backlog.FILE_UNREAD: "the file's genre could not be read",
    backlog.ROW_LAGS_FILE: f"the file carries a genre adoption files by, which {backlog.ROWS_VERB} writes onto the row",
    backlog.NO_GENRE: f"no genre on the row or the file, which {backlog.SUGGEST_VERB} weighs",
    backlog.TOO_COARSE: f"a word too coarse to be a genre, which {backlog.RETAG_VERB} replaces",
    backlog.OFF_TAXONOMY: "a genre word no folder takes, one question per word",
}


def _check(key: str, title: str, detail: str) -> dict[str, Any]:
    return {"key": key, "title": title, "status": _INFO, "detail": detail, "remedy": None}


def _word_detail(word: backlog.Word) -> str:
    if word.settled:
        return (
            f"{word.rows} row(s); one answer, asking nothing: {word.settled} retags "
            f"the files, moving {len(word.reached)} row(s)"
        )
    if word.unanswerable is not None:
        _why, message, step = word.unanswerable
        return f"{word.rows} row(s); asks nothing: {message}; {step}"
    answers = []
    for index, option in enumerate(word.options, start=1):
        shown = f"{index}) {option.label}" + (" (recommended)" if index == 1 else "")
        shown += f": {option.detail}"
        if option.command:
            shown += f"; run {option.command}"
        answers.append(shown)
    return f"{word.question()} " + " ".join(answers)


def _proposed_detail(plan: backlog.Backlog) -> str:
    seen = Counter((row.proposal.genre, row.proposal.source) for row in plan.proposals if row.proposal)
    ordered = sorted(seen.items(), key=lambda entry: (-entry[1], entry[0]))
    parts = [f"{count} {genre} from {source}" for (genre, source), count in ordered]
    return (
        f"{len(plan.proposals)} row(s) with no genre have a proposal at {backlog.FLOOR} or "
        f"better: {named(parts)}; each item carries its votes and share"
    )


def _asked_rows(plan: backlog.Backlog) -> list[suggest.Asked]:
    return [row.asked for row in plan.rows if row.asked is not None]


def _catalogue_detail(plan: backlog.Backlog) -> str:
    """Each catalogue's answers across the rows asked about, as a person reads them (U322)."""
    counted = suggest.catalogue_counts(_asked_rows(plan))
    parts = []
    for source, entry in counted["catalogues"].items():
        said = (
            f"{source} asked about {entry['asked']}, matched {entry['matched']}, "
            f"missed {entry['missed']}, could not be read for {entry['unread']}, "
            f"not asked about {entry['not_asked']}"
        )
        if entry["not_sent"]:
            said += f" ({entry['not_sent']} of them once it had refused this client)"
        parts.append(said)
    detail = f"{counted['rows']} row(s) with no genre were weighed with the catalogues"
    detail += (": " + "; ".join(parts)) if parts else ", and no catalogue's answer is recorded"
    if counted["stopped"]:
        detail += (
            f"; the walk asked nothing about {counted['stopped']} row(s) once no "
            f"catalogue could be read for {suggest.STOP_AFTER_UNREAD} rows in a row"
        )
    return detail


def checks(plan: backlog.Backlog) -> list[dict[str, Any]]:
    """The backlog as rows a person reads: causes, proposals, words, steps, remainder."""
    found: list[dict[str, Any]] = []
    for cause, count in plan.counts.items():
        if count:
            found.append(
                _check(f"backlog.cause.{cause}", cause, f"{count} row(s): {_CAUSE_WORDS[cause]}")
            )
    if plan.proposals:
        found.append(_check("backlog.proposed", "proposed", _proposed_detail(plan)))
    if plan.catalogue:
        found.append(_check("backlog.catalogue", "catalogue", _catalogue_detail(plan)))
    for word in plan.words:
        found.append(_check(f"backlog.word.{word.spelling}", word.spelling, _word_detail(word)))
    for number, step in enumerate(plan.campaign(), start=1):
        found.append(
            _check(
                f"backlog.step.{number}",
                step["command"],
                f"{step['command']}: {step['rows']} row(s), {step['why']}",
            )
        )
    for entry in plan.remainder():
        found.append(
            _check(
                f"backlog.left.{entry['cause']}.{entry['reason']}",
                entry["reason"],
                f"{entry['rows']} row(s) left by hand: {entry['settle']}",
            )
        )
    if plan.unread:
        found.append(
            _check(
                "backlog.unread",
                "in no cause",
                f"{sum(plan.unread.values())} row(s) whose file is not here or could "
                f"not be read: {_counts(plan.unread)}",
            )
        )
    if plan.joining:
        found.append(
            _check(
                "backlog.joining",
                "moved into needs genre",
                f"{len(plan.joining)} row(s) adoption files today that {backlog.ROWS_VERB} "
                f"would give a genre no folder takes",
            )
        )
    projected = plan.projected()
    found.append(
        _check(
            "backlog.projected",
            "needs genre",
            f"{projected['now']} row(s) need a genre now of {plan.tracks}; "
            f"{projected['no_word_answered']} after the campaign with no word "
            f"answered, {projected['every_word_answered']} with every word given "
            f"its widest answer",
        )
    )
    return found


def _counts(counted) -> str:
    return ", ".join(f"{count} {name}" for name, count in counted.items() if count)


def _payload(plan: backlog.Backlog) -> dict[str, Any]:
    """The backlog as the envelope carries it, a ``diagnostic/1`` payload."""
    return {
        "checks": checks(plan),
        "summary": {
            "digest": plan.digest,
            "count": len(plan.rows),
            "tracks": plan.tracks,
            "floor": backlog.FLOOR,
            "catalogue": plan.catalogue,
            "catalogue_answers": (
                suggest.catalogue_counts(_asked_rows(plan)) if plan.catalogue else None
            ),
            "causes": plan.counts,
            "statuses": plan.statuses,
            "words": [word.to_json() for word in plan.words],
            "campaign": plan.campaign(),
            "remainder": plan.remainder(),
            "projected": plan.projected(),
            "unread": dict(plan.unread),
            "joining": list(plan.joining),
            "items": [row.to_json() for row in plan.rows],
        },
    }


def tag_backlog(ctx) -> Envelope:
    """Sort the needs genre backlog by cause and name the campaign. Writes nothing."""
    cfg = load_config(("tagging.backlog_cli",))
    declared = active_taxonomy.load(cfg)
    plan = read_plan(
        cfg, declared, bool(getattr(ctx.args, "catalogue", False)), getattr(ctx, "progress", None)
    )
    return ctx.envelope(
        data=_payload(plan),
        outcome=Outcome.OK if plan.rows or plan.unread or plan.joining else Outcome.NO_OP,
        warnings=advisories(plan),
    )


__all__ = [
    "CATALOGUE_UNREAD", "FILES_UNREAD", "LIBRARY_ALONE", "REMAINDER", "ROWS_JOINING", "WORDS_ASKED",
    "advisories", "build", "checks", "named", "read_plan", "tag_backlog",
]
