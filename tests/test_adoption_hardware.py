"""U23 on real removable media: the volume proofs this unit deferred.

rekordbox exports live on FAT, and the revert ledger records identities and
vacancies about files on that volume, so the filesystem's behaviour is part of
the contract; a temp directory on APFS has other identity semantics and is never
unmounted. :func:`tests._hardware.fat_volume` refuses below FAT32's 33 MB floor,
and :func:`tests._hardware.filesystem_kind` reads the mount table because the
msdos driver allows symlinks. These FAIL rather than skip without ``hdiutil``,
since a skipped proof reads as a passing one. D1 applies to every name here, and
nothing here touches the live rekordbox database.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import revert as adopt_revert
from cratekit.adopt import scan as adopt_scan
from cratekit.core import config, tags, taxonomy
from tests import _hardware
from tests.test_config import valid_data
from tests.test_tags import _synth

TREE_ID = "adoption"


def _require_hdiutil() -> None:
    """Refuse to pretend. Absent tooling is a failure here, never a skip."""
    if not _hardware.hdiutil_available():
        raise AssertionError(
            "hdiutil is not on this machine, so U23's volume proofs cannot run. "
            "This FAILS rather than skips: a skipped hardware proof reads as a "
            "passing one in every summary anybody reads, and these proofs were "
            "already deferred once on exactly that reading."
        )


@pytest.fixture
def fat(tmp_path):
    """A real mounted FAT32 volume, asked what it is rather than probed."""
    _require_hdiutil()
    with _hardware.fat_volume() as mountpoint:
        kind = _hardware.filesystem_kind(mountpoint)
        assert kind == "msdos", (
            f"the fixture mounted {kind!r} and these proofs are about FAT. The "
            f"kind is read from the mount table rather than inferred from "
            f"behaviour, because the macOS msdos driver allows symlinks and "
            f"case folding matches the default filesystem too, so every cheap "
            f"behavioural probe answers the same on both."
        )
        yield mountpoint


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A config whose ledgers live on the default filesystem."""
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    resolved = config.from_dict(valid_data(root))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    return resolved


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


def _genre_of(declared_taxonomy) -> str:
    """A genre the shipped template really routes, derived rather than spelled."""
    for bucket in declared_taxonomy.buckets:
        if bucket.id == declared_taxonomy.fallback.bucket:
            continue
        resolution = adopt_scan.routing.resolve_bucket(declared_taxonomy, bucket.display)
        if resolution.bucket_id == bucket.id and resolution.match is not (
            adopt_scan.routing.Match.FALLBACK
        ):
            return bucket.display
    raise AssertionError("the shipped template declares no routable bucket")


# ═══════════════════════════════════════════════════════════════════════════
# The census, over a library that is actually on the removable volume
# ═══════════════════════════════════════════════════════════════════════════


def test_a_cloud_backed_track_on_a_fat_volume_is_EXCLUDED_and_never_applicable(fat, cfg, declared):
    """AE12's second half: the named category has to reach the DISPOSITION."""
    music = fat / "Music"
    music.mkdir()
    genre = _genre_of(declared)

    present = _synth(music, ".mp3")
    evicted = music / "Evicted.mp3"
    (music / ".Evicted.mp3.icloud").write_bytes(b"")

    rows = [
        adopt_scan.CollectionRow("present", str(present), genre, False),
        adopt_scan.CollectionRow("evicted", str(evicted), genre, False),
    ]
    scanned = list(adopt_scan.scan_rows(rows, declared, root=fat))
    found = {track.content_id: track for track in scanned}

    assert found["present"].readability is adopt_scan.Readability.READABLE
    assert found["evicted"].readability is adopt_scan.Readability.ONLINE_ONLY

    assert found["evicted"].disposition is adopt_scan.Disposition.EXCLUDED, (
        "the row is named online-only and then routed anyway"
    )
    assert found["present"].disposition is adopt_scan.Disposition.ROUTE

    built = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)
    applicable = {entry.content_id for entry in built.applicable()}
    assert "evicted" not in applicable, "an excluded track is applicable"
    assert "present" in applicable
    assert {track.content_id for track in scanned} == {"present", "evicted"}, (
        "AE12: excluded is carried"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The revert ledger, over files on the removable volume
# ═══════════════════════════════════════════════════════════════════════════


def test_an_absent_genre_on_a_fat_file_comes_back_ABSENT(fat, cfg):
    """Scenario 5, "reverted exactly", including the absence, on real msdos."""
    music = fat / "Music"
    music.mkdir()
    path = _synth(music, ".mp3")
    assert tags.read_tag_values(path, "genre") is None

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    assert tags.read_tag_values(path, "genre") == ("Adopted Genre",)

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}
    assert tags.read_tag_values(path, "genre") is None, "an absence came back as a value"


def test_a_deleted_fat_file_strands_its_record_for_a_byte_identical_copy(fat, cfg):
    """The half of round 8's vacancy guard that must still say YES."""
    music = fat / "Music"
    music.mkdir()
    path = _synth(music, ".mp3")
    tags.write_tag_values(path, "genre", ("Original Genre",))

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    assert len(adopt_revert.read(cfg).snapshots) == 1

    moved = music / "Renamed.mp3"
    shutil.copyfile(path, moved)
    path.unlink()
    assert music.is_dir(), "the containing directory has to stay present"

    adopt_revert.write_tag_with_record(
        cfg, moved, field="genre", written="Adopted Genre", entry_id="e2"
    )

    snapshots = adopt_revert.read(cfg).snapshots
    assert len(snapshots) == 1, "a second record was written beside the first"
    assert snapshots[0].original == ("Original Genre",), "adoption's value read as original"
    assert Path(snapshots[0].path) == moved


def test_a_record_whose_directory_is_gone_is_NOT_treated_as_a_deleted_file(fat, cfg):
    """Round 8's fix, driven on real msdos: absence of a path is not evidence."""
    music = fat / "Music"
    music.mkdir()
    backup_dir = fat / "Backup"
    backup_dir.mkdir()

    path = _synth(music, ".mp3")
    tags.write_tag_values(path, "genre", ("Original Genre",))
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )

    backup = backup_dir / "Copy.mp3"
    shutil.copyfile(path, backup)
    # REMOVED BY HAND RATHER THAN BY ``shutil.rmtree``, and that is a FAT fact rather
    # than a preference. rmtree walks with ``dir_fd`` relative unlinks where the
    # platform claims support, and on this msdos volume that walk raises
    # FileNotFoundError for the directory it is standing in.
    for child in sorted(music.iterdir()):
        child.unlink()
    music.rmdir()
    assert not music.exists(), "the whole containing directory has to be gone"

    adopt_revert.write_tag_with_record(
        cfg, backup, field="genre", written="Adopted Genre", entry_id="e2"
    )

    snapshots = adopt_revert.read(cfg).snapshots
    by_path = {Path(record.path): record for record in snapshots}
    assert len(snapshots) == 2, "the byte identical copy was handed the vanished directory's record"
    assert by_path[path].original == ("Original Genre",), "the original must survive"
    assert by_path[backup].original == ("Adopted Genre",), "the copy keeps its own value"
