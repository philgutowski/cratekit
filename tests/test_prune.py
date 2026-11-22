"""R-836: a dropped track leaves a playlist this product made, and nothing else does.

Both prune verbs through the real dispatcher, the provider seams faked and the review holds
real; the adapter's removal over a stand in for the client. D1 applies.
"""

from __future__ import annotations

import copy
import os
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.cli import registry
from cratekit.core import review
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import Queue
from cratekit.label import catalogue, sweep
from cratekit.label import registry as labels
from cratekit.modules.outbound import export as outbound_export
from cratekit.modules.outbound import ledger, prune, tidal_account
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_label_playlists import LABEL, LABEL_ID, RELEASES
from tests.test_label_workers import register
from tests.test_organize_mirror import persons_playlist
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture

BUILD = "label.playlists.confirm"
PRUNE = "label.prune.confirm"
EXPORT_PRUNE = "export.prune.confirm"
OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)

#: The build's catalogue less the release the provider no longer has, so every
#: confirmed release's tracks are read. Years 2021 (pl-1: t1 t2), 2022 (pl-2:
#: t3), 2023 (pl-3: t4 to t7).
YEARS = {"r1": "2021", "r2": "2022", "r3": "2023", "r4": "2023", "r5": "", "r6": "2023"}
LISTED = [FakeRelease(release, year=year) for release, year in YEARS.items()]
CONFIRMED = frozenset({"r1", "r2", "r3", "r4", "r5"})
BUILT = {"pl-1": ["t1", "t2"], "pl-2": ["t3"], "pl-3": ["t4", "t5", "t6", "t7"]}


#: The verifier's word on a release it credits to another label.
ELSEWHERE = {"verdict": "mismatch", "resolved_label": "Another Label", "source": "fake-catalogue"}


