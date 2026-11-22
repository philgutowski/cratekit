"""The rekordbox XML byte bridge: one set of locates, one set of writes, one guard.

rekordbox's export is a byte format with conventions a general serializer does
not keep, and every rule below was learned by breaking a real library.

THE FOUR BYTE RULES.

* **CRLF only, on the write side.** A bare LF rendered a playlist wrong and was
  invisible in any editor. Reads are forgiving, because real exports still carry
  lines an old splicer wrote, and a removal that missed them would make that
  corruption permanent.
* **Never round trip through a tree serializer.** ``lxml`` and the standard
  library collapse multi line attributes and rekordbox's display breaks. Reads
  may parse; writes are byte splices into the original document.
* **Anchors are scoped to the playlist section.** A ``Name=`` search from byte
  zero finds a COLLECTION track of that name first, and three old splicers
  silently dropped the routing write that way.
* **Patch the count AFTER the insert, never before.** Growing ``Entries="0"``
  to ``Entries="10"`` adds a byte, and a write at an offset taken before the
  patch corrupted the document tail.

THE LOCATES ARE HERE AND NOT AT THE CALL SITES, because a call site that can
locate a node can splice into it without calling a writer, and the guard in the
writers then covers nothing. INDENTATION IS DERIVED from depth by one function,
because pinned constants emitted another tree's nodes at an indent no locate
found.

THE INTAKE TREE'S SHAPE IS PINNED HERE (KTD14): one folder holding one playlist
per batch, whatever the genre tree looks like. The routing tree follows the
taxonomy, and one nesting deeper than this indentation encodes is refused by
name. How many levels a template may declare lives in ``taxonomy``, and a test
pins it equal to :data:`TREE_DEPTH`.

The read-only placement helpers the structural inserts use are in
:mod:`cratekit.write.rbxml_insert` and imported back; every byte writer is here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Iterable, Iterator, Sequence

from cratekit.core import taxonomy, tree_registry

CRLF = b"\r\n"

# ---------------------------------------------------------------------------
# Indentation, derived from depth
# ---------------------------------------------------------------------------

#: The indent of the playlist root's own open tag. Everything below is derived.
ROOT_INDENT = 4

#: Spaces rekordbox adds per level.
INDENT_STEP = 2

#: Levels below the playlist root the indentation encodes: a root child, a
#: folder inside it, and a sub-playlist inside that. A deeper declared tree is
#: refused by name (see :func:`assert_bridge_can_serve`).
TREE_DEPTH = 3

#: The intake tree's depth, PINNED HERE and never read from the taxonomy (KTD14).
INTAKE_DEPTH = 2


def indent_at(depth: int) -> int:
    """Spaces of indentation for a node at ``depth`` below the playlist root (0)."""
    if depth < 0:
        raise ValueError(f"depth must not be negative, got {depth}")
    return ROOT_INDENT + INDENT_STEP * depth


#: Where a sub-playlist's own tags sit, and where its track keys sit. Both stay
#: arguments on every writer that emits them, for a caller serving a shallower tree.
SUB_CLOSE_INDENT = indent_at(TREE_DEPTH)
TRACK_INDENT = indent_at(TREE_DEPTH + 1)

#: The two node types rekordbox writes. A folder carries ``Count`` and a
#: playlist ``Entries``, so confusing them patches the wrong attribute.
FOLDER_TYPE = "0"
PLAYLIST_TYPE = "1"

#: What a node's kind reads as, in THREE answers. :func:`node_at` reads an absent
#: or unreadable ``Type`` as the empty string, and "a playlist, or else a folder"
#: then calls every such node a folder: retyped playlists dropped to zero and an
#: intake report rendered a clean queue over a tree it could not read.
KIND_FOLDER = "folder"
KIND_PLAYLIST = "playlist"
KIND_UNREADABLE = "unreadable"


def node_kind(node_type: str) -> str:
    """Which of the three kinds a node's ``Type`` value spells.

    POSITIVE ON BOTH KNOWN VALUES, and unreadable on everything else: an absent
    attribute, an empty one, and an undefined value are one fact, an unknown kind,
    and a rule defaulting to one kind reports such a node as that kind.
    """
    if node_type == FOLDER_TYPE:
        return KIND_FOLDER
    if node_type == PLAYLIST_TYPE:
        return KIND_PLAYLIST
    return KIND_UNREADABLE

#: The document sections, spelled once for the locate scope and the message.
PLAYLISTS_SECTION = "PLAYLISTS"
COLLECTION_SECTION = "COLLECTION"

# Quote aware open tag matchers. A value may legally hold '>', and a track's open
# tag spans several lines, so neither is bounded by a search for the next '>'.
_NODE_OPEN = re.compile(rb'<NODE\b((?:[^>"]|"[^"]*")*)>')
_TRACK_OPEN = re.compile(rb'<TRACK\b((?:[^>"]|"[^"]*")*)>')
_ATTR_PAIR = re.compile(rb'\b([A-Za-z_][A-Za-z0-9_]*)="([^"]*)"')
_TRACK_KEY = re.compile(rb'<TRACK Key="(\d+)"/>')

_NODE_CLOSE = b"</NODE>"
_NODE_OPEN_LEAD = b"<NODE"


# ---------------------------------------------------------------------------
# Escaping. One escaper, and its exact inverse.
# ---------------------------------------------------------------------------


def xml_escape_attr(value: object) -> str:
    """Escape a value for a double quoted attribute the way rekordbox does.

    Ampersand, angle brackets and the double quote only. rekordbox leaves the
    apostrophe, so escaping it produces a marker no search will match.
    """
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def xml_unescape_attr(value: str) -> str:
    """The exact inverse, so a name read out of the document compares equal.

    The ampersand is undone LAST, or an escaped ampersand followed by ``lt;``
    would come back as a literal angle bracket.
    """
    return (
        value.replace("&quot;", '"')
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
    )


def name_marker(name: str) -> bytes:
    """The exact ``Name="..."`` bytes, built with the one escaper the emitters use."""
    return b'Name="' + xml_escape_attr(name).encode("utf-8") + b'"'


# ---------------------------------------------------------------------------
# Emitters. Exact bytes, including indent widths, because splices anchor on them.
# ---------------------------------------------------------------------------


def track_key_lines(track_ids: Iterable[object], indent: int = TRACK_INDENT) -> str:
    """One track key line per id, CRLF terminated, at ``indent`` spaces."""
    pad = " " * indent
    return "".join(f'{pad}<TRACK Key="{tid}"/>\r\n' for tid in track_ids)


def folder_open(name: str, count: int, indent: int) -> str:
    """A folder node's open tag, CRLF terminated."""
    return (
        f'{" " * indent}<NODE Name="{xml_escape_attr(name)}" '
        f'Type="{FOLDER_TYPE}" Count="{count}">\r\n'
    )


