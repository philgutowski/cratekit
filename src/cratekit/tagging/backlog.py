"""The needs genre backlog, sorted by cause, in one plan that writes nothing (U292).

WHY THIS EXISTS. Adoption's census at sitting 94 read 1,345 of 10,737 readable
rows as ``needs-genre``: a row with no genre, one too coarse to be a genre, or
a word no folder takes. Each population has a verb that settles it, ``tag
rows``, ``tag suggest``, ``taxonomy alias`` and ``taxonomy folder``, and no
sitting had swept the backlog with them, because nothing said which row was
whose. This is that census: every ``needs-genre`` row in exactly one cause, the
verb that settles it, and what that verb would do to it today.

EACH VERB'S OWN PLAN, NEVER A SECOND OPINION. A row lagging its file is
counted from :func:`cratekit.tagging.rows.plan_rows` over the same handle, and
a row with no genre from :func:`cratekit.tagging.suggest.plan_suggestions` at
the floor, so those counts are what each verb would write if run next. A
word's answers are planned by the two verbs' own edits,
:func:`cratekit.core.taxonomy_word.alias` and
:func:`cratekit.core.taxonomy_word.folder`, on the library's active copy, so
an answer offered here is one those verbs take, and one they refuse is never
offered (round one of the review found a genre the alias verb refuses
recommended, and a word it takes called unanswerable).

WHAT AN ANSWER MOVES IS COUNTED BY THE ROW, since adoption files by the row.
A folder of the word's name files a row whose row carries that spelling
exactly, or whose file does and ``tag rows`` would write it onto the row. An
alias retags each file whose one genre is the word, and the row follows only
where the library has a genre entry for the alias's genre, which ``tag rows``
links and never creates.

THE CAUSES, in the order a row is tested against them, :data:`CAUSES`:

* ``file-unread``: the file's genre could not be read, so nothing is known;
* ``row-lags-file``: the file carries a genre adoption files by and the row
  does not, which ``tag rows`` writes onto the row;
* ``no-genre``: no genre on the row or the file, which ``tag suggest`` weighs;
* ``too-coarse``: the only word is one the taxonomy calls too coarse to be a
  genre, which ``tag retag`` replaces from the catalogues, per folder;
* ``off-taxonomy``: a word no folder takes, grouped by word, so a person
  answers once per word and not once per track.

A ROW WHOSE FILE IS NOT HERE IS COUNTED, NOT DROPPED. Adoption reads it as
excluded rather than needs genre, so it is in no cause, and whether it needs a
genre is unknown: it is counted by why (round one).

THE FLOOR IS ``tag suggest``'S HIGH BAND, :data:`FLOOR`: at least 80 percent
of the weighted votes over at least six, so a lone catalogue match proposes
and two artist neighbours do not. Nothing below it is proposed; such a row is
the remainder, with its band.

NOTHING HERE WRITES. The plan is read on a handle the caller opened to read,
and the copy's edits are planned on its text and never saved. The one thing a
run keeps is ``tag suggest``'s catalogue answers, in its own state entry, so
the run that applies reads the answers this one read.

Layer: modules. It opens no database of its own and names no verb.
"""

from __future__ import annotations

import shlex
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from cratekit.adopt import collection
from cratekit.adopt import genres as genres_report
from cratekit.adopt import scan as adopt_scan
from cratekit.cli.output import digest_of
from cratekit.core import config, locations, taxonomy
from cratekit.core import taxonomy_word as word_edit
from cratekit.tagging import rows, suggest
from cratekit.write import metadata, trees

#: The name the plan digests under.
WORKFLOW = "tag-backlog"

#: The weakest band proposed. Not a flag: the first live run uses it.
FLOOR = suggest.HIGH

#: The causes, in the order a row is tested against them. Every
#: ``needs-genre`` row lands in exactly one.
FILE_UNREAD = "file-unread"
ROW_LAGS_FILE = "row-lags-file"
NO_GENRE = "no-genre"
TOO_COARSE = "too-coarse"
OFF_TAXONOMY = "off-taxonomy"

CAUSES: tuple[str, ...] = (FILE_UNREAD, ROW_LAGS_FILE, NO_GENRE, TOO_COARSE, OFF_TAXONOMY)

#: What the plan does about a row. ``served`` and ``proposed`` are written by
#: the verb named; ``settled`` by the one answer its word has; ``asked`` waits
#: on its word's question; ``left`` is the remainder, by hand, with a reason.
SERVED = "served"
PROPOSED = "proposed"
SETTLED = "settled"
ASKED = "asked"
LEFT = "left"

