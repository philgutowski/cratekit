"""U1: the package declares an installable, portable, genuinely slim core.

Read from ``pyproject.toml`` as data; the import guard (U269) also reads the installed
metadata. A clean install is proved by CI's ``cold-install`` job, not here.
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

# Packages the slim core must never DECLARE: the DSP, machine learning and web stacks.
# numpy arrives through pyrekordbox, but the analysis module must still declare it.
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
    """Reduce ``"librosa>=0.10"`` to ``"librosa"``, extras and environment markers stripped."""
    head = specifier.split(";", 1)[0]
    head = head.split("[", 1)[0]
    return re.split(r"[<>=!~ ]", head, maxsplit=1)[0].strip().lower()


def test_python_bound_is_closed_at_both_ends(pyproject):
    """KTD19 pins 3.12 and 3.13, closed at both ends, so 3.14 never installs and fails obscurely."""
    requires = pyproject["project"]["requires-python"]
    assert ">=3.12" in requires
    assert "<3.14" in requires


def _clauses(specifier: str) -> frozenset[str]:
    """A requires-python string as a SET of clauses, since metadata reorders ``>=3.12,<3.14``."""
    return frozenset(part.strip() for part in specifier.split(",") if part.strip())


def test_the_installed_metadata_carries_the_bound_pyproject_declares(pyproject):
    """The installed metadata carries the bound pyproject declares, since doctor reads it
    (KTD19) and a stale ``dist-info`` once made it call the running 3.12 unsupported."""
    from importlib import metadata

    from cratekit.cli import registry

    try:
        installed = metadata.metadata(registry.DISTRIBUTION)["Requires-Python"]
    except metadata.PackageNotFoundError:  # pragma: no cover - see the assertion
        installed = None

    assert installed is not None, (
        f"{registry.DISTRIBUTION} is not installed here, so nothing enforces the bound; "
        f"install the package, editable is enough"
    )
    assert _clauses(installed) == _clauses(pyproject["project"]["requires-python"]), (
        f"the installed metadata says {installed!r} and pyproject declares "
        f"{pyproject['project']['requires-python']!r}; reinstall the distribution"
    )


def test_the_doctor_reads_the_installed_bound_rather_than_a_constant():
    """Nothing in the package repeats the bound as a constant."""
    import ast

    from cratekit.cli import doctor

    assert doctor._declared_python_bound() is not None
    # Over the syntax tree, so a comment explaining the ceiling does not fire.
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


# ── U269: every core dependency earns its place, and the comments name real files. ───

#: A core dependency declared for another reason than our own import, with it. Empty.
DECLARED_WITHOUT_AN_IMPORT: dict[str, str] = {}


def _imported_top_level_names(root: Path) -> set[str]:
    """Every top level name an import under ``root`` reaches, function level and literal
    ``importlib.import_module`` ones included; relative imports are the package itself."""
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
    """Every core dependency is imported by the package, the vendored tree included, its
    import names read from the installed metadata (Pillow is ``PIL``)."""
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
        requirement = Requirement(spec)
        name = canonicalize_name(requirement.name)
        if name in DECLARED_WITHOUT_AN_IMPORT:
            continue
        if requirement.marker is not None and not requirement.marker.evaluate():
            # Declared for another platform, judged by the battery there.
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


#: A repository path ``pyproject.toml`` names, with an optional ``::test_name``; never a
#: URL's tail, a glob's prefix such as ``tests/test_*.py``, or a sentence's full stop.
_NAMED_PATH = re.compile(
    r"(?<![\w./:-])((?:tests|scripts|src|docs|vendor)/[\w./-]*[\w/])(?![\w*/-]|\.[\w*])(?:::(\w+))?"
)


def test_every_path_pyproject_names_exists():
    """Every path ``pyproject.toml`` names exists, so a comment never points at a missing guard."""
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
    """KTD7: extras map one-to-one onto modules, and the analysis extra pulls the DSP stack."""
    extras = pyproject["project"]["optional-dependencies"]
    analysis = {_distribution_name(spec) for spec in extras["analysis"]}
    assert "librosa" in analysis

    vocals = {_distribution_name(spec) for spec in extras["vocals"]}
    assert "torch" in vocals

    # The aggregate names every feature module's extra; "all" and "dev" are not modules.
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


# ── scripts/ci_deps.py ───────────────────────────────────────────────────────
# CI installs whatever this prints, so every line parses as a requirement, undecorated:
# its first run handed pip a shell quoted ``'lxml>=5.0'``.


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
        # Raises on anything pip would reject, the quoted form included.
        Requirement(line)


def test_emitted_lines_carry_no_shell_decoration():
    """No line carries a quote: xargs does not strip quotes either."""
    for line in _run_ci_deps():
        assert not (line.startswith(("'", '"')) or line.endswith(("'", '"'))), (
            f"{line!r} is shell-quoted; emit the raw specifier"
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
