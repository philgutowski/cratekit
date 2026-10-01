"""Ask a general music catalogue what genre a track was published under, by its ISRC.

WHY A SECOND KIND OF SOURCE (R-796). The three record shops in
:mod:`cratekit.tagging.searchers` sell dance music and are asked by artist and
title. They do not carry funk, rock or soul, and two of them refuse this machine
with bot checks, so every such file waited for a genre by hand while the
taxonomy already had folders for it. A general catalogue knows those records,
and it can be asked by the one identifier a download already carries, so no
search result needs interpreting and nothing here is a guess.

THE CATALOGUE IS DEEZER, ASKED WITH NO KEY. Two requests a track: the track by
its ISRC, then that track's album, because the genre is published on the album
and not on the track. Measured on 2026-10-01: an ISRC it knows answers an object
carrying ``isrc`` and ``album.id``, the album answers ``genres.data``, a list of
named genres, and an ISRC it does not know answers HTTP 200 with an ``error``
object whose code is 800.

THE LOOKUP KNOWS NO TAXONOMY, AND THAT IS WHAT MAKES IT SHARED. :func:`genre_lookup`
answers the catalogue's own words for an ISRC. :func:`choose` is the separate
question of which of them a declared taxonomy has a folder for, and
:func:`second_opinion` is the tagger's use of both. The label genre gate judges
a release with its own rules and calls the first alone.

THE ANSWER HAS THE SEARCHERS' VALUES AND ONE MORE. MATCHED, MISS, UNREACHABLE,
BLOCKED and PARSE_BREAK mean here what they mean there, and only MISS says the
catalogue does not know the track. ``no-isrc`` is the sixth: the value handed in
was empty or does not read as an ISRC, so nothing was asked. A file with no
ISRC, a track the catalogue does not know and a catalogue that could not be read
are three facts a person acts on in three ways, and folding any two together is
absence read as evidence of absence.

A REFUSAL IS AN ANSWER AND NOTHING TRIES TO GET PAST ONE. A 403, a 429 that
outlasted the shared backoff, a challenge page and the catalogue's own quota
error are BLOCKED, read through the same check the fallbacks use (R-791). The
quota error is not retried at all. The request names this tool rather than a
browser, because this is a public API and not a page, and a client that
disguised itself to one would be the first step of the thing this module never
does.

A REFUSAL IS REMEMBERED FOR THE REST OF THE RUN. Once the catalogue has
answered BLOCKED, the lookup asks it nothing further and answers BLOCKED for
every later ISRC, saying so. A worker builds its seam per file, and without the
memory a rate limited sweep would spend the whole backoff on every file and
keep sending requests to a catalogue that had said stop. So the worker's lookup
is one per process, :func:`for_lookup`, and the next run asks again.

NO PICTURE IS READ OFF THIS CATALOGUE. Pictures stay the record shops' rows.
A first draft took the album cover and the review found two faults in one
sitting, a placeholder image for an album with no artwork and a fetch that
went out under the browser identity, so the cover was dropped rather than
patched. A picture a record shop's row already named is kept and says whose
it is.

AN ERROR THIS READER DOES NOT KNOW IS A PARSE BREAK, NOT A MISS. The catalogue
answers errors inside a 200, so the status says nothing, and reading an unknown
error as "no such track" would report a catalogue that changed its rules as a
library of tracks nobody carries.

THE ANSWER IS CHECKED AGAINST THE QUESTION. The track that comes back carries
its own ISRC, and one that names a different recording, or none, is not read as
this track's genre. The album identifier becomes a URL, so it is an integer or
it is nothing.

THE GENRE IS THE ALBUM'S, NOT THE TRACK'S, and that limit is accepted rather
than hidden. A dance remix of a non dance artist that Beatport misses files as
non dance. The author took that on 2026-10-01, and it is why Beatport is asked
first and a usable answer from it is never replaced.

BEATPORT MUST HAVE ANSWERED BEFORE THIS CATALOGUE IS ASKED. A genre is written
once, fill if empty, so an album level answer written while Beatport was
unreachable would stand in for Beatport's for good. When Beatport's answer is
anything but a match or a miss, this catalogue is recorded as not asked and the
file stays askable. The two fallbacks do not hold it back: they refuse this
machine on every search, and waiting on them would mean never asking.

A WORD NOTHING DECLARES IS A DECLINE HERE AND A WRITE FOR BEATPORT, on purpose.
The resolver's last tier passes an unknown word through so a new dance genre
survives long enough to be noticed. A general catalogue's vocabulary is a
different one, a few dozen broad words, and passing those through would file
every track it calls by a broad name under a word no folder holds. So an answer
is written only when it maps to a folder, and the first of an album's genres
that does is the one used.

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
from cratekit.core import routing
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging import searchers
from cratekit.tagging.searchers import Answer, Fetch, Pacer
from cratekit.tagging.tag import NO_ISRC, PublishedGenre, SearchHit, SourceAnswer

#: The general catalogue, as a file's record names it. One, on the measurement
#: the plan records: of the two others tried, one published no genre for any of
#: 79 tracks and the other found none of 30.
SOURCE = "deezer"

TRACK_BY_ISRC = "https://api.deezer.com/track/isrc:"
ALBUM = "https://api.deezer.com/album/"

#: What every request here says about itself. This tool, by name, asking for
#: JSON. Never the browser identity the record shops are asked with.
HEADERS = {
    "User-Agent": f"cratekit/{__version__} (published genre lookup by ISRC)",
    "Accept": "application/json",
}

#: The answers that leave the question open, the searchers' own tuple.
UNREAD: tuple[str, ...] = searchers.UNREAD_ANSWERS

#: Every word a file's record may carry for the general catalogue. A closed set,
#: so a summary can zero fill it.
ANSWERS: tuple[str, ...] = (
    *(answer.value for answer in Answer),
    NO_ISRC,
    searchers.NOT_ASKED,
)

#: The codes of the catalogue's published error table this reader acts on. An
#: error arrives inside a 200, so the code is the only thing that tells a track
#: nobody listed from a refusal of this client.
_NO_DATA = 800
_QUOTA = 4
_BUSY = 700

#: The error type the catalogue gives a client it will not serve without
#: credentials. A refusal of this client, whatever its code.
_PERMISSION = "OAuthException"

#: Beatport's answers that count as Beatport having ANSWERED. Anything else and
#: the general catalogue is not asked, see the module docstring.
_BEATPORT_ANSWERED = (Answer.MATCHED.value, Answer.MISS.value)


@dataclass(frozen=True, slots=True)
class Published:
    """What the general catalogue said about one ISRC.

    ``answer`` is one of :data:`ANSWERS` other than ``not-asked``. ``genres`` is
    every genre the catalogue lists for the track's album, in its own order and
    its own words, and is empty for every answer but a match. A match with no
    genres is a track the catalogue knows and publishes no genre for.
    """

    source: str
    answer: str
    genres: tuple[str, ...] = ()
    note: str = ""


#: Given an ISRC as some row or tag spelled it, what the catalogue published.
#: Answers and does not raise.
Lookup = Callable[[object], Published]


# ---------------------------------------------------------------------------
# Reading one answer
# ---------------------------------------------------------------------------


def _said(answer: Answer, note: str = "") -> Published:
    return Published(SOURCE, answer.value, note=note)


def _error(payload: dict[str, Any]) -> Published | None:
    """The answer an ``error`` object is, or None when the payload carries none.

    FOUR ERRORS ARE KNOWN AND EVERY OTHER ONE IS A PARSE BREAK. "No data" is the
    only one that says the catalogue does not list what was asked for. The quota
    error and a permission error are refusals of this client. "Service busy" is
    the catalogue saying try later. An error outside those is one this reader
    was never written against, and calling it a miss would be a guess.
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
    """One paced touch: the JSON object it answered, or the answer its absence is.

    The refusal check is the fallbacks' own, so a block is recognised here on
    exactly the evidence it is recognised on there, and is never answered.
    """
    pacer.wait()
    page = fetch(url)
    refused = searchers.unread_outcome(SOURCE, page)
    if refused is not None:
        return _said(refused.answer, refused.note)
    try:
        payload = json.loads(page.text or "")
    except ValueError:
        payload = None
    if not isinstance(payload, dict):
        return _said(
            Answer.PARSE_BREAK, "the catalogue's answer is not the JSON object this reader knows"
        )
    return payload


