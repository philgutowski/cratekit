"""U18: the tree writers, in both mediums, and the row matching between them.

The nine goldens in tests/test_xml_splice_golden.py pin every bridge writer's
bytes; this file covers the paths no golden was produced for and the whole
database half. The plan's five scenarios: a second pass adds nothing
(``test_a_second_pass_adds_nothing``), it adopts the folder the first made
(``test_a_second_pass_adopts_the_folder_the_first_pass_made``), normalization
resolves a prefixed path, a composition-form mismatch and a device-relative
row (the ``test_normalization_*`` cases), two active rows on one location are
skipped and surfaced, and a tree still on the bridge refuses
(``test_a_database_write_at_a_tree_still_on_the_bridge_is_refused``).

The database half runs against a real database, since the joints (adoption by
name, idempotence through the binding, the session spine) are where
correct-looking code guards nothing. D1: every name is synthetic, carrying a
space and an accented character in both composition forms.
"""

from __future__ import annotations

import unicodedata
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import locations, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rbxml, trees
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.xml_fixtures import _fresh_xml, _no_bare_lf, _xml_doc

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"
FOLDER_DISPLAY = "Loud! Room"
SUB_DISPLAY = "Café Nights"
OTHER_FOLDER = "Quiet? Corner"
CATALOG_DISPLAY = "Catalogued Sources"
ADOPTED_ROOT = "root-row-7788"

DECLARED = taxonomy.default_taxonomy()



def _esc(value: str) -> str:
    return rbxml.xml_escape_attr(value)


def _tree_doc(*, folders: tuple[str, ...] = (FOLDER_DISPLAY,)) -> bytes:
    """One tree holding one empty sub-playlist per named folder."""
    children: list[str] = [f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">']
    for folder in folders:
        children += [
            f'        <NODE Name="{_esc(folder)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
        ]
    children.append("      </NODE>")
    return _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"], root_children=children
    )


def _ungoverned() -> rbxml.Tree:
    return rbxml.Tree(display=TREE_DISPLAY)


def _registry(mode: tree_registry.Mode, *, root_id: str | None = ADOPTED_ROOT):
    if mode is tree_registry.Mode.DATABASE:
        return tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=TREE_ID,
                    mode=mode,
                    cutover_on=date(2026, 8, 1),
                    root_id=root_id,
                    source=tree_registry.DerivationSource.TAXONOMY,
                ),
            )
        )
    return tree_registry.Registry((tree_registry.TreeRecord(tree_id=TREE_ID, mode=mode),))


# ═══════════════════════════════════════════════════════════════════════════
# The bridge half: the paths no golden was produced for
# ═══════════════════════════════════════════════════════════════════════════


def test_a_routing_sweep_reports_what_it_could_not_place_rather_than_raising():
    """One absent folder is a fact to carry to the end, not a reason to stop."""
    content = bytearray(_tree_doc())
    report = trees.apply_playlist_changes(
        {(FOLDER_DISPLAY, SUB_DISPLAY): [1, 2], (OTHER_FOLDER, SUB_DISPLAY): [3]},
        content,
        tree=_ungoverned(),
    )
    assert report.inserted == 2
    assert len(report.warnings) == 1 and OTHER_FOLDER in report.warnings[0]
    assert _no_bare_lf(bytes(content))


def test_the_creating_sweep_creates_and_the_placing_sweep_refuses_to():
    """The one difference between the two entry points, asserted from both sides."""
    placing = bytearray(_tree_doc())
    placed = trees.apply_playlist_changes(
        {(FOLDER_DISPLAY, "Not There Yet"): [7]}, placing, tree=_ungoverned()
    )
    assert placed.inserted == 0 and placed.created == () and placed.warnings

    creating = bytearray(_tree_doc())
    made = trees.apply_unplaced_changes(
        {(FOLDER_DISPLAY, "Not There Yet"): [7]}, creating, tree=_ungoverned()
    )
    assert made.inserted == 1
    assert made.created == (f"{FOLDER_DISPLAY}/Not There Yet",)
    assert b'<TRACK Key="7"/>' in bytes(creating)
    assert _no_bare_lf(bytes(creating))


def test_a_sweep_with_nothing_to_place_writes_nothing():
    """An empty plan entry is skipped rather than emitted as an empty playlist."""
    content = bytearray(_tree_doc())
    before = bytes(content)
    report = trees.apply_unplaced_changes(
        {(FOLDER_DISPLAY, "Not There Yet"): []}, content, tree=_ungoverned()
    )
    assert report.inserted == 0 and bytes(content) == before


def test_the_sweep_order_does_not_depend_on_the_callers_dict_order():
    """A golden compares BYTES, so the byte output cannot depend on insertion order."""
    first = bytearray(_tree_doc(folders=(FOLDER_DISPLAY, OTHER_FOLDER)))
    trees.apply_playlist_changes(
        {(FOLDER_DISPLAY, SUB_DISPLAY): [1], (OTHER_FOLDER, SUB_DISPLAY): [2]},
        first,
        tree=_ungoverned(),
    )
    second = bytearray(_tree_doc(folders=(FOLDER_DISPLAY, OTHER_FOLDER)))
    trees.apply_playlist_changes(
        {(OTHER_FOLDER, SUB_DISPLAY): [2], (FOLDER_DISPLAY, SUB_DISPLAY): [1]},
        second,
        tree=_ungoverned(),
    )
    assert bytes(first) == bytes(second)


def test_a_bridge_sweep_at_a_database_native_tree_is_refused_by_name():
    """The bridge guard reaches the sweep through the emitter, not around it."""
    governed = rbxml.Tree(
        display=TREE_DISPLAY, id=TREE_ID, registry=_registry(tree_registry.Mode.DATABASE)
    )
    content = bytearray(_tree_doc())
    before = bytes(content)
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        trees.apply_playlist_changes(
            {(FOLDER_DISPLAY, SUB_DISPLAY): [1]}, content, tree=governed
        )
    assert excinfo.value.tree_id == TREE_ID
    assert bytes(content) == before


