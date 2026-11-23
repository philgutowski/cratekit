"""The taxonomy's model: its constants and the frozen classes a template builds into.

Split from :mod:`cratekit.core.taxonomy` (U299), which re-exports every name
here; read and build a taxonomy through that module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence

# A stable identifier: lowercase snake, compared and persisted, never rendered.
# Enforced so a display name cannot pose as an id and orphan state on rename (R19).
_ID = re.compile(r"^[a-z][a-z0-9_]*$")

SUPPORTED_SCHEMA_VERSIONS = frozenset({1, 2, 3, 4, 5})

# The schema version a template must state to declare a former place (R-797).
# An older build ignores the unknown key and would file tracks still sitting in
# the old playlist, so the declaration is tied to a version it refuses by name.
FORMER_PLACE_SCHEMA_VERSION = 2

# The schema version needed to declare a split place (U118), for the same reason.
SPLIT_PLACE_SCHEMA_VERSION = 3

# The schema version needed to declare a sub class derived from a playlist
# (U119), so a build knowing only the vocal signal refuses rather than misreads it.
PLAYLIST_SIGNAL_SCHEMA_VERSION = 4

# The schema version needed to declare a genre sub (U155), for the same reason.
GENRE_SUB_SCHEMA_VERSION = 5

# What a derived sub class is derived from (U119): vocal prominence against the
# calibrated cut, or another playlist's membership (the genre Favorites). One
# additive class per signal, since two would declare one dimension twice.
SIGNAL_VOX = "vox"
SIGNAL_PLAYLIST = "playlist"
SIGNALS = frozenset({SIGNAL_VOX, SIGNAL_PLAYLIST})

# The sources whose words are read through a table of their own (R-799, U244,
# U245). Record shops are absent: the bucket aliases resolve their words. Any
# other name is refused at load, since a misspelled table would silently do
# nothing. The tagging package owns these names; a test pins the two equal.
VOCABULARY_SOURCES: tuple[str, ...] = ("deezer", "discogs", "cyanite")

# How many levels a routing tree may nest: root child, folder, sub-playlist
# (KTD14). Must equal ``cratekit.write.rbxml.TREE_DEPTH``, which imports this
# module, so a test pins the two equal.
SUPPORTED_TREE_DEPTH = 3

# How a shipped template is named on disk; the short name between is the
# identifier configuration records. Declared once so the walk and reader agree.
_TEMPLATE_PREFIX = "taxonomy."
_TEMPLATE_SUFFIX = ".toml"

# The packaged default, read-only in the wheel. A library's active template is a
# copy in its own state root (S6), so a snapshot rolls it back with the database.
DEFAULT_TEMPLATE_NAME = "default"
DEFAULT_TEMPLATE = f"{_TEMPLATE_PREFIX}{DEFAULT_TEMPLATE_NAME}{_TEMPLATE_SUFFIX}"


class TaxonomyError(ValueError):
    """A template that cannot be trusted to route anything; carries every problem."""

    def __init__(self, problems: Sequence[str]) -> None:
        self.problems = tuple(problems)
        super().__init__("; ".join(self.problems))


class SubPolicy(str, Enum):
    """How automation may treat a sub-playlist.

    A manual sub is never written nor read as a move source. A derived sub is
    written by automation but is still never a move source, since moving a track
    out without re-deriving the signal drops the routing that put it there.
    """

    MANUAL = "manual"
    DERIVED = "derived"


@dataclass(frozen=True)
class Sub:
    """One sub-playlist. ``id`` is persisted, ``display`` is what rekordbox sees."""

    id: str
    display: str
    tag_aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class Band:
    """One energy band. ``max`` is an inclusive upper bound on the level scale."""

    id: str
    display: str
    max: int


@dataclass(frozen=True)
class RatingCut:
    """One step of the star curve. Deliberately independent of the band cuts."""

    max: int
    rating: int


@dataclass(frozen=True)
class BpmPrior:
    """A tempo detection window, on the bucket so a renamed folder keeps it.

    A window spanning a full octave folds nothing and defeats the prior.
    """

    start: float
    floor: float
    ceil: float


@dataclass(frozen=True)
class SubClass:
    """A sub-playlist that exists under many buckets and carries a write policy.

    ``signal`` is what a derived class is derived from; ``signal_playlist`` names
    a playlist class's source by display name, as it has no id of ours (U119).
    """

    id: str
    display: str
    policy: SubPolicy
    additive: bool = False
    present_in: str = "all_buckets"
    signal: str = SIGNAL_VOX
    signal_playlist: str = ""


@dataclass(frozen=True)
class BucketEnergy:
    """A bucket's energy settings; ``band_display`` relabels a band, never its cut."""

    enabled: bool = True
    band_display: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SubBySource:
    """A bucket that routes by source genre instead of energy; ``default`` is explicit."""

    default: str
    map: Mapping[str, str]


