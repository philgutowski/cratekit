"""U24: the deletion pass, the proof that gates it, and the watermark that scopes it.

Most assertions are "no file moved, and here is the category that says why": the
failure of a deletion pass is taking something it should not have. Every fixture
is synthetic or a disposable copy built from the binding's schema in a temporary
directory. Layers: the watermark (arithmetic, no library), the Trash (real files,
real renames), the candidate rules (real inodes and sizes), and the pass (a fake
binding for the branches, a real disposable database for "nothing in it changes").
"""

from __future__ import annotations

import ast
import errno
import hashlib
import inspect
import io
import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.core import config, locations, preflight, rb_writer, review, session, tombstone
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.deletion import candidates, library, run, stores, trash, watermark
from cratekit.write import trees
from tests import _mounts
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "cratekit" / "deletion"

# ── synthesized names (D1). Nothing here names a real volume or a real track ──

ONE = "First Track.flac"
TWO = "Second Track (Someone Remix).flac"
ACCENTED = "Café Track.flac"
ARTIST = "A Synthesized Artist"


# Fixtures


@pytest.fixture
def library_root(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library_root):
    """Configuration with the application pin RECORDED, since an unset one refuses."""
    return config.from_dict(
        valid_data(
            library_root,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "pin_validated_on": "2026-08-02",
            },
        )
    )


@pytest.fixture
def gates_pass(cfg, monkeypatch):
    """The volume identity agrees, the acknowledgment is recorded, rekordbox is shut."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: cfg.library.volume_id
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


def _music(cfg, name: str, *, body: bytes = b"audio bytes") -> Path:
    path = Path(cfg.library.root) / "Music" / name
    path.write_bytes(body)
    return path


def _home(tmp_path) -> Path:
    """A home directory holding an empty macOS Trash, for ``run.apply(home=...)``."""
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    return home


def _row(cfg, name: str, content_id: str, *, deleted: bool = False):
    return trees.ContentRow(
        content_id=content_id,
        recorded=str(Path(cfg.library.root) / "Music" / name),
        deleted=deleted,
    )


def _removed(cfg, name: str, content_id: str, *, sequence: int = 10, size: int | None = 11):
    return library.RemovedRow(
        content_id=content_id,
        recorded=str(Path(cfg.library.root) / "Music" / name),
        sequence=sequence,
        size=size,
        artist=ARTIST,
        title=Path(name).stem,
    )


class FakeRow:
    """One mapped collection row, with only the columns the reader touches."""

    def __init__(self, **columns):
        for key, value in columns.items():
            setattr(self, key, value)


class FakeQuery:
    """The binding hands back a query, not a list, and the guarded canary uses it."""

    def __init__(self, rows):
        self._rows = list(rows)

    def __iter__(self):
        return iter(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def count(self):
        return len(self._rows)


class SpentQuery:
    """A query whose rows can be WALKED once, which is what a raw cursor is."""

    def __init__(self, rows):
        self._rows = list(rows)
        self._declared = len(self._rows)
        self._walked = False

    def __iter__(self):
        if self._walked:
            return iter(())
        self._walked = True
        return iter(self._rows)

    def count(self):
        return self._declared


class MuteQuery:
    """A query that cannot say how many rows it holds. Neither ``len`` nor ``count``."""

    def __init__(self, rows):
        self._rows = list(rows)

    def __iter__(self):
        return iter(self._rows)


class FakeDb:
    """A binding that answers the five questions the pass asks and nothing else."""

    def __init__(
        self,
        rows=(),
        memberships=(),
        *,
        usn=100,
        identity="db-identity-1",
        memberships_walk_once=False,
        memberships_cannot_count=False,
    ):
        self.rows = list(rows)
        self.memberships = list(memberships)
        self.usn = usn
        self.identity = identity
        self.memberships_cannot_count = memberships_cannot_count
        self._spent = SpentQuery(self.memberships) if memberships_walk_once else None

    def get_content(self):
        return FakeQuery(self.rows)

    def get_playlist_songs(self):
        if self._spent is not None:
            return self._spent
        if self.memberships_cannot_count:
            return MuteQuery(self.memberships)
        return FakeQuery(self.memberships)

    def get_local_usn(self):
        return self.usn

    def get_property(self):
        return FakeQuery([FakeRow(DBID=self.identity)])


def _membership(content_id, *, deleted=False):
    """One playlist membership row, with only the two columns the reader touches."""
    return FakeRow(ID=f"m{content_id}", ContentID=content_id, rb_local_deleted=1 if deleted else 0)


def _at(folder, content_id, *, deleted=False, usn=None, size=11, title=None, isrc=None):
    """A collection row recorded at ``folder``, titled by its stem unless told otherwise."""
    return FakeRow(
        ID=content_id,
        FolderPath=folder,
        FileSize=size,
        rb_local_deleted=1 if deleted else 0,
        rb_local_usn=usn,
        Title=title if title is not None else Path(folder).stem,
        ArtistName=ARTIST,
        ISRC=isrc,
    )


def _content(cfg, name, content_id, *, deleted=False, usn=None, size=11, title=None, isrc=None):
    folder = str(Path(cfg.library.root) / "Music" / name)
    return _at(folder, content_id, deleted=deleted, usn=usn, size=size, title=title, isrc=isrc)


# Part 1: the watermark


def test_a_first_run_baselines_and_a_second_run_does_not(cfg):
    store = watermark.WatermarkStore(cfg)
    assert store.read() is None
    first, baselined = store.baseline(database_identity="db-1", sequence=40, actor="cli")
    assert baselined and first.sequence == 40
    second, again = store.baseline(database_identity="db-1", sequence=90, actor="cli")
    assert not again, "a second baseline would move the position nobody asked to move"
    assert second.sequence == 40


def test_a_rebuilt_library_forces_a_re_baseline_rather_than_silence(cfg):
    """The number is a position in ONE database's sequence space."""
    store = watermark.WatermarkStore(cfg)
    store.baseline(database_identity="db-1", sequence=900, actor="cli")
    fresh, baselined = store.baseline(database_identity="db-2", sequence=3, actor="cli")
    assert baselined
    assert fresh.sequence == 3 and fresh.database_identity == "db-2"


def test_the_watermark_never_moves_backwards(cfg):
    store = watermark.WatermarkStore(cfg)
    store.baseline(database_identity="db-1", sequence=40, actor="cli")
    store.advance(database_identity="db-1", sequence=60, actor="cli")
    held = store.advance(database_identity="db-1", sequence=50, actor="cli")
    assert held.sequence == 60


def test_advancing_against_a_different_database_refuses(cfg):
    store = watermark.WatermarkStore(cfg)
    store.baseline(database_identity="db-1", sequence=40, actor="cli")
    with pytest.raises(CratekitError) as excinfo:
        store.advance(database_identity="db-2", sequence=41, actor="cli")
    assert excinfo.value.cause.reason == "deletion-watermark-unusable"


@pytest.mark.parametrize(
    "document",
    [
        "[]",
        '"a string"',
        "null",
        '{"version": 99, "database_identity": "db-1", "sequence": 4}',
        '{"version": 1, "sequence": 4}',
        '{"version": 1, "database_identity": "db-1", "sequence": "4"}',
        '{"version": 1, "database_identity": "db-1", "sequence": true}',
        "not json at all",
    ],
)
def test_a_document_that_is_not_this_document_refuses_rather_than_reading_as_unset(cfg, document):
    """The defect the decision stores shipped, in the file beside them."""
    store = watermark.WatermarkStore(cfg)
    config.atomic_write_bytes(document.encode(), store.path)
    with pytest.raises(CratekitError) as excinfo:
        store.read()
    assert excinfo.value.cause.reason == "deletion-watermark-unusable"


def test_a_correct_document_round_trips(cfg):
    store = watermark.WatermarkStore(cfg)
    store.baseline(database_identity="db-1", sequence=7, actor="cli")
    assert store.read().sequence == 7


def test_the_lock_lives_outside_the_coupled_set_it_guards(cfg):
    """A lock beside the document has its inode swapped by a restore."""
    assert config.state_file("deletion_watermark").snapshot is config.SnapshotRole.COUPLED
    assert (
        config.state_file("deletion_watermark_lock").snapshot is config.SnapshotRole.NEVER_RESTORED
    )
    store = watermark.WatermarkStore(cfg)
    assert config.library_coupled_dir(cfg) not in store.lock_path.parents


def test_two_real_processes_advancing_at_once_lose_nothing(cfg, tmp_path):
    """PROCESSES, not threads. The lock is advisory and per file descriptor."""
    import subprocess

    config.save(cfg)
    script = tmp_path / "advance.py"
    script.write_text(
        "import sys\nfrom cratekit.core import config\nfrom cratekit.deletion import "
        "watermark\ncfg = config.load()\nstore = watermark.WatermarkStore(cfg)\nfor _ in "
        "range(20):\n    with store._locked():\n        held = store.read()\n        "
        "store._write(\n            watermark.Watermark(\n                "
        "database_identity='db-1',\n                sequence=held.sequence + 1,\n                "
        "recorded=held.recorded,\n                actor='child',\n            )\n        )\n"
    )
    watermark.WatermarkStore(cfg).baseline(database_identity="db-1", sequence=0, actor="cli")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    children = [subprocess.Popen([sys.executable, str(script)], env=env) for _ in range(2)]
    for child in children:
        assert child.wait(timeout=60) == 0
    assert watermark.WatermarkStore(cfg).read().sequence == 40


@pytest.mark.parametrize(
    "pairs, floor, expected",
    [
        ([], 5, 5),
        ([(6, True), (7, True)], 5, 7),
        ([(6, False), (7, True)], 5, 5),
        ([(6, True), (7, False), (8, True)], 5, 6),
        # TWO ROWS ON ONE SEQUENCE, one handled and one not.
        ([(6, True), (6, False), (7, True)], 5, 5),
        # THE FLOOR IS A FLOOR, and nothing drove it.
        ([(5, True), (7, True)], 100, 100),
    ],
)
def test_the_watermark_stops_before_the_first_sequence_holding_anything_unhandled(
    pairs, floor, expected
):
    assert watermark.contiguous_sequence(pairs, floor=floor) == expected


# Part 2: the Trash


def test_a_confirmed_file_lands_in_the_trash_and_is_recoverable(tmp_path):
    home = _home(tmp_path)
    source = tmp_path / "track.flac"
    source.write_bytes(b"audio")
    layout = trash.assert_usable(source, home=home, platform="darwin")
    target = trash.move_to_trash(source, layout=layout)
    assert not source.exists()
    assert target.read_bytes() == b"audio"
    assert trash.recover(target, source) == source
    assert source.read_bytes() == b"audio"


def test_a_second_file_of_the_same_name_never_replaces_the_first(tmp_path):
    """POSIX rename REPLACES. Two tracks of one name trashed a week apart is the
    real shape, and the second one landing on the first is data loss performed by
    the recovery mechanism itself."""
    home = _home(tmp_path)
    for body in (b"first", b"second"):
        source = tmp_path / "track.flac"
        source.write_bytes(body)
        layout = trash.assert_usable(source, home=home, platform="darwin")
        trash.move_to_trash(source, layout=layout)
    held = sorted(p.read_bytes() for p in (home / ".Trash").iterdir())
    assert held == [b"first", b"second"]


def test_a_volume_with_no_usable_trash_refuses_rather_than_deleting(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    source = tmp_path / "track.flac"
    source.write_bytes(b"audio")

    def refuse_to_create(path):
        raise OSError("read-only file system")

    monkeypatch.setattr(config, "mkdir_private", refuse_to_create)
    with pytest.raises(CratekitError) as excinfo:
        trash.assert_usable(source, home=home, platform="darwin")
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert source.exists(), "the file must still be there after a refusal"


def test_the_xdg_layout_is_the_specification_shape_and_the_macos_one_is_not(tmp_path):
    """Both platform branches, driven from one machine."""
    home = tmp_path / "home"
    home.mkdir()
    target = home / "Music" / "track.flac"
    macos = trash.layout_for(target, home=home, uid=501, platform="darwin")
    assert macos.files == home / ".Trash"
    assert macos.info is None
    xdg = trash.layout_for(target, home=home, uid=501, platform="linux")
    assert xdg.files.name == "files" and xdg.info is not None
    assert xdg.info.name == "info"


def test_a_trash_on_another_filesystem_is_refused_before_a_byte_moves(tmp_path):
    """A cross-device move is a copy and an unlink wearing a rename's name."""
    home = _home(tmp_path)
    source = tmp_path / "track.flac"
    source.write_bytes(b"audio")

    class Elsewhere:
        def __init__(self, device):
            self.st_dev = device

    devices = {str(home / ".Trash"): 1}

    def two_filesystems(path):
        return Elsewhere(devices.get(str(path), 2))

    with pytest.raises(CratekitError) as excinfo:
        trash.assert_usable(source, home=home, platform="darwin", stat=two_filesystems)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.code is ExitCode.PRECONDITION
    assert "different filesystem" in excinfo.value.cause.message
    assert source.exists(), "the file must still be there after a refusal"


# Part 3: the proof


def _references(cfg, rows, **kwargs):
    return candidates.reference_set(rows, root=cfg.library.root, **kwargs)


def _categorize(cfg, removed, references, **kwargs):
    return candidates.categorize(removed, references, root=cfg.library.root, **kwargs)


def test_a_removed_row_whose_file_nothing_else_claims_is_deletable(cfg):
    _music(cfg, ONE)
    references = _references(cfg, [])
    answered = _categorize(cfg, [_removed(cfg, ONE, "1")], references)
    assert answered[0].category is candidates.Category.DELETABLE


def test_a_path_that_will_not_resolve_is_unresolved_and_never_deletable(cfg):
    """AE16, and it is the reason the watermark stops where it does."""
    row = replace(_removed(cfg, ONE, "1"), recorded="/nowhere/this/machine/knows/x.flac")
    answered = _categorize(cfg, [row], _references(cfg, []))
    assert answered[0].category is candidates.Category.UNRESOLVED
    assert not answered[0].handled, "an unresolved row is not finished business"


@pytest.mark.parametrize("variant", ["same", "case", "composition"])
def test_a_file_an_active_row_also_points_at_is_a_collision_in_every_spelling(cfg, variant):
    """The 144-file loss, in three spellings, proved by inode rather than by string."""
    import unicodedata

    original = _music(cfg, ACCENTED)
    spelling = {
        "same": ACCENTED,
        "case": ACCENTED.upper(),
        "composition": unicodedata.normalize("NFD", ACCENTED),
    }[variant]
    variant_path = Path(cfg.library.root) / "Music" / spelling
    active = [_row(cfg, spelling, "9")]
    answered = _categorize(cfg, [_removed(cfg, ACCENTED, "1")], _references(cfg, active))
    # ASSERTED IN BOTH DIRECTIONS RATHER THAN SKIPPED, because which way this
    # goes depends on the filesystem under the test and both answers are correct.
    folds = variant_path.exists() and variant_path.stat().st_ino == original.stat().st_ino
    if folds:
        assert answered[0].category is candidates.Category.COLLIDES_WITH_ACTIVE_ROW
        assert answered[0].collides_with == ("9",)
    else:
        assert answered[0].category is candidates.Category.DELETABLE


def test_a_hard_link_from_an_active_row_is_a_collision(cfg):
    """One inode, two names. No string comparison can see this at all."""
    original = _music(cfg, ONE)
    linked = Path(cfg.library.root) / "Music" / "Another Name.flac"
    os.link(original, linked)
    references = _references(cfg, [_row(cfg, "Another Name.flac", "9")])
    answered = _categorize(cfg, [_removed(cfg, ONE, "1")], references)
    assert answered[0].category is candidates.Category.COLLIDES_WITH_ACTIVE_ROW


def test_a_file_of_a_different_size_is_never_deletable(cfg):
    """A path later reclaimed by a different track through name truncation."""
    _music(cfg, ONE, body=b"a completely different recording")
    answered = _categorize(cfg, [_removed(cfg, ONE, "1", size=11)], _references(cfg, []))
    assert answered[0].category is candidates.Category.SIZE_MISMATCH


def test_a_row_that_recorded_no_size_can_never_be_proved(cfg):
    _music(cfg, ONE)
    answered = _categorize(cfg, [_removed(cfg, ONE, "1", size=None)], _references(cfg, []))
    assert answered[0].category is candidates.Category.SIZE_MISMATCH


def test_a_file_a_playlist_still_references_is_not_trashed(cfg):
    _music(cfg, ONE)
    answered = _categorize(
        cfg, [_removed(cfg, ONE, "1")], _references(cfg, []), referenced=frozenset({"1"})
    )
    assert answered[0].category is candidates.Category.STILL_REFERENCED


def test_a_file_already_gone_is_finished_business_rather_than_unresolved(cfg):
    """The resume case. A run interrupted after trashing some files must not
    re-offer them, and must not report them as a configuration failure either."""
    answered = _categorize(cfg, [_removed(cfg, ONE, "1")], _references(cfg, []))
    assert answered[0].category is candidates.Category.GONE
    assert answered[0].handled


def test_a_declined_file_is_absent_from_the_next_run_and_returns_when_revoked(cfg):
    _music(cfg, ONE)
    row = _removed(cfg, ONE, "1")
    record = stores.record_decline(cfg, row, actor="cli")
    declined = _categorize(cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg))
    assert declined[0].category is candidates.Category.DECLINED
    stores.revoke_decline(cfg, record.suppression_id, actor="cli")
    offered = _categorize(cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg))
    assert offered[0].category is candidates.Category.DELETABLE


def test_a_row_with_no_artist_and_no_title_is_never_deletable(cfg):
    """R36 makes the tombstone part of the deletion rather than a consequence."""
    _music(cfg, ONE)
    row = replace(_removed(cfg, ONE, "1"), artist="", title="")
    answered = _categorize(cfg, [row], _references(cfg, []), identifiable=stores.identifiable)
    assert answered[0].category is candidates.Category.UNIDENTIFIABLE


def test_an_unresolvable_active_row_makes_the_whole_run_refuse(cfg):
    """Absence of evidence is not evidence. The proof is over EVERY active row."""
    active = [trees.ContentRow(content_id="9", recorded="/nowhere/known/x.flac", deleted=False)]
    references = _references(cfg, active)
    assert not references.complete
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    assert excinfo.value.cause.reason == "deletion-reference-set-incomplete"


def test_an_active_row_that_will_not_stat_makes_the_run_refuse(cfg):
    _music(cfg, ONE)

    def blind(path):
        raise PermissionError("no")

    references = _references(cfg, [_row(cfg, ONE, "9")], stat=blind)
    assert references.uninspectable == ("9",)
    with pytest.raises(CratekitError):
        candidates.assert_complete(references)


def test_an_active_row_whose_file_is_simply_missing_does_not_block_the_run(cfg):
    """The deliberate reading, recorded in the module and asserted here."""
    references = _references(cfg, [_row(cfg, "Never Existed.flac", "9")])
    assert references.complete and references.missing == ("9",)
    candidates.assert_complete(references)


#: A prefix no machine has, so every row recorded under it needs a rule to reach
#: a path at all. Synthesized rather than named after a real volume (D1, R1).
RECORDED_ELSEWHERE = "/recorded/on/another/machine"


def _elsewhere(count: int = 50):
    """``count`` active rows recorded under a prefix only a rule can resolve."""
    return [
        trees.ContentRow(
            content_id=f"e{index}",
            recorded=f"{RECORDED_ELSEWHERE}/Music/Track {index}.flac",
            deleted=False,
        )
        for index in range(count)
    ]


def _identified(cfg, target: str) -> locations.PrefixRule:
    """A rule onto a directory outside the library root, WITH its volume recorded."""
    return locations.PrefixRule(RECORDED_ELSEWHERE, target, cfg.library.volume_id)


def _populate(volume: Path, rows) -> None:
    for row in rows:
        target = Path(str(volume) + row.recorded[len(RECORDED_ELSEWHERE) :])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"audio bytes")


def test_a_prefix_rule_whose_target_is_not_there_refuses_rather_than_proving_nothing(cfg, tmp_path):
    """One wrong character in a prefix rule used to delete the completeness proof."""
    volume = tmp_path / "other-volume"
    _populate(volume, _elsewhere())
    correct = _references(
        cfg, _elsewhere(), prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))]
    )
    assert len(correct.by_identity) == 50 and correct.complete
    assert correct.missing == () and correct.unanchored == ()
    no_rule = _references(cfg, _elsewhere())
    assert len(no_rule.unmapped) == 50 and not no_rule.complete
    typo = tmp_path / "other-volumme"
    wrong = _references(
        cfg, _elsewhere(), prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(typo))]
    )
    assert wrong.by_identity == {}
    assert wrong.missing == (), (
        "a rule pointing at a directory that is not there is not fifty separate "
        "statements about fifty separate files"
    )
    assert len(wrong.unanchored) == 50
    assert wrong.dead_anchors == (str(typo),)
    assert not wrong.complete
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(wrong)
    assert excinfo.value.cause.reason == "deletion-reference-set-incomplete"
    assert excinfo.value.cause.detail["unanchored"] == 50
    assert excinfo.value.cause.detail["dead_anchors"] == [str(typo)]
    assert str(typo) in excinfo.value.cause.message


def test_a_mapped_volume_that_is_not_plugged_in_refuses(cfg, tmp_path):
    """The author's claim that this already refused was false, and it is reachable."""
    unmounted = tmp_path / "not-mounted-today"
    references = _references(
        cfg, _elsewhere(3), prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(unmounted))]
    )
    assert len(references.unanchored) == 3 and not references.complete


