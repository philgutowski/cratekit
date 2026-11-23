"""U13: the vendored downloader is importable, licensed, and carries no secrets.

KTD4 vendors the downloader as a source tree because its upstream was deleted
from GitHub and PyPI in December 2025, so a committed tree is the only way a
clone can acquire music. Each test pins one quieter failure vendoring brings:
a dependency specifier creeping back in, the AGPL licence going missing
(KTD19), a credential riding along, a tempo tag surviving (R17), and a
re-vendor dropping the patches. A working download needs an account and the
network, so it is the attended smoke test in ``vendor/README.md``.
"""

from __future__ import annotations

import ast
import importlib
import re
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
VENDOR_ROOT = REPO_ROOT / "src" / "cratekit" / "_vendor"
VENDORED_PACKAGE = VENDOR_ROOT / "downloader"
PYPROJECT = REPO_ROOT / "pyproject.toml"

# The upstream distribution name in every spelling a specifier could use; PEP
# 503 normalises "-" and "_" to one project.
VENDORED_PROJECT_SPELLINGS = ("tidal-dl-ng", "tidal_dl_ng", "tidaldlng")


@pytest.fixture(scope="module")
def pyproject() -> dict:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)


def _vendored_sources() -> list[Path]:
    return sorted(VENDORED_PACKAGE.rglob("*.py"))


# ═══════════════════════════════════════════════════════════════════════════
# It imports, from inside cratekit._vendor, with no network
# ═══════════════════════════════════════════════════════════════════════════


def test_the_vendored_package_imports_from_inside_cratekit_vendor():
    """The package imports from ``cratekit._vendor``, which a file check could not prove (KTD4).

    Every absolute self import had to be re-rooted. No network is touched: the
    one outbound call sits behind a function nothing here invokes.
    """
    module = importlib.import_module("cratekit._vendor.downloader")
    assert module.__version__, "the vendored package reports no version"


@pytest.mark.parametrize(
    "name",
    [
        "cratekit._vendor.downloader.cli",
        "cratekit._vendor.downloader.config",
        "cratekit._vendor.downloader.download",
        "cratekit._vendor.downloader.metadata",
        "cratekit._vendor.downloader.helper.path",
        "cratekit._vendor.downloader.helper.tidal",
        "cratekit._vendor.downloader.helper.decryption",
        "cratekit._vendor.downloader.model.cfg",
    ],
)
def test_every_module_on_the_download_path_imports(name):
    """One case per module on the path from "give me a track" to the file on disk."""
    assert importlib.import_module(name) is not None


def test_every_vendored_module_byte_compiles():
    """Every vendored file byte compiles, standing in for ruff's E9, which excludes the tree."""
    for source in _vendored_sources():
        compile(source.read_text(encoding="utf-8"), str(source), "exec")


def test_no_module_still_imports_itself_by_its_upstream_name():
    """No module still imports itself by its upstream name, lazy imports included."""
    stragglers = [
        f"{source.relative_to(REPO_ROOT)}:{number}"
        for source in _vendored_sources()
        for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1)
        if re.match(r"\s*(from|import)\s+tidal_dl_ng\b", line)
    ]
    assert not stragglers, (
        "these lines still import the vendored package by its upstream name, which "
        "does not resolve under cratekit._vendor:\n  " + "\n  ".join(stragglers)
    )


# ═══════════════════════════════════════════════════════════════════════════
# No dependency specifier names the vendored project
# ═══════════════════════════════════════════════════════════════════════════


def test_no_dependency_specifier_names_the_vendored_project(pyproject):
    """No dependency list, extras included, names the deleted project."""
    project = pyproject["project"]
    groups = {"dependencies": project.get("dependencies", [])}
    groups.update(project.get("optional-dependencies", {}))

    offenders = [
        f"[{group}] {spec}"
        for group, specs in groups.items()
        for spec in specs
        if any(name in spec.lower() for name in VENDORED_PROJECT_SPELLINGS)
    ]
    assert not offenders, (
        "the vendored downloader is named as a dependency:\n  "
        + "\n  ".join(offenders)
        + "\nIt is a source tree under src/cratekit/_vendor/ precisely because no "
        "public index still serves it (KTD4)."
    )


