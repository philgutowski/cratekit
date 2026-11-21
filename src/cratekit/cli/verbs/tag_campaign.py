"""``crate tag campaign``: apply the needs genre backlog under one gate (U294).

WHAT IT ANSWERS. ``tag backlog`` (U292) sorts every row adoption leaves under
needs genre by cause and names the existing gated verbs that settle it, in
order. Driving them by hand is five verbs and five gates. This verb is that
campaign under one approval: one gate over the backlog plan and every word a
person answered, and then each step through its own verb's plan and apply.

A COMPOSER, as ``crate organize`` is (U112). It owns the order, the one gate
and the stop, and no write of its own: every row is written by ``tag rows``'s
or ``tag suggest``'s apply, every file by ``tag suggest``'s or ``taxonomy
alias``'s, and the copy by ``taxonomy alias``'s or ``taxonomy folder``'s.

THE ORDER IS ``tag rows``'S, and for its reasons:

* the backup acknowledgment is read before the plan and the gate (R-733);
* the backlog is planned on a handle opened to read, by ``tag backlog``'s own
  plan, and a library most of whose rows are under no prefix rule refuses;
* the answers are checked against the plan, and each one the verbs' own
  edits would refuse is refused, all before the gate and before any write;
* the gate is asked over one digest, the backlog's and the answers', AND AN
  EMPTY PLAN STILL ASKS. The run that answers rebuilds the backlog, so a
  library or an answer that moved refuses as stale with nothing written.

THE DIGEST NAMES NO COPY. The backlog's covers its rows and words and no path,
and the answers are words and genres, so a rehearsal on a disposable copy
digests equal to the live plan, and ``--rehearsed`` sets the rehearsal's digest
beside the live one at the gate for CLAUDE.md's rehearsal rule. It is shown and
never digested: the answer binds the plan.

THE STEPS, EACH PLANNED ON THE LIBRARY THE STEPS BEFORE IT LEFT (R-1732):

1. ``tag rows``, narrowed to the rows the backlog served. A row it would move
   into needs genre (R-1734), or any other routed row whose file differs, was
   never shown, and is held out.
2. ``tag suggest`` at the backlog's floor, narrowed to the proposals the backlog
   showed with the genre it showed. One that appeared or moved since, as a
   row's neighbours read the first step's genres, is left and named, so no
   genre is written that was not shown or that the floor would not give now.
3. The words: each settled word's one answer, then each answered word through
   ``taxonomy alias`` or ``taxonomy folder``'s own plan and apply.
4. ``tag rows`` again, narrowed to the rows of the words the third step answered.
5. ``route resort`` is NAMED, NOT RUN. Its adds are known only once the steps
   have written, and its gate binds those adds, so this answer cannot stand for
   them without one minted for a plan nobody was shown (U294's question for
   Phillip; the conservative answer is built).

A STEP THAT REFUSES STOPS THE CAMPAIGN THERE. Each step is its own verb's
session, so what landed stays landed. The refusal is the step's own, reworded
to name each step that landed with its count, the step that refused, and the
steps not run, with the whole report in its detail. A second run plans only
what is left.

NEEDS GENRE IS MEASURED, before the campaign and after each step, by the
backlog's own census (R-1737), never projected.

THE GATE TAKES NO INLINE ANSWER, for the reason ``tag rows`` gives (R34).

Layer: cli. It names the verbs it composes, ``taxonomy alias`` and ``taxonomy
folder`` among them, which live on this layer.
"""

from __future__ import annotations

import argparse
import dataclasses
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cratekit.cli import output, registry
from cratekit.cli.output import Envelope
from cratekit.cli.verbs import taxonomy_word
from cratekit.core import active_taxonomy, config, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import backlog, backlog_cli, rows, rows_cli, suggest, suggest_cli

if TYPE_CHECKING:  # pragma: no cover
    from cratekit.cli import Context

#: The explicit gate the whole campaign is asked behind.
CONFIRM_GATE = "tag.campaign.approve"

#: The gate's go option.
APPLY = "apply"