def test_a_dangling_symlink_is_still_one_missing_file_and_still_does_not_refuse(cfg):
    """The deliberate reading survives, because its own case is genuinely per row."""
    link = Path(cfg.library.root) / "Music" / "Dangling.flac"
    link.symlink_to(Path(cfg.library.root) / "Music" / "Never Existed.flac")
    references = _references(cfg, [_row(cfg, "Dangling.flac", "9")])
    assert references.missing == ("9",) and references.unanchored == ()
    assert references.complete
    candidates.assert_complete(references)


def test_a_folder_the_user_deleted_under_the_root_is_still_served(cfg):
    """The false positive the ANCHOR choice exists to avoid."""
    rows = [
        trees.ContentRow(
            content_id=str(index),
            recorded=str(Path(cfg.library.root) / "Music" / "An Album" / f"{index}.flac"),
            deleted=False,
        )
        for index in range(5)
    ]
    references = _references(cfg, rows)
    assert len(references.missing) == 5 and references.unanchored == ()
    assert references.complete
    candidates.assert_complete(references)


def test_a_removed_row_under_a_dead_rule_is_unresolved_rather_than_finished(cfg, tmp_path):
    """``GONE`` is handled, so fusing this one is worse than fusing the other one."""
    row = replace(_removed(cfg, ONE, "1"), recorded=f"{RECORDED_ELSEWHERE}/Music/Track 0.flac")
    answered = _categorize(
        cfg,
        [row],
        _references(cfg, []),
        prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(tmp_path / "gone"))],
    )
    assert answered[0].category is candidates.Category.UNRESOLVED
    assert not answered[0].handled
    assert str(tmp_path / "gone") in answered[0].problem


def test_a_dead_prefix_rule_stops_the_whole_pass_before_anything_is_offered(
    cfg, gates_pass, tmp_path
):
    """End to end. With the rule fused, this run reported one deletable candidate,
    offered it, trashed the file, and advanced the watermark, while the active row
    that would have collided with it was sitting under a directory nobody checked."""
    _music(cfg, ONE)
    _baseline(cfg)
    elsewhere = _at(f"{RECORDED_ELSEWHERE}/Music/Track 0.flac", "9", usn=45)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50), elsewhere], usn=50)
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, db, actor="cli", prefix_map=[_identified(cfg, str(tmp_path / "gone"))])
    assert excinfo.value.cause.reason == "deletion-reference-set-incomplete"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_nul_byte_in_a_recorded_path_refuses_rather_than_escaping_as_a_defect(cfg):
    """``os.stat`` raises ValueError for this, not OSError, so both handlers missed
    it and it reached the command line as an internal defect rather than as a
    refusal carrying its remedy (S4)."""
    poisoned = trees.ContentRow(
        content_id="9",
        recorded=str(Path(cfg.library.root) / "Music" / "Bad\x00Name.flac"),
        deleted=False,
    )
    references = _references(cfg, [poisoned])
    assert references.uninspectable == ("9",) and not references.complete
    row = replace(_removed(cfg, ONE, "1"), recorded=poisoned.recorded)
    answered = _categorize(cfg, [row], _references(cfg, []))
    assert answered[0].category is candidates.Category.UNRESOLVED
    assert not answered[0].handled


def test_a_streamed_row_is_neither_indexed_nor_counted_against_the_proof(cfg):
    streamed = trees.ContentRow(content_id="9", recorded="tidal:track:123", deleted=False)
    references = _references(cfg, [streamed])
    assert references.complete and not references.by_identity and not references.unmapped
    assert references.not_a_path == ("9",), (
        "excused from the proof is not the same as invisible; a set of rows the proof does not "
        "cover is a claim, and a claim nobody can size is one nobody can check"
    )


def test_a_tombstoned_row_never_contributes_to_the_reference_set(cfg):
    """The active-row rule, inherited rather than re-implemented."""
    _music(cfg, ONE)
    references = _references(cfg, [_row(cfg, ONE, "1", deleted=True)])
    assert not references.by_identity


def test_a_recorded_prefix_the_map_covers_resolves_on_both_sides(cfg, library_root):
    """Most active rows in a real library record a volume that stopped existing."""
    older = "/an/older/mount"
    rules = [locations.PrefixRule(older, str(library_root))]
    _music(cfg, ONE)
    active = [trees.ContentRow(content_id="9", recorded=f"{older}/Music/{ONE}", deleted=False)]
    references = _references(cfg, active, prefix_map=rules)
    row = replace(_removed(cfg, ONE, "1"), recorded=f"{older}/Music/{ONE}")
    answered = _categorize(cfg, [row], references, prefix_map=rules)
    assert answered[0].category is candidates.Category.COLLIDES_WITH_ACTIVE_ROW


# Part 4: the pass


def test_a_first_run_presents_nothing_and_records_where_it_started(cfg, gates_pass):
    _music(cfg, ONE)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=7)], usn=40)
    found = run.plan(cfg, db, actor="cli")
    assert found.baselined and found.candidates == ()
    assert found.baselined_over == 1
    assert watermark.WatermarkStore(cfg).read().sequence == 40


def test_a_track_removed_after_the_baseline_is_offered_and_one_before_it_is_not(cfg, gates_pass):
    _music(cfg, ONE)
    _music(cfg, TWO)
    old = _content(cfg, ONE, "1", deleted=True, usn=7)
    db = FakeDb([old], usn=40)
    run.plan(cfg, db, actor="cli")
    fresh = _content(cfg, TWO, "2", deleted=True, usn=50)
    found = run.plan(cfg, FakeDb([old, fresh], usn=50), actor="cli")
    assert [item.row.content_id for item in found.candidates] == ["2"]
    assert found.deletable[0].category is candidates.Category.DELETABLE


def test_the_offered_items_reach_the_review_queue_and_re_offering_is_idempotent(cfg, gates_pass):
    _music(cfg, ONE)
    db = FakeDb([], usn=40)
    run.plan(cfg, db, actor="cli")
    removed = _content(cfg, ONE, "1", deleted=True, usn=50)
    found = run.plan(cfg, FakeDb([removed], usn=50), actor="cli")
    first = run.present(cfg, found, handler_key="delete.review")
    second = run.present(cfg, found, handler_key="delete.review")
    assert [item.item_id for item in first] == [item.item_id for item in second]
    with review.open_store(cfg) as store:
        assert review.count_unresolved(store, queue=review.Queue.DELETION) == 1


def _confirm(cfg, item_id, verdict=review.Verdict.ACCEPTED):
    with review.open_store(cfg) as store:
        review.resolve(store, item_id, verdict, actor="cli")


def _confirm_all(cfg, items, verdict=review.Verdict.ACCEPTED):
    """``_confirm`` for every offered item, through one open of the review store."""
    with review.open_store(cfg) as store:
        for item in items:
            review.resolve(store, item.item_id, verdict, actor="cli")


def _confirm_first(cfg, db, **plan):
    """Plan, offer, and confirm the first offered item, as a person would; returns the plan."""
    found = run.plan(cfg, db, actor="cli", **plan)
    _confirm(cfg, run.present(cfg, found)[0].item_id)
    return found


def _confirmed_one(cfg, tmp_path):
    """A home with a Trash, and a baselined library whose one removal is confirmed."""
    home = _home(tmp_path)
    db = _prepared(cfg)
    _confirm_first(cfg, db)
    return home, db


def _baseline(cfg) -> None:
    """The watermark a first run over ``FakeDb([], usn=40)`` leaves, written directly."""
    watermark.WatermarkStore(cfg).baseline(
        database_identity="db-identity-1", sequence=40, actor="cli"
    )


def _prepared(cfg, *, names=(ONE,), usn=50):
    """A library that has been baselined, with ``names`` removed after that."""
    for name in names:
        _music(cfg, name)
    _baseline(cfg)
    rows = [
        _content(cfg, name, str(index + 1), deleted=True, usn=usn + index)
        for index, name in enumerate(names)
    ]
    return FakeDb(rows, usn=usn + len(names))


def test_a_confirmed_file_is_trashed_and_leaves_a_tombstone(cfg, gates_pass, tmp_path):
    home, db = _confirmed_one(cfg, tmp_path)
    report = run.apply(cfg, db, actor="cli", home=home)
    assert len(report.trashed) == 1
    assert not (Path(cfg.library.root) / "Music" / ONE).exists()
    assert Path(report.trashed[0].target).read_bytes() == b"audio bytes"
    assert stores.suppressed_version(cfg, artist=ARTIST, title=Path(ONE).stem)
    assert report.watermark.sequence == 50


def test_a_rejected_item_becomes_a_decline_and_the_file_stays(cfg, gates_pass, tmp_path):
    home = _home(tmp_path)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id, review.Verdict.REJECTED)
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == () and len(report.declined) == 1
    assert (Path(cfg.library.root) / "Music" / ONE).exists()
    assert len(stores.declines(cfg).suppressions()) == 1
    # THE WATERMARK MAY NOT PASS OVER IT, and the previous version of this test
    # asserted 50 here with a comment blessing the advance.
    assert report.watermark.sequence == 40


def test_revoking_a_decline_puts_the_file_back_in_front_of_a_person(cfg, gates_pass, tmp_path):
    """R35's revocability clause, driven through the path the product takes."""
    home = _home(tmp_path)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id, review.Verdict.REJECTED)
    run.apply(cfg, db, actor="cli", home=home)
    held = stores.declines(cfg).suppressions()
    assert len(held) == 1
    run.revoke(cfg, held[0].suppression_id, actor="cli")
    assert stores.declines(cfg).suppressions() == ()
    again = run.plan(cfg, db, actor="cli")
    assert [item.category for item in again.candidates] == [candidates.Category.DELETABLE]
    reoffered = run.present(cfg, again)
    assert len(reoffered) == 1
    assert reoffered[0].verdict is None, (
        "the review item still carried the rejection, so the next apply would "
        "record the decline again and the revocation would change nothing"
    )
    # And the file moves once the person answers the re-offered question, which
    # is the whole point of the clause.
    _confirm(cfg, reoffered[0].item_id)
    report = run.apply(cfg, db, actor="cli", home=home)
    assert len(report.trashed) == 1
    assert not (Path(cfg.library.root) / "Music" / ONE).exists()
    assert report.watermark.sequence == 50


def test_a_declined_row_holds_the_watermark_and_lets_it_go_when_revoked(cfg, gates_pass):
    """The cost of revocability, asserted rather than assumed."""
    _music(cfg, ONE)
    row = _removed(cfg, ONE, "1", sequence=50)
    record = stores.record_decline(cfg, row, actor="cli")
    answered = _categorize(cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg))
    assert answered[0].category is candidates.Category.DECLINED
    assert not answered[0].handled, "a revocable decision is not finished business"
    assert watermark.contiguous_sequence([(50, answered[0].handled)], floor=40) == 40
    stores.revoke_decline(cfg, record.suppression_id, actor="cli")
    lifted = _categorize(cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg))
    assert lifted[0].category is candidates.Category.DELETABLE


def test_an_item_nobody_has_answered_holds_the_watermark_where_it_is(cfg, gates_pass, tmp_path):
    home = _home(tmp_path)
    db = _prepared(cfg, names=(ONE, TWO))
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    # The SECOND one is confirmed and the first is left open, so the watermark
    # may not pass the first even though everything above it is finished.
    _confirm(cfg, offered[1].item_id)
    report = run.apply(cfg, db, actor="cli", home=home)
    assert len(report.trashed) == 1
    assert report.watermark.sequence == 40, (
        "the watermark advanced past a removal nobody has answered for"
    )


def test_a_confirmed_item_invalidated_before_the_move_is_refused_at_move_time(
    cfg, gates_pass, tmp_path
):
    """R37's last sentence. A review item is durable and a library is not."""
    home, db = _confirmed_one(cfg, tmp_path)
    db.rows.append(_content(cfg, ONE, "99", deleted=False, usn=60))
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == ()
    assert [item.category for item in report.refused] == [
        candidates.Category.COLLIDES_WITH_ACTIVE_ROW
    ]
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_run_interrupted_after_trashing_resumes_without_re_offering(cfg, gates_pass, tmp_path):
    home, db = _confirmed_one(cfg, tmp_path)
    run.apply(cfg, db, actor="cli", home=home)
    # The crash: the watermark is put back to where it was before the apply, so
    # the next run sees the removal again exactly as an interrupted one would.
    marks = watermark.WatermarkStore(cfg)
    with marks._locked():
        marks._write(replace(marks.read(), sequence=40))
    again = run.plan(cfg, db, actor="cli")
    assert [item.category for item in again.candidates] == [candidates.Category.GONE]
    assert again.deletable == ()
    assert len(stores.list_tombstones(cfg)) == 1


def test_only_deletable_candidates_are_ever_offered(cfg, gates_pass):
    """Nobody can answer "this file is also an active row's file" with a decision."""
    _music(cfg, ONE, body=b"a different length entirely")
    _baseline(cfg)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50, size=11)], usn=50)
    found = run.plan(cfg, db, actor="cli")
    assert found.candidates[0].category is candidates.Category.SIZE_MISMATCH
    assert run.present(cfg, found) == ()
    with review.open_store(cfg) as store:
        assert review.count_unresolved(store, queue=review.Queue.DELETION) == 0


def test_an_unreadable_tombstone_store_refuses_before_the_first_file_moves(
    cfg, gates_pass, tmp_path
):
    """R36 makes the tombstone part of the deletion, so it has to be writable first."""
    home, db = _confirmed_one(cfg, tmp_path)
    config.atomic_write_bytes(b"[]\n", config.state_path(tombstone.STORE_KEY, cfg))
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    assert excinfo.value.cause.reason == "review-file-unusable"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_move_that_fails_refuses_with_a_cause_rather_than_a_bare_error(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """An unstructured exception reaches the command line as an internal defect."""
    home, db = _confirmed_one(cfg, tmp_path)

    def refuse_to_move(path, *, layout):
        raise OSError("read-only file system")

    monkeypatch.setattr(trash, "move_to_trash", refuse_to_move)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.code is ExitCode.PRECONDITION
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_the_pass_refuses_while_rekordbox_is_open(cfg, gates_pass, monkeypatch):
    """Without it every identity assertion is evaluated against a stale view."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, FakeDb([]), actor="cli")
    assert excinfo.value.cause.code is ExitCode.REKORDBOX_OPEN


def test_the_pass_refuses_while_the_background_agent_is_running(cfg, gates_pass, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, FakeDb([]), actor="cli")
    assert excinfo.value.cause.code is ExitCode.REKORDBOX_OPEN


def test_a_decoy_volume_at_the_configured_path_refuses_before_anything_resolves(
    cfg, gates_pass, monkeypatch, tmp_path
):
    """R38. A restored clone mounted where the real library belongs is internally
    consistent all the way down to trashing the backup the recovery depends on."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: "SOME-OTHER-ID"
    )
    _music(cfg, ONE)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=50)
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, db, actor="cli")
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert watermark.WatermarkStore(cfg).read() is None, (
        "the refusal happened after something had already been written"
    )


def test_a_row_that_cannot_report_the_soft_delete_marker_refuses(cfg):
    blind = FakeRow(ID="9", FolderPath="/x.flac")
    with pytest.raises(CratekitError) as excinfo:
        library.read_collection([blind])
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


@pytest.mark.parametrize("value", [None, True, False, "not a number"], ids=str)
def test_a_removed_row_with_no_usable_update_sequence_refuses(cfg, value):
    """A BOOLEAN is refused beside a missing value, and that is not fussiness."""
    blind = FakeRow(ID="9", FolderPath="/x.flac", rb_local_deleted=1, rb_local_usn=value)
    with pytest.raises(CratekitError) as excinfo:
        library.read_collection([blind])
    assert excinfo.value.cause.reason == "removal-sequence-unreadable"


@pytest.mark.parametrize("identity", ["", None], ids=["empty", "absent"])
def test_a_database_that_names_no_identity_of_its_own_refuses(cfg, identity):
    """An unbound watermark is the state where a rebuild reports nothing forever."""
    with pytest.raises(CratekitError) as excinfo:
        library.database_identity(FakeDb([], identity=identity))
    assert excinfo.value.cause.reason == "canary-read-failed"
    assert excinfo.value.cause.detail["column"] == "DBID"


def test_a_database_that_cannot_report_its_update_counter_refuses(cfg):
    """The baseline's own input. Read as zero it re-offers a whole library's history."""

    class Mute(FakeDb):
        def get_local_usn(self):
            raise RuntimeError("the counter could not be read")

    with pytest.raises(CratekitError) as excinfo:
        library.current_sequence(Mute([]))
    assert excinfo.value.cause.reason == "canary-read-failed"
    assert excinfo.value.cause.detail["column"] == "localUpdateCount"


def test_the_apply_refuses_without_the_backup_acknowledgment(cfg, monkeypatch, tmp_path):
    """KTD24 binds the gates to DESTRUCTION, not to database writes."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: cfg.library.volume_id
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    _music(cfg, ONE)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=50)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=tmp_path)
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


# Part 5: against a real disposable database


def _fingerprint(path: Path) -> dict[str, str]:
    """Every byte of the database and its sidecars, hashed."""
    found: dict[str, str] = {}
    for candidate in sorted(path.parent.iterdir()):
        if candidate.is_file():
            found[candidate.name] = hashlib.sha256(candidate.read_bytes()).hexdigest()
    return found


@pytest.fixture
def real_db(cfg, monkeypatch):
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        yield handle
    finally:
        rb_writer.close_db(handle)


def _write_rows(db_path: Path, rows) -> None:
    """Set the collection rows' columns BEFORE the pass ever opens the database."""
    conn = sqlite3.connect(db_path)
    try:
        for content_id, path, deleted, usn, size, title in rows:
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = ?, "
                "rb_local_usn = ?, FileSize = ?, Title = ? WHERE ID = ?",
                (path, 1 if deleted else 0, usn, size, title, content_id),
            )
        conn.commit()
    finally:
        conn.close()


def test_a_whole_run_against_a_real_database_changes_not_one_byte_of_it(
    cfg, gates_pass, real_db, tmp_path
):
    """The verification the brief asks for, in the form a suite can carry."""
    home = _home(tmp_path)
    music = _music(cfg, ONE)
    db_path = Path(cfg.library.db_path)
    _write_rows(
        db_path,
        [
            ("1", str(music), True, 50, music.stat().st_size, Path(ONE).stem),
            ("2", str(Path(cfg.library.root) / "Music" / TWO), False, 20, 11, Path(TWO).stem),
        ],
    )
    _music(cfg, TWO)
    rb_writer.close_db(real_db)
    handle = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        watermark.WatermarkStore(cfg).baseline(
            database_identity=library.database_identity(handle), sequence=40, actor="cli"
        )
        found = run.plan(cfg, handle, actor="cli")
        assert [item.row.content_id for item in found.deletable] == ["1"]
        offered = run.present(cfg, found)
        _confirm(cfg, offered[0].item_id)
        before = _fingerprint(db_path)
        report = run.apply(cfg, handle, actor="cli", home=home)
        after = _fingerprint(db_path)
    finally:
        rb_writer.close_db(handle)
    assert len(report.trashed) == 1
    assert before == after, "the deletion pass changed the database"
    assert not music.exists() and Path(report.trashed[0].target).exists()


def test_the_real_binding_answers_every_column_the_reader_asks_for(cfg, real_db):
    """The adapter joint. The fake above proves the branches; this proves the reads."""
    db_path = Path(cfg.library.db_path)
    music = _music(cfg, ONE)
    rb_writer.close_db(real_db)
    _write_rows(db_path, [("1", str(music), True, 51, 99, Path(ONE).stem)])
    handle = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        seen = library.read_collection(handle.get_content())
        assert library.database_identity(handle) == "1"
        assert library.current_sequence(handle) == 100
    finally:
        rb_writer.close_db(handle)
    assert [row.content_id for row in seen.removed] == ["1"]
    assert seen.removed[0].sequence == 51 and seen.removed[0].size == 99


# Part 6: what a green suite cannot see


#: Every module name that would let this package speak to a streaming service.
_NETWORK_MODULES = frozenset(
    {
        "requests",
        "urllib",
        "urllib3",
        "http",
        "socket",
        "tidalapi",
        "ftplib",
        "smtplib",
        "cratekit.acquire",
    }
)


def _imported_modules(source: str) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
            found |= {f"{node.module}.{alias.name}" for alias in node.names}
    return found


def _reaches_the_network(source: str) -> list[str]:
    """Every import in one module that could reach a service. Prefix-matched."""
    offenders: list[str] = []
    for imported in _imported_modules(source):
        head = imported.split(".")
        for depth in range(1, len(head) + 1):
            if ".".join(head[:depth]) in _NETWORK_MODULES:
                offenders.append(imported)
                break
    return offenders


def test_the_network_guard_bites_and_stays_quiet_on_correct_code():
    """P7, both halves, before the guard is pointed at anything real."""
    assert _reaches_the_network("import requests\n")
    assert _reaches_the_network("from urllib.request import urlopen\n")
    assert _reaches_the_network("import tidalapi\n")
    assert _reaches_the_network("from cratekit.acquire import adapter\n")
    assert not _reaches_the_network("from cratekit.core import review\n")
    assert not _reaches_the_network("import os\nimport hashlib\n")


def test_no_module_in_the_deletion_package_can_reach_a_streaming_service():
    """R36. A deletion is a fact about this disk and about nothing else."""
    reached = {
        path.name: _reaches_the_network(path.read_text()) for path in PACKAGE_ROOT.rglob("*.py")
    }
    offenders = {name: found for name, found in sorted(reached.items()) if found}
    assert not offenders, f"the deletion package can reach a service: {offenders}"


