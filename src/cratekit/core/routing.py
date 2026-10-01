"""Routing and tagging over a declared taxonomy. One table, two entry points.

WHY TWO ENTRY POINTS AND NOT ONE RESOLVER. Nine call sites in the system this
replaces need an answer that ALWAYS lands: they build a plan keyed by (bucket,
sub), and a missing answer means the track enters the collection with no place in
the tree and quietly disappears from it. Five other call sites need to be allowed
to DECLINE: on a decline they write nothing, and one of them actively deletes the
existing genre tag, because a coarse guess written onto a file outlives the run
that guessed it. Merging the two either reintroduces the blanket guess into
tagging or makes routing raise. So they share one table and stay two functions.

WHY NOTHING HERE READS CONFIGURATION. Every function takes the taxonomy as an
argument (KTD23, seam decisions S3 and D7). Two consequences are load-bearing:

* The vocal threshold is a value the CALLER supplies. The old router reached
  UPWARD, lazily, into an analysis module to fetch it. That module is an optional
  extra, so on a slim install the router raised ImportError the first time a
  track needed vocal routing, and the traceback named an import inside a function
  rather than the packaging decision behind it. Here, an absent threshold routes
  no track as vocal and raises nothing.
* Two taxonomies can be exercised in one process, which is the only way to prove
  that a friend's differently-named tree routes correctly with no code change.

WHY THE TAG READERS ARE NOT HERE. Four functions that read tags off disk used to
live beside this logic. They do real input, which the domain layer does not do,
and they belong with the writer that has to agree with them on container
dispatch. They now live in the tags module (seam decision S5). Everything here
takes VALUES, never paths.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from cratekit.core.taxonomy import BpmPrior, Bucket, FormerPlace, Sub, Taxonomy


class Match(str, Enum):
    """How a routing answer was reached.

    Carried on every result so a summary can show the fallback rate instead of
    hiding it. The old resolver returned a human-readable note for exactly this
    purpose and two sweeps printed it; a structured value renders the same line
    without a lower layer writing prose (seam decision D2).
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


@dataclass(frozen=True)
class Resolution:
    """A routing answer. ``bucket_id`` is always a declared bucket."""

    bucket_id: str
    match: Match
    matched_on: str | None = None


