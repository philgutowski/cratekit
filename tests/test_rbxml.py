"""The rekordbox XML byte rules: CRLF, indentation, scoping, and Entries arithmetic.

Each rule was learned by breaking a real library; :mod:`cratekit.write.rbxml`
states them and why.
"""

from __future__ import annotations

import re
import unicodedata

from cratekit.core.locations import location_to_path, location_url
from cratekit.write import rbxml
from tests.xml_fixtures import _fresh_xml, _no_bare_lf, _routing_xml, _xml_doc


def _doc(root_children: list[str]) -> bytes:
    """A document with an empty collection and ``root_children`` under ROOT."""
    return _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"], root_children=root_children
    )


def test_escaper_matches_rekordbox_semantics():
    """Match rekordbox, not the XML specification: no marker search finds an escaped apostrophe."""
    assert rbxml.xml_escape_attr('A & B <x> "q"') == "A &amp; B &lt;x&gt; &quot;q&quot;"
    assert rbxml.xml_escape_attr("Jackin' House") == "Jackin' House"


def test_name_marker_uses_the_one_escaper():
    """One escaper, used by the marker builder too, or a marker stops matching."""
    assert rbxml.name_marker("Drum & Bass") == b'Name="Drum &amp; Bass"'
    assert rbxml.name_marker("Jackin' House") == b'Name="Jackin\' House"'


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


def test_dedupe_by_exact_tid_and_norm():
    """A re download, another release or a re import gives one recording two ids."""
    by_tid = {"1": "artist song", "2": "artist song", "3": "other tune"}
    assert rbxml.dedupe_track_ids([1, 2, 3, 3, 9], norm_by_tid=by_tid) == [1, 3, 9]


def test_dedupe_against_existing_keys_and_their_norms():
    by_tid = {"5": "artist song", "6": "artist song"}
    assert rbxml.dedupe_track_ids([5, 6, 7], existing_keys={"5"}, norm_by_tid=by_tid) == [7]


def test_splice_digit_growth_into_self_closing_sub():
    """Ten tracks grow ``Entries="0"`` a byte; a close position taken before the patch overran."""
    content = bytearray(_routing_xml())
    result = rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", list(range(1, 11)))
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


def test_splice_dedups_on_the_run_that_CREATES_the_sub_too():
    """The same batch, into a sub that exists and into one that does not."""
    by_tid = {"201": "artist song", "202": "artist song", "203": "other tune"}
    content = bytearray(_routing_xml())
    created = rbxml.splice_into_subplaylist(
        content,
        "Deep House",
        "Low Energy",
        [201, 201, 202, 203],
        create_missing=True,
        norm_by_tid=by_tid,
    )
    out = bytes(content)
    assert created.created and created.inserted == 2 and created.entries_after == 2
    assert out.count(b'<TRACK Key="201"/>') == 1
    assert b'<TRACK Key="202"/>' not in out, "the same recording landed under two ids"
    assert b'<NODE Name="Low Energy" Type="1" KeyType="0" Entries="2">' in out
    assert _no_bare_lf(out)

    existing = bytearray(_routing_xml())
    found = rbxml.splice_into_subplaylist(
        existing, "Deep House", "High Energy", [201, 201, 202, 203], norm_by_tid=by_tid
    )
    assert (found.inserted, found.entries_after) == (created.inserted, created.entries_after)


def test_splice_warnings_and_no_partial_writes():
    """A failed splice writes NOTHING, compared over the whole document."""
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
    """The mis-anchor: bait tracks named after the folder AND the sub."""
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
    """Read forgivingly, write strictly: a removal must also meet an old splicer's bare LF."""
    content = bytearray(_routing_xml())
    rbxml.splice_into_subplaylist(content, "Deep House", "High Energy", [1])
    marker = b'<TRACK Key="1"/>'
    index = content.find(marker + b"\r\n")
    del content[index + len(marker) : index + len(marker) + 1]  # drop the CR
    removed, _ = rbxml.remove_tracks_from_subplaylist(content, "Deep House", "High Energy", [1])
    assert removed == 1
    assert marker not in bytes(content)


def test_rating_patch_is_exact_id_match():
    """``TrackID="42"`` must not match ``TrackID="421"`` and rate the wrong track."""
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