def test_the_preview_and_the_write_run_the_same_categoriser():
    """A destructive verb whose dry run and real run take different code paths."""
    source = (PACKAGE_ROOT / "candidates.py").read_text()
    tree = ast.parse(source)
    recheck = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "recheck"
    )
    calls = {
        node.func.id
        for node in ast.walk(recheck)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "categorize" in calls, (
        "recheck no longer goes through the categoriser, so the review and the "
        "move are two opinions about one library"
    )


def test_every_category_is_classified_as_handled_or_not(cfg):
    """A category added later must not join whichever side an ``if`` left it on."""
    for category in candidates.Category:
        item = candidates.Candidate(row=_removed(cfg, ONE, "1"), category=category)
        assert item.handled is (category in candidates.HANDLED)
    assert candidates.Category.DELETABLE not in candidates.HANDLED, (
        "a deletable candidate is finished business only once its file has moved"
    )


def test_the_module_and_the_state_inventory_agree_about_which_stores_exist():
    """One symbol, one meaning. The store keys are spelled once, below both."""
    assert tombstone.STORE_KEY in review.DECISION_STORE_KEYS
    assert tombstone.DECLINE_STORE_KEY in review.DECISION_STORE_KEYS


# Part 5: the one verb this unit could land


def _drive(argv):
    """Run the real dispatcher, the way the conformance suite drives every verb."""
    from cratekit import cli

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


@pytest.fixture
def deletion_enabled(cfg, library_root):
    """The same library, saved to disk under a profile that switches deletion on."""
    on_disk = config.from_dict(
        valid_data(
            library_root,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "pin_validated_on": "2026-08-02",
            },
            profile={"name": "full"},
        )
    )
    config.save(on_disk)
    config.reset_cache()
    return on_disk


def test_tombstone_list_shows_what_the_deletion_pass_suppressed(
    cfg, gates_pass, deletion_enabled, tmp_path
):
    home, db = _confirmed_one(cfg, tmp_path)
    run.apply(cfg, db, actor="cli", home=home)
    code, out, err = _drive(["--output", "json", "tombstone", "list"])
    assert code == int(ExitCode.OK), err or out
    payload = json.loads(out)["data"]
    assert [item["title"] for item in payload["items"]] == [Path(ONE).stem]
    assert payload["items"][0]["revoked"] is False
    assert payload["unresolved"] == 0, (
        "a settled suppression is not a backlog; unresolved is what the deletion "
        "queue still has open"
    )


def test_tombstone_list_revokes_and_then_shows_the_lifted_record(
    cfg, gates_pass, deletion_enabled, tmp_path
):
    """The revocable half, which no surface offered before this verb existed."""
    home, db = _confirmed_one(cfg, tmp_path)
    report = run.apply(cfg, db, actor="cli", home=home)
    held = report.trashed[0].suppression_id
    assert stores.suppressed_version(cfg, artist=ARTIST, title=Path(ONE).stem)
    code, out, err = _drive(["--output", "json", "tombstone", "list", "--revoke", held])
    assert code == int(ExitCode.OK), err or out
    payload = json.loads(out)["data"]
    assert [item["revoked"] for item in payload["items"]] == [True]
    assert not stores.suppressed_version(cfg, artist=ARTIST, title=Path(ONE).stem)
    # And it is gone from the default listing afterwards, which is the other half
    # of the same rule: the ordinary question is "what is suppressed".
    _code, plain, _err = _drive(["--output", "json", "tombstone", "list"])
    assert json.loads(plain)["data"]["items"] == []


def test_tombstone_list_refuses_an_identifier_that_resolves_in_neither_store(cfg, deletion_enabled):
    code, out, _err = _drive(["--output", "json", "tombstone", "list", "--revoke", "dc_nope"])
    assert code != int(ExitCode.OK)
    assert json.loads(out)["cause"]["reason"] == "review-item-unknown"


# Part 6: findings the review accepted, fixed and held


def test_a_verdict_does_not_travel_to_whatever_the_row_resolves_to_later(cfg, gates_pass, tmp_path):
    """A person was shown one path, accepted, and a DIFFERENT file was moved."""
    first = tmp_path / "volume-one"
    second = tmp_path / "volume-two"
    for volume in (first, second):
        (volume / "Music").mkdir(parents=True)
        (volume / "Music" / ONE).write_bytes(b"audio bytes")
    to_first = [_identified(cfg, str(first))]
    to_second = [_identified(cfg, str(second))]
    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=to_first)
    removed = _at(f"{RECORDED_ELSEWHERE}/Music/{ONE}", "1", deleted=True, usn=50)
    db = FakeDb([removed], usn=50)
    found = run.plan(cfg, db, actor="cli", prefix_map=to_first)
    offered = run.present(cfg, found)
    assert offered[0].payload["path"] == str(first / "Music" / ONE)
    _confirm(cfg, offered[0].item_id)
    home = _home(tmp_path)
    report = run.apply(cfg, db, actor="cli", home=home, prefix_map=to_second)
    assert report.trashed == ()
    assert [item.row.content_id for item in report.refused] == ["1"]
    assert (second / "Music" / ONE).exists(), "a file the person never saw was moved"
    assert (first / "Music" / ONE).exists()
    assert report.watermark.sequence == 40


def test_a_name_the_filesystem_will_not_take_refuses_for_that_one_file(tmp_path):
    """Errno 63 is a fact about one name, and it used to condemn the whole run."""
    directory = tmp_path / "trash"
    directory.mkdir()
    name = "n" * 250 + ".flac"
    (directory / name).write_bytes(b"")
    with pytest.raises(CratekitError) as excinfo:
        trash._free_name(directory, name)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.scope is Scope.ITEM


def test_a_disk_that_will_not_take_any_name_still_stops_the_run(tmp_path, monkeypatch):
    """The other side of the same split, asserted so the narrowing did not go too far."""
    directory = tmp_path / "trash"
    directory.mkdir()

    def full(*args, **kwargs):
        raise OSError(errno.ENOSPC, "no space left on device")

    monkeypatch.setattr(os, "open", full)
    with pytest.raises(OSError) as excinfo:
        trash._free_name(directory, ONE)
    assert excinfo.value.errno == errno.ENOSPC


def test_one_impossible_name_costs_one_file_rather_than_the_whole_pass(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """Correct on safety, wrong on granularity, and this is the granularity."""
    home = _home(tmp_path)
    db = _prepared(cfg, names=(ONE, TWO))
    found = run.plan(cfg, db, actor="cli")
    _confirm_all(cfg, run.present(cfg, found))
    real = trash.move_to_trash

    def refuse_one(path, *, layout):
        if Path(path).name == ONE:
            raise refuse(
                "trash-unavailable",
                "this one name has nowhere to land",
                remedy=Remedy.RUN_DOCTOR,
                scope=Scope.ITEM,
                origin=("deletion.trash",),
                detail={},
            )
        return real(path, layout=layout)

    monkeypatch.setattr(trash, "move_to_trash", refuse_one)
    report = run.apply(cfg, db, actor="cli", home=home)
    assert [Path(item.candidate.resolved).name for item in report.trashed] == [TWO]
    assert (Path(cfg.library.root) / "Music" / ONE).exists()
    assert len(report.refused) == 1
    assert report.watermark.sequence == 40, (
        "the watermark passed a removal that was confirmed and never moved"
    )


def test_a_name_that_is_all_suffix_is_numbered_without_a_leading_space(tmp_path):
    """``.flac`` used to collide onto " 2.flac", with a leading space and the
    original name nowhere in it."""
    directory = tmp_path / "trash"
    directory.mkdir()
    (directory / ".flac").write_bytes(b"")
    claimed = trash._free_name(directory, ".flac")
    assert claimed.name == ".flac 2"


# Part 7: what the second review round found


def test_the_reference_set_it_built_is_reported_on_every_run(cfg, gates_pass, caplog):
    """The module docstring sells this as the answer, so it is asserted like one."""
    _music(cfg, ONE)
    _baseline(cfg)
    db = FakeDb(
        [
            _content(cfg, ONE, "1", deleted=False, usn=44),
            _content(cfg, "Never Existed.flac", "2", deleted=False, usn=45),
        ],
        usn=50,
    )
    with caplog.at_level(logging.INFO, logger="cratekit.deletion.run"):
        run.plan(cfg, db, actor="cli")
    said = [
        record.getMessage() for record in caplog.records if "reference set" in record.getMessage()
    ]
    assert said, "the pass no longer reports the reference set it built"
    assert "'indexed': 1" in said[0] and "'missing': 1" in said[0]


def test_an_anchor_that_answered_nothing_is_named_in_a_warning(cfg, gates_pass, tmp_path, caplog):
    """The all-or-nothing version of this was silenced by ONE unrelated good row."""
    wrong = tmp_path / "real-but-not-the-one"
    wrong.mkdir()
    _music(cfg, ONE)
    _baseline(cfg)
    elsewhere = _at(f"{RECORDED_ELSEWHERE}/Music/Track 0.flac", "9", usn=45)
    db = FakeDb([_content(cfg, ONE, "1", deleted=False, usn=44), elsewhere], usn=50)
    with caplog.at_level(logging.WARNING, logger="cratekit.deletion.run"):
        found = run.plan(cfg, db, actor="cli", prefix_map=[_identified(cfg, str(wrong))])
    assert found.references.by_identity, (
        "this library indexes a row, which is what silenced the previous warning"
    )
    warned = [record.getMessage() for record in caplog.records if record.levelno >= logging.WARNING]
    assert warned, "an anchor that proved nothing went unmentioned"
    assert str(wrong) in warned[0]


def test_a_prefix_target_that_exists_but_is_wrong_is_flagged_and_does_not_refuse(cfg, tmp_path):
    """THE HOLE THE ANCHOR SPLIT DOES NOT CLOSE, pinned so it cannot widen quietly."""
    wrong = tmp_path / "real-but-not-the-one"
    wrong.mkdir()
    _music(cfg, ONE)
    references = _references(
        cfg,
        [_row(cfg, ONE, "root-1"), *_elsewhere(1)],
        prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(wrong))],
    )
    assert len(references.by_identity) == 1
    assert references.missing == ("e0",)
    assert references.unanchored == ()
    assert references.suspect_anchors == (str(wrong),)
    assert references.complete, (
        "recorded as open in the residual finding "
        "Five findings the U24 review accepted, and the reason each stands",
        "not asserted as safe",
    )


def test_an_anchor_with_one_missing_row_and_one_good_row_is_not_suspect(cfg):
    """The other side of the same rule, so the signal is not simply "any missing"."""
    _music(cfg, ONE)
    references = _references(cfg, [_row(cfg, ONE, "1"), _row(cfg, "Never Existed.flac", "2")])
    assert references.missing == ("2",)
    assert references.suspect_anchors == ()


def test_a_volume_that_goes_away_mid_walk_refuses_rather_than_shrinking_the_proof(cfg, tmp_path):
    """The cache has a direction and the unsafe one used to win silently."""
    volume = tmp_path / "ejected-halfway"
    volume.mkdir()
    real = os.stat
    asked = {"count": 0}

    def ejects_after_the_first_look(path):
        if path == str(volume):
            asked["count"] += 1
            if asked["count"] > 1:
                raise FileNotFoundError(path)
        return real(path)

    references = _references(
        cfg,
        _elsewhere(3),
        prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))],
        stat=ejects_after_the_first_look,
    )
    assert references.missing == ("e0", "e1", "e2"), "the shape the old cache produced"
    assert references.unstable_anchors == (str(volume),)
    assert not references.complete
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    assert excinfo.value.cause.reason == "deletion-reference-set-incomplete"
    assert "two different filesystems" in excinfo.value.cause.message
    assert excinfo.value.cause.detail["unstable_anchors"] == [str(volume)]


def test_a_rule_onto_the_filesystem_root_names_an_anchor_a_person_can_read(cfg):
    """``PrefixRule`` right strips its target, so a rule onto "/" stores ""."""
    rule = locations.PrefixRule(RECORDED_ELSEWHERE, "/")
    assert rule.target == ""
    references = _references(
        cfg,
        [
            trees.ContentRow(
                content_id="9", recorded=f"{RECORDED_ELSEWHERE}/no/such/file.flac", deleted=False
            )
        ],
        prefix_map=[rule],
    )
    assert references.unanchored == () and references.dead_anchors == ()
    assert references.missing == ("9",)


def test_the_library_root_anchor_is_folded_the_way_a_rule_target_is(cfg):
    """One directory, two composition forms, and this project's own worst incident."""
    # Spelled with explicit escapes, because the two forms are the same
    # glyphs on screen and an editor that normalizes on save would quietly
    # turn this test into a comparison of one string with itself.
    composed = "/library/Caf\u00e9"
    decomposed = "/library/Cafe\u0301"
    under_root = locations.ResolvedPath(
        locations.Resolution.UNDER_ROOT, path=f"{decomposed}/Music/x.flac"
    )
    rule = locations.PrefixRule(RECORDED_ELSEWHERE, composed)
    remapped = locations.ResolvedPath(
        locations.Resolution.REMAPPED, path=f"{composed}/Music/x.flac", rule_index=0
    )
    assert candidates._anchor_of(
        under_root, root=decomposed, prefix_map=[rule]
    ) == candidates._anchor_of(remapped, root=decomposed, prefix_map=[rule])


def test_revoking_a_decline_whose_review_item_is_gone_still_lifts_it(cfg, gates_pass):
    """A revoke that finds nothing to reopen has SUCCEEDED."""
    _music(cfg, ONE)
    record = stores.record_decline(cfg, _removed(cfg, ONE, "1"), actor="cli")
    assert len(stores.declines(cfg).suppressions()) == 1
    lifted = run.revoke(cfg, record.suppression_id, actor="cli")
    assert lifted.revoked
    assert stores.declines(cfg).suppressions() == ()


