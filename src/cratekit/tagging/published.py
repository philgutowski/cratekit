"""Ask a general music catalogue what genre a track was published under, by its ISRC.

WHY (R-796). The record shops sell dance music and are asked by artist and
title, so funk, rock or soul waited for a genre by hand. A general catalogue
knows those records and is asked by the identifier a download already
carries, so nothing here is a guess. It is Deezer, asked with no key: the
track by its ISRC, then its album, where the genre is published.

THE LOOKUP KNOWS NO TAXONOMY, so it is shared: :func:`genre_lookup` answers
the catalogue's words, :func:`choose` which of them a taxonomy has a folder
for, :func:`second_opinion` the tagger's use of both. The label genre gate
calls the first alone.

THE ANSWER HAS THE SEARCHERS' VALUES AND ``no-isrc``, nothing asked. A file
with no ISRC, a track not known and a catalogue not read are three facts a
person acts on three ways. A refusal is BLOCKED, read through the shared check
(R-791), never retried, and remembered for the run, so the lookup is one per
process, :func:`for_lookup`. The request names this tool: this is an API, and
a client disguised to one is what this module never does. An unknown error,
which arrives inside a 200, is a parse break, never a miss; a body that is not
JSON did not come from the API and is unreachable. An answer naming another
ISRC is not this track's.

NO PICTURE IS READ HERE: pictures stay the record shops' rows.

THE GENRE IS THE ALBUM'S, a limit accepted on 2026-10-01, which is why the
record catalogues are asked first and a usable answer is never replaced.

BEATPORT MUST HAVE ANSWERED FIRST, a match or a miss, and a Discogs that was
asked must not be unread (U244's review): a genre is written once, so an album
word written meanwhile would stand in for theirs for good. Discogs unasked for
want of a token holds nothing back. The suggest verbs' binder,
:func:`for_suggestions`, asks past a Beatport that refused this client once
Discogs answered (U322); ``tag folder`` keeps the gate (#796).

A WORD NOTHING DECLARES IS A DECLINE HERE, unlike a record shop's: this
catalogue's few dozen broad words passed through would file tracks under words
no folder holds. Its words have a table of their own in the taxonomy (R-799),
under :data:`SOURCE`, asked before the buckets' aliases, which were written for
the record shops.

Layer: modules.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from typing import Any

from cratekit import __version__
from cratekit.acquire.match import isrc_token
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging import searchers
from cratekit.tagging.searchers import Answer, Fetch, Pacer
from cratekit.tagging.tag import NO_ISRC, PublishedGenre, SearchHit, SourceAnswer

#: The general catalogue, as a file's record names it: of two others tried, one
#: published no genre for 79 tracks and the other found none of 30.
SOURCE = "deezer"

TRACK_BY_ISRC = "https://api.deezer.com/track/isrc:"
ALBUM = "https://api.deezer.com/album/"

#: This tool, by name, asking for JSON, never the browser identity.
HEADERS = {
    "User-Agent": f"cratekit/{__version__} (published genre lookup by ISRC)",
    "Accept": "application/json",
}

#: The answers that leave the question open, the searchers' own tuple.
UNREAD: tuple[str, ...] = searchers.UNREAD_ANSWERS

#: Every word a file's record may carry for the general catalogue, closed so a
#: summary can zero fill it.
ANSWERS: tuple[str, ...] = (
    *(answer.value for answer in Answer),
    NO_ISRC,
    searchers.NOT_ASKED,
)

#: The catalogue's error codes this reader acts on. An error arrives inside a
#: 200, so the code alone tells a track nobody listed from a refusal.
_NO_DATA = 800
_QUOTA = 4
_BUSY = 700

#: The error type of a client not served without credentials, a refusal
#: whatever its code.
_PERMISSION = "OAuthException"

#: Beatport's answers that count as Beatport having ANSWERED.
_BEATPORT_ANSWERED = (Answer.MATCHED.value, Answer.MISS.value)

#: Discogs' answers that let the suggest verbs ask past a refusing Beatport (U322).
_DISCOGS_ANSWERED = (Answer.MATCHED.value, Answer.MISS.value)


@dataclass(frozen=True, slots=True)
class Published:
    """What the general catalogue said about one ISRC.

    ``genres`` is every genre listed for the track's album, in the catalogue's
    order and words, empty for every answer but a match; a match with none is
    a known track published with no genre.
    """

    source: str
    answer: str
    genres: tuple[str, ...] = ()
    note: str = ""


#: Given an ISRC as some row or tag spelled it, what the catalogue published.
#: Answers and does not raise.
Lookup = Callable[[object], Published]


def _said(answer: Answer, note: str = "") -> Published:
    return Published(SOURCE, answer.value, note=note)


def _error(payload: dict[str, Any]) -> Published | None:
    """The answer an ``error`` object is, or None when the payload carries none.

    "No data" is a miss, quota and permission errors are refusals, "service
    busy" is unreachable, and any other error is a parse break, never a guess.
    """
    error = payload.get("error")
    if error is None:
        return None
    fields = error if isinstance(error, dict) else {}
    code, kind = fields.get("code"), fields.get("type")
    described = f"{kind}, code {code}, {str(fields.get('message') or '')!r}"
    if code == _NO_DATA:
        return _said(Answer.MISS)
    if code == _QUOTA:
        return _said(
            Answer.BLOCKED,
            f"the catalogue's rate limit refused this client, {described}",
        )
    if kind == _PERMISSION:
        return _said(Answer.BLOCKED, f"the catalogue refused this client, {described}")
    if code == _BUSY:
        return _said(Answer.UNREACHABLE, f"the catalogue said it was busy, {described}")
    return _said(
        Answer.PARSE_BREAK,
        f"the catalogue answered with an error this reader does not know, {described}",
    )


def _read(url: str, *, fetch: Fetch, pacer: Pacer) -> dict[str, Any] | Published:
    """One paced touch: the JSON object it answered, or the answer its absence
    is, a block recognised by the record shops' own check."""
    pacer.wait()
    page = fetch(url)
    refused = searchers.unread_outcome(SOURCE, page)
    if refused is not None:
        return _said(refused.answer, refused.note)
    try:
        payload = json.loads(page.text or "")
    except ValueError:
        return _said(
            Answer.UNREACHABLE,
            "the answer was not JSON, so it did not come from the catalogue's API",
        )
    if not isinstance(payload, dict):
        return _said(
            Answer.PARSE_BREAK, "the catalogue's answer is not the JSON object this reader knows"
        )
    return payload


