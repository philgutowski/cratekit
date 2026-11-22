"""Routing and tagging over a declared taxonomy. One table, two entry points.

Two entry points, not one resolver: routing must ALWAYS land, because a plan
keyed by (bucket, sub) loses a track with no answer, while tagging must be able
to DECLINE, because a coarse guess written onto a file outlives the run that
guessed it. So they share one table and stay two functions.

Nothing here reads configuration (KTD23, S3, D7). The taxonomy is an argument,
so two taxonomies can be exercised in one process, and the vocal threshold is a
value the caller supplies, so an absent one routes no track as vocal instead of
raising on a slim install. Tag readers live in the tags module (S5); everything
here takes VALUES, never paths.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from cratekit.core.taxonomy import (
    ANY_KIND,
    BpmPrior,
    Bucket,
    FormerPlace,
    GateRule,
    GenreSub,
    PublishedRule,
    SplitPlace,
    Sub,
    Taxonomy,
)


class Match(str, Enum):
    """How a routing answer was reached.

    Carried on every result so a summary can show the fallback rate, as a value
    rather than prose from a lower layer (D2).
    """

    EXACT = "exact"
    PASSTHROUGH = "passthrough"
    FUZZY = "fuzzy"
    FALLBACK = "fallback"


class Decline(str, Enum):
    """Why tagging refused to answer. A decline is a result, not a failure."""

    ASK = "ask"
    REVIEW = "review"
    NOT_FOUND = "not_found"


class GateVerdict(str, Enum):
    KEEP = "keep"
    DROP = "drop"


class KindVerdict(str, Enum):
    """What the label gate says about one release's published words (R-798)."""

    PASS = "passed"
    HOLD = "held"
    NOT_JUDGED = "not-judged"


@dataclass(frozen=True)
class KindJudgment:
    """One release judged against the kind its label is followed as.

    ``kind`` is the label's kind as judged, the default filled in. ``placed`` is
    every published word a rule knew, with its kind, in the catalogue's order.
    ``reason`` is the sentence a person reads.
    """

    verdict: KindVerdict
    kind: str
    placed: tuple[tuple[str, str], ...]
    reason: str


@dataclass(frozen=True)
class Resolution:
    """A routing answer. ``bucket_id`` is always a declared bucket."""

    bucket_id: str
    match: Match
    matched_on: str | None = None


@dataclass(frozen=True)
class Suggestion:
    """A tagging answer, which may decline.

    ``tag`` is the string to write onto the file, and may come with no bucket
    when the source names something the taxonomy has no folder for.
    ``needs_review`` is not a decline: the answer stands but a human should
    confirm it, as when the tempo rule had no tempo to split on.

    ``off_taxonomy`` means the tag is the source's own word and this template has
    no place for it. Only the last tier sets it, and not for a bucket's own
    display. It is about the WORD on the file, not where the track lands, and
    ``bucket_id is None`` does not imply it. A caller asking whether the taxonomy
    recognized the string asks ``not declined and not off_taxonomy``.
    """

    bucket_id: str | None = None
    sub_id: str | None = None
    tag: str | None = None
    decline: Decline | None = None
    needs_review: bool = False
    off_taxonomy: bool = False

    @property
    def declined(self) -> bool:
        return self.decline is not None


# ---------------------------------------------------------------------------
# Entry point 1: routing. Total. Never raises. Always lands.
# ---------------------------------------------------------------------------


def resolve_bucket(taxonomy: Taxonomy, raw_genre: str | None) -> Resolution:
    """Resolve any source genre string to a declared bucket.

    Four tiers, in order, and the order is behaviour:

    1. an exact declared alias, case sensitive, since vendor names are exact;
    2. the value already IS a bucket's display, as the tagger writes them back;
    3. the first ordered keyword rule whose substring is in the lowercased value;
    4. the declared fallback bucket, so this never returns None or raises, and
       ``match`` shows that it did not resolve.
    """
    value = raw_genre or ""

    bucket_id = taxonomy.routing_alias(value)
    if bucket_id is not None:
        return Resolution(bucket_id, Match.EXACT, value)

    bucket_id = taxonomy.bucket_for_display(value)
    if bucket_id is not None:
        return Resolution(bucket_id, Match.PASSTHROUGH, value)

    lowered = value.lower()
    for rule in taxonomy.fuzzy:
        if rule.keyword in lowered:
            return Resolution(rule.bucket, Match.FUZZY, rule.keyword)

    return Resolution(taxonomy.fallback.bucket, Match.FALLBACK, None)


