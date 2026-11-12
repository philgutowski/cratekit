"""U254: the applied ledger is written in proportion to the entries applied.

Before U254 every mark took the lock, parsed and validated the whole applied
ledger and wrote the whole of it back, so N marks wrote about 127 x N squared
bytes: half a gigabyte for two thousand entries. A mark now appends one synced
record line to a journal, and the whole file is rewritten only when it is
created, when a ledger written before U254 is met, and when a torn last record
has to be cut away.

What these tests hold, beside the saving itself, is everything the saving must
not cost: a mark is durable before the next entry is touched, an apply killed at
any mark resumes with exactly the marks that landed, a ledger written by the
code before U254 still reads, a torn last record is read as the mark that did
not finish and never as an empty ledger, and the lock still surrounds every
write. The byte count is the assertion, never a wall clock.
"""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import approval as adopt_approval
from cratekit.adopt import revert as adopt_revert
from cratekit.adopt import scan as adopt_scan
from cratekit.core import config, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from tests.test_adoption import (
    SRC_ROOT,
    _bucket_and_genre,
    _plan_of,
    _row,
    _synth_in,
)
from tests.test_config import valid_data

#: The bytes the writer before U254 left for three records, captured from that
#: code on 2026-11-12 rather than composed here, so the compatibility test reads
#: what a library on disk really holds today and not this test's idea of it. Out
#: of entry order on purpose in the source calls (the writer sorted), with an
#: empty digest and an empty sub, which the reader fills from ``or ""``.
DOCUMENT_BEFORE_U254 = (
    '{\n  "applied": [\n    {\n      "actor": "a-person",\n      "applied": '
    '"2026-11-01T00:00:00+00:00",\n      "bucket": "house",\n      "content": '
    '"c0",\n      "digest": "1111111111111111",\n      "entry": '
    '"genre_energy:c0:house:med",\n      "sub": "med",\n      "tree": '
    '"genre_energy"\n    },\n    {\n      "actor": "a-person",\n      "applied": '
    '"2026-11-03T00:00:00+00:00",\n      "bucket": "disco",\n      "content": '
    '"c2",\n      "digest": "",\n      "entry": "genre_energy:c2:disco:",\n      '
    '"sub": "",\n      "tree": "genre_energy"\n    },\n    {\n      "actor": '
    '"session",\n      "applied": "2026-11-02T00:00:00+00:00",\n      "bucket": '
    '"techno",\n      "content": "c1",\n      "digest": "2222222222222222",\n      '
    '"entry": "shelf_stack:c1:techno:high",\n      "sub": "high",\n      "tree": '
    '"shelf_stack"\n    }\n  ],\n  "schema_version": 1\n}\n'
)

#: What a reader must answer for ``DOCUMENT_BEFORE_U254``, written out by hand.
RECORDS_BEFORE_U254 = (
    adopt_apply.AppliedEntry(
        entry_id="genre_energy:c0:house:med",
        tree="genre_energy",
        content_id="c0",
        bucket="house",
        sub="med",
        actor="a-person",
        digest="1111111111111111",
        applied="2026-11-01T00:00:00+00:00",
    ),
    adopt_apply.AppliedEntry(
        entry_id="genre_energy:c2:disco:",
        tree="genre_energy",
        content_id="c2",
        bucket="disco",
        sub="",
        actor="a-person",
        digest="",
        applied="2026-11-03T00:00:00+00:00",
    ),
    adopt_apply.AppliedEntry(
        entry_id="shelf_stack:c1:techno:high",
        tree="shelf_stack",
        content_id="c1",
        bucket="techno",
        sub="high",
        actor="session",
        digest="2222222222222222",
        applied="2026-11-02T00:00:00+00:00",
    ),
)

HEADER = b'{"format": "journal", "schema_version": 2}\n'


class _Killed(BaseException):
    """A process that stops existing, not a refusal anything handles."""


def _cfg_at(root: Path) -> config.Config:
    (root / "db").mkdir(parents=True, exist_ok=True)
    (root / "Music").mkdir(parents=True, exist_ok=True)
    return config.from_dict(valid_data(root))


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    _cfg_at(root)
    return root


@pytest.fixture
def cfg(library, monkeypatch):
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    return resolved


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


def _entry(n: int, *, tree: str = "genre_energy", actor: str = "a-person"):
    return adopt_apply.AppliedEntry(
        entry_id=f"{tree}:entry-{n:06d}",
        tree=tree,
        content_id=str(n),
        bucket="house",
        sub="med",
        actor=actor,
        digest="0" * 16,
        applied="2026-11-12T00:00:00+00:00",
    )


