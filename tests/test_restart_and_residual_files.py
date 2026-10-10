"""U124: the restart state and the residuals are per unit files.

Every unit used to append a paragraph to the head of ``RESTART-cratekit.md``
and number its residuals in ``docs/residual-findings.md``, so two branches cut
from one base conflicted in both files, and a residual's number was taken by
whoever FILED rather than by whoever landed. A unit's restart paragraph is now
``docs/restart/<unit>.md``, and a residual waits unnumbered in
``docs/residuals/`` until ``board.py residuals --land`` numbers it on main.

The scripts are loaded by path, the way ``tests/test_pending_units.py`` loads
them, because they are not part of the distribution.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The main commit U124 split ``RESTART-cratekit.md`` from. Pinned because the
#: byte identity of the move is a statement about that one text.
SPLIT_BASE = "a984968"


def _load(name: str):
    path = REPO_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"{name}_under_test_u124", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _residual(title: str, found: str = "at the review of #1, U1, 2026-10-09.", **extra) -> str:
    meta = "".join(f"{k}: {v}\n" for k, v in {"title": title, "found": found, **extra}.items())
    return f"---\n{meta}---\n\n**The mechanism.** {title}.\n\n**Closes when:** never.\n"


LEDGER_TEXT = (
    "# Residual findings\n\n---\n\n"
    "## R-5. An older finding\n\n**Found:** long ago.\n\nBody.\n\n"
    "## R-12. The highest, past a gap\n\n**Found:** later.\n\nBody.\n"
)


def _run(root: Path):
    def run(*argv: str) -> subprocess.CompletedProcess:
        return subprocess.run(argv, cwd=root, capture_output=True, text=True, check=False)

    return run


def _seed(root: Path):
    """A repository holding a restart file and a ledger, one commit on main."""
    root.mkdir(parents=True)
    run = _run(root)
    for argv in (
        ("git", "init", "-q", "-b", "main"),
        ("git", "config", "user.email", "fixture@example.invalid"),
        ("git", "config", "user.name", "Fixture"),
        ("git", "config", "commit.gpgsign", "false"),
    ):
        assert run(*argv).returncode == 0
    (root / "docs" / "restart").mkdir(parents=True)
    (root / "docs" / "residuals").mkdir()
    (root / "docs" / "residual-findings.md").write_text(LEDGER_TEXT)
    (root / "RESTART-cratekit.md").write_text("# Restart\n\n## What is open\n\nNothing.\n")
    (root / "docs" / "restart" / "u1.md").write_text("**U1 built.** First.\n")
    assert run("git", "add", "-A").returncode == 0
    assert run("git", "commit", "-q", "--no-verify", "-m", "seed").returncode == 0
    return run


def _unit_branch(run, root: Path, unit: int) -> None:
    """One unit's record, built the new way: a fragment and a residual file."""
    assert run("git", "checkout", "-q", "-b", f"unit/{unit}", "main").returncode == 0
    (root / "docs" / "restart" / f"u{unit}.md").write_text(f"**U{unit} built.** Its record.\n")
    # Git keeps no empty folder, so the checkout back to main removed it.
    folder = root / "docs" / "residuals"
    folder.mkdir(exist_ok=True)
    (folder / f"u{unit}-a-finding.md").write_text(
        _residual(f"Unit {unit} left a finding")
    )
    assert run("git", "add", "-A").returncode == 0
    assert run("git", "commit", "-q", "--no-verify", "-m", f"u{unit}").returncode == 0
    assert run("git", "checkout", "-q", "main").returncode == 0


@pytest.mark.parametrize("order", [("unit/2", "unit/3"), ("unit/3", "unit/2")])
def test_two_units_built_from_one_base_land_in_either_order(order, tmp_path, monkeypatch):
    """The goal of the unit, driven through git rather than asserted of a layout.

    Both branches are cut from the same main, each adds a restart fragment and
    a residual file, and both merge without a conflict whichever lands first.
    The numbers are then given at landing, past the ledger's highest, and the
    one that landed first does not get a lower number for filing first: name
    order decides within one landing, and that is the same for either order.
    """
    board = _load("board")
    root = tmp_path / "repo"
    run = _seed(root)
    _unit_branch(run, root, 2)
    _unit_branch(run, root, 3)

    for branch in order:
        merged = run("git", "merge", "--no-ff", "--no-edit", "-q", branch)
        assert merged.returncode == 0, f"merging {branch} conflicted: {merged.stdout}{merged.stderr}"

    assert (root / "docs" / "restart" / "u2.md").read_text() == "**U2 built.** Its record.\n"
    assert (root / "docs" / "restart" / "u3.md").read_text() == "**U3 built.** Its record.\n"

    ledger = root / "docs" / "residual-findings.md"
    folder = root / "docs" / "residuals"
    landed = board.land_residuals(ledger, folder)
    assert landed == [
        (13, "Unit 2 left a finding", False),
        (14, "Unit 3 left a finding", False),
    ]
    assert board.residual_titles(ledger)[13] == "Unit 2 left a finding"
    assert board.residual_files(folder) == []