#: The name the digest is taken under.
WORKFLOW = "tag-campaign"

#: The steps, in the order they run.
ROWS = "rows"
SUGGEST = "suggest"
WORDS = "words"
FOLLOW = "follow"
RESORT = "resort"
STEPS: tuple[str, ...] = (ROWS, SUGGEST, WORDS, FOLLOW, RESORT)

#: How a refusal and a report name each step.
TITLES = {
    ROWS: backlog.ROWS_VERB,
    SUGGEST: backlog.SUGGEST_VERB,
    WORDS: "the words",
    FOLLOW: "tag rows again",
    RESORT: "route resort",
}

#: What became of a step.
LANDED = "landed"
EMPTY = "nothing-to-write"
REFUSED = "refused"
NOT_RUN = "not-run"
NEXT = "next"

#: The notes the verb carries on its warnings channel.
CAMPAIGN_LANDED = "campaign-landed"
NOTHING = "campaign-nothing-to-write"
MOVED = "campaign-moved-since-plan"
RESORT_NEXT = "campaign-resort-next"
REMAINDER = "campaign-remainder"
WORDS_LEFT = "campaign-words-left"

#: How many identifiers or words a sentence names. The data carries all.
_NAMED = 5

_ORIGIN = ("cli", "verbs", "tag_campaign")


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
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    """Declare the verb. The answers are its only arguments, besides the catalogue."""
    del entry
    parser.add_argument(
        "--alias",
        action="append",
        default=[],
        metavar="WORD=GENRE",
        help=(
            "answer a word tag backlog asks about with an alias of one of your "
            "genre folders; repeat it for each word, and give the same answers on "
            "the run that applies"
        ),
    )
    parser.add_argument(
        "--folder",
        action="append",
        default=[],
        dest="folder_word",
        metavar="WORD",
        help="answer a word tag backlog asks about with a genre folder of its own",
    )
    parser.add_argument(
        "--leave-word",
        action="append",
        default=[],
        dest="leave_word",
        metavar="WORD",
        help="leave a word tag backlog asks about for hand tagging",
    )
    parser.add_argument(
        "--catalogue",
        action="store_true",
        help=(
            "weigh the catalogues' answers as tag backlog --catalogue does, reading "
            "the answers it kept"
        ),
    )
    parser.add_argument(
        "--rehearsed",
        default=None,
        metavar="DIGEST",
        help=(
            "the digest a rehearsal on a disposable copy showed, set beside this "
            "plan's at the gate; shown, never digested"
        ),
    )
    parser.set_defaults(_handler=tag_campaign)


def _confirm_gate(entry: registry.Entry) -> registry.GateSpec:
    """The verb's own gate by name, never by position, as ``tag rows`` finds it."""
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


# ---------------------------------------------------------------------------
# The answers
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Answer:
    """One word's answer: an alias of ``genre``, its own folder, or left."""

    word: str
    answer: str
    genre: str = ""

    def to_json(self) -> dict[str, str]:
        return {"word": self.word, "answer": self.answer, "genre": self.genre}


def _invalid(message: str, **detail: Any) -> CratekitError:
    return refuse(
        "review-selection-invalid",
        f"{message}; nothing was written",
        origin=_ORIGIN,
        detail=detail,
    )


def _asked(plan: backlog.Backlog) -> str:
    asked = [word.spelling for word in plan.words if word.options]
    if not asked:
        return "the backlog asks about no word"
    shown = ", ".join(asked[:_NAMED]) + (f" and {len(asked) - _NAMED} more" if len(asked) > _NAMED else "")
    return f"the words it asks about: {shown}"


