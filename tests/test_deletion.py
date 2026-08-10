"""U24: the deletion pass, the proof that gates it, and the watermark that scopes it.

WHAT THIS FILE IS TRYING TO CATCH. Every other suite in this repository is about
work being done. This one is about work being REFUSED, because the failure mode
of a deletion pass is not "it did not run", it is "it ran and took something it
should not have". So most of the assertions below are of the form "no file moved,
and here is the category that says why", and the ones that do move a file assert
afterwards that the file is in the Trash and recoverable rather than gone.

EVERY FIXTURE IS SYNTHETIC OR A DISPOSABLE COPY. The live rekordbox database is
off limits everywhere in this repository and it matters most here: this is the
unit that removes files. The database used below is built from the binding's own
schema in a temporary directory, and every music file is a handful of bytes this
file wrote.

THE FOUR LAYERS, and why the split is not arbitrary:

1. the watermark, with no library at all, because contiguity and re-baselining
   are arithmetic and belong where they can be read;
2. the Trash, against real files on a real filesystem, because the whole point of
   the module is what the operating system does with a rename;
3. the candidate rules, against real files and synthetic rows, because the proof
   is about inodes and sizes and a mocked stat would prove nothing;
4. the pass, against a fake binding for the branches and against a REAL
   disposable database for the claim that nothing in it changes.
"""

from __future__ import annotations

import ast
import errno
import hashlib
import io
import json
import logging
import os
import sqlite3
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.core import config, locations, preflight, rb_writer, review, session, tombstone
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.deletion import candidates, library, run, stores, trash, watermark
from cratekit.write import trees
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


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


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
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
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
    """The binding hands back a query, not a list, and the guarded canary uses it.

    Materialized per call so a caller that walks it and a caller that asks for
    the first row do not consume each other's rows. That is exactly the hazard
    the real binding has, so a fake that quietly avoided it would be a fake that
    passes tests the real one fails.
    """

    def __init__(self, rows):
        self._rows = list(rows)

    def __iter__(self):
        return iter(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def count(self):
        return len(self._rows)


class SpentQuery:
    """A query whose rows can be WALKED once, which is what a raw cursor is.

    ``count()`` keeps answering, because the database can always be asked the
    question again; it is the walk that is spent. That asymmetry is the entire
    shape of the defect this repository has already shipped once, and the fake
    that shipped with U24 could not express it at all: ``FakeDb`` materialized a
    fresh ``FakeQuery`` on every call, so a test that went near the membership
    walk was testing a binding nobody has, and the one input that decides whether
    a playlist-referenced file gets trashed had no guard and no way to write one.
    """

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
    """A binding that answers the five questions the pass asks and nothing else.

    A fake rather than a real database for the branch tests, deliberately. What
    the branches are about is which category a row lands in, and building ten
    libraries to express ten categories would put the interesting part of each
    test behind fifty lines of schema. The real database appears once, below,
    for the claim only a real one can carry: that this pass writes nothing to it.

    ``memberships_walk_once`` and ``memberships_cannot_count`` exist so the two
    ways the membership read can come up short are reachable. They are OFF by
    default, so every other test still describes the binding that behaves.
    """

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


def _content(cfg, name, content_id, *, deleted=False, usn=None, size=11, title=None, isrc=None):
    return FakeRow(
        ID=content_id,
        FolderPath=str(Path(cfg.library.root) / "Music" / name),
        FileSize=size,
        rb_local_deleted=1 if deleted else 0,
        rb_local_usn=usn,
        Title=title if title is not None else Path(name).stem,
        ArtistName=ARTIST,
        ISRC=isrc,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: the watermark
# ═══════════════════════════════════════════════════════════════════════════


def test_a_first_run_baselines_and_a_second_run_does_not(cfg):
    store = watermark.WatermarkStore(cfg)
    assert store.read() is None
    first, baselined = store.baseline(database_identity="db-1", sequence=40, actor="cli")
    assert baselined and first.sequence == 40
    second, again = store.baseline(database_identity="db-1", sequence=90, actor="cli")
    assert not again, "a second baseline would move the position nobody asked to move"
    assert second.sequence == 40


def test_a_rebuilt_library_forces_a_re_baseline_rather_than_silence(cfg):
    """The number is a position in ONE database's sequence space.

    Carried across a rebuild it sits above every sequence the new database will
    issue for a long time, so the pass reports nothing to do forever while
    removals pile up where nobody is looking.
    """
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
def test_a_document_that_is_not_this_document_refuses_rather_than_reading_as_unset(
    cfg, document
):
    """The defect the decision stores shipped, in the file beside them.

    A watermark read as unset re-baselines at TODAY's sequence, which silently
    accepts every removal a person had not yet answered for. Recognizing
    positively field by field is the only thing that tells a corrupt document
    from an absent one, and the version this build writes is READ rather than
    merely stamped.
    """
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
    """A lock beside the document has its inode swapped by a restore.

    Asserted against the declared roles rather than against the paths, because
    the paths are derived from the roles and a check on the string would pass a
    day after somebody moved the entry.
    """
    assert config.state_file("deletion_watermark").snapshot is config.SnapshotRole.COUPLED
    assert (
        config.state_file("deletion_watermark_lock").snapshot
        is config.SnapshotRole.NEVER_RESTORED
    )
    store = watermark.WatermarkStore(cfg)
    assert config.library_coupled_dir(cfg) not in store.lock_path.parents


def test_two_real_processes_advancing_at_once_lose_nothing(cfg, tmp_path):
    """PROCESSES, not threads. The lock is advisory and per file descriptor.

    Each child advances the watermark by one from whatever it reads, twenty
    times. Unlocked, the read-modify-write cycles interleave and the final value
    is far below forty; the rename being atomic does nothing for the cycle around
    it, which is exactly how the decision stores next door lost 122 of 200
    records while every losing call reported success.
    """
    import subprocess

    config.save(cfg)
    script = tmp_path / "advance.py"
    script.write_text(
        "import sys\n"
        "from cratekit.core import config\n"
        "from cratekit.deletion import watermark\n"
        "cfg = config.load()\n"
        "store = watermark.WatermarkStore(cfg)\n"
        "for _ in range(20):\n"
        "    with store._locked():\n"
        "        held = store.read()\n"
        "        store._write(\n"
        "            watermark.Watermark(\n"
        "                database_identity='db-1',\n"
        "                sequence=held.sequence + 1,\n"
        "                recorded=held.recorded,\n"
        "                actor='child',\n"
        "            )\n"
        "        )\n"
    )
    watermark.WatermarkStore(cfg).baseline(
        database_identity="db-1", sequence=0, actor="cli"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    children = [
        subprocess.Popen([sys.executable, str(script)], env=env) for _ in range(2)
    ]
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
        # TWO ROWS ON ONE SEQUENCE, one handled and one not. Advancing to that
        # sequence would skip the unhandled row permanently, because the next run
        # asks for rows STRICTLY above the watermark.
        ([(6, True), (6, False), (7, True)], 5, 5),
        # THE FLOOR IS A FLOOR, and nothing drove it. Every row above walks
        # upward from a floor below the pairs, so ``reached = max(reached,
        # sequence)`` could be written ``reached = sequence`` and no test moved.
        # Here every pair sits BELOW the floor, which is the ordinary shape after
        # a run whose watermark is already past a batch of old removals, and
        # without the clamp the answer is 7: the watermark moves BACKWARD and
        # re-presents removals a person has already answered for. ``advance``
        # clamps again under its lock, which is what made this copy unmeasurable
        # rather than what makes it unnecessary.
        ([(5, True), (7, True)], 100, 100),
    ],
)
def test_the_watermark_stops_before_the_first_sequence_holding_anything_unhandled(
    pairs, floor, expected
):
    assert watermark.contiguous_sequence(pairs, floor=floor) == expected


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: the Trash
# ═══════════════════════════════════════════════════════════════════════════


def test_a_confirmed_file_lands_in_the_trash_and_is_recoverable(tmp_path):
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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

    monkeypatch.setattr(config, "_mkdir_private", refuse_to_create)
    with pytest.raises(CratekitError) as excinfo:
        trash.assert_usable(source, home=home, platform="darwin")
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert source.exists(), "the file must still be there after a refusal"


def test_the_xdg_layout_is_the_specification_shape_and_the_macos_one_is_not(tmp_path):
    """Both platform branches, driven from one machine.

    A platform branch that can only run on its own platform is a branch that
    ships untested, which is why the seam is a parameter rather than a read of
    ``sys.platform`` inside the function.
    """
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
    """A cross-device move is a copy and an unlink wearing a rename's name.

    Driven through the stat seam rather than by mounting a second disk, which is
    why the seam exists: this is the branch that matters most in the module and
    it is the one a machine with one filesystem could otherwise never reach.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: the proof
# ═══════════════════════════════════════════════════════════════════════════


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
    """The 144-file loss, in three spellings, proved by inode rather than by string.

    A string comparison catches the first of these and misses the other two, and
    the two it misses are exactly the ones that cost 144 files: every file that
    sweep deleted was non-ASCII.
    """
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
    # The claim is not "these spellings always collide"; it is that the FILE
    # SYSTEM decides and a string comparison is never consulted. On a folding
    # volume the two spellings open one inode and it is a collision; on a
    # sensitive one they are two files, one of which does not exist.
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

    declined = _categorize(
        cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg)
    )
    assert declined[0].category is candidates.Category.DECLINED

    stores.revoke_decline(cfg, record.suppression_id, actor="cli")
    offered = _categorize(
        cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg)
    )
    assert offered[0].category is candidates.Category.DELETABLE


def test_a_row_with_no_artist_and_no_title_is_never_deletable(cfg):
    """R36 makes the tombstone part of the deletion rather than a consequence.

    Discovering that the tombstone cannot be written AFTER the move would be the
    one window in the whole pass where a failure has already destroyed something.
    """
    _music(cfg, ONE)
    row = replace(_removed(cfg, ONE, "1"), artist="", title="")
    answered = _categorize(
        cfg, [row], _references(cfg, []), identifiable=stores.identifiable
    )
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
    """The deliberate reading, recorded in the module and asserted here.

    The filesystem ANSWERED: this row references no existing file, so it cannot
    be the row that references a file that does exist. Counting it as missing
    evidence would refuse the feature for every library holding one file the user
    moved by hand, which is every library.
    """
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


def _populate(volume: Path, rows) -> None:
    for row in rows:
        target = Path(str(volume) + row.recorded[len(RECORDED_ELSEWHERE) :])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"audio bytes")


def test_a_prefix_rule_whose_target_is_not_there_refuses_rather_than_proving_nothing(
    cfg, tmp_path
):
    """One wrong character in a prefix rule used to delete the completeness proof.

    Measured over fifty rows of each shape. A correct rule indexed fifty. NO rule
    at all left fifty unmapped and refused, correctly. A rule with one character
    wrong produced fifty "the file is missing" answers, an EMPTY reference set,
    ``complete`` true, ``assert_complete`` passing, and every removed row judged
    deletable against a proof about nothing at all. Omitting a rule refused
    loudly while adding a wrong one proceeded silently, which is backwards, and
    the wrong one is the shape that moves files.
    """
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
    """The author's claim that this already refused was false, and it is reachable.

    Nothing about it involves a typo: the rule is exactly right and the disk is
    simply not mounted this afternoon. Every row through it answered
    ``FileNotFoundError``, and every one of those used to read as a file the user
    had moved by hand.
    """
    unmounted = tmp_path / "not-mounted-today"
    references = _references(
        cfg, _elsewhere(3), prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(unmounted))]
    )
    assert len(references.unanchored) == 3 and not references.complete


def test_a_dangling_symlink_is_still_one_missing_file_and_still_does_not_refuse(cfg):
    """The deliberate reading survives, because its own case is genuinely per row.

    A link into the library that points at nothing is a fact about that one row,
    exactly like a file the user moved by hand. The anchor is there, so the
    answer is still "this row references no existing file", and the run proceeds.
    """
    link = Path(cfg.library.root) / "Music" / "Dangling.flac"
    link.symlink_to(Path(cfg.library.root) / "Music" / "Never Existed.flac")
    references = _references(cfg, [_row(cfg, "Dangling.flac", "9")])
    assert references.missing == ("9",) and references.unanchored == ()
    assert references.complete
    candidates.assert_complete(references)


def test_a_folder_the_user_deleted_under_the_root_is_still_served(cfg):
    """The false positive the ANCHOR choice exists to avoid.

    Splitting on the immediate parent directory instead would refuse the whole
    feature for any library where somebody dragged one album folder to the Trash
    in the Finder, which is a real library with a real hole in it and one that
    must still be served. The anchor is the library root, the root is there, so
    these are missing files and the run proceeds.
    """
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
    """``GONE`` is handled, so fusing this one is worse than fusing the other one.

    A dead rule would mark a library's entire removal history as finished
    business, the watermark would pass over all of it, and fixing the rule
    afterwards would bring none of it back.
    """
    row = replace(
        _removed(cfg, ONE, "1"), recorded=f"{RECORDED_ELSEWHERE}/Music/Track 0.flac"
    )
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
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    elsewhere = FakeRow(
        ID="9",
        FolderPath=f"{RECORDED_ELSEWHERE}/Music/Track 0.flac",
        FileSize=11,
        rb_local_deleted=0,
        rb_local_usn=45,
        Title="Track 0",
        ArtistName=ARTIST,
        ISRC=None,
    )
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50), elsewhere], usn=50)

    with pytest.raises(CratekitError) as excinfo:
        run.plan(
            cfg,
            db,
            actor="cli",
            prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(tmp_path / "gone"))],
        )
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
        "excused from the proof is not the same as invisible; a set of rows the "
        "proof does not cover is a claim, and a claim nobody can size is one "
        "nobody can check"
    )


def test_a_tombstoned_row_never_contributes_to_the_reference_set(cfg):
    """The active-row rule, inherited rather than re-implemented.

    A removed row may not claim a location, or a tombstone sitting beside its own
    file would collide with itself and nothing could ever be deleted.
    """
    _music(cfg, ONE)
    references = _references(cfg, [_row(cfg, ONE, "1", deleted=True)])
    assert not references.by_identity


def test_a_recorded_prefix_the_map_covers_resolves_on_both_sides(cfg, library_root):
    """Most active rows in a real library record a volume that stopped existing.

    A resolver without the map resolves zero of 9,919 rows, so the reference set
    is empty and every file in the library reads as unreferenced. That is the
    single most dangerous failure this unit has.
    """
    older = "/an/older/mount"
    rules = [locations.PrefixRule(older, str(library_root))]
    _music(cfg, ONE)
    active = [trees.ContentRow(content_id="9", recorded=f"{older}/Music/{ONE}", deleted=False)]
    references = _references(cfg, active, prefix_map=rules)
    row = replace(_removed(cfg, ONE, "1"), recorded=f"{older}/Music/{ONE}")
    answered = _categorize(cfg, [row], references, prefix_map=rules)
    assert answered[0].category is candidates.Category.COLLIDES_WITH_ACTIVE_ROW


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: the pass
# ═══════════════════════════════════════════════════════════════════════════


def test_a_first_run_presents_nothing_and_records_where_it_started(cfg, gates_pass):
    _music(cfg, ONE)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=7)], usn=40)
    found = run.plan(cfg, db, actor="cli")
    assert found.baselined and found.candidates == ()
    assert found.baselined_over == 1
    assert watermark.WatermarkStore(cfg).read().sequence == 40


def test_a_track_removed_after_the_baseline_is_offered_and_one_before_it_is_not(
    cfg, gates_pass
):
    _music(cfg, ONE)
    _music(cfg, TWO)
    old = _content(cfg, ONE, "1", deleted=True, usn=7)
    db = FakeDb([old], usn=40)
    run.plan(cfg, db, actor="cli")

    fresh = _content(cfg, TWO, "2", deleted=True, usn=50)
    found = run.plan(cfg, FakeDb([old, fresh], usn=50), actor="cli")
    assert [item.row.content_id for item in found.candidates] == ["2"]
    assert found.deletable[0].category is candidates.Category.DELETABLE


def test_the_offered_items_reach_the_review_queue_and_re_offering_is_idempotent(
    cfg, gates_pass
):
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


def _prepared(cfg, *, names=(ONE,), usn=50):
    """A library that has been baselined, with ``names`` removed after that."""
    for name in names:
        _music(cfg, name)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    rows = [
        _content(cfg, name, str(index + 1), deleted=True, usn=usn + index)
        for index, name in enumerate(names)
    ]
    return FakeDb(rows, usn=usn + len(names))


def test_a_confirmed_file_is_trashed_and_leaves_a_tombstone(cfg, gates_pass, tmp_path):
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)

    report = run.apply(cfg, db, actor="cli", home=home)

    assert len(report.trashed) == 1
    assert not (Path(cfg.library.root) / "Music" / ONE).exists()
    assert Path(report.trashed[0].target).read_bytes() == b"audio bytes"
    assert stores.suppressed_version(cfg, artist=ARTIST, title=Path(ONE).stem)
    assert report.watermark.sequence == 50


def test_a_rejected_item_becomes_a_decline_and_the_file_stays(cfg, gates_pass, tmp_path):
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id, review.Verdict.REJECTED)

    report = run.apply(cfg, db, actor="cli", home=home)

    assert report.trashed == () and len(report.declined) == 1
    assert (Path(cfg.library.root) / "Music" / ONE).exists()
    assert len(stores.declines(cfg).suppressions()) == 1
    # THE WATERMARK MAY NOT PASS OVER IT, and the previous version of this test
    # asserted 50 here with a comment blessing the advance. A decline is
    # revocable by R35, so it is suspended business rather than finished, and the
    # watermark is what decides whether the row is ever considered again: passing
    # it would retire the row permanently and leave the revocation below with
    # nothing to reach.
    assert report.watermark.sequence == 40


def test_revoking_a_decline_puts_the_file_back_in_front_of_a_person(
    cfg, gates_pass, tmp_path
):
    """R35's revocability clause, driven through the path the product takes.

    The guard that existed for this called ``_categorize`` directly and never
    reached ``plan``, so it proved the PREDICATE flips and proved nothing about
    whether a revoked file is ever offered again. Both halves of the door are
    asserted here: the watermark that decides whether the row is considered, and
    the review item that decides whether anybody is asked.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    """The cost of revocability, asserted rather than assumed.

    A decline pins the watermark at its own sequence for as long as it stands.
    That is deliberate and it is the reason revoking can work at all, so it is
    written down as behaviour: the pin arrives with the decline and leaves with
    the revocation.
    """
    _music(cfg, ONE)
    row = _removed(cfg, ONE, "1", sequence=50)
    record = stores.record_decline(cfg, row, actor="cli")

    answered = _categorize(
        cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg)
    )
    assert answered[0].category is candidates.Category.DECLINED
    assert not answered[0].handled, "a revocable decision is not finished business"
    assert watermark.contiguous_sequence([(50, answered[0].handled)], floor=40) == 40

    stores.revoke_decline(cfg, record.suppression_id, actor="cli")
    lifted = _categorize(
        cfg, [row], _references(cfg, []), declined=stores.decline_predicate(cfg)
    )
    assert lifted[0].category is candidates.Category.DELETABLE


