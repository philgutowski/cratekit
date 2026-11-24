"""``crate sync unmark``: a mark a pass wrote can be taken off again (R-838).

Since U242 a mark retitles nothing (``tests/test_u242_taken.py``); this drives
the title half, putting back every prefix a pass wrote before U242, over the
record entry and retitled listing such a mark left.
"""

from __future__ import annotations

import json

import pytest

from cratekit.cli import registry
from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli
from cratekit.sync import mark_record
from tests import outbound_fakes
from tests._sync_builders import exited, failed
from tests.cli_drive import drive
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_outbound_workers import bind as bind_account
from tests.test_sync_all import _playlist, _tracks
from tests.test_sync_all import slim as slim  # noqa: PLC0414 - the fixture, re-exported
from tests.test_sync_mark import _answered as _mark_answered
from tests.test_sync_mark import _by_id, _land, _swept_pass

CONFIRM = "sync.unmark.confirm"

THREE = (
    (_playlist("pl-a", "Warmup"), _tracks("101", "102")),
    (_playlist("pl-b", "Peak"), _tracks("201")),
    (_playlist("pl-c", "Closing"), _tracks("301")),
)


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


def _marked(slim_cfg, monkeypatch, *listed):
    """A pass over ``listed``, landed whole and marked, its listing retitled to the mark."""
    listed = listed or THREE
    fake, name = _swept_pass(monkeypatch, *listed)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    ids = [track.id for _playlist_, tracks in listed for track in tracks]
    xml = _land(slim_cfg, name, *ids)
    mark_record.MarkRecord(slim_cfg).record_marked(
        name,
        {
            playlist.playlist_id: (playlist.name, "DOWNLOADED " + playlist.name)
            for playlist, _tracks_ in listed
        },
    )
    fake.account = [
        _playlist(playlist.playlist_id, "DOWNLOADED " + playlist.name)
        for playlist, _tracks_ in listed
    ]
    return fake, account, name, xml


def _landed_pass(slim_cfg, monkeypatch):
    """The three playlists swept and landed, nothing marked yet: (account, pass, intake file)."""
    _fake, name = _swept_pass(monkeypatch, *THREE)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    return account, name, _land(slim_cfg, name, "101", "102", "201", "301")


def _unmark(name: str, *extra: str) -> tuple[int, dict]:
    return drive(["sync", "unmark", "--pass", name, *extra])


