"""U143: organize keeps the account root to working custom playlists.

Driven at the root step's own plan and apply over the recording fake account,
with the filing plan it reads its candidates from, so each scenario reads what
the account holds rather than the step's own report. Then the adapter's two
root removals, over a stand in for the provider client, each refusal asserted
with no removal sent. The verb level drive is in ``tests/test_organize.py``.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

from cratekit.core.cause import CratekitError
from cratekit.favorites import placeholders
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import kinds, ledger, tidal_account
from cratekit.organize import filing, root
from cratekit.sync import mark_record
from tests import outbound_fakes
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

LABEL = "Colorize"
LABEL_ID = "label-colorize"
DEBRIS = f"{LABEL} LIBRARY"
YEAR = "2026"
LEGACY = f"{YEAR} Custom Playlists"
CATALOGUE = tuple(f"t{n}" for n in range(1, 6))


class World:
    """One fake account, the listing the catalogue would report, and its folders."""

    def __init__(self) -> None:
        self.account = outbound_fakes.StrictAccount()
        self.listed: list[AccountPlaylist] = []

    def folder(self, name: str) -> str:
        """A root folder already on the account, made by hand rather than by a step."""
        folder_id = f"hand-{len(self.account.folder_names) + 1}"
        self.account.folder_names[folder_id] = name
        return folder_id

    def playlist(
        self,
        playlist_id: str,
        name: str,
        tracks=(),
        *,
        folder: str = "",
        declared: int | None = -1,
    ) -> str:
        self.account.titles[playlist_id] = name
        self.account.playlists[playlist_id] = list(tracks)
        if folder:
            self.account.placed[playlist_id] = folder
        count = len(tracks) if declared == -1 else declared
        self.listed.append(AccountPlaylist(playlist_id, name, count))
        return playlist_id

    def label_folder(self, tracks=CATALOGUE) -> str:
        folder_id = self.folder(LABEL)
        self.playlist("year-1", f"DOWNLOADED {LABEL} {YEAR}", tracks, folder=folder_id)
        return folder_id

    def plans(self, cfg, *, followed=((LABEL_ID, LABEL),)) -> tuple[filing.FilePlan, root.RootPlan]:
        filed = filing.plan(
            cfg,
            listed=self.listed,
            remote=self.account,
            labels=tuple(name for _id, name in followed),
            marks=mark_record.MarkRecord(cfg).all(),
            working=placeholders.is_placeholder,
        )
        return filed, root.plan(
            cfg, listed=self.listed, remote=self.account, filed=filed, followed=followed
        )

    def kept(self, cfg) -> root.RootPlan:
        return self.plans(cfg)[1]

    def forget_removed(self) -> None:
        """The catalogue's next listing, without what the account no longer holds."""
        self.listed = [one for one in self.listed if one.playlist_id in self.account.titles]


def _rows(planned: root.RootPlan) -> dict[str, root.RootRow]:
    return {row.target: row for row in planned.rows}


# ═══════════════════════════════════════════════════════════════════════════
# 1. Label debris
# ═══════════════════════════════════════════════════════════════════════════


def test_four_identical_debris_copies_with_every_track_filed_plan_four_removals(installed):
    world = World()
    folder = world.label_folder()
    for n in range(1, 5):
        world.playlist(f"debris-{n}", DEBRIS, CATALOGUE[:3])

    filed, planned = world.plans(installed)

    assert {row.playlist_id: row.why for row in filed.rows if row.why == filing.DEBRIS} == {
        f"debris-{n}": filing.DEBRIS for n in range(1, 5)
    }
    assert [(row.target, row.kind, row.action, row.why) for row in planned.rows] == [
        (f"debris-{n}", kinds.DEBRIS, root.REMOVE, root.EVERY_TRACK_FILED) for n in range(1, 5)
    ]
    done = root.apply(installed, world.account, planned)
    assert world.account.root_removed == [(f"debris-{n}", kinds.DEBRIS) for n in range(1, 5)]
    assert done.totals()["removed"] == [[kinds.DEBRIS, f"debris-{n}", DEBRIS] for n in range(1, 5)]
    # The label folder and its year playlist are read, never written.
    assert world.account.placed["year-1"] == folder
    assert world.account.playlists["year-1"] == list(CATALOGUE)


