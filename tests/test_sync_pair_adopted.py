"""U216, ``crate sync pair`` never brings into rekordbox a playlist an adopted account folder already held.

At sitting 59 a rehearsal planned 18 rekordbox playlists, ``DOWNLOADED Techno``
and its kind, out of the account's ``Genre Trivia!`` root folder, which U198
had adopted with those playlists already inside. Driven here through the
dispatcher on a disposable database and the fake account U198's tests built:
a playlist an adopted folder held when it was adopted, and a ``DOWNLOADED ``
copy of a playlist a pair in the same folder holds, are named on the gate and
never made, and a playlist made on the account after the sync still comes in,
in an adopted folder or a created one, as U202 built it.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli, pair_discover
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_back import LONG_AGO, in_rekordbox, on_account
from tests.test_sync_pair_discover import _items, _said, plan_only, sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414

FOLDER = "Genre Trivia!"


def later(minutes: int) -> datetime:
    """A moment after every sync a test drives so far."""
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


@pytest.fixture
def trivia(world):
    """``Genre Trivia!`` on both sides, the account's holding two old DOWNLOADED copies.

    The sync adopts the account's root folder and makes one account playlist
    for each rekordbox playlist, as sitting 54 did on the live library.
    Answers the rekordbox folder and the two copies' account identifiers.
    """
    folder_id = world.account.create_folder(FOLDER)
    copies = {}
    for title in ("DOWNLOADED Techno", "DOWNLOADED House"):
        playlist_id = world.account.create_playlist(title)
        world.account.move_to_folder(playlist_id, folder_id)
        world.account.made_at[playlist_id] = LONG_AGO
        copies[title] = playlist_id
    rekordbox = world.folder(FOLDER)
    world.playlist("Techno", "1", under=rekordbox)
    world.playlist("House", "2", under=rekordbox)
    for track in ("t1", "t2", "t3", "t4", "t5", "t6"):
        world.dates[track] = LONG_AGO
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.folders_created == [FOLDER]
    return rekordbox, copies


def unrecorded(cfg) -> None:
    """Make the document read as one written before U216: no folder says what it held."""
    path = config.state_path("playlist_pairs", cfg)
    raw = json.loads(path.read_text(encoding="utf-8"))
    for folder in raw.get("folders", {}).values():
        folder.pop("held", None)
    path.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def left(plan, kind: str) -> dict[str, dict]:
    """Each account playlist left out for ``kind``, by its title."""
    return {item["name"]: item for item in _items(plan, "account-discovery", kind)}


# ═══════════════════════════════════════════════════════════════════════════
# What an adopted folder held is never brought in
# ═══════════════════════════════════════════════════════════════════════════


def test_the_adoption_records_what_the_folder_held(world, cfg, trivia):
    _rekordbox, copies = trivia
    (recorded,) = [one for name, one in pairs.PairStore(cfg).folders().items() if name == FOLDER]
    assert recorded.created is False
    assert recorded.held == frozenset(copies.values())


def test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made(world, trivia):
    rekordbox, copies = trivia
    plan = plan_only()
    assert not _items(plan, "rekordbox", "create")
    named = left(plan, pair_discover.BEFORE)
    assert set(named) == set(copies)
    assert named["DOWNLOADED Techno"]["account_id"] == copies["DOWNLOADED Techno"]
    assert "held it when a sync adopted" in named["DOWNLOADED Techno"]["why"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert set(in_rekordbox(world, rekordbox)) == {"Techno", "House"}
    assert "DOWNLOADED Techno" in _said(envelope, pair_cli.NOT_BROUGHT)


def test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in(world, cfg, trivia):
    rekordbox, _copies = trivia
    disco = on_account(world, f"{FOLDER} Disco", FOLDER, "t3", "t4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    inside = in_rekordbox(world, rekordbox)
    assert set(inside) == {"Techno", "House", "Disco"}
    assert world.held(inside["Disco"]) == ["3", "4"]
    assert pairs.PairStore(cfg).get(disco).rekordbox_id == inside["Disco"]


def test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in(world, cfg):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    world.dates["t1"] = LONG_AGO
    assert sync()[0] == int(ExitCode.OK)
    recorded = pairs.PairStore(cfg).folders()["GIG READY"]
    assert recorded.created is True and recorded.held == frozenset()
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(in_rekordbox(world, gig)["Closer"]) == ["4"]
    assert pairs.PairStore(cfg).get(closer).made


# ═══════════════════════════════════════════════════════════════════════════
# A DOWNLOADED copy of a paired playlist, in any synced folder
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "title", ["DOWNLOADED Techno", f"DOWNLOADED {FOLDER} Techno", "downloaded techno"]
)
def test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy(
    world, trivia, title
):
    rekordbox, _copies = trivia
    copy = on_account(world, title, FOLDER, "t1")
    plan = plan_only()
    assert not _items(plan, "rekordbox", "create")
    (named,) = _items(plan, "account-discovery", pair_discover.COPY)
    assert named["account_id"] == copy
    assert f"{FOLDER} Techno" in named["why"]
    assert sync()[0] == int(ExitCode.OK)
    assert set(in_rekordbox(world, rekordbox)) == {"Techno", "House"}


def test_a_downloaded_playlist_no_pair_names_still_comes_in(world, trivia):
    rekordbox, _copies = trivia
    on_account(world, "DOWNLOADED Disco", FOLDER, "t5")
    assert sync()[0] == int(ExitCode.OK)
    assert world.held(in_rekordbox(world, rekordbox)["DOWNLOADED Disco"]) == ["5"]


def test_a_downloaded_copy_in_a_created_folder_is_named_a_copy(world):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    world.dates["t1"] = LONG_AGO
    assert sync()[0] == int(ExitCode.OK)
    on_account(world, "DOWNLOADED Opener", "GIG READY", "t1")
    plan = plan_only()
    assert set(left(plan, pair_discover.COPY)) == {"DOWNLOADED Opener"}
    assert not _items(plan, "rekordbox", "create")


# ═══════════════════════════════════════════════════════════════════════════
# A folder adopted before U216, whose record says nothing of what it held
# ═══════════════════════════════════════════════════════════════════════════


def test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named(
    world, cfg, trivia
):
    """The brief's last scenario: no readable creation time leaves the playlist out."""
    rekordbox, copies = trivia
    unrecorded(cfg)
    assert pairs.PairStore(cfg).folders()[FOLDER].held is None
    world.account.made_at.clear()
    late = on_account(world, f"{FOLDER} Disco", FOLDER, "t3")
    plan = plan_only()
    assert not _items(plan, "rekordbox", "create")
    named = left(plan, pair_discover.BEFORE)
    assert set(named) == {*copies, f"{FOLDER} Disco"}
    assert named[f"{FOLDER} Disco"]["account_id"] == late
    assert "no creation time" in named[f"{FOLDER} Disco"]["why"]
    assert sync()[0] == int(ExitCode.OK)
    assert set(in_rekordbox(world, rekordbox)) == {"Techno", "House"}