@dataclass(frozen=True)
class Suggestion:
    """A tagging answer, which may decline.

    ``tag`` is the string to write onto the file. It can be present with no
    bucket: a source vocabulary can name something the taxonomy has no folder
    for, and preserving the source's own word is better than forcing it into a
    bucket that does not describe it.

    ``needs_review`` is not a decline. It means the answer stands but a human
    should confirm it, which is how the one tempo-dependent rule reports that it
    had no tempo to split on.

    ``off_taxonomy`` means the tag above is the source's own word and this
    template has no place of its own for it. It can only be true on the LAST
    tier, and it is not true of everything that tier answers: a bucket's own
    display reaches it as well, and routing recognises that one exactly.

    IT IS NOT A STATEMENT ABOUT WHERE THE TRACK LANDS, and reading it as one
    goes wrong in both directions. ``Psy-Trance`` is off taxonomy on the shipped
    template and a fuzzy routing rule still puts it in the trance bucket, while
    a SUB's display is a declared word that routing leaves in the fallback. This
    flag is about the WORD written onto the file, which is what decides whether
    the library's own vocabulary still describes what is on disk.

    It is stated here rather than inferred by a caller because ``bucket_id is
    None`` does not mean it, twice over. A declared rule carrying a literal tag
    and no bucket produces exactly that shape on purpose, and so does a bucket
    display with no alias of its own. A caller that wants to know whether this
    taxonomy RECOGNIZED the string asks ``not declined and not off_taxonomy``.
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

    1. an exact declared alias, matched case-sensitively because vendor genre
       names are exact strings;
    2. the value already IS a bucket's display name, which happens constantly
       because the tagger writes bucket names back onto files;
    3. the first ordered keyword rule whose substring appears in the lowercased
       value;
    4. the declared fallback bucket.

    Tier 4 is why this function never returns None and never raises. An empty
    string, a language this taxonomy has never heard of, and a typo all land in
    the declared bucket for things that did not resolve, and the caller can see
    from ``match`` that they did not resolve.
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
    taxonomy: Taxonomy, raw_genre: str | None, *, bpm: float | None = None
) -> Suggestion:
    """Suggest the genre tag to write onto a file, or decline.

    Precedence, stated rather than emergent, in three passes:

    1. nothing at all declines as not-found;
    2. the BETTER-INFORMED pass, which runs before the alias lookup. Two kinds of
       rule qualify. An EXACT refusal, because the strings it names are catch-all
       buckets from a source taxonomy and accepting one as a final tag is the
       blanket-genre bug this entry point exists to prevent. And a rule that
       reads TEMPO, because it decides on evidence a name lookup does not have;
    3. an EXACT declared alias, which beats a plain substring rule: a declaration
       is a statement and a substring is a guess;
    4. the ordered substring corrections, which fix a source taxonomy's combined
       buckets;
    5. otherwise the source's own string passes through unchanged, which is how a
       genuinely new genre survives long enough for someone to notice it. That
       tier, and only that tier, sets ``off_taxonomy``, so the noticing has a
       mechanism behind it rather than a hope (R-650).

    There is no tier that invents a bucket. That is the difference from routing,
    and it is enforced: a template declaring otherwise is refused at load.
    """
    value = (raw_genre or "").strip()
    if not value:
        return Suggestion(decline=Decline.NOT_FOUND)

    lowered = value.lower()

    for rule in taxonomy.suggest:
        if not (rule.equals or rule.split):
            continue
        if _rule_matches(rule, lowered):
            return _apply_suggest_rule(taxonomy, rule, lowered, bpm)

    hit = taxonomy.tagging_alias(lowered)
    if hit is not None:
        bucket_id, sub_id = hit
        return Suggestion(bucket_id=bucket_id, sub_id=sub_id, tag=_display_of(taxonomy, hit))

    for rule in taxonomy.suggest:
        if rule.equals or rule.split:
            continue
        if _rule_matches(rule, lowered):
            return _apply_suggest_rule(taxonomy, rule, lowered, bpm)

    # THE LAST TIER, AND THE ONE STRING IT DOES NOT FLAG. Nothing here claimed
    # the value, so there is no bucket to return either way, and the tag is the
    # source's own word. The flag says that word is outside this template, and
    # there is exactly one kind that is not: a BUCKET's own display, which
    # ``resolve_bucket``'s second tier recognises byte for byte and places where
    # the template says. That happens constantly, because this tagger writes
    # bucket names back onto files and two shipped buckets carry no alias naming
    # themselves, and reporting it would put the library's own folder names in
    # front of a person as a gap.
    #
    # THE TEST IS THAT TIER, NOT THE VOCABULARY, and the difference was measured
    # rather than reasoned. A SUB's display is equally a declared word and
    # routing does NOT recognise it, so a file wearing one lands in the fallback
    # bucket exactly like a word nobody declared: suppressing it would hide the
    # very case R-650 is about. The same holds for a display in another case,
    # which the Bandcamp picker produces because it selects lowercased tags.
    # So the question this asks is the one that decides where the file ends up.
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)


def _rule_matches(rule, lowered: str) -> bool:
    if rule.equals:
        return lowered in {needle.lower() for needle in rule.equals}
    if rule.all_of:
        return all(needle in lowered for needle in rule.all_of)
    return bool(rule.any_of) and any(needle in lowered for needle in rule.any_of)


def _display_of(taxonomy: Taxonomy, hit: tuple[str, str | None]) -> str:
    bucket_id, sub_id = hit
    bucket = taxonomy.bucket(bucket_id)
    if sub_id is None:
        return bucket.display
    for sub in bucket.subs:
        if sub.id == sub_id:
            return sub.display
    return bucket.display


def _apply_suggest_rule(taxonomy, rule, lowered: str, bpm: float | None) -> Suggestion:
    if rule.decline is not None:
        return Suggestion(decline=Decline(rule.decline))

    if rule.split is not None and rule.split.when_contains in lowered:
        split = rule.split
        if bpm is None:
            # No tempo to split on. Take the declared safe side and ask for a
            # look rather than guessing, because the two sides of this split are
            # different rooms of a night, not neighbours.
            bucket = taxonomy.bucket(split.unknown_bpm)
            return Suggestion(
                bucket_id=bucket.id,
                tag=bucket.display,
                needs_review=split.unknown_bpm_needs_review,
            )
        target = split.below if bpm < split.max_bpm else split.at_or_above
        bucket = taxonomy.bucket(target)
        return Suggestion(bucket_id=bucket.id, tag=bucket.display)

    if rule.bucket is not None:
        bucket = taxonomy.bucket(rule.bucket)
        return Suggestion(bucket_id=bucket.id, tag=bucket.display)

    # A rule with a literal tag and no bucket: the source taxonomy names
    # something this taxonomy has no folder for. Declared on purpose so the gap
    # is visible instead of being silently collapsed into a neighbour.
    #
    # NOT off taxonomy, and the difference is the whole point of that field. The
    # template author wrote this tag down and said in a comment why there is no
    # bucket for it, so nobody needs telling about it. The last tier's string is
    # one nobody has declared anywhere, which is the one worth reporting.
    return Suggestion(tag=rule.tag)


# ---------------------------------------------------------------------------
# Energy
# ---------------------------------------------------------------------------


def energy_sub(
    taxonomy: Taxonomy,
    bucket_id: str,
    level: int | None,
    *,
    source_genre: str = "",
) -> Sub | None:
    """The sub-playlist a track belongs in, or None to leave it where it is.

    The tier order below reproduces three per-bucket exceptions that used to be
    three hardcoded branches, and the ORDER is load-bearing rather than
    stylistic:

    * A bucket that routes by source genre is checked FIRST, so it never
      consults energy at all.
    * A bucket with no energy dimension is checked BEFORE the missing-level
      case, so a track in it with no energy reading lands in its single sub
      rather than in a sink that bucket does not have.

    Returning None is a real answer. It means this taxonomy declares no place for
    the track below its bucket, and a caller that treats None as an error would
    reintroduce the crash the declaration exists to avoid.
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
            # The returned id is the BAND's id, deliberately. Two buckets that
            # split at the same levels then key state identically even when one
            # of them labels its bands differently, which is the whole reason a
            # label override is not a second set of cuts.
            return Sub(band.id, bucket.energy.band_display.get(band.id, band.display))
    # Unreachable while the loader holds: the last band's bound equals the top of
    # the scale. Kept explicit so an out-of-range level never returns None and
    # gets mistaken for "no place declared".
    last = taxonomy.energy.bands[-1]
    return Sub(last.id, bucket.energy.band_display.get(last.id, last.display))