def test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it(installed):
    world = World()
    world.label_folder(CATALOGUE[:3])
    world.playlist("debris-1", DEBRIS, ("t1", "t9"))
    world.account.names["t9"] = ("Some Artist", "Lost Track")

    row = _rows(world.kept(installed))["debris-1"]

    assert row.action == root.LEFT
    assert "1 of its tracks" in row.why and "Some Artist - Lost Track" in row.why
    root.apply(installed, world.account, world.kept(installed))
    assert world.account.root_removed == []


def test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left(installed):
    world = World()
    world.label_folder()
    # Declared four, three read: the provider leaves out a track it cannot play.
    world.playlist("debris-1", DEBRIS, CATALOGUE[:3], declared=4)

    row = _rows(world.kept(installed))["debris-1"]

    assert row.action == root.LEFT and "3 of its 4 track(s) could be read" in row.why


def test_debris_with_no_label_folder_or_two_of_them_is_left_with_why(installed):
    world = World()
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])
    assert "no root folder is named" in _rows(world.kept(installed))["debris-1"].why

    world.folder(LABEL)
    world.folder(LABEL)
    assert "2 root folders named" in _rows(world.kept(installed))["debris-1"].why


def test_a_label_folder_with_no_downloaded_playlist_proves_nothing(installed):
    world = World()
    folder = world.folder(LABEL)
    world.playlist("year-1", f"{LABEL} {YEAR}", CATALOGUE, folder=folder)
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])

    row = _rows(world.kept(installed))["debris-1"]

    assert row.action == root.LEFT and "no DOWNLOADED playlist" in row.why


def test_a_followed_labels_recorded_folder_is_read_whatever_it_is_called_now(installed):
    world = World()
    folder = world.label_folder()
    world.account.folder_names[folder] = f"{LABEL} (kept)"
    ledger.reserve_label_folder(installed, LABEL_ID, LABEL, lambda: "unused", adopt=folder)
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])

    row = _rows(world.kept(installed))["debris-1"]

    assert (row.action, row.folder) == (root.REMOVE, folder)


def test_a_debris_playlist_a_ledger_claims_is_not_the_root_steps(installed):
    world = World()
    world.label_folder()
    ledger.reserve_playlist(installed, "crate-x", lambda: "debris-1")
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])

    assert "debris-1" not in _rows(world.kept(installed))


# ═══════════════════════════════════════════════════════════════════════════
# 2. Working custom playlists, empties, and what is never touched
# ═══════════════════════════════════════════════════════════════════════════


def test_a_working_custom_playlist_is_left_and_nothing_is_planned_for_it(installed):
    world = World()
    world.playlist("custom-1", "tech_house_hits - Phil", CATALOGUE)

    filed, planned = world.plans(installed)

    (row,) = filed.rows
    assert (row.action, row.why) == (filing.LEFT, filing.WORKING_CUSTOM)
    assert planned.rows == () and not planned.writes and not filed.writes


def test_an_empty_root_playlist_plans_a_removal(installed):
    world = World()
    world.playlist("empty-1", "Untitled Playlist", ())

    filed, planned = world.plans(installed)

    assert {row.playlist_id: row.why for row in filed.rows} == {"empty-1": filing.EMPTY}
    assert [(row.target, row.kind, row.action) for row in planned.rows] == [
        ("empty-1", kinds.EMPTY, root.REMOVE)
    ]
    root.apply(installed, world.account, planned)
    assert world.account.root_removed == [("empty-1", kinds.EMPTY)]