def test_insert_root_playlist_and_idempotent_replace():
    """Re-running replaces, never duplicates, so running again stays the recovery."""
    content = bytearray(_routing_xml())
    assert rbxml.insert_root_playlist("Sets and Long Tracks", [7, 8], content) is None
    first = bytes(content)
    # A new child moves the root's count; replacing it on the second run must not.
    assert b'<NODE Type="0" Name="ROOT" Count="2">' in first
    assert b'<NODE Name="Sets and Long Tracks" Type="1" KeyType="0" Entries="2">' in first
    assert b'        <TRACK Key="7"/>\r\n' in first
    assert _no_bare_lf(first)

    assert rbxml.insert_root_playlist("Sets and Long Tracks", [9], content) is None
    second = bytes(content)
    assert second.count(b'Name="Sets and Long Tracks"') == 1
    assert b'Entries="1">' in second and b'<TRACK Key="9"/>' in second
    assert b'<TRACK Key="7"/>' not in second
    assert _no_bare_lf(second)
    assert b'<NODE Type="0" Name="ROOT" Count="2">' in second, "a replace bumped the count"
    assert re.search(rb"\r\n    </NODE>\r\n  </PLAYLISTS>", second), "ROOT closed wrong"


def test_an_intake_playlist_replaced_leaves_its_folders_count_alone():
    """A second landing of one name keeps INBOX's Count, the child count, at one."""
    content = bytearray(_fresh_xml())
    assert rbxml.insert_intake_playlist(content, "2026-11-22 batch", [7]) is None
    assert b'<NODE Name="INBOX" Type="0" Count="1">' in content
    assert rbxml.insert_intake_playlist(content, "2026-11-22 batch", [8, 9]) is None
    assert bytes(content).count(b'Name="2026-11-22 batch"') == 1
    assert b'<NODE Name="INBOX" Type="0" Count="1">' in content, "a replace bumped the count"
    assert _no_bare_lf(bytes(content))


def test_a_writer_refuses_to_replace_a_node_of_the_other_type():
    """The data loss guard on the three writers that replace or delete by name."""
    shelf = [
        '      <NODE Name="Shelf" Type="0" Count="1">',
        '        <NODE Name="Loud Room" Type="0" Count="1">',
        '          <NODE Name="Med" Type="1" KeyType="0" Entries="1">',
        '            <TRACK Key="404"/>',
        "          </NODE>",
        "        </NODE>",
        "      </NODE>",
    ]
    base = _doc(shelf)

    # A root-level playlist named after a root-level FOLDER.
    content = bytearray(base)
    warning = rbxml.insert_root_playlist("Shelf", [777], content)
    assert warning is not None and "already there" in warning
    assert bytes(content) == base, "a whole tree was replaced by a flat playlist"

    # A folder removal aimed at a PLAYLIST of that name.
    keepers = _doc([
        '      <NODE Name="Shelf" Type="0" Count="1">',
        '        <NODE Name="Keepers" Type="1" KeyType="0" Entries="1">',
        '          <TRACK Key="1"/>',
        "        </NODE>",
        "      </NODE>",
    ])
    content = bytearray(keepers)
    warning = rbxml.remove_folder_node(content, "Keepers")
    assert warning is not None and "already there" in warning
    assert bytes(content) == keepers, "a track-bearing playlist was deleted as a folder"

    # An intake playlist named after a FOLDER that already holds one.
    content = bytearray(base)
    warning = rbxml.insert_intake_playlist(content, "Loud Room", [9])
    assert warning is not None and "already there" in warning
    assert bytes(content) == base, "a folder was replaced by a flat playlist"


def test_a_node_kind_is_read_positively_and_has_a_third_answer():
    """Three answers, the third no default, so an unreadable node is never called a folder."""
    assert rbxml.node_kind(rbxml.FOLDER_TYPE) == rbxml.KIND_FOLDER
    assert rbxml.node_kind(rbxml.PLAYLIST_TYPE) == rbxml.KIND_PLAYLIST
    for unreadable in ("", " ", "2", "01", "1 ", "folder", "-1"):
        assert rbxml.node_kind(unreadable) == rbxml.KIND_UNREADABLE, unreadable


def test_a_node_whose_kind_is_unreadable_is_never_described_as_a_playlist():
    """The kind is never guessed, and the writer refuses a node of unknown kind."""
    base = _doc([
        '      <NODE Name="Shelf" Type="0" Count="1">',
        '        <NODE Name="Loud Room" Type="7" Count="0">',
        "        </NODE>",
        "      </NODE>",
    ])
    content = bytearray(base)
    warning = rbxml.insert_intake_playlist(content, "Loud Room", [9])
    assert warning is not None
    assert "node of an unreadable kind named 'Loud Room' is already there" in warning
    assert "playlist named 'Loud Room'" not in warning
    assert bytes(content) == base, "a node of an unknown kind was written into"


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
    return _doc(children)


