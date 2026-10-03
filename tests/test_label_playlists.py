"""R-835: a followed label becomes a folder of year playlists on the account.

Every scenario the brief names is here, driven through the real dispatcher with
the two provider seams faked: the label catalogue, which the crawl reads, and
the streaming account, which records every call. The adapter's own folder
members are driven against a stand in for the client at the end. The live build
on the author's account is owed to an attended sitting and is not claimed here.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue, playlists_cli
from cratekit.label import registry as labels
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import folders, ledger, tidal_account
from cratekit.sync import mark_record
from cratekit.sync import playlists as sync_playlists
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import (
    FakeCatalogue,
    FakePagedArtist,
    FakeRelease,
    FakeTrack,
    UnreadableCatalogue,
    catalogue_factory,
)
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_label_workers import register
from tests.test_outbound_workers import bind as bind_account

BUILD = "label.playlists.confirm"
MARK = "label.mark.confirm"
LABEL = "Kompakt"
LABEL_ID = "kompakt"

#: Three release years, four releases, seven tracks, plus three releases the
#: plan must leave out for three different reasons.
RELEASES = {
    "r1": ([FakeTrack("t1"), FakeTrack("t2")], 2021),
    "r2": ([FakeTrack("t3")], 2022),
    "r3": ([FakeTrack("t4"), FakeTrack("t5")], 2023),
    "r4": ([FakeTrack("t6"), FakeTrack("t7")], 2023),
    # Dated by nothing the seam can read as a year.
    "r5": ([FakeTrack("t8")], None),
    # Not confirmed as the label's, since a roster artist's release elsewhere
    # is not this label's catalogue.
    "r6": ([FakeTrack("t9")], 2023),
}
LISTED = [
    FakeRelease("r1", year="2021"),
    FakeRelease("r2", year="2022"),
    FakeRelease("r3", year="2023"),
    FakeRelease("r4", year="2023"),
    FakeRelease("r5", year=""),
    FakeRelease("r6", year="2023"),
    # Listed and gone from the provider: no entry in RELEASES.
    FakeRelease("r7", year="2020"),
]


def _catalogue(releases=None, listed=None, **kwargs) -> FakeCatalogue:
    return FakeCatalogue(
        artists={LABEL_ID: FakePagedArtist(list(LISTED if listed is None else listed))},
        releases=dict(RELEASES if releases is None else releases),
        confirmed={"r1", "r2", "r3", "r4", "r5", "r7"},
        **kwargs,
    )


@pytest.fixture
def followed(installed, monkeypatch):
    """Kompakt followed, its catalogue faked, and an account that records calls."""
    register(LABEL)
    fake = _catalogue()
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    return installed, fake, account


def _entry() -> labels.LabelEntry:
    found = labels.RegistryStore().load().resolve(LABEL)
    assert found is not None
    return found


def _plan(cfg, fake, account) -> folders.Plan:
    return folders.plan(cfg, playlists_cli.read_catalogue(cfg, _entry(), fake), account)


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on an explicit gate, then the run that carries them out."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _build(option: str = "apply") -> tuple[int, dict]:
    return _two_acts(["label", "playlists", LABEL], BUILD, option)


def _years(account, folder_id: str) -> dict[str, list[str]]:
    """Each playlist the folder holds, by title, with its tracks."""
    return {
        account.titles[pid]: account.playlists[pid]
        for pid, held in account.placed.items()
        if held == folder_id
    }


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_both_verbs_write_only_the_account_behind_an_explicit_gate():
    for name, gate in (("label.playlists", BUILD), ("label.mark", MARK)):
        entry = registry.entry(name)
        assert entry.writes == frozenset({"remote"}), name
        assert entry.module_id == "labels" and entry.feature_rows == (23,)
        (spec,) = entry.gates
        assert (spec.name, spec.options, spec.explicit) == (gate, ("apply", "abort"), True)
        assert spec.digest_source == "plan"


def test_feature_row_23_is_a_module_row_and_no_longer_deferred():
    assert registry.features_by_row()[23].disposition == "module"


def test_the_mark_prefix_is_the_one_the_sweep_reads():
    assert folders.MARK_PREFIX == sync_playlists.SWEPT_PREFIX


# ═══════════════════════════════════════════════════════════════════════════
# 2. The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_three_years_plan_one_folder_and_three_playlists_with_their_counts(followed):
    cfg, fake, account = followed
    planned = _plan(cfg, fake, account)
    assert planned.folder_action == folders.CREATE
    assert [(s.year, s.name, s.action, s.move, s.add) for s in planned.years] == [
        ("2021", "Kompakt 2021", folders.CREATE, True, ("t1", "t2")),
        ("2022", "Kompakt 2022", folders.CREATE, True, ("t3",)),
        ("2023", "Kompakt 2023", folders.CREATE, True, ("t4", "t5", "t6", "t7")),
    ]
    read = planned.catalogue
    assert (read.releases, read.undated, read.dropped, read.gone) == (6, 1, 1, 1)
    assert account.created == [] and account.folders_created == []


def test_the_build_asks_before_anything_reaches_the_account(followed):
    _cfg, _fake, account = followed
    code, refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["year playlists"] == [
        "Kompakt 2021: create it private, put it in the folder, add 2 of 2 track(s)",
        "Kompakt 2022: create it private, put it in the folder, add 1 of 1 track(s)",
        "Kompakt 2023: create it private, put it in the folder, add 4 of 4 track(s)",
    ]
    assert account._writes == 0


def test_a_label_nobody_follows_is_a_plan_of_nothing_still_gated(installed, monkeypatch):
    fake = _catalogue()
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    code, done = _two_acts(["label", "playlists", "Nobody Follows This"], BUILD)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-not-followed"]
    assert fake.asked_for == [] and account._writes == 0


def test_a_catalogue_read_in_part_is_refused_before_the_gate(installed, monkeypatch):
    register(LABEL)

    class AlbumsOnly:
        def get_albums(self, limit=None, offset=0):
            return list(LISTED)[offset : offset + (limit or 100)]

    fake = _catalogue()
    fake.artists[LABEL_ID] = AlbumsOnly()
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    code, refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "label-playlists-incomplete"
    assert "gate" not in refused["cause"]["detail"]
    assert account._writes == 0


def test_a_release_whose_tracks_cannot_be_read_refuses_the_plan(installed, monkeypatch):
    register(LABEL)
    fake = UnreadableCatalogue(
        artists={LABEL_ID: FakePagedArtist(list(LISTED))}, releases=dict(RELEASES)
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    bind_account(monkeypatch, outbound_fakes.StrictAccount())
    code, refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "label-playlists-incomplete"


def test_two_root_folders_named_as_the_label_refuse_and_write_nothing(followed):
    _cfg, _fake, account = followed
    account.folder_names = {"f-a": LABEL, "f-b": LABEL}
    code, refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "label-playlists-ambiguous"
    assert account._writes == 0


# ═══════════════════════════════════════════════════════════════════════════
# 3. The build, and the second run
# ═══════════════════════════════════════════════════════════════════════════


def test_approved_the_account_holds_the_folder_and_three_private_playlists(followed):
    cfg, _fake, account = followed
    code, done = _build()
    assert code == int(ExitCode.OK), done
    assert account.folders_created == [LABEL]
    (folder_id,) = account.folder_names
    assert _years(account, folder_id) == {
        "Kompakt 2021": ["t1", "t2"],
        "Kompakt 2022": ["t3"],
        "Kompakt 2023": ["t4", "t5", "t6", "t7"],
    }
    assert account.private == set(account.placed)
    shape = ledger.label_shape(cfg, LABEL_ID)
    assert shape.folder_id == folder_id
    assert {year: sorted(y.added) for year, y in shape.years.items()} == {
        "2021": ["t1", "t2"],
        "2022": ["t3"],
        "2023": ["t4", "t5", "t6", "t7"],
    }


def test_declined_nothing_reaches_the_account(followed):
    _cfg, _fake, account = followed
    code, done = _build(option="abort")
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op" and account._writes == 0


def test_a_second_run_over_an_unchanged_catalogue_plans_nothing(followed):
    cfg, fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    writes = account._writes
    planned = _plan(cfg, fake, account)
    assert planned.folder_action == folders.REUSE
    assert not planned.writes, planned
    code, done = _build()
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert account._writes == writes


def test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated(followed):
    cfg, fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    (folder_id,) = account.folder_names
    by_hand = account.create_playlist("Kompakt 2024")
    account.move_to_folder(by_hand, folder_id)
    account.created.clear()
    fake.releases["r8"] = ([FakeTrack("t10")], 2024)
    fake.artists[LABEL_ID] = FakePagedArtist([*LISTED, FakeRelease("r8", year="2024")])
    fake.confirmed = fake.confirmed | {"r8"}

    planned = _plan(cfg, fake, account)
    (adopted,) = [step for step in planned.years if step.year == "2024"]
    assert (adopted.action, adopted.remote_id, adopted.move) == (folders.ADOPT, by_hand, False)
    assert _build()[0] == int(ExitCode.OK)
    assert account.created == []
    assert account.playlists[by_hand] == ["t10"]
    assert ledger.label_shape(cfg, LABEL_ID).years["2024"].remote_id == by_hand


def test_a_folder_made_by_hand_at_the_root_is_adopted(followed):
    cfg, fake, account = followed
    account.folder_names = {"f-hand": LABEL, "f-other": "Another Label"}
    assert _plan(cfg, fake, account).folder_action == folders.ADOPT
    assert _build()[0] == int(ExitCode.OK)
    assert account.folders_created == []
    assert set(account.placed.values()) == {"f-hand"}


def test_two_playlists_named_for_one_year_leave_that_year_alone(followed):
    cfg, fake, account = followed
    account.folder_names = {"f-hand": LABEL}
    for _ in range(2):
        account.move_to_folder(account.create_playlist("Kompakt 2022"), "f-hand")
    planned = _plan(cfg, fake, account)
    (left,) = [step for step in planned.years if step.year == "2022"]
    assert left.action == folders.AMBIGUOUS and not left.writes


# ═══════════════════════════════════════════════════════════════════════════
# 4. A refusal part way, and the resume
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes(
    followed,
):
    cfg, _fake, account = followed
    account.fail_on = frozenset({"Kompakt 2022"})
    code, failed = _build()
    assert code == int(ExitCode.INTERNAL), failed
    assert "were created" in failed["cause"]["message"]
    shape = ledger.label_shape(cfg, LABEL_ID)
    assert shape.folder_id and set(shape.years) == {"2021"}
    assert sorted(shape.years["2021"].added) == ["t1", "t2"]

    account.fail_on = frozenset()
    code, done = _build()
    assert code == int(ExitCode.OK), done
    assert account.folders_created == [LABEL]
    assert sorted(account.titles.values()) == ["Kompakt 2021", "Kompakt 2022", "Kompakt 2023"]
    (folder_id,) = account.folder_names
    assert _years(account, folder_id)["Kompakt 2021"] == ["t1", "t2"]
    assert len(account.chunks) == 3, "the resume added the first year's tracks again"


def test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again(
    followed,
):
    cfg, _fake, account = followed
    # The FIRST year playlist the fake will make. A move that fails on it is a
    # build stopped between the create and the move.
    account.fail_on = frozenset({"pl-1"})
    code, _failed = _build()
    assert code == int(ExitCode.INTERNAL)
    assert account.created == ["Kompakt 2021"] and "pl-1" not in account.placed

    account.fail_on = frozenset()
    assert _build()[0] == int(ExitCode.OK)
    assert account.created.count("Kompakt 2021") == 1
    (folder_id,) = account.folder_names
    assert account.placed["pl-1"] == folder_id
    assert account.playlists["pl-1"] == ["t1", "t2"]
    assert ledger.label_shape(cfg, LABEL_ID).years["2021"].remote_id == "pl-1"


def test_a_track_the_provider_will_not_add_is_recorded_and_not_asked_again(followed):
    cfg, fake, account = followed
    account.unaddable = {"t5"}
    code, done = _build()
    assert code == int(ExitCode.OK), done
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-tracks-refused"]
    assert ledger.label_shape(cfg, LABEL_ID).years["2023"].refused == frozenset({"t5"})
    assert not _plan(cfg, fake, account).writes


def test_a_track_taken_off_by_a_person_is_not_put_back(followed):
    cfg, fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    year = ledger.label_shape(cfg, LABEL_ID).years["2021"].remote_id
    account.playlists[year].remove("t2")
    assert not _plan(cfg, fake, account).writes


def test_a_ledger_written_by_another_verb_keeps_the_label_shape(followed):
    """``_load`` rebuilds the document, so a key it forgot is dropped on every
    write, and the next build would make the whole folder a second time."""
    cfg, _fake, _account = followed
    assert _build()[0] == int(ExitCode.OK)
    before = ledger.label_shape(cfg, LABEL_ID)
    ledger.record_heart(cfg, "tid-1")
    ledger.record_playlist(cfg, "crate", "remote-1")
    assert ledger.label_shape(cfg, LABEL_ID) == before


def test_the_sweep_never_reads_a_built_year_playlist_as_intake(followed):
    cfg, _fake, _account = followed
    assert _build()[0] == int(ExitCode.OK)
    built = ledger.label_playlist_ids(cfg)
    assert len(built) == 3
    for playlist_id in built:
        listed = AccountPlaylist(playlist_id=playlist_id, name="Kompakt 2021", tracks=2)
        assert (
            sync_playlists.exclusion(
                listed, recorded=set(), in_flight=set(), label_built=built
            )
            is sync_playlists.Excluded.LABEL_FOLDER
        )


# ═══════════════════════════════════════════════════════════════════════════
# 5. The mark, recorded for sync unmark
# ═══════════════════════════════════════════════════════════════════════════


def _landed(cfg, name: str = "label-sync-batch") -> Path:
    folder = cfg.library.root / "landed"
    return outbound_fakes.write_export(folder).rename(folder / f"{name}_inboxed.xml")


def _mark(xml: Path, option: str = "apply") -> tuple[int, dict]:
    return _two_acts(["label", "mark", LABEL, "--xml", str(xml)], MARK, option)


def test_the_prefix_step_renames_each_year_and_records_it_for_unmark(followed):
    cfg, _fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    xml = _landed(cfg)
    code, done = _mark(xml)
    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-1", "DOWNLOADED Kompakt 2021"),
        ("pl-2", "DOWNLOADED Kompakt 2022"),
        ("pl-3", "DOWNLOADED Kompakt 2023"),
    ]
    held = mark_record.MarkRecord(cfg).of_pass("label-sync-batch")
    assert sorted((e.playlist_id, e.name, e.to) for e in held) == [
        ("pl-1", "Kompakt 2021", "DOWNLOADED Kompakt 2021"),
        ("pl-2", "Kompakt 2022", "DOWNLOADED Kompakt 2022"),
        ("pl-3", "Kompakt 2023", "DOWNLOADED Kompakt 2023"),
    ]


def test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years(
    followed,
):
    cfg, fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    xml = _landed(cfg)
    assert _mark(xml)[0] == int(ExitCode.OK)
    account.renamed.clear()
    code, done = _mark(xml)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op" and account.renamed == []
    assert not _plan(cfg, fake, account).writes


def test_sync_unmark_takes_the_label_mark_off_again(followed):
    cfg, fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    assert _mark(_landed(cfg))[0] == int(ExitCode.OK)
    fake.account = [
        AccountPlaylist(playlist_id=pid, name=title, tracks=None)
        for pid, title in account.titles.items()
    ]
    account.renamed.clear()
    code, done = _two_acts(
        ["sync", "unmark", "--pass", "label-sync-batch"], "sync.unmark.confirm"
    )
    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-1", "Kompakt 2021"),
        ("pl-2", "Kompakt 2022"),
        ("pl-3", "Kompakt 2023"),
    ]


def test_a_mark_with_no_landed_file_refuses_before_anything(followed):
    cfg, _fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    missing = cfg.library.root / "landed" / "never-landed_inboxed.xml"
    code, refused = drive(["label", "mark", LABEL, "--xml", str(missing)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert account.renamed == []


def test_a_year_retitled_since_it_was_built_is_left_alone(followed):
    cfg, _fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    account.titles["pl-2"] = "Kompakt Classics"
    code, done = _mark(_landed(cfg))
    assert code == int(ExitCode.OK), done
    assert "pl-2" not in dict(account.renamed)
    reasons = {item["id"]: item.get("reason") for item in done["data"]["items"]}
    assert reasons["pl-2"] == "retitled-since-built"


# ═══════════════════════════════════════════════════════════════════════════
# 6. Add only, by the suite's own scan
# ═══════════════════════════════════════════════════════════════════════════

SOURCES = (
    Path(folders.__file__),
    Path(playlists_cli.__file__),
    Path(playlists_cli.__file__).with_name("mark_cli.py"),
)


@pytest.mark.parametrize("source", SOURCES, ids=lambda p: p.name)
def test_no_removal_shape_appears_in_the_label_folder_path(source):
    shapes = ("remove", "delete", "unheart", "unlike", "clear")
    named = sorted(
        {
            node.attr if isinstance(node, ast.Attribute) else node.name
            for node in ast.walk(ast.parse(source.read_text(encoding="utf-8")))
            if (isinstance(node, ast.Attribute) and any(s in node.attr.lower() for s in shapes))
            or (
                isinstance(node, ast.FunctionDef)
                and any(s in node.name.lower() for s in shapes)
            )
        }
    )
    assert named == [], named


# ═══════════════════════════════════════════════════════════════════════════
# 7. The adapter's folder members, over a stand in for the client
# ═══════════════════════════════════════════════════════════════════════════


class _Named:
    def __init__(self, item_id: str, name: str) -> None:
        self.id = item_id
        self.name = name


class _Folder:
    """The client's folder object as the adapter builds it: empty, then named."""

    def __init__(self, client: _Client) -> None:
        self.client = client
        self.id = None

    def items(self, offset: int = 0, limit: int = 50) -> list[_Named]:
        held = [
            _Named(pid, self.client.titles[pid])
            for pid, folder in self.client.placed.items()
            if folder == self.id
        ]
        self.client.pages.append(("items", limit, offset))
        return held[offset : offset + limit]

    def move_items_to_folder(self, trns: list[str], folder: str | None = None) -> bool:
        self.client.moves.append((tuple(trns), folder))
        if self.client.move_fail:
            raise self.client.move_fail.pop(0)
        if not self.client.move_answer:
            return False
        for trn in trns:
            self.client.placed[trn] = folder
        return True


