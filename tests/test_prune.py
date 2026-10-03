"""R-836: a dropped track leaves a playlist this product made, and nothing else does.

Every scenario the brief names is here. The two prune verbs are driven through
the real dispatcher with the provider seams faked: the label catalogue, the
review database's holds, which are real, and the streaming account, which
records every call. The adapter's one removal is driven against a stand in for
the client at the end, where the refusal before any provider call is proved.
The live prune of one label is owed to an attended sitting and is not claimed.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.cli import registry
from cratekit.core import review
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import Queue
from cratekit.label import catalogue, sweep
from cratekit.modules.outbound import export as outbound_export
from cratekit.modules.outbound import ledger, prune, tidal_account
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_label_playlists import LABEL, LABEL_ID, RELEASES
from tests.test_label_workers import register
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture

BUILD = "label.playlists.confirm"
PRUNE = "label.prune.confirm"
EXPORT_PRUNE = "export.prune.confirm"

#: The build's catalogue less the release the provider no longer has, so every
#: confirmed release's tracks are read and a track no longer confirmed is
#: judged. Years 2021 (pl-1: t1 t2), 2022 (pl-2: t3), 2023 (pl-3: t4 to t7).
LISTED = [
    FakeRelease("r1", year="2021"),
    FakeRelease("r2", year="2022"),
    FakeRelease("r3", year="2023"),
    FakeRelease("r4", year="2023"),
    FakeRelease("r5", year=""),
    FakeRelease("r6", year="2023"),
]
CONFIRMED = frozenset({"r1", "r2", "r3", "r4", "r5"})


def _catalogue(confirmed=CONFIRMED, listed=None) -> FakeCatalogue:
    return FakeCatalogue(
        artists={LABEL_ID: FakePagedArtist(list(LISTED if listed is None else listed))},
        releases=dict(RELEASES),
        confirmed=set(confirmed),
    )


@pytest.fixture
def built(installed, monkeypatch):
    """Kompakt followed, its three years built on a fake account, the build approved."""
    register(LABEL)
    fake = _catalogue()
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    code, done = _two_acts(["label", "playlists", LABEL], BUILD)
    assert code == int(ExitCode.OK), done
    assert account.playlists == {"pl-1": ["t1", "t2"], "pl-2": ["t3"], "pl-3": ["t4", "t5", "t6", "t7"]}
    return SimpleNamespace(cfg=installed, fake=fake, account=account, monkeypatch=monkeypatch)


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _prune(option: str = "apply") -> tuple[int, dict]:
    return _two_acts(["label", "prune", LABEL], PRUNE, option)


def _hold(cfg, *release_ids: str) -> None:
    with review.open_store(cfg) as store:
        for release_id in release_ids:
            review.hold(
                store,
                queue=Queue.LABEL_RELEASE,
                kind=sweep.KIND,
                identity={"release_id": release_id},
                payload={"identity": release_id, "title": f"Release {release_id}"},
                group=LABEL_ID,
                name=LABEL,
                reason="held",
                detail={"genres": ["Christian"], "kind": "dance"},
                run_id="run-1",
            )


def _taken(envelope: dict) -> list[tuple[str, str]]:
    return [
        (item["playlist"], item["id"])
        for item in envelope["data"]["items"]
        if item["action"] == "take-off"
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_both_prune_verbs_write_only_the_account_behind_an_explicit_gate():
    for name, gate, module, row in (
        ("label.prune", PRUNE, "labels", 23),
        ("export.prune", EXPORT_PRUNE, "export", 36),
    ):
        entry = registry.entry(name)
        assert entry.writes == frozenset({"remote"}), name
        assert entry.destructive is True, name
        assert entry.module_id == module and entry.feature_rows == (row,)
        (spec,) = entry.gates
        assert (spec.name, spec.options, spec.explicit) == (gate, ("apply", "abort"), True)
        assert spec.digest_source == "plan"


def test_the_protocol_declares_exactly_one_removal():
    removals = {name for name in outbound_fakes.PROTOCOL_METHODS if "remove" in name}
    assert removals == {"remove_tracks"}


# ═══════════════════════════════════════════════════════════════════════════
# 2. A label's year playlists
# ═══════════════════════════════════════════════════════════════════════════


def test_a_held_release_plans_exactly_its_tracks_and_approved_only_they_leave(built):
    _hold(built.cfg, "r3")
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert _taken(done) == [("pl-3", "t4"), ("pl-3", "t5")]
    assert built.account.playlists == {"pl-1": ["t1", "t2"], "pl-2": ["t3"], "pl-3": ["t6", "t7"]}
    year = ledger.label_shape(built.cfg, LABEL_ID).years["2023"]
    assert year.pruned == frozenset({"t4", "t5"})
    assert year.added == frozenset({"t6", "t7"})
    assert done["data"]["totals"]["applied"]["taken"] == {"Kompakt 2023": ["t4", "t5"]}


def test_a_release_the_catalogue_no_longer_confirms_plans_its_tracks(built):
    built.monkeypatch.setattr(
        catalogue, "resolve", catalogue_factory(_catalogue(confirmed=CONFIRMED - {"r2"}))
    )
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert _taken(done) == [("pl-2", "t3")]
    assert built.account.playlists["pl-2"] == []
    assert built.account.playlists["pl-1"] == ["t1", "t2"]


def test_a_release_the_provider_no_longer_has_stops_the_unconfirmed_judgement(built):
    """r7 is confirmed and gone, so any track could be its: only holds are judged."""
    built.monkeypatch.setattr(
        catalogue,
        "resolve",
        catalogue_factory(
            _catalogue(
                confirmed=(CONFIRMED - {"r2"}) | {"r7"},
                listed=[*LISTED, FakeRelease("r7", year="2020")],
            )
        ),
    )
    _hold(built.cfg, "r1")
    code, refused = drive(["label", "prune", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert list(shown["take off"]) == ["Kompakt 2021"]
    assert "provider no longer has" in shown["not judged"][0]


def test_a_track_on_a_held_release_and_a_kept_one_of_the_same_year_stays(built):
    built.fake.releases["r4"] = (
        [*built.fake.releases["r4"][0], *built.fake.releases["r3"][0][:1]],
        2023,
    )
    _hold(built.cfg, "r3")
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert _taken(done) == [("pl-3", "t5")]
    assert built.account.playlists["pl-3"] == ["t4", "t6", "t7"]


def test_the_gate_lists_every_track_by_artist_and_title_per_playlist(built):
    built.account.names.update({"t4": ("Artist Four", "Four"), "t5": ("Artist Five", "Five")})
    _hold(built.cfg, "r3")
    code, refused = drive(["label", "prune", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["take off"] == {"Kompakt 2023": ["Artist Four - Four", "Artist Five - Five"]}
    assert built.account.taken == []


def test_an_empty_plan_still_asks_and_takes_nothing(built):
    code, refused = drive(["label", "prune", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == PRUNE
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert done["data"]["items"] == [] and done["data"]["totals"]["writes"] is False
    assert built.account.taken == []


def test_a_second_run_plans_nothing(built):
    _hold(built.cfg, "r3")
    assert _prune()[0] == int(ExitCode.OK)
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert _taken(done) == []
    assert built.account.taken == [("pl-3", ("t4", "t5"))]


def test_a_refusal_part_way_resumes_without_taking_anything_off_twice(built):
    _hold(built.cfg, "r1", "r3")
    built.account.fail_on = frozenset({"pl-3"})
    built.account.transient = True
    code, refused = _prune()
    assert code != int(ExitCode.OK), refused
    assert "2 track(s) were taken off" in refused["cause"]["message"]
    assert built.account.playlists["pl-1"] == []
    assert built.account.playlists["pl-3"] == ["t4", "t5", "t6", "t7"]
    built.account.fail_on = frozenset()
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert _taken(done) == [("pl-3", "t4"), ("pl-3", "t5")]
    asked = [playlist for playlist, _ids in built.account.taken]
    assert asked.count("pl-1") == 1


def test_a_pruned_track_is_not_put_back_by_the_next_build(built):
    _hold(built.cfg, "r3")
    assert _prune()[0] == int(ExitCode.OK)
    code, done = _two_acts(["label", "playlists", LABEL], BUILD)
    assert code == int(ExitCode.OK), done
    assert built.account.playlists["pl-3"] == ["t6", "t7"]


def test_a_year_adopted_from_the_account_is_said_and_left_alone(installed, monkeypatch):
    register(LABEL)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(_catalogue()))
    account = outbound_fakes.StrictAccount()
    account.folder_names["folder-made"] = LABEL
    account.playlists["by-hand"] = []
    account.titles["by-hand"] = "Kompakt 2023"
    account.placed["by-hand"] = "folder-made"
    bind_account(monkeypatch, account)
    assert _two_acts(["label", "playlists", LABEL], BUILD)[0] == int(ExitCode.OK)
    assert ledger.label_shape(installed, LABEL_ID).years["2023"].created is False
    _hold(installed, "r3")
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    (item,) = done["data"]["items"]
    assert (item["id"], item["action"], item["would"]) == ("by-hand", "left-alone", 2)
    assert account.taken == []
    assert account.playlists["by-hand"] == ["t4", "t5", "t6", "t7"]


def test_a_track_a_person_added_by_hand_is_never_planned(built):
    built.account.playlists["pl-3"].append("by-hand")
    built.monkeypatch.setattr(
        catalogue, "resolve", catalogue_factory(_catalogue(confirmed=CONFIRMED - {"r3"}))
    )
    code, done = _prune()
    assert code == int(ExitCode.OK), done
    assert _taken(done) == [("pl-3", "t4"), ("pl-3", "t5")]
    assert "by-hand" in built.account.playlists["pl-3"]


def test_the_apply_asks_the_ledger_again_and_refuses_a_playlist_it_no_longer_vouches_for(
    installed,
):
    account = outbound_fakes.FakeAccount()
    account.playlists["elsewhere"] = ["t1"]
    planned = prune.Plan(
        kind=prune.EXPORTED,
        subject="crate",
        playlists=(
            prune.PlaylistPrune(
                key="crate", name="Crate", remote_id="elsewhere", take=(prune.Taken("t1"),)
            ),
        ),
    )
    with pytest.raises(CratekitError) as refused:
        prune.apply(installed, account, planned, prune.Pruned())
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert account.taken == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. An exported playlist
# ═══════════════════════════════════════════════════════════════════════════


def _exported(cfg, account) -> None:
    """The crate's three tracks written to the account by the export engine."""
    planned = outbound_export.plan(
        [outbound_export.LocalTrack(identity=str(index)) for index in (1, 2, 3)],
        playlist_key=outbound_fakes.CRATE,
        name=outbound_fakes.CRATE,
        account=account,
    )
    outbound_export.apply(cfg, account, planned)
    assert account.playlists["pl-1"] == ["tid-1", "tid-2", "tid-3"]