class Competing(str, Enum):
    """What kind of place a bucket's exclusive subs are.

    A track belongs in ONE of a bucket's competing subs. Which subs those are
    is the taxonomy's to say, and the kind is what a report splits its count by.
    """

    #: The energy bands and the no reading sub beside them.
    BAND = "band"

    #: The style subs of a bucket that does not split by energy.
    STYLE = "style"


def competing_subs(taxonomy: Taxonomy, bucket_id: str) -> tuple[Competing, frozenset[str]]:
    """The subs of one bucket a track may hold only one of, and their kind.

    THE TIER ORDER IS :func:`energy_sub`'S OWN, because this answers the
    question that function's answer raises: given the sub a track was routed
    to, which other subs would be a second place for it. A bucket that routes
    by source genre never consults energy, so its style subs compete. A bucket
    with no energy dimension holds its style subs and its single sub. Every
    other bucket splits by energy, so its bands compete, and the no reading
    sub competes with them, since a track filed under a band has a reading as
    far as the tree is concerned.

    A SUB CLASS IS NEVER IN THE SET. A manual or derived sub sits beside a
    track's band rather than instead of it, which is what additive means, so
    it is removed by identifier even where a bucket happens to declare a sub
    of the same identifier.

    Identifiers, never display names (R19, D5). A bucket that labels its bands
    differently still competes on the band's identifier.

    A FORMER PLACE COMPETES TOO (R-797), in the bucket that declares it and in
    no other. It is the playlist that bucket's tracks were filed in before the
    bucket had a folder of its own, so a track sitting there and in a band is
    in two places, and a track sitting there alone is held elsewhere. It does
    not change the kind: the kind says what a reading decides among, and no
    reading ever names a former place.
    """
    bucket = taxonomy.bucket(bucket_id)
    classes = {entry.id for entry in taxonomy.sub_classes}
    former = {place.id for place in bucket.formerly}

    if (
        bucket.sub_by_source is not None
        or not taxonomy.energy.enabled
        or not bucket.energy.enabled
    ):
        found = {sub.id for sub in bucket.subs}
        if bucket.single_sub is not None:
            found.add(bucket.single_sub.id)
        return Competing.STYLE, frozenset((found | former) - classes)

    found = {band.id for band in taxonomy.energy.bands}
    if taxonomy.energy.no_energy_sub is not None:
        found.add(taxonomy.energy.no_energy_sub.id)
    return Competing.BAND, frozenset((found | former) - classes)