def test_the_default_tree_is_governed_so_a_cutover_refuses_the_sweep():
    """The hole a reviewer walked through, pinned from the entry point that had it."""
    declared = taxonomy.default_taxonomy()
    document = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(declared.tree.display)}" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
        ],
    )
    native = tree_registry.Registry(
        (
            tree_registry.TreeRecord(
                tree_id=declared.tree.id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id=ADOPTED_ROOT,
                source=tree_registry.DerivationSource.TAXONOMY,
            ),
        )
    )
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        trees.add_vox_playlists(document, DECLARED, registry=native)
    assert excinfo.value.tree_id == declared.tree.id

    # And the same registry with the tree still on the bridge lets it through,
    # or the assertion above would also hold for a writer that refused always.
    out, report = trees.add_vox_playlists(document, DECLARED, registry=tree_registry.EMPTY)
    assert report.modified == (FOLDER_DISPLAY,)
    assert out != document


def test_a_sweep_naming_neither_a_registry_nor_a_tree_refuses_to_guess():
    """There is no ungoverned default, which is the property, not the message."""
    with pytest.raises(ValueError, match="registry"):
        trees.add_vox_playlists(_tree_doc(), DECLARED)


def test_a_catalog_import_naming_neither_a_registry_nor_a_tree_refuses(tmp_path):
    """The catalog entry point's half of the same property."""
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    with pytest.raises(ValueError, match="registry"):
        trees.insert_record_labels_tree(
            source, "Kompakt", _buckets(2025), tmp_path / "out.xml", declared=DECLARED
        )
    assert not (tmp_path / "out.xml").exists()


def test_a_catalog_tree_is_not_written_outside_a_self_closed_playlist_root(tmp_path):
    """rekordbox exports a childless node self closed, and it has no body to write into."""
    document = (
        '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        '<DJ_PLAYLISTS Version="1.0.0">\r\n'
        '  <COLLECTION Entries="0">\r\n  </COLLECTION>\r\n'
        "  <PLAYLISTS>\r\n"
        '    <NODE Type="0" Name="ROOT" Count="0"/>\r\n'
        "  </PLAYLISTS>\r\n</DJ_PLAYLISTS>\r\n"
    ).encode()
    content = bytearray(document)
    warning = rbxml.insert_catalog_folder(
        content, "Kompakt", [("Kompakt 2025", [1])], tree=rbxml.Tree(display=CATALOG_DISPLAY)
    )
    assert warning is not None
    assert bytes(content) == document, "a refusal wrote bytes"


def test_the_vocal_sweep_writes_the_direct_child_not_a_nested_namesake():
    """The enumeration and the write have to mean the same folder."""
    document = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="2">',
            f'        <NODE Name="{_esc(OTHER_FOLDER)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="0">',
            "          </NODE>",
            "        </NODE>",
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
        ],
    )
    out, report = trees.add_vox_playlists(document, DECLARED, tree=_ungoverned())
    vox = taxonomy.default_taxonomy().sub_class(trees.VOX_SUB_CLASS).display

    # Both direct children gain one; the nested namesake, never enumerated, must not.
    root = rbxml.root_node(out)
    tree_node = rbxml.direct_child(out, root, TREE_DISPLAY, rbxml.FOLDER_TYPE)
    outer = rbxml.direct_child(out, tree_node, OTHER_FOLDER, rbxml.FOLDER_TYPE)
    nested = rbxml.direct_child(out, outer, FOLDER_DISPLAY, rbxml.FOLDER_TYPE)
    target = rbxml.direct_child(out, tree_node, FOLDER_DISPLAY, rbxml.FOLDER_TYPE)

    assert rbxml.name_marker(vox) in out[target.tag_start : target.close_end], (
        "the tree's own child did not get the vocal playlist"
    )
    assert rbxml.name_marker(vox) not in out[nested.tag_start : nested.close_end], (
        "the nested namesake took a write meant for the tree's direct child"
    )
    assert out.count(rbxml.name_marker(vox)) == 2, "one per direct folder child"
    assert report.modified == (OTHER_FOLDER, FOLDER_DISPLAY)


def test_the_vocal_sweep_carries_out_a_warning_instead_of_dropping_it():
    """A folder it could not serve and a folder that needed nothing are not one fact."""
    document = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            # A FOLDER standing where the vocal PLAYLIST would go. The emitter
            # refuses to replace one node type with the other, because doing so
            # deletes everything the existing node holds.
            '          <NODE Name="with vox" Type="0" Count="0">',
            "          </NODE>",
            "        </NODE>",
            "      </NODE>",
        ],
    )
    before = bytes(document)
    out, report = trees.add_vox_playlists(document, DECLARED, tree=_ungoverned())
    assert report.modified == ()
    assert len(report.warnings) == 1
    assert "with vox" in report.warnings[0]
    assert out == before, "a warned folder must not be written"


def test_two_folders_of_one_name_are_refused_rather_than_half_served():
    """A name-targeted writer cannot tell them apart, so it must not try."""
    raw = _tree_doc(folders=(FOLDER_DISPLAY, FOLDER_DISPLAY))
    with pytest.raises(trees.DuplicateFolders) as excinfo:
        trees.add_vox_playlists(raw, DECLARED, tree=_ungoverned())
    assert FOLDER_DISPLAY in str(excinfo.value)


def test_a_playlist_wearing_the_trees_name_refuses_rather_than_walking_nothing():
    """The wrong-type collision, which "not found" would have hidden."""
    document = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
        ],
    )
    with pytest.raises(trees.TreeUnreachable) as excinfo:
        trees.add_vox_playlists(document, DECLARED, tree=_ungoverned())
    assert "playlist" in str(excinfo.value)


def test_a_sweep_over_a_document_with_no_such_tree_refuses(tmp_path):
    """The other half. An absent tree is a mistake, not a quiet no-op."""
    with pytest.raises(trees.TreeUnreachable):
        trees.add_vox_playlists(_fresh_xml(), DECLARED, tree=_ungoverned())


