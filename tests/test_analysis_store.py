"""R-14. The analysis store is the share beside the database, and nothing else.

A rekordbox library on an external volume has two directory trees ending in
``PIONEER/USBANLZ``. The share under ``PIONEER/Master`` holds the beat grids and
every row resolves into it. The one at the volume root is the USB export cache
and no row resolves into it. ``AnalysisDataPath`` is stored share relative, so a
join to the library root finds nothing and reads as "the analysis is missing".

Every fixture here plants BOTH trees where the claim is about which one is
found, because a fixture holding only the right tree cannot tell the right join
from a wrong one that happens to land in the only place there is.
"""

from __future__ import annotations

import ast
import contextlib
import re
import stat
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.core import analysis_store, backup_facts, config, session
from cratekit.modules.tools import backup

SRC = Path(__file__).resolve().parents[1] / "src" / "cratekit"

#: A track's analysis key, in the UUID shape the share uses.
KEY = "1f0c2b9e-6a41-4c55-9d1e-7b3f0a2c5e11"

#: A stored ``AnalysisDataPath`` in the shape rekordbox writes it: share
#: relative, with a leading separator, a three character bucket, then the key.
STORED = f"/PIONEER/USBANLZ/8d2/{KEY}/ANLZ0000.DAT"

#: The date an outside database was accepted, in the shape the loader requires.
ACCEPTED = "2026-09-11"


def _cfg(
    root: Path, db_path: Path, monkeypatch, *, acknowledged: str | None = None
) -> config.Config:
    """A validated config over ``root``, with the database wherever it is put.

    The environment override is aimed at the same root, because validation
    applies it before the containment rule runs and the suite's isolation points
    it elsewhere.
    """
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    library: dict[str, str] = {
        "root": str(root),
        "volume_id": "F1E2-D3C4",
        "db_path": str(db_path),
    }
    if acknowledged is not None:
        library["db_outside_root_acknowledged_on"] = acknowledged
    return config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": library,
            "paths": {"download_staging": str(root.parent / "staging")},
            "profile": {"name": "slim"},
            "backup": {
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        }
    )


@pytest.fixture
def volume(tmp_path) -> Path:
    root = tmp_path / "volume"
    (root / "Music").mkdir(parents=True)
    return root


@pytest.fixture
def contained(volume, monkeypatch) -> config.Config:
    """The external volume layout: the database, and so the share, under the root."""
    return _cfg(volume, volume / "PIONEER" / "Master" / "master.db", monkeypatch)


@pytest.fixture
def home(tmp_path) -> Path:
    """Where an outside database lives, standing in for the platform default."""
    return tmp_path / "home" / "rekordbox"


@pytest.fixture
def outside(volume, home, monkeypatch) -> config.Config:
    """The acknowledged layout: the database, and so the share, off the volume."""
    return _cfg(volume, home / "master.db", monkeypatch, acknowledged=ACCEPTED)


@pytest.fixture
def rclone_on_path(tmp_path, monkeypatch) -> Path:
    """A resolvable rclone that nothing executes, since every runner is injected."""
    fake = tmp_path / "bin" / "rclone"
    fake.parent.mkdir(parents=True, exist_ok=True)
    fake.write_text("#!/bin/sh\nexit 0\n")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(fake))
    return fake


def _plant(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"PMAI")
    return path


def _both_trees(volume: Path) -> tuple[Path, Path]:
    """The grid in the share, and a cache file in the export tree beside it."""
    grid = _plant(
        volume / "PIONEER" / "Master" / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY
        / "ANLZ0000.DAT"
    )
    cache = _plant(volume / "PIONEER" / "USBANLZ" / "P001" / "0000A1B2" / "ANLZ0000.DAT")
    return grid, cache


def _succeeding(_command: backup.Command) -> backup.CommandResult:
    return backup.CommandResult(returncode=0, stdout="")


def _codes(warnings) -> list[str]:
    return [warning["code"] for warning in warnings]


# ═══════════════════════════════════════════════════════════════════════════
# The join
# ═══════════════════════════════════════════════════════════════════════════


def test_a_stored_analysis_path_joins_to_the_share_and_not_to_the_library_root(
    contained, volume
):
    """The pin R-14 closes on, measured over a volume holding both trees."""
    grid, cache = _both_trees(volume)

    resolved = analysis_store.analysis_file(contained, STORED)

    assert resolved == grid, f"the join landed on {resolved}, not on the grid in the share"
    assert resolved.is_file()
    assert volume / "PIONEER" / "USBANLZ" not in resolved.parents, (
        "the join resolved into the USB export cache, which no row points into"
    )
    assert cache.is_file()
    assert not (volume / STORED.lstrip("/")).exists(), (
        "the fixture lets the library root join find a file, so it cannot tell "
        "the right join from the wrong one"
    )


