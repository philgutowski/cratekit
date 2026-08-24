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

import argparse
import importlib.util
import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: The shipped skills live INSIDE the package, not at the repository root, and
#: U28 moved this constant rather than the other way round. R7 says the skills
#: "ship with the package", and a directory beside the package is not shipped by
#: a wheel: ``[tool.setuptools.package-data]`` can only name paths under the
#: importable tree, so a repo-root ``skills/`` would be present in this checkout,
#: absent from every install, and the install verb would have nothing to copy on
#: the one machine that matters. ``cratekit.core.taxonomy`` already reads its
#: shipped templates through ``importlib.resources``, and this follows that
#: precedent rather than inventing a second answer to one question.
SKILLS_ROOT = SRC_ROOT / "cratekit" / "skills" / "assets"


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
# Inline code spans, which is where a taxonomy name would be spelled as a value
# in running prose rather than inside a fenced block.
_CODE_SPANS = re.compile(r"`([^`\n]+)`")


def verb_table() -> dict[tuple[str, ...], dict[str, bool]]:
    """Every verb path the CLI exposes, mapped to its flags and whether each takes a value.

    DERIVED BY WALKING THE REAL PARSER, never by reading the registry's own
    fields. The registry says which entries exist; only the assembled parser says
    what a person may actually type, because each verb's ``build`` adds its own
    arguments and the root adds the ones that ride on every invocation. A rule
    checked against the registry would pass a skill naming a flag no builder ever
    declared, which is precisely the drift this file exists to catch.
    """
    from cratekit.cli import build_parser  # noqa: PLC0415

    def walk(parser, prefix: tuple[str, ...]):
        # flag -> whether it consumes the token after it. Recorded because a
        # value-taking flag's ARGUMENT is not a subcommand, and a walker that did
        # not know the difference read the "json" in ``--output json`` as a verb
        # and reported a correct command as naming no real verb. Found by the
        # fixture below, not by reading this function.
        found = {
            prefix: {
                name: action.nargs != 0
                for action in parser._actions
                for name in action.option_strings
            }
        }
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, sub in action.choices.items():
                    found.update(walk(sub, prefix + (name,)))
        return found

    return walk(build_parser(), ())


def taxonomy_display_names() -> set[str]:
    """Every display name the shipped taxonomy declares.

    Derived from the template the product actually ships rather than listed here,
    so a taxonomy edit cannot leave this rule checking last month's names. R19 is
    the reason the rule exists at all: a display name is simultaneously code,
    config, a persisted key, XML bytes, and a folder in somebody's library, so a
    skill that spells one has hardcoded a choice the user is allowed to change.
    """
    from cratekit.core import taxonomy  # noqa: PLC0415

    declared = taxonomy.default_taxonomy()
    return (
        {declared.tree.display, declared.intake.display}
        | {bucket.display for bucket in declared.buckets}
        | {band.display for band in declared.energy.bands}
    )


def _verb_problems(
    line: str, skill: str, verbs: dict[tuple[str, ...], dict[str, bool]]
) -> list[str]:
    """Check one fenced command line that invokes the product's own entry point.

    Lines that do not start with the entry point are somebody else's command and
    are not this rule's business. A continuation line, which is how a long
    invocation is written, carries no verb of its own and is skipped rather than
    reported: the rule reads what a person would type as one command, and a
    trailing backslash means the command is not finished.

    THE VERB PATH IS CONSUMED GREEDILY WHILE IT STAYS A PREFIX of some real path,
    which is what lets a positional argument follow it without being mistaken for
    a further subcommand. ``crate restore run no-such-session`` walks to
    ``restore run`` and stops, because ``restore run no-such-session`` is not a
    prefix of anything.
    """
    tokens = line.split()
    if not tokens or tokens[0] != "crate":
        return []
    if line.rstrip().endswith("\\"):
        return []

    prefixes = {path[:n] for path in verbs for n in range(len(path) + 1)}
    known = dict(verbs.get((), {}))
    path: tuple[str, ...] = ()
    flags: list[str] = []
    rest = tokens[1:]
    index = 0
    while index < len(rest):
        token = rest[index]
        if token.startswith("-"):
            flag = token.split("=", 1)[0]
            flags.append(flag)
            # Skip the flag's ARGUMENT when it takes one and did not carry it
            # inline, or the value is read as a subcommand.
            takes_value = known.get(flag) or verbs.get(path, {}).get(flag)
            index += 2 if takes_value and "=" not in token else 1
            continue
        if path + (token,) in prefixes and path + (token,) != path:
            path += (token,)
            known.update(verbs.get(path, {}))
            index += 1
            continue
        break
    # Everything after the verb path is a value, except the flags among it.
    for token in rest[index:]:
        if token.startswith("-"):
            flags.append(token.split("=", 1)[0])

    if path not in verbs or not path:
        spelled = " ".join(path) if path else " ".join(rest[:2])
        return [f"{skill}: fenced command names no real verb: 'crate {spelled}'"]

    allowed = set(verbs[path]) | set(verbs[()])
    return [
        f"{skill}: 'crate {' '.join(path)}' does not declare the flag {flag!r}"
        for flag in sorted(set(flags))
        if flag not in allowed
    ]


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
    verbs: dict[tuple[str, ...], dict[str, bool]] | None = None,
    taxonomy_names: set[str] | None = None,
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
    verbs = verbs if verbs is not None else verb_table()
    taxonomy_names = (
        taxonomy_names if taxonomy_names is not None else taxonomy_display_names()
    )

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

        # (g) every crate invocation names a real verb path and real flags.
        for line in command_text.split("\n"):
            problems += _verb_problems(line, directory.name, verbs)

        # (h) no shipped skill hardcodes a taxonomy display name.
        #
        # SCOPED TO CODE, NOT TO PROSE, and the scoping is by CONTEXT rather than
        # by exempted file, which is the difference between this and the
        # carve-out rule (d) exists to refuse. The hazard R19 names is a name
        # BAKED IN as a value: a path segment, a flag argument, a folder a
        # command walks. Several display names are also ordinary English words,
        # so a rule over whole files would fire on a sentence about a high energy
        # track and get suppressed, and a suppressed rule protects nothing (P7).
        # Fenced blocks and inline code spans are where a value lives.
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