class _Writes:
    """Every byte the two ledger writers are handed, and which writer took it."""

    def __init__(self) -> None:
        self.rewritten = 0
        self.appended = 0
        self.rewrites = 0
        self.appends = 0

    @property
    def total(self) -> int:
        return self.rewritten + self.appended


def _count_writes(monkeypatch) -> _Writes:
    seen = _Writes()
    real_rewrite = config.atomic_write_bytes
    real_append = config.append_durable_bytes

    def rewrite(payload, path, *args, **kwargs):
        seen.rewritten += len(payload)
        seen.rewrites += 1
        return real_rewrite(payload, path, *args, **kwargs)

    def append(payload, path, *args, **kwargs):
        seen.appended += len(payload)
        seen.appends += 1
        return real_append(payload, path, *args, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", rewrite)
    monkeypatch.setattr(config, "append_durable_bytes", append)
    return seen


def _line_of(entry) -> bytes:
    return json.dumps(entry.to_json(), sort_keys=True).encode("utf-8") + b"\n"


def _lines(path: Path) -> list[bytes]:
    raw = path.read_bytes()
    assert raw.endswith(b"\n"), "the journal does not end on a whole record"
    return raw[:-1].split(b"\n")


# ═══════════════════════════════════════════════════════════════════════════
# The saving, by the byte
# ═══════════════════════════════════════════════════════════════════════════


def _bytes_for(root: Path, count: int, monkeypatch) -> tuple[_Writes, int]:
    with monkeypatch.context() as patched:
        # The environment names the library over the document, so each count
        # gets a library of its own only if the variable says so too.
        patched.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfg_value = _cfg_at(root)
        seen = _count_writes(patched)
        for n in range(count):
            adopt_apply.mark_applied(cfg_value, _entry(n))
        path = adopt_apply.path_for(cfg_value)
    assert path.is_relative_to(root), "the two counts shared one ledger"
    return seen, path.stat().st_size


def test_twice_the_marks_write_about_twice_the_bytes(tmp_path, monkeypatch):
    """The card's measure: 400 marks write under 2.5 times what 200 do.

    The writer before U254 wrote four times as much for twice the entries,
    because each mark rewrote everything marked before it. The total is also
    held EQUAL to the final file's size, so every byte that reached the ledger
    went through one of the two wrapped writers and none was written around
    them, and to exactly one whole file rewrite, the one that created it.
    """
    two_hundred, size_200 = _bytes_for(tmp_path / "two-hundred", 200, monkeypatch)
    four_hundred, size_400 = _bytes_for(tmp_path / "four-hundred", 400, monkeypatch)

    assert four_hundred.total < 2.5 * two_hundred.total, (
        f"400 marks wrote {four_hundred.total} bytes against {two_hundred.total} "
        f"for 200, which is the square growth the journal exists to end"
    )
    assert two_hundred.total == size_200
    assert four_hundred.total == size_400
    assert (two_hundred.rewrites, two_hundred.appends) == (1, 199)
    assert (four_hundred.rewrites, four_hundred.appends) == (1, 399)


def test_a_mark_does_not_parse_the_ledger_it_appends_to(cfg, monkeypatch):
    """The CPU half of the square: no whole read per mark once the file exists."""
    adopt_apply.mark_applied(cfg, _entry(0))
    ledger = adopt_apply.path_for(cfg)
    real_read = Path.read_bytes
    whole_reads: list[Path] = []

    def watched(self):
        if self == ledger:
            whole_reads.append(self)
        return real_read(self)

    with monkeypatch.context() as patched:
        patched.setattr(Path, "read_bytes", watched)
        for n in range(1, 20):
            adopt_apply.mark_applied(cfg, _entry(n))
    assert whole_reads == [], f"{len(whole_reads)} marks read the whole ledger"
    assert len(adopt_apply.read(cfg).applied) == 20


def test_every_append_is_synced_before_the_mark_returns(cfg, monkeypatch):
    """A mark is durable before the loop moves on to the next entry's writes."""
    adopt_apply.mark_applied(cfg, _entry(0))
    synced: list[int] = []
    real_fsync = os.fsync
    monkeypatch.setattr(os, "fsync", lambda fd: (synced.append(fd), real_fsync(fd)))
    adopt_apply.mark_applied(cfg, _entry(1))
    assert synced, "an appended mark returned without reaching the disk"


def test_an_append_the_system_writes_in_pieces_still_lands_whole(cfg, monkeypatch):
    """``os.write`` may write fewer bytes than it was handed; the rest must follow."""
    adopt_apply.mark_applied(cfg, _entry(0))
    real_write = os.write
    with monkeypatch.context() as patched:
        patched.setattr(os, "write", lambda fd, data: real_write(fd, bytes(data[:3])))
        adopt_apply.mark_applied(cfg, _entry(1))
    assert adopt_apply.read(cfg).entry_ids() == {_entry(0).entry_id, _entry(1).entry_id}
    assert all(json.loads(line) for line in _lines(adopt_apply.path_for(cfg)))


def test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark(cfg):
    """Skipping the whole read is earned only by a file exactly as it was left.

    Every mark before U254 read and validated the whole ledger, so a damaged one
    refused the mark. A file another hand changed is read whole again, and
    refuses the same way, before anything is appended to it.
    """
    for n in range(3):
        adopt_apply.mark_applied(cfg, _entry(n))
    path = adopt_apply.path_for(cfg)
    damaged = path.read_bytes().replace(b'"actor": "a-person"', b'"actor": "a-pers', 1)
    path.write_bytes(damaged)
    with pytest.raises(adopt_apply.AppliedLedgerUnreadable):
        adopt_apply.mark_applied(cfg, _entry(3))
    assert path.read_bytes() == damaged, "a mark appended to a damaged ledger"


def _same_size_document(path: Path) -> bytes:
    """A schema 1 document padded to the journal's exact size, with its records.

    Appending to it would leave a file no build can read, so a mark that takes
    it for the journal it replaced is visible at the next read.
    """
    size = path.stat().st_size
    body = DOCUMENT_BEFORE_U254.encode("utf-8").rstrip(b"\n")
    assert len(body) + 1 <= size, "mark more entries so the journal outgrows it"
    return body + b" " * (size - len(body) - 1) + b"\n"


def _marked_past_the_document(cfg_value) -> Path:
    for n in range(6):
        adopt_apply.mark_applied(cfg_value, _entry(n))
    return adopt_apply.path_for(cfg_value)


def _after_one_more_mark_reads_the_document_and_the_mark(cfg_value):
    adopt_apply.mark_applied(cfg_value, _entry(9))
    assert adopt_apply.read(cfg_value).entry_ids() == {
        *(record.entry_id for record in RECORDS_BEFORE_U254),
        _entry(9).entry_id,
    }


def test_a_file_put_in_place_with_the_same_size_and_time_is_read_again(cfg):
    """A restore's shape: a new file, the same size and time. The inode tells.

    Copied beside the ledger, given its modification time, and renamed over
    it, as a staged restore does. Taken for the file this process left, the
    next mark would append a journal record to a whole document.
    """
    path = _marked_past_the_document(cfg)
    before = os.stat(path)
    staged = path.with_name("staged.tmp")
    staged.write_bytes(_same_size_document(path))
    os.utime(staged, ns=(before.st_atime_ns, before.st_mtime_ns))
    os.replace(staged, path)
    after = os.stat(path)
    assert (after.st_size, after.st_mtime_ns) == (before.st_size, before.st_mtime_ns)
    assert after.st_ino != before.st_ino
    _after_one_more_mark_reads_the_document_and_the_mark(cfg)


def test_a_file_rewritten_in_place_at_the_same_size_is_read_again(cfg):
    """The same inode and size, written over: the modification time tells."""
    path = _marked_past_the_document(cfg)
    before = os.stat(path)
    path.write_bytes(_same_size_document(path))
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns + 1_000_000_000))
    after = os.stat(path)
    assert (after.st_ino, after.st_size) == (before.st_ino, before.st_size)
    _after_one_more_mark_reads_the_document_and_the_mark(cfg)


