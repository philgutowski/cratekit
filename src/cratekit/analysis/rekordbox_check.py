"""Read rekordbox's own result for the landed rows, and say whether the visit is done right (U167).

After the rekordbox visit, one question: is every landed row analysed, is each
grid the shape it should be, is the Key column filled, and how far does
rekordbox's key agree with the key the title's head carries. Sitting 47 had to
answer that with a throwaway script over the analysis files, which found every
one of 116 rows on a variable grid because the dialog was left on Dynamic. This
module is that script made a product, and it answers with a verdict a skill can
wait on: done, waiting, or suspect.

READ ONLY, IN BOTH PLACES IT LOOKS. The database is read through
``rb_writer.read_only_copy``, a disposable copy that refuses while rekordbox or
its agent runs, because a copy taken under the live application is torn. The
analysis files are read as bytes. A beat grid is READ here and never written:
the grid tag is parsed with pyrekordbox's own structure for it over bytes this
module read itself, and nothing here holds the serialiser the R17 name scan
forbids, so there is no object in hand that could save a file back.

WHAT ANALYSED MEANS is :func:`cratekit.intake.analyzed.member`'s, the one the
clear of INBOX / Analyze uses, so this check and the clear never disagree about
which rows rekordbox has finished with. The check calls its judgment,
:func:`cratekit.intake.analyzed.judge`, over rows it already holds.

THE COLLECTION IS READ IN A HANDFUL OF STATEMENTS (U259), never one or three
a row: the scope of every row rekordbox has not analysed is judged off the one
read of the collection, a scope of playlist members is read a chunk of IDs to
a statement, and each row in scope is read once, its judgment, key, title head
and analysis path all off that one read.

THE VERDICT, and why each part is there:

* **waiting** when any row in scope is not analysed. The visit is not over.
* **suspect** when every row is analysed and at least one of: a variable grid
  on a row not marked ``dyn`` (the mark U157 writes on a track whose tempo
  really moves); an analysed row whose grid could not be read, since a grid
  nobody read is not a grid anybody can vouch for; or the title keys agreeing
  with rekordbox's far less often than the recorded agreement says they should.
  SUSPECT OUTRANKS WAITING: a grid that came out wrong says the dialog's
  settings were wrong, and they are wrong for the rows still to come as well.
* **done** otherwise.

An empty scope has no verdict of the three. It says so rather than calling
nothing done.

Layer: modules. It opens the database copy itself, through the one reader every
diagnostic uses.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cratekit.analysis import agreement, detect
from cratekit.core import analysis_store, config, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.naming import NameTemplate, pad_camelot, parse_camelot, parse_head
from cratekit.intake import analyzed, native, refill

_ORIGIN = ("analysis.rekordbox_check",)

# ---------------------------------------------------------------------------
# The vocabulary
# ---------------------------------------------------------------------------

#: The three verdicts, and the answer for a scope that holds no row.
DONE = "done"
WAITING = "waiting"
SUSPECT = "suspect"
NOTHING = "nothing"

#: Where the rows came from, in the order they are asked for.
SCOPE_PASS = "pass"
SCOPE_SESSION = "session"
SCOPE_ANALYZE = "analyze"
SCOPE_UNANALYSED = "unanalysed"

#: What a row is, before its grid is read.
ANALYSED = "analysed"
NOT_ANALYSED = "not_analysed"
GONE = "gone"

#: What a row's grid reads as. Kept five ways apart, because "no grid tag in
#: the file", "no file" and "a file that would not parse" have three different
#: fixes and none of them is a constant grid.
CONSTANT = "constant"
VARIABLE = "variable"
ABSENT = "absent"
MISSING = "missing"
UNREADABLE = "unreadable"
#: The grid of a row that is not analysed, which nobody looked for.
NOT_READ = "not_read"

#: The title key against rekordbox's key.
KEY_EQUAL = "equal"
KEY_ONE_STEP = "one_step"
KEY_FAR = "far"
KEY_UNKEYED = "unkeyed"

#: The My Tag value U157 writes on a row whose tempo really moves, so that row
#: is analysed Dynamic and a variable grid on it is the right answer. The
#: landing's own constant, imported, so the two cannot disagree; read under any
#: category, since a person may file the value under one of their own.
DYN_VALUE = native.DYN_VALUE

#: How many standard errors below the recorded key agreement a sample's rate
#: must fall before it reads as suspect. Three, so a library whose keys agree
#: at the recorded rate is called suspect about once in seven hundred checks,
#: and a sample too small to say anything (a handful of rows) never is.
KEY_AGREEMENT_SIGMAS = 3.0

#: The ANLZ header and every tag header: four ASCII bytes, then two big endian
#: lengths, the header's and the whole tag's (or the whole file's).
_HEADER = struct.Struct(">4sII")
_FILE_KIND = b"PMAI"
_GRID_KIND = b"PQTZ"


# ---------------------------------------------------------------------------
# The grid, read from the bytes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Grid:
    """One row's beat grid as rekordbox wrote it, or why it could not be read."""

    state: str
    #: How many beats the grid carries, zero when it was not read.
    beats: int = 0
    #: The lowest and highest tempo the grid's beats carry, in hundredths, as
    #: the file stores them. Equal on a constant grid.
    low: int = 0
    high: int = 0
    #: Why a grid is missing or unreadable, empty otherwise.
    why: str = ""

    @property
    def span(self) -> float:
        """How far the tempo moves inside the track, in beats per minute."""
        return (self.high - self.low) / 100.0

    def as_dict(self) -> dict[str, Any]:
        read = self.state in (CONSTANT, VARIABLE)
        return {
            "grid": self.state,
            "beats": self.beats,
            "tempo_low": self.low / 100.0 if read else None,
            "tempo_high": self.high / 100.0 if read else None,
            "tempo_span": self.span if read else None,
            **({"why": self.why} if self.why else {}),
        }


