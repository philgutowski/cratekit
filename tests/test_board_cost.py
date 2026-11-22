"""`scripts/board.py` reads the board for points in the tens, not the hundreds (U151).

Cards come off the issues' memberships, the fields in one query, and Unblocks is
written only when it changed. The `gh` double refuses the old listings outright.
"""

from __future__ import annotations

import pytest

from tests.test_board_reads import _fake_gh, _issues, _items, _membership, issue, load_board


@pytest.fixture
def board(monkeypatch):
    module = load_board()
    monkeypatch.setattr(module, "repo_slug", lambda: ("owner", "repo"))
    return module


def _five() -> list[dict]:
    """#1 releases #2 and #3, #3 releases #4, #5 stands alone."""
    deps = {1: "none", 2: "#1", 3: "#1", 4: "#3", 5: "none"}
    return [
        issue(n, f"U{n}: unit {n}", body=f"**Depends on:** {dep}",
              labels=["unit", "ready" if n in (1, 5) else "blocked"])
        for n, dep in deps.items()
    ]


def _settled(issues: list[dict]) -> list[dict]:
    unblocks = {1: 2, 2: 0, 3: 1, 4: 0, 5: 0}
    return [
        {"id": f"item-{i['number']}", "status": "Ready" if i["number"] in (1, 5) else "Blocked",
         "number": i["number"], "unblocks": unblocks[i["number"]]}
        for i in issues
    ]


def _sync(board, monkeypatch, edit=None, cards=5):
    """Reconcile the five issue board, with `edit` applied to its settled cards."""
    issues = _five()
    settled = _settled(issues)[:cards]
    if edit:
        edit(settled)
    fake = _fake_gh(issues, settled)
    monkeypatch.setattr(board, "gh", fake)
    return board.reconcile("owner", apply=True), fake.calls


def _edits(calls, field: str) -> list[tuple[str, ...]]:
    return [c for c in calls if c[:2] == ("project", "item-edit") and field in c]


def _reads(calls, marker: str) -> list[tuple[str, ...]]:
    return [c for c in calls if c[:2] == ("api", "graphql") and marker in " ".join(c)]


def _after(call):
    return call[call.index("--id") + 1], call[-1]


def test_a_sync_with_no_drift_lists_nothing_and_writes_nothing(board, monkeypatch):
    drift, calls = _sync(board, monkeypatch)
    assert drift == []
    assert not [c for c in calls if c[0] == "project" or c[:2] == ("issue", "edit")]
    assert len(_reads(calls, "projectItems")) == 1
    assert len(_reads(calls, "projectV2(number")) == 1


def test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card(board, monkeypatch):
    """330 issues in four pages, each after the last one's cursor, as `-f`, archived out."""
    assert "includeArchived: false" in board.MEMBERSHIP_QUERY
    issues = _issues(330)
    fake = _fake_gh(issues, _items(issues, 316))
    monkeypatch.setattr(board, "gh", fake)
    assert len(board.project_items("owner")) == 316
    pages = _reads(fake.calls, "projectItems")
    cursors = [next((a for a in page if a.startswith("after=")), None) for page in pages]
    assert cursors == [None, "after=100", "after=200", "after=300"]
    for page in pages[1:]:
        assert page[page.index(next(a for a in page if a.startswith("after="))) - 1] == "-f"


@pytest.mark.parametrize(
    ("index", "stored", "written"), [(0, 7, [("item-1", "2")]), (2, None, [("item-3", "1")])]
)
def test_a_changed_or_missing_unblocks_number_is_written_once(
    board, monkeypatch, index, stored, written
):
    _, calls = _sync(board, monkeypatch, lambda cards: cards[index].update(unblocks=stored))
    assert [_after(e) for e in _edits(calls, "unblocks")] == written


def test_an_issue_off_the_board_is_added_then_given_its_status_and_number(board, monkeypatch):
    drift, calls = _sync(board, monkeypatch, cards=4)
    assert any("#5" in line and "not on the board" in line for line in drift)
    added = [c for c in calls if c[:2] == ("project", "item-add")]
    assert len(added) == 1 and added[0][added[0].index("--url") + 1].endswith("/issues/5")
    assert [_after(e) for e in _edits(calls, "status")] == [("item-added", "Ready")]
    assert [_after(e) for e in _edits(calls, "unblocks")] == [("item-added", "0")]