def test_a_revoke_that_cannot_reopen_the_item_leaves_the_decline_standing(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The queue is written FIRST, and this is why the order is the design."""
    home = _home(tmp_path)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id, review.Verdict.REJECTED)
    run.apply(cfg, db, actor="cli", home=home)
    held = stores.declines(cfg).suppressions()[0]
    real = review.clear
    broken = {"on": True}

    def unreadable(store, item_id, *, actor):
        if broken["on"]:
            raise refuse(
                "review-file-unusable",
                "the queue could not be written",
                scope=Scope.RUN,
                origin=("review",),
                detail={},
            )
        return real(store, item_id, actor=actor)

    # Patched by flag rather than undone, because ``monkeypatch.undo`` would also
    # revert the volume identity and process probes the gates fixture installed.
    monkeypatch.setattr(run.review, "clear", unreadable)
    with pytest.raises(CratekitError) as excinfo:
        run.revoke(cfg, held.suppression_id, actor="cli")
    assert excinfo.value.cause.reason == "review-file-unusable"
    assert len(stores.declines(cfg).suppressions()) == 1, (
        "the decline was lifted while the rejection that re-creates it was still "
        "armed, which is the one half-done state that must not be reachable"
    )
    broken["on"] = False
    again = run.plan(cfg, db, actor="cli")
    assert [item.category for item in again.candidates] == [candidates.Category.DECLINED]
    # And retrying completes it, which is what makes the pair recoverable rather
    # than merely ordered.
    run.revoke(cfg, held.suppression_id, actor="cli")
    reopened = run.plan(cfg, db, actor="cli")
    assert [item.category for item in reopened.candidates] == [candidates.Category.DELETABLE]
    assert run.present(cfg, reopened)[0].verdict is None


def test_a_trash_directory_that_is_the_problem_is_not_blamed_on_one_name(tmp_path, monkeypatch):
    """ENAMETOOLONG and EINVAL can be facts about the DESTINATION, not the name."""
    absent = tmp_path / "no-such-trash"

    def too_long(*args, **kwargs):
        raise OSError(errno.ENAMETOOLONG, "file name too long")

    monkeypatch.setattr(os, "open", too_long)
    with pytest.raises(OSError) as excinfo:
        trash._free_name(absent, ONE)
    assert excinfo.value.errno == errno.ENAMETOOLONG, (
        "a fact about the Trash was converted into an item scoped skip about a track"
    )


# Part 8: the round-three findings


def test_a_refusal_naming_a_dead_anchor_says_which_directory_to_mount(cfg, tmp_path):
    """Open 5's remediation in the residual finding
    "Five findings the U24 review accepted, and the reason each stands",
    which nothing asserted.
    """
    typo = tmp_path / "not-mounted"
    references = _references(
        cfg, _elsewhere(3), prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(typo))]
    )
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    steps = excinfo.value.cause.remediation.steps
    assert steps, (
        "the refusal carries no step at all, so a person whose archive drive is "
        "unplugged is told to run doctor and nothing else"
    )
    assert str(typo) in steps[0], "the step does not name the directory to mount"
    assert "mount" in steps[0] and "prefix rule" in steps[0], (
        "the step names neither of the two acts that clear this, which are "
        "mounting the volume and correcting the rule that points at it"
    )
    # AND IT REACHES A PERSON.
    from cratekit.cli import render

    assert any(str(typo) in line for line in render.render_cause(excinfo.value.cause))


def test_a_refusal_with_no_dead_anchor_offers_no_directory_to_mount(cfg):
    """The other branch, which is what stops the step being unconditional."""
    active = [trees.ContentRow(content_id="9", recorded="/nowhere/known/x.flac", deleted=False)]
    references = _references(cfg, active)
    assert references.dead_anchors == ()
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    steps = excinfo.value.cause.remediation.steps
    assert not any("mount the volume" in step for step in steps), (
        "a refusal with no dead anchor offered a step naming an empty list of "
        "directories, which reads as an instruction and names nothing"
    )
    # U243: the one step it does offer is the rule for the prefix it names.
    assert len(steps) == 1 and 'from = "/nowhere/known"' in steps[0]
    assert excinfo.value.cause.remediation.remedy is Remedy.RUN_DOCTOR


# ── F3: the version-bearing column, and the identity that was not unique ──────


def _remixed(cfg, name, content_id, *, title, version, sequence=10):
    return replace(_removed(cfg, name, content_id, sequence=sequence), title=title, version=version)


def test_two_remixes_filed_under_one_title_are_two_tombstones(cfg):
    """The identity collision, in the shape a remix-heavy library actually holds."""
    original = _remixed(cfg, ONE, "1", title="Strobe", version="")
    remix = _remixed(cfg, ONE, "2", title="Strobe", version="Michael Woods Remix")
    assert stores.version_of(original) != stores.version_of(remix), (
        "two different versions of one recording produced one identity, so "
        "deleting either suppresses both"
    )
    stores.record_tombstone(cfg, remix, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Strobe"), (
        "deleting the remix suppressed the original, which is music the user "
        "still wants and will never be offered again"
    )


def test_a_mix_name_already_in_the_title_is_not_written_twice(cfg):
    """The legitimate case the composition must not break."""
    split = _remixed(cfg, ONE, "1", title="Strobe", version="Michael Woods Remix")
    inline = _remixed(
        cfg, ONE, "2", title="Strobe (Michael Woods Remix)", version="Michael Woods Remix"
    )
    assert stores.version_of(split) == stores.version_of(inline)
    assert stores.version_of(inline)["title"] == "strobe (michael woods remix)"


def test_a_row_with_no_mix_name_keeps_the_identity_it_always_had(cfg):
    """Most rows. The composition may not move the ordinary case one character."""
    plain = _remixed(cfg, ONE, "1", title="Strobe", version="")
    assert stores.version_of(plain) == tombstone.version_identity(artist=ARTIST, title="Strobe")


def test_the_reader_takes_the_mix_name_from_either_column(cfg):
    """``RemixerName`` first, ``Subtitle`` second, and never both joined."""
    remixer = _content(cfg, ONE, "1", deleted=True, usn=50, title="Strobe")
    remixer.RemixerName = "Michael Woods Remix"
    remixer.Subtitle = "Ignored"
    subtitle = _content(cfg, TWO, "2", deleted=True, usn=51, title="Strobe")
    subtitle.RemixerName = ""
    subtitle.Subtitle = "Extended Mix"
    seen = library.read_collection(FakeQuery([remixer, subtitle]))
    assert [row.version for row in seen.removed] == ["Michael Woods Remix", "Extended Mix"]
    assert stores.version_of(seen.removed[0])["title"] == "strobe (michael woods remix)"


def test_a_row_from_a_binding_with_no_version_column_still_answers(cfg):
    """``_text`` defaults, so a binding without the column is "" rather than a raise."""
    bare = _at(
        str(Path(cfg.library.root) / "Music" / ONE), "1", deleted=True, usn=50, title="Strobe"
    )
    seen = library.read_collection(FakeQuery([bare]))
    assert seen.removed[0].version == ""
    assert stores.version_of(seen.removed[0])["title"] == "strobe"


def test_the_real_binding_answers_the_version_columns_too(cfg, real_db):
    """The adapter joint for the two columns F3 added, against the real schema."""
    db_path = Path(cfg.library.db_path)
    music = _music(cfg, ONE)
    second = _music(cfg, TWO)
    rb_writer.close_db(real_db)
    _write_rows(
        db_path,
        [("1", str(music), True, 51, 99, "Strobe"), ("2", str(second), True, 52, 99, "Strobe")],
    )
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO djmdArtist (ID, Name) VALUES (?, ?)", ("77", "Michael Woods Remix")
        )
        conn.execute("UPDATE djmdContent SET RemixerID = ? WHERE ID = ?", ("77", "1"))
        conn.execute("UPDATE djmdContent SET Subtitle = ? WHERE ID = ?", ("Extended Mix", "2"))
        conn.commit()
    finally:
        conn.close()
    handle = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        seen = library.read_collection(handle.get_content())
    finally:
        rb_writer.close_db(handle)
    versions = {row.content_id: row.version for row in seen.removed}
    assert versions == {"1": "Michael Woods Remix", "2": "Extended Mix"}, (
        "the reader asked for a name the real binding does not answer, so every "
        "identity silently collapses back onto artist and bare title"
    )
    by_id = {row.content_id: row for row in seen.removed}
    assert stores.version_of(by_id["1"])["title"] == "strobe (michael woods remix)"
    assert stores.version_of(by_id["1"]) != stores.version_of(by_id["2"])


# ── F4: one reason that meant two things ─────────────────────────────────────


def test_a_decline_whose_review_item_cannot_be_addressed_refuses(cfg, gates_pass):
    """The derivation fault, told apart from the queue legitimately not holding it."""
    _music(cfg, ONE)
    row = _removed(cfg, ONE, "1")
    # Written straight into the declines store under a kind this queue never
    # uses, which is what a derivation drift looks like from the store's side.
    drifted = stores.declines(cfg).record(
        kind="some-other-kind",
        identity=stores.row_identity(row),
        payload={"artist": row.artist, "title": row.title},
        actor="cli",
    )
    with pytest.raises(CratekitError) as excinfo:
        run.revoke(cfg, drifted.suppression_id, actor="cli")
    assert excinfo.value.cause.reason == "internal-error"
    assert excinfo.value.cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert stores.declines(cfg).suppressions()[0].suppression_id == drifted.suppression_id, (
        "the decline was lifted anyway, so the half-done state the queue-first "
        "order exists to avoid was reached through the derivation instead"
    )
    # The other half of the derivation: the right kind, an identity this queue
    # could never have addressed.
    bad_identity = stores.declines(cfg).record(
        kind=run.REVIEW_KIND, identity={"content_id": "1"}, payload={}, actor="cli"
    )
    with pytest.raises(CratekitError) as second:
        run.revoke(cfg, bad_identity.suppression_id, actor="cli")
    assert second.value.cause.reason == "internal-error"


def test_a_decline_the_queue_simply_does_not_hold_is_still_addressable(cfg, gates_pass):
    """The legitimate case, which the check above must not refuse."""
    _music(cfg, ONE)
    record = stores.record_decline(cfg, _removed(cfg, ONE, "1"), actor="cli")
    run._assert_addressable(stores.declines(cfg).suppressions()[0])
    lifted = run.revoke(cfg, record.suppression_id, actor="cli")
    assert lifted.revoked and stores.declines(cfg).suppressions() == ()


# ── F5: the assertion the re-check dropped ───────────────────────────────────


def _decline_between_the_plan_and_the_move(cfg, monkeypatch, row):
    """Record a decline in the window apply's re-check is supposed to cover."""
    real = run.library.playlist_referenced
    calls = {"count": 0}

    def after_the_plan(memberships):
        calls["count"] += 1
        if calls["count"] == 2:
            stores.record_decline(cfg, row, actor="somebody-else")
        return real(memberships)

    monkeypatch.setattr(run.library, "playlist_referenced", after_the_plan)
    return calls


def test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """``recheck`` re-runs EVERY assertion, and this is the one it was missing."""
    home, db = _confirmed_one(cfg, tmp_path)
    calls = _decline_between_the_plan_and_the_move(cfg, monkeypatch, _removed(cfg, ONE, "1"))
    report = run.apply(cfg, db, actor="cli", home=home)
    assert calls["count"] >= 2, (
        "the decline was never recorded in the window this test is about, so a "
        "pass here would say nothing about the re-check"
    )
    assert report.trashed == (), "a file somebody declined mid-run was trashed anyway"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()
    assert [item.category for item in report.refused] == [candidates.Category.DECLINED]
    assert report.plan.candidates[0].category is candidates.Category.DELETABLE, (
        "the plan already saw the decline, so this drove the plan's predicate "
        "rather than the re-check's and proves nothing about the missing argument"
    )


def test_a_row_nobody_declined_is_still_trashed(cfg, gates_pass, tmp_path):
    """The legitimate case, pinned beside the guard above."""
    home, db = _confirmed_one(cfg, tmp_path)
    report = run.apply(cfg, db, actor="cli", home=home)
    assert len(report.trashed) == 1 and report.refused == ()
    assert not (Path(cfg.library.root) / "Music" / ONE).exists()


# ── F6: a trashed file with no tombstone ─────────────────────────────────────


def _tombstone_store_that_will_not_write(monkeypatch, *, raising=None):
    """Break ``record_tombstone`` behind a FLAG rather than by patching and undoing."""
    real = run.stores.record_tombstone
    broken = {"on": True}

    def unwritable(cfg, row, *, actor, trashed_to=None):
        if not broken["on"]:
            return real(cfg, row, actor=actor, trashed_to=trashed_to)
        if raising is not None:
            raise raising()
        raise refuse(
            "review-file-unusable",
            "the suppression store could not be written",
            scope=Scope.RUN,
            origin=("review",),
            detail={},
        )

    monkeypatch.setattr(run.stores, "record_tombstone", unwritable)
    return broken


def test_a_tombstone_that_cannot_be_written_puts_the_file_back(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """R36's worst reachable state, driven and then closed."""
    home, db = _confirmed_one(cfg, tmp_path)
    broken = _tombstone_store_that_will_not_write(monkeypatch)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    assert excinfo.value.cause.reason == "review-file-unusable", (
        "the store's own refusal was replaced, so the remedy that says what is "
        "wrong with the store was discarded"
    )
    original = Path(cfg.library.root) / "Music" / ONE
    assert original.exists(), (
        "the file is in the Trash with no tombstone, which is the state R36 says "
        "cannot exist and which no later run can even notice"
    )
    assert original.read_bytes() == b"audio bytes"
    assert stores.list_tombstones(cfg, include_revoked=True) == ()
    assert list((home / ".Trash").iterdir()) == []
    # AND THE NEXT RUN STILL SEES IT. This is the half that matters: the row must
    # not answer GONE, because GONE retires it and the deletion never happened.
    broken["on"] = False
    again = run.plan(cfg, db, actor="cli")
    assert [item.category for item in again.candidates] == [candidates.Category.DELETABLE]
    finished = run.apply(cfg, db, actor="cli", home=home)
    assert len(finished.trashed) == 1, (
        "the deletion the store failure interrupted could not be completed by "
        "re-running, which is the whole reason the move is undone rather than left"
    )
    assert len(stores.list_tombstones(cfg)) == 1


def test_a_file_that_cannot_be_put_back_refuses_naming_both_paths(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """When the undo fails too, the person is told where their file is."""
    home, db = _confirmed_one(cfg, tmp_path)
    _tombstone_store_that_will_not_write(monkeypatch)

    def no_way_back(target, original):
        raise OSError("the volume went read only")

    monkeypatch.setattr(run.trash, "recover", no_way_back)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    cause = excinfo.value.cause
    assert cause.reason == "internal-error"
    assert str(Path(cfg.library.root) / "Music" / ONE) in cause.message
    assert cause.detail["trashed_to"]
    assert cause.remediation.steps and "by hand" in cause.remediation.steps[0]
    assert cause.inner is not None and cause.inner.reason == "review-file-unusable", (
        "the store failure that started this was dropped, so why the tombstone "
        "could not be written is nowhere in the record"
    )


# ── F7: the bound nothing pinned ─────────────────────────────────────────────


def test_the_name_search_gives_up_at_a_bound_a_person_will_wait_for(tmp_path, monkeypatch):
    """``MAX_NAME_ATTEMPTS`` raised to 10**9 left the suite green."""
    # THE VALUE, NOT A CEILING OVER IT.
    assert trash.MAX_NAME_ATTEMPTS == 1000, (
        "the bound is no longer the bound a person will wait behind, and the only "
        "way to pin a constant is to assert the constant"
    )
    directory = tmp_path / "trash"
    directory.mkdir()
    tries = {"count": 0}

    def always_taken(*args, **kwargs):
        tries["count"] += 1
        raise FileExistsError()

    monkeypatch.setattr(os, "open", always_taken)
    with pytest.raises(CratekitError) as excinfo:
        trash._free_name(directory, ONE)
    assert excinfo.value.cause.scope is Scope.ITEM, (
        "running out of numbers is one file's problem, not the volume's"
    )
    # NOT THE PIN, AND IT IS WORTH SAYING SO OUT LOUD.
    assert tries["count"] == trash.MAX_NAME_ATTEMPTS, (
        "the loop did not stop at the declared bound, so the constant names one "
        "number and the code spends another"
    )


# ── F9: a row excused from the proof that should never have been ─────────────


@pytest.mark.parametrize(
    "recorded",
    [
        "C:\\Music\\Track.flac",
        "D:/Music/Track.flac",
        "file://localhost/Volumes/Music/Caf%C3%A9%20Track.flac",
        "FILE://localhost/Volumes/Music/Track.flac",
    ],
    ids=["windows-backslash", "windows-slash", "percent-encoded-location", "upper-case-scheme"],
)
def test_a_row_that_is_a_path_this_build_cannot_name_refuses(cfg, recorded):
    """The worst shape this unit has, closed from inside U24's own consumer."""
    active = [trees.ContentRow(content_id="9", recorded=recorded, deleted=False)]
    references = _references(cfg, active)
    assert references.unnameable == ("9",)
    assert references.not_a_path == (), (
        "a row naming a real file was excused with the streamed rows, and the "
        "argument for excusing those is that they reference no file"
    )
    assert not references.complete
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    assert excinfo.value.cause.reason == "deletion-reference-set-incomplete"
    assert excinfo.value.cause.detail["unnameable_rows"] == ["9"]
    assert excinfo.value.cause.detail["unnameable"] == 1, (
        "the tally the refusal reports is not the tally it refused on, so a person reading the "
        "detail is told a different number from the one that stopped the run"
    )
    assert excinfo.value.cause.remediation.steps


def test_a_genuinely_streamed_library_still_runs(cfg):
    """The case the excusal exists for, which the refusal above must not break."""
    _music(cfg, ONE)
    active = [
        trees.ContentRow(content_id="9", recorded="tidal:track:123", deleted=False),
        trees.ContentRow(content_id="8", recorded="", deleted=False),
    ]
    references = _references(cfg, active)
    assert references.unnameable == ()
    assert sorted(references.not_a_path) == ["8", "9"]
    assert references.complete
    candidates.assert_complete(references)
    answered = _categorize(cfg, [_removed(cfg, ONE, "1")], references)
    assert answered[0].category is candidates.Category.DELETABLE


# Round 4: what the last round over-restricted, and what an identity is

# ── R4-F1: a streamed row spelled as a URL is not a path ─────────────────────


@pytest.mark.parametrize(
    "recorded",
    [
        "tidal://track/123",
        "spotify://track/abc",
        "beatport://12345",
        "https://api.tidal.com/v1/tracks/123",
    ],
    ids=["tidal", "spotify", "beatport", "https"],
)
def test_a_streamed_row_spelled_as_a_url_is_excused_rather_than_stopping_the_run(cfg, recorded):
    """THE REGRESSION THE UNNAMEABLE SPLIT INTRODUCED, in every scheme that hits it."""
    _music(cfg, ONE)
    active = [trees.ContentRow(content_id="9", recorded=recorded, deleted=False)]
    references = _references(cfg, active)
    assert references.unnameable == (), (
        "a row that references no file was called a path this build cannot "
        "name, which refuses the run with a step nothing can satisfy"
    )
    assert references.not_a_path == ("9",)
    assert references.complete
    candidates.assert_complete(references)
    answered = _categorize(cfg, [_removed(cfg, ONE, "1")], references)
    assert answered[0].category is candidates.Category.DELETABLE, (
        "the run refused rather than proceeding, so the verb is off for every "
        "library that has ever streamed anything"
    )


# ── R4-F2: an interrupt is not an Exception ──────────────────────────────────


@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, SystemExit], ids=["ctrl-c", "sigterm"])
def test_an_interrupt_during_the_store_write_still_puts_the_file_back(
    cfg, gates_pass, tmp_path, monkeypatch, interrupt
):
    """The undo caught ``Exception``, and the likeliest failure here is not one."""
    home, db = _confirmed_one(cfg, tmp_path)
    broken = _tombstone_store_that_will_not_write(monkeypatch, raising=interrupt)
    with pytest.raises(interrupt):
        run.apply(cfg, db, actor="cli", home=home)
    original = Path(cfg.library.root) / "Music" / ONE
    assert original.exists(), (
        "an interrupt left the file in the Trash with no tombstone, which is the "
        "one state in this unit that loses an invariant with no trace at all"
    )
    assert original.read_bytes() == b"audio bytes"
    assert stores.list_tombstones(cfg, include_revoked=True) == ()
    assert list((home / ".Trash").iterdir()) == []
    # And the row is still live business, because GONE would have retired it.
    broken["on"] = False
    again = run.plan(cfg, db, actor="cli")
    assert [item.category for item in again.candidates] == [candidates.Category.DELETABLE]
    finished = run.apply(cfg, db, actor="cli", home=home)
    assert len(finished.trashed) == 1
    assert len(stores.list_tombstones(cfg)) == 1


# ── R4-F3: a version contained in a title is not a version carried by it ─────


@pytest.mark.parametrize(
    ("title", "version"),
    [("Lively Up", "Live"), ("Extended Play Track", "Extended")],
    ids=["live-inside-lively", "extended-inside-extended-play"],
)
def test_a_version_that_is_merely_a_substring_of_the_title_still_splits_the_identity(
    cfg, title, version
):
    """The containment short circuit was a PLAIN SUBSTRING TEST on folded text."""
    plain = _remixed(cfg, ONE, "1", title=title, version="")
    carried = _remixed(cfg, TWO, "2", title=title, version=version)
    assert stores.version_of(plain) != stores.version_of(carried), (
        "the two versions share one identity, so deleting either suppresses both"
    )
    stores.record_tombstone(cfg, carried, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=f"{title} ({version})")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title=title), (
        "the version the person kept is suppressed, and it will never be offered to them again"
    )


def test_a_remixer_name_inside_the_titles_own_bracket_is_not_composed_twice(cfg):
    """The legitimate case a bracket-only test would have broken."""
    inline = _remixed(cfg, ONE, "1", title="Strobe (Michael Woods Remix)", version="Michael Woods")
    assert stores.version_of(inline)["title"] == "strobe (michael woods remix)"
    stores.record_tombstone(cfg, inline, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)")


def test_a_square_bracketed_mix_name_keeps_its_brackets_which_is_R_19(cfg):
    """Pinned as the CURRENT behaviour, and it is a residual rather than a fix."""
    bracketed = _remixed(
        cfg, ONE, "1", title="Sun Path [Nightwave Remix]", version="Nightwave Remix"
    )
    assert stores.version_of(bracketed)["title"] == "sun path [nightwave remix]"
    stores.record_tombstone(cfg, bracketed, actor="cli")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Sun Path (Nightwave Remix)")


# ── R4-F4: a Subtitle is not guaranteed to be a mix name ─────────────────────


def _subtitled(cfg, name, content_id, *, title, subtitle, usn=50):
    row = _content(cfg, name, content_id, deleted=True, usn=usn, title=title)
    row.RemixerName = ""
    row.Subtitle = subtitle
    return row


def test_a_subtitle_that_is_not_a_mix_name_leaves_the_identity_the_provider_spells(cfg):
    """rekordbox's ``Subtitle`` is ID3 ``TIT3`` and holds a label as readily as a mix."""
    row = _subtitled(cfg, ONE, "1", title="Atlas", subtitle="Anjunadeep")
    seen = library.read_collection(FakeQuery([row]))
    assert seen.removed[0].version == ""
    assert stores.version_of(seen.removed[0])["title"] == "atlas"
    stores.record_tombstone(cfg, seen.removed[0], actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Atlas"), (
        "the tombstone was written under a title no acquisition source will ever "
        "ask about, so the suppression exists and does nothing"
    )


def test_a_subtitle_that_is_a_mix_name_is_still_composed(cfg):
    """The other direction, which is the collision the Subtitle column exists to close."""
    original = _subtitled(cfg, ONE, "1", title="Strobe", subtitle="")
    extended = _subtitled(cfg, TWO, "2", title="Strobe", subtitle="Extended Mix", usn=51)
    seen = library.read_collection(FakeQuery([original, extended]))
    by_id = {row.content_id: row for row in seen.removed}
    assert by_id["2"].version == "Extended Mix"
    assert stores.version_of(by_id["1"]) != stores.version_of(by_id["2"])
    written = stores.record_tombstone(cfg, by_id["2"], actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Extended Mix)")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Strobe")
    # THE PAYLOAD KEEPS THE COLUMN VALUE, uncomposed and unfolded, and nothing
    # pinned it.
    assert written.payload["version"] == "Extended Mix"


@pytest.mark.parametrize(
    ("subtitle", "believed"),
    [
        ("Extended Mix", True),
        ("Nightwave Remix", True),
        ("Radio Edit", True),
        ("Live at a Venue", True),
        ("Instrumental", True),
        ("Anjunadeep", False),
        ("feat. A Guest", False),
        ("Toolroom Records", False),
        ("ripped from vinyl", False),
        ("Mixmag Records", False),
    ],
)
def test_which_subtitles_read_as_a_version(cfg, subtitle, believed):
    """The vocabulary, in both directions, because a word list nothing drives rots."""
    row = _subtitled(cfg, ONE, "1", title="Atlas", subtitle=subtitle)
    seen = library.read_collection(FakeQuery([row]))
    assert bool(seen.removed[0].version) is believed


def test_a_remixer_name_is_believed_without_reading_as_a_version(cfg):
    """``RemixerName`` is not free text, so the vocabulary must not be applied to it."""
    row = _content(cfg, ONE, "1", deleted=True, usn=50, title="Strobe")
    row.RemixerName = "Michael Woods"
    row.Subtitle = ""
    seen = library.read_collection(FakeQuery([row]))
    assert seen.removed[0].version == "Michael Woods"
    assert seen.removed[0].version_kind == library.VERSION_IS_AN_ARTIST


def test_a_bracketed_group_that_merely_contains_the_version_is_not_a_carry(cfg):
    """The match INSIDE the bracketed group is delimited too, and it has to be."""
    plain = _remixed(cfg, ONE, "1", title="Track (Lively Up Mix)", version="")
    live = _remixed(cfg, TWO, "2", title="Track (Lively Up Mix)", version="Live")
    assert stores.version_of(plain) != stores.version_of(live)
    assert stores.version_of(live)["title"] == "track (lively up mix) (live)"


def test_an_interrupt_while_putting_the_file_back_still_names_both_paths(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The inner handler takes ``BaseException`` too, and that one converts."""
    home, db = _confirmed_one(cfg, tmp_path)
    _tombstone_store_that_will_not_write(monkeypatch)

    def interrupted(target, original):
        raise KeyboardInterrupt()

    monkeypatch.setattr(run.trash, "recover", interrupted)
    # CAUGHT AND RE-RAISED AS AN ASSERTION, because an interrupt that escapes
    # here does not fail this test, it ENDS THE PYTEST SESSION, and a mutation
    # measured against a suite that stopped early has measured nothing.
    with pytest.raises(CratekitError) as excinfo:
        try:
            run.apply(cfg, db, actor="cli", home=home)
        except KeyboardInterrupt as escaped:
            raise AssertionError(
                "the interrupt escaped the undo, so the one state where a person must be told "
                "both paths and a manual step reaches them as a bare traceback"
            ) from escaped
    cause = excinfo.value.cause
    assert cause.reason == "internal-error"
    assert str(Path(cfg.library.root) / "Music" / ONE) in cause.message
    assert cause.detail["trashed_to"]
    assert cause.remediation.steps and "by hand" in cause.remediation.steps[0]


# Part 9: round five, stage one.


# ── S1-A: the membership walk is the only thing protecting a referenced file ──


def test_a_membership_walk_that_comes_back_short_refuses_rather_than_freeing_the_file(
    cfg, gates_pass, tmp_path
):
    """The one input in this pass with no assertion on it, driven end to end."""
    _home(tmp_path)
    _music(cfg, ONE)
    _baseline(cfg)
    rows = [_content(cfg, ONE, "1", deleted=True, usn=50)]
    # The plan's own walk answers, so the candidate is offered and confirmed
    # exactly as it would be.
    db = FakeDb(rows, [_membership("1")], usn=50, memberships_walk_once=True)
    found = run.plan(cfg, db, actor="cli")
    assert [item.category for item in found.candidates] == [candidates.Category.STILL_REFERENCED], (
        "the first walk saw the playlist entry, so the file is spoken for"
    )
    spent = FakeDb(rows, [_membership("1")], usn=50, memberships_walk_once=True)
    for _ in spent.get_playlist_songs():
        pass
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, spent, actor="cli")
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses(cfg, gates_pass):
    """There is no safe default, which is the rule this module already applies twice."""
    _music(cfg, ONE)
    _baseline(cfg)
    db = FakeDb(
        [_content(cfg, ONE, "1", deleted=True, usn=50)],
        [_membership("1")],
        usn=50,
        memberships_cannot_count=True,
    )
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, db, actor="cli")
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"


def test_a_library_whose_playlists_are_all_empty_still_runs(cfg, gates_pass):
    """An HONEST zero is accepted, and only an honest one."""
    _music(cfg, ONE)
    _baseline(cfg)
    found = run.plan(
        cfg, FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=50), actor="cli"
    )
    assert [item.category for item in found.candidates] == [candidates.Category.DELETABLE]


def test_a_playlist_that_claims_the_file_between_the_review_and_the_move_stops_it(
    cfg, gates_pass, tmp_path
):
    """STILL_REFERENCED through ``apply``, which nothing drove before this round."""
    home, db = _confirmed_one(cfg, tmp_path)
    db.memberships.append(_membership("1"))
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == ()
    assert [item.category for item in report.refused] == [candidates.Category.STILL_REFERENCED]
    assert (Path(cfg.library.root) / "Music" / ONE).exists()
    assert report.watermark.sequence == 40


def test_a_membership_rekordbox_removed_is_not_a_reference(cfg):
    """The marker is read on the membership row too, through the shared reader."""
    live = library.playlist_referenced(FakeQuery([_membership("1"), _membership("2")]))
    assert live == frozenset({"1", "2"})
    lifted = library.playlist_referenced(
        FakeQuery([_membership("1"), _membership("2", deleted=True)])
    )
    assert lifted == frozenset({"1"})


# ── S1-B: the anchor cache in categorize is never re-asked ───────────────────


def test_a_volume_that_goes_away_mid_categorization_refuses_rather_than_retiring(cfg, tmp_path):
    """The identical cache as the reference set's, and MORE at stake in this walk."""
    volume = tmp_path / "ejected-halfway"
    volume.mkdir()
    real = os.stat
    asked = {"count": 0}

    def ejects_after_the_first_look(path):
        if path == str(volume):
            asked["count"] += 1
            if asked["count"] > 1:
                raise FileNotFoundError(path)
            return real(path)
        raise FileNotFoundError(path)

    rules = [locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))]
    rows = [
        replace(
            _removed(cfg, ONE, str(index)),
            recorded=f"{RECORDED_ELSEWHERE}/Music/Track {index}.flac",
        )
        for index in range(3)
    ]
    with pytest.raises(CratekitError) as excinfo:
        _categorize(
            cfg, rows, _references(cfg, []), prefix_map=rules, stat=ejects_after_the_first_look
        )
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert excinfo.value.cause.detail["unstable_anchors"] == [str(volume)]


