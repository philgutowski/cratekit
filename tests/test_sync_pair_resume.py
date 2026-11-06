"""U210: a sync stopped part way through its write finishes with a continue of the same run.

Driven through ``crate sync pair`` on the disposable databases the sync pair
suites build, with every write the fake account makes sent through a real
provider gate, so ``--calls`` stops the write on the ceiling exactly as it
stops a live one: the dispatcher's own scope, the gate's own park. A plan
made by the first command is held under its run (U209); this file asks what
the run's recorded steps let a continue do after a stop.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import shlex

import pytest

from cratekit.core import held_plan, provider_gate
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_calls, pair_cli
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414

APPLY = ["apply", "--actor", "a-person"]
VERB = ["sync", "pair"]
CEILING = int(ExitCode.REFUSED_BY_POLICY)


class Answer:
    """What the transport answers, as the gate reads its status off it."""

    status_code = 200


class Limited:
    """The provider's rate limit answer, asking for a wait longer than any cooldown."""

    status_code = 429
    headers = {"Retry-After": "100000"}


def gate_the_account(account, monkeypatch, *, limited_on: int | None = None) -> None:
    """Send every write the fake account makes through a real provider gate.

    The fake counts a write in ``_bump`` before it changes anything, so the
    gate is asked first: a call the ceiling refuses is never made and changes
    nothing, which is the gate's own promise for a live call. ``limited_on``
    makes that gated call answer rate limited, writing nothing, which trips
    the gate's cooldown: a park that is not the ceiling.
    """
    gate = provider_gate.Gate(
        provider_gate.GateSettings(min_interval_s=0.0), sleep=lambda seconds: None
    )
    real = account._bump
    made = [0]

    def bump(subject: str = "") -> None:
        def send():
            made[0] += 1
            if made[0] == limited_on:
                return Limited()
            real(subject)
            return Answer()

        gate.call(send)

    monkeypatch.setattr(account, "_bump", bump)


def _gate(envelope) -> str:
    return envelope["cause"]["detail"]["gate"]


def to_the_write(args: list[str], *, calls: int | None = None) -> tuple[str, dict]:
    """Answer both gates apply, one command each. The run id and the first gate's envelope."""
    lead = ["--calls", str(calls)] if calls else []
    code, first = drive([*lead, *args])
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, _gate(first), *APPLY])[0] == int(ExitCode.OK)
    code, second = drive(["--run", run_id, *args])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert drive(["run", "decide", run_id, _gate(second), *APPLY])[0] == int(ExitCode.OK)
    return run_id, first


def write(run_id: str, args: list[str], calls: int) -> tuple[int, dict]:
    return drive(["--calls", str(calls), "--run", run_id, *args])


def _codes(envelope) -> set[str]:
    return {warning["code"] for warning in envelope.get("warnings") or ()}


# ═══════════════════════════════════════════════════════════════════════════
# Many made pairs: the Sitting 54 shape
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def gated(world, monkeypatch):
    """The discovery suite's world, its account's writes sent through a real gate."""
    gate_the_account(world.account, monkeypatch)
    return world


@pytest.fixture
def made_world(gated):
    """Five rekordbox playlists in one folder, each made on the account by the write.

    Each made pair costs three gated writes (make, move, fill) and the folder
    one, so the write is sixteen calls: a ceiling of ten stops it after three
    pairs, on the fourth pair's make.
    """
    world = gated
    folder = world.folder("GIG READY")
    playlists = [world.playlist(f"Set {index}", str(index), under=folder) for index in range(1, 6)]
    return world, playlists


def _made_titles(world) -> list[str]:
    return sorted(world.in_folder("GIG READY"))


def test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run(
    made_world, cfg
):
    world, playlists = made_world
    run_id, _first = to_the_write(VERB)
    listings = world.catalogue.account_listings
    lookups = len(world.account.matches)

    code, stopped = write(run_id, VERB, 10)
    assert code == CEILING, stopped
    assert stopped["cause"]["reason"] == provider_gate.CEILING
    assert len(world.account.created) == 3, world.account.created
    assert world.account._writes == 10

    code, done = write(run_id, VERB, 100)
    assert code == int(ExitCode.OK), done
    # Pairs four and five only: two makes, two moves, two fills.
    assert world.account._writes == 16
    assert len(world.account.created) == 5, "a playlist was made twice"
    assert len(world.account.moves) == 5
    assert _made_titles(world) == [f"GIG READY Set {index}" for index in range(1, 6)]
    for index, rekordbox_id in enumerate(playlists, start=1):
        account_id = world.in_folder("GIG READY")[f"GIG READY Set {index}"]
        assert world.account.playlists[account_id] == [f"t{index}"]
        held = pairs.PairStore(cfg).get(account_id)
        assert held is not None and held.rekordbox_id == rekordbox_id
        assert held.account == (f"t{index}",), "the snapshot did not move"
    # No new plan: the account's playlists were not listed and no track asked.
    assert world.catalogue.account_listings == listings
    assert len(world.account.matches) == lookups
    assert pair_cli.REPLANNED not in _codes(done)
    assert pair_cli.RESUMED in _codes(done)
    assert done["data"]["totals"]["finished_before"] == 3
    assert len(done["data"]["totals"]["created_playlists"]) == 2
    # The run is finished, so its plan and its steps are let go.
    assert not held_plan.path(run_id).exists()
    assert not held_plan.steps_path(run_id).exists()