def test_an_item_nobody_has_answered_holds_the_watermark_where_it_is(cfg, gates_pass, tmp_path):
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    """R37's last sentence. A review item is durable and a library is not.

    Between the confirmation and the move the user re-imported the track, so an
    ACTIVE row now points at the same file. The photograph taken at review time
    said deletable; the library says otherwise, and the library wins.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)

    db.rows.append(_content(cfg, ONE, "99", deleted=False, usn=60))
    report = run.apply(cfg, db, actor="cli", home=home)

    assert report.trashed == ()
    assert [item.category for item in report.refused] == [
        candidates.Category.COLLIDES_WITH_ACTIVE_ROW
    ]
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_run_interrupted_after_trashing_resumes_without_re_offering(
    cfg, gates_pass, tmp_path
):
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)
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
    """Nobody can answer "this file is also an active row's file" with a decision.

    Offering one would train a person to approve things the software has already
    said it cannot prove, which is how a review surface becomes a formality.
    """
    _music(cfg, ONE, body=b"a different length entirely")
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50, size=11)], usn=50)
    found = run.plan(cfg, db, actor="cli")

    assert found.candidates[0].category is candidates.Category.SIZE_MISMATCH
    assert run.present(cfg, found) == ()
    with review.open_store(cfg) as store:
        assert review.count_unresolved(store, queue=review.Queue.DELETION) == 0


def test_an_unreadable_tombstone_store_refuses_before_the_first_file_moves(
    cfg, gates_pass, tmp_path
):
    """R36 makes the tombstone part of the deletion, so it has to be writable first.

    The window between the move and the record is the only place in this pass
    where a failure has already destroyed something, so the store is proved
    readable while nothing has moved.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)

    config.atomic_write_bytes(
        b"[]\n", config.state_path(tombstone.STORE_KEY, cfg)
    )
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    assert excinfo.value.cause.reason == "review-file-unusable"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_move_that_fails_refuses_with_a_cause_rather_than_a_bare_error(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """An unstructured exception reaches the command line as an internal defect.

    S4: every refusal this unit raises has a reserved code and a remediation, or
    the remedy it was carrying is discarded at the process boundary.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)

    def refuse_to_move(path, *, layout):
        raise OSError("read-only file system")

    monkeypatch.setattr(trash, "move_to_trash", refuse_to_move)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=home)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.code is ExitCode.PRECONDITION
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_the_pass_refuses_while_rekordbox_is_open(cfg, gates_pass, monkeypatch):
    """Without it every identity assertion is evaluated against a stale view.

    The natural flow is to remove tracks in rekordbox and then run this, so
    rekordbox is the application most likely to be open.
    """
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
        preflight, "default_identity_provider", lambda: (lambda _path: "SOME-OTHER-ID")
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
    """A BOOLEAN is refused beside a missing value, and that is not fussiness.

    ``int(True)`` is 1 and ``int(False)`` is 0, so a column answering a boolean
    would be read as a real position in the library's sequence space, one it
    never issued. Guessing low re-offers every removal in the library; guessing
    high hides this one forever. Neither is a default this may take.
    """
    blind = FakeRow(ID="9", FolderPath="/x.flac", rb_local_deleted=1, rb_local_usn=value)
    with pytest.raises(CratekitError) as excinfo:
        library.read_collection([blind])
    assert excinfo.value.cause.reason == "removal-sequence-unreadable"


@pytest.mark.parametrize("identity", ["", None], ids=["empty", "absent"])
def test_a_database_that_names_no_identity_of_its_own_refuses(cfg, identity):
    """An unbound watermark is the state where a rebuild reports nothing forever.

    Without the refusal the identity is ``str(None)`` or the empty string, which
    is a perfectly usable dictionary key and a completely wrong one: every
    rebuilt library would share it, so a position measured in a sequence space
    that no longer exists is inherited silently.
    """
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
    """KTD24 binds the gates to DESTRUCTION, not to database writes.

    This verb writes no database row and is the single most destructive thing the
    product does, so it is exactly the verb the acknowledgment exists for.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    _music(cfg, ONE)
    db = FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=50)
    with pytest.raises(CratekitError) as excinfo:
        run.apply(cfg, db, actor="cli", home=tmp_path)
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: against a real disposable database
# ═══════════════════════════════════════════════════════════════════════════


def _fingerprint(path: Path) -> dict[str, str]:
    """Every byte of the database and its sidecars, hashed.

    "No row is created, modified, or deleted" is asserted against the FILE rather
    than inferred from the code, because the whole class of defect it guards is a
    read path that wrote something on the way past.
    """
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
    """Set the collection rows' columns BEFORE the pass ever opens the database.

    Written with raw SQL rather than through the binding, because creating or
    editing a collection row is exactly what this unit may never do, and a test
    that did it through the guarded writer would be exercising a path the unit
    does not have.
    """
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
    """The verification the brief asks for, in the form a suite can carry.

    A run that trashes a file, records a tombstone and advances the watermark,
    against a real binding and a real schema, and the database is byte-identical
    afterwards. KTD15 is the reason the writer's delete prohibition never has to
    be reopened, and this is what makes that claim checkable.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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


# ═══════════════════════════════════════════════════════════════════════════
# Part 6: what a green suite cannot see
# ═══════════════════════════════════════════════════════════════════════════


#: Every module name that would let this package speak to a streaming service.
#: R36's last sentence: deletion never writes to a streaming service, and
#: streaming-service state never triggers a deletion. Asserted over the SOURCE
#: rather than by monkeypatching a client, because the claim is about the whole
#: package rather than about one run of one function.
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
    """Every import in one module that could reach a service. Prefix-matched.

    Prefix-matched so ``requests.adapters`` and ``urllib.request`` are caught by
    the same entry, which is what stops the list needing a line per submodule.
    """
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
    offenders = {
        path.name: _reaches_the_network(path.read_text())
        for path in sorted(PACKAGE_ROOT.rglob("*.py"))
        if _reaches_the_network(path.read_text())
    }
    assert not offenders, f"the deletion package can reach a service: {offenders}"


def test_the_preview_and_the_write_run_the_same_categoriser():
    """A destructive verb whose dry run and real run take different code paths.

    The preview would then be a second implementation that agrees most of the
    time, and the only cases it disagrees on are the ones nobody tested. The
    re-check is asserted to CALL ``categorize`` rather than to re-derive it, by
    reading the syntax tree: a docstring saying it does would satisfy a grep and
    keep satisfying it after every call was deleted.
    """
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
    """A category added later must not join whichever side an ``if`` left it on.

    Derived by iterating the enum rather than listing members, so the next
    category cannot arrive uncovered (P3, P4).
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: the one verb this unit could land
# ═══════════════════════════════════════════════════════════════════════════
#
# R36 says a tombstone is LISTABLE and revocable, and both words are about a
# person. The engine could do both from the day it landed and nothing a user
# could type reached it, which is a requirement met by nobody. The sibling verb
# stays behind the explicit-gate wall; this one never touched it.


def _drive(argv):
    """Run the real dispatcher, the way the conformance suite drives every verb."""
    from cratekit import cli

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


@pytest.fixture
def deletion_enabled(cfg, library_root):
    """The same library, saved to disk under a profile that switches deletion on.

    The suite's own config is ``slim``, which is correct for the engine tests and
    wrong for these: a verb gated on a feature module is not even in the parser
    when its module is off, so an argparse error would be what these assert
    against rather than the verb.
    """
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
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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
    """The revocable half, which no surface offered before this verb existed.

    The lifted record stays in the listing without --all, because the record a
    person just acted on is the one they need to see and a listing that dropped
    it would answer "did that work" with silence.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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


def test_tombstone_list_refuses_an_identifier_that_resolves_in_neither_store(
    cfg, deletion_enabled
):
    code, out, _err = _drive(["--output", "json", "tombstone", "list", "--revoke", "dc_nope"])
    assert code != int(ExitCode.OK)
    assert json.loads(out)["cause"]["reason"] == "review-item-unknown"


# ═══════════════════════════════════════════════════════════════════════════
# Part 6: findings the review accepted, fixed and held
# ═══════════════════════════════════════════════════════════════════════════


def test_a_verdict_does_not_travel_to_whatever_the_row_resolves_to_later(
    cfg, gates_pass, tmp_path
):
    """A person was shown one path, accepted, and a DIFFERENT file was moved.

    The review item's identity deliberately excludes the resolved path, so a
    remount does not throw away a decision somebody already made. The argued cost
    of that exclusion was "asked again after a remount". The real cost was
    larger: edit the volume prefix map between the review and the apply and the
    verdict lands on whatever the row resolves to now, while the file the person
    looked at is still sitting on disk.
    """
    first = tmp_path / "volume-one"
    second = tmp_path / "volume-two"
    for volume in (first, second):
        (volume / "Music").mkdir(parents=True)
        (volume / "Music" / ONE).write_bytes(b"audio bytes")
    to_first = [locations.PrefixRule(RECORDED_ELSEWHERE, str(first))]
    to_second = [locations.PrefixRule(RECORDED_ELSEWHERE, str(second))]

    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=to_first)
    removed = FakeRow(
        ID="1",
        FolderPath=f"{RECORDED_ELSEWHERE}/Music/{ONE}",
        FileSize=11,
        rb_local_deleted=1,
        rb_local_usn=50,
        Title=Path(ONE).stem,
        ArtistName=ARTIST,
        ISRC=None,
    )
    db = FakeDb([removed], usn=50)

    found = run.plan(cfg, db, actor="cli", prefix_map=to_first)
    offered = run.present(cfg, found)
    assert offered[0].payload["path"] == str(first / "Music" / ONE)
    _confirm(cfg, offered[0].item_id)

    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    report = run.apply(cfg, db, actor="cli", home=home, prefix_map=to_second)

    assert report.trashed == ()
    assert [item.row.content_id for item in report.refused] == ["1"]
    assert (second / "Music" / ONE).exists(), "a file the person never saw was moved"
    assert (first / "Music" / ONE).exists()
    assert report.watermark.sequence == 40


def test_a_name_the_filesystem_will_not_take_refuses_for_that_one_file(tmp_path):
    """Errno 63 is a fact about one name, and it used to condemn the whole run.

    A name already at the length limit has no numbered alternative, so the
    exclusive create comes back with a length error rather than a collision. The
    refusal is Scope.ITEM, like running out of numbers is, because the next
    file's name is a different length.
    """
    directory = tmp_path / "trash"
    directory.mkdir()
    name = "n" * 250 + ".flac"
    (directory / name).write_bytes(b"")
    with pytest.raises(CratekitError) as excinfo:
        trash._free_name(directory, name)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.scope is Scope.ITEM


def test_a_disk_that_will_not_take_any_name_still_stops_the_run(tmp_path, monkeypatch):
    """The other side of the same split, asserted so the narrowing did not go too far.

    Out of space, read only, no permission: each of those is about the volume and
    the next file meets it too, so it must leave this function as it arrived and
    reach the caller's run-scoped handler.
    """
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
    """Correct on safety, wrong on granularity, and this is the granularity.

    Aborting on the first unusable name leaves a person with a queue full of
    confirmed items, no files moved, and one reason for all of them.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg, names=(ONE, TWO))
    found = run.plan(cfg, db, actor="cli")
    for item in run.present(cfg, found):
        _confirm(cfg, item.item_id)

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


# ═══════════════════════════════════════════════════════════════════════════
# Part 7: what the second review round found
# ═══════════════════════════════════════════════════════════════════════════


def test_the_reference_set_it_built_is_reported_on_every_run(cfg, gates_pass, caplog):
    """The module docstring sells this as the answer, so it is asserted like one.

    ``missing`` is the tally the proof deliberately does not block on, and a
    tally nothing ever reports is indistinguishable from a tally nobody computes:
    the whole reference set could have come back empty for a configuration reason
    and the run would still have read as clean.
    """
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    db = FakeDb(
        [
            _content(cfg, ONE, "1", deleted=False, usn=44),
            _content(cfg, "Never Existed.flac", "2", deleted=False, usn=45),
        ],
        usn=50,
    )
    with caplog.at_level(logging.INFO, logger="cratekit.deletion.run"):
        run.plan(cfg, db, actor="cli")

    said = [record.getMessage() for record in caplog.records if "reference set" in record.getMessage()]
    assert said, "the pass no longer reports the reference set it built"
    assert "'indexed': 1" in said[0] and "'missing': 1" in said[0]


