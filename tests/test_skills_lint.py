"""Lint the shipped operator skills against the CLI they drive (R7).

A skill naming a command the CLI no longer exposes is a confidently wrong
instruction. Rules: (a) frontmatter names the directory and a description;
(b) every command token in a fenced command line is a real console script;
(c) every ``python -m cratekit.<module>`` target exists and is allowlisted (the
list is empty, R2); (d) no personal literal, by the portability scanner; (e) no
year literal path segment; (f) every repository reference resolves; (g) every
crate invocation parses with the real parser; (h) no taxonomy display name as a
value in code. Fixtures prove each rule bites; the last test lints the real tree.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import re
import shlex
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: The shipped skills live INSIDE the package, since a wheel ships nothing
#: beside it.
SKILLS_ROOT = SRC_ROOT / "cratekit" / "skills" / "assets"


def _load_scanner():
    spec = importlib.util.spec_from_file_location(
        "cratekit_scan_repo_for_skills", REPO_ROOT / "scripts" / "scan_repo.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan = _load_scanner()

# Modules deliberately reached by module path. EMPTY BY DESIGN (R2); an entry
# is a decision and needs a comment saying who made it.
NO_SCRIPT_ALLOWLIST: frozenset[str] = frozenset()

# Retired skill names may live on in fenced COMMENTS, never in a COMMAND.
RETIRED_SKILL_NAMES: frozenset[str] = frozenset()

_FENCED = re.compile(r"(?:```|~~~)[^\n]*\n(.*?)(?:```|~~~)", re.DOTALL)
# An INDENTED command line, the house style no fence matcher sees, narrowed to
# lines invoking the product so list continuations are left alone (P7).
_INDENTED_COMMAND = re.compile(r"^[ \t]{4,}(crate(?:\s+\S.*)?)$", re.M)
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
# The project's own command tokens, so shell builtins are never flagged.
_COMMAND_TOKEN = re.compile(r"(?<![\w/-])(crate(?:-[a-z0-9-]+)?)\b")
_PY_MODULE = re.compile(r"python3? -m (cratekit\.[\w.]+)")
_YEAR = re.compile(r"/20\d\d(?=[/\s\"']|$)")
_DEEP_REF = re.compile(r"`?(src/cratekit/[\w/]+/[A-Za-z0-9_.-]+\.md)`?")
# Inline code spans, where a taxonomy name would be spelled as a value in prose.
_CODE_SPANS = re.compile(r"`([^`\n]+)`")


def real_parser():
    """The installed CLI's parser over every module, fresh, since a failed parse leaves state."""
    from cratekit.cli import build_parser  # noqa: PLC0415

    return build_parser()


class _ParserUntilRejected:
    """The real parser, reused across lines and rebuilt after any line it exits on."""

    def __init__(self):
        self._parser = None

    def __call__(self):
        if self._parser is None:
            self._parser = real_parser()
        return self._parser

    def rejected(self):
        self._parser = None


def _rejected(parser_for) -> None:
    getattr(parser_for, "rejected", lambda: None)()


def taxonomy_display_names() -> set[str]:
    """Every display name the shipped taxonomy declares (R19), derived from the template."""
    from cratekit.core import taxonomy  # noqa: PLC0415

    declared = taxonomy.default_taxonomy()
    return (
        {declared.tree.display, declared.intake.display}
        | {bucket.display for bucket in declared.buckets}
        | {band.display for band in declared.energy.bands}
    )


def _verb_problems(line: str, skill: str, parser_for) -> list[str]:
    """Check one command line by parsing it with the real parser, whose exit 2 is the verdict.

    Not checked (P7): a continuation line, text after a pipe or redirection, bad quoting.
    """
    text = line.strip()
    # A prompt marker is decoration, and a person copying the line drops it.
    for marker in ("$ ", "% "):
        if text.startswith(marker):
            text = text[len(marker) :]
    if not text.startswith("crate ") and text != "crate":
        return []
    if text.endswith("\\"):
        return []
    # Everything from a shell operator onwards belongs to another program.
    for operator in ("|", ">", "<", "&&", ";"):
        if operator in text:
            text = text.split(operator, 1)[0].strip()
    try:
        argv = shlex.split(text)[1:]
    except ValueError:
        return []
    if not argv:
        return []

    parser = parser_for()
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stderr(buffer), contextlib.redirect_stdout(buffer):
            parser.parse_args(argv)
    except SystemExit as exit_code:
        _rejected(parser_for)
        # 0 is --help and --version, which are real answers rather than failures.
        if exit_code.code in (0, None):
            return []
        complaint = buffer.getvalue().strip().splitlines()
        detail = complaint[-1] if complaint else "rejected by the parser"
        return [f"{skill}: fenced command does not parse: {text!r}: {detail}"]
    except Exception as exc:  # pragma: no cover - a parser defect, not a skill's
        _rejected(parser_for)
        return [f"{skill}: fenced command raised {type(exc).__name__}: {text!r}"]
    return []


