"""U2: the config schema, the two state roots, profiles, and credentials.

Four things are proved here, each failing a different way:

1. **Validation names every missing key**, not the first, so a first run
   wizard costs one round trip rather than one per missing value.
2. **Every state file has exactly one root, and the right one.** The inventory
   is audited whole, because a file on the wrong root fails only on a second
   install, a reinstall or the migration overlap.
3. **Nothing snapshots config at import time.** The lint makes the source
   system's import time path binding impossible to introduce.
4. **A credential failure says which of three things went wrong**, since a
   missing credential and a rejected one need opposite remediations.

The checkers follow ``test_layering.py``: pure functions over source text,
fixture tests proving each rule bites, then one run over the real package.
"""

from __future__ import annotations

import ast
import functools
import json
import os
import re
import stat
import subprocess
import sys
import tomllib
import unicodedata
from collections import deque
from pathlib import Path

import keyring
import keyring.backends.null
import keyring.errors
import pytest
import tomli_w

from cratekit.core import config, config_validate, profiles, secrets
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"


@functools.cache
def parsed(source: str) -> ast.Module:
    """``ast.parse``, once per text in a process: guards here walk the whole package."""
    return ast.parse(source)


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A per test library root, with the conftest override re-pointed at it to agree."""
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


# Validation names EVERY missing key.


def test_a_config_missing_required_keys_names_each_one():
    """All of them, not the first: one round trip per missing value loses the user."""
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
    """Asserted because "required" grows silently; each addition should be a diff."""
    assert len(config.REQUIRED_KEYS) == 6


# R38: the volume identity key and its validation.


def test_a_volume_identity_that_is_a_mount_path_is_rejected(library):
    """R38 identifies a volume by recorded identity, never by where it mounts."""
    data = valid_data(library)
    data["library"]["volume_id"] = str(library)
    problems = config.validate(data)
    assert any(config.VOLUME_IDENTITY_KEY in p and "mount path" in p for p in problems)


def test_the_volume_identity_key_is_published_for_the_assertion_to_read():
    """U31 reads the key from here, so a rename cannot leave its guard behind."""
    assert config.VOLUME_IDENTITY_KEY == "library.volume_id"


# Profiles toggle module membership and nothing else (D6).


def test_a_profile_change_toggles_membership_without_touching_unrelated_keys(library):
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
    added = profiles.resolve("slim", {"analysis": True})
    assert "analysis" in added.modules
    assert added.overridden == frozenset({"analysis"})

    removed = profiles.resolve("full", {"vocals": False})
    assert "vocals" not in removed.modules
    assert removed.overridden == frozenset({"vocals"})


def test_switching_profiles_preserves_the_users_own_toggles(library):
    """A profile is a preset, not a reset: a module the user turned off stays off."""
    data = valid_data(library, modules={"desktop": False})
    after = profiles.apply(data, "full")
    assert after["modules"] == {"desktop": False}
    assert "desktop" not in config.from_dict(after).enabled_modules()


def test_a_profile_change_returns_a_copy_the_caller_cannot_edit_backwards(library):
    """A shallow copy aliases the nested tables, which an equality check passes."""
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
    """KTD7: extras are one to one with modules, read from ``pyproject.toml`` so it cannot drift."""
    with (REPO_ROOT / "pyproject.toml").open("rb") as handle:
        extras = tomllib.load(handle)["project"]["optional-dependencies"]
    declared = set(extras) - {"all", "dev"}
    assert declared == set(profiles.EXTRAS_BACKED)
    assert profiles.EXTRAS_BACKED <= set(profiles.MODULES)


def test_a_module_without_a_heavy_dependency_reports_no_extras_group():
    """None is an answer, not a gap: some modules need nothing extra installed."""
    assert profiles.install_command("analysis") == "analysis"
    assert profiles.install_command("favorites") is None


# The two state roots (KTD21).


def test_there_are_exactly_two_state_roots():
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
    """Two entries at one path is one writer silently overwriting the other."""
    seen: dict[Path, str] = {}
    for entry in config.STATE_FILES:
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        path = config.state_path(entry.key, cfg)
        assert path not in seen, f"{entry.key} collides with {seen.get(path)} at {path}"
        seen[path] = entry.key


def test_installation_state_never_lands_under_the_library(cfg, library):
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


# An entry must resolve where the code that reads and writes it looks.


@pytest.fixture
def split_installation_dirs(monkeypatch, tmp_path):
    """Force the two installation directories apart; macOS platformdirs makes them one."""
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "installation-config"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "installation-state"))
    assert config.config_dir() != config.installation_state_dir()
    return tmp_path


#: Inventory entries that also have a named accessor, where two pieces of code
#: can disagree about one path.
_NAMED_ACCESSORS = {
    "config": lambda: config.config_path(),
    "credential_index": lambda: secrets._index_path(),
}


def test_every_entry_with_a_named_accessor_resolves_to_the_same_path(
    split_installation_dirs,
):
    """Catches an entry under the wrong installation directory, which the root audits cannot."""
    for key, accessor in _NAMED_ACCESSORS.items():
        assert config.state_path(key) == accessor(), (
            f"{key} is declared at {config.state_path(key)} but the code that "
            f"reads and writes it uses {accessor()}. One file, two roots, is the "
            f"straddling the Definition of Done forbids."
        )


def test_every_installation_entry_resolves_under_a_directory_the_module_names(
    split_installation_dirs,
):
    """Stated positively, so an invented directory fails here."""
    # The provider gate's own directory (U278) is the third the module names.
    known = (config.config_dir(), config.installation_state_dir(), config.provider_gate_dir())
    for entry in config.state_files_for(config.StateRoot.INSTALLATION):
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        path = config.state_path(entry.key)
        assert any(directory in path.parents for directory in known), (
            f"{entry.key} resolves to {path}, which is under neither the "
            f"installation config directory nor the installation state directory"
        )


#: Every config function handing out a directory under a state root. Must be
#: complete, kept so by the export test below.
_STATE_ROOT_ACCESSORS = {
    "config_dir",
    "installation_state_dir",
    "provider_gate_dir",
    "library_state_dir",
    "library_coupled_dir",
    "library_history_dir",
    "library_local_dir",
}


def _paths_composed_from_a_state_root(source: str) -> list[str]:
    """Every path built under a state root directly: a state file the inventory misses."""
    found: list[str] = []
    for node in ast.walk(parsed(source)):
        if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Div):
            continue
        left = node.left
        if isinstance(left, ast.Call) and _called_name(left.func) in _STATE_ROOT_ACCESSORS:
            found.append(ast.unparse(node))
    return found


@pytest.mark.parametrize(
    "source",
    [
        'from cratekit.core.config import installation_state_dir\n\ndef p():\n    return installation_state_dir() / "mine.json"\n',
        'def p(cfg):\n    return library_coupled_dir(cfg) / "mine.json"\n',
        'def p(cfg):\n    return library_history_dir(cfg) / "mine.json"\n',
        'def p(cfg):\n    return library_local_dir(cfg) / "mine.json"\n',
    ],
    ids=["installation-state-dir", "library-coupled-dir", "library-history-dir", "library-local-dir"],
)
def test_the_composed_path_lint_catches_a_module_inventing_its_own_state_file(source):
    """The last three are the accessors the reorganization added and the lint first missed."""
    assert _paths_composed_from_a_state_root(source)


def test_the_composed_path_lint_covers_every_directory_accessor_the_module_exports():
    """The next exported accessor fails the build rather than escaping the guard."""
    exported = {name for name in config.__all__ if name.endswith("_dir")}
    missing = exported - _STATE_ROOT_ACCESSORS
    assert not missing, (
        f"config exports directory accessors the composed-path lint does not "
        f"know about: {sorted(missing)}. Add them to _STATE_ROOT_ACCESSORS, or "
        f"the first module to compose a path onto one is invisible to the guard."
    )


#: The modules that define the roots and resolve the inventory over them.
INVENTORY_MODULES = frozenset({"cratekit/core/config.py", "cratekit/core/state_files.py"})


@pytest.mark.parametrize(
    "key",
    ["write_lock", "session_lock", "session_log", "snapshots", "favorites_state"],
)
def test_the_locks_the_log_and_the_snapshots_live_with_the_library(key, cfg, library):
    """KTD17, R31, KTD21b and KTD21: two installs must not mean two locks on one database."""
    assert config.state_file(key).root is config.StateRoot.LIBRARY
    assert library in config.state_path(key, cfg).parents


def test_the_job_queue_stays_with_the_installation(cfg):
    """A detached job belongs to the machine running it, so its record names its library."""
    entry = config.state_file("job_queue")
    assert entry.root is config.StateRoot.INSTALLATION
    assert "library it targets" in entry.why
    # Resolvable with no config, so the queue reads with the library unmounted.
    assert config.state_path("job_queue") == config.installation_state_dir() / "jobs"


def test_the_per_set_workspaces_resolve_from_configured_directory_names(cfg, library):
    """Inside the sets directory, never it: it holds the user's own recordings."""
    resolved = config.state_path("set_workspaces", cfg)
    sets_dir = library / cfg.library.music_dir / cfg.library.sets_dir
    assert resolved.parent == sets_dir
    assert resolved != sets_dir


