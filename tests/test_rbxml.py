"""The rekordbox XML byte rules: CRLF, indentation, scoping, and Entries arithmetic.

rekordbox's XML is not "some XML". It is a byte format with conventions that a
general-purpose serializer does not preserve, and every one of the rules below
was learned by breaking a real library.

The four rules, and the incident behind each:

* **CRLF only.** rekordbox writes ``\\r\\n``. A splicer that inserted a bare LF
  produced a playlist rekordbox rendered wrong, and the corruption was invisible
  in every text editor anyone looked at it in.
* **Never round-trip through a tree serializer.** Both ``lxml`` and the standard
  library collapse multi-line attributes, and rekordbox's display breaks on the
  result. Reads may parse; writes are byte splices into the original document.
* **Anchors are scoped to PLAYLISTS.** A search from byte zero for
  ``Name="Deep House"`` finds a COLLECTION TRACK of that name first, because
  COLLECTION precedes PLAYLISTS. The source system had three splicers that did
  exactly this: given a track named after a genre folder AND a track named after
  the sub-playlist, all three warned and silently dropped the routing write. The
  user saw a successful run and an empty playlist.
* **Patch Entries before computing offsets.** Growing ``Entries="0"`` to
  ``Entries="10"`` adds a byte. A splicer that recorded the closing tag's
  position first, then patched Entries, then wrote at the stale offset, corrupted
  the file tail. Ten tracks was the threshold, which is why it survived testing.

THIS FILE WAS SKIPPED UNTIL U17 LANDED THE BRIDGE. The assertions were ported
complete before the writer existed, nothing was stubbed to make them green, and
tests/test_pending_units.py would have failed the build the moment the module
appeared unless the gate came off. That ordering is what made the cutover safe:
the first version of the writer was measured against these, not reviewed against
a memory of them. Every assertion below is now armed.
"""

from __future__ import annotations

import re

from cratekit.core.locations import location_to_path, location_url
from cratekit.write import rbxml
from tests.xml_fixtures import _no_bare_lf, _routing_xml, _xml_doc

# ── escaping ─────────────────────────────────────────────────────────────────


def test_escaper_matches_rekordbox_semantics():
    """Match rekordbox, not the XML specification.

    An apostrophe is legal to escape and rekordbox does not escape it. Escaping
    it anyway turns ``Jackin' House`` into ``Jackin&#x27; House``, which is valid
    XML that no marker search will ever find, so the write silently misses.
    """
    assert rbxml.xml_escape_attr('A & B <x> "q"') == "A &amp; B &lt;x&gt; &quot;q&quot;"
    assert rbxml.xml_escape_attr("Jackin' House") == "Jackin' House"


def test_name_marker_uses_the_one_escaper():
    """One escaper, used by the marker builder too.

    Two escapers is how a marker stops matching the node it was built from.
    """
    assert rbxml.name_marker("Drum & Bass") == b'Name="Drum &amp; Bass"'
    assert rbxml.name_marker("Jackin' House") == b'Name="Jackin\' House"'


# ── emitters ─────────────────────────────────────────────────────────────────


def test_emitters_are_crlf_and_indented():
    """Exact bytes, including the indent widths, because splices anchor on them."""
    assert rbxml.track_key_lines([1, 2]) == (
        '            <TRACK Key="1"/>\r\n            <TRACK Key="2"/>\r\n'
    )
    assert rbxml.folder_open("X", 3, 6) == '      <NODE Name="X" Type="0" Count="3">\r\n'
    assert rbxml.playlist_open("Y", 0, 8) == (
        '        <NODE Name="Y" Type="1" KeyType="0" Entries="0">\r\n'
    )
    assert rbxml.empty_playlist("with vox", 10) == (
        '          <NODE Name="with vox" Type="1" KeyType="0" Entries="0"/>'
    )
    assert rbxml.node_close(6) == "      </NODE>\r\n"


# ── deduplication ────────────────────────────────────────────────────────────


def test_dedupe_by_exact_tid_and_norm():
    """Two identifiers can be the same track. The same track twice is a bug.

    A re-download, a different release, or a re-import gives one recording two
    track identifiers. Deduplicating on the identifier alone puts it in the
    playlist twice.
    """
    by_tid = {"1": "artist song", "2": "artist song", "3": "other tune"}
    assert rbxml.dedupe_track_ids([1, 2, 3, 3, 9], norm_by_tid=by_tid) == [1, 3, 9]


def test_dedupe_against_existing_keys_and_their_norms():
    by_tid = {"5": "artist song", "6": "artist song"}
    assert rbxml.dedupe_track_ids([5, 6, 7], existing_keys={"5"}, norm_by_tid=by_tid) == [7]


# ── splicing into a sub-playlist ─────────────────────────────────────────────


