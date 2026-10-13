"""U131: every playlist on the account sits in a folder chosen by a readable rule.

Driven at the filing step's own plan and apply, and at ``export playlist``'s
apply, against the recording fake account, so each scenario reads where the
account says a playlist sits rather than the step's own report.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import export, kinds, ledger
from cratekit.organize import filing
from cratekit.sync import mark_record
from tests import outbound_fakes
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

MARKED_WHEN = "2026-10-08T21:00:00+00:00"

#: A playlist of the author's that goes to Mine: its name says downloaded and
#: no sync recorded when, so no year files it. Since U143 an unmarked one with
#: no prefix is a working custom playlist and stays at the root instead.
OWN = "DOWNLOADED Sunday warmup"


def _world(cfg, account, *playlists: tuple[str, str]) -> list[AccountPlaylist]:
    listed = []
    for playlist_id, name in playlists:
        account.titles[playlist_id] = name
        listed.append(AccountPlaylist(playlist_id, name, 1))
    return listed


def _plan(cfg, account, listed, *, labels=(), marks=None):
    return filing.plan(
        cfg,
        listed=listed,
        remote=account,
        labels=labels,
        marks=mark_record.MarkRecord(cfg).all() if marks is None else marks,
        working=lambda name: name == "Work in progress",
    )


def _rows(planned) -> dict[str, filing.Placement]:
    return {row.playlist_id: row for row in planned.rows}


def _mark(cfg, playlist_id: str, name: str, when: str = MARKED_WHEN) -> None:
    mark_record.MarkRecord(cfg).record_marked(
        "a pass", {playlist_id: (name, f"DOWNLOADED {name}")}, now=when
    )


def _folder_of(account, playlist_id: str) -> str:
    return account.folder_names.get(account.placed.get(playlist_id, ""), "")


def test_each_kind_lands_in_its_own_folder(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    ledger.reserve_playlist(cfg, "crate-export", lambda: "exported-1")
    ledger.reserve_set_playlist(cfg, "A set", "2026", lambda: "set-1")
    _mark(cfg, "marked-1", "Phil 10_8_26")
    listed = _world(
        cfg,
        account,
        ("exported-1", "Exported crate"),
        ("set-1", "A set"),
        ("marked-1", "DOWNLOADED Phil 10_8_26"),
        ("own-1", OWN),
        ("custom-1", "Sunday warmup"),
        ("label-1", "Kompakt 2024"),
        ("work-1", "Work in progress"),
    )

    planned = _plan(cfg, account, listed, labels=("Kompakt",))
    rows = _rows(planned)

    assert (rows["exported-1"].action, rows["exported-1"].kind) == (filing.MOVE, kinds.EXPORTS)
    assert (rows["own-1"].action, rows["own-1"].kind) == (filing.MOVE, kinds.MINE)
    # U143: unmarked, unprefixed and unclaimed, it is a working custom playlist.
    assert (rows["custom-1"].action, rows["custom-1"].why) == (filing.LEFT, filing.WORKING_CUSTOM)
    assert (rows["marked-1"].action, rows["marked-1"].year) == (filing.MOVE, "2026")
    # A set awaiting its archive stays at the root for the archive to file.
    assert (rows["set-1"].action, rows["set-1"].why) == (filing.LEFT, filing.SET_STEP)
    assert (rows["label-1"].action, rows["label-1"].why) == (filing.LEFT, filing.LABEL_STEP)
    assert rows["work-1"].action == filing.LEFT
    assert planned.creates() == ("2026", kinds.EXPORTS, kinds.MINE)

    done = filing.apply(cfg, account, planned)

    assert _folder_of(account, "exported-1") == kinds.EXPORTS
    assert _folder_of(account, "own-1") == kinds.MINE
    assert _folder_of(account, "marked-1") == "2026"
    assert not {"set-1", "label-1", "work-1", "custom-1"} & set(account.placed)
    assert sorted(done.kinds_created) == [kinds.EXPORTS, kinds.MINE]
    assert ledger.kind_folder(cfg, kinds.MINE).created is True


def test_a_rerun_plans_nothing(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    listed = _world(cfg, account, ("own-1", OWN), ("own-2", "DOWNLOADED Digging"))
    filing.apply(cfg, account, _plan(cfg, account, listed))
    moves = len(account.moves)

    again = _plan(cfg, account, listed)

    assert again.rows == () and not again.writes
    assert account.folders_created == [kinds.MINE]
    assert len(account.moves) == moves


def test_a_playlist_in_a_hand_made_folder_is_left(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    hand = account.create_folder("Old faves")
    account.folders_created.clear()
    listed = _world(cfg, account, ("own-1", OWN))
    account.placed["own-1"] = hand
    _mark(cfg, "own-1", "Sunday warmup")

    planned = _plan(cfg, account, listed)

    assert "own-1" not in _rows(planned)
    filing.apply(cfg, account, planned)
    assert account.placed["own-1"] == hand and account.moves == []


def test_a_renamed_playlist_and_a_renamed_folder_stay_where_they_are(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    listed = _world(cfg, account, ("own-1", OWN))
    filing.apply(cfg, account, _plan(cfg, account, listed))
    mine = account.placed["own-1"]
    # A person renames both the playlist and the folder on the account.
    account.titles["own-1"] = "Sunday warmup, kept"
    account.folder_names[mine] = "My own"
    listed = _world(
        cfg, account, ("own-1", "Sunday warmup, kept"), ("own-2", "DOWNLOADED New one")
    )

    planned = _plan(cfg, account, listed)
    filing.apply(cfg, account, planned)

    assert "own-1" not in _rows(planned)
    # The kind's folder is recorded by its identifier, so the renamed one is reused.
    assert account.placed["own-2"] == mine == account.placed["own-1"]
    assert account.folders_created == [kinds.MINE]


def test_a_playlist_matching_no_rule_is_listed_and_left(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    # A label's dated playlist is the product's, not an export, not the author's.
    ledger.reserve_label_dated(cfg, "label-x", "Label X 10_10_26", lambda: "dated-1")
    listed = _world(cfg, account, ("dated-1", "Label X 10_10_26"))

    row = _rows(_plan(cfg, account, listed))["dated-1"]

    assert (row.action, row.why) == (filing.LEFT, filing.PRODUCT_MADE)


def test_two_folders_named_mine_leave_the_authors_playlists_listed(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    account.create_folder(kinds.MINE)
    account.create_folder(kinds.MINE)
    listed = _world(cfg, account, ("own-1", OWN))

    row = _rows(_plan(cfg, account, listed))["own-1"]

    assert row.action == filing.LEFT and "2 root folders" in row.why
    assert row.kind == kinds.MINE


def test_a_hand_made_folder_named_mine_is_adopted_and_never_emptied(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    hand = account.create_folder(kinds.MINE)
    account.folders_created.clear()
    listed = _world(cfg, account, ("own-1", OWN), ("held-1", "Kept by hand"))
    account.placed["held-1"] = hand
    _mark(cfg, "held-1", "Kept by hand")

    planned = _plan(cfg, account, listed)
    filing.apply(cfg, account, planned)

    assert account.placed["own-1"] == hand
    assert account.folders_created == []
    # The folder was a person's before it was adopted, so nothing leaves it.
    assert account.placed["held-1"] == hand
    assert "held-1" not in _rows(_plan(cfg, account, listed))


def test_a_playlist_marked_after_it_was_filed_in_mine_reaches_its_year(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    listed = _world(cfg, account, ("own-1", OWN))
    filing.apply(cfg, account, _plan(cfg, account, listed))
    assert _folder_of(account, "own-1") == kinds.MINE
    _mark(cfg, "own-1", "Sunday warmup")

    planned = _plan(cfg, account, listed)
    row = _rows(planned)["own-1"]
    filing.apply(cfg, account, planned)

    assert (row.action, row.year) == (filing.MOVE, "2026")
    assert _folder_of(account, "own-1") == "2026"
    assert _plan(cfg, account, listed).rows == ()


def _exported(cfg, account, key="crate-a", name="A crate", tracks=("t1",)):
    account.catalog.update({one: f"remote-{one}" for one in tracks})
    planned = export.plan(
        [export.LocalTrack(identity=one, title=one) for one in tracks],
        playlist_key=key,
        name=name,
        account=account,
        # What the gate would show and cover, read off the account now.
        filing=kinds.token(kinds.decide(cfg, export.KIND, account.folders())),
    )
    return export.apply(cfg, account, planned)


def test_a_new_export_is_filed_in_exports_at_creation(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()

    first = _exported(cfg, account)
    second = _exported(cfg, account, tracks=("t1", "t2"))

    assert first.created and first.unfiled == ""
    assert _folder_of(account, first.remote_id) == kinds.EXPORTS
    # The playlist already existed, so the second apply moves nothing.
    assert not second.created and len(account.moves) == 1
    assert account.folders_created == [kinds.EXPORTS]
    assert account.playlists[first.remote_id] == ["remote-t1", "remote-t2"]


def test_an_export_whose_folder_a_name_cannot_decide_stays_at_the_root(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    account.create_folder(kinds.EXPORTS)
    account.create_folder(kinds.EXPORTS)

    report = _exported(cfg, account)

    assert report.created and "2 root folders" in report.unfiled
    assert report.remote_id not in account.placed
    assert account.playlists[report.remote_id] == ["remote-t1"]


def test_a_refused_move_at_creation_keeps_the_export_and_says_why(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount(provider_error=True)
    original = account.move_to_folder

    def refuse(playlist_id, folder_id):
        account.fail_on = frozenset({playlist_id})
        original(playlist_id, folder_id)

    account.move_to_folder = refuse

    report = _exported(cfg, account)

    assert report.created and report.unfiled
    assert account.playlists[report.remote_id] == ["remote-t1"]
    assert ledger.exported_playlist(cfg, "crate-a").remote_id == report.remote_id


def test_the_kind_folders_record_survives_another_write(installed):
    cfg = installed
    ledger.reserve_kind_folder(cfg, kinds.MINE, lambda: "folder-m")
    ledger.reserve_set_folder(cfg, "2026", lambda: "folder-y")

    assert ledger.kind_folder(cfg, kinds.MINE) == ledger.KindFolder("folder-m", True)
    assert ledger.reserve_kind_folder(cfg, kinds.MINE, lambda: "again") == ("folder-m", False)
    assert ledger.exported_playlist_ids(cfg) == frozenset()


def test_a_stale_kind_folder_record_is_replaced(installed):
    cfg = installed
    account = outbound_fakes.StrictAccount()
    ledger.reserve_kind_folder(cfg, kinds.MINE, lambda: "gone-folder")

    folder = kinds.decide(cfg, kinds.MINE, account.folders())

    assert (folder.action, folder.stale) == (kinds.CREATE, "gone-folder")
    assert kinds.reserve(cfg, account, folder) == "folder-1"
    assert ledger.kind_folder(cfg, kinds.MINE).folder_id == "folder-1"




def test_a_playlist_whose_mark_has_no_year_is_filed_in_mine(installed):
    """U131 REVERSES U116's UNDATED LEAVE. Before, a playlist whose mark carried
    no readable year was reported and left at the root; no ledger claims it,
    so it is now the author's own and goes to Mine, with the old reason."""
    cfg = installed
    account = outbound_fakes.StrictAccount()
    _mark(cfg, "own-1", "Sunday warmup", when="soon")
    listed = _world(cfg, account, ("own-1", "DOWNLOADED Sunday warmup"))

    row = _rows(_plan(cfg, account, listed))["own-1"]

    assert (row.action, row.kind, row.why) == (filing.MOVE, kinds.MINE, filing.UNDATED)