def test_without_a_record_the_creation_time_decides(world, cfg, trivia):
    rekordbox, copies = trivia
    unrecorded(cfg)
    late = on_account(world, f"{FOLDER} Disco", FOLDER, "t3")
    world.account.made_at[late] = later(5)
    plan = plan_only()
    named = left(plan, pair_discover.BEFORE)
    assert set(named) == set(copies)
    assert "not after a sync adopted" in named["DOWNLOADED Techno"]["why"]
    (made,) = _items(plan, "rekordbox", "create")
    assert made["account_id"] == late
    assert sync()[0] == int(ExitCode.OK)
    assert set(in_rekordbox(world, rekordbox)) == {"Techno", "House", "Disco"}


def test_without_a_record_a_creation_time_without_a_zone_is_no_time(world, cfg, trivia):
    _rekordbox, _copies = trivia
    unrecorded(cfg)
    late = on_account(world, f"{FOLDER} Disco", FOLDER, "t3")
    world.account.made_at[late] = later(5).replace(tzinfo=None)
    plan = plan_only()
    assert not _items(plan, "rekordbox", "create")
    assert f"{FOLDER} Disco" in left(plan, pair_discover.BEFORE)


def test_a_created_folder_without_a_record_still_brings_in(world, cfg):
    """A folder this product created held nothing, record or none."""
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    world.dates["t1"] = LONG_AGO
    assert sync()[0] == int(ExitCode.OK)
    unrecorded(cfg)
    on_account(world, "GIG READY Closer", "GIG READY", "t4")
    assert sync()[0] == int(ExitCode.OK)
    assert world.held(in_rekordbox(world, gig)["Closer"]) == ["4"]


# ═══════════════════════════════════════════════════════════════════════════
# The rules alone
# ═══════════════════════════════════════════════════════════════════════════

ADOPTED = datetime(2026, 11, 4, 12, 0, tzinfo=timezone.utc)


def test_before_adoption_reads_the_record_first():
    rule = pair_discover.before_adoption
    assert rule("a", held=frozenset({"a"}), created=False, folder=FOLDER, made=None, adopted=None)
    assert not rule(
        "b", held=frozenset({"a"}), created=False, folder=FOLDER, made=LONG_AGO, adopted=ADOPTED
    )
    assert not rule("a", held=frozenset(), created=True, folder=FOLDER, made=None, adopted=None)
    assert not rule("a", held=None, created=True, folder=FOLDER, made=None, adopted=None)


