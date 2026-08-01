"""U2: forward-only config migrations, and the property that makes them safe.

THE PROPERTY. A migration that raises partway leaves the original file
byte-identical and leaves nothing new on disk. Not because a cleanup path tidied
up, but because there was never anything to clean up: every step runs in memory
over a deep copy, the fully migrated result is validated in full, and only then
does the first byte reach the disk.

That is stronger than the plan's own phrasing, which says the steps are "applied
to a temporary file that replaces the original only after all steps succeed". A
temp file still has to be removed when step two of three raises, and the removal
is one more thing that can fail, at the moment the system is already failing.

WHY THE SHIPPED LADDER IS EMPTY, AND WHY THAT IS NOT A GAP IN THE TESTS. Cratekit
ships schema version 1, so there is nothing before it to migrate from. Inventing
two historical versions so that a two-step test has something to run would make
the version number a lie: a config claiming version 3 would have been written by
a build that never existed. So the ENGINE takes its ladder as a parameter, and
the ordering tests below drive it with a synthetic three-version ladder that
records the order its steps ran in. The shipped ladder is separately asserted to
have no gaps, so the day a real migration lands, the machinery it lands into is
already proven.
"""

from __future__ import annotations

import tomllib

import pytest
import tomli_w

from cratekit.core import config
from tests.test_config import valid_data

# ═══════════════════════════════════════════════════════════════════════════
# A synthetic ladder: three versions, two steps, each one recording that it ran
# ═══════════════════════════════════════════════════════════════════════════


def _ladder(record: list[str], *, fails_at: int | None = None):
    """Build a 1 -> 2 -> 3 ladder whose steps append their name to ``record``.

    ``fails_at`` makes one named step raise, which is how the "raises partway"
    scenario gets a partway to raise at. The step that fails does so AFTER
    mutating its working copy, so a test cannot pass merely because nothing was
    changed before the failure.
    """

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


def _versioned(library, version: int) -> dict:
    data = valid_data(library)
    data["schema_version"] = version
    return data


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: one version old migrates forward; two versions old runs both steps
# ═══════════════════════════════════════════════════════════════════════════


def test_a_config_one_version_old_migrates_forward(library):
    record: list[str] = []
    migrated = config.migrate(
        _versioned(library, 2), current=3, migrations=_ladder(record)
    )

    assert record == ["v2->v3"]
    assert migrated["schema_version"] == 3
    assert migrated["added_in_v3"] is True


def test_a_config_two_versions_old_migrates_through_both_steps_in_order(library):
    """Order is the assertion, not just arrival.

    A ladder that ran its steps out of order could still land on the right
    version number while producing data no step ever expected to receive.
    """
    record: list[str] = []
    migrated = config.migrate(
        _versioned(library, 1), current=3, migrations=_ladder(record)
    )

    assert record == ["v1->v2", "v2->v3"]
    assert migrated["schema_version"] == 3
    assert migrated["added_in_v2"] is True
    assert migrated["added_in_v3"] is True


def test_a_config_already_current_runs_no_steps(library):
    record: list[str] = []
    config.migrate(_versioned(library, 3), current=3, migrations=_ladder(record))
    assert record == []


def test_migration_never_mutates_the_input(library):
    """Steps run over a deep copy, so a caller's dict is never edited underneath it."""
    original = _versioned(library, 1)
    before = repr(original)
    config.migrate(original, current=3, migrations=_ladder([]))
    assert repr(original) == before


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: a migration that raises partway leaves NOTHING behind
# ═══════════════════════════════════════════════════════════════════════════


def test_a_migration_that_raises_partway_leaves_the_original_untouched(library, tmp_path):
    """The plan's third scenario, asserted on bytes AND on the directory listing.

    Two assertions rather than one. Byte equality proves the target was not
    rewritten; the directory listing proves no partial artifact was orphaned
    beside it. A test that checked only the first would pass for an
    implementation that leaves a half-written temp file every time a migration
    fails, and that file is exactly what a later run would find and puzzle over.
    """
    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))
    before_bytes = path.read_bytes()
    before_listing = sorted(p.name for p in tmp_path.iterdir())

    record: list[str] = []
    with pytest.raises(RuntimeError, match="migration 2 failed"):
        config.load_from_path(
            path, current=3, migrations=_ladder(record, fails_at=2)
        )

    assert record == ["v1->v2", "v2->v3"], "the failing step must actually have run"
    assert path.read_bytes() == before_bytes
    assert sorted(p.name for p in tmp_path.iterdir()) == before_listing


