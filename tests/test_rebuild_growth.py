"""U246: a rebuild's second pass costs in proportion to its placements, not their square.

The speed survey of 2026-11-12 profiled ``crate rebuild --job`` on ten thousand
tracks and counted 106,781,222 calls of ``DeclaredPlacement.__hash__``, the
derived placement count squared, every one under the comprehension that picked
the second pass's favourites out of the placements: it built a set of every
derived placement once for each placement it tested. ``crate route resort``
runs the same worker and paid the same.

The proof here is a call count, never a wall clock: the worker is driven on a
disposable database at two sizes, the second twice the first, and the hash
calls it makes are counted. Work that grows with the placements doubles; the
old shape quadrupled. Every expected membership is spelled from the brief, a
track in its band playlist and, being a favourite, in its folder's Favorites,
and read straight from the file, never from the worker's own report.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

from cratekit.core import config, preflight, rb_writer, routing, session, taxonomy, tree_registry
from cratekit.write import rebuild, trees
from cratekit.write.tree_read import DeclaredPlacement
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
TREE = DECLARED.tree.id
FAVORITES = DECLARED.sub_class("favorites")
#: The genres the tracks are tagged with, so the placements spread over several
#: folders rather than one, as a real library's do.
GENRES = ("Deep House", "Tech House", "Afro House", "Organic House")
#: The smaller library, in tracks; the larger one holds twice as many.
SMALL = 24


def _drive(base: Path, monkeypatch, tracks: int) -> tuple[int, dict[tuple[str, str], set[str]]]:
    """Rebuild a library of ``tracks`` favourites; the hash calls and what was written.

    Each size is its own library, configuration and state, under its own
    directory, so the second rebuild reads nothing the first one recorded.
    """
    with monkeypatch.context() as patch:
        root = base / f"library-{tracks}"
        (root / "db").mkdir(parents=True)
        (root / "Music").mkdir(parents=True)
        for name, sub in (("CRATEKIT_CONFIG_DIR", "config"), ("CRATEKIT_STATE_DIR", "state")):
            patch.setenv(name, str(base / f"{sub}-{tracks}"))
        patch.setattr(config, "CONFIG_DIR", base / f"config-{tracks}", raising=False)
        patch.setattr(config, "STATE_DIR", base / f"state-{tracks}", raising=False)
        patch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfg = config.from_dict(
            valid_data(
                root,
                rekordbox={
                    "pinned_app_version": RECORDED_APP_VERSION,
                    "validated_on": "2026-08-01",
                },
            )
        )
        patch.setattr(config, "load", lambda *args, **kwargs: cfg)
        patch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
        patch.setattr(
            preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
        )
        patch.setattr(preflight, "local_mount_points", lambda: ())
        session.record_acknowledgment(cfg, terminal=lambda: True)

        ids = [str(index) for index in range(1, tracks + 1)]
        location = {one: f"{cfg.library.root}/Music/track {one}.flac" for one in ids}
        path = Path(cfg.library.db_path)
        _build_disposable_database(path)
        conn = sqlite3.connect(path)
        try:
            for one in ids:
                conn.execute(
                    "INSERT OR IGNORE INTO djmdContent (ID, Title, rb_local_deleted, "
                    "created_at, updated_at) VALUES (?, ?, 0, '2026-01-01', '2026-01-01')",
                    (one, f"track {one}"),
                )
                conn.execute(
                    "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = 0 WHERE ID = ?",
                    (location[one], one),
                )
            conn.commit()
        finally:
            conn.close()
        real_integrity_ok = rb_writer.integrity_ok
        patch.setattr(
            rb_writer,
            "integrity_ok",
            lambda target, **kwargs: real_integrity_ok(target, unlock=False),
        )

        db = rb_writer.open_db(path, unlock=False, cfg=cfg)
        try:
            tree_root = rb_writer.ensure_folder(db, DECLARED.tree.display)
            source = db.create_playlist(
                FAVORITES.signal_playlist, parent=db.create_playlist_folder("Favorites")
            )
            for one in ids:
                db.add_to_playlist(source, one)
            db.session.commit()
            registry = tree_registry.Registry(
                (
                    tree_registry.TreeRecord(
                        tree_id=TREE,
                        mode=tree_registry.Mode.DATABASE,
                        cutover_on=date(2026, 10, 9),
                        root_id=str(tree_root.ID),
                        source=tree_registry.DerivationSource.TAXONOMY,
                    ),
                )
            )
            tree_registry.write(cfg, registry)
            truth = [
                rebuild.Truth(
                    location=location[one],
                    genre=GENRES[index % len(GENRES)],
                    energy=DECLARED.energy.scale_max,
                    voxlevel=None,
                )
                for index, one in enumerate(ids)
            ]
            rows = [trees.ContentRow(one, location[one], deleted=False) for one in ids]

            calls = 0
            real_hash = DeclaredPlacement.__hash__

            def counted(self):
                nonlocal calls
                calls += 1
                return real_hash(self)

            patch.setattr(DeclaredPlacement, "__hash__", counted)
            report = rebuild.rebuild_tree(
                cfg,
                db,
                tree_id=TREE,
                registry=registry,
                declared=DECLARED,
                rows=rows,
                root_exists=lambda _root: True,
                analysis_roots=[Path(cfg.library.root)],
                vocal_threshold=None,
                truth=truth,
            )
            patch.setattr(DeclaredPlacement, "__hash__", real_hash)
            assert report.after.converged, report.after.summaries()
            tree_root_id = str(tree_root.ID)
        finally:
            rb_writer.close_db(db)
        return calls, _written(path, tree_root_id)


def _written(path: Path, root_id: str) -> dict[tuple[str, str], set[str]]:
    """Every playlist two levels under the root, by its folder and name, and its rows.

    Read straight from the file with sqlite, never through the worker's walk.
    """
    conn = sqlite3.connect(path)
    try:
        held: dict[tuple[str, str], set[str]] = {}
        for folder_id, folder in conn.execute(
            "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? "
            "AND COALESCE(rb_local_deleted, 0) = 0",
            (root_id,),
        ).fetchall():
            for playlist_id, name in conn.execute(
                "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0",
                (folder_id,),
            ).fetchall():
                held[(folder, name)] = {
                    str(row[0])
                    for row in conn.execute(
                        "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                        "AND COALESCE(rb_local_deleted, 0) = 0",
                        (playlist_id,),
                    )
                }
        return held
    finally:
        conn.close()


def _expected(tracks: int) -> dict[tuple[str, str], set[str]]:
    """From the brief: each track in its genre's top energy band, and in its Favorites."""
    held: dict[tuple[str, str], set[str]] = {}
    for index in range(tracks):
        one = str(index + 1)
        bucket = DECLARED.bucket(routing.resolve_bucket(DECLARED, GENRES[index % len(GENRES)]).bucket_id)
        band = routing.energy_sub(DECLARED, bucket.id, DECLARED.energy.scale_max)
        assert band is not None, "the shipped template declares no top band for a genre"
        held.setdefault((bucket.display, band.display), set()).add(one)
        held.setdefault((bucket.display, FAVORITES.display), set()).add(one)
    return held


def test_a_rebuilds_hash_calls_double_when_its_favourites_double(tmp_path, monkeypatch):
    """Twice the tracks, under three times the hashing: the placements, not their square."""
    small, small_written = _drive(tmp_path, monkeypatch, SMALL)
    large, large_written = _drive(tmp_path, monkeypatch, 2 * SMALL)

    assert small_written == _expected(SMALL)
    assert large_written == _expected(2 * SMALL)
    assert small > 0
    assert large < 3 * small, (
        f"{SMALL} favourites cost {small} placement hashes and {2 * SMALL} cost {large}, "
        f"{large / small:.1f} times as many for twice the tracks: the rebuild grows "
        f"with the square of its placements"
    )

