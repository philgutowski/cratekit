"""`scripts/board.py` reads every issue and project item, or refuses (U148).

Both reads asked `gh` for at most 300 rows. The project passed 300 items on
2026-10-13 and every newer card read as "not on the board" with no status, a
drift no sync could repair because the next read dropped the same cards.

The double here is `gh` itself, at the one boundary a test cannot cross, and it
behaves the way the real one does: it pages internally and returns at most
`--limit` rows, silently. Everything downstream, `load_issues`, `project_items`
and `reconcile`, runs for real on what it serves.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

# A label name, held in a constant so no quoted string follows the word in the
# source, which the citation rule in test_reserved_causes reads as a title.
RESIDUAL = "residual"

BOARD = Path(__file__).resolve().parent.parent / "scripts" / "board.py"

ISSUES = 330
ITEMS = 316


@pytest.fixture
def board():
    """Loaded fresh per test by path, because each test replaces its `gh`."""
    spec = importlib.util.spec_from_file_location("board_reads_under_test", BOARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _issues(count: int) -> list[dict]:
    """Open and closed residual issues, so every status derives without labels."""
    return [
        {
            "number": n,
            "title": f"R-{n}: finding {n}",
            "state": "CLOSED" if n % 2 else "OPEN",
            "body": "",
            "labels": [{"name": RESIDUAL}],
        }
        for n in range(1, count + 1)
    ]


def _items(issues: list[dict], count: int) -> list[dict]:
    """The first `count` issues on the project, each with its derived status set."""
    return [
        {
            "id": f"item-{issue['number']}",
            "status": "Done" if issue["state"] == "CLOSED" else "Ready",
            "content": {"number": issue["number"]},
        }
        for issue in issues[:count]
    ]


def _fake_gh(issues: list[dict], items: list[dict], *, total: int | None = None):
    """A `gh` that honours `--limit` the way the real one does, by cutting short."""
    calls: list[tuple[str, ...]] = []

    def gh(*args: str, parse: bool = False):
        calls.append(args)
        limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
        if args[:2] == ("issue", "list"):
            return issues[:limit]
        if args[:2] == ("project", "item-list"):
            served = items[:limit]
            return {"items": served, "totalCount": len(items) if total is None else total}
        if args[:2] == ("project", "field-list"):
            options = [{"name": s, "id": s} for s in ("Ready", "Done", "Blocked")]
            return {"fields": [{"name": "Status", "id": "status", "options": options}]}
        if args[:2] == ("project", "view"):
            return {"id": "project", "url": "https://example.invalid/project"}
        if args[:2] == ("repo", "view"):
            return {"owner": {"login": "owner"}, "name": "repo"}
        raise AssertionError(f"the fake gh was not expecting {args}")

    gh.calls = calls
    return gh


def test_every_issue_and_project_item_is_read_past_three_hundred(board, monkeypatch):
    issues = _issues(ISSUES)
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _items(issues, ITEMS)))

    assert [i["number"] for i in board.load_issues()] == list(range(1, ISSUES + 1))
    assert sorted(board.project_items("owner")) == list(range(1, ITEMS + 1))


def test_the_audit_reads_an_item_past_three_hundred_as_on_the_board(board, monkeypatch):
    """Only the issues genuinely missing from the project are reported missing."""
    issues = _issues(ISSUES)
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _items(issues, ITEMS)))

    drift = board.reconcile("owner", apply=False)

    missing = sorted(int(line.split()[0][1:]) for line in drift if "is not on the board" in line)
    assert missing == list(range(ITEMS + 1, ISSUES + 1))
    assert len(drift) == ISSUES - ITEMS, drift


def test_the_old_three_hundred_limit_is_what_lost_them(board, monkeypatch):
    """The control: the same fake under the old limit cannot read the board whole."""
    issues = _issues(ISSUES)
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _items(issues, ITEMS)))
    monkeypatch.setattr(board, "READ_LIMIT", 300)

    with pytest.raises(board.Truncated, match="issue read returned 300 rows"):
        board.load_issues()
    with pytest.raises(board.Truncated, match="project item read returned 300 rows"):
        board.project_items("owner")


@pytest.mark.parametrize("limit", [ITEMS, ITEMS - 1])
def test_a_read_that_fills_the_limit_is_refused_by_name(board, monkeypatch, limit):
    """A full page is a truncated read, even when it happens to be everything."""
    issues = _issues(ITEMS)
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _items(issues, ITEMS)))
    monkeypatch.setattr(board, "READ_LIMIT", limit)

    with pytest.raises(board.Truncated, match=f"the whole limit of {limit}"):
        board.load_issues()
    with pytest.raises(board.Truncated, match=f"the whole limit of {limit}"):
        board.project_items("owner")


def test_one_row_under_the_limit_is_taken_as_whole(board, monkeypatch):
    issues = _issues(ITEMS)
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _items(issues, ITEMS)))
    monkeypatch.setattr(board, "READ_LIMIT", ITEMS + 1)

    assert len(board.load_issues()) == ITEMS
    assert len(board.project_items("owner")) == ITEMS


def test_items_short_of_the_projects_own_count_are_refused(board, monkeypatch):
    """The project's totalCount checks the read without trusting the limit."""
    issues = _issues(ITEMS)
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _items(issues, ITEMS), total=ITEMS + 1))

    with pytest.raises(board.Truncated, match=f"returned {ITEMS} of the {ITEMS + 1} items"):
        board.project_items("owner")


def test_both_reads_ask_gh_for_the_limit(board, monkeypatch):
    issues = _issues(3)
    fake = _fake_gh(issues, _items(issues, 3))
    monkeypatch.setattr(board, "gh", fake)

    board.load_issues()
    board.project_items("owner")

    limits = [call[call.index("--limit") + 1] for call in fake.calls]
    assert limits == [str(board.READ_LIMIT)] * 2


def test_next_refuses_a_truncated_item_read_rather_than_blame_the_token(
    board, monkeypatch, capsys
):
    """`next` reads a failed item read as a token problem; a truncation is not one."""
    monkeypatch.setattr(board, "repo_slug", lambda: ("owner", "repo"))
    monkeypatch.setattr(board, "load_issues", lambda: _issues(2))

    def truncated(owner):
        raise board.Truncated("cut short")

    monkeypatch.setattr(board, "project_items", truncated)
    with pytest.raises(board.Truncated):
        board.cmd_next(None)
    assert "cannot read the project board with this token" not in capsys.readouterr().out


def test_next_still_names_a_token_that_cannot_read_the_board(board, monkeypatch, capsys):
    monkeypatch.setattr(board, "repo_slug", lambda: ("owner", "repo"))
    monkeypatch.setattr(board, "load_issues", lambda: _issues(2))

    def refused(owner):
        raise board.Fail("token cannot reach the project")

    monkeypatch.setattr(board, "project_items", refused)
    assert board.cmd_next(None) == 0
    assert "cannot read the project board with this token" in capsys.readouterr().out
