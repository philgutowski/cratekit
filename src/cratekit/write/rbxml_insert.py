"""Where a structural insert into the XML bridge lands, read but never written.

The byte writers stay in :mod:`cratekit.write.rbxml`, whose source the emitter
guard's conformance test derives the writers from. What is here only reads, and
nothing here takes a buffer it may change.
"""

from __future__ import annotations

import unicodedata
from typing import Sequence


def _playlist_root(content: bytes) -> NodeSpan | str:
    """The playlist root, or a warning naming the part of the document that is missing."""
    if playlists_span(content) is None:
        return f"{PLAYLISTS_SECTION} section not found"
    root = root_node(content)
    if root is None:
        return "ROOT node not found"
    return root


def _tree_node(content: bytes, tree: Tree | None) -> NodeSpan | str:
    """The node a tree scoped write happens inside, or a warning naming why not.

    With no tree named, it is INFERRED as the playlist root's one folder child,
    and inference refuses when there is more than one rather than guess.
    """
    root = _playlist_root(content)
    if isinstance(root, str):
        return root
    folders = [child for child in child_nodes(content, root) if child.node_type == FOLDER_TYPE]
    if tree is not None:
        # A tree is a DIRECT child of the root, so it is looked up among those: a
        # folder several levels down could share the name.
        node = next((child for child in folders if child.name == tree.display), None)
        if node is None:
            return f"folder not found: {tree.display}"
        return node
    if len(folders) == 1:
        return folders[0]
    return (
        f"the enclosing tree was not named and the playlist root holds "
        f"{len(folders)} folders, so it cannot be inferred"
    )


def _tree_scope(content: bytes, tree: Tree | None) -> tuple[int, int] | str:
    """The byte range a folder search is confined to, or a warning naming why not.

    A named tree's own node, so a folder of the same name under another tree is
    no candidate; with none named, the playlist section, never the whole
    document, because the collection precedes it and holds track names.
    """
    span = playlists_span(content)
    if span is None:
        return f"{PLAYLISTS_SECTION} section not found"
    if tree is None:
        return span
    node = _tree_node(content, tree)
    if isinstance(node, str):
        return node
    return node.body_start, node.body_end


def _folder_and_sub(
    content: bytes, genre_folder: str, sub_name: str, tree: Tree | None
) -> tuple[NodeSpan, NodeSpan | None] | str:
    """A genre folder in the tree's scope and its sub-playlist, or a warning.

    The sub is searched AFTER the folder's own open tag, or it would re-find the
    folder when the two share a name.
    """
    scope = _tree_scope(content, tree)
    if isinstance(scope, str):
        return scope
    folder = find_node(content, genre_folder, start=scope[0], end=scope[1], node_type=FOLDER_TYPE)
    if folder is None:
        return f"genre folder not found: {genre_folder}"
    sub = find_node(
        content, sub_name, start=folder.body_start, end=folder.body_end, node_type=PLAYLIST_TYPE
    )
    return folder, sub


def _type_name(node_type: str) -> str:
    """How a node type is spelled in a refusal, read through :func:`node_kind`.

    An unreadable kind is said to be one, never guessed as a playlist, because a
    person acts on the sentence.
    """
    kind = node_kind(node_type)
    return "node of an unreadable kind" if kind == KIND_UNREADABLE else kind


def _collision(name: str, found_type: str, wanted_type: str) -> str:
    """The refusal for a child of the right name and the wrong type."""
    return (
        f"a {_type_name(found_type)} named {name!r} is already there, and "
        f"this writer emits a {_type_name(wanted_type)}; replacing one with the "
        f"other would delete everything the existing node holds"
    )


def direct_child(
    content: bytes, parent: NodeSpan, name: str, node_type: str
) -> NodeSpan | str | None:
    """The direct child of ``parent`` named ``name``, of that TYPE, or a warning.

    Three answers: the node, None when no child carries the name, and a warning
    when one does at the other type, which a combined filter would report as
    "not found". A locate, so it takes no tree. PUBLIC so no caller re-filters
    :func:`child_nodes` itself.
    """
    for child in child_nodes(content, parent):
        if child.name != name:
            continue
        if child.node_type == node_type:
            return child
        return _collision(name, child.node_type, node_type)
    return None


def intake_names(content: bytes, *, tree: Tree | None = None) -> tuple[str, ...] | str:
    """Every name a node anywhere under the intake tree carries, or a warning naming why not.

    A LOCATE, NOT A WRITER, for a landing choosing a name INBOX does not hold
    yet (U113). Every descendant and not only the direct children, so a batch
    the rotation moved into ``Old`` still holds its name, and a folder's name
    counts as much as a playlist's.
    """
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    return tuple(node.name for _path, node in walk_nodes(content, parent))


def _lead_broken_playlist(
    name: str, track_ids: Sequence[object], indent: int, track_indent: int
) -> str:
    """A populated playlist node led by a CRLF and with no break after its close."""
    return (
        "\r\n"
        + playlist_open(name, len(track_ids), indent)
        + track_key_lines(track_ids, track_indent)
        + " " * indent
        + "</NODE>"
    )


