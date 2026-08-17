"""U20: a flipped tree refuses the XML bridge; an unflipped sibling still accepts it.

The plan's test scenarios for per-tree cutover. The emitter guard is already
proved per emitter in ``tests/test_tree_registry.py``. This file is the
coexistence claim those tests do not make: one document, two governed trees,
one flipped, and a write into the unflipped tree still lands.
"""

from __future__ import annotations

from datetime import date

import pytest

from cratekit.core import tree_registry
from cratekit.write import rbxml
from tests.test_tree_registry import (
    FOLDER_DISPLAY,
    SUB_DISPLAY,
    TREE_DISPLAY,
    TREE_ID,
    _esc,
    _invoke,
    _sub_lines,
    _tree_doc,
)
from tests.xml_fixtures import _no_bare_lf, _xml_doc

CUTOVER_ON = date(2026, 8, 1)
OTHER_ID = "second_shelf"
OTHER_DISPLAY = "Second & Shelf"
DERIVATION = tree_registry.DerivationSource.TAXONOMY


def _two_tree_doc() -> bytes:
    """One document carrying two governed trees with the same folder shape."""
    return _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            *_sub_lines(),
            "        </NODE>",
            "      </NODE>",
            f'      <NODE Name="{_esc(OTHER_DISPLAY)}" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            *_sub_lines(),
            "        </NODE>",
            "      </NODE>",
        ],
    )


def _mixed_registry() -> tree_registry.Registry:
    flipped = tree_registry.TreeRecord(
        tree_id=TREE_ID,
        mode=tree_registry.Mode.DATABASE,
        cutover_on=CUTOVER_ON,
        root_id="root-row-7788",
        source=DERIVATION,
    )
    still = tree_registry.TreeRecord(tree_id=OTHER_ID, mode=tree_registry.Mode.XML)
    return tree_registry.Registry((flipped, still)).with_record(flipped).with_record(still)


def _tree(tree_id: str, display: str, registry: tree_registry.Registry) -> rbxml.Tree:
    return rbxml.Tree(display=display, id=tree_id, registry=registry)


@pytest.mark.parametrize(
    "emitter",
    [
        "splice_into_subplaylist",
        "remove_tracks_from_subplaylist",
        "insert_genre_folder",
        "insert_empty_subplaylist",
    ],
)
def test_a_flipped_tree_refuses_the_bridge_while_its_sibling_still_accepts(emitter):
    """One document, two trees, one flip. The unflipped write has to change bytes."""
    registry = _mixed_registry()
    flipped = _tree(TREE_ID, TREE_DISPLAY, registry)
    sibling = _tree(OTHER_ID, OTHER_DISPLAY, registry)

    blocked = bytearray(_two_tree_doc())
    before = bytes(blocked)
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        _invoke(emitter, blocked, flipped)
    assert excinfo.value.tree_id == TREE_ID
    assert bytes(blocked) == before

    allowed = bytearray(_two_tree_doc())
    _invoke(emitter, allowed, sibling)
    assert bytes(allowed) != before
    assert _no_bare_lf(bytes(allowed))


def test_an_all_bridge_library_is_unchanged_by_the_coexistence_rule():
    """Until the first flip, every governed write is still a byte splice."""
    content = bytearray(_tree_doc())
    before = bytes(content)
    tree = rbxml.Tree(
        display=TREE_DISPLAY,
        id=TREE_ID,
        registry=tree_registry.EMPTY,
    )
    rbxml.splice_into_subplaylist(content, FOLDER_DISPLAY, SUB_DISPLAY, [901], tree=tree)
    assert bytes(content) != before
