"""U18: the tree writers, in both mediums, and the row matching between them.

WHAT THE GOLDENS ALREADY COVER AND THIS FILE DOES NOT REPEAT. Nine golden files
in tests/test_xml_splice_golden.py pin the exact bytes every bridge writer here
emits, which is the answer to "did collapsing five implementations into one
change the output". This file covers what a byte comparison cannot: the paths no
golden was ever produced for, and the whole database half, which has no bytes.

THE FIVE SCENARIOS THE PLAN NAMES FOR THIS UNIT, and where each is proved:

1. membership deduplicates on re-run, zero new rows on a second pass
   -> ``test_a_second_pass_adds_nothing``
2. adoption by name picks the existing folder, not a numbered duplicate
   -> ``test_a_second_pass_adopts_the_folder_the_first_pass_made``
3. normalization resolves a prefixed path, a composition-form mismatch, and a
   device-relative row -> the three ``test_normalization_*`` cases
4. two active rows on one normalized location are skipped and surfaced
   -> ``test_two_active_rows_on_one_location_are_skipped_and_both_surfaced``
5. the writer refuses when the registry still marks the tree as XML
   -> ``test_a_database_write_at_a_tree_still_on_the_bridge_is_refused``

WHY THE DATABASE HALF RUNS AGAINST A REAL DATABASE. The pure rules are proved
pure, without one. What a synthetic mapping cannot prove is the joint: that a
folder found by name is the folder the previous run created, that a membership
insert really is idempotent through the binding rather than through our reading
of it, and that the whole thing survives the session spine it is wrapped in.
Those are the joints where correct-looking code guards nothing.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track, and the paths are synthetic while still carrying the character
classes that matter: a space, and an accented character in both composition
forms.
"""

from __future__ import annotations

import unicodedata
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, locations, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rbxml, trees
from tests.test_config import valid_data
from tests.test_rb_writer_db import (
    RECORDED_APP_VERSION,
    _build_disposable_database,
)
from tests.xml_fixtures import _fresh_xml, _no_bare_lf, _xml_doc

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"
FOLDER_DISPLAY = "Loud! Room"
SUB_DISPLAY = "Café Nights"
OTHER_FOLDER = "Quiet? Corner"
CATALOG_DISPLAY = "Catalogued Sources"
ADOPTED_ROOT = "root-row-7788"


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
    """One absent folder is a fact to carry to the end, not a reason to stop.

    A sweep touches many playlists. Raising on the first miss abandons the other
    writes, and the source system's answer, printing and continuing, is not
    available to a layer with no console.
    """
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
    """The one difference between the two entry points, asserted from both sides.

    They shared a body and differ by one flag, so the risk is that the flag stops
    reaching one of them. Proved by driving the same absent sub through both.
    """
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
    """An empty plan entry is skipped rather than emitted as an empty playlist.

    The creating path is the one that could get this wrong: asked to create a sub
    for zero tracks, it would leave an empty node behind on every run.
    """
    content = bytearray(_tree_doc())
    before = bytes(content)
    report = trees.apply_unplaced_changes(
        {(FOLDER_DISPLAY, "Not There Yet"): []}, content, tree=_ungoverned()
    )
    assert report.inserted == 0 and bytes(content) == before


def test_the_sweep_order_does_not_depend_on_the_callers_dict_order():
    """A golden compares BYTES, so the byte output cannot depend on insertion order.

    Two plans holding the same pairs in opposite orders must produce one document,
    or a golden becomes a test of whichever order the producer happened to use.
    """
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
    """The bridge guard reaches the sweep through the emitter, not around it.

    Asserted here as well as per-emitter in tests/test_tree_registry.py, because
    what this file is about is the CALL SITE: a sweep that dropped the tree
    argument would pass every emitter test and still splice a tree the database
    owns.
    """
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
    """The hole a reviewer walked through, pinned from the entry point that had it.

    tests/test_tree_registry.py proves the emitter guard fires when a governed
    tree is handed to it, and the sweep test above proves a call site that
    forwards one keeps that property. Neither says anything about the tree a
    caller gets when it names none, and that was the one that was wrong: an
    ungoverned tree built from a declared node, which the guard correctly ignores
    because most playlists in a real library are somebody's own. The sweep then
    spliced an export for a tree the database already owned, and under U9's A2
    verdict importing that export replaces the database-native tree outright.
    """
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
        trees.add_vox_playlists(document, registry=native)
    assert excinfo.value.tree_id == declared.tree.id

    # And the same registry with the tree still on the bridge lets it through,
    # or the assertion above would also hold for a writer that refused always.
    out, report = trees.add_vox_playlists(document, registry=tree_registry.EMPTY)
    assert report.modified == (FOLDER_DISPLAY,)
    assert out != document


