"""U208: a paired row whose ISRC names several agreeing releases is paired as one of them.

Matches go through the real adapter, whose rule ``tests/test_outbound_tidal_account.py``
pins; here the pairs ask it, link its choice and keep every refusal. D1 applies.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from cratekit.core import tags
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import pairs, service, tidal_account
from cratekit.sync import pair_cli
from tests import outbound_fakes
from tests._sync_builders import exited
from tests.cli_drive import drive
from tests.test_outbound_tidal_account import FakeClient, Track, no_sleep, on_album
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair import ACCOUNT, ROWS, VERB, _untagged_row, isrc, sync
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import world as world  # noqa: PLC0414

#: The row whose ISRC names several releases.
TIED = "1"
#: The whole sync of the one pair, named.
PAIR = [*VERB, ACCOUNT]


class Matched(outbound_fakes.StrictAccount):
    """The recording fake for every write, the real adapter for every match."""

    def __init__(self, client: FakeClient) -> None:
        super().__init__(catalog={})
        self.client = client
        self.adapter = tidal_account.TidalAccount(client, sleep=no_sleep)

    def match_track(self, **asked):
        self.matches.append(asked)
        if asked.get("any_agreeing"):
            self.any_agreeing.append(asked["identity"])
        return self.adapter.match_track(**asked)

    def unmatched_reason(self, identity: str) -> str:
        return self.adapter.unmatched_reason(identity)

    def tie_broken(self, identity: str) -> bool:
        return self.adapter.tie_broken(identity)


def release(remote_id: str, content_id: str = TIED, version: str | None = None) -> Track:
    """One provider release spelled as the library row ``content_id`` is."""
    return Track(remote_id, f"Title t{content_id}", version, (f"Artist {content_id}",))


def _artists(cfg) -> None:
    """Give every content row an artist and its title, which the adapter judges agreement by."""
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        for content_id in ROWS:
            conn.execute(
                "INSERT OR IGNORE INTO djmdArtist (ID, Name) VALUES (?, ?)",
                (f"a{content_id}", f"Artist {content_id}"),
            )
            conn.execute(
                "UPDATE djmdContent SET ArtistID = ?, Title = ? WHERE ID = ?",
                (f"a{content_id}", f"Title t{content_id}", content_id),
            )
        conn.commit()
    finally:
        conn.close()


@pytest.fixture
def tied(world, cfg, monkeypatch):
    """A pair whose rekordbox side holds row 1, and the provider's releases of its ISRC."""

    def made(releases: list[Track], *, hearts=(), rekordbox=(TIED,), account=()):
        w = world(account=account, rekordbox=rekordbox)
        _artists(cfg)
        found = {isrc(TIED): list(releases)}
        for content_id in rekordbox:
            if content_id != TIED:
                found[isrc(content_id)] = [release(f"9{content_id}", content_id)]
                w.codes[f"9{content_id}"] = isrc(content_id)
        for one in releases:
            w.codes[str(one.id)] = isrc(TIED)
        matched = Matched(FakeClient(isrcs=found, hearts=list(hearts)))
        matched.playlists = w.account.playlists
        w.account = matched
        monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(matched))
        return w

    return made


def _plan(w) -> dict:
    """The plan both gates show, both answered skip, so nothing is written."""
    return exited(sync(w.args(), rekordbox="skip", account="skip"))["data"]


def _pair(cfg) -> pairs.Pair:
    held = pairs.PairStore(cfg).get(ACCOUNT)
    assert held is not None
    return held


def _three():
    return [release("303"), release("101"), release("202")]


# The tie is broken as the mirror breaks it, and linked


def test_a_tie_with_none_hearted_is_linked_to_the_lowest_release(tied, cfg):
    w = tied(_three())

    exited(sync(w.args()))

    assert w.on_account() == ["101"]
    assert _pair(cfg).links == {"101": TIED}
    assert TIED not in pairs.PairStore(cfg).misses()
    assert w.account.any_agreeing and set(w.account.any_agreeing) == {TIED}


def _pair_line(w) -> tuple[str, dict]:
    """The gate's line for the pair, nothing yet written."""
    asked = exited(drive(w.args()), ExitCode.DECISION_REQUIRED)
    return asked["cause"]["detail"]["shown"][f"pair {ACCOUNT}"], asked["cause"]["detail"]["shown"]


def test_the_gate_names_how_many_rows_a_broken_tie_matched(tied):
    w = tied(_three(), rekordbox=(TIED, "2"))

    line, shown = _pair_line(w)

    assert "1 row(s) matched as one of several releases that all agree with it" in line
    assert sum(1 for item in shown["items"] if item.get("tied")) == 1
    assert _plan(w)["totals"]["tied"] == 1


def test_a_pair_with_no_tie_says_nothing_of_one(tied):
    w = tied([release("101")], rekordbox=(TIED, "2"))
    line, _shown = _pair_line(w)
    assert "agree with it" not in line
    assert _plan(w)["totals"]["tied"] == 0


