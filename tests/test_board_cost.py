"""`scripts/board.py` reads the board for points in the tens, not the hundreds (U151).

GitHub meters GraphQL by the node, 5,000 points an hour for the whole account.
`gh project item-list` cost about 101 points a page of a hundred cards and
`gh project field-list` another 101, and `sync` rewrote Unblocks on every card
whether or not it changed, so one sync cost about 850 points. The cards are now
read off the issues' own memberships, a point a page of a hundred issues, the
fields in one query, and Unblocks is written only when it changed.

The double is the `gh` of `test_board_reads`, which refuses the two listings
outright, so a call to either fails the test that made it.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from tests.test_board_reads import _fake_gh, _issues, _items, _membership

BOARD = Path(__file__).resolve().parent.parent / "scripts" / "board.py"


@pytest.fixture
def board(monkeypatch):
    spec = importlib.util.spec_from_file_location("board_cost_under_test", BOARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "repo_slug", lambda: ("owner", "repo"))
    return module


def _unit(number: int, deps: str = "none", state: str = "OPEN") -> dict:
    return {
        "number": number,
        "title": f"U{number}: unit {number}",
        "state": state,
        "body": f"**Depends on:** {deps}",
        "labels": [{"name": "unit"}],
    }


def _five() -> list[dict]:
    """A five issue graph: #1 releases #2 and #3, #3 releases #4, #5 stands alone."""
    issues = [
        _unit(1),
        _unit(2, "#1"),
        _unit(3, "#1"),
        _unit(4, "#3"),
        _unit(5),
    ]
    for issue in issues:
        ready = issue["number"] in (1, 5)
        issue["labels"].append({"name": "ready" if ready else "blocked"})
    return issues


def _settled(issues: list[dict]) -> list[dict]:
    """Each card with the status and the Unblocks number a sync would derive."""
    status = {1: "Ready", 2: "Blocked", 3: "Blocked", 4: "Blocked", 5: "Ready"}
    unblocks = {1: 2, 2: 0, 3: 1, 4: 0, 5: 0}
    return [
        {"id": f"item-{i['number']}", "status": status[i["number"]],
         "number": i["number"], "unblocks": unblocks[i["number"]]}
        for i in issues
    ]


def _edits(calls, field: str) -> list[tuple[str, ...]]:
    return [c for c in calls if c[:2] == ("project", "item-edit") and field in c]


def _reads(calls, marker: str) -> list[tuple[str, ...]]:
    return [c for c in calls if c[:2] == ("api", "graphql") and marker in " ".join(c)]


def test_a_sync_with_no_drift_lists_nothing_and_writes_nothing(board, monkeypatch):
    issues = _five()
    fake = _fake_gh(issues, _settled(issues))
    monkeypatch.setattr(board, "gh", fake)

    assert board.reconcile("owner", apply=True) == []

    assert not [c for c in fake.calls if c[:2] == ("project", "item-list")]
    assert not [c for c in fake.calls if c[:2] == ("project", "field-list")]
    assert not [c for c in fake.calls if c[:2] in (("project", "item-edit"), ("issue", "edit"))]
    assert len(_reads(fake.calls, "projectItems")) == 1
    assert len(_reads(fake.calls, "projectV2(number")) == 1


def test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card(board, monkeypatch):
    """330 issues read in four pages, each after the cursor the last one gave."""
    issues = _issues(330)
    fake = _fake_gh(issues, _items(issues, 316))
    monkeypatch.setattr(board, "gh", fake)

    assert len(board.project_items("owner")) == 316

    pages = _reads(fake.calls, "projectItems")
    assert len(pages) == 4
    cursors = [next((a for a in page if a.startswith("after=")), None) for page in pages]
    assert cursors == [None, "after=100", "after=200", "after=300"]
    # A cursor is text, so it goes as `-f`; `-F` would type it.
    for page in pages[1:]:
        assert page[page.index(next(a for a in page if a.startswith("after="))) - 1] == "-f"


