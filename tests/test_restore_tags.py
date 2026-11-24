"""R-1924: a restore of an ``analyze adopt`` session puts the files back beside the rows.

End to end on the native landing suite's disposable library, as
``tests/test_analyze_adopt.py`` drives the adopt: land headed tracks, simulate
rekordbox's visit, adopt, then ``crate restore run SESSION`` through the real
dispatcher, and read the row, the title tag and the key tag back. Then the
record reader and the put back on values built here. D1 applies.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.analysis import head_adopt as ha
from cratekit.core import reconcile, restore, restore_tags, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import native
from cratekit.write import metadata
from tests.cli_drive import drive
from tests.test_analyze_adopt import (
    BARE,
    LANDED,
    STAMPED,
    _bare_and_visited,
    _file,
    _id,
    _land_headed,
    _landed_and_visited,
    _surfaces,
    _two_acts,
    _visit,
)
from tests.test_analyze_adopt import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_analyze_adopt import full_machine as full_machine  # noqa: PLC0414
from tests.test_analyze_adopt import native_library as native_library  # noqa: PLC0414
from tests.test_inbox_refill import offline as offline  # noqa: PLC0414
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

GATE = "restore.run.confirm"


def _restore(*argv: str, expect: ExitCode | None = ExitCode.OK) -> dict:
    """``crate restore run`` with ``argv``, asked, answered ``restore``, exiting ``expect``.

    ``expect=None`` asserts only that the run did not exit OK."""
    verb = ["restore", "run", *argv]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "restore", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, envelope = drive(["--run", run_id, *verb])
    if expect is None:
        assert code != int(ExitCode.OK), envelope
    else:
        assert code == int(expect), envelope
    return envelope


def _adopt() -> dict:
    """Both acts of ``analyze adopt``, which exit OK; answers the acting envelope."""
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    return acted


def _the_other_adopt(cfg, first: str) -> str:
    """The one adopt session on the library other than ``first``."""
    adopts = [r.session_id for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    (other,) = [one for one in adopts if one != first]
    return other


def _tagged_copy(silence, tmp_path, title: str, key: str) -> Path:
    """A FLAC copy of ``silence`` whose title tag and key tag are written as given."""
    path = tmp_path / "a.flac"
    path.write_bytes(silence.read_bytes())
    assert tags.write_tags(path, {"title": title, "initialkey": key})
    return path


@pytest.fixture
def keyed(native_library, silence) -> tuple:
    """The library after ``_keyed_and_adopted``: its config, the surfaces before, the session."""
    cfg, _root = native_library
    return (cfg, *_keyed_and_adopted(cfg, silence))


def _adopted(cfg) -> session.SessionRecord:
    """The one adopt session on the library."""
    (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    return record


def _all(cfg) -> dict[str, tuple]:
    """(row Title, title tag, initialkey) of every landed track."""
    return {stem: _surfaces(cfg, stem)[:3] for stem in LANDED}


def _keyed_and_adopted(cfg, silence) -> tuple[dict[str, tuple], str]:
    """Land, visit, key Alpha's file, adopt: every surface before the adopt, and its session."""
    _landed_and_visited(cfg, silence)
    assert tags.write_tags(_file(cfg, "Alpha"), {"initialkey": "01A"})
    before = _all(cfg)
    acted = _adopt()
    assert _all(cfg) != before
    # THE ADOPT'S ANSWER SAYS WHAT A RESTORE OF IT NOW DOES.
    assert "puts the rows back and each file's old title tag and key tag" in (
        acted["warnings"][0]["message"]
    )
    return before, _adopted(cfg).session_id


# 1. The brief's scenarios, through the verb


def test_a_restore_puts_the_row_the_title_tag_and_the_key_tag_back(keyed):
    cfg, before, adopted = keyed
    assert _surfaces(cfg, "Golf")[:3] == ("09A - 98 - Golf", "09A - 98 - Golf", "09A")
    assert _surfaces(cfg, "Alpha")[2] == "07B"

    envelope = _restore(adopted)

    assert envelope["outcome"] == "ok"
    assert _all(cfg) == before
    # A KEY TAG THE FILE CARRIED IS PUT BACK AS IT WAS, and one it never had is absent.
    assert _surfaces(cfg, "Alpha")[2] == "01A"
    assert _surfaces(cfg, "Golf")[2] is None
    files = envelope["data"]["totals"]["file_tags"]
    assert files == {"planned": 5, "read_back": 5, "failed": [], "wrong": []}


