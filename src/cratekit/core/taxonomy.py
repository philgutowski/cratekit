"""The declared taxonomy: one table, loaded and validated before anything routes.

WHY THIS MODULE EXISTS. The system this replaces spread one person's playlist
tree across eight genre resolvers, twelve energy mappings, four definitions of a
single sub-playlist name, and six inline copies of the bucket that catches
everything else. None of them shared a constant. Adding one genre meant editing
four tables and remembering the fifth, and the drift that produced was not
theoretical: two of those resolvers disagree today on strings the library
actually contains, and a third silently degrades tempo detection for anyone whose
folders are not named exactly like the author's.

KTD13 is the ordering rule that fixes it: consolidate FIRST, parameterise SECOND.
Parameterising five drifted copies would have preserved the drift in a config
file, where it is harder to see. So the drift was resolved against the live
library, and only the resolved result became declarable.

WHY IT TAKES NO CONFIGURATION. This module reads no configuration VALUE (KTD23,
seam decision S3). A resolver that reaches for global configuration cannot be
tested against two different taxonomies in one process, and proving that a
friend's differently-named tree routes correctly with no code change is exactly
the verification this unit owes. So a Taxonomy is a value the caller supplies,
and the only file this module reads is the read-only default that ships inside
the wheel.

The one thing it does import from ``core/config`` is a pure predicate over a
string, ``template_name_is_usable``, and the distinction is worth stating because
the sentence above used to say "imports none". Nothing is READ: no path is
resolved, no document is loaded, no global is consulted, and every function here
is still a function of its arguments. What the import buys is that the set of
template names this module OFFERS and the set configuration ACCEPTS are one set.
Spelling the rule twice is how a wizard comes to offer a name that validation
then refuses, which is the same two-answers-to-one-question defect the shared
walk below exists to close.

WHY VALIDATION HAPPENS AT LOAD. Every rule below fails at load time and again in
the setup wizard, never at write time. A friend whose template omits a tempo
prior should learn during setup, not three hours into their first intake with a
library half-written.
"""

from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass, field, replace
from enum import Enum
from importlib import resources
from typing import Any, Mapping, Sequence

from cratekit.core import config

# A stable identifier. Lowercase snake, because it is compared, persisted, and
# never rendered. The pattern is enforced rather than documented so that a
# template cannot smuggle a display name in as an id and re-orphan state on the
# next rename (R19).
_ID = re.compile(r"^[a-z][a-z0-9_]*$")

SUPPORTED_SCHEMA_VERSIONS = frozenset({1, 2, 3, 4, 5})

# The schema version a template has to state before it may declare a former
# place (R-797). A former place changes what competes, and a loader ignores a
# key it does not know. So a build older than this unit, handed a library's
# copy that declares one, would load it cleanly, see no competing place for the
# old playlist, and file every track into a band while it still sat there. The
# version is what such a build refuses by name, so the declaration is tied to
# it: version 1 with a former place is refused here, and version 2 is refused
# there.
FORMER_PLACE_SCHEMA_VERSION = 2

# The schema version a template has to state before it may declare a split
# place (U118), for the former place's reason: a build that reads version 2
# ignores the key, sees no competing place in the folder the genre left, and
# files every track into the new folder while it still sits in the old one.
SPLIT_PLACE_SCHEMA_VERSION = 3

# The schema version a template has to state before it may declare a sub class
# derived from a PLAYLIST (U119), the genre Favorites, for the same reason one
# version on: a build that reads version 3 refuses two additive classes by
# count, loudly, and a build that knows only one signal would otherwise read
# the second class as a vocal one and ask the rebuild to derive it from a
# reading it does not have.
PLAYLIST_SIGNAL_SCHEMA_VERSION = 4

# The schema version a template has to state before it may declare a genre sub
# (U155), for the former place's reason one version on: a build that reads
# version 4 ignores the key, routes a Rominimal track into its band alone, and
# reports the genre sub's playlist as one nobody declared. The version is what
# such a build refuses by name.
GENRE_SUB_SCHEMA_VERSION = 5

# What a derived sub class is derived FROM (U119). The vocal class reads the
# file's vocal prominence against the calibrated cut; a playlist class mirrors
# another playlist's membership into every genre folder, which is the genre
# Favorites. ONE additive class per signal: two classes on one signal would be
# one dimension declared twice.
SIGNAL_VOX = "vox"
SIGNAL_PLAYLIST = "playlist"
SIGNALS = frozenset({SIGNAL_VOX, SIGNAL_PLAYLIST})

# The sources whose words are read through a table of their own (R-799), by the
# name a file's record gives each. TWO: the general catalogue, and Discogs,
# whose collector styles are a vocabulary of their own (U244). The record shops
# asked by page are not here: their words are resolved by the buckets' aliases,
# which were written for them, and a table declared for one would be read by
# nothing. A name outside this tuple is refused at load for the same reason,
# since a misspelled table loads clean and changes nothing, with nothing said.
# The tagging package owns the names and cannot be imported from here, so the
# two are pinned equal by a test, as the tree depth below is.
VOCABULARY_SOURCES: tuple[str, ...] = ("deezer", "discogs")

# How many levels a declared routing tree may nest: a root child, a folder, and a
# sub-playlist (KTD14). Named here rather than written as a literal in the check
# and again in its message, because it is the SAME number the XML bridge's
# indentation encodes as ``cratekit.write.rbxml.TREE_DEPTH``. The bridge cannot
# be imported from here, since it imports this module, so the two are pinned
# equal by a test instead. One number in two files with nothing holding them
# together is how a template starts loading at a depth the writer cannot emit.
SUPPORTED_TREE_DEPTH = 3

# How a shipped template is named on disk. The short name between the two is the
# stable identifier configuration records, so both halves are declared once and
# the walk below and the reader below cannot disagree about which files count.
_TEMPLATE_PREFIX = "taxonomy."
_TEMPLATE_SUFFIX = ".toml"

# The name of the packaged default. Read-only data inside the wheel; a library's
# ACTIVE template is a copy in its own state root (seam decision S6), which is
# what lets one library be self-describing and lets a snapshot roll the taxonomy
# back alongside the database it describes.
DEFAULT_TEMPLATE_NAME = "default"
DEFAULT_TEMPLATE = f"{_TEMPLATE_PREFIX}{DEFAULT_TEMPLATE_NAME}{_TEMPLATE_SUFFIX}"


class TaxonomyError(ValueError):
    """A template that cannot be trusted to route anything.

    Carries EVERY problem, not the first. A friend fixing their template one
    error per run is a friend who gives up on the third run.
    """

    def __init__(self, problems: Sequence[str]) -> None:
        self.problems = tuple(problems)
        super().__init__("; ".join(self.problems))


class SubPolicy(str, Enum):
    """How automation is allowed to treat a sub-playlist.

    Two values rather than one "excluded" flag, and the distinction is the whole
    point. In the system this came from, five separate places excluded two subs
    from being touched, for two different reasons, using one shape. Collapsing
    them loses the reason, and the reason is what stops the bug: a curated sub
    must never be written OR read as a move source, while a derived sub IS
    written by automation and is still never a move source, because moving a
    track out of it without re-deriving the signal silently drops the routing
    that put it there.
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
    """One energy band. ``max`` is an INCLUSIVE upper bound on the level scale."""

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
    """A tempo detection window, per bucket.

    This lives on the bucket rather than in a separate table because of a
    concrete failure: the source system keyed its priors by folder DISPLAY name,
    so a user whose folders are named anything else got the generic window for
    every track in their library, silently. A window spanning a full octave folds
    nothing, which disables the exact defence the priors exist to provide.
    """

    start: float
    floor: float
    ceil: float


@dataclass(frozen=True)
class SubClass:
    """A sub-playlist that exists under many buckets and carries a write policy.

    ``signal`` says what a derived class is derived from, :data:`SIGNAL_VOX` or
    :data:`SIGNAL_PLAYLIST`, and ``signal_playlist`` names the playlist a
    playlist class mirrors, by the display name rekordbox shows, since that
    playlist is the author's and has no stable id of this product's (U119).
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
    """A bucket's relationship to the energy dimension.

    ``band_display`` overrides only the LABEL of a global band, never its cut.
    That split matters: one bucket in the shipped default names its bands
    differently while splitting at exactly the same levels, and encoding that as
    a second set of cuts would let the two drift apart the moment either moved.
    """

    enabled: bool = True
    band_display: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SubBySource:
    """A bucket that routes by the SOURCE genre instead of by energy.

    ``default`` is explicit on purpose. The source system hardcoded one sub as
    the landing place for anything unrecognised, with no way to see it from
    outside the function, so unrelated styles accumulated there and looked like
    real classifications.
    """

    default: str
    map: Mapping[str, str]


@dataclass(frozen=True)
class FormerPlace:
    """A playlist a bucket's tracks were filed in before the bucket had its folder.

    WHY IT IS DECLARED (R-797). A genre promoted from a sub of one folder to a
    folder of its own leaves its tracks sitting in the old playlist, and every
    reader of the tree asks the taxonomy what a place is. A playlist the
    taxonomy stopped declaring is no place at all, so nothing would withhold a
    second filing over it and nothing could plan leaving it. Declaring it on
    the bucket that took its tracks over makes it one of that bucket's
    competing subs, which is the single question the adoption plan, the
    placement reader and the move already ask.

    ``id`` is the identifier it competes under in the bucket that declares it.
    ``bucket`` is the declared bucket whose folder holds the playlist, ``sub``
    the identifier the playlist had there, which is what a previous write
    recorded its node under, and ``display`` the name it carries.

    A FORMER PLACE IS ONLY EVER LEFT. No resolver answers with one, so nothing
    is filed into it, and the loader refuses one that names a place the
    taxonomy still declares.
    """

    id: str
    bucket: str
    sub: str
    display: str


@dataclass(frozen=True)
class SplitPlace:
    """A band of another bucket that this bucket's tracks still sit in (U118).

    WHY IT IS NOT A FORMER PLACE. Soul was filed under R&B's energy bands as
    one folder until the author split it out. Those bands are still R&B's, so
    a former place naming one is refused by design: leaving it would take
    R&B's own tracks out of a playlist that is theirs. A split place is the
    other half of that rule. It names a playlist the holder still files into,
    and a track leaves it only when its genre names the bucket that declares
    the place, so an R&B track in ``R&B / Med`` is never touched and a Soul
    track there moves to ``Soul / Med``.

    IT COMPETES IN THE DECLARING BUCKET ONLY. In the holder it is already one
    of the holder's own bands, and competing a second time there would read
    every track in it as holding two places.

    ``id`` is the identifier it competes under in the declaring bucket.
    ``bucket`` is the holder, ``sub`` the band's identifier there, and
    ``display`` the name the holder gives that band, which the loader checks.
    ``sub`` may instead be the holder's own former place, the playlist both
    genres sat in before either had a folder, and is then left the same way.

    A SPLIT PLACE IS ONLY EVER LEFT. No resolver answers with one, so nothing
    is filed into it through the declaring bucket.
    """

    id: str
    bucket: str
    sub: str
    display: str


