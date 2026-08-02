"""U17: per-tree write medium, the two guards, and the locate set that makes the
guards' coverage claim true.

FOUR THINGS ARE PROVED HERE, AND THEY FAIL IN FOUR DIFFERENT WAYS.

1. **The registry is library-scoped state that starts entirely on the bridge.**
   The failure it prevents is a shipped repository carrying one person's cutover
   flips and one person's row identifiers, which every friend who clones then
   writes against.

2. **The byte bridge refuses a tree the database owns, for EVERY emitter.** The
   emitter set is DERIVED from the module twice, by two independent readings, and
   the two must agree. A hand-listed emitter set is a set that misses the next
   emitter, and the next emitter would then ship unguarded with a green build.

3. **The database side refuses the inverse, and refuses a registry the database
   disagrees with.** A mode alone cannot tell a library that has cut over from a
   library restored from before the cutover, and writing to the second one
   creates a silent parallel tree.

4. **The locates are consolidated, so the guard cannot be routed around.** A call
   site that can find a node can splice into it without calling any writer, so
   the shapes the old call sites used are enumerated below and each one is proved
   expressible with the primitives here.

A NOTE ON THE FIXTURES. Every display name in this file is synthesized (D1).
Between them they carry a space, a literal exclamation mark, an ampersand, and an
accented character in both composition forms, which is the character coverage the
escaper and the locates actually have to survive. None of them names a real
volume, a real person, or a real track.
"""

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
from tests._pending import requires
from tests.xml_fixtures import _ml_track, _no_bare_lf, _xml_doc

REPO_ROOT = Path(__file__).resolve().parent.parent


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


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
    """Run the body under umask 000, then put the process back.

    A test that does not manipulate the umask cannot see this defect at all: on
    a machine with umask 022 a plain write lands 0644, which looks fine right up
    until somebody with a laxer umask runs the same code.
    """
    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


# ── synthesized display names (D1) ───────────────────────────────────────────

#: A tree name carrying an ampersand, which the escaper has to encode and the
#: marker builder has to encode identically or the locate misses the node.
TREE_DISPLAY = "Shelf & Stack"
#: A folder name carrying a literal exclamation mark and a space.
FOLDER_DISPLAY = "Loud! Room"
#: A sub-playlist name carrying an accented character, PRECOMPOSED.
SUB_DISPLAY = "Café Nights"
#: The same name DECOMPOSED. macOS stores filenames this way and rekordbox stores
#: them the other way, so the two forms turn up in one document routinely.
SUB_DISPLAY_NFD = unicodedata.normalize("NFD", SUB_DISPLAY)

TREE_ID = "shelf_stack"
NEW_FOLDER = "Quiet? Corner"
NEW_PLAYLIST = "Batch 001 & 002"

CUTOVER_ON = date(2026, 8, 1)
ADOPTED_ROOT = "root-row-7788"


def _esc(value: str) -> str:
    return rbxml.xml_escape_attr(value)


def _tree_doc() -> bytes:
    """One tree holding one folder holding one empty sub-playlist."""
    return _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
        ],
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
                ),
            )
        )
    return tree_registry.Registry((tree_registry.TreeRecord(tree_id=TREE_ID, mode=mode),))


def _governed(mode: tree_registry.Mode) -> rbxml.Tree:
    return rbxml.Tree(display=TREE_DISPLAY, id=TREE_ID, registry=_registry(mode))


# ═══════════════════════════════════════════════════════════════════════════
# The registry: what it holds, where it lives, how it starts
# ═══════════════════════════════════════════════════════════════════════════


def test_every_tree_starts_on_the_bridge_and_that_is_not_a_setting(cfg):
    """The plan's default, asserted from three directions.

    A library with no registry file, a registry with no record for a tree, and a
    record written with no explicit mode all resolve to the bridge. Anything else
    would mean a fresh install could be talked into writing a tree natively before
    that tree had ever been adopted.
    """
    assert tree_registry.DEFAULT_MODE is tree_registry.Mode.XML
    assert tree_registry.read(cfg) is tree_registry.EMPTY
    assert tree_registry.read(cfg).mode("anything_at_all") is tree_registry.Mode.XML
    assert tree_registry.TreeRecord(tree_id=TREE_ID).mode is tree_registry.Mode.XML
    assert tree_registry.EMPTY.is_on_the_bridge(TREE_ID)