def playlist_open(name: str, entries: int, indent: int) -> str:
    """A playlist node's open tag, CRLF terminated."""
    return (
        f'{" " * indent}<NODE Name="{xml_escape_attr(name)}" '
        f'Type="{PLAYLIST_TYPE}" KeyType="0" Entries="{entries}">\r\n'
    )


def empty_playlist(name: str, indent: int) -> str:
    """A self closed, empty playlist node, with no trailing newline: callers
    splice it in front of an existing line break."""
    return (
        f'{" " * indent}<NODE Name="{xml_escape_attr(name)}" '
        f'Type="{PLAYLIST_TYPE}" KeyType="0" Entries="0"/>'
    )


def node_close(indent: int) -> str:
    """A node's closing tag, CRLF terminated."""
    return f'{" " * indent}</NODE>\r\n'


# ---------------------------------------------------------------------------
# The governed tree: the argument the guard is keyed on
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Tree:
    """The tree a byte write targets, and whether anything governs it.

    ``display`` is the name the document carries and the locates match; ``id`` is
    the taxonomy's stable identifier the registry is keyed on, never a display
    name (R19), so renaming a folder in rekordbox changes one and not the other.

    Both governance fields are present or both absent: either alone could not be
    checked, and the guard would pass by default. ``Tree(display=...)`` is an
    UNGOVERNED playlist, which anchors the write and bypasses the guard, because
    most playlists in a library are somebody's own and governed by nothing.
    """

    display: str
    id: str | None = None
    registry: tree_registry.Registry | None = None

    def __post_init__(self) -> None:
        if (self.id is None) != (self.registry is None):
            raise ValueError(
                "a governed tree carries both a stable identifier and the "
                "registry that governs it; with one and not the other the guard "
                "would either have nothing to look up or nothing to look it up in, "
                "and would pass by default"
            )

    @property
    def governed(self) -> bool:
        return self.id is not None and self.registry is not None


def tree_for(node: taxonomy.Node, registry: tree_registry.Registry) -> Tree:
    """A governed :class:`Tree` from a declared taxonomy node.

    The registry has NO default: a default would hand a caller who omitted it an
    ungoverned tree that passes the guard in silence. A caller with no records yet
    passes ``tree_registry.EMPTY``.
    """
    return Tree(display=node.display, id=node.id, registry=registry)


class TreeTooDeep(ValueError):
    """A declared tree the bridge's indentation cannot express, refused by name,
    rather than emitted at an indent no later locate finds again."""

    def __init__(self, *, tree_id: str, declared: int, supported: int) -> None:
        self.tree_id = tree_id
        self.declared = declared
        self.supported = supported
        super().__init__(
            f"the declared tree {tree_id!r} nests {declared} levels and the XML "
            f"bridge encodes {supported}: a root child, a folder, and a "
            f"sub-playlist. Writing it would put nodes at an indent no later "
            f"locate can find, so the sweep would report success and change "
            f"nothing (KTD14)"
        )


def assert_bridge_can_serve(declared: taxonomy.Taxonomy) -> None:
    """Refuse a taxonomy whose tree is deeper than this indentation encodes.

    Only DEEPER, the case that would emit at an indent no locate finds; a
    shallower tree's indent is derived and findable, and what a template may
    declare is the taxonomy loader's rule. This is the second guard of two,
    kept because a ``Taxonomy`` can be built without the loader.
    """
    if declared.tree_depth > TREE_DEPTH:
        raise TreeTooDeep(
            tree_id=declared.tree.id,
            declared=declared.tree_depth,
            supported=TREE_DEPTH,
        )


def routing_tree(declared: taxonomy.Taxonomy, registry: tree_registry.Registry) -> Tree:
    """The declared routing tree, refused if the bridge cannot express its shape."""
    assert_bridge_can_serve(declared)
    return tree_for(declared.tree, registry)


def intake_tree(declared: taxonomy.Taxonomy, registry: tree_registry.Registry) -> Tree:
    """The intake tree, at the pinned shallow shape (KTD14), never depth checked,
    so a taxonomy the bridge cannot route still has a working intake tree."""
    return tree_for(declared.intake, registry)


def _refuse_wrong_medium(tree: Tree | None) -> None:
    """The emitter guard. Every byte writer below calls it first, except the ones
    ``UNGOVERNED_WRITERS`` names and says why.

    A governed tree native to the database is refused by name; a governed tree
    still on the bridge proceeds; an ungoverned tree is not this guard's at all,
    because a guard that fires on correct code gets suppressed (P7).
    """
    if tree is None or tree.id is None or tree.registry is None:
        return
    tree_registry.refuse_bridge_write(tree.id, tree.registry)


# ---------------------------------------------------------------------------
# Locates. One set, covering every shape the call sites need.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class NodeSpan:
    """One located node, bounded exactly.

    ``close_start`` is -1 for a self closed node: a childless folder has no
    matching close, and a walk assuming one marches on to a SIBLING's close and
    deletes everything in between.
    """

    name: str
    node_type: str
    depth: int
    line_start: int
    tag_start: int
    tag_end: int
    self_closing: bool
    close_start: int
    close_end: int

    @property
    def body_start(self) -> int:
        """The first byte after the open tag."""
        return self.tag_end + 1

    @property
    def indent(self) -> int:
        return self.tag_start - self.line_start

    @property
    def body_end(self) -> int:
        """The last byte of the node's children, or the end of a self closed tag."""
        return self.close_end if self.self_closing else self.close_start


@dataclass(frozen=True, slots=True)
class TrackSpan:
    """One located collection track element, bounded by its real close.

    Self closed in a minimal export, multi line with a close tag in a real one.
    Bounded by the next ``/>``, a patch lands in the track's own tempo child.
    """

    track_id: str
    line_start: int
    tag_start: int
    tag_end: int
    self_closing: bool
    end: int


