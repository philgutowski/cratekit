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
from cratekit.core import restore, restore_tags, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests.cli_drive import drive
from tests.test_analyze_adopt import (
    LANDED,
    _file,
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


def _restore(*argv: str) -> tuple[int, dict]:
    """``crate restore run`` with ``argv``, asked and then answered ``restore``."""
    verb = ["restore", "run", *argv]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "restore", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    return drive(["--run", run_id, *verb])


def _adopted(cfg) -> session.SessionRecord:
    """The one adopt session on the library."""
    (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    return record


def _all(cfg) -> dict[str, tuple]:
    """(row Title, title tag, initialkey) of every landed track."""
    return {stem: _surfaces(cfg, stem)[:3] for stem in LANDED}


def _keyed_and_adopted(cfg, silence) -> tuple[dict[str, tuple], str]:
    """Land and visit, give Alpha's file a key tag of its own, then adopt.

    Answers every track's surfaces before the adopt and the adopt's session.
    """
    _landed_and_visited(cfg, silence)
    assert tags.write_tags(_file(cfg, "Alpha"), {"initialkey": "01A"})
    before = _all(cfg)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert _all(cfg) != before
    return before, _adopted(cfg).session_id


# 1. The brief's scenarios, through the verb


def test_a_restore_puts_the_row_the_title_tag_and_the_key_tag_back(native_library, silence):
    cfg, _root = native_library
    before, adopted = _keyed_and_adopted(cfg, silence)
    assert _surfaces(cfg, "Golf")[:3] == ("09A - 98 - Golf", "09A - 98 - Golf", "09A")
    assert _surfaces(cfg, "Alpha")[2] == "07B"

    code, envelope = _restore(adopted)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert _all(cfg) == before
    # A KEY TAG THE FILE CARRIED IS PUT BACK AS IT WAS, and one it never had is absent.
    assert _surfaces(cfg, "Alpha")[2] == "01A"
    assert _surfaces(cfg, "Golf")[2] is None
    files = envelope["data"]["totals"]["file_tags"]
    assert files == {"planned": 5, "read_back": 5, "failed": [], "wrong": []}


def test_a_blank_key_tag_is_put_back_absent_never_an_empty_tag(native_library, silence):
    import mutagen

    cfg, _root = native_library
    _before, adopted = _keyed_and_adopted(cfg, silence)

    code, envelope = _restore(adopted)

    assert code == int(ExitCode.OK), envelope
    handle = mutagen.File(_file(cfg, "Golf"))
    assert "initialkey" not in {str(key).lower() for key in (handle.tags or {}).keys()}


def test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    before, adopted = _keyed_and_adopted(cfg, silence)
    golf = _file(cfg, "Golf")
    real = tags.write_tags

    def refuses_golf(path, fields):
        return False if Path(path) == golf else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", refuses_golf)

    code, envelope = _restore(adopted)

    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "restore-tags-unwritten"
    assert str(golf) in cause["message"]
    assert cause["detail"]["failed"] == [str(golf)]
    assert cause["detail"]["session"] == adopted
    # THE DATABASE HALF LANDED AND THE REST OF THE FILES WITH IT.
    assert _surfaces(cfg, "Golf")[:3] == (before["Golf"][0], "09A - 98 - Golf", "09A")
    assert {stem: v for stem, v in _all(cfg).items() if stem != "Golf"} == {
        stem: v for stem, v in before.items() if stem != "Golf"
    }
    # WHAT THE RESTORE DID IS KEPT ON THE REFUSAL.
    assert envelope["data"]["totals"]["file_tags"]["read_back"] == 4


def test_a_file_that_does_not_read_back_is_named(native_library, silence, monkeypatch):
    cfg, _root = native_library
    _before, adopted = _keyed_and_adopted(cfg, silence)
    golf = _file(cfg, "Golf")
    real = tags.write_tags

    def says_it_wrote_golf(path, fields):
        return True if Path(path) == golf else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", says_it_wrote_golf)

    code, envelope = _restore(adopted)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-tags-unwritten"
    assert envelope["cause"]["detail"]["wrong"] == [str(golf)]
    assert "do not read back" in envelope["cause"]["message"]


def test_a_file_gone_since_the_adopt_is_named(native_library, silence):
    cfg, _root = native_library
    _before, adopted = _keyed_and_adopted(cfg, silence)
    golf = _file(cfg, "Golf")
    golf.unlink()

    code, envelope = _restore(adopted)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["detail"]["failed"] == [str(golf)]


def test_a_session_with_no_kept_tags_restores_as_before(native_library, silence):
    cfg, _root = native_library
    _land_headed(cfg, silence, "2026-11-22_first", {"Kilo": "03A - 120"})
    kilo = _file(cfg, "Kilo")
    tagged = tags.read_tags(kilo, ("title", "initialkey"))
    (landing,) = [r for r in session.records(cfg) if r.snapshot_path]
    assert restore_tags.RECORD_KEY not in landing.detail

    code, envelope = _restore(landing.session_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["data"]["totals"]["file_tags"] == {
        "planned": 0, "read_back": 0, "failed": [], "wrong": [],
    }
    assert tags.read_tags(kilo, ("title", "initialkey")) == tagged


def test_a_dry_run_puts_no_file_back(native_library, silence):
    cfg, _root = native_library
    _before, adopted = _keyed_and_adopted(cfg, silence)
    adopted_now = _all(cfg)

    code, envelope = _restore(adopted, "--dry-run")

    assert code == int(ExitCode.OK), envelope
    assert _all(cfg) == adopted_now
    assert envelope["data"]["totals"]["file_tags"]["planned"] == 5
    assert envelope["data"]["totals"]["file_tags"]["read_back"] == 0


def test_a_record_it_cannot_read_refuses_before_the_database_is_replaced(
    native_library, silence
):
    cfg, _root = native_library
    _before, adopted = _keyed_and_adopted(cfg, silence)
    record = _adopted(cfg)
    record.detail[restore_tags.RECORD_KEY] = {"not": "a list"}
    session.write_record(record, cfg)
    adopted_now = _all(cfg)

    code, envelope = _restore(adopted)

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "restore-record-unusable"
    assert restore_tags.RECORD_KEY in envelope["cause"]["message"]
    assert _all(cfg) == adopted_now


def test_a_later_adopt_the_restore_discards_puts_its_files_back_too(native_library, silence):
    """The restore goes back to before the earliest session, so the earliest
    session's before value is the one a file takes, never a later one's."""
    cfg, _root = native_library
    before, first = _keyed_and_adopted(cfg, silence)
    _visit(cfg, "Alpha", scale="4A", bpm=12400)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    (second,) = [
        r.session_id for r in session.records(cfg)
        if r.workflow == ha.WORKFLOW and r.session_id != first
    ]
    assert _surfaces(cfg, "Alpha")[1:3] == ("04A - 124 - Alpha", "04A")

    code, envelope = _restore(first, "--discard", second)

    assert code == int(ExitCode.OK), envelope
    assert _all(cfg) == before
    assert envelope["data"]["totals"]["file_tags"]["planned"] == 5


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
    ],
)
def test_a_record_kept_in_another_shape_refuses(kept):
    with pytest.raises(CratekitError) as refused:
        restore_tags.kept_by(_record({restore_tags.RECORD_KEY: kept}))
    assert refused.value.cause.reason == "restore-record-unusable"
    assert refused.value.cause.detail["session_id"] == "s-1"


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

    found = restore_tags.befores(
        (earlier, later), rebased=lambda path: Path("/new") / path.name
    )

    assert [(str(f.path), f.title, f.initialkey, f.session_id) for f in found] == [
        ("/new/a.flac", "A0", "", "s-1"),
        ("/new/b.flac", "B0", "02A", "s-1"),
        ("/new/c.flac", "C1", "", "s-2"),
    ]


def _before(path: Path, title: str, key: str) -> restore_tags.FileBefore:
    return restore_tags.FileBefore(path, title, key, "s-1")


def test_a_file_already_as_it_was_writes_nothing_and_reads_back(silence, tmp_path, monkeypatch):
    path = tmp_path / "a.flac"
    path.write_bytes(silence.read_bytes())
    assert tags.write_tags(path, {"title": "01A - 124 - A", "initialkey": "01A"})
    writes: list = []
    monkeypatch.setattr(tags, "write_tags", lambda *a: writes.append(a) or True)
    monkeypatch.setattr(tags, "clear_tags", lambda *a: writes.append(a) or True)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "01A")])

    assert writes == []
    assert done.read_back == (str(path),) and not done.unwritten


