"""`board.py residuals --search` finds a finding without printing the ledger (U196).

The search runs for real on a ledger the test writes.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from tests.test_board_reads import load_board


@pytest.fixture
def board():
    return load_board()


LEDGER_TEXT = "# Residual findings\n" + "".join(
    f"\n## R-{n}. {title}\n\nFound: U{n}.\n"
    for n, title in (
        (7, "Label sync reads a failed listing as nothing new"),
        (12, "A tag retag that fails names only the last file"),
        (30, "LABEL SYNC go lands a refused track"),
        (31, "The mirror drops a heart"),
    )
)


@pytest.fixture
def ledger(tmp_path):
    path = tmp_path / "residual-findings.md"
    path.write_text(LEDGER_TEXT)
    return path


@pytest.mark.parametrize(
    ("words", "cap", "found", "more"),
    [
        (["label"], 25, [30, 7], 0),
        (["Sync", "REFUSED"], 25, [30], 0),
        (["bandcamp"], 25, [], 0),
        (["a"], 2, [31, 30], 2),
    ],
)
def test_every_word_must_appear_in_any_case_newest_first(board, ledger, words, cap, found, more):
    hits, rest = board.search_residuals(words, ledger, cap=cap)
    assert [number for number, _ in hits] == found
    assert rest == more


def _search(board, monkeypatch, ledger, words):
    monkeypatch.setattr(board, "LEDGER", ledger)
    monkeypatch.setattr(board, "residual_file_problems", lambda: [])
    return board.cmd_residuals(SimpleNamespace(land=False, search=words))


def test_the_command_prints_hits_and_refuses_an_empty_search(board, ledger, monkeypatch, capsys):
    assert _search(board, monkeypatch, ledger, ["mirror"]) == 0
    out = capsys.readouterr().out
    assert "R-31. The mirror drops a heart" in out
    assert "R-7." not in out
    assert _search(board, monkeypatch, ledger, []) == 2


def test_a_missing_ledger_is_refused_never_read_as_no_match(board, tmp_path, monkeypatch, capsys):
    missing = tmp_path / "residual-findings.md"
    with pytest.raises(FileNotFoundError):
        board.search_residuals(["token"], missing)
    assert _search(board, monkeypatch, missing, ["token"]) == 2
    captured = capsys.readouterr()
    assert "cannot search" in captured.err
    assert "No ledger heading" not in captured.out