def _genre_names(listing: dict[str, Any]) -> tuple[str, ...] | None:
    """The album's genre names in the catalogue's order, or None for an unknown shape.

    None and an empty tuple are different answers. Empty is an album the
    catalogue publishes no genre for. None is a listing this reader cannot
    read: no genre list at all, or entries present and none of them carrying a
    name, which is the only evidence that separates a redesign from an album
    with no genre.
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

    ``albums`` is the lookup's memory of the genre lists it has already read,
    by album identifier. A release's tracks share an album, so the second track
    asks for the track alone. Only a list that was READ is remembered: a
    refusal or an unreadable album is asked about again by the next track.
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
            # THE TRACK IS KNOWN AND ITS ALBUM IS NOT LISTED. Not a miss, which
            # would say the catalogue does not know the track it just named.
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


#: What separates two values in one ISRC field. An ID3 text frame holding two
#: values reads back joined by a null, and people type the rest.
_ISRC_SEPARATORS = re.compile(r"[\x00;,/|]")


def _first_isrc(value: object) -> str:
    """The folded ISRC a value holds, the first when it holds several, or empty.

    The whole value is tried first, through the one fold the rest of the product
    matches ISRCs with. A field carrying two is read as its first that reads as
    an ISRC, because driven on 2026-10-01 an ID3 frame written with two values
    came back as one string joined by a null, which folds to nothing, and the
    file would have been reported as carrying no ISRC while it carried two.
    """
    whole = isrc_token(value)
    if whole:
        return whole
    for part in _ISRC_SEPARATORS.split(str(value or "")):
        token = isrc_token(part)
        if token:
            return token
    return ""


def genre_lookup(
    *,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
    pacing: Pacer | None = None,
) -> Lookup:
    """Build the lookup: an ISRC in, what the general catalogue published out.

    The seams are the searcher's own shapes, a fetch, a sleep and a pacer, so
    the suite drives every answer with nothing on the network. Every touch is
    paced, the first included, at the searchers' interval, which is far inside
    the catalogue's published limit.

    THE ISRC IS FOLDED AND CHECKED BEFORE IT BECOMES A URL. A tag is text
    somebody else wrote, and one that does not read as an ISRC is ``no-isrc``
    and never a request.

    ONE LOOKUP REMEMBERS TWO THINGS, both for its own lifetime. The genre lists
    it has read, by album, so a release is asked about once. And the first
    BLOCKED answer: from then on nothing is asked and every ISRC is answered
    BLOCKED, with a note saying it was not asked and why. Waiting out a rate
    limit on every file is the nearest this module could come to arguing with
    one, so it does not. An unreachable answer is not remembered: that is a
    network, and the next file may find it back.
    """
    naps = time.sleep if sleep is None else sleep
    pacer = Pacer(sleep=naps) if pacing is None else pacing
    touch = searchers.default_fetch(sleep=naps, headers=HEADERS) if fetch is None else fetch
    albums: dict[int, tuple[str, ...]] = {}
    refusals: list[Published] = []

    def lookup(isrc: object) -> Published:
        token = _first_isrc(isrc)
        if not token:
            given = str(isrc or "").strip()
            return Published(
                SOURCE,
                NO_ISRC,
                note=f"{given!r} does not read as an ISRC" if given else "no ISRC was given",
            )
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


# ---------------------------------------------------------------------------
# Choosing among an album's genres, for one declared taxonomy
# ---------------------------------------------------------------------------


def choose(declared: Taxonomy, genres: Sequence[str]) -> tuple[str, str] | None:
    """The first published genre that maps to a folder, with the tag to write.

    The catalogue's word and the taxonomy's tag for it, or None when no word of
    the album's maps anywhere. "Maps to a folder" is the shipped resolver
    answering with a BUCKET, not declining, and not a name the taxonomy lists as
    too coarse to be a final tag. So the resolver's pass through tier and a rule
    that declares a tag with no bucket are both passed over: each would put a
    word on the file that no folder holds.

    IN THE CATALOGUE'S ORDER, because that order is the only ranking it
    publishes, and a chooser that preferred the narrowest or the rarest word
    would be this module forming an opinion about music.

    THE TAG IS THE RESOLVER'S ANSWER AND NOTHING HERE ADJUSTS IT. The alias
    table was written against the record shops' vocabulary and this catalogue's
    broad words inherit it as it stands, which is recorded as a residual with
    the words measured rather than corrected by a second table in this module.
    """
    for word in genres:
        suggestion = routing.suggest_tag(declared, word)
        tag = suggestion.tag
        if suggestion.declined or suggestion.bucket_id is None or not tag:
            continue
        if declared.is_too_coarse_as_source(tag):
            continue
        return word, tag
    return None


# ---------------------------------------------------------------------------
# The tagger's use of it
# ---------------------------------------------------------------------------


def second_opinion(declared: Taxonomy, *, lookup: Lookup | None = None) -> PublishedGenre:
    """Build the seam :func:`cratekit.tagging.tag.tag_one` offers a hit to.

    Given the searcher's hit and the file's ISRC tag, it returns the hit to act
    on, with the general catalogue's answer appended to the hit's record. Every
    rule of when the catalogue is asked lives here, in one place:

    * a hit that carries no per source answers is returned untouched. Whether
      Beatport answered cannot be read off it, so nothing is asked on its
      strength;
    * a hit that already has a genre, and a file that needs none (an ISRC of
      None), are recorded ``not-asked``. That is R4: a usable answer from a
      record shop is never replaced;
    * a hit whose Beatport answer is not a match or a miss is recorded
      ``not-asked`` with the reason, and the file stays as the searcher left it;
    * otherwise the catalogue is asked. A genre that maps to a folder becomes
      the hit's genre, with no flag saying it was inferred, because it was not.
      Anything else leaves the hit a decline that says what was answered.

    A DECLINE KEEPS THE RECORD SHOP'S WORD WHEN THERE IS ONE. Beatport calling a
    track by a catch-all and this catalogue calling it by another are both in
    the answers, and the file's own ``source_genre`` stays the first, since the
    alias a person would add is against the catalogue that sells the record.

    A DECLINED WORD OF THIS CATALOGUE'S OWN BECOMES THE FILE'S, and the file is
    then ``unmapped-genre`` even beside fallbacks that could not be read. That
    is the engine's existing precedence, a declined word outranks an unread
    source, and it is kept on purpose: the word is what a person can act on,
    it reaches the summary's unresolved list, and the unread fallbacks are
    still in the file's record and in the warning that names a catalogue
    refused throughout.

    THE PICTURE STAYS THE RECORD SHOP'S. When this catalogue supplies the genre
    for a hit whose picture a shop's row named, ``art_source`` says whose it is.
    """
    ask = genre_lookup() if lookup is None else lookup

    def decide(hit: SearchHit, isrc: str | None) -> SearchHit:
        if not hit.answers:
            return hit

        def recorded(entry: SourceAnswer, **changed: Any) -> SearchHit:
            return replace(hit, answers=(*hit.answers, entry), **changed)

        if hit.genre or isrc is None:
            return recorded(SourceAnswer(SOURCE, searchers.NOT_ASKED))
        first = next((said for said in hit.answers if said.source == searchers.BEATPORT), None)
        if first is None or first.answer not in _BEATPORT_ANSWERED:
            return recorded(
                SourceAnswer(
                    SOURCE,
                    searchers.NOT_ASKED,
                    note=f"{searchers.BEATPORT} was not read for this track, and the "
                    f"general catalogue is asked only once it has answered",
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
        if picked is None and hit.source_genre:
            return recorded(entry)
        # THIS CATALOGUE BECOMES THE HIT'S SOURCE, for a genre to write or for a
        # declined word of its own. A picture already on the hit came off a
        # record shop's row and keeps that shop's name.
        return recorded(
            entry,
            genre=picked[1] if picked else None,
            source=SOURCE,
            source_genre=word,
            off_taxonomy=False,
            art_source=(hit.art_source or hit.source) if hit.art_url else "",
        )

    return decide


# ---------------------------------------------------------------------------
# The binders, looked up at call time
# ---------------------------------------------------------------------------

#: The one lookup this process asks the catalogue through, built on first use.
_shared: list[Lookup] = []


def for_lookup() -> Lookup:
    """The lookup a caller should use, looked up rather than constructed.

    The same shape and the same reason as
    :func:`cratekit.tagging.searchers.for_taxonomy`: a test replaces this
    attribute on this module, and a caller that built its own lookup inline
    would leave it nowhere to hand a fake in. Building one touches no network.
    This is the entry the label genre gate calls for a release's ISRC.

    ONE PER PROCESS, unlike the searcher's binder. A worker asks for its seam
    once per file, and the lookup's memory of a refusal and of the albums it
    has read is only worth having if the next file meets the same lookup. A job
    is driven in one process, so the memory lasts the run and no longer.
    """
    if not _shared:
        _shared.append(genre_lookup())
    return _shared[0]


def for_taxonomy(declared: Taxonomy) -> PublishedGenre:
    """The seam a tagging worker should hand :func:`cratekit.tagging.tag.tag_one`.

    Built over :func:`for_lookup`, read off this module at call time, so
    replacing the lookup replaces what the worker asks. The in process limit
    R-226 records for the searcher's binder applies here too.
    """
    return second_opinion(declared, lookup=for_lookup())


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
    "for_taxonomy",
    "genre_lookup",
    "second_opinion",
]