def grid_ticks(data: bytes) -> list[Any] | None:
    """The beat grid tag's entries from one analysis file's bytes, or None when it has none.

    Walks the tags by their own headers and parses only the grid tag, with
    pyrekordbox's structure for it. Raises ``ValueError`` for bytes that are not
    an analysis file, a file whose stated length is not its size (a file cut off
    mid write), or a tag that runs past the end, so a damaged file is never
    read as a file with no grid.
    """
    from construct import ConstructError
    from pyrekordbox.anlz import structs

    if len(data) < _HEADER.size:
        raise ValueError(f"{len(data)} bytes is shorter than an analysis file's header")
    kind, header_length, file_length = _HEADER.unpack_from(data, 0)
    if kind != _FILE_KIND:
        raise ValueError(f"the file begins {kind!r}, not {_FILE_KIND!r}")
    if file_length != len(data):
        raise ValueError(
            f"the header says {file_length} bytes and the file holds {len(data)}"
        )
    offset = header_length
    while offset < len(data):
        if offset + _HEADER.size > len(data):
            raise ValueError(f"a tag header at byte {offset} runs past the end of the file")
        tag, _tag_header, tag_length = _HEADER.unpack_from(data, offset)
        if tag_length < _HEADER.size or offset + tag_length > len(data):
            raise ValueError(
                f"the {tag!r} tag at byte {offset} says {tag_length} bytes and does not fit"
            )
        if tag == _GRID_KIND:
            try:
                parsed = structs.PQTZ.parse(data[offset + _HEADER.size : offset + tag_length])
            except ConstructError as exc:
                raise ValueError(f"the grid tag would not parse: {exc}") from exc
            return list(parsed.entries)
        offset += tag_length
    return None


def read_grid(path: Path | None) -> Grid:
    """Read one row's grid from its analysis file. Every failure is named, never folded."""
    if path is None:
        return Grid(state=MISSING, why="the row names no analysis file")
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return Grid(state=MISSING, why=f"no analysis file at {path}")
    except OSError as exc:
        return Grid(state=UNREADABLE, why=f"{path} could not be read: {exc}")
    try:
        ticks = grid_ticks(data)
    except ValueError as exc:
        return Grid(state=UNREADABLE, why=f"{path}: {exc}")
    if not ticks:
        return Grid(state=ABSENT, why=f"{path} holds no beat grid")
    tempos = [int(tick.tempo) for tick in ticks]
    low, high = min(tempos), max(tempos)
    return Grid(
        state=CONSTANT if low == high else VARIABLE, beats=len(ticks), low=low, high=high
    )