def line_start(content: bytes, pos: int) -> int:
    """The offset of the start of the line holding ``pos``."""
    return content.rfind(b"\n", 0, pos) + 1


def section_span(content: bytes, tag: str) -> tuple[int, int] | None:
    """The offsets of a top level section's ``<`` and its closing tag's ``<``.

    None when either end is missing, never a -1 for slice arithmetic.
    """
    opening = content.find(f"<{tag}".encode("utf-8"))
    if opening == -1:
        return None
    closing = content.find(f"</{tag}>".encode("utf-8"), opening)
    if closing == -1:
        return None
    return opening, closing


def playlists_span(content: bytes) -> tuple[int, int] | None:
    """The playlist section's bounds. Every name search starts inside this."""
    return section_span(content, PLAYLISTS_SECTION)


def playlists_start(content: bytes) -> int:
    """The offset of the playlist section's open tag, or -1, without parsing the tree."""
    return content.find(f"<{PLAYLISTS_SECTION}>".encode("utf-8"))


def collection_span(content: bytes) -> tuple[int, int] | None:
    """The collection section's bounds, for track element locates."""
    return section_span(content, COLLECTION_SECTION)


def attributes(content: bytes, node: NodeSpan | TrackSpan) -> dict[str, str]:
    """Every attribute on a located tag, unescaped, ORDER INDEPENDENT: two old
    writers matched one node with the attributes in opposite orders."""
    raw = bytes(content[node.tag_start : node.tag_end])
    return {
        key.decode("utf-8"): xml_unescape_attr(value.decode("utf-8"))
        for key, value in _ATTR_PAIR.findall(raw)
    }


@lru_cache(maxsize=64)
def _attr_pattern(name: str) -> re.Pattern[bytes]:
    return re.compile(rb'\b' + re.escape(name.encode("utf-8")) + rb'="([^"]*)"')


def attribute_span(content: bytes, name: str, *, start: int, end: int) -> tuple[int, int] | None:
    """Absolute bounds of one attribute's VALUE inside a located tag, so digits
    can be replaced in place with offsets that survive an insert elsewhere."""
    match = _attr_pattern(name).search(bytes(content[start:end]))
    if match is None:
        return None
    return start + match.start(1), start + match.end(1)


def _read_int(content: bytes, span: tuple[int, int]) -> int:
    """The integer currently written in a located attribute value span."""
    return int(bytes(content[span[0] : span[1]]).decode("utf-8"))


def _open_tag_bounds(content: bytes, opening: int) -> tuple[int, bool] | None:
    """One open tag's end offset and whether it closes itself, quote aware.

    Through :func:`node_at`'s own matcher: a walk bounding a tag by the next '>'
    stopped inside a display name and handed back an ancestor's close. None when
    the bytes are not a complete NODE open tag, so truncation refuses.
    """
    match = _NODE_OPEN.match(content, opening)
    if match is None:
        return None
    return match.end(), match.group(1).endswith(b"/")


def _node_tokens(content: bytes, cursor: int, limit: int) -> Iterator[tuple[int, int]]:
    """Each NODE token in ``[cursor, limit)``, as its depth change and its offset.

    An open tag is +1, a close tag -1 and a self closed node 0, because it opens
    and closes itself. PAIRS, never a count of close tags (which puts the first
    close on the wrong node) or self closing syntax alone (which puts every empty
    sibling a level too deep). Ends at the last token or a truncated open tag.
    """
    while True:
        opening = content.find(_NODE_OPEN_LEAD, cursor, limit)
        closing = content.find(_NODE_CLOSE, cursor, limit)
        if opening != -1 and (closing == -1 or opening < closing):
            bounds = _open_tag_bounds(content, opening)
            if bounds is None:
                return
            cursor, self_closing = bounds
            yield (0 if self_closing else 1), opening
        elif closing != -1:
            cursor = closing + len(_NODE_CLOSE)
            yield -1, closing
        else:
            return


def matching_close(content: bytes, tag_end: int) -> int:
    """The offset of the close tag matching an open tag that ends at ``tag_end``.

    -1 when the node is unterminated, never a guess.
    """
    depth = 1
    for step, at in _node_tokens(content, tag_end + 1, len(content)):
        depth += step
        if depth == 0:
            return at
    return -1


def _open_tag(
    pattern: re.Pattern[bytes], content: bytes, tag_start: int
) -> tuple[re.Match[bytes], dict[bytes, bytes], bool] | None:
    """The open tag ``pattern`` matches at ``tag_start``: the match, its raw
    attributes, and whether it closes itself."""
    match = pattern.match(content, tag_start)
    if match is None:
        return None
    raw_attrs = match.group(1)
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), raw_attrs.endswith(b"/")


def node_at(content: bytes, tag_start: int, *, depth: int = 0) -> NodeSpan | None:
    """Bound the node whose open tag begins at ``tag_start``.

    None rather than a partial span when the tag cannot be parsed or the node is
    unterminated: a slice with a -1 in it deletes to the end of the document.
    """
    tag = _open_tag(_NODE_OPEN, content, tag_start)
    if tag is None:
        return None
    match, found, self_closing = tag
    tag_end = match.end() - 1
    name = found.get(b"Name")
    node_type = found.get(b"Type")
    if self_closing:
        close_start, close_end = -1, match.end()
    else:
        close_start = matching_close(content, tag_end)
        if close_start == -1:
            return None
        close_end = close_start + len(_NODE_CLOSE)
    return NodeSpan(
        name="" if name is None else xml_unescape_attr(name.decode("utf-8")),
        node_type="" if node_type is None else node_type.decode("utf-8"),
        depth=depth,
        line_start=line_start(content, tag_start),
        tag_start=tag_start,
        tag_end=tag_end,
        self_closing=self_closing,
        close_start=close_start,
        close_end=close_end,
    )


def depth_of(content: bytes, tag_start: int) -> int:
    """How many nodes enclose the node whose open tag begins at ``tag_start``.

    Counted by node PAIRS from the playlist section, never from the indent, which
    is formatting and misread every tree whose levels were not two spaces apart.
    """
    span = playlists_span(content)
    if span is None:
        return 0
    return sum(step for step, _at in _node_tokens(content, span[0], tag_start))