def test_a_lone_heart_takes_the_hearted_release_and_is_not_a_broken_tie(tied, cfg):
    w = tied(_three(), hearts=("202",))
    assert _plan(w)["totals"]["tied"] == 0
    exited(sync(w.args()))
    assert w.on_account() == ["202"]
    assert _pair(cfg).links == {"202": TIED}


def test_two_hearted_releases_take_the_lower_hearted_one(tied, cfg):
    w = tied([release("101"), release("303"), release("202")], hearts=("303", "202"))
    assert _plan(w)["totals"]["tied"] == 1
    exited(sync(w.args()))
    assert w.on_account() == ["202"]


def test_the_files_album_narrows_the_tie_before_the_lowest_is_taken(tied, cfg, tmp_path):
    w = tied(
        [
            on_album(release("101"), "Single"),
            on_album(release("303"), "Long Player"),
            on_album(release("202"), "Long Player"),
        ]
    )
    _untagged_row(cfg, TIED, tmp_path, file_isrc=isrc(TIED))
    target = Path(cfg.library.root) / "Music" / f"{TIED}.flac"
    assert tags.write_tags(target, {"album": "Long Player"}) is True

    exited(sync(w.args()))

    assert w.on_account() == ["202"]
    assert _pair(cfg).links == {"202": TIED}


def _writes(w) -> tuple[list, list, list]:
    return list(w.account.added), list(w.account.chunks), list(w.account.taken)


def test_a_second_sync_asks_the_provider_nothing_about_a_linked_tie(tied):
    w = tied([release("202"), release("101")])
    exited(sync(w.args()))
    asked = list(w.account.client.isrc_asked)
    writes = _writes(w)
    w.account.client.user.favorites.hearts.append("202")

    exited(sync(PAIR))

    assert w.account.client.isrc_asked == asked
    assert _writes(w) == writes
    assert w.on_account() == ["101"]


# The refusals before the tie stand


def test_a_tie_beside_an_unreadable_release_still_refuses_and_is_not_remembered(tied, cfg):
    w = tied([release("101"), release("202"), Track("303", "", None, ())])

    envelope = exited(sync(w.args()))

    assert w.on_account() == []
    assert TIED not in pairs.PairStore(cfg).misses()
    message = next(
        one["message"] for one in envelope["warnings"] if one["code"] == pair_cli.UNMATCHED
    )
    assert service.UNREADABLE_CANDIDATE in message
    asked = len(w.account.client.isrc_asked)
    exited(sync(PAIR))
    assert len(w.account.client.isrc_asked) > asked, "an unreadable tie is asked again"


def test_releases_that_do_not_agree_with_the_row_still_refuse(tied, cfg):
    w = tied([release("101", version="Radio Edit"), release("202", version="Extended Mix")])

    exited(sync(w.args()))

    assert w.on_account() == []
    assert "none of them agrees" in pairs.PairStore(cfg).misses()[TIED].reason


def test_a_tie_remembered_as_a_miss_before_this_unit_is_asked_once_and_linked(tied, cfg):
    w = tied([release("202"), release("101")])
    pairs.PairStore(cfg).remember(
        {
            TIED: pairs.Miss(
                isrc(TIED),
                f"the ISRC {isrc(TIED)} names 2 provider tracks, 2 "
                f"{service.AGREEING_RELEASES} and the account hearts 0 of those, and "
                f"the file carries no album tag, so none was chosen",
            )
        }
    )

    exited(sync(w.args()))

    assert isrc(TIED) in w.account.client.isrc_asked
    assert w.on_account() == ["101"]
    assert _pair(cfg).links == {"101": TIED}
    assert TIED not in pairs.PairStore(cfg).misses()
    asked = list(w.account.client.isrc_asked)
    exited(sync(PAIR))
    assert w.account.client.isrc_asked == asked


# The reverse direction: a sibling release added on the account


def _sibling_added(w) -> None:
    """A person adds, on the account, a release of the tied row the link did not take."""
    w.account.playlists[ACCOUNT].append("202")


def _quiet(w) -> dict:
    """One more whole sync, which must write nothing on either side."""
    held, on_account = w.held(), w.on_account()
    envelope = exited(sync(PAIR))
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert (w.held(), w.on_account()) == (held, on_account)
    return envelope


def _with_sibling(tied, rekordbox, cfg=None, tmp_path=None, on_file=False):
    """The tie linked to 101 and synced, then 202 added on the account and synced in."""
    w = tied([release("202"), release("101")], rekordbox=rekordbox)
    if on_file:
        _untagged_row(cfg, TIED, tmp_path, file_isrc=isrc(TIED))
    exited(sync(w.args()))
    _sibling_added(w)
    exited(sync(PAIR))
    return w