def _genre_names(listing: dict[str, Any]) -> tuple[str, ...] | None:
    """The album's genre names in the catalogue's order, or None for an unknown shape.

    Empty is an album published with no genre; None is no list at all, or
    entries none of which carries a name, the only evidence of a redesign.
    """
    genres = listing.get("genres")
    entries = genres.get("data") if isinstance(genres, dict) else None
    if not isinstance(entries, list):
        return None
    names = tuple(
        entry["name"].strip()
        for entry in entries
        if isinstance(entry, dict)
        and isinstance(entry.get("name"), str)
        and entry["name"].strip()
    )
    if entries and not names:
        return None
    return names


def _ask(
    isrc: str, *, fetch: Fetch, pacer: Pacer, albums: dict[int, tuple[str, ...]]
) -> Published:
    """Ask the catalogue about one well formed ISRC. Two touches at most.

    ``albums`` remembers the genre lists already read, by album, so a release's
    second track asks for the track alone. Only a list READ is remembered.
    """
    track = _read(f"{TRACK_BY_ISRC}{isrc}", fetch=fetch, pacer=pacer)
    if isinstance(track, Published):
        return track
    refused = _error(track)
    if refused is not None:
        return refused
    if isrc_token(track.get("isrc")) != isrc:
        return _said(
            Answer.PARSE_BREAK,
            f"asked about {isrc} and the answer names {track.get('isrc')!r}, so it "
            f"is not read as this track's",
        )
    album = track.get("album")
    album_id = album.get("id") if isinstance(album, dict) else None
    if not isinstance(album_id, int) or isinstance(album_id, bool) or album_id <= 0:
        return _said(
            Answer.PARSE_BREAK,
            "the track's answer names no album, and the genre is published on the album",
        )

    names = albums.get(album_id)
    if names is None:
        listing = _read(f"{ALBUM}{album_id}", fetch=fetch, pacer=pacer)
        if isinstance(listing, Published):
            return listing
        refused = _error(listing)
        if refused is not None:
            if refused.answer != Answer.MISS.value:
                return refused
            # Not a miss: the catalogue just named the track.
            return Published(
                SOURCE,
                Answer.MATCHED.value,
                note="the catalogue knows the track and lists no album for it, so no "
                "genre is published",
            )
        names = _genre_names(listing)
        if names is None:
            return _said(
                Answer.PARSE_BREAK, "the album's answer carries no genre list this reader knows"
            )
        albums[album_id] = names
    return Published(
        SOURCE,
        Answer.MATCHED.value,
        genres=names,
        note="" if names else "the catalogue knows the track and publishes no genre for its album",
    )