# ---------------------------------------------------------------------------
# The key
# ---------------------------------------------------------------------------


def key_relation(head: str | None, reference: str | None) -> str:
    """The title key against rekordbox's, on the Camelot wheel.

    One step is a neighbour: the number one either side with the same letter,
    or the same number with the other letter (the relative major or minor).
    Either side missing is unkeyed, which is not a disagreement.
    """
    one = parse_camelot(head) if head else None
    other = parse_camelot(reference) if reference else None
    if one is None or other is None:
        return KEY_UNKEYED
    if one == other:
        return KEY_EQUAL
    (number, letter), (other_number, other_letter) = one, other
    if letter == other_letter and (number - other_number) % 12 in (1, 11):
        return KEY_ONE_STEP
    if number == other_number:
        return KEY_ONE_STEP
    return KEY_FAR


def head_key(row: Any, *, template: NameTemplate) -> str | None:
    """The key the row's title head carries, the filename's when the title has no head."""
    for name in (getattr(row, "Title", None), getattr(row, "FileNameL", None)):
        parsed = parse_head(str(name or ""), template=template)
        if parsed and parsed.get("key"):
            return str(parsed["key"])
    return None


def key_floor(compared: int) -> float | None:
    """The lowest equal rate a sample of ``compared`` keys may show and not read as suspect.

    The recorded agreement (``detect.head_agreement``) less
    :data:`KEY_AGREEMENT_SIGMAS` standard errors of a sample this size. None for
    no sample, which is never suspect.
    """
    if compared <= 0:
        return None
    measured = detect.head_agreement()["key"]
    total = measured["equal"] + measured["differs"]
    rate = measured["equal"] / total
    return rate - KEY_AGREEMENT_SIGMAS * math.sqrt(rate * (1.0 - rate) / compared)


# ---------------------------------------------------------------------------
# The scope
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Scope:
    """Which rows the check reads, and where they came from."""

    kind: str
    #: What the scope names: a pass, a session, the playlist, or the collection.
    name: str
    content_ids: tuple[str, ...]
    #: Each step that was looked at and passed over on the way, with why.
    passed_over: tuple[str, ...] = ()
    #: The session records the log could not read, which a named landing might be among.
    #: An unlisted log never reaches a Scope: it reads no record, so a named
    #: landing refuses, naming the listing (R-1255).
    unreadable_records: int = 0
    #: The collection rows the scope already read, by content ID, so the rows
    #: are not read a second time (U259). The unanalysed scope holds every row
    #: it names; a scope of playlist members holds none and its rows are read
    #: in :func:`check_rows`. Not part of what a scope IS, so it is left out of
    #: equality and of its repr.
    read: Mapping[str, Any] = field(default_factory=dict, compare=False, repr=False)


def _recorded_playlists(record: session.SessionRecord) -> tuple[str, ...]:
    """Every batch and account playlist one landing record names by id."""
    ids: list[str] = []
    batch = record.detail.get(native.BATCH_PLAYLIST_KEY)
    if isinstance(batch, dict) and batch.get("id"):
        ids.append(str(batch["id"]))
    for entry in record.detail.get(native.INBOX_PLAYLISTS_KEY) or ():
        if isinstance(entry, dict) and entry.get("id"):
            ids.append(str(entry["id"]))
    return tuple(ids)