def test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head(native_library, silence):
    """U342: a title that had no head and was stamped goes back to having none, on
    the row, the title tag and the key tag, beside a corrected row."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    _bare_and_visited(cfg, silence)
    stems = [*LANDED, *BARE]
    before = {stem: _surfaces(cfg, stem)[:3] for stem in stems}
    _adopt()
    assert _surfaces(cfg, "Tango")[:3] == (STAMPED["Tango"], STAMPED["Tango"], "09A")

    envelope = _restore(_adopted(cfg).session_id)

    assert {stem: _surfaces(cfg, stem)[:3] for stem in stems} == before
    assert _surfaces(cfg, "Tango")[:3] == ("[MP3] Tango", "[MP3] Tango", None)
    assert _surfaces(cfg, "Tango")[3] == "Tango.flac"
    files = envelope["data"]["totals"]["file_tags"]
    assert files == {"planned": 9, "read_back": 9, "failed": [], "wrong": []}


def test_a_blank_key_tag_is_put_back_absent_never_an_empty_tag(keyed):
    import mutagen

    cfg, _before, adopted = keyed

    _restore(adopted)

    handle = mutagen.File(_file(cfg, "Golf"))
    assert "initialkey" not in {str(key).lower() for key in (handle.tags or {}).keys()}


def test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok(
    keyed, monkeypatch
):
    cfg, before, adopted = keyed
    golf = _file(cfg, "Golf")
    real = tags.write_tags

    def refuses_golf(path, fields):
        return False if Path(path) == golf else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", refuses_golf)

    envelope = _restore(adopted, expect=ExitCode.PRECONDITION)

    cause = envelope["cause"]
    assert cause["reason"] == "restore-tags-unwritten"
    assert str(golf) in cause["message"]
    assert cause["detail"]["failed"] == [str(golf)]
    assert cause["detail"]["session"] == adopted
    assert f"run the same restore of session {adopted} again" in " ".join(
        cause["remediation"]["steps"]
    )
    # THE DATABASE HALF LANDED AND THE REST OF THE FILES WITH IT.
    assert _surfaces(cfg, "Golf")[:3] == (before["Golf"][0], "09A - 98 - Golf", "09A")
    assert {stem: v for stem, v in _all(cfg).items() if stem != "Golf"} == {
        stem: v for stem, v in before.items() if stem != "Golf"
    }
    # WHAT THE RESTORE DID IS KEPT ON THE REFUSAL.
    assert envelope["data"]["totals"]["file_tags"]["read_back"] == 4


def test_a_file_that_does_not_read_back_is_named(keyed, monkeypatch):
    cfg, _before, adopted = keyed
    golf = _file(cfg, "Golf")
    real = tags.write_tags

    def says_it_wrote_golf(path, fields):
        return True if Path(path) == golf else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", says_it_wrote_golf)

    envelope = _restore(adopted, expect=ExitCode.PRECONDITION)

    assert envelope["cause"]["reason"] == "restore-tags-unwritten"
    assert envelope["cause"]["detail"]["wrong"] == [str(golf)]
    assert "do not read back" in envelope["cause"]["message"]


def test_a_file_gone_since_the_adopt_is_named(keyed):
    cfg, _before, adopted = keyed
    golf = _file(cfg, "Golf")
    golf.unlink()

    envelope = _restore(adopted, expect=ExitCode.PRECONDITION)

    assert envelope["cause"]["detail"]["failed"] == [str(golf)]


def test_a_session_with_no_kept_tags_restores_as_before(native_library, silence):
    cfg, _root = native_library
    _land_headed(cfg, silence, "2026-11-22_first", {"Kilo": "03A - 120"})
    kilo = _file(cfg, "Kilo")
    tagged = tags.read_tags(kilo, ("title", "initialkey"))
    (landing,) = [r for r in session.records(cfg) if r.snapshot_path]
    assert restore_tags.RECORD_KEY not in landing.detail

    envelope = _restore(landing.session_id)

    assert envelope["outcome"] == "ok"
    assert envelope["data"]["totals"]["file_tags"] == {
        "planned": 0, "read_back": 0, "failed": [], "wrong": [],
    }
    assert tags.read_tags(kilo, ("title", "initialkey")) == tagged


def test_a_dry_run_puts_no_file_back(keyed):
    cfg, _before, adopted = keyed
    adopted_now = _all(cfg)

    envelope = _restore(adopted, "--dry-run")

    assert _all(cfg) == adopted_now
    assert envelope["data"]["totals"]["file_tags"]["planned"] == 5
    assert envelope["data"]["totals"]["file_tags"]["read_back"] == 0


def test_a_record_it_cannot_read_refuses_before_the_database_is_replaced(
    keyed
):
    cfg, _before, adopted = keyed
    record = _adopted(cfg)
    record.detail[restore_tags.RECORD_KEY] = {"not": "a list"}
    session.write_record(record, cfg)
    adopted_now = _all(cfg)

    envelope = _restore(adopted, expect=None)

    assert envelope["cause"]["reason"] == "restore-record-unusable"
    assert restore_tags.RECORD_KEY in envelope["cause"]["message"]
    assert _all(cfg) == adopted_now


def test_a_later_adopt_the_restore_discards_puts_its_files_back_too(keyed):
    """The restore goes back to before the earliest session, so the earliest
    session's before value is the one a file takes, never a later one's."""
    cfg, before, first = keyed
    assert _surfaces(cfg, "Charlie")[1] == before["Charlie"][1]
    _visit(cfg, "Alpha", scale="4A", bpm=12400)
    # A FILE ONLY THE LATER SESSION NAMES: Charlie agreed at the first adopt.
    _visit(cfg, "Charlie", scale="3A", bpm=12400)
    _adopt()
    second = _the_other_adopt(cfg, first)
    assert _surfaces(cfg, "Alpha")[1:3] == ("04A - 124 - Alpha", "04A")
    assert _surfaces(cfg, "Charlie")[1:3] == ("03A - 124 - Charlie", "03A")

    envelope = _restore(first, "--discard", second)

    assert _all(cfg) == before
    assert envelope["data"]["totals"]["file_tags"]["planned"] == 6


# 2. The record reader and the put back, on values built here


def _record(detail: dict) -> session.SessionRecord:
    return session.SessionRecord(
        session_id="s-1", workflow=ha.WORKFLOW, started="2026-11-23T00:00:00Z", detail=detail
    )


def test_the_key_is_the_one_the_adopt_writes():
    assert restore_tags.RECORD_KEY == ha.RECORD_KEY


def test_the_part_is_re_exported_by_the_restore():
    assert restore.restore_tags is restore_tags


@pytest.mark.parametrize(
    "kept",
    [
        pytest.param("a string", id="not-a-list"),
        pytest.param({"path": "/x"}, id="a-mapping"),
        pytest.param(["entry"], id="an-entry-not-a-mapping"),
        pytest.param([{"tag_title": "t", "initialkey": ""}], id="no-path"),
        pytest.param([{"path": "", "tag_title": "t", "initialkey": ""}], id="an-empty-path"),
        pytest.param([{"path": "/x", "initialkey": ""}], id="no-title"),
        pytest.param([{"path": "/x", "tag_title": "t"}], id="no-key"),
        pytest.param([{"path": "/x", "tag_title": None, "initialkey": ""}], id="a-null-title"),
        pytest.param([{"path": "/x", "tag_title": "t", "initialkey": 8}], id="a-number-key"),
        pytest.param([{"path": "x.flac", "tag_title": "t", "initialkey": ""}], id="relative"),
        pytest.param([{"path": " ", "tag_title": "t", "initialkey": ""}], id="a-blank-path"),
        pytest.param([{"path": "/x ", "tag_title": "t", "initialkey": ""}], id="padded"),
        pytest.param([{"path": "/x", "tag_title": " ", "initialkey": ""}], id="a-blank-title"),
    ],
)
def test_a_record_kept_in_another_shape_refuses(kept):
    with pytest.raises(CratekitError) as refused:
        restore_tags.kept_by(_record({restore_tags.RECORD_KEY: kept}))
    assert refused.value.cause.reason == "restore-record-unusable"
    assert refused.value.cause.detail["session_id"] == "s-1"
    assert "run the restore again" in " ".join(refused.value.cause.remediation.steps)


def test_a_record_with_no_key_keeps_nothing():
    assert restore_tags.kept_by(_record({})) == ()
    assert restore_tags.kept_by(_record({restore_tags.RECORD_KEY: []})) == ()


def test_the_first_record_to_name_a_file_wins_and_each_path_is_rebased():
    def entry(path: str, title: str, key: str) -> dict:
        return {"content_id": "1", "path": path, "title": title, "tag_title": title,
                "initialkey": key}

    earlier = _record({restore_tags.RECORD_KEY: [entry("/old/a.flac", "A0", ""),
                                                  entry("/old/b.flac", "B0", "02A")]})
    later = session.SessionRecord(
        session_id="s-2", workflow=ha.WORKFLOW, started="2026-11-23T01:00:00Z",
        detail={restore_tags.RECORD_KEY: [entry("/old/a.flac", "A1", "07B"),
                                          entry("/old/c.flac", "C1", "")]},
    )

    found = restore_tags.befores((earlier, later), rebased=lambda path: Path("/new") / path.name)

    assert [(str(f.path), f.title, f.initialkey, f.session_id) for f in found] == [
        ("/new/a.flac", "A0", "", "s-1"),
        ("/new/b.flac", "B0", "02A", "s-1"),
        ("/new/c.flac", "C1", "", "s-2"),
    ]


def _before(path: Path, title: str, key: str) -> restore_tags.FileBefore:
    return restore_tags.FileBefore(path, title, key, "s-1")


def test_a_file_already_as_it_was_writes_nothing_and_reads_back(silence, tmp_path, monkeypatch):
    path = _tagged_copy(silence, tmp_path, "01A - 124 - A", "01A")
    writes: list = []
    monkeypatch.setattr(tags, "write_tags", lambda *a: writes.append(a) or True)
    monkeypatch.setattr(tags, "clear_tags", lambda *a: writes.append(a) or True)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "01A")])

    assert writes == []
    assert done.read_back == (str(path),) and not done.unwritten


def test_only_the_tag_that_differs_is_written(silence, tmp_path, monkeypatch):
    path = _tagged_copy(silence, tmp_path, "09A - 98 - A", "01A")
    real = tags.write_tags
    asked: list[dict] = []

    def noting(where, fields):
        asked.append(dict(fields))
        return real(where, fields)

    monkeypatch.setattr(tags, "write_tags", noting)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "01A")])

    assert asked == [{"title": "01A - 124 - A"}]
    assert done.read_back == (str(path),)


def test_an_unknown_container_is_one_failed_file(tmp_path):
    odd = tmp_path / "a.xyz"
    odd.write_bytes(b"not audio")

    done = restore_tags.put_back([_before(odd, "01A - 124 - A", "")])

    assert done.failed == (str(odd),) and done.unwritten == (str(odd),)


def test_a_clear_that_fails_is_a_failed_file(silence, tmp_path, monkeypatch):
    path = _tagged_copy(silence, tmp_path, "01A - 124 - A", "09A")
    monkeypatch.setattr(tags, "clear_tags", lambda *a: False)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "")])

    assert done.failed == (str(path),)


def test_the_answer_carries_every_count_and_every_name():
    done = restore_tags.TagsPutBack(4, ("/a",), ("/b",), ("/c", "/d"))
    assert done.to_json() == {
        "planned": 4, "read_back": 1, "failed": ["/b"], "wrong": ["/c", "/d"],
    }
    assert done.unwritten == ("/b", "/c", "/d")


def test_the_session_record_round_trips_what_the_adopt_kept(keyed):
    """The record read from disk is what the put back reads, not the one in memory."""
    cfg, _before, adopted = keyed
    on_disk = json.loads(session.log_path(adopted, cfg).read_text())
    found = restore_tags.kept_by(session.read_record(adopted, cfg))
    assert len(found) == len(on_disk["detail"][restore_tags.RECORD_KEY]) == 5
    assert {str(f.path) for f in found} >= {str(_file(cfg, "Golf"))}


# 3. Review round one


def _stopped_adopt(cfg, monkeypatch) -> str:
    """An adopt that wrote its files and stopped before the rows: no commit."""
    real = metadata.write_plan

    def stops(*args, **kwargs):
        raise RuntimeError("the process died between the files and the rows")

    monkeypatch.setattr(metadata, "write_plan", stops)
    code, acted, _refused = _two_acts()
    assert code != int(ExitCode.OK), acted
    monkeypatch.setattr(metadata, "write_plan", real)
    record = _adopted(cfg)
    assert not restore._committed(record)
    return record.session_id


def _landing_of(cfg, stem: str) -> str:
    """The landing session that landed ``stem``, chosen by its row, never by order."""
    content_id = _id(cfg, stem)
    (landing,) = [
        one.session_id
        for one in session.records(cfg)
        if content_id
        in {
            row["content_id"]
            for row in one.detail.get(native.LANDED_ROWS_KEY, {}).get("rows", ())
        }
    ]
    return landing


def _tagged(paths: dict[str, Path]) -> dict[str, tuple]:
    return {
        stem: tuple(tags.read_tags(path, ("title", "initialkey")).values())
        for stem, path in paths.items()
    }


@pytest.mark.parametrize("left", ["abandoned", "open"])
def test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back(
    native_library, silence, monkeypatch, left
):
    """B1: a commit is no evidence about files. A restore of an earlier session
    reads every later record that kept tags, committed or not, and asks no discard
    for one that committed nothing."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    paths = {stem: _file(cfg, stem) for stem in LANDED}
    before = _tagged(paths)
    landing = _landing_of(cfg, "Golf")
    stopped = _stopped_adopt(cfg, monkeypatch)
    if left == "open":
        # A PROCESS KILLED OUTRIGHT leaves its record open (review round two).
        record = session.read_record(stopped, cfg)
        record.state = session.SessionState.OPEN
        session.write_record(record, cfg)
    assert _surfaces(cfg, "Golf")[1:3] == ("09A - 98 - Golf", "09A")
    assert _surfaces(cfg, "Golf")[0] == "01A - 124 - Golf"

    envelope = _restore(landing)

    assert envelope["data"]["totals"]["file_tags"] == {
        "planned": 5, "read_back": 5, "failed": [], "wrong": [],
    }
    assert _tagged(paths) == before
    assert stopped != landing