def _export_prune(path, option: str = "apply") -> tuple[int, dict]:
    return _two_acts(
        ["export", "prune", outbound_fakes.CRATE, "--export", str(path)], EXPORT_PRUNE, option
    )


def test_an_exported_playlist_whose_library_playlist_lost_a_track_plans_exactly_it(
    installed, monkeypatch
):
    account = outbound_fakes.FakeAccount(catalog={str(i): f"tid-{i}" for i in (1, 2, 3)})
    bind_account(monkeypatch, account)
    _exported(installed, account)
    now = outbound_fakes.write_export(installed.library.root / "outbound", crate=(1, 2))
    code, done = _export_prune(now)
    assert code == int(ExitCode.OK), done
    assert _taken(done) == [("pl-1", "tid-3")]
    assert account.playlists["pl-1"] == ["tid-1", "tid-2"]
    record = ledger.exported_playlist(installed, outbound_fakes.CRATE)
    assert record is not None
    assert (record.added, record.pruned) == (frozenset({"tid-1", "tid-2"}), frozenset({"tid-3"}))
    code, again = _export_prune(now)
    assert code == int(ExitCode.OK), again
    assert _taken(again) == []
    assert account.taken == [("pl-1", ("tid-3",))]


def test_an_unmatched_row_leaves_the_exported_playlist_alone(installed, monkeypatch):
    account = outbound_fakes.FakeAccount(catalog={str(i): f"tid-{i}" for i in (1, 2, 3)})
    bind_account(monkeypatch, account)
    _exported(installed, account)
    del account.catalog["2"]
    now = outbound_fakes.write_export(installed.library.root / "outbound", crate=(1, 2))
    code, done = _export_prune(now)
    assert code == int(ExitCode.OK), done
    (item,) = done["data"]["items"]
    assert (item["action"], item["would"]) == ("left-alone", 2)
    assert account.taken == []


