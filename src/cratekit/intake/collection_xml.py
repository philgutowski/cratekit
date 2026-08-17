"""The one COLLECTION TRACK emitter. Gridless, Location-faithful (R17, KTD27).

This is the subject ``tests/test_no_beatgrid_ever.py`` has been waiting for.
No other unit ports it. Without this file that suite has no emitter to hold
and the Definition of Done's XML-layer claim is unbacked.

Two rules, both absolute:

1. Never emit a tempo child element, and never emit a real average BPM.
   Tracks import gridless so rekordbox derives BPM and grid from the audio.
   A first-beat inizio value in the metadata is a dormant file tag. It must
   never become a grid element. The adversarial case (inizio set, energy
   missing) is the shape the source system's removed tempo path fired on.
2. A ``Location`` is either inherited byte-identical from a Fresh Export or
   synthesized through :func:`cratekit.core.locations.location_url`. A second
   encoder here would be the byte mismatch that silently duplicates a
   collection row (KTD27).

A U22 stub listing (``TRACK Name="..."`` with no Location) is not a Fresh
Export. Passing one in as the document to splice is refused rather than
treated as an importable file.

Layer: modules.
"""

from __future__ import annotations

import re
from pathlib import Path

from cratekit.core import locations, routing, taxonomy
from cratekit.core.cause import refuse
from cratekit.write import rbxml
from cratekit.write.rbxml import xml_escape_attr

#: The one AverageBpm value this emitter may write. A string, because the
#: attribute is compared as bytes. Interpolating a number here is the defect.
GRIDLESS_AVERAGE_BPM = "0.00"

#: Synthetic TrackIDs start here so they sit above anything rekordbox assigned
#: in a typical library. Bumped past every existing id at splice time so a
#: chained inbox never reuses one.
SYNTHETIC_TID_BASE = 900_000_000

_COLLECTION_ENTRIES = re.compile(rb'<COLLECTION\b[^>]*\bEntries="(\d+)"')
_TRACK_ID = re.compile(rb'<TRACK\b[^>]*\bTrackID="(\d+)"')
_TRACK_NAME_ONLY = re.compile(rb"<TRACK\b[^>]*\bName=")


def _rating_for(energy: object) -> int:
    """Star rating from energy, or 0 when there is no reading.

    Cuts come from the shipped taxonomy so a later template that changes the
    even-fifths map is the one this emitter follows. A hardcoded table here
    would be a second opinion about a value the template already holds.
    """
    if energy is None or energy == "":
        return 0
    try:
        level = int(energy)
    except (TypeError, ValueError):
        return 0
    value = routing.energy_rating(taxonomy.default_taxonomy(), level)
    return int(value) if value is not None else 0


def _location_attr(raw: object) -> str:
    """Inherit a Location, or synthesize one. Never invent a third spelling.

    A value that already looks like a Location is the Fresh Export's own
    bytes, decoded only as far as Python strings require. Re-encoding it
    would be the KTD27 mismatch even when the path is the same file.
    """
    text = str(raw)
    if locations.looks_like_location(text):
        return text
    return locations.location_url(text)


def build_track_xml(tid: int, meta: dict, date_added: str) -> str:
    """One COLLECTION TRACK element, gridless, CRLF, rekordbox attribute order.

    ``inizio`` may be present. It is ignored. ``bpm`` may be present. It is
    ignored. Neither may reach the XML.
    """
    escape = xml_escape_attr
    rating = _rating_for(meta.get("energy"))
    location = _location_attr(meta["location"])
    kind = escape(meta.get("kind") or "FLAC File")
    # The empty ``grid`` binding is the whole R17 claim in one place. A
    # future edit that puts a tempo child back has to assign it here, and
    # the no-beatgrid suite fails the moment that happens.
    grid = ""
    return (
        f'    <TRACK TrackID="{int(tid)}" Name="{escape(meta["name"])}" '
        f'Artist="{escape(meta["artist"])}" Composer=""\r\n'
        f'           Album="{escape(meta.get("album") or "")}" Grouping="" '
        f'Genre="{escape(meta.get("genre") or "")}" Kind="{kind}" '
        f'Size="{int(meta.get("size_bytes") or 0)}"\r\n'
        f'           TotalTime="{int(meta.get("duration_s") or 0)}" '
        f'DiscNumber="0" TrackNumber="0" Year="0" AverageBpm="0.00"\r\n'
        f'           DateAdded="{escape(date_added)}" '
        f'BitRate="{int(meta.get("bitrate_kbps") or 0)}" '
        f'SampleRate="{int(meta.get("sample_rate") or 0)}" Comments=""\r\n'
        f'           PlayCount="0" Rating="{rating}" '
        f'Location="{escape(location)}"\r\n'
        f'           Remixer="" Tonality="{escape(meta.get("tonality") or "")}" '
        f'Label="" Mix="">\r\n'
        f"{grid}"
        f"    </TRACK>\r\n"
    )