def _approved(name: str, *extra: str, option: str = "apply") -> str:
    """The unmark's own gate shown and answered ``option`` (R34's two acts): its run."""
    refused = exited(_unmark(name, *extra), ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["gate"] == CONFIRM
    run_id = refused["run_id"]
    exited(drive(["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"]))
    return run_id


def _carried_out(run_id: str, name: str, *extra: str) -> tuple[int, dict]:
    return drive(["--run", run_id, "sync", "unmark", "--pass", name, *extra])


def _answered(name: str, *extra: str, option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on the unmark's own gate, then the run that carries them out."""
    return _carried_out(_approved(name, *extra, option=option), name, *extra)


def _stamped(slim_cfg, name: str) -> dict[str, bool]:
    """Whether the record stamps each playlist of the pass as put back."""
    return {e.playlist_id: bool(e.unmarked) for e in mark_record.MarkRecord(slim_cfg).of_pass(name)}


# 1. The declaration, and the record the mark keeps


def test_the_verb_declares_one_remote_write_behind_an_explicit_gate():
    entry = registry.entry("sync.unmark")
    assert entry.writes == frozenset({"remote"}) and entry.destructive
    (gate,) = entry.gates
    assert (gate.name, gate.options, gate.explicit) == (CONFIRM, ("apply", "abort"), True)
    assert gate.digest_source == "plan"


def test_the_record_survives_a_restore():
    """The renames it records stay on the account whatever a restore rolls back."""
    for key in ("sync_mark_record", "sync_mark_record_lock"):
        assert config.state_file(key).snapshot is config.SnapshotRole.NEVER_RESTORED


def test_sync_mark_since_u242_holds_each_playlist_as_taken_under_the_pass(slim, monkeypatch):
    """The record the unmark reads: a taken entry per playlist, no title."""
    account, name, xml = _landed_pass(slim, monkeypatch)
    exited(_mark_answered(xml))
    taken = mark_record.MarkRecord(slim).taken()
    assert {identity: (entry.name, entry.by) for identity, entry in taken.items()} == {
        "pl-a": ("Warmup", name),
        "pl-b": ("Peak", name),
        "pl-c": ("Closing", name),
    }
    assert all(entry.at and entry.held for entry in taken.values())
    assert account.renamed == [] and mark_record.MarkRecord(slim).of_pass(name) == ()


# 2. The brief's scenarios


def test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them(slim, monkeypatch):
    fake, account, name, _xml = _marked(slim, monkeypatch)

    exited(_unmark(name), ExitCode.DECISION_REQUIRED)
    assert account.renamed == [], "a rename landed before the gate was answered"

    done = exited(_answered(name))
    assert account.renamed == [("pl-a", "Warmup"), ("pl-b", "Peak"), ("pl-c", "Closing")]
    assert {key: item["action"] for key, item in _by_id(done).items()} == {
        "pl-a": "unmarked",
        "pl-b": "unmarked",
        "pl-c": "unmarked",
    }
    assert done["data"]["totals"] == {"count": 3, "unmarked": 3, "released": 0, "skip": 0}
    held = mark_record.MarkRecord(slim).of_pass(name)
    assert all(entry.unmarked for entry in held)
    del fake


def _skipped(done: dict, playlist_id: str) -> tuple[str, str]:
    item = _by_id(done)[playlist_id]
    return item["action"], item["reason"]


def test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left(slim, monkeypatch):
    """With the prefix or without it, a later title is somebody's decision."""
    fake, account, name, _xml = _marked(slim, monkeypatch)
    fake.account = [
        _playlist("pl-a", "Warmup (mine)"),
        _playlist("pl-b", "DOWNLOADED Peak v2"),
        _playlist("pl-c", "DOWNLOADED Closing"),
    ]
    done = exited(_answered(name))
    assert account.renamed == [("pl-c", "Closing")]
    items = _by_id(done)
    for identity in ("pl-a", "pl-b"):
        assert _skipped(done, identity) == ("skip", "renamed-since-mark")
    assert "no longer carries the prefix" in items["pl-a"]["why"]
    assert "under another title" in items["pl-b"]["why"]
    assert not mark_record.MarkRecord(slim).of_pass(name)[0].unmarked


def test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title(slim, monkeypatch):
    listed = THREE[:2]
    fake, account, name, _xml = _marked(slim, monkeypatch, *listed)
    fake.account = [*fake.account, _playlist("pl-x", "DOWNLOADED Somebody Else's")]
    listings = fake.account_listings

    refused = exited(_unmark(name, "--playlist", "pl-x"), ExitCode.PRECONDITION)
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert refused["cause"]["detail"]["not_marked"] == ["pl-x"]
    assert fake.account_listings == listings, "the account was listed before the refusal"

    # And left out of the whole pass's plan.
    done = exited(_answered(name))
    assert sorted(_by_id(done)) == ["pl-a", "pl-b"]
    assert ("pl-x", "Somebody Else's") not in account.renamed


def test_a_second_run_plans_nothing_and_still_asks(slim, monkeypatch):
    fake, account, name, _xml = _marked(slim, monkeypatch)
    exited(_answered(name))
    fake.account = [_playlist(p.playlist_id, p.name.removeprefix("DOWNLOADED ")) for p in fake.account]
    account.renamed.clear()
    listings = fake.account_listings

    exited(_unmark(name), ExitCode.DECISION_REQUIRED)
    again = exited(_answered(name))
    assert again["outcome"] == "no_op"
    assert account.renamed == []
    assert again["data"]["totals"] == {"count": 3, "unmark": 0, "release": 0, "skip": 3}
    assert {item["reason"] for item in again["data"]["items"]} == {"already-unmarked"}
    assert fake.account_listings == listings, "nothing to put back still listed the account"


def test_a_pass_the_record_holds_nothing_for_is_a_gated_plan_of_nothing(slim, monkeypatch):
    fake, account, _name, _xml = _marked(slim, monkeypatch)
    listings = fake.account_listings
    done = exited(_answered("no-such-pass_synced"))
    assert done["outcome"] == "no_op"
    assert done["data"]["items"] == []
    assert [w["code"] for w in done["warnings"]] == ["sync-unmark-no-mark"]
    assert fake.account_listings == listings
    assert account.renamed == []


# 3. Naming the pass, narrowing it, and the answer


@pytest.mark.parametrize(
    "tail", ["", land_cli.RETIRED_SUFFIX, f"{land_cli.RETIRED_SUFFIX}-2"]
)
def test_the_intake_file_names_the_pass_retired_or_not(slim, monkeypatch, tail):
    """The file need not be there: the name is all that is read."""
    _fake, account, name, xml = _marked(slim, monkeypatch)
    given = xml.with_name(f"{name}{land_cli.INTAKE_SUFFIX}{tail}")
    xml.unlink()
    exited(_answered(str(given)))
    assert len(account.renamed) == 3


@pytest.mark.parametrize(
    ("named", "renamed", "stamped"),
    [
        pytest.param(("pl-b",), [("pl-b", "Peak")], (False, True, False), id="one"),
        # U246: every playlist named is kept, not the first alone.
        pytest.param(
            ("pl-a", "pl-c"), [("pl-a", "Warmup"), ("pl-c", "Closing")], (True, False, True),
            id="twice",
        ),
    ],
)
def test_playlist_narrows_to_the_marks_named(slim, monkeypatch, named, renamed, stamped):
    _fake, account, name, _xml = _marked(slim, monkeypatch)
    flags = [part for one in named for part in ("--playlist", one)]
    done = exited(_answered(name, *flags))
    assert sorted(account.renamed) == renamed
    assert sorted(_by_id(done)) == list(named)
    assert _stamped(slim, name) == dict(zip(("pl-a", "pl-b", "pl-c"), stamped, strict=True))


def test_an_abort_renames_nothing_and_stamps_nothing(slim, monkeypatch):
    _fake, account, name, _xml = _marked(slim, monkeypatch)
    done = exited(_answered(name, option="abort"))
    assert done["outcome"] == "no_op"
    assert account.renamed == []
    assert not any(entry.unmarked for entry in mark_record.MarkRecord(slim).of_pass(name))


def test_an_answer_is_stale_once_the_account_moves(slim, monkeypatch):
    fake, account, name, _xml = _marked(slim, monkeypatch)
    run_id = _approved(name)
    fake.account = [_playlist("pl-a", "Warmup (mine)"), *fake.account[1:]]
    failed(_carried_out(run_id, name))
    assert account.renamed == []


def test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said(slim, monkeypatch):
    fake, account, name, _xml = _marked(slim, monkeypatch)
    run_id = _approved(name)

    planned_at = fake.account_listings + 1
    listing = type(fake).account_playlists

    def moving(self):
        listed = listing(self)
        if self.account_listings > planned_at:
            return (_playlist("pl-a", "Warmup (mine)"), *listed[1:])
        return listed

    monkeypatch.setattr(type(fake), "account_playlists", moving)
    done = exited(_carried_out(run_id, name))
    assert account.renamed == [("pl-b", "Peak"), ("pl-c", "Closing")]
    assert _skipped(done, "pl-a") == ("skip", "changed-since-plan")
    assert [w["code"] for w in done["warnings"]] == ["sync-unmark-changed-since-plan"]
    assert done["data"]["totals"] == {"count": 3, "unmarked": 2, "released": 0, "skip": 1}


def test_a_failure_part_way_names_what_was_put_back(slim, monkeypatch):
    _fake, account, name, _xml = _marked(slim, monkeypatch)
    account.fail_on = frozenset({"pl-b"})
    stopped = exited(_answered(name), ExitCode.INTERNAL)
    assert "DOWNLOADED Warmup" in stopped["cause"]["message"]
    assert stopped["cause"]["detail"]["unmarked"] == ["pl-a"]
    assert stopped["cause"]["detail"]["still_marked"] == ["pl-b", "pl-c"]
    assert _stamped(slim, name) == {"pl-a": True, "pl-b": False, "pl-c": False}


def test_a_mark_after_an_unmark_clears_the_stamp(slim, monkeypatch):
    _fake, _account, name, _xml = _marked(slim, monkeypatch)
    record = mark_record.MarkRecord(slim)
    record.record_unmarked(name, "pl-a")
    record.record_marked(name, {"pl-a": ("Warmup", "DOWNLOADED Warmup")})
    held = {entry.playlist_id: entry for entry in record.of_pass(name)}
    assert held["pl-a"].unmarked == ""
    assert len(record.of_pass(name)) == 3


# 4. A record that cannot be read is not an empty one


#: Every field present and non empty, one not text, so only the type check
#: refuses it (row R4 in docs/mutation/r838-c.md).
_UNTYPED = {"pass": "p", "playlist_id": "x", "name": "n", "to": "DOWNLOADED n", "marked": "t",
            "unmarked": 7}


@pytest.mark.parametrize(
    "written",
    [
        "not json",
        json.dumps([]),
        json.dumps({"version": 2, "library_id": "x", "marks": []}),
        json.dumps({"version": 1, "library_id": "another-library", "marks": []}),
        "LIBRARY:" + json.dumps({"version": 1, "marks": {}}),
        "LIBRARY:" + json.dumps({"version": 1, "marks": [{"pass": "p", "playlist_id": "x"}]}),
        "LIBRARY:" + json.dumps({"version": 1, "marks": [_UNTYPED]}),
    ],
)
def test_an_unreadable_record_refuses_rather_than_reading_as_empty(slim, monkeypatch, written):
    record = mark_record.MarkRecord(slim)
    if written.startswith("LIBRARY:"):
        document = json.loads(written.removeprefix("LIBRARY:"))
        document["library_id"] = slim.library.volume_id
        written = json.dumps(document)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    record.path.write_text(written, encoding="utf-8")
    refused = exited(_unmark("any-pass_synced"), ExitCode.PRECONDITION)
    assert refused["cause"]["reason"] == "sync-mark-record-unusable"


# 5. Stamps, record failures and a playlist gone from the account


def test_a_title_already_put_back_is_skipped_without_a_stamp(slim, monkeypatch):
    """A stamp that did not land, or the old title typed back, reads as this verb's title."""
    fake, account, name, _xml = _marked(slim, monkeypatch)
    fake.account = [_playlist("pl-a", "Warmup"), *fake.account[1:]]
    done = exited(_answered(name))
    assert account.renamed == [("pl-b", "Peak"), ("pl-c", "Closing")]
    assert _skipped(done, "pl-a") == ("skip", "already-unmarked")


def test_a_later_mark_by_another_pass_owns_the_prefix(slim, monkeypatch):
    _fake, account, name, _xml = _marked(slim, monkeypatch)
    mark_record.MarkRecord(slim).record_marked(
        "later_synced", {"pl-a": ("Warmup", "DOWNLOADED Warmup")}
    )
    done = exited(_answered(name))
    assert ("pl-a", "Warmup") not in account.renamed
    assert _skipped(done, "pl-a") == ("skip", "marked-again")
    assert "later_synced" in _by_id(done)["pl-a"]["why"]

    exited(_answered("later_synced"))
    assert account.renamed[-1] == ("pl-a", "Warmup")
    # THE LATER PASS'S ENTRY IS THE ONE STAMPED, never the first the record
    # holds for that playlist (row R3 in docs/mutation/r838-c.md).
    assert mark_record.MarkRecord(slim).of_pass("later_synced")[0].unmarked
    assert not _stamped(slim, name)["pl-a"]


def test_an_unlockable_record_refuses_the_unmark_before_any_rename(slim, monkeypatch):
    _fake, account, name, _xml = _marked(slim, monkeypatch)
    code, refused = _unmark(name)
    run_id = refused["run_id"]
    exited(drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"]))

    def unlockable(self):
        raise self._unusable("it could not be locked")

    monkeypatch.setattr(mark_record.MarkRecord, "ready", unlockable)
    refused = exited(_carried_out(run_id, name), ExitCode.PRECONDITION)
    assert refused["cause"]["reason"] == "sync-mark-record-unusable"
    assert account.renamed == []


def test_an_unreadable_record_refuses_the_mark_before_its_gate(slim, monkeypatch):
    account, _name, xml = _landed_pass(slim, monkeypatch)
    record = mark_record.MarkRecord(slim)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    record.path.write_text("not json", encoding="utf-8")
    refused = exited(drive(["sync", "mark", "--xml", str(xml)]), ExitCode.PRECONDITION)
    assert refused["cause"]["reason"] == "sync-mark-record-unusable"
    assert account.renamed == []


def test_a_record_that_cannot_be_written_refuses_the_mark_and_renames_nothing(slim, monkeypatch):
    """The record is the mark (U242), so a full disk refuses the mark."""
    account, _name, xml = _landed_pass(slim, monkeypatch)

    def full(self, *args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(mark_record.MarkRecord, "take", full)
    refused = exited(_mark_answered(xml), ExitCode.PRECONDITION)
    assert refused["cause"]["reason"] == "sync-mark-record-unusable"
    assert refused["cause"]["detail"]["marked"] == []
    assert account.renamed == []


def test_the_mark_screen_says_a_playlist_was_put_back(slim, monkeypatch):
    fake, _account, name, xml = _marked(slim, monkeypatch)
    exited(_answered(name, "--playlist", "pl-a"))
    fake.account = [_playlist("pl-a", "Warmup"), *fake.account[1:]]
    refused = exited(drive(["sync", "mark", "--xml", str(xml)]), ExitCode.DECISION_REQUIRED)
    said = [line for line in json.dumps(refused).split('"') if "sync unmark let it go" in line]
    assert len(said) == 1 and said[0].startswith("Warmup ("), said


def test_a_playlist_the_account_no_longer_lists_is_said_and_left(slim, monkeypatch):
    """Closes the zero row U7 in docs/mutation/r838-a.md."""
    fake, account, name, _xml = _marked(slim, monkeypatch)
    fake.account = list(fake.account[:2])
    done = exited(_answered(name))
    assert account.renamed == [("pl-a", "Warmup"), ("pl-b", "Peak")]
    assert _skipped(done, "pl-c") == ("skip", "not-listed")
    assert not _stamped(slim, name)["pl-c"]
