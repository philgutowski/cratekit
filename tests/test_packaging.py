"""U1: the package declares an installable, portable, genuinely slim core.

These assertions run against ``pyproject.toml`` as data rather than against an
installed distribution, so they fail in the pull request that introduces the
regression instead of on the first friend's machine.

The end-to-end proof that a clean environment installs and imports lives in
CI's ``cold-install`` job and in the manual rehearsal recorded for U1. A unit
test cannot build a virtual environment honestly.
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"

# Packages that must never be DECLARED by the slim core: the audio DSP stack,
# the machine-learning stack, and the web framework. A friend who only wants
# playlist curation should not download any of them.
#
# Declared, not present. numpy does land in a slim install, transitively, because
# pyrekordbox requires it and guarded database access is Core. That is fine —
# numpy is neither DSP nor ML on its own. It stays on this list because the
# analysis module must keep declaring it explicitly: relying on a transitive
# dependency of an unrelated package for a module's own import is how a
# pyrekordbox release note quietly breaks key detection.
HEAVY_PACKAGES = {
    "librosa",
    "numpy",
    "scipy",
    "torch",
    "panns-inference",
    "fastapi",
    "uvicorn",
    "sse-starlette",
    "jinja2",
    "pywebview",
}


@pytest.fixture(scope="module")
def pyproject() -> dict:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)


def _distribution_name(specifier: str) -> str:
    """Reduce ``"librosa>=0.10"`` to ``"librosa"``.

    Extras and environment markers are stripped too, so ``cratekit[analysis]``
    and ``foo>=1; python_version < '3.13'`` both reduce to their bare name.
    """
    head = specifier.split(";", 1)[0]
    head = head.split("[", 1)[0]
    return re.split(r"[<>=!~ ]", head, maxsplit=1)[0].strip().lower()


def test_python_bound_is_closed_at_both_ends(pyproject):
    """KTD19 pins 3.12 and 3.13. An open upper bound is the failure we avoid.

    Without the ceiling, a resolver happily installs on 3.14 and the vendored
    downloader fails later with an error that names none of this.
    """
    requires = pyproject["project"]["requires-python"]
    assert ">=3.12" in requires
    assert "<3.14" in requires


def test_license_is_mit_and_the_text_ships(pyproject):
    project = pyproject["project"]
    assert project["license"] == "MIT"
    assert "LICENSE" in project["license-files"]
    assert (REPO_ROOT / "LICENSE").read_text().startswith("MIT License")


def test_slim_core_carries_no_dsp_web_or_ml_dependency(pyproject):
    """R5's slim profile is a promise about download size, not just a config flag."""
    core = {_distribution_name(spec) for spec in pyproject["project"]["dependencies"]}
    offenders = sorted(core & HEAVY_PACKAGES)
    assert not offenders, (
        f"slim core declares heavy dependencies {offenders}; "
        "move each into the extra named for the module that needs it (KTD7)"
    )


def test_extras_are_named_for_modules_and_carry_the_weight(pyproject):
    """KTD7: extras groups map one-to-one onto modules.

    The analysis extra must actually pull the DSP stack, otherwise enabling the
    module silently produces a broken install rather than a clear one.
    """
    extras = pyproject["project"]["optional-dependencies"]
    analysis = {_distribution_name(spec) for spec in extras["analysis"]}
    assert "librosa" in analysis

    vocals = {_distribution_name(spec) for spec in extras["vocals"]}
    assert "torch" in vocals

    # The aggregate must name every extra that corresponds to a feature module,
    # so installing it cannot silently miss one. Two extras are deliberately not
    # feature modules and are excluded by name: "all" itself, and "dev", which
    # carries contributor tooling. A user installing every feature should not
    # thereby install a test runner and a commit-hook framework.
    NON_MODULE_EXTRAS = {"all", "dev"}
    aggregate = extras["all"]
    assert len(aggregate) == 1
    named = set(re.search(r"\[(.*)\]", aggregate[0]).group(1).split(","))
    module_extras = set(extras) - NON_MODULE_EXTRAS
    assert named == module_extras, (
        "the 'all' aggregate must list exactly the feature-module extras; "
        "a new module extra was added without adding it here"
    )


def test_one_console_script_named_crate(pyproject):
    """R2: one entry point replaces the source system's thirty console scripts."""
    scripts = pyproject["project"]["scripts"]
    assert list(scripts) == ["crate"]
    assert scripts["crate"] == "cratekit.cli:main"


def test_no_author_identity_in_shipped_metadata(pyproject):
    """R1: shipped artifacts carry no author name, path, volume, or account."""
    authors = pyproject["project"]["authors"]
    assert authors == [{"name": "Cratekit contributors"}]


# ---------------------------------------------------------------------------
# scripts/ci_deps.py
#
# CI installs whatever this script prints, so a malformed line is a broken build
# on every branch at once. It shipped with no test and its first real CI run
# failed: it shell-quoted each line, and the workflow consumed it with command
# substitution, which word-splits but does NOT strip quotes, so pip received a
# literal `'lxml>=5.0'` and rejected it.
#
# These tests exist to pin the output CONTRACT rather than the implementation:
# every line parses as a real requirement, and nothing decorates it.
# ---------------------------------------------------------------------------


def _run_ci_deps(*args: str) -> list[str]:
    """Invoke the script the way CI does and return its stdout lines."""
    import subprocess

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "ci_deps.py"), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


@pytest.mark.parametrize("args", [(), ("analysis",), ("vocals",), ("web",), ("dev",)])
def test_every_emitted_line_parses_as_a_requirement(args):
    """Each line must be installable as-is, with no unwrapping by the caller."""
    from packaging.requirements import Requirement

    lines = _run_ci_deps(*args)
    assert lines, f"ci_deps.py printed nothing for {args!r}"
    for line in lines:
        # Requirement() raises InvalidRequirement on anything pip would reject,
        # including the quoted form that broke the first CI run.
        Requirement(line)


def test_emitted_lines_carry_no_shell_decoration():
    """The output is consumed by xargs, which does not strip quotes either.

    Asserted separately from the parse check because it names the specific
    regression: a quote character here is always a bug, never a valid specifier.
    """
    for line in _run_ci_deps():
        assert not (line.startswith(("'", '"')) or line.endswith(("'", '"'))), (
            f"{line!r} is shell-quoted; emit the raw specifier and let the "
            f"caller use xargs"
        )
        assert line == line.strip(), f"{line!r} carries surrounding whitespace"


def test_core_output_is_exactly_the_declared_core_dependencies(pyproject):
    """The whole point of the script is that CI never mirrors this list by hand."""
    assert _run_ci_deps() == pyproject["project"]["dependencies"]


def test_an_unknown_extra_fails_loudly_and_names_the_known_ones():
    """A typo in a workflow must not silently install nothing."""
    import subprocess

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "ci_deps.py"), "nope"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert not result.stdout.strip(), "a failed lookup must print no specifiers"
    assert "analysis" in result.stderr, "the error should name the known extras"