def _landed(
    cfg: config.Config, *, pass_name: str | None, session_id: str | None
) -> tuple[tuple[session.SessionRecord, ...], int, bool]:
    """The closed native landings a pass or a session names, the unread count, and whether
    the log could not be listed at all (R-1255).

    A pass is :func:`cratekit.intake.native.landings_of_pass`'s proof, so a
    landing refused after its moves, which names no pass, is never read as one.
    A session is the same proof for one landing named by its id.
    """
    records, unreadable = session.scan_log(cfg)
    if session.log_unlisted(unreadable, cfg):
        # NO LANDING CAN BE READ, so the caller refuses naming the listing
        # rather than the pass lookup refusing in words of its own.
        return (), len(unreadable), True
    if pass_name is not None:
        wanted = set(native.landings_of_pass(cfg, pass_name))
    else:
        wanted = {
            record.session_id
            for record in records
            if record.session_id == session_id
            and record.workflow == native.WORKFLOW
            and record.state is session.SessionState.CLOSED
            and str(session.SourceState.COMMITTED) in record.sources.values()
        }
    return (
        tuple(record for record in records if record.session_id in wanted),
        len(unreadable),
        False,
    )


def _live_members(db: Any, playlist_ids: Iterable[str]) -> tuple[str, ...]:
    """Every live member of the playlists, first appearance kept; a playlist gone holds none."""
    seen: dict[str, None] = {}
    for playlist_id in playlist_ids:
        for content_id in analyzed.live_members(db, playlist_id):
            seen.setdefault(content_id, None)
    return tuple(seen)


def _analyze_members(
    db: Any, declared: taxonomy.Taxonomy, registry: tree_registry.Registry
) -> tuple[tuple[str, ...], str]:
    """INBOX / Analyze's live members, or none with why it was passed over."""
    try:
        root_id = refill.anchored_root(db, declared.intake.id, registry)
    except CratekitError as exc:
        return (), f"INBOX / {native.ANALYZE} was not read: {exc.cause.message}"
    playlist = native.analyze_playlist(db, str(root_id))
    if playlist is None:
        return (), f"the intake folder holds no {native.ANALYZE} playlist"
    members = analyzed.live_members(db, str(playlist.ID))
    if not members:
        return (), f"INBOX / {native.ANALYZE} holds no row"
    return tuple(dict.fromkeys(members)), ""


def _unanalysed(db: Any) -> dict[str, Any]:
    """Every live collection row rekordbox has not analysed, by the clear's own reading,
    each with the row the one read of the collection holds, in the collection's order.

    ONE STATEMENT, NOT ONE A ROW (U259). Each row is judged by
    :func:`cratekit.intake.analyzed.judge` as the read hands it over, which is
    the judgment the clear reads by ID, so no row is asked for again; the check
    reads a private copy, so nothing changes a row between the read and the
    judgment.

    A ROW WHOSE ID IS NOT TEXT IS LEFT OUT, as the read by ID always left it
    (review round one): an ID stored as bytes is never found by the text of
    its ID, so it was never in this scope, and judging it in hand would add
    it. Whether it belongs in the scope is a question of its own, not one
    this saving answers.
    """
    waiting: dict[str, Any] = {}
    for content in db.get_content():
        if not isinstance(content.ID, str):
            continue
        content_id = content.ID
        one = analyzed.judge(content_id, content)
        if one.why == analyzed.NOT_ANALYSED or one.why == analyzed.NO_ANALYSIS_PATH:
            waiting[one.content_id] = content
    return waiting


#: How many IDs one statement asks for, under every SQLite build's variable limit.
_CHUNK = 500


def _content_rows(db: Any, content_ids: Sequence[str]) -> dict[str, Any]:
    """The collection rows named, by content ID, read a chunk of IDs to a statement (U259).

    A row the collection lacks is absent from the answer, which the caller
    reads as ``None``: what a read by ID answers for it.
    """
    from pyrekordbox.db6 import tables

    found: dict[str, Any] = {}
    for start in range(0, len(content_ids), _CHUNK):
        chunk = list(content_ids[start : start + _CHUNK])
        query = db.query(tables.DjmdContent).filter(tables.DjmdContent.ID.in_(chunk))
        for row in query.all():
            found[str(row.ID)] = row
    return found