# ---------------------------------------------------------------------------
# Entry point 2: tagging. Allowed to decline.
# ---------------------------------------------------------------------------


def suggest_tag(
    taxonomy: Taxonomy, raw_genre: str | None, *, bpm: float | None = None, source: str | None = None
) -> Suggestion:
    """Suggest the genre tag to write onto a file, or decline.

    When the taxonomy declares a vocabulary for ``source``, that table is asked
    first (R-799); a word with no row goes on to the passes below.

    1. nothing at all declines as not-found;
    2. the better-informed rules, before the aliases: an EXACT refusal of a
       source's catch-all bucket, and a rule that reads TEMPO;
    3. an exact declared alias, which beats a substring guess;
    4. the ordered substring corrections;
    5. otherwise the source's own string passes through, and only this tier
       sets ``off_taxonomy`` (R-650).

    No tier invents a bucket; a template declaring otherwise is refused at load.
    """
    value = (raw_genre or "").strip()
    if not value:
        return Suggestion(decline=Decline.NOT_FOUND)

    lowered = value.lower()

    table = taxonomy.vocabulary(source) if source is not None else None
    row = table.get(lowered) if table is not None else None
    if row is not None:
        return Suggestion(bucket_id=row.bucket, sub_id=row.sub, tag=row.tag)

    for rule in taxonomy.suggest:
        if not (rule.equals or rule.split):
            continue
        if _rule_matches(rule, lowered):
            return _apply_suggest_rule(taxonomy, rule, lowered, bpm)

    hit = taxonomy.tagging_alias(lowered)
    if hit is not None:
        bucket_id, sub_id = hit
        genre = _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id)
        if genre is not None:
            # A genre sub is written as the source this word matched, in its
            # declared spelling, since routing files it by source exactly (U155).
            spelled = next(
                (source for source in genre.sources if source.lower().strip() == lowered),
                genre.sources[0],
            )
            return Suggestion(bucket_id=bucket_id, sub_id=sub_id, tag=spelled)
        return Suggestion(bucket_id=bucket_id, sub_id=sub_id, tag=display_of(taxonomy, hit))

    for rule in taxonomy.suggest:
        if rule.equals or rule.split:
            continue
        if _rule_matches(rule, lowered):
            return _apply_suggest_rule(taxonomy, rule, lowered, bpm)

    # The last tier flags every word except a BUCKET's own display, which
    # ``resolve_bucket``'s second tier places byte for byte. A sub's display or
    # another case lands in the fallback, so it is flagged (R-650).
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)


def display_of(taxonomy: Taxonomy, hit: tuple[str, str | None]) -> str:
    """The name a bucket and sub pair carries: the sub's, or the bucket's own."""
    bucket_id, sub_id = hit
    bucket = taxonomy.bucket(bucket_id)
    if sub_id is None:
        return bucket.display
    sub = _sub_by_id(bucket, sub_id)
    return bucket.display if sub is None else sub.display


def _apply_suggest_rule(taxonomy, rule, lowered: str, bpm: float | None) -> Suggestion:
    if rule.decline is not None:
        return Suggestion(decline=Decline(rule.decline))

    if rule.split is not None and rule.split.when_contains in lowered:
        split = rule.split
        if bpm is None:
            # No tempo to split on: take the declared safe side and ask for a look.
            bucket = taxonomy.bucket(split.unknown_bpm)
            return Suggestion(
                bucket_id=bucket.id, tag=bucket.display, needs_review=split.unknown_bpm_needs_review
            )
        target = split.below if bpm < split.max_bpm else split.at_or_above
        bucket = taxonomy.bucket(target)
        return Suggestion(bucket_id=bucket.id, tag=bucket.display)

    if rule.bucket is not None:
        bucket = taxonomy.bucket(rule.bucket)
        return Suggestion(bucket_id=bucket.id, tag=bucket.display)

    # A literal tag with no bucket, declared on purpose by the template author,
    # so it is not off taxonomy: nobody needs telling about it.
    return Suggestion(tag=rule.tag)