def test_a_volume_that_stays_put_categorizes_every_row(cfg, tmp_path):
    """The half that pins the guard to a MOVING anchor rather than to any anchor."""
    volume = tmp_path / "still-mounted"
    volume.mkdir()
    rules = [locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))]
    row = replace(_removed(cfg, ONE, "1"), recorded=f"{RECORDED_ELSEWHERE}/Music/Track 0.flac")
    answered = _categorize(cfg, [row], _references(cfg, []), prefix_map=rules)
    assert answered[0].category is candidates.Category.GONE


# ── S1-C: a hand-moved file must not retire a confirmed removal ──────────────


def test_a_file_moved_by_hand_after_the_confirmation_is_recorded_rather_than_retired_silently(
    cfg, gates_pass, tmp_path, caplog
):
    """ABSENCE READ AS EVIDENCE OF ABSENCE, costing a confirmed deletion outright."""
    home, db = _confirmed_one(cfg, tmp_path)
    music = Path(cfg.library.root) / "Music" / ONE
    moved = Path(cfg.library.root) / "Music" / "Renamed By Hand.flac"
    music.rename(moved)
    with caplog.at_level(logging.WARNING):
        report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == (), "there was nothing at the recorded path to move"
    assert [item.category for item in report.refused] == [candidates.Category.GONE]
    recorded = stores.list_tombstones(cfg, include_revoked=True)
    assert len(recorded) == 1, (
        "the confirmed removal was settled without the tombstone R36 makes part "
        "of the deletion, so R36 is false for this row with nothing recording it"
    )
    assert recorded[0].payload["trashed_to"] == "", (
        "the record claims this pass moved a file it never touched"
    )
    assert moved.exists(), "the file the person moved was destroyed"
    assert recorded[0].suppression_id in caplog.text, (
        "the person is not told which suppression to revoke if they only moved the file"
    )


def test_a_resumed_deletion_whose_tombstone_was_recorded_is_still_finished_business(
    cfg, gates_pass, tmp_path
):
    """The half the tombstone test may not cost, driven through ``apply``."""
    home, db = _confirmed_one(cfg, tmp_path)
    run.apply(cfg, db, actor="cli", home=home)
    marks = watermark.WatermarkStore(cfg)
    with marks._locked():
        marks._write(replace(marks.read(), sequence=40))
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == ()
    assert [item.category for item in report.refused] == [candidates.Category.GONE]
    assert report.watermark.sequence == 50, (
        "an interrupted run that had already recorded the deletion re-offered it "
        "forever instead of resuming"
    )


# ── S1-D: three zero rows on the destructive path itself ─────────────────────


def test_recover_refuses_to_overwrite_a_path_something_else_now_occupies(tmp_path):
    """The UNDO of a half done deletion, and it was entirely untested."""
    home = _home(tmp_path)
    source = tmp_path / "track.flac"
    source.write_bytes(b"the deleted one")
    layout = trash.assert_usable(source, home=home, platform="darwin")
    target = trash.move_to_trash(source, layout=layout)
    source.write_bytes(b"a different recording the person put back")
    with pytest.raises(CratekitError) as excinfo:
        trash.recover(target, source)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.scope is Scope.ITEM
    assert source.read_bytes() == b"a different recording the person put back"
    assert target.read_bytes() == b"the deleted one", "the trashed copy was consumed"


@pytest.mark.parametrize(
    "raising",
    [OSError("read-only file system"), KeyboardInterrupt()],
    ids=["an-exception", "an-interrupt"],
)
def test_a_move_that_fails_leaves_no_placeholder_wearing_the_track_s_name(
    tmp_path, monkeypatch, raising
):
    """The placeholder cleanup, which round four cited as its own precedent untested."""
    home = _home(tmp_path)
    source = tmp_path / "track.flac"
    source.write_bytes(b"audio")
    layout = trash.assert_usable(source, home=home, platform="darwin")

    def will_not_rename(a, b):
        raise raising

    monkeypatch.setattr(trash.os, "replace", will_not_rename)
    # CAUGHT AND RE-RAISED, because an interrupt that escapes ENDS the pytest
    # session rather than failing one test, and a suite that stopped early has
    # measured nothing.
    with pytest.raises(type(raising)):
        trash.move_to_trash(source, layout=layout)
    assert source.read_bytes() == b"audio"
    assert list((home / ".Trash").iterdir()) == [], (
        "an empty file with a real track's name was left in the Trash"
    )


def test_the_tombstone_store_is_proved_readable_before_any_file_is_touched(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The pre-flight, pinned by what it PREVENTS rather than by the end state."""
    home, db = _confirmed_one(cfg, tmp_path)

    def nothing_may_move(path, *, layout):
        raise AssertionError(
            f"{path} was moved to the Trash before the tombstone store was proved readable, so a "
            "store that refuses every write would leave the file trashed with nothing recording it"
        )

    monkeypatch.setattr(trash, "move_to_trash", nothing_may_move)
    config.atomic_write_bytes(b"[]\n", config.state_path(tombstone.STORE_KEY, cfg))
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    assert excinfo.value.cause.reason == "review-file-unusable"


# ── S1-E: a corrected prefix rule must let the retry through ─────────────────


def test_a_corrected_prefix_rule_lets_the_confirmed_deletion_through_on_the_retry(
    cfg, gates_pass, tmp_path
):
    """The guard is right and it used to have no way out at all."""
    first = tmp_path / "volume-one"
    second = tmp_path / "volume-two"
    for volume in (first, second):
        (volume / "Music").mkdir(parents=True)
        (volume / "Music" / ONE).write_bytes(b"audio bytes")
    to_first = [_identified(cfg, str(first))]
    to_second = [_identified(cfg, str(second))]
    home = _home(tmp_path)
    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=to_first)
    removed = _at(f"{RECORDED_ELSEWHERE}/Music/{ONE}", "1", deleted=True, usn=50)
    db = FakeDb([removed], usn=50)
    _confirm_first(cfg, db, prefix_map=to_first)
    stale = run.apply(cfg, db, actor="cli", home=home, prefix_map=to_second)
    assert stale.trashed == () and stale.watermark.sequence == 40
    assert (first / "Music" / ONE).exists() and (second / "Music" / ONE).exists()
    again = run.plan(cfg, db, actor="cli", prefix_map=to_second)
    reoffered = run.present(cfg, again)
    assert len(reoffered) == 1
    assert reoffered[0].verdict is None, (
        "the item kept the confirmation made about the other file, so every "
        "later apply refuses it again and the deletion can never complete"
    )
    assert reoffered[0].payload["path"] == str(second / "Music" / ONE)
    _confirm(cfg, reoffered[0].item_id)
    report = run.apply(cfg, db, actor="cli", home=home, prefix_map=to_second)
    assert len(report.trashed) == 1
    assert not (second / "Music" / ONE).exists()
    assert (first / "Music" / ONE).exists(), "the file the person first saw was moved"
    assert report.watermark.sequence == 50


# ── S1-F: two more zero rows ─────────────────────────────────────────────────


def test_a_recorded_value_that_merely_mentions_a_file_location_is_not_one(cfg):
    """The scheme test is ANCHORED, and unanchored it refuses a run it must not."""
    for recorded in ("a note about file:// locations", "ripped from D:\\ by somebody"):
        mentions = trees.ContentRow(content_id="9", recorded=recorded, deleted=False)
        references = _references(cfg, [mentions])
        assert references.not_a_path == ("9",), recorded
        assert references.unnameable == () and references.complete, recorded
        candidates.assert_complete(references)
    for content_id, recorded in (
        ("8", "file:///Volumes/Music/Track.flac"),
        ("7", "D:\\Music\\Track.flac"),
    ):
        spelled = trees.ContentRow(content_id=content_id, recorded=recorded, deleted=False)
        assert _references(cfg, [spelled]).unnameable == (content_id,), recorded


def test_a_row_that_recorded_a_zero_size_can_never_be_proved(cfg):
    """R37 proves the file is the file the row NAMED, and zero proves nothing."""
    empty = Path(cfg.library.root) / "Music" / ONE
    empty.write_bytes(b"")
    for recorded in (0, -1):
        row = _content(cfg, ONE, "1", deleted=True, usn=50, size=recorded)
        seen = library.read_collection(FakeQuery([row]))
        assert seen.removed[0].size is None
        answered = _categorize(cfg, [seen.removed[0]], _references(cfg, []))
        assert answered[0].category is candidates.Category.SIZE_MISMATCH


# Part 10: round five, stage two.


# ── S2-D: a tombstone written from RemixerName matched nothing ───────────────


def _remixed_row(cfg, name, content_id, *, title, remixer, usn=50):
    row = _content(cfg, name, content_id, deleted=True, usn=usn, title=title)
    row.RemixerName = remixer
    row.Subtitle = ""
    return library.read_collection(FakeQuery([row])).removed[0]


def test_a_remix_filed_as_a_bare_artist_name_is_spelled_the_way_a_provider_spells_it(cfg):
    """THE DEEPEST FINDING OF THE ROUND, and the code already knew why."""
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="Michael Woods")
    assert stores.version_of(row)["title"] == "strobe (michael woods remix)"
    stores.record_tombstone(cfg, row, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)"), (
        "the tombstone was written under a spelling no provider will ever produce"
    )
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Strobe"), (
        "deleting the remix suppressed the original"
    )


def test_the_two_conventions_one_collection_holds_now_reach_one_identity(cfg):
    """The same collection holds both spellings, and they used to be two identities."""
    split = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="Michael Woods")
    inline = _remixed_row(
        cfg, TWO, "2", title="Strobe (Michael Woods Remix)", remixer="Michael Woods", usn=51
    )
    assert stores.version_of(split) == stores.version_of(inline)
    assert stores.version_of(split)["title"] == "strobe (michael woods remix)"


def test_a_remixer_the_title_already_names_is_not_given_a_second_bracket(cfg):
    """The test is on the BARE name, not on the spelled one, and it has to be."""
    row = _remixed_row(
        cfg, ONE, "1", title="Strobe (Michael Woods Extended Remix)", remixer="Michael Woods"
    )
    assert stores.version_of(row)["title"] == "strobe (michael woods extended remix)"


def test_a_remixer_column_already_holding_a_mix_name_is_not_doubled(cfg):
    """Some importers put a whole mix name in the column, and appending breaks it."""
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="Michael Woods Remix")
    assert stores.version_of(row)["title"] == "strobe (michael woods remix)"


def test_an_empty_remixer_column_leaves_the_ordinary_identity_alone(cfg):
    """Most rows. The spelling rule may not move the ordinary case one character."""
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="")
    assert stores.version_of(row) == tombstone.version_identity(artist=ARTIST, title="Strobe")


# ── S2-E: one identity naming two tracks, and one track with two identities ──


def test_a_featured_credit_bracket_does_not_stand_in_for_the_remix(cfg):
    """Two DIFFERENT tracks reached one identity through the guest credit."""
    original = _remixed_row(cfg, ONE, "1", title="Losing It (feat. Anna)", remixer="")
    remix = _remixed_row(cfg, TWO, "2", title="Losing It (feat. Anna)", remixer="Anna", usn=51)
    assert stores.version_of(original) != stores.version_of(remix), (
        "the original and the remix of it share one identity, so deleting the "
        "remix suppresses music the user still wants"
    )
    stores.record_tombstone(cfg, remix, actor="cli")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Losing It (feat. Anna)")


@pytest.mark.parametrize(
    ("title", "version", "carried"),
    [
        ("Track (feat. Anna)", "Anna", False),
        ("Track (ft. Anna)", "Anna", False),
        ("Track (featuring Anna)", "Anna", False),
        ("Track (with Anna)", "Anna", False),
        # A marker anywhere but the HEAD is a word in a mix name, and the head is
        # the whole rule. Reading it by containment would break this one.
        ("Track (Live with Strings)", "Live with Strings", True),
        ("Track (Anna Remix)", "Anna", True),
    ],
)
def test_which_bracketed_groups_can_stand_in_for_the_version(title, version, carried):
    assert (tombstone.version_title(title, version) == title) is carried


def test_the_module_no_longer_claims_the_remixer_column_makes_composition_safe(cfg):
    """The docstring said those collisions were unreachable, and named the wrong reason."""
    remixed = _remixed_row(cfg, ONE, "1", title="Sun", remixer="Sun Path")
    titled = _remixed_row(cfg, TWO, "2", title="Sun (Sun Path)", remixer="", usn=51)
    assert stores.version_of(remixed)["title"] == "sun (sun path remix)"
    assert stores.version_of(remixed) != stores.version_of(titled)
    source = (SRC_ROOT / "cratekit" / "core" / "tombstone.py").read_text()
    assert "unreachable in practice" not in source, (
        "the corrected claim was left in place beside the code that disproves it"
    )


# ── S2-A: the vocabulary's membership, pinned exactly ────────────────────────


def test_the_version_vocabulary_is_exactly_this_set_and_no_other():
    """WIDENING WAS CAUGHT AND NARROWING WAS NOT, which is how a defect walks back."""
    assert tombstone.VERSION_WORDS == frozenset(
        {
            "acapella",
            "acoustic",
            "alternate",
            "bootleg",
            "club",
            "cut",
            "demo",
            "dub",
            "edit",
            "extended",
            "flip",
            "instrumental",
            "interlude",
            "live",
            "mashup",
            "mix",
            "original",
            "radio",
            "remaster",
            "remastered",
            "remix",
            "reprise",
            "rework",
            "session",
            "unplugged",
            "version",
            "vip",
        }
    )


@pytest.mark.parametrize(
    ("subtitle", "believed"),
    [
        # One realistic phrase per word that carries the ordinary library.
        ("Club Mix", True),
        ("Dub", True),
        ("VIP", True),
        ("Acoustic", True),
        ("Original Mix", True),
        ("Radio Edit", True),
        ("Extended Mix", True),
        ("Instrumental", True),
        ("Live", True),
        ("Nightwave Remix", True),
        ("2024 Remaster", True),
        ("Piano Version", True),
        # A NON-WORD split rather than a whitespace one.
        ("Re-Edit", True),
        ("Extended/Club Mix", True),
    ],
)
def test_each_word_the_ordinary_library_leans_on_is_driven_by_a_real_phrase(
    cfg, subtitle, believed
):
    row = _subtitled(cfg, ONE, "1", title="Atlas", subtitle=subtitle)
    seen = library.read_collection(FakeQuery([row]))
    assert bool(seen.removed[0].version) is believed


def test_a_subtitle_the_vocabulary_did_not_believe_is_still_recorded(cfg):
    """The measured failure direction may not be the one place it is invisible."""
    row = _subtitled(cfg, ONE, "1", title="Atlas", subtitle="Anjunadeep")
    seen = library.read_collection(FakeQuery([row])).removed[0]
    assert seen.version == "" and seen.version_unbelieved == "Anjunadeep"
    written = stores.record_tombstone(cfg, seen, actor="cli")
    assert written.payload["version"] == ""
    assert written.payload["version_unbelieved"] == "Anjunadeep"


# ── S2-F: the dead filter, deleted, and the surviving one pinned ─────────────


def test_a_removal_sitting_exactly_on_the_watermark_is_not_offered_again(cfg, gates_pass):
    """STRICTLY GREATER, and it is now written in exactly one place."""
    for name in (ONE, TWO):
        _music(cfg, name)
    on_the_mark = _content(cfg, ONE, "1", deleted=True, usn=40)
    above_it = _content(cfg, TWO, "2", deleted=True, usn=41)
    _baseline(cfg)
    found = run.plan(cfg, FakeDb([on_the_mark, above_it], usn=41), actor="cli")
    assert [item.row.content_id for item in found.candidates] == ["2"]


def test_the_collection_walk_hands_back_every_removal_it_saw(cfg):
    """The walk is unfiltered, because the baseline needs the highest sequence."""
    rows = [_content(cfg, ONE, str(index), deleted=True, usn=index) for index in range(1, 6)]
    seen = library.read_collection(FakeQuery(rows))
    assert [row.sequence for row in seen.removed] == [1, 2, 3, 4, 5]


# Part 10: round six.


# ── F1: the spelling decision was routed through the vocabulary's own known
#        false positives ───────────────────────────────────────────────────────


#: The artist and label names the vocabulary's measured false-positive set names.
_FALSE_POSITIVE_REMIXERS = (
    "Radio Slave",
    "Dub Pistols",
    "Cut Chemist",
    "Mix Master Mike",
    "Club Sweat",
    "Original Gee",
)


@pytest.mark.parametrize("remixer", _FALSE_POSITIVE_REMIXERS)
def test_a_remixer_whose_name_carries_a_version_word_is_still_spelled_matchably(cfg, remixer):
    """THE ROUND'S HEADLINE FIX, SELF REFUTED BY THE TEST IT WAS BUILT ON."""
    assert tombstone.reads_as_version(remixer), (
        "this row no longer exercises the false positive it was written for"
    )
    row = _remixed_row(cfg, ONE, "1", title="Screamer", remixer=remixer)
    assert stores.version_of(row)["title"] == f"screamer ({remixer.casefold()} remix)"
    stores.record_tombstone(cfg, row, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=f"Screamer ({remixer} Remix)"), (
        "the tombstone was written under a spelling no provider will ever produce"
    )


@pytest.mark.parametrize(
    ("remixer", "expected"),
    [
        # THE ONLY VALUES LEFT VERBATIM. The last word is the very word about to
        # be appended, so appending would write it twice.
        ("Michael Woods Remix", "strobe (michael woods remix)"),
        ("Michael Woods Extended Remix", "strobe (michael woods extended remix)"),
        # A designation ending in some OTHER vocabulary word is composed anyway.
        ("Michael Woods Dub", "strobe (michael woods dub remix)"),
        ("Extended Mix", "strobe (extended mix remix)"),
        # An ordinary artist name, which is what this column is guaranteed to
        # hold, spelled the way a provider spells it.
        ("Michael Woods", "strobe (michael woods remix)"),
        ("Anna", "strobe (anna remix)"),
        ("Radio Slave", "strobe (radio slave remix)"),
        ("Cut Copy", "strobe (cut copy remix)"),
        ("The Cut", "strobe (the cut remix)"),
        ("Todd Terry Live", "strobe (todd terry live remix)"),
    ],
)
def test_the_only_remixer_left_verbatim_is_one_that_already_says_remix(cfg, remixer, expected):
    """Both halves of the rule in one table, so neither can be moved alone."""
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer=remixer)
    assert stores.version_of(row)["title"] == expected


# ── F7: an identity that is not unique, and the guard that could never fire ───


def test_a_removed_row_with_no_identifier_of_its_own_is_refused_rather_than_named_None(cfg):
    """``str(None)`` is ``'None'``, which is truthy, so the guard never fired."""
    with pytest.raises(CratekitError) as excinfo:
        tombstone.removed_file_identity(content_id=None, recorded="/music/x.flac")
    assert excinfo.value.cause.reason == "review-selection-invalid"
    with pytest.raises(CratekitError):
        tombstone.removed_file_identity(content_id="", recorded="/music/x.flac")
    # A NUMERIC identifier is a legitimate identifier and zero is a number. The
    # emptiness test runs on the converted value for exactly this reason.
    assert tombstone.removed_file_identity(content_id=0, recorded="/x")["content_id"] == "0"


def test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable(cfg, gates_pass):
    """The same defect end to end, which is where it actually bites."""
    _music(cfg, ONE)
    _baseline(cfg)
    nameless = _content(cfg, ONE, "1", deleted=True, usn=50)
    nameless.ID = None
    seen = library.read_collection(FakeQuery([nameless]))
    assert seen.removed[0].content_id == "", (
        "a row with no identifier was given the identifier 'None'"
    )
    found = run.plan(cfg, FakeDb([nameless], usn=50), actor="cli")
    assert [item.category for item in found.candidates] == [candidates.Category.UNIDENTIFIABLE]
    assert run.present(cfg, found) == (), (
        "a row that can never be deleted was put in front of a person as deletable"
    )


