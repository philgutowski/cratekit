"""Building a disposable library the adopt verbs can actually read.

FOUR SUITES WANT THE SAME DATABASE and before this module they would each have
built one. That matters more than the line count: what "a library the adopt verbs
can read" means is a contract between the reader, the census and the two verbs,
and four copies of a contract is four chances for one of them to build a library
the code under test would never meet.

WHY THE ROWS CARRY REAL FILES. ``cratekit.adopt.scan.scan_rows`` stats every
recorded location, and a row whose file is absent classifies ``missing`` and is
EXCLUDED from the plan. A fixture that recorded paths nothing backs would build a
census in which nothing is ever applicable, and every assertion about an apply
would pass over a run that had nothing to do.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from cratekit.core import config, locations, rb_writer
from tests.test_rb_writer_db import _build_disposable_database, _row

#: The two content rows ``_build_disposable_database`` seeds. They carry no
#: location at all, so every census over a library built here reports them
#: ``not-a-path`` and excludes them. Named rather than subtracted silently: a
#: test asserting a census size has to know they are there.
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


def recorded_location(root: Path, filename: str) -> str:
    """The percent-encoded file URL rekordbox would record for this path.

    THROUGH ``cratekit.core.locations`` RATHER THAN BY HAND, because the encoding
    is the thing the resolver has to undo and a fixture that spelled it itself
    would be testing the two spellings against each other rather than the code.
    """
    return locations.location_url(root / "Music" / filename)


def build(cfg: config.Config, tracks: tuple[Track, ...] = ()) -> Path:
    """Create a disposable database at the configured path, holding ``tracks``.

    A supplied ``CRATEKIT_TEST_DB`` snapshot is NOT substituted here, and that is
    the one place this module diverges from the convention seam decisions Part 4
    sets. These fixtures assert against rows they seeded by identifier; a real
    snapshot carries somebody else's rows and every one of those assertions would
    be false about it. The reader's own suite is where a supplied snapshot
    substitutes, because what it asserts there is a property of the read rather
    than of the rows.
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
            if track.on_disk:
                write_audio(music / track.filename)
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=track.content_id,
                    Title=track.filename,
                    GenreID=by_name.get(track.genre),
                    rb_local_deleted=1 if track.deleted else 0,
                    FolderPath=recorded_location(root, track.filename),
                )
            )
        db_session.commit()
    engine.dispose()
    return db_path


def write_audio(path: Path) -> Path:
    """A real file the probe can open and read a byte from.

    The census only reads ONE byte, so the contents do not have to be a decodable
    container. What matters is that the file exists, is regular, and is not
    dataless, because those are the three questions ``probe_readability`` asks.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x00" * 64)
    return path


def copy_supplied(cfg: config.Config) -> Path | None:
    """Copy a supplied snapshot into the configured path, or answer None.

    The copy is what makes a supplied file safe to point a battery at: nothing
    here opens the original, so a run against a real snapshot cannot leave a
    fingerprint on it.
    """
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
