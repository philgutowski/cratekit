"""U119: the end of an adoption that files a track runs the additive refresh.

Driven through the real dispatcher on the cutover suite's library: two tracks
of one genre, the routing tree cut over, one of the two hearted into All
Favorites. The adoption files both into their band, and the favourite reaches
its folder's Favorites in the same job, the resume reporting what it added.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

from cratekit.core import rb_writer, taxonomy
from cratekit.core.exit_codes import ExitCode
from tests.test_cutover_cli import _adopt, _cut_over, _memberships
from tests.test_cutover_cli import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_cutover_cli import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_cutover_cli import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_cutover_cli import library as library  # noqa: PLC0414
from tests.test_cutover_cli import machine as machine  # noqa: PLC0414
from tests.test_cutover_cli import ready as ready  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
FAVORITES = DECLARED.sub_class("favorites")


def _heart(cfg, *content_ids: str) -> str:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        folder = handle.create_playlist_folder("Favorites")
        row = handle.create_playlist(FAVORITES.signal_playlist, parent=folder)
        for content_id in content_ids:
            handle.add_to_playlist(row, content_id)
        handle.session.commit()
        return str(row.ID)
    finally:
        rb_writer.close_db(handle)


def _favorites_playlists(cfg) -> dict[str, list[str]]:
    """Every live Favorites playlist of the class's name, by id, with its members."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        return {
            str(row.ID): sorted(
                str(entry.ContentID)
                for entry in handle.get_playlist_songs(PlaylistID=str(row.ID))
                if not rb_writer.membership_removed(entry)
            )
            for row in handle.get_playlist(Name=FAVORITES.display)
            if not rb_writer.is_folder(row) and not rb_writer.node_removed(row)
        }
    finally:
        rb_writer.close_db(handle)


def test_an_adoption_that_files_a_favourite_puts_it_in_its_folders_favorites(ready):
    """AE1's adoption half: the refresh runs at the end of the job, adds only,
    and the resume says what it added and that nothing is owed."""
    cfg, export, _root_id = ready
    source_id = _heart(cfg, "r-one")
    _cut_over(export)

    code, resumed = _adopt()

    assert code == int(ExitCode.OK), resumed
    favorites = _favorites_playlists(cfg)
    assert len(favorites) == 1, favorites
    ((playlist_id, members),) = favorites.items()
    assert members == ["r-one"] and playlist_id != source_id
    # The band still holds both, so Favorites is beside the band, not instead.
    held = _memberships(cfg)
    assert any(sorted(m) == ["r-one", "r-two"] for m in held.values()), held
    kept = resumed["data"]["progress"]["adoption"]["favorites"]
    assert kept["added"] == 1 and kept["removals_owed"] == 0 and kept["skipped"] == ""
    assert kept["created"] and kept["disagreements"] == []
    assert [w["code"] for w in resumed.get("warnings", [])] == []


def test_an_adoption_with_no_source_playlist_files_its_tracks_and_says_the_refresh_skipped(ready):
    cfg, export, _root_id = ready
    _cut_over(export)

    code, resumed = _adopt()

    assert code == int(ExitCode.OK), resumed
    assert _favorites_playlists(cfg) == {}
    kept = resumed["data"]["progress"]["adoption"]["favorites"]
    assert kept["added"] == 0 and "no live playlist" in kept["skipped"]