def test_the_stop_names_the_run_and_the_calls_its_continue_needs(made_world):
    world, _playlists = made_world
    run_id, _first = to_the_write(VERB)
    code, stopped = write(run_id, VERB, 10)
    assert code == CEILING, stopped
    cause = stopped["cause"]
    assert run_id in cause["message"]
    assert "finished 3 of 5 pair(s)" in cause["message"]
    assert cause["detail"]["run_id"] == run_id
    assert cause["detail"]["finished"] == 3
    command = cause["detail"]["continue"]
    words = shlex.split(command)
    assert words[words.index("--run") + 1] == run_id
    higher = int(words[words.index("--calls") + 1])
    assert higher == pair_calls.named(cause["detail"]["expected"], 10)
    assert higher > cause["detail"]["expected"]
    assert cause["remediation"]["steps"][0].endswith(command)
    # The command it names is the one that finishes the run.
    code, done = drive(words[1:])
    assert code == int(ExitCode.OK), done
    assert len(world.account.created) == 5


@pytest.mark.parametrize(
    ("calls", "between"),
    [(2, "the make and the move"), (3, "the move and the fill")],
)
def test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second(
    gated, cfg, calls, between
):
    world = gated
    folder = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", under=folder)
    run_id, _first = to_the_write(VERB)

    code, stopped = write(run_id, VERB, calls)
    assert code == CEILING, (between, stopped)
    assert len(world.account.created) == 1
    made = next(iter(world.account.titles))
    assert world.account.playlists[made] == [], between

    code, done = write(run_id, VERB, 100)
    assert code == int(ExitCode.OK), (between, done)
    assert world.account.created == ["GIG READY Opener"], "a second playlist was made"
    assert world.in_folder("GIG READY") == {"GIG READY Opener": made}, between
    # Moved once: by the stopped command, or by the continue when the stop
    # came before the move, never by both.
    assert len(world.account.moves) == 1, (between, world.account.moves)
    assert world.account.playlists[made] == ["t1", "t2", "t3"]
    held = pairs.PairStore(cfg).get(made)
    assert held is not None and held.rekordbox_id == opener
    assert held.account == ("t1", "t2", "t3")


