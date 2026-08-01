"""Lint the shipped operator skills against the CLI they drive (R7).

The skills are an OPTIONAL layer: every workflow runs from the CLI without them.
That makes them the layer most likely to rot, because nothing breaks when they
do. A skill that names a command the CLI no longer exposes does not fail a build,
it just produces a confidently wrong instruction the next time somebody follows
it. The source system watched exactly that happen through a seven-stage refactor,
and turned the drift into a build failure. This is that check, ported and
widened.

The rules:

  (a) every skill has frontmatter with a name and a description, and the name
      matches its directory;
  (b) every project command token used in a fenced COMMAND line resolves to a
      real console script; fenced COMMENT lines may also name skills and retired
      aliases, because history notes are useful and are not instructions;
  (c) every ``python -m cratekit.<module>`` target exists AND is on the
      deliberate no-script allowlist, which is empty by design: R2 says one entry
      point, so nothing should be reached by module path;
  (d) **no shipped skill carries a personal literal at all** (widened, see below);
  (e) no year literal inside a fenced command, because a hardcoded year rots
      silently at the rollover and produces a path that simply does not exist;
  (f) every deep reference to a repository file actually resolves.

RULE (d) IS WIDER THAN THE ONE IT REPLACES, and this is the substantive change.
The source rule matched one exact volume path and exempted two skills that were
allowed to say it. Two live violations sit in that gap right now:

* one shipped skill instructs the reader to work in the author's HOME directory,
  which the volume-only rule never looked for;
* another names the author's volume by BARE NAME with no path prefix, which the
  full-path match could not see.

Here rule (d) delegates to the portability scanner, so the skills and the package
share one literal set and one definition of what personal means. There is no
sanctioned home for a personal literal in a shipped skill. R7 says the skills
contain no personal context, with no carve-out, and a carve-out is how the two
violations above became invisible.

The checker is a pure function over a skills root, so the fixture tests prove
each rule bites against synthetic trees. The final test runs it over the real
tree, which lands in U28.
"""

from __future__ import annotations

import importlib.util
import re
import tomllib
from pathlib import Path

from tests._pending import requires

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
SRC_ROOT = REPO_ROOT / "src"


def _load_scanner():
    spec = importlib.util.spec_from_file_location(
        "cratekit_scan_repo_for_skills", REPO_ROOT / "scripts" / "scan_repo.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan = _load_scanner()

# Modules deliberately reached by module path rather than a console script.
# EMPTY BY DESIGN. R2 gives the product one entry point, so a skill that reaches
# past it is naming an implementation detail that the next refactor will move.
# An entry here is a decision, and it needs a comment saying who made it.
NO_SCRIPT_ALLOWLIST: frozenset[str] = frozenset()

# Skill names retired by a consolidation live on as invocation aliases and as
# "formerly ..." history notes in PROSE and in fenced COMMENTS. A non-comment
# fenced COMMAND may only use a real console script.
RETIRED_SKILL_NAMES: frozenset[str] = frozenset()

_FENCED = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
# The project's own command tokens. Anything starting with the product name is a
# command this repository is responsible for; a general "first token on the line"
# rule would flag `cd`, `mkdir`, and every other shell builtin.
_COMMAND_TOKEN = re.compile(r"(?<![\w/-])(crate(?:-[a-z0-9-]+)?)\b")
_PY_MODULE = re.compile(r"python3? -m (cratekit\.[\w.]+)")
_YEAR = re.compile(r"/20\d\d(?=[/\s\"']|$)")
_DEEP_REF = re.compile(r"`?(src/cratekit/[\w/]+/[A-Za-z0-9_.-]+\.md)`?")


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
) -> list[str]:
    """Return a list of ``"<skill>: <problem>"`` over every SKILL.md found.

    ``scripts`` is the ``[project.scripts]`` key set. ``skill_names`` defaults to
    the directory names under ``skills_root``. The roots are injectable so the
    fixture tests can drive the checker against synthetic trees rather than
    against the repository, which is what lets every rule be proved to bite.
    """
    problems: list[str] = []
    src_root = src_root if src_root is not None else SRC_ROOT
    repo_root = repo_root if repo_root is not None else REPO_ROOT

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

        # Split fenced blocks into COMMAND text and COMMENT text. A whole-line
        # comment, or the trailing " # ..." tail of a command line, is
        # commentary; everything before the marker is command.
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
        command_text = "\n".join(command_parts)
        comment_text = "\n".join(comment_parts)

        # (b) command tokens must resolve
        for token in sorted(set(_COMMAND_TOKEN.findall(command_text))):
            if token in scripts:
                continue
            problems.append(
                f"{directory.name}: fenced command references unknown script '{token}'"
            )
        for token in sorted(set(_COMMAND_TOKEN.findall(comment_text))):
            if token in names or token in scripts or token in RETIRED_SKILL_NAMES:
                continue
            problems.append(
                f"{directory.name}: fenced comment references unknown name '{token}'"
            )

        # (c) module-path invocations
        for module in sorted(set(_PY_MODULE.findall(fenced))):
            if not _module_exists(module, src_root):
                problems.append(
                    f"{directory.name}: python -m targets missing module '{module}'"
                )
            elif module not in NO_SCRIPT_ALLOWLIST:
                problems.append(
                    f"{directory.name}: '{module}' invoked via python -m but is not on "
                    f"the no-script allowlist (use the console script)"
                )

        # (d) WIDENED: no personal literal at all, no sanctioned exceptions.
        # Delegated to the portability scanner so there is one literal set.
        for violation in scan.portability_violations(
            text, identity_tokens=scan.machine_identity_tokens()
        ):
            problems.append(
                f"{directory.name}: personal literal in a shipped skill: {violation}"
            )

        # (e) year-literal PATH SEGMENTS in fenced commands
        if _YEAR.search(fenced):
            problems.append(
                f"{directory.name}: year-literal path segment in a fenced command "
                f"(use a {{year}} placeholder)"
            )

        # (f) deep references must resolve
        for reference in sorted(set(_DEEP_REF.findall(text))):
            if not (repo_root / reference).exists():
                problems.append(
                    f"{directory.name}: deep reference does not exist: {reference}"
                )

    return problems


