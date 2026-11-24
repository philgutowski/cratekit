"""Byte exact golden characterization of every XML splice.

Nine are ported from the source system, whose five splicers Cratekit collapses
into one writer; ``NOT_PORTED`` names this product's own. **These pin CURRENT
behaviour, bugs included**: decide whether a change was intended, then
regenerate, never hand edit a ``.bytes`` file.

    REGEN=1 pytest tests/test_xml_splice_golden.py

The goldens are checked intact, then each writer is driven against its own.
"""

from __future__ import annotations

import difflib
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from cratekit.core import taxonomy, tree_registry
from cratekit.write import trees
from cratekit.write.rbxml import splice_into_subplaylist
from tests.xml_fixtures import _fresh_xml, _no_bare_lf, _routing_xml, _xml_doc

GOLDEN_DIR = Path(__file__).parent / "golden"
DECLARED = taxonomy.default_taxonomy()
REGEN = os.environ.get("REGEN") == "1"

# Every golden, the invariant it locks, and a byte marker proving it is still in
# the file; without the marker any nine well formed documents would pass.
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
        "CRLF-only routing splice with the Entries count bumped to match", b'Entries="2"'
    ),
    "sort_inbox_rating": (
        "the Rating value is patched in place and CRLF is undisturbed", b'Rating="255"'
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
        "the second copy of the rating writer, pinned so the merge is byte-checked on both sides",
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
    # Not ported: the source system had no landing step. Produced by
    # ``tests/test_landing_labels.py``, the file REGEN=1 is run over for this one.
    "land_label_tree": (
        "a landed batch whose one document carries the intake playlist and the "
        "label tree, labels A to Z and newest year first",
        b'<NODE Name="Record Labels" Type="0" Count="2">',
    ),
}


#: Goldens this product produced itself, with no source system file behind them.
#: Named, so the count of ported ones below cannot be met by one of these.
NOT_PORTED = frozenset({"land_label_tree"})

#: The two years of one label the label tree tests write.
LABEL_BUCKETS = {2025: [{"track_ids": [900000001, 900000002]}], 2024: [{"track_ids": [900000003]}]}


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
        diff = "\n".join(
            difflib.unified_diff(
                expected.decode("utf-8", "replace").splitlines(),
                produced.decode("utf-8", "replace").splitlines(),
                fromfile=f"{name}.bytes (golden)", tofile="produced", lineterm="",
            )
        )
        raise AssertionError(f"byte mismatch vs golden {name}:\n{diff}")


def _written(apply, changes: dict, xml: bytes | None = None) -> bytes:
    """``xml``, the routing fixture unless given, after ``apply`` writes ``changes`` into it."""
    content = bytearray(_routing_xml() if xml is None else xml)
    apply(changes, content)
    return bytes(content)


# Integrity half: the ported goldens are intact and still mean something.


def test_every_declared_golden_is_present_and_no_others():
    """The table and the directory agree both ways."""
    on_disk = {path.stem for path in GOLDEN_DIR.glob("*.bytes")}
    declared = set(GOLDEN_INVARIANTS)
    assert on_disk == declared, (
        f"goldens on disk but undeclared: {sorted(on_disk - declared)}; "
        f"declared but missing from disk: {sorted(declared - on_disk)}"
    )
    assert len(declared - NOT_PORTED) == 9, "the source system had nine goldens; all nine port"
    assert NOT_PORTED <= declared, "a golden named as this product's own is gone"


@pytest.mark.parametrize("name", sorted(GOLDEN_INVARIANTS))
def test_golden_is_crlf_only(name):
    """A line ending conversion in the port would damage the rule the goldens enforce."""
    data = (GOLDEN_DIR / f"{name}.bytes").read_bytes()
    assert _no_bare_lf(data), f"golden {name} carries a bare LF; it must be CRLF only"


@pytest.mark.parametrize("name", sorted(GOLDEN_INVARIANTS))
def test_golden_is_a_complete_well_formed_document(name):
    """Well formed AND terminated: the stale offset bug corrupted the TAIL."""
    data = (GOLDEN_DIR / f"{name}.bytes").read_bytes()
    ET.fromstring(data.decode("utf-8"))  # raises on malformed XML
    assert data.endswith(b"</DJ_PLAYLISTS>\r\n"), f"golden {name} is truncated"


@pytest.mark.parametrize("name", sorted(GOLDEN_INVARIANTS))
def test_golden_still_carries_the_invariant_it_documents(name):
    """The table's claim is checked against the bytes, so the golden stays reviewable."""
    description, marker = GOLDEN_INVARIANTS[name]
    assert marker in (GOLDEN_DIR / f"{name}.bytes").read_bytes(), (
        f"golden {name} no longer contains the bytes for its documented invariant "
        f"({description}); marker was {marker!r}"
    )