def _module_exists(dotted: str, src_root: Path) -> bool:
    relative = Path(*dotted.split("."))
    return (src_root / relative).with_suffix(".py").exists() or (
        src_root / relative / "__init__.py"
    ).exists()


def lint_skills(
    skills_root: Path,
    scripts: set[str],
    *,
    skill_names: set[str] | None = None,
    src_root: Path | None = None,
    repo_root: Path | None = None,
    parser_for=None,
    taxonomy_names: set[str] | None = None,
) -> list[str]:
    """``"<skill>: <problem>"`` over every SKILL.md; the roots are injectable for fixtures."""
    problems: list[str] = []
    src_root = src_root if src_root is not None else SRC_ROOT
    repo_root = repo_root if repo_root is not None else REPO_ROOT
    parser_for = parser_for if parser_for is not None else real_parser
    taxonomy_names = taxonomy_names if taxonomy_names is not None else taxonomy_display_names()

    dirs = sorted(d for d in skills_root.glob("*") if d.is_dir())
    names = skill_names if skill_names is not None else {d.name for d in dirs}

    for directory in dirs:
        skill = directory / "SKILL.md"
        if not skill.exists():
            problems.append(f"{directory.name}: missing SKILL.md")
            continue
        text = skill.read_text()

        # (a) frontmatter
        frontmatter = _FRONTMATTER.match(text)
        if not frontmatter:
            problems.append(f"{directory.name}: no YAML frontmatter")
        else:
            body = frontmatter.group(1)
            match = re.search(r"^name:\s*(\S+)", body, re.M)
            if not match or match.group(1) != directory.name:
                problems.append(f"{directory.name}: frontmatter name != directory")
            if not re.search(r"^description:", body, re.M):
                problems.append(f"{directory.name}: frontmatter missing description")

        # Split fenced blocks into COMMAND and COMMENT text: a whole line comment
        # or a trailing " # ..." tail is commentary.
        fenced = "\n".join(_FENCED.findall(text))
        command_parts: list[str] = []
        comment_parts: list[str] = []
        for line in fenced.split("\n"):
            if line.lstrip().startswith("#"):
                comment_parts.append(line)
            elif " #" in line:
                command, _, tail = line.partition(" #")
                command_parts.append(command)
                comment_parts.append(tail)
            else:
                command_parts.append(line)
        # Indented invocations join the command text, so rule (g) sees them too.
        command_parts += _INDENTED_COMMAND.findall(text)
        command_text = "\n".join(command_parts)
        comment_text = "\n".join(comment_parts)

        # (b) command tokens must resolve
        for token in sorted(set(_COMMAND_TOKEN.findall(command_text))):
            if token in scripts:
                continue
            problems.append(f"{directory.name}: fenced command references unknown script '{token}'")
        for token in sorted(set(_COMMAND_TOKEN.findall(comment_text))):
            if token in names or token in scripts or token in RETIRED_SKILL_NAMES:
                continue
            problems.append(f"{directory.name}: fenced comment references unknown name '{token}'")

        # (c) module-path invocations
        for module in sorted(set(_PY_MODULE.findall(fenced))):
            if not _module_exists(module, src_root):
                problems.append(f"{directory.name}: python -m targets missing module '{module}'")
            elif module not in NO_SCRIPT_ALLOWLIST:
                problems.append(
                    f"{directory.name}: '{module}' invoked via python -m but is not on "
                    f"the no-script allowlist (use the console script)"
                )

        # (d) no personal literal at all, through the portability scanner.
        for violation in scan.portability_violations(
            text, identity_tokens=scan.machine_identity_tokens()
        ):
            problems.append(f"{directory.name}: personal literal in a shipped skill: {violation}")

        # (e) year-literal PATH SEGMENTS in fenced commands
        if _YEAR.search(fenced):
            problems.append(
                f"{directory.name}: year-literal path segment in a fenced command "
                f"(use a {{year}} placeholder)"
            )

        # (g) every crate invocation parses against the real parser.
        for line in command_text.split("\n"):
            problems += _verb_problems(line, directory.name, parser_for)

        # (h) no taxonomy display name in fenced blocks or inline code spans,
        # where a value lives; several names are ordinary English in prose (P7).
        for span in _CODE_SPANS.findall(text) + _FENCED.findall(text):
            for name in sorted(taxonomy_names):
                if name in span:
                    problems.append(
                        f"{directory.name}: hardcoded taxonomy name {name!r} in a "
                        f"command or path; read it from the configured taxonomy "
                        f"instead"
                    )

        # (f) deep references must resolve
        for reference in sorted(set(_DEEP_REF.findall(text))):
            if not (repo_root / reference).exists():
                problems.append(f"{directory.name}: deep reference does not exist: {reference}")

    return problems


