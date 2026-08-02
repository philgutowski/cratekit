"""U2: the config schema, the two state roots, profiles, and credentials.

Four things are being proved here, and they fail in four different ways:

1. **Validation names every missing key**, not the first. The failure this
   prevents is a first-run wizard that costs one round trip per missing value.
2. **Every state file has exactly one root, and the right one.** This is the
   heart of the unit. The tests below audit the whole inventory rather than
   spot-checking it, because a state file assigned to the wrong root fails only
   on a second install, a reinstall, or during the migration overlap: three
   situations nobody is in while they are writing the code.
3. **Nothing snapshots config at import time.** The source system has seventeen
   modules that bind a state path at their own import, so half the package tracks
   a reload and half does not, silently, forever. The lint here makes that shape
   impossible to introduce rather than something to remember.
4. **A credential failure says which of three things went wrong.** A missing
   credential and a rejected one need opposite remediations.

The checkers follow the house style set by ``test_layering.py``: pure functions
over source text, fixture tests proving each rule bites against a synthetic
input, then one test running the checker over the real package. That order
matters most when the package is small, which it still is.
"""

from __future__ import annotations

import ast
import json
import os
import re
import stat
import subprocess
import sys
import tomllib
from pathlib import Path

import keyring
import keyring.backends.null
import keyring.errors
import pytest
import tomli_w

from cratekit.core import config, profiles, secrets
from tests._pending import requires

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A synthetic library root, aligned with the suite's isolation fixture.

    ``tests/conftest.py`` already points ``CRATEKIT_LIBRARY_ROOT`` at a temp
    directory for every test. This re-points it at a per-test one and returns it,
    so a test can write a config naming the same root the override will apply and
    the two do not silently disagree.
    """
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def valid_data(library: Path, **overrides) -> dict:
    """A minimal config that passes validation. Every key here is required."""
    data = {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library),
            "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(library.parent / "staging")},
        "profile": {"name": "slim"},
    }
    data.update(overrides)
    return data


@pytest.fixture
def cfg(library):
    return config.from_dict(valid_data(library))


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 1: validation names EVERY missing key
# ═══════════════════════════════════════════════════════════════════════════


def test_a_config_missing_required_keys_names_each_one():
    """The plan's first scenario. Note the assertion is on ALL of them.

    Stopping at the first missing key turns one setup session into one round
    trip per missing value, and a user who has to run the same command five times
    to learn five facts stops reading the fifth message.
    """
    with pytest.raises(config.ConfigInvalid) as excinfo:
        config.from_dict({})

    message = str(excinfo.value)
    for key in config.REQUIRED_KEYS:
        assert key in message, f"{key} was not named among the missing keys"
    assert len(excinfo.value.problems) >= len(config.REQUIRED_KEYS)


def test_a_partially_filled_config_names_only_what_is_actually_missing(library):
    data = valid_data(library)
    del data["library"]["volume_id"]
    del data["profile"]

    problems = config.validate(data)
    joined = "\n".join(problems)
    assert "library.volume_id" in joined
    assert "profile.name" in joined
    assert "library.root" not in joined
    assert "paths.download_staging" not in joined


def test_an_empty_string_counts_as_missing(library):
    """A blank in a wizard field is an unanswered question, not an answer."""
    data = valid_data(library)
    data["library"]["volume_id"] = "   "
    assert any("library.volume_id" in p for p in config.validate(data))


def test_the_required_list_is_exactly_six_keys():
    """Short by design: every other key is a decision the product can make.

    Asserted rather than merely documented because "required" grows silently.
    Each addition is one more question between a new user and a working install,
    so it should be a decision somebody made in a diff.
    """
    assert len(config.REQUIRED_KEYS) == 6


# ── R38: the volume identity key and its validation ──────────────────────────


def test_a_volume_identity_that_is_a_mount_path_is_rejected(library):
    """R38 identifies a volume by RECORDED IDENTITY, never by where it mounts.

    Recording the mount path passes the assertion for whatever drive happens to
    mount there next, which is the exact failure the requirement names.
    """
    data = valid_data(library)
    data["library"]["volume_id"] = str(library)
    problems = config.validate(data)
    assert any(config.VOLUME_IDENTITY_KEY in p and "mount path" in p for p in problems)


def test_the_volume_identity_key_is_published_for_the_assertion_to_read():
    """U31 implements the assertion; it must not spell the key itself.

    A guard that hardcodes the name of the thing it guards stops guarding the day
    that thing is renamed, and nothing fails to say so.
    """
    assert config.VOLUME_IDENTITY_KEY == "library.volume_id"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 2: profiles toggle module membership and nothing else (D6)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_profile_change_toggles_membership_without_touching_unrelated_keys(library):
    """The plan's fourth scenario, asserted on the whole rest of the document."""
    data = valid_data(
        library,
        naming={"lossy_marker": "[LOSSY]"},
        backup={"remote": "somewhere"},
        taxonomy={"template": "custom"},
    )
    before = {k: v for k, v in data.items() if k != "profile"}

    after = profiles.apply(data, "full")

    assert after["profile"]["name"] == "full"
    for key, value in before.items():
        assert after[key] == value, f"changing the profile changed {key}"

    assert config.from_dict(data).enabled_modules() == frozenset()
    assert config.from_dict(after).enabled_modules() == frozenset(profiles.MODULES)


def test_an_explicit_toggle_overrides_the_profile_in_both_directions():
    """Precedence is stated, not emergent: the explicit toggle wins."""
    added = profiles.resolve("slim", {"analysis": True})
    assert "analysis" in added.modules
    assert added.overridden == frozenset({"analysis"})

    removed = profiles.resolve("full", {"vocals": False})
    assert "vocals" not in removed.modules
    assert removed.overridden == frozenset({"vocals"})


def test_switching_profiles_preserves_the_users_own_toggles(library):
    """A profile is a preset, not a reset.

    Somebody who turned one module off meant it. Clearing overrides on a profile
    switch would undo a decision the user made without ever saying so.
    """
    data = valid_data(library, modules={"desktop": False})
    after = profiles.apply(data, "full")
    assert after["modules"] == {"desktop": False}
    assert "desktop" not in config.from_dict(after).enabled_modules()


def test_a_profile_change_returns_a_copy_the_caller_cannot_edit_backwards(library):
    """"Touches module membership and nothing else" has to be true of the nested tables too.

    A shallow copy hands back the caller's own sub-dictionaries, so the claim
    holds for the returned document and breaks the moment anybody writes into one
    of them: the input is edited at the same time, invisibly. The existing D6
    scenario test compares for equality, which aliasing passes.
    """
    data = valid_data(library, backup={"remote": "somewhere"})

    after = profiles.apply(data, "full")
    after["backup"]["remote"] = "somewhere-else"

    assert data["backup"]["remote"] == "somewhere"


def test_library_adoption_is_available_in_every_profile():
    """R5's one exception. The slim user is the one most likely to need it."""
    for name in profiles.PROFILE_NAMES:
        assert "adoption" in profiles.resolve(name).available


def test_the_slim_profile_enables_no_modules():
    assert profiles.resolve("slim").modules == frozenset()


def test_an_unknown_profile_or_module_refuses_by_name():
    with pytest.raises(profiles.UnknownProfile):
        profiles.resolve("gigantic")
    with pytest.raises(profiles.UnknownModule):
        profiles.resolve("slim", {"telepathy": True})


def test_config_validation_rejects_an_unknown_module_toggle(library):
    data = valid_data(library, modules={"telepathy": True})
    assert any("telepathy" in p for p in config.validate(data))


def test_every_extras_group_names_a_real_module(library):
    """KTD7: extras are named one-to-one with modules.

    Read from ``pyproject.toml`` rather than mirrored by hand, for the reason the
    CI dependency list already taught this repository: a hand-mirrored list is a
    list that drifts, and the drift shows up as a guard that stopped guarding.
    """
    with (REPO_ROOT / "pyproject.toml").open("rb") as handle:
        extras = tomllib.load(handle)["project"]["optional-dependencies"]
    declared = set(extras) - {"all", "dev"}
    assert declared == set(profiles.EXTRAS_BACKED)
    assert profiles.EXTRAS_BACKED <= set(profiles.MODULES)


def test_a_module_without_a_heavy_dependency_reports_no_extras_group():
    """None is an answer, not a gap: some modules need nothing extra installed."""
    assert profiles.install_command("analysis") == "analysis"
    assert profiles.install_command("favorites") is None


# ═══════════════════════════════════════════════════════════════════════════
# The two state roots (KTD21). The heart of the unit.
# ═══════════════════════════════════════════════════════════════════════════


def test_there_are_exactly_two_state_roots():
    """Two, not three, not "and also this one place". KTD21 is a closed set."""
    assert set(config.StateRoot) == {config.StateRoot.INSTALLATION, config.StateRoot.LIBRARY}


def test_every_state_entry_is_assigned_to_exactly_one_root_and_says_why():
    for entry in config.STATE_FILES:
        assert entry.root in config.StateRoot
        assert len(entry.why) > 60, (
            f"{entry.key} has no real justification. The rule is that 'why' names "
            f"what BREAKS under a second install, a reinstall, or the migration "
            f"overlap; anything shorter is a label, not a reason."
        )


def test_state_keys_are_unique():
    keys = [entry.key for entry in config.STATE_FILES]
    assert len(keys) == len(set(keys))


