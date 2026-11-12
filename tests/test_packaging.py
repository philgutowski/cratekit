"""U1: the package declares an installable, portable, genuinely slim core.

These assertions run against ``pyproject.toml`` as data rather than against an
installed distribution, so they fail in the pull request that introduces the
regression instead of on the first friend's machine.

The end-to-end proof that a clean environment installs and imports lives in
CI's ``cold-install`` job and in the manual rehearsal recorded for U1. A unit
test cannot build a virtual environment honestly.
"""

from __future__ import annotations

import ast
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


def _clauses(specifier: str) -> frozenset[str]:
    """A requires-python string as a SET of clauses, whitespace and order removed.

    Order is not meaningful in a specifier and the two sources spell it
    differently: pyproject says ``>=3.12,<3.14`` and the metadata generated from
    it comes back ``<3.14,>=3.12``. Comparing the strings would fail on a
    difference that means nothing, and comparing nothing at all is what left the
    two free to differ in ways that mean everything.
    """
    return frozenset(part.strip() for part in specifier.split(",") if part.strip())


def test_the_installed_metadata_carries_the_bound_pyproject_declares(pyproject):
    """KTD19's bound is READ from packaging metadata by doctor, so the two must agree.

    ``cli/doctor`` deliberately does not repeat the bound: it reads
    ``Requires-Python`` from this distribution's own metadata, on the argument
    that a second copy is a copy that drifts. That argument is only true while
    something PINS the metadata to the declaration it was built from, and nothing
    did: the assertions above read the pyproject text and never opened the
    installed distribution at all.

    What that permits is not theoretical. A stale ``dist-info`` left behind by an
    earlier editable install carries whatever bound was declared when it was
    generated, so with ``>=3.9,<3.11`` sitting there doctor reports the running
    3.12 as UNSUPPORTED and exits the whole run on PRECONDITION, driven entirely
    by a file nobody looked at. The failure names the interpreter, which is the
    one thing that is not wrong.
    """
    from importlib import metadata

    from cratekit.cli import registry

    try:
        installed = metadata.metadata(registry.DISTRIBUTION)["Requires-Python"]
    except metadata.PackageNotFoundError:  # pragma: no cover - see the assertion
        installed = None

    assert installed is not None, (
        f"{registry.DISTRIBUTION} is not installed in this environment, so "
        f"doctor's interpreter bound reads as 'not asserted' and this "
        f"declaration is enforced by nothing. Install the package, editable is "
        f"enough, before trusting a green run."
    )
    assert _clauses(installed) == _clauses(pyproject["project"]["requires-python"]), (
        f"the installed metadata says {installed!r} and pyproject declares "
        f"{pyproject['project']['requires-python']!r}. Doctor reads the first and "
        f"this repository maintains the second, so a run can refuse an "
        f"interpreter this project supports, or accept one it does not. "
        f"Reinstall the distribution."
    )