def root_node(content: bytes) -> NodeSpan | None:
    """The playlist root: the first node inside the playlist section, found by
    position so an export spelling it differently fails at the locate."""
    span = playlists_span(content)
    if span is None:
        return None
    start, end = span
    at = content.find(_NODE_OPEN_LEAD, start, end)
    if at == -1:
        return None
    return node_at(content, at, depth=0)


def child_nodes(content: bytes, parent: NodeSpan) -> tuple[NodeSpan, ...]:
    """The DIRECT children of a located node, in document order.

    A byte search inside the range finds grandchildren too, and a writer treating
    one as a child replaces a node several levels down.
    """
    if parent.self_closing:
        return ()
    out: list[NodeSpan] = []
    cursor = parent.body_start
    while True:
        at = content.find(_NODE_OPEN_LEAD, cursor, parent.close_start)
        if at == -1:
            return tuple(out)
        child = node_at(content, at, depth=parent.depth + 1)
        if child is None:
            return tuple(out)
        out.append(child)
        cursor = child.close_end


def walk_nodes(
    content: bytes, parent: NodeSpan, *, path: tuple[str, ...] = ()
) -> Iterator[tuple[tuple[str, ...], NodeSpan]]:
    """Every descendant of ``parent`` in document order, with its display path.

    The root's own name is not in the path: it is a constant of the format.
    """
    for child in child_nodes(content, parent):
        here = (*path, child.name)
        yield here, child
        yield from walk_nodes(content, child, path=here)


def find_node(
    content: bytes,
    name: str,
    *,
    start: int,
    end: int | None = None,
    node_type: str | None = None,
) -> NodeSpan | None:
    """The first node named ``name`` in ``[start, end)``, optionally by type.

    ``start`` has NO default: every historical mis-anchor in this format began at
    byte zero. The type filter is the second defence, because a folder and its
    own sub-playlist share names and a splice matching the folder patched
    ``Count`` and dropped the track.
    """
    limit = len(content) if end is None or end < 0 else end
    marker = name_marker(name)
    cursor = start
    while True:
        at = content.find(marker, cursor, limit)
        if at == -1:
            return None
        tag_start = content.rfind(_NODE_OPEN_LEAD, start, at)
        if tag_start != -1:
            node = node_at(content, tag_start, depth=depth_of(content, tag_start))
            # The marker has to sit inside THIS open tag, or it belongs to
            # something else and the enclosing node is a coincidence.
            if (
                node is not None
                and node.tag_start <= at < node.tag_end
                and (node_type is None or node.node_type == node_type)
            ):
                return node
        cursor = at + 1


def track_keys(content: bytes, node: NodeSpan) -> tuple[str, ...]:
    """The track ids a playlist node currently holds, in document order."""
    if node.self_closing:
        return ()
    return tuple(
        value.decode("utf-8")
        for value in _TRACK_KEY.findall(bytes(content[node.body_start : node.close_start]))
    )


def track_key_line(
    content: bytes, node: NodeSpan, track_id: object, *, indent: int = TRACK_INDENT
) -> tuple[int, int] | None:
    """The bounds of one track key LINE inside a playlist, terminator included.

    The one place a bare LF terminator is tolerated, so a removal finds lines an
    old splicer wrote. Writes remain strictly CRLF.
    """
    if node.self_closing:
        return None
    pad = " " * indent
    body = f'{pad}<TRACK Key="{track_id}"/>'.encode("utf-8")
    for terminator in (CRLF, b"\n"):
        needle = body + terminator
        at = content.find(needle, node.body_start, node.close_start)
        if at != -1:
            return at, at + len(needle)
    return None


def find_collection_track(
    content: bytes, track_id: object, *, start: int | None = None, end: int | None = None
) -> TrackSpan | None:
    """One collection track element, matched on its id EXACTLY.

    The marker carries the closing quote, so an id of 42 cannot match 421 and
    rate, retag or relocate the wrong track.
    """
    span = collection_span(content)
    low = start if start is not None else (span[0] if span else 0)
    high = end if end is not None else (span[1] if span else len(content))
    marker = b'TrackID="' + str(track_id).encode("utf-8") + b'"'
    at = content.find(marker, low, high)
    if at == -1:
        return None
    tag_start = content.rfind(b"<TRACK", low, at)
    if tag_start == -1:
        return None
    return _track_at(content, tag_start)


def collection_tracks(content: bytes) -> tuple[TrackSpan, ...]:
    """Every collection track element, in document order, in ONE pass: locating
    each separately is quadratic, which is where the old fixed size window came
    from, and that window let a patch reach into the following element."""
    span = collection_span(content)
    if span is None:
        return ()
    start, end = span
    out: list[TrackSpan] = []
    cursor = start
    while True:
        at = content.find(b"<TRACK", cursor, end)
        if at == -1:
            return tuple(out)
        track = _track_at(content, at)
        if track is None:
            return tuple(out)
        if track.track_id:
            out.append(track)
        cursor = track.end


def _track_at(content: bytes, tag_start: int) -> TrackSpan | None:
    tag = _open_tag(_TRACK_OPEN, content, tag_start)
    if tag is None:
        return None
    match, found, self_closing = tag
    track_id = found.get(b"TrackID", b"").decode("utf-8")
    if self_closing:
        end = match.end()
    else:
        closing = content.find(b"</TRACK>", match.end())
        if closing == -1:
            return None
        end = closing + len(b"</TRACK>")
    return TrackSpan(
        track_id=track_id,
        line_start=line_start(content, tag_start),
        tag_start=tag_start,
        tag_end=match.end() - 1,
        self_closing=self_closing,
        end=end,
    )


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def dedupe_track_ids(
    track_ids: Iterable[object],
    existing_keys: Iterable[object] = (),
    norm_by_tid: dict | None = None,
) -> list:
    """First occurrence dedup, by exact id and then by normalized name, because a
    re download, another release or a re import gives one recording two ids."""
    by_tid = norm_by_tid or {}
    seen_tid = {str(key) for key in existing_keys}
    seen_norm = {by_tid[key] for key in seen_tid if by_tid.get(key)}
    out: list = []
    for tid in track_ids:
        text = str(tid)
        if text in seen_tid:
            continue
        norm = by_tid.get(text)
        if norm and norm in seen_norm:
            continue
        out.append(tid)
        seen_tid.add(text)
        if norm:
            seen_norm.add(norm)
    return out


