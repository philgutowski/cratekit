"""Building a taxonomy from a parsed template, and every check it must pass.

Split from :mod:`cratekit.core.taxonomy` (U299), which re-exports
``build_taxonomy`` and ``live_places``. Every rule fails here, at load, so a
template nobody can route by is refused in setup rather than mid intake.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping, Sequence

from cratekit.core.taxonomy_model import (
    _ID,
    ANY_KIND,
    DEFAULT_LABEL_KIND,
    DEFAULT_LONG_TRACK_SECONDS,
    FOREIGN_ROOT_NAMES,
    FORMER_PLACE_SCHEMA_VERSION,
    GENRE_SUB_SCHEMA_VERSION,
    KIND_NAME,
    NO_KIND,
    PLAYLIST_SIGNAL_SCHEMA_VERSION,
    SIGNAL_PLAYLIST,
    SIGNAL_VOX,
    SIGNALS,
    SPLIT_PLACE_SCHEMA_VERSION,
    SUPPORTED_SCHEMA_VERSIONS,
    SUPPORTED_TREE_DEPTH,
    VOCABULARY_SOURCES,
    Band,
    BpmPrior,
    Bucket,
    BucketEnergy,
    Energy,
    Fallback,
    FamilyAffinity,
    FormerPlace,
    FuzzyRule,
    GateRule,
    GenreSub,
    LabelGate,
    LongTracks,
    Node,
    PublishedRule,
    RatingCut,
    Split,
    SplitPlace,
    Sub,
    SubBySource,
    SubClass,
    SubPolicy,
    SuggestRule,
    Taxonomy,
    TaxonomyError,
    Vocabulary,
    VocabularyWord,
    _tag_place,
)


def build_taxonomy(data: Mapping[str, Any]) -> Taxonomy:
    """Validate a parsed template and freeze it, raising every problem at once."""
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
    # An optional section is declared or absent, never half declared, and is
    # validated as strictly as the mandatory trees. Keyed on presence, never
    # truthiness, since an empty table is falsy but still a declaration.
    catalog_raw = data.get("catalog") if "catalog" in data else None
    catalog = (
        Node(str(catalog_raw.get("id", "")), str(catalog_raw.get("display", "")))
        if catalog_raw is not None
        else None
    )
    long_tracks, long_problems = _build_long_tracks(data)
    problems += long_problems
    # Keyed on presence; a value that is not a table is reported by name.
    old_raw = data.get("intake_old") if "intake_old" in data else None
    intake_old: Node | None = None
    if old_raw is not None and not isinstance(old_raw, Mapping):
        problems.append("[intake_old] must be a table with an id and a display")
    elif old_raw is not None:
        intake_old = Node(str(old_raw.get("id", "")), str(old_raw.get("display", "")))
        # An Old sharing the intake flow's id or display declares one folder twice.
        if intake_old.id == intake.id or intake_old.display == intake.display:
            problems.append(
                "[intake_old] must differ from [intake] in both id and display; "
                "it declares a folder inside the intake flow, not the flow itself"
            )
    # Keyed on presence (U121); a root folder, not inside the intake flow.
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
    # KTD14: the XML bridge encodes exactly this depth; any other is refused here.
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

    # Keyed on presence: an empty table is a declaration.
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


# Section builders. Each returns (value, problems) so one bad section never
# hides the next.


def _build_long_tracks(data: Mapping[str, Any]) -> tuple[LongTracks | None, list[str]]:
    """The long track playlist, or None when the template declares none.

    Keyed on presence. The id and display are checked with the other nodes. The
    threshold must be a whole number of seconds above zero, and a boolean is
    refused, since ``true`` read as 1 would take in the whole collection.
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
    # Rating cuts need not align with band cuts: both are valid splits of a
    # decile scale, and coupling them would re-rate a library when a band moved.

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

        # The shape is checked before a row is read: a hand-written
        # `[bucket.formerly]` arrives as a table, not a list, and must be
        # reported as a line to fix rather than raise.
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
        # The same shape check (U118).
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

        # The same shape check (U155). Sources that are not a list of strings
        # read as none, which the genre sub check refuses by name.
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

    Declared subs, the single sub, the bands under the bucket's labels and the
    no reading sub when it splits by energy, every sub class and every genre sub
    (U155). What a former place must not be. Public, since the adoption plan
    asks it too (R-788), so a shape added here reaches both.
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

    Tracks are removed from a former place, so it must not name a live
    playlist. Its bucket must be declared (the folder is found by it); its sub
    and name must not be ones that bucket still holds; its own id must be free
    in both the declaring and holding bucket and unique among former places;
    and one playlist is the former place of one bucket only. Requires
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
    """The bands and no reading sub one energy bucket files into, by id, its labels.

    Shared by :func:`live_places` and the split place check.
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

    The reverse of :func:`_check_former_places`: it must be a band the holder
    still files into (or the holder's own former place), under the holder's
    name for it, or a move would leave a playlist the writer cannot find. The
    declaring bucket must split by energy; the id must be its own and unique
    among former and split places; one band is split out by one bucket.
    Requires :data:`SPLIT_PLACE_SCHEMA_VERSION`.
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
            # A band of the holder, or its own former place: the playlist both
            # genres sat in before either had a folder.
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

    The bucket must split by energy. Its id and name must not be taken by any
    other place in the bucket, or two places would be one playlist. Each
    source is an exact routing alias of the bucket, and one source names one
    genre sub. Requires :data:`GENRE_SUB_SCHEMA_VERSION`.
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
        # R21's sibling: tagging must be free to decline rather than guess.
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
        # The signal (U119), vocal when absent. A playlist signal names its
        # playlist, is derived and additive, and needs its schema version.
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
            # One additive class per signal (U119): a second would file each
            # track into two playlists for one reading.
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
        # Folded lowercase here, since ``routing._rule_matches`` folds nothing.
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
    # Checked only when a published rule exists; otherwise nothing is judged.
    if published and default_kind != ANY_KIND and default_kind not in kinds:
        problems.append(
            f"[label_gate] default_kind {default_kind!r} is not a kind any "
            f"[[label_gate.published]] rule names ({', '.join(sorted(kinds))}), so "
            f"no release of a label left at the default would ever be judged; set "
            f"default_kind to one of those, or to {ANY_KIND!r}"
        )
    return LabelGate(tuple(rules), share, published, default_kind), problems


def _needles(entry: Mapping[str, Any], key: str) -> tuple[tuple[str, ...], bool]:
    """One matcher list, folded to lowercase, and whether it was a list of words."""
    raw = entry.get(key)
    if raw is None:
        return (), True
    if not isinstance(raw, list) or not all(isinstance(one, str) and one.strip() for one in raw):
        return (), False
    return tuple(one.strip().lower() for one in raw), True


def _build_published(raw: Any) -> tuple[tuple[PublishedRule, ...], list[str]]:
    """The ``[[label_gate.published]]`` rules, and what is wrong with them.

    An unusable rule is a problem, not a skip, or its music would pass unjudged.
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


