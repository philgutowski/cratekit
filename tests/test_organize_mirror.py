"""U147: the genre tree and the Favorites folder mirrored onto the account.

Driven at the organize step itself, :func:`account_mirror.add_steps`, over the
recording fake account with every call through the seam counted, and the
library handed in as values, so each scenario reads what the account holds
rather than the step's own report. Then the library side on a disposable
database, the ledger's record, and the intake sweep that must leave a mirror
alone. The verb level drive is in ``tests/test_organize.py``.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import ledger, mirror
from cratekit.organize import account_mirror
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, REFUSED, Area
from cratekit.sync import playlists
from tests import outbound_fakes
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

SOUL_BANDS = ("Favorites", "High", "Low", "Med", "Unsorted", "with vox")


def row(n: int, *, isrc: str | None = None) -> mirror.Row:
    """Library row ``c<n>``, matched by the fake to ``r<n>`` when the catalogue holds it."""
    return mirror.Row(
        content_id=f"c{n}",
        title=f"Title {n}",
        artist=f"Artist {n}",
        isrc=f"ISRC{n:05d}" if isrc is None else isrc,
    )


def folder(name: str, **playlists: tuple[int, ...]) -> mirror.Folder:
    """A rekordbox folder, each keyword one playlist's rows by number."""
    return mirror.Folder(
        name=name,
        playlists=tuple(
            mirror.Source(name=mirror.title(name, band), rows=tuple(row(n) for n in numbers))
            for band, numbers in playlists.items()
        ),
    )


def soul() -> mirror.Folder:
    return mirror.Folder(
        name="Soul",
        playlists=tuple(
            mirror.Source(name=mirror.title("Soul", band), rows=(row(10 + i), row(20 + i)))
            for i, band in enumerate(SOUL_BANDS)
        ),
    )


class World:
    """One fake account matching ``c<n>`` to ``r<n>``, and the library to mirror."""

    def __init__(self, cfg, monkeypatch, *, unmatched: tuple[int, ...] = ()) -> None:
        self.cfg = cfg
        self.account = outbound_fakes.StrictAccount(
            catalog={f"c{n}": f"r{n}" for n in range(1, 400) if n not in unmatched}
        )
        self.library = account_mirror.Library()
        monkeypatch.setattr(account_mirror, "read_library", lambda _cfg: self.library)

    def mirror(self, *folders: mirror.Folder, refused=None, favorites: str = "") -> None:
        self.library = account_mirror.Library(
            folders=folders, refused=dict(refused or {}), favorites=favorites
        )

    def plan(self) -> Area:
        area = Area(name="account")
        account_mirror.add_steps(self.cfg, area, lambda: self.account)
        return area

    def apply(self, area: Area) -> list[dict]:
        done = []
        for step in area.steps:
            if step.apply is not None:
                step.applied = step.apply()
                done.append(step.applied)
        return done

    def run(self) -> Area:
        area = self.plan()
        self.apply(area)
        return area

    def folder_id(self, name: str) -> str:
        (found,) = [fid for fid, title in self.account.folders().items() if title == name]
        return found

    def held(self, title: str) -> list[str]:
        """What the account playlist of this title holds, by title among the mirror's."""
        (found,) = [pid for pid, name in self.account.titles.items() if name == title]
        return list(self.account.playlists[found])

    def playlist_id(self, title: str) -> str:
        (found,) = [pid for pid, name in self.account.titles.items() if name == title]
        return found


def _steps(area: Area) -> dict[str, object]:
    return {step.key: step for step in area.steps}