def test_a_torn_record_another_process_left_is_cut_before_the_next_append(cfg):
    """Another process killed mid append: this one must not append after its bytes."""
    adopt_apply.mark_applied(cfg, _entry(0))
    path = adopt_apply.path_for(cfg)
    with path.open("ab") as other:
        other.write(_line_of(_entry(5))[:9])
    adopt_apply.mark_applied(cfg, _entry(1))
    assert adopt_apply.read(cfg).entry_ids() == {_entry(0).entry_id, _entry(1).entry_id}
    assert all(json.loads(line) for line in _lines(path))


def test_a_torn_tail_left_inside_one_clock_tick_is_still_cut(cfg):
    """The size tells, where a coarse clock gives the torn file its old time.

    FAT, exFAT and HFS+ keep modification times to a second or two, so another
    process's torn append can leave the inode and the time as this process
    left them. Taken for the file it left, the next mark would join its record
    to the torn bytes and read back as not applied.
    """
    for n in range(3):
        adopt_apply.mark_applied(cfg, _entry(n))
    path = adopt_apply.path_for(cfg)
    before = os.stat(path)
    with path.open("ab") as other:
        other.write(_line_of(_entry(5))[:15])
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
    adopt_apply.mark_applied(cfg, _entry(9))
    assert adopt_apply.read(cfg).entry_ids() == {
        _entry(n).entry_id for n in (0, 1, 2, 9)
    }