STATUSES: tuple[str, ...] = (SERVED, PROPOSED, SETTLED, ASKED, LEFT)

#: The verbs that settle each population, as a person types them.
ROWS_VERB = "crate tag rows"
SUGGEST_VERB = "crate tag suggest"
RETAG_VERB = "crate tag retag"
RESORT_VERB = "crate route resort"

#: The answers a word's question offers.
ALIAS = "alias"
FOLDER = "folder"
LEAVE = "leave"

#: Why a row is left, beside the reasons ``tag rows`` and ``tag suggest`` give.
#: A word neither ``taxonomy alias`` nor ``taxonomy folder`` takes keeps the
#: refusal's own kind, prefixed, so a reader sees which.
UNANSWERABLE = "word-unanswerable"

#: Why a row of a word with one answer is left: that answer does not move it,
#: since its file does not hold the word alone or the library has no genre
#: entry for the answer's genre.
NOT_REACHED = "answer-does-not-reach"

#: The refusal's kind when the library has no active taxonomy copy, which the
#: two verbs refuse too, so no word can be answered in it.
NO_COPY = "no-copy"

#: The bands a word's neighbours must reach for their genre to be offered.
_NEIGHBOURS_AGREE = (suggest.HIGH, suggest.MEDIUM)

_ORIGIN = ("tagging", "backlog")


@dataclass(frozen=True, slots=True)
class Proposal:
    """A genre ``tag suggest`` would write on a row with none, and its evidence.

    ``source`` is the catalogue whose match voted for the genre, or
    :data:`NEIGHBOURS` when only the library voted. ``share`` is the genre's
    weight over every vote, the words no folder takes included, rounded to two
    places; with ``band`` it is the confidence.
    """

    genre: str
    band: str
    share: float
    source: str
    source_genre: str
    votes: tuple[tuple[str, int], ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "genre": self.genre,
            "band": self.band,
            "share": self.share,
            "source": self.source,
            "source_genre": self.source_genre,
            "votes": [[word, weight] for word, weight in self.votes],
        }


#: The source of a proposal only the library voted for.
NEIGHBOURS = "neighbours"


@dataclass(frozen=True, slots=True)
class Row:
    """One ``needs-genre`` row, its cause, and what the campaign does about it.

    ``row_word`` and ``file_word`` are the two genres as read. ``word`` is the
    one the cause is about: the file's on ``row-lags-file``, the off taxonomy or
    too coarse word, and empty otherwise. ``verb`` settles the row, ``reason``
    says why a row is left. ``asked`` is what the catalogue said about a row
    with no genre, when the run asked it.
    """

    content_id: str
    path: str
    artist: str
    title: str
    row_word: str
    file_word: str
    cause: str
    word: str
    status: str
    verb: str = ""
    reason: str = ""
    proposal: Proposal | None = None
    asked: suggest.Asked | None = None

    def digested(self) -> dict[str, Any]:
        """What the digest covers: nothing that names a copy."""
        return {
            "content_id": self.content_id,
            "row_word": self.row_word,
            "file_word": self.file_word,
            "cause": self.cause,
            "word": self.word,
            "status": self.status,
            "verb": self.verb,
            "reason": self.reason,
            "proposal": self.proposal.to_json() if self.proposal else None,
            "catalogue": self.asked.to_json() if self.asked else None,
        }

    def to_json(self) -> dict[str, Any]:
        return {**self.digested(), "path": self.path, "artist": self.artist, "title": self.title}


@dataclass(frozen=True, slots=True)
class Option:
    """One answer a word's question offers, with the rows it would move."""

    answer: str
    label: str
    detail: str
    command: str
    rows: int

    def to_json(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "label": self.label,
            "detail": self.detail,
            "command": self.command,
            "rows": self.rows,
        }


