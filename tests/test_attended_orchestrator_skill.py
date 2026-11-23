"""U316: the attended-orchestrator skill is a project skill that lints clean.

It is text, so nothing breaks when it rots: it must never say a step another
skill owns, name a card the board should be read for, or carry a personal
literal into a public repository. Each is read here from the files themselves.
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

#: The card numbers the skill may name, whose rules are about them by nature: U29,
#: the cutover, and A5, the live proofs it reads, each by number and issue.
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
    """The frontmatter's keys and lines, read line by line since PyYAML is not declared."""
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
    """Anti vacuity for the lint: each inline crate span goes through its parse, so
    a renamed verb or flag fails."""
    spans = _spans(text)
    worker = _spans(WORKER.read_text())
    assert {
        "crate --version",
        "crate backup run",
        "crate backup run --job ID",
        "crate session ack",
    } <= set(spans)
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
    # Not repeated: each owning skill's steps, by the commands and fields that
    # spell them; the skill points to their owners instead.
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
    # The placeholder the orchestrator writes the date and sitting into on the copy.
    assert ".local/attended/<DATE>-s<N>/" in worker
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
    assert "folder inside" in flat and "`.local/attended/<DATE>-s<N>/`" in flat
    # Every place the folder is spelled, the wait loop included, is under .local.
    for body in (text, WORKER.read_text()):
        places = re.findall(r"(\S*)attended/<DATE>-s<N>/", body)
        assert places and all(p.lstrip("`").endswith(".local/") for p in places), places
    probe = ".local/attended/2026-11-21-s103/STATE.md"
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
    """The text without frontmatter fences, code blocks and spans, which may wrap a
    line; a flag's double hyphen is code, and the house rule is about prose."""
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


def _section(text: str, heading: str) -> str:
    """One bold headed paragraph of the skill, to the next bold or section heading."""
    start = text.index(heading)
    ends = [i for i in (text.find(m, start + len(heading)) for m in ("\n\n**", "\n## ")) if i != -1]
    return " ".join(text[start : min(ends) if ends else None].split())


def test_the_state_folder_carries_the_sitting_number_and_a_fresh_one_resumes(flat):
    """Two sittings on one day never share a folder (U321, sitting 102)."""
    worker = " ".join(WORKER.read_text().split())
    for body in (flat, worker):
        assert "attended/<DATE>-s<N>/" in body
        assert "attended/<DATE>/" not in body
    assert "`<N>` the sitting number, this sitting's own" in flat
    # The resume reads the folder whose ledger is not at its end state, and the
    # end state is one the ledger can be read for.
    assert flat.count("`none, the sitting is over`") == 2, "the ledger's line and the end step"
    assert "a folder named by date alone predates this form and is finished" in flat
    assert "resumes from the folder whose STATE.md is not at its end state" in flat


def test_each_kickoff_line_goes_to_the_clipboard_one_at_a_time(text, flat):
    """Printed lines Phillip could not see to copy, so each is put on the clipboard."""
    kickoff = (
        "You are Cratekit attended worker W1. Read .local/attended/<DATE>-s<N>/WORKER.md "
        "and follow it."
    )
    assert f"    {kickoff}\n" in text, "the printed kickoff line"
    assert f"printf '%s' '{kickoff}' | pbcopy" in text, "the clipboard command"
    assert "W1's first, and W2's once he says W1's is pasted" in flat
    # A replacement worker's line goes the same way.
    assert "printed and put on the clipboard as Starting the workers says" in _section(
        text, "**Keeping context small.**"
    )