def test_no_two_state_entries_resolve_to_the_same_path(cfg):
    """The structural form of "nothing straddles".

    Two entries at one path is the same defect as one entry at two roots: one
    writer silently overwrites the other, and which one wins depends on order.
    """
    seen: dict[Path, str] = {}
    for entry in config.STATE_FILES:
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        path = config.state_path(entry.key, cfg)
        assert path not in seen, f"{entry.key} collides with {seen.get(path)} at {path}"
        seen[path] = entry.key


def test_installation_state_never_lands_under_the_library(cfg, library):
    """The audit that makes "nothing straddles" checkable rather than asserted."""
    for entry in config.state_files_for(config.StateRoot.INSTALLATION):
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        path = config.state_path(entry.key, cfg)
        assert library not in path.parents, (
            f"{entry.key} is declared installation-scoped but resolves inside the "
            f"library at {path}"
        )


def test_library_state_never_lands_under_the_installation_root(cfg):
    installation = config.installation_state_dir()
    for entry in config.state_files_for(config.StateRoot.LIBRARY):
        path = config.state_path(entry.key, cfg)
        assert installation not in path.parents, (
            f"{entry.key} is declared library-scoped but resolves under the "
            f"installation state root at {path}. That is the placement KTD21 exists "
            f"to end: restore per installation, database per library."
        )


# ── The audit the two tests above could not make: an entry must resolve where ──
# ── the code that reads and writes it actually looks. ────────────────────────


@pytest.fixture
def split_installation_dirs(monkeypatch, tmp_path):
    """Force the two installation directories apart, and prove they are apart.

    This fixture is the whole reason the audits below can see anything. On macOS
    platformdirs returns ONE directory for both ``user_config_dir`` and
    ``user_state_dir``, so an entry declared under the state directory while its
    loader reads the config directory agrees by accident on the author's machine
    and diverges on Linux. An audit run with the two coincident is an audit that
    certifies the defect.
    """
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "installation-config"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "installation-state"))
    assert config.config_dir() != config.installation_state_dir()
    return tmp_path


#: Every inventory entry that ALSO has a named accessor somewhere in the package,
#: mapped to that accessor. An entry in this table is one where two pieces of code
#: can disagree about a path, which is the only way "declared here, written there"
#: can happen. The lint below keeps the table honest.
_NAMED_ACCESSORS = {
    "config": lambda: config.config_path(),
    "credential_index": lambda: secrets._index_path(),
}


def test_every_entry_with_a_named_accessor_resolves_to_the_same_path(
    split_installation_dirs,
):
    """The audit that catches a declared root nothing writes to.

    The two existing root audits only check that an installation entry does not
    land under the library. Neither can see an entry that lands under the wrong
    INSTALLATION directory, because both of those are outside the library.
    """
    for key, accessor in _NAMED_ACCESSORS.items():
        assert config.state_path(key) == accessor(), (
            f"{key} is declared at {config.state_path(key)} but the code that "
            f"reads and writes it uses {accessor()}. One file, two roots, is the "
            f"straddling the Definition of Done forbids."
        )


def test_every_installation_entry_resolves_under_a_directory_the_module_names(
    split_installation_dirs,
):
    """No installation entry may resolve outside the two directories that exist.

    Stated positively rather than as "not under the library", so a third
    directory invented by a future entry fails here instead of resolving to
    somewhere nothing enumerates.
    """
    known = (config.config_dir(), config.installation_state_dir())
    for entry in config.state_files_for(config.StateRoot.INSTALLATION):
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        path = config.state_path(entry.key)
        assert any(directory in path.parents for directory in known), (
            f"{entry.key} resolves to {path}, which is under neither the "
            f"installation config directory nor the installation state directory"
        )


#: Every function in the config module that hands out a directory under a state
#: root. The lint below refuses a path composed onto any of them, so this set has
#: to be COMPLETE: the first consumer of a new accessor is the first code the
#: guard cannot see, and the library reorganization proved that by adding three
#: accessors that the lint went on ignoring.
#:
#: Kept honest by ``test_the_composed_path_lint_covers_every_directory_accessor``
#: rather than by remembering.
_STATE_ROOT_ACCESSORS = {
    "config_dir",
    "installation_state_dir",
    "library_state_dir",
    "library_coupled_dir",
    "library_history_dir",
    "library_local_dir",
}


def _paths_composed_from_a_state_root(source: str) -> list[str]:
    """Return every expression that builds a path under a state root directly.

    A module that composes ``installation_state_dir() / "something.json"`` for
    itself has invented a state file the inventory does not know about, which is
    the same defect as declaring one under the wrong root: nothing that walks
    ``STATE_FILES`` will find it, back it up, or clear it.
    """
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Div):
            continue
        left = node.left
        if isinstance(left, ast.Call) and _called_name(left.func) in _STATE_ROOT_ACCESSORS:
            found.append(ast.unparse(node))
    return found


def test_the_composed_path_lint_catches_a_module_inventing_its_own_state_file():
    source = 'from cratekit.core.config import installation_state_dir\n\ndef p():\n    return installation_state_dir() / "mine.json"\n'
    assert _paths_composed_from_a_state_root(source)


@pytest.mark.parametrize(
    "accessor", ["library_coupled_dir", "library_history_dir", "library_local_dir"]
)
def test_the_composed_path_lint_catches_the_accessors_the_reorganization_added(accessor):
    """The three the guard could not see, asserted one at a time.

    These are documented as the handle the snapshot and restore units should
    hold, which makes them the accessors most likely to have a path composed onto
    them, and they were the ones the lint's name set left out.
    """
    source = f'def p(cfg):\n    return {accessor}(cfg) / "mine.json"\n'
    assert _paths_composed_from_a_state_root(source)


def test_the_composed_path_lint_covers_every_directory_accessor_the_module_exports():
    """The guard's name set cannot fall behind the module it guards.

    Widening the set by hand once fixes today. This makes the NEXT accessor fail
    the build the moment it is exported, which is the difference between a guard
    that was correct and a guard that stays correct.
    """
    exported = {name for name in config.__all__ if name.endswith("_dir")}
    missing = exported - _STATE_ROOT_ACCESSORS
    assert not missing, (
        f"config exports directory accessors the composed-path lint does not "
        f"know about: {sorted(missing)}. Add them to _STATE_ROOT_ACCESSORS, or "
        f"the first module to compose a path onto one is invisible to the guard."
    )


def test_no_module_composes_its_own_path_under_a_state_root():
    """Every path under a state root comes from ``state_path``, so it is declared.

    ``config.py`` is excluded because it is the module that DEFINES the roots and
    resolves the inventory; everywhere else, composing a root path by hand is how
    a file ends up outside the audit.
    """
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path.relative_to(SRC_ROOT).as_posix() == "cratekit/core/config.py":
            continue
        for hit in _paths_composed_from_a_state_root(path.read_text()):
            offenders.append(f"{path.relative_to(SRC_ROOT)}: {hit}")
    assert not offenders, (
        "paths composed under a state root outside the inventory:\n"
        + "\n".join(offenders)
        + "\nDeclare the entry in config.STATE_FILES and resolve it with state_path()."
    )


@pytest.mark.parametrize(
    "key",
    ["write_lock", "session_lock", "session_log", "snapshots", "favorites_state"],
)
def test_the_locks_the_log_and_the_snapshots_live_with_the_library(key, cfg, library):
    """KTD17, R31, KTD21b, and the KTD21 headline, one assertion each.

    Concretely: two installations means two lock files means zero mutual
    exclusion against one database, and a restore that lives per installation
    cannot roll back a write another machine made.
    """
    assert config.state_file(key).root is config.StateRoot.LIBRARY
    assert library in config.state_path(key, cfg).parents


def test_the_job_queue_stays_with_the_installation(cfg):
    """KTD21 names it, and a detached job does belong to the machine running it.

    The consequence is recorded on the entry itself: because the queue is per
    install and the library is per config, a job record has to NAME the library
    it targets, or a queue drained after the user reconfigures runs against the
    wrong volume.
    """
    entry = config.state_file("job_queue")
    assert entry.root is config.StateRoot.INSTALLATION
    assert "library it targets" in entry.why
    # Resolvable with no config at all, which is what lets the queue be read on a
    # machine whose library is not mounted.
    assert config.state_path("job_queue") == config.installation_state_dir() / "jobs"


def test_the_per_set_workspaces_resolve_from_configured_directory_names(cfg, library):
    """The one entry composed from config values rather than a fixed relative path.

    It is already correct by accident of location in the source system: the stage
    artifacts sit beside the audio they describe. What must not survive the port
    is the literal, since both directory names are user-configurable.

    It resolves to a Cratekit-owned directory INSIDE the sets directory, never to
    the sets directory itself. The sets directory holds the user's own recordings,
    and an entry that names it puts hundreds of gigabytes of audio into every
    generic pass over the inventory: the snapshot would try to copy it, a state
    report would list the user's music as Cratekit state, and any future "clear
    this library's state" built off the inventory would target user content.
    """
    resolved = config.state_path("set_workspaces", cfg)
    sets_dir = library / cfg.library.music_dir / cfg.library.sets_dir
    assert resolved.parent == sets_dir
    assert resolved != sets_dir


# ═══════════════════════════════════════════════════════════════════════════
# KTD21b: the snapshot boundary is declared in the schema, not kept as a list
# ═══════════════════════════════════════════════════════════════════════════


