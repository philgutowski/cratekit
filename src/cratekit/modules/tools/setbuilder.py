"""The library grounded set builder (Feature Inventory row 29).

Give it an anchor track and it returns owned tracks that mix with it, ranked and
sequenced, from the library's own analyzed tags alone: no network call, no
adapter, no write, so the same anchor over the same files gives the same answer.

Index membership IS ownership. The pool is filtered from the index, ranked, and
the sequence drawn from the ranking, so nothing that is not on disk can be
recommended. The index reads files rather than an export because energy and
vocal prominence live only in the tags, tempo lives in the title head (nothing
here writes a tempo tag, R17), and an export lags a fresh import.

The Camelot parser is the shared, bounded one; the head is parsed from the
declared name template; genre affinity comes from the declared taxonomy (R19);
the vocal threshold is a parameter (D7). An unowned anchor is never looked up on
the web: a caller may inject a lookup, and without one it asks for a key.
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

#: The tag fields the index reads, all through ``core.tags``'s one reader, so
#: this module never opens an audio file itself.
INDEX_FIELDS: tuple[str, ...] = (
    "title",
    "artist",
    "genre",
    "initialkey",
    "energylevel",
    "voxlevel",
    "voxgender",
)

#: Cache format. Bumped when :class:`Track` changes shape, AND when the parse
#: that fills one changes (``match_key``, the head or Camelot parser): a changed
#: parse touches no file's modification time, so nothing else retires old answers.
#: 3: an entry carries the file's size and its modification time in nanoseconds.
CACHE_VERSION = 3


# The types


@dataclass(frozen=True, slots=True)
class Track:
    """One owned track and the five signals the ranker uses.

    ``key`` is canonical Camelot (``2A``, ``12B``). None means UNKNOWN throughout
    and scores neutrally; a track with no energy reading is not a quiet track.
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

    An unowned anchor carries a supplied key and tempo and no ``track``, so its
    genre, energy and vocal signals score neutral.
    """

    key: str | None
    bpm: float | None
    owned: bool
    track: Track | None = None
    display: str = ""
    #: True when the key did not come from the library's own analysis, so the
    #: caller must show it before the picks are trusted.
    key_needs_confirming: bool = False
    #: Why the anchor could not be resolved: an ordinary answer, not an exception.
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
    """Ranking weights, summing to one; a value so two rankings can differ in one process."""

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


# Identity and normalization


def canonical_key(code: str | None) -> str:
    """Canonical unpadded Camelot, or "" when the code is not on the wheel.

    A track whose key cannot be placed cannot be ranked, so "" keeps it out of
    the index.
    """
    parsed = parse_camelot(code or "")
    if parsed is None:
        return ""
    number, letter = parsed
    return f"{number}{letter}"


def match_key(artist: str, title: str) -> str:
    """The comparison form for anchor lookup and duplicate collapse.

    Lowercased, punctuation stripped, whitespace collapsed. Not the version
    identity a match uses: being wrong here costs one duplicate line, not a file.
    """
    text = f"{artist} {title}".lower()
    kept = [c if c.isalnum() or c.isspace() else " " for c in text]
    return " ".join("".join(kept).split())


# The index

TagReader = Callable[[Path], Mapping[str, str | None]]
FileLister = Callable[[Path, Sequence[Path]], Iterable[Path]]


def read_index_tags(path: Path) -> dict[str, str | None]:
    """Read the index fields from one file through ONE container open.

    An absent, undecodable or unreadable field reads as None, exactly as
    ``core.tags.read_tag`` answers it. A wholly unreadable file yields all None
    rather than aborting the scan, which is safe only because the caller checks
    the mount first.
    """
    return tags.read_tags(path, INDEX_FIELDS)


def iter_audio(root: Path, exclude: Iterable[Path] = ()) -> Iterator[Path]:
    """Every audio file under ``root``, sorted, less the ``exclude`` folders.

    Sorted because the order decides which duplicate survives the collapse.
    ``exclude`` names folders under the library that are not its own music (the
    state folder and the download staging folder), matched by :class:`Exclusion`
    as directories, never by name, and pruned rather than walked. Everything else
    is yielded as ``sorted(root.rglob("*"))`` yields it.
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
    """The folders under a root the index leaves out, BY LOCATION.

    A path is not an identity (symlinked mounts, ``..``, letter case, a deeper
    folder sharing a name), so each configured folder is read once as its device
    and inode. ``folders`` maps each to the configured path a refusal names;
    ``ancestors`` holds the directories between the root and an excluded folder,
    the only ones walked by hand. A folder that is missing, is the root, holds
    it, or sits outside it excludes nothing.
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

        Like ``rglob``: every entry of every directory reached, descending into
        real directories only, passing over what cannot be listed.
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

        Read up the path's folders as directories, so a spelling through a link
        is placed where it really is.
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

    Empty unless ``folder`` is a directory strictly under ``top``; read on the
    resolved path and compared by identity.
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
    """Build a :class:`Track` from a tag mapping, or None without a Camelot key.

    The key comes from the ``initialkey`` tag, which the analysis wrote, falling
    back to the name head a renamer wrote from it; tempo and clean title come
    from the head.
    """
    raw_title = (raw.get("title") or "").strip()
    head, remainder = split_head(raw_title, template=template)
    head_fields = parse_head(raw_title, template=template) or {}
    clean_title = remainder.strip() if head else raw_title
    key = canonical_key(raw.get("initialkey") or head_fields.get("key"))
    if not key:
        return None
    artist = (raw.get("artist") or "").strip()
    return Track(
        artist=artist,
        title=clean_title,
        key=key,
        bpm=_as_float(head_fields.get("bpm")),
        genre=(raw.get("genre") or "").strip(),
        energy=_as_int(raw.get("energylevel")),
        vox=_as_int(raw.get("voxlevel")),
        voxgender=(raw.get("voxgender") or "").strip() or None,
        match=match_key(artist, clean_title),
        path=path,
    )


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

    ``cache_path`` None means no cache, with no fallback: the cache is the
    declared state file ``setbuilder_index_cache``, which the caller resolves.
    An entry is keyed on path, nanosecond modification time AND size (restore
    tools keep the old time over new bytes), and the whole cache is stamped with
    the template it was parsed under, since a changed template changes titles
    without touching a file.

    A parse that yielded nothing is cached as nothing, but a read with no field
    at all is not cached: it cannot be told from an I/O error on an external
    volume. Nothing is written when the walk found no file, since that is what
    an unmounted volume's mountpoint looks like. A failed cache write is logged
    and swallowed. ``exclude`` is handed to the lister, so an entry cached under
    an excluded folder is never served and is dropped on the next write.
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

    Every comparison checks TYPE too: the cache syncs, and a hand edit or a
    conflict copy can hold any JSON. An untrusted entry costs one read.
    """
    return (
        isinstance(entry, dict)
        and entry.get("mtime_ns") == identity["mtime_ns"]
        and entry.get("size") == identity["size"]
        and (entry.get("track") is None or _track_from_cache(entry.get("track")) is not None)
    )