def test_a_record_another_process_appended_is_kept(cfg):
    adopt_apply.mark_applied(cfg, _entry(0))
    path = adopt_apply.path_for(cfg)
    with path.open("ab") as other:
        other.write(_line_of(_entry(5)))
    adopt_apply.mark_applied(cfg, _entry(1))
    assert adopt_apply.read(cfg).entry_ids() == {
        _entry(n).entry_id for n in (0, 1, 5)
    }


# ═══════════════════════════════════════════════════════════════════════════
# The lock, the validation and the shape
# ═══════════════════════════════════════════════════════════════════════════


def test_every_ledger_write_happens_under_the_exclusive_lock(cfg, monkeypatch):
    held = {"now": False}
    real_lock = config._exclusive_lock

    @contextlib.contextmanager
    def watched(path):
        with real_lock(path):
            held["now"] = True
            try:
                yield
            finally:
                held["now"] = False

    real_rewrite = config.atomic_write_bytes
    real_append = config.append_durable_bytes
    outside: list[str] = []

    def rewrite(payload, path, *args, **kwargs):
        if path == adopt_apply.path_for(cfg) and not held["now"]:
            outside.append("rewrite")
        return real_rewrite(payload, path, *args, **kwargs)

    def append(payload, path, *args, **kwargs):
        if not held["now"]:
            outside.append("append")
        return real_append(payload, path, *args, **kwargs)

    monkeypatch.setattr(config, "_exclusive_lock", watched)
    monkeypatch.setattr(config, "atomic_write_bytes", rewrite)
    monkeypatch.setattr(config, "append_durable_bytes", append)
    for n in range(3):
        adopt_apply.mark_applied(cfg, _entry(n))
    assert outside == [], f"a ledger write ran outside the lock: {outside}"


def test_the_journal_is_a_header_and_one_line_per_record(cfg):
    for n in range(3):
        adopt_apply.mark_applied(cfg, _entry(n))
    lines = _lines(adopt_apply.path_for(cfg))
    assert lines[0] + b"\n" == HEADER
    assert [json.loads(line) for line in lines[1:]] == [
        _entry(n).to_json() for n in range(3)
    ]


def test_the_ledger_stays_owner_only_after_appends(cfg):
    for n in range(3):
        adopt_apply.mark_applied(cfg, _entry(n))
    if config._CAN_SET_MODE:
        assert adopt_apply.path_for(cfg).stat().st_mode & 0o777 == 0o600


@pytest.mark.parametrize("field", ["entry_id", "tree", "content_id", "actor"])
def test_a_record_the_reader_would_refuse_is_never_written(cfg, field):
    """A mark the reader cannot read back would make the whole ledger refuse."""
    adopt_apply.mark_applied(cfg, _entry(0))
    before = adopt_apply.path_for(cfg).read_bytes()
    fields = {
        "entry_id": "genre_energy:entry-000009",
        "tree": "genre_energy",
        "content_id": "9",
        "bucket": "house",
        "sub": "med",
        "actor": "a-person",
        "digest": "0" * 16,
        "applied": "2026-11-12T00:00:00+00:00",
    }
    fields[field] = ""
    with pytest.raises(CratekitError) as excinfo:
        adopt_apply.mark_applied(cfg, adopt_apply.AppliedEntry(**fields))
    assert excinfo.value.cause.reason == "adoption-ledger-unusable"
    assert adopt_apply.path_for(cfg).read_bytes() == before
    assert adopt_apply.read(cfg).entry_ids() == {_entry(0).entry_id}