def test_the_fixtures_the_goldens_were_produced_from_still_build():
    """The inputs too: a golden pins nothing next to a fixture that drifted."""
    for builder in (_fresh_xml, _routing_xml):
        data = builder()
        assert _no_bare_lf(data)
        ET.fromstring(data.decode("utf-8"))
    assert b'Artist="Bait"' in _routing_xml(collision=True)


# Producer half: armed when the writers land.


def test_splice_tracks_into_subplaylist_golden():
    content = bytearray(_routing_xml())
    result = splice_into_subplaylist(content, "Deep House", "High Energy", [900000001, 900000002])
    assert result.warning is None and result.inserted == 2
    out = bytes(content)
    _check("splice_subplaylist", out)
    assert _no_bare_lf(out), "the splice must emit CRLF only"
    assert b'            <TRACK Key="900000001"/>\r\n' in out


def test_name_collision_current_behaviour():
    """The unique sub name disambiguates the collision, so a change is a behaviour shift."""
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


def test_route_into_energy_sub_golden():
    out = _written(trees.apply_playlist_changes, {("Deep House", "High Energy"): [101, 102]})
    _check("sort_inbox_route", out)
    assert _no_bare_lf(out)
    assert b'Entries="2"' in out
    assert b'            <TRACK Key="101"/>\r\n' in out


def test_entries_count_matches_tracks_actually_inserted():
    """Entries is not decorative. rekordbox trusts it over the child count."""
    out = _written(trees.apply_playlist_changes, {("Deep House", "High Energy"): [1, 2, 3]})
    assert b'Entries="3"' in out
    assert out.count(b'<TRACK Key="') == 3


def test_unplaced_existing_sub_golden():
    """That path once emitted a bare LF where every sibling emitted CRLF."""
    out = _written(trees.apply_unplaced_changes, {("Deep House", "High Energy"): [101, 102]})
    _check("sort_unplaced_existing_sub", out)
    assert b'            <TRACK Key="101"/>\r\n' in out
    assert _no_bare_lf(out)


def test_unplaced_new_sub_golden():
    out = _written(trees.apply_unplaced_changes, {("Deep House", "Low Energy"): [201]})
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


@pytest.mark.parametrize("golden", ["sort_inbox_rating", "sort_unplaced_rating"])
def test_rating_write_golden(golden):
    """The source carried two rating writers; both goldens matching proves one lost nothing."""
    out = _written(trees.apply_rating_changes, {42: 255}, _rating_fixture(42, 0))
    _check(golden, out)
    assert b'Rating="255"' in out and b'Rating="0"' not in out
    assert _no_bare_lf(out), "the rating writer must not disturb CRLF"


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


def test_add_vocal_playlists_golden():
    out, modified = trees.add_vox_playlists(_vox_fixture(), DECLARED, registry=tree_registry.EMPTY)
    assert modified == ["Deep House"]
    _check("create_vox_playlists", out)
    assert _no_bare_lf(out)
    assert b'<NODE Name="with vox" Type="1" KeyType="0" Entries="0"/>' in out


def test_add_vocal_playlists_is_idempotent():
    once, _ = trees.add_vox_playlists(_vox_fixture(), DECLARED, registry=tree_registry.EMPTY)
    twice, modified = trees.add_vox_playlists(once, DECLARED, registry=tree_registry.EMPTY)
    assert modified == []
    assert twice == once


@pytest.fixture
def fresh(tmp_path) -> Path:
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    return source


def _labelled(source: Path, out: Path) -> bytes:
    """``LABEL_BUCKETS`` written as Kompakt's label tree from ``source`` into ``out``."""
    trees.insert_record_labels_tree(
        source, "Kompakt", LABEL_BUCKETS, out, declared=DECLARED, registry=tree_registry.EMPTY
    )
    return out.read_bytes()


def test_label_subtree_golden(tmp_path, fresh):
    """The fifth duplicated splicer, and the only one that writes a whole tree."""
    out = _labelled(fresh, tmp_path / "labeled.xml")
    _check("label_library_insert", out)
    assert _no_bare_lf(out)
    assert b'<NODE Name="Record Labels" Type="0" Count="1">' in out
    assert out.find(b"Kompakt 2025") < out.find(b"Kompakt 2024"), "newest year must sort first"
    assert b'            <TRACK Key="900000001"/>\r\n' in out


def test_label_subtree_written_twice_matches_the_single_write_golden(tmp_path, fresh):
    """R-129: a second write of the same label adds nothing, against the single write's golden."""
    once = _labelled(fresh, tmp_path / "once.xml")
    twice = _labelled(tmp_path / "once.xml", tmp_path / "twice.xml")
    _check("label_library_insert", twice)
    assert twice == once