def _real_scripts() -> set[str]:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    return set(data["project"]["scripts"])


# ═══════════════════════════════════════════════════════════════════════════
# Fixture tests: each rule bites
# ═══════════════════════════════════════════════════════════════════════════


def _mk_skill(root: Path, name: str, body: str, frontmatter: str | None = None) -> None:
    directory = root / name
    directory.mkdir(parents=True)
    header = (
        frontmatter
        if frontmatter is not None
        else f"---\nname: {name}\ndescription: x\n---\n"
    )
    (directory / "SKILL.md").write_text(header + body)


def test_unknown_script_token_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate-nonexistent --run\n```\n")
    problems = lint_skills(tmp_path, {"crate"})
    assert any("unknown script 'crate-nonexistent'" in p for p in problems)


def test_known_script_and_skill_names_pass(tmp_path):
    _mk_skill(tmp_path, "crate-x", "See crate-x and run:\n```bash\ncrate sync --ok\n```\n")
    assert lint_skills(tmp_path, {"crate"}) == []


def test_missing_module_target_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "```bash\npython -m cratekit.nope.gone\n```\n")
    problems = lint_skills(tmp_path, set())
    assert any("missing module 'cratekit.nope.gone'" in p for p in problems)


def test_module_path_invocation_fails_even_when_the_module_exists(tmp_path, monkeypatch):
    """R2: one entry point. Reaching past it names an implementation detail.

    A skill that says ``python -m cratekit.something`` is coupled to the module
    layout, so the next refactor breaks the instruction without breaking a test,
    unless this rule exists.
    """
    src = tmp_path / "src"
    (src / "cratekit" / "intake").mkdir(parents=True)
    (src / "cratekit" / "intake" / "__init__.py").write_text("")
    skills = tmp_path / "skills"
    _mk_skill(skills, "crate-x", "```bash\npython -m cratekit.intake\n```\n")
    problems = lint_skills(skills, set(), src_root=src)
    assert any("not on the no-script allowlist" in p for p in problems)


# ── rule (d): the widened personal-literal rule ──────────────────────────────

# Assembled at runtime. See tests/test_portability.py for why: a test for a
# literal guard must not contain the literal, or the guard flags its own tests
# and somebody adds an exemption, which is the hole being closed.
_A_HOME_LITERAL = "/" + "Users" + "/" + "jdoe" + "/Documents/Cratekit/"
_A_VOLUME_LITERAL = "/" + "Volumes" + "/" + "BigAudioDrive"


def test_a_volume_literal_in_any_skill_fails(tmp_path):
    """The widening. No skill has a sanctioned home for this any more.

    The source rule exempted two skills by name. An exemption for a rule about
    personal content is a place personal content accumulates.
    """
    _mk_skill(tmp_path, "crate-x", f"the volume is {_A_VOLUME_LITERAL} today\n")
    _mk_skill(tmp_path, "crate-backup", f"mirror {_A_VOLUME_LITERAL} nightly\n")
    problems = lint_skills(tmp_path, set())
    assert any(p.startswith("crate-x: personal literal") for p in problems)
    assert any(p.startswith("crate-backup: personal literal") for p in problems), (
        "no skill is exempt; the source rule's two carve-outs are exactly where "
        "its live violations went unnoticed"
    )


def test_a_home_directory_literal_in_a_skill_fails(tmp_path):
    """The first of the two live violations in the source system.

    A shipped skill told the reader to work in the author's home directory. The
    volume-only rule never looked for a home directory at all.
    """
    _mk_skill(tmp_path, "crate-x", f"while working in {_A_HOME_LITERAL}.\n")
    problems = lint_skills(tmp_path, set())
    assert any("hardcoded home directory" in p for p in problems)


def test_a_bare_volume_name_in_a_skill_fails(tmp_path):
    """The second live violation: a volume named with no path prefix.

    "The X volume must be mounted" carries no leading path, so a full-path match
    cannot see it. The runtime-derived identity tier is what catches this, which
    is why rule (d) calls the scanner rather than keeping its own copy of a
    literal set.
    """
    _mk_skill(tmp_path, "crate-x", "The SomeSpecificDrive volume must be mounted.\n")
    problems = lint_skills(tmp_path, set())
    # Driven through the scanner directly, since the token depends on the machine.
    assert scan.portability_violations(
        "The SomeSpecificDrive volume must be mounted.",
        identity_tokens={"SomeSpecificDrive"},
    )
    # And the lint reports nothing else about this otherwise-valid skill.
    assert [p for p in problems if "personal literal" not in p] == []


def test_placeholder_paths_in_a_skill_pass(tmp_path):
    """A skill must still be able to show the SHAPE of a path."""
    _mk_skill(
        tmp_path,
        "crate-x",
        "Point the library root at /Volumes/<your-library>/Music.\n",
    )
    assert lint_skills(tmp_path, set()) == []


# ── remaining rules ──────────────────────────────────────────────────────────


def test_year_literal_in_fenced_block_fails_prose_passes(tmp_path):
    _mk_skill(
        tmp_path,
        "crate-x",
        "Written 2026-08-01.\n```bash\nmv f Processed_Tracks/2026/x/\n```\n",
    )
    assert any("year-literal path segment" in p for p in lint_skills(tmp_path, set()))
    _mk_skill(
        tmp_path / "b",
        "crate-y",
        'Written 2026-08-01.\n```bash\nmv f "Processed_Tracks/{year}/x/"\n```\n',
    )
    assert lint_skills(tmp_path / "b", set()) == []


def test_year_in_a_flag_value_is_not_flagged(tmp_path):
    """``--track-limit 2000`` is a count, not a year path."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate sync --track-limit 2000\n```\n")
    assert lint_skills(tmp_path, {"crate"}) == []