def test_nothing_in_the_repository_declares_it_as_a_requirement():
    """No requirements file, CI step or install line anywhere names it either."""
    patterns = re.compile(
        r"(?:pip\s+install|uv\s+(?:pip\s+install|add)|poetry\s+add)[^\n]*"
        r"(?:tidal[-_]dl[-_]ng)",
        re.IGNORECASE,
    )
    offenders: list[str] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        # Every dot-directory is skipped, including .venv and .worktrees, whose extra
        # checkouts would be slow to walk and report another checkout's files.
        if any(part.startswith(".") for part in path.relative_to(REPO_ROOT).parts):
            continue
        if VENDOR_ROOT in path.parents or path.suffix in {".pyc", ".gz"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if patterns.search(text):
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert not offenders, (
        "these files tell an installer to fetch the vendored project from an "
        f"index that deleted it: {offenders}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The licence ships, intact, in both places
# ═══════════════════════════════════════════════════════════════════════════


def test_the_vendored_licence_is_present_and_non_empty():
    """KTD19: the vendored component keeps its own AGPL text, present and non-empty."""
    from cratekit._vendor import DOWNLOADER, license_text

    text = license_text(DOWNLOADER)
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" in text
    assert len(text) > 10_000, "the AGPL text is far shorter than the real licence"


def test_the_declared_licence_matches_the_text_that_ships():
    """The declared SPDX id matches the licence text that ships."""
    from cratekit._vendor import DOWNLOADER, license_text

    assert DOWNLOADER.license_id == "AGPL-3.0-only"
    assert "Version 3, 19 November 2007" in license_text(DOWNLOADER)


def test_the_two_licence_copies_cannot_drift():
    """The licence copy in the package and at the root cannot drift."""
    inside = (VENDORED_PACKAGE / "LICENSE").read_bytes()
    at_root = (REPO_ROOT / "vendor" / "LICENSE.downloader").read_bytes()
    assert inside == at_root, (
        "the two copies of the vendored licence differ; "
        "re-run scripts/revendor_downloader.py rather than editing either by hand"
    )


def test_the_licence_ships_as_package_data(pyproject):
    """The licence is package data, so it reaches the wheel and not only the checkout."""
    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert "LICENSE" in package_data["cratekit._vendor.downloader"]


def test_the_recorded_version_matches_the_code_on_disk():
    """The recorded version matches the code on disk, the only provenance left."""
    from cratekit._vendor import DOWNLOADER

    module = importlib.import_module("cratekit._vendor.downloader")
    assert module.__version__ == DOWNLOADER.version


# ═══════════════════════════════════════════════════════════════════════════
# No credential material, in any of the three shapes it took upstream
# ═══════════════════════════════════════════════════════════════════════════


def test_the_atmos_client_credentials_are_empty():
    """The Atmos client credentials, base64 split across literals upstream, decode to empty."""
    constants = importlib.import_module("cratekit._vendor.downloader.constants")
    assert constants.ATMOS_CLIENT_ID == ""
    assert constants.ATMOS_CLIENT_SECRET == ""


def test_no_module_in_the_vendored_tree_carries_a_credential_literal():
    """Any assignment or mapping entry named like a client credential is empty.

    Stricter than the repository scan, whose pattern expects snake_case while
    upstream also uses camelCase JSON keys.
    """
    offenders: list[str] = []
    credential_name = re.compile(
        r"client_?(?:id|secret)|api_?key|access_?token|refresh_?token", re.IGNORECASE
    )

    for source in _vendored_sources():
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                names = [
                    t.id
                    for t in node.targets
                    if isinstance(t, ast.Name) and credential_name.search(t.id)
                ]
                if names and isinstance(node.value, ast.Constant) and node.value.value:
                    offenders.append(f"{source.name}: {names[0]} has a non-empty literal")
            if isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values):
                    if (
                        isinstance(key, ast.Constant)
                        and isinstance(key.value, str)
                        and credential_name.search(key.value)
                        and isinstance(value, ast.Constant)
                        and value.value
                    ):
                        offenders.append(f"{source.name}: {key.value!r} maps to a literal")

    assert not offenders, "credential literals in the vendored tree:\n  " + "\n  ".join(offenders)


def test_no_credential_carrying_module_was_vendored():
    """``api.py`` stays out: plaintext client pairs, a JSONDecodeError at import, no importer."""
    assert not (VENDORED_PACKAGE / "api.py").exists(), (
        "api.py was vendored. It carries plaintext third-party OAuth client "
        "secrets and is upstream-broken at import; scripts/revendor_downloader.py "
        "drops it deliberately."
    )


def test_no_session_or_token_file_rode_along():
    """No session or token file, nor any compressed payload, rode along from the extract."""
    strays = [
        str(path.relative_to(REPO_ROOT))
        for path in VENDOR_ROOT.rglob("*")
        if path.is_file()
        and re.search(r"(session|token|credential|secret)", path.name, re.IGNORECASE)
    ]
    assert not strays, f"credential-shaped files under the vendored tree: {strays}"


# ═══════════════════════════════════════════════════════════════════════════
# R17: the vendored downloader writes no tempo tag
# ═══════════════════════════════════════════════════════════════════════════


def test_the_vendored_downloader_writes_no_tempo_tag():
    """R17: no tempo tag in any of the three shapes upstream wrote.

    A Vorbis ``BPM`` comment, an ID3 ``TBPM`` frame, an MP4 ``tmpo`` atom: each
    seeds a grid in rekordbox, and a wrong grid moves every cue and loop. The
    repository's own R17 guard sees only subscript assignments, missing the ID3
    call and the MP4 key.
    """
    offenders: list[str] = []

    for source in _vendored_sources():
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            # Shape 1: a mapping write under a tempo key (Vorbis, MP4).
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.slice, ast.Constant)
                        and str(target.slice.value).lower() in {"bpm", "tmpo", "tempo"}
                    ):
                        offenders.append(
                            f"{source.name}:{node.lineno} writes the tag "
                            f"{target.slice.value!r}"
                        )
            # Shape 2: an ID3 tempo frame constructed and added (MP3, AIFF).
            if isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
                if name in {"TBPM", "TMPO"}:
                    offenders.append(f"{source.name}:{node.lineno} builds an {name} frame")

    assert not offenders, (
        "R17 violations in the vendored downloader:\n  "
        + "\n  ".join(offenders)
        + "\nBeat grids are rekordbox-only. Do not loosen this assertion; re-run "
        "scripts/revendor_downloader.py, which removes these writes."
    )