# ---------------------------------------------------------------------------
# Byte writers. Every one calls the guard first, except those UNGOVERNED_WRITERS
# names, and that set is checked against this module rather than trusted.
# ---------------------------------------------------------------------------

#: Byte writers that target no tree and take no ``tree`` argument. Declared, and
#: tests/test_tree_registry.py derives every byte writer from this module and
#: asserts this set plus the guarded ones covers it EXACTLY (P3). None of the
#: three writes membership INSIDE A TREE, which is what a cutover moves:
#:
#: * the rating patch writes one collection attribute, which no cutover moves;
#: * the attribute patcher replaces a value in a tag the caller located: a
#:   collection attribute, or a recount while ASSEMBLING a new document. Using it
#:   to change a live tree's entry count would route around the guard, a
#:   residual the call sites owe by naming the tree at the writers;
#: * the root playlist writer emits a DIRECT child of the playlist root, where a
#:   tree is a folder, never a playlist, and no record could govern it. A tree
#:   argument would arm the guard on a subject the write does not touch, and a
#:   guard firing on correct code gets switched off (P7). It still makes the type
#:   check, so a root playlist named after a tree refuses instead of replacing it.
UNGOVERNED_WRITERS = frozenset(
    {"apply_rating_changes", "patch_attribute", "insert_root_playlist"}
)


@dataclass
class SpliceResult:
    """What a splice did, or the reason it did nothing.

    A missing node is a warning, so one absent folder does not abandon forty
    other writes; a refusal by the guard IS an exception, because it means the
    wrong medium and continuing would corrupt a library.
    """

    inserted: int = 0
    entries_after: int | None = None
    created: bool = False
    warning: str | None = None


#: Attribute names that carry a beat grid, compared lowercase so case cannot
#: reach the grid. Held here as well as in the source scan, which reads string
#: constants and cannot see a name arriving as an argument. R17 is absolute both
#: ways: this package never creates a grid, nor destroys rekordbox's.
_GRID_ATTRIBUTES = frozenset({"averagebpm", "bpm", "inizio", "metro", "battito"})


def patch_attribute(
    content: bytearray, name: str, value: object, *, start: int, end: int
) -> bool:
    """Replace one attribute's value inside an ALREADY LOCATED tag.

    Bounded by the tag, never a fixed window, which patched the next element's
    attribute and landed a rating on a track nobody touched. Strings go through
    the one escaper; numbers are written as digits.

    A tempo bearing attribute is REFUSED: a track's average tempo seeds
    rekordbox's analysis on import, and a range bounding a whole tempo element
    reaches its attributes. Both are grid writes, and a grid is rekordbox's (R17).
    """
    if name.lower() in _GRID_ATTRIBUTES:
        raise ValueError(
            f"refusing to patch the attribute {name!r}: it carries tempo, and a "
            f"tempo value written into an export is a beat grid by another route. "
            f"rekordbox authors grids from the audio and this package never "
            f"creates one, nor overwrites the one a user's analysis produced (R17)"
        )
    span = attribute_span(content, name, start=start, end=end)
    if span is None:
        return False
    text = xml_escape_attr(value) if isinstance(value, str) else str(value)
    content[span[0] : span[1]] = text.encode("utf-8")
    return True


def splice_into_subplaylist(
    content: bytearray,
    genre_folder: str,
    sub_name: str,
    track_ids: Sequence[object],
    *,
    tree: Tree | None = None,
    norm_by_tid: dict | None = None,
    create_missing: bool = False,
    track_indent: int = TRACK_INDENT,
    close_indent: int = SUB_CLOSE_INDENT,
) -> SpliceResult:
    """Insert track keys into a sub-playlist and bump its entry count.

    Dedup on BOTH paths, by id or normalized name, against the sub and within the
    batch. With ``create_missing`` an absent sub is created as the folder's last
    child.

    A FOLDER's ``Count`` is advisory, since rekordbox recounts children on import,
    and this splice leaves it alone because a golden pins its bytes; the writers
    adding or removing a child keep it accurate. A PLAYLIST's ``Entries`` is
    always patched, because rekordbox trusts it over the children it sees.

    A failure writes NOTHING: a partial splice into this format is a corrupt file.
    """
    _refuse_wrong_medium(tree)
    if not track_ids:
        return SpliceResult()

    located = _folder_and_sub(content, genre_folder, sub_name, tree)
    if isinstance(located, str):
        return SpliceResult(warning=located)
    folder, sub = located

    if sub is None:
        if not create_missing:
            return SpliceResult(warning=f"sub-playlist not found: {genre_folder}/{sub_name}")
        if folder.self_closing:
            return SpliceResult(
                warning=f"cannot find close tag for genre folder: {genre_folder}"
            )
        # Deduplicated against nothing, or the run that creates the sub keeps a
        # recording the batch names twice and the run that finds it keeps one.
        # THE BREAK BEFORE THE CLOSE LINE HAS TO BE A CRLF, or the node splits a
        # ``/>`` in two and writes a file no parser reads, as a success (U91).
        # Refused rather than written around, which would invent a line ending.
        at = _break_before(content, line_start(content, folder.close_start))
        if at is None:
            return SpliceResult(
                warning=f"the line before the close tag of genre folder {genre_folder} "
                f"does not end in CRLF, so {sub_name} cannot be created there "
                f"without inventing a line ending"
            )
        fresh = dedupe_track_ids(track_ids, (), norm_by_tid)
        new_node = _lead_broken_playlist(sub_name, fresh, close_indent, track_indent)
        content[at:at] = bytearray(new_node.encode("utf-8"))
        return SpliceResult(inserted=len(fresh), entries_after=len(fresh), created=True)

    existing_keys = track_keys(content, sub)
    filtered = dedupe_track_ids(track_ids, existing_keys, norm_by_tid)
    if not filtered:
        return SpliceResult()

    entries = attribute_span(content, "Entries", start=sub.tag_start, end=sub.tag_end)
    if entries is None:
        return SpliceResult(warning=f"Entries attr not found for {genre_folder}/{sub_name}")
    new_entries = _read_int(content, entries) + len(filtered)

    # Insert FIRST, then patch the count: the insert is past the open tag, so the
    # count's offsets stay valid.
    new_lines = track_key_lines(filtered, track_indent).encode("utf-8")
    if sub.self_closing:
        close_marker = b" " * close_indent + _NODE_CLOSE
        content[sub.tag_end - 1 : sub.tag_end + 1] = bytearray(
            b">" + CRLF + new_lines + close_marker
        )
    else:
        at = line_start(content, sub.close_start)
        content[at:at] = bytearray(new_lines)
    content[entries[0] : entries[1]] = str(new_entries).encode("utf-8")
    return SpliceResult(inserted=len(filtered), entries_after=new_entries)


