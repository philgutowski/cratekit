"""The scraped record shops, Beatport, Traxsource and Bandcamp, asked by artist and title.

Each search is handed the fetch, the pacer and ``query``, the one escaping of
the question :mod:`cratekit.tagging.searchers` owns, and answers a
:class:`~cratekit.tagging.catalogues.SourceOutcome`. A page with no result to
read goes through :func:`~cratekit.tagging.catalogues.unread_outcome`, so a
refusal of this client is BLOCKED and an outage UNREACHABLE.

THE PICTURE RIDES THE GENRE'S ROW: both come off the one row that matched, or
a file wears another record's cover. Traxsource names none.

Layer: modules.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from cratekit.core import routing
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging import titles
from cratekit.tagging.catalogues import (
    _DASH,
    _GONE_STATUSES,
    BANDCAMP,
    BEATPORT,
    TRAXSOURCE,
    Answer,
    Fetch,
    Pacer,
    SourceOutcome,
    _artist_matches,
    _artist_parts,
    _identifies,
    _normalized,
    _title_matches,
    _words,
    unread_outcome,
)

BEATPORT_SEARCH = "https://www.beatport.com/search"
TRAXSOURCE_SEARCH = "https://www.traxsource.com/search/tracks"
BANDCAMP_SEARCH = "https://bandcamp.com/search"

#: The escaped query a search sends, ``searchers._query``.
Query = Callable[[str, str], str]

#: Release descriptors a Bandcamp seller types among the genres. No genre word
#: appears here: a tag too coarse to write is the taxonomy's judgement to make.
_TAG_NOISE = frozenset({"edit", "edits", "remix", "remixes", "extended mix"})

_NEXT_DATA = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.DOTALL
)


def _beatport_tracks(page: str) -> list[dict[str, Any]] | None:
    """The track objects on a search page, or None when the shape is unknown.

    An empty list is a search that found nothing; None is a page this parser
    has never seen, since the payload is present with or without results.
    """
    found = _NEXT_DATA.search(page)
    if not found:
        return None
    try:
        payload = json.loads(found.group(1))
    except ValueError:
        return None
    queries = (
        payload.get("props", {})
        .get("pageProps", {})
        .get("dehydratedState", {})
        .get("queries", [])
    )
    for query in queries:
        data = query.get("state", {}).get("data", {})
        if "tracks" in data:
            return data["tracks"].get("data", [])
    return None


def _beatport_genre(track: dict[str, Any]) -> str:
    genres = track.get("genre") or []
    if not genres:
        return ""
    return genres[0].get("genre_name") or ""


_BEATPORT_IMAGE_SIZE = re.compile(r"image_size/\d+x\d+/")

#: The edge Beatport is asked to serve a cover at, large enough that the
#: re-encode to the CDJ size only ever shrinks.
BEATPORT_IMAGE_EDGE = 1400


def _web_url(value: object) -> str:
    """``value`` when it is an http or https URL, else empty: a payload field
    somebody else chose becomes a GET."""
    text = value.strip() if isinstance(value, str) else ""
    return text if text.startswith(("https://", "http://")) else ""


def _beatport_art(track: dict[str, Any]) -> str:
    """The row's release cover, resized, or empty when the row names none."""
    release = track.get("release")
    uri = _web_url(release.get("release_image_uri") if isinstance(release, dict) else "")
    edge = BEATPORT_IMAGE_EDGE
    return _BEATPORT_IMAGE_SIZE.sub(f"image_size/{edge}x{edge}/", uri)


@dataclass(frozen=True, slots=True)
class _Pick:
    """The best scoring Beatport row's genre and picture, read off ONE row."""

    genre: str
    art_url: str = ""


def _beatport_best(tracks: Iterable[dict[str, Any]], artist: str, title: str) -> _Pick | None:
    """The genre and picture off the best scoring track, or None when nothing scores.

    A row with no genre is no candidate, or a title alone would turn an answer
    into a decline. The title is ranked past its ``KEY - BPM - `` head and read
    as the shared matcher reads it (R-1534, R-1631, R-1646): first the row's
    name with its mix in brackets, then the core title word for word, then
    :func:`titles.matches`. No tier reads a name inside the other's brackets,
    and an empty credit is no credit.
    """
    title_normalized = _normalized(title)
    if not _identifies(title_normalized):
        return None
    proper = titles.without_head(title_normalized)
    whole_title = _words(titles.own_core(proper)[0])
    searched_title = titles.read_file(title_normalized, artist)
    searched = _artist_parts(artist, r"[,&]")

    best_score = 0
    best: _Pick | None = None
    for track in tracks:
        genre = _beatport_genre(track)
        if not genre:
            continue
        name = _normalized(track.get("track_name", ""))
        if not _identifies(name):
            continue
        mix = _normalized(track.get("mix_name", ""))
        credited = [_normalized(entry.get("artist_name", "")) for entry in track.get("artists", [])]
        credited = [other for other in credited if other]

        artist_score = 0
        for part in searched:
            if any(part == other or part in other or other in part for other in credited):
                artist_score += 1
        if artist_score == 0:
            continue

        if _words(proper) == _words(f"{name} ({mix})"):
            title_score = 4
        elif whole_title == _words(name):
            title_score = 3
        elif titles.matches(searched_title, titles.read_beatport_row(name, mix)):
            title_score = 2
        else:
            continue

        # Title dominates: a shared artist over a different record is wrong,
        # a shared record with one credit missing is right.
        score = title_score * 10 + artist_score
        if score > best_score:
            best_score = score
            best = _Pick(genre, _beatport_art(track))
    return best


