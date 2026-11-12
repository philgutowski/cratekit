"""U242: the DOWNLOADED prefix is retired, and Cratekit records what it took itself.

THE PRODUCER IS THE PRODUCT. A hand prefixed playlist is one the fake account
lists under the prefix with nothing in the cursor or the record, which is the
shape the live account's 599 take. A Cratekit marked one is made by driving
``crate sync all``, finishing its jobs, landing the pass and answering ``crate
sync mark``'s gate, through ``tests/test_sync_mark.py``'s own helpers. What is
faked is the two provider seams. The fake catalogue does not see the fake
account's renames, so each test retitles the listing to what the account would
list after a strip, as ``tests/test_sync_unmark.py`` does after a mark.
"""

from __future__ import annotations

import json

import pytest

from cratekit.cli import registry
from cratekit.core import config, provider_gate
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.label.catalogue import AccountPlaylist
from cratekit.organize import inspiration
from cratekit.sync import mark_record, pair_discover, playlists, strip_cli, taken_cli, twins
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.test_outbound_workers import bind as bind_account
from tests.test_sync_all import _playlist, _tracks, bind_playlists
from tests.test_sync_all import slim as slim  # noqa: PLC0414 - the fixture, re-exported
from tests.test_sync_mark import _answered as _mark_answered
from tests.test_sync_mark import _land, _swept_pass

TAKEN = "sync.taken.confirm"
STRIP = "sync.strip.confirm"


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