#: The verb table the FIXTURE skills are checked against. Synthetic on purpose,
#: exactly as the synthetic skills root is: a fixture proving that the year rule
#: ignores a flag value must not also have to satisfy the verb rule, or it stops
#: proving one thing and starts proving two, and the failure message stops naming
#: which. The real tree is checked against the real parser by the final test.
_FIXTURE_VERBS: dict[tuple[str, ...], dict[str, bool]] = {
    (): {"--output": True, "-h": False, "--help": False},
    ("sync",): {"--ok": False, "--track-limit": True},
}

#: No taxonomy at all for the fixtures, so rule (h) is inert against them and is
#: proved by its own fixtures below rather than as a side effect of every other.
_FIXTURE_TAXONOMY: set[str] = set()


def _lint(root: Path, scripts: set[str], **kwargs):
    """Lint a synthetic tree with the synthetic verb table and taxonomy."""
    kwargs.setdefault("verbs", _FIXTURE_VERBS)
    kwargs.setdefault("taxonomy_names", _FIXTURE_TAXONOMY)
    return lint_skills(root, scripts, **kwargs)


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
    problems = _lint(tmp_path, {"crate"})
    assert any("unknown script 'crate-nonexistent'" in p for p in problems)


def test_known_script_and_skill_names_pass(tmp_path):
    _mk_skill(tmp_path, "crate-x", "See crate-x and run:\n```bash\ncrate sync --ok\n```\n")
    assert _lint(tmp_path, {"crate"}) == []


def test_missing_module_target_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "```bash\npython -m cratekit.nope.gone\n```\n")
    problems = _lint(tmp_path, set())
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
    problems = _lint(skills, set(), src_root=src)
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
    problems = _lint(tmp_path, set())
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
    problems = _lint(tmp_path, set())
    assert any("hardcoded home directory" in p for p in problems)


def test_a_bare_volume_name_in_a_skill_fails(tmp_path):
    """The second live violation: a volume named with no path prefix.

    "The X volume must be mounted" carries no leading path, so a full-path match
    cannot see it. The runtime-derived identity tier is what catches this, which
    is why rule (d) calls the scanner rather than keeping its own copy of a
    literal set.
    """
    _mk_skill(tmp_path, "crate-x", "The SomeSpecificDrive volume must be mounted.\n")
    problems = _lint(tmp_path, set())
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
    assert _lint(tmp_path, set()) == []


# ── remaining rules ──────────────────────────────────────────────────────────


def test_year_literal_in_fenced_block_fails_prose_passes(tmp_path):
    _mk_skill(
        tmp_path,
        "crate-x",
        "Written 2026-08-01.\n```bash\nmv f Processed_Tracks/2026/x/\n```\n",
    )
    assert any("year-literal path segment" in p for p in _lint(tmp_path, set()))
    _mk_skill(
        tmp_path / "b",
        "crate-y",
        'Written 2026-08-01.\n```bash\nmv f "Processed_Tracks/{year}/x/"\n```\n',
    )
    assert _lint(tmp_path / "b", set()) == []


