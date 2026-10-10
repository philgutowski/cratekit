"""U123: a label's dated playlist heard, merged into the year and removed.

Every scenario the brief names that the product can reach, driven through the
real dispatcher with the catalogue and the account faked as U117's suite fakes
them: the dated playlist is made by :func:`dated.apply`, so the ledger vouches
for it exactly as it would for one ``crate organize`` made. The adapter's
playlist removal is driven over a stand in for the client at the end. The
Record Labels tree half is not built, because that tree stays on the xml
bridge (R39); the suite holds the verb to saying so and to writing nothing in
rekordbox. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.label import dated, heard, heard_cli, playlists_cli, sync_cli
from cratekit.modules.outbound import ledger, tidal_account
from tests.cli_drive import drive
from tests.label_fakes import FakeTrack
from tests.test_label_dated import _answer, _built, _plan, _record
from tests.test_label_playlists import LABEL, LABEL_ID, _entry, _years
from tests.test_label_playlists import followed as followed  # noqa: PLC0414 - fixture
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

GATE = "label.heard.confirm"
DAY = "2026-10-09"
DATED = f"{LABEL} 2023 new {DAY}"
YEAR = f"{LABEL} 2023"
VERB = ["label", "heard", LABEL, "2023", DAY]


def _two_acts(argv: list[str], option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on the explicit gate, then the run that carries them out."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    assert refused["cause"]["detail"]["explicit"] is True
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, GATE, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _made(cfg, fake, account, answers) -> str:
    """The years built, the answers recorded, and the dated playlist made by U117."""
    _built(cfg, fake, account)
    _record(cfg, answers)
    dated.apply(cfg, account, _plan(cfg, fake, account))
    (folder_id,) = account.folder_names
    return folder_id


def _ids(account, folder_id: str) -> dict[str, str]:
    return {account.titles[pid]: pid for pid, held in account.placed.items() if held == folder_id}


def _heard(cfg) -> list[str]:
    return list(sync_cli.load_record(cfg)["labels"][LABEL_ID].get(heard.HEARD, []))


def _writes(account) -> tuple[int, int, int, int]:
    return len(account.chunks), len(account.taken), len(account.deleted), len(account.created)


def _codes(envelope: dict) -> list[str]:
    return [one["code"] for one in envelope.get("warnings") or ()]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_writes_only_the_account_behind_one_explicit_gate():
    entry = registry.entry("label.heard")
    assert entry.landed
    assert entry.writes == frozenset({"remote"})
    assert entry.destructive is True
    assert entry.module_id == "labels" and entry.feature_rows == (23,)
    (spec,) = entry.gates
    assert (spec.name, spec.options, spec.explicit) == (GATE, ("apply", "abort"), True)
    assert spec.digest_source == "plan"


def test_nothing_on_the_heard_path_reaches_rekordbox_a_grid_a_tempo_or_a_rating():
    """The brief's last scenario, held at the import graph and at the names.

    The verb writes the account and the label review store and nothing else,
    so neither module may import the database writer, the tree writers or the
    file tag writer, and neither may name a grid, a tempo or a rating.
    """
    banned = ("cratekit.core.rb_writer", "cratekit.write", "cratekit.core.tags")
    for module in (heard, heard_cli):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        imported = {
            node.module or ""
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        } | {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        assert not {one for one in imported if one.startswith(banned)}, (module.__name__, imported)
        names = {
            (node.attr if isinstance(node, ast.Attribute) else node.id).lower()
            for node in ast.walk(tree)
            if isinstance(node, (ast.Attribute, ast.Name))
        }
        assert not {one for one in names if any(s in one for s in ("grid", "bpm", "tempo", "rating"))}


# ═══════════════════════════════════════════════════════════════════════════
# 2. Heard, merged and removed
# ═══════════════════════════════════════════════════════════════════════════


def test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    dated_id = _ids(account, folder_id)[DATED]
    assert ledger.product_made(cfg, dated_id)

    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    assert _heard(cfg) == ["r3", "r4"]
    assert DATED not in _ids(account, folder_id)
    assert account.deleted == [(dated_id, ("t4", "t5", "t6", "t7"))]
    assert _years(account, folder_id)[YEAR] == ["t4", "t5", "t6", "t7"]
    assert envelope["data"]["totals"]["applied"]["removed"] is True
    assert not ledger.product_made(cfg, dated_id), "the removed playlist is still vouched for"

    before = _writes(account), config.state_path("label_sync", cfg).read_bytes()
    code, again = _two_acts(VERB)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert again["data"]["totals"]["writes"] is False
    assert (_writes(account), config.state_path("label_sync", cfg).read_bytes()) == before


def test_the_merge_adds_only_what_the_year_lacks_and_never_a_duplicate(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    year_id = _ids(account, folder_id)[YEAR]
    # A person took two tracks off the year since it was built.
    account.playlists[year_id] = [one for one in account.playlists[year_id] if one not in ("t4", "t6")]

    code, refused = drive(VERB)
    (added,) = [one for one in refused["cause"]["detail"]["shown"]["items"] if one["action"] == "add"]
    assert (added["add"], added["already"]) == (2, 2)
    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    held = _years(account, folder_id)[YEAR]
    assert held == ["t5", "t7", "t4", "t6"]
    assert account.chunks[-1] == (year_id, ("t4", "t6"))


def test_a_release_not_in_the_dated_playlist_is_refused_by_name(followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3", "r4"], DAY), _answer(["r1"], DAY)])
    before = _writes(account), config.state_path("label_sync", cfg).read_bytes()

    code, refused = drive([*VERB, "--release", "r3", "--release", "r1"])
    assert code != int(ExitCode.OK)
    cause = refused["cause"]
    assert cause["reason"] == "label-heard-not-in-playlist"
    assert "r1" in cause["message"] and cause["detail"]["outside"] == ["r1"]
    assert cause["detail"]["releases"] == ["r3", "r4"]
    assert (_writes(account), config.state_path("label_sync", cfg).read_bytes()) == before


def test_some_releases_heard_take_their_tracks_off_and_the_last_removes_it(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    dated_id = _ids(account, folder_id)[DATED]

    code, envelope = _two_acts([*VERB, "--release", "r3"])
    assert code == int(ExitCode.OK), envelope
    assert _heard(cfg) == ["r3"]
    assert account.playlists[dated_id] == ["t6", "t7"]
    assert account.taken == [(dated_id, ("t4", "t5"))]
    assert account.deleted == []

    code, envelope = _two_acts([*VERB, "--release", "r4"])
    assert code == int(ExitCode.OK), envelope
    assert _heard(cfg) == ["r3", "r4"]
    assert account.deleted == [(dated_id, ("t6", "t7"))]
    assert _years(account, folder_id)[YEAR] == ["t4", "t5", "t6", "t7"]


def test_a_named_release_already_heard_is_said_and_writes_nothing(followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    _two_acts([*VERB, "--release", "r3"])
    before = _writes(account)
    code, envelope = _two_acts([*VERB, "--release", "r3"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _writes(account) == before
    actions = {one["id"]: one["action"] for one in envelope["data"]["items"] if one["kind"] == "release"}
    assert actions == {"r3": "already heard", "r4": "left unheard"}


def test_declined_nothing_is_written(followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    before = _writes(account), config.state_path("label_sync", cfg).read_bytes()
    code, envelope = _two_acts(VERB, option="abort")
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert (_writes(account), config.state_path("label_sync", cfg).read_bytes()) == before


def test_no_dated_playlist_on_the_account_marks_heard_and_touches_nothing(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r3"], DAY)])
    before = _writes(account)
    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    assert _heard(cfg) == ["r3"]
    assert _writes(account) == before
    (playlist,) = [one for one in envelope["data"]["items"] if one["kind"] == "playlist"]
    assert playlist["action"] == heard.ABSENT


def test_every_run_says_the_record_labels_tree_is_not_changed(followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3"], DAY)])
    code, refused = drive(VERB)
    assert refused["cause"]["detail"]["shown"]["rekordbox"] == heard.TREE_SAID
    code, envelope = _two_acts(VERB)
    assert heard_cli.TREE_UNCHANGED in _codes(envelope)
    code, again = _two_acts(VERB)
    assert heard_cli.TREE_UNCHANGED in _codes(again)


# ═══════════════════════════════════════════════════════════════════════════
# 3. Refused before the gate
# ═══════════════════════════════════════════════════════════════════════════


def test_a_dated_playlist_the_ledger_does_not_vouch_for_is_refused(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    (folder_id,) = account.folder_names
    # Made by a person with the dated name, so reused and never recorded.
    account.move_to_folder(account.create_playlist(DATED), folder_id)
    _record(cfg, [_answer(["r3"], DAY)])
    dated.apply(cfg, account, _plan(cfg, fake, account))
    before = _writes(account), config.state_path("label_sync", cfg).read_bytes()

    code, refused = drive(VERB)
    assert refused["cause"]["reason"] == "label-heard-not-product-made"
    assert (_writes(account), config.state_path("label_sync", cfg).read_bytes()) == before


def test_a_date_no_go_took_anything_on_is_refused(followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3"], DAY)])
    code, refused = drive(["label", "heard", LABEL, "2023", "2026-10-08"])
    assert refused["cause"]["reason"] == "label-heard-no-releases"
    code, refused = drive(["label", "heard", LABEL, "2021", DAY])
    assert refused["cause"]["reason"] == "label-heard-no-releases"


@pytest.mark.parametrize(
    "argv",
    [[LABEL, "23", DAY], [LABEL, "2023", "2026-13-01"], [LABEL, "2023", "yesterday"]],
)
def test_a_year_or_date_that_is_not_one_is_refused(followed, argv):
    code, refused = drive(["label", "heard", *argv])
    assert refused["cause"]["reason"] == "label-heard-invalid"


def test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    year_id = _ids(account, folder_id)[YEAR]
    account.placed.pop(year_id)
    code, refused = drive(VERB)
    assert refused["cause"]["reason"] == "label-heard-no-year-playlist"
    assert account.deleted == []


def test_two_playlists_with_the_dated_name_refuse(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    account.move_to_folder(account.create_playlist(DATED), folder_id)
    code, refused = drive(VERB)
    assert refused["cause"]["reason"] == "label-heard-ambiguous"


def test_a_label_nobody_follows_is_a_plan_of_nothing_still_gated(installed):
    code, refused = drive(["label", "heard", "no-such-label", "2023", DAY])
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["gate"] == GATE


# ═══════════════════════════════════════════════════════════════════════════
# 4. A write the account refuses
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_the_year_will_not_take_keeps_the_dated_playlist(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    year_id = _ids(account, folder_id)[YEAR]
    account.playlists[year_id].remove("t4")
    account.unaddable.add("t4")

    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    assert DATED in _ids(account, folder_id)
    assert account.deleted == []
    assert "label-heard-tracks-refused" in _codes(envelope)
    assert envelope["data"]["totals"]["applied"]["kept"] is True
    assert _heard(cfg) == ["r3"]


def test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes(
    followed,
):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    ids = _ids(account, folder_id)
    account.playlists[ids[YEAR]].remove("t5")
    account.fail_on = frozenset({ids[DATED]})

    code, refused = _two_acts(VERB)
    assert code != int(ExitCode.OK)
    assert "1 track(s) were added" in refused["cause"]["message"]
    assert "no release was marked heard" in refused["cause"]["message"]
    assert _heard(cfg) == []

    account.fail_on = frozenset()
    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["applied"]["added"] == 0
    assert account.deleted and account.deleted[-1][0] == ids[DATED]
    assert _heard(cfg) == ["r3"]


# ═══════════════════════════════════════════════════════════════════════════
# 5. The engine and the record
# ═══════════════════════════════════════════════════════════════════════════


def test_the_releases_of_a_dated_playlist_are_the_dated_plans_own(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r1", "r3", "r6"], DAY), _answer(["r4"], "2026-10-08")])
    read = playlists_cli.read_catalogue(cfg, _entry(), fake)
    document = sync_cli.load_record(cfg)
    assert heard.releases_of(document, read, "2023", DAY) == ("r3",)
    assert heard.releases_of(document, read, "2021", DAY) == ("r1",)
    assert heard.releases_of(document, read, "2023", "2026-10-08") == ("r4",)
    names = {step.name for step in _plan(cfg, fake, account).steps}
    assert names == {f"{LABEL} 2021 new {DAY}", DATED, f"{LABEL} 2023 new 2026-10-08"}


def test_the_heard_list_is_added_to_never_replaced_and_kept_sorted(installed):
    cfg = installed
    sync_cli.write_record(
        cfg,
        {
            "version": sync_cli.RECORD_VERSION,
            "labels": {LABEL_ID: {"asked": ["x"], heard.HEARD: ["r9"]}},
            "answers": [],
        },
    )
    assert heard.record_heard(cfg, LABEL_ID, ["r3", "r9"]) == 1
    held = sync_cli.load_record(cfg)["labels"][LABEL_ID]
    assert held[heard.HEARD] == ["r3", "r9"] and held["asked"] == ["x"]
    assert heard.record_heard(cfg, LABEL_ID, ["r3"]) == 0


def test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    made = _ids(account, folder_id)[DATED]
    assert ledger.product_made(cfg, made)
    ledger.forget_label_dated(cfg, LABEL_ID, made)
    assert not ledger.product_made(cfg, made)


def test_an_adopted_year_still_wins_over_a_dated_entry_for_the_same_identifier(installed):
    cfg = installed
    ledger.reserve_label_year(cfg, LABEL_ID, "2023", YEAR, lambda: "never", adopt="pl-9")
    assert ledger.reserve_label_dated(cfg, LABEL_ID, DATED, lambda: "pl-9") == "pl-9"
    assert not ledger.product_made(cfg, "pl-9")
    ledger.reserve_label_dated(cfg, LABEL_ID, DATED, lambda: "pl-10")
    assert ledger.product_made(cfg, "pl-10")


def test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for(installed):
    cfg = installed
    path = config.state_path("outbound_writes", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"version": 1, "labels": {"kompakt": {"years": {}, "dated": {"a": "", "": "pl-3", "b": "pl-4"}}}}',
        encoding="utf-8",
    )
    assert not ledger.product_made(cfg, "pl-3")
    assert ledger.product_made(cfg, "pl-4")


def test_the_plan_refuses_through_the_engine_as_through_the_verb(followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3"], DAY)])
    read = playlists_cli.read_catalogue(cfg, _entry(), fake)
    with pytest.raises(CratekitError) as caught:
        heard.plan(cfg, read, account, sync_cli.load_record(cfg), year="2023", day=DAY, named=["r4"])
    assert caught.value.cause.reason == "label-heard-not-in-playlist"


# ═══════════════════════════════════════════════════════════════════════════
# 6. The adapter's playlist removal, over a stand in for the client
# ═══════════════════════════════════════════════════════════════════════════


class ObjectNotFound(Exception):
    """Named as the client's own not found, which the adapter reads by name."""


