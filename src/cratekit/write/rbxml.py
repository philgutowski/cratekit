"""The rekordbox XML byte bridge: one set of locates, one set of writes, one guard.

rekordbox's export is not "some XML". It is a byte format with conventions a
general purpose serializer does not preserve, and every rule below was learned by
breaking a real library.

THE FOUR BYTE RULES, AND THE INCIDENT BEHIND EACH.

* **CRLF only, on the write side.** rekordbox writes and reads ``\\r\\n``. A
  splicer that emitted a bare LF produced a playlist rekordbox rendered wrong,
  and the damage was invisible in every text editor anybody opened it in. Reads
  are forgiving, because real exports still carry lines that old splicer wrote,
  and removal has to find those or the corruption becomes permanent.

* **Never round trip through a tree serializer.** Both ``lxml`` and the standard
  library collapse multi line attributes, and rekordbox's display breaks on the
  result. Reads may parse; writes are byte splices into the original document.

* **Anchors are scoped to the playlist section.** A search from byte zero for a
  ``Name=`` attribute finds a COLLECTION track of that name first, because the
  collection precedes the playlists in the document. The system this replaces had
  three splicers that did exactly this: given a track named after a folder and a
  track named after a sub-playlist, all three warned and silently dropped the
  routing write. The user saw a successful run and an empty playlist.

* **Patch the count AFTER the insert, never before.** Growing ``Entries="0"`` to
  ``Entries="10"`` adds a byte. A splicer that recorded the closing tag's offset
  first, then patched the count, then wrote at the stale offset, corrupted the
  document tail. Ten tracks was the threshold, which is why it survived testing.

WHY THE LOCATES ARE HERE AND NOT AT THE CALL SITES. The claim this module makes
is that a guard living in the byte writers covers every byte write. That claim is
false while call sites can find a node themselves, because a call site that can
locate a node can splice into it without ever calling a writer. So the locates
are consolidated too, and they are the half that makes the guard's coverage real
rather than nominal. In the system this replaces there were, at least: two whole
byte engines, a locate keyed on a full open tag with its attributes in one fixed
order, a second locate keyed on the SAME tag with the attributes in the other
order, three indent pinned close tag searches, an indent based tree walk, a track
element bounded by the wrong token, and a track attribute patched inside a fixed
size window that could reach into the next element. Every one of those shapes is
expressible with the primitives below, and none of them needs its own regex.

WHY INDENTATION IS DERIVED. rekordbox indents the playlist root at four spaces
and adds two per level. The system this replaces pinned three constants for that,
so a tree of another depth silently emitted nodes at the wrong indent, which
every indent pinned locate then failed to find. Here one function turns a depth
into an indent, and the constants are named depths.

WHAT THE BRIDGE SERVES, AND WHY THAT RECONCILES A FIXED DEPTH WITH A USER'S OWN
TAXONOMY (KTD14). The intake tree's shape is pinned in this module and is not
read from the declared taxonomy: intake is one folder holding one playlist per
arriving batch, whatever anybody's genre tree looks like. So a template that
renames the levels, or reorders them, changes the routing tree and leaves intake
alone. The routing tree's shape does follow the taxonomy, and a taxonomy nesting
deeper than this indentation encodes is refused by name rather than emitted at an
indent nothing can find again. How many levels a template may DECLARE is one
number, and it lives in ``taxonomy`` because that is where a template is read;
this module carries the same number as the indentation it encodes, and a test
pins the two equal.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
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

#: How many levels below the playlist root the bridge's indentation encodes: a
#: root child, a folder inside it, and a sub-playlist inside that. Track keys sit
#: one level deeper again. A declared tree deeper than this is refused by name
#: (see :func:`assert_bridge_can_serve`) rather than written at an indent that no
#: later locate would find.
TREE_DEPTH = 3

#: The intake tree's depth, PINNED HERE and never read from the taxonomy (KTD14).
#: Intake is one folder holding one playlist per arriving batch. Deriving it from
#: somebody's genre tree is what forced the old system to choose between a fixed
#: depth and a user definable taxonomy; pinning it means neither has to give.
INTAKE_DEPTH = 2


def indent_at(depth: int) -> int:
    """Spaces of indentation for a node at ``depth`` below the playlist root.

    Depth 0 is the root node itself. One function rather than three constants,
    because three constants is how a tree of another shape came to be emitted at
    an indent that every indent pinned search then failed to find.
    """
    if depth < 0:
        raise ValueError(f"depth must not be negative, got {depth}")
    return ROOT_INDENT + INDENT_STEP * depth


#: Where a sub-playlist's own tags sit, and where its track keys sit. Both are
#: derived, and both remain arguments on every writer that emits them so a caller
#: serving a shallower tree does not have to fight the default.
SUB_CLOSE_INDENT = indent_at(TREE_DEPTH)
TRACK_INDENT = indent_at(TREE_DEPTH + 1)

#: The two node types rekordbox writes. A folder holds nodes, a playlist holds
#: track keys, and confusing them patches the wrong attribute: a folder carries
#: ``Count`` and a playlist carries ``Entries``.
FOLDER_TYPE = "0"
PLAYLIST_TYPE = "1"

#: The document sections. Named because both the locate scope and the failure
#: message have to spell them the same way.
PLAYLISTS_SECTION = "PLAYLISTS"
COLLECTION_SECTION = "COLLECTION"

# Quote aware open tag matchers. An attribute value may legally contain '>', and
# a track's open tag spans several lines in a real export, so neither tag can be
# bounded by a plain search for the next '>'.
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

    Ampersand, angle brackets and the double quote only. An apostrophe is legal
    to escape and rekordbox does not escape it, so escaping it anyway produces
    valid XML that no marker search will ever match, and the write silently
    misses the node it was aimed at.
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

    The ampersand is undone LAST, mirroring the escaper doing it first. Undoing
    it first would turn an escaped ampersand followed by ``lt;`` back into a
    literal angle bracket, which is a different string from the one that was
    written.
    """
    return (
        value.replace("&quot;", '"')
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
    )


