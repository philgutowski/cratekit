"""The one COLLECTION TRACK emitter. Gridless, Location-faithful (R17, KTD27).

``tests/test_no_beatgrid_ever.py`` holds this emitter. Two rules, both absolute:

1. Never emit a tempo child element or a real average BPM, so tracks import
   gridless and rekordbox derives BPM and grid from the audio. An inizio value
   in the metadata is a dormant file tag and never becomes a grid element.
2. A ``Location`` is inherited byte-identical from a Fresh Export or made by
   :func:`cratekit.core.locations.location_url`; a second encoder would be the
   byte mismatch that silently duplicates a collection row (KTD27).

A U22 stub listing (``TRACK Name="..."`` with no Location) is not a Fresh
Export, and splicing into one is refused.

Layer: modules.
"""

from __future__ import annotations

import re

from cratekit.core import locations, routing, taxonomy
from cratekit.core.cause import CratekitError, refuse
from cratekit.write import rbxml
from cratekit.write.rbxml import xml_escape_attr

#: The one AverageBpm value this emitter may write. A string, because the
#: attribute is compared as bytes. Interpolating a number here is the defect.
GRIDLESS_AVERAGE_BPM = "0.00"

#: Synthetic TrackIDs start above anything rekordbox assigns, and past every
#: existing id, so a chained inbox never reuses one.
SYNTHETIC_TID_BASE = 900_000_000

_ORIGIN = ("intake.collection_xml",)

_COLLECTION_ENTRIES = re.compile(rb'<COLLECTION\b[^>]*\bEntries="(\d+)"')
_TRACK_ID = re.compile(rb'<TRACK\b[^>]*\bTrackID="(\d+)"')
_TRACK_NAME_ONLY = re.compile(rb"<TRACK\b[^>]*\bName=")


def _rating_for(energy: object, declared: taxonomy.Taxonomy) -> int:
    """Star rating from energy by the active taxonomy's cuts (R-685), or 0 with no reading."""
    if energy is None or energy == "":
        return 0
    try:
        level = int(energy)
    except (TypeError, ValueError):
        return 0
    value = routing.energy_rating(declared, level)
    return int(value) if value is not None else 0


def _location_attr(raw: object) -> str:
    """Inherit a Location, or synthesize one; re-encoding an inherited one is KTD27's mismatch."""
    text = str(raw)
    if locations.looks_like_location(text):
        return text
    return locations.location_url(text)


def build_track_xml(
    tid: int, meta: dict, date_added: str, *, declared: taxonomy.Taxonomy
) -> str:
    """One COLLECTION TRACK element, gridless, CRLF, rekordbox attribute order.

    ``inizio`` and ``bpm`` are ignored and never reach the XML. ``declared``'s
    energy cuts give the rating.
    """
    escape = xml_escape_attr
    rating = _rating_for(meta.get("energy"), declared)
    location = _location_attr(meta["location"])
    kind = escape(meta.get("kind") or "FLAC File")
    # The empty ``grid`` binding is the whole R17 claim in one place, held by
    # the no-beatgrid suite.
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
    """True when ``content`` is a U22 listing: TRACK rows with names and no Location."""
    if b"<TRACK" not in content:
        return False
    if b"Location=" in content:
        return False
    return _TRACK_NAME_ONLY.search(content) is not None


def next_track_id(content: bytes, default: int = SYNTHETIC_TID_BASE) -> int:
    """One past every TrackID already in the document, at least ``default``."""
    existing = max((int(match.group(1)) for match in _TRACK_ID.finditer(content)), default=0)
    return max(default, existing) + 1


def _unusable(said: str) -> CratekitError:
    return refuse(
        "library-export-unusable",
        said,
        steps=("export the collection again from rekordbox and point intake at the new file",),
        origin=_ORIGIN,
    )


def _bump_collection_entries(content: bytearray, delta: int) -> None:
    match = _COLLECTION_ENTRIES.search(bytes(content))
    if match is None:
        raise _unusable(
            "this export has no COLLECTION Entries count, so a splice cannot "
            "say how many rows the document will hold after the insert"
        )
    new_value = str(max(0, int(match.group(1)) + delta)).encode("utf-8")
    content[match.start(1) : match.end(1)] = new_value


def splice_tracks(content: bytearray, tracks: list[str]) -> bytearray:
    """Insert TRACK elements before ``</COLLECTION>`` and bump Entries; a U22 stub refuses."""
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
            origin=_ORIGIN,
        )
    span = rbxml.collection_span(raw)
    if span is None:
        raise _unusable(
            "this export has no COLLECTION section, so there is nowhere to put a new TRACK element"
        )
    close = raw.rfind(b"</COLLECTION>", span[0], span[1] if span[1] > 0 else None)
    if close < 0:
        close = raw.rfind(b"</COLLECTION>")
    if close < 0:
        raise _unusable("this export has a COLLECTION open tag and no close tag")
    content[close:close] = "".join(tracks).encode("utf-8")
    _bump_collection_entries(content, len(tracks))
    return content