def test_only_this_owners_project_is_the_board_whatever_the_case(board, monkeypatch):
    """Issue 5 sits on project 3 and on another owner's project 2, and on nothing of ours."""
    issues = _five()
    stray = {"id": "stray", "status": "Done"}
    extra = {5: [_membership(stray, number=3), _membership(stray, login="someone")]}
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _settled(issues)[:4], extra=extra))
    assert sorted(board.project_items("owner")) == [1, 2, 3, 4]
    monkeypatch.setattr(board, "gh", _fake_gh(issues, _settled(issues)))
    assert sorted(board.project_items("OWNER")) == [1, 2, 3, 4, 5]


def _doctored(fake, change):
    def gh(*args, parse=False):
        served = fake(*args, parse=parse)
        if "projectItems" in " ".join(args):
            change(served["data"]["repository"]["issues"])
        return served

    return gh


@pytest.mark.parametrize(
    ("count", "change", "says"),
    [
        (5, lambda p: p["nodes"][0]["projectItems"].update(totalCount=21),
         "#1 project membership read returned 1 of the 21"),
        (150, lambda p: p["pageInfo"].update(endCursor=None), "gave no cursor"),
        (150, lambda p: p.update(pageInfo={"hasNextPage": True, "endCursor": "0"}), "ran past"),
    ],
)
def test_a_card_read_that_is_short_or_never_ends_is_refused(
    board, monkeypatch, count, change, says
):
    issues = _issues(count)
    monkeypatch.setattr(board, "gh", _doctored(_fake_gh(issues, _items(issues, count)), change))
    with pytest.raises(board.Truncated, match=says):
        board.project_items("owner")


def test_the_context_is_one_query_for_the_project_its_status_and_unblocks(board, monkeypatch):
    fake = _fake_gh([], [])
    monkeypatch.setattr(board, "gh", fake)
    ctx = board.project_context("owner")
    fields = (ctx["id"], ctx["status_field"], ctx["unblocks_field"])
    assert fields == ("project", "status", "unblocks")
    assert set(ctx["options"]) == set(board.STATUS_ORDER)
    assert len(fake.calls) == 1
    # The number goes as a typed variable, never formatted into the query.
    assert "number=2" in fake.calls[0] and "-F" in fake.calls[0]

    def org_only(*args, parse=False):
        if "user(login" in " ".join(args):
            raise board.Fail("Could not resolve to a User with the login of 'owner'.")
        return fake(*args, parse=parse)

    monkeypatch.setattr(board, "gh", org_only)
    assert board.project_context("owner")["id"] == "project"


def _unseen(fake):
    def gh(*args, parse=False):
        if "projectV2(number" in " ".join(args):
            return {"data": {"user": {"projectV2": None}}}
        return fake(*args, parse=parse)

    return gh


def _project(nodes, total):
    project = {"id": "p", "url": "u", "fields": {"totalCount": total, "nodes": nodes}}
    return lambda *a, parse=False: {"data": {"user": {"projectV2": project}}}


@pytest.mark.parametrize(
    ("gh", "refusal", "says"),
    [
        (_unseen(_fake_gh([], [])), "Fail", "cannot be read with this token"),
        (_project([{"name": "Title", "id": "t"}], 1), "Fail", "no single select Status field"),
        (_project([{"name": "Status", "id": "s", "options": []}], 101), "Truncated",
         "project field read returned 1 of the 101"),
    ],
)
def test_a_project_the_token_cannot_read_whole_is_refused_by_name(
    board, monkeypatch, gh, refusal, says
):
    monkeypatch.setattr(board, "gh", gh)
    with pytest.raises(getattr(board, refusal), match=says):
        board.project_context("owner")


def test_next_asks_for_the_project_before_trusting_an_empty_card_read(board, monkeypatch, capsys):
    """A token that cannot see the project reads every issue as on no card at all."""
    issues = _five()
    monkeypatch.setattr(board, "gh", _unseen(_fake_gh(issues, [])))
    monkeypatch.setattr(board, "load_issues", lambda: issues)
    assert board.cmd_next(None) == 0
    assert "cannot read the project board with this token" in capsys.readouterr().out