def name_marker(name: str) -> bytes:
    """The exact ``Name="..."`` bytes as they appear in the document.

    Built with the one escaper the emitters use. Two escapers is how a marker
    stops matching the node it was built from.
    """
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
    """A self closed, empty playlist node.

    No trailing newline: callers splice it in front of an existing line break, so
    emitting one here would double it.
    """
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

    ``display`` is the name the document carries and is what the locates match
    on. ``id`` is the taxonomy's stable identifier, which is what the registry is
    keyed on, and it is never a display name (R19). The two are separate fields
    precisely because they are separate things: renaming a folder in rekordbox
    changes one and must not change the other.

    Both governance fields are present or both are absent. A tree that names an
    identifier but carries no registry could not be checked, and passing the
    check by default is the exact hole the guard exists to close; a registry with
    no identifier has nothing to look up. Neither half is useful alone, so
    neither half is allowed alone.

    ``Tree(display=...)`` with no governance is an UNGOVERNED playlist. It
    anchors the write and bypasses the guard entirely, which is correct and not a
    weakening: most playlists in a real library are somebody's own, this product
    governs none of them, and a guard that refused them would fire on correct
    code until somebody switched it off.
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

    The registry is REQUIRED and has no default, deliberately. These are the
    trees the registry exists to govern, so a default would hand a caller who
    omitted one argument a fully ungoverned tree that passes the guard in
    silence. That is the same hole :meth:`Tree.__post_init__` refuses one level
    down, and manufacturing it from a default here would be refusing it in one
    place and offering it in the other.

    A caller that has genuinely loaded no records yet passes
    ``tree_registry.EMPTY``, which says "nothing is recorded, so every tree is
    still on the bridge". That is a sentence somebody can check. An ungoverned
    playlist is still expressible, as ``Tree(display=...)``, because most
    playlists in a real library are somebody's own.
    """
    return Tree(display=node.display, id=node.id, registry=registry)


class TreeTooDeep(ValueError):
    """A declared tree the bridge's indentation cannot express.

    Refused by name, with the declared depth and the supported depth both in the
    message. The alternative is emitting nodes at an indent no later locate finds
    again, which reads to the user as a sweep that ran and did nothing.
    """

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

    Only DEEPER is refused here, because deeper is the case that would emit at an
    indent no later locate finds. Shallower is not this function's to refuse: the
    indent is derived from the depth rather than pinned, so the bytes would be
    findable, and the number of levels a TEMPLATE may declare is the taxonomy
    loader's rule rather than the bridge's. That loader takes exactly
    :data:`taxonomy.SUPPORTED_TREE_DEPTH` today, which is the same number as
    :data:`TREE_DEPTH`, and a test pins the two equal so the pair cannot drift
    into a template that loads at a depth this module cannot emit.

    So this guard is the second of two, not the only one, and it stays because a
    ``Taxonomy`` is a value a caller can build without going through the loader.
    """
    if declared.tree_depth > TREE_DEPTH:
        raise TreeTooDeep(
            tree_id=declared.tree.id,
            declared=declared.tree_depth,
            supported=TREE_DEPTH,
        )


def routing_tree(declared: taxonomy.Taxonomy, registry: tree_registry.Registry) -> Tree:
    """The declared routing tree, refused if the bridge cannot express its shape.

    The depth check belongs HERE and not on the intake tree, because this is the
    tree whose shape follows the taxonomy.
    """
    assert_bridge_can_serve(declared)
    return tree_for(declared.tree, registry)


def intake_tree(declared: taxonomy.Taxonomy, registry: tree_registry.Registry) -> Tree:
    """The intake tree, at the pinned shallow shape (KTD14).

    Deliberately NOT depth checked against the declared tree. Intake is one
    folder holding one playlist per arriving batch, and its shape is fixed in this
    module, so a taxonomy the bridge cannot serve for routing still has a working
    intake tree. That is the whole reconciliation: the fixed depth constrains the
    tree it actually describes, and stops constraining the one it does not.
    """
    return tree_for(declared.intake, registry)