@dataclass(frozen=True)
class GenreSub:
    """A sub of an energy bucket chosen by the track's source genre (U155).

    WHY IT IS NOT ``sub_by_source``. A bucket that routes by source genre never
    reads energy at all, so declaring Rominimal that way on Minimal / Deep Tech
    would take Low, Med and High away from every track in the bucket. A genre
    sub sits BESIDE the bands instead: a track whose genre is one of
    ``sources`` files into its band as before and into this sub as well, the
    way "with vox" sits beside a band. It is additive, so it never competes,
    nothing is ever moved out of it, and no band loses a track to it.

    ``sources`` are exact, case sensitive source genres, each one an exact
    routing alias of the bucket, so a track wearing one is filed by this
    bucket and reaches this sub, and ``Minimal`` beside ``Rominimal`` does not.
    The first source is the word the tagger writes for the sub.
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

    Three match kinds, and which one a rule uses decides WHEN it runs, not just
    what it matches. ``equals`` is an exact refusal or an exact answer and runs
    before the alias lookup; ``all_of`` and ``any_of`` are substring guesses and
    run after it. That precedence is what lets one rule refuse a catch-all
    without also refusing every specific sub-genre whose name contains it.
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
    """One ordered acquisition-gate rule over the SOURCE vocabulary."""

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

#: The word that CLEARS a label's kind, so it follows ``default_kind`` again.
#: Reserved like :data:`ANY_KIND`: a rule naming it would declare a kind no
#: label could be marked with, since marking with it means "none".
NO_KIND = "default"

#: The shape of a kind's name, once folded: one word. ONE PATTERN FOR THE
#: TAXONOMY AND THE REGISTRY. A person types a kind on a command line to mark a
#: label with it, so a rule naming a kind in a shape the registry refuses would
#: declare a kind no label could ever be given: it could hold releases and
#: never pass one.
KIND_NAME = re.compile(r"[a-z0-9][a-z0-9_-]*")


@dataclass(frozen=True)
class PublishedRule:
    """One ordered rule saying what KIND of music a general catalogue's word is.

    The matchers are :class:`GateRule`'s, held lowercase. The vocabulary is not:
    these read the words a general catalogue publishes for an album, where
    :class:`GateRule` reads the record shops' (R-798).
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

    ``word`` is the source's word as the template spells it, matched whole and
    without regard to case. ``tag`` is the genre written onto the file.
    ``bucket`` and ``sub`` are the place routing files that tag in, resolved
    by the loader and never declared, so a row cannot say one folder and write
    a word that files in another. ``sub`` is None for a bucket that splits by
    energy, where the band is the reading's to choose.
    """

    word: str
    tag: str
    bucket: str
    sub: str | None = None


@dataclass(frozen=True)
class Vocabulary:
    """Where each word of ONE source's vocabulary goes (R-799).

    WHY A TABLE PER SOURCE. The alias lists on the buckets were written against
    the record shops' words, where Pop is a dance genre. A general catalogue
    says Pop of every kind of pop, so one table read for both files a pop
    record beside dance tracks. ``source`` is the name a file's record gives
    the source, which is the name the tag summary counts under.

    THE TABLE IS ASKED FIRST. A word with no row goes on to the buckets'
    aliases, as every word did before the table existed, so a specific word
    those aliases already file correctly is not lost. What the table changes
    for such a word is one thing: on a copy that declares a table, the answer
    must still name a folder, see :meth:`Taxonomy.named_folder`.
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
    # The family that means "nothing in common". Declared rather than inferred,
    # because two buckets share it without being alike, and rewarding them for
    # sharing it would make the least informative answer the strongest signal.
    catch_all: str | None = None


@dataclass(frozen=True)
class Node:
    """A named place in the tree that is not a bucket: the root, the intake flow."""

    id: str
    display: str


#: The source system's threshold for a set rather than a track: twenty minutes.
#: A template that declares the long track playlist and omits the threshold
#: takes this one, which is the separation a person had before the port.
DEFAULT_LONG_TRACK_SECONDS = 1200


@dataclass(frozen=True)
class LongTracks:
    """The root playlist every collection track over a length is a member of.

    ``over_seconds`` is a strict bound, as the source system's was: a track of
    exactly that length is not a member.
    """

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

    # The tree a whole-catalog import writes into: one folder per catalogued
    # source, each holding one playlist per year. It sits here beside the routing
    # tree and the intake flow rather than in the writer that emits it, because
    # R19 puts every playlist display name in the declared template and the write
    # layer is forbidden from carrying one at all.
    #
    # OPTIONAL, unlike the other two, and that is a decision rather than an
    # omission. A library that never imports a catalog has no such tree, and a
    # template declaring none is complete rather than deficient. The writer
    # refuses by name when asked to write a tree nobody declared, which beats
    # inventing a folder in somebody's library from a default they never saw.
    catalog: Node | None = None

    # The playlist that keeps sets apart from tracks, a direct child of the
    # playlist root. OPTIONAL for the catalog's reason: a template without it
    # builds no such playlist rather than one named by a default nobody saw.
    long_tracks: LongTracks | None = None

    # The folder inside the intake flow that a batch is rotated into once it is
    # stale (U111), ``INBOX / Old`` in the shipped template. OPTIONAL for the
    # catalog's reason: a library whose active copy predates the section has no
    # such folder declared, and ``inbox rotate`` refuses by name rather than
    # creating a folder from a default nobody saw.
    intake_old: Node | None = None

    # The folder at the playlist root that keeps a set's playlist for good
    # (U121), ``INSPIRATION`` in the shipped template: a set intake lands its
    # batch under the intake flow, which the rotation clears, and writes the
    # whole set once more here, which nothing rotates. OPTIONAL for the
    # catalog's reason: a library whose active copy predates the section has
    # no such folder declared, and the set playlist is refused by name rather
    # than written under a folder nobody declared.
    inspiration: Node | None = None

    # The vocabularies of the sources that have one of their own (R-799), in
    # declared order. EMPTY in a copy written before that unit, and then every
    # source's word is resolved by the buckets' aliases, as it always was.
    vocabularies: tuple[Vocabulary, ...] = ()

    # Indexes, built once at construction. They are derived data, so they can
    # never disagree with the declaration they came from.
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

        NONE AND AN EMPTY TABLE ARE DIFFERENT ANSWERS. None says this taxonomy
        declares nothing for the source, so its words are resolved exactly as
        they were before any table existed. A table with no rows is a
        declaration: it answers for no word, and the copy has still taken the
        rule that a genre written from that source names a folder.
        """
        return self._vocabulary.get(source)

    def named_folder(self, genre: str) -> tuple[str, str | None] | None:
        """The place a written genre names by an exact declaration, or None.

        The bucket and, in a bucket that files by source genre, the style sub.
        None when the genre is filed by a keyword or the fallback, is too
        coarse to be a final genre, or is such a bucket's bare name or a word
        that would land in its default sub. ONE RULE WITH THE LOADER: this is
        the test a vocabulary row's tag passed to be declared, asked again of
        a genre the buckets' aliases answered.
        """
        place, _problem = _tag_place(
            genre, self._by_id, self._by_display, self._routing_alias, self.fallback
        )
        return place

    def former_places(self, bucket_id: str) -> tuple[tuple[str, "FormerPlace"], ...]:
        """Every former place that competes in one bucket, with its declarer.

        The ones the bucket declares and the ones its folder holds for another
        bucket, in declared order. Built once at load, since what competes is
        asked per track and per bucket.
        """
        return self._former_places.get(bucket_id, ())

    def split_places(self, bucket_id: str) -> tuple[tuple[str, "SplitPlace"], ...]:
        """Every split place one bucket declares or holds, with its declarer.

        BOTH SIDES, as :meth:`former_places` answers, though a split place
        competes only where it is declared: the holder's side is what the move
        asks to know a band of its own is settled by the declaring bucket.
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
        """The bucket a source string is DECLARED to route to, exactly.

        Case-sensitive, because the strings these aliases came from are exact
        vendor genre names and a case-insensitive match would silently merge two
        that a source taxonomy keeps apart.
        """
        return self._routing_alias.get(source_genre)

    def bucket_for_display(self, display: str) -> str | None:
        """The bucket whose display name is exactly ``display``, if any.

        This is a lookup FROM a display name, not a record keyed BY one. The
        distinction is the whole of R19: nothing persisted keys on a display
        name, but a tagger that writes bucket names back onto files means routing
        constantly has to recognise one.

        BUCKETS ONLY, AND EXACT, WHICH IS NOW LOAD BEARING TWICE. It places a
        name in the tree, so a sub's display must not answer it and put a track
        one level up. ``suggest_tag``'s last tier reads it for the other half of
        the same fact: a word this answers for is one routing will place where
        the template says, and a word it does not is one the file wears while
        landing somewhere the template did not choose (R-650).
        """
        return self._by_display.get(display)

    def tagging_alias(self, lowered_source_genre: str) -> tuple[str, str | None] | None:
        """The (bucket id, sub id) a source string is declared to tag as.

        Case-INSENSITIVE, unlike the routing lookup, because these strings are
        scraped from pages whose capitalisation varies run to run.
        """
        return self._tagging_alias.get(lowered_source_genre)

    def buckets_without_bpm_prior(self) -> tuple[str, ...]:
        """Buckets that declare no tempo window.

        A caller that needs priors asks this once and refuses by name, rather
        than detecting every track against a generic window and reporting
        nothing. Silent defaulting here is the exact failure that made a custom
        taxonomy degrade detection across a whole library.
        """
        return tuple(b.id for b in self.buckets if b.bpm is None)

    def is_too_coarse_as_source(self, value: str) -> bool:
        """Whether a source string is too coarse to accept as a final genre tag.

        Replaces two separate constants in the source system: a reject set used
        to decide whether a lookup improved on an existing tag, and a fallback
        folder name used to decide whether a track counted as a taxonomy gap.
        They always meant the same thing and were never the same string.
        """
        return (value or "").strip() in self.fallback.too_coarse_as_source


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