def former_place(taxonomy: Taxonomy, bucket_id: str, sub_id: str) -> FormerPlace | None:
    """The former place one of a bucket's competing subs is, or None.

    None for a band, a style sub, the no reading sub and anything the bucket
    does not declare, which is every identifier a resolver can answer with. A
    caller that is about to FILE a track asks this to refuse; a caller that is
    about to read or leave a place asks it to find the playlist.
    """
    for place in taxonomy.bucket(bucket_id).formerly:
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

    THROUGH :func:`resolve_bucket` AND NOTHING ELSE, so the answer is where
    routing files the track and no second opinion on that can grow here.

    THE FALLBACK TIER IS NO FOLDER. Routing lands there so that it never
    raises, and a genre that got there was claimed by nothing declared.

    A BUCKET THAT ROUTES BY SOURCE GENRE HOLDS GENRES THAT HAVE NO FOLDER OF
    THEIR OWN. Each row of its map names the style sub a source string files
    in, and a string with no row lands in the declared default, which is a
    place to put it and not a statement about what it is. The bucket's own
    name is the exception: a track tagged with it has that folder by name.
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

    Deliberately independent of the band cuts. Energy is decile-calibrated, so
    an even five-way spread lands tracks across all five stars while the tree
    stays a three-way split. Tying the two together would silently re-rate a
    library the first time a band boundary moved.
    """
    if level is None:
        return None
    for cut in taxonomy.energy.rating_cuts:
        if level <= cut.max:
            return cut.rating
    return taxonomy.energy.rating_cuts[-1].rating if taxonomy.energy.rating_cuts else None


def no_energy_sub(taxonomy: Taxonomy, bucket_id: str) -> Sub | None:
    """The sink a bucket sweeps out of, or None when it declares none.

    A bucket with no sink is a bucket nothing gets swept out of. That single
    declaration replaces two separate hardcoded exclusion lists in the source
    system, one suppressing the sweep and one suppressing the rating write.
    """
    bucket = taxonomy.bucket(bucket_id)
    if bucket.sub_by_source is not None or not bucket.energy.enabled:
        return None
    return taxonomy.energy.no_energy_sub


def rates(taxonomy: Taxonomy, bucket_id: str) -> bool:
    """Whether automation may write a star rating for tracks in this bucket."""
    return taxonomy.bucket(bucket_id).rates


def routes_with_vox(voxlevel: int | None, threshold: float | None) -> bool:
    """Whether a vocal-prominence reading clears the cut for the additive sub.

    The threshold is PASSED IN, never fetched. The old version defaulted it by
    importing an analysis module from inside this layer, which meant a slim
    install without that module raised on the first vocal track. Here an absent
    threshold simply routes nothing as vocal, which is what a library with no
    vocal analysis should do.
    """
    if voxlevel is None or threshold is None:
        return False
    return voxlevel >= threshold


# ---------------------------------------------------------------------------
# Tempo priors
# ---------------------------------------------------------------------------


def bpm_prior(taxonomy: Taxonomy, raw_genre: str | None) -> BpmPrior | None:
    """The tempo detection window for a source genre, via its bucket.

    Resolving through the bucket rather than looking the raw string up in a
    parallel table is the fix for a silent, total failure: the old table was
    keyed by folder DISPLAY name, so a user whose folders were named anything
    else matched none of them and every track in their library detected against
    one generic window. A window spanning a full octave folds nothing, which
    disables the octave-error defence the priors exist to provide, with no
    warning anywhere.

    Returns None when the resolved bucket declares no window, so the caller can
    refuse rather than quietly detect against a default.
    """
    return taxonomy.bucket(resolve_bucket(taxonomy, raw_genre).bucket_id).bpm


# ---------------------------------------------------------------------------
# The family projection (a parallel vocabulary, not a merge)
# ---------------------------------------------------------------------------


def family_of(taxonomy: Taxonomy, raw_genre: str | None) -> str | None:
    """The family of whatever bucket this genre resolves to.

    A projection off the bucket, not a second genre table. It also fixes a live
    inconsistency for free: the old rules ran on the RAW tag, so a track tagged
    for two genres could sit in one folder and score as a different family than
    the folder it sat in.
    """
    return taxonomy.bucket(resolve_bucket(taxonomy, raw_genre).bucket_id).family


def _supergroup_of(taxonomy: Taxonomy, family: str | None) -> str | None:
    if family is None:
        return None
    return taxonomy.family.supergroup.get(family, family)


def genre_affinity(taxonomy: Taxonomy, anchor_genre: str | None, cand_genre: str | None) -> float:
    """A soft genre prior for ranking. Never a hard exclude.

    An unknown anchor scores neutral so genre neither helps nor hurts, which is
    what an unowned anchor track needs.
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

    Keyed on the SOURCE taxonomy's own genre, never on the bucket it resolves
    to, and that is deliberate rather than an oversight. A bucket-level "ask"
    means the FOLDER is uncertain; a confident source sub-genre is still a
    confident FAMILY signal. Collapsing the two would undo the softening that
    stopped this gate dropping most of a legitimate catalogue.

    Timid by construction: an empty string and any string no rule claims are
    both keep, because absence of evidence is not evidence of a bad fit.
    """
    value = (source_genre or "").strip().lower()
    if not value:
        return None
    for rule in taxonomy.label_gate.rules:
        matched = (
            (rule.equals and value in {e.lower() for e in rule.equals})
            or (rule.all_of and all(needle in value for needle in rule.all_of))
            or (rule.any_of and any(needle in value for needle in rule.any_of))
        )
        if not matched:
            continue
        return None if rule.keep else rule.family
    return None


def gate_decisions(
    taxonomy: Taxonomy,
    source_genres: Sequence[str | None],
    *,
    out_of_place_share: float | None = None,
) -> list[GateVerdict]:
    """Keep or drop each track, judged against the WHOLE catalogue at once.

    The share is computed over tracks the source actually classified. Counting
    the unclassified ones would dilute every share toward zero and turn a timid
    gate into an aggressive one, which is the opposite of what it is for.

    A family drops only when it is a small minority of what this label puts out,
    so a label that genuinely makes that music keeps it and a one-off release in
    an unrelated style does not drag the whole style in.
    """
    share = (
        taxonomy.label_gate.out_of_place_share
        if out_of_place_share is None
        else out_of_place_share
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


def _sub_by_id(bucket: Bucket, sub_id: str) -> Sub | None:
    for sub in bucket.subs:
        if sub.id == sub_id:
            return sub
    return None