def test_an_anchor_that_answered_nothing_is_named_in_a_warning(cfg, gates_pass, tmp_path, caplog):
    """The all-or-nothing version of this was silenced by ONE unrelated good row.

    Its whole reason for existing is a prefix rule pointing at an existing but
    wrong directory, which is the case where the rest of the library resolves
    perfectly well, so a warning keyed on the global set being empty could never
    fire for it.
    """
    wrong = tmp_path / "real-but-not-the-one"
    wrong.mkdir()
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    elsewhere = FakeRow(
        ID="9",
        FolderPath=f"{RECORDED_ELSEWHERE}/Music/Track 0.flac",
        FileSize=11,
        rb_local_deleted=0,
        rb_local_usn=45,
        Title="Track 0",
        ArtistName=ARTIST,
        ISRC=None,
    )
    db = FakeDb([_content(cfg, ONE, "1", deleted=False, usn=44), elsewhere], usn=50)

    with caplog.at_level(logging.WARNING, logger="cratekit.deletion.run"):
        found = run.plan(
            cfg,
            db,
            actor="cli",
            prefix_map=[locations.PrefixRule(RECORDED_ELSEWHERE, str(wrong))],
        )

    assert found.references.by_identity, (
        "this library indexes a row, which is what silenced the previous warning"
    )
    warned = [record.getMessage() for record in caplog.records if record.levelno >= logging.WARNING]
    assert warned, "an anchor that proved nothing went unmentioned"
    assert str(wrong) in warned[0]


def test_a_prefix_target_that_exists_but_is_wrong_is_flagged_and_does_not_refuse(cfg, tmp_path):
    """THE HOLE THE ANCHOR SPLIT DOES NOT CLOSE, pinned so it cannot widen quietly.

    The check asks whether the anchor IS THERE. It cannot ask whether it is
    RIGHT, so a rule aimed at an existing but wrong directory still produces an
    empty index under it, ``complete`` still true. The residual finding
    "Five findings the U24 review accepted, and the reason each stands"
    in the residual findings
    carries the reasoning: every rule that refuses on this needs a threshold, and
    every threshold that catches it also refuses a rule that legitimately matches
    a handful of rows whose files the user moved by hand.

    What IS asserted is that the signal is there, per anchor, with the rest of
    the library resolving normally beside it.
    """
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
        "not asserted as safe"
    )


def test_an_anchor_with_one_missing_row_and_one_good_row_is_not_suspect(cfg):
    """The other side of the same rule, so the signal is not simply "any missing".

    A library where one file was moved by hand under a root that indexes
    thousands is the ordinary state of every real library, and a signal that
    fired on it would be a signal nobody reads.
    """
    _music(cfg, ONE)
    references = _references(
        cfg, [_row(cfg, ONE, "1"), _row(cfg, "Never Existed.flac", "2")]
    )
    assert references.missing == ("2",)
    assert references.suspect_anchors == ()


def test_a_volume_that_goes_away_mid_walk_refuses_rather_than_shrinking_the_proof(
    cfg, tmp_path
):
    """The cache has a direction and the unsafe one used to win silently.

    Eject BEFORE the first row through an anchor and every row is unanchored and
    the run refuses, which is right. Eject AFTER and the cached "present" stood,
    so the remaining rows landed in ``missing`` and quietly shrank the set the
    proof is made of. The anchors are re-asked at the end for exactly this.
    """
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
    """``PrefixRule`` right strips its target, so a rule onto "/" stores "".

    The anchor was then the empty string, which stats as absent, so a rule that
    is perfectly valid refused the whole run and named a directory nobody could
    read in the refusal.
    """
    rule = locations.PrefixRule(RECORDED_ELSEWHERE, "/")
    assert rule.target == ""
    references = _references(
        cfg,
        [
            trees.ContentRow(
                content_id="9",
                recorded=f"{RECORDED_ELSEWHERE}/no/such/file.flac",
                deleted=False,
            )
        ],
        prefix_map=[rule],
    )
    assert references.unanchored == () and references.dead_anchors == ()
    assert references.missing == ("9",)


def test_the_library_root_anchor_is_folded_the_way_a_rule_target_is(cfg):
    """One directory, two composition forms, and this project's own worst incident.

    ``PrefixRule`` NFC folds its target in ``__post_init__``; the library root
    arrives raw from configuration. Unfolded, one root spelled NFD and one rule
    target spelled NFC are two cache keys and two stats for one directory, and
    two directories that ARE one compare as different. APFS hides it by
    normalizing on lookup. An exFAT external drive, which is what a mapped music
    volume usually is, does not.
    """
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
    """A revoke that finds nothing to reopen has SUCCEEDED.

    Reproduced before this: the decline was written revoked and the call then
    raised ``review-item-unknown``, naming a queue identifier the user never
    typed, for an item the queue legitimately may not hold after an export and
    re-import or after somebody cleared it themselves.
    """
    _music(cfg, ONE)
    record = stores.record_decline(cfg, _removed(cfg, ONE, "1"), actor="cli")
    assert len(stores.declines(cfg).suppressions()) == 1

    lifted = run.revoke(cfg, record.suppression_id, actor="cli")

    assert lifted.revoked
    assert stores.declines(cfg).suppressions() == ()


