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

_CARD = re.compile(r"(?<![\w-])(?:[UA]\d+|R-\d+|#\d+)\b")
_DASHES = ("—", "–", "--")


@pytest.fixture(scope="module")
def text() -> str:
    return SKILL.read_text()


@pytest.fixture(scope="module")
def flat(text) -> str:
    """The text with every run of white space one space, for phrases a line wraps."""
    return re.sub(r"\s+", " ", text)


def _frontmatter(text: str) -> dict[str, str]:
    """The frontmatter's top level keys, each value on its one line."""
    block = _FRONTMATTER.match(text)
    assert block, "no frontmatter"
    return dict(line.split(": ", 1) for line in block.group(1).splitlines() if ": " in line)


def test_the_skill_passes_the_shipped_skills_lint(tmp_path):
    """Frontmatter, every crate line parsed by the real parser, no personal literal."""
    shutil.copytree(SKILL_DIR, tmp_path / SKILL_DIR.name)
    assert lint_skills(tmp_path, _real_scripts()) == []


def test_every_crate_command_it_names_parses(text):
    """Anti vacuity for the lint, whose parse reads only fenced and indented lines.

    The skill names its crate commands inline and leaves the steps that run
    them to the skills that own them, so each inline span is parsed here by the
    real parser instead, and a verb renamed under it fails.
    """
    spans = sorted(set(re.findall(r"`(crate [^`]+)`", text)))
    assert {"crate --version", "crate backup run", "crate session ack"} <= set(spans)
    parser = real_parser()
    for span in spans:
        with pytest.raises(SystemExit) as stop:
            parser.parse_args([*span.split()[1:], "--help"])
        assert stop.value.code == 0, span


def test_the_frontmatter_names_the_skill_and_says_when_to_use_it(text):
    fields = _frontmatter(text)
    assert fields["name"] == SKILL_DIR.name == "attended-orchestrator"
    description = fields["description"]
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
    # Not repeated: the visit's analysis settings and the pass's landing gate
    # are each the owning skill's, and neither is spelled here.
    for owned in ("Analysis Mode", "High precision", "intake.land.native", "--rehearse"):
        assert owned not in flat, owned


def test_the_worker_rules_ship_beside_it_and_are_copied_into_the_state_folder(flat):
    assert WORKER.is_file()
    worker = WORKER.read_text()
    assert worker.startswith("# Cratekit attended worker\n")
    assert "`WORKER.md`" in flat and "copy this skill's `WORKER.md`" in flat
    # The placeholder the orchestrator writes the date into on the copy.
    assert ".local/attended/<DATE>/" in worker
    for never in ("commit", "push", "desktop control", "answer a gate", "beat grid"):
        assert never in worker, never


def test_the_state_folder_is_under_an_ignored_directory(text):
    assert ".local/attended/<DATE>/" in text
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
    about the prose around it.
    """
    body = re.sub(r"\A---\n|\n---\n", "\n", body, count=2)
    body = re.sub(r"(?:```|~~~).*?(?:```|~~~)", "", body, flags=re.DOTALL)
    body = re.sub(r"^ {4,}\S.*$", "", body, flags=re.M)
    return re.sub(r"`[^`\n]+`", "", body)


def test_no_dash_and_no_personal_literal_in_either_file(text):
    for path, body in ((SKILL, text), (WORKER, WORKER.read_text())):
        prose = _prose(body)
        for dash in _DASHES:
            assert dash not in prose, (path.name, dash)
        violations = scan.portability_violations(
            body, identity_tokens=scan.machine_identity_tokens()
        )
        assert violations == [], (path.name, violations)


def test_the_prose_reader_still_sees_a_dash_outside_code():
    """Anti vacuity: the reader that strips code leaves a dash in prose standing."""
    sample = "---\nname: x\n---\n\nRun `crate --version`, then wait\u2014no.\n"
    assert "\u2014" in _prose(sample) and "--" not in _prose(sample)


def test_the_docs_name_it_as_how_a_whole_sitting_runs():
    """Docs always current: CLAUDE.md and METHOD-local each name the skill."""
    for doc in ("CLAUDE.md", "docs/METHOD-local.md"):
        assert "`attended-orchestrator` skill" in (REPO_ROOT / doc).read_text(), doc