def _refuse_wrong_medium(tree: Tree | None) -> None:
    """The emitter guard. Every byte writer below calls it first, except the ones
    ``UNGOVERNED_WRITERS`` names and says why.

    Three outcomes, and the middle one is the one people get wrong:

    * the tree is governed and native to the database, so the write is refused
      and the refusal names the tree;
    * the tree is governed and still on the bridge, so the write proceeds;
    * the tree is ungoverned, so the guard does not apply at all.

    The third is not a gap. A guard that refused an ordinary user playlist would
    fire on correct code, and a guard that fires on correct code gets suppressed,
    and a suppressed guard protects nothing (P7).
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

    ``close_start`` is -1 for a self closed node, and that is the distinction the
    depth walk exists to respect: a childless folder is exported self closed, so
    it has no matching close tag, and a walk that assumes one marches on to a
    SIBLING's close and deletes everything in between.
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

    A track element is self closed in a minimal export and multi line with a
    separate close tag in a real one. Bounding it by the next ``/>`` gets the
    second shape wrong, and the patch that follows then lands in whatever
    self closed element came next, which in an analysed export is the tempo child
    of the very same track.
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
    """The half open byte range of a top level section, open tag to close tag.

    Returns the offset of the section's ``<`` and the offset of its closing
    tag's ``<``. None when either end is missing, never a -1 for the caller to
    feed into slice arithmetic.
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
    """The offset of the playlist section's open tag, or -1.

    Kept as a named primitive because a caller's first question is usually "does
    this document even have a playlist section", and answering it by parsing the
    whole tree is a waste on a file this size.
    """
    return content.find(f"<{PLAYLISTS_SECTION}>".encode("utf-8"))


def collection_span(content: bytes) -> tuple[int, int] | None:
    """The collection section's bounds, for track element locates."""
    return section_span(content, COLLECTION_SECTION)


def attributes(content: bytes, node: NodeSpan | TrackSpan) -> dict[str, str]:
    """Every attribute on a located tag, unescaped, order independent.

    Order independent is the point. Two writers in the system this replaces
    matched the same node with the attributes in opposite orders, and each one
    silently found nothing in the other's output.
    """
    raw = bytes(content[node.tag_start : node.tag_end])
    return {
        key.decode("utf-8"): xml_unescape_attr(value.decode("utf-8"))
        for key, value in _ATTR_PAIR.findall(raw)
    }


@lru_cache(maxsize=64)
def _attr_pattern(name: str) -> re.Pattern[bytes]:
    return re.compile(rb'\b' + re.escape(name.encode("utf-8")) + rb'="([^"]*)"')


def attribute_span(content: bytes, name: str, *, start: int, end: int) -> tuple[int, int] | None:
    """Absolute bounds of one attribute's VALUE inside a located tag.

    The value's bounds rather than the value, because the two writes that matter
    here both need to replace digits in place, and both need offsets that stay
    valid across an insertion made elsewhere in the document.
    """
    match = _attr_pattern(name).search(bytes(content[start:end]))
    if match is None:
        return None
    return start + match.start(1), start + match.end(1)


def _read_int(content: bytes, span: tuple[int, int]) -> int:
    """The integer currently written in a located attribute value span."""
    return int(bytes(content[span[0] : span[1]]).decode("utf-8"))


def _open_tag_bounds(content: bytes, opening: int) -> tuple[int, bool] | None:
    """One open tag's end offset and whether it closes itself, quote aware.

    Through the same matcher :func:`node_at` uses, and that is the whole point.
    An attribute value may legally carry a '>', so a depth walk that bounded a
    tag with a plain search for the next one stopped inside a display name,
    counted a self closed node as an opening, and handed back a close tag
    belonging to an ancestor. The splice that followed landed in a different
    folder and reported success, which is the failure this module opens with.

    None when the bytes at ``opening`` are not a complete NODE open tag, so a
    truncated document refuses rather than being guessed at.
    """
    match = _NODE_OPEN.match(content, opening)
    if match is None:
        return None
    return match.end(), match.group(1).endswith(b"/")


def matching_close(content: bytes, tag_end: int) -> int:
    """The offset of the close tag matching an open tag that ends at ``tag_end``.

    A depth walk over node token PAIRS, and the pairing is what makes it correct.
    rekordbox writes an empty playlist as a self closed node, which opens and
    closes itself and so is depth neutral, and writes a track bearing one across
    several lines. Deriving depth from a count of close tags puts the first close
    after the open tag on the wrong node, and deriving it from self closing
    syntax puts every empty sibling one level too deep.

    Returns -1 when the node is unterminated, never a guess.
    """
    depth = 1
    cursor = tag_end + 1
    while True:
        opening = content.find(_NODE_OPEN_LEAD, cursor)
        closing = content.find(_NODE_CLOSE, cursor)
        if closing == -1:
            return -1
        if opening != -1 and opening < closing:
            bounds = _open_tag_bounds(content, opening)
            if bounds is None:
                return -1
            end, self_closing = bounds
            if not self_closing:
                depth += 1
            cursor = end
        else:
            depth -= 1
            if depth == 0:
                return closing
            cursor = closing + len(_NODE_CLOSE)