def _answered(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on a verb's own gate, then the run that carries them out."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _items(done: dict) -> dict[str, dict]:
    return {item["id"]: item for item in done["data"]["items"]}


def _retitled(fake, account: outbound_fakes.FakeAccount) -> None:
    """The listing as the account would read after the renames the fake took."""
    renamed = dict(account.renamed)
    fake.account = [
        AccountPlaylist(
            playlist_id=one.playlist_id,
            name=renamed.get(one.playlist_id, one.name),
            tracks=one.tracks,
        )
        for one in fake.account
    ]


def _excluded(passed: dict) -> dict[str, str]:
    block = passed["data"]["summary"]["playlists"]
    return {identity: row["reason"] for identity, row in block["excluded"].items()}


def _queued(passed: dict) -> list[str]:
    return [row["playlist_id"] for row in passed["data"]["summary"]["playlists"]["queued"]]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The ledger, and the one predicate every reader asks
# ═══════════════════════════════════════════════════════════════════════════


def test_is_taken_holds_a_recorded_id_whatever_its_title_and_a_legacy_prefix():
    assert playlists.is_taken("pl-1", "Techno", frozenset({"pl-1"}))
    assert playlists.is_taken("pl-2", "DOWNLOADED Techno", frozenset())
    assert not playlists.is_taken("pl-3", "Techno", frozenset({"pl-1"}))
    assert not playlists.is_taken("pl-3", "downloaded Techno", frozenset())


def test_untaken_name_takes_off_every_copy_of_the_prefix():
    assert playlists.untaken_name("DOWNLOADED Techno") == "Techno"
    assert playlists.untaken_name("DOWNLOADED DOWNLOADED  Warmup ") == "Warmup"
    assert playlists.untaken_name("Techno") == "Techno"
    assert playlists.untaken_name("DOWNLOADED ") == ""


def test_exclusion_answers_swept_for_a_taken_playlist_with_no_prefix():
    stripped = AccountPlaylist(playlist_id="pl-1", name="Techno", tracks=3)
    assert (
        playlists.exclusion(stripped, recorded=set(), in_flight=set(), taken=frozenset({"pl-1"}))
        is playlists.Excluded.SWEPT
    )
    assert playlists.exclusion(stripped, recorded=set(), in_flight=set()) is None


def test_a_version_one_record_reads_as_one_with_nothing_taken(slim):
    record = mark_record.MarkRecord(slim)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    record.path.write_text(
        json.dumps(
            {
                "version": 1,
                "library_id": slim.library.volume_id,
                "marks": [
                    {
                        "pass": "p1",
                        "playlist_id": "pl-a",
                        "name": "Warmup",
                        "to": "DOWNLOADED Warmup",
                        "marked": "2026-10-01T10:00:00Z",
                        "unmarked": "",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    assert record.taken() == {} and record.taken_ids() == frozenset()
    assert [entry.playlist_id for entry in record.all()] == ["pl-a"]
    # THE FIRST WRITE REWRITES IT AS VERSION 2, the mark kept.
    record.take([mark_record.Taken("pl-b", "Peak", "p2", mark_record.BY_PASS, "2026-10-02T10:00:00Z")])
    raw = json.loads(record.path.read_text(encoding="utf-8"))
    assert raw["version"] == mark_record.RECORD_VERSION == 2
    assert [one["playlist_id"] for one in raw["marks"]] == ["pl-a"]
    assert record.taken_ids() == frozenset({"pl-b"})


def test_take_is_idempotent_and_a_released_entry_is_taken_afresh(slim):
    record = mark_record.MarkRecord(slim)
    first = mark_record.Taken("pl-a", "Warmup", "p1", mark_record.BY_PASS, "2026-10-01T10:00:00Z")
    again = mark_record.Taken("pl-a", "Warmup", "p2", mark_record.BY_PASS, "2026-10-09T10:00:00Z")
    assert record.take([first]) == ("pl-a",)
    assert record.take([again]) == ()
    assert record.taken()["pl-a"].by == "p1", "the first taker and its stamp stand"
    record.release("p1", "pl-a")
    assert record.taken_ids() == frozenset()
    assert record.taken()["pl-a"].released
    assert record.take([again]) == ("pl-a",)
    assert record.taken()["pl-a"].by == "p2" and record.taken()["pl-a"].held


def test_a_release_by_another_taker_is_refused(slim):
    record = mark_record.MarkRecord(slim)
    record.take([mark_record.Taken("pl-a", "Warmup", "p1", mark_record.BY_PASS, "2026-10-01T10:00:00Z")])
    with pytest.raises(CratekitError) as caught:
        record.release("p2", "pl-a")
    assert caught.value.cause.reason == "sync-mark-record-unusable"
    assert record.taken_ids() == frozenset({"pl-a"})


@pytest.mark.parametrize(
    "taken",
    [
        "not a list",
        [{"playlist_id": "pl-a", "name": "A", "by": "p", "how": "guessed", "at": "t", "released": ""}],
        [{"playlist_id": "pl-a", "name": "A", "by": "", "how": "pass", "at": "t", "released": ""}],
        [
            {"playlist_id": "pl-a", "name": "A", "by": "p", "how": "pass", "at": "t", "released": ""},
            {"playlist_id": "pl-a", "name": "A", "by": "q", "how": "pass", "at": "t", "released": ""},
        ],
    ],
)
def test_an_unreadable_taken_list_refuses_rather_than_reading_as_none(slim, taken):
    """UNREAD IS NOT NONE: empty would offer every taken playlist as new."""
    record = mark_record.MarkRecord(slim)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    record.path.write_text(
        json.dumps(
            {"version": 2, "library_id": slim.library.volume_id, "marks": [], "taken": taken}
        ),
        encoding="utf-8",
    )
    with pytest.raises(CratekitError) as caught:
        playlists.taken_ids(slim)
    assert caught.value.cause.reason == "sync-mark-record-unusable"


def test_a_record_of_an_unknown_version_refuses(slim):
    record = mark_record.MarkRecord(slim)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    for version in (3, True, [2], "2"):
        record.path.write_text(
            json.dumps({"version": version, "library_id": slim.library.volume_id, "marks": []}),
            encoding="utf-8",
        )
        with pytest.raises(CratekitError):
            record.taken_ids()


# ═══════════════════════════════════════════════════════════════════════════
# 2. The declarations
# ═══════════════════════════════════════════════════════════════════════════


def test_the_marks_write_nothing_on_the_account_and_the_strip_is_its_one_write():
    for name in ("sync.mark", "label.mark", "sync.taken"):
        entry = registry.entry(name)
        assert entry.writes == frozenset() and not entry.destructive, name
    strip = registry.entry("sync.strip")
    assert strip.writes == frozenset({"remote"}) and strip.destructive
    for name, gate in (("sync.taken", TAKEN), ("sync.strip", STRIP)):
        (spec,) = registry.entry(name).gates
        assert (spec.name, spec.options, spec.explicit) == (gate, ("apply", "abort"), True)
        assert spec.digest_source == "plan"


def test_the_record_still_survives_a_restore():
    for key in ("sync_mark_record", "sync_mark_record_lock"):
        assert config.state_file(key).snapshot is config.SnapshotRole.NEVER_RESTORED


# ═══════════════════════════════════════════════════════════════════════════
# 3. The migration
# ═══════════════════════════════════════════════════════════════════════════


HAND = (_playlist("pl-h", "DOWNLOADED Hand", 2), _tracks("901", "902"))
FRESH = (_playlist("pl-f", "Fresh", 1), _tracks("801"))


def test_the_migration_records_every_prefix_and_standing_mark_once_and_says_how_many(
    slim, monkeypatch
):
    bind_playlists(monkeypatch, HAND, FRESH, (_playlist("pl-m", "DOWNLOADED Marked", 1), _tracks("701")))
    record = mark_record.MarkRecord(slim)
    record.record_marked("old-pass", {"pl-m": ("Marked", "DOWNLOADED Marked")}, now="2025-06-01T10:00:00Z")
    record.record_marked("gone-pass", {"pl-x": ("Undone", "DOWNLOADED Undone")}, now="2025-06-01T10:00:00Z")
    record.record_unmarked("gone-pass", "pl-x")

    code, done = _answered(["sync", "taken"], TAKEN)
    assert code == int(ExitCode.OK), done
    assert done["data"]["totals"]["taken"] == 2
    held = record.taken()
    assert set(held) == {"pl-h", "pl-m"}, "an unmarked mark and a plain title are not taken"
    assert (held["pl-h"].by, held["pl-h"].how, held["pl-h"].name) == (
        mark_record.MIGRATION,
        mark_record.FOUND_PREFIXED,
        "Hand",
    )
    assert (held["pl-m"].by, held["pl-m"].how, held["pl-m"].at) == (
        "old-pass",
        mark_record.BY_PASS,
        "2025-06-01T10:00:00Z",
    ), "a pass's mark keeps its pass and its time, which filing reads a year from"

    # IDEMPOTENT: a second run records nothing and says the two are held.
    code, again = _answered(["sync", "taken"], TAKEN)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert again["data"]["totals"]["take"] == 0 and again["data"]["totals"]["held"] == 2


def test_the_migration_answered_abort_records_nothing(slim, monkeypatch):
    bind_playlists(monkeypatch, HAND)
    code, done = _answered(["sync", "taken"], TAKEN, option="abort")
    assert code == int(ExitCode.OK), done
    assert mark_record.MarkRecord(slim).taken() == {}


def test_the_migration_does_not_copy_the_cursor(slim, monkeypatch):
    """A recorded playlist whose pass still owes tracks stays in sync mark's plan."""
    fake, _name = _swept_pass(monkeypatch, FRESH)
    # THE NEXT PASS RECONCILES, which is when the cursor records the playlist.
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    code, done = _answered(["sync", "taken"], TAKEN)
    assert code == int(ExitCode.OK), done
    assert done["data"]["totals"]["cursor_only"] == 1
    assert mark_record.MarkRecord(slim).taken_ids() == frozenset()
    del fake


# ═══════════════════════════════════════════════════════════════════════════
# 4. The strip, and a stripped playlist never offered as new
# ═══════════════════════════════════════════════════════════════════════════


def _strip(*extra: str, option: str = "apply") -> tuple[int, dict]:
    return _answered(["sync", "strip", *extra], STRIP, option=option)


def test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered(slim, monkeypatch):
    fake = bind_playlists(monkeypatch, HAND, FRESH)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)

    code, done = _strip()
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-h", "Hand")]
    assert _items(done)["pl-h"]["action"] == strip_cli.STRIPPED
    assert "pl-h" in mark_record.MarkRecord(slim).taken_ids()

    _retitled(fake, account)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert _queued(passed) == ["pl-f"]
    assert _excluded(passed)["pl-h"] == str(playlists.Excluded.SWEPT)


def test_a_cratekit_marked_playlist_is_never_offered_once_stripped(slim, monkeypatch):
    """A mark made before U242 is a legacy prefix with a record entry: the strip
    keeps it taken under its pass, and no later sync offers it."""
    fake, name = _swept_pass(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    record = mark_record.MarkRecord(slim)
    record.record_marked(name, {"pl-a": ("Warmup", "DOWNLOADED Warmup")})
    fake.account = [_playlist("pl-a", "DOWNLOADED Warmup", 1)]
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)

    code, done = _strip()
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-a", "Warmup")]
    assert record.taken()["pl-a"].by == name

    _retitled(fake, account)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert _queued(passed) == []
    assert _excluded(passed)["pl-a"] == str(playlists.Excluded.SWEPT)


def test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered(slim, monkeypatch):
    fake, name = _swept_pass(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101", "102")))
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102")
    code, done = _mark_answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [], "no verb writes the prefix"
    held = mark_record.MarkRecord(slim).taken()["pl-a"]
    assert (held.by, held.how, held.name) == (name, mark_record.BY_PASS, "Warmup")
    assert mark_record.MarkRecord(slim).of_pass(name) == ()

    # THE LEDGER IS WHAT SAYS SO, checked before the cursor.
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert "pl-a" not in _queued(passed)
    assert _excluded(passed)["pl-a"] == str(playlists.Excluded.SWEPT)
    del fake


def test_a_collision_is_refused_and_named_and_the_rest_strip(slim, monkeypatch):
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-t", "DOWNLOADED Techno", 1), _tracks("1")),
        (_playlist("pl-o", "techno", 1), _tracks("2")),
        (_playlist("pl-a", "DOWNLOADED Acid", 1), _tracks("3")),
        (_playlist("pl-b", "DOWNLOADED DOWNLOADED Acid", 1), _tracks("4")),
        (_playlist("pl-e", "DOWNLOADED ", 1), _tracks("5")),
        (_playlist("pl-h", "DOWNLOADED House", 1), _tracks("6")),
    )
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    code, done = _strip()
    assert code == int(ExitCode.OK), done
    items = _items(done)
    assert account.renamed == [("pl-h", "House")]
    for identity in ("pl-t", "pl-a", "pl-b"):
        assert (items[identity]["action"], items[identity]["reason"]) == ("skip", strip_cli.COLLIDES)
    assert "'techno'" in items["pl-t"]["why"]
    assert "'DOWNLOADED DOWNLOADED Acid'" in items["pl-a"]["why"]
    assert items["pl-e"]["reason"] == strip_cli.NOTHING_LEFT
    # A REFUSED ONE STAYS TAKEN, prefix and record both.
    assert {"pl-t", "pl-a", "pl-b", "pl-e", "pl-h"} <= mark_record.MarkRecord(slim).taken_ids()
    del fake


def test_the_gate_screen_lists_every_rename_and_every_refusal(slim, monkeypatch):
    bind_playlists(
        monkeypatch,
        HAND,
        (_playlist("pl-t", "DOWNLOADED Techno", 1), _tracks("1")),
        (_playlist("pl-o", "Techno", 1), _tracks("2")),
    )
    code, refused = drive(["sync", "strip"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["renamed on the account"] == ["DOWNLOADED Hand -> Hand"]
    assert [line.split(":")[0] for line in shown["left with the prefix"]] == ["DOWNLOADED Techno"]
    assert mark_record.MarkRecord(slim).taken() == {}, "the plan records nothing"


class _Ceiling(outbound_fakes.FakeAccount):
    """An account whose provider gate stops after ``allowed`` renames."""

    def __init__(self, allowed: int) -> None:
        super().__init__()
        self.allowed = allowed

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        if len(self.renamed) >= self.allowed:
            raise refuse(
                provider_gate.CEILING,
                "this command made as many provider calls as its ceiling allows",
                steps=("run it again with a higher ceiling, --calls",),
                origin=("test",),
            )
        super().rename_playlist(playlist_id, name)


def test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes(slim, monkeypatch):
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-1", "DOWNLOADED One", 1), _tracks("1")),
        (_playlist("pl-2", "DOWNLOADED Two", 1), _tracks("2")),
        (_playlist("pl-3", "DOWNLOADED Three", 1), _tracks("3")),
    )
    account = _Ceiling(allowed=1)
    bind_account(monkeypatch, account)
    code, stopped = _strip()
    assert code != int(ExitCode.OK), stopped
    cause = stopped["cause"]
    assert cause["reason"] == provider_gate.CEILING
    assert cause["detail"]["stripped"] == ["pl-1"]
    assert sorted(cause["detail"]["still_prefixed"]) == ["pl-2", "pl-3"]
    assert "run crate sync strip again" in " ".join(cause["remediation"]["steps"])
    # EVERY ONE IS TAKEN, the stopped two as well.
    assert {"pl-1", "pl-2", "pl-3"} <= mark_record.MarkRecord(slim).taken_ids()

    _retitled(fake, account)
    account.allowed = 10
    code, resumed = _strip()
    assert code == int(ExitCode.OK), resumed
    assert sorted(_items(resumed)) == ["pl-2", "pl-3"], "only what is still prefixed is planned"
    assert sorted(dict(account.renamed)) == ["pl-1", "pl-2", "pl-3"]


def test_no_rename_is_made_for_a_playlist_the_record_does_not_hold(slim, monkeypatch):
    """THE MERGE BLOCKER: a rename before the record holds the id would offer it as new."""
    bind_playlists(monkeypatch, HAND)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    monkeypatch.setattr(taken_cli, "migrate", lambda cfg, listed, now=None: ([], ()))
    code, refused = _strip()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["detail"]["not_held"] == ["pl-h"]
    assert account.renamed == []


def test_a_title_changed_since_the_plan_is_not_renamed(slim, monkeypatch):
    fake = bind_playlists(monkeypatch, HAND)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    code, refused = drive(["sync", "strip"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, STRIP, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    plan_listing = list(fake.account)
    calls = {"n": 0}
    original = fake.account_playlists

    def moving():
        calls["n"] += 1
        if calls["n"] == 1:
            return original()
        return [_playlist("pl-h", "Hand by hand", 2)]

    monkeypatch.setattr(fake, "account_playlists", moving)
    code, done = drive(["--run", run_id, "sync", "strip"])
    assert code == int(ExitCode.OK), done
    assert account.renamed == []
    assert _items(done)["pl-h"]["reason"] == strip_cli.CHANGED_SINCE
    del plan_listing


def test_every_old_title_is_restored_by_unmark_of_the_strip(slim, monkeypatch):
    fake = bind_playlists(monkeypatch, HAND, (_playlist("pl-2", "DOWNLOADED Two", 1), _tracks("2")))
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    code, done = _strip()
    assert code == int(ExitCode.OK), done
    _retitled(fake, account)
    account.renamed.clear()

    code, back = _answered(
        ["sync", "unmark", "--pass", strip_cli.PASS], "sync.unmark.confirm"
    )
    assert code == int(ExitCode.OK), back
    assert sorted(account.renamed) == [("pl-2", "DOWNLOADED Two"), ("pl-h", "DOWNLOADED Hand")]
    assert {"pl-2", "pl-h"} <= mark_record.MarkRecord(slim).taken_ids(), "restored, still taken"


def test_nothing_prefixed_is_a_plan_of_nothing(slim, monkeypatch):
    bind_playlists(monkeypatch, FRESH)
    code, refused = drive(["sync", "strip"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["nothing to strip"] == strip_cli.NOTHING_SAID


def test_playlist_narrows_and_refuses_a_playlist_with_no_prefix(slim, monkeypatch):
    bind_playlists(monkeypatch, HAND, FRESH, (_playlist("pl-2", "DOWNLOADED Two", 1), _tracks("2")))
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    code, refused = drive(["sync", "strip", "--playlist", "pl-f"])
    assert code != int(ExitCode.OK) and refused["cause"]["detail"]["not_prefixed"] == ["pl-f"]
    code, done = _strip("--playlist", "pl-2")
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-2", "Two")]


# ═══════════════════════════════════════════════════════════════════════════
# 5. sync unmark lets go what a pass took
# ═══════════════════════════════════════════════════════════════════════════


def test_unmark_lets_go_a_pass_mark_with_no_write_to_the_account(slim, monkeypatch):
    fake, name = _swept_pass(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    code, done = _mark_answered(_land(slim, name, "101"))
    assert code == int(ExitCode.OK), done
    assert "pl-a" in mark_record.MarkRecord(slim).taken_ids()

    code, back = _answered(["sync", "unmark", "--pass", name], "sync.unmark.confirm")
    assert code == int(ExitCode.OK), back
    assert _items(back)["pl-a"]["action"] == "released"
    assert account.renamed == []
    assert "pl-a" not in mark_record.MarkRecord(slim).taken_ids()
    # A SECOND UNMARK FINDS IT LET GO.
    code, again = _answered(["sync", "unmark", "--pass", name], "sync.unmark.confirm")
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    del fake


# ═══════════════════════════════════════════════════════════════════════════
# 6. The readers, unchanged for a stripped playlist
# ═══════════════════════════════════════════════════════════════════════════


class _Folders:
    """The two account reads a sets or year folder reader makes."""

    def __init__(self, folders: dict[str, str], inside: dict[str, dict[str, str]]) -> None:
        self._folders = folders
        self._inside = inside

    def folders(self) -> dict[str, str]:
        return dict(self._folders)

    def folder_playlists(self, folder_id: str) -> dict[str, str]:
        return dict(self._inside.get(folder_id, {}))


def test_the_inspiration_set_rule_reads_a_stripped_set_as_the_prefixed_one():
    remote = _Folders(
        {"f-1": "Downloaded Sets 2026"},
        {"f-1": {"pl-s": "Signal Live 2-26", "pl-p": "DOWNLOADED Other Set", "pl-x": "Loose"}},
    )
    sets_found, rows = inspiration.account_sets(remote, (), frozenset({"pl-s"}))
    assert [(one[1], one[2]) for one in sets_found] == [
        ("pl-p", "Other Set"),
        ("pl-s", "Signal Live 2-26"),
    ]
    assert [(row.playlist_id, row.action) for row in rows] == [("pl-x", inspiration.UNPREFIXED)]


def test_twins_reads_a_stripped_custom_playlist_as_downloaded():
    remote = _Folders({"f-y": "2026"}, {"f-y": {"pl-1": "Phil 9-30-26", "pl-2": "Not Taken"}})
    own = {"pl-1": "Phil 9-30-26", "pl-2": "Not Taken"}
    assert twins.candidates(remote, own, (), frozenset({"pl-1"})) == [("2026", "pl-1", "Phil 9-30-26")]
    assert twins.twin_name("DOWNLOADED Phil 9-30-26") == twins.twin_name("Phil 9-30-26")


def test_pairing_techno_with_a_stripped_former_downloaded_techno():
    folder = "Genre Trivia!"
    assert pair_discover.downloaded_copy(folder, "Techno", ["Techno"], taken=True) == "Techno"
    assert pair_discover.downloaded_copy(folder, "DOWNLOADED Techno", ["Techno"]) == "Techno"
    assert pair_discover.downloaded_copy(folder, "Techno", ["Techno"]) == "", (
        "a playlist the record does not hold is never a copy"
    )
    assert pair_discover.downloaded_copy(folder, "House", ["Techno"], taken=True) == ""


def test_filing_reads_a_found_prefix_as_undated_and_a_pass_mark_as_dated():
    from cratekit.organize import filing

    found = mark_record.Taken("pl-h", "Hand", mark_record.MIGRATION, mark_record.FOUND_PREFIXED, "2026-11-12T10:00:00Z")
    marked = mark_record.Taken("pl-m", "Warmup", "p1", mark_record.BY_PASS, "2025-06-01T10:00:00Z")
    gone = mark_record.Taken("pl-g", "Gone", "p1", mark_record.BY_PASS, "2025-06-01T10:00:00Z", released="x")
    standing = filing._standing_marks((), (found, marked, gone))
    assert standing == {"pl-m": "2025-06-01T10:00:00Z"}
    assert filing.year_of_mark(standing["pl-m"]) == "2025"
