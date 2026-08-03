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

WHY IT TAKES NO CONFIGURATION. This module reads no config and imports none
(KTD23, seam decision S3). A resolver that reaches for global configuration
cannot be tested against two different taxonomies in one process, and proving
that a friend's differently-named tree routes correctly with no code change is
exactly the verification this unit owes. So a Taxonomy is a value the caller
supplies, and the only file this module reads is the read-only default that ships
inside the wheel.

WHY VALIDATION HAPPENS AT LOAD. Every rule below fails at load time and again in
the setup wizard, never at write time. A friend whose template omits a tempo
prior should learn during setup, not three hours into their first intake with a
library half-written.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from enum import Enum
from importlib import resources
from typing import Any, Mapping, Sequence

# A stable identifier. Lowercase snake, because it is compared, persisted, and
# never rendered. The pattern is enforced rather than documented so that a
# template cannot smuggle a display name in as an id and re-orphan state on the
# next rename (R19).
_ID = re.compile(r"^[a-z][a-z0-9_]*$")

SUPPORTED_SCHEMA_VERSIONS = frozenset({1})

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
    """A sub-playlist that exists under many buckets and carries a write policy."""

    id: str
    display: str
    policy: SubPolicy
    additive: bool = False
    present_in: str = "all_buckets"


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


@dataclass(frozen=True)
class LabelGate:
    rules: tuple[GateRule, ...] = ()
    out_of_place_share: float = 0.10


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

    # Indexes, built once at construction. They are derived data, so they can
    # never disagree with the declaration they came from.
    _by_id: Mapping[str, Bucket] = field(repr=False, default_factory=dict)
    _by_display: Mapping[str, str] = field(repr=False, default_factory=dict)
    _routing_alias: Mapping[str, str] = field(repr=False, default_factory=dict)
    _tagging_alias: Mapping[str, tuple[str, str | None]] = field(
        repr=False, default_factory=dict
    )

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
    cannot vary at runtime. A library's active template is read by the caller and
    passed to :func:`load_taxonomy` as text.
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
    """
    found = []
    for item in (resources.files("cratekit") / "templates").iterdir():
        name = item.name
        if name.startswith(_TEMPLATE_PREFIX) and name.endswith(_TEMPLATE_SUFFIX):
            found.append(name[len(_TEMPLATE_PREFIX) : -len(_TEMPLATE_SUFFIX)])
    return tuple(sorted(found))


def shipped_template_text(name: str) -> str:
    """The packaged text of one template, by its short name.

    Raises ``FileNotFoundError`` when nothing ships under that name, which is the
    answer a caller wants: the shipped set is read-only data, so a name outside
    it is a configuration error rather than a transient failure.
    """
    source = resources.files("cratekit") / "templates" / f"{_TEMPLATE_PREFIX}{name}{_TEMPLATE_SUFFIX}"
    return source.read_text(encoding="utf-8")


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
    declared_nodes = [(tree, "tree"), (intake, "intake")]
    if catalog is not None:
        declared_nodes.append((catalog, "catalog"))
    for node, label in declared_nodes:
        if not _ID.match(node.id):
            problems.append(f"[{label}] id {node.id!r} must match {_ID.pattern}")
        if not node.display:
            problems.append(f"[{label}] display must be a non-empty string")
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

    sub_classes, sub_class_problems = _build_sub_classes(data.get("sub_class") or [])
    problems += sub_class_problems

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
        _by_id=by_id,
        _by_display={b.display: b.id for b in buckets},
        _routing_alias=routing_alias,
        _tagging_alias=tagging_alias,
    )


# ---------------------------------------------------------------------------
# Section builders. Each returns (value, problems) so one bad section never
# hides the next one.
# ---------------------------------------------------------------------------


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
            )
        )

    if not buckets:
        problems.append("no [[bucket]] declared; a taxonomy with no buckets routes nothing")
    return tuple(buckets), problems


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


def _build_sub_classes(raw: Sequence[Mapping[str, Any]]) -> tuple[tuple[SubClass, ...], list[str]]:
    problems: list[str] = []
    out: list[SubClass] = []
    additive_seen = 0
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
        if additive:
            additive_seen += 1
        if additive and policy is not SubPolicy.DERIVED:
            problems.append(
                f"[[sub_class]] {entry_id!r}: additive is only meaningful for a derived sub, "
                f"which coexists with the sub a track is already in"
            )
        out.append(
            SubClass(
                id=entry_id,
                display=str(entry.get("display", "")),
                policy=policy,
                additive=additive,
                present_in=str(entry.get("present_in", "all_buckets")),
            )
        )
    if additive_seen > 1:
        # KTD14 pins the tree at three levels, so a track can hold at most one
        # additional membership per bucket without a fourth level to hold it.
        problems.append(
            f"{additive_seen} additive sub classes declared; only one is supported at the "
            f"pinned tree depth"
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
        rule = GateRule(
            all_of=tuple(entry.get("all_of") or ()),
            any_of=tuple(entry.get("any_of") or ()),
            equals=tuple(entry.get("equals") or ()),
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
    return LabelGate(tuple(rules), share), problems


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

    for bucket in buckets:
        # Bucket-level first, sub-level second: a sub alias is the more specific
        # statement, and the tagger's own table answers with the sub's name.
        for alias in (*bucket.aliases, *bucket.tag_aliases):
            key = alias.lower().strip()
            existing = tagging.get(key)
            if existing is not None and existing != (bucket.id, None):
                problems.append(
                    f"tagging alias {alias!r} is claimed by both {existing} and "
                    f"({bucket.id!r}, None)"
                )
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

    return routing, tagging, problems
