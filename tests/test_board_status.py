"""What `scripts/board.py` derives for a card somebody holds right now.

The relay runner moves each card it starts to In review, and a lane's builder
moves each card it starts to In Progress. Neither status can be derived from the
graph, so `audit` reading either as drift is a false exit 1 on every in flight
card, and `sync` acting on it pulls a card out from under its build (U122).

The board's own issues are fed in as data through `build_graph`, so every node
here has the shape the real reconcile hands `derive_status`. Nothing touches the
network: `cmd_next` runs with its three readers replaced.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

BOARD = Path(__file__).resolve().parent.parent / "scripts" / "board.py"


@pytest.fixture(scope="module")
def board():
    """Loaded by path, as `test_pending_units` does, because it is a script."""
    spec = importlib.util.spec_from_file_location("board_status_under_test", BOARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _issue(number, title, *, labels=(), state="OPEN", body="**Depends on:** none"):
    return {
        "number": number,
        "title": title,
        "state": state,
        "body": body,
        "labels": [{"name": name} for name in labels],
    }


def _graph(board):
    return board.build_graph(
        [
            _issue(1, "U1: a foundation", labels=["unit"]),
            _issue(2, "U2: on the foundation", labels=["unit"], body="**Depends on:** #1"),
            _issue(3, "U3: landed", labels=["unit"], state="CLOSED"),
            _issue(4, "R-4: a residual nothing closes", labels=["residual"], body=""),
            _issue(
                5,
                "R-5: a residual U1 closes",
                labels=["residual"],
                body="**Closes with:** #1",
            ),
            _issue(6, "R-6: a residual already closed", labels=["residual"], state="CLOSED"),
            _issue(7, "U7: attended", labels=["unit", "attended"]),
        ]
    )


@pytest.mark.parametrize("held", ["In Progress", "In review"])
def test_an_open_unit_somebody_holds_keeps_the_status_it_holds(board, held):
    graph = _graph(board)
    assert graph[1]["open_deps"] == []
    assert board.derive_status(graph[1], held) == held
    # and one still waiting on a dependency, which a lane could hold all the same
    assert graph[2]["open_deps"] == [1]
    assert board.derive_status(graph[2], held) == held


@pytest.mark.parametrize("held", ["In Progress", "In review"])
@pytest.mark.parametrize("number", [4, 5])
def test_an_open_residual_somebody_holds_keeps_the_status_it_holds(board, held, number):
    """Amended 2026-10-09: a lane builds residual cards, #262 to #264 on the Grok lane."""
    assert board.derive_status(_graph(board)[number], held) == held


@pytest.mark.parametrize("held", ["In Progress", "In review", "Ready", None])
@pytest.mark.parametrize("number", [3, 6])
def test_a_closed_card_is_done_whatever_it_held(board, held, number):
    assert board.derive_status(_graph(board)[number], held) == "Done"


@pytest.mark.parametrize("held", ["In Progress", "In review"])
def test_an_attended_card_somebody_holds_keeps_the_hold(board, held):
    """An attended unit is still built, by a person, and its hold is just as real."""
    assert board.derive_status(_graph(board)[7], held) == held


@pytest.mark.parametrize("current", ["Ready", "Blocked", None])
def test_an_attended_card_nobody_holds_is_attended(board, current):
    assert board.derive_status(_graph(board)[7], current) == "Attended"


@pytest.mark.parametrize("current", ["Ready", "Blocked", "Done", None])
def test_a_card_nobody_holds_is_derived_from_the_graph(board, current):
    graph = _graph(board)
    assert board.derive_status(graph[1], current) == "Ready"
    assert board.derive_status(graph[2], current) == "Blocked"
    assert board.derive_status(graph[4], current) == "Ready"
    assert board.derive_status(graph[5], current) == "Blocked"


@pytest.mark.parametrize("held", ["In Progress", "In review"])
def test_next_lists_a_held_card_as_busy_and_never_offers_it(board, monkeypatch, capsys, held):
    issues = [
        _issue(10, "U10: held by the runner", labels=["unit"]),
        _issue(11, "U11: nobody has it", labels=["unit"]),
    ]
    monkeypatch.setattr(board, "repo_slug", lambda: ("owner", "repo"))
    monkeypatch.setattr(board, "load_issues", lambda: issues)
    monkeypatch.setattr(
        board,
        "project_items",
        lambda owner: {10: {"id": "a", "status": held}, 11: {"id": "b", "status": "Ready"}},
    )

    assert board.cmd_next(None) == 0
    out = capsys.readouterr().out
    busy, _, ready = out.partition("Ready now")
    assert f"#10  {held}" in busy
    assert "#10" not in ready
    assert "#11" in ready
    assert "Take #11." in ready
