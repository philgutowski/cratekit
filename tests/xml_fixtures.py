"""Shared byte-level rekordbox XML builders for the test suite (not a test module).

Ported from the source system's ``tests/xml_fixtures.py``. Every fixture here is
pure in-memory bytes: no volume, no network, no real library. That is deliberate
and load-bearing, because the invariant these fixtures serve is a BYTE rule, and
a byte rule can only be tested against bytes you control completely.

The byte rules these builders encode, and why each one matters:

* **CRLF everywhere.** rekordbox writes ``\\r\\n`` and reads ``\\r\\n``. A bare LF
  smuggled into an export is not a cosmetic difference; the source system shipped
  a splicer that emitted one and rekordbox rendered the affected playlist wrong.
* **Exact indentation.** Anchors are found by byte pattern, and the splicers carry
  hardcoded indent widths. A fixture at the wrong indent silently stops proving
  anything, because the pattern it was written to exercise no longer matches.
* **The document skeleton lives in one place.** ``_xml_doc`` owns the header, the
  PRODUCT line, the PLAYLISTS/ROOT wrapper, and the footer, so each fixture below
  differs from its siblings only by the part it is actually testing.

Two names are deliberately kept from the source: ``_no_bare_lf`` and ``_xml_doc``
are referenced by name in the golden README, so renaming them would orphan the
documentation that explains what each golden locks.
"""

from __future__ import annotations

_EMPTY_COLLECTION = ['  <COLLECTION Entries="0">', "  </COLLECTION>"]

# Synthetic location prefix. Deliberately NOT a real volume path: the portability
# guard (tests/test_portability.py) treats any concrete /Volumes/<name>/ or
# /Users/<name>/ literal as a violation wherever it appears, tests included, and
# the source system had exactly this blind spot. A relative-looking synthetic
# path proves the same byte behaviour and stays portable.
_LOC_PREFIX = "file://localhost/library/"


def _xml_doc(*, collection: list[str], root_children: list[str]) -> bytes:
    """Assemble a byte-exact rekordbox export from its two varying parts.

    ``collection`` is the COLLECTION lines (including the open and close tags) and
    ``root_children`` is the children of the ROOT playlist NODE. Everything else,
    the header, the PRODUCT line, the wrapper, the footer, the CRLF, and the UTF-8
    encoding, is owned here so it cannot drift fixture by fixture.
    """
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<DJ_PLAYLISTS Version="1.0.0">',
        '  <PRODUCT Name="rekordbox" Version="6.0.0" Company="AlphaTheta"/>',
        *collection,
        "  <PLAYLISTS>",
        '    <NODE Type="0" Name="ROOT" Count="1">',
        *root_children,
        "    </NODE>",
        "  </PLAYLISTS>",
        "</DJ_PLAYLISTS>",
    ]
    return ("\r\n".join(lines) + "\r\n").encode("utf-8")


def _no_bare_lf(data: bytes) -> bool:
    """True when every LF in the payload is part of a CRLF.

    This is the byte-exact rule stated as a predicate. It requires at least one
    newline on purpose: a payload with no newline at all would pass a naive
    "contains no bare LF" check while proving nothing.
    """
    return b"\n" in data and data.replace(b"\r\n", b"").find(b"\n") == -1


def _fresh_xml() -> bytes:
    """A minimal but structurally real FRESH export: a CRLF COLLECTION and an
    empty INBOX folder. Enough for an intake splice to target, routing off."""
    return _xml_doc(
        collection=_EMPTY_COLLECTION,
        root_children=[
            '      <NODE Name="INBOX" Type="0" Count="0">',
            "      </NODE>",
        ],
    )


def _ml_track(tid: int, name: str, *, analyzed: bool = False) -> list[str]:
    """One COLLECTION TRACK element in the production multi-line shape.

    Open tag at 4 spaces, continuation attributes at 11, ``</TRACK>`` close at 4.

    ``analyzed=True`` mirrors a rekordbox-analyzed track from a real fresh export:
    a real ``AverageBpm`` and a ``<TEMPO>`` child. That is rekordbox-AUTHORED grid
    data. It must round-trip verbatim through any tool that subsets an export,
    while our own emitters must never CREATE it (R17). Both halves of that rule
    are asserted in tests/test_no_beatgrid_ever.py, and this builder is what makes
    the round-trip half testable.
    """
    bpm = "124.00" if analyzed else "0.00"
    lines = [
        f'    <TRACK TrackID="{tid}" Name="{name}" Artist="A" Composer=""',
        '           Album="" Genre="Deep House" Kind="FLAC File" Size="1000"',
        f'           TotalTime="300" Year="0" AverageBpm="{bpm}"',
        f'           Location="{_LOC_PREFIX}{tid}.flac"',
        '           Tonality="01A" Label="" Mix="">',
    ]
    if analyzed:
        lines.append('      <TEMPO Inizio="0.512" Bpm="124.00" Metro="4/4" Battito="1"/>')
    lines.append("    </TRACK>")
    return lines


def _routing_xml(*, collision: bool = False) -> bytes:
    """A FRESH export carrying the BY GENRE routing tree the splicers target.

    ROOT / BY GENRE / "Deep House" / "High Energy", where the sub-playlist is an
    empty self-closing node at the real 10-space indent, so a splice's hardcoded
    10-space ``</NODE>`` and 12-space TRACK indents land exactly as they do in
    production.

    ``collision=True`` adds a COLLECTION TRACK whose Name is the same string as the
    genre folder. Because a naive splicer scans for ``Name="Deep House"`` from byte
    zero, and COLLECTION precedes PLAYLISTS in the document, this fixture is the
    mis-anchor bait: it is the exact shape that made the source system's splicers
    warn and silently drop a routing write. Any splicer that is not scoped to
    <PLAYLISTS> fails on this fixture.
    """
    if collision:
        collection = [
            '  <COLLECTION Entries="1">',
            '    <TRACK TrackID="1" Name="Deep House" Artist="Bait" '
            'Location="file://localhost/bait.flac"/>',
            "  </COLLECTION>",
        ]
    else:
        collection = _EMPTY_COLLECTION
    return _xml_doc(
        collection=collection,
        root_children=[
            '      <NODE Type="0" Name="BY GENRE" Count="1">',
            '        <NODE Type="0" Name="Deep House" Count="1">',
            '          <NODE Name="High Energy" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
        ],
    )
