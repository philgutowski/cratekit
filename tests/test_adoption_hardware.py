"""U23 on real removable media: the volume proofs this unit deferred.

WHY A REAL VOLUME AND NOT A TEMP DIRECTORY, which is the reason these were
deferred rather than written against ``tmp_path`` five sessions ago. rekordbox
exports live on FAT. Adoption reads and classifies a library that is sitting on
a removable volume, and the revert ledger records identities and vacancies about
files on that volume, so the filesystem's own behaviour is part of the contract
rather than a detail underneath it. A temp directory on APFS does not stand in:
it has different identity semantics, it is never unmounted, and its directories
never vanish underneath a recorded path.

WHAT THE HARNESS ALREADY PAID FOR, restated here so nobody re-learns it.
FAT32 refuses to format under about 33 MB and ``hdiutil`` reports that refusal
as a permissions error, which sends you looking at entitlements instead of at
the size; :func:`tests._hardware.fat_volume` refuses first and says so. And the
macOS msdos driver ALLOWS symlinks, so a behavioural probe cannot tell you which
filesystem you are on. :func:`tests._hardware.filesystem_kind` reads the mount
table instead, and that is what these tests ask.

THESE FAIL RATHER THAN SKIP when ``hdiutil`` is absent. A skipped hardware proof
is indistinguishable from a passing one in every summary anybody reads, and this
whole file exists because the proofs that were deferred read as covered.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track, and nothing here opens, copies, or names the live rekordbox
database.
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
    """A config whose ledgers live on the default filesystem.

    Deliberately NOT on the FAT volume. What is under test is adoption's
    handling of FILES on removable media, and putting the ledger there too would
    fold a second question, whether the ledger's locking survives msdos, into
    every assertion below. That question is real and it belongs to its own test
    rather than to these.
    """
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
        resolution = adopt_scan.routing.resolve_bucket(
            declared_taxonomy, bucket.display
        )
        if resolution.bucket_id == bucket.id and resolution.match is not (
            adopt_scan.routing.Match.FALLBACK
        ):
            return bucket.display
    raise AssertionError("the shipped template declares no routable bucket")


# ═══════════════════════════════════════════════════════════════════════════
# The census, over a library that is actually on the removable volume
# ═══════════════════════════════════════════════════════════════════════════


def test_a_cloud_backed_track_on_a_fat_volume_is_EXCLUDED_and_never_applicable(
    fat, cfg, declared
):
    """AE12's second half: the named category has to reach the DISPOSITION.

    The existing census test proves an online-only row is named
    ``ONLINE_ONLY``. It does not prove that naming it keeps it out of the work,
    and an independent mutation table measured the gap: widening
    :data:`cratekit.adopt.scan.ADOPTABLE` to admit
    :attr:`Readability.ONLINE_ONLY` killed ZERO tests against a green suite of
    3782. A category that is reported and then adopted anyway is worse than one
    that was never reported, because the report says the tool understood.

    WHAT IT WOULD COST, which is why this is asserted about ``applicable`` and
    not only about the disposition. An applicable entry is one ``apply_plan``
    writes a tag to. Writing a tag to a cloud-backed stub materializes the file:
    the provider is asked for bytes that are not here, on a volume the person
    plugged in expecting a library read. On a whole library that is every
    evicted track downloaded, in bulk, on an approval given for a plan that said
    the file was excluded.

    Driven on real msdos rather than on ``tmp_path`` because the stub convention
    is a filename convention, and FAT is the filesystem whose name mangling and
    case folding would break it if anything did.
    """
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
        "the row is named online-only and then routed anyway, so the plan "
        "proposes writing a tag to a file whose bytes are not on this machine"
    )
    assert found["present"].disposition is adopt_scan.Disposition.ROUTE

    built = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)
    applicable = {entry.content_id for entry in built.applicable()}
    assert "evicted" not in applicable, (
        "an excluded track reached the applicable set, which is the set "
        "apply_plan writes tags to"
    )
    assert "present" in applicable
    assert {track.content_id for track in scanned} == {"present", "evicted"}, (
        "AE12 says an excluded track is carried in the plan rather than "
        "omitted from it"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The revert ledger, over files on the removable volume
# ═══════════════════════════════════════════════════════════════════════════


def test_an_absent_genre_on_a_fat_file_comes_back_ABSENT(fat, cfg):
    """Scenario 5, "reverted exactly", including the absence, on real msdos.

    The sibling of this test runs on the default filesystem. It is repeated here
    because the two branches of :func:`cratekit.adopt.revert.restore_tag` are a
    DELETE and a WRITE, and a delete is the operation whose result a filesystem
    is most able to differ about: FAT has no extended attributes, no resource
    fork and its own rewrite behaviour for a container whose tag block shrinks.
    """
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
    assert tags.read_tag_values(path, "genre") is None, (
        "the field came back as a value rather than as an absence, which "
        "leaves a tag on the file that was never there"
    )


def test_a_deleted_fat_file_strands_its_record_for_a_byte_identical_copy(fat, cfg):
    """The half of round 8's vacancy guard that must still say YES.

    A record is handed on by its BYTES only when its recorded path is
    demonstrably vacant. Vacant has to keep meaning something, or the guard that
    round 8 tightened would have closed the byte search entirely and a renamed
    file would silently get a second record with adoption's own value stored as
    its original.

    So: adopt on the volume, copy the adopted file, delete the original while
    its directory stays mounted and answering, and adopt the copy. The ledger
    must still hold ONE record and it must still hold the value the file had
    BEFORE adoption ever ran.
    """
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
    assert len(snapshots) == 1, (
        "a second record was written beside the first, so one of the two "
        "originals is now unreachable"
    )
    assert snapshots[0].original == ("Original Genre",), (
        "the surviving record stores adoption's OWN value as the original, "
        "which puts the user's value in no file and no record"
    )
    assert Path(snapshots[0].path) == moved


def test_a_record_whose_directory_is_gone_is_NOT_treated_as_a_deleted_file(fat, cfg):
    """Round 8's fix, driven on real msdos: absence of a path is not evidence.

    THE MOTIVATING CASE IS AN EJECTED VOLUME and the mechanism is the branch
    below. ``_the_recorded_path_is_vacant`` asks for the recorded path's
    containing directory to be PRESENT AND ANSWERING before it will call the
    file gone. A deleted or renamed file leaves its directory behind; a volume
    that went away takes the whole path with it, mount point included, and the
    previous version of this test was ``not Path(record.path).exists()`` alone,
    which cannot tell those apart.

    WHAT IS ACTUALLY DRIVEN HERE, said plainly rather than overclaimed. This
    test removes the recorded file's whole directory on a live msdos volume. It
    does not detach the volume: detaching it mid test leaves
    :func:`tests._hardware.fat_volume` no mountpoint to tear down and turns a
    teardown failure into the result. The predicate branch is the same one an
    ejected volume reaches, because both arrive as "the parent is not a
    directory", and it is the branch that decides whether the record is handed
    to something else.

    The cost of the branch is real and is not hidden: a file whose directory
    also vanished is no longer findable by its bytes, so a SECOND record is
    written. That is the trade round 8 chose, one record's original against a
    live file's value, and this test pins it as a decision rather than leaving
    it to be rediscovered as a bug.
    """
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
    # REMOVED BY HAND RATHER THAN BY ``shutil.rmtree``, and that is a FAT fact
    # rather than a preference. rmtree walks with ``dir_fd`` relative unlinks
    # where the platform claims support, and on this msdos volume that walk
    # raises FileNotFoundError for the directory it is standing in. Measured
    # here: the rmtree form failed on the real image while this form succeeds,
    # which is one more reason these proofs are not written against tmp_path.
    for child in sorted(music.iterdir()):
        child.unlink()
    music.rmdir()
    assert not music.exists(), "the whole containing directory has to be gone"

    adopt_revert.write_tag_with_record(
        cfg, backup, field="genre", written="Adopted Genre", entry_id="e2"
    )

    snapshots = adopt_revert.read(cfg).snapshots
    by_path = {Path(record.path): record for record in snapshots}
    assert len(snapshots) == 2, (
        "the byte identical copy was handed the vanished directory's record, "
        "which is the defect: when that directory comes back its file is "
        "adopted afresh with adoption's own value stored as its original"
    )
    assert by_path[path].original == ("Original Genre",), (
        "the original record's own value has to survive untouched"
    )
    assert by_path[backup].original == ("Adopted Genre",), (
        "the copy carries what was actually on it when it was adopted"
    )