# ---------------------------------------------------------------------------
# Energy
# ---------------------------------------------------------------------------


def energy_sub(
    taxonomy: Taxonomy, bucket_id: str, level: int | None, *, source_genre: str = ""
) -> Sub | None:
    """The sub-playlist a track belongs in, or None to leave it where it is.

    The tier order is load-bearing: a bucket routing by source genre is checked
    first and never consults energy, and a bucket with no energy dimension is
    checked before the missing level, so its track lands in its single sub.
    None is a real answer, no place declared below the bucket, not an error.
    """
    bucket = taxonomy.bucket(bucket_id)

    if bucket.sub_by_source is not None:
        target = bucket.sub_by_source.map.get(source_genre, bucket.sub_by_source.default)
        return _sub_by_id(bucket, target)

    if not taxonomy.energy.enabled or not bucket.energy.enabled:
        return bucket.single_sub

    if level is None:
        return taxonomy.energy.no_energy_sub

    for band in taxonomy.energy.bands:
        if level <= band.max:
            # The BAND's id, so buckets splitting at the same levels key state
            # identically whatever they label their bands.
            return Sub(band.id, bucket.energy.band_display.get(band.id, band.display))
    # Unreachable while the loader holds; explicit so an out-of-range level
    # never returns None and reads as "no place declared".
    last = taxonomy.energy.bands[-1]
    return Sub(last.id, bucket.energy.band_display.get(last.id, last.display))


def genre_sub(taxonomy: Taxonomy, bucket_id: str, source_genre: str | None) -> Sub | None:
    """The genre sub a track files into beside its band, or None (U155).

    Exact and case sensitive, like a ``sub_by_source`` row. Additive: never
    :func:`energy_sub`'s answer nor one of :func:`competing_subs`, and only on a
    bucket that splits by energy.
    """
    value = source_genre or ""
    for genre in taxonomy.bucket(bucket_id).genre_subs:
        if value in genre.sources:
            return Sub(genre.id, genre.display)
    return None


def genre_sub_named(taxonomy: Taxonomy, bucket_id: str, sub_id: str) -> bool:
    """Whether a sub identifier is one of a bucket's genre subs (U155)."""
    return _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id) is not None


class Competing(str, Enum):
    """What kind of place a bucket's exclusive subs are, which a report counts by."""

    #: The energy bands and the no reading sub beside them.
    BAND = "band"

    #: The style subs of a bucket that does not split by energy.
    STYLE = "style"


def competing_subs(taxonomy: Taxonomy, bucket_id: str) -> tuple[Competing, frozenset[str]]:
    """The subs of one bucket a track may hold only one of, and their kind.

    The tier order is :func:`energy_sub`'s own: a bucket routing by source genre
    or with no energy dimension competes on its style subs and single sub, any
    other on its bands and the no reading sub. Identifiers, never displays (R19,
    D5). A sub class or a genre sub is never in the set, since it sits beside
    the band (U155). Every place of :func:`left_only` competes too: a former place
    where declared and where held (R-797), a split place where declared (U118).
    """
    bucket = taxonomy.bucket(bucket_id)
    classes = {entry.id for entry in taxonomy.sub_classes}
    former = left_only(taxonomy, bucket_id)

    if bucket.sub_by_source is not None or not taxonomy.energy.enabled or not bucket.energy.enabled:
        found = {sub.id for sub in bucket.subs}
        if bucket.single_sub is not None:
            found.add(bucket.single_sub.id)
        return Competing.STYLE, frozenset((found | former) - classes)

    found = {band.id for band in taxonomy.energy.bands}
    if taxonomy.energy.no_energy_sub is not None:
        found.add(taxonomy.energy.no_energy_sub.id)
    return Competing.BAND, frozenset((found | former) - classes)


def former_places(taxonomy: Taxonomy, bucket_id: str) -> tuple[tuple[str, FormerPlace], ...]:
    """Every former place that competes in one bucket, with the bucket declaring it.

    Declared and held ones, in declared order, read off the loader's index.
    """
    return taxonomy.former_places(bucket_id)