# ── F6: the predicate wired at review time, unpinned in one of its two sites ──


def test_a_row_that_could_never_carry_a_tombstone_is_not_offered_as_deletable(cfg, gates_pass):
    """``plan``'s ``identifiable`` wiring could be deleted with nothing noticing."""
    _music(cfg, ONE)
    _baseline(cfg)
    anonymous = _content(cfg, ONE, "1", deleted=True, usn=50, title="")
    anonymous.ArtistName = ""
    found = run.plan(cfg, FakeDb([anonymous], usn=50), actor="cli")
    assert [item.category for item in found.candidates] == [candidates.Category.UNIDENTIFIABLE]
    assert found.candidates[0].problem
    assert run.present(cfg, found) == ()
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


# ── F9: the discriminator the Subtitle vocabulary finding said nothing carried ─


def _versioned(cfg, name, content_id, *, usn, title, isrc, subtitle="", remixer=""):
    """One removed collection row with a version column and an ISRC filled in."""
    row = _content(cfg, name, content_id, deleted=True, usn=usn, title=title, isrc=isrc)
    row.Subtitle = subtitle
    row.RemixerName = remixer
    return row


def test_two_recordings_that_land_on_one_identity_are_refused_rather_than_suppressed(
    cfg, gates_pass
):
    """The indistinguishability claim is false as stated, and this is why."""
    for name in (ONE, TWO):
        _music(cfg, name)
    _baseline(cfg)
    rows = [
        _versioned(
            cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111", subtitle="Acappella"
        ),
        _versioned(cfg, TWO, "2", usn=51, title="Strobe", isrc="BBBB22222222", subtitle="Refix"),
    ]
    seen = library.read_collection(FakeQuery(rows))
    assert stores.version_of(seen.removed[0]) == stores.version_of(seen.removed[1]), (
        "this row no longer exercises the collision it was written for"
    )
    found = run.plan(cfg, FakeDb(rows, usn=51), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.AMBIGUOUS_VERSION,
        candidates.Category.AMBIGUOUS_VERSION,
    ]
    assert run.present(cfg, found) == (), (
        "a suppression that would take out a second recording was offered"
    )
    assert found.candidates[0].problem


def test_the_convergence_composition_exists_to_produce_is_still_deletable(cfg, gates_pass):
    """The half the discriminator may not cost, and it is the whole point of composing."""
    for name in (ONE, TWO):
        _music(cfg, name)
    _baseline(cfg)
    rows = [
        _versioned(
            cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111", remixer="Michael Woods"
        ),
        _versioned(
            cfg, TWO, "2", usn=51, title="Strobe (Michael Woods Remix)", isrc="AAAA11111111"
        ),
    ]
    found = run.plan(cfg, FakeDb(rows, usn=51), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.DELETABLE,
        candidates.Category.DELETABLE,
    ]


def test_an_absent_isrc_is_read_as_agreement_rather_than_as_a_collision(cfg, gates_pass):
    """The check is inconclusive without a code, and inconclusive means proceed."""
    for name in (ONE, TWO):
        _music(cfg, name)
    _baseline(cfg)
    rows = [
        _versioned(
            cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111", subtitle="Acappella"
        ),
        _versioned(cfg, TWO, "2", usn=51, title="Strobe", isrc=None, subtitle="Refix"),
    ]
    found = run.plan(cfg, FakeDb(rows, usn=51), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.DELETABLE,
        candidates.Category.DELETABLE,
    ]


def test_the_collision_is_looked_for_across_the_whole_walk_not_the_offered_rows(cfg, gates_pass):
    """The row a candidate collides with is very often one an earlier run retired."""
    for name in (ONE, TWO):
        _music(cfg, name)
    below = _versioned(
        cfg, ONE, "1", usn=10, title="Strobe", isrc="AAAA11111111", subtitle="Acappella"
    )
    run.plan(cfg, FakeDb([below], usn=40), actor="cli")
    above = _versioned(cfg, TWO, "2", usn=50, title="Strobe", isrc="BBBB22222222", subtitle="Refix")
    found = run.plan(cfg, FakeDb([below, above], usn=50), actor="cli")
    assert [item.row.content_id for item in found.candidates] == ["2"], (
        "the row below the watermark should not be offered"
    )
    assert found.candidates[0].category is candidates.Category.AMBIGUOUS_VERSION, (
        "the colliding row was invisible because it sat below the watermark"
    )


def test_a_confirmed_ambiguous_row_is_refused_at_move_time_too(cfg, gates_pass, tmp_path):
    """The re-check gets the same answer the review was made under."""
    home = _home(tmp_path)
    for name in (ONE, TWO):
        _music(cfg, name)
    _baseline(cfg)
    alone = _versioned(
        cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111", subtitle="Acappella"
    )
    db = FakeDb([alone], usn=50)
    _confirm_first(cfg, db)
    # The second recording is removed between the confirmation and the move.
    db.rows.append(
        _versioned(cfg, TWO, "2", usn=51, title="Strobe", isrc="BBBB22222222", subtitle="Refix")
    )
    db.usn = 51
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == ()
    assert (Path(cfg.library.root) / "Music" / ONE).exists()
    assert stores.list_tombstones(cfg, include_revoked=True) == ()


# ── F2: one Finder delete wedged every removal above it ──────────────────────


def test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one(
    cfg, gates_pass, tmp_path, caplog
):
    """THE HOLD THAT CLOSED A SILENT RETIREMENT WEDGED THE WHOLE QUEUE."""
    home = _home(tmp_path)
    db = _prepared(cfg, names=(ONE, TWO))
    found = run.plan(cfg, db, actor="cli")
    _confirm_all(cfg, run.present(cfg, found))
    (Path(cfg.library.root) / "Music" / ONE).unlink()
    with caplog.at_level(logging.WARNING):
        report = run.apply(cfg, db, actor="cli", home=home)
    assert [item.candidate.row.content_id for item in report.trashed] == ["2"]
    assert [item.category for item in report.refused] == [candidates.Category.GONE]
    assert len(stores.list_tombstones(cfg, include_revoked=True)) == 2, (
        "the deletion the person completed themselves was never recorded, so R36 "
        "is false for that row with nothing saying so"
    )
    assert report.watermark.sequence == 51, (
        "a removal that was trashed and recorded is held behind one whose file "
        "the person deleted in the Finder, forever"
    )
    # And a later run has nothing left to do, which is what "finished" means.
    again = run.plan(cfg, db, actor="cli")
    assert again.candidates == ()


# ── F3: the mirror case, retired without a word ──────────────────────────────


def test_an_unanswered_removal_whose_file_moved_is_retired_but_not_in_silence(
    cfg, gates_pass, tmp_path, caplog
):
    """The scoping is deliberate. The silence was not."""
    home = _home(tmp_path)
    db = _prepared(cfg)
    moved = Path(cfg.library.root) / "Music" / "Moved By Hand.flac"
    (Path(cfg.library.root) / "Music" / ONE).rename(moved)
    with caplog.at_level(logging.WARNING):
        report = run.apply(cfg, db, actor="cli", home=home)
    assert report.trashed == ()
    assert stores.list_tombstones(cfg, include_revoked=True) == (), (
        "a deletion nobody asked for was recorded"
    )
    assert report.watermark.sequence == 50, "the deliberate scoping was changed"
    assert "nothing will offer it again" in caplog.text, (
        "the file went out of reach of both rekordbox and this pass without a word"
    )
    assert moved.exists()


# ── F4: two commits that interact, and a store every existing user already has ─


def test_a_tombstone_an_earlier_build_wrote_is_still_recognised(cfg, gates_pass, tmp_path):
    """TWO COMMITS IN ONE ROUND, NEITHER RECORDING THAT THEY INTERACT."""
    _music(cfg, ONE)
    _baseline(cfg)
    row = _versioned(
        cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111", remixer="Michael Woods"
    )
    removed = library.read_collection(FakeQuery([row])).removed[0]
    # THE EARLIER SPELLING IS A LITERAL, AND IT HAS TO BE.
    earlier = tombstone.version_identity(artist=removed.artist, title="Strobe (Michael Woods)")
    assert earlier != stores.version_of(removed), (
        "this row no longer exercises the spelling change it was written for"
    )
    stores.tombstones(cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=earlier,
        payload={"content_id": removed.content_id, "recorded": removed.recorded},
        actor="cli",
    )
    assert stores.tombstone_predicate(cfg)(removed), (
        "a deletion an earlier build recorded is not recognised, so the row is held open forever "
        "and the person is told to put back a file that is already in the Trash where they put it"
    )
    # AND THE CONSULT IS NOT WIDENED WITH IT, which is the scope of the whole
    # change.
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods)")
    home = _home(tmp_path)
    db = FakeDb([row], usn=50)
    _confirm_first(cfg, db)
    (Path(cfg.library.root) / "Music" / ONE).unlink()
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.watermark.sequence == 50
    assert len(stores.list_tombstones(cfg, include_revoked=True)) == 1, (
        "the deletion was recorded a second time under the new spelling"
    )


# ── F10: the completeness proof was one sided, and the walk could raise ───────


class UndercountQuery:
    """A query that DECLARES fewer rows than it hands back."""

    def __init__(self, rows, declared):
        self._rows = list(rows)
        self._declared = declared

    def __iter__(self):
        return iter(self._rows)

    def count(self):
        return self._declared


class FailingWalk:
    """A query whose walk raises partway through. ``count()`` answers normally."""

    def __init__(self, rows, declared):
        self._rows = list(rows)
        self._declared = declared

    def __iter__(self):
        yield from self._rows
        raise RuntimeError("the cursor was closed underneath the walk")

    def count(self):
        return self._declared


def test_a_membership_count_that_is_short_refuses_as_readily_as_a_short_walk(cfg):
    """Either side of the comparison being wrong is the same fault."""
    with pytest.raises(CratekitError) as excinfo:
        library.playlist_referenced(UndercountQuery([_membership("1"), _membership("2")], 1))
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert excinfo.value.cause.detail == {"declared": 1, "walked": 2}


def test_a_membership_walk_that_raises_is_a_refusal_rather_than_a_traceback(cfg):
    """S4: an unstructured exception reaches the command line as an internal defect."""
    with pytest.raises(CratekitError) as excinfo:
        library.playlist_referenced(FailingWalk([_membership("1")], 5))
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert excinfo.value.cause.detail == {"walked": 1}
    assert "cursor was closed" in excinfo.value.cause.message


def test_a_live_membership_that_names_no_row_refuses_rather_than_freeing_the_file(cfg):
    """A reference this pass cannot address would read as no reference at all."""
    with pytest.raises(CratekitError) as excinfo:
        library.playlist_referenced(
            FakeQuery([FakeRow(ID="m1", ContentID=None, rb_local_deleted=0)])
        )
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"


# ── Z: two round-four zero rows on the destructive path ──────────────────────


def test_a_trash_directory_this_account_cannot_write_to_is_not_usable(tmp_path):
    """``probe``'s access check could be neutralised with nothing noticing."""
    home = tmp_path / "home"
    files = home / ".Trash"
    files.mkdir(parents=True)
    music = tmp_path / "Track.flac"
    music.write_bytes(b"x")
    assert trash.probe(music, home=home, platform="darwin").usable
    files.chmod(0o500)
    try:
        status = trash.probe(music, home=home, platform="darwin")
        assert not status.usable, (
            "a Trash this account cannot write to was reported usable, so the move would be "
            "attempted and the refusal that protects the file would never be raised"
        )
        assert "not writable" in status.problem
        with pytest.raises(CratekitError) as excinfo:
            trash.assert_usable(music, home=home, platform="darwin")
        assert excinfo.value.cause.reason == "trash-unavailable"
    finally:
        files.chmod(0o700)


def test_a_name_the_filesystem_calls_invalid_costs_one_file_and_not_the_run(tmp_path, monkeypatch):
    """``EINVAL`` could be dropped from the set with the whole suite green."""
    directory = tmp_path / "trash"
    directory.mkdir()

    def invalid(*args, **kwargs):
        raise OSError(errno.EINVAL, "invalid argument")

    monkeypatch.setattr(os, "open", invalid)
    with pytest.raises(CratekitError) as excinfo:
        trash._free_name(directory, ONE)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.scope is Scope.ITEM, "one unacceptable name aborted the whole pass"


# Round 7: an empty mount point is not a deletion, and a remixer is an artist


def _removed_elsewhere(count, *, usn=50):
    """``count`` REMOVED collection rows recorded under the mapped prefix."""
    rows = []
    for index in range(count):
        row = _at(
            f"{RECORDED_ELSEWHERE}/Music/Removed {index}.flac",
            f"r{index}",
            deleted=True,
            usn=usn + index,
        )
        rows.append(row)
    return rows


def _mapped_volume(cfg, tmp_path, *, active=50, removed=20, volume_id=None):
    """A mounted volume holding ``active`` referenced files and ``removed`` candidates."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    volume.mkdir(parents=True)
    live = _elsewhere(active)
    gone = _removed_elsewhere(removed)
    _populate(volume, live)
    for row in gone:
        target = Path(str(volume) + row.FolderPath[len(RECORDED_ELSEWHERE) :])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"audio bytes")
    rule = [
        locations.PrefixRule(RECORDED_ELSEWHERE, str(volume), volume_id or cfg.library.volume_id)
    ]
    _baseline(cfg)
    active_rows = [_at(row.recorded, row.content_id, usn=10) for row in live]
    return volume, rule, FakeDb([*active_rows, *gone], usn=100), gone


def _empty_the_mount_point(volume: Path) -> None:
    """What macOS leaves after an unclean eject: the directory, and nothing in it."""
    for child in sorted(volume.rglob("*"), reverse=True):
        if child.is_file() or child.is_symlink():
            child.unlink()
        else:
            child.rmdir()


def test_a_stale_empty_mount_point_writes_no_tombstone_and_retires_no_row(
    cfg, gates_pass, tmp_path, caplog
):
    """F1: ABSENCE READ AS EVIDENCE, upgraded to a permanent record of a deletion."""
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path)
    home = _home(tmp_path)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    offered = run.present(cfg, found)
    assert len(offered) == len(gone), "every removed row was offered while mounted"
    _confirm_all(cfg, offered)
    _empty_the_mount_point(volume)
    with caplog.at_level(logging.WARNING):
        report = run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert report.plan.references.suspect_anchors == (str(volume),)
    assert len(report.plan.references.missing) == 50
    assert [item.category for item in report.refused] == [candidates.Category.GONE] * len(gone)
    assert stores.list_tombstones(cfg, include_revoked=True) == (), (
        "twenty deletions were RECORDED for an unmounted drive, so remounting it "
        "brings none of those versions back"
    )
    assert report.watermark.sequence == 40, (
        "the watermark walked past twenty rows whose files this run never saw"
    )
    assert str(volume) in caplog.text


def test_a_genuine_unmount_still_answers_unresolved_on_every_row(cfg, tmp_path):
    """The half that must not regress, and it is a DIFFERENT branch from F1's."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    rule = [locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))]
    rows = [
        library.RemovedRow(
            content_id=f"r{index}",
            recorded=f"{RECORDED_ELSEWHERE}/Music/Removed {index}.flac",
            sequence=50 + index,
            size=11,
            artist=ARTIST,
            title=f"Removed {index}",
        )
        for index in range(20)
    ]
    answered = _categorize(cfg, rows, _references(cfg, []), prefix_map=rule)
    assert [item.category for item in answered] == [candidates.Category.UNRESOLVED] * 20
    assert not any(item.handled for item in answered)
    assert all(str(volume) in item.problem for item in answered)


def test_an_unanswered_removal_under_a_stale_mount_point_is_not_retired_either(
    cfg, gates_pass, tmp_path, caplog
):
    """The mirror, because a retirement is permanent with or without a tombstone."""
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path)
    home = _home(tmp_path)
    run.plan(cfg, db, actor="cli", prefix_map=rule)
    _empty_the_mount_point(volume)
    with caplog.at_level(logging.WARNING):
        report = run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert report.trashed == ()
    assert report.watermark.sequence == 40, (
        "twenty unanswered removals were retired off an empty directory"
    )
    assert "was NOT retired" in caplog.text


def test_one_file_deleted_by_hand_under_a_healthy_anchor_is_still_settled(
    cfg, gates_pass, tmp_path
):
    """The wedge fix that F1 may not take back, driven on the case it was for."""
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, removed=1)
    home = _home(tmp_path)
    _confirm_first(cfg, db, prefix_map=rule)
    Path(str(volume) + gone[0].FolderPath[len(RECORDED_ELSEWHERE) :]).unlink()
    report = run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert report.plan.references.suspect_anchors == ()
    recorded = stores.list_tombstones(cfg, include_revoked=True)
    assert len(recorded) == 1, "the queue wedged on a file that cannot come back"
    assert report.watermark.sequence == 50


# ── F4: the remixer spelling, measured over 65 values in three classes ───────


#: 40 values that are genuine mix-name DESIGNATIONS.
_DESIGNATIONS = (
    "Extended Mix",
    "Club Mix",
    "Radio Edit",
    "Original Mix",
    "Michael Woods Remix",
    "Instrumental Version",
    "Acoustic Version",
    "Extended Remix",
    "Dub Mix",
    "Radio Mix",
    "Extended Club Mix",
    "Remix Edit",
    "Original Version",
    "Extended Version",
    "Radio Version",
    "Acapella",
    "Bootleg",
    "Rework",
    "Instrumental Dub",
    "Live Session",
    "Versión Extendida",
    "Mezcla Extendida",
    "Versão Estendida",
    "Version Longue",
    "Ao Vivo em Lisboa",
    "Live aus Berlin",
    "Studioversion 2",
    "Versione Estesa",
    "Live at Wembley",
    "Mixed by Someone",
    "Remix Edit 2024",
    "Dub Mix Pt. 2",
    "Alternate Take",
    "Remastered 2019",
    "Live in Tokyo",
    "Demo Take 2",
    "Extended Mix 2",
    "Live Session at Maida Vale",
    "Club Mix Pt. 2",
    "Mezcla Ampliada",
)

#: 15 ARTIST names whose LAST word is in the vocabulary. Round six left every one
#: of these verbatim.
_ARTISTS_WORD_LAST = (
    "The Cut",
    "Da Dub",
    "Todd Terry Live",
    "Bicep Live",
    "Sasha Live",
    "Group Therapy Radio",
    "Anjunadeep Radio",
    "Kaskade Radio",
    "Rinse Club",
    "Sub Club",
    "Smoke Machine Dub",
    "King Tubby Dub",
    "Studio Session",
    "Boiler Room Live",
    "Defected Radio",
)

#: 10 ARTIST names carrying a vocabulary word anywhere but last. Round five left
#: every one of these verbatim.
_ARTISTS_WORD_FIRST = (
    "Radio Slave",
    "Dub Pistols",
    "Cut Chemist",
    "Mix Master Mike",
    "Club Sweat",
    "Original Gee",
    "Dub Phizix",
    "Remix Artist Collective",
    "Live Element",
    "Cut Copy",
)

#: The measured miss counts for the SHIPPED rule, per class, pinned exactly so a
#: change in either direction is a failing test rather than a paragraph.
_MEASURED_MISSES = {"designation": 38, "artist-word-last": 0, "artist-word-first": 0}


def _provider_spelling(value: str, klass: str) -> str:
    """What a provider actually spells for the version this value names."""
    if klass == "designation":
        return tombstone.version_title("Strobe", value)
    return tombstone.version_title("Strobe", f"{value} {tombstone.REMIX_DESIGNATION}")


def test_the_remixer_spelling_misses_exactly_where_it_is_measured_to_miss():
    """F4: the rule is decided by a measurement over classes, not by a frequency."""
    values = (
        [(value, "designation") for value in _DESIGNATIONS]
        + [(value, "artist-word-last") for value in _ARTISTS_WORD_LAST]
        + [(value, "artist-word-first") for value in _ARTISTS_WORD_FIRST]
    )
    assert len(values) == 65
    misses = {klass: 0 for klass in _MEASURED_MISSES}
    for value, klass in values:
        if tombstone.remixer_title("Strobe", value) != _provider_spelling(value, klass):
            misses[klass] += 1
    assert misses == _MEASURED_MISSES
    assert misses["artist-word-last"] + misses["artist-word-first"] == 0, (
        "the rule errs on an ARTIST NAME, which is the class the column holds by "
        "schema and the only error class that can reach over-suppression"
    )


def test_appending_unconditionally_would_be_strictly_worse_and_by_how_much():
    """Why a test survives at all, stated as the two values that decide it."""
    differing = [
        value
        for value in (*_DESIGNATIONS, *_ARTISTS_WORD_LAST, *_ARTISTS_WORD_FIRST)
        if tombstone.remixer_title("Strobe", value)
        != tombstone.version_title("Strobe", f"{value} {tombstone.REMIX_DESIGNATION}")
    ]
    assert differing == ["Michael Woods Remix", "Extended Remix"]
    assert all(
        tombstone.remixer_title("Strobe", value) == _provider_spelling(value, "designation")
        for value in differing
    ), "the branch that survives has to be right on the values it survives for"


