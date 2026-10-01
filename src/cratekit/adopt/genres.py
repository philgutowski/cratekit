"""The folder suggestion count: which genres have outgrown having no folder.

WHY THIS EXISTS (R-797). Rock sat at 109 tracks as a style sub of the non
electronic folder with nothing saying so, and R&B was promoted to a folder of
its own only because the author happened to ask. This is the count that says
it: every genre the collection holds that no top level folder answers for,
with how many tracks carry it, and the ones at or over the threshold named.

IT COUNTS THE COLLECTION, NOT THE TREE. A folder is filled from a track's
genre, so what a new folder would hold is the tracks whose genre names it,
whether or not they have been filed yet. Counting playlist members would miss
every track still waiting in the intake and would count a track a person
dragged into a playlist its genre does not name.

WHAT A GENRE IS HERE is :func:`cratekit.core.routing.folder_of`'s answer. A
source string filed in a style sub is counted under that SUB, so the four
strings that file under one sub are one genre with one count and the row lists
them, and so is another spelling of one of those strings or of the sub's own
name, wherever routing happens to file it. Any other string that lands in a
default sub, or that nothing declared claims at all, is counted under its own
word, folded on case, because the default is a place to put it and not what it
is.

IT SUGGESTS AND NEVER CREATES. Nothing here writes, and a folder is added by a
person editing the taxonomy.

Layer: modules. It performs no input. Everything it reads is handed in.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

from cratekit.adopt.scan import CollectionRow
from cratekit.core import routing, taxonomy

#: How many tracks a genre holds before the report names it. The author's
#: number, decided on 2026-10-01. A genre one short of it is counted and not
#: named.
FOLDER_WORTH = 50


@dataclass(frozen=True, slots=True)
class GenreCount:
    """One genre with no top level folder of its own, and what carries it.

    ``name`` is the style sub's display name, or the genre word itself in its
    commonest spelling. ``bucket`` and ``sub`` are the style sub the genre is,
    or where routing lands the word, both empty when nothing declared claims
    it. ``sources`` is every genre string counted under it with its own count,
    largest first.

    ``strays`` IS THE PART OF A STYLE SUB'S COUNT ROUTING DOES NOT FILE THERE.
    Another spelling of the sub's name is the same genre and is counted with
    it, and routing, which matches a source string exactly, lands it in a
    default sub or nowhere. Found by the second review: the row said such
    tracks were filed under the sub, and a person looking in that playlist
    found none of them. So the spellings are named and the sentence says so.
    """

    name: str
    tracks: int
    kind: str
    bucket: str
    sub: str
    filed_under: tuple[str, str] | None
    sources: tuple[tuple[str, int], ...]
    strays: tuple[str, ...] = ()

    @property
    def not_filed_there(self) -> int:
        """How many of the tracks routing does not file under ``filed_under``."""
        return sum(tracks for word, tracks in self.sources if word in self.strays)


@dataclass(frozen=True, slots=True)
class GenreReport:
    """Every live track counted once: with a folder, without one, with no
    genre, or with a word the taxonomy calls too coarse to be one."""

    threshold: int
    tracks: int
    with_folder: int
    no_genre: int
    too_coarse: int
    genres: tuple[GenreCount, ...]

    @property
    def without_folder(self) -> int:
        return sum(genre.tracks for genre in self.genres)

    @property
    def named(self) -> tuple[GenreCount, ...]:
        """The genres at or over the threshold, which is what the report names."""
        return tuple(genre for genre in self.genres if genre.tracks >= self.threshold)


def _style_subs_by_word(declared: taxonomy.Taxonomy) -> dict[str, tuple[str, str]]:
    """Every word that names a style sub, folded on case, to its bucket and sub.

    The source strings of each map and each sub's own name. Routing matches a
    source string exactly, so `rock` beside `Rock` lands in the default sub or
    nowhere while being the same genre by name, and counted apart the two
    would each fall short of a threshold the genre has passed. Found by the
    review, with 45 and 10 tracks. A source string wins over a sub's name, and
    the first declared wins among equals, so the answer does not depend on
    iteration order.
    """
    found: dict[str, tuple[str, str]] = {}
    for bucket in declared.buckets:
        if bucket.sub_by_source is None:
            continue
        for source, sub_id in bucket.sub_by_source.map.items():
            found.setdefault(source.casefold(), (bucket.id, sub_id))
    for bucket in declared.buckets:
        if bucket.sub_by_source is None:
            continue
        for sub in bucket.subs:
            found.setdefault(sub.display.casefold(), (bucket.id, sub.id))
    return found


def count(
    rows: Iterable[CollectionRow],
    declared: taxonomy.Taxonomy,
    *,
    threshold: int = FOLDER_WORTH,
) -> GenreReport:
    """Count the live collection by genre and find the ones with no folder.

    A TOMBSTONE IS NOT COUNTED. A row rekordbox has marked removed is a track
    the person took out, and a folder is not suggested for what they deleted.

    A TRACK WITH NO GENRE IS COUNTED APART and is never a genre. "No genre" at
    fifty tracks is a tagging backlog and not a folder anybody is missing.

    SO IS A WORD THE TAXONOMY CALLS TOO COARSE, asked of the taxonomy the way
    adoption's census asks it. Routing resolves such a word to the catch all
    bucket by an alias, and adoption files none of those tracks, so counting
    them as having a folder said a folder answers for tracks no folder will
    receive. Found by the second review.

    THE ORDER IS LARGEST FIRST, THEN BY NAME, so two runs over one collection
    list the same rows in the same order.
    """
    tracks = 0
    with_folder = 0
    no_genre = 0
    too_coarse = 0
    style_subs = _style_subs_by_word(declared)
    sub_kind = str(routing.Folder.SUB.value)
    spellings: dict[tuple[str, str, str, str], Counter[str]] = {}
    strays: dict[tuple[str, str, str, str], set[str]] = {}
    for row in rows:
        if row.deleted:
            continue
        tracks += 1
        value = (row.genre or "").strip()
        if not value:
            no_genre += 1
            continue
        if declared.is_too_coarse_as_source(value):
            too_coarse += 1
            continue
        folder = routing.folder_of(declared, value)
        if folder.kind is routing.Folder.OWN:
            with_folder += 1
            continue
        if folder.kind is routing.Folder.SUB:
            key = (sub_kind, folder.bucket_id, folder.sub_id or "", "")
        elif value.casefold() in style_subs:
            # ANOTHER SPELLING OF A STYLE SUB'S OWN GENRE. Where routing files
            # it is not what it is, and it is counted with the genre it names.
            key = (sub_kind, *style_subs[value.casefold()], "")
            strays.setdefault(key, set()).add(value)
        else:
            # ITS OWN WORD, folded on case. Where it lands is carried on the
            # row and is not part of what it is counted as, except that a word
            # in a default sub and a word nothing claims stay two rows.
            key = (str(folder.kind.value), folder.bucket_id, folder.sub_id or "", value.casefold())
        spellings.setdefault(key, Counter())[value] += 1

    genres: list[GenreCount] = []
    for key, seen in spellings.items():
        kind, bucket_id, sub_id, _word = key
        sources = tuple(sorted(seen.items(), key=lambda item: (-item[1], item[0])))
        bucket = declared.bucket(bucket_id)
        if kind == routing.Folder.NONE.value:
            name, filed_under, bucket_id = sources[0][0], None, ""
        elif kind == routing.Folder.SUB.value:
            name = routing.display_of(declared, (bucket_id, sub_id))
            filed_under = (bucket.display, name)
        else:
            name = sources[0][0]
            filed_under = (bucket.display, routing.display_of(declared, (bucket_id, sub_id)))
        genres.append(
            GenreCount(
                name=name,
                tracks=sum(seen.values()),
                kind=kind,
                bucket=bucket_id,
                sub=sub_id,
                filed_under=filed_under,
                sources=sources,
                strays=tuple(sorted(strays.get(key, ()))),
            )
        )
    genres.sort(key=lambda genre: (-genre.tracks, genre.name, genre.kind, genre.bucket))
    return GenreReport(
        threshold=threshold,
        tracks=tracks,
        with_folder=with_folder,
        no_genre=no_genre,
        too_coarse=too_coarse,
        genres=tuple(genres),
    )


def row_json(genre: GenreCount) -> dict[str, Any]:
    """One counted genre as the report carries it."""
    return {
        "genre": genre.name,
        "tracks": genre.tracks,
        "kind": genre.kind,
        "bucket": genre.bucket or None,
        "sub": genre.sub or None,
        "filed_under": None if genre.filed_under is None else list(genre.filed_under),
        "not_filed_there": genre.not_filed_there,
        "sources": [
            {"genre": word, "tracks": tracks, "filed_there": word not in genre.strays}
            for word, tracks in genre.sources
        ],
    }


def where(genre: GenreCount) -> str:
    """Where one counted genre is filed today, as a sentence fragment."""
    if genre.filed_under is None:
        return "no declared folder claims it, so it falls to the fallback"
    folder, sub = genre.filed_under
    if genre.kind == routing.Folder.DEFAULT.value:
        return f"filed under {folder} / {sub}, that folder's default, with no sub of its own"
    if genre.not_filed_there:
        return (
            f"filed under {folder} / {sub}, except {genre.not_filed_there} under another "
            f"spelling ({', '.join(genre.strays)}), which routing does not file there"
        )
    return f"filed under {folder} / {sub}"


__all__ = [
    "FOLDER_WORTH",
    "GenreCount",
    "GenreReport",
    "count",
    "row_json",
    "where",
]