def test_a_migration_whose_result_fails_validation_writes_nothing(library, tmp_path):
    """Validation happens before the first byte, not after the last one.

    A step that produces a structurally invalid config is a bug in the step. If
    the write came first, that bug would be permanent: the user's config would
    already be the invalid thing, and the only remaining move would be a restore.
    """
    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))
    before_bytes = path.read_bytes()
    before_listing = sorted(p.name for p in tmp_path.iterdir())

    def destroys_a_required_key(data: dict) -> dict:
        out = dict(data)
        out["library"] = {k: v for k, v in out["library"].items() if k != "volume_id"}
        return out

    with pytest.raises(config.ConfigInvalid, match="library.volume_id"):
        config.load_from_path(path, current=2, migrations={1: destroys_a_required_key})

    assert path.read_bytes() == before_bytes
    assert sorted(p.name for p in tmp_path.iterdir()) == before_listing


def test_a_successful_migration_rewrites_the_file_and_keeps_a_backup(library, tmp_path):
    """The one case where bytes DO change, and what has to survive it.

    The backup is named for the version it came FROM, so a user who needs to go
    back knows which build wrote it without opening the file.
    """
    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))

    cfg = config.load_from_path(path, current=3, migrations=_ladder([]))

    assert cfg.schema_version == 3
    reread = tomllib.loads(path.read_text())
    assert reread["schema_version"] == 3
    assert (tmp_path / "config.toml.v1.bak").is_file()


def test_a_gap_in_the_ladder_is_refused_before_anything_is_written(library, tmp_path):
    """A missing step is a refusal, never a silent skip to the next version."""
    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))
    before = path.read_bytes()

    with pytest.raises(config.ConfigCorrupt, match="gap"):
        config.load_from_path(path, current=3, migrations={2: lambda d: d})

    assert path.read_bytes() == before


# ═══════════════════════════════════════════════════════════════════════════
# Forward only, in both directions
# ═══════════════════════════════════════════════════════════════════════════


def test_a_newer_config_refuses_rather_than_downgrading(library):
    """Migrations are forward-only. Downgrading is never attempted.

    A newer build may have written keys this build does not know, and this build
    would drop them on its next save. A silent drop of a value the user set is
    worse than a refusal naming both versions.
    """
    with pytest.raises(config.ConfigTooNew) as excinfo:
        config.migrate(_versioned(library, 9), current=3, migrations=_ladder([]))
    assert "9" in str(excinfo.value) and "3" in str(excinfo.value)


def test_an_absent_schema_version_is_corruption_not_age(library):
    """Cratekit has written the field since its first release.

    So a file without one was hand-edited, and guessing its version could migrate
    it with the wrong steps, which is worse than refusing.
    """
    data = valid_data(library)
    del data["schema_version"]
    with pytest.raises(config.ConfigCorrupt, match="schema_version"):
        config.migrate(data)


def test_a_non_integer_schema_version_is_corruption(library):
    data = valid_data(library)
    data["schema_version"] = "one"
    with pytest.raises(config.ConfigCorrupt):
        config.migrate(data)


# ═══════════════════════════════════════════════════════════════════════════
# The shipped ladder
# ═══════════════════════════════════════════════════════════════════════════


def test_the_shipped_ladder_has_no_gaps():
    """The version number can never get ahead of the code that upgrades to it.

    This is the test that makes an empty ladder at version 1 safe: the day
    CURRENT_SCHEMA_VERSION is bumped without a step, the build goes red.
    """
    expected = set(range(1, config.CURRENT_SCHEMA_VERSION))
    assert set(config.MIGRATIONS) == expected, (
        f"the migration ladder must cover every version below "
        f"{config.CURRENT_SCHEMA_VERSION}; missing "
        f"{sorted(expected - set(config.MIGRATIONS))}"
    )