def test_a_record_carries_the_mode_the_date_and_the_adopted_root(cfg):
    """All three, because a mode alone cannot detect skew.

    The date places the flip against the snapshots either side of it, and the
    adopted root is what a later write compares the live library against.
    """
    tree_registry.record_cutover(cfg, TREE_ID, root_id=ADOPTED_ROOT, on=CUTOVER_ON)
    record = tree_registry.read(cfg).record(TREE_ID)
    assert record is not None
    assert record.mode is tree_registry.Mode.DATABASE
    assert record.cutover_on == CUTOVER_ON
    assert record.root_id == ADOPTED_ROOT


def test_a_native_record_without_an_adopted_root_cannot_be_constructed():
    """Refused at construction, not at the write that would have needed it.

    A record that says native and names nothing is indistinguishable from a
    library that never cut over, so the writer would create a root and report
    success.
    """
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
    tree_registry.record_cutover(cfg, "first_tree", root_id="root-1", on=CUTOVER_ON)
    tree_registry.record_cutover(cfg, "second_tree", root_id="root-2", on=CUTOVER_ON)
    after = tree_registry.read(cfg)
    assert after.tree_ids() == ("first_tree", "second_tree")
    assert after.is_database_native("first_tree")
    assert after.is_database_native("second_tree")


def test_the_persisted_record_is_keyed_on_the_identifier_not_the_display_name(cfg):
    """R19 and D5, asserted against the BYTES rather than against the API.

    The failure is concrete: rename a folder in rekordbox and every record keyed
    on its old name is orphaned, and an orphaned record reads as "still on the
    bridge", which sends the next write to the wrong medium.
    """
    tree_registry.record_cutover(cfg, TREE_ID, root_id=ADOPTED_ROOT, on=CUTOVER_ON)
    raw = tree_registry.path_for(cfg).read_text(encoding="utf-8")
    assert TREE_ID in raw
    assert TREE_DISPLAY not in raw, "a display name reached the persisted record"
    parsed = json.loads(raw)
    assert [entry["tree"] for entry in parsed["trees"]] == [TREE_ID]


def test_the_state_entry_is_library_scoped_coupled_and_never_committed():
    """KTD22 in the three places it has to hold at once.

    Library-scoped so a second installation reads the same answer, COUPLED so a
    snapshot rolls it back with the database it describes, and ignored by git so
    it cannot ship. The plan's top-ranked risk is this entry's snapshot coupling,
    so it is asserted rather than assumed.
    """
    entry = config.state_file(tree_registry.STATE_KEY)
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.snapshot is config.SnapshotRole.COUPLED
    assert entry in config.coupled_state_files()
    ignored = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert entry.relative in ignored


def test_the_registry_file_and_the_directories_it_creates_are_private(
    permissive_umask, cfg
):
    """P1: the file mode is meaningless without the directory mode.

    A 0600 file inside a world-writable directory can be unlinked and replaced by
    any local account, because unlink and rename are governed by the directory.
    Whoever replaces this file decides which writer runs against a real library.
    """
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
    """P2: a check and a consumer must never disagree about their input.

    The configuration FILE names one library root and the environment relocates
    it to another. A reader that composed its path from the file's value would
    read a registry the writers never touch, and the two would then disagree about
    which medium owns a tree, which is the shape that produced a config file
    validating clean while violating its own invariant.
    """
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
    config.atomic_write_bytes(
        json.dumps(
            {
                "schema_version": tree_registry.SCHEMA_VERSION,
                "trees": [
                    {
                        "tree": TREE_ID,
                        "mode": "database",
                        "cutover_on": CUTOVER_ON.isoformat(),
                        "root": ADOPTED_ROOT,
                    }
                ],
            }
        ).encode("utf-8"),
        decoy,
    )
    tree_registry.write(effective, _registry(tree_registry.Mode.XML))

    assert tree_registry.path_for(effective) != decoy
    assert tree_registry.read(effective).is_on_the_bridge(TREE_ID), (
        "the registry was read from the file's library root rather than the effective one"
    )


