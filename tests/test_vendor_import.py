"""U13: the vendored downloader is importable, licensed, and carries no secrets.

KTD4 vendors the downloader as a source tree because its upstream was deleted
from GitHub and PyPI in December 2025 together with its author's account. Nothing
can install it from an index any more, so a committed tree is the only shape in
which a friend's clone can acquire music at all.

Vendoring trades one failure for a set of quieter ones, and each test here pins
one of them:

* **A dependency specifier creeps back in.** Then an install starts asking an
  index for a package the index deleted, and the failure lands on somebody else's
  machine as a resolution error. Asserted over every specifier in the file.
* **The licence goes missing.** KTD19 keeps authored code MIT and each vendored
  component under its own licence. A stripped or empty AGPL text is a licensing
  defect that no runtime test would ever notice.
* **A credential rides along.** The upstream artifact really does carry
  credential material, in three separate forms, and it really does sit on disk
  next to a live session token. Asserted as an absence, per shape.
* **A tempo tag survives.** R17 has no configuration flag, and the vendored
  downloader wrote the provider's BPM into all three container formats.
* **A re-vendor drops the patches.** Every assertion below is written so that
  re-extracting upstream without re-applying the patch set goes red immediately,
  rather than in six months when somebody notices their grids moved.

What these do NOT prove is that a download works. That needs an account, an
authorised session, and the network, so it is the attended smoke test recorded in
``vendor/README.md``, not a unit test.
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
VENDORED_PACKAGE = VENDOR_ROOT / "tidal_dl_ng"
PYPROJECT = REPO_ROOT / "pyproject.toml"

# The upstream distribution name in every spelling a specifier could use. PEP 503
# normalises "-" and "_" to the same project, so checking one spelling would let
# the other through.
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
    """The whole point of KTD4, asserted as the one thing a user needs.

    Importing rather than merely checking the files exist is deliberate. The
    package imports itself absolutely throughout, so moving it under
    ``cratekit._vendor`` breaks every one of those imports unless they were
    re-rooted. A file-presence check would pass on a tree that cannot import.

    No network is touched: the module bodies build constants and class
    definitions, and the only outbound call in the package sits behind a function
    nothing here invokes.
    """
    module = importlib.import_module("cratekit._vendor.tidal_dl_ng")
    assert module.__version__, "the vendored package reports no version"


@pytest.mark.parametrize(
    "name",
    [
        "cratekit._vendor.tidal_dl_ng.cli",
        "cratekit._vendor.tidal_dl_ng.config",
        "cratekit._vendor.tidal_dl_ng.download",
        "cratekit._vendor.tidal_dl_ng.metadata",
        "cratekit._vendor.tidal_dl_ng.helper.path",
        "cratekit._vendor.tidal_dl_ng.helper.tidal",
        "cratekit._vendor.tidal_dl_ng.helper.decryption",
        "cratekit._vendor.tidal_dl_ng.model.cfg",
    ],
)
def test_every_module_on_the_download_path_imports(name):
    """One case per module U14's adapter will actually reach through.

    Parametrized so a failure names the module rather than the first one in a
    loop. These are the modules between "give me a track" and "the file is on
    disk"; a break in any of them is a break in acquisition.
    """
    assert importlib.import_module(name) is not None


def test_every_vendored_module_byte_compiles():
    """Stands in for the linter, which is excluded from the vendored tree.

    ``pyproject.toml`` excludes ``src/cratekit/_vendor`` from ruff, because
    restyling third-party code turns every lint rule into another patch to
    re-apply on the next version bump. That exclusion gives up ruff's E9 syntax
    check, so it is replaced here with something stricter for the question that
    matters: is every file in the extract valid Python for the interpreters
    KTD19 supports. This also covers the modules no import test reaches.
    """
    for source in _vendored_sources():
        compile(source.read_text(encoding="utf-8"), str(source), "exec")


def test_no_module_still_imports_itself_by_its_upstream_name():
    """A missed re-root is invisible until the branch that needs it runs.

    The package imports itself absolutely (``from tidal_dl_ng.config import
    Settings``). Every one of those has to be re-rooted under
    ``cratekit._vendor``, and a lazy import inside a rarely taken branch is
    exactly the one a manual pass misses. A source scan finds all of them.
    """
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
    """KTD4's load-bearing half.

    The moment the name appears in a specifier, an install asks an index for a
    package that index deleted, and a fresh clone stops being installable. Every
    dependency list is checked, not just the core one, because an extra is just
    as fatal to the friend who enables that module.
    """
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
    """A specifier can hide outside pyproject.toml, and one there still installs.

    A requirements file, a CI step, or an install line in a document all reach
    the same index. The check is deliberately wider than the packaging metadata
    because the failure is about what gets FETCHED, not about which file asked.
    """
    patterns = re.compile(
        r"(?:pip\s+install|uv\s+(?:pip\s+install|add)|poetry\s+add)[^\n]*"
        r"(?:tidal[-_]dl[-_]ng)",
        re.IGNORECASE,
    )
    offenders: list[str] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        # Every dot-directory is skipped, not just .git. That covers .venv,
        # .pytest_cache, and .worktrees — and the last one matters: a checkout
        # with agent worktrees under it holds whole extra copies of this
        # repository, so walking them would be slow AND would report another
        # checkout's files as findings in this one.
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
    """KTD19: authored code is MIT, the vendored component keeps its own AGPL.

    Non-empty is asserted rather than merely present because a truncated or
    placeholder licence file is the shape this fails in: something copies the
    path and forgets the contents, and nothing at runtime ever notices.
    """
    from cratekit._vendor import TIDAL_DL_NG, license_text

    text = license_text(TIDAL_DL_NG)
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" in text
    assert len(text) > 10_000, "the AGPL text is far shorter than the real licence"


def test_the_declared_licence_matches_the_text_that_ships():
    """A declared SPDX id that disagrees with the file is a licensing defect.

    It is also the exact thing a downstream audit checks first, so getting it
    wrong is worse than not declaring one.
    """
    from cratekit._vendor import TIDAL_DL_NG, license_text

    assert TIDAL_DL_NG.license_id == "AGPL-3.0-only"
    assert "Version 3, 19 November 2007" in license_text(TIDAL_DL_NG)


def test_the_two_licence_copies_cannot_drift():
    """The text ships twice, so something has to hold them equal.

    Inside the package it travels with the code it covers; at the repository root
    it is where a licence audit looks. Two copies with nothing checking them is
    how one gets updated and the other does not.
    """
    inside = (VENDORED_PACKAGE / "LICENSE").read_bytes()
    at_root = (REPO_ROOT / "vendor" / "LICENSE.tidal-dl-ng").read_bytes()
    assert inside == at_root, (
        "the two copies of the vendored licence differ; "
        "re-run scripts/revendor_downloader.py rather than editing either by hand"
    )


def test_the_licence_ships_as_package_data(pyproject):
    """Present in the checkout is not the same as present in the wheel.

    Without this entry the file exists for every contributor and for nobody who
    installs, which is precisely the population the licence is for.
    """
    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert "LICENSE" in package_data["cratekit._vendor.tidal_dl_ng"]


def test_the_recorded_version_matches_the_code_on_disk():
    """Provenance that disagrees with the tree is worse than no provenance.

    With upstream gone there is nothing to check a version against later, so the
    recorded one is the only answer to "which copy do you have". It has to be
    the truth at the moment it is read, not at the moment somebody typed it.
    """
    from cratekit._vendor import TIDAL_DL_NG

    module = importlib.import_module("cratekit._vendor.tidal_dl_ng")
    assert module.__version__ == TIDAL_DL_NG.version


# ═══════════════════════════════════════════════════════════════════════════
# No credential material, in any of the three shapes it took upstream
# ═══════════════════════════════════════════════════════════════════════════


def test_the_atmos_client_credentials_are_empty():
    """The patch that removed them must survive every future re-vendor.

    Upstream base64-encodes a third-party streaming client id and secret and
    splits each across concatenated string literals, which is a deliberate shape
    for getting past a scanner. Asserting the DECODED values are empty is what
    makes re-encoding them under a new name fail this test too.
    """
    constants = importlib.import_module("cratekit._vendor.tidal_dl_ng.constants")
    assert constants.ATMOS_CLIENT_ID == ""
    assert constants.ATMOS_CLIENT_SECRET == ""


def test_no_module_in_the_vendored_tree_carries_a_credential_literal():
    """The general form, so a NEW credential in a future version is caught too.

    The repository scan already runs over this tree and is the primary guard.
    This is narrower and stricter: any assignment or mapping entry whose name
    reads as a client credential must have an empty value. It catches the two
    shapes the repository scanner does not, because its pattern expects
    snake_case and upstream also uses camelCase JSON keys.
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
    """``api.py`` must stay out, and stay out for the reasons it went out.

    It carries five plaintext third-party client id and secret pairs, it raises
    JSONDecodeError at import because its embedded JSON uses ``//`` comments, and
    nothing in the package imports it. A re-vendor that copies the tree wholesale
    brings all three back.
    """
    assert not (VENDORED_PACKAGE / "api.py").exists(), (
        "api.py was vendored. It carries plaintext third-party OAuth client "
        "secrets and is upstream-broken at import; scripts/revendor_downloader.py "
        "drops it deliberately."
    )


