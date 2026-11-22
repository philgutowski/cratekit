"""U124: the restart state and the residuals are per unit files.

A restart paragraph is ``docs/restart/<unit>.md``, and a residual waits in
``docs/residuals/`` until ``scripts/board.py residuals --land`` numbers it on
main. ``scripts/scan_repo.py`` guards the restart state.
"""

from __future__ import annotations

import functools
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import NamedTuple

import pytest

from tests.test_board_reads import load_board as _load

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The main commit U124 split ``RESTART-cratekit.md`` from, the text the move is about.
SPLIT_BASE = "a984968"


@pytest.fixture
def board():
    return _load("board")


def _residual(title: str, found: str = "at the review of #1, U1, 2026-10-09.", **extra) -> str:
    meta = "".join(f"{k}: {v}\n" for k, v in {"title": title, "found": found, **extra}.items())
    return f"---\n{meta}---\n\n**The mechanism.** {title}.\n\n**Closes when:** never.\n"


LEDGER_TEXT = (
    "# Residual findings\n\n---\n\n"
    "## R-5. An older finding\n\n**Found:** long ago.\n\nBody.\n\n"
    "## R-12. The highest, past a gap\n\n**Found:** later.\n\nBody.\n"
)
NO_FOUND = "---\ntitle: A finding with no Found line\n---\n\nBody.\n"


def _seed(root: Path):
    """A repository holding a restart file and a ledger, one commit on main."""
    root.mkdir(parents=True)

    def run(*argv: str) -> subprocess.CompletedProcess:
        return subprocess.run(argv, cwd=root, capture_output=True, text=True, check=True)

    run("git", "init", "-q", "-b", "main")
    run("git", "config", "user.email", "fixture@example.invalid")
    run("git", "config", "user.name", "Fixture")
    run("git", "config", "commit.gpgsign", "false")
    (root / "docs" / "restart").mkdir(parents=True)
    (root / "docs" / "residuals").mkdir()
    (root / "docs" / "residual-findings.md").write_text(LEDGER_TEXT)
    (root / "RESTART-cratekit.md").write_text("# Restart\n\n## What is open\n\nNothing.\n")
    (root / "docs" / "restart" / "u1.md").write_text("**U1 built.** First.\n")
    _commit(run, "seed")
    return run


def _commit(run, message: str) -> None:
    run("git", "add", "-A")
    run("git", "commit", "-q", "--no-verify", "-m", message)


def _folder(tmp_path: Path, **files: str) -> tuple[Path, Path]:
    ledger = tmp_path / "ledger.md"
    ledger.write_text(LEDGER_TEXT)
    folder = tmp_path / "residuals"
    folder.mkdir()
    for name, text in files.items():
        (folder / f"{name}.md").write_text(text)
    return ledger, folder


@pytest.mark.parametrize("order", [("unit/2", "unit/3"), ("unit/3", "unit/2")])
def test_two_units_built_from_one_base_land_in_either_order(order, tmp_path, board):
    """Both branches merge without a conflict, and name order decides the numbers."""
    root = tmp_path / "repo"
    run = _seed(root)
    for unit in (2, 3):
        run("git", "checkout", "-q", "-b", f"unit/{unit}", "main")
        (root / "docs" / "restart" / f"u{unit}.md").write_text(f"**U{unit} built.** Its record.\n")
        # Git keeps no empty folder, so the checkout back to main removed it.
        folder = root / "docs" / "residuals"
        folder.mkdir(exist_ok=True)
        (folder / f"u{unit}-a-finding.md").write_text(
            _residual(f"Unit {unit} left a finding")
        )
        _commit(run, f"u{unit}")
        run("git", "checkout", "-q", "main")
    for branch in order:
        run("git", "merge", "--no-ff", "--no-edit", "-q", branch)  # raises on a conflict
    for unit in (2, 3):
        record = (root / "docs" / "restart" / f"u{unit}.md").read_text()
        assert record == f"**U{unit} built.** Its record.\n"
    ledger = root / "docs" / "residual-findings.md"
    folder = root / "docs" / "residuals"
    assert board.land_residuals(ledger, folder) == [
        (13, "Unit 2 left a finding", False),
        (14, "Unit 3 left a finding", False),
    ]
    assert board.residual_titles(ledger)[13] == "Unit 2 left a finding"
    assert board.residual_files(folder) == []


