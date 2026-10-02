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

THE VOCAL SUBS ARE READ HERE TOO (R-788), and so is the tag that says a track
belongs in one. Adoption files a vox tagged track under its bucket's vocal
sub, so the plan needs which tracks carry the tag and which vocal subs
already hold them, from the same open of the same database. The tag is the
My Tag value the vocals verb writes, found by the names that verb writes it
under, :data:`cratekit.write.metadata_cli.CATEGORY` and ``VALUE_VOX``, spelled
once there. Whether the library has a calibrated cut is read through that
module's one reader of the calibration, as every routing pass reads it.

Layer: modules. It reads configuration and the database and names no verb.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from cratekit.adopt.plan import NO_VOCALS, UNREAD, Placements, Vocals, vocal_sub
from cratekit.core import config, convergence, rb_writer, routing, taxonomy, tree_registry
from cratekit.write import metadata_cli, rebuild
from cratekit.write.routing_pass import destination

_ORIGIN = ("adopt", "placements")


def named_place(declared: taxonomy.Taxonomy, bucket_id: str, sub_id: str) -> tuple[str, str]:
    """The folder and playlist names one competing sub of a bucket answers to.

    A FORMER PLACE RESOLVES HERE AND NOT IN ``destination`` (R-797). That
    function is the one every writer that FILES a track asks, and it refuses an
    identifier no routing rule can return. A former place is such an
    identifier on purpose: it is read, and it is left, and nothing is ever
    filed into it. So the two callers that read or leave a place ask this, and
    a caller about to add a membership keeps asking ``destination`` and is
    refused. The folder is the declared bucket's own name as it is now, so a
    folder renamed in the taxonomy is still found.
    """
    former = routing.former_place(declared, bucket_id, sub_id)
    if former is None:
        return destination(declared, bucket_id, sub_id)
    return declared.bucket(former.bucket).display, former.display


def recorded_under(
    declared: taxonomy.Taxonomy, bucket_id: str, sub_id: str
) -> tuple[str, str]:
    """The bucket and sub identifiers a previous write recorded this place's node under.

    A former place was written while it was a sub of the bucket whose folder
    holds it, so its node is recorded under that bucket and that sub, and
    asking for it under the bucket that now declares it would find nothing
    and read a renamed playlist as absent.
    """
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

    A FORMER PLACE IS READ UNDER BOTH BUCKETS IT COMPETES IN (R-797), the one
    that declares it and the one whose folder holds it. A track in it holds
    that competing sub of each, found by the old folder's name and the old
    playlist's, or by the node recorded while the playlist was still a sub.

    A PLAYLIST REKORDBOX REMOVED IS NOT A PLACE EITHER (R-758). It shows no
    track, and the move finds the playlists it removes from among the live
    ones, so a sub held only through a removed playlist would be planned for a
    removal nothing could perform.
    """
    by_ids, by_display = _indexed(nodes)

    held: dict[str, dict[str, set[str]]] = {}
    unnamed: dict[str, dict[str, set[str]]] = {}
    doubled: dict[str, dict[str, set[str]]] = {}
    for bucket in declared.buckets:
        _kind, competing = routing.competing_subs(declared, bucket.id)
        for sub_id in sorted(competing):
            recorded = (
                None
                if record is None
                else record.node(*recorded_under(declared, bucket.id, sub_id))
            )
            answering, under_the_name, under_another = _answering(
                by_display, by_ids, named_place(declared, bucket.id, sub_id), recorded
            )
            for content_id in under_the_name | under_another:
                held.setdefault(bucket.id, {}).setdefault(content_id, set()).add(sub_id)
            for content_id in under_another:
                unnamed.setdefault(bucket.id, {}).setdefault(content_id, set()).add(sub_id)
            # THE MULTIPLICITY THE WALK COUNTED, kept per sub (R-781). A pair
            # two rows hold in one node is a double; a track in two nodes that
            # both answer for one sub is two playlists and is not.
            for content_id in {cid for node in answering for cid in node.doubled}:
                doubled.setdefault(bucket.id, {}).setdefault(content_id, set()).add(sub_id)

    return Placements(
        read=True, held=_frozen(held), unnamed=_frozen(unnamed), doubled=_frozen(doubled)
    )


def _indexed(
    nodes: Sequence[rebuild.TreeNode],
) -> tuple[
    dict[tuple[str, str], rebuild.TreeNode],
    dict[tuple[str, str], list[rebuild.TreeNode]],
]:
    """The live nodes of a tree, by their identifiers and by their names.

    A PLAYLIST REKORDBOX REMOVED IS IN NEITHER (R-758), for the reason
    :func:`placements_from` gives. ONE BODY for both readers, so which nodes
    count and how one is keyed is decided once.
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
    declared names, and the tracks held ONLY through the recorded node when
    that node no longer carries them. ONE BODY for the competing subs and the
    vocal subs, so the two readers cannot come to recognise a renamed
    playlist differently.
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

    ``tagged`` is what :func:`vox_tagged` answered: the tracks carrying the
    tag, or None when the library has no such tag at all. ``calibrated`` is
    whether the library has a fitted cut, and has no default, because the
    permissive answer would file a library nobody calibrated.

    ONLY A BUCKET THAT HAS THE VOCAL SUB IS READ, asked of
    :func:`cratekit.adopt.plan.vocal_sub`, which is the question the plan asks
    before it files. A playlist of the vocal name in a folder where that name
    is one of the bucket's own subs is that sub, and is not a vocal place.

    EVERY NODE THAT ANSWERS COUNTS AND WHICH NAME IT ANSWERS UNDER IS KEPT,
    for the two reasons :func:`placements_from` gives, through the one body
    both readers share. A removed playlist is not a place here either.

    A BUCKET WHOSE VOCAL SUB ANSWERS UNDER ANOTHER NAME ONLY IS NAMED, because
    the plan adds a track that is NOT in the sub, which the competing subs
    never do, and the writer would make the declared playlist to hold it.
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
        answering, under_the_name, under_another = _answering(
            by_display, by_ids, names, recorded
        )
        if under_the_name or under_another:
            filed[bucket.id] = frozenset(under_the_name | under_another)
        if under_another:
            unnamed[bucket.id] = frozenset(under_another)
        # A SUB THAT ANSWERS AND NOT BY ITS NAME. The writer would not find
        # it, so an addition here would make a second playlist beside it.
        if answering and not by_display.get(names):
            renamed.add(bucket.id)

    return Vocals(
        read=True,
        calibrated=calibrated,
        tag_found=tagged is not None,
        tagged=frozenset() if tagged is None else tagged,
        filed=filed,
        unnamed=unnamed,
        renamed=frozenset(renamed),
    )


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

    FOUND BY THE NAMES THE VOCALS VERB WRITES IT UNDER, a value of that name
    inside a category of that name. A value of the same name under some other
    category is another tag.

    THIS IS NOT THE WRITER'S OWN FIND, AND THE DIFFERENCE IS THE MARKER.
    :func:`cratekit.core.rb_writer.ensure_my_tag_value` takes the first
    category of the name and reads no soft delete marker, so over a category
    rekordbox removed it would write under a row nobody can see while this
    answers that the library has no such tag. That is the direction that
    files nothing, and the writer's half is recorded as a residual rather
    than copied here.

    NONE IS NOT THE EMPTY SET. A library with the tag and nothing carrying it
    answers the empty set, and the plan document tells the two apart.

    A ROW REKORDBOX REMOVED IS NOT A TAG (R-758). The binding hands a removed
    row back beside the live ones, and a removed association is a tag a
    person took off, so reading it as live would file a track the person had
    just said is not vocal. A row that cannot say whether it was removed
    refuses, through the one read of the marker.
    """
    categories = {
        str(tag.ID)
        for tag in db.get_my_tag(Name=metadata_cli.CATEGORY)
        if not _removed(tag, "My Tag")
    }
    values = [
        tag
        for tag in db.get_my_tag(Name=metadata_cli.VALUE_VOX)
        if str(getattr(tag, "ParentID", "") or "") in categories
        and not _removed(tag, "My Tag")
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


def _read_tree(
    cfg: config.Config, declared: taxonomy.Taxonomy, *, tags: bool
) -> tuple[Sequence[rebuild.TreeNode], convergence.TreeConvergence | None, frozenset[str] | None] | None:
    """The configured library's tree, read once. None when it cannot be read.

    Returns the tree's nodes, the node record a previous write left, and, when
    ``tags`` is asked for, what :func:`vox_tagged` answered over the same
    handle. ``tags`` is a parameter so a caller that asks nothing about
    vocals, the move verb through every one of its reads, opens no table it
    does not need and meets no refusal about one.

    THE TWO REFUSALS ``anchored_root`` RAISES ANSWER NONE and nothing else
    does. A database that is missing, a pin that fails, a convergence record
    that cannot be parsed: each is raised as it came, because each is a reason
    the plan cannot be trusted rather than a tree with nothing in it.

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
            return None
        nodes = rebuild.read_tree(handle, root_id)
        tagged = vox_tagged(handle) if tags else None
    finally:
        rb_writer.close_db(handle)
    state = convergence.read(cfg)
    return nodes, state.tree(declared.tree.id), tagged