def answers(
    plan: backlog.Backlog,
    *,
    alias: list[str],
    folder: list[str],
    leave_word: list[str],
) -> tuple[Answer, ...]:
    """Each answer given, matched to its word in the plan, in the plan's word order.

    REFUSED BEFORE ANYTHING IS WRITTEN when an alias is not ``WORD=GENRE``, a
    word names none the backlog asks about in any of its spellings, a word is
    answered twice, or the word is not one the backlog asks: a settled word,
    whose one answer the campaign runs anyway, or one neither verb takes. The
    answer carries the plan's spelling, so two cases of one word on the command
    line are one answer and one digest.
    """
    given: list[tuple[str, str, str, str]] = []
    for value in alias:
        word, sep, genre = value.partition("=")
        word, genre = word.strip(), genre.strip()
        if not sep or not word or not genre:
            raise _invalid(f"--alias {value!r} is not WORD=GENRE", alias=value)
        given.append((word, backlog.ALIAS, genre, f"--alias {value!r}"))
    given.extend((value.strip(), backlog.FOLDER, "", f"--folder {value!r}") for value in folder)
    given.extend((value.strip(), backlog.LEAVE, "", f"--leave-word {value!r}") for value in leave_word)

    by_fold: dict[str, backlog.Word] = {}
    for word in plan.words:
        for spelling, _count in word.spellings:
            by_fold[spelling.casefold()] = word
    found: dict[str, Answer] = {}
    for spelling, kind, genre, flag in given:
        word = by_fold.get(spelling.casefold())
        if word is None:
            raise _invalid(
                f"{flag} names no word the backlog asks about; {_asked(plan)}", word=spelling
            )
        if word.settled:
            raise _invalid(
                f"{flag} answers {word.spelling!r}, which has one answer, {word.settled}, "
                f"and the campaign runs it with no answer given",
                word=word.spelling,
            )
        if word.unanswerable is not None:
            raise _invalid(
                f"{flag} answers {word.spelling!r}, which cannot be answered: "
                f"{word.unanswerable[1]}",
                word=word.spelling,
                why=word.unanswerable[0],
            )
        if word.spelling in found:
            raise _invalid(f"{flag} answers {word.spelling!r}, which is answered twice", word=word.spelling)
        found[word.spelling] = Answer(word.spelling, kind, genre)
    order = {word.spelling: index for index, word in enumerate(plan.words)}
    return tuple(sorted(found.values(), key=lambda answer: order[answer.word]))


def check_edits(cfg: config.Config, given: tuple[Answer, ...]) -> None:
    """Plan every answer's edit of the copy, in order, and refuse one the verbs refuse.

    THE VERBS' OWN EDITS, ``taxonomy alias``'s and ``taxonomy folder``'s, each on
    the text the answers before it leave, so an answer that refuses, or two
    that cannot both be written, refuse here with the verb's own words before
    the gate. Nothing is saved.
    """
    writing = [answer for answer in given if answer.answer != backlog.LEAVE]
    if not writing:
        return
    path, text = active_taxonomy.read_text(cfg)
    if text is None:
        raise refuse(
            "config-unusable",
            f"this library has no active taxonomy copy at {path}, so there is nothing to "
            f"answer a word in; setup makes one; nothing was written",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
            detail={"path": str(path)},
        )
    for answer in writing:
        if answer.answer == backlog.ALIAS:
            text = taxonomy_word.edit_alias(text, answer.word, answer.genre).after
        else:
            text = taxonomy_word.edit_folder(text, answer.word).after


def digest(plan: backlog.Backlog, given: tuple[Answer, ...]) -> str:
    """The fingerprint the one approval binds to: the backlog's and the answers'.

    NOTHING THAT NAMES A COPY: the backlog's digest names none, and the answers
    are words and genres, so a rehearsal on a disposable copy digests equal to
    the live plan.
    """
    return output.digest_of(
        {
            "kind": WORKFLOW,
            "backlog": plan.digest,
            "answers": [answer.to_json() for answer in given],
        }
    )


# ---------------------------------------------------------------------------
# What the gate shows
# ---------------------------------------------------------------------------


def _settled(plan: backlog.Backlog) -> list[backlog.Word]:
    """The settled words the campaign runs: those whose one answer moves a row."""
    return [word for word in plan.words if word.settled and word.reached]


