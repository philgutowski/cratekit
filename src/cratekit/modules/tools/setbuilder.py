"""Feature Inventory row 29: the library-grounded set builder.

Give it an anchor track and it returns owned tracks that mix with it, ranked and
sequenced. Everything it knows comes from the library's own analyzed tags, which
is what makes it deterministic: the same anchor against the same files always
produces the same answer, with no network call, no adapter, and no write.

THE GROUNDING RULE, WHICH IS THE WHOLE DESIGN. Index membership IS ownership, so
a track that is not in the index cannot be recommended. That sounds obvious and
it is the constraint most recommendation code loses first, usually by enriching a
candidate from the web and forgetting that the enrichment created a candidate
that does not exist on disk. Here the pool is filtered from the index, the
ranking runs over pool entries, and the sequence is drawn from the ranked list,
so the constraint holds at the output boundary rather than being re-checked.

WHY THE INDEX READS FILES AND NOT AN EXPORT. Two of the five ranking signals,
energy and vocal prominence, exist only in the file tags; the export does not
carry them. Tempo lives in the title head rather than in a tempo tag, because
nothing in this product writes a tempo tag (R17). And an export lags a fresh
import by however long it has been since the user last exported, so a track added
this morning would be invisible to a set built this afternoon.

FOUR THINGS THIS PORT CHANGES, each closing a defect rather than tidying:

1. **The Camelot parser is the shared one.** The source module's own
   normalizer merely uppercased and stripped leading zeros, so ``0A``, ``13A``
   and ``99B`` all became confident answers for keys that are not on the wheel,
   and a candidate carrying one could enter the pool through a wrap-around that
   means nothing. ``naming.parse_camelot`` is bounded to 1..12 and is the only
   code parser in the product now.
2. **The head is parsed from the declared name template**, not from a private
   regular expression. The source's pattern hardcoded ``key - bpm - title`` and
   did not know about the lossy marker, so a marked file's clean title kept the
   marker and matched nothing.
3. **Genre affinity comes from the declared taxonomy** (R19). The source
   hardcoded one person's genre families as substring rules, so a user whose
   library is not house-centric got a soft prior that described somebody else's
   record collection.
4. **The vocal threshold is a parameter** (D7). The source reached up into an
   analysis module for it, which is one of the two live layering violations the
   plan says to fix rather than port; here an unsupplied threshold simply makes
   the vocal signal neutral, which is what a library with no vocal analysis
   should produce.

WHAT IS DELIBERATELY NOT PORTED. The source resolves an unowned anchor by
querying a streaming service for its artist and title, then asking a web lookup
for a key. The plan's disposition for this unit is "pure read, no writes, no
adapter, no jobs", so no network call ships here. The affordance survives as an
injected seam: a caller that wants web enrichment supplies it, and the default is
None, which means an unowned anchor asks for its key to be supplied rather than
guessing one.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from rapidfuzz import fuzz, process

from cratekit.core import config, routing, tags
from cratekit.core.naming import (
    AUDIO_EXTS,
    NameTemplate,
    parse_camelot,
    parse_head,
    split_head,
)
from cratekit.core.taxonomy import Taxonomy

log = logging.getLogger(__name__)

#: The tag fields the index reads. Every one is looked up through
#: ``core.tags``'s single container-correct reader, so this module never opens an
#: audio file itself and cannot disagree with the writer about where a field
#: lives.
INDEX_FIELDS: tuple[str, ...] = (
    "title",
    "artist",
    "genre",
    "initialkey",
    "energylevel",
    "voxlevel",
    "voxgender",
)

#: Cache format. Bumped when :class:`Track` gains or loses a field, because a
#: cached entry is deserialized straight into one and a stale shape would raise
#: on a machine that had simply run an older build. ALSO BUMPED WHEN THE PARSE
#: THAT FILLS ONE CHANGES, ``match_key``, the head parser or the Camelot parser:
#: a cached entry is that parse's output, and a changed parse touches no file's
#: modification time, so nothing else would ever retire the old answers. The
#: template stamp covers the parse's one DATA input; this covers its code.
#: 3: an entry carries the file's size and its modification time in nanoseconds.
CACHE_VERSION = 3


# ---------------------------------------------------------------------------
# The types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Track:
    """One owned track and the five signals the ranker uses.

    ``key`` is canonical Camelot (unpadded, upper: ``2A``, ``12B``). ``bpm`` is
    None when the name carried no tempo, ``energy`` and ``vox`` are None when the
    analysis passes never tagged the file. None means UNKNOWN throughout and is
    scored neutrally; it never means zero, because a track with no energy reading
    is not a track with no energy.
    """

    artist: str
    title: str
    key: str
    bpm: float | None
    genre: str
    energy: int | None
    vox: int | None
    voxgender: str | None
    #: The comparison form used for anchor lookup and for collapsing duplicates.
    match: str
    path: str = ""

    @property
    def display(self) -> str:
        return f"{self.artist} - {self.title}" if self.artist else self.title


@dataclass(frozen=True, slots=True)
class Anchor:
    """The track a set is built around, owned or not.

    ``owned`` and ``track`` are not redundant. An unowned anchor still carries a
    key and a tempo, supplied by the caller, and the pool is built from those; it
    simply contributes no genre, energy, or vocal signal, so those score neutral.
    """

    key: str | None
    bpm: float | None
    owned: bool
    track: Track | None = None
    display: str = ""
    #: True when the key did not come from the library's own analysis, so the
    #: caller must show it before the picks are trusted. A web-derived key flips
    #: the relative major/minor side often enough that trusting it silently
    #: produces a plausible, wrong set.
    key_needs_confirming: bool = False
    #: Set when the anchor could not be resolved at all. A structured absence
    #: rather than an exception: "not in your library" is an ordinary answer to
    #: an ordinary question, and the caller renders it.
    unresolved: str = ""


@dataclass(frozen=True, slots=True)
class Scored:
    """A pool entry with its harmonic tier, its role, and why it scored."""

    track: Track
    tier: str
    role: str
    score: float
    reason: str = ""


@dataclass(frozen=True, slots=True)
class SetPlan:
    """The result: the anchor, the ranked pool, and one suggested sequence."""

    anchor: Anchor
    pool: tuple[Scored, ...] = ()
    sequence: tuple[Scored, ...] = ()


@dataclass(frozen=True, slots=True)
class Weights:
    """Ranking weights, summing to one.

    A dataclass rather than module constants so two rankings can run in one
    process with different weights, which is what makes the weighting testable
    at all: constants would force a monkeypatch, and a monkeypatched weight is
    not the weight that ships.
    """

    harmonic: float = 0.35
    bpm: float = 0.20
    genre: float = 0.20
    energy: float = 0.15
    vocal: float = 0.10

    def __post_init__(self) -> None:
        total = self.harmonic + self.bpm + self.genre + self.energy + self.vocal
        if abs(total - 1.0) > 1e-9:
            raise ValueError(
                f"weights must sum to 1.0, found {total}. Scores from two "
                f"differently-normalized runs are not comparable, and the whole "
                f"output is an ordering of scores."
            )


DEFAULT_WEIGHTS = Weights()

#: Harmonic tiers, best first, with the score each contributes.
TIER_SCORE: Mapping[str, float] = {"perfect": 1.0, "boost": 0.6, "wider": 0.3}

#: Default half-width of the tempo band, in BPM.
DEFAULT_BPM_WIDTH = 5.0

#: Ranked companions returned when the caller names no count.
DEFAULT_POOL = 8

#: Picks per side in the suggested sequence.
DEFAULT_SIDE = 2


# ---------------------------------------------------------------------------
# Identity and normalization
# ---------------------------------------------------------------------------


def canonical_key(code: str | None) -> str:
    """Canonical unpadded Camelot, or "" when the code is not on the wheel.

    One parser, shared with naming and with every other consumer. The empty
    string is deliberate: a track whose key cannot be placed on the wheel cannot
    be harmonically ranked, so it is excluded from the index rather than carried
    with a key nobody can compare.
    """
    parsed = parse_camelot(code or "")
    if parsed is None:
        return ""
    number, letter = parsed
    return f"{number}{letter}"


def match_key(artist: str, title: str) -> str:
    """The comparison form for anchor lookup and duplicate collapse.

    Lowercased, punctuation-stripped, whitespace-collapsed. Deliberately NOT the
    identity primitive a match or a tombstone uses: those decide whether two
    recordings are the same VERSION, and being wrong there costs a file. This
    decides whether two index entries are the same work for the purpose of not
    listing it twice, and being wrong here costs one duplicate line.
    """
    text = f"{artist} {title}".lower()
    kept = [c if c.isalnum() or c.isspace() else " " for c in text]
    return " ".join("".join(kept).split())


# ---------------------------------------------------------------------------
# The index
# ---------------------------------------------------------------------------

TagReader = Callable[[Path], Mapping[str, str | None]]
FileLister = Callable[[Path, Sequence[Path]], Iterable[Path]]


def read_index_tags(path: Path) -> dict[str, str | None]:
    """Read the index fields from one file through ONE container open.

    All of :data:`INDEX_FIELDS` go through one ``core.tags.read_tags`` call,
    which opens the file once and reads each field under the dialect's own
    key. Each field answers exactly what ``core.tags.read_tag`` answers for it,
    because that reader is one field of this one: an absent field, an
    undecodable one (its neighbours still read), a container the tag module
    does not handle (nothing is opened) and a file that cannot be opened all
    read as None. Until U266 this asked ``read_tag`` once per field, and the
    first walk of a library opened every file seven times.

    A single unreadable file yields all-None rather than aborting the scan,
    which is safe here only because the caller asserts the mount precondition
    first: with the volume absent every file reads as untagged, and a whole
    library of untagged tracks is a perfectly valid input that produces a
    silently wrong answer.
    """
    return tags.read_tags(path, INDEX_FIELDS)


def iter_audio(root: Path, exclude: Iterable[Path] = ()) -> Iterator[Path]:
    """Every audio file under ``root``, in a stable order, less ``exclude``.

    Sorted, because the index order decides which of two duplicate works
    survives the collapse, and an unsorted walk would make that choice depend on
    the filesystem's mood.

    ``exclude`` names folders the library holds that are NOT the library's own
    music (U279): Cratekit's library state folder, whose rehearsals keep staged
    copies of real tracks, and the download staging folder when it sits under
    the root, which is where setup puts it by default. Their copies sorted ahead
    of ``Music`` and took the real files' place in the collapse. Each is matched
    by :class:`Exclusion`, by the directory it IS and never by its name, and is
    pruned rather than walked and filtered. Everything outside them is yielded
    exactly as ``sorted(root.rglob("*"))`` yields it, in the same order.
    """
    suffixes = frozenset(AUDIO_EXTS)
    for candidate in sorted(Exclusion.under(root, exclude).walk(root)):
        if candidate.suffix.lower() in suffixes:
            yield candidate


#: A directory's identity for the length of one walk: device and inode.
_Identity = tuple[int, int]


def _identity(status: os.stat_result) -> _Identity:
    return (status.st_dev, status.st_ino)


@dataclass(frozen=True, slots=True)
class Exclusion:
    """The folders under a root the index leaves out, BY LOCATION (U279).

    A path is not an identity. The configured staging folder may be spelled
    through a symlinked mount, with a trailing separator or a ``..``, or in
    another letter case on a volume that ignores case, and a library folder
    deeper down may share the state folder's NAME. So each configured folder is
    read once as the directory it is, its device and inode, and the walk
    compares directories against that, never names.

    ``folders`` maps each excluded directory's identity to the configured path,
    which a refusal names. ``ancestors`` holds the directories strictly between
    the root and an excluded folder: only those are walked by hand, and every
    other subtree is handed to ``rglob`` whole, so what is yielded outside the
    excluded folders is what today's walk yields. A configured folder that is
    missing, is the root, holds the root, or sits outside it excludes nothing.
    """

    folders: Mapping[_Identity, Path]
    ancestors: frozenset[_Identity]
    root: _Identity | None

    @classmethod
    def under(cls, root: Path, exclude: Iterable[Path]) -> Exclusion:
        try:
            top = _identity(os.stat(root))
        except OSError:
            return cls(folders={}, ancestors=frozenset(), root=None)
        folders: dict[_Identity, Path] = {}
        ancestors: set[_Identity] = set()
        for folder in exclude:
            chain = _chain_to(Path(folder), top)
            if chain:
                folders.setdefault(chain[0], Path(folder))
                ancestors.update(chain[1:])
        return cls(folders=folders, ancestors=frozenset(ancestors), root=top)

    def walk(self, root: Path) -> Iterator[Path]:
        """What ``root.rglob("*")`` yields, less every excluded folder and its contents.

        ``rglob`` yields every entry of every directory it reaches and descends
        into real directories only, never a symlink to one, and an entry it
        cannot list it passes over. The hand walk below keeps all three.
        """
        if not self.folders:
            yield from root.rglob("*")
            return
        try:
            with os.scandir(root) as listing:
                entries = list(listing)
        except OSError:
            return
        for entry in entries:
            child = root / entry.name
            identity = None
            try:
                if entry.is_dir(follow_symlinks=False):
                    identity = _identity(entry.stat(follow_symlinks=False))
            except OSError:
                identity = None
            if identity in self.folders:
                continue
            yield child
            if identity is None:
                continue
            if identity in self.ancestors:
                yield from self.walk(child)
            else:
                yield from child.rglob("*")

    def holder(self, path: Path) -> Path | None:
        """The configured excluded folder ``path`` sits in, or None.

        Read up the path's own folders, each as the directory it is, until the
        root: so an anchor spelled through a link into staging is placed where
        it is rather than where its spelling says.
        """
        if not self.folders:
            return None
        for folder in Path(path).parents:
            try:
                identity = _identity(os.stat(folder))
            except OSError:
                continue
            if identity in self.folders:
                return self.folders[identity]
            if identity == self.root:
                return None
        return None


def _chain_to(folder: Path, top: _Identity) -> list[_Identity]:
    """``folder`` and each directory above it, up to and not including ``top``.

    Empty when ``folder`` is not a directory strictly under ``top``. Read on the
    resolved path, so the chain is the real directories whatever the spelling,
    and each step compared by identity, so case and mount spelling cannot hide
    the root.
    """
    try:
        current = folder.resolve()
        if not current.is_dir():
            return []
    except OSError:
        return []
    chain: list[_Identity] = []
    while True:
        try:
            identity = _identity(os.stat(current))
        except OSError:
            return []
        if identity == top:
            return chain
        chain.append(identity)
        if current.parent == current:
            return []
        current = current.parent


def parse_entry(
    raw: Mapping[str, str | None],
    *,
    path: str = "",
    template: NameTemplate,
) -> Track | None:
    """Build a :class:`Track` from a tag mapping. Pure, so it needs no audio.

    Returns None when no Camelot key can be established, because a track that
    cannot be placed on the wheel cannot be harmonically compared and would enter
    the pool only through a tier lookup that means nothing.

    The key comes from the ``initialkey`` tag, falling back to the name head; the
    tempo and the clean title come from the head. That order matters: the tag is
    what the analysis pass wrote, while the head is what a renamer wrote from it,
    so the tag is the earlier and more authoritative of the two.
    """
    raw_title = (raw.get("title") or "").strip()
    head, remainder = split_head(raw_title, template=template)
    fields = _head_fields(raw_title, template=template)
    clean_title = remainder.strip() if head else raw_title

    key = canonical_key(raw.get("initialkey") or fields.get("key"))
    if not key:
        return None

    bpm = _as_float(fields.get("bpm"))
    artist = (raw.get("artist") or "").strip()
    return Track(
        artist=artist,
        title=clean_title,
        key=key,
        bpm=bpm,
        genre=(raw.get("genre") or "").strip(),
        energy=_as_int(raw.get("energylevel")),
        vox=_as_int(raw.get("voxlevel")),
        voxgender=(raw.get("voxgender") or "").strip() or None,
        match=match_key(artist, clean_title),
        path=path,
    )


def _head_fields(name: str, *, template: NameTemplate) -> dict[str, str]:
    return parse_head(name, template=template) or {}


def _as_int(value: object) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def build_index(
    root: Path | str,
    *,
    template: NameTemplate,
    cache_path: Path | None = None,
    reader: TagReader = read_index_tags,
    lister: FileLister = iter_audio,
    exclude: Sequence[Path] = (),
) -> tuple[Track, ...]:
    """Scan ``root`` and return the deduplicated index, in walk order.

    ``cache_path`` defaults to None, meaning NO CACHE, and there is deliberately
    no fallback path. The cache is a declared state file
    (``setbuilder_index_cache``) that the caller resolves through the state
    inventory; a module that composed its own path under a state root would
    create a file nothing walking that inventory can find, snapshot, or clear.
    None is what a test wants and what a one-off run can afford.

    The cache is keyed on path, modification time in nanoseconds AND size, so an
    edited file invalidates only itself. Size is there because the time alone is
    forgeable by exactly the tools a library is restored with: ``rsync -a``,
    ``cp -p`` and rclone all put different bytes at the same path under the old
    time, and the rest of this product pairs the two for that reason.

    THE WHOLE CACHE IS ALSO STAMPED WITH THE TEMPLATE it was parsed under,
    because a cached entry is the OUTPUT of a parse and the template is that
    parse's other input: a changed lossy marker alters every marked file's clean
    title and match key while touching no file's modification time, so without
    the stamp the old titles would be served for ever. A stamp that differs
    discards the cache, at the cost of one scan.

    A file whose parse yielded nothing is cached as nothing: without that, every
    keyless file in the library is re-read on every run, which is the majority
    of the cost on a library with unanalyzed corners. BUT A READ THAT RETURNED
    NO FIELD AT ALL IS NOT CACHED. The shared reader answers None for an absent
    tag and for a file it could not open alike, so a wholly empty read cannot be
    told from a momentary I/O error on an external volume, and caching it would
    drop an analyzed track from the index until somebody touched the file.
    Re-reading a file with no tags at all costs one open per run, which is the
    cheaper of the two mistakes.

    NOTHING IS WRITTEN WHEN THE WALK FOUND NO FILE. An empty walk over a root
    that is a directory is what an unmounted volume's leftover mountpoint looks
    like, and creating a state directory inside it is how the real volume comes
    to mount under a second name.

    A cache write failure is logged and swallowed. The cache is an optimization,
    and refusing to produce a set because a cache could not be written would turn
    a performance feature into an outage.

    ``exclude`` names the folders under ``root`` that are not the library's own
    music, handed to the lister (U279); :func:`iter_audio` prunes them. A cache
    entry is only ever served for a path the walk yields, and the cache written
    back holds only those, so an entry an earlier build cached under an excluded
    folder is never served and is gone after the next write.
    """
    root = Path(root)
    files = list(lister(root, tuple(exclude)))
    stamp = _template_stamp(template)
    cached = _load_cache(cache_path, stamp)

    fresh: dict[str, dict] = {}
    tracks: list[Track] = []
    seen: set[str] = set()
    for path in files:
        key = str(path)
        try:
            stat = path.stat()
            identity = {"mtime_ns": stat.st_mtime_ns, "size": stat.st_size}
        except OSError:
            # A file that cannot be stat'ed has no identity to cache under.
            identity = None
        entry = cached.get(key)
        if identity is not None and _entry_is_current(entry, identity):
            track = _track_from_cache(entry.get("track"))
            fresh[key] = entry
        else:
            raw = reader(path)
            track = parse_entry(raw, path=key, template=template)
            if identity is not None and any(value is not None for value in raw.values()):
                fresh[key] = {**identity, "track": asdict(track) if track else None}
        if track is None or not track.match or track.match in seen:
            continue
        seen.add(track.match)
        tracks.append(track)

    if files:
        _save_cache(cache_path, fresh, stamp)
    return tuple(tracks)


def _entry_is_current(entry: object, identity: Mapping[str, int]) -> bool:
    """Whether a cached entry describes the file as it is now.

    Every comparison is against a value of the right TYPE, because the cache is a
    file on a volume that syncs, and a hand edit or a conflict copy can hold any
    JSON at all. A cache that cannot be trusted costs one read, never the run.
    """
    return (
        isinstance(entry, dict)
        and entry.get("mtime_ns") == identity["mtime_ns"]
        and entry.get("size") == identity["size"]
        and (entry.get("track") is None or _track_from_cache(entry.get("track")) is not None)
    )


def _template_stamp(template: NameTemplate) -> str:
    """The template as a string that is equal exactly when the template is.

    Built field by field rather than taken from ``repr``, because the template
    holds a frozenset and a set's repr follows string hashing, which differs
    between two runs of the same build. A stamp that moved on its own would
    discard the cache on every run and look exactly like a cache that works.
    """
    parts = []
    for field in fields(template):
        value = getattr(template, field.name)
        if isinstance(value, (set, frozenset)):
            value = sorted(value)
        parts.append(f"{field.name}={value!r}")
    return ";".join(parts)


def _load_cache(cache_path: Path | None, stamp: str) -> dict[str, dict]:
    if cache_path is None or not cache_path.is_file():
        return {}
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict) or data.get("cache_version") != CACHE_VERSION:
        # A cache written by another build describes a Track shape this one may
        # not have. Discarding it costs one scan; deserializing it costs a
        # TypeError in the middle of a run.
        return {}
    if data.get("template") != stamp:
        return {}
    entries = data.get("entries")
    return entries if isinstance(entries, dict) else {}


def _save_cache(cache_path: Path | None, entries: Mapping[str, dict], stamp: str) -> None:
    if cache_path is None:
        return
    payload = json.dumps(
        {"cache_version": CACHE_VERSION, "template": stamp, "entries": dict(entries)}
    )
    try:
        # The shared state writer: a rename into place, so a killed run or two
        # runs at once leave the old cache or the new one and never half of one.
        config.atomic_write_bytes(payload.encode("utf-8"), cache_path)
    except OSError as exc:
        log.debug("set-builder index cache not written to %s: %s", cache_path, exc)


def _track_from_cache(raw: object) -> Track | None:
    if not isinstance(raw, dict):
        return None
    try:
        track = Track(**raw)
    except TypeError:
        return None
    # The right NAMES with the wrong TYPES construct without complaint and fail
    # later, inside the ranking, where nothing says the cache was the cause.
    texts = (track.artist, track.title, track.key, track.genre, track.match, track.path)
    if not all(isinstance(value, str) for value in texts):
        return None
    if not isinstance(track.voxgender, str | None):
        return None
    if not all(_is_number(value) for value in (track.bpm, track.energy, track.vox)):
        return None
    return track


def _is_number(value: object) -> bool:
    """None, or a real number. A bool is an int to Python and not to this."""
    return value is None or (isinstance(value, int | float) and not isinstance(value, bool))


# ---------------------------------------------------------------------------
# Harmony: the Camelot wheel and the tempo band
# ---------------------------------------------------------------------------


def _wrap(number: int) -> int:
    return ((number - 1) % 12) + 1


def compatible_keys(anchor_key: str) -> dict[str, str]:
    """``{camelot: tier}`` for the anchor. The perfect tier wins any overlap.

    Tiers relative to anchor ``nL`` (number n, letter L, other letter O):

        perfect  nL, (n+1)L, (n-1)L, nO     same key, either neighbour, relative
        boost    (n+2)L                     the energy lift
        wider    (n-2)L, (n+3)L, (n-1)O, (n+1)O   diagonals, used sparingly

    Assigned widest-first so the narrower tiers overwrite them, which is how a
    key that is both a diagonal and a neighbour ends up reported as the
    neighbour it is.
    """
    parsed = parse_camelot(anchor_key or "")
    if parsed is None:
        return {}
    number, letter = parsed
    other = "B" if letter == "A" else "A"
    tiers: dict[str, str] = {}
    for code in (
        f"{_wrap(number - 2)}{letter}",
        f"{_wrap(number + 3)}{letter}",
        f"{_wrap(number - 1)}{other}",
        f"{_wrap(number + 1)}{other}",
    ):
        tiers[code] = "wider"
    tiers[f"{_wrap(number + 2)}{letter}"] = "boost"
    for code in (
        f"{_wrap(number)}{letter}",
        f"{_wrap(number + 1)}{letter}",
        f"{_wrap(number - 1)}{letter}",
        f"{_wrap(number)}{other}",
    ):
        tiers[code] = "perfect"
    return tiers


def in_band(
    candidate_bpm: float | None,
    anchor_bpm: float | None,
    *,
    width: float = DEFAULT_BPM_WIDTH,
) -> bool:
    """True when the candidate sits within ``width`` of the anchor, its half, or
    its double.

    Half and double time are included because they are a mix, not a coincidence.
    An anchor with no tempo drops the constraint entirely rather than excluding
    everything, which is what makes a key-only pool possible; a CANDIDATE with no
    tempo is excluded when the anchor has one, because there is nothing to check
    it against and a silent pass would put an untested tempo in the set.
    """
    if anchor_bpm is None:
        return True
    if candidate_bpm is None:
        return False
    return any(
        abs(candidate_bpm - reference) <= width
        for reference in (anchor_bpm, anchor_bpm / 2, anchor_bpm * 2)
    )


def build_pool(
    anchor: Anchor,
    index: Sequence[Track],
    *,
    width: float = DEFAULT_BPM_WIDTH,
) -> tuple[tuple[Track, str], ...]:
    """Filter the index to harmonically and rhythmically compatible candidates.

    The anchor itself is excluded by match key rather than by path, so a second
    copy of the anchor (a re-import, an extended edit that normalizes the same)
    does not come back as its own best companion.
    """
    tiers = compatible_keys(anchor.key or "")
    anchor_match = anchor.track.match if anchor.track else None
    out: list[tuple[Track, str]] = []
    for track in index:
        if anchor_match and track.match == anchor_match:
            continue
        tier = tiers.get(track.key)
        if tier is None:
            continue
        if not in_band(track.bpm, anchor.bpm, width=width):
            continue
        out.append((track, tier))
    return tuple(out)


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------


def harmonic_score(tier: str) -> float:
    return TIER_SCORE.get(tier, 0.0)


def bpm_score(
    candidate: float | None,
    anchor: float | None,
    *,
    width: float = DEFAULT_BPM_WIDTH,
) -> float:
    """Proximity to the nearest of the anchor, its half, or its double.

    Neutral when either tempo is unknown, so a library where the tempo never made
    it into the name ranks on its other four signals instead of ranking randomly.
    """
    if candidate is None or anchor is None:
        return 0.5
    distance = min(abs(candidate - r) for r in (anchor, anchor / 2, anchor * 2))
    return max(0.0, 1.0 - distance / width)


def energy_score(candidate: int | None, anchor: int | None, role: str) -> float:
    """Role-aware energy fit, neutral when either reading is unknown.

    ``before`` rewards equal or lower (a lead-in), ``after`` rewards equal or
    higher (a lift), ``either`` rewards closeness. The divisor is the usable span
    of the 1-to-10 scale, so a full-scale difference saturates rather than going
    negative and being clamped away silently.
    """
    if candidate is None or anchor is None:
        return 0.5
    delta = candidate - anchor
    if role == "before":
        return max(0.0, min(1.0, 0.5 - delta / 8.0))
    if role == "after":
        return max(0.0, min(1.0, 0.5 + delta / 8.0))
    return max(0.0, 1.0 - abs(delta) / 8.0)


def vocal_score(
    candidate: int | None,
    anchor: int | None,
    *,
    threshold: float | None,
) -> float:
    """Penalize a vocal-forward companion beside a vocal-forward anchor.

    Two lead vocals over one another is the clash this signal exists to avoid.
    The threshold that decides "vocal-forward" is PASSED IN (D7): the source
    fetched it by importing an analysis module from inside the ranker, which
    raises on a slim install that has no analysis module at all. An absent
    threshold scores neutral-high, which is what a library with no vocal analysis
    should produce: no penalty, and no false confidence either.
    """
    if candidate is None or anchor is None or threshold is None:
        return 0.7
    both_vocal = candidate >= threshold and anchor >= threshold
    return 0.3 if both_vocal else 1.0


def _key_direction(candidate_key: str, anchor_key: str | None) -> int:
    """+1 for an upward move around the wheel, -1 for downward, 0 for neither."""
    anchor = parse_camelot(anchor_key or "")
    cand = parse_camelot(candidate_key or "")
    if anchor is None or cand is None:
        return 0
    diff = (cand[0] - anchor[0]) % 12
    if diff in (1, 2, 3):
        return 1
    if diff in (9, 10, 11):
        return -1
    return 0


def assign_role(track: Track, anchor: Anchor) -> str:
    """Where the candidate sits relative to the anchor.

    Energy decides it, with the wheel direction as the tiebreak, because energy
    is what a listener hears as "this came before that". When neither signal
    resolves, the answer is ``either`` rather than a guess, and the sequence
    builder uses those as filler for whichever side is short.
    """
    anchor_energy = anchor.track.energy if anchor.track else None
    if track.energy is not None and anchor_energy is not None:
        if track.energy > anchor_energy:
            return "after"
        if track.energy < anchor_energy:
            return "before"
    direction = _key_direction(track.key, anchor.key)
    if direction > 0:
        return "after"
    if direction < 0:
        return "before"
    return "either"


def _reason(track: Track, tier: str, anchor: Anchor, role: str, affinity: float) -> str:
    bits = [f"{tier} key ({track.key})"]
    anchor_energy = anchor.track.energy if anchor.track else None
    if track.energy is not None and anchor_energy is not None and track.energy != anchor_energy:
        delta = track.energy - anchor_energy
        bits.append(f"{delta:+d} energy, {role}")
    if affinity >= 0.6:
        bits.append("same family")
    return ", ".join(bits)


def rank(
    pool: Sequence[tuple[Track, str]],
    anchor: Anchor,
    *,
    taxonomy: Taxonomy,
    width: float = DEFAULT_BPM_WIDTH,
    weights: Weights = DEFAULT_WEIGHTS,
    vox_threshold: float | None = None,
) -> tuple[Scored, ...]:
    """Score the pool and order it, best first.

    ``taxonomy`` is a PARAMETER because the domain layer takes values (KTD23) and
    because a user's genre families are their own declaration (R19). The tie
    break is the match key, so two candidates that score identically order the
    same way on every run: an ordering that depends on the walk is an ordering a
    user cannot reproduce, and reproducibility is the point of the whole engine.
    """
    anchor_track = anchor.track
    anchor_genre = anchor_track.genre if anchor_track else None
    anchor_energy = anchor_track.energy if anchor_track else None
    anchor_vox = anchor_track.vox if anchor_track else None

    scored: list[Scored] = []
    for track, tier in pool:
        role = assign_role(track, anchor)
        affinity = routing.genre_affinity(taxonomy, anchor_genre, track.genre)
        score = (
            weights.harmonic * harmonic_score(tier)
            + weights.bpm * bpm_score(track.bpm, anchor.bpm, width=width)
            + weights.genre * affinity
            + weights.energy * energy_score(track.energy, anchor_energy, role)
            + weights.vocal * vocal_score(track.vox, anchor_vox, threshold=vox_threshold)
        )
        scored.append(
            Scored(
                track=track,
                tier=tier,
                role=role,
                score=score,
                reason=_reason(track, tier, anchor, role, affinity),
            )
        )
    scored.sort(key=lambda s: (-s.score, s.track.match))
    return tuple(scored)


# ---------------------------------------------------------------------------
# Anchor resolution and the sequence
# ---------------------------------------------------------------------------

WebKeyLookup = Callable[[str, str], Mapping[str, object] | None]


#: How close a typed anchor must be to an index entry before it counts as that
#: entry. High on purpose: building a set around the WRONG anchor is a worse
#: answer than refusing to build one, because every pick that follows is
#: internally consistent and therefore looks right.
MATCH_THRESHOLD = 90

#: How many candidates a refusal names. A vague query can reach a whole label's
#: worth of titles, and a listing nobody can read is not a remedy.
CANDIDATE_LIMIT = 10

#: How close one typed WORD must be to a word of the title to count as that
#: word. Low enough that a slip of the finger still lands, "anchr" on "anchor",
#: and high enough that the words which tell two versions apart never do:
#: "extended" on "original", "club" on "dub" and "remix" on "mix" all fall under.
WORD_THRESHOLD = 80


@dataclass(frozen=True, slots=True)
class AnchorMatch:
    """What a typed anchor names in the index: one track, several, or nothing.

    Three answers and not two. ``track`` set is a resolution. ``track`` None with
    ``candidates`` is a REFUSAL THAT KNOWS WHY: the name reached owned tracks and
    could not choose between them, and the caller shows them rather than picking.
    Both empty is an ordinary absence. Folding the middle answer into either
    neighbour is the defect this type exists to end (R-187): folded into the
    first it builds a set around whichever track the walk met first, and folded
    into the last it tells a person their track is not in their library.
    """

    track: Track | None = None
    #: The owned tracks the name reached, best score first, when none was chosen.
    candidates: tuple[Track, ...] = ()
    #: True when NO candidate holds every word of the name. Several candidates
    #: that each hold all of it is a choice between owned tracks. Candidates that
    #: all lack part of it is a different statement: the person named a version,
    #: a remix or a credit the library's copies do not carry, so what they named
    #: may not be owned at all.
    partial: bool = False


def match_in_index(
    query: str, index: Sequence[Track], *, threshold: int = MATCH_THRESHOLD
) -> AnchorMatch:
    """Resolve ``query`` against the index, refusing rather than guessing.

    AN EXACT HIT ON THE COMPARISON KEY WINS OUTRIGHT, before any fuzzy score is
    taken. ``token_set_ratio`` scores a subset at 100, so "Alder - Anchor Work"
    scores identically against that track and against "Alder - Anchor Work
    (Extended Mix)", and no threshold separates two candidates that are both at
    the ceiling. The exact comparison is the only thing that can.

    Fuzzy after that, because a user types what they remember, and the library's
    titles carry remix credits, feature credits, and label suffixes that nobody
    types. EVERY hit at the threshold is collected, never the first: one hit is
    a resolution and two are a question only the person can answer.

    A HIT COUNTS ONLY WHEN IT HOLDS EVERY WORD OF THE NAME. The set score cannot
    say so: it is 100 whenever one side is a subset of the other, in EITHER
    direction, and on a long title it stays above the threshold while the one
    word that matters differs, "Original Mix" against "Extended Mix". So each
    typed word is looked for among the hit's own, with room for a slip of the
    finger and none for a different word. Typing LESS than the title is
    remembering; typing something the title does not hold is naming something
    else. One hit that holds the whole name is the resolution, even when other
    titles scored as high on fewer words. Several are a question only the person
    can answer. Hits that ALL lack part of the name come back ``partial``.

    Candidates are ordered by score and then by match key and path, so the
    listing does not depend on the order a filesystem walk produced.
    """
    wanted = match_key("", query)
    if not wanted or not index:
        return AnchorMatch()
    exact = [t for t in index if t.match == wanted]
    if len(exact) == 1:
        return AnchorMatch(track=exact[0])
    if exact:
        return AnchorMatch(candidates=tuple(sorted(exact, key=lambda t: t.path)))
    hits = process.extract(
        wanted,
        [t.match for t in index],
        scorer=fuzz.token_set_ratio,
        score_cutoff=threshold,
        limit=None,
    )
    ordered = tuple(
        index[position]
        for _, score, position in sorted(
            hits, key=lambda hit: (-hit[1], index[hit[2]].match, index[hit[2]].path)
        )
    )
    holding = tuple(t for t in ordered if _holds_every_word(t.match, wanted))
    if len(holding) == 1:
        return AnchorMatch(track=holding[0])
    if holding:
        return AnchorMatch(candidates=holding)
    return AnchorMatch(candidates=ordered, partial=bool(ordered))


def _holds_every_word(match: str, wanted: str) -> bool:
    """Whether every word of ``wanted`` is a word of ``match``, give or take a slip."""
    held = match.split()
    return all(
        any(fuzz.ratio(word, other) >= WORD_THRESHOLD for other in held)
        for word in wanted.split()
    )


def find_in_index(
    query: str, index: Sequence[Track], *, threshold: int = MATCH_THRESHOLD
) -> Track | None:
    """The one track ``query`` names, or None. See :func:`match_in_index`.

    None covers both "nothing matched" and "more than one did", which is right
    for a caller that only wants an owned anchor when there is exactly one. A
    caller that has to TELL a person which it was reads the verdict instead.
    """
    return match_in_index(query, index, threshold=threshold).track


def resolve_anchor(
    query: str,
    index: Sequence[Track],
    *,
    key: str | None = None,
    bpm: float | None = None,
    web_lookup: WebKeyLookup | None = None,
) -> Anchor:
    """Resolve the anchor against the library, or against supplied values.

    Owned wins outright: the library's own analysis is authoritative, and an
    explicitly supplied key overrides it only because a user who passes one has
    seen the disagreement and made a call.

    An unowned anchor with no supplied key and no injected lookup is UNRESOLVED,
    not guessed. The source fired a streaming-service search here; this unit
    ships no network call, and a fabricated key would produce a full, confident,
    wrong set.
    """
    matched = match_in_index(query, index)
    # A PARTIAL REACH WITH A SUPPLIED KEY IS THE UNOWNED ANSWER, and falls
    # through to it: the person named a remix the library's copies do not carry
    # and said what key it is in, which is the "should I buy this" question.
    if matched.track is None and matched.candidates and not (matched.partial and key):
        # REACHED AND NOT CHOSEN, which is neither of the answers below. Falling
        # through would call an owned track unowned: with a key it would rank
        # the library's own copies as companions to themselves, and without one
        # it would say "not in your library" about a name that hit several.
        named = "; ".join(t.display for t in matched.candidates[:CANDIDATE_LIMIT])
        if matched.partial:
            why = (
                f"that anchor names more than the library's nearest copies hold, "
                f"so it may be a version you do not own; supply its Camelot key "
                f"if so, or name one of these as it is written: {named}"
            )
        else:
            why = (
                f"that anchor names {len(matched.candidates)} owned tracks, and "
                f"picking for you would build a set around the wrong one: {named}"
            )
        return Anchor(key=None, bpm=None, owned=False, display=query, unresolved=why)
    owned = matched.track
    if owned is not None:
        resolved_key = canonical_key(key) or owned.key
        return Anchor(
            key=resolved_key,
            bpm=bpm if bpm is not None else owned.bpm,
            owned=True,
            track=owned,
            display=owned.display,
            key_needs_confirming=bool(key) and canonical_key(key) != owned.key,
        )

    if key:
        canonical = canonical_key(key)
        if not canonical:
            return Anchor(
                key=None,
                bpm=None,
                owned=False,
                display=query,
                unresolved=f"{key!r} is not a Camelot code between 1A and 12B",
            )
        return Anchor(
            key=canonical, bpm=bpm, owned=False, display=query, key_needs_confirming=True
        )

    if web_lookup is not None:
        derived = web_lookup("", query) or {}
        canonical = canonical_key(str(derived.get("key") or ""))
        if canonical:
            return Anchor(
                key=canonical,
                bpm=_as_float(derived.get("bpm")),
                owned=False,
                display=query,
                key_needs_confirming=True,
            )

    return Anchor(
        key=None,
        bpm=None,
        owned=False,
        display=query,
        unresolved=(
            "that anchor is not in your library, and no Camelot key was supplied "
            "for it; nothing here looks a key up on the web, so supply one"
        ),
    )


def _energy_order(scored: Scored) -> tuple[bool, int]:
    """Sort a run by energy, with unknown energy last.

    Unknown last rather than treated as zero: a track with no reading is not a
    quiet track, and putting it at the bottom of a build-up would state something
    about it that nothing measured.
    """
    return (scored.track.energy is None, scored.track.energy or 0)


def _pick_side(ranked: Sequence[Scored], side: str, count: int) -> tuple[Scored, ...]:
    picks = [s for s in ranked if s.role == side]
    if len(picks) < count:
        chosen = {id(s) for s in picks}
        picks += [s for s in ranked if s.role == "either" and id(s) not in chosen]
    return tuple(sorted(picks[:count], key=_energy_order))


def build_plan(
    ranked: Sequence[Scored],
    anchor: Anchor,
    *,
    count: int | None = None,
    role: str | None = None,
) -> SetPlan:
    """Compose the ranked pool and one suggested sequence.

    ``role`` narrows the answer to one side of the anchor. ``either`` entries are
    included on whichever side is asked for, because a candidate whose role could
    not be decided is a legitimate pick for both, not for neither.

    BUT IT IS PLAYED ONCE. With both sides asked for, the after side draws from
    what the before side left, so an ``either`` filler cannot be placed on both
    sides of the anchor. Without that, one same-key companion of equal energy
    was the whole sequence twice, and an unowned anchor, whose companions all
    carry an unknown energy relative to it, hit that on most runs (U98).
    """
    if role in ("before", "after"):
        pool = tuple(s for s in ranked if s.role in (role, "either"))
        sequence = _pick_side(ranked, role, count or DEFAULT_SIDE)
    else:
        pool = tuple(ranked)
        before = _pick_side(ranked, "before", DEFAULT_SIDE)
        taken = {id(s) for s in before}
        sequence = before + _pick_side(
            [s for s in ranked if id(s) not in taken], "after", DEFAULT_SIDE
        )
    return SetPlan(anchor=anchor, pool=pool[: count or DEFAULT_POOL], sequence=sequence)


def build_set(
    query: str,
    index: Sequence[Track],
    *,
    taxonomy: Taxonomy,
    key: str | None = None,
    bpm: float | None = None,
    count: int | None = None,
    role: str | None = None,
    width: float = DEFAULT_BPM_WIDTH,
    weights: Weights = DEFAULT_WEIGHTS,
    vox_threshold: float | None = None,
    web_lookup: WebKeyLookup | None = None,
) -> SetPlan:
    """The whole engine over a prepared index. No input, no output, no network.

    Taking the index as an argument rather than building one is what makes this
    testable and what makes it honest: the scan is the only part that touches a
    disk, so keeping it outside means every ranking decision can be exercised
    against synthetic tracks in microseconds.
    """
    anchor = resolve_anchor(query, index, key=key, bpm=bpm, web_lookup=web_lookup)
    if anchor.key is None:
        return SetPlan(anchor=anchor)
    pool = build_pool(anchor, index, width=width)
    ranked = rank(
        pool,
        anchor,
        taxonomy=taxonomy,
        width=width,
        weights=weights,
        vox_threshold=vox_threshold,
    )
    return build_plan(ranked, anchor, count=count, role=role)


# ---------------------------------------------------------------------------
# Structured output (R32). Rendering stays with the CLI.
# ---------------------------------------------------------------------------

#: Bumped whenever a field is removed or its meaning changes, so a consumer can
#: refuse rather than silently reading a field that now means something else.
PAYLOAD_VERSION = 1


def as_payload(plan: SetPlan) -> dict:
    """The plan as plain data, for the CLI's structured output mode.

    Data only: no colour, no column widths, no sentence. R32 keeps human
    rendering separate, and the separation only holds if the structured half
    never acquires a rendering decision.

    THE TEMPO FIELD IS CALLED ``tempo``, NOT ``bpm``, AND THAT IS AN R17
    DECISION RATHER THAN A MATTER OF TASTE. ``bpm`` is the literal tag key in
    the Vorbis dialect and one letter from the MP4 atom, so a mapping spelled
    that way is one copy-paste from being handed to a tag writer, and a tempo
    tag reaches rekordbox on import exactly as a grid element does. The
    invariant guard treats any mapping carrying that key as a violation and it
    is right to: the cost of being wrong is a grid seeded at half or double
    time, which moves every cue point the user has ever set. The dataclass
    attribute keeps the domain word, because an attribute cannot be splatted
    into a tag call; the serialized KEY does not.
    """
    return {
        "payload_version": PAYLOAD_VERSION,
        "anchor": {
            "display": plan.anchor.display,
            "key": plan.anchor.key,
            "tempo": plan.anchor.bpm,
            "owned": plan.anchor.owned,
            "key_needs_confirming": plan.anchor.key_needs_confirming,
            "unresolved": plan.anchor.unresolved,
        },
        "pool": [_scored_payload(s) for s in plan.pool],
        "sequence": [_scored_payload(s) for s in plan.sequence],
    }


def _scored_payload(scored: Scored) -> dict:
    return {
        "artist": scored.track.artist,
        "title": scored.track.title,
        "key": scored.track.key,
        # See as_payload: the serialized key avoids the tag spelling on purpose.
        "tempo": scored.track.bpm,
        "genre": scored.track.genre,
        "energy": scored.track.energy,
        "vox": scored.track.vox,
        "path": scored.track.path,
        "tier": scored.tier,
        "role": scored.role,
        "score": round(scored.score, 6),
        "reason": scored.reason,
    }


__all__ = [
    "CACHE_VERSION",
    "CANDIDATE_LIMIT",
    "MATCH_THRESHOLD",
    "WORD_THRESHOLD",
    "DEFAULT_BPM_WIDTH",
    "DEFAULT_POOL",
    "DEFAULT_SIDE",
    "DEFAULT_WEIGHTS",
    "INDEX_FIELDS",
    "PAYLOAD_VERSION",
    "TIER_SCORE",
    "Anchor",
    "AnchorMatch",
    "Exclusion",
    "Scored",
    "SetPlan",
    "Track",
    "Weights",
    "as_payload",
    "assign_role",
    "bpm_score",
    "build_index",
    "build_plan",
    "build_pool",
    "build_set",
    "canonical_key",
    "compatible_keys",
    "energy_score",
    "find_in_index",
    "match_in_index",
    "harmonic_score",
    "in_band",
    "iter_audio",
    "match_key",
    "parse_entry",
    "rank",
    "read_index_tags",
    "resolve_anchor",
    "vocal_score",
]