def test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it(
    gated,
):
    world = gated
    folder = world.folder("GIG READY")
    world.playlist("Opener", "1", "2", under=folder)
    run_id, _first = to_the_write(VERB)
    assert write(run_id, VERB, 3)[0] == CEILING
    made = next(iter(world.account.titles))
    world.account.playlists[made].append("t9")

    code, refused = write(run_id, VERB, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    moved = refused["cause"]["detail"]["moved"]
    assert moved == [
        {
            "side": "account",
            "playlist_id": made,
            "name": "GIG READY Opener",
            "why": "holds 1 track(s) this run neither read nor added since the plan",
        }
    ]
    assert "nothing more was written" in refused["cause"]["message"]
    assert world.account.playlists[made] == ["t9"], "the playlist was written over"


def test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it(made_world):
    world, _playlists = made_world
    run_id, _first = to_the_write(VERB)
    assert write(run_id, VERB, 10)[0] == CEILING
    folder_id = next(fid for fid, name in world.account.folders().items() if name == "GIG READY")
    taken = world.account.create_playlist("GIG READY Set 5")
    world.account.placed[taken] = folder_id
    writes = world.account._writes

    code, refused = write(run_id, VERB, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["why"] for one in refused["cause"]["detail"]["moved"]] == [
        "now holds a playlist titled 'GIG READY Set 5'"
    ]
    assert world.account._writes == writes, "the continue wrote over a moved folder"


# ═══════════════════════════════════════════════════════════════════════════
# The gate's forecast
# ═══════════════════════════════════════════════════════════════════════════


def test_a_gate_whose_ceiling_is_below_the_expected_calls_says_so_with_the_calls_value(
    made_world,
):
    code, first = drive(["--calls", "10", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), first
    shown = first["cause"]["detail"]["shown"]
    run_id = first["run_id"]
    assert "one command may make 10" in shown["provider calls"]
    said = shown["call ceiling"]
    assert said.startswith("too low for this write")
    words = shlex.split(said.split("for example ", 1)[1].split(" once ", 1)[0])
    higher = int(words[words.index("--calls") + 1])
    assert higher > 10
    assert words[words.index("--run") + 1] == run_id
    # The value it names lets the write finish in one command.
    assert drive(["run", "decide", run_id, _gate(first), *APPLY])[0] == int(ExitCode.OK)
    code, second = drive(["--run", run_id, *VERB])
    assert drive(["run", "decide", run_id, _gate(second), *APPLY])[0] == int(ExitCode.OK)
    code, done = write(run_id, VERB, higher)
    assert code == int(ExitCode.OK), done
    assert len(made_world[0].account.created) == 5


def test_a_gate_under_its_ceiling_shows_the_expected_calls_and_no_warning(made_world):
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    shown = first["cause"]["detail"]["shown"]
    assert "the command that writes is expected to make about" in shown["provider calls"]
    assert "call ceiling" not in shown


def test_a_stop_in_a_run_whose_plan_was_not_held_says_it_cannot_be_continued(
    made_world, monkeypatch
):
    """Round one's second finding: no step recorded, so no continue of the run is promised."""
    world, _playlists = made_world
    monkeypatch.setattr(pair_cli, "_hold", lambda *args: "the plan could not be written")
    run_id, _first = to_the_write(VERB)
    code, stopped = write(run_id, VERB, 10)
    assert code == CEILING, stopped
    cause = stopped["cause"]
    assert "cannot be continued" in cause["message"]
    assert "run_id" not in cause["detail"]
    assert "--run" not in shlex.split(cause["detail"]["continue"])
    assert not held_plan.steps_path(run_id).exists()


def test_made_here_reads_only_a_pair_made_for_this_playlist_in_this_folder():
    from cratekit.modules.outbound.pairs import Pair

    one = pair_cli.PairPlan.__new__(pair_cli.PairPlan)
    object.__setattr__(one, "target", pair_cli.Target("", "rb-1", False, "GIG READY", "t"))
    object.__setattr__(one, "place", pair_cli.Place("GIG READY", "t", pair_cli.FOLDER_CREATE))

    def pair(**changed) -> Pair:
        fields = {
            "account_id": "pl-1",
            "rekordbox_id": "rb-1",
            "name": "t",
            "marked": "2026-11-05",
            "made": True,
            "folder": "GIG READY",
        }
        fields.update(changed)
        return Pair(**fields)

    assert pair_cli._made_here(pair(), one)
    assert not pair_cli._made_here(None, one)
    assert not pair_cli._made_here(pair(made=False), one), "a pair made by hand was read as made"
    assert not pair_cli._made_here(pair(rekordbox_id="rb-2"), one)
    assert not pair_cli._made_here(pair(folder="ARCHIVE"), one)


def test_the_forecast_on_a_continue_counts_only_what_is_left(made_world):
    """The first pair made and moved, its fill refused: what the continue is named for."""
    world, _playlists = made_world
    run_id, _first = to_the_write(VERB)
    code, stopped = write(run_id, VERB, 3)
    assert code == CEILING, stopped
    # The check: the made playlist listed with its unpaged read beside it
    # (U226), and the root folders read once.
    check = pair_calls.judged_calls(0) + pair_calls.READ_FOLDER
    # The write: the first pair filled after its membership is read, and the
    # other four made and filled; their folder is made already.
    fill = pair_calls.listing_calls(0) + 1 + 1
    others = 4 * (pair_calls.MAKE_PLAYLIST + 1 + 1)
    assert stopped["cause"]["detail"]["expected"] == check + fill + others


def test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue(made_world):
    """A list the write is done with is the author's again: changed, it stops nothing."""
    world, _playlists = made_world
    run_id, _first = to_the_write(VERB)
    assert write(run_id, VERB, 10)[0] == CEILING
    first = world.in_folder("GIG READY")["GIG READY Set 1"]
    world.account.playlists[first].append("t9")

    code, done = write(run_id, VERB, 100)
    assert code == int(ExitCode.OK), done
    assert world.account.playlists[first] == ["t1", "t9"], "the finished pair was written again"
    assert len(world.account.created) == 5