class _Gone:
    def __init__(self, client: _Client, playlist_id: str) -> None:
        self.client = client
        self.id = playlist_id

    def delete(self) -> bool:
        self.client.deletes.append(self.id)
        if self.client.answer:
            self.client.held.discard(self.id)
        return self.client.answer


class _Client:
    def __init__(self, held: set[str], *, answer: bool = True, stays: bool = False) -> None:
        self.held = set(held)
        self.answer = answer
        self.stays = stays
        self.deletes: list[str] = []
        self.opened: list[str] = []

    def playlist(self, playlist_id: str) -> _Gone:
        self.opened.append(playlist_id)
        if playlist_id not in self.held and not (self.stays and self.deletes):
            raise ObjectNotFound(playlist_id)
        return _Gone(self, playlist_id)


def _vouched(cfg, playlist_id: str) -> None:
    ledger.reserve_label_dated(cfg, LABEL_ID, DATED, lambda: playlist_id)


def test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked(installed):
    client = _Client({"pl-1"})
    adapter = tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=installed)
    with pytest.raises(CratekitError) as caught:
        adapter.remove_playlist("pl-1")
    assert caught.value.cause.detail["problem"] == "not-product-made"
    assert client.opened == [] and client.deletes == []
    none = tidal_account.TidalAccount(client, sleep=lambda seconds: None)
    with pytest.raises(CratekitError):
        none.remove_playlist("pl-1")
    assert client.opened == []