def test_splice_digit_growth_into_self_closing_sub():
    """The stale-offset corruption, reproduced.

    Ten tracks into an empty self-closing sub grows ``Entries="0"`` to
    ``Entries="10"``, one byte. The old code computed the closing tag's position
    BEFORE patching Entries, so the growth shifted the tag and the replacement
    landed past the end of the document. Under ten tracks it worked perfectly.
    """
    content = bytearray(_routing_xml())
    result = rbxml.splice_into_subplaylist(
        content, "Deep House", "High Energy", list(range(1, 11))
    )
    out = bytes(content)
    assert result.warning is None and result.inserted == 10 and result.entries_after == 10
    assert b'<NODE Name="High Energy" Type="1" KeyType="0" Entries="10">' in out
    assert out.count(b"<TRACK Key=") == 10
    assert _no_bare_lf(out)
    assert out.endswith(b"</DJ_PLAYLISTS>\r\n"), "document structure did not survive"


def test_splice_into_open_sub_dedups_existing_members():
    content = bytearray(_routing_xml())
    rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [101, 102])
    result = rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [102, 103])
    out = bytes(content)
    assert result.inserted == 1 and result.entries_after == 3
    assert out.count(b'<TRACK Key="102"/>') == 1
    assert b'Entries="3"' in out


def test_splice_create_missing_sub():
    content = bytearray(_routing_xml())
    result = rbxml.splice_into_subplaylist(
        content, "Deep House", "Low Energy", [201], create_missing=True
    )
    out = bytes(content)
    assert result.created and result.inserted == 1
    assert b'<NODE Name="Low Energy" Type="1" KeyType="0" Entries="1">' in out
    assert _no_bare_lf(out)


def test_splice_warnings_and_no_partial_writes():
    """A failed splice writes NOTHING. Not most of it, nothing.

    A partial byte splice into an XML document is not a partial success, it is a
    corrupt file. The whole document is compared, not just the target region.
    """
    base = _routing_xml()
    for genre, sub, warning in [
        ("Nope", "High Energy", "genre folder not found: Nope"),
        ("Deep House", "Nope", "sub-playlist not found: Deep House/Nope"),
    ]:
        content = bytearray(base)
        result = rbxml.splice_into_subplaylist(content, genre, sub, [1])
        assert result.warning == warning and result.inserted == 0
        assert bytes(content) == base


def test_splice_is_playlists_scoped():
    """The mis-anchor, reproduced: bait named after the folder AND the sub.

    This is the shape that made three separate splicers warn and silently drop
    the write. Scoping the search to PLAYLISTS is the fix, and this fixture is
    how it stays fixed.
    """
    content = bytearray(
        _xml_doc(
            collection=[
                '  <COLLECTION Entries="2">',
                '    <TRACK TrackID="1" Name="Deep House" Artist="Bait" '
                'Location="file://localhost/b1.flac"/>',
                '    <TRACK TrackID="2" Name="High Energy" Artist="Bait" '
                'Location="file://localhost/b2.flac"/>',
                "  </COLLECTION>",
            ],
            root_children=[
                '      <NODE Type="0" Name="BY GENRE" Count="1">',
                '        <NODE Type="0" Name="Deep House" Count="1">',
                '          <NODE Name="High Energy" Type="1" KeyType="0" Entries="0"/>',
                "        </NODE>",
                "      </NODE>",
            ],
        )
    )
    result = rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [777])
    out = bytes(content)
    assert result.warning is None and result.inserted == 1
    assert b'<NODE Name="High Energy" Type="1" KeyType="0" Entries="1">' in out
    assert out.count(b'Artist="Bait"') == 2
    assert b'b1.flac"/>' in out and b'b2.flac"/>' in out


def test_splice_empty_ids_is_noop():
    content = bytearray(_routing_xml())
    before = bytes(content)
    result = rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [])
    assert result.inserted == 0 and result.warning is None
    assert bytes(content) == before


# ── removal ──────────────────────────────────────────────────────────────────


def test_remove_tracks_decrements_entries():
    content = bytearray(_routing_xml())
    rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [1, 2, 3])
    removed, warning = rbxml.remove_tracks_from_subplaylist(
        content, "Deep House", "High Energy", [2, 99]
    )
    out = bytes(content)
    assert warning is None and removed == 1
    assert b'<TRACK Key="2"/>' not in out
    assert b'Entries="2"' in out
    assert _no_bare_lf(out)


def test_remove_tolerates_bare_lf_lines():
    """Read forgivingly, write strictly.

    Real library exports still carry bare-LF track lines written by the old buggy
    splicer. Removal has to find those, or the corruption becomes permanent. This
    is the one place a bare LF is tolerated, and only on the read side.
    """
    content = bytearray(_routing_xml())
    rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [1])
    marker = b'<TRACK Key="1"/>'
    index = content.find(marker + b"\r\n")
    del content[index + len(marker) : index + len(marker) + 1]  # drop the CR
    removed, _ = rbxml.remove_tracks_from_subplaylist(
        content, "Deep House", "High Energy", [1]
    )
    assert removed == 1
    assert marker not in bytes(content)