def test_an_unchanged_unblocks_number_is_not_written(board, monkeypatch):
    issues = _five()
    fake = _fake_gh(issues, _settled(issues))
    monkeypatch.setattr(board, "gh", fake)

    board.reconcile("owner", apply=True)

    assert _edits(fake.calls, "unblocks") == []


def test_a_changed_unblocks_number_is_written_once_with_the_derived_count(board, monkeypatch):
    issues = _five()
    cards = _settled(issues)
    cards[0]["unblocks"] = 7
    fake = _fake_gh(issues, cards)
    monkeypatch.setattr(board, "gh", fake)

    board.reconcile("owner", apply=True)

    edits = _edits(fake.calls, "unblocks")
    assert len(edits) == 1
    assert edits[0][edits[0].index("--id") + 1] == "item-1"
    assert edits[0][edits[0].index("--number") + 1] == "2"


def test_a_card_with_no_unblocks_number_gets_one(board, monkeypatch):
    issues = _five()
    cards = _settled(issues)
    cards[2]["unblocks"] = None
    fake = _fake_gh(issues, cards)
    monkeypatch.setattr(board, "gh", fake)

    board.reconcile("owner", apply=True)

    edits = _edits(fake.calls, "unblocks")
    assert [e[e.index("--id") + 1] for e in edits] == ["item-3"]


def test_an_issue_off_the_board_is_added_then_given_its_status_and_number(board, monkeypatch):
    issues = _five()
    fake = _fake_gh(issues, _settled(issues)[:4])
    monkeypatch.setattr(board, "gh", fake)

    drift = board.reconcile("owner", apply=True)

    assert any("#5" in line and "not on the board" in line for line in drift)
    added = [c for c in fake.calls if c[:2] == ("project", "item-add")]
    assert len(added) == 1 and added[0][added[0].index("--url") + 1].endswith("/issues/5")
    status = _edits(fake.calls, "status")
    assert [(e[e.index("--id") + 1], e[-1]) for e in status] == [("item-added", "Ready")]
    unblocks = _edits(fake.calls, "unblocks")
    assert [(e[e.index("--id") + 1], e[e.index("--number") + 1]) for e in unblocks] == [
        ("item-added", "0")
    ]


def test_a_card_on_another_project_or_owner_is_not_this_boards(board, monkeypatch):
    """Issue 5 sits on project 3 and on another owner's project 2, and on nothing of ours."""
    issues = _five()
    stray = {"id": "stray", "status": "Done"}
    extra = {5: [_membership(stray, number=3), _membership(stray, login="someone")]}
    fake = _fake_gh(issues, _settled(issues)[:4], extra=extra)
    monkeypatch.setattr(board, "gh", fake)

    items = board.project_items("owner")

    assert sorted(items) == [1, 2, 3, 4]


def test_the_owner_is_matched_whatever_its_case(board, monkeypatch):
    issues = _five()
    fake = _fake_gh(issues, _settled(issues))
    monkeypatch.setattr(board, "gh", fake)

    assert sorted(board.project_items("OWNER")) == [1, 2, 3, 4, 5]


def test_an_issue_whose_memberships_come_back_short_is_refused(board, monkeypatch):
    issues = _five()
    fake = _fake_gh(issues, _settled(issues))

    def short(*args, parse=False):
        served = fake(*args, parse=parse)
        if "projectItems" in " ".join(args):
            served["data"]["repository"]["issues"]["nodes"][0]["projectItems"]["totalCount"] = 21
        return served

    monkeypatch.setattr(board, "gh", short)
    with pytest.raises(board.Truncated, match="#1 project membership read returned 1 of the 21"):
        board.project_items("owner")