class _Credited(FakeCatalogue):
    """The fake catalogue, with releases the verifier credits to another label."""

    def __init__(self, *args, elsewhere=(), **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.elsewhere = frozenset(elsewhere)

    def search_release(self, claimed, release) -> dict:
        if str(getattr(release, "id", "") or "") in self.elsewhere:
            return {**ELSEWHERE, "notes": "credited as 'Another Label'"}
        return super().search_release(claimed, release)


def _catalogue(confirmed=CONFIRMED, listed=None, elsewhere=()) -> FakeCatalogue:
    return _Credited(
        artists={LABEL_ID: FakePagedArtist(list(LISTED if listed is None else listed))},
        # A DEEP COPY, since a test that marks one track unplayable mutates it.
        releases=copy.deepcopy(RELEASES),
        confirmed=set(confirmed) - set(elsewhere),
        elsewhere=elsewhere,
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
    assert code == OK, done
    assert account.playlists == BUILT
    return SimpleNamespace(cfg=installed, fake=fake, account=account, monkeypatch=monkeypatch)


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    code, refused = drive(argv)
    assert code == ASKED, refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == OK, decided
    return drive(["--run", run_id, *argv])


def _prune(option: str = "apply") -> tuple[int, dict]:
    return _two_acts(["label", "prune", LABEL], PRUNE, option)


def _pruned() -> dict:
    code, done = _prune()
    assert code == OK, done
    return done


def _shown() -> dict:
    """The label prune's gate screen, with nothing approved."""
    code, refused = drive(["label", "prune", LABEL])
    assert code == ASKED, refused
    return refused["cause"]["detail"]["shown"]


def _recatalogue(built, **kwargs) -> None:
    built.monkeypatch.setattr(catalogue, "resolve", catalogue_factory(_catalogue(**kwargs)))


def _hold(cfg, *release_ids: str, genres=("Christian",)) -> None:
    with review.open_store(cfg) as store:
        for release_id in release_ids:
            payload = {"identity": release_id, "title": f"Release {release_id}"}
            review.hold(
                store, queue=Queue.LABEL_RELEASE, kind=sweep.KIND,
                identity={"release_id": release_id}, payload=payload, group=LABEL_ID, name=LABEL,
                reason="held", detail={"genres": list(genres), "kind": "dance"}, run_id="run-1",
            )


def _taken(envelope: dict, action: str = "take-off") -> list[tuple[str, str]]:
    items = envelope["data"]["items"]
    return [(item["playlist"], item["id"]) for item in items if item["action"] == action]


def _shape(cfg):
    return ledger.label_shape(cfg, LABEL_ID)


def _year(cfg, year: str = "2023"):
    return _shape(cfg).years[year]


# 1. The declaration


def test_both_prune_verbs_write_only_the_account_behind_an_explicit_gate():
    for name, gate, module, row in (("label.prune", PRUNE, "labels", 23), ("export.prune", EXPORT_PRUNE, "export", 36)):
        entry = registry.entry(name)
        assert entry.writes == frozenset({"remote"}), name
        assert entry.destructive is True, name
        assert entry.module_id == module and entry.feature_rows == (row,)
        (spec,) = entry.gates
        assert (spec.name, spec.options, spec.explicit) == (gate, ("apply", "abort"), True)
        assert spec.digest_source == "plan"
    # The protocol's removals: R-836's tracks, U123's playlist, U143's two root removals.
    removals = {name for name in outbound_fakes.PROTOCOL_METHODS if "remove" in name}
    assert removals == {"remove_tracks", "remove_playlist", "remove_root_playlist", "remove_legacy_folder"}
    # The client library still offers the removal the adapter makes.
    import tidalapi.playlist
    assert callable(getattr(tidalapi.playlist.UserPlaylist, "remove_by_indices", None))
    assert "remove_by_indices" in Path(tidal_account.__file__).read_text(encoding="utf-8")


# 2. A label's year playlists


def test_a_held_release_plans_exactly_its_tracks_and_approved_only_they_leave(built):
    _hold(built.cfg, "r3")
    done = _pruned()
    assert _taken(done) == [("pl-3", "t4"), ("pl-3", "t5")]
    assert built.account.playlists == {**BUILT, "pl-3": ["t6", "t7"]}
    year = _year(built.cfg)
    assert (year.pruned, year.added) == (frozenset({"t4", "t5"}), frozenset({"t6", "t7"}))
    assert done["data"]["totals"]["applied"]["taken"] == {"Kompakt 2023": ["t4", "t5"]}


def test_a_release_the_catalogue_no_longer_confirms_plans_its_tracks(built):
    """Credited to another label is the catalogue saying so; its tracks are read for it."""
    _recatalogue(built, elsewhere={"r2"})
    assert _taken(_pruned()) == [("pl-2", "t3")]
    assert (built.account.playlists["pl-2"], built.account.playlists["pl-1"]) == ([], ["t1", "t2"])


def test_a_release_merely_unconfirmed_is_not_evidence_and_its_tracks_stay(built):
    """No credit found is an absence. The track stays and the gate says why."""
    _recatalogue(built, confirmed=CONFIRMED - {"r2"})
    shown = _shown()
    assert shown["take off"].startswith("nothing")
    assert "1 recorded track(s) are on no release" in shown["not judged"][0]


def test_a_catalogue_read_as_empty_takes_nothing_off(built):
    """The R-135 shape, a first page served empty: absence is not evidence."""
    _recatalogue(built, listed=[])
    assert _pruned()["data"]["items"] == []
    assert built.account.taken == []


def test_a_release_the_provider_no_longer_has_stops_the_unconfirmed_judgement(built):
    """r7 is confirmed and gone, so any track could be its: only holds are judged."""
    _recatalogue(
        built,
        confirmed=CONFIRMED | {"r7"},
        listed=[*LISTED, FakeRelease("r7", year="2020")],
        elsewhere={"r2"},
    )
    _hold(built.cfg, "r1")
    shown = _shown()
    assert list(shown["take off"]) == ["Kompakt 2021"]
    assert "provider no longer has" in shown["not judged"][0]


def test_a_track_on_a_held_release_and_a_kept_one_of_the_same_year_stays(built):
    releases = built.fake.releases
    releases["r4"] = ([*releases["r4"][0], *releases["r3"][0][:1]], 2023)
    _hold(built.cfg, "r3")
    assert _taken(_pruned()) == [("pl-3", "t5")]
    assert built.account.playlists["pl-3"] == ["t4", "t6", "t7"]


def test_the_gate_lists_every_track_by_artist_and_title_per_playlist(built):
    built.account.names.update({"t4": ("Artist Four", "Four"), "t5": ("Artist Five", "Five")})
    _hold(built.cfg, "r3")
    assert _shown()["take off"] == {"Kompakt 2023": ["Artist Four - Four", "Artist Five - Five"]}
    assert built.account.taken == []


def test_an_empty_plan_still_asks_and_takes_nothing(built):
    # The build marked every year it created as created.
    created = {year: one.created for year, one in _shape(built.cfg).years.items()}
    assert created == dict.fromkeys(("2021", "2022", "2023"), True)
    done = _pruned()
    assert done["data"]["items"] == [] and done["data"]["totals"]["writes"] is False
    assert built.account.taken == []


def test_a_second_run_plans_nothing(built):
    _hold(built.cfg, "r3")
    _pruned()
    assert _taken(_pruned()) == []
    assert built.account.taken == [("pl-3", ("t4", "t5"))]


def test_a_refusal_part_way_resumes_without_taking_anything_off_twice(built):
    _hold(built.cfg, "r1", "r3")
    built.account.fail_on = frozenset({"pl-3"})
    built.account.transient = True
    code, refused = _prune()
    assert code != OK, refused
    assert "2 track(s) were taken off" in refused["cause"]["message"]
    assert built.account.playlists["pl-1"] == []
    assert built.account.playlists["pl-3"] == BUILT["pl-3"]
    built.account.fail_on = frozenset()
    assert _taken(_pruned()) == [("pl-3", "t4"), ("pl-3", "t5")]
    assert [playlist for playlist, _ids in built.account.taken].count("pl-1") == 1


def test_a_pruned_track_is_not_put_back_by_the_next_build(built):
    _hold(built.cfg, "r3")
    _pruned()
    code, done = _two_acts(["label", "playlists", LABEL], BUILD)
    assert code == OK, done
    assert built.account.playlists["pl-3"] == ["t6", "t7"]


def test_a_year_adopted_from_the_account_is_said_and_left_alone(installed, monkeypatch):
    register(LABEL)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(_catalogue()))
    account = outbound_fakes.StrictAccount()
    persons_playlist(account, LABEL, "Kompakt 2023", folder_id="folder-made", playlist_id="by-hand")
    bind_account(monkeypatch, account)
    assert _two_acts(["label", "playlists", LABEL], BUILD)[0] == OK
    assert _year(installed).created is False
    _hold(installed, "r3")
    (item,) = _pruned()["data"]["items"]
    assert (item["id"], item["action"], item["would"]) == ("by-hand", "left-alone", 2)
    assert account.taken == []
    assert account.playlists["by-hand"] == ["t4", "t5", "t6", "t7"]


def test_a_track_a_person_added_by_hand_is_never_planned(built):
    built.account.playlists["pl-3"].append("by-hand")
    _recatalogue(built, elsewhere={"r3"})
    assert _taken(_pruned()) == [("pl-3", "t4"), ("pl-3", "t5")]
    assert "by-hand" in built.account.playlists["pl-3"]


def _plan(kind: str, subject: str, key: str, name: str, remote_id: str, **step) -> prune.Plan:
    return prune.Plan(kind, subject, (prune.PlaylistPrune(key, name, remote_id, **step),))


def test_the_apply_asks_the_ledger_again_and_refuses_a_playlist_it_no_longer_vouches_for(installed):
    account = outbound_fakes.FakeAccount()
    account.playlists["elsewhere"] = ["t1"]
    taken = (prune.Taken("t1"),)
    planned = _plan(prune.EXPORTED, "crate", "crate", "Crate", "elsewhere", take=taken)
    with pytest.raises(CratekitError) as refused:
        prune.apply(installed, account, planned, prune.Pruned())
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert account.taken == []


# 3. An exported playlist


def _bound(monkeypatch, **catalog: str) -> outbound_fakes.FakeAccount:
    """A fake account matching rows 1 to 3 to tid-1 to tid-3, bound to the seam."""
    account = outbound_fakes.FakeAccount(catalog={str(i): f"tid-{i}" for i in (1, 2, 3)})
    account.catalog.update(catalog)
    bind_account(monkeypatch, account)
    return account


def _exported(cfg, account, written: str = "") -> None:
    """The crate's three tracks written to the account by the export engine."""
    planned = outbound_export.plan(
        [outbound_export.LocalTrack(identity=str(index)) for index in (1, 2, 3)],
        playlist_key=outbound_fakes.CRATE,
        name=outbound_fakes.CRATE,
        account=account,
        written=written,
    )
    outbound_export.apply(cfg, account, planned)
    assert account.playlists["pl-1"] == ["tid-1", "tid-2", "tid-3"]


def _written_before_rows(cfg, account) -> None:
    """The crate's three tracks recorded as a build before R-836 wrote them: no rows."""
    remote = ledger.reserve_playlist(
        cfg, outbound_fakes.CRATE, lambda: account.create_playlist(outbound_fakes.CRATE)
    ).remote_id
    for index in (1, 2, 3):
        account.add_to_playlist(remote, f"tid-{index}")
        ledger.record_playlist_track(cfg, outbound_fakes.CRATE, f"tid-{index}")


def _crate(cfg, *rows: int, under: str = "outbound", **kwargs) -> Path:
    return outbound_fakes.write_export(cfg.library.root / under, crate=rows, **kwargs)


def _export_prune(path) -> dict:
    code, done = _two_acts(["export", "prune", outbound_fakes.CRATE, "--export", str(path)], EXPORT_PRUNE)
    assert code == OK, done
    return done


def test_an_exported_playlist_whose_library_playlist_lost_a_track_plans_exactly_it(installed, monkeypatch):
    account = _bound(monkeypatch)
    _exported(installed, account)
    now = _crate(installed, 1, 2)
    assert _taken(_export_prune(now)) == [("pl-1", "tid-3")]
    assert account.playlists["pl-1"] == ["tid-1", "tid-2"]
    record = ledger.exported_playlist(installed, outbound_fakes.CRATE)
    assert (record.added, record.pruned) == (frozenset({"tid-1", "tid-2"}), frozenset({"tid-3"}))
    assert _taken(_export_prune(now)) == []
    assert account.taken == [("pl-1", ("tid-3",))]


def test_a_row_whose_match_failed_today_does_not_stop_a_track_recorded_by_its_row(installed, monkeypatch):
    account = _bound(monkeypatch)
    _exported(installed, account)
    del account.catalog["2"]
    assert _taken(_export_prune(_crate(installed, 1, 2))) == [("pl-1", "tid-3")]
    assert account.playlists["pl-1"] == ["tid-1", "tid-2"]


def test_an_unmatched_row_leaves_a_playlist_written_before_rows_alone(installed, monkeypatch):
    account = _bound(monkeypatch)
    _written_before_rows(installed, account)
    del account.catalog["2"]
    (item,) = _export_prune(_crate(installed, 1, 2))["data"]["items"]
    assert (item["action"], item["would"]) == ("left-alone", 2)
    assert account.taken == []


def test_a_match_that_moved_leaves_a_playlist_written_before_rows_alone(installed, monkeypatch):
    """Row 1 now matches a track never written, a drifted match: tid-1 is not gone."""
    account = _bound(monkeypatch, **{"1": "tid-9"})
    _written_before_rows(installed, account)
    (item,) = _export_prune(_crate(installed, 1, 2, 3))["data"]["items"]
    assert item["action"] == "left-alone" and "never written with" in item["why"]
    assert account.taken == []


def test_a_match_that_moved_never_takes_off_a_track_recorded_by_its_row(installed, monkeypatch):
    account = _bound(monkeypatch)
    _exported(installed, account)
    account.catalog["1"] = "tid-9"
    assert _export_prune(_crate(installed, 1, 2, 3))["data"]["items"] == []
    assert account.playlists["pl-1"] == ["tid-1", "tid-2", "tid-3"]


def test_a_playlist_written_before_rows_is_pruned_by_match_when_every_row_agrees(installed, monkeypatch):
    _written_before_rows(installed, _bound(monkeypatch))
    assert _taken(_export_prune(_crate(installed, 1, 2))) == [("pl-1", "tid-3")]


def test_a_playlist_never_exported_is_a_plan_of_nothing_still_gated(installed, monkeypatch):
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    path = outbound_fakes.write_export(installed.library.root / "outbound")
    assert _export_prune(path)["data"]["items"] == []
    assert account.matches == [] and account.taken == []


# 4. The ledger's answer


def test_product_made_says_yes_only_where_a_record_does(installed):
    ledger.reserve_label_year(installed, "lbl", "2021", "L 2021", lambda: "made")
    ledger.reserve_label_year(installed, "lbl", "2022", "L 2022", lambda: "never", adopt="adopted")
    ledger.reserve_set_playlist(installed, "A Set", "2026", lambda: "set-made")
    ledger.reserve_playlist(installed, "crate", lambda: "exported")
    for one, made in (("made", True), ("set-made", True), ("exported", True), ("adopted", False)):
        assert ledger.product_made(installed, one) is made, one
    assert ledger.product_made(installed, "nobody") is False
    assert ledger.product_made(installed, "") is False
    # A year recorded before this build, with no created field, is not product made.
    document = ledger._load(installed)
    del document["labels"]["lbl"]["years"]["2021"]["created"]
    ledger._write(installed, document)
    assert ledger.product_made(installed, "made") is False


def test_adopted_anywhere_wins_over_another_record_of_the_same_playlist(installed):
    ledger.reserve_label_year(installed, "lbl", "2022", "L 2022", lambda: "x", adopt="shared")
    ledger.reserve_set_playlist(installed, "A Set", "2026", lambda: "shared")
    assert ledger.product_made(installed, "shared") is False


# 5. The adapter's one removal, over a stand in for the client


class _Track:
    def __init__(self, track_id: str, at: str = "") -> None:
        self.id = track_id
        self.name = self.full_name = f"Title {track_id}"
        self.artists = [SimpleNamespace(name=f"Artist {track_id}")]
        self.user_date_added = datetime.fromisoformat(at) if at else None


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
        #: When each track was added, and the playlists that declare no count.
        self.added: dict[str, str] = {}
        self.undeclared: set[str] = set()


class _Playlist:
    def __init__(self, store: _Store, playlist_id: str) -> None:
        self.store = store
        self.id = playlist_id
        declared = len(store.members[playlist_id]) + store.hidden.get(playlist_id, 0)
        self.num_tracks = None if playlist_id in store.undeclared else declared
        self.num_videos = store.videos.get(playlist_id, 0)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[_Track]:
        size = 100 if limit is None else limit
        return [_Track(one, self.store.added.get(one, "")) for one in self.store.members[self.id][offset : offset + size]]

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


def _mine(cfg, *members: str, **store_state) -> _Store:
    """A store holding ``mine``, a playlist the product made, with these members."""
    store = _Store()
    _made(cfg, store, "mine", list(members))
    for name, value in store_state.items():
        setattr(store, name, value)
    return store


def _refused(cfg, store: _Store, playlist: str = "mine", ids=("b",)):
    with pytest.raises(CratekitError) as refused:
        _adapter(cfg, store).remove_tracks(playlist, ids)
    return refused.value.cause


def test_a_removal_from_a_playlist_the_product_did_not_create_is_refused_before_any_call(installed):
    store = _Store()
    store.members["theirs"] = ["a", "b"]
    cause = _refused(installed, store, "theirs", ("a",))
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "not-product-made"
    assert store.opened == [] and store.removals == []
    assert store.members["theirs"] == ["a", "b"]


def test_an_adapter_with_no_configuration_refuses_every_removal(installed):
    store = _mine(installed, "a")
    assert _refused(None, store, ids=("a",)).reason == "outbound-remove-refused"
    assert store.opened == []


def test_the_adapter_takes_off_every_occurrence_of_the_asked_tracks_and_nothing_else(installed):
    store = _mine(installed, "a", "b", "c", "b", "d")
    gone = _adapter(installed, store).remove_tracks("mine", ("b", "d", "never-there"))
    assert gone == ("b", "d", "never-there")
    assert store.members["mine"] == ["a", "c"]
    assert store.removals == [("mine", (1, 3, 4))]
    # The adapter names each track by artist and title.
    named = _adapter(installed, _mine(installed, "a", "b")).track_names("mine")
    assert named == {"a": ("Artist a", "Title a"), "b": ("Artist b", "Title b")}


def test_more_than_one_chunk_is_taken_off_one_request_at_a_time(installed):
    members = [f"t{index}" for index in range(tidal_account.REMOVE_CHUNK + 5)]
    store = _mine(installed, *members, "keep")
    assert _adapter(installed, store).remove_tracks("mine", tuple(members)) == tuple(members)
    assert store.members["mine"] == ["keep"]
    assert [len(asked) for _pid, asked in store.removals] == [tidal_account.REMOVE_CHUNK, 5]


def test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent(installed):
    store = _mine(installed, "a", "b", hidden={"mine": 1})
    assert _refused(installed, store).detail["problem"] == "positions-unknown"
    assert store.removals == []


def test_a_playlist_holding_a_video_is_refused_with_nothing_sent(installed):
    store = _mine(installed, "a", "b", videos={"mine": 1})
    assert _refused(installed, store).detail["problem"] == "positions-unknown"
    assert store.removals == []


def test_a_removal_the_provider_refuses_once_is_never_sent_again(installed):
    store = _mine(installed, "a", "b", fail=[RuntimeError("timed out")])
    _refused(installed, store)
    assert store.removals == [("mine", (1,))]
    # A removal answered false is a failure too, not a quiet return.
    _refused(installed, _mine(installed, "a", "b", answer=False))


def test_a_removal_that_took_the_wrong_position_is_read_back_and_refused(installed):
    store = _mine(installed, "a", "b", "c", wrong=[0])
    cause = _refused(installed, store)
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.retryable is False
    assert len(store.removals) == 1


def test_the_hold_reader_returns_the_held_release_identifiers(installed):
    from cratekit.label import prune_cli
    register(LABEL)
    entry = labels.RegistryStore().load().resolve(LABEL)
    _hold(installed, "r3", "r5")
    assert prune_cli.held_releases(installed, entry) == frozenset({"r3", "r5"})


# 6. What the review of the first round found


def test_a_track_already_off_the_playlist_is_settled_through_the_removals_own_read(built):
    """A removal landed before a failure is recorded as taken off once the adapter's read vouches."""
    _hold(built.cfg, "r3")
    built.account.playlists["pl-3"].remove("t4")
    done = _pruned()
    assert _taken(done) == [("pl-3", "t5")]
    assert _taken(done, "already-off") == [("pl-3", "t4")]
    assert built.account.taken == [("pl-3", ("t5", "t4"))]
    assert done["data"]["totals"]["applied"]["settled"] == {"Kompakt 2023": ["t4"]}
    assert _year(built.cfg).pruned == frozenset({"t4", "t5"})
    assert _prune()[1]["data"]["items"] == []


def test_a_track_on_the_playlist_twice_is_left_alone(built):
    _hold(built.cfg, "r3")
    built.account.playlists["pl-3"].append("t4")
    assert _taken(_pruned()) == [("pl-3", "t5")]
    assert built.account.playlists["pl-3"].count("t4") == 2


def test_a_hold_the_gate_would_now_release_takes_nothing_off(built):
    """Judged again from its own words, as the sweep judges a standing hold."""
    _hold(built.cfg, "r3", genres=("House",))
    assert _pruned()["data"]["items"] == []
    assert built.account.taken == []


def test_an_unplayable_track_on_a_kept_release_stays(built):
    built.fake.releases["r4"][0][0].available = False
    _hold(built.cfg, "r3")
    _pruned()
    assert "t6" in built.account.playlists["pl-3"]


def test_an_export_older_than_the_last_one_written_leaves_the_playlist_alone(installed, monkeypatch):
    account = _bound(monkeypatch)
    _exported(installed, account, written="2026-10-02T12:00:00+00:00")
    old = _crate(installed, 1, 2, under="older")
    stamp = 1_759_320_000  # 2025-10-01, a year before the recorded write
    os.utime(old, (stamp, stamp))
    (item,) = _export_prune(old)["data"]["items"]
    assert item["action"] == "left-alone" and "older" in item["why"]
    assert account.taken == []


def test_the_export_worker_records_the_date_of_the_export_it_read(installed, monkeypatch):
    from tests.cli_drive import approve_and_queue
    from tests.test_outbound_workers import _resume
    _bound(monkeypatch)
    path = outbound_fakes.write_export(installed.library.root / "outbound")
    _run, job_id = approve_and_queue(
        ["export", "playlist", outbound_fakes.CRATE, "--export", str(path)],
        "export.playlist.confirm",
    )
    assert _resume(job_id)[0] == OK
    written = ledger.exported_playlist(installed, outbound_fakes.CRATE).written
    assert written
    assert ledger.older_than("2000-01-01T00:00:00+00:00", written) is True
    assert ledger.older_than(written, written) is False
    assert ledger.older_than("", written) is True
    assert ledger.older_than("", "") is False


def test_a_later_export_date_moves_the_record_and_an_earlier_one_does_not(installed):
    def on(day: str) -> str:
        return f"2026-10-{day}T00:00:00+00:00"
    for day, kept in (("02", "02"), ("01", "02"), ("03", "03")):
        ledger.reserve_playlist(installed, "crate", lambda: "pl", written=on(day))
        assert ledger.exported_playlist(installed, "crate").written == on(kept)


# 7. What the review of the second round found


def test_a_settled_track_the_listing_hides_is_not_recorded_as_off(installed):
    """A track the listing hides and counts reads as off; the removal's read refuses, still added."""
    store = _Store()
    ledger.reserve_label_year(installed, "lbl", "2021", "L 2021", lambda: "mine")
    ledger.record_label_tracks(installed, "lbl", "2021", added=["shown", "hidden"])
    store.members["mine"] = ["shown"]
    store.hidden["mine"] = 1
    planned = _plan(prune.LABEL, "lbl", "2021", "L 2021", "mine", settle=("hidden",))
    with pytest.raises(CratekitError) as refused:
        prune.apply(installed, _adapter(installed, store), planned, prune.Pruned())
    assert refused.value.cause.detail["problem"] == "positions-unknown"
    year = ledger.label_shape(installed, "lbl").years["2021"]
    assert "hidden" in year.added and year.pruned == frozenset()


def test_an_account_that_does_not_vouch_for_every_asked_track_is_refused(installed):
    class Partial(outbound_fakes.FakeAccount):
        def remove_tracks(self, playlist_id, remote_ids):
            super().remove_tracks(playlist_id, remote_ids)
            return remote_ids[:1]
    account = Partial()
    ledger.reserve_set_playlist(installed, "A Set", "2026", lambda: "mine")
    ledger.reserve_playlist(installed, "crate", lambda: "mine")
    account.playlists["mine"] = ["a", "b"]
    taken = (prune.Taken("a"), prune.Taken("b"))
    planned = _plan(prune.EXPORTED, "crate", "crate", "Crate", "mine", take=taken)
    with pytest.raises(CratekitError) as refused:
        prune.apply(installed, account, planned, prune.Pruned())
    assert refused.value.cause.detail["unsaid"] == ["b"]


def test_the_export_date_goes_on_the_record_the_job_was_confirmed_to_update(installed):
    ledger.reserve_playlist(installed, "J", lambda: "Y")
    ledger.reserve_playlist(installed, "K", lambda: "X")
    ledger.reserve_playlist(installed, "K", lambda: "never", expected="Y", written="2026-10-03T00:00:00+00:00")
    assert ledger.exported_playlist(installed, "J").written == "2026-10-03T00:00:00+00:00"
    assert ledger.exported_playlist(installed, "K").written == ""


def test_a_year_recorded_before_the_field_is_said_as_such_not_as_adopted(built):
    document = ledger._load(built.cfg)
    del document["labels"][LABEL_ID]["years"]["2023"]["created"]
    ledger._write(built.cfg, document)
    _hold(built.cfg, "r3")
    (item,) = _pruned()["data"]["items"]
    assert item["action"] == "left-alone" and "predates" in item["why"]
    assert built.account.taken == []


def test_a_read_back_that_differed_is_not_told_to_run_again():
    def steps(problem: str) -> tuple[str, ...]:
        refused = refuse(
            "outbound-remove-refused", "refused", steps=("check by hand",), origin=("test",),
            detail={"problem": problem},
        )
        failed = prune.failed_part_way(refused, prune.Pruned(), origin=("test",), again="again")
        return failed.cause.remediation.steps
    assert "again" not in steps("read-back-differs")
    assert "again" in steps("positions-unknown")


def test_a_track_on_a_kept_release_of_another_year_is_not_said_unreached(built):
    built.fake.releases["r2"] = (built.fake.releases["r2"][0], 2024)
    assert "not judged" not in _shown()


def test_a_row_the_export_names_and_does_not_carry_keeps_its_track(installed, monkeypatch):
    """A dangling row is still a row of the playlist, so its track stays."""
    account = _bound(monkeypatch)
    _exported(installed, account)
    assert _taken(_export_prune(_crate(installed, 1, 2, 3, tracks=2))) == []
    assert account.playlists["pl-1"] == ["tid-1", "tid-2", "tid-3"]


def test_a_row_is_never_recorded_for_a_track_this_product_did_not_write(installed):
    ledger.reserve_playlist(installed, "crate", lambda: "pl")
    ledger.record_playlist_track(installed, "crate", "tid-1", identity="1")
    ledger.record_playlist_row(installed, "crate", "2", "by-hand")
    ledger.record_playlist_row(installed, "crate", "1", "tid-1")
    assert ledger.exported_playlist(installed, "crate").rows == {"1": "tid-1"}
