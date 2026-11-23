"""U17: per-tree write medium, the two guards, and the locate set that makes coverage true.

The registry is library scoped and starts on the bridge, the byte bridge refuses a database
tree for every DERIVED emitter, the database side refuses the inverse and a skewed registry,
and the locates are consolidated so no call site routes around the guard. Every display
name is synthesized (D1)."""

from __future__ import annotations

import ast
import inspect
import json
import os
import stat
import unicodedata
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, taxonomy, tree_registry
from cratekit.write import rbxml
from tests.xml_fixtures import _EMPTY_COLLECTION, _ml_track, _no_bare_lf, _xml_doc

REPO_ROOT = Path(__file__).resolve().parent.parent


# Fixtures


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A synthetic library root, aligned with the suite's isolation fixture."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def _config_data(root: Path) -> dict:
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root),
            "volume_id": "A1B2-C3D4",
            "db_path": str(root / "db" / "master.db"),
        },
        "paths": {"download_staging": str(root.parent / "staging")},
        "profile": {"name": "slim"},
    }


@pytest.fixture
def cfg(library):
    return config.from_dict(_config_data(library))


@pytest.fixture
def permissive_umask():
    """Run the body under umask 000, since umask 022 hides a missing explicit mode."""
    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


# ── synthesized display names (D1) ───────────────────────────────────────────

#: A tree name carrying an ampersand, which escaper and marker builder must encode alike.
TREE_DISPLAY = "Shelf & Stack"
#: A folder name carrying a literal exclamation mark and a space.
FOLDER_DISPLAY = "Loud! Room"
#: A sub-playlist name carrying an accented character, PRECOMPOSED.
SUB_DISPLAY = "Café Nights"
#: The same name DECOMPOSED, as macOS stores it, so both forms meet in one document.
SUB_DISPLAY_NFD = unicodedata.normalize("NFD", SUB_DISPLAY)

TREE_ID = "shelf_stack"
NEW_FOLDER = "Quiet? Corner"
NEW_PLAYLIST = "Batch 001 & 002"

CUTOVER_ON = date(2026, 8, 1)
ADOPTED_ROOT = "root-row-7788"

#: The derivation source every cutover records, a required part of a native record (U36).
DERIVATION = tree_registry.DerivationSource.TAXONOMY

#: A key the fixture sub already holds, so the REMOVAL emitter really removes something.
SEEDED_TRACK = 900


def _esc(value: str) -> str:
    return rbxml.xml_escape_attr(value)


def _sub_lines(indent: str = "          ") -> list[str]:
    """The fixture sub-playlist, holding one track key."""
    return [
        f'{indent}<NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="1">',
        f'{indent}  <TRACK Key="{SEEDED_TRACK}"/>',
        f"{indent}</NODE>",
    ]


def _tree_doc() -> bytes:
    """One tree holding one folder holding one track-bearing sub-playlist."""
    return _playlists(
        f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">',
        f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
        *_sub_lines(),
        "        </NODE>",
        "      </NODE>",
    )


def _registry(mode: tree_registry.Mode | None) -> tree_registry.Registry:
    """A registry with one record for the fixture tree, or with none at all."""
    if mode is None:
        return tree_registry.EMPTY
    if mode is tree_registry.Mode.DATABASE:
        return tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=TREE_ID,
                    mode=mode,
                    cutover_on=CUTOVER_ON,
                    root_id=ADOPTED_ROOT,
                    source=tree_registry.DerivationSource.TAXONOMY,
                ),
            )
        )
    return tree_registry.Registry((tree_registry.TreeRecord(tree_id=TREE_ID, mode=mode),))


def _governed(mode: tree_registry.Mode) -> rbxml.Tree:
    return rbxml.Tree(display=TREE_DISPLAY, id=TREE_ID, registry=_registry(mode))


#: The fixture tree's record once cut over, as the persisted document spells it.
_NATIVE = {
    "tree": TREE_ID,
    "mode": "database",
    "cutover_on": CUTOVER_ON.isoformat(),
    "root": ADOPTED_ROOT,
}


def _write_document(path: Path, trees: list, *, version=tree_registry.SCHEMA_VERSION) -> None:
    """Write a registry document by hand, as another build or a hand edit would."""
    config.atomic_write_bytes(
        json.dumps({"schema_version": version, "trees": trees}).encode(), path
    )


def _cut_over(cfg, tree_id: str = TREE_ID, root_id: str = ADOPTED_ROOT) -> None:
    tree_registry.record_cutover(cfg, tree_id, root_id=root_id, on=CUTOVER_ON, source=DERIVATION)


def _playlists(*root_children: str) -> bytes:
    """A document with an empty collection and these children of the ROOT node."""
    return _xml_doc(collection=_EMPTY_COLLECTION, root_children=list(root_children))


# The registry: what it holds, where it lives, how it starts


def test_every_tree_starts_on_the_bridge_and_that_is_not_a_setting(cfg):
    """No registry, no record, or no explicit mode all resolve to the bridge."""
    assert tree_registry.DEFAULT_MODE is tree_registry.Mode.XML
    assert tree_registry.read(cfg) is tree_registry.EMPTY
    assert tree_registry.read(cfg).mode("anything_at_all") is tree_registry.Mode.XML
    assert tree_registry.TreeRecord(tree_id=TREE_ID).mode is tree_registry.Mode.XML
    assert tree_registry.EMPTY.is_on_the_bridge(TREE_ID)


