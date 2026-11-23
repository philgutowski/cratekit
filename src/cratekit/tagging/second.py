"""Set or clear a track's second genre on its file (U340).

A second genre files a track into a second genre folder of the routing tree
beside the one its genre names, each in its own energy band, by
:func:`cratekit.core.routing.second_bucket`. It is a file tag of its own,
``SecondGenre``, read by every path that files a track, so this module writes
the file and nothing else: no row, no genre, no key, no tempo, no grid.

THE ROWS ARE CHOSEN, never found: by content identifier or by a playlist of
the library's tree, each read through adoption's census, which resolves a row
to its file the way adoption does. EVERY CHOSEN ROW LANDS IN ONE OUTCOME, a
write or a reason it is left, so a row the plan does not write is never
silently missing from it. A file is written only while it still carries what
the plan read, and read back.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable

from cratekit.adopt import scan as adopt_scan
from cratekit.cli.output import digest_of
from cratekit.core import config, rb_writer, routing, tags, taxonomy
from cratekit.core.cause import refuse
from cratekit.tagging import remap, rows

#: The name a plan digests under.
WORKFLOW = "tag-second"

#: The field this verb writes, and the only one.
FIELD = "secondgenre"

#: What happens to one chosen row.
WRITE = "write"
LEAVE = "leave"

#: Why a chosen row is left. Each is counted, and each left row is listed.
ALREADY = "already-that-second-genre"
NONE_TO_CLEAR = "no-second-genre"
#: The second genre would name the folder the file's genre already names.
SAME_FOLDER = "genre-names-that-folder"
#: The file's genre names no folder, so a second genre would file nothing.
GENRE_FILES_NOWHERE = "genre-names-no-folder"
HELD_OUT = "held-out"
ROW_GONE = "row-not-in-collection"
FILE_MISSING = "file-missing"
FILE_UNREADABLE = "file-unreadable"

#: Every outcome, in the order a report lists them.
OUTCOMES: tuple[str, ...] = (
    WRITE, ALREADY, NONE_TO_CLEAR, SAME_FOLDER, GENRE_FILES_NOWHERE, HELD_OUT, ROW_GONE,
    FILE_MISSING, FILE_UNREADABLE,
)
LEFT: tuple[str, ...] = OUTCOMES[1:]

#: The census's readability, as this verb names a row it could not open.
_PROBED = {
    adopt_scan.Readability.MISSING: FILE_MISSING,
    adopt_scan.Readability.ONLINE_ONLY: FILE_MISSING,
    adopt_scan.Readability.UNMAPPED: FILE_MISSING,
    adopt_scan.Readability.NOT_A_PATH: FILE_MISSING,
}

#: How a playlist's path is spelled on the command line, folder by folder.
PATH_SEPARATOR = " / "

_ORIGIN = ("tagging", "second")


@dataclass(frozen=True, slots=True)
class Item:
    """One chosen row: its file, its genre, its second genre now and wanted.

    ``current`` is the second genre the file carries, empty for none or not
    read; ``wanted`` is the one to write, empty to clear. ``current`` is the
    undo of a write.
    """

    content_id: str
    path: str
    genre: str
    current: str
    wanted: str
    action: str
    reason: str = ""

    def to_json(self) -> dict[str, str]:
        return {
            "content_id": self.content_id,
            "path": self.path,
            "genre": self.genre,
            "second_genre_was": self.current,
            "second_genre": self.wanted,
            "action": self.action,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class SecondPlan:
    """Every chosen row in one outcome, and the genre being set, empty to clear."""

    genre: str
    items: tuple[Item, ...]
    counts: Mapping[str, int]

    @property
    def writes(self) -> tuple[Item, ...]:
        return tuple(item for item in self.items if item.action == WRITE)

    @property
    def rows(self) -> int:
        return len(self.items)

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to: every row, both values, every outcome."""
        return digest_of(
            {
                "kind": WORKFLOW,
                "genre": self.genre,
                "items": [item.to_json() for item in self.items],
                "counts": dict(self.counts),
            }
        )


#: What an apply did. ``tag remap``'s own record of a file write, since the two
#: verbs write and read back a file the same way; ``rewritten`` holds this
#: module's items and ``unrecorded`` is always empty, since nothing is recorded.
Written = remap.Written