def test_every_state_entry_declares_a_snapshot_role():
    """The plan's top-ranked risk is the registry rolling back while the database does not.

    Without a declared role per entry, U8 and U32 have to hand-maintain an
    exclusion list against a flat directory. This repository already refuses that
    shape for its CI dependency list and its extras table, for the same reason: a
    hand-mirrored list drifts, and the drift shows up as a guard that stopped
    guarding.
    """
    for entry in config.STATE_FILES:
        assert entry.snapshot in config.SnapshotRole, (
            f"{entry.key} does not say whether a restore rolls it back"
        )


def test_the_locks_and_the_snapshot_store_are_not_in_the_coupled_set():
    """Two failures, one assertion each, both silent.

    A restore that replaces the directory holding a lock swaps the inode a live
    advisory lock is held on, so mutual exclusion disappears mid-session with
    nothing raised. A restore that replaces the snapshot store destroys the record
    of which sessions are restorable, and capturing it nests every prior snapshot
    inside the new one.
    """
    coupled = {entry.key for entry in config.coupled_state_files()}
    for key in (
        "write_lock",
        "session_lock",
        "favorites_state_lock",
        "snapshots",
        "session_log",
    ):
        assert key not in coupled, f"{key} must not roll back with the database"


def test_the_snapshot_store_and_the_session_log_survive_a_rollback():
    for key in ("snapshots", "session_log"):
        assert config.state_file(key).snapshot is config.SnapshotRole.SURVIVES_ROLLBACK


def test_the_undo_logs_are_never_rolled_back():
    """Their own ``why`` says it: they hold the ONLY copy of an overwritten value.

    The values they record were written to the user's files on disk. A database
    restore does not roll those writes back, so rolling the log back discards the
    only record of how to undo them. That is not a stale record, it is data loss.
    """
    for key in ("energy_undo_log", "genre_tag_undo_log"):
        assert config.state_file(key).snapshot is config.SnapshotRole.NEVER_RESTORED


def test_the_coupled_state_named_by_the_plan_rolls_back_with_the_database():
    """R30 names these by name: registry, watermarks, tombstones, declines."""
    for key in (
        "tree_registry",
        "label_watermarks",
        "deletion_watermark",
        "tombstones",
        "declines",
        "taxonomy_active",
        "favorites_state",
        "rekordbox_db",
    ):
        assert config.state_file(key).snapshot is config.SnapshotRole.COUPLED, key


def test_the_coupled_set_is_a_directory_boundary_rather_than_a_list(cfg):
    """A snapshot is one directory plus the database, derived from the schema.

    Both halves are asserted. Every coupled entry must sit inside a declared
    snapshot source, and nothing that is NOT coupled may sit inside the coupled
    directory, or a restore that replaces that directory would roll back an entry
    the schema says must not roll back.
    """
    sources = config.snapshot_sources(cfg)
    coupled_dir = config.library_coupled_dir(cfg)

    for entry in config.coupled_state_files():
        path = config.state_path(entry.key, cfg)
        assert any(path == source or source in path.parents for source in sources), (
            f"{entry.key} is coupled but resolves to {path}, which no declared "
            f"snapshot source covers"
        )

    for entry in config.STATE_FILES:
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        if entry.snapshot is config.SnapshotRole.COUPLED:
            continue
        path = config.state_path(entry.key, cfg if entry.root is config.StateRoot.LIBRARY else None)
        assert coupled_dir not in path.parents, (
            f"{entry.key} is declared {entry.snapshot} but sits inside the coupled "
            f"directory, so a restore would replace it anyway"
        )


def test_the_snapshot_store_does_not_nest_inside_what_it_snapshots(cfg):
    """Otherwise every snapshot contains every previous one, forever."""
    store = config.state_path("snapshots", cfg)
    for source in config.snapshot_sources(cfg):
        assert source != store and source not in store.parents


# ── The capture set is WAL-aware, because a database is not one file ─────────


def test_the_capture_set_includes_the_databases_sqlite_sidecars(cfg):
    """A U8 implementer who copies exactly these paths must not get a torn database.

    SQLite in WAL mode keeps committed-but-uncheckpointed transactions in
    ``<db>-wal``. A capture set naming only ``<db>`` produces a copy that opens
    cleanly and is silently missing them, which is the worst shape a backup can
    take. The source system captures the database and both sidecars as one
    matched set; deriving that here is what stops U8 from re-deriving it as a
    hand-kept companion list, which is the drift this schema exists to abolish.
    """
    sources = config.snapshot_sources(cfg)
    db = cfg.library.db_path

    assert db in sources
    for suffix in ("-wal", "-shm"):
        expected = db.with_name(db.name + suffix)
        assert expected in sources, (
            f"{expected.name} is not in the capture set, so a snapshot taken "
            f"from it copies a database missing everything still in the log"
        )


def test_the_sidecars_are_declared_on_the_entry_rather_than_listed_by_a_consumer():
    """The set is derived, so it cannot drift from the entry it belongs to."""
    entry = config.state_file("rekordbox_db")
    assert entry.sidecars == config.SQLITE_SIDECARS
    assert [s.suffix for s in entry.sidecars] == ["-wal", "-shm"]
    # Every other entry is a single file, and says so rather than defaulting into
    # a shape nobody decided.
    for other in config.STATE_FILES:
        if other.key != "rekordbox_db":
            assert other.sidecars == ()


def test_a_restore_writes_back_the_log_and_never_the_shared_memory_index(cfg):
    """The source system's asymmetry, carried across as a declaration.

    Its restore clears BOTH live sidecars first, so the engine cannot replay a
    log belonging to the database that was just replaced, then copies the
    snapshot's ``-wal`` and never its ``-shm``. The shared-memory index is
    derived from the log, so putting a stale one back beside a fresh log hands
    SQLite two disagreeing views of one database.
    """
    db = cfg.library.db_path
    everything = config.sidecar_paths("rekordbox_db", cfg)
    restored = config.sidecar_paths("rekordbox_db", cfg, restored_only=True)

    assert everything == (
        db.with_name(db.name + "-wal"),
        db.with_name(db.name + "-shm"),
    )
    assert restored == (db.with_name(db.name + "-wal"),)


def test_an_entry_with_no_sidecars_resolves_to_no_sidecar_paths(cfg):
    assert config.sidecar_paths("tree_registry", cfg) == ()


# ── Nothing yet holds the consumers to the derivation, so the register does ──


def test_the_capture_unit_derives_its_source_set_rather_than_listing_it():
    """``snapshot_sources`` being correct is worth nothing if U8 ignores it.

    ``coupled_state_files`` and ``snapshot_sources`` both assert in their own
    docstrings that U8 and U32 never maintain a second copy of the set. Until
    this guard is armed, nothing makes that true: U8 could land with a hand-typed
    path list including or omitting the sidecars, and the build would stay green.
    That is the same softening the application pin's own countdown already
    closes, so it is closed the same way here.

    Both halves are asserted. The module must REACH FOR the derivation, and it
    must not carry a sidecar suffix of its own, because a literal ``-wal`` in the
    capture unit is precisely the companion list this schema replaced.
    """
    import cratekit.core.snapshot as snapshot  # noqa: PLC0415

    source = Path(snapshot.__file__).read_text()
    assert "snapshot_sources" in source, (
        "the capture unit does not call config.snapshot_sources, so its capture "
        "set is a second copy of the inventory"
    )
    assert not re.search(r"""["'][^"']*-(?:wal|shm)""", source), (
        "the capture unit spells a SQLite sidecar suffix itself; the suffixes are "
        "declared on the rekordbox_db entry and expanded by sidecar_paths"
    )


@requires("cratekit.core.restore")
def test_the_restore_unit_derives_its_target_set_rather_than_listing_it():
    """The symmetric half, and the one the plan's top-ranked risk turns on.

    A restore that replaces a set even slightly different from the captured one
    is how the registry rolls back while the database does not. It must derive
    the set, and it must get the sidecar asymmetry from the declaration rather
    than from a suffix it typed.
    """
    import cratekit.core.restore as restore  # noqa: PLC0415

    source = Path(restore.__file__).read_text()
    assert "sidecar_paths" in source or "snapshot_sources" in source, (
        "the restore unit does not resolve its targets through the inventory"
    )
    assert not re.search(r"""["'][^"']*-(?:wal|shm)""", source), (
        "the restore unit spells a SQLite sidecar suffix itself; which sidecars "
        "come back is declared by Sidecar.restored, not retyped here"
    )


def test_a_library_scoped_entry_never_declares_an_installation_area():
    """The field is read only for installation entries, so it must stay unset elsewhere.

    A field that is set but unread is the shape that made ``at_library_root``
    factually wrong on one entry and dead at the same time.
    """
    for entry in config.state_files_for(config.StateRoot.LIBRARY):
        assert entry.installation_area is config.InstallationArea.STATE


# ═══════════════════════════════════════════════════════════════════════════
# The database is state too, and KTD21b needs it beside its coupled state
# ═══════════════════════════════════════════════════════════════════════════


def test_the_rekordbox_database_is_declared_library_scoped_state(cfg):
    """It is the single most important piece of library-scoped state in the product.

    An inventory that omits it looks complete while the thing every other entry
    describes has no row.
    """
    entry = config.state_file("rekordbox_db")
    assert entry.root is config.StateRoot.LIBRARY
    assert config.state_path("rekordbox_db", cfg) == cfg.library.db_path