def test_the_share_follows_the_database_when_it_sits_outside_the_root(outside, home):
    """The share is the database's sibling, not a fixed place under the library."""
    assert analysis_store.share_root(outside) == home / "share"
    assert analysis_store.analysis_file(outside, STORED) == (
        home / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY / "ANLZ0000.DAT"
    )


def test_a_windows_separated_stored_path_joins_to_the_same_file(contained, volume):
    expected = volume / "PIONEER" / "Master" / "share" / "PIONEER" / "USBANLZ" / "8d2"
    assert analysis_store.analysis_file(contained, STORED.replace("/", "\\")) == (
        expected / KEY / "ANLZ0000.DAT"
    )


def test_an_empty_stored_path_is_no_analysis_rather_than_a_missing_file(contained):
    assert analysis_store.analysis_file(contained, "") is None
    assert analysis_store.analysis_file(contained, "/") is None


def test_a_stored_path_that_climbs_out_of_the_share_is_refused(contained):
    with pytest.raises(ValueError, match="climbs out of the analysis share"):
        analysis_store.analysis_file(contained, "/PIONEER/../../master.db")


# ═══════════════════════════════════════════════════════════════════════════
# The watch
# ═══════════════════════════════════════════════════════════════════════════


def test_a_contained_share_is_watched_through_the_library_root(contained, volume):
    grid, _cache = _both_trees(volume)
    roots = analysis_store.watch_roots(contained)
    assert roots == (volume,)
    assert grid in session.analysis_files_under(roots)


def test_an_outside_share_is_watched_alongside_the_library_root(outside, volume, home):
    """In this layout the root holds no grid, so the root alone is a barren watch."""
    _both_trees(volume)
    grid = _plant(home / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY / "ANLZ0000.DAT")
    assert grid not in session.analysis_files_under([volume]), (
        "the fixture put the outside grid under the library root, so it cannot "
        "show that the root alone misses it"
    )

    roots = analysis_store.watch_roots(outside)

    assert roots == (volume, home / "share")
    assert grid in session.analysis_files_under(roots)


def _hand_listed(function: ast.AST) -> set[str]:
    """Names this function binds to a literal list, tuple or set of roots."""
    literal = (ast.List, ast.Tuple, ast.Set)
    names: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and isinstance(node.value, literal):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.value, literal)
            and isinstance(node.target, ast.Name)
        ):
            names.add(node.target.id)
    return names