def test_a_revoke_that_cannot_reopen_the_item_leaves_the_decline_standing(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The queue is written FIRST, and this is why the order is the design.

    There is no transaction across the two files, so one of the intermediate
    states is reachable and the only question is which. Store first left the bad
    one: the decline lifted, the item still REJECTED, and the very next apply
    re-recording the decline, so a failed revoke ended as one standing decline
    with no trace anybody had tried. Queue first leaves the harmless one.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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


def test_a_trash_directory_that_is_the_problem_is_not_blamed_on_one_name(
    tmp_path, monkeypatch
):
    """ENAMETOOLONG and EINVAL can be facts about the DESTINATION, not the name.

    Attributing those to the name would report one item scoped skip per confirmed
    file, hundreds of them, each blaming a track, while the one true sentence
    about the Trash is never said.
    """
    absent = tmp_path / "no-such-trash"

    def too_long(*args, **kwargs):
        raise OSError(errno.ENAMETOOLONG, "file name too long")

    monkeypatch.setattr(os, "open", too_long)
    with pytest.raises(OSError) as excinfo:
        trash._free_name(absent, ONE)
    assert excinfo.value.errno == errno.ENAMETOOLONG, (
        "a fact about the Trash was converted into an item scoped skip about a track"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Part 8: the round-three findings
#
# Every assertion below was written because the guard it covers survived a
# mutation. The suite was green at 3281 with each of these guards deleted, which
# is the state the file header calls the one a green suite cannot see: the code
# was right and nothing was holding it there.
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refusal_naming_a_dead_anchor_says_which_directory_to_mount(cfg, tmp_path):
    """Open 5's remediation in the residual finding
    "Five findings the U24 review accepted, and the reason each stands",
    which nothing asserted.

    The refusal carries STEPS naming the directory to mount or the rule to
    correct, and the whole point of them is that a two drive library with the
    archive drive unplugged is one act away from a run that works. With the
    ``steps`` expression deleted the suite stayed green at 3281, and the user met
    a refusal naming thousands of unprovable rows whose only remedy was "run
    doctor", which is the wall the steps were added to remove.
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
    # AND IT REACHES A PERSON. The steps are only remediation if the renderer
    # prints them, so the assertion goes through the real renderer rather than
    # stopping at the cause.
    from cratekit.cli import render

    assert any(str(typo) in line for line in render.render_cause(excinfo.value.cause))


def test_a_refusal_with_no_dead_anchor_offers_no_directory_to_mount(cfg):
    """The other branch, which is what stops the step being unconditional.

    An unmapped prefix has no anchor to name, so a step reading "mount the volume
    holding " with nothing after it would be worse than no step: it would look
    like an instruction and name nothing. The conditional is the guard and this
    is the half that pins it.
    """
    active = [trees.ContentRow(content_id="9", recorded="/nowhere/known/x.flac", deleted=False)]
    references = _references(cfg, active)
    assert references.dead_anchors == ()
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    assert excinfo.value.cause.remediation.steps == (), (
        "a refusal with no dead anchor offered a step naming an empty list of "
        "directories, which reads as an instruction and names nothing"
    )
    assert excinfo.value.cause.remediation.remedy is Remedy.RUN_DOCTOR


# ── F3: the version-bearing column, and the identity that was not unique ──────


def _remixed(cfg, name, content_id, *, title, version, sequence=10):
    return replace(
        _removed(cfg, name, content_id, sequence=sequence), title=title, version=version
    )


def test_two_remixes_filed_under_one_title_are_two_tombstones(cfg):
    """The identity collision, in the shape a remix-heavy library actually holds.

    rekordbox has a dedicated ``RemixerName`` column, so the ORIGINAL and a remix
    routinely arrive with the same bare ``Title``. Keyed on artist and title
    alone they are ONE identity, so deleting the remix reported the original
    suppressed and never re-acquired it. That is over-suppression, which this
    module's own docstring calls the worse direction.
    """
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
    """The legitimate case the composition must not break.

    One library holds both conventions: the same collection has ``Strobe`` with
    the remixer in its own column and ``Strobe (Michael Woods Remix)`` with the
    column filled in as well. Appending unconditionally would give those two rows
    two identities, so a re-import under the other convention would walk straight
    past its own tombstone.
    """
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
    """``RemixerName`` first, ``Subtitle`` second, and never both joined.

    Two columns describing one mix would otherwise compose a title carrying it
    twice, which is a second identity for one version.
    """
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
    """``_text`` defaults, so a binding without the column is "" rather than a raise.

    The right default HERE and the wrong one for the soft-delete marker: an
    absent mix name leaves the identity exactly as wide as it was, while an
    absent marker would decide whether a row is somebody's music.
    """
    bare = FakeRow(
        ID="1",
        FolderPath=str(Path(cfg.library.root) / "Music" / ONE),
        FileSize=11,
        rb_local_deleted=1,
        rb_local_usn=50,
        Title="Strobe",
        ArtistName=ARTIST,
        ISRC=None,
    )
    seen = library.read_collection(FakeQuery([bare]))
    assert seen.removed[0].version == ""
    assert stores.version_of(seen.removed[0])["title"] == "strobe"


def test_the_real_binding_answers_the_version_columns_too(cfg, real_db):
    """The adapter joint for the two columns F3 added, against the real schema.

    A reader that asks for a name the binding does not answer would return "" for
    every row and re-open the collision silently, which is exactly the shape the
    fake above cannot catch. It is a real hazard here rather than a formality:
    ``RemixerName`` is not a column at all, it is an association proxy over
    ``RemixerID`` into ``djmdArtist``, exactly as ``ArtistName`` already is, so
    the rows are written the way rekordbox writes them and the reader is asked
    the question it will really be asked.
    """
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
    """The derivation fault, told apart from the queue legitimately not holding it.

    ``review-item-unknown`` arrives for both, and the caller read it as the
    second one. If the derivation ever drifts, the queue holds the item under a
    different identifier, the clear misses it, the decline is lifted, the
    REJECTED verdict is still armed, and the next apply re-records the decline.
    The only trace was an INFO line saying the revocation stands.

    DRIVEN THROUGH ``run.revoke`` rather than by calling the check directly. A
    test that calls the helper proves the helper works and says nothing about
    whether anything calls it, which the mutation demonstrated: deleting the call
    site killed nothing at all.
    """
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
        kind=run.REVIEW_KIND,
        identity={"content_id": "1"},
        payload={},
        actor="cli",
    )
    with pytest.raises(CratekitError) as second:
        run.revoke(cfg, bad_identity.suppression_id, actor="cli")
    assert second.value.cause.reason == "internal-error"


def test_a_decline_the_queue_simply_does_not_hold_is_still_addressable(cfg, gates_pass):
    """The legitimate case, which the check above must not refuse.

    An export and re-import, a ``review.clear`` somebody ran themselves, or any
    pruning leaves a decline whose review item is gone. Nothing is holding the
    file shut, which is the state the revoke exists to reach, so it succeeds.
    """
    _music(cfg, ONE)
    record = stores.record_decline(cfg, _removed(cfg, ONE, "1"), actor="cli")
    run._assert_addressable(stores.declines(cfg).suppressions()[0])
    lifted = run.revoke(cfg, record.suppression_id, actor="cli")
    assert lifted.revoked and stores.declines(cfg).suppressions() == ()


# ── F5: the assertion the re-check dropped ───────────────────────────────────


def _decline_between_the_plan_and_the_move(cfg, monkeypatch, row):
    """Record a decline in the window apply's re-check is supposed to cover.

    **ON THE SECOND CALL, AND THE COUNT IS THE WHOLE TEST.** ``apply`` reads
    ``playlist_referenced`` twice: once inside the plan it rebuilds, and once
    afterwards, immediately before it snapshots the declines. Firing on the FIRST
    call lands inside the plan, so the plan's own predicate sees the decline, the
    candidate is DECLINED before the loop ever starts, and the test passes through
    a branch that has nothing to do with the re-check. That is exactly how it was
    written first, and the mutation caught it: deleting the re-check's ``declined``
    argument killed nothing. Firing on the second call lands after the plan and
    before the snapshot, which is the only window the finding is about.
    """
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
    """``recheck`` re-runs EVERY assertion, and this is the one it was missing.

    ``apply`` passed no ``declined`` predicate, so the parameter fell back to one
    answering False for every row: the re-check read "no decline is recorded"
    rather than asking. Adding the argument back killed zero tests, so neither
    behaviour was pinned and the missing assertion was absence read as evidence
    of absence, in the function whose docstring says it is not a smaller version
    of the plan.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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
    """The legitimate case, pinned beside the guard above.

    A guard made too restrictive is a defect in this project in the same class as
    the hole it closes, so the ordinary confirmed removal is asserted to still
    move with the predicate wired in.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)

    report = run.apply(cfg, db, actor="cli", home=home)

    assert len(report.trashed) == 1 and report.refused == ()
    assert not (Path(cfg.library.root) / "Music" / ONE).exists()


# ── F6: a trashed file with no tombstone ─────────────────────────────────────


def _tombstone_store_that_will_not_write(monkeypatch, *, raising=None):
    """Break ``record_tombstone`` behind a FLAG rather than by patching and undoing.

    ``monkeypatch.undo`` would also revert the volume identity and process probes
    the gates fixture installed, so a test that needs a working run afterwards has
    to switch the failure off rather than unwind the patch. The suite already
    learned this once, in the revoke test above.

    ``raising`` names a class to raise instead of the store's own refusal, which
    is how the ``BaseException`` shapes are driven. It defaults to None so the
    ordinary refusal is still what the ordinary caller gets.
    """
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
    """R36's worst reachable state, driven and then closed.

    The pre-flight proves the store READABLE, which is not writable: a full disk,
    a volume gone read only, or a lock that cannot be taken all read perfectly.
    So the move could succeed and the record fail, and the exception left the
    gates block with the watermark un-advanced, which LOOKS safe. It is not: the
    next run finds the file absent, answers GONE, GONE is the one member of
    HANDLED, and the watermark passes straight over the row. The file sits in the
    Trash forever with no tombstone and nothing anywhere records that it happened.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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
    """When the undo fails too, the person is told where their file is.

    A store that will not write is an errand. A file in the Trash with no
    tombstone and no way back is a fact about their music, and the only thing
    that helps is both paths, so the refusal is REPLACED rather than chained
    quietly and the original cause rides inside it.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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
    """``MAX_NAME_ATTEMPTS`` raised to 10**9 left the suite green.

    Its own docstring justifies it as the bound that stops the loop spending "an
    unbounded amount of time saying nothing", and nothing tested that half. The
    ceiling is asserted BEFORE the loop is driven, deliberately: a mutation that
    raises the constant would otherwise be discovered by a test that hangs rather
    than by one that fails.
    """
    # THE VALUE, NOT A CEILING OVER IT. This read ``<= 1000``, which pins nothing
    # a mutation cares about: 1000 to 999 satisfies it and the loop assertion
    # below reads the constant itself, so the expectation moved with the defect
    # and the pair could not fail. A test that cannot fail is worse than no test,
    # because the row it occupies reads as covered.
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
    # NOT THE PIN, AND IT IS WORTH SAYING SO OUT LOUD. This reads the constant
    # under test, so it holds the loop to whatever the constant says and holds
    # the constant to nothing. The literal ceiling asserted at the top of this
    # test is the only thing pinning the number itself, and the pair is sound
    # only while both are here. Deleting the literal because "the other one
    # covers it" restores exactly the defect this test was written for.
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
    ids=[
        "windows-backslash",
        "windows-slash",
        "percent-encoded-location",
        "upper-case-scheme",
    ],
)
def test_a_row_that_is_a_path_this_build_cannot_name_refuses(cfg, recorded):
    """The worst shape this unit has, closed from inside U24's own consumer.

    ``resolve_recorded_path`` answers NOT_A_PATH for anything without a leading
    slash, which is right on macOS and excuses every ``C:\\`` row on Windows. The
    reference set then comes back EMPTY, ``complete`` is true, and every removed
    row is proved unreferenced against nothing at all. The percent-encoded case
    is the same hole by another door: ``core.locations`` ships the decoder for
    the two ``file://`` spellings and the reader never routes anything through it.
    """
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
        "the tally the refusal reports is not the tally it refused on, so a "
        "person reading the detail is told a different number from the one that "
        "stopped the run"
    )
    assert excinfo.value.cause.remediation.steps


def test_a_genuinely_streamed_library_still_runs(cfg):
    """The case the excusal exists for, which the refusal above must not break.

    A library that has ever streamed anything holds pseudo-locations, and
    counting those against completeness would refuse the whole feature for it.
    The split is on whether the value looks like a path, not on how many rows
    were excused, so there is no threshold here to tune wrong.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Round 4: what the last round over-restricted, and what an identity is
# ═══════════════════════════════════════════════════════════════════════════

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
    """THE REGRESSION THE UNNAMEABLE SPLIT INTRODUCED, in every scheme that hits it.

    The split asked ``locations.looks_like_location``, which is ``"://" in
    value``, so every one of these landed in ``unnameable``, made ``complete``
    false, and refused the whole destructive verb at RUN scope with the step "run
    this on the machine and platform the library was recorded on". A streamed row
    can never satisfy that step and no configuration change clears it, so one
    such row in a library turned deletion off permanently.

    A pseudo-location references no file, which is the entire argument for
    excusing it, and the argument does not care whether it is spelled with a
    scheme. Only ``file`` names a file.
    """
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


@pytest.mark.parametrize(
    "interrupt", [KeyboardInterrupt, SystemExit], ids=["ctrl-c", "sigterm"]
)
def test_an_interrupt_during_the_store_write_still_puts_the_file_back(
    cfg, gates_pass, tmp_path, monkeypatch, interrupt
):
    """The undo caught ``Exception``, and the likeliest failure here is not one.

    The store write takes a sibling lock, which is the slowest thing in the pass
    and therefore exactly where a Ctrl-C lands. ``KeyboardInterrupt`` and the
    ``SystemExit`` a SIGTERM handler raises are both ``BaseException``, so both
    walked straight past the undo: the original path was gone, the Trash held the
    audio, no tombstone existed, and the next run answered GONE, which is the one
    member of HANDLED, so the watermark retired the only row that could ever have
    said so. ``trash.move_to_trash`` already caught ``BaseException`` for the
    identical window one file over.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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
    """The containment short circuit was a PLAIN SUBSTRING TEST on folded text.

    So a version appearing anywhere in the title at all was dropped out of the
    identity: ``Live`` was "already carried" by ``Lively Up`` and ``Extended`` by
    ``Extended Play Track``. Two rows of one recording, one with the column empty
    and one with it filled in, then produced ONE identity, and recording the
    second suppressed the first. That is over-suppression, which this module's
    own docstring calls the worse direction, and it is the defect round 3 claimed
    to close.
    """
    plain = _remixed(cfg, ONE, "1", title=title, version="")
    carried = _remixed(cfg, TWO, "2", title=title, version=version)

    assert stores.version_of(plain) != stores.version_of(carried), (
        "the two versions share one identity, so deleting either suppresses both"
    )
    stores.record_tombstone(cfg, carried, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=f"{title} ({version})")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title=title), (
        "the version the person kept is suppressed, and it will never be "
        "offered to them again"
    )


def test_a_remixer_name_inside_the_titles_own_bracket_is_not_composed_twice(cfg):
    """The legitimate case a bracket-only test would have broken.

    ``RemixerName`` is an association proxy into ``djmdArtist``, so it holds an
    ARTIST name and not a mix name: the real row is ``Strobe (Michael Woods
    Remix)`` with ``Michael Woods`` in the column. Requiring the bracketed group
    to EQUAL the version would compose ``Strobe (Michael Woods Remix) (Michael
    Woods)``, which no provider will ever spell, so the tombstone would suppress
    nothing. The group has to CONTAIN the version at word boundaries, which is
    the test that answers yes here and still answers no for ``Live`` inside
    ``Lively``.
    """
    inline = _remixed(cfg, ONE, "1", title="Strobe (Michael Woods Remix)", version="Michael Woods")
    assert stores.version_of(inline)["title"] == "strobe (michael woods remix)"
    stores.record_tombstone(cfg, inline, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)")


def test_a_square_bracketed_mix_name_keeps_its_brackets_which_is_R_19(cfg):
    """Pinned as the CURRENT behaviour, and it is a residual rather than a fix.

    Nothing is folded but case, space and composition form, so ``Track (Live)``
    and ``Track [Live]`` are deliberately two identities. The consequence is that
    a row whose title already carries its mix name in square brackets keeps them,
    and a provider spelling the same version with parentheses does not match it.
    That is under-suppression, the milder direction, and closing it means folding
    punctuation for every identity in the product. Recorded as the residual
    finding "A square-bracketed mix name never matches the provider spelling of the same version".
    """
    bracketed = _remixed(cfg, ONE, "1", title="Sun Path [Nightwave Remix]", version="Nightwave Remix")
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
    """rekordbox's ``Subtitle`` is ID3 ``TIT3`` and holds a label as readily as a mix.

    Believing it on sight wrote an ordinary track's tombstone under ``atlas
    (anjunadeep)``. The consulter is handed a provider's title, which is
    ``Atlas``, so it answered NOT SUPPRESSED: R36 did not work for that row, and
    nothing anywhere reported it, because the tombstone existed and was listable.
    """
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
    """The other direction, which is the collision the Subtitle column exists to close.

    A library that files the mix name in ``Subtitle`` still gets two identities
    for two versions, so narrowing which subtitles are believed may not quietly
    take that back.
    """
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
    # pinned it. It is what an audit reads to see which column value an identity
    # was built out of, which is the first thing to look at when a tombstone
    # missed, and the composed title cannot show it.
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
    """The vocabulary, in both directions, because a word list nothing drives rots.

    A version word is a WORD and not a substring: ``Toolroom Records`` is a
    label and must not read as a version because ``record`` looks like one when
    it is tested with ``in``.
    """
    row = _subtitled(cfg, ONE, "1", title="Atlas", subtitle=subtitle)
    seen = library.read_collection(FakeQuery([row]))
    assert bool(seen.removed[0].version) is believed


def test_a_remixer_name_is_believed_without_reading_as_a_version(cfg):
    """``RemixerName`` is not free text, so the vocabulary must not be applied to it.

    It is an association proxy over ``RemixerID`` into ``djmdArtist``, so a
    non-empty value IS the artist who remixed this, by schema. Real remixer names
    carry no version word at all, and holding that column to the vocabulary would
    collapse every remix in the library back onto its original.

    The BELIEF is unchanged and the SPELLING is the round-five correction. See
    the test below: believing the column and writing its value verbatim into the
    title produced an identity no provider will ever ask about.
    """
    row = _content(cfg, ONE, "1", deleted=True, usn=50, title="Strobe")
    row.RemixerName = "Michael Woods"
    row.Subtitle = ""
    seen = library.read_collection(FakeQuery([row]))

    assert seen.removed[0].version == "Michael Woods"
    assert seen.removed[0].version_kind == library.VERSION_IS_AN_ARTIST


def test_a_bracketed_group_that_merely_contains_the_version_is_not_a_carry(cfg):
    """The match INSIDE the bracketed group is delimited too, and it has to be.

    A group is believed to name the version when it contains it at word
    boundaries, which is what lets ``Michael Woods`` be recognised inside
    ``(Michael Woods Remix)``. Testing plain containment inside the group instead
    would put ``Live`` back inside ``(Lively Up Mix)`` and collapse two versions
    onto one identity again, one bracket further in than the defect that was
    fixed.
    """
    plain = _remixed(cfg, ONE, "1", title="Track (Lively Up Mix)", version="")
    live = _remixed(cfg, TWO, "2", title="Track (Lively Up Mix)", version="Live")
    assert stores.version_of(plain) != stores.version_of(live)
    assert stores.version_of(live)["title"] == "track (lively up mix) (live)"


def test_an_interrupt_while_putting_the_file_back_still_names_both_paths(
    cfg, gates_pass, tmp_path, monkeypatch
):
    """The inner handler takes ``BaseException`` too, and that one converts.

    An interrupt during the recover leaves the file in the Trash with no
    tombstone and no way back, which is the one state in this unit where a person
    has to be told two paths and a manual step. A bare traceback tells them
    neither, so the interrupt becomes this refusal and rides in as its cause.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
    _tombstone_store_that_will_not_write(monkeypatch)

    def interrupted(target, original):
        raise KeyboardInterrupt()

    monkeypatch.setattr(run.trash, "recover", interrupted)

    # CAUGHT AND RE-RAISED AS AN ASSERTION, because an interrupt that escapes
    # here does not fail this test, it ENDS THE PYTEST SESSION, and a mutation
    # measured against a suite that stopped early has measured nothing. This is
    # the shape that turns "the guard is gone" into one named failure.
    with pytest.raises(CratekitError) as excinfo:
        try:
            run.apply(cfg, db, actor="cli", home=home)
        except KeyboardInterrupt as escaped:
            raise AssertionError(
                "the interrupt escaped the undo, so the one state where a person "
                "must be told both paths and a manual step reaches them as a "
                "bare traceback"
            ) from escaped

    cause = excinfo.value.cause
    assert cause.reason == "internal-error"
    assert str(Path(cfg.library.root) / "Music" / ONE) in cause.message
    assert cause.detail["trashed_to"]
    assert cause.remediation.steps and "by hand" in cause.remediation.steps[0]


# ═══════════════════════════════════════════════════════════════════════════
# Part 9: round five, stage one. Data safety.
#
# Every finding below is a file that is lost or a removal that is silently
# retired, which is why they are in their own stage and land before anything
# about string matching. Each one is a reading of ABSENCE AS EVIDENCE OF
# ABSENCE, in a place where the permissive answer moves somebody's music.
# ═══════════════════════════════════════════════════════════════════════════


# ── S1-A: the membership walk is the only thing protecting a referenced file ──


def test_a_membership_walk_that_comes_back_short_refuses_rather_than_freeing_the_file(
    cfg, gates_pass, tmp_path
):
    """The one input in this pass with no assertion on it, driven end to end.

    ``assert_complete`` cannot cover a playlist reference: that proof is over the
    ACTIVE rows and a removed content row is by definition absent from the active
    half, so the membership walk is the only surviving statement that anybody
    still points at the file. An empty answer reads as "no playlist references
    anything", which is the permissive reading, and the file moves.

    The walk here is spent, which is the module's own named hazard: the second
    walk of a database cursor returns nothing at all, and that defect has already
    shipped in this repository once.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    rows = [_content(cfg, ONE, "1", deleted=True, usn=50)]

    # The plan's own walk answers, so the candidate is offered and confirmed
    # exactly as it would be. It is the SECOND walk, the one ``apply`` makes
    # immediately before the move, that comes back empty.
    db = FakeDb(rows, [_membership("1")], usn=50, memberships_walk_once=True)
    found = run.plan(cfg, db, actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.STILL_REFERENCED
    ], "the first walk saw the playlist entry, so the file is spoken for"

    spent = FakeDb(rows, [_membership("1")], usn=50, memberships_walk_once=True)
    for _ in spent.get_playlist_songs():
        pass
    with pytest.raises(CratekitError) as excinfo:
        run.plan(cfg, spent, actor="cli")
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert (Path(cfg.library.root) / "Music" / ONE).exists()


def test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses(cfg, gates_pass):
    """There is no safe default, which is the rule this module already applies twice.

    An unreadable identity refuses and an unreadable update sequence refuses. A
    membership count that cannot be read was the third of the same shape and was
    silently treated as "everything I saw is everything there is".
    """
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
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
    """An HONEST zero is accepted, and only an honest one.

    The guard may not cost the feature to somebody who keeps no playlists. Zero
    declared and zero walked agree; it is a walk that declares nothing at all
    that is refused.
    """
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    found = run.plan(cfg, FakeDb([_content(cfg, ONE, "1", deleted=True, usn=50)], usn=50), actor="cli")
    assert [item.category for item in found.candidates] == [candidates.Category.DELETABLE]


def test_a_playlist_that_claims_the_file_between_the_review_and_the_move_stops_it(
    cfg, gates_pass, tmp_path
):
    """STILL_REFERENCED through ``apply``, which nothing drove before this round.

    The only test touching the category called ``categorize`` directly, so the
    membership argument at the move site was never exercised at all: the re-check
    could have been handed an empty set and the suite would have stayed green.
    Here the person confirms a file no playlist claims, then puts it in a
    playlist, and the move must not happen.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)

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


def test_a_volume_that_goes_away_mid_categorization_refuses_rather_than_retiring(
    cfg, tmp_path
):
    """The identical cache as the reference set's, and MORE at stake in this walk.

    ``reference_set`` re-asks at the end and refuses on any anchor whose answer
    moved, because "the half that wins is the wrong one". ``categorize`` had the
    same cache and never asked, so ejecting a volume partway through left every
    remaining row through that anchor reading ``GONE`` off a stale ``present``.
    ``GONE`` is the single member of ``HANDLED``, so the watermark retires those
    rows, nobody is ever asked, and remounting brings none of them back.
    """
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
    """The half that pins the guard to a MOVING anchor rather than to any anchor.

    An anchor asked twice and answering the same thing both times is the ordinary
    run, and refusing there would take the feature away from everybody.
    """
    volume = tmp_path / "still-mounted"
    volume.mkdir()
    rules = [locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))]
    row = replace(
        _removed(cfg, ONE, "1"), recorded=f"{RECORDED_ELSEWHERE}/Music/Track 0.flac"
    )
    answered = _categorize(cfg, [row], _references(cfg, []), prefix_map=rules)
    assert answered[0].category is candidates.Category.GONE


# ── S1-C: a hand-moved file must not retire a confirmed removal ──────────────