def _template_stamp(template: NameTemplate) -> str:
    """The template as a string equal exactly when the template is.

    Field by field rather than ``repr``, because a frozenset's repr follows
    string hashing and would differ between runs, discarding the cache each time.
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
        # Renamed into place, so a killed run leaves the old cache or the new one.
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
    # Right names with wrong types construct fine and fail later, in the ranking.
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


# Harmony: the Camelot wheel and the tempo band


def _wrap(number: int) -> int:
    return ((number - 1) % 12) + 1


def compatible_keys(anchor_key: str) -> dict[str, str]:
    """``{camelot: tier}`` for the anchor. The perfect tier wins any overlap.

    Tiers relative to anchor ``nL`` (number n, letter L, other letter O):

        perfect  nL, (n+1)L, (n-1)L, nO     same key, either neighbour, relative
        boost    (n+2)L                     the energy lift
        wider    (n-2)L, (n+3)L, (n-1)O, (n+1)O   diagonals, used sparingly

    Assigned widest first so the narrower tiers overwrite them.
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
    """True when the candidate sits within ``width`` of the anchor, its half, or its double.

    An anchor with no tempo drops the constraint (a key only pool); a candidate
    with no tempo is excluded when the anchor has one, as untested.
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

    The anchor is excluded by match key, not path, so a second copy of it does
    not come back as its own best companion.
    """
    tiers = compatible_keys(anchor.key or "")
    anchor_match = anchor.track.match if anchor.track else None
    out: list[tuple[Track, str]] = []
    for track in index:
        if anchor_match and track.match == anchor_match:
            continue
        tier = tiers.get(track.key)
        if tier is not None and in_band(track.bpm, anchor.bpm, width=width):
            out.append((track, tier))
    return tuple(out)