# KTD21b: the snapshot boundary is declared in the schema, not kept as a list.


def test_every_state_entry_declares_a_snapshot_role():
    """Without a role per entry, U8 and U32 would hand keep an exclusion list that drifts."""
    for entry in config.STATE_FILES:
        assert entry.snapshot in config.SnapshotRole, (
            f"{entry.key} does not say whether a restore rolls it back"
        )


def test_the_locks_and_the_snapshot_store_are_not_in_the_coupled_set():
    """A restored lock swaps the inode a live lock holds; a restored store nests snapshots."""
    coupled = {entry.key for entry in config.coupled_state_files()}
    for key in (
        "write_lock",
        "session_lock",
        "favorites_state_lock",
        "snapshots",
        "session_log",
    ):
        assert key not in coupled, f"{key} must not roll back with the database"
    # Derived as well as named (P3), so a lock added later is covered too.
    for entry in config.STATE_FILES:
        if any(part.startswith("lock") for part in entry.key.split("_")):
            assert entry.key not in coupled, (
                f"{entry.key} is a lock inside the coupled set, so a restore "
                f"swaps the inode a live lock is held on and every holder keeps "
                f"believing it has exclusive access"
            )


_SURVIVES = config.SnapshotRole.SURVIVES_ROLLBACK
_NEVER = config.SnapshotRole.NEVER_RESTORED
_COUPLED = config.SnapshotRole.COUPLED


@pytest.mark.parametrize(
    "key, role",
    [
        ("snapshots", _SURVIVES),
        ("session_log", _SURVIVES),
        # The undo logs hold the only copy of a value overwritten on disk.
        ("energy_undo_log", _NEVER),
        ("genre_tag_undo_log", _NEVER),
        # R30 names the coupled state by name.
        ("tree_registry", _COUPLED),
        ("label_watermarks", _COUPLED),
        ("source_watermarks", _COUPLED),
        ("deletion_watermark", _COUPLED),
        ("tombstones", _COUPLED),
        ("declines", _COUPLED),
        ("taxonomy_active", _COUPLED),
        ("favorites_state", _COUPLED),
        ("rekordbox_db", _COUPLED),
    ],
    ids=lambda value: value if isinstance(value, str) else value.name.lower(),
)
def test_each_named_entry_carries_its_declared_snapshot_role(key, role):
    assert config.state_file(key).snapshot is role, key


def test_the_coupled_set_is_a_directory_boundary_rather_than_a_list(cfg):
    """Every coupled entry sits in a snapshot source, and nothing else sits in the coupled directory."""
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


# The capture set is WAL aware, because a database is not one file.


def test_the_capture_set_includes_the_databases_sqlite_sidecars(cfg):
    """A capture of ``<db>`` alone opens cleanly and silently lacks the uncheckpointed ``-wal``."""
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
    entry = config.state_file("rekordbox_db")
    assert entry.sidecars == config.SQLITE_SIDECARS
    assert [s.suffix for s in entry.sidecars] == ["-wal", "-shm"]
    # Every other entry is a single file, and says so.
    for other in config.STATE_FILES:
        if other.key != "rekordbox_db":
            assert other.sidecars == ()


def test_a_restore_writes_back_the_log_and_never_the_shared_memory_index(cfg):
    """A stale ``-shm`` beside a fresh log gives SQLite two views of one database."""
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


# The consumers are held to the derivation by text guards.


def test_the_capture_unit_derives_its_source_set_rather_than_listing_it():
    """U8 must reach for ``snapshot_sources`` and type no sidecar suffix of its own."""
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


def test_the_restore_unit_derives_its_target_set_rather_than_listing_it():
    """A text search only; ``tests/test_restore.py`` drives whether the derivation is used."""
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
    """The field is read only for installation entries, so it stays unset elsewhere."""
    for entry in config.state_files_for(config.StateRoot.LIBRARY):
        assert entry.installation_area is config.InstallationArea.STATE


# The database is state too, and KTD21b needs it beside its coupled state.


def test_the_rekordbox_database_is_declared_library_scoped_state(cfg):
    entry = config.state_file("rekordbox_db")
    assert entry.root is config.StateRoot.LIBRARY
    assert config.state_path("rekordbox_db", cfg) == cfg.library.db_path


def test_a_database_outside_the_library_root_refuses_until_it_is_acknowledged(
    library, tmp_path
):
    """A database on another filesystem has no rename based atomic commit with its coupled state."""
    data = valid_data(library)
    data["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")

    problems = config.validate(data)

    assert any("db_path" in p and "library.root" in p for p in problems), problems


def test_an_acknowledged_database_outside_the_library_root_loads_and_says_so(
    library, tmp_path
):
    """Permitted only as a recorded decision, visible at setup."""
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
    """The acknowledgment records WHEN, so ``no`` must not disable the rule it reads as enforcing."""
    data = valid_data(library)
    data["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")
    data["library"]["db_outside_root_acknowledged_on"] = value

    problems = config.validate(data)

    assert any(config.ACKNOWLEDGMENT_KEY in p and "date" in p for p in problems), problems
    assert any("is not under library.root" in p for p in problems), problems


