"""U2: forward-only config migrations, and the property that makes them safe.

Steps run in memory over a deep copy, validated before a byte is written, so a migration that
raises leaves the original byte-identical. The shipped ladder is empty (schema version 1), so the
engine takes its ladder as a parameter, driven here by a synthetic three-version ladder."""

from __future__ import annotations

import tomllib

import pytest
import tomli_w

from cratekit.core import config
from tests.test_config import valid_data
from tests.test_config_update import library as library  # noqa: PLC0414


def _ladder(record: list[str], *, fails_at: int | None = None):
    """A 1 -> 2 -> 3 ladder recording its steps; ``fails_at`` raises after mutating the copy."""

    def step(from_version: int):
        def run(data: dict) -> dict:
            record.append(f"v{from_version}->v{from_version + 1}")
            out = dict(data)
            out[f"added_in_v{from_version + 1}"] = True
            if fails_at == from_version:
                raise RuntimeError(f"migration {from_version} failed")
            return out

        return run

    return {1: step(1), 2: step(2)}


def _write(path, data: dict) -> None:
    """Raw TOML, bypassing the typed schema: a migration test writes old shapes."""
    path.write_text(tomli_w.dumps(data))


def _versioned(library, version: int) -> dict:
    data = valid_data(library)
    data["schema_version"] = version
    return data


def _v1_file(library, tmp_path):
    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))
    return path


def _listing(directory) -> list[str]:
    return sorted(p.name for p in directory.iterdir())


def _state(path) -> tuple[bytes, list[str]]:
    """The file's bytes and its directory's listing, which an aborted migration leaves alone."""
    return path.read_bytes(), _listing(path.parent)


@pytest.mark.parametrize(
    "version, steps, added",
    [
        (2, ["v2->v3"], [3]),
        # Order is the assertion: out of order still lands on the right number.
        (1, ["v1->v2", "v2->v3"], [2, 3]),
        (3, [], []),
    ],
    ids=["one-version-old", "two-versions-old-in-order", "already-current-runs-none"],
)
def test_a_config_migrates_forward_through_each_step_it_lacks(library, version, steps, added):
    record: list[str] = []
    migrated = config.migrate(_versioned(library, version), current=3, migrations=_ladder(record))
    assert record == steps
    if added:
        assert migrated["schema_version"] == 3
    for one in added:
        assert migrated[f"added_in_v{one}"] is True


def test_migration_never_mutates_the_input(library):
    """Steps run over a deep copy, so a caller's dict is never edited underneath it."""
    original = _versioned(library, 1)
    before = repr(original)
    config.migrate(original, current=3, migrations=_ladder([]))
    assert repr(original) == before


def test_a_migration_that_raises_partway_leaves_the_original_untouched(library, tmp_path):
    """Bytes prove the target was not rewritten; the listing, that nothing was orphaned."""
    path = _v1_file(library, tmp_path)
    before = _state(path)
    record: list[str] = []
    with pytest.raises(RuntimeError, match="migration 2 failed"):
        config.load_from_path(path, current=3, migrations=_ladder(record, fails_at=2))
    assert record == ["v1->v2", "v2->v3"], "the failing step must actually have run"
    assert _state(path) == before


def test_a_migration_whose_result_fails_validation_writes_nothing(library, tmp_path):
    """Validation precedes the first byte, or a buggy step's output is permanent."""
    path = _v1_file(library, tmp_path)
    before = _state(path)

    def destroys_a_required_key(data: dict) -> dict:
        out = dict(data)
        out["library"] = {k: v for k, v in out["library"].items() if k != "volume_id"}
        return out

    with pytest.raises(config.ConfigInvalid, match="library.volume_id"):
        config.load_from_path(path, current=2, migrations={1: destroys_a_required_key})
    assert _state(path) == before


def test_a_successful_migration_rewrites_the_file_and_keeps_a_backup(library, tmp_path):
    """The backup is named for the version it came FROM."""
    path = _v1_file(library, tmp_path)
    cfg = config.load_from_path(path, current=3, migrations=_ladder([]))
    assert cfg.schema_version == 3
    assert tomllib.loads(path.read_text())["schema_version"] == 3
    assert (tmp_path / "config.toml.v1.bak").is_file()