def node_at(content: bytes, tag_start: int, *, depth: int = 0) -> NodeSpan | None:
    """Bound the node whose open tag begins at ``tag_start``.

    None rather than a partially filled span when the tag cannot be parsed or the
    node is unterminated: a half located node feeds -1 into slice arithmetic, and
    a slice with a -1 in it does not fail, it deletes to the end of the document.
    """
    match = _NODE_OPEN.match(content, tag_start)
    if match is None:
        return None
    raw_attrs = match.group(1)
    self_closing = raw_attrs.endswith(b"/")
    tag_end = match.end() - 1
    found = dict(_ATTR_PAIR.findall(raw_attrs))
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

    Counted by walking node PAIRS from the playlist section, never derived from
    the indent. Indent is a formatting artifact, and reading depth out of it is
    exactly the shape that made an intake report misread any tree whose levels
    were not two spaces apart.
    """
    span = playlists_span(content)
    if span is None:
        return 0
    depth = 0
    cursor = span[0]
    while cursor < tag_start:
        opening = content.find(_NODE_OPEN_LEAD, cursor, tag_start)
        closing = content.find(_NODE_CLOSE, cursor, tag_start)
        if opening == -1 and closing == -1:
            break
        if opening != -1 and (closing == -1 or opening < closing):
            bounds = _open_tag_bounds(content, opening)
            if bounds is None:
                break
            end, self_closing = bounds
            if not self_closing:
                depth += 1
            cursor = end
        else:
            depth -= 1
            cursor = closing + len(_NODE_CLOSE)
    return depth


def root_node(content: bytes) -> NodeSpan | None:
    """The playlist root: the first node inside the playlist section.

    Located by position rather than by its name attribute. The name is a
    structural constant of the format rather than anything a user chose, but
    finding it by position also means an export that spells it differently, or a
    fixture that omits it, fails at the locate rather than three splices later.
    """
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

    Direct is the load bearing word. A byte search inside a node's range finds
    grandchildren too, and a writer that treated one as a child would replace a
    node several levels down while reporting that it had replaced a sibling.
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

    The path is what a caller diffing two documents needs, and building it during
    the walk is what stops each caller inventing its own tree index. The root's
    own name is not in the path, because it is a constant of the format rather
    than part of any tree a user named.
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

    ``start`` is required and has no default, deliberately. Every historical
    mis-anchor in this format came from a search that began at byte zero, and a
    default would be a byte zero waiting to happen.

    The type filter is the second half of the same defence. A folder and one of
    its own sub-playlists routinely share a name, the folder carries ``Count``
    and the playlist carries ``Entries``, and a splice that matched the folder
    patched the wrong attribute and dropped the track.
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
            # The marker has to sit inside THIS open tag. Otherwise it belongs to
            # something else entirely and the enclosing node is a coincidence.
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

    Tolerates a bare LF terminator, and this is the one place that tolerance
    lives. Real exports still carry lines an old splicer wrote with a bare LF, and
    a removal that could not find those would make that corruption permanent.
    Writes remain strictly CRLF.
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

    The marker carries the closing quote, so an id of 42 cannot match an element
    whose id is 421. A prefix match here rates, retags or relocates the wrong
    track, and the user has no way to tell which write was wrong.
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
    """Every collection track element, in document order, in one pass.

    The pass is the point. A caller patching many tracks that located each one
    separately is quadratic in the size of a real export, which is where the
    fixed size search window in the system this replaces came from, and that
    window is what let a patch reach into the following element.
    """
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
    match = _TRACK_OPEN.match(content, tag_start)
    if match is None:
        return None
    raw_attrs = match.group(1)
    self_closing = raw_attrs.endswith(b"/")
    tag_end = match.end() - 1
    found = dict(_ATTR_PAIR.findall(raw_attrs))
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
        tag_end=tag_end,
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
    """First occurrence dedup, by exact id and then by normalized name.

    Two identifiers can be the same recording. A re download, a different
    release, or a re import gives one recording two ids, so deduplicating on the
    identifier alone puts it in the playlist twice.
    """
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

#: Byte writers that target no tree, so no tree governs them and none of them
#: takes a ``tree`` argument.
#:
#: Declared rather than inferred, and the conformance test in
#: tests/test_tree_registry.py derives the full set of byte writers from this
#: module and asserts that this set plus the guarded ones covers it EXACTLY. So a
#: new emitter cannot land unguarded without the omission appearing in a diff
#: here, which is the P3 obligation applied to a set that cannot be derived from
#: behaviour alone.
#:
#: All three are decisions, and the boundary is the same one in each case: none
#: of them writes membership INSIDE A TREE, which is the thing a cutover moves.
#:
#: * the rating patch writes one collection attribute on one track. A track's
#:   rating does not change medium when a tree cuts over, so no tree governs it.
#: * the attribute patcher replaces one value inside a tag the caller has already
#:   located. Its legitimate uses are a collection attribute, which is ungoverned
#:   for the reason above, and recounting a tag while ASSEMBLING a new document,
#:   which writes nothing into the library at all. Reaching for it to change a
#:   live tree's entry count instead of calling a writer would route around the
#:   guard, and that is a residual this module cannot close from the inside: the
#:   locate consolidation makes calling it the only way to try, and naming the
#:   tree at the writers is the contract the call sites owe.
#: * the root playlist writer emits a playlist as a DIRECT child of the playlist
#:   root. A tree is a folder at that level, never a playlist, and the registry
#:   is keyed on taxonomy identifiers, which a standalone root playlist does not
#:   have. So no record could ever govern this write, and a tree argument here
#:   would arm the guard on a subject the write does not touch: name a tree that
#:   has cut over and a correct write is refused, name none and the tree the
#:   write is not touching goes unmentioned either way. A guard that fires on
#:   correct code gets switched off, and a switched off guard protects nothing
#:   (P7). What this writer DOES owe is the type check every other writer makes,
#:   so a root playlist named after a tree refuses instead of replacing it.
UNGOVERNED_WRITERS = frozenset(
    {"apply_rating_changes", "patch_attribute", "insert_root_playlist"}
)


@dataclass
class SpliceResult:
    """What a splice did, or the reason it did nothing.

    A warning rather than an exception for a missing node, because a sweep
    touches many playlists and one absent folder is a fact to report at the end,
    not a reason to abandon the other forty writes. A refusal by the guard IS an
    exception, because that one means the caller is writing in the wrong medium
    and continuing would corrupt a library.
    """

    inserted: int = 0
    entries_after: int | None = None
    created: bool = False
    warning: str | None = None


#: Attribute names that carry a beat grid, in the one spelling this module
#: compares: lowercase, so a caller cannot reach the grid through a difference in
#: case. Held here rather than only in the source scan because the scan reads
#: string CONSTANTS, and an attribute name arriving as a call argument is not a
#: constant it can see. R17 is absolute in both directions: this package never
#: creates a grid, and never destroys the one rekordbox authored. A generic
#: attribute patcher over export bytes is the only primitive here that could do
#: either, so the refusal lives in it.
_GRID_ATTRIBUTES = frozenset({"averagebpm", "bpm", "inizio", "metro", "battito"})


def patch_attribute(
    content: bytearray, name: str, value: object, *, start: int, end: int
) -> bool:
    """Replace one attribute's value inside an ALREADY LOCATED tag.

    Bounded by the tag, never by a fixed size window. The window version of this
    could not tell "this element has no such attribute" from "the next element
    does", so it patched the next element's, and the user saw a rating land on a
    track they had never touched.

    Strings are escaped through the one escaper. Numbers are written as digits.

    A tempo bearing attribute is REFUSED rather than patched. The two reachable
    shapes are a track's own average tempo, which rekordbox reads on import as
    the seed for its analysis, and a tempo element's own attributes, which a
    caller reaches by passing a range that bounds the whole element rather than
    its open tag. Both are grid writes, and a grid is rekordbox's to author (R17).
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