def test_the_vocal_sweep_touches_only_the_folders_that_lack_the_playlist():
    """Idempotence per FOLDER, not per document."""
    declared = taxonomy.default_taxonomy()
    vox = declared.sub_class(trees.VOX_SUB_CLASS).display

    once, modified = trees.add_vox_playlists(_tree_doc(), DECLARED, tree=_ungoverned())
    assert modified == [FOLDER_DISPLAY]
    assert once.count(rbxml.name_marker(vox)) == 1

    grown = _tree_doc(folders=(FOLDER_DISPLAY, OTHER_FOLDER))
    seeded, _ = trees.add_vox_playlists(grown, DECLARED, tree=_ungoverned())
    again, modified_again = trees.add_vox_playlists(seeded, DECLARED, tree=_ungoverned())
    assert modified_again == []
    assert again == seeded
    assert again.count(rbxml.name_marker(vox)) == 2
    assert _no_bare_lf(again)


def test_copying_a_taxonomy_for_a_test_keeps_its_derived_indexes():
    """The trap the two tests below would otherwise fall into, pinned here."""
    declared = taxonomy.default_taxonomy()
    copied = replace(declared, catalog=None)
    assert copied.catalog is None
    bucket_id = declared.buckets[0].id
    assert copied.bucket(bucket_id) == declared.bucket(bucket_id)


def test_the_vocal_sweep_reads_both_names_from_the_declared_taxonomy():
    """R19 in its live form: rename either name and the sweep follows."""
    declared = taxonomy.default_taxonomy()
    renamed = tuple(
        entry if entry.id != trees.VOX_SUB_CLASS else replace(entry, display="Sung")
        for entry in declared.sub_classes
    )
    out, modified = trees.add_vox_playlists(
        _tree_doc(), replace(declared, sub_classes=renamed), tree=_ungoverned()
    )
    assert modified == [FOLDER_DISPLAY]
    assert rbxml.name_marker("Sung") in out
    assert (
        rbxml.name_marker(declared.sub_class(trees.VOX_SUB_CLASS).display) not in out
    )


def _buckets(*years: int) -> dict:
    return {year: [{"track_ids": [year * 10 + 1, year * 10 + 2]}] for year in years}


def test_a_catalog_rerun_refreshes_the_folder_rather_than_duplicating_it(tmp_path):
    """The source system's second run grew a second copy of the whole label."""
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    first = tmp_path / "one.xml"
    trees.insert_record_labels_tree(
        source, "Kompakt", _buckets(2025), first, declared=DECLARED, tree=rbxml.Tree(display=CATALOG_DISPLAY)
    )
    second = tmp_path / "two.xml"
    trees.insert_record_labels_tree(
        first, "Kompakt", _buckets(2025, 2024), second, declared=DECLARED, tree=rbxml.Tree(display=CATALOG_DISPLAY)
    )

    out = second.read_bytes()
    assert out.count(rbxml.name_marker("Kompakt")) == 1, "the folder was duplicated"
    assert out.count(rbxml.name_marker(CATALOG_DISPLAY)) == 1
    assert rbxml.name_marker("Kompakt 2024") in out
    assert b'<NODE Name="' + CATALOG_DISPLAY.encode() + b'" Type="0" Count="1">' in out
    assert _no_bare_lf(out)


def test_a_catalog_write_into_a_taxonomy_declaring_no_catalog_tree_refuses_by_name(tmp_path):
    """A default nobody saw would put a folder in somebody's library by surprise."""
    declared = taxonomy.default_taxonomy()
    without = replace(declared, catalog=None)
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    with pytest.raises(CratekitError) as excinfo:
        trees.insert_record_labels_tree(
            source, "Kompakt", _buckets(2025), tmp_path / "out.xml", declared=without
        )
    assert excinfo.value.cause.reason == "catalog-tree-undeclared"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_PREREQUISITE
    assert not (tmp_path / "out.xml").exists(), "a refusal left a document behind"


def test_a_catalog_write_that_cannot_place_its_folder_writes_no_document(tmp_path):
    """A refusal that still produced an output file is a refusal a user imports."""
    source = tmp_path / "notxml.xml"
    source.write_bytes(b"<DJ_PLAYLISTS></DJ_PLAYLISTS>\r\n")
    with pytest.raises(CratekitError):
        trees.insert_record_labels_tree(
            source,
            "Kompakt",
            _buckets(2025),
            tmp_path / "out.xml", declared=DECLARED,
            tree=rbxml.Tree(display=CATALOG_DISPLAY),
        )
    assert not (tmp_path / "out.xml").exists()


def test_the_catalog_check_refuses_what_the_writer_would_and_writes_nothing():
    """U77: the landing engine asks before it moves a file, so the check has to
    refuse exactly where the writer does."""
    without = replace(taxonomy.default_taxonomy(), catalog=None)
    raw = _fresh_xml()
    with pytest.raises(CratekitError) as excinfo:
        trees.check_record_labels_tree(raw, {"Kompakt": [2025]}, declared=without)
    assert excinfo.value.cause.reason == "catalog-tree-undeclared"

    with pytest.raises(CratekitError) as excinfo:
        trees.check_record_labels_tree(
            b"<DJ_PLAYLISTS></DJ_PLAYLISTS>\r\n",
            {"Kompakt": [2025]}, declared=DECLARED,
            tree=rbxml.Tree(display=CATALOG_DISPLAY),
        )
    assert "Kompakt" in excinfo.value.cause.message


def test_the_catalog_check_asks_nothing_when_there_is_nothing_to_write():
    """An undeclared tree costs a caller with no catalogued source nothing."""
    without = replace(taxonomy.default_taxonomy(), catalog=None)
    trees.check_record_labels_tree(_fresh_xml(), {}, declared=without)


def test_the_catalog_check_passes_a_document_the_writer_can_write_and_leaves_it_alone():
    raw = _fresh_xml()
    trees.check_record_labels_tree(
        raw, {"Kompakt": [2025, 2024], "Ostgut Ton": [2025]}, declared=DECLARED, registry=tree_registry.EMPTY
    )
    assert raw == _fresh_xml()