def _items(plan: backlog.Backlog, given: tuple[Answer, ...]) -> list[dict[str, Any]]:
    """Every write the campaign will make, as the backlog showed it."""
    items: list[dict[str, Any]] = []
    for row in plan.rows:
        if row.status == backlog.SERVED:
            items.append(
                {"kind": ROWS, "content_id": row.content_id, "row": row.row_word, "file": row.file_word}
            )
    for row in plan.proposals:
        proposal = row.proposal
        items.append(
            {
                "kind": SUGGEST,
                "content_id": row.content_id,
                "genre": proposal.genre,
                "band": proposal.band,
                "share": proposal.share,
                "source": proposal.source,
                "source_genre": proposal.source_genre,
            }
        )
    for word in _settled(plan):
        items.append(
            {
                "kind": WORDS,
                "word": word.spelling,
                "answer": "settled",
                "genre": word.settled_genre,
                "command": word.settled,
                "rows": len(word.reached),
            }
        )
    for answer in given:
        if answer.answer != backlog.LEAVE:
            items.append({"kind": WORDS, **answer.to_json()})
    return items


def _payload(plan: backlog.Backlog, given: tuple[Answer, ...]) -> dict[str, Any]:
    items = _items(plan, given)
    return {
        "digest": digest(plan, given),
        "items": items,
        "totals": {
            "count": len(items),
            "catalogue": plan.catalogue,
            "floor": backlog.FLOOR,
            "answers": [answer.to_json() for answer in given],
            "steps": [],
            "needs_genre": {"before": len(plan.rows), "after": len(plan.rows)},
        },
        "chunk": None,
    }


def _unanswered(plan: backlog.Backlog, given: tuple[Answer, ...]) -> list[str]:
    answered = {answer.word for answer in given}
    return [word.spelling for word in plan.words if word.options and word.spelling not in answered]


def _facts(
    plan: backlog.Backlog, given: tuple[Answer, ...], data: dict[str, Any], rehearsed: str | None
) -> dict[str, Any]:
    """What the gate puts in front of the items."""
    facts: dict[str, Any] = {
        "needs_genre": len(plan.rows),
        "causes": plan.counts,
        "floor": backlog.FLOOR,
        "catalogue": plan.catalogue,
        "answers": [answer.to_json() for answer in given],
        "unanswered": _unanswered(plan, given),
        "campaign": plan.campaign(),
        "joining": len(plan.joining),
        "resort": f"named, not run: {backlog.RESORT_VERB} asks its own gate over its adds",
    }
    if rehearsed is not None:
        facts["rehearsed"] = {"digest": rehearsed, "matches": rehearsed == data["digest"]}
    return facts


# ---------------------------------------------------------------------------
# The steps
# ---------------------------------------------------------------------------


@dataclass
class Step:
    """What one step did. ``counted`` is rows, or files for the words."""

    key: str
    state: str = NOT_RUN
    planned: int = 0
    written: int = 0
    read_back: int = 0
    files: int = 0
    held: int = 0
    moved: list[str] = field(default_factory=list)
    left: dict[str, str] = field(default_factory=dict)
    sessions: list[str] = field(default_factory=list)
    words: list[dict[str, Any]] = field(default_factory=list)
    needs_genre_after: int | None = None
    sentences: list[dict[str, str]] = field(default_factory=list)
    error: CratekitError | None = None

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "step": self.key,
            "command": TITLES[self.key] if self.key != RESORT else backlog.RESORT_VERB,
            "state": self.state,
            "planned": self.planned,
            "written": self.written,
            "read_back": self.read_back,
            "held": self.held,
            "moved": list(self.moved),
            "left": dict(self.left),
            "sessions": list(self.sessions),
            "needs_genre_after": self.needs_genre_after,
        }
        if self.key == WORDS:
            out["files"] = self.files
            out["words"] = list(self.words)
        if self.error is not None:
            out["refused"] = {"reason": self.error.cause.reason, "message": self.error.cause.message}
        return out

    def said(self) -> str:
        """The step as one clause of a sentence."""
        if self.key == WORDS:
            return f"{TITLES[self.key]} {self.state}, {len(self.words)} word(s) and {self.files} file(s)"
        return f"{TITLES[self.key]} {self.state}, {self.written} row(s)"