def test_the_number_given_at_landing_is_one_past_the_ledgers_highest(tmp_path):
    """Past the highest, not past the count and not into a gap.

    The fixture ledger holds R-5 and R-12, so a count would give 3 and a gap
    filler would give 6. A second landing continues from what the first wrote.
    """
    board = _load("board")
    ledger = tmp_path / "ledger.md"
    ledger.write_text(LEDGER_TEXT)
    folder = tmp_path / "residuals"
    folder.mkdir()
    (folder / "README.md").write_text("not a residual\n")
    (folder / "u9-b.md").write_text(_residual("The second by name", issue="yes"))
    (folder / "u9-a.md").write_text(_residual("The first by name"))

    assert board.land_residuals(ledger, folder) == [
        (13, "The first by name", False),
        (14, "The second by name", True),
    ]
    text = ledger.read_text()
    assert text.endswith(
        "## R-14. The second by name\n\n"
        "**Found:** at the review of #1, U1, 2026-10-09.\n\n"
        "**The mechanism.** The second by name.\n\n**Closes when:** never.\n"
    )
    assert "Body.\n\n---\n\n## R-13. The first by name\n" in text
    assert "never.\n\n---\n\n## R-14. The second by name\n" in text
    assert [p.name for p in folder.iterdir()] == ["README.md"]

    (folder / "u10-c.md").write_text(_residual("A later landing"))
    assert board.land_residuals(ledger, folder) == [(15, "A later landing", False)]


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("**The mechanism.** No frontmatter at all.\n", "does not open"),
        ("title: T\nfound: today.\n---\n\nBody.\n", "does not open"),
        ("---\ntitle: Never closed\nfound: today.\n", "never closed"),
        ("---\nfound: today.\n---\n\nBody.\n", "no title"),
        ("---\ntitle: No found line\n---\n\nBody.\n", "no found"),
        ("---\ntitle: T\nfound: today.\nfond: typo\n---\n\nBody.\n", "fond"),
        ("---\ntitle: T\nfound: today.\nissue: maybe\n---\n\nBody.\n", "issue"),
        ("---\ntitle: R-12. Numbered by its filer\nfound: today.\n---\n\nBody.\n", "number"),
        ("---\ntitle: T\nfound: today.\n---\n\n\n", "no body"),
    ],
)
def test_a_residual_file_the_landing_could_not_read_is_named(text, reason, tmp_path):
    board = _load("board")
    (tmp_path / "u1-x.md").write_text(text)
    problems = board.residual_file_problems(tmp_path)
    assert len(problems) == 1 and reason in problems[0], problems


def test_a_title_citing_another_residual_is_not_a_number(tmp_path):
    """The ledger holds headings like "R-204 is discharged by half"."""
    board = _load("board")
    (tmp_path / "u1-x.md").write_text(_residual("R-204 is discharged by half"))
    assert board.residual_file_problems(tmp_path) == []


def test_a_file_that_landed_once_is_not_numbered_again(tmp_path):
    """A branch edit after the landing can bring a deleted file back."""
    board = _load("board")
    ledger = tmp_path / "ledger.md"
    ledger.write_text(LEDGER_TEXT)
    folder = tmp_path / "residuals"
    folder.mkdir()
    (folder / "u1-a.md").write_text(_residual("The highest, past a gap"))
    with pytest.raises(ValueError, match="R-12 already"):
        board.land_residuals(ledger, folder)
    assert ledger.read_text() == LEDGER_TEXT