def _prog_folder_lines() -> list[str]:
    lines = ['        <NODE Name="Progressive House" Type="0" Count="6">']
    lines += [f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="0"/>' for sub in _SUBS]
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
    """The FIRST ``</NODE>`` after the folder's open tag belongs to its multi line sub."""
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
    """A folder holding a sub of the SAME name gets ``Entries`` patched, not ``Count``."""
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
    """A childless folder exports SELF CLOSED, so siblings flank it against a runaway walk."""
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


# ── the catalog writer merges, and refuses a duplicated sibling (R-129) ─────

_LABELS = rbxml.Tree(display="Record Labels")


def _labels_doc(children: list[str]) -> bytes:
    """A document whose catalog tree holds ``children``, and its count at the label indent."""
    count = sum(1 for line in children if line.startswith("        <NODE"))
    return _doc([
        f'      <NODE Name="Record Labels" Type="0" Count="{count}">',
        *children,
        "      </NODE>",
    ])


def _catalog(content: bytes, label: str, pairs) -> tuple[bytes, str | None]:
    work = bytearray(content)
    warning = rbxml.insert_catalog_folder(work, label, pairs, tree=_LABELS)
    return bytes(work), warning


def test_a_catalog_written_twice_is_byte_identical_to_written_once():
    """R-129: a second import doubled every playlist, so the property is the merge's."""
    pairs = [("Kompakt 2025", [1, 2]), ("Kompakt 2024", [3])]
    once, warning = _catalog(_fresh_xml(), "Kompakt", pairs)
    assert warning is None
    assert once.count(rbxml.name_marker("Kompakt")) == 1
    twice, warning = _catalog(once, "Kompakt", pairs)
    assert warning is None
    assert twice == once
    thrice, _ = _catalog(twice, "Kompakt", list(reversed(pairs)))
    assert thrice == once, "the order the years arrive in wrote bytes"


def test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else():
    """One new playlist, in newest first order, and every other byte as it was."""
    once, _ = _catalog(_fresh_xml(), "Kompakt", [("Kompakt 2025", [1, 2]), ("Kompakt 2023", [5])])
    assert b'<NODE Name="Kompakt" Type="0" Count="2">' in once

    twice, warning = _catalog(
        once,
        "Kompakt",
        [("Kompakt 2025", [1, 2]), ("Kompakt 2024", [3]), ("Kompakt 2023", [5])],
    )
    assert warning is None
    block = (
        b'          <NODE Name="Kompakt 2024" Type="1" KeyType="0" Entries="1">\r\n'
        b'            <TRACK Key="3"/>\r\n'
        b"          </NODE>\r\n"
    )
    anchor = b'          <NODE Name="Kompakt 2023"'
    expected = once.replace(anchor, block + anchor).replace(
        b'<NODE Name="Kompakt" Type="0" Count="2">', b'<NODE Name="Kompakt" Type="0" Count="3">'
    )
    assert twice == expected
    assert _no_bare_lf(twice)


def test_a_new_year_lands_first_or_last_by_the_callers_order():
    """Newest first holds at both ends, not only between two held years."""
    once, _ = _catalog(_fresh_xml(), "Kompakt", [("Kompakt 2025", [1])])
    out, warning = _catalog(
        once,
        "Kompakt",
        [("Kompakt 2026", [9]), ("Kompakt 2025", [1]), ("Kompakt 2022", [4])],
    )
    assert warning is None
    at = [out.find(rbxml.name_marker(f"Kompakt {year}")) for year in (2026, 2025, 2022)]
    assert -1 not in at and at == sorted(at)
    assert b'<NODE Name="Kompakt" Type="0" Count="3">' in out


def test_a_new_year_is_placed_among_held_years_the_caller_did_not_name():
    """Holding 2025 and naming 2026 and 2024 once wrote 2025, 2026, 2024."""
    once, _ = _catalog(_fresh_xml(), "Kompakt", [("Kompakt 2025", [1])])
    out, warning = _catalog(once, "Kompakt", [("Kompakt 2026", [9]), ("Kompakt 2024", [4])])
    assert warning is None
    at = [out.find(rbxml.name_marker(f"Kompakt {year}")) for year in (2026, 2025, 2024)]
    assert -1 not in at and at == sorted(at), at


def test_track_ids_are_deduplicated_inside_a_playlist():
    """A held member, a duplicate included, stays where it was, across two pairs."""
    once, _ = _catalog(_fresh_xml(), "Kompakt", [("Kompakt 2025", [1, 1, 2])])
    assert b'Name="Kompakt 2025" Type="1" KeyType="0" Entries="2">' in once
    assert once.count(b'<TRACK Key="1"/>') == 1

    twice, warning = _catalog(
        once, "Kompakt", [("Kompakt 2025", [2, 3, 3]), ("Kompakt 2025", [1, 4])]
    )
    assert warning is None
    assert b'Name="Kompakt 2025" Type="1" KeyType="0" Entries="4">' in twice
    assert rbxml.name_marker("Kompakt 2025") in twice
    assert twice.count(rbxml.name_marker("Kompakt 2025")) == 1
    keys = re.findall(rb'<TRACK Key="(\d+)"/>', twice)
    assert keys == [b"1", b"2", b"3", b"4"]

    held = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="2">',
            '            <TRACK Key="7"/>',
            '            <TRACK Key="7"/>',
            "          </NODE>",
            "        </NODE>",
        ]
    )
    out, warning = _catalog(held, "Kompakt", [("Kompakt 2025", [7, 8])])
    assert warning is None
    assert re.findall(rb'<TRACK Key="(\d+)"/>', out) == [b"7", b"7", b"8"]
    assert b'Entries="3">' in out


