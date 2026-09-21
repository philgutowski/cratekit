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
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from rapidfuzz import fuzz, process

from cratekit.core import routing, tags
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
#: on a machine that had simply run an older build.
CACHE_VERSION = 2


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
FileLister = Callable[[Path], Iterable[Path]]


def read_index_tags(path: Path) -> dict[str, str | None]:
    """Read the index fields from one file through the shared tag reader.

    Every field goes through ``core.tags.read_tag``, which classifies the
    container once and reads the dialect's own key. A single unreadable file
    yields all-None rather than aborting the scan, which is safe here only
    because the caller asserts the mount precondition first: with the volume
    absent every file reads as untagged, and a whole library of untagged tracks
    is a perfectly valid input that produces a silently wrong answer.
    """
    return {name: tags.read_tag(path, name) for name in INDEX_FIELDS}


def iter_audio(root: Path) -> Iterator[Path]:
    """Every audio file under ``root``, in a stable order.

    Sorted, because the index order decides which of two duplicate works
    survives the collapse, and an unsorted walk would make that choice depend on
    the filesystem's mood.
    """
    suffixes = frozenset(AUDIO_EXTS)
    for candidate in sorted(root.rglob("*")):
        if candidate.suffix.lower() in suffixes:
            yield candidate


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
) -> tuple[Track, ...]:
    """Scan ``root`` and return the deduplicated index, in walk order.

    ``cache_path`` defaults to None, meaning NO CACHE, and there is deliberately
    no fallback path. The cache is a declared state file
    (``setbuilder_index_cache``) that the caller resolves through the state
    inventory; a module that composed its own path under a state root would
    create a file nothing walking that inventory can find, snapshot, or clear.
    None is what a test wants and what a one-off run can afford.

    The cache is keyed on path AND modification time, so an edited file
    invalidates only itself. THE WHOLE CACHE IS ALSO STAMPED WITH THE TEMPLATE it
    was parsed under, because a cached entry is the OUTPUT of a parse and the
    template is that parse's other input: a changed lossy marker alters every
    marked file's clean title and match key while touching no file's
    modification time, so without the stamp the old titles would be served for
    ever. A stamp that differs discards the cache, at the cost of one scan. A file whose parse yielded nothing is cached as
    nothing: without that, every keyless file in the library is re-read on every
    run, which is the majority of the cost on a library with unanalyzed corners.

    A cache write failure is logged and swallowed. The cache is an optimization,
    and refusing to produce a set because a cache could not be written would turn
    a performance feature into an outage.
    """
    root = Path(root)
    files = list(lister(root))
    stamp = _template_stamp(template)
    cached = _load_cache(cache_path, stamp)

    fresh: dict[str, dict] = {}
    tracks: list[Track] = []
    seen: set[str] = set()
    for path in files:
        key = str(path)
        try:
            mtime = path.stat().st_mtime
        except OSError:
            mtime = 0.0
        entry = cached.get(key)
        if entry is not None and entry.get("mtime") == mtime:
            track = _track_from_cache(entry.get("track"))
        else:
            track = parse_entry(reader(path), path=key, template=template)
        fresh[key] = {"mtime": mtime, "track": asdict(track) if track else None}
        if track is None or not track.match or track.match in seen:
            continue
        seen.add(track.match)
        tracks.append(track)

    _save_cache(cache_path, fresh, stamp)
    return tuple(tracks)


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
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(
            json.dumps(
                {"cache_version": CACHE_VERSION, "template": stamp, "entries": dict(entries)}
            ),
            encoding="utf-8",
        )
    except OSError as exc:
        log.debug("set-builder index cache not written to %s: %s", cache_path, exc)


def _track_from_cache(raw: object) -> Track | None:
    if not isinstance(raw, dict):
        return None
    try:
        return Track(**raw)
    except TypeError:
        return None


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

    ONE HIT IS STILL REFUSED WHEN THE QUERY NAMES MORE THAN THE HIT HOLDS. A
    person who types "Anchor Work (Extended Mix)" against a library holding only
    "Anchor Work" named a version the library does not have, and the subset score
    is 100 in that direction too. Typing LESS than the title is remembering;
    typing MORE is naming something else.

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
    if len(ordered) == 1 and not set(ordered[0].match.split()) < set(wanted.split()):
        return AnchorMatch(track=ordered[0])
    return AnchorMatch(candidates=ordered)


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
    if matched.track is None and matched.candidates:
        # REACHED AND NOT CHOSEN, which is neither of the answers below. Falling
        # through would call an owned track unowned: with a key it would rank
        # the library's own copies as companions to themselves, and without one
        # it would say "not in your library" about a name that hit several.
        named = "; ".join(t.display for t in matched.candidates[:CANDIDATE_LIMIT])
        return Anchor(
            key=None,
            bpm=None,
            owned=False,
            display=query,
            unresolved=(
                f"that anchor names more than one owned track, or a longer "
                f"version of one, and picking for you would build a set around "
                f"the wrong one: {named}"
            ),
        )
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
    "DEFAULT_BPM_WIDTH",
    "DEFAULT_POOL",
    "DEFAULT_SIDE",
    "DEFAULT_WEIGHTS",
    "INDEX_FIELDS",
    "PAYLOAD_VERSION",
    "TIER_SCORE",
    "Anchor",
    "AnchorMatch",
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