def test_one_string_read_as_an_artist_and_as_a_designation_stays_two_identities(cfg):
    """F2: the fix's own safety claim, falsified on the docstring's own examples."""
    for value in ("The Cut", "Da Dub"):
        as_artist = _remixed_row(cfg, ONE, "1", title="Strobe", remixer=value)
        subtitled = _subtitled(cfg, TWO, "2", title="Strobe", subtitle=value, usn=51)
        as_designation = library.read_collection(FakeQuery([subtitled])).removed[0]
        assert stores.version_of(as_artist) != stores.version_of(as_designation), (
            f"{value!r} read as an artist and read as a designation are one "
            f"identity, so deleting either suppresses the other"
        )
        assert stores.ambiguous_versions([as_artist, as_designation]) == frozenset(), (
            "the discriminator cannot see this and was never the thing holding it"
        )


# ── F3: the listing has to say which deletions this tool actually performed ──


def test_a_listing_says_which_suppressions_moved_no_file(cfg, gates_pass, tmp_path):
    """A tombstone the tool HONOURED and one it ASSERTED were indistinguishable."""
    home = _home(tmp_path)
    db = _prepared(cfg, names=(ONE, TWO), usn=50)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm_all(cfg, offered)
    (Path(cfg.library.root) / "Music" / TWO).unlink()
    run.apply(cfg, db, actor="cli", home=home)
    listed = {
        record["title"]: record for record in map(stores.summarize, stores.list_tombstones(cfg))
    }
    assert set(listed) == {Path(ONE).stem, Path(TWO).stem}
    assert listed[Path(ONE).stem]["trashed_to"], "a real move is not shown as one"
    assert listed[Path(TWO).stem]["trashed_to"] == "", (
        "a suppression written for a file this pass never touched is listed "
        "exactly like one it moved into the Trash"
    )
    assert set(listed[Path(ONE).stem]) >= {"version", "version_unbelieved", "isrc"}, (
        "the payload's own comment says an auditor can see which column value "
        "the identity was built from, and the listing did not emit it"
    )


def test_the_listing_carries_the_column_value_a_missed_tombstone_was_built_from(cfg):
    """The other half of the same claim, on the row where it is the whole answer."""
    row = library.read_collection(
        FakeQuery([_subtitled(cfg, ONE, "1", title="Atlas", subtitle="Anjunadeep")])
    ).removed[0]
    stores.record_tombstone(cfg, row, actor="cli", trashed_to="/x/.Trash/Atlas.flac")
    listed = stores.summarize(stores.list_tombstones(cfg)[0])
    assert listed["version"] == ""
    assert listed["version_unbelieved"] == "Anjunadeep"
    assert listed["trashed_to"] == "/x/.Trash/Atlas.flac"


# ── F8 and F9: two low residuals on identity and on the discriminator ────────


@pytest.mark.parametrize("blank", ["   ", "\t", "\n ", " "])
def test_a_removed_row_identified_by_whitespace_is_refused(blank):
    """The same shape as the ``'None'`` defect just closed, one step along."""
    with pytest.raises(CratekitError) as excinfo:
        tombstone.removed_file_identity(content_id=blank, recorded="/x.flac")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_a_numeric_identifier_is_still_addressable():
    """The half the stripped test may not cost: ``not 0`` would refuse a real row."""
    assert tombstone.removed_file_identity(content_id=0, recorded="/x.flac")["content_id"] == "0"


def test_two_spellings_of_one_isrc_are_one_recording(cfg):
    """F9: an ISRC is case-insensitive by specification and was compared raw."""
    one = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="gbaya1500001")
    other = replace(_removed(cfg, TWO, "2"), title="Strobe", isrc="GBAYA1500001")
    assert stores.version_of(one) == stores.version_of(other)
    assert stores.ambiguous_versions([one, other]) == frozenset(), (
        "one recording filed twice was refused as two recordings on case alone"
    )
    third = replace(_removed(cfg, ACCENTED, "3"), title="Strobe", isrc="USRC17607839")
    assert stores.ambiguous_versions([one, third]) == frozenset({"1", "3"}), (
        "folding may not cost the discriminator the collision it exists for"
    )


# ── Round 8: three values whose own typing survived into an identity ─────────


def test_the_display_form_of_one_isrc_is_not_two_recordings(cfg):
    """Round 8: the case fix went green over a wider defect at the same site."""
    one = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="GBAYA1500001")
    other = replace(_removed(cfg, TWO, "2"), title="Strobe", isrc="GB-AYA-15-00001")
    assert stores.version_of(one) == stores.version_of(other)
    assert stores.ambiguous_versions([one, other]) == frozenset(), (
        "the display form of a code is the same code, and reading it as a second "
        "recording wedges the queue at that row forever"
    )


def test_a_placeholder_in_the_isrc_column_is_an_absent_code(cfg):
    """A separator is not a code, and silence is read as agreement."""
    real = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="GBAYA1500001")
    placeholder = replace(_removed(cfg, TWO, "2"), title="Strobe", isrc="-")
    assert stores.ambiguous_versions([real, placeholder]) == frozenset(), (
        "a placeholder is an absent code, not a code that disagrees"
    )


def test_folding_the_code_does_not_cost_the_collision_it_exists_for(cfg):
    """The half a wider fold could cost: two real codes must still disagree."""
    one = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="GB-AYA-15-00001")
    third = replace(_removed(cfg, ACCENTED, "3"), title="Strobe", isrc="US-RC1-76-07839")
    assert stores.ambiguous_versions([one, third]) == frozenset({"1", "3"}), (
        "two different recordings in display form must still read as a collision"
    )


@pytest.mark.parametrize(
    "version, expected",
    [
        pytest.param("Michael Woods Remix   ", "Strobe (Michael Woods Remix)", id="trailing-space"),
        pytest.param(" Michael Woods Remix", "Strobe (Michael Woods Remix)", id="leading-space"),
        pytest.param("Michael  Woods  Remix", "Strobe (Michael Woods Remix)", id="interior-run"),
        pytest.param("Michael Woods (Remix)", "Strobe (Michael Woods Remix)", id="own-brackets"),
        pytest.param(
            "[Michael Woods Remix]", "Strobe (Michael Woods Remix)", id="own-square-brackets"
        ),
    ],
)
def test_a_columns_own_typing_does_not_become_a_second_identity(version, expected):
    """Round 8: the value is tidied BEFORE it goes inside the bracket."""
    assert tombstone.version_title("Strobe", version) == expected


def test_tidying_the_value_does_not_rewrite_the_persons_own_text():
    """The bound on the tidy: the ends and the brackets and NOTHING else."""
    assert (
        tombstone.version_title("Strobe", "  Michael Woods' 12\" Re-Edit  ")
        == "Strobe (Michael Woods' 12\" Re-Edit)"
    )


@pytest.mark.parametrize("boolean", [True, False])
def test_a_boolean_identifier_is_refused_rather_than_addressed_as_its_repr(boolean):
    """Round 8: ``str(False)`` is ``'False'``, truthy, and strips to itself."""
    with pytest.raises(CratekitError) as excinfo:
        tombstone.removed_file_identity(content_id=boolean, recorded="/x.flac")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_refusing_booleans_does_not_take_the_numeric_identifier_with_it():
    """Why the guard is ``isinstance`` and not a comparison."""
    assert tombstone.removed_file_identity(content_id=0, recorded="/x.flac")["content_id"] == "0"
    assert tombstone.removed_file_identity(content_id=1, recorded="/x.flac")["content_id"] == "1"


# ── Round 10: the era is stamped in the record, so history is a LOOKUP ───────


def test_the_folding_limb_of_the_tidy_is_covered_on_its_own(cfg):
    """F3 from the round 8 verification: a guard covered only by another guard."""
    assert (
        tombstone.version_title("Strobe (Michael Woods Remix)", "[Michael Woods Remix]")
        == "Strobe (Michael Woods Remix)"
    )
    assert tombstone.version_title("Strobe", "()") == "Strobe"


def _record_an_earlier_build_wrote(cfg, row, *, title, stamp=None):
    """Plant the record a build with OTHER composition rules left on this disk."""
    payload = {
        "artist": row.artist,
        "title": row.title,
        "version": row.version,
        "version_unbelieved": row.version_unbelieved,
        "isrc": row.isrc or "",
        "content_id": row.content_id,
        "recorded": row.recorded,
        "trashed_to": "",
    }
    if stamp is not None:
        payload[stores.IDENTITY_SCHEME_FIELD] = stamp
    return stores.tombstones(cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist=row.artist, title=title),
        payload=payload,
        actor="cli",
    )


def _one_removed_row(cfg, *, title, subtitle="", remixer="", content_id="1"):
    _music(cfg, ONE)
    _baseline(cfg)
    row = _versioned(
        cfg,
        ONE,
        content_id,
        usn=50,
        title=title,
        isrc="AAAA11111111",
        subtitle=subtitle,
        remixer=remixer,
    )
    return library.read_collection(FakeQuery([row])).removed[0]


@pytest.mark.parametrize(
    "spelling",
    [
        pytest.param("Strobe (Michael Woods)", id="before-the-remixer-was-spelled"),
        pytest.param("Strobe ( Michael Woods  Remix)", id="before-the-value-was-tidied"),
        pytest.param("Strobe", id="before-anything-was-composed"),
        pytest.param("Strobe (Michael Woods Rework)", id="a-designation-nobody-uses"),
        # THE ROW THIS TEST EXISTS FOR.
        pytest.param("a rule this build has never heard of", id="a-rule-nobody-has-written"),
    ],
)
def test_a_tombstone_is_recognised_whatever_rule_composed_its_identity(cfg, gates_pass, spelling):
    """The recognition question no longer depends on the spelling at all."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    planted = _record_an_earlier_build_wrote(cfg, removed, title=spelling)
    assert planted.identity != stores.version_of(removed), (
        "this spelling is what this build writes, so it exercises no history"
    )
    assert stores.tombstone_predicate(cfg)(removed), (
        "a deletion an earlier build recorded is not recognised, so the row is held open forever "
        "and the person is told to put back a file that is already in the Trash where they put it"
    )
    # AND THE CONSULT IS NOT WIDENED WITH IT.
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)")


def test_the_ordinary_row_whose_history_was_reported_as_absent(cfg, gates_pass):
    """B2 from the round 9 verification, and it needed no unusual column at all."""
    removed = _one_removed_row(cfg, title="Strobe Extended Mix", subtitle="Extended Mix")
    assert stores.version_of(removed)["title"] == "strobe extended mix (extended mix)"
    _record_an_earlier_build_wrote(cfg, removed, title="Strobe Extended Mix")
    assert stores.tombstone_predicate(cfg)(removed), (
        "the record the substring-test build wrote for an ordinary row is "
        "orphaned, so that row holds the watermark and every removal above it"
    )


def test_an_earlier_builds_record_retires_the_row_through_the_whole_pass(
    cfg, gates_pass, tmp_path, caplog
):
    """The same thing driven end to end, which is where the cost is paid."""
    home = _home(tmp_path)
    db = _prepared(cfg)
    found = _confirm_first(cfg, db)
    removed = found.candidates[0].row
    _record_an_earlier_build_wrote(cfg, removed, title="whatever that build composed")
    (Path(cfg.library.root) / "Music" / ONE).unlink()
    with caplog.at_level(logging.WARNING):
        report = run.apply(cfg, db, actor="cli", home=home)
    assert [item.category for item in report.refused] == [candidates.Category.GONE]
    assert report.watermark.sequence == 50, (
        "the row was held open, so every removal after it is held too"
    )
    assert len(stores.list_tombstones(cfg, include_revoked=True)) == 1, (
        "a second tombstone was written for a deletion that already had one"
    )


def test_a_record_this_build_wrote_says_which_rules_composed_it(cfg, gates_pass):
    """The stamp is written, is the measured value, and reaches the listing."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    record = stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")
    assert record.payload[stores.IDENTITY_SCHEME_FIELD] == stores.identity_scheme()
    assert stores.summarize(record)[stores.IDENTITY_SCHEME_FIELD] == stores.identity_scheme()
    # THE SHAPE IS PINNED SEPARATELY FROM THE VALUE, because the equalities above
    # take their expected value from the code under test and would be satisfied
    # by a stamp that is always the empty string.
    stamp = stores.identity_scheme()
    assert stamp.startswith("is2_") and len(stamp) == len("is2_") + 16
    # AND IT IS ON THE DISK, not only on the object the writer returned.
    assert stamp in stores.tombstones(cfg).path.read_text()


def _fold_nfkc(value):
    """``fold``, normalising NFKC rather than NFC. A real function, so it has source."""
    return tombstone._SPACING.sub(" ", unicodedata.normalize("NFKC", str(value)).casefold()).strip()


def _fold_unnormalised(value):
    """``fold`` with the normalisation step gone and everything else kept."""
    return tombstone._SPACING.sub(" ", str(value).casefold()).strip()


@pytest.mark.parametrize(
    "module_name, attribute, replacement",
    [
        # ── ADDITIVE DRIFTS.
        *(
            pytest.param(
                "tombstone",
                "VERSION_WORDS",
                tombstone.VERSION_WORDS | {word},
                id=f"vocabulary-gains-{word}",
            )
            for word in (
                "refix",
                "redux",
                "vocal",
                "acappella",
                "nightcore",
                "slowed",
                "rmx",
                "dubplate",
                "versión",
                "bootie",
            )
        ),
        pytest.param(
            "tombstone",
            "_CREDIT_MARKERS",
            tombstone._CREDIT_MARKERS | {"vs"},
            id="credit-markers-gains-vs",
        ),
        pytest.param(
            "tombstone",
            "_CREDIT_MARKERS",
            tombstone._CREDIT_MARKERS | {"x"},
            id="credit-markers-gains-x",
        ),
        pytest.param("tombstone", "fold", _fold_nfkc, id="the-fold-goes-nfkc"),
        pytest.param("tombstone", "fold", _fold_unnormalised, id="the-fold-stops-normalising"),
        pytest.param(
            "tombstone",
            "_BRACKET_CHARACTERS",
            re.compile(r"[()\[\]{}]+"),
            id="the-tidy-covers-braces",
        ),
        pytest.param(
            "tombstone",
            "_BRACKETED",
            re.compile(r"\(([^()]*)\)|\[([^\[\]]*)\]|\{([^{}]*)\}"),
            id="the-carrying-test-covers-braces",
        ),
        pytest.param("tombstone", "REMIX_DESIGNATION", "Remix Edit", id="designation-gains-a-word"),
        pytest.param(
            "tombstone",
            "_WORD_SPLIT",
            re.compile(r"[^\w']+", re.UNICODE),
            id="the-word-split-keeps-apostrophes",
        ),
        pytest.param(
            "library",
            "_VERSION_COLUMNS",
            (
                ("RemixerName", library.VERSION_IS_AN_ARTIST),
                ("Subtitle", library.VERSION_IS_A_DESIGNATION),
                ("Comments", library.VERSION_IS_A_DESIGNATION),
            ),
            id="a-third-column-below-the-two",
        ),
        # ── SUBTRACTIVE DRIFTS, the round 10 set ──
        pytest.param("tombstone", "_is_a_credit", lambda group: False, id="is-a-credit"),
        pytest.param("tombstone", "_CREDIT_MARKERS", frozenset(), id="credit-markers"),
        pytest.param(
            "tombstone",
            "_already_carries",
            lambda title, folded: folded in tombstone.fold(title),
            id="already-carries",
        ),
        pytest.param(
            "tombstone",
            "already_spelled_as_a_remix",
            lambda value: False,
            id="already-spelled-as-a-remix",
        ),
        pytest.param("tombstone", "REMIX_DESIGNATION", "Rework", id="remix-designation"),
        pytest.param(
            "tombstone", "_as_a_bracketed_value", lambda version: str(version), id="the-tidy"
        ),
        pytest.param(
            "tombstone", "fold", lambda value: " ".join(str(value).split()), id="the-fold"
        ),
        pytest.param("tombstone", "VERSION_WORDS", frozenset({"remix"}), id="the-vocabulary"),
        pytest.param(
            "library",
            "_VERSION_COLUMNS",
            (
                ("Subtitle", library.VERSION_IS_A_DESIGNATION),
                ("RemixerName", library.VERSION_IS_AN_ARTIST),
            ),
            id="the-column-order",
        ),
    ],
)
def test_the_stamp_moves_when_any_rule_below_it_moves(
    monkeypatch, module_name, attribute, replacement
):
    """B1 GENERALISED, which is the whole reason this round exists."""
    before = stores.identity_scheme()
    monkeypatch.setattr(
        {"tombstone": tombstone, "library": library}[module_name], attribute, replacement
    )
    assert stores.identity_scheme() != before, (
        f"{module_name}.{attribute} changed what a row composes to and the stamp did not move, so "
        "a build with this change would read its predecessor's records as its own and miss them"
    )


def test_this_builds_own_record_is_matched_on_its_version_not_on_its_row(cfg, gates_pass):
    """What the stamp DECIDES, which is the only thing it decides."""
    removed = _one_removed_row(cfg, title="Strobe", subtitle="Extended Mix")
    stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")
    assert stores.tombstone_predicate(cfg)(removed)
    edited = replace(removed, version="Club Mix")
    assert stores.version_of(edited) != stores.version_of(removed)
    assert not stores.tombstone_predicate(cfg)(edited), (
        "a row whose version column changed after the deletion was recorded is read as already "
        "recorded, so the tombstone naming the version it claims now is never written"
    )


def test_reading_a_store_from_before_the_stamp_migrates_it_and_writes_nothing(cfg, gates_pass):
    """The migration path, and it is that there is nothing to migrate."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    planted = _record_an_earlier_build_wrote(cfg, removed, title="Strobe (Michael Woods)")
    assert stores.IDENTITY_SCHEME_FIELD not in planted.payload
    path = stores.tombstones(cfg).path
    before = path.read_bytes()
    assert stores.tombstone_predicate(cfg)(removed)
    assert path.read_bytes() == before, (
        "asking a question rewrote the store, so a question can now fail in a "
        "way that loses somebody's decisions"
    )
    assert stores.summarize(stores.list_tombstones(cfg)[0])[stores.IDENTITY_SCHEME_FIELD] == "", (
        "an era before the stamp is a fact about the record, not a missing field"
    )


def test_a_record_that_names_no_row_matches_no_row(cfg, gates_pass):
    """The row lookup is a lookup on a NAME, and an absent name is not a name."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    nameless = replace(removed, content_id="")
    stores.tombstones(cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist=removed.artist, title="Strobe (Woods)"),
        payload={"content_id": "", "recorded": removed.recorded},
        actor="cli",
    )
    assert not stores.tombstone_predicate(cfg)(nameless)


@pytest.mark.parametrize(
    "stored, spelled",
    [
        pytest.param(None, "None", id="json-null"),
        pytest.param(True, "True", id="json-true"),
        pytest.param(False, "False", id="json-false"),
    ],
)
def test_a_record_naming_nothing_is_not_a_record_naming_the_string_of_nothing(
    cfg, gates_pass, stored, spelled
):
    """``str(None)`` is ``'None'``, and this module has now fixed that at four doors."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    stores.tombstones(cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist=removed.artist, title="Strobe (Woods)"),
        payload={"content_id": stored, "recorded": removed.recorded},
        actor="cli",
    )
    assert not stores.tombstone_predicate(cfg)(replace(removed, content_id=spelled)), (
        "a record that names no row retired a row whose identifier happens to be "
        "the text that value stringifies to"
    )


def test_the_row_lookup_reads_two_composition_forms_of_one_path_as_one_path(cfg, gates_pass):
    """macOS hands out NFD and rekordbox stores NFC, so this is the ordinary case."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    composed = "/Volumes/Music/Café Track.flac"
    decomposed = "/Volumes/Music/Café Track.flac"
    assert composed != decomposed
    stores.tombstones(cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist=removed.artist, title="Strobe (Woods)"),
        payload={"content_id": removed.content_id, "recorded": decomposed},
        actor="cli",
    )
    assert stores.tombstone_predicate(cfg)(replace(removed, recorded=composed)), (
        "one path spelled two ways read as two rows, so a completed deletion is "
        "unrecognisable and its row holds the whole queue"
    )