def _real_scripts() -> set[str]:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    return set(data["project"]["scripts"])


# Fixture tests: each rule bites


def _fixture_parser():
    """A tiny real argparse parser, so each fixture takes the real tree's code path."""
    parser = argparse.ArgumentParser(prog="crate", add_help=True)
    parser.add_argument("--output")
    subparsers = parser.add_subparsers(dest="verb")
    sync = subparsers.add_parser("sync")
    sync.add_argument("--ok", action="store_true")
    sync.add_argument("--track-limit")
    sync.add_argument("value", nargs="*")
    return parser


#: No taxonomy for the fixtures, so rule (h) is proved only by its own fixtures.
_FIXTURE_TAXONOMY: set[str] = set()


def _lint(root: Path, scripts: set[str], **kwargs):
    """Lint a synthetic tree with the synthetic verb table and taxonomy."""
    kwargs.setdefault("parser_for", _fixture_parser)
    kwargs.setdefault("taxonomy_names", _FIXTURE_TAXONOMY)
    return lint_skills(root, scripts, **kwargs)


def _mk_skill(root: Path, name: str, body: str, frontmatter: str | None = None) -> None:
    directory = root / name
    directory.mkdir(parents=True)
    header = frontmatter if frontmatter is not None else f"---\nname: {name}\ndescription: x\n---\n"
    (directory / "SKILL.md").write_text(header + body)


# Rule (d). Assembled at runtime so this file does not trip the guard it tests.
_A_HOME_LITERAL = "/" + "Users" + "/" + "jdoe" + "/Documents/Cratekit/"
_A_VOLUME_LITERAL = "/" + "Volumes" + "/" + "BigAudioDrive"


@pytest.mark.parametrize(
    ("body", "scripts", "expected"),
    [
        (
            "```bash\ncrate-nonexistent --run\n```\n",
            {"crate"},
            "unknown script 'crate-nonexistent'",
        ),
        (
            "```bash\npython -m cratekit.nope.gone\n```\n",
            set(),
            "missing module 'cratekit.nope.gone'",
        ),
        ("Deep reference: `src/cratekit/nope/NOTES.md`\n", set(), "deep reference does not exist"),
        (f"while working in {_A_HOME_LITERAL}.\n", set(), "hardcoded home directory"),
        # Rule (g): a flag renamed underneath the skill.
        ("```bash\ncrate sync --no-such-flag\n```\n", {"crate"}, "--no-such-flag"),
    ],
    ids=["unknown script", "missing module", "dead deep reference", "home literal", "unknown flag"],
)
def test_a_rule_reports_what_it_finds(tmp_path, body, scripts, expected):
    _mk_skill(tmp_path, "crate-x", body)
    assert any(expected in p for p in _lint(tmp_path, scripts))


@pytest.mark.parametrize(
    ("body", "scripts"),
    [
        ("See crate-x and run:\n```bash\ncrate sync --ok\n```\n", {"crate"}),
        # A count, not a year path.
        ("```bash\ncrate sync --track-limit 2000\n```\n", {"crate"}),
        # A positional must not be read as a subcommand.
        ("```bash\ncrate sync --ok some-value\ncrate --output json sync\n```\n", {"crate"}),
        # A continuation line carries no verb of its own.
        ("```bash\ncrate sync \\\n    --ok\n```\n", {"crate"}),
        # A list continuation and indented prose are not commands.
        (
            "- a list item\n    that continues on the next line\n\n    plain indented prose\n",
            {"crate"},
        ),
        # A skill must still be able to show the SHAPE of a path.
        ("Point the library root at /Volumes/<your-library>/Music.\n", set()),
    ],
    ids=[
        "known script and skill names",
        "year in a flag value",
        "real verb, flags and positional",
        "continuation line",
        "indented non command",
        "placeholder path",
    ],
)
def test_a_correct_skill_lints_clean(tmp_path, body, scripts):
    _mk_skill(tmp_path, "crate-x", body)
    assert _lint(tmp_path, scripts) == []