class _Favorites:
    def __init__(self, client: _Client) -> None:
        self.client = client

    def playlist_folders(self, limit: int = 50, offset: int = 0) -> list[_Named]:
        self.client.pages.append(("folders", limit, offset))
        return self.client.root[offset : offset + limit]


class _User:
    def __init__(self, client: _Client) -> None:
        self.client = client
        self.favorites = _Favorites(client)

    def create_folder(self, title: str, parent_id: str = "root") -> _Named:
        del parent_id
        self.client.folder_creates.append(title)
        if self.client.create_fail is not None:
            raise self.client.create_fail
        made = _Named(f"folder-{len(self.client.folder_creates)}", title)
        self.client.root.append(made)
        return made


class _Playlist:
    def __init__(self, members: list[str], skip: set[str]) -> None:
        self.members = members
        self.skip = skip
        self.adds: list[list[str]] = []
        self.num_tracks = len(members)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[_Named]:
        size = 100 if limit is None else limit
        return [_Named(one, one) for one in self.members[offset : offset + size]]

    def add(self, media_ids: list[str]) -> list[str]:
        self.adds.append(list(media_ids))
        fresh = [one for one in media_ids if one not in self.skip and one not in self.members]
        self.members.extend(fresh)
        self.num_tracks = len(self.members)
        return fresh


