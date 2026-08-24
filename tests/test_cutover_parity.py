"""U29's parity table: every Feature Inventory row, and the verb that covers it.

WHY THIS EXISTS BEFORE U29 DOES. U29 is the cutover, and its own test scenario is
"the parity table is generated from the CLI verb inventory and fails when a row
has no covering verb". The cutover itself is attended and runs against the live
library, which no agent may touch, but the TABLE is derived from the registry and
touches nothing. So the part that can be mechanised is mechanised, and what is
left for a person is the part that genuinely needs one.

WHAT THIS ADDS OVER THE CONTRACT SUITE, WHICH IS THE ONLY REASON IT IS A SECOND
FILE. ``tests/test_cli_contract.py`` already asserts that every row is claimed at
its stated disposition, and that a cut or deferred row is claimed by nothing. It
counts a DECLARED verb as a claim, which is correct for the question it asks: is
the product's shape faithful to the plan. It is the wrong answer to the cutover
question, because a verb that is declared and not built replaces nothing a person
can run. Everything here turns on ``entry.landed``, and that is the whole of the
difference.

THE INVENTORY IS NOT COPIED HERE, AND THE FIRST VERSION OF THIS FILE COPIED IT.
``registry.FEATURES`` is already the plan's table transcribed into the package,
already carries each row's disposition, and is already what the contract suite
reads. Vendoring a second copy alongside it put two transcriptions of one table
in one repository, which is the defect this file exists to prevent, one level up.
Worse, the copy dropped the disposition column, so three rows the plan CUT and
two it DEFERRED were reported as an open backlog with a note reading "cited by no
registry entry at all". That sentence states a mechanical fact and buries a
decision, and it cost a session's work to discover that the decision had been
made on 2026-08-01 and written down.

WHAT A DISPOSITION MEANS, since the whole file turns on it. ``core``, ``module``
and ``reshaped`` are rows the product replaces, so a missing verb is backlog.
``cut`` is a row the product deliberately does not replace, so the capability
ends when the source system is retired, and ``CUT.md`` carries the reason per
entry point. ``defer`` is a row that comes back after launch. Neither is backlog,
and counting them as backlog makes the cutover look further away than it is while
hiding the rows that genuinely block it.
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
#: one. Absent is a normal state and is handled by asserting less about DRIFT,
#: never by asserting less about parity: every assertion below except the drift
#: check reads ``registry.FEATURES`` and needs no file outside this repository.
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

    NORMALISED, because the plan's column is prose and the package's is an enum.
    "Module, off by default" and "Module, on by default" are both ``module``: the
    qualifier says which way the toggle ships, which is R5's business and is
    asserted in the contract suite, not this row's disposition.
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
    """The drift check that makes the transcription legitimate.

    DISPOSITIONS AND ROW NUMBERS, NOT TITLES. ``registry.FEATURES`` deliberately
    retitles rows in the product's own vocabulary, "label to streaming playlist
    folders" where the plan names one service, so comparing the prose would fail
    on a rewording that was intentional and would be silenced by copying the
    plan's words back, which is the wrong repair. The disposition is the load
    bearing cell: it decides whether a row is a debt or a decision.

    It asserts nothing when the sibling repository is absent, and that is the ONE
    thing here allowed to depend on it. No skip, because a skip outside the
    pending register is a guard switched off with no record of when it comes back.
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
    """Feature row to the LANDED verbs that cover it, from the registry itself.

    Landed only, and this is the line that separates this file from the contract
    suite. A verb that is declared and not built covers nothing a person can run,
    and counting it would make the parity table report a cutover as possible while
    the workflow it replaces has no replacement.
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
    """Rows the product OWES and has not landed. The cutover backlog, derived.

    Nothing here is written down by hand. A verb landing shrinks this with no
    edit, a row changing disposition moves in or out of it with no edit, and a row
    nobody has looked at cannot quietly drop off it.
    """
    covered = covering_verbs()
    return {
        row: disposition
        for row, disposition in dispositions().items()
        if disposition in OWED and row not in covered
    }


def test_the_inventory_is_complete_and_contiguous():
    """Anti-vacuity, and a missing row number would hide a whole feature.

    Contiguity matters more than the count: the rows are numbered from one with
    no gaps in the plan, so a gap means a row was dropped in transcription and the
    parity table would report a feature nobody has to cover.
    """
    rows = dispositions()
    assert len(rows) == 37, f"the inventory holds {len(rows)} rows rather than 37"
    assert sorted(rows) == list(range(1, 38)), "the inventory row numbers have a gap"


def test_every_declared_disposition_is_one_this_file_understands():
    """A sixth disposition would fall through OWED and be silently not-a-debt.

    ``backlog`` asks whether a disposition is in ``OWED``, so anything unrecognised
    lands in the complement and the row leaves the backlog without anybody
    deciding it should. That is the same silence this file was rewritten to close,
    so it is asserted rather than assumed.
    """
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
    """The registry cannot cite a feature row the inventory does not declare.

    This is the direction that rots silently: a verb carrying `feature_rows=(99,)`
    would look covered and cover nothing.
    """
    rows = dispositions()
    unknown = sorted(set(citing_verbs()) - set(rows))
    assert not unknown, (
        f"verbs cite Feature Inventory rows that do not exist: {unknown}. Either "
        f"the row number is a typo or the inventory moved underneath the registry."
    )


def test_a_row_cited_by_nothing_is_a_decision_and_not_an_oversight():
    """THE GUARD THAT WOULD HAVE CAUGHT THE FIRST VERSION OF THIS FILE.

    A row no verb cites at all, landed or declared, is either a row the plan cut
    or deferred, which is a decision, or a row the product owes and nobody has
    even declared a verb for, which is an oversight nothing else reports. The
    contract suite asserts the same property from the other end and counts
    declared verbs as claims; this states it in the cutover's own terms so the
    two halves of "uncovered" can never be collapsed into one undifferentiated
    list again.
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
    """THE PARITY TABLE. It fails when an owed row has no landed verb.

    Derived in both directions, so there is no table to keep in step. The
    assertion is that every row in the backlog is genuinely owed and genuinely
    unlanded, which is true by construction, and the value is the message: it
    names the rows and the units they are waiting on.
    """
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


def test_the_cutover_is_not_yet_possible_and_says_why():
    """The headline U29 answers, asserted so it cannot be assumed either way.

    When this test starts failing, every owed inventory row has a landed verb and
    the cutover is mechanically possible. It is still attended, and it still has
    to be run against the live library one workflow at a time, which is a person's
    job.
    """
    assert backlog(), (
        "every owed Feature Inventory row now has a landed verb. The cutover is "
        "mechanically possible: U29's remaining work is attended, one workflow at "
        "a time, against the live library. Update docs/METHOD.md's do-not-touch "
        "note, which explains why U29 is not an agent's unit."
    )


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
    assert "AWAITING" in rendered, "the backlog is empty, see the test above"