def test_a_record_carries_the_mode_the_date_and_the_adopted_root(cfg):
    """Mode, date and adopted root, because a mode alone cannot detect skew."""
    _cut_over(cfg)
    record = tree_registry.read(cfg).record(TREE_ID)
    assert record is not None
    assert record.mode is tree_registry.Mode.DATABASE
    assert record.cutover_on == CUTOVER_ON
    assert record.root_id == ADOPTED_ROOT


def test_a_native_record_without_an_adopted_root_cannot_be_constructed():
    """Refused at construction, since native naming nothing reads as never cut over."""
    with pytest.raises(ValueError, match="adopted root"):
        tree_registry.TreeRecord(
            tree_id=TREE_ID, mode=tree_registry.Mode.DATABASE, cutover_on=CUTOVER_ON
        )
    with pytest.raises(ValueError, match="cutover date"):
        tree_registry.TreeRecord(
            tree_id=TREE_ID, mode=tree_registry.Mode.DATABASE, root_id=ADOPTED_ROOT
        )


def test_a_cutover_leaves_every_other_tree_alone(cfg):
    """Trees cut over one at a time, so a whole-file overwrite would erase the rest."""
    _cut_over(cfg, "first_tree", "root-1")
    _cut_over(cfg, "second_tree", "root-2")
    after = tree_registry.read(cfg)
    assert after.tree_ids() == ("first_tree", "second_tree")
    assert after.is_database_native("first_tree")
    assert after.is_database_native("second_tree")


def test_the_persisted_record_is_keyed_on_the_identifier_not_the_display_name(cfg):
    """R19 and D5: keyed on the identifier, read from the BYTES, so a rename orphans nothing."""
    _cut_over(cfg)
    raw = tree_registry.path_for(cfg).read_text(encoding="utf-8")
    assert TREE_ID in raw
    assert TREE_DISPLAY not in raw, "a display name reached the persisted record"
    parsed = json.loads(raw)
    assert [entry["tree"] for entry in parsed["trees"]] == [TREE_ID]


def test_the_state_entry_is_library_scoped_coupled_and_never_committed():
    """KTD22: library scoped, COUPLED to snapshots, and ignored by git."""
    entry = config.state_file(tree_registry.STATE_KEY)
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.snapshot is config.SnapshotRole.COUPLED
    assert entry in config.coupled_state_files()
    ignored = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert entry.relative in ignored


def test_the_registry_file_and_the_directories_it_creates_are_private(
    permissive_umask, cfg
):
    """P1: the directory mode matters too, since unlink and rename are the directory's."""
    path = tree_registry.write(cfg, _registry(tree_registry.Mode.XML))
    assert stat.S_IMODE(path.stat().st_mode) == config.PRIVATE_FILE_MODE

    created = []
    node = path.parent
    while node != cfg.library.root and cfg.library.root in node.parents:
        created.append(node)
        node = node.parent
    assert created, "the write created no directory under the library root"
    for directory in created:
        assert stat.S_IMODE(directory.stat().st_mode) == config.PRIVATE_DIR_MODE, (
            f"{directory} was created at the umask rather than at an explicit mode"
        )


def test_the_registry_is_read_through_the_effective_config_not_the_file_value(
    tmp_path, monkeypatch
):
    """P2: the registry is read through the effective config, as the writers read it."""
    written = tmp_path / "written"
    (written / "Music").mkdir(parents=True)
    relocated = tmp_path / "relocated"
    (relocated / "Music").mkdir(parents=True)

    data = _config_data(written)
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT, raising=False)
    at_file_value = config.from_dict(data)
    decoy = config.state_path(tree_registry.STATE_KEY, at_file_value)

    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(relocated))
    effective = config.from_dict(data)
    assert effective.library.root == relocated

    # The decoy says the tree already cut over. Nothing may read it.
    _write_document(decoy, [_NATIVE])
    tree_registry.write(effective, _registry(tree_registry.Mode.XML))

    assert tree_registry.path_for(effective) != decoy
    assert tree_registry.read(effective).is_on_the_bridge(TREE_ID), (
        "the registry was read from the file's library root rather than the effective one"
    )


# ── reading a file this build cannot vouch for ───────────────────────────────


def test_an_unreadable_registry_is_its_own_answer_and_not_an_empty_one(cfg):
    """Unreadable is never "no record", which would send a byte write at a database tree."""
    path = tree_registry.path_for(cfg)
    config.atomic_write_bytes(b"{ not json", path)
    with pytest.raises(tree_registry.TreeRegistryUnreadable) as excinfo:
        tree_registry.read(cfg)
    assert excinfo.value.path == path
    assert excinfo.value.remedy is not None


def test_a_registry_from_a_newer_build_is_refused_rather_than_guessed_at(cfg):
    _write_document(tree_registry.path_for(cfg), [], version=tree_registry.SCHEMA_VERSION + 1)
    with pytest.raises(tree_registry.TreeRegistryUnreadable, match="schema version"):
        tree_registry.read(cfg)


def test_a_record_with_an_unknown_mode_is_refused_rather_than_dropped(cfg):
    """An unknown mode fails the whole read, since a dropped record reads as the bridge."""
    _write_document(tree_registry.path_for(cfg), [{"tree": TREE_ID, "mode": "carrier-pigeon"}])
    with pytest.raises(tree_registry.TreeRegistryUnreadable, match="unusable record"):
        tree_registry.read(cfg)


def test_two_records_for_one_tree_are_refused_rather_than_resolved_by_position(cfg):
    """Two answers for one tree fail the read, never resolved by line order."""
    _write_document(tree_registry.path_for(cfg), [{"tree": TREE_ID, "mode": "xml"}, _NATIVE])
    with pytest.raises(tree_registry.TreeRegistryUnreadable, match="two records"):
        tree_registry.read(cfg)