def test_a_file_moved_by_hand_after_the_confirmation_is_recorded_rather_than_retired_silently(
    cfg, gates_pass, tmp_path, caplog
):
    """ABSENCE READ AS EVIDENCE OF ABSENCE, costing a confirmed deletion outright.

    The person confirms, then renames the file in the Finder before the apply
    runs. The file is not where the row names it, so the answer is ``GONE``,
    ``GONE`` is the one member of ``HANDLED``, and the watermark walked straight
    over the row: nothing trashed, no tombstone, and the removal never offered
    again. The file not being where it was is not evidence that THIS LIBRARY
    deleted it, and R36 was quietly false for that row.

    The repair is to complete the deletion rather than to retire it silently or
    to hold it open forever. The person confirmed the removal and the collection
    no longer holds the row, so the deletion happened; the tombstone R36 owes is
    written, the file is not moved because there is nothing at that path to move,
    and the person is told that the suppression exists and can be revoked.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    _confirm(cfg, offered[0].item_id)

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
        "the person is not told which suppression to revoke if they only moved "
        "the file"
    )


def test_a_resumed_deletion_whose_tombstone_was_recorded_is_still_finished_business(
    cfg, gates_pass, tmp_path
):
    """The half the tombstone test may not cost, driven through ``apply``.

    A run that trashed the file, wrote the tombstone and then failed to advance
    the watermark must RESUME rather than re-offer, and the row must retire. That
    is the whole reason ``GONE`` is handled, and holding every gone row open
    would have traded one defect for a pass that never finishes anything.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
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
    """The UNDO of a half done deletion, and it was entirely untested.

    ``recover`` is what puts a file back when the tombstone cannot be written, so
    it runs at the one moment the library is already half changed. Overwriting a
    file the person has since put back at that path would be data loss performed
    by the recovery mechanism, which is the same sentence the Trash's own naming
    rule is written for.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    """The placeholder cleanup, which round four cited as its own precedent untested.

    A free name is claimed with an exclusive create before the rename, so a
    failure between the two leaves an EMPTY file in the person's Trash wearing a
    real track's name, which looks exactly like the file that was supposed to be
    there. The handler takes ``BaseException`` because a Ctrl-C lands in that
    window as readily as an error does.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    """The pre-flight, pinned by what it PREVENTS rather than by the end state.

    Its sibling asserted that the file is still on disk afterwards, which is true
    with the pre-flight and true without it: the undo puts the file back and the
    refusal is the same either way. What only the pre-flight buys is that nothing
    was moved at all, so that is what is asserted, and a move here fails the test
    rather than being quietly repaired.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)

    def nothing_may_move(path, *, layout):
        raise AssertionError(
            f"{path} was moved to the Trash before the tombstone store was "
            f"proved readable, so a store that refuses every write would leave "
            f"the file trashed with nothing recording it"
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
    """The guard is right and it used to have no way out at all.

    Review under one rule, correct the rule, and the verdict is refused for
    naming a different file. That is correct once. But ``review.offer`` leaves a
    RESOLVED item's payload alone, so the item kept the stale path forever and
    every later apply compared the corrected path against it and refused again:
    nothing moved, ever. This is the exact case ``core.tombstone`` says a person
    "would be asked again" after, and they were not. Now the confirmation is
    withdrawn, the item is re-offered under the path the row resolves to now, and
    answering it once completes the deletion.
    """
    first = tmp_path / "volume-one"
    second = tmp_path / "volume-two"
    for volume in (first, second):
        (volume / "Music").mkdir(parents=True)
        (volume / "Music" / ONE).write_bytes(b"audio bytes")
    to_first = [locations.PrefixRule(RECORDED_ELSEWHERE, str(first))]
    to_second = [locations.PrefixRule(RECORDED_ELSEWHERE, str(second))]
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)

    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=to_first)
    removed = FakeRow(
        ID="1",
        FolderPath=f"{RECORDED_ELSEWHERE}/Music/{ONE}",
        FileSize=11,
        rb_local_deleted=1,
        rb_local_usn=50,
        Title=Path(ONE).stem,
        ArtistName=ARTIST,
        ISRC=None,
    )
    db = FakeDb([removed], usn=50)

    found = run.plan(cfg, db, actor="cli", prefix_map=to_first)
    _confirm(cfg, run.present(cfg, found)[0].item_id)

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
    """The scheme test is ANCHORED, and unanchored it refuses a run it must not.

    A row that references no file is excused from the completeness proof, and
    that excusal is the only thing keeping the destructive verb usable for
    anybody who has ever streamed anything. A ``file://`` at the START of a value
    names a real file this build cannot resolve, so it refuses; the same text
    anywhere else in a value that is not a path at all is text.
    """
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
    """R37 proves the file is the file the row NAMED, and zero proves nothing.

    "The row said nothing" and "the row said the file is empty" are kept apart as
    values and are the same fact here: neither can satisfy the size assertion. A
    zero read as a size would let a zero-byte file at the recorded path pass the
    proof, and a zero-byte file at a music path is the shape a truncated copy or
    a placeholder leaves behind.
    """
    empty = Path(cfg.library.root) / "Music" / ONE
    empty.write_bytes(b"")
    for recorded in (0, -1):
        row = _content(cfg, ONE, "1", deleted=True, usn=50, size=recorded)
        seen = library.read_collection(FakeQuery([row]))
        assert seen.removed[0].size is None
        answered = _categorize(cfg, [seen.removed[0]], _references(cfg, []))
        assert answered[0].category is candidates.Category.SIZE_MISMATCH


# ═══════════════════════════════════════════════════════════════════════════
# Part 10: round five, stage two. The version vocabulary.
#
# Two questions were being asked of one word list. BELIEF, "is this Subtitle a
# version at all", which has no syntax to test and whose error rates are
# measured on ``tombstone.VERSION_WORDS``. And SPELLING, "how is this written
# into a title a provider will hand the consulter", which was never asked at all
# for the column that always needs it.
# ═══════════════════════════════════════════════════════════════════════════


# ── S2-D: a tombstone written from RemixerName matched nothing ───────────────


def _remixed_row(cfg, name, content_id, *, title, remixer, usn=50):
    row = _content(cfg, name, content_id, deleted=True, usn=usn, title=title)
    row.RemixerName = remixer
    row.Subtitle = ""
    return library.read_collection(FakeQuery([row])).removed[0]


def test_a_remix_filed_as_a_bare_artist_name_is_spelled_the_way_a_provider_spells_it(
    cfg,
):
    """THE DEEPEST FINDING OF THE ROUND, and the code already knew why.

    ``RemixerName`` is an association proxy into ``djmdArtist``, so it ALWAYS
    holds a bare artist name. Composed verbatim it wrote ``strobe (michael
    woods)``, and a provider spells the same version ``Strobe (Michael Woods
    Remix)``, so the consulter asked for ``strobe (michael woods remix)`` and
    missed. ``_already_carries`` states that exact defect in its own docstring,
    "a spelling no provider will ever produce and therefore a tombstone that
    suppresses nothing", and closed it only for the branch where the title
    already has the bracket. The bare-title branch, which is the normal case,
    composed the same unmatchable string. Every remix the user deleted was
    re-acquirable.
    """
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="Michael Woods")
    assert stores.version_of(row)["title"] == "strobe (michael woods remix)"

    stores.record_tombstone(cfg, row, actor="cli")
    assert stores.suppressed_version(
        cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)"
    ), "the tombstone was written under a spelling no provider will ever produce"
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Strobe"), (
        "deleting the remix suppressed the original"
    )


def test_the_two_conventions_one_collection_holds_now_reach_one_identity(cfg):
    """The same collection holds both spellings, and they used to be two identities.

    ``Strobe`` with ``Michael Woods`` in the column and ``Strobe (Michael Woods
    Remix)`` with the column filled in as well are ONE version of ONE recording.
    Composed verbatim they were ``strobe (michael woods)`` and ``strobe (michael
    woods remix)``, so re-importing under the other convention walked straight
    past its own tombstone. Spelling the artist name closes that too.
    """
    split = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="Michael Woods")
    inline = _remixed_row(
        cfg, TWO, "2", title="Strobe (Michael Woods Remix)", remixer="Michael Woods", usn=51
    )
    assert stores.version_of(split) == stores.version_of(inline)
    assert stores.version_of(split)["title"] == "strobe (michael woods remix)"


def test_a_remixer_the_title_already_names_is_not_given_a_second_bracket(cfg):
    """The test is on the BARE name, not on the spelled one, and it has to be.

    ``Strobe (Michael Woods Extended Remix)`` carries ``Michael Woods`` and does
    not carry ``Michael Woods Remix``. Testing the spelled form would compose a
    second bracket onto a title that already says everything it needs to, which
    is the unmatchable spelling coming back one bracket further out.
    """
    row = _remixed_row(
        cfg, ONE, "1", title="Strobe (Michael Woods Extended Remix)", remixer="Michael Woods"
    )
    assert stores.version_of(row)["title"] == "strobe (michael woods extended remix)"


def test_a_remixer_column_already_holding_a_mix_name_is_not_doubled(cfg):
    """Some importers put a whole mix name in the column, and appending breaks it.

    ``(Michael Woods Remix Remix)`` is a second unmatchable spelling replacing
    the first, so the value is asked whether it already reads as a designation.
    That is the one place the vocabulary touches this column, and it decides
    SPELLING rather than belief: a non-empty remixer is a version either way.
    """
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="Michael Woods Remix")
    assert stores.version_of(row)["title"] == "strobe (michael woods remix)"


def test_an_empty_remixer_column_leaves_the_ordinary_identity_alone(cfg):
    """Most rows. The spelling rule may not move the ordinary case one character."""
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer="")
    assert stores.version_of(row) == tombstone.version_identity(artist=ARTIST, title="Strobe")


# ── S2-E: one identity naming two tracks, and one track with two identities ──


def test_a_featured_credit_bracket_does_not_stand_in_for_the_remix(cfg):
    """Two DIFFERENT tracks reached one identity through the guest credit.

    ``Losing It (feat. Anna)`` with the remixer column empty is the original.
    The same title with ``Anna`` in the column is Anna's remix of it. The credit
    bracket contains the remixer's name at word boundaries, so the version read
    as already carried, nothing was composed, and both rows produced ``losing it
    (feat. anna)``: deleting the remix suppressed the original, which is the
    over-suppression direction this package calls the worse one.
    """
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
    """The docstring said those collisions were unreachable, and named the wrong reason.

    A remixer is an ARTIST, so ``RemixerName`` holds an artist NAME, which is
    exactly "something that is not a mix name": the ``("Sun", "Sun Path")``
    collision it called unreachable was reachable the moment a row credited a
    remixer called Sun Path. Spelling the column closes the collision as well as
    the missed match, and this is the driven half of that claim.
    """
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
    """WIDENING WAS CAUGHT AND NARROWING WAS NOT, which is how a defect walks back.

    Adding ``anjunadeep`` or ``records`` killed tests through the negative pins,
    but 24 of the 27 words could be DELETED one at a time with the whole suite
    green, ``mix`` among them: the tests that need it spell ``Extended Mix``, and
    ``extended`` covers that on its own, and vice versa. A list that can be
    silently emptied is a list nothing pins. This is the assertion that catches
    both directions, and it is deliberately a literal rather than anything
    derived from the module, because a derived expectation moves with the defect.
    """
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
        # One realistic phrase per word that carries the ordinary library. The
        # membership assertion above catches a deletion; these say what each
        # deletion would COST, which is a different thing and worth both.
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
        # A NON-WORD split rather than a whitespace one. ``Re-Edit`` is two words
        # and a whitespace split reads it as one, so the designation is lost and
        # the row keeps a bare title, which is the collision direction.
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
    """The measured failure direction may not be the one place it is invisible.

    56 of 75 genuine version designations do not read as versions, so the row
    keeps a bare title and two versions of one recording can collide. The
    tombstone's payload showed an empty version for that row, which reads exactly
    like a row that never had one, so the audit trail that exists to answer "why
    did this suppression miss" was silent on the commonest reason.
    """
    row = _subtitled(cfg, ONE, "1", title="Atlas", subtitle="Anjunadeep")
    seen = library.read_collection(FakeQuery([row])).removed[0]

    assert seen.version == "" and seen.version_unbelieved == "Anjunadeep"
    written = stores.record_tombstone(cfg, seen, actor="cli")
    assert written.payload["version"] == ""
    assert written.payload["version_unbelieved"] == "Anjunadeep"


# ── S2-F: the dead filter, deleted, and the surviving one pinned ─────────────


def test_a_removal_sitting_exactly_on_the_watermark_is_not_offered_again(cfg, gates_pass):
    """STRICTLY GREATER, and it is now written in exactly one place.

    ``read_collection`` carried the same comparison behind a ``since`` the only
    caller permanently disabled, so one rule was written twice with one copy
    unreachable and neither could be measured. Greater-or-equal here would
    re-offer the last row of every previous run, forever.
    """
    for name in (ONE, TWO):
        _music(cfg, name)
    on_the_mark = _content(cfg, ONE, "1", deleted=True, usn=40)
    above_it = _content(cfg, TWO, "2", deleted=True, usn=41)

    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    found = run.plan(cfg, FakeDb([on_the_mark, above_it], usn=41), actor="cli")
    assert [item.row.content_id for item in found.candidates] == ["2"]


def test_the_collection_walk_hands_back_every_removal_it_saw(cfg):
    """The walk is unfiltered, because the baseline needs the highest sequence.

    The filter needs the baseline and the baseline needs the walk, so the walk
    cannot be filtered at all. That was the reason the parameter was permanently
    disabled, and saying it as a test is what keeps somebody from re-adding one.
    """
    rows = [_content(cfg, ONE, str(index), deleted=True, usn=index) for index in range(1, 6)]
    seen = library.read_collection(FakeQuery(rows))
    assert [row.sequence for row in seen.removed] == [1, 2, 3, 4, 5]


# ═══════════════════════════════════════════════════════════════════════════
# Part 10: round six. The round's own fix, self refuted, and the discriminator
# the residual finding on the Subtitle vocabulary said did not exist.
#
# Every finding below was measured end to end by the round five verifier rather
# than argued, and two of them are the previous round's fixes landing on the
# wrong object: a vocabulary proved wrong in one place and then relied on in
# another, and a hold that closed a silent retirement by wedging the queue.
# ═══════════════════════════════════════════════════════════════════════════


# ── F1: the spelling decision was routed through the vocabulary's own known
#        false positives ───────────────────────────────────────────────────────


#: The artist and label names the vocabulary's measured false-positive set names.
#: Every one of them contains a version word, so ``reads_as_version`` answers
#: True for all six, which is exactly why asking it about a REMIXER was wrong.
_FALSE_POSITIVE_REMIXERS = (
    "Radio Slave",
    "Dub Pistols",
    "Cut Chemist",
    "Mix Master Mike",
    "Club Sweat",
    "Original Gee",
)


@pytest.mark.parametrize("remixer", _FALSE_POSITIVE_REMIXERS)
def test_a_remixer_whose_name_carries_a_version_word_is_still_spelled_matchably(
    cfg, remixer
):
    """THE ROUND'S HEADLINE FIX, SELF REFUTED BY THE TEST IT WAS BUILT ON.

    ``remixer_title`` decided how to spell a remixer by asking
    ``reads_as_version`` about the remixer's NAME. That test's measured false
    positives are, exactly, artist and label names carrying a version word, so
    for every one of them the "already reads as a designation" branch fired and
    the bare name was composed verbatim: ``Screamer`` remixed by Radio Slave
    produced ``screamer (radio slave)`` while a provider spells ``Screamer
    (Radio Slave Remix)``. The round measured that false-positive set and then
    routed the spelling decision through it, applied to a column whose own
    docstring says it ALWAYS holds a bare artist name and therefore never holds a
    designation at all.
    """
    assert tombstone.reads_as_version(remixer), (
        "this row no longer exercises the false positive it was written for"
    )
    row = _remixed_row(cfg, ONE, "1", title="Screamer", remixer=remixer)
    assert stores.version_of(row)["title"] == f"screamer ({remixer.casefold()} remix)"

    stores.record_tombstone(cfg, row, actor="cli")
    assert stores.suppressed_version(
        cfg, artist=ARTIST, title=f"Screamer ({remixer} Remix)"
    ), "the tombstone was written under a spelling no provider will ever produce"


@pytest.mark.parametrize(
    ("remixer", "expected"),
    [
        # THE ONLY VALUES LEFT VERBATIM. The last word is the very word about to
        # be appended, so appending would write it twice.
        ("Michael Woods Remix", "strobe (michael woods remix)"),
        ("Michael Woods Extended Remix", "strobe (michael woods extended remix)"),
        # A designation ending in some OTHER vocabulary word is composed anyway.
        # That is this rule's error class, stated here rather than hidden: the
        # spelling misses, so the deletion does not stick, which is the milder
        # direction. Round six left both of these alone by consulting the
        # vocabulary, and paid for it on every row below.
        ("Michael Woods Dub", "strobe (michael woods dub remix)"),
        ("Extended Mix", "strobe (extended mix remix)"),
        # An ordinary artist name, which is what this column is guaranteed to
        # hold, spelled the way a provider spells it. The last four are the two
        # shapes the two vocabulary rules each got wrong: round five composed
        # ``Radio Slave`` and ``Cut Copy`` verbatim, round six composed ``The
        # Cut`` and ``Todd Terry Live`` verbatim.
        ("Michael Woods", "strobe (michael woods remix)"),
        ("Anna", "strobe (anna remix)"),
        ("Radio Slave", "strobe (radio slave remix)"),
        ("Cut Copy", "strobe (cut copy remix)"),
        ("The Cut", "strobe (the cut remix)"),
        ("Todd Terry Live", "strobe (todd terry live remix)"),
    ],
)
def test_the_only_remixer_left_verbatim_is_one_that_already_says_remix(
    cfg, remixer, expected
):
    """Both halves of the rule in one table, so neither can be moved alone.

    Skipping the append is only ever right when appending would DUPLICATE the
    word being appended. Anything wider is a vocabulary being asked to classify a
    column whose schema already classified it, which is what both previous rounds
    did and what the 65 value measurement below settles.
    """
    row = _remixed_row(cfg, ONE, "1", title="Strobe", remixer=remixer)
    assert stores.version_of(row)["title"] == expected


# ── F7: an identity that is not unique, and the guard that could never fire ───


def test_a_removed_row_with_no_identifier_of_its_own_is_refused_rather_than_named_None(
    cfg,
):
    """``str(None)`` is ``'None'``, which is truthy, so the guard never fired.

    ``removed_file_identity`` refuses an unidentifiable row precisely so that
    "every removed file in the library addresses the same decision" cannot
    happen, and it tested ``not str(content_id)``. A row with no identifier
    therefore produced the identity ``{'content_id': 'None'}``, and that string
    went on to address the review item, the decline, and the membership test.
    """
    with pytest.raises(CratekitError) as excinfo:
        tombstone.removed_file_identity(content_id=None, recorded="/music/x.flac")
    assert excinfo.value.cause.reason == "review-selection-invalid"

    with pytest.raises(CratekitError):
        tombstone.removed_file_identity(content_id="", recorded="/music/x.flac")

    # A NUMERIC identifier is a legitimate identifier and zero is a number. The
    # emptiness test runs on the converted value for exactly this reason.
    assert tombstone.removed_file_identity(content_id=0, recorded="/x")["content_id"] == "0"


def test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable(cfg, gates_pass):
    """The same defect end to end, which is where it actually bites.

    ``read_collection`` did ``str(row.ID)``, so a row with no identifier arrived
    as the perfectly ordinary string ``'None'`` and the guard one module down
    could never see it. Folded to empty instead, it reaches the identity module,
    is refused there, and the pass answers ``UNIDENTIFIABLE`` before anything is
    resolved rather than offering a row that can never be deleted.
    """
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    nameless = _content(cfg, ONE, "1", deleted=True, usn=50)
    nameless.ID = None

    seen = library.read_collection(FakeQuery([nameless]))
    assert seen.removed[0].content_id == "", (
        "a row with no identifier was given the identifier 'None'"
    )

    found = run.plan(cfg, FakeDb([nameless], usn=50), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.UNIDENTIFIABLE
    ]
    assert run.present(cfg, found) == (), (
        "a row that can never be deleted was put in front of a person as deletable"
    )


# ── F6: the predicate wired at review time, unpinned in one of its two sites ──


def test_a_row_that_could_never_carry_a_tombstone_is_not_offered_as_deletable(
    cfg, gates_pass
):
    """``plan``'s ``identifiable`` wiring could be deleted with nothing noticing.

    ``categorize`` defaults the predicate to "every row is identifiable", so
    removing the argument in ``plan`` made ``UNIDENTIFIABLE`` unreachable at
    review time and offered a row whose deletion could never be recorded. The
    sibling wiring in ``apply`` was pinned; this one was the asymmetry.
    """
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    anonymous = _content(cfg, ONE, "1", deleted=True, usn=50, title="")
    anonymous.ArtistName = ""

    found = run.plan(cfg, FakeDb([anonymous], usn=50), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.UNIDENTIFIABLE
    ]
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
    """The indistinguishability claim is false as stated, and this is why.

    The residual finding it belongs to is
    "The Subtitle vocabulary's false negatives collide, and the ISRC tells a collision from a convergence".

    Two versions of one recording whose designations the closed vocabulary does
    not recognise both keep a bare title, so they land on ONE identity and
    deleting either suppresses the other. That is the vocabulary's measured worse
    error direction and the user loses a track they never deleted. That finding
    recorded
    that telling this from a legitimate convergence "needs a signal neither the
    row nor the library carries today". The row carries it: two recordings carry
    two ISRCs.
    """
    for name in (ONE, TWO):
        _music(cfg, name)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    rows = [
        _versioned(cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111",
                   subtitle="Acappella"),
        _versioned(cfg, TWO, "2", usn=51, title="Strobe", isrc="BBBB22222222",
                   subtitle="Refix"),
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
    assert run.present(cfg, found) == (), "a suppression that would take out a second recording was offered"
    assert found.candidates[0].problem


def test_the_convergence_composition_exists_to_produce_is_still_deletable(cfg, gates_pass):
    """The half the discriminator may not cost, and it is the whole point of composing.

    ``Strobe`` with ``Michael Woods`` in the remixer column and ``Strobe (Michael
    Woods Remix)`` with it filled in as well are ONE recording filed under two
    conventions. They land on one identity BY DESIGN. One recording carries one
    ISRC, so the check has to let them through, and a check that refused them
    would take the verb away from a remix-heavy library.
    """
    for name in (ONE, TWO):
        _music(cfg, name)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    rows = [
        _versioned(cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111",
                   remixer="Michael Woods"),
        _versioned(cfg, TWO, "2", usn=51, title="Strobe (Michael Woods Remix)",
                   isrc="AAAA11111111"),
    ]
    found = run.plan(cfg, FakeDb(rows, usn=51), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.DELETABLE,
        candidates.Category.DELETABLE,
    ]


def test_an_absent_isrc_is_read_as_agreement_rather_than_as_a_collision(cfg, gates_pass):
    """The check is inconclusive without a code, and inconclusive means proceed.

    An absent code is not evidence AGAINST the identity's own claim that two rows
    are one version, and refusing on silence would refuse most of a library whose
    metadata is thin. What is refused is a positive statement that the two rows
    are two recordings, which is two codes that are both present and different.
    """
    for name in (ONE, TWO):
        _music(cfg, name)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    rows = [
        _versioned(cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111",
                   subtitle="Acappella"),
        _versioned(cfg, TWO, "2", usn=51, title="Strobe", isrc=None, subtitle="Refix"),
    ]
    found = run.plan(cfg, FakeDb(rows, usn=51), actor="cli")
    assert [item.category for item in found.candidates] == [
        candidates.Category.DELETABLE,
        candidates.Category.DELETABLE,
    ]


def test_the_collision_is_looked_for_across_the_whole_walk_not_the_offered_rows(
    cfg, gates_pass
):
    """The row a candidate collides with is very often one an earlier run retired.

    ``run.plan`` filters removals by the watermark before offering them, and
    asking the FILTERED set would find a collision only when both halves of it
    were removed in the same window. The whole collection walk is already in hand,
    so the question is asked of that.
    """
    for name in (ONE, TWO):
        _music(cfg, name)
    below = _versioned(cfg, ONE, "1", usn=10, title="Strobe", isrc="AAAA11111111",
                       subtitle="Acappella")
    run.plan(cfg, FakeDb([below], usn=40), actor="cli")
    above = _versioned(cfg, TWO, "2", usn=50, title="Strobe", isrc="BBBB22222222",
                       subtitle="Refix")

    found = run.plan(cfg, FakeDb([below, above], usn=50), actor="cli")
    assert [item.row.content_id for item in found.candidates] == ["2"], (
        "the row below the watermark should not be offered"
    )
    assert found.candidates[0].category is candidates.Category.AMBIGUOUS_VERSION, (
        "the colliding row was invisible because it sat below the watermark"
    )


def test_a_confirmed_ambiguous_row_is_refused_at_move_time_too(cfg, gates_pass, tmp_path):
    """The re-check gets the same answer the review was made under.

    ``apply`` rebuilds the plan and re-runs the categoriser per row, so a
    predicate wired into ``plan`` and not into the re-check would let a row
    confirmed before the collision existed walk straight through the guard.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    for name in (ONE, TWO):
        _music(cfg, name)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    alone = _versioned(cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111",
                       subtitle="Acappella")
    db = FakeDb([alone], usn=50)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)

    # The second recording is removed between the confirmation and the move.
    db.rows.append(
        _versioned(cfg, TWO, "2", usn=51, title="Strobe", isrc="BBBB22222222",
                   subtitle="Refix")
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
    """THE HOLD THAT CLOSED A SILENT RETIREMENT WEDGED THE WHOLE QUEUE.

    Holding a confirmed row open until its file comes back is unsatisfiable when
    the person deleted the file rather than moving it, and the watermark is
    CONTIGUOUS, so the row below holds every row above it as well. Row 51 here is
    confirmed, trashed and recorded perfectly, and it was re-walked forever
    because row 50's file could never come back.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg, names=(ONE, TWO))
    found = run.plan(cfg, db, actor="cli")
    for item in run.present(cfg, found):
        _confirm(cfg, item.item_id)

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
    """The scoping is deliberate. The silence was not.

    Nobody answered for this row, so there is no deletion of ours to record and
    re-walking a person's whole removal history forever would do more harm than
    the defect. But if they MOVED the file rather than deleting it, it is still
    on the disk, no longer in the collection, and now no longer reachable by this
    pass either. That is the one state where a file goes quietly out of reach.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    """TWO COMMITS IN ONE ROUND, NEITHER RECORDING THAT THEY INTERACT.

    One made the tombstone the test for whether a confirmed removal whose file is
    absent may be retired. The other changed how a ``RemixerName`` is spelled into
    the identity. Together they say a deletion an earlier build completed, with
    the file in the Trash and the record written, is unrecognisable: the predicate
    computes ``strobe (michael woods remix)`` and the store holds ``strobe
    (michael woods)``. It only bites a store written by an earlier build, which is
    every existing user.
    """
    _music(cfg, ONE)
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    row = _versioned(cfg, ONE, "1", usn=50, title="Strobe", isrc="AAAA11111111",
                     remixer="Michael Woods")
    removed = library.read_collection(FakeQuery([row])).removed[0]

    # THE EARLIER SPELLING IS A LITERAL, AND IT HAS TO BE. This planted the
    # record with ``tombstone.version_title`` until round nine, which is the
    # function the whole backward compatibility surface is about. Both sides
    # moved together, so when round eight changed the composer the record this
    # test plants moved with the build, the test stayed green, and the spelling
    # on real disks did not move at all. A test whose expected value is computed
    # by the code under test cannot see the code under test change.
    #
    # AND THE PAYLOAD IS THE ONE THAT BUILD REALLY WROTE, which round ten
    # corrected. It planted ``payload={}`` here, and no build of this pass has
    # ever written a tombstone that does not say which row it was about, so the
    # fixture described a store nobody has.
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
        "a deletion an earlier build recorded is not recognised, so the row is "
        "held open forever and the person is told to put back a file that is "
        "already in the Trash where they put it"
    )

    # AND THE CONSULT IS NOT WIDENED WITH IT, which is the scope of the whole
    # change. A consulter holds a provider's title and is answered under the one
    # spelling providers use; a record written under a spelling this build has
    # decided is wrong stays unmatched there, and the store is what has to be
    # rewritten for that, not the question.
    assert not stores.suppressed_version(
        cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)"
    )
    assert stores.suppressed_version(cfg, artist=ARTIST, title="Strobe (Michael Woods)")

    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = FakeDb([row], usn=50)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)
    (Path(cfg.library.root) / "Music" / ONE).unlink()
    report = run.apply(cfg, db, actor="cli", home=home)
    assert report.watermark.sequence == 50
    assert len(stores.list_tombstones(cfg, include_revoked=True)) == 1, (
        "the deletion was recorded a second time under the new spelling"
    )