def _tree_node(content: bytes, tree: Tree | None) -> NodeSpan | str:
    """The node a tree scoped write happens inside, or a warning naming why not.

    With no tree named, the enclosing node is INFERRED as the playlist root's one
    folder child, and inference is refused when there is more than one. Guessing
    among several would put a whole genre folder inside whichever tree happened to
    come first in the document.
    """
    span = playlists_span(content)
    if span is None:
        return f"{PLAYLISTS_SECTION} section not found"
    root = root_node(content)
    if root is None:
        return "ROOT node not found"
    folders = [child for child in child_nodes(content, root) if child.node_type == FOLDER_TYPE]
    if tree is not None:
        # A tree is a DIRECT child of the playlist root, so it is looked up among
        # those rather than searched for anywhere below. That is not pedantry: a
        # folder several levels down could share the name, and writing a whole
        # tree's worth of nodes inside it would be silent.
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


def _type_name(node_type: str) -> str:
    """How a node type is spelled in a refusal a person has to act on."""
    return "folder" if node_type == FOLDER_TYPE else "playlist"


def _direct_child(
    content: bytes, parent: NodeSpan, name: str, node_type: str
) -> NodeSpan | str | None:
    """The direct child of ``parent`` named ``name``, of that TYPE, or a warning.

    Three answers: the node, None when no child carries the name, and a warning
    when one does at the other type.

    The type half is not pedantry, it is the same defence :func:`find_node`
    carries. A folder and a playlist routinely share a name, and every writer
    below replaces or deletes what this returns. Matched on the name alone, a
    root level playlist named after a tree replaced that whole tree with a flat
    playlist, and every playlist and every track key underneath it went with it,
    while the run reported success. Refusing is the only safe answer: the caller
    asked to write one kind of node and something else is already standing there.
    """
    for child in child_nodes(content, parent):
        if child.name != name:
            continue
        if child.node_type == node_type:
            return child
        return (
            f"a {_type_name(child.node_type)} named {name!r} is already there, and "
            f"this writer emits a {_type_name(node_type)}; replacing one with the "
            f"other would delete everything the existing node holds"
        )
    return None


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

    Dedup on insert, on BOTH paths: a track already in the sub is never added
    again, by id or by normalized name, and neither is a track the batch itself
    names twice. With ``create_missing`` a sub that does not exist is created as
    the last child of the folder.

    A FOLDER's ``Count`` is advisory, because rekordbox recounts a folder's
    children on import, and this one splice leaves it alone: its exact bytes are
    pinned by a golden ported from the system being replaced. The writers that
    add or remove a whole child do keep it accurate, so a document this package
    wrote still describes itself to the next thing that reads it. A PLAYLIST's
    ``Entries`` is not advisory and is always patched, because rekordbox trusts
    it over the children it can see.

    A failure writes NOTHING. Not most of it, nothing. A partial byte splice into
    this format is not a partial success, it is a corrupt file.
    """
    _refuse_wrong_medium(tree)
    if not track_ids:
        return SpliceResult()

    scope = _tree_scope(content, tree)
    if isinstance(scope, str):
        return SpliceResult(warning=scope)
    scope_start, scope_end = scope

    folder = find_node(
        content, genre_folder, start=scope_start, end=scope_end, node_type=FOLDER_TYPE
    )
    if folder is None:
        return SpliceResult(warning=f"genre folder not found: {genre_folder}")

    # Search for the sub AFTER the folder's own open tag. Starting at the folder
    # would re-find the folder itself when the two share a name, landing on a tag
    # that carries a count rather than an entry count, and silently dropping the
    # track.
    sub = find_node(
        content,
        sub_name,
        start=folder.body_start,
        end=folder.body_end,
        node_type=PLAYLIST_TYPE,
    )

    if sub is None:
        if not create_missing:
            return SpliceResult(warning=f"sub-playlist not found: {genre_folder}/{sub_name}")
        if folder.self_closing:
            return SpliceResult(
                warning=f"cannot find close tag for genre folder: {genre_folder}"
            )
        # Deduplicated here too, against nothing existing. The batch itself can
        # carry one recording twice, under one identifier or under two, and a
        # create path that skipped this made the outcome depend on whether the
        # sub happened to exist yet: the run that created it kept both copies
        # forever, and the run that found it kept one.
        fresh = dedupe_track_ids(track_ids, (), norm_by_tid)
        new_node = (
            "\r\n"
            + playlist_open(sub_name, len(fresh), close_indent)
            + track_key_lines(fresh, track_indent)
            + " " * close_indent
            + "</NODE>"
        ).encode("utf-8")
        at = line_start(content, folder.close_start) - len(CRLF)
        content[at:at] = bytearray(new_node)
        return SpliceResult(inserted=len(fresh), entries_after=len(fresh), created=True)

    existing_keys = track_keys(content, sub)
    filtered = dedupe_track_ids(track_ids, existing_keys, norm_by_tid)
    if not filtered:
        return SpliceResult()

    entries = attribute_span(content, "Entries", start=sub.tag_start, end=sub.tag_end)
    if entries is None:
        return SpliceResult(warning=f"Entries attr not found for {genre_folder}/{sub_name}")
    new_entries = _read_int(content, entries) + len(filtered)

    # Insert FIRST, then patch the count. The insert happens at or after the open
    # tag's end, so the count's offsets stay valid; patching first shifts every
    # later offset the moment the count grows a digit, and the write then lands
    # past the end of the document.
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


def _tree_scope(content: bytes, tree: Tree | None) -> tuple[int, int] | str:
    """The byte range a folder search is confined to, or a warning naming why not.

    With a tree named, the range is that tree's own node, so a folder of the same
    name under a DIFFERENT tree is not a candidate. With none named, it is the
    whole playlist section, which is the narrowest honest answer: still never the
    whole document, because the collection precedes it and holds track names.
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

    Returns how many were actually removed and a warning or None. The count is
    decremented by what was removed rather than by what was asked for, because
    rekordbox trusts the count over the number of children it can see.

    Takes ``track_indent`` and NOT the close indent its inserting counterpart
    takes. Removal re-bounds the node from the bytes it finds rather than from a
    width it was told, so a close indent here would be a knob that does nothing,
    and a knob that does nothing reads as a pair of functions being symmetric
    when only one half of them is.
    """
    _refuse_wrong_medium(tree)
    if not track_ids:
        return 0, None

    scope = _tree_scope(content, tree)
    if isinstance(scope, str):
        return 0, scope
    scope_start, scope_end = scope

    folder = find_node(
        content, genre_folder, start=scope_start, end=scope_end, node_type=FOLDER_TYPE
    )
    if folder is None:
        return 0, f"genre folder not found: {genre_folder}"
    sub = find_node(
        content,
        sub_name,
        start=folder.body_start,
        end=folder.body_end,
        node_type=PLAYLIST_TYPE,
    )
    if sub is None:
        return 0, f"sub-playlist not found: {genre_folder}/{sub_name}"
    if sub.self_closing:
        return 0, None  # an empty sub, nothing to remove

    entries = attribute_span(content, "Entries", start=sub.tag_start, end=sub.tag_end)
    removed = 0
    close_start = sub.close_start
    for tid in track_ids:
        # Re-bound the node on each pass: every deletion moves its close tag.
        current = NodeSpan(
            name=sub.name,
            node_type=sub.node_type,
            depth=sub.depth,
            line_start=sub.line_start,
            tag_start=sub.tag_start,
            tag_end=sub.tag_end,
            self_closing=False,
            close_start=close_start,
            close_end=close_start + len(_NODE_CLOSE),
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

    Ids appear on collection tracks only, since playlists reference tracks by
    key, so this needs no playlist scoping. Every element is located in ONE pass
    and the patches are applied from the end of the document backwards, so a
    value that grows a digit cannot invalidate the offsets of the ones still to
    come.

    No tree governs this: it writes an attribute on a track and no membership
    anywhere, so a tree's cutover does not change where it belongs. See
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


def insert_root_playlist(
    name: str,
    track_ids: Sequence[object],
    content: bytearray,
) -> str | None:
    """Append a playlist as the last child of the playlist root, replacing any
    existing playlist of the same name.

    Every workflow here is re-runnable, which means every write is idempotent. A
    second run that appended a second copy would turn "run it again" from the
    recovery procedure into a second failure.

    Only a DIRECT child is replaced. The version this ports searched the whole
    subtree and then assumed whatever it found sat at the root's own indent, so a
    nested playlist of the same name was deleted across a range that was not its
    own.

    Takes no tree, and that is a decision rather than an omission. See
    ``UNGOVERNED_WRITERS``: the playlist root is not a tree, nothing the registry
    can record sits at this level, and a tree named here would arm the guard on a
    subject the write does not touch.
    """
    if playlists_span(content) is None:
        return f"{PLAYLISTS_SECTION} section not found"
    root = root_node(content)
    if root is None:
        return "ROOT node not found"

    existing = _direct_child(content, root, name, PLAYLIST_TYPE)
    if isinstance(existing, str):
        return existing
    if existing is not None:
        start = existing.line_start
        if bytes(content[start - len(CRLF) : start]) == CRLF:
            start -= len(CRLF)
        del content[start : existing.close_end]
        root = root_node(content)
        if root is None:  # pragma: no cover - the delete cannot remove the root
            return "ROOT node not found"

    new_node = (
        "\r\n"
        + playlist_open(name, len(track_ids), indent_at(1))
        + track_key_lines(track_ids, indent_at(2))
        + " " * indent_at(1)
        + "</NODE>"
    ).encode("utf-8")
    at = line_start(content, root.close_start) - len(CRLF)
    content[at:at] = bytearray(new_node)
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

    The folder sits one level below the tree and its subs one level below that,
    both derived from :data:`TREE_DEPTH` rather than pinned. Bumps the tree's
    count by one. Idempotent: an existing child of that name is left alone, which
    is what stops a second import growing a duplicate node.
    """
    _refuse_wrong_medium(tree)
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    existing = _direct_child(content, parent, folder_name, FOLDER_TYPE)
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
    ).encode("utf-8")

    # Insert FIRST, then bump the count, mirroring the splice: the count sits
    # inside the open tag, which precedes the insertion point, so its offsets stay
    # valid and a count that grows a digit cannot shift a live offset.
    at = line_start(content, parent.close_start) - len(CRLF)
    content[at:at] = bytearray(block)
    _bump_count(content, parent, +1)
    return None