def test_a_database_outside_the_library_root_refuses_until_it_is_acknowledged(
    library, tmp_path
):
    """The default rekordbox install puts the database in the user's home directory.

    The coupled state then sits on the music volume while the database sits on the
    boot disk, so the atomic commit KTD21b requires spans two filesystems, where
    no rename-based atomic commit exists. The plan's stated premise for the
    decision, that the coupled state is a handful of small files beside the
    database, is simply false for that install.
    """
    data = valid_data(library)
    data["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")

    problems = config.validate(data)

    assert any("db_path" in p and "library.root" in p for p in problems), problems


def test_an_acknowledged_database_outside_the_library_root_loads_and_says_so(
    library, tmp_path
):
    """Permitted, but only as a recorded decision with the consequence attached.

    The failure has to be visible at setup, when the user can still move the
    database, rather than at the first snapshot, when they cannot.
    """
    data = valid_data(library)
    data["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")
    data["library"]["db_outside_root_acknowledged_on"] = "2026-08-01"

    assert config.validate(data) == []
    cfg = config.from_dict(data)
    assert cfg.db_is_inside_library_root() is False
    assert cfg.library.db_outside_root_acknowledged_on == "2026-08-01"


def test_a_database_beside_the_library_needs_no_acknowledgment(cfg):
    assert cfg.db_is_inside_library_root() is True
    assert cfg.library.db_outside_root_acknowledged_on is None


@pytest.mark.parametrize("value", ["no", "true", "yes", "1", "2026-13-99", "01-08-2026", "20260801"])
def test_a_non_date_acknowledgment_does_not_switch_the_refusal_off(library, tmp_path, value):
    """Accepting any non-empty string made ``no`` disable the rule it reads as enforcing.

    The escape hatch records WHEN the non-atomic-snapshot consequence was
    accepted, so the value has to be a real calendar date. Its sibling in the
    same validator, ``library.volume_id``, is shape-checked for exactly this
    reason: a merely truthy value passes a truthiness test while meaning nothing,
    and here it silently disables a refusal.

    Both problems are asserted. The shape is named, AND the containment refusal
    still fires, because an acknowledgment nobody can parse is not an
    acknowledgment.
    """
    data = valid_data(library)
    data["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")
    data["library"]["db_outside_root_acknowledged_on"] = value

    problems = config.validate(data)

    assert any(config.ACKNOWLEDGMENT_KEY in p and "date" in p for p in problems), problems
    assert any("is not under library.root" in p for p in problems), problems


def test_a_malformed_acknowledgment_is_named_even_when_the_database_is_contained(cfg, library):
    """A bad date is a defect in the file whether or not it is load-bearing today.

    Naming it only when the database happens to sit elsewhere would hide it until
    the day the user moves the database, which is the day they can least afford a
    second surprise.
    """
    data = valid_data(library)
    data["library"]["db_outside_root_acknowledged_on"] = "someday"
    assert any(config.ACKNOWLEDGMENT_KEY in p for p in config.validate(data))


# ── The layout of the library state directory, and what does NOT migrate it ──


def test_the_library_state_layout_carries_no_migration_because_nothing_wrote_another_one():
    """A deferral recorded in code, with a countdown attached.

    Library entries used to resolve into one flat directory and now resolve into
    role subdirectories. Nothing reconciles an existing directory, and nothing
    here can: ``MIGRATIONS`` is dict-to-dict by construction, which is what makes
    "a failed migration leaves the original untouched" true rather than hoped
    for, and that same purity makes it structurally unable to move a file.

    At layout version 1 there is nothing to reconcile, because the subdirectories
    were introduced before this package had any write path at all, so no build
    has ever written another shape. The version constant is what makes that a
    decision rather than an omission: bumping it without a mechanism fails here.
    """
    assert config.LIBRARY_STATE_LAYOUT_VERSION == 1, (
        "the library state layout changed. Config migrations are dict-to-dict "
        "and cannot move a file, so the unit that changed it owns a one-time "
        "on-disk reconciliation with its own mechanism, run under the same "
        "exclusive lock, idempotent, and refusing rather than half-moving. Add "
        "it, then update this test to cover it."
    )


@requires("cratekit.cli.doctor")
def test_doctor_reports_a_database_that_sits_outside_the_library_root(
    library, tmp_path, monkeypatch
):
    """The other half of the containment rule, and the half U2 cannot arm alone.

    Refusing at load makes the consequence visible at setup, which is when the
    user can still move the database. It does nothing about the install where
    somebody accepted the consequence eighteen months ago and has since forgotten
    that their snapshots are copies across two filesystems rather than atomic
    commits. Doctor is the run that has to keep saying so, and until it lands this
    is registered against U27 rather than left as a hope.
    """
    from cratekit.cli import doctor

    data = valid_data(library)
    data["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")
    data["library"]["db_outside_root_acknowledged_on"] = "2026-08-01"
    acknowledged = config.from_dict(data)
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: acknowledged)

    report = doctor.run()

    assert any(
        "db_path" in str(finding) and "atomic" in str(finding) for finding in report.findings
    ), report


def test_credentials_are_not_a_file_at_all(cfg):
    for key in ("credentials", "provider_session"):
        assert config.state_file(key).medium is config.Medium.KEYCHAIN
        with pytest.raises(ValueError, match="keychain"):
            config.state_path(key, cfg)


def test_resolving_a_library_scoped_entry_without_a_config_refuses():
    """No silent fallback to the installation root. That fallback IS the bug."""
    with pytest.raises(ValueError, match="library-scoped"):
        config.state_path("write_lock")


def test_an_undeclared_state_key_raises_with_the_declared_list():
    with pytest.raises(KeyError, match="not a declared state entry"):
        config.state_file("some_new_ledger")


# ── D4: the two straddling entries became two files each ─────────────────────


@pytest.mark.parametrize(
    "install_key, library_key",
    [
        ("label_crawl_cache", "label_outcomes"),
        ("label_intent", "label_watermarks"),
    ],
)
def test_a_previously_straddling_entry_is_two_files_with_distinct_names(
    install_key, library_key
):
    """D4. One file with two owners is not a resolution, it is the problem named.

    The registry case is concrete: in the source system the whole file is
    committed to git, so cloning hands every friend one person's label list AND
    their sweep watermarks. Splitting makes the intent half shareable on purpose
    and leaves the watermarks with the library they describe.
    """
    install = config.state_file(install_key)
    library_side = config.state_file(library_key)
    assert install.root is config.StateRoot.INSTALLATION
    assert library_side.root is config.StateRoot.LIBRARY
    assert install.relative != library_side.relative


# ── D5: no persisted record is keyed by a display name ───────────────────────


def test_the_one_ported_shape_keyed_by_a_display_name_is_flagged_for_rekeying():
    flagged = [e.key for e in config.STATE_FILES if e.rekey_from_display_name]
    assert flagged == ["playlist_parole_ledger"]


def test_rekeying_maps_records_onto_stable_identifiers():
    records = {"Late Night": {"seen": "2026-01-01"}, "Sunset": {"seen": "2026-02-01"}}
    identifiers = {"Late Night": "pl-0001", "Sunset": "pl-0002"}

    migrated, unresolved = config.rekey_records(records, identifiers.get)

    assert migrated == {"pl-0001": {"seen": "2026-01-01"}, "pl-0002": {"seen": "2026-02-01"}}
    assert unresolved == ()


def test_rekeying_reports_records_it_could_not_resolve_rather_than_dropping_them():
    """An unresolvable record IS the orphan the rule exists to surface.

    Dropping it silently would make the one-time migration look clean while
    losing exactly the history the rename orphaned.
    """
    migrated, unresolved = config.rekey_records({"Gone": {}}, lambda _: None)
    assert migrated == {}
    assert unresolved == ("Gone",)


# ═══════════════════════════════════════════════════════════════════════════
# Seam decisions that live in this schema
# ═══════════════════════════════════════════════════════════════════════════


def test_the_prefix_map_is_ordered_and_first_match_wins(library):
    """S1. Order is load-bearing: one prefix can be another's prefix.

    An unordered map resolves those two differently on different runs, and the
    symptom is a resolver that works today and silently mis-resolves after an
    unrelated change to iteration order.
    """
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [
        {"from": "/mnt/volume/deep", "to": "{library.root}/deep"},
        {"from": "/mnt/volume", "to": "{library.root}"},
    ]
    resolved = config.from_dict(data).resolved_prefix_map()

    assert resolved[0][0] == "/mnt/volume/deep"
    assert resolved[1][0] == "/mnt/volume"
    assert resolved[0][1] == f"{library}/deep"


def test_the_prefix_map_survives_a_remount_because_it_interpolates(library, tmp_path, monkeypatch):
    """The stored map is written once and keeps working when the drive moves."""
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [{"from": "/mnt/volume", "to": "{library.root}"}]

    moved = tmp_path / "elsewhere"
    moved.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(moved))

    assert config.from_dict(data).resolved_prefix_map() == (("/mnt/volume", str(moved)),)


def test_an_unsupported_interpolation_in_the_prefix_map_is_named(library):
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [{"from": "/mnt/volume", "to": "{home}"}]
    assert any("unsupported interpolation" in p for p in config.validate(data))


def test_a_malformed_prefix_entry_is_named_by_index(library):
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [{"from": "/mnt/volume"}]
    assert any("location_prefix_map[0].to" in p for p in config.validate(data))