def test_the_files_go_back_with_the_latch_still_held(keyed, monkeypatch):
    """Review round one, R2: the database is already back and the restore still
    says it has not finished while the files are written."""
    cfg, _before, adopted = keyed
    real = restore_tags.put_back
    seen: list[tuple] = []

    def noting(planned, *, dry_run=False):
        latched = [r.marker.kind for r in reconcile.outstanding(cfg)]
        seen.append((latched, _surfaces(cfg, "Golf")[0]))
        return real(planned, dry_run=dry_run)

    monkeypatch.setattr(restore_tags, "put_back", noting)

    _restore(adopted)

    ((latched, row_title),) = seen
    assert reconcile.Kind.IN_FLIGHT_RESTORE in latched
    assert row_title == "01A - 124 - Golf"
    assert not reconcile.outstanding(cfg)


def test_a_key_tag_that_does_not_come_back_is_named(silence, tmp_path, monkeypatch):
    path = _tagged_copy(silence, tmp_path, "01A - 124 - A", "09A")
    monkeypatch.setattr(tags, "clear_tags", lambda *a: True)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "")])

    assert done.wrong == (str(path),) and not done.read_back


def test_a_file_that_cannot_be_read_back_is_named(silence, tmp_path, monkeypatch):
    path = _tagged_copy(silence, tmp_path, "09A - 98 - A", "09A")
    real = tags.read_tags_checked
    reads: list[int] = []

    def fails_the_second(where, fields):
        reads.append(1)
        if len(reads) > 1:
            raise tags.TagReadFailed("gone unreadable")
        return real(where, fields)

    monkeypatch.setattr(tags, "read_tags_checked", fails_the_second)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "01A")])

    assert done.wrong == (str(path),)