# ── F10: the completeness proof was one sided, and the walk could raise ───────


class UndercountQuery:
    """A query that DECLARES fewer rows than it hands back.

    The mirror of ``SpentQuery``, and the shape a floor comparison accepts in
    silence: the walk is compared against a number the walk did not produce
    precisely so a short walk cannot certify itself, and ``walked < declared``
    then agrees with any number that is short in the other direction.
    """

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
    """Either side of the comparison being wrong is the same fault.

    The number exists to be a statement the walk did not produce. A count that
    UNDERCOUNTS passes a floor comparison in silence, so the one assertion
    protecting a playlist-referenced file is satisfied by a number that proves
    nothing about the walk.
    """
    with pytest.raises(CratekitError) as excinfo:
        library.playlist_referenced(UndercountQuery([_membership("1"), _membership("2")], 1))
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert excinfo.value.cause.detail == {"declared": 1, "walked": 2}


def test_a_membership_walk_that_raises_is_a_refusal_rather_than_a_traceback(cfg):
    """S4: an unstructured exception reaches the command line as an internal defect.

    The count was already taken through a handler that answers "it cannot say".
    The walk was not, so a binding that failed partway through it discarded the
    remedy it should have been carrying.
    """
    with pytest.raises(CratekitError) as excinfo:
        library.playlist_referenced(FailingWalk([_membership("1")], 5))
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"
    assert excinfo.value.cause.detail == {"walked": 1}
    assert "cursor was closed" in excinfo.value.cause.message


def test_a_live_membership_that_names_no_row_refuses_rather_than_freeing_the_file(cfg):
    """A reference this pass cannot address would read as no reference at all.

    ``ContentID`` is folded to empty when it is absent rather than to the string
    ``'None'``, which is right, and empty matches no removed row's identifier. So
    the permissive reading of an unaddressable reference is "no playlist points
    at that file", which is the one answer in this module that moves music.
    """
    with pytest.raises(CratekitError) as excinfo:
        library.playlist_referenced(FakeQuery([FakeRow(ID="m1", ContentID=None,
                                                       rb_local_deleted=0)]))
    assert excinfo.value.cause.reason == "deletion-evidence-incomplete"


# ── Z: two round-four zero rows on the destructive path ──────────────────────


def test_a_trash_directory_this_account_cannot_write_to_is_not_usable(tmp_path):
    """``probe``'s access check could be neutralised with nothing noticing.

    Every other branch of the probe is driven, and the one that asks whether this
    account may actually put a file in the directory was not, so a read-only
    Trash reported usable and the refusal that stands between a confirmed file
    and an unlink never fired.
    """
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
            "a Trash this account cannot write to was reported usable, so the "
            "move would be attempted and the refusal that protects the file "
            "would never be raised"
        )
        assert "not writable" in status.problem
        with pytest.raises(CratekitError) as excinfo:
            trash.assert_usable(music, home=home, platform="darwin")
        assert excinfo.value.cause.reason == "trash-unavailable"
    finally:
        files.chmod(0o700)


