"""Give chosen rows a genre the taxonomy declares, over the one they carry (U339).

``tag suggest --set`` writes only a row with no genre on the row or the file,
``tag retag`` only a word too coarse to be a genre, and ``taxonomy alias``
refuses a word a folder already takes, so a person who decides a set of
tracks belongs in another genre folder had no verb. This is it.

THE ROWS ARE A PERSON'S LIST, by content identifier or by one playlist, and
EVERY ROW NAMED IS ONE ITEM, a row left listed with its reason: held out, gone
from the collection, its file not readable, its file holding several genres, or
already carrying the genre on the file and the row. Nothing is counted and not
shown, since the person named each row.

WHAT IT WRITES IS THE GENRE AND NOTHING ELSE: the file's genre tag through
:func:`cratekit.core.tags.write_genre`, and the row's ``GenreID`` through
:func:`cratekit.write.metadata.plan_genre_retag` under ``RETAG_GENRE``. A word
with no active lookup row is minted by :func:`cratekit.write.metadata.mint_genre`
on the same commit that links it, since rekordbox drops a lookup row nothing
references. THE FILE IS WRITTEN FIRST AND THE ROW ONLY WHEN ITS FILE READ BACK,
inside the session, after every file's old genre is in the record, so a restore
of the session puts the rows back from its capture and the files back from the
record (:mod:`cratekit.core.restore_tags`).

Layer: modules. It opens no database of its own and names no verb.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.adopt import collection, genre_moves
from cratekit.adopt import scan as adopt_scan
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    rb_writer,
    routing,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import rows, suggest
from cratekit.write import metadata, row_defaults, trees

_ORIGIN = ("tagging", "genre_set")

#: The name a session record carries for this write, and a digest is kinded by.
WORKFLOW = "tag-set"

#: What the row write is filed under in a session record's change summary,
#: the genre's own key, as ``tag rows`` files it.
CHANGE_KEY = rows.CHANGE_KEY

#: Where the record keeps each file's genre before the write, read by a restore;
#: ``cratekit.core.restore_tags.GENRE_RECORD_KEY`` is the same name, spelled
#: there and here since this layer does not reach that module.
RECORD_KEY = "genre_set_before"

#: What a plan shows for a genre the library has no active lookup row for.
MINTED = "mint"

#: The outcomes, in the order a summary lists them, zero filled.
WRITE = "write"
ALREADY = "already-that-genre"
HELD_OUT = rows.HELD_OUT
ROW_GONE = "row-gone"
FILE_MULTI_VALUED = rows.FILE_MULTI_VALUED

OUTCOMES: tuple[str, ...] = (
    WRITE, ALREADY, HELD_OUT, ROW_GONE, FILE_MULTI_VALUED, rows.FILE_UNREADABLE, *rows.UNREAD[1:],
)

#: The outcomes of a named row that is not written, each an item.
LEFT: tuple[str, ...] = OUTCOMES[1:]

#: What an item whose row is not written says it does.
LEAVE = rows.LEAVE

#: What the census's answers about a row's file count as, ``tag rows``' table.
_PROBED = rows._PROBED


@dataclass(frozen=True, slots=True)
class Item:
    """One named row: its words before, and what the plan does with it.

    ``file_writes`` and ``row_writes`` say which surface the write changes; a
    left row changes neither and carries its ``reason``.
    """

    content_id: str
    path: str
    title: str
    row: str
    file: str
    action: str
    reason: str = ""
    file_writes: bool = False
    row_writes: bool = False

    def digested(self) -> dict[str, Any]:
        """What the digest covers: the words, what is written, and why a row is
        not. NOT THE PATH, so a rehearsal on a copy digests equal."""
        return {
            "content_id": self.content_id,
            "row": self.row,
            "file": self.file,
            "action": self.action,
            "reason": self.reason,
            "file_writes": self.file_writes,
            "row_writes": self.row_writes,
        }

    def to_json(self) -> dict[str, Any]:
        """The item as the gate shows it, with its file and title."""
        return {**self.digested(), "path": self.path, "title": self.title}

    def before(self) -> dict[str, str]:
        """The file's genre as it stood, for the session record."""
        return {"content_id": self.content_id, "path": self.path, "genre": self.file}


