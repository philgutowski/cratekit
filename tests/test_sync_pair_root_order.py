"""R-1404 and R-1416: a pair whose account order is not kept keeps rekordbox's order.

Since U231 a pair whose rekordbox playlist is not under GIG READY never has
its account order written, so once rekordbox leads a reorder the pair's
snapshot holds rekordbox's new order and the account's old one. The merge let
the account lead whenever neither side had changed order since that snapshot,
so the sync after the reorder put the account's old order back into rekordbox
with nothing said. Driven through the dispatcher on the disposable database:
a pair made by hand of an account playlist and a rekordbox playlist at the
root, with ``outbound.pair_order_every_pair`` off, as a DJ's library has it.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from dataclasses import replace

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair import ACCOUNT, VERB, _codes, sync
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import world as world  # noqa: PLC0414


def _kept(monkeypatch, w, *, every: bool) -> None:
    """Set ``outbound.pair_order_every_pair`` for every later run of the verb."""
    w.cfg = replace(w.cfg, outbound=replace(w.cfg.outbound, pair_order_every_pair=every))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: w.cfg)


def _at_the_root(world, monkeypatch, *tracks: str):
    """A hand pair at the rekordbox root whose account order is not kept, synced once."""
    w = world(account=tracks, rekordbox=tracks)
    _kept(monkeypatch, w, every=False)
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    return w


def _again(w):
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    return envelope


def test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync(world, monkeypatch, cfg):
    """The brief's scenario: the reorder is never put back to the account's older order."""
    w = _at_the_root(world, monkeypatch, "1", "2", "3")
    w.rekordbox_order("3", "1", "2")
    envelope = _again(w)
    assert pair_cli.NOTHING in _codes(envelope), envelope
    assert w.held() == ["3", "1", "2"]
    assert w.on_account() == ["t1", "t2", "t3"], "the account order was written outside GIG READY"
    for _ in range(2):
        envelope = _again(w)
        assert w.held() == ["3", "1", "2"], "the account's older order was put back into rekordbox"
        assert w.on_account() == ["t1", "t2", "t3"]
        assert pair_cli.NOTHING in _codes(envelope), envelope
    held = pairs.PairStore(cfg).get(ACCOUNT)
    assert held is not None
    assert [member.content_id for member in held.rekordbox] == ["3", "1", "2"]


def test_an_account_reorder_still_leads_rekordbox_outside_gig_ready(world, monkeypatch):
    """U231's product call: rekordbox still takes an order the account leads with."""
    w = _at_the_root(world, monkeypatch, "1", "2", "3")
    w.rekordbox_order("3", "1", "2")
    _again(w)
    _again(w)
    w.account.playlists[ACCOUNT] = ["t2", "t3", "t1"]
    _again(w)
    assert w.held() == ["2", "3", "1"]
    assert w.on_account() == ["t2", "t3", "t1"]
    _again(w)
    assert w.held() == ["2", "3", "1"]


def test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place(world, monkeypatch):
    """A rekordbox addition put mid playlist goes to the account's end and must stay put in rekordbox."""
    w = _at_the_root(world, monkeypatch, "1", "2", "3")
    w.rekordbox_add("4")
    w.rekordbox_order("1", "4", "2", "3")
    _again(w)
    assert w.held() == ["1", "4", "2", "3"]
    assert w.on_account() == ["t1", "t2", "t3", "t4"]
    for _ in range(2):
        _again(w)
        assert w.held() == ["1", "4", "2", "3"], "the account's appended order was put back"


def test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order(world, monkeypatch):
    """With rekordbox's order standing, a track the account adds still lands after its neighbour."""
    w = _at_the_root(world, monkeypatch, "1", "2", "3")
    w.rekordbox_order("3", "1", "2")
    _again(w)
    w.account.playlists[ACCOUNT] = ["t1", "t5", "t2", "t3"]
    _again(w)
    assert w.held() == ["3", "1", "5", "2"]
    assert w.on_account() == ["t1", "t5", "t2", "t3"]
    _again(w)
    assert w.held() == ["3", "1", "5", "2"]


def test_a_pair_whose_order_is_kept_later_takes_rekordbox_s_order_onto_the_account(
    world, monkeypatch
):
    """A pair that diverged outside the scope and is then kept puts the account in rekordbox's order."""
    w = _at_the_root(world, monkeypatch, "1", "2", "3")
    w.rekordbox_order("3", "1", "2")
    _again(w)
    _kept(monkeypatch, w, every=True)
    _again(w)
    assert w.held() == ["3", "1", "2"], "the account's older order was put back into rekordbox"
    assert w.on_account() == ["t3", "t1", "t2"]