def _catalog_block(
    folder_name: str, playlists: Sequence[tuple[str, Sequence[object]]], indent: int
) -> str:
    """One folder holding one ready-made playlist per pair, fully populated."""
    out = [folder_open(folder_name, len(playlists), indent)]
    for name, track_ids in playlists:
        out.append(_catalog_playlist(name, track_ids, indent + INDENT_STEP))
    out.append(node_close(indent))
    return "".join(out)


def _catalog_playlist(name: str, track_ids: Sequence[object], indent: int) -> str:
    """One populated playlist node at ``indent``, every line CRLF terminated."""
    ids = list(track_ids)
    return (
        playlist_open(name, len(ids), indent)
        + track_key_lines(ids, indent + INDENT_STEP)
        + node_close(indent)
    )


def _folded(name: str) -> str:
    """A node name in the form two sibling names are compared in.

    Canonical Unicode equivalence and nothing wider: one ``Café`` composed and one
    decomposed are one name drawn two ways. Case is NOT folded, since nothing
    recorded says rekordbox merges folders differing only by case (R-453).
    """
    return unicodedata.normalize("NFC", name)


def _sole_child(
    content: bytes, parent: NodeSpan, name: str, node_type: str
) -> NodeSpan | str | None:
    """The ONE direct child of ``parent`` named ``name``, of that type, or a warning.

    :func:`direct_child`'s answers plus a fourth, R-129: rekordbox merges an
    imported folder by name and appends every child, so two siblings of one name
    double on each import; two of a name refuse.
    """
    wanted = _folded(name)
    matches = [child for child in child_nodes(content, parent) if _folded(child.name) == wanted]
    if not matches:
        return None
    for child in matches:
        if child.node_type != node_type:
            return _collision(name, child.node_type, node_type)
    if len(matches) > 1:
        return (
            f"{len(matches)} {_type_name(node_type)}s named {name!r} already sit side "
            f"by side under {parent.name!r}; rekordbox merges an imported folder by "
            f"name and appends every child it carries, so this document would "
            f"duplicate them again on import. Remove the extra copies first"
        )
    return matches[0]


def _merged_pairs(
    playlists: Sequence[tuple[str, Sequence[object]]],
) -> list[tuple[str, list]]:
    """The caller's playlists with one entry per name and each id listed once.

    A caller naming one playlist twice is asking for one (R-129), so the two are
    joined in order under the first spelling rather than emitted as a sibling pair.
    """
    order: list[str] = []
    joined: dict[str, tuple[str, list]] = {}
    for name, track_ids in playlists:
        key = _folded(name)
        if key not in joined:
            joined[key] = (name, [])
            order.append(key)
        joined[key][1].extend(track_ids)
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]


def _starts_its_line(content: bytes, line_at: int, tag_at: int) -> bool:
    """Whether only indentation stands between a line's start and a tag on it.

    A merge writes whole lines at a line start, and a tag sharing its line with
    something else would put that write inside the something else.
    """
    return bytes(content[line_at:tag_at]).strip(b" ") == b""


def _first_child_offset(content: bytes, parent: NodeSpan) -> int | None:
    """Where a first child's own line begins, or None when there is no such place.

    After the break ending the open tag's line, so a block lands on its own line.
    None when that break is absent, rather than invent a line ending, and for a
    SELF CLOSED node, whose ``body_start`` lies past ``/>`` and outside the node.
    """
    if parent.self_closing:
        return None
    at = parent.body_start
    if bytes(content[at : at + len(CRLF)]) != CRLF:
        return None
    return at + len(CRLF)


def _break_before(content: bytes, line_at: int) -> int | None:
    """Where the CRLF ending the line before ``line_at`` begins, or None.

    None when that line ends in a bare LF, in nothing, or when there is no line
    before, for the reason :func:`_first_child_offset` gives.
    """
    at = line_at - len(CRLF)
    if bytes(content[at:line_at]) != CRLF:
        return None
    return at


def _absorb_lead_break(content: bytes, start: int) -> int:
    """Where a node's removal begins once the break ending the line before is taken.

    Every insert emits a lead break and then the node, so a delete takes the
    break too: ``start`` moved back over one directly preceding CRLF, else unchanged.
    """
    if bytes(content[start - len(CRLF) : start]) == CRLF:
        return start - len(CRLF)
    return start


# Bound last: rbxml imports this module's names at its own end, so either module
# may be imported first and each finds the other's names defined.
from cratekit.write.rbxml import (
    CRLF,
    FOLDER_TYPE,
    INDENT_STEP,
    KIND_UNREADABLE,
    PLAYLIST_TYPE,
    PLAYLISTS_SECTION,
    NodeSpan,
    Tree,
    child_nodes,
    dedupe_track_ids,
    find_node,
    folder_open,
    node_close,
    node_kind,
    playlist_open,
    playlists_span,
    root_node,
    track_key_lines,
    walk_nodes,
)