def test_the_bytes_are_a_function_of_the_content_alone(cfg):
    """Identical bytes for one registry, so the file only diffs when something changed."""
    registry = tree_registry.EMPTY.with_record(
        tree_registry.TreeRecord(tree_id="zulu")
    ).with_record(tree_registry.TreeRecord(tree_id="alpha"))
    first = tree_registry.write(cfg, registry).read_bytes()
    reversed_order = tree_registry.Registry(tuple(reversed(registry.trees)))
    second = tree_registry.write(cfg, reversed_order).read_bytes()
    assert first == second


# The emitter guard, over a DERIVED emitter set (P3), cross-checked (P4)


def _public_functions() -> dict[str, object]:
    return {
        name: obj
        for name, obj in vars(rbxml).items()
        if not name.startswith("_")
        and inspect.isfunction(obj)
        and obj.__module__ == rbxml.__name__
    }


#: Methods that mutate their buffer, a byte write no subscript walk catches.
_MUTATING_METHODS = frozenset(
    {"extend", "insert", "append", "clear", "pop", "remove", "__setitem__"}
)


def _byte_writers_by_annotation(
    functions: dict[str, object] | None = None,
) -> frozenset[str]:
    """Every public function whose annotation MENTIONS ``bytearray``, the first reading."""
    found = set()
    for name, obj in (_public_functions() if functions is None else functions).items():
        for parameter in inspect.signature(obj).parameters.values():
            annotation = parameter.annotation
            if isinstance(annotation, str) and "bytearray" in annotation:
                found.add(name)
    return frozenset(found)


def _byte_writers_by_source(source: str | None = None) -> frozenset[str]:
    """Every public function that mutates a parameter, directly, by method, or transitively."""
    tree = ast.parse(
        Path(rbxml.__file__).read_text(encoding="utf-8") if source is None else source
    )
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    direct: set[str] = set()
    calls: dict[str, set[str]] = {}
    for name, node in functions.items():
        parameters = {arg.arg for arg in (*node.args.args, *node.args.kwonlyargs)}
        called: set[str] = set()
        for inner in ast.walk(node):
            targets: list[ast.expr] = []
            if isinstance(inner, ast.Assign):
                targets = list(inner.targets)
            elif isinstance(inner, ast.Delete):
                targets = list(inner.targets)
            for target in targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and target.value.id in parameters
                ):
                    direct.add(name)
            if isinstance(inner, ast.Call):
                if isinstance(inner.func, ast.Name):
                    called.add(inner.func.id)
                elif (
                    isinstance(inner.func, ast.Attribute)
                    and isinstance(inner.func.value, ast.Name)
                    and inner.func.value.id in parameters
                    and inner.func.attr in _MUTATING_METHODS
                ):
                    direct.add(name)
        calls[name] = called

    mutating = set(direct)
    changed = True
    while changed:
        changed = False
        for name, called in calls.items():
            if name not in mutating and called & mutating:
                mutating.add(name)
                changed = True
    return frozenset(name for name in mutating if not name.startswith("_"))


def _guarded_writers() -> frozenset[str]:
    return _byte_writers_by_annotation() - rbxml.UNGOVERNED_WRITERS


def probe_buffer_mutation(buf: "bytes | bytearray", marker: bytes) -> None:
    """The shape both readings once missed, a permissive annotation and a METHOD mutation."""
    buf.extend(marker)  # type: ignore[union-attr]


def test_both_readings_catch_a_buffer_mutated_through_a_method_call():
    """The hole that made the coverage claim false, pinned from both sides."""
    source = inspect.getsource(probe_buffer_mutation)
    assert "probe_buffer_mutation" in _byte_writers_by_source(source), (
        "the syntax walk sees only subscript writes, so a method call is invisible"
    )
    assert "probe_buffer_mutation" in _byte_writers_by_annotation(
        {"probe_buffer_mutation": probe_buffer_mutation}
    ), "the signature reading demands an exact annotation, so a union slips past"


def test_the_two_readings_of_what_writes_bytes_agree():
    """P4: the two readings agree, since the coverage claim rests on a complete emitter set."""
    by_annotation = _byte_writers_by_annotation()
    by_source = _byte_writers_by_source()
    assert by_annotation == by_source, (
        f"declared writers not seen mutating: {sorted(by_annotation - by_source)}; "
        f"mutating but not declared: {sorted(by_source - by_annotation)}"
    )
    assert by_annotation, "no byte writers were derived at all; the walk is broken"


def test_the_ungoverned_writers_are_a_real_subset_and_take_no_tree():
    """The declared exceptions exist and cannot name a tree, so the guarded set never shrinks."""
    writers = _byte_writers_by_annotation()
    assert rbxml.UNGOVERNED_WRITERS <= writers, (
        f"declared ungoverned but not a byte writer: "
        f"{sorted(rbxml.UNGOVERNED_WRITERS - writers)}"
    )
    for name in rbxml.UNGOVERNED_WRITERS:
        parameters = inspect.signature(getattr(rbxml, name)).parameters
        assert "tree" not in parameters, f"{name} can name a tree, so it must be guarded"


def test_every_guarded_writer_accepts_the_tree_the_guard_is_keyed_on():
    for name in _guarded_writers():
        parameters = inspect.signature(getattr(rbxml, name)).parameters
        assert "tree" in parameters, f"{name} writes a tree and cannot be told which"
        assert parameters["tree"].default is None, (
            f"{name} must default to an ungoverned write, since most playlists in "
            f"a real library are governed by nothing"
        )


