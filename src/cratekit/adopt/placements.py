"""The placement reader: where the tree already files the tracks a plan routes.

WHY THIS EXISTS (R-731). The adoption plan placed each track by its genre and
its file's energy reading and never read the tree it was about to write, and the
membership writer is add only. On a copy of a real library 569 of 700 additions
were a second energy band beside the one the track already held. This module is
the read that was missing: it answers, for every bucket, which of that bucket's
competing subs each track sits in, and hands the answer to the plan layer as a
value.

IT READS THE DATABASE THE CENSUS READ AND NO OTHER. The path is
:func:`cratekit.core.rb_writer.live_db_path` over the configuration it is
handed, which is the path :func:`cratekit.adopt.collection.read_collection`
opens, through the same open with the same read intent. It resolves no path of
its own, so a run pointed at a disposable copy reads the copy, and there is no
second spelling of "the database" that could name a different file.

THIS MODULE READS AND CANNOT WRITE, for the reason and by the means the
collection reader gives: every open leaves ``require_closed`` False, nothing
here imports the session module, and nothing calls ``commit``.

UNREAD IS THE WRITER'S OWN REFUSAL, ASKED EARLY. A tree still on the bridge has
no adopted root to walk down from, so there is nothing to read, and that is the
same tree :func:`cratekit.write.trees.write_tree_membership` refuses to write.
The two are kept one condition by asking the one function,
:func:`cratekit.core.tree_registry.anchored_root`, rather than by spelling its
rules again here: a plan that says ``unread`` is a plan whose apply cannot land
a membership, so nothing an unread plan failed to withhold is ever written.

A NODE IS RESOLVED BY IDENTIFIER FIRST AND BY DECLARED NAME SECOND, which is
the order :func:`cratekit.write.rebuild.resolve_destinations` argues. What
competes is decided from taxonomy identifiers, through
:func:`cratekit.core.routing.competing_subs`. The declared display name is how
a node a previous write never recorded is recognised as a destination at all,
which is the one thing a library and a taxonomy share before any write.

Layer: modules. It reads configuration and the database and names no verb.
"""

from __future__ import annotations

from typing import Sequence

from cratekit.adopt.plan import UNREAD, Placements
from cratekit.core import config, convergence, rb_writer, routing, taxonomy, tree_registry
from cratekit.write import rebuild
from cratekit.write.routing_pass import destination


def placements_from(
    declared: taxonomy.Taxonomy,
    nodes: Sequence[rebuild.TreeNode],
    record: convergence.TreeConvergence | None,
) -> Placements:
    """What a tree already read holds, as the plan layer's value. No input.

    EVERY NODE THAT ANSWERS FOR A DESTINATION COUNTS, the recorded one and
    every node carrying the declared names. A folder renamed in rekordbox and
    then created again under the taxonomy's name leaves two nodes for one
    destination, and a track in either one holds that sub. Choosing between
    them here would make what a track holds depend on which node a query
    yielded first. THIS IS NOT ``resolve_destinations``'S TIE RULE AND IS NOT
    MEANT TO BE: that function picks the one node a write goes to and refuses
    to choose between two, and this one asks where a track sits, which has no
    reason to choose.

    WHICH NAME A TRACK IS HELD UNDER IS KEPT, because the writer finds a
    playlist by its declared name and cannot see a renamed one. A sub held
    only through a node that does not carry the declared names goes in
    ``unnamed`` as well, and the plan withholds on it even when it is the very
    sub the plan names.

    A PLAYLIST NO COMPETING SUB RESOLVES TO IS NOT A PLACE. A sub class, a
    playlist a person made by hand inside a bucket folder, a folder the
    taxonomy declares no bucket for: none of them is read, because none of
    them can compete.

    A PLAYLIST REKORDBOX REMOVED IS NOT A PLACE EITHER (R-758). It shows no
    track, and the move finds the playlists it removes from among the live
    ones, so a sub held only through a removed playlist would be planned for a
    removal nothing could perform.
    """
    nodes = [node for node in nodes if not node.removed]
    by_ids = {(node.folder_id, node.playlist_id): node for node in nodes}
    by_display: dict[tuple[str, str], list[rebuild.TreeNode]] = {}
    for node in nodes:
        by_display.setdefault((node.folder_display, node.playlist_display), []).append(node)

    held: dict[str, dict[str, set[str]]] = {}
    unnamed: dict[str, dict[str, set[str]]] = {}
    for bucket in declared.buckets:
        _kind, competing = routing.competing_subs(declared, bucket.id)
        for sub_id in sorted(competing):
            named = by_display.get(destination(declared, bucket.id, sub_id), ())
            under_the_name = {cid for node in named for cid in node.content_ids}
            under_another: set[str] = set()
            recorded = None if record is None else record.node(bucket.id, sub_id)
            if recorded is not None:
                node = by_ids.get((recorded.folder_id, recorded.playlist_id))
                if node is not None and node not in named:
                    under_another = set(node.content_ids) - under_the_name
            for content_id in under_the_name | under_another:
                held.setdefault(bucket.id, {}).setdefault(content_id, set()).add(sub_id)
            for content_id in under_another:
                unnamed.setdefault(bucket.id, {}).setdefault(content_id, set()).add(sub_id)

    return Placements(read=True, held=_frozen(held), unnamed=_frozen(unnamed))


def _frozen(found: dict[str, dict[str, set[str]]]) -> dict[str, dict[str, tuple[str, ...]]]:
    return {
        bucket_id: {content_id: tuple(sorted(subs)) for content_id, subs in tracks.items()}
        for bucket_id, tracks in found.items()
    }


def read_placements(cfg: config.Config, declared: taxonomy.Taxonomy) -> Placements:
    """The configured library's tree, read once, as what each track holds.

    NOT CACHED, unlike the collection. A worker reads the placements, writes
    memberships, and may be run again in the same process, and a cache would
    hand the second run the tree as it stood before the first one wrote.

    THE TWO REFUSALS ``anchored_root`` RAISES ANSWER ``UNREAD`` and nothing
    else does. A database that is missing, a pin that fails, a convergence
    record that cannot be parsed: each is raised as it came, because each is a
    reason the plan cannot be trusted rather than a tree with nothing in it.

    THE HANDLE IS CLOSED BEFORE THIS RETURNS, in a ``finally``, through
    ``close_db``, for the reason the collection reader gives.
    """
    registry = tree_registry.read(cfg)
    handle = rb_writer.open_db(
        rb_writer.live_db_path(cfg),
        require_closed=False,
        check_app_version=False,
        cfg=cfg,
    )
    try:
        try:
            root_id = tree_registry.anchored_root(
                declared.tree.id,
                registry,
                root_exists=lambda root: handle.get_playlist(ID=str(root)) is not None,
            )
        except (tree_registry.TreeModeRefused, tree_registry.RegistrySkew):
            return UNREAD
        nodes = rebuild.read_tree(handle, root_id)
    finally:
        rb_writer.close_db(handle)
    state = convergence.read(cfg)
    return placements_from(declared, nodes, state.tree(declared.tree.id))


__all__ = [
    "placements_from",
    "read_placements",
]