def test_a_malformed_acknowledgment_is_named_even_when_the_database_is_contained(cfg, library):
    """A bad date is a defect whether or not it is load bearing today."""
    data = valid_data(library)
    data["library"]["db_outside_root_acknowledged_on"] = "someday"
    assert any(config.ACKNOWLEDGMENT_KEY in p for p in config.validate(data))


def test_the_library_state_layout_carries_no_migration_because_nothing_wrote_another_one():
    """A deferral with a countdown: dict to dict migrations cannot move a file."""
    assert config.LIBRARY_STATE_LAYOUT_VERSION == 1, (
        "the library state layout changed. Config migrations are dict-to-dict "
        "and cannot move a file, so the unit that changed it owns a one-time "
        "on-disk reconciliation with its own mechanism, run under the same "
        "exclusive lock, idempotent, and refusing rather than half-moving. Add "
        "it, then update this test to cover it."
    )


def test_doctor_reports_a_database_that_sits_outside_the_library_root(
    library, tmp_path, monkeypatch
):
    """ARMED by U27. Asserted on what the OK branch cannot produce, not on "atomic"."""
    from cratekit.cli import doctor

    outside = tmp_path / "elsewhere" / "master.db"
    data = valid_data(library)
    data["library"]["db_path"] = str(outside)
    data["library"]["db_outside_root_acknowledged_on"] = "2026-08-01"
    acknowledged = config.from_dict(data)
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: acknowledged)

    report = doctor.run()

    finding = next(f for f in report.findings if f.key == "library.db_containment")
    assert finding.status is doctor.Status.INFO, finding.detail
    assert str(outside) in finding.detail
    assert str(library) in finding.detail
    assert "2026-08-01" in finding.detail
    assert "two filesystems" in finding.detail
    assert "commits atomically with a rename" not in finding.detail


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
    """D4: one file with two owners is the problem, so each half has its own root."""
    install = config.state_file(install_key)
    library_side = config.state_file(library_key)
    assert install.root is config.StateRoot.INSTALLATION
    assert library_side.root is config.StateRoot.LIBRARY
    assert install.relative != library_side.relative


# D5: no persisted record is keyed by a display name.


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
    """An unresolvable record is the orphan the rule exists to surface."""
    migrated, unresolved = config.rekey_records({"Gone": {}}, lambda _: None)
    assert migrated == {}
    assert unresolved == ("Gone",)


# Seam decisions that live in this schema.


def test_the_prefix_map_is_ordered_and_first_match_wins(library):
    """S1. Order is load bearing: one prefix can be another's prefix."""
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
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [{"from": "/mnt/volume", "to": "{library.root}"}]

    moved = tmp_path / "elsewhere"
    moved.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(moved))

    assert config.from_dict(data).resolved_prefix_map() == (("/mnt/volume", str(moved)),)


@pytest.mark.parametrize(
    "rule, expected",
    [
        ({"from": "/mnt/volume", "to": "{home}"}, "unsupported interpolation"),
        ({"from": "/mnt/volume"}, "location_prefix_map[0].to"),
    ],
    ids=["unsupported-interpolation", "malformed-entry-named-by-index"],
)
def test_a_bad_prefix_rule_is_named(library, rule, expected):
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [rule]
    assert any(expected in p for p in config.validate(data))


def test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at(library):
    """A rule onto another disk says WHICH disk, and keeps it through a round trip."""
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [
        {"from": "/mnt/music", "to": "/Volumes/MUSIC", "volume_id": "AAAA-1111"},
        {"from": "/mnt/volume", "to": "{library.root}"},
    ]
    cfg = config.from_dict(data)

    assert cfg.resolved_prefix_rules() == (
        ("/mnt/music", "/Volumes/MUSIC", "AAAA-1111"),
        ("/mnt/volume", str(library), None),
    )
    again = config.from_dict(cfg.to_toml_dict())
    assert again.resolved_prefix_rules() == cfg.resolved_prefix_rules()
    assert again.fingerprint() == cfg.fingerprint()


def test_a_rule_with_no_identity_serializes_to_the_bytes_it_always_did(library):
    """KTD9. Spelled out, so a writer emitting an empty key for every rule fails."""
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [{"from": "/mnt/volume", "to": "{library.root}"}]
    written = config.from_dict(data).to_toml_dict()["library"]["location_prefix_map"]

    assert written == [{"from": "/mnt/volume", "to": "{library.root}"}]


@pytest.mark.parametrize(
    "identity",
    ["/Volumes/MUSIC", "\\\\server\\share", "E:\\", "", "   ", 7, None],
    ids=["posix-path", "unc-path", "drive-path", "empty", "blank", "number", "null"],
)
def test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index(library, identity):
    """R38 per rule. A present but unusable key is a problem, never "none recorded"."""
    data = valid_data(library)
    data["library"]["location_prefix_map"] = [
        {"from": "/mnt/volume", "to": "{library.root}"},
        {"from": "/mnt/music", "to": "/Volumes/MUSIC", "volume_id": identity},
    ]
    problems = config.validate(data)

    assert [p for p in problems if "location_prefix_map[1].volume_id" in p], problems
    assert not [p for p in problems if "location_prefix_map[0]" in p], problems


def test_an_unset_rekordbox_pin_refuses_to_write_with_its_own_remedy(cfg):
    """S2. Unset refuses and is never auto recorded; the remedy is "record this one thing"."""
    assert cfg.rekordbox.pinned_app_version is None
    with pytest.raises(config.ConfigInvalid, match="pinned_app_version") as excinfo:
        cfg.assert_rekordbox_pin_recorded()
    assert excinfo.value.remedy is config.Remedy.RECORD_REKORDBOX_PIN


def test_a_recorded_pin_permits_the_write_and_carries_its_validation_date(library):
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
    """S3. U2 owns the values; the naming engine takes them as parameters."""
    assert cfg.naming.lossy_marker
    assert cfg.naming.path_budget_bytes == 250
    assert cfg.naming.filename_max_bytes == 255
    assert cfg.naming.path_budget_bytes < cfg.naming.filename_max_bytes


def test_there_is_no_configuration_in_which_lossy_goes_unmarked(library):
    """S3 and R21. Unrepresentable beats validated away."""
    assert config.from_dict(valid_data(library)).acquisition.lossless_policy == "strict"

    permitted = valid_data(library, acquisition={"lossless_policy": "allow_lossy_marked"})
    assert config.validate(permitted) == []

    for bad in ("allow_lossy", "off", "none", "unmarked"):
        problems = config.validate(valid_data(library, acquisition={"lossless_policy": bad}))
        assert any("lossless_policy" in p for p in problems), bad


def test_the_vendored_adapter_is_the_default_under_its_neutral_name(library):
    assert config.from_dict(valid_data(library)).acquisition.adapter == "vendored"


def test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one(library, tmp_path):
    """U197. A file written before the rename selects the same adapter, read as an install reads it."""
    path = tmp_path / "config.toml"
    written = valid_data(library, acquisition={"adapter": "tidal_dl_ng", "quality": "lossless"})
    path.write_bytes(tomli_w.dumps(written).encode("utf-8"))
    loaded = config.load_from_path(path)
    assert loaded.acquisition.adapter == "vendored"
    assert loaded.acquisition.quality == "lossless"
    assert config.validate(written) == []