def test_the_provider_tempo_never_reaches_the_metadata_writer():
    """The provider tempo is zeroed at the call site, so a future writer has nothing to write."""
    download = (VENDORED_PACKAGE / "download.py").read_text(encoding="utf-8")
    assert "bpm=0," in download, (
        "the metadata writer is being handed the provider's tempo again; "
        "scripts/revendor_downloader.py pins it to zero (R17)"
    )


def test_the_patch_record_names_as_many_patches_as_the_script_applies():
    """Every vendored file the script patches is named in ``vendor/README.md``'s patch record."""
    readme = (REPO_ROOT / "vendor" / "README.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\d+) \| ", readme, flags=re.MULTILINE)
    assert rows, "the vendor patch table changed shape; this guard reads its numbered rows"
    assert [int(n) for n in rows] == list(range(1, len(rows) + 1)), (
        "the patch table's row numbers are not a gapless sequence"
    )

    # Row counts are not compared, since one row can cover several patches. A
    # second patch to a listed file is not caught.
    script = (REPO_ROOT / "scripts" / "revendor_downloader.py").read_text(encoding="utf-8")
    patched_files = set(re.findall(r'relative_path="([^"]+)"', script))
    assert patched_files, "the revendor script's patch declarations changed shape"

    table = readme[readme.index("### Patches") :]
    undocumented = sorted(f for f in patched_files if f not in table)
    assert not undocumented, (
        f"scripts/revendor_downloader.py patches {undocumented} and vendor/README.md's "
        f"patch table never names those files; a patch nobody recorded is one the "
        f"next re-vendor drops silently"
    )


def _calls_in(function_name: str, module: str) -> set[str]:
    """Every method name a named function actually EVALUATES, from the syntax tree.

    Not the text: the patch's own comment names ``login_oauth_simple``.
    """
    tree = ast.parse((VENDORED_PACKAGE / module).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return {
                inner.func.attr
                for inner in ast.walk(node)
                if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Attribute)
            }
    raise AssertionError(f"{module} no longer defines {function_name}()")


def test_the_interactive_login_is_pkce_and_the_device_flow_is_gone():
    """R-196: login is PKCE; the device flow, served lossy audio, is gone with no flag."""
    calls = _calls_in("login", "config.py")
    assert "login_pkce" in calls, (
        "the vendored login no longer mints a PKCE session; re-run "
        "scripts/revendor_downloader.py rather than editing the tree by hand"
    )
    assert "login_oauth_simple" not in calls, (
        "the device-linking login is live again, and the provider serves that "
        "client lossy audio (R-196)"
    )