def test_a_playlist_whose_count_the_listing_did_not_give_is_not_empty(installed):
    world = World()
    world.playlist("unknown-1", "Untitled Playlist", (), declared=None)

    filed, planned = world.plans(installed)

    assert filed.rows[0].why == filing.WORKING_CUSTOM and planned.rows == ()


def test_an_empty_debris_copy_is_removed_as_empty(installed):
    world = World()
    world.playlist("debris-1", DEBRIS, ())

    assert _rows(world.kept(installed))["debris-1"].kind == kinds.EMPTY


def test_an_empty_playlist_the_product_made_or_a_placeholder_is_never_removed(installed):
    world = World()
    ledger.reserve_playlist(installed, "crate-x", lambda: "made-1")
    world.playlist("made-1", "Exported, nothing yet", ())
    world.playlist("held-1", placeholders.placeholder_name("2026-Q4"), ())
    assert placeholders.is_placeholder(world.account.titles["held-1"])

    filed, planned = world.plans(installed)

    assert planned.rows == ()
    assert {row.playlist_id for row in filed.rows if row.why == filing.EMPTY} == set()


def test_folders_a_person_made_never_appear_and_nothing_in_them_is_read_for_removal(installed):
    world = World()
    spotify = world.folder("Phil's Spotify")
    trivia = world.folder("Genre Trivia!")
    mine = world.folder(kinds.MINE)
    world.playlist("in-spotify", "Old list", (), folder=spotify)
    world.playlist("in-trivia", f"Trivia {LABEL} LIBRARY", ("t1",), folder=trivia)
    world.playlist("in-mine", "Untitled Playlist", (), folder=mine)

    filed, planned = world.plans(installed)

    shown = str(planned.items()) + str(filed.items())
    assert "Phil's Spotify" not in shown and "Genre Trivia!" not in shown
    assert planned.rows == () and filed.rows == ()


# ═══════════════════════════════════════════════════════════════════════════
# 3. The legacy year folder
# ═══════════════════════════════════════════════════════════════════════════


def test_a_legacy_year_folder_is_emptied_into_its_year_then_removed_on_a_later_run(installed):
    world = World()
    year = world.folder(YEAR)
    legacy = world.folder(LEGACY)
    for n in range(1, 4):
        world.playlist(f"old-{n}", f"Custom {n}", ("t1",), folder=legacy)

    first = world.kept(installed)

    assert [(row.target, row.action) for row in first.moves] == [
        (f"old-{n}", root.MOVE) for n in range(1, 4)
    ]
    assert first.removals == ()
    (stays,) = [row for row in first.rows if row.what == root.FOLDER]
    assert (stays.target, stays.action) == (legacy, root.LEFT)
    assert first.years[YEAR].folder_id == year
    done = root.apply(installed, world.account, first)
    assert done.totals()["moved"] == [[f"old-{n}", year] for n in range(1, 4)]
    # Never removed by the apply that emptied it.
    assert legacy in world.account.folder_names and world.account.folders_removed == []

    second = world.kept(installed)

    assert [(row.target, row.what, row.action) for row in second.rows] == [
        (legacy, root.FOLDER, root.REMOVE)
    ]
    root.apply(installed, world.account, second)
    assert world.account.folders_removed == [legacy]
    assert world.kept(installed).rows == ()


def test_a_legacy_folder_holding_a_folder_stays_and_its_folder_is_not_moved(installed):
    world = World()
    legacy = world.folder(LEGACY)
    world.account.nest_folder("Deeper", legacy)

    planned = world.kept(installed)

    (row,) = planned.rows
    assert (row.target, row.action) == (legacy, root.LEFT) and "never moves a folder" in row.why
    assert not planned.writes