@dataclass(frozen=True, slots=True)
class SetPlan(rows.Tallied):
    """Every named row, the count of every outcome, and the genre's lookup row."""

    genre: str
    #: The active lookup row the genre links, or empty when the apply mints one.
    genre_row: str
    #: The playlist the rows were named by, as given, or empty.
    playlist: str
    items: tuple[Item, ...]
    counts: Mapping[str, int]
    #: ``--leave`` identifiers naming no row in scope, shown and digested.
    leave_unmatched: tuple[str, ...] = ()

    @property
    def mints(self) -> bool:
        """Whether the apply makes the genre's lookup row."""
        return not self.genre_row

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to: the genre, its row or the
        mint, the scope's playlist and every item, and nothing that names a copy."""
        return digest_of(
            {
                "kind": WORKFLOW,
                "genre": self.genre,
                "genre_row": self.genre_row or MINTED,
                "playlist": self.playlist,
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
                "leave_unmatched": list(self.leave_unmatched),
            }
        )


def assert_declared(declared: taxonomy.Taxonomy, genre: str) -> str:
    """The genre as given, stripped, or a refusal before any row is read: it must
    be one the active taxonomy files by an exact declaration (U114's test)."""
    word = (genre or "").strip()
    if suggest.suggestable(declared, word):
        return word
    raise refuse(
        "review-selection-invalid",
        f"{word!r} is not a genre the active taxonomy declares as one adoption "
        f"files by, so this verb will not write it on any row",
        steps=(
            "name a genre exactly as the taxonomy declares it; `crate taxonomy "
            "show` lists them",
        ),
        origin=_ORIGIN,
        detail={"genre": word},
    )


# The scope.


#: How a playlist path is written: each node's name, top first, joined by this.
PATH_SEPARATOR = " / "


def _scope_refused(message: str, **detail: Any):
    return refuse(
        "tag-set-scope-unknown",
        message,
        steps=(
            "name the playlist by its path from the top of the rekordbox tree, "
            f"each folder's name joined by {PATH_SEPARATOR.strip()!r} with a space "
            "on each side, for example 'INBOX / Analyze'",
        ),
        origin=_ORIGIN,
        detail=detail,
    )


def playlist_members(db: Any, path: str) -> tuple[str, ...]:
    """The live rows one playlist holds, in its order and each once, the playlist
    found by its path through live nodes. A path that names nothing, names two
    nodes, or names a folder or a smart playlist refuses: none has members."""
    names = [part.strip() for part in path.split(PATH_SEPARATOR.strip())]
    if not path.strip() or not all(names):
        raise _scope_refused(f"{path!r} is not a playlist path", playlist=path)
    live = [node for node in db.get_playlist() if not rb_writer.node_removed(node)]
    children: dict[str, list[Any]] = {}
    for node in live:
        parent = str(getattr(node, "ParentID", "") or "")
        if parent in rb_writer.ROOT_PARENT_SENTINELS:
            parent = ""
        children.setdefault(parent, []).append(node)
    at = ""
    found: Any = None
    for depth, name in enumerate(names):
        matches = [node for node in children.get(at, ()) if str(node.Name or "") == name]
        where = PATH_SEPARATOR.join(names[: depth + 1])
        if not matches:
            raise _scope_refused(
                f"no playlist or folder is at {where!r}, so {path!r} names no rows",
                playlist=path,
            )
        if len(matches) > 1:
            raise _scope_refused(
                f"{len(matches)} nodes are named {where!r}, so {path!r} does not say "
                f"which rows it means",
                playlist=path,
            )
        found = matches[0]
        at = str(found.ID)
    attribute = int(getattr(found, "Attribute", 0) or 0)
    if attribute != 0:
        kind = "a folder" if attribute == 1 else "a smart playlist"
        raise _scope_refused(
            f"{path!r} is {kind}, which holds no rows of its own; name a plain "
            f"playlist",
            playlist=path,
        )
    songs = [
        song
        for song in db.get_playlist_songs(PlaylistID=str(found.ID))
        if not rb_writer.membership_removed(song)
    ]
    songs.sort(key=lambda song: int(getattr(song, "TrackNo", 0) or 0))
    return tuple(dict.fromkeys(str(song.ContentID) for song in songs))


def scoped(db: Any, named: Iterable[str], playlist: str = "") -> tuple[str, ...]:
    """Every content identifier the person named, each once, the ``--row`` and
    file identifiers first in the order given, then the playlist's."""
    found = [str(one).strip() for one in named if str(one).strip()]
    if playlist:
        found.extend(playlist_members(db, playlist))
    return tuple(dict.fromkeys(found))


# The plan.


def _row_title(row: Any) -> str:
    return str(getattr(row, "Title", "") or "").strip()