# ── ratings ──────────────────────────────────────────────────────────────────


def test_rating_patch_is_exact_id_match():
    """``TrackID="42"`` must not match ``TrackID="421"``.

    A prefix match here rates the wrong track, and the user has no way to tell
    which write was wrong.
    """
    content = bytearray(
        _xml_doc(
            collection=[
                '  <COLLECTION Entries="2">',
                '    <TRACK TrackID="42" Name="a" Rating="0" '
                'Location="file://localhost/a.flac"/>',
                '    <TRACK TrackID="421" Name="b" Rating="0" '
                'Location="file://localhost/b.flac"/>',
                "  </COLLECTION>",
            ],
            root_children=['      <NODE Name="INBOX" Type="0" Count="0">', "      </NODE>"],
        )
    )
    changed = rbxml.apply_rating_changes({42: 255}, content)
    out = bytes(content)
    assert changed == 1
    assert b'TrackID="42" Name="a" Rating="255"' in out
    assert b'TrackID="421" Name="b" Rating="0"' in out


# ── root-level playlists ─────────────────────────────────────────────────────


def test_insert_root_playlist_and_idempotent_replace():
    """Re-running replaces, never duplicates.

    Every workflow here is designed to be re-runnable, which means every write
    must be idempotent. A second run that appends a second copy turns "run it
    again" from the recovery procedure into a second failure.
    """
    content = bytearray(_routing_xml())
    assert rbxml.insert_root_playlist("Sets and Long Tracks", [7, 8], content) is None
    first = bytes(content)
    assert b'<NODE Name="Sets and Long Tracks" Type="1" KeyType="0" Entries="2">' in first
    assert b'        <TRACK Key="7"/>\r\n' in first
    assert _no_bare_lf(first)

    assert rbxml.insert_root_playlist("Sets and Long Tracks", [9], content) is None
    second = bytes(content)
    assert second.count(b'Name="Sets and Long Tracks"') == 1
    assert b'Entries="1">' in second and b'<TRACK Key="9"/>' in second
    assert b'<TRACK Key="7"/>' not in second
    assert _no_bare_lf(second)
    assert re.search(rb"\r\n    </NODE>\r\n  </PLAYLISTS>", second), "ROOT closed wrong"


# ── whole-folder lifecycle ───────────────────────────────────────────────────

_SUBS = ["Low", "Med", "High", "Candy", "Unsorted", "with vox"]

_DEEP_HOUSE = [
    '        <NODE Name="Deep House" Type="0" Count="1">',
    '          <NODE Name="High Energy" Type="1" KeyType="0" Entries="0"/>',
    "        </NODE>",
]


def _bge_doc(genre_folders: list[str], count: int) -> bytes:
    children = [f'      <NODE Name="BY GENRE + ENERGY" Type="0" Count="{count}">']
    children += genre_folders
    children.append("      </NODE>")
    return _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=children,
    )


def _prog_folder_lines() -> list[str]:
    lines = ['        <NODE Name="Progressive House" Type="0" Count="6">']
    lines += [
        f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="0"/>' for sub in _SUBS
    ]
    lines.append("        </NODE>")
    return lines


def test_insert_genre_folder_byte_exact():
    content = bytearray(_bge_doc(_DEEP_HOUSE, 1))
    assert rbxml.insert_genre_folder(content, "Progressive House", _SUBS) is None
    assert bytes(content) == _bge_doc(_DEEP_HOUSE + _prog_folder_lines(), 2)
    assert _no_bare_lf(bytes(content))


def test_insert_genre_folder_is_idempotent():
    content = bytearray(_bge_doc(_DEEP_HOUSE, 1))
    rbxml.insert_genre_folder(content, "Progressive House", _SUBS)
    once = bytes(content)
    assert rbxml.insert_genre_folder(content, "Progressive House", _SUBS) is None
    assert bytes(content) == once, "second call duplicated the folder or drifted Count"


def test_remove_folder_node_with_track_bearing_subs():
    """Locks the depth walk against a naive count of closing tags.

    The removed folder holds a multi-line, track-bearing sub, so the FIRST
    ``</NODE>`` after the folder's opening tag belongs to the sub, not the
    folder. Stopping there leaves a dangling close and a broken document.
    """
    nested = [
        '        <NODE Name="Progressive / Melodic" Type="0" Count="1">',
        '          <NODE Name="Med" Type="1" KeyType="0" Entries="2">',
        '            <TRACK Key="101"/>',
        '            <TRACK Key="102"/>',
        "          </NODE>",
        "        </NODE>",
    ]
    content = bytearray(_bge_doc(_DEEP_HOUSE + nested, 2))
    assert rbxml.remove_folder_node(content, "Progressive / Melodic") is None
    assert bytes(content) == _bge_doc(_DEEP_HOUSE, 1)
    assert b"Progressive / Melodic" not in bytes(content)
    assert _no_bare_lf(bytes(content))