@dataclass(frozen=True, slots=True)
class Word:
    """One off taxonomy word, folded on case, and what answers it.

    ``rows`` carry it. ``files_carry`` have a file whose one genre is the word
    in some case, which an alias retags; ``several`` have a file holding it
    beside another genre, which an alias leaves; ``elsewhere`` carry it on the
    row with a file that does not, which no alias reaches. ``on_row`` would
    carry the commonest spelling exactly on the row once ``tag rows`` has run,
    which a folder of that name files.

    Exactly one of three holds. ``options`` is the question, the
    recommendation first. ``settled`` is the one answer the word has, a
    command that plans no change to the copy and retags its files (another
    case of a folder's name, or an alias already saved), with ``reached`` the
    rows it moves. ``unanswerable`` is the two verbs' refusal, its kind,
    sentence and next step.
    """

    word: str
    rows: int
    spellings: tuple[tuple[str, int], ...]
    files_carry: int
    several: int
    elsewhere: int
    on_row: int
    neighbours: tuple[tuple[str, int], ...]
    options: tuple[Option, ...] = ()
    settled: str = ""
    reached: frozenset[str] = frozenset()
    unanswerable: tuple[str, str, str] | None = None

    @property
    def spelling(self) -> str:
        """The commonest spelling, which a question and a command name."""
        return self.spellings[0][0]

    @property
    def widest(self) -> int:
        """The most rows one answer would move, a folder or an alias."""
        return max((option.rows for option in self.options), default=0)

    def question(self) -> str:
        return (
            f"{self.spelling}: {self.rows} track(s) carry this genre word and no "
            f"genre folder takes it, so they sit under needs genre. How should it "
            f"be answered?"
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "word": self.spelling,
            "rows": self.rows,
            "spellings": [{"genre": word, "rows": count} for word, count in self.spellings],
            "files_carry": self.files_carry,
            "several_genres": self.several,
            "elsewhere": self.elsewhere,
            "on_row": self.on_row,
            "neighbours": [[word, weight] for word, weight in self.neighbours],
            "question": self.question() if self.options else None,
            "options": [option.to_json() for option in self.options],
            "recommended": 0 if self.options else None,
            "settled": self.settled or None,
            "settled_rows": len(self.reached),
            "unanswerable": (
                None
                if self.unanswerable is None
                else dict(zip(("why", "message", "step"), self.unanswerable))
            ),
        }


@dataclass(frozen=True, slots=True)
class Backlog:
    """Every ``needs-genre`` row in one cause, the words, and the campaign.

    ``unread`` counts the live rows adoption excludes because their file is not
    here or cannot be read, by why. ``joining`` names the rows not in the
    backlog that ``tag rows`` would give a genre adoption files nowhere, which
    the campaign's first step moves INTO needs genre.
    """

    rows: tuple[Row, ...]
    words: tuple[Word, ...]
    tracks: int
    catalogue: bool
    unread: Mapping[str, int] = field(default_factory=dict)
    joining: tuple[str, ...] = ()

    @property
    def counts(self) -> dict[str, int]:
        """Rows per cause, zero filled."""
        found = dict.fromkeys(CAUSES, 0)
        for row in self.rows:
            found[row.cause] += 1
        return found

    @property
    def statuses(self) -> dict[str, int]:
        """Rows per status, zero filled."""
        found = dict.fromkeys(STATUSES, 0)
        for row in self.rows:
            found[row.status] += 1
        return found

    @property
    def proposals(self) -> tuple[Row, ...]:
        return tuple(row for row in self.rows if row.status == PROPOSED)

    def remainder(self) -> list[dict[str, Any]]:
        """The rows left by hand, by cause and reason, largest first."""
        seen = Counter((row.cause, row.reason) for row in self.rows if row.status == LEFT)
        ordered = sorted(seen.items(), key=lambda entry: (-entry[1], entry[0]))
        return [
            {"cause": cause, "reason": reason, "rows": count, "settle": settle(cause, reason)}
            for (cause, reason), count in ordered
        ]

    def projected(self) -> dict[str, int]:
        """Needs genre now, after the campaign with no word answered, and with
        every word given its widest answer. A row ``tag rows`` moves into needs
        genre is added back, since the campaign's first step is that verb."""
        now = len(self.rows)
        moved = sum(1 for row in self.rows if row.status in (SERVED, PROPOSED, SETTLED))
        after = now - moved + len(self.joining)
        return {
            "now": now,
            "no_word_answered": after,
            "every_word_answered": after - sum(word.widest for word in self.words),
        }

    def campaign(self) -> list[dict[str, Any]]:
        """The existing gated verbs in the order the campaign runs them.

        Only a step with rows to move is listed, an answered word's counted at
        its alias's rows. ``route resort`` comes last, listed when any step
        moves a row or any word waits on its answer, since it files every
        track the steps give a genre, and then with the rows the steps before
        it move.
        """
        statuses = self.statuses
        steps: list[dict[str, Any]] = []
        if statuses[SERVED]:
            steps.append(
                _step(ROWS_VERB, statuses[SERVED], "rows whose file carries a genre adoption files by")
            )
        if statuses[PROPOSED]:
            command = SUGGEST_VERB + (" --catalogue" if self.catalogue else "")
            steps.append(
                _step(command, statuses[PROPOSED], f"rows with no genre proposed at {FLOOR}")
            )
        settled = [word for word in self.words if word.settled and word.reached]
        for word in settled:
            steps.append(
                _step(word.settled, len(word.reached), "the one answer the word has, retagging its files")
            )
        asked = [word for word in self.words if word.options]
        if asked:
            steps.append(
                _step(
                    f"{word_edit.ALIAS_VERB} WORD GENRE or {word_edit.FOLDER_VERB} WORD",
                    sum(word.widest for word in asked),
                    f"once per answered word, {len(asked)} word(s), at most this many "
                    f"rows; waits on the word questions",
                )
            )
        follow = sum(len(word.reached) for word in settled) + sum(
            option.rows for word in asked for option in word.options if option.answer == ALIAS
        )
        if follow:
            steps.append(
                _step(
                    ROWS_VERB,
                    follow,
                    "the rows follow the files an alias retagged, an answered word's at "
                    "most this many",
                )
            )
        moved = statuses[SERVED] + statuses[PROPOSED] + statuses[SETTLED]
        if moved or asked:
            steps.append(
                _step(
                    RESORT_VERB,
                    moved,
                    "files every track the steps before it gave a genre, and an "
                    "answered word's tracks besides, into its folder",
                )
            )
        return steps

    @property
    def digest(self) -> str:
        """The fingerprint a campaign's approval binds to.

        OVER THE ROWS AND THE WORDS, AND NOTHING THAT NAMES A COPY, for the
        reason :attr:`cratekit.tagging.rows.RowsPlan.digest` gives, so a
        rehearsal on a disposable copy digests equal to the live plan.
        """
        return digest_of(
            {
                "kind": WORKFLOW,
                "floor": FLOOR,
                "catalogue": self.catalogue,
                "rows": [row.digested() for row in self.rows],
                "words": [word.to_json() for word in self.words],
                "unread": dict(self.unread),
                "joining": list(self.joining),
            }
        )