def test_a_re_mark_replaces_the_earlier_record_as_the_document_did(cfg):
    """``with_applied`` replaced a record with the same id; the fold keeps that."""
    adopt_apply.mark_applied(cfg, _entry(0, actor="first"))
    adopt_apply.mark_applied(cfg, _entry(1))
    adopt_apply.mark_applied(cfg, _entry(0, actor="second"))
    ledger = adopt_apply.read(cfg)
    assert [entry.entry_id for entry in ledger.applied] == [
        _entry(0).entry_id,
        _entry(1).entry_id,
    ]
    assert ledger.applied[0].actor == "second"


def test_two_plans_marking_in_turn_keep_both(cfg):
    """More than one plan accumulates in one ledger, interleaved mark by mark."""
    for n in range(4):
        adopt_apply.mark_applied(cfg, _entry(n, tree="genre_energy"))
        adopt_apply.mark_applied(cfg, _entry(n, tree="shelf_stack"))
    ledger = adopt_apply.read(cfg)
    assert {entry.tree for entry in ledger.applied} == {"genre_energy", "shelf_stack"}
    assert ledger.entry_ids() == {
        _entry(n, tree=tree).entry_id
        for n in range(4)
        for tree in ("genre_energy", "shelf_stack")
    }


_MARKER = """
import sys
from pathlib import Path
from cratekit.adopt import apply
from cratekit.core import config
from tests.test_config import valid_data

root, worker = Path(sys.argv[1]), sys.argv[2]
cfg = config.from_dict(valid_data(root))
for n in range(25):
    apply.mark_applied(
        cfg,
        apply.AppliedEntry(
            entry_id=f"{worker}:{n:03d}", tree=worker, content_id=str(n),
            bucket="house", sub="med", actor="a-person", digest="0" * 16,
            applied="2026-11-12T00:00:00+00:00",
        ),
    )
"""


def test_four_real_processes_marking_at_once_lose_nothing(library, tmp_path):
    """The lock is what a read, append or repair needs between processes.

    Real interpreters rather than threads, because what is proved is what
    reached the disk while another process held the lock.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([str(SRC_ROOT), str(SRC_ROOT.parent)])
    running = [
        subprocess.Popen(
            [sys.executable, "-c", _MARKER, str(library), f"w{worker}"],
            env=env,
            cwd=str(SRC_ROOT.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for worker in range(4)
    ]
    for process in running:
        _out, err = process.communicate(timeout=120)
        assert process.returncode == 0, err.decode()
    cfg_value = config.from_dict(valid_data(library))
    ledger = adopt_apply.read(cfg_value)
    assert len(ledger.applied) == 100
    assert all(json.loads(line) for line in _lines(adopt_apply.path_for(cfg_value)))


# ═══════════════════════════════════════════════════════════════════════════
# A ledger written before U254
# ═══════════════════════════════════════════════════════════════════════════


def _plant(cfg_value, payload: bytes | str) -> Path:
    path = adopt_apply.path_for(cfg_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    path.write_bytes(payload)
    return path


def test_a_ledger_written_before_u254_reads_the_same(cfg):
    path = _plant(cfg, DOCUMENT_BEFORE_U254)
    assert adopt_apply.read(cfg) == adopt_apply.AppliedLedger(RECORDS_BEFORE_U254)
    assert path.read_text() == DOCUMENT_BEFORE_U254, "a read rewrote the document"


def test_a_mark_on_a_ledger_written_before_u254_keeps_every_record(cfg, monkeypatch):
    """Rewritten once as a journal, then appended to like any other."""
    path = _plant(cfg, DOCUMENT_BEFORE_U254)
    seen = _count_writes(monkeypatch)
    adopt_apply.mark_applied(cfg, _entry(0))
    adopt_apply.mark_applied(cfg, _entry(1))

    assert (seen.rewrites, seen.appends) == (1, 1)
    assert _lines(path)[0] + b"\n" == HEADER
    ledger = adopt_apply.read(cfg)
    assert ledger == adopt_apply.AppliedLedger(
        tuple(
            sorted(
                (*RECORDS_BEFORE_U254, _entry(0), _entry(1)),
                key=lambda held: held.entry_id,
            )
        )
    )


def test_a_damaged_ledger_written_before_u254_still_refuses_a_mark(cfg):
    """The old document's refusals hold for the mark as they did for the read."""
    path = _plant(cfg, DOCUMENT_BEFORE_U254[:-40])
    with pytest.raises(CratekitError) as excinfo:
        adopt_apply.mark_applied(cfg, _entry(0))
    assert excinfo.value.cause.reason == "adoption-ledger-unusable"
    assert path.read_text() == DOCUMENT_BEFORE_U254[:-40]


