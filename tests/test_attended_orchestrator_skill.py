"""U316: the attended-orchestrator skill is a project skill that lints clean.

The skill is the text one attended session on Phillip's Mac follows to drive
every open attended card with worker sessions. It is text, so nothing breaks
when it rots, and what it must never do is say a step another skill owns, name
a card the board should be read for, or carry a personal literal into a
public repository. Each of those is read here from the files themselves: the
shipped skills lint over the folder (frontmatter, every crate line parsed by
the real parser, the portability scan), the description's length, the three
skills it points to by name, the worker rules beside it, the ignored state
folder, the only card numbers it may name, and no dash in its prose.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from tests.test_skills_lint import (
    _FRONTMATTER,
    _real_scripts,
    _verb_problems,
    lint_skills,
    real_parser,
    scan,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "attended-orchestrator"
SKILL = SKILL_DIR / "SKILL.md"
WORKER = SKILL_DIR / "WORKER.md"

#: The one length a skill description is held to by the harness that loads it.
DESCRIPTION_LIMIT = 1024

#: The card numbers the skill may name, whose rules are about them by nature:
#: U29, the cutover, by unit and issue, and A5, the live proofs it reads, by
#: attended number and issue. Anything else is a card the board should be read for.
ALLOWED_CARDS = {"U29", "#29", "A5", "#178"}

#: A card in any of the forms a brief or a record writes one: U29, u287, A 178,
#: A-178, R-1631, #29, issue 838. A markdown heading's ``## 1.`` is not one.
_CARD = re.compile(
    r"(?<![\w-])(?:[UuAaRr][ -]?\d+|#\d+|issues?\s+\d+)\b",
)


@pytest.fixture(scope="module")
def text() -> str:
    return SKILL.read_text()


@pytest.fixture(scope="module")
def flat(text) -> str:
    """The text with every run of white space one space, for phrases a line wraps."""
    return re.sub(r"\s+", " ", text)


def _frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """The frontmatter's keys, one per line as the loader reads them, and its lines.

    PyYAML is not a declared dependency, so the block is read line by line, and
    the test below holds it to one line a key, where that reading is YAML's.
    """
    block = _FRONTMATTER.match(text)
    assert block, "no frontmatter"
    lines = block.group(1).splitlines()
    return dict(line.split(": ", 1) for line in lines if ": " in line), lines


def _spans(body: str) -> list[str]:
    """Every inline crate command, a span wrapped across a line joined back."""
    return sorted({" ".join(span.split()) for span in re.findall(r"`(crate\s[^`]+)`", body)})


def test_the_skill_passes_the_shipped_skills_lint(tmp_path):
    """Frontmatter, every crate line parsed by the real parser, no personal literal."""
    shutil.copytree(SKILL_DIR, tmp_path / SKILL_DIR.name)
    assert lint_skills(tmp_path, _real_scripts()) == []


def test_every_crate_command_it_names_parses(text):
    """Anti vacuity for the lint, whose parse reads only fenced and indented lines.

    The skill and its worker rules name their crate commands inline and leave
    the steps that run them to the skills that own them, so each inline span is
    put through the lint's own parse instead, and a verb or a flag renamed
    under it fails.
    """
    spans = _spans(text)
    worker = _spans(WORKER.read_text())
    assert {"crate --version", "crate backup run", "crate session ack"} <= set(spans)
    assert worker == ["crate backup run"], worker
    for span in spans + worker:
        assert _verb_problems(span, SKILL_DIR.name, real_parser) == [], span


def test_the_span_parse_refuses_a_flag_the_verb_does_not_take():
    """Anti vacuity: the parse above answers a bogus flag as a problem."""
    assert _verb_problems("crate backup run --bogus", SKILL_DIR.name, real_parser)


def test_the_frontmatter_names_the_skill_and_says_when_to_use_it(text):
    fields, lines = _frontmatter(text)
    assert set(fields) == {"name", "description"}, fields
    assert fields["name"] == SKILL_DIR.name == "attended-orchestrator"
    description = fields["description"]
    # One line each, so the length read is the length a loader reads.
    assert len(lines) == 2 and lines[1] == f"description: {description}", lines
    assert len(description) < DESCRIPTION_LIMIT, len(description)
    for phrase in (
        "/attended-orchestrator",
        "run the attended work",
        "work the attended cards",
        "start an attended sitting",
    ):
        assert phrase in description, phrase


def test_it_points_to_the_skills_that_own_their_steps(flat):
    """The visit, the pass and a new card are other skills', named and not repeated."""
    for skill in ("rekordbox-visit", "crate-sync", "file-card"):
        assert f"`{skill}` skill" in flat, skill
        assert (REPO_ROOT / ".claude" / "skills" / skill / "SKILL.md").is_file(), skill
    # Not repeated: each owning skill's steps, by the commands and fields
    # that spell them, none of them here. The original prompt carried the
    # first four, and the skill points to their owners instead.
    owned = (
        "crate job list",  # both preflights
        "pgrep -x",  # the visit's check that rekordbox is gone
        "/mcp",  # the visit's release of the desktop control lock
        "sort -t U",  # file-card's next U number
        "Analysis Mode",  # the visit's settings
        "High precision",
        "Analyze Track",
        "inbox analyzed",  # the visit's clear
        "analyze check",
        "sync land",  # the pass
        "intake.land.native",
        "--rehearse",
        "organize --only",
        "**Depends on:**",  # file-card's body form
        "labels[]=unit",
    )
    worker = WORKER.read_text()
    for step in owned:
        assert step not in flat and step not in worker, step