def test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice(tmp_path):
    """The deepest of the three levels the writer refuses at, reached only when
    the check names the YEAR and not the label alone."""
    once = tmp_path / "once.xml"
    once.write_bytes(_fresh_xml())
    trees.insert_record_labels_tree(
        once, "Kompakt", _buckets(2025), once, declared=DECLARED, registry=tree_registry.EMPTY
    )
    body = once.read_bytes()
    start = body.index(b'<NODE Name="Kompakt 2025"')
    start = body.rindex(b"\r\n", 0, start) + 2
    close = b"</NODE>\r\n"
    end = body.index(close, start) + len(close)
    doubled = body.replace(body[start:end], body[start:end] * 2, 1)

    trees.check_record_labels_tree(doubled, {"Kompakt": [2024]}, declared=DECLARED, registry=tree_registry.EMPTY)
    with pytest.raises(CratekitError):
        trees.check_record_labels_tree(
            doubled, {"Kompakt": [2025]}, declared=DECLARED, registry=tree_registry.EMPTY
        )


def test_several_sources_are_one_write_and_a_new_tree_reads_a_to_z(tmp_path):
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    out = tmp_path / "out.xml"
    catalog = {"Ostgut Ton": _buckets(2025), "Kompakt": _buckets(2025, 2024)}

    trees.insert_record_labels_trees(source, catalog, out, declared=DECLARED, registry=tree_registry.EMPTY)

    body = out.read_bytes()
    assert _no_bare_lf(body)
    assert body.count(b'<NODE Name="Record Labels" Type="0" Count="2">') == 1
    assert body.find(b'Name="Kompakt"') < body.find(b'Name="Ostgut Ton"')
    # The same bytes the one source writer gives, written last name first.
    step = tmp_path / "step.xml"
    trees.insert_record_labels_tree(
        source, "Ostgut Ton", catalog["Ostgut Ton"], step, declared=DECLARED, registry=tree_registry.EMPTY
    )
    trees.insert_record_labels_tree(
        step, "Kompakt", catalog["Kompakt"], step, declared=DECLARED, registry=tree_registry.EMPTY
    )
    assert step.read_bytes() == body


def test_one_source_the_writer_refuses_writes_none_of_them(tmp_path):
    """All or nothing. A document holding one label of two would import as a
    finished one."""
    once = tmp_path / "once.xml"
    once.write_bytes(_fresh_xml())
    trees.insert_record_labels_tree(
        once, "Kompakt", _buckets(2025), once, declared=DECLARED, registry=tree_registry.EMPTY
    )
    body = once.read_bytes()
    opened = b'<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="2">'
    assert body.count(opened) == 1
    once.write_bytes(body.replace(opened, b'<NODE Name="Kompakt 2025" Type="1" KeyType="0">'))
    out = tmp_path / "out.xml"

    with pytest.raises(CratekitError):
        trees.insert_record_labels_trees(
            once,
            {"Ostgut Ton": _buckets(2025), "Kompakt": {2025: [{"track_ids": [7]}]}},
            out, declared=DECLARED,
            registry=tree_registry.EMPTY,
        )

    assert not out.exists()


def test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend(tmp_path):
    """The trial gives every year one id no document holds. With none, the
    writer returns before it looks at the held playlist's own layout, and the
    check passed a document the write then refused."""
    once = tmp_path / "once.xml"
    once.write_bytes(_fresh_xml())
    trees.insert_record_labels_tree(
        once, "Kompakt", _buckets(2025), once, declared=DECLARED, registry=tree_registry.EMPTY
    )
    body = once.read_bytes()
    opened = b'<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="2">'
    assert body.count(opened) == 1
    broken = body.replace(opened, b'<NODE Name="Kompakt 2025" Type="1" KeyType="0">')

    with pytest.raises(CratekitError) as excinfo:
        trees.check_record_labels_tree(broken, {"Kompakt": [2025]}, declared=DECLARED, registry=tree_registry.EMPTY)

    assert "Entries" in excinfo.value.cause.message
    # And the trial id is left in nothing: the check writes to a copy only.
    trees.check_record_labels_tree(body, {"Kompakt": [2025]}, declared=DECLARED, registry=tree_registry.EMPTY)
    assert b'Key="-1"' not in body


# ═══════════════════════════════════════════════════════════════════════════
# Row matching: the active-row rule and the two-sided normalization
# ═══════════════════════════════════════════════════════════════════════════

#: A synthetic library root and a synthetic older volume name, so the prefix map
#: has something anchored to rewrite that names nobody's actual disk.
ROOT = "/synthetic/current"
OLDER = "/synthetic/older"

#: One filename in both composition forms. macOS hands back one and rekordbox
#: recorded the other, which is the pair that cost the source system 144 files.
NFC_NAME = unicodedata.normalize("NFC", "Café.flac")
NFD_NAME = unicodedata.normalize("NFD", "Café.flac")


def _rules() -> list[locations.PrefixRule]:
    return [locations.PrefixRule(OLDER, ROOT)]