def test_the_number_given_at_landing_is_one_past_the_ledgers_highest(tmp_path, board):
    """Past R-12, the highest, not past the count of two and not into a gap."""
    ledger, folder = _folder(tmp_path, README="not a residual\n", **{
        "u9-b": _residual("The second by name", issue="yes"),
        "u9-a": _residual("The first by name"),
    })
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
        # A title citing another residual is not a number of its own.
        (_residual("R-204 is discharged by half"), None),
    ],
)
def test_a_residual_file_the_landing_could_not_read_is_named(text, reason, tmp_path, board):
    (tmp_path / "u1-x.md").write_text(text)
    problems = board.residual_file_problems(tmp_path)
    assert problems == [] if reason is None else len(problems) == 1 and reason in problems[0]


@pytest.mark.parametrize(
    ("files", "says"),
    [
        # A branch edit after the landing can bring a deleted file back.
        ({"u1-a": _residual("The highest, past a gap")}, "R-12 already"),
        # Validated before anything is written.
        ({"u1-a": _residual("Fine on its own"), "u1-b": "no frontmatter\n"}, "u1-b.md"),
    ],
)
def test_a_landing_that_cannot_number_every_file_writes_nothing(files, says, tmp_path, board):
    ledger, folder = _folder(tmp_path, **files)
    with pytest.raises(ValueError, match=says):
        board.land_residuals(ledger, folder)
    assert ledger.read_text() == LEDGER_TEXT
    assert sorted(p.name for p in folder.iterdir()) == sorted(f"{n}.md" for n in files)


def test_an_untracked_draft_is_neither_judged_nor_landed(tmp_path, board):
    """Only what git knows is filed. A draft blocked every unrelated commit."""
    root = tmp_path / "repo"
    run = _seed(root)
    folder = root / "docs" / "residuals"
    (folder / "u1-draft.md").write_text("half written\n")
    assert board.residual_file_problems(folder) == []
    (folder / "u1-filed.md").write_text(_residual("Filed and committed"))
    run("git", "add", "docs/residuals/u1-filed.md")
    assert [p.name for p in board.residual_files(folder)] == ["u1-filed.md"]
    assert board.land_residuals(root / "docs" / "residual-findings.md", folder) == [
        (13, "Filed and committed", False)
    ]
    assert (folder / "u1-draft.md").exists()


@pytest.mark.parametrize("path", ["hook", "range", "unreadable range"])
def test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter(
    path, tmp_path, monkeypatch, board
):
    """The hook, CI's pushed range, and a range it cannot read: the file alone refuses."""
    _, folder = _folder(tmp_path)
    monkeypatch.setattr(board, "RESIDUALS_DIR", folder)
    monkeypatch.setattr(board, "owed_by_unit", lambda: {})
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text("docs(u1): the record\n")
    args = SimpleNamespace(since="HEAD", message_file=None)
    if path == "hook":
        args.message_file = str(message)
    elif path == "range":
        _seed(tmp_path / "repo")
        monkeypatch.chdir(tmp_path / "repo")
    else:
        args.since = "deadbeef"
        monkeypatch.chdir(folder)
    (folder / "u1-a.md").write_text(NO_FOUND)
    assert board.cmd_closing(args) == 2
    (folder / "u1-a.md").write_text(_residual("A finding with its Found line"))
    assert board.cmd_closing(args) == 0


def test_the_landing_refuses_off_main_and_behind_origin(tmp_path, monkeypatch, capsys, board):
    """A number given on a branch, or behind the remote, may already be taken."""
    root = tmp_path / "repo"
    run = _seed(root)
    run("git", "checkout", "-q", "-b", "unit/9")
    folder = root / "docs" / "residuals"
    (folder / "u9-a.md").write_text(_residual("Filed on a branch"))
    run("git", "add", "-A")
    ledger = root / "docs" / "residual-findings.md"
    monkeypatch.setattr(board, "LEDGER", ledger)
    monkeypatch.setattr(board, "RESIDUALS_DIR", folder)
    land = SimpleNamespace(land=True)
    assert board.cmd_residuals(land) == 1
    assert "unit/9" in capsys.readouterr().err
    assert ledger.read_text() == LEDGER_TEXT

    run("git", "commit", "-q", "--no-verify", "-m", "u9")
    run("git", "checkout", "-q", "main")
    run("git", "update-ref", "refs/remotes/origin/main", "unit/9")
    assert board.cmd_residuals(land) == 1
    assert "behind origin/main" in capsys.readouterr().err
    run("git", "merge", "-q", "unit/9")
    assert board.cmd_residuals(land) == 0
    assert board.residual_titles(ledger)[13] == "Filed on a branch"