def test_a_pair_whose_order_is_kept_still_follows_a_rekordbox_reorder(world, monkeypatch):
    """Inside the scope nothing changes: the account follows, and the next sync plans nothing."""
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_order("3", "1", "2")
    _again(w)
    assert w.on_account() == ["t3", "t1", "t2"]
    envelope = _again(w)
    assert pair_cli.NOTHING in _codes(envelope), envelope
    assert w.held() == ["3", "1", "2"]


# ═══════════════════════════════════════════════════════════════════════════
# R-1416: a hand pair's first sync outside GIG READY keeps rekordbox's order
# ═══════════════════════════════════════════════════════════════════════════
#
# Decided by Phillip on #608 (608-outside-order-2): outside GIG READY Tidal's
# order is never written (U231), so a first sync that put rekordbox in Tidal's
# order lost the DJ's arrangement for good. The first sync keeps the order
# rekordbox stands in; a later Tidal reorder still brings Tidal's whole order
# (608-outside-order-1).


def _paired(world, monkeypatch, *, account, rekordbox, every: bool = False):
    """A hand pair at the rekordbox root, not yet synced, with the key as asked."""
    w = world(account=account, rekordbox=rekordbox)
    _kept(monkeypatch, w, every=every)
    return w


def _line(w) -> str:
    """The pair's gate line on its first sync, read before anything is answered."""
    code, envelope = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    return envelope["cause"]["detail"]["shown"][f"pair {ACCOUNT}"]


def test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order(world, monkeypatch):
    """The brief's scenario: Tidal 1, 2, 3 and rekordbox 3, 1, 2, each left as it stands."""
    w = _paired(world, monkeypatch, account=("1", "2", "3"), rekordbox=("3", "1", "2"))
    line = _line(w)
    assert "first sync, additions only" in line, line
    assert "order follows rekordbox's" in line, line
    assert "order follows the account's" not in line, line
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["3", "1", "2"], "the first sync put rekordbox in Tidal's order"
    assert w.on_account() == ["t1", "t2", "t3"], "the account order was written outside GIG READY"
    envelope = _again(w)
    assert pair_cli.NOTHING in _codes(envelope), envelope
    assert w.held() == ["3", "1", "2"]
    assert w.on_account() == ["t1", "t2", "t3"]


def test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order(
    world, monkeypatch
):
    """Track 4 follows 3 on Tidal, so it lands after 3 and the rest keep rekordbox's order."""
    w = _paired(world, monkeypatch, account=("1", "2", "3", "4"), rekordbox=("3", "1", "2"))
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["3", "4", "1", "2"]
    assert w.on_account() == ["t1", "t2", "t3", "t4"]
    envelope = _again(w)
    assert pair_cli.NOTHING in _codes(envelope), envelope
    assert w.held() == ["3", "4", "1", "2"]


def test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves(
    world, monkeypatch
):
    w = _paired(world, monkeypatch, account=("1", "2", "3"), rekordbox=("3", "5", "1", "2"))
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["3", "5", "1", "2"]
    assert w.on_account() == ["t1", "t2", "t3", "t5"]
    envelope = _again(w)
    assert pair_cli.NOTHING in _codes(envelope), envelope
    assert w.held() == ["3", "5", "1", "2"]
    assert w.on_account() == ["t1", "t2", "t3", "t5"]


def test_a_hand_pairs_first_sync_with_every_pairs_order_kept_follows_tidal(world, monkeypatch):
    """With ``outbound.pair_order_every_pair`` on the first sync follows Tidal, as it always has."""
    w = _paired(
        world, monkeypatch, account=("1", "2", "3"), rekordbox=("3", "1", "2"), every=True
    )
    line = _line(w)
    assert "order follows the account's" in line, line
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2", "3"]
    assert w.on_account() == ["t1", "t2", "t3"]


def test_an_empty_rekordbox_playlist_paired_by_hand_is_planned_as_before(world, monkeypatch):
    """Nothing in rekordbox to keep: it takes Tidal's tracks in Tidal's order, the gate as before."""
    w = _paired(world, monkeypatch, account=("3", "1", "2"), rekordbox=())
    line = _line(w)
    assert "order follows the account's" in line, line
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["3", "1", "2"]
    assert w.on_account() == ["t3", "t1", "t2"]


def test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands(
    world, monkeypatch
):
    """608-outside-order-1: a Tidal reorder brings Tidal's whole order; a rekordbox one stays."""
    w = _paired(world, monkeypatch, account=("1", "2", "3"), rekordbox=("3", "1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t2", "t3", "t1"]
    _again(w)
    assert w.held() == ["2", "3", "1"], "a Tidal reorder after the first sync was not taken"
    assert w.on_account() == ["t2", "t3", "t1"]
    w.rekordbox_order("1", "3", "2")
    for _ in range(2):
        _again(w)
        assert w.held() == ["1", "3", "2"], "a rekordbox reorder after the first sync was put back"
        assert w.on_account() == ["t2", "t3", "t1"]