def test_an_untracked_draft_is_neither_judged_nor_landed(tmp_path):
    """Only what git knows is filed. A draft blocked every unrelated commit."""
    board = _load("board")
    root = tmp_path / "repo"
    run = _seed(root)
    folder = root / "docs" / "residuals"
    (folder / "u1-draft.md").write_text("half written\n")
    assert board.residual_file_problems(folder) == []
    (folder / "u1-filed.md").write_text(_residual("Filed and committed"))
    assert run("git", "add", "docs/residuals/u1-filed.md").returncode == 0
    assert [p.name for p in board.residual_files(folder)] == ["u1-filed.md"]
    assert board.land_residuals(root / "docs" / "residual-findings.md", folder) == [
        (13, "Filed and committed", False)
    ]
    assert (folder / "u1-draft.md").exists()


def test_a_malformed_file_lands_nothing(tmp_path):
    """Validated before anything is written, so the ledger and folder are untouched."""
    board = _load("board")
    ledger = tmp_path / "ledger.md"
    ledger.write_text(LEDGER_TEXT)
    folder = tmp_path / "residuals"
    folder.mkdir()
    (folder / "u1-a.md").write_text(_residual("Fine on its own"))
    (folder / "u1-b.md").write_text("no frontmatter\n")
    with pytest.raises(ValueError, match="u1-b.md"):
        board.land_residuals(ledger, folder)
    assert ledger.read_text() == LEDGER_TEXT
    assert sorted(p.name for p in folder.iterdir()) == ["u1-a.md", "u1-b.md"]


class _ClosingArgs:
    def __init__(self, *, since=None, message_file=None):
        self.since = since
        self.message_file = message_file


@pytest.mark.parametrize("path", ["hook", "range"])
def test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter(
    path, tmp_path, monkeypatch
):
    """Both paths the check runs on: the commit-msg hook and CI's pushed range.

    The message itself is clean and the register owes nothing, so the only
    thing that can refuse is the residual file. A good file in its place passes.
    """
    board = _load("board")
    folder = tmp_path / "residuals"
    folder.mkdir()
    monkeypatch.setattr(board, "RESIDUALS_DIR", folder)
    monkeypatch.setattr(board, "owed_by_unit", lambda: {})
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text("docs(u1): the record\n")
    if path == "hook":
        args = _ClosingArgs(message_file=str(message))
    else:
        root = tmp_path / "repo"
        _seed(root)
        monkeypatch.chdir(root)
        args = _ClosingArgs(since="HEAD")

    (folder / "u1-a.md").write_text("---\ntitle: A finding with no Found line\n---\n\nBody.\n")
    assert board.cmd_closing(args) == 2

    (folder / "u1-a.md").write_text(_residual("A finding with its Found line"))
    assert board.cmd_closing(args) == 0


def test_an_unreadable_range_still_refuses_a_malformed_residual_file(tmp_path, monkeypatch):
    board = _load("board")
    folder = tmp_path / "residuals"
    folder.mkdir()
    (folder / "u1-a.md").write_text("no frontmatter\n")
    monkeypatch.setattr(board, "RESIDUALS_DIR", folder)
    empty = tmp_path / "not-a-repo"
    empty.mkdir()
    monkeypatch.chdir(empty)
    assert board.cmd_closing(_ClosingArgs(since="deadbeef")) == 2


def test_the_landing_refuses_off_main(tmp_path, monkeypatch, capsys):
    """A number given on a branch is a number given by whoever filed."""
    board = _load("board")
    root = tmp_path / "repo"
    run = _seed(root)
    assert run("git", "checkout", "-q", "-b", "unit/9").returncode == 0
    folder = root / "docs" / "residuals"
    (folder / "u9-a.md").write_text(_residual("Filed on a branch"))
    assert run("git", "add", "-A").returncode == 0
    ledger = root / "docs" / "residual-findings.md"
    monkeypatch.setattr(board, "LEDGER", ledger)
    monkeypatch.setattr(board, "RESIDUALS_DIR", folder)

    class Args:
        land = True

    assert board.cmd_residuals(Args()) == 1
    assert "unit/9" in capsys.readouterr().err
    assert ledger.read_text() == LEDGER_TEXT

    assert run("git", "commit", "-q", "--no-verify", "-m", "u9").returncode == 0
    assert run("git", "checkout", "-q", "main").returncode == 0
    assert run("git", "merge", "-q", "unit/9").returncode == 0

    # Behind the remote as last fetched: the highest read here may be stale.
    assert run("git", "update-ref", "refs/remotes/origin/main", "unit/9").returncode == 0
    assert run("git", "reset", "-q", "--hard", "HEAD~1").returncode == 0
    assert board.cmd_residuals(Args()) == 1
    assert "behind origin/main" in capsys.readouterr().err
    assert run("git", "merge", "-q", "unit/9").returncode == 0

    assert board.cmd_residuals(Args()) == 0
    assert board.residual_titles(ledger)[13] == "Filed on a branch"