def test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction(
    tmp_path, monkeypatch, capsys, board
):
    """Everything else the audit reads matches, so the file alone moves the exit."""
    _, folder = _folder(tmp_path)
    monkeypatch.setattr(board, "RESIDUALS_DIR", folder)
    monkeypatch.setattr(board, "repo_slug", lambda: ("fixture", "cratekit"))
    monkeypatch.setattr(board, "load_issues", lambda: [])
    monkeypatch.setattr(board, "reconcile", lambda owner, apply, labels_only=False: [])
    monkeypatch.setattr(board, "owed_by_unit", lambda: {})
    args = SimpleNamespace(labels_only=True)
    (folder / "u1-a.md").write_text(_residual("Waiting for its number"))
    assert board.cmd_audit(args) == 0
    assert "1 residual file(s) in docs/residuals wait for a number" in capsys.readouterr().out
    (folder / "u1-a.md").write_text(NO_FOUND)
    assert board.cmd_audit(args) == 2
    assert "CANNOT LAND" in capsys.readouterr().out


def test_the_shipped_residual_folder_holds_only_files_that_can_land(board):
    assert board.residual_file_problems() == []


# U314: the ledger archived by number range in docs/ledger/.

#: Every separator shape the real ledger carries: none, a rule with no blank
#: line, a doubled rule, a comment, and a section that is not a finding.
_SEPARATORS = ("\n---\n\n", "\n", "\n---\n", "\n---\n\n---\n\n", "\n<!-- x -->\n\n---\n\n")


def _long_ledger(count: int = 30) -> str:
    text = "# Residual findings\n\nThe preamble.\n"
    for n in range(1, count + 1):
        text += _SEPARATORS[n % len(_SEPARATORS)] + f"## R-{n}. Finding {n}\n\n"
        text += "".join(f"Line {k} of {n}.  \n" for k in range(n % 4 + 1))
        if n % 7 == 0:
            text += "\n## Note. Not a finding, attached to the one before\n\nProse.\n"
    return text


def _layout(root: Path) -> dict[str, str]:
    docs = root / "docs"
    return {p.relative_to(docs).as_posix(): p.read_text() for p in sorted(docs.rglob("*.md"))}


def test_the_archive_moves_every_entry_byte_for_byte_and_a_rerun_changes_nothing(
    tmp_path, monkeypatch, board
):
    monkeypatch.setattr(board, "LEDGER_LIMIT", 40)
    ledger = tmp_path / "docs" / "residual-findings.md"
    ledger.parent.mkdir()
    ledger.write_text(_long_ledger())
    written = board.archive_ledger(ledger)
    assert len(written) > 2
    files = board.ledger_files(ledger)
    assert files[:-1] == written and files[-1] == ledger
    moved = [entry for path in files for entry in board.ledger_entries(path.read_text())]
    assert moved == board.ledger_entries(_long_ledger())
    assert [n for n, _ in moved] == list(range(1, 31))
    for path in files:
        text = path.read_text()
        assert text.count("\n") <= 40 and text.endswith("\n") and not text.endswith("\n\n")
    assert written[0].read_text().startswith(
        f"# Residual findings, R-1 to R-{moved[len(board.ledger_entries(written[0].read_text())) - 1][0]}"
        "\n\nArchived from "
    )
    assert ledger.read_text().startswith("# Residual findings\n\nThe preamble.\n\nThe older ")
    assert board.ledger_problems(ledger) == []
    before = _layout(tmp_path)
    assert board.archive_ledger(ledger) == []
    assert _layout(tmp_path) == before
    # From scratch again, as a merge that takes the single file ledger does.
    for path in written:
        path.unlink()
    ledger.write_text(_long_ledger())
    assert board.archive_ledger(ledger) == written
    assert _layout(tmp_path) == before


def test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over(
    tmp_path, monkeypatch, board
):
    ledger, folder = _folder(tmp_path, **{"u9-a": _residual("Lands past the archive")})
    archive = ledger.parent / "ledger" / "R-0013-R-0040.md"
    archive.parent.mkdir()
    archive.write_text("# Archived\n\n---\n\n## R-13. Held\n\nBody.\n\n---\n\n## R-40. Top\n\nB.\n")
    assert board.land_residuals(ledger, folder) == [(41, "Lands past the archive", False)]
    (folder / "u9-b.md").write_text(_residual("Top"))
    with pytest.raises(ValueError, match="R-40 already"):
        board.land_residuals(ledger, folder)
    (folder / "u9-b.md").write_text(_residual("Over the limit"))
    monkeypatch.setattr(board, "LEDGER_LIMIT", 20)
    assert board.land_residuals(ledger, folder) == [(42, "Over the limit", False)]
    assert [p.name for p in board.ledger_files(ledger)] == [
        "R-0005-R-0012.md", "R-0013-R-0040.md", "R-0041-R-0041.md", "ledger.md"
    ]
    assert list(board.residual_titles(ledger)) == [5, 12, 13, 40, 41, 42]
    assert "## R-42. Over the limit" in ledger.read_text()