def test_normalization_resolves_a_prefixed_path_to_the_right_row():
    """Most active rows in a real library record a volume name it no longer uses."""
    rows = [trees.ContentRow("41", f"{OLDER}/Music/a.flac", deleted=False)]
    (match,) = trees.match_active_rows(
        [f"{ROOT}/Music/a.flac"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.MATCHED
    assert match.content_id == "41"


def test_normalization_resolves_a_composition_form_mismatch():
    """Both sides go through the normalizer, or neither side is comparable."""
    rows = [trees.ContentRow("42", f"{ROOT}/Music/{NFD_NAME}", deleted=False)]
    (match,) = trees.match_active_rows(
        [f"{ROOT}/Music/{NFC_NAME}"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.MATCHED
    assert match.content_id == "42"


def test_a_device_relative_row_is_reported_as_unresolved_and_not_as_missing():
    """Three different problems keep three different names."""
    rows = [trees.ContentRow("43", "Contents/a.flac", deleted=False)]
    (match,) = trees.match_active_rows(
        ["Contents/a.flac"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.UNRESOLVED
    assert match.resolution is locations.Resolution.NOT_A_PATH
    assert match.content_id is None


def test_an_unmapped_prefix_is_unresolved_rather_than_silently_absent():
    """A configuration error must not be reported as a deleted file."""
    rows = [trees.ContentRow("44", "/synthetic/elsewhere/a.flac", deleted=False)]
    (match,) = trees.match_active_rows(
        ["/synthetic/elsewhere/a.flac"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.UNRESOLVED
    assert match.resolution is locations.Resolution.UNMAPPED


def test_a_location_url_and_a_plain_path_resolve_to_one_row():
    """The XML side records a URL and the database side records a path."""
    rows = [trees.ContentRow("45", f"{ROOT}/Music/one two.flac", deleted=False)]
    (match,) = trees.match_active_rows(
        [locations.location_url(f"{ROOT}/Music/one two.flac")],
        rows,
        root=ROOT,
        prefix_map=_rules(),
    )
    assert match.outcome is trees.MatchOutcome.MATCHED
    assert match.content_id == "45"


def test_a_soft_deleted_row_beside_one_active_row_resolves_cleanly():
    """rekordbox keeps the row and marks it. A tombstone is not a candidate."""
    rows = [
        trees.ContentRow("46", f"{ROOT}/Music/a.flac", deleted=True),
        trees.ContentRow("47", f"{ROOT}/Music/a.flac", deleted=False),
    ]
    (match,) = trees.match_active_rows(
        [f"{ROOT}/Music/a.flac"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.MATCHED
    assert match.content_id == "47"


def test_a_sweep_matches_every_entry_against_rows_supplied_as_a_cursor():
    """The library is walked ONCE, and a one-shot iterator survives the sweep."""
    rows = [
        trees.ContentRow("50", f"{ROOT}/Music/a.flac", deleted=False),
        trees.ContentRow("51", f"{ROOT}/Music/b.flac", deleted=False),
    ]
    cursor = (row for row in rows)
    index = trees.index_active_rows(cursor, root=ROOT, prefix_map=_rules())

    (first,) = trees.match_indexed_rows(
        [f"{ROOT}/Music/a.flac"], index, root=ROOT, prefix_map=_rules()
    )
    (second,) = trees.match_indexed_rows(
        [f"{ROOT}/Music/b.flac"], index, root=ROOT, prefix_map=_rules()
    )
    assert first.content_id == "50"
    assert second.content_id == "51", "the second entry matched against a spent iterator"


def test_two_active_rows_on_one_location_are_skipped_and_both_surfaced():
    """Written to both, one track sits in a playlist twice under two identities."""
    rows = [
        trees.ContentRow("48", f"{OLDER}/Music/a.flac", deleted=False),
        trees.ContentRow("49", f"{ROOT}/Music/a.flac", deleted=False),
    ]
    (match,) = trees.match_active_rows(
        [f"{ROOT}/Music/a.flac"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.AMBIGUOUS
    assert match.content_ids == ("48", "49")
    assert match.content_id is None, "an ambiguous match must name no single row"


# ═══════════════════════════════════════════════════════════════════════════
# The database half, against a real database and the real session spine
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def db(cfg, tmp_path, monkeypatch):
    """A disposable database, opened through the whole gate and released after."""
    import shutil

    supplied = rb_writer.integration_db_path()
    if supplied is not None:
        path = tmp_path / "supplied" / supplied.name
        path.parent.mkdir(parents=True)
        shutil.copy2(supplied, path)
        for suffix in rb_writer.db_sidecar_suffixes():
            sidecar = supplied.with_name(supplied.name + suffix)
            if sidecar.exists():
                shutil.copy2(sidecar, path.with_name(path.name + suffix))
        unlock = True
    else:
        path = Path(cfg.library.db_path)
        _build_disposable_database(path)
        unlock = False
        # The integrity check reaches for the key and this fixture is unencrypted.
        # Compensated here, never by a verifier argument the writer would accept.
        real_integrity_ok = rb_writer.integrity_ok
        monkeypatch.setattr(
            rb_writer,
            "integrity_ok",
            lambda target, **kwargs: real_integrity_ok(target, unlock=False),
        )

    handle = rb_writer.open_db(path, unlock=unlock, cfg=cfg)
    try:
        yield handle
    finally:
        rb_writer.close_db(handle)


def _rows(root: Path) -> list[trees.ContentRow]:
    """The two content rows the disposable database carries, given locations."""
    return [
        trees.ContentRow("1", f"{root}/Music/one.flac", deleted=False),
        trees.ContentRow("2", f"{root}/Music/two.flac", deleted=False),
    ]


@pytest.fixture
def adopted_root(db):
    """The tree folder a cutover adopted, as a REAL row with a real identifier."""
    folder = rb_writer.ensure_folder(db, TREE_DISPLAY)
    db.session.commit()
    return folder


def _write(cfg, db, *, plan, root_id, registry=None, root_exists=lambda _root: True):
    return trees.write_tree_membership(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=(
            _registry(tree_registry.Mode.DATABASE, root_id=root_id)
            if registry is None
            else registry
        ),
        plan=plan,
        rows=_rows(Path(cfg.library.root)),
        root_exists=root_exists,
        analysis_roots=[Path(cfg.library.root) / "Music"],
    )


def _one(cfg) -> dict:
    """The plan most writes here take: one track into the named folder and sub."""
    return {(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]}


def _unverified_capture(monkeypatch) -> None:
    """Every capture comes back reporting that its integrity check failed."""
    import cratekit.core.snapshot as snapshot_module

    real_capture = snapshot_module.capture

    def unverified(*args, **kwargs):
        taken = real_capture(*args, **kwargs)
        return type(taken)(
            stamp=taken.stamp, root=taken.root, database=taken.database,
            integrity_verified=False, sources=taken.sources, manifest=taken.manifest,
        )

    monkeypatch.setattr(trees.snapshot, "capture", unverified)


def _volume_agrees(cfg, monkeypatch) -> None:
    """The volume identity agrees, and no acknowledgment is recorded."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


def _fail_second_insert(db, monkeypatch) -> dict:
    """The binding's second membership insert raises; returns the call count."""
    real_insert = db.add_to_playlist
    calls = {"n": 0}

    def explode_on_the_second(playlist, content, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("the library went away mid-sweep")
        return real_insert(playlist, content, *args, **kwargs)

    monkeypatch.setattr(db, "add_to_playlist", explode_on_the_second)
    return calls


def test_a_database_write_at_a_tree_still_on_the_bridge_is_refused(cfg, gates_pass):
    """The plan's fifth scenario, and it refuses before it opens anything."""
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        _write(
            cfg,
            None,
            plan={},
            root_id=ADOPTED_ROOT,
            registry=_registry(tree_registry.Mode.XML),
        )
    assert excinfo.value.tree_id == TREE_ID


def test_a_registry_naming_a_root_this_library_lacks_is_refused(cfg, gates_pass):
    """The restored pre-cutover database. Writing now forks the tree in silence."""
    with pytest.raises(tree_registry.RegistrySkew) as excinfo:
        _write(
            cfg,
            None,
            plan={},
            root_id=ADOPTED_ROOT,
            root_exists=lambda _root: False,
        )
    assert excinfo.value.root_id == ADOPTED_ROOT


def test_naming_no_analysis_root_is_refused_rather_than_watching_nothing(cfg, gates_pass):
    """P5, on this unit's own softening path."""
    with pytest.raises(ValueError, match="watch nothing"):
        trees.write_tree_membership(
            cfg,
            None,
            tree_id=TREE_ID,
            registry=_registry(tree_registry.Mode.DATABASE),
            plan={},
            rows=[],
            root_exists=lambda _root: True,
            analysis_roots=[],
        )


def test_a_grid_rewritten_during_a_membership_write_refuses_the_session(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """R-11. The watch this writer arms, driven over a root that holds a grid."""
    root = Path(cfg.library.root)
    # In the share beside the database, the analysis store (R-14), rather than
    # the USB export cache at the volume root that no row resolves into.
    grid = Path(cfg.library.db_path).parent / "share" / "PIONEER" / "USBANLZ" / "8d2" / "ANLZ0000.DAT"
    grid.parent.mkdir(parents=True, exist_ok=True)
    grid.write_bytes(b"analysis")
    assert grid in session.analysis_files_under([root]), "the watch cannot see the grid"

    real_batch = rb_writer.add_memberships

    def rewriting_batch(db_handle, playlist, content_ids):
        grid.write_bytes(b"a rewritten grid, longer than what was there")
        return real_batch(db_handle, playlist, content_ids)

    monkeypatch.setattr(trees.rb_writer, "add_memberships", rewriting_batch)
    with pytest.raises(CratekitError) as excinfo:
        trees.write_tree_membership(
            cfg,
            db,
            tree_id=TREE_ID,
            registry=_registry(tree_registry.Mode.DATABASE, root_id=str(adopted_root.ID)),
            plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{root}/Music/one.flac"]},
            rows=_rows(root),
            root_exists=lambda _root: True,
            analysis_roots=[root],
        )

    cause = excinfo.value.cause
    assert cause.reason == "anlz-modified"
    assert cause.code is ExitCode.REFUSED_BY_POLICY
    assert any(str(grid) in line for line in cause.detail["changed"])
    # The record closes after the watch judged, so a refused session is not on
    # record as clean, and it says the commit landed before the watch looked.
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.committed_sources() == (TREE_ID,)


def test_membership_lands_in_the_named_folder_and_sub(cfg, gates_pass, db, adopted_root):
    """The happy path, end to end through the gates and a real commit."""
    report = _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))
    assert report.added == 1 and report.already_present == 0
    assert report.skipped == ()
    assert report.root_id == str(adopted_root.ID)
    assert report.playlists == (f"{FOLDER_DISPLAY}/{SUB_DISPLAY}",)


def test_a_second_pass_adds_nothing(cfg, gates_pass, db, adopted_root):
    """The plan's first scenario. Re-running is the recovery procedure."""
    plan = _one(cfg)
    root_id = str(adopted_root.ID)
    first = _write(cfg, db, plan=plan, root_id=root_id)
    second = _write(cfg, db, plan=plan, root_id=root_id)
    assert first.added == 1
    assert second.added == 0 and second.already_present == 1


def test_entries_sharing_a_folder_resolve_it_once_and_insert_once_per_playlist(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """R-10. One folder lookup per folder and one membership call per playlist."""
    from pyrekordbox.db6 import tables

    real_folder = rb_writer.ensure_folder
    real_batch = rb_writer.add_memberships
    folder_lookups: list[str] = []
    batches: list[list[str]] = []

    def counting_folder(db_handle, name, parent=None):
        folder_lookups.append(name)
        return real_folder(db_handle, name, parent=parent)

    def counting_batch(db_handle, playlist, content_ids):
        batches.append(list(content_ids))
        return real_batch(db_handle, playlist, content_ids)

    monkeypatch.setattr(trees.rb_writer, "ensure_folder", counting_folder)
    monkeypatch.setattr(trees.rb_writer, "add_memberships", counting_batch)
    report = _write(
        cfg,
        db,
        plan={
            (FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"],
            (FOLDER_DISPLAY, "A Second Sub"): [f"{cfg.library.root}/Music/two.flac"],
        },
        root_id=str(adopted_root.ID),
    )

    assert folder_lookups == [FOLDER_DISPLAY]
    assert sorted(batches) == [["1"], ["2"]]
    assert report.added == 2 and report.already_present == 0
    folders = [
        row for row in db.session.query(tables.DjmdPlaylist).all() if row.Name == FOLDER_DISPLAY
    ]
    assert len(folders) == 1
    subs = [
        row
        for row in db.session.query(tables.DjmdPlaylist).all()
        if row.Name in (SUB_DISPLAY, "A Second Sub")
    ]
    assert sorted(str(row.ParentID) for row in subs) == [str(folders[0].ID)] * 2


def test_a_track_named_twice_in_one_entry_lands_once(cfg, gates_pass, db, adopted_root):
    """The second mention reads as present, as it did when each track was its own read."""
    from pyrekordbox.db6 import tables

    path = f"{cfg.library.root}/Music/one.flac"
    report = _write(
        cfg, db, plan={(FOLDER_DISPLAY, SUB_DISPLAY): [path, path]}, root_id=str(adopted_root.ID)
    )
    assert report.added == 1 and report.already_present == 1
    songs = [
        row
        for row in db.session.query(tables.DjmdSongPlaylist).all()
        if str(row.ContentID) == "1"
    ]
    assert len(songs) == 1


def test_a_second_pass_adopts_the_folder_the_first_pass_made(cfg, gates_pass, db, adopted_root):
    """The plan's second scenario, asserted by COUNTING rows rather than by name."""
    from pyrekordbox.db6 import tables

    plan = _one(cfg)
    root_id = str(adopted_root.ID)
    _write(cfg, db, plan=plan, root_id=root_id)
    _write(
        cfg,
        db,
        plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/two.flac"]},
        root_id=root_id,
    )

    names = [
        row.Name
        for row in db.session.query(tables.DjmdPlaylist).all()
        if row.Name in (FOLDER_DISPLAY, SUB_DISPLAY)
    ]
    assert names.count(FOLDER_DISPLAY) == 1, "the folder was created twice"
    assert names.count(SUB_DISPLAY) == 1, "the sub-playlist was created twice"


def test_an_ambiguous_location_is_skipped_and_carried_into_the_report(
    cfg, gates_pass, db, adopted_root
):
    """Surfaced, which means it reaches the caller rather than a log line."""
    report = trees.write_tree_membership(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_registry(tree_registry.Mode.DATABASE, root_id=str(adopted_root.ID)),
        plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]},
        rows=[
            trees.ContentRow("1", f"{cfg.library.root}/Music/one.flac", deleted=False),
            trees.ContentRow("2", f"{cfg.library.root}/Music/one.flac", deleted=False),
        ],
        root_exists=lambda _root: True,
        analysis_roots=[Path(cfg.library.root) / "Music"],
    )
    assert report.added == 0
    assert len(report.skipped) == 1
    assert report.skipped[0].outcome is trees.MatchOutcome.AMBIGUOUS
    assert report.skipped[0].content_ids == ("1", "2")


def test_the_folder_hangs_off_the_root_the_cutover_adopted(cfg, gates_pass, db, adopted_root):
    """The assertion has to reach the write, or it is decoration."""
    from pyrekordbox.db6 import tables

    _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))
    written = [
        row for row in db.session.query(tables.DjmdPlaylist).all() if row.Name == FOLDER_DISPLAY
    ]
    assert len(written) == 1
    assert str(written[0].ParentID) == str(adopted_root.ID), (
        "the folder was created outside the tree the cutover adopted"
    )


def test_a_root_the_probe_vouched_for_but_the_database_lacks_is_refused(
    cfg, gates_pass, db
):
    """The gap between the caller's probe and the database itself."""
    with pytest.raises(tree_registry.RegistrySkew) as excinfo:
        _write(
            cfg,
            db,
            plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]},
            root_id="a-row-this-library-does-not-have",
            root_exists=lambda _root: True,
        )
    assert excinfo.value.root_id == "a-row-this-library-does-not-have"


def test_a_failure_mid_loop_leaves_nothing_pending_on_the_handle(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """Nothing durable lands, and nothing waits to land under another name."""
    from pyrekordbox.db6 import tables

    # Faulted at the binding's insert rather than at a writer primitive, so the
    # fault lands between two real inserts whichever primitive the loop calls.
    _fail_second_insert(db, monkeypatch)
    with pytest.raises(RuntimeError, match="mid-sweep"):
        _write(
            cfg,
            db,
            plan={
                (FOLDER_DISPLAY, SUB_DISPLAY): [
                    f"{cfg.library.root}/Music/one.flac",
                    f"{cfg.library.root}/Music/two.flac",
                ]
            },
            root_id=str(adopted_root.ID),
        )

    pending = db.session.new | db.session.dirty | db.session.deleted
    assert not pending, f"objects left pending after the failure: {pending}"
    survivors = [
        row for row in db.session.query(tables.DjmdPlaylist).all() if row.Name == SUB_DISPLAY
    ]
    assert survivors == [], "a partial sweep committed a playlist"


def test_the_write_commits_behind_a_verified_capture(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """Nothing commits behind a capture that did not verify."""
    _unverified_capture(monkeypatch)
    with pytest.raises(CratekitError) as excinfo:
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))
    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


def test_a_missing_acknowledgment_refuses_before_the_database_is_touched(
    cfg, monkeypatch, db, adopted_root
):
    """The gates are the writer's, not a caller's to remember."""
    _volume_agrees(cfg, monkeypatch)
    with pytest.raises(CratekitError) as excinfo:
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


# ── R-12 and R-375: the capture a membership write pays for is a reachable undo ──


def _the_one_record(cfg) -> session.SessionRecord:
    recorded = session.records(cfg)
    assert len(recorded) == 1, [entry.session_id for entry in recorded]
    return recorded[0]


def test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts(
    cfg, gates_pass, db, adopted_root
):
    """The cost R-375 names, reproduced: the write took a capture nothing could list."""
    from cratekit.core import restore

    _write(
        cfg,
        db,
        plan={
            (FOLDER_DISPLAY, SUB_DISPLAY): [
                f"{cfg.library.root}/Music/one.flac",
                f"{cfg.library.root}/Music/two.flac",
            ]
        },
        root_id=str(adopted_root.ID),
    )

    listed = restore.list_sessions(cfg)
    assert len(listed) == 1
    only = listed[0]
    assert only.workflow == trees.MEMBERSHIP_WORKFLOW
    assert only.restorable, only.unusable
    assert only.change.trees == (session.TreeChange(tree=TREE_ID, created=2, updated=0),)
    assert only.record.state is session.SessionState.CLOSED
    assert only.record.ended is not None
    # What a LATER restore reads to decide this write is work it would discard.
    assert only.record.committed_sources() == (TREE_ID,)
    assert only.record.actor and only.record.acknowledged_at


def test_the_capture_is_protected_from_pruning_for_the_life_of_the_write(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """R-12's first consequence, asked at the moment it matters: mid write."""
    seen: dict[str, object] = {}
    real_commit = rb_writer.commit_guarded

    def commit_and_look(handle, *args, **kwargs):
        seen["protected"] = rb_writer.default_protected_snapshot_paths(cfg)
        seen["state"] = _the_one_record(cfg).state
        return real_commit(handle, *args, **kwargs)

    monkeypatch.setattr(trees.rb_writer, "commit_guarded", commit_and_look)
    _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))

    record = _the_one_record(cfg)
    assert seen["state"] is session.SessionState.OPEN
    assert seen["protected"] == {Path(record.snapshot_path).resolve()}
    # And the finished write RELEASES it, or every capture is kept for ever.
    assert rb_writer.default_protected_snapshot_paths(cfg) == set()


def test_a_membership_write_that_fails_is_abandoned_and_claims_no_commit(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """Closed on BOTH paths. An open record refuses pruning and the cutover for ever."""

    def explode(*args, **kwargs):
        raise RuntimeError("the library went away mid-sweep")

    monkeypatch.setattr(db, "add_to_playlist", explode)
    with pytest.raises(RuntimeError, match="mid-sweep"):
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))

    record = _the_one_record(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.snapshot_path
    assert record.committed_sources() == ()
    assert record.change.trees == ()


def test_a_failure_after_the_commit_still_reads_as_committed_work(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """The commit is recorded the instant it lands, not at the clean end."""
    from cratekit.core import convergence

    def explode(*args, **kwargs):
        raise RuntimeError("the state write failed")

    monkeypatch.setattr(convergence, "record_fingerprint", explode)
    with pytest.raises(RuntimeError, match="state write failed"):
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))

    record = _the_one_record(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.committed_sources() == (TREE_ID,)
    assert record.change.trees == (session.TreeChange(tree=TREE_ID, created=1, updated=0),)


def test_a_refused_gate_leaves_no_record(cfg, monkeypatch, db, adopted_root):
    """A refusal writes nothing. No acknowledgment is minted here."""
    _volume_agrees(cfg, monkeypatch)
    with pytest.raises(CratekitError):
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))
    assert session.records(cfg) == ()


def test_a_capture_that_did_not_verify_is_recorded_before_the_refusal(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """Attached the instant it exists, which is BEFORE it is judged."""
    _unverified_capture(monkeypatch)
    with pytest.raises(CratekitError):
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))
    record = _the_one_record(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.snapshot_path and Path(record.snapshot_path).is_dir()


def test_a_pass_that_added_nothing_claims_no_commit(cfg, gates_pass, db, adopted_root):
    """The inbox sweep re-runs this writer on every tree, and most runs add nothing."""
    from cratekit.core import restore

    plan = _one(cfg)
    _write(cfg, db, plan=plan, root_id=str(adopted_root.ID))
    again = _write(cfg, db, plan=plan, root_id=str(adopted_root.ID))
    assert again.added == 0

    # By recorded start, which carries microseconds. The identifier's tail is
    # random, so two sessions inside one second do not sort by it.
    first, noop = sorted(session.records(cfg), key=lambda entry: entry.started)
    assert first.committed_sources() == (TREE_ID,)
    assert noop.committed_sources() == ()
    assert noop.state is session.SessionState.CLOSED
    assert noop.change.trees == ()
    assert noop.snapshot_path
    # The question a restore to the first session asks, answered by the function
    # that asks it: the no-op after it is not work that restore would discard.
    assert restore._later_committed(cfg, first) == ()


def test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """An exception out of the commit is not proof that nothing was committed."""
    from pyrekordbox.db6 import tables

    real_commit = db.commit

    def lands_then_fails(*args, **kwargs):
        real_commit(*args, **kwargs)
        raise OSError("the playlist file could not be saved")

    monkeypatch.setattr(db, "commit", lands_then_fails)
    with pytest.raises(OSError, match="playlist file"):
        _write(cfg, db, plan=_one(cfg), root_id=str(adopted_root.ID))

    landed = [row for row in db.session.query(tables.DjmdPlaylist).all() if row.Name == SUB_DISPLAY]
    assert landed, "the fixture did not land the commit it claims to"
    record = _the_one_record(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.committed_sources() == (TREE_ID,)
    assert record.change.trees == (session.TreeChange(tree=TREE_ID, created=1, updated=0),)


def test_the_commit_witness_leaves_the_handle_as_it_found_it(cfg, gates_pass, db, adopted_root):
    """The listener is removed on the way out, on a handle that outlives the write."""
    from sqlalchemy import event

    with rb_writer.commit_witness(db) as witness:
        assert event.contains(db.session, "after_commit", witness._mark)
        assert witness.landed is False
        rb_writer.ensure_folder(db, "a witnessed folder")
        db.session.commit()
        assert witness.landed is True
    assert not event.contains(db.session, "after_commit", witness._mark)


def test_the_commit_witness_does_not_read_a_commit_that_never_landed_as_landed(
    cfg, gates_pass, db, adopted_root
):
    """The other half: a commit refused on its way IN recorded nothing durable."""
    from sqlalchemy import event

    def refuse(_session):
        raise RuntimeError("the transaction was refused before it landed")

    with rb_writer.commit_witness(db) as witness:
        event.listen(db.session, "before_commit", refuse)
        try:
            rb_writer.ensure_folder(db, "a folder that never lands")
            with pytest.raises(RuntimeError, match="before it landed"):
                db.session.commit()
        finally:
            event.remove(db.session, "before_commit", refuse)
            db.session.rollback()
        assert witness.landed is False


def test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit(
    cfg, gates_pass, db, adopted_root, monkeypatch
):
    """The witness decides, not the count. Found by the mutation table as a zero row."""
    calls = _fail_second_insert(db, monkeypatch)
    with pytest.raises(RuntimeError, match="mid-sweep"):
        _write(
            cfg,
            db,
            plan={
                (FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"],
                (OTHER_FOLDER, SUB_DISPLAY): [f"{cfg.library.root}/Music/two.flac"],
            },
            root_id=str(adopted_root.ID),
        )

    assert calls["n"] == 2, "the fixture never reached the second playlist"
    record = _the_one_record(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.committed_sources() == ()
    assert record.change.trees == ()