def test_no_call_site_hand_lists_the_roots_an_analysis_watch_covers():
    """Every root list is derived, so the share cannot be left out of one again.

    A literal is refused whether it is written at the keyword or bound to a name
    first, which were the two shapes the call sites used before R-14. A parameter
    passed through, or a list built from one, is not a literal and is allowed:
    those are the writers the call sites feed, not call sites themselves.
    """
    offenders: list[str] = []
    for path in sorted(SRC.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            bound = _hand_listed(function)
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                for keyword in node.keywords:
                    if keyword.arg != "analysis_roots":
                        continue
                    value = keyword.value
                    if isinstance(value, (ast.List, ast.Tuple, ast.Set)) or (
                        isinstance(value, ast.Name) and value.id in bound
                    ):
                        offenders.append(f"{path.relative_to(SRC)}:{node.lineno}")
    assert not offenders, (
        "these call sites hand-list the roots an analysis watch covers rather than "
        "taking analysis_store.watch_roots, so a database outside the library root "
        f"leaves every grid unwatched: {sorted(set(offenders))}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The backup
# ═══════════════════════════════════════════════════════════════════════════


def _rclone_matches(pattern: str, path: str) -> bool:
    """Whether an rclone filter pattern matches a slash rooted path.

    rclone's rules as far as the mirror's patterns use them: a leading slash
    anchors at the transfer root, otherwise the pattern matches any trailing run
    of components, ``**`` crosses separators and ``*`` does not.
    """
    body = ""
    index = 0
    text = pattern.lstrip("/")
    while index < len(text):
        if text.startswith("**", index):
            body += ".*"
            index += 2
        elif text[index] == "*":
            body += "[^/]*"
            index += 1
        elif text[index] == "?":
            body += "[^/]"
            index += 1
        else:
            body += re.escape(text[index])
            index += 1
    prefix = "^/" if pattern.startswith("/") else "(^|.*/)"
    return re.match(prefix + body + "$", path) is not None


def test_a_contained_share_rides_the_mirror_and_draws_no_warning(
    contained, volume, rclone_on_path
):
    """The mirror excludes the database fileset by name, and never the share."""
    grid, _cache = _both_trees(volume)
    config.state_path("rekordbox_db", contained).write_bytes(b"SQLite format 3\x00")

    plan = backup.plan_backup(contained, process_lister=lambda: (), settings_dirs=())

    mirror = plan.portion(backup_facts.Portion.FILES).commands[0]
    assert mirror.label == backup.MIRROR
    source = Path(mirror.argv[2])
    assert source in grid.parents, f"the mirror copies {source}, which does not hold the share"
    relative = "/" + grid.relative_to(source).as_posix()
    excludes = [mirror.argv[i + 1] for i, arg in enumerate(mirror.argv) if arg == "--exclude"]
    assert "/PIONEER/Master/master.db" in excludes, (
        "the database is not excluded, so this reading of the patterns is not the mirror's"
    )
    assert not [p for p in excludes if _rclone_matches(p, relative)], (
        f"the mirror excludes the grid at {relative}, so no portion carries the share"
    )
    assert plan.portion(backup_facts.Portion.DATABASE).warnings == ()


def _share_commands(plan: backup.BackupPlan) -> list[backup.Command]:
    return [c for p in plan.portions for c in p.commands if c.label == backup.SNAPSHOT_SHARE]


def _outside_library(home: Path) -> Path:
    """An outside database with a grid in the share beside it. Returns the share."""
    home.mkdir(parents=True, exist_ok=True)
    (home / "master.db").write_bytes(b"SQLite format 3\x00")
    _plant(home / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY / "ANLZ0000.DAT")
    return home / "share"


def test_an_outside_share_rides_the_database_portion_to_its_own_mirror(
    outside, home, rclone_on_path
):
    """R-338's cost, reversed: a command names the share, and nothing warns.

    Before this the plan named the share in no command and said so with a
    warning, which is a backup that returns every row without its grids.
    """
    share = _outside_library(home)

    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=())

    database = plan.portion(backup_facts.Portion.DATABASE)
    assert database.will_run
    carried = _share_commands(plan)
    assert len(carried) == 1, f"the share is carried by {len(carried)} commands, wanted one"
    assert carried[0] in database.commands, "the share rides a portion with no rekordbox gate"
    argv = carried[0].argv
    assert argv[1:3] == ("sync", str(share))
    assert argv[3] == "remote:database-snapshots/analysis-share/f1e2-d3c4/current"
    # One run is undoable, as the mirror's is: whatever the sync would overwrite
    # or delete moves to a dated folder first, outside the mirrored tree.
    assert argv[argv.index("--backup-dir") + 1] == (
        f"remote:database-snapshots/analysis-share/f1e2-d3c4/archive/{plan.stamp}"
    )
    assert database.warnings == ()

    outcome = backup.run_backup(outside, plan, runner=_succeeding, publish=False)

    ran = {row["portion"]: row for row in backup.outcome_payload(outcome)["portions"]}
    assert ran["database"]["ran"] is True
    assert ran["database"]["warnings"] == []


def test_the_share_is_the_last_thing_the_database_portion_copies(
    outside, home, rclone_on_path, tmp_path
):
    """Gigabytes go after the settings, so a share that fails costs nothing else."""
    _outside_library(home)
    settings = tmp_path / "rekordbox6"
    settings.mkdir()

    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=(settings,))

    labels = [c.label for c in plan.portion(backup_facts.Portion.DATABASE).commands]
    assert labels == [
        backup.SNAPSHOT_DATABASE,
        backup.SNAPSHOT_IDENTITY,
        backup.SNAPSHOT_SETTINGS,
        backup.SNAPSHOT_SHARE,
    ]


def test_a_share_that_did_not_copy_fails_the_portion_and_publishes_no_age(
    outside, home, rclone_on_path
):
    """A database age published over an uncarried share is R-338 said quietly."""
    _outside_library(home)
    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=())

    def runner(command: backup.Command) -> backup.CommandResult:
        failed = command.label == backup.SNAPSHOT_SHARE
        return backup.CommandResult(returncode=1 if failed else 0, stderr="quota exceeded")

    outcome = backup.run_backup(outside, plan, runner=runner)

    database = next(p for p in outcome.portions if p.portion is backup_facts.Portion.DATABASE)
    assert database.ran is False
    assert "quota exceeded" in database.detail
    assert backup_facts.Portion.DATABASE not in backup_facts.read_facts(outside)
    assert not outcome.ok


