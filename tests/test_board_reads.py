"""`scripts/board.py` reads every issue and project item, or refuses (U148).

The double is `gh`, which returns at most `--limit` rows silently and serves the
cards as GraphQL pages of the issues' memberships. The other board tests share
this file's loader and doubles.
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
STATUSES = ["Ready", "In Progress", "In review", "Blocked", "Attended", "Done"]
#: Leaves a count as the true one, as distinct from None, which drops the key.
TRUE = object()


def load_board(name: str = "board"):
    """A fresh script, `scripts/board.py` by default, loaded by path."""
    spec = importlib.util.spec_from_file_location(f"{name}_under_test", BOARD.parent / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def issue(number, title, *, labels=("unit",), state="OPEN", body="**Depends on:** none"):
    labels = [{"name": name} for name in labels]
    return {"number": number, "title": title, "state": state, "body": body, "labels": labels}


@pytest.fixture
def board():
    return load_board()


def _issues(count: int) -> list[dict]:
    return [
        issue(n, f"R-{n}: finding {n}", labels=[RESIDUAL], body="",
              state="CLOSED" if n % 2 else "OPEN")
        for n in range(1, count + 1)
    ]


def _items(issues: list[dict], count: int) -> list[dict]:
    return [
        {"id": f"item-{i['number']}", "number": i["number"],
         "status": "Done" if i["state"] == "CLOSED" else "Ready"}
        for i in issues[:count]
    ]


def _membership(item: dict, *, number: int = 2, login: str = "owner") -> dict:
    unblocks = item.get("unblocks")
    return {
        "id": item["id"],
        "project": {"number": number, "owner": {"login": login}},
        "status": {"name": item["status"]} if item.get("status") else None,
        "unblocks": None if unblocks is None else {"number": float(unblocks)},
    }


def _card_page(issues, by_number, extra, args, total):
    start = int(next((a.split("=", 1)[1] for a in args if a.startswith("after=")), "0"))
    nodes = []
    for row in issues[start:start + 100]:
        cards = [_membership(by_number[row["number"]])] if row["number"] in by_number else []
        cards += extra.get(row["number"], [])
        nodes.append({"number": row["number"],
                      "projectItems": {"totalCount": len(cards), "nodes": cards}})
    more = start + 100 < len(issues)
    served = {
        "totalCount": len(issues) if total is TRUE else total,
        "pageInfo": {"hasNextPage": more, "endCursor": str(start + 100) if more else None},
        "nodes": nodes,
    }
    if total is None:
        del served["totalCount"]
    return {"data": {"repository": {"issues": served}}}


def _fake_gh(issues: list[dict], items: list[dict], *, total=TRUE, issue_total=TRUE, extra=None):
    """A `gh` that honours `--limit` by cutting short and pages the cards by cursor.

    `extra` maps an issue number to further memberships, another project's or
    another owner's.
    """
    calls: list[tuple[str, ...]] = []
    by_number = {item["number"]: item for item in items}

    def gh(*args: str, parse: bool = False):
        calls.append(args)
        query = " ".join(args)
        graphql = args[:2] == ("api", "graphql")
        if graphql and "issues { totalCount }" in query:
            # `--jq` prints the bare count, and `gh` hands back text
            return str(len(issues) if issue_total is TRUE else issue_total)
        if graphql and "projectItems" in query:
            return _card_page(issues, by_number, extra or {}, args, total)
        if graphql and "projectV2(number" in query:
            fields = [
                {"name": "Status", "id": "status",
                 "options": [{"name": s, "id": s} for s in STATUSES]},
                {"name": "Unblocks", "id": "unblocks"},
            ]
            kind = "organization" if "organization(login" in query else "user"
            project = {"id": "project", "url": "https://example.invalid/project",
                       "fields": {"totalCount": len(fields), "nodes": fields}}
            return {"data": {kind: {"projectV2": project}}}
        if args[:2] == ("issue", "list"):
            return issues[:int(args[args.index("--limit") + 1])]
        if args[:2] == ("project", "item-add"):
            return {"id": "item-added"}
        if args[:2] in (("project", "item-edit"), ("issue", "edit")):
            return ""
        if args[:2] == ("repo", "view"):
            return {"owner": {"login": "owner"}, "name": "repo"}
        raise AssertionError(f"the fake gh was not expecting {args}")

    gh.calls = calls
    return gh


def _serve(board, monkeypatch, count=ISSUES, items=ITEMS, **options):
    issues = _issues(count)
    fake = _fake_gh(issues, _items(issues, items), **options)
    monkeypatch.setattr(board, "gh", fake)
    return fake


def test_every_issue_and_project_item_is_read_past_three_hundred(board, monkeypatch):
    _serve(board, monkeypatch)
    assert [i["number"] for i in board.load_issues()] == list(range(1, ISSUES + 1))
    assert sorted(board.project_items("owner")) == list(range(1, ITEMS + 1))
    # Only the issues genuinely missing from the project are reported missing.
    drift = board.reconcile("owner", apply=False)
    missing = sorted(int(line.split()[0][1:]) for line in drift if "is not on the board" in line)
    assert missing == list(range(ITEMS + 1, ISSUES + 1))
    assert len(drift) == ISSUES - ITEMS, drift


@pytest.mark.parametrize(
    ("limit", "count", "says"),
    [
        (300, ISSUES, "issue read returned 300 rows"),  # the old limit is what lost them
        (ITEMS, ITEMS, f"the whole limit of {ITEMS}"),
        (ITEMS - 1, ITEMS, f"the whole limit of {ITEMS - 1}"),
    ],
)
def test_a_read_that_fills_the_limit_is_refused_by_name(board, monkeypatch, limit, count, says):
    """A full page is a truncated read, even when it happens to be everything."""
    _serve(board, monkeypatch, count=count)
    monkeypatch.setattr(board, "READ_LIMIT", limit)
    with pytest.raises(board.Truncated, match=says):
        board.load_issues()


def test_one_row_under_the_limit_is_taken_as_whole(board, monkeypatch):
    _serve(board, monkeypatch, count=ITEMS)
    monkeypatch.setattr(board, "READ_LIMIT", ITEMS + 1)
    assert len(board.load_issues()) == ITEMS
    assert len(board.project_items("owner")) == ITEMS


@pytest.mark.parametrize(
    ("options", "read", "says"),
    [
        ({"total": ITEMS + 1}, "project_items", f"returned {ITEMS} of the {ITEMS + 1} GitHub"),
        ({"total": None}, "project_items", "no count to check it against"),
        ({"issue_total": ITEMS + 1}, "load_issues", f"returned {ITEMS} of the {ITEMS + 1} GitHub"),
        ({"issue_total": "null"}, "load_issues", "no count to check it against"),
    ],
)
def test_a_read_short_of_its_count_or_with_none_is_refused(board, monkeypatch, options, read, says):
    """The count checks every read; no count means no check, never a whole read."""
    _serve(board, monkeypatch, count=ITEMS, **options)
    with pytest.raises(board.Truncated, match=says):
        getattr(board, read)(*(["owner"] if read == "project_items" else []))


def test_issues_filed_after_the_count_are_read_and_not_refused(board, monkeypatch):
    """The count comes first, so a newer issue lengthens the read past it."""
    fake = _serve(board, monkeypatch, issue_total=ISSUES - 2)
    assert len(board.load_issues()) == ISSUES
    assert [call[:2] for call in fake.calls] == [("api", "graphql"), ("issue", "list")]


def _offline(board, monkeypatch, items):
    monkeypatch.setattr(board, "repo_slug", lambda: ("owner", "repo"))
    monkeypatch.setattr(board, "load_issues", lambda: _issues(2))
    monkeypatch.setattr(board, "project_context", lambda owner: {})

    def refused(owner):
        raise items

    monkeypatch.setattr(board, "project_items", refused if isinstance(items, Exception) else
                        lambda owner: items)


def test_next_refuses_a_truncated_item_read_and_names_a_blind_token(board, monkeypatch, capsys):
    """A truncation is not a token that cannot see the board."""
    _offline(board, monkeypatch, board.Truncated("cut short"))
    with pytest.raises(board.Truncated):
        board.cmd_next(None)
    assert "cannot read the project board with this token" not in capsys.readouterr().out
    _offline(board, monkeypatch, board.Fail("token cannot reach the project"))
    assert board.cmd_next(None) == 0
    assert "cannot read the project board with this token" in capsys.readouterr().out


def test_start_reads_the_board_before_it_branches(board, monkeypatch, capsys):
    """A refused read leaves the checkout on main; a card off the board is named."""
    git: list = []
    monkeypatch.setattr(board.subprocess, "run", lambda argv, **k: git.append(argv) or type(
        "Done", (), {"stdout": "main\n" if argv[:2] == ["git", "rev-parse"] else ""}))
    _offline(board, monkeypatch, board.Truncated("cut short"))
    with pytest.raises(board.Truncated):
        board.cmd_start(type("Args", (), {"number": 2}))
    assert not [argv for argv in git if argv[:2] == ["git", "checkout"]]

    _offline(board, monkeypatch, {})
    monkeypatch.setattr(board, "gh", _fake_gh([], []))
    assert board.cmd_start(type("Args", (), {"number": 2})) == 0
    out = capsys.readouterr().out
    assert "is NOT on the" in out
    assert "#2 is In Progress" not in out
    assert [argv for argv in git if argv[:2] == ["git", "checkout"]]