def test_a_revoked_tombstone_still_says_a_run_recorded_this_deletion(cfg, gates_pass):
    """The question is "did a run record this", not "is this suppressed today"."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    record = stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")
    stores.revoke_tombstone(cfg, record.suppression_id, actor="cli")
    assert stores.list_tombstones(cfg) == (), "the revocation did not take"
    assert stores.tombstone_predicate(cfg)(removed), (
        "revoking a tombstone re-opened a removal that was finished business"
    )


def test_the_stamp_field_is_spelled_on_disk_and_not_only_in_this_build(cfg):
    """A persisted field name is a wire format, so it is pinned to a literal."""
    assert stores.IDENTITY_SCHEME_FIELD == "identity_scheme"


def test_the_stamp_this_build_writes_is_pinned_to_a_literal():
    """The VALUE is a wire format too, and a literal is the only way to see it move."""
    assert stores.identity_scheme() == "is2_5b356bbb451de9cc"


def test_the_row_identity_composes_NFC_and_the_normal_form_is_pinned():
    """The normal form is a WIRE FORMAT, so it is pinned to a literal like the stamp."""
    composed = "Café Track.flac"
    decomposed = "Café Track.flac"
    assert composed != decomposed
    identity = tombstone.removed_file_identity(content_id="1", recorded=decomposed)
    assert identity["recorded"] == composed, (
        "the row identity is not composed to NFC, so a decline recorded under one "
        "spelling of a path is orphaned when the collection reports the other"
    )
    assert tombstone.removed_file_identity(content_id="1", recorded=composed) == identity


def test_the_stamp_is_the_same_value_in_a_process_that_is_not_this_one():
    """It is written to a disk and compared by a LATER process, so it must not vary."""
    seeds = ("0", "1", "12345", "99999")
    children = [
        subprocess.Popen(
            [
                sys.executable,
                "-c",
                "from cratekit.deletion import stores; print(stores.identity_scheme())",
            ],
            stdout=subprocess.PIPE,
            text=True,
            env={**os.environ, "PYTHONHASHSEED": seed, "PYTHONPATH": str(SRC_ROOT)},
        )
        for seed in seeds
    ]
    answers = set()
    for child in children:
        out, _err = child.communicate(timeout=120)
        assert child.returncode == 0
        answers.add(out.strip())
    assert answers == {stores.identity_scheme()}, (
        f"the stamp depends on the process hash seed: {answers}"
    )


def test_the_stamp_reaches_every_rule_by_walking_rather_than_by_a_list():
    """The membership of what the stamp covers is COMPUTED, and this pins the result."""
    reached = stores._composition_rules()
    for name in (
        "cratekit.core.tombstone.VERSION_WORDS",
        "cratekit.core.tombstone._CREDIT_MARKERS",
        "cratekit.core.tombstone.REMIX_DESIGNATION",
        "cratekit.core.tombstone._SPACING",
        "cratekit.core.tombstone._BRACKETED",
        "cratekit.core.tombstone._BRACKET_CHARACTERS",
        "cratekit.core.tombstone._WORD_SPLIT",
        "cratekit.deletion.library._VERSION_COLUMNS",
    ):
        assert f"value:{name}" in reached, f"the walk stopped reaching {name}"
    for name in (
        "cratekit.core.tombstone.fold",
        "cratekit.core.tombstone._already_carries",
        "cratekit.core.tombstone._is_a_credit",
        "cratekit.core.tombstone._as_a_bracketed_value",
        "cratekit.core.tombstone.already_spelled_as_a_remix",
        "cratekit.core.tombstone.reads_as_version",
        "cratekit.core.tombstone.remixer_title",
        "cratekit.core.tombstone.version_title",
        "cratekit.core.tombstone.version_identity",
        "cratekit.deletion.library._version_of",
        "cratekit.deletion.library._text",
        "cratekit.deletion.stores.version_of",
    ):
        assert f"code:{name}" in reached, f"the walk stopped reaching {name}"
    # AND THE VOCABULARY IS IN THERE AS ITS MEMBERS rather than as a name, since
    # a digest that recorded only "there is a frozenset here" would be exactly
    # the round 10 defect wearing a new shape.
    encoded = json.dumps(reached["value:cratekit.core.tombstone.VERSION_WORDS"])
    assert "extended" in encoded and "remix" in encoded


def test_the_walk_reads_what_is_composed_and_not_what_is_raised():
    """The one narrowing in the walk, with the measurement that bought it."""
    reached = stores._composition_rules()
    strayed = [name for name in reached if ".cause." in name or ".exit_codes." in name]
    assert strayed == [], f"the walk read the refusal path: {strayed}"
    composed = reached["code:cratekit.core.tombstone.version_identity"]
    assert "raise" in composed and "if not folded_artist and (not folded_title):" in composed, (
        "the refusal guard is not in the digested source, so a build that stopped "
        "refusing an empty identity would carry its predecessor's stamp"
    )


def test_prose_is_not_a_rule_and_a_reordered_call_is():
    """What the normalisation buys, driven on the two edits that bracket it."""
    source = inspect.getsource(tombstone.fold)
    assert '"""' in source, "the fixture below assumes fold carries a docstring"
    reworded = stores._normalised_source(tombstone.fold)
    assert '"""' not in reworded and "NFC first, then case" not in reworded, (
        "the docstring survived into the digested form, so rewording it moves "
        "the stamp and every record ever written falls to the row lookup"
    )
    assert "casefold" in reworded and "normalize" in reworded, (
        "the code did not survive into the digested form, so the stamp is vacuous"
    )


def test_a_record_of_another_kind_does_not_answer_the_tombstone_question(cfg, gates_pass):
    """The kind is recognised POSITIVELY, so a record of another kind decides nothing."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    stores.tombstones(cfg).record(
        kind=tombstone.KIND_REMOVED_FILE,
        identity=stores.row_identity(removed),
        payload={"content_id": removed.content_id, "recorded": removed.recorded},
        actor="cli",
    )
    assert not stores.tombstone_predicate(cfg)(removed), (
        "a record that is not a tombstone answered the tombstone question, so a "
        "confirmed removal is retired against a decision nobody made about it"
    )


def test_a_row_that_cannot_be_identified_is_not_read_as_already_recorded(cfg, gates_pass):
    """B4 from the round 9 verification, carried and closed."""
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")
    anonymous = replace(removed, artist="", title="", version="", content_id="9")
    with pytest.raises(CratekitError):
        stores.version_of(anonymous)
    assert not stores.tombstone_predicate(cfg)(anonymous), (
        "a row nobody can identify reads as already recorded, so a confirmed "
        "removal is retired for a file somebody merely renamed"
    )


def test_nothing_reconstructs_a_former_builds_composition_any_more(cfg):
    """The claim stated as a SHAPE, because the round 10 version stated it as three names."""
    # OUR rules, which is what can drift.
    composition = {name for name in stores._composition_rules() if not name.startswith("foreign:")}
    assert len(composition) > 20, "the walk collapsed, so the assertions below are vacuous"
    strayed = set(stores._rules_reachable_from(stores._row_coordinates)) & composition
    assert strayed == set(), (
        f"the history answer now reaches composition rules, so it drifts with "
        f"them exactly as four rounds of reconstruction did: {sorted(strayed)}"
    )
    doors = set()
    for path in stores._referenced_paths(stores.tombstone_predicate):
        value = vars(stores).get(path[0])
        for step in path[1:]:
            value = getattr(value, step, None)
        # FUNCTIONS ONLY. ``RemovedRow`` is reached too, as the row type in the
        # predicate's own annotation, and naming a type is not consulting a rule.
        if not inspect.isfunction(value):
            continue
        name = f"code:{value.__module__}.{value.__qualname__}"
        if name in composition:
            doors.add(name)
    assert doors == {"code:cratekit.deletion.stores.version_of"}, (
        f"the recogniser consults the composition rules through {sorted(doors)} rather than "
        "through version_of alone, so a second composer decides a question about history"
    )


# The delete.review shell


@pytest.fixture
def review_cli(library_root, gates_pass, monkeypatch):
    """A configured machine the delete.review verb can actually finish on."""
    data = valid_data(
        library_root,
        profile={"name": "full"},
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "pin_validated_on": "2026-08-02"},
    )
    ready = config.from_dict(data)
    _build_disposable_database(Path(ready.library.db_path))
    config.save(ready)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: ready.library.volume_id
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    session.record_acknowledgment(ready, terminal=lambda: True)
    return ready


def test_delete_review_refuses_at_its_explicit_gate(review_cli):
    """First drive discovers the confirm gate and leaves the run resumable."""
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    envelope = json.loads(out)
    assert envelope["resumable"] is True
    assert envelope["cause"]["detail"]["gate"] == "delete.review.confirm"
    assert envelope["cause"]["detail"]["explicit"] is True


def test_delete_review_refuses_an_inline_answer_and_does_not_record_it(review_cli):
    """R34: the same invocation cannot answer the gate it just discovered."""
    code, out, _ = _drive(["--output", "json", "delete", "review"])
    run_id = json.loads(out)["run_id"]
    code, out, err = _drive(
        [
            "--output",
            "json",
            "-d",
            "delete.review.confirm=trash",
            "--run",
            run_id,
            "delete",
            "review",
        ]
    )
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    from cratekit.cli import gates

    assert "delete.review.confirm" not in gates.load(run_id).decisions


def test_delete_review_exits_ok_after_the_recorded_decision(review_cli):
    """The two-act path: refuse, record with an actor, resume, emit a review set."""
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    run_id = json.loads(out)["run_id"]
    code, _, err = _drive(
        ["run", "decide", run_id, "delete.review.confirm", "trash", "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), err
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    envelope = json.loads(out)
    assert envelope["data"]["queue"] == "deletion"
    assert envelope["data"]["items"] == []
    assert envelope["data"]["unresolved"] == 0


def test_delete_review_abort_moves_nothing(review_cli):
    code, out, err = _drive(["--output", "json", "delete", "review"])
    run_id = json.loads(out)["run_id"]
    code, _, err = _drive(
        ["run", "decide", run_id, "delete.review.confirm", "abort", "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), err
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    assert json.loads(out)["outcome"] == "no_op"


def test_delete_review_trashes_a_confirmed_file(review_cli, tmp_path, monkeypatch):
    """The gate is the confirmation: a deletable file lands in the Trash."""
    home = _home(tmp_path)
    monkeypatch.setattr("cratekit.deletion.trash.Path.home", lambda: home)
    music = _music(review_cli, ONE)
    db_path = Path(review_cli.library.db_path)
    handle = rb_writer.open_db(db_path, unlock=False, cfg=review_cli)
    try:
        watermark.WatermarkStore(review_cli).baseline(
            database_identity=library.database_identity(handle), sequence=40, actor="cli"
        )
    finally:
        rb_writer.close_db(handle)
    _write_rows(
        db_path,
        [
            ("1", str(music), True, 50, music.stat().st_size, Path(ONE).stem),
            (
                "2",
                str(Path(review_cli.library.root) / "Music" / TWO),
                False,
                20,
                11,
                Path(TWO).stem,
            ),
        ],
    )
    _music(review_cli, TWO)
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    run_id = json.loads(out)["run_id"]
    code, _, err = _drive(
        ["run", "decide", run_id, "delete.review.confirm", "trash", "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), err
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    assert not music.exists()
    assert any(home.joinpath(".Trash").iterdir()), "the confirmed file never reached the Trash"
    # U60: the whole of what the inline pass owes, asserted through the SHIPPED
    # verb rather than the engine, since nothing queues it and no worker will
    # ever finish it later.
    assert len(stores.list_tombstones(review_cli)) == 1
    assert watermark.WatermarkStore(review_cli).read().sequence >= 50


def _history(cfg) -> Path:
    """A library whose collection already carries one removal nobody has reviewed."""
    music = _music(cfg, ONE)
    _write_rows(
        Path(cfg.library.db_path),
        [("1", str(music), True, 50, music.stat().st_size, Path(ONE).stem)],
    )
    return music


def _fake_trash(tmp_path, monkeypatch) -> Path:
    home = _home(tmp_path)
    monkeypatch.setattr("cratekit.deletion.trash.Path.home", lambda: home)
    return home / ".Trash"


def test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history(
    review_cli, tmp_path, monkeypatch
):
    """R-134, driven through the shipped verb, and what an abort can and cannot undo."""
    trash = _fake_trash(tmp_path, monkeypatch)
    music = _history(review_cli)
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    refused = json.loads(out)
    assert refused["cause"]["detail"]["shown"] == {
        "baselined": True,
        "accepted_as_history": 1,
        "offered": 0,
    }
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, "delete.review.confirm", "abort", "--actor", "a-person"])
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    assert json.loads(out)["outcome"] == "no_op"
    assert music.exists() and not any(trash.iterdir())
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    second = json.loads(out)
    assert second["cause"]["detail"]["shown"] == {
        "baselined": False,
        "accepted_as_history": 0,
        "offered": 0,
        # U243: the disposable database's other row records no location, so the
        # proof excused it, and the screen says how many it excused.
        "ignored, not local files": 1,
    }
    _drive(
        ["run", "decide", second["run_id"], "delete.review.confirm", "trash", "--actor", "a-person"]
    )
    code, out, err = _drive(["--output", "json", "--run", second["run_id"], "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    assert json.loads(out)["data"]["items"] == []
    assert music.exists() and not any(trash.iterdir())


def test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing(
    review_cli, tmp_path, monkeypatch
):
    """Conformance 3's other half: the gate fires on a baseline and a trash answer is OK."""
    trash = _fake_trash(tmp_path, monkeypatch)
    music = _history(review_cli)
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    run_id = json.loads(out)["run_id"]
    _drive(["run", "decide", run_id, "delete.review.confirm", "trash", "--actor", "a-person"])
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    envelope = json.loads(out)
    assert envelope["outcome"] == "ok"
    assert envelope["data"]["items"] == []
    assert music.exists() and not any(trash.iterdir())
    assert stores.list_tombstones(review_cli) == ()


def test_delete_review_prints_the_baseline_to_a_person_not_only_to_json(review_cli):
    """The display half. A context that stopped at the envelope reaches no human."""
    _history(review_cli)
    code, out, err = _drive(["delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    assert "accepted_as_history: 1" in out + err


def test_delete_review_names_a_missing_library_directory(review_cli):
    """Exit 22 is the unmounted-volume sentence, not a traceback."""
    gone = Path(review_cli.library.root) / "not-mounted" / "master.db"
    data = review_cli.to_toml_dict()
    data["library"]["db_path"] = str(gone)
    missing = config.from_dict(data)
    config.save(missing)
    config.reset_cache()
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), err or out
    assert json.loads(out)["cause"]["reason"] == "library-directory-missing"


# Every volume the pass can reach proves its identity, not only the library's

ARCHIVE_ID = "AAAA-1111-the-archive"


def _the_same_file_through_a_rule(cfg):
    """One real file, a REMOVED row on it, and an ACTIVE row on it through a rule."""
    _music(cfg, ONE)
    _baseline(cfg)
    still_referenced = _at(f"{RECORDED_ELSEWHERE}/{ONE}", "active-through-the-rule", usn=45)
    return FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50), still_referenced], usn=51)


def test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """R-44 Open 4 through the door a volume identity can close, driven end to end."""
    db = _the_same_file_through_a_rule(cfg)
    right = [locations.PrefixRule(RECORDED_ELSEWHERE, str(Path(cfg.library.root) / "Music"))]
    found = run.plan(cfg, db, actor="cli", prefix_map=right)
    assert [item.category for item in found.candidates] == [
        candidates.Category.COLLIDES_WITH_ACTIVE_ROW
    ]
    wrong = tmp_path / "Volumes" / "NOT THE ONE"
    wrong.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {wrong: "BBBB-some-other-disk"}, otherwise=cfg.library.volume_id)
    for rule in (
        locations.PrefixRule(RECORDED_ELSEWHERE, str(wrong)),
        locations.PrefixRule(RECORDED_ELSEWHERE, str(wrong), ARCHIVE_ID),
    ):
        with pytest.raises(CratekitError) as excinfo:
            run.plan(cfg, db, actor="cli", prefix_map=[rule])
        assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_the_wrong_directory_on_the_right_volume_is_still_offered_and_is_recorded_as_open(
    cfg, gates_pass, tmp_path
):
    """WHAT THE IDENTITY CANNOT SEE, pinned end to end so it cannot be read as closed."""
    db = _the_same_file_through_a_rule(cfg)
    wrong = tmp_path / "real-but-not-the-one"
    wrong.mkdir()
    found = run.plan(cfg, db, actor="cli", prefix_map=[_identified(cfg, str(wrong))])
    assert found.references.suspect_anchors == (str(wrong),)
    assert [item.category for item in found.candidates] == [candidates.Category.DELETABLE]


def test_a_different_disk_at_a_mapped_target_stops_the_apply_before_any_file_moves(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """R-44 Open 1. The pass wrote to a second volume with no identity asked of it."""
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path)
    home = _home(tmp_path)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    _confirm_all(cfg, run.present(cfg, found))
    _mounts.stand_in(monkeypatch, {volume: "BBBB-a-clone"}, otherwise=cfg.library.volume_id)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert len(list((volume / "Music").glob("Removed *.flac"))) == len(gone)
    assert stores.list_tombstones(cfg, include_revoked=True) == ()
    assert not any((home / ".Trash").iterdir())


def test_a_volume_holding_only_removed_rows_does_not_settle_off_an_empty_mount_point(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """R-51. No active row goes through the anchor, so ``suspect_anchors`` is silent."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    _mounts.stand_in(monkeypatch, {volume: ARCHIVE_ID}, otherwise=cfg.library.volume_id)
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, active=0, volume_id=ARCHIVE_ID)
    home = _home(tmp_path)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    offered = run.present(cfg, found)
    assert len(offered) == len(gone)
    _confirm_all(cfg, offered)
    _empty_the_mount_point(volume)
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert stores.list_tombstones(cfg, include_revoked=True) == (), (
        "twenty deletions were recorded off an empty directory"
    )
    assert watermark.WatermarkStore(cfg).read().sequence == 40


def _identity_that_changes(monkeypatch, cfg, volume, *, on_change=lambda: None):
    """An archive whose identity is right until ``arm`` says otherwise."""
    reads = {"count": 0, "limit": None, "changed": False}

    def identity():
        reads["count"] += 1
        limit = reads["limit"]
        if limit is None or reads["count"] < limit:
            return ARCHIVE_ID
        if reads["count"] == limit:
            if not reads["changed"]:
                reads["changed"] = True
                on_change()
            return ARCHIVE_ID
        return "BBBB-swapped"

    def arm(more: int) -> None:
        reads["limit"] = reads["count"] + more

    _mounts.stand_in(
        monkeypatch, {volume: identity}, otherwise=cfg.library.volume_id, enumerated=()
    )
    return reads, arm


def test_a_disk_swapped_after_the_plan_stops_a_confirmed_move(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The second look, for a file that is there, confirmed, and about to move."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    reads, arm = _identity_that_changes(monkeypatch, cfg, volume)
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, removed=1, volume_id=ARCHIVE_ID)
    home = _home(tmp_path)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    _confirm_all(cfg, run.present(cfg, found))
    arm(1)  # the rebuilt plan, and nothing after it
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert (volume / "Music" / "Removed 0.flac").exists()
    assert stores.list_tombstones(cfg, include_revoked=True) == ()


def test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The review's second finding, and the branch a missing disk actually takes."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    reads, arm = _identity_that_changes(
        monkeypatch, cfg, volume, on_change=lambda: _empty_the_mount_point(volume)
    )
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, volume_id=ARCHIVE_ID)
    home = _home(tmp_path)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    _confirm_all(cfg, run.present(cfg, found))
    # The rebuilt plan, then the look at the top of the loop for the first item.
    arm(2)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    # UNMOUNTED rather than mismatch: the eject took the file's own directory
    # with it, so the recorded volume is nowhere and the probed path is absent.
    assert excinfo.value.cause.reason == "mapped-volume-unmounted"
    assert reads["changed"], "the drive was never ejected, so this proved nothing"
    assert stores.list_tombstones(cfg, include_revoked=True) == (), (
        "files on an ejected drive were recorded as deleted"
    )
    assert watermark.WatermarkStore(cfg).read().sequence == 40


def test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The other permanent act, which has no re-check in front of it at all."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    reads, arm = _identity_that_changes(monkeypatch, cfg, volume)
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, volume_id=ARCHIVE_ID)
    for path in (volume / "Music").glob("Removed *.flac"):
        path.unlink()
    home = _home(tmp_path)
    arm(1)  # the rebuilt plan, and nothing after it
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert watermark.WatermarkStore(cfg).read().sequence == 40


def test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The fourth finding through the whole pass: the rule proves itself, the file does not."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    inner = volume / "Music"
    _mounts.stand_in(
        monkeypatch,
        {volume: ARCHIVE_ID, inner: "BBBB-inner"},
        otherwise=cfg.library.volume_id,
        enumerated=(),
    )
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, removed=3, volume_id=ARCHIVE_ID)
    home = _home(tmp_path)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    _confirm_all(cfg, run.present(cfg, found))
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert excinfo.value.cause.detail["probed"] == str(inner)
    assert len(list(inner.glob("Removed *.flac"))) == 3
    assert not any((home / ".Trash").iterdir())


def test_a_file_under_the_library_root_asks_nothing_of_any_rule_before_it_moves(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The look before the move is for the rule the file went through, and only that."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    volume.mkdir(parents=True)
    reads = {"count": 0}

    def identity():
        reads["count"] += 1
        return ARCHIVE_ID

    _mounts.stand_in(monkeypatch, {volume: identity}, otherwise=cfg.library.volume_id)
    rule = [locations.PrefixRule(RECORDED_ELSEWHERE, str(volume), ARCHIVE_ID)]
    home = _home(tmp_path)
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=rule)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=51)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    _confirm_all(cfg, run.present(cfg, found))
    before = reads["count"]
    report = run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)
    assert len(report.trashed) == 1
    assert reads["count"] == before + 1, "only the rebuilt plan read the mapped volume"


def test_a_rule_nothing_uses_whose_directory_is_absent_does_not_stop_the_pass(
    cfg, gates_pass, tmp_path
):
    """The availability the gate deliberately keeps: identity proved, directory absent."""
    _music(cfg, ONE)
    rule = [_identified(cfg, str(tmp_path / "never-made"))]
    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=rule)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=51)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    assert [item.category for item in found.candidates] == [candidates.Category.DELETABLE]


def test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity(library_root):
    """The join between the config key and the assertion, which no other test crosses."""
    data = valid_data(
        library_root,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "pin_validated_on": "2026-08-02"},
    )
    data["library"]["location_prefix_map"] = [
        {"from": "/mnt/music", "to": "/Volumes/MUSIC", "volume_id": ARCHIVE_ID},
        {"from": "/mnt/volume", "to": "{library.root}/Music"},
    ]
    rules = run._rules(config.from_dict(data), None)
    assert rules == [
        locations.PrefixRule("/mnt/music", "/Volumes/MUSIC", ARCHIVE_ID),
        locations.PrefixRule("/mnt/volume", str(library_root / "Music"), None),
    ]