#: The names of the top level folders another app owns in rekordbox's tree,
#: exactly as it writes them (U185). Declared HERE, in the domain layer, since
#: it is a fact about names a declared tree may not take; the writer's guard,
#: :mod:`cratekit.core.foreign_tree`, reads it from here, downward.
FOREIGN_ROOT_NAMES: frozenset[str] = frozenset({"DEADCA7"})


def load_taxonomy(text: str) -> Taxonomy:
    """Parse and validate a template from TOML text.

    Text rather than a path, so the caller owns the input and this stays a pure
    function of its argument. That is what lets one test drive two taxonomies
    through the same process, which is the verification this unit owes.
    """
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise TaxonomyError([f"template is not valid TOML: {exc}"]) from exc
    return build_taxonomy(data)


def default_taxonomy() -> Taxonomy:
    """The template that ships in the wheel, read-only.

    The ONE input this module performs, and it is against packaged data that
    cannot vary at runtime. It is NOT the taxonomy a verb routes by: a library's
    active template is read by :func:`cratekit.core.active_taxonomy.load`, and
    ``tests/test_active_taxonomy.py`` refuses a call to this from any other
    module in the package (R-685). No verb read the active copy until then.
    """
    return load_taxonomy(shipped_template_text(DEFAULT_TEMPLATE_NAME))


def shipped_template_names() -> tuple[str, ...]:
    """Every taxonomy template that ships in the wheel, by its short name.

    Walked rather than listed, so a second template is offered by the wizard and
    accepted by the health check on the day it is added (P3).

    It lives HERE rather than in the wizard that first needed it because two
    layers ask the same question and the answers have to be one answer: the
    wizard offers the shipped names as a closed set, and doctor refuses a
    configuration naming a template that is not one of them. A copy of this walk
    in the CLI would let a name be offered that the check rejects, or accepted by
    the check with nothing shipping it.

    IT NEVER RAISES, and that is not defensive habit. Its caller is an ARGUMENT
    PARSER, and the whole command tree is built before anything dispatches, so a
    packaged directory that is missing or unreadable used to take every command
    down with an unhandled error, including the health report. That report exists
    for the broken machine, and a partial install is a broken machine: it has to
    be able to describe one. An empty answer here is the honest one, and the
    caller reports the missing template as a finding rather than as a traceback.

    ``ValueError`` IS CAUGHT BESIDE ``OSError``, and the reason is that the claim
    above was false without it. ``importlib.resources`` does not promise one
    exception family: a filesystem-backed traversable raises ``FileNotFoundError``
    or ``NotADirectoryError``, both of which are ``OSError``, while a zip-backed
    one raises ``ValueError("Can't listdir a file")``, which is not. Catching one
    family and writing "never raises" is the shape of overclaim this unit has
    been shipping all week, so both are caught and the sentence is true.

    WHICH LEAVES THE OTHER HALF, and it is why this delegates. An empty answer is
    honest to an argument parser, which only ever needed a list of choices, and
    it is a LIE to a health check, which needs to know whether nothing ships or
    nothing could be read. Those have opposite remedies and the check was giving
    the wrong one. :func:`shipped_templates` returns both halves; this returns
    the half a parser can use.
    """
    return shipped_templates()[0]


def shipped_templates() -> tuple[tuple[str, ...], str | None]:
    """The shipped template names, AND why the directory could not be listed.

    Two returns rather than one because "no template ships under that name" and
    "the packaged directory could not be read" are different diagnoses with
    opposite remedies, and collapsing them into an empty tuple gave every caller
    the first sentence for the second condition. Doctor told a user with a
    damaged install that their configuration named a template nothing ships and
    sent them to re-run setup, which cannot repair packaged data.

    The problem is a SENTENCE rather than the exception, because the caller
    renders it into a report and the only thing it needs from the failure is what
    went wrong with which directory.

    A NAME IS ONLY OFFERED IF CONFIGURATION WOULD ACCEPT IT. Anything between the
    prefix and the suffix is a candidate on disk, so ``taxonomy.deep.house.toml``
    yields ``deep.house``, which ``config.validate`` refuses because the name is
    composed into a resource path. Offering a value that is then rejected one
    layer down is the same two-answers-to-one-question defect this function was
    written to close, so the filter is applied here, from the module that owns
    the rule.

    IT NEVER RAISES either, for the reason above it: the argument parser reaches
    this through :func:`shipped_template_names` on every invocation of every verb.
    """
    try:
        entries = list((resources.files("cratekit") / "templates").iterdir())
    except (OSError, ValueError) as exc:
        return (), f"the packaged template directory could not be listed: {exc}"
    found = []
    for item in entries:
        name = item.name
        if not name.startswith(_TEMPLATE_PREFIX) or not name.endswith(_TEMPLATE_SUFFIX):
            continue
        short = name[len(_TEMPLATE_PREFIX) : -len(_TEMPLATE_SUFFIX)]
        if config.template_name_is_usable(short):
            found.append(short)
    return tuple(sorted(found)), None


def shipped_template_text(name: str) -> str:
    """The packaged text of one template, by its short name.

    Raises ``FileNotFoundError`` when nothing ships under that name, which is the
    answer a caller wants: the shipped set is read-only data, so a name outside
    it is a configuration error rather than a transient failure.
    """
    source = resources.files("cratekit") / "templates" / f"{_TEMPLATE_PREFIX}{name}{_TEMPLATE_SUFFIX}"
    return source.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The origin record (R-689)
# ---------------------------------------------------------------------------


def template_digest(text: str) -> str:
    """The fingerprint of one template's TEXT, as setup records it and doctor compares it.

    ONE DEFINITION, used by both, because the comparison is only meaningful if
    the two sides hashed the same bytes the same way. It is taken over the text
    as read, not over the bytes on disk: ``Path.read_text`` folds a Windows line
    ending to a newline, so an editor that rewrote the line endings and nothing
    else is not counted as an edit, and the shipped text is read the same way.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Fingerprint:
    """What doctor compares two template texts by: the digest, and the top level
    tables and arrays of tables the text declares, so a difference can be named."""

    digest: str
    sections: frozenset[str]


def template_fingerprint(text: str) -> Fingerprint:
    """The fingerprint of one template's text. Text that is not TOML has no sections."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        sections: frozenset[str] = frozenset()
    else:
        sections = frozenset(
            name for name, value in data.items() if isinstance(value, (dict, list))
        )
    return Fingerprint(digest=template_digest(text), sections=sections)


def shipped_template_fingerprint(name: str) -> Fingerprint:
    """The fingerprint of the packaged text of one template, by its short name.

    THE SHIPPED TEXT STAYS IN THIS MODULE. Doctor compares a library's active copy
    against the shipped template by this and never reads the text itself, so the
    guard in ``tests/test_active_taxonomy.py`` can keep doctor off the list of
    modules that read the shipped text: a module holding both that text and the
    parser is one line from routing by a template that is not the library's.
    Raises what :func:`shipped_template_text` raises.
    """
    return template_fingerprint(shipped_template_text(name))


@dataclass(frozen=True, slots=True)
class Origin:
    """Which shipped text an active copy was made from: the name and its digest."""

    template: str
    digest: str


def origin_record_text(template: str, text: str) -> str:
    """The record setup writes beside the copy, as TOML text."""
    return (
        "# Written by crate setup with the active taxonomy copy beside it. Which\n"
        "# shipped template the copy was made from and a digest of that text, so\n"
        "# doctor can tell a copy that fell behind the shipped template from one a\n"
        "# person edited (R-689). Nothing routes by this file.\n"
        f'template = "{template}"\n'
        f'sha256 = "{template_digest(text)}"\n'
    )


