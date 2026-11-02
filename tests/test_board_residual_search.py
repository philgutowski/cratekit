"""`board.py residuals --search` finds a finding without printing the ledger (U196).

Filing a card checked for a duplicate by printing every `## R-` heading, over a
thousand of them by 2026-11-02. The search runs for real on a ledger the test writes.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

BOARD = Path(__file__).resolve().parent.parent / "scripts" / "board.py"

LEDGER_TEXT = """# Residual findings

## R-7. Label sync reads a failed listing as nothing new

Found: U1.

## R-12. A tag retag that fails names only the last file

Found: U2.

## R-30. LABEL SYNC go lands a refused track

Found: U3.

## R-31. The mirror drops a heart

Found: U4.
"""


@pytest.fixture
def board():
    spec = importlib.util.spec_from_file_location("board_search_under_test", BOARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def ledger(tmp_path):
    path = tmp_path / "residual-findings.md"
    path.write_text(LEDGER_TEXT)
    return path


def test_one_word_finds_every_heading_carrying_it_newest_first(board, ledger):
    hits, more = board.search_residuals(["label"], ledger)
    assert [number for number, _ in hits] == [30, 7]
    assert more == 0


def test_every_word_must_appear_in_any_case(board, ledger):
    hits, _ = board.search_residuals(["Sync", "REFUSED"], ledger)
    assert hits == [(30, "LABEL SYNC go lands a refused track")]


def test_no_match_is_empty(board, ledger):
    assert board.search_residuals(["bandcamp"], ledger) == ([], 0)


def test_past_the_cap_it_counts_the_rest(board, ledger):
    hits, more = board.search_residuals(["a"], ledger, cap=2)
    assert len(hits) == 2
    assert more == 2


def test_the_command_prints_hits_and_refuses_an_empty_search(board, ledger, monkeypatch, capsys):
    monkeypatch.setattr(board, "LEDGER", ledger)
    monkeypatch.setattr(board, "residual_file_problems", lambda: [])
    args = SimpleNamespace(land=False, search=["mirror"])
    assert board.cmd_residuals(args) == 0
    out = capsys.readouterr().out
    assert "R-31. The mirror drops a heart" in out
    assert "R-7." not in out
    args = SimpleNamespace(land=False, search=[])
    assert board.cmd_residuals(args) == 2


def test_a_missing_ledger_is_refused_never_read_as_no_match(board, tmp_path, monkeypatch, capsys):
    missing = tmp_path / "residual-findings.md"
    with pytest.raises(FileNotFoundError):
        board.search_residuals(["token"], missing)
    monkeypatch.setattr(board, "LEDGER", missing)
    assert board.cmd_residuals(SimpleNamespace(land=False, search=["token"])) == 2
    captured = capsys.readouterr()
    assert "cannot search" in captured.err
    assert "No ledger heading" not in captured.out