def test_a_playlist_never_exported_is_a_plan_of_nothing_still_gated(installed, monkeypatch):
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    now = outbound_fakes.write_export(installed.library.root / "outbound")
    code, done = _export_prune(now)
    assert code == int(ExitCode.OK), done
    assert done["data"]["items"] == []
    assert account.matches == [] and account.taken == []


# ═══════════════════════════════════════════════════════════════════════════
# 4. The ledger's answer
# ═══════════════════════════════════════════════════════════════════════════


def test_product_made_says_yes_only_where_a_record_does(installed):
    ledger.reserve_label_year(installed, "lbl", "2021", "L 2021", lambda: "made")
    ledger.reserve_label_year(installed, "lbl", "2022", "L 2022", lambda: "never", adopt="adopted")
    ledger.reserve_set_playlist(installed, "A Set", "2026", lambda: "set-made")
    ledger.reserve_playlist(installed, "crate", lambda: "exported")
    assert ledger.product_made(installed, "made") is True
    assert ledger.product_made(installed, "set-made") is True
    assert ledger.product_made(installed, "exported") is True
    assert ledger.product_made(installed, "adopted") is False
    assert ledger.product_made(installed, "nobody") is False
    assert ledger.product_made(installed, "") is False


def test_a_year_recorded_before_this_build_is_not_product_made(installed):
    ledger.reserve_label_year(installed, "lbl", "2021", "L 2021", lambda: "made")
    document = ledger._load(installed)
    del document["labels"]["lbl"]["years"]["2021"]["created"]
    ledger._write(installed, document)
    assert ledger.product_made(installed, "made") is False


