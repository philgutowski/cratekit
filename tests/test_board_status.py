"""What `scripts/board.py` derives for a card somebody holds right now (U122).

In review (the relay runner) and In Progress (a builder) are holds no graph
derives, so neither may read as drift.
"""

from __future__ import annotations

import pytest

from tests.test_board_reads import RESIDUAL, issue
from tests.test_board_reads import board as board  # noqa: PLC0414

HELD = ["In Progress", "In review"]


def _graph(board):
    return board.build_graph([
        issue(1, "U1: a foundation"),
        issue(2, "U2: on the foundation", body="**Depends on:** #1"),
        issue(3, "U3: landed", state="CLOSED"),
        issue(4, "R-4: a residual nothing closes", labels=[RESIDUAL], body=""),
        issue(5, "R-5: a residual U1 closes", labels=[RESIDUAL], body="**Closes with:** #1"),
        issue(6, "R-6: a residual already closed", labels=[RESIDUAL], state="CLOSED"),
        issue(7, "U7: attended", labels=["unit", "attended"]),
    ])


@pytest.mark.parametrize("held", HELD)
@pytest.mark.parametrize("number", [1, 2, 4, 5, 7])
def test_an_open_card_somebody_holds_keeps_the_status_it_holds(board, held, number):
    """Units, residuals (a lane builds those too) and attended units alike."""
    graph = _graph(board)
    assert (graph[1]["open_deps"], graph[2]["open_deps"]) == ([], [1])
    assert board.derive_status(graph[number], held) == held


@pytest.mark.parametrize("held", [*HELD, "Ready", None])
@pytest.mark.parametrize("number", [3, 6])
def test_a_closed_card_is_done_whatever_it_held(board, held, number):
    assert board.derive_status(_graph(board)[number], held) == "Done"


@pytest.mark.parametrize("current", ["Ready", "Blocked", "Done", None])
def test_a_card_nobody_holds_is_derived_from_the_graph(board, current):
    graph = _graph(board)
    derived = {n: board.derive_status(graph[n], current) for n in (1, 2, 4, 5, 7)}
    assert derived == {1: "Ready", 2: "Blocked", 4: "Ready", 5: "Blocked", 7: "Attended"}


@pytest.mark.parametrize("held", HELD)
def test_next_lists_a_held_card_as_busy_and_never_offers_it(board, monkeypatch, capsys, held):
    issues = [issue(10, "U10: held by the runner"), issue(11, "U11: nobody has it")]
    monkeypatch.setattr(board, "repo_slug", lambda: ("owner", "repo"))
    monkeypatch.setattr(board, "load_issues", lambda: issues)
    monkeypatch.setattr(board, "project_context", lambda owner: {})
    items = {10: {"id": "a", "status": held}, 11: {"id": "b", "status": "Ready"}}
    monkeypatch.setattr(board, "project_items", lambda owner: items)
    assert board.cmd_next(None) == 0
    busy, _, ready = capsys.readouterr().out.partition("Ready now")
    assert f"#10  {held}" in busy
    assert "#10" not in ready
    assert "#11" in ready
    assert "Take #11." in ready
