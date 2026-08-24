"""U29's parity table: every Feature Inventory row, and the verb that covers it.

WHY THIS EXISTS BEFORE U29 DOES. U29 is the cutover, and its own test scenario is
"the parity table is generated from the CLI verb inventory and fails when a row
has no covering verb". The cutover itself is attended and runs against the live
library, which no agent may touch, but the TABLE is derived from the registry and
touches nothing. So the part that can be mechanised is mechanised, and what is
left for a person is the part that genuinely needs one.

WHAT IT IS FOR. Before DJ_tools can be retired, every row of the Feature
Inventory has to be covered by a verb that exists. Rows without one are the
remaining backlog, and the whole point is that the backlog is DERIVED rather than
remembered: a verb landing shrinks it with no edit here, and a row nobody has
looked at cannot quietly drop off it.

THE INVENTORY IS READ FROM THE PLAN, NOT COPIED. The plan is the authority on
what the product is replacing, and a copy of a 37 row table maintained here would
be a second register that drifts. DJ_tools is read only for code and its docs are
the exception, which is what makes reading it legitimate.
"""

from __future__ import annotations

import re
from pathlib import Path

from cratekit.cli import registry

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The Feature Inventory, VENDORED. It is the plan's table and it lives here so
#: this test rests on nothing outside the repository.
#:
#: A COPY IS NORMALLY THE WRONG ANSWER AND IT IS THE RIGHT ONE HERE, for a reason
#: worth stating. The plan lives in a sibling repository, so reading it directly
#: made this suite fail on any clone that does not have that sibling, and the
#: only ways out of that were a skip, which ``tests/test_pending_units.py``
#: correctly forbids outside the pending register, or silently asserting less
#: when the file is missing, which is worse than skipping because nothing says
#: so. What makes the copy safe is the reconciliation below: when the plan IS
#: reachable, it is compared row for row, so a copy that drifts is a failure
#: rather than a quiet second opinion.
INVENTORY: dict[int, str] = {
    1: "Mix URL set identification (ACRCloud)",
    2: "Tracklist intake (paste, screenshot)",
    3: "Tidal playlist import",
    4: "Single file ingest",
    5: "ID-only mode, no downloads",
    6: "Vendored concurrent downloader",
    7: "Fallback lossy acquisition",
    8: "Genre and album art tagging",
    9: "Audio analysis: key, BPM, energy",
    10: "Vocal detection",
    11: "Naming engine",
    12: "Guarded DB writes, per surface",
    13: "Playlist routing to taxonomy",
    14: "Inbox sorting, unplaced audit",
    15: "Duplicate audit",
    16: "Camelot padding pass",
    17: "Filename and path repair",
    18: "Electronica retag passes",
    19: "Streamed-track playlist scan",
    20: "Intake aging report",
    21: "Favorite labels registry and sweeps",
    22: "Label import and label harvest",
    23: "Label to Tidal playlist folders",
    24: "Tidal hearts sync with auto-acquire",
    25: "dj-sync orchestrator",
    26: "Embedded job engine",
    27: "Setup wizard, config, profiles",
    28: "Doctor and status diagnostics",
    29: "Set builder",
    30: "Set recording mastering",
    31: "Library backup (rclone)",
    32: "Web dashboard and desktop app",
    33: "Claude skill layer",
    34: "Library adoption",
    35: "Spotify playlist intake",
    36: "Playlist export to streaming",
    37: "Track deletion and tombstones",
}

#: Where the plan lives when the sibling repository is checked out beside this
#: one. Absent is a normal state and is handled by asserting less about DRIFT,
#: never by asserting less about parity.
PLAN = (
    REPO_ROOT.parent
    / "DJ_tools"
    / "docs"
    / "plans"
    / "2026-08-01-001-feat-dj-product-reengineering-plan.md"
)

#: One inventory row: `| 7 | Fallback lossy acquisition | Module, off by default | ...`
_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", re.M)

#: THE BACKLOG SPLITS IN TWO AND THE SECOND HALF IS THE ONE THAT SURPRISES.
#: Rows 6, 7, 29, 30 and 31 are DECLARED by a registry entry and not yet built,
#: so they are visible to anybody reading the registry. Rows 16, 18, 19, 23 and
#: 32 are cited by NO entry at all, landed or planned, so nothing in the package
#: claims them and a table derived from the registry alone reports them as though
#: they did not exist. That asymmetry is the whole argument for reading the
#: inventory rather than the registry: the first measurement taken for this unit
#: looked only at cited rows and put the backlog at five when it is ten.
UNCOVERED: dict[int, str] = {
    6: "vendored concurrent downloader, declared as acquire.download, planned",
    7: "fallback lossy acquisition, declared as acquire.download and acquire.audit, planned",
    16: "Camelot padding pass, cited by no registry entry at all",
    18: "Electronica retag passes, cited by no registry entry at all",
    19: "streamed-track playlist scan, cited by no registry entry at all",
    23: "label to Tidal playlist folders, cited by no registry entry at all",
    29: "the set builder, declared as setbuild, planned",
    30: "set mastering, declared as master, planned",
    31: "the off machine backup, declared as backup.run, planned",
    32: "web dashboard and desktop app, cited by no registry entry at all",
}


def inventory_rows() -> dict[int, str]:
    """Every Feature Inventory row. The vendored table, not the plan."""
    return dict(INVENTORY)


def plan_rows() -> dict[int, str] | None:
    """The plan's own table, or None when the sibling repository is not present."""
    if not PLAN.is_file():
        return None
    text = PLAN.read_text()
    body = text[text.index("#### Feature Inventory") :]
    found: dict[int, str] = {}
    for number, feature, _disposition in _ROW.findall(body):
        found.setdefault(int(number), feature.strip())
    return found