def test_a_page_that_says_more_and_gives_no_cursor_is_refused(board, monkeypatch):
    issues = _issues(150)
    fake = _fake_gh(issues, _items(issues, 150))

    def no_cursor(*args, parse=False):
        served = fake(*args, parse=parse)
        if "projectItems" in " ".join(args):
            served["data"]["repository"]["issues"]["pageInfo"]["endCursor"] = None
        return served

    monkeypatch.setattr(board, "gh", no_cursor)
    with pytest.raises(board.Truncated, match="gave no cursor"):
        board.project_items("owner")


def test_a_cursor_that_never_ends_is_refused(board, monkeypatch):
    issues = _issues(150)
    fake = _fake_gh(issues, _items(issues, 150))

    def endless(*args, parse=False):
        served = fake(*args, parse=parse)
        if "projectItems" in " ".join(args):
            served["data"]["repository"]["issues"]["pageInfo"] = {
                "hasNextPage": True, "endCursor": "0",
            }
        return served

    monkeypatch.setattr(board, "gh", endless)
    with pytest.raises(board.Truncated, match="ran past"):
        board.project_items("owner")


def test_the_card_read_leaves_archived_cards_out_as_the_listing_did(board):
    """The recorded decision: an archived card reads as not on the board."""
    assert "includeArchived: false" in board.MEMBERSHIP_QUERY


def test_the_context_is_one_query_for_the_project_its_status_and_unblocks(board, monkeypatch):
    fake = _fake_gh([], [])
    monkeypatch.setattr(board, "gh", fake)

    ctx = board.project_context("owner")

    assert ctx["id"] == "project"
    assert ctx["status_field"] == "status"
    assert ctx["unblocks_field"] == "unblocks"
    assert set(ctx["options"]) == set(board.STATUS_ORDER)
    assert len(fake.calls) == 1
    # The number goes as a typed variable, never formatted into the query.
    assert "number=2" in fake.calls[0] and "-F" in fake.calls[0]


def test_the_context_asks_the_organization_when_the_owner_is_not_a_user(board, monkeypatch):
    fake = _fake_gh([], [])

    def org_only(*args, parse=False):
        if "user(login" in " ".join(args):
            raise board.Fail("Could not resolve to a User with the login of 'owner'.")
        return fake(*args, parse=parse)

    monkeypatch.setattr(board, "gh", org_only)
    assert board.project_context("owner")["id"] == "project"


def test_a_project_the_token_cannot_see_is_refused_and_says_why(board, monkeypatch):
    def unseen(*args, parse=False):
        if "projectV2(number" in " ".join(args):
            return {"data": {"user": {"projectV2": None}}}
        raise AssertionError(args)

    monkeypatch.setattr(board, "gh", unseen)
    with pytest.raises(board.Fail, match="cannot be read with this token"):
        board.project_context("owner")


def test_a_project_with_no_status_field_is_refused_by_name(board, monkeypatch):
    project = {"id": "p", "url": "u", "fields": {"totalCount": 1, "nodes": [{"name": "Title", "id": "t"}]}}
    monkeypatch.setattr(board, "gh", lambda *a, parse=False: {"data": {"user": {"projectV2": project}}})
    with pytest.raises(board.Fail, match="no single select Status field"):
        board.project_context("owner")


def test_next_asks_for_the_project_before_trusting_an_empty_card_read(board, monkeypatch, capsys):
    """A token that cannot see the project reads every issue as on no card at all."""
    issues = _five()
    fake = _fake_gh(issues, [])

    def unseen(*args, parse=False):
        if "projectV2(number" in " ".join(args):
            return {"data": {"user": {"projectV2": None}}}
        return fake(*args, parse=parse)

    monkeypatch.setattr(board, "gh", unseen)
    monkeypatch.setattr(board, "load_issues", lambda: issues)

    assert board.cmd_next(None) == 0
    assert "cannot read the project board with this token" in capsys.readouterr().out


def test_a_stored_unblocks_float_compares_as_the_int_it_holds(board):
    assert board._stored_number(2.0) == 2
    assert board._stored_number(None) is None
    assert board._stored_number(2.5) == 2.5