def test_an_unset_rekordbox_pin_refuses_to_write(cfg):
    """S2. Unset REFUSES, and is never auto-recorded from the running install.

    A pin the software copies from whatever happens to be installed refuses
    nothing, forever, which is the entire property the pin exists to provide.
    """
    assert cfg.rekordbox.pinned_app_version is None
    with pytest.raises(config.ConfigInvalid, match="pinned_app_version"):
        cfg.assert_rekordbox_pin_recorded()


def test_a_recorded_pin_permits_the_write_and_carries_its_validation_date(library):
    """The pin is only meaningful with the date somebody verified it."""
    data = valid_data(
        library,
        rekordbox={
            "pinned_app_version": "7.2.14.0323",
            "validated_on": "2026-08-01",
            "app_path": "/Applications/rekordbox",
        },
    )
    cfg = config.from_dict(data)
    cfg.assert_rekordbox_pin_recorded()
    assert cfg.rekordbox.validated_on == "2026-08-01"
    assert cfg.rekordbox.app_path == Path("/Applications/rekordbox")


def test_config_owns_the_naming_values(cfg):
    """S3. U2 owns the VALUES; the naming engine owns the mechanism.

    The engine takes these as parameters and imports no config, because a
    function that reads global configuration cannot be exercised against two
    taxonomies in one process, and proving a second template works needs exactly
    that.
    """
    assert cfg.naming.lossy_marker
    assert cfg.naming.path_budget_bytes == 250
    assert cfg.naming.filename_max_bytes == 255
    assert cfg.naming.path_budget_bytes < cfg.naming.filename_max_bytes


def test_there_is_no_configuration_in_which_lossy_goes_unmarked(library):
    """S3 and R21. Two values, and neither one is 'allow lossy, skip marking'.

    Unrepresentable beats validated-away: there is no toggle to set wrong.
    """
    assert config.from_dict(valid_data(library)).acquisition.lossless_policy == "strict"

    permitted = valid_data(library, acquisition={"lossless_policy": "allow_lossy_marked"})
    assert config.validate(permitted) == []

    for bad in ("allow_lossy", "off", "none", "unmarked"):
        problems = config.validate(valid_data(library, acquisition={"lossless_policy": bad}))
        assert any("lossless_policy" in p for p in problems), bad


def test_config_carries_only_the_taxonomy_selection(cfg):
    """S6. The active template is library-scoped state, not a config value."""
    field_names = {f for f in type(cfg.taxonomy).__dataclass_fields__}
    assert field_names == {"template"}
    assert config.state_file("taxonomy_active").root is config.StateRoot.LIBRARY


def test_analysis_worker_count_defaults_to_probing(cfg):
    """KTD10: worker counts come from a memory probe, never from a CPU count.

    Absent means probe. A shipped numeric default would be a guess about
    somebody else's machine, permanently.
    """
    assert cfg.analysis.jobs is None


def test_no_backup_destination_ships_with_a_default(cfg):
    """Every one of these is a hardcoded literal naming one person's remote."""
    assert cfg.backup.remote is None
    assert cfg.backup.dest is None
    assert cfg.backup.archive_root is None
    assert cfg.backup.db_dest_root is None


# ═══════════════════════════════════════════════════════════════════════════
# The fingerprint (KTD9)
# ═══════════════════════════════════════════════════════════════════════════


def test_the_fingerprint_survives_a_round_trip_through_disk(cfg, tmp_path):
    """A job compares fingerprints to report drift, so serialization must not drift."""
    path = tmp_path / "config.toml"
    config.save(cfg, path)
    reloaded = config.load(path)
    assert reloaded.fingerprint() == cfg.fingerprint()


def test_the_fingerprint_is_stable_across_repeated_serialization(cfg):
    assert cfg.to_toml_bytes() == cfg.to_toml_bytes()
    assert cfg.fingerprint() == cfg.fingerprint()


def test_the_fingerprint_does_not_depend_on_key_order(library):
    """Two files that mean the same thing must hash the same.

    Otherwise every hand edit that reorders a section reports as drift, and users
    learn to ignore drift reports.
    """
    first = config.from_dict(valid_data(library, taxonomy={"template": "default"}))
    reordered = valid_data(library)
    reordered["taxonomy"] = {"template": "default"}
    reordered = dict(reversed(list(reordered.items())))
    assert config.from_dict(reordered).fingerprint() == first.fingerprint()


@pytest.mark.parametrize(
    "section, key, value",
    [
        ("library", "music_dir", "Audio"),
        ("paths", "download_staging", "staging-elsewhere"),
        ("modules", "analysis", True),
        ("naming", "lossy_marker", "[LOSSY]"),
        ("naming", "path_budget_bytes", 240),
        ("acquisition", "lossless_policy", "allow_lossy_marked"),
        ("analysis", "jobs", 2),
        ("taxonomy", "template", "other"),
        ("rekordbox", "pinned_app_version", "7.2.17.0000"),
        ("backup", "remote", "somewhere"),
        ("profile", "name", "full"),
    ],
)
def test_the_fingerprint_changes_when_any_value_changes(library, section, key, value):
    """One case per top-level section, so a section left out of serialization is caught.

    Every section is covered, including ``modules``, which is the one a user is
    most likely to change and the one nothing else reaches: a job queued with
    analysis on and run after the user turned it off would report no drift.

    The change is MERGED into the section rather than replacing it, because
    ``library`` and ``paths`` carry required keys that a replacement would drop,
    and the config would then fail validation instead of fingerprinting
    differently.
    """
    base_data = valid_data(library)
    changed_data = valid_data(library)
    changed_data.setdefault(section, {})[key] = value

    base = config.from_dict(base_data)
    changed = config.from_dict(changed_data)
    assert changed.fingerprint() != base.fingerprint()


def test_a_default_valued_section_and_an_absent_one_fingerprint_alike(library):
    """An all-default section is the same configuration as no section at all."""
    absent = config.from_dict(valid_data(library))
    explicit = config.from_dict(valid_data(library, naming={"lossy_marker": "[MP3]"}))
    assert explicit.fingerprint() == absent.fingerprint()


# ═══════════════════════════════════════════════════════════════════════════
# Lazy resolution: no import-time side effects, no module-level snapshots
# ═══════════════════════════════════════════════════════════════════════════


def test_importing_the_config_module_creates_nothing(tmp_path):
    """Rule 1, proved in a real interpreter rather than by reading the source.

    This is what lets doctor and help run on a machine that has never been set
    up. A unit test that only called the functions would miss an import-time
    mkdir entirely, which is the exact side effect being forbidden.
    """
    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ)
    env.update(
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "CRATEKIT_CONFIG_DIR": str(tmp_path / "cfg"),
            "CRATEKIT_STATE_DIR": str(tmp_path / "state"),
        }
    )
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from cratekit.core import config; config.config_path(); "
            "config.installation_state_dir()",
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not (tmp_path / "cfg").exists()
    assert not (tmp_path / "state").exists()
    assert list(home.iterdir()) == []


def test_config_exposes_no_module_level_location_constant():
    """There is nothing to snapshot, which is why snapshotting cannot happen.

    Removing the constant is stronger than forbidding its use: the source system
    forbade nothing and seventeen modules bound a path at their own import time.
    """
    offenders = [
        name
        for name, value in vars(config).items()
        if not name.startswith("_") and isinstance(value, Path)
    ]
    assert not offenders, (
        f"cratekit.core.config exposes module-level Path constants {offenders}. "
        f"Every location is a function so that a caller cannot bind one at its "
        f"own import time and stop tracking later changes."
    )


#: Names a module is likely to bind the config module to.
_CONFIG_MODULE_ALIASES = frozenset({"config", "cfg", "_config"})

#: Functions that RESOLVE a location. Calling one at import time freezes the
#: answer, which is the same defect as reading an attribute, in different clothes.
_CONFIG_RESOLVERS = frozenset(
    {
        "load",
        "config_dir",
        "config_path",
        "installation_state_dir",
        "library_state_dir",
        # The three the library reorganization added. ``library_state_dir`` was
        # already here, so leaving its three siblings out would have made the
        # rule depend on which of four equivalent accessors somebody reached for.
        "library_coupled_dir",
        "library_history_dir",
        "library_local_dir",
        "state_path",
    }
)


def _called_name(func: ast.expr) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _deferred_nodes(tree: ast.AST) -> set[int]:
    """Ids of every node that only runs when something CALLS it.

    A read inside a function body or a lambda is not a snapshot: it happens at
    call time, with whatever config is current. Excluding them is what keeps the
    rule about binding at import rather than about mentioning config at all,
    which is the difference between a guard people obey and a guard people mute.
    """
    deferred: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda):
            for child in ast.walk(node):
                if child is not node:
                    deferred.add(id(child))
    return deferred


