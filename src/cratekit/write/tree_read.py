"""What a governed tree holds and what the declaration puts in it, as values (U36, U119).

The two records the rebuild compares, and the walk that reads one of them, moved
here from the rebuild so that the genre favorites engine, which plans against
the same walk and hands the rebuild its placements, can import them without
the rebuild and the engine importing each other. The rebuild re-exports every
name, so a reader that knew them there still finds them there.

Layer: write.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cratekit.core import rb_writer


@dataclass(frozen=True, slots=True)
class DeclaredPlacement:
    """One file and the ONE destination the declaration puts it in.

    ``bucket`` and ``sub`` are stable taxonomy identifiers, never display names
    (R19, D5). A track that belongs in two places, which is what an additive
    sub-playlist means, produces two of these rather than one carrying a list:
    the pair is the unit the check compares and the write plans on, and folding
    them would make "this track is missing from one of its two playlists"
    inexpressible.
    """

    location: str
    bucket: str
    sub: str


@dataclass(frozen=True, slots=True)
class TreeNode:
    """One playlist inside a governed tree, its folder, and what it holds.

    Both identifiers AND both display names, deliberately. The identifiers are
    what a destination is resolved through, so a rename cannot orphan it; the
    display names are what the membership writer's find-or-create targets, so
    they are what a plan has to be phrased in. Carrying only one of the two
    would mean re-reading the database to get the other, from a walk that has
    already been done.
    """

    folder_id: str
    folder_display: str
    playlist_id: str
    playlist_display: str
    content_ids: frozenset[str] = frozenset()
    #: Every content identifier this playlist holds MORE THAN ONE row for.
    #:
    #: Carried beside the set rather than being lost inside it. A frozenset over
    #: the rows answers "is this track in this playlist", which is the question
    #: the comparison asks, and silently answers "yes" for a track sitting there
    #: twice. Two ``djmdSongPlaylist`` rows for one pair is a doubled tree inside
    #: one playlist: rekordbox shows the track twice, removing it once leaves the
    #: other, and the additive write cannot take either away. The check that
    #: exists to catch a doubled tree could not see doubling at this depth at all,
    #: and reported such a tree converged.
    doubled: frozenset[str] = frozenset()
    #: Whether rekordbox removed this playlist or the folder it sits in. The
    #: binding's lookup hands a removed node back beside the live ones, and
    #: this walk reports it as it always did, since the comparison that reads
    #: it was argued over what the lookup returns. The flag is for a reader
    #: asking where a track SITS, which a playlist nobody can see is not.
    removed: bool = False


def read_tree(db: Any, root_id: str) -> tuple[TreeNode, ...]:
    """Every playlist two levels under the adopted root, with its membership.

    THE WALK GOES DOWN FROM THE ADOPTED ROOT BY IDENTIFIER, never by name. A walk
    that resolved the tree by its display name would find a namesake anywhere in
    the library and report on that instead, which is the silent parallel tree
    arriving through the check meant to detect it.

    TWO LEVELS, because that is the depth the taxonomy declares: a tree holds
    folders and a folder holds playlists. A playlist sitting directly under the
    root is not a shape any declared destination can name, so its membership is
    not part of this comparison and is left alone rather than being reported as a
    difference nobody can act on.

    The folder list is MATERIALIZED before the inner queries run. Iterating one
    query while issuing others on the same session is the shape that made a
    previous unit's row index report an empty library on its second pass.

    A MEMBERSHIP MARKED REMOVED IS NOT HELD (R-758). The binding's query hands
    back a soft deleted row beside the live ones and rekordbox shows no track
    for it, so a track moved out of a playlist would still read as sitting
    there, and the plan that moved it would plan the same move for ever.
    """
    out: list[TreeNode] = []
    folders = list(db.get_playlist(ParentID=str(root_id)))
    for folder in folders:
        playlists = list(db.get_playlist(ParentID=str(folder.ID)))
        for playlist in playlists:
            members = [
                str(row.ContentID)
                for row in db.get_playlist_songs(PlaylistID=str(playlist.ID))
                if not rb_writer.membership_removed(row)
            ]
            # COUNTED BEFORE IT IS COLLAPSED. The set is what the comparison
            # needs; the multiplicity is a fact that only exists before the set
            # is taken, and it is the one this walk used to throw away.
            seen: dict[str, int] = {}
            for content_id in members:
                seen[content_id] = seen.get(content_id, 0) + 1
            out.append(
                TreeNode(
                    folder_id=str(folder.ID),
                    folder_display=str(folder.Name),
                    playlist_id=str(playlist.ID),
                    playlist_display=str(playlist.Name),
                    content_ids=frozenset(seen),
                    doubled=frozenset(
                        content_id for content_id, count in seen.items() if count > 1
                    ),
                    removed=rb_writer.node_removed(folder)
                    or rb_writer.node_removed(playlist),
                )
            )
    return tuple(out)


__all__ = ["DeclaredPlacement", "TreeNode", "read_tree"]
