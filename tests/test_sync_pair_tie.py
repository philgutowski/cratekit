"""U208: a paired row whose ISRC names several agreeing releases is paired as one of them.

Driven through ``crate sync pair`` on the disposable database
``tests/test_sync_pair.py`` builds, every write through the recording fake
account and every MATCH through the real adapter over the fake provider client,
so the release a tie takes is the one ``match_track`` chooses and not one a
fake was told to choose. The adapter's own rule is pinned at its level in
``tests/test_outbound_tidal_account.py``; this file pins that the pairs ask it,
link what it chose, and keep every refusal before the tie.

D1 applies. Nothing here names a real account, a real person or a real track.
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
from tests.cli_drive import drive
from tests.test_outbound_tidal_account import FakeClient, Track, no_sleep
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair import (
    ACCOUNT,
    ROWS,
    VERB,
    _untagged_row,
    isrc,
    sync,
)
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import world as world  # noqa: PLC0414

#: The row whose ISRC names several releases.
TIED = "1"


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


def _on_album(track: Track, name: str) -> Track:
    from tests.test_outbound_tidal_account import on_album

    return on_album(track, name)


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
    code, envelope = sync(w.args(), rekordbox="skip", account="skip")
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]


def _pair(cfg) -> pairs.Pair:
    held = pairs.PairStore(cfg).get(ACCOUNT)
    assert held is not None
    return held


# ═══════════════════════════════════════════════════════════════════════════
# The tie is broken as the mirror breaks it, and linked
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tie_with_none_hearted_is_linked_to_the_lowest_release(tied, cfg):
    w = tied([release("303"), release("101"), release("202")])

    code, envelope = sync(w.args())

    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["101"]
    assert _pair(cfg).links == {"101": TIED}
    assert TIED not in pairs.PairStore(cfg).misses()
    assert w.account.any_agreeing and set(w.account.any_agreeing) == {TIED}


def test_the_gate_names_how_many_rows_a_broken_tie_matched(tied):
    w = tied([release("303"), release("101"), release("202")], rekordbox=(TIED, "2"))

    code, envelope = drive(w.args())

    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    shown = envelope["cause"]["detail"]["shown"]
    line = shown[f"pair {ACCOUNT}"]
    assert "1 row(s) matched as one of several releases that all agree with it" in line
    assert sum(1 for item in shown["items"] if item.get("tied")) == 1
    assert _plan(w)["totals"]["tied"] == 1


def test_a_pair_with_no_tie_says_nothing_of_one(tied):
    w = tied([release("101")], rekordbox=(TIED, "2"))
    code, envelope = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert "agree with it" not in envelope["cause"]["detail"]["shown"][f"pair {ACCOUNT}"]
    assert _plan(w)["totals"]["tied"] == 0


def test_a_lone_heart_takes_the_hearted_release_and_is_not_a_broken_tie(tied, cfg):
    w = tied([release("303"), release("101"), release("202")], hearts=("202",))
    assert _plan(w)["totals"]["tied"] == 0
    assert sync(w.args())[0] == int(ExitCode.OK)
    assert w.on_account() == ["202"]
    assert _pair(cfg).links == {"202": TIED}


def test_two_hearted_releases_take_the_lower_hearted_one(tied, cfg):
    w = tied([release("101"), release("303"), release("202")], hearts=("303", "202"))
    assert _plan(w)["totals"]["tied"] == 1
    assert sync(w.args())[0] == int(ExitCode.OK)
    assert w.on_account() == ["202"]


def test_the_files_album_narrows_the_tie_before_the_lowest_is_taken(tied, cfg, tmp_path):
    w = tied(
        [
            _on_album(release("101"), "Single"),
            _on_album(release("303"), "Long Player"),
            _on_album(release("202"), "Long Player"),
        ]
    )
    _untagged_row(cfg, TIED, tmp_path, file_isrc=isrc(TIED))
    target = Path(cfg.library.root) / "Music" / f"{TIED}.flac"
    assert tags.write_tags(target, {"album": "Long Player"}) is True

    assert sync(w.args())[0] == int(ExitCode.OK)

    assert w.on_account() == ["202"]
    assert _pair(cfg).links == {"202": TIED}


def test_a_second_sync_asks_the_provider_nothing_about_a_linked_tie(tied):
    w = tied([release("202"), release("101")])
    assert sync(w.args())[0] == int(ExitCode.OK)
    asked = list(w.account.client.isrc_asked)
    writes = (list(w.account.added), list(w.account.chunks), list(w.account.taken))
    w.account.client.user.favorites.hearts.append("202")

    code, envelope = sync([*VERB, ACCOUNT])

    assert code == int(ExitCode.OK), envelope
    assert w.account.client.isrc_asked == asked
    assert (list(w.account.added), list(w.account.chunks), list(w.account.taken)) == writes
    assert w.on_account() == ["101"]


# ═══════════════════════════════════════════════════════════════════════════
# The refusals before the tie stand
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tie_beside_an_unreadable_release_still_refuses_and_is_not_remembered(tied, cfg):
    w = tied([release("101"), release("202"), Track("303", "", None, ())])

    code, envelope = sync(w.args())

    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == []
    assert TIED not in pairs.PairStore(cfg).misses()
    message = next(
        one["message"] for one in envelope["warnings"] if one["code"] == pair_cli.UNMATCHED
    )
    assert service.UNREADABLE_CANDIDATE in message
    asked = len(w.account.client.isrc_asked)
    assert sync([*VERB, ACCOUNT])[0] == int(ExitCode.OK)
    assert len(w.account.client.isrc_asked) > asked, "an unreadable tie is asked again"


def test_releases_that_do_not_agree_with_the_row_still_refuse(tied, cfg):
    w = tied([release("101", version="Radio Edit"), release("202", version="Extended Mix")])

    code, envelope = sync(w.args())

    assert code == int(ExitCode.OK), envelope
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

    assert sync(w.args())[0] == int(ExitCode.OK)

    assert isrc(TIED) in w.account.client.isrc_asked
    assert w.on_account() == ["101"]
    assert _pair(cfg).links == {"101": TIED}
    assert TIED not in pairs.PairStore(cfg).misses()
    asked = list(w.account.client.isrc_asked)
    assert sync([*VERB, ACCOUNT])[0] == int(ExitCode.OK)
    assert w.account.client.isrc_asked == asked


# ═══════════════════════════════════════════════════════════════════════════
# The reverse direction: a sibling release added on the account
# ═══════════════════════════════════════════════════════════════════════════


def _sibling_added(w) -> None:
    """A person adds, on the account, a release of the tied row the link did not take."""
    w.account.playlists[ACCOUNT].append("202")


def _quiet(w) -> dict:
    """One more whole sync, which must write nothing on either side."""
    held, on_account = w.held(), w.on_account()
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert (w.held(), w.on_account()) == (held, on_account)
    return envelope


@pytest.mark.parametrize("on_file", [False, True], ids=["database-isrc", "file-isrc"])
def test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued(
    tied, cfg, tmp_path, on_file
):
    w = tied([release("202"), release("101")])
    if on_file:
        _untagged_row(cfg, TIED, tmp_path, file_isrc=isrc(TIED))
    assert sync(w.args())[0] == int(ExitCode.OK)
    assert w.on_account() == ["101"]
    _sibling_added(w)

    code, envelope = sync([*VERB, ACCOUNT])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert w.held() == [TIED]
    assert w.on_account() == ["101", "202"]
    assert _pair(cfg).links.get("202") == TIED
    _quiet(w)