def test_adopted_anywhere_wins_over_another_record_of_the_same_playlist(installed):
    ledger.reserve_label_year(installed, "lbl", "2022", "L 2022", lambda: "x", adopt="shared")
    ledger.reserve_set_playlist(installed, "A Set", "2026", lambda: "shared")
    assert ledger.product_made(installed, "shared") is False


# ═══════════════════════════════════════════════════════════════════════════
# 5. The adapter's one removal, over a stand in for the client
# ═══════════════════════════════════════════════════════════════════════════


class _Track:
    def __init__(self, track_id: str) -> None:
        self.id = track_id
        self.name = f"Title {track_id}"
        self.full_name = f"Title {track_id}"
        self.artists = [SimpleNamespace(name=f"Artist {track_id}")]


class _Store:
    """The provider's playlists, shared by every object the client opens on them."""

    def __init__(self) -> None:
        self.members: dict[str, list[str]] = {}
        self.hidden: dict[str, int] = {}
        self.videos: dict[str, int] = {}
        self.opened: list[str] = []
        self.removals: list[tuple[str, tuple[int, ...]]] = []
        self.fail: list[Exception] = []
        self.answer = True
        #: Positions the provider takes off instead of the asked ones, once.
        self.wrong: list[int] | None = None


class _Playlist:
    def __init__(self, store: _Store, playlist_id: str) -> None:
        self.store = store
        self.id = playlist_id
        members = store.members[playlist_id]
        self.num_tracks = len(members) + store.hidden.get(playlist_id, 0)
        self.num_videos = store.videos.get(playlist_id, 0)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[_Track]:
        size = 100 if limit is None else limit
        return [_Track(one) for one in self.store.members[self.id][offset : offset + size]]

    def remove_by_indices(self, indices) -> bool:
        asked = tuple(indices)
        self.store.removals.append((self.id, asked))
        if self.store.fail:
            raise self.store.fail.pop(0)
        if not self.store.answer:
            return False
        taken = set(self.store.wrong if self.store.wrong is not None else asked)
        self.store.wrong = None
        members = self.store.members[self.id]
        self.store.members[self.id] = [one for i, one in enumerate(members) if i not in taken]
        return True


class _Client:
    def __init__(self, store: _Store) -> None:
        self.store = store

    def playlist(self, playlist_id: str) -> _Playlist:
        self.store.opened.append(playlist_id)
        return _Playlist(self.store, playlist_id)