def test_a_gap_in_the_ladder_is_refused_before_anything_is_written(library, tmp_path):
    """A missing step is a refusal, never a silent skip to the next version."""
    path = _v1_file(library, tmp_path)
    before = path.read_bytes()
    with pytest.raises(config.ConfigCorrupt, match="gap"):
        config.load_from_path(path, current=3, migrations={2: lambda d: d})
    assert path.read_bytes() == before


def test_a_newer_config_refuses_rather_than_downgrading(library):
    """Forward only: this build would drop a newer build's keys on its next save."""
    with pytest.raises(config.ConfigTooNew) as excinfo:
        config.migrate(_versioned(library, 9), current=3, migrations=_ladder([]))
    assert "9" in str(excinfo.value) and "3" in str(excinfo.value)


@pytest.mark.parametrize(
    "version,match",
    # Written since the first release, so its absence means a hand edit, not age.
    [(None, "schema_version"), ("one", None)],
    ids=["absent-is-corruption-not-age", "non-integer-is-corruption"],
)
def test_an_unreadable_schema_version_is_corruption(library, version, match):
    data = valid_data(library)
    if version is None:
        del data["schema_version"]
    else:
        data["schema_version"] = version
    with pytest.raises(config.ConfigCorrupt, match=match):
        config.migrate(data)


def test_the_shipped_ladder_has_no_gaps():
    """Bumping CURRENT_SCHEMA_VERSION without a step turns the build red."""
    expected = set(range(1, config.CURRENT_SCHEMA_VERSION))
    assert set(config.MIGRATIONS) == expected, (
        f"the migration ladder must cover every version below {config.CURRENT_SCHEMA_VERSION}; "
        f"missing {sorted(expected - set(config.MIGRATIONS))}"
    )


def test_a_current_config_loads_without_a_backup_being_written(library, tmp_path):
    """No migration means no rewrite, so an ordinary load leaves the file alone."""
    path = tmp_path / "config.toml"
    _write(path, valid_data(library))
    before = _listing(tmp_path)
    config.load_from_path(path)
    assert _listing(tmp_path) == before


def test_a_migration_that_cannot_take_the_lock_refuses(library, tmp_path, monkeypatch):
    """A failed lock is refused here, since a subprocess could half-upgrade the config."""
    # Imported here so the file still collects on a platform without fcntl.
    import fcntl  # noqa: PLC0415
    path = _v1_file(library, tmp_path)
    before, before_listing = _state(path)

    def cannot_lock(*args, **kwargs):
        raise OSError("locking is not supported on this filesystem")

    monkeypatch.setattr(fcntl, "flock", cannot_lock)
    with pytest.raises(config.ConfigLockUnavailable):
        config.load_from_path(path, current=3, migrations=_ladder([]))
    assert path.read_bytes() == before
    assert _listing(tmp_path) == sorted([*before_listing, "config.toml.migrate.lock"])


def test_a_second_process_that_migrated_first_does_not_get_its_backup_clobbered(
    library, tmp_path, monkeypatch
):
    """B never re-reads, so A's ``.v1.bak`` would be clobbered; A migrates as B takes the lock."""
    path = _v1_file(library, tmp_path)
    v1_bytes = path.read_bytes()
    backup = tmp_path / "config.toml.v1.bak"
    original_enter = config.exclusive_lock.__enter__

    def another_process_finished_while_we_waited(self):
        acquired = original_enter(self)
        backup.write_bytes(v1_bytes)
        _write(path, _versioned(library, 3))
        return acquired

    finished = another_process_finished_while_we_waited
    monkeypatch.setattr(config.exclusive_lock, "__enter__", finished)
    cfg = config.load_from_path(path, current=3, migrations=_ladder([]))
    assert cfg.schema_version == 3
    assert tomllib.loads(backup.read_text())["schema_version"] == 1, (
        "the version backup was overwritten with already-migrated bytes"
    )
    assert tomllib.loads(path.read_text())["schema_version"] == 3