def former_place(taxonomy: Taxonomy, bucket_id: str, sub_id: str) -> FormerPlace | None:
    """The former place one of a bucket's competing subs is, or None.

    The same place whether asked of the declaring bucket or the holding one.
    """
    for _declarer, place in former_places(taxonomy, bucket_id):
        if place.id == sub_id:
            return place
    return None


def left_only(taxonomy: Taxonomy, bucket_id: str) -> frozenset[str]:
    """The competing subs of one bucket that a track is only ever moved OUT of.

    Every former place competing there and every split place it declares, one
    answer for what competes and what a track with no reading may still leave.
    """
    return frozenset(
        {place.id for _declarer, place in former_places(taxonomy, bucket_id)}
        | {place.id for place in taxonomy.bucket(bucket_id).split_from}
    )


def split_places(taxonomy: Taxonomy, bucket_id: str) -> tuple[tuple[str, SplitPlace], ...]:
    """Every split place one bucket declares or holds, with the declaring bucket."""
    return taxonomy.split_places(bucket_id)


def split_place(taxonomy: Taxonomy, bucket_id: str, sub_id: str) -> SplitPlace | None:
    """The split place one of a bucket's competing subs is, or None.

    Only a place the bucket DECLARES; in the holder the band is its own.
    """
    for place in taxonomy.bucket(bucket_id).split_from:
        if place.id == sub_id:
            return place
    return None


class Folder(str, Enum):
    """What a genre has in the tree, which is what a folder suggestion asks."""

    #: A top level folder answers for it: a bucket that files by energy or
    #: holds one sub, reached by an alias, a keyword or the bucket's own name.
    OWN = "own"

    #: It is a style sub under a folder that routes by source genre.
    SUB = "sub"

    #: It lands in such a folder's default sub, with no row of its own.
    DEFAULT = "default"

    #: Nothing declared claims it, and routing fell back.
    NONE = "none"


@dataclass(frozen=True, slots=True)
class GenreFolder:
    """Where one genre is filed and whether that is a folder of its own."""

    kind: Folder
    bucket_id: str
    sub_id: str | None = None


def folder_of(taxonomy: Taxonomy, raw_genre: str | None) -> GenreFolder:
    """What one genre string has in the tree (R-797).

    Through :func:`resolve_bucket` alone. The fallback tier is no folder. In a
    bucket routing by source genre, a map row is a style sub and any other string
    lands in the default, except the bucket's own name, which is its folder.
    """
    value = raw_genre or ""
    resolution = resolve_bucket(taxonomy, value)
    if resolution.match is Match.FALLBACK:
        return GenreFolder(Folder.NONE, resolution.bucket_id)
    bucket = taxonomy.bucket(resolution.bucket_id)
    by_source = bucket.sub_by_source
    if by_source is None or resolution.match is Match.PASSTHROUGH:
        return GenreFolder(Folder.OWN, bucket.id)
    if value in by_source.map:
        return GenreFolder(Folder.SUB, bucket.id, by_source.map[value])
    return GenreFolder(Folder.DEFAULT, bucket.id, by_source.default)


def energy_rating(taxonomy: Taxonomy, level: int | None) -> int | None:
    """Map an energy level to a star-rating integer, or None with no reading.

    Independent of the band cuts, so moving a band boundary never re-rates a
    library.
    """
    if level is None:
        return None
    for cut in taxonomy.energy.rating_cuts:
        if level <= cut.max:
            return cut.rating
    return taxonomy.energy.rating_cuts[-1].rating if taxonomy.energy.rating_cuts else None


def no_energy_sub(taxonomy: Taxonomy, bucket_id: str) -> Sub | None:
    """The sink a bucket sweeps out of, or None when it declares none."""
    bucket = taxonomy.bucket(bucket_id)
    if bucket.sub_by_source is not None or not bucket.energy.enabled:
        return None
    return taxonomy.energy.no_energy_sub


def rates(taxonomy: Taxonomy, bucket_id: str) -> bool:
    """Whether automation may write a star rating for tracks in this bucket."""
    return taxonomy.bucket(bucket_id).rates