def plan_set(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    genre: str,
    content_ids: Sequence[str],
    *,
    playlist: str = "",
    leave: Iterable[str] = (),
    probe: Callable[[Path], adopt_scan.Readability] = adopt_scan.probe_readability,
) -> SetPlan:
    """Read every named row and its file once and give each one outcome.

    THE WALK IS ADOPTION'S CENSUS over the named rows alone, so a file's path is
    the one adoption would file it from. Items keep the order the rows were
    named in; only values are returned, so the handle may be a read one closed
    before the gate.
    """
    held_out = frozenset(str(content_id) for content_id in leave)
    counts = dict.fromkeys(OUTCOMES, 0)
    wanted = frozenset(content_ids)
    every = {str(row.ID): row for row in db.get_content()}
    mapped = {
        content_id: row
        for content_id, row in every.items()
        if content_id in wanted and not trees.soft_delete_marker(row)
    }
    census = {
        track.content_id: track for track in rows.scanned(cfg, mapped, declared, probe)
    }
    items: list[Item] = []
    for content_id in content_ids:
        row = mapped.get(content_id)
        track = census.get(content_id)
        if row is None or track is None:
            counts[ROW_GONE] += 1
            items.append(Item(content_id, "", "", "", "", LEAVE, reason=ROW_GONE))
            continue
        row_word = collection.genre_of(row).strip()
        title = _row_title(row)
        if track.readability is not adopt_scan.Readability.READABLE or track.path is None:
            reason = _PROBED.get(track.readability, rows.FILE_UNREADABLE)
            counts[reason] += 1
            items.append(
                Item(content_id, str(track.path or ""), title, row_word, "", LEAVE, reason=reason)
            )
            continue
        path = str(track.path)
        file_word, outcome = rows._file_word(Path(path))
        reason = ""
        if outcome == rows.FILE_UNREADABLE:
            reason = rows.FILE_UNREADABLE
        elif rows._file_words(Path(path)):
            # A FILE HOLDING SEVERAL GENRES IS LEFT: one written value would drop
            # the others, and a restore could put back only one.
            reason, file_word = FILE_MULTI_VALUED, "; ".join(rows._file_words(Path(path)))
        elif content_id in held_out:
            reason = HELD_OUT
        elif file_word == genre and row_word == genre:
            reason = ALREADY
        if reason:
            counts[reason] += 1
            items.append(Item(content_id, path, title, row_word, file_word, LEAVE, reason=reason))
            continue
        counts[WRITE] += 1
        items.append(
            Item(
                content_id, path, title, row_word, file_word, WRITE,
                file_writes=file_word != genre, row_writes=row_word != genre,
            )
        )
    genre_row = metadata.resolve_genre_id(db, genre)
    listed = {item.content_id for item in items}
    return SetPlan(
        genre=genre,
        genre_row="" if genre_row is None else str(genre_row),
        playlist=playlist,
        items=tuple(items),
        counts=MappingProxyType(counts),
        leave_unmatched=tuple(sorted(held_out - listed)),
    )


def assert_plan_unchanged(approved: SetPlan, again: SetPlan) -> None:
    """Refuse, writing nothing, when the plan taken again on the write handle is
    not the plan approved: a row, a file or the genre's lookup row moved between."""
    if again.digest == approved.digest:
        return
    shown = {item.content_id: item for item in approved.items}
    found = {item.content_id: item for item in again.items}
    moved = [
        content_id
        for content_id in sorted(set(shown) | set(found))
        if content_id not in shown
        or content_id not in found
        or shown[content_id].digested() != found[content_id].digested()
    ]
    if approved.genre_row != again.genre_row:
        moved.append(f"the lookup row for {approved.genre!r}")
    raise refuse(
        "decision-stale",
        f"{len(moved) or 'the totals of'} of the named row(s) are not as the "
        f"approved plan read them, so nothing was written: "
        + row_defaults.named(moved or ["the plan's totals"]),
        steps=("run the verb again and approve the plan as it is now",),
        origin=_ORIGIN,
        detail={"moved": moved},
    )


# The write.


#: Each written row's file, by content identifier: read back carrying the genre,
#: ``moved`` since the plan read it, ``failed`` to take the write, or ``wrong`` on
#: the read back. ``tag suggest``'s shape, the same four answers.
FilesWritten = suggest.FilesWritten


@dataclass(frozen=True, slots=True)
class Written(row_defaults.RowsWritten):
    """What one apply did, files and rows, and the lookup row it minted, if any."""

    files: FilesWritten = FilesWritten()
    minted: str = ""