# Ranking


def harmonic_score(tier: str) -> float:
    return TIER_SCORE.get(tier, 0.0)


def bpm_score(
    candidate: float | None,
    anchor: float | None,
    *,
    width: float = DEFAULT_BPM_WIDTH,
) -> float:
    """Proximity to the nearest of the anchor, its half, or its double; neutral when unknown."""
    if candidate is None or anchor is None:
        return 0.5
    distance = min(abs(candidate - r) for r in (anchor, anchor / 2, anchor * 2))
    return max(0.0, 1.0 - distance / width)


def energy_score(candidate: int | None, anchor: int | None, role: str) -> float:
    """Role aware energy fit, neutral when either reading is unknown.

    ``before`` rewards equal or lower, ``after`` equal or higher, ``either``
    closeness; the divisor is the usable span of the 1 to 10 scale.
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
    """Penalize a vocal forward companion beside a vocal forward anchor.

    The threshold is passed in (D7) so the ranker imports no analysis module; an
    absent one scores neutral high.
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
    """Where the candidate sits relative to the anchor: energy first, then the wheel.

    ``either`` when neither resolves; the sequence uses those as filler.
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

    ``taxonomy`` is a parameter (KTD23, R19). Ties break on the match key, so the
    order is the same on every run.
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
        reason = _reason(track, tier, anchor, role, affinity)
        scored.append(Scored(track=track, tier=tier, role=role, score=score, reason=reason))
    scored.sort(key=lambda s: (-s.score, s.track.match))
    return tuple(scored)


# Anchor resolution and the sequence

WebKeyLookup = Callable[[str, str], Mapping[str, object] | None]


#: How close a typed anchor must be to an index entry to count as it. High: a
#: set around the WRONG anchor looks right and is worse than a refusal.
MATCH_THRESHOLD = 90

#: How many candidates a refusal names; a listing nobody can read is no remedy.
CANDIDATE_LIMIT = 10

#: How close one typed WORD must be to a title word: "anchr" lands on "anchor",
#: while "extended" on "original", "club" on "dub", "remix" on "mix" fall under.
WORD_THRESHOLD = 80


@dataclass(frozen=True, slots=True)
class AnchorMatch:
    """What a typed anchor names in the index: one track, several, or nothing.

    ``track`` set is a resolution; ``track`` None with ``candidates`` is a
    refusal that knows why (several owned tracks reached, none chosen); both
    empty is an ordinary absence. The middle answer must never fold into either
    neighbour (R-187).
    """

    track: Track | None = None
    #: The owned tracks the name reached, best score first, when none was chosen.
    candidates: tuple[Track, ...] = ()
    #: True when NO candidate holds every word of the name: the person named a
    #: version, remix or credit the library's copies do not carry.
    partial: bool = False


def match_in_index(
    query: str, index: Sequence[Track], *, threshold: int = MATCH_THRESHOLD
) -> AnchorMatch:
    """Resolve ``query`` against the index, refusing rather than guessing.

    An exact hit on the comparison key wins outright: ``token_set_ratio`` scores
    a subset at 100, so no threshold separates a title from its extended mix.
    Then every fuzzy hit at the threshold is collected, and a hit counts only
    when it holds every typed word, give or take a slip. One such hit resolves;
    several are a question for the person; hits that all lack part of the name
    come back ``partial``. Candidates order by score, match key and path.
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
    """The one track ``query`` names, or None for no match and for several alike."""
    return match_in_index(query, index, threshold=threshold).track