def _needing(cfg: config.Config, declared) -> int:
    """Needs genre now, by the backlog's own census, through a handle opened to read."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return len(backlog.needing(cfg, db, declared))
    finally:
        rb_writer.close_db(db)


def _rows_step(
    cfg: config.Config, declared, step: Step, keep: frozenset[str], *, served: bool
) -> None:
    """``tag rows``, its own plan and apply, narrowed to the rows ``keep`` names.

    ``served`` says each kept row is one the backlog showed this verb writing,
    as the first step's are; the fourth step's are a word's rows, some of which
    agree with their file already.
    """
    step.planned = len(keep)
    if not keep:
        step.state = EMPTY
        return
    whole = rows_cli.plan_library(cfg, declared, [])
    narrowed = rows.narrowed(whole, keep)
    step.held = len(whole.writes) - len(narrowed.writes)
    writing = {item.content_id for item in narrowed.writes}
    # A KEPT ROW THE VERB LEAVES keeps the verb's own reason, a word with no
    # genre row above all, which ``tag rows`` links and never makes.
    step.left = {
        item.content_id: item.reason
        for item in whole.items
        if item.content_id in keep and item.action == rows.LEAVE
    }
    if served:
        # A SERVED ROW THE VERB NO LONGER WRITES moved since the plan showed it.
        step.moved = sorted(keep - writing - set(step.left))
    if not writing:
        step.state = EMPTY
        return
    written = rows_cli.apply_plan(cfg, narrowed)
    step.written, step.read_back = written.written, written.read_back
    step.sessions.append(written.session_id)
    step.state = LANDED


def _suggest_step(
    cfg: config.Config, declared, step: Step, plan: backlog.Backlog, progress
) -> None:
    """``tag suggest`` at the floor, its own plan and apply, narrowed to what was shown."""
    keep = {row.content_id: row.proposal.genre for row in plan.proposals}
    step.planned = len(keep)
    if not any(row.cause == backlog.NO_GENRE for row in plan.rows):
        step.state = EMPTY
        return
    whole = suggest_cli.plan_library(
        cfg,
        declared,
        band=backlog.FLOOR,
        leave=[],
        chosen={},
        catalogue=plan.catalogue,
        progress=progress,
    )
    narrowed = suggest.narrowed(whole, keep)
    now = {item.content_id: item.genre for item in whole.writes}
    step.held = len(whole.writes) - len(narrowed.writes)
    step.moved = sorted(
        content_id for content_id in set(keep) | set(now) if keep.get(content_id) != now.get(content_id)
    )
    if not narrowed.writes:
        step.state = EMPTY
        return
    written = suggest_cli.apply_plan(cfg, narrowed)
    step.written, step.read_back = written.written, written.read_back
    step.sessions.append(written.session_id)
    step.state = LANDED


def _words_step(
    cfg: config.Config,
    spec: registry.GateSpec,
    run_id: str,
    step: Step,
    plan: backlog.Backlog,
    given: tuple[Answer, ...],
) -> None:
    """Each settled word's one answer, then each answered word, by the verbs' own apply."""
    todo: list[tuple[str, str, str]] = [
        (word.spelling, "settled", word.settled_genre) for word in _settled(plan)
    ]
    todo += [(answer.word, answer.answer, answer.genre) for answer in given if answer.answer != backlog.LEAVE]
    step.planned = len(todo)
    for spelling, kind, genre in todo:
        if kind == backlog.FOLDER:
            planned_folder = taxonomy_word.plan_folder(cfg, spelling)
            made = planned_folder.edit.writes
            if made:
                step.sentences += taxonomy_word.apply_folder(cfg, spec, run_id, planned_folder)
            step.words.append({"word": spelling, "answer": kind, "folder_made": made, "files": 0})
            continue
        planned = taxonomy_word.plan_alias(cfg, spelling, genre)
        files = len(planned.files.of(taxonomy_word.WRITE))
        if planned.writes:
            step.sentences += taxonomy_word.apply_alias(cfg, spec, run_id, planned)
        step.files += files
        step.words.append(
            {
                "word": spelling,
                "answer": kind,
                "genre": planned.edit.display,
                "alias_saved": planned.edit.writes,
                "files": files,
            }
        )
    step.state = (
        LANDED
        if step.files or any(word.get("alias_saved") or word.get("folder_made") for word in step.words)
        else EMPTY
    )


def _followers(plan: backlog.Backlog, given: tuple[Answer, ...]) -> frozenset[str]:
    """The rows of every word the third step answered, which ``tag rows`` follows."""
    answered = {word.spelling.casefold() for word in _settled(plan)}
    answered |= {answer.word.casefold() for answer in given if answer.answer != backlog.LEAVE}
    return frozenset(
        row.content_id
        for row in plan.rows
        if row.cause == backlog.OFF_TAXONOMY and row.word.casefold() in answered
    )


# ---------------------------------------------------------------------------
# The report and the stop
# ---------------------------------------------------------------------------


def _named(values: list[str]) -> str:
    shown = ", ".join(values[:_NAMED])
    more = len(values) - _NAMED
    return shown + (f" and {more} more" if more > 0 else "")


def _report(data: dict[str, Any], steps: list[Step], before: int, after: int) -> dict[str, Any]:
    data["totals"] = {
        **data["totals"],
        "steps": [step.to_json() for step in steps],
        "needs_genre": {"before": before, "after": after},
    }
    return data


def _stopped(steps: list[Step], failed: Step, data: dict[str, Any]) -> CratekitError:
    """The step's own refusal, reworded to name what landed and what did not run."""
    landed = [step.said() for step in steps if step.state == LANDED]
    not_run = [TITLES[step.key] for step in steps if step.state == NOT_RUN]
    error = failed.error
    cause = error.cause
    said = (
        f"{cause.message}. The campaign stopped at {TITLES[failed.key]}: "
        + ("; ".join(landed) if landed else "no step landed")
        + (f"; not run: {', '.join(not_run)}" if not_run else "")
        + "; what landed stays landed, and a second run plans only what is left"
    )
    return rebuilt(
        error,
        dataclasses.replace(
            cause,
            message=said,
            origin=(*cause.origin, *_ORIGIN),
            detail={**dict(cause.detail or {}), "campaign": data["totals"]},
        ),
    )