def _search_beatport(
    artist: str,
    title: str,
    *,
    fetch: Fetch,
    pacer: Pacer,
    query: Query,
    track: str | None = None,
    **_: Any,
) -> SourceOutcome:
    pacer.wait()
    page = fetch(f"{BEATPORT_SEARCH}?q={query(artist, title if track is None else track)}")
    # THE PAYLOAD IS READ FIRST, the refusal check only when there is none
    # (U281): a 200 challenge page has no payload and is BLOCKED, not a parser
    # defect (R-794), and a page with the payload is results whatever script
    # Cloudflare added to it.
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
        if refused is not None:
            return refused
        return SourceOutcome(
            BEATPORT,
            Answer.PARSE_BREAK,
            note="the search page carries no readable track payload",
        )
    pick = _beatport_best(tracks, artist, title)
    if pick is None:
        return SourceOutcome(BEATPORT, Answer.MISS)
    return SourceOutcome(
        BEATPORT, Answer.MATCHED, source_genre=pick.genre, art_url=pick.art_url
    )


_TRAX_ROW = re.compile(r'data-trid="\d+"')
_TRAX_TITLE = re.compile(r'class="trk-cell title".*?<a[^>]*>([^<]+)</a>', re.DOTALL)
_TRAX_ARTISTS = re.compile(r'class="com-artists"[^>]*>([^<]+)</a>')
_TRAX_GENRE = re.compile(r'class="trk-cell genre".*?<a[^>]*>([^<]+)</a>', re.DOTALL)


def _traxsource_rows(page: str) -> list[str]:
    """The result rows, sliced at their own markers: a match to a closing tag
    breaks when a row gains a nested element."""
    starts = [found.start() for found in _TRAX_ROW.finditer(page)]
    if not starts:
        return []
    bounds = [*starts, len(page)]
    return [page[bounds[index] : bounds[index + 1]] for index in range(len(starts))]


def _search_traxsource(
    artist: str,
    title: str,
    *,
    fetch: Fetch,
    pacer: Pacer,
    query: Query,
    track: str | None = None,
    **_: Any,
) -> SourceOutcome:
    pacer.wait()
    page = fetch(f"{TRAXSOURCE_SEARCH}?term={query(artist, title if track is None else track)}&page=1")
    refused = unread_outcome(TRAXSOURCE, page)
    if refused is not None:
        return refused

    rows = _traxsource_rows(page.text or "")
    titles_read = 0
    for row in rows:
        found_title = _TRAX_TITLE.search(row)
        if not found_title:
            continue
        titles_read += 1
        found_genre = _TRAX_GENRE.search(row)
        if not found_genre:
            continue
        found_artist = _TRAX_ARTISTS.search(row)
        credited = found_artist.group(1).strip() if found_artist else ""
        if not _title_matches(title, found_title.group(1).strip(), artist=artist):
            continue
        if credited and not _artist_matches(artist, credited):
            continue
        return SourceOutcome(
            TRAXSOURCE, Answer.MATCHED, source_genre=found_genre.group(1).strip()
        )

    if rows and titles_read == 0:
        # Rows present and none read is the only evidence of a redesign.
        return SourceOutcome(
            TRAXSOURCE,
            Answer.PARSE_BREAK,
            note="result rows are present and none of them parsed",
        )
    return SourceOutcome(TRAXSOURCE, Answer.MISS)