def test_a_dry_run_finds_a_file_gone_and_refuses_as_the_run_would(keyed):
    """Review round one, R3: the rehearsal proves this refusal too, writing nothing."""
    cfg, _before, adopted = keyed
    golf = _file(cfg, "Golf")
    golf.unlink()
    rows = _surfaces(cfg, "Alpha")[0]

    envelope = _restore(adopted, "--dry-run", expect=ExitCode.PRECONDITION)

    cause = envelope["cause"]
    assert cause["reason"] == "restore-tags-unwritten"
    assert "a dry run" in cause["message"] and str(golf) in cause["message"]
    assert cause["detail"]["failed"] == [str(golf)]
    assert cause["detail"]["wrong"] == []
    assert _surfaces(cfg, "Alpha")[:3] == (rows, "07B - 124 - Alpha", "07B")


def test_a_dry_run_writes_no_file(silence, tmp_path, monkeypatch):
    path = _tagged_copy(silence, tmp_path, "09A - 98 - A", "09A")
    monkeypatch.setattr(tags, "write_tags", lambda *a: pytest.fail("a dry run wrote"))
    monkeypatch.setattr(tags, "clear_tags", lambda *a: pytest.fail("a dry run cleared"))

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "")], dry_run=True)

    assert done == restore_tags.TagsPutBack(1)