def test_year_in_a_flag_value_is_not_flagged(tmp_path):
    """``--track-limit 2000`` is a count, not a year path."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate sync --track-limit 2000\n```\n")
    assert _lint(tmp_path, {"crate"}) == []


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


def test_dead_deep_reference_fails(tmp_path):
    _mk_skill(tmp_path, "crate-x", "Deep reference: `src/cratekit/nope/NOTES.md`\n")
    assert any("deep reference does not exist" in p for p in _lint(tmp_path, set()))


def test_extra_files_in_a_skill_directory_pass(tmp_path):
    _mk_skill(tmp_path, "crate-x", "```bash\n./helper.sh check\n```\n")
    (tmp_path / "crate-x" / "helper.sh").write_text("#!/bin/sh\n")
    assert _lint(tmp_path, set()) == []


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
    problems = _lint(tmp_path, set())
    assert any("unknown script 'crate-nonexistent'" in p for p in problems)
    assert any("year-literal path segment" in p for p in problems)


def test_the_allowlist_is_empty_by_design():
    """R2 gives the product one entry point.

    Asserted rather than commented, so growing the allowlist is a deliberate act
    that shows up in a diff as a changed test.
    """
    assert NO_SCRIPT_ALLOWLIST == frozenset()


def test_a_command_naming_no_real_verb_fails(tmp_path):
    """Rule (g). The script token resolves and the verb does not, which is the
    whole gap between this rule and (b): ``crate`` is a real console script, so
    (b) is satisfied by any nonsense typed after it."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate synchronise --ok\n```\n")
    problems = _lint(tmp_path, {"crate"})
    assert any("names no real verb" in p for p in problems), problems


def test_a_command_naming_a_flag_the_verb_does_not_declare_fails(tmp_path):
    """Rule (g), the half that catches the likelier rot. The verb still exists and
    the flag was renamed underneath the skill, which is the seven-stage-refactor
    failure this file was ported to catch."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate sync --no-such-flag\n```\n")
    problems = _lint(tmp_path, {"crate"})
    assert any("does not declare the flag '--no-such-flag'" in p for p in problems), problems


def test_a_real_verb_with_real_flags_and_a_positional_passes(tmp_path):
    """The other direction, so the two rules above are not passing on a checker
    that rejects everything. The positional must not be read as a subcommand."""
    _mk_skill(
        tmp_path, "crate-x", "```bash\ncrate sync --ok some-value\ncrate --output json sync\n```\n"
    )
    assert _lint(tmp_path, {"crate"}) == []


def test_a_continuation_line_is_not_read_as_a_verb(tmp_path):
    """A long invocation is written across lines, and the tail of one carries no
    verb. Reporting it would make the rule fire on correct prose, which is how a
    rule gets suppressed (P7)."""
    _mk_skill(
        tmp_path, "crate-x", "```bash\ncrate sync \\\n    --ok\n```\n"
    )
    assert _lint(tmp_path, {"crate"}) == []


def test_a_hardcoded_taxonomy_name_in_a_command_fails(tmp_path):
    """Rule (h). R19: a display name is a choice the user owns, so a skill that
    spells one has baked in somebody else's library."""
    _mk_skill(tmp_path, "crate-x", "```bash\ncrate sync --ok 'BY GENRE + ENERGY/Deep House'\n```\n")
    problems = _lint(
        tmp_path, {"crate"}, taxonomy_names={"BY GENRE + ENERGY", "Deep House"}
    )
    assert sum("hardcoded taxonomy name" in p for p in problems) == 2, problems


def test_a_hardcoded_taxonomy_name_in_an_inline_code_span_fails(tmp_path):
    """The same value spelled in running prose as code rather than in a fence.
    Both are the name used as a VALUE, which is what the rule is about."""
    _mk_skill(tmp_path, "crate-x", "Put it under `Deep House` when you are done.\n")
    problems = _lint(tmp_path, {"crate"}, taxonomy_names={"Deep House"})
    assert any("hardcoded taxonomy name" in p for p in problems), problems


def test_a_taxonomy_word_in_ordinary_prose_passes(tmp_path):
    """The scoping decision, asserted rather than commented. Several display names
    are ordinary English, and a rule that fired on a sentence would be suppressed
    and would then protect nothing."""
    _mk_skill(tmp_path, "crate-x", "Deep House sets tend to run long, so plan for it.\n")
    assert _lint(tmp_path, {"crate"}, taxonomy_names={"Deep House"}) == []


# ═══════════════════════════════════════════════════════════════════════════
# The real tree
# ═══════════════════════════════════════════════════════════════════════════


def test_real_skills_pass_lint():
    problems = lint_skills(SKILLS_ROOT, _real_scripts())
    assert not problems, "skill lint violations:\n" + "\n".join(sorted(problems))
