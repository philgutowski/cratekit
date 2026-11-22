"""U29's parity table: every Feature Inventory row, and the landed verb that covers it.

The cutover is attended, but the table derives from the registry and touches
nothing, so it is mechanised here. Unlike ``tests/test_cli_contract.py``, which
counts a declared verb as a claim, everything here turns on ``entry.landed``,
because a declared verb replaces nothing a person can run. The inventory is read
from ``registry.FEATURES`` and never copied, so the plan has one transcription.
``core``, ``module`` and ``reshaped`` rows are owed, so a missing verb is backlog;
``cut`` and ``defer`` rows are decisions and never backlog.
"""

from __future__ import annotations

import re
from pathlib import Path

from cratekit.cli import registry

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Dispositions under which the product owes this row a verb. The complement,
#: ``cut`` and ``defer``, is a decision rather than a debt.
OWED = frozenset({"core", "module", "reshaped"})

#: Where the plan lives when the sibling repository is checked out beside this
#: one. Only the drift check reads it, and asserts nothing when it is absent.
PLAN = (
    REPO_ROOT.parent
    / "DJ_tools"
    / "docs"
    / "plans"
    / "2026-08-01-001-feat-dj-product-reengineering-plan.md"
)

#: One inventory row: `| 7 | Fallback lossy acquisition | Module, off by default | ...`
_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", re.M)


def dispositions() -> dict[int, str]:
    """Row to disposition, from the package's own transcription of the plan."""
    return {feature.row: feature.disposition for feature in registry.FEATURES}


def titles() -> dict[int, str]:
    """Row to title, for rendering. The product's wording, not the plan's."""
    return {feature.row: feature.title for feature in registry.FEATURES}


def plan_dispositions() -> dict[int, str] | None:
    """The plan's own dispositions, or None when the sibling repository is absent.

    Normalised to the first word of the prose column, so "Module, off by default"
    is ``module``; the toggle default is the contract suite's business.
    """
    if not PLAN.is_file():
        return None
    text = PLAN.read_text()
    body = text[text.index("#### Feature Inventory") :]
    found: dict[int, str] = {}
    for number, _feature, disposition in _ROW.findall(body):
        found.setdefault(int(number), disposition.split(",")[0].strip().lower())
    return found


def test_the_transcribed_dispositions_match_the_plan_when_it_is_reachable():
    """The transcribed dispositions and row numbers match the plan.

    Titles are not compared, because the registry retitles rows on purpose. With the
    sibling repository absent it asserts nothing rather than skipping, since a skip
    outside the pending register is a guard switched off with no record.
    """
    original = plan_dispositions()
    if original is None:
        return
    mine = dispositions()
    assert original == mine, (
        f"the transcribed dispositions have drifted from the plan. Only in the "
        f"plan: {sorted(set(original) - set(mine))}. Only transcribed: "
        f"{sorted(set(mine) - set(original))}. Differences: "
        f"{ {n: (original[n], mine[n]) for n in set(original) & set(mine) if original[n] != mine[n]} }"
    )


def covering_verbs() -> dict[int, list[str]]:
    """Feature row to the LANDED verbs that cover it.

    A declared verb covers nothing a person can run, so counting it would report a
    cutover as possible with no replacement in place.
    """
    found: dict[int, list[str]] = {}
    for entry in registry.entries():
        if not entry.landed:
            continue
        for row in entry.feature_rows or ():
            found.setdefault(row, []).append(entry.name)
    return found


def citing_verbs() -> dict[int, list[str]]:
    """Feature row to every verb citing it, landed or merely declared."""
    found: dict[int, list[str]] = {}
    for entry in registry.entries():
        for row in entry.feature_rows or ():
            found.setdefault(row, []).append(entry.name)
    return found


def backlog() -> dict[int, str]:
    """Rows the product owes and has not landed, derived with no hand written list."""
    covered = covering_verbs()
    return {
        row: disposition
        for row, disposition in dispositions().items()
        if disposition in OWED and row not in covered
    }


def test_the_inventory_is_complete_and_contiguous():
    """Rows run 1 to 37 with no gap, since a gap is a feature dropped in transcription."""
    rows = dispositions()
    assert len(rows) == 37, f"the inventory holds {len(rows)} rows rather than 37"
    assert sorted(rows) == list(range(1, 38)), "the inventory row numbers have a gap"


