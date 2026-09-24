"""The gate layer shows a digested plan's items whenever one is passed (R-693).

R-670 and R-686 each closed one verb whose gate carried the question and not
the plan, and the review that closed R-686 swept every ``gate.require`` call in
``src`` and found seven more passing a digest and nothing to show. The class is
closed here once: :func:`cratekit.cli.gates.shown_plan` is the one body a
digest bound gate shows through, :meth:`Gates.require` calls it for any plan it
is handed, and the sweep that found the seven is a guard below rather than a
grep somebody has to remember to run.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.cli import gates, registry, render

SRC = Path(__file__).resolve().parent.parent / "src" / "cratekit"


def _spec(*, explicit: bool = False) -> registry.GateSpec:
    return registry.GateSpec(
        name="shown.probe",
        options=("apply", "abort"),
        prompt="Apply this plan?",
        explicit=explicit,
        digest_source="plan",
    )


def _plan(*items: dict) -> dict:
    return {"digest": "sha256:abc", "items": list(items), "totals": {"count": 1}}


def _refused(**kwargs) -> dict:
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(gates.DecisionRequired) as raised:
        gates.Gates(state=state).require(_spec(), **kwargs)
    return raised.value.cause.detail


# ---------------------------------------------------------------------------
# The helper
# ---------------------------------------------------------------------------


def test_shown_plan_carries_the_facts_then_the_digest_the_count_and_every_item():
    shown = gates.shown_plan(_plan({"a": 1}, {"a": 2}), {"folder": "/music"})
    assert list(shown) == ["folder", "digest", "count", "items"]
    assert shown["folder"] == "/music"
    assert shown["digest"] == "sha256:abc"
    assert shown["count"] == 2
    assert shown["items"] == [{"a": 1}, {"a": 2}]


def test_shown_plan_counts_the_items_and_not_a_narrower_total():
    """``totals.count`` is a verb's own number, the renames it can perform or
    the tracks it routes. The count on the screen is how many items the digest
    covers, since that is what the person is approving."""
    plan = {"digest": "d", "items": [{"n": 1}, {"n": 2}, {"n": 3}], "totals": {"count": 1}}
    assert gates.shown_plan(plan)["count"] == 3


def test_shown_plan_refuses_a_fact_it_would_overwrite():
    """A fact under digest, count or items would be replaced by the plan's
    value without a word, so the collision is refused rather than resolved."""
    for name in gates.SHOWN_PLAN_KEYS:
        with pytest.raises(ValueError, match=name):
            gates.shown_plan(_plan(), {name: "anything"})
    assert gates.shown_plan(_plan(), {"plan": "full"})["plan"] == "full"


def test_shown_plan_has_no_bound():
    """A list cut short asks for approval of items nobody was shown."""
    items = [{"n": index} for index in range(1000)]
    shown = gates.shown_plan({"digest": "d", "items": items})
    assert shown["items"] == items
    assert shown["count"] == 1000


def test_shown_plan_says_none_for_an_empty_plan_rather_than_nothing():
    """An empty plan is still a plan a person can abort, and its screen has to
    say the list is empty rather than print a bare header (R-686)."""
    shown = gates.shown_plan({"digest": "d", "items": []})
    assert shown["items"] == [] and shown["count"] == 0
    cause = _refused(plan={"digest": "d", "items": []})
    screen = render.render_gate(_cause(cause))
    assert "  items: none" in screen


# ---------------------------------------------------------------------------
# require() with a plan
# ---------------------------------------------------------------------------


def test_require_shows_the_plan_it_binds_the_decision_to():
    detail = _refused(plan=_plan({"path": "a.flac"}), context={"folder": "/music"})
    assert detail["shown"] == {
        "folder": "/music",
        "digest": "sha256:abc",
        "count": 1,
        "items": [{"path": "a.flac"}],
    }


def test_require_records_the_offer_off_the_plan_it_showed():
    """The digest the answer is judged against is the one on the screen."""
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(_spec(), plan=_plan())
    assert state.offers["shown.probe"] == "sha256:abc"


def test_require_shows_the_plan_on_the_explicit_refusal_as_well():
    """Both refusals carry it, so what a person sees does not depend on
    whether they typed a flag."""
    state = gates.RunState(run_id="r", verb="probe", created="now")
    resolver = gates.Gates(state=state, supplied={"shown.probe": "apply"})
    with pytest.raises(gates.DecisionRequired) as raised:
        resolver.require(_spec(explicit=True), plan=_plan({"n": 1}))
    assert raised.value.cause.detail["shown"]["items"] == [{"n": 1}]


def test_require_refuses_a_digest_beside_a_plan():
    """Two sources of the digest is how the screen and the binding disagree."""
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(TypeError):
        gates.Gates(state=state).require(_spec(), digest="other", plan=_plan())


def test_require_answers_from_the_plan_and_records_its_digest():
    state = gates.RunState(run_id="r", verb="probe", created="now")
    resolver = gates.Gates(state=state, supplied={"shown.probe": "apply"})
    assert resolver.require(_spec(), plan=_plan()) == "apply"
    assert state.decisions["shown.probe"].digest == "sha256:abc"


def test_require_with_no_plan_and_no_context_still_carries_no_shown_key():
    """Absent and empty stay different: the new keyword adds nothing to a call
    that passes neither."""
    assert "shown" not in _refused(digest="d")


def test_the_screen_prints_the_plan_in_the_default_mode():
    cause = _refused(plan=_plan({"path": "a.flac", "to": "b.flac"}), context={"root": "/m"})
    screen = render.render_gate(_cause(cause))
    assert "  root: /m" in screen
    assert "  digest: sha256:abc" in screen
    assert "  count: 1" in screen
    assert "    path=a.flac, to=b.flac" in screen


def _cause(detail: dict):
    """The refusal's cause, rebuilt so the renderer is driven as the CLI drives it."""
    state = gates.RunState(run_id="r", verb="probe", created="now")
    try:
        gates.Gates(state=state).require(_spec(), digest="unused")
    except gates.DecisionRequired as raised:
        cause = raised.cause
    cause.detail.clear()
    cause.detail.update(detail)
    return cause