def test_extra_files_in_a_skill_directory_pass(tmp_path):
    _mk_skill(tmp_path, "crate-x", "```bash\n./helper.sh check\n```\n")
    (tmp_path / "crate-x" / "helper.sh").write_text("#!/bin/sh\n")
    assert _lint(tmp_path, set()) == []


def test_module_path_invocation_fails_even_when_the_module_exists(tmp_path):
    """R2: reaching past the one entry point couples a skill to the module layout."""
    src = tmp_path / "src"
    (src / "cratekit" / "intake").mkdir(parents=True)
    (src / "cratekit" / "intake" / "__init__.py").write_text("")
    skills = tmp_path / "skills"
    _mk_skill(skills, "crate-x", "```bash\npython -m cratekit.intake\n```\n")
    problems = _lint(skills, set(), src_root=src)
    assert any("not on the no-script allowlist" in p for p in problems)


def test_a_volume_literal_in_any_skill_fails(tmp_path):
    """No skill has a sanctioned home for a personal literal."""
    _mk_skill(tmp_path, "crate-x", f"the volume is {_A_VOLUME_LITERAL} today\n")
    _mk_skill(tmp_path, "crate-backup", f"mirror {_A_VOLUME_LITERAL} nightly\n")
    problems = _lint(tmp_path, set())
    assert any(p.startswith("crate-x: personal literal") for p in problems)
    assert any(p.startswith("crate-backup: personal literal") for p in problems), "an exemption"


def test_a_bare_volume_name_in_a_skill_fails(tmp_path):
    """A volume named with no path prefix is caught by the scanner's identity tier."""
    _mk_skill(tmp_path, "crate-x", "The SomeSpecificDrive volume must be mounted.\n")
    problems = _lint(tmp_path, set())
    # Driven through the scanner directly, since the token depends on the machine.
    assert scan.portability_violations(
        "The SomeSpecificDrive volume must be mounted.",
        identity_tokens={"SomeSpecificDrive"},
    )
    # And the lint reports nothing else about this otherwise-valid skill.
    assert [p for p in problems if "personal literal" not in p] == []


def test_year_literal_in_fenced_block_fails_prose_passes(tmp_path):
    _mk_skill(tmp_path, "crate-x",
              "Written 2026-08-01.\n```bash\nmv f Processed_Tracks/2026/x/\n```\n")
    assert any("year-literal path segment" in p for p in _lint(tmp_path, set()))
    _mk_skill(tmp_path / "b", "crate-y",
              'Written 2026-08-01.\n```bash\nmv f "Processed_Tracks/{year}/x/"\n```\n')
    assert _lint(tmp_path / "b", set()) == []


def test_missing_frontmatter_and_name_mismatch_fail(tmp_path):
    _mk_skill(tmp_path, "crate-x", "no frontmatter here\n", frontmatter="")
    _mk_skill(
        tmp_path, "crate-y", "body\n", frontmatter="---\nname: crate-z\ndescription: d\n---\n"
    )
    problems = _lint(tmp_path, set())
    assert any("no YAML frontmatter" in p for p in problems)
    assert any("crate-y: frontmatter name != directory" in p for p in problems)


def test_missing_description_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "body\n", frontmatter="---\nname: crate-x\n---\n")
    assert any("missing description" in p for p in _lint(tmp_path, set()))


def test_info_string_fence_is_not_a_blind_spot(tmp_path):
    """A fence with an info string tail, ```` ```bash title=x ````, is still linted."""
    _mk_skill(tmp_path, "crate-x",
              "```bash title=x\ncrate-nonexistent --run\nmv f Processed_Tracks/2026/\n```\n")
    problems = _lint(tmp_path, set())
    assert any("unknown script 'crate-nonexistent'" in p for p in problems)
    assert any("year-literal path segment" in p for p in problems)


def test_the_allowlist_is_empty_by_design():
    """R2, asserted so growing the allowlist shows up as a changed test."""
    assert NO_SCRIPT_ALLOWLIST == frozenset()