_BC_RESULT = re.compile(r'class="searchresult.*?</li>', re.DOTALL)
_BC_HEADING = re.compile(
    r'class="heading">\s*<a[^>]*href="(https://[^"]+bandcamp\.com/track/[^"]+)"[^>]*>'
    r"\s*(.*?)\s*</a>",
    re.DOTALL,
)
_BC_SUBHEAD = re.compile(r'class="subhead">\s*(.*?)\s*</div>', re.DOTALL)
_BC_BY = re.compile(r"by\s+(.*?)$")
_BC_LISTING_GENRE = re.compile(r'class="genre">\s*genre:\s*(.*?)\s*</div>', re.DOTALL)
_BC_TAG = re.compile(r'<a class="tag"[^>]*>([^<]+)</a>')
_BC_LISTING_ART = re.compile(r'<img src="(https://f4\.bcbits\.com/img/[^"]+)"')
_BC_OG_IMAGE = re.compile(r'<meta property="og:image"\s+content="([^"]+)"')
_BC_IMAGE_SIZE = re.compile(r"_\d+\.jpg$")


def _bandcamp_art(found: re.Match[str] | None) -> str:
    """The picture a listing or a track page names, at ``_10``, the original
    upload, or empty."""
    if found is None:
        return ""
    return _BC_IMAGE_SIZE.sub("_10.jpg", _web_url(found.group(1)))


def _bandcamp_credited(entry: str) -> str:
    subhead = _BC_SUBHEAD.search(entry)
    if not subhead:
        return ""
    credited = _BC_BY.search(subhead.group(1).strip())
    return credited.group(1).strip() if credited else ""


def _bandcamp_heading_matches(title: str, heading: str, artist: str) -> bool:
    # A heading is sometimes "Artist - Title". Only a head naming the artist is
    # dropped, and then never read: "Sunrise Mood - Original Mix" is a title
    # and its version, never a title "Original Mix" (R-1631).
    head, dash, rest = heading.partition(_DASH)
    if dash and _artist_matches(artist, head):
        return _title_matches(title, rest, artist=artist)
    return _title_matches(title, heading, artist=artist)


def _bandcamp_tag(tags: Sequence[str], declared: Taxonomy) -> str:
    """Choose one tag out of a seller's free text list: the first the declared
    taxonomy recognises, capitalised location tags skipped, else the first
    remaining tag raw, so the decline names a string a person can alias."""
    candidates = [tag for tag in tags if tag == tag.lower() and tag not in _TAG_NOISE]
    for tag in candidates:
        suggestion = routing.suggest_tag(declared, tag)
        if suggestion.bucket_id is not None and not suggestion.declined:
            return tag
    return candidates[0] if candidates else ""


def _search_bandcamp(
    artist: str,
    title: str,
    *,
    fetch: Fetch,
    pacer: Pacer,
    declared: Taxonomy,
    query: Query,
    track: str | None = None,
) -> SourceOutcome:
    pacer.wait()
    page = fetch(f"{BANDCAMP_SEARCH}?q={query(artist, title if track is None else track)}&item_type=t")
    refused = unread_outcome(BANDCAMP, page)
    if refused is not None:
        return refused

    entries = _BC_RESULT.findall(page.text or "")
    headings_read = 0
    # A matched listing whose track page could not be read is no miss: it is
    # held while a later listing may answer. A block ends the walk over
    # listings, and a gone page, 404 or 410, is a dead listing passed over,
    # or the file would stay undecidable while the dead link is listed.
    track_unread: SourceOutcome | None = None
    for entry in entries:
        heading = _BC_HEADING.search(entry)
        if not heading:
            continue
        headings_read += 1
        track_url, text = heading.group(1).split("?")[0], heading.group(2).strip()
        if not _bandcamp_heading_matches(title, text, artist):
            continue
        credited = _bandcamp_credited(entry)
        if credited and not _artist_matches(artist, credited):
            continue

        listed = _BC_LISTING_GENRE.search(entry)
        genre = listed.group(1).strip() if listed else ""
        art_url = _bandcamp_art(_BC_LISTING_ART.search(entry))
        if not genre or not art_url:
            # The track page, a second paced touch, usually carries the genre
            # and the picture; the listing's own answer wins where it gave one.
            pacer.wait()
            track_page = fetch(track_url)
            unread = unread_outcome(BANDCAMP, track_page)
            if unread is None:
                text = track_page.text or ""
                genre = genre or _bandcamp_tag(_BC_TAG.findall(text), declared)
                art_url = art_url or _bandcamp_art(_BC_OG_IMAGE.search(text))
            elif not genre and unread.answer is Answer.BLOCKED:
                track_unread = unread
                break
            elif not genre and track_page.status not in _GONE_STATUSES:
                track_unread = track_unread or unread
        if genre:
            return SourceOutcome(
                BANDCAMP, Answer.MATCHED, source_genre=genre, art_url=art_url
            )

    if entries and headings_read == 0:
        return SourceOutcome(
            BANDCAMP,
            Answer.PARSE_BREAK,
            note="search results are present and none of them parsed",
        )
    if track_unread is not None:
        return track_unread
    return SourceOutcome(BANDCAMP, Answer.MISS)