#: One call per guarded emitter, asserted to be EXACTLY the derived guarded set below.
_CALLABLE_EMITTERS = frozenset(
    {
        "splice_into_subplaylist",
        "remove_tracks_from_subplaylist",
        "insert_genre_folder",
        "insert_empty_subplaylist",
        "insert_catalog_folder",
        "remove_folder_node",
        "insert_intake_playlist",
    }
)


def _invoke(name: str, content: bytearray, tree: rbxml.Tree | None):
    """Drive one emitter so it CHANGES the fixture, or the guard assertions prove nothing."""
    if name == "splice_into_subplaylist":
        return rbxml.splice_into_subplaylist(
            content, FOLDER_DISPLAY, SUB_DISPLAY, [901], tree=tree
        )
    if name == "remove_tracks_from_subplaylist":
        return rbxml.remove_tracks_from_subplaylist(
            content, FOLDER_DISPLAY, SUB_DISPLAY, [SEEDED_TRACK], tree=tree
        )
    if name == "insert_genre_folder":
        return rbxml.insert_genre_folder(content, NEW_FOLDER, [SUB_DISPLAY], tree=tree)
    if name == "insert_empty_subplaylist":
        # A name the fixture lacks, since the seeded one is an idempotent no-op.
        return rbxml.insert_empty_subplaylist(
            content, FOLDER_DISPLAY, NEW_PLAYLIST, tree=tree
        )
    if name == "insert_catalog_folder":
        return rbxml.insert_catalog_folder(
            content, NEW_FOLDER, [(NEW_PLAYLIST, [901])], tree=tree
        )
    if name == "remove_folder_node":
        return rbxml.remove_folder_node(content, FOLDER_DISPLAY, tree=tree)
    if name == "insert_intake_playlist":
        return rbxml.insert_intake_playlist(content, NEW_PLAYLIST, [901], tree=tree)
    raise KeyError(name)


def test_every_guarded_emitter_is_actually_exercised():
    """P3 on the fixtures: every derived emitter is in the table that drives it."""
    assert _CALLABLE_EMITTERS == _guarded_writers(), (
        f"emitters with no call fixture: {sorted(_guarded_writers() - _CALLABLE_EMITTERS)}; "
        f"fixtures for something that is not an emitter: "
        f"{sorted(_CALLABLE_EMITTERS - _guarded_writers())}"
    )


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_a_byte_write_at_a_database_native_tree_is_refused_by_name(emitter):
    """The plan's first scenario, for EVERY emitter, naming the tree that stopped it."""
    content = bytearray(_tree_doc())
    before = bytes(content)
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        _invoke(emitter, content, _governed(tree_registry.Mode.DATABASE))
    assert TREE_ID in str(excinfo.value), "the refusal did not name the tree"
    assert excinfo.value.tree_id == TREE_ID
    assert bytes(content) == before, f"{emitter} wrote bytes before refusing"


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_a_byte_write_at_a_tree_still_on_the_bridge_passes(emitter):
    """The other half, and the document must actually CHANGE."""
    content = bytearray(_tree_doc())
    before = bytes(content)
    _invoke(emitter, content, _governed(tree_registry.Mode.XML))
    assert bytes(content) != before, f"{emitter} was driven into doing nothing"
    assert _no_bare_lf(bytes(content))


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_an_ungoverned_playlist_bypasses_the_guard_entirely(emitter):
    """P7: a playlist nobody governs bypasses the guard, or the guard gets switched off."""
    content = bytearray(_tree_doc())
    _invoke(emitter, content, None)
    assert _no_bare_lf(bytes(content))

    named_but_ungoverned = rbxml.Tree(display=TREE_DISPLAY)
    assert named_but_ungoverned.governed is False
    other = bytearray(_tree_doc())
    _invoke(emitter, other, named_but_ungoverned)
    assert _no_bare_lf(bytes(other))


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_an_all_xml_registry_changes_not_one_byte(emitter):
    """The registry decides whether a write happens, never what it writes."""
    ungoverned = bytearray(_tree_doc())
    _invoke(emitter, ungoverned, None)
    governed = bytearray(_tree_doc())
    _invoke(emitter, governed, _governed(tree_registry.Mode.XML))
    assert bytes(governed) == bytes(ungoverned)


def test_a_tree_cannot_carry_an_identifier_without_the_registry_that_governs_it():
    """Half a governed tree would pass the guard by default, which is the hole itself."""
    with pytest.raises(ValueError, match="pass by default"):
        rbxml.Tree(display=TREE_DISPLAY, id=TREE_ID)
    with pytest.raises(ValueError, match="pass by default"):
        rbxml.Tree(display=TREE_DISPLAY, registry=tree_registry.EMPTY)


def _two_tree_doc() -> bytes:
    """Two trees told apart by nothing but the tree."""
    return _playlists(
        '      <NODE Name="Other Shelf" Type="0" Count="1">',
        f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
        *_sub_lines(),
        "        </NODE>",
        "      </NODE>",
        f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">',
        f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
        *_sub_lines(),
        "        </NODE>",
        "      </NODE>",
    )