#: An ISRC inside a longer value, hyphens allowed at its joints, with nothing
#: alphanumeric either side, so a longer catalogue number is not one.
_ISRC_WITHIN = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]{2}-?[A-Za-z0-9]{3}-?[0-9]{2}-?[0-9]{5}(?![A-Za-z0-9])"
)


def _first_isrc(value: object) -> str:
    """The folded ISRC a value holds, the first when it holds several, or empty.

    The whole value first, then the first ISRC inside it: an ID3 frame of two
    values reads as one string joined by a null, which folds to nothing.
    """
    whole = isrc_token(value)
    if whole:
        return whole
    for found in _ISRC_WITHIN.finditer(str(value or "")):
        token = isrc_token(found.group(0))
        if token:
            return token
    return ""


def _no_isrc(value: object) -> Published | None:
    """The ``no-isrc`` answer for a value that holds no ISRC, or None when it
    does, built once for the lookup and the tagger's seam."""
    if _first_isrc(value):
        return None
    given = str(value or "").strip()
    return Published(
        SOURCE,
        NO_ISRC,
        note=f"{given!r} does not read as an ISRC" if given else "no ISRC was given",
    )


def genre_lookup(
    *,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
    pacing: Pacer | None = None,
) -> Lookup:
    """Build the lookup: an ISRC in, what the general catalogue published out.

    The seams are the searcher's shapes, and every touch is paced, the first
    included. The ISRC is folded and checked before it becomes a URL. A lookup
    remembers the albums it read and its first BLOCKED answer, after which
    nothing is asked; an unreachable answer is a network, not remembered.
    """
    naps = time.sleep if sleep is None else sleep
    pacer = Pacer(sleep=naps) if pacing is None else pacing
    touch = searchers.default_fetch(sleep=naps, headers=HEADERS) if fetch is None else fetch
    albums: dict[int, tuple[str, ...]] = {}
    refusals: list[Published] = []

    def lookup(isrc: object) -> Published:
        bare = _no_isrc(isrc)
        if bare is not None:
            return bare
        token = _first_isrc(isrc)
        if refusals:
            return _said(
                Answer.BLOCKED,
                f"not asked: the catalogue refused this client earlier in this run and "
                f"is not asked again in it. Then, {refusals[0].note}",
            )
        said = _ask(token, fetch=touch, pacer=pacer, albums=albums)
        if said.answer == Answer.BLOCKED.value:
            refusals.append(said)
        return said

    return lookup


def choose(declared: Taxonomy, genres: Sequence[str]) -> tuple[str, str] | None:
    """The first published genre that maps to a folder, with the tag to write.

    :func:`cratekit.tagging.searchers.choose_word`, Discogs' chooser too (U244),
    so the two sources that answer several words mean one thing by "maps to a
    folder". The word is resolved as this catalogue's (R-799), and on a copy
    that declares its table the tag must name a folder, or an alias's bare
    bucket name would land in a default sub with the word lost.
    """
    return searchers.choose_word(
        declared,
        genres,
        source=SOURCE,
        named_only=declared.vocabulary(SOURCE) is not None,
    )