def test_missing_frontmatter_and_name_mismatch_fail(tmp_path):
    _mk_skill(tmp_path, "crate-x", "no frontmatter here\n", frontmatter="")
    _mk_skill(
        tmp_path, "crate-y", "body\n", frontmatter="---\nname: crate-z\ndescription: d\n---\n"
    )
    problems = lint_skills(tmp_path, set())
    assert any("no YAML frontmatter" in p for p in problems)
    assert any("crate-y: frontmatter name != directory" in p for p in problems)


def test_missing_description_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "body\n", frontmatter="---\nname: crate-x\n---\n")
    assert any("missing description" in p for p in lint_skills(tmp_path, set()))


def test_dead_deep_reference_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "Deep reference: `src/cratekit/nope/NOTES.md`\n")
    assert any("deep reference does not exist" in p for p in lint_skills(tmp_path, set()))


def test_extra_files_in_a_skill_directory_pass(tmp_path):
    _mk_skill(tmp_path, "crate-x", "```bash\n./helper.sh check\n```\n")
    (tmp_path / "crate-x" / "helper.sh").write_text("#!/bin/sh\n")
    assert lint_skills(tmp_path, set()) == []


def test_info_string_fence_is_not_a_blind_spot(tmp_path):
    """A fence with an info-string tail must still be linted.

    The source system's earlier ``[a-z]*`` fence regex silently skipped
    ```` ```bash title=x ````, which is a verified evasion: a skill could put
    anything it liked inside such a fence and no rule would look at it.
    """
    _mk_skill(
        tmp_path,
        "crate-x",
        "```bash title=x\ncrate-nonexistent --run\nmv f Processed_Tracks/2026/\n```\n",
    )
    problems = lint_skills(tmp_path, set())
    assert any("unknown script 'crate-nonexistent'" in p for p in problems)
    assert any("year-literal path segment" in p for p in problems)


def test_the_allowlist_is_empty_by_design():
    """R2 gives the product one entry point.

    Asserted rather than commented, so growing the allowlist is a deliberate act
    that shows up in a diff as a changed test.
    """
    assert NO_SCRIPT_ALLOWLIST == frozenset()


# ═══════════════════════════════════════════════════════════════════════════
# The real tree
# ═══════════════════════════════════════════════════════════════════════════


@requires("path:skills")
def test_real_skills_pass_lint():
    problems = lint_skills(SKILLS_ROOT, _real_scripts())
    assert not problems, "skill lint violations:\n" + "\n".join(sorted(problems))