def parse_origin_record(text: str) -> Origin:
    """Read the record back. Raises ``ValueError`` when the text is not TOML or
    either field is missing or malformed. A key it does not know is left alone."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"not valid TOML: {exc}") from exc
    template, digest = data.get("template"), data.get("sha256")
    if not isinstance(template, str) or not config.template_name_is_usable(template):
        raise ValueError(f"template is not a shipped template name: {template!r}")
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        raise ValueError(f"sha256 is not a hex digest: {digest!r}")
    return Origin(template=template, digest=digest)


_DIGEST = re.compile(r"[0-9a-f]{64}")


def build_taxonomy(data: Mapping[str, Any]) -> Taxonomy:
    """Validate a parsed template and freeze it into a Taxonomy.

    Every problem is collected before anything is raised. Reporting the first
    error only is how a bad template turns into a long evening.
    """
    problems: list[str] = []

    version = data.get("schema_version")
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        problems.append(
            f"schema_version {version!r} is not supported "
            f"(supported: {sorted(SUPPORTED_SCHEMA_VERSIONS)})"
        )
        raise TaxonomyError(problems)

    tree_raw = data.get("tree") or {}
    intake_raw = data.get("intake") or {}
    tree = Node(str(tree_raw.get("id", "")), str(tree_raw.get("display", "")))
    intake = Node(str(intake_raw.get("id", "")), str(intake_raw.get("display", "")))
    tree_depth = int(tree_raw.get("depth", 0))
    # Declared or absent, never half declared. A section carrying an id and no
    # display, or the reverse, is validated exactly as strictly as the two
    # mandatory trees: an optional section is optional to WRITE, not optional to
    # get right, and a half-declared tree would reach a writer as a folder named
    # the empty string.
    # Keyed on PRESENCE, never on truthiness. An empty ``[catalog]`` table is a
    # declaration, and it is falsy, so a truthiness test reads "the user wrote a
    # section" as "the user wrote no section" and skips the very validation the
    # paragraph above promises. That is the shape this whole block exists to
    # refuse, arriving through the check meant to enforce it.
    catalog_raw = data.get("catalog") if "catalog" in data else None
    catalog = (
        Node(str(catalog_raw.get("id", "")), str(catalog_raw.get("display", "")))
        if catalog_raw is not None
        else None
    )
    long_tracks, long_problems = _build_long_tracks(data)
    problems += long_problems
    # Keyed on PRESENCE, for the catalog section's reason, and a value that is
    # not a table is a problem reported by name rather than a traceback.
    old_raw = data.get("intake_old") if "intake_old" in data else None
    intake_old: Node | None = None
    if old_raw is not None and not isinstance(old_raw, Mapping):
        problems.append("[intake_old] must be a table with an id and a display")
    elif old_raw is not None:
        intake_old = Node(str(old_raw.get("id", "")), str(old_raw.get("display", "")))
        # A rotation tells INBOX from Old by the tree, but an Old that shares
        # the intake flow's id or display is a declaration of one folder twice.
        if intake_old.id == intake.id or intake_old.display == intake.display:
            problems.append(
                "[intake_old] must differ from [intake] in both id and display; "
                "it declares a folder inside the intake flow, not the flow itself"
            )
    # Keyed on PRESENCE, for the catalog section's reason (U121). A folder at
    # the playlist root and not inside the intake flow, so it shares nothing
    # with [intake] and [intake_old] except the shape of its declaration.
    inspiration_raw = data.get("inspiration") if "inspiration" in data else None
    inspiration: Node | None = None
    if inspiration_raw is not None and not isinstance(inspiration_raw, Mapping):
        problems.append("[inspiration] must be a table with an id and a display")
    elif inspiration_raw is not None:
        inspiration = Node(
            str(inspiration_raw.get("id", "")), str(inspiration_raw.get("display", ""))
        )
    declared_nodes = [(tree, "tree"), (intake, "intake")]
    if catalog is not None:
        declared_nodes.append((catalog, "catalog"))
    if intake_old is not None:
        declared_nodes.append((intake_old, "intake_old"))
    if inspiration is not None:
        declared_nodes.append((inspiration, "inspiration"))
    if long_tracks is not None:
        declared_nodes.append((Node(long_tracks.id, long_tracks.display), "long_tracks"))
    for node, label in declared_nodes:
        if not _ID.match(node.id):
            problems.append(f"[{label}] id {node.id!r} must match {_ID.pattern}")
        if not node.display:
            problems.append(f"[{label}] display must be a non-empty string")
        elif node.display in FOREIGN_ROOT_NAMES:
            # U185. A declared tree of that name would adopt another app's folder.
            problems.append(
                f"[{label}] display {node.display!r} is the folder another app owns at "
                f"the top of rekordbox's tree, and a tree of that name would adopt it"
            )
    # KTD14: the XML bridge's indentation constants encode exactly three levels.
    # A template that declares another depth is refused BY NAME here, rather than
    # emitting bytes that rekordbox reads as a different tree.
    if tree_depth != SUPPORTED_TREE_DEPTH:
        problems.append(
            f"[tree] depth is {tree_depth}, and only {SUPPORTED_TREE_DEPTH} is "
            f"supported: the XML bridge's indentation encodes a root child, a "
            f"folder, and a sub-playlist (KTD14)"
        )

    energy, energy_problems = _build_energy(data.get("energy") or {})
    problems += energy_problems

    buckets, bucket_problems = _build_buckets(data.get("bucket") or [], energy)
    problems += bucket_problems

    by_id = {b.id: b for b in buckets}

    fallback, fallback_problems = _build_fallback(data.get("fallback") or {}, by_id)
    problems += fallback_problems

    sub_classes, sub_class_problems = _build_sub_classes(data.get("sub_class") or [], int(version))
    problems += sub_class_problems

    problems += _check_former_places(buckets, energy, sub_classes, int(version))
    problems += _check_split_places(buckets, energy, sub_classes, int(version))
    problems += _check_genre_subs(buckets, energy, sub_classes, int(version))

    fuzzy, fuzzy_problems = _build_fuzzy(data.get("fuzzy") or [], by_id)
    problems += fuzzy_problems

    suggest, suggest_problems = _build_suggest(data.get("suggest") or [], by_id)
    problems += suggest_problems

    gate, gate_problems = _build_gate(data.get("label_gate") or {})
    problems += gate_problems

    family, family_problems = _build_family(data.get("family") or {}, buckets)
    problems += family_problems

    routing_alias, tagging_alias, alias_problems = _build_alias_indexes(buckets)
    problems += alias_problems

    # Keyed on PRESENCE, for the catalog section's reason above: an empty
    # table is a declaration and must be read as one.
    by_display = {b.display: b.id for b in buckets}
    vocabularies, vocabulary_problems = _build_vocabularies(
        data.get("vocabulary") if "vocabulary" in data else None,
        by_id,
        by_display,
        routing_alias,
        fallback,
    )
    problems += vocabulary_problems

    if problems:
        raise TaxonomyError(problems)

    return Taxonomy(
        schema_version=int(version),
        tree=tree,
        tree_depth=tree_depth,
        intake=intake,
        buckets=buckets,
        energy=energy,
        fallback=fallback,
        sub_classes=sub_classes,
        fuzzy=fuzzy,
        suggest=suggest,
        label_gate=gate,
        family=family,
        catalog=catalog,
        long_tracks=long_tracks,
        intake_old=intake_old,
        inspiration=inspiration,
        vocabularies=vocabularies,
        _by_id=by_id,
        _by_display=by_display,
        _routing_alias=routing_alias,
        _tagging_alias=tagging_alias,
        _former_places=_index_former_places(buckets),
        _split_places=_index_split_places(buckets),
        _vocabulary={
            table.source: {row.word.lower(): row for row in table.words}
            for table in vocabularies
        },
    )


def _index_former_places(
    buckets: Sequence[Bucket],
) -> dict[str, tuple[tuple[str, FormerPlace], ...]]:
    """Each bucket's former places, its own and the ones its folder holds."""
    found: dict[str, list[tuple[str, FormerPlace]]] = {}
    for declarer in buckets:
        for place in declarer.formerly:
            for bucket_id in dict.fromkeys((declarer.id, place.bucket)):
                found.setdefault(bucket_id, []).append((declarer.id, place))
    return {bucket_id: tuple(places) for bucket_id, places in found.items()}


def _index_split_places(
    buckets: Sequence[Bucket],
) -> dict[str, tuple[tuple[str, SplitPlace], ...]]:
    """Each bucket's split places, its own and the ones its bands are for another."""
    found: dict[str, list[tuple[str, SplitPlace]]] = {}
    for declarer in buckets:
        for place in declarer.split_from:
            for bucket_id in dict.fromkeys((declarer.id, place.bucket)):
                found.setdefault(bucket_id, []).append((declarer.id, place))
    return {bucket_id: tuple(places) for bucket_id, places in found.items()}


# ---------------------------------------------------------------------------
# Section builders. Each returns (value, problems) so one bad section never
# hides the next one.
# ---------------------------------------------------------------------------


def _build_long_tracks(data: Mapping[str, Any]) -> tuple[LongTracks | None, list[str]]:
    """The long track playlist, or None when the template declares none.

    Keyed on PRESENCE, for the reason the catalog section gives: an empty table
    is a declaration and is validated as one. The id and display are checked
    with the other declared nodes; the threshold is checked here.

    THE THRESHOLD IS A WHOLE NUMBER OF SECONDS ABOVE ZERO, and a boolean is
    refused rather than read as 1, because ``true`` would put every track in the
    collection into the playlist. A zero or negative bound does the same.
    """
    if "long_tracks" not in data:
        return None, []
    raw = data.get("long_tracks")
    if not isinstance(raw, Mapping):
        return None, ["[long_tracks] must be a table"]
    problems: list[str] = []
    seconds = raw.get("over_seconds", DEFAULT_LONG_TRACK_SECONDS)
    if isinstance(seconds, bool) or not isinstance(seconds, int) or seconds < 1:
        problems.append(
            f"[long_tracks] over_seconds must be a whole number of seconds of at "
            f"least 1, got {seconds!r}"
        )
        seconds = DEFAULT_LONG_TRACK_SECONDS
    declared = LongTracks(str(raw.get("id", "")), str(raw.get("display", "")), seconds)
    return declared, problems


def _build_energy(raw: Mapping[str, Any]) -> tuple[Energy, list[str]]:
    problems: list[str] = []
    enabled = bool(raw.get("enabled", True))
    scale_max = int(raw.get("scale_max", 10))
    if scale_max < 1:
        problems.append(f"[energy] scale_max must be at least 1, got {scale_max}")

    bands: list[Band] = []
    seen_band_ids: set[str] = set()
    previous = 0
    for index, entry in enumerate(raw.get("bands") or []):
        band = Band(str(entry.get("id", "")), str(entry.get("display", "")), int(entry.get("max", 0)))
        if not _ID.match(band.id):
            problems.append(f"[energy] band {index} id {band.id!r} must match {_ID.pattern}")
        if band.id in seen_band_ids:
            problems.append(f"[energy] duplicate band id {band.id!r}")
        seen_band_ids.add(band.id)
        if not band.display:
            problems.append(f"[energy] band {band.id!r} needs a display name")
        if band.max <= previous:
            problems.append(
                f"[energy] band {band.id!r} max {band.max} does not increase on {previous}; "
                f"bands are ordered and their bounds must be strictly increasing or a "
                f"level falls into two bands"
            )
        previous = band.max
        bands.append(band)
    if enabled and not bands:
        problems.append("[energy] enabled but no bands declared")
    if bands and bands[-1].max != scale_max:
        problems.append(
            f"[energy] the last band ends at {bands[-1].max}, not at scale_max {scale_max}; "
            f"a level above the last band would route nowhere"
        )

    cuts: list[RatingCut] = []
    previous = 0
    for entry in raw.get("rating", {}).get("cuts", []):
        cut = RatingCut(int(entry.get("max", 0)), int(entry.get("rating", 0)))
        if cut.max <= previous:
            problems.append(
                f"[energy.rating] cut ending at {cut.max} does not increase on {previous}"
            )
        previous = cut.max
        cuts.append(cut)
    if cuts and cuts[-1].max != scale_max:
        problems.append(
            f"[energy.rating] the last cut ends at {cuts[-1].max}, not at scale_max {scale_max}"
        )
    # The rating cuts are NOT required to align with the band cuts. They are
    # decoupled deliberately: energy is decile-calibrated, so an even five-way
    # star spread and a three-way tree split are both correct and neither should
    # be forced to follow the other. Requiring alignment here would silently
    # re-rate a whole library the first time a band moved.

    no_energy_raw = raw.get("no_energy_sub")
    no_energy = None
    if no_energy_raw:
        no_energy = Sub(str(no_energy_raw.get("id", "")), str(no_energy_raw.get("display", "")))
        if not _ID.match(no_energy.id):
            problems.append(f"[energy] no_energy_sub id {no_energy.id!r} must match {_ID.pattern}")

    return Energy(enabled, scale_max, tuple(bands), tuple(cuts), no_energy), problems