def _warnings(
    plan: backlog.Backlog,
    given: tuple[Answer, ...],
    steps: list[Step],
    before: int,
    after: int,
) -> list[dict[str, str]]:
    found: list[dict[str, str]] = [
        {
            "code": CAMPAIGN_LANDED,
            "message": (
                f"needs genre {before} before the campaign and {after} after: "
                + "; ".join(step.said() for step in steps if step.key != RESORT)
            ),
        }
    ]
    for step in steps:
        found.extend(step.sentences)
    moved = [content_id for step in steps for content_id in step.moved]
    if moved:
        found.append(
            {
                "code": MOVED,
                "message": (
                    f"{len(moved)} row(s) were not as the plan showed them once the steps "
                    f"before reached them, {_named(moved)}, and were left; a row is "
                    f"written only as it was shown, and the next run shows each again"
                ),
            }
        )
    resort = steps[STEPS.index(RESORT)]
    if resort.state == NEXT:
        found.append(
            {
                "code": RESORT_NEXT,
                "message": (
                    f"the tracks the campaign gave a genre are not yet filed into BY "
                    f"GENRE + ENERGY: run {backlog.RESORT_VERB}, which shows every add "
                    f"before it files and asks its own gate"
                ),
            }
        )
    left = _unanswered(plan, given) + [
        answer.word for answer in given if answer.answer == backlog.LEAVE
    ]
    if left:
        found.append(
            {
                "code": WORDS_LEFT,
                "message": (
                    f"{len(left)} word(s) were left for hand tagging, {_named(left)}; "
                    f"answer one with --alias WORD=GENRE or --folder WORD on a later run"
                ),
            }
        )
    if after:
        remainder = plan.remainder()
        reasons = "; ".join(
            f"{entry['rows']} {entry['cause']} ({entry['reason']}), {entry['settle']}"
            for entry in remainder[:_NAMED]
        )
        found.append(
            {
                "code": REMAINDER,
                "message": (
                    f"{after} row(s) still need a genre"
                    + (f"; left by hand: {reasons}" if reasons else "")
                ),
            }
        )
    return found