class _Client:
    def __init__(self) -> None:
        self.root: list[_Named] = []
        self.titles: dict[str, str] = {}
        self.placed: dict[str, str] = {}
        self.pages: list[tuple[str, int, int]] = []
        self.moves: list[tuple[tuple[str, ...], str | None]] = []
        self.move_fail: list[Exception] = []
        self.move_answer = True
        self.folder_creates: list[str] = []
        self.create_fail: Exception | None = None
        self.user = _User(self)
        self.lists: dict[str, _Playlist] = {}

    def folder(self, folder_id: str | None = None) -> _Folder:
        assert folder_id is None, "the adapter asked the client's own folder lookup"
        return _Folder(self)

    def playlist(self, playlist_id: str) -> _Playlist:
        return self.lists[playlist_id]


def _adapter(client: _Client) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(client, sleep=lambda seconds: None)


def test_the_root_folders_are_read_past_one_page():
    client = _Client()
    client.root = [_Named(f"f{index}", f"Label {index}") for index in range(120)]
    found = _adapter(client).folders()
    assert len(found) == 120 and found["f119"] == "Label 119"
    assert [page for page in client.pages if page[0] == "folders"][-1] == ("folders", 50, 150)


def test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup():
    client = _Client()
    for index in range(60):
        client.titles[f"p{index}"] = f"Label {1960 + index}"
        client.placed[f"p{index}"] = "f1"
    client.placed["elsewhere"] = "f2"
    client.titles["elsewhere"] = "Other"
    found = _adapter(client).folder_playlists("f1")
    assert len(found) == 60 and "elsewhere" not in found