def test_copies_go_on_the_library_volume_and_never_in_the_state_folder(text, flat):
    """The checkout is mirrored to Google Drive, so no audio or database copy sits in it."""
    worker = " ".join(WORKER.read_text().split())
    for body in (flat, worker):
        assert "one level down in the library volume's scratch folder" in body
        assert "mirrored to Google Drive" in body
        assert "the volume copies folder" in body
    assert (
        "The state folder keeps orders, reports, STATE.md, JSON summaries and the throwaway audio only."
        in flat
    )
    # The sweep and the settlement each name the volume, and the end deletes it.
    for heading in (
        "**Who does what.**",
        "**Sweeps and other reads on copies",
        "**Settlements in rekordbox",
    ):
        assert "the volume copies folder" in _section(text, heading), heading
    assert "the volume copies folder deleted" in flat and "the throwaway audio deleted" in flat
    assert "an order names it to the worker" in flat
    # The old places that sent a copy into the state folder are gone, each one.
    for old in ("copies in `scratch/`", "temporary copies", "to copy them into scratch/"):
        assert old not in flat and old not in worker, old
    assert (
        "scratch/ keeps reports, JSON summaries, long output and the throwaway audio only" in worker
    )


def test_a_worker_reads_a_database_copy_and_never_the_live_file():
    worker = " ".join(WORKER.read_text().split())
    assert (
        "a dated backup the orchestrator made, fetched read only from the backup remote" in worker
    )
    assert "the disposable copy run CLAUDE.md describes" in worker
    assert "Never a direct read of the live database file by you." in worker


def test_the_backup_from_a_session_is_driven_by_its_job(flat):
    """With no terminal the verb only queues; the job it prints is driven under nohup."""
    assert "`crate backup run --job ID` under `nohup`" in flat
    assert "only queues, with a terminal or without" in flat
    assert "queues its job, prints the job's identifier and exits" in flat
    assert "waits on that process, and read the job's result" in flat
    # A BEFORE over an unchanged database is the newest earlier snapshot.
    assert "a database portion that reads `unchanged` made no new snapshot" in flat


def test_the_worker_takes_the_conservative_reading_and_names_no_personal_literal():
    worker = " ".join(WORKER.read_text().split())
    assert "no library paths, absolute home paths, credentials or personal data" in worker
    # The report's draft keeps the same rule, where the brief's "no paths" stood.
    assert "with no dashes and no library paths, absolute home paths or personal data" in worker
    assert "take the conservative reading" in worker
    assert "the orchestrator's to take, not yours" in worker


def test_ask_nothing_departs_from_the_stop_and_nothing_else(text):
    ask = _section(text, "**Ask nothing.**")
    assert "the one place" not in ask
    assert "departs from CLAUDE.md's stop" in ask
    assert "a worker still takes the conservative reading" in ask


def test_settlements_stay_inside_claude_md_and_their_throwaway_can_be_analysed(text):
    """The skill points to CLAUDE.md's clause, which carries the list (U321, R-1754)."""
    claude = " ".join((REPO_ROOT / "CLAUDE.md").read_text().split())
    assert (
        "Where an attended card asks what rekordbox itself writes, it may also "
        "make, on a throwaway track and a playlist made by hand for the check, "
        "the change that card names"
    ) in claude
    assert (
        "(removing it from the collection, setting cues, playing it on a deck, deleting "
        "that playlist), and may change an analysis setting a probe names and put it back "
        "to Phillip's standard, read back by a screenshot; never on a real track, and never "
        "a change the card does not name"
    ) in claude
    settle = _section(text, "**Settlements in rekordbox")
    assert "only what CLAUDE.md's rekordbox constraint allows" in settle
    assert "silent unless the card needs it analysed, and then a click track" in settle
    assert "ten second silent AIFF" not in settle
    assert "never touches a real track" in settle
    assert "A probe changes only the setting it names" in " ".join(text.split())


def test_a_cutover_line_is_proven_live_until_phillip_has_lived_on_it(text):
    u29 = _section(text, "**U29 (#29), the cutover")
    assert '"proven live"' in u29
    assert 'moves to "cut over" only on Phillip\'s word that he has lived on' in u29
    assert "quotes him and names the sitting" in u29
    cutover = (REPO_ROOT / "docs" / "cutover.md").read_text()
    blocks = cutover[
        cutover.index("## What blocks retiring DJ_tools") : cutover.index("## Sitting 43,")
    ]
    flat_blocks = " ".join(blocks.split())
    assert "Sitting 101's 19 per workflow lines" in flat_blocks
    assert "read as proven live until Phillip says he has lived on each" in flat_blocks
    assert 'From U321 a sitting writes "proven live"' in flat_blocks