def test_only_a_retired_adapter_key_is_folded(library):
    """A mapping of retired names, never a fallback: any other name passes as written."""
    assert dict(config.RETIRED_ADAPTER_NAMES) == {"tidal_dl_ng": "vendored"}
    for name in ("streamrip", "vendored", "not-a-real-adapter", "Tidal_DL_NG"):
        cfg = config.from_dict(valid_data(library, acquisition={"adapter": name}))
        assert cfg.acquisition.adapter == name


def test_config_carries_only_the_taxonomy_selection(cfg):
    """S6. The active template is library scoped state, not a config value."""
    field_names = {f for f in type(cfg.taxonomy).__dataclass_fields__}
    assert field_names == {"template"}
    assert config.state_file("taxonomy_active").root is config.StateRoot.LIBRARY


def test_analysis_worker_count_defaults_to_probing(cfg):
    """KTD10: absent means probe a memory budget, never a shipped guess."""
    assert cfg.analysis.jobs is None


def test_no_backup_destination_ships_with_a_default(cfg):
    assert cfg.backup.remote is None
    assert cfg.backup.dest is None
    assert cfg.backup.archive_root is None
    assert cfg.backup.db_dest_root is None


# Backup destinations name an rclone remote (R-345).


REMOTE_DESTINATIONS = {
    "dest": "gdrive:bucket/path",
    "archive_root": "gdrive:bucket/archive",
    "db_dest_root": "gdrive:bucket/db",
}


def test_a_backup_destination_naming_an_rclone_remote_is_accepted(library):
    """The remote is derived from the destinations rather than typed again."""
    data = valid_data(library, backup=dict(REMOTE_DESTINATIONS))
    assert config.validate(data) == []
    cfg = config.from_dict(data)
    assert cfg.backup.dest == "gdrive:bucket/path"
    assert cfg.backup.remote == "gdrive"


@pytest.mark.parametrize("key", ["dest", "archive_root", "db_dest_root"])
@pytest.mark.parametrize(
    "typed",
    [
        # A bare folder name, read as a path beside the worker's cwd.
        "MusicBackup",
        # An on the fly backend with no configured remote.
        ":local:/tmp/backups",
        # A Windows drive, which rclone treats as local either slash.
        "C:\\Backups",
        "C:/Backups",
        # Names rclone cannot hold: a leading hyphen, a trailing space.
        "-gdrive:bucket",
        "gdrive :bucket",
    ],
)
def test_a_backup_destination_naming_no_remote_is_refused(library, key, typed):
    """R-345: a bare folder copied the library beside the worker. The refusal names key and value."""
    backup = dict(REMOTE_DESTINATIONS)
    backup[key] = typed
    data = valid_data(library, backup=backup)
    problems = config.validate(data)
    assert len(problems) == 1, problems
    assert f"backup.{key}" in problems[0]
    assert repr(typed) in problems[0]
    assert "rclone remote" in problems[0]
    with pytest.raises(config.ConfigInvalid) as excinfo:
        config.from_dict(data)
    assert excinfo.value.problems == tuple(problems)


def test_the_backup_destination_check_reads_the_effective_mapping(library, monkeypatch):
    """P2: the check judges what rclone gets, driven at the override seam."""
    backup = dict(REMOTE_DESTINATIONS)
    backup["dest"] = "MusicBackup"
    data = valid_data(library, backup=backup)
    assert any("backup.dest" in p for p in config.validate(data))

    real = config._apply_env_overrides

    def relocating(mapping):
        effective = real(mapping)
        effective["backup"]["dest"] = "gdrive:" + effective["backup"]["dest"]
        return effective

    # The seam is named in both modules that pass through it (U299).
    monkeypatch.setattr(config, "_apply_env_overrides", relocating)
    monkeypatch.setattr(config_validate, "_apply_env_overrides", relocating)
    assert config.validate(data) == []
    assert config.from_dict(data).backup.dest == "gdrive:MusicBackup"


def test_the_backup_destinations_must_name_one_remote(library):
    backup = dict(REMOTE_DESTINATIONS)
    backup["db_dest_root"] = "other:bucket/db"
    problems = config.validate(valid_data(library, backup=backup))
    assert len(problems) == 1, problems
    assert "one rclone remote" in problems[0]
    assert "'gdrive'" in problems[0] and "'other'" in problems[0]


@pytest.mark.parametrize("spelled", ["gdrive", "gdrive:", "gdrive:bucket"])
def test_a_spelled_backup_remote_that_matches_the_destinations_is_kept(library, spelled):
    """The NAME must agree, and the file keeps its own spelling."""
    backup = dict(REMOTE_DESTINATIONS, remote=spelled)
    data = valid_data(library, backup=backup)
    assert config.validate(data) == []
    assert config.from_dict(data).backup.remote == spelled


def test_a_spelled_backup_remote_that_names_another_remote_is_refused(library):
    """Otherwise doctor checks a remote nothing writes to."""
    backup = dict(REMOTE_DESTINATIONS, remote="elsewhere")
    problems = config.validate(valid_data(library, backup=backup))
    assert len(problems) == 1, problems
    assert "backup.remote" in problems[0]
    assert "'elsewhere'" in problems[0] and "'gdrive'" in problems[0]


@pytest.mark.parametrize("profile", ["slim", "full"])
def test_an_unset_backup_destination_stays_allowed(library, profile):
    """P7: refusing absence at load would lock every fresh full install out of its config."""
    data = valid_data(library, profile={"name": profile})
    assert config.validate(data) == []
    cfg = config.from_dict(data)
    assert cfg.backup.remote is None
    assert cfg.backup.dest is None
    partial = valid_data(library, profile={"name": profile}, backup={"dest": "gdrive:m"})
    assert config.validate(partial) == []
    assert config.from_dict(partial).backup.remote == "gdrive"


@pytest.mark.parametrize(
    "name",
    ["me@gdrive", "work+home", "my drive", "gdrive-2.old", "Sicherung_ü", "b2"],
)
def test_every_name_rclone_can_store_is_accepted_as_a_remote(library, name):
    """rclone 1.61's rule; anything stricter fires on a correct setup (P7)."""
    backup = {key.split(".")[1]: f"{name}:library/{key}" for key in config.BACKUP_DESTINATION_KEYS}
    data = valid_data(library, backup=backup)
    assert config.validate(data) == []
    assert config.from_dict(data).backup.remote == name


def test_the_destination_keys_are_published_for_the_wizard_and_the_verb():
    assert config.BACKUP_DESTINATION_KEYS == (
        "backup.dest",
        "backup.archive_root",
        "backup.db_dest_root",
    )
    assert config.backup_remote_name("gdrive:bucket/path") == "gdrive"
    assert config.backup_remote_name("MusicBackup") is None
    assert config.backup_remote_name(None) is None
    assert config.derived_backup_remote({"backup": {"dest": "gdrive:m"}}) == "gdrive"
    assert config.derived_backup_remote({"backup": {"remote": "x", "dest": "gdrive:m"}}) is None