def tag_campaign(ctx: "Context") -> Envelope:
    """Plan the backlog, check the answers, ask once, then run each step in order."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    spec = _confirm_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    args = ctx.args
    progress = getattr(ctx, "progress", None)
    plan = backlog_cli.plan_library(cfg, declared, bool(args.catalogue), progress)
    given = answers(
        plan,
        alias=list(args.alias or ()),
        folder=list(args.folder_word or ()),
        leave_word=list(args.leave_word or ()),
    )
    check_edits(cfg, given)
    data = _payload(plan, given)
    facts = _facts(plan, given, data, getattr(args, "rehearsed", None))
    if ctx.gate.require(spec, plan=data, context=facts) != APPLY:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
    before = len(plan.rows)
    if not data["items"]:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": NOTHING,
                    "message": (
                        f"the campaign has nothing to write: {before} row(s) need a genre "
                        f"and no step the backlog names would move one"
                    ),
                }
            ],
        )

    steps = [Step(key) for key in STEPS]
    by_key = {step.key: step for step in steps}
    run_id = ctx.run.run_id
    served = frozenset(row.content_id for row in plan.rows if row.status == backlog.SERVED)
    work = (
        (ROWS, lambda d: _rows_step(cfg, d, by_key[ROWS], served, served=True)),
        (SUGGEST, lambda d: _suggest_step(cfg, d, by_key[SUGGEST], plan, progress)),
        (WORDS, lambda d: _words_step(cfg, spec, run_id, by_key[WORDS], plan, given)),
        (FOLLOW, lambda d: _rows_step(cfg, d, by_key[FOLLOW], _followers(plan, given), served=False)),
    )
    after = before
    for key, run in work:
        step = by_key[key]
        try:
            run(declared)
        except CratekitError as exc:
            step.state, step.error = REFUSED, exc
        except Exception as exc:  # noqa: BLE001 - raised below, never swallowed
            # ANY OTHER FAILURE IS THIS BUILD'S OWN, and it is the step's: it
            # is raised naming what landed, as organize names its steps.
            step.state = REFUSED
            step.error = refuse(
                "internal-error",
                f"{TITLES[key]} failed in a way this build does not expect "
                f"({type(exc).__name__}: {exc})",
                remedy=Remedy.REPORT_DEFECT,
                origin=_ORIGIN,
                detail={"step": key, "kind": type(exc).__name__},
            )
        if step.state == REFUSED:
            raise _stopped(steps, step, _report(data, steps, before, after))
        if key == WORDS and step.state == LANDED:
            # THE COPY MOVED, so the rows that follow are planned on it.
            declared = active_taxonomy.load(cfg)
        if step.state == LANDED:
            after = _needing(cfg, declared)
        step.needs_genre_after = after
    landed = any(step.state == LANDED for step in steps)
    by_key[RESORT].state = NEXT if landed else EMPTY
    _report(data, steps, before, after)
    return ctx.envelope(
        data=data,
        outcome=Outcome.OK if landed else Outcome.NO_OP,
        warnings=_warnings(plan, given, steps, before, after),
    )


__all__ = [
    "APPLY",
    "CAMPAIGN_LANDED",
    "CONFIRM_GATE",
    "EMPTY",
    "FOLLOW",
    "LANDED",
    "MOVED",
    "NEXT",
    "NOTHING",
    "NOT_RUN",
    "REFUSED",
    "REMAINDER",
    "RESORT",
    "RESORT_NEXT",
    "ROWS",
    "STEPS",
    "SUGGEST",
    "WORDS",
    "WORDS_LEFT",
    "Answer",
    "Step",
    "answers",
    "build",
    "check_edits",
    "digest",
    "tag_campaign",
]