def test_the_shipped_residual_folder_holds_only_files_that_can_land():
    board = _load("board")
    assert board.residual_file_problems() == []


# --------------------------------------------------------------------------
# the restart state


def _restart_text() -> str:
    return (REPO_ROOT / "RESTART-cratekit.md").read_text()


def test_the_restart_state_as_shipped_passes_its_own_scan():
    scan = _load("scan_repo")
    assert scan.restart_violations("RESTART-cratekit.md", _restart_text()) == []


@pytest.mark.parametrize(
    ("edit", "says"),
    [
        (
            lambda t: t.replace(
                "## Main, verify",
                "**U999 built, 2026-10-10, on `relay/999`.** A record.\n\n## Main, verify",
                1,
            ),
            "head",
        ),
        (
            lambda t: t.replace(
                "## Main, verify",
                "A plain paragraph somebody added.\n\n## Main, verify",
                1,
            ),
            "head",
        ),
        (lambda t: t + "\n## What U999 left behind\n\nThree residuals.\n", "U999"),
        (
            lambda t: t.replace(
                "## What is open\n",
                "## What is open\n\n**R-999 built, 2026-10-10.** A record.\n",
                1,
            ),
            "opens a unit's record",
        ),
        (
            lambda t: t.replace(
                "## What is open\n",
                "## What is open\n\n**Sitting 99, 2026-10-10, attended.** A record.\n",
                1,
            ),
            "opens a unit's record",
        ),
    ],
)
def test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan(edit, says, tmp_path):
    """Driven through ``scan_tree``, the function the hook and CI call."""
    scan = _load("scan_repo")
    edited = edit(_restart_text())
    assert edited != _restart_text()
    path = tmp_path / "RESTART-cratekit.md"
    path.write_text(edited)
    findings = scan.scan_tree(tmp_path, [path], check_identity=False)
    assert findings and any(says in f for f in findings), findings
    assert all(f.startswith("RESTART-cratekit.md: ") for f in findings)


def test_the_scan_judges_no_other_file_by_the_restart_rule(tmp_path):
    scan = _load("scan_repo")
    path = tmp_path / "docs" / "restart" / "u999.md"
    path.parent.mkdir(parents=True)
    path.write_text("**U999 built, 2026-10-10, on `relay/999`.** A record.\n")
    assert scan.scan_tree(tmp_path, [path], check_identity=False) == []


def _paragraphs(text: str) -> list[str]:
    return [p for p in text.split("\n\n") if p.strip()]


def test_every_moved_paragraph_is_in_a_fragment_byte_for_byte():
    """The split moved text and changed none of it.

    Every paragraph of the restart state at the split base that is not in the
    restart state now is found verbatim in some ``docs/restart/`` file. A
    paragraph can only be split at a blank line, and the split moved whole
    records, so a paragraph is the unit of comparison. "Moved" is read off the
    base's own layout, everything outside the sections the restart state
    keeps, so a later edit to a kept section is not mistaken for a lost
    record. The base commit is on main's history, so a clone without it is a
    shallow one, and CI does not run the suite.
    """
    shown = subprocess.run(
        ["git", "show", f"{SPLIT_BASE}:RESTART-cratekit.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert shown.returncode == 0, f"the split base {SPLIT_BASE} is not in this clone"
    scan = _load("scan_repo")
    sections = re.split(r"\n(?=## )", shown.stdout)
    # The head kept its title and its first paragraph; the rest was records.
    moved = _paragraphs(sections[0])[2:]
    for section in sections[1:]:
        heading = section.split("\n", 1)[0]
        if heading == "## Main, verify before trusting it":
            # The heading and the command block stayed.
            moved += _paragraphs(section)[2:]
        elif heading not in scan.RESTART_SECTIONS:
            moved += _paragraphs(section)
    fragments = "\n\n".join(
        p.read_text() for p in sorted((REPO_ROOT / "docs" / "restart").glob("*.md"))
    )
    assert len(moved) > 250
    lost = [p[:80] for p in moved if p not in fragments]
    assert lost == []