def module_level_config_snapshots(source: str, module: str) -> list[str]:
    """Return one message per module-level binding of a config-derived value.

    The rule: outside the config module itself, no assignment evaluated AT IMPORT
    may read a config attribute or call a config resolver. Class bodies count,
    because a class attribute is evaluated at import too.

    Detected as data flow rather than by name, because the failure has two shapes
    that look nothing alike: ``STATE = config.load().library.root`` and
    ``STATE = installation_state_dir()`` freeze the same value.
    """
    problems: list[str] = []
    tree = ast.parse(source)
    deferred = _deferred_nodes(tree)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign | ast.AnnAssign):
            continue
        if id(node) in deferred or node.value is None:
            continue
        for sub in ast.walk(node.value):
            if id(sub) in deferred:
                continue
            if (
                isinstance(sub, ast.Attribute)
                and isinstance(sub.value, ast.Name)
                and sub.value.id in _CONFIG_MODULE_ALIASES
            ):
                problems.append(
                    f"{module}: module-level binding of {ast.unparse(sub)!r}; "
                    f"read config where it is used, never at import time"
                )
            if isinstance(sub, ast.Call) and _called_name(sub.func) in _CONFIG_RESOLVERS:
                problems.append(
                    f"{module}: module-level call to {_called_name(sub.func)}(); a "
                    f"resolved location bound at import time stops tracking config"
                )
    return problems


def test_the_snapshot_lint_catches_an_attribute_binding():
    source = "from cratekit.core import config\nLIBRARY = config.load().library.root\n"
    assert module_level_config_snapshots(source, "cratekit.label.sweep")


def test_the_snapshot_lint_catches_a_resolver_call():
    source = "from cratekit.core.config import installation_state_dir\nSTATE = installation_state_dir()\n"
    assert module_level_config_snapshots(source, "cratekit.web.jobs")


def test_the_snapshot_lint_catches_a_class_attribute():
    """A class body runs at import, so a class attribute is the same snapshot."""
    source = "from cratekit.core import config\n\nclass Sweep:\n    root = config.load().library.root\n"
    assert module_level_config_snapshots(source, "cratekit.label.sweep")


def test_the_snapshot_lint_allows_reading_config_inside_a_function():
    """What correct code looks like, asserted so the guard cannot forbid it."""
    source = (
        "from cratekit.core import config\n\n"
        "def sweep():\n"
        "    return config.load().library.root\n"
    )
    assert module_level_config_snapshots(source, "cratekit.label.sweep") == []


def test_no_module_in_the_package_snapshots_config_at_import_time():
    """The real package. Empty today; the point is that it can never fill up."""
    problems: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        relative = path.relative_to(SRC_ROOT).as_posix()
        if relative == "cratekit/core/config.py":
            continue  # the module that DEFINES them
        parts = list(path.relative_to(SRC_ROOT).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        problems += module_level_config_snapshots(path.read_text(), ".".join(parts))
    assert not problems, "module-level config snapshots:\n" + "\n".join(problems)


# ═══════════════════════════════════════════════════════════════════════════
# Environment overrides relocate; they never supply
# ═══════════════════════════════════════════════════════════════════════════


def test_an_override_relocates_a_configured_value(library, tmp_path, monkeypatch):
    moved = tmp_path / "moved"
    moved.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(moved))
    assert config.from_dict(valid_data(library)).library.root == moved


def test_an_override_never_supplies_a_value_the_file_omitted(library, monkeypatch):
    """The distinction the whole override design rests on.

    An override that can SUPPLY a library root lets a machine with no setup at
    all resolve one from the environment and start writing to it, which is the
    "runs against the wrong volume" failure R38 exists to prevent.
    """
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    data = valid_data(library)
    del data["library"]["root"]
    assert any("library.root" in p for p in config.validate(data))


# ── The containment rule is decided where it LIVES: against the effective root ─


def test_a_containment_violation_created_by_the_override_is_not_validated_clean(
    library, tmp_path, monkeypatch
):
    """The rule used to be decided against one root and enforced against another.

    ``validate`` dug ``library.root`` out of the raw file mapping while the
    builder applied ``CRATEKIT_LIBRARY_ROOT``, so a file whose database sat under
    the root it NAMED validated clean while the running process read a different
    root entirely. Reproduced before the fix: validate returned no problems and
    ``db_is_inside_library_root()`` returned False on the very same config.

    The environment variable is set for real rather than simulated, because a
    synthetic root passed as an argument exercises the arithmetic and not the
    path where the two answers actually diverged.
    """
    relocated = tmp_path / "relocated"
    relocated.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(relocated))

    data = valid_data(library)  # names the stale root, database under it
    cfg = config.from_dict(data)

    # Whatever validate says, it must be saying it about the values the process
    # will actually use. The two answers can no longer differ.
    assert (config.validate(data) == []) is cfg.db_is_inside_library_root()


def test_a_relocated_root_carries_the_database_that_sat_under_it(
    library, tmp_path, monkeypatch
):
    """What "relocate" has to mean when the two values are related.

    The file records where the database sits RELATIVE to the library. Moving the
    library and leaving the database aims it into a tree that is no longer the
    library, and makes a legitimate remount fail the containment rule with
    nothing the user can act on.

    It is also a safety property this suite has been relying on without stating
    it: redirecting the library root is the whole mechanism keeping tests off the
    real rekordbox database, and before this the redirect moved the root while
    the database path stayed exactly where the file pointed it.
    """
    relocated = tmp_path / "relocated"
    relocated.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(relocated))

    cfg = config.from_dict(valid_data(library))

    assert cfg.library.root == relocated
    assert cfg.library.db_path == relocated / "db" / "master.db"
    assert cfg.db_is_inside_library_root()


def test_a_relocation_leaves_a_database_that_was_never_under_the_root_alone(
    library, tmp_path, monkeypatch
):
    """The other half, and the one that keeps the acknowledgment meaningful.

    A database outside the library was never expressed relative to it, so there
    is nothing to re-base. Dragging it along would silently move a path the user
    chose, and would quietly retire the recorded decision that goes with it.
    """
    outside = tmp_path / "elsewhere" / "master.db"
    relocated = tmp_path / "relocated"
    relocated.mkdir()
    data = valid_data(library)
    data["library"]["db_path"] = str(outside)
    data["library"]["db_outside_root_acknowledged_on"] = "2026-08-01"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(relocated))

    cfg = config.from_dict(data)

    assert cfg.library.db_path == outside
    assert cfg.db_is_inside_library_root() is False


def test_a_save_under_a_relocation_writes_a_file_that_loads_again(
    library, tmp_path, monkeypatch
):
    """The lockout, driven end to end through the real environment path.

    Before the fix this sequence produced a file the module refused to load:
    ``save`` serialized the relocated root beside the db_path the override had
    not touched, and the next load raised ConfigInvalid naming a containment
    violation on a file the user had never edited. Observed exactly that.
    """
    relocated = tmp_path / "relocated"
    relocated.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(relocated))

    path = tmp_path / "config.toml"
    path.write_bytes(tomli_w.dumps(valid_data(library)).encode("utf-8"))

    config.save(config.load_from_path(path), path)
    config.reset_cache()

    reloaded = config.load_from_path(path)  # must not raise
    assert reloaded.library.root == relocated
    assert reloaded.db_is_inside_library_root()


def test_saving_refuses_to_write_a_file_this_module_would_refuse_to_load(cfg, tmp_path):
    """The general guarantee, not the one instance of it.

    Re-basing makes the relocation case consistent, but the CLASS of failure is
    not about those two fields: any pair of values a validation rule relates can
    drift apart in memory, and a write is the moment a runtime inconsistency
    becomes a permanent one. Constructed straight through the dataclass, which is
    the only way to reach an invalid Config now that ``from_dict`` refuses one.
    """
    from dataclasses import replace  # noqa: PLC0415

    broken = replace(
        cfg,
        library=replace(cfg.library, db_path=tmp_path / "elsewhere" / "master.db"),
    )
    with pytest.raises(config.ConfigInvalid, match="is not under library.root"):
        config.save(broken, tmp_path / "config.toml")
    assert not (tmp_path / "config.toml").exists()