def test_a_governed_tree_scopes_the_folder_search_to_its_own_subtree():
    """Naming the tree narrows the anchor, as two trees may hold folders of one name."""
    content = bytearray(_two_tree_doc())
    result = rbxml.splice_into_subplaylist(
        content, FOLDER_DISPLAY, SUB_DISPLAY, [901], tree=_governed(tree_registry.Mode.XML)
    )
    assert result.warning is None and result.inserted == 1
    out = bytes(content)
    # The write landed in the SECOND tree, so the first one still reads one.
    first = out.index(b'Name="Other Shelf"')
    second = out.index(_esc(TREE_DISPLAY).encode("utf-8"))
    assert b'Entries="1"' in out[first:second]
    assert b'Entries="2"' in out[second:]


def test_a_governed_tree_scopes_a_REMOVAL_to_its_own_subtree_too():
    """The same narrowing on the writer that DELETES, where a wrong tree goes unseen."""
    content = bytearray(_two_tree_doc())
    removed, warning = rbxml.remove_tracks_from_subplaylist(
        content,
        FOLDER_DISPLAY,
        SUB_DISPLAY,
        [SEEDED_TRACK],
        tree=_governed(tree_registry.Mode.XML),
    )
    assert warning is None and removed == 1
    out = bytes(content)
    first = out.index(b'Name="Other Shelf"')
    second = out.index(_esc(TREE_DISPLAY).encode("utf-8"))
    assert f'<TRACK Key="{SEEDED_TRACK}"/>'.encode("utf-8") in out[first:second], (
        "the removal reached into the tree it was not given"
    )
    assert b'Entries="1"' in out[first:second]
    assert f'<TRACK Key="{SEEDED_TRACK}"/>'.encode("utf-8") not in out[second:]
    assert b'Entries="0"' in out[second:]


# The inverse check, and the skew a mode alone cannot see


def test_a_database_writer_refuses_a_tree_still_marked_xml():
    """The plan's second scenario: until cutover the export owns the tree."""
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        tree_registry.refuse_database_write(TREE_ID, _registry(tree_registry.Mode.XML))
    assert excinfo.value.tree_id == TREE_ID
    assert excinfo.value.attempted == tree_registry.Mode.DATABASE
    # And an unrecorded tree is the same answer, since unrecorded means the bridge.
    with pytest.raises(tree_registry.TreeModeRefused):
        tree_registry.refuse_database_write(TREE_ID, tree_registry.EMPTY)


def test_a_database_writer_passes_once_the_cutover_is_recorded():
    tree_registry.refuse_database_write(TREE_ID, _registry(tree_registry.Mode.DATABASE))


def test_the_anchored_root_is_returned_when_the_library_actually_has_it():
    found = tree_registry.anchored_root(
        TREE_ID,
        _registry(tree_registry.Mode.DATABASE),
        root_exists=lambda root_id: root_id == ADOPTED_ROOT,
    )
    assert found == ADOPTED_ROOT


def test_a_restored_pre_cutover_database_refuses_rather_than_forking_the_tree():
    """A restored pre-cutover database refuses, as the mode alone would fork the root."""
    with pytest.raises(tree_registry.RegistrySkew) as excinfo:
        tree_registry.anchored_root(
            TREE_ID,
            _registry(tree_registry.Mode.DATABASE),
            root_exists=lambda root_id: False,
        )
    assert excinfo.value.tree_id == TREE_ID
    assert excinfo.value.root_id == ADOPTED_ROOT
    assert "second tree" in str(excinfo.value)


def test_the_anchor_check_refuses_a_tree_on_the_bridge_before_it_looks_anything_up():
    """Three failures, three refusals, the bridge checked before any lookup."""
    looked_up = []

    def watcher(root_id):
        looked_up.append(root_id)
        return True

    with pytest.raises(tree_registry.TreeModeRefused):
        tree_registry.anchored_root(
            TREE_ID, _registry(tree_registry.Mode.XML), root_exists=watcher
        )
    assert looked_up == []


def _calls(module: ast.Module):
    """Every call in a module by the name it calls, an attribute's or a bare name's."""
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            yield node.func.attr, node
        elif isinstance(node.func, ast.Name):
            yield node.func.id, node


def _called_names(module: ast.Module) -> set[str]:
    """Every name CALLED in a module, since a mere mention could be a local duplicate."""
    return {name for name, _node in _calls(module)}