def resolve_scope(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    pass_name: str | None = None,
    session_id: str | None = None,
) -> Scope:
    """The rows to read: a named landing, else INBOX / Analyze, else every unanalysed row.

    A NAME THE PERSON GAVE WINS, so a pass or a session given on the command
    line is read even when the playlist holds rows. A NAME NOTHING RECORDED
    REFUSES, rather than reading as an empty scope and an answer of nothing to
    check, which a mistyped pass would otherwise get.
    """
    if pass_name is not None or session_id is not None:
        kind = SCOPE_PASS if pass_name is not None else SCOPE_SESSION
        name = str(pass_name if pass_name is not None else session_id)
        records, unreadable, unlisted = _landed(
            cfg, pass_name=pass_name, session_id=session_id
        )
        if not records:
            unread = (
                "; the session log could not be listed and it may be in it"
                if unlisted
                else f"; {unreadable} session record(s) could not be read and it may be "
                "among them"
                if unreadable
                else ""
            )
            raise refuse(
                "analysis-check-landing-unknown",
                f"no closed landing is recorded for the {kind} {name!r}, so there are no "
                f"landed rows to check{unread}",
                origin=_ORIGIN,
                detail={
                    "kind": kind,
                    "name": name,
                    "unreadable_records": unreadable,
                    "log_unlisted": unlisted,
                },
            )
        playlists = [one for record in records for one in _recorded_playlists(record)]
        members = _live_members(db, playlists)
        # A LANDING WHOSE PLAYLISTS HOLD NO LIVE ROW REFUSES TOO (review round
        # one): its rows were landed, so a scope that finds none of them is a
        # playlist removed or emptied since, and answering "nothing to check"
        # would exit 0, done's status, over rows nobody read.
        if not members:
            raise refuse(
                "analysis-check-landing-unknown",
                f"the {kind} {name!r} is recorded as landed, and the playlists it filed "
                f"into ({', '.join(playlists) or 'none recorded'}) hold no live row now, "
                f"so its landed rows cannot be found to check",
                origin=_ORIGIN,
                detail={"kind": kind, "name": name, "playlists": playlists},
            )
        return Scope(
            kind=kind,
            name=name,
            content_ids=members,
            unreadable_records=unreadable,
        )
    members, why = _analyze_members(db, declared, registry)
    if members:
        return Scope(kind=SCOPE_ANALYZE, name=f"INBOX / {native.ANALYZE}", content_ids=members)
    waiting = dict(_unanalysed(db))
    return Scope(
        kind=SCOPE_UNANALYSED,
        name="every row rekordbox has not analysed",
        content_ids=tuple(waiting),
        passed_over=(why,),
        read=waiting,
    )


# ---------------------------------------------------------------------------
# The rows and the verdict
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Row:
    """One row in scope, as the check read it."""

    content_id: str
    title: str
    state: str
    #: Why a row is not analysed or gone, in the clear's words.
    why: str = ""
    grid: Grid = field(default_factory=lambda: Grid(state=NOT_READ))
    #: rekordbox's key as a padded Camelot code, None when the Key column is empty.
    key: str | None = None
    head_key: str | None = None
    relation: str = KEY_UNKEYED
    dyn: bool = False

    @property
    def suspect_grid(self) -> bool:
        """A variable grid on a row not marked dyn, or an analysed row's grid nobody could read."""
        if self.state != ANALYSED:
            return False
        if self.grid.state == VARIABLE:
            return not self.dyn
        return self.grid.state in (ABSENT, MISSING, UNREADABLE)

    def as_dict(self) -> dict[str, Any]:
        return {
            "content_id": self.content_id,
            "title": self.title,
            "state": self.state,
            **({"why": self.why} if self.why else {}),
            **self.grid.as_dict(),
            "key": self.key,
            "head_key": self.head_key,
            "key_agreement": self.relation,
            "dyn": self.dyn,
            "suspect": self.suspect_grid,
        }


#: The one reader of the mark, the landing's own, so the check reads as marked
#: exactly what the landing reports it wrote (U157).
dyn_marked = native.dyn_marked

#: What :func:`read_row` is handed when its caller holds no row, told apart
#: from ``None``, which is a row the collection lacks.
_UNREAD: Any = object()