def test_the_doctor_reads_the_installed_bound_rather_than_a_constant():
    """The other half of the pin: nothing in the package repeats the number.

    A constant here would be the drift the test above exists to catch, arriving
    from the other direction and invisible to it.
    """
    import ast

    from cratekit.cli import doctor

    assert doctor._declared_python_bound() is not None
    # Over the syntax tree rather than the text, so a COMMENT that mentions the
    # ceiling while explaining why it is not repeated does not fire the guard
    # that exists to stop it being repeated.
    sources: list[str] = []
    for path in sorted((REPO_ROOT / "src").rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if "3.14" in node.value and "<" in node.value:
                    sources.append(f"{path.name}:{node.lineno}")
    assert not sources, (
        f"the interpreter ceiling is written into {sources} as well as into "
        f"pyproject.toml, so one of the two is now the copy that drifts"
    )


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


# ---------------------------------------------------------------------------
# U269: every core dependency earns its place, and the comments name real files.
#
# lxml sat in the core list for months "for rekordbox XML parsing" while every
# reader of an export scanned bytes and nothing imported it, so each install
# downloaded and unpacked a compiled library that no line of Cratekit used. No
# test could see that: the slim core test above asks whether a dependency is
# heavy, never whether anything needs it.
# ---------------------------------------------------------------------------

#: A core dependency declared for a reason other than an import of our own, such
#: as bounding a transitive dependency, is named here with that reason. Empty
#: today: every core dependency is imported by the package.
DECLARED_WITHOUT_AN_IMPORT: dict[str, str] = {}


def _imported_top_level_names(root: Path) -> set[str]:
    """Every top level name an import under ``root`` reaches, lazy ones included.

    Read from the syntax tree, so an import inside a function counts (the
    Bandcamp transport imports ``curl_cffi`` only when a request is made), and
    an ``importlib.import_module("name")`` with a literal name counts too.
    Relative imports name the package itself and are skipped.
    """
    names: set[str] = set()
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_bytes(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    names.add(node.module.split(".", 1)[0])
            elif isinstance(node, ast.Call) and node.args:
                func = node.func
                called = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
                first = node.args[0]
                if called in ("import_module", "__import__") and isinstance(first, ast.Constant):
                    if isinstance(first.value, str):
                        names.add(first.value.split(".", 1)[0])
    return names


def test_every_core_dependency_is_imported_by_the_package(pyproject):
    """A core dependency nothing imports is weight every install carries for nothing.

    The import names come from the installed distributions' own metadata, never
    from a table written here, because a hand table of which distribution
    provides which module is the second copy that drifts (Pillow is ``PIL``,
    pycryptodome is ``Crypto``, python-ffmpeg is ``ffmpeg``). The sweep covers
    the whole package, the vendored downloader included, because the vendored
    tree's own dependencies are declared in the core list too.
    """
    from importlib.metadata import packages_distributions

    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    provides: dict[str, set[str]] = {}
    for top_level, distributions in packages_distributions().items():
        for distribution in distributions:
            provides.setdefault(canonicalize_name(distribution), set()).add(top_level)

    imported = _imported_top_level_names(REPO_ROOT / "src" / "cratekit")
    not_installed, unused = [], []
    for spec in pyproject["project"]["dependencies"]:
        name = canonicalize_name(Requirement(spec).name)
        if name in DECLARED_WITHOUT_AN_IMPORT:
            continue
        if name not in provides:
            not_installed.append(name)
        elif not provides[name] & imported:
            unused.append(f"{name} (provides {sorted(provides[name])})")

    assert not not_installed, (
        f"core dependencies {not_installed} are not installed here, so the modules "
        "they provide cannot be read; install the package with its dependencies"
    )
    assert not unused, (
        f"core dependencies {unused} are imported nowhere under src/cratekit; drop "
        "each one, or name it in DECLARED_WITHOUT_AN_IMPORT with the reason it stays"
    )


#: A repository path a comment in ``pyproject.toml`` names, with an optional
#: ``::test_name`` after a test file.
_NAMED_PATH = re.compile(r"\b((?:tests|scripts|src)/[\w./-]*[\w/])(?:::(\w+))?")


def test_every_path_pyproject_names_exists():
    """A comment that names a guard must name one that exists.

    The slim core comment named ``tests/test_slim_core.py`` as the test that
    fails the build when a heavy dependency appears, a file that never existed
    under that name, so a reader looking for the guard found nothing.
    """
    text = PYPROJECT.read_text(encoding="utf-8")
    named = _NAMED_PATH.findall(text)
    assert named, "pyproject.toml names no repository path; the pattern no longer reads it"

    missing = []
    for relative, function in named:
        path = REPO_ROOT / relative.rstrip("/")
        if not path.exists():
            missing.append(relative)
        elif function and not re.search(
            rf"^def {re.escape(function)}\(", path.read_text(encoding="utf-8"), re.M
        ):
            missing.append(f"{relative}::{function}")
    assert not missing, f"pyproject.toml names paths that do not exist: {missing}"


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