def _build_buckets(
    raw: Sequence[Mapping[str, Any]], energy: Energy
) -> tuple[tuple[Bucket, ...], list[str]]:
    problems: list[str] = []
    buckets: list[Bucket] = []
    seen_ids: set[str] = set()
    seen_displays: set[str] = set()
    band_ids = {b.id for b in energy.bands}

    for index, entry in enumerate(raw):
        bucket_id = str(entry.get("id", ""))
        display = str(entry.get("display", ""))
        where = f"[[bucket]] {bucket_id or index}"
        if not _ID.match(bucket_id):
            problems.append(
                f"{where}: id {bucket_id!r} must match {_ID.pattern}; an id is persisted and "
                f"never rendered, so a display name cannot serve as one (R19)"
            )
        if bucket_id in seen_ids:
            problems.append(f"{where}: duplicate bucket id")
        seen_ids.add(bucket_id)
        if not display:
            problems.append(f"{where}: display must be a non-empty string")
        if display in seen_displays:
            problems.append(f"{where}: duplicate display name {display!r}")
        seen_displays.add(display)

        bpm_raw = entry.get("bpm")
        bpm = None
        if bpm_raw:
            bpm = BpmPrior(
                float(bpm_raw.get("start", 0)),
                float(bpm_raw.get("floor", 0)),
                float(bpm_raw.get("ceil", 0)),
            )
            if not (0 < bpm.floor < bpm.start < bpm.ceil):
                problems.append(
                    f"{where}: bpm window must satisfy 0 < floor < start < ceil, got "
                    f"floor={bpm.floor} start={bpm.start} ceil={bpm.ceil}"
                )

        subs = tuple(
            Sub(
                str(s.get("id", "")),
                str(s.get("display", "")),
                tuple(s.get("tag_aliases") or ()),
            )
            for s in entry.get("sub") or []
        )
        for sub in subs:
            if not _ID.match(sub.id):
                problems.append(f"{where}: sub id {sub.id!r} must match {_ID.pattern}")

        energy_raw = entry.get("energy") or {}
        band_display = dict(energy_raw.get("band_display") or {})
        for key in band_display:
            if key not in band_ids:
                problems.append(
                    f"{where}: band_display names {key!r}, which is not a declared band "
                    f"({sorted(band_ids)}); a label override must override a real band"
                )
        bucket_energy = BucketEnergy(bool(energy_raw.get("enabled", True)), band_display)

        single_raw = entry.get("single_sub")
        single = None
        if single_raw:
            single = Sub(str(single_raw.get("id", "")), str(single_raw.get("display", "")))
            if not _ID.match(single.id):
                problems.append(f"{where}: single_sub id {single.id!r} must match {_ID.pattern}")

        sbs_raw = entry.get("sub_by_source")
        sub_by_source = None
        if sbs_raw:
            mapping = {
                str(row.get("source", "")): str(row.get("sub", ""))
                for row in sbs_raw.get("map") or []
            }
            sub_by_source = SubBySource(str(sbs_raw.get("default", "")), mapping)
            declared = {s.id for s in subs}
            if sub_by_source.default not in declared:
                problems.append(
                    f"{where}: sub_by_source default {sub_by_source.default!r} is not a "
                    f"declared sub of this bucket ({sorted(declared)})"
                )
            for source, target in mapping.items():
                if target not in declared:
                    problems.append(
                        f"{where}: sub_by_source maps {source!r} to {target!r}, which is not "
                        f"a declared sub of this bucket"
                    )

        if bucket_energy.enabled and single is not None:
            problems.append(
                f"{where}: declares single_sub while energy is enabled; a bucket either "
                f"splits by energy or has one sub, never both"
            )

        # THE SHAPE IS CHECKED BEFORE A ROW IS READ. A person edits a library's
        # copy by hand, and `[bucket.formerly]` with one pair of brackets is
        # valid TOML that arrives here as a table, not a list of them. Read as
        # rows it raised an attribute error out of the loader, which every verb
        # then reported as a defect in this product instead of a line to fix.
        formerly_raw = entry.get("formerly") or []
        if not isinstance(formerly_raw, list) or not all(
            isinstance(row, Mapping) for row in formerly_raw
        ):
            problems.append(
                f"{where}: formerly must be an array of tables, written "
                f"[[bucket.formerly]] with an id, a bucket, a sub and a display"
            )
            formerly_raw = []
        formerly = tuple(
            FormerPlace(
                id=str(row.get("id", "")),
                bucket=str(row.get("bucket", "")),
                sub=str(row.get("sub", "")),
                display=str(row.get("display", "")),
            )
            for row in formerly_raw
        )
        # THE SAME SHAPE CHECK, for the same hand edit (U118).
        split_raw = entry.get("split_from") or []
        if not isinstance(split_raw, list) or not all(
            isinstance(row, Mapping) for row in split_raw
        ):
            problems.append(
                f"{where}: split_from must be an array of tables, written "
                f"[[bucket.split_from]] with an id, a bucket, a sub and a display"
            )
            split_raw = []
        split_from = tuple(
            SplitPlace(
                id=str(row.get("id", "")),
                bucket=str(row.get("bucket", "")),
                sub=str(row.get("sub", "")),
                display=str(row.get("display", "")),
            )
            for row in split_raw
        )

        # THE SAME SHAPE CHECK, for the same hand edit (U155). A row whose
        # sources are not a list of strings is read as having none, which the
        # genre sub check then refuses by name.
        genre_raw = entry.get("genre_sub") or []
        if not isinstance(genre_raw, list) or not all(
            isinstance(row, Mapping) for row in genre_raw
        ):
            problems.append(
                f"{where}: genre_sub must be an array of tables, written "
                f"[[bucket.genre_sub]] with an id, a display and a list of sources"
            )
            genre_raw = []
        genre_subs = tuple(
            GenreSub(
                id=str(row.get("id", "")),
                display=str(row.get("display", "")),
                sources=_sources(row.get("sources")),
            )
            for row in genre_raw
        )

        buckets.append(
            Bucket(
                id=bucket_id,
                display=display,
                family=entry.get("family"),
                bpm=bpm,
                aliases=tuple(entry.get("aliases") or ()),
                tag_aliases=tuple(entry.get("tag_aliases") or ()),
                subs=subs,
                energy=bucket_energy,
                single_sub=single,
                sub_by_source=sub_by_source,
                rates=bool(entry.get("rates", True)),
                formerly=formerly,
                split_from=split_from,
                genre_subs=genre_subs,
            )
        )

    if not buckets:
        problems.append("no [[bucket]] declared; a taxonomy with no buckets routes nothing")
    return tuple(buckets), problems


def _sources(raw: Any) -> tuple[str, ...]:
    """A genre sub's sources as declared, or none when they are not a list of strings."""
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        return ()
    return tuple(raw)


def live_places(
    bucket: Bucket, energy: Energy, sub_classes: Sequence[SubClass]
) -> tuple[set[str], set[str]]:
    """The identifiers and the names of every sub one bucket's folder can hold.

    The declared subs and the single sub, the bands under the bucket's own
    labels and the no reading sub when the bucket splits by energy, and every
    sub class, and since U155 every genre sub. This is what a former place
    must not be.

    PUBLIC, because the adoption plan asks it too (R-788): handed the sub
    classes without the vocal one, it answers whether a bucket's own places
    take the vocal sub's name. One list of what a folder can hold, so a shape
    added here is a shape both askers see.
    """
    ids = {sub.id for sub in bucket.subs}
    displays = {sub.display for sub in bucket.subs}
    if bucket.single_sub is not None:
        ids.add(bucket.single_sub.id)
        displays.add(bucket.single_sub.display)
    bands = _band_names(bucket, energy)
    ids.update(bands)
    displays.update(bands.values())
    for entry in sub_classes:
        ids.add(entry.id)
        displays.add(entry.display)
    for genre in bucket.genre_subs:
        ids.add(genre.id)
        displays.add(genre.display)
    return ids, displays


def _check_former_places(
    buckets: Sequence[Bucket],
    energy: Energy,
    sub_classes: Sequence[SubClass],
    version: int,
) -> list[str]:
    """Refuse a former place that is still a place (R-797).

    A FORMER PLACE IS REMOVED FROM, so every way of naming a live playlist
    through one is refused here, before any plan is built. Its bucket has to be
    declared, since the folder is found by that bucket's name. The sub
    identifier and the name it carries must not be ones that bucket still
    holds, or a move would leave a playlist tracks are still filed into. Its
    own identifier must not be one the declaring bucket or the holding bucket
    already competes on, since it competes in both, and no two former places
    share one. And one playlist cannot be the former place of two buckets,
    since a track leaving it would be claimed twice.

    THE TEMPLATE HAS TO STATE THE VERSION THAT KNOWS ONE. See
    :data:`FORMER_PLACE_SCHEMA_VERSION`.
    """
    problems: list[str] = []
    by_id = {bucket.id: bucket for bucket in buckets}
    claimed_subs: dict[tuple[str, str], str] = {}
    claimed_displays: dict[tuple[str, str], str] = {}
    seen: dict[str, str] = {}
    for bucket in buckets:
        own_ids, _own_displays = live_places(bucket, energy, sub_classes)
        if bucket.formerly and version < FORMER_PLACE_SCHEMA_VERSION:
            problems.append(
                f"[[bucket]] {bucket.id}: declares a former place under schema_version "
                f"{version}; write schema_version = {FORMER_PLACE_SCHEMA_VERSION}, since a "
                f"build that reads version {version} ignores the declaration and files a "
                f"track into its new place while it still sits in the old one"
            )
        for former in bucket.formerly:
            where = f"[[bucket]] {bucket.id} formerly {former.id or former.display!r}"
            if not _ID.match(former.id):
                problems.append(f"{where}: id {former.id!r} must match {_ID.pattern}")
            if former.id in own_ids:
                problems.append(
                    f"{where}: id {former.id!r} is already a sub of this bucket; a former "
                    f"place competes under an identifier of its own"
                )
            if former.id in seen:
                problems.append(
                    f"{where}: duplicate former place id, already declared by "
                    f"{seen[former.id]!r}"
                )
            seen.setdefault(former.id, bucket.id)
            if not _ID.match(former.sub):
                problems.append(f"{where}: sub {former.sub!r} must match {_ID.pattern}")
            if not former.display:
                problems.append(f"{where}: display must be a non-empty string")
            holder = by_id.get(former.bucket)
            if holder is None:
                problems.append(
                    f"{where}: names bucket {former.bucket!r}, which is not declared; the "
                    f"folder a former place sits in is found by its bucket"
                )
                continue
            live_ids, live_displays = live_places(holder, energy, sub_classes)
            if former.id in live_ids:
                problems.append(
                    f"{where}: id {former.id!r} is a sub of {former.bucket!r}, where a "
                    f"former place competes as well; give it an identifier of its own"
                )
            if former.sub in live_ids:
                problems.append(
                    f"{where}: {former.bucket!r} still declares the sub {former.sub!r}; a "
                    f"former place is one the taxonomy no longer files into"
                )
            if former.display in live_displays:
                problems.append(
                    f"{where}: {former.bucket!r} still holds a sub named "
                    f"{former.display!r}; leaving a former place would remove tracks "
                    f"from a playlist that is still theirs"
                )
            for claimed, key in (
                (claimed_subs, (former.bucket, former.sub)),
                (claimed_displays, (former.bucket, former.display)),
            ):
                other = claimed.get(key)
                if other is not None:
                    problems.append(
                        f"{where}: {key[1]!r} under {former.bucket!r} is already the "
                        f"former place of {other!r}; one playlist is left by one bucket"
                    )
                else:
                    claimed[key] = bucket.id
    return problems