def test_a_current_config_loads_without_a_backup_being_written(library, tmp_path):
    """No migration means no rewrite, so an ordinary load leaves the file alone."""
    path = tmp_path / "config.toml"
    _write(path, valid_data(library))
    before = sorted(p.name for p in tmp_path.iterdir())

    config.load_from_path(path)

    assert sorted(p.name for p in tmp_path.iterdir()) == before


# ═══════════════════════════════════════════════════════════════════════════
# The migration write refuses rather than proceeding unlocked
# ═══════════════════════════════════════════════════════════════════════════


def test_a_migration_that_cannot_take_the_lock_refuses(library, tmp_path, monkeypatch):
    """The one place a failed lock is NOT tolerated.

    The source system's advisory ledgers swallow a flock failure and carry on,
    which is defensible for a ledger. It is not defensible here: the job engine
    re-invokes the CLI as subprocesses, so two processes can reach an unmigrated
    config in the same second, and two concurrent migrations of one file leave it
    half-upgraded.

    The directory listing is asserted too, with the ONE expected residual named:
    the lock file itself. The lock is opened before it can be taken, so a refusal
    leaves it behind, and a listing assertion with a stated expectation is what
    stops that residual from growing into two.
    """
    # Imported inside the test rather than at module scope so this file still
    # COLLECTS on a platform without fcntl. A module-scope import turns a
    # platform gap into a collection error for the whole file, and the
    # portability guard checks literals, not platform-only imports.
    import fcntl  # noqa: PLC0415

    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))
    before = path.read_bytes()
    before_listing = sorted(p.name for p in tmp_path.iterdir())

    def cannot_lock(*args, **kwargs):
        raise OSError("locking is not supported on this filesystem")

    monkeypatch.setattr(fcntl, "flock", cannot_lock)

    with pytest.raises(config.ConfigLockUnavailable):
        config.load_from_path(path, current=3, migrations=_ladder([]))

    assert path.read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted(
        [*before_listing, "config.toml.migrate.lock"]
    )


def test_a_second_process_that_migrated_first_does_not_get_its_backup_clobbered(
    library, tmp_path, monkeypatch
):
    """The lock is worthless if the decision it protects was already made outside it.

    Two processes reach an unmigrated config in the same second, which is the
    exact scenario the lock's own docstring names. Both read version 1. A takes
    the lock, migrates, and writes ``config.toml.v1.bak`` holding version 1. B
    then takes the lock and, if it never re-reads, copies whatever is at the path
    NOW into the same backup name. The user's rollback artifact called ".v1.bak"
    ends up holding version 3, which is the half-safe outcome the lock exists to
    prevent.

    Process A is simulated at the moment B blocks on the lock, because that is the
    only interleaving that reproduces it and a real second process makes the test
    a race rather than a proof.
    """
    path = tmp_path / "config.toml"
    _write(path, _versioned(library, 1))
    v1_bytes = path.read_bytes()
    backup = tmp_path / "config.toml.v1.bak"

    original_enter = config._exclusive_lock.__enter__

    def another_process_finished_while_we_waited(self):
        acquired = original_enter(self)
        backup.write_bytes(v1_bytes)
        _write(path, _versioned(library, 3))
        return acquired

    monkeypatch.setattr(
        config._exclusive_lock, "__enter__", another_process_finished_while_we_waited
    )

    cfg = config.load_from_path(path, current=3, migrations=_ladder([]))

    assert cfg.schema_version == 3
    assert tomllib.loads(backup.read_text())["schema_version"] == 1, (
        "the version backup was overwritten with already-migrated bytes"
    )
    assert tomllib.loads(path.read_text())["schema_version"] == 3


# ═══════════════════════════════════════════════════════════════════════════
# helpers
# ═══════════════════════════════════════════════════════════════════════════


def _write(path, data: dict) -> None:
    """Write raw config data as TOML, bypassing the typed schema on purpose.

    A migration test must be able to write a shape the CURRENT schema would not
    produce, which is the whole situation a migration exists for.
    """
    path.write_text(tomli_w.dumps(data))