# ── reading a file this build cannot vouch for ───────────────────────────────


def test_an_unreadable_registry_is_its_own_answer_and_not_an_empty_one(cfg):
    """Collapsing this into "no record" would read as "everything is on the bridge".

    That is the single misreading that sends a byte write at a tree the database
    already owns, so the unreadable case has to refuse rather than default.
    """
    path = tree_registry.path_for(cfg)
    config.atomic_write_bytes(b"{ not json", path)
    with pytest.raises(tree_registry.TreeRegistryUnreadable) as excinfo:
        tree_registry.read(cfg)
    assert excinfo.value.path == path
    assert excinfo.value.remedy is not None


def test_a_registry_from_a_newer_build_is_refused_rather_than_guessed_at(cfg):
    path = tree_registry.path_for(cfg)
    config.atomic_write_bytes(
        json.dumps({"schema_version": tree_registry.SCHEMA_VERSION + 1, "trees": []}).encode(),
        path,
    )
    with pytest.raises(tree_registry.TreeRegistryUnreadable, match="schema version"):
        tree_registry.read(cfg)


def test_a_record_with_an_unknown_mode_is_refused_rather_than_dropped(cfg):
    """A dropped record reads as "still on the bridge", which is the wrong medium.

    So a mode this build has never heard of fails the whole read rather than
    quietly leaving one tree unaccounted for.
    """
    path = tree_registry.path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(
            {
                "schema_version": tree_registry.SCHEMA_VERSION,
                "trees": [{"tree": TREE_ID, "mode": "carrier-pigeon"}],
            }
        ).encode(),
        path,
    )
    with pytest.raises(tree_registry.TreeRegistryUnreadable, match="unusable record"):
        tree_registry.read(cfg)


def test_the_bytes_are_a_function_of_the_content_alone(cfg):
    """Two writes of the same registry produce identical bytes.

    An unordered dump makes every write a diff even when nothing changed, which
    is noise in exactly the file somebody opens to find out whether anything did.
    """
    registry = tree_registry.EMPTY.with_record(
        tree_registry.TreeRecord(tree_id="zulu")
    ).with_record(tree_registry.TreeRecord(tree_id="alpha"))
    first = tree_registry.write(cfg, registry).read_bytes()
    reversed_order = tree_registry.Registry(tuple(reversed(registry.trees)))
    second = tree_registry.write(cfg, reversed_order).read_bytes()
    assert first == second


# ═══════════════════════════════════════════════════════════════════════════
# The emitter guard, over a DERIVED emitter set (P3), cross-checked (P4)
# ═══════════════════════════════════════════════════════════════════════════


def _public_functions() -> dict[str, object]:
    return {
        name: obj
        for name, obj in vars(rbxml).items()
        if not name.startswith("_")
        and inspect.isfunction(obj)
        and obj.__module__ == rbxml.__name__
    }


def _byte_writers_by_annotation() -> frozenset[str]:
    """Every public function that takes a MUTABLE buffer.

    The first of two independent readings of the same question. A parameter
    annotated ``bytearray`` is a buffer the function may write; the locates take
    ``bytes`` and cannot.
    """
    found = set()
    for name, obj in _public_functions().items():
        for parameter in inspect.signature(obj).parameters.values():
            if parameter.annotation == "bytearray":
                found.add(name)
    return frozenset(found)


def _byte_writers_by_source() -> frozenset[str]:
    """Every public function that mutates a parameter, directly or through another.

    The second reading, and it is deliberately structural rather than declared: a
    function that assigns into or deletes from one of its own parameters is
    writing bytes whatever its annotation says. The transitive step matters,
    because the rating writer mutates nothing itself, it delegates to the shared
    attribute patcher, and a reading that stopped at direct mutation would call
    it a locate.
    """
    tree = ast.parse(Path(rbxml.__file__).read_text(encoding="utf-8"))
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
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                called.add(inner.func.id)
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