def test_a_legacy_year_with_two_year_folders_leaves_its_playlists(installed):
    world = World()
    world.folder(YEAR)
    world.folder(YEAR)
    legacy = world.folder(LEGACY)
    world.playlist("old-1", "Custom 1", ("t1",), folder=legacy)

    row = _rows(world.kept(installed))["old-1"]

    assert row.action == root.LEFT and "2 root folders" in row.why


@pytest.mark.parametrize(
    ("name", "year"),
    [
        (LEGACY, YEAR),
        ("1999 Custom Playlists", "1999"),
        ("2026 custom playlists", ""),
        ("My 2026 Custom Playlists", ""),
        ("2026 Custom Playlists 2", ""),
        (YEAR, ""),
    ],
)
def test_only_a_year_and_these_exact_words_name_a_legacy_folder(name, year):
    assert kinds.legacy_year(name) == year


# ═══════════════════════════════════════════════════════════════════════════
# 4. The whole root, twice, and a refusal part way
# ═══════════════════════════════════════════════════════════════════════════


def _messy(world: World) -> None:
    world.label_folder()
    world.folder(YEAR)
    legacy = world.folder(LEGACY)
    world.playlist("old-1", "Custom 1", ("t1",), folder=legacy)
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])
    world.playlist("debris-2", DEBRIS, CATALOGUE[:2])
    world.playlist("empty-1", "Untitled Playlist", ())
    world.playlist("custom-1", "tech_house_hits - Phil", CATALOGUE)


def test_a_second_run_on_a_clean_root_plans_nothing(installed):
    world = World()
    _messy(world)
    root.apply(installed, world.account, world.kept(installed))
    world.forget_removed()
    root.apply(installed, world.account, world.kept(installed))
    world.forget_removed()

    filed, planned = world.plans(installed)

    assert planned.rows == () and not planned.writes
    assert [(row.playlist_id, row.why) for row in filed.rows] == [
        ("custom-1", filing.WORKING_CUSTOM)
    ]


def test_a_refusal_part_way_stops_and_names_what_was_removed(installed):
    world = World()
    _messy(world)
    world.account.fail_on = frozenset({"debris-2"})
    world.account.provider_error = True

    with pytest.raises(CratekitError) as raised:
        root.apply(installed, world.account, world.kept(installed))

    message = raised.value.cause.message
    assert "1 removed (the debris 'Colorize LIBRARY')" in message
    assert raised.value.cause.detail["removed"] == [[kinds.DEBRIS, "debris-1", DEBRIS]]
    assert "empty-1" in world.account.titles


def test_the_plans_digest_moves_when_a_row_changes(installed):
    world = World()
    _messy(world)
    before = world.kept(installed).identity()
    world.account.playlists["debris-1"].append("t9")
    world.listed = [
        AccountPlaylist(one.playlist_id, one.name, 3) if one.playlist_id == "debris-1" else one
        for one in world.listed
    ]

    assert world.kept(installed).identity() != before


# ═══════════════════════════════════════════════════════════════════════════
# 5. The adapter's root removals, over a stand in for the client
# ═══════════════════════════════════════════════════════════════════════════


class ObjectNotFound(Exception):
    """Named as the client's own not found, which the adapter reads by name."""


class _Served:
    def __init__(self, client: _Client, playlist_id: str) -> None:
        self.client = client
        self.id = playlist_id
        self.name, self.num_tracks, self.num_videos = client.held[playlist_id]

    def delete(self) -> bool:
        self.client.deletes.append(self.id)
        if self.client.answer and not self.client.stays:
            self.client.held.pop(self.id, None)
        return self.client.answer


class _Favourites:
    def __init__(self, client: _Client) -> None:
        self.client = client

    def remove_folders_playlists(self, trns, type="folder"):  # noqa: A002 - the client's name
        self.client.folder_calls.append((list(trns), type))
        if self.client.answer and not self.client.stays:
            for one in trns:
                self.client.root.pop(one, None)
        return self.client.answer


class _User:
    def __init__(self, client: _Client) -> None:
        self.favorites = _Favourites(client)


