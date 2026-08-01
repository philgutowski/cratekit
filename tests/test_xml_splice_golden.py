"""Byte-exact golden characterization of every XML splice.

A golden file pins the EXACT bytes a splicer emits against a synthetic fixture.
It is the cheapest possible answer to the question that makes an incremental
rewrite safe: did that refactor change the output, and by how much.

The nine goldens are ported unchanged, byte for byte, from the source system.
They matter more here than they did there. The source system had FIVE duplicated
splice implementations, and Cratekit collapses them into one writer. Collapsing
five implementations into one is exactly the change that produces a silent byte
difference, and a silent byte difference in this format means a playlist that
renders wrong in rekordbox, or a document tail that is quietly truncated. The
goldens turn that into a failing test with a readable diff.

**These pin CURRENT behaviour, bugs included.** A golden going red means the
bytes changed. Decide whether that change was intended, then regenerate. Never
hand-edit a ``.bytes`` file: the producing code is the source of truth, and a
hand-edited golden pins a fiction.

    REGEN=1 pytest tests/test_xml_splice_golden.py

THIS FILE HAS TWO HALVES, and the split is deliberate.

*The integrity half runs today.* It asserts the ported goldens arrived intact and
still describe the rules they were written to describe: CRLF only, well formed,
correctly terminated, and carrying the specific structure the table below names.
Porting a binary fixture is exactly the kind of step where a file gets truncated,
line-ending-converted by a helpful tool, or simply forgotten, and none of those
would be visible until the producer lands.

*The producer half is skipped until its writer lands.* Nothing is stubbed to make
it pass, and tests/test_pending_units.py fails the build the moment the writer
lands unless the skip is removed.
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from tests._pending import requires
from tests.xml_fixtures import _fresh_xml, _no_bare_lf, _routing_xml, _xml_doc

GOLDEN_DIR = Path(__file__).parent / "golden"
REGEN = os.environ.get("REGEN") == "1"

# Every golden, the invariant it locks, and a byte marker proving that invariant
# is still present in the ported file. The marker is what makes the integrity
# half meaningful: without it, "the file exists and has CRLF" would pass on any
# nine well-formed documents.
GOLDEN_INVARIANTS: dict[str, tuple[str, bytes]] = {
    "splice_subplaylist": (
        "CRLF only, 12-space TRACK indent, Entries bumped on the target sub",
        b'            <TRACK Key="900000001"/>\r\n',
    ),
    "splice_subplaylist_collision": (
        "a COLLECTION track named after the genre folder does not hijack the "
        "anchor; the bait TRACK stays self-closed and untouched",
        b'Location="file://localhost/bait.flac"/>',
    ),
    "sort_inbox_route": (
        "CRLF-only routing splice with the Entries count bumped to match",
        b'Entries="2"',
    ),
    "sort_inbox_rating": (
        "the Rating value is patched in place and CRLF is undisturbed",
        b'Rating="255"',
    ),
    "sort_unplaced_existing_sub": (
        "the existing-sub insert path emits CRLF, not the bare LF it once did",
        b'            <TRACK Key="101"/>\r\n',
    ),
    "sort_unplaced_new_sub": (
        "the sub-creation path emits CRLF and opens the new node correctly",
        b'<NODE Name="Low Energy" Type="1" KeyType="0" Entries="1">',
    ),
    "sort_unplaced_rating": (
        "the second copy of the rating writer, pinned so the merge is "
        "byte-checked on both sides",
        b'Rating="255"',
    ),
    "create_vox_playlists": (
        "CRLF only, a self-closed vocal sub-playlist node, folder Count bumped",
        b'<NODE Name="with vox" Type="1" KeyType="0" Entries="0"/>',
    ),
    "label_library_insert": (
        "CRLF label subtree, ROOT Count bumped, newest year ordered first",
        b'<NODE Name="Record Labels" Type="0" Count="1">',
    ),
}


def _check(name: str, produced: bytes) -> None:
    """Compare produced bytes to the golden, or rewrite it under REGEN=1."""
    path = GOLDEN_DIR / f"{name}.bytes"
    if REGEN:
        GOLDEN_DIR.mkdir(exist_ok=True)
        path.write_bytes(produced)
        return
    assert path.exists(), f"missing golden {path}; run REGEN=1 to create it"
    expected = path.read_bytes()
    if produced != expected:
        import difflib

        diff = "\n".join(
            difflib.unified_diff(
                expected.decode("utf-8", "replace").splitlines(),
                produced.decode("utf-8", "replace").splitlines(),
                fromfile=f"{name}.bytes (golden)",
                tofile="produced",
                lineterm="",
            )
        )
        raise AssertionError(f"byte mismatch vs golden {name}:\n{diff}")


# ═══════════════════════════════════════════════════════════════════════════
# Integrity half: the ported goldens are intact and still mean something.
# ═══════════════════════════════════════════════════════════════════════════


def test_every_declared_golden_is_present_and_no_others():
    """The table and the directory agree, in both directions.

    One direction catches a golden that failed to copy. The other catches a
    golden that was added without documenting what it locks, which is how a
    golden file becomes a byte blob nobody dares change.
    """
    on_disk = {path.stem for path in GOLDEN_DIR.glob("*.bytes")}
    declared = set(GOLDEN_INVARIANTS)
    assert on_disk == declared, (
        f"goldens on disk but undeclared: {sorted(on_disk - declared)}; "
        f"declared but missing from disk: {sorted(declared - on_disk)}"
    )
    assert len(declared) == 9, "the source system had nine goldens; all nine port"


@pytest.mark.parametrize("name", sorted(GOLDEN_INVARIANTS))
def test_golden_is_crlf_only(name):
    """A line-ending conversion during the port would be invisible otherwise.

    Copying a binary fixture through a tool that thinks it is text is the single
    most likely way these files get damaged, and the damage is exactly the rule
    they exist to enforce.
    """
    data = (GOLDEN_DIR / f"{name}.bytes").read_bytes()
    assert _no_bare_lf(data), f"golden {name} carries a bare LF; it must be CRLF only"


@pytest.mark.parametrize("name", sorted(GOLDEN_INVARIANTS))
def test_golden_is_a_complete_well_formed_document(name):
    """Well formed AND correctly terminated.

    The termination check is not redundant with parsing. The stale-offset bug
    these goldens were written for corrupted the document TAIL, and a truncated
    tail is the shape that most needs catching.
    """
    data = (GOLDEN_DIR / f"{name}.bytes").read_bytes()
    ET.fromstring(data.decode("utf-8"))  # raises on malformed XML
    assert data.endswith(b"</DJ_PLAYLISTS>\r\n"), f"golden {name} is truncated"


@pytest.mark.parametrize("name", sorted(GOLDEN_INVARIANTS))
def test_golden_still_carries_the_invariant_it_documents(name):
    """The table's claim is checked against the bytes, not trusted.

    Without this, the documentation and the fixture drift apart and the golden
    becomes an opaque blob that nobody can review a diff against.
    """
    description, marker = GOLDEN_INVARIANTS[name]
    data = (GOLDEN_DIR / f"{name}.bytes").read_bytes()
    assert marker in data, (
        f"golden {name} no longer contains the bytes for its documented invariant "
        f"({description}); marker was {marker!r}"
    )


def test_the_fixtures_the_goldens_were_produced_from_still_build():
    """The inputs, not just the outputs.

    A golden is only meaningful next to the fixture that produced it. If the
    fixture builder drifts, the golden pins the output of an input nobody has.
    """
    for builder in (_fresh_xml, _routing_xml):
        data = builder()
        assert _no_bare_lf(data)
        ET.fromstring(data.decode("utf-8"))
    assert b'Artist="Bait"' in _routing_xml(collision=True)


# ═══════════════════════════════════════════════════════════════════════════
# Producer half: armed when the writers land.
# ═══════════════════════════════════════════════════════════════════════════


@requires("cratekit.write.rbxml")
def test_splice_tracks_into_subplaylist_golden():
    from cratekit.write.rbxml import splice_into_subplaylist

    content = bytearray(_routing_xml())
    result = splice_into_subplaylist(
        content, "Deep House", "High Energy", [900000001, 900000002]
    )
    assert result.warning is None and result.inserted == 2
    out = bytes(content)
    _check("splice_subplaylist", out)
    assert _no_bare_lf(out), "the splice must emit CRLF only"
    assert b'            <TRACK Key="900000001"/>\r\n' in out


@requires("cratekit.write.rbxml")
def test_name_collision_current_behaviour():
    """Characterizes the collision case so the scoped fix yields a reviewed diff.

    The unique sub name re-disambiguates the anchor here, so this specific
    collision is survived even by an unscoped search. Pinned anyway: the scoped
    implementation should preserve these exact bytes, and a change flags a
    behaviour shift rather than a bug fix.
    """
    from cratekit.write.rbxml import splice_into_subplaylist

    content = bytearray(_routing_xml(collision=True))
    result = splice_into_subplaylist(content, "Deep House", "High Energy", [900000001])
    out = bytes(content)
    _check("splice_subplaylist_collision", out)
    assert _no_bare_lf(out)
    assert result.warning is None and result.inserted == 1
    assert b'<NODE Name="High Energy" Type="1" KeyType="0" Entries="1">' in out
    assert (
        b'<TRACK TrackID="1" Name="Deep House" Artist="Bait" '
        b'Location="file://localhost/bait.flac"/>'
    ) in out


@requires("cratekit.write.trees")
def test_route_into_energy_sub_golden():
    from cratekit.write import trees

    content = bytearray(_routing_xml())
    trees.apply_playlist_changes({("Deep House", "High Energy"): [101, 102]}, content)
    out = bytes(content)
    _check("sort_inbox_route", out)
    assert _no_bare_lf(out)
    assert b'Entries="2"' in out
    assert b'            <TRACK Key="101"/>\r\n' in out


@requires("cratekit.write.trees")
def test_entries_count_matches_tracks_actually_inserted():
    """Entries is not decorative. rekordbox trusts it over the child count."""
    from cratekit.write import trees

    content = bytearray(_routing_xml())
    trees.apply_playlist_changes({("Deep House", "High Energy"): [1, 2, 3]}, content)
    out = bytes(content)
    assert b'Entries="3"' in out
    assert out.count(b'<TRACK Key="') == 3


@requires("cratekit.write.trees")
def test_unplaced_existing_sub_golden():
    """The regression guard for the bare-LF insert.

    The existing-sub path once emitted a bare LF while every sibling path emitted
    CRLF, which is how the bug survived: the common path was correct.
    """
    from cratekit.write import trees

    content = bytearray(_routing_xml())
    trees.apply_unplaced_changes({("Deep House", "High Energy"): [101, 102]}, content)
    out = bytes(content)
    _check("sort_unplaced_existing_sub", out)
    assert b'            <TRACK Key="101"/>\r\n' in out
    assert _no_bare_lf(out)


@requires("cratekit.write.trees")
def test_unplaced_new_sub_golden():
    from cratekit.write import trees

    content = bytearray(_routing_xml())
    trees.apply_unplaced_changes({("Deep House", "Low Energy"): [201]}, content)
    out = bytes(content)
    _check("sort_unplaced_new_sub", out)
    assert b'<NODE Name="Low Energy" Type="1" KeyType="0" Entries="1">' in out
    assert b'            <TRACK Key="201"/>\r\n' in out
    assert _no_bare_lf(out)


def _rating_fixture(track_id: int, rating: int) -> bytes:
    return _xml_doc(
        collection=[
            '  <COLLECTION Entries="1">',
            f'    <TRACK TrackID="{track_id}" Name="x" Rating="{rating}" '
            'Location="file://localhost/x.flac"/>',
            "  </COLLECTION>",
        ],
        root_children=['      <NODE Name="INBOX" Type="0" Count="0">', "      </NODE>"],
    )


@requires("cratekit.write.trees")
def test_rating_write_golden():
    from cratekit.write import trees

    content = bytearray(_rating_fixture(42, 0))
    trees.apply_rating_changes({42: 255}, content)
    out = bytes(content)
    _check("sort_inbox_rating", out)
    assert b'Rating="255"' in out and b'Rating="0"' not in out
    assert _no_bare_lf(out), "the rating writer must not disturb CRLF"


@requires("cratekit.write.trees")
def test_second_rating_writer_golden():
    """The source system carried TWO copies of the rating writer.

    Both are pinned so the consolidation is byte-checked from both sides. When
    one writer replaces both, these two goldens must both still match, which is
    what proves the merge lost nothing.
    """
    from cratekit.write import trees

    content = bytearray(_rating_fixture(42, 0))
    trees.apply_rating_changes({42: 255}, content)
    out = bytes(content)
    _check("sort_unplaced_rating", out)
    assert b'Rating="255"' in out and b'Rating="0"' not in out


def _vox_fixture() -> bytes:
    return _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            '      <NODE Name="BY GENRE + ENERGY" Type="0" Count="1">',
            '        <NODE Name="Deep House" Type="0" Count="1">',
            '          <NODE Name="High Energy" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
        ],
    )


@requires("cratekit.write.trees")
def test_add_vocal_playlists_golden():
    from cratekit.write.trees import add_vox_playlists

    out, modified = add_vox_playlists(_vox_fixture())
    assert modified == ["Deep House"]
    _check("create_vox_playlists", out)
    assert _no_bare_lf(out)
    assert b'<NODE Name="with vox" Type="1" KeyType="0" Entries="0"/>' in out


@requires("cratekit.write.trees")
def test_add_vocal_playlists_is_idempotent():
    from cratekit.write.trees import add_vox_playlists

    once, _ = add_vox_playlists(_vox_fixture())
    twice, modified = add_vox_playlists(once)
    assert modified == []
    assert twice == once


@requires("cratekit.write.trees")
def test_label_subtree_golden(tmp_path):
    """The fifth duplicated splicer, and the only one that writes a whole tree."""
    from cratekit.write import trees

    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    out_path = tmp_path / "labeled.xml"
    buckets = {
        2025: [{"track_ids": [900000001, 900000002]}],
        2024: [{"track_ids": [900000003]}],
    }
    trees.insert_record_labels_tree(source, "Kompakt", buckets, out_path)
    out = out_path.read_bytes()
    _check("label_library_insert", out)
    assert _no_bare_lf(out)
    assert b'<NODE Name="Record Labels" Type="0" Count="1">' in out
    assert out.find(b"Kompakt 2025") < out.find(b"Kompakt 2024"), "newest year must sort first"
    assert b'            <TRACK Key="900000001"/>\r\n' in out