def read_row(
    cfg: config.Config,
    db: Any,
    content_id: str,
    *,
    keys: dict[str, str | None],
    dyn: frozenset[str],
    template: NameTemplate,
    content: Any = _UNREAD,
) -> Row:
    """Read one row: analysed or not, then its grid, its key and its mark.

    ONE READ OF THE ROW (U259): the clear's judgment, the key, the title head
    and the analysis path all come off ``content``, the row the caller already
    holds (``None`` for a row the collection lacks), and only a call that
    hands none reads it, once, by ID.
    """
    if content is _UNREAD:
        content = db.get_content(ID=content_id)
    one = analyzed.judge(content_id, content)
    if one.why in (analyzed.NO_ROW, analyzed.ROW_REMOVED):
        return Row(content_id=content_id, title=one.title, state=GONE, why=one.why)
    key_id = getattr(content, "KeyID", None)
    key = agreement.camelot_from_scale_name(keys.get(str(key_id))) if key_id else None
    head = head_key(content, template=template)
    common = {
        "content_id": content_id,
        "title": one.title,
        "key": key,
        "head_key": None if head is None else pad_camelot(head),
        "relation": key_relation(head, key),
        "dyn": content_id in dyn,
    }
    if one.action != analyzed.CLEAR:
        return Row(state=NOT_ANALYSED, why=one.why, **common)
    stored = str(getattr(content, "AnalysisDataPath", "") or "")
    try:
        path = analysis_store.analysis_file(cfg, stored)
    except ValueError as exc:
        return Row(state=ANALYSED, grid=Grid(state=UNREADABLE, why=str(exc)), **common)
    return Row(state=ANALYSED, grid=read_grid(path), **common)


@dataclass(frozen=True, slots=True)
class Check:
    """The rows read, the counts, and the verdict."""

    scope: Scope
    rows: tuple[Row, ...]

    def counted(self, state: str) -> int:
        return sum(1 for row in self.rows if row.state == state)

    @property
    def analysed(self) -> tuple[Row, ...]:
        return tuple(row for row in self.rows if row.state == ANALYSED)

    @property
    def key_counts(self) -> dict[str, int]:
        counts = {KEY_EQUAL: 0, KEY_ONE_STEP: 0, KEY_FAR: 0, KEY_UNKEYED: 0}
        for row in self.analysed:
            counts[row.relation] += 1
        return counts

    @property
    def key_compared(self) -> int:
        counts = self.key_counts
        return counts[KEY_EQUAL] + counts[KEY_ONE_STEP] + counts[KEY_FAR]

    @property
    def key_suspect(self) -> bool:
        """Title keys agreeing with rekordbox's far below the recorded rate."""
        floor = key_floor(self.key_compared)
        if floor is None:
            return False
        return self.key_counts[KEY_EQUAL] / self.key_compared < floor

    @property
    def verdict(self) -> str:
        if not self.rows or self.counted(GONE) == len(self.rows):
            return NOTHING
        if any(row.suspect_grid for row in self.rows) or self.key_suspect:
            return SUSPECT
        if self.counted(NOT_ANALYSED):
            return WAITING
        return DONE

    def summary(self) -> dict[str, Any]:
        grids: dict[str, int] = {}
        for row in self.analysed:
            grids[row.grid.state] = grids.get(row.grid.state, 0) + 1
        floor = key_floor(self.key_compared)
        return {
            "verdict": self.verdict,
            "scope": self.scope.kind,
            "scope_name": self.scope.name,
            "rows": len(self.rows),
            "analysed": self.counted(ANALYSED),
            "not_analysed": self.counted(NOT_ANALYSED),
            "gone": self.counted(GONE),
            "grids": {state: grids.get(state, 0) for state in (CONSTANT, VARIABLE, ABSENT, MISSING, UNREADABLE)},
            "variable_not_dyn": sum(
                1 for row in self.analysed if row.grid.state == VARIABLE and not row.dyn
            ),
            "widest_span": max(
                (row.grid.span for row in self.analysed if row.grid.state == VARIABLE),
                default=0.0,
            ),
            "key_filled": sum(1 for row in self.analysed if row.key is not None),
            "key_agreement": self.key_counts,
            "key_equal_floor": None if floor is None else round(floor, 4),
            "key_suspect": self.key_suspect,
        }


