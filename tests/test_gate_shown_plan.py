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
    shown = gates.shown_plan(_plan({"a": 1}, {"a": 2}), folder="/music")
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


def test_every_digest_bound_gate_shows_something():
    """R-693's class, closed: a gate that binds a decision to a digest either
    hands the plan to the gate layer or names what it shows. A digest and
    nothing else is the screen R-670 and R-686 each fixed once."""
    blind = [
        f"{path}:{line}"
        for path, line, keywords in _require_calls()
        if "digest" in keywords and not ({"plan", "context"} & keywords)
    ]
    assert blind == [], f"digest bound gates showing nothing: {blind}"


def test_no_gate_passes_a_digest_beside_a_plan():
    twice = [
        f"{path}:{line}"
        for path, line, keywords in _require_calls()
        if {"digest", "plan"} <= keywords
    ]
    assert twice == [], twice