def remove_folder_node(
    content: bytearray,
    folder_name: str,
    *,
    tree: Tree | None = None,
) -> str | None:
    """Remove a named folder that is a direct child of a tree, and its lead break.

    The matching close is found by a depth walk over node PAIRS, so a childless
    folder, which rekordbox exports self closed and which therefore has no
    matching close at all, is removed as exactly its own open tag. A walk that
    assumed a close tag would march on to a SIBLING's and delete everything in
    between, which destroys data rather than merely misbehaving.

    An absent name is a warning and a no-op, never an exception and never a
    corrupting slice.
    """
    _refuse_wrong_medium(tree)
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    target = _direct_child(content, parent, folder_name, FOLDER_TYPE)
    if isinstance(target, str):
        return target
    if target is None:
        return f"folder node not found: {folder_name}"

    start = target.line_start
    if bytes(content[start - len(CRLF) : start]) == CRLF:
        start -= len(CRLF)
    del content[start : target.close_end]
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

    :data:`INTAKE_DEPTH` rather than the tree's own depth, and that is KTD14 made
    concrete: intake is one folder holding one playlist per arriving batch, so
    this shape does not move when somebody's genre taxonomy does.

    Idempotent, like every other write here: an existing playlist of that name is
    replaced rather than joined by a second copy, and the tree's count is bumped
    only when a new node is actually added.
    """
    _refuse_wrong_medium(tree)
    parent = _tree_node(content, tree)
    if isinstance(parent, str):
        return parent
    if parent.self_closing:
        return f"cannot find close tag for folder: {parent.name}"

    replaced = False
    existing = _direct_child(content, parent, name, PLAYLIST_TYPE)
    if isinstance(existing, str):
        return existing
    if existing is not None:
        start = existing.line_start
        if bytes(content[start - len(CRLF) : start]) == CRLF:
            start -= len(CRLF)
        del content[start : existing.close_end]
        replaced = True
        refreshed = _tree_node(content, tree)
        if isinstance(refreshed, str):  # pragma: no cover - the tree cannot vanish
            return refreshed
        parent = refreshed

    node = (
        "\r\n"
        + playlist_open(name, len(track_ids), indent_at(INTAKE_DEPTH))
        + track_key_lines(track_ids, indent_at(INTAKE_DEPTH + 1))
        + " " * indent_at(INTAKE_DEPTH)
        + "</NODE>"
    ).encode("utf-8")
    at = line_start(content, parent.close_start) - len(CRLF)
    content[at:at] = bytearray(node)
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

    The one write no other emitter here can make, and it exists because rekordbox
    has no import path that creates an empty playlist. A splice needs somewhere to
    splice INTO, so a routing sub that no track has landed in yet has to be
    created before the first track can be routed to it, and
    :func:`splice_into_subplaylist` cannot do it: with no track keys there is
    nothing to insert, and it returns early rather than emitting a node.

    Idempotent, and that is the property the caller depends on: a folder that
    already carries the sub is left byte-identical, so a re-run after a new folder
    appears touches only the new one.

    The indent is derived from the located folder's own depth rather than pinned,
    so a shallower tree gets a sub at the indent its own document uses. The
    override exists for a caller assembling a document at a shape this tree does
    not describe, and defaults to None rather than to a number so that "derive it"
    stays the answer nobody has to opt into.
    """
    _refuse_wrong_medium(tree)
    scope = _tree_scope(content, tree)
    if isinstance(scope, str):
        return SpliceResult(warning=scope)
    scope_start, scope_end = scope

    folder = find_node(
        content, folder_name, start=scope_start, end=scope_end, node_type=FOLDER_TYPE
    )
    if folder is None:
        return SpliceResult(warning=f"genre folder not found: {folder_name}")

    existing = _direct_child(content, folder, sub_name, PLAYLIST_TYPE)
    if isinstance(existing, str):
        return SpliceResult(warning=existing)
    if existing is not None:
        return SpliceResult()
    if folder.self_closing:
        return SpliceResult(warning=f"cannot find close tag for genre folder: {folder_name}")

    indent = indent_at(folder.depth + 1) if close_indent is None else close_indent
    node = ("\r\n" + empty_playlist(sub_name, indent)).encode("utf-8")
    at = line_start(content, folder.close_start) - len(CRLF)
    content[at:at] = bytearray(node)
    _bump_count(content, folder, +1)
    return SpliceResult(created=True, entries_after=0)


