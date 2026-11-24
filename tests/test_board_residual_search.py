"""`board.py residuals --search` finds a finding without printing the ledger (U196).

The search runs for real on a ledger the test writes, and across its archive
files in `docs/ledger/` (U314).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from tests.test_board_reads import board as board  # noqa: PLC0414

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
    assert [number for number, _, _ in hits] == found
    assert {path for _, _, path in hits} <= {ledger}
    assert rest == more


def _search(board, monkeypatch, ledger, words):
    monkeypatch.setattr(board, "LEDGER", ledger)
    monkeypatch.setattr(board, "residual_file_problems", lambda: [])
    return board.cmd_residuals(SimpleNamespace(land=False, search=words))


def test_the_command_prints_hits_and_refuses_an_empty_search(board, ledger, monkeypatch, capsys):
    assert _search(board, monkeypatch, ledger, ["mirror"]) == 0
    out = capsys.readouterr().out
    assert f"R-31. The mirror drops a heart  ({ledger.relative_to(ledger.parent.parent)})" in out
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


def _archived(tmp_path):
    """The oldest finding and a middle one in two archives, the newest in the working file."""
    archives = tmp_path / "docs" / "ledger"
    archives.mkdir(parents=True)
    for name, entries in (
        ("R-0001-R-0002.md", ((1, "The oldest token leak"), (2, "A heart is dropped"))),
        ("R-0003-R-0004.md", ((3, "A middle token expiry"), (4, "Sync reads nothing"))),
    ):
        (archives / name).write_text(
            "# Residual findings, archived\n"
            + "".join(f"\n---\n\n## R-{n}. {title}\n\nFound: U{n}.\n" for n, title in entries)
        )
    ledger = tmp_path / "docs" / "residual-findings.md"
    ledger.write_text("# Residual findings\n\n---\n\n## R-5. The newest token refresh\n\nBody.\n")
    return ledger


def test_a_search_reads_every_archive_and_says_where_each_hit_is(board, tmp_path, monkeypatch, capsys):
    ledger = _archived(tmp_path)
    hits, _ = board.search_residuals(["TOKEN"], ledger)
    assert [(number, path.name) for number, _, path in hits] == [
        (5, "residual-findings.md"), (3, "R-0003-R-0004.md"), (1, "R-0001-R-0002.md"),
    ]
    assert _search(board, monkeypatch, ledger, ["token"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "R-5. The newest token refresh  (docs/residual-findings.md)",
        "R-3. A middle token expiry  (docs/ledger/R-0003-R-0004.md)",
        "R-1. The oldest token leak  (docs/ledger/R-0001-R-0002.md)",
    ]
    assert board.residual_titles(ledger) == {
        1: "The oldest token leak", 2: "A heart is dropped", 3: "A middle token expiry",
        4: "Sync reads nothing", 5: "The newest token refresh",
    }