def test_a_live_rekordbox_refuses_the_share_with_the_database(outside, home, rclone_on_path):
    """rekordbox writes the share while it analyses, so the share has the database's gate."""
    _outside_library(home)

    for running in (("rekordbox",), ("rekordboxAgent",)):
        plan = backup.plan_backup(outside, process_lister=lambda r=running: r, settings_dirs=())

        database = plan.portion(backup_facts.Portion.DATABASE)
        assert database.refusal is backup.Refusal.REKORDBOX_RUNNING
        assert _share_commands(plan) == [], f"the share is copied under a live {running[0]}"


def test_a_contained_share_is_not_copied_twice(contained, volume, rclone_on_path):
    """The mirror already carries it, so the contained layout gains no command."""
    _both_trees(volume)
    config.state_path("rekordbox_db", contained).write_bytes(b"SQLite format 3\x00")

    plan = backup.plan_backup(contained, process_lister=lambda: (), settings_dirs=())

    assert _share_commands(plan) == []


def test_an_outside_share_that_is_not_there_is_said_and_not_synced(
    outside, home, rclone_on_path
):
    """Nothing to carry is a different fact from carried, and a sync of nothing empties the copy."""
    home.mkdir(parents=True)
    (home / "master.db").write_bytes(b"SQLite format 3\x00")

    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=())

    database = plan.portion(backup_facts.Portion.DATABASE)
    assert database.will_run, "the database portion refused, so the warning proves nothing"
    assert _share_commands(plan) == []
    assert _codes(database.warnings) == [backup.ANALYSIS_SHARE_ABSENT]
    assert str(home / "share") in database.warnings[0]["message"]

    outcome = backup.run_backup(outside, plan, runner=_succeeding, publish=False)
    ran = {row["portion"]: row for row in backup.outcome_payload(outcome)["portions"]}
    assert _codes(ran["database"]["warnings"]) == [backup.ANALYSIS_SHARE_ABSENT]


def test_the_absent_share_warning_survives_a_refused_database_portion(outside, rclone_on_path):
    """A skipped snapshot does not make an absent share a carried one."""
    plan = backup.plan_backup(
        outside, process_lister=lambda: ("rekordbox",), settings_dirs=()
    )

    outcome = backup.run_backup(outside, plan, runner=_succeeding, publish=False)

    database = next(
        p for p in outcome.portions if p.portion is backup_facts.Portion.DATABASE
    )
    assert database.refusal is backup.Refusal.REKORDBOX_RUNNING
    assert _codes(database.warnings) == [backup.ANALYSIS_SHARE_ABSENT]


def test_two_libraries_under_one_snapshot_root_keep_two_share_mirrors(
    volume, home, monkeypatch, rclone_on_path
):
    """A sync makes its destination match, so one shared mirror is each library archiving the other."""
    _outside_library(home)
    mine = _cfg(volume, home / "master.db", monkeypatch, acknowledged=ACCEPTED)
    theirs = replace(mine, library=replace(mine.library, volume_id="0A0B-0C0D"))

    destinations = {
        _share_commands(
            backup.plan_backup(each, process_lister=lambda: (), settings_dirs=())
        )[0].argv[3]
        for each in (mine, theirs)
    }

    assert len(destinations) == 2, destinations


def test_a_library_with_no_usable_identity_still_carries_its_share(
    volume, home, monkeypatch, rclone_on_path
):
    """An identity that cannot be a path component is not interpolated into one."""
    _outside_library(home)
    mine = _cfg(volume, home / "master.db", monkeypatch, acknowledged=ACCEPTED)
    unnamed = replace(mine, library=replace(mine.library, volume_id="../up and out"))

    carried = _share_commands(
        backup.plan_backup(unnamed, process_lister=lambda: (), settings_dirs=())
    )

    assert carried[0].argv[3] == "remote:database-snapshots/analysis-share/_unrecorded/current"


def test_a_rehearsed_backup_transfers_no_share(outside, home, rclone_on_path):
    """The share's label is a transferring one, so the preview neutralizes it."""
    _outside_library(home)
    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=())
    issued: list[backup.Command] = []

    def runner(command: backup.Command) -> backup.CommandResult:
        issued.append(command)
        return backup.CommandResult(returncode=0)

    backup.run_backup(outside, plan, runner=runner, dry_run=True)

    shares = [c for c in issued if c.label == backup.SNAPSHOT_SHARE]
    assert shares and all(c.argv[-1] == "--dry-run" for c in shares)