def test_the_config_directory_resolves_through_the_platform_library(monkeypatch, tmp_path):
    """KTD6, and R1's portability half: no hardcoded per-platform path."""
    monkeypatch.delenv(config.ENV_CONFIG_DIR, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    resolved = config.config_dir()
    assert resolved.name == "cratekit"
    assert tmp_path in resolved.parents


# ═══════════════════════════════════════════════════════════════════════════
# Loading, saving, memoization
# ═══════════════════════════════════════════════════════════════════════════


def test_a_missing_config_says_so_rather_than_returning_defaults(tmp_path):
    """Defaults for a config that was never written would silently invent a library."""
    with pytest.raises(config.ConfigMissing):
        config.load(tmp_path / "nothing.toml")


def test_unparseable_toml_names_the_file(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("this is not = = toml\n")
    with pytest.raises(config.ConfigCorrupt, match=re.escape(path.name)):
        config.load(path)


def test_a_rewritten_config_is_not_served_from_the_memo(cfg, library, tmp_path):
    """Memoization is keyed on file identity, and every write mints a new inode.

    That is what makes it safe for callers to call ``load()`` wherever they need
    a value instead of binding one at their own import time. Removing the reason
    to snapshot is the only thing that actually stops the snapshotting.
    """
    path = tmp_path / "config.toml"
    config.save(cfg, path)
    assert config.load(path).taxonomy.template == "default"

    # Replaced the way any external writer would, WITHOUT going through save(),
    # so the memo is not politely cleared for us. This is the case the cache key
    # has to survive on its own: another process, or a hand edit, swapped the
    # file under a long-lived reader.
    changed = config.from_dict(valid_data(library, taxonomy={"template": "second"}))
    staging = tmp_path / "staged.toml"
    staging.write_bytes(changed.to_toml_bytes())
    os.replace(staging, path)

    assert config.load(path).taxonomy.template == "second"


def test_the_default_location_round_trips_end_to_end(cfg):
    """Save with no path, load with no path. The path everything else will use.

    Worth its own test because every other test here names a file explicitly, and
    the default resolution is the one code path a user actually exercises.
    """
    written = config.save(cfg)
    assert written == config.config_path()
    assert config.load().fingerprint() == cfg.fingerprint()


def test_saving_creates_the_directory_only_when_it_writes(cfg, tmp_path):
    target = tmp_path / "deep" / "nested" / "config.toml"
    assert not target.parent.exists()
    config.save(cfg, target)
    assert target.is_file()


def test_a_failed_write_leaves_no_temporary_file_behind(cfg, tmp_path, monkeypatch):
    """The atomic-write contract, tested at its failure edge.

    The temp file is created in the TARGET's directory so ``os.replace`` is a
    same-filesystem rename. If the replace never happens, the temp file must not
    survive, or every failed save leaves litter that looks like a real config.
    """
    target = tmp_path / "config.toml"
    config.save(cfg, target)
    before = sorted(p.name for p in tmp_path.iterdir())

    def boom(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError, match="disk full"):
        config.save(cfg, target)

    assert sorted(p.name for p in tmp_path.iterdir()) == before


# ═══════════════════════════════════════════════════════════════════════════
# Credentials (R4)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_read_with_no_keychain_backend_raises_rather_than_returning_nothing(monkeypatch):
    """The plan's fifth scenario.

    Returning None here is how a caller ends up sending a request with no
    credential at all and reading the 401 back as the service being down. The
    remediation is to install a backend, which is not the same advice as either
    of the other two failures.
    """

    def no_backend(*args, **kwargs):
        raise keyring.errors.NoKeyringError("no backend")

    monkeypatch.setattr(keyring, "get_password", no_backend)

    with pytest.raises(secrets.CredentialBackendUnavailable) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert excinfo.value.remedy is secrets.Remedy.INSTALL_KEYCHAIN_BACKEND


def test_an_absent_credential_is_a_different_failure_from_a_broken_backend():
    with pytest.raises(secrets.CredentialMissing) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert excinfo.value.remedy is secrets.Remedy.SET_CREDENTIAL


def test_the_three_credential_failures_carry_three_different_remedies():
    """A missing credential and a rejected one need OPPOSITE remediations.

    Collapsing them into one error forces every caller to parse a message string
    to decide what to tell the user, which is precisely the failure KTD25 names.
    """
    remedies = {
        secrets.CredentialBackendUnavailable.remedy,
        secrets.CredentialMissing.remedy,
        secrets.CredentialRejected.remedy,
    }
    assert len(remedies) == 3


def test_a_remedy_is_a_token_and_not_the_command_a_user_types():
    """D2: no foundation module contains a verb string.

    The CLI renders a token into a command, because the command depends on the
    interface the user is sitting in front of and this layer does not know which.
    """
    for remedy in secrets.Remedy:
        assert " " not in remedy.value
        assert "crate " not in remedy.value


def test_recording_and_reading_a_credential_round_trips():
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"


def test_a_multi_field_credential_is_stored_as_one_blob():
    """Several entries can be updated apart; one blob cannot.

    A half-refreshed session authenticates once and then fails in a way that
    looks like the service being down.
    """
    payload = {"token": "NOT-A-REAL-1", "refresh": "NOT-A-REAL-2", "kind": "pkce"}
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, payload)
    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == payload


def test_an_empty_credential_is_refused_rather_than_stored():
    with pytest.raises(secrets.CredentialMissing):
        secrets.set(secrets.Credential.IDENTIFY_KEY, "")


def test_presence_is_answered_without_retrieving_the_value(monkeypatch):
    """Doctor asks this on every run and must not raise the keychain's prompt.

    On macOS, retrieving a value from a process the user has not authorized
    raises an interactive dialog. In an unattended health check that means the
    run hangs rather than reports.
    """
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    def must_not_be_called(*args, **kwargs):
        raise AssertionError("presence check retrieved the credential value")

    monkeypatch.setattr(keyring, "get_password", must_not_be_called)
    assert secrets.exists(secrets.Credential.IDENTIFY_KEY)
    assert secrets.Credential.IDENTIFY_KEY in secrets.recorded()


def test_deleting_a_credential_clears_it_from_the_presence_index():
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    secrets.delete(secrets.Credential.IDENTIFY_KEY)
    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)
    with pytest.raises(secrets.CredentialMissing):
        secrets.get(secrets.Credential.IDENTIFY_KEY)


def test_the_presence_index_records_names_and_never_values():
    """The index is installation-scoped state. It must be safe to read."""
    secrets.set(secrets.Credential.IDENTIFY_SIGNING_KEY, "value-from-the-user")
    payload = json.loads(config.state_path("credential_index").read_text())
    assert payload["recorded"] == [secrets.Credential.IDENTIFY_SIGNING_KEY.value]
    assert "value-from-the-user" not in json.dumps(payload)


def test_the_environment_fallback_is_opt_in_and_never_silent(monkeypatch):
    """No silent fallbacks: not to a file, not to an empty string, not to the environment.

    The failure being avoided is an unauthenticated request that looks like a
    service outage. An override the user did not ask for is the same failure with
    a different cause.
    """
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_IDENTIFY_KEY", "value-from-the-env")
    monkeypatch.delenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, raising=False)

    with pytest.raises(secrets.CredentialMissing) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert "value-from-the-env" not in str(excinfo.value)

    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-env"


def test_the_backend_refusal_names_the_opt_in_rather_than_taking_it(monkeypatch):
    def no_backend(*args, **kwargs):
        raise keyring.errors.NoKeyringError("no backend")

    monkeypatch.setattr(keyring, "get_password", no_backend)
    with pytest.raises(secrets.CredentialBackendUnavailable) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert secrets.ENV_ALLOW_ENV_CREDENTIALS in str(excinfo.value)


def test_the_keychain_service_is_not_namespaced_per_library():
    """A credential is an account fact, not a library fact (KTD21).

    Namespacing by library would make one account's token get re-entered once per
    library the user owns.
    """
    assert secrets.SERVICE == "cratekit"


# ── Permissions do not depend on the user's umask ────────────────────────────


@pytest.fixture
def permissive_umask():
    """Run the body under umask 000, then put the process back.

    A test that does not manipulate the umask cannot see this defect at all: on
    the author's machine the umask is 022 and a plain write lands 0644, which
    looks fine until somebody with a laxer umask runs the same code.
    """
    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


def _drive_every_write_path(cfg) -> list[Path]:
    """Exercise every way this unit puts something on disk. Returns the roots.

    Listed as OPERATIONS, not as files. That is the point: the audit below walks
    whatever these produce, so a future writer is covered by adding its operation
    here rather than by remembering to add its filename to an assertion.
    """
    # A credential, which creates the installation STATE directory and the
    # presence index inside it.
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    # The config file, which creates the installation CONFIG directory.
    config.save(cfg)
    # A library-scoped write, which creates the library state directory AND a
    # role subdirectory under it: two levels, so an intermediate directory
    # created at the default mode shows up.
    config.atomic_write_bytes(b"{}\n", config.state_path("tree_registry", cfg))
    # A migration, which creates the lock file and a versioned backup beside the
    # config. The lock is the writer the hand-enumerated version of this test
    # missed entirely.
    migrating = config.config_dir() / "migrating.toml"
    data = valid_data(cfg.library.root)
    data["schema_version"] = 1
    config.atomic_write_bytes(tomli_w.dumps(data).encode("utf-8"), migrating)
    config.load_from_path(migrating, current=2, migrations={1: lambda d: d})

    return [
        config.config_dir(),
        config.installation_state_dir(),
        config.library_state_dir(cfg),
    ]


def test_every_file_and_directory_this_unit_creates_is_private_under_any_umask(
    permissive_umask, cfg
):
    """The defect class this whole module was chartered to end, audited rather than listed.

    The source system's credential files are 0600 because of the author's umask
    rather than because of any code, so on a machine with a laxer umask they land
    world readable. The presence index carries no credential VALUES, but under
    umask 000 a plain write lands world WRITABLE, and that is enough: any other
    local account can add a name, making doctor report a credential is set when
    the keychain has nothing, or remove one, making a working install report as
    unconfigured.

    THE DIRECTORY IS PART OF THE FILE'S MODE, which the first version of this
    test could not see. Unlink and rename are governed by the DIRECTORY's
    permissions, so a 0600 file inside a 0777 directory can still be deleted and
    replaced by any local account: the file's mode is intact and the property it
    was supposed to provide is gone. Both were observed at 0o777.

    IT WALKS RATHER THAN ENUMERATES, and that is the difference that matters. The
    version this replaces hand-listed two files, so its name was false the moment
    a third writer appeared, and one had: the migration lock file landed 0666 and
    the suite stayed green with it sitting there. A test that enumerates is a test
    that misses the next writer, so this one drives the write paths and then
    audits whatever turned up.
    """
    roots = _drive_every_write_path(cfg)

    offenders: list[str] = []
    seen_files = 0
    seen_dirs = 0
    for root in roots:
        assert root.is_dir(), f"{root} was not created by any write path"
        for path in [root, *root.rglob("*")]:
            mode = stat.S_IMODE(path.stat().st_mode)
            if path.is_dir():
                seen_dirs += 1
                if mode != config.PRIVATE_DIR_MODE:
                    offenders.append(f"{path} is a directory at {oct(mode)}")
            else:
                seen_files += 1
                if mode != config.PRIVATE_FILE_MODE:
                    offenders.append(f"{path} is a file at {oct(mode)}")

    assert not offenders, (
        "created under umask 000 at a mode that depends on the umask:\n"
        + "\n".join(offenders)
    )
    # The walk has to have found something, or a green result would only mean the
    # write paths above quietly stopped writing.
    assert seen_files >= 4 and seen_dirs >= 4, (
        f"the audit only saw {seen_files} files and {seen_dirs} directories, "
        f"which is too few for the write paths it drove"
    )