def assert_genre_files(declared: taxonomy.Taxonomy, genre: str) -> None:
    """Refuse a second genre that names no folder, before anything is read.

    A blank word, one the taxonomy calls too coarse to be a genre, and one
    that resolves only through the fallback tier would file a track nowhere,
    by the same rule every filing path asks.
    """
    if routing.files_by_genre(declared, genre) is not None:
        return
    raise refuse(
        "tag-second-genre-undeclared",
        f"{genre!r} names no genre folder of the active taxonomy: it is blank, too "
        f"coarse to be a genre, or resolves only through the fallback, so a track "
        f"given it as a second genre would be filed nowhere beside its own",
        steps=(
            "give a genre the taxonomy files into a folder of its own, such as one of "
            "the folder names `crate report genres` lists",
        ),
        origin=_ORIGIN,
        detail={"genre": genre},
    )


def playlist_members(db: Any, path: str) -> tuple[str, ...]:
    """The tracks one playlist of the library's tree holds, by its path.

    ``path`` names each folder from the top, joined by :data:`PATH_SEPARATOR`.
    MATCHED WHOLE against every live playlist's own path, never split, since a
    genre folder's name may hold the separator itself (``Minimal / Deep Tech``).
    Only live nodes and live memberships count. A path that names no playlist,
    a folder, or more than one playlist REFUSES rather than choosing, since a
    choice would write to rows nobody named.
    """
    wanted = PATH_SEPARATOR.join(part.strip() for part in path.split(PATH_SEPARATOR))
    nodes = {str(node.ID): node for node in db.get_playlist() if not rb_writer.node_removed(node)}

    def full(node: Any, seen: frozenset[str] = frozenset()) -> str | None:
        parent = str(getattr(node, "ParentID", ""))
        name = str(getattr(node, "Name", "") or "")
        if parent in rb_writer.ROOT_PARENT_SENTINELS:
            return name
        above = nodes.get(parent)
        if above is None or parent in seen:
            return None
        head = full(above, seen | {parent})
        return None if head is None else f"{head}{PATH_SEPARATOR}{name}"

    found = [node for node in nodes.values() if full(node) == wanted]
    if not found:
        raise _no_playlist(path, "nothing in the tree is at that path")
    if len(found) > 1:
        raise _no_playlist(path, f"{len(found)} nodes answer to it")
    if rb_writer.is_folder(found[0]):
        raise _no_playlist(path, "it names a folder")
    return tuple(
        sorted(
            {
                str(song.ContentID)
                for song in db.get_playlist_songs(PlaylistID=str(found[0].ID))
                if not rb_writer.membership_removed(song)
            }
        )
    )


def _no_playlist(path: str, why: str):
    return refuse(
        "tag-second-playlist-unknown",
        f"--playlist {path!r} names no one playlist of the library's tree: {why}",
        steps=(
            "name the playlist by every folder above it, top first, joined by ' / ', "
            "as rekordbox's tree shows it",
        ),
        origin=_ORIGIN,
        detail={"playlist": path},
    )


def _read(path: Path) -> tuple[str, str] | None:
    """The file's genre and second genre, or None when its tags cannot be read."""
    try:
        values = tags.read_tags_checked(path, ("genre", FIELD))
    except tags.TagReadFailed:
        return None
    return (values["genre"] or "").strip(), (values[FIELD] or "").strip()


def plan(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    *,
    genre: str,
    chosen: Iterable[str],
    leave: Iterable[str] = (),
    probe: Callable[[Path], adopt_scan.Readability] = adopt_scan.probe_readability,
) -> SecondPlan:
    """Sort every chosen row into one outcome. ``genre`` empty clears.

    The rows are read through :func:`cratekit.tagging.rows.scanned`, adoption's
    census, and each readable file's genre and second genre through one
    container open. Only values are returned, so the handle may be closed
    before the gate.
    """
    wanted = genre.strip()
    if wanted:
        assert_genre_files(declared, wanted)
    held_out = frozenset(str(one) for one in leave)
    picked = sorted({str(one) for one in chosen})
    mapped = {str(row.ID): row for row in db.get_content()}
    present = {content_id: mapped[content_id] for content_id in picked if content_id in mapped}
    census = {track.content_id: track for track in rows.scanned(cfg, present, declared, probe)}
    counts = dict.fromkeys(OUTCOMES, 0)
    items: list[Item] = []

    def put(item: Item) -> None:
        counts[item.reason or WRITE] += 1
        items.append(item)

    for content_id in picked:
        track = census.get(content_id)
        if track is None:
            put(Item(content_id, "", "", "", wanted, LEAVE, ROW_GONE))
            continue
        path = track.path or ""
        if track.readability is not adopt_scan.Readability.READABLE or not path:
            reason = _PROBED.get(track.readability, FILE_UNREADABLE)
            put(Item(content_id, path, "", "", wanted, LEAVE, reason))
            continue
        read = _read(Path(path))
        if read is None:
            put(Item(content_id, path, "", "", wanted, LEAVE, FILE_UNREADABLE))
            continue
        file_genre, current = read
        reason = _reason(declared, file_genre, current, wanted, held=content_id in held_out)
        put(Item(content_id, path, file_genre, current, wanted, LEAVE if reason else WRITE, reason))
    return SecondPlan(genre=wanted, items=tuple(items), counts=MappingProxyType(counts))


def _reason(
    declared: taxonomy.Taxonomy, file_genre: str, current: str, wanted: str, *, held: bool
) -> str:
    """Why one readable row is left, or empty when it is written."""
    if current == wanted:
        return ALREADY if wanted else NONE_TO_CLEAR
    if held:
        return HELD_OUT
    if not wanted:
        return ""
    if routing.files_by_genre(declared, file_genre) is None:
        return GENRE_FILES_NOWHERE
    if routing.second_bucket(declared, file_genre, wanted) is None:
        return SAME_FOLDER
    return ""


def apply(second_plan: SecondPlan) -> Written:
    """Write each planned second genre onto its file and read it back.

    Each file is read again first and written only while it carries what the
    plan read; nothing raises for one file.
    """
    written = read_back = 0
    wrong: list[str] = []
    moved: list[str] = []
    failed: list[str] = []
    rewritten: list[Item] = []
    for item in second_plan.writes:
        target = Path(item.path)
        now = _read(target)
        if now is None or now != (item.genre, item.current):
            moved.append(item.path)
            continue
        took = (
            tags.write_tags(target, {FIELD: item.wanted})
            if item.wanted
            else tags.clear_tags(target, (FIELD,))
        )
        if not took:
            failed.append(item.path)
            continue
        written += 1
        after = _read(target)
        if after is None or after != (item.genre, item.wanted):
            wrong.append(item.path)
            continue
        read_back += 1
        rewritten.append(item)
    return Written(
        written=written,
        read_back=read_back,
        wrong=tuple(wrong),
        moved=tuple(moved),
        failed=tuple(failed),
        rewritten=tuple(rewritten),
    )


def chosen_rows(
    db: Any, *, rows_given: Sequence[str], rows_file: str | None, playlist: str | None
) -> tuple[str, ...]:
    """Every row the command line chose, by identifier, from a file, or by playlist.

    A rows file holds one content identifier per line; a blank line and a line
    opening ``#`` are skipped. Nothing chosen REFUSES, since an empty plan
    would read as a library with nothing to set.
    """
    picked = [str(one).strip() for one in rows_given if str(one).strip()]
    if rows_file:
        try:
            text = Path(rows_file).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise refuse(
                "tag-second-rows-unreadable",
                f"--rows-file {rows_file!r} could not be read: {exc}",
                steps=("name a readable text file of content identifiers, one per line",),
                origin=_ORIGIN,
                detail={"rows_file": rows_file},
            ) from exc
        picked += [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    if playlist:
        picked += playlist_members(db, playlist)
    if not picked:
        raise refuse(
            "tag-second-no-rows",
            "no row was chosen: name rows with --row, --rows-file or --playlist",
            steps=("run it again naming the rows to set or clear",),
            origin=_ORIGIN,
            detail={},
        )
    return tuple(dict.fromkeys(picked))


__all__ = [
    "ALREADY", "FIELD", "FILE_MISSING", "FILE_UNREADABLE", "GENRE_FILES_NOWHERE", "HELD_OUT",
    "Item", "LEAVE", "LEFT", "NONE_TO_CLEAR", "OUTCOMES", "PATH_SEPARATOR", "ROW_GONE",
    "SAME_FOLDER", "SecondPlan", "WORKFLOW", "WRITE", "Written", "apply", "assert_genre_files",
    "chosen_rows", "plan", "playlist_members",
]