# The fingerprint (KTD9).


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
    """Otherwise every reordering hand edit reports as drift."""
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
        ("reports", "intake_stale_days", 45),
        ("outbound", "export_stale_days", 14),
        ("recognition", "host", "identify-eu-west-1.acrcloud.com"),
        ("recognition", "monthly_calls", 250),
    ],
)
def test_the_fingerprint_changes_when_any_value_changes(library, section, key, value):
    """One case per section, so a section left out of serialization is caught.

    Merged into the section rather than replacing it, which would drop required keys.
    """
    base_data = valid_data(library)
    changed_data = valid_data(library)
    changed_data.setdefault(section, {})[key] = value

    base = config.from_dict(base_data)
    changed = config.from_dict(changed_data)
    assert changed.fingerprint() != base.fingerprint()


def test_a_default_valued_section_and_an_absent_one_fingerprint_alike(library):
    absent = config.from_dict(valid_data(library))
    explicit = config.from_dict(valid_data(library, naming={"lossy_marker": "[MP3]"}))
    assert explicit.fingerprint() == absent.fingerprint()


# Lazy resolution: no import time side effects, no module level snapshots.


def test_importing_the_config_module_creates_nothing(tmp_path):
    """Proved in a real interpreter, which an import time mkdir cannot hide from."""
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
    """With nothing to snapshot, snapshotting cannot happen."""
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