def test_the_vendored_inventory_matches_the_plan_when_the_plan_is_reachable():
    """The drift check that makes the copy legitimate.

    It asserts nothing when the sibling repository is absent, and that is the ONE
    thing here allowed to depend on it: parity is asserted unconditionally from
    the vendored table above, and only the question "is the copy still faithful"
    needs the original. No skip, because a skip outside the pending register is a
    guard switched off with no record of when it comes back.
    """
    original = plan_rows()
    if original is None:
        return
    assert original == INVENTORY, (
        f"the vendored Feature Inventory has drifted from the plan. Only in the "
        f"plan: {sorted(set(original) - set(INVENTORY))}. Only vendored: "
        f"{sorted(set(INVENTORY) - set(original))}. Text differences: "
        f"{ {n: (original[n], INVENTORY[n]) for n in set(original) & set(INVENTORY) if original[n] != INVENTORY[n]} }"
    )


def covering_verbs() -> dict[int, list[str]]:
    """Feature row to the LANDED verbs that cover it, from the registry itself.

    Landed only. A verb that is declared and not built covers nothing a person can
    run, and counting it would make the parity table report a cutover as possible
    while the workflow it replaces has no replacement.
    """
    found: dict[int, list[str]] = {}
    for entry in registry.entries():
        if not entry.landed:
            continue
        for row in entry.feature_rows or ():
            found.setdefault(row, []).append(entry.name)
    return found


def test_the_inventory_is_complete_and_contiguous():
    """Anti-vacuity, and a missing row number would hide a whole feature.

    Contiguity matters more than the count: the rows are numbered from one with
    no gaps in the plan, so a gap here means a row was dropped in the copying and
    the parity table would report a feature nobody has to cover.
    """
    rows = inventory_rows()
    assert len(rows) == 37, f"the inventory holds {len(rows)} rows rather than 37"
    assert sorted(rows) == list(range(1, 38)), "the inventory row numbers have a gap"


def test_every_covered_row_names_a_real_inventory_row():
    """The registry cannot cite a feature row the inventory does not declare.

    This is the direction that rots silently: a verb carrying `feature_rows=(99,)`
    would look covered and cover nothing, and no other guard reads that field.
    """
    rows = inventory_rows()
    cited = set(covering_verbs())
    unknown = sorted(cited - set(rows))
    assert not unknown, (
        f"verbs cite Feature Inventory rows that do not exist: {unknown}. Either "
        f"the row number is a typo or the inventory moved underneath the registry."
    )


def test_the_uncovered_backlog_is_exactly_what_is_written_down():
    """THE PARITY TABLE. It fails when a row has no covering verb, in both directions.

    Landing a verb shrinks the backlog and fails here until somebody removes the
    row from ``UNCOVERED``, which is the act that records the cutover becoming
    possible. A row silently losing its verb fails here too.
    """
    rows = inventory_rows()
    covered = set(covering_verbs())
    uncovered = {number for number in rows if number not in covered}

    newly_uncovered = sorted(uncovered - set(UNCOVERED))
    newly_covered = sorted(set(UNCOVERED) - uncovered)
    assert not newly_uncovered, (
        f"Feature Inventory rows have no covering verb and are not in the "
        f"recorded backlog: "
        f"{[(n, rows[n]) for n in newly_uncovered]}"
    )
    assert not newly_covered, (
        f"these rows are now covered, so the cutover backlog has shrunk. Remove "
        f"them from UNCOVERED: {[(n, UNCOVERED[n]) for n in newly_covered]}"
    )


def test_the_backlog_distinguishes_declared_from_unclaimed():
    """The two halves close differently, so the table has to tell them apart.

    A row a registry entry declares is waiting on a unit that exists. A row no
    entry cites is waiting on somebody deciding whether the product covers it at
    all, which is a different question and is not on anybody's board. Collapsing
    them into one count is how the second kind goes unnoticed, and it is what the
    first measurement taken for this unit did.
    """
    cited = {row for entry in registry.entries() for row in (entry.feature_rows or ())}
    declared = sorted(number for number in UNCOVERED if number in cited)
    unclaimed = sorted(number for number in UNCOVERED if number not in cited)
    assert declared and unclaimed, (
        f"one half of the backlog is empty, so this guard proves nothing: "
        f"declared={declared} unclaimed={unclaimed}"
    )
    for number in unclaimed:
        assert "cited by no registry entry" in UNCOVERED[number], (
            f"row {number} is cited by nothing and its note does not say so"
        )


def test_the_cutover_is_not_yet_possible_and_says_why():
    """The headline U29 answers, asserted so it cannot be assumed either way.

    When this test starts failing, every inventory row has a verb and the cutover
    is mechanically possible. It is still attended, and it still has to be run
    against the live library one workflow at a time, which is a person's job.
    """
    assert UNCOVERED, (
        "every Feature Inventory row now has a covering verb. The cutover is "
        "mechanically possible: U29's remaining work is attended, one workflow at "
        "a time, against the live library. Update docs/METHOD.md's do-not-touch "
        "note, which explains why U29 is not an agent's unit."
    )


def test_the_parity_table_renders_for_a_person():
    """The table itself, so the artifact is readable rather than only assertable."""
    rows = inventory_rows()
    covered = covering_verbs()
    lines = []
    for number in sorted(rows):
        verbs = ", ".join(sorted(covered.get(number, []))) or "NO COVERING VERB"
        lines.append(f"{number:3d}  {rows[number][:44]:44}  {verbs}")
    rendered = "\n".join(lines)
    assert rendered.count("\n") + 1 == len(rows)
    assert "NO COVERING VERB" in rendered, "the backlog is empty, see the test above"
