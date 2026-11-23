"""The folder suggestion count: which genres have outgrown having no folder.

Every genre the collection holds that no top level folder answers for, with how
many tracks carry it, and the ones at or over the threshold named (R-797).

IT COUNTS THE COLLECTION, NOT THE TREE: a folder is filled from a track's genre,
filed or not, and a playlist member a person dragged in is not its genre.

A GENRE is :func:`cratekit.core.routing.folder_of`'s answer. Strings filed in a
style sub count under that SUB, and so does another spelling of one of them or
of the sub's own name, wherever routing files it. Any other string, in a default
sub or claimed by nothing, counts under its own word folded on case.

IT SUGGESTS AND NEVER CREATES: a folder is added by a person editing the
taxonomy.

Layer: modules. It performs no input. Everything it reads is handed in.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

from cratekit.adopt.scan import CollectionRow
from cratekit.core import routing, taxonomy

#: How many tracks a genre holds before the report names it, the author's
#: number (2026-10-01).
FOLDER_WORTH = 50


@dataclass(frozen=True, slots=True)
class GenreCount:
    """One genre with no top level folder of its own, and what carries it.

    ``name`` is the style sub's display name or the genre word in its commonest
    spelling. ``bucket`` and ``sub`` are the style sub, or where routing lands
    the word, both empty when nothing claims it. ``sources`` is every string
    counted under it with its count, largest first. ``strays`` is the spellings
    counted with a style sub that routing does not file there, so the row says
    so.
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

    Routing matches a source string exactly, so `rock` beside `Rock` would count
    apart and each fall short of a threshold the genre has passed. A source
    string wins over a sub's name and the first declared wins among equals, so
    the answer does not depend on iteration order.
    """
    found: dict[str, tuple[str, str]] = {}
    styled = [bucket for bucket in declared.buckets if bucket.sub_by_source is not None]
    for bucket in styled:
        for source, sub_id in bucket.sub_by_source.map.items():
            found.setdefault(source.casefold(), (bucket.id, sub_id))
    for bucket in styled:
        for sub in bucket.subs:
            found.setdefault(sub.display.casefold(), (bucket.id, sub.id))
    return found


def count(
    rows: Iterable[CollectionRow], declared: taxonomy.Taxonomy, *, threshold: int = FOLDER_WORTH
) -> GenreReport:
    """Count the live collection by genre and find the ones with no folder.

    A tombstone is not counted. A track with no genre is counted apart, and so is
    a word the taxonomy calls too coarse, asked as adoption's census asks it:
    adoption files none of those, so no folder answers for them. Largest first,
    then by name, so two runs list the same rows in the same order.
    """
    tracks = with_folder = no_genre = too_coarse = 0
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
            # ANOTHER SPELLING OF A STYLE SUB'S OWN GENRE, counted with it.
            key = (sub_kind, *style_subs[value.casefold()], "")
            strays.setdefault(key, set()).add(value)
        else:
            # ITS OWN WORD, folded on case; a default sub and nothing stay two rows.
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
        spelled = tuple(sorted(strays.get(key, ())))
        tracks_of = sum(seen.values())
        genres.append(
            GenreCount(name, tracks_of, kind, bucket_id, sub_id, filed_under, sources, spelled)
        )
    genres.sort(key=lambda genre: (-genre.tracks, genre.name, genre.kind, genre.bucket))
    return GenreReport(threshold, tracks, with_folder, no_genre, too_coarse, tuple(genres))


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