def remove_tracks_from_subplaylist(
    content: bytearray,
    genre_folder: str,
    sub_name: str,
    track_ids: Sequence[object],
    *,
    tree: Tree | None = None,
    track_indent: int = TRACK_INDENT,
) -> tuple[int, str | None]:
    """Delete track key lines from a sub-playlist and decrement its entry count.

    Returns how many were removed and a warning or None. The count moves by what
    was removed, not what was asked for. No close indent: removal re-bounds the
    node from the bytes it finds, so that knob would do nothing.
    """
    _refuse_wrong_medium(tree)
    if not track_ids:
        return 0, None

    located = _folder_and_sub(content, genre_folder, sub_name, tree)
    if isinstance(located, str):
        return 0, located
    _folder, sub = located
    if sub is None:
        return 0, f"sub-playlist not found: {genre_folder}/{sub_name}"
    if sub.self_closing:
        return 0, None  # an empty sub, nothing to remove

    entries = attribute_span(content, "Entries", start=sub.tag_start, end=sub.tag_end)
    removed = 0
    close_start = sub.close_start
    for tid in track_ids:
        # Re-bound the node on each pass: every deletion moves its close tag.
        current = replace(
            sub, close_start=close_start, close_end=close_start + len(_NODE_CLOSE)
        )
        line = track_key_line(content, current, tid, indent=track_indent)
        if line is None:
            continue
        del content[line[0] : line[1]]
        close_start -= line[1] - line[0]
        removed += 1

    if removed and entries is not None:
        new_entries = max(0, _read_int(content, entries) - removed)
        content[entries[0] : entries[1]] = str(new_entries).encode("utf-8")
    return removed, None


def apply_rating_changes(rating_plan: dict, content: bytearray) -> int:
    """Patch the rating attribute in place on collection track elements.

    Ids sit on collection tracks only, so no playlist scoping. Every element is
    located in ONE pass and patched from the end backwards, so a value growing a
    digit cannot move the offsets still to come. Ungoverned: see
    ``UNGOVERNED_WRITERS``.
    """
    if not rating_plan:
        return 0
    index = {track.track_id: track for track in collection_tracks(content)}
    targets = [
        (index[str(track_id)], rating)
        for track_id, rating in rating_plan.items()
        if str(track_id) in index
    ]
    updated = 0
    for track, rating in sorted(targets, key=lambda pair: pair[0].tag_start, reverse=True):
        if patch_attribute(
            content, "Rating", rating, start=track.tag_start, end=track.tag_end
        ):
            updated += 1
    return updated


def _insert_last(content: bytearray, parent: NodeSpan, block: str) -> None:
    """Splice a lead broken ``block`` in as ``parent``'s last child, just before
    the break that ends its last line."""
    at = line_start(content, parent.close_start) - len(CRLF)
    content[at:at] = bytearray(block.encode("utf-8"))


def insert_root_playlist(
    name: str,
    track_ids: Sequence[object],
    content: bytearray,
) -> str | None:
    """Append a playlist as the last child of the playlist root, replacing any
    existing playlist of the same name.

    Idempotent, so "run it again" stays the recovery procedure. Only a DIRECT
    child is replaced: the version this ports searched the whole subtree and
    deleted a nested namesake across a range that was not its own. Takes no tree,
    by decision: see ``UNGOVERNED_WRITERS``.
    """
    root = _playlist_root(content)
    if isinstance(root, str):
        return root

    existing = direct_child(content, root, name, PLAYLIST_TYPE)
    if isinstance(existing, str):
        return existing
    if existing is not None:
        del content[_absorb_lead_break(content, existing.line_start) : existing.close_end]
        root = root_node(content)
        if root is None:  # pragma: no cover - the delete cannot remove the root
            return "ROOT node not found"

    _insert_last(content, root, _lead_broken_playlist(name, track_ids, indent_at(1), indent_at(2)))
    if existing is None:
        _bump_count(content, root, +1)
    return None


def insert_genre_folder(
    content: bytearray,
    folder_name: str,
    sub_names: Sequence[str],
    *,
    tree: Tree | None = None,
) -> str | None:
    """Insert a folder as the last child of a tree, with one empty sub per name.

    Indents derived from the tree's depth, the tree's count bumped by one.
    Idempotent: an existing child of that name is left alone.
    """
    _refuse_wrong_medium(tree)
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    existing = direct_child(content, parent, folder_name, FOLDER_TYPE)
    if isinstance(existing, str):
        return existing
    if existing is not None:
        return None
    if parent.self_closing:
        return f"cannot find close tag for folder: {parent.name}"

    block = (
        "\r\n"
        + folder_open(folder_name, len(sub_names), indent_at(parent.depth + 1))
        + "".join(
            empty_playlist(sub, indent_at(parent.depth + 2)) + "\r\n" for sub in sub_names
        )
        + " " * indent_at(parent.depth + 1)
        + "</NODE>"
    )
    # Insert FIRST, then bump the count, which sits before the insertion point.
    _insert_last(content, parent, block)
    _bump_count(content, parent, +1)
    return None


def remove_folder_node(
    content: bytearray,
    folder_name: str,
    *,
    tree: Tree | None = None,
) -> str | None:
    """Remove a named folder that is a direct child of a tree, and its lead break.

    Bounded by a depth walk over node PAIRS, so a self closed childless folder is
    removed as exactly its own tag rather than up to a SIBLING's close. An absent
    name is a warning and a no-op.
    """
    _refuse_wrong_medium(tree)
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    target = direct_child(content, parent, folder_name, FOLDER_TYPE)
    if isinstance(target, str):
        return target
    if target is None:
        return f"folder node not found: {folder_name}"

    del content[_absorb_lead_break(content, target.line_start) : target.close_end]
    _bump_count(content, parent, -1)
    return None