def test_the_persisted_token_records_which_client_minted_it():
    """The persisted token keeps ``is_pkce``, so it does not refresh as a lossy device token."""
    from cratekit._vendor.downloader.model.cfg import Token

    assert "is_pkce" in Token.__dataclass_fields__, (
        "the token model dropped is_pkce; re-run scripts/revendor_downloader.py"
    )

    assigned = set()
    tree = ast.parse((VENDORED_PACKAGE / "config.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "token_persist":
            for inner in ast.walk(node):
                if isinstance(inner, ast.Attribute) and isinstance(inner.ctx, ast.Store):
                    assigned.add(inner.attr)
    assert "is_pkce" in assigned, "token_persist writes the four keys again and drops is_pkce"


# ═══════════════════════════════════════════════════════════════════════════
# The reductions hold
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "relative",
    ["gui.py", "logger.py", "dialog.py", "worker.py", "helper/gui.py", "ui"],
)
def test_the_gui_half_is_not_vendored(relative):
    """The GUI half, which imports PySide6 that Cratekit never installs, is not vendored."""
    assert not (VENDORED_PACKAGE / relative).exists()


def test_the_download_path_needs_no_gui_toolkit(pyproject):
    """The reduction has to show up in the dependency list, or it saved nothing."""
    declared = " ".join(pyproject["project"]["dependencies"]).lower()
    for gui_only in ("pyside6", "pyqtdarktheme", "ansi2html", "coloredlogs"):
        assert gui_only not in declared, (
            f"{gui_only} is declared but only the un-vendored GUI half used it"
        )


def test_the_state_directory_name_is_pinned():
    """``__name_display__`` names the on-disk state directory, so it is pinned, not derived."""
    module = importlib.import_module("cratekit._vendor.downloader")
    # A neutral name since U197, and never the derived dotted ``_vendor`` path
    # with a "-dev" suffix.
    assert module.__name_display__ == "cratekit-downloader"
    assert "_vendor" not in module.__name_display__
    assert "." not in module.__name_display__
    assert not module.__name_display__.endswith("-dev")


def test_nothing_outside_the_tree_reaches_the_package_by_its_old_path():
    """U197 renamed the package: nothing outside the tree reaches it or its licence by the old path.

    Swept over code, tests, scripts, packaging and CI, dotted, slashed, joined
    on a ``Path`` and relative to ``_vendor``. This file spells the old names, so
    it is left out.
    """
    old_names = re.compile(
        r"_vendor[./]tidal_dl_ng"
        r"""|["']_vendor["']\s*/\s*["']tidal_dl_ng["']"""
        r"""|["']tidal_dl_ng/"""
        r"|TIDAL_DL_NG|LICENSE\.tidal-dl-ng"
    )
    roots = [REPO_ROOT / "src", REPO_ROOT / "tests", REPO_ROOT / "scripts"]
    files = [path for root in roots for suffix in ("*.py", "*.sh") for path in root.rglob(suffix)]
    files += [PYPROJECT]
    files += sorted(
        path for suffix in ("*.yml", "*.yaml") for path in (REPO_ROOT / ".github").rglob(suffix)
    )
    this_file = Path(__file__).resolve()
    stragglers = [
        f"{path.relative_to(REPO_ROOT)}:{number}"
        for path in files
        if path.resolve() != this_file
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if old_names.search(line)
    ]
    assert files and not stragglers, (
        "these lines still name the vendored package by its old path:\n  "
        + "\n  ".join(stragglers)
    )


# ── the state directory an installation made before U197 is adopted ────────


def _revendor_script():
    """The revendor script as a module, so its declared patch text can be read."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "revendor_downloader", REPO_ROOT / "scripts" / "revendor_downloader.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_tree_carries_the_adoption_patch_the_script_declares():
    """The tree carries the adoption patch the script declares, compared by the patch's own text."""
    script = _revendor_script()
    path_module = (VENDORED_PACKAGE / "helper" / "path.py").read_text(encoding="utf-8")
    assert script.PATCH_STATE_DIRECTORY_ADOPTION.new in path_module
    assert script.PATCH_STATE_DIRECTORY_ADOPTION in _applied_patches(script)
    module = importlib.import_module("cratekit._vendor.downloader")
    assert module.__name_display__ == script.STATE_DIRECTORY_NAME


def _applied_patches(script) -> list:
    """Every patch object ``main`` applies, read off its source rather than run."""
    source = (REPO_ROOT / "scripts" / "revendor_downloader.py").read_text(encoding="utf-8")
    body = source[source.index("def main(") :]
    names = re.findall(r"^\s+(PATCH_[A-Z0-9_]+),$", body, flags=re.MULTILINE)
    return [getattr(script, name) for name in names]


def _state_directories(tmp_path, monkeypatch) -> tuple[Path, Path]:
    """The new and the old state directory under a configuration home of the test's own."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    return tmp_path / "cratekit-downloader", tmp_path / "tidal-dl-ng"


def test_the_old_state_directory_is_moved_into_place_with_its_token(tmp_path, monkeypatch):
    from cratekit._vendor.downloader.helper import path as tool_path

    new, old = _state_directories(tmp_path, monkeypatch)
    old.mkdir()
    (old / "token.json").write_text('{"is_pkce": true}', encoding="utf-8")
    (old / "settings.json").write_text("{}", encoding="utf-8")

    assert tool_path.path_config_base() == str(new)
    assert not old.exists(), "a copy would leave a second plaintext token behind"
    assert (new / "token.json").read_text(encoding="utf-8") == '{"is_pkce": true}'
    assert (new / "settings.json").is_file()
    assert tool_path.path_file_token() == str(new / "token.json")


def test_the_new_state_directory_wins_and_the_old_one_is_left_alone(tmp_path, monkeypatch):
    from cratekit._vendor.downloader.helper import path as tool_path

    new, old = _state_directories(tmp_path, monkeypatch)
    new.mkdir()
    (new / "token.json").write_text("new", encoding="utf-8")
    old.mkdir()
    (old / "token.json").write_text("old", encoding="utf-8")

    assert tool_path.path_config_base() == str(new)
    assert (new / "token.json").read_text(encoding="utf-8") == "new"
    assert (old / "token.json").read_text(encoding="utf-8") == "old"


def test_no_old_state_directory_resolves_the_new_one_and_makes_nothing(tmp_path, monkeypatch):
    from cratekit._vendor.downloader.helper import path as tool_path

    new, old = _state_directories(tmp_path, monkeypatch)
    assert tool_path.path_config_base() == str(new)
    assert not new.exists() and not old.exists()


def test_a_file_under_the_old_name_is_not_moved_into_the_state_directory_slot(
    tmp_path, monkeypatch
):
    """Only a directory is adopted; a file in the slot would break every later state write."""
    from cratekit._vendor.downloader.helper import path as tool_path

    new, old = _state_directories(tmp_path, monkeypatch)
    old.write_text("not a directory", encoding="utf-8")

    assert tool_path.path_config_base() == str(new)
    assert not new.exists()
    assert old.read_text(encoding="utf-8") == "not a directory"


def test_a_failed_move_keeps_the_old_state_directory_in_use(tmp_path, monkeypatch):
    from cratekit._vendor.downloader.helper import path as tool_path

    new, old = _state_directories(tmp_path, monkeypatch)
    old.mkdir()
    (old / "token.json").write_text("kept", encoding="utf-8")

    def refuse(source, destination):
        raise PermissionError(13, "refused", source)

    monkeypatch.setattr(tool_path.os, "rename", refuse)
    assert tool_path.path_config_base() == str(old)
    assert tool_path.path_file_token() == str(old / "token.json")
    assert (old / "token.json").read_text(encoding="utf-8") == "kept"


def test_a_move_lost_to_another_process_resolves_the_new_directory(tmp_path, monkeypatch):
    """Two runs adopting at once: the one whose rename fails finds the other's result."""
    from cratekit._vendor.downloader.helper import path as tool_path

    new, old = _state_directories(tmp_path, monkeypatch)
    old.mkdir()
    real_rename = tool_path.os.rename

    def raced(source, destination):
        real_rename(source, destination)
        raise FileNotFoundError(2, "gone", source)

    monkeypatch.setattr(tool_path.os, "rename", raced)
    assert tool_path.path_config_base() == str(new)


def test_version_detection_does_not_read_a_nearby_pyproject():
    """Version detection never reads a nearby ``pyproject.toml``.

    Upstream walks three parents from its ``__file__`` for one, which misses
    Cratekit's own by one directory; reaching it would raise KeyError at import.
    Asserting the version against Cratekit's own catches that.
    """
    tree = ast.parse((VENDORED_PACKAGE / "__init__.py").read_text(encoding="utf-8"))

    # Asserted over the syntax tree, since the patch's comment names the filename.
    literals = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]
    assert "pyproject.toml" not in literals, (
        "the vendored package names a pyproject.toml in live code again; it will "
        "eventually read the host application's"
    )
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert "toml" not in imported, (
        "the TOML reader is back in the vendored package; the only thing it read "
        "was another project's pyproject.toml"
    )

    with PYPROJECT.open("rb") as handle:
        host_version = tomllib.load(handle)["project"]["version"]
    module = importlib.import_module("cratekit._vendor.downloader")
    assert module.__version__ != host_version