def _band_names(bucket: Bucket, energy: Energy) -> dict[str, str]:
    """The bands and the no reading sub one bucket files into, by identifier.

    EMPTY FOR A BUCKET THAT DOES NOT SPLIT BY ENERGY. ONE BODY for
    :func:`live_places` and the split place check, so the two cannot disagree
    about which buckets have bands or what each band is called. Each under the
    bucket's own label for it.
    """
    if bucket.sub_by_source is not None or not energy.enabled or not bucket.energy.enabled:
        return {}
    names = {
        band.id: bucket.energy.band_display.get(band.id, band.display) for band in energy.bands
    }
    if energy.no_energy_sub is not None:
        names[energy.no_energy_sub.id] = energy.no_energy_sub.display
    return names


def _check_split_places(
    buckets: Sequence[Bucket],
    energy: Energy,
    sub_classes: Sequence[SubClass],
    version: int,
) -> list[str]:
    """Refuse a split place that is not one of its holder's live bands (U118).

    THE REVERSE OF :func:`_check_former_places`. A split place is left by the
    tracks whose genre names the declaring bucket and stays the holder's for
    every other track, so it has to be a place the holder still competes on,
    a band it files into or its own former place, under the name the holder
    gives it, or a move would leave a playlist the writer cannot find. The
    declaring bucket has to split by energy, since a track leaves the holder's
    place for the band its reading names. Its identifier is its own: not a place the declaring bucket
    already holds, and not shared with any other former or split place. And
    one band is split out by one bucket, since a track leaving it would
    otherwise be claimed twice.

    THE TEMPLATE HAS TO STATE THE VERSION THAT KNOWS ONE. See
    :data:`SPLIT_PLACE_SCHEMA_VERSION`.
    """
    problems: list[str] = []
    by_id = {bucket.id: bucket for bucket in buckets}
    seen = {former.id: bucket.id for bucket in buckets for former in bucket.formerly}
    claimed: dict[tuple[str, str], str] = {}
    for bucket in buckets:
        if bucket.split_from and version < SPLIT_PLACE_SCHEMA_VERSION:
            problems.append(
                f"[[bucket]] {bucket.id}: declares a split place under schema_version "
                f"{version}; write schema_version = {SPLIT_PLACE_SCHEMA_VERSION}, since a "
                f"build that reads version {version} ignores the declaration and files a "
                f"track into its new place while it still sits in the old one"
            )
        if bucket.split_from and not _band_names(bucket, energy):
            problems.append(
                f"[[bucket]] {bucket.id}: declares a split place and does not split by "
                f"energy; a track leaves the band it was split from for the band its "
                f"reading names here"
            )
        own_ids, _own_displays = live_places(bucket, energy, sub_classes)
        for place in bucket.split_from:
            where = f"[[bucket]] {bucket.id} split_from {place.id or place.display!r}"
            if not _ID.match(place.id):
                problems.append(f"{where}: id {place.id!r} must match {_ID.pattern}")
            if place.id in own_ids:
                problems.append(
                    f"{where}: id {place.id!r} is already a sub of this bucket; a split "
                    f"place competes under an identifier of its own"
                )
            if place.id in seen:
                problems.append(
                    f"{where}: id {place.id!r} is already a former or split place of "
                    f"{seen[place.id]!r}"
                )
            seen.setdefault(place.id, bucket.id)
            holder = by_id.get(place.bucket)
            if holder is None or holder.id == bucket.id:
                problems.append(
                    f"{where}: names bucket {place.bucket!r}, which is not another declared "
                    f"bucket; a split place is a band of the folder the genre was split from"
                )
                continue
            # A BAND OF THE HOLDER, OR THE HOLDER'S OWN FORMER PLACE. The second
            # is the playlist the genre sat in with the holder's before either
            # had a folder: Soul tracks left in NonElectronic's old "Soul / R&B"
            # playlist leave it for Soul, where R&B's former place alone would
            # send them nowhere.
            bands = _band_names(holder, energy)
            bands.update((former.id, former.display) for former in holder.formerly)
            if place.sub not in bands:
                problems.append(
                    f"{where}: {place.sub!r} is not a band or a former place of "
                    f"{place.bucket!r} ({sorted(bands)}); a split place is a playlist its "
                    f"holder still competes on, and one it stopped declaring is a former place"
                )
            elif place.display != bands[place.sub]:
                problems.append(
                    f"{where}: display {place.display!r} is not {bands[place.sub]!r}, the "
                    f"name {place.bucket!r} gives {place.sub!r}; a move finds the playlist "
                    f"it leaves by that name"
                )
            key = (place.bucket, place.sub)
            if key in claimed:
                problems.append(
                    f"{where}: {place.sub!r} under {place.bucket!r} is already split out by "
                    f"{claimed[key]!r}; one band is left by one bucket"
                )
            else:
                claimed[key] = bucket.id
    return problems


def _check_genre_subs(
    buckets: Sequence[Bucket],
    energy: Energy,
    sub_classes: Sequence[SubClass],
    version: int,
) -> list[str]:
    """Refuse a genre sub that is not a place of its own beside a bucket's bands (U155).

    It needs a bucket that splits by energy, since it sits beside the bands; a
    bucket that routes by source genre already files each source into a style
    sub of its own, and one with no energy dimension has a single sub. Its
    identifier and its name are its own: not a band under the bucket's label
    for it, not the no reading sub, not a sub class, not a declared sub, and
    not another genre sub of the bucket, or two places would be one playlist.
    Each source is an exact routing alias of the bucket, so a track wearing it
    is filed by this bucket and no other, and one source names one genre sub.

    THE TEMPLATE HAS TO STATE THE VERSION THAT KNOWS ONE. See
    :data:`GENRE_SUB_SCHEMA_VERSION`.
    """
    problems: list[str] = []
    for bucket in buckets:
        if not bucket.genre_subs:
            continue
        if version < GENRE_SUB_SCHEMA_VERSION:
            problems.append(
                f"[[bucket]] {bucket.id}: declares a genre sub under schema_version "
                f"{version}; write schema_version = {GENRE_SUB_SCHEMA_VERSION}, since a "
                f"build that reads version {version} ignores the declaration and files "
                f"the genre's tracks into their band alone"
            )
        if not _band_names(bucket, energy):
            problems.append(
                f"[[bucket]] {bucket.id}: declares a genre sub and does not split by "
                f"energy; a genre sub sits beside a bucket's bands, and a bucket that "
                f"routes by source genre files a source into a sub through its "
                f"sub_by_source map"
            )
        others = replace(bucket, genre_subs=())
        taken_ids, taken_displays = live_places(others, energy, sub_classes)
        aliases = set(bucket.aliases)
        claimed: dict[str, str] = {}
        seen_ids: set[str] = set()
        for genre in bucket.genre_subs:
            where = f"[[bucket]] {bucket.id} genre_sub {genre.id or genre.display!r}"
            if not _ID.match(genre.id):
                problems.append(f"{where}: id {genre.id!r} must match {_ID.pattern}")
            if not genre.display:
                problems.append(f"{where}: display must be a non-empty string")
            if genre.id in seen_ids:
                problems.append(
                    f"{where}: id {genre.id!r} is already another genre sub of this "
                    f"bucket; one identifier names one place"
                )
            elif genre.id in taken_ids:
                problems.append(
                    f"{where}: id {genre.id!r} is already a band, a sub or a sub class "
                    f"of this bucket; a genre sub is a place of its own"
                )
            if genre.display in taken_displays:
                problems.append(
                    f"{where}: display {genre.display!r} is already the name of a band, "
                    f"a sub or a sub class in this bucket's folder; two places of one "
                    f"name are one playlist"
                )
            seen_ids.add(genre.id)
            taken_displays.add(genre.display)
            if not genre.sources:
                problems.append(
                    f"{where}: sources must be a non-empty list of source genres, "
                    f"written sources = [\"Rominimal\"]"
                )
            for source in genre.sources:
                if source not in aliases:
                    problems.append(
                        f"{where}: source {source!r} is not an exact alias of this "
                        f"bucket, so a track wearing it may be filed by another bucket "
                        f"or by a keyword rule; add it to this bucket's aliases"
                    )
                if source in claimed:
                    problems.append(
                        f"{where}: source {source!r} already names the genre sub "
                        f"{claimed[source]!r}; one genre files into one genre sub"
                    )
                claimed.setdefault(source, genre.id)
    return problems


def _build_fallback(
    raw: Mapping[str, Any], by_id: Mapping[str, Bucket]
) -> tuple[Fallback, list[str]]:
    problems: list[str] = []
    bucket = str(raw.get("bucket", ""))
    if bucket not in by_id:
        problems.append(
            f"[fallback] bucket {bucket!r} is not a declared bucket; routing must always "
            f"land somewhere, so the landing place has to exist"
        )
    tagging_uses = bool(raw.get("tagging_uses_fallback", False))
    if tagging_uses:
        # R21's sibling rule, and the one the source system enforces by deleting
        # a tag rather than leaving a stale guess on the file.
        problems.append(
            "[fallback] tagging_uses_fallback is true; tagging must be allowed to decline. "
            "A blanket genre written onto a file outlives the run that guessed it"
        )
    return (
        Fallback(
            bucket=bucket,
            routing_uses_fallback=bool(raw.get("routing_uses_fallback", True)),
            tagging_uses_fallback=tagging_uses,
            too_coarse_as_source=tuple(raw.get("too_coarse_as_source") or ()),
        ),
        problems,
    )