def insert_intake_playlist(
    content: bytearray,
    name: str,
    track_ids: Sequence[object],
    *,
    tree: Tree | None = None,
) -> str | None:
    """Insert a playlist as the last child of the intake tree, at the pinned shape.

    :data:`INTAKE_DEPTH`, never the tree's own depth (KTD14). Idempotent: an
    existing playlist of that name is replaced, and the count bumped only when a
    node is added.
    """
    _refuse_wrong_medium(tree)
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    if parent.self_closing:
        return f"cannot find close tag for folder: {parent.name}"

    replaced = False
    existing = direct_child(content, parent, name, PLAYLIST_TYPE)
    if isinstance(existing, str):
        return existing
    if existing is not None:
        del content[_absorb_lead_break(content, existing.line_start) : existing.close_end]
        replaced = True
        refreshed = _tree_node(content, tree)
        if isinstance(refreshed, str):  # pragma: no cover - the tree cannot vanish
            return refreshed
        parent = refreshed

    node = _lead_broken_playlist(name, track_ids, indent_at(INTAKE_DEPTH), indent_at(INTAKE_DEPTH + 1))
    _insert_last(content, parent, node)
    if not replaced:
        _bump_count(content, parent, +1)
    return None


def insert_empty_subplaylist(
    content: bytearray,
    folder_name: str,
    sub_name: str,
    *,
    tree: Tree | None = None,
    close_indent: int | None = None,
) -> SpliceResult:
    """Insert an EMPTY sub-playlist as the last child of a folder inside a tree.

    rekordbox has no import path that creates an empty playlist, and
    :func:`splice_into_subplaylist` returns early with no keys, so a routing sub
    no track has reached yet is made here. Idempotent: a folder already holding
    the sub is left byte identical. The indent derives from the folder's depth;
    ``close_indent`` overrides it for a document at another shape.
    """
    _refuse_wrong_medium(tree)
    # A DIRECT child of the tree, never a body wide search: the caller loops over
    # the tree's direct folders by name, and a body search finds a namesake
    # nested in an earlier sibling first, so the write would land elsewhere.
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return SpliceResult(warning=parent)

    folder = direct_child(content, parent, folder_name, FOLDER_TYPE)
    if isinstance(folder, str):
        return SpliceResult(warning=folder)
    if folder is None:
        return SpliceResult(warning=f"genre folder not found: {folder_name}")

    existing = direct_child(content, folder, sub_name, PLAYLIST_TYPE)
    if isinstance(existing, str):
        return SpliceResult(warning=existing)
    if existing is not None:
        return SpliceResult()
    if folder.self_closing:
        return SpliceResult(warning=f"cannot find close tag for genre folder: {folder_name}")

    indent = indent_at(folder.depth + 1) if close_indent is None else close_indent
    _insert_last(content, folder, "\r\n" + empty_playlist(sub_name, indent))
    _bump_count(content, folder, +1)
    return SpliceResult(created=True, entries_after=0)


def insert_catalog_folder(
    content: bytearray,
    folder_name: str,
    playlists: Sequence[tuple[str, Sequence[object]]],
    *,
    tree: Tree | None = None,
) -> str | None:
    """Insert a whole populated folder into a tree, creating the tree when absent.

    The one writer that emits a subtree: a label's releases, a playlist per year.

    * **A new folder goes in FIRST, not last**, unlike every other insert: the
      caller orders playlists newest first, and a golden pins the layout.
    * **An existing folder of that name is MERGED INTO** (R-129). A held
      playlist gains only the ids it lacks; a missing one goes before the first
      held playlist whose name sorts below its own, newest first for years. So a
      second identical write changes no byte, and the old always inserting
      system duplicated the whole label.
    * **Two siblings of one name refuse** at each level written: the tree, the
      folder and each playlist. See ``_sole_child``.
    * **The tree's own node is created when missing**, as the root's first child,
      because a catalog tree is created by its first write, not by setup.

    Names compare through ``_folded``; ids are deduplicated within each playlist
    and against its members. Returns a warning or None. A failure writes nothing:
    every edit is made on a copy that replaces the document only at the end.
    """
    _refuse_wrong_medium(tree)
    work = bytearray(content)
    warning = _write_catalog(work, folder_name, _merged_pairs(playlists), tree)
    if warning is None:
        content[:] = work
    return warning


def _write_catalog(
    content: bytearray,
    folder_name: str,
    pairs: Sequence[tuple[str, Sequence[object]]],
    tree: Tree | None,
) -> str | None:
    root = _playlist_root(content)
    if isinstance(root, str):
        return root

    # With no tree named the enclosing node is inferred and inference refuses
    # rather than guesses. With one named, an absent node is created here.
    if tree is None:
        inferred = _tree_node(content, None)
        if isinstance(inferred, str):
            return inferred
        parent = inferred
    else:
        found = _sole_child(content, root, tree.display, FOLDER_TYPE)
        if isinstance(found, str):
            return found
        if found is None:
            block = (
                folder_open(tree.display, 1, indent_at(1))
                + _catalog_block(folder_name, pairs, indent_at(2))
                + node_close(indent_at(1))
            )
            at = _first_child_offset(content, root)
            if at is None:
                return (
                    f"the {tree.display!r} tree cannot be created: "
                    f"ROOT is not line terminated"
                )
            content[at:at] = bytearray(block.encode("utf-8"))
            _bump_count(content, root, +1)
            return None
        parent = found

    if parent.self_closing:
        return f"cannot find close tag for folder: {parent.name}"

    existing = _sole_child(content, parent, folder_name, FOLDER_TYPE)
    if isinstance(existing, str):
        return existing
    if existing is not None:
        return _merge_catalog(content, existing, pairs)

    block = _catalog_block(folder_name, pairs, indent_at(parent.depth + 1)).encode("utf-8")
    at = _first_child_offset(content, parent)
    if at is None:
        return f"the folder {parent.name!r} is not line terminated"
    content[at:at] = bytearray(block)
    _bump_count(content, parent, +1)
    return None