@dataclass(frozen=True)
class FormerPlace:
    """A playlist a bucket's tracks were filed in before the bucket had its folder.

    Declared so it competes as one of the declaring bucket's subs (R-797).
    ``id`` is its competing id, ``bucket`` the bucket whose folder holds it,
    ``sub`` the id it had there, ``display`` its name. It is only ever left:
    no resolver answers with one, and it may not name a live place.
    """

    id: str
    bucket: str
    sub: str
    display: str


@dataclass(frozen=True)
class SplitPlace:
    """A band of another bucket that this bucket's tracks still sit in (U118).

    The holder still files into it, so only tracks whose genre names the
    declaring bucket leave it, and it competes in the declaring bucket only.
    ``id`` is its competing id, ``bucket`` the holder, ``sub`` the band's id
    there (or the holder's former place), ``display`` the holder's name for
    it. It is only ever left: no resolver answers with one.
    """

    id: str
    bucket: str
    sub: str
    display: str


@dataclass(frozen=True)
class GenreSub:
    """A sub of an energy bucket chosen by the track's source genre (U155).

    Additive beside the bands, unlike ``sub_by_source``: it never competes and
    nothing is moved out of it within its bucket; a track whose genre ``tag
    set`` moved to another bucket leaves it with the band (R-1965). ``sources`` are exact routing aliases of the
    bucket; the first is the word the tagger writes for the sub.
    """

    id: str
    display: str
    sources: tuple[str, ...]


@dataclass(frozen=True)
class Bucket:
    """One folder in the tree, with everything that varies about it declared."""

    id: str
    display: str
    family: str | None = None
    bpm: BpmPrior | None = None
    aliases: tuple[str, ...] = ()
    tag_aliases: tuple[str, ...] = ()
    subs: tuple[Sub, ...] = ()
    energy: BucketEnergy = field(default_factory=BucketEnergy)
    single_sub: Sub | None = None
    sub_by_source: SubBySource | None = None
    rates: bool = True
    formerly: tuple[FormerPlace, ...] = ()
    split_from: tuple[SplitPlace, ...] = ()
    genre_subs: tuple[GenreSub, ...] = ()


@dataclass(frozen=True)
class FuzzyRule:
    """One ordered keyword rule for routing. First match wins."""

    keyword: str
    bucket: str


@dataclass(frozen=True)
class Split:
    """The one tagging rule that reads tempo."""

    when_contains: str
    max_bpm: float
    below: str
    at_or_above: str
    unknown_bpm: str
    unknown_bpm_needs_review: bool = True


@dataclass(frozen=True)
class SuggestRule:
    """One ordered tagging rule.

    The match kind decides when it runs: ``equals`` runs before the alias
    lookup, ``all_of`` and ``any_of`` (substring guesses) after it, so a rule
    can refuse a catch-all without refusing every sub-genre containing it.
    """

    equals: tuple[str, ...] = ()
    all_of: tuple[str, ...] = ()
    any_of: tuple[str, ...] = ()
    bucket: str | None = None
    tag: str | None = None
    decline: str | None = None
    split: Split | None = None


@dataclass(frozen=True)
class GateRule:
    """One ordered acquisition-gate rule over the source vocabulary."""

    all_of: tuple[str, ...] = ()
    any_of: tuple[str, ...] = ()
    equals: tuple[str, ...] = ()
    family: str | None = None
    keep: bool = False


#: The label kind that passes every release and asks the catalogue nothing.
#: Reserved: no published rule may name it, or a word could be "of any kind".
ANY_KIND = "any"

#: What a followed label is taken to be when its entry names no kind, and no
#: ``default_kind`` is declared.
DEFAULT_LABEL_KIND = "dance"

#: The word that clears a label's kind, so it follows ``default_kind`` again.
#: Reserved like :data:`ANY_KIND`, since marking with it means "none".
NO_KIND = "default"

#: The shape of a kind's name, once folded: one word. Shared with the registry,
#: so a rule cannot name a kind no label could ever be marked with.
KIND_NAME = re.compile(r"[a-z0-9][a-z0-9_-]*")


@dataclass(frozen=True)
class PublishedRule:
    """One ordered rule saying what kind of music a general catalogue's word is.

    Matchers as in :class:`GateRule`, lowercase, over catalogue words (R-798).
    """

    kind: str
    all_of: tuple[str, ...] = ()
    any_of: tuple[str, ...] = ()
    equals: tuple[str, ...] = ()