#: Functions that resolve a location; calling one at import freezes the answer.
_CONFIG_RESOLVERS = frozenset(
    {
        "load",
        "config_dir",
        "config_path",
        "installation_state_dir",
        "library_state_dir",
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


def _eager_walk(root: ast.AST):
    """``ast.walk`` that never enters a function or lambda body, which runs at call time."""
    todo = deque([root])
    while todo:
        node = todo.popleft()
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda):
            todo.extend(ast.iter_child_nodes(node))
        yield node


def module_level_config_snapshots(source: str, module: str) -> list[str]:
    """One message per binding evaluated at import (class bodies too) that reads config."""
    problems: list[str] = []
    for node in _eager_walk(parsed(source)):
        if not isinstance(node, ast.Assign | ast.AnnAssign) or node.value is None:
            continue
        for sub in _eager_walk(node.value):
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


@pytest.mark.parametrize(
    "source",
    [
        "from cratekit.core import config\nLIBRARY = config.load().library.root\n",
        "from cratekit.core.config import installation_state_dir\nSTATE = installation_state_dir()\n",
        "from cratekit.core import config\n\nclass Sweep:\n    root = config.load().library.root\n",
    ],
    ids=["attribute-binding", "resolver-call", "class-attribute"],
)
def test_the_snapshot_lint_catches_a_binding_evaluated_at_import(source):
    assert module_level_config_snapshots(source, "cratekit.label.sweep")


def test_the_snapshot_lint_allows_reading_config_inside_a_function():
    source = (
        "from cratekit.core import config\n\n"
        "def sweep():\n"
        "    return config.load().library.root\n"
    )
    assert module_level_config_snapshots(source, "cratekit.label.sweep") == []


def test_no_module_composes_its_own_path_under_a_state_root():
    """Every path under a state root comes from ``state_path``, so it is declared.

    Only a source naming an accessor can hold a hit (identifiers compared after
    the NFKC folding the parser applies), so the rest are not parsed.
    """
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path.relative_to(SRC_ROOT).as_posix() in INVENTORY_MODULES:
            continue
        source = path.read_text()
        folded = unicodedata.normalize("NFKC", source)
        if not any(name in folded for name in _STATE_ROOT_ACCESSORS):
            continue
        for hit in _paths_composed_from_a_state_root(source):
            offenders.append(f"{path.relative_to(SRC_ROOT)}: {hit}")
    assert not offenders, (
        "paths composed under a state root outside the inventory:\n"
        + "\n".join(offenders)
        + "\nDeclare the entry in config.STATE_FILES and resolve it with state_path()."
    )


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


# Environment overrides relocate; they never supply.


def test_an_override_never_supplies_a_value_the_file_omitted(library, monkeypatch):
    """A supplied root lets an unset machine write to whatever the environment names (R38)."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    data = valid_data(library)
    del data["library"]["root"]
    assert any("library.root" in p for p in config.validate(data))


def test_a_containment_violation_created_by_the_override_is_not_validated_clean(
    library, tmp_path, monkeypatch
):
    """Containment is decided against the effective root, set through the real variable."""
    relocated = tmp_path / "relocated"
    relocated.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(relocated))

    data = valid_data(library)  # names the stale root, database under it
    cfg = config.from_dict(data)

    assert (config.validate(data) == []) is cfg.db_is_inside_library_root()


def test_a_relocated_root_carries_the_database_that_sat_under_it(
    library, tmp_path, monkeypatch
):
    """The database is recorded relative to the library, and the redirect keeps tests off the real one."""
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
    """Dragging it along would move a path the user chose and retire its acknowledgment."""
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
    """Before the fix, save under a relocation wrote a file the next load refused."""
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
    """The general guarantee. Built through the dataclass, the only way to an invalid Config."""
    from dataclasses import replace  # noqa: PLC0415

    broken = replace(
        cfg,
        library=replace(cfg.library, db_path=tmp_path / "elsewhere" / "master.db"),
    )
    with pytest.raises(config.ConfigInvalid, match="is not under library.root"):
        config.save(broken, tmp_path / "config.toml")
    assert not (tmp_path / "config.toml").exists()


def test_the_config_directory_resolves_through_the_platform_library(monkeypatch, tmp_path):
    """KTD6 and R1: no hardcoded per platform path."""
    monkeypatch.delenv(config.ENV_CONFIG_DIR, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    resolved = config.config_dir()
    assert resolved.name == "cratekit"
    assert tmp_path in resolved.parents


# Loading, saving, memoization.


def test_a_missing_config_says_so_and_carries_the_setup_remedy(tmp_path):
    """Defaults for a config never written would silently invent a library."""
    with pytest.raises(config.ConfigMissing) as excinfo:
        config.load(tmp_path / "nothing.toml")
    assert excinfo.value.remedy is config.Remedy.RUN_SETUP


def test_unparseable_toml_names_the_file(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("this is not = = toml\n")
    with pytest.raises(config.ConfigCorrupt, match=re.escape(path.name)):
        config.load(path)


def test_a_rewritten_config_is_not_served_from_the_memo(cfg, library, tmp_path):
    """The memo is keyed on file identity, so callers can ``load()`` where they need a value."""
    path = tmp_path / "config.toml"
    config.save(cfg, path)
    assert config.load(path).taxonomy.template == "default"

    # Replaced the way an external writer would, without save() clearing the memo.
    changed = config.from_dict(valid_data(library, taxonomy={"template": "second"}))
    staging = tmp_path / "staged.toml"
    staging.write_bytes(changed.to_toml_bytes())
    os.replace(staging, path)

    assert config.load(path).taxonomy.template == "second"


def test_the_default_location_round_trips_end_to_end(cfg):
    """Save with no path, load with no path: the path a user actually exercises."""
    written = config.save(cfg)
    assert written == config.config_path()
    assert config.load().fingerprint() == cfg.fingerprint()


def test_saving_creates_the_directory_only_when_it_writes(cfg, tmp_path):
    target = tmp_path / "deep" / "nested" / "config.toml"
    assert not target.parent.exists()
    config.save(cfg, target)
    assert target.is_file()


def test_a_failed_write_leaves_no_temporary_file_behind(cfg, tmp_path, monkeypatch):
    """If the replace never happens, the temp file beside the target must not survive."""
    target = tmp_path / "config.toml"
    config.save(cfg, target)
    before = sorted(p.name for p in tmp_path.iterdir())

    def boom(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError, match="disk full"):
        config.save(cfg, target)

    assert sorted(p.name for p in tmp_path.iterdir()) == before


# Credentials (R4).


def test_a_read_with_no_keychain_backend_raises_and_names_the_opt_in(monkeypatch):
    """Never None, which reads a 401 as an outage; it names the opt in, never takes it."""

    def no_backend(*args, **kwargs):
        raise keyring.errors.NoKeyringError("no backend")

    monkeypatch.setattr(keyring, "get_password", no_backend)

    with pytest.raises(secrets.CredentialBackendUnavailable) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert excinfo.value.remedy is secrets.Remedy.INSTALL_KEYCHAIN_BACKEND
    assert secrets.ENV_ALLOW_ENV_CREDENTIALS in str(excinfo.value)


def test_an_absent_credential_is_a_different_failure_from_a_broken_backend():
    with pytest.raises(secrets.CredentialMissing) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert excinfo.value.remedy is secrets.Remedy.SET_CREDENTIAL


def test_the_three_credential_failures_carry_three_different_remedies():
    """KTD25: collapsing them forces callers to parse messages."""
    remedies = {
        secrets.CredentialBackendUnavailable.remedy,
        secrets.CredentialMissing.remedy,
        secrets.CredentialRejected.remedy,
    }
    assert len(remedies) == 3


@pytest.mark.parametrize(
    "vocabulary", [secrets.Remedy, config.Remedy], ids=["secrets-remedy", "config-remedy"]
)
def test_a_remedy_is_a_token_and_not_the_command_a_user_types(vocabulary):
    """D2: the CLI renders a token into a command; this layer knows no interface."""
    for remedy in vocabulary:
        assert " " not in remedy.value
        assert "crate " not in remedy.value


def test_recording_and_reading_a_credential_round_trips():
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"


def test_a_multi_field_credential_is_stored_as_one_blob():
    """Separate entries can be half refreshed; one blob cannot."""
    payload = {"token": "NOT-A-REAL-1", "refresh": "NOT-A-REAL-2", "kind": "pkce"}
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, payload)
    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == payload


def test_an_empty_credential_is_refused_rather_than_stored():
    with pytest.raises(secrets.CredentialMissing):
        secrets.set(secrets.Credential.IDENTIFY_KEY, "")


def test_presence_is_answered_without_retrieving_the_value(monkeypatch):
    """Doctor asks on every run; a retrieval on macOS raises a prompt that hangs it."""
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
    secrets.set(secrets.Credential.IDENTIFY_SIGNING_KEY, "value-from-the-user")
    payload = json.loads(config.state_path("credential_index").read_text())
    assert payload["recorded"] == [secrets.Credential.IDENTIFY_SIGNING_KEY.value]
    assert "value-from-the-user" not in json.dumps(payload)


# Item 4 of the five places residual: the index reader tells missing from
# unreadable from damaged. The doctor half is in ``tests/test_doctor.py``.


def _unreadable_index(monkeypatch, path: Path):
    """One file answers EACCES (chmod is vacuous under root); returns a disarm.

    Disarm rather than ``monkeypatch.undo``, which also undoes the autouse isolation.
    """
    real = Path.read_text
    armed = True

    def refuse(self, *args, **kwargs):
        if armed and self == path:
            raise PermissionError(13, "Permission denied", str(path))
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refuse)

    def disarm() -> None:
        nonlocal armed
        armed = False

    return disarm


def test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded(
    monkeypatch,
):
    """Answering False sent doctor and three verbs to "record it", a loop that never ends (R-116)."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    index = config.state_path("credential_index")
    _unreadable_index(monkeypatch, index)

    with pytest.raises(CratekitError) as excinfo:
        secrets.exists(secrets.Credential.IDENTIFY_KEY)

    cause = excinfo.value.cause
    assert str(index) in cause.message, "the refusal must name the file it could not read"
    # The remedy follows the kind of refusal the OS made: a permission is granted.
    assert cause.remediation.remedy is not Remedy.SET_CREDENTIAL
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.reason == "path-permission-denied"
    assert cause.code is not ExitCode.OK


def test_an_absent_presence_index_still_answers_nothing_recorded():
    """A fresh install has no index; refusing here would block setup."""
    index = config.state_path("credential_index")
    assert not index.exists()
    assert secrets.exists(secrets.Credential.IDENTIFY_KEY) is False
    assert secrets.recorded() == frozenset()


def test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act():
    """EISDIR, which no classification claims, shows the site's own declared act."""
    index = config.state_path("credential_index")
    index.parent.mkdir(parents=True, exist_ok=True)
    index.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        secrets.exists(secrets.Credential.IDENTIFY_KEY)

    cause = excinfo.value.cause
    assert cause.reason == "credential-index-unreadable"
    assert cause.remediation.remedy is Remedy.REPAIR_CREDENTIAL_STORE
    assert cause.detail["index"] == "unreadable"
    assert str(index) in cause.message
    # A precondition the person can repair, never a defect to report.
    assert cause.code is ExitCode.PRECONDITION


def test_a_damaged_presence_index_refuses_and_says_it_was_read(monkeypatch):
    """Bytes read that do not say what is recorded are a different repair from a refusal."""
    index = config.state_path("credential_index")
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text("{not json at all")

    with pytest.raises(CratekitError) as excinfo:
        secrets.exists(secrets.Credential.PROVIDER_SESSION)

    cause = excinfo.value.cause
    assert cause.reason == "credential-index-unreadable"
    assert cause.remediation.remedy is Remedy.REPAIR_CREDENTIAL_STORE
    assert cause.detail["index"] == "damaged"
    assert cause.code is ExitCode.PRECONDITION
    assert str(index) in cause.message


def test_a_presence_index_without_a_list_of_names_refuses_rather_than_answering():
    index = config.state_path("credential_index")
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(json.dumps({"recorded": "identify-key"}))

    with pytest.raises(CratekitError) as excinfo:
        secrets.recorded()
    assert excinfo.value.cause.reason == "credential-index-unreadable"


def test_recording_a_credential_does_not_truncate_an_index_it_could_not_read(
    monkeypatch,
):
    """An empty answer from a failed read made ``_record_name`` rewrite the index to one name."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    index = config.state_path("credential_index")
    before = index.read_text()
    disarm = _unreadable_index(monkeypatch, index)

    with pytest.raises(CratekitError):
        secrets.set(secrets.Credential.IDENTIFY_SIGNING_KEY, "another-value")

    disarm()
    assert index.read_text() == before, "the index was rewritten from a read that failed"
    assert secrets.recorded() == frozenset({secrets.Credential.IDENTIFY_KEY.value})


def test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain(
    monkeypatch,
):
    """``_record_name`` runs after the keychain write landed, so the refusal must say so."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    index = config.state_path("credential_index")
    disarm = _unreadable_index(monkeypatch, index)

    with pytest.raises(CratekitError) as excinfo:
        secrets.set(secrets.Credential.IDENTIFY_SIGNING_KEY, "another-value")
    message = excinfo.value.cause.message

    disarm()
    # Driven: the keychain is asked what it holds.
    assert secrets.get(secrets.Credential.IDENTIFY_SIGNING_KEY) == "another-value"
    assert "THE VALUE IS IN THE KEYCHAIN" in message
    assert "Nothing was stored" not in message


def test_a_refusal_from_the_remove_half_says_neither_store_was_touched(monkeypatch):
    """``delete`` reads the index first, so a refusal there touched neither store."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    index = config.state_path("credential_index")
    disarm = _unreadable_index(monkeypatch, index)

    with pytest.raises(CratekitError) as excinfo:
        secrets.delete(secrets.Credential.IDENTIFY_KEY)
    message = excinfo.value.cause.message

    disarm()
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"
    assert "Nothing was removed" in message
    assert "THE VALUE IS IN THE KEYCHAIN" not in message


def test_removing_a_credential_does_not_truncate_an_index_it_could_not_read(
    monkeypatch,
):
    """``delete`` clears the index before the keychain, so the refusal must come first."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    secrets.set(secrets.Credential.IDENTIFY_SIGNING_KEY, "another-value")
    index = config.state_path("credential_index")
    before = index.read_text()
    disarm = _unreadable_index(monkeypatch, index)

    with pytest.raises(CratekitError):
        secrets.delete(secrets.Credential.IDENTIFY_KEY)

    disarm()
    assert index.read_text() == before
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"


def test_the_environment_fallback_answers_presence_without_reading_the_index(
    monkeypatch,
):
    """The opted in fallback is checked first; it has no index by design."""
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_IDENTIFY_KEY", "value-from-the-env")
    index = config.state_path("credential_index")
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text("{not json at all")

    assert secrets.exists(secrets.Credential.IDENTIFY_KEY) is True


def test_the_environment_fallback_is_opt_in_and_never_silent(monkeypatch):
    """An override the user did not ask for is an unauthenticated request in disguise."""
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_IDENTIFY_KEY", "value-from-the-env")
    monkeypatch.delenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, raising=False)

    with pytest.raises(secrets.CredentialMissing) as excinfo:
        secrets.get(secrets.Credential.IDENTIFY_KEY)
    assert "value-from-the-env" not in str(excinfo.value)

    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-env"