def test_a_playlist_that_gains_nothing_is_left_byte_identical():
    held = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">',
            '            <TRACK Key="7"/>',
            "          </NODE>",
            "        </NODE>",
        ]
    )
    out, warning = _catalog(held, "Kompakt", [("Kompakt 2025", [7])])
    assert warning is None
    assert out == held


def test_a_similarly_named_sibling_folder_is_untouched():
    """A longer name or one differing by case is another label; both neighbours keep every byte."""
    neighbours = [
        '        <NODE Name="Kompakt Extra" Type="0" Count="1">',
        '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">',
        '            <TRACK Key="7"/>',
        "          </NODE>",
        "        </NODE>",
        '        <NODE Name="KOMPAKT" Type="0" Count="1">',
        '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">',
        '            <TRACK Key="8"/>',
        "          </NODE>",
        "        </NODE>",
    ]
    held = _labels_doc(neighbours)
    out, warning = _catalog(held, "Kompakt", [("Kompakt 2025", [1])])
    assert warning is None
    kept = "\r\n".join(neighbours).encode()
    assert kept in out, "a neighbouring folder's bytes changed"
    assert out.count(rbxml.name_marker("Kompakt")) == 1
    assert b'<NODE Name="Record Labels" Type="0" Count="3">' in out


def test_a_name_drawn_two_ways_in_unicode_is_one_folder():
    """A composed and a decomposed spelling are the same name, so they merge."""
    decomposed = unicodedata.normalize("NFD", "Café Records")
    composed = unicodedata.normalize("NFC", "Café Records")
    assert decomposed != composed
    held = _labels_doc(
        [
            f'        <NODE Name="{decomposed}" Type="0" Count="1">',
            f'          <NODE Name="{decomposed} 2025" Type="1" KeyType="0" Entries="1">',
            '            <TRACK Key="7"/>',
            "          </NODE>",
            "        </NODE>",
        ]
    )
    out, warning = _catalog(held, composed, [(f"{composed} 2025", [7, 8])])
    assert warning is None
    assert out.count(b'Type="0" Count="1">') == 2, "a second folder was written"
    assert b'Entries="2">' in out
    assert composed.encode() not in out, "the held spelling was not kept"


def test_self_closed_folder_and_playlist_are_merged_into():
    """rekordbox exports a childless node self closed, with no body to write into."""
    held = _labels_doc(['        <NODE Name="Kompakt" Type="0" Count="0"/>'])
    out, warning = _catalog(held, "Kompakt", [("Kompakt 2025", [1])])
    assert warning is None
    assert out.count(rbxml.name_marker("Kompakt")) == 1
    assert (
        b'        <NODE Name="Kompakt" Type="0" Count="1">\r\n'
        b'          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">\r\n'
        b'            <TRACK Key="1"/>\r\n'
        b"          </NODE>\r\n"
        b"        </NODE>\r\n"
    ) in out
    assert _no_bare_lf(out)

    empty = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
        ]
    )
    out, warning = _catalog(empty, "Kompakt", [("Kompakt 2025", [1])])
    assert warning is None
    assert (
        b'          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">\r\n'
        b'            <TRACK Key="1"/>\r\n'
        b"          </NODE>\r\n"
    ) in out
    assert _no_bare_lf(out)


