"""``crate tag campaign``: apply the needs genre backlog under one gate (U294).

A composer, as ``crate organize`` is (U112): it owns the order, the one gate and
the stop, and writes nothing itself. The steps are ``tag rows``, ``tag
suggest`` at the backlog's floor, the words through ``taxonomy alias`` and
``taxonomy folder``, and ``tag rows`` again for the rows those words filed, each
planned on the library the steps before it left (R-1732) and held to what the
gate showed. ``route resort`` is named, not run, since its gate binds adds
known only after the steps write (#851).

The backup acknowledgment is read before the plan (R-733), and every answer is
checked before the gate, which asks over one digest even for an empty plan and
takes no inline answer (R34). The digest names no copy, so a rehearsal digests
equal to the live plan. A step that refuses stops the campaign there, naming
what landed. Needs genre is measured by the backlog's census (R-1737).
"""

from __future__ import annotations

import argparse
import dataclasses
from collections import Counter
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, output, registry, tail
from cratekit.cli.output import Envelope
from cratekit.cli.verbs import taxonomy_word
from cratekit.core import active_taxonomy, config, rb_writer, session
from cratekit.core import taxonomy_word as word_edit
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
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
ROWS_LEFT = "campaign-rows-left"

#: How many identifiers or words a sentence names. The data carries all.
_NAMED = 5

_ORIGIN = ("cli", "verbs", "tag_campaign")


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


def _held_by_copy(declared, spelling: str, kind: str, genre: str) -> bool:
    """Whether the copy already holds this answer to the word: its folder, or the alias."""
    if declared is None:
        return False
    if kind == backlog.FOLDER:
        # Its own name exactly, or in another case, which ``own_folder`` answers.
        return (
            declared.bucket_for_display(spelling) is not None
            or word_edit.own_folder(declared, spelling) is not None
        )
    if kind != backlog.ALIAS:
        return False
    saved = declared.tagging_alias(spelling.lower())
    if saved is None or saved[1] is not None:
        return False
    return genre.casefold() in (saved[0].casefold(), declared.bucket(saved[0]).display.casefold())


def _same_as_settled(word: backlog.Word, kind: str, genre: str) -> bool:
    """Whether an answer is the settled word's own one answer, given again."""
    if kind == backlog.ALIAS:
        return genre.casefold() == word.settled_genre.casefold()
    if kind == backlog.FOLDER:
        return word.settled_genre.casefold() == word.spelling.casefold()
    return False