def read_placements(cfg: config.Config, declared: taxonomy.Taxonomy) -> Placements:
    """The configured library's tree, read once, as what each track holds.

    NOT CACHED, unlike the collection. A worker reads the placements, writes
    memberships, and may be run again in the same process, and a cache would
    hand the second run the tree as it stood before the first one wrote.

    A TREE THAT CANNOT BE READ ANSWERS ``UNREAD``. See :func:`_read_tree` for
    which refusals that is and which are raised as they came.
    """
    found = _read_tree(cfg, declared, tags=False)
    if found is None:
        return UNREAD
    nodes, record, _tagged = found
    return placements_from(declared, nodes, record)


def read_holdings(
    cfg: config.Config, declared: taxonomy.Taxonomy
) -> tuple[Placements, Vocals]:
    """What each track holds and what the vocal subs hold, from ONE read of the tree.

    The adoption plan asks both, and two reads would be two opens of one
    database with a write possible between them, so the placements and the
    vocals could describe two different trees. NOT CACHED, for the reason
    :func:`read_placements` gives.

    A TREE THAT CANNOT BE READ ANSWERS UNREAD FOR BOTH, and the tag is then
    not read either: with no tree nothing can say which tracks are already
    filed, so the plan files none.

    WHETHER THE LIBRARY IS CALIBRATED IS READ HERE, through
    :func:`cratekit.write.metadata_cli.load_vocal_threshold`, the one reader
    every routing pass comes through. A calibration that cannot be read
    refuses as it does there. It is read before the database is opened, so
    that refusal costs nothing.
    """
    calibrated = metadata_cli.load_vocal_threshold(cfg) is not None
    found = _read_tree(cfg, declared, tags=True)
    if found is None:
        return UNREAD, NO_VOCALS
    nodes, record, tagged = found
    return placements_from(declared, nodes, record), vocals_from(
        declared, nodes, record, tagged, calibrated=calibrated
    )


__all__ = [
    "named_place",
    "placements_from",
    "read_holdings",
    "read_placements",
    "recorded_under",
    "vocals_from",
    "vox_tagged",
]