def check_rows(
    cfg: config.Config, db: Any, scope: Scope, *, template: NameTemplate
) -> Check:
    """Read every row the scope names, once, off the handle given.

    IN A HANDFUL OF STATEMENTS, NOT ONE A ROW (U259): the rows the scope
    already read are used as read, the rest are read a chunk of IDs to a
    statement, and each row is then judged in the scope's order, so the first
    row that cannot say whether it was removed refuses as it did when each
    row was read by itself.

    A BATCH THE BINDING CANNOT LOAD IS READ A ROW AT A TIME (review round
    one). A batch loads every row before any is judged, so a later row the
    binding cannot load, a date it cannot parse, would fail the read ahead of
    an earlier row's refusal. The rows are then read one by one by ID, as
    they were before U259, and the first failure in the scope's order is the
    answer: the same refusal, or the same error, nothing swallowed.
    """
    keys = {str(key.ID): key.ScaleName for key in db.get_key()}
    dyn = dyn_marked(db)
    held: dict[str, Any] | None = dict(scope.read)
    try:
        held.update(
            _content_rows(
                db, [content_id for content_id in scope.content_ids if content_id not in held]
            )
        )
    except Exception:  # noqa: BLE001 - every failure is met again, in order, below
        held = None
    rows = tuple(
        read_row(
            cfg,
            db,
            content_id,
            keys=keys,
            dyn=dyn,
            template=template,
            content=_UNREAD if held is None else held.get(content_id),
        )
        for content_id in scope.content_ids
    )
    # THE ROWS THE SCOPE CARRIED STAY WITH THE HANDLE: they belong to the
    # copy's session, which closes when the check returns, so the answer
    # holds the scope without them.
    return Check(scope=replace(scope, read={}), rows=rows)


def check(
    cfg: config.Config,
    *,
    declared: taxonomy.Taxonomy,
    template: NameTemplate,
    pass_name: str | None = None,
    session_id: str | None = None,
    database: Path | None = None,
) -> Check:
    """Copy the database, resolve the scope on the copy, read every row in it."""
    source = database if database is not None else cfg.library.db_path
    registry = tree_registry.read(cfg)
    with rb_writer.read_only_copy(source, cfg=cfg) as db:
        scope = resolve_scope(
            cfg, db, declared=declared, registry=registry, pass_name=pass_name, session_id=session_id
        )
        found = check_rows(cfg, db, scope, template=template)
    # A NAMED LANDING WHOSE EVERY ROW HAS LEFT THE COLLECTION REFUSES TOO (review
    # round two), for the reason a landing whose playlists hold no live row
    # does: its rows were landed, none of them could be read, and nothing,
    # exit 0, would read as done over a landing nobody checked.
    if found.verdict == NOTHING and scope.kind in (SCOPE_PASS, SCOPE_SESSION):
        raise refuse(
            "analysis-check-landing-unknown",
            f"the {scope.kind} {scope.name!r} is recorded as landed, and every one of its "
            f"{len(found.rows)} row(s) has left the collection, so there is nothing of it "
            f"left to check",
            origin=_ORIGIN,
            detail={"kind": scope.kind, "name": scope.name, "gone": len(found.rows)},
        )
    return found


__all__: Sequence[str] = (
    "ABSENT",
    "ANALYSED",
    "CONSTANT",
    "DONE",
    "DYN_VALUE",
    "GONE",
    "KEY_AGREEMENT_SIGMAS",
    "KEY_EQUAL",
    "KEY_FAR",
    "KEY_ONE_STEP",
    "KEY_UNKEYED",
    "MISSING",
    "NOTHING",
    "NOT_ANALYSED",
    "NOT_READ",
    "SCOPE_ANALYZE",
    "SCOPE_PASS",
    "SCOPE_SESSION",
    "SCOPE_UNANALYSED",
    "SUSPECT",
    "UNREADABLE",
    "VARIABLE",
    "WAITING",
    "Check",
    "Grid",
    "Row",
    "Scope",
    "check",
    "check_rows",
    "dyn_marked",
    "grid_ticks",
    "head_key",
    "key_floor",
    "key_relation",
    "read_grid",
    "read_row",
    "resolve_scope",
)