def test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone(installed):
    _vouched(installed, "pl-1")
    client = _Client({"pl-1"})
    tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=installed).remove_playlist("pl-1")
    assert client.deletes == ["pl-1"]
    assert client.opened == ["pl-1", "pl-1"]


def test_a_playlist_already_gone_is_removed_with_no_delete(installed):
    _vouched(installed, "pl-1")
    client = _Client(set())
    tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=installed).remove_playlist("pl-1")
    assert client.deletes == []


def test_a_delete_the_client_answers_false_is_a_failure(installed):
    _vouched(installed, "pl-1")
    client = _Client({"pl-1"}, answer=False)
    with pytest.raises(CratekitError):
        tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=installed).remove_playlist(
            "pl-1"
        )
    assert client.deletes == ["pl-1"]


def test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed(installed):
    _vouched(installed, "pl-1")
    client = _Client({"pl-1"}, stays=True)
    with pytest.raises(CratekitError) as caught:
        tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=installed).remove_playlist(
            "pl-1"
        )
    assert caught.value.cause.detail["problem"] == "read-back-differs"
    assert client.deletes == ["pl-1"]


class _NotOwned(_Client):
    """The client hands back a playlist it does not read as this account's."""

    def playlist(self, playlist_id: str) -> object:
        self.opened.append(playlist_id)
        return object()