def test_splice_into_sub_sharing_folder_name():
    """A folder holding a sub of the SAME name.

    The folder marker carries ``Count``; the sub carries ``Entries``. A splice
    that re-finds the folder marker patches the wrong attribute and drops the
    track. Common in practice, since a one-genre folder is often named after its
    only playlist.
    """
    doc = "\r\n".join(
        [
            "<DJ_PLAYLISTS>",
            "  <PLAYLISTS>",
            '    <NODE Type="0" Name="ROOT" Count="1">',
            '      <NODE Name="BY GENRE + ENERGY" Type="0" Count="1">',
            '        <NODE Name="Chill / Ambient" Type="0" Count="2">',
            '          <NODE Name="Chill / Ambient" Type="1" KeyType="0" Entries="1">',
            '            <TRACK Key="900"/>',
            "          </NODE>",
            '          <NODE Name="with vox" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
            "    </NODE>",
            "  </PLAYLISTS>",
            "</DJ_PLAYLISTS>",
        ]
    ).encode()
    content = bytearray(doc)
    result = rbxml.splice_into_subplaylist(
        content, "Chill / Ambient", "Chill / Ambient", ["901", "902"]
    )
    out = bytes(content)
    assert result.warning is None
    assert result.inserted == 2 and result.entries_after == 3
    assert b'Key="900"' in out and b'Key="901"' in out and b'Key="902"' in out
    assert b'<NODE Name="Chill / Ambient" Type="0" Count="2">' in out
    assert b'<NODE Name="Chill / Ambient" Type="1" KeyType="0" Entries="3">' in out
    assert _no_bare_lf(out)


def test_remove_folder_node_self_closed_target_does_not_wipe_siblings():
    """The data-loss guard.

    A childless folder exports SELF-CLOSED. A depth walk that assumes an opening
    tag has a matching closing tag marches on to a SIBLING's ``</NODE>`` and
    deletes everything in between. The target sits in the middle here, with a
    sibling on each side, because that is the arrangement where the bug destroys
    data rather than merely misbehaving.
    """
    children = (
        _DEEP_HOUSE
        + ['        <NODE Name="Empty Genre" Type="0" Count="0"/>']
        + [
            '        <NODE Name="Techno" Type="0" Count="1">',
            '          <NODE Name="Med" Type="1" KeyType="0" Entries="1">',
            '            <TRACK Key="201"/>',
            "          </NODE>",
            "        </NODE>",
        ]
    )
    content = bytearray(_bge_doc(children, 3))
    assert rbxml.remove_folder_node(content, "Empty Genre") is None
    out = bytes(content)
    assert b'Name="Empty Genre"' not in out
    assert b'Name="Deep House"' in out, "sibling before the target was destroyed"
    assert b'Name="Techno"' in out, "sibling after the target was destroyed"
    assert b'Key="201"' in out, "a sibling's tracks were destroyed"
    assert b'Count="2"' in out
    assert _no_bare_lf(out)


def test_remove_folder_node_absent_is_warning_noop():
    base = _bge_doc(_DEEP_HOUSE, 1)
    content = bytearray(base)
    assert rbxml.remove_folder_node(content, "Nonexistent Genre") == (
        "folder node not found: Nonexistent Genre"
    )
    assert bytes(content) == base


def test_insert_then_remove_round_trips():
    """Insert then remove returns the ORIGINAL bytes, not merely valid bytes."""
    base = _bge_doc(_DEEP_HOUSE, 1)
    content = bytearray(base)
    rbxml.insert_genre_folder(content, "Progressive House", _SUBS)
    assert bytes(content) != base
    rbxml.remove_folder_node(content, "Progressive House")
    assert bytes(content) == base


# ── location round-trip ──────────────────────────────────────────────────────


def test_location_roundtrip():
    """Percent-encoding survives a round trip, spaces and ampersands included.

    Track filenames carry apostrophes, ampersands, and spaces routinely. A
    location that does not round-trip is a track rekordbox cannot find.
    """
    from pathlib import Path

    path = "/library/Music/Processed_Tracks/2026/x/01A - 124 - It's A & B.flac"
    assert location_to_path(location_url(Path(path))) == path
    assert location_to_path("file:///library/x/a%20b.flac") == "/library/x/a b.flac"
    assert location_to_path("/plain/path.flac") == "/plain/path.flac"