def _unresolved(query: str, why: str) -> Anchor:
    return Anchor(key=None, bpm=None, owned=False, display=query, unresolved=why)


def resolve_anchor(
    query: str,
    index: Sequence[Track],
    *,
    key: str | None = None,
    bpm: float | None = None,
    web_lookup: WebKeyLookup | None = None,
) -> Anchor:
    """Resolve the anchor against the library, or against supplied values.

    Owned wins; a supplied key overrides the library's only because the person
    saw the disagreement. An unowned anchor with no key and no injected lookup
    is unresolved, never guessed.
    """
    matched = match_in_index(query, index)
    # A partial reach with a supplied key is the unowned answer, and falls
    # through to it: "should I buy this" about a version the library lacks.
    if matched.track is None and matched.candidates and not (matched.partial and key):
        # Reached and not chosen: falling through would call an owned track unowned.
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
        return _unresolved(query, why)
    owned = matched.track
    if owned is not None:
        return Anchor(
            key=canonical_key(key) or owned.key,
            bpm=bpm if bpm is not None else owned.bpm,
            owned=True,
            track=owned,
            display=owned.display,
            key_needs_confirming=bool(key) and canonical_key(key) != owned.key,
        )

    if key:
        canonical = canonical_key(key)
        if not canonical:
            return _unresolved(query, f"{key!r} is not a Camelot code between 1A and 12B")
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

    return _unresolved(
        query,
        "that anchor is not in your library, and no Camelot key was supplied "
        "for it; nothing here looks a key up on the web, so supply one",
    )


def _energy_order(scored: Scored) -> tuple[bool, int]:
    """Sort a run by energy, unknown last: no reading is not a quiet track."""
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

    ``role`` narrows the answer to one side; ``either`` entries count for any
    side asked for. With both sides, the after side draws from what the before
    side left, so one ``either`` filler is never placed on both sides.
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
    """The whole engine over a prepared index. No input, no output, no network."""
    anchor = resolve_anchor(query, index, key=key, bpm=bpm, web_lookup=web_lookup)
    if anchor.key is None:
        return SetPlan(anchor=anchor)
    pool = build_pool(anchor, index, width=width)
    ranked = rank(
        pool, anchor, taxonomy=taxonomy, width=width, weights=weights, vox_threshold=vox_threshold
    )
    return build_plan(ranked, anchor, count=count, role=role)


# Structured output (R32). Rendering stays with the CLI.

#: Bumped whenever a field is removed or its meaning changes.
PAYLOAD_VERSION = 1


def as_payload(plan: SetPlan) -> dict:
    """The plan as plain data, with no rendering decision in it.

    The tempo field is ``tempo``, never ``bpm`` (R17): ``bpm`` is a tag key, so a
    mapping spelled that way is one paste from a tag writer, and a tempo tag
    seeds a beat grid in rekordbox. The invariant guard rejects any such mapping.
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
    "CACHE_VERSION", "CANDIDATE_LIMIT", "MATCH_THRESHOLD", "WORD_THRESHOLD",
    "DEFAULT_BPM_WIDTH", "DEFAULT_POOL", "DEFAULT_SIDE", "DEFAULT_WEIGHTS", "INDEX_FIELDS",
    "PAYLOAD_VERSION", "TIER_SCORE", "Anchor", "AnchorMatch", "Exclusion", "Scored", "SetPlan",
    "Track", "Weights", "as_payload", "assign_role", "bpm_score", "build_index", "build_plan",
    "build_pool", "build_set", "canonical_key", "compatible_keys", "energy_score",
    "find_in_index", "match_in_index", "harmonic_score", "in_band", "iter_audio", "match_key",
    "parse_entry", "rank", "read_index_tags", "resolve_anchor", "vocal_score",
]