def test_the_presence_index_cycle_is_held_under_an_exclusive_lock():
    """Unlocked, two processes lost a name in 23 of 25 trials; a fresh descriptor contends."""
    import fcntl

    lock_path = config.state_path("credential_index_lock")
    # Created so a build that never locks fails on contention, not a missing file.
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.touch()
    contended: list[bool] = []
    real_write = secrets._index_write

    def _contend(names):
        with open(lock_path, "a+") as contender:
            try:
                fcntl.flock(contender, fcntl.LOCK_EX | fcntl.LOCK_NB)
                contended.append(False)
                fcntl.flock(contender, fcntl.LOCK_UN)
            except BlockingIOError:
                contended.append(True)
        return real_write(names)

    secrets._index_write = _contend
    try:
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
        secrets.delete(secrets.Credential.IDENTIFY_KEY)
    finally:
        secrets._index_write = real_write

    assert contended == [True, True], "the read then write cycle ran unlocked"
    # And the lock is released afterwards.
    with open(lock_path, "a+") as after:
        fcntl.flock(after, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(after, fcntl.LOCK_UN)


def test_the_presence_index_lock_lives_beside_the_file_it_guards(cfg):
    entry = config.state_file("credential_index_lock")
    assert entry.root is config.state_file("credential_index").root
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert config.state_path("credential_index_lock").parent == (
        config.state_path("credential_index").parent
    )


def test_a_credential_index_that_cannot_be_locked_refuses_rather_than_writing(
    monkeypatch,
):
    """Proceeding unlocked IS the defect, so it is not the degradation."""
    real_open = os.open

    def refuse(path, *args, **kwargs):
        if str(path).endswith("credential_index.lock"):
            raise PermissionError("no")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(os, "open", refuse)
    with pytest.raises(secrets.CredentialIndexUnusable) as excinfo:
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    assert excinfo.value.remedy is secrets.Remedy.REPAIR_CREDENTIAL_STORE
    assert not config.state_path("credential_index").exists()


def test_a_backend_message_never_reaches_the_refusal_a_user_reads(monkeypatch):
    """Third party exception text may carry the secret; only its type is named."""

    def leaky(_service, _name, password):
        raise RuntimeError(f"could not store {password}")

    monkeypatch.setattr(keyring, "set_password", leaky)
    with pytest.raises(secrets.CredentialBackendUnavailable) as excinfo:
        secrets.set(secrets.Credential.IDENTIFY_KEY, "NOT-A-REAL-SECRET")

    assert "NOT-A-REAL-SECRET" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_the_keychain_service_is_not_namespaced_per_library():
    """A credential is an account fact, not a library fact (KTD21)."""
    assert secrets.SERVICE == "cratekit"


# Permissions do not depend on the user's umask.


@pytest.fixture
def permissive_umask():
    """Run the body under umask 000, where a mode left to the umask shows."""
    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


def _drive_every_write_path(cfg) -> list[Path]:
    """Exercise every way this unit writes, as operations; returns the roots to audit."""
    # A credential: the installation state directory and the presence index.
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    # The config file: the installation config directory.
    config.save(cfg)
    # A library write two levels deep, so an intermediate directory shows.
    config.atomic_write_bytes(b"{}\n", config.state_path("tree_registry", cfg))
    # A migration: its lock file and a versioned backup beside the config.
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
    """Walked, not enumerated, directories included; the migration lock is named as well."""
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
    # A green walk over nothing would only mean the write paths stopped writing.
    assert seen_files >= 4 and seen_dirs >= 4, (
        f"the audit only saw {seen_files} files and {seen_dirs} directories, "
        f"which is too few for the write paths it drove"
    )

    locks = sorted(config.config_dir().rglob("*.migrate.lock"))
    assert locks, "the migration never took a lock, so this asserts nothing"
    for lock in locks:
        assert stat.S_IMODE(lock.stat().st_mode) == config.PRIVATE_FILE_MODE


def _bare_mkdir_calls(source: str) -> list[str]:
    """Every ``.mkdir(...)`` outside ``mkdir_private``; ``parents=True`` makes 0o777 levels."""
    tree = parsed(source)
    inside_helper: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "mkdir_private":
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
    """One creator decides the mode, and keeps ``save``'s docstring from claiming to be it."""
    source = (SRC_ROOT / "cratekit" / "core" / "config.py").read_text()
    offenders = _bare_mkdir_calls(source)
    assert not offenders, (
        "directories created outside mkdir_private:\n"
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
    """A migration must not leave a laxer duplicate of the config."""
    path = tmp_path / "config.toml"
    data = valid_data(library)
    data["schema_version"] = 1
    path.write_text(tomli_w.dumps(data))

    config.load_from_path(path, current=2, migrations={1: lambda d: d})

    backup = tmp_path / "config.toml.v1.bak"
    assert stat.S_IMODE(backup.stat().st_mode) == 0o600


# The keychain is an external system, so its failures are not a closed set.


def test_a_backend_that_fails_with_an_unexpected_type_still_refuses_typed(monkeypatch):
    """SecretService on a headless machine raises outside KeyringError."""

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
    """A backend's ``priority`` raises where it is not viable, the machine doctor diagnoses."""

    class _NotViableHere:
        @property
        def priority(self):
            raise RuntimeError("this backend is not viable here")

    monkeypatch.setattr(keyring, "get_keyring", lambda: _NotViableHere())
    assert secrets.backend_available() is False


def test_a_backend_that_accepts_a_write_and_stores_nothing_refuses(monkeypatch):
    """The null backend's no-op write needs a read back, or the user loops forever."""
    backend = keyring.backends.null.Keyring()
    monkeypatch.setattr(keyring, "set_password", backend.set_password)
    monkeypatch.setattr(keyring, "get_password", backend.get_password)

    with pytest.raises(secrets.CredentialBackendUnavailable):
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)
    assert secrets.Credential.IDENTIFY_KEY not in secrets.recorded()


# D2: a foundation module carries a remedy token, never a command line.


def test_every_config_failure_carries_a_structured_remedy():
    """KTD25, in the module that raises the most types."""
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


# Values the file supplies, and the ones it must be type checked on.


def test_the_library_root_is_read_from_the_file_when_nothing_relocates_it(
    library, monkeypatch
):
    """The autouse isolation always relocates, so the file's own value is tested only here."""
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT, raising=False)
    assert config.from_dict(valid_data(library)).library.root == library