def test_the_migration_lock_file_is_one_of_the_files_that_audit_covers(
    permissive_umask, cfg
):
    """Named explicitly, because it is the writer the enumerated test missed.

    It also persists after a successful migration, on purpose: unlinking a lock
    file lets a second process create a new inode at the same name and take a
    second lock on it, so both processes believe they hold the only one. The mode
    is what makes persisting harmless, so the mode is what is asserted.
    """
    _drive_every_write_path(cfg)

    locks = sorted(config.config_dir().rglob("*.migrate.lock"))
    assert locks, "the migration never took a lock, so this asserts nothing"
    for lock in locks:
        assert stat.S_IMODE(lock.stat().st_mode) == config.PRIVATE_FILE_MODE


def _bare_mkdir_calls(source: str) -> list[str]:
    """Return every ``.mkdir(...)`` that is not the one inside the private helper.

    A directory created straight through ``Path.mkdir`` takes its mode from the
    umask, and with ``parents=True`` its intermediate levels take 0o777 no matter
    what mode was asked for. So the rule is that every creation in this module
    goes through one function, and this is what keeps that true.
    """
    tree = ast.parse(source)
    inside_helper: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_mkdir_private":
            for child in ast.walk(node):
                inside_helper.add(id(child))

    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or id(node) in inside_helper:
            continue
        if isinstance(node.func, ast.Attribute) and node.func.attr == "mkdir":
            found.append(ast.unparse(node))
    return found


def test_the_bare_mkdir_lint_catches_a_creation_that_skips_the_helper():
    source = 'def save(path):\n    path.parent.mkdir(parents=True, exist_ok=True)\n'
    assert _bare_mkdir_calls(source)


def test_every_directory_the_config_module_creates_goes_through_the_private_helper():
    """One creator, so one place decides the mode. Also keeps the docstrings true.

    ``save`` used to claim it was "the one function in the module that creates a
    directory". Two others did by then, both added in the previous fix round, and
    in a module whose docstrings carry the rules an inaccurate claim about
    directory creation is not cosmetic: it is the sentence a reader trusts instead
    of checking. Routing every creation through one helper makes the claim
    checkable, and this is the check.
    """
    source = (SRC_ROOT / "cratekit" / "core" / "config.py").read_text()
    offenders = _bare_mkdir_calls(source)
    assert not offenders, (
        "directories created outside _mkdir_private:\n"
        + "\n".join(offenders)
        + "\nPath.mkdir takes its mode from the umask, and with parents=True it "
        "creates intermediate levels at 0o777 regardless of the mode given."
    )
    assert "one function in the module that creates a directory" not in source, (
        "save's docstring claims to be the only directory creator; three "
        "functions create one"
    )


def test_a_migration_backup_gets_the_same_mode_as_the_file_it_copies(
    permissive_umask, library, tmp_path
):
    """A migration must not produce a laxer-permissioned duplicate of the config.

    Config carries no credentials today, so the exposure is library paths and
    backup destinations. It is still the same function being careful about
    atomicity and careless about mode, and it matters the moment anything
    sensitive joins the schema.
    """
    path = tmp_path / "config.toml"
    data = valid_data(library)
    data["schema_version"] = 1
    path.write_text(tomli_w.dumps(data))

    config.load_from_path(path, current=2, migrations={1: lambda d: d})

    backup = tmp_path / "config.toml.v1.bak"
    assert stat.S_IMODE(backup.stat().st_mode) == 0o600


# ── The keychain is an external system, so its failures are not a closed set ──


def test_a_backend_that_fails_with_an_unexpected_type_still_refuses_typed(monkeypatch):
    """Not hypothetical on the second platform R1 cares about.

    keyring's SecretService backend calls into D-Bus outside its own try block, so
    a headless machine with no session bus raises an exception that is not a
    KeyringError, and its ``priority`` classproperty raises a bare RuntimeError.
    Either escapes an ``except KeyringError`` handler untyped and with no remedy,
    and the CLI's CredentialError handler never sees it.
    """

    def dead_session_bus(*args, **kwargs):
        raise RuntimeError("Unable to initialize SecretService: no session bus")

    for name in ("get_password", "set_password", "delete_password"):
        monkeypatch.setattr(keyring, name, dead_session_bus)

    with pytest.raises(secrets.CredentialBackendUnavailable):
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    with pytest.raises(secrets.CredentialBackendUnavailable):
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    with pytest.raises(secrets.CredentialBackendUnavailable):
        secrets.delete(secrets.Credential.IDENTIFY_KEY)


def test_the_doctor_probe_reports_false_rather_than_raising(monkeypatch):
    """Doctor is the command a user runs precisely when the keychain is broken.

    keyring's backends define ``priority`` as a classproperty that raises when the
    backend is not viable on this machine. Reading it outside the try turns a
    health check into an unhandled traceback on exactly the machine it exists to
    diagnose.
    """

    class _NotViableHere:
        @property
        def priority(self):
            raise RuntimeError("this backend is not viable here")

    monkeypatch.setattr(keyring, "get_keyring", lambda: _NotViableHere())
    assert secrets.backend_available() is False


def test_a_backend_that_accepts_a_write_and_stores_nothing_refuses(monkeypatch):
    """The null backend is the documented way to disable keyring on a headless box.

    Its ``set_password`` is a no-op that raises nothing, so the module's own
    argument that "the exception is an observation" has no observation to make.
    Without a read-back the credential is silently discarded, the presence index
    records it anyway, and the user loops forever: doctor says the credential is
    present, every read says it is missing, and re-recording it changes nothing.
    """
    backend = keyring.backends.null.Keyring()
    monkeypatch.setattr(keyring, "set_password", backend.set_password)
    monkeypatch.setattr(keyring, "get_password", backend.get_password)

    with pytest.raises(secrets.CredentialBackendUnavailable):
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)
    assert secrets.Credential.IDENTIFY_KEY not in secrets.recorded()


# ── D2: a foundation module carries a remedy token, never a command line ─────


def test_every_config_failure_carries_a_structured_remedy():
    """KTD25 again, in the module that raises the most types.

    A caller deciding between "run setup", "upgrade Cratekit", and "fix these
    values" by string-matching a message is exactly the failure the typed
    vocabulary exists to prevent.
    """
    for kind in (
        config.ConfigMissing,
        config.ConfigCorrupt,
        config.ConfigTooNew,
        config.ConfigInvalid,
        config.ConfigLockUnavailable,
    ):
        assert isinstance(kind.remedy, config.Remedy)

    remedies = {
        config.ConfigMissing.remedy,
        config.ConfigCorrupt.remedy,
        config.ConfigTooNew.remedy,
        config.ConfigInvalid.remedy,
        config.ConfigLockUnavailable.remedy,
    }
    assert len(remedies) == 5, "collapsed remedies force callers back to string matching"


def test_a_config_remedy_is_a_token_and_not_the_command_a_user_types():
    for remedy in config.Remedy:
        assert " " not in remedy.value
        assert "crate " not in remedy.value


def test_the_unset_pin_refusal_carries_its_own_remedy(cfg):
    """Its remediation is not "fix these values", it is "record this one thing"."""
    with pytest.raises(config.ConfigInvalid) as excinfo:
        cfg.assert_rekordbox_pin_recorded()
    assert excinfo.value.remedy is config.Remedy.RECORD_REKORDBOX_PIN


def test_a_missing_config_carries_the_setup_remedy_rather_than_prose(tmp_path):
    with pytest.raises(config.ConfigMissing) as excinfo:
        config.load(tmp_path / "nothing.toml")
    assert excinfo.value.remedy is config.Remedy.RUN_SETUP


# ═══════════════════════════════════════════════════════════════════════════
# Values the file supplies, and the ones it must be type-checked on
# ═══════════════════════════════════════════════════════════════════════════


def test_the_library_root_is_read_from_the_file_when_nothing_relocates_it(
    library, monkeypatch
):
    """The suite's autouse isolation sets the relocation override for every test.

    So the file's own value is never exercised anywhere else, and a regression
    that ignored ``library.root`` from the file entirely would pass the whole
    suite. Deleting the variable inside the test is the seam; the conftest fixture
    is not this file's to change.
    """
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT, raising=False)
    assert config.from_dict(valid_data(library)).library.root == library


@pytest.mark.parametrize("key", ["path_budget_bytes", "filename_max_bytes"])
def test_a_naming_budget_that_is_not_an_integer_is_named_at_load(library, key):
    """S3 hands these to a pure engine as parameters.

    A string budget therefore surfaces as a TypeError deep inside a rename rather
    than as a named problem while the user is still looking at their config.
    """
    problems = config.validate(valid_data(library, naming={key: "250"}))
    assert any(key in p for p in problems), problems