def test_a_sweep_naming_neither_a_registry_nor_a_tree_refuses_to_guess():
    """There is no ungoverned default, which is the property, not the message.

    A default would hand back exactly the tree the test above proves is unsafe,
    so the absence of one is what closes the hole. Asserted on both entry points
    because they had the same default and would regress independently.
    """
    with pytest.raises(ValueError, match="registry"):
        trees.add_vox_playlists(_tree_doc())


def test_a_catalog_import_naming_neither_a_registry_nor_a_tree_refuses(tmp_path):
    """The catalog entry point's half of the same property."""
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    with pytest.raises(ValueError, match="registry"):
        trees.insert_record_labels_tree(
            source, "Kompakt", _buckets(2025), tmp_path / "out.xml"
        )
    assert not (tmp_path / "out.xml").exists()


def test_a_catalog_tree_is_not_written_outside_a_self_closed_playlist_root(tmp_path):
    """rekordbox exports a childless node self closed, and it has no body to write into.

    The offset arithmetic succeeds against one anyway: the bytes just past the
    closing slash are the break ending the node's OWN line, so the write lands
    beside the root rather than inside it and reports success. Refused now, with
    the document left byte for byte as it was found.
    """
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
    """The enumeration and the write have to mean the same folder.

    The sweep lists the tree's DIRECT folder children, then writes to each by
    name. A body-wide search resolves that name to whichever node carries it
    first in document order, which is a folder nested inside an earlier sibling
    whenever the two share a name. The write would land one level too deep and
    report the outer folder's name.
    """
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
    out, report = trees.add_vox_playlists(document, tree=_ungoverned())
    vox = taxonomy.default_taxonomy().sub_class(trees.VOX_SUB_CLASS).display

    # Both DIRECT children gain one, which is the sweep doing its job. What must
    # not gain one is the nested namesake, because it is not a child of the tree
    # and the enumeration never named it. Before the direct-child scoping, the
    # write for FOLDER_DISPLAY resolved to that nested node instead, so the
    # direct child of the same name got nothing and the report said otherwise.
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
    """A folder it could not serve and a folder that needed nothing are not one fact.

    Reported through ``modified`` alone they were: both leave the name off the
    list. The blocked folder is the one somebody has to act on.
    """
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
    out, report = trees.add_vox_playlists(document, tree=_ungoverned())
    assert report.modified == ()
    assert len(report.warnings) == 1
    assert "with vox" in report.warnings[0]
    assert out == before, "a warned folder must not be written"


def test_two_folders_of_one_name_are_refused_rather_than_half_served():
    """A name-targeted writer cannot tell them apart, so it must not try.

    Without this the vocal sweep writes to the first folder twice and to the
    second one never, and the count it returns says two.
    """
    raw = _tree_doc(folders=(FOLDER_DISPLAY, FOLDER_DISPLAY))
    with pytest.raises(trees.DuplicateFolders) as excinfo:
        trees.add_vox_playlists(raw, tree=_ungoverned())
    assert FOLDER_DISPLAY in str(excinfo.value)


def test_a_playlist_wearing_the_trees_name_refuses_rather_than_walking_nothing():
    """The wrong-type collision, which "not found" would have hidden.

    A root-level PLAYLIST named after the tree is not an absent tree. Reported as
    absent, the sweep walks zero folders, returns an empty modified list, and
    reads to the user exactly like a library that was already up to date.
    """
    document = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
        ],
    )
    with pytest.raises(trees.TreeUnreachable) as excinfo:
        trees.add_vox_playlists(document, tree=_ungoverned())
    assert "playlist" in str(excinfo.value)


def test_a_sweep_over_a_document_with_no_such_tree_refuses(tmp_path):
    """The other half. An absent tree is a mistake, not a quiet no-op."""
    with pytest.raises(trees.TreeUnreachable):
        trees.add_vox_playlists(_fresh_xml(), tree=_ungoverned())