def test_a_name_the_filesystem_calls_invalid_costs_one_file_and_not_the_run(
    tmp_path, monkeypatch
):
    """``EINVAL`` could be dropped from the set with the whole suite green.

    Only ``ENAMETOOLONG`` was ever driven through the item-scoped branch, so the
    other two members of the set were carried by the comment beside them. A name
    the filesystem rejects is one file's problem; anything wider stops a pass
    over a thousand good ones.
    """
    directory = tmp_path / "trash"
    directory.mkdir()

    def invalid(*args, **kwargs):
        raise OSError(errno.EINVAL, "invalid argument")

    monkeypatch.setattr(os, "open", invalid)
    with pytest.raises(CratekitError) as excinfo:
        trash._free_name(directory, ONE)
    assert excinfo.value.cause.reason == "trash-unavailable"
    assert excinfo.value.cause.scope is Scope.ITEM, (
        "one unacceptable name aborted the whole pass"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Round 7: an empty mount point is not a deletion, and a remixer is an artist
# ═══════════════════════════════════════════════════════════════════════════


def _removed_elsewhere(count, *, usn=50):
    """``count`` REMOVED collection rows recorded under the mapped prefix."""
    rows = []
    for index in range(count):
        row = FakeRow(
            ID=f"r{index}",
            FolderPath=f"{RECORDED_ELSEWHERE}/Music/Removed {index}.flac",
            FileSize=len(b"audio bytes"),
            rb_local_deleted=1,
            rb_local_usn=usn + index,
            Title=f"Removed {index}",
            ArtistName=ARTIST,
            ISRC=None,
        )
        rows.append(row)
    return rows


def _mapped_volume(cfg, tmp_path, *, active=50, removed=20):
    """A mounted volume holding ``active`` referenced files and ``removed`` candidates.

    Returns the volume path, the prefix rule, the binding, and the removed rows,
    with the pass already baselined so the removals are the only outstanding work.
    """
    volume = tmp_path / "Volumes" / "EP_DJ_LIBRARY"
    volume.mkdir(parents=True)
    live = _elsewhere(active)
    gone = _removed_elsewhere(removed)
    _populate(volume, live)
    for row in gone:
        target = Path(str(volume) + row.FolderPath[len(RECORDED_ELSEWHERE) :])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"audio bytes")
    rule = [locations.PrefixRule(RECORDED_ELSEWHERE, str(volume))]
    run.plan(cfg, FakeDb([], usn=40), actor="cli", prefix_map=rule)
    active_rows = [
        FakeRow(
            ID=row.content_id,
            FolderPath=row.recorded,
            FileSize=len(b"audio bytes"),
            rb_local_deleted=0,
            rb_local_usn=10,
            Title=Path(row.recorded).stem,
            ArtistName=ARTIST,
            ISRC=None,
        )
        for row in live
    ]
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
    """F1: ABSENCE READ AS EVIDENCE, upgraded to a permanent record of a deletion.

    A ``GONE`` verdict asks only whether the row's ANCHOR DIRECTORY exists, and
    an empty directory standing where a volume mounts passes that. macOS leaves
    exactly that behind after an unclean eject, and anything at all that writes
    to the path while the drive is detached creates it. Every removed row on the
    volume then reads ``GONE``; every confirmed one was given a tombstone,
    ``handled=True`` and a watermark that walked past it, so remounting the drive
    brought none of them back. Twenty rows, twenty suppressions, twenty files
    still on a disk sitting on the desk.

    The refusing signal was already computed one function up and was wired to
    nothing that decides: ``reference_set`` walks the ACTIVE rows through the
    same anchor, and ``suspect_anchors`` names an anchor that exists, indexed
    nothing, and had rows go missing under it. Here that is fifty active rows
    missing and zero indexed.
    """
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path)
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    offered = run.present(cfg, found)
    assert len(offered) == len(gone), "every removed row was offered while mounted"
    for item in offered:
        _confirm(cfg, item.item_id)

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
    """The half that must not regress, and it is a DIFFERENT branch from F1's.

    A volume that unmounted cleanly leaves no mount point at all, so the anchor
    is absent, and every row through it is ``UNRESOLVED`` rather than ``GONE``:
    not finished business, not retired, offered again on the next run that finds
    the drive. That answer comes from ``_Anchors.present`` and owes nothing to
    the reference set, which is why F1's repair had to be additional rather than
    a change to this test.
    """
    volume = tmp_path / "Volumes" / "EP_DJ_LIBRARY"
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
    """The mirror, because a retirement is permanent with or without a tombstone.

    A removal nobody answered for uses ``item.handled`` directly, and ``GONE`` is
    the one member of ``HANDLED``. An empty mount point therefore retired a whole
    library's removal history in one silent pass: no tombstone, no offer, no
    second chance. The same anchor question settles it, so the two paths cannot
    drift apart.
    """
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path)
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
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
    """The wedge fix that F1 may not take back, driven on the case it was for.

    A person confirms a removal and then deletes that file in the Finder. The
    file cannot come back, so holding the row open holds every removal above it
    forever. Here the anchor indexes fifty live rows, so it is answering, the
    absence IS evidence about the file, and the deletion is completed with the
    tombstone R36 owes.
    """
    volume, rule, db, gone = _mapped_volume(cfg, tmp_path, removed=1)
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    found = run.plan(cfg, db, actor="cli", prefix_map=rule)
    _confirm(cfg, run.present(cfg, found)[0].item_id)
    Path(str(volume) + gone[0].FolderPath[len(RECORDED_ELSEWHERE) :]).unlink()

    report = run.apply(cfg, db, actor="cli", home=home, prefix_map=rule)

    assert report.plan.references.suspect_anchors == ()
    recorded = stores.list_tombstones(cfg, include_revoked=True)
    assert len(recorded) == 1, "the queue wedged on a file that cannot come back"
    assert report.watermark.sequence == 50


# ── F4: the remixer spelling, measured over 65 values in three classes ───────


#: 40 values that are genuine mix-name DESIGNATIONS. A designation in this column
#: is a data anomaly, since ``RemixerName`` is an association proxy over
#: ``RemixerID`` into ``djmdArtist``, but importers write them. Twenty put their
#: version word last and twenty do not, which is the shape both previous rules
#: turned on.
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
#: change in either direction is a failing test rather than a paragraph. See
#: ``tombstone.already_spelled_as_a_remix`` for the comparison against the two
#: rules this replaced and for why the artist column is the criterion and the
#: total is not.
_MEASURED_MISSES = {"designation": 38, "artist-word-last": 0, "artist-word-first": 0}


def _provider_spelling(value: str, klass: str) -> str:
    """What a provider actually spells for the version this value names."""
    if klass == "designation":
        return tombstone.version_title("Strobe", value)
    return tombstone.version_title("Strobe", f"{value} {tombstone.REMIX_DESIGNATION}")