def routes_with_vox(voxlevel: int | None, threshold: float | None) -> bool:
    """Whether a vocal-prominence reading clears the cut for the additive sub.

    The threshold is passed in, never fetched; an absent one routes nothing.
    """
    if voxlevel is None or threshold is None:
        return False
    return voxlevel >= threshold


# ---------------------------------------------------------------------------
# Tempo priors
# ---------------------------------------------------------------------------


def bpm_prior(taxonomy: Taxonomy, raw_genre: str | None) -> BpmPrior | None:
    """The tempo detection window for a source genre, via its bucket.

    Through the bucket, never a table keyed by folder display name, which
    matched nothing in a library named differently. None when the bucket
    declares no window, so the caller can refuse rather than use a default.
    """
    return taxonomy.bucket(resolve_bucket(taxonomy, raw_genre).bucket_id).bpm


# ---------------------------------------------------------------------------
# The family projection (a parallel vocabulary, not a merge)
# ---------------------------------------------------------------------------


def family_of(taxonomy: Taxonomy, raw_genre: str | None) -> str | None:
    """The family of whatever bucket this genre resolves to, a projection off it."""
    return taxonomy.bucket(resolve_bucket(taxonomy, raw_genre).bucket_id).family


def _supergroup_of(taxonomy: Taxonomy, family: str | None) -> str | None:
    if family is None:
        return None
    return taxonomy.family.supergroup.get(family, family)


def genre_affinity(taxonomy: Taxonomy, anchor_genre: str | None, cand_genre: str | None) -> float:
    """A soft genre prior for ranking. Never a hard exclude.

    An unknown anchor scores neutral, so genre neither helps nor hurts.
    """
    if not (anchor_genre or "").strip():
        return taxonomy.family.unknown_anchor

    anchor = (anchor_genre or "").strip().lower()
    candidate = (cand_genre or "").strip().lower()
    if anchor and anchor == candidate:
        return taxonomy.family.same_genre

    anchor_family = family_of(taxonomy, anchor_genre)
    cand_family = family_of(taxonomy, cand_genre)
    catch_all = taxonomy.family.catch_all

    if anchor_family == cand_family and anchor_family != catch_all:
        return taxonomy.family.same_family
    anchor_super = _supergroup_of(taxonomy, anchor_family)
    cand_super = _supergroup_of(taxonomy, cand_family)
    if anchor_super == cand_super and anchor_super != catch_all:
        return taxonomy.family.same_supergroup
    return taxonomy.family.unrelated


# ---------------------------------------------------------------------------
# The acquisition gate (keyed on the SOURCE vocabulary, deliberately)
# ---------------------------------------------------------------------------


def gate_family(taxonomy: Taxonomy, source_genre: str | None) -> str | None:
    """Classify a source genre into a candidate-drop family, or None to keep.

    Keyed on the SOURCE genre, never its bucket: an uncertain folder can still
    be a confident family. Timid: an empty or unclaimed string keeps.
    """
    value = (source_genre or "").strip().lower()
    if not value:
        return None
    for rule in taxonomy.label_gate.rules:
        if not _rule_matches(rule, value):
            continue
        return None if rule.keep else rule.family
    return None


def _rule_matches(rule: GateRule | PublishedRule, value: str) -> bool:
    """Whether one rule claims a lowercase word, the one matcher of every table.

    Every needle is folded lowercase by the loader, so nothing is folded here.
    """
    return bool(
        (rule.equals and value in rule.equals)
        or (rule.all_of and all(needle in value for needle in rule.all_of))
        or (rule.any_of and any(needle in value for needle in rule.any_of))
    )


def gate_decisions(
    taxonomy: Taxonomy,
    source_genres: Sequence[str | None],
    *,
    out_of_place_share: float | None = None,
) -> list[GateVerdict]:
    """Keep or drop each track, judged against the WHOLE catalogue at once.

    The share counts only tracks the source classified, so the unclassified do
    not dilute it. A family drops only as a small minority of the label's output.
    """
    share = (
        taxonomy.label_gate.out_of_place_share if out_of_place_share is None else out_of_place_share
    )
    families = [gate_family(taxonomy, g) for g in source_genres]
    classified = sum(1 for g in source_genres if (g or "").strip())
    if classified == 0:
        return [GateVerdict.KEEP] * len(source_genres)
    counts = Counter(f for f in families if f)
    out_of_place = {f for f, n in counts.items() if n / classified < share}
    return [
        GateVerdict.DROP if (f and f in out_of_place) else GateVerdict.KEEP for f in families
    ]