def _build_vocabularies(
    raw: Any,
    by_id: Mapping[str, Bucket],
    by_display: Mapping[str, str],
    routing_alias: Mapping[str, str],
    fallback: Fallback,
) -> tuple[tuple[Vocabulary, ...], list[str]]:
    """The ``[vocabulary.SOURCE]`` tables, and what is wrong with them (R-799).

    An unusable row is a problem, not a skip, since a dropped row would silently
    fall back to the bucket aliases. The shape is checked before a row is read,
    so a hand edit in the wrong shape is a line to fix, not a crash.
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
        # Lowercase, as a file's record names the source, or it is never looked up.
        if not _ID.match(str(source)):
            problems.append(
                f"{where}: the source name must match {_ID.pattern}, the name a "
                f"file's record gives the source"
            )
            continue
        # A table nothing reads is refused, not ignored.
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
    # A one-member family is dead weight, not an error, so it is not rejected.
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
    """Build the routing (exact) and tagging (case insensitive) alias lookups.

    Tagging may deliberately disagree with routing, never with itself.
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

    # Bucket level first, sub level second, and within the bucket level routing
    # aliases before tagging-only ones (U118): the later statement is the more
    # specific one and wins. Two routing aliases, or two tagging-only aliases,
    # of two buckets still refuse.
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
    # A genre sub's source tags as that sub (U155), last as the most specific,
    # or the tagger would rewrite it to the bucket's name and lose the sub.
    for bucket in buckets:
        for genre in bucket.genre_subs:
            for source in genre.sources:
                tagging[source.lower().strip()] = (bucket.id, genre.id)

    return routing, tagging, problems