# ═══════════════════════════════════════════════════════════════════════════
# The restore
# ═══════════════════════════════════════════════════════════════════════════

STAMP = "2026-08-01T000000Z"


def _open_gates():
    return contextlib.nullcontext()


class _Remote:
    """A runner that answers the restore's listings and records everything else."""

    def __init__(self, *, share: str = "PIONEER/\n", share_exit: int = 0, marker: bool = True):
        self.commands: list[backup.Command] = []
        self.share = share
        self.share_exit = share_exit
        self.marker = marker

    def __call__(self, command: backup.Command) -> backup.CommandResult:
        self.commands.append(command)
        if command.label == backup.LIST_SNAPSHOT_IDENTITY:
            name = backup.IDENTITY_MARKER_PREFIX + "f1e2-d3c4\n"
            return backup.CommandResult(returncode=0, stdout=name if self.marker else "")
        if command.label == backup.LIST_SNAPSHOT_CONTENTS:
            return backup.CommandResult(returncode=0, stdout="master.db\n")
        if command.label == backup.LIST_SHARE:
            return backup.CommandResult(returncode=self.share_exit, stdout=self.share)
        return backup.CommandResult(returncode=0)

    def labelled(self, label: str) -> list[backup.Command]:
        return [c for c in self.commands if c.label == label]


def _planned(cfg: config.Config, target: Path, remote: _Remote) -> backup.RestorePlan:
    target.mkdir(parents=True, exist_ok=True)
    return backup.plan_restore(
        cfg,
        target=target,
        confirmed=True,
        snapshot=STAMP,
        runner=remote,
        process_lister=lambda: (),
        gates=_open_gates,
    )


def test_a_restore_puts_an_outside_share_back_beside_the_database(
    outside, rclone_on_path, tmp_path
):
    """R-338's other half: the grids land where the restored rows look for them."""
    remote = _Remote()
    target = tmp_path / "recovered"

    plan = _planned(outside, target, remote)

    shares = [c for c in plan.commands if c.label == backup.RESTORE_SHARE]
    assert len(shares) == 1
    assert shares[0].argv[1:4] == (
        "copy",
        "remote:database-snapshots/analysis-share/f1e2-d3c4/current",
        str(plan.database_target.parent / analysis_store.SHARE_DIRNAME),
    )
    assert plan.commands[-1] == shares[0], "the share is pulled before the database set"
    assert plan.share_absent is False

    backup.run_restore(plan, outside, runner=remote, gates=_open_gates)
    assert remote.labelled(backup.RESTORE_SHARE) == shares


def test_the_share_is_listed_before_anything_is_cleared(outside, rclone_on_path, tmp_path):
    """The ledger's third option: planned from a listing, never found out by a failed copy."""
    remote = _Remote(share="", share_exit=backup.RCLONE_DIRECTORY_NOT_FOUND)
    target = tmp_path / "recovered"
    target.mkdir()
    log = target / "master.db-wal"
    log.write_bytes(b"live log")

    plan = _planned(outside, target, remote)

    assert log.exists(), "planning cleared a sidecar"
    assert [c for c in plan.commands if c.label == backup.RESTORE_SHARE] == []
    assert plan.share_absent is True


def test_a_share_mirror_that_lists_empty_is_absent_too(outside, rclone_on_path, tmp_path):
    remote = _Remote(share="\n")

    plan = _planned(outside, tmp_path / "recovered", remote)

    assert [c for c in plan.commands if c.label == backup.RESTORE_SHARE] == []
    assert plan.share_absent is True


def test_a_share_mirror_that_could_not_be_listed_refuses_before_the_sidecars_go(
    outside, rclone_on_path, tmp_path
):
    """A remote that did not answer is not a remote holding no share."""
    remote = _Remote(share="", share_exit=1)
    target = tmp_path / "recovered"
    target.mkdir()
    log = target / "master.db-wal"
    log.write_bytes(b"live log")

    with pytest.raises(backup.BackupRefused) as refused:
        _planned(outside, target, remote)

    assert refused.value.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE
    assert "analysis share" in refused.value.detail
    assert log.exists()
    assert remote.labelled(backup.RESTORE_DATABASE) == []