def test_the_two_readings_of_what_writes_bytes_agree():
    """P4: a derivation is checked against the thing it must cover, or it is a list.

    Two independent readings of the module, one from the signatures and one from
    the syntax tree. If a writer ever annotates its buffer as immutable, or a
    locate starts mutating, these disagree and this fails, which is the whole
    point: the guard's coverage claim rests on the emitter set being complete.
    """
    by_annotation = _byte_writers_by_annotation()
    by_source = _byte_writers_by_source()
    assert by_annotation == by_source, (
        f"declared writers not seen mutating: {sorted(by_annotation - by_source)}; "
        f"mutating but not declared: {sorted(by_source - by_annotation)}"
    )
    assert by_annotation, "no byte writers were derived at all; the walk is broken"


def test_the_ungoverned_writers_are_a_real_subset_and_take_no_tree():
    """The declared exceptions have to be exceptions to something that exists.

    A stale name here would silently shrink the guarded set, which is exactly how
    a hand-kept list stops guarding. Each one also has to be structurally
    incapable of naming a tree, so it cannot be a governed writer that somebody
    listed here to avoid the argument.
    """
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


#: One call per guarded emitter. The test below asserts these keys are EXACTLY
#: the derived guarded set, so an emitter added without a call here fails the
#: build rather than shipping unexercised.
_CALLABLE_EMITTERS = frozenset(
    {
        "splice_into_subplaylist",
        "remove_tracks_from_subplaylist",
        "insert_root_playlist",
        "insert_genre_folder",
        "remove_folder_node",
        "insert_intake_playlist",
    }
)


def _invoke(name: str, content: bytearray, tree: rbxml.Tree | None):
    """Drive one emitter against the fixture document."""
    if name == "splice_into_subplaylist":
        return rbxml.splice_into_subplaylist(
            content, FOLDER_DISPLAY, SUB_DISPLAY, [901], tree=tree
        )
    if name == "remove_tracks_from_subplaylist":
        return rbxml.remove_tracks_from_subplaylist(
            content, FOLDER_DISPLAY, SUB_DISPLAY, [901], tree=tree
        )
    if name == "insert_root_playlist":
        return rbxml.insert_root_playlist(NEW_PLAYLIST, [901], content, tree=tree)
    if name == "insert_genre_folder":
        return rbxml.insert_genre_folder(content, NEW_FOLDER, [SUB_DISPLAY], tree=tree)
    if name == "remove_folder_node":
        return rbxml.remove_folder_node(content, FOLDER_DISPLAY, tree=tree)
    if name == "insert_intake_playlist":
        return rbxml.insert_intake_playlist(content, NEW_PLAYLIST, [901], tree=tree)
    raise KeyError(name)


def test_every_guarded_emitter_is_actually_exercised():
    """P3 again, on the fixtures rather than on the code.

    Deriving the emitter set is worth nothing if the table that drives it is
    allowed to cover only some of them.
    """
    assert _CALLABLE_EMITTERS == _guarded_writers(), (
        f"emitters with no call fixture: {sorted(_guarded_writers() - _CALLABLE_EMITTERS)}; "
        f"fixtures for something that is not an emitter: "
        f"{sorted(_CALLABLE_EMITTERS - _guarded_writers())}"
    )


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_a_byte_write_at_a_database_native_tree_is_refused_by_name(emitter):
    """The plan's first scenario, for EVERY calling emitter rather than for one.

    The refusal names the tree because a sweep touches several, and a message
    that does not say which one stopped it leaves the reader to guess.
    """
    content = bytearray(_tree_doc())
    before = bytes(content)
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        _invoke(emitter, content, _governed(tree_registry.Mode.DATABASE))
    assert TREE_ID in str(excinfo.value), "the refusal did not name the tree"
    assert excinfo.value.tree_id == TREE_ID
    assert bytes(content) == before, f"{emitter} wrote bytes before refusing"


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_a_byte_write_at_a_tree_still_on_the_bridge_passes(emitter):
    """The other half. A guard that refused everything would also pass the first test."""
    content = bytearray(_tree_doc())
    _invoke(emitter, content, _governed(tree_registry.Mode.XML))
    assert _no_bare_lf(bytes(content))