def _catalog_block(
    folder_name: str, playlists: Sequence[tuple[str, Sequence[object]]], indent: int
) -> str:
    """One folder holding one ready-made playlist per pair, fully populated.

    A pure emitter over the shared string builders, so the only thing the caller
    below has to get right is where the bytes go.
    """
    out = [folder_open(folder_name, len(playlists), indent)]
    for name, track_ids in playlists:
        ids = list(track_ids)
        out.append(playlist_open(name, len(ids), indent + INDENT_STEP))
        out.append(track_key_lines(ids, indent + 2 * INDENT_STEP))
        out.append(node_close(indent + INDENT_STEP))
    out.append(node_close(indent))
    return "".join(out)


def insert_catalog_folder(
    content: bytearray,
    folder_name: str,
    playlists: Sequence[tuple[str, Sequence[object]]],
    *,
    tree: Tree | None = None,
) -> str | None:
    """Insert a whole populated folder into a tree, creating the tree when absent.

    The only writer here that emits a subtree rather than a node, because it
    serves the one workflow that produces a whole catalog at once: a label's
    releases, grouped into a playlist per year. Everything else in this module
    adds to a tree somebody already has.

    Where the bytes go, and why each choice rather than the other:

    * **A new folder goes in FIRST, not last**, which is the reverse of every
      other insert here. The caller orders its playlists newest first, and a
      catalog whose newest year sits at the top of the folder while its newest
      folder sits at the bottom of the tree is ordered two ways at once. This
      preserves the byte layout the system being replaced produced, which a
      golden pins.
    * **An existing folder of that name is REPLACED IN PLACE**, so a re-crawl
      refreshes a label rather than growing a second copy of it, and refreshing
      does not reshuffle a tree the user reads. The system being replaced always
      inserted, so its second run duplicated the whole label and its first run's
      tracks stayed behind in the stale copy. No golden covers that path, because
      that system had no test that ran twice.
    * **The tree's own node is created when it is missing**, as the playlist
      root's first child. A catalog tree is not a taxonomy tree: nobody's setup
      created it, and the first write is the thing that brings it into existence.

    Returns a warning naming what stopped it, or None on success. A failure
    writes nothing at all.
    """
    _refuse_wrong_medium(tree)
    if playlists_span(content) is None:
        return f"{PLAYLISTS_SECTION} section not found"
    root = root_node(content)
    if root is None:
        return "ROOT node not found"

    # With no tree named the enclosing node is inferred exactly as it is
    # everywhere else here, and inference refuses rather than guesses. With one
    # named, an absent node is not a failure: this writer creates it.
    created_tree = False
    if tree is None:
        inferred = _tree_node(content, None)
        if isinstance(inferred, str):
            return inferred
        parent: NodeSpan | None = inferred
    else:
        found = _direct_child(content, root, tree.display, FOLDER_TYPE)
        if isinstance(found, str):
            return found
        parent = found
        created_tree = found is None

    if created_tree:
        assert tree is not None  # created_tree is only reachable on the named branch
        block = (
            folder_open(tree.display, 1, indent_at(1))
            + _catalog_block(folder_name, playlists, indent_at(2))
            + node_close(indent_at(1))
        )
        at = _first_child_offset(content, root)
        if at is None:
            return f"the {tree.display!r} tree cannot be created: ROOT is not line terminated"
        content[at:at] = bytearray(block.encode("utf-8"))
        _bump_count(content, root, +1)
        return None

    assert parent is not None  # every other branch either returned or found one
    if parent.self_closing:
        return f"cannot find close tag for folder: {parent.name}"

    existing = _direct_child(content, parent, folder_name, FOLDER_TYPE)
    if isinstance(existing, str):
        return existing

    block = _catalog_block(folder_name, playlists, indent_at(parent.depth + 1)).encode("utf-8")
    if existing is not None:
        # Replaced across its own lines, trailing break included, so the block
        # that lands is exactly as line terminated as the one that left. The
        # count does not move: one child went out and one came in.
        start = existing.line_start
        end = existing.close_end
        if bytes(content[end : end + len(CRLF)]) == CRLF:
            end += len(CRLF)
        content[start:end] = bytearray(block)
        return None

    at = _first_child_offset(content, parent)
    if at is None:
        return f"the folder {parent.name!r} is not line terminated"
    content[at:at] = bytearray(block)
    _bump_count(content, parent, +1)
    return None


def _first_child_offset(content: bytes, parent: NodeSpan) -> int | None:
    """Where a first child's own line begins, or None when there is no such place.

    A node's body starts immediately after its open tag's ``>``, and what follows
    in this format is the break that ends that line. A block emitted at the body
    start would land ON the open tag's line; a block emitted after the break lands
    on its own. None rather than a guess when the break is absent, because the
    only way to write there anyway is to invent a line ending, and inventing one
    is how a bare LF got into an export in the first place.
    """
    at = parent.body_start
    if bytes(content[at : at + len(CRLF)]) != CRLF:
        return None
    return at + len(CRLF)


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
    "empty_playlist",
    "find_collection_track",
    "find_node",
    "folder_open",
    "indent_at",
    "insert_catalog_folder",
    "insert_empty_subplaylist",
    "insert_genre_folder",
    "insert_intake_playlist",
    "insert_root_playlist",
    "intake_tree",
    "line_start",
    "matching_close",
    "name_marker",
    "node_at",
    "node_close",
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