def _build_sub_classes(
    raw: Sequence[Mapping[str, Any]], version: int
) -> tuple[tuple[SubClass, ...], list[str]]:
    problems: list[str] = []
    out: list[SubClass] = []
    additive_by_signal: dict[str, list[str]] = {}
    for entry in raw:
        entry_id = str(entry.get("id", ""))
        policy_raw = str(entry.get("policy", ""))
        if not _ID.match(entry_id):
            problems.append(f"[[sub_class]] id {entry_id!r} must match {_ID.pattern}")
        try:
            policy = SubPolicy(policy_raw)
        except ValueError:
            problems.append(
                f"[[sub_class]] {entry_id!r}: policy {policy_raw!r} must be one of "
                f"{[p.value for p in SubPolicy]}"
            )
            continue
        additive = bool(entry.get("additive", False))
        if additive and policy is not SubPolicy.DERIVED:
            problems.append(
                f"[[sub_class]] {entry_id!r}: additive is only meaningful for a derived sub, "
                f"which coexists with the sub a track is already in"
            )
        # THE SIGNAL (U119). Absent, it is the vocal reading, which is what
        # every class declared before the key existed meant. A playlist signal
        # names the playlist it mirrors and is only ever derived and additive,
        # and it needs the schema version that knows it, so a build that does
        # not refuses the copy by name rather than reading it as a vocal class.
        signal = str(entry.get("signal", SIGNAL_VOX))
        signal_playlist = str(entry.get("signal_playlist", "") or "").strip()
        if signal not in SIGNALS:
            problems.append(
                f"[[sub_class]] {entry_id!r}: signal {signal!r} must be one of "
                f"{sorted(SIGNALS)}"
            )
        elif signal == SIGNAL_PLAYLIST:
            if not signal_playlist:
                problems.append(
                    f"[[sub_class]] {entry_id!r}: a playlist signal names the playlist it "
                    f"mirrors in signal_playlist, and none is given"
                )
            if not (additive and policy is SubPolicy.DERIVED):
                problems.append(
                    f"[[sub_class]] {entry_id!r}: a playlist signal is derived and additive, "
                    f"since it mirrors another playlist beside the sub a track is already in"
                )
            if version < PLAYLIST_SIGNAL_SCHEMA_VERSION:
                problems.append(
                    f"[[sub_class]] {entry_id!r}: declares a playlist signal under "
                    f"schema_version {version}; write schema_version = "
                    f"{PLAYLIST_SIGNAL_SCHEMA_VERSION}, since a build that reads version "
                    f"{version} would take the class for a vocal one"
                )
        elif signal_playlist:
            problems.append(
                f"[[sub_class]] {entry_id!r}: signal_playlist is only meaningful for a "
                f"playlist signal"
            )
        if additive:
            additive_by_signal.setdefault(signal, []).append(entry_id)
        out.append(
            SubClass(
                id=entry_id,
                display=str(entry.get("display", "")),
                policy=policy,
                additive=additive,
                present_in=str(entry.get("present_in", "all_buckets")),
                signal=signal,
                signal_playlist=signal_playlist,
            )
        )
    for signal, ids in additive_by_signal.items():
        if len(ids) > 1:
            # ONE ADDITIVE CLASS PER SIGNAL (U119, lifting the one class limit
            # the pinned tree depth was once said to need): a second class on
            # one signal is one dimension declared twice, so the rebuild would
            # file every vocal track into two playlists for one reading.
            problems.append(
                f"{len(ids)} additive sub classes declared on the {signal!r} signal "
                f"({', '.join(ids)}); only one is supported per signal"
            )
    return tuple(out), problems


def _build_fuzzy(
    raw: Sequence[Mapping[str, Any]], by_id: Mapping[str, Bucket]
) -> tuple[tuple[FuzzyRule, ...], list[str]]:
    problems: list[str] = []
    out: list[FuzzyRule] = []
    for index, entry in enumerate(raw):
        keyword = str(entry.get("keyword", ""))
        bucket = str(entry.get("bucket", ""))
        if not keyword:
            problems.append(f"[[fuzzy]] {index}: keyword must be a non-empty string")
        if keyword != keyword.lower():
            problems.append(
                f"[[fuzzy]] {keyword!r}: keywords are matched against a lowercased source "
                f"string, so an uppercase keyword can never match"
            )
        if bucket not in by_id:
            problems.append(f"[[fuzzy]] {keyword!r}: bucket {bucket!r} is not declared")
        out.append(FuzzyRule(keyword, bucket))
    return tuple(out), problems


def _build_suggest(
    raw: Sequence[Mapping[str, Any]], by_id: Mapping[str, Bucket]
) -> tuple[tuple[SuggestRule, ...], list[str]]:
    problems: list[str] = []
    out: list[SuggestRule] = []
    for index, entry in enumerate(raw):
        equals = tuple(entry.get("equals") or ())
        all_of = tuple(entry.get("all_of") or ())
        any_of = tuple(entry.get("any_of") or ())
        where = f"[[suggest]] {index} ({list(equals) or list(all_of) or list(any_of)})"
        if not (equals or all_of or any_of):
            problems.append(f"{where}: needs equals, all_of, or any_of")
        if equals and (all_of or any_of):
            problems.append(
                f"{where}: mixes an exact match with a substring match, and the two run in "
                f"different passes, so the rule would fire twice with no defined precedence"
            )
        for needle in (*equals, *all_of, *any_of):
            if needle != needle.lower():
                problems.append(f"{where}: {needle!r} must be lowercase to ever match")

        bucket = entry.get("bucket")
        tag = entry.get("tag")
        decline = entry.get("decline")
        if bucket is not None and bucket not in by_id:
            problems.append(f"{where}: bucket {bucket!r} is not declared")
        if sum(x is not None for x in (bucket, tag, decline)) != 1:
            problems.append(
                f"{where}: declare exactly one of bucket, tag, decline; a rule that both "
                f"answers and declines has no defined result"
            )

        split_raw = entry.get("split")
        split = None
        if split_raw:
            split = Split(
                when_contains=str(split_raw.get("when_contains", "")),
                max_bpm=float(split_raw.get("max_bpm", 0)),
                below=str(split_raw.get("below", "")),
                at_or_above=str(split_raw.get("at_or_above", "")),
                unknown_bpm=str(split_raw.get("unknown_bpm", "")),
                unknown_bpm_needs_review=bool(split_raw.get("unknown_bpm_needs_review", True)),
            )
            for name in ("below", "at_or_above", "unknown_bpm"):
                target = getattr(split, name)
                if target not in by_id:
                    problems.append(f"{where}: split {name} {target!r} is not a declared bucket")
        out.append(SuggestRule(equals, all_of, any_of, bucket, tag, decline, split))
    return tuple(out), problems


def _build_gate(raw: Mapping[str, Any]) -> tuple[LabelGate, list[str]]:
    problems: list[str] = []
    share = float(raw.get("out_of_place_share", 0.10))
    if not 0.0 <= share <= 1.0:
        problems.append(f"[label_gate] out_of_place_share {share} must be between 0 and 1")
    rules: list[GateRule] = []
    for index, entry in enumerate(raw.get("rule") or []):
        # FOLDED LOWERCASE HERE, as the published rules' needles are, because a
        # word is matched lowercase and ``routing._rule_matches`` folds nothing.
        rule = GateRule(
            all_of=tuple(str(one).lower() for one in entry.get("all_of") or ()),
            any_of=tuple(str(one).lower() for one in entry.get("any_of") or ()),
            equals=tuple(str(one).lower() for one in entry.get("equals") or ()),
            family=entry.get("family"),
            keep=bool(entry.get("keep", False)),
        )
        if not (rule.all_of or rule.any_of or rule.equals):
            problems.append(f"[[label_gate.rule]] {index}: needs all_of, any_of, or equals")
        if rule.keep == (rule.family is not None):
            problems.append(
                f"[[label_gate.rule]] {index}: declare exactly one of keep or family"
            )
        rules.append(rule)
    published, published_problems = _build_published(raw.get("published"))
    problems += published_problems
    default_kind = raw.get("default_kind", DEFAULT_LABEL_KIND)
    kinds = {rule.kind for rule in published}
    if not isinstance(default_kind, str) or not KIND_NAME.fullmatch(
        default_kind.strip().lower()
    ):
        problems.append(
            f"[label_gate] default_kind must be a kind's name, one word, not {default_kind!r}"
        )
        default_kind = DEFAULT_LABEL_KIND
    default_kind = default_kind.strip().lower()
    # CHECKED ONLY WHEN SOMETHING IS DECLARED. A copy with no published rule
    # judges nothing, so its default names nothing that could be wrong.
    if published and default_kind != ANY_KIND and default_kind not in kinds:
        problems.append(
            f"[label_gate] default_kind {default_kind!r} is not a kind any "
            f"[[label_gate.published]] rule names ({', '.join(sorted(kinds))}), so "
            f"no release of a label left at the default would ever be judged; set "
            f"default_kind to one of those, or to {ANY_KIND!r}"
        )
    return LabelGate(tuple(rules), share, published, default_kind), problems


def _needles(entry: Mapping[str, Any], key: str) -> tuple[tuple[str, ...], bool]:
    """One matcher list, folded to lowercase, and whether it was a list of words.

    FOLDED HERE AND NOT AT EACH MATCH. A word is matched lowercase, and a needle
    typed with a capital would never match and would say nothing about it.
    """
    raw = entry.get(key)
    if raw is None:
        return (), True
    if not isinstance(raw, list) or not all(isinstance(one, str) and one.strip() for one in raw):
        return (), False
    return tuple(one.strip().lower() for one in raw), True


def _build_published(raw: Any) -> tuple[tuple[PublishedRule, ...], list[str]]:
    """The ``[[label_gate.published]]`` rules, and what is wrong with them.

    A RULE THAT COULD NEVER MATCH, OR THAT NAMES NO KIND, IS A PROBLEM AND NOT A
    SKIP. These rules decide what a sweep holds back, and one dropped silently
    would leave its words unknown, which the gate reads as not judged: the
    music the rule was written to hold would be filed with nothing said.
    """
    problems: list[str] = []
    if raw is None:
        return (), problems
    if not isinstance(raw, list):
        return (), [
            "[[label_gate.published]] must be a list of rules, written with two "
            "pairs of brackets"
        ]
    rules: list[PublishedRule] = []
    for index, entry in enumerate(raw):
        where = f"[[label_gate.published]] {index}"
        if not isinstance(entry, Mapping):
            problems.append(f"{where}: is not a table")
            continue
        matchers: dict[str, tuple[str, ...]] = {}
        for key in ("all_of", "any_of", "equals"):
            matchers[key], readable = _needles(entry, key)
            if not readable:
                problems.append(f"{where}: {key} must be a list of words")
        if not any(matchers.values()):
            problems.append(f"{where}: needs all_of, any_of, or equals")
        kind = entry.get("kind")
        if not isinstance(kind, str) or not kind.strip():
            problems.append(f"{where}: needs a kind")
            continue
        kind = kind.strip().lower()
        if not KIND_NAME.fullmatch(kind):
            problems.append(
                f"{where}: kind {kind!r} is not one word, and a label is marked "
                f"with a kind by typing it, so no label could be given this one"
            )
            continue
        if kind == ANY_KIND:
            problems.append(
                f"{where}: {ANY_KIND!r} is the kind of a label that passes everything "
                f"and cannot be the kind of a word"
            )
            continue
        if kind == NO_KIND:
            problems.append(
                f"{where}: {NO_KIND!r} is the word that clears a label's kind and "
                f"cannot be the kind of a word"
            )
            continue
        rules.append(PublishedRule(kind=kind, **matchers))
    return tuple(rules), problems


