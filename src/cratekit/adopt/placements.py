"""The placement reader: where the tree already files the tracks a plan routes.

Without it, an add only writer filed a second band beside the one a track held
(R-731). It answers, for every bucket, which competing subs each track sits in,
as a value for the plan layer.

IT READS THE DATABASE THE CENSUS READ AND NO OTHER, through
:func:`cratekit.core.rb_writer.live_db_path` over the configuration handed in,
the path :func:`cratekit.adopt.collection.read_collection` opens, so a run
pointed at a disposable copy reads the copy. It reads and cannot write, as the
collection reader: every open leaves ``require_closed`` False, nothing here
imports the session module, and nothing calls ``commit``.

UNREAD IS THE WRITER'S OWN REFUSAL, ASKED EARLY: a tree with no adopted root
is the tree :func:`cratekit.write.trees.write_tree_membership` refuses, and
both ask :func:`cratekit.core.tree_registry.anchored_root`, so an unread plan
is one whose apply cannot land a membership.

A NODE IS RESOLVED BY IDENTIFIER FIRST AND BY DECLARED NAME SECOND, the order
:func:`cratekit.write.rebuild.resolve_destinations` argues. What competes is
decided from taxonomy identifiers through
:func:`cratekit.core.routing.competing_subs`; the declared display name is how
a node no write recorded is recognised as a destination at all.

THE VOCAL SUBS ARE READ HERE TOO (R-788), with the tag that says a track
belongs in one, from the same open of the same database. The tag is the My Tag
value the vocals verb writes, found by the names it writes it under,
:data:`cratekit.write.metadata_cli.CATEGORY` and ``VALUE_VOX``. Whether the
library has a calibrated cut is read through that module's one reader.

Layer: modules. It reads configuration and the database and names no verb.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from cratekit.adopt.plan import (
    NO_VOCALS,
    UNREAD,
    Placements,
    Vocals,
    derived_classes,
    in_own_folder,
    vocal_sub,
)
from cratekit.core import config, convergence, rb_writer, routing, taxonomy, tree_registry
from cratekit.write import metadata_cli, rebuild
from cratekit.write.routing_pass import destination

_ORIGIN = ("adopt", "placements")


def named_place(declared: taxonomy.Taxonomy, bucket_id: str, sub_id: str) -> tuple[str, str]:
    """The folder and playlist names one competing sub of a bucket answers to.

    A FORMER PLACE RESOLVES HERE AND NOT IN ``destination`` (R-797), which
    every writer that FILES a track asks and which refuses an identifier no
    routing rule returns. A former place is read and left, never filed into,
    so only the callers that read or leave a place ask this. The folder is the
    declared bucket's name as it is now, so a renamed folder is still found. A
    SPLIT PLACE resolves as the holder's own place, asked of the holder (U118).
    """
    split = routing.split_place(declared, bucket_id, sub_id)
    if split is not None:
        return named_place(declared, split.bucket, split.sub)
    former = routing.former_place(declared, bucket_id, sub_id)
    if former is None:
        return destination(declared, bucket_id, sub_id)
    return declared.bucket(former.bucket).display, former.display


def recorded_under(declared: taxonomy.Taxonomy, bucket_id: str, sub_id: str) -> tuple[str, str]:
    """The bucket and sub identifiers a previous write recorded this place's node under.

    A former place was written while it was a sub of the bucket whose folder
    holds it, so its node is recorded there; asked under the declarer it would
    read a renamed playlist as absent. A split place is recorded wherever the
    holder's is (U118).
    """
    split = routing.split_place(declared, bucket_id, sub_id)
    if split is not None:
        return recorded_under(declared, split.bucket, split.sub)
    former = routing.former_place(declared, bucket_id, sub_id)
    if former is None:
        return bucket_id, sub_id
    return former.bucket, former.sub


def placements_from(
    declared: taxonomy.Taxonomy,
    nodes: Sequence[rebuild.TreeNode],
    record: convergence.TreeConvergence | None,
) -> Placements:
    """What a tree already read holds, as the plan layer's value. No input.

    EVERY NODE THAT ANSWERS FOR A DESTINATION COUNTS, the recorded one and
    every node carrying the declared names, so what a track holds never
    depends on which node a query yielded first. This is not
    ``resolve_destinations``'s tie rule, which picks the one node a write goes
    to; this asks where a track sits.

    WHICH NAME A TRACK IS HELD UNDER IS KEPT, because the writer finds a
    playlist by its declared name: a sub held only through a node without the
    declared names goes in ``unnamed`` too, and the plan withholds on it.

    A playlist no competing sub resolves to is not a place, and neither is one
    rekordbox removed (R-758): the move removes only from live playlists. A
    FORMER PLACE IS READ UNDER BOTH BUCKETS IT COMPETES IN (R-797), and a
    SPLIT PLACE under both too (U118): every track in the holder's band holds
    the split place in the declarer, whatever its genre, and which it leaves
    is the move's question.

    THE DERIVED SUB CLASSES AND THE FOLDER'S OTHER PLAYLISTS ARE READ BESIDE
    THEM (R-1965), from the same nodes: the move across genre folders leaves a
    folder's ``with vox`` and Favorites with its band, and a track another
    playlist of that folder still holds keeps the Favorites there. The folder
    is the one the bucket's own places answer from, by identifier, so a
    renamed folder is still the bucket's.
    """
    by_ids, by_display = _indexed(nodes)
    by_folder: dict[str, list[rebuild.TreeNode]] = {}
    for node in by_ids.values():
        by_folder.setdefault(node.folder_id, []).append(node)

    held: dict[str, dict[str, set[str]]] = {}
    unnamed: dict[str, dict[str, set[str]]] = {}
    doubled: dict[str, dict[str, set[str]]] = {}
    derived: dict[str, dict[str, set[str]]] = {}
    derived_unnamed: dict[str, dict[str, set[str]]] = {}
    others: dict[str, dict[str, set[str]]] = {}
    for bucket in declared.buckets:
        _kind, competing = routing.competing_subs(declared, bucket.id)
        known: set[tuple[str, str]] = set()
        folders: set[str] = set()
        for sub_id in sorted(competing):
            answering = _read_place(
                declared, bucket.id, sub_id, by_display, by_ids, record, held, unnamed
            )
            # A pair two rows hold in one node is a double (R-781); a track in
            # two nodes that both answer for one sub is two playlists, not one.
            for content_id in {cid for node in answering for cid in node.doubled}:
                doubled.setdefault(bucket.id, {}).setdefault(content_id, set()).add(sub_id)
            known.update((node.folder_id, node.playlist_id) for node in answering)
            if in_own_folder(declared, bucket.id, sub_id):
                folders.update(node.folder_id for node in answering)
        for sub_id in derived_classes(declared, bucket.id):
            answering = _read_place(
                declared, bucket.id, sub_id, by_display, by_ids, record, derived, derived_unnamed
            )
            known.update((node.folder_id, node.playlist_id) for node in answering)
            folders.update(node.folder_id for node in answering)
        for folder_id in folders:
            for node in by_folder.get(folder_id, ()):
                if (node.folder_id, node.playlist_id) in known:
                    continue
                for content_id in node.content_ids:
                    found = others.setdefault(bucket.id, {}).setdefault(content_id, set())
                    found.add(node.playlist_display)

    return Placements(
        read=True,
        held=_frozen(held),
        unnamed=_frozen(unnamed),
        doubled=_frozen(doubled),
        derived=_frozen(derived),
        derived_unnamed=_frozen(derived_unnamed),
        others=_frozen(others),
    )


def _read_place(
    declared: taxonomy.Taxonomy,
    bucket_id: str,
    sub_id: str,
    by_display: Mapping[tuple[str, str], Sequence[rebuild.TreeNode]],
    by_ids: Mapping[tuple[str, str], rebuild.TreeNode],
    record: convergence.TreeConvergence | None,
    held: dict[str, dict[str, set[str]]],
    unnamed: dict[str, dict[str, set[str]]],
) -> list[rebuild.TreeNode]:
    """Who one place of a bucket holds, into ``held``, and under another name
    only, into ``unnamed``; returns the nodes answering for it. ONE BODY for a
    competing sub and a derived class, so both find a renamed playlist alike."""
    under = recorded_under(declared, bucket_id, sub_id)
    recorded = None if record is None else record.node(*under)
    answering, under_the_name, under_another = _answering(
        by_display, by_ids, named_place(declared, bucket_id, sub_id), recorded
    )
    for content_id in under_the_name | under_another:
        held.setdefault(bucket_id, {}).setdefault(content_id, set()).add(sub_id)
    for content_id in under_another:
        unnamed.setdefault(bucket_id, {}).setdefault(content_id, set()).add(sub_id)
    return answering


def _indexed(
    nodes: Sequence[rebuild.TreeNode],
) -> tuple[dict[tuple[str, str], rebuild.TreeNode], dict[tuple[str, str], list[rebuild.TreeNode]]]:
    """The live nodes of a tree, by their identifiers and by their names.

    A playlist rekordbox removed is in neither (R-758). ONE BODY for both
    readers, so which nodes count and how one is keyed is decided once.
    """
    live = [node for node in nodes if not node.removed]
    by_ids = {(node.folder_id, node.playlist_id): node for node in live}
    by_display: dict[tuple[str, str], list[rebuild.TreeNode]] = {}
    for node in live:
        by_display.setdefault((node.folder_display, node.playlist_display), []).append(node)
    return by_ids, by_display


def _answering(
    by_display: Mapping[tuple[str, str], Sequence[rebuild.TreeNode]],
    by_ids: Mapping[tuple[str, str], rebuild.TreeNode],
    names: tuple[str, str],
    recorded: convergence.DestinationNode | None,
) -> tuple[list[rebuild.TreeNode], set[str], set[str]]:
    """The nodes answering for one destination, and who they hold under which name.

    Returns every answering node, the tracks held through a node carrying the
    declared names, and the tracks held ONLY through the recorded node when it
    no longer carries them. ONE BODY for the competing and the vocal subs, so
    the two cannot recognise a renamed playlist differently.
    """
    named = list(by_display.get(names, ()))
    under_the_name = {cid for node in named for cid in node.content_ids}
    under_another: set[str] = set()
    answering = list(named)
    if recorded is not None:
        node = by_ids.get((recorded.folder_id, recorded.playlist_id))
        if node is not None and node not in named:
            under_another = set(node.content_ids) - under_the_name
            answering.append(node)
    return answering, under_the_name, under_another


def vocals_from(
    declared: taxonomy.Taxonomy,
    nodes: Sequence[rebuild.TreeNode],
    record: convergence.TreeConvergence | None,
    tagged: frozenset[str] | None,
    *,
    calibrated: bool,
) -> Vocals:
    """Who carries the vox tag and which vocal subs hold them, as a value. No input.

    ``tagged`` is what :func:`vox_tagged` answered, None when the library has no
    such tag. ``calibrated`` has no default, because the permissive answer would
    file a library nobody calibrated.

    ONLY A BUCKET WITH A VOCAL SUB is read, asked of
    :func:`cratekit.adopt.plan.vocal_sub` as the plan asks: a playlist of the
    vocal name where that name is one of the bucket's own subs is not a vocal
    place. Every answering node counts and its name is kept, through the body
    both readers share. A BUCKET WHOSE VOCAL SUB ANSWERS UNDER ANOTHER NAME
    ONLY IS NAMED, because the plan adds tracks NOT in the sub and the writer
    would make the declared playlist beside it.
    """
    by_ids, by_display = _indexed(nodes)

    filed: dict[str, frozenset[str]] = {}
    unnamed: dict[str, frozenset[str]] = {}
    renamed: set[str] = set()
    for bucket in declared.buckets:
        sub_id = vocal_sub(declared, bucket.id)
        if sub_id is None:
            continue
        names = destination(declared, bucket.id, sub_id)
        recorded = None if record is None else record.node(bucket.id, sub_id)
        answering, under_the_name, under_another = _answering(by_display, by_ids, names, recorded)
        if under_the_name or under_another:
            filed[bucket.id] = frozenset(under_the_name | under_another)
        if under_another:
            unnamed[bucket.id] = frozenset(under_another)
        if answering and not by_display.get(names):
            renamed.add(bucket.id)

    return Vocals(
        read=True,
        has_sub=has_vocal_sub(declared),
        calibrated=calibrated,
        tag_found=tagged is not None,
        tagged=frozenset() if tagged is None else tagged,
        filed=filed,
        unnamed=unnamed,
        renamed=frozenset(renamed),
    )


def has_vocal_sub(declared: taxonomy.Taxonomy) -> bool:
    """Whether any bucket of this taxonomy has a vocal sub to file under."""
    return any(vocal_sub(declared, bucket.id) is not None for bucket in declared.buckets)


def vocal_standing(cfg: config.Config, declared: taxonomy.Taxonomy) -> bool:
    """Whether this library can be filed vocally at all: a sub to file under and a cut on record.

    ASKED BEFORE ANYTHING EXPENSIVE, so an unreadable calibration refuses
    before the census walks a library. The calibration is read only when a
    bucket has a vocal sub, through
    :func:`cratekit.write.metadata_cli.load_vocal_threshold`, which refuses an
    unreadable one; with no vocal sub its state is not this run's to refuse.
    """
    if not has_vocal_sub(declared):
        return False
    return metadata_cli.load_vocal_threshold(cfg) is not None


def _removed(row: Any, what: str) -> bool:
    """Whether rekordbox removed one My Tag row, through the one read of the marker."""
    return rb_writer.soft_deleted(
        row,
        message=(
            f"the {what} row {getattr(row, 'ID', '?')!r} cannot say whether "
            f"rekordbox removed it, and treating that as live would file a "
            f"track under a vocal sub for a tag nobody can see on it"
        ),
        origin=_ORIGIN,
        detail={"row": str(getattr(row, "ID", "")), "kind": what},
    )


def vox_tagged(db: Any) -> frozenset[str] | None:
    """Every track carrying the vox My Tag, or None when the library has no such tag.

    A value of the vox name inside a category of the category name: the same
    value under another category is another tag. NONE IS NOT THE EMPTY SET, a
    library with the tag and nothing carrying it, and the plan tells them apart.

    NOT THE WRITER'S FIND, AND THE DIFFERENCE IS THE MARKER.
    :func:`cratekit.core.rb_writer.ensure_my_tag_value` takes the first
    category of the name and reads no soft delete marker; that half is in the
    ledger as a residual. A ROW REKORDBOX REMOVED IS NOT A TAG (R-758): a
    removed association is a tag a person took off. A row that cannot say
    whether it was removed refuses, through the one read of the marker.
    """
    categories = {
        str(tag.ID)
        for tag in db.get_my_tag(Name=metadata_cli.CATEGORY)
        if not _removed(tag, "My Tag")
    }
    values = [
        tag
        for tag in db.get_my_tag(Name=metadata_cli.VALUE_VOX)
        if str(getattr(tag, "ParentID", "") or "") in categories and not _removed(tag, "My Tag")
    ]
    if not values:
        return None
    return frozenset(
        str(song.ContentID)
        for value in values
        for song in db.get_my_tag_songs(MyTagID=str(value.ID))
        if not _removed(song, "My Tag association")
    )


def _frozen(found: dict[str, dict[str, set[str]]]) -> dict[str, dict[str, tuple[str, ...]]]:
    return {
        bucket_id: {content_id: tuple(sorted(subs)) for content_id, subs in tracks.items()}
        for bucket_id, tracks in found.items()
    }


#: One read of the tree: its nodes, the node record, and the tracks carrying the vox tag.
_Read = tuple[Sequence[rebuild.TreeNode], convergence.TreeConvergence | None, frozenset[str] | None]


def _read_tree(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    tags: bool,
    one_read: rb_writer.SharedRead | None = None,
) -> _Read | None:
    """The configured library's tree, read once. None when it cannot be read.

    Returns the nodes, the node record a previous write left, and, when
    ``tags`` is asked, what :func:`vox_tagged` answered over the same handle; a
    caller asking nothing about vocals, the move verb, opens no table it does
    not need. ONLY THE TWO REFUSALS ``anchored_root`` RAISES ANSWER NONE: a
    missing database, a failed pin or an unparseable record is raised as it
    came, a reason the plan cannot be trusted. The handle is closed in a
    ``finally``; a read only report's one handle, ``one_read`` (U267), is read
    through and released.
    """
    registry = tree_registry.read(cfg)
    handle = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    )
    try:
        try:
            root_id = tree_registry.anchored_root(
                declared.tree.id,
                registry,
                root_exists=lambda root: handle.get_playlist(ID=str(root)) is not None,
            )
        except (tree_registry.TreeModeRefused, tree_registry.RegistrySkew):
            return None
        nodes = rebuild.read_tree(handle, root_id)
        tagged = vox_tagged(handle) if tags else None
    finally:
        rb_writer.done_reading(handle, one_read)
    state = convergence.read(cfg)
    return nodes, state.tree(declared.tree.id), tagged


def read_placements(
    cfg: config.Config, declared: taxonomy.Taxonomy, *, one_read: rb_writer.SharedRead | None = None
) -> Placements:
    """The configured library's tree, read once, as what each track holds.

    NOT CACHED: a worker reads, writes memberships and may run again in the
    same process, and a cache would hand it the tree as it was. A tree that
    cannot be read answers ``UNREAD`` (see :func:`_read_tree`). ``one_read`` is
    :func:`read_holdings`'.
    """
    found = _read_tree(cfg, declared, tags=False, one_read=one_read)
    if found is None:
        return UNREAD
    return placements_from(declared, *found[:2])


def read_holdings(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    standing: bool | None = None,
    one_read: rb_writer.SharedRead | None = None,
) -> tuple[Placements, Vocals]:
    """What each track holds and what the vocal subs hold, from ONE read of the tree.

    Two reads would be two opens with a write possible between them, so the
    two answers could describe different trees. Not cached, as
    :func:`read_placements`. A tree that cannot be read answers unread for
    both and reads no tag. ``standing`` is what :func:`vocal_standing`
    answered for a caller that asked it first, else it is asked here; the tag
    is read only when it could file something, so with no vocal sub or no cut
    a tag row that cannot be read stops nothing. ``one_read`` is a read only
    report's one handle (U267).
    """
    if standing is None:
        standing = vocal_standing(cfg, declared)
    found = _read_tree(cfg, declared, tags=standing, one_read=one_read)
    if found is None:
        return UNREAD, NO_VOCALS
    nodes, record, tagged = found
    return placements_from(declared, nodes, record), vocals_from(
        declared, nodes, record, tagged, calibrated=standing
    )
