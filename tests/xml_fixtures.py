"""Shared byte-level rekordbox XML builders for the test suite (not a test module).

Ported from the source system, pure in-memory bytes, since the invariants are
byte rules: CRLF everywhere (a bare LF made rekordbox render a playlist
wrong), exact indentation (the splicers' anchors and indents are hardcoded),
and one document skeleton in ``_xml_doc``. ``_no_bare_lf`` and ``_xml_doc``
keep their source names, which the golden README cites.
"""

from __future__ import annotations

_EMPTY_COLLECTION = ['  <COLLECTION Entries="0">', "  </COLLECTION>"]

# Synthetic location prefix, never a real volume path, which the portability
# guard refuses in tests too.
_LOC_PREFIX = "file://localhost/library/"


def _xml_doc(*, collection: list[str], root_children: list[str]) -> bytes:
    """A byte-exact rekordbox export from its COLLECTION lines and ROOT's children."""
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
    """True when every LF in the payload is part of a CRLF, requiring at least one newline."""
    return b"\n" in data and data.replace(b"\r\n", b"").find(b"\n") == -1


def _fresh_xml() -> bytes:
    """A minimal FRESH export: a CRLF COLLECTION and an empty INBOX folder, routing off."""
    inbox = ['      <NODE Name="INBOX" Type="0" Count="0">', "      </NODE>"]
    return _xml_doc(collection=_EMPTY_COLLECTION, root_children=inbox)


def _ml_track(tid: int, name: str, *, analyzed: bool = False) -> list[str]:
    """One COLLECTION TRACK in the production multi-line shape (tag at 4, attributes at 11).

    ``analyzed=True`` adds rekordbox's own ``AverageBpm`` and ``<TEMPO>``, which must
    round-trip verbatim while our emitters never create one (R17, tests/test_no_beatgrid_ever.py).
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
    """A FRESH export with ROOT / BY GENRE / Deep House / High Energy, empty at the real indent.

    ``collision=True`` adds a COLLECTION TRACK named as the genre folder, the bait that
    made the source system's splicers mis-anchor outside <PLAYLISTS>.
    """
    collection = _EMPTY_COLLECTION
    if collision:
        bait = 'Name="Deep House" Artist="Bait" Location="file://localhost/bait.flac"/>'
        track = f'    <TRACK TrackID="1" {bait}'
        collection = ['  <COLLECTION Entries="1">', track, "  </COLLECTION>"]
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