# ---------------------------------------------------------------------------
# The same gate, asked about KIND, over a general catalogue's vocabulary
# ---------------------------------------------------------------------------


def published_kind(taxonomy: Taxonomy, word: str | None) -> str | None:
    """The kind of music a general catalogue's word is, or None when no rule knows it.

    The first matching rule wins. None is never a kind (R-798).
    """
    value = (word or "").strip().lower()
    if not value:
        return None
    for rule in taxonomy.label_gate.published:
        if _rule_matches(rule, value):
            return rule.kind
    return None


def label_kind(taxonomy: Taxonomy, kind: str | None) -> str:
    """The kind a label is judged as: its own when it names one, else the default."""
    named = (kind or "").strip().lower()
    return named or taxonomy.label_gate.default_kind


def kind_settled(taxonomy: Taxonomy, kind: str | None) -> KindJudgment | None:
    """The judgment no published word could change, or None when the words decide.

    A label followed for ``any`` kind passes; a taxonomy with no rule for this
    vocabulary, or a kind it does not name, is not judged.
    """
    gate = taxonomy.label_gate
    judged_as = label_kind(taxonomy, kind)
    if judged_as == ANY_KIND:
        return KindJudgment(
            KindVerdict.PASS, judged_as, (), "its label is followed for any kind of music"
        )
    if not gate.published:
        return KindJudgment(
            KindVerdict.NOT_JUDGED, judged_as, (),
            "the library's taxonomy declares no rule for the general catalogue's "
            "genre words, so the gate has nothing to judge with",
        )
    if judged_as not in gate.kinds:
        return KindJudgment(
            KindVerdict.NOT_JUDGED, judged_as, (),
            f"its label is marked as kind {judged_as!r}, which the library's taxonomy "
            f"does not name (it names {', '.join(gate.kinds)}, or {ANY_KIND})",
        )
    return None


def kind_verdict(taxonomy: Taxonomy, kind: str | None, genres: Sequence[str]) -> KindJudgment:
    """Pass, hold or decline to judge one release, by what kind of music it is.

    ``genres`` is every word the catalogue publishes, in order; ``kind`` is the
    label's, or None for the default. Unlike :func:`gate_decisions` this judges
    one release alone (R-798). One word of the label's kind passes; a hold needs
    a known word of another kind and none of the label's; everything else is not
    judged, because a hold on a guess is music a person never sees.
    """
    settled = kind_settled(taxonomy, kind)
    if settled is not None:
        return settled
    judged_as = label_kind(taxonomy, kind)
    words = tuple(word.strip() for word in genres if isinstance(word, str) and word.strip())
    if not words:
        return KindJudgment(
            KindVerdict.NOT_JUDGED, judged_as, (), "the general catalogue publishes no genre for it"
        )
    placed = tuple(
        (word, found) for word in words if (found := published_kind(taxonomy, word)) is not None
    )
    said = ", ".join(words)
    if any(found == judged_as for _word, found in placed):
        return KindJudgment(
            KindVerdict.PASS, judged_as, placed,
            f"the general catalogue calls it {said}, and its label is followed as {judged_as}",
        )
    if placed:
        others = ", ".join(dict.fromkeys(found for _word, found in placed))
        return KindJudgment(
            KindVerdict.HOLD, judged_as, placed,
            f"the general catalogue calls it {said}, which is {others} and not "
            f"{judged_as}, the kind its label is followed as",
        )
    return KindJudgment(
        KindVerdict.NOT_JUDGED, judged_as, (),
        f"the general catalogue calls it {said}, and no rule of the gate knows "
        f"what kind of music that is",
    )


def _genre_sub_by_id(bucket: Bucket, sub_id: str | None) -> GenreSub | None:
    return next((genre for genre in bucket.genre_subs if genre.id == sub_id), None)


def _sub_by_id(bucket: Bucket, sub_id: str) -> Sub | None:
    return next((sub for sub in bucket.subs if sub.id == sub_id), None)