def test_the_vocal_sweep_touches_only_the_folders_that_lack_the_playlist():
    """Idempotence per FOLDER, not per document.

    The golden proves one folder gains one playlist. This proves the second run
    after a new folder appears touches the new one and leaves the other byte for
    byte alone, which is what makes re-running it the ordinary thing to do.
    """
    declared = taxonomy.default_taxonomy()
    vox = declared.sub_class(trees.VOX_SUB_CLASS).display

    once, modified = trees.add_vox_playlists(_tree_doc(), tree=_ungoverned())
    assert modified == [FOLDER_DISPLAY]
    assert once.count(rbxml.name_marker(vox)) == 1

    grown = _tree_doc(folders=(FOLDER_DISPLAY, OTHER_FOLDER))
    seeded, _ = trees.add_vox_playlists(grown, tree=_ungoverned())
    again, modified_again = trees.add_vox_playlists(seeded, tree=_ungoverned())
    assert modified_again == []
    assert again == seeded
    assert again.count(rbxml.name_marker(vox)) == 2
    assert _no_bare_lf(again)


def test_copying_a_taxonomy_for_a_test_keeps_its_derived_indexes():
    """The trap the two tests below would otherwise fall into, pinned here.

    A ``Taxonomy`` carries four indexes derived at construction, each defaulting
    to an empty mapping. Rebuilding one by hand-listing its public fields, which
    is the obvious way to change a single entry, silently hands back an object
    whose bucket and alias lookups all answer nothing. Nothing raises; the
    taxonomy simply behaves as though it declared no buckets at all.

    ``dataclasses.replace`` copies every field including those four, which is why
    it is the idiom this suite already uses. This asserts the property rather
    than the idiom, so a future hand-rolled copy fails here and says why.
    """
    declared = taxonomy.default_taxonomy()
    copied = replace(declared, catalog=None)
    assert copied.catalog is None
    bucket_id = declared.buckets[0].id
    assert copied.bucket(bucket_id) == declared.bucket(bucket_id)


def test_the_vocal_sweep_reads_both_names_from_the_declared_taxonomy():
    """R19 in its live form: rename either name and the sweep follows.

    The write layer may not spell a display name at all, so the only way this can
    be wrong is by reaching for the shipped default when a caller supplied their
    own template. Driven with a renamed sub-playlist, which is what a user who
    dislikes the shipped name actually does.
    """
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
    """The source system's second run grew a second copy of the whole label.

    No golden covers this, because the system these were ported from had no test
    that ran twice. It is the defect the consolidation fixes, so it is asserted
    directly: one folder, the new contents, and the tree's own count unmoved.
    """
    source = tmp_path / "fresh.xml"
    source.write_bytes(_fresh_xml())
    first = tmp_path / "one.xml"
    trees.insert_record_labels_tree(
        source, "Kompakt", _buckets(2025), first, tree=rbxml.Tree(display=CATALOG_DISPLAY)
    )
    second = tmp_path / "two.xml"
    trees.insert_record_labels_tree(
        first, "Kompakt", _buckets(2025, 2024), second, tree=rbxml.Tree(display=CATALOG_DISPLAY)
    )

    out = second.read_bytes()
    assert out.count(rbxml.name_marker("Kompakt")) == 1, "the folder was duplicated"
    assert out.count(rbxml.name_marker(CATALOG_DISPLAY)) == 1
    assert rbxml.name_marker("Kompakt 2024") in out
    assert b'<NODE Name="' + CATALOG_DISPLAY.encode() + b'" Type="0" Count="1">' in out
    assert _no_bare_lf(out)