def answers(
    plan: backlog.Backlog,
    *,
    alias: list[str],
    folder: list[str],
    leave_word: list[str],
    declared=None,
) -> tuple[Answer, ...]:
    """Each answer given, matched to its word in the plan, in the plan's word order.

    Refused before any write when an alias is not ``WORD=GENRE``, or a word is
    unknown, answered twice, settled, or unanswerable. The answer carries the
    plan's spelling, so two cases of one word are one answer. An answer the
    ``declared`` copy already holds is a repeat and is dropped.
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
            if _held_by_copy(declared, spelling, kind, genre):
                continue
            raise _invalid(
                f"{flag} names no word the backlog asks about; {_asked(plan)}", word=spelling
            )
        if word.settled:
            if _same_as_settled(word, kind, genre):
                continue
            raise _invalid(
                f"{flag} answers {word.spelling!r}, which already has its one answer, "
                f"{word.settled}, so it takes none on the command line; the campaign "
                f"runs that answer whenever it moves a row",
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


#: What a settled word's answer is called in a word plan.
SETTLED = "settled"


@dataclass(frozen=True, slots=True)
class WordPlan:
    """One word the third step writes, planned before the gate by the verbs' own plans.

    ``asked`` is the genre as given; ``genre`` is the folder the edit names.
    ``files`` is every file the alias walk found carrying the word, by its path
    under the library root; ``notes`` are that verb's sentences about them.
    """

    word: str
    answer: str
    asked: str
    genre: str
    bucket: str
    like: str
    copy: bool
    files: tuple[dict[str, str], ...] = ()
    notes: tuple[dict[str, str], ...] = ()

    @property
    def retags(self) -> int:
        return sum(1 for item in self.files if item["change"] == taxonomy_word.WRITE)

    def to_json(self) -> dict[str, Any]:
        """What the digest and the gate carry: nothing that names a copy."""
        return {
            "word": self.word,
            "answer": self.answer,
            "genre": self.genre,
            "bucket": self.bucket,
            "like": self.like,
            "copy": self.copy,
            "files": [dict(item) for item in self.files],
        }


def plan_words(
    cfg: config.Config, plan: backlog.Backlog, given: tuple[Answer, ...]
) -> tuple[WordPlan, ...]:
    """Plan every word the third step writes, in order, before the gate. Writes nothing.

    Each edit is the verbs' own, on the text the words before it leave, so a
    refused answer refuses here. Each alias's files are walked as that verb
    walks them, so every retagged file is on the gate and in its digest.
    """
    todo = [(word.spelling, SETTLED, word.settled_genre) for word in _settled(plan)]
    todo += [(answer.word, answer.answer, answer.genre) for answer in given if answer.answer != backlog.LEAVE]
    if not todo:
        return ()
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
    root = taxonomy_word.library_root(cfg, None)
    found: list[WordPlan] = []
    for spelling, kind, genre in todo:
        if kind == backlog.FOLDER:
            edit = taxonomy_word.edit_folder(text, spelling)
            found.append(
                WordPlan(spelling, kind, "", edit.display, edit.bucket_id, edit.like or "", edit.writes)
            )
        else:
            edit = taxonomy_word.edit_alias(text, spelling, genre)
            files = taxonomy_word.carrying(root, edit.word, edit.display)
            found.append(
                WordPlan(
                    spelling,
                    kind,
                    genre,
                    edit.display,
                    edit.bucket_id,
                    "",
                    edit.writes,
                    files=tuple(item.to_json(edit.display) for item in files.items),
                    notes=tuple(taxonomy_word.file_notes(files)),
                )
            )
        text = edit.after
    return tuple(found)


def digest(
    plan: backlog.Backlog, given: tuple[Answer, ...], words: tuple[WordPlan, ...] = ()
) -> str:
    """The fingerprint the one approval binds to: the backlog, the answers and the words.

    Nothing in it names a copy, so a rehearsal digests equal to the live plan.
    """
    return output.digest_of(
        {
            "kind": WORKFLOW,
            "backlog": plan.digest,
            "answers": [answer.to_json() for answer in given],
            "words": [word.to_json() for word in words],
        }
    )


# ---------------------------------------------------------------------------
# What the gate shows
# ---------------------------------------------------------------------------


def _settled(plan: backlog.Backlog) -> list[backlog.Word]:
    """The settled words the campaign runs: those whose one answer moves a row."""
    return [word for word in plan.words if word.settled and word.reached]


def _items(plan: backlog.Backlog, words: tuple[WordPlan, ...]) -> list[dict[str, Any]]:
    """Every write the campaign plans before the gate: rows, proposals, words, files."""
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
    for word in words:
        shown = word.to_json()
        files = shown.pop("files")
        items.append({"kind": WORDS, **shown, "retags": word.retags})
        items.extend({**item, "kind": "file", "word": word.word} for item in files)
    return items


def _payload(
    plan: backlog.Backlog, given: tuple[Answer, ...], words: tuple[WordPlan, ...]
) -> dict[str, Any]:
    items = _items(plan, words)
    return {
        "digest": digest(plan, given, words),
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


#: The backlog's own notes the campaign carries to its report.
_CARRIED = (
    backlog_cli.FILES_UNREAD,
    backlog_cli.CATALOGUE_UNREAD,
    backlog_cli.LIBRARY_ALONE,
    backlog_cli.ROWS_JOINING,
)


def _notes(plan: backlog.Backlog, words: tuple[WordPlan, ...]) -> list[dict[str, str]]:
    """What the composed verbs say they could not read or left, in their own words.

    A gate standing for those verbs shows what each would show at its own.
    """
    found = [
        note
        for note in backlog_cli.advisories(plan)
        if note["code"] in _CARRIED and note["code"] != backlog_cli.ROWS_JOINING
    ]
    if plan.joining:
        # In the campaign's own words, since the backlog's names a flag this
        # verb does not take.
        found.append(
            {
                "code": backlog_cli.ROWS_JOINING,
                "message": (
                    f"{backlog.ROWS_VERB} would write a genre no folder takes onto "
                    f"{len(plan.joining)} row(s) adoption files today, "
                    f"{backlog_cli.named(list(plan.joining))}, moving them into needs genre; the "
                    f"campaign holds each of them out and writes them nothing"
                ),
            }
        )
    for word in words:
        found.extend(
            {"code": note["code"], "message": f"{word.word}: {note['message']}"} for note in word.notes
        )
    return found


def _facts(
    plan: backlog.Backlog,
    given: tuple[Answer, ...],
    words: tuple[WordPlan, ...],
    data: dict[str, Any],
    rehearsed: str | None,
) -> dict[str, Any]:
    """What the gate puts in front of the items."""
    facts: dict[str, Any] = {
        "needs_genre": len(plan.rows),
        "causes": plan.counts,
        "unread": dict(plan.unread),
        "floor": backlog.FLOOR,
        "catalogue": plan.catalogue,
        "answers": [answer.to_json() for answer in given],
        "unanswered": _unanswered(plan, given),
        "campaign": plan.campaign(),
        "joining": len(plan.joining),
        "retags": sum(word.retags for word in words),
        "notes": [note["message"] for note in _notes(plan, words)],
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
            if self.state == REFUSED:
                return f"{TITLES[self.key]} refused after {len(self.words)} word(s) and {self.files} file(s)"
            return f"{TITLES[self.key]} {self.state}, {len(self.words)} word(s) and {self.files} file(s)"
        if self.state == REFUSED:
            return f"{TITLES[self.key]} refused, and its own sentence says what it wrote"
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


#: Why a follower is held out: its file carries another spelling of the word,
#: so ``tag rows`` would unfile it.
ANOTHER_SPELLING = "file-carries-another-spelling"


def _rows_step(
    cfg: config.Config,
    declared,
    step: Step,
    keep: frozenset[str],
    *,
    served: bool,
    expected: dict[str, str] | None = None,
) -> None:
    """``tag rows``, its own plan and apply, narrowed to the rows ``keep`` names.

    ``served`` marks rows the backlog showed this verb writing. ``expected``
    holds a row to the file word its answer filed, so another spelling is never
    written over it.
    """
    step.planned = len(keep)
    if not keep:
        step.state = EMPTY
        return
    whole = rows_cli.read_plan(cfg, declared, [])
    other = {
        item.content_id
        for item in whole.writes
        if expected is not None and item.content_id in keep and item.file != expected.get(item.content_id)
    }
    narrowed = rows.narrowed(whole, keep - other)
    step.held = len(whole.writes) - len(narrowed.writes)
    writing = {item.content_id for item in narrowed.writes}
    # A kept row the verb leaves keeps the verb's own reason.
    step.left = {
        item.content_id: item.reason
        for item in whole.items
        if item.content_id in keep and item.action == rows.LEAVE
    }
    step.left.update(dict.fromkeys(other, ANOTHER_SPELLING))
    if served:
        # A served row the verb no longer writes moved since the plan.
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
    whole = suggest_cli.read_plan(
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
    words: tuple[WordPlan, ...],
) -> None:
    """Each word the gate showed, by the verbs' own plan and apply, held to what it showed.

    Each word is planned again and refused as stale when its edit or files
    differ from the gate's. A word is recorded once its apply returns, so a
    refusal names the words before it.
    """
    step.planned = len(words)
    for shown in words:
        if shown.answer == backlog.FOLDER:
            folder = taxonomy_word.plan_folder(cfg, shown.word)
            fresh = (folder.edit.display, folder.edit.bucket_id, folder.edit.like or "", folder.edit.writes)
            if fresh != (shown.genre, shown.bucket, shown.like, shown.copy):
                raise gates.DecisionStale(
                    spec, run_id, output.digest_of(shown.to_json()), output.digest_of(list(fresh))
                )
            if folder.edit.writes:
                step.sentences += taxonomy_word.apply_folder(cfg, spec, run_id, folder)
            step.words.append({"word": shown.word, "answer": shown.answer, "folder_made": shown.copy, "files": 0})
            continue
        planned = taxonomy_word.plan_alias(cfg, shown.word, shown.asked)
        files = tuple(item.to_json(planned.edit.display) for item in planned.files.items)
        if (planned.edit.display, files) != (shown.genre, shown.files):
            raise gates.DecisionStale(
                spec,
                run_id,
                output.digest_of([dict(item) for item in shown.files]),
                output.digest_of([dict(item) for item in files]),
            )
        if planned.writes:
            # The verb's advice to run tag rows is dropped; the fourth step does.
            step.sentences += [
                sentence
                for sentence in taxonomy_word.apply_alias(cfg, spec, run_id, planned)
                if sentence["code"] != taxonomy_word.FILES_RETAGGED
            ]
        step.files += shown.retags
        step.words.append(
            {
                "word": shown.word,
                "answer": shown.answer,
                "genre": shown.genre,
                "alias_saved": planned.edit.writes,
                "files": shown.retags,
            }
        )
    step.state = (
        LANDED
        if step.files or any(word.get("alias_saved") or word.get("folder_made") for word in step.words)
        else EMPTY
    )


def _followers(plan: backlog.Backlog, words: tuple[WordPlan, ...]) -> dict[str, str]:
    """The rows of every word the third step wrote, each with the file word it files.

    No cause is checked, since only an off taxonomy row can carry such a word.
    """
    filed = {word.word.casefold(): word.genre for word in words}
    return {
        row.content_id: filed[row.word.casefold()]
        for row in plan.rows
        if row.word.casefold() in filed
    }


# ---------------------------------------------------------------------------
# The report and the stop
# ---------------------------------------------------------------------------


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
    if failed.key == WORDS and failed.words:
        landed.append(failed.said())
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
    words: tuple[WordPlan, ...],
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
    found.extend(_notes(plan, words))
    moved = [content_id for step in steps for content_id in step.moved]
    if moved:
        found.append(
            {
                "code": MOVED,
                "message": (
                    f"{len(moved)} row(s) were not as the plan showed them once the steps "
                    f"before reached them, {backlog_cli.named(moved)}, and were left; a row is "
                    f"written only as it was shown, and the next run shows each again"
                ),
            }
        )
    left = {content_id: reason for step in steps for content_id, reason in step.left.items()}
    if left:
        reasons = "; ".join(
            f"{count} {reason}" for reason, count in sorted(Counter(left.values()).items())
        )
        advice = []
        if rows.GENRE_UNKNOWN in left.values():
            advice.append(
                f"{rows.GENRE_UNKNOWN}: a word with no genre row in the library gets one "
                f"when a track is given that genre in rekordbox, and the next run writes it"
            )
        if ANOTHER_SPELLING in left.values():
            advice.append(
                f"{ANOTHER_SPELLING}: the file carries the word in another spelling than "
                f"the one the answer filed, so writing it would move the row back into "
                f"needs genre; retag the file by hand"
            )
        if set(left.values()) - {rows.GENRE_UNKNOWN, ANOTHER_SPELLING}:
            advice.append(f"any other reason is {backlog.ROWS_VERB}'s own, which names each row")
        found.append(
            {
                "code": ROWS_LEFT,
                "message": (
                    f"{len(left)} row(s) the campaign meant to write were left ({reasons}), "
                    f"{backlog_cli.named(sorted(left))}; " + "; ".join(advice)
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
    words_left = _unanswered(plan, given) + [
        answer.word for answer in given if answer.answer == backlog.LEAVE
    ]
    if words_left:
        found.append(
            {
                "code": WORDS_LEFT,
                "message": (
                    f"{len(words_left)} word(s) were left for hand tagging, {backlog_cli.named(words_left)}; "
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
    cfg = tail.load_config(_ORIGIN)
    declared = active_taxonomy.load(cfg)
    spec = output.confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # Before the plan and the gate (R-733).
    session.assert_backup_acknowledged(cfg)

    args = ctx.args
    progress = getattr(ctx, "progress", None)
    plan = backlog_cli.read_plan(cfg, declared, bool(args.catalogue), progress)
    given = answers(
        plan,
        alias=list(args.alias or ()),
        folder=list(args.folder_word or ()),
        leave_word=list(args.leave_word or ()),
        declared=declared,
    )
    words = plan_words(cfg, plan, given)
    data = _payload(plan, given, words)
    facts = _facts(plan, given, words, data, getattr(args, "rehearsed", None))
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
                },
                *_notes(plan, words),
            ],
        )

    steps = [Step(key) for key in STEPS]
    by_key = {step.key: step for step in steps}
    run_id = ctx.run.run_id
    served = frozenset(row.content_id for row in plan.rows if row.status == backlog.SERVED)
    followers = _followers(plan, words)
    work = (
        (ROWS, lambda d: _rows_step(cfg, d, by_key[ROWS], served, served=True)),
        (SUGGEST, lambda d: _suggest_step(cfg, d, by_key[SUGGEST], plan, progress)),
        (WORDS, lambda d: _words_step(cfg, spec, run_id, by_key[WORDS], words)),
        (
            FOLLOW,
            lambda d: _rows_step(
                cfg, d, by_key[FOLLOW], frozenset(followers), served=False, expected=followers
            ),
        ),
    )
    after = before
    for key, run in work:
        step = by_key[key]
        try:
            run(declared)
        except CratekitError as exc:
            step.state, step.error = REFUSED, exc
        except Exception as exc:  # noqa: BLE001 - raised below, never swallowed
            # Any other failure is a defect, raised naming what landed.
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
            # A refused step may have written part of itself, so needs genre is
            # read again and the refusal's session is kept.
            session_id = (step.error.cause.detail or {}).get("session")
            if session_id:
                step.sessions.append(str(session_id))
            try:
                after = _needing(cfg, active_taxonomy.load(cfg))
            except CratekitError:
                pass
            step.needs_genre_after = after
            raise _stopped(steps, step, _report(data, steps, before, after))
        if key == WORDS and step.state == LANDED:
            # The copy moved, so the rows that follow are planned on it.
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
        warnings=_warnings(plan, given, words, steps, before, after),
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
    "ANOTHER_SPELLING",
    "ROWS_LEFT",
    "STEPS",
    "SUGGEST",
    "WORDS",
    "WORDS_LEFT",
    "Answer",
    "Step",
    "WordPlan",
    "answers",
    "plan_words",
    "build",
    "digest",
    "tag_campaign",
]