def test_two_siblings_of_one_name_refuse_and_write_nothing():
    """The fourth answer at each level the writer reaches: merging into the first of two refuses."""
    two_folders = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="0"/>',
            '        <NODE Name="Kompakt" Type="0" Count="0"/>',
        ]
    )
    two_playlists = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="2">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="0"/>',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
        ]
    )
    two_trees = _doc([
        '      <NODE Name="Record Labels" Type="0" Count="0"/>',
        '      <NODE Name="Record Labels" Type="0" Count="0"/>',
    ])
    for document, what in (
        (two_folders, "folders named 'Kompakt'"),
        (two_playlists, "playlists named 'Kompakt 2025'"),
        (two_trees, "folders named 'Record Labels'"),
    ):
        work = bytearray(document)
        warning = rbxml.insert_catalog_folder(
            work, "Kompakt", [("Kompakt 2025", [1])], tree=_LABELS
        )
        assert warning is not None and f"2 {what}" in warning, warning
        assert bytes(work) == document, f"a refusal over two {what} wrote bytes"


def test_a_failure_after_an_earlier_merge_writes_nothing():
    """The first year merges, the second meets a folder of its name, nothing lands."""
    held = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="2">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="0"/>',
            '          <NODE Name="Kompakt 2024" Type="0" Count="0"/>',
            "        </NODE>",
        ]
    )
    work = bytearray(held)
    warning = rbxml.insert_catalog_folder(
        work, "Kompakt", [("Kompakt 2025", [1]), ("Kompakt 2024", [2])], tree=_LABELS
    )
    assert warning is not None and "a folder named 'Kompakt 2024'" in warning
    assert bytes(work) == held, "the first year's merge survived a refusal"


def test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write():
    """The R-129 payload carried a subtree twice; only the CREATING write could emit both."""
    out, warning = _catalog(
        _fresh_xml(), "Kompakt", [("Kompakt 2025", [1]), ("Kompakt 2025", [2, 1])]
    )
    assert warning is None
    assert out.count(rbxml.name_marker("Kompakt 2025")) == 1
    assert b'<NODE Name="Kompakt" Type="0" Count="1">' in out
    assert b'Name="Kompakt 2025" Type="1" KeyType="0" Entries="2">' in out
    assert re.findall(rb'<TRACK Key="(\d+)"/>', out) == [b"1", b"2"]


def test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one():
    held = _labels_doc(
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0">',
            '            <TRACK Key="7"/>',
            "          </NODE>",
            "        </NODE>",
        ]
    )
    out, warning = _catalog(held, "Kompakt", [("Kompakt 2025", [8])])
    assert warning is not None and "Entries" in warning and "'Kompakt 2025'" in warning
    assert out == held


_SHARED_LINES = {
    "folder close": (
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="0"/></NODE>',
        ],
        "the close tag of folder 'Kompakt'",
    ),
    "playlist close": (
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">',
            '          <NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">',
            '            <TRACK Key="7"/></NODE>',
            "        </NODE>",
        ],
        "the close tag of playlist 'Kompakt 2025'",
    ),
    "anchor playlist": (
        [
            '        <NODE Name="Kompakt" Type="0" Count="1">'
            '<NODE Name="Kompakt 2020" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
        ],
        "the playlist 'Kompakt 2020'",
    ),
    "folder": (
        [
            '        <NODE Name="Other" Type="0" Count="0"/>'
            '<NODE Name="Kompakt" Type="0" Count="0"/>',
        ],
        "the folder 'Kompakt'",
    ),
    "held playlist": (
        [
            '        <NODE Name="Kompakt" Type="0" Count="2">',
            '          <NODE Name="X" Type="1" KeyType="0" Entries="0"/>'
            '<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
        ],
        "the playlist 'Kompakt 2025'",
    ),
}


def test_a_merge_point_sharing_its_line_refuses_and_writes_nothing():
    """A merge beside a tag sharing its line would land inside it; each of five places driven."""
    for shape, (lines, named) in _SHARED_LINES.items():
        held = _labels_doc(lines)
        out, warning = _catalog(held, "Kompakt", [("Kompakt 2025", [1]), ("Kompakt 2024", [2])])
        assert warning is not None and named in warning, (shape, warning)
        assert "does not start its own line" in warning, (shape, warning)
        assert out == held, f"{shape}: a refusal wrote bytes"


def test_location_roundtrip():
    """Percent encoding survives a round trip, spaces and ampersands included."""
    from pathlib import Path

    path = "/library/Music/Processed_Tracks/2026/x/01A - 124 - It's A & B.flac"
    assert location_to_path(location_url(Path(path))) == path
    assert location_to_path("file:///library/x/a%20b.flac") == "/library/x/a b.flac"
    assert location_to_path("/plain/path.flac") == "/plain/path.flac"