@pytest.mark.parametrize("emitter", sorted(_CALLABLE_EMITTERS))
def test_an_ungoverned_playlist_bypasses_the_guard_entirely(emitter):
    """P7 in its live form for this unit.

    Most playlists in a real library are somebody's own and this product governs
    none of them. A guard that refused those would fire on correct code, and a
    guard that fires on correct code is switched off, and a switched-off guard
    protects nothing.
    """
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
    """The plan's fifth scenario: goldens are unchanged while everything is on XML.

    Asserted directly as well as through the golden files, because the goldens
    call the emitters with no tree at all and this compares that call against the
    governed one. The registry decides whether a write happens, never what it
    writes.
    """
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


def test_a_governed_tree_scopes_the_folder_search_to_its_own_subtree():
    """Naming the tree narrows the anchor as well as arming the guard.

    Two trees may each hold a folder of the same name, and a search across the
    whole playlist section finds whichever comes first in the document.
    """
    doc = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            '      <NODE Name="Other Shelf" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="1">',
            f'          <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            "        </NODE>",
            "      </NODE>",
        ],
    )
    content = bytearray(doc)
    result = rbxml.splice_into_subplaylist(
        content, FOLDER_DISPLAY, SUB_DISPLAY, [901], tree=_governed(tree_registry.Mode.XML)
    )
    assert result.warning is None and result.inserted == 1
    out = bytes(content)
    # The write landed in the SECOND tree, so the first one still reads zero.
    first = out.index(b'Name="Other Shelf"')
    second = out.index(_esc(TREE_DISPLAY).encode("utf-8"))
    assert b'Entries="0"' in out[first:second]
    assert b'Entries="1"' in out[second:]


# ═══════════════════════════════════════════════════════════════════════════
# The inverse check, and the skew a mode alone cannot see
# ═══════════════════════════════════════════════════════════════════════════


def test_a_database_writer_refuses_a_tree_still_marked_xml():
    """The plan's second scenario.

    Until the cutover is recorded the export owns this tree, so a native write
    lands rows the export knows nothing about and the next import overwrites them.
    """
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
    """The failure the adopted root identifier exists to catch.

    A snapshot taken before the cutover, restored under a registry that was not
    rolled back with it. The mode still says native, so a writer that trusted the
    mode alone would create a second root beside the real one and report success.
    """
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
    """Three failures, three refusals, and the order matters.

    Reporting "no such root" for a tree that has not cut over would send somebody
    looking in the database for a row that was never supposed to exist.
    """
    looked_up = []

    def watcher(root_id):
        looked_up.append(root_id)
        return True

    with pytest.raises(tree_registry.TreeModeRefused):
        tree_registry.anchored_root(
            TREE_ID, _registry(tree_registry.Mode.XML), root_exists=watcher
        )
    assert looked_up == []


@requires("cratekit.write.trees")
def test_the_database_tree_writer_uses_the_shared_anchor_assertion():
    """P5: a docstring saying a later unit will call this is a wish.

    This is the countdown. The moment the tree writers land, this arms and fails
    unless they call the shared assertion rather than hand-rolling their own
    check. Two implementations of one rule is how they come to disagree, and the
    disagreement here costs a user a duplicated tree.
    """
    from cratekit.write import trees

    source = Path(trees.__file__).read_text(encoding="utf-8")
    named = {
        node.attr if isinstance(node, ast.Attribute) else node.id
        for node in ast.walk(ast.parse(source))
        if isinstance(node, (ast.Attribute, ast.Name))
    }
    assert "anchored_root" in named, (
        "the database tree writers must assert the anchored root through "
        "cratekit.core.tree_registry.anchored_root before writing membership, "
        "so a restored pre-cutover database refuses rather than forking the tree"
    )


# ═══════════════════════════════════════════════════════════════════════════
# KTD14: the pinned intake shape, and the depth the bridge cannot express
# ═══════════════════════════════════════════════════════════════════════════


def test_a_taxonomy_nesting_deeper_than_the_bridge_encodes_is_refused_by_name():
    """The plan's third scenario.

    Refused rather than written at an indent no later locate finds, which reads
    to the user as a sweep that ran and changed nothing.
    """
    declared = taxonomy.default_taxonomy()
    deeper = replace(declared, tree_depth=rbxml.TREE_DEPTH + 1)
    with pytest.raises(rbxml.TreeTooDeep) as excinfo:
        rbxml.assert_bridge_can_serve(deeper)
    message = str(excinfo.value)
    assert declared.tree.id in message
    assert str(rbxml.TREE_DEPTH) in message and str(rbxml.TREE_DEPTH + 1) in message
    with pytest.raises(rbxml.TreeTooDeep):
        rbxml.routing_tree(deeper)