class _Client:
    def __init__(self, held=None, root_folders=None, *, answer=True, stays=False) -> None:
        self.held = dict(held or {})
        self.root = dict(root_folders or {})
        self.inside: dict[str, int] = {}
        self.answer = answer
        self.stays = stays
        self.deletes: list[str] = []
        self.folder_calls: list[tuple[list[str], str]] = []
        self.opened: list[str] = []
        self.user = _User(self)

    def playlist(self, playlist_id: str) -> _Served:
        self.opened.append(playlist_id)
        if playlist_id not in self.held:
            raise ObjectNotFound(playlist_id)
        return _Served(self, playlist_id)


def _adapter(client: _Client, cfg) -> tidal_account.TidalAccount:
    adapter = tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=cfg)
    # THE FOLDER READS ARE THE ADAPTER'S OWN PAGED WALKS, read here off the
    # stand in so the removal member is what is driven.
    adapter.folders = lambda: dict(client.root)
    adapter.folder_playlists = lambda folder_id: {
        f"p{n}": "x" for n in range(client.inside.get(folder_id, 0))
    }
    adapter.folder_folders = lambda folder_id: {}
    return adapter


def test_the_adapter_removes_a_debris_playlist_and_reads_it_back_gone(installed):
    client = _Client({"pl-1": (DEBRIS, 3, 0)})

    _adapter(client, installed).remove_root_playlist("pl-1", kinds.DEBRIS)

    assert client.deletes == ["pl-1"] and client.opened == ["pl-1", "pl-1"]


def test_the_adapter_removes_an_empty_playlist(installed):
    client = _Client({"pl-1": ("Untitled Playlist", 0, 0)})

    _adapter(client, installed).remove_root_playlist("pl-1", kinds.EMPTY)

    assert client.deletes == ["pl-1"]


@pytest.mark.parametrize(
    ("served", "kind"),
    [
        (("Colorize Library", 3, 0), kinds.DEBRIS),
        (("A person's list", 3, 0), kinds.DEBRIS),
        (("Untitled Playlist", 1, 0), kinds.EMPTY),
        (("Untitled Playlist", 0, 1), kinds.EMPTY),
        (("Untitled Playlist", 0, None), kinds.EMPTY),
        (("Untitled Playlist", None, 0), kinds.EMPTY),
    ],
)
def test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete(
    installed, served, kind
):
    client = _Client({"pl-1": served})

    with pytest.raises(CratekitError) as caught:
        _adapter(client, installed).remove_root_playlist("pl-1", kind)

    assert caught.value.cause.detail["problem"] == "not-this-kind"
    assert client.deletes == []


def test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call(installed):
    ledger.reserve_set_playlist(installed, "A set", YEAR, lambda: "pl-1")
    client = _Client({"pl-1": (DEBRIS, 0, 0), "pl-2": (DEBRIS, 0, 0)})
    adapter = _adapter(client, installed)

    with pytest.raises(CratekitError) as claimed:
        adapter.remove_root_playlist("pl-1", kinds.EMPTY)
    with pytest.raises(CratekitError) as other:
        adapter.remove_root_playlist("pl-2", "old")
    with pytest.raises(CratekitError) as unnamed:
        _adapter(client, None).remove_root_playlist("pl-2", kinds.EMPTY)

    assert claimed.value.cause.detail["problem"] == "ledger-claimed"
    assert other.value.cause.detail["problem"] == "not-a-root-kind"
    assert unnamed.value.cause.detail["problem"] == "ledger-claimed"
    assert client.opened == [] and client.deletes == []


def test_a_root_playlist_still_served_after_its_delete_is_refused_not_reported_removed(installed):
    client = _Client({"pl-1": (DEBRIS, 3, 0)}, stays=True)

    with pytest.raises(CratekitError) as caught:
        _adapter(client, installed).remove_root_playlist("pl-1", kinds.DEBRIS)

    assert caught.value.cause.detail["problem"] == "read-back-differs"