def _merge_catalog(
    content: bytearray,
    folder: NodeSpan,
    pairs: Sequence[tuple[str, Sequence[object]]],
) -> str | None:
    """Merge the pairs into a folder the document already holds, in place.

    Every edit lands after the folder's open tag, so the folder is re-read from
    that offset after each one rather than trusting spans an edit has moved.
    """
    if not _starts_its_line(content, folder.line_start, folder.tag_start):
        return f"the folder {folder.name!r} does not start its own line"
    indent = folder.indent + INDENT_STEP
    if folder.self_closing:
        # An empty folder exported self closed has no body, so it is opened first.
        content[folder.tag_end - 1 : folder.tag_end + 1] = bytearray(
            b">" + CRLF + b" " * folder.indent + _NODE_CLOSE
        )

    created = 0
    for name, track_ids in pairs:
        here = node_at(content, folder.tag_start, depth=folder.depth)
        if here is None:  # pragma: no cover - the folder was bounded a moment ago
            return f"the folder {folder.name!r} is no longer terminated"
        playlist = _sole_child(content, here, name, PLAYLIST_TYPE)
        if isinstance(playlist, str):
            return playlist
        if playlist is not None:
            warning = _extend_playlist(content, playlist, track_ids)
            if warning is not None:
                return warning
            continue

        # Before the first HELD playlist whose name sorts below the new one, and
        # last when none does: newest first among what the folder holds, even a
        # year the caller left out this time.
        wanted = _folded(name)
        anchor = next(
            (
                child
                for child in child_nodes(content, here)
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
            ),
            None,
        )
        if anchor is not None:
            at = anchor.line_start
            if not _starts_its_line(content, at, anchor.tag_start):
                return f"the playlist {anchor.name!r} does not start its own line"
        else:
            at = line_start(content, here.close_start)
            if not _starts_its_line(content, at, here.close_start):
                return f"the close tag of folder {folder.name!r} does not start its own line"
        content[at:at] = bytearray(_catalog_playlist(name, track_ids, indent).encode("utf-8"))
        created += 1

    if created:
        here = node_at(content, folder.tag_start, depth=folder.depth)
        if here is None:  # pragma: no cover - the folder was bounded a moment ago
            return f"the folder {folder.name!r} is no longer terminated"
        _bump_count(content, here, created)
    return None


def _extend_playlist(
    content: bytearray, playlist: NodeSpan, track_ids: Sequence[object]
) -> str | None:
    """Add the ids a playlist does not already hold, and move its entry count.

    Its members stay exactly as they are, duplicates included: rewriting a
    person's playlist would be the replace this writer stopped doing.
    """
    fresh = dedupe_track_ids(track_ids, track_keys(content, playlist))
    if not fresh:
        return None
    if not _starts_its_line(content, playlist.line_start, playlist.tag_start):
        return f"the playlist {playlist.name!r} does not start its own line"
    entries = attribute_span(content, "Entries", start=playlist.tag_start, end=playlist.tag_end)
    if entries is None:
        return f"Entries attr not found for playlist {playlist.name!r}"
    total = _read_int(content, entries) + len(fresh)
    lines = track_key_lines(fresh, playlist.indent + INDENT_STEP).encode("utf-8")
    # Insert FIRST, then patch the count, which sits before every insert point.
    if playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
        )
    else:
        at = line_start(content, playlist.close_start)
        if not _starts_its_line(content, at, playlist.close_start):
            return f"the close tag of playlist {playlist.name!r} does not start its own line"
        content[at:at] = bytearray(lines)
    content[entries[0] : entries[1]] = str(total).encode("utf-8")
    return None


def _bump_count(content: bytearray, node: NodeSpan, delta: int) -> None:
    """Move a folder's child count by ``delta``, never below zero."""
    span = attribute_span(content, "Count", start=node.tag_start, end=node.tag_end)
    if span is None:
        return
    current = _read_int(content, span)
    content[span[0] : span[1]] = str(max(0, current + delta)).encode("utf-8")


__all__ = [
    "COLLECTION_SECTION",
    "CRLF",
    "FOLDER_TYPE",
    "INDENT_STEP",
    "INTAKE_DEPTH",
    "KIND_FOLDER",
    "KIND_PLAYLIST",
    "KIND_UNREADABLE",
    "PLAYLISTS_SECTION",
    "PLAYLIST_TYPE",
    "ROOT_INDENT",
    "SUB_CLOSE_INDENT",
    "TRACK_INDENT",
    "TREE_DEPTH",
    "UNGOVERNED_WRITERS",
    "NodeSpan",
    "SpliceResult",
    "TrackSpan",
    "Tree",
    "TreeTooDeep",
    "apply_rating_changes",
    "assert_bridge_can_serve",
    "attribute_span",
    "attributes",
    "child_nodes",
    "collection_span",
    "collection_tracks",
    "dedupe_track_ids",
    "depth_of",
    "direct_child",
    "empty_playlist",
    "find_collection_track",
    "find_node",
    "folder_open",
    "indent_at",
    "insert_catalog_folder",
    "insert_empty_subplaylist",
    "insert_genre_folder",
    "insert_intake_playlist",
    "intake_names",
    "insert_root_playlist",
    "intake_tree",
    "line_start",
    "matching_close",
    "name_marker",
    "node_at",
    "node_close",
    "node_kind",
    "patch_attribute",
    "playlist_open",
    "playlists_span",
    "playlists_start",
    "remove_folder_node",
    "remove_tracks_from_subplaylist",
    "root_node",
    "routing_tree",
    "section_span",
    "splice_into_subplaylist",
    "track_key_line",
    "track_key_lines",
    "track_keys",
    "tree_for",
    "walk_nodes",
    "xml_escape_attr",
    "xml_unescape_attr",
]

# The read-only placement helpers, bound last: rbxml_insert imports this
# module's names at its own end, so either module may be imported first.
from cratekit.write.rbxml_insert import (
    _absorb_lead_break,
    _break_before,
    _catalog_block,
    _catalog_playlist,
    _first_child_offset,
    _folded,
    _folder_and_sub,
    _lead_broken_playlist,
    _merged_pairs,
    _playlist_root,
    _sole_child,
    _starts_its_line,
    _tree_node,
    _tree_scope,  # noqa: F401 - reachable as rbxml._tree_scope
    _type_name,  # noqa: F401 - reachable as rbxml._type_name
    direct_child,
    intake_names,
)