def _check(board, monkeypatch, ledger, against=None, unchanged=False) -> int:
    monkeypatch.setattr(board, "LEDGER", ledger)
    return board.cmd_residuals(SimpleNamespace(check=True, against=against, unchanged=unchanged))


def test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one(
    tmp_path, monkeypatch, capsys, board
):
    monkeypatch.setattr(board, "LEDGER_LIMIT", 40)
    ledger = tmp_path / "docs" / "residual-findings.md"
    ledger.parent.mkdir()
    ledger.write_text(_long_ledger())
    first, second = board.archive_ledger(ledger)[:2]
    assert _check(board, monkeypatch, ledger) == 0
    entry = "\n## R-3. Finding 3\n\nCopied.\n"
    second.write_text(second.read_text() + entry)
    assert _check(board, monkeypatch, ledger) == 1
    out = capsys.readouterr().out
    assert f"R-3 is a heading in docs/ledger/{first.name} and in docs/ledger/{second.name}" in out
    assert "out of number order" in out and "not named by what it holds" in out
    second.write_text(second.read_text().replace(entry, ""))
    assert _check(board, monkeypatch, ledger) == 0
    renamed = first.with_name("R-0001-R-0099.md")
    first.rename(renamed)
    assert _check(board, monkeypatch, ledger) == 1
    assert f"{renamed.name} is not named by what it holds, R-1 to" in capsys.readouterr().out


def test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry(
    tmp_path, monkeypatch, capsys, board
):
    root = tmp_path / "repo"
    run = _seed(root)
    ledger = root / "docs" / "residual-findings.md"
    ledger.write_text(_long_ledger())
    _commit(run, "the single file")
    monkeypatch.setattr(board, "LEDGER_LIMIT", 40)
    board.archive_ledger(ledger)
    assert _check(board, monkeypatch, ledger, "HEAD", unchanged=True) == 0
    _commit(run, "the move")
    assert _check(board, monkeypatch, ledger, "HEAD~1", unchanged=True) == 0
    archive = board.ledger_files(ledger)[0]
    archive.write_text(archive.read_text().replace("Line 0 of 2.", "Line 0 of two."))
    assert _check(board, monkeypatch, ledger, "HEAD") == 0
    assert _check(board, monkeypatch, ledger, "HEAD", unchanged=True) == 1
    assert "entries that differ from HEAD: R-2" in capsys.readouterr().out
    archive.write_text(archive.read_text().replace("## R-4. Finding 4", "R-4 retired"))
    assert _check(board, monkeypatch, ledger, "HEAD") == 1
    assert "headings at HEAD are gone now: R-4" in capsys.readouterr().out
    assert _check(board, monkeypatch, ledger, None, unchanged=True) == 2


def _restart_text() -> str:
    return (REPO_ROOT / "RESTART-cratekit.md").read_text()


def test_the_restart_state_as_shipped_passes_its_own_scan_and_no_other_file_is_judged(tmp_path):
    scan = _load("scan_repo")
    assert scan.restart_violations("RESTART-cratekit.md", _restart_text()) == []
    path = tmp_path / "docs" / "restart" / "u999.md"
    path.parent.mkdir(parents=True)
    path.write_text("**U999 built, 2026-10-10, on `relay/999`.** A record.\n")
    assert scan.scan_tree(tmp_path, [path], check_identity=False) == []


def _insert(anchor: str, text: str, before: bool = False):
    return lambda t: t.replace(anchor, text + anchor if before else anchor + text, 1)