def test_an_unmarked_snapshot_pulls_this_librarys_share(outside, rclone_on_path, tmp_path):
    """A marker that failed to write does not orphan the share the same run carried."""
    remote = _Remote(marker=False)

    plan = _planned(outside, tmp_path / "recovered", remote)

    shares = [c for c in plan.commands if c.label == backup.RESTORE_SHARE]
    assert shares[0].argv[2] == "remote:database-snapshots/analysis-share/f1e2-d3c4/current"


def test_a_contained_restore_neither_lists_nor_pulls_a_share(
    contained, rclone_on_path, tmp_path
):
    """The mirror half carries a contained share, so the database half gains nothing."""
    remote = _Remote()

    plan = _planned(contained, tmp_path / "recovered", remote)

    assert remote.labelled(backup.LIST_SHARE) == []
    assert [c for c in plan.commands if c.label == backup.RESTORE_SHARE] == []
    assert plan.share_absent is False


def test_a_rehearsed_restore_transfers_no_share(outside, rclone_on_path, tmp_path):
    remote = _Remote()
    plan = _planned(outside, tmp_path / "recovered", remote)

    backup.run_restore(plan, outside, runner=remote, dry_run=True, gates=_open_gates)

    issued = remote.labelled(backup.RESTORE_SHARE)
    assert issued and all(c.argv[-1] == "--dry-run" for c in issued)


# ═══════════════════════════════════════════════════════════════════════════
# The share is read and copied, and never authored
# ═══════════════════════════════════════════════════════════════════════════


def _is_local(place: str) -> bool:
    """Whether an rclone location is on this machine. A remote is ``name:path``."""
    return ":" not in place.split("/", 1)[0]


def test_no_backup_command_writes_to_this_machine_least_of_all_to_the_share(
    outside, home, rclone_on_path, tmp_path
):
    """The beat grid constraint, for the capture: the share is a source and only a source.

    Every grid this library holds is under the share, so a backup command with
    the share, or anything local, as its destination is a command that can write
    one. Read from the plan, which is the run (``run_backup`` executes the plan's
    own commands and adds only a flag).
    """
    share = _outside_library(home)
    settings = tmp_path / "rekordbox6"
    settings.mkdir()
    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=(settings,))
    assert _share_commands(plan), "no share command was planned, so this proves nothing"

    for command in (c for p in plan.portions for c in p.commands):
        verb, places = command.argv[1], [a for a in command.argv[2:] if not a.startswith("--")]
        if verb in {"sync", "copy"}:
            source, destination = places[0], places[1]
            assert not _is_local(destination), f"{command.label} writes to {destination}"
            assert not destination.startswith(str(share))
            assert _is_local(source)
        backup_dirs = [
            command.argv[i + 1] for i, a in enumerate(command.argv) if a == "--backup-dir"
        ]
        assert not [d for d in backup_dirs if _is_local(d)], command


def test_a_restore_writes_the_share_with_a_copy_and_only_beside_the_database(
    outside, rclone_on_path, tmp_path
):
    """A copy adds and overwrites. A sync would delete every grid the mirror lacks."""
    plan = _planned(outside, tmp_path / "recovered", _Remote())

    share = next(c for c in plan.commands if c.label == backup.RESTORE_SHARE)
    assert share.argv[1] == "copy"
    assert "--backup-dir" not in share.argv
    assert Path(share.argv[3]) == plan.database_target.parent / analysis_store.SHARE_DIRNAME
    for command in plan.commands:
        assert command.argv[1] == "copy", f"{command.label} is a {command.argv[1]}"


def test_the_backup_module_moves_analysis_files_and_never_opens_one():
    """The constraint's other half, read off the source: no file is authored here.

    The module's whole file surface is a directory it makes and the sidecars it
    clears. Anything that opens or writes a file would be the first thing in it
    able to produce an analysis file rather than move one, so it is refused by
    name rather than left to a review to notice.
    """
    tree = ast.parse((SRC / "modules" / "tools" / "backup.py").read_text())
    authoring = {
        "open", "write_bytes", "write_text", "touch", "copy", "copy2", "copyfile",
        "copytree", "move", "replace", "rename",
    }
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            target = node.func
            name = target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
            called.add(name)
    assert {"unlink", "mkdir"} <= called, "the walk is not seeing this module's file calls"
    assert not (called & authoring), sorted(called & authoring)


def test_the_retired_warning_has_no_producer_left():
    """R-338's closing condition, third clause."""
    holders = [
        path.relative_to(SRC).as_posix()
        for path in SRC.rglob("*.py")
        if "share-not-carried" in path.read_text()
    ]
    assert holders == []