def test_no_session_or_token_file_rode_along():
    """The adjacency this whole unit was warned about.

    The known-good copies of the downloader sit in a directory that also holds a
    live OAuth session cache. Extracting a directory rather than an archive's
    package subtree is how that file gets committed, and a compressed payload is
    invisible to a content scan.
    """
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
    """R17 has no configuration flag, and this tree violated it three times.

    Upstream writes the streaming provider's BPM into every file it saves: a
    Vorbis ``BPM`` comment for FLAC, an ID3 ``TBPM`` frame for MP3 and AIFF, and
    an MP4 ``tmpo`` atom. rekordbox reads file tags on import, so each one seeds
    a grid Cratekit never authored. A wrong grid is worse than none, because
    detection octave-folds and a half-time or double-time grid moves every cue
    and every loop the user ever set against that track.

    This asserts all three shapes. The repository's own R17 guard finds only the
    first: it matches subscript ASSIGNMENTS with a key in its forbidden set, so
    the ID3 write slips through as a CALL and the MP4 write slips through on a
    key name that is not in the set. Both would have shipped.
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
    """Defence in depth at the single point where the value enters.

    Removing the three writes fixes today's tree. Zeroing the value at the call
    site means a container writer added by a future upstream release has nothing
    to write, so the next version is safe before anyone reviews it.
    """
    download = (VENDORED_PACKAGE / "download.py").read_text(encoding="utf-8")
    assert "bpm=0," in download, (
        "the metadata writer is being handed the provider's tempo again; "
        "scripts/revendor_downloader.py pins it to zero (R17)"
    )


def _calls_in(function_name: str, module: str) -> set[str]:
    """Every method name a named function actually EVALUATES, from the syntax tree.

    Over the tree rather than the text, for the reason
    ``test_version_detection_does_not_read_a_nearby_pyproject`` gives: the patch
    that removed the device flow explains itself in a comment that names
    ``login_oauth_simple``, so a substring check on the source would fail on the
    fix rather than on the defect. Only a name the CODE evaluates counts.
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
    """R-196: the device-linking client is served lossy audio, so it is not offered.

    The provider gates lossless behind the PKCE client. Upstream called
    ``login_oauth_simple`` and carried the PKCE call beside it as a comment, so
    the commented line was the working one and the live one silently produced
    lossy downloads. There is no flag preserving the device flow: a flag that
    preserved it would preserve the defect.
    """
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
    """A field the write never stores is a field the read cannot see.

    Upstream persists four keys and drops ``is_pkce``, so a PKCE token reloads as
    a device-flow one and refreshes against the client the provider serves lossy.
    """
    from cratekit._vendor.tidal_dl_ng.model.cfg import Token

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
    """Every one of these imports PySide6 at module scope.

    PySide6 is an optional upstream extra that Cratekit does not install, so in a
    Cratekit environment none of them can import at all. Shipping a module that
    provably cannot import is not caution, it is a trap for the next reader. It
    also drags 356 KB of icon binaries and two dependencies that nothing on the
    download path uses.
    """
    assert not (VENDORED_PACKAGE / relative).exists()


