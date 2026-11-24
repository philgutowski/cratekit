"""U959: a bare ``crate sync pair`` never pairs a WIP playlist the account mirror already copies. D1 applies."""

from __future__ import annotations

from cratekit.modules.outbound import ledger, mirror
from cratekit.sync import pair_discover
from tests._sync_builders import exited
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair import sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414 - fixture
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414 - fixture

SET = "deep and soulful"


def _mirrored(monkeypatch, *titles: str) -> None:
    """The outbound ledger recording the account mirror's WIP folder holding ``titles``."""
    held = ledger.MirrorFolder(
        name=mirror.WIP, folder_id="mirror-wip", created=True,
        playlists={title: ledger.MirrorPlaylist(name=title, remote_id=f"m-{title}") for title in titles},
    )
    monkeypatch.setattr(ledger, "mirror_folders", lambda _cfg: {mirror.WIP: held})


def test_a_wip_playlist_the_mirror_copies_is_not_paired_and_another_is(world, monkeypatch):
    phil = world.folder("Phil", under=world.folder("WIP "))
    world.playlist(SET, "1", under=phil)
    world.playlist("feelings wip", "2", under=phil)
    _mirrored(monkeypatch, f"Phil {SET}")
    exited(sync())
    made = list(world.in_folder("WIP "))
    assert len(made) == 1 and made[0].endswith("feelings wip")
    assert not any(SET in title for title in world.account.titles.values())


def test_with_nothing_mirrored_every_wip_playlist_is_paired_as_before(world, monkeypatch):
    phil = world.folder("Phil", under=world.folder("WIP "))
    world.playlist(SET, "1", under=phil)
    world.playlist("feelings wip", "2", under=phil)
    monkeypatch.setattr(ledger, "mirror_folders", lambda _cfg: {})
    exited(sync())
    assert len(world.in_folder("WIP ")) == 2


def test_only_a_title_under_wip_is_left_out(world, monkeypatch):
    """A GIG READY playlist whose title the mirror holds under WIP is still paired."""
    world.playlist(SET, "1", under=world.folder("Phil", under=world.folder("GIG READY")))
    _mirrored(monkeypatch, f"Phil {SET}")
    exited(sync())
    assert len(world.in_folder("GIG READY")) == 1


def test_the_titles_are_read_off_the_ledger(monkeypatch, cfg):
    _mirrored(monkeypatch, f"Phil {SET}", "WIP warmup")
    assert pair_discover.mirrored_wip(cfg) == frozenset({f"Phil {SET}", "WIP warmup"})
    monkeypatch.setattr(ledger, "mirror_folders", lambda _cfg: {})
    assert pair_discover.mirrored_wip(cfg) == frozenset()


def test_a_wip_set_the_mirror_copies_after_the_plan_is_never_paired_at_the_answer(world, monkeypatch):
    """The pair check discovers again before it writes: a set the mirror copied since the plan stops the run."""
    from cratekit.core.exit_codes import ExitCode
    from tests.cli_drive import drive
    from tests.test_sync_pair import VERB

    phil = world.folder("Phil", under=world.folder("WIP "))
    world.playlist(SET, "1", under=phil)
    monkeypatch.setattr(ledger, "mirror_folders", lambda _cfg: {})
    code, envelope = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = envelope["run_id"]
    # The mirror ran between the plan and the answer, and copied the set.
    _mirrored(monkeypatch, f"Phil {SET}")
    for _ in range(2):
        gate = envelope["cause"]["detail"]["gate"]
        exited(drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"]))
        code, envelope = drive(["--run", run_id, *VERB])
        if code != int(ExitCode.DECISION_REQUIRED):
            break
    assert (envelope.get("cause") or {}).get("reason") == "decision-stale", envelope
    assert world.account.created == []
    assert not any(SET in title for title in world.account.titles.values())