@pytest.mark.parametrize("key", ["path_budget_bytes", "filename_max_bytes"])
def test_a_naming_budget_that_is_not_an_integer_is_named_at_load(library, key):
    """Else a string budget surfaces as a TypeError deep inside a rename."""
    problems = config.validate(valid_data(library, naming={key: "250"}))
    assert any(key in p for p in problems), problems


def test_the_overlap_contract_names_are_pinned_while_the_old_system_reads_them():
    """U30: DJ_tools spells these paths itself, so a rename would silently disarm its guard."""
    default = config.LibraryConfig.__dataclass_fields__["state_dirname"].default
    assert default == ".cratekit"
    assert config._LIBRARY_SUBDIR_BY_ROLE[config.SnapshotRole.NEVER_RESTORED] == "local"
    assert config._LIBRARY_SUBDIR_BY_ROLE[config.SnapshotRole.COUPLED] == "coupled"


# R-227: the age past which an outbound verb calls its export old.


def test_the_export_staleness_default_is_seven_days_and_a_file_can_move_it(library):
    assert config.from_dict(valid_data(library)).outbound.export_stale_days == 7
    moved = config.from_dict(valid_data(library, outbound={"export_stale_days": 21}))
    assert moved.outbound.export_stale_days == 21


@pytest.mark.parametrize("value", [0, -3, "seven", 2.5, True])
def test_an_export_staleness_that_is_not_a_positive_day_count_is_refused(library, value):
    """``True`` by name: an ``int`` to ``isinstance`` that would read as one day."""
    problems = config.validate(valid_data(library, outbound={"export_stale_days": value}))
    assert [p for p in problems if "outbound.export_stale_days" in p], problems
    assert all("positive whole number" in p for p in problems), problems


def test_an_export_staleness_nobody_could_mean_is_refused_with_its_ceiling(library):
    """Ten billion days overflowed the duration and crashed all three verbs at the gate."""
    ceiling = config.MAX_EXPORT_STALE_DAYS
    assert config.validate(valid_data(library, outbound={"export_stale_days": ceiling})) == []
    problems = config.validate(
        valid_data(library, outbound={"export_stale_days": 10_000_000_000})
    )
    assert len(problems) == 1 and "outbound.export_stale_days" in problems[0]
    assert str(ceiling) in problems[0]


# R-301: the recognition host and the monthly bound are the user's.


def test_the_recognition_defaults_bound_the_month_and_name_one_region(library):
    section = config.from_dict(valid_data(library)).recognition
    assert section.host == config.DEFAULT_RECOGNITION_HOST
    assert section.monthly_calls == config.DEFAULT_RECOGNITION_MONTHLY_CALLS
    assert section.monthly_calls > 0, "an unconfigured machine must still bound the month"
    moved = config.from_dict(
        valid_data(
            library,
            recognition={"host": "identify-ap-southeast-1.acrcloud.com", "monthly_calls": 5},
        )
    ).recognition
    assert moved == config.RecognitionConfig(
        host="identify-ap-southeast-1.acrcloud.com", monthly_calls=5
    )


def test_the_recognition_section_round_trips_through_the_file(library):
    built = config.from_dict(
        valid_data(library, recognition={"host": "identify-eu-west-1.acrcloud.com"})
    )
    again = config.from_dict(tomllib.loads(built.to_toml_bytes().decode()))
    assert again.recognition == built.recognition
    assert again.fingerprint() == built.fingerprint()


@pytest.mark.parametrize("value", [0, -3, "many", 2.5, True])
def test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused(library, value):
    """``True`` is an ``int`` to ``isinstance``; zero, since nothing switches the bound off."""
    problems = config.validate(valid_data(library, recognition={"monthly_calls": value}))
    assert len(problems) == 1, problems
    assert "recognition.monthly_calls" in problems[0]


@pytest.mark.parametrize(
    "value",
    [
        "https://identify-eu-west-1.acrcloud.com",
        "identify-eu-west-1.acrcloud.com/v1/identify",
        "identify-eu-west-1.acrcloud.com:443",
        "identify eu.acrcloud.com",
        "Identify-EU-west-1.acrcloud.com",
        "identify-eu-west-1.acrcloud.com.attacker.example",
        "acrcloud.com.example",
        "evilacrcloud.com",
        "acrcloud.com",
        "",
        "-bad.acrcloud.com",
        7,
    ],
)
def test_a_host_that_is_not_a_bare_name_under_the_service_is_refused(library, value):
    """The access key and its signature travel to this host."""
    problems = config.validate(valid_data(library, recognition={"host": value}))
    assert len(problems) == 1, problems
    assert "recognition.host" in problems[0]


@pytest.mark.parametrize(
    "overrides",
    [
        {},
        {"outbound": {}},
        {"recognition": {}},
        {"recognition": {"host": "identify-eu-west-1.acrcloud.com"}},
    ],
    ids=["no-sections", "empty-outbound", "empty-recognition", "recognition-host-only"],
)
def test_an_absent_optional_section_or_key_is_not_a_problem(library, overrides):
    assert config.validate(valid_data(library, **overrides)) == []