def test_a_root_playlist_already_gone_is_removed_with_no_delete(installed):
    client = _Client({})

    _adapter(client, installed).remove_root_playlist("pl-1", kinds.EMPTY)

    assert client.deletes == []


def test_the_generic_removal_still_refuses_an_unrecorded_playlist(installed):
    client = _Client({"pl-1": (DEBRIS, 3, 0)})

    with pytest.raises(CratekitError) as caught:
        _adapter(client, installed).remove_playlist("pl-1")

    assert caught.value.cause.reason == "outbound-remove-refused"
    assert client.opened == [] and client.deletes == []


def test_the_adapter_removes_an_empty_legacy_folder_and_reads_the_root_again(installed):
    client = _Client(root_folders={"f-1": LEGACY, "f-2": YEAR})

    _adapter(client, installed).remove_legacy_folder("f-1")

    assert client.folder_calls == [(["f-1"], "folder")]
    assert client.root == {"f-2": YEAR}


@pytest.mark.parametrize(
    ("name", "inside", "problem"),
    [
        (YEAR, 0, "not-a-legacy-folder"),
        ("Phil's Spotify", 0, "not-a-legacy-folder"),
        (LEGACY, 2, "not-empty"),
    ],
)
def test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal(
    installed, name, inside, problem
):
    client = _Client(root_folders={"f-1": name})
    client.inside["f-1"] = inside

    with pytest.raises(CratekitError) as caught:
        _adapter(client, installed).remove_legacy_folder("f-1")

    assert caught.value.cause.detail["problem"] == problem
    assert client.folder_calls == []


def test_a_legacy_folder_still_listed_after_its_removal_is_refused(installed):
    client = _Client(root_folders={"f-1": LEGACY}, stays=True)

    with pytest.raises(CratekitError) as caught:
        _adapter(client, installed).remove_legacy_folder("f-1")

    assert caught.value.cause.detail["problem"] == "read-back-differs"


def test_a_legacy_folder_the_root_no_longer_lists_is_already_removed(installed):
    client = _Client(root_folders={})

    _adapter(client, installed).remove_legacy_folder("f-1")

    assert client.folder_calls == []


def test_a_folder_removal_the_client_answers_false_is_a_failure(installed):
    client = _Client(root_folders={"f-1": LEGACY}, answer=False)

    with pytest.raises(CratekitError):
        _adapter(client, installed).remove_legacy_folder("f-1")

    assert client.folder_calls == [(["f-1"], "folder")] and "f-1" in client.root


# ═══════════════════════════════════════════════════════════════════════════
# 6. The review round's findings, each driven
# ═══════════════════════════════════════════════════════════════════════════


def test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed(installed):
    world = World()
    world.label_folder()
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])
    world.playlist("empty-1", "Untitled Playlist", ())
    planned = world.kept(installed)
    world.account.playlists["debris-1"].append("t9")

    done = root.apply(installed, world.account, planned)

    assert world.account.root_removed == [("empty-1", kinds.EMPTY)]
    assert done.kept == [
        [kinds.DEBRIS, "debris-1", DEBRIS, "it holds a track it did not hold when the gate was answered"]
    ]


def test_a_playlist_moved_into_a_folder_since_the_plan_is_kept(installed):
    world = World()
    world.playlist("empty-1", "Untitled Playlist", ())
    planned = world.kept(installed)
    world.account.placed["empty-1"] = world.folder("Phil's Spotify")

    done = root.apply(installed, world.account, planned)

    assert world.account.root_removed == []
    assert done.kept[0][1] == "empty-1" and "in a folder now" in done.kept[0][3]