def test_a_document_at_the_journal_schema_refuses(cfg):
    """No build ever wrote the ledger whole at schema 2, so one that says so is damage."""
    path = _plant(cfg, '{"schema_version": 2, "applied": []}')
    with pytest.raises(adopt_apply.AppliedLedgerUnreadable) as excinfo:
        adopt_apply.read(cfg)
    assert excinfo.value.remedy is Remedy.RUN_DOCTOR
    assert path.read_text() == '{"schema_version": 2, "applied": []}'


def test_a_newer_document_still_asks_for_an_upgrade(cfg):
    _plant(cfg, '{"schema_version": 3, "applied": []}')
    with pytest.raises(adopt_apply.AppliedLedgerUnreadable) as excinfo:
        adopt_apply.read(cfg)
    assert excinfo.value.remedy is Remedy.UPGRADE_CRATEKIT


# ═══════════════════════════════════════════════════════════════════════════
# A torn last record, decided: read as the mark that did not finish
# ═══════════════════════════════════════════════════════════════════════════


def _journal_of(count: int) -> bytes:
    return HEADER + b"".join(
        json.dumps(_entry(n).to_json(), sort_keys=True).encode("utf-8") + b"\n"
        for n in range(count)
    )


_FOURTH = json.dumps(_entry(3).to_json(), sort_keys=True).encode("utf-8")