def test_a_command_naming_no_real_verb_fails(tmp_path):
    """Rule (g): ``crate`` is a real script, so (b) passes any verb after it."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate synchronise --ok\n```\n")
    problems = _lint(tmp_path, {"crate"})
    assert any("does not parse" in p for p in problems), problems
    assert any("invalid choice" in p for p in problems), problems


@pytest.mark.parametrize(
    "body",
    [
        # A flag missing the value argparse wants.
        "```bash\ncrate sync --track-limit\n```\n",
        # The house style indented block.
        "Run this:\n\n    crate not-a-verb\n\nDone.\n",
        # A tilde fence is a fence.
        "~~~bash\ncrate not-a-verb\n~~~\n",
    ],
    ids=["missing required value", "indented block", "tilde fence"],
)
def test_a_command_that_does_not_parse_is_reported(tmp_path, body):
    _mk_skill(tmp_path, "crate-x", body)
    problems = _lint(tmp_path, {"crate"}, parser_for=_fixture_parser)
    assert any("does not parse" in p for p in problems), problems


def test_a_hardcoded_taxonomy_name_in_a_command_fails(tmp_path):
    """Rule (h): a display name is a choice the user owns (R19)."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate sync --ok 'BY GENRE + ENERGY/Deep House'\n```\n")
    problems = _lint(tmp_path, {"crate"}, taxonomy_names={"BY GENRE + ENERGY", "Deep House"})
    assert sum("hardcoded taxonomy name" in p for p in problems) == 2, problems


def test_a_hardcoded_taxonomy_name_in_an_inline_code_span_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "Put it under `Deep House` when you are done.\n")
    problems = _lint(tmp_path, {"crate"}, taxonomy_names={"Deep House"})
    assert any("hardcoded taxonomy name" in p for p in problems), problems


def test_a_taxonomy_word_in_ordinary_prose_passes(tmp_path):
    _mk_skill(tmp_path, "crate-x", "Deep House sets tend to run long, so plan for it.\n")
    assert _lint(tmp_path, {"crate"}, taxonomy_names={"Deep House"}) == []


def test_a_rejected_line_hands_the_next_line_a_fresh_parser(tmp_path):
    """The reuse the real tree's lint takes: one parser until a line exits it."""
    built = []

    class Counting(_ParserUntilRejected):
        def __call__(self):
            if self._parser is None:
                built.append(1)
                self._parser = _fixture_parser()
            return self._parser

    body = "```bash\ncrate sync --ok\ncrate sync --ok\ncrate nope\ncrate sync --ok\n```\n"
    _mk_skill(tmp_path, "crate-x", body)
    problems = _lint(tmp_path, {"crate"}, parser_for=Counting())
    assert len(built) == 2
    assert [p.split(": ")[2] for p in problems] == ["'crate nope'"], problems


def test_a_profile_disabled_verb_is_absent_rather_than_refusing():
    """A switched off module's verb is an invalid choice to argparse, not a refusal with a cause."""
    from cratekit.cli import build_parser  # noqa: PLC0415
    from cratekit.core import profiles  # noqa: PLC0415

    slim = build_parser(membership=profiles.resolve("slim"))
    full = build_parser(membership=profiles.resolve("full"))

    def names(parser):
        found = set()
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                found |= set(action.choices)
        return found

    hidden = names(full) - names(slim)
    assert hidden, "no verb differs between the presets, so this pins nothing"
    absent = sorted(hidden)[0]
    with pytest.raises(SystemExit) as exit_code:
        slim.parse_args([absent])
    assert exit_code.value.code == 2, f"{absent!r} refuses now, so the skills need rewriting"


# The real tree

#: What ships, written out because the count is a decision that belongs in a diff.
EXPECTED_SKILLS: frozenset[str] = frozenset({
    "adopt-a-library", "analyze-audio", "first-run", "intake-and-name", "label-catalogues",
    "library-reports", "library-status", "remove-tracks", "restore-and-converge", "review-queue",
    "route-the-library", "sync-and-publish",
})


def test_the_real_tree_holds_exactly_the_skills_that_are_meant_to_ship():
    """ANTI-VACUITY: a lint over an empty root is also an empty problem list."""
    found = {d.name for d in SKILLS_ROOT.iterdir() if d.is_dir()}
    assert found == EXPECTED_SKILLS, "the shipped skill set moved: update EXPECTED_SKILLS with it"


def test_real_skills_pass_lint():
    problems = lint_skills(SKILLS_ROOT, _real_scripts(), parser_for=_ParserUntilRejected())
    assert not problems, "skill lint violations:\n" + "\n".join(sorted(problems))
