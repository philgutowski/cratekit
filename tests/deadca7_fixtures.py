"""A DEADCA7 push into a disposable database, written the way the push writes it (U185).

The research note of 2026-10-26 read the push's SQL from the app: a folder named
``DEADCA7`` at the top of the playlist tree, playlists in it with their
memberships, ``rb_local_usn`` bumped on what it wrote, hot cues per track
(``djmdCue`` rows of ``Kind`` above zero) with ``CueUpdated`` set, and grids
and waveforms as analysis files with ``AnalysisUpdated`` set. This module
writes those rows straight through SQLite, as another app would, never through
this product's writer, and reads them back whole so a test can assert they are
byte for byte what they were.

THE FOLDER'S POSITION IS PAST THE ROOT'S ROW COUNT on purpose: rekordbox's
binding renumbers every root sibling at or past a position a caller names, so
the folder sits where such a write would move it, and a test that writes beside
it would see it move.
"""

from __future__ import annotations

import sqlite3
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


@dataclass(frozen=True)
class Pushed:
    """What one push wrote, by identifier."""

    folder_id: str
    playlist_ids: tuple[str, ...]
    content_ids: tuple[str, ...]
    pushed_track: str
    cue_ids: tuple[str, ...]


def push(db_path: Path | str, content_ids: tuple[str, ...]) -> Pushed:
    """Write one push: the folder, two playlists holding ``content_ids``, cues, analysis."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, UUID, "
            "rb_local_deleted, rb_local_usn, created_at, updated_at) "
            "VALUES (?, ?, ?, 1, 'root', ?, 0, ?, ?, ?)",
            (FOLDER_ID, FOLDER_SEQ, FOLDER, "dc7-folder", USN, STAMP, STAMP),
        )
        for seq, (playlist_id, name) in enumerate(PLAYLISTS.items(), start=1):
            conn.execute(
                "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, UUID, "
                "rb_local_deleted, rb_local_usn, created_at, updated_at) "
                "VALUES (?, ?, ?, 0, ?, ?, 0, ?, ?, ?)",
                (playlist_id, seq, name, FOLDER_ID, f"dc7-{playlist_id}", USN, STAMP, STAMP),
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
                        STAMP,
                        STAMP,
                    ),
                )
        track = content_ids[0]
        for kind, cue_id in enumerate(CUE_IDS, start=1):
            conn.execute(
                "INSERT INTO djmdCue (ID, ContentID, InMsec, Kind, Color, UUID, "
                "rb_local_deleted, rb_local_usn, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, 1, ?, 0, ?, ?, ?)",
                (cue_id, track, 1000 * kind, kind, f"dc7-cue-{cue_id}", USN, STAMP, STAMP),
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
    """Every row the push wrote, whole, as the database holds it now.

    The folder, its playlists, their memberships, the cue rows, and the
    pushed track's analysis and cue columns, each table's rows sorted by
    identifier, so two readings compare equal exactly when nothing moved.
    """
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
    """The analysis files a push writes for its grid and waveforms, under ``share``.

    Answers each file's bytes and modification time, so a test can assert no
    step rewrote, moved or removed one.
    """
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
    "FOLDER",
    "FOLDER_ID",
    "Pushed",
    "analysis_files_now",
    "nested_namesake",
    "push",
    "push_analysis_files",
    "written",
]