@pytest.mark.parametrize(
    ("edit", "says"),
    [
        (_insert("## Main, verify", "**U999 built, 2026-10-10, on `relay/999`.** A record.\n\n",
                 before=True), "head"),
        (_insert("## Main, verify", "A plain paragraph somebody added.\n\n", before=True), "head"),
        (lambda t: t + "\n## What U999 left behind\n\nThree residuals.\n", "U999"),
        (_insert("## What is open\n", "\n**R-999 built, 2026-10-10.** A record.\n"),
         "opens a unit's record"),
        (_insert("## What is open\n", "\n**Sitting 99, 2026-10-10, attended.** A record.\n"),
         "opens a unit's record"),
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


class Rewording(NamedTuple):
    unit: str
    fragment: str
    old: str
    new: str


#: The deliberate rewordings of moved text since the split, applied before the
#: byte for byte comparison and checked first, so a stale entry fails.
REWORDINGS = (
    # U195 (#469) stopped the public prose naming the service beside the
    # vendored downloader; restoring the old sentence would undo that unit.
    Rewording(
        unit="U195",
        fragment="r301.md",
        old="the vendored Tidal\nclient, neither",
        new="the vendored\ndownloader, neither",
    ),
)


def _paragraphs(text: str) -> list[str]:
    return [p for p in text.split("\n\n") if p.strip()]


@functools.cache
def _moved_paragraphs() -> tuple[str, ...]:
    """The paragraphs the split moved out of the restart state, as the base had them."""
    shown = subprocess.run(
        ["git", "show", f"{SPLIT_BASE}:RESTART-cratekit.md"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    assert shown.returncode == 0, f"the split base {SPLIT_BASE} is not in this clone"
    sections = re.split(r"\n(?=## )", shown.stdout)
    # The head kept its title and its first paragraph; the rest was records.
    moved = _paragraphs(sections[0])[2:]
    for section in sections[1:]:
        heading = section.split("\n", 1)[0]
        if heading == "## Main, verify before trusting it":
            # The heading and the command block stayed.
            moved += _paragraphs(section)[2:]
        elif heading not in _load("scan_repo").RESTART_SECTIONS:
            moved += _paragraphs(section)
    return tuple(moved)


def _fragments() -> dict[str, str]:
    return {p.name: p.read_text() for p in sorted((REPO_ROOT / "docs" / "restart").glob("*.md"))}


def _lost(fragments: dict[str, str], rewordings=REWORDINGS, check: bool = True) -> list[str]:
    """Stale table entries, else the opening of every moved paragraph no fragment holds."""
    moved = _moved_paragraphs()
    stale = []
    for entry in rewordings:
        found = sum(p.count(entry.old) for p in moved)
        if found != 1:
            stale.append(f"{entry.unit}: its old text is in the split base {found} times, not once")
        if entry.new not in fragments.get(entry.fragment, ""):
            stale.append(f"{entry.unit}: its new text is not in {entry.fragment}")
    if stale and check:
        return stale
    expected = list(moved)
    for entry in rewordings:
        expected = [p.replace(entry.old, entry.new) for p in expected]
    joined = "\n\n".join(fragments.values())
    return [p[:80] for p in expected if p not in joined]


def test_every_moved_paragraph_is_in_a_fragment_byte_for_byte():
    """The split moved whole records and changed none, but for the named rewordings."""
    assert len(_moved_paragraphs()) > 250
    assert _lost(_fragments()) == []


@pytest.mark.parametrize(
    "change",
    [
        ("tagging searchers", "tag searchers"),  # outside the reworded span
        ("downloader, neither", "downloader, nor"),  # inside it
        ("literal\nprovider hosts", "literal\nprovider names"),  # just before it
        "first", "middle", "last",  # a paragraph removed from another fragment
    ],
)
def test_a_changed_or_removed_paragraph_still_fails(change):
    fragments = _fragments()
    if isinstance(change, tuple):
        assert fragments["r301.md"].count(change[0]) == 1
        fragments["r301.md"] = fragments["r301.md"].replace(*change)
        opening = "**The session before: R-301, issue #168"
    else:
        joined = "\n\n".join(fragments.values())
        # Paragraphs held by exactly one fragment other than R-301's.
        held_once = [
            (name, p) for p in _moved_paragraphs() if joined.count(p) == 1
            for name, text in fragments.items() if name != "r301.md" and p in text
        ]
        assert len(held_once) > 200
        name, paragraph = held_once[{"first": 0, "middle": len(held_once) // 2, "last": -1}[change]]
        fragments[name] = fragments[name].replace(paragraph, "")
        opening = paragraph[:80]
    assert [p for p in _lost(fragments, check=False) if p.startswith(opening)]


@pytest.mark.parametrize(
    "entry, says",
    [
        (REWORDINGS[0]._replace(old="the vendored Tidal\nservice, neither"),
         "in the split base 0 times"),
        (REWORDINGS[0]._replace(old="\n"), "times, not once"),
        (REWORDINGS[0]._replace(new="the vendored\nfetcher, neither"),
         "its new text is not in r301.md"),
        (REWORDINGS[0]._replace(fragment="r999.md"), "its new text is not in r999.md"),
    ],
)
def test_a_stale_rewording_fails_rather_than_excusing_nothing(entry, says):
    # Added beside the real entry, so the only thing wrong is the stale one.
    problems = _lost(_fragments(), REWORDINGS + (entry._replace(unit="U0"),))
    assert len(problems) == 1
    assert says in problems[0]