def _imports_module(module: ast.Module, dotted: str) -> bool:
    """True when ``module`` imports ``dotted``, by either import form."""
    package, _, leaf = dotted.rpartition(".")
    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            if any(alias.name == dotted for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            source = node.module or ""
            if source == dotted:
                return True
            if source == package and any(alias.name == leaf for alias in node.names):
                return True
    return False


def test_the_database_tree_writer_uses_the_shared_anchor_assertion():
    """P5: the tree writers CALL the shared assertion, imported from its module."""
    from cratekit.write import trees

    module = ast.parse(Path(trees.__file__).read_text(encoding="utf-8"))
    assert _imports_module(module, "cratekit.core.tree_registry"), (
        "the database tree writers must reach the shared assertion through "
        "cratekit.core.tree_registry, since a check spelled locally is a second "
        "implementation of one rule"
    )
    assert "anchored_root" in _called_names(module), (
        "the database tree writers must assert the anchored root through "
        "cratekit.core.tree_registry.anchored_root before writing membership, "
        "so a restored pre-cutover database refuses rather than forking the tree"
    )


def test_every_bridge_call_in_the_tree_writers_names_the_tree_it_targets():
    """P5: every bridge call passes ``tree=``, since an omitted one is refused by nothing."""
    from cratekit.write import trees

    guarded = _guarded_writers()
    module = ast.parse(Path(trees.__file__).read_text(encoding="utf-8"))
    unnamed = [
        called
        for called, node in _calls(module)
        if called in guarded and not any(kw.arg == "tree" for kw in node.keywords)
    ]
    assert not unnamed, (
        f"these calls into guarded emitters name no tree, so the emitter guard "
        f"cannot fire on any of them: {sorted(set(unnamed))}"
    )


# KTD14: the pinned intake shape, and the depth the bridge cannot express


def test_a_taxonomy_nesting_deeper_than_the_bridge_encodes_is_refused_by_name():
    """The plan's third scenario, refused rather than written at an unfindable indent."""
    declared = taxonomy.default_taxonomy()
    deeper = replace(declared, tree_depth=rbxml.TREE_DEPTH + 1)
    with pytest.raises(rbxml.TreeTooDeep) as excinfo:
        rbxml.assert_bridge_can_serve(deeper)
    message = str(excinfo.value)
    assert declared.tree.id in message
    assert str(rbxml.TREE_DEPTH) in message and str(rbxml.TREE_DEPTH + 1) in message
    with pytest.raises(rbxml.TreeTooDeep):
        rbxml.routing_tree(deeper, tree_registry.EMPTY)


def test_the_depth_the_bridge_encodes_and_the_depth_a_template_may_declare_are_one():
    """Two modules that cannot import each other share one depth, pinned here."""
    assert rbxml.TREE_DEPTH == taxonomy.SUPPORTED_TREE_DEPTH


def test_the_bridge_refuses_only_deeper_and_the_template_loader_owns_the_rest():
    """The bridge refuses only deeper, and the template loader owns the rest."""
    declared = taxonomy.default_taxonomy()
    shallower = replace(declared, tree_depth=rbxml.TREE_DEPTH - 1)
    rbxml.assert_bridge_can_serve(shallower)
    assert rbxml.routing_tree(shallower, tree_registry.EMPTY).display == (
        declared.tree.display
    )


def test_the_intake_tree_is_pinned_and_survives_a_taxonomy_the_bridge_refuses():
    """KTD14: intake is pinned, so a taxonomy the bridge refuses still has an intake tree."""
    declared = taxonomy.default_taxonomy()
    deeper = replace(declared, tree_depth=rbxml.TREE_DEPTH + 4)
    intake = rbxml.intake_tree(deeper, tree_registry.EMPTY)
    assert intake.display == declared.intake.display
    assert rbxml.INTAKE_DEPTH < rbxml.TREE_DEPTH


def test_the_two_tree_constructors_cannot_produce_an_ungoverned_tree_by_default():
    """No default registry, which would make an ungoverned tree pass in silence."""
    declared = taxonomy.default_taxonomy()
    for factory in (rbxml.routing_tree, rbxml.intake_tree):
        with pytest.raises(TypeError):
            factory(declared)
        assert factory(declared, tree_registry.EMPTY).governed
    with pytest.raises(TypeError):
        rbxml.tree_for(declared.tree)
    assert rbxml.tree_for(declared.tree, tree_registry.EMPTY).governed


def test_the_intake_playlist_lands_at_the_pinned_indent():
    """The pinned shape as bytes, derived from the pinned depth."""
    doc = _playlists(
        f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="0">',
        "      </NODE>",
    )
    content = bytearray(doc)
    assert rbxml.insert_intake_playlist(content, NEW_PLAYLIST, [901, 902]) is None
    out = bytes(content)
    assert (
        f'        <NODE Name="{_esc(NEW_PLAYLIST)}" Type="1" KeyType="0" Entries="2">'
    ).encode("utf-8") in out
    assert b'          <TRACK Key="901"/>\r\n' in out
    assert b'      </NODE>\r\n' in out
    assert b'Count="1"' in out, "the tree's child count was not bumped"
    assert _no_bare_lf(out)


def test_a_second_intake_run_replaces_rather_than_duplicating():
    """Every write is re-runnable, so none appends a second copy."""
    doc = _playlists(
        f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="0">',
        "      </NODE>",
    )
    content = bytearray(doc)
    rbxml.insert_intake_playlist(content, NEW_PLAYLIST, [901])
    once = bytes(content)
    rbxml.insert_intake_playlist(content, NEW_PLAYLIST, [902])
    twice = bytes(content)
    assert twice.count(_esc(NEW_PLAYLIST).encode("utf-8")) == 1
    assert b'Key="902"' in twice and b'Key="901"' not in twice
    assert once.count(b'Count="1"') == twice.count(b'Count="1"')
    assert _no_bare_lf(twice)


def test_the_indent_derivation_reproduces_the_pinned_widths():
    """The derivation must land on the widths every splice anchors on."""
    assert [rbxml.indent_at(depth) for depth in range(5)] == [4, 6, 8, 10, 12]
    assert rbxml.SUB_CLOSE_INDENT == 10
    assert rbxml.TRACK_INDENT == 12
    with pytest.raises(ValueError):
        rbxml.indent_at(-1)


# The consolidated locates: every shape the old call sites used

#: THE INVENTORY: every byte-level LOCATE shape in the replaced system and the primitive
#: covering it, so no call site needs a scan of its own.
LOCATE_SHAPES: dict[str, tuple[str, ...]] = {
    "the playlist section's bounds, so no name search begins at byte zero": (
        "playlists_span",
        "playlists_start",
    ),
    "the collection's bounds, for track element locates": ("collection_span",),
    "a node found by its name attribute, from an explicit anchor": ("find_node",),
    "a node found by a full open tag with its attributes in ONE fixed order, and "
    "the same node found with them in the OTHER order": ("find_node", "attributes"),
    "the open tag's bounds and whether it closes itself": ("node_at",),
    "the matching close tag, by walking node pairs rather than counting closes": (
        "matching_close",
    ),
    "a node's DIRECT children, rather than every descendant": ("child_nodes",),
    "the whole tree indexed by display path, for a document-to-document diff": (
        "walk_nodes",
    ),
    "the line a tag starts on, for splices that include the leading break": (
        "line_start",
    ),
    "the track keys a playlist currently holds, in document order": ("track_keys",),
    "one track key LINE, tolerating the bare LF an old splicer wrote": (
        "track_key_line",
    ),
    "one collection track element, matched on its id exactly and bounded by its "
    "real close rather than by the next self-closing token": (
        "find_collection_track",
        "collection_tracks",
    ),
    "one attribute's value inside an already located tag, patched in the original "
    "bytes rather than re-emitted from a template": (
        "attribute_span",
        "patch_attribute",
    ),
}


def test_every_locate_shape_names_a_primitive_that_exists():
    """The inventory is checked against the module, so no call site invents a scan."""
    for shape, primitives in LOCATE_SHAPES.items():
        for name in primitives:
            assert callable(getattr(rbxml, name, None)), (
                f"the shape {shape!r} names {name!r}, which this module does not provide"
            )


def test_the_section_probe_answers_from_the_document_and_not_from_a_constant():
    """The one cover in the inventory nothing else exercises."""
    doc = _tree_doc()
    assert rbxml.playlists_start(doc) == doc.index(b"<PLAYLISTS>")
    assert rbxml.playlists_start(b"<DJ_PLAYLISTS>\r\n</DJ_PLAYLISTS>\r\n") == -1


def test_a_raw_angle_bracket_in_a_display_name_does_not_unanchor_the_document():
    """A legal '>' in a name must not end an open tag and misplace a splice."""
    doc = _playlists(
        f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="2">',
        f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
        '          <NODE Name="Warmup > Peak" Type="1" KeyType="0" Entries="0"/>',
        "        </NODE>",
        '        <NODE Name="Quiet Room" Type="0" Count="1">',
        f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
        "        </NODE>",
        "      </NODE>",
    )
    root = rbxml.root_node(doc)
    assert root is not None, "one unescaped angle bracket un-anchored the whole document"
    assert [child.name for child in rbxml.child_nodes(doc, root)] == [TREE_DISPLAY]

    content = bytearray(doc)
    result = rbxml.splice_into_subplaylist(content, FOLDER_DISPLAY, SUB_DISPLAY, [901])
    assert result.warning is not None and result.inserted == 0, (
        "the sub belongs to the OTHER folder, so this must warn rather than write"
    )
    assert bytes(content) == doc


def test_a_name_search_is_never_allowed_to_default_to_byte_zero():
    """``start`` has no default, so the historic mis-anchor cannot be written by accident."""
    parameters = inspect.signature(rbxml.find_node).parameters
    assert parameters["start"].default is inspect.Parameter.empty


def test_the_locates_read_attributes_in_either_order():
    """Attribute order differs between writers, and a miss reads as a successful sweep."""
    doc = _playlists(
        f'      <NODE Type="0" Name="{_esc(TREE_DISPLAY)}" Count="1">',
        f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="0"/>',
        "      </NODE>",
    )
    span = rbxml.playlists_span(doc)
    assert span is not None
    tree_node = rbxml.find_node(
        doc, TREE_DISPLAY, start=span[0], end=span[1], node_type=rbxml.FOLDER_TYPE
    )
    assert tree_node is not None and tree_node.name == TREE_DISPLAY
    assert rbxml.attributes(doc, tree_node) == {
        "Type": "0",
        "Name": TREE_DISPLAY,
        "Count": "1",
    }
    children = rbxml.child_nodes(doc, tree_node)
    assert [child.name for child in children] == [FOLDER_DISPLAY]
    assert children[0].self_closing


def test_the_escaper_and_its_inverse_round_trip_every_character_class():
    """D1: a name read back must equal the name passed in, or idempotency stops matching."""
    for name in (TREE_DISPLAY, FOLDER_DISPLAY, SUB_DISPLAY, SUB_DISPLAY_NFD, NEW_PLAYLIST):
        assert rbxml.xml_unescape_attr(rbxml.xml_escape_attr(name)) == name
    assert rbxml.xml_escape_attr("a & b") == "a &amp; b"
    assert rbxml.xml_unescape_attr("&amp;lt;") == "&lt;", (
        "the ampersand must be undone last, or an escaped ampersand becomes a tag"
    )


def test_the_two_composition_forms_are_two_different_nodes():
    """A BYTE splicer finds the bytes given, so folding forms is the locations module's job."""
    doc = _playlists(
        f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="2">',
        f'        <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
        f'        <NODE Name="{_esc(SUB_DISPLAY_NFD)}" Type="1" KeyType="0" Entries="0"/>',
        "      </NODE>",
    )
    assert SUB_DISPLAY != SUB_DISPLAY_NFD
    span = rbxml.playlists_span(doc)
    assert span is not None
    precomposed = rbxml.find_node(doc, SUB_DISPLAY, start=span[0], end=span[1])
    decomposed = rbxml.find_node(doc, SUB_DISPLAY_NFD, start=span[0], end=span[1])
    assert precomposed is not None and decomposed is not None
    assert precomposed.tag_start != decomposed.tag_start


def test_the_tree_walk_reports_a_display_path_for_every_node():
    """The index a document diff needs, built once rather than by counting indents."""
    doc = _tree_doc()
    root = rbxml.root_node(doc)
    assert root is not None
    walked = list(rbxml.walk_nodes(doc, root))
    assert [path for path, _ in walked] == [
        (TREE_DISPLAY,),
        (TREE_DISPLAY, FOLDER_DISPLAY),
        (TREE_DISPLAY, FOLDER_DISPLAY, SUB_DISPLAY),
    ]
    assert [node.depth for _, node in walked] == [1, 2, 3]
    assert [rbxml.indent_at(node.depth) for _, node in walked] == [6, 8, 10]


def test_a_collection_track_is_bounded_by_its_real_close_not_the_next_slash_bracket():
    """A track is bounded by its own close tag, so a patch never rewrites rekordbox's data."""
    doc = _xml_doc(
        collection=[
            '  <COLLECTION Entries="2">',
            *_ml_track(101, "One Track", analyzed=True),
            *_ml_track(102, "Two Track"),
            "  </COLLECTION>",
        ],
        root_children=['      <NODE Name="Anything" Type="0" Count="0">', "      </NODE>"],
    )
    found = rbxml.find_collection_track(doc, 101)
    assert found is not None and not found.self_closing
    assert doc[found.end - len(b"</TRACK>") : found.end] == b"</TRACK>"
    assert rbxml.attributes(doc, found)["Name"] == "One Track"
    assert [track.track_id for track in rbxml.collection_tracks(doc)] == ["101", "102"]


def test_a_track_id_never_matches_a_longer_one():
    doc = _xml_doc(
        collection=[
            '  <COLLECTION Entries="2">',
            '    <TRACK TrackID="42" Name="a" Rating="0" Location="file://localhost/a.flac"/>',
            '    <TRACK TrackID="421" Name="b" Rating="0" Location="file://localhost/b.flac"/>',
            "  </COLLECTION>",
        ],
        root_children=['      <NODE Name="Anything" Type="0" Count="0">', "      </NODE>"],
    )
    found = rbxml.find_collection_track(doc, 42)
    assert found is not None and rbxml.attributes(doc, found)["Name"] == "a"


def test_an_attribute_patch_never_reaches_into_the_next_element():
    """A patch never scans into the FOLLOWING track for an attribute this one lacks."""
    without_rating = [
        '    <TRACK TrackID="700" Name="No Rating Here" Artist="A"',
        '           Location="file://localhost/x.flac" Mix="">',
        "    </TRACK>",
    ]
    with_rating = [
        '    <TRACK TrackID="701" Name="Has One" Artist="A" Rating="0"',
        '           Location="file://localhost/y.flac" Mix="">',
        "    </TRACK>",
    ]
    content = bytearray(
        _xml_doc(
            collection=['  <COLLECTION Entries="2">', *without_rating, *with_rating,
                        "  </COLLECTION>"],
            root_children=['      <NODE Name="Anything" Type="0" Count="0">',
                           "      </NODE>"],
        )
    )
    before = bytes(content)
    assert rbxml.apply_rating_changes({700: 255}, content) == 0
    assert bytes(content) == before, "the patch reached into the following element"


def test_rekordbox_authored_analysis_survives_a_rating_patch_verbatim():
    """R17's other half: never create a grid, and never destroy one either."""
    analysed = _ml_track(101, "One Track", analyzed=True)
    grid_line = next(line for line in analysed if line.strip().startswith("<TEMPO"))
    content = bytearray(
        _xml_doc(
            collection=[
                '  <COLLECTION Entries="1">',
                *[
                    line.replace(' Tonality=', ' Rating="0" Tonality=')
                    if "Tonality=" in line
                    else line
                    for line in analysed
                ],
                "  </COLLECTION>",
            ],
            root_children=['      <NODE Name="Anything" Type="0" Count="0">',
                           "      </NODE>"],
        )
    )
    assert rbxml.apply_rating_changes({101: 255}, content) == 1
    out = bytes(content)
    assert b'Rating="255"' in out
    assert grid_line.encode("utf-8") in out, "rekordbox-authored analysis was disturbed"
    assert _no_bare_lf(out)


def test_a_missing_section_is_a_warning_and_never_a_corrupting_slice():
    """Every failure returns a warning, since a -1 slice writes to the wrong place."""
    content = bytearray(b"<DJ_PLAYLISTS>\r\n</DJ_PLAYLISTS>\r\n")
    before = bytes(content)
    result = rbxml.splice_into_subplaylist(content, FOLDER_DISPLAY, SUB_DISPLAY, [1])
    assert result.warning is not None and result.inserted == 0
    assert rbxml.insert_root_playlist(NEW_PLAYLIST, [1], content) is not None
    assert rbxml.insert_genre_folder(content, NEW_FOLDER, []) is not None
    assert rbxml.remove_folder_node(content, NEW_FOLDER) is not None
    assert bytes(content) == before


def test_an_unnamed_tree_is_inferred_only_when_there_is_exactly_one():
    """Guessing among several would put a folder inside whichever came first.

    So the inference is refused by name instead, and the message says how many it
    found.
    """
    two_trees = bytearray(
        _playlists(
            '      <NODE Name="Shelf One" Type="0" Count="0">',
            "      </NODE>",
            '      <NODE Name="Shelf Two" Type="0" Count="0">',
            "      </NODE>",
        )
    )
    before = bytes(two_trees)
    warning = rbxml.insert_genre_folder(two_trees, NEW_FOLDER, [])
    assert warning is not None and "cannot be inferred" in warning
    assert bytes(two_trees) == before