def is_stub_listing(content: bytes) -> bool:
    """True when ``content`` is a U22 listing, not a Fresh Export splice.

    The stub writer emits ``<TRACK Name="identity"/>`` rows and no Location.
    A real export carries Location on every collection row. Treating the
    listing as importable is how a later sync would try to consume debris.
    """
    if b"<TRACK" not in content:
        return False
    if b"Location=" in content:
        return False
    return _TRACK_NAME_ONLY.search(content) is not None


def next_track_id(content: bytes, default: int = SYNTHETIC_TID_BASE) -> int:
    """One past every TrackID already in the document, at least ``default``."""
    existing = max(
        (int(match.group(1)) for match in _TRACK_ID.finditer(content)),
        default=0,
    )
    return max(default, existing) + 1


def _bump_collection_entries(content: bytearray, delta: int) -> None:
    match = _COLLECTION_ENTRIES.search(bytes(content))
    if match is None:
        raise refuse(
            "library-export-unusable",
            "this export has no COLLECTION Entries count, so a splice cannot "
            "say how many rows the document will hold after the insert",
            steps=(
                "export the collection again from rekordbox and point intake at "
                "the new file",
            ),
            origin=("intake.collection_xml",),
        )
    new_value = str(max(0, int(match.group(1)) + delta)).encode("utf-8")
    content[match.start(1) : match.end(1)] = new_value


def splice_tracks(
    content: bytearray,
    tracks: list[str],
) -> bytearray:
    """Insert TRACK elements before ``</COLLECTION>`` and bump Entries.

    Refuses a U22 stub so a listing cannot be dressed up as a splice.
    """
    raw = bytes(content)
    if is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
            "this file is a U22 stub listing, not a Fresh Export, so it is "
            "not an importable splice and new tracks cannot be added to it",
            steps=(
                "take a Fresh Export from rekordbox",
                "do not treat a U22 stub listing as an importable splice",
            ),
            origin=("intake.collection_xml",),
        )
    span = rbxml.collection_span(raw)
    if span is None:
        raise refuse(
            "library-export-unusable",
            "this export has no COLLECTION section, so there is nowhere to "
            "put a new TRACK element",
            steps=(
                "export the collection again from rekordbox and point intake at "
                "the new file",
            ),
            origin=("intake.collection_xml",),
        )
    close = raw.rfind(b"</COLLECTION>", span[0], span[1] if span[1] > 0 else None)
    if close < 0:
        close = raw.rfind(b"</COLLECTION>")
    if close < 0:
        raise refuse(
            "library-export-unusable",
            "this export has a COLLECTION open tag and no close tag",
            steps=(
                "export the collection again from rekordbox and point intake at "
                "the new file",
            ),
            origin=("intake.collection_xml",),
        )
    payload = "".join(tracks).encode("utf-8")
    if close >= 2 and raw[close - 2 : close] == rbxml.CRLF:
        insert_at = close
    else:
        insert_at = close
    content[insert_at:insert_at] = payload
    _bump_collection_entries(content, len(tracks))
    return content


def write_inboxed(export: Path, tracks: list[str], destination: Path) -> Path:
    """Splice ``tracks`` into a copy of ``export`` and write ``destination``."""
    data = export.read_bytes()
    buf = bytearray(data)
    splice_tracks(buf, tracks)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(bytes(buf))
    return destination