def test_every_declared_disposition_is_one_this_file_understands():
    """Every disposition is owed, cut or defer, so none silently leaves the backlog."""
    known = OWED | {"cut", "defer"}
    unknown = sorted(
        {d for d in dispositions().values() if d not in known}
    )
    assert not unknown, (
        f"registry.FEATURES carries dispositions this parity check does not "
        f"classify as owed or decided: {unknown}. Add them to OWED or to the "
        f"decided set deliberately, rather than letting them default."
    )


def test_every_covered_row_names_a_real_inventory_row():
    """No verb cites a feature row the inventory lacks, which would look covered."""
    rows = dispositions()
    unknown = sorted(set(citing_verbs()) - set(rows))
    assert not unknown, (
        f"verbs cite Feature Inventory rows that do not exist: {unknown}. Either "
        f"the row number is a typo or the inventory moved underneath the registry."
    )


def test_a_row_cited_by_nothing_is_a_decision_and_not_an_oversight():
    """A row cited by no verb, landed or declared, must be cut or deferred.

    An owed row nobody has declared a verb for is an oversight nothing else reports,
    so it is kept apart from a decision.
    """
    cited = set(citing_verbs())
    rows = dispositions()
    unclaimed = sorted(row for row in rows if row not in cited)
    wrong = [(row, rows[row]) for row in unclaimed if rows[row] in OWED]
    assert not wrong, (
        f"Feature Inventory rows the product owes are cited by no verb at all, "
        f"not even a declared one, so nothing on the board is waiting on them: "
        f"{wrong}"
    )
    assert unclaimed, (
        "every row is cited by some verb, so this guard proves nothing. If the "
        "plan really cut nothing, delete it rather than leaving it vacuous."
    )


def test_the_backlog_is_every_owed_row_without_a_landed_verb():
    """The parity table: every backlog row is owed, unlanded and awaits a declared verb."""
    owed = backlog()
    covered = covering_verbs()
    cited = citing_verbs()

    for row in owed:
        assert row not in covered, f"row {row} is in the backlog and has a landed verb"

    waiting = {row: sorted(set(cited.get(row, []))) for row in owed}
    assert all(waiting.values()), (
        f"a backlog row is waiting on no declared verb, so no unit owns it: "
        f"{ {row: names for row, names in waiting.items() if not names} }"
    )


def test_the_cutover_is_mechanically_possible_and_says_what_is_left():
    """Every owed row has a landed verb, so the cutover is mechanically possible (U45).

    A broken derivation also yields an empty backlog, so the emptiness is asserted
    beside the owed and covered populations, neither of which may be empty.
    Mechanically possible is not done: U29 stays attended, as ``docs/METHOD.md``
    argues.
    """
    owed = {row for row, disposition in dispositions().items() if disposition in OWED}
    covered = covering_verbs()
    assert owed, (
        "no inventory row is owed at all, so an empty backlog is a statement "
        "about nothing; the OWED spellings no longer match any disposition"
    )
    assert covered, "no row has a landed verb, so the covering map derived nothing"
    assert backlog() == {}, (
        f"these owed rows still have no landed verb, so the cutover is not "
        f"mechanically possible: {sorted(backlog())}"
    )
    assert owed <= set(covered), sorted(owed - set(covered))


def test_the_parity_table_renders_for_a_person():
    """The table itself, so the artifact is readable rather than only assertable."""
    rows = titles()
    disposition = dispositions()
    covered = covering_verbs()
    cited = citing_verbs()
    lines = []
    for number in sorted(rows):
        landed = sorted(covered.get(number, []))
        if landed:
            state = ", ".join(landed)
        elif disposition[number] not in OWED:
            state = disposition[number].upper()
        else:
            declared = sorted(set(cited.get(number, [])))
            state = f"AWAITING {', '.join(declared)}" if declared else "NO COVERING VERB"
        lines.append(f"{number:3d}  {disposition[number]:9}  {rows[number][:40]:40}  {state}")
    rendered = "\n".join(lines)
    assert rendered.count("\n") + 1 == len(rows)
    # AWAITING is a declared but unlanded verb and NO COVERING VERB a row nothing
    # declares, two different failures, so each is asserted on its own.
    assert "AWAITING" not in rendered, (
        "an owed row's verb is declared and not landed, so the cutover backlog is "
        "no longer empty; see the test above"
    )
    assert "NO COVERING VERB" not in rendered, (
        "an owed inventory row is cited by no verb at all, so no unit owns it"
    )
    # The same claim taken off the render, so a render from a stale map still fails.
    for number, disposition in sorted(dispositions().items()):
        if disposition in OWED:
            assert sorted(covered.get(number, [])), number
            assert ", ".join(sorted(covered[number])) in rendered, number