def test_a_shallower_taxonomy_is_served_rather_than_refused():
    """The indent is derived from the depth, so a template that drops a dimension
    is a case this serves rather than a case it refuses."""
    declared = taxonomy.default_taxonomy()
    shallower = replace(declared, tree_depth=rbxml.TREE_DEPTH - 1)
    rbxml.assert_bridge_can_serve(shallower)
    assert rbxml.routing_tree(shallower).display == declared.tree.display


def test_the_intake_tree_is_pinned_and_survives_a_taxonomy_the_bridge_refuses():
    """KTD14, and it is the whole reconciliation.

    Intake is one folder holding one playlist per arriving batch. Its shape is
    fixed here, so a taxonomy whose ROUTING tree the bridge cannot express still
    has a working intake tree, and a user definable taxonomy costs nothing.
    """
    declared = taxonomy.default_taxonomy()
    deeper = replace(declared, tree_depth=rbxml.TREE_DEPTH + 4)
    intake = rbxml.intake_tree(deeper)
    assert intake.display == declared.intake.display
    assert rbxml.INTAKE_DEPTH < rbxml.TREE_DEPTH


def test_the_intake_playlist_lands_at_the_pinned_indent():
    """The pinned shape, asserted as bytes.

    One folder, its playlists one level in, their track keys one level further.
    Derived from the pinned depth rather than from three constants, so this test
    fails if either the derivation or the pin moves.
    """
    doc = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="0">',
            "      </NODE>",
        ],
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
    """Every write here is re-runnable, so none of them appends a second copy.

    This diverges deliberately from the system being replaced, which appended and
    relied on each batch having a unique name. A re-run there produced two
    playlists with one name, and the count then disagreed with the children.
    """
    doc = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="0">',
            "      </NODE>",
        ],
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
    """The derivation has to land exactly where the format already is.

    These four numbers are what every splice anchors on, so deriving them is only
    safe if the derivation agrees with the document rekordbox writes.
    """
    assert [rbxml.indent_at(depth) for depth in range(5)] == [4, 6, 8, 10, 12]
    assert rbxml.SUB_CLOSE_INDENT == 10
    assert rbxml.TRACK_INDENT == 12
    with pytest.raises(ValueError):
        rbxml.indent_at(-1)


# ═══════════════════════════════════════════════════════════════════════════
# The consolidated locates: every shape the old call sites used
# ═══════════════════════════════════════════════════════════════════════════

#: THE INVENTORY. Every distinct byte-level LOCATE shape found in the system
#: being replaced, and the primitive here that covers it. The claim "the guard
#: lives in the byte writers" is only true while a call site cannot find a node
#: without this module, so the shapes are enumerated from the source rather than
#: guessed at, and each names its cover.
#:
#: The inventory was taken from the two byte engines and the eight call sites
#: that scan an export: the shared byte writer, the reduced-export builder, the
#: whole-label subtree inserter, the vocal sub-playlist creator, the intake
#: splice, the genre attribute patcher, the intake rotation report, and the
#: unplaced sweep.
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
    """The inventory is checked against the module, not trusted.

    A shape whose cover was renamed away, or was never written, is a call site
    that will have to invent its own scan, and an invented scan is a byte write
    the guard never sees.
    """
    for shape, primitives in LOCATE_SHAPES.items():
        for name in primitives:
            assert callable(getattr(rbxml, name, None)), (
                f"the shape {shape!r} names {name!r}, which this module does not provide"
            )


def test_a_name_search_is_never_allowed_to_default_to_byte_zero():
    """The one locate every historical mis-anchor came through.

    ``start`` has no default on purpose, so the shape that produced three silent
    routing failures cannot be written by accident.
    """
    parameters = inspect.signature(rbxml.find_node).parameters
    assert parameters["start"].default is inspect.Parameter.empty