def _writes(account: outbound_fakes.FakeAccount) -> tuple:
    """Every mutation the fake recorded, to compare before and after a run."""
    return (
        list(account.created),
        list(account.folders_created),
        list(account.moves),
        list(account.chunks),
        list(account.taken),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 1. A genre folder with no mirror
# ═══════════════════════════════════════════════════════════════════════════


def test_soul_with_six_playlists_and_no_mirror_plans_one_folder_and_six_playlists(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.mirror(soul())

    area = world.plan()
    step = _steps(area)["mirror:Soul"]

    assert step.state == PLANNED
    assert step.counts["create folder"] == 1 and step.counts["create playlist"] == 6
    assert [(item["playlist"], item["action"], item["add"]) for item in step.items[1:]] == [
        (f"Soul {band}", mirror.CREATE, 2) for band in SOUL_BANDS
    ]
    # Nothing written by the plan.
    assert _writes(world.account) == ([], [], [], [], [])

    (applied,) = world.apply(area)

    soul_id = world.folder_id("Soul")
    assert world.account.folders_created == ["Soul"]
    for i, band in enumerate(SOUL_BANDS):
        title = f"Soul {band}"
        assert world.held(title) == [f"r{10 + i}", f"r{20 + i}"]
        assert world.account.placed[world.playlist_id(title)] == soul_id
        assert world.playlist_id(title) in world.account.private
    # One folder, six creates, six moves and six adds: nineteen calls.
    assert applied["requests"] == 19, applied
    assert applied["added"] == 12 and applied["created"] == [f"Soul {band}" for band in SOUL_BANDS]
    assert "seconds" in applied
    # The plan read the root once and matched twelve rows: thirteen calls.
    assert area.facts[account_mirror.PLAN_FACT].startswith("13 account request(s) in ")


def test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any(installed, monkeypatch):
    """U207. ``read`` hands the account every code the plans will ask, once and
    before the first match, so the codes the catalogue files nothing under are
    screened in batches; a linked row is not handed over on the next run."""
    world = World(installed, monkeypatch)
    codes = {n: f"GBAAA24{n:05d}" for n in (1, 2, 3)}
    world.mirror(
        mirror.Folder(
            name="Soul",
            playlists=(
                mirror.Source(
                    name=mirror.title("Soul", "Low"),
                    rows=tuple(row(n, isrc=code) for n, code in codes.items()),
                ),
            ),
        )
    )

    world.run()

    assert world.account.screened == [tuple(codes.values())]
    assert [asked["isrc"] for asked in world.account.matches] == list(codes.values())

    world.plan()
    # Every row was linked by the first apply: nothing is screened again.
    assert world.account.screened == [tuple(codes.values())]


def test_a_second_run_plans_nothing_writes_nothing_and_asks_no_match_again(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(soul())
    world.run()
    before, matched = _writes(world.account), len(world.account.matches)

    area = world.plan()

    assert [step.state for step in area.steps] == [NOTHING]
    assert area.steps[0].apply is None and not area.writes
    assert _writes(world.account) == before
    # Every row was linked by the first apply, so the provider matches none again.
    assert len(world.account.matches) == matched


# ═══════════════════════════════════════════════════════════════════════════
# 2. A folder a person made, and two of them
# ═══════════════════════════════════════════════════════════════════════════


def test_a_root_folder_of_the_name_with_no_record_is_adopted_and_filled(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.account.folder_names["hand-1"] = "Techno"
    world.mirror(folder("Techno", Low=(1, 2)))

    area = world.run()

    assert _steps(area)["mirror:Techno"].items[0]["action"] == mirror.ADOPT
    assert world.account.folders_created == []
    assert world.account.placed[world.playlist_id("Techno Low")] == "hand-1"
    recorded = ledger.mirror_folders(installed)["Techno"]
    assert recorded.folder_id == "hand-1" and recorded.created is False


def test_two_root_folders_of_the_name_refuse_that_genre_and_the_rest_proceeds(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.account.folder_names["hand-1"] = "Techno"
    world.account.folder_names["hand-2"] = "Techno"
    world.mirror(folder("Techno", Low=(1,)), soul())

    area = world.run()
    steps = _steps(area)

    assert steps["mirror:Techno"].state == REFUSED
    assert steps["mirror:Techno"].cause.reason == "account-mirror-ambiguous"
    assert "2 root folders named 'Techno'" in steps["mirror:Techno"].detail
    assert steps["mirror:Soul"].state == PLANNED
    assert world.account.folders_created == ["Soul"]
    assert all(name.startswith("Soul ") for name in world.account.created)


def test_a_persons_playlist_of_the_same_title_is_left_and_nothing_made_beside_it(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.account.folder_names["hand-1"] = "Techno"
    world.account.titles["mine-1"] = "Techno Low"
    world.account.playlists["mine-1"] = ["r99"]
    world.account.placed["mine-1"] = "hand-1"
    world.mirror(folder("Techno", Low=(1,), High=(2,)))

    area = world.run()
    items = {item["playlist"]: item for item in _steps(area)["mirror:Techno"].items[1:]}

    assert items["Techno Low"]["action"] == mirror.LEFT and "did not make" in items["Techno Low"]["why"]
    assert world.account.created == ["Techno High"]
    assert world.account.playlists["mine-1"] == ["r99"] and world.account.taken == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. Removals: a moved track, a track added by hand
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.mirror(folder("Deep House", Med=(1, 2), High=(3,)))
    world.run()

    world.mirror(folder("Deep House", Med=(1,), High=(3, 2)))
    area = world.plan()
    items = {item["playlist"]: item for item in _steps(area)["mirror:Deep House"].items[1:]}
    assert (items["Deep House High"]["add"], items["Deep House High"]["remove"]) == (1, 0)
    assert (items["Deep House Med"]["add"], items["Deep House Med"]["remove"]) == (0, 1)
    world.apply(area)

    assert world.held("Deep House High") == ["r3", "r2"]
    assert world.held("Deep House Med") == ["r1"]
    # Added before it was taken off, so the track is never on neither.
    adds = [i for i, (pid, ids) in enumerate(world.account.chunks) if "r2" in ids]
    assert world.account.taken == [(world.playlist_id("Deep House Med"), ("r2",))]
    assert adds


def test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Deep House", Low=(1, 2)))
    world.run()
    low = world.playlist_id("Deep House Low")
    world.account.playlists[low].append("r77")
    world.account.names["r77"] = ("Someone", "Added On The Phone")

    area = world.plan()
    (item,) = _steps(area)["mirror:Deep House"].items[1:]
    assert item["removed"] == ["Someone - Added On The Phone (r77)"]
    world.apply(area)

    assert world.held("Deep House Low") == ["r1", "r2"]
    assert ledger.product_made(installed, low)


def test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Deep House", Low=(1, 2), High=(3,)))
    world.run()
    world.account.playlists[world.playlist_id("Deep House Low")].append("r77")

    def refused(_pid, _ids):
        raise refuse(
            "outbound-remove-refused", "positions unknown", scope=Scope.SOURCE, origin=("test",)
        )

    monkeypatch.setattr(world.account, "remove_tracks", refused)
    world.mirror(folder("Deep House", Low=(1, 2), High=(3, 4)))
    area = world.plan()
    (applied,) = world.apply(area)

    assert applied["kept"] == ["Deep House Low: positions unknown"]
    assert world.held("Deep House High") == ["r3", "r4"]
    assert [w["code"] for w in area.steps[0].warnings] == ["organize-mirror-kept"]


def test_a_removal_whose_read_back_differs_is_raised_never_kept(installed, monkeypatch):
    """Something may have come off that was not asked; the step fails and says so."""
    world = World(installed, monkeypatch)
    world.mirror(folder("Deep House", Low=(1, 2)))
    world.run()
    world.account.playlists[world.playlist_id("Deep House Low")].append("r77")

    def differs(_pid, _ids):
        raise refuse(
            "outbound-remove-refused",
            "the playlist read back is not what it held with the asked positions gone",
            scope=Scope.RUN,
            origin=("test",),
            detail={"problem": "read-back-differs"},
        )

    monkeypatch.setattr(world.account, "remove_tracks", differs)
    area = world.plan()

    with pytest.raises(CratekitError) as caught:
        world.apply(area)

    assert caught.value.cause.detail["problem"] == "read-back-differs"


def test_every_track_a_refresh_takes_off_is_named_on_the_gate(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Deep House", Low=(1, 2)))
    world.run()
    world.account.playlists[world.playlist_id("Deep House Low")].append("r77")
    world.account.names["r77"] = ("Someone", "Added On The Phone")

    area = world.plan()

    assert area.deletes == [
        "1 track(s) off the mirrored playlist 'Deep House Low': Someone - Added On The Phone (r77)"
    ]
    assert area.shown()["deletes"] == area.deletes


# ═══════════════════════════════════════════════════════════════════════════
# 4. Unmatched rows, retired folders, the Favorites folder
# ═══════════════════════════════════════════════════════════════════════════


def test_a_row_with_no_match_is_left_out_and_named_under_its_playlist(installed, monkeypatch):
    world = World(installed, monkeypatch, unmatched=(5,))
    world.account.reasons["c5"] = "the account has no track this row's ISRC names"
    nameless = mirror.Row(content_id="c6", title="Title 6", artist="Artist 6", isrc="")
    world.mirror(
        mirror.Folder(
            name="Techno",
            playlists=(mirror.Source(name="Techno High", rows=(row(4), row(5), nameless)),),
        )
    )
    monkeypatch.setattr(account_mirror, "identify", lambda _cfg: lambda one: mirror.Identity(isrc=one.isrc))

    area = world.run()
    (item,) = _steps(area)["mirror:Techno"].items[1:]

    assert item["unmatched"] == [
        "Artist 5 - Title 5: the account has no track this row's ISRC names",
        f"Artist 6 - Title 6: {mirror.NO_ISRC}",
    ]
    assert world.held("Techno High") == ["r4"]
    # A row with no code is never sent to the provider.
    assert [one["identity"] for one in world.account.matches] == ["c4", "c5"]


def test_a_folder_the_library_no_longer_holds_is_left_and_named(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Jazz", Low=(1,)), soul())
    world.run()

    world.mirror(soul())
    area = world.run()
    jazz = _steps(area)["mirror:Jazz"]

    assert jazz.state == LISTED and "left on the account" in jazz.detail
    assert world.held("Jazz Low") == ["r1"]
    assert world.account.taken == [] and world.account.deleted == []


def test_a_playlist_the_folder_no_longer_holds_is_left_and_named(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,), High=(2,)))
    world.run()

    world.mirror(folder("Techno", High=(2,)))
    area = world.run()
    step = _steps(area)["mirror:Techno"]

    assert step.state == NOTHING and step.counts["left"] == 1
    assert any(
        "Techno Low" in item.get("playlist", "") and item["action"] == mirror.LEFT
        for item in step.items
    )
    assert world.held("Techno Low") == ["r1"]


def test_the_favorites_folder_mirrors_under_its_own_names(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(
        mirror.Folder(
            name="Favorites",
            playlists=(
                mirror.Source(name="All Favorites", rows=(row(1), row(2))),
                mirror.Source(name=mirror.title("Favorites", "2026-10"), rows=(row(1),)),
                mirror.Source(name=mirror.title("Favorites", "Undated"), rows=(row(2),)),
            ),
        )
    )

    world.run()

    favorites = world.folder_id("Favorites")
    assert sorted(world.account.folder_playlists(favorites).values()) == [
        "All Favorites",
        "Favorites 2026-10",
        "Favorites Undated",
    ]


def test_a_favourites_playlist_at_the_root_is_listed_and_not_mirrored(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(soul(), favorites="the playlist 'All Favorites' sits at the playlist root")

    step = _steps(world.plan())["mirror:favorites"]

    assert step.state == LISTED and "sits at the playlist root" in step.detail


# ═══════════════════════════════════════════════════════════════════════════
# 5. Chunks, resume, an unread account
# ═══════════════════════════════════════════════════════════════════════════


def test_two_hundred_fifty_tracks_add_in_three_requests(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Peak=tuple(range(1, 251))))

    (applied,) = world.apply(world.plan())

    peak = world.playlist_id("Techno Peak")
    sizes = [len(ids) for pid, ids in world.account.chunks if pid == peak]
    assert sizes == [100, 100, 50]
    assert world.held("Techno Peak") == [f"r{n}" for n in range(1, 251)]
    # Create folder, create playlist, move, three adds.
    assert applied["requests"] == 6


def test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.mirror(soul())
    world.account.fail_on = frozenset({"Soul High"})

    area = world.plan()
    with pytest.raises(RuntimeError):
        world.apply(area)
    assert world.account.folders_created == ["Soul"]
    made_before = list(world.account.created)

    world.account.fail_on = frozenset()
    area = world.plan()
    assert _steps(area)["mirror:Soul"].items[0]["action"] == mirror.REUSE
    world.apply(area)

    assert world.account.folders_created == ["Soul"]
    assert sorted(world.account.created) == sorted(f"Soul {band}" for band in SOUL_BANDS)
    assert world.account.created[: len(made_before)] == made_before
    assert world.plan().steps[0].state == NOTHING


def test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    # The first playlist the fake makes is pl-1, and its move is the write that fails.
    world.account.fail_on = frozenset({"pl-1"})

    with pytest.raises(RuntimeError):
        world.apply(world.plan())
    low = world.playlist_id("Techno Low")
    assert low not in world.account.placed

    world.account.fail_on = frozenset()
    area = world.plan()
    (item,) = _steps(area)["mirror:Techno"].items[1:]
    assert item["action"] == mirror.REUSE and item["move"] is True
    world.apply(area)

    assert world.account.placed[low] == world.folder_id("Techno")
    assert world.account.created == ["Techno Low"]


def test_a_recorded_folder_deleted_on_the_account_is_made_again_rather_than_reused(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    world.run()
    gone = world.folder_id("Techno")
    del world.account.folder_names[gone]

    area = world.plan()
    head = _steps(area)["mirror:Techno"].items[0]
    world.apply(area)

    assert head["action"] == mirror.CREATE
    assert world.account.folders_created == ["Techno", "Techno"]
    assert ledger.mirror_folders(installed)["Techno"].folder_id == world.folder_id("Techno") != gone


def test_a_track_the_provider_refused_is_not_offered_again_so_a_refresh_plans_nothing(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.account.unaddable.add("r2")
    world.mirror(folder("Techno", Low=(1, 2)))
    (applied,) = world.apply(world.plan())
    assert applied["refused"] == 1 and world.held("Techno Low") == ["r1"]

    step = world.plan().steps[0]

    assert step.state == NOTHING
    assert step.items[1]["refused before"] == 1 and "add" in step.items[1]
    assert step.items[1]["add"] == 0


def test_an_account_that_cannot_be_resolved_refuses_the_kind_with_its_reason(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(soul())

    def unbound():
        raise refuse("outbound-ledger-unusable", "no account here", origin=("test",))

    area = Area(name="account")
    account_mirror.add_steps(installed, area, unbound)

    assert [(step.key, step.state) for step in area.steps] == [(account_mirror.MIRROR, REFUSED)]


def test_a_folder_whose_playlist_cannot_be_read_refuses_alone(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)), soul())
    world.run()
    real = world.account.track_names

    def unread(playlist_id):
        if playlist_id == world.playlist_id("Techno Low"):
            raise refuse("unavailable-transient", "the read timed out", origin=("test",))
        return real(playlist_id)

    monkeypatch.setattr(world.account, "track_names", unread)
    steps = _steps(world.plan())

    assert steps["mirror:Techno"].state == REFUSED
    assert steps["mirror:Soul"].state == NOTHING


def test_a_library_name_two_folders_take_is_refused_by_name(installed, monkeypatch):
    world = World(installed, monkeypatch)
    cause = account_mirror._twice("Soul", "folders")
    world.mirror(folder("Techno", Low=(1,)), refused={"Soul": cause})

    steps = _steps(world.plan())

    assert steps["mirror:Soul"].state == REFUSED and "two of folders" in steps["mirror:Soul"].detail
    assert steps["mirror:Techno"].state == PLANNED


# ═══════════════════════════════════════════════════════════════════════════
# 6. The links, the digest, the ledger, the sweep
# ═══════════════════════════════════════════════════════════════════════════


def test_a_row_whose_database_code_changed_is_matched_again(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    world.run()
    asked = len(world.account.matches)

    world.mirror(
        mirror.Folder(
            name="Techno",
            playlists=(mirror.Source(name="Techno Low", rows=(row(1, isrc="NEWCODE0001"),)),),
        )
    )
    world.plan()

    assert len(world.account.matches) == asked + 1
    assert world.account.matches[-1]["isrc"] == "NEWCODE0001"


def test_a_code_read_off_the_file_asks_the_one_track_to_agree_and_a_database_code_does_not(
    installed, monkeypatch
):
    from cratekit.sync import pair_cli

    world = World(installed, monkeypatch)
    monkeypatch.setattr(pair_cli, "file_identity", lambda _cfg, _path: ("FILECODE001", "An Album"))
    tagged_only = mirror.Row(content_id="c2", title="Title 2", artist="Artist 2", isrc="", path="x")
    world.mirror(
        mirror.Folder(
            name="Techno",
            playlists=(mirror.Source(name="Techno Low", rows=(row(1), tagged_only)),),
        )
    )

    world.plan()

    assert world.account.agreeing == ["c2"]
    asked = {one["identity"]: one for one in world.account.matches}
    assert asked["c2"]["isrc"] == "FILECODE001" and asked["c2"]["album"] == "An Album"
    assert asked["c1"]["isrc"] == "ISRC00001"


def test_a_persons_playlist_left_alone_costs_no_match(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.account.folder_names["hand-1"] = "Techno"
    world.account.titles["mine-1"] = "Techno Low"
    world.account.playlists["mine-1"] = []
    world.account.placed["mine-1"] = "hand-1"
    world.mirror(folder("Techno", Low=(1, 2)))

    world.plan()

    assert world.account.matches == []


def test_rows_a_folder_with_nothing_to_write_matched_are_linked_by_another_folders_apply(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    world.run()
    # The Techno rows' links are lost, so its plan matches them again and has
    # nothing to write, and the new Soul folder's apply records them anyway.
    path = config.state_path("outbound_writes", installed)
    document = json.loads(path.read_text())
    document["mirror_links"] = {}
    path.write_text(json.dumps(document))
    world.mirror(folder("Techno", Low=(1,)), folder("Soul", Low=(2,)))

    area = world.run()

    assert _steps(area)["mirror:Techno"].state == NOTHING
    assert set(ledger.mirror_links(installed)) == {"c1", "c2"}


def test_a_library_name_two_folders_take_names_its_remedy_in_rekordbox(installed, monkeypatch):
    cause = account_mirror._twice("Soul", "folders")

    assert cause.reason == mirror.AMBIGUOUS_REASON
    assert any("in rekordbox" in step for step in cause.remediation.steps)


def test_sync_pair_refuses_to_pair_a_mirrored_playlist():
    from types import SimpleNamespace

    from cratekit.sync import pair_cli

    listed = {"pl-1": SimpleNamespace(name="Deep House Low")}

    with pytest.raises(CratekitError) as caught:
        pair_cli._scope_account("pl-1", listed, frozenset(), frozenset(), frozenset({"pl-1"}))

    assert caught.value.cause.reason == "sync-pair-out-of-scope"
    assert "mirrored" in caught.value.cause.message
    assert pair_cli._scope_account("pl-1", listed, frozenset(), frozenset()) == "Deep House Low"


def test_the_digest_moves_when_a_write_changes_and_not_when_only_the_timing_does(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1, 2)))
    first = world.plan().steps[0].digest
    again = world.plan().steps[0].digest
    world.mirror(folder("Techno", Low=(1, 3)))
    other = world.plan().steps[0].digest

    assert first == again and first != other


def test_a_malformed_mirror_record_refuses_rather_than_reading_as_none(installed):
    path = config.state_path("outbound_writes", installed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 1, "mirrors": {"Soul": "not a record"}}))

    with pytest.raises(CratekitError) as caught:
        ledger.mirror_folders(installed)

    assert caught.value.cause.reason == "outbound-ledger-unusable"


def test_a_write_elsewhere_in_the_ledger_carries_the_mirror_record_through(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    world.run()
    held = ledger.mirror_folders(installed)

    ledger.reserve_kind_folder(installed, "Mine", lambda: "mine-folder")

    assert ledger.mirror_folders(installed) == held
    assert ledger.mirror_links(installed) == {"c1": ("r1", "ISRC00001")}


def test_the_intake_sweep_leaves_a_mirrored_playlist_alone():
    mirrored = AccountPlaylist("pl-1", "Deep House Low", 12)

    reason = playlists.exclusion(mirrored, recorded=set(), in_flight=set(), mirrored={"pl-1"})

    assert reason == playlists.Excluded.MIRROR
    assert playlists.exclusion(mirrored, recorded=set(), in_flight=set()) is None


def test_the_sync_pass_hands_the_sweep_every_mirrored_playlist(installed, monkeypatch):
    from types import SimpleNamespace

    from cratekit.label import catalogue
    from cratekit.sync import cli as sync_cli

    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,), High=(2,)))
    world.run()
    handed: list[frozenset[str]] = []

    class Stop(Exception):
        pass

    def plan(store, cfg_, found, *, handler_key, mirrored=frozenset(), **_others):
        handed.append(mirrored)
        raise Stop

    monkeypatch.setattr(catalogue, "resolve", lambda _cfg: object())
    monkeypatch.setattr(playlists, "plan", plan)
    with pytest.raises(Stop):
        sync_cli._plan_playlists(SimpleNamespace(handler_key="intake.playlist"), None)

    assert handed == [{world.playlist_id("Techno Low"), world.playlist_id("Techno High")}]