def test_the_download_path_needs_no_gui_toolkit(pyproject):
    """The reduction has to show up in the dependency list, or it saved nothing."""
    declared = " ".join(pyproject["project"]["dependencies"]).lower()
    for gui_only in ("pyside6", "pyqtdarktheme", "ansi2html", "coloredlogs"):
        assert gui_only not in declared, (
            f"{gui_only} is declared but only the un-vendored GUI half used it"
        )


def test_the_state_directory_name_is_pinned():
    """``__name_display__`` names a directory on disk, not a label.

    It is derived from ``__package__`` upstream, and it decides where the
    settings file, the log, and the persisted token live. Vendored, that
    derivation yields the internal import path plus a "-dev" suffix, so the tool
    would write its state to a directory named after ``cratekit._vendor``.
    """
    module = importlib.import_module("cratekit._vendor.tidal_dl_ng")
    assert module.__name_display__ == "tidal-dl-ng"
    assert "cratekit" not in module.__name_display__


def test_version_detection_does_not_read_a_nearby_pyproject():
    """The sharpest hazard vendoring introduced, pinned so it cannot return.

    Upstream walks up to three parent directories from its own ``__file__``
    looking for a ``pyproject.toml`` and reads another project's version out of
    whichever it finds. Under ``src/cratekit/_vendor/tidal_dl_ng/`` those parents
    are ``tidal_dl_ng``, ``_vendor``, and ``cratekit``; Cratekit's own file sits
    one level beyond, so today the walk misses it by a single directory. Were it
    ever reached, the repository-URL lookup would raise KeyError outside
    upstream's try block and ``import`` itself would fail.

    Asserting the version against Cratekit's own is the point: if the walk ever
    found the host's file, these two would be equal.
    """
    tree = ast.parse((VENDORED_PACKAGE / "__init__.py").read_text(encoding="utf-8"))

    # Asserted over the syntax tree, not over the file text. The patch that
    # removed this behaviour explains it in a comment that names the filename, so
    # a substring check on the source would fail on the fix rather than on the
    # defect. Only a string the CODE evaluates counts.
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
    module = importlib.import_module("cratekit._vendor.tidal_dl_ng")
    assert module.__version__ != host_version
