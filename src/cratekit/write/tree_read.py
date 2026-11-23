"""What a governed tree holds and what the declaration puts in it, as values (U36, U119).

Here so the genre favorites engine and the rebuild can both import them without
importing each other; the rebuild re-exports every name. Layer: write.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from cratekit.core import rb_writer


@dataclass(frozen=True, slots=True)
class DeclaredPlacement:
    """One file and the ONE destination the declaration puts it in.

    ``bucket`` and ``sub`` are stable taxonomy identifiers, never display names
    (R19, D5). A track that belongs in two places produces two of these, so
    "missing from one of its two playlists" stays expressible.
    """

    location: str
    bucket: str
    sub: str


@dataclass(frozen=True, slots=True)
class TreeNode:
    """One playlist inside a governed tree, its folder, and what it holds.

    Both identifiers, which a destination resolves through so a rename cannot
    orphan it, and both display names, which the membership writer's
    find-or-create targets.
    """

    folder_id: str
    folder_display: str
    playlist_id: str
    playlist_display: str
    content_ids: frozenset[str] = frozenset()
    #: Every content identifier this playlist holds MORE THAN ONE row for: a
    #: doubled tree inside one playlist, which the set alone reads as held once.
    doubled: frozenset[str] = frozenset()
    #: Whether rekordbox removed this playlist or its folder. The walk still
    #: reports the node; the flag is for a reader asking where a track SITS.
    removed: bool = False


def read_tree(db: Any, root_id: str) -> tuple[TreeNode, ...]:
    """Every playlist two levels under the adopted root, with its membership.

    Down from the adopted root by identifier, never by name. The folder list is
    materialized before the inner queries run, since iterating one query while
    issuing others on the session misreads. A membership marked removed is not
    held (R-758).
    """
    out: list[TreeNode] = []
    folders = list(db.get_playlist(ParentID=str(root_id)))
    for folder in folders:
        playlists = list(db.get_playlist(ParentID=str(folder.ID)))
        for playlist in playlists:
            # Counted before it is collapsed, so a doubled membership is seen.
            seen = Counter(
                str(row.ContentID)
                for row in db.get_playlist_songs(PlaylistID=str(playlist.ID))
                if not rb_writer.membership_removed(row)
            )
            out.append(
                TreeNode(
                    folder_id=str(folder.ID),
                    folder_display=str(folder.Name),
                    playlist_id=str(playlist.ID),
                    playlist_display=str(playlist.Name),
                    content_ids=frozenset(seen),
                    doubled=frozenset(content_id for content_id, count in seen.items() if count > 1),
                    removed=rb_writer.node_removed(folder) or rb_writer.node_removed(playlist),
                )
            )
    return tuple(out)


__all__ = ["DeclaredPlacement", "TreeNode", "read_tree"]