ON_FILE = pytest.mark.parametrize("on_file", [False, True], ids=["database-isrc", "file-isrc"])


@ON_FILE
def test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued(
    tied, cfg, tmp_path, on_file
):
    w = tied([release("202"), release("101")])
    if on_file:
        _untagged_row(cfg, TIED, tmp_path, file_isrc=isrc(TIED))
    exited(sync(w.args()))
    assert w.on_account() == ["101"]
    _sibling_added(w)

    envelope = exited(sync(PAIR))

    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert w.held() == [TIED]
    assert w.on_account() == ["101", "202"]
    assert _pair(cfg).links.get("202") == TIED
    _quiet(w)


def _rows_of_playlist(cfg, playlist_id: str) -> list[tuple[str, str]]:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        return [
            (str(one[0]), str(one[1]))
            for one in conn.execute(
                "SELECT ID, ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY ID",
                (playlist_id,),
            ).fetchall()
        ]
    finally:
        conn.close()


@ON_FILE
def test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account(
    tied, cfg, tmp_path, on_file
):
    """Two releases linked to one row are one key, so both leave the account."""
    w = _with_sibling(tied, (TIED, "2"), cfg, tmp_path, on_file)
    assert w.on_account() == ["101", "92", "202"]
    w.rekordbox_remove(TIED)

    exited(sync(PAIR))

    assert w.held() == ["2"]
    assert w.on_account() == ["92"]
    _quiet(w)
    assert w.held() == ["2"]


@ON_FILE
def test_one_release_taken_off_the_account_while_another_stays_changes_nothing(
    tied, cfg, tmp_path, on_file
):
    """The row is not rewritten in rekordbox and the release is not put back."""
    w = _with_sibling(tied, (TIED, "2", "3"), cfg, tmp_path, on_file)
    memberships = _rows_of_playlist(cfg, w.rekordbox_id)
    w.account.playlists[ACCOUNT].remove("202")

    exited(sync(PAIR))

    assert _rows_of_playlist(cfg, w.rekordbox_id) == memberships
    assert w.on_account() == ["101", "92", "93"]
    _quiet(w)
    assert w.on_account() == ["101", "92", "93"]


def test_both_releases_taken_off_the_account_take_the_row_out_of_rekordbox(tied):
    w = _with_sibling(tied, (TIED, "2"))
    w.account.playlists[ACCOUNT][:] = ["92"]

    exited(sync(PAIR))

    assert w.held() == ["2"]
    _quiet(w)
    # PUT BACK IN REKORDBOX, the row goes as its lowest linked release, every run.
    w.rekordbox_add(TIED)
    exited(sync(PAIR))
    assert w.on_account() == ["92", "101"]


def test_two_releases_already_on_the_account_take_the_lower_and_add_no_third(tied, cfg):
    """The provider's lowest release is not added beside the two already there."""
    w = tied([release("101"), release("202"), release("303")], account=())
    w.account.playlists[ACCOUNT][:] = ["303", "202"]

    envelope = exited(sync(w.args()))

    assert w.on_account() == ["303", "202"]
    assert w.held() == [TIED]
    assert _pair(cfg).links.get("202") == TIED
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert isrc(TIED) not in w.account.client.isrc_asked
    _quiet(w)


def test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off(tied):
    """Removals are not expanded under links made after the merge."""
    w = tied([release("202"), release("101")], rekordbox=(TIED, "2"))
    exited(sync(w.args()))
    assert w.on_account() == ["101", "92"]
    w.rekordbox_remove(TIED)
    _sibling_added(w)

    exited(sync(PAIR))

    assert "202" in w.on_account() and "101" not in w.on_account()
    settled = (sorted(w.held()), w.on_account())
    _quiet(w)
    _quiet(w)
    assert (sorted(w.held()), w.on_account()) == settled


def test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it(tied):
    """The order does not group a row's releases in another key space."""
    w = tied([release("202"), release("101")], rekordbox=("2", TIED))
    exited(sync(w.args()))
    assert w.on_account() == ["92", "101"]
    w.account.playlists[ACCOUNT].insert(0, "202")
    ordered = list(w.account.ordered)

    exited(sync(PAIR))

    assert w.on_account() == ["202", "92", "101"]
    assert w.account.ordered == ordered
    held = w.held()
    _quiet(w)
    _quiet(w)
    assert w.held() == held
    assert w.account.ordered == ordered


def test_the_first_release_taken_off_while_a_later_one_stays_keeps_the_row(tied):
    """Dropping the first release while a later one stays keeps the row."""
    w = _with_sibling(tied, (TIED, "2", "3"))
    w.account.playlists[ACCOUNT].remove("101")

    exited(sync(PAIR))

    assert sorted(w.held()) == [TIED, "2", "3"]
    assert w.on_account() == ["92", "93", "202"]
    _quiet(w)