@dataclass(frozen=True)
class LabelGate:
    rules: tuple[GateRule, ...] = ()
    out_of_place_share: float = 0.10
    #: The rules over the general catalogue's words, in declared order. Empty
    #: in a copy written before R-798, and then the gate judges no release.
    published: tuple[PublishedRule, ...] = ()
    #: The kind a followed label is when its registry entry names none.
    default_kind: str = DEFAULT_LABEL_KIND

    @property
    def kinds(self) -> tuple[str, ...]:
        """Every kind a published rule names, in first declared order."""
        return tuple(dict.fromkeys(rule.kind for rule in self.published))


@dataclass(frozen=True)
class VocabularyWord:
    """One word of a source's own vocabulary, and the genre written for it (R-799).

    ``word`` matches whole, ignoring case. ``bucket`` and ``sub`` are resolved
    from ``tag`` by the loader, never declared; ``sub`` is None for an energy bucket.
    """

    word: str
    tag: str
    bucket: str
    sub: str | None = None


@dataclass(frozen=True)
class Vocabulary:
    """Where each word of one source's vocabulary goes (R-799).

    Per source, since bucket aliases were written for record shop words. Asked
    first; a word with no row falls through to the aliases, but must still
    name a folder (:meth:`Taxonomy.named_folder`).
    """

    source: str
    words: tuple[VocabularyWord, ...] = ()


@dataclass(frozen=True)
class Energy:
    enabled: bool
    scale_max: int
    bands: tuple[Band, ...]
    rating_cuts: tuple[RatingCut, ...]
    no_energy_sub: Sub | None


@dataclass(frozen=True)
class Fallback:
    bucket: str
    routing_uses_fallback: bool
    tagging_uses_fallback: bool
    too_coarse_as_source: tuple[str, ...]


@dataclass(frozen=True)
class FamilyAffinity:
    same_genre: float
    same_family: float
    same_supergroup: float
    unrelated: float
    unknown_anchor: float
    supergroup: Mapping[str, str]
    # The family that means "nothing in common", so sharing it earns no affinity.
    catch_all: str | None = None


@dataclass(frozen=True)
class Node:
    """A named place in the tree that is not a bucket: the root, the intake flow."""

    id: str
    display: str


#: The threshold for a set rather than a track, twenty minutes, used when a
#: template declares the long track playlist without one.
DEFAULT_LONG_TRACK_SECONDS = 1200


@dataclass(frozen=True)
class LongTracks:
    """The root playlist of every collection track strictly over ``over_seconds``."""

    id: str
    display: str
    over_seconds: int = DEFAULT_LONG_TRACK_SECONDS