def _adapter(cfg, store: _Store) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(_Client(store), sleep=lambda seconds: None, cfg=cfg)


def _made(cfg, store: _Store, playlist_id: str, members: list[str]) -> None:
    ledger.reserve_set_playlist(cfg, f"set {playlist_id}", "2026", lambda: playlist_id)
    store.members[playlist_id] = list(members)


def test_a_removal_from_a_playlist_the_product_did_not_create_is_refused_before_any_call(
    installed,
):
    store = _Store()
    store.members["theirs"] = ["a", "b"]
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).remove_tracks("theirs", ("a",))
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert refused.value.cause.detail["problem"] == "not-product-made"
    assert store.opened == [] and store.removals == []
    assert store.members["theirs"] == ["a", "b"]


def test_an_adapter_with_no_configuration_refuses_every_removal(installed):
    store = _Store()
    _made(installed, store, "mine", ["a"])
    with pytest.raises(CratekitError) as refused:
        _adapter(None, store).remove_tracks("mine", ("a",))
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert store.opened == []


def test_the_adapter_takes_off_every_occurrence_of_the_asked_tracks_and_nothing_else(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b", "c", "b", "d"])
    gone = _adapter(installed, store).remove_tracks("mine", ("b", "d", "never-there"))
    assert gone == ("b", "d", "never-there")
    assert store.members["mine"] == ["a", "c"]
    assert store.removals == [("mine", (1, 3, 4))]


def test_more_than_one_chunk_is_taken_off_one_request_at_a_time(installed):
    store = _Store()
    members = [f"t{index}" for index in range(tidal_account.REMOVE_CHUNK + 5)]
    _made(installed, store, "mine", [*members, "keep"])
    gone = _adapter(installed, store).remove_tracks("mine", tuple(members))
    assert gone == tuple(members)
    assert store.members["mine"] == ["keep"]
    assert [len(asked) for _pid, asked in store.removals] == [tidal_account.REMOVE_CHUNK, 5]


def test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b"])
    store.hidden["mine"] = 1
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).remove_tracks("mine", ("b",))
    assert refused.value.cause.detail["problem"] == "positions-unknown"
    assert store.removals == []


def test_a_playlist_holding_a_video_is_refused_with_nothing_sent(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b"])
    store.videos["mine"] = 1
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).remove_tracks("mine", ("b",))
    assert refused.value.cause.detail["problem"] == "positions-unknown"
    assert store.removals == []


def test_a_removal_the_provider_refuses_once_is_never_sent_again(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b"])
    store.fail = [RuntimeError("timed out")]
    with pytest.raises(CratekitError):
        _adapter(installed, store).remove_tracks("mine", ("b",))
    assert store.removals == [("mine", (1,))]


def test_a_removal_answered_false_is_a_failure_not_a_quiet_return(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b"])
    store.answer = False
    with pytest.raises(CratekitError):
        _adapter(installed, store).remove_tracks("mine", ("b",))


def test_a_removal_that_took_the_wrong_position_is_read_back_and_refused(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b", "c"])
    store.wrong = [0]
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).remove_tracks("mine", ("b",))
    assert "read back" in refused.value.cause.message


def test_the_adapter_names_each_track_by_artist_and_title(installed):
    store = _Store()
    _made(installed, store, "mine", ["a", "b"])
    assert _adapter(installed, store).track_names("mine") == {
        "a": ("Artist a", "Title a"),
        "b": ("Artist b", "Title b"),
    }


def test_the_client_library_still_offers_the_removal_the_adapter_makes():
    import tidalapi.playlist

    assert callable(getattr(tidalapi.playlist.UserPlaylist, "remove_by_indices", None))
    assert "remove_by_indices" in Path(tidal_account.__file__).read_text(encoding="utf-8")


def test_the_hold_reader_returns_the_held_release_identifiers(installed):
    from cratekit.label import prune_cli

    _hold(installed, "r3", "r5")
    assert prune_cli.held_releases(installed, LABEL_ID) == frozenset({"r3", "r5"})


def test_a_build_marks_a_year_it_created_and_not_one_it_adopted(built):
    shape = ledger.label_shape(built.cfg, LABEL_ID)
    assert {year: one.created for year, one in shape.years.items()} == {
        "2021": True,
        "2022": True,
        "2023": True,
    }