# ---------------------------------------------------------------------------
# The sweep that found the seven, as a guard
# ---------------------------------------------------------------------------


def _require_calls():
    """Every ``<something>.gate.require(...)`` call in the package, with its
    keyword names and where it is."""
    for path in sorted(SRC.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Attribute) and func.attr == "require"):
                continue
            owner = func.value
            if not (isinstance(owner, ast.Attribute) and owner.attr == "gate"):
                continue
            keywords = {keyword.arg for keyword in node.keywords}
            yield path.relative_to(SRC.parent.parent), node.lineno, keywords


def test_the_population_this_guard_sweeps_is_the_one_the_ledger_counted():
    """The sweep sees the whole package, or it guards nothing. Every gate the
    product declares is asked through ``ctx.gate.require``."""
    found = list(_require_calls())
    assert len(found) >= 19, found


#: Digest bound gates that show their plan through a body of their own rather
#: than through ``plan=``, by file, with how many such calls the file holds and
#: why each is allowed. A new call in one of these files, or in any other file,
#: fails the guard below until it hands the gate layer its plan or is named here
#: with a reason.
SHOWS_ITS_OWN_WAY: dict[str, tuple[int, str]] = {
    "src/cratekit/write/naming_cli.py": (
        1,
        "R-670's screen is bounded at PLAN_SHOWN by decision, because the "
        "default root is the whole library; the gate layer's body has no bound",
    ),
    "src/cratekit/intake/land_cli.py": (
        1,
        "shows the landing's files by name with the folder, the target and the "
        "batch, the screen R-670 was written to match",
    ),
    "src/cratekit/sync/mark_cli.py": (
        2,
        "shows each item as renamed on the account or left alone with its "
        "reason, one line per fact",
    ),
    "src/cratekit/session/restore_cli.py": (
        1,
        "shows the off machine snapshot the restore would pull; the offer's "
        "items are the two halves, not a list a person approves one by one",
    ),
    "src/cratekit/deletion/cli.py": (
        1,
        "shows the baseline and the offered count only, R-134's screen; the "
        "files themselves are not listed, recorded as R-702",
    ),
}


def test_every_digest_bound_gate_shows_the_plan_it_binds_to():
    """R-693's class, closed: a gate that binds a decision to a digest hands
    the plan to the gate layer, which shows every item the digest covers, or
    is named above with the reason it shows its items some other way. A
    digest and a fact or two beside it is not enough, since that is the
    screen the outbound first asks had, an age and no track."""
    allowed = {path: count for path, (count, _why) in SHOWS_ITS_OWN_WAY.items()}
    seen: dict[str, int] = {}
    blind = []
    for path, line, keywords in _require_calls():
        if "digest" not in keywords:
            continue
        seen[str(path)] = seen.get(str(path), 0) + 1
        if str(path) not in allowed:
            blind.append(f"{path}:{line}")
    assert blind == [], f"digest bound gates not showing their plan: {blind}"
    assert {path: seen.get(path, 0) for path in allowed} == allowed, (
        "a file named in SHOWS_ITS_OWN_WAY gained or lost a digest bound gate; "
        "hand the new one its plan or name it with a reason"
    )


def test_no_gate_passes_a_digest_beside_a_plan():
    twice = [
        f"{path}:{line}"
        for path, line, keywords in _require_calls()
        if {"digest", "plan"} <= keywords
    ]
    assert twice == [], twice
