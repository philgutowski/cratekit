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


class FakeDb:
    """A binding that answers the five questions the pass asks and nothing else.

    A fake rather than a real database for the branch tests, deliberately. What
    the branches are about is which category a row lands in, and building ten
    libraries to express ten categories would put the interesting part of each
    test behind fifty lines of schema. The real database appears once, below,
    for the claim only a real one can carry: that this pass writes nothing to it.
    """

    def __init__(self, rows=(), memberships=(), *, usn=100, identity="db-identity-1"):
        self.rows = list(rows)
        self.memberships = list(memberships)
        self.usn = usn
        self.identity = identity

    def get_content(self):
        return FakeQuery(self.rows)

    def get_playlist_songs(self):
        return FakeQuery(self.memberships)

    def get_local_usn(self):
        return self.usn

    def get_property(self):
        return FakeQuery([FakeRow(DBID=self.identity)])


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
        library.read_collection([blind], since=0)
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


def test_a_removed_row_with_no_update_sequence_refuses(cfg):
    blind = FakeRow(ID="9", FolderPath="/x.flac", rb_local_deleted=1, rb_local_usn=None)
    with pytest.raises(CratekitError) as excinfo:
        library.read_collection([blind], since=0)
    assert excinfo.value.cause.reason == "removal-sequence-unreadable"


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
        seen = library.read_collection(handle.get_content(), since=0)
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