# 4. Review round two


def test_a_restore_of_the_later_adopt_leaves_the_earlier_one_s_files(keyed):
    """Only sessions that started after the one restored are read: an earlier
    adopt's files keep what it wrote, as its rows do."""
    cfg, _before, first = keyed
    adopted = _all(cfg)
    _visit(cfg, "Alpha", scale="4A", bpm=12400)
    _adopt()
    second = _the_other_adopt(cfg, first)

    envelope = _restore(second)

    assert envelope["data"]["totals"]["file_tags"]["planned"] == 1
    assert _all(cfg) == adopted


def test_two_later_adopts_put_a_file_back_to_before_the_earlier(native_library, silence):
    """Among the later sessions the earliest wins, so a file read by two goes back
    to before the first of them, never to the second's before value."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    paths = {stem: _file(cfg, stem) for stem in LANDED}
    before = _tagged(paths)
    landing = _landing_of(cfg, "Golf")
    _adopt()
    _visit(cfg, "Alpha", scale="4A", bpm=12400)
    _adopt()
    adopts = [r.session_id for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    assert len(adopts) == 2

    _restore(landing, *[f for one in adopts for f in ("--discard", one)])

    assert _tagged(paths) == before


def test_a_dry_run_counts_a_file_it_cannot_read_as_failed(tmp_path):
    path = tmp_path / "a.flac"
    path.write_bytes(b"not audio at all")

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "")], dry_run=True)

    assert done.failed == (str(path),) and not done.read_back


def test_the_title_tag_goes_back_to_the_file_s_own_value_not_the_row_s(
    native_library, silence
):
    """The adopt compares a title tag with its row by body alone, so a file whose
    tag carries another head than its row's is adopted, and the restore puts back
    the tag's own head (the table's T6, which no earlier test reached)."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    golf = _file(cfg, "Golf")
    assert tags.write_tags(golf, {"title": "05A - 124 - Golf"})
    _adopt()
    assert _surfaces(cfg, "Golf")[:2] == ("09A - 98 - Golf", "09A - 98 - Golf")

    _restore(_adopted(cfg).session_id)

    assert _surfaces(cfg, "Golf")[:3] == ("01A - 124 - Golf", "05A - 124 - Golf", None)