def write_files(genre: str, items: Sequence[Item]) -> FilesWritten:
    """Write the genre onto each item's file where it differs, then read it back.
    EACH FILE IS READ AGAIN FIRST, and one no longer carrying the word the plan
    read is named and left. Nothing raises for one file."""
    read_back: list[str] = []
    moved: list[str] = []
    failed: list[str] = []
    wrong: list[str] = []
    for item in items:
        path = Path(item.path)
        word, outcome = rows._file_word(path)
        if word != item.file or outcome == rows.FILE_UNREADABLE:
            moved.append(item.content_id)
            continue
        if item.file_writes and not tags.write_genre(path, genre):
            failed.append(item.content_id)
            continue
        if rows._file_word(path)[0] != genre:
            wrong.append(item.content_id)
            continue
        read_back.append(item.content_id)
    return FilesWritten(tuple(read_back), tuple(moved), tuple(failed), tuple(wrong))


def judge(
    genre: str,
    items: Sequence[Item],
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
    names: Mapping[str, str],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong: (wrong, moved), a row not carrying the
    genre, and one with a column beside ``GenreID`` and the bookkeeping changed."""
    unread = [
        item.content_id
        for item in items
        if before.get(item.content_id) is None or after.get(item.content_id) is None
    ]
    wrong = [f"{content_id}: the row could not be read" for content_id in unread]
    moved: list[str] = []
    for item in items:
        if item.content_id in unread:
            continue
        row = after[item.content_id]
        word = names.get(str(row.get("GenreID") or ""), "")
        if word != genre:
            wrong.append(f"{item.content_id}: reads {word!r}, not {genre!r}")
        changed = row_defaults.moved_columns(before[item.content_id], row, planned=("GenreID",))
        if changed:
            moved.append(f"{item.content_id}: {', '.join(changed)}")
    return tuple(wrong), tuple(moved)


def named_bucket(declared: taxonomy.Taxonomy, genre: str) -> str:
    """The bucket a genre word files a row into, or empty for a blank word and
    one only the fallback tier places, as :func:`cratekit.adopt.move.genre_names`
    reads it."""
    if not genre.strip():
        return ""
    resolution = routing.resolve_bucket(declared, genre)
    return "" if resolution.match is routing.Match.FALLBACK else resolution.bucket_id


def moved_out_of(
    declared: taxonomy.Taxonomy, genre: str, items: Iterable[Item]
) -> dict[str, frozenset[str]]:
    """The bucket each row's old row genre filed it into, where that is another
    bucket than ``genre``'s: what :mod:`cratekit.adopt.genre_moves` records. THE
    ROW'S WORD, since adoption files by the row's genre and not the file's."""
    into = named_bucket(declared, genre)
    moved: dict[str, frozenset[str]] = {}
    for item in items:
        was = named_bucket(declared, item.row)
        if was and was != into:
            moved[item.content_id] = frozenset({was})
    return moved


def apply_set(
    cfg: config.Config,
    db: Any,
    plan: SetPlan,
    *,
    declared: taxonomy.Taxonomy,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Write the plan inside one guarded session: every file's old genre into the
    record, the files, then the rows whose file read back, the genre's lookup row
    minted on that same commit when the library has none, read back from SQL.
    Each row's old bucket is recorded for ``adopt move`` before the commit, after
    the capture, so a restore takes it back with the rows.

    THE CALLER TOOK THE PLAN AGAIN ON THIS HANDLE (:func:`assert_plan_unchanged`).
    """
    watched = row_defaults.watched_roots(analysis_roots)
    writes = plan.writes
    mapped = row_defaults.read_mapped(db, [item.content_id for item in writes])
    # THE EVIDENCE IS READ BEFORE IT IS REPLACED, as every content row write reads it.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    metadata.enable((metadata.RETAG_GENRE,))
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        # BEFORE THE CAPTURE IS ATTACHED, WHICH PERSISTS THE RECORD: every file's
        # old genre is on disk before the first file is written.
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes if item.file_writes]
        record, _capture = trees.attached_capture(gates, cfg, db)
        files = write_files(plan.genre, writes)
        landed = frozenset(files.read_back)
        rowed = [item for item in writes if item.content_id in landed and item.row_writes]
        ids = [item.content_id for item in rowed]
        before = row_defaults.read_columns(db, ids)
        done = {"written": 0, "minted": ""}
        try:
            if rowed:
                _write_rows(cfg, db, plan, declared, rowed, mapped, done)
        except BaseException:
            trees.rollback_quietly(db)
            # AN EXCEPTION IS NOT PROOF NOTHING LANDED: the witness is the
            # engine's own answer, and a landed commit is recorded before the raise.
            if witness.landed:
                row_defaults.record_commit(record, CHANGE_KEY, int(done["written"]), cfg)
            raise
        # RECORDED THE INSTANT THE COMMIT RETURNS.
        row_defaults.record_commit(record, CHANGE_KEY, int(done["written"]), cfg)
        written, minted = int(done["written"]), str(done["minted"])
        convergence.record_fingerprint(cfg, db)
        after = row_defaults.read_columns(db, ids)
        names = rows._genre_names(db)
        session_id = record.session_id
    # The process wide collection cache holds the words as they were.
    collection.reset_cache()
    wrong, moved = judge(plan.genre, rowed, before, after, names)
    return Written(
        session_id=session_id,
        written=written,
        read_back=len(rowed) - len(wrong),
        wrong=wrong,
        moved=moved,
        files=files,
        minted=minted,
    )


def _write_rows(
    cfg: config.Config,
    db: Any,
    plan: SetPlan,
    declared: taxonomy.Taxonomy,
    rowed: Sequence[Item],
    mapped: Mapping[str, Any],
    done: dict[str, Any],
) -> None:
    """Link each row to the genre's lookup row, minting it first when the library
    has none, record each row's old bucket, and commit. ``done`` holds the count
    and the mint as they happen, so a commit that raised after landing is
    recorded with what it wrote.

    MINTED ONLY WHEN A ROW LINKS IT, AND ON THE COMMIT THAT LINKS IT: rekordbox
    drops a lookup row nothing references (A4).
    """
    ids = [item.content_id for item in rowed]
    if plan.mints:
        done["minted"] = metadata.mint_genre(db, plan.genre)
    changes = metadata.plan_genre_retag(
        [mapped[content_id] for content_id in ids], dict.fromkeys(ids, plan.genre), db=db
    )
    _assert_all_linked(changes, ids, plan.genre)
    metadata.assert_within_policy(changes)
    done["written"] = len(metadata.write_plan(changes, mapped).written)
    # AFTER THE CAPTURE AND BEFORE THE COMMIT, so a restore takes it back.
    genre_moves.record(
        cfg, moved_out_of(declared, plan.genre, rowed), into=named_bucket(declared, plan.genre)
    )
    rb_writer.commit_guarded(db, creations=(rb_writer.GENRE_TABLE,) if done["minted"] else ())


def _assert_all_linked(changes: metadata.Plan, ids: Sequence[str], genre: str) -> None:
    """Refuse, before any row is set, when the resolution on the write handle
    links fewer rows than were planned: the genre's row was minted or found."""
    linked = {change.content_id for change in changes.changes}
    unlinked = [content_id for content_id in ids if content_id not in linked]
    if not unlinked:
        return
    raise refuse(
        "internal-error",
        f"the lookup row for {genre!r} could not be resolved for "
        f"{len(unlinked)} row(s) after it was found or made, so no row was written: "
        + row_defaults.named(unlinked),
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"unlinked": unlinked, "genre": genre},
    )


def assert_read_back(written: Written) -> None:
    """Refuse when the database does not say what the plan said it would, naming
    the session that undoes the durable write. A moved column outranks a genre
    not carried: the guard should have refused it before the commit."""
    undo = (f"the write is durable; restore session {written.session_id} to undo it",)
    if written.moved:
        raise refuse(
            "whitelist-violation",
            "a row given its genre has another column changed after the commit, "
            "which the guard should have refused before it: "
            + row_defaults.named(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    if written.wrong:
        raise refuse(
            "internal-error",
            f"{len(written.wrong)} of {written.written} row(s) written do not read "
            f"back with their new genre: " + row_defaults.named(written.wrong),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"wrong": list(written.wrong), "session": written.session_id},
        )


__all__ = [
    "ALREADY", "CHANGE_KEY", "FILE_MULTI_VALUED", "HELD_OUT", "LEAVE", "LEFT", "MINTED",
    "OUTCOMES", "PATH_SEPARATOR", "RECORD_KEY", "ROW_GONE", "WORKFLOW", "WRITE", "FilesWritten",
    "Item", "SetPlan", "Written", "apply_set", "assert_declared", "assert_plan_unchanged",
    "assert_read_back", "judge", "moved_out_of", "named_bucket", "plan_set", "playlist_members", "scoped", "write_files",
]