def test_only_the_tag_that_differs_is_written(silence, tmp_path, monkeypatch):
    path = tmp_path / "a.flac"
    path.write_bytes(silence.read_bytes())
    assert tags.write_tags(path, {"title": "09A - 98 - A", "initialkey": "01A"})
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
    path = tmp_path / "a.flac"
    path.write_bytes(silence.read_bytes())
    assert tags.write_tags(path, {"title": "01A - 124 - A", "initialkey": "09A"})
    monkeypatch.setattr(tags, "clear_tags", lambda *a: False)

    done = restore_tags.put_back([_before(path, "01A - 124 - A", "")])

    assert done.failed == (str(path),)


def test_the_answer_carries_every_count_and_every_name():
    done = restore_tags.TagsPutBack(4, ("/a",), ("/b",), ("/c", "/d"))
    assert done.to_json() == {
        "planned": 4, "read_back": 1, "failed": ["/b"], "wrong": ["/c", "/d"],
    }
    assert done.unwritten == ("/b", "/c", "/d")


def test_the_session_record_round_trips_what_the_adopt_kept(native_library, silence):
    """The record read from disk is what the put back reads, not the one in memory."""
    cfg, _root = native_library
    _before, adopted = _keyed_and_adopted(cfg, silence)
    on_disk = json.loads(session.log_path(adopted, cfg).read_text())
    found = restore_tags.kept_by(session.read_record(adopted, cfg))
    assert len(found) == len(on_disk["detail"][restore_tags.RECORD_KEY]) == 5
    assert {str(f.path) for f in found} >= {str(_file(cfg, "Golf"))}