def _step(command: str, moved: int, why: str) -> dict[str, Any]:
    return {"command": command, "rows": moved, "why": why}


def settle(cause: str, reason: str) -> str:
    """What would settle a row left for ``reason``, as a sentence."""
    if cause == FILE_UNREAD:
        return "the file's genre could not be read: check the file opens, then run this again"
    if cause == TOO_COARSE:
        return (
            f"a word too coarse to be a genre: {RETAG_VERB} FOLDER asks the catalogues "
            f"for a better one, then {ROWS_VERB}"
        )
    if reason == rows.GENRE_UNKNOWN or reason == suggest.GENRE_UNKNOWN:
        return (
            "the library has no genre entry for the word yet: give one track the "
            "genre by hand in rekordbox, then run this again"
        )
    if reason == rows.HELD_OUT:
        return "held out by a person: left as they set it"
    if reason == rows.FILE_MULTI_VALUED:
        return "the file holds several genres: choose one on the file by hand"
    if reason in (suggest.BELOW_BAND, suggest.TIED, suggest.NO_VOTES):
        return (
            f"no proposal at {FLOOR}: tag by hand, or {SUGGEST_VERB} --set "
            f"CONTENT_ID=GENRE for a genre you choose"
        )
    if reason == NOT_REACHED:
        return (
            "the word's one answer does not move it, since its file does not hold "
            "the word alone or the library has no genre entry for the answer: tag by hand"
        )
    if reason.startswith(UNANSWERABLE):
        return (
            "neither taxonomy alias nor taxonomy folder takes the word, and the "
            "word's own entry says why and what to do"
        )
    return "tag by hand"


# ---------------------------------------------------------------------------
# The rules, pure
# ---------------------------------------------------------------------------


def cause_of(declared: taxonomy.Taxonomy, row_word: str, file_word: str) -> tuple[str, str]:
    """The cause of one ``needs-genre`` row whose file was read, and its word. Pure.

    A FILE WORD THAT ROUTES IS THE ROW LAGGING ITS FILE, tested first, since
    ``tag rows`` settles it with no question. Otherwise the word is the first of
    the file's and the row's that is not blank and not too coarse, so a specific
    word on either is never hidden behind a catch all on the other.
    """
    row_word, file_word = row_word.strip(), file_word.strip()
    if file_word:
        disposition, _bucket, _match = adopt_scan.classify_genre(declared, file_word)
        if disposition is adopt_scan.Disposition.ROUTE:
            return ROW_LAGS_FILE, file_word
    present = [word for word in (file_word, row_word) if word]
    specific = [word for word in present if not declared.is_too_coarse_as_source(word)]
    if specific:
        return OFF_TAXONOMY, specific[0]
    if present:
        return TOO_COARSE, present[0]
    return NO_GENRE, ""