def test_before_adoption_without_a_record_reads_the_time():
    def rule(made, adopted):
        return pair_discover.before_adoption(
            "a", held=None, created=False, folder=FOLDER, made=made, adopted=adopted
        )

    assert "no creation time" in rule(None, ADOPTED)
    assert "dates the adoption" in rule(ADOPTED + timedelta(days=1), None)
    assert "not after" in rule(ADOPTED, ADOPTED)
    assert "not after" in rule(ADOPTED - timedelta(seconds=1), ADOPTED)
    assert rule(ADOPTED + timedelta(seconds=1), ADOPTED) == ""
    assert "no creation time" in rule(datetime(2026, 12, 1), ADOPTED)


def test_the_adoption_moment_is_the_earliest_readable_mark():
    moment = pair_discover.adoption_moment
    assert moment([]) is None
    assert moment(["", "not a time", "2026-11-04T12:00:00"]) is None
    assert moment(["2026-11-04T13:00:00+00:00", "2026-11-04T12:00:00+00:00", "junk"]) == ADOPTED


def test_downloaded_copy_names_the_paired_title_it_copies():
    copy = pair_discover.downloaded_copy
    paired = [f"{FOLDER} Techno", f"{FOLDER} House"]
    assert copy(FOLDER, "DOWNLOADED Techno", paired) == f"{FOLDER} Techno"
    assert copy(FOLDER, f"DOWNLOADED {FOLDER} House", paired) == f"{FOLDER} House"
    assert copy(FOLDER, "Downloaded TECHNO", paired) == f"{FOLDER} Techno"
    assert copy(FOLDER, "Techno", paired) == ""
    assert copy(FOLDER, "DOWNLOADED Disco", paired) == ""
    assert copy(FOLDER, "DOWNLOADED ", paired) == ""
    assert copy(FOLDER, f"DOWNLOADED {FOLDER}", [FOLDER]) == ""
    assert copy(FOLDER, "DOWNLOADEDTechno", paired) == ""


# ═══════════════════════════════════════════════════════════════════════════
# The record, read and written
# ═══════════════════════════════════════════════════════════════════════════


def _document(cfg, folders) -> None:
    path = config.state_path("playlist_pairs", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "version": pairs.PAIRS_VERSION,
                "library_id": cfg.library.volume_id,
                "pairs": {},
                "folders": folders,
            }
        ),
        encoding="utf-8",
    )


@pytest.mark.parametrize("held", ["a", [""], [3], {"a": 1}])
def test_a_folder_whose_held_is_not_ids_refuses_the_document(cfg, held):
    _document(cfg, {FOLDER: {"folder_id": "f1", "created": False, "held": held}})
    with pytest.raises(CratekitError) as caught:
        pairs.PairStore(cfg).folders()
    assert caught.value.cause.reason == "sync-pair-store-unusable"


def test_a_folder_record_keeps_what_it_held_through_another_write(cfg):
    _document(
        cfg,
        {
            FOLDER: {"folder_id": "f1", "created": False, "held": ["b", "a"]},
            "Old": {"folder_id": "f2", "created": False},
        },
    )
    store = pairs.PairStore(cfg)
    store.remember({"9": pairs.Miss("X", "none")})
    folders = store.folders()
    assert folders[FOLDER].held == frozenset({"a", "b"})
    assert folders["Old"].held is None
    raw = json.loads(config.state_path("playlist_pairs", cfg).read_text(encoding="utf-8"))
    assert raw["folders"][FOLDER]["held"] == ["a", "b"]
    assert "held" not in raw["folders"]["Old"]


def test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing(cfg):
    store = pairs.PairStore(cfg)
    store.reserve_folder(FOLDER, lambda: "unused", adopt="f1", held=("p1", "p2"))
    store.reserve_folder("GIG READY", lambda: "f2", held=("ignored",))
    folders = store.folders()
    assert folders[FOLDER].held == frozenset({"p1", "p2"}) and not folders[FOLDER].created
    assert folders["GIG READY"].held == frozenset() and folders["GIG READY"].created


# ═══════════════════════════════════════════════════════════════════════════
# The account's dated folder read
# ═══════════════════════════════════════════════════════════════════════════


def test_the_dated_folder_read_gives_each_playlists_creation_time_from_the_same_pages():
    from cratekit.modules.outbound.tidal_account import TidalAccount
    from tests.test_adapter_listing import CountingTransport, _logged_in_over, _owned_playlist

    held = [_owned_playlist(n) for n in range(3)]
    held[0]["created"] = "2025-03-01T10:00:00.000+0000"
    transport = CountingTransport(held)
    account = TidalAccount(_logged_in_over(transport), sleep=lambda _: None)
    dated = account.folder_playlists_dated("folder-trivia")
    assert dated["pl0"] == ("List 000", datetime(2025, 3, 1, 10, 0, tzinfo=timezone.utc))
    assert dated["pl1"] == ("List 001", None)
    assert set(dated) == {"pl0", "pl1", "pl2"}
    assert transport.single_fetches() == 0