def test_a_playlist_the_client_does_not_serve_as_owned_is_refused_in_words(installed):
    _vouched(installed, "pl-1")
    client = _NotOwned({"pl-1"})
    with pytest.raises(CratekitError) as caught:
        tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=installed).remove_playlist(
            "pl-1"
        )
    assert caught.value.cause.detail["problem"] == "not-owned"
    assert client.deletes == []


# ═══════════════════════════════════════════════════════════════════════════
# 7. The review round's findings, each driven
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unreadable_ledger_refuses_a_dated_create_before_anything_exists(installed):
    cfg = installed
    path = config.state_path("outbound_writes", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")

    def create() -> str:
        raise AssertionError("the playlist was created before the ledger was read")

    with pytest.raises(CratekitError) as caught:
        ledger.reserve_label_dated(cfg, LABEL_ID, DATED, create)
    assert caught.value.cause.reason == "outbound-ledger-unusable"


def test_marking_heard_with_nothing_to_write_on_a_playlist_made_by_hand_is_not_refused(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    (folder_id,) = account.folder_names
    by_hand = account.create_playlist(DATED)
    account.move_to_folder(by_hand, folder_id)
    account.playlists[by_hand] = ["t6", "t7"]
    _record(cfg, [_answer(["r3", "r4"], DAY)])
    before = _writes(account)

    code, envelope = _two_acts([*VERB, "--release", "r3"])
    assert code == int(ExitCode.OK), envelope
    (playlist,) = [one for one in envelope["data"]["items"] if one["kind"] == "playlist"]
    assert playlist["action"] == heard.KEEP
    assert _writes(account) == before
    assert _heard(cfg) == ["r3"]


def test_a_dated_playlist_the_ledger_records_outside_the_folder_is_said(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r3"], DAY)])
    ledger.reserve_label_dated(cfg, LABEL_ID, DATED, lambda: "pl-at-root")

    code, refused = drive(VERB)
    (playlist,) = [one for one in refused["cause"]["detail"]["shown"]["items"] if one["kind"] == "playlist"]
    assert playlist["action"] == heard.ABSENT and playlist["id"] == "pl-at-root"
    assert "outside the folder" in playlist["why"]


def test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist(followed):
    cfg, fake, account = followed
    tracks, year = fake.releases["r4"]
    fake.releases["r4"] = ([FakeTrack("t5"), *tracks], year)
    folder_id = _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    dated_id = _ids(account, folder_id)[DATED]
    assert account.playlists[dated_id] == ["t4", "t5", "t6", "t7"]

    code, envelope = _two_acts([*VERB, "--release", "r3"])
    assert code == int(ExitCode.OK), envelope
    assert account.taken == [(dated_id, ("t4",))]
    assert account.playlists[dated_id] == ["t5", "t6", "t7"]


def test_what_the_merge_adds_to_a_recorded_year_is_recorded_on_it(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    year_id = _ids(account, folder_id)[YEAR]
    account.playlists[year_id].remove("t4")
    shape = ledger.label_shape(cfg, LABEL_ID)
    ledger_path = config.state_path("outbound_writes", cfg)
    document = json.loads(ledger_path.read_text(encoding="utf-8"))
    document["labels"][LABEL_ID]["years"]["2023"]["added"].remove("t4")
    ledger_path.write_text(json.dumps(document), encoding="utf-8")
    assert "t4" not in ledger.label_shape(cfg, LABEL_ID).years["2023"].added
    assert shape.years["2023"].remote_id == year_id

    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["applied"]["added"] == 1
    assert "t4" in ledger.label_shape(cfg, LABEL_ID).years["2023"].added


def test_a_year_known_only_by_the_marks_prefixed_name_is_the_year(followed):
    cfg, fake, account = followed
    folder_id = _made(cfg, fake, account, [_answer(["r3"], DAY)])
    old_year = _ids(account, folder_id)[YEAR]
    account.placed.pop(old_year)
    marked = account.create_playlist(f"DOWNLOADED {YEAR}")
    account.move_to_folder(marked, folder_id)

    code, envelope = _two_acts(VERB)
    assert code == int(ExitCode.OK), envelope
    assert account.playlists[marked] == ["t4", "t5"]