def proposal_of(item: suggest.Item) -> Proposal:
    """The evidence ``tag suggest`` holds for one row it would write."""
    total = sum(weight for _word, weight in item.votes)
    weight = dict(item.votes).get(item.genre, 0)
    asked = item.catalogue
    voted = (
        asked is not None
        and asked.said == suggest.MATCHED
        and not asked.off_taxonomy
        and asked.genre == item.genre
    )
    return Proposal(
        genre=item.genre,
        band=item.band,
        share=round(weight / total, 2) if total else 0.0,
        source=asked.source if voted and asked is not None else NEIGHBOURS,
        source_genre=asked.source_genre if voted and asked is not None else "",
        votes=item.votes,
    )


def _artist_key(value: str) -> str:
    return " ".join(value.casefold().split())


def _folder_of(recorded: str) -> str:
    text = recorded.strip()
    return text.rsplit("/", 1)[0] if "/" in text else ""


@dataclass(frozen=True, slots=True)
class _Live:
    content_id: str
    artist: str
    folder: str
    genre: str
    title: str


def neighbour_votes(
    members: Iterable[str],
    live: Mapping[str, _Live],
    declared: taxonomy.Taxonomy,
) -> dict[str, int]:
    """What the artist and folder neighbours of a word's rows say, once each. Pure.

    ``tag suggest``'s weights. A neighbour votes once for the whole word, at the
    higher of its weights, so an artist with twenty tracks carrying the word does
    not count each neighbour twenty times. Only a genre adoption files by votes:
    a neighbour carrying another off taxonomy word, or none, says nothing about
    which folder this word belongs in.
    """
    ids = set(members)
    by_artist: dict[str, list[str]] = {}
    by_folder: dict[str, list[str]] = {}
    for other in live.values():
        if other.content_id in ids or not suggest.suggestable(declared, other.genre):
            continue
        if other.artist:
            by_artist.setdefault(_artist_key(other.artist), []).append(other.content_id)
        if other.folder:
            by_folder.setdefault(other.folder, []).append(other.content_id)
    weights: dict[str, int] = {}
    for content_id in ids:
        row = live.get(content_id)
        if row is None:
            continue
        for other in by_folder.get(row.folder, ()) if row.folder else ():
            weights[other] = max(weights.get(other, 0), suggest.FOLDER_WEIGHT)
        for other in by_artist.get(_artist_key(row.artist), ()) if row.artist else ():
            weights[other] = max(weights.get(other, 0), suggest.ARTIST_WEIGHT)
    votes: Counter[str] = Counter()
    for other, weight in weights.items():
        votes[live[other].genre] += weight
    return dict(votes)


def _ordered(votes: Mapping[str, int]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(votes.items(), key=lambda entry: (-entry[1], entry[0])))


def _edit(plan: Callable[[], word_edit.Edit]) -> word_edit.Edit | word_edit.Refused:
    """One of the two verbs' own edits, or its refusal. A copy that does not load
    is a refusal of every answer, as the verbs refuse it."""
    try:
        return plan()
    except word_edit.Refused as refused:
        return refused
    except taxonomy.TaxonomyError as exc:
        return word_edit.Refused(
            NO_COPY,
            f"the active taxonomy copy is not usable: {exc}; it is repaired by hand "
            f"before a word can be answered in it",
        )
    except ValueError as exc:
        # A WORD THE COPY CANNOT HOLD, a control character the TOML parser
        # refuses in the edited text (round two), is an answer the verb cannot
        # write, never a failure of the whole report.
        return word_edit.Refused(
            word_edit.WOULD_NOT_LOAD,
            f"the copy would not load with the word written into it: {exc}",
        )


def _fixed_target(declared: taxonomy.Taxonomy, spelling: str) -> str | None:
    """The genre folder the word already answers to, when it has one: its own
    folder in another case, or the bucket a tagging alias already names."""
    own = word_edit.own_folder(declared, spelling)
    if own is not None:
        return own.display
    saved = declared.tagging_alias(spelling.lower())
    if saved is not None and saved[1] is None:
        return declared.bucket(saved[0]).display
    return None