def test_a_folder_create_is_never_retried_into_a_second_folder():
    client = _Client()
    client.create_fail = TimeoutError("the create timed out after it reached the provider")
    with pytest.raises(CratekitError):
        _adapter(client).create_folder(LABEL)
    assert client.folder_creates == [LABEL]


def test_a_created_folder_returns_the_identifier_the_provider_assigned():
    client = _Client()
    assert _adapter(client).create_folder(LABEL) == "folder-1"


def test_a_move_refused_once_is_retried_once_and_lands():
    client = _Client()
    client.move_fail = [TimeoutError("a dropped connection")]
    _adapter(client).move_to_folder("p1", "f1")
    assert client.placed["p1"] == "f1" and len(client.moves) == 2
    assert client.moves[-1] == (("p1",), "f1")


def test_a_move_the_client_answers_false_is_a_failure_not_a_quiet_return():
    client = _Client()
    client.move_answer = False
    with pytest.raises(CratekitError):
        _adapter(client).move_to_folder("p1", "f1")


def test_tracks_are_added_in_chunks_and_members_are_never_asked_again():
    client = _Client()
    client.lists["p1"] = _Playlist(["a0"], skip=set())
    wanted = tuple(f"a{index}" for index in range(250))
    held = _adapter(client).add_tracks("p1", wanted)
    assert held == wanted
    assert [len(chunk) for chunk in client.lists["p1"].adds] == [100, 100, 49]
    assert "a0" not in client.lists["p1"].adds[0]


def test_a_track_the_client_skips_is_read_again_and_left_out_of_the_answer():
    client = _Client()
    client.lists["p1"] = _Playlist([], skip={"b2"})
    assert _adapter(client).add_tracks("p1", ("b1", "b2", "b3")) == ("b1", "b3")


def test_the_client_library_still_offers_the_folder_calls_the_adapter_makes():
    """A rename upstream would fail every folder member at the provider; this
    turns it red here instead."""
    import tidalapi.playlist
    import tidalapi.user

    assert callable(getattr(tidalapi.user.LoggedInUser, "create_folder", None))
    assert callable(getattr(tidalapi.user.Favorites, "playlist_folders", None))
    assert callable(getattr(tidalapi.playlist.Folder, "items", None))
    assert callable(getattr(tidalapi.playlist.Folder, "move_items_to_folder", None))