def second_opinion(
    declared: Taxonomy, *, lookup: Lookup | None = None, past_a_refusing_shop: bool = False
) -> PublishedGenre:
    """Build the seam :func:`cratekit.tagging.tag.tag_one` offers a hit to.

    It returns the hit to act on, the catalogue's answer appended to its record.
    Every rule of when the catalogue is asked lives here:

    * a hit with no per source answers is returned untouched;
    * a hit with a genre, or a file that needs none (ISRC None), is
      ``not-asked``: a usable answer is never replaced (R4);
    * an ISRC tag holding no ISRC is ``no-isrc``, whatever the shops did;
    * a Beatport answer not a match or a miss, or a Discogs asked and unread
      (U244), is ``not-asked``, save that with ``past_a_refusing_shop`` a
      refusing Beatport gives way once Discogs answered (U322);
    * otherwise the catalogue is asked, and a genre that maps to a folder is
      the hit's genre; anything else leaves a decline saying what was answered.

    A decline keeps the record shop's word when there is one, since a person's
    alias is against the catalogue that sells the record. A declined word of
    this catalogue's own becomes the file's, a word outranking an unread source.
    A match publishing no genre changes only the record. ``art_source`` stays
    the record shop's whose row matched, or nobody's.
    """
    ask = genre_lookup() if lookup is None else lookup

    def decide(hit: SearchHit, isrc: str | None) -> SearchHit:
        if not hit.answers:
            return hit

        def recorded(entry: SourceAnswer, **changed: Any) -> SearchHit:
            return replace(hit, answers=(*hit.answers, entry), **changed)

        if hit.genre or isrc is None:
            return recorded(SourceAnswer(SOURCE, searchers.NOT_ASKED))
        bare = _no_isrc(isrc)
        if bare is not None:
            return recorded(SourceAnswer(SOURCE, bare.answer, note=bare.note))
        first = next((said for said in hit.answers if said.source == searchers.BEATPORT), None)
        if first is None or (
            first.answer not in _BEATPORT_ANSWERED
            and not (past_a_refusing_shop and _refused_beside_discogs(first, hit))
        ):
            return recorded(
                SourceAnswer(
                    SOURCE,
                    searchers.NOT_ASKED,
                    note=f"{searchers.BEATPORT} was not read for this track, and the "
                    f"general catalogue is asked only once it has answered",
                )
            )
        discogs = next((said for said in hit.answers if said.source == searchers.DISCOGS), None)
        if discogs is not None and discogs.answer in UNREAD:
            return recorded(
                SourceAnswer(
                    SOURCE,
                    searchers.NOT_ASKED,
                    note=f"{searchers.DISCOGS} was asked and not read for this track "
                    f"({discogs.answer}), and the general catalogue is asked only once "
                    f"it has answered",
                )
            )

        said = ask(isrc)
        if said.answer != Answer.MATCHED.value:
            unread = (*hit.unread, SOURCE) if said.answer in UNREAD else hit.unread
            return recorded(SourceAnswer(SOURCE, said.answer, note=said.note), unread=unread)

        note = said.note
        if len(said.genres) > 1:
            note = f"the album lists {', '.join(said.genres)}"
        picked = choose(declared, said.genres)
        word = picked[0] if picked else (said.genres[0] if said.genres else "")
        entry = SourceAnswer(SOURCE, said.answer, source_genre=word, note=note)
        if picked is None and (hit.source_genre or not word):
            return recorded(entry)
        # This catalogue becomes the hit's source; the picture stays the shop's.
        return recorded(
            entry,
            genre=picked[1] if picked else None,
            source=SOURCE,
            source_genre=word,
            off_taxonomy=False,
            art_source=hit.source if hit.art_source is None else hit.art_source,
        )

    return decide


def _refused_beside_discogs(beatport: SourceAnswer, hit: SearchHit) -> bool:
    """Whether Beatport refused this client while Discogs answered about the track (U322)."""
    if beatport.answer != Answer.BLOCKED.value:
        return False
    discogs = next((said for said in hit.answers if said.source == searchers.DISCOGS), None)
    return discogs is not None and discogs.answer in _DISCOGS_ANSWERED


#: The one lookup this process asks the catalogue through, built on first use.
_shared: list[Lookup] = []


def for_lookup() -> Lookup:
    """The lookup a caller should use, looked up so a test can replace it here.

    One per process, so the next file meets the memory of a refusal and of the
    albums read. Building one touches no network. The label genre gate calls
    this for a release's ISRC.
    """
    if not _shared:
        _shared.append(genre_lookup())
    return _shared[0]


def for_taxonomy(declared: Taxonomy) -> PublishedGenre:
    """The seam a tagging worker hands :func:`cratekit.tagging.tag.tag_one`,
    over :func:`for_lookup` read at call time (in process only, R-226)."""
    return second_opinion(declared, lookup=for_lookup())


def for_suggestions(declared: Taxonomy) -> PublishedGenre:
    """The seam ``tag suggest --catalogue`` and ``tag backlog --catalogue`` ask
    through: :func:`for_taxonomy`'s, past a refusing Beatport once Discogs
    answered (U322)."""
    return second_opinion(declared, lookup=for_lookup(), past_a_refusing_shop=True)


__all__ = [
    "ALBUM",
    "ANSWERS",
    "HEADERS",
    "SOURCE",
    "TRACK_BY_ISRC",
    "UNREAD",
    "Lookup",
    "Published",
    "choose",
    "for_lookup",
    "for_suggestions",
    "for_taxonomy",
    "genre_lookup",
    "second_opinion",
]