def word_of(
    declared: taxonomy.Taxonomy,
    text: str | None,
    members: list[Row],
    votes: Mapping[str, int],
    *,
    several: frozenset[str] = frozenset(),
    rows_write: Mapping[str, str] | None = None,
    known: Callable[[str], bool] = lambda genre: True,
) -> Word:
    """One word's counts and what answers it, the recommendation first. Pure.

    ``text`` is the active copy, which each answer is planned on by the verb's
    own edit; None when the library holds none. ``several`` names the rows whose
    file holds the word beside another genre, ``rows_write`` the file word ``tag
    rows`` would write onto each row it would write, and ``known`` whether the
    library has a genre entry for a genre.

    THE RECOMMENDATION. A folder that would file
    :data:`cratekit.adopt.genres.FOLDER_WORTH` rows or more, the threshold
    ``report genres`` names a genre at, is recommended; otherwise the alias the
    neighbours agree on at medium or better; otherwise leaving it for hand
    tagging, the conservative answer, since a wrong alias retags every file
    carrying the word.
    """
    writes = rows_write or {}
    spellings = Counter(row.word for row in members)
    ordered = tuple(sorted(spellings.items(), key=lambda entry: (-entry[1], entry[0])))
    spelling = ordered[0][0]
    folded = spelling.casefold()
    carrying = [row for row in members if row.file_word.casefold() == folded]
    alone = [row for row in carrying if row.content_id not in several]
    on_row = [
        row
        for row in members
        if row.row_word == spelling or writes.get(row.content_id) == spelling
    ]
    base = {
        "word": spelling,
        "rows": len(members),
        "spellings": ordered,
        "files_carry": len(alone),
        "several": len(carrying) - len(alone),
        "elsewhere": len(members) - len(carrying),
        "on_row": len(on_row),
        "neighbours": _ordered(votes),
    }
    if text is None:
        return Word(
            **base,
            unanswerable=(
                NO_COPY,
                "this library has no active taxonomy copy, so taxonomy alias and "
                "taxonomy folder have nothing to answer the word in",
                "crate setup makes one",
            ),
        )

    def reached(genre: str) -> frozenset[str]:
        return frozenset(row.content_id for row in alone) if known(genre) else frozenset()

    fixed = _fixed_target(declared, spelling)
    if fixed is not None:
        edit = _edit(lambda: word_edit.alias(text, spelling, fixed))
        if isinstance(edit, word_edit.Edit) and not edit.writes:
            command = f"{word_edit.ALIAS_VERB} {shlex.join((spelling, edit.display))}"
            return Word(**base, settled=command, reached=reached(edit.display))

    # THE HEAVIEST GENRE ALONE, since at medium or better it holds 60 percent
    # of the votes and no second genre can agree as far. One the alias verb
    # refuses, a style sub or a folder filing by sub, offers no alias at all.
    alias = None
    top = _ordered(votes)[:1]
    band = suggest.band_of(top[0][1], sum(votes.values())) if top else suggest.NONE
    edit = (
        _edit(lambda: word_edit.alias(text, spelling, top[0][0]))
        if band in _NEIGHBOURS_AGREE
        else None
    )
    if isinstance(edit, word_edit.Edit):
        moved = reached(edit.display)
        # THE FILES AND THE ROWS ARE TWO COUNTS (round two): the alias retags
        # every file holding the word alone, and a row follows only where the
        # library has a genre entry for the alias's genre.
        detail = (
            f"the neighbours agree at {band}; {len(alone)} file(s) holding the word "
            f"alone are retagged {edit.display}, and {len(moved)} row(s) follow by "
            f"{ROWS_VERB}, which {RESORT_VERB} files"
        )
        if alone and not moved:
            detail += (
                f"; but the library has no genre entry for {edit.display}, so "
                f"{ROWS_VERB} cannot follow until one track carries it"
            )
        if len(members) > len(moved):
            detail += f"; {len(members) - len(moved)} stay under needs genre"
        alias = Option(
            answer=ALIAS,
            label=f"An alias of {edit.display}",
            detail=detail,
            command=f"{word_edit.ALIAS_VERB} {shlex.join((spelling, edit.display))}",
            rows=len(moved),
        )

    made = _edit(lambda: word_edit.folder(text, spelling))
    folder = None
    if isinstance(made, word_edit.Edit):
        folder = Option(
            answer=FOLDER,
            label=f"Its own genre folder, {spelling}",
            detail=(
                f"a top level folder named {spelling} with energy bands; once "
                f"{ROWS_VERB} has run, {RESORT_VERB} files the {len(on_row)} track(s) "
                f"whose row carries that spelling exactly, nothing rewritten"
                + (
                    f"; {len(members) - len(on_row)} stay under needs genre"
                    if len(members) > len(on_row)
                    else ""
                )
            ),
            command=f"{word_edit.FOLDER_VERB} {shlex.join((spelling,))}",
            rows=len(on_row),
        )
    if alias is None and folder is None:
        refused = made if isinstance(made, word_edit.Refused) else None
        why = refused.why if refused is not None else word_edit.ALREADY_FILED
        message = str(refused) if refused is not None else f"{spelling!r} has no answer"
        step = (refused.step if refused is not None else "") or "retag each file carrying the word by hand"
        return Word(**base, unanswerable=(why, message, step))
    leave = Option(
        answer=LEAVE,
        label="Leave it for hand tagging",
        detail=f"the {len(members)} track(s) stay under needs genre until tagged by hand",
        command="",
        rows=0,
    )
    offered = [option for option in (folder, alias) if option is not None]
    # AN ALIAS THAT MOVES NO ROW IS NEVER RECOMMENDED (round two): following it
    # retags the files, files nothing, and leaves the word one the folder verb
    # then refuses.
    if folder is not None and folder.rows >= genres_report.FOLDER_WORTH:
        first = folder
    elif alias is not None and alias.rows:
        first = alias
    else:
        first = leave
    rest = [option for option in (*offered, leave) if option is not first]
    return Word(**base, options=(first, *rest))