def test_the_remixer_spelling_misses_exactly_where_it_is_measured_to_miss():
    """F4: the rule is decided by a measurement over classes, not by a frequency.

    A raw rate over a hand-authored value set measures the SET, since the total
    is a weighted average whose weights are how often this column holds a
    designation rather than an artist name, and nothing in this repository
    samples a real ``RemixerName``. That is the unmeasurable frequency the
    residual findings deleted a claim about. So both class rates are pinned
    separately, and the criterion is the artist classes: 25 values the schema
    says this column holds, and the shipped rule must miss NONE of them.

    The designation rate is pinned in the same table rather than left implicit,
    because it is the cost being paid and a rule that quietly stopped paying it
    would be a rule that started guessing again.
    """
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
    """Why a test survives at all, stated as the two values that decide it.

    Deleting the branch entirely also misses nothing on the artist classes, so
    the artist criterion cannot separate the two. What separates them is the
    designation class, where the two rules differ on exactly the values already
    ending in ``Remix``: there the unconditional rule writes ``Remix Remix`` and
    this one writes what a provider spells. Two of the 65, measured. The shipped
    rule dominates pointwise and is never worse, which needs no claim about how
    often anything occurs.
    """
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
    """F2: the fix's own safety claim, falsified on the docstring's own examples.

    Round six argued that composing can only ADD a bracket, so no error of its
    spelling rule could merge two identities. It could. ``The Cut`` in
    ``RemixerName`` is an artist and was left verbatim, giving ``strobe (the
    cut)``; ``The Cut`` in ``Subtitle`` is a designation and composes ``strobe
    (the cut)`` as well. One identity, two versions, and deleting either
    suppressed the other, which is the OVER-suppression direction this package
    calls the worse one. The ISRC discriminator does not save it: with either
    code absent the convergence is accepted as deletable.

    The repair is structural rather than a widened list. The verbatim branch now
    fires only on a value already ending in ``Remix``, and a ``Subtitle`` holding
    that same string names that same version, so no reading of it can produce two
    versions wearing one identity.
    """
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
    """A tombstone the tool HONOURED and one it ASSERTED were indistinguishable.

    ``_settle_a_confirmed_absence`` writes ``trashed_to`` empty on purpose: the
    row was confirmed, the collection no longer holds it, and there was nothing
    at the recorded path to move. That is a materially different record from one
    written beside a real rename into the Trash, and ``summarize`` is the sole
    projection any surface renders. It emitted neither ``trashed_to`` nor
    ``version``, ``version_unbelieved`` or ``isrc``, so the only notice was a log
    line that scrolls away.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg, names=(ONE, TWO), usn=50)
    found = run.plan(cfg, db, actor="cli")
    offered = run.present(cfg, found)
    for item in offered:
        _confirm(cfg, item.item_id)
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
    """The other half of the same claim, on the row where it is the whole answer.

    A ``Subtitle`` the closed vocabulary does not believe leaves the row with a
    bare title, which is the vocabulary's measured worse direction. The record
    keeps the unbelieved value so an audit can answer "why did this tombstone
    miss", and that answer has to reach a person through the listing.
    """
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
    """The same shape as the ``'None'`` defect just closed, one step along.

    ``'   '`` is truthy, so the guard passed it, and ``{'content_id': '   '}``
    went on to address the review item, the decline and the membership test. A
    wrong key rather than a collapse, since ``recorded`` still separates two such
    rows, and a key nobody can type is a decision nobody can revoke.
    """
    with pytest.raises(CratekitError) as excinfo:
        tombstone.removed_file_identity(content_id=blank, recorded="/x.flac")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_a_numeric_identifier_is_still_addressable():
    """The half the stripped test may not cost: ``not 0`` would refuse a real row."""
    assert tombstone.removed_file_identity(content_id=0, recorded="/x.flac")["content_id"] == "0"


def test_two_spellings_of_one_isrc_are_one_recording(cfg):
    """F9: an ISRC is case-insensitive by specification and was compared raw.

    ``gbaya1500001`` against ``GBAYA1500001`` is one code, and the raw comparison
    read it as a positive statement that two rows are two recordings, so a
    legitimate convergence was refused as ambiguous. The direction was safe and
    the discriminator was still firing on a difference in spelling rather than on
    the thing it names.

    **THE FOLDING THIS TEST ORIGINALLY NAMED WAS THE WRONG ONE.** It said
    ``tombstone.fold`` is the folding both halves of every identity in this
    package already agree on, and it passed, because case is the one difference
    ``fold`` does close. It went green over a function that still read the DISPLAY
    FORM of this same code as a second recording. See
    :func:`test_the_display_form_of_one_isrc_is_not_two_recordings`.
    """
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
    """Round 8: the case fix went green over a wider defect at the same site.

    ISO 3901 defines an ISRC as twelve alphanumeric characters, and
    ``GB-AYA-15-00001`` is the DISPLAY FORM of ``GBAYA1500001``, not another code.
    Compared under the free-text ``tombstone.fold``, which keeps punctuation on
    purpose, those are two strings, so ONE recording filed twice was reported
    AMBIGUOUS_VERSION.

    That is not merely a refused deletion. ``candidates.Category.AMBIGUOUS_VERSION``
    is not in ``candidates.HANDLED``, so the watermark does not pass over the row,
    the pass never offers it, and nothing can ever clear it: the queue wedges at
    those rows permanently. Safe direction, permanent cost.
    """
    one = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="GBAYA1500001")
    other = replace(_removed(cfg, TWO, "2"), title="Strobe", isrc="GB-AYA-15-00001")
    assert stores.version_of(one) == stores.version_of(other)
    assert stores.ambiguous_versions([one, other]) == frozenset(), (
        "the display form of a code is the same code, and reading it as a second "
        "recording wedges the queue at that row forever"
    )


def test_a_placeholder_in_the_isrc_column_is_an_absent_code(cfg):
    """A separator is not a code, and silence is read as agreement.

    A column holding ``-`` is a person's placeholder for "no code". It folds to
    nothing, is discarded before the count, and so leaves the identity's own claim
    standing rather than contradicting a real code on the other row.
    """
    real = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="GBAYA1500001")
    placeholder = replace(_removed(cfg, TWO, "2"), title="Strobe", isrc="-")
    assert stores.ambiguous_versions([real, placeholder]) == frozenset(), (
        "a placeholder is an absent code, not a code that disagrees"
    )


def test_folding_the_code_does_not_cost_the_collision_it_exists_for(cfg):
    """The half a wider fold could cost: two real codes must still disagree.

    Stated at the call site as well as at the unit, because a fold that erased the
    value entirely would also make this function return the empty set and every
    unit test of the folding would still pass.
    """
    one = replace(_removed(cfg, ONE, "1"), title="Strobe", isrc="GB-AYA-15-00001")
    third = replace(_removed(cfg, ACCENTED, "3"), title="Strobe", isrc="US-RC1-76-07839")
    assert stores.ambiguous_versions([one, third]) == frozenset({"1", "3"}), (
        "two different recordings in display form must still read as a collision"
    )


@pytest.mark.parametrize(
    "version, expected",
    [
        pytest.param(
            "Michael Woods Remix   ", "Strobe (Michael Woods Remix)", id="trailing-space"
        ),
        pytest.param(
            " Michael Woods Remix", "Strobe (Michael Woods Remix)", id="leading-space"
        ),
        pytest.param(
            "Michael  Woods  Remix", "Strobe (Michael Woods Remix)", id="interior-run"
        ),
        pytest.param(
            "Michael Woods (Remix)", "Strobe (Michael Woods Remix)", id="own-brackets"
        ),
        pytest.param(
            "[Michael Woods Remix]", "Strobe (Michael Woods Remix)", id="own-square-brackets"
        ),
    ],
)
def test_a_columns_own_typing_does_not_become_a_second_identity(version, expected):
    """Round 8: the value is tidied BEFORE it goes inside the bracket.

    ``fold`` strips the ends of the WHOLE composed string, and the closing bracket
    sits outside the value, so a trailing space in one rekordbox column composed
    ``strobe (michael woods remix )``. That matches no provider spelling AND
    differs from the identity the same value produces without the space, so one
    stray keystroke is both a version that cannot be suppressed and a second
    identity for a version that already has one.

    A value carrying its own brackets is the same defect with a different
    character: ``Strobe (Michael Woods (Remix))``, which ``tombstone._BRACKETED``
    is non-nesting by design and so reads as no version group at all.
    """
    assert tombstone.version_title("Strobe", version) == expected


def test_tidying_the_value_does_not_rewrite_the_persons_own_text():
    """The bound on the tidy: the ends and the brackets and NOTHING else.

    Interior punctuation, case and the words themselves are the person's text and
    this module does not get to normalise them. Only the characters that broke the
    composition are touched.
    """
    assert (
        tombstone.version_title("Strobe", "  Michael Woods' 12\" Re-Edit  ")
        == "Strobe (Michael Woods' 12\" Re-Edit)"
    )


@pytest.mark.parametrize("boolean", [True, False])
def test_a_boolean_identifier_is_refused_rather_than_addressed_as_its_repr(boolean):
    """Round 8: ``str(False)`` is ``'False'``, truthy, and strips to itself.

    So a boolean in the identifier column addressed the review item, the decline
    and the playlist membership test as the literal string ``'False'``, exactly as
    ``None`` addressed them as ``'None'`` before the guard above it. Tested by TYPE
    and not by truthiness, because ``not False`` is true while ``not True`` is not,
    so a falsiness test would refuse one boolean and accept the other.
    """
    with pytest.raises(CratekitError) as excinfo:
        tombstone.removed_file_identity(content_id=boolean, recorded="/x.flac")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_refusing_booleans_does_not_take_the_numeric_identifier_with_it():
    """Why the guard is ``isinstance`` and not a comparison.

    ``0 == False`` in Python, so a guard written as a comparison against ``False``
    would refuse the legitimate row whose collection identifier is ``0``, which
    :func:`test_a_numeric_identifier_is_still_addressable` says must stay
    addressable. This is the pair of that test on the other side of the new guard.
    """
    assert tombstone.removed_file_identity(content_id=0, recorded="/x.flac")["content_id"] == "0"
    assert tombstone.removed_file_identity(content_id=1, recorded="/x.flac")["content_id"] == "1"


# ── Round 10: the era is stamped in the record, so history is a LOOKUP ───────
#
# Four rounds answered "was this deletion already recorded" by recomputing what
# an earlier build would have composed for this row, and every one of them was
# correct on the day it was written. The reconstruction is made of live
# functions, so it moves with the build; when it moves in step with the current
# composer the two agree and the caller reports that there is no history at all.
# Freezing the composer does not fix it, because a frozen composer calls ``fold``,
# ``_already_carries`` and ``already_spelled_as_a_remix``, and those are live.
#
# Nothing below asks what a former build would have composed. The record says
# which rules composed it, and a record composed by other rules is matched on the
# ROW it names.


def test_the_folding_limb_of_the_tidy_is_covered_on_its_own(cfg):
    """F3 from the round 8 verification: a guard covered only by another guard.

    Round 8's table mutated the tidy through the COMPOSITION limb twice and never
    removed the FOLDING limb alone, so reverting ``fold(tidied)`` to
    ``fold(version)`` while still composing the tidied value killed zero tests out
    of 3458. The limb is load bearing on a reachable path: without it, a title
    that already names the version stops being recognised as naming it, and a
    second bracket is composed onto a title that already says everything.

    It is about the LIVE composer rather than about history, and it sits here
    because round ten deleted the history block it happened to be filed inside.
    """
    assert tombstone.version_title(
        "Strobe (Michael Woods Remix)", "[Michael Woods Remix]"
    ) == "Strobe (Michael Woods Remix)"
    assert tombstone.version_title("Strobe", "()") == "Strobe"


def _record_an_earlier_build_wrote(cfg, row, *, title, stamp=None):
    """Plant the record a build with OTHER composition rules left on this disk.

    Written with the payload ``record_tombstone`` has carried since the first
    commit of this pass, measured across all eleven commits on this branch, so
    the only things that differ from a record this build would write are the
    identity spelling and the stamp.

    **PLANTING AN EMPTY PAYLOAD IS WHAT THE ROUND 9 TESTS DID AND IT MEASURED THE
    FIXTURE.** No build of this pass has ever written a tombstone without the row
    it was about; a fixture that omits it describes a store nobody has.
    """
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
    run.plan(cfg, FakeDb([], usn=40), actor="cli")
    row = _versioned(cfg, ONE, content_id, usn=50, title=title, isrc="AAAA11111111",
                     subtitle=subtitle, remixer=remixer)
    return library.read_collection(FakeQuery([row])).removed[0]


@pytest.mark.parametrize(
    "spelling",
    [
        pytest.param("Strobe (Michael Woods)", id="before-the-remixer-was-spelled"),
        pytest.param("Strobe ( Michael Woods  Remix)", id="before-the-value-was-tidied"),
        pytest.param("Strobe", id="before-anything-was-composed"),
        pytest.param("Strobe (Michael Woods Rework)", id="a-designation-nobody-uses"),
        # THE ROW THIS TEST EXISTS FOR. Every spelling above is one a build of
        # this pass really did write, so an implementation that reconstructs the
        # eras it knows about passes all four. This one is a rule nobody has
        # written, which is the only honest stand-in for the rule the NEXT round
        # invents, and no reconstruction can produce it. It is what pins the
        # design rather than the era list.
        pytest.param("a rule this build has never heard of", id="a-rule-nobody-has-written"),
    ],
)
def test_a_tombstone_is_recognised_whatever_rule_composed_its_identity(
    cfg, gates_pass, spelling
):
    """The recognition question no longer depends on the spelling at all.

    A store on a user's disk was written by the build that wrote it, and the only
    thing every build agrees on is WHICH ROW the deletion was about. That pair,
    the collection identifier and the path the row recorded, has ridden in the
    payload since the first commit of this pass and is written down raw, so
    matching on it consults no composition rule and no composition rule can move
    it.
    """
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    planted = _record_an_earlier_build_wrote(cfg, removed, title=spelling)

    assert planted.identity != stores.version_of(removed), (
        "this spelling is what this build writes, so it exercises no history"
    )
    assert stores.tombstone_predicate(cfg)(removed), (
        "a deletion an earlier build recorded is not recognised, so the row is "
        "held open forever and the person is told to put back a file that is "
        "already in the Trash where they put it"
    )

    # AND THE CONSULT IS NOT WIDENED WITH IT. A consulter holds a provider's
    # title and is answered under the one spelling providers use; a record
    # written under a spelling this build has decided is wrong stays unmatched
    # there, and the store is what has to be rewritten for that, not the
    # question.
    assert not stores.suppressed_version(
        cfg, artist=ARTIST, title="Strobe (Michael Woods Remix)"
    )


def test_the_ordinary_row_whose_history_was_reported_as_absent(cfg, gates_pass):
    """B2 from the round 9 verification, and it needed no unusual column at all.

    ``Strobe Extended Mix`` with the ``Subtitle`` ``Extended Mix`` is a row a
    rekordbox library holds by the thousand. Before ``_already_carries`` became a
    bracketed test it was a plain substring test, ``"extended mix" in "strobe
    extended mix"`` is true, so the build of the day composed NOTHING and wrote
    the bare title. The round 9 reconstruction asked the LIVE ``_already_carries``,
    which answers no, so it reconstructed the same string this build writes,
    found no difference, and returned the empty tuple: not a wrong earlier
    spelling but no earlier spelling at all, reported as "there is no history
    here".
    """
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
    """The same thing driven end to end, which is where the cost is paid.

    The person confirmed the removal, an earlier build trashed the file and wrote
    the tombstone, and the watermark never advanced. Unrecognised, the row is
    refused forever and every removal above it waits behind it, because the
    watermark is contiguous. Recognised, it retires and no second record is
    written for a deletion that already has one.
    """
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    db = _prepared(cfg)
    found = run.plan(cfg, db, actor="cli")
    _confirm(cfg, run.present(cfg, found)[0].item_id)

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
    """The stamp is written, is the measured value, and reaches the listing.

    A record outlives the build that wrote it, so the record is what has to carry
    the era. Every attempt to work it out afterwards has been a recomputation
    that drifts.
    """
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    record = stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")

    assert record.payload[stores.IDENTITY_SCHEME_FIELD] == stores.identity_scheme()
    assert stores.summarize(record)[stores.IDENTITY_SCHEME_FIELD] == stores.identity_scheme()

    # THE SHAPE IS PINNED SEPARATELY FROM THE VALUE, because the equalities above
    # take their expected value from the code under test and would be satisfied
    # by a stamp that is always the empty string. A digest that is prefixed and
    # long enough not to collide is the property, and the value itself may move
    # freely, which is exactly what it is for.
    stamp = stores.identity_scheme()
    assert stamp.startswith("is1_") and len(stamp) == len("is1_") + 16

    # AND IT IS ON THE DISK, not only on the object the writer returned.
    assert stamp in stores.tombstones(cfg).path.read_text()


@pytest.mark.parametrize(
    "module_name, attribute, replacement",
    [
        pytest.param("tombstone", "_is_a_credit", lambda group: False, id="is-a-credit"),
        pytest.param(
            "tombstone", "_CREDIT_MARKERS", frozenset(), id="credit-markers"
        ),
        pytest.param(
            "tombstone", "_already_carries",
            lambda title, folded: folded in tombstone.fold(title),
            id="already-carries",
        ),
        pytest.param(
            "tombstone", "already_spelled_as_a_remix", lambda value: False,
            id="already-spelled-as-a-remix",
        ),
        pytest.param("tombstone", "REMIX_DESIGNATION", "Rework", id="remix-designation"),
        pytest.param(
            "tombstone", "_as_a_bracketed_value", lambda version: str(version),
            id="the-tidy",
        ),
        pytest.param(
            "tombstone", "fold", lambda value: " ".join(str(value).split()),
            id="the-fold",
        ),
        pytest.param(
            "tombstone", "VERSION_WORDS", frozenset({"remix"}), id="the-vocabulary",
        ),
        pytest.param(
            "library", "_VERSION_COLUMNS",
            (("Subtitle", library.VERSION_IS_A_DESIGNATION),
             ("RemixerName", library.VERSION_IS_AN_ARTIST)),
            id="the-column-order",
        ),
    ],
)
def test_the_stamp_moves_when_any_rule_below_it_moves(
    monkeypatch, module_name, attribute, replacement
):
    """B1 GENERALISED, which is the whole reason this round exists.

    Freezing one node of a call tree does not freeze the reconstruction: any
    helper below it can drift, and the round 9 frozen composers drifted through
    ``_already_carries`` within one commit of being written. The stamp is a
    MEASUREMENT of the rules rather than a number somebody remembers to bump, so
    a change anywhere from the column the reader believes down to the bracket
    pattern the composer uses comes out as a different value.

    ``_VERSION_COLUMNS`` and ``VERSION_WORDS`` are in this list on purpose. They
    live one file over, in the READER, and they change the identity a rekordbox
    row produces with every composition function untouched. A stamp taken over
    the composer alone would still match, and the recogniser would still trust an
    identity that had moved: the same defect one file over, which is the fifth
    pattern.
    """
    before = stores.identity_scheme()
    monkeypatch.setattr(
        {"tombstone": tombstone, "library": library}[module_name], attribute, replacement
    )
    assert stores.identity_scheme() != before, (
        f"{module_name}.{attribute} changed what a row composes to and the stamp "
        f"did not move, so a build with this change would read its predecessor's "
        f"records as its own and miss them"
    )


def test_this_builds_own_record_is_matched_on_its_version_not_on_its_row(cfg, gates_pass):
    """What the stamp DECIDES, which is the only thing it decides.

    A record carrying this build's stamp was composed by rules this build has, so
    the identity is trustworthy and stays the question. Widening every record to
    its row would retire a row whose version column has been edited since the
    deletion was recorded, against a record naming a version the row no longer
    claims, and the listing would never gain the second spelling.
    """
    removed = _one_removed_row(cfg, title="Strobe", subtitle="Extended Mix")
    stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")
    assert stores.tombstone_predicate(cfg)(removed)

    edited = replace(removed, version="Club Mix")
    assert stores.version_of(edited) != stores.version_of(removed)
    assert not stores.tombstone_predicate(cfg)(edited), (
        "a row whose version column changed after the deletion was recorded is "
        "read as already recorded, so the tombstone naming the version it claims "
        "now is never written"
    )


def test_reading_a_store_from_before_the_stamp_migrates_it_and_writes_nothing(
    cfg, gates_pass
):
    """The migration path, and it is that there is nothing to migrate.

    A record written before the stamp existed cannot carry this build's stamp, so
    it falls to the row lookup by the same rule that will catch an era nobody has
    written yet. Nothing rewrites the file to make that true, because a read that
    repairs is a read that can fail while a person is only asking a question.
    """
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
    assert stores.summarize(stores.list_tombstones(cfg)[0])[
        stores.IDENTITY_SCHEME_FIELD
    ] == "", "an era before the stamp is a fact about the record, not a missing field"


def test_a_record_that_names_no_row_matches_no_row(cfg, gates_pass):
    """The row lookup is a lookup on a NAME, and an absent name is not a name.

    Without this the coordinates of a record naming nothing would be a real key
    in the set, and every row that also names nothing would match it. That is the
    empty-identity collapse ``version_identity`` refuses one module down, arriving
    through a different door: one record would retire every unnameable row in the
    library, permanently, and it would look exactly like the feature working.
    """
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
    """``str(None)`` is ``'None'``, and this module has now fixed that at four doors.

    The store is JSON, so ``null``, ``true`` and ``false`` are values a record can
    carry in the field that names the row, whether a hand edit put them there or a
    binding did. Stringified they are perfectly ordinary truthy names, and a row
    whose own identifier is that same text would then be retired against a record
    that names no row at all. ``removed_file_identity`` refuses each of the three
    for exactly this reason; the row lookup is a second reader of the same field
    and owes the same answer.
    """
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


def test_the_row_lookup_reads_two_composition_forms_of_one_path_as_one_path(
    cfg, gates_pass
):
    """macOS hands out NFD and rekordbox stores NFC, so this is the ordinary case.

    ``removed_file_identity`` already composes this field to NFC, and the row
    lookup is a second reader of the same field. Two rules for one field is how
    the two come to disagree, and the disagreement costs the thing the whole round
    is about: the record is not recognised, the row is held open forever, and the
    watermark is contiguous so every removal above it is held too.
    """
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
    """The question is "did a run record this", not "is this suppressed today".

    Revoking makes the version acquirable again and says nothing about whether
    the file was moved. Reading a revocation as "no deletion happened" re-opens
    the very row the person already dealt with, and then a confirmed removal is
    offered again with the file already in the Trash.
    """
    removed = _one_removed_row(cfg, title="Strobe", remixer="Michael Woods")
    record = stores.record_tombstone(cfg, removed, actor="cli", trashed_to="/x")
    stores.revoke_tombstone(cfg, record.suppression_id, actor="cli")

    assert stores.list_tombstones(cfg) == (), "the revocation did not take"
    assert stores.tombstone_predicate(cfg)(removed), (
        "revoking a tombstone re-opened a removal that was finished business"
    )


def test_the_stamp_field_is_spelled_on_disk_and_not_only_in_this_build(cfg):
    """A persisted field name is a wire format, so it is pinned to a literal.

    Renaming the constant renames it consistently for every reader in this build
    and silently orphans the stamp in every store the previous build wrote. The
    direction is safe, since an unreadable stamp reads as another era and falls to
    the row lookup, but a format nobody pinned is a format that moves.
    """
    assert stores.IDENTITY_SCHEME_FIELD == "identity_scheme"


def test_a_row_that_cannot_be_identified_is_not_read_as_already_recorded(cfg, gates_pass):
    """B4 from the round 9 verification, carried and closed.

    ``recorded`` answers a question whose True retires a confirmed removal
    without moving anything, so True on a row nobody can identify would throw
    away a deletion somebody confirmed for a file they had merely renamed. False
    re-offers the row, which costs one question.

    **ITS FIELD REACHABILITY, MEASURED RATHER THAN ASSUMED.** Both callers in
    ``run`` ask this only of a row whose category is ``GONE``, and
    ``candidates.categorize`` asks ``identifiable`` FIRST, so a row that cannot
    be identified is answered ``UNIDENTIFIABLE`` and never reaches ``GONE``. The
    guard is therefore unreachable through the pass and reachable through the
    module's own exported predicate, which is what this test asks it as.
    """
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
    """The claim stated structurally, so it cannot quietly come back.

    Every previous round closed this class by adding another reconstruction, and
    the reconstruction is the class. A function whose name says it reproduces
    what an earlier build wrote is the shape to refuse, whatever it is called.
    """
    for module in (tombstone, stores):
        offenders = [
            name for name in dir(module)
            if "before_the" in name or "earlier_builds" in name or "historical" in name
        ]
        assert offenders == [], (
            f"{module.__name__} reconstructs a former build's composition again: "
            f"{offenders}"
        )