def test_a_removal_the_account_refuses_before_sending_is_kept_and_the_apply_goes_on(
    installed, monkeypatch
):
    from cratekit.core.cause import refuse

    world = World()
    world.playlist("empty-1", "Untitled Playlist", ())
    world.playlist("empty-2", "Videos only", ())
    real = world.account.remove_root_playlist

    def refusing(playlist_id, kind):
        if playlist_id == "empty-2":
            raise refuse(
                "outbound-remove-refused",
                "the provider serves it with 2 video(s), which is not empty",
                detail={"problem": "not-this-kind"},
            )
        real(playlist_id, kind)

    monkeypatch.setattr(world.account, "remove_root_playlist", refusing)

    done = root.apply(installed, world.account, world.kept(installed))

    assert world.account.root_removed == [("empty-1", kinds.EMPTY)]
    assert [one[1] for one in done.kept] == ["empty-2"]


def test_a_label_folder_that_cannot_be_read_leaves_its_debris_and_refuses_nothing_else(
    installed, monkeypatch
):
    from cratekit.core.cause import refuse

    world = World()
    folder = world.label_folder()
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2])
    world.playlist("empty-1", "Untitled Playlist", ())
    real = world.account.folder_playlists
    reads = {"walked": False}

    def failing(folder_id):
        # The filing's walk of every folder reads it first; the debris check second.
        if folder_id == folder and reads["walked"]:
            raise refuse("unavailable-transient", "the provider did not answer")
        if folder_id == folder:
            reads["walked"] = True
        return real(folder_id)

    monkeypatch.setattr(world.account, "folder_playlists", failing)

    rows = _rows(world.kept(installed))

    assert rows["debris-1"].action == root.LEFT and "could not be read" in rows["debris-1"].why
    assert rows["empty-1"].action == root.REMOVE


def test_a_debris_copy_with_no_listed_count_is_left_before_any_read(installed, monkeypatch):
    world = World()
    world.label_folder()
    world.playlist("debris-1", DEBRIS, CATALOGUE[:2], declared=None)
    monkeypatch.setattr(
        world.account, "playlist_tracks", lambda _id: pytest.fail("a track read was made")
    )

    row = _rows(world.kept(installed))["debris-1"]

    assert row.action == root.LEFT and "no track count" in row.why


def test_a_year_record_whose_folder_now_carries_a_legacy_name_is_not_reused(installed):
    world = World()
    legacy = world.folder(LEGACY)
    ledger.reserve_set_folder(installed, YEAR, lambda: "unused", adopt=legacy)
    world.playlist("old-1", "Custom 1", ("t1",), folder=legacy)

    planned = world.kept(installed)

    assert planned.years[YEAR].action == "create" and planned.years[YEAR].stale == legacy
    root.apply(installed, world.account, planned)
    assert world.account.placed["old-1"] != legacy
    assert world.account.folder_names[world.account.placed["old-1"]] == YEAR


def test_a_legacy_folder_whose_year_is_undecided_says_so(installed):
    world = World()
    world.folder(YEAR)
    world.folder(YEAR)
    legacy = world.folder(LEGACY)
    world.playlist("old-1", "Custom 1", ("t1",), folder=legacy)

    row = _rows(world.kept(installed))[legacy]

    assert "until the 2026 folder is decided" in row.why and "later run" not in row.why


def test_a_folder_removal_answered_not_found_is_read_back_rather_than_failed(installed):
    client = _Client(root_folders={"f-1": LEGACY})

    def gone(trns, type="folder"):  # noqa: A002 - the client's name
        client.root.pop("f-1", None)
        raise ObjectNotFound("f-1")

    client.user.favorites.remove_folders_playlists = gone

    _adapter(client, installed).remove_legacy_folder("f-1")

    assert client.root == {}


def test_a_session_with_no_user_is_a_provider_failure_not_a_crash(installed):
    client = _Client(root_folders={"f-1": LEGACY})
    client.user = None

    with pytest.raises(CratekitError):
        _adapter(client, installed).remove_legacy_folder("f-1")