def _tag_place(
    tag: str,
    by_id: Mapping[str, Bucket],
    by_display: Mapping[str, str],
    routing_alias: Mapping[str, str],
    fallback: Fallback,
) -> tuple[tuple[str, str | None] | None, str]:
    """The place routing files one written genre in, or why it names no folder.

    THE FIRST TWO TIERS OF ``routing.resolve_bucket`` AND NOT THE OTHER TWO. A
    genre a table declares must be filed by a declaration: an exact routing
    alias, or a bucket's own name. A keyword rule is a guess and the fallback
    is nowhere, and a table that wrote a word either of those catches would
    put a genre on a file that this taxonomy has no folder for. Spelled here
    because routing imports this module and cannot be asked, and held to
    routing's own answer by a test over every string the template declares.
    The indexes are the loader's, built once, and the built taxonomy's.

    IN A BUCKET THAT FILES BY SOURCE GENRE THE TAG NEEDS A ROW OF ITS OWN in
    that bucket's map. The bucket's bare name has none and lands in the default
    sub, which is how Alternative came to be written as the bucket's name and
    filed under another style with its word lost (R-799). A word with no row
    lands there too, so both are refused, by the one test.
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


def _build_vocabularies(
    raw: Any,
    by_id: Mapping[str, Bucket],
    by_display: Mapping[str, str],
    routing_alias: Mapping[str, str],
    fallback: Fallback,
) -> tuple[tuple[Vocabulary, ...], list[str]]:
    """The ``[vocabulary.SOURCE]`` tables, and what is wrong with them (R-799).

    A ROW THAT CANNOT BE USED IS A PROBLEM AND NOT A SKIP. A word whose row was
    dropped silently would go on to the buckets' aliases, which is the filing
    the row was written to replace, and nothing would say so.

    THE SHAPE IS CHECKED BEFORE A ROW IS READ, for the reason the former place
    check gives: a person edits a library's copy by hand, and a table in the
    wrong shape must be a line to fix and not a crash.
    """
    problems: list[str] = []
    if raw is None:
        return (), problems
    if not isinstance(raw, Mapping):
        return (), [
            "[vocabulary] must be a table of sources, each written "
            "[vocabulary.NAME] with words, a list of rows"
        ]
    tables: list[Vocabulary] = []
    for source, table in raw.items():
        where = f"[vocabulary.{source}]"
        # LOWERCASE, AS A FILE'S RECORD NAMES THE SOURCE. A capital would be a
        # table no source is ever looked up under, and its words would go on
        # being filed by the buckets' aliases with nothing said.
        if not _ID.match(str(source)):
            problems.append(
                f"{where}: the source name must match {_ID.pattern}, the name a "
                f"file's record gives the source"
            )
            continue
        # A TABLE NOTHING READS IS REFUSED, NOT IGNORED. A misspelled name, or
        # a record shop's, would load clean and file every word as before.
        if source not in VOCABULARY_SOURCES:
            problems.append(
                f"{where}: no source's words are read through a table of this "
                f"name, so it would change nothing; the sources that are: "
                f"{', '.join(VOCABULARY_SOURCES)}"
            )
            continue
        rows = table.get("words") if isinstance(table, Mapping) else None
        if not isinstance(rows, list):
            problems.append(
                f"{where}: needs words, a list of rows, each a word and the tag "
                f"written for it"
            )
            continue
        seen: set[str] = set()
        words: list[VocabularyWord] = []
        for index, row in enumerate(rows):
            at = f"{where} words {index}"
            if not isinstance(row, Mapping):
                problems.append(f"{at}: is not a table")
                continue
            word, tag = row.get("word"), row.get("tag")
            if not isinstance(word, str) or not word.strip():
                problems.append(f"{at}: needs a word")
                continue
            word = word.strip()
            at = f"{at} ({word!r})"
            if not isinstance(tag, str) or not tag.strip():
                problems.append(f"{at}: needs a tag, the genre written for the word")
                continue
            if word.lower() in seen:
                problems.append(
                    f"{at}: the word is declared twice, and one word cannot go two ways"
                )
                continue
            seen.add(word.lower())
            place, problem = _tag_place(
                tag.strip(), by_id, by_display, routing_alias, fallback
            )
            if place is None:
                problems.append(f"{at}: {problem}")
                continue
            words.append(VocabularyWord(word, tag.strip(), place[0], place[1]))
        tables.append(Vocabulary(str(source), tuple(words)))
    return tuple(tables), problems


def _build_family(
    raw: Mapping[str, Any], buckets: Sequence[Bucket]
) -> tuple[FamilyAffinity, list[str]]:
    problems: list[str] = []
    supergroup = dict(raw.get("supergroup") or {})
    families = [b.family for b in buckets if b.family]
    for bucket in buckets:
        if bucket.family is not None and not str(bucket.family).strip():
            problems.append(f"[[bucket]] {bucket.id}: family must be a non-empty string if present")
    # A family with one member can never award a same-family bonus, which makes
    # it dead weight in the ranker rather than an error. Warned about in the
    # template, not rejected here: a user mid-way through re-grouping their tree
    # should not be blocked by it.
    for name in supergroup.values():
        if name not in families and name not in supergroup:
            problems.append(
                f"[family.supergroup] target {name!r} is neither a declared family nor itself "
                f"a supergroup key"
            )
    catch_all = raw.get("catch_all")
    if catch_all is not None and catch_all not in families:
        problems.append(
            f"[family] catch_all {catch_all!r} is not a family any bucket declares"
        )
    return (
        FamilyAffinity(
            same_genre=float(raw.get("same_genre", 1.0)),
            same_family=float(raw.get("same_family", 0.6)),
            same_supergroup=float(raw.get("same_supergroup", 0.4)),
            unrelated=float(raw.get("unrelated", 0.2)),
            unknown_anchor=float(raw.get("unknown_anchor", 0.5)),
            supergroup=supergroup,
            catch_all=catch_all,
        ),
        problems,
    )


def _build_alias_indexes(
    buckets: Sequence[Bucket],
) -> tuple[dict[str, str], dict[str, tuple[str, str | None]], list[str]]:
    """Build the two alias lookups and reject the collisions that matter.

    ROUTING aliases are matched exactly, case included, because the source
    strings they came from are exact vendor genre names. TAGGING aliases are
    matched case-insensitively, because the tagger reads them from web pages
    whose capitalisation varies.

    A tagging alias may deliberately disagree with routing: three source strings
    in the shipped default resolve to one bucket for routing and a different one
    for tagging, which is honest, documented drift the two old tables hid. What
    is never allowed is the SAME index disagreeing with itself.
    """
    problems: list[str] = []
    routing: dict[str, str] = {}
    tagging: dict[str, tuple[str, str | None]] = {}

    for bucket in buckets:
        for alias in bucket.aliases:
            if alias in routing and routing[alias] != bucket.id:
                problems.append(
                    f"alias {alias!r} is declared under both {routing[alias]!r} and "
                    f"{bucket.id!r}; one source string cannot route two ways"
                )
            routing[alias] = bucket.id

    # Bucket-level first, sub-level second: a sub alias is the more specific
    # statement, and the tagger's own table answers with the sub's name.
    #
    # AND WITHIN THE BUCKET LEVEL, ROUTING ALIASES FIRST AND TAGGING-ONLY ONES
    # SECOND (U118), for the same reason one level up: a word a bucket lists
    # for tagging alone is the more specific statement about what to write.
    # "Trap / Wave" routes to the breaks bucket and has always tagged as
    # Hip-Hop, through a sub alias while Hip-Hop was a sub. Hip-Hop is a bucket
    # now, so its word is a bucket's tagging alias and must still win over the
    # routing alias. Two routing aliases, or two tagging-only aliases, of two
    # buckets still refuse.
    tagged: dict[str, str] = {}
    for bucket in buckets:
        for alias in bucket.aliases:
            key = alias.lower().strip()
            existing = tagging.get(key)
            if existing is not None and existing != (bucket.id, None):
                problems.append(
                    f"tagging alias {alias!r} is claimed by both {existing} and "
                    f"({bucket.id!r}, None)"
                )
            tagging[key] = (bucket.id, None)
    for bucket in buckets:
        for alias in bucket.tag_aliases:
            key = alias.lower().strip()
            claimer = tagged.get(key)
            if claimer is not None and claimer != bucket.id:
                problems.append(
                    f"tagging alias {alias!r} is claimed by both ({claimer!r}, None) and "
                    f"({bucket.id!r}, None)"
                )
            tagged[key] = bucket.id
            tagging[key] = (bucket.id, None)
    for bucket in buckets:
        for sub in bucket.subs:
            for alias in sub.tag_aliases:
                key = alias.lower().strip()
                existing = tagging.get(key)
                if existing is not None and existing[0] != bucket.id and existing[1] is not None:
                    problems.append(
                        f"tagging alias {alias!r} is claimed by two different sub-playlists: "
                        f"{existing} and ({bucket.id!r}, {sub.id!r})"
                    )
                tagging[key] = (bucket.id, sub.id)
    # A GENRE SUB'S SOURCE TAGS AS THAT SUB (U155), last because it is the most
    # specific statement of all. Each source is one of its bucket's routing
    # aliases, which the bucket level pass above answers with the bucket's own
    # name, and the tagger would then rewrite ``Rominimal`` on a file to
    # ``Minimal / Deep Tech`` and take the track out of the very sub its genre
    # names. The loader has already refused a source that is not the bucket's.
    for bucket in buckets:
        for genre in bucket.genre_subs:
            for source in genre.sources:
                tagging[source.lower().strip()] = (bucket.id, genre.id)

    return routing, tagging, problems