TORN_TAILS = {
    "a few bytes of a record": _FOURTH[:5],
    "half a record": _FOURTH[: len(_FOURTH) // 2],
    "a whole record with no newline": _FOURTH,
    "zeros where the record was": b"\x00" * 40,
    "zeros then the record's last page": b"\x00" * 30 + _FOURTH[30:] + b"\n",
    "an empty last line": b"\n",
}


@pytest.mark.parametrize("tail", TORN_TAILS.values(), ids=TORN_TAILS.keys())
def test_a_torn_last_record_is_the_mark_that_did_not_finish(cfg, tail):
    """Every whole record before it is kept; the torn one reads as not applied.

    Not applied is the safe direction: the mark is the last act of an entry, so
    a mark that did not land is the documented crash between the tag write and
    the applied record, which a resume re-applies without refreshing the revert
    record. Read as empty, it would re-apply the plan from its first entry.
    """
    path = _plant(cfg, _journal_of(3) + tail)
    assert adopt_apply.read(cfg).entry_ids() == {_entry(n).entry_id for n in range(3)}
    assert path.read_bytes() == _journal_of(3) + tail, "a read repaired the file"


@pytest.mark.parametrize("tail", TORN_TAILS.values(), ids=TORN_TAILS.keys())
def test_the_next_mark_cuts_a_torn_record_away(cfg, monkeypatch, tail):
    """Appending after torn bytes would bury them mid file, where they refuse."""
    path = _plant(cfg, _journal_of(3) + tail)
    seen = _count_writes(monkeypatch)
    adopt_apply.mark_applied(cfg, _entry(7))
    adopt_apply.mark_applied(cfg, _entry(8))
    assert (seen.rewrites, seen.appends) == (1, 1), "the repair was not one rewrite"
    assert adopt_apply.read(cfg).entry_ids() == {
        _entry(n).entry_id for n in (0, 1, 2, 7, 8)
    }
    assert all(json.loads(line) for line in _lines(path))


WRONG_JOURNALS = {
    "a damaged line before the last": (
        HEADER + b'{"actor": "a-pe\n' + _journal_of(2)[len(HEADER) :],
        Remedy.RUN_DOCTOR,
    ),
    "two torn lines at the end": (
        _journal_of(2) + b'{"actor": "a-pe\n' + b'{"act',
        Remedy.RUN_DOCTOR,
    ),
    "a record missing its actor, last": (
        _journal_of(2)
        + json.dumps({k: v for k, v in _entry(5).to_json().items() if k != "actor"})
        .encode()
        + b"\n",
        Remedy.RUN_DOCTOR,
    ),
    "a record that is a list": (_journal_of(1) + b"[1, 2]\n" + _journal_of(2)[len(HEADER) :], Remedy.RUN_DOCTOR),
    "a header from a newer build": (
        b'{"format": "journal", "schema_version": 3}\n' + _journal_of(1)[len(HEADER) :],
        Remedy.UPGRADE_CRATEKIT,
    ),
    "a header with a string version": (
        b'{"format": "journal", "schema_version": "2"}\n' + _journal_of(1)[len(HEADER) :],
        Remedy.RUN_DOCTOR,
    ),
    "a header with an older version": (
        b'{"format": "journal", "schema_version": 1}\n' + _journal_of(1)[len(HEADER) :],
        Remedy.RUN_DOCTOR,
    ),
    "a header alone with no newline": (HEADER[:-1], Remedy.RUN_DOCTOR),
    "a damaged header": (b'{"format": "jour\n' + _journal_of(1)[len(HEADER) :], Remedy.RUN_DOCTOR),
    "an empty file": (b"", Remedy.RUN_DOCTOR),
}


@pytest.mark.parametrize(
    ("payload", "remedy"), WRONG_JOURNALS.values(), ids=WRONG_JOURNALS.keys()
)
def test_a_wrong_journal_refuses_rather_than_reading_as_empty(cfg, payload, remedy):
    """Only the LAST line may be torn; everything else wrong refuses as before."""
    path = _plant(cfg, payload)
    with pytest.raises(adopt_apply.AppliedLedgerUnreadable) as excinfo:
        adopt_apply.read(cfg)
    assert excinfo.value.cause.reason == "adoption-ledger-unusable"
    assert excinfo.value.remedy is remedy
    with pytest.raises(adopt_apply.AppliedLedgerUnreadable):
        adopt_apply.mark_applied(cfg, _entry(9))
    assert path.read_bytes() == payload, "a refused ledger was written over"


def test_a_header_alone_is_a_ledger_with_nothing_applied(cfg):
    _plant(cfg, HEADER)
    assert adopt_apply.read(cfg) == adopt_apply.EMPTY


# ═══════════════════════════════════════════════════════════════════════════
# An apply killed at every mark resumes with exactly the marks that landed
# ═══════════════════════════════════════════════════════════════════════════

PLAN_SIZE = 5


def _five(cfg_value, declared_taxonomy):
    _routable, genre = _bucket_and_genre(declared_taxonomy)
    rows = [
        _row(cfg_value, f"Track {n:02d}.flac", genre, f"c{n:02d}")
        for n in range(1, PLAN_SIZE + 1)
    ]
    return _plan_of(cfg_value, declared_taxonomy, rows)


def _kill_ledger_write(monkeypatch, cfg_value, *, at: int, keep: int | None = None):
    """Make the ``at``-th write to the applied ledger kill the process.

    ``keep`` of None kills before any byte lands; a number lands that many bytes
    of the record first, through the real writer, which is a write torn by a
    kill, and a negative one all but that many. A ``keep`` past the record's
    length lands all of it and then kills, before the mark returns. Counted over both writers, because the first mark creates the file
    and every later one appends.
    """
    calls = {"n": 0}
    real_rewrite = config.atomic_write_bytes
    real_append = config.append_durable_bytes
    ledger = adopt_apply.path_for(cfg_value)

    def rewrite(payload, path, *args, **kwargs):
        if path == ledger:
            calls["n"] += 1
            if calls["n"] == at:
                raise _Killed(f"killed at ledger write {at}")
        return real_rewrite(payload, path, *args, **kwargs)

    def append(payload, path, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] == at:
            if keep is not None:
                landed = payload[:keep]
                if landed:
                    real_append(landed, path, *args, **kwargs)
            raise _Killed(f"killed at ledger write {at}")
        return real_append(payload, path, *args, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", rewrite)
    monkeypatch.setattr(config, "append_durable_bytes", append)


def _resume_and_check(cfg_value, declared_taxonomy, plan, granted, *, marked: int):
    ids = [entry.entry_id for entry in plan.applicable()]
    assert adopt_apply.read(cfg_value).entry_ids() == frozenset(ids[:marked]), (
        f"an apply killed at mark {marked + 1} did not read as exactly {marked} marked"
    )
    resumed: list[str] = []
    report = adopt_apply.apply_plan(
        cfg_value,
        plan,
        declared_taxonomy,
        approval=granted,
        place=lambda entry, _f, _s: resumed.append(entry.entry_id),
    )
    assert resumed == ids[marked:], "the resume placed the wrong entries"
    assert report.already_applied == tuple(ids[:marked])
    assert report.resumed_at == (marked + 1 if marked < len(ids) else None)
    assert adopt_apply.read(cfg_value).entry_ids() == frozenset(ids)
    assert all(json.loads(line) for line in _lines(adopt_apply.path_for(cfg_value)))


@pytest.mark.parametrize("marked", range(PLAN_SIZE))
def test_an_apply_killed_at_each_mark_resumes_with_exactly_the_marks_before_it(
    cfg, declared, monkeypatch, marked
):
    """The write of mark k + 1 made to fail, for every k the plan has."""
    plan = _five(cfg, declared)
    assert len(plan.applicable()) == PLAN_SIZE
    granted = adopt_approval.grant(plan, actor="tester")
    placed: list[str] = []
    with monkeypatch.context() as patched:
        _kill_ledger_write(patched, cfg, at=marked + 1)
        with pytest.raises(_Killed):
            adopt_apply.apply_plan(
                cfg,
                plan,
                declared,
                approval=granted,
                place=lambda entry, _f, _s: placed.append(entry.entry_id),
            )
    assert len(placed) == marked + 1, "the kill did not land on the mark it named"
    _resume_and_check(cfg, declared, plan, granted, marked=marked)


#: Past any record's length, so the whole record lands before the kill.
WHOLE_RECORD = 1 << 20


@pytest.mark.parametrize("marked", range(1, PLAN_SIZE))
@pytest.mark.parametrize("keep", [0, 1, 40, -2, -1], ids=["none", "one", "some", "all-but-two", "all-but-newline"])
def test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it(
    cfg, declared, monkeypatch, marked, keep
):
    """Mark k + 1 torn partway: k read as marked, and the resume repairs it."""
    plan = _five(cfg, declared)
    granted = adopt_approval.grant(plan, actor="tester")
    with monkeypatch.context() as patched:
        _kill_ledger_write(patched, cfg, at=marked + 1, keep=keep)
        with pytest.raises(_Killed):
            adopt_apply.apply_plan(
                cfg, plan, declared, approval=granted, place=lambda *_: None
            )
    _resume_and_check(cfg, declared, plan, granted, marked=marked)


@pytest.mark.parametrize("marked", range(1, PLAN_SIZE))
def test_a_kill_after_the_whole_record_landed_counts_the_mark(
    cfg, declared, monkeypatch, marked
):
    """The crash between the applied record and the end of the run: skipped after."""
    plan = _five(cfg, declared)
    granted = adopt_approval.grant(plan, actor="tester")
    with monkeypatch.context() as patched:
        _kill_ledger_write(patched, cfg, at=marked + 1, keep=WHOLE_RECORD)
        with pytest.raises(_Killed):
            adopt_apply.apply_plan(
                cfg, plan, declared, approval=granted, place=lambda *_: None
            )
    _resume_and_check(cfg, declared, plan, granted, marked=marked + 1)


def test_a_revert_after_a_partial_apply_restores_what_it_wrote(
    cfg, declared, monkeypatch, tmp_path
):
    """Killed at the third mark: three files were written, two marked, all three revert."""
    _routable, genre = _bucket_and_genre(declared)
    music = Path(cfg.library.root) / "Music"
    paths = []
    for n in range(4):
        path = music / f"Track {n}.flac"
        path.write_bytes(_synth_in(tmp_path / f"source{n}", ".flac").read_bytes())
        tags.write_genre(path, f"Original {n}")
        paths.append(path)
    rows = [
        adopt_scan.CollectionRow(str(path), str(path), genre, False) for path in paths
    ]
    plan = _plan_of(cfg, declared, rows)
    assert len(plan.applicable()) == 4
    granted = adopt_approval.grant(plan, actor="tester")

    with monkeypatch.context() as patched:
        _kill_ledger_write(patched, cfg, at=3)
        with pytest.raises(_Killed):
            adopt_apply.apply_plan(
                cfg,
                plan,
                declared,
                approval=granted,
                place=lambda *_: None,
                tag_value=lambda _entry, _declared: "Adopted Genre",
            )

    order = [Path(entry.path) for entry in plan.applicable()]
    written = order[:3]
    assert [tags.read_genre_from_file(path) for path in written] == ["Adopted Genre"] * 3
    assert tags.read_genre_from_file(order[3]) != "Adopted Genre"
    assert len(adopt_apply.read(cfg).applied) == 2

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}
    assert sorted(report.restored) == sorted((str(path), "genre") for path in written)
    originals = {path: f"Original {paths.index(path)}" for path in paths}
    assert [tags.read_genre_from_file(path) for path in paths] == [
        originals[path] for path in paths
    ]