def test_the_locates_read_attributes_in_either_order():
    """Two writers matched the same node with the attributes in opposite orders.

    Each one silently found nothing in the other's output, and the sweep that
    found nothing reported success.
    """
    doc = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Type="0" Name="{_esc(TREE_DISPLAY)}" Count="1">',
            f'        <NODE Name="{_esc(FOLDER_DISPLAY)}" Type="0" Count="0"/>',
            "      </NODE>",
        ],
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
    """D1's character coverage, asserted on the pair rather than on one side.

    A name read out of a document has to compare equal to the name a caller
    passed in, or every idempotency check silently stops matching.
    """
    for name in (TREE_DISPLAY, FOLDER_DISPLAY, SUB_DISPLAY, SUB_DISPLAY_NFD, NEW_PLAYLIST):
        assert rbxml.xml_unescape_attr(rbxml.xml_escape_attr(name)) == name
    assert rbxml.xml_escape_attr("a & b") == "a &amp; b"
    assert rbxml.xml_unescape_attr("&amp;lt;") == "&lt;", (
        "the ampersand must be undone last, or an escaped ampersand becomes a tag"
    )


def test_the_two_composition_forms_are_two_different_nodes():
    """Recorded rather than fixed here, and the distinction is deliberate.

    This is a BYTE splicer: it finds the bytes it was given. Folding the two forms
    together would make a locate match a node whose bytes differ from the ones it
    would then patch. Normalizing a path before comparing is the locations
    module's job, and it is where the composition-form rule already lives.
    """
    doc = _xml_doc(
        collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
        root_children=[
            f'      <NODE Name="{_esc(TREE_DISPLAY)}" Type="0" Count="2">',
            f'        <NODE Name="{_esc(SUB_DISPLAY)}" Type="1" KeyType="0" Entries="0"/>',
            f'        <NODE Name="{_esc(SUB_DISPLAY_NFD)}" Type="1" KeyType="0" Entries="0"/>',
            "      </NODE>",
        ],
    )
    assert SUB_DISPLAY != SUB_DISPLAY_NFD
    span = rbxml.playlists_span(doc)
    assert span is not None
    precomposed = rbxml.find_node(doc, SUB_DISPLAY, start=span[0], end=span[1])
    decomposed = rbxml.find_node(doc, SUB_DISPLAY_NFD, start=span[0], end=span[1])
    assert precomposed is not None and decomposed is not None
    assert precomposed.tag_start != decomposed.tag_start


def test_the_tree_walk_reports_a_display_path_for_every_node():
    """The index a document-to-document diff needs, built once here.

    Two call sites in the old system built their own, one by counting indent
    characters, and an indent count is wrong the moment a tree of another depth
    turns up.
    """
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
    """The multi line track element, and the token that gets it wrong.

    A real export writes a track's attributes across five lines and closes it with
    its own tag. Bounding it by the next self-closing token lands inside the very
    same track when it carries analysis data, and the patch that follows then
    rewrites something rekordbox authored.
    """
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
    """The fixed-size window, reproduced, and refused.

    The version this ports scanned a fixed number of bytes forward from the id
    for the attribute it wanted. A track that did not carry that attribute meant
    the scan ran on into the FOLLOWING track and patched its value instead, and
    the user saw a change on a track they had never named.
    """
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
    """R17's other half: never create a grid, and never destroy one either.

    A user who has analysed their library owns something worth more than the
    files. Anything that rewrites an export hands every byte of it back.
    """
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
    """Every failure path returns a warning rather than feeding -1 into a slice.

    A slice with a -1 in it does not fail, it writes to the wrong place, and in
    this format that is a document nobody can import.
    """
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
        _xml_doc(
            collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
            root_children=[
                '      <NODE Name="Shelf One" Type="0" Count="0">',
                "      </NODE>",
                '      <NODE Name="Shelf Two" Type="0" Count="0">',
                "      </NODE>",
            ],
        )
    )
    before = bytes(two_trees)
    warning = rbxml.insert_genre_folder(two_trees, NEW_FOLDER, [])
    assert warning is not None and "cannot be inferred" in warning
    assert bytes(two_trees) == before