def test_the_worker_rules_ship_beside_it_and_are_copied_into_the_state_folder(flat):
    assert WORKER.is_file()
    worker = WORKER.read_text()
    assert worker.startswith("# Cratekit attended worker\n")
    assert "`WORKER.md`" in flat and "copy this skill's `WORKER.md`" in flat
    # The placeholder the orchestrator writes the date into on the copy.
    assert ".local/attended/<DATE>/" in worker
    flat_worker = " ".join(worker.split())
    for rule in (
        "never write a beat grid",
        "never open rekordbox or its agent",
        "never touch the live rekordbox database",
        "only with rekordbox and rekordboxAgent both confirmed gone",
        "DJ_tools is read only",
        "You never commit, push, pull, check out, comment on or close a card, use "
        "desktop control, run `crate backup run`, answer a gate, or run a verb "
        "against the live database.",
        "Never ask Phillip anything.",
    ):
        assert rule in flat_worker, rule


def test_the_state_folder_is_under_an_ignored_directory(text):
    flat = " ".join(text.split())
    assert "the checkout's ignored `.local/` directory" in flat
    assert "folder inside" in flat and "`.local/attended/<DATE>/`" in flat
    # Every place the folder is spelled, the wait loop included, is under .local.
    for body in (text, WORKER.read_text()):
        places = re.findall(r"(\S*)attended/<DATE>/", body)
        assert places and all(p.lstrip("`").endswith(".local/") for p in places), places
    probe = ".local/attended/2026-11-21/STATE.md"
    ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", probe], cwd=REPO_ROOT, check=False
    )
    assert ignored.returncode == 0, "the state folder is not ignored"


def test_it_names_no_card_but_u29_and_a5(text):
    """The board is read fresh, so no card is named but the two whose rules are theirs."""
    for path, body in ((SKILL, text), (WORKER, WORKER.read_text())):
        named = set(_CARD.findall(body))
        assert named <= ALLOWED_CARDS, (path.name, sorted(named - ALLOWED_CARDS))
    assert {"U29", "#29", "A5", "#178"} <= set(_CARD.findall(text))


def test_it_says_the_four_things_it_never_does(flat):
    for never in (
        "never cuts a release",
        "never writes the decisions page",
        "never retires, moves, disables or changes anything of DJ_tools",
        "never starts a restore onto a drive",
    ):
        assert never in flat, never


def _prose(body: str) -> str:
    """The text with its frontmatter fences and every code block and span taken out.

    A flag is code, and its double hyphen is the parser's; the house rule is
    about the prose around it. A span may wrap across a line, as markdown
    allows, so the span pattern crosses one.
    """
    body = re.sub(r"\A---\n|\n---\n", "\n", body, count=2)
    body = re.sub(r"(?:```|~~~).*?(?:```|~~~)", "", body, flags=re.DOTALL)
    body = re.sub(r"^ {4,}\S.*$", "", body, flags=re.M)
    return re.sub(r"`[^`]+`", "", body)


def test_no_dash_and_no_personal_literal_in_either_file(text):
    """No em or en dash anywhere, code included, and no double hyphen in prose."""
    for path, body in ((SKILL, text), (WORKER, WORKER.read_text())):
        for dash in ("\u2014", "\u2013"):
            assert dash not in body, (path.name, dash)
        assert "--" not in _prose(body), path.name
        violations = scan.portability_violations(
            body, identity_tokens=scan.machine_identity_tokens()
        )
        assert violations == [], (path.name, violations)


def test_the_prose_reader_still_sees_a_dash_outside_code():
    """Anti vacuity: the reader that strips code leaves a dash in prose standing."""
    sample = "---\nname: x\n---\n\nRun `crate\n--version`, then wait -- no.\n"
    assert "--" in _prose(sample) and "version" not in _prose(sample)


def test_the_docs_name_it_as_how_a_whole_sitting_runs():
    """Docs always current: CLAUDE.md and METHOD-local each name the skill."""
    for doc, sentence in (
        (
            "CLAUDE.md",
            "A whole attended sitting, every open attended card driven with "
            "worker sessions, follows the project's `attended-orchestrator` skill (U316).",
        ),
        (
            "docs/METHOD-local.md",
            "A whole attended sitting, every open attended card at "
            "once with worker sessions Phillip starts, runs by the project's "
            "`attended-orchestrator` skill (U316)",
        ),
    ):
        flat = " ".join((REPO_ROOT / doc).read_text().split())
        assert sentence in flat, doc
