"""Building a disposable library the adopt verbs can actually read.

Rows carry real files, since ``cratekit.adopt.scan.scan_rows`` stats each
location and a missing file is excluded from the plan. D1 applies: nothing
names a real volume, person or track.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from cratekit.core import config, locations, rb_writer
from tests.test_rb_writer_db import _build_disposable_database, _row

#: The two content rows ``_build_disposable_database`` seeds, with no location,
#: so every census reports them ``not-a-path``; named so a census size can count them.
BASELINE_CONTENT_IDS = ("1", "2")


@dataclass(frozen=True)
class Track:
    """One row to seed, and whether its file should exist on disk."""

    content_id: str
    filename: str
    genre: str
    #: rekordbox's soft-delete marker. A tombstone the census must skip.
    deleted: bool = False
    #: False writes the row and NOT the file, which is how a ``missing`` row is
    #: made. The census must still carry it, excluded, rather than dropping it.
    on_disk: bool = True
    #: The folder the row records, when not the library's music folder (U956): a
    #: location a prefix rule maps elsewhere. Nothing is written there.
    recorded_at: Path | None = None


def recorded_location(root: Path, filename: str) -> str:
    """The file URL rekordbox would record, built through ``cratekit.core.locations``."""
    return locations.location_url(root / "Music" / filename)


def _recorded(root: Path, track: Track) -> str:
    """The location one seeded row records."""
    if track.recorded_at is None:
        return recorded_location(root, track.filename)
    return locations.location_url(track.recorded_at / track.filename)


def build(cfg: config.Config, tracks: tuple[Track, ...] = ()) -> Path:
    """Create a disposable database at the configured path, holding ``tracks``.

    A supplied ``CRATEKIT_TEST_DB`` snapshot is NOT substituted here, unlike seam
    decisions Part 4's convention: these fixtures assert on rows they seeded.
    """
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    root = Path(cfg.library.root)
    music = root / "Music"
    music.mkdir(parents=True, exist_ok=True)

    db_path = Path(cfg.library.db_path)
    if db_path.exists():
        db_path.unlink()
    _build_disposable_database(db_path, with_tag_category=False)

    genres = {track.genre for track in tracks if track.genre}
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as db_session:
        for ordinal, name in enumerate(sorted(genres), start=100):
            db_session.add(_row(tables.DjmdGenre, ID=str(ordinal), Name=name))
        by_name = {name: str(ordinal) for ordinal, name in enumerate(sorted(genres), start=100)}
        for track in tracks:
            if track.on_disk and track.recorded_at is None:
                write_audio(music / track.filename)
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=track.content_id,
                    Title=track.filename,
                    GenreID=by_name.get(track.genre),
                    rb_local_deleted=1 if track.deleted else 0,
                    FolderPath=_recorded(root, track),
                )
            )
        db_session.commit()
    engine.dispose()
    return db_path


def write_audio(path: Path) -> Path:
    """A real, regular, non-dataless file the probe can read one byte from."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x00" * 64)
    return path


def copy_supplied(cfg: config.Config) -> Path | None:
    """Copy a supplied snapshot into the configured path, or None; the original is never opened."""
    supplied = rb_writer.integration_db_path()
    if supplied is None:
        return None
    target = Path(cfg.library.db_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(supplied, target)
    for suffix in rb_writer.db_sidecar_suffixes():
        sidecar = supplied.with_name(supplied.name + suffix)
        if sidecar.exists():
            shutil.copy2(sidecar, target.with_name(target.name + suffix))
    return target


__all__ = [
    "BASELINE_CONTENT_IDS",
    "Track",
    "build",
    "copy_supplied",
    "recorded_location",
    "write_audio",
]