@dataclass(frozen=True)
class Taxonomy:
    """A validated, self-consistent taxonomy. Immutable, and safe to share."""

    schema_version: int
    tree: Node
    tree_depth: int
    intake: Node
    buckets: tuple[Bucket, ...]
    energy: Energy
    fallback: Fallback
    sub_classes: tuple[SubClass, ...]
    fuzzy: tuple[FuzzyRule, ...]
    suggest: tuple[SuggestRule, ...]
    label_gate: LabelGate
    family: FamilyAffinity

    # The tree a whole-catalog import writes into: a folder per source, a
    # playlist per year. Here because R19 keeps every display name in the
    # template. Optional: the writer refuses by name rather than invent a folder
    # from a default nobody saw. The optional nodes below follow the same rule.
    catalog: Node | None = None

    # The root playlist that keeps sets apart from tracks.
    long_tracks: LongTracks | None = None

    # The intake folder a stale batch is rotated into (U111), ``INBOX / Old``.
    intake_old: Node | None = None

    # The root folder that keeps a set's playlist for good, never rotated (U121),
    # ``INSPIRATION`` in the shipped template.
    inspiration: Node | None = None

    # Per-source vocabularies (R-799), in declared order. Empty in an older copy,
    # where every word is resolved by the bucket aliases.
    vocabularies: tuple[Vocabulary, ...] = ()

    # Indexes derived once at construction, so they cannot disagree with it.
    _by_id: Mapping[str, Bucket] = field(repr=False, default_factory=dict)
    _by_display: Mapping[str, str] = field(repr=False, default_factory=dict)
    _routing_alias: Mapping[str, str] = field(repr=False, default_factory=dict)
    _tagging_alias: Mapping[str, tuple[str, str | None]] = field(
        repr=False, default_factory=dict
    )
    _former_places: Mapping[str, tuple[tuple[str, "FormerPlace"], ...]] = field(
        repr=False, default_factory=dict
    )
    _split_places: Mapping[str, tuple[tuple[str, "SplitPlace"], ...]] = field(
        repr=False, default_factory=dict
    )
    _vocabulary: Mapping[str, Mapping[str, VocabularyWord]] = field(
        repr=False, default_factory=dict
    )

    def vocabulary(self, source: str) -> Mapping[str, VocabularyWord] | None:
        """One source's own table, by lowercased word, or None when it has none.

        None and an empty table differ: an empty table answers no word but still
        imposes the rule that a genre written from that source names a folder.
        """
        return self._vocabulary.get(source)

    def named_folder(self, genre: str) -> tuple[str, str | None] | None:
        """The place a written genre names by an exact declaration, or None.

        The bucket and, in a bucket that files by source genre, the style sub.
        None for a keyword or fallback match, a too coarse genre, or such a
        bucket's bare name or default sub word. The same test the loader puts
        to a vocabulary row's tag.
        """
        place, _problem = _tag_place(
            genre, self._by_id, self._by_display, self._routing_alias, self.fallback
        )
        return place

    def former_places(self, bucket_id: str) -> tuple[tuple[str, "FormerPlace"], ...]:
        """Every former place one bucket declares or holds, with its declarer."""
        return self._former_places.get(bucket_id, ())

    def split_places(self, bucket_id: str) -> tuple[tuple[str, "SplitPlace"], ...]:
        """Every split place one bucket declares or holds, with its declarer.

        Both sides, though it competes only where declared: the move reads the
        holder's side to know the declaring bucket settles that band.
        """
        return self._split_places.get(bucket_id, ())

    def bucket(self, bucket_id: str) -> Bucket:
        try:
            return self._by_id[bucket_id]
        except KeyError:
            raise KeyError(
                f"no bucket declared with id {bucket_id!r}; "
                f"declared ids are {sorted(self._by_id)}"
            ) from None

    def bucket_ids(self) -> tuple[str, ...]:
        return tuple(b.id for b in self.buckets)

    def sub_class(self, sub_class_id: str) -> SubClass:
        for entry in self.sub_classes:
            if entry.id == sub_class_id:
                return entry
        raise KeyError(f"no sub_class declared with id {sub_class_id!r}")

    def routing_alias(self, source_genre: str) -> str | None:
        """The bucket a source string is declared to route to, exactly, case included."""
        return self._routing_alias.get(source_genre)

    def bucket_for_display(self, display: str) -> str | None:
        """The bucket whose display name is exactly ``display``, if any.

        A lookup from a display name, not a record keyed by one (R19). Buckets
        only and exact, so a sub's display cannot place a track one level up;
        ``suggest_tag``'s last tier relies on that to know routing will place
        the word where the template says (R-650).
        """
        return self._by_display.get(display)

    def tagging_alias(self, lowered_source_genre: str) -> tuple[str, str | None] | None:
        """The (bucket id, sub id) a source string tags as; case insensitive."""
        return self._tagging_alias.get(lowered_source_genre)

    def buckets_without_bpm_prior(self) -> tuple[str, ...]:
        """Buckets with no tempo window, so a caller can refuse by name, not default."""
        return tuple(b.id for b in self.buckets if b.bpm is None)

    def is_too_coarse_as_source(self, value: str) -> bool:
        """Whether a source string is too coarse to accept as a final genre tag."""
        return (value or "").strip() in self.fallback.too_coarse_as_source


#: Top level folder names another app owns in rekordbox's tree (U185), which a
#: declared tree may not take; :mod:`cratekit.core.foreign_tree` reads it.
FOREIGN_ROOT_NAMES: frozenset[str] = frozenset({"DEADCA7"})


def _tag_place(
    tag: str,
    by_id: Mapping[str, Bucket],
    by_display: Mapping[str, str],
    routing_alias: Mapping[str, str],
    fallback: Fallback,
) -> tuple[tuple[str, str | None] | None, str]:
    """The place routing files one written genre in, or why it names no folder.

    The first two tiers of ``routing.resolve_bucket`` only, an exact routing
    alias or a bucket's own name, since a keyword guess or the fallback would
    write a genre with no folder. Spelled here because routing imports this
    module; a test holds it to routing's answer.

    In a bucket that files by source genre the tag needs its own row in the
    map, or it lands in the default sub with its word lost (R-799).
    """
    bucket_id = routing_alias.get(tag) or by_display.get(tag)
    bucket = by_id.get(bucket_id or "")
    if bucket is None:
        return None, (
            f"tag {tag!r} is filed by no exact declaration: it is neither a "
            f"routing alias nor a bucket's own name, so routing would guess at "
            f"it or leave it in the fallback"
        )
    if tag in fallback.too_coarse_as_source:
        return None, (
            f"tag {tag!r} is one this taxonomy lists as too coarse to be a final genre"
        )
    if bucket.sub_by_source is None:
        return (bucket.id, None), ""
    sub = bucket.sub_by_source.map.get(tag)
    if sub is None:
        return None, (
            f"tag {tag!r} files under {bucket.display!r} with no row of its own "
            f"in that bucket's sub_by_source map, so it would land in the default "
            f"sub {bucket.sub_by_source.default!r} and the word naming its folder "
            f"would be lost; write a genre the map lists"
        )
    return (bucket.id, sub), ""