def test_a_catalog_write_into_a_taxonomy_declaring_no_catalog_tree_refuses_by_name(tmp_path):
    """A default nobody saw would put a folder in somebody's library by surprise.

    The catalog tree is optional in the template on purpose, so the writer has to
    have an answer for a library that declares none, and inventing one is not it.
    """
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
            tmp_path / "out.xml",
            tree=rbxml.Tree(display=CATALOG_DISPLAY),
        )
    assert not (tmp_path / "out.xml").exists()


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
    """Most active rows in a real library record a volume name it no longer uses.

    A resolver with no map resolves none of them, so this is not an edge case, it
    is the ordinary case.
    """
    rows = [trees.ContentRow("41", f"{OLDER}/Music/a.flac", deleted=False)]
    (match,) = trees.match_active_rows(
        [f"{ROOT}/Music/a.flac"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.MATCHED
    assert match.content_id == "41"


def test_normalization_resolves_a_composition_form_mismatch():
    """Both sides go through the normalizer, or neither side is comparable.

    Asserted in the direction that actually occurs: the row carries one form and
    the caller supplies the other.
    """
    rows = [trees.ContentRow("42", f"{ROOT}/Music/{NFD_NAME}", deleted=False)]
    (match,) = trees.match_active_rows(
        [f"{ROOT}/Music/{NFC_NAME}"], rows, root=ROOT, prefix_map=_rules()
    )
    assert match.outcome is trees.MatchOutcome.MATCHED
    assert match.content_id == "42"


def test_a_device_relative_row_is_reported_as_unresolved_and_not_as_missing():
    """Three different problems keep three different names.

    A streaming pseudo-location and a device-relative path are not files this
    machine can resolve, and calling either one "absent" tells a user to go
    looking for something that was never there.
    """
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
    """The XML side records a URL and the database side records a path.

    One matcher serves both, because a cutover compares what the bridge wrote
    against what the database holds and the two spell the same file differently.
    """
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
    """The library is walked ONCE, and a one-shot iterator survives the sweep.

    The natural way to hand over "every content row" for a library this size is a
    database cursor, not a materialized list. A sweep that rebuilt its index per
    plan entry would consume the whole cursor on the first entry and see an
    exhausted iterable on every entry after it, reporting each of those tracks as
    absent while the run reported itself clean. That is the shape this pins: the
    same rows, supplied as a generator, matched twice.
    """
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
    """Written to both, one track sits in a playlist twice under two identities.

    The user then removes it once and it is still there, which reads as the
    product ignoring them. Skipping and naming both is the only answer that lets
    them fix it.
    """
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
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library, monkeypatch):
    """Configuration with the application pin RECORDED, since an unset one refuses."""
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(
        rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION
    )
    return resolved


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """Everything about THIS machine that a temporary library cannot speak for.

    The three process probes and the cloud-sync marker, patched where the guards
    resolve them. None of this weakens what is under test here: that these guards
    refuse is proved directly, against the same seams driven the other way, in
    tests/test_rb_writer_db.py.
    """
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


@pytest.fixture
def gates_pass(cfg, monkeypatch):
    """The volume identity agrees and the acknowledgment is recorded.

    Patched at the PRECONDITION seam rather than injected, so the writer is
    driven with no seam supplied at all, which is exactly how a real caller
    reaches the gates.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


@pytest.fixture
def db(cfg, tmp_path, monkeypatch):
    """A disposable database, opened through the whole gate and released after.

    A supplied snapshot SUBSTITUTES for the synthetic build rather than switching
    these tests on, which is the convention seam decision Part 4 sets for every
    volume-dependent gate: the battery runs either way, and supplying a real
    snapshot strengthens it. The supplied file is copied first, because these
    tests write and writing to a file somebody handed us is not ours to do. The
    synthetic build is not encrypted, so it opens without the key and the key
    path is exercised only by a supplied snapshot.
    """
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
        # The capture's integrity check reaches for the key by default, and an
        # unencrypted fixture fails it, which would report every session here as
        # having no verified recovery point. Compensated at the FIXTURE, never by
        # giving the writer a verifier argument: a writer that accepts one
        # accepts ``lambda _: True``, and the gate this unit is registered
        # against would then be defeatable by the parameter meant to test it.
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
    """The two content rows the disposable database carries, given locations.

    The database's own rows hold no path, so the matcher is fed the mapping a
    caller would build from them. What is under test on this side is the write,
    not the read.
    """
    return [
        trees.ContentRow("1", f"{root}/Music/one.flac", deleted=False),
        trees.ContentRow("2", f"{root}/Music/two.flac", deleted=False),
    ]


@pytest.fixture
def adopted_root(db):
    """The tree folder a cutover adopted, as a REAL row with a real identifier.

    Seeded rather than invented, because the whole point of the adopted root is
    that the folders a membership write creates hang off it. A test naming an
    identifier no row carries can only prove the refusal path; proving the write
    lands INSIDE the tree needs a row the write can be parented to.
    """
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


def test_a_database_write_at_a_tree_still_on_the_bridge_is_refused(cfg, gates_pass):
    """The plan's fifth scenario, and it refuses before it opens anything.

    Driven with no database handle at all, which is the assertion: a writer that
    checked the medium after opening the library would need one.
    """
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
    """P5, on this unit's own softening path.

    An empty watch reports a clean session whatever happened to the library's
    grids, which is worse than no watch at all because it looks like one ran.
    """
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


def test_membership_lands_in_the_named_folder_and_sub(cfg, gates_pass, db, adopted_root):
    """The happy path, end to end through the gates and a real commit."""
    report = _write(
        cfg,
        db,
        plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]},
        root_id=str(adopted_root.ID),
    )
    assert report.added == 1 and report.already_present == 0
    assert report.skipped == ()
    assert report.root_id == str(adopted_root.ID)
    assert report.playlists == (f"{FOLDER_DISPLAY}/{SUB_DISPLAY}",)


def test_a_second_pass_adds_nothing(cfg, gates_pass, db, adopted_root):
    """The plan's first scenario. Re-running is the recovery procedure.

    A second pass that inserted again would turn "run it again" into a second
    failure, and the duplicate is one the user cannot remove by removing it once.
    """
    plan = {(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]}
    root_id = str(adopted_root.ID)
    first = _write(cfg, db, plan=plan, root_id=root_id)
    second = _write(cfg, db, plan=plan, root_id=root_id)
    assert first.added == 1
    assert second.added == 0 and second.already_present == 1


def test_a_second_pass_adopts_the_folder_the_first_pass_made(cfg, gates_pass, db, adopted_root):
    """The plan's second scenario, asserted by COUNTING rows rather than by name.

    A "numbered duplicate" is what the binding's own create helper produces when
    a find misses, and it is invisible to any assertion that only looks up the
    name again: the lookup finds the first one and reports success.
    """
    from pyrekordbox.db6 import tables

    plan = {(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]}
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
    """Surfaced, which means it reaches the caller rather than a log line.

    The whole value of skipping is that somebody is told. A skip the report does
    not carry is indistinguishable from a track that was never asked for.
    """
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
    """The assertion has to reach the write, or it is decoration.

    ``anchored_root`` refuses a tree whose adopted root this library lacks, which
    is the restored pre-cutover database. That refusal buys nothing if the write
    then resolves its folder globally by name: the assertion holds, and the
    folder is created at the database root beside the tree rather than inside it,
    which is the silent parallel tree the registry exists to prevent. Asserted on
    ParentID, because counting rows by name passes either way.
    """
    from pyrekordbox.db6 import tables

    _write(
        cfg,
        db,
        plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]},
        root_id=str(adopted_root.ID),
    )
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
    """The gap between the caller's probe and the database itself.

    ``anchored_root`` asks a ``root_exists`` callable the caller supplies, so a
    caller whose probe is optimistic, or simply stale, gets past it. Reaching the
    write with no such row and creating the folders unparented would put the
    whole tree beside itself, so this refuses on the read-back instead.
    """
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
    """Nothing durable lands, and nothing waits to land under another name.

    The loop creates folders, playlists and membership rows and commits once at
    the end. An exception between the two leaves those objects pending on the
    CALLER'S handle, and the guarded commit raises on two of its own refusals
    before reaching its rollback. Left pending, they ride out on whatever commits
    next and arrive attributed to that operation.
    """
    from pyrekordbox.db6 import tables

    real_add = rb_writer.add_membership
    calls = {"n": 0}

    def explode_on_the_second(db_handle, playlist, content_id):
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("the library went away mid-sweep")
        return real_add(db_handle, playlist, content_id)

    monkeypatch.setattr(trees.rb_writer, "add_membership", explode_on_the_second)
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
    """Nothing commits behind a capture that did not verify.

    Driven by failing the capture's own integrity check, which is the condition
    the gate exists for, rather than by patching the gate itself.
    """
    import cratekit.core.snapshot as snapshot_module

    real_capture = snapshot_module.capture

    def unverified(*args, **kwargs):
        record = real_capture(*args, **kwargs)
        return type(record)(
            stamp=record.stamp,
            root=record.root,
            database=record.database,
            integrity_verified=False,
            sources=record.sources,
            manifest=record.manifest,
        )

    monkeypatch.setattr(trees.snapshot, "capture", unverified)
    with pytest.raises(CratekitError) as excinfo:
        _write(
            cfg,
            db,
            plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]},
            root_id=str(adopted_root.ID),
        )
    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


def test_a_missing_acknowledgment_refuses_before_the_database_is_touched(
    cfg, monkeypatch, db, adopted_root
):
    """The gates are the writer's, not a caller's to remember.

    No acknowledgment is minted here, which is the whole fixture difference from
    every test above.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    with pytest.raises(CratekitError) as excinfo:
        _write(
            cfg,
            db,
            plan={(FOLDER_DISPLAY, SUB_DISPLAY): [f"{cfg.library.root}/Music/one.flac"]},
            root_id=str(adopted_root.ID),
        )
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED
