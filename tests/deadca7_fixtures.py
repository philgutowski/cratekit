"""A DEADCA7 push into a disposable database, written the way the push writes it (U185).

From the 2026-10-26 research note: a ``DEADCA7`` folder at the top of the
tree, its playlists and memberships, ``rb_local_usn`` bumped, hot cues
(``djmdCue`` rows of ``Kind`` above zero) with ``CueUpdated``, and analysis
files with ``AnalysisUpdated``. Written straight through SQLite, never this
product's writer, and read back whole. The content row update is a superset
of what the note found, which can only widen the proof.

The zero date is DEADCA7 0.2.3's own value (U285): :data:`ZERO_STAMP`, read
on a real push, on its folder, playlists, memberships and cues. The binding
reads it in local time, failing only west of UTC, which :func:`west_of_utc`
sets. The folder sits past the root's row count, where rekordbox's
renumbering would move it.
"""

from __future__ import annotations

import os
import sqlite3
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

FOLDER = "DEADCA7"
FOLDER_ID = "88000"
PLAYLISTS = {"88001": "warm up", "88002": "peak"}
#: Past any root row count a fixture here builds.
FOLDER_SEQ = 50
#: What the push stamps on what it wrote.
USN = 7777
#: The analysis path a push leaves on a track it pushed a grid for.
ANALYSIS_PATH = "/PIONEER/USBANLZ/dc7/0001/ANLZ0000.DAT"
ANALYSIS_UPDATED = 2
CUE_IDS = ("88101", "88102")
STAMP = "2026-10-30 12:00:00.000 +00:00"
#: What DEADCA7 0.2.3 stamps on a real push, read at sitting 98 (U285).
ZERO_STAMP = "0001-01-01T00:00:00Z"
#: US Eastern as a POSIX rule, so it needs no zone database on either platform.
EASTERN = "EST5EDT,M3.2.0,M11.1.0"


@dataclass(frozen=True)
class Pushed:
    """What one push wrote, by identifier."""

    folder_id: str
    playlist_ids: tuple[str, ...]
    content_ids: tuple[str, ...]
    pushed_track: str
    cue_ids: tuple[str, ...]


@contextmanager
def west_of_utc(zone: str = EASTERN) -> Iterator[None]:
    """The process's local time zone set west of UTC, and put back after, so the zero date bites."""
    before = os.environ.get("TZ")
    os.environ["TZ"] = zone
    time.tzset()
    try:
        yield
    finally:
        if before is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = before
        time.tzset()


def push(db_path: Path | str, content_ids: tuple[str, ...], *, stamp: str = STAMP) -> Pushed:
    """Write one push: the folder, two playlists holding ``content_ids``, cues, analysis.

    ``stamp`` is the date on every row; :data:`ZERO_STAMP` is the real app's.
    """
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, UUID, "
            "rb_local_deleted, rb_local_usn, created_at, updated_at) "
            "VALUES (?, ?, ?, 1, 'root', ?, 0, ?, ?, ?)",
            (FOLDER_ID, FOLDER_SEQ, FOLDER, "dc7-folder", USN, stamp, stamp),
        )
        for seq, (playlist_id, name) in enumerate(PLAYLISTS.items(), start=1):
            conn.execute(
                "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, UUID, "
                "rb_local_deleted, rb_local_usn, created_at, updated_at) "
                "VALUES (?, ?, ?, 0, ?, ?, 0, ?, ?, ?)",
                (playlist_id, seq, name, FOLDER_ID, f"dc7-{playlist_id}", USN, stamp, stamp),
            )
            for number, content_id in enumerate(content_ids, start=1):
                conn.execute(
                    "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, UUID, "
                    "rb_local_deleted, rb_local_usn, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?)",
                    (
                        f"{playlist_id}{number:02d}",
                        playlist_id,
                        content_id,
                        number,
                        f"dc7-m-{playlist_id}-{number}",
                        USN,
                        stamp,
                        stamp,
                    ),
                )
        track = content_ids[0]
        for kind, cue_id in enumerate(CUE_IDS, start=1):
            conn.execute(
                "INSERT INTO djmdCue (ID, ContentID, InMsec, Kind, Color, UUID, "
                "rb_local_deleted, rb_local_usn, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, 1, ?, 0, ?, ?, ?)",
                (cue_id, track, 1000 * kind, kind, f"dc7-cue-{cue_id}", USN, stamp, stamp),
            )
        conn.execute(
            "UPDATE djmdContent SET AnalysisDataPath = ?, AnalysisUpdated = ?, "
            "CueUpdated = ?, rb_local_usn = ? WHERE ID = ?",
            (ANALYSIS_PATH, ANALYSIS_UPDATED, "1", USN, track),
        )
        conn.commit()
    finally:
        conn.close()
    return Pushed(
        folder_id=FOLDER_ID,
        playlist_ids=tuple(PLAYLISTS),
        content_ids=tuple(content_ids),
        pushed_track=content_ids[0],
        cue_ids=CUE_IDS,
    )


def written(db_path: Path | str, pushed: Pushed) -> dict[str, list[tuple]]:
    """Every row the push wrote, whole and sorted by identifier: equal readings mean nothing moved."""
    nodes = (pushed.folder_id, *pushed.playlist_ids)
    marks = ", ".join("?" for _ in nodes)
    conn = sqlite3.connect(db_path)
    try:
        return {
            "djmdPlaylist": conn.execute(
                f"SELECT * FROM djmdPlaylist WHERE ID IN ({marks}) ORDER BY ID", nodes
            ).fetchall(),
            "djmdSongPlaylist": conn.execute(
                f"SELECT * FROM djmdSongPlaylist WHERE PlaylistID IN ({marks}) ORDER BY ID",
                nodes,
            ).fetchall(),
            "djmdCue": conn.execute(
                "SELECT * FROM djmdCue WHERE ContentID = ? ORDER BY ID", (pushed.pushed_track,)
            ).fetchall(),
            "djmdContent": conn.execute(
                "SELECT AnalysisDataPath, AnalysisUpdated, CueUpdated, Analysed "
                "FROM djmdContent WHERE ID = ?",
                (pushed.pushed_track,),
            ).fetchall(),
        }
    finally:
        conn.close()


def push_analysis_files(share: Path) -> dict[Path, tuple[bytes, int]]:
    """The analysis files a push writes under ``share``, with bytes and modification time."""
    folder = Path(share) / "PIONEER" / "USBANLZ" / "dc7" / "0001"
    folder.mkdir(parents=True, exist_ok=True)
    written: dict[Path, tuple[bytes, int]] = {}
    for suffix in ("DAT", "EXT", "2EX"):
        path = folder / f"ANLZ0000.{suffix}"
        path.write_bytes(f"PMAI pushed {suffix}".encode("ascii"))
        written[path] = (path.read_bytes(), path.stat().st_mtime_ns)
    return written


def analysis_files_now(files: dict[Path, tuple[bytes, int]]) -> dict[Path, tuple[bytes, int]]:
    """The same files read again, absent ones as ``None``."""
    return {
        path: (path.read_bytes(), path.stat().st_mtime_ns) if path.exists() else None
        for path in files
    }


def nested_namesake(db_path: Path | str, parent_id: str, node_id: str = "88900") -> str:
    """A folder named ``DEADCA7`` BELOW the root, under ``parent_id``: a namesake."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, UUID, "
            "rb_local_deleted, created_at, updated_at) VALUES (?, 1, ?, 1, ?, ?, 0, ?, ?)",
            (node_id, FOLDER, parent_id, f"namesake-{node_id}", STAMP, STAMP),
        )
        conn.commit()
    finally:
        conn.close()
    return node_id


__all__ = [
    "EASTERN",
    "FOLDER",
    "FOLDER_ID",
    "ZERO_STAMP",
    "Pushed",
    "analysis_files_now",
    "nested_namesake",
    "push",
    "push_analysis_files",
    "west_of_utc",
    "written",
]