# ---------------------------------------------------------------------------
# The walk
# ---------------------------------------------------------------------------


def plan_backlog(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    *,
    text: str | None = None,
    catalogue: suggest.KeptCatalogue | None = None,
    progress: Callable[[str], None] | None = None,
    probe: Callable[[Path], adopt_scan.Readability] = adopt_scan.probe_readability,
) -> Backlog:
    """Sort every ``needs-genre`` row into one cause and read each verb's plan.

    THE POPULATION IS ADOPTION'S, its census over the same rows, so the count
    here is the count ``adopt scan`` reads as needs genre. A tombstone is not
    a row, and a row whose file is not here is counted in ``unread``.

    ``text`` is the active taxonomy copy the words' answers are planned on.

    NOTHING IS PENDING ON THE HANDLE WHEN THIS RETURNS, for the reason
    :func:`cratekit.tagging.rows.plan_rows` gives: each plan it reads leaves
    none either, and a genre entry is only looked up.
    """
    mapped = {str(row.ID): row for row in db.get_content()}
    live: dict[str, _Live] = {}
    for content_id, row in mapped.items():
        if trees.soft_delete_marker(row):
            continue
        live[content_id] = _Live(
            content_id=content_id,
            artist=str(getattr(row, "ArtistName", "") or "").strip(),
            folder=_folder_of(str(getattr(row, "FolderPath", "") or "")),
            genre=collection.genre_of(row).strip(),
            title=str(getattr(row, "Title", "") or "").strip(),
        )
    census = adopt_scan.scan_rows(
        collection.collection_rows(mapped.values()),
        declared,
        root=Path(cfg.library.root),
        prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
        probe=probe,
        energy_reader=rows._no_energy,
    )
    unread: Counter[str] = Counter()
    needing: list[tuple[adopt_scan.ScannedTrack, str, str]] = []
    for track in census:
        if track.content_id not in live:
            continue
        if track.readability is adopt_scan.Readability.NOT_A_PATH:
            # NO FILE AT ALL, a streaming row or another host's: no folder is
            # ever filled from it, so it is no file nobody read.
            continue
        if track.readability is not adopt_scan.Readability.READABLE or track.path is None:
            unread[rows._PROBED.get(track.readability, rows.FILE_UNREADABLE)] += 1
            continue
        if track.disposition is not adopt_scan.Disposition.NEEDS_GENRE:
            continue
        word, outcome = rows._file_word(Path(track.path))
        needing.append((track, word, outcome))
        if word and not track.genre.strip():
            # IT VOTES WITH ITS FILE'S WORD, as ``tag suggest`` votes it: the
            # row lags its file, and the file is the newer of the two (round one).
            live[track.content_id] = replace(live[track.content_id], genre=word)
    if progress is not None:
        progress(f"census: {len(needing)} of {len(live)} row(s) need a genre")

    rows_plan = rows.plan_rows(cfg, db, declared, probe=probe)
    by_rows = {item.content_id: item for item in rows_plan.items}
    suggested = suggest.plan_suggestions(
        cfg, db, declared, band=FLOOR, catalogue=catalogue, progress=progress, probe=probe
    )
    by_suggest = {item.content_id: item for item in suggested.items}
    needing_ids = {track.content_id for track, _word, _outcome in needing}
    # A ROW TAG ROWS WOULD MOVE INTO NEEDS GENRE: a row adoption files today
    # whose file carries a word it files nowhere (round one). The campaign's
    # first step is that verb, so the projection adds them back.
    joining = tuple(
        sorted(
            item.content_id
            for item in rows_plan.writes
            if item.content_id not in needing_ids
            and adopt_scan.classify_genre(declared, item.file)[0]
            is not adopt_scan.Disposition.ROUTE
        )
    )

    found: list[Row] = []
    for track, file_word, outcome in sorted(needing, key=lambda entry: entry[0].content_id):
        known = live[track.content_id]
        base = {
            "content_id": track.content_id,
            "path": str(track.path),
            "artist": known.artist,
            "title": known.title,
            "row_word": track.genre.strip(),
            "file_word": file_word,
        }
        if outcome == rows.FILE_UNREADABLE:
            found.append(
                Row(**base, cause=FILE_UNREAD, word="", status=LEFT, reason=rows.FILE_UNREADABLE)
            )
            continue
        cause, word = cause_of(declared, track.genre, file_word)
        if cause == ROW_LAGS_FILE:
            item = by_rows.get(track.content_id)
            if item is not None and item.action == rows.WRITE:
                found.append(Row(**base, cause=cause, word=word, status=SERVED, verb=ROWS_VERB))
            else:
                reason = item.reason if item is not None else "not-planned"
                found.append(
                    Row(**base, cause=cause, word=word, status=LEFT, verb=ROWS_VERB, reason=reason)
                )
        elif cause == NO_GENRE:
            offered = by_suggest.get(track.content_id)
            if offered is not None and offered.action == suggest.WRITE:
                found.append(
                    Row(
                        **base,
                        cause=cause,
                        word="",
                        status=PROPOSED,
                        verb=SUGGEST_VERB,
                        proposal=proposal_of(offered),
                        asked=offered.catalogue,
                    )
                )
            else:
                found.append(
                    Row(
                        **base,
                        cause=cause,
                        word="",
                        status=LEFT,
                        verb=SUGGEST_VERB,
                        reason=offered.reason if offered is not None else "not-planned",
                        asked=offered.catalogue if offered is not None else None,
                    )
                )
        elif cause == TOO_COARSE:
            found.append(
                Row(**base, cause=cause, word=word, status=LEFT, verb=RETAG_VERB, reason=TOO_COARSE)
            )
        else:
            found.append(Row(**base, cause=cause, word=word, status=ASKED))

    groups: dict[str, list[Row]] = {}
    for row in found:
        if row.cause == OFF_TAXONOMY:
            groups.setdefault(row.word.casefold(), []).append(row)
    rows_write = {item.content_id: item.file for item in rows_plan.writes}
    entries: dict[str, bool] = {}

    def has_entry(genre: str) -> bool:
        if genre not in entries:
            entries[genre] = metadata.resolve_genre_id(db, genre) is not None
        return entries[genre]

    words: list[Word] = []
    changes: dict[str, tuple[str, str, str]] = {}
    for folded, members in groups.items():
        # ASKED ONLY OF A FILE CARRYING THE WORD, since the second open is
        # paid per row and only a file an alias would retag can hold it twice.
        several = frozenset(
            row.content_id
            for row in members
            if row.file_word.casefold() == folded and rows._file_words(Path(row.path))
        )
        votes = neighbour_votes((row.content_id for row in members), live, declared)
        word = word_of(
            declared,
            text,
            members,
            votes,
            several=several,
            rows_write=rows_write,
            known=has_entry,
        )
        words.append(word)
        for row in members:
            if word.settled:
                changes[row.content_id] = (
                    (SETTLED, word.settled, "")
                    if row.content_id in word.reached
                    else (LEFT, "", NOT_REACHED)
                )
            elif word.unanswerable is not None:
                changes[row.content_id] = (LEFT, "", f"{UNANSWERABLE}:{word.unanswerable[0]}")
    words.sort(key=lambda word: (-word.rows, word.spelling.casefold(), word.spelling))
    return Backlog(
        rows=tuple(
            replace(
                row,
                status=changes[row.content_id][0],
                verb=changes[row.content_id][1],
                reason=changes[row.content_id][2],
            )
            if row.content_id in changes
            else row
            for row in found
        ),
        words=tuple(words),
        tracks=len(live),
        catalogue=catalogue is not None,
        unread=dict(sorted(unread.items())),
        joining=joining,
    )


__all__ = [
    "ALIAS",
    "ASKED",
    "CAUSES",
    "FILE_UNREAD",
    "FLOOR",
    "FOLDER",
    "LEAVE",
    "LEFT",
    "NEIGHBOURS",
    "NOT_REACHED",
    "NO_COPY",
    "NO_GENRE",
    "OFF_TAXONOMY",
    "PROPOSED",
    "ROW_LAGS_FILE",
    "SERVED",
    "SETTLED",
    "STATUSES",
    "TOO_COARSE",
    "WORKFLOW",
    "Backlog",
    "Option",
    "Proposal",
    "Row",
    "Word",
    "cause_of",
    "neighbour_votes",
    "plan_backlog",
    "proposal_of",
    "settle",
    "word_of",
]
